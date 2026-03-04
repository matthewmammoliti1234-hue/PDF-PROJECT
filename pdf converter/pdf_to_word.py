import sys
import os
import fitz  # PyMuPDF
from docx import Document

# Check for PDF argument
if len(sys.argv) < 2:
    print("Usage: python pdf_to_word.py input.pdf")
    exit()

input_pdf = sys.argv[1]
output_dir = "output"

# Make output folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open PDF
try:
    pdf = fitz.open(input_pdf)
except Exception as e:
    print(f"Failed to open PDF: {e}")
    exit()

# Create Word document
doc = Document()

for page in pdf:
    text = page.get_text()
    if text.strip():  # Only add if there’s text
        doc.add_paragraph(text)

# Save Word file
output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_pdf))[0] + ".docx")
doc.save(output_file)

print(f"Conversion complete! Check {output_file}")
