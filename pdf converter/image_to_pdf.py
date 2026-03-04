import sys
import os
from PIL import Image

if len(sys.argv) < 2:
    print("Usage: python image_to_pdf.py image1.jpg [image2.png ...]")
    sys.exit(1)

images = sys.argv[1:]
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

for img_path in images:
    try:
        img = Image.open(img_path)
        # Convert to RGB (required for PDF)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        output_file = os.path.join(
            output_folder,
            os.path.splitext(os.path.basename(img_path))[0] + ".pdf"
        )

        img.save(output_file, "PDF")
        print(f"Converted {img_path} → {output_file}")
    except Exception as e:
        print(f"Failed {img_path}: {e}")
