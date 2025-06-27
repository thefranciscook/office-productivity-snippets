import sys
from PIL import Image

if len(sys.argv) < 2:
    print("Usage: python3 extract_png_pages.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

try:
    im = Image.open(input_file)
except FileNotFoundError:
    print(f"File not found: {input_file}")
    sys.exit(1)
except Exception as e:
    print(f"Error opening file: {e}")
    sys.exit(1)

i = 0
while True:
    try:
        im.seek(i)
        im.save(f"page_{i}.png")
        print(f"Saved page_{i}.png")
        i += 1
    except EOFError:
        print("Done extracting all pages.")
        break
