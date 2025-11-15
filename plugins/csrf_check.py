import requests
from bs4 import BeautifulSoup
class CSRFChecker:
    name = 'CSRF Token Checker'
    def __init__(self, url):
        self.url = url
    def run(self):
        try:
            res = requests.get(self.url, timeout=5)
        except Exception as e:
            return {'error': str(e)}
        soup = BeautifulSoup(res.text, 'lxml')
        forms = soup.find_all('form')
        missing = []
        for i, f in enumerate(forms):
            if not (f.find('input', {'name':'csrf_token'}) or f.find('input', {'name':'_csrf'})):
                missing.append({'form_index': i, 'action': f.get('action')})
        return {'forms_missing_csrf': missing}
