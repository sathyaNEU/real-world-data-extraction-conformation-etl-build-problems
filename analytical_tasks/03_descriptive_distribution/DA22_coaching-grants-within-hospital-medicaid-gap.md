# DA22 — How many patient-experience coaching grants a health foundation budgets, when a system's Medicaid gap can come from which of its hospitals Medicaid patients use

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Nonprofit & Grant-making · health-equity grant programmes |
| Mirrors | Acting on a subgroup gap measured across a portfolio, when the subgroup is concentrated in the weaker units and the gap inside each unit is small (satisfaction gaps by customer plan pooled across stores or support centres, employee-survey gaps by grade pooled across offices at large companies, conversion gaps by device pooled across country storefronts) |
| Decision shape | One figure committed at a date: the number of coaching grants in the foundation's FY2027 budget, approved on 12 March 2027 |
| Committed call | The number of grants, one per qualifying organisation |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E22, the deciding comparison (Medicaid patients against other patients inside each hospital, then pooled) against the components pooled first, with E25 (withheld Medicaid cells bounded by each hospital's published total) and E02 (the organisation, which the report does not store) below it, pinned by Pattern B on the 2025 acknowledgements |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #20 leaves the deciding comparison unstated · #24 treats an unpublished figure as unknown · #2 counts file rows instead of the real unit · #12 stops at the first control that passes |
| Calibration form | Counterparty acknowledgement file: the 31 applicant organisations' acknowledgements of the foundation's 2025 decision letters, each confirming the gap its letter states and the hospital cells behind it, unsuppressed |
| Driving force | The programme measures each organisation's Medicaid gap as its 2025 decision letters did, and only one construction reproduces all 31 of them: Medicaid patients against the other patients of the same hospital, then pooled. Pool a system's rates first, as every equity summary does, and a system whose Medicaid patients go mostly to its busy safety-net campus shows a wide gap even where, inside every one of its hospitals, they rate their care like everyone else. Six of the thirteen organisations with a pooled gap of six points are such systems. Compared inside each hospital, seven organisations qualify, and small hospitals' withheld cells must be bounded first to show their own gaps. |

## 1. Situation

A health foundation funds patient-experience coaches for organisations where Medicaid patients fare worse than other patients. Its
FY2027 programme gives one grant to each organisation (a health system or an independent hospital) whose Medicaid patients fare at
least six points worse than its other patients on the "would recommend" top-box rate in the state health department's 2026 report,
measured as the 2025 programme measured it. The report covers 64 hospitals with a respondent count and an unadjusted rate for all
patients and for each payer, and withholds a Medicaid rate under 30 respondents together with a complementary cell. The pack holds the
2025 and 2026 reports, the suppression note, the state's ownership registry, the 31 applicants' acknowledgements of their 2025 decision
letters and the programme rules. The board approves the budget on 12 March 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the published rates and counts, the registry and the acknowledgements. A system's pooled Medicaid
  rate is a true statement about its Medicaid patients, and nobody's reading of their own numbers is overturned. The difficulty is which
  comparison the programme makes.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the programme officer's view, the analyst's view and the quality bureau's basis. Pooling a system's rates by
  respondents is still the standard way to give it one rate, and the pooled gaps still clear the line for 13 organisations.
* **Instrument repair.** Clean-data test. The suspect file is the 2026 report, whose 24 small hospitals' Medicaid cells are withheld.
  Publish them: rung 1 and rung 2 both become 13 organisations by direct read, rung 0 becomes 26 hospitals, and the answer stays 7,
  because the comparison inside each hospital is still needed. No other file is suspect: the registry and the acknowledgements are
  complete, and the published cells are correct for what they count.
* **Lens swap.** The two reads compare different populations: a system's Medicaid patients against all its patients, across hospitals
  of different quality, against Medicaid patients and other patients of the same hospital.

## 3. The driving force

A strong solver builds the programme's unit first: it groups the report's 64 hospitals into the registry's 41 organisations and pools
each one's rates by respondents. It meets the withheld cells and bounds them from each hospital's published total, printed payer cells
and cell counts, which the 2025 acknowledgements confirm in every case. Thirteen organisations then clear the line. But the 2025 letters
measured something else, and the rules say to measure as they did: Medicaid patients against other patients of the same hospital. In
six of the thirteen, a large urban system
sends most of its Medicaid patients to one busy safety-net campus that everyone rates lower, while its suburban hospitals carry most of
its other patients. Pooled, Medicaid patients look far worse off. Inside each hospital they rate their care within two points of the
hospital's other patients. One system shows the opposite: its Medicaid patients use its children's hospital, which everyone rates
highly, and inside each hospital they rate it eight points lower. Compared hospital by hospital and then pooled, seven organisations
qualify.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each hospital row with a printed Medicaid rate, six points or more below its all-patient rate | 17 (+142.9%) | The report as published, hospital by hospital | The programme funds organisations as the ownership registry records them on 1 January 2027 |
| 1 | Organisations (E02), Medicaid and all-patient rates pooled by respondents over hospitals with printed cells | 10 (+42.9%) | The programme's unit, built exactly from the registry | The rules pool every hospital's Medicaid patients, and 24 hospitals' cells are withheld |
| 2 | Withheld Medicaid cells bounded by each hospital's published total, other payers and cell counts (E25), then pooled | 13 (+85.7%) | Every cell printed or bounded clear of the line; every 2025 withheld cell confirmed inside its bound | The acknowledgements: pooled rates reproduce 22 of the 31 gaps the 2025 letters state, every miss a system whose Medicaid patients use its weaker hospitals |
| 3 | **Decisive:** in each hospital, Medicaid against other patients (the hospital's total less its Medicaid cell), the gaps then pooled over the organisation's hospitals by Medicaid respondents (E22) | **7** | — | — |

* **Figure shape.** The answer is bracketed. Every construction that pools rates first counts 8 to 13 organisations, and every comparison
  inside hospitals that drops or fills the withheld cells counts 4 to 6. A budget filed at rung 2 pays six coaches to systems whose
  Medicaid patients are treated like everyone else in every hospital they use.
* **Partial correction priced (L3).** Comparing inside hospitals but against all patients, Medicaid included, gives 6 (−14.3%). Comparing
  inside hospitals with the withheld cells dropped gives 5 (−28.6%), and with the state's Medicaid rate filled in, 4 (−42.9%). Counting
  hospitals whose own inside gap clears the line gives 12 hospitals (+71.4%).
* **Grid.** Unit (hospital or organisation) × withheld cells (dropped, filled with the state rate, bounded) × comparison (pooled rates, or
  inside each hospital) gives 12 cells, from 4 to 28. Only organisations, bounded cells and the inside comparison give 7. The nearest
  wrong cells are 6 (−14.3%) and 8 (+14.3%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rules say Medicaid patients must fare six points worse than the organisation's other patients, measured as
   in 2025. The 2025 letters state each gap and its hospital cells, not how the gap was formed. The department's equity summaries pool
   rates by system. No document says the comparison is made inside hospitals.
2. **Reproduction, and why it is a construction.** Comparing inside each hospital and pooling by Medicaid respondents reproduces all 31
   gaps the 2025 letters state. Pooling rates first reproduces 22, and its nine misses are all systems, every one too wide, so it cannot
   reconcile on the cohort either. The reproducing quantity is a weighted average of within-hospital differences, each built from a total
   less its Medicaid cell. No parameter or menu reaches it.
3. **No arithmetic symptom.** Every printed cell is consistent, every count adds up, and the pooled rates reproduce the department's
   published system summaries exactly.
4. **Not a row predicate.** The decisive quantity is a respondent-weighted average of within-hospital differences, each built from a
   hospital's total less its Medicaid cell, over a group that the registry defines.
5. **The enumeration is arithmetic.** 64 inside gaps, 24 of them from bounded cells, pooled into 41 organisations.
6. **No cutover date.** The systems' patient flows are the same every year, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, pooling is still how a system gets one rate.

## 6. The calibration corpus

* **Form.** The 31 applicant organisations' acknowledgements of their 2025 decision letters: each letter stated the organisation's gap
  and the hospital cells behind it, and each hospital confirmed its cells, unsuppressed, in acknowledging.
* **What it certifies.** The bounds (E25): every confirmed Medicaid cell of 2025 falls inside the bound built from the 2025 report, and
  the bounds classify all 23 withheld cells, where the state-rate fill classifies 14 and dropping none. And the comparison: 31 of 31
  gaps reproduce only inside hospitals (above).
* **Twin pair.** Riverbend Health and Calloway Health applied in 2025 and are identical on every organisation-level column: three
  hospitals each, 1,900 respondents, a pooled Medicaid rate of 74.6% and a pooled all-patient rate of 82.8%. Riverbend sends 70% of its
  Medicaid patients to its safety-net campus; Calloway spreads them evenly. Their letters state gaps of 3.6 and 7.4 points (2.1×), and
  only Calloway was funded. Every pooled construction treats them alike.
* **Resemblance points at the decoy.** By size, region and pooled gap, the six composition-driven systems most resemble the 2025 cohort's
  largest grantees, whose pooled and inside gaps happened to agree.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme rules: "One grant goes to each organisation, as the state's ownership registry records it on 1 January
  2027, whose Medicaid patients fare at least six points worse than its other patients on the 'would recommend' top-box rate of the 2026
  report. Gaps are measured as the 2025 programme measured them." The suppression note gives the threshold of 30 and the complementary
  cell.
* **Empirical pins.** The inside comparison and its weights, and the bounds' validity, from the acknowledgements.
* **Voices.** The programme officer: "The state's equity summary already shows us which systems leave Medicaid patients behind." The data
  analyst: "One rate per system, pooled by respondents, is how everyone compares them."
* **Licensed wrong basis.** The rules record that the department's quality bureau summarises equity gaps from system-pooled rates and
  will see the foundation's list.

## 8. Determinism by construction

* **Other patients.** A hospital's other-patient rate is its total less its Medicaid cell, by respondents. Rates are unadjusted shares,
  so every total is the respondent-weighted mean of its cells.
* **Bounds.** Every withheld cell's bound, and every organisation's pooled inside gap built from bounds, clears the six-point line by at
  least 0.8 points, and published rates' rounding to one decimal is already inside every bound.
* **Weights.** The 2025 gaps reproduce with Medicaid-respondent weights, and all-respondent weights would qualify the same seven.
* **Organisations.** The registry as of 1 January 2027; no hospital changes parent before the decision.

## 9. Prompt sketch and deliverables

> We're budgeting next year's Medicaid patient-experience coaching programme, one coach per grant, and the board approves on 12 March.
> Our programme officer believes the state's equity summary already shows us which systems leave Medicaid patients behind. Tell me how
> many grants to budget, in a sentence for the board, and send `coaching_grants.xlsx` with the sheets below and a chart
> `inside_versus_pooled.png`.

* `coaching_grants.xlsx` — each organisation's pooled gap and its inside gap under each rung's construction, the bounds and the
  acknowledgement back-test (ask C), the disbursements sheet (ask A) and the funds sheet (ask B).
* `inside_versus_pooled.png` — each organisation's pooled gap against its inside gap, the six-point lines on both axes, bounded hospitals
  drawn as intervals, Riverbend and Calloway annotated, and the qualifying organisations marked.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Disbursements by programme and quarter, 2025–2026, for the foundation's five programmes.
  *Device:* a grant paid in instalments has one commitment row and a payment row per instalment, as the grants-ledger guide documents.
  Summing every row double-counts committed funds in 29 of the 40 cells.
* **Ask B (device-carried).** Each of the four board-designated funds' balance at each quarter-end of 2025–2026. *Device:* an inter-fund
  transfer posts as a negative entry in the sending fund and a positive one in the receiving fund under one transfer reference, as the
  finance manual documents. Reading positive entries as income overstates 14 of the 32 balances.
* **Ask C (validity).** The grant count under each of the four rung constructions, each construction's reproduction count on the 31
  acknowledged gaps, and Riverbend's and Calloway's pooled and inside gaps.
* **Decoupling.** The foundation's ledgers share no row with the department's reports, the registry or the acknowledgements. Clearing the
  inside comparison changes no figure in asks A or B.

## 11. Rubric arithmetic

5 programmes × 8 quarters (ask A) + 4 funds × 8 quarters (ask B) + 4 rung counts, 2 back-test counts and 4 twin figures (ask C) + the
committed count and the 7 organisations named + 4 named chart parts + 2 files ≈ 96 criteria.

## 12. World-building constraints

* 64 hospitals in 41 organisations (30 independents, 11 systems); 24 Medicaid cells withheld in 2026 (23 in 2025), each with a self-pay
  cell of 1 to 4 respondents withheld beside it.
* Counts: hospitals 17 / 21 / 26 against all patients and 19 / 23 / 28 against other patients (dropped, state-rate fill, bounded);
  organisations pooled 10 / 8 / 13; inside comparison 5 / 4 / 7; inside against all patients 6.
* Of the 13 organisations with a pooled gap, 6 are systems whose inside gaps are under two points; one system qualifies only inside.
* Acknowledgements: the inside comparison reproduces 31 of 31 stated gaps, pooled rates 22; bounds classify all 23 withheld 2025 cells,
  the state-rate fill 14, dropping none.
* Riverbend and Calloway are identical on every organisation-level column; pooled inside gaps 3.6 and 7.4 points.
* The foundation's ledgers touch no report cell.
