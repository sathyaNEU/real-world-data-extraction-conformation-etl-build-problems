# DA22 — How many patient-experience coaching grants a health foundation budgets, when the hospitals with the widest Medicaid gaps have their Medicaid results withheld

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Nonprofit & Grant-making · health-equity grant programmes |
| Mirrors | Acting on subgroup gaps in survey results published with small-cell suppression (customer-satisfaction gaps by plan in enterprise CSAT reporting, employee-survey results withheld below a respondent floor at large companies, satisfaction by user group in platform and app-store surveys), where a withheld cell is bounded by its published total and siblings |
| Decision shape | One figure committed at a date: the number of coaching grants in the foundation's FY2027 budget, approved on 12 March 2027 |
| Committed call | The number of grants, one per qualifying organisation |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · E25, Medicaid rates withheld together with a complementary cell and bounded by the published total and the other payers' cells tightly enough to classify every organisation, with E02 (the organisation, which the report does not store) below it, pinned by Pattern B on the hospitals' acknowledgements |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #2 counts file rows instead of the real unit · #1 reports a failed back-test, ships anyway · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the 64 hospitals' review-period acknowledgements of the department's 2025 report, each confirming its own payer cells unsuppressed |
| Driving force | The department withholds a hospital's Medicaid rate when fewer than 30 Medicaid patients responded, and withholds a second cell so that the rate cannot be recovered exactly. It is still not unknown. The all-patient rate and the published Medicare and commercial cells fix the combined rate of the two withheld cells, and the second cell, self-pay and other, has one to four respondents. That bounds the Medicaid rate within 4 to 12 points, and every bound sits clear of the programme's six-point line. The small hospitals whose cells are withheld are where Medicaid patients fare worst. Dropping them, or filling them with the state average, loses three to five organisations' grants. |

## 1. Situation

A health foundation funds patient-experience coaches for hospitals where Medicaid patients fare worse than other patients. Its FY2027
programme gives one grant to each organisation (a health system or an independent hospital) whose Medicaid patients' "would recommend"
top-box rate in the state health department's 2026 report is at least six points below the rate for all its patients. The report covers
64 hospitals with a respondent count and an unadjusted rate for all patients and for each payer (Medicare, Medicaid, commercial, self-pay
and other). The pack holds the 2025 and 2026 reports, the department's suppression note, the state's hospital ownership registry, the
hospitals' acknowledgements of the 2025 report, and the programme rules. The board approves the budget on 12 March 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the published rates and counts, the ownership registry and the acknowledgements. Suppression is the
  department's lawful practice, and the published cells are right. Nobody's reading of their own numbers is overturned. The difficulty is
  what a withheld cell still says.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the programme officer's view, the analyst's view and the department's basis. Twenty-four Medicaid rates
  still read "withheld", and the report still lists hospitals, not organisations.
* **Instrument repair.** A larger survey would publish more cells, but the report as it stands is complete for its rules. Every withheld
  cell is already pinned within a few points by numbers the department publishes.
* **Lens swap.** The two reads cover different populations: the 40 hospitals whose Medicaid rate is printed, against all 64 hospitals
  in 41 organisations, the 24 withheld cells included.

## 3. The driving force

A strong solver builds the programme's unit first: it groups the report's hospitals into the 41 organisations of the ownership registry
and pools each organisation's rates by respondents. It meets the withheld cells and does what analysts do: it drops them, or fills them
with the state's published Medicaid rate. The hospitals' acknowledgements of the 2025 report show the fill misclassifying 9 of 23
withheld cells, all the same way, and the analyst calls it noise. It is not. Rates are unadjusted shares of respondents, so each
hospital's all-patient rate is the respondent-weighted mean of its payer cells. Subtract the published Medicare and commercial cells and
what remains is the combined rate of the two withheld cells, whose counts the report prints. The second cell, self-pay and other, has one
to four respondents, so even at 0% or 100% it moves the Medicaid rate by a few points. The withheld hospitals are small rural and
safety-net hospitals, and their Medicaid patients are the least satisfied in the state. Bounded, nine of them sit clear below the line.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Each hospital row with a printed Medicaid rate, gap of six points or more | 17 (+30.8%) | The report as published, hospital by hospital | The programme funds organisations as the ownership registry records them on 1 January 2027 |
| 1 | Organisations, rates pooled by respondents over hospitals with printed cells (E02) | 10 (−23.1%) | The programme's unit, built exactly from the registry | The rule pools every hospital's Medicaid patients, and 24 hospitals' cells are withheld |
| 2 | Organisations, withheld Medicaid rates filled with the state's published Medicaid rate | 8 (−38.5%) | The standard fill, from the report's own average | The acknowledgements: the fill misclassifies 9 of 2025's 23 withheld cells, every miss hiding a gap |
| 3 | **Decisive:** organisations, each withheld Medicaid rate bounded by its hospital's published total, other payers and cell counts (E25) | **13** | — | — |

* **Figure shape.** The first two corrections lower the count and the decisive move reverses them. A budget filed at any lower rung leaves
  three to five qualifying organisations without a coach, all of them where the gap is widest.
* **Partial correction priced (L3).** No route that ignores the published totals comes near: filling withheld cells with each hospital's
  own all-patient rate gives 7, and applying the state's average Medicaid gap gives 9. Any route through the totals reaches 13, because
  every bound clears the line: the bound's midpoint, either end, or a guess for the self-pay cell inside 0–100% classifies every
  organisation the same way.
* **Grid.** Unit (hospital or organisation) × withheld cells (dropped, filled with the state rate, bounded) gives 6 cells: 17, 21 and 26
  hospitals, and 10, 8 and 13 organisations. The nearest wrong cell is 10 (−23.1%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The suppression note says Medicaid rates under 30 respondents are withheld "with a complementary cell so they
   cannot be derived". No document says they can be bounded, or that the bound decides anything.
2. **Reproduction, and why it is a construction.** On the 2025 acknowledgements the bounds classify all 23 withheld cells correctly. The
   state-rate fill gets 14, the own-hospital fill 9, and dropping classifies none. Every fill error hides a gap, so no fill reconciles in
   aggregate. The bound is built from each hospital's published total, its printed payer cells and the withheld cells' counts. No
   parameter or menu reaches it.
3. **No arithmetic symptom.** Every printed cell is consistent, every count adds up to its total, and nothing the report prints is wrong.
4. **Not a row predicate.** A withheld cell's bound depends on four other cells of the same hospital and on the count of the second
   withheld cell.
5. **The enumeration is arithmetic.** 24 bounds are computed, and 9 fall wholly below the line, 15 wholly above.
6. **No cutover date.** Suppression has applied the same rule every year, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, a withheld cell still looks unknown.

## 6. The calibration corpus

* **Form.** The 64 hospitals' acknowledgements of the 2025 report: during the department's review window each hospital confirmed its own
  cells, unsuppressed, and the department shares the acknowledgements with the foundation under its data-use agreement.
* **What it pins.** That the withheld cells are recoverable within their bounds: every confirmed 2025 Medicaid rate lies inside the
  bound built from the 2025 report, and the bound classifies all 23. It also refuses the fills (above).
* **Twin pair.** In 2025, Hollins Ridge and Marston Valley are identical on every column a lookup would use: 96 beds, the same region,
  an all-patient rate of 88.0% from 412 respondents, 27 Medicaid and 3 self-pay respondents withheld, the same Medicaid share of
  discharges. Their confirmed Medicaid gaps were 11.8 and 5.4 points (2.2×). Only the bound separates them: Hollins Ridge's printed
  Medicare and commercial cells are high, so its withheld pair must be low.
* **Resemblance points at the decoy.** By size and region, the 2026 withheld hospitals most resemble the 2025 hospitals whose confirmed
  Medicaid rates sat near the state average.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The programme rules: "One grant goes to each organisation, as the state's ownership registry records it on 1 January
  2027, whose Medicaid patients' 'would recommend' top-box rate in the 2026 report is at least six points below its rate for all
  patients, rates pooled over its hospitals by respondents." The suppression note gives the threshold of 30 and the complementary cell.
* **Empirical pins.** The bounds' validity and the fills' failure, from the acknowledgements.
* **Voices.** The programme officer: "The state's report already shows us where the gaps are." The data analyst: "A withheld cell is a
  hole; the state average is the fairest fill."
* **Licensed wrong basis.** The programme rules record that the department's quality bureau summarises equity gaps from printed cells
  only and will see the foundation's list.

## 8. Determinism by construction

* **Totals.** Rates are unadjusted shares, so each total is the respondent-weighted mean of its payer cells and no weighting can put a
  total outside its parts.
* **Rounding.** Published rates carry one decimal, which widens each bound by at most 0.3 points, already inside every margin.
* **The second cell.** The complementary cell is always self-pay and other, with 1 to 4 respondents, and its counts are printed.
* **Organisations.** The registry as of 1 January 2027. No hospital changes parent between then and the decision.
* **Margins.** Every bound, at hospital and organisation level, clears the six-point line by at least 0.8 points.

## 9. Prompt sketch and deliverables

> We're budgeting next year's Medicaid patient-experience coaching programme, one coach per grant, and the board approves on 12 March.
> Our programme officer believes the state's report already shows us where the gaps are. Tell me how many grants to budget, in a sentence
> for the board, and send `coaching_grants.xlsx` with the sheets below and a chart `medicaid_gap_bounds.png`.

* `coaching_grants.xlsx` — the organisations with their pooled rates or bounds under each rung's construction, the acknowledgement
  back-test (ask C), the disbursements sheet (ask A) and the funds sheet (ask B).
* `medicaid_gap_bounds.png` — each organisation's Medicaid gap as a point or a bound against the six-point line, withheld hospitals drawn
  as intervals, Hollins Ridge and Marston Valley annotated, and the qualifying organisations marked.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Disbursements by programme and quarter, 2025–2026, for the foundation's five programmes.
  *Device:* a grant paid in instalments has one commitment row and a payment row per instalment, as the grants-ledger guide documents.
  Summing every row double-counts committed funds in 29 of the 40 cells.
* **Ask B (device-carried).** Each of the four board-designated funds' balance at each quarter-end of 2025–2026. *Device:* an inter-fund
  transfer posts as a negative entry in the sending fund and a positive one in the receiving fund under one transfer reference, as the
  finance manual documents. Reading positive entries as income overstates 14 of the 32 balances.
* **Ask C (validity).** The grant count under each of the four rung constructions, each construction's classification of the 23
  withheld 2025 cells against the acknowledgements, and Hollins Ridge's and Marston Valley's bounds and confirmed gaps.
* **Decoupling.** The foundation's ledgers share no row with the department's reports, the registry or the acknowledgements. Clearing the
  bounds changes no figure in asks A or B.

## 11. Rubric arithmetic

5 programmes × 8 quarters (ask A) + 4 funds × 8 quarters (ask B) + 4 rung counts, 4 back-test counts and 4 twin figures (ask C) + the
committed count and the 13 organisations named + 4 named chart parts + 2 files ≈ 104 criteria.

## 12. World-building constraints

* 64 hospitals in 41 organisations; 24 Medicaid cells withheld in 2026 (23 in 2025), each with a self-pay and other cell of 1 to 4
  respondents withheld beside it.
* Counts: hospitals 17 / 21 / 26 (dropped, state-rate fill, bounded); organisations 10 / 8 / 13; own-rate fill 7; state-gap fill 9.
* Bounds 4 to 12 points wide; 9 wholly below the line and 15 wholly above, every one at least 0.8 points clear.
* Acknowledgements: bounds 23 of 23, state-rate fill 14, own-hospital fill 9, dropping 0.
* Hollins Ridge and Marston Valley are identical on every lookup column; confirmed gaps 11.8 and 5.4 points.
* The foundation's ledgers touch no report cell.
