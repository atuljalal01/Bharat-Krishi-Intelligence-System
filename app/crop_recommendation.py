# ==========================================
# Crop Recommendation
# ==========================================

import joblib
import pandas as pd

from pathlib import Path


# ==========================================
# Model Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "crop_recommendation_model.pkl"

ENCODER_PATH = MODEL_DIR / "crop_label_encoder.pkl"


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
# Crop Prediction
# ==========================================

def recommend_crop(
    N,
    P,
    K,
    temperature,
    humidity,
    ph,
    rainfall
):

    input_data = pd.DataFrame([{

        "N": N,
        "P": P,
        "K": K,
        "temperature": temperature,
        "humidity": humidity,
        "ph": ph,
        "rainfall": rainfall

    }])

    prediction = model.predict(
        input_data
    )

    crop_name = label_encoder.inverse_transform(
        prediction
    )[0]

    return crop_name