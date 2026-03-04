import fitz  # PyMuPDF
import sys
import os
import zipfile

# Get input/output from command line
if len(sys.argv) != 3:
    print("Usage: python pdf_to_image.py input.pdf output.zip")
    sys.exit(1)

input_pdf = sys.argv[1]
output_zip = sys.argv[2]

# Ensure the output folder exists
os.makedirs(os.path.dirname(output_zip), exist_ok=True)

# Open PDF
doc = fitz.open(input_pdf)
temp_images = []

# Save each page as PNG
for i, page in enumerate(doc, start=1):
    img_name = f"temp_page_{i}.png"
    pix = page.get_pixmap()
    pix.save(img_name)
    temp_images.append(img_name)

# Zip the images
with zipfile.ZipFile(output_zip, 'w') as zipf:
    for img in temp_images:
        zipf.write(img, arcname=os.path.basename(img))
        os.remove(img)  # delete temp image

print(f"Success! Output saved to {output_zip}")