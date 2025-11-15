import requests, re
from bs4 import BeautifulSoup

class DOMXSSScanner:
    name = 'DOM XSS Scanner'
    SUSPICIOUS = [r'document\.write\(', r'innerHTML', r'location\.hash', r'location\.search', r'eval\(']
    def __init__(self, url):
        self.url = url
    def run(self):
        findings = []
        try:
            res = requests.get(self.url, timeout=5)
        except Exception as e:
            return {'error': str(e)}
        soup = BeautifulSoup(res.text, 'lxml')
        scripts = soup.find_all('script')
        for s in scripts:
            txt = (s.string or '')
            for pat in self.SUSPICIOUS:
                if re.search(pat, txt or '', re.IGNORECASE):
                    findings.append({'script': (txt or '')[:200], 'pattern': pat})
        return findings
