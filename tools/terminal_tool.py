import subprocess

def run_terminal_command(command: str) -> str:
    """
    Run any bash command on the Kali Linux terminal and return the full output (stdout and stderr). Use this to execute reconnaissance, exploitation, or interact with CLI tools like curl.
    Args:
        command (str): The shell command to run.
    Returns:
        str: The command output or error message.
    """
    print(f"[Tool] Running command: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return "Command output: " + result.stdout
        else:
            return f"ERROR (code {result.returncode}): " + result.stderr
    except Exception as e:
        return f"TOOL ERROR: {str(e)}"