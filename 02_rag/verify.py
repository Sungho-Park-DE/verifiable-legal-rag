"""Verification for project 02.

Run:  .venv/bin/python 02_rag/verify.py

Rebuilds the index, then checks that retrieval actually finds the right
clause for three differently-phrased questions — including one that
shares almost no words with the clause text (the case where embeddings
must beat keyword search). Exits non-zero on failure.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import build_index
from chunking import MD, chunk_markdown
from query import build_prompt, retrieve

failures = 0


def check(name: str, ok: bool) -> None:
    global failures
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        failures += 1


def main() -> None:
    # --- chunking ---
    chunks = chunk_markdown(MD.read_text(encoding="utf-8"))
    check("chunking produced >= 8 chunks (one per clause)", len(chunks) >= 8)
    check("no chunk exceeds max_chars + title prefix slack",
          all(len(c["text"]) <= 1300 for c in chunks))
    check("every chunk carries a section title",
          all(c["section"] for c in chunks))
    check("termination clause text survived chunking intact",
          any("thirty (30) days" in c["text"] for c in chunks))

    # --- indexing ---
    build_index.main()
    check("index contains all chunks",
          build_index.get_collection().count() == len(chunks))

    # --- retrieval: (question, expected substring in top-k) ---
    cases = [
        ("What is the termination notice period?", "thirty (30) days"),
        ("Is there a cap on damages?", "EUR 100,000"),
        # paraphrase test: no shared keywords with clause 10
        # ("Governing law and jurisdiction" / "Munich")
        ("Where would we have to sue them?", "Munich"),
    ]
    for question, expected in cases:
        hits = retrieve(question, k=3)
        joined = " ".join(h["text"] for h in hits)
        check(f"top-3 for {question!r} contains {expected!r}", expected in joined)

    # --- prompt assembly ---
    hits = retrieve(cases[0][0], k=3)
    prompt = build_prompt(cases[0][0], hits)
    check("prompt has numbered sources", "[1]" in prompt and "[3]" in prompt)
    check("prompt contains the question", cases[0][0] in prompt)
    check("prompt contains grounding instruction", "ONLY" in prompt)

    print()
    if failures:
        print(f"{failures} check(s) failed")
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
