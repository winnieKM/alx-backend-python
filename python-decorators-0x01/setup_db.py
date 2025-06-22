import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Insert some sample users
cursor.executemany('''
INSERT INTO users (name, email) VALUES (?, ?)
''', [
    ('Alice Johnson', 'alice@example.com'),
    ('Bob Smith', 'bob@example.com'),
    ('Charlie Brown', 'charlie@example.com')
])

# Save changes and close the connection
conn.commit()
conn.close()

print("✅ users.db and table created with sample data.")
