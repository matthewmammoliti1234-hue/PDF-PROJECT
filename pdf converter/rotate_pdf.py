import sys
import os
from PyPDF2 import PdfReader, PdfWriter

# Ensure correct usage
if len(sys.argv) < 3:
    print("Usage: python rotate_pdf.py input.pdf degrees [output.pdf]")
    print("Example: python rotate_pdf.py test.pdf 90 output.pdf")
    sys.exit(1)

# Input PDF and rotation degrees
input_pdf = sys.argv[1]
try:
    degrees = int(sys.argv[2])
except ValueError:
    print("Degrees must be an integer (90, 180, 270)")
    sys.exit(1)

# Optional output file path
if len(sys.argv) >= 4:
    output_file = sys.argv[3]
else:
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(
        output_folder,
        f"{os.path.splitext(os.path.basename(input_pdf))[0]}_rotated.pdf"
    )

# Read PDF and rotate pages
reader = PdfReader(input_pdf)
writer = PdfWriter()

for page in reader.pages:
    page.rotate(degrees)  # positive degrees = clockwise
    writer.add_page(page)

# Write output PDF
with open(output_file, "wb") as f:
    writer.write(f)

print(f"Rotation complete! Saved to: {output_file}")