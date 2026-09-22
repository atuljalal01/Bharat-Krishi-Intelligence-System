# ==========================================
# Mandi Price Prediction
# ==========================================

import joblib
import pandas as pd

from pathlib import Path


# ==========================================
# Model Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "mandi_price_model.pkl"

ENCODER_PATH = MODEL_DIR / "mandi_encoder.pkl"

FEATURE_NAMES_PATH = MODEL_DIR / "mandi_feature_names.pkl"


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
# Categorical Columns
# ==========================================

categorical_columns = [
    "State",
    "District",
    "Market",
    "Commodity",
    "Variety",
    "Grade",
    "Season"
]


# ==========================================
# Season Function
# ==========================================

def get_season(month):

    if month in [12, 1, 2]:
        return "Winter"

    elif month in [3, 4, 5]:
        return "Summer"

    elif month in [6, 7, 8, 9]:
        return "Monsoon"

    else:
        return "Post-Monsoon"


# ==========================================
# Mandi Price Prediction
# ==========================================

def predict_mandi_price(
    state,
    district,
    market,
    commodity,
    variety,
    grade,
    min_price,
    max_price,
    year,
    month,
    day
):

    # --------------------------------------
    # Date Features
    # --------------------------------------

    date = pd.Timestamp(
        year=year,
        month=month,
        day=day
    )

    day_of_week = date.dayofweek

    week = int(
        date.isocalendar().week
    )

    quarter = date.quarter

    season = get_season(
        month
    )


    # --------------------------------------
    # Create Input DataFrame
    # --------------------------------------

    input_data = pd.DataFrame({

        "State": [state],

        "District": [district],

        "Market": [market],

        "Commodity": [commodity],

        "Variety": [variety],

        "Grade": [grade],

        "Min_Price": [min_price],

        "Max_Price": [max_price],

        "Year": [year],

        "Month": [month],

        "Day": [day],

        "DayOfWeek": [day_of_week],

        "Week": [week],

        "Quarter": [quarter],

        "Season": [season]

    })


    # --------------------------------------
    # Encode Categorical Features
    # --------------------------------------

    input_data[categorical_columns] = (
        encoder.transform(
            input_data[categorical_columns]
        )
    )


    # --------------------------------------
    # Ensure Feature Order
    # --------------------------------------

    input_data = input_data.reindex(
        columns=feature_names
    )


    # --------------------------------------
    # Prediction
    # --------------------------------------

    predicted_price = model.predict(
        input_data
    )[0]


    return predicted_price