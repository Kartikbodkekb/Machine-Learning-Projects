"""
Ames Housing Price Prediction API
FastAPI backend serving the trained linear regression pipeline
and the frontend static files.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import pickle
import json
import pandas as pd
import os

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Ames Housing Price Prediction API",
    description="Predicts house sale prices using the Ames Housing Dataset model.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load model & metadata ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "ames_housing_model.pkl")
META_PATH  = os.path.join(BASE_DIR, "..", "models", "model_meta.json")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(META_PATH, "r") as f:
    meta = json.load(f)

# ── Request / Response schemas ─────────────────────────────────────────────────
class HouseFeatures(BaseModel):
    year_built:    int   = Field(..., ge=1800, le=2025, description="Year the house was built")
    garage_cars:   float = Field(..., ge=0,    le=5,    description="Garage capacity (cars)")
    first_flr_sf:  int   = Field(..., ge=0,            description="First floor square footage")
    gr_liv_area:   int   = Field(..., ge=0,            description="Above grade living area (sq ft)")
    full_bath:     int   = Field(..., ge=0,    le=10,   description="Number of full bathrooms")
    bedroom_abvgr: int   = Field(..., ge=0,    le=15,   description="Bedrooms above grade")
    neighborhood:  str   = Field(...,                   description="Neighborhood name")
    foundation:    str   = Field(...,                   description="Foundation type")
    house_style:   str   = Field(...,                   description="House style")
    bldg_type:     str   = Field(...,                   description="Building type")

class PredictionResponse(BaseModel):
    predicted_price: float
    formatted_price: str
    model_r2:        float = 0.8544

# ── Endpoints ──────────────────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "model": "LinearRegression", "r2_score": 0.8544}


@app.get("/meta", tags=["Metadata"])
def get_meta():
    """Return valid categorical values for frontend dropdowns."""
    return meta


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict(features: HouseFeatures):
    """Predict house sale price from input features."""

    # Validate categoricals
    if features.neighborhood not in meta["neighborhoods"]:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown neighborhood '{features.neighborhood}'. Valid: {meta['neighborhoods']}"
        )
    if features.foundation not in meta["foundations"]:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown foundation '{features.foundation}'. Valid: {meta['foundations']}"
        )
    if features.house_style not in meta["house_styles"]:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown house style '{features.house_style}'. Valid: {meta['house_styles']}"
        )
    if features.bldg_type not in meta["bldg_types"]:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown building type '{features.bldg_type}'. Valid: {meta['bldg_types']}"
        )

    # Build input DataFrame matching training column names exactly
    # Note: 'Year Built' appears twice in numerica_col — that's how the notebook had it
    row = {
        "Year Built":    features.year_built,
        "Garage Cars":   features.garage_cars,
        "1st Flr SF":    features.first_flr_sf,
        "Gr Liv Area":   features.gr_liv_area,
        "Full Bath":     features.full_bath,
        "Bedroom AbvGr": features.bedroom_abvgr,
        "Neighborhood":  features.neighborhood,
        "Foundation":    features.foundation,
        "House Style":   features.house_style,
        "Bldg Type":     features.bldg_type,
    }
    df = pd.DataFrame([row])

    price = float(model.predict(df)[0])
    price = max(price, 0)  # clamp negative predictions

    return PredictionResponse(
        predicted_price=round(price, 2),
        formatted_price=f"${price:,.0f}",
    )


# ── Serve frontend static files ────────────────────────────────────────────────
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

@app.get("/", include_in_schema=False)
def serve_index():
    """Serve the frontend index.html at the root URL."""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Mount static assets (CSS, JS) under /static
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
