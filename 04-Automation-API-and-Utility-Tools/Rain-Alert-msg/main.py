import requests
from twilio.rest import Client

import os
from dotenv import load_dotenv

load_dotenv()

OWM_Endpoints = os.getenv("OWM_ENDPOINT")
api_key = os.getenv("OWM_API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")


weather_params = {
    "lat": 18.520430,
    "lon": 73.856743,
    "appid": api_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoints,params=weather_params)
# print(response.status_code)
response.raise_for_status()
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="It's going to rain today.Remember to bring an Umbrella",
        from_="+15173992642",
        to="+918421879348",
    )

    print(message.status)