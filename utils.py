import inspect


def caller_info():
    stack = inspect.stack()
    caller_function = stack[1].function  # Get the function name of the caller
    print(f"Called from: {caller_function}")
