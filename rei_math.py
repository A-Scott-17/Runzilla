# Calculate Runzilla Effort Index (REI)
import math
import json

# Function to calculate REI
def calculate_rei(activity, max_hr=None, recent_runs=None):
    rei_est = 0

    # Heart rate
    if activity.get("avg_hr") and max_hr:
        hr_ratio = activity["avg_hr"] / max_hr
        rei_est += hr_ratio * activity.get("moving_time_s", 0)

    # Distance
    distance_m = activity.get("distance_m", 0)
    distance_miles = distance_m / 1609.34 # conver meters to miles
    rei_est += math.sqrt(distance_miles) * 10 if distance_miles > 0 else 0

    # Elevation gain
    rei_est += activity.get("elev_gain_m", 0) * 0.5 # 0.5 REI per meter climbed

    # Pace ajustment
    if recent_runs and len(recent_runs) > 1 and distance_m > 0:
        avg_pace = sum(r["moving_time_s"] / r["distance_m"] 
                       for r in recent_runs if r["distance_m"] > 0) / len(recent_runs)
        current_pace = activity["moving_time_s"] / distance_m
        pace_ratio = avg_pace / current_pace # faster than average => ratio > 1
        rei_est *= pace_ratio

    # Factor in Strava suffer_score if available
    strava_suffer = activity.get("suffer_score")
    if strava_suffer:
        # Weighted blend 60% suffer score, 40% REI
        rei_final = round((strava_suffer * 0.6) + (rei_est * 0.4), 1)
    # If no suffer score, use REI estimate directly
    else:
        rei_final = round(rei_est, 1)

    return rei_final

def add_rei_to_activities(input_file="data/activities.json",
                          output_file="data/activities_with_rei.json", 
                          max_hr=None):
    # Load activities
    with open(input_file, "r") as f:
        activities = json.load(f)
    
    # Calculate REI for each activity
    for act in activities:
        act["rei"] = calculate_rei(act, max_hr=max_hr, recent_runs=activities)
    
    # Save to new file
    with open(output_file, "w") as f:
        json.dump(activities, f, indent=2)
    
    print(f"REI added to {len(activities)} activities and saved to {output_file}")
    return activities

if __name__ == "__main__":
    add_rei_to_activities(max_hr=190)  # Example max HR

    # *** Test output *** 
    with open("data/activities_with_rei.json", "r") as f:
        activities = json.load(f)

    print("\n Runzilla Effort Index (REI) Sample Activities:")
    for act in activities[:5]:
        print(f"{act['date']}: {act['name']} - REI: {act['rei']}")