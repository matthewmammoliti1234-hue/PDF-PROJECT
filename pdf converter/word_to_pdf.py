import sys
import os
from docx2pdf import convert

if len(sys.argv) < 2:
    print("Usage: python word_to_pdf.py input.docx")
    sys.exit(1)

input_docx = sys.argv[1]
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Convert Word to PDF
try:
    # If you want to save in output folder
    convert(input_docx, os.path.join(output_folder, os.path.splitext(os.path.basename(input_docx))[0] + ".pdf"))
    print(f"Conversion complete! Check output folder for PDF.")
except Exception as e:
    print(f"Conversion failed: {e}")
