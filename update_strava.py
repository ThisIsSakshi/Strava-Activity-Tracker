import requests
import config
import re
import os

# Load secrets
CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["STRAVA_REFRESH_TOKEN"]

# 1. Refresh access token
res = requests.post(
    "https://www.strava.com/oauth/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    },
)
res.raise_for_status()
ACCESS_TOKEN = res.json()["access_token"]

# 2. Get latest activity
headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
activities = requests.get("https://www.strava.com/api/v3/athlete/activities", headers=headers).json()

latest = activities[0]
print('\n\nstrava data',latest)
activity_text = f"🚴 **{latest['name']}** — {latest['distance']/1000:.2f} km in {latest['moving_time']//60} min 🕒"
# 3. Update README.md
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

with open("README.md", "w", encoding="utf-8") as f:
    f.write(activity_text)
