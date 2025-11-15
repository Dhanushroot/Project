import requests, os, html
from .form_discover import discover_forms
from bs4 import BeautifulSoup

class XSSScanner:
    name = 'XSS Scanner'
    def __init__(self, url):
        self.url = url
        base_params_file = os.path.join('scanner','parameters','xss_params.txt')
        if os.path.exists(base_params_file):
            with open(base_params_file) as f:
                self.priority = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]
        else:
            self.priority = ['name','q','search','id']
        payload_file = os.path.join('scanner','payloads','xss.txt')
        if os.path.exists(payload_file):
            with open(payload_file) as f:
                self.payloads = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')]
        else:
            self.payloads = ['<script>alert(1)</script>']

    def _test_injection(self, action, method, params, payload):
        """Submit GET or POST and test response for payload reflection."""
        try:
            if method == 'post':
                r = requests.post(action, data=params, timeout=8)
            else:
                r = requests.get(action, params=params, timeout=8)
        except Exception as e:
            return False, str(e)
        # decode HTML entities and compare
        text = html.unescape(r.text)
        if payload in text:
            return True, None
        return False, None

    def run(self):
        findings = []
        # discover forms on page
        forms = discover_forms(self.url)
        # build param candidate list: priority + form inputs + generic
        candidates = list(self.priority)
        for f in forms:
            for inp in f.get('inputs', []):
                if inp['name'] not in candidates:
                    candidates.append(inp['name'])
        # ensure unique
        candidates = list(dict.fromkeys(candidates))
        # For pages with no forms, still try priority params on the page URL
        targets = []
        if forms:
            for f in forms:
                targets.append({'action': f['full_action'], 'method': f['method'], 'inputs': f['inputs']})
        else:
            targets.append({'action': self.url, 'method': 'get', 'inputs': []})

        for payload in self.payloads:
            for t in targets:
                # try form inputs first (if any)
                if t['inputs']:
                    # make a copy and set payload for each input one at a time and submit
                    for inp in t['inputs']:
                        params = {}
                        for i in t['inputs']:
                            # preserve default values for non-target fields
                            params[i['name']] = i.get('value','') or '1'
                        params[inp['name']] = payload
                        ok, err = self._test_injection(t['action'], t['method'], params, payload)
                        if ok:
                            findings.append({'payload': payload, 'endpoint': t['action'], 'type': 'Reflected XSS', 'param': inp['name'], 'method': t['method']})
                            break
                        # if error, continue trying
                else:
                    # try priority params as GET
                    for p in candidates:
                        params = {p: payload}
                        ok, err = self._test_injection(t['action'], 'get', params, payload)
                        if ok:
                            findings.append({'payload': payload, 'endpoint': t['action'], 'type':'Reflected XSS', 'param': p, 'method':'get'})
                            break
        return findings
