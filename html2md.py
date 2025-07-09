import sys
import os
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def extract_clean_text(tag):
    # Join all strings inside tag (including nested), with a space, and collapse whitespace
    text = " ".join(tag.stripped_strings)
    return " ".join(text.split())

def html_list_to_markdown(tag, indent=0, ordered=False):
    markdown = ""
    for idx, li in enumerate(tag.find_all('li', recursive=False)):
        sublists = li.find_all(['ul', 'ol'], recursive=False)
        # Temporarily remove sublists so they don't pollute the text
        for sublist in sublists:
            sublist.extract()
        line = extract_clean_text(li)
        bullet = f"{' ' * indent}{str(idx + 1) + '.' if ordered else '-'} {line}"
        markdown += f"{bullet}\n"
        # Now add back nested lists (and process them)
        for sublist in sublists:
            markdown += html_list_to_markdown(
                sublist,
                indent=indent + 2,
                ordered=(sublist.name == "ol")
            )
    return markdown

def convert_html_to_markdown(file_path):
    try:
        with open(file_path, encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        logging.error(f"Failed to read file: {e}")
        return

    soup = BeautifulSoup(html, 'html.parser')
    lists = soup.find_all(['ul', 'ol'])
    if not lists:
        logging.info("No lists found in HTML.")
        return

    output_md = ""
    for tag in lists:
        is_ordered = tag.name == "ol"
        output_md += html_list_to_markdown(tag, indent=0, ordered=is_ordered)
        break  # Remove this if you want to process all lists

    out_file = os.path.splitext(file_path)[0] + '.md'
    try:
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(output_md)
        logging.info(f"Markdown written to {out_file}")
    except Exception as e:
        logging.error(f"Failed to write Markdown file: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: python html2md.py inputfile.html")
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        logging.error(f"File does not exist: {file_path}")
        sys.exit(1)
    convert_html_to_markdown(file_path)
