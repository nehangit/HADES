import os
from config import SANDBOX_ROOT

# Ensure the directory exists
os.makedirs(SANDBOX_ROOT, exist_ok=True)

def read_file(path: str) -> str:
    """
    Read the contents of a file from within the agent workspace.

    Args:
        path (str): Relative path inside the sandbox.
    Returns:
        str: The file contents or error message.
    """
    full_path = os.path.abspath(os.path.join(SANDBOX_ROOT, path))
    print(f"[Tool] Reading file: {full_path}")

    # Security check: prevent directory traversal
    if not full_path.startswith(SANDBOX_ROOT):
        return "Access denied: Outside of agent workspace"

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return str(e)

def write_file(path: str, content: str) -> str:
    """
    Write content to a file within the agent workspace.

    Args:
        path (str): Relative path inside the sandbox.
        content (str): The content to write.
    Returns:
        str: Success message or error message.
    """
    full_path = os.path.abspath(os.path.join(SANDBOX_ROOT, path))
    print(f"[Tool] Writing to file: {full_path}")

    # Security check: prevent directory traversal
    if not full_path.startswith(SANDBOX_ROOT):
        return "Access denied: Outside of agent workspace"

    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return "Write successful"
    except Exception as e:
        return str(e)
