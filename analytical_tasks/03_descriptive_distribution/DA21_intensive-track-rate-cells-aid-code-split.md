# DA21 — Which parts of a health plan's book get the intensive care-management track, when Medicaid is one line in the files and two rate cells in the contract

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · health-plan administration and care management |
| Mirrors | Choosing which customer segments get a high-touch programme from a concentration measure, when one labelled segment pools two contracts priced separately (enterprise and education plans reported under one label at Apple and Google, cloud customers on two committed-use schedules under one tier, marketplace sellers on two fee plans in one category) |
| Decision shape | A structure the board adopts: which of the book's rate cells get the 2027 intensive track, scored on whether each cell's costliest 5% of members account for at least half of its allowed spending |
| Committed call | The list of rate cells that get the intensive track |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E29, a uniformly labelled line (Medicaid) that the state contract prices as two rate cells, split month by month through the state's aid-code roster, with E15 (paid amounts, the quiet trap behind the loud spenders-only decoy) below it and a published control set blind to rate cells (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #6 treats a mixed segment all one way · #11 beats the headline trap, misses the quiet one · #12 stops at the first control that passes · #14 coarsens the segment it was asked about |
| Calibration form | Published control set with a reproduction clause: the state insurance department's concentration reports on the plan for 2023–2025 (each line's top-5% share and 95th-percentile spending, 42 cells), which the board's rule makes the test of any construction |
| Driving force | The board funds the track rate cell by rate cell, and every file the plan keeps labels Medicaid as one line. The state contract prices it as two cells by aid code, month by month: Family Health and Disability Health. Pooled, Medicaid's costliest 5% hold 54% of its spending and the line qualifies. Split, Family Health's hold 63%: newborns in intensive care, trauma, a few cancers among mostly healthy families. Disability Health's hold 41%, because almost everyone in it is costly. The aid code lives only in the state's monthly roster, and a member granted disability status changes cell from the month it takes effect. The state's report, the control the board requires, is published by line and cannot see the split. |

## 1. Situation

A nonprofit health plan with seven lines of business (large group, small group, self-funded employers, individual, Medicaid, Medicare
Advantage and a dual-eligible plan) will run an intensive care-management track in 2027. Nurse case managers are paid for out of each
rate cell's care-management allowance, so the board's rule decides the track cell by cell. A cell gets it where its costliest 5% of
members account for at least half of the cell's 2026 allowed spending, the condition under which targeting the top pays. The pack holds
the enrolment file (member, line, months), the 2026 claims (allowed and paid amounts, dates of service), the state's monthly Medicaid
eligibility roster, the Medicaid contract, the state's concentration reports for 2023–2025 and the board's rule. The board adopts the
structure on 20 January 2027.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: enrolment, claims, the roster and the state's reports. Pooled Medicaid's concentration is right
  about the line, the state's figures are right about the plan's lines, and nobody's reading of their own numbers is overturned. The
  difficulty is what one cell of the board's rule is.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CFO's view, the analytics lead's view and the actuaries' basis. Every plan file still labels Medicaid as
  one line, and the state's report still checks only lines.
* **Instrument repair.** Perfect the plan's files and Medicaid is still one line of business with one product code, because the plan
  sells one Medicaid product. The rate cell is the state's classification, carried in the state's roster.
* **Lens swap.** The two reads cover different populations: 82,000 Medicaid members pooled, against 63,000 member-years in Family Health
  and 19,000 in Disability Health, each scored on its own costliest 5%.

## 3. The driving force

A strong solver sees that concentration among members with spending understates it, because a member with no claims is still a member,
and includes everyone. It then notices that the claims extract's amount column is the plan's payment, after deductibles and
coinsurance, while the rule counts allowed spending. Switching to allowed amounts makes the small-group and large-group books, full of
high-deductible plans, far less concentrated. That construction reproduces all 42 cells of the state's reports, and it names Individual
and Medicaid. But the rule scores rate cells, and the Medicaid contract prices two of them: Family Health for families and Disability
Health for members with a disability determination. The plan's files carry neither. The state's roster carries the aid code month by
month, and a member granted disability status moves cell from the effective month. Split on that roster, Family Health is the most
concentrated cell in the book and Disability Health one of the least.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Members with any 2026 claim, paid amounts, the plan's seven lines | Small group, Individual | The usual reading of who drives the spending | The rule counts members, and a member with no claims is one; with zeros the state's reports reproduce, without them none do |
| 1 | All members, paid amounts | Large group, Small group, Individual, Medicaid | The population right, the extract's amount column | The rule counts allowed spending, and the paid column nets out deductibles and coinsurance (E15); paid amounts reproduce 6 of the state's 42 cells |
| 2 | All members, allowed amounts | Individual, Medicaid | Reproduces all 42 cells of the state's reports | The Medicaid contract's rate schedule: two cells by aid code, which only the state's roster carries |
| 3 | **Decisive:** all members, allowed amounts, Medicaid split into Family Health and Disability Health by the aid code in force in each month of service (E29) | **Individual, Family Health** | — | — |

* **Structure shape.** Each rung adopts a different list, and only rung 3 names Family Health. Top-5% shares by rung (lines, then the
  split): Large group 46 / 54 / 46, Small group 54 / 60 / 45, Individual 55 / 60 / 55, Medicaid 46 / 55 / 54, then Family Health 63 and
  Disability Health 41 at rung 3. Self-funded, Medicare Advantage and the dual plan never reach 50.
* **Partial correction priced (L3).** Every half-applied split adopts a wrong list. Splitting by each member's aid code at year end
  moves the members granted disability status mid-year, Family Health's costliest, wholly into Disability Health, drops Family Health to
  46% and adopts Individual alone. Splitting by age, children against adults, adopts Individual and "Medicaid children" (58%), a cell the
  contract does not have. Splitting on paid amounts adopts Large group, Small group, Individual and Family Health.
* **Grid.** Members (spenders or all) × amount (paid or allowed) × Medicaid (pooled or split) gives 8 cells and 8 different lists, from
  none at all (spenders, allowed, pooled) to four cells. Only all members, allowed amounts and the monthly split adopt Individual and
  Family Health.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The rule says "rate cell". The plan's product file has one Medicaid product, and every plan table reports seven
   lines. The cells are defined only in the contract's rate schedule, an appendix on capitation rather than care management, by aid
   codes that no plan file carries.
2. **Corpus blind to the split.** The state's reports certify the population and the amount exactly. *In every published cell Medicaid is
   one line, because the department reports carriers by line of business.* Run over the reports, the pooled and split constructions
   return the same 42 figures.
3. **No arithmetic symptom.** Enrolment reconciles to member-months, claims to the plan's ledger, and every construction partitions the
   same spending. The roster ties to the Medicaid membership month by month.
4. **Not a row predicate.** A claim's cell is the aid code in force in its month of service, read from another organisation's roster, and
   a member can sit in both cells in one year.
5. **The enumeration is arithmetic.** 2,140 members changed cell during 2026, and $611 million of Medicaid spending is divided month by
   month.
6. **No cutover date.** Disability determinations take effect in every month, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without any voice, the plan's files still have one Medicaid line.

## 6. The calibration corpus

* **Form.** The department's concentration reports on the plan for 2023, 2024 and 2025: for each of the seven lines, the share of
  allowed spending held by the costliest 5% of members and the 95th-percentile spending (42 cells). The board's rule requires any
  construction to reproduce them.
* **What it certifies.** Zeros included and allowed amounts reproduce 42 of 42. Paid amounts reproduce 6, and spenders only none. The
  misses run one way (too concentrated), so no rival reconciles on the reports' totals either. It also fixes how a member who changes
  line mid-year counts: in each line, with that line's months.
* **What it is blind to.** Rate cells within a line (above).
* **Twin pair.** The Northern and Southern Medicaid service areas are identical on every column the plan's files and the state's
  reports carry: 41,000 members each, the same allowed spending and a pooled top-5% share of 54%. Family Health's costliest 5% hold 66%
  of its spending in the North and 33% in the South (2.0×), where most of the high-cost members are in Disability Health. Only the
  roster split separates them.
* **Resemblance points at the decoy.** Pooled Medicaid's spending distribution most resembles Individual's, the line that qualifies
  under every construction with zeros and allowed amounts.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's rule: "The intensive track goes to each rate cell in which the costliest 5% of members account for at
  least half of the cell's 2026 allowed spending, and any construction must reproduce the department's concentration reports." The
  Medicaid contract's rate schedule defines Family Health and Disability Health by aid code for each month of eligibility.
* **Empirical pins.** Zeros, allowed amounts and the treatment of mid-year movers, from the department's reports.
* **Voices.** The CFO: "The commercial book is where the money concentrates." The analytics lead: "We matched the department's report to
  the decimal. The method is settled."
* **Licensed wrong basis.** The rule records that the plan's actuaries present concentration by line of business at the board.

## 8. Determinism by construction

* **Months.** Each claim takes the aid code in force in its month of service. The roster carries exactly one aid code per member-month,
  retroactive changes already applied.
* **Members.** A member counts in each cell they belonged to in 2026, with that cell's months and spending, as the reports do for lines.
* **Percentile.** The costliest 5% is the top 5% of members by allowed spending, ranked in descending order. Every cell's share sits at
  least three points from 50% under every construction and partial, so no tie or rounding rule moves a cell.
* **Amounts.** Allowed amounts after adjustments, as the claims extract's final version carries them.

## 9. Prompt sketch and deliverables

> Which parts of our book should get the intensive care-management track next year? The board adopts the structure on 20 January, and
> our CFO is sure the commercial book is where the money concentrates. Give me the list, as the board would minute it, and send
> `intensive_track.xlsx` with the sheets below and a chart `concentration_by_cell.png`.

* `intensive_track.xlsx` — each line and cell's top-5% share under each rung's construction, the reproduction of the department's 42
  cells (ask C), the call-centre sheet (ask A) and the authorisation sheet (ask B).
* `concentration_by_cell.png` — concentration curves for every cell with the 5% and 50% lines, pooled Medicaid drawn against Family
  Health and Disability Health, the Northern and Southern areas' Family Health curves annotated, and the adopted cells marked.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** The call-centre abandonment rate by line of business and month, July to December 2026.
  *Device:* a call transferred between queues is logged as two legs under one call ID, as the telephony guide documents. Computing
  abandonment per leg understates it in 31 of the 42 cells.
* **Ask B (device-carried).** Median prior-authorisation turnaround by service category (imaging, surgery, drugs, therapy) and quarter of
  2026. *Device:* a request pended for more information stops its clock until the information arrives, as the utilisation-management
  policy documents. Measuring from receipt to decision without the pauses overstates 13 of the 16 cells.
* **Ask C (validity).** Each line's and cell's top-5% share under each of the four rung constructions, each construction's reproduction
  count on the department's reports, and the Northern and Southern areas' Family Health shares.
* **Decoupling.** Telephony and authorisation records share no row with enrolment, claims or the roster. Clearing the Medicaid split
  changes no figure in asks A or B.

## 11. Rubric arithmetic

7 lines × 6 months (ask A) + 4 categories × 4 quarters (ask B) + 9 lines and cells × 4 constructions, 4 reproduction counts and 2 twin
shares (ask C) + 8 cell decisions + 4 named chart parts + 2 files ≈ 114 criteria.

## 12. World-building constraints

* Top-5% shares (spenders paid / all paid / spenders allowed / all allowed): Large group 46 / 54 / 42 / 46; Small group 54 / 60 / 41 / 45;
  Self-funded 44 / 47 / 40 / 44; Individual 55 / 60 / 46 / 55; Medicaid pooled 46 / 55 / 41 / 54; Family Health 58 / 66 / 54 / 63;
  Disability Health 36 / 40 / 35 / 41; Medicare Advantage 37 / 42 / 35 / 39; dual plan 32 / 36 / 31 / 34.
* Partials: Family Health 46% on year-end aid codes; Medicaid children 58%, adults 44%.
* Medicaid: 82,000 members, $611 million allowed, 2,140 members changing cell in 2026.
* The department's reports: 42 cells, reproduced 42/42 by all members on allowed amounts, 6 by paid amounts, 0 by spenders only.
* The Northern and Southern areas are identical on every plan and report column.
* Telephony and authorisation data touch no claim or enrolment row.
