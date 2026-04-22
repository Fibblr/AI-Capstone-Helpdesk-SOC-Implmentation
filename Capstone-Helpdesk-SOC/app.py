from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
import sqlite3
import json
from datetime import datetime


try:
    from soc_logic.normalization import normalize
    from soc_logic.client import classify_auth_alert
    from soc_logic.severity import calculate_risk, map_severity

    AI_AVAILABLE = True
except ImportError:
    print("WARNING: soc_logic module not found. AI features will run in fallback mode.")
    AI_AVAILABLE = False

DB_PATH = "helpdesk.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        # IT & SOC Staff (Formerly Teachers)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE,
            password TEXT
        );
        """)
        # Standard Employees (Formerly Students)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE,
            password TEXT
        );
        """)
        # Unified Ticket Queue (Formerly Classes/Grades/Assignments)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            source TEXT NOT NULL, -- 'IT' or 'SOC'
            employee_id INTEGER,  -- Null if it's a SOC alert
            description TEXT NOT NULL,
            ai_classification TEXT,
            confidence_score INTEGER,
            severity TEXT,
            status TEXT DEFAULT 'Open',
            FOREIGN KEY(employee_id) REFERENCES employee(id)
        );
        """)

        # Seed initial users
        cur.execute(
            "INSERT OR IGNORE INTO staff (id, name, username, password) VALUES (1, 'Admin Jacob', 'jacob', 'pass123')")
        cur.execute(
            "INSERT OR IGNORE INTO staff (id, name, username, password) VALUES (2, 'SOC Cameron', 'cameron', 'pass123')")
        cur.execute(
            "INSERT OR IGNORE INTO employee (id, name, username, password) VALUES (1, 'John Sales', 'john', 'user123')")
        conn.commit()


app = Flask(__name__, template_folder="templates")
app.secret_key = "super_secret_helpdesk_key"
init_db()


# --- Core Routes ---

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# --- STAFF ROUTES (IT & SOC Analysts) ---

@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        with get_conn() as conn:
            staff = conn.execute("SELECT * FROM staff WHERE username = ?", (username,)).fetchone()

        if staff and staff['password'] == password:
            session['role'] = 'staff'
            session['user_id'] = staff['id']
            session['name'] = staff['name']
            return redirect(url_for('staff_dashboard'))
        else:
            error = "Invalid Staff Credentials"
    return render_template('staff_login.html', error=error)


@app.route('/staff_dashboard')
def staff_dashboard():
    if session.get('role') != 'staff': return abort(403)

    with get_conn() as conn:
        tickets = conn.execute(
            "SELECT * FROM tickets ORDER BY CASE WHEN status='Open' THEN 1 ELSE 2 END, id DESC").fetchall()
    return render_template('staff_dashboard.html', name=session['name'], tickets=tickets)


@app.route('/ticket/<int:ticket_id>', methods=['GET', 'POST'])
def view_ticket(ticket_id):
    if session.get('role') != 'staff': return abort(403)

    with get_conn() as conn:
        if request.method == 'POST':
            new_status = request.form.get('status')
            conn.execute("UPDATE tickets SET status = ? WHERE id = ?", (new_status, ticket_id))
            conn.commit()
            return redirect(url_for('staff_dashboard'))

        ticket = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()

    return render_template('ticket_detail.html', ticket=ticket)


# --- EMPLOYEE ROUTES (Standard Users submitting IT Tickets) ---

@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        with get_conn() as conn:
            emp = conn.execute("SELECT * FROM employee WHERE username = ?", (username,)).fetchone()

        if emp and emp['password'] == password:
            session['role'] = 'employee'
            session['user_id'] = emp['id']
            session['name'] = emp['name']
            return redirect(url_for('employee_dashboard'))
        else:
            error = "Invalid Employee Credentials"
    return render_template('employee_login.html', error=error)


@app.route('/employee_dashboard')
def employee_dashboard():
    if session.get('role') != 'employee': return abort(403)

    with get_conn() as conn:
        tickets = conn.execute("SELECT * FROM tickets WHERE employee_id = ? ORDER BY id DESC",
         (session['user_id'],)).fetchall()
    return render_template('employee_dashboard.html', name=session['name'], tickets=tickets)


@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if session.get('role') != 'employee': return abort(403)

    if request.method == 'POST':
        description = request.form.get('description')
        with get_conn() as conn:
            # Standard IT tickets get a default severity until reviewed
            conn.execute("""
                INSERT INTO tickets (source, employee_id, description, severity, status) 
                VALUES ('IT', ?, ?, 'Pending Analysis', 'Open')
            """, (session['user_id'], description))
            conn.commit()
        return redirect(url_for('employee_dashboard'))

    return render_template('create_ticket.html')


# --- SOC WEBHOOK (For Cameron's Script) ---

@app.route('/webhook', methods=['POST'])
def receive_alert():
    raw_data = request.json
    if not raw_data:
        return jsonify({"error": "No payload"}), 400

    try:
        if AI_AVAILABLE:
            clean_data = normalize(raw_data)
            ai_response = classify_auth_alert(clean_data)
            try:
                parsed_ai = json.loads(ai_response)
            except:
                parsed_ai = {"classification": "Unknown", "confidence": 0} 
            
            classification = parsed_ai.get("classification", "Unknown")
            confidence = parsed_ai.get("confidence", 0)
            
            
            severity = map_severity(
                calculate_risk(clean_data, confidence))
        else:
            classification = "AI Offline"
            confidence = 0
            severity = "Manual Review Required"

    except Exception as e:
        print(f"AI Error: {e}")
        classification = "Processing Error"
        confidence = 0
        severity = "High"

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tickets (source, description, ai_classification, confidence_score, severity)
            VALUES ('SOC', ?, ?, ?, ?)
        """, (json.dumps(raw_data), classification, confidence, severity))
        conn.commit()
        ticket_id = cur.lastrowid

    return jsonify({"status": "Success", "ticket_id": ticket_id, "severity": severity}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)

