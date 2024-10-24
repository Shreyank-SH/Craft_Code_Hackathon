import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('auditing.db')
cursor = conn.cursor()

# Create a table for storing issues
cursor.execute('''CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY,
                    issue_type TEXT,
                    image BLOB,
                    description TEXT,
                    raised_by TEXT  -- New column to store the username of the employee who raised the issue
                 )''')

# Create a table for storing accepted issues with auto-incremented ID
cursor.execute('''CREATE TABLE IF NOT EXISTS accepted_issues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incremented ID
                    issue_type TEXT,
                    image BLOB,
                    description TEXT,
                    raised_by TEXT
                 )''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        points INTEGER DEFAULT 0  -- New column for storing points, default is 0
    )
''')

conn.commit()
conn.close()
