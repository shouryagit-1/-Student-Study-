"""
AI-Powered Student Study Planner
Flask application with SQLite backend.
Generates daily study timetables and tracks completed topics.
"""

import sqlite3
import os
from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g

app = Flask(__name__)
app.secret_key = "study_planner_secret_key_2024"
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "study_planner.db")


# ─── Database Helpers ───────────────────────────────────────────────

def get_db():
    """Get a database connection for the current request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of each request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database schema."""
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            daily_study_hours REAL DEFAULT 2.0,
            color TEXT DEFAULT '#7C6BA0',
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            estimated_hours REAL DEFAULT 1.0,
            completed INTEGER DEFAULT 0,
            completed_at TEXT,
            FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS study_settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            daily_hours REAL DEFAULT 6.0,
            start_hour INTEGER DEFAULT 9,
            break_minutes INTEGER DEFAULT 15,
            session_minutes INTEGER DEFAULT 45
        );

        INSERT OR IGNORE INTO study_settings (id, daily_hours, start_hour, break_minutes, session_minutes)
        VALUES (1, 6.0, 9, 15, 45);
    """)
    db.commit()
    db.close()


# ─── Routes ─────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    """Main dashboard showing overview stats and upcoming exams."""
    db = get_db()
    subjects = db.execute(
        "SELECT * FROM subjects ORDER BY exam_date ASC"
    ).fetchall()

    # Calculate stats
    total_subjects = len(subjects)
    total_topics = db.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
    completed_topics = db.execute(
        "SELECT COUNT(*) FROM topics WHERE completed = 1"
    ).fetchone()[0]

    # Build subject data with progress
    subjects_data = []
    today = date.today()
    for s in subjects:
        topic_count = db.execute(
            "SELECT COUNT(*) FROM topics WHERE subject_id = ?", (s["id"],)
        ).fetchone()[0]
        done_count = db.execute(
            "SELECT COUNT(*) FROM topics WHERE subject_id = ? AND completed = 1",
            (s["id"],),
        ).fetchone()[0]
        exam_dt = datetime.strptime(s["exam_date"], "%Y-%m-%d").date()
        days_left = (exam_dt - today).days
        progress = (done_count / topic_count * 100) if topic_count > 0 else 0

        subjects_data.append({
            "id": s["id"],
            "name": s["name"],
            "exam_date": s["exam_date"],
            "exam_date_formatted": exam_dt.strftime("%b %d, %Y"),
            "days_left": max(days_left, 0),
            "color": s["color"],
            "topic_count": topic_count,
            "done_count": done_count,
            "progress": round(progress, 1),
            "daily_study_hours": s["daily_study_hours"],
        })

    overall_progress = (
        (completed_topics / total_topics * 100) if total_topics > 0 else 0
    )

    return render_template(
        "dashboard.html",
        subjects=subjects_data,
        total_subjects=total_subjects,
        total_topics=total_topics,
        completed_topics=completed_topics,
        overall_progress=round(overall_progress, 1),
    )


@app.route("/subjects")
def subjects_page():
    """List all subjects with their topics."""
    db = get_db()
    subjects = db.execute(
        "SELECT * FROM subjects ORDER BY exam_date ASC"
    ).fetchall()

    subjects_data = []
    today = date.today()
    for s in subjects:
        topics = db.execute(
            "SELECT * FROM topics WHERE subject_id = ? ORDER BY completed ASC, id ASC",
            (s["id"],),
        ).fetchall()
        exam_dt = datetime.strptime(s["exam_date"], "%Y-%m-%d").date()
        days_left = (exam_dt - today).days
        done = sum(1 for t in topics if t["completed"])
        progress = (done / len(topics) * 100) if topics else 0

        subjects_data.append({
            "id": s["id"],
            "name": s["name"],
            "exam_date": s["exam_date"],
            "exam_date_formatted": exam_dt.strftime("%b %d, %Y"),
            "days_left": max(days_left, 0),
            "color": s["color"],
            "daily_study_hours": s["daily_study_hours"],
            "topics": [dict(t) for t in topics],
            "progress": round(progress, 1),
        })

    return render_template("subjects.html", subjects=subjects_data)


@app.route("/subjects/add", methods=["GET", "POST"])
def add_subject():
    """Add a new subject with topics."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        exam_date = request.form.get("exam_date", "").strip()
        daily_hours = float(request.form.get("daily_study_hours", 2.0))
        color = request.form.get("color", "#7C6BA0")
        topics_raw = request.form.get("topics", "").strip()

        if not name or not exam_date:
            flash("Subject name and exam date are required.", "error")
            return redirect(url_for("add_subject"))

        db = get_db()
        cursor = db.execute(
            "INSERT INTO subjects (name, exam_date, daily_study_hours, color) VALUES (?, ?, ?, ?)",
            (name, exam_date, daily_hours, color),
        )
        subject_id = cursor.lastrowid

        # Parse topics (one per line, optional hours after |)
        if topics_raw:
            for line in topics_raw.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if "|" in line:
                    parts = line.split("|", 1)
                    topic_name = parts[0].strip()
                    try:
                        hours = float(parts[1].strip())
                    except ValueError:
                        hours = 1.0
                else:
                    topic_name = line
                    hours = 1.0
                if topic_name:
                    db.execute(
                        "INSERT INTO topics (subject_id, name, estimated_hours) VALUES (?, ?, ?)",
                        (subject_id, topic_name, hours),
                    )

        db.commit()
        flash(f'Subject "{name}" added successfully!', "success")
        return redirect(url_for("subjects_page"))

    return render_template("add_subject.html")


@app.route("/subjects/<int:subject_id>/edit", methods=["GET", "POST"])
def edit_subject(subject_id):
    """Edit an existing subject."""
    db = get_db()
    subject = db.execute(
        "SELECT * FROM subjects WHERE id = ?", (subject_id,)
    ).fetchone()
    if not subject:
        flash("Subject not found.", "error")
        return redirect(url_for("subjects_page"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        exam_date = request.form.get("exam_date", "").strip()
        daily_hours = float(request.form.get("daily_study_hours", 2.0))
        color = request.form.get("color", "#7C6BA0")

        db.execute(
            "UPDATE subjects SET name=?, exam_date=?, daily_study_hours=?, color=? WHERE id=?",
            (name, exam_date, daily_hours, color, subject_id),
        )
        db.commit()
        flash(f'Subject "{name}" updated!', "success")
        return redirect(url_for("subjects_page"))

    topics = db.execute(
        "SELECT * FROM topics WHERE subject_id = ? ORDER BY id ASC",
        (subject_id,),
    ).fetchall()

    return render_template(
        "edit_subject.html", subject=dict(subject), topics=[dict(t) for t in topics]
    )


@app.route("/subjects/<int:subject_id>/delete", methods=["POST"])
def delete_subject(subject_id):
    """Delete a subject and all its topics."""
    db = get_db()
    db.execute("DELETE FROM subjects WHERE id = ?", (subject_id,))
    db.commit()
    flash("Subject deleted.", "success")
    return redirect(url_for("subjects_page"))


@app.route("/subjects/<int:subject_id>/topics/add", methods=["POST"])
def add_topic(subject_id):
    """Add a topic to a subject."""
    name = request.form.get("name", "").strip()
    hours = float(request.form.get("estimated_hours", 1.0))
    if name:
        db = get_db()
        db.execute(
            "INSERT INTO topics (subject_id, name, estimated_hours) VALUES (?, ?, ?)",
            (subject_id, name, hours),
        )
        db.commit()
        flash(f'Topic "{name}" added!', "success")
    return redirect(url_for("subjects_page"))


@app.route("/topics/<int:topic_id>/toggle", methods=["POST"])
def toggle_topic(topic_id):
    """Toggle topic completion status."""
    db = get_db()
    topic = db.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
    if topic:
        new_status = 0 if topic["completed"] else 1
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M") if new_status else None
        db.execute(
            "UPDATE topics SET completed = ?, completed_at = ? WHERE id = ?",
            (new_status, completed_at, topic_id),
        )
        db.commit()

    # Return JSON for AJAX calls
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"status": "ok", "completed": new_status})

    return redirect(request.referrer or url_for("subjects_page"))


@app.route("/topics/<int:topic_id>/delete", methods=["POST"])
def delete_topic(topic_id):
    """Delete a topic."""
    db = get_db()
    db.execute("DELETE FROM topics WHERE id = ?", (topic_id,))
    db.commit()
    flash("Topic deleted.", "success")
    return redirect(request.referrer or url_for("subjects_page"))


@app.route("/timetable")
def timetable():
    """Generate and display a smart study timetable."""
    db = get_db()
    settings = db.execute("SELECT * FROM study_settings WHERE id = 1").fetchone()
    subjects = db.execute(
        "SELECT * FROM subjects ORDER BY exam_date ASC"
    ).fetchall()

    today = date.today()
    num_days = int(request.args.get("days", 7))

    schedule = generate_timetable(db, subjects, settings, today, num_days)

    return render_template(
        "timetable.html",
        schedule=schedule,
        settings=dict(settings),
        num_days=num_days,
        today=today.strftime("%Y-%m-%d"),
    )


@app.route("/settings", methods=["GET", "POST"])
def settings():
    """Manage study settings."""
    db = get_db()
    if request.method == "POST":
        daily_hours = float(request.form.get("daily_hours", 6.0))
        start_hour = int(request.form.get("start_hour", 9))
        break_minutes = int(request.form.get("break_minutes", 15))
        session_minutes = int(request.form.get("session_minutes", 45))

        db.execute(
            """UPDATE study_settings
               SET daily_hours=?, start_hour=?, break_minutes=?, session_minutes=?
               WHERE id=1""",
            (daily_hours, start_hour, break_minutes, session_minutes),
        )
        db.commit()
        flash("Settings updated!", "success")
        return redirect(url_for("settings"))

    current = db.execute("SELECT * FROM study_settings WHERE id = 1").fetchone()
    return render_template("settings.html", settings=dict(current))


# ─── Timetable Generation Algorithm ────────────────────────────────

def generate_timetable(db, subjects, settings, start_date, num_days):
    """
    Generate a smart study timetable based on:
    - Exam proximity (urgency)
    - Remaining incomplete topics
    - Available study hours per day
    - Session duration and break configuration
    """
    session_mins = settings["session_minutes"]
    break_mins = settings["break_minutes"]
    daily_hours = settings["daily_hours"]
    start_hour = settings["start_hour"]

    # How many sessions fit in a day?
    total_daily_minutes = daily_hours * 60
    block_minutes = session_mins + break_mins
    max_sessions = int(total_daily_minutes / block_minutes)

    schedule = []

    for day_offset in range(num_days):
        current_date = start_date + timedelta(days=day_offset)
        day_name = current_date.strftime("%A")
        date_str = current_date.strftime("%Y-%m-%d")
        date_formatted = current_date.strftime("%b %d, %Y")

        # Calculate priority scores for each subject
        subject_priorities = []
        for s in subjects:
            exam_dt = datetime.strptime(s["exam_date"], "%Y-%m-%d").date()
            days_until_exam = (exam_dt - current_date).days

            if days_until_exam < 0:
                continue  # Exam already passed

            # Get remaining topics
            remaining = db.execute(
                "SELECT * FROM topics WHERE subject_id = ? AND completed = 0 ORDER BY id ASC",
                (s["id"],),
            ).fetchall()

            if not remaining:
                continue  # All topics done

            total_remaining_hours = sum(t["estimated_hours"] for t in remaining)

            # Priority formula: higher = more urgent
            # Closer exams and more remaining work = higher priority
            if days_until_exam == 0:
                urgency = 100
            else:
                urgency = (total_remaining_hours / max(days_until_exam, 1)) * 10

            subject_priorities.append({
                "subject": dict(s),
                "remaining_topics": [dict(t) for t in remaining],
                "days_until_exam": days_until_exam,
                "urgency": urgency,
                "total_remaining_hours": total_remaining_hours,
            })

        # Sort by urgency (highest first)
        subject_priorities.sort(key=lambda x: x["urgency"], reverse=True)

        # Distribute sessions across subjects
        sessions = []
        current_time_minutes = start_hour * 60
        sessions_used = 0

        if subject_priorities:
            # Allocate sessions proportionally to urgency
            total_urgency = sum(sp["urgency"] for sp in subject_priorities)

            for sp in subject_priorities:
                if sessions_used >= max_sessions:
                    break

                # Calculate how many sessions this subject gets
                if total_urgency > 0:
                    share = sp["urgency"] / total_urgency
                else:
                    share = 1 / len(subject_priorities)

                num_subject_sessions = max(1, round(share * max_sessions))
                num_subject_sessions = min(
                    num_subject_sessions, max_sessions - sessions_used
                )

                # Assign topics to sessions
                topic_idx = 0
                for _ in range(num_subject_sessions):
                    if topic_idx >= len(sp["remaining_topics"]):
                        topic_idx = 0  # Cycle through topics if needed

                    topic = sp["remaining_topics"][topic_idx]
                    start_h = current_time_minutes // 60
                    start_m = current_time_minutes % 60
                    end_minutes = current_time_minutes + session_mins
                    end_h = end_minutes // 60
                    end_m = end_minutes % 60

                    sessions.append({
                        "subject_name": sp["subject"]["name"],
                        "subject_color": sp["subject"]["color"],
                        "topic_name": topic["name"],
                        "topic_id": topic["id"],
                        "start_time": f"{start_h:02d}:{start_m:02d}",
                        "end_time": f"{end_h:02d}:{end_m:02d}",
                        "duration": session_mins,
                        "days_until_exam": sp["days_until_exam"],
                    })

                    current_time_minutes = end_minutes + break_mins
                    sessions_used += 1
                    topic_idx += 1

        schedule.append({
            "date": date_str,
            "date_formatted": date_formatted,
            "day_name": day_name,
            "is_today": current_date == start_date,
            "sessions": sessions,
        })

    return schedule


# ─── Main ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)
