import subprocess

def run_zap_scan(
    target_url: str,
    active_scan: bool = False,
    timeout_sec: int = 600
) -> str:
    """
    Run OWASP ZAP CLI scan on the target URL and return the CLI output.

    Args:
        target_url (str): URL to scan.
        active_scan (bool): If True, perform active scan; else passive only. Default is False (passive scan).
        timeout_sec (int): Max time to wait for the scan (seconds). Default is 600 seconds.

    Returns:
        str: ZAP CLI output or error message.
    """
    try:
        cmd = [
            "zap.sh",
            "-cmd",
            "-quickurl", target_url
        ]

        if active_scan:
            cmd.append("-quickscan")
        else:
            cmd.append("-quickpassive")

        # Run zap.sh command and capture stdout and stderr
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)

        if result.returncode != 0:
            return f"[ZAP ERROR] {result.stderr.strip()}"

        # Return combined output (stdout + stderr)
        output = result.stdout.strip()
        if result.stderr.strip():
            output += "\n[ZAP STDERR]\n" + result.stderr.strip()
        return output

    except subprocess.TimeoutExpired:
        return "ERROR: Scan timed out."
    except Exception as e:
        return f"TOOL ERROR: {str(e)}"
