# task446 design note (architecture 3, re-rooted 2026-10-21 under the 10/10 rules)

Halstow Bank plc's 2027 watch-list caseload: how many of the 913 obligor groups in the 30 September 2026
monitored book reach the watch list by 30 September 2027. The client returned architecture 2 on its
2026-10-12 review (Stumped type match failed: CRM-07 5.2 filed the model, one probability per flag status the
same across the book, the fitting window and the leave-one-cohort-out selection, so once the cohorts were
built the solver ran a stated procedure). The 2026-10-15 repair unfiled the selection rule only: 5.3 still filed
one probability per flag status shared across the bands, and the decisive insight (a screen's error rates carry
across years while its yield moves with the base rate) is task192's driver. Architecture 3 keeps the world, the
registers, the signals, the watch-list history, GLEIF and section 4's cohort definitions, as the client asked,
and moves the decisive step onto a genuine forecasting choice the reviewer named: flagged groups whose chance of
reaching the list depends on the kind of signal behind the flag, so one flagged rate misses. CRM-07 now files
the estimand and the reporting precision only.

## Draw

| Axis | Draw |
|---|---|
| Card | `cards/task446.json`, architecture v3, registered 2026-10-21 (forum and forcing event redrawn and re-registered at stage 3, below): `guard.py check` WARN (question form repeats task272), test.same_puzzle_older and test.same_driver_older differentiated (task134 v2, task149, task131 v2, task183, task230 v3); lineage keeps v1, v2 loop 1 and v2 as repaired with their fates |
| Domain / task type | banking-credit-financial-risk / credit-scoring-pd-modeling, which serves Forecasting: the call is the twelve-month watch-list migration of the flagged and unflagged book, worked as a PD is, by segmenting the population where the risk driver differs |
| Objective | Forecasting & Predictive Modeling: a count for a window that opens on 1 October 2026 |
| Shape | 05 allocation to a fixed total: the caseload over five exposure bands (groups, committed exposure, groups flagged, expected arrivals, expected exposure arriving) with a total row |
| Gate G mechanism | forecasting |
| Gap / pattern | time then population / none; generators G14 (decisive), G6, G19 |
| Decision type | quantity_figure |
| Stump strategy | composition_mix; decisive rule filed: no; official decoy: no; validated decoy: no |
| Calibration | existing_book_actuals: the bank's own four closed cohorts |
| Context artifact | filed_model (CRM-07, the monitoring standard) |
| Role, forum, forcing event | credit risk monitoring; the chief risk officer's leadership team, which sets the 2027 Restructuring and Business Support headcount from the caseload (executive_team); the close of the monitoring year to 30 September 2026 (period_close) |
| World | United Kingdom, GBP, Halstow Bank plc; personas from `guard.py names --geo 'United Kingdom' --seed 446` |
| Layer 2 | estimand_identification, own:group-flag-conversion-by-raising-member |

**Data-native sentence.** CRM-07 3.2 flags an obligor group when any member is AMBER or RED, and the engine covers
the parents and sister companies the bank does not lend to as well as its customers, so every year's flagged pool
mixes two signals: a customer the bank lends to deteriorating, which reaches the watch list about half the time,
and a non-borrowing member reached only through the GLEIF consolidation records, which reaches it about one time in
sixteen; this September's 165 flags sit on customers 77 per cent of the time against 48 to 69 per cent in the
closed cohorts, so the pooled flagged rate the cohorts measured belongs to their mix and not to this book's.

**One line per source.** The client's return (2026-10-12) and its "How to fix": the standard states the goal, not
the model or the selection rule, and the answer turns on flagged groups whose arrival risk differs by signal, so a
single flagged rate misses. `layer2-rigor-patterns` (credit-scoring-pd-modeling): segment where the risk driver
differs and carry each segment's rate onto the forward mix; the judgment here is which segmentation the records
force (the member that raised the flag, rebuilt from the obligor master and GLEIF), not the method. task445
(portal failure on a literal reading): avoided, no filed sentence reads to the easy answer. task192 and task134 v2
(spent drivers): the error-rate transport and the hazard by time since entry are both refused as this build's
decisive step (Tried and rejected).

**Guard WARNs answered.** The decision is a count because the leadership team sets headcount from a caseload, and
the prompt asks "how many" because a count asks how many; the prompt's call sentence is the shipped one.

**Forum and forcing event, redrawn at stage 3.** `guard.py heart` found committee_or_panel and
budget_or_appropriation banned against task486 v2, filed at 03:15Z, before this card, and brought into the corpus
by the pull that followed the DRAWN check. The pack was changed rather than the labels: CRM-07 5.1 now makes the
forecast part of the close of the monitoring year that ends on the cohort date, 5.2 has the chief risk officer's
leadership team set the Restructuring and Business Support headcount from it, and Credit Risk Monitoring's
year-end close timetable replaces the executive risk committee agenda. executive_team and period_close are the
honest labels for that fiction: the people who act on the caseload are the chief risk officer and the officer's
direct reports, not a constituted committee, and what puts the forecast on the table now is the close of the year
at the cohort date. No figure, rung or device moved: every data file rebuilt byte-identical, and only the standard
and the replaced document changed.

## Default path

1. Roll each September publication in `ews_entity_signals_2022-09_to_2026-09.csv` up to obligor groups through the
   group register, the obligor master and the GLEIF consolidation records in force (CRM-07 2.2, 3.2): 165 of the
   913 groups in the 30 September 2026 book are flagged.
2. Build the four closed cohorts (4.1, 4.2) and match them to `watch_list_history_2020-01_to_2026-09.csv`.
3. Take the share of flagged groups that reached the list over the cohorts taken together (131 of 416, 0.3149) and
   the share of the other groups (50 of 3,092, 0.0162).
4. Give each flagged group the first and every other group the second, and sum over the book: 64.05.
5. File the caseload at the nearest whole group (5.3).

Ends on: 64 groups

Golden: 78 groups

## Stump sentence

A competent solver rolls the entity signals up to groups, builds the four closed cohorts and gives each flagged
group the share of flagged groups that reached the list over those cohorts taken together and each other group
the unflagged share, and files 64 (Ends on); the step that lands it there is treating every group flag as one kind
of signal, when a flag raised on a customer the bank lends to reaches the list half the time (120 of 240) and one
raised only on a member it does not lend to one time in sixteen (11 of 176), and this September's flags are 77 per
cent customer-raised against 48 to 69 per cent in the cohorts; pricing each kind of flag at its own rate predicts
every closed cohort within 3.9 per cent out of sample (the single flagged rate misses one by 14.4) and gives 78.

## Three rules

- Task type: credit-scoring-pd-modeling in Banking, Credit & Financial Risk, which serves Forecasting & Predictive
  Modeling: the call is the book's twelve-month watch-list migration, forecast by segmenting the flagged population
  where the risk driver differs, the way a PD model segments a portfolio.
- Domain test: the deciding quantity is the watch-list inflow a bank sizes its workout caseload on, and credit
  monitoring reads a group-level early-warning flag by where in the obligor group it sits, because a deteriorating
  borrower and a stressed sister company the bank has no lending to are different credit events (the contagion
  question group monitoring asks of every group flag); the conversion of each kind is the PD-style segment rate.
- Swap: "how many of our registered patients will be admitted next year, given this year's risk flags" loses the
  task: there is no obligor group built through accounting consolidation, no lending relationship that separates
  the member that borrows from the member that does not, no watch list with a twelve-month cohort window and no
  committed book, so the segmentation that decides the call has nothing to attach to.
- Layer 1: the engine's entity-level signals keyed by LEI or company number for borrowers and non-borrowing members;
  GLEIF Level 1 and 2 files with lapsed registrations, successors, branches and fund links; the credit system's
  group register, obligor master (open and closed customers with the date each was opened) and watch-list history
  in its own namespace; a two-ledger facility extract at facility-and-obligor grain run after the 1 October
  start-of-day batch, a limit history stamped in UTC, customers not yet grouped and joint-venture companies booked
  to one partner's group while GLEIF consolidates them into the other's. Each is what the bank's systems produce;
  none sits on the decisive step (asserted).
- Layer 2: estimand_identification, a composition shift: the flagged pool's conversion is a blend of two kinds of
  flag the group rule treats alike, the forward pool holds a different blend, and the forecaster has to find the
  segmentation the records force and carry each segment's rate rather than the pooled one.
- Decisive step: forecasting each flagged group at the conversion of its own kind of flag (raised on a customer the
  bank lends to, or only on a member reached through the GLEIF consolidation records), rather than at the flagged
  pool's single rate, which carries the cohorts' mix of the two onto a book that holds far more of the first.
- Not semantics: every field, code and definition is read the same on the default path and the golden (the flag
  under 3.2, the group under 2.2, the cohort and outcome under 4.1 and 4.2); the pooled flagged rate is correctly
  defined and correctly computed, and it is still the wrong thing to carry onto this book.
- Not rule application: CRM-07 files the estimand (5.2) and the reporting precision (5.3) and no model, segment,
  fitting window or selection test; the family the filed rules leave open spreads from 43.9 to 136.0 on the call
  (one flagged rate 64.1, the latest and most stressed cohorts 65.1, the colour and covenant-trigger splits 64.6 and
  65.8, the error-rate basis 136.0, the trended and regression bases 43.9 to 51.5), while every member that prices
  flags by the member that raised them (pooled or mean rates, any window of the cohorts, colour or covenant within
  kind, the rates trended) lands on 78 (77.94 to 78.36).
- Analyst test: a strong analyst who conforms every signal to its group and reads every clause of CRM-07 correctly,
  then forecasts the easy way, one probability for flagged groups and one for the rest as the four cohorts measured
  them, files the default path's Ends on, 64; only one who traces each flag to the member that raised it, sees the
  two kinds convert at 0.50 and 0.0625, and sees this September's flags sit mostly on customers, reaches 78
  (executed on the clean truth in `generator/checks.py`).
- Estimand: CRM-07 5.2 (with 4.1, 4.2, 5.1 and 5.3): the number of groups in the 30 September 2026 monitored book
  expected to reach the watch list by 30 September 2027, groups joining later left out, to the nearest whole group,
  in `early_warning_and_watch_list_standard.pdf`.
- No decoy: no performance report, prior forecast, memo or caseload figure ships; no hit rate, capture rate or
  conversion is stated as a number anywhere in the pack, and no sentence argues for any basis.
- No certified replay: nothing certified is reproduced to recover a method; the closed cohorts are evidence the
  forecaster segments and validates, and nothing tells them how.
- Lesson: a group-level early-warning flag is a mixture of signals, and its conversion belongs to the mix of the
  year it was measured in, so a forward caseload prices each flag by the member that raised it; nearest drivers on
  file 0.06, and the two spent drivers it could be mistaken for (task192, task134 v2) are differentiated on the card.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 one flagged rate, one unflagged rate | 4.3 defines the hit rate | no | yes, the default | no | no | yes | readable |
| R0b latest or most stressed cohort's rates | no | no | yes, freshest evidence | no | no | yes | readable |
| R1 colour split (RED and AMBER) | no | the signal column | yes, stratify on a visible attribute | no | no | yes | readable |
| R1b covenant-trigger split | no | the trigger column | yes, stratify on a visible attribute | no | no | yes | readable |
| R2 capture and false-alarm rates, arrival share backed out of the flagged share | 4.3 defines the measures | no | a Bayes reflex | no | no | no | readable |
| R2b rates trended on flagged share or regressed on flag counts | no | no | a regression reflex | no | no | no | readable |
| Flags priced by the member that raised them (decisive) | no: 2.2 and 3.2 make every member's flag count alike and say nothing of conversion | no: no column says which member a group's flag came from or whether that member borrows; it is rebuilt by joining each AMBER or RED key to the obligor master as at the cohort date | no: the colour, score and trigger reflexes all land on 64 to 66 | no: no control or corpus scores a segmentation | no | no: a join to the customer list as at each cohort date, then a rate per kind | silent |

## Semantic fork table

| ID | Term | Golden reading | Alternative | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | an ultimate parent that is not booked | a member (2.2 as amended) | members only when booked or consolidated | same call: no flag sits on an unbooked ultimate parent at any cohort date (asserted) | 2.2: "A group's members are its ultimate parent, ..." |
| SF2 | a flag raised on a customer (the decisive step's partition) | an AMBER or RED entity that is a customer on the credit system opened by the cohort date, open or closed now | customers ACTIVE at the extract date only; obligors on the 30 Sep 2026 facility extract only | 73.08 and 73.37 (both 73) | the field reference: the obligor master is "every customer on the credit system, open or closed", `customer_status` is "at the extract date", `customer_since` dates each customer; the facility extract is the 30 September 2026 book only |
| SF3 | the closed cohorts the rates are taken over | the four closed cohorts taken together | the latest alone, the last two, the last three, the first three | same call (77.95, 77.98, 78.23, 77.98; asserted); the 2025 cohort alone puts the GBP 40m to 100m band's arrivals at 9.1 | 5.2: the forecast "rests on the closed cohorts scored by the current release, taken together", and 1.2 (the engine unchanged since January 2022); filed at the stage 4 judge's FIX_NOW, a WHAT that names no model, segmentation or basis |
| SF4 | pooled rates against the mean of the cohorts' rates | pooled | mean of the four cohorts' rates | same call (77.97) and every band's expected arrivals in the same bin (asserted) | converges |
| SF5 | refinements within each kind of flag | none needed | RED against AMBER, covenant trigger or not, rates trended over the cohorts | same call (77.97, 77.97, 78.36; asserted) | converges: pooled over the cohorts each kind's RED and AMBER flags, and its flags with and without a covenant trigger, reach the list at exactly the kind's rate |
| SF6 | a customer booked to one group whose GLEIF records consolidate it into another group's ultimate parent (21 joint ventures; asks only) | a member of both, its facility counted in both groups' committed exposure | the booked group only; the consolidating group only | same call (no such company carries a signal at any cohort date; asserted); band figures move (the ask device) | 2.2: members are "the customers the credit system books to it and every legal entity whose GLEIF relationship record shows it accounting-consolidated into the ultimate parent" |
| SF7 | an international branch or a fund of a group member | read through its head office or manager, or left out | the other reading | same call | every such entity is green at every cohort date (texture inert, asserted) |
| SF8 | a facility the ledger booked twice (22; asks only) | no commitment: left out | every facility number counted once; near-duplicates dropped on their terms; the undrawn near-duplicate dropped | same call (exposure never enters the forecast; asserted); every band figure moves (the ask's primary) | the records: each copy is undrawn and repeats, stamp, limit and user, the whole limit history of the facility numbered just before it for the same customer and terms; every genuine same-day pair is keyed apart (asserted) |
| SF9 | the flag classes the rates are taken over | three: raised on a customer, raised only elsewhere, not flagged | two: raised on a customer against everything else | same call (78.17); three band arrival figures move by 0.1 | the closed cohorts: predicting each from the other three, the three-way split misses by at most 3.92 per cent and the two-way by 4.77 (`solve.basis_test`; the stage 4 judge measured the same) |

## Ladder

Closed cohorts (built from the pack): monitored 846 / 871 / 889 / 902; flags raised on a customer 58 / 62 / 58 / 62,
reaching 28 / 32 / 30 / 30; flags raised only on a non-borrowing member 62 / 28 / 40 / 46, reaching 4 / 2 / 1 / 4;
groups not flagged reaching 13 / 11 / 12 / 14. Hit rate 0.267 / 0.378 / 0.316 / 0.315; customer-raised share of the
flags 48.3 / 68.9 / 59.2 / 57.4 per cent; flagged share 14.2 / 10.3 / 11.0 / 12.0 per cent. Taken together: flags on
customers 120 of 240 (0.5000), flags on other members 11 of 176 (0.0625), not flagged 50 of 3,092 (0.01617); hit rate
131 of 416 (0.3149). Forward book at 30 Sep 2026: 913 monitored, 165 flagged, 127 of them on a customer (77.0 per
cent), 38 only on other members.

**The cohorts' out-of-sample record** (each closed cohort predicted from the other three taken together; misses as a
share of actual arrivals; forward figure). Nothing in the pack files this test.

| Basis | Misses 2022 / 2023 / 2024 / 2025 (per cent) | Worst | Forward |
|---|---|---|---|
| **Answer: a rate by the member that raised the flag, one for the rest** | -1.2 / +1.2 / +3.9 / -3.6 | **3.9** | **77.97 (78)** |
| the same on the mean of the cohorts' rates | -1.2 / +1.1 / +4.0 / -3.6 | 4.0 | 77.97 |
| the same with RED and AMBER, or covenant trigger, within each kind | -1.1 / +1.2 / +3.9 / -3.6 | 3.9 | 77.97 |
| flags on customers against everything else | -3.8 / +3.2 / +4.8 / -3.7 | 4.8 | 78.17 |
| each kind's rate trended over the cohorts | +2.5 / +2.2 / +5.7 / -7.4 | 7.4 | 78.36 |
| R0: one flagged rate, one for the rest | +14.4 / -11.2 / +2.0 / -3.2 | 14.4 | 64.05 (64) |
| mean of the cohorts' hit and miss rates | +14.9 / -10.8 / +3.3 / -1.9 | 14.9 | 64.73 |
| R0b: the latest cohort's rates (also the most stressed by arrival share) | +12.4 / -6.4 / +4.2 / -3.7 | 12.4 | 65.13 |
| R1: RED and AMBER rates | +13.9 / -10.8 / +2.1 / -3.1 | 13.9 | 64.63 |
| R1b: covenant trigger or not | +12.9 / -9.9 / +2.6 / -3.6 | 12.9 | 65.83 |
| R2: capture and false-alarm rates, arrival share backed out of the flagged share | +84.7 / -63.4 / -27.4 / +0.4 | 84.7 | 136.01 |
| R2b: hit and miss rates trended on the flagged share | -3.9 / -6.5 / +8.7 / -2.4 | 8.7 | 43.88 |
| arrival share on the flagged share, straight line | +3.0 / -5.1 / +8.1 / -3.8 | 8.1 | 51.46 |
| arrivals on the flagged count | +9.3 / -2.6 / +6.7 / -7.4 | 9.3 | 48.15 |
| one share for every group | -4.0 / -0.2 / +8.9 / -4.1 | 8.9 | 47.11 |

| Rung | Reading | Figure | Killed by |
|---|---|---|---|
| R0 | the pooled flagged and unflagged rates | 64.05 (64) | the cohorts' own record (misses 2022 by 14.4 per cent against 3.9) and the forward mix: 77 per cent of this year's flags sit on customers against 48 to 69 |
| R0b | the latest or the most stressed cohort's rates | 65.13 | one cohort's mix carried forward |
| R1 | RED and AMBER rates | 64.63 | colour carries nothing beyond the kind of flag (pooled RED and AMBER rates within each kind are equal) |
| R1b | covenant trigger or not | 65.83 | covenant triggers sit only on customers but on a quarter of their flags; within kind they carry nothing |
| R2 | capture and false-alarm rates with the arrival share backed out | 136.01 | the flagged share rose because customer flags did, not because the screen's error rates held; out of sample it misses by 84.7 per cent |
| R2b | trends on the flagged share or the flag count | 43.9 to 51.5 | the flagged share moves with the non-borrowing flags as much as with the customer flags (2022 had the most flags and the fewest customer-raised) |
| Answer | 127 x 0.5000 + 38 x 0.0625 + 748 x 0.01617 | **77.97 (78)** | |

- **Convergent routes (C1):** every member that prices a flag by the member that raised it lands on 78, from 77.94
  (the latest cohort alone) to 78.36 (rates trended), pooled or mean, any window of the cohorts, colour or covenant
  trigger within kind (asserted). Spread 0.42 of a group.
- **Satisfying to stop at.** R0 is the measure the standard reports, applied as it reads; R0b is the freshest
  evidence; R1 and R1b stratify on the columns the publication carries; R2 is the clever inversion, the old basis.
- **Direction.** Every rung but R2 lies below the answer; the nearest natural rung is R1b at -15.6 per cent, and
  the misreadings of the customer test under SF2 at 73 (-6.3 per cent) are lower rungs on the decisive path.
- **Bins.** 77.97 sits 0.47 from the nearer edge; the trended family member 78.36 sits 0.14 from it.
- **The decisive move against the seven properties.** 1 no sentence states it; 2 no column marks a flag's source; 3
  no arithmetic symptom (R0 reconciles to every count it uses); 4 not a row predicate on the decision file (a join of
  each AMBER or RED key to the obligor master as at the cohort date); 5 the enumeration is a two-way split; 6 no
  cutover date; 7 survives deletion (nothing is wrong).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | monitored book: active on the register and not on the watch list at 30 Sep (4.1); later joiners out (5.1); C1: no register or watch-list date within 8 days of a cohort date |
| 2 | Unit | obligor group; members = the ultimate parent, booked customers and GLEIF accounting-consolidation members in force at the date (2.1, 2.2); no flag sits on an unbooked ultimate parent (SF1, asserted) |
| 3 | Attribution window | placed in the twelve months after the cohort date (4.2); C1: no placement within 8 days of a window edge |
| 4 | As-of dating | the September month-end publication; relationship periods covering the date; a customer is a customer from the date the credit system opened it (`customer_since`); asks: limits as they stood at the end of 30 Sep UK time (1.3, 6.1) read from a history stamped in UTC |
| 5 | Version basis | one publication per month-end; asks: the limit version in force at the end of 30 Sep (6.1), not the extract's limit at its 01:15 run on 1 Oct |
| 6 | Denominator | each kind's flags in the cohorts taken together; 5.2's estimand is a count of groups |
| 7 | Weighting | the cohorts taken together (5.2); the mean of the cohorts' rates converges on the call and on every band figure (SF4, asserted) |
| 8 | Window length | every closed cohort scored by release 3.2, taken together (5.2, 1.2); every window variant files 78 (SF3, asserted) |
| 9 | Inclusivity | band edges "and under" (6.2); C1: no group within GBP 0.25m of an edge on the right path |
| 10 | Rounding path | unrounded throughout; whole groups to the nearest (5.3); one decimal on report; every graded figure at least 0.25 of its bin from an edge (asserted) |
| 11 | Tie-break | none needed: every member of the decisive family files 78 |
| 12 | Maturity | a cohort is closed once its twelve months have ended (4.2); 2025's window ends 30 Sep 2026 and the history runs to that date |
| 13 | Order of operations | flag at group level before counting; a group's flag is kind D when any AMBER or RED member is a customer, and every second carrier is of its lead's kind (no mixed group, asserted); convert each facility to sterling before summing |
| 14 | Row order | irrelevant on the right path; the whole-extract de-duplication stops depend on it and both orders are asserted off the golden |
| 15 | Duplicate resolution | a group counts once per window (4.2); a facility counts once in each group with a member on it (6.1); a creation message the ledger booked twice is one facility, told from a genuine same-day tranche by its limit history (SF8, asks only) |
| 16 | Identity | LEI case-normalised; CRN keys through the company number; merged LEIs green (inert); a facility is its booking entity and ledger number, the copies apart (SF8) |
| 17 | Netting | none |
| 18 | Units | limits in facility currency; rates in `units_per_gbp` (inert) |
| 19 | Code semantics | AMBER and RED flag, GREEN does not (3.2); every watch level is on the list; CANCELLED and CLOSED facilities carry a nil limit in the extract and in the history's version in force |
| 20 | Integerisation | nearest whole group (5.3); 77.97 sits 0.47 from the nearest edge |
| 21 | Clause scope | 5.2 files the count and exposure for the whole book and the cohorts it rests on; 5.3 the reporting precision; 2.2 makes a company booked to one group and consolidated into another a member of both (asks only, SF6) |
| 22 | Forward window | the 30 Sep 2026 monitored book only (5.1, 5.2); every group in it carries at least one facility in force at the end of 30 Sep 2026 (asserted) |
| decisive | The basis | design-forced, C3: nothing filed names a segmentation; every basis that prices a flag by the member that raised it files 78 and validates within 4.8 per cent (7.4 trended); every basis that does not misses a closed cohort by 8.1 per cent or more and files 43.9 to 65.8 or 136.0 (asserted) |

## Literal reader

Executing the prompt and CRM-07 word for word, a reader computes the expected number of the 913 groups in the 30
September 2026 monitored book (4.1, later joiners out under 5.1) placed on the watch list by 30 September 2027
(4.2, 5.2), to the nearest whole group (5.3), resting on the closed cohorts taken together (5.2). The text names
no model, segmentation or basis, so every forecasting basis the cohorts support is an option: each one that prices a group's flag by the member that raised
it files 78 (pooled or mean rates, any window, colour or covenant trigger within kind, trended); every other files
43.9 to 65.8, or 136.0, and misses a closed cohort by 8.1 per cent or more. The easy 64 comes from an easy method on
the same literal estimand; no sentence in the pack, read literally, gives it.

## Oracles

None. No performance report, published forecast or prior caseload ships; the close timetable names the steps, their
owners and the caseload standard of twelve groups per analyst, not a figure. The closed cohorts are the forecaster's
evidence, not a control that ties only under the golden: they score every basis, and a solver has to segment them
to score the answer.

## Ask sheet

**Main call's declared row population** (the zero-counts run against it): the five September publications
(2022-09-30 to 2026-09-30) in the signal file; the GLEIF LEI-CDF and RR-CDF rows of every entity carrying AMBER
or RED in any of them, and of its parents up the consolidation chain; the obligor master rows whose LEI or
Companies House number matches such an entity; every group register row; every watch-list history row. Device and
hazard rows: every row of the facility-obligor extract, the limit history and the rates file (outside by file),
the 22 facilities booked twice and the 22 second tranches among them; the obligor master, GLEIF and signal rows of
the customers not yet grouped and of the 21 joint-venture companies, each green in every September publication
(asserted zero inside); no device writes a register, watch-list or September-publication row the call reads
(asserted by building the main-path files with and without the devices).

**The asks** (one band table in `watchlist_inflow_2027.xlsx`, its expected arrivals drawn in the chart):

| Column | Figures | Construction | Devices on the path | Use |
|---|---|---|---|---|
| Groups the band holds | 5 counts, total 913 | each group's committed exposure at 30 Sep 2026 (6.1), banded (6.2) | DV-D; DV-C, DV-A, DV-B, HZ | how the book splits between Restructuring (GBP 40m and over) and Business Support |
| Their committed exposure | 5 in GBP m, total | the band's sum of group exposures | DV-D; DV-C, DV-A, DV-B, HZ | the close timetable's "committed exposure by caseload band" |
| Groups flagged in September | 5 counts, total 165 | the call's flags (3.2) by band | DV-D and the rest through band membership | where the early-warning load sits |
| Expected arrivals | 5, total 78.0 | each group's probability by the kind of its flag, summed by band | the same | caseload by team |
| Expected exposure arriving | 5 in GBP m, total | probability x committed exposure | all | what the arriving caseload carries |

**Device ledger.**

- **DV-D, primary, facilities the ledger booked twice beside genuine same-day tranches (D1, silent: "a replay
  under fresh ids, key kept, beside genuine same-day pairs").** Root cause: when the limit system's interface timed
  out on a facility-creation message it sent the message again, and the ledger booked a second facility under the
  next number. Each copy carries its original's customer, product, currency, limit and dates and, stamp for stamp,
  limit for limit and user for user, its original's whole limit history, and has never been drawn. 22 copies,
  2016 to 2025, the largest GBP 37m. Beside them, 22 genuine pairs of tranches booked the same day on the same terms
  and keyed apart, the second tranche undrawn in 17 of them. Right: leave the copies out, keep both tranches.
  Wrong stops: Dk, the extract's every facility number counted once (the readers' path: the copies lift twelve
  groups over an edge, flagged 1 / 2 / 1 / 2 and not flagged 1 / 2 / 1 / 2 across the GBP 5m, 15m, 40m and 100m
  edges); Dt, over-cleaning, near-duplicates dropped on their terms (a genuine tranche goes too, and twelve groups
  drop under an edge, flagged 1 / 2 / 1 / 2 and not flagged 2 / 2 / 2 / 0); Du, the undrawn near-duplicate dropped
  (the copies go, and so do the undrawn second tranches). Organs: the extract and the limit history only (split
  evidence: the terms and drawn balance in one, the stamps and users in the other, neither enough alone); no filed
  sentence speaks to it, and the extract log's reconciliation control ties under every handling. Silent: the
  extract is unique on its key, every row joins the master and the history, every control ties; the copies show
  only when a customer's same-terms facilities are set side by side and their histories compared.
- **DV-C, a hazard (it was the primary until stage 4): a company booked to one group and consolidated into
  another (D7).** 21 joint ventures booked to the minority partner's group and consolidated through GLEIF into the
  majority partner's ultimate parent; under 2.2 each is a member of both, its facility in both groups' committed
  exposure. Both stage 4 readers built each group as a set of members under 2.2 and counted them in both without
  noticing them. Wrong stops: C1 one group per booked customer; C2 the consolidating group only. Seven cross nothing.
- **DV-A, the facility-and-obligor grain (D6, documented: a mirror device).** The extract carries one row per
  facility per obligor with the facility's limit on each row; joint property facilities with borrowers in two
  groups; about 40 ledger numbers that coincide across the two booking entities. Right: within each group each
  (booking entity, facility number) once. Wrong stops: A1 every row summed; A2 each facility number once across the
  extract; A3 each booking entity and number once across the extract. 6.1 and the field reference resolve it.
- **DV-B, the limit clock (D8, documented: a mirror device).** The extract ran at 01:15 on 1 October after the
  start-of-day batch applied about 70 increases and 12 activations stamped 2026-09-30T23:30:00Z. Right: each
  facility's version in force at 23:00Z on 30 September. Wrong stops: B1 the extract's limit; B2 the history on its
  UTC date; B3 the latest version; B0, over-cleaning, versions before 30 September only. 1.3, 6.1 and the field
  reference resolve it.
- **HZ, customers not yet grouped (D7, documented: a mirror device).** 14 September HB-DAC customers with a blank
  `group_id`, each consolidated through GLEIF into a monitored group's ultimate parent (2.2). Wrong stop: dropped.

**Movers** (distinct groups per device; edges in GBP 5m, 15m, 40m, 100m order): DV-D twelve copies (flagged
1 / 2 / 1 / 2, not flagged 1 / 2 / 1 / 2) and twelve tranche pairs (flagged 1 / 2 / 1 / 2, not flagged 2 / 2 / 2 /
0; the flags crossing into and out of the GBP 40m to 100m band of opposite kinds, so its arrivals cannot net back
into their bin), ten copies and ten pairs crossing nothing, two of each in every band; DV-C 14 crossing and 7 not;
A1 flagged 1 / 3 / 1 / 2 and not flagged 3 / 7 / 3 / 7; B2 flagged 1 / 3 / 1 / 3 and not flagged 3 / 7 / 3 / 7; A3,
B0 and HZ as before. DV-D is planted after the exposures are tuned, on its own random stream: it moves no group's
true exposure, so every graded figure stood still when it went in (asserted on the golden band table).

**Assertions for the builder** (all in `generator/checks.py`).
1. Zero device and hazard rows inside the declared population.
2. Dk, Dt and Du, and C1, A1 and B2, each alone move all 25 band figures and the arriving total; every other single
   reading moves 12 or more and the committed total by GBP 5m or more.
3. The device grid (A at four stops, B at five, HZ at two, C at three, D at four): every one of the 479 cells but the
   all-correct one misses the golden on 12 or more of the 25 band figures and moves the committed total by GBP 3m or
   more (the nearest printed by the run); no subset of mishandlings cancels back onto the golden band figures.
4. Fairness: the right handling reproduces the world's own group exposures exactly.
5. The hygiene battery on every wrong path runs clean.
6. The over-cleaners (A2, A3, B0, C2, Dt, Du) each land on their own values below the golden; Dk lands above it.
7. Every band figure at least 0.25 of its bin from an edge; every group in the book has a facility in force.
8. SF8: the right reading drops exactly the 22 copies; each copy repeats its original's history and takes the next
   number; every genuine same-day pair is keyed apart.

**Pair arithmetic** (`generator/cracker.py` on the cut pack, Part 0's weights 38 / 7 / 55, 34 graded ask figures:
the heading, 25 band figures, the total row's five and the chart's three parts). The cracker lands 78 and takes the
path both stage 4 readers took on the earlier cut: 2.2's members as sets, 6.1, 1.3 and the UTC history, the
customers not yet grouped placed through GLEIF, every facility number in the extract counted once. It keeps 6 of 34
(the heading, 913, 165, 78.0, the caseload on the chart and the title), 54.7 in all. The mirror stops on R0 and
handles the asks the same way: it keeps 2 of 34 (913 and 165), 15.2.

| Ask figure | Where the cracker's path goes | Mirror (stops at R0) | Cracker (lands 78, executes every filed rule it points at) |
|---|---|---|---|
| Groups per band (5) | the copies counted: twelve groups sit a band high | miss | miss |
| Committed exposure per band (5) | the 22 copies' limits added | miss | miss |
| Groups flagged per band (5) | six flagged groups sit a band high | miss | miss |
| Expected arrivals per band (5) | the same band membership | miss | miss |
| Expected exposure arriving per band (5) | the same membership and exposures | miss | miss |
| Total committed and arriving exposure (2) | the copies' limits in the total | miss | miss |
| The chart's bars (1) | the band arrivals above | miss | miss |

- **Main-path figures in the ask layer:** the heading, 913, 165 and the expected-arrivals total (78.0) sit on the
  call's own construction or the book's own size, and the chart's caseload and title carry the call: whoever lands 78
  keeps them, the mirror keeps 913 and 165. They are counted in the pair arithmetic, not in the cracker sheet.
- Mirror leakage: 5.9 per cent of ask weight (913 and 165).
- Pair ceiling: 35.0 (C = 38 + 7 + 55 x 6/34 = 54.7; S = 5 + 7 + 55 x 2/34 = 15.2).
- Measured by: generator/cracker.py, run on the cut pack by `generator/checks.py` on every build. Stage 4 round 1
  (the cut before DV-D) measured both readers off the call at 64 with 18 of 34 ask figures each (52.9 per cent), on
  the path the cracker now models; the re-sited device is measured again by two fresh readers on this cut.

## Layers

- **Layer 1 (main path, conformance the standard files):** entity signals keyed by LEI, or by `CRN:` and company
  number for entities without an LEI; non-borrowing members (parents, sisters, holding companies) reached through
  GLEIF accounting-consolidation records whose period covers the cohort date; the credit system's own customer and
  group namespace, with closed customers kept and each customer's opening date; every watch level is on the list;
  groups already on the list excluded; groups leaving the book count as not reaching. GLEIF texture on the main path
  (lapsed registrations, merged LEIs still in the vendor feed, international branches, fund-management links,
  reporting exceptions) sits on entities whose signals are green at every cohort date, so mishandling it moves
  nothing (asserted).
- **Layer 1 (ask paths, ledgered devices):** the facilities the ledger booked twice beside genuine same-day
  tranches, the joint ventures booked to the other partner, the facility-obligor grain, the UTC limit clock and the
  customers not yet grouped.
- **Layer 2:** a group-level flag is a mixture of two signals that convert at 0.50 and 0.0625; the cohorts measured
  the mixture at their own mix, this book holds another.

## Gate G

- **Litmus.** No reported number in the pack is wrong and nothing is overturned. The signals, the watch-list history,
  the registers and every extract are correct for the dates they describe; the pooled flagged rate the cohorts give
  is the right rate for the cohorts. The difficulty is that it is a property of their mix of flags, and the call is
  about a book whose flags sit on customers far more often.
- **Mechanism:** forecasting: the standard files the estimand only; the decisive step is the forecaster's own choice
  of segmentation (the member that raised the flag), forced by the records and validated on the closed cohorts.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Delete every wrong number:** there are none to delete. Repair every file at source and the call and the naive
  figure do not move, because no facility, limit-history or rates row is on the call's path (asserted).
- **Lens swap:** no. The naive figure and the answer are the same book under two forecasting models.
- **No artifact ranks or forecasts.** No performance report, no prior forecast, no prior caseload figure ships.

## Leak sweep

`leak.py --asof 2026-10-08`: REVIEW, no LEAK. Each REVIEW line:

- "the model" in the standard: 1.2's governance line (a new engine release needs the Model Risk Committee); it names
  no forecasting model. Harmless.
- "golden figure 5.1" in the standard: the section number 5.1, not the GBP 100m band's 5.1 expected arrivals.
  Harmless.
- The call's words in the field reference, the close timetable and the standard: the field's own nouns (watch list,
  caseload, obligor group, monitored book, 30 September 2027) and no figure. Harmless.
- Stump-paragraph terms in the field reference, the close timetable, the standard and the extract log: definitions
  of the obligor master's customers, the GLEIF parents and the cohorts; none says that a flag's conversion depends on
  where in the group it was raised. Harmless.
- Dates after 2026-10-08 in the facility extract: final maturity dates of facilities in force, forward by nature.
  Harmless.

**Solver's-eye read, stage 4 round 1** (two isolated scored readers on the cut before DV-D): both filed 64 (one
rate for every flagged group) and named the decisive step an analytical choice (question 6); question 1 quoted only
5.2's estimand and nothing that names the segmentation; questions 2 and 4 none; question 3 the field reference and
the extract log; question 5 quoted 5.2 and gave each reader's own forecast as its result, while 5.2 names no basis
(the judge, executing it literally, filed 78 under every construction it tried). Both kept 18 of 34 ask figures
(52.9 per cent, score_reader exit 1), which re-sited the ask primary (Tried and rejected). Realism notes: every LEI
on one 213800 prefix, formulaic entity names, round limits, the fourteen ungrouped Irish customers alike, the
extract log's "no breaks" beside 1 October starts; none moves a figure and none is on the decisive step.

**Solver's-eye read, stage 4 round 2** (two fresh isolated scored readers on the DV-D cut, sha256 06a4c8d5): both
filed 64 again and named the decisive step an analytical choice (question 6). Reader C kept 5 of 34 ask figures
(14.7 per cent: 913, 165, the under GBP 5m band's groups and flags, and one coincident arriving figure) and reader D
2 of 34 (5.9 per cent: 913 and 165), score_reader exit 0 for both; neither noticed the facilities booked twice
(reader D's total committed exposure is the copies-kept reading, GBP 25,943.2m). Both quoted 5.2's window sentence
for question 1 and gave their own pooled two-class forecast (64) as 5.2's literal result for question 5; the sentence
names the cohorts, not a segmentation, and the judge settles what it licenses: its round 2 pass (DETERMINISTIC, APPROVE) finds no licensed
competing answer. On the REVIEW lines both readers called four harmless; reader D called the stump-paragraph terms
"partly a leak" for 5.2's window with 4.3's rate definitions, which point at pooling the closed cohorts, a step the
easy route and the golden share; ruled harmless, since the deciding segmentation is named nowhere and both filed 64. Realism notes: the extract dated 30
September but run on 1 October (the log says so), lower-case LEI keys in the signal file (Layer 1 texture), the 21
joint ventures noticed by reader D as customers booked away from their GLEIF parent (the DV-C hazard), uniform LEI
prefixes; none moves a figure.

## Pre-ship check

1. Domain: group credit monitoring's own reading of an early-warning flag (where in the obligor group it sits); with
   another field's nouns the consolidation hierarchy, the lending relationship and the committed book have nothing
   to attach to.
2. Real work, nothing planted: every Layer 1 item is what the bank's or GLEIF's systems produce; none is on the
   decisive step (asserted).
3. The step that flips the call is analytical: the segmentation of the flagged pool; no clause makes the choice.
4. Analyst test: every field and rule read correctly, the easy forecast files 64 (asserted on the clean truth and on
   the pack, with and without devices).
5. CRM-07 files the estimand, the cohorts it rests on (taken together, 5.2) and the precision, and no model,
   segment or selection rule (asserted); every member of the decisive family files 78.
6. No decoy, no withheld rule against a stated one, no certified replay.
7. The lesson is on no other card: nearest drivers 0.06; task192 and task134 v2 differentiated.
8. Re-read against the built pack at stage 4: four isolated scored readers filed 64 and called the deciding step an
   analytical choice; the judge's re-pass on the shipped cut is DETERMINISTIC and APPROVE, Gate H analytical, with no
   licensed competing answer; the mess carrying the asks is Layer 1 only, and none of it reaches the call.

## Realism debts

- The forward caseload of 78 (8.5 per cent of the book) is above every closed cohort (4.8 to 5.3 per cent). It is
  what this September's flags imply: 127 customer-raised flags against 58 to 62 in the cohorts, the summer 2026
  stress showing in the monthly signals as a run of new AMBER and RED customers from May.
- 21 joint ventures among 913 groups, spread across the sectors, each booked to the partner that arranged its
  facility.
- 22 facilities the ledger booked twice and never closed, booked 2016 to 2025 and undrawn throughout, the largest
  GBP 37m: an undrawn duplicate limit moves no balance and so passes the ledger's balance reconciliations, which is
  how such records survive; the limit system's own reconciliation to the extract ties, since both hold the copies.

## Realism repairs for the loop 1 rebuild (the reader's tells and golden-realism)

1. **Containers.** The close timetable is built from a Word-authored skeleton (styles, theme, settings and font table as
   Word 16 writes them, app.xml with Template Normal.dotm, TotalTime, Pages, Words, Characters, Company Halstow
   Bank plc, AppVersion 16.0000), never python-docx's default template. Every input workbook carries a full Excel
   app.xml (DocSecurity, ScaleCrop, HeadingPairs and TitlesOfParts naming its real sheets, Company, LinksUpToDate,
   SharedDoc, HyperlinksChanged, AppVersion 16.0300). Core stamps follow each file's own story: the register,
   written by the Reference Data job at 05:05Z on 1 October (created equal to modified, as a job writes it); the
   rating master scale, Credit Risk Models, created 2025-12-12, modified 2026-10-02; the outlook, Group Economics,
   created 2026-10-05, modified 2026-10-06; the close timetable, created 2026-10-02 by the head of Credit Risk
   Monitoring and last modified 2026-10-07 by the analyst it names, revision 4. Asserted: no two input containers share a
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
- Architecture 2 as repaired on 2026-10-15 (CRM-07 5.2 filing the estimand only, the basis left to the cohorts'
  out-of-sample record), spent 2026-10-21 against the client's return of 2026-10-12: 5.3 still filed one probability
  per flag status shared across the bands (the model the reviewer named), 4.3's last four closed cohorts still closed
  the fitting window, the decisive insight (a screen's error rates carry across years while its yield moves with the
  base rate) is task192's driver, and this September's colour mix (RED flat at 41, AMBER up to 124) contradicted the
  backed-out base rate for any solver who inverted each colour. Re-rooted to architecture 3.
- Architecture 3 candidate, flag age (flags new this summer against flags standing since the previous September,
  the standing ones survivors that rarely convert, after a summer surge of new flags): the same driver as task134 v2
  round 1 (a conversion hazard by time since entry after a surge filled the pool), retired there as reachable from
  the surface; the 2022 cohort's flags were also left-censored by the signal archive's start.
- Architecture 3 candidate, a change in the trigger set partway through the history (pooling across it mixes two
  regimes): either the pack states the release, and the right computation follows from the sentence, or it does not
  and nothing in the records measures the break (stumping 1.2b, cases one and three).
- Architecture 3 candidate, an interval on the caseload with the headcount set on its upper end (between-year
  dispersion of the arrival rates): the dispersion and variance-only screens, four cohorts cannot pin a dispersion
  and the conservative reflex lands the hold.
- Architecture 3, first count set (customer flags 66 / 56 / 56 / 62 reaching 34 / 28 / 28 / 30, member flags 62 /
  26 / 44 / 44 reaching 2 / 2 / 3 / 4, forward 126 and 39): the call 77.05, but the trended member of the decisive
  family filed 76.43 and the member-raised rate's mean of cohort rates sat 0.0046 above the pooled rate, enough to
  split band figures. Re-tuned to the shipped counts, where every member of the family files 78.
- The ask layer as shipped in architecture 2 (the facility-obligor grain, the UTC limit clock and the customers not
  yet grouped as devices; each band's expected arrivals split flagged and not flagged): measured with a cracker that
  executes 6.1, 1.3 and 2.2 it kept every band figure (the in-house round 2 solver had already cleared both
  primaries), and an unflagged arrival figure moves 0.016 a group, so no device of realistic size could move it.
  The three devices stay as mirror devices; the joint ventures booked to the other partner (two memberships under
  2.2) are the silent primary; the band columns became groups, committed exposure, groups flagged, expected
  arrivals and exposure arriving, and the chart one bar per band.
- The joint ventures booked to the other partner as the ask layer's primary (DV-C), spent at stage 4 on 2026-10-21:
  both isolated scored readers built each group's members as a set under 2.2 (the ultimate parent, the customers
  booked to it, every entity GLEIF consolidates into it), so every joint venture counted in both groups without being
  noticed, and with 6.1, 1.3 and the GLEIF placement executed both kept 18 of 34 ask figures (52.9 per cent) while
  missing the call at 64. A device that a filed rule resolves for anyone who executes it is a fork closed in the
  golden's favour, not a device. Re-sited onto the facility records the readers' path runs through, where no
  sentence speaks: the ledger's facilities booked twice beside genuine same-day tranches (DV-D); the joint ventures
  stay as a hazard.
