# What wins at legaltech hackathons (2024–2026)

Events analyzed: Stanford CodeX LLM x Law #5/#6, Hack the Law Cambridge
2025, LegalTechTalk London 2025, Munich Hacking Legal 2025/26, Hamburg
recode.law 2025, Global Legal Hackathon, Docusign Unlocked.

## Seven winning archetypes

1. **Contract intelligence / review / risk scoring** — the most common
   category and by 2026 saturated. Winners now need a deterministic or
   verifiable layer on top: ClauseWise (Stanford #6 2026 overall winner)
   compiled contracts into an executable intermediate representation,
   explicitly avoiding probabilistic LLM guessing. Plain contract-review
   chatbots no longer place.
   (https://law.stanford.edu/2026/04/27/2026-llm-x-law-hackathon-6-winners/)
2. **Litigation / argument analytics + simulation** — took the top
   overall prizes at Cambridge 2025. CounterClaim Eagle (1st, £10,000,
   solo builder): LLM agents testing counterclaims against precedent +
   Monte-Carlo litigation simulation + citation-backed responses.
   Quantified risk/outcome simulation on top of LLM analysis is a
   proven top-prize formula. (https://hackthelaw-cambridge.com/hackathon-2025/)
3. **Access to justice (A2J)** — dominant at German/civic events.
   Hamburg 2025 winner: a form-filling tool for young parents claiming
   government benefits. Many events now carve out a dedicated A2J
   prize track. (https://recode.law/en/nachbericht-legal-hackathon-2025-in-hamburg-access-to-justice/)
4. **Regulatory compliance monitoring** — frequent sponsor-challenge
   winner (Law Croissant: multi-agent regulation mapping; an EU AI Act
   repo scanner). Warning: by 2026 the generic "AI Act compliance
   wizard" is the most predictable build in the room.
5. **Junior-lawyer training / institutional knowledge capture** — low
   technical bar, high judge resonance. LexMentor AI won a Clifford
   Chance challenge built entirely by non-programmers via vibe coding.
   (https://www.kingselab.org/blog/vibe-legal)
6. **Hallucination detection / trust layer** — a distinctly 2025–26
   archetype: tools that police AI itself (Hallucin8, Tracy AI,
   JusticeGPS). Anti-hallucination architecture is a winning feature,
   not hygiene. This repo's project 04 implements the core pattern.
7. **Agentic document retrieval / drafting** — RAG grounded in real
   firm/client corpora plus agent orchestration (Cura, Revax).

## Winning technical stacks

- **Agentic-LLM-first (the 2025–26 default):** sponsor-credit LLM APIs
  (GPT/Gemini/Mistral/Groq), LangGraph or hand-rolled orchestration,
  RAG over legal APIs (Jus Mundi, vLex, RegGenome), Next.js/Streamlit
  frontends, PostgreSQL. By 2026 multi-agent + tool-use is the expected
  baseline, not a differentiator.
- **Classic ML + simulation as a rigor signal:** podium finishers still
  use BART-mnli, LightGBM, calibrated classifiers, Monte-Carlo risk —
  quantified, calibrated outputs demo extremely well to lawyer judges.
- **No-code / vibe-coding:** wins sponsor challenges outright (Lovable +
  Momen). Implication for team composition: law-student teammates ship
  independently; engineers should spend effort on the differentiating
  layer (retrieval quality, determinism, evals), not CRUD.

## What judges reward

Typical rubric weights Innovation / Feasibility / Tech Execution /
Impact roughly equally. Legaltech-specific signals on top:

- A **narrow, real pain point named precisely** — domain insight beats
  code quality. Clifford Chance picked a winner because it solved a
  problem the firm had itself tried to build internally.
- **Trust features**: citations to sources, confidence scores,
  explainability, audit trails, deterministic logic.
- **Quantified business framing** (ClauseWise opened with "companies
  lose ~9% of revenue to untracked contract triggers").
- A working end-to-end demo with one 90-second moment that lands.
- Interdisciplinary teams — both Munich winners were law+CS mixes.

A mediocre model behind an excellent demo and clear problem
articulation beats a strong model behind a weak pitch.
(https://info.devpost.com/blog/hackathon-judging-tips)
