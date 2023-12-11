import asyncio
import requests
import sqlite3
from datetime import datetime

# Function to fetch data from the API
def get_data():
    url = "https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi"
    response = requests.get(url)
    return response.json()

# Storing the data in DB
def store_in_db(data):
    connection = sqlite3.connect("data.db")
    cursor = connection.cursor()

    # Putting data in the table
    timestamp = data['time']
    factor = data['factor']
    pi_value = data['pi']

    cursor.execute('''
        INSERT INTO data (timestamp, factor, pi)
        VALUES (?, ?, ?)
    ''', (timestamp, factor, pi_value))

    connection.commit()
    connection.close()

async def execution(in_seconds):
    count = 0
    while True:
        try:
            #Getting data from the API
            data = get_data()

            # Store data in the database
            store_in_db(data)

            count += 1
            print(f"The data is stored now. Amount: {count}")

        except Exception as e:
            print(f"Error: {e}")

       
        await asyncio.sleep(in_seconds)

# Set the interval (in seconds) for getting data
get_interval = 60


class_loop = asyncio.get_event_loop()

try:
    class_loop.run_until_complete(execution(get_interval))
except KeyboardInterrupt:
    pass 
finally:
    class_loop.close()