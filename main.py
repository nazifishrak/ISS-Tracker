import smtplib
import time
import requests
from datetime import datetime
USERNAME = input("Enter email address: ")
PASSWORD = input("Enter password: ")
MY_LAT = 23.746466  # Your latitude
MY_LONG = 90.376015  # Your longitude


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


while True:
    if is_near() and is_night():
        with open(smtplib.SMTP("smtp.gmail.com", port= 587)) as connection:
            connection.starttls()
            connection.sendmail(from_addr=USERNAME, to_addrs=PASSWORD,
            msg= "Subject: Look Up☝️\n\n The ISS is above you ")
    time.sleep(60)