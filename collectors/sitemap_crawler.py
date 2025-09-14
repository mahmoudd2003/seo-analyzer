
from typing import List, Set
import requests
from lxml import etree

def extract_urls_from_sitemap(sitemap_url: str, respect_robots: bool = False, timeout: int = 20) -> List[str]:
    # Minimal sitemap reader (no robots handling in this stub)
    r = requests.get(sitemap_url, timeout=timeout)
    r.raise_for_status()
    content = r.content
    root = etree.fromstring(content)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = []
    # If it's a sitemap index
    if root.tag.endswith("sitemapindex"):
        for sm_el in root.findall(".//sm:sitemap/sm:loc", ns):
            child_url = sm_el.text.strip()
            urls.extend(extract_urls_from_sitemap(child_url, respect_robots=respect_robots, timeout=timeout))
    else:
        for loc in root.findall(".//sm:url/sm:loc", ns):
            urls.append(loc.text.strip())
    # Deduplicate
    return list(dict.fromkeys(urls))
