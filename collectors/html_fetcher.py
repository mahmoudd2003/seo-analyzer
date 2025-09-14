
from typing import Tuple, Optional
import httpx
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": "SEO-SystemBot/1.0 (+https://example.com/bot)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ar,en;q=0.9",
}

async def _async_fetch(url: str, timeout: int = 20) -> Tuple[int, str]:
    async with httpx.AsyncClient(follow_redirects=True, headers=DEFAULT_HEADERS, timeout=timeout) as client:
        r = await client.get(url)
        return r.status_code, r.text

def fetch(url: str, timeout: int = 20) -> Tuple[int, str]:
    """Sync wrapper around httpx to avoid forcing async in Streamlit."""
    with httpx.Client(follow_redirects=True, headers=DEFAULT_HEADERS, timeout=timeout) as client:
        r = client.get(url)
        return r.status_code, r.text

def extract_basic_fields(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    # Title/H1
    h1 = soup.find("h1")
    h1_text = (h1.get_text(strip=True) if h1 else "")[:300]
    title_tag = soup.find("title")
    title_text = (title_tag.get_text(strip=True) if title_tag else "")[:300]

    # Visible text length (quick heuristic)
    for tag in soup(["script","style","noscript","template"]):
        tag.extract()
    text = soup.get_text(" ", strip=True)
    text_len = len(text)
    html_len = len(html)

    # Count images and alts
    imgs = soup.find_all("img")
    imgs_no_alt = sum(1 for im in imgs if not im.get("alt"))

    # Simple dates (best effort)
    pub_date = ""
    mod_date = ""
    for meta in soup.find_all("meta"):
        n = (meta.get("name") or meta.get("property") or "").lower()
        if n in ("article:published_time","pubdate","date"):
            pub_date = meta.get("content","")[:30] or pub_date
        if n in ("article:modified_time","og:updated_time","lastmod"):
            mod_date = meta.get("content","")[:30] or mod_date

    return {
        "h1": h1_text,
        "title": title_text,
        "text": text,
        "text_len": text_len,
        "html_len": html_len,
        "imgs_no_alt": imgs_no_alt,
        "pub_date": pub_date,
        "mod_date": mod_date,
    }
