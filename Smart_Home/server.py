from flask import Flask, request, render_template, jsonify
from firestore import upload_image , download_image, firebase_init, check_user_and_pass, download_images
import subprocess
from gpiozero import LED
from time import sleep
from dht import read_dht
import Adafruit_DHT

server = Flask(__name__)


# the script that detect and notify for burglary
capture_script = "capture_burglar.py"

# iteration global variable
i = 0

# blocking global variable
blocked = False

# logged in global variable
logged_in = False

sensor_type = Adafruit_DHT.DHT11

# define upload route for the server
@server.route("/upload", methods=['POST'])
def server_upload():
    # Save the image to the server
    upload_image(request.json["image"], request.json["id"])

    # Return a success message
    return "OK"

# define download route for the server
@server.route("/download/<id>", methods=['GET'])
def server_download(id):
    # Download the image from Firestore
    image = download_image(id)

    # Return the image
    return {"image": image}

@server.route("/login", methods=['POST'])
def login():
    global blocked

    # if blocked:
    #     return render_template('login.html', message="Login failed 3/3, Blocked!.")

    # Get the username and password from the form
    username = request.form['username']
    password = request.form['password']

    global i
    i+=1
    if check_user_and_pass('users', username, password):
        i = 0
        global logged_in
        logged_in = True
        
        return render_template('index.html')
    else:
        if i == 3:
            # Reset global variables
            i = 0
            blocked = True
        
            # running the burglary script
            try:
                subprocess.run(["python", capture_script], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")

            return render_template('login.html', message="Login failed 3/3, Blocked!.")
        else:
            print("Invalid username or password. Please try again.")
            return render_template('login.html', message=f"Login failed {i}/3.")

@server.route("/")
def login_get():
    return render_template('login.html')

@server.route("/turn_on_led1", methods=['POST'])
def turn_on_led1():
   
    try:
        subprocess.run(["python", "led_yellow_on.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    return render_template('index.html')


@server.route("/turn_off_led1", methods=['POST'])
def turn_off_led1():
    try:
        subprocess.run(["python", "led_yellow_off.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

    return render_template('index.html')


@server.route("/turn_on_led2", methods=['POST'])
def turn_on_led2():
   
    try:
        subprocess.run(["python", "led_blue_on.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
    return render_template('index.html')


@server.route("/turn_off_led2", methods=['POST'])
def turn_off_led2():
   
    try:
        subprocess.run(["python", "led_blue_off.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
    return render_template('index.html')


@server.route("/burglars")
def burglars():
    if logged_in:
        all_images = download_images()
        return render_template('burglars.html', images=all_images)
    return render_template('login.html', message="You have to log in first!")

@server.route("/logout")
def logout():
    global logged_in
    logged_in = False
    return render_template('login.html')

@server.route("/control")
def control():
    if logged_in:
        return render_template('index.html')
    return render_template('login.html', message="You have to log in first!")

@server.route("/get_temperature")
def get_temperature():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor_type, 16)
        if humidity is not None and temperature is not None:
            # Return temperature as a JSON response
            return jsonify(temperature=temperature)
        else:
            return jsonify(error="Failed to read temperature data"), 500
    except Exception as e:
        return jsonify(error=str(e)), 500

# run flask app to listen 
if __name__ == "__main__":
    # initialize the firebase admin sdk once
    firebase_init()

    # run the flask app
    server.run(port=8000, debug=True)