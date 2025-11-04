import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Model to predict next day REI based on current activity features

def load_dataset(file_path="data/activities_with_rei.json"):
    with open(file_path, "r") as f:
        activities = json.load(f)

    df = pd.DataFrame(activities)
    df = df[["date", "distance_m", "moving_time_s", "elev_gain_m", "avg_hr", "rei"]]
    df.sort_values("date", inplace=True)

    # Shift REI to next activity
    df["rei_next_day"] = df["rei"].shift(-1)
    # Drop rows with where nexr day REI is missing
    df = df.dropna(subset=["rei_next_day", "distance_m", "moving_time_s", "elev_gain_m", "avg_hr"])
    return df 

def train_model():
    df = load_dataset()
    
    X = df[["distance_m", "moving_time_s", "elev_gain_m", "avg_hr"]].dropna()
    y = df["rei_next_day"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model R^2 score: {round(score,3)}")
    
    # Save model for Coach Zilla
    
    joblib.dump(model, "data/rei_model.joblib")
    print("Model saved to data/rei_model.joblib")
if __name__ == "__main__":
    train_model() 