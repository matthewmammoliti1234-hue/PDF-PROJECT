import sys
import subprocess
import os

input_file = sys.argv[1]
output_file = sys.argv[2]

try:
    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to",
        "pdf",
        input_file,
        "--outdir",
        os.path.dirname(output_file)
    ], check=True)

    print("Conversion successful")

except Exception as e:
    print("Conversion failed:", e)
    sys.exit(1)
