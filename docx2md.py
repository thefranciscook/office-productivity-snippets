import os
import sys
import zipfile
import email
from markdownify import markdownify as md

from docx import Document

def is_zipfile(path):
    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            return True
    except zipfile.BadZipFile:
        return False

def is_html_mime(path):
    # Quick test: look for "Content-Type: multipart/" and <html
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            first_2k = f.read(2048)
            return "Content-Type: multipart/" in first_2k or "<html" in first_2k.lower()
    except Exception:
        return False

def extract_html_from_mime(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        msg = email.message_from_file(f)
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                return part.get_payload(decode=True).decode(part.get_content_charset('utf-8'))
    return None

def docx_to_html(docx_path):
    doc = Document(docx_path)
    html = ''
    for para in doc.paragraphs:
        style = para.style.name.lower()
        if style.startswith('heading'):
            # Convert to Markdown heading
            level = ''.join(filter(str.isdigit, style))
            level = int(level) if level else 1
            html += f'<h{level}>{para.text}</h{level}>\n'
        else:
            html += f'<p>{para.text}</p>\n'
    return html

def convert_file(file_path, output_folder):
    filename = os.path.basename(file_path)
    name, _ = os.path.splitext(filename)
    md_filename = name + '.md'
    md_path = os.path.join(output_folder, md_filename)

    # Handle docx
    if is_zipfile(file_path):
        try:
            html = docx_to_html(file_path)
            markdown = md(html)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f'[docx] Converted: {filename} -> {md_filename}')
        except Exception as e:
            print(f'[docx] Error processing {filename}: {e}')
        return

    # Handle HTML MIME (Confluence etc)
    if is_html_mime(file_path):
        html = extract_html_from_mime(file_path)
        if html:
            markdown = md(html)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f'[html-mime] Converted: {filename} -> {md_filename}')
        else:
            print(f'[html-mime] Skipped: {filename} (No HTML found)')
        return

    # Handle legacy .doc (binary, not supported)
    print(f'[legacy-doc] ERROR: {filename} appears to be a legacy Word .doc (binary) file. Skipped!')

def convert_folder(folder_path, output_folder=None):
    if output_folder is None:
        output_folder = folder_path
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.doc', '.docx')):
            file_path = os.path.join(folder_path, filename)
            convert_file(file_path, output_folder)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python docx2md.py <folder_path> [output_folder]")
    else:
        folder = sys.argv[1]
        out_folder = sys.argv[2] if len(sys.argv) > 2 else None
        convert_folder(folder, out_folder)