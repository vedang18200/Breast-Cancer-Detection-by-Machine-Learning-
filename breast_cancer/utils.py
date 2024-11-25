import tensorflow as tf
import numpy as np
import cv2
import pdfplumber
import re
import joblib
import os

# Load TensorFlow model for images
image_model_path = os.path.join("V:/Breast_cancer/model", "breast_cancer_model.h5")
image_model = tf.keras.models.load_model(image_model_path)

# Load joblib model for PDFs
pdf_model_path = os.path.join("V:/Breast_cancer/model", "breast_cancer_model.pkl")
pdf_model = joblib.load(pdf_model_path)

# Features expected in PDF reports
features = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave_points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
    "compactness_se", "concavity_se", "concave_points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave_points_worst", "symmetry_worst", "fractal_dimension_worst"
]


def preprocess_image(image_path, target_size=(128, 128)):
    """Preprocess an image for TensorFlow model."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found at path: {image_path}")

    img = cv2.resize(img, target_size)
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img


def predict_image(image_path):
    """Predict cancer type from an image using TensorFlow model."""
    preprocessed_image = preprocess_image(image_path)
    prediction = image_model.predict(preprocessed_image)
    return "Malignant" if prediction[0][0] > 0.5 else "Benign"


def extract_parameters_from_pdf(file_path):
    """Extract features from a PDF medical report."""
    extracted_data = {}
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "".join([page.extract_text() for page in pdf.pages])

        for feature in features:
            match = re.search(rf"{feature}[:\s]+([0-9.]+)", text, re.IGNORECASE)
            if match:
                extracted_data[feature] = float(match.group(1))
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {e}")

    if not extracted_data:
        raise ValueError("No valid features found in the PDF.")
    return extracted_data


def make_pdf_prediction(data):
    """Predict cancer type from extracted PDF data."""
    if len(data) != len(features):
        missing = [f for f in features if f not in data]
        raise ValueError(f"Missing features in PDF: {missing}")

    input_data = np.array([data[feature] for feature in features]).reshape(1, -1)
    prediction = pdf_model.predict(input_data)
    return "Malignant" if prediction[0] == 1 else "Benign"
