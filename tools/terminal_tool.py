import subprocess

def run_terminal_command(command: str) -> str:
    """
    Run a shell command on the system and return its output.
    Args:
        command (str): The shell command to run.
    Returns:
        str: The command output or error message.
    """
    print(f"[Tool] Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return "Command output: " + result.stdout
    except Exception as e:
        return "ERROR: " + str(e) 