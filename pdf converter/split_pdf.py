import sys
import os
from PyPDF2 import PdfReader, PdfWriter

# Check if user provided file
if len(sys.argv) < 2:
    print("Usage: python split_pdf.py filename.pdf")
    sys.exit(1)

input_pdf = sys.argv[1]

# Create output folder if it doesn't exist
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

reader = PdfReader(input_pdf)

# Loop through every page
for page_num in range(len(reader.pages)):
    writer = PdfWriter()
    writer.add_page(reader.pages[page_num])

    output_filename = os.path.join(
        output_folder,
        f"{os.path.splitext(os.path.basename(input_pdf))[0]}_page_{page_num+1}.pdf"
    )

    with open(output_filename, "wb") as output_file:
        writer.write(output_file)

print(f"Split complete. Files saved in '{output_folder}' folder.")
