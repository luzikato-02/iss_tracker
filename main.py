import time

import requests
import smtplib
from datetime import datetime

MY_LAT = -8.184486
MY_LON = 113.668076
MY_EMAIL = ""
MY_PASSWORD = ""

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latidude = float(data["iss_position"]["latitude"])

    if MY_LAT-5 <= iss_latidude <= MY_LAT+5 and MY_LON-5 <= iss_longitude <= MY_LON+5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "longitude": MY_LON,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    if time_now.hour <= sunrise or time_now.hour >= sunset:
        return True
while True:
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="anasnurfauzan@outlook.com",
                                msg="Subject: Look Up!\n\nThe ISS is above you in the sky!"
            )
    time.sleep(60)


