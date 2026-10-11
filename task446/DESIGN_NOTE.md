# task446 design note (architecture 2, loop 1)

Seed ET03 (GLEIF LEI-hierarchy issuer-group concentration, Data Extraction & Conformation). Architecture 1
(obligor-group house-limit projection on the projection-date membership) was spent at solver round 1 as a
rule-application stump (see the tried-and-rejected section and `solver_rounds/round-1.md`). Architecture 2
keeps the number, the objective and the seed's world (the GLEIF consolidation hierarchy carrying entity-level records up
to obligor groups, a UK bank's own systems) and draws a new decision and a new Layer 2 pitfall.

Loop 1 is a designer pass before any solver round on architecture 2. The stage 4 reader found that the
standard's 5.2 filed a basis ("set from the performance measures in 4.3") whose literal reading is the pooled
hit rate, about 74 against the golden 134: the defect the portal failed task445 on (`answer_contradicts_files`)
and an official decoy on the card's terms. Loop 1 files the estimand and the test that selects the basis, names
no basis, retunes the cohort counts so the test separates the bases widely, redraws the ask devices off
architecture 1's families, and lists the realism repairs. The builder executes the brief at the end of this note.

## DRAW

| Axis | Draw |
|---|---|
| Card | `cards/task446.json` v2, refiled 2026-10-11 for loop 1: `guard.py check` WARN (repeat.gate_g, overuse.gate_g, answered under Gate G), `heart` WARN, nearest driver 0.07; v1 kept in `lineage` with its fate |
| Domain / task type | banking-credit-financial-risk / other: early-warning and watch-list monitoring of corporate obligor groups (client domain Banking, Credit & Financial Risk) |
| Objective | Data Extraction & Conformation (ETL): four closed annual cohorts and the live book built from an early-warning engine's entity-level monthly signals, carried to obligor groups through the credit system's group register and the GLEIF consolidation hierarchy, matched to the watch-list history; committed exposure conformed from a two-ledger facility extract and its limit history; the forecast runs on the conformed cohort table |
| Shape | 05 allocation to a fixed total: the caseload allocated over the five exposure bands, each band with the groups it holds, their committed exposure, expected arrivals from flagged and from unflagged groups and the expected committed exposure arriving, with a total row |
| Gate G mechanism | method_or_model_selection (the basis the filed test selects), with forecasting support (a forward count for a window that has not opened) |
| Gap / pattern | time then population / none; generators G16 (decisive), G13, G19 |
| Decision type | quantity_figure (count: obligor groups the 2027 watch-list caseload plans for) |
| Stump strategy | forecast_method_backtest; decisive rule filed: no (the criterion that selects the basis is filed, the basis is not); official decoy: no; validated decoy: no |
| Calibration | existing_book_actuals: the bank's own four closed cohorts, on which the filed test is run |
| Context artifact | filed_model (the early-warning and watch-list monitoring standard) |
| Role | head of credit risk monitoring (portfolio_manager family); forum committee_or_panel (executive risk committee); forcing event budget_or_appropriation (2027 resourcing budget); org financial_institution |
| As of | 2026-10-11, the request (data as at 30 Sep 2026, pack compiled 8 Oct 2026; the agenda carries the 4 Nov meeting) |
| World | United Kingdom, GBP, Halstow Bank plc; personas Jill Berry, Mathew Long (`guard.py names --geo 'United Kingdom' --seed 446`) |
| Layer 2 | forecast_uncertainty, own:screen-yield-under-a-moved-base-rate |
| Layer 1 | entity signals keyed by LEI or company number including non-borrowing entities; GLEIF L1/L2 with relationship periods, lapsed registrations, successors, branches, fund-management links; the credit system's group register and watch-list history in its own namespace; a two-ledger facility extract at facility-and-obligor grain run after the 1 October start-of-day batch, a limit history stamped in UTC, and customers not yet booked to a group (ask paths only) |

**Similarity claim.** No build on file turns on which of a screen's measured properties carries to a year with
a different base rate. Nearest drivers sit at 0.07 and below (task57 v19 held-out year, task89 v11 forward roll,
task51 decomposition). Rejected neighbours this draw passed through are recorded in `## Loop 1 build (builder, 2026-10-11)

Built to the brief; `generator/checks.py` green (9,147 assertions), `solve.py` reproduces every figure from
`target/`, two builds byte-identical, `target.zip` cut last. Call 133 (133.04); 5.2's test over the 13 bases as the
table above (capture and false-alarm 1.57 per cent, next 2.00, every non-convergent basis 7.97 or more), the five
convergent routes in the 133 bin, the mean-of-rates variant on 103.9 / 29.1 and every band arrival figure. Band row:
201 / 306 / 250 / 120 / 36 groups; committed GBP 475.8m / 3,016.2m / 7,153.8m / 8,213.8m / 6,640.9m (25,500.5m);
arriving GBP 69.6m / 411.5m / 1,108.6m / 1,121.5m / 1,283.4m (3,994.6m); every figure 0.25 of a bin or more from an
edge, rounded rows tie to the rounded totals.

- **Devices as built.** A1 and B2 move all 25 band figures (crossers 1/3/1/3 flagged, 3/7/3/7 unflagged at the four
  edges); A2 20 and 21 (first and last row kept), A3 20 and 20, B1 25, B3 25, B0 24, HZ-C 18; committed-total moves
  A1 +3,594.7, A2 -509.4 / -412.8, A3 -129.1, B1 and B2 +252.9, B3 +257.7, B0 -237.4, HZ-C -64.6 (GBP m). All 59
  grid cells miss at least 15 band figures and the committed total by GBP 5m or more. A3's crossers are 2 flagged
  and 6 unflagged across the four edges, with partners chosen to cross under the last-row order too; B0's are 2
  flagged and 12 unflagged; HZ-C's 1 flagged and 4 unflagged at GBP 15m, 1 and 2 at GBP 40m, plus 6 non-crossers
  in four bands. 43 coinciding ledger numbers; 11.6 per cent of facilities carry two to four obligors.
- **Readings fixed by the build.** B1 and B2 are numerically one stop (nothing is stamped between 23:30Z and the
  01:15 BST run). The 1 October activations and the facilities maturing on 30 September are inert under every reading
  that applies 6.1's start and maturity sentence. The not-yet-grouped customers are outside the engine's coverage (no
  publication rows), so no device writes a September-publication row; the register, the watch list and the September
  rows are byte-identical with the devices off (asserted). Device-row spacing is asserted at facility grain (no run of
  more than three device facilities; mean position 0.40 to 0.60), since a four-obligor facility is four rows by itself.
- **leak.py (REVIEW, no LEAK), answered.** "the model" is the Model Risk Committee in 1.2. "5.2" is the clause number
  the write-up cites. The standard carries the call's words because it files the estimand (by design, the literal
  reading). Stump-paragraph terms in the standard, field reference and log are the domain's own nouns; none names the
  basis. Dates after 2026-10-11 in the facility extract are final maturity dates (forward by design).
- **Personas.** User ids in the limit history come from the seed-446 name draw (Jade Ali replaces a first name the
  guard warned on); the secretariat officer on the agenda is Abbie Stevens. Card updated.

## Pre-ship check (client two-layer standard)

- Domain: credit risk monitoring; the field's own early-warning performance measures (capture, false alarm, hit rate) and the base-rate dependence of the hit rate decide the caseload; with another field's nouns the screen's error rates and the cohort structure do not exist.
- Layer 1: group membership through the credit system and GLEIF consolidation (lapsed holdcos, a branch, fund links, a direct-only parent, CRN-keyed members), facility rows repeated per obligor, a limit history stamped in UTC with a start-of-day batch, a superseded extract run, FX quoted per pound; all real system behaviour, none on the main call's rows (asserted).
- Decisive step: a method choice (which basis carries the screen onto a year whose flagged share jumped), forced by the filed 5.2 test on the closed cohorts; not a planted catch, not a field reading, not a stated rule applied (5.2 names no basis).
- Analyst test: a strong analyst who reads every field and rule correctly and runs 5.2's test over the bases it reaches for (the hit and miss rates, a single book rate) files 73 (round 2 did exactly this); the capture and false-alarm basis gives 133.
- Estimand pinned: 4.1, 4.2 and 5.1 (book, outcome, exclusions) and 5.2 (one probability per flag status, the basis with the smallest largest leave-one-out miss); the literal reading gives 133 (judge, literal reading first).
- No decoy memo, no withheld rule, no certified record blessing a method; the lesson is not one an earlier build teaches (pre-flight: Track B clean; one soft Track A shape echo repaired by the distractor rename).
- Judge: DETERMINISTIC, APPROVE, no FIX_NOW.

## Tried and rejected`.

## Stump sentence

A competent solver rolls the entity signals up to groups, builds the four closed cohorts and sets the
probabilities from the share of flagged and of unflagged groups that reached the list over those cohorts taken
together, the hit and miss rates the committee is shown each November, and files 73; one who runs the
standard's test, sees that basis miss the 2024 cohort by 40.6 per cent and trends the hit and miss rates on the
flagged share (worst miss 8.0 per cent) files 147; only the basis that backs each year's share of the book
reaching the list out of that year's flagged share through the capture and false-alarm rates, which hold
across the cohorts, predicts every closed cohort within 1.6 per cent, and it gives 133.

## Data-native sentence

An early-warning screen on a credit book is judged by its hit rate, but how many flags turn bad depends on how
much of the book is deteriorating that year, and the bank's own cohorts show exactly that: the capture and
false-alarm rates sit still while the hit rate climbs in the year rates rose, so a year in which the flagged
share has jumped is a year in which the hit rate measured on calmer years undercounts the inflow.

## Literal reader

Executing the prompt and CRM-07 word for word, a reader computes the expected number of the 913 groups in the
30 September 2026 monitored book (4.1, with later joiners out under 5.1) that are placed on the watch list by
30 September 2027 (4.2), as the sum of one probability for the 165 flagged groups and one for the 748 others
(5.2), on the basis that, set in turn from three of the last four closed cohorts taken together and applied to
the fourth cohort's book and flags at its date, has the smallest largest miss (5.2), rounded to the nearest
whole group (5.3). The text names no basis. Of every basis that can be set from the cohorts taken together, the
share of flagged and of unflagged groups reaching the list misses the 2024 cohort by 40.6 per cent, and the
capture and false-alarm rates applied to each cohort's own flagged share miss no cohort by more than 1.6 per
cent, so the literal reading is 133. The easy 73 comes only from an easy method (the pooled hit and miss rates
applied without the test 5.2 requires); no sentence in the pack, read literally, gives it.

## The three rules

- **Domain test.** The call is a credit-monitoring forecast, the watch-list inflow a bank sizes its workout
  caseload on, from an early-warning system's performance on obligor groups (signals raised on any legal entity
  and carried to the group through accounting consolidation, a twelve-month watch-list outcome, the committed
  book as the monitored population). With another field's nouns in, the group roll-up of entity signals, the
  watch-list window and the committed-book population have nothing to attach to.
- **Two layers.** Layer 1: an early-warning engine that publishes monthly signals per legal entity by LEI
  (borrowers and the non-borrowing parents and sisters the vendors cover), the GLEIF concatenated files with their
  real behaviour, the credit system's group register and watch-list history in its own customer namespace, and on
  the ask paths a two-ledger facility extract and limit history with the mess two loan platforms produce. Layer 2:
  a screen's past yield is carried onto a year whose base rate has moved; the yield is a property of the year,
  the error rates are the screen's, and the filed test on the cohorts shows it.
- **Decisive step class: analytical.** Analyst test: a strong analyst who conforms every signal to its group
  correctly and reads the standard's book, outcome, cohort and test clauses correctly sets the flagged and
  unflagged probabilities first from the share of each that reached the list over the four cohorts taken
  together, because that is the probability of reaching given flag status as the cohorts measured it; that easy
  method gives 73, its test miss is 40.6 per cent, and an analyst who then searches only among rates measured on
  flag status (latest, most stressed, trended on the flagged share) still files 69, 98 or 147, because the hit
  rate is a property of each year's share of the book reaching the list, which this year's flagged share puts far
  above every closed cohort.

## Gate G

- **Litmus.** No reported number in the pack is wrong and nothing is overturned. The early-warning
  signals, the watch-list history, the group register and every extract are correct for the dates they
  describe; the hit rate the standard defines is the right hit rate for the cohorts it was measured on.
  The difficulty is that a hit rate is a property of the year it was measured in, and the call is about
  a year whose flagged share sits far outside the history.
- **Mechanism:** method_or_model_selection: the standard files the estimand and the test that selects the
  basis, and the decisive step is constructing the basis that passes it (this year's share of the book
  reaching the list backed out of the flagged share through the two rates that hold across cohorts).
  Forecasting is the vehicle (a forward count for a window that has not opened).
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Delete every wrong number:** there are none to delete. Repair every file at source (the facility
  extract read at its proper grain and as at the end of 30 September, every customer grouped) and the call and
  the naive figure do not move, because no facility, limit-history or rates row is on the call's path (asserted).
- **Lens swap:** no. The naive figure and the answer are the same book under two forecasting models:
  the naive carries P(arrival | flag status) from calmer years, the answer carries P(flag | outcome)
  and backs the year's share reaching the list out of the flagged share; the filed test separates them.
- **No artifact ranks or forecasts.** No performance report, no prior forecast, no prior caseload
  figure ships. The standard defines the three measures, the group-flag rule and the test.
- **Guard WARNs, answered.** `repeat.gate_g` (task230, task445) and `overuse.gate_g` (5 of the last 12): the
  label follows the decisive step, and with the test filed the step is a choice of basis; the alternative label,
  forecasting, sits in 5 of the last 12 too (task130, task132, task133, task135, task181), so neither clears
  it. No neighbour turns on a screen's yield moving with the base rate: task445 completes each reporter from its
  own arrival history, task230 is a causal design, task228 a false-alarm budget per run, task134 maturity,
  task131 a causal design; drivers sit at 0.07 and below.

## Entity and decision

Halstow Bank plc, a UK commercial bank. Credit risk monitoring sizes the 2027 watch-list caseload for
the executive risk committee on 4 November 2026 (one analyst carries twelve groups). The committed
call: **133 obligor groups from the 30 September 2026 monitored book will reach the watch list by
30 September 2027.** Forward facing: the window opens on 1 October 2026. The tag stays ETL: the work
is building the five cohorts from four systems (entity signals keyed by LEI or company number, the
GLEIF consolidation hierarchy for non-borrowing members, the credit system's group register and
watch-list history) and conforming committed exposure from a two-ledger facility extract and its limit
history; the forecast is one line of algebra on the conformed cohort table once the test has chosen it.

## Filed text for the builder (CRM-07 v3.1, exact wording)

Every section not listed keeps its stage 3 wording. 5.2 names no hit, capture or false-alarm rate, no base rate
and no inversion.

- **1.3 (new):** "Dates and times in this standard are UK time (GMT or BST, whichever is in force)."
- **2.3 (replaces the stage 3 list of the pack's edge cases):** "Group structure is read from GLEIF's Level 1 and
  Level 2 data as GLEIF publishes it, under GLEIF's own definitions of its relationship types and registration
  statuses."
- **4.2 (one sentence added at the end):** "A cohort is closed once its twelve months have ended."
- **5.2 (replaced):** "The forecast is the number of groups in the monitored book at the cohort date expected to
  reach the watch list in the twelve months after it, with the book, the outcome and the groups left out as 4.1,
  4.2 and 5.1 set them. Each group is given a probability of reaching the list that depends only on whether it is
  flagged at the cohort date and is the same across the book; expected arrivals are the sum of the probabilities,
  and expected exposure the sum of each probability times the group's committed exposure at the cohort date. The
  probabilities are set from the last four closed cohorts taken together, on whichever basis predicts those
  cohorts best: each cohort in turn is predicted from its own book and flags at its cohort date, on the basis set
  from the other three taken together; a basis's error is the largest of its four misses, each taken as a share of
  that cohort's actual arrivals; and the basis with the smallest error is the one used."
- **6.1 (replaced):** "A group's committed exposure at a date is the sum of the committed limits, as they stood at
  the end of that date, of the facilities on which one or more of its members is an obligor, across Halstow Bank
  plc and Halstow Bank Ireland DAC, in sterling at that date's Group Treasury closing rates. Only facilities in
  force at the end of the date count: a facility whose start date falls after the date, or whose final maturity
  date falls on or before it, is not in force at the end of it."
- **6.2 (first sentence reworded):** "The caseload is reported in five bands of committed exposure at the cohort
  date: under GBP 5m; GBP 5m and under GBP 15m; GBP 15m and under GBP 40m; GBP 40m and under GBP 100m; GBP 100m
  and over. Groups of GBP 40m and over are worked by Restructuring, the rest by Business Support."
- **Field reference.** The three facility-extract sections go; in their place
  `facility_obligor_extract_20260930.csv` ("Facilities on the Halstow Bank plc and Halstow Bank Ireland DAC loan
  ledgers when the quarter-end extract ran, with their obligors"; fields booking_entity "HB-PLC or HB-DAC, the
  ledger the facility is booked on", facility_id "the facility number on that ledger", customer_id "the obligor
  the row is for", product, currency, committed_limit "the facility's committed limit when the extract ran, in the
  facility currency", drawn_balance "the obligor's drawings when the extract ran", start_date, final_maturity_date,
  facility_status "ACTIVE, CANCELLED or CLOSED when the extract ran") and `facility_limit_history_20261008.csv`
  ("Every committed limit each facility has carried, one row per version"; booking_entity and facility_id as in
  the extract, committed_limit, effective_from "when the version took effect, UTC, as the loan platform records
  it", source "SOD_BATCH for the start-of-day batch, otherwise the user who keyed it"). The obligor master's
  group_id reads "the obligor group the credit system books the customer to; blank until the monthly grouping
  review books a new customer". The rates file's column is `units_per_gbp` ("units of the currency for one pound
  sterling at the Group Treasury 16:00 London close"). Nothing in the reference states a row grain beyond these
  sentences, names a device, or says how many rows a facility has.
- **Extract log.** The three facility jobs and the plc control line go. In their place:
  `FACILITY_OBLIGOR_EXTRACT 2026-10-01 01:15 <rows> both ledgers; held for the HB-DAC ledger close, ran after
  start of day 01/10`, `FACILITY_LIMIT_HISTORY 2026-10-08 05:50 <rows> limit versions to 07/10/2026`, and
  `Control: limit history reconciled to the facility extract, no breaks.` No line states a facility count.
- **Distractor.** `ifrs9_macro_scenarios_2026q3.xlsx` becomes `group_economics_uk_outlook_oct2026.xlsx`, titled
  "Group Economics: UK outlook, October 2026", sheets Central, Downside and Severe downside (quarterly real GDP
  growth, unemployment, Bank Rate and CPI to 2029 Q4) and Notes; no scenario weights, no IFRS 9 wording; author
  Group Economics. It stays in `metadata.json`'s distractor list beside the rating master scale.

## Ladder (asserted in `generator/checks.py`; the call, groups)

Closed cohorts (built from the pack; counts retuned in loop 1): monitored 846 / 871 / 889 / 902; reaching the
watch list 75 / 43 / 36 / 47; flagged 119 / 98 / 95 / 104; flagged and reaching 58 / 32 / 28 / 39 (flagged and
not reaching 61 / 66 / 67 / 65). Hit rate 0.487 / 0.327 / 0.295 / 0.375; capture rate 0.773 / 0.744 / 0.778 /
0.830; false-alarm rate 0.0791 / 0.0797 / 0.0785 / 0.0760; share reaching 8.9 / 4.9 / 4.0 / 5.2 per cent; flagged
share 14.1 / 11.3 / 10.7 / 11.5 per cent. Taken together: hit 0.3774 (157 of 416), capture 0.7811 (157 of 201),
false-alarm 0.0783 (259 of 3,307), miss 0.0142 (44 of 3,092). Forward book at 30 Sep 2026: 913 monitored, 165
flagged (0.1807).

**5.2's test over the family** (each closed cohort predicted from the other three; worst miss as a share of
actual arrivals; forward figure):

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
three cohorts 132.44, the first three 135.01 (5.2 and 4.3 name the last four closed cohorts).

| Rung | Reading | Figure | Killed by |
|---|---|---|---|
| R0 | the pooled hit and miss rates, the measure the committee sees | 72.9 (73) | 5.2's test: 40.6 per cent against 1.6 |
| R0b | the latest closed cohort's rates | 69.4 | 5.2's window (the last four closed cohorts taken together) and its test |
| R1 | the most stressed cohort's rates | 97.9 | the same |
| R2 | hit and miss rates trended on the flagged share | 146.7 (147) | not set from the cohorts taken together, and its test miss is 8.0 per cent |
| R3 | every flagged group reaches, plus the unflagged miss rate | 175.6 | the test (198 per cent); about 7.8 per cent of groups that do not reach are flagged every year |
| Answer | 913 x (0.1807 - 0.0783) / (0.7811 - 0.0783) | **133.04 (133)** | |

- **Convergent routes (C1):** the mean of cohort rates (132.97), the straight-line fits of the arrival share on
  the flagged share (132.83 unweighted and weighted) and arrivals on flagged count and book size (132.84) all file
  133, and each loses the test to the pooled basis (2.0 against 1.6) and is not "taken together" in any case. The
  mean-of-rates variant also lands both arrival totals (103.9, 29.1) and every arrival figure in the golden's bin
  (its probabilities differ by -0.00018 flagged and -0.00005 not flagged); on the top bands' exposure figures it
  can differ, which 5.2's "taken together" and the test both rule out.
- **Probabilities:** this year's share reaching 0.14571; flagged 0.62978 (63.0 per cent), not flagged 0.03893
  (3.9 per cent); expected arrivals 103.91 flagged and 29.12 not flagged.
- **Satisfying to stop at.** R0 is the measure the standard reports, applied as it reads; R0b is the freshest
  evidence; R1 is the "use a stressed year" instinct; R2 is the half insight with a decent test score.
- **Direction.** R0, R0b and R1 sit below the answer, R2 and R3 above. Nearest natural rung: R2 at +10.3 per
  cent. The base rate with no flags (52.3) and flagged arrivals only (79.7) are bases the test refuses.
- **Bins.** 133.04 sits 0.46 from the nearer edge (the call moves only if expected arrivals rise by 0.46 groups);
  103.91 and 29.12 sit 0.4 and 0.3 of a bin from theirs.
- **The decisive move against the seven properties.** 1 no sentence states it (5.2 files the test, not the
  basis); 2 the closed cohorts score it, which is the filed test working (C2 confirmation of a filed criterion,
  not recovery of an unwritten rule); 3 no arithmetic symptom: R0 reconciles to every count it uses; 4 not a row
  predicate: a property of the whole cohort table; 5 the enumeration is algebra over four cohorts; 6 no cutover
  date (2022's high rate is a cycle, not an event); 7 survives deletion (nothing is wrong).

## Stump or fork

The standard files the estimand (5.2 with 4.1, 4.2, 5.1 and 5.3) and the test that selects the basis (5.2), and
names no basis. The four closed cohorts separate the bases under the test by a wide margin: the pooled
capture-and-false-alarm basis is the unique minimum at 1.6 per cent; the bases that converge on 133 sit at 2.0
per cent and are not "taken together"; every basis that gives another figure misses a cohort by 7.97 per cent or
more, and every one set from the cohorts taken together by 35.6 per cent or more. A second answer exists only for
a reader who skips the test, and skipping it violates 5.2.

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

## Closure table (22 axes)

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | monitored book: active on the register and not on the watch list at 30 Sep (4.1); later joiners out (5.1); C1: no register or watch-list date within 8 days of a cohort date |
| 2 | Unit | obligor group; members = booked customers plus GLEIF accounting-consolidation members in force at the date (2.1, 2.2); C1: every flagged entity's membership stable across all cohort dates |
| 3 | Attribution window | placed in the twelve months after the cohort date (4.2); C1: no placement within 8 days of a window edge |
| 4 | As-of dating | the September month-end publication; relationship periods covering the date; asks: limits as they stood at the end of 30 Sep UK time (1.3, 6.1) read from a history stamped in UTC (field reference) |
| 5 | Version basis | one publication per month-end; asks: the limit version in force at the end of 30 Sep (6.1), not the extract's limit at its 01:15 run on 1 Oct |
| 6 | Denominator | the three measures' denominators filed (4.3); the test's miss is a share of the cohort's actual arrivals (5.2) |
| 7 | Weighting | the four cohorts taken together (5.2); mean-of-rates converges on the call, both arrival totals and every arrival figure (asserted) and loses the test |
| 8 | Window length | the last four closed cohorts (4.3, 5.2); latest-alone 126.82 and three-cohort 132.44 and 135.01 violate it |
| 9 | Inclusivity | band edges "and under" (6.2); C1: no group within GBP 0.25m of an edge on the right path |
| 10 | Rounding path | unrounded throughout; whole groups to the nearest (5.3); one decimal on report; every graded figure at least 0.25 of its bin from an edge (asserted) |
| 11 | Tie-break | the test's minimum is unique (1.6 against 2.0 and more); no ranking elsewhere |
| 12 | Maturity | a cohort is closed once its twelve months have ended (4.2); 2025's window ends 30 Sep 2026 and the history runs to that date; C1: no placement after 30 Sep 2026 in the history |
| 13 | Order of operations | flag at group level before counting; convert each facility to sterling before summing; collect a group's facilities before summing |
| 14 | Row order | irrelevant on the right path; the whole-extract de-duplication stops depend on it and both orders are asserted off the golden |
| 15 | Duplicate resolution | a group counts once per window (4.2); a facility counts once in each group with an obligor on it (6.1) |
| 16 | Identity | LEI case-normalised; CRN keys through the company number; merged LEIs green (inert); a facility is its booking entity and ledger number |
| 17 | Netting | none |
| 18 | Units | limits in facility currency; rates in `units_per_gbp` (inert) |
| 19 | Code semantics | AMBER and RED flag, GREEN does not (3.2); every watch level is on the list; CANCELLED and CLOSED facilities carry a nil limit in the extract and in the history's version in force (C1 on any status reading) |
| 20 | Integerisation | nearest whole group (5.3); 133.04 sits 0.46 from the nearest edge |
| 21 | Clause scope | one probability per flag status, the same across the book (5.2): not split by band, sector or size |
| 22 | Forward window | the 30 Sep 2026 monitored book only (5.1, 5.2); every group in it carries at least one facility in force at the end of 30 Sep 2026 (asserted) |
| decisive | The basis | C2 confirmation of 5.2's filed test on the closed cohorts: a family of 13 bases (the table above), the pooled capture-and-false-alarm basis the unique minimum at 1.6 per cent (1.57), every non-convergent basis at 7.97 per cent or more |

## Ask sheet (supplemental-stumping)

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
| Expected arrivals, flagged | 5, total 103.9 | flagged groups in the band x 0.62978 | DV-A, DV-B through band membership | caseload by team |
| Expected arrivals, not flagged | 5, total 29.1 | the rest x 0.03893 | DV-A, DV-B through band membership | manual-review capacity |
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

## Shape and criteria

Shape 05: the 133 allocated over five bands, each band with five figures (25), the total row (5), the call, the
chart's named parts (stacked bars per band, the band order, flagged against not flagged, the caseload written on
the chart, a quotable title) and two files: 38.

## Prompt

`prompt.md`, 946 characters by voice-check, 157 words, opening on the analyst caseload (number-first; the script
files it as other, 9 of 12 in the window, a batch property). The role moves from the bare closing sentence ("I head
credit risk monitoring.", which closed task445 to task447 in turn) into the opening sentence ("the caseload I put
to it as head of credit risk monitoring"). The call is one sentence at the seam carrying its unit and the book's
date; both later paragraphs tie back to it. The band row gains the groups it holds and their committed exposure,
the agenda's own requirement. No input file, method, measure or trap word. Deliverables
`watchlist_inflow_2027.xlsx` and `watchlist_inflow_2027.svg`. voice-check: no carrier flags, no repeated runs,
economy inside every flag.

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

## Stopping rule

A round that lands 133 sends the build to loop 2 with the solver's path sentence. If that path is 5.2's test with
the capture-and-false-alarm basis or a straight-line fit of the arrival share on the flagged share, the next
designer records it in `## Tried and rejected` and weighs a re-root against a ladder change, because the test is
filed and the data has to separate the bases; a hardening may deepen the analysis but never un-file the test. A
round on 73, 69, 98 or 147 with the band figures on the same model is the designed stump, and the build goes on
to stage 6b and the judge.

## Loop 1 build brief (for the builder)

- **`world.py`:** `TP_FLAG = [58, 32, 28, 39]`, `FP_FLAG = [61, 66, 67, 65]` (N, reaching and the forward 913 and
  165 unchanged); `band_plan` retuned to the new probabilities and the two new columns' bins; `plant_devices`
  rewritten for DV-A, DV-B and HZ-C (D2, D3, D4 and the matured-ACTIVE D8 removed; cancelled and closed facilities
  carry a nil limit); facilities carry obligor lists, ledger numbering per booking entity and limit versions with
  UTC stamps; `build_signals` draws RED through the year.
- **`make.py`:** `FILES` loses the two plc extracts and the HB-DAC extract and gains
  `facility_obligor_extract_20260930.csv` and `facility_limit_history_20261008.csv`; the scenarios workbook becomes
  `group_economics_uk_outlook_oct2026.xlsx`; the rates column becomes `units_per_gbp`; natural row order.
- **`docs.py`:** the standard's 1.3, 2.3, 4.2, 5.2, 6.1 and 6.2 as filed above; the field reference and the extract
  log as above; the outlook workbook; the containers per the realism repairs. Keep GLEIF's own term for the
  concatenated files (never "golden copy", which tripped leak.py at stage 3).
- **`solve.py`:** 5.2's test over the 13 bases and the choice by smallest worst miss; exposures from the
  facility-obligor extract with the history as of 2026-09-30T23:00:00Z, per group by booking entity and number,
  not-yet-grouped customers through GLEIF; the band table's five columns.
- **`checks.py`:** the test table (every basis's misses and forward figure, the unique minimum), the convergence
  of the 133 routes, the bins, the device assertions 1 to 7, the zero-counts, the literal-reader assertion (the
  filed test's winner is the golden's basis), and the realism assertions.
- **`deliver.py`, `writeup.py`, `meta.py`:** the two new columns and the 133; the Cohorts sheet carries the test
  table; the steps cite 5.2's test; `metadata.json` files and distractors. The chart stays an SVG (a PNG put
  task87, task100 and task130 on the surface screen at stage 3).
- **Then** stages 3 to 5 as the pipeline sets them: the reader reads again (the prompt and documents changed).

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
