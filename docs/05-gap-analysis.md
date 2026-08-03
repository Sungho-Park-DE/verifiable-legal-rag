# Gap analysis: what legal AI still cannot do (July 2026)

Four research axes, each run as an independent web-research agent with
per-claim sourcing. These findings are the evidence base the scenarios
in doc 06 anchor to.

## Axis 1 — Practitioner pain points (what lawyers still complain about)

1. **Verification burden erases promised time savings.** Even
   purpose-built legal RAG hallucinates (Lexis+ AI 17%+, Westlaw 34%+ —
   Stanford JELS 2025), so "first draft in seconds" becomes "cite-check
   for hours". Verification is irreducibly human under professional
   responsibility rules.
2. **New drudgery created by AI: cite-checking opponents' filings.**
   Courts sanction "non-offending counsel" who miss the other side's
   fabricated citations; ~712 tracked hallucination decisions by early
   2026, ~90% written in 2025 (LawSites, ABA Journal, Bloomberg Law).
3. **Adoption-value gap.** 74% of professionals use AI weekly, yet 91%
   say their organizations fall short of its potential value (Thomson
   Reuters Future of Professionals 2026); only ~27% say current tools
   deliver.
4. **Billable-hour mismatch.** ~90% of legal spend is still hourly;
   only 7% of in-house counsel saw matter costs fall, 6% were offered
   AI-driven alternative pricing (ACC/Everlaw 2025). Efficiency has no
   business model to land in — except flat-fee volume work (exploited
   by the MietMathe scenario).
5. **Integration failure ("toggle tax").** AI sits outside Word/DMS
   workflows; a third+ of professionals report integration difficulty
   (Wolters Kluwer FRL 2026). Micro-drudgery (cross-references, defined
   terms, tables of authorities) remains untouched; lawyers bill 2.9h
   of an 8h day (Clio 2025).
6. **Pilot fatigue and shelfware; change management outranks tech.**
   ILTA 2025: 57% cite user resistance as the top hurdle — worsening
   year over year. Only 12% of in-house teams track technology ROI
   (ACC CLO Survey 2026).
7. **Germany-specific:** AI lands on a missing digitization base — only
   16% of Kanzleien use dedicated AI tools (legal-tech.de survey 2025)
   — plus EU AI Act deployer documentation duties arriving before value.

## Axis 2 — German structural bottlenecks (state infrastructure)

1. **e-Akte mandate slipped 2026 → 2027**; 16 incompatible state IT
   systems in parallel (LTO 2025-10).
2. **beA (lawyer mailbox) fails repeatedly** — multiple outages logged
   by BRAK in Feb 2025 alone — while BGH case law puts the burden of
   proving the outage (Glaubhaftmachung) on the lawyer. State
   infrastructure risk transferred to users. (→ FristSchutz scenario)
3. **Under 1% of judgments published, flat since 1971** (Hamann, JZ
   2021: never above 1.01% in any year); even top federal courts
   publish 30–40%. Blocker: manual anonymization cost. NeuRIS covers
   federal courts only. (→ Schwärze scenario)
4. **The overload paradox**: civil case intake at a 20-year low, yet
   time-to-judgment at record highs (LG 17.5 months, +24% in two
   years) — process and tooling, not headcount.
5. **Mass standardized litigation paralyzes specific courts**: 121,000+
   air-passenger suits in 2025; up to 93% of one Amtsgericht's civil
   docket; court-side AI (Frauke, Kai) still "test-stage" per the
   judges' association. (→ Fließband scenario)
6. **Social courts overloaded**: 300,000+ new cases in 2025; LSG NRW
   officially flagged an influx of AI-generated mega-complaints from
   unrepresented claimants — citizens armed with AI, courts unarmed.
   The 2026-07-01 Grundsicherung reform is expected to add a wave.
   (→ BescheidCheck scenario)
7. **Legal-aid supply failure**: Beratungshilfe pays below cost, so
   lawyers avoid the mandates; applications are still paper-based.
8. **Small claims double gap**: BMJV itself concluded small monetary
   claims simply go unclaimed and is piloting a fully digital
   Online-Verfahren at test courts.
9. **RDG constraints**: non-lawyer legal services banned; legaltech
   squeezes through the Inkasso registration route (BGH wenigermiete);
   the 2021 Legal Tech Act's €2,000 cap is under evaluation.
10. **High-volume standardized disputes, un-automated**: Mietrecht
    197,092 suits/yr (+7.8%), rent-increase share jumped 17.4% → 21.8%
    in one year; dismissal suits +33% in 2025.
11. **The government's own broken-list**: the new Pakt für den
    Rechtsstaat commits ~€450–500M, incl. a €210M "Digitalsäule" for
    justice digitization (BMJV, June 2026).

## Axis 3 — Measured technical limits of legal AI

| # | Finding | Evidence | Hackathon-attackable? |
|---|---|---|---|
| 1 | Even legal RAG hallucinates 17–33%; dominant error is **misgrounding** (real source, wrong proposition) | Stanford JELS 2025 | Yes — quote-and-verify (project 04) |
| 2 | **Statutory citation matching <14%** for the best models ("catastrophic failure") | CLAUSE benchmark, EACL 2026 (arXiv 2511.00340) | Yes — deterministic resolver over official XML |
| 3 | **Point-in-time law: 0% reasoning accuracy** on post-cutoff German statutes (vanilla frontier models); version-filtered RAG recovers to 0.78–0.88 | "Asking For An Old Friend", arXiv 2605.23497 | Yes — the single most attackable finding (data layer, not model) |
| 4 | Precedent-overruling detection unreliable | arXiv 2510.20941 | Partially |
| 5 | Long-context degradation ("context rot"): accuracy loss from ~50K tokens, lost-in-the-middle | Chroma Research 2025 | Fundamental — design around it |
| 6 | **Omission blindness**: absence of required text systematically missed; discrepancy detection F1 52–63% | CLAUSE 2025 | Yes — statutory checklists instead of open review (ClauseGap) |
| 7 | Redlining and expert research still below lawyer baseline | VLAIR (Vals AI) 2025 | Context |
| 8 | German legal NLP resources structurally scarce; Subsumtion-style reasoning "assistive, not autonomous" | BenGER, arXiv 2605.28183 | Context |
| 9 | LegalBench asymmetry: classification fine, open-ended multi-step rule application is the bottleneck | LegalBench aggregations | Fundamental |
| 10 | **Calibration failure**: equally confident when right and wrong | AI Law Librarians review 2026-02 | Yes — structural (traffic-light workflows), not tonal |
| 11 | Admissibility rules (FRE 707 draft, AI Act) demand methodology transparency and chain-of-custody | Nelson Mullins 2025 | Yes — audit-log-first design is a product feature |
| 12 | Multi-jurisdictional questions degrade sharply; hallucination varies by jurisdiction (US-centric training data) | Curran et al. 2025 | Context for German-language work |

**Synthesis:** the attackable family is *verifiable grounding +
point-in-time versioning + deterministic § resolution + statutory
checklists*. Multi-step legal reasoning itself, context rot, and
calibration are fundamental limits — design around them, don't fight
them.

## Axis 4 — Market saturation vs whitespace (funding-verified)

Record ~$6.0B legaltech funding in 2025, extremely concentrated:
"Legal AI Assistants" took 51% of deals and 59% of capital in a
Jul-2025–Jun-2026 dataset, while compliance, access-to-justice,
immigration, and court-facing tech recorded **zero venture deals**.

**Saturated:** legal research / AI-assistant chat (Harvey at $11B,
Legora $5.5B); contract review / CLM (~100 vendors); e-signature;
German B2C claims automation (a decade of "Flightright for X").

**Whitespace (verified):**
- Litigation analytics for civil-law jurisdictions — blocked upstream
  by data scarcity (and France's judge-analytics ban), which makes the
  data layer itself the opportunity.
- Legal data infrastructure for civil-law case data (no machine-readable
  German corpus; Amtsgericht decisions "practically never published").
- Independent legal-AI evaluation/benchmarking — essentially one
  private firm plus vendor-owned benchmarks; nothing for German law.
- A2J / legal-aid infrastructure; court-side tools (€210M Digitalsäule
  funded, almost no startup supply); compliance-for-SME (qualified);
  insolvency tech; notary/registry workflow (regulatory moat caveat).
