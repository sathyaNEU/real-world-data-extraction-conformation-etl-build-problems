# FC16 — Where six new customs-broker posts go across five import gateways, or whether to hold them, when the entry forecasts' own record decides the bar

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · express-carrier customs brokerage |
| Mirrors | Holding clearance headcount when the forecast's own track record says the case is not yet made (customs brokerage teams at DHL Express and Expeditors import gateways, clearance desks at Flexport and Amazon Global Logistics, where new shipper accounts from sales drives move entry volumes the forecast cannot know at issue) |
| Decision shape | An allocation under a cap: up to six funded broker posts across five import gateways, with unplaced posts held to the next cycle |
| Committed call | The posts placed at each gateway, or held, with the blocking quantity: the best gateway's lower-bound monthly entries per broker |
| Gap · Pattern | Gap 1 (time) over Gap 3 (objective) · hold as the answer, forced by a computed blocking quantity: the forecast's realised error, from the revision log, is wider than every gateway's margin over the staffing bar |
| Gate G mechanism | signal_vs_noise_or_hold, with forecasting and binding_constraint support |
| Measured traps engaged | #9 picks from the offered options when none passes · #10 notes a binding limit as a risk · #12 stops at the first control that passes |
| Calibration form | Revision log: every twelve-month entry forecast the planning team has issued over three years, by gateway and month, with its revisions and the realised outcome |
| Driving force | The staffing standard places a post only where the forecast's lower bound clears 1,500 entries per broker a month, the bound being the forecast less its 80th-percentile error. A back-test that re-runs the shipper-cohort model at past origins plugs in the new shipper accounts that actually arrived, and errs by 7%. The forecasts the team actually issued had to use the onboarding plans of their day, and the revision log shows them erring by 25%. At 25% the best gateway's lower bound is 1,275, 15% under the bar, and no gateway clears. |

## 1. Situation

An express carrier's customs brokerage files import entries for its shippers at five gateways and has six new broker posts for next year.
The staffing standard places a post, one at a time, at the gateway with the most forecast entries per broker a month. It does so only while
that gateway's lower bound exceeds 1,500. The lower bound is the point forecast less the 80th percentile of the forecasting method's
absolute errors at the twelve-month horizon. Every new broker files under a licensed senior broker's supervision for a year, and a senior
supervises one trainee at a time. Posts not placed are held to the next cycle. The planning team's shipper-cohort model is the filed method.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the entry history, the cohort model, the back-test, the revision log, the onboarding plan and the
  supervision register. No one's claim about their own numbers is overturned. The difficulty is which error the standard's bound is made
  of.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. The cohort model's point forecasts with its back-test interval still
  place three posts.
* **Instrument repair.** No file is suspect: the entry history holds every accepted entry, the revision log every issued vintage with the
  onboarding plan assumed at issue, and the supervision register every senior broker with their current trainee. Perfect records return the
  same rungs (2 · 2 · 1 · 1 · 0, then 1 · 2 · 1 · 1 · 0, then 1 · 0 · 1 · 1 · 0), because a model back-test plugs in the accounts that
  arrived, and the issued forecasts missed by 25% because onboarding plans changed after issue. No instrument can record next year's
  onboarding before it happens, so the error at issue is the forecast's own property, not a gap in any file.
* **Lens swap.** The naive read and the answer differ in moment: a forecast scored as if the future inflow were known, against the same
  forecast scored as it was issued.

## 3. The driving force

A strong solver replaces the aggregate year-on-year ratio with shipper-cohort retention, respects the supervision caps, and computes the
standard's lower bound from a careful back-test. It re-runs the cohort model at 24 past origins. That back-test needs each origin's
new-account inflow, and the planning memo's back-test procedure feeds the model the cohorts that actually arrived, as model back-tests
do. Scored that way the method errs by 7%, and three gateways clear the bar. The standard's bound is the method's error as a forecast,
and new accounts are the one input a forecast never knows. The revision log holds every twelve-month forecast the team issued, each made
with the onboarding plan of its day. Two marketplace onboarding drives were cancelled after issue and one was doubled, and 22 of the 60
issued forecasts were made before one of those changes. The 80th-percentile absolute error is 25%. At that width G1's 1,700 entries per
broker has a lower bound of 1,275, 225 (15%) short of the bar. Every other gateway is further short, so all six posts are held.

## 4. The ladder

| Rung | Construction | Lands on (G1 · G2 · G3 · G4 · G5 posts) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Aggregate year-on-year ratio applied to the latest totals, point forecasts, posts placed greedily while entries per broker exceed 1,500 | 2 · 2 · 1 · 1 · 0 | The team's long-standing forecast and the standard's placement order | **E14 (a binding limit applied in the figure):** the supervision register shows one senior broker free at G1, and every new broker files under a senior's supervision for a year |
| 1 | The same with each gateway capped at its free seniors | 1 · 2 · 1 · 1 · 0 (one held) | Every placement can actually be supervised | The entry history: shippers onboarded in last year's drives lapse far faster than established shippers, so the aggregate ratio overstates next year where drives ran |
| 2 | Shipper-cohort model (entries by months since a shipper's first entry, new accounts from next year's onboarding plan), lower bound from a 24-origin back-test with realised accounts (±7%) | 1 · 0 · 1 · 1 · 0 (three held) | The filed method, a rolling back-test, the standard's bound applied | The revision log: the forecasts actually issued, made with the onboarding plans of their day, erred by 25% at the 80th percentile |
| 3 | **Decisive:** the same forecasts with the bound built from the issued forecasts' realised errors (±25%) | **Hold all six: best lower bound 1,275 (G1), 225 (15%) short** | — | — |

* **Blocking quantity.** G1's lower bound is 1,700 × 0.75 = 1,275, 225 (15%) below the bar. G4 (1,260), G3 (1,245), G2 (1,181) and G5
  (900) fall further short. The hold would become a pick only if the realised error were below 11.8%; every defensible way of measuring
  it gives 23–28% (section 8), so the best lower bound stays 12.7–18.4% under the bar.
* **Figure shape.** Each correction removes placements (six, then five, then three, then none), so a solver who stops short always
  over-commits headcount.
* **Partial correction priced (L3).** Using the log's six-month-horizon errors (±11%) for a twelve-month forecast places one post at G1.
  Applying the realised ±25% to the aggregate forecasts places two (G1 and G2). Both commit headcount the evidence does not support.
* **Grid.** Forecast (aggregate, cohort) × caps (off, on) × bound (none, back-test, realised) gives 12 cells. The two that pair the
  cohort forecasts with the realised bound hold all six, because the caps bind nothing once nothing clears. Every other cell places at
  least two posts; the nearest, the realised bound on the aggregate forecasts, places two (G1 and G2).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "the method's 80th-percentile absolute error at the twelve-month horizon". No document says
   that a back-test with known accounts is not that error, or that onboarding plans changed after issue.
2. **Corpus blind for a computable reason.** *In every one of the 24 back-test origins the new-account inflow used is the inflow that
   arrived, because the memo's back-test procedure feeds the model observed cohorts.* The back-test reproduces the entry history within 7%
   and contains no onboarding surprise at all.
3. **No arithmetic symptom.** Cohorts tie to the entry history, the back-test ties to realised entries, and the supervision caps hold
   under every rung.
4. **Not a row predicate.** The blocking quantity is an order statistic over 60 issued forecasts' realised errors (12 vintages × 5
   gateways), set against each gateway's margin over the bar.
5. **The enumeration is arithmetic.** Which gateways clear depends on the computed interval. No column flags them.
6. **No cutover date.** Onboarding changes are spread over three years. No series steps, and the hold rests on an error distribution.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The revision log: twelve vintages of twelve-month forecasts for five gateways, each with the onboarding plan assumed at
  issue, each monthly revision and the realised average monthly entries.
* **What it certifies.** The cohort model's structure: with each vintage's own inflow it reproduces the realised outcomes within 2%, so
  rung 2's model is right and only its error at issue is wide.
* **What it pins.** The forecast error the standard asks for: the 80th percentile of 60 absolute errors at the twelve-month horizon is
  25%.
* **Twin pair.** The March vintages for G2 and G4 are identical on every column the log carries at issue: point forecast, model
  parameters and planned onboarding growth. They realised errors of −12% and −25% (2.1×), because G4's planned marketplace onboarding
  drive was cancelled two months after issue. A back-test that plugs in realised accounts gives both −3%.
* **Resemblance points at the decoy.** Next year's onboarding plan most resembles the plans of the stable-inflow vintages, whose errors
  were small.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The staffing standard: posts are placed one at a time at the gateway with the most forecast entries per broker a month,
  while its lower bound (forecast less the method's 80th-percentile absolute twelve-month error) exceeds 1,500; unplaced posts are held.
  The planning memo: an entry is a declaration filed and accepted, amendments excluded, and the shipper-cohort model is the method,
  back-tested by re-running it at past origins on the cohorts observed. The supervision policy: one trainee per senior broker per year.
* **Empirical pins.** The interval, from the revision log. Entries by shipper-cohort age, from the entry history.
* **Voices.** The head of gateway operations: "The big gateways are always short of brokers; the numbers just confirm it." The planning
  analyst: "Our model back-tests within seven per cent. That's tight enough to hire on."
* **Licensed wrong basis.** The standard records that the executive committee reviews staffing proposals on point forecasts and will see
  the placements on that basis.

## 8. Determinism by construction

* **Interval.** G1 qualifies only below 11.8%. Every defensible measurement of the issued forecasts' error stays at least 11 points above
  that: the 80th percentile of the 60 absolute errors of the annual average is 25% with inclusive interpolation, 26% exclusive and 25%
  nearest-rank; 23% with errors scaled by the forecast instead of the outcome; 28% on the twelfth month alone instead of the annual
  average; 24% pooling the ten- to fourteen-month horizons; and 23% on G1's own twelve errors. The best lower bound runs from 1,224 to
  1,309, 12.7–18.4% under the bar.
* **Placement order.** No two gateways tie on entries per broker at any step of any rung.
* **Entries.** The entry definition (accepted declarations, amendments excluded) is filed, and the cohort model reproduces the published
  monthly entry counts exactly.
* **Supervision.** The register lists seniors by name with their current trainee, and every free senior has capacity for exactly one.
* **Maturity.** Every vintage in the log is at least twelve months old, so all 60 errors are realised.

## 9. Prompt sketch and deliverables

> We have six new broker posts for next year across our five import gateways. Tell me where each goes, or which we hold to next year if
> the case isn't there, in a form I can take to the executive committee. Our head of gateway operations expects the big gateways to take
> them all. Send `broker_placement.xlsx`, a chart `staffing_bar_check.png`, and a one-page `committee_note.pdf`.

* `broker_placement.xlsx` — forecasts, bounds and placements under each construction, the holds sheet (ask A) and the penalty sheet
  (ask B).
* `staffing_bar_check.png` — each gateway's forecast entries per broker as a point, with the ±7% back-test and ±25% realised intervals as
  error bars, the 1,500 bar as a labelled line, supervision caps annotated, and the hold verdict in the title.
* `committee_note.pdf` — the committed placement or hold, the blocking quantity, and what would change it.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each gateway, monthly cargo holds over the last year and the share released within seven
  days. *Device:* extending a hold is logged as a release and a new hold under the same hold ID, as the hold-logging guide documents.
  Counting those paired releases as real releases inflates the released share at three gateways.
* **Ask B (device-carried).** For each gateway, the penalty notices received over the last year and the share reduced on mitigation.
  *Device:* a mitigated notice is reissued as a new notice citing the original's number, and the penalty guide counts only the latest
  issue. Counting every row overstates notices at four gateways and halves their reduced share.
* **Ask C (validity).** The placement under each of the four rung constructions, with each one's interval and the best gateway's lower
  bound.
* **Decoupling.** Replacing the realised interval with the back-test interval changes no figure in asks A or B.

## 11. Rubric arithmetic

5 gateways × 3 (ask A: mean monthly holds, released share, worst month) + 5 gateways × 2 (ask B) + 4 constructions × 3 (ask C) + the
hold, the blocking quantity, its shortfall and the falsifying error + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Brokers: G1–G5 have 4, 4, 4, 3 and 3; free senior brokers 1, 2, 2, 2 and 2.
* Aggregate forecasts (entries a month): 9,600 / 8,200 / 6,800 / 5,250 / 3,900. Cohort forecasts: 6,800 / 6,300 / 6,640 / 5,040 / 3,600.
* Back-test 80th-percentile error 7%; issued-forecast 80th-percentile error 25% (23–28% across the conventions in section 8). 22 of the
  60 issued forecasts precede an onboarding-plan change, and shippers from a drive make up 30–45% of a gateway's entries in drive years.
  With each vintage's own inflow the model reproduces outcomes within 2%.
* Placements 6 / 5 / 3 / 0 across the rungs. G2's and G4's March vintages are identical at issue.
* Hold extensions and reissued penalty notices never touch entries, cohorts or the revision log.
