"""Step 4b — cited answers end-to-end: the full trust-layer pipeline.

Run:  .venv/bin/python 04_trust_layer/cited_answer.py "Is there a cap on damages?"
      (needs ANTHROPIC_API_KEY + the project-02 index; verify.py tests the
      pipeline offline with a scripted fake client)

This file composes everything built so far:

    retrieve (02)  ->  structured output (03): answer + per-claim
    verbatim quotes  ->  deterministic verification (4a)  ->  render
    each claim with a pass/fail badge

The schema IS the trust mechanism: by making `quote` a required field
described as "copied character-for-character", the model must commit to
checkable evidence for every claim — and the verifier makes fabricated
evidence visible instead of persuasive. In a demo, judges see exactly
this: a wrong claim doesn't disappear, it gets a failing badge.
"""

import sys
from pathlib import Path

import anthropic
from pydantic import BaseModel, Field

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "02_rag"))
sys.path.insert(0, str(Path(__file__).parent))

from query import retrieve  # project 02's Chroma retriever
from verifier import Verdict, verify_quote

MODEL = "claude-opus-4-8"


class Claim(BaseModel):
    statement: str = Field(
        description="one factual claim from your answer, in your own words"
    )
    quote: str = Field(
        # min_length is validated client-side by the SDK (the API strips
        # string constraints from the schema); the verifier additionally
        # rejects empty/whitespace quotes — defense in both layers.
        min_length=1,
        description=(
            "the supporting evidence, copied VERBATIM character-for-character "
            "from exactly one source — no paraphrasing, no ellipses, no "
            "stitching together separate sentences"
        ),
    )
    source_id: str = Field(
        description="id of the source the quote comes from, e.g. 's06-c00'"
    )


class CitedAnswer(BaseModel):
    answer: str = Field(description="answer to the question, plain prose")
    claims: list[Claim] = Field(
        description=(
            "one entry per factual claim in the answer. If the sources do "
            "not contain the answer, say so in `answer` and return zero claims."
        )
    )


def build_prompt(question: str, sources: dict[str, str]) -> str:
    listing = "\n\n".join(f"<source id={sid}>\n{text}\n</source>" for sid, text in sources.items())
    return (
        "You are a contract analyst. Answer the question using ONLY the "
        "sources below.\n\n"
        f"{listing}\n\n"
        f"Question: {question}\n"
    )


def answer_with_citations(client, question: str, k: int = 3):
    """Returns (parsed CitedAnswer, [(Claim, Verdict), ...]).
    `client` is injected so verify.py can pass a fake."""
    hits = retrieve(question, k=k)
    sources = {h["id"]: h["text"] for h in hits}

    response = client.messages.parse(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": build_prompt(question, sources)}],
        output_format=CitedAnswer,
    )
    parsed = response.parsed_output

    # The trust layer: every claim's quote gets checked, no exceptions.
    verdicts = [(c, verify_quote(c.quote, c.source_id, sources)) for c in parsed.claims]
    return parsed, verdicts


BADGE = {
    "supported": "[OK]   ",
    "supported_fuzzy": "[~OK]  ",
    "quote_not_found": "[FAIL] ",
    "unknown_source": "[FAIL] ",
}


def render(parsed: CitedAnswer, verdicts: list[tuple[Claim, Verdict]]) -> None:
    print(parsed.answer + "\n")
    for claim, v in verdicts:
        print(f"{BADGE[v.status]}{claim.statement}")
        print(f'        quote:  "{claim.quote}"')
        print(f"        source: {claim.source_id}  ({v.status}, score {v.score:.2f})")
        if not v.ok:
            print(f'        closest span found: "{v.best_match[:80]}"')
    bad = [v for _, v in verdicts if not v.ok]
    print(f"\n{len(verdicts) - len(bad)}/{len(verdicts)} claims verified"
          + (" — DO NOT TRUST the unverified ones" if bad else ""))


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the termination notice period?"
    client = anthropic.Anthropic()

    try:
        parsed, verdicts = answer_with_citations(client, question)
    # no credentials -> TypeError at request time; invalid key -> AuthenticationError
    except (anthropic.AuthenticationError, TypeError) as err:
        if isinstance(err, TypeError) and "authentication" not in str(err).lower():
            raise  # a real bug elsewhere in the pipeline, not missing credentials
        raise SystemExit(
            "No usable API credentials. Set ANTHROPIC_API_KEY and re-run. "
            "verify.py tests this pipeline offline without a key."
        )

    print(f"question: {question}\n")
    render(parsed, verdicts)
