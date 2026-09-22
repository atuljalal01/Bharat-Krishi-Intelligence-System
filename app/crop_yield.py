# ==========================================
# Crop Yield Prediction
# ==========================================

import joblib
import pandas as pd

from pathlib import Path


# ==========================================
# Model Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "yield_prediction_model.pkl"

ENCODER_PATH = MODEL_DIR / "yield_encoder.pkl"

FEATURE_NAMES_PATH = MODEL_DIR / "yield_feature_names.pkl"

CATEGORICAL_COLUMNS_PATH = (
    MODEL_DIR / "yield_categorical_columns.pkl"
)


# ==========================================
# Load Model
# ==========================================

model = joblib.load(
    MODEL_PATH
)


# ==========================================
# Load Encoder
# ==========================================

encoder = joblib.load(
    ENCODER_PATH
)


# ==========================================
# Load Feature Names
# ==========================================

feature_names = joblib.load(
    FEATURE_NAMES_PATH
)


# ==========================================
# Load Categorical Columns
# ==========================================

categorical_columns = joblib.load(
    CATEGORICAL_COLUMNS_PATH
)


# ==========================================
# Crop Yield Prediction
# ==========================================

def predict_crop_yield(
    crop_year,
    area,
    production,
    annual_rainfall,
    fertilizer,
    pesticide,
    crop,
    season,
    state
):

    # --------------------------------------
    # Create Raw Input DataFrame
    # --------------------------------------

    input_data = pd.DataFrame([{

        "Crop_Year": crop_year,
        "Area": area,
        "Production": production,
        "Annual_Rainfall": annual_rainfall,
        "Fertilizer": fertilizer,
        "Pesticide": pesticide,

        "Fertilizer_per_Area":
            fertilizer / area if area != 0 else 0,

        "Pesticide_per_Area":
            pesticide / area if area != 0 else 0,

        "Crop": crop,
        "Season": season,
        "State": state

    }])


    # --------------------------------------
    # Separate Numerical Features
    # --------------------------------------

    numerical_features = [
        "Crop_Year",
        "Area",
        "Production",
        "Annual_Rainfall",
        "Fertilizer",
        "Pesticide",
        "Fertilizer_per_Area",
        "Pesticide_per_Area"
    ]


    X_num = input_data[
        numerical_features
    ]


    # --------------------------------------
    # One-Hot Encode Categorical Features
    # --------------------------------------

    X_cat = encoder.transform(
        input_data[categorical_columns]
    )

    X_cat = pd.DataFrame(
        X_cat,
        columns=encoder.get_feature_names_out(
            categorical_columns
        ),
        index=input_data.index
    )


    # --------------------------------------
    # Combine Numerical + Categorical
    # --------------------------------------

    X_final = pd.concat(
        [
            X_num,
            X_cat
        ],
        axis=1
    )


    # --------------------------------------
    # Ensure Exact Feature Order
    # --------------------------------------

    X_final = X_final.reindex(
        columns=feature_names,
        fill_value=0
    )


    # --------------------------------------
    # Prediction
    # --------------------------------------

    prediction = model.predict(
        X_final
    )

    return prediction[0]