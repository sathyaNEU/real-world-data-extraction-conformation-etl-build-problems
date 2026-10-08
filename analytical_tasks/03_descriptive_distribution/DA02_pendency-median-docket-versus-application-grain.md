# DA02 — The median pendency a patent office reports for its FY2022 filings, when its docket counts examinations and the applicant waits on an application

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · intellectual-property administration and examination workload |
| Mirrors | Resolution-time commitments measured on the work item when the customer waits on the case (support tickets reopened under new numbers at Apple and Amazon, app-review resubmissions as new reviews, cloud support cases split across engineering queues) |
| Decision shape | One figure committed at a date: the headline pendency in the annual performance report filed with the ministry on 31 January 2027 |
| Committed call | The median time from filing to the office's final decision for FY2022 filings, in months to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · Pattern D (two grains, both flawless), with E16 (finer controls in the partner's archive) below it and a corpus blind to the grain (L1) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #2 counts file rows instead of the real unit · #12 stops at the first control that passes · #7 uses the ready-made measure · #13 validates on one population, applies to another |
| Calibration form | Counterparty acknowledgement file: the partner office's acknowledgements of final decisions on 12,400 work-sharing applications filed FY2019 to FY2022 |
| Driving force | The office's examination docket closes a docket when the applicant asks for continued examination (end code CX) and opens a new one under a new number, linked only through the continuity table. The 27% of applications continued at least once are the slow ones. At docket grain each appears as two or three short spells, and their later dockets join the cohort of the year they were docketed. The partner's acknowledgements, the cleanest timing data in the pack, cannot see this: programme applications cannot be continued. |

## 1. Situation

A national patent office files an annual performance report with the ministry on 31 January. Its headline is the median pendency of a
fiscal year's filings, and FY2022 (October 2021 to September 2022) is the cohort due this year, with 13% of its applications still
undecided at the 30 September 2026 extract. The pack holds the examination docket (one row per docket, 2.9 million rows since FY2016),
the action history (every office action with its type and date), the continuity table, the partner office's acknowledgement file from
the work-sharing programme, and the annual report's published counts. The production system that examiners are measured on has reported
docket pendency for twenty years.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the docket and its dates, the action history, the continuity table, the partner's acknowledgements
  and the published counts. The production system's docket pendency is a true statement about dockets, and no one's reading of their
  own numbers is overturned. The difficulty is which unit the applicant waits on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Remove the deputy commissioner's view, the union's licensed basis and the production system's figures. The docket
  still has one tidy row per docket with a filing date, an end date and an end code, and survival analysis on it is still the competent
  first build.
* **Instrument repair.** Make the docket, the action history and the partner's file perfect; each one already is. Examination is
  organised in dockets. An applicant's wait is a chain of dockets that no row records, so no better docket instrument shows it.
* **Lens swap.** The two reads cover different populations: 476,000 dockets opened in FY2022, 96,000 of them continued-examination
  dockets (91% for applications filed earlier), against 380,000 applications filed in FY2022.

## 3. The driving force

A strong solver takes the FY2022 dockets, runs Kaplan–Meier with undecided dockets censored at the extract, and checks its decision dates
against the partner office's acknowledgements, which it reproduces to the day. If careful, it notices that a docket ending in CX is not a
decision and censors those dockets at the CX date. Each step is competent. But a CX docket is half of an application's wait, not a lost
observation. The applicant goes on waiting on a new docket under a new number, and the remaining wait is long, because applications that
need continued examination are the hard ones. The only link is the continuity table's CX edge from the old docket to the new one. Chained
along CX edges only (continuing and divisional filings are separate applications), the cohort becomes 380,000 applications with a median
of 31.4 months. The partner's file cannot warn anyone, because the programme forbids continued examination.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | FY2022 dockets, Kaplan–Meier, each closed docket ending on the docket's end date (grant date for allowed dockets) | 22.4 months (−28.7%) | Survival analysis done properly on a clean docket, censoring included | The partner's archive: its acknowledged decision dates are allowance and abandonment notices, never grants |
| 1 | Same dockets, ending at the decision (allowance or abandonment notice in the action history) | 19.0 months (−39.5%) | Reproduces every one of the partner's 11,982 acknowledged decisions to the day | The docket's end codes: 96,000 FY2022 dockets close on CX, which is no decision |
| 2 | CX-closed dockets censored at the CX date, others ending at the decision | 23.8 months (−24.2%) | The textbook treatment of an exit that is not the event | The continuity table: every CX docket continues as a new docket of the same application, so the censoring is informative |
| 3 | **Decisive:** dockets chained into applications along CX edges only, each application dated by its first docket, ending at the decision | **31.4 months** | — | — |

* **Figure shape.** The answer is the maximum cell. Every correction short of chaining files a shorter wait, so the ministry is told the
  office is faster than its applicants find it.
* **Partial correction priced (L3).** A solver who chains every continuity edge, continuing and divisional filings included, treats a
  family as an application and lands at 38.9 months (+23.9%). One who chains CX edges but keeps the cohort by docket year, so that
  chains with any FY2022 docket enter, lands at 36.2 months (+15.3%). Neither half-step comes nearer the answer than 15%.
* **Grid.** End event (grant or decision) × CX treatment (an end, censored, chained) gives 6 cells. The nearest non-answer cells are
  grant-ended chains at +11.5% and grant-ended censoring at −12.7%; reaching the answer takes the decision date and the chain.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter says the office reports "the median time from an application's filing to the office's final decision
   on it". The docket calls each row a docket, and the continuity codebook glosses CX only as "continued examination requested". No
   sentence says a docket is less than an application.
2. **Corpus blind for a computable reason.** *In every acknowledged case the application had exactly one docket, because programme rules
   bar continued examination (an applicant wanting more examination files a continuing application instead).* So docket and application
   coincide on all 12,400 cases. The partner's file reproduces rungs 1, 2 and 3 identically and certifies the decision date.
3. **No arithmetic symptom.** Docket counts tie to the annual report, every docket has one end, no docket number repeats, and the action
   history reconciles to every docket.
4. **Not a row predicate.** An application is a chain of dockets built by following CX edges (and only CX edges) through the continuity
   table, then dated by its first link. No column on a docket says which application it belongs to.
5. **The enumeration is arithmetic.** Which dockets share an application is computed by walking the chains; 96,000 FY2022 dockets
   resolve into applications filed in five different years.
6. **No cutover date.** Continued examination has run at a steady 27% of applications in every cohort, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. With every voice and every production figure removed, the docket still
   offers itself as the unit.

## 6. The calibration corpus

* **Form.** The partner office's acknowledgement file: 12,400 work-sharing applications filed FY2019 to FY2022, each with its filing date
  and the date the partner acknowledged the office's final decision (11,982 decided, 418 open), plus the partner's quarterly medians of
  days to decision.
* **What it certifies (E16).** The decision end. The salient control, the annual report's counts of FY2022 dockets allowed and abandoned,
  is passed by every end convention because it counts dockets, not dates. The two finer controls are the partner's per-application
  decision dates and its quarterly medians. The decision-dated construction reproduces 11,982 of 11,982 and all 16 quarterly medians. The
  grant-dated construction misses all 8,640 allowed cases by 97 to 212 days.
* **What it is blind to.** Chaining (above). Every construction that ends at the decision agrees with the answer on every corpus case.
* **Twin pair.** Dockets D22-118204 and D22-118377 are identical on group, docketing date (3 March 2022), end code, allowance date
  (14.5 months later), claim count and examiner. One is the first docket of an application filed that day. The other continues an
  application filed 14.8 months earlier. Their applicants waited 14.5 and 29.3 months (2.02×), and only the CX edge separates them.
* **Resemblance points at the decoy.** The FY2022 docket profile (allowance rate, claim counts, group mix) most resembles the programme's
  applications, the population every docket-grain construction reproduces exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: "The office reports the median time from an application's filing to the office's final decision on it,
  for each fiscal year's filings, in months to one decimal." The action-history codebook lists notice types (allowance, abandonment,
  restriction, rejection). The production system's docket report is labelled "examiner docket pendency", a different question correctly
  answered.
* **Empirical pins.** The decision date as the end, from the partner's archive.
* **Voices.** The deputy commissioner for operations: "Our dockets are our applications; we've measured them the same way for twenty
  years." The work-sharing coordinator: "The partner's acknowledgements are the cleanest timing data we have. A method that matches them
  is a method I'd sign."
* **Licensed wrong basis.** The charter records that the examiners' association reports pendency per docket from the production system
  and will publish its figure beside the office's.

## 8. Determinism by construction

* **Cohort.** After chaining, an application belongs to the fiscal year of its first docket. Continuing and divisional filings are
  applications with their own first dockets, so the FY2022 cohort is exactly 380,000.
* **Censoring.** Undecided applications are censored at 30 September 2026. The median is the first time the Kaplan–Meier survival falls
  to 0.5 or below, and no decision falls within three days of that crossing, so day-count and month-length conventions (30.4375 days or
  calendar months) file the same tenth.
* **Decision date.** Allowance and abandonment notices each carry one service date. No application has two final notices, because a
  withdrawn allowance re-opens the same docket.
* **Group transfers.** These happen inside a docket and never create a new docket number, so transfers cannot create spurious chains.

## 9. Prompt sketch and deliverables

> The annual performance report goes to the ministry on 31 January, and its headline is the median pendency of our FY2022 filings. The
> deputy commissioner thinks twenty years of docket statistics already tell us the answer. Give me that median in months to one decimal,
> as the sentence that goes in the report, with `pendency_build.xlsx` holding the build and the sheets below, and `pendency_curves.png`.

* `pendency_build.xlsx` — the cohort build, the four constructions' medians with their match counts against the partner file (ask C),
  the maintenance sheet (ask A) and the examiner roster sheet (ask B).
* `pendency_curves.png` — Kaplan–Meier curves of time to final decision for FY2022 under the docket and application grains, with the 50%
  line, both medians labelled, the twin dockets' waits marked, and the share still undecided at the extract annotated.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight technology centres, the share of patents granted in FY2014, FY2018 and
  FY2022 whose maintenance fee due at 11.5, 7.5 and 3.5 years respectively was paid. *Device:* a fee paid in the six-month grace period
  posts with a surcharge code on its payment date, after the due date, as the fee schedule documents. Counting only payments by the due
  date understates maintenance by 4 to 9 points in every centre.
* **Ask B (device-carried).** Examiner headcount on 30 September 2026 and FY2026 separations for each centre. *Device:* examiners on
  detail to the training academy carry the academy's organisation code while keeping their home centre in the assignment history, as the
  HR codebook documents. Counting by organisation code misplaces 212 examiners and counts 31 internal returns as separations.
* **Ask C (validity).** The FY2022 median under each of the four rung constructions, with each construction's match count against the
  partner's 11,982 decided cases.
* **Decoupling.** The fee ledger and the HR roster share no row with the docket. Clearing the chaining changes no figure in asks A or B.

## 11. Rubric arithmetic

8 centres × 3 stages (ask A) + 8 centres × 2 figures (ask B) + 4 constructions × 2 (ask C) + the committed median, the share undecided at the
extract and the twin waits + 5 named chart parts + 2 files ≈ 58 criteria.

## 12. World-building constraints

* 380,000 FY2022 applications. 27% are continued at least once by the extract and 8% twice or more. 13.2% are undecided at the extract
  (4.1% of FY2022 dockets).
* 476,000 dockets are opened in FY2022: 380,000 first dockets and 96,000 CX dockets, 91% of them continuing applications filed before
  FY2022.
* Medians by rung are 22.4 / 19.0 / 23.8 / 31.4 months, the grid's other cells are 35.0 and 27.4, and the partial cells are 38.9 and 36.2.
  No non-answer cell lies within 11% of 31.4.
* Allowance-to-grant lags run 97 to 212 days. The partner file has no CX dockets, matches the decision construction 11,982 of 11,982 and
  holds 16 quarterly medians.
* The twin dockets are identical on every docket and action-history column except their CX edge.
* The maintenance ledger and the HR roster touch no docket.
