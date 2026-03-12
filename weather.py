import os
import requests
from twilio.rest import Client

def get_weather():
    r = requests.get("https://wttr.in/11231?format=3", headers={"User-Agent": "curl/7.0"})
    return r.text.strip()

def send_whatsapp(message):
    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
    client.messages.create(
        from_="whatsapp:+14155238886",
        to="whatsapp:+13363391181",
        body=message
    )

if __name__ == "__main__":
    weather = get_weather()
    send_whatsapp(f"Good morning! Here's your weather for today:\n{weather}")
