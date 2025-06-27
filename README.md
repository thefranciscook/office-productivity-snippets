# 🧰 Mac-Friendly Office Tools (Python)

These are lightweight Python scripts built for common office tasks — like turning images into slides, converting PDFs, or splitting multi-page image files. No coding experience needed. If you're a designer, executive assistant, or just someone who works with documents a lot, you're in the right place.

---

## ✅ What You Need

- A Mac (macOS)
- Basic Terminal use
- Python 3 (built into most Macs)
- A one-time install of a few small tools (see below)

---

## 🛠️ One-Time Setup

In Terminal, install the required Python libraries:

```bash
pip3 install pillow python-pptx pymupdf
```

If `pip3` isn't found, install it first with:

```bash
sudo easy_install pip
```

Then rerun the install command.

---

## 📦 What Each Script Does

### `images_to_pptx.py`

Turns a folder of images into a PowerPoint presentation, with each image on its own slide and the filename as a title.

**Usage in Terminal:**

```bash
python3 images_to_pptx.py <image_folder> <output_file.pptx>
```

---

### `pdf_to_png_nomadmin.py`

Converts a PDF into separate PNG image files — one per page. No special permissions or admin installs required.

**Usage in Terminal:**

```bash
python3 pdf_to_png_nomadmin.py <pdf_file.pdf>
```

---

### `extract_pages.py`

Takes a multi-page image file and splits it into separate PNG files (e.g. page_0.png, page_1.png, etc).

**Usage in Terminal:**

```bash
python3 extract_pages.py <input_file.png>
```

---

## 🔧 Requirements Summary

| Library       | Purpose                           |
|---------------|------------------------------------|
| `pillow`      | Image loading and saving           |
| `python-pptx` | Creating PowerPoint (.pptx) files  |
| `pymupdf`     | Reading and exporting PDF pages    |

---

## 💡 Tips

- File and folder names with spaces must be in quotes.
- You can drag folders and files into Terminal to auto-fill their paths.
- Need a simpler interface? These can be wrapped into clickable Mac apps.
