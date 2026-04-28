import sqlite3
import os

DB_PATH = "logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                  input_data TEXT, 
                  prediction TEXT, 
                  status TEXT)''')
    conn.commit()
    conn.close()

def log_decision(input_data, result, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logs (input_data, prediction, status) VALUES (?, ?, ?)",
              (str(input_data), str(result), status))
    conn.commit()
    conn.close()
