import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract

BASE_URL = "https://site.gctu.edu.gh"
VISITED = set()
MAX_DEPTH = 2

def is_valid(url):
    # Stay within site.gctu.edu.gh and ignore certain paths, focus on IT department
    parsed = urlparse(url)
    domain = tldextract.extract(parsed.netloc).domain
    path = parsed.path.lower()
    # Focus on IT-related paths: computer science, information technology, etc.
    it_keywords = ["it", "computer", "information", "technology", "cs", "ict", "software", "engineering"]
    is_it_related = any(keyword in path for keyword in it_keywords)
    return (
        "gctu" in domain and
        all(x not in url for x in ["#", "mailto:", ".pdf", "/wp-login", "/contact", "javascript:"]) and
        (is_it_related or "gs.gctu.edu.gh" in url)  # Include graduate school which has IT programmes
    )

def crawl(url, depth=0):
    if depth > MAX_DEPTH or url in VISITED:
        return []

    VISITED.add(url)
    urls = [url]
    try:
        resp = requests.get(url, timeout=5)
        soup = BeautifulSoup(resp.content, "html.parser")
        for a in soup.find_all("a", href=True):
            next_url = urljoin(url, a['href'])
            if is_valid(next_url):
                urls += crawl(next_url, depth + 1)
    except Exception as e:
        print(f"Error visiting {url}: {e}")
    return urls

if __name__ == "__main__":
    all_urls = crawl(BASE_URL)
    unique_urls = list(set(all_urls))
    print(f"✅ Found {len(unique_urls)} useful URLs.")
    with open("gctu_urls.txt", "w") as f:
        f.write("\n".join(unique_urls))
