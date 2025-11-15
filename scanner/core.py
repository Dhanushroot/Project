import concurrent.futures
from .xss import XSSScanner
from .sqli import SQLiScanner
from .sqli_time import SQLiTimeScanner
from .dom_xss import DOMXSSScanner
from plugins.headers import HeaderAnalyzer
from plugins.csrf_check import CSRFChecker
from plugins.open_redirect import OpenRedirectChecker

class Scanner:
    def __init__(self, config):
        self.config = config

    def run_all(self, url):
        scanners = [
            XSSScanner(url),
            DOMXSSScanner(url),
            SQLiScanner(url),
            SQLiTimeScanner(url),
            HeaderAnalyzer(url),
            CSRFChecker(url),
            OpenRedirectChecker(url)
        ]
        results = {}
        max_workers = self.config.get('threads', 5)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {executor.submit(s.run): s.name for s in scanners}
            for future in concurrent.futures.as_completed(future_map):
                name = future_map[future]
                try:
                    results[name] = future.result()
                except Exception as e:
                    results[name] = {'error': str(e)}
        return results
