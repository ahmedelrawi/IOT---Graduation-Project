import random
import csv
import datetime

# Generate a synthetic temperature, humidity, and some forecasting weather dataset
def generate_temperature_humidity_dataset(filename, start_date, end_date, interval_minutes):

    # defining a variable 
    current_date = start_date

    # creating a csv file at a specifi location 'IOT - Graduation project' and writing a defining columns in the csv file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Time', 'Temperature (°C)', 'Humidity (%)', 'Air Moisture (%)','Dew Point'])
        
        # creating a while loop to make sure the variables added in the specifi columns
        while current_date <= end_date:
            
            # define another variable 
            time = current_date    

            # creating if condition for adding a specific temprature and humidity at interval of time. between 12 am --> 9 am
            if time.hour > 0 and time.hour < 10:
                temperature = random.uniform(21, 26)
                humidity = random.uniform(60, 80)
            
            # creating if condition for adding a specific temprature and humidity at interval of time. between 10 am --> 6 pm
            elif time.hour >= 10 and time.hour < 18:
                temperature = random.uniform(28, 36)
                humidity = random.uniform(30, 40)

            # creating if condition for adding a specific temprature and humidity at interval of time. between 6 pm --> 9 pm
            elif time.hour >= 18 and time.hour < 21:
                temperature = random.uniform(35, 28)
                humidity = random.uniform(40, 55)

            # creating if condition for adding a specific temprature and humidity at interval of time. between 9 pm --> 12 am
            else :
                temperature = random.uniform(27, 22)
                humidity = random.uniform(55, 60)

            # defining and adding some forecastin variables as a function of temprature and humidity
            air_moisture = (humidity/100) * 101.325 
            dew_point = temperature - ((100-humidity) / 5)

            # writing the variables at specified columns in the csv file created
            writer.writerow([current_date.strftime('%Y-%m-%d'), time.time(), temperature, humidity, air_moisture,dew_point])
            current_date += datetime.timedelta(minutes=interval_minutes)

# Specify the parameters for the dataset
filename = 'Forecasting.csv' # Name of csv file
start_date = datetime.datetime(2023, 8, 20) # starting time 
end_date = datetime.datetime(2023, 10, 6) # ending time
interval_minutes = 60  # 1 hour interval


try:
    # Generate the dataset
    generate_temperature_humidity_dataset(filename, start_date, end_date, interval_minutes)

    # printing the succes of operation
    print(f"Temperature, humidity, and air moisture dataset generated and saved to {filename}.")

except Exception as error:
    print('There is error in: ', error)