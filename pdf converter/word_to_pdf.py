import sys
import subprocess
import os

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    output_dir = os.path.dirname(output_file)

    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to", "pdf",
        input_file,
        "--outdir", output_dir
    ], check=True)

    # LibreOffice creates PDF with same base filename
    generated_pdf = os.path.join(
        output_dir,
        os.path.splitext(os.path.basename(input_file))[0] + ".pdf"
    )

    # Rename it to the desired output file name
    os.rename(generated_pdf, output_file)

    print("Conversion successful")

except Exception as e:
    print("Conversion failed:", e)
    sys.exit(1)
