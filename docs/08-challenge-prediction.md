# Challenge prediction: Legal Loves Tech 2026 tracks

Research snapshot Aug 3, 2026. The challenge briefs are only revealed
during the hackathon week (Verbraucherrecht: Wed Aug 19, Justiz: Thu
Aug 20), so this doc profiles the two challenge-providing organizations
to predict the likely problem domains. Three research passes: the
consumer-protection agency, the justice ministry, the organizer
ecosystem.

## Track 1 — Verbraucherrecht (Verbraucherzentrale Bayern)

**Presenter:** Simone Bueb, Juristin/Referentin für Verbraucherrecht in
the "Recht und Digitales" unit — a practitioner whose public beat is
everyday consumer contract law: subscription traps, warranty add-ons,
fake discounts, telecom rights, non-EU platform shopping. Expect a
challenge grounded in advice-desk case patterns, not abstract AI
policy.

**The organization's structural math** (Jahresbericht 2024): ~82
advisory staff for 13M Bavarians vs 2.29M web visits — the web channel
absorbs ~25× what humans can. Their explicit answer is self-service
tooling: five interactive individualized Musterbrief generators built
in 2024 alone, plus Fakeshop-Finder and Fake-Check Geldanlage.

**Top current problem areas by their own evidence:** (1) online fraud —
fake shops ×6 since 2020, fraudulent Oktoberfest reservation sites =
their most successful press release ever; (2) subscription traps and
obstructed cancellation (Kündigungsbutton enforcement incl. Microsoft,
Vodafone); (3) the "case of the year": 1N Telecom — deceptive letters
to elderly Telekom customers followed by Inkasso pressure that "even
very experienced advisors struggled to fend off", now a 15,000+
complaint collective action; (4) energy; (5) finance/insurance.

**Challenge hypotheses (ranked):**
1. **Self-service claim-enforcement assistant** — triage a consumer
   problem → check rights → generate an individualized
   Musterbrief/cancellation/withdrawal. This is the tool class they
   already build, aimed at their capacity gap.
2. **Inkasso / demand-letter defense** — upload a dunning letter, check
   legitimacy, draft the objection (1N Telecom pattern + vzbv's Oct
   2025 Inkasso reform paper).
3. **Fraud/fake-shop first aid** — detection plus what-to-do-now rails
   (chargeback, Widerruf, Anzeige).
4. **Collective-redress matching** — does this consumer's case fit a
   running Sammelklage (sammelklagen.de, VDuG Abhilfeklage)?
5. (Weaker) rural/multilingual/einfache-Sprache advice access.

**Culture note:** vzbv is publicly AI-skeptical about company-side
chatbots (manipulation, hallucinated advice) while building digital
tools itself → a free-form advice chatbot fights their culture;
verifiable, source-grounded, human-in-the-loop outputs match it.

## Track 2 — Justiz (Bavarian State Ministry of Justice)

**Presenter:** Maximilian Kruger — StMJ, active in the legaltech
circuit (LMU certificate teaching, Legal Tech Colab funding handover);
unit unverified but almost certainly the Digitalisierung-und-Innovation
Referat that owns the projects below.

**Live projects (the ministry showcases running systems, not
greenfield):**
- E-Akte rollout complete (Dec 2025, all 99 courts); "next steps" named
  as AI + legal tech + civil-procedure modernization.
- **Online-Verfahren Reallabor live since Apr 15, 2026** — Bavaria is a
  pilot state: AG Nürnberg (payment claims ≤ €10k) and AG Erding (air
  passenger rights).
- **Digitale Rechtsantragstelle** (service.justiz.de) — first citizen
  use case: the Beratungshilfe (legal-aid) application.
- Mass-proceedings AI: AG Erding Fluggastrechte software with an LLM
  since Aug 2025; diesel assistants at LG München I / Ingolstadt / OLG
  München; federal MAKI umbrella; a Bavaria+NRW generative LLM for the
  judiciary (with TUM + Uni Köln) in test until end-2026.
- Judgment anonymization with FAU Erlangen — target: publish 50,000
  Bavarian judgments within 3 years.
- Basisdokument (structured party submissions), Codefy e-file
  structuring, SMART/IMJ mail extraction; Denkfabrik lineage includes a
  Fake-Shop Detector.

**Flagged friction:** mass proceedings (the most repeated pain point),
a Bavarian social-court crisis (38,640 new cases 2025, urgent
proceedings doubled), citizen filing friction (Beratungshilfe chosen as
the #1 digital use case precisely because it is the most-filed citizen
application).

**Challenge hypotheses (ranked):**
1. **Citizen-facing entry into the Online-Verfahren / digitale
   Rechtsantragstelle** — turn a layperson's problem into a
   well-formed digital claim or aid application; Bavaria just went
   live as a pilot state and needs adoption + submission quality.
2. **Mass-proceedings assistance** (Fluggastrechte at AG Erding is
   their live LLM testbed).
3. **Judgment comprehension layer** — search/summarize/plain-language
   explain the 50,000 judgments the anonymization project will
   publish.
4. Basisdokument-style structured submissions for self-represented
   litigants.

**Precedent:** in 2023 the StMJ held patronage only, with no own
challenge; a dedicated StMJ-presented track in 2026 is a step up —
expect it anchored to a currently live pilot.

## Organizer-ecosystem taste (what gets rewarded)

1. **Auditability/determinism over LLM magic** — partner startup
   Bayshore's entire thesis is deterministic guardrails around agents
   ("reliable, explainable, auditable"); Libra (€90M Wolters Kluwer
   exit) sold grounding; Radtke works on AI Act human oversight; Wais
   builds citation-grounded retrieval pipelines.
2. **Citizen/SME-facing, narrow, real use case** — the entire 2023
   podium: ComplAI (SME regulatory monitoring), LiKA (LkSG supply-chain
   compliance), **Prozesskostenkompass (plain-language legal-aid
   application help — 3rd place, and now the exact domain of the
   digitale Rechtsantragstelle's first use case)**.
3. **German-law specificity** — winners were anchored in named German
   instruments; MLTech benchmarks LLMs on the Bavarian state exam.
4. **Legal design / comprehensibility as substance** — Djeffal holds
   the Legal Design professorship; the 2023 3rd place won explicitly
   for understandability.

## Convergence and field choice

Both tracks converge on the same product shape: **structured intake →
deterministic verification → generated, citation-anchored documents for
laypeople.** The consumer agency already builds Musterbrief generators
and drowns in demand; the ministry just launched the digital rails
(Online-Verfahren, digitale Rechtsantragstelle) and needs well-formed
citizen submissions flowing into them. The ecosystem independently
rewards exactly this architecture (auditable, German-law-specific,
comprehensible).

Field assessment:
- **Verbraucherrecht** is the more predictable track (the challenge
  will almost certainly live inside their existing self-service
  strategy), with easy demo data (scam letters, subscription
  cancellations, Inkasso demands) and a practitioner presenter.
- **Justiz** is anchored to live pilots; the sharpest concrete targets
  are Fluggastrechte (AG Erding) and the Beratungshilfe application —
  note the deep overlap with the consumer track at the
  "citizen-with-a-money-problem" level.

Preparation implication: study both domains' primitives (consumer
letters: Widerruf/Kündigung/Inkasso objection; justice rails:
Online-Verfahren, Rechtsantragstelle, Beratungshilfe), go deep on one,
and keep the shared architecture ready — it serves either brief.
