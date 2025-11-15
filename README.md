# Web Application Vulnerability Scanner  
### *Elevate Lab – Cybersecurity Internship Project*  
**Author:** DHANUSH S

---

## 📘 Overview
The **Web Application Vulnerability Scanner** is a Python-based security testing tool designed to identify common vulnerabilities in web applications.  
It automates scanning for OWASP Top 10 issues such as **SQL Injection, XSS, CSRF, Open Redirects, and Security Header Misconfigurations**.

The project includes a modern **Flask-based Web Interface**, an organized **plugin-driven scanning engine**, and a detailed **report generation system**, making it an excellent internship-level cybersecurity project.

---

## 🎯 Key Features
- 🔍 **Multi-Vulnerability Detection**
  - SQL Injection (Error-based & Time-based)
  - Cross-Site Scripting (Reflected XSS)
  - Open Redirect
  - Missing Security Headers
  - CSRF Weakness Detection

- 🧩 **Modular Plugin Architecture**
  - Easily add new scanning modules  
  - Each vulnerability type is handled independently

- 🖥️ **Interactive Web Dashboard**
  - Login authentication system  
  - Simple interface to initiate scans  
  - Tables & cards for viewing results  
  - Detailed report viewer with payload evidence  

- 📄 **Automatic Reporting**
  - Stores logs for each scan  
  - Shows severity levels  
  - Displays vulnerable parameters, URLs, and payloads  

- 🐳 **Docker Support** (optional)
  - Easy deployment using Dockerfile  

---

## 🛠️ Technologies Used
- **Python 3.x**
- **Flask** (Backend Framework)
- **Requests** (HTTP Communication)
- **BeautifulSoup** (HTML Parsing)
- **Regex** (Pattern Matching)
- **HTML / CSS / JavaScript**
- **JSON Files** (User database, logs, settings)
- **Docker** (Containerization)

---

## 📂 Folder Structure
```
Web-Vulnerability-Scanner/
│── app.py                     # Main Flask Application
│── api.py                     # API for triggering scans
│── auth.py                    # User Authentication
│── config.json                # Application Configuration
│── users.json                 # Login Credentials
│── requirements.txt           # Python Dependencies
│── Dockerfile                 # Optional Container Build File
│
├── scanner/                   # Scanning Engine (Plugins)
│   ├── core.py                # Central Scan Controller
│   ├── xss.py                 # XSS Detection Logic
│   ├── sqli.py                # Basic SQL Injection Test
│   ├── sqli_time.py           # Time-based SQLi Module
│   ├── open_redirect.py       # Open Redirect Test
│   ├── headers.py             # Security Headers Validator
│   └── csrf_check.py          # CSRF Weakness Analyzer
│
├── templates/                 # User Interface Pages
│   ├── login.html
│   ├── dashboard.html
│   ├── scanner.html
│   ├── reports.html
│   └── report_view.html
│
└── static/                    # CSS / JS / Images
```

---

## 🚀 How It Works

### 1️⃣ **User Authentication**
The application uses a basic JSON-based login system to ensure only authorized users can run scans.

### 2️⃣ **Scan Initialization**
The user enters:
- A website URL  
- A page with parameters  
- Any target endpoint  

The core engine handles scanning tasks.

### 3️⃣ **Payload Injection**
Each module generates crafted inputs and analyzes web responses using:
- Pattern matching  
- Error-based detection  
- Time delays  
- HTML/DOM analysis  
- Response code behavior  

### 4️⃣ **Vulnerability Reporting**
After scanning:
- Results appear in the UI  
- Evidence and payloads are displayed  
- Reports are stored for later review  

---

## ▶️ Installation & Usage

### **1. Install Dependencies**
```
pip install -r requirements.txt
```

### **2. Run the Application**
```
python app.py
```

### **3. Access the Dashboard**
Open your browser and visit:
```
http://127.0.0.1:5000/
```

---

## ⚠️ Ethical Usage Warning
This tool is strictly for:
- Learning  
- Research  
- Self-testing  
- Internship demonstration  
- Authorized security assessments  

**Do NOT scan websites without explicit permission.  
Unauthorized scanning is illegal and punishable by law.**

---

## 📌 Why This Project Is Valuable
This scanner demonstrates real cybersecurity skills:
- Web security fundamentals  
- OWASP Top 10 awareness  
- Secure coding practices  
- Backend development using Flask  
- Writing vulnerability detection logic  
- Report generation system  
- Plugin-based architecture  

It reflects practical offensive security knowledge and is ideal for internships, resumes, and project portfolios.

---

## 🏁 Conclusion
The **Web Application Vulnerability Scanner** is a complete, modular, and educational project that showcases real-world cybersecurity techniques.  
It combines web development, security scanning logic, vulnerability detection, and reporting into a single, professional tool—built as part of the **Elevate Lab Cybersecurity Internship**.

