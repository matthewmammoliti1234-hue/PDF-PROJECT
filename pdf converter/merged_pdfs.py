import sys
import os
from PyPDF2 import PdfMerger

if len(sys.argv) < 3:
    print("Usage: python merge_pdfs.py file1.pdf file2.pdf [file3.pdf ...]")
    exit()

output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

merger = PdfMerger()

for pdf in sys.argv[1:]:
    merger.append(pdf)

output_file = os.path.join(output_dir, "merged.pdf")
merger.write(output_file)
merger.close()

print(f"Merged PDF created: {output_file}")
