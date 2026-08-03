"""Step 4c — the managed alternative: Claude's native Citations API.

Run:  .venv/bin/python 04_trust_layer/citations_api.py "What law governs the agreement?"
      (live only — needs ANTHROPIC_API_KEY)

Step 4b built citation grounding BY HAND: schema forces quotes, our code
verifies them. Claude also has this built in — pass the document as a
`document` content block with `citations: {enabled: true}` and the
response comes back as text blocks that each carry a `citations` list
with `cited_text` and exact char offsets into your document. The
API-side grounding means you don't write the quote-extraction prompt or
the span bookkeeping yourself.

When to use which (both are current, mid-2026):

  hand-built quote-and-verify (4b)     native citations API (this file)
  ---------------------------------    --------------------------------
  works with structured outputs        NOT combinable with structured
  (one pipeline: extraction +          outputs (output_config.format +
  grounding in a single schema)        citations returns a 400)
  works with ANY model/provider        Claude-specific
  verification is your code —          spans are API-guaranteed to be
  you can show/pitch the check         from the document
  chunk-level sources (from RAG)       whole documents (no chunking
                                       needed — 1M context helps here)

At a hackathon: 4b when your pipeline is schema-first or multi-provider;
this API when you want clickable page/char-anchored citations over full
documents with zero verification code.
"""

import sys
from pathlib import Path

import anthropic

MD = Path(__file__).parent.parent / "data" / "sample_agreement.md"
MODEL = "claude-opus-4-8"


def ask_with_citations(client, question: str, document_text: str):
    return client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "text",
                            "media_type": "text/plain",
                            "data": document_text,
                        },
                        "title": "Service Agreement",
                        "citations": {"enabled": True},
                    },
                    {"type": "text", "text": question},
                ],
            }
        ],
    )


def render(response, document_text: str) -> None:
    """The response is SPLIT into text blocks; cited blocks carry a
    `citations` list. For plain-text documents each citation has
    `cited_text` plus char offsets (`start_char_index`/`end_char_index`);
    for PDFs you get page numbers (`page_location`) instead."""
    n = 0
    footnotes = []
    for block in response.content:
        if block.type != "text":
            continue
        cites = getattr(block, "citations", None) or []
        marker = ""
        for c in cites:
            n += 1
            marker += f"[{n}]"
            footnotes.append((n, c))
        print(block.text + marker, end="")
    print("\n")
    for i, c in footnotes:
        located = document_text[c.start_char_index : c.end_char_index]
        # sanity check our own offsets against cited_text
        agrees = c.cited_text.strip() == located.strip()
        print(f'[{i}] chars {c.start_char_index}-{c.end_char_index}: "{c.cited_text.strip()[:90]}"'
              + ("" if agrees else "  (!) offset mismatch"))


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the termination notice period?"
    document_text = MD.read_text(encoding="utf-8")
    client = anthropic.Anthropic()

    try:
        response = ask_with_citations(client, question, document_text)
    except (anthropic.AuthenticationError, TypeError):
        raise SystemExit(
            "No usable API credentials — this demo is live-only. Set "
            "ANTHROPIC_API_KEY and re-run. (The hand-built pipeline in "
            "cited_answer.py has offline verification instead.)"
        )

    print(f"question: {question}\n")
    render(response, document_text)
