# ==========================================
# Fertilizer Recommendation
# ==========================================

import joblib
import pandas as pd

from pathlib import Path


# ==========================================
# Model Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "fertilizer_recommendation_model.pkl"

ENCODER_PATH = MODEL_DIR / "fertilizer_label_encoder.pkl"

FEATURE_NAMES_PATH = MODEL_DIR / "fertilizer_feature_names.pkl"

REMARK_LOOKUP_PATH = MODEL_DIR / "fertilizer_remark_lookup.pkl"


# ==========================================
# Load Model
# ==========================================

model = joblib.load(
    MODEL_PATH
)


# ==========================================
# Load Label Encoder
# ==========================================

label_encoder = joblib.load(
    ENCODER_PATH
)


# ==========================================
# Load Feature Names
# ==========================================

feature_names = joblib.load(
    FEATURE_NAMES_PATH
)


# ==========================================
# Load Remark Lookup
# ==========================================

remark_lookup = joblib.load(
    REMARK_LOOKUP_PATH
)


# ==========================================
# Fertilizer Prediction
# ==========================================

def recommend_fertilizer(
    temperature,
    moisture,
    rainfall,
    ph,
    nitrogen,
    phosphorous,
    potassium,
    carbon,
    soil,
    crop
):

    # Create empty input DataFrame
    input_data = pd.DataFrame(
        0,
        index=[0],
        columns=feature_names
    )

    # Numerical features
    input_data["Temperature"] = temperature
    input_data["Moisture"] = moisture
    input_data["Rainfall"] = rainfall
    input_data["PH"] = ph
    input_data["Nitrogen"] = nitrogen
    input_data["Phosphorous"] = phosphorous
    input_data["Potassium"] = potassium
    input_data["Carbon"] = carbon

    # Categorical features
    soil_column = f"Soil_{soil}"
    crop_column = f"Crop_{crop}"

    if soil_column in input_data.columns:
        input_data[soil_column] = 1

    if crop_column in input_data.columns:
        input_data[crop_column] = 1

    # Prediction
    prediction = model.predict(
        input_data
    )

    # Convert encoded prediction to fertilizer name
    fertilizer = label_encoder.inverse_transform(
        prediction
    )[0]

    # Get corresponding remark
    remark = remark_lookup.get(
        fertilizer,
        "No additional information available."
    )

    return fertilizer, remark