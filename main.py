import smtplib
import requests
from datetime import datetime

MY_LAT = 23.746466  # Your latitude
MY_LONG = 90.376015  # Your longitude


# Your position is within +5 or -5 degrees of the ISS position.

def is_near():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if (MY_LAT-5 <= iss_latitude <= MY_LAT+5) and (MY_LONG-5 <= iss_longitude < MY_LONG+5):
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour()

    if time_now >= sunset or time_now <= sunrise:
        return True




if is_near() and is_night():
    connection = smtplib.SMTP("smtp.gmail.com", port= 587)
    connection.starttls()
    connection.sendmail()