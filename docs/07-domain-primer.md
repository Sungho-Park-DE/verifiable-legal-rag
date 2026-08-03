# Domain primer: the one-day legal kit

Four regulatory/institutional systems every legaltech build in Germany
touches. Each is a design logic, not a rule list — grasp the logic and
the details follow. (Case names and years below are reliable; verify
docket-number-level specifics before citing formally.)

## 1. EU AI Act — product-safety thinking

The AI Act is **not** a rights-based law like the GDPR; it is product-
safety regulation in the CE-marking tradition: "this product class is
risky, so prove a quality-management system before placing it on the
market." The regulated unit is *placing an AI system on the market*,
not a data-processing operation.

The risk tiers follow from that frame:

- **Prohibited** (Art. 5): risks no safeguard can justify (subliminal
  manipulation, social scoring). In force since Feb 2025.
- **High-risk** (Annex III): domains where AI errors directly threaten
  fundamental rights. Justice is listed because errors touch the right
  to an effective remedy and a fair trial (Charter Art. 47). High-risk
  ≠ banned — it means risk management, data governance, logging, human
  oversight, accuracy/robustness requirements, and conformity
  assessment.
- **Limited risk** (Art. 50): where the risk is *not knowing you're
  talking to an AI* — hence the duty is disclosure, nothing more.

The legaltech dividing line, Annex III point 8(a): AI intended to
assist a **judicial authority** (or ADR body with legal effect) in
researching/interpreting facts and law and applying it to concrete
facts is high-risk. Lawyer-facing tools generally are not — the logic
being that an independent professional's judgment sits between the AI
error and the fundamental-rights impact. Recital 61 excludes "purely
ancillary administrative activities" (e.g. judgment anonymization);
Art. 6(3) exempts narrow preparatory/procedural systems.

Roles: **provider** (develops/markets the system) vs **deployer**
(uses it professionally) carry different duty sets — a commercialized
hackathon prototype makes you the provider; the law firm using it is
the deployer.

Timeline (as amended by the 2026 Digital Omnibus): prohibitions and
AI-literacy Feb 2025; GPAI-model duties Aug 2025; **Annex III
high-risk duties deferred to Dec 2, 2027**; Art. 50 transparency stays
on the original schedule and applies now.
(https://artificialintelligenceact.eu/annex/3/)

## 2. GDPR — prohibition by default

The key to the GDPR is the direction of its default: processing
personal data is **prohibited unless justified** by one of six legal
bases (Art. 6) — the opposite of "do it and answer for problems". Every
GDPR question reduces to "what is my basis?".

The gates, in order:

1. **Is it personal data at all?** Anonymous data is outside the GDPR
   entirely (Recital 26) — which is *why* officially anonymized court
   decisions are the safe demo corpus. **Pseudonymization is not
   anonymization**: if a key can re-identify, it is still personal
   data; "I deleted the names" is usually pseudonymization.
2. **Which Art. 6 basis?** Consent is revocable and burdensome; the
   workhorse in practice is **legitimate interest** — Art. 6(1)(f),
   a documented three-step balancing test: legitimate purpose →
   necessity (no less-intrusive alternative) → the data subject's
   interests do not override.
3. **Special regimes on top.** Art. 9 (health, religion, sexual
   orientation …) and Art. 10 (criminal data) add an extra prohibition
   layer with narrower exceptions — and legitimate interest is *not*
   among the Art. 9 exceptions. This is fatal for legal documents:
   case facts structurally contain such data (divorce → health,
   criminal cases → Art. 10). "Court files are bundles of
   special-category data" is the core intuition of this domain.

Above all of it sit the Art. 5 principles (minimization, purpose
limitation) — they constrain *how* you process even when a basis
exists.

## 3. RDG — the "individual legal examination" boundary (Germany)

The Rechtsdienstleistungsgesetz bans non-lawyer legal services to
protect consumers from unqualified advice. §2(1) defines the regulated
activity: work in **a concrete third-party matter** requiring
**individual legal examination** (rechtliche Prüfung des Einzelfalls).
Both prongs must be present:

- General information ("the filing deadline is three weeks") concerns
  no specific matter → outside RDG.
- **Deterministic computation and form assembly involve no legal
  judgment** — mechanical application of statutory formulas and
  requirements → outside RDG. The BGH's *Smartlaw* decision (2021)
  confirmed this for a Q&A-tree contract generator: schematic
  processing, not individual legal examination.
- "Your case will win, do X" — individual legal advice → lawyers only.
- The **Inkasso route**: §10 RDG allows registered debt collectors to
  provide collection services; the BGH's *LexFox/wenigermiete*
  decision (2019) read "collection" broadly enough to cover checking,
  asserting, and enforcing consumer rights (rent-cap claims) as
  incidental to collection. The 2021 Legal Tech Act partially codified
  this (success fees for collection claims, disclosure duties, with a
  €2,000 threshold currently under evaluation).

Violations have teeth: the service contract is void (§134 BGB) and
competitors can sue under unfair-competition law — which is why German
legaltech startups have litigated this line for a decade (the Smartlaw
plaintiff was a bar association).

Design consequence used throughout doc 06: tools that **compute,
verify, and assemble** — leaving judgment to a human — can be built
RDG-clean, ideally distributed through recognized advice organizations.

## 4. German courts — why the structure looks like this

Germany splits adjudication into five branches out of specialization
plus **social-protection design**: labor and social courts carry lay
judges, and social courts charge insured claimants **no court fees** —
which is structurally why benefit recipients can file AI-written
complaints directly (the BescheidCheck context).

- Ordinary courts: Amtsgericht (small claims ≤ €5,000; exclusive
  jurisdiction over residential tenancy regardless of amount) →
  Landgericht → Oberlandesgericht → BGH. Constitutional review sits
  separately at the BVerfG.
- Specialized: Arbeitsgericht (dismissal suits, 3-week deadline),
  Sozialgericht (benefits), Verwaltungsgericht (incl. asylum),
  Finanzgericht (tax).
- **Widerspruch before Klage**: administrative decisions get an
  agency self-review stage first (social law: SGB X), typically with a
  one-month deadline — free, fast, and the statistically best
  intervention point for calculation errors. That is why A2J tools
  target the Widerspruch, not the lawsuit.
- **Legal aid**: Beratungshilfe (out-of-court advice; flat fees below
  cost → lawyers avoid it → the supply gap) and PKH (litigation cost
  aid, income-tested).
- Citation grammar: `§ 233 ZPO` (section, code), `Abs.` (paragraph),
  `S.` (sentence), `i.V.m.` (in conjunction with), `BGBl.` (federal
  gazette). Core codes: BGB (civil), ZPO (civil procedure), SGB II
  (basic income support), KSchG (dismissal protection), DSGVO (GDPR).

## The common thread

All four systems ask the same question from different angles: **where
does the judgment happen?** The AI Act asks whether it reaches a judge;
the GDPR asks whether data identifies a person; the RDG asks whether a
tool replaces legal judgment. An architecture where the model proposes
and deterministic code disposes — this repo's trust-layer design —
lands on the favorable side of all three lines by construction.
