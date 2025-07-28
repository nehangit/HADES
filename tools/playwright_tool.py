from playwright.sync_api import sync_playwright
from utils.html_simplifier import simplify_html

class PlaywrightSession:
    def __init__(self):
        """Initialize a new Playwright browser session."""
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def goto(self, url: str) -> str:
        """
        Navigate to a given URL and return the simplified HTML content of the page.
        Input: A string representing a full URL (e.g., "https://example.com").
        Output: Simplified HTML as a string.
        """
        self.page.goto(url)
        return simplify_html(self.page.content())

    def fill(self, selector_and_value: str) -> str:
        """
        Fill a form input field using a CSS selector and a value.
        Input: A string in the format "selector|value", e.g., "input[name='username']|admin".
        Output: Confirmation message or error string.
        """
        try:
            selector, value = selector_and_value.split("|", 1)
            self.page.fill(selector, value)
            return f"Filled {selector} with {value}"
        except Exception as e:
            return f"Error filling form: {e}"

    def click(self, selector: str) -> str:
        """
        Click an element on the page using its CSS selector.
        Input: A string representing a CSS selector (e.g., "button[type='submit']").
        Output: Confirmation message or error string.
        """
        try:
            self.page.click(selector)
            return f"Clicked on {selector}"
        except Exception as e:
            return f"Error clicking: {e}"

    def content(self) -> str:
        """
        Get the current page's simplified HTML content.
        Input: None.
        Output: Simplified HTML as a string.
        """
        return simplify_html(self.page.content())

    def close(self):
        """Close the browser and stop Playwright."""
        self.browser.close()
        self.p.stop()
