# task482 design note

Status lives in `pipeline.json`; this note holds the design. Architecture 3, drawn 2026-10-21 after architectures 1
and 2 were spent at stage 4; nothing of their worlds or decisive steps is kept.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task482.json` (architecture v3, lineage v1 and v2 spent), registered
  2026-10-21 after a pull. Guard WARN only, answered here: `overuse.objective` (the lane), `repeat.decision` and
  `repeat.question_form` (a designation set asked as "which"), `people.first`. Redrawn at the draw: role family and
  organisation family (bans against task480), differentiation lines for task231, task234, task445 and task469. People
  from `guard.py names --geo ie --seed 4823`: Eunan Reid and Jennifer Dyer.
- **Pairing:** Survey Research & Official Statistics, task type `census-register-administrative-data-quality`, which
  serves ETL: a business registry's registration log in two systems' layouts, its open caseload snapshot and its
  holiday calendar conformed by office and application, and each office's third-quarter timeliness measured.
- **The decision and the quantity:** the registry's management board places on a timeliness improvement plan the
  regional offices whose median working days from a complete application to registration, for applications received
  from 1 July to 30 September 2026, exceed 20. Forward facing in its data: at the 9 October extract the quarter's
  applications are still being registered.
- **Data-native sentence:** at the extract a share of each office's third-quarter applications is still open, listed
  only as counts by office and receipt day in the open caseload snapshot, and the open ones are the slow ones.
- **Strategy:** `other` (maturity_censoring, banned against task179 at stage 3); Gate G `etl_conformance`; gap `time`;
  generators G9, G12 (G12 banned against task179 as the decisive pattern at stage 3; differentiation for task100); context
  artifact capacity_report then published_series (bans against task179 and task486) to monitoring_export. Layer 2 family
  `estimand_identification`, pattern `own:a cohort's median duration read from its finished members alone when the
  unfinished are the slow ones`.

## Default path

A strong analyst with every field read correctly:

1. Reads the paper: an office goes on a plan when the median working days from a complete application to
   registration, for its July to September 2026 receipts, exceeds 20, every application counting, registered or open.
2. Stacks the legacy and case system logs, keeps the third-quarter receipts, counts working days from the clock start
   (not counted) to registration with the holiday calendar, and takes each office's median.
3. Compares with 20.

**Ends on:** CRO-FM and CRO-MG planned

- On that path the four backlog offices CRO-AD, CRO-CV, CRO-GQ and CRO-LW stand at 14 to 15 working days. Counting
  each open application at its age gives the same two; counting every open application as over the line adds CRO-DL,
  CRO-IB and CRO-SL, whose open applications are mostly late-September receipts only days old.

**Golden:** CRO-AD, CRO-CV, CRO-FM, CRO-GQ, CRO-LW and CRO-MG planned; with each open application at risk until its
age, the product-limit medians are 26 to 28 working days in the six and 9 to 16 elsewhere.

## Stump sentence

The default path takes each office's median working days over its registered third-quarter applications and files CRO-FM and CRO-MG planned, because it never asks how long the applications still open at the extract will take: they are the slow ones, so the four offices with a backlog look quick on what they have registered, and only the product-limit median over registered and open applications, each open one at risk until its age, gives the quarter's median.

## Three rules

Task type: census-register-administrative-data-quality (Survey Research & Official Statistics): a registry's case logs in two systems' layouts, its open caseload snapshot and its holiday calendar conformed by office and application into working-day durations, and each office's timeliness measured for one cohort, a conformation serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each office's median processing time for one quarter's applications, worked the way official statistics measures the timeliness of a register's intake from a cohort still being processed: the open cases are right-censored at their age and the median is read from the product-limit (Kaplan-Meier) survival estimate over the whole cohort.

Swap: "which bakeries' median loaf weight exceeds 800 grams" keeps a median and loses the step: no member of the cohort is still running at the cut, nothing is censored, and the finished members are the whole cohort.

Layer 1: the legacy log's DD/MM/YYYY dates and two-letter office codes against the case system's, the migration of applications in hand on 1 August, working days against calendar days and the holiday calendar, query restarts moving the clock, June and October receipts in the logs, the open caseload by office, receipt and clock start rather than by application, and card payments carrying the settlement day while their batches carry the day paid (the ask); each is how the producing systems write, nothing is placed to be caught, and checks.py asserts the call under them (SF2 to SF7).

Layer 2: estimand_identification, a cohort's median from records some of which have not ended: the choice that flips the call is keeping each open application at risk until its age (the product-limit median), instead of taking the registered applications' median or treating the open ones as finished at their age or as late.

Decisive step: estimating each office's median working days by the product-limit estimate over its registered and open third-quarter applications, the open ones censored at their working days on 9 October, which puts CRO-AD, CRO-CV, CRO-GQ and CRO-LW at 26 to 28 days and keeps CRO-DL, CRO-IB and CRO-SL at 16.

Not semantics: every field, code and definition read correctly (the two logs, the clock start, working days, the holidays, the open caseload's counts) still leaves the easy route on the median of what has been registered or the median with each open application at its age, because no field gives an open application's duration; the step is the inference that an open application has lasted at least its age and that the open ones are the slow ones, which the open caseload against the registrations shows and no sentence says.

Not rule application: the paper fixes the population (every third-quarter receipt, registered or open), the outcome (working days from complete to registration), the unit, the window and the comparison, and no rule says how an open application's duration enters the median; executing every filed rule on the registered applications files CRO-FM and CRO-MG planned.

Analyst test: a strong analyst who conforms every file and reads every rule, taking each office's median over its registered applications, files CRO-FM and CRO-MG planned (the default path's Ends on); one who counts open applications at their age files the same; one who counts them as late files nine offices; only the product-limit median files the golden six; checks.py runs them on the clean truth (R3a to R3c).

Estimand: the board paper (cro_board_paper_timeliness_q3_2026.pdf, section 2): the population (every application an office received from 1 July to 30 September 2026, registered by 9 October or still open), the outcome (working days from the complete day, not counted, to the registration day, weekends and the calendar's holidays excluded), the unit (each office's median), the window (the third-quarter cohort) and the comparison (exceeding 20).

No decoy: nothing is planted: the logs, the open caseload, the calendar, the payments and batches are the producing systems' records, the paper states the basis without a method, and no earlier timeliness report, published median or ranking ships; the staffing workbook and the customer survey rank nothing on the third quarter's working days.

No certified replay: no certified or published median, survival estimate or backlog projection ships; the method is not recovered by reproducing any figure.

Lesson: a cohort's median read while the cohort is still running is a censored estimate, and the members still running are the slow ones; no build on file reads a cohort's median processing time with the open cases censored at their age.

## Readability screen

Each rung, the sentence or file a reader would have to read to take it, and whether any shipped text hands it over.

| Rung | What takes the reader there | Verdict |
|---|---|---|
| R0 every open application counted as late | the paper's "those still open on it" | readable |
| Layer 1: two logs, working days, holidays, migration | the dictionary and the paper's section 3 | readable |
| R1 (default path) the median of the registered | the logs | readable |
| R2 open applications at their age | the open caseload's clock start | readable |
| R3 (decisive) the product-limit median, open applications censored at their age | nothing: no sentence names censoring, a survival estimate or a lower bound on an open application's duration | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the cohort | receipts 1 July to 30 September 2026 | registrations in the quarter | not filed alternatives | paper section 2 |
| SF2 | the start day | not counted | counted | same call (no office within 1.5 days, C2) | paper section 2 |
| SF3 | working days | weekdays less the calendar's holidays | calendar days | not filed alternatives (calendar days file nine) | paper section 2 |
| SF4 | open applications | in the population | left out | not filed alternatives | paper section 2 |
| SF5 | the clock start | the complete day | receipt | not filed alternatives | paper section 2; the logs' clock start |
| SF6 | the two logs | one record per registration | duplicates | same call (none, asserted) | SF6 |
| SF7 | the clock start against receipt | on or after | before | same call (asserted) | SF7 |
| SF8 | exceeds | strictly over | at or over | same call (C2) | paper section 2 |

## Ladder

Built values from the cut pack (generator/checks.py L1 to L3, C2, C3), median working days.

| Rung | Route | Planned | CRO-AD, CRO-CV, CRO-GQ, CRO-LW / CRO-DL, CRO-IB, CRO-SL |
|---|---|---|---|
| R0 | every open application as late | nine offices | 33, 34, 33.5, 32 / 25, 24, 23 |
| R1 (default path) | the registered alone | CRO-FM, CRO-MG | 15, 15, 14, 14 / 13, 13, 13 |
| R2 | open applications at their age | CRO-FM, CRO-MG | 18, 18, 18, 17 / 12, 12, 12 |
| Golden | the product-limit median | CRO-AD, CRO-CV, CRO-FM, CRO-GQ, CRO-LW, CRO-MG | 27, 27, 28, 26 / 16, 16, 16 |

- Dominance: under the product-limit median, its interpolated form and its strict form, every office sits 1.5 working
  days or more from 20 (C2), and each lies within two days of the quarter's own median once every application is
  registered (C3).
- The data separates the readings: in the backlog offices a third or more of the quarter is open at the extract, the
  open applications are older than the registered median, and the late-September filing rush leaves CRO-DL, CRO-IB
  and CRO-SL with many open applications only days old.

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every third-quarter receipt | filed (SF1, SF4) |
| 2 | Unit of account | each office's median | filed |
| 3 | Attribution window | receipts 1 July to 30 September | filed |
| 4 | As-of dating | the 9 October extract | filed |
| 5 | Version basis | one record per registration | SF6 |
| 6 | Denominator | none | commutes |
| 7 | Weighting | none | commutes |
| 8 | Window length | one quarter | filed |
| 9 | Boundary inclusivity | strictly over 20 | SF8 |
| 10 | Rounding path | whole working days | C2 |
| 11 | Tie-break | none | C2 |
| 12 | Maturity and censoring | open applications censored at their age | the decisive step |
| 13 | Order of operations | conform, count days, estimate, compare | commutes |
| 14 | Row order | none | commutes |
| 15 | Duplicate resolution | none | SF6 |
| 16 | Identity normalisation | office codes across logs | the dictionary |
| 17 | Netting against gross | none | commutes |
| 18 | Dimensional units | working against calendar days | SF3 |
| 19 | Code and status semantics | query flag, service | the dictionary; never the stump |
| 20 | Integerisation | whole days | commutes |
| 21 | Clause scope | every office | filed |
| 22 | Forward window contents | the open applications' completion | the decisive step |

## Literal reader

The paper executed word for word asks for each office's median working days over every application it received in the
quarter, registered or still open; the literal question is a median over durations some of which are still running,
which the registered durations and the open applications' ages answer only as a censored sample. A literal reader who
takes the registered median or counts open applications at their age has assumed the open ones finish at once, which
their ages and the backlog contradict; every other reading converges or violates a quoted sentence (fork table).
Re-run on the finished pack.

## Oracles

- No shipped file carries a median, a survival estimate or a ranking of the offices on the third quarter.
- The staffing workbook and the customer survey are distractors (metadata.json).
- No control ties only under the golden on the ask.

## Ask sheet

- **Ask, each office's card payments made in the third quarter of 2026, number and amount (fourteen offices, two
  figures each, whole numbers and whole euros).** H18 home: the fee income the plans are costed against (paper section
  4). Path: the payment file (reference, office, batch, settlement day, amount) and the batch file (batch, terminal
  day, settlement day). Primary device: D8, a settlement date for the event date: the payment file carries only the
  day the acquirer settled the payment, the next working day, so filtering it on the quarter takes in 30 June's
  payments and leaves out 30 September's; only the batch's terminal day dates a payment. Hazards: the batch file's own
  totals tie under either dating.
- **The construction layer:** the call, the fourteen decisions and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads the two logs, the open caseload and the holidays; the ask
  reads the payments and batches only (X1).
- **Hazard table (asserted):** A1, A2 in checks.py; none moves the call.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| Third-quarter card payments | the payment file's settlement day; keeps 0 of 28 | miss |

- Mirror leakage: 0.0 per cent of ask weight on the cut pack (0 of 28).
- Pair ceiling: 36.0 on the cut pack (weights 38 / 7 / 55: the cracker keeps the call and instructions, 45.0; the
  mirror at the default path misses the set and keeps 10 of 14 decisions, 27.0). Re-measured by the stage 4 readers.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

READERS_LINE

JUDGE_LINE

## Tried and rejected
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
