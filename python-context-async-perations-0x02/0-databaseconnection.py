import sqlite3

class DatabaseConnection:
    def __enter__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

# Using the context manager to fetch users
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
