"""Step 2b — embed the chunks and store them in a local vector DB.

Run:  .venv/bin/python 02_rag/build_index.py

Chroma is the hackathon default vector DB: pip install, no server, and
it ships a DEFAULT EMBEDDING FUNCTION (all-MiniLM-L6-v2, a 384-dim
sentence-transformer running locally via ONNX — downloaded once,
~80 MB, then cached). So this entire project needs NO API key.

In a real hackathon you would usually swap the embedding for an API
model (OpenAI text-embedding-3-large, Voyage, or the legal-specialized
Kanon 2 Embedder) — in Chroma that is one argument:

    from chromadb.utils import embedding_functions
    ef = embedding_functions.OpenAIEmbeddingFunction(api_key=..., model_name=...)
    client.get_or_create_collection("contract", embedding_function=ef)

Everything else (this file, query.py) stays identical. That is the
point of learning the pipeline shape rather than a framework.
"""

from pathlib import Path

import chromadb

from chunking import MD, chunk_markdown

DB_DIR = Path(__file__).parent / "chroma_db"
COLLECTION = "contract"


def get_collection() -> chromadb.Collection:
    # PersistentClient writes the index to disk, so build once, query many.
    client = chromadb.PersistentClient(path=str(DB_DIR))
    # cosine distance is the standard choice for sentence embeddings
    # (they are compared by angle, not magnitude).
    return client.get_or_create_collection(
        COLLECTION, metadata={"hnsw:space": "cosine"}
    )


def main() -> None:
    chunks = chunk_markdown(MD.read_text(encoding="utf-8"))

    # Rebuild from scratch on every run. The tempting alternative —
    # upsert into the existing collection — has a real-world gotcha:
    # if a chunking change REDUCES the chunk count, the ids that no
    # longer exist stay behind as stale entries and quietly pollute
    # retrieval. Drop-and-recreate makes re-runs truly reproducible.
    client = chromadb.PersistentClient(path=str(DB_DIR))
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass  # first run — nothing to delete
    col = get_collection()

    col.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[{"section": c["section"]} for c in chunks],
    )
    print(f"indexed {len(chunks)} chunks into {DB_DIR}/")


if __name__ == "__main__":
    main()
