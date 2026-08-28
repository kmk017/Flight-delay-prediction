# ✈️ Flight Delay Prediction

A full-stack machine learning application that predicts whether a flight is likely to be delayed based on flight details, schedule, route, and weather conditions.

The project combines a React frontend, Flask REST API, and a Scikit-learn machine learning pipeline.

## 🚀 Features

- Predict flight delay probability
- Interactive React frontend
- Flask REST API for predictions
- Flight route and airline selection
- Weather condition inputs
- Input validation
- Delay probability visualization
- Logistic Regression, Random Forest, and Decision Tree comparison
- Feature engineering and exploratory data analysis
- Data leakage prevention
- Saved trained ML model

## 🏗️ Architecture

```text
User
 │
 ▼
React Frontend
 │
 │ HTTP POST /predict
 ▼
Flask REST API
 │
 ▼
Scikit-learn Pipeline
 │
 ├── One-Hot Encoding
 ├── Feature Scaling
 └── Logistic Regression
 │
 ▼
Prediction
 │
 ├── On-time / Delayed
 └── Delay Probability