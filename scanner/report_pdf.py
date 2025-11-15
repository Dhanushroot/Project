from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json, os

class PDFReport:
    @staticmethod
    def generate(json_path, out_path=None):
        if out_path is None:
            out_path = json_path.replace('.json', '.pdf')
        with open(json_path) as f:
            data = json.load(f)
        c = canvas.Canvas(out_path, pagesize=letter)
        width, height = letter
        x = 40; y = height - 40
        c.setFont('Helvetica-Bold', 14)
        c.drawString(x, y, f"Scan Report: {data.get('url')}")
        y -= 30
        c.setFont('Helvetica', 10)
        for section, findings in data.get('results', {}).items():
            if y < 80:
                c.showPage(); y = height - 40; c.setFont('Helvetica', 10)
            c.setFont('Helvetica-Bold', 12)
            c.drawString(x, y, section)
            y -= 18
            c.setFont('Helvetica', 9)
            if isinstance(findings, list):
                if not findings:
                    c.drawString(x + 12, y, 'No issues found'); y -= 14
                for fnd in findings:
                    if y < 80:
                        c.showPage(); y = height - 40; c.setFont('Helvetica', 9)
                    line = json.dumps(fnd)
                    c.drawString(x + 12, y, line[:120])
                    y -= 12
            elif isinstance(findings, dict):
                line = json.dumps(findings)
                c.drawString(x + 12, y, line[:120])
                y -= 12
        c.save()
        return out_path
