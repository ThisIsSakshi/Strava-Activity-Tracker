import requests
import config
import re
import os
from datetime import datetime

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
activity_date = datetime.strptime(latest['start_date'], "%Y-%m-%dT%H:%M:%SZ")
formatted_date = activity_date.strftime("%d%%20%b%%20%Y")
activity_time = int(latest['moving_time'])//60

activity_text = f"""
### 🏃 Latest Strava Activity
#### {latest['name']}
![Activity](https://img.shields.io/badge/Run-{round(int(latest['distance'])/1000,2)}km-blue?style=for-the-badge&logo=strava)
![Time](https://img.shields.io/badge/⏱️_Time-{activity_time}min-pink?style=for-the-badge)
![Elevation](https://img.shields.io/badge/⛰️_Elevation-{latest['total_elevation_gain']}m-green?style=for-the-badge)
![Kudos](https://img.shields.io/badge/👏_Kudos-{latest['kudos_count']}-red?style=for-the-badge)
![Date](https://img.shields.io/badge/📅_Date-{formatted_date}-yellow?style=for-the-badge)
"""
# 3. Update README.md
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

with open("README.md", "w", encoding="utf-8") as f:
    f.write(activity_text)
