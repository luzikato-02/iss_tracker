import time

import requests
from datetime import datetime

MY_LAT = -8.184486
MY_LON = 113.668076

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()

iss_longitude = float(data["iss_position"]["longitude"])
iss_latidude = float(data["iss_position"]["latitude"])

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

while True:
    if iss_longitude - MY_LON == -5 or iss_longitude - MY_LON == 5 and iss_latidude - MY_LAT == -5 or iss_latidude - MY_LAT == 5:
        if time_now.hour <= sunrise or time_now.hour >= sunset:
            print("ISS Overhead!")
        else:
            print("It's still day, the ISS is overhead but you won't be able to see it.")
    else:
        print("ISS is not overhead.")
    time.sleep(60)
