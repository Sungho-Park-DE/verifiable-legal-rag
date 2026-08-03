# German / EU open legal data — weekend-usable sources

Everything below is free and accessible without partnerships, verified
July 2026. This is unusually good open data for a legal system — the
scenarios in doc 06 are built on it.

## German federal law and case law

| Source | What | Access |
|---|---|---|
| gesetze-im-internet.de | All ~6,000+ current federal statutes as XML | No auth; machine-readable index at https://www.gesetze-im-internet.de/gii-toc.xml enables full bulk download. Current consolidated versions only — no history |
| github.com/bundestag/gesetze | Community git mirror of the above | Git history serves as an approximate version store (commit date ≠ in-force date — align via DIP) |
| rechtsprechung-im-internet.de | ~63,000 federal court decisions (BVerfG, BGH, BVerwG, BFH, BAG, BSG) since 2010, officially anonymized | XML per decision, bulk-downloadable via TOC; federal courts only |
| NeuRIS / rechtsinformationen.bund.de | New official portal: statutes + federal decisions, modern REST/JSON API | No auth; test phase (https://docs.rechtsinformationen.bund.de); dataset incomplete — fall back to the older portals for coverage |
| Open Legal Data (openlegaldata.io) | ~250k German decisions incl. some Länder courts | REST API + bulk dumps; volunteer-run, check dump freshness |
| DIP Bundestag API | All parliamentary materials: bills, amendment laws, procedures | Official REST/JSON; rotating public API key on the help page |

## EU level

| Source | What | Access |
|---|---|---|
| EUR-Lex via Cellar SPARQL | 2.7M+ works: regulations, directives, CJEU judgments, 24 languages | Public endpoint http://publications.europa.eu/webapi/rdf/sparql — no registration; 60s query timeout, paginate |
| Bundesgesetzblatt (recht.bund.de) | Federal law gazette, open access since 2023 | In-force dates for amendment alignment |

## Company data (the weak spot)

handelsregister.de is free since 2022 but has **no official API** and
caps automated retrieval (~60 queries/h; mass scraping may be a
criminal offence). Use the offeneregister.de bulk dump (dated: 2019
snapshot) or commercial APIs. Register data still contains personal
data (directors' names) — public availability ≠ GDPR-free.

## Datasets for demos

- **CUAD** — 510 real commercial contracts, 13k+ expert annotations,
  41 clause categories (https://arxiv.org/pdf/2103.06268). Best used as
  realistic demo contracts + a ready-made extraction taxonomy.
- **Munich Mietspiegel 2025** — city-published rent-comparison tables
  (used by the MietMathe scenarios).
- **US comparison**: CourtListener/RECAP (rate-limited free tier since
  May 2026 — prefer bulk downloads) and the Caselaw Access Project
  (6.9M opinions, zero-friction via Hugging Face
  `free-law/Caselaw_Access_Project`).

## Practical notes

- The federal court decisions are **officially anonymized** — the
  GDPR-safe default demo corpus.
- Only ~1% of German court decisions are published at all (see doc 05)
  — case-law coverage below federal level is structurally thin; any
  citation-verification design must distinguish "not in public corpora"
  from "fabricated".
- gesetze-im-internet carries **current versions only** — point-in-time
  law requires building a version layer (the LexZeit scenario).
