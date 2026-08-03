# 02 — RAG from scratch (no framework)

Goal: see that "RAG" is ~120 lines of plain Python — chunk, embed,
retrieve, assemble a prompt. No LangChain, no API key: Chroma's built-in
local embedding model (all-MiniLM-L6-v2, downloaded once to
`~/.cache/chroma/`) does the embedding.

## Run order

```bash
.venv/bin/python 02_rag/chunking.py      # 2a: see the chunks + sizes
.venv/bin/python 02_rag/build_index.py   # 2b: embed + store in chroma_db/
.venv/bin/python 02_rag/query.py "Is there a cap on damages?"   # 2c
.venv/bin/python 02_rag/verify.py        # rebuilds index + retrieval checks
```

## What to study, in order

1. `chunking.py` — the quality lever. Why heading-aware, why overlap,
   why the section title is prepended to each chunk's text.
2. `build_index.py` — 20 lines. Note `upsert` (idempotent re-runs) and
   where you would swap in an API embedding model (one argument).
3. `query.py` — retrieval + prompt assembly. Run it with your own
   questions and READ THE PRINTED PROMPT: that exact string is all the
   LLM will ever see. There is no other magic in RAG.
4. `verify.py` — note the paraphrase test: "Where would we have to sue
   them?" shares no keywords with clause 10 ("Governing law and
   jurisdiction ... Munich") but retrieval still finds it. That is the
   embedding earning its keep over keyword search.

## Ideas to retain

* Chunk = unit of meaning (here: one clause), not a fixed byte count.
* The grounding instruction in `build_prompt` ("answer ONLY from the
  sources, cite [n], say so if absent") is the minimum viable
  anti-hallucination setup for legal text.
* Everything here scales unchanged: swap the sample contract for 10,000
  court decisions and the code stays the same shape.

## Experiments worth trying

* Break it: set `max_chars=300, overlap=0` in `chunking.py`, rebuild,
  re-run `verify.py` and watch which retrieval checks start failing.
* Ask a question whose answer is NOT in the contract and look at the
  distances in `query.py` — how would you threshold "don't answer"?
