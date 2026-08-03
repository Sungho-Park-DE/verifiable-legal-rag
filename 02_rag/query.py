"""Step 2c — retrieval + prompt assembly. This IS the "G" setup in RAG.

Run:  .venv/bin/python 02_rag/query.py "What is the termination notice period?"

Demystification is the goal of this file: "RAG" is nothing more than

    1. embed the question with the SAME model as the chunks,
    2. take the k nearest chunks (cosine distance),
    3. paste them into a prompt with numbered source tags,
    4. instruct the model to answer ONLY from those sources and cite.

No framework needed — this file is ~40 lines of logic. The assembled
prompt is printed in full so you can see there is no magic: what the
LLM receives is exactly what you built here. Project 03 sends prompts
like this one to Claude.
"""

import sys

from build_index import get_collection


def retrieve(question: str, k: int = 3) -> list[dict]:
    col = get_collection()
    res = col.query(query_texts=[question], n_results=k)
    # Chroma returns parallel lists (one per query); zip them into dicts.
    return [
        {"id": i, "text": d, "section": m["section"], "distance": dist}
        for i, d, m, dist in zip(
            res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
        )
    ]


def build_prompt(question: str, hits: list[dict]) -> str:
    """Numbered sources + a grounding instruction.

    The two instruction lines are the minimum viable anti-hallucination
    setup for legal text: forbid outside knowledge, force citations.
    (Project 03 and the Claude citations API push this further.)
    """
    sources = "\n\n".join(f"[{n}] {h['text']}" for n, h in enumerate(hits, start=1))
    return (
        "You are a contract analyst. Answer the question using ONLY the "
        "numbered sources below.\n"
        "Cite the source number like [1] after every claim. If the sources "
        "do not contain the answer, say so instead of guessing.\n\n"
        f"Sources:\n{sources}\n\n"
        f"Question: {question}\n"
    )


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the termination notice period?"

    hits = retrieve(question)
    print(f"question: {question}\n")
    print("--- top matches (smaller distance = closer) ---")
    for n, h in enumerate(hits, start=1):
        print(f"  [{n}] {h['distance']:.4f}  {h['id']}  {h['section']}")

    print("\n--- assembled prompt (what the LLM would receive) ---\n")
    print(build_prompt(question, hits))
