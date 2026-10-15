# task446 design note (architecture 2, repaired 2026-10-15 under the 10/10 rules)

Halstow Bank plc's 2027 watch-list caseload: how many of the 913 obligor groups in the 30 September 2026
monitored book reach the watch list by 30 September 2027. Shipped 2026-10-11; portal round 1 returned a
membership fork (CRM-07 2.2, fixed); the client returned the build on 2026-10-15 on the 10/10 rule-application
rule, because CRM-07 5.2 filed the model (one probability per flag status, the same across the book), the
fitting window and the leave-one-cohort-out selection, so once the cohorts were built the solver ran a stated
procedure. The repair keeps the world, the data, the call (133) and every graded figure; 5.2 now files the
estimand only, 5.3 the band split as a reporting convention, and the basis is forced by the data: every basis
that validates within 2 per cent on the closed cohorts files 133, every other misses a cohort by 7.97 per cent or
more. The prompt moves to `prompt.txt` and the pairing to Forecasting.

## Draw

| Axis | Draw |
|---|---|
| Card | `cards/task446.json`, repaired 2026-10-15: `guard.py heart` WARN (first names only); lineage keeps v1 and v2 loop 1 with their fates |
| Domain / task type | banking-credit-financial-risk / credit-scoring-pd-modeling, which serves Forecasting: the early-warning screen is a scoring system and the call is the twelve-month watch-list migration of the flagged and unflagged book |
| Objective | Forecasting & Predictive Modeling: a count for a window that opens on 1 October 2026 |
| Shape | 05 allocation to a fixed total: the caseload over five exposure bands (groups, committed exposure, expected arrivals flagged and not flagged, expected exposure arriving) with a total row |
| Gate G mechanism | forecasting |
| Gap / pattern | time then population / none; generators G16 (decisive), G13, G19 |
| Decision type | quantity_figure |
| Stump strategy | composition_mix; decisive rule filed: no (5.2 files the estimand only); official decoy: no; validated decoy: no |
| Calibration | existing_book_actuals: the bank's own four closed cohorts |
| Context artifact | filed_model (CRM-07, the monitoring standard) |
| Role, forum, forcing event | credit risk monitoring; the executive risk committee on 4 November 2026; the 2027 resourcing budget |
| World | United Kingdom, GBP, Halstow Bank plc; personas from `guard.py names --geo 'United Kingdom' --seed 446` |
| Layer 2 | forecast_uncertainty, own:screen-yield-under-a-moved-base-rate |

**Data-native sentence.** An early-warning screen on a credit book is judged by its hit rate, but how many flags
turn bad depends on how much of the book is deteriorating that year, and the bank's own cohorts show exactly that:
the capture and false-alarm rates sit still while the hit rate climbs in the year rates rose, so a year in which
the flagged share has jumped to 18.1 per cent is a year in which the hit rate measured on calmer years undercounts
the inflow.

**One line per source.** task445 (portal failure on a literal reading): avoided, no sentence here reads to 73.
The client's return: the decisive step must be a choice no clause makes, so 5.2 now names no model, window or
selection rule. `layer2-rigor-patterns`: a forecast validated out of sample, where the analyst's easy route files
a wrong answer.

## Default path

1. Roll each September publication in `ews_entity_signals_2022-09_to_2026-09.csv` up to obligor groups through the
   group register, the obligor master and the GLEIF consolidation records in force (CRM-07 2.2, 3.2): 165 of the
   913 groups in the 30 September 2026 book are flagged.
2. Build the four closed cohorts (4.1, 4.2) and match them to `watch_list_history_2020-01_to_2026-09.csv`.
3. Take the measures the committee is shown (4.3) over the cohorts taken together: hit rate 0.377 (157 of 416),
   and the share of unflagged groups reaching the list, 0.0142 (44 of 3,092).
4. Give each flagged group the hit rate and each other group the unflagged share, and sum over the book: 72.9.
5. File the caseload at the nearest whole group (5.3).

Ends on: 73 groups

Golden: 133 groups

## Stump sentence

A competent solver rolls the entity signals up to groups, builds the four closed cohorts and gives each flagged
group the share of flagged groups that reached the list over those cohorts taken together and each other group
the unflagged share, the hit and miss rates the committee is shown each November, and files 73 (Ends on); the step
that lands it there is carrying the hit rate onto a book whose flagged share has jumped to 18.1 per cent, when the
hit rate moves with each year's share of the book reaching the list (0.49, 0.33, 0.29, 0.38 across the cohorts)
and only the screen's capture and false-alarm rates hold; backing this year's arrival share out of the flagged
share through those two rates predicts every closed cohort within 1.6 per cent out of sample and gives 133.

## Three rules

- Task type: credit-scoring-pd-modeling in Banking, Credit & Financial Risk, which serves Forecasting & Predictive
  Modeling: the early-warning engine is a scoring screen and the call is the book's twelve-month watch-list
  migration, forecast from the screen's measured performance.
- Domain test: the deciding quantity is the watch-list inflow a bank sizes its workout caseload on, forecast from
  an early-warning screen's performance on obligor groups; credit risk monitoring reads a screen by its capture
  and false-alarm rates because the hit rate depends on how much of the book is deteriorating, and backs the
  year's arrival share out of the flagged share through those rates.
- Swap: "how many of our patients will be admitted next year, given this year's screening flags" keeps the algebra
  but loses the task: there is no obligor group built from entity signals through accounting consolidation, no
  watch list with a twelve-month cohort window and no committed book whose exposure the arrivals carry, so the
  conformance and the exposure bands have nothing to attach to.
- Layer 1: the engine's entity-level signals keyed by LEI or company number for borrowers and non-borrowing
  parents; GLEIF Level 1 and 2 files with lapsed registrations, successors, branches and fund links; the credit
  system's group register and watch-list history in its own namespace; a two-ledger facility extract at
  facility-and-obligor grain run after the 1 October start-of-day batch, a limit history stamped in UTC, customers
  not yet grouped. Each is what the bank's systems produce; none sits on the decisive step (asserted).
- Layer 2: forecast_uncertainty: a screen's yield measured in calmer years carried onto a year whose base rate
  moved; the forecaster has to see which measured property carries across years and validate it out of sample.
- Decisive step: forecasting through the screen's capture and false-alarm rates, which hold across the cohorts,
  with this year's share of the book reaching the list backed out of this year's flagged share, rather than
  carrying the hit rate, a property of each year's base rate, onto a year whose flagged share has jumped.
- Not semantics: every field, code and definition (the flag, the group, the cohort, the three measures) is read
  the same on the default path and the golden; the hit rate is correctly defined and correctly computed, and it
  is still the wrong thing to carry forward.
- Not rule application: CRM-07 5.2 files only what is forecast (the count and exposure for the book at the cohort
  date over twelve months); no clause names a model, a fitting window, a basis or a validation test, so executing
  every stated rule leaves the forecast to be built and the easy build files 73.
- Analyst test: a strong analyst who conforms every signal to its group and reads every clause of CRM-07
  correctly, then forecasts the easy way, the probability of reaching the list given flag status as the cohorts
  measured it, files the default path's Ends on, 73; only one who sees the hit rate moving with each year's base
  rate and validates out of sample reaches 133.
- Estimand: CRM-07 5.2 (with 4.1, 4.2, 5.1 and 5.3): the number of groups in the 30 September 2026 monitored book
  expected to reach the watch list by 30 September 2027, groups joining later left out, to the nearest whole
  group, in `early_warning_and_watch_list_standard.pdf`.
- No decoy: no performance report, prior forecast, memo or caseload figure ships; the hit rate is never stated as
  a number anywhere in the pack, and no sentence argues for it.
- No certified replay: no certified figure is reproduced to recover a method; the closed cohorts are evidence the
  forecaster validates against, and nothing tells them to.
- Lesson: a screen's yield belongs to the year it was measured in, so a forward count comes from the screen's
  error rates and the share it now flags; no build on file teaches it (nearest drivers 0.06).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 hit and miss rates | 4.3 defines the hit rate | no | yes, the default | no | no | yes | readable |
| R0b latest cohort | no | no | yes, freshest evidence | no | no | yes | readable |
| R2 trended on the flagged share | no | no | a regression reflex | no | no | no | readable |
| Capture and false-alarm, base rate backed out (decisive) | no: 4.3 defines the measures the committee is shown and never says which carries across years | no: no column holds a base rate or a probability | no: carrying the hit rate is the reflex | no: no control or corpus scores a basis; the cohorts do so only for a forecaster who back-tests | no | no: an inversion through two rates and this year's flagged share | silent |

## Semantic fork table

Membership under CRM-07 2.2 as amended after portal round 1, one row per edge the ultimate-parent clause touches
(asserted in `generator/checks.py` and in `solve.check_membership`).

| ID | Term | Golden reading | Alternative | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | an ultimate parent that is not booked | a member: 165 flagged at 30 Sep 2026, apex-only flags 6 / 5 / 3 / 5 / 6 by cohort | members only when booked or consolidated into the parent (the pre-amendment text): 159 flagged | 133 (132.77), but band arrivals move (under GBP 5m not flagged 6.5 to 7.0, GBP 5m to 15m flagged 34.0 to 31.9) | 2.2: "A group's members are its ultimate parent, ..." |
| SF2 | an ultimate parent the credit system books | a member, booked to its own register group (901 of 1,306, none to another group) | none: booked and named both make it a member | same call | the records converge (asserted) |
| SF3 | an ultimate parent with a GLEIF reporting exception | the register's ultimate parent is GLEIF's top: every apex files NON_CONSOLIDATING, NATURAL_PERSONS or NO_KNOWN_PERSON for both parent categories | a hidden consolidating parent above it | same call | no exception reason on an apex withholds a parent (asserted); 2.1 and the register name the parent |
| SF4 | an international branch of the ultimate parent (30 records) | read with its head office under 2.3 | left out as not a legal entity | same call | every branch of an apex is GREEN at every cohort date (asserted, branches off inert) |
| SF5 | an ultimate parent with its own direct parent | does not occur | the parent's parent as the top | same call | no apex is the start node of any consolidation record (asserted) |
| SF6 | the cohorts the screen's measures are taken over | the last four closed cohorts taken together | the latest cohort alone (126.8), the last three (132.4), the first three (135.0) | 127, 132 or 135 | 4.3 defines the measures over the last four closed cohorts taken together, and 1.2 keeps the engine unchanged since January 2022, so no cohort sits outside the regime (asserted) |
| SF7 | each band's arrivals by flag status (5.3) | the book's flagged and other arrivals shared in proportion to the band's groups of each status | per-status probabilities from the mean of cohort rates | same call, every band arrival figure in the same bin | asserted for the mean-of-rates variant; the regression bases give no per-status split |

## Ladder

Closed cohorts (built from the pack; counts retuned in loop 1): monitored 846 / 871 / 889 / 902; reaching the
watch list 75 / 43 / 36 / 47; flagged 119 / 98 / 95 / 104; flagged and reaching 58 / 32 / 28 / 39 (flagged and
not reaching 61 / 66 / 67 / 65). Hit rate 0.487 / 0.327 / 0.295 / 0.375; capture rate 0.773 / 0.744 / 0.778 /
0.830; false-alarm rate 0.0791 / 0.0797 / 0.0785 / 0.0760; share reaching 8.9 / 4.9 / 4.0 / 5.2 per cent; flagged
share 14.1 / 11.3 / 10.7 / 11.5 per cent. Taken together: hit 0.3774 (157 of 416), capture 0.7811 (157 of 201),
false-alarm 0.0783 (259 of 3,307), miss 0.0142 (44 of 3,092). Forward book at 30 Sep 2026: 913 monitored, 165
flagged (0.1807).

**The cohorts' out-of-sample record over the family** (each closed cohort predicted from the other three; worst miss
as a share of actual arrivals; forward figure). Nothing in the pack files this test: it is the validation a
forecaster runs, and it is how the data forces the basis.

| Basis | Set from the cohorts taken together? | Test misses 2022 / 2023 / 2024 / 2025 (per cent) | Worst | Forward |
|---|---|---|---|---|
| R0: share of flagged and of unflagged groups reaching (hit and miss) | yes | -36.0 / +15.2 / +40.6 / +10.3 | 40.6 | 72.92 (73) |
| one share for every group | yes | -46.6 / +21.4 / +55.6 / +13.4 | 55.6 | 52.31 |
| arrivals per flagged group, none from the rest | yes | -32.7 / +13.2 / +35.6 / +9.2 | 35.6 | 79.72 |
| R3: every flagged group reaches, the rest at the miss rate | yes | +69.7 / +153.5 / +198.4 / +147.9 | 198.4 | 175.64 |
| **Answer: capture and false-alarm, share reaching backed out of the cohort's flagged share** | yes | -0.2 / -1.6 / +0.5 / +1.1 | **1.6** | **133.04 (133)** |
| mean of cohort capture and false-alarm rates | no | 0.0 / -2.0 / +0.2 / +1.2 | 2.0 | 132.97 (133) |
| arrival share on flagged share, straight line (unweighted or by book size) | no | -0.5 / -2.0 / +0.8 / +1.4 | 2.0 | 132.83 (133) |
| arrivals on flagged count and book size | no | -0.6 / -2.0 / +0.7 / +1.4 | 2.0 | 132.84 (133) |
| R2: hit and miss trended on the flagged share | no | +8.0 / -2.9 / +3.4 / -0.2 | 8.0 | 146.72 (147) |
| mean of cohort hit and miss rates | no | -36.2 / +14.0 / +39.6 / +8.8 | 39.6 | 71.99 |
| R0b: the latest cohort's hit and miss | no (window) | -30.8 / +3.5 / +21.1 / -17.7 | 30.8 | 69.37 |
| R1: the most stressed cohort's hit and miss | no (window) | -30.8 / +53.1 / +80.2 / +47.6 | 80.2 | 97.91 |

Window violations of the answer's own basis: the latest cohort's capture and false-alarm alone 126.82, the last
three cohorts 132.44, the first three 135.01 (4.3 takes the measures over the last four closed cohorts, and 1.2 keeps the engine unchanged since January 2022; SF6).

| Rung | Reading | Figure | Killed by |
|---|---|---|---|
| R0 | the pooled hit and miss rates, the measure the committee sees | 72.9 (73) | the cohorts' own record: misses 2024 by 40.6 per cent against 1.6 |
| R0b | the latest closed cohort's rates | 69.4 | one year's arrival share carried forward; misses by 30.8 per cent out of sample |
| R1 | the most stressed cohort's rates | 97.9 | the same; misses by 80.2 per cent |
| R2 | hit and miss rates trended on the flagged share | 146.7 (147) | four parameters on four cohorts extrapolated past every flagged share they saw (10.7 to 14.1 per cent against 18.1); out of sample it misses by 8.0 per cent against 1.6 |
| R3 | every flagged group reaches, plus the unflagged miss rate | 175.6 | about 7.8 per cent of groups that do not reach are flagged every year (198 per cent out of sample) |
| Answer | 913 x (0.1807 - 0.0783) / (0.7811 - 0.0783) | **133.04 (133)** | |

- **Convergent routes (C1):** every basis that validates within 2 per cent out of sample forecasts 133: the pooled
  capture and false-alarm basis (133.04, 1.6), the mean of cohort rates (132.97), the straight-line fits of the arrival
  share on the flagged share (132.83 unweighted and weighted) and arrivals on flagged count and book size (132.84).
  Of these only the two capture and false-alarm bases give per-status probabilities for the band split (5.3); both land
  103.9 and 29.1 and every band arrival figure (asserted, SF7).
- **Probabilities:** this year's share reaching 0.14571; flagged 0.62978 (63.0 per cent), not flagged 0.03893
  (3.9 per cent); expected arrivals 103.91 flagged and 29.12 not flagged.
- **Satisfying to stop at.** R0 is the measure the standard reports, applied as it reads; R0b is the freshest
  evidence; R1 is the "use a stressed year" instinct; R2 is the half insight with a decent test score.
- **Direction.** R0, R0b and R1 sit below the answer, R2 and R3 above. Nearest natural rung: R2 at +10.3 per
  cent. The base rate with no flags (52.3) and flagged arrivals only (79.7) are bases the test refuses.
- **Bins.** 133.04 sits 0.46 from the nearer edge (the call moves only if expected arrivals rise by 0.46 groups);
  103.91 and 29.12 sit 0.4 and 0.3 of a bin from theirs.
- **The decisive move against the seven properties.** 1 no sentence states it (5.2 files the estimand only); 2
  the closed cohorts score it only for a forecaster who validates out of sample, an analysis no clause asks for; 3 no
  arithmetic symptom: R0 reconciles to every count it uses; 4 not a row predicate: a property of the whole cohort
  table; 5 the enumeration is algebra over four cohorts; 6 no cutover date (2022's high rate is a cycle, not an
  event); 7 survives deletion (nothing is wrong).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | monitored book: active on the register and not on the watch list at 30 Sep (4.1); later joiners out (5.1); C1: no register or watch-list date within 8 days of a cohort date |
| 2 | Unit | obligor group; members = the ultimate parent, booked customers and GLEIF accounting-consolidation members in force at the date (2.1, 2.2 as amended after portal round 1); pinned at authority: 2.2 names the ultimate parent a member, so its literal reading counts the 6 / 5 / 3 / 5 / 6 apex-only flags and gives 165 flagged (the pre-amendment reading, 159, moves band arrivals; SF1 to SF5); C1: every flagged entity's membership stable across all cohort dates |
| 3 | Attribution window | placed in the twelve months after the cohort date (4.2); C1: no placement within 8 days of a window edge |
| 4 | As-of dating | the September month-end publication; relationship periods covering the date; asks: limits as they stood at the end of 30 Sep UK time (1.3, 6.1) read from a history stamped in UTC (field reference) |
| 5 | Version basis | one publication per month-end; asks: the limit version in force at the end of 30 Sep (6.1), not the extract's limit at its 01:15 run on 1 Oct |
| 6 | Denominator | the three measures' denominators filed (4.3); 5.2's estimand is a count of groups, so a miss is read on arrivals |
| 7 | Weighting | the four cohorts taken together, as 4.3 measures them; mean-of-rates converges on the call, both arrival totals and every arrival figure (asserted, SF7) |
| 8 | Window length | the last four closed cohorts (4.3), the engine unchanged since January 2022 (1.2); latest-alone 126.82 and three-cohort 132.44 and 135.01 take the measures off 4.3's definition (SF6, asserted) |
| 9 | Inclusivity | band edges "and under" (6.2); C1: no group within GBP 0.25m of an edge on the right path |
| 10 | Rounding path | unrounded throughout; whole groups to the nearest (5.3); one decimal on report; every graded figure at least 0.25 of its bin from an edge (asserted) |
| 11 | Tie-break | none needed: every validated basis files 133 |
| 12 | Maturity | a cohort is closed once its twelve months have ended (4.2); 2025's window ends 30 Sep 2026 and the history runs to that date; C1: no placement after 30 Sep 2026 in the history |
| 13 | Order of operations | flag at group level before counting; convert each facility to sterling before summing; collect a group's facilities before summing |
| 14 | Row order | irrelevant on the right path; the whole-extract de-duplication stops depend on it and both orders are asserted off the golden |
| 15 | Duplicate resolution | a group counts once per window (4.2); a facility counts once in each group with an obligor on it (6.1) |
| 16 | Identity | LEI case-normalised; CRN keys through the company number; merged LEIs green (inert); a facility is its booking entity and ledger number |
| 17 | Netting | none |
| 18 | Units | limits in facility currency; rates in `units_per_gbp` (inert) |
| 19 | Code semantics | AMBER and RED flag, GREEN does not (3.2); every watch level is on the list; CANCELLED and CLOSED facilities carry a nil limit in the extract and in the history's version in force (C1 on any status reading) |
| 20 | Integerisation | nearest whole group (5.3); 133.04 sits 0.46 from the nearest edge |
| 21 | Clause scope | 5.2 files the count and exposure for the whole book; 5.3 splits each band's arrivals by flag status in proportion to its groups and their exposure (a reporting convention for the asks); scores within a colour and bands carry no signal beyond the flag (built so), so a finer model converges |
| 22 | Forward window | the 30 Sep 2026 monitored book only (5.1, 5.2); every group in it carries at least one facility in force at the end of 30 Sep 2026 (asserted) |
| decisive | The basis | design-forced, C3: 5.2 names none; every basis that validates within 2 per cent out of sample files 133, every other misses a cohort by 7.97 per cent or more (asserted) |

## Literal reader

Executing the prompt and CRM-07 word for word, a reader computes the expected number of the 913 groups in the 30
September 2026 monitored book (4.1, later joiners out under 5.1) placed on the watch list by 30 September 2027
(4.2, 5.2), to the nearest whole group (5.3). The text names no model, window or basis, so every forecasting basis
the cohorts support is an option: each one that validates within 2 per cent when each closed cohort is predicted
from the other three files 133 (the pooled and mean capture and false-alarm bases, the straight-line fits of the
arrival share on the flagged share, arrivals on flagged count and book size); every other misses a closed cohort
by 7.97 per cent or more. The easy 73 comes from an easy method on the same literal estimand, the hit rate carried
onto a moved base rate; no sentence in the pack, read literally, gives it.

## Oracles

None. No performance report, published forecast or prior caseload ships; the agenda names the meeting and its
item, not a figure. The closed cohorts are the forecaster's evidence, not a control that ties only under the
golden: they score every basis, and a solver has to think to score them.

## Ask sheet

**Main call's declared row population** (the zero-counts run against it): the five September publications
(2022-09-30 to 2026-09-30) in the signal file; the GLEIF LEI-CDF and RR-CDF rows of every entity carrying AMBER
or RED in any of them, and of its parents up the consolidation chain; the obligor master rows whose LEI or
Companies House number matches such an entity; every group register row (group, ultimate parent LEI, relationship
dates); every watch-list history row. Device and hazard rows: every row of the facility-obligor extract, the
limit history and the rates file (outside by file); the obligor master and GLEIF rows of the not-yet-grouped
customers, each GREEN in every September publication (asserted zero inside); no device writes a register,
watch-list or September-publication row (asserted by building the main-path files with and without the devices and
comparing bytes).

**The asks** (one band table in `watchlist_inflow_2027.xlsx`, its arrival columns drawn in the chart):

| Column | Figures | Construction | Devices on the path | Use |
|---|---|---|---|---|
| Groups the band holds | 5 counts, total 913 | each group's committed exposure at 30 Sep 2026 (6.1), banded (6.2) | DV-A, DV-B, HZ-C | how the book splits between Restructuring (GBP 40m and over) and Business Support, read against 3.2's headcount |
| Their committed exposure | 5 in GBP m, total | the band's sum of group exposures | DV-A, DV-B, HZ-C | the agenda's "committed exposure by caseload band" |
| Expected arrivals, flagged | 5, total 103.9 | the book's flagged arrivals shared by the band's flagged groups (5.3), 0.62978 each | DV-A, DV-B through band membership | caseload by team |
| Expected arrivals, not flagged | 5, total 29.1 | the book's other arrivals shared by the band's other groups (5.3), 0.03893 each | DV-A, DV-B through band membership | manual-review capacity |
| Expected exposure arriving | 5 in GBP m, total | probability x committed exposure | DV-A, DV-B, HZ-C | what the arriving caseload carries |

The groups and committed-exposure columns need nothing from the main call; the arrival and arriving-exposure
columns carry the main construction (a response on the naive model loses all fifteen whatever it does with the
devices) and every device. The two arrival totals and 913 are the only ask figures the devices do not reach.

**Device ledger** (none from architecture 1's families D2, D3, D4; architecture 2's stage 3 devices retired):

- **DV-A, primary, facility-and-obligor grain (D6, with a D7 over-cleaning half and stated non-additivity).**
  Root cause: the credit data warehouse's facility-obligor table, fed by two loan ledgers that number facilities
  independently; LMA facilities with several borrowers in one group; joint property facilities whose borrowers
  sit in two monitored groups. The extract carries one row per facility per obligor with the facility's committed
  limit repeated on each row. Right: within each group, each (booking entity, facility number) once; a joint
  facility counts in both groups (6.1, "the facilities on which one or more of its members is an obligor").
  Wrong stops: A1 every row summed (multi-obligor groups move up); A2 each facility number once across the whole
  extract (HB-DAC facilities whose numbers coincide with HB-PLC numbers, and one group of each joint facility,
  drop); A3 each booking entity and number once across the whole extract (one group of each joint facility drops).
  Organs: 6.1 and the records (identical attributes across a facility's obligor rows; coinciding numbers differ in
  booking entity, currency, dates and obligors; the limit history keyed by booking entity and number). Silent:
  (booking entity, facility, customer) is unique, every customer joins, nothing states a facility count. Scale:
  about 12 per cent of facilities with 2 to 4 obligors in one group; 15 to 20 joint facilities (sector RE); about
  40 coinciding ledger numbers.
- **DV-B, primary, the limit clock (D8).** Root cause: the extract was held for the Dublin ledger close and ran
  at 01:15 on 1 October, after the start-of-day batch; the loan platform stamps limit versions in UTC; the
  batch runs at 00:30 UK time, so in BST it stamps 23:30Z on the previous date. The 1 October batch applies about
  70 limit increases approved in September with effect from 1 October and activates about 12 facilities
  available from 1 October, all stamped 2026-09-30T23:30:00Z, and closes the facilities maturing on 30 September.
  Right: each facility's version in force at 2026-09-30T23:00:00Z (the end of 30 September UK time). Wrong stops:
  B1 the extract's committed_limit (the 1 October increases in, up); B2 the history read on its UTC date (the same
  rows in, up); B3 the latest version in the history (the 2 to 7 October changes in as well); B0, over-cleaning,
  versions dated before 30 September only (increases keyed in the day on 30 September drop, down). Organs: 1.3 and
  6.1, the field reference's "UTC", the history records; referee: the extract log's run time. Silent: one version
  per facility is selected under any reading and nothing fails. Blending: the batch stamps every day of the year
  (23:30Z in BST months, 00:30Z in GMT months) and users key amendments in the day, so no column isolates the
  1 October rows.
- **HZ-C, hazard, customers not yet grouped (D7).** Root cause: about 14 customers the HB-DAC ledger created in
  September 2026, which the monthly grouping review has not yet booked (group_id blank), each with an LEI whose
  GLEIF consolidation, in force at 30 September 2026, runs to a monitored group's ultimate parent; 2.2 makes them
  members. Wrong stop: their facilities dropped with the blank group (down). Each is GREEN in every September
  publication.

**Movers** (distinct groups per device; each edge in GBP 5m, 15m, 40m, 100m order): A1 up across the four edges
1, 3, 1, 3 flagged and 3, 7, 3, 7 not flagged; B2 up across the four edges with the same counts on other groups;
A2 and A3 down through the joint facilities and coinciding numbers; B0 down across every edge; HZ-C down across
the 15m and 40m edges (2 flagged, 6 not flagged). Every band's flagged count then moves by at least one and its
unflagged count by at least three under A1 and under B2, so every arrival figure leaves its bin (a flagged group
is 0.63, three unflagged 0.12).

**Assertions for the builder.**
1. Zero device and hazard rows inside the declared population, the counts written into this ledger.
2. A1 alone and B2 alone each move all 25 band figures and both exposure totals out of their bins; A2, A3, B1,
   B3, B0 and the HZ-C drop each move at least 15 of the 25 and the committed-exposure total.
3. The device grid (A at four stops, B at five, HZ-C at two): every cell but the all-correct one misses the golden
   on at least 15 of the 25 band figures and on the committed-exposure total by at least GBP 5m; no subset of
   mishandlings cancels back onto a golden figure.
4. Fairness: the right handling reproduces the world's own group exposures exactly.
5. The hygiene battery on every wrong path runs clean (unique keys at the extract's grain, every customer joins
   the master, the history joins on booking entity and number without fan-out).
6. The over-cleaners (A2, A3, B0) each land on their own off-golden values.
7. Every band figure at least 0.25 of its bin from an edge; every group in the book has a facility in force.

**Pair arithmetic, stated plainly** (planning weights 38/7/55, about 50 criteria: the call, 4 components and 8
steps in the 38; the heading, 25 band figures, 5 totals and 4 chart parts in the 55). A response that lands 133
keeps the recommendation, instruction following, the heading, 913, both arrival totals and the chart's structure,
about 58, and about 100 only if it clears every device. A response on 73 keeps the book components and the
conformance steps, instruction following, 913 and the chart's structure, about 27, and about 44 if it clears every
device (the groups and committed-exposure columns). Pairs: no response on 133, 27 to 44; one on 133 missing a
device beside one on 73, about 42 to 51; one on 133 clearing every device, about 63 to 72, which fails. The pass
condition rests on the main ladder keeping the top two off 133; the devices hold a response that lands it near 58.
For the writer: the critical components should carry the decisive construction (the test's result, the share
reaching implied by the flagged share, the two probabilities) with the book and flag counts as one component, so a
response on 73 keeps as little of the 38 as the analysis allows.

| Ask figure | Where the cracker's path goes | Mirror (stops at R0) | Cracker (lands 133, runs the battery) |
|---|---|---|---|
| Groups and committed exposure (10) | sums every extract row, or reads the limit as extracted on 1 October | misses the same way | miss |
| Expected arrivals, flagged and not (10) | carries the band membership the devices moved | misses (and on the 73 basis) | miss |
| Expected exposure arriving (5) | the same membership and the same limits | misses | miss |
| Total row's committed and arriving exposure (2) | the same membership and limits as the rows | misses | miss |

- **Main-path figures in the ask layer:** the heading, the 913 and the two arrival totals (103.9, 29.1) sit on the
  call's own construction and no device reaches them: whoever lands 133 keeps them, the mirror on 73 loses all but
  913. They are counted in the pair arithmetic, not in the device table.
- **Cracker keeps:** about 0.23 of the ask weight (those main-path figures and the chart's structure); the band rows
  go with any one device.
- Mirror leakage: 11 per cent of ask weight (913 and the chart's structure; the arrival totals sit on the call's
  basis).
- Pair ceiling: 37.9 (C = 38 + 7 + 55 x 0.23 = 57.6; S = 5 + 7 + 55 x 0.11 = 18.1; mean 37.9).

## Layers

- **Layer 1 (main path, conformance the standard files):** entity signals keyed by LEI, or by
  `CRN:` and company number for entities without an LEI; non-borrowing members (parents, sisters)
  reached through GLEIF accounting-consolidation records whose period covers the cohort date; the
  credit system's own customer and group namespace; every watch level is on the list; groups already on the list
  excluded; groups leaving the book count as not reaching. GLEIF texture on the main path (lapsed registrations,
  merged LEIs still in the vendor feed, international branches, fund-management links, reporting exceptions) sits
  on entities whose signals are green at every cohort date, so mishandling it moves nothing (asserted).
- **Layer 1 (ask paths, ledgered devices):** the facility-obligor grain, the UTC limit clock and the
  not-yet-grouped customers below.
- **Layer 2:** a screen's yield measured in calm years is carried onto a stressed year; the yield
  depends on the base rate, the screen's error rates do not.

## Gate G

- **Litmus.** No reported number in the pack is wrong and nothing is overturned. The early-warning
  signals, the watch-list history, the group register and every extract are correct for the dates they
  describe; the hit rate the standard defines is the right hit rate for the cohorts it was measured on.
  The difficulty is that a hit rate is a property of the year it was measured in, and the call is about
  a year whose flagged share sits far outside the history.
- **Mechanism:** forecasting: the standard files the estimand only; the decisive step is the forecaster's own
  choice of what carries across years (the screen's error rates, not its yield), validated on the closed cohorts,
  with this year's arrival share backed out of the flagged share.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Delete every wrong number:** there are none to delete. Repair every file at source (the facility
  extract read at its proper grain and as at the end of 30 September, every customer grouped) and the call and
  the naive figure do not move, because no facility, limit-history or rates row is on the call's path (asserted).
- **Lens swap:** no. The naive figure and the answer are the same book under two forecasting models:
  the naive carries P(arrival | flag status) from calmer years, the answer carries P(flag | outcome)
  and backs the year's share reaching the list out of the flagged share; the cohorts' out-of-sample record separates them.
- **No artifact ranks or forecasts.** No performance report, no prior forecast, no prior caseload
  figure ships. The standard defines the three measures and the group-flag rule.
- **Guard, 2026-10-15 repair.** `heart` WARN only (first names Victor and Dennis in older builds). The pairing
  moved to credit-scoring-pd-modeling with Forecasting (no banking task type serves ETL); the stump strategy key
  moved to composition_mix (the hit rate is a property of each year's mix); differentiation lines on the card answer
  task127, task138, task254, task501 and this slot's own lineage.

## Pre-ship check

1. Domain: credit risk monitoring's own reading of an early-warning screen (capture and false-alarm rates hold,
   the hit rate moves with the base rate); with a hospital screen's nouns the group roll-up, the watch-list cohort
   and the committed book have nothing to attach to.
2. Real work, nothing planted: every Layer 1 item is what the bank's or GLEIF's systems produce; none is on the
   decisive step (asserted).
3. The step that flips the call is analytical: which measured property of the screen carries across years,
   validated on the closed cohorts; no clause makes the choice.
4. Analyst test: every field and rule read correctly, the easy forecast files 73 (asserted as R0 in `checks.py`).
5. 5.2 files the estimand only (asserted: no model, window or selection wording in the standard); every validated
   basis converges on 133.
6. No decoy, no withheld rule against a stated one, no certified replay.
7. The lesson is on no other card: nearest drivers 0.06.

## Realism debts

- A share reaching the list of 14.6 per cent of the monitored book in one year is a stress year (the
  closed cohorts run 4.0 to 8.9 per cent). It is what the flagged share implies, and the flagged
  share's jump is the forcing fact; the signal file shows it in the trigger mix (payment delays and
  rating actions), not in coverage or engine version.

## Realism repairs for the loop 1 rebuild (the reader's tells and golden-realism)

1. **Containers.** The agenda is built from a Word-authored skeleton (styles, theme, settings and font table as
   Word 16 writes them, app.xml with Template Normal.dotm, TotalTime, Pages, Words, Characters, Company Halstow
   Bank plc, AppVersion 16.0000), never python-docx's default template. Every input workbook carries a full Excel
   app.xml (DocSecurity, ScaleCrop, HeadingPairs and TitlesOfParts naming its real sheets, Company, LinksUpToDate,
   SharedDoc, HyperlinksChanged, AppVersion 16.0300). Core stamps follow each file's own story: the register,
   written by the Reference Data job at 05:05Z on 1 October (created equal to modified, as a job writes it); the
   rating master scale, Credit Risk Models, created 2025-12-12, modified 2026-10-02; the outlook, Group Economics,
   created 2026-10-05, modified 2026-10-06; the agenda, created 2026-10-07 by the Company Secretariat and last
   modified 2026-10-08 by a named secretariat officer, revision 4. Asserted: no two input containers share a
   created stamp, and the producer-metadata audit is clean.
2. **Standard 2.3** is the general sentence above, not a list of the pack's edge cases (the GLEIF texture is
   inert on the main path, so no fork opens).
3. **RED through the year.** Signals draw RED month by month within a flagged episode (rising towards a
   watch-list entry, with a steady RED share among flagged entity-months), never as a September draw; asserted:
   each September's RED count lies within 15 per cent of the mean of its August and October.
4. **Row order.** The facility extract is sorted by booking entity, facility number and customer, device
   facilities draw their numbers from the same ledger sequences, and the facilities maturing on 30 September show
   CLOSED with a nil limit (the 1 October batch closed them); asserted: no run of more than 3 consecutive device rows, and device rows'
   mean position between 40 and 60 per cent of the file.

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
- Chart deliverable as a PNG (stage 3): the xlsx-plus-png set is shared by task87, task100 and task130, and the surface screen promoted all three on deliverable species, layout and format mix alone; the chart ships as an SVG with its text kept as text.
- Standard 5.2 as filed at architecture 2 stage 3 ("a probability of reaching the watch list that depends only on its flag status at the cohort date and is the same across the book. It is set from the performance measures in 4.3"): read literally, the flagged probability is the cohorts' hit rate, so the filed text gives about 74 against the golden 134; the stage 4 reader sized it as a main-call fork, it is the defect the portal failed task445 on (answer_contradicts_files, golden_wrong) and an official decoy on the card's terms. Replaced in loop 1 by a 5.2 that files the estimand and the leave-one-cohort-out test that selects the basis and names no basis.
- Architecture 2's stage 3 ask devices: the superseded scheduled plc run (D2), the HB-DAC file delivered on its own (D4) and closing rates quoted per pound (D3) were re-skinned from architecture 1's set, which its round-1 solver cleared in full (asks 3 of 3 at 80 per cent of tokens), and facilities maturing on the cohort date still ACTIVE (D8) were executed by any reader of 6.1's maturity sentence (and sat as the last 25 rows); with CANCELLED and CLOSED rows carrying their last limit, 6.1 also left the status reading open (18 groups between bands). Replaced in loop 1 by the facility-obligor grain, the UTC limit clock and the not-yet-grouped hazard, with cancelled and closed limits nil in the records.
- Stage 3 cohort counts under loop 1's test (flagged and reaching 58/33/28/39, flagged and not reaching 60/64/66/63): the pooled basis lost the test to the mean of cohort rates (2.5 against 1.9 per cent), whose unflagged total sat in another bin (28.5 against 28.7). The first retune tried (59/34/28/39 and 60/64/66/64) put the straight-line fit of the arrival share at 131.49 against the pooled 131.92, on a bin edge and a different whole number. Retuned to 58/32/28/39 and 61/66/67/65, where every convergent route lands in the 133 bin with at least 0.33 of margin.
- CRM-07 2.2 as shipped ("the customers the credit system books to it and every legal entity whose GLEIF relationship record shows it accounting-consolidated into the group's ultimate parent"), portal round 1, 2026-10-11: read literally it leaves out an ultimate parent that is neither booked nor consolidated into itself, giving 159 flagged against the golden's 165 and moving every band arrival figure past its bin (the headline 133 held). Pinned at authority by amending 2.2 to name the ultimate parent a member; convergence would have moved main-call rows.
- CRM-07 5.2 as shipped after loop 1 (the model, the fitting window and the leave-one-cohort-out selection filed),
  returned by the client on 2026-10-15 on the 10/10 rule-application rule: once the cohorts were built the solver
  ran a stated procedure, and the in-task blocks' own fork ledger closed the basis fork by quoting 5.2. Repaired in
  place: 5.2 files the estimand only, 5.3 carries the band split as a reporting convention, the data's own
  out-of-sample record forces the basis (every validated basis files 133); figures unchanged.
- The prompt as `prompt.md` (three paragraphs, the role in the opening sentence): replaced by a one-paragraph,
  question-first `prompt.txt` at the 2026-10-15 repair.
- The pairing etl with subdomain other (no banking task type serves ETL): retagged to credit-scoring-pd-modeling
  with Forecasting at the 2026-10-15 repair.
