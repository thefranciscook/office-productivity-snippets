"""
Combine all Markdown files in a folder into a single Markdown file.

Output format:

----------
filename.md
----------
<contents of filename.md>

----------
nextfile.md
----------
<contents of nextfile.md>
"""

from pathlib import Path
import argparse
import sys

SEPARATOR = "----------"

def combine_md(source_dir: Path, output_path: Path, ext: str = ".md") -> None:
    md_files = sorted(
        [p for p in source_dir.iterdir() if p.suffix == ext and p != output_path]
    )

    if not md_files:
        sys.exit(f"No '{ext}' files found in {source_dir}")

    with output_path.open("w", encoding="utf-8") as out_file:
        for i, md in enumerate(md_files, 1):
            header = f"{SEPARATOR}\n{md.name}\n{SEPARATOR}\n"
            out_file.write(header)
            out_file.write(md.read_text(encoding="utf-8"))

            # Add a blank line between files (even after the last one)
            out_file.write("\n\n")

            print(f"[{i}/{len(md_files)}] Added {md.name}")

    print(f"\n✅ Combined {len(md_files)} files into {output_path}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Combine Markdown files.")
    parser.add_argument(
        "folder",
        type=Path,
        help="Folder containing Markdown files to combine",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("combined.md"),
        help="Name (or path) of the combined output file",
    )
    parser.add_argument(
        "--ext",
        default=".md",
        help="File extension to include (default: .md)",
    )

    args = parser.parse_args()
    combine_md(args.folder, args.output, args.ext)

if __name__ == "__main__":
    main()
