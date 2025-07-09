# 🧰 Mac‑Friendly Office Tools (Python)

These lightweight Python scripts help with everyday office tasks — like turning images into slides, converting PDFs, **converting Word documents to Markdown**, cleaning up HTML, **merging Markdown files based on a Table of Contents**, or splitting multi‑page image files. No coding experience needed. If you're a designer, executive assistant, or just someone who works with documents a lot, you're in the right place.

---

## ✅ What You Need

- A Mac (macOS)
- Basic Terminal use
- Python 3 (built into most Macs)
- A one‑time install of a few small tools (see below)

---

## 🛠️ One‑Time Setup

In Terminal, install the required Python libraries:

```bash
pip3 install pillow python-pptx pymupdf beautifulsoup4 markdownify python-docx
```

If `pip3` isn't found, install it first with:

```bash
sudo easy_install pip
```

Then rerun the install command.

---

## 📦 What Each Script Does

### `combine_by_toc.py`

Merges a folder of Markdown files into **one combined document** that follows the order and hierarchy of a bullet‑list Table of Contents (ToC) file.  
Features:

- Fuzzy matching between ToC entries and filenames (handles punctuation, spaces, URL‑encoding).  
- Skips headings that have no matching file.  
- Appends any “orphan” Markdown files under an **Unreferenced files** section.  
- Uses only the Python standard library.

**Usage in Terminal:**

```bash
python3 combine_by_toc.py <toc_file.md> <folder_with_md_files> -o combined.md
```

---

### `docx2md.py`

Converts a folder of **`.doc` / `.docx` Word files** to Markdown:

- **True `.docx`** files → Markdown via `python-docx`.
- **Confluence “Word” exports** (MIME‑wrapped HTML) → Markdown after HTML extraction.
- **Legacy binary `.doc`** files are detected and skipped with a clear error.

**Usage in Terminal:**

```bash
python3 docx2md.py <input_folder_with_docs> [output_folder]
```

If `output_folder` is omitted, Markdown files are created beside the originals.

---

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

Takes a multi‑page image file and splits it into separate PNG files (e.g. `page_0.png`, `page_1.png`, etc).

**Usage in Terminal:**

```bash
python3 extract_pages.py <input_file.png>
```

---

### `clean_html.py`

Cleans an HTML file or fragment by removing:

- Inline SVGs  
- All classes and IDs  
- `aria-*` attributes  
- `style` attributes  
- (And more clutter)

Great for preparing HTML for documentation or Markdown conversion.

**Usage in Terminal:**

```bash
python3 clean_html.py <input_file.html> <output_file.html>
```

---

### `html2md.py`

Converts an HTML list or fragment into a clean, readable Markdown list. Ideal for moving web‑based outlines or lists into Markdown docs.

**Usage in Terminal:**

```bash
python3 html2md.py <input_file.html> <output_file.md>
```

---

## 🔧 Requirements Summary

| Library          | Purpose                                   |
|------------------|-------------------------------------------|
| `pillow`         | Image loading and saving                  |
| `python-pptx`    | Creating PowerPoint (.pptx) files         |
| `pymupdf`        | Reading and exporting PDF pages           |
| `beautifulsoup4` | HTML parsing and cleanup                  |
| `markdownify`    | Converting HTML to Markdown               |
| `python-docx`    | Reading `.docx` files for conversion      |
| — (stdlib only)  | `combine_by_toc.py` — no extra libraries  |

---

## 💡 Tips

- File and folder names with spaces must be in quotes.
- You can drag folders and files into Terminal to auto‑fill their paths.
- Need a simpler interface? These scripts can be wrapped into clickable Mac apps.
