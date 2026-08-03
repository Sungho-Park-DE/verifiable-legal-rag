# 01 — PDF parsing

Goal: understand why "PDF -> structured markdown" (not "PDF -> plain
text") is the standard first step of a legaltech pipeline.

## Run order

```bash
.venv/bin/python data/make_sample_pdf.py        # once, creates the sample contract
.venv/bin/python 01_pdf_parsing/extract_text.py       # 1a: the naive baseline
.venv/bin/python 01_pdf_parsing/extract_markdown.py   # 1b: the real approach
.venv/bin/python 01_pdf_parsing/verify.py             # checks both outputs
```

## What to study, in order

1. `extract_text.py` — plain PyMuPDF. Open `out_plain.txt` next to the
   PDF and see what structure was lost (headings, table).
2. `extract_markdown.py` — pymupdf4llm. Open
   `data/sample_agreement.md` and compare: headings are `##` lines, the
   fee schedule is a pipe table.
3. `verify.py` — the assertions ARE the lesson: content survives in
   both, structure survives only in markdown.

## The one idea to retain

RAG quality is decided at chunking time, and you cannot chunk on
structure you no longer have. Headings recovered here become chunk
boundaries in project 02.

## Escalation path (when this tool is not enough)

| Input | Tool |
|---|---|
| digital-born PDF, simple layout | pymupdf4llm (this project) |
| complex tables / multi-column | Docling (IBM, runs layout models) |
| scans / photos (no text layer) | vision-LLM OCR API (e.g. Mistral OCR) |
