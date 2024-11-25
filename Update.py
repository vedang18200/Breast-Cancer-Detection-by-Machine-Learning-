import joblib
import numpy as np
import pdfplumber  # 
import re  # For regex-based extraction

# Load the model
model_path = "V:\\Breast_cancer\\model\\breast_cancer_model.pkl"
model = joblib.load(model_path)

# Define the feature names
features = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave_points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
    "compactness_se", "concavity_se", "concave_points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave_points_worst", "symmetry_worst", "fractal_dimension_worst"
]

def extract_parameters_from_pdf(file_path):
    """Extract parameters from a PDF medical report."""
    extracted_data = {}
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        
        # Extract each feature using regex
        for feature in features:
            # Match the feature name followed by a numeric value
            match = re.search(rf"{feature}[:\s]+([0-9.]+)", text, re.IGNORECASE)
            if match:
                extracted_data[feature] = float(match.group(1))
        
    except Exception as e:
        print(f"Error reading PDF: {e}")
    
    return extracted_data

# Prompt the user to upload their PDF report
report_path = input("Upload the path to your medical report (PDF format): ")
extracted_data = extract_parameters_from_pdf(report_path)

# Check if all features are extracted
if len(extracted_data) != len(features):
    print("\nSome parameters are missing from the report. Please input them manually.")
    for feature in features:
        if feature not in extracted_data:
            value = float(input(f"Enter {feature}: "))
            extracted_data[feature] = value

# Convert the extracted features to a NumPy array
input_data = np.array([extracted_data[feature] for feature in features]).reshape(1, -1)

# Make prediction
prediction = model.predict(input_data)
prediction_label = "Malignant" if prediction[0] == 1 else "Benign"

print(f"\nPrediction: {prediction_label}")
