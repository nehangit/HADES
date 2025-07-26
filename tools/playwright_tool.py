from playwright.sync_api import sync_playwright
from utils.html_simplifier import simplify_html

def browse_with_playwright(url: str) -> str:
    """
    Browse a web page using Playwright and return the simplified HTML content.
    Args:
        url (str): The URL to browse.
    Returns:
        str: Simplified HTML content of the page.
    """
    print(f"[Tool] Browsing {url}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        html = page.content()
        browser.close()
    return simplify_html(html) 