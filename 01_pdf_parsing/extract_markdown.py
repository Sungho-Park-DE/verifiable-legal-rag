"""Step 1b — the HACKATHON DEFAULT: structured markdown with pymupdf4llm.

Run:  .venv/bin/python 01_pdf_parsing/extract_markdown.py

pymupdf4llm sits on top of PyMuPDF and reconstructs document STRUCTURE:

  * font-size heuristics turn section titles into markdown headings
    ("## **6. Term and termination**"),
  * tables are detected and emitted as markdown pipe tables,
  * bold/italic survive as **bold** / *italic*.

The markdown file this writes is the INPUT for project 02: its headings
are what the chunker splits on. This "PDF -> markdown -> chunk on
headings" pipeline is the standard first hour of a legaltech hackathon.

When this tool is NOT enough (know the escalation path):
  * scanned/photographed PDFs have no text layer at all -> you need OCR
    (a vision-LLM OCR API, e.g. Mistral OCR),
  * heavy multi-column layouts or complex tables -> Docling (IBM), which
    runs real layout-detection models and is slower but more faithful.
"""

from pathlib import Path

import pymupdf4llm

PDF = Path(__file__).parent.parent / "data" / "sample_agreement.pdf"
OUT = Path(__file__).parent.parent / "data" / "sample_agreement.md"


def main() -> None:
    # One call does everything: layout analysis, heading detection,
    # table extraction. Returns a single markdown string.
    md = pymupdf4llm.to_markdown(PDF)

    OUT.write_text(md, encoding="utf-8")

    headings = [line for line in md.splitlines() if line.startswith("#")]
    table_rows = [line for line in md.splitlines() if line.startswith("|")]

    print(f"chars:      {len(md)}")
    print(f"headings:   {len(headings)}")
    print(f"table rows: {len(table_rows)}")
    print(f"wrote:      {OUT}")
    print("\n--- detected headings ---")
    for h in headings:
        print(f"  {h}")


if __name__ == "__main__":
    main()
