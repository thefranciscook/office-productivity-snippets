import sys
import os
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def remove_inline_svgs(soup):
    try:
        for svg in soup.find_all('svg'):
            svg.decompose()
        logging.info("Removed inline SVG elements.")
    except Exception as e:
        logging.error(f"Failed to remove inline SVGs: {e}")

def remove_classnames(soup):
    try:
        for tag in soup.find_all(attrs={"class": True}):
            del tag['class']
        logging.info("Removed all class names.")
    except Exception as e:
        logging.error(f"Failed to remove class names: {e}")

def remove_ids(soup):
    try:
        for tag in soup.find_all(attrs={"id": True}):
            del tag['id']
        logging.info("Removed all ids.")
    except Exception as e:
        logging.error(f"Failed to remove ids: {e}")

def remove_data_tags(soup):
    try:
        for tag in soup.find_all(True):
            attrs_to_remove = [attr for attr in tag.attrs if attr.startswith('data-')]
            for attr in attrs_to_remove:
                del tag[attr]
        logging.info("Removed all data-* attributes.")
    except Exception as e:
        logging.error(f"Failed to remove data-* attributes: {e}")

def remove_aria_tags(soup):
    try:
        for tag in soup.find_all(True):
            attrs_to_remove = [attr for attr in tag.attrs if attr.startswith('aria-')]
            for attr in attrs_to_remove:
                del tag[attr]
        logging.info("Removed all aria-* attributes.")
    except Exception as e:
        logging.error(f"Failed to remove aria-* attributes: {e}")

def remove_style_tags(soup):
    try:
        for tag in soup.find_all(attrs={"style": True}):
            del tag['style']
        logging.info("Removed all style attributes.")
    except Exception as e:
        logging.error(f"Failed to remove style attributes: {e}")

def unwrap_spans(soup):
    try:
        for span in soup.find_all('span'):
            span.unwrap()
        logging.info("Unwrapped all <span> tags, keeping their content.")
    except Exception as e:
        logging.error(f"Failed to unwrap <span> tags: {e}")

def main():
    if len(sys.argv) < 2:
        logging.error("Usage: python clean_html.py inputfile.html")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        logging.error(f"File does not exist: {file_path}")
        sys.exit(1)

    with open(file_path, encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Order doesn't matter, but unwrapping spans usually comes last
    remove_inline_svgs(soup)
    remove_classnames(soup)
    remove_ids(soup)
    remove_data_tags(soup)
    remove_aria_tags(soup)
    remove_style_tags(soup)
    unwrap_spans(soup)

    cleaned_html = str(soup)

    out_file = file_path.replace('.html', '_cleaned.html')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_html)

    logging.info(f"Cleaned HTML written to {out_file}")

if __name__ == '__main__':
    main()
