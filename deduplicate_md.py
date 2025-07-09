import re
import sys
from collections import defaultdict

def extract_sections(md):
    # Splits the doc by headings (any level) and keeps headings with their content
    pattern = r"(#{1,6} .*)"
    parts = re.split(pattern, md)
    sections = []
    if not parts[0].strip():
        parts = parts[1:]  # skip possible pre-heading junk
    for i in range(0, len(parts), 2):
        if i+1 < len(parts):
            heading, content = parts[i], parts[i+1]
            sections.append((heading.strip(), content.strip()))
    return sections

def sections_to_str(sections):
    return ''.join([f"{h}\n{c}\n\n" for h, c in sections])

def normalize(text):
    return re.sub(r'\s+', ' ', text.strip().lower())

def main(infile, outfile):
    with open(infile, "r", encoding="utf-8") as f:
        md = f.read()

    sections = extract_sections(md)

    # Identify duplicate sections (by normalized heading+content)
    section_dict = defaultdict(list)
    for idx, (heading, content) in enumerate(sections):
        key = normalize(heading + "\n" + content)
        section_dict[key].append(idx)

    # Find keys with duplicates
    dup_keys = [k for k, idxs in section_dict.items() if len(idxs) > 1]

    appendix = []
    appendix_refs = {}
    cleaned_sections = sections.copy()

    for i, key in enumerate(dup_keys, start=1):
        idxs = section_dict[key]
        heading, content = sections[idxs[0]]
        appendix_id = f"appendix-{i}"
        appendix.append((f"#### {heading[2:].strip()} (Moved to Appendix)", content))
        ref = f"[See Appendix §{i}](#appendix-{i})"
        appendix_refs[key] = ref

        # Replace all but the first occurrence with a reference
        for j in idxs[1:]:
            cleaned_sections[j] = (heading, ref)
        # Tag the appendix section for anchor
        appendix[-1] = (f'<a name="{appendix_id}"></a>\n' + appendix[-1][0], appendix[-1][1])

    # Reconstruct the cleaned doc
    doc = sections_to_str(cleaned_sections)
    if appendix:
        doc += "\n---\n## Appendix\n\n"
        doc += sections_to_str(appendix)

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(doc)

    print(f"Deduplicated file written to: {outfile}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python deduplicate_sections.py input.md output.md")
    else:
        main(sys.argv[1], sys.argv[2])
