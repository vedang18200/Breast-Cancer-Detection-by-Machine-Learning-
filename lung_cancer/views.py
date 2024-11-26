

from django.shortcuts import render
from django.conf import settings
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

# Parameters
input_shape = (128, 128, 3)
class_names = ['Benign', 'Malignant', 'Normal']

# Load the model once during server startup

model_path = os.path.join(settings.MODEL_DIR, 'lung_cancer.h5')
try:
    model = load_model(model_path)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# Preprocessing function
def preprocess_image(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize(input_shape[:2])
        image = np.array(image, dtype=np.float32) / 255.0
        image = np.expand_dims(image, axis=0)
        return image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Prediction function
def predict_image(image_path):
    if model is None:
        return None, "Model not loaded"
    image = preprocess_image(image_path)
    if image is not None:
        try:
            prediction = model.predict(image)
            predicted_class_index = np.argmax(prediction, axis=1)[0]
            confidence = np.max(prediction)
            predicted_class_name = class_names[predicted_class_index]
            return predicted_class_name, confidence
        except Exception as e:
            return None, f"Prediction error: {e}"
    return None, "Image preprocessing failed"

# Django view to handle file upload and display results
def lung_cancer_detection(request):
    context = {
        'result': None,
        'confidence': None,
        'error': None,
        'info': None,
    }

    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        file_path = f"temp/{file.name}"

        try:
            os.makedirs("temp", exist_ok=True)
            with open(file_path, 'wb+') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)

            predicted_class, confidence = predict_image(file_path)
            os.remove(file_path)

            if predicted_class:
                context['result'] = predicted_class
                context['confidence'] = f"{confidence:.2f}"
                context['info'] = {
                    'Normal': "The CT scan appears to show no signs of abnormalities.",
                    'Malignant': "The CT scan indicates a malignant lesion. Please consult an oncologist.",
                    'Benign': "The CT scan suggests a benign growth. Regular monitoring is recommended."
                }.get(predicted_class, "Unknown result. Please consult a specialist.")
            else:
                context['error'] = confidence

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'lungcancer.html', context)
