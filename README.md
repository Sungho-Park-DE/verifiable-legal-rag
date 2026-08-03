# Verifiable legal RAG

An end-to-end legal-document analysis pipeline with a deterministic
trust layer: every claim the LLM makes must carry a verbatim quote that
plain code verifies against the claimed source — so a fabricated claim
gets a failing badge instead of a persuasive paragraph. Built
framework-free (no LangChain) to keep every moving part inspectable.

**Why it exists:** legal AI's core failure mode is misgrounding — even
commercial legal RAG tools hallucinate in 17–33% of answers (Stanford
RegLab, [J. Empirical Legal Studies 2025](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf)),
and ~1,490 court decisions worldwide involve AI-fabricated material
filed by lawyers (Charlotin database, 2026). The answer implemented
here: the model proposes, deterministic code disposes.

**Stack:** Python · Anthropic SDK (structured outputs, tool use) ·
ChromaDB (local embeddings) · pymupdf4llm · Pydantic

Four heavily-commented projects, each building on the previous one's
output:

```
01  PDF -> structured markdown        (pymupdf4llm)
02  markdown -> chunks -> vector DB   (Chroma, local embeddings, no API key)
03  LLM: structured outputs + agent   (Anthropic SDK; 02's retriever as a tool)
04  trust layer                       (quote-and-verify + native Citations API)
```

## Quickstart from a fresh clone

Generated artifacts (sample PDF/markdown, vector index) are gitignored —
the scripts reproduce everything:

```bash
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python data/make_sample_pdf.py              # sample contract PDF
.venv/bin/python 01_pdf_parsing/extract_text.py       # baseline extraction
.venv/bin/python 01_pdf_parsing/extract_markdown.py   # structured markdown
.venv/bin/python 02_rag/build_index.py                # embed + index (downloads a local model once)
.venv/bin/python 01_pdf_parsing/verify.py \
  && .venv/bin/python 02_rag/verify.py \
  && .venv/bin/python 03_llm_structured/verify.py \
  && .venv/bin/python 04_trust_layer/verify.py        # 50+ checks, no API key needed
```

Projects 03/04 additionally run live checks when `ANTHROPIC_API_KEY`
is set; without it, scripted fake clients cover the loop and pipeline
mechanics offline.

## How it was verified

Every project ships a `verify.py` whose assertions document what the
stage guarantees — including adversarial cases found by a fresh-context
code review: an empty quote that would trivially pass a naive substring
check (`"" in s` is always `True`), a stitched quote (whole chunk +
invented sentence) that diluted fuzzy matching past the threshold, and
paraphrases probing both sides of the similarity boundary. The review
findings and their fixes are preserved as test cases in
`04_trust_layer/verify.py`.

## Study path

Work through the projects in order; each folder's README has a "what to
study, in order" list and experiments. Verify scripts double as living
documentation — their assertions state exactly what each stage guarantees.

| Project | Run | Needs API key |
|---|---|---|
| 01 PDF parsing | `.venv/bin/python 01_pdf_parsing/verify.py` | no |
| 02 RAG | `.venv/bin/python 02_rag/verify.py` | no (local embedding model) |
| 03 LLM | `.venv/bin/python 03_llm_structured/verify.py` | offline checks: no · live: yes |
| 04 trust layer | `.venv/bin/python 04_trust_layer/verify.py` | offline checks: no · live: yes |

## The end-to-end pipeline in one sentence

A contract PDF is parsed into markdown whose headings mark clause
boundaries (01); clauses are chunked, embedded, and indexed so a
paraphrased question finds the right clause (02); the model extracts a
validated risk analysis from the document and answers questions through
a search tool it decides when to call, citing sections (03); and every
claim the model makes must carry a verbatim quote that deterministic
code verifies against the claimed source, so a fabricated claim gets a
failing badge instead of a persuasive paragraph (04).

## What is deliberately NOT here (and why)

* **LangChain / LlamaIndex** — the 2026 consensus for simple RAG is
  provider SDK + vector DB directly; frameworks add debugging layers a
  24-48h hackathon can't afford. LlamaIndex remains useful specifically
  for messy multi-format document ingestion.
* **Demo UI** — Streamlit/Gradio wrap around projects 03/04's functions
  in ~20 lines; that layer is best learned by building the actual demo.
  (`04_trust_layer/cited_answer.py`'s render() output is exactly what
  the UI would show as pass/fail citation badges.)

## Swapping in real data

Drop any contract PDF into `data/` and point `01_pdf_parsing` scripts at
it. For realistic material use CUAD (510 real commercial contracts with
41 labeled clause types): https://arxiv.org/pdf/2103.06268 — its category
taxonomy also makes a good replacement for the `Clause.category` enum in
`03_llm_structured/structured_extract.py`.
