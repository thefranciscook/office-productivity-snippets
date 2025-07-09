#!/usr/bin/env python3
"""combine_by_toc.py — merge Markdown files according to a bullet‑list ToC.

Features
--------
1. **Fuzzy / normalised matching** so minor punctuation or spacing
   differences between ToC titles and filenames don't break the match.
2. **Includes all 'orphan' files** (those not referenced in the ToC)
   under an "Unreferenced files" section at the end.
3. **Skips blank headings** – it only writes a section header if the
   corresponding file is found.

Usage
-----
python3 combine_by_toc.py toc.md ./notes_folder -o combined.md

Requirements: Python ⩾ 3.8 (standard library only).
"""

from pathlib import Path
from urllib.parse import unquote_plus
import argparse
import re
import sys
import unicodedata

# ---------- configuration ----------
EXT = ".md"         # default file extension to look for
SEP = "----------"  # dashed separator used for "orphans" section
# -----------------------------------

TOC_PATTERN = re.compile(r"^(\s*)[-•]\s*(.*?)\s+More actions", re.IGNORECASE)

def normalise(text: str) -> str:
    """Lower‑case, strip punctuation, collapse whitespace."""
    text = unicodedata.normalize("NFKD", text)
    text = text.lower()
    text = re.sub(r"[|:()\-.,]+", " ", text)   # drop or replace punctuation
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_toc(toc_path: Path):
    """Return a list of (depth, title) tuples from a bullet‑list ToC."""
    items = []
    for line in toc_path.read_text(encoding="utf-8").splitlines():
        m = TOC_PATTERN.match(line)
        if not m:
            continue
        indent, title = m.groups()
        depth = len(indent) // 2
        items.append((depth, title.strip()))
    return items


def build_file_lookup(folder: Path, ext: str = EXT):
    """Map *decoded* filenames → Path objects (case‑insensitive)."""
    lookup = {}
    for p in folder.iterdir():
        if p.suffix.lower() != ext:
            continue
        decoded = unquote_plus(p.stem) + p.suffix  # keep .md suffix
        lookup[decoded.lower()] = p
    return lookup


def find_best_match(title: str, lookup: dict):
    """Return Path whose normalised key matches the normalised title, else None."""
    key_norm = normalise(f"{title}{EXT}")
    for fname, path in lookup.items():
        if normalise(fname) == key_norm:
            return path
    return None


def merge_by_toc(toc_items, folder: Path, lookup: dict, out_path: Path):
    used_paths = set()

    with out_path.open("w", encoding="utf-8") as out:
        for depth, title in toc_items:
            path = find_best_match(title, lookup)
            if not path:
                # Skip writing header if we have nothing to insert
                continue

            used_paths.add(path)
            heading = "#" * min(depth + 1, 6)
            out.write(f"{heading} {title}\n\n")
            out.write(path.read_text(encoding="utf-8").rstrip())
            out.write("\n\n")

        # --- append orphan files ---
        orphan_paths = sorted(
            [p for p in folder.iterdir() if p.suffix.lower() == EXT and p not in used_paths and p != out_path]
        )
        if orphan_paths:
            out.write("# Unreferenced files\n\n")
            for p in orphan_paths:
                out.write(f"{SEP}\n{p.name}\n{SEP}\n\n")
                out.write(p.read_text(encoding="utf-8").rstrip())
                out.write("\n\n")

    print(f"✅ Combined {len(used_paths) + len(orphan_paths)} files → {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Combine Markdown files using a bullet‑list ToC.")
    parser.add_argument("toc", type=Path, help="Path to the ToC markdown/text file")
    parser.add_argument("folder", type=Path, help="Folder containing the Markdown files")
    parser.add_argument("-o", "--output", type=Path, default=Path("combined.md"), help="Output file name")
    args = parser.parse_args()

    toc_items = parse_toc(args.toc)
    if not toc_items:
        sys.exit("❌ No valid ToC items parsed – check your file.")

    file_lookup = build_file_lookup(args.folder)
    merge_by_toc(toc_items, args.folder, file_lookup, args.output)


if __name__ == "__main__":
    main()
