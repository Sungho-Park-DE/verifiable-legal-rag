"""Step 4a — the verifier: prove every quoted span actually exists.

Run:  .venv/bin/python 04_trust_layer/verifier.py   (self-contained demo)

Legal AI's worst failure mode is MISGROUNDING: an answer that sounds
right and cites a real-looking source — but the source doesn't actually
say that. This is not hypothetical: ~1,490 court decisions worldwide
involve AI-fabricated material filed by lawyers (Charlotin database,
May 2026), and even commercial legal RAG tools hallucinate — Lexis+ AI
>17%, Westlaw ~33% (Stanford RegLab, J. Empirical Legal Studies 2025).

The fix that fits in a hackathon weekend:

    1. force the model to QUOTE its evidence verbatim (step 4b),
    2. CHECK each quote against the claimed source with plain string
       code (this file).

The key property: this check is DETERMINISTIC. An LLM judging "is this
claim supported?" can itself hallucinate; a substring match cannot.
That asymmetry — probabilistic generation, deterministic verification —
is the design idea behind the 2025-26 winning "trust layer" projects.
"""

from dataclasses import dataclass
from difflib import SequenceMatcher

# Above this similarity a near-miss still counts as supported. 0.90 keeps
# whitespace/OCR-level noise while rejecting real paraphrases — tune it
# against your own data (verify.py probes both sides of the boundary).
FUZZY_THRESHOLD = 0.90


def normalize(text: str) -> str:
    """Collapse differences that are never meaningful evidence-wise:
    whitespace runs, curly vs straight quotes, unicode dashes. Case is
    KEPT — a verbatim quote should match case."""
    for fancy, plain in (
        ("“", '"'), ("”", '"'),   # curly double quotes
        ("‘", "'"), ("’", "'"),   # curly single quotes
        ("–", "-"), ("—", "-"),   # en/em dashes
    ):
        text = text.replace(fancy, plain)
    return " ".join(text.split())


@dataclass
class Verdict:
    status: str        # supported | supported_fuzzy | quote_not_found | unknown_source
    score: float       # 1.0 for exact; best fuzzy ratio otherwise
    best_match: str    # closest span found — shows WHY a check failed

    @property
    def ok(self) -> bool:
        return self.status in ("supported", "supported_fuzzy")


def _best_window(quote: str, source: str) -> tuple[float, str]:
    """Best fuzzy alignment of `quote` anywhere inside `source`: slide a
    quote-sized window one character at a time and keep the highest
    similarity ratio. The stride must be 1 — a coarser stride makes the
    score depend on WHERE the quote happens to sit in the source, and a
    verdict that changes with alignment is not a verdict. Chunk-sized
    sources keep the O(len(source) x len(quote)) cost trivial; swap in
    rapidfuzz.fuzz.partial_ratio for whole-corpus scale."""
    win = len(quote)
    best_ratio, best = 0.0, ""
    for i in range(0, max(1, len(source) - win + 1)):
        window = source[i : i + win]
        ratio = SequenceMatcher(None, quote, window).ratio()
        if ratio > best_ratio:
            best_ratio, best = ratio, window
    return best_ratio, best


def verify_quote(quote: str, source_id: str, sources: dict[str, str]) -> Verdict:
    """Does `quote` really appear in the source the model claims it's from?

    Note the check is against the CLAIMED source only: a quote that
    exists in a different chunk still fails — a citation has to point
    at the right place, not just somewhere.
    """
    if source_id not in sources:
        return Verdict("unknown_source", 0.0, "")

    q = normalize(quote)
    s = normalize(sources[source_id])

    # Degenerate quotes must fail BEFORE any matching. An empty/whitespace
    # quote would trivially "verify" ('""' is a substring of everything),
    # and a quote LONGER than its source can only be source-plus-padding —
    # the classic stitched fabrication. Both are fabrication shapes, not
    # evidence.
    if not q or len(q) > len(s):
        return Verdict("quote_not_found", 0.0, s[:80])

    if q in s:
        return Verdict("supported", 1.0, q)

    ratio, best = _best_window(q, s)
    if ratio >= FUZZY_THRESHOLD:
        return Verdict("supported_fuzzy", ratio, best)
    return Verdict("quote_not_found", ratio, best)


if __name__ == "__main__":
    sources = {
        "s06": (
            "It renews automatically for successive twelve (12) month "
            "periods unless either party gives written notice of "
            "termination at least thirty (30) days before the end of the "
            "then-current term."
        ),
    }
    cases = [
        ("real quote", "written notice of termination at least thirty (30) days", "s06"),
        ("fabricated quote", "the Provider guarantees 99.9% service uptime", "s06"),
        ("wrong source id", "written notice of termination", "s99"),
    ]
    for label, quote, sid in cases:
        v = verify_quote(quote, sid, sources)
        print(f"{label:>16}: {v.status:<16} score={v.score:.2f}")
