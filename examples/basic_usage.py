from local_executor import LocalPythonExecutor


def main():
    # Initialize the executor
    executor = LocalPythonExecutor(additional_authorized_imports=[])

    # Example 1: Simple arithmetic
    print("\nExample 1: Simple arithmetic")
    code = "2 + 2"
    result, logs, is_final_answer = executor(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    print(f"Logs: {logs}")
    print(f"Is final answer: {is_final_answer}")

    # Example 2: Using print statements
    print("\nExample 2: Using print statements")
    code = """
x = 10
y = 20
result = x + y
"""
    result, logs, is_final_answer = executor(code)
    print(f"Code: {code}")
    print(f"Result: {result}")
    print(f"Logs: {logs}")
    print(f"Is final answer: {is_final_answer}")


if __name__ == "__main__":
    main()
