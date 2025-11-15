from flask import Flask, render_template, request, redirect, url_for, current_app
from scanner.core import Scanner
from scanner.report import ReportGenerator
from scanner.utils import sanitize_url
from auth import login_manager, LoginForm, USERS
from flask_login import login_required, login_user, logout_user, current_user
import json, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'replace-with-strong-secret-key')
app.config['API_KEY'] = os.environ.get('API_KEY', 'supersecretapikey')

login_manager.init_app(app)

# load config
CONFIG = {}
try:
    with open('config.json') as f:
        CONFIG = json.load(f)
except Exception:
    CONFIG = {"timeout":5, "threads":5}

scanner = Scanner(CONFIG)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not sanitize_url(url):
            return render_template('index.html', error="Invalid URL")
        # optional depth
        depth = int(request.form.get('depth', 0))
        endpoints = [url]
        if depth > 0:
            from scanner.crawler import Crawler
            endpoints = Crawler(url, max_depth=depth, timeout=CONFIG.get('timeout',5)).crawl()
        results = {}
        for ep in endpoints:
            results[ep] = scanner.run_all(ep)
        report_id = ReportGenerator.generate(results, url)
        return redirect(url_for('view_report', id=report_id))
    return render_template('index.html')

@app.route('/report/<id>')
def view_report(id):
    return ReportGenerator.load(id)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # find user
        user = None
        for u in USERS.values():
            if u.username == username:
                user = u; break
        if user and user.verify(password):
            login_user(user)
            return redirect(url_for('index'))
        return render_template('login.html', form=form, error='Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# API blueprint registered in separate file to keep simple
from api import api as api_bp
app.register_blueprint(api_bp)
# register extra routes
from app_extra_routes import register_extra
register_extra(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
