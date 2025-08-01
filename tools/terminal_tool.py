import subprocess
from config import SANDBOX_ROOT

def run_terminal_command(command: str) -> str:
    """
    Run any bash command on the Ubuntu Linux terminal and return the full output (stdout and stderr). You do not have root permissions.

    Args:
        command (str): The shell command to run.
    Returns:
        str: The command output or error message.
    """
    print(f"[Tool] Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=SANDBOX_ROOT)
        if result.returncode == 0:
            return "Command output: " + result.stdout
        else:
            return f"ERROR (code {result.returncode}): " + result.stderr
    except Exception as e:
        return f"TOOL ERROR: {str(e)}"