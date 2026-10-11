# task130: Tenter House, the replacement units for 1 April 2027 (v2, hardening loop 1)

v2 failed on the portal on 2026-10-11: the reported model built the duty-date queue the allocations scheme files, worked the record's bedroom need against the revised plan and filed the golden, 46 units (0 / 7 / 20 / 19) at GBP 21,615 a week. The author asked for the stump to be improved in this slot, so this is hardening loop 1 on architecture v2: the same world, the same question and the same queue, with the lists rebuilt on the household's need on the day of each offer round. Every count below is measured by the generator and asserted.

```
DRAW  (checked with ../.claude/skills/fingerprint/guard.py, 2026-10-11, loop 1)
  Verdict: PASS (NOTE test.same_puzzle_older against task102, differentiated on the card: task102 moves
    payments across a fiscal-year boundary; here a household attribute is worked out on each allocation
    day from the members' ages against a case record that holds it as last assessed). heart PASS.
  Shape: 02 forecast across many periods   Gate G mechanism: method_or_model_selection
  Gap: time (decisive), then population   Generators: G13 horizon mismatch, G11 eligibility precondition,
    G16 method selection
  Domain: Demographic & Social Science (client domain Urban & Regional Science)   Subdomain: housing
  Objective: Forecasting & Predictive Modeling
  Stump strategy: time_semantics (the as-of date of the need decides which list a household is on);
    decisive_rule_filed: yes (scheme Part 3 and 6.4); official_decoy: no; validated_decoy: no
  Layer 2: allocation_constraints, own:queue-classes-recomputed-on-the-day
  Stakeholder role: temporary accommodation and procurement manager (procurement_lead)
  Context artifact: operations_log (the TA team's weekly position)   Calibration form: none
  Forum: minister_or_cabinet   Forcing event: purchase_order_or_contract   Organisation: local_government
  Opening move: evidence-first
  Personas (guard.py names --geo "United Kingdom, England" --seed 130): Maria Field (the requester),
    Irene Roberts (cabinet member for housing), Eileen Nicholls (housing register and lettings),
    Declan Morton (TA placements team leader), Debra Young (finance), Nicola Robinson (Corvane)
As-of date: 2026-09-30 (the extracts run to that day); the forecast date is 2027-03-31
```

**World.** Larkmoor Borough Council (fictional, Kent) houses homeless households it owes the main housing duty in temporary accommodation (TA): bed and breakfast and hostels first, then self-contained flats (private sector leases, nightly-paid flats and Tenter House, a 178-flat converted office block leased from Corvane Property Services since April 2021). On 15 September 2026 Corvane gave notice for vacant possession on 31 March 2027. No placements go in after that day and nobody moves out except into settled housing. Every household still there on 31 March moves on 1 April into a replacement self-contained unit called off under Lot 3 of the Kent and Medway TA DPS. Maria Field puts the call-off to Irene Roberts in November.

**How households leave TA.** After its first months under the main duty a household leaves TA only when a move-on let reaches it. Lets are offered in monthly rounds: the round for tenancies starting in a month is held on the third Monday of the month before, and each home goes to the first household, by the date the duty was accepted (case reference on the same date), among every main-duty household in the borough, in TA or not, that needs its number of bedrooms on the day of the round (scheme 3.4, 6.3 and 6.4). Need is the bedroom standard in Part 3, worked out from the people on the application: a child reaching ten (sharing with a child of the other sex) or sixteen can add a room, and a household needing five or more waits for a home that size. The case record carries the need assessed at the decision and reassessed only when a birth is reported, when the TA team checks a household before a move, and when the lettings team checks it before an offer. Nobody reports a birthday, so the record lags the household, and it lags most for the longest-waiting households at the front of every list.

**Two layers (client standard).** Layer 1: several sources for one picture (cases, placements, reviews, household members, lets, the plan, the register); the case record's need, assessed at events, beside the members on the housing register; a household's stay spread across placement rows; offers dated by round, with the October lets already accepted and starting after the extract; a superseded plan sheet beside the revised one and a five-or-more row of zeros; rates in two lots and two rate years. Layer 2 (`allocation_constraints`, `own:queue-classes-recomputed-on-the-day`): a queue whose classes are an attribute the governing rule works out on the day, forecast as if the attribute were the value on the record. Six-point check: the inputs take real work and none of it is planted (the record says what it is, an assessment at a dated event); the flipping step is a method choice (the record's need against the standard applied on each round day); the scheme defines the quantity so only the second is defensible; no decoy memo, draft or certified figure; the method is filed (Part 3, 6.4), not recovered from records; the lesson (a class defined by age is not a fixed attribute) is not one an earlier build teaches.

## Data-native sentence

A household waits years for a move-on let, and in those years its children grow up: the scheme offers each home to the household that needs its bedrooms on the day of the round, but the case record still holds the need assessed when the duty was accepted, so the households at the front of every list, the ones Tenter House was filled with, are exactly the ones the record most often has on the wrong list.

## Gate G

- **Litmus.** No. Every file is correct: the case record's need is the need assessed on its dated events, the members are as the register holds them, the lets log, the plan, the weekly position and the price schedule are right. No stakeholder states a number the task overturns.
- **Primary mechanism:** `method_or_model_selection` (lists on the record's need against lists on the standard applied on each round day; the scheme pins the second and the September round confirms it, 49 of 49 lets against 25 of 49).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test.** Fill: every extract is complete to 30 September. Semantics: every field means what the dictionary says, the record's need included. Instrument: nothing observes who is in Tenter House on 31 March 2027 before that day. The generator asserts the answer is unchanged when the placements are consolidated into one row per stay, and that the record-based reading is unchanged too.
- **Lens swap.** No. The record's need and the standard's need are not one population under two lenses: they are the same attribute on two dates, and the scheme says which date governs.
- **Deletion test.** Delete the weekly position, the distractors and the price schedule: the record-based queue is still the natural build and still wrong.
- **No shipped artifact ranks the candidates on the decision question.** The weekly position counts households by the unit they occupy on 27 September; nothing forecasts 31 March.

## Stump sentence

A competent solver builds the borough-wide duty-date queue the scheme files, takes each household's bedroom need from the case record (the need at the decision, updated by the reviews file), works it against the revised plan with the accepted October lets taken out, and calls off 66 units (no one-bed, 19 two-bed, 35 three-bed, 12 four-bed); the step that lands it there is taking the recorded need as the household's need, when the scheme offers each home to the household that needs its number of bedrooms on the day of the round, worked out from the people on the application, and the record lags children reaching ten and sixteen for the long-waiting households at the front of every list: lists rebuilt from the household members on each round day, with five-or-more households waiting for homes that size and each unit sized on the need on 1 April, leave 52 households (no one-bed, 10 two-bed, 18 three-bed, 24 four-bed).

## The ladder (measured on the shipped pack; one- to four-bed on 31 March, total, cells of 24 that miss)

| Rung | Construction | 31 March | Total | Cells off | Killed by |
|---|---|---|---|---|---|
| R0 | nobody leaves | 26 / 56 / 47 / 31 | 160 | 23 | the lets log: Tenter House households leave for lets every month |
| R1 | the borough's monthly leaving rate by recorded need, run six months | 20 / 44 / 46 / 19 | 129 | 24 | the scheme: lets go in duty-date order, not at a rate |
| R2 | the plan's lets shared over each recorded-need list in proportion | 22 / 45 / 47 / 18 | 132 | 24 | as R1 |
| R3 | Kaplan-Meier on time since the duty, by recorded need | 0 / 6 / 24 / 16 | 46 | 20 | as R1; the curve knows no plan |
| R4 | the queue right, households in TA only | 0 / 4 / 17 / 23 | 44 | 11 | scheme 6.1: households at home are on the list |
| **R5 (stump)** | **the queue on the case record's need on 30 September, four or more as one list** | **0 / 19 / 35 / 12** | **66** | **18** | scheme 3.4 and 6.4: need on the day of the round under Part 3; the September round, 49 of 49 lets on the members against 25 of 49 on the record |
| R5a | the record's lists, units sized on 1 April, sizes exact | 0 / 18 / 33 / 16 | 67 | 14 | as R5 |
| R6 | Part 3 from the members, worked out once on 30 September for every round | 0 / 10 / 19 / 24 | 53 | 2 | scheme 6.4: the day of each round |
| R6a | Part 3 worked out once on 1 April for every round | 0 / 9 / 18 / 24 | 51 | 2 | as R6 |
| R7 | the lists right, units sized on the 30 September need | 0 / 11 / 19 / 22 | 52 | 18 | procedure point 5: the need on 1 April |
| R8 | the lists right, four or more as one list | 0 / 10 / 18 / 23 | 51 | 5 | scheme 3.4: a home goes only to a household that needs its bedrooms; the plan's five-or-more row |
| R9 | the lists right, the superseded March plan | 0 / 10 / 25 / 27 | 62 | 10 | the plan's revised sheet |
| R10 | the lists right, the accepted October lets taken out and October's plan applied again | 0 / 0 / 16 / 22 | 38 | 21 | the plan's note: October is the round of 21 September |
| R11 | the lists right, ordered by first TA placement | 0 / 15 / 24 / 23 | 62 | 16 | scheme 6.3 |
| **Answer** | the lists on Part 3 need on each round day, every main-duty household, exact sizes, units on the 1 April need, the revised plan | **0 / 10 / 18 / 24** | **52** | 0 | |

Every rung files a distinct vector and none lands the answer (asserted). The stump rung misses 18 of the 24 month-end cells and three of four sizes, and its total is 27 per cent high. The second-level rungs (R6, R6a, R7, R8) are one step short of the answer and each misses at least one size; R7 matches the total because it re-sizes the same households, and misses three sizes.

**Survival properties.** (1) Every rule is filed: the order (6.3), the rounds and the need on the round day (3.4, 6.4), the standard (3.1), the unit size on 1 April (procedure point 5). (2) The record's need is a real field and is correct for its dated assessments; nothing in the pack is planted. (3) No arithmetic symptom: the record-based queue computes cleanly and every join closes. (4) Not a per-row predicate: a household's fate depends on every other household's need on each round day. (5) The replay on the record's need reproduces 3,668 of 5,257 lets since April 2018 and 25 of the 49 September-round lets, a failed back-test a solver has to act on; the members reproduce all 49. (6) The difficulty survives deleting every distractor and the weekly position.

## Determinism: the 22 axes

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | households in Tenter House on 30 September 2026 (a live placement there) | procedure pins (no placements in, no moves out except settled); C1: no placement starts after 15 September |
| 2 | Unit of account | one household, one replacement unit | procedure pin |
| 3 | Attribution window | departures by tenancy start month | plan pin |
| 4 | As-of dating | list need on each round day; unit size on 1 April | scheme 3.4 and 6.4; procedure point 5; C1: the September round reproduces 49 of 49 on the members |
| 5 | Version basis | the revised plan of 14 September | plan pin (the original labelled superseded); rung R9 |
| 6 | Denominator | every open main-duty case of that need, wherever living | scheme 6.1; rung R4 |
| 7 | Weighting | none (counts) | stated |
| 8 | Window length | 1 October 2026 to 31 March 2027 | the notice |
| 9 | Boundary | a let starting by 31 March vacates by 31 March; the round on 15 February is March's | scheme 6.4; plan pin |
| 10 | Rounding | none: whole counts; the cost to the nearest pound | prompt |
| 11 | Tie-break | case reference on equal duty dates | scheme 6.3; C1: no round's cut splits a same-day tie mixing Tenter House and other households (asserted) |
| 12 | Maturity | households reached are past day 120 of the duty | C1: no main-duty case left after day 120 other than by a let since 2018; every household a round reaches is past day 120 (asserted) |
| 13 | Order of operations | rounds in month order; within a round sizes are independent | C1: a household is on one list on a given day |
| 14 | Row order | irrelevant | C1 |
| 15 | Duplicate resolution | one household per case reference | dictionary pin |
| 16 | Identity | case reference joins every file | C1: every placement, review, member and let joins one case |
| 17 | Netting | none | n/a |
| 18 | Units | lists by exact bedrooms; units 1 to 4, four meaning four or more | scheme 3.4; procedure point 5; the plan's five-or-more row of zeros; rung R8 |
| 19 | Status semantics | accepted lets are the September round, October's whole supply | plan note pin; C1: the plan's October column equals the accepted lets; rung R10 |
| 20 | Integerisation | none needed | counts |
| 21 | Scope of a clause | Part 3 need governs the lists and the unit; the case record governs neither | scheme 3.4, 6.4; procedure point 5 |
| 22 | Forward window contents | the plan's lets only; the people on the application on 30 September (no births after the cut) | procedure point 5 ("counting the people listed on its application on 30 September 2026"); C1 |

## Deliverables and criteria

Shape 02, two files, the visual first-class: `tenter_house_replacement_units.xlsx` (the call-off by size and in total for 1 April 2027 and its weekly cost at the Lot 3 rates in force on the start date; the month-end households October 2026 to March 2027 by replacement unit size) and `tenter_house_runoff.png` (the month-end households by size with the call-off marked at March). Criteria: the call-off by size and total (5), the weekly cost (1), 24 month-end cells, the chart and its named parts (about 4): about 34.

## Ask sheet (supplemental-stumping)

- **Ask A, the month-end run-off (24 cells).** Devices, each silent: the October lets already accepted (counted once); the plan's rephasing; the Brook Meadow handover in February and March; the lists on each round day (three Tenter House households change size before 1 April); five-or-more households staying. The stump rung misses 18 cells, the rate rungs all 24, R6 2, R8 5, R9 10, R10 21.
- **Ask B, the weekly cost.** Lot 2 nightly rates and Lot 3 weekly rates, each for 2026/27 and 2027/28; the units start 1 April 2027 under Lot 3. Devices: the lot, the rate year. GBP 24,512.30, filed as GBP 24,512; neither wrong basis rounds to it (asserted).
- **Pair arithmetic.** A response on R5 keeps the one-bed zero, a few cells and possibly the cost structure: about 10 to 15. A response on R6 or R8 misses the call by one unit in one size and keeps most cells: about 55 to 65. A response on the answer lands about 90. The build stands if both top responses stop at R5 or below, or one at R5 and the other at R6 or R8: (15 + 60) / 2, under 40.

## Pack plan

| File | Format | Role |
|---|---|---|
| `ta_placements_2018-04_2026-09.csv` | CSV, 27,987 rows | spine: every TA placement live on or after 1 April 2018 |
| `homelessness_cases_2026-09-30.csv` | CSV, 14,038 rows | every case open on or after 1 April 2018: dates, decision, need at the decision, closure |
| `bedroom_need_reviews.csv` | CSV, 248 rows | later assessments that changed a case's recorded need (birth reported, TA move, offer) |
| `household_members_2026-09-30.csv` | CSV, 6,871 rows | the people on the application of each of the 2,181 open cases: relationship, sex, date of birth |
| `moveon_lets_2018-04_2026-09.csv` | CSV, 5,319 rows | every move-on let since April 2018 (5,270 started; 49 accepted in the September round) |
| `moveon_plan_2026-27.xlsx` | XLSX | revised plan (14 September), original plan (March), notes |
| `housing_allocations_scheme_2024_parts_3_and_6.pdf` | PDF | the bedroom standard and the main-duty lettings rules |
| `corvane_notice_tenter_house.pdf` | PDF | the owner's notice |
| `tenter_house_closure_procedure.docx` | DOCX | the TA team's procedure for the closure (point 5 sizes the units) |
| `dps_lot2_lot3_price_schedule.xlsx` | XLSX | DPS rates, 2026/27 and 2027/28 |
| `ta_weekly_position_2026-09-28.xlsx` | XLSX | distractor: households in TA by type and unit size |
| `accommodation_register_2026-09.csv` | CSV | TA units: type, address, bedrooms, provider |
| `housing_needs_extracts_dictionary.txt` | TXT | field definitions |
| `housing_register_lets_2025-26.csv` | CSV | distractor: every register and transfer let in 2025/26 |
| `ta_spend_monitoring_2026-27_q1.xlsx` | XLSX | distractor: TA spend monitoring |

## Prompt

Evidence-first, unchanged from v2 except two clauses: the call-off sentence no longer says each household is matched on its current assessed need (the procedure sizes the units), and the month-end table is counted by the size of replacement unit each household will move into. 262 words, voice-check clean.

## Build record

v2 as first shipped, 2026-10-11: 46 units (0 / 7 / 20 / 19), GBP 21,615.23 a week, two judge passes DETERMINISTIC with FIX_NOW applied, `target.zip` cut and delivered. Failed on the portal the same day.

Loop 1, 2026-10-11. The simulation keeps its seed (130) and now carries each household's members: need is the bedroom standard on the day; lets go in rounds on the third Monday of the month before by need on the round day; Tenter House flats go by the need checked on the day; the case record is assessed at the decision, at reported births (7 to 60 days after), at TA moves and at offers. Plans: the revised November to March phasing settled by `build.tune_plans` so no round's cut splits a mixed same-day tie (one one-bed let moved from January to November); October is the September round as made. Generator `generator/build.py`, estimators `generator/estimators.py`, goldens `generator/golden.py`, assertions `generator/checks.py` (142, green), independent verifier `generator/verify.py` (plain loops and a brute-force bedroom standard, green). Two scratch builds and the task-folder build byte-identical, `target/` and `golden/`; containers audit clean.

**The answer as built.** 160 households in Tenter House on 30 September; by the unit each needs on 1 April 26 / 56 / 47 / 31. Call off 52 units: 0 / 10 / 18 / 24. Month ends: one-bed 20, 10, 4, 0, 0, 0; two-bed 49, 41, 35, 26, 18, 10; three-bed 43, 38, 35, 31, 26, 18; four-bed 31, 30, 30, 29, 26, 24. Weekly cost at the Lot 3 2027/28 rates GBP 24,512.30, filed as GBP 24,512.

**Device sizes.** The record's need differs from Part 3 on 30 September for 17 Tenter House households and 139 of the 1,827 open main-duty cases. Three Tenter House households change size between 30 September and 1 April; twelve need five or more bedrooms. Replay: the members reproduce 49 of 49 September-round lets; the record 25 of 49, and 3,668 of 5,257 lets since April 2018.

## Leak review

(loop 1: filled after `leak.py` and the reader)

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

Hardening loop 1 (after the v2 portal failure, 2026-10-11):

- Portal 2026-10-11, v2 as shipped: failed; the reported model built the filed duty-date queue on the case record's need against the revised plan, took the accepted October lets out once and filed the golden 46 (0 / 7 / 20 / 19) at GBP 21,615. Once the order was filed, the queue was a computation.
- Ageing alone (the members' birthdays inside the window moving households between lists) as the decisive device: rejected after measurement on seeds 130 to 166, it moves two to four Tenter House households in six months and leaves a solver who freezes need on 30 September within one unit, often on the same total; kept as the second-level rung R6.
- Exact-size lists for households needing five or more as the decisive device: rejected, it is one filed sentence and a plan row away and moves only the four-bed count; kept as R8.
- Tenter House flats let on the case record's need (the record then stale for 27 per cent of the block): rejected, it fills the block with families in flats too small for them, which reads as a data defect; flats go on the need checked on the day, as a TA move would.
- Reassessing the record for every household near the front of a list before each round, so that a replay on the record reproduces every let: rejected before building, the lets log would then bless the record until the forward rounds broke it, the validated-record shape the client bans; the record is reassessed only for the household offered.
