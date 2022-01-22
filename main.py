from datetime import datetime
import requests
import smtplib
import time
import os

MY_LAT = -23.481708
MY_LONG = -46.605073

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


def iss_track():
    global MY_LAT, MY_LONG
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    my_loc_lat = int(MY_LAT)
    my_loc_long = int(MY_LONG)
    if iss_latitude in range(my_loc_lat - 5, my_loc_lat + 5) and iss_longitude in range(my_loc_long - 5, my_loc_long + 5):
        return True
    else:
        return False


def night_hour():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    hour_now = datetime.now().hour

    if hour_now <= sunrise or hour_now >= sunset:
        return True
    else:
        return False


while True:
    if iss_track() and night_hour():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs=email,
                msg="Subject: ISS in the sky\nLook up.")
    time.sleep(60)
