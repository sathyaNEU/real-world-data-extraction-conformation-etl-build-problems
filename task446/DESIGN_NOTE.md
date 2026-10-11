# task446 design note (architecture 2)

Seed ET03 (GLEIF LEI-hierarchy issuer-group concentration, Data Extraction & Conformation). Architecture 1
(obligor-group house-limit projection on the projection-date membership) was spent at solver round 1 as a
rule-application stump (see the tried-and-rejected section and `solver_rounds/round-1.md`). Architecture 2
keeps the number, the objective and the seed's world (the GLEIF consolidation hierarchy carrying entity-level records up
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


## Gate G

- **Litmus.** No reported number in the pack is wrong and nothing is overturned. The early-warning
  signals, the watch-list history, the group register and every extract are correct for the dates they
  describe; the hit rate the standard defines is the right hit rate for the cohorts it was measured on.
  The difficulty is that a hit rate is a property of the year it was measured in, and the call is about
  a year whose flagged share sits far outside the history.
- **Mechanism:** forecasting (a forward count for a window that has not opened), with
  method_or_model_selection support: which of the screen's measured properties carries across years.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Delete every wrong number:** there are none to delete. Repair every file at source (one facility
  extract, rates quoted both ways, the Dublin file merged, matured facilities closed) and the call and
  the naive figure do not move, because no exposure file is on the call's path (asserted).
- **Lens swap:** no. The naive figure and the answer are the same book under two forecasting models:
  the naive carries P(arrival | flag status) from calmer years, the answer carries P(flag | outcome)
  and backs the year's deterioration rate out of the flagged share; the back-test separates them.
- **No artifact ranks or forecasts.** No performance report, no prior forecast, no prior caseload
  figure ships. The standard defines the three measures and the group-flag rule only.

## Entity and decision

Halstow Bank plc, a UK commercial bank. Credit risk monitoring sizes the 2027 watch-list caseload for
the executive risk committee on 4 November 2026 (one analyst carries twelve groups). The committed
call: **134 obligor groups from the 30 September 2026 monitored book will reach the watch list by
30 September 2027.** Forward facing: the window opens on 1 October 2026. The tag stays ETL: the work
is building the five cohorts from four systems (entity signals keyed by LEI or company number, the
GLEIF consolidation hierarchy for non-borrowing members, the credit system's group register and
watch-list history) and conforming committed exposure from two booking entities; the forecast is one
line of algebra on the conformed cohort table.

## Ladder (asserted in `generator/checks.py`; the call, groups)

Closed cohorts (built from the pack): monitored 846 / 871 / 889 / 902; reaching the watch list
75 / 43 / 36 / 47; flagged 118 / 97 / 94 / 102; flagged and reaching 58 / 33 / 28 / 39. Hit rate
0.492 / 0.340 / 0.298 / 0.382; capture rate 0.773 / 0.767 / 0.778 / 0.830; false-alarm rate
0.0778 / 0.0773 / 0.0774 / 0.0737. Taken together: hit 0.3844, capture 0.7861 (158 of 201),
false-alarm 0.0765 (253 of 3,307). Forward book at 30 Sep 2026: 913 monitored, 165 flagged (0.1807).

| Rung | Reading | Figure | Killed by |
|---|---|---|---|
| R0 | flagged x pooled hit rate + unflagged x pooled miss rate | 73.8 (74) | the hit rate moves with each cohort's deterioration rate (0.492 in the 8.9 per cent year, 0.298 in the 4.0 per cent year); re-run one cohort out it misses by -35.6, +15.4, +40.7 and +9.5 per cent |
| R0b | the latest closed cohort's rates (2025) | 70.6 | the standard measures performance on the four closed cohorts taken together; and the 2025 rates fail the same back-test |
| R1 | the most stressed cohort's rates (2022) | 98.6 | the same; 2022's flagged share (0.140) is still far below this year's (0.181) |
| R2 | hit and miss rates trended on flagged share and extrapolated | 148.4 | not a measure the standard defines; the hit rate is not linear in the flagged share |
| R3 | every flagged group reaches, plus pooled misses | 175.4 | the false-alarm rate: about 7.7 per cent of groups that do not deteriorate are flagged every year |
| Answer | the deterioration rate backed out of the flagged share through the pooled capture and false-alarm rates: 913 x (0.1807 - 0.0765) / (0.7861 - 0.0765) | **134.10 (134)** | |

- **Convergent rigorous routes (C1):** the pooled measures, a straight-line fit of deterioration rate on
  flagged share across the four cohorts, the same fit weighted by cohort size, the mean of the four
  cohort-by-cohort solutions and the solution on averaged rates land at 133.86 to 134.30; all file 134.
- **Back-test the answer's model passes:** re-run one cohort out, capture and false-alarm rates predict
  each closed cohort's arrivals within -0.4, -0.5, +2.5 and -1.7 per cent.
- **Satisfying to stop at.** R0 is the standard's own measure applied the way the measure reads; R0b is
  the freshest evidence; R1 is the analyst's "use a stressed year" instinct; R2 is the half insight.
- **Direction.** Every rung but R2 and R3 sits below the answer; the answer brackets between the
  conditional-rate family (all low) and the flag-count family (high). Nearest wrong cell: R2 at +10.6
  per cent. The base rate with no flags (52.3) and flagged arrivals only (105.4) are rule violations.
- **The decisive move against the seven properties.** 1 no sentence states it (the standard defines the
  measures and that the forecast uses them, not which of them carries across years); 2 the closed
  cohorts do score it, by design (the back-test above), and that is what makes it the only defensible
  model; 3 no arithmetic symptom: R0 reconciles to every count it uses; 4 not a row predicate: it is a
  property of the whole cohort table; 5 the enumeration is algebra over four cohorts; 6 no cutover date
  (the 2022 cohort's high rate is a cycle, not an event); 7 survives deletion (nothing is wrong).

## Stump or fork

The standard files the estimand (expected arrivals from the monitored book within twelve months, by
flag status at book level, rounded to the nearest whole group) and that the forecast uses the
section-4 measures taken together. Two readings of "uses the measures" exist; the data's own structure
decides between them: the hit rate tracks each cohort's deterioration rate while the capture and
false-alarm rates hold, and only the second model survives the one-cohort-out re-run. Every route that
uses the stable properties lands on 134.

## Layers

- **Layer 1 (main path, conformance the standard files):** entity signals keyed by LEI, or by
  `CRN:` and company number for entities without an LEI; non-borrowing members (parents, sisters)
  reached through GLEIF accounting-consolidation records whose period covers the cohort date; the
  credit system's own customer and group namespace; watch-list categories (WATCH and WORKOUT are one
  list); groups already on the list excluded; groups leaving the book count as not reaching.
  GLEIF texture on the main path (lapsed registrations, merged LEIs still in the vendor feed,
  international branches, fund-management links, reporting exceptions) sits on entities whose
  signals are green at every cohort date, so mishandling it moves nothing (asserted).
- **Layer 1 (ask paths, ledgered devices):** the committed-exposure conformance below.
- **Layer 2:** a screen's yield measured in calm years is carried onto a stressed year; the yield
  depends on the base rate, the screen's error rates do not.

## Closure table (22 axes)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | monitored book: active on the group register and not on the watch list at 30 Sep (standard 4.1); C1: no register or watch-list date within 7 days of a cohort date |
| 2 | Unit | obligor group; members = register borrowers plus GLEIF accounting-consolidation members (standard 2); C1: every flagged entity's membership stable across all cohort dates |
| 3 | Attribution window | placed on the list within the twelve months after the cohort date (4.2); C1: no entry within 7 days of a window edge |
| 4 | As-of dating | the September month-end publication; relationship periods covering the date; C1 |
| 5 | Version basis | one publication per month-end; facility extracts: the rerun is the record (extract log, ask path) |
| 6 | Denominator | the three measures' denominators filed (4.3) |
| 7 | Weighting | four cohorts taken together (4.3); C1 across mean-of-cohort and fitted variants (asserted, 133.86 to 134.30) |
| 8 | Window length | the last four closed cohorts (4.3) |
| 9 | Inclusivity | band edges "and under" (standard 6); C1: no group within GBP 0.25m of an edge on the right path |
| 10 | Rounding path | unrounded throughout; whole groups to the nearest (5.3); one decimal on report; every graded figure at least 0.15 of its bin from an edge (asserted) |
| 11 | Tie-break | none (no ranking) |
| 12 | Maturity | the four cohorts are closed (2025's window ends 30 Sep 2026; the history runs to that date); C1: no entry after 30 Sep 2026 in the history |
| 13 | Order of operations | flag at group level before counting; FX before summing exposure |
| 14 | Row order | irrelevant |
| 15 | Duplicate resolution | a group counts once per window; C1: no group enters twice inside one window |
| 16 | Identity | LEI case-normalised; CRN keys through the company number; merged LEIs green (inert) |
| 17 | Netting | none |
| 18 | Units | limits in facility currency; treasury rates in units per pound (ask path) |
| 19 | Code semantics | AMBER and RED flag, GREEN does not (3.2); WATCH and WORKOUT are one list, a category change is not an entry (field reference) |
| 20 | Integerisation | nearest whole group (5.3); 134.10 sits 0.40 from the nearest edge |
| 21 | Clause scope | a group's probability depends only on its flag status, for the book as a whole (5.2): not split by band, sector or size |
| 22 | Forward window | the 30 Sep 2026 monitored book only; no new groups (5.1) |

## Ask sheet (supplemental-stumping)

**Main call's declared row population:** the September publications of 2022 to 2026 in the signal
file, the obligor master's key columns, the group register's key and date columns, the GLEIF records
of signalling entities, the watch-list history. Zero facility, FX or maturity rows inside it (the
exposure files are not on the path at all).

| Ask | In the decision | Construction | Devices (all on the exposure path) | Use |
|---|---|---|---|---|
| Per band: expected arrivals from flagged groups | caseload split for the two teams (restructuring above GBP 40m, business support below) | PPV under this year's base rate | band membership moves under every device | team sizing |
| Per band: expected arrivals from unflagged groups | the arrivals the screen will miss, worked by manual review | miss probability under this year's base rate | same | review capacity |
| Per band: expected committed exposure arriving | stage 2 and provisioning planning | probability x committed exposure | all four devices | finance |
| Total row | ties to the call | as above | exposure total under all devices | |
| Chart | the call at a glance | bars are the band figures | inherits | committee |

**Devices.** D2 version: the plc scheduled run (19:40) is superseded by the 23:05 rerun after limit
amendments approved on 30 Sep posted late (extract log is the organ; 41 facilities differ). D4 absent
channel: Halstow Bank Ireland DAC's extract was delivered on 7 October in its own file and is not in
the plc file. D3 units: limits are in facility currency and the treasury closing rates are quoted in
currency units per pound (field reference plus rate file). D8 boundary: facilities whose final
maturity date is the cohort date still carry status ACTIVE in both plc runs; the standard counts only
facilities in force at the end of the cohort date. Each device moves at least one flagged group across
a band edge (asserted per device: which band figures move and by how much).

**Pair arithmetic, stated plainly.** Every band figure is an output of the decisive construction, so a
response on the naive model loses all fifteen band figures and the exposure total whatever it does
with the devices; it keeps the chart's structure. A response on the right model keeps the call and the
two split totals, and keeps the fifteen band figures and the exposure total only if it handles all
four exposure devices. Pair simulation and the generated-rubric recount run at stage 3.

## Shape and criteria

Shape 05: the 134 allocated over five bands, each band with three figures (15), the total row (3,
the two split totals and the exposure total), the call, the chart's five named parts (stacked bars per
band, the band order, flagged against not flagged, the caseload written on the chart, a quotable
title) and two files: 26.

## Prompt

`prompt.md`, 888 characters by voice-check, 148 words, opening on the analyst caseload (number-first;
the script files it as other). The call is one sentence at the seam carrying its unit, both later
paragraphs open by tying back to it. No input file, method, measure or trap word; "early-warning run"
names the system the committee knows. Deliverables `watchlist_inflow_2027.xlsx` and
`watchlist_inflow_2027.png`.

## Realism debts

- A deterioration rate of 14.7 per cent of the monitored book in one year is a stress year (the
  closed cohorts run 4.0 to 8.9 per cent). It is what the flagged share implies, and the flagged
  share's jump is the forcing fact; the signal file shows it in the trigger mix (payment delays and
  rating actions), not in coverage or engine version.

## Stopping rule

A round that lands 134 by the capture and false-alarm route files the architecture as spent at its
decisive rung if the solver's path cites a filed sentence for the move; a round that lands 134 by the
back-test licenses one hardening of the device layer and the ladder below. A round on 74, 71 or 99
with the band figures on the same model is the designed stump.

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
