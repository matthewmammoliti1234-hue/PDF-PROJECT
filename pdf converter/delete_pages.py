import sys
import os
from PyPDF2 import PdfReader, PdfWriter

if len(sys.argv) < 3:
    print("Usage: python delete_pages.py input.pdf page_numbers")
    print("Example: python delete_pages.py document.pdf 1,3,5")
    sys.exit(1)

input_pdf = sys.argv[1]
pages_input = sys.argv[2]

# Convert page numbers to zero-based indices
pages_to_delete = [int(p.strip()) - 1 for p in pages_input.split(",")]

reader = PdfReader(input_pdf)
writer = PdfWriter()

for i, page in enumerate(reader.pages):
    if i not in pages_to_delete:
        writer.add_page(page)

output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    f"{os.path.splitext(os.path.basename(input_pdf))[0]}_deleted.pdf"
)

with open(output_file, "wb") as f:
    writer.write(f)

print(f"Deleted pages complete! Saved to: {output_file}")
