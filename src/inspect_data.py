import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "flights_weather.csv"

df = pd.read_csv(DATA_PATH)

print("\n===== DATASET SHAPE =====")
print(df.shape)

print("\n===== COLUMNS =====")
print(df.columns.tolist())

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DELAY COUNTS =====")
print(df["delayed"].value_counts())

print("\n===== DELAY PERCENTAGE =====")
print(df["delayed"].value_counts(normalize=True) * 100)