# task130: Tenter House, the replacement units for 1 April 2027 (v2, re-rooted after the v1 portal failure)

v1 (the 2027 large-holder designation of Valencian census sections) failed on the portal on 2026-10-10: both top models filed the golden seven-section answer. The author asked for the stump to be redesigned in this slot. v1's architecture is kept on the card's lineage and its dead ends are carried into `## Tried and rejected` below. This note is the build's one design note from here on. Every count below is measured by the generator and asserted; the stage 2 figures were measured on the simulation core before the pack was cut, and the build record at the end carries the shipped values.

```
DRAW  (checked with ../.claude/skills/fingerprint/guard.py; card re-registered 2026-10-10 as v2)
  Verdict: PASS (two NOTEs, test.same_puzzle_older and test.same_driver_older against task80, differentiated
    on the card: task80 dates a fixed-term status from its conferring event; here a closed group's
    departures are a rank inside a borough-wide priority list against a planned supply)
  Shape: 02 forecast across many periods   Gate G mechanism: method_or_model_selection
  Gap: rule (decisive), then population   Pattern: none (G16 method selection, G2 grain, G11 eligibility)
  Domain: Demographic & Social Science   Subdomain (enumerated): housing (homelessness and temporary accommodation)
  Objective: Forecasting & Predictive Modeling
  Stump strategy: other (rank-ordered rationing: departures come from a planned supply handed out in
    a priority order, so survivors are a rank inside a group, not a rate); decisive_rule_filed: yes (the allocation scheme, Part 6);
    official_decoy: no; validated_decoy: no
  Stakeholder role: temporary accommodation and procurement manager (procurement_lead)
  Context artifact: operations_log (the TA team's weekly position)   Calibration form: none
  Forum: minister_or_cabinet (the cabinet member for housing signs the call-off)
  Forcing event: purchase_order_or_contract (the DPS call-off for 1 April 2027)
  Organisation family: local_government   Opening move: evidence-first
  Personas (guard.py names --geo "United Kingdom, England" --seed 130): Maria Field (the requester,
    TA and procurement manager), Irene Roberts (cabinet member for housing), Eileen Nicholls (housing
    register and lettings manager), Declan Morton (TA placements team leader), Debra Young (finance
    business partner, housing), Nicola Robinson (Corvane's head of property)
As-of date: 2026-09-30 (the extracts run to that day); the forecast date is 2027-03-31
```

**World.** Larkmoor Borough Council (fictional, Kent) houses homeless households it owes the main housing duty in temporary accommodation (TA): bed and breakfast and hostels first, then self-contained flats (private sector leases, nightly-paid flats and Tenter House, a 178-flat converted office block leased from Corvane Property Services since April 2021). On 15 September 2026 Corvane gave notice: the owner has sold the building and wants vacant possession on 31 March 2027. The council stopped placing anyone in Tenter House that day and moves nobody out except into settled housing. Every household still there on 31 March needs a replacement self-contained unit of its bedroom need, called off under the Kent and Medway TA dynamic purchasing system (Lot 3) to start on 1 April 2027. Maria Field has to put the call-off to Irene Roberts in November.

**How households leave TA, which is the whole task.** Once a household has been on the main duty for a few months it leaves TA only when a move-on let reaches it: a social housing let through nominations or a private let through the council's lettings agency. Move-on lets go to every household owed the main duty, wherever it is living (in TA, or at home with family), in order of the date the duty was accepted, within the bedroom size it currently needs, case reference breaking ties. The monthly number of lets by size is planned by the lettings team (the move-on plan). The council's allocations scheme (Part 6, shipped) states the order; the move-on lets log follows it without exception.

**Two layers (client standard).** Layer 1: several sources for one picture (cases, placements, reviews, lets, the plan, the register), a household's stay spread across placement rows, bedroom need revised in a separate reviews file with effective dates, a superseded plan sheet beside the revised one, accepted lets with tenancy starts after the extract, and rates in two lots and two rate years. Layer 2 (`allocation_constraints`, `own:queue-runoff-against-planned-supply`): forecasting a closed group's departures as a rate when they are a rank in a filed priority list worked against a planned supply. Six-point check: the inputs take real work and none of it is planted; the flipping step is a method choice (rate against queue); the prompt and the filed scheme and plan define the quantity so only the queue is defensible; no decoy memo or draft; the method is filed, not recovered from certified figures; the lesson (rationed departures are not a hazard rate) is not one an earlier build teaches.

## Data-native sentence

Tenter House is where the council has put, since April 2023, the household that had waited longest in a nightly-paid flat, so its families sit near the front of every bedroom size's move-on list, and in a world where a household leaves only when a let reaches its place in that list, the block will empty far faster than any rate the borough's TA population has ever left at.

## Gate G

- **Litmus.** No. Every file is correct: the cases, placements, reviews, lets, the plan, the weekly position and the price schedule. No stakeholder states a number the task overturns. The difficulty is forecasting how a closed group runs off when departures are a rationed supply handed out in an order.
- **Primary mechanism:** `method_or_model_selection` (a rate or survival model of leaving against a rank-and-supply model; the second is the process the data was generated by and the lets log reproduces it 100 per cent).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test.** Fill: no file is incomplete; the extracts are complete to 30 September. Semantics: every field means what the dictionary says. Instrument: no instrument can observe who is in Tenter House on 31 March 2027 before that day. The generator asserts the answer is unchanged when the placements are consolidated into one row per household stay (the grain repair) and that the rate reading is unchanged too, and that the two differ.
- **Lens swap.** No. The rate reading and the answer are not one population under two lenses: they are two models of the same future, and they disagree because of the order the departures follow.
- **Deletion test.** Delete the weekly position, the distractors and the price schedule: the rate reading is still the natural forecast and still wrong.
- **No shipped artifact ranks the candidates on the decision question.** The weekly position counts households in TA by type and size on 28 September (past, correct, labelled); nothing forecasts 31 March.

## Stump sentence

A competent solver rebuilds each household's stay from its placements, measures how fast main-duty households have been leaving temporary accommodation over the last year by bedroom size (or fits a survival curve on time since the duty was accepted, or shares the plan's lets out over the borough's list) and runs the Tenter House households forward on it, calling off around 136 units; the step that lands it there is forecasting departures as a rate, when after its first months a household leaves only when a move-on let reaches it, lets go borough-wide in duty-date order within each bedroom size against the move-on plan, and Tenter House's households sit near the front of those lists because its flats have gone to the longest-waiting nightly-paid household since 2023, so most of them are reached before 31 March: the queue leaves 46 households (no one-bed, 7 two-bed, 20 three-bed, 19 four-bed).

## The ladder (stage 2 measured on the simulation core; the shipped values are in the build record below)

| Rung | Construction | 1 / 2 / 3 / 4-bed on 31 March | Total | Killed by |
|---|---|---|---|---|
| R0 | nobody leaves: a unit for every household in the block on 30 September | 29 / 67 / 51 / 26 | 173 | the lets log: households in Tenter House have been leaving it for settled lets every month |
| R1 | the borough's monthly rate of main-duty households leaving TA over the last year, by current need, run six months | 22.5 / 47.7 / 44.0 / 24.4 | 139 | the lets log: lets go in duty-date order; Tenter House households are not average members of their lists |
| R2 | the plan's lets shared out over each size's list in proportion | 24 / 50 / 45 / 24 | 144 | as R1 |
| R3 | survival curve (Kaplan-Meier on time since the duty was accepted) read at each household's elapsed time | 3 / 0 / 4 / 14 | 21 | the list today is longer than the history's average, and the curve knows no plan; the lets log's order refutes it |
| R4 | the queue built from households in TA only (homeless-at-home households left out) | 0 / 0 / 18 / 17 | 35 | the lets log: households living at home receive lets in their place in the order |
| R5 | the queue by bedroom need at the decision, ignoring reviews | 2 / 12 / 30 / 10 | 54 | the reviews file: lets match the need assessed at the let |
| R5' | the queue ordered by TA start date | 4 / 18 / 27 / 19 | 68 | the lets log: the duty date reproduces every let, the TA start date does not |
| R6 | the queue right, the original March plan (no Brook Meadow handover) | to measure | | the plan's revised sheet of 14 September |
| R6' | the queue right, accepted October lets taken out and the full October plan applied on top | to measure | | the plan's notes: October counts include lets already accepted |
| **Answer** | the queue: every open main-duty case, current need, duty date then case reference, against the revised plan | **0 / 8 / 21 / 19** | **48** | |

Every rung files a different set of four counts, and none equals the answer in more than two sizes (asserted; R6 and R6' share the one-bed zero and one other size with it). The answer's total is at least 12 per cent from every rung's total (asserted), and both directions occur across rungs (R0 to R2 far above, R3 below).

**Survival properties.** (1) The order is filed (the allocations scheme, Part 6), as a real council's would be; no sentence says the forecast has to work it against the plan, and the prompt asks a forecasting question a rate answers naturally. (2) The lets log confirms the filed order; it pins nothing hidden. (3) No arithmetic symptom: rates, curves and plan shares all compute cleanly, every join closes. (4) Not a per-row predicate: a household's fate is its rank inside its size's list, which needs every other open case, including households not in TA. (5) Its enumeration is arithmetic: cumulative plan against rank. (6) No cutover date steps a series; the Brook Meadow handover is in the forward plan. (7) It survives the deletion.

## Determinism: the 22 axes

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | households in Tenter House on 30 September 2026 (a live placement there) | procedure pin (no placements in, no moves out except settled); C1: no Tenter House placement starts after 15 September |
| 2 | Unit of account | one household, one replacement unit of its bedroom need | procedure pin |
| 3 | Attribution window | departures counted by tenancy start month | plan dictionary pin |
| 4 | As-of dating | need as assessed at the extract (latest review on or before 30 September) | procedure pin |
| 5 | Version basis | the revised move-on plan of 14 September | plan pin (the original sheet labelled superseded); rung R6 |
| 6 | Denominator | the list: every open main-duty case of that need, wherever living | C2: the lets log, 100 per cent of lets since April 2018 |
| 7 | Weighting | none (counts) | stated |
| 8 | Window length | 1 October 2026 to 31 March 2027 | fixed by the notice |
| 9 | Boundary | a let starting on 31 March vacates by 31 March | plan pin (by tenancy start month) |
| 10 | Rounding | none: every figure is a whole count | C1 |
| 11 | Tie-break | case reference on equal duty dates | C2 on the log; C1: no tie straddles any monthly cumulative cut in any size (asserted) |
| 12 | Maturity | households on the list are past their first 120 days of the duty, where other departures happen | C1: no main-duty household has left TA other than by a let after day 120 since April 2018 (asserted); every list position reached by the plan is past day 120 by 1 October |
| 13 | Order of operations | lets applied month by month in plan order | C1: the cumulative cut gives the same counts in any within-month order |
| 14 | Row order | irrelevant | C1: shuffles |
| 15 | Duplicate resolution | one household per case reference; a household returning on a new case starts a new duty date | dictionary pin; C2 on the log |
| 16 | Identity | case reference joins every file | C1: every placement and let joins one case |
| 17 | Netting | none | n/a |
| 18 | Units | bedrooms, four meaning four or more | dictionary pin |
| 19 | Status semantics | "Accepted, tenancy starts" lets are October lets already counted in the plan | plan notes pin; rung R6' |
| 20 | Integerisation | none needed | counts |
| 21 | Scope of a clause | the procedure's "need as assessed" governs the call-off and the list | pin |
| 22 | Forward window contents | the plan's lets only; no new placements into the block; no reviews after the extract | procedure pins; C1: new main-duty cases join behind every Tenter House household |

**Rivals and their misses on the order (C2 on the lets log, April 2018 to September 2026):** duty date with current need, wherever living: 100 per cent of lets reproduced; TA start date: misses; application date: misses; need at decision: misses on every let after a review; households in TA only: misses every let to a household at home. Counts to be asserted at build.

## Deliverables and criteria

Shape 02. Two files, the visual first-class:

1. `tenter_house_replacement_units.xlsx`: the call-off (units by bedroom size and in total for 1 April 2027) and the weekly cost at the Lot 3 rates in force on the start date; the month-end run-off of households still in the block, October 2026 to March 2027, by bedroom size.
2. `tenter_house_runoff.png`: the month-end households by size, with the call-off marked at March.

Criteria arithmetic: the call-off by size and total (5), the weekly cost (1), 24 month-end cells, the chart and its named parts (about 4): about 34.

## Ask sheet (supplemental-stumping)

- **Ask A, the month-end run-off by size (24 cells).** Use: Declan's team schedules the moves and the Lot 3 starts. Devices, each silent: the October lets already accepted (counted once, in the plan); the plan's September rephasing of one- and two-bed lets across months (half-year totals unchanged, so the call does not move); the Brook Meadow handover in February and March (three- and four-bed). A rate response misses all 24; a queue response on the original plan misses at least 10 cells; a double count misses every October-onward cell in the sizes where accepted lets fall to Tenter House.
- **Ask B, the weekly cost.** The price schedule carries Lot 2 nightly rates and Lot 3 weekly rates, each for 2026/27 and from 1 April 2027 after the uplift; the call-off starts on 1 April 2027 under Lot 3. Devices: the lot, the rate year.
- **Pair arithmetic, on paper.** A response that runs a rate files every count wrong: it keeps the chart parts, a few zero cells at most and possibly the cost structure, about r = 4 of the recommendation block and under 0.15 of the asks. A response that builds the queue right lands the call (about 45) and the asks less what the devices take. Both top responses need to miss the queue for the pair to sit near 25; if one lands it, the pair averages about (45 + 0.6 x 55 + 4 + 7) / 2, about 45. The build therefore stands on the main ladder: at most one response in the field may build the borough-wide duty-date queue with homeless-at-home households and current needs.

## Pack plan

| File | Format | Role |
|---|---|---|
| `ta_placements_2018-04_2026-09.csv` | CSV, 25,000+ rows | spine: every TA placement live on or after 1 April 2018 |
| `homelessness_cases_2026-09-30.csv` | CSV | every case open on or after 1 April 2018: dates, decision, need at decision, closure |
| `bedroom_need_reviews.csv` | CSV | reviews of bedroom need with effective dates |
| `moveon_lets_2018-04_2026-09.csv` | CSV | every move-on let, offer date, tenancy start, bedrooms, landlord; accepted October lets |
| `moveon_plan_2026-27.xlsx` | XLSX | revised plan (14 September), original plan (March), notes |
| `corvane_notice_tenter_house.pdf` | PDF | the owner's notice |
| `tenter_house_closure_procedure.docx` | DOCX | the TA team's procedure for the closure (the pins) |
| `dps_lot2_lot3_price_schedule.xlsx` | XLSX | DPS rates, 2026/27 and from 1 April 2027 |
| `ta_weekly_position_2026-09-28.xlsx` | XLSX | context artifact: households in TA by type and size |
| `accommodation_register_2026-09.csv` | CSV | TA units: block, unit, bedrooms, type |
| `housing_needs_extracts_dictionary.txt` | TXT | field definitions |
| `housing_register_lets_2025-26.csv` | CSV | distractor: every social let in the borough to every register band |
| `ta_spend_monitoring_2026-27_q1.xlsx` | XLSX | distractor: TA spend monitoring |

## Prompt

Evidence-first: opens on Corvane's notice. Prose, first person, the two files, units inside the sentences. Nothing about lets, order, the list or rates.

## Build record

Stage 3, 2026-10-10. Generator `generator/build.py` (modules `world`, `sim`, `extracts`, `docs`, `distract`, `xlcalc`, `postprocess`), estimators `generator/estimators.py`, goldens `generator/golden.py` (reads `target/` only), assertions `generator/checks.py` (108, green), independent verifier `generator/verify.py` (plain pandas and loops, shares no code with the generator, green). Seed 130. Two scratch builds and the task-folder build byte-identical; goldens byte-identical across runs; containers audit clean on `target/` and `golden/`.

**Pack as built.** 13 files, 5 formats (csv, xlsx, pdf, docx, txt). `ta_placements_2018-04_2026-09.csv` 27,981 rows (spine); `homelessness_cases_2026-09-30.csv` 13,997 cases; `moveon_lets_2018-04_2026-09.csv` 5,280 lets (5,262 started, 18 accepted with October starts); `bedroom_need_reviews.csv` 204 reviews. Distractors in `metadata.json`: `housing_register_lets_2025-26.csv`, `ta_spend_monitoring_2026-27_q1.xlsx`, `ta_weekly_position_2026-09-28.xlsx`.

**Departures from the stage 2 plan.** The random history shifted with every generator change, so the move-on plan's monthly phasing is settled in `build.tune_plans`: single lets moved between adjacent months (half-year totals fixed) until no monthly cut falls inside a same-day tie that mixes Tenter House and other households; the March original plan is given its own front-loaded phasing with the one- and two-bed totals unchanged. Revised plan totals 89, 117, 56 and 19 lets.

**The answer as built.** 170 households in Tenter House on 30 September (28 / 66 / 50 / 26 by need). Call off 46 units: 0 / 7 / 20 / 19. Month ends: one-bed 20, 13, 8, 0, 0, 0; two-bed 57, 46, 42, 32, 21, 7; three-bed 46, 42, 38, 34, 29, 20; four-bed 26, 25, 24, 23, 21, 19. Weekly cost at the Lot 3 2027/28 rates GBP 21,615.23, filed as GBP 21,615.

**The ladder as built (31 March, one- to four-bed, total).** R0 none 28 / 66 / 50 / 26, 170. R1 rate 22 / 47 / 43 / 24, 136. R2 plan share 23 / 50 / 44 / 24, 141. R3 survival 3 / 0 / 4 / 14, 21. R4 TA households only 0 / 0 / 17 / 17, 34. R5 need at decision 2 / 11 / 29 / 10, 52. R5' TA start order 3 / 17 / 26 / 19, 65. R6 original plan 0 / 7 / 26 / 23, 56. R6' accepted lets counted twice 0 / 3 / 17 / 19, 39. Every rung distinct, none matching the answer in more than two sizes, every total at least 12 per cent from 46 (nearest R5, 52), rungs both above and below.

**C2 on the lets log.** Duty date then case reference within current need, every open main-duty case wherever living: 5,262 of 5,262 lets. TA start date 308; application date 306; households in TA only 4,434; need at decision 2,229. No main-duty case has closed after day 120 other than by a let since April 2018; every household the plan reaches is past day 120 on 1 October; the accepted October lets are the front of each list.

**Checks run.** `leak.py --asof 2026-09-30`: REVIEW, no LEAK (answered below). `guard.py heart`: PASS (two NOTEs against task80, differentiated). `guard.py surface`: three promoted pairs (task100, task87, task80), adjudicated by the clone pre-flight. Clone pre-flight (`clone_check_report_task130.md`): shape echo only, against task86 (a bedroom-size waiting list in the same domain, different driver) and task125 (an English council's April 2027 call-off); no reject-tier finding. The deliverable stem was renamed from `calloff_2027` to `replacement_units` and the card's differentiation now names task86, task50 and task125.

**Determinism judge, pass 1 (2026-10-10):** DETERMINISTIC, FIX_NOW. Every figure reproduced (170, 46 and 0 / 7 / 20 / 19, all 24 month-end cells, GBP 21,615.23, the 5,262-let replay). The one fix: the price schedule, last modified 22 September 2026, cited September 2026 CPI, which is published in October; it now cites August 2026 CPI in the schedule and the golden note, no rate moved. Also taken: critical component 1 reads "at the end of 30 September"; this note's stage 2 answer and ladder claims brought up to the build. Not taken: the judge's low note that a lets log following the order without exception is tidier than a real one (the exceptions would make the order a judgment call, which Gate C forbids).

**Determinism judge, pass 2 (2026-10-11):** DETERMINISTIC, FIX_NOW, every figure reproduced again (170; 46 as 0 / 7 / 20 / 19; all 24 cells; GBP 21,615; the 5,262-let replay; every rival ruled out by a shipped file). Findings were dates and labels, taken in the generator with no graded figure moving (checks and verifier re-run, diff confirmed): the move-on plan's saved date moved from 14 September to 1 October (it carries September's lets and lets accepted on offers made to 30 September); accepted lets now all start in October (one had started on 3 November while the plan counts it in October); the golden workbook re-dated 6 October; the register's lease label now reads to 31 March 2027. The pipeline's one re-judge is spent; no third pass was run.

Stage 6, ship, 2026-10-11. `target.zip` cut from the final rebuild: 13 members, 781,402 bytes, sha256 48249e0a96558440dc28e5306dbe053eb9f8bfaf2f52db1efcf59b626263f16c. Byte-identical double build, containers clean, `leak.py` REVIEW with no LEAK, `guard.py heart` PASS.

2026-10-11, client two-layer standard: the allocation order, previously recoverable only from the lets log, is now filed as the council's Housing Allocations Scheme 2024, Part 6 (`housing_allocations_scheme_2024_part6.pdf`), because the client caps a method recovered from records. No figure moved (109 assertions, verifier green, byte-identical rebuild); the judge was not re-run for a filed pin that changes no figure.

## Leak review

`leak.py task130 --asof 2026-09-30`, REVIEW, no LEAK. The dictionary and the closure procedure share ordinary words with the call (call off, replacement units, bedrooms) and carry no figure. Corvane's letter shares three generic stump terms (housing, register, repair). The procedure's point 5 is flagged as an announcement: it is the bedroom-need pin for the call-off, a convention the procedure would state anyway, and it says nothing about how households leave. The 18 dates after 30 September are the accepted October lets' tenancy start dates, forward by design.

## Tried and rejected

v1 (large-holder designation, failed on the portal), carried over:

- The blueprint's stated-memo architecture (a methodology memo fixing the holdings rows, the amendment semantics, the unit-by-filing-date rule, CUSIP repair and the denominator source): rejected because a strong solver implements every stated clause, so the bridge becomes a computation; its traps are kept only as lower rungs.
- Capital-markets ownership kept literally (13F holders, issuers, shares outstanding) under an accepted domain label: rejected, markets trading is outside Economics and none of the nine owns a vendor's crowding flag without a relabel a reviewer would not accept.
- Confidentially omitted holdings recovered from another public disclosure as the decisive rung: rejected on the clean-data test, the public returns are a filtered file whose repair hands the natural pipeline the answer (sole_data_defect yes).
- Denominator timing (dwellings or shares outstanding taken at a later date than the holdings) as the decisive rung: rejected on the clean-data test (a stale file whose repair collapses the task) and as a single-fact flip.
- Holders whose returns are not yet due completed from the title register: rejected, the incomplete feed is a suspect file under the clean-data test, and the register-to-titles route is a schema-visible two-hop join a strong solver takes.
- Double reporting under a non-exclusive holding definition: rejected, the regime text that makes both returns correct concedes the overlap, and dwelling-level returns are deduplicated by reference by default.
- Agent-filed returns and nominee title holders as the decisive rung: rejected as a lens swap, registrant against owner of the same dwellings on the same date.
- Employer concentration with PEO look-through as the re-skin: rejected, it drops the ownership scenario and co-employment look-through is textbook.
- Passive holders re-derived at a forward date around an index change: rejected, out-of-scope domain and textbook.
- The agency's takeovers evidenced by preventive annotations in the deed extract: rejected, the evidence would sit in the forward roll's own source.
- Settled large-holder takeovers as the clock's evidence: rejected, a back-test mismatch sends the solver to the ledger.
- The programme order naming the first-offer programme: rejected, a sentence in the document that defines the quantity sends every solver looking.
- A bridge from the raw lodged rows to the conformed total, and a bridge with one bar per kind of movement: rejected, free weight and a taxonomy fork.
- Round 1 (plain) landed v1's six-section answer: the agency's first-offer takeovers in a budget ledger with a 120-day clock recovered from settled deeds died because the solver audited the ledger for transfers unprompted.
- Hardening loop 1's pre-registered repair (re-key the ledger by expedient in a second file): rejected before building, it only hides a step the solver completed.
- Portal 2026-10-10, the hardened v1 (holders inscribed after 30 June rung): failed, both top models filed the golden seven sections. Any rung that is a record a diligent solver can find and join is solved; the certified-bulletin reproduction blessed the path instead of hiding it.

Re-root (v2):

- Staying in the large-holder world with a property-against-dwelling grain stump (undivided buildings counted as one return row but holding several flats): rejected, the judge's lens-swap example (rank by logo count when the decision needs seats) is this move, and a dwelling-grain return collapses it.
- Staying in the large-holder world with any further hidden record (a licence register for new blocks, an inheritance date, a section split): rejected, the portal solvers join every record they can reach.
- The tensioned-zone rent burden from a deposit register (stock against flow, rents indexed on each anniversary): rejected, the update rules would have to be filed and a filed rule is a computation; the stock-and-flow reading is also close to a semantic fork on "rent".
- A survival-curve stump on the whole TA population (length-biased stock, pooled leaving rate as the decoy): rejected after simulation, in near steady state the pooled rate and the duration-conditional forecast agree within 4 per cent on the TA total because the stock's slow leavers and the new entrants' fast leavers offset; and "last year's stock survival" lands within 3 per cent.
- The same survival stump on a closed cohort: rejected, the gap opens (12 per cent against a rate) but a survival curve is the textbook answer to a closed-cohort question and a strong solver fits one; it is kept as a wrong rung (R3) because the departures are rationed, not hazards.
- Tenter House filled in order of each household's first move out of emergency accommodation: rejected after simulation, the block's positions in the lists were left to chance and swung from front-heavy to back-heavy between seeds, so the call was an accident of the history; the 2023 longest-in-nightly-paid lettings rule makes the positions a property of the world.
- v2 as first shipped: the move-on order left unfiled and recoverable only from the lets log; replaced by a filed allocations scheme extract under the client's two-layer standard, which caps a method hidden and recovered from records. A scheme clause letting main-duty households also bid through HomeChoice was drafted and cut, because it opens a second exit route the plan does not count.
