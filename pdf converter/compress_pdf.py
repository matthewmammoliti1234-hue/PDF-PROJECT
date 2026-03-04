import sys
import os
import pikepdf

if len(sys.argv) < 2:
    print("Usage: python compress_pdf.py input.pdf")
    sys.exit(1)

input_pdf = sys.argv[1]
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(
    output_folder,
    f"{os.path.splitext(os.path.basename(input_pdf))[0]}_compressed.pdf"
)

try:
    pdf = pikepdf.open(input_pdf)
    pdf.save(output_file)  # default save will reduce size
    pdf.close()
    print(f"Compression complete. Saved to: {output_file}")
except Exception as e:
    print(f"Compression failed: {e}")
