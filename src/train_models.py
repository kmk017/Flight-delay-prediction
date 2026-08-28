"""
train_models.py
----------------
End-to-end pipeline for the Flight Delay Prediction project.

Steps:
1. Load merged flight + weather data
2. Preprocessing & feature engineering (encoding, scaling, cyclical time features)
3. Train/test split
4. Train Logistic Regression, Decision Tree, and Random Forest
5. Evaluate each with accuracy, precision, recall, F1-score, ROC-AUC
6. Analyze feature importance (Random Forest + Decision Tree)
7. Save comparison table, confusion matrices, and feature importance plots
"""

import json
import os

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

sns.set_theme(style="whitegrid")


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = PROJECT_ROOT / "data" / "flights_weather.csv"
OUT_DIR = PROJECT_ROOT / "outputs"
MODEL_DIR = PROJECT_ROOT / "model"

OUT_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# ============================================================
# 2. FEATURE ENGINEERING
# ============================================================

df["hour_sin"] = np.sin(
    2 * np.pi * df["sched_dep_hour"] / 24
)

df["hour_cos"] = np.cos(
    2 * np.pi * df["sched_dep_hour"] / 24
)

df["month_sin"] = np.sin(
    2 * np.pi * df["month"] / 12
)

df["month_cos"] = np.cos(
    2 * np.pi * df["month"] / 12
)


# ============================================================
# 3. FEATURES AND TARGET
# ============================================================

target = "delayed"

categorical_features = [
    "airline",
    "origin",
    "dest",
]

numeric_features = [
    "distance",
    "is_weekend",
    "is_peak_hour",
    "is_holiday_season",
    "temperature_f",
    "wind_speed_mph",
    "precipitation_in",
    "visibility_miles",
    "origin_congestion_index",
    "dest_congestion_index",
    "hour_sin",
    "hour_cos",
    "month_sin",
    "month_cos",
]

X = df[categorical_features + numeric_features]
y = df[target]


# ============================================================
# 4. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 5. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features,
        ),
        (
            "num",
            StandardScaler(),
            numeric_features,
        ),
    ]
)


# ============================================================
# 6. MODELS
# ============================================================

models = {
    "Logistic Regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        C=0.01,
    ),

    "Decision Tree": DecisionTreeClassifier(
        max_depth=8,
        min_samples_leaf=20,
        random_state=42,
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        min_samples_leaf=10,
        random_state=42,
        n_jobs=1,
        class_weight="balanced",
    ),
}


# ============================================================
# 7. TRAIN AND EVALUATE
# ============================================================

results = []
fitted_pipelines = {}

for name, model in models.items():

    pipe = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ]
    )

    pipe.fit(X_train, y_train)

    fitted_pipelines[name] = pipe

    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]

    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1-Score": f1_score(y_test, y_pred),
        "ROC-AUC": roc_auc_score(y_test, y_proba),
    }

    results.append(metrics)

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(4.5, 4))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["On-time", "Delayed"],
        yticklabels=["On-time", "Delayed"],
    )

    plt.title(f"Confusion Matrix — {name}")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.tight_layout()

    filename = name.lower().replace(" ", "_")

    plt.savefig(
        OUT_DIR / f"confusion_matrix_{filename}.png",
        dpi=150,
    )

    plt.close()

    # Classification report
    with open(
        OUT_DIR / f"classification_report_{filename}.txt",
        "w",
    ) as f:

        f.write(f"Classification Report — {name}\n")
        f.write("=" * 50 + "\n")

        f.write(
            classification_report(
                y_test,
                y_pred,
                target_names=["On-time", "Delayed"],
            )
        )


# ============================================================
# 8. MODEL COMPARISON
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    "F1-Score",
    ascending=False,
)

results_df.to_csv(
    OUT_DIR / "model_comparison.csv",
    index=False,
)

print("\n=== MODEL COMPARISON ===")
print(results_df.to_string(index=False))


# ============================================================
# 9. SAVE BEST MODEL
# ============================================================

best_model_name = results_df.iloc[0]["Model"]

best_pipeline = fitted_pipelines[best_model_name]

model_path = MODEL_DIR / "flight_delay_model.pkl"

joblib.dump(
    best_pipeline,
    model_path,
)

print("\nBest model:", best_model_name)
print("Saved model:", model_path)


# ============================================================
# 10. MODEL COMPARISON CHART
# ============================================================

plot_df = results_df.melt(
    id_vars="Model",
    value_vars=[
        "Accuracy",
        "Precision",
        "Recall",
        "F1-Score",
        "ROC-AUC",
    ],
    var_name="Metric",
    value_name="Score",
)

plt.figure(figsize=(9, 5.5))

sns.barplot(
    data=plot_df,
    x="Metric",
    y="Score",
    hue="Model",
)

plt.ylim(0, 1)
plt.title("Model Performance Comparison")
plt.legend(
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
)

plt.tight_layout()

plt.savefig(
    OUT_DIR / "model_comparison.png",
    dpi=150,
)

plt.close()


# ============================================================
# 11. FEATURE IMPORTANCE
# ============================================================

rf_pipe = fitted_pipelines["Random Forest"]

ohe = (
    rf_pipe
    .named_steps["preprocess"]
    .named_transformers_["cat"]
)

cat_feature_names = list(
    ohe.get_feature_names_out(
        categorical_features
    )
)

all_feature_names = (
    cat_feature_names + numeric_features
)

rf_model = rf_pipe.named_steps["model"]

importances = rf_model.feature_importances_

importance_map = {}

for fname, imp in zip(
    all_feature_names,
    importances,
):

    if fname in numeric_features:

        importance_map[fname] = (
            importance_map.get(fname, 0) + imp
        )

    else:

        base = fname

        for cat in categorical_features:

            if fname.startswith(cat + "_"):
                base = cat
                break

        importance_map[base] = (
            importance_map.get(base, 0) + imp
        )


importance_df = pd.DataFrame(
    sorted(
        importance_map.items(),
        key=lambda x: x[1],
        reverse=True,
    ),
    columns=[
        "Feature",
        "Importance",
    ],
)

importance_df.to_csv(
    OUT_DIR / "feature_importance.csv",
    index=False,
)


# ============================================================
# 12. SAVE SUMMARY
# ============================================================

summary = {
    "n_samples": int(len(df)),
    "delay_rate": float(df["delayed"].mean()),
    "best_model_by_f1": best_model_name,
    "results": results_df.to_dict(
        orient="records"
    ),
    "top_5_features": importance_df.head(
        5
    ).to_dict(orient="records"),
}

with open(
    OUT_DIR / "summary.json",
    "w",
) as f:

    json.dump(
        summary,
        f,
        indent=2,
    )


print("\nAll outputs saved to:", OUT_DIR)