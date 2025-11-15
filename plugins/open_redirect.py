import requests
class OpenRedirectChecker:
    name = 'Open Redirect Checker'
    def __init__(self, url):
        self.url = url
    def run(self):
        # simple heuristic: check redirect behavior for a known external host
        test = self.url
        try:
            res = requests.get(test, timeout=5, allow_redirects=True)
        except Exception as e:
            return {'error': str(e)}
        # we can't fully test without parameters; return status code and final URL
        return {'status_code': res.status_code, 'final_url': res.url}
