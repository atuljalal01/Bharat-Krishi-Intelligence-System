import json
from pathlib import Path

import numpy as np
from PIL import Image
import tensorflow as tf 
from tensorflow.keras.models import load_model

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

MODEL_PATH = MODEL_DIR / "best_crop_disease_model.keras"

CLASS_NAMES_PATH = MODEL_DIR / "class_names.json"


model = load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r") as file:
    class_names = json.load(file)


def preprocess_image(image):

    image = image.resize((224, 224))

    image = np.array(image)

    if image.shape[-1] == 4:
        image = image[:, :, :3]

    image = image / 255.0

    image = np.expand_dims(
        image,
        axis=0
    )

    return image


def predict_disease(image):

    processed_image = preprocess_image(
        image
    )

    prediction = model.predict(
        processed_image,
        verbose=0
    )

    predicted_index = np.argmax(
        prediction[0]
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = float(
        np.max(prediction[0])
    )

    return predicted_class, confidence