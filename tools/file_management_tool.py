def read_file(path: str) -> str:
    """
    Read the contents of a file.
    Args:
        path (str): The file path to read.
    Returns:
        str: The file contents or error message.
    """
    print(f"[Tool] Reading file: {path}")
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return str(e)

def write_file(path: str, content: str) -> str:
    """
    Write content to a file.
    Args:
        path (str): The file path to write to.
        content (str): The content to write.
    Returns:
        str: Success message or error message.
    """
    print(f"[Tool] Writing to file: {path}")
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return "Write successful"
    except Exception as e:
        return str(e) 