# Coach Zilla - Adaptive coach 
import json
from statistics import mean

def load_activities(file_path="data/activities_with_rei.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def suggest_next_run(activities):
    if not activities:
        return "🦖 Coach Zilla: No run found. Go run. NOW!"
    
    last_run = activities[0] # activities sorted by date descending
    
    avg_rei = mean(recent_reis)
    rei = last_run["rei"]

    # decide suggestion based on REI
    
