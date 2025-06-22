import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()

for col in columns:
    print(col)  # Prints (cid, name, type, notnull, dflt_value, pk)

conn.close()
