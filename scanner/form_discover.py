import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def discover_forms(url, timeout=5):
    """Return list of forms: {'action':..., 'method': 'get'/'post', 'inputs': [{'name':..., 'type':...,'value':...}], 'full_action':...} """
    forms = []
    try:
        r = requests.get(url, timeout=timeout)
    except Exception:
        return forms
    soup = BeautifulSoup(r.text, 'lxml')
    for form in soup.find_all('form'):
        action = form.get('action') or ''
        method = (form.get('method') or 'get').lower()
        full = urljoin(url, action)
        inputs = []
        for inp in form.find_all(['input','textarea','select']):
            name = inp.get('name') or inp.get('id') or None
            typ = inp.get('type') or inp.name
            val = inp.get('value') or ''
            if name:
                inputs.append({'name': name, 'type': typ, 'value': val})
        forms.append({'action': action, 'full_action': full, 'method': method, 'inputs': inputs})
    return forms
