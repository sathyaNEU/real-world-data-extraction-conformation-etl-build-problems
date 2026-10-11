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
  Context artifact: operations_log (the plan's claims and eligibility feeds, the administrator's claim lines and the
    PBM's claims, the record the baseline is built on; the vendor's lists carry tiers and scores, never a cost;
    redrawn at the build from filed_model, banned against task133, and from register, banned against task131)
  Forum: trustees_or_governors (the school board)   Forcing event: purchase_order_or_contract
  Organisation: university_or_school   Opening move: stakes-first
  Personas (guard.py names --geo "United States" --seed 130): Joyce Salinas (requester, director of risk
    management and benefits), Deborah Johnson (board chair), Anthony Olsen (chief financial officer),
    Michael Perry (consulting actuary, Lindqvist Benefits Consulting), Allison Santiago (Northcourt account
    lead), Tiffany Barrett (benefits analyst); added at the build from the same draw: Phillip Alvarado (Northcourt
    chief operating officer), Amy Kelley (Northcourt clinical analytics), Michelle Peterson (Quarrystone client
    account executive), Jonathan Hoffman (Wyecliff stop-loss underwriting), Sandra Lopez (superintendent); added at
    repair 1 from the same draw: Samantha Galvan (Northcourt clinical manager), Edward Miller (Northcourt member
    outreach supervisor)
As-of date: 2027-03-12 (claims paid through 28 February 2027); the programme year is 1 April 2027 to 31 March 2028
```

**World.** Red Cedar Valley School District (fictional, Minnesota) self-insures the health plan for about 6,000 covered members (employees, early retirees under 65, spouses and children). A third-party administrator has run the medical plan since 1 January 2025, when it replaced the previous administrator and issued new member identifiers (a conversion crosswalk maps the old ones); pharmacy runs through a PBM keyed on the district's employee number and a person code. In January 2025 the district tendered for high-cost care management with a programme year from 1 April 2025; the bidders stratified the plan's 2024 claims, and Northcourt Care Partners' bid flagged 140 members in four risk tiers on its acuity score. The award was suspended in April 2025 under the district's budget freeze and no services were provided. The services agreement was signed in February 2027 for a programme year from 1 April 2027; Northcourt stratified the plan's 2026 claims with the same model and the 140 members on its final list are enrolled from 1 April. Northcourt is paid 40 per cent of the savings, the difference between the baseline and the enrolled members' actual allowed claims per member month in the programme year, tier by tier and benefit by benefit. Joyce Salinas certifies the baseline and the board approves it on 25 March 2027.

**Why this is hard.** The 140 members were chosen because their 2026 claims put them at the top of the plan. A cost that high is partly lasting (dialysis, specialty drugs, a chronic condition) and partly a one-off (an operation, a heart attack, a cancer course that ends, a premature birth, a hepatitis C cure), and the one-off part does not come back. Projecting each tier's 2026 claims forward at the renewal trend, which is how the plan projects every other group and which is right for any group not chosen on its claims, certifies a baseline several times what the cohort will cost, and Northcourt is paid for savings the members were always going to show. The plan's own record holds the answer: the 140 members Northcourt flagged with the same model on 2024 claims were never enrolled, and their allowed claims in the year from April 2025, the programme year they were flagged for, are what a flagged member costs the following year without the programme, tier by tier and benefit by benefit.

**Two layers (client standard).** Layer 1: medical claim lines with replacements, voids and denied lines; pharmacy claims from the PBM with reversals in its own layout and keyed on employee number and person code; eligibility as coverage spans; the administrator change on 1 January 2025 with a conversion crosswalk (the bid list carries the old identifiers); claims history that starts with the new administrator; run-out on the latest year; a superseded draft stratification beside the final one. Layer 2 (`estimand_identification`, `own:selection-on-the-outcome-baseline`): a cohort chosen on an extreme value of a noisy outcome is forecast by carrying its own value forward, when the outcome regresses toward the mean; the counterfactual is the next-period experience of a cohort chosen the same way and left untreated, which the plan's record contains. Six-point check: the inputs take real work (lines, replacements, reversals, two key systems, the conversion, member months) and none of it is planted; the flipping step is a method choice (persistence against the untreated cohort's realised year); Schedule C defines the estimand (expected claims in the programme year without the programme) and the bid cohort makes the analog the design-implied estimator; no decoy memo and no filed method that gives the wrong answer; the method is not recovered from certified figures; the lesson (a cohort chosen on its outcome regresses) is not one an earlier build teaches.

## Data-native sentence

Northcourt picked the 140 members the plan paid most for in 2026, and a year of the highest claims in a self-insured plan is mostly the year someone had the operation, the heart attack, the cancer course or the premature baby, so the members who top the list are the ones whose next year looks least like their last; the district already watched it happen to the 140 members Northcourt flagged in its 2025 bid, who were never enrolled.

## Gate G

- **Litmus.** No. Every file is correct: the claims, the eligibility, the crosswalk, both stratification lists, the agreement, the renewal letter. No stakeholder states a number the task overturns.
- **Primary mechanism:** `forecasting` (a forecast the correctly read past does not pin: the 2026 claims are right and are not the forecast).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test.** With perfectly clean claims, the persistence projection is still the natural one and still wrong; the bid cohort's realised year is what refutes it.
- **Deletion test.** Delete every distractor (rebates, stop-loss, the draft list, Northcourt's implementation plan): the persistence projection is still natural and still wrong.
- **No shipped artifact ranks or forecasts the cohort's cost.** The stratification files carry an acuity score and a tier, never a cost or a predicted cost; the renewal letter projects the whole plan, not the cohort.

## Why the analog's level is the one method (forcing)

- The estimand is Schedule C's: the allowed claims per member month that the enrolled members in each tier would be expected to incur in the programme year without the programme, medical and pharmacy separately, in programme-year dollars at the renewal trend from the midpoint of any experience period to the midpoint of the programme year.
- The bid cohort was chosen by the same model, on the same tiers, on a calendar year of claims, for a programme year starting three months after that year, exactly as the enrolled cohort was; it was never treated. Its realised allowed claims per member month in April 2025 to March 2026, by tier and benefit, projected 24 months at the trend, is the expected cost of a member the model puts in that tier. Midpoint to midpoint is 24 months whichever convention is used.
- The ratio form (the enrolled cohort's 2026 cost times the bid cohort's next-year-over-selection-year ratio) cannot be built: the claims history starts on 1 January 2025 with the new administrator and neither stratification file carries a cost. A cost-only regression on the whole plan does not reproduce the selection, which runs on the acuity score (claims, conditions, specialty drugs and admissions, not cost alone), and its window would not match the three-month lag.
- Members of the bid cohort who left the plan before April 2025 carry no member months and drop out on their own; those who left during the year count for the months they were enrolled.

## Stump sentence

A competent solver nets the claim lines and the pharmacy reversals, links the members, takes each tier's 2026 allowed claims per member month for medical and pharmacy, projects them 15 months at the renewal trend and certifies about $8,895; the step that lands it there is projecting a cohort chosen for its high 2026 claims at its own 2026 level, when the members the same model flagged on 2024 claims, never enrolled, cost about $3,385 per member month the following year (at the enrolled tier mix, before trend); the baseline is $3,916.

## The ladder (measured on the shipped pack)

Programme totals per member per month against the golden $3,916.30. Every rung also moves the tier figures; the four rungs within 5 per cent on the total still miss every whole-dollar tier cell and both programme components (checks.py asserts it for every rung table).

| Rung | Construction | Programme total | Killed by |
|---|---|---|---|
| R0 | each tier's 2026 PMPM by benefit projected 15 months at the renewal trend (persistence) | $8,895.03, +127.1% ($7,204.57 medical, $1,690.46 pharmacy); R0c with 2026 medical completed at the letter's factors $9,127.75, +133.1% | the bid cohort's realised year |
| R1 | the renewal letter's plan-wide projection | $742.48, -81.0% | the bid cohort's realised year is several times the plan average |
| R2 | the bid cohort's calendar 2025, trended 27 months | $4,229.67, +8.0% | the bid's proposed programme year and the three-month lag |
| R3 | R3a the bid cohort's year untrended; R3b trended 18 months to the programme start | $3,385.31, -13.6%; $3,776.03, -3.6% | Schedule C.1(g)'s midpoint rule |
| R4 | R4a twelve months for each listed member; R4b twelve months for each member enrolled on 1 April 2025 | $3,521.94, -10.1%; $3,659.73, -6.6% (members left during the year in every tier, so neither lands on a tier cell) | Schedule C.1(b)'s member month |
| R5 | R5a the Bramwell numbers matched to nothing, so the bid cohort is lost and persistence is left; R5b the January draft's tier counts as weights | $8,895.03; $3,799.90, -3.0% | the crosswalk; the final list |
| R6 | R6a paid instead of allowed; R6b replacements, voids and reversals not netted; R6c both | $3,652.85, -6.7%; $4,234.65, +8.1%; $3,953.48, +0.9% | Schedule C.1(a) and the warehouse readme |
| Pooled | the bid cohort's year without tiers | $3,677.35, -6.1% on the total, every tier baseline wrong | Schedule C.1(g), a baseline per tier |
| Answer | each tier's bid-cohort allowed PMPM, April 2025 to March 2026, medical and pharmacy, over member months, times 1.065 squared and 1.09 squared; the programme baseline weights the tiers by enrolled members | $3,916.30 ($2,227.15 medical, $1,689.15 pharmacy) | |

## Three rules (client update, 10/10)

- **Domain (swap test).** The deciding quantity is the expected allowed claims per member month of a selected cohort in a programme year without the programme, by tier and by medical and pharmacy, projected at the plan's trend over member months, a claims-cost projection a health actuary certifies; with another field's nouns the claim lines, member months, medical and pharmacy trend, run-out and the vendor's acuity tiers have nothing to attach to.
- **Two layers.** Layer 1 is the claims plumbing a self-insured plan really produces (claim versions and denials, PBM reversals in their own layout, two key systems, an administrator conversion, run-out, a superseded draft list) and carries no stump; Layer 2 is selection on the outcome, a cohort chosen on its extreme 2026 claims regressing toward the mean, with the untreated 2025 bid cohort as the design-implied estimator.
- **The decisive step is analytical** (`stump_class: analytical`). Analyst test: a strong analyst who nets the claims, links the members and reads Schedule C and the renewal letter correctly still projects each tier's 2026 allowed PMPM fifteen months at the renewal trend and certifies about $8,895 programme total against $3,916, because the cohort was chosen on its extreme 2026 claims, which regress toward the mean.

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
| 9 | Boundary | a medical claim is incurred on its first date of service, a pharmacy claim on its fill date; a claim counts in its period whether or not its month is a member month (a newborn's month of birth) | Schedule C.1(a) |
| 10 | Rounding | whole dollars, no intermediate rounding | prompt; Schedule C |
| 11 | Tie-break | none | n/a |
| 12 | Maturity | the analog year is fully run out by February 2027; 2026 is taken as paid by 28 February 2027 without completion | Schedule C |
| 13 | Order of operations | net claims, link members, then aggregate | warehouse readme |
| 14 | Row order | irrelevant | |
| 15 | Duplicates | a replacement supersedes the claim it names, a void cancels it; an exact duplicate submission is denied (reason 18); a pharmacy reversal cancels its paid claim | warehouse readme; rung R6 |
| 16 | Identity | conversion crosswalk for the bid list; employee number and the person code in effect on the fill date for pharmacy | crosswalk; warehouse readme; rung R5 |
| 17 | Netting | voids and reversals net to zero | warehouse readme |
| 18 | Units | USD | |
| 19 | Status semantics | denied lines carry no allowed amount | warehouse readme |
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
| `northcourt_implementation_plan_2027-28.pdf` | PDF | distractor: Northcourt's implementation and outreach plan (account team, timeline, outreach), no amounts |
| `warehouse_readme_2027-03.txt` | TXT | the benefits warehouse readme: field definitions, claim frequency, denial and transaction codes, the conversion |

## Prompt

Stakes-first, first person, two files, units in the sentences; nothing about selection, regression, persistence or the bid; the stakes stated both ways (too high pays for savings that never happened, too low invites a dispute).

## Build record

- **Generator** (`generator/`, `python3 build.py` writes target/, target.zip, golden/ and metadata.json). `world.py` constants, calendars (clinic and bank holidays, Ellery's Thursday check runs) and plan designs; `catalog.py` the code sets, fee schedule, drug list and prices; `providers.py` the billing NPIs and pharmacies, sticky by family; `coding.py` each service coded and priced (fee schedule, share of charges, case rates spread over revenue lines, payment lags); `sim.py` the plan member by member, January 2023 to March 2028 (2023 is burn-in, so the 2024 and 2026 selection years carry the same depth of history); `acuity.py` the vendor's model and the bid, draft and final lists; `extracts.py` claim versions, denials, PBM transactions, eligibility spans, the crosswalk; `docs.py` the agreement, renewal letter, stop-loss schedule, implementation plan, stratification and rebate workbooks, warehouse readme; `containers.py` LibreOffice PDF conversion with the export clock pinned and Office containers in Excel's and Word's part order; `estimators.py` the golden and every rung from the shipped files; `tune.py` and `tune_table.py` bin centring; `golden.py` the workbook, chart and memo; `checks.py` 5,972 assertions; `verify.py` an independent recompute (csv module and Decimal, no shared code) of every graded figure against golden/ and submission.md.
- **Seeds.** World seed 101050 (population at the seed, health +11, coding +37, claim history +131, PBM +151); provider directory 52311, pharmacies 52323 and birth-date corrections 52367, fixed apart from the world seed so a seed sweep and the build share one directory; the acuity model's member noise keyed by crc32 of member, year and salt 41730; acuity dollars on a 2023 base of 2,500; tier floors 53.5, 45.5 and 40.0, ranked on the unrounded score.
- **Magnitudes.** 5,887 members covered on 1 January 2025; 70,888 member months in 2025; plan-wide 2025 allowed PMPM $467.62 medical and $153.74 pharmacy; medical claim lines 303,148 rows, PBM transactions 105,653, eligibility spans 8,063, crosswalk 5,880; 13 files, 59.8 MB, csv, pdf, txt and xlsx (target.zip 11.6 MB). Final tiers 20, 34, 48, 38 (1,634 member months in 2026); bid tiers 18, 31, 47, 44, all 140 linked, 136 enrolled on 1 April 2025, 1,542 member months in the analog year; draft tiers 19, 33, 45, 43 (eight members swapped against the final, five re-tiered); 13 members on both the bid and the final list.
- **Golden** (whole dollars PMPM: members; 2026 medical, pharmacy; baseline medical, pharmacy). Tier 1: 20; 13,317, 294; 5,529, 934. Tier 2: 34; 8,914, 1,051; 2,660, 2,622. Tier 3: 48; 4,815, 2,056; 1,630, 2,241. Tier 4: 38; 3,468, 1,899; 857, 555. Programme baseline $2,227 medical, $1,689 pharmacy, $3,916 total (unrounded 2,227.15, 1,689.15, 3,916.30).
- **Simulated truth** (the enrolled members' untreated 2027-28 year, read from the simulation, never shipped): $4,076.82 at the tier weights ($2,287.05 medical, $1,789.76 pharmacy), $4,064.68 pooled; golden over truth 0.961, persistence over truth 2.18. Per tier the analog is noisy, as 18 to 47 members with heavy-tailed claims will be (tier 1 pharmacy $934 against a simulated $316; one or two specialty-drug members carry 63 to 89 per cent of each bid tier's pharmacy); the method is pinned by Schedule C's estimand and the design, not by the tier-level fit.
- **Regression to the mean in the record.** The bid cohort's April 2025 to March 2026 claims ran at 0.28 of its 2024 level for medical and 0.99 for pharmacy, in real terms (2024: $6,008 medical, $1,246 pharmacy PMPM); specialty drug regimens persist, one-off medical episodes do not. 130 of the 140 enrolled members had a hospital stay or a cancer course in 2026 (an operation 26, pneumonia 13, a heart attack 7, a cancer course 21, a premature birth 5).
- **Regression alternative.** A cost-only least-squares fit of 2026 allowed on 2025 allowed over members enrolled all 24 months, applied to the enrolled members' annualised 2026 claims and trended three months: $4,841.98, +23.6% from the golden and +18.8% from the truth. It is not the estimator: the selection runs on the acuity score (conditions, specialty drugs, admissions, not cost alone), the fit's population is the whole plan rather than a cohort chosen the same way, and its year does not match the three-month lag.
- **Clean-data and deletion tests.** The golden equals the simulation's claim-free service amounts for the bid members' year in every tier; persistence on complete claim-free 2026 data is $8,960.63. Deleting the four distractors leaves every golden figure unchanged.
- **Bins.** 11 centring adjustments to clean facility and pharmacy claims (largest $310.38, none above 4 per cent of its claim), validated against all three lists; the nearest graded figure sits 0.20 from a rounding boundary, the rounded medical and pharmacy parts add to the rounded total, and the programme medical and pharmacy sit at least a dollar from the persistence rung's.
- **Reproducibility.** Two scratch rebuilds are byte-identical to each other and to the shipped target/, golden/ and target.zip (13 entries at the top level, contents identical to target/; sha256 9b5648de8246f3ded10132046a292686a39ed07d2a63b6ca68b2c1d0a0bb6e98).

## Repair 1 (2026-10-11, after the v3 reader round and the clone pre-flight)

- **L1.** The folder now holds Northcourt's implementation and outreach plan of 8 March 2027 (account team, timeline, outreach, reporting; no amount, cost, baseline, score or word on how the members were chosen; a distractor in metadata.json), so "everything Northcourt has sent us" is true. The RFP 2025-07 cover lost its "for use in the evaluation of RFP 2025-07 only" line and keeps the model, the tier floors, the proposed programme year and the 1 January 2025 enrolment basis.
- **P1.** Schedule C.1(a) defines Allowed Claims as claims incurred while the member is covered, counted in their period whether or not the month is a Member Month; C.1(b) keeps the first-day rule. Six newborns on the final list were covered from a mid-month birth date in 2026, with $829,027 of medical claims in their months of birth inside their tiers' 2026 figures.
- **P2.** An exact duplicate submission is denied with reason 18 and carries no allowed amount (2,196 claims), and the readme says so; no service is paid on two live original claims.
- **P3.** Asserted: four bid members left before 1 April 2025 and none returned, so counting all 140 by member months equals counting the 136 enrolled on 1 April 2025, in every tier.
- **P4.** PBM transactions are processed 1 January 2025 to 28 February 2027 (no reversal after the window); medical claims paid 9 January 2025 to 25 February 2027.
- **R1.** Codes fit the patient: PSA for men from 40, preventive codes and examinations by age, otitis media for children, adult chronic diagnoses never under 12, sex-specific diagnoses and procedures, NICU only for newborns with neonatal diagnoses, and no overlapping stays (856 stays).
- **R2.** 231 billing NPIs, 326 procedure codes, 389 principal diagnoses, 267 NDCs and 40 pharmacies on skewed frequencies (the top ten diagnoses carry 33 per cent of claims); each professional group bills its own specialty's signature services.
- **R3.** A clinic calendar (no office visits on Sundays or clinic holidays, Saturdays under 8 per cent), every payment on an Ellery Thursday check run or the next business day after a bank holiday, pharmacy fills dipping at the weekend, emergency visits every day.
- **R4.** Professional lines at the fee schedule or a lower billed charge (0.8 per cent of lines allowed at billed), outpatient lines at a share of charges, stays at case rates spread over revenue lines that carry their own charges; receipt to payment median 7 days, 6.0 per cent at 30 days or more, longest 128 (pended claims). Three fills join only on the person code in effect after a birth-date correction renumbered a family, and seven birth dates differ between the crosswalk and eligibility; none is on a graded member.
- **R5.** PDFs are LibreOffice Writer conversions that keep LibreOffice's own Producer, tagged with fonts embedded and the export clock pinned to the fiction; workbooks are packed as Excel writes them (shared strings, Excel's part order) with their own save histories.
- **R6.** Every eligibility span's coverage tier fits the dependents enrolled in it.
- **R7.** Deborah Johnson (Chair, School Board) and Sandra Lopez (Superintendent) sign for the District and Phillip Alvarado for Northcourt, under a recital recording the Board's approval of 9 February 2027.
- **Clone surface.** `claims_extract_dictionary.txt` is now `warehouse_readme_2027-03.txt`, the district's own name for it, everywhere it is cited.
- **Moved figures** (old to new, whole dollars). Members by tier 18, 38, 41, 43 to 20, 34, 48, 38. 2026 PMPM medical and pharmacy: tier 1 15,338 and 2,780 to 13,317 and 294; tier 2 8,182 and 1,242 to 8,914 and 1,051; tier 3 4,828 and 1,603 to 4,815 and 2,056; tier 4 3,413 and 1,262 to 3,468 and 1,899. Baseline medical and pharmacy: tier 1 4,177 and 899 to 5,529 and 934; tier 2 2,729 and 2,072 to 2,660 and 2,622; tier 3 1,172 and 1,484 to 1,630 and 2,241; tier 4 1,745 and 884 to 857 and 555. Programme 2,157, 1,384 and 3,541 to 2,227, 1,689 and 3,916. The claims engine was rebuilt for R1 to R4 and the seed redrawn, so every graded figure moved; the method, the estimator and the ladder's constructions are unchanged.

## Leak review

`leak.py task130 --asof 2027-03-12` after repair 1: REVIEW, no LEAK (report in `leak_check_report.md`); the producer-metadata audit reports no writer signature on target/ and golden/ (the PDFs keep LibreOffice's own Producer, which LibreOffice writes in UTF-16 where the audit's substring sweep does not read it; R5 wants it kept).

- Reader round and clone pre-flight on v3 (2026-10-11): the reader's findings (L1, a folder holding no Northcourt paper beside the lists and a bid cover marked for the RFP evaluation only; P1 to P4; R1 to R7) and the pre-flight's surface note (the dictionary named on the `<system>_extract_dictionary.txt` pattern of earlier builds) are answered in Repair 1 above; none of them touched the estimator.
- REVIEW, Schedule C carries 19 of 24 distinctive words of the call: they are the estimand's own defined terms (Programme Baseline, per Member Month, Enrolled Members, medical and pharmacy) that the prompt also uses; it carries no figure of the answer, and its recitals record the 2025 tender and its suspension as history without saying the bid cohort sets the baseline.
- REVIEW, design-note words in the implementation plan (record, register, benefits, client) and the warehouse readme (record, benefits, analyst): ordinary furniture (the records a care team sees, a registered nurse, Northcourt's Client Implementation team, the Risk Management and Benefits office, a Bramwell member record, the benefits analyst who keeps the readme); neither says anything about the bid list's use, how the members were chosen or how their cost moves, and the plan carries no amount, cost, tier figure or trend (asserted in checks.py).
- REVIEW, 140 dates after the as-of in the final list: the Enrolment effective column is 1 April 2027 for every member, the programme start the list exists to schedule, not an outcome.

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

v3 build (2026-10-11):

- The first acuity score (claims dollars with pharmacy at full weight): rejected after measurement, specialty-drug members dominated every list and persistence came out only 1.1 to 1.5 times the golden, because a specialty regimen persists; the score now weights pharmacy at 0.2 of medical and the world carries the one-off medical episodes a top-of-plan list really holds (major surgery, stroke, post-acute stays, readmissions, longer cancer courses).
- Model noise keyed by a member's position on the list: rejected, the draft and the final list scored the same member differently; noise is keyed by member and year.
- Tiers from a rank on the rounded score: rejected, it tied at place 140; ranks use the unrounded score and the lists show one decimal, as the cover sheets say.
- Scores on nominal dollars: rejected, the 2024 and 2026 scores drifted apart with prices and the bid and final tiers stopped meaning the same acuity; dollars are restated to a 2023 base.
- Model noise salted with the world seed: rejected, the seed sweep and the build drew different lists; the salt is fixed (41730).
- Seeds 100000 and 102002: passed every gate but their tier baselines fell out of order (a lower tier costing more than a higher one in total), which a board reads as a broken model; seed 101005 kept.
- A tier total column in the workbook: rejected, Schedule C.2 forbids intermediate rounding and tier 4's unrounded total rounds to 2,630 against 2,629 from its rounded parts; the medical and pharmacy figures stand alone and Note 1 says why.
- R3b, R5b and R6c land within 5 per cent of the golden total: accepted rather than forced apart, they are the arithmetic of 18 against 24 months of trend, weights only, and two offsetting errors; each still misses the whole-dollar tier cells it touches.
- R4b equal to the golden in tier 3: accepted as structural, no tier-3 bid member left the plan during the year; checks.py reports it.
- The renewal letter restating Schedule C's member-month and incurred-date rules: cut, each convention is stated once, in Schedule C.
- Procedure lines carrying diagnoses drawn at random: replaced by procedure-appropriate diagnosis maps for outpatient surgery and hospital services.
- context_artifact register, asked for at the card update to clear filed_model's collision with task133: BLOCK ban.artifact against task131; redrawn to operations_log, the plan's claims and eligibility feeds the baseline is built on.

Repair 1 (2026-10-11):

- Seed 101005 under the rebuilt claims engine: bid tier 1 fell to 8 members and the tier baselines fell out of order at every acuity base from 2,200 to 2,500; a sweep of seeds 101000 to 101053 at four bases kept 101050 at 2,500, which passes every gate at all four.
- A simulation that started in January 2024: the 2024 selection year had a shallower history than 2026, so the bid's tier 1 shrank against the final's; the simulation starts in January 2023 as burn-in.
- A plan-wide medical PMPM near $425 under the first fee schedule: low for a school district plan; facility charges, consults and the commercial multiple (1.14 of the reference schedule) bring it to $468.
- Home health priced as a case rate: allowed ran above billed; it is priced per visit at a share of charges.
- A wrong-member claim drawn from any family member: it put PSA tests on women and deliveries on men; the wrong member is drawn from the same sex and age band.
- Birth-date corrections drawn freely: five-year changes no conversion produces; one digit of the year, on two-child families.
- Pharmacy pickups on the day a fill fell due: a Monday spike; pickups spread over five days on a weekday profile.
- A hepatitis C first visit dated the first of the month: a Sunday office visit; moved to the next business day, no graded figure moved.
- The duplicate assertion counting a wrong-member claim that was later voided as a second payment: the assertion reads only live claims.
- The first rebuild's programme pharmacy ($1,689.88) rounded with the persistence rung's ($1,690.46): centring now holds the programme figures a dollar clear of persistence's, and checks.py asserts no rung lands on either programme figure.
- Centring that let one pharmacy fill move 7 per cent: a fill now moves at most 2.5 per cent and a facility claim 4 per cent.
- The memo's "a transplant, a premature baby, a cancer course or an accident" and the chart title "pharmacy moves much less": false on this seed (no enrolled member had a transplant in 2026; tier pharmacy baselines run 0.29 to 3.18 times 2026); rewritten to the enrolled members' own 2026 and to "pharmacy moves both ways", both asserted.
- Implementation plan tables that opened with the role and the milestone: the guard's name reader joined cells into "Ellery Final", "Ellery Welcome", "Kelley Enrolment" and "Santiago Direct" (a BLOCK on two Ellerys); the tables open with the name and the date.
- Jessica Petty from the draw as outreach supervisor: a first-name WARN against task104; Edward Miller from the same draw.
- LibreOffice's /DocChecksum left as exported: it hashes the run clock and broke byte identity between rebuilds; it is recomputed over the pinned file.
