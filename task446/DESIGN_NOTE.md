# task446 design note

Seed ET03 (GLEIF LEI-hierarchy issuer-group concentration over N-PORT holdings, Data Extraction &
Conformation). Re-rooted at the draw: the seed's stump (relationship types, LAPSED status, successor
LEIs, ISIN fallback) is rule application and data semantics, and its asset-management pairing
(Quantitative Finance with ETL) was taken by task445, registered first the same day. The objective and
the number stay; the domain moves to Banking, Credit & Financial Risk and the LEI-hierarchy mechanics
stay as Layer 1 on the ask paths.

## DRAW

| Axis | Draw |
|---|---|
| Card | `cards/task446.json`, registered 2026-10-11 with `guard.py register` before the ladder; verdict WARN (answered below) |
| Domain / task type | banking-credit-financial-risk / other: obligor-group credit concentration and house-limit monitoring (client domain Banking, Credit & Financial Risk) |
| Objective | Data Extraction & Conformation (ETL): five quarter-ends of loan, securities and derivative exposure from three booking systems conformed to obligor groups on the GLEIF consolidation hierarchy, then projected under the bank's filed standard |
| Shape | 01 ranked list under a cap: every agenda group ranked on projected utilisation of its house limit, the in-or-out on its request, the approvable amount |
| Gate G mechanism | etl_conformance (the history conformed to the estimand the standard defines) |
| Gap / pattern | population then time / none; generators G4 (attribution at transition, decisive), G2, G19, G13 |
| Decision type | quantity_figure (GBP, the approvable commitment for the requesting group) |
| Stump strategy | time_semantics (which membership a history describes); decisive rule filed: yes (estimand), official decoy: no, validated decoy: no |
| Calibration | none, because nothing has to be recovered: the projection formula and the group definition are filed, and the difficulty is the history the formula runs on |
| Context artifact | other: the credit committee's pending-request agenda |
| Role | head of credit portfolio analytics (portfolio_manager family); forum committee_or_panel; forcing event vote_or_meeting; org financial_institution |
| World | United Kingdom, GBP, a UK commercial bank; personas Lesley Miller, Russell Hussain (`guard.py names --geo 'United Kingdom' --seed 446`) |
| Layer 2 | estimand_identification, own:history-rebuilt-on-the-projected-membership |
| Layer 1 | GLEIF merger events with retired predecessors still keyed in the loan system; lapsed relationship records; international branches; fund-management links; blank issuer LEIs resolvable through the ISIN map; three booking systems with their own keys, currencies and units; quarterly archived reference-data snapshots |

**Guard WARN answered.** `three_rules.strategy_risk` (time_semantics). The decisive step is not
reading a date field: every date in the pack is read the same way on the wrong path and the right
one. The step is choosing which membership a five-quarter history describes when the standard
projects the group as it stands now. The analyst test below names the route that fails after every
field and rule is read correctly: point-in-time joins, the discipline a careful analyst applies to any
history by habit.

**Similarity claim.** No prior build turns on rebuilding a history on the membership of the date the
projection is for. Nearest drivers on file sit at 0.07 and below (task33 forward yield, task65 filed
grouping rule, task87 per-entity cap, task14 entitlement resolved point in time). task14 resolves
membership point in time as the right answer; here point in time is the trap.

## The three rules

- **Domain test.** The call turns on credit-exposure aggregation to obligor groups under
  accounting-consolidation control (drawn loans, undrawn commitments under a credit conversion
  factor, investment securities, derivative replacement cost net of cash collateral per netting set)
  checked against house limits through a limit-monitoring projection; put another field's nouns in
  and the consolidation hierarchy, the commitment exposure measure and the limit framework have
  nothing to attach to.
- **Two layers.** Layer 1: the bank's three booking systems (loans, investment securities, derivatives
  with CSA collateral), each with its own keys, currency and units, and the GLEIF golden copy
  archived at each quarter-end, with its real behaviour (merged LEIs still keyed in the customer
  master, lapsed relationship records, branches, fund-management links, blank issuer LEIs on
  custodian feeds). Layer 2: a five-quarter history built for a projection of the group as it stands
  on the projection date has to be rebuilt on that membership; the point-in-time build books
  acquisitions and disposals as growth and shrinkage.
- **Decisive step class: analytical.** Analyst test: a strong analyst who conforms every quarter's
  three books correctly and reads the standard correctly builds each past quarter on the hierarchy
  archived for that quarter, because point-in-time joins are the default discipline for history, and
  so books membership changes as exposure change and files the wrong approvable amount, too low for a
  group that grew by acquisition and too high for one that sold a borrower.

## Stump sentence

A competent solver conforms all three books, groups each quarter-end on the hierarchy the bank archived
at that quarter-end (or on the customer master's group code as it stood then), and so the requesting
group's April acquisition of a borrower the bank already lends to enters its history as
quarter-on-quarter growth; the least-squares trend it projects with is inflated, the projected
year-end exposure is overstated and it approves a commitment well short of what the limit allows
(figures fixed at build, recorded in the ladder below).

## Data-native sentence

Obligor groups change shape between quarter-ends (a parent buys a borrower the bank already lends to,
sells another to a group the bank also lends to), and the bank's own records of those quarter-ends,
the archived golden copy and the customer master's group code, are both correctly point-in-time, so
the history a projection naturally reads describes groups that no longer exist in that form, while
the standard projects the group as it stands on the projection date.

## Tried and rejected

- Seed as written (5/10/40 group test on N-PORT holdings, relationship types, LAPSED, successors,
  ISIN fallback decide): rule application and data semantics as the decisive step; pairing taken by
  task445 (quantitative-finance with etl).
- Pro forma borrowing base for a fund-finance revolver (concentration caps re-struck on the pool the
  advance buys): the borrowing base is a filed formula; a coding solver re-runs its base function on
  the pro forma pool and bisects the advance, so the decisive step is executing stated definitions
  (dead shape: a committed figure that is the output of a filed formula).
- Self-referencing allocation cap for an allocator funding a new fund mandate (the cap's denominator
  grows with the allocation): honest domain is Quantitative Finance (blocked pairing), and a solver
  who writes the post-funding inequality solves it.
- Quarter-end window dressing of money-fund repo with foreign banks: the only exact construction lowers
  a bank group's exposure at quarter-ends, so every decision it can carry either games a quarter-end
  test or needs a seasonal estimator with open forks.
- Default dependence within obligor groups for a pool tail loss (members default together): the same
  insight as task229 (the independent unit sits behind a shared parent node).
- Linkage-error propagation for holdings without LEIs (gold-standard review sample): calibration form
  banned against task228, estimator forks.
