import subprocess

def run_zap_scan(url: str) -> str:
    """
    Run ZAP to scan a URL for web vulnerabilities.
    Args:
        url (str): The URL to scan.
    Returns:
        str: The output from ZAP.
    """
    print(f"[Tool] Scanning {url} with ZAP...")
    try:
        result = subprocess.run(f"zap.sh -cmd -quickurl {url}", shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e) 