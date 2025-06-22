import sqlite3

def stream_users():
    # Connect to the SQLite database file 'users.db'
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # So we get rows as dictionaries

    cursor = conn.cursor()

    # Execute query to select all rows from user_data table
    cursor.execute("SELECT * FROM user_data")

    # Fetch rows one by one using a generator
    for row in cursor:
        yield dict(row)  # Convert sqlite3.Row to a dict and yield it

    # Close connection when done
    conn.close()
