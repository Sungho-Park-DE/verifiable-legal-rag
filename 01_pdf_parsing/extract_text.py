"""Step 1a — the BASELINE: plain text extraction with PyMuPDF.

Run:  .venv/bin/python 01_pdf_parsing/extract_text.py

This is the naive approach: one string per page, no structure. Read the
output and notice what is LOST compared to the original PDF:

  * headings look identical to body text (no way to tell "6. Term and
    termination" is a section boundary),
  * the fee table collapses into a soup of cell values,
  * paragraphs are broken at line-wrap positions, not at meaning.

That matters downstream: RAG quality is decided at chunking time, and
you cannot chunk on structure you no longer have. Project 02 will chunk
on markdown headings — which is why extract_markdown.py exists.
"""

from pathlib import Path

import pymupdf  # this is PyMuPDF; the import name changed from `fitz` in 2024 (PyMuPDF 1.24)

PDF = Path(__file__).parent.parent / "data" / "sample_agreement.pdf"
OUT = Path(__file__).parent / "out_plain.txt"


def main() -> None:
    doc = pymupdf.open(PDF)

    pages = []
    for page in doc:
        # get_text() with no arguments returns the page's plain text in
        # reading order. Fast (no ML), but layout-blind.
        pages.append(page.get_text())

    text = "\n".join(pages)
    OUT.write_text(text, encoding="utf-8")

    print(f"pages: {doc.page_count}")
    print(f"chars: {len(text)}")
    print(f"wrote: {OUT}")
    print("\n--- first 400 chars ---")
    print(text[:400])


if __name__ == "__main__":
    main()
