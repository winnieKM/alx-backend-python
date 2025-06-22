import mysql.connector
import csv
import uuid

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password"
    )

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()
    connection.commit()

def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kimani003!",
        database="ALX_prodev"
    )

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    )
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Use UUID if user_id missing or empty in CSV
            user_id = row.get('user_id') or str(uuid.uuid4())
            # Insert only if not exists
            cursor.execute("""
            INSERT IGNORE INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)
            """, (user_id, row['name'], row['email'], int(row['age'])))
    connection.commit()
    cursor.close()
