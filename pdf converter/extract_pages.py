import sys
import os
from PyPDF2 import PdfReader, PdfWriter

if len(sys.argv) < 3:
    print("Usage: python extract_pages.py input.pdf page_numbers")
    print("Example: python extract_pages.py test.pdf 1,3,5")
    sys.exit(1)

input_pdf = sys.argv[1]
pages_input = sys.argv[2]

# Convert page numbers from string to list
pages = [int(p.strip()) - 1 for p in pages_input.split(",")]

reader = PdfReader(input_pdf)
writer = PdfWriter()

for page_num in pages:
    if page_num < len(reader.pages):
        writer.add_page(reader.pages[page_num])

output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

output_filename = os.path.join(
    output_folder,
    f"{os.path.splitext(os.path.basename(input_pdf))[0]}_extracted.pdf"
)

with open(output_filename, "wb") as f:
    writer.write(f)

print("Extraction complete.")
