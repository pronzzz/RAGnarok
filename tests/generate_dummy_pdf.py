import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_dummy():
    os.makedirs("tests", exist_ok=True)
    c = canvas.Canvas("tests/dummy.pdf", pagesize=letter)
    c.drawString(100, 750, "RAGnarok Test Document")
    c.drawString(100, 730, "This is a simple paragraph to test extraction.")
    c.save()
    print("Created tests/dummy.pdf")

if __name__ == "__main__":
    create_dummy()
