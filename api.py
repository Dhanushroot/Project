from flask import Blueprint, jsonify, request, current_app, send_from_directory
from scanner.core import Scanner
from scanner.report import ReportGenerator
from scanner.report_pdf import PDFReport
import threading, uuid, os, time, json

api = Blueprint('api', __name__, url_prefix='/api')

# in-memory stores for status and logs (also write to reports/ and logs/)
STATUS = {}  # id -> {'status': 'running'|'done'|'error', 'logs': [...], 'report': id}
LOGS_DIR = 'logs'

def _append_log(scan_id, msg, status='info'):
    STATUS.setdefault(scan_id, {'status':'running','logs':[]})
    STATUS[scan_id]['logs'].append({'ts': time.time(), 'msg': msg, 'status': status})
    # also write incremental to a file for persistence
    os.makedirs(LOGS_DIR, exist_ok=True)
    with open(os.path.join(LOGS_DIR, f"{scan_id}.log"), 'a') as f:
        f.write(f"[{time.ctime()}] {status.upper()}: {msg}\n")

def _run_scan_background(scan_id, url, scanners, depth, config):
    try:
        _append_log(scan_id, f"Initializing scan for {url}", 'info')
        endpoints = [url]
        if depth and int(depth) > 0:
            from scanner.crawler import Crawler
            _append_log(scan_id, f"Running crawler depth={depth}", 'info')
            endpoints = Crawler(url, max_depth=int(depth), timeout=config.get('timeout',5)).crawl()
            _append_log(scan_id, f"Crawler found {len(endpoints)} endpoints", 'info')
        scanner = Scanner(config)
        all_results = {}
        for ep in endpoints:
            _append_log(scan_id, f"Scanning endpoint: {ep}", 'info')
            # for each endpoint we can choose specific scanners
            # If scanners contains 'all' run everything (Scanner.run_all does that)
            if 'all' in scanners:
                res = scanner.run_all(ep)
                all_results[ep] = res
                _append_log(scan_id, f"Completed endpoint: {ep}", 'success')
            else:
                # run only requested modules
                res = {}
                # map short names to scanner classes run via Scanner.run_all but filter
                temp = scanner.run_all(ep)
                # filter results to requested scanners
                for k,v in temp.items():
                    key = k.lower().split()[0]
                    if key in scanners:
                        res[k] = v
                all_results[ep] = res
                _append_log(scan_id, f"Completed endpoint (filtered): {ep}", 'success')
        # generate report JSON
        report_id = ReportGenerator.generate(all_results, url)
        STATUS[scan_id]['status'] = 'done'
        STATUS[scan_id]['report_id'] = report_id
        _append_log(scan_id, f"Report generated: {report_id}", 'success')
    except Exception as e:
        STATUS[scan_id]['status'] = 'error'
        STATUS[scan_id]['error'] = str(e)
        _append_log(scan_id, f"Scan failed: {e}", 'error')

@api.route('/scan', methods=['POST'])
def api_scan():
    data = request.get_json() or {}
    url = data.get('url')
    depth = data.get('depth', 0)
    scanners = data.get('scanners', ['all'])
    if not url:
        return jsonify({'error':'url required'}), 400
    scan_id = str(uuid.uuid4())
    STATUS[scan_id] = {'status':'running','logs':[]}
    # start background thread
    thread = threading.Thread(target=_run_scan_background, args=(scan_id, url, scanners, depth, current_app.config), daemon=True)
    thread.start()
    return jsonify({'id': scan_id}), 200

@api.route('/scan_status/<scan_id>', methods=['GET'])
def api_scan_status(scan_id):
    st = STATUS.get(scan_id)
    if not st:
        return jsonify({'error':'not found'}), 404
    # return last N logs to avoid huge payloads
    logs = st.get('logs', [])[-50:]
    return jsonify({'status': st.get('status','unknown'), 'logs': logs, 'report_id': st.get('report_id')})

@api.route('/generate_pdf/<report_id>', methods=['GET'])
def api_generate_pdf(report_id):
    json_path = os.path.join('reports', f"{report_id}.json")
    if not os.path.exists(json_path):
        return jsonify({'error':'report not found'}), 404
    pdf = None
    try:
        pdf = PDFReport.generate(json_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'pdf': f'/reports/{os.path.basename(pdf)}'})

