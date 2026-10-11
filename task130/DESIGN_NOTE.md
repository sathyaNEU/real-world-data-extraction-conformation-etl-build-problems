# task130: Red Cedar Valley, the care-management baseline for 2027-28 (v3, re-rooted after v2 was spent)

v1 (a 2027 large-holder designation) and v2 (the Tenter House replacement-unit call-off) are spent: v1 failed on the portal, v2 failed on the portal and its hardening loop came back from the clone pre-flight as a Template of task73 world ten (the same move had already been solved on the portal in task86 v2). Both are on the card's lineage and their dead ends are in `## Tried and rejected` below. v3 is the third and last architecture this number gets.

```
DRAW  (guard.py check and register, 2026-10-11; refined before the ladder was cut, same card)
  Verdict: PASS
  Shape: 14 cuts of a distribution (the baseline by Northcourt's four risk tiers, medical and pharmacy)
  Gap: objective (decisive), then population   Pattern: A (past exceedance against forward yield)
  Generators: G14 conditioned yield, G13 horizon mismatch   Gate G mechanism: forecasting
  Domain: Actuarial Science & Insurance   Task type: claims-frequency-severity
  Objective: Forecasting & Predictive Modeling
  Stump strategy: forecast_method_backtest (persistence, the natural projection, is wrong out of sample for a
    cohort chosen on its outcome; the bid cohort's realised year is the back-test); decisive_rule_filed: no
    (Schedule C defines the estimand, not a method); official_decoy: no; validated_decoy: no
  Layer 2: estimand_identification, own:selection-on-the-outcome-baseline   Calibration form: other (the bid
    cohort list, its outcomes read from the claims)
  Stakeholder role: director of risk management and benefits (procurement_lead)
  Context artifact: filed_model (the vendor's stratification exports)
  Forum: trustees_or_governors (the school board)   Forcing event: purchase_order_or_contract
  Organisation: university_or_school   Opening move: stakes-first
  Personas (guard.py names --geo "United States" --seed 130): Joyce Salinas (requester, director of risk
    management and benefits), Deborah Johnson (board chair), Anthony Olsen (chief financial officer),
    Michael Perry (consulting actuary, Lindqvist Benefits Consulting), Allison Santiago (Northcourt account
    lead), Tiffany Barrett (benefits analyst)
As-of date: 2027-03-12 (claims paid through 28 February 2027); the programme year is 1 April 2027 to 31 March 2028
```

**World.** Red Cedar Valley School District (fictional, Minnesota) self-insures the health plan for about 6,000 covered members (employees, early retirees under 65, spouses and children). A third-party administrator has run the medical plan since 1 January 2025, when it replaced the previous administrator and issued new member identifiers (a conversion crosswalk maps the old ones); pharmacy runs through a PBM keyed on the district's employee number and a person code. In January 2025 the district tendered for high-cost care management with a programme year from 1 April 2025; the bidders stratified the plan's 2024 claims, and Northcourt Care Partners' bid flagged 140 members in four risk tiers on its acuity score. The award was suspended in April 2025 under the district's budget freeze and no services were provided. The services agreement was signed in February 2027 for a programme year from 1 April 2027; Northcourt stratified the plan's 2026 claims with the same model and the 140 members on its final list are enrolled from 1 April. Northcourt is paid 40 per cent of the savings, the difference between the baseline and the enrolled members' actual allowed claims per member month in the programme year, tier by tier and benefit by benefit. Joyce Salinas certifies the baseline and the board approves it on 25 March 2027.

**Why this is hard.** The 140 members were chosen because their 2026 claims put them at the top of the plan. A cost that high is partly lasting (dialysis, specialty drugs, a chronic condition) and partly a one-off (a transplant, a premature birth, trauma, a hepatitis C cure, a cancer course that ends), and the one-off part does not come back. Projecting each tier's 2026 claims forward at the renewal trend, which is how the plan projects every other group and which is right for any group not chosen on its claims, certifies a baseline several times what the cohort will cost, and Northcourt is paid for savings the members were always going to show. The plan's own record holds the answer: the 140 members Northcourt flagged with the same model on 2024 claims were never enrolled, and their allowed claims in the year from April 2025, the programme year they were flagged for, are what a flagged member costs the following year without the programme, tier by tier and benefit by benefit.

**Two layers (client standard).** Layer 1: medical claim lines with replacements, voids and denied lines; pharmacy claims from the PBM with reversals in its own layout and keyed on employee number and person code; eligibility as coverage spans; the administrator change on 1 January 2025 with a conversion crosswalk (the bid list carries the old identifiers); claims history that starts with the new administrator; run-out on the latest year; a superseded draft stratification beside the final one. Layer 2 (`estimand_identification`, `own:selection-on-the-outcome-baseline`): a cohort chosen on an extreme value of a noisy outcome is forecast by carrying its own value forward, when the outcome regresses toward the mean; the counterfactual is the next-period experience of a cohort chosen the same way and left untreated, which the plan's record contains. Six-point check: the inputs take real work (lines, replacements, reversals, two key systems, the conversion, member months) and none of it is planted; the flipping step is a method choice (persistence against the untreated cohort's realised year); Schedule C defines the estimand (expected claims in the programme year without the programme) and the bid cohort makes the analog the design-implied estimator; no decoy memo and no filed method that gives the wrong answer; the method is not recovered from certified figures; the lesson (a cohort chosen on its outcome regresses) is not one an earlier build teaches.

## Data-native sentence

Northcourt picked the 140 members the plan paid most for in 2026, and a year of the highest claims in a self-insured plan is mostly the year someone had the transplant, the premature baby, the hepatitis C cure or the car crash, so the members who top the list are the ones whose next year looks least like their last; the district already watched it happen to the 140 members Northcourt flagged in its 2025 bid, who were never enrolled.

## Gate G

- **Litmus.** No. Every file is correct: the claims, the eligibility, the crosswalk, both stratification lists, the agreement, the renewal letter. No stakeholder states a number the task overturns.
- **Primary mechanism:** `forecasting` (a forecast the correctly read past does not pin: the 2026 claims are right and are not the forecast).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test.** With perfectly clean claims, the persistence projection is still the natural one and still wrong; the bid cohort's realised year is what refutes it.
- **Deletion test.** Delete every distractor (rebates, stop-loss, the draft list): the persistence projection is still natural and still wrong.
- **No shipped artifact ranks or forecasts the cohort's cost.** The stratification files carry an acuity score and a tier, never a cost or a predicted cost; the renewal letter projects the whole plan, not the cohort.

## Why the analog's level is the one method (forcing)

- The estimand is Schedule C's: the allowed claims per member month that the enrolled members in each tier would be expected to incur in the programme year without the programme, medical and pharmacy separately, in programme-year dollars at the renewal trend from the midpoint of any experience period to the midpoint of the programme year.
- The bid cohort was chosen by the same model, on the same tiers, on a calendar year of claims, for a programme year starting three months after that year, exactly as the enrolled cohort was; it was never treated. Its realised allowed claims per member month in April 2025 to March 2026, by tier and benefit, projected 24 months at the trend, is the expected cost of a member the model puts in that tier. Midpoint to midpoint is 24 months whichever convention is used.
- The ratio form (the enrolled cohort's 2026 cost times the bid cohort's next-year-over-selection-year ratio) cannot be built: the claims history starts on 1 January 2025 with the new administrator and neither stratification file carries a cost. A cost-only regression on the whole plan does not reproduce the selection, which runs on the acuity score (claims, conditions, specialty drugs and admissions, not cost alone), and its window would not match the three-month lag.
- Members of the bid cohort who left the plan before April 2025 carry no member months and drop out on their own; those who left during the year count for the months they were enrolled.

## Stump sentence

(Figures filled at build.) A competent solver nets the claim lines and the pharmacy reversals, links the members, takes each tier's 2026 allowed claims per member month for medical and pharmacy, projects them 15 months at the renewal trend and certifies about $X; the step that lands it there is projecting a cohort chosen for its high 2026 claims at its own 2026 level, when the members the same model flagged on 2024 claims, never enrolled, cost about $Y per member month the following year; the baseline is $Z.

## The ladder (planned; measured values in the build record)

| Rung | Construction | Killed by |
|---|---|---|
| R0 | each tier's 2026 PMPM by benefit projected 15 months at the renewal trend (persistence) | the bid cohort's realised year |
| R1 | the plan-wide PMPM at trend (ignores that the cohort is high-cost) | the bid cohort's realised year is several times the plan average |
| R2 | the bid cohort's calendar 2025 instead of the programme-year window (the lag not matched) | the bid's proposed programme year and the three-month lag |
| R3 | the bid cohort's realised year without the trend, or trended to the programme start (18 months) | Schedule C's midpoint rule |
| R4 | the bid cohort's claims over twelve months per member, not over member months (leavers and deaths) | Schedule C's member month |
| R5 | the bid cohort found without the conversion crosswalk (old identifiers matched to nothing, or the draft list) | the crosswalk; the final list |
| R6 | paid instead of allowed, replacements and voids and reversals not netted | Schedule C and the dictionary |
| Answer | each tier's bid-cohort allowed PMPM, April 2025 to March 2026, medical and pharmacy, over member months, times 1.065 squared and 1.09 squared; the programme baseline weights the tiers by enrolled members | |

## Determinism: the 22 axes

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 140 members on Northcourt's final 2027 enrolment list | Schedule C; the final list (the January draft is superseded) |
| 2 | Unit | allowed claims per member month, medical and pharmacy | Schedule C |
| 3 | Window | 1 April 2027 to 31 March 2028; the analog's year 1 April 2025 to 31 March 2026 | Schedule C; the bid list's cover sheet |
| 4 | As-of | 2026 claims incurred in 2026 and paid by 28 February 2027 (the 2026 PMPM ask) | Schedule C |
| 5 | Version | the final list, not the January draft | file names and the lists' cover sheets |
| 6 | Denominator | member months: enrolled in the plan on the first day of the month | Schedule C; rung R4 |
| 7 | Weighting | a tier's PMPM is its claims over its member months; the programme baseline weights tiers by enrolled members | Schedule C |
| 8 | Window length | twelve months | Schedule C |
| 9 | Boundary | a medical claim is incurred on its first date of service, a pharmacy claim on its fill date | dictionary; Schedule C |
| 10 | Rounding | whole dollars, no intermediate rounding | prompt; Schedule C |
| 11 | Tie-break | none | n/a |
| 12 | Maturity | the analog year is fully run out by February 2027; 2026 is taken as paid by 28 February 2027 without completion | Schedule C |
| 13 | Order of operations | net claims, link members, then aggregate | dictionary |
| 14 | Row order | irrelevant | |
| 15 | Duplicates | a replacement supersedes the claim it names, a void cancels it; a pharmacy reversal cancels its paid claim | dictionary; rung R6 |
| 16 | Identity | conversion crosswalk for the bid list; employee number and person code for pharmacy | crosswalk; dictionary; rung R5 |
| 17 | Netting | voids and reversals net to zero | dictionary |
| 18 | Units | USD | |
| 19 | Status semantics | denied lines carry no allowed amount | dictionary |
| 20 | Integerisation | n/a | |
| 21 | Scope | allowed before cost sharing, pharmacy before rebates, stop-loss reimbursements not deducted | Schedule C |
| 22 | Forward window contents | no programme effect, the same plan design; trend from midpoint to midpoint | Schedule C; renewal letter |

## Deliverables and criteria

Shape 14. `cohort_baseline_2027.xlsx`: one row per tier (enrolled members, 2026 allowed PMPM medical and pharmacy, baseline PMPM medical and pharmacy) and the programme baseline (medical, pharmacy, total). `baseline_certification_memo.docx`: one page for the board, opening with the total programme baseline, with a chart of each tier's 2026 PMPM against its baseline. Criteria: 4 tiers x 5 figures (20), the programme baseline (3), the memo's opening figure and chart (2 to 3), the call: about 26.

## Pack plan

| File | Format | Role |
|---|---|---|
| `medical_claim_lines_2025-01_2027-02.csv` | CSV, large | spine: medical claim lines incurred from 1 January 2025, paid to 28 February 2027 |
| `pharmacy_claims_2025-01_2027-02.csv` | CSV, large | PBM claims with reversals, keyed on employee number and person code |
| `eligibility_spans_2027-02.csv` | CSV | coverage spans by member, with employee number and person code |
| `tpa_conversion_crosswalk_2025-01-01.csv` | CSV | previous administrator's member identifiers to the current ones |
| `northcourt_stratification_2026_claims_final.xlsx` | XLSX | the 140 enrolled members: acuity score, tier, on the current identifiers |
| `northcourt_stratification_2026_claims_draft.xlsx` | XLSX | distractor: the January draft on claims paid through December, superseded |
| `northcourt_rfp_2025-07_stratification_2024_claims.xlsx` | XLSX | the bid's 140 members, score and tier, on the previous administrator's identifiers; cover sheet with the proposed programme year |
| `care_management_services_agreement_schedule_c.pdf` | PDF | the baseline's definition and the savings share |
| `renewal_letter_2027-28.pdf` | PDF | the consulting actuary's renewal: trend 6.5 per cent medical, 9.0 per cent pharmacy, unchanged |
| `pbm_rebate_report_2026.xlsx` | XLSX | distractor: rebates (the baseline is before rebates) |
| `stop_loss_policy_2027.pdf` | PDF | distractor: specific and aggregate stop-loss |
| `claims_extract_dictionary.txt` | TXT | field definitions, claim frequency and transaction codes, the conversion |

## Prompt

Stakes-first, first person, two files, units in the sentences; nothing about selection, regression, persistence or the bid; the stakes stated both ways (too high pays for savings that never happened, too low invites a dispute).

## Build record

(filled at build)

## Leak review

(filled after `leak.py` and the reader)

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
- Hardening loop 1 as built (the move-on lists on Part 3 need worked out from the household members on each round day, against a case record that lags it; 52 units against the record's 66): rejected at the clone pre-flight, reject tier (Template, Track B) against task73 world ten, whose stump is the same move (carry the class the household's record holds, when a filed rule re-derives it from the circumstances on file); task86's v2 first cut carried the same move (the bedroom standard applied with ages on the offer date) and both platform responses solved it on 2026-09-12. Its realism read (birth histories, working-day dates, the 56-day relief period, TA sizing and voids, procedure dating) was not repaired, since the device is spent. With rate-against-queue (v2) and record-against-re-derived-class (loop 1) both gone, the Tenter House queue world has no honest decisive device left that a filed rule does not turn into a computation; v2 is spent and task130 is re-rooted as architecture v3 in the same objective.
