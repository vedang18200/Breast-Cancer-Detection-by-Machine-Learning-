import tensorflow as tf

import numpy as np
import cv2


def preprocess_image(image_path, target_size=(128, 128)):
    """
    Preprocess the input image to match the model's requirements.
    Args:
        image_path (str): Path to the input image.
        target_size (tuple): Target size for the model (height, width).
    Returns:
        numpy.ndarray: Preprocessed image ready for model input.
    """
    # Load the image in grayscale
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found at path: {image_path}")
    
    # Resize and normalize the image
    img = cv2.resize(img, target_size)  # Resize to (128, 128)
    img = img / 255.0  # Normalize pixel values to [0, 1]
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img
# Step 5: Load the saved model and predict
print("Loading the saved model...")
loaded_model = tf.keras.models.load_model('V:\\Breast_cancer\\model\\breast_cancer_model.h5')

# Test prediction on a new image
image_path = input("Enter the path to the breast cancer image: ")
try:
    preprocessed_image = preprocess_image(image_path)
    prediction = loaded_model.predict(preprocessed_image)
    result = "Malignant" if prediction[0][0] > 0.5 else "Benign"
    print(f"The predicted cancer type is: {result}")
except ValueError as e:
    print(e)