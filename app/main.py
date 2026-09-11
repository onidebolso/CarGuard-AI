from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "carguard_model.joblib"

app = FastAPI(title="CarGuard AI", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class VehicleInput(BaseModel):
    Auction: str = "ADESA"
    VehYear: int = 2018
    VehicleAge: int = 3
    Make: str = "FORD"
    Model: str = "FUSION"
    Transmission: str = "AUTO"
    WheelType: str = "Alloy"
    VehOdo: int = 85000
    Nationality: str = "AMERICAN"
    Size: str = "MEDIUM"
    TopThreeAmericanName: str = "OTHER"
    Color: str = "RED"
    MMRAcquisitionAuctionAveragePrice: float = 12000.0
    MMRAcquisitionAuctionCleanPrice: float = 14000.0
    MMRAcquisitionRetailAveragePrice: float = 17000.0
    MMRAcquisitonRetailCleanPrice: float = 18600.0
    MMRCurrentAuctionAveragePrice: float = 11000.0
    MMRCurrentAuctionCleanPrice: float = 13000.0
    MMRCurrentRetailAveragePrice: float = 16000.0
    MMRCurrentRetailCleanPrice: float = 17400.0
    PRIMEUNIT: str = "NULL"
    AUCGUART: str = "NULL"
    VNST: str = "FL"
    VehBCost: float = 32000.0
    IsOnlineSale: int = 0
    WarrantyCost: float = 1200.0


@app.get("/")
def home() -> dict:
    return {"message": "CarGuard AI API está online."}


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_exists": MODEL_PATH.exists()}


@app.post("/predict")
def predict(vehicle: VehicleInput) -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Modelo ainda não foi treinado. Execute python src/train_model.py")

    model = joblib.load(MODEL_PATH)

    row = {
        "Auction": vehicle.Auction,
        "VehYear": vehicle.VehYear,
        "VehicleAge": vehicle.VehicleAge,
        "Make": vehicle.Make,
        "Model": vehicle.Model,
        "Transmission": vehicle.Transmission,
        "WheelType": vehicle.WheelType,
        "VehOdo": vehicle.VehOdo,
        "Nationality": vehicle.Nationality,
        "Size": vehicle.Size,
        "TopThreeAmericanName": vehicle.TopThreeAmericanName,
        "Color": vehicle.Color,
        "MMRAcquisitionAuctionAveragePrice": vehicle.MMRAcquisitionAuctionAveragePrice,
        "MMRAcquisitionAuctionCleanPrice": vehicle.MMRAcquisitionAuctionCleanPrice,
        "MMRAcquisitionRetailAveragePrice": vehicle.MMRAcquisitionRetailAveragePrice,
        "MMRAcquisitonRetailCleanPrice": vehicle.MMRAcquisitonRetailCleanPrice,
        "MMRCurrentAuctionAveragePrice": vehicle.MMRCurrentAuctionAveragePrice,
        "MMRCurrentAuctionCleanPrice": vehicle.MMRCurrentAuctionCleanPrice,
        "MMRCurrentRetailAveragePrice": vehicle.MMRCurrentRetailAveragePrice,
        "MMRCurrentRetailCleanPrice": vehicle.MMRCurrentRetailCleanPrice,
        "PRIMEUNIT": vehicle.PRIMEUNIT,
        "AUCGUART": vehicle.AUCGUART,
        "VNST": vehicle.VNST,
        "VehBCost": vehicle.VehBCost,
        "IsOnlineSale": vehicle.IsOnlineSale,
        "WarrantyCost": vehicle.WarrantyCost,
    }

    df = pd.DataFrame([row])
    prob_bad = float(model.predict_proba(df)[0][1])
    prediction = int(prob_bad >= 0.5)
    decision = "Compra de risco" if prediction == 1 else "Boa oportunidade"
    confidence = round(prob_bad * 100, 2) if prediction == 1 else round((1 - prob_bad) * 100, 2)

    return {
        "prediction": prediction,
        "decision": decision,
        "confidence": confidence,
        "probability_bad_buy": round(prob_bad, 4),
        "probability_good_buy": round(1 - prob_bad, 4),
    }
