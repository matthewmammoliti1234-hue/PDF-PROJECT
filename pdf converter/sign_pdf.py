import sys
import os
import fitz  # PyMuPDF

if len(sys.argv) < 5:
    print("Usage: python sign_pdf.py input.pdf signature.png page_number x y")
    print("Example: python sign_pdf.py document.pdf signature.png 1 100 150")
    sys.exit(1)

input_pdf = sys.argv[1]
signature_img = sys.argv[2]
page_number = int(sys.argv[3]) - 1  # zero-based
x = float(sys.argv[4])
y = float(sys.argv[5])

output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    f"{os.path.splitext(os.path.basename(input_pdf))[0]}_signed.pdf"
)

try:
    pdf = fitz.open(input_pdf)
    page = pdf[page_number]

    # Insert image
    rect = fitz.Rect(x, y, x + 200, y + 100)  # width 200, height 100, adjust if needed
    page.insert_image(rect, filename=signature_img)

    pdf.save(output_file)
    pdf.close()
    print(f"Signature added! Saved to: {output_file}")
except Exception as e:
    print(f"Signing failed: {e}")
