from bs4 import BeautifulSoup

def simplify_html(html):
    print("[Utils] Simplifying HTML...")
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["img", "svg", "style", "script", "link", "meta", "iframe", "object", "embed", "noscript"]):
        tag.decompose()
    return str(soup) 