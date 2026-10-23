"""Seed script to populate the database with sample data for demonstration."""

import sqlite3
import os
from datetime import date, timedelta

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "study_planner.db")


def seed():
    db = sqlite3.connect(DATABASE)
    db.execute("PRAGMA foreign_keys = ON")

    # Clear existing data
    db.execute("DELETE FROM topics")
    db.execute("DELETE FROM subjects")

    today = date.today()

    # Subject 1: Data Structures & Algorithms
    db.execute(
        "INSERT INTO subjects (id, name, exam_date, daily_study_hours, color) VALUES (?, ?, ?, ?, ?)",
        (1, "Data Structures & Algorithms", (today + timedelta(days=23)).strftime("%Y-%m-%d"), 2.0, "#7C6BA0"),
    )
    dsa_topics = [
        ("Arrays & Linked Lists", 2.0, 1),       # completed
        ("Stacks & Queues", 1.5, 1),              # completed
        ("Trees & Binary Trees", 3.0, 0),
        ("Graphs & Traversals", 2.5, 0),
        ("Sorting Algorithms", 2.0, 0),
        ("Dynamic Programming", 4.0, 0),
        ("Hashing & Hash Tables", 1.5, 0),
    ]
    for name, hours, done in dsa_topics:
        db.execute(
            "INSERT INTO topics (subject_id, name, estimated_hours, completed, completed_at) VALUES (?, ?, ?, ?, ?)",
            (1, name, hours, done, "2026-10-22 14:30" if done else None),
        )

    # Subject 2: Operating Systems
    db.execute(
        "INSERT INTO subjects (id, name, exam_date, daily_study_hours, color) VALUES (?, ?, ?, ?, ?)",
        (2, "Operating Systems", (today + timedelta(days=28)).strftime("%Y-%m-%d"), 1.5, "#E8A0A8"),
    )
    os_topics = [
        ("Process Management", 2.0, 1),           # completed
        ("Threads & Concurrency", 1.5, 0),
        ("Memory Management", 2.5, 0),
        ("File Systems", 1.5, 0),
        ("CPU Scheduling", 2.0, 0),
        ("Deadlocks", 1.5, 0),
    ]
    for name, hours, done in os_topics:
        db.execute(
            "INSERT INTO topics (subject_id, name, estimated_hours, completed, completed_at) VALUES (?, ?, ?, ?, ?)",
            (2, name, hours, done, "2026-10-21 10:00" if done else None),
        )

    # Subject 3: Database Systems
    db.execute(
        "INSERT INTO subjects (id, name, exam_date, daily_study_hours, color) VALUES (?, ?, ?, ?, ?)",
        (3, "Database Systems", (today + timedelta(days=18)).strftime("%Y-%m-%d"), 2.0, "#6B8EAD"),
    )
    db_topics = [
        ("SQL Fundamentals", 1.5, 1),             # completed
        ("Normalization (1NF–BCNF)", 2.0, 1),     # completed
        ("Transaction Management", 2.0, 0),
        ("Indexing & Hashing", 1.5, 0),
        ("ER Modeling & Design", 1.0, 0),
        ("Concurrency Control", 2.0, 0),
    ]
    for name, hours, done in db_topics:
        db.execute(
            "INSERT INTO topics (subject_id, name, estimated_hours, completed, completed_at) VALUES (?, ?, ?, ?, ?)",
            (3, name, hours, done, "2026-10-20 16:00" if done else None),
        )

    # Subject 4: Computer Networks
    db.execute(
        "INSERT INTO subjects (id, name, exam_date, daily_study_hours, color) VALUES (?, ?, ?, ?, ?)",
        (4, "Computer Networks", (today + timedelta(days=35)).strftime("%Y-%m-%d"), 1.5, "#7BAA8E"),
    )
    cn_topics = [
        ("OSI & TCP/IP Models", 1.0, 0),
        ("Transport Layer (TCP/UDP)", 2.0, 0),
        ("Network Layer & Routing", 2.5, 0),
        ("Data Link Layer", 1.5, 0),
        ("Application Layer Protocols", 1.5, 0),
    ]
    for name, hours, done in cn_topics:
        db.execute(
            "INSERT INTO topics (subject_id, name, estimated_hours, completed) VALUES (?, ?, ?, ?)",
            (4, name, hours, done),
        )

    db.commit()
    db.close()
    print("✅ Database seeded with 4 subjects and 24 topics!")
    print("   → 5 topics already marked as completed")
    print("   → Open http://127.0.0.1:5000 to see the app")


if __name__ == "__main__":
    seed()
