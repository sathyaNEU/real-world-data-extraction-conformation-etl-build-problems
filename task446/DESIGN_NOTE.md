# task446 design note (architecture 2)

Seed ET03 (GLEIF LEI-hierarchy issuer-group concentration, Data Extraction & Conformation). Architecture 1
(obligor-group house-limit projection on the projection-date membership) was spent at solver round 1 as a
rule-application stump (see `## Tried and rejected` and `solver_rounds/round-1.md`). Architecture 2 keeps the
number, the objective and the seed's world (the GLEIF consolidation hierarchy carrying entity-level records up
to obligor groups, a UK bank's own systems) and draws a new decision and a new Layer 2 pitfall.

## DRAW

| Axis | Draw |
|---|---|
| Card | `cards/task446.json` v2, `guard.py check` PASS, registered 2026-10-11 before the ladder; v1 kept in `lineage` with its fate |
| Domain / task type | banking-credit-financial-risk / other: early-warning and watch-list monitoring of corporate obligor groups (client domain Banking, Credit & Financial Risk) |
| Objective | Data Extraction & Conformation (ETL): four closed annual cohorts and the live book built from an early-warning engine's entity-level monthly signals, carried to obligor groups through the credit system's group register and the GLEIF consolidation hierarchy, matched to the watch-list history; the forecast runs on that conformed cohort table |
| Shape | 01 ranked list: the six sectors ranked by expected watch-list arrivals, each with groups monitored, groups flagged, expected arrivals and expected arriving exposure |
| Gate G mechanism | forecasting, with method_or_model_selection support (which performance measure carries across cohorts) |
| Gap / pattern | time then population / none; generators G16 (decisive), G13, G19 |
| Decision type | quantity_figure (count: obligor groups the 2027 watch-list caseload plans for) |
| Stump strategy | forecast_method_backtest; decisive rule filed: no; official decoy: no; validated decoy: no |
| Calibration | existing_book_actuals: the bank's own four closed cohorts, used to measure the screen and to back-test how its performance carries forward |
| Context artifact | filed_model (the early-warning system's model documentation and monitoring standard) |
| Role | head of credit risk monitoring (portfolio_manager family); forum committee_or_panel (executive risk committee); forcing event budget_or_appropriation (2027 resourcing budget); org financial_institution |
| World | United Kingdom, GBP, Halstow Bank plc; personas Jill Berry, Mathew Long (`guard.py names --geo 'United Kingdom' --seed 446`) |
| Layer 2 | forecast_uncertainty, own:screen-yield-under-a-moved-base-rate |
| Layer 1 | entity signals keyed by LEI including non-borrowing entities; GLEIF L1/L2 with relationship periods, lapsed registrations, successors, branches, fund-management links; credit-system group register and watch-list history in their own namespace; a re-issued sector code with a crosswalk; facility extracts from two booking entities with currencies and a late file (exposure asks only) |

**Similarity claim.** No build on file turns on which of a screen's measured properties carries to a year with
a different base rate. Nearest drivers sit at 0.06 and below (task57 v19 held-out year, task89 v11 forward roll,
task51 decomposition). Rejected neighbours this draw passed through are recorded in `## Tried and rejected`.

## Stump sentence

A competent solver rolls the entity signals up to groups, builds the four closed cohorts, measures the
early-warning system's hit rate (the share of flagged groups that reach the watch list within twelve months)
and its miss rate exactly as the monitoring standard reports them, applies them to the groups flagged and not
flagged at 30 September 2026 and files a caseload about half the golden; the hit rate rises with each cohort's
deterioration rate, and this year's flagged share implies a deterioration rate far above any closed cohort,
which only the capture and false-alarm rates (stable across the cohorts) can back out of the flagged share.

## Data-native sentence

An early-warning screen on a credit book is judged by its hit rate, but how many flags turn bad depends on how
much of the book is deteriorating that year, and the bank's own cohorts show exactly that: the capture and
false-alarm rates sit still while the hit rate climbs in the year rates rose, so a year in which the flagged
share has jumped is a year in which the hit rate measured on calmer years undercounts the inflow.

## The three rules

- **Domain test.** The call is a credit-monitoring forecast, the watch-list inflow a bank sizes its workout
  caseload on, from an early-warning system's performance on obligor groups (signals raised on any legal entity
  and carried to the group through accounting consolidation, a twelve-month watch-list outcome, the committed
  book as the monitored population). With another field's nouns in, the group roll-up of entity signals, the
  watch-list window and the committed-book population have nothing to attach to.
- **Two layers.** Layer 1: an early-warning engine that publishes monthly signals per legal entity by LEI
  (borrowers and the non-borrowing parents and sisters the vendors cover), the GLEIF golden copy with its real
  behaviour, the credit system's group register and watch-list history in its own customer namespace, a sector
  taxonomy change that re-issued codes, facility extracts with currencies and a late booking-entity file. Layer
  2: a screen's past yield is carried onto a year whose base rate has moved; the yield is a property of the year,
  the error rates are the screen's, and the cohorts show it.
- **Decisive step class: analytical.** Analyst test: a strong analyst who conforms every signal to its group
  correctly and reads the standard's group-flag rule, cohort definition and performance measures correctly
  applies the measured hit rate to this year's flagged groups and the miss rate to the rest, because those are
  the screen's reported performance over exactly the cohorts the standard names, and so files about half the
  expected inflow.

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
- Architecture 1 (obligor-group house-limit projection, history rebuilt on the membership at the projection date), spent at round 1, 2026-10-11: the solver fixed the 30 Sep 2026 group and applied it to all five quarter-ends citing LMS-03 s.2.3, landing 21.8 and cracking every ask device (proxy 93.4). The decisive step was the stated clause applied, a rule-application stump; un-stating it would be a withheld rule or a fork, so no honest hardening exists. Re-rooted to architecture 2.
- Architecture 2 candidate, corporate deposit retention standardised on whether the depositor's consolidation group borrows from the bank (moderator behind the GLEIF join, mix moved by a notice-account campaign): the same driver as task97 (a forward rate set by a linked entity's property, newcomers concentrated on one side, every unit-level route misforecasts) and task44 v2 (a correct pooled effect carried onto a moved mix); a Template finding waiting to happen, and a real treasury would file its segmentation.
- Architecture 2 candidate, deposit run-off assumptions moved only when the year's measured share clears two standard errors, with the error clustered on the GLEIF consolidation group so the move becomes a hold: the same driver as task229 (the standard error of a mean over entities that fail together through a shared parent).
- Corporate deposit retention with intra-group sweeps capped at account level (retention has to be measured on the group's money): stump strategy grain_or_unit, banned against task229 in the last three.
- Seasonal working-capital projection of group exposure chosen by back-test: a seasonal pattern clean enough for the seasonal methods to converge is plain on the twelve-quarter series, and with noise the seasonal methods fork on the approvable step.
- Contractual roll-forward of group exposure to the projection date (maturities, amortisation, commitment expiries): every step is a row predicate on a filed date, a filter a solver writes first.
- Near-term deposit outflow from the register of notices already given: maturity_censoring family, banned against task445 in the last three.
- Partial verification of a sampled review (below-the-line alert testing, a file-review sample): stratum rates are what a solver computes by default, and a value-proportional design is either filed (a reading) or unrecoverable (a fork).
