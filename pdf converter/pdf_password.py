import sys
from PyPDF2 import PdfReader, PdfWriter

if len(sys.argv) < 5:
    print("Usage: python pdf_password.py input.pdf output.pdf lock/unlock password")
    sys.exit(1)

input_pdf = sys.argv[1]
output_pdf = sys.argv[2]
mode = sys.argv[3].lower()
password = sys.argv[4]

try:
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    if mode == "lock":
        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        with open(output_pdf, "wb") as f:
            writer.write(f)

        print("PDF locked successfully")

    elif mode == "unlock":

        if not reader.is_encrypted:
            print("PDF is not encrypted")
            sys.exit(1)

        # Attempt decryption
        result = reader.decrypt(password)

        if result == 0:
            print("Wrong password")
            sys.exit(1)

        # NOW safely read pages
        for page in reader.pages:
            writer.add_page(page)

        with open(output_pdf, "wb") as f:
            writer.write(f)

        print("PDF unlocked successfully")

    else:
        print("Mode must be 'lock' or 'unlock'")
        sys.exit(1)

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)