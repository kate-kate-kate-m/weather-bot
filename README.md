# weather-bot

Sends a daily weather forecast to Kate's WhatsApp via Twilio at 6:23am ET.

- Fetches forecast for zip 11231 from Open-Meteo API (no API key needed)
- Sends via Twilio WhatsApp sandbox (same sandbox as twilio-notion)
- Runs on GitHub Actions cron schedule

## Setup

1. Create a GitHub repo and push this folder
2. Set two GitHub secrets:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
3. Make sure your phone is joined to the Twilio WhatsApp sandbox

## Notes

- Cron is set to `23 10 * * *` (6:23am EDT / UTC-4) — update to `23 11 * * *` in winter (EST)
- Uses the same Twilio sandbox as the Notion bot — phone must be joined to the first Twilio account's sandbox
- Do NOT join a second Twilio sandbox from the same phone — it will override the first and break the Notion bot

## Session log

### 2026-03-12
- Initial build: daily weather forecast via GitHub Actions + Twilio WhatsApp
- Learned: joining a second Twilio sandbox from the same phone overrides the first — keep one sandbox per phone

### 2026-03-15 3:30pm
- Rewrote forecast: switched from wttr.in to Open-Meteo API for real forecast data
- Now shows today's high/low, chance of rain with time windows, and comparison to yesterday's high
- Fixed Node.js deprecation warning: pinned actions/checkout@v4.2.2 and actions/setup-python@v5.4.0
