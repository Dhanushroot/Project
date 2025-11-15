import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, base_url, max_depth=2, allowed_domain=None, timeout=5):
        self.base = base_url
        self.max_depth = max_depth
        self.timeout = timeout
        self.allowed_domain = allowed_domain or urlparse(base_url).netloc
        self.visited = set()

    def _allowed(self, url):
        parsed = urlparse(url)
        return parsed.netloc == '' or parsed.netloc == self.allowed_domain

    def crawl(self):
        to_visit = [(self.base, 0)]
        results = set()
        while to_visit:
            url, depth = to_visit.pop(0)
            if depth > self.max_depth:
                continue
            if url in self.visited:
                continue
            try:
                res = requests.get(url, timeout=self.timeout)
            except Exception:
                self.visited.add(url)
                continue
            self.visited.add(url)
            results.add(url)
            soup = BeautifulSoup(res.text, 'lxml')
            for a in soup.find_all('a', href=True):
                href = a['href']
                full = urljoin(url, href)
                if self._allowed(full) and full not in self.visited:
                    to_visit.append((full, depth + 1))
        return list(results)
