
import sqlite3

DB_NAME = "students.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS students (name TEXT PRIMARY KEY, grade TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS attendance (name TEXT, date TEXT, status TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS assignments (name TEXT, title TEXT, description TEXT, due_date TEXT, filename TEXT, submitted INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS scores (name TEXT, subject TEXT, score INTEGER)")
    conn.commit()
    conn.close()

def add_student(name, grade):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("REPLACE INTO students (name, grade) VALUES (?, ?)", (name, grade))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT name, grade FROM students")
    result = c.fetchall()
    conn.close()
    return result

def get_scores(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT subject, score FROM scores WHERE name=?", (name,))
    result = c.fetchall()
    conn.close()
    return result

def get_attendance(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT date, status FROM attendance WHERE name=?", (name,))
    result = c.fetchall()
    conn.close()
    return result

def get_assignments(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT title, description, due_date, filename, submitted FROM assignments WHERE name=?", (name,))
    result = c.fetchall()
    conn.close()
    return result

def submit_assignment(name, title):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE assignments SET submitted=1 WHERE name=? AND title=?", (name, title))
    conn.commit()
    conn.close()

def add_score(name, subject, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO scores (name, subject, score) VALUES (?, ?, ?)", (name, subject, score))
    conn.commit()
    conn.close()

def add_assignment(name, title, description, due_date, filename, submitted):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO assignments (name, title, description, due_date, filename, submitted) VALUES (?, ?, ?, ?, ?, ?)", (name, title, description, due_date, filename, int(submitted)))
    conn.commit()
    conn.close()
