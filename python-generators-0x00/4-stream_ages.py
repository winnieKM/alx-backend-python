#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """
    Generator that yields user ages one by one.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()


def calculate_average_age():
    """
    Calculates and prints the average age using the generator without loading all ages into memory.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")
