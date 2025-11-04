# Get activities using Strava API
import requests
import urllib3
import os
import json
# Disable warnings for insecure requests (probably not kosher)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API URLs
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
AUTH_URL = "https://www.strava.com/oauth/token"

# Credentials
CLIENT_ID = "175200"
CLIENT_SECRET = "bf3ec552d1fb464d141fd68bf1b98139b2923390"
REFRESH_TOKEN = "505170b7642ef86e06361496fccf442df9e8dfb9"

def get_access_token():
    # Request fresh access token using refresh token
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }
    print("Requesting access token... \n")
    res = requests.post(AUTH_URL, data=payload, verify=False)
    data = res.json()

    if 'access_token' in data:
        access_token = data['access_token']
    # if access token request fails, print error and exit
    else:
        print("Error: Failed to get access token \n")
        print("Response status:", res.status_code)
        print("Response JSON:", res.json())
        print("Exiting...")
        exit()
    print("Access token obtained! \n")
    return data["access_token"]

def get_activities(per_page=200, page=3):
    token = get_access_token()
    header = {"Authorization": f"Bearer {token}"}
    param = {'per_page': per_page, 'page': page}

    print("Requesting activities... \n")
    res = requests.get(ACTIVITIES_URL, headers=header, params=param, verify=False)
    if res.status_code != 200:
        print("Error: Failed to get activities \n")
        print("Response status:", res.status_code)
        print("Response JSON:", res.json())
        print("Exiting...")
        exit()

    raw_activities = res.json()
    # Filter coachable data
    filtered_data = []

    for act in raw_activities:
        # Only run activities
        if act.get("type") != "Run":
            continue
        filtered_data.append({
            "name": act.get("name"),
            "type": act.get("type"),
            "date": act.get("start_date_local"),
            "distance_m": act.get("distance"),
            "moving_time_s": act.get("moving_time"),
            "elapsed_time_s": act.get("elapsed_time"),
            "avg_speed_mps": act.get("average_speed"),
            "max_speed_mps": act.get("max_speed"),
            "avg_cadence": act.get("average_cadence"),
            "avg_hr": act.get("average_heartrate"),
            "max_hr": act.get("max_heartrate"),
            "elev_gain_m": act.get("total_elevation_gain"),
            "suffer_score": act.get("suffer_score"),
        })

    # Check data folder exists, if not create it
    os.makedirs("data", exist_ok=True)
    # Save to file
    with open("data/activities.json", "w") as f:
        json.dump(filtered_data, f, indent=2)
    if filtered_data:
        first_date = filtered_data[-1]['date'] # newest activity
        last_date = filtered_data[0]['date'] # oldest activity
        print(f"Saved {len(filtered_data)} activities to data/activities.json")
        print(f"From {first_date} to {last_date}\n")
    else: 
        print("No activities found.")
    return filtered_data


if __name__ == "__main__":
    activities = get_activities()
    # print first activity as sample
    if activities:
        print("Sample activity:")
        print(json.dumps(activities[0], indent=2))
    else:
        print("No activities found.")