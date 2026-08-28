from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
from pathlib import Path


app = Flask(__name__)
CORS(app)


# ============================================================
# Load trained ML model
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "model" / "flight_delay_model.pkl"

model = joblib.load(MODEL_PATH)


# ============================================================
# Airport congestion values
# ============================================================
AIRLINES = [
    "AA", "DL", "UA", "WN",
    "AS", "B6", "NK", "F9"
]

AIRPORT_CONGESTION = {
    "ATL": 0.8,
    "ORD": 0.85,
    "DFW": 0.7,
    "DEN": 0.6,
    "LAX": 0.75,
    "JFK": 0.9,
    "SFO": 0.8,
    "SEA": 0.5,
    "LAS": 0.55,
    "MCO": 0.6,
}


# ============================================================
# Home route
# ============================================================

@app.route("/")
def home():
    return {
        "message": "Flight Delay Prediction API is running"
    }


# ============================================================
# Prediction API
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    try:
        airline = data["airline"]
        origin = data["origin"]
        dest = data["dest"]

        month = int(data["month"])
        sched_dep_hour = int(data["sched_dep_hour"])
        distance = float(data["distance"])

        temperature_f = float(data["temperature_f"])
        wind_speed_mph = float(data["wind_speed_mph"])
        precipitation_in = float(data["precipitation_in"])
        visibility_miles = float(data["visibility_miles"])

        day_of_week = int(data["day_of_week"])

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Invalid or missing input data"
        }), 400

    if airline not in AIRLINES:
        return jsonify({"error": "Invalid airline"}), 400

    if origin not in AIRPORT_CONGESTION:
        return jsonify({"error": "Invalid origin airport"}), 400

    if dest not in AIRPORT_CONGESTION:
        return jsonify({"error": "Invalid destination airport"}), 400

    if origin == dest:
        return jsonify({"error": "Origin and destination must be different"}), 400

    if not 1 <= month <= 12:
        return jsonify({"error": "Invalid month"}), 400

    if not 0 <= day_of_week <= 6:
        return jsonify({"error": "Invalid day of week"}), 400

    if not 5 <= sched_dep_hour <= 22:
        return jsonify({"error": "Invalid departure hour"}), 400


    # ========================================================
    # Feature engineering
    # ========================================================

    is_weekend = 1 if day_of_week >= 5 else 0

    is_peak_hour = (
        1 if sched_dep_hour in (7, 8, 16, 17, 18)
        else 0
    )

    is_holiday_season = (
        1 if month in (11, 12)
        else 0
    )

    origin_congestion_index = AIRPORT_CONGESTION[origin]
    dest_congestion_index = AIRPORT_CONGESTION[dest]

    hour_sin = np.sin(
        2 * np.pi * sched_dep_hour / 24
    )

    hour_cos = np.cos(
        2 * np.pi * sched_dep_hour / 24
    )

    month_sin = np.sin(
        2 * np.pi * month / 12
    )

    month_cos = np.cos(
        2 * np.pi * month / 12
    )


    # ========================================================
    # Prepare model input
    # ========================================================

    input_data = {
        "airline": airline,
        "origin": origin,
        "dest": dest,

        "distance": distance,
        "is_weekend": is_weekend,
        "is_peak_hour": is_peak_hour,
        "is_holiday_season": is_holiday_season,

        "temperature_f": temperature_f,
        "wind_speed_mph": wind_speed_mph,
        "precipitation_in": precipitation_in,
        "visibility_miles": visibility_miles,

        "origin_congestion_index": origin_congestion_index,
        "dest_congestion_index": dest_congestion_index,

        "hour_sin": hour_sin,
        "hour_cos": hour_cos,
        "month_sin": month_sin,
        "month_cos": month_cos,
    }


    # ========================================================
    # Make prediction
    # ========================================================

    input_df = pd.DataFrame([input_data])

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(
      input_df
    )[0][1]


    result = "Delayed" if prediction == 1 else "On-time"


    return jsonify({
        "prediction": result,
        "delayed": int(prediction),
        "delay_probability": round(
            float(probability) * 100,
            2
        )
    })


# ============================================================
# Start server
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)