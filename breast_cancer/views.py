import os
import uuid  # To generate unique filenames
from django.conf import settings
from django.shortcuts import render
from .utils import predict_image, extract_parameters_from_pdf, make_pdf_prediction

def predict_cancer(request):
    """
    Handles the prediction based on file type: mammogram image or PDF report.
    """
    result = None  # Initialize result for rendering
    error = None   # Initialize error for rendering

    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        # Generate a unique filename to prevent overwriting
        unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
        file_path = os.path.join(settings.MEDIA_ROOT, unique_filename)

        try:
            # Save the uploaded file
            with open(file_path, "wb") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            # Determine the upload type
            upload_type = request.POST.get("upload-type")
            if upload_type == "image":
                # Predict based on mammogram image
                result = predict_image(file_path)
            elif upload_type == "pdf":
                # Predict based on PDF report
                extracted_data = extract_parameters_from_pdf(file_path)
                result = make_pdf_prediction(extracted_data)
            else:
                error = "Invalid file type selected."
        except Exception as e:
            error = f"Error: {str(e)}"
        finally:
            # Ensure the file is deleted after processing
            if os.path.exists(file_path):
                os.remove(file_path)

    # Render the template with the prediction result or error
    return render(request, "index.html", {"result": result, "error": error})
