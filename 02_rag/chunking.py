"""Step 2a — heading-aware chunking with overlap.

Run:  .venv/bin/python 02_rag/chunking.py   (demo: chunks the sample contract)

Chunking is THE quality lever of a RAG system — more than the embedding
model, more than the vector DB. Two ideas are implemented here:

1. HEADING-AWARE splitting. A chunk should be a self-contained unit of
   meaning. In a contract, that unit is the clause — and project 01
   recovered clause boundaries as markdown headings. So we split on
   headings first, never in the middle of a clause if we can avoid it.
   (Naive fixed-size chunking can put half of the liability cap in one
   chunk and half in another; neither chunk then matches a query well.)

2. OVERLAP for oversized sections. If a single section exceeds
   max_chars we fall back to a sliding window WITHIN the section, with
   each window repeating the last `overlap` characters of the previous
   one, so a sentence cut at a window edge still appears whole in one
   of the two windows.

Each chunk also carries its section title as METADATA. That pays off
twice in retrieval: the title can be shown as a citation ("source:
clause 6"), and the vector DB can filter on it.
"""

from pathlib import Path

MD = Path(__file__).parent.parent / "data" / "sample_agreement.md"


def _sections(md: str) -> list[tuple[str, str]]:
    """Split markdown into (title, body) pairs on heading lines."""
    sections: list[tuple[str, str]] = []
    title, body_lines = "(preamble)", []
    for line in md.splitlines():
        if line.lstrip().startswith("#"):
            if body_lines:
                sections.append((title, "\n".join(body_lines).strip()))
            # "## **6. Term and termination**" -> "6. Term and termination"
            title = line.strip().lstrip("#").strip().strip("*").strip()
            body_lines = []
        else:
            body_lines.append(line)
    if body_lines:
        sections.append((title, "\n".join(body_lines).strip()))
    return [(t, b) for t, b in sections if b]


def chunk_markdown(md: str, max_chars: int = 1200, overlap: int = 200) -> list[dict]:
    """Return a list of {"id", "section", "text"} dicts ready for indexing.

    The section title is prepended to the chunk text itself ("[6. Term
    and termination] It renews automatically...") — a cheap trick that
    measurably helps retrieval, because the embedding then encodes what
    the passage is ABOUT, not just what it literally says.
    """
    assert overlap < max_chars, "overlap must be smaller than max_chars"

    chunks: list[dict] = []
    for s_idx, (title, body) in enumerate(_sections(md)):
        if len(body) <= max_chars:
            windows = [body]
        else:
            step = max_chars - overlap
            starts = list(range(0, len(body), step))
            # if the second-to-last window already reaches the end of the
            # body, the last start would produce a window fully contained
            # in it — drop the redundant duplicate
            if len(starts) > 1 and starts[-2] + max_chars >= len(body):
                starts.pop()
            windows = [body[i : i + max_chars] for i in starts]
        for w_idx, window in enumerate(windows):
            chunks.append(
                {
                    "id": f"s{s_idx:02d}-c{w_idx:02d}",
                    "section": title,
                    "text": f"[{title}] {window}",
                }
            )
    return chunks


if __name__ == "__main__":
    chunks = chunk_markdown(MD.read_text(encoding="utf-8"))
    print(f"{len(chunks)} chunks\n")
    for c in chunks:
        print(f"  {c['id']}  {len(c['text']):>5} chars  {c['section']}")

    split = sum(1 for c in chunks if not c["id"].endswith("c00"))
    print(f"\nsections split by the sliding window: {split}"
          + (" — every section fits in one chunk with the defaults; "
             "try chunk_markdown(md, max_chars=300) to see the overlap path"
             if split == 0 else ""))
