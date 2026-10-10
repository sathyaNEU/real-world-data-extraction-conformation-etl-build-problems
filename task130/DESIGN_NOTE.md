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
    a priority order, so survivors are a rank inside a group, not a rate); decisive_rule_filed: no;
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

**How households leave TA, which is the whole task.** Once a household has been on the main duty for a few months it leaves TA only when a move-on let reaches it: a social housing let through nominations or a private let through the council's lettings agency. Move-on lets go to every household owed the main duty, wherever it is living (in TA, or at home with family), in order of the date the duty was accepted, within the bedroom size it currently needs, case reference breaking ties. The monthly number of lets by size is planned by the lettings team (the move-on plan). Nothing in the pack states the order; the move-on lets log shows it to anyone who asks who got each let.

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

A competent solver rebuilds each household's stay from its placements, measures how fast main-duty households have been leaving temporary accommodation over the last year by bedroom size (or fits a survival curve on time since the duty was accepted, or shares the plan's lets out over the borough's list) and runs the Tenter House households forward on it, calling off around 140 units; the step that lands it there is forecasting departures as a rate, when after its first months a household leaves only when a move-on let reaches it, lets go borough-wide in duty-date order within each bedroom size against the move-on plan, and Tenter House's households sit near the front of those lists because its flats have gone to the longest-waiting nightly-paid household since 2023, so most of them are reached before 31 March: the queue leaves 48 households (no one-bed, 8 two-bed, 21 three-bed, 19 four-bed).

## The ladder (stage 2 measurements on the simulation core; the build re-measures and asserts)

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

Every rung files a different set of four counts, and none equals the answer in more than one size (asserted). The answer's total is at least 12 per cent from every rung's total (asserted), and both directions occur across rungs (R0 to R2 far above, R3 below).

**Survival properties.** (1) No shipped sentence states the order; the plan, the procedure and the dictionary describe their own fields. (2) The lets log nominates the order only to a solver who asks who got each let; nothing a rate model computes touches it. (3) No arithmetic symptom: rates, curves and plan shares all compute cleanly, every join closes. (4) Not a per-row predicate: a household's fate is its rank inside its size's list, which needs every other open case, including households not in TA. (5) Its enumeration is arithmetic: cumulative plan against rank. (6) No cutover date steps a series; the Brook Meadow handover is in the forward plan. (7) It survives the deletion.

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

1. `tenter_house_calloff_2027.xlsx`: the call-off (units by bedroom size and in total for 1 April 2027) and the weekly cost at the Lot 3 rates in force on the start date; the month-end run-off of households still in the block, October 2026 to March 2027, by bedroom size.
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
