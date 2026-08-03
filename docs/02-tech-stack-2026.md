# The mid-2026 rapid-prototyping stack

What is considered current best practice for LLM hackathon builds as of
July 2026, and what is outdated. This repo's projects 01–04 implement
the "current" column end to end.

## Current vs outdated

| Layer | Current (mid-2026) | Outdated / avoid |
|---|---|---|
| RAG | Provider SDK + vector DB directly (~50 lines); framework only when real pain appears | Classic LangChain chains for simple RAG ("why developers are leaving LangChain" era) |
| Document ingestion | pymupdf4llm (fast baseline) → Docling (layout/tables) → VLM OCR API for scans | Building custom layout parsing; Mathpix-style pipelines largely replaced by VLM OCR |
| Vector DB | Chroma (hackathon default), pgvector if already on Postgres, Qdrant for filter-heavy search | FAISS used as a database (no persistence — it is a library) |
| Structured output | Schema-first: Pydantic/Zod + provider-native strict structured outputs | JSON mode + regex parsing of the response |
| Agents | One agent + a good tool set; hand-written tool-use loop; MCP for tool integration | Multi-agent orchestration frameworks in a 24–48h build; OpenAI Swarm |
| Demo UI | Gradio (fastest share link) / Streamlit (chat + dashboard) / Next.js + Vercel AI SDK for polish; v0/Lovable for scaffolding | Hand-coding frontend from scratch |
| Citations | Native citation features (e.g. Claude Citations API) or hand-built quote-and-verify | Prompting the model to "include citations" without verification |

LlamaIndex survives specifically for messy multi-format document
ingestion pipelines; the common hybrid is LlamaIndex for ingestion,
plain SDK for query/generation.

## LLM API access at hackathons

Sponsor credits drive model choice (Mistral/Groq run "best use of our
API" prize tracks). Gemini's free tier (no credit card) makes it the
common student default; Anthropic access typically comes via sponsor
credit pools. Standard insurance against rate-limit death mid-demo:
route across providers with OpenRouter or LiteLLM.

## Legal NLP: weekend-practical vs overkill (benchmarked verdicts)

| Tool / technique | Verdict | Why |
|---|---|---|
| Exact-span quote-and-verify RAG | **Practical, highest leverage** | Verification step is ~50 lines; clickable verified spans demo extremely well (implemented in project 04) |
| CUAD dataset (510 contracts, 41 clause types) | **Practical as data + taxonomy** | Use the 41-category taxonomy as a prompt schema; training a model on it is overkill (https://arxiv.org/pdf/2103.06268) |
| LegalBench / LegalBench-RAG | **Practical as an eval slice** | Mine task definitions; score your system on 20–50 samples for a credibility number; running in full is overkill (https://arxiv.org/pdf/2408.10343) |
| Frontier LLM + good prompts for clause work | **Practical** | ContractEval: prompted frontier models perform at "junior legal staff" level on CUAD clause-risk tasks (https://arxiv.org/pdf/2508.03080) |
| Legal-specialized embeddings (Kanon 2, MLEB #1) | Nice-to-have | ~10% over general APIs; an API swap, but not the usual bottleneck (https://arxiv.org/pdf/2510.19365) |
| Legal-BERT fine-tuning | **Overkill / legacy** | Superseded on every hackathon-relevant axis by prompted frontier models |
| GLiNER-style zero-shot NER | Practical for bulk pre-tagging | Only when corpus is too large to prompt an LLM per chunk |

## The pitch-motivating numbers (verified at research time)

- Commercial legal RAG tools hallucinate: Lexis+ AI >17%, Westlaw
  AI-Assisted Research ~33% (Stanford RegLab, J. Empirical Legal
  Studies 2025 — https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf).
- ~1,490 court decisions worldwide involve AI-fabricated material filed
  by lawyers (Charlotin database, May 2026 —
  https://www.damiencharlotin.com/hallucinations/).
