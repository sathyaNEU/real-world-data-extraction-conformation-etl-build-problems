# FC16 — Where six new moderator positions go next year, or whether to hold them, when the forecast's own record decides the bar

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Nonprofit & Grant-making · open-knowledge community operations |
| Mirrors | Holding headcount when the forecast's own track record says the staffing case is not yet made (moderator staffing on community-growth forecasts at Meta and Reddit, support headcount on usage forecasts at Google, trust-and-safety hiring at marketplaces) |
| Decision shape | An allocation under a cap: up to six funded moderator positions across five language wikis, with unplaced positions held to the next cycle |
| Committed call | The positions placed on each wiki, or held, with the blocking quantity: the best wiki's lower-bound active contributors per moderator |
| Gap · Pattern | Gap 1 (time) over Gap 3 (objective) · hold as the answer, forced by a computed blocking quantity: the forecast's realised error, from the revision log, is wider than every wiki's margin over the staffing bar |
| Gate G mechanism | signal_vs_noise_or_hold, with forecasting and binding_constraint support |
| Measured traps engaged | #9 picks from the offered options when none passes · #10 notes a binding limit as a risk · #12 stops at the first control that passes |
| Calibration form | Revision log: every twelve-month forecast the growth team has issued over three years, by wiki and month, with its revisions and the realised outcome |
| Driving force | The staffing standard places a position only where the forecast's lower bound clears 1,500 active contributors per moderator, the bound being the forecast less its 80th-percentile error. A back-test that re-runs the cohort model at past origins plugs in the inflows that actually arrived, and errs by 7%. The forecasts the team actually issued had to use the campaign plans of their day, and the revision log shows them erring by 18%. At 18% the best wiki's lower bound is 1,394, and no wiki clears. |

## 1. Situation

An open-knowledge foundation funds moderators for its language wikis and has six new positions for next year. The staffing standard
places a position, one at a time, on the wiki with the most forecast active contributors per moderator. It does so only while that wiki's
lower bound exceeds 1,500. The lower bound is the point forecast less the 80th percentile of the forecasting method's absolute errors at
the twelve-month horizon. Every new moderator is paired with a mentor, and a mentor takes one mentee a year. Positions not placed are
held to the next cycle. The growth team's cohort model is the filed method.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the edit history, the cohort model, the back-test, the revision log, the campaign plan and the
  mentorship register. No one's claim about their own numbers is overturned. The difficulty is which error the standard's bound is made
  of.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. The cohort model's point forecasts with its back-test interval still
  place three positions.
* **Instrument repair.** Count every edit perfectly. The issued forecasts still missed by 18%, because the inflows they had to assume
  changed after issue. A better record of the past does not shrink the error of a forecast about the future.
* **Lens swap.** The naive read and the answer differ in moment: a forecast scored as if the future inflow were known, against the same
  forecast scored as it was issued.

## 3. The driving force

A strong solver replaces the aggregate retention ratio with cohort retention, respects the mentorship caps, and computes the standard's
lower bound from a careful back-test. It re-runs the cohort model at 24 past origins. That back-test needs each origin's new-contributor
inflow. The campaign plans of those origins were overwritten, and only next year's plan ships, so the back-test uses the inflow that
actually arrived. Scored that way the method errs by 7%, and three wikis clear the bar. The standard's bound is the method's error as a
forecast, and inflow is the one input a forecast never knows. The revision log holds every twelve-month forecast the team issued, each
made with the plan of its day. Two campaigns were cancelled after issue and one was doubled. The 80th-percentile absolute error is 18%.
At that width W1's 1,700 per moderator has a lower bound of 1,394, 106 short of the bar. Every other wiki is further short, so all six
positions are held.

## 4. The ladder

| Rung | Construction | Lands on (W1 · W2 · W3 · W4 · W5 positions) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Aggregate retention ratio applied to the latest totals, point forecasts, positions placed greedily while per-moderator load exceeds 1,500 | 2 · 2 · 1 · 1 · 0 | The team's long-standing forecast and the standard's placement order | **E14 (a binding limit applied in the figure):** the mentorship register shows one mentor on W1, and every new moderator needs a mentor that year |
| 1 | The same with each wiki capped at its mentors | 1 · 2 · 1 · 1 · 0 (one held) | Every placement can actually be onboarded | The edit history: last year's campaign cohorts lapse far faster than tenured editors, so the aggregate ratio overstates next year where campaigns ran |
| 2 | Cohort model (retention by months since first edit, new cohorts from next year's plan), lower bound from a 24-origin back-test with realised inflows (±7%) | 1 · 0 · 1 · 1 · 0 (three held) | The filed method, a rolling back-test, the standard's bound applied | The revision log: the forecasts actually issued, made with the plans of their day, erred by 18% at the 80th percentile |
| 3 | **Decisive:** the same forecasts with the bound built from the issued forecasts' realised errors (±18%) | **Hold all six: best lower bound 1,394 (W1), 106 short** | — | — |

* **Blocking quantity.** W1's lower bound is 1,700 × 0.82 = 1,394, 106 below the bar. W4 (1,378), W3 (1,361), W2 (1,292) and W5 (984)
  fall further short. The hold would become a pick if the realised error were below 11.8%; the log's 80th percentile is 18% under every
  interpolation convention (17–19%).
* **Figure shape.** Each correction removes placements (six, then five, then three, then none), so a solver who stops short always
  over-commits headcount.
* **Partial correction priced (L3).** Using the log's six-month-horizon errors (±11%) for a twelve-month forecast places one position
  on W1. Applying the realised ±18% to the aggregate forecasts places two (W1 and W2). Both commit headcount the evidence does not
  support.
* **Grid.** Forecast (aggregate, cohort) × caps (off, on) × bound (none, back-test, realised) gives 12 cells. Every cell except the answer
  places at least one position. The nearest wrong cell places one.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "the method's 80th-percentile absolute error at the twelve-month horizon". No document says
   that a back-test with known inflows is not that error, or that inflow plans changed after issue.
2. **Corpus blind for a computable reason.** *In every one of the 24 back-test origins the inflow used is the inflow that arrived,
   because past campaign plans were overwritten and only next year's plan ships.* The back-test reproduces the edit history to within 7%
   and contains no inflow surprise at all.
3. **No arithmetic symptom.** Cohorts tie to the edit history, the back-test ties to realised actives, and the mentorship caps hold
   under every rung.
4. **Not a row predicate.** The blocking quantity is an order statistic over 60 issued forecasts' realised errors (12 vintages × 5
   wikis), set against each wiki's margin over the bar.
5. **The enumeration is arithmetic.** Which wikis clear depends on the computed interval. No column flags them.
6. **No cutover date.** Campaign changes are spread over three years. No series steps, and the hold rests on an error distribution.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The revision log: twelve vintages of twelve-month forecasts for five wikis, each with the campaign plan assumed at issue,
  each monthly revision and the realised average active contributors.
* **What it certifies.** The cohort model's structure: with each vintage's own inflow it reproduces the realised outcomes within 2%, so
  rung 2's model is right and only its error at issue is wide.
* **What it pins.** The forecast error the standard asks for: the 80th percentile of 60 absolute errors at the twelve-month horizon is
  18%.
* **Twin pair.** The March vintages for W2 and W4 are identical on every column the log carries at issue: point forecast, model
  parameters and planned inflow growth. They realised errors of −8% and −17% (2.1×), because W4's planned campaign was cancelled two
  months after issue. A back-test that plugs in realised inflow gives both −3%.
* **Resemblance points at the decoy.** Next year's plan most resembles the plans of the stable-inflow vintages, whose errors were small.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The staffing standard: positions are placed one at a time on the wiki with the most forecast active contributors per
  moderator, while its lower bound (forecast less the method's 80th-percentile absolute twelve-month error) exceeds 1,500; unplaced
  positions are held. The growth memo: active means five or more edits in a month by a registered non-bot account, and the cohort model is
  the method. The mentorship policy: one mentee per mentor per year.
* **Empirical pins.** The interval, from the revision log. Retention by cohort age, from the edit history.
* **Voices.** The community-support director: "Big wikis always need more moderators; the numbers just confirm it." The growth analyst:
  "Our model back-tests within seven per cent. That's tight enough to staff on."
* **Licensed wrong basis.** The standard records that the board's finance committee reviews staffing proposals on point forecasts and
  will see the placements on that basis.

## 8. Determinism by construction

* **Interval.** 60 errors at one horizon. Inclusive, exclusive and nearest-rank 80th percentiles give 17–19%, all above the 11.8% that
  would let W1 qualify.
* **Placement order.** No two wikis tie on load per moderator at any step of any rung.
* **Activity.** The five-edit threshold and bot exclusion are filed, and the cohort model reproduces the published active counts
  exactly.
* **Mentors.** The register lists mentors by name with their current mentee, and every mentor has capacity for exactly one.
* **Maturity.** Every vintage in the log is at least twelve months old, so all 60 errors are realised.

## 9. Prompt sketch and deliverables

> We have six new moderator positions for next year across our five language wikis. Tell me where each goes, or which we hold to next
> year if the case isn't there, in a form I can put to the board. Our community-support director expects the big wikis to take them all.
> Send `moderator_placement.xlsx`, a chart `staffing_bar_check.png`, and a one-page `board_note.pdf`.

* `moderator_placement.xlsx` — forecasts, bounds and placements under each construction, the admin-actions sheet (ask A) and the
  response-time sheet (ask B).
* `staffing_bar_check.png` — each wiki's forecast active contributors per moderator as a point, with the ±7% back-test and ±18% realised
  intervals as error bars, the 1,500 bar as a labelled line, mentor caps annotated, and the hold verdict in the title.
* `board_note.pdf` — the committed placement or hold, the blocking quantity, and what would change it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each wiki, monthly administrator blocks over the last year and the share undone within seven
  days. *Device:* changing a block's length is logged as an unblock and a reblock under the same block ID, as the logging guide documents.
  Counting those unblocks as reversals inflates the undone share at three wikis.
* **Ask B (device-carried).** For each wiki, the median and 90th-percentile hours from a vandalism report to a moderator's first action
  over the last six months. *Device:* a report merged into an earlier duplicate keeps a "duplicate of" reference, and the response clock
  runs on the surviving report. Timing every report separately overstates both figures at four wikis.
* **Ask C (validity).** The placement under each of the four rung constructions, with each one's interval and the best wiki's lower
  bound.
* **Decoupling.** Replacing the realised interval with the back-test interval changes no figure in asks A or B.

## 11. Rubric arithmetic

5 wikis × 3 (ask A: mean monthly blocks, undone share, worst month) + 5 wikis × 2 (ask B) + 4 constructions × 3 (ask C) + the hold, the
blocking quantity, its shortfall and the falsifying error + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Moderators: W1–W5 have 4, 4, 4, 3 and 3; mentors 1, 2, 2, 2 and 2.
* Aggregate forecasts: 9,600 / 8,200 / 6,800 / 5,250 / 3,900. Cohort forecasts: 6,800 / 6,300 / 6,640 / 5,040 / 3,600.
* Back-test 80th-percentile error 7%; issued-forecast 80th-percentile error 18%. With each vintage's own inflow the model reproduces
  outcomes within 2%.
* Placements 6 / 5 / 3 / 0 across the rungs. W2's and W4's March vintages are identical at issue.
* Block-length changes and merged reports never touch edits, cohorts or the revision log.
