"""Verification for project 04.

Run:  .venv/bin/python 04_trust_layer/verify.py

Layers:
  1. OFFLINE verifier unit checks — the deterministic core, probed on
     both sides of every boundary (exact / normalized / fuzzy / miss /
     wrong-place / unknown source).
  2. OFFLINE end-to-end — the full pipeline with a scripted fake LLM
     that returns one honest claim and one FABRICATED claim; the trust
     layer must flag exactly the fabricated one. Retrieval is real
     (project-02 index).
  3. LIVE (only with ANTHROPIC_API_KEY) — real cited answer, all claims
     must verify; native Citations API returns offset-accurate spans.
"""

import os
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(ROOT / "02_rag"))

from chunking import MD, chunk_markdown
from cited_answer import Claim, CitedAnswer, answer_with_citations
from verifier import FUZZY_THRESHOLD, normalize, verify_quote

failures = 0


def check(name: str, ok: bool) -> None:
    global failures
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        failures += 1


# --- offline 1: verifier unit checks ---------------------------------------

REAL_QUOTE = "written notice of termination at least thirty (30) days"


def offline_verifier_checks() -> None:
    chunks = chunk_markdown(MD.read_text(encoding="utf-8"))
    sources = {c["id"]: c["text"] for c in chunks}
    term_id = next((c["id"] for c in chunks if REAL_QUOTE in c["text"]), None)
    other_id = next((c["id"] for c in chunks if REAL_QUOTE not in c["text"]), None)
    curly_id = next((c["id"] for c in chunks if "the 'Agreement'" in c["text"]), None)
    if not (term_id and other_id and curly_id):
        check("sample contract still contains the test anchors", False)
        return

    check("verbatim quote -> supported",
          verify_quote(REAL_QUOTE, term_id, sources).status == "supported")

    fabricated = "the Provider guarantees 99.9% service uptime"
    check("fabricated quote -> quote_not_found",
          verify_quote(fabricated, term_id, sources).status == "quote_not_found")

    # normalization: doubled whitespace and curly quotes still count as
    # verbatim (the source uses straight quotes; the model might emit curly)
    styled = "written  notice of termination at least thirty (30) days"
    check("whitespace-mangled quote -> supported (normalization)",
          verify_quote(styled, term_id, sources).status == "supported")
    curly = "This Service Agreement (the ‘Agreement’) is entered into"
    check("curly-quote variant -> supported (normalization)",
          verify_quote(curly, curly_id, sources).status == "supported")

    # adversarial: fabrication shapes that would trivially pass a naive
    # substring check must fail
    check("empty quote -> quote_not_found (not trivially supported)",
          verify_quote("", term_id, sources).status == "quote_not_found")
    check("whitespace-only quote -> quote_not_found",
          verify_quote("  \n\t ", term_id, sources).status == "quote_not_found")
    stitched = sources[term_id] + " The Provider guarantees 99.9% uptime."
    check("whole-chunk + invented sentence (stitched) -> quote_not_found",
          verify_quote(stitched, term_id, sources).status == "quote_not_found")

    # fuzzy boundary, near side: one typo in a 50+ char quote
    typo = REAL_QUOTE.replace("notice", "notise")
    v = verify_quote(typo, term_id, sources)
    check(f"one-typo quote -> supported_fuzzy (score {v.score:.2f} >= {FUZZY_THRESHOLD})",
          v.status == "supported_fuzzy")

    # fuzzy boundary, far side: a paraphrase must NOT pass
    paraphrase = "either side may cancel with one month's warning before renewal"
    v = verify_quote(paraphrase, term_id, sources)
    check(f"paraphrase -> quote_not_found (score {v.score:.2f} < {FUZZY_THRESHOLD})",
          v.status == "quote_not_found")

    # a real quote pointed at the WRONG chunk must fail: citations have to
    # point at the right place, not just somewhere
    check("real quote, wrong source -> quote_not_found",
          verify_quote(REAL_QUOTE, other_id, sources).status == "quote_not_found")

    check("nonexistent source id -> unknown_source",
          verify_quote(REAL_QUOTE, "s99-c99", sources).status == "unknown_source")


# --- offline 2: end-to-end with a scripted fake LLM -------------------------


class FakeClient:
    """Mimics anthropic.Anthropic() for messages.parse(): pops scripted
    responses, records request kwargs. self.messages = self makes
    client.messages.parse(...) resolve here."""

    def __init__(self, scripted):
        self._scripted = list(scripted)
        self.calls = []
        self.messages = self

    def parse(self, **kwargs):
        self.calls.append(kwargs)
        return self._scripted.pop(0)


def offline_pipeline_checks() -> None:
    import build_index

    if build_index.get_collection().count() == 0:
        print("project-02 index is empty — run 02_rag/build_index.py first")
        check("project-02 index exists (retrieval is real in this test)", False)
        return

    from query import retrieve

    question = "What is the termination notice period?"
    hits = retrieve(question, k=3)
    term_hit = next((h for h in hits if REAL_QUOTE in h["text"]), None)
    if term_hit is None:
        check("retrieval still surfaces the termination clause", False)
        return

    scripted_answer = CitedAnswer(
        answer="Notice must be given 30 days before the end of the term. "
               "The provider also guarantees 99.9% uptime.",
        claims=[
            Claim(
                statement="30 days written notice is required",
                quote=REAL_QUOTE,
                source_id=term_hit["id"],
            ),
            Claim(  # the hallucination: fluent, plausible, and false
                statement="The provider guarantees 99.9% uptime",
                quote="the Provider guarantees an uptime of 99.9%",
                source_id=term_hit["id"],
            ),
        ],
    )
    fake = FakeClient([SimpleNamespace(parsed_output=scripted_answer)])

    parsed, verdicts = answer_with_citations(fake, question)

    check("pipeline sent tagged sources to the model",
          "<source id=" in fake.calls[0]["messages"][0]["content"])
    check("pipeline requested the CitedAnswer schema",
          fake.calls[0]["output_format"] is CitedAnswer)
    check("honest claim verified", verdicts[0][1].ok)
    check("fabricated claim flagged", verdicts[1][1].status == "quote_not_found")
    check("exactly one of two claims failed",
          sum(1 for _, v in verdicts if not v.ok) == 1)


# --- live (needs credentials) ------------------------------------------------


def live_checks() -> None:
    import anthropic

    from citations_api import ask_with_citations

    client = anthropic.Anthropic()
    document_text = MD.read_text(encoding="utf-8")

    parsed, verdicts = answer_with_citations(
        client, "What is the termination notice period?"
    )
    check("LIVE: answer has >= 1 claim", len(verdicts) >= 1)
    check("LIVE: every claim's quote verified against its source",
          all(v.ok for _, v in verdicts))
    check("LIVE: answer mentions 30 days",
          "30" in parsed.answer or "thirty" in parsed.answer.lower())

    response = ask_with_citations(client, "Which law governs this agreement?", document_text)
    citations = [
        c
        for block in response.content
        if block.type == "text"
        for c in (getattr(block, "citations", None) or [])
    ]
    check("LIVE: native citations returned", len(citations) >= 1)
    check("LIVE: every cited_text really occurs in the document",
          all(normalize(c.cited_text) in normalize(document_text) for c in citations))


def main() -> None:
    print("--- offline: verifier unit checks ---")
    offline_verifier_checks()
    print("\n--- offline: end-to-end (scripted LLM, real retrieval) ---")
    offline_pipeline_checks()

    if os.environ.get("ANTHROPIC_API_KEY"):
        print("\n--- live: real API calls ---")
        live_checks()
    else:
        print("\n(no ANTHROPIC_API_KEY — live checks skipped; the verifier and "
              "pipeline mechanics are fully covered offline. Other auth methods "
              "also skip: export ANTHROPIC_API_KEY to opt in to live checks.)")

    print()
    if failures:
        print(f"{failures} check(s) failed")
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
