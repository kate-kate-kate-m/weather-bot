import os
import requests
from twilio.rest import Client

LATITUDE = 40.6501
LONGITUDE = -73.9496
RAIN_THRESHOLD = 40  # % probability considered "likely rain"

def get_weather_data():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&hourly=precipitation_probability"
        "&timezone=America%2FNew_York"
        "&forecast_days=1"
        "&past_days=1"
        "&temperature_unit=fahrenheit"
    )
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def fmt_hour(h):
    if h == 0: return "midnight"
    if h == 12: return "noon"
    if h < 12: return f"{h}am"
    return f"{h - 12}pm"

def get_rain_description(hourly_probs_today):
    """Return a rain description string, or None if no rain expected."""
    rainy_hours = [h for h, p in enumerate(hourly_probs_today) if p >= RAIN_THRESHOLD]
    if not rainy_hours:
        return None

    # Find contiguous windows
    windows = []
    start = rainy_hours[0]
    prev = rainy_hours[0]
    for h in rainy_hours[1:]:
        if h > prev + 1:
            windows.append((start, prev + 1))
            start = h
        prev = h
    windows.append((start, prev + 1))

    # Label each window by time of day
    def label(start, end):
        mid = (start + end) // 2
        max_prob = max(hourly_probs_today[start:end])
        if 6 <= mid < 12:
            period = "morning"
        elif 12 <= mid < 18:
            period = "afternoon"
        elif 18 <= mid < 22:
            period = "evening"
        else:
            period = "overnight"
        return f"{period} ({fmt_hour(start)}–{fmt_hour(end)}, {max_prob}%)"

    parts = [label(s, e) for s, e in windows]
    return "🌧 Rain expected: " + ", ".join(parts)

def build_message(today_high, today_low, yesterday_high, rain_desc):
    diff = today_high - yesterday_high
    if diff >= 4:
        comparison = f"Warmer than yesterday (yesterday's high: {yesterday_high}°F)"
    elif diff <= -4:
        comparison = f"Colder than yesterday (yesterday's high: {yesterday_high}°F)"
    else:
        comparison = f"About the same as yesterday (yesterday's high: {yesterday_high}°F)"

    rain_line = rain_desc if rain_desc else "No rain expected today ✓"

    return (
        f"Good morning! Today in Brooklyn:\n"
        f"High: {today_high}°F | Low: {today_low}°F\n"
        f"{comparison}\n"
        f"{rain_line}"
    )

def send_whatsapp(message):
    client = Client(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
    client.messages.create(
        from_="whatsapp:+14155238886",
        to="whatsapp:+13363391181",
        body=message
    )

if __name__ == "__main__":
    data = get_weather_data()

    # daily[0] = yesterday, daily[1] = today
    yesterday_high = round(data["daily"]["temperature_2m_max"][0])
    today_high = round(data["daily"]["temperature_2m_max"][1])
    today_low = round(data["daily"]["temperature_2m_min"][1])

    # hourly has 48 entries: [0-23] = yesterday, [24-47] = today
    today_hourly = data["hourly"]["precipitation_probability"][24:48]

    rain_desc = get_rain_description(today_hourly)
    message = build_message(today_high, today_low, yesterday_high, rain_desc)
    send_whatsapp(message)
