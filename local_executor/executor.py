import ast
import builtins
import logging
import math
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class InterpreterError(ValueError):
    """
    An error raised when the interpreter cannot evaluate a Python expression, due to syntax error or unsupported
    operations.
    """
    pass


ERRORS = {
    name: getattr(builtins, name)
    for name in dir(builtins)
    if isinstance(getattr(builtins, name), type) and issubclass(getattr(builtins, name), BaseException)
}

DEFAULT_MAX_LEN_OUTPUT = 50000
MAX_OPERATIONS = 10000000
MAX_WHILE_ITERATIONS = 1000000

BASE_BUILTIN_MODULES = [
    "math",
    "random",
    "datetime",
    "time",
    "json",
    "re",
    "string",
    "collections",
    "itertools",
    "functools",
    "operator",
]

BASE_PYTHON_TOOLS = {
    "print": lambda *args: None,  # Custom print that does nothing
    "isinstance": isinstance,
    "range": range,
    "float": float,
    "int": int,
    "bool": bool,
    "str": str,
    "set": set,
    "list": list,
    "dict": dict,
    "tuple": tuple,
    "round": round,
    "ceil": math.ceil,
    "floor": math.floor,
    "log": math.log,
    "exp": math.exp,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "atan2": math.atan2,
    "degrees": math.degrees,
    "radians": math.radians,
    "pow": pow,
    "sqrt": math.sqrt,
    "len": len,
    "sum": sum,
    "max": max,
    "min": min,
    "abs": abs,
    "enumerate": enumerate,
    "zip": zip,
    "reversed": reversed,
    "sorted": sorted,
    "all": all,
    "any": any,
    "map": map,
    "filter": filter,
    "ord": ord,
    "chr": chr,
    "next": next,
    "iter": iter,
    "divmod": divmod,
    "callable": callable,
    "getattr": getattr,
    "hasattr": hasattr,
    "setattr": setattr,
    "issubclass": issubclass,
    "type": type,
    "complex": complex,
}

DANGEROUS_FUNCTIONS = [
    "builtins.compile",
    "builtins.eval",
    "builtins.exec",
    "builtins.globals",
    "builtins.locals",
    "builtins.__import__",
    "os.popen",
    "os.system",
    "posix.system",
]


class PrintContainer:
    def __init__(self):
        self.value = ""

    def append(self, text):
        self.value += text
        return self

    def __iadd__(self, other):
        """Implements the += operator"""
        self.value += str(other)
        return self

    def __str__(self):
        """String representation"""
        return self.value

    def __repr__(self):
        """Representation for debugging"""
        return f"PrintContainer({self.value})"

    def __len__(self):
        """Implements len() function support"""
        return len(self.value)


class BreakException(Exception):
    pass


class ContinueException(Exception):
    pass


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class FinalAnswerException(Exception):
    def __init__(self, value):
        self.value = value


def truncate_content(content: str, max_length: int = DEFAULT_MAX_LEN_OUTPUT) -> str:
    """Truncate content to a maximum length."""
    if len(content) <= max_length:
        return content
    return content[:max_length] + "..."


def evaluate_ast(
    expression: ast.AST,
    state: Dict[str, Any],
    static_tools: Dict[str, Callable],
    authorized_imports: List[str] = BASE_BUILTIN_MODULES,
) -> Any:
    """
    Evaluate an abstract syntax tree using the content of the variables stored in a state and only evaluating a given set
    of functions.

    Args:
        expression (`ast.AST`):
            The code to evaluate, as an abstract syntax tree.
        state (`Dict[str, Any]`):
            A dictionary mapping variable names to values. The `state` is updated if need be when the evaluation
            encounters assignments.
        static_tools (`Dict[str, Callable]`):
            Functions that may be called during the evaluation.
        authorized_imports (`List[str]`):
            The list of modules that can be imported by the code.

    Returns:
        Any: The result of evaluating the AST.
    """
    if state.setdefault("_operations_count", {"counter": 0})["counter"] >= MAX_OPERATIONS:
        raise InterpreterError(
            f"Reached the max number of operations of {MAX_OPERATIONS}. Maybe there is an infinite loop somewhere in the code, or you're just asking too many calculations."
        )
    state["_operations_count"]["counter"] += 1

    if isinstance(expression, ast.Constant):
        return expression.value
    elif isinstance(expression, ast.Name):
        if expression.id in state:
            return state[expression.id]
        elif expression.id in static_tools:
            return static_tools[expression.id]
        elif expression.id in ERRORS:
            return ERRORS[expression.id]
        raise InterpreterError(f"The variable `{expression.id}` is not defined.")
    elif isinstance(expression, ast.BinOp):
        left = evaluate_ast(expression.left, state, static_tools, authorized_imports)
        right = evaluate_ast(expression.right, state, static_tools, authorized_imports)
        if isinstance(expression.op, ast.Add):
            return left + right
        elif isinstance(expression.op, ast.Sub):
            return left - right
        elif isinstance(expression.op, ast.Mult):
            return left * right
        elif isinstance(expression.op, ast.Div):
            return left / right
        elif isinstance(expression.op, ast.Mod):
            return left % right
        elif isinstance(expression.op, ast.Pow):
            return left ** right
        elif isinstance(expression.op, ast.FloorDiv):
            return left // right
        elif isinstance(expression.op, ast.BitAnd):
            return left & right
        elif isinstance(expression.op, ast.BitOr):
            return left | right
        elif isinstance(expression.op, ast.BitXor):
            return left ^ right
        elif isinstance(expression.op, ast.LShift):
            return left << right
        elif isinstance(expression.op, ast.RShift):
            return left >> right
        else:
            raise InterpreterError(f"Binary operation {type(expression.op).__name__} is not supported.")
    elif isinstance(expression, ast.UnaryOp):
        operand = evaluate_ast(expression.operand, state, static_tools, authorized_imports)
        if isinstance(expression.op, ast.USub):
            return -operand
        elif isinstance(expression.op, ast.UAdd):
            return operand
        elif isinstance(expression.op, ast.Not):
            return not operand
        elif isinstance(expression.op, ast.Invert):
            return ~operand
        else:
            raise InterpreterError(f"Unary operation {type(expression.op).__name__} is not supported.")
    elif isinstance(expression, ast.Compare):
        left = evaluate_ast(expression.left, state, static_tools, authorized_imports)
        result = True
        for i, (op, comparator) in enumerate(zip(expression.ops, expression.comparators)):
            right = evaluate_ast(comparator, state, static_tools, authorized_imports)
            if isinstance(op, ast.Eq):
                current_result = left == right
            elif isinstance(op, ast.NotEq):
                current_result = left != right
            elif isinstance(op, ast.Lt):
                current_result = left < right
            elif isinstance(op, ast.LtE):
                current_result = left <= right
            elif isinstance(op, ast.Gt):
                current_result = left > right
            elif isinstance(op, ast.GtE):
                current_result = left >= right
            elif isinstance(op, ast.Is):
                current_result = left is right
            elif isinstance(op, ast.IsNot):
                current_result = left is not right
            elif isinstance(op, ast.In):
                current_result = left in right
            elif isinstance(op, ast.NotIn):
                current_result = left not in right
            else:
                raise InterpreterError(f"Unsupported comparison operator: {type(op)}")

            if current_result is False:
                return False
            result = current_result if i == 0 else (result and current_result)
            left = right
        return result
    elif isinstance(expression, ast.BoolOp):
        if isinstance(expression.op, ast.And):
            for value in expression.values:
                if not evaluate_ast(value, state, static_tools, authorized_imports):
                    return False
            return True
        elif isinstance(expression.op, ast.Or):
            for value in expression.values:
                if evaluate_ast(value, state, static_tools, authorized_imports):
                    return True
            return False
    elif isinstance(expression, ast.Call):
        func = evaluate_ast(expression.func, state, static_tools, authorized_imports)
        args = [evaluate_ast(arg, state, static_tools, authorized_imports) for arg in expression.args]
        kwargs = {
            keyword.arg: evaluate_ast(keyword.value, state, static_tools, authorized_imports)
            for keyword in expression.keywords
        }
        return func(*args, **kwargs)
    elif isinstance(expression, ast.Assign):
        value = evaluate_ast(expression.value, state, static_tools, authorized_imports)
        for target in expression.targets:
            if isinstance(target, ast.Name):
                if target.id in static_tools:
                    raise InterpreterError(f"Cannot assign to name '{target.id}': doing this would erase the existing tool!")
                state[target.id] = value
            elif isinstance(target, ast.Tuple):
                if not isinstance(value, tuple):
                    if hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
                        value = tuple(value)
                    else:
                        raise InterpreterError("Cannot unpack non-tuple value")
                if len(target.elts) != len(value):
                    raise InterpreterError("Cannot unpack tuple of wrong size")
                for i, elem in enumerate(target.elts):
                    if isinstance(elem, ast.Name):
                        state[elem.id] = value[i]
                    else:
                        raise InterpreterError(f"Unsupported assignment target: {type(elem)}")
            else:
                raise InterpreterError(f"Unsupported assignment target: {type(target)}")
        return value
    elif isinstance(expression, ast.Expr):
        return evaluate_ast(expression.value, state, static_tools, authorized_imports)
    elif isinstance(expression, ast.If):
        test_result = evaluate_ast(expression.test, state, static_tools, authorized_imports)
        if test_result:
            for node in expression.body:
                result = evaluate_ast(node, state, static_tools, authorized_imports)
        else:
            result = None
            for node in expression.orelse:
                result = evaluate_ast(node, state, static_tools, authorized_imports)
        return result
    elif isinstance(expression, ast.For):
        iter_value = evaluate_ast(expression.iter, state, static_tools, authorized_imports)
        result = None
        for value in iter_value:
            if isinstance(expression.target, ast.Name):
                state[expression.target.id] = value
            elif isinstance(expression.target, ast.Tuple):
                if not isinstance(value, tuple):
                    if hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
                        value = tuple(value)
                    else:
                        raise InterpreterError("Cannot unpack non-tuple value")
                if len(expression.target.elts) != len(value):
                    raise InterpreterError("Cannot unpack tuple of wrong size")
                for i, elem in enumerate(expression.target.elts):
                    if isinstance(elem, ast.Name):
                        state[elem.id] = value[i]
                    else:
                        raise InterpreterError(f"Unsupported assignment target: {type(elem)}")
            else:
                raise InterpreterError(f"Unsupported assignment target: {type(expression.target)}")
            for node in expression.body:
                try:
                    result = evaluate_ast(node, state, static_tools, authorized_imports)
                except BreakException:
                    return result
                except ContinueException:
                    break
        return result
    elif isinstance(expression, ast.While):
        iterations = 0
        while evaluate_ast(expression.test, state, static_tools, authorized_imports):
            for node in expression.body:
                try:
                    evaluate_ast(node, state, static_tools, authorized_imports)
                except BreakException:
                    return None
                except ContinueException:
                    break
            iterations += 1
            if iterations > MAX_WHILE_ITERATIONS:
                raise InterpreterError(f"Maximum number of {MAX_WHILE_ITERATIONS} iterations in While loop exceeded")
        return None
    elif isinstance(expression, ast.Break):
        raise BreakException()
    elif isinstance(expression, ast.Continue):
        raise ContinueException()
    elif isinstance(expression, ast.Return):
        if expression.value:
            raise ReturnException(evaluate_ast(expression.value, state, static_tools, authorized_imports))
        raise ReturnException(None)
    elif isinstance(expression, ast.FunctionDef):
        def new_func(*args: Any, **kwargs: Any) -> Any:
            func_state = state.copy()
            arg_names = [arg.arg for arg in expression.args.args]
            default_values = [
                evaluate_ast(d, state, static_tools, authorized_imports)
                for d in expression.args.defaults
            ]
            defaults = dict(zip(arg_names[-len(default_values):], default_values))
            for name, value in zip(arg_names, args):
                func_state[name] = value
            for name, value in kwargs.items():
                func_state[name] = value
            if expression.args.vararg:
                vararg_name = expression.args.vararg.arg
                func_state[vararg_name] = args
            if expression.args.kwarg:
                kwarg_name = expression.args.kwarg.arg
                func_state[kwarg_name] = kwargs
            for name, value in defaults.items():
                if name not in func_state:
                    func_state[name] = value
            if expression.args.args and expression.args.args[0].arg == "self":
                if args:
                    func_state["self"] = args[0]
                    func_state["__class__"] = args[0].__class__
            result = None
            try:
                for stmt in expression.body:
                    result = evaluate_ast(stmt, func_state, static_tools, authorized_imports)
            except ReturnException as e:
                result = e.value
            if expression.name == "__init__":
                return None
            return result
        return new_func
    else:
        raise InterpreterError(f"{expression.__class__.__name__} is not supported.")


def evaluate_python_code(
    code: str,
    static_tools: Optional[Dict[str, Callable]] = None,
    state: Optional[Dict[str, Any]] = None,
    authorized_imports: List[str] = BASE_BUILTIN_MODULES,
    max_print_outputs_length: int = DEFAULT_MAX_LEN_OUTPUT,
):
    """
    Evaluate a python expression using the content of the variables stored in a state and only evaluating a given set
    of functions.

    Args:
        code (`str`):
            The code to evaluate.
        static_tools (`Dict[str, Callable]`):
            The functions that may be called during the evaluation.
        state (`Dict[str, Any]`):
            A dictionary mapping variable names to values. The state will be updated with all variables as they are evaluated.
        authorized_imports (`List[str]`):
            The list of modules that can be imported by the code.
        max_print_outputs_length (`int`):
            Maximum length of print outputs to keep.

    Returns:
        Tuple[Any, str, bool]: The result of the code execution, the logs, and whether it was a final answer.
    """
    try:
        expression = ast.parse(code)
    except SyntaxError as e:
        raise InterpreterError(
            f"Code parsing failed on line {e.lineno} due to: {type(e).__name__}\n"
            f"{e.text}"
            f"{' ' * (e.offset or 0)}^\n"
            f"Error: {str(e)}"
        )

    if state is None:
        state = {}
    static_tools = static_tools.copy() if static_tools is not None else {}
    state["_print_outputs"] = PrintContainer()
    state["_operations_count"] = {"counter": 0}

    if "final_answer" in static_tools:
        previous_final_answer = static_tools["final_answer"]

        def final_answer(answer):
            raise FinalAnswerException(previous_final_answer(answer))

        static_tools["final_answer"] = final_answer

    try:
        for node in expression.body:
            result = evaluate_ast(node, state, static_tools, authorized_imports)
        state["_print_outputs"].value = truncate_content(
            str(state["_print_outputs"]), max_length=max_print_outputs_length
        )
        is_final_answer = False
        return result, is_final_answer
    except FinalAnswerException as e:
        state["_print_outputs"].value = truncate_content(
            str(state["_print_outputs"]), max_length=max_print_outputs_length
        )
        is_final_answer = True
        return e.value, is_final_answer
    except Exception as e:
        state["_print_outputs"].value = truncate_content(
            str(state["_print_outputs"]), max_length=max_print_outputs_length
        )
        raise InterpreterError(
            f"Code execution failed at line '{ast.get_source_segment(code, node)}' due to: {type(e).__name__}: {e}"
        )


class LocalPythonExecutor:
    """A class for safely executing Python code in a controlled environment."""

    def __init__(
        self,
        additional_authorized_imports: List[str],
        max_print_outputs_length: Optional[int] = None,
    ):
        """
        Initialize the executor.

        Args:
            additional_authorized_imports (`List[str]`):
                Additional modules that can be imported by the code.
            max_print_outputs_length (`Optional[int]`):
                Maximum length of print outputs to keep.
        """
        self.state = {}
        self.max_print_outputs_length = max_print_outputs_length
        if max_print_outputs_length is None:
            self.max_print_outputs_length = DEFAULT_MAX_LEN_OUTPUT
        self.additional_authorized_imports = additional_authorized_imports
        self.authorized_imports = list(set(BASE_BUILTIN_MODULES) | set(self.additional_authorized_imports))
        self.static_tools = None

    def __call__(self, code_action: str) -> Tuple[Any, str, bool]:
        """
        Execute the given code.

        Args:
            code_action (`str`):
                The Python code to execute.

        Returns:
            Tuple[Any, str, bool]: The result of the code execution, the logs, and whether it was a final answer.
        """
        output, is_final_answer = evaluate_python_code(
            code_action,
            static_tools=self.static_tools,
            state=self.state,
            authorized_imports=self.authorized_imports,
            max_print_outputs_length=self.max_print_outputs_length,
        )
        logs = str(self.state["_print_outputs"])
        return output, logs, is_final_answer

    def send_variables(self, variables: dict):
        """
        Set variables in the execution environment.

        Args:
            variables (`dict`):
                Dictionary of variable names and their values.
        """
        self.state.update(variables)
