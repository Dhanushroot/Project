import os
import json
from flask import render_template, jsonify, send_from_directory

def register_extra(app):

    # -------------------------
    # SCANNERS PAGE
    # -------------------------
    def scanners_page():
        return render_template('scanners.html')
    app.add_url_rule('/scanners', 'scanners_page', scanners_page)

    # -------------------------
    # REPORTS PAGE
    # -------------------------
    def reports_page():
        return render_template('reports.html')
    app.add_url_rule('/reports', 'reports_page', reports_page)

    # -------------------------
    # LIVE FEED PAGE
    # -------------------------
    def live_page():
        return render_template('live.html')
    app.add_url_rule('/live', 'live_page', live_page)

    # -------------------------
    # LIST REPORTS
    # -------------------------
    def reports_list():
        rpt_dir = 'reports'
        os.makedirs(rpt_dir, exist_ok=True)
        out = []

        for f in os.listdir(rpt_dir):
            if f.endswith('.json'):
                path = os.path.join(rpt_dir, f)
                try:
                    with open(path) as fh:
                        js = json.load(fh)
                    out.append({
                        'id': f.replace('.json',''),
                        'file': f,
                        'url': js.get('url')
                    })
                except:
                    out.append({
                        'id': f.replace('.json',''),
                        'file': f,
                        'url': 'unknown'
                    })
        return jsonify(out)

    app.add_url_rule('/reports_list', 'reports_list', reports_list)

    # -------------------------
    # DOWNLOAD REPORT FILE
    # -------------------------
    def report_file(filename):
        return send_from_directory('reports', filename)

    app.add_url_rule('/reports/<path:filename>', 'report_file', report_file)

    # -------------------------
    # LIVE FEED (API)
    # -------------------------
    def live_feed():
        entries = []
        logs_dir = 'logs'
        os.makedirs(logs_dir, exist_ok=True)

        for fn in os.listdir(logs_dir):
            if fn.endswith('.log'):
                sid = fn.replace('.log','')
                try:
                    with open(os.path.join(logs_dir, fn)) as fh:
                        lines = fh.read().splitlines()[-5:]
                except:
                    continue

                for line in lines:
                    status = 'info'
                    u = line.upper()
                    if 'SUCCESS' in u:
                        status = 'success'
                    elif 'ERROR' in u:
                        status = 'error'
                    elif 'WARN' in u:
                        status = 'warn'

                    entries.append({
                        'id': sid,
                        'msg': line,
                        'status': status
                    })

        return jsonify(entries)

    app.add_url_rule('/live_feed', 'live_feed', live_feed)

