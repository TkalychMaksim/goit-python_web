import sqlite3
from faker import Faker
import random

fake = Faker()


conn = sqlite3.connect('university.db')
cur = conn.cursor()


cur.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_name TEXT
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        group_id INTEGER,
        FOREIGN KEY (group_id) REFERENCES groups (group_id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_name TEXT
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        grade INTEGER,
        grade_date DATE,
        FOREIGN KEY (student_id) REFERENCES students (student_id),
        FOREIGN KEY (subject_id) REFERENCES subjects (subject_id)
    )
''')


group_names = ["KI2024", "KN2024", "KB2024"]
for group in group_names:
    cur.execute("INSERT INTO groups (group_name) VALUES (?)", (group,))

for _ in range(3):
    cur.execute("INSERT INTO teachers (teacher_name) VALUES (?)", (fake.name(),))

subject_names = ["Math", "Physics", "Computer Science", "Computer Networks", "English"]
for subject in subject_names:
    cur.execute("INSERT INTO subjects (subject_name, teacher_id) VALUES (?, ?)", (subject, random.randint(1, 3)))

for _ in range(35):
    cur.execute("INSERT INTO students (student_name, group_id) VALUES (?, ?)", (fake.name(), random.randint(1, 3)))

for _ in range(250):
    cur.execute("INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (?, ?, ?, ?)", 
                (random.randint(1, 30), random.randint(1, 5), random.randint(1, 5), fake.date_this_year()))


conn.commit()


conn.close()
