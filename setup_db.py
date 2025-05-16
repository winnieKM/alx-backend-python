import sqlite3

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the user_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    # Insert some sample data
    sample_users = [
        ('001', 'Alice Johnson', 'alice@example.com', 30),
        ('002', 'Bob Smith', 'bob@example.com', 25),
        ('003', 'Charlie Rose', 'charlie@example.com', 35),
        ('004', 'Diana Prince', 'diana@example.com', 28),
        ('005', 'Ethan Hunt', 'ethan@example.com', 40),
        ('006', 'Fiona Glenanne', 'fiona@example.com', 32),
    ]

    cursor.executemany('INSERT OR IGNORE INTO user_data VALUES (?, ?, ?, ?)', sample_users)

    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
