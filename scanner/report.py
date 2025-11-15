import json, uuid, os
from flask import render_template

class ReportGenerator:
    @staticmethod
    def generate(results, url):
        id = str(uuid.uuid4())
        path = os.path.join('reports', f"{id}.json")
        os.makedirs('reports', exist_ok=True)
        with open(path, 'w') as f:
            json.dump({'url': url, 'results': results}, f, indent=2)
        return id

    @staticmethod
    def load(id):
        path = os.path.join('reports', f"{id}.json")
        if not os.path.exists(path):
            return 'Report not found'
        with open(path) as f:
            data = json.load(f)
        return render_template('report_view.html', data=data)
