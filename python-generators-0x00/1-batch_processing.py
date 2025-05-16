import sqlite3

def stream_users_in_batches(batch_size):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    offset = 0

    while True:
        cursor.execute("SELECT * FROM user_data LIMIT ? OFFSET ?", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        users = []
        for row in rows:
            users.append({
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3]
            })
        yield users
        offset += batch_size

    conn.close()

def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                print(user)
