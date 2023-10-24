import time
import psycopg2
import Adafruit_DHT

# PostgreSQL database connection parameters
db_params = {
    'dbname': 'your_db_name',
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': 'localhost',  # or the address of your PostgreSQL server
    'port': 5432,         # PostgreSQL default port
}

# Sensor details
sensor = Adafruit_DHT.DHT22
pin = 16  # GPIO pin connected to the DHT sensor

# Function to insert data into the PostgreSQL database
def insert_temperature_data(temperature, humidity):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO temperature_data (temperature, humidity) VALUES (%s, %s)", (temperature, humidity))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            conn.close()

# Main loop to continuously read and insert data
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.2f}°C, Humidity: {humidity:.2f}%")
        insert_temperature_data(temperature, humidity)
    else:
        print("Failed to retrieve data from the DHT sensor")

    time.sleep(3600)  # Wait for an hour before the next reading and insertion
