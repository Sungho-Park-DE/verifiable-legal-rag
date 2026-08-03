# Domain fundamentals: consumer-law weapons & justice rails

Study notes for the two predicted challenge domains (see
[doc 08](08-challenge-prediction.md)). Figures are stable core rules but
verify against current statute text before encoding — the point-in-time
problem applies to this doc too.

## Cluster A — consumer-law primitives

**Widerruf (§§312g, 355 BGB)** — 14-day no-reason withdrawal for
distance contracts (cooling-off logic; unrelated to defects). The
period starts only upon proper Widerrufsbelehrung; a missing/defective
instruction extends it to 12 months + 14 days (§356(3)) — a
deterministic "instruction-defect check = deadline-extension verdict".
Without proper instruction, no value compensation for use (Wertersatz).
Exercise is form-free but must be explicit.

**Kündigung** — exit rules for continuing obligations. Two tool-ready
protections: §309 Nr. 9 BGB (AGB limits since 2022: max 2-year initial
term; after auto-renewal, terminate anytime on 1 month's notice) and
§312k BGB Kündigungsbutton (since 2022: online continuing contracts
need a two-click cancel button; missing/defective button → terminate
anytime without notice — a binary check with legal effect).

**Gewährleistung vs Garantie** — statutory 2-year defect rights
(repair/replacement first; 12-month burden-of-proof reversal §477) vs
a voluntary seller promise. Paid warranty extensions often resell what
the statute already grants — a comparable, tool-able delta.

**Inkasso defense** — chain verification: ① does the underlying claim
exist (subscription traps often lack a valid contract), ② is the
collector in the public Rechtsdienstleistungsregister (open lookup),
③ are fees within the post-2021 RVG caps (arithmetic), ④ limitation
(3 years, year-end start, §§195/199 — calendar math). A disputed claim
(bestrittene Forderung) may not be reported to Schufa — the threat is
pressure, not law.

**The escalation ladder** — the one asymmetry to internalize:
Rechnung/Mahnung and Inkasso letters carry **no legal deadline**
(verify and contest); the court **Mahnbescheid** is issued *without any
merits review* and must be answered within **2 weeks** with a
Widerspruch (a checkbox form, no reasons required), else it becomes
enforceable (Vollstreckungsbescheid: last 2-week Einspruch window,
then enforcement). Typical victim failure: ignoring the Mahnbescheid
because the Inkasso letters were ignorable.

## Cluster B — justice rails

**Mahnverfahren** — the automated payment-order track (millions/yr,
central courts, no merits check); Widerspruch converts it to normal
litigation. Cheapest attack for creditors; a no-review pipeline from
the debtor's view — tooling angles on both sides.

**Online-Verfahren (Reallabor, live Apr 2026)** — fully digital civil
procedure for money claims ≤ €10k on structured input forms instead of
free-text pleadings; 18 pilot courts incl. AG Nürnberg (payment) and
AG Erding (air passenger). The bottleneck is citizen-side: converting a
messy situation into the structured inputs.

**Rechtsantragstelle** — the court walk-in desk where staff convert a
citizen's oral request into legal form; the century-old human intake
converter, now being digitized (service.justiz.de; first use case:
the Beratungshilfe application).

**Beratungshilfe & PKH** — out-of-court aid (Beratungshilfeschein from
the AG, €15 own share, means-test arithmetic on published allowance
tables; supply fails because lawyer fees are below cost) vs in-court
aid (PKH, §§114ff ZPO: means test **plus** a merits/prospects check —
so tools should compute the arithmetic and leave prospects to humans).

## Case walkthrough: the subscription trap end to end

Facts: Jan 10 — "free trial" signup, button says "Jetzt kostenlos
testen", fine print converts to a 12-month €29.99/month plan; no
withdrawal instruction; no cancel button on the site. March — charges
noticed, email cancellation rejected ("12-month term, pay €270
remainder"); SEPA charge-back; May Mahnung; June Inkasso (€270 + €95
fees, Schufa threat); July 30 (worst case) a Mahnbescheid.

| Decision point | Rule | Nature |
|---|---|---|
| Did a contract form at all? | §312j(3),(4) Button-Lösung: the order button must state a payment obligation; "kostenlos testen" → consumer not bound | lookup (edge cases: judgment) |
| Withdrawal alive in March? | No instruction → deadline never started; max: Jan 10 + 12m + 14d = Jan 24, 2027 | arithmetic |
| Termination path? | No Kündigungsbutton → §312k(6): terminate anytime | binary lookup |
| Money back fast | SEPA direct debit: unconditional refund within 8 weeks of the debit | arithmetic |
| Inkasso letter | chain check (claim / register / fee caps / disputed-claim-no-Schufa) | lookup + arithmetic |
| Mahnbescheid | the only real deadline: 2-week Widerspruch, checkbox form, no reasons | arithmetic + form assembly |
| If low income | Beratungshilfe: €15, means-test tables → application form | arithmetic + assembly |

**The cascading-defense letter** (the document-generation schema):
primary — no contract (§312j); in the alternative (hilfsweise) —
withdrawal exercised (extended deadline); in the further alternative —
terminated per §312k. One passing check wins; paragraphs assemble from
check results.

**Takeaway:** nearly every outcome-determining check in this case is a
lookup or arithmetic; genuine judgment appears once (trial-conversion
edge cases). The pipeline it implies — extract with confirmation →
deterministic checks → cascading letter + form assembly → deadline
watch — is the convergent product shape from doc 08.

## Engineer's domain-depth guide (interdisciplinary team)

Own deeply: the deterministic/judgment boundary (it decides the
architecture), the data terrain (doc 03), the three safety one-liners
(AI Act / GDPR / RDG). Conversation-level: the primitives above.
Deliberately skip: statute wording details, case-law landscapes —
that's what law teammates own. Day-1 interface behaviors: propose a
fillable format (schema/rule-tree/checklist) within 30 minutes; ask
"is this a table number or a judgment call?"; ask "when does the clock
start and what stops it?"; ask for 3 ground-truth examples per check —
those become the test suite.
