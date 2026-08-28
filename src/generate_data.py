"""
generate_data.py
-----------------
Generates a realistic synthetic dataset of historical flights merged with
weather conditions at departure time. Designed to mimic the structure of
real-world sources like the BTS (Bureau of Transportation Statistics) On-Time
Performance data joined with NOAA weather data, which is what this project
would use in a production setting.

Delay is modeled as a function of weather severity, time-of-day congestion,
carrier, and route distance, with realistic noise added -- so the resulting
classification task is non-trivial but learnable (similar to real flight
delay prediction difficulty, where accuracy typically lands 75-85%).
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

N_SAMPLES = 20000

AIRLINES = ["AA", "DL", "UA", "WN", "AS", "B6", "NK", "F9"]

AIRLINE_DELAY_BIAS = {
    "AA": 0.05,
    "DL": -0.10,
    "UA": 0.02,
    "WN": 0.00,
    "AS": -0.05,
    "B6": 0.08,
    "NK": 0.12,
    "F9": 0.10,
}

AIRPORTS = ["ATL", "ORD", "DFW", "DEN", "LAX", "JFK", "SFO", "SEA", "LAS", "MCO"]

AIRPORT_CONGESTION = {
    "ATL": 0.80,
    "ORD": 0.85,
    "DFW": 0.70,
    "DEN": 0.60,
    "LAX": 0.75,
    "JFK": 0.90,
    "SFO": 0.80,
    "SEA": 0.50,
    "LAS": 0.55,
    "MCO": 0.60,
}


def sample_route():
    origin = RNG.choice(AIRPORTS)
    dest = RNG.choice([airport for airport in AIRPORTS if airport != origin])
    return origin, dest


def generate():
    rows = []

    for _ in range(N_SAMPLES):

        origin, dest = sample_route()
        airline = RNG.choice(AIRLINES)

        month = int(RNG.integers(1, 13))
        day_of_week = int(RNG.integers(0, 7))
        sched_dep_hour = int(RNG.integers(5, 23))

        distance = int(RNG.integers(200, 2600))

        # -----------------------------
        # Weather
        # -----------------------------

        winter = month in (12, 1, 2)
        transition = month in (3, 11)

        winter_factor = 1.30 if winter else (1.10 if transition else 1.00)

        temperature_f = (
            RNG.normal(60, 18)
            - (10 if winter else 0)
        )

        wind_speed_mph = max(
            0,
            RNG.normal(10, 5) * winter_factor
        )

        precipitation_in = max(
            0,
            RNG.exponential(0.04) * winter_factor
        )

        visibility_miles = np.clip(
            RNG.normal(9, 1.8) - precipitation_in * 5,
            0.5,
            10
        )

        # -----------------------------
        # Schedule / congestion
        # -----------------------------

        origin_congestion = AIRPORT_CONGESTION[origin]
        dest_congestion = AIRPORT_CONGESTION[dest]

        is_weekend = int(day_of_week >= 5)

        is_peak_hour = int(
            sched_dep_hour in (7, 8, 16, 17, 18)
        )

        is_holiday_season = int(
            month in (11, 12)
        )

        # -----------------------------
        # Route effect
        # -----------------------------

        route = f"{origin}_{dest}"

        route_bias = (
            0.15
            if origin in ("ATL", "JFK", "ORD")
            and dest in ("ATL", "JFK", "ORD")
            else 0
        )

        # -----------------------------
        # Delay score
        # -----------------------------

        score = (
            -2.35
            + 1.40 * origin_congestion
            + 0.70 * dest_congestion
            + 0.085 * wind_speed_mph
            + 4.00 * precipitation_in
            - 0.20 * visibility_miles
            + 0.80 * is_peak_hour
            + 0.40 * is_holiday_season
            + 0.15 * is_weekend
            + AIRLINE_DELAY_BIAS[airline]
            + 0.00030 * distance
            + route_bias
            + RNG.normal(0, 0.25)
        )

        # Convert score into probability
        prob_delay = 1 / (1 + np.exp(-score))

        delayed = int(RNG.random() < prob_delay)

        # -----------------------------
        # Delay duration
        # -----------------------------

        delay_minutes = 0

        if delayed:
            delay_minutes = int(
                max(
                    15,
                    RNG.gamma(2.0, 30)
                    + 20 * precipitation_in
                )
            )

        rows.append({
            "airline": airline,
            "origin": origin,
            "dest": dest,
            "month": month,
            "day_of_week": day_of_week,
            "sched_dep_hour": sched_dep_hour,
            "distance": distance,
            "is_weekend": is_weekend,
            "is_peak_hour": is_peak_hour,
            "is_holiday_season": is_holiday_season,
            "temperature_f": round(temperature_f, 1),
            "wind_speed_mph": round(wind_speed_mph, 1),
            "precipitation_in": round(precipitation_in, 3),
            "visibility_miles": round(visibility_miles, 2),
            "origin_congestion_index": origin_congestion,
            "dest_congestion_index": dest_congestion,
            "delay_minutes": delay_minutes,
            "delayed": delayed,
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":

    df = generate()

    out_path = "data/flights_weather.csv"

    df.to_csv(out_path, index=False)

    print(f"Saved {len(df)} rows to {out_path}")

    print("\nDelay distribution:")
    print(
        df["delayed"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
    )