import requests, re, os, html
from .form_discover import discover_forms

class SQLiScanner:
    name = 'SQL Injection Scanner'
    def __init__(self, url):
        self.url = url
        base_params_file = os.path.join('scanner','parameters','sqli_params.txt')
        if os.path.exists(base_params_file):
            with open(base_params_file) as f:
                self.priority = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]
        else:
            self.priority = ['id','q','search']
        payload_file = os.path.join('scanner','payloads','sqli.txt')
        if os.path.exists(payload_file):
            with open(payload_file) as f:
                self.payloads = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]
        else:
            self.payloads = ["' OR '1'='1"]

        self.error_signatures = [
            r"SQL syntax", r"mysql_fetch", r"PDOException", r"Warning: mysql_",
            r"unclosed quotation mark", r"SQLite\/JDBC", r"syntax error", r"You have an error in your SQL syntax"
        ]

    def _test(self, action, method, params, payload):
        try:
            if method == 'post':
                r = requests.post(action, data=params, timeout=8)
            else:
                r = requests.get(action, params=params, timeout=8)
        except Exception as e:
            return False, str(e), ''
        text = r.text or ''
        for sig in self.error_signatures:
            if re.search(sig, text, re.IGNORECASE):
                return True, None, sig
        return False, None, ''

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

        for payload in self.payloads:
            for t in targets:
                if t['inputs']:
                    for inp in t['inputs']:
                        params = {}
                        for i in t['inputs']:
                            params[i['name']] = i.get('value','') or '1'
                        params[inp['name']] = payload
                        ok, err, sig = self._test(t['action'], t['method'], params, payload)
                        if ok:
                            findings.append({'payload': payload, 'endpoint': t['action'], 'type':'Error-Based SQLi', 'param': inp['name'], 'signature': sig})
                            break
                else:
                    for p in candidates:
                        params = {p: payload}
                        ok, err, sig = self._test(t['action'], 'get', params, payload)
                        if ok:
                            findings.append({'payload': payload, 'endpoint': t['action'], 'type':'Error-Based SQLi', 'param': p, 'signature': sig})
                            break
        return findings
