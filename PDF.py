from fpdf import FPDF

# Sample data for the 30 features
features_with_values = {
    "radius_mean": 17.99,
    "texture_mean": 10.38,
    "perimeter_mean": 122.8,
    "area_mean": 1001.0,
    "smoothness_mean": 0.1184,
    "compactness_mean": 0.2776,
    "concavity_mean": 0.3001,
    "concave_points_mean": 0.1471,
    "symmetry_mean": 0.2419,
    "fractal_dimension_mean": 0.07871,
    "radius_se": 1.095,
    "texture_se": 0.9053,
    "perimeter_se": 8.589,
    "area_se": 153.4,
    "smoothness_se": 0.006399,
    "compactness_se": 0.04904,
    "concavity_se": 0.05373,
    "concave_points_se": 0.01587,
    "symmetry_se": 0.03003,
    "fractal_dimension_se": 0.006193,
    "radius_worst": 25.38,
    "texture_worst": 17.33,
    "perimeter_worst": 184.6,
    "area_worst": 2019.0,
    "smoothness_worst": 0.1622,
    "compactness_worst": 0.6656,
    "concavity_worst": 0.7119,
    "concave_points_worst": 0.2654,
    "symmetry_worst": 0.4601,
    "fractal_dimension_worst": 0.1189
}

# Function to create the PDF
def create_breast_cancer_report(output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # Add title
    pdf.cell(0, 10, "Sample Breast Cancer Report for Testing", ln=1, align='C')
    pdf.ln(10)
    pdf.cell(0, 10, "Below are the 30 features with their respective values:", ln=1)
    pdf.ln(5)

    # Add features and values
    for feature, value in features_with_values.items():
        pdf.cell(0, 10, f"{feature}: {value}", ln=1)

    # Save the PDF
    pdf.output(output_path)

# Specify the file path for the PDF
output_file = "Breast_Cancer_Test_Report.pdf"
create_breast_cancer_report(output_file)
print(f"PDF report created: {output_file}")
