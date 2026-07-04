from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import date, datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_NAME = "database/attendance.db"


# ---------- Database helpers ----------
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'teacher'
    );

    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        course_id INTEGER,
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );

    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL, -- 'Present' or 'Absent'
        marked_by TEXT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        UNIQUE(student_id, date)
    );
    """)
    # default admin user
    cur.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
                    ("admin", "admin123", "admin"))
    conn.commit()
    conn.close()


# ---------- Auth ----------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()
        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        flash("Invalid username or password")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- Dashboard ----------
@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db()
    total_students = conn.execute("SELECT COUNT(*) c FROM students").fetchone()["c"]
    today = date.today().isoformat()
    present_today = conn.execute(
        "SELECT COUNT(*) c FROM attendance WHERE date=? AND status='Present'", (today,)
    ).fetchone()["c"]
    conn.close()
    return render_template("dashboard.html", total_students=total_students,
                           present_today=present_today, today=today)


# ---------- Students ----------
@app.route("/students", methods=["GET", "POST"])
@login_required
def students():
    conn = get_db()
    if request.method == "POST":
        roll_no = request.form["roll_no"]
        name = request.form["name"]
        course_id = request.form.get("course_id") or None
        try:
            conn.execute("INSERT INTO students (roll_no, name, course_id) VALUES (?,?,?)",
                         (roll_no, name, course_id))
            conn.commit()
            flash("Student added")
        except sqlite3.IntegrityError:
            flash("Roll number already exists")
    all_students = conn.execute("""
        SELECT students.*, courses.name as course_name
        FROM students LEFT JOIN courses ON students.course_id = courses.id
    """).fetchall()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("students.html", students=all_students, courses=courses)


@app.route("/courses", methods=["GET", "POST"])
@login_required
def courses():
    conn = get_db()
    if request.method == "POST":
        name = request.form["name"]
        conn.execute("INSERT INTO courses (name) VALUES (?)", (name,))
        conn.commit()
        flash("Course added")
    all_courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("courses.html", courses=all_courses)


# ---------- Mark Attendance ----------
@app.route("/attendance", methods=["GET", "POST"])
@login_required
def mark_attendance():
    conn = get_db()
    selected_date = request.form.get("date") or date.today().isoformat()

    if request.method == "POST" and request.form.get("action") == "submit_attendance":
        student_ids = request.form.getlist("student_id")
        for sid in student_ids:
            status = request.form.get(f"status_{sid}", "Absent")
            conn.execute("""
                INSERT INTO attendance (student_id, date, status, marked_by)
                VALUES (?,?,?,?)
                ON CONFLICT(student_id, date) DO UPDATE SET status=excluded.status
            """, (sid, selected_date, status, session["user"]))
        conn.commit()
        flash(f"Attendance saved for {selected_date}")

    all_students = conn.execute("SELECT * FROM students").fetchall()
    existing = conn.execute(
        "SELECT student_id, status FROM attendance WHERE date=?", (selected_date,)
    ).fetchall()
    existing_map = {row["student_id"]: row["status"] for row in existing}
    conn.close()
    return render_template("mark_attendance.html", students=all_students,
                           selected_date=selected_date, existing_map=existing_map)


# ---------- Analytics / Reports ----------
@app.route("/reports")
@login_required
def reports():
    conn = get_db()
    rows = conn.execute("""
        SELECT s.id, s.roll_no, s.name,
               COUNT(a.id) as total_marked,
               SUM(CASE WHEN a.status='Present' THEN 1 ELSE 0 END) as present_count
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        GROUP BY s.id
    """).fetchall()

    report_data = []
    defaulters = []
    for r in rows:
        total = r["total_marked"] or 0
        present = r["present_count"] or 0
        pct = round((present / total) * 100, 2) if total > 0 else 0.0
        entry = {
            "roll_no": r["roll_no"],
            "name": r["name"],
            "total": total,
            "present": present,
            "percentage": pct
        }
        report_data.append(entry)
        if pct < 75 and total > 0:
            defaulters.append(entry)

    conn.close()
    return render_template("reports.html", report_data=report_data, defaulters=defaulters)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
