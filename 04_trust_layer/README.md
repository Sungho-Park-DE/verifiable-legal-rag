# 04 — Trust layer (hallucination detection)

Goal: build the differentiator. In 2025-26 legaltech hackathons,
anti-hallucination architecture became a winning feature in itself
(Hallucin8, Tracy AI, ClauseWise's "deterministic decompilation") — not
hygiene. This project implements the weekend-sized version:
**quote-and-verify** — probabilistic generation, deterministic checking.

The pitch numbers this addresses (current, citable):
* ~1,490 court decisions worldwide involve AI-fabricated material filed
  by lawyers — Charlotin database, May 2026.
* Even commercial legal RAG tools hallucinate: Lexis+ AI >17%, Westlaw
  AI-Assisted Research ~33% — Stanford RegLab, J. Empirical Legal
  Studies 2025 (https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf).

## Run order

Prerequisite: the project-02 index (`02_rag/build_index.py`).

```bash
.venv/bin/python 04_trust_layer/verifier.py     # self-contained demo
.venv/bin/python 04_trust_layer/verify.py       # works WITHOUT an API key
# with a key:
.venv/bin/python 04_trust_layer/cited_answer.py "Is there a cap on damages?"
.venv/bin/python 04_trust_layer/citations_api.py "Which law governs this agreement?"
```

## What to study, in order

1. `verifier.py` — the deterministic core (~60 lines of logic). The one
   idea: an LLM judging "is this supported?" can itself hallucinate; a
   substring match cannot. Understand `normalize` (what differences are
   never evidence-relevant), the fuzzy window (what noise to tolerate),
   and `FUZZY_THRESHOLD` (where verbatim ends and paraphrase begins).
2. `cited_answer.py` — the schema IS the trust mechanism: a required
   `quote` field described as character-for-character forces the model
   to commit to checkable evidence. Note this file is just 02 + 03 + 4a
   composed; there is no new API concept in it.
3. `citations_api.py` — the managed alternative, with the decision
   table for choosing between hand-built and native (key constraint:
   native citations can't combine with structured outputs — 400).
4. `verify.py` — the boundary probes are the interesting part: one typo
   scores 0.98 (passes fuzzy), a paraphrase scores 0.39 (blocked), and
   a real quote pointed at the wrong chunk still fails — citations must
   point at the RIGHT place, not just somewhere.

## Ideas to retain

* Trust layer = split the roles: model proposes (fluent, probabilistic),
  code disposes (boring, deterministic). Judges reward exactly this
  split because it's auditable.
* Failing claims are RENDERED, not dropped — "1/2 claims verified, do
  not trust the rest" demos better than silently hiding a bad claim.
* The threshold is a product decision, not a constant: what score
  separates OCR noise from paraphrase depends on your corpus. Keep the
  boundary tests when you tune it.

## Experiments worth trying

* Lower `FUZZY_THRESHOLD` to 0.35 and watch the paraphrase test fail —
  then argue (to yourself) what the right threshold is for court PDFs
  with OCR noise.
* Add a `page`/`char_offset` field to `Claim` and render clickable
  highlights — that plus Streamlit is the classic winning demo.
* Next level beyond string matching: an NLI/entailment check ("does the
  quote actually SUPPORT the statement, not just exist?") — string
  verification catches fabricated evidence, not misused evidence. A
  cheap version: one extra LLM call per claim with the quote and
  statement, asking only "entails / does not entail", which is itself
  checkable against a small labeled set (LegalBench-RAG has exact-span
  ground truth: https://arxiv.org/pdf/2408.10343).
