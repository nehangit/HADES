import subprocess

def run_sqlmap_scan(url: str) -> str:
    """
    Run sqlmap to scan a URL for SQL injection vulnerabilities.
    Args:
        url (str): The URL to scan.
    Returns:
        str: The output from sqlmap.
    """
    print(f"[Tool] Scanning {url} with sqlmap...")
    try:
        result = subprocess.run(f"sqlmap -u {url} --batch", shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e) 