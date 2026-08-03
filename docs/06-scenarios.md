# 15 project scenarios, judged and ranked

Generated through five persona lenses (small law firm · citizen/A2J ·
court/public sector · company compliance · legal-AI infrastructure),
each scenario anchored to specific findings in [doc 05](05-gap-analysis.md).
Scored by a simulated judge panel (legaltech VC + law-firm innovation
partner + CS professor) on five 1–5 axes: feasibility, novelty,
demoability, data availability, judge appeal (max 25).

## Ranking

| # | Score | Scenario | Lens | One-line verdict |
|---|---|---|---|---|
| 1 | 22 | BescheidCheck | citizen/A2J | Devastating version-toggle demo (reform 11 days old); extraction robustness unproven beyond synthetic forms |
| 1 | 22 | FristSchutz | small firm | Genuinely uncontested niche; legally unsettled whether self-generated logs satisfy the BGH standard |
| 1 | 22 | LexZeit | infra/evals | Productizes a published 0%→0.88 accuracy recovery; least product-shaped demo |
| 4 | 21 | §-Check | small firm | Crispest pain-plus-number framing; least novel concept (two siblings in this list) |
| 4 | 21 | MietMathe (lawyer-side) | small firm | Flat-fee unit-economics framing judges love; Vergleichsmiete has real judgment margins |
| 4 | 21 | Fließband | court/public | Tightest single demo beat (74 cases / 90 seconds); pilots exist, buyer is slow procurement |
| 4 | 21 | Zitat-TÜV | court/public | Best audience-participation moment; duplicates §-Check, yellow-bucket problem |
| 4 | 21 | Justitia-Bench | infra/evals | Live-regenerating benchmark + calibration axis; driest demo format |
| 4 | 21 | Fristklar | citizen/A2J | Built-in countdown tension, zero-LLM critical path; technically shallow |
| 10 | 20 | Schwärze | court/public | Most rigorous eval story; cerebral demo, slowest buyer |
| 10 | 20 | ClauseGap | compliance | Real architectural insight (checklist inversion); sits in the most saturated category |
| 10 | 20 | ParagraphProof | infra/evals | Cleanest one-liner; third instance of the citation-verifier idea |
| 13 | 19 | NormRadar | compliance | Genuine step beyond alert services; weakest data foundation (fakes the version layer LexZeit builds honestly) |
| 14 | 18 | MietMathe (tenant-side) | citizen/A2J | Munich-local resonance; lawyer-side twin strictly better on buyer, legality, economics |
| 15 | 17 | DeployerPass | compliance | Real deadline urgency; the most predictable build at any 2026 legaltech hackathon |

**Overlap families (build one, not three):** the deterministic
citation-verifier core appears as §-Check (small-firm packaging, best),
Zitat-TÜV (court-side), and ParagraphProof (infra); the point-in-time
version layer appears honestly in LexZeit and faked in NormRadar; the
Mieterhöhung rule engine appears lawyer-side (better) and tenant-side.

---

## 1. BescheidCheck — deterministic recomputation of Bürgergeld decisions (22)

**Problem.** Benefits recipients cannot verify whether their Jobcenter
decision (Bescheid) is computed correctly. Legal-aid lawyers avoid
these mandates (below-cost fees), so claimants file 30-page
ChatGPT-written complaints directly at social courts — 300,000+ new
cases in 2025, ~15.6 months average duration in NRW. The 2026-07-01
Grundsicherung reform (tightened sanctions and asset checks) is
officially expected to add a litigation wave.

**Gap anchor.** Social-court overload + legal-aid supply failure (axis
2) + temporal reasoning: vanilla LLM reasoning accuracy on
post-amendment German law is a measured 0%, recovered to 0.78–0.88 by
version-filtered RAG (axis 3 #3). Because the reform just took effect,
generic chatbots are currently answering with repealed law.

**Solution & demo.** PDF extraction (structured outputs) → user
confirms fields → a Python rules engine with pre- and post-reform
Regelbedarf rate tables recomputes the benefit → diff view ("Jobcenter
says €563/month — the law says €587") → auto-generated 2-page
structured Widerspruch. Killer demo: toggle the decision date between
2026-06-30 and 2026-07-02 and watch the applicable norms and amounts
change, next to a generic chatbot answering with the old law.

**Data.** gesetze-im-internet XML (SGB II, SGB X, Regelbedarf
ordinances, both versions), DIP Bundestag API (reform bill for old/new
diffs), rechtsprechung-im-internet/NeuRIS (BSG case law), synthetic
Bescheide modeled on public advisory templates (Tacheles e.V.).

**Trust angle.** The recomputation is 100% deterministic (statutory
rate tables + arithmetic); deadlines are calendar math; § citations are
version-pinned RAG with XML anchors. The verdict is a replayable
calculation, not a model opinion. LLM only extracts and phrases.

**Risks.** Bescheid formats vary by Jobcenter (scope demo to synthetic
standard forms); housing costs (KdU) are municipal discretion — exclude
from the deterministic scope; RDG boundary → frame as "calculation
verification + document assembly", distribute via recognized advice
organizations.

---

## 2. FristSchutz — the beA blackbox: outage evidence recorder (22)

**Problem.** Since 2022 German lawyers must file through beA — which
fails repeatedly (BRAK's own log for Feb 2025: a login outage, three
remote-signature outages, directory failures). BGH case law makes the
lawyer prove the outage "immediately and concretely" (Glaubhaftmachung)
or eat the missed deadline and the malpractice claim. Solo lawyers have
no monitoring, and deadline filings happen at 23:40.

**Gap anchor.** beA outages + burden-of-proof transfer (axis 2 #2);
non-billable admin drudgery (axis 1); zero venture deals in
court-infrastructure tooling while 59% of capital chases assistant chat
(axis 4).

**Solution & demo.** A lightweight background agent (menu-bar app):
continuously probes beA availability and archives the official BRAK
status feed into a hash-chained timestamped log; on a failed filing,
captures structured evidence (probe results, errors, screenshots,
matching BRAK notices); one click generates a court-ready dossier —
Glaubhaftmachung meeting the BGH concreteness bar, a
Wiedereinsetzungsantrag (§233 ZPO) or §130d S.2 ZPO alternative-
submission cover letter, evidence log as appendix. Demo: simulate an
outage at 23:40 on deadline day, then the one-click recovery.

**Data.** BRAK beA status feed, gesetze-im-internet XML (ZPO), BGH
case law on Glaubhaftmachung; mock beA endpoint for the demo.

**Trust angle.** The evidence record is hash-chained and timestamped —
deterministic, tamper-evident; document generation is template
assembly from logged facts.

**Risks.** Demo runs against a mock beA; legally unsettled whether
self-generated connectivity logs alone satisfy the BGH standard
(position as evidence *support*, paired with the official BRAK log).

---

## 3. LexZeit — point-in-time version API for German federal law (22)

**Problem.** German law changes constantly, but gesetze-im-internet
serves only the current consolidated version. Any legal question about
past facts (a 2021 termination, a pre-reform sanction) needs the law as
it stood then. LLMs silently apply the wrong version in both directions
— and no open German version infrastructure exists.

**Gap anchor.** Axis 3 #3, the most attackable finding: vanilla
frontier models measure 24–40% outcome / **0% reasoning** accuracy on
post-cutoff German statutory questions; version-filtered RAG recovers
0.78–0.88 (arXiv 2605.23497). The fix is proven and it is a data
layer, not a better model.

**Solution & demo.** Scope to 3–5 heavily-amended statutes (BGB
tenancy §§549–577a, SGB II around the 2026 reform, KSchG). Ingest the
bundestag/gesetze git history, align commits to in-force dates via DIP
amendment records, build a versioned store + API + diff endpoint, then
a temporal-RAG wrapper with structured date extraction. Split-screen
demo: the same question answered with and without version filtering.

**Data.** github.com/bundestag/gesetze (git history as version store),
DIP Bundestag API (amendment metadata), gesetze-im-internet XML
(canonical current text), Bundesgesetzblatt (in-force dates), NeuRIS.

**Trust angle.** Version resolution is fully deterministic — every
returned norm carries its commit hash, in-force interval, and BGBl
citation of the amending law. The RAG date filter is a database query,
not a prompt instruction. No version for the requested date → the
system says so instead of guessing.

**Risks.** Community git history has gaps (commit date ≠ in-force
date) — the DIP/BGBl alignment step plus hand-verification of the demo
statutes is the mitigation and the law-teammates' real work. Landesrecht
out of scope (same limitation NeuRIS has).

---

## 4. §-Check — deterministic cite-and-quote verifier for German briefs (21)

**Problem.** Courts now expect lawyers to cite-check the other side's
AI-generated filings — judges have refused fee awards to counsel who
missed opponents' fabricated cases. Checking every § reference, quoted
statute text, and case citation in a 40-page opposing brief is 2–3
hours of unpaid work.

**Gap anchor.** New AI-created drudgery (axis 1 #2); statutory citation
matching <14% for the best models — proving an LLM-only checker cannot
work, which is exactly why a deterministic resolver is the product
(axis 3 #2); misgrounding as the dominant hallucination type (axis 3 #1).

**Solution & demo.** Citation grammar parser (§/Abs./Satz chains,
docket numbers, ECLI) → resolution against official XML corpora →
character-diff of quoted statute text against official wording. Demo:
feed an AI-slop brief with three planted errors (fabricated BGH docket
number, repealed § applied as current, misquoted statute text) — all
flagged in under 60 seconds with diffs; then a clean brief to show the
false-positive rate.

**Data.** gesetze-im-internet full XML, rechtsprechung-im-internet,
NeuRIS API, Open Legal Data, EUR-Lex/Cellar for EU citations.

**Trust angle.** The verdict is a lookup, not generation: citation
resolution is exact matching against official XML, quote checking is a
character diff. Model involvement is quarantined to the
support-relationship layer, always rendered next to retrieved ground
truth.

**Risks.** German citation syntax edge cases (chained cites, i.V.m.,
abbreviation zoo) need a real grammar; <1% publication rate means many
Länder-court cites are unverifiable — the UI must distinguish "not in
public corpora" from "fabricated"; current-version-only XML requires a
version caveat on quote diffs.

---

## 5. MietMathe (lawyer-side) — the 10-minute Mieterhöhung audit (21)

**Problem.** Rent-increase disputes are the fastest-growing slice of
Germany's ~197,000 annual tenancy suits (17.4% → 21.8% in one year).
Auditing one increase demand — §558a formal validity, waiting periods,
Kappungsgrenze, Mietspiegel comparison — is 1–2 hours against a
€150–250 flat or insurance fee, so small firms decline or lose money.

**Gap anchor.** High-volume standardized disputes (axis 2 #10);
billable-hour mismatch — flat-fee volume work is the one business model
where efficiency lands on the small firm's bottom line (axis 1 #4);
omission blindness dictates checklist design (axis 3 #6).

**Solution & demo.** Upload letter + contract → structured extraction
with per-field source spans for one-glance confirmation → deterministic
rule engine: waiting periods (§558 BGB), Kappungsgrenze 15% (Munich),
§558a formal checklist, Munich Mietspiegel 2025 table lookup →
traffic-light audit report where every line expands into its §
citation → reply letter draft. Demo: three sample letters (valid /
cap violation / formal defect), 30-second audits.

**Data.** Munich Mietspiegel 2025 (city-published tables), gesetze-im-
internet XML (§§557–561 BGB, Bavarian Kappungsgrenzen-VO), BGH formal-
validity case law, Destatis litigation statistics.

**Trust angle.** The legal conclusion never comes from the model — a
unit-tested rules engine computes it from human-confirmed fields;
arithmetic shown step by step; omission checks hard-coded.

**Risks.** Mietspiegel systems differ per city (ship Munich-only);
Vergleichsmiete has genuine judgment margins — output ranges, lawyer
decides; a direct-to-tenant pivot would collide with RDG.

---

## 6. Fließband — mass-claims triage bench for airport courts (21)

**Problem.** A handful of Amtsgerichte near airports are paralyzed by
industrialized flight-compensation litigation: 121,000+ suits in 2025,
up to 93% of one court's civil docket. Plaintiff-side legaltech mass-
produces filings; the judge opens every PDF by hand. The judges'
association: no standard software exists.

**Gap anchor.** Mass-litigation paralysis + pilots still test-stage
(axis 2 #5); court-side tools whitespace with €210M funded demand
(axis 4).

**Solution & demo.** Batch intake: folder of complaints → structured
extraction with span-level provenance (flight, date, delay, amount,
defenses) → deterministic core: cluster by flight, compute EU 261/2004
compensation from great-circle distance bands in a unit-tested rules
engine, validate claimed vs owed → cluster dashboard → one-click draft
orders. Demo: 60–80 synthetic complaints, on-screen timer — "74 cases,
10 flights, 90 seconds".

**Data.** EUR-Lex (Regulation 261/2004), OpenFlights airports.dat
(coordinates), gesetze-im-internet (ZPO), BGH Fluggastrechte snippets;
synthetic complaints from claim-portal templates.

**Trust angle.** The money question is answered by a deterministic
rules engine encoding the Regulation's distance/delay table; every
extracted field carries a clickable source span; draft orders are
templates filled from verified fields; the discretionary call
(extraordinary circumstances) is explicitly left to the judge.

**Risks.** Frauke/Kai pilots exist (differentiate: open deterministic
rules core + cluster workflow); real complaints aren't public (say the
demo data is synthetic); court procurement is slow.

---

## 7. Zitat-TÜV — citation firewall for courts (21)

Court-side packaging of the §-Check core: a filing-intake firewall for
the Geschäftsstelle producing traffic-light annotated briefs (green =
resolves, red = does not exist, yellow = unverifiable given the <1%
publication rate). Killer demo: judges invent a plausible BGH citation
and watch it flash red against the government's own XML. Gap anchors
add the LSG NRW AI-complaint influx. Ranked below §-Check because it
substantially duplicates it with a harder buyer; the three-state
yellow design is load-bearing, not cosmetic.

---

## 8. Justitia-Bench — self-regenerating German legal-AI leaderboard (21)

**Problem.** Firms choosing between Harvey/Legora/Vincent/plain GPT for
German-law work have zero independent evidence — every benchmark is
vendor-owned or one private US firm; none measures German law.

**Gap anchor.** Eval-infrastructure whitespace: $6B/yr into legal AI,
essentially one independent evaluator (axis 4); German legal NLP
scarcity (axis 3 #8); calibration failure (axis 3 #10).

**Solution & demo.** Ground truth generated programmatically from
official XML: mask a real § citation in a real BGH decision (ground
truth = the actual citation), quote attribution, norm-existence traps.
Exact-match scoring — no LLM-as-judge, so the leaderboard cannot
hallucinate. Calibration axis: highlight the "confidently wrong"
quadrant. Stage moment: click "regenerate benchmark" — 50 fresh tasks
minted live from this week's decisions, contamination-resistant by
construction.

**Data.** rechtsprechung-im-internet XML (continuously updated → post-
cutoff regeneration), gesetze-im-internet, Open Legal Data, DIP for
amendment-based temporal tasks.

**Risks.** Auto-generated tasks skew mechanical (add an expert-curated
hard tier; frame honestly as "the verifiable substrate"); API costs for
5 models × hundreds of items; federal-court-only coverage.

---

## 9. Fristklar — dismissal 3-week countdown + legal-aid paperwork rail (21)

**Problem.** Miss the 3-week deadline of §4 KSchG and even an unlawful
dismissal becomes valid (§7 KSchG). Dismissal suits +33% in 2025, but
low-wage/short-tenure workers can't reach a lawyer in time: legal-aid
fees make lawyers decline, the aid application is still a paper form,
and success-fee legaltech won't take low-value cases.

**Gap anchor.** Dismissal-suit surge + legal-aid supply failure (axis
2); the saturation warning itself — incumbents cherry-pick profitable
cases — is the evidence of the gap. The twist is the product: not
claims monetization but a rail to the legal-aid system for the people
incumbents decline.

**Solution & demo.** Photo of the termination letter → LLM parses
receipt date/form (user confirms) → three deterministic stages:
deadline clock (statutory period-computation rules), KSchG
applicability decision tree (business size §23, tenure §1, special
protections), Beratungshilfe/PKH eligibility from the published income
tables → outputs a pre-filled official aid application, a draft
complaint for the court's Rechtsantragstelle, and the competent court's
address. Demo: a judge plays "just dismissed", complete filing-ready
paperwork in five minutes under a live countdown.

**Trust angle.** Zero LLM calls on the critical path — deadline
arithmetic, eligibility tree, income-table lookup are all deterministic
with input→rule→result traces. In a domain where a missed deadline is
irreversible, "we don't trust the model" is the product thesis.

**Risks.** RDG boundary (no case-merits assessment — deadline,
eligibility, assembly only; a rail to lawyers, not a replacement);
receipt-date (Zugang) edge cases → always display the conservative
shortest deadline; differentiate from Chevalier-style incumbents by
serving the segment they decline.

---

## 10. Schwärze — audit-grade judgment anonymization (20)

**Problem.** Courts publish <1% of decisions because anonymization is
manual clerk/judge work they call prohibitively expensive; NeuRIS
covers federal courts only. Everyone downstream is starved of data.

**Solution & demo.** The LLM never rewrites text — it only proposes
redaction spans. Deterministic first pass (Rubrum layout, docket
numbers, dates, addresses), recall-oriented LLM sweep second, all
candidates into a replacement table with consistent pseudonyms, human
approval, then byte-identical substitution + audit JSON. Ground truth
by inversion: re-inject fake names into already-anonymized decisions
and show a live recall/precision scoreboard — the eval is the demo.

**Trust angle.** Output text byte-identical except approved spans; full
audit log; a measured recall number instead of vibes; the human
formally makes every redaction decision.

**Risks.** One missed name is a data-protection incident (position as
mandatory-review decision support); slow public-sector buyer;
over-redaction destroys legal usability (whitelist rules essential).

---

## 11. ClauseGap — statutory-checklist omission auditor (20)

**Problem.** SME legal generalists must verify vendor DPAs and supplier
contracts contain what the law requires — GDPR Art. 28(3) lists 8
mandatory DPA elements, LkSG §6(4) expects contractual assurances, AI
Act Art. 25/26 creates pass-through terms. Nobody exhaustively checks
50 contracts for *missing* clauses; it surfaces in audits and due
diligence.

**Gap anchor.** Omission blindness — best models F1 52–63% on
discrepancy detection, systematically missing absent text (axis 3 #6);
calibration failure (#10); compliance-for-SME whitespace vs the
saturated summary-style contract review category (axis 4).

**Solution & demo.** Invert the problem: the statute writes the
checklist. Deterministic layer: Art. 28(3)(a)–(h), LkSG §6(4), AI Act
Art. 26 compiled into machine-readable checklists with norm anchors.
LLM layer: per requirement, a narrow evidence-retrieval task — "find
the satisfying passage with exact character offsets, or report
absence" (absence established only by an exhaustive logged
chunk-by-chunk pass). Output: contract × requirement coverage matrix;
every green cell falsifiable with one click to the highlighted source
span. Demo: 10 public DPA templates, one with the sub-processor
flow-down clause removed — one red cell, click, "47 chunks scanned, no
match; nearest candidate and why it's insufficient".

**Trust angle.** What is checked = statute-derived fixed checklist (the
model doesn't invent criteria); "satisfied" requires a verbatim span
offset; "absent" requires an exhaustive scan log; uncertainty is a
forced separate yellow state — calibration handled by workflow
structure, not model tone.

**Risks.** Paraphrased clauses can trigger false reds (partial/unsure
grade + human queue); must un-pattern-match from "contract review
chatbot" within the first minute; 48h realistically covers 2–3 legal
sources — the expansion story is "adding a statute = adding a data
file".

---

## 12. ParagraphProof — §-citation resolver as an audit layer (20)

Infrastructure packaging of the citation-verifier core: a firewall
between any LLM and the user, with a deterministic German-citation
grammar (Gesetz → § → Absatz → Satz → Nummer, abbreviation table,
ECLI), resolution against normalized official XML trees, and an audit
report carrying source hashes and prompt/model-version logs (aimed at
FRE-707-style chain-of-custody expectations). Pitch line: "We get it
right 100% of the time — by not asking the model." Ranked below
§-Check: same core, most diffuse buyer.

---

## 13. NormRadar — point-in-time statute diff wired to a contract portfolio (19)

Citation-graph join answering "which of MY documents are affected by
this amendment": a deterministic citation parser over company
documents + periodic XML snapshots as a version store + text diffs +
graph join, LLM quarantined to writing impact memos over confirmed
diffs, DIP API as an early-warning panel for pending bills. Judged a
genuine step beyond alert services, but its core temporal capability
must be faked with two self-made snapshots (gesetze-im-internet has no
history) — the weakest data foundation in the field; LexZeit builds
that layer honestly.

## 14. MietMathe (tenant-side) — rent-increase audit for tenants (18)

Identical rule engine to #5 with the tenant as the user: upload the
increase demand, get a traffic-light lawfulness report (cap arithmetic,
timing rules, §558a formal checklist, Mietspiegel range) and a response
letter. Munich-local demo resonance, but closest to the saturated
Conny-style B2C archetype, with real RDG exposure — the lawyer-side
twin is strictly better positioned on buyer, legality, and economics.

## 15. DeployerPass — EU AI Act deployer classifier for SMEs (17)

Deterministic decision-tree encoding of Art. 6 + Annex III + Art.
25/26 (every node carries its norm ID; the full path exports as an
audit log), with an LLM pre-filling the wizard from pasted vendor docs
and generating obligation registers with mandatory per-paragraph norm
anchors. The model never decides the risk class. Real urgency (Aug 2026
staging, €35M fine ceiling), but judged the single most predictable
build at any 2026 legaltech hackathon — half the room will demo some
version of it; edge cases must escalate honestly to "lawyer review
needed".

---

## Cross-cutting pattern

Every top scenario has the same architecture: **the model proposes,
deterministic code disposes** — recomputation, citation lookup, version
resolution, calendar arithmetic, statutory checklists. Plus one
citable number for the pitch and one 90-second demo moment. This is
the trust-layer thesis of project 04 applied to different pain points.
