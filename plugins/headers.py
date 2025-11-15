import requests
class HeaderAnalyzer:
    name = 'Header Analyzer'
    def __init__(self, url):
        self.url = url
    def run(self):
        try:
            res = requests.get(self.url, timeout=5)
        except Exception as e:
            return {'error': str(e)}
        missing = []
        security_headers = ['X-Content-Type-Options','X-Frame-Options','Strict-Transport-Security','Content-Security-Policy']
        for h in security_headers:
            if h not in res.headers:
                missing.append(h)
        return {'missing': missing}
