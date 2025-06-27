import sys
import os
import fitz  # PyMuPDF

if len(sys.argv) < 2:
    print("Usage: python3 pdf_to_png_nomadmin.py <pdf_file>")
    sys.exit(1)

pdf_path = sys.argv[1]

if not os.path.isfile(pdf_path):
    print(f"File not found: {pdf_path}")
    sys.exit(1)

basename = os.path.splitext(os.path.basename(pdf_path))[0]
output_folder = os.getcwd()

doc = fitz.open(pdf_path)

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    # Zoom factor to simulate ~300 DPI
    zoom = 300 / 72  # default is 72 DPI
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    out_path = os.path.join(output_folder, f"{basename}_page_{page_num}.png")
    pix.save(out_path)
    print(f"Saved: {out_path}")

print("Done.")
