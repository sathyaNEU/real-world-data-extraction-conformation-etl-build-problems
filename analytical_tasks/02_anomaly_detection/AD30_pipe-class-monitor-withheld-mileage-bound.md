# AD30 — Which pipe gets its own rare-incident chart for 2027, when the failing class has its mileage withheld in every published table

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Supply Chain & Logistics · pipeline integrity oversight |
| Mirrors | Monitoring rare failures by the population that carries the hazard rather than the account it is booked to, when that population's exposure is only published in aggregate (drive-failure monitoring by model and batch across cloud fleets, component reliability by part batch across airlines, battery incidents by cell lot at consumer-device makers) |
| Decision shape | A structure the body adopts: the partition of the state's pipe into separately monitored classes, and which class's chart is signalling, scored on the commission's rule that no chart may pool pipe whose incident rates differ by more than 1.5× |
| Committed call | The monitored classes and the signalling class, filed with the commission on 1 December as the 2027 monitoring structure |
| Gap · Pattern | Gap 2 (population: the hazard lives in a pipe class, not an operator) over Gap 3 (objective: the homogeneity rule) · a withheld cell bounded from a published total and its other components, with a saturated tie broken by the record's open gaps below it |
| Gate G mechanism | decomposition_attribution, with signal_vs_noise_or_hold support |
| Measured traps engaged | #24 treats an unpublished figure as unknown · #19 breaks a big tie instead of questioning it · #4 never tests its reading against the control |
| Calibration form | Change-log natural experiments: nine pipeline segments that changed operator in 2015–2024, each with its incident record before and after the transfer |
| Driving force | Incident rates follow the pipe, not the operator, and the pipe failing now is pre-1970 low-frequency ERW seam. Only two operators hold it, so the published mileage table withholds every LF-ERW cell and its rate looks uncomputable. It is bounded: the statewide pre-1970 total, less the published mileage of every other pre-1970 seam type, leaves LF-ERW between 410 and 470 miles, so its rate is at least 2.4× the rest of pre-1970 pipe under every value in the bound. That forces it onto its own chart, and only that chart signals. |

## 1. Situation

The state pipeline commission's integrity office monitors 6,200 miles of hazardous-liquid pipe run by ten operators. Incidents are rare
(38 since 2021), so it watches time between incidents, normalised by mileage, on control charts. For 2027 it must file the monitoring
structure: which populations get their own chart, and which chart, if any, is signalling at the 30 June 2026 review, since a signalling
population gets an inspection order. The commission's rule says no chart may pool pipe whose incident rates differ by more than 1.5×. The
office holds the incident reports (with each failed segment's seam type and install decade), the federal regulator's published mileage
tables and the operator-change log. Operations believes operator X slipped after its reorganisation.

## 2. Gate G: why this is legal

* **Litmus.** Every reported figure is correct: incident dates, the published mileage cells, the withheld markers and the transfer records.
  Operations is right that X had a run of short gaps. Nothing reported is overturned; the difficulty is a rate that looks unknowable and is
  in fact bounded.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the operations view and the office's old operator charts. A class-based build that treats withheld mileage as
  unknown still pools all pre-1970 pipe and still orders inspection of 1,840 miles.
* **Instrument repair.** Publish every cell the confidentiality rule allows and correct every incident record: the LF-ERW cells are still
  withheld by rule, and the bound is still the only route to the rate.
* **Lens swap.** The naive structure watches operators (or all pre-1970 pipe); the answer watches 430 miles of one seam class held by two
  operators. Different populations of pipe, not one population under two lenses.

## 3. The driving force

A strong solver moves from annual counts to time between incidents, breaks the saturated tie properly, reads the transfer log as natural
experiments and sees that a segment keeps its incident rate when it changes hands, so the monitor should run on pipe classes. It splits by
era, finds pre-1970 pipe failing at four times the rate of newer pipe, and orders inspection of all of it. Every step is correct. The
homogeneity rule then asks whether pre-1970 pipe is one population, and the incident reports say eleven of its 24 recent failures were on
LF-ERW seam. LF-ERW's exposure is withheld in every county cell and in the statewide row, because only two operators hold it, and a solver
reading "withheld" as "unknown" cannot test the rule and keeps pre-1970 pooled. The statewide pre-1970 total is published, and so is every
other pre-1970 seam type except one small SAW cell in one county, which the county total caps. So LF-ERW lies between 410 and 470 miles,
its rate between 4.3 and 4.9 incidents per thousand mile-years against 1.65 to 1.73 for the rest, and the split is forced at both ends.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Per-operator time-between-incident charts; six operators tie at 100% of 2025–26 gaps below their lower limit, broken by the monitor's documented tie-break (largest mileage) | Per-operator structure, operator X on enhanced inspection | The office's standing monitor and its written tie-break | The incident file to the review date: X's open gap since March 2025 is above its lower limit, so X's share is 67% |
| 1 | Saturation broken by the standard's rule (the lowest share consistent with every file of record, counting each open gap to 30 June) | Per-operator structure, operator Y | The standard applied exactly; only Y stays at 100% | The transfer log: in all nine transfers the segment kept its rate within 12% while the acquirers' own rates differ up to 3× |
| 2 | Class charts by era, withheld LF-ERW mileage treated as unknown so pre-1970 cannot be tested for homogeneity | Two classes; the pre-1970 chart signals; order on all 1,840 pre-1970 miles | Rates follow the pipe, the era split is homogeneous on everything computable, and the transfers confirm it | The published county and statewide tables bound LF-ERW mileage at 410–470 miles |
| 3 | **Decisive:** bound LF-ERW's exposure from the published totals, apply the 1.5× rule, chart three classes | **Three classes (pre-1970 LF-ERW, other pre-1970, post-1970); only the LF-ERW chart signals; order on about 430 miles** | — | — |

* **Structure table.** Four different structures: two per-operator structures naming different operators, a two-class era split ordering
  1,840 miles, and the three-class answer ordering 430. No lower rung holds the answer's partition or its order scope.
* **Separation at the decisive rung.** LF-ERW's rate is 4.26 to 4.88 per thousand mile-years across the bound and the rest of pre-1970 runs
  1.65 to 1.73, a ratio of at least 2.46 against the rule's 1.5. LF-ERW's last five gaps all fall below its lower limit at both ends of the
  bound; the other pre-1970 chart has none below.
* **Partial correction priced (L3).** A solver who builds class mileage by summing seam-type cells and reads a withheld cell as zero keeps
  LF-ERW's eleven incidents in a pre-1970 class of 1,370 published miles, sees that chart signal, and orders inspection of 1,370 miles that
  leave out all 430 failing ones: a two-class structure ordering the wrong pipe, further from the answer than rung 2's 1,840-mile order,
  which at least contains it. A solver who bounds LF-ERW but keeps operator charts names Y again, the only operator at 100% against X's
  67%.
* **Grid.** Monitored unit (operator or class) × tie handling (documented tie-break or open gaps) × withheld mileage (unknown, zero or
  bounded) = 12 cells. Operator cells name X or Y; class cells name the two-class era split, ordering 1,840 miles, or with withheld read as
  zero 1,370 miles without LF-ERW; only class charts with the bound name the three-class structure.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The mileage tables mark withheld cells and state the confidentiality rule. No document combines tables, and none
   suggests LF-ERW differs from other pre-1970 pipe.
2. **Corpus blind for a computable reason.** *In every transfer the segment was HF-ERW, seamless or SAW pipe, because neither LF-ERW holder
   has ever sold a segment.* The log certifies that rates follow the pipe (rung 2) and is silent on whether LF-ERW differs from the rest.
3. **No arithmetic symptom.** Published cells sum to published totals wherever both are shown, incident counts tie to the regulator's
   annual summary, and the withheld markers are exactly where the rule puts them.
4. **Not a row predicate.** The bound comes from subtracting published components from a published total across two tables, capping the
   one other withheld cell by its county total, and carrying the interval through a rate and a control chart.
5. **The enumeration is arithmetic.** LF-ERW's exposure exists in no cell; its interval is computed.
6. **No cutover date.** X's reorganisation is dated and is decoy material; LF-ERW's failures cluster in no single month and no series steps
   on a date.
7. **Survives deletion.** Remove the operations view and the old charts, and the class build with LF-ERW unknown is still the natural one.

## 6. The calibration corpus

* **Form.** The operator-change log: nine segments that changed hands in 2015–2024, each with four years of incidents and mileage before and
  after the transfer.
* **What it certifies.** Rates follow the pipe: each segment's post-transfer rate is within 12% of its pre-transfer rate. The rival "rate
  follows the operator" predicts each segment at its acquirer's system rate and misses eight of nine by 40% or more, all in the direction of
  the acquirer, so it fails on the total as well.
* **What it is blind to.** LF-ERW (above).
* **Twin pair.** Harlan and Mercer counties publish identical pre-1970 totals (310 miles), identical incident counts (six each) and both
  withhold their LF-ERW cell. Bounding puts Harlan's LF-ERW at 150–160 miles and Mercer's at 70–80, so their LF-ERW rates differ about 2×,
  separated only by the bound.
* **Resemblance points at the decoy.** Y's run of short gaps most resembles the two transfers in which the acquirer was first blamed and
  the segment's rate later held, so a lookup reads the signal as an operator problem.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The commission's rule: no chart may pool pipe whose incident rates differ by more than 1.5×, and a signalling population
  receives an inspection order. The monitoring standard: chart construction, the review date and the share defined as the lowest value
  consistent with every file of record. The federal tables' confidentiality rule. One sentence each.
* **Empirical pins.** That rates follow the pipe, from the transfer log; LF-ERW's exposure interval, from the published tables.
* **Voices.** The head of operations: "X has not been the same since the reorganisation." The regulator's liaison: "If the tables withhold
  it, we do not have it; build on what is published."
* **Licensed wrong basis.** The standard records that the operators' association monitors each operator's system as a whole and will present
  its operator charts at the filing hearing.

## 8. Determinism by construction

* **The bound.** The split and the LF-ERW signal hold at every value from 410 to 470 miles, so no point estimate inside the bound is a fork.
* **Mileage over time.** No LF-ERW pipe was added or retired since 1970, and the published tables give the same pre-1970 totals in every
  year of the window.
* **Chart settings.** The transformation, the baseline (2015–2020) and the limits are filed in the standard; the review date is 30 June
  2026.
* **Seam type of incidents.** Every incident report carries the failed segment's seam type and decade, with no blanks among pre-1970
  failures.

## 9. Prompt sketch and deliverables

> The 2027 monitoring structure goes to the commission on 1 December: which pipe gets its own rare-incident chart, and which chart, if any,
> is signalling now and needs an inspection order. Operations is sure X has slipped since its reorganisation. Give me the classes and the
> signalling one in a paragraph I can file, with the miles any order would cover to the nearest ten, plus `monitor_structure.xlsx`, a chart
> `class_charts.png`, and a one-page `filing_note.pdf`.

* `monitor_structure.xlsx` — rates and bounds by class, the assessments sheet (ask A), the one-call sheet (ask B) and the structure table
  (ask C).
* `class_charts.png` — one panel per adopted class: transformed gaps since 2021, centre line and lower limit labelled with their values,
  LF-ERW's limits drawn at both ends of the mileage bound, and the signalling points marked.
* `filing_note.pdf` — the committed structure, the signalling class and the order's scope.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each operator, in-line inspection runs completed in 2025 and the miles assessed. *Device:* a
  run repeated after a tool failure keeps its run ID with a revision suffix, and the assessment guide counts only the accepted revision.
  Counting every revision inflates four operators. The monitor never uses assessment records.
* **Ask B (device-carried).** For each operator, 2025 excavation tickets with a marking dispute and the share resolved within the statutory
  two business days. *Device:* business days exclude the holidays in the one-call centre's calendar; calendar days misstate the share for
  four operators.
* **Ask C (validity).** For each of the four rung structures: its monitored populations, which chart signals, and its result on the nine
  transfers.
* **Decoupling.** Clearing the bound and the open-gap rule changes no figure in asks A or B.

## 11. Rubric arithmetic

10 operators × 2 (ask A) + 10 × 2 (ask B) + 4 structures × 2 (ask C) + the committed classes, the signalling class, the LF-ERW mileage
bound and the rate ratio + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* 6,200 miles; pre-1970 1,840 (LF-ERW 430, inside a published bound of 410–470); incidents since 2021: 11 LF-ERW, 13 other pre-1970, 14
  post-1970. Published pre-1970 seam cells sum to 1,370 miles; the one withheld SAW cell holds 40, capped at 60 by its county total.
* Y holds 300 LF-ERW miles and Z 130. Six operators tie at 100% on closed gaps; only Y stays there with open gaps counted.
* The nine transfers hold every post-transfer rate within 12% of the pre-transfer rate; none is LF-ERW.
* Harlan and Mercer are identical on every published column.
* Assessment records and one-call tickets never touch incident reports or the mileage tables.
