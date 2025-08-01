from typing import Optional
from config import SANDBOX_ROOT
import subprocess

def run_sqlmap_scan(
    target_url: str,
    method: Optional[str] = None,
    data: Optional[str] = None,
    cookie: Optional[str] = None,
    level: int = 1,
    risk: int = 1,
    dump: bool = False
) -> str:
    """
    Run sqlmap against a target URL to detect and exploit SQL injection vulnerabilities.

    Args:
        target_url (str): The full URL to test for SQL injection.
        method (str, optional): HTTP method to use.
        data (str, optional): POST body (if applicable).
        cookie (str, optional): Cookie string to include.
        level (int, optional): Testing level (1–5). Higher is more aggressive.
        risk (int, optional): Risk level (1–3). Higher tries more dangerous payloads.
        dump (bool, optional): Whether to dump database contents if vulnerable.

    Returns:
        str: Output from sqlmap command.
    """
    command = ["sqlmap", "-u", target_url, f"--level={level}", f"--risk={risk}", "--batch"]

    if method:
        command.extend(["--method", method.upper()])
    if data:
        command.extend(["--data", data])
    if cookie:
        command.extend(["--cookie", cookie])
    if dump:
        command.append("--dump")

    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=SANDBOX_ROOT, timeout=300)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return f"TOOL ERROR: {str(e)}"