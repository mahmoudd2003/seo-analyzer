
from bs4 import BeautifulSoup

def extract_main_text(html: str) -> str:
    """Very light boilerplate removal: drops scripts/styles and returns page text.
    You can later replace with 'trafilatura' for better accuracy.":
    """
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script","style","noscript","template","header","footer","nav","aside"]):
        tag.extract()
    text = soup.get_text(" ", strip=True)
    return text
