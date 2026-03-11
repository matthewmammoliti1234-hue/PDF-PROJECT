import sys
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

input_file = sys.argv[1]
output_file = sys.argv[2]

doc = Document(input_file)

c = canvas.Canvas(output_file, pagesize=letter)
width, height = letter
y = height - 50

for para in doc.paragraphs:
    text = para.text
    c.drawString(50, y, text)
    y -= 20

    if y < 50:
        c.showPage()
        y = height - 50

c.save()

print("Conversion successful")
