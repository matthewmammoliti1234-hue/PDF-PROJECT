import sys
import os
import fitz  # PyMuPDF

if len(sys.argv) < 2:
    print("Usage: python pdf_to_text.py input.pdf")
    sys.exit(1)

input_pdf = sys.argv[1]
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    os.path.splitext(os.path.basename(input_pdf))[0] + ".txt"
)

pdf = fitz.open(input_pdf)
with open(output_file, "w", encoding="utf-8") as f:
    for page_num, page in enumerate(pdf):
        text = page.get_text()
        f.write(f"--- Page {page_num+1} ---\n")
        f.write(text + "\n\n")

pdf.close()
print(f"Text extracted! Saved to: {output_file}")
