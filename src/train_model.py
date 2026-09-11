from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "csv" / "training.csv"
MODEL_PATH = BASE_DIR / "artifacts" / "carguard_model.joblib"

NUMERIC_COLUMNS = [
    "VehYear",
    "VehicleAge",
    "VehOdo",
    "MMRAcquisitionAuctionAveragePrice",
    "MMRAcquisitionAuctionCleanPrice",
    "MMRAcquisitionRetailAveragePrice",
    "MMRAcquisitonRetailCleanPrice",
    "MMRCurrentAuctionAveragePrice",
    "MMRCurrentAuctionCleanPrice",
    "MMRCurrentRetailAveragePrice",
    "MMRCurrentRetailCleanPrice",
    "VehBCost",
    "WarrantyCost",
]

CATEGORICAL_COLUMNS = [
    "Auction",
    "Make",
    "Model",
    "Transmission",
    "WheelType",
    "Nationality",
    "Size",
    "TopThreeAmericanName",
    "Color",
    "PRIMEUNIT",
    "AUCGUART",
    "VNST",
    "IsOnlineSale",
]

FEATURE_COLUMNS = NUMERIC_COLUMNS + CATEGORICAL_COLUMNS


def build_model_pipeline() -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median"))]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_COLUMNS),
            ("cat", categorical_transformer, CATEGORICAL_COLUMNS),
        ]
    )

    model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        solver="liblinear",
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )


def main() -> None:
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["IsBadBuy"]).copy()
    df["IsBadBuy"] = df["IsBadBuy"].astype(int)

    X = df[FEATURE_COLUMNS]
    y = df["IsBadBuy"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = build_model_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("Accuracy:", round(accuracy, 4))
    print("F1-score:", round(f1, 4))
    print(classification_report(y_test, y_pred, target_names=["Boa compra", "Má compra"]))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Modelo salvo em: {MODEL_PATH}")


if __name__ == "__main__":
    main()
