# FC28 — How much the January winter guarantee will pay drivers, when a wave of last winter's recruits returns through neither the onboarding funnel nor December's roster

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · platform labour supply and marketplace incentives |
| Mirrors | Supply incentives funded before a seasonal wave of returning workers (Uber and Lyft winter driver guarantees, DoorDash and Instacart holiday boosts, Amazon Flex peak-season block pay), where returners appear in neither the onboarding funnel nor last month's active roster |
| Decision shape | One figure committed at a date: the January guarantee fund finance pre-funds on Monday 4 January |
| Committed call | The total the winter guarantee will pay for the four weeks of January, to the nearest $10,000 |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S2 (a residual population between two correct records, projected on a single-valued interval), with finer controls separating constructions (measured #12) at rung 2 |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #12 stops at the first control that passes · #13 validates on one population, applies to another · #4 never tests its reading against the control |
| Calibration form | Counterparty acknowledgement file: the insurer's acknowledgement of every monthly driver-roster declaration since January 2024, each driver listed with the date they were first declared |
| Driving force | Seasonal drivers who lapse in spring come back in January. They are in neither the onboarding stream (they are not new) nor December's active roster (they were away), so the only exact record of them is the residual between consecutive insurer acknowledgements. They return on a single-valued interval: 70% of each winter cohort's spring lapsers reappear in the same calendar month a year on. Last January's recruitment campaign made that cohort 6,000 lapsers instead of the usual 2,700–3,700, and returners qualify for the guarantee at 0.80 against 0.30 for continuing drivers. |

## 1. Situation

A ride-hail operator in a large Midwestern city runs a winter guarantee: every driver who completes 40 trips in the four January weeks
receives a flat $350 top-up. Finance pre-funds the whole guarantee on the first Monday of January and asks driver operations for one
figure. The pack holds the monthly supply KPI report (active, continuing and first-trip drivers), the onboarding pipeline, the
driver-month activity extract, last two Januaries' guarantee payout files, and the insurer's acknowledgement file for the monthly roster
the operator declares to its commercial auto insurer. Last January the operator ran its first winter recruitment campaign, and most of
the recruits had stopped driving by May.

## 2. Gate G: why this is legal

* **Litmus.** Every figure in the pack is correct: the KPI series, the pipeline, the payout files and every acknowledgement. No
  stakeholder's reading of their own numbers is overturned; the campaign recruits did stop driving in spring. The difficulty is a
  population that January will contain and that neither the funnel nor December's roster records.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and last year's payout total. The stock-flow model still reproduces every closed month it is
  calibrated on, and it still has no term for drivers who return after a gap.
* **Instrument repair.** Clean-data test. No file the ladder reads is incomplete, stale or narrower than it claims: the KPI report's
  active, continuing and first-trip counts are exact, the insurer's acknowledgements list every declared driver with the date first
  declared, and the payout files hold every payment. The deepest repair available, a KPI report with a returning-driver line, leaves rung
  0 at $2,904,200, rung 1 at $2,102,100 and rung 2 at $2,634,100 (it would show last January's 1,900 returners, the constant rung 2
  already carries), and the decisive projection is still needed, because this January's returners come from last spring's 6,000 lapsers
  and have not returned yet.
* **Lens swap.** The naive read and the answer are different populations at different moments: last January's mix of continuing, new
  and returning drivers, against this January's, whose returners come from a cohort more than twice as large.

## 3. The driving force

A strong solver builds the January forecast the way the supply team does: December's active drivers carried forward at measured
retention, plus January's first-trip drivers from the pipeline, each qualifying at its measured rate. Calibrated on closed months, the
model under-fits every January, so the solver adds last January's unexplained drivers back as a seasonal term and reproduces last
January's KPI total exactly. That term is a constant, and the population it stands for is not. The drivers January adds outside the
funnel are seasonal workers returning a year after their first winter; the insurer's acknowledgements show them as drivers re-declared
after a gap, with a first-declared date a year or more old, and every closed January shows 70% of the previous winter's spring lapsers
coming back. Last January's campaign recruited 6,600 winter drivers and 6,000 of them lapsed by May. The returning wave this January
is 4,200 drivers, against 1,900 last year, and returners drive full weeks: 80% of them qualify.

## 4. The ladder

| Rung | Construction | Lands on (fund) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Last January's guarantee payout grown at the December active-driver growth rate (4.9%) | $2,904,200 (−11.4%) | Finance's own budgeting basis, and January's seasonality is carried whole | The pipeline holds 2,000 January first-trip drivers against last January's 6,600: the mix has changed |
| 1 | Stock-flow: December's active drivers × measured January retention × 0.30, plus pipeline first-trip drivers × 0.15 | $2,102,100 (−35.9%) | Reproduces every closed non-January month to within 0.5% and is the model finance signs off | The KPI report: the model falls short of every closed January's active total |
| 2 | Stock-flow plus last January's unexplained drivers (1,900) carried as a seasonal constant, qualifying at their own measured 0.80 | $2,634,100 (−19.6%) | Reproduces last January's active total and its payout exactly: the salient controls pass | The acknowledgement file's finer controls: January 2025 held 2,600 returners, not 1,900, and no constant or share of December reproduces both Januaries |
| 3 | **Decisive:** returners recovered as the residual between consecutive acknowledgements and projected on their twelve-month interval, 70% of last winter's 6,000 spring lapsers, qualifying at 0.80 | **$3,278,100** | — | — |

* **Figure shape.** Every rung lands below the answer (−11.4%, −35.9%, −19.6%), so the answer is the maximum cell and every partial
  build under-funds the guarantee.
* **Partial correction priced (L3).** A solver who recovers the returners but projects them as a share of December's active drivers
  (9.2%) lands at $2,660,000 (−18.9%), beside rung 2. One who projects them from the right cohort but qualifies them at the continuing
  rate (0.30) lands at $2,543,100 (−22.4%), further away than rung 2.
* **Grid.** Base (seasonal grow-on or stock-flow) × returners (none, last January's count, share of December, cohort interval) ×
  returner qualification (continuing rate or their own) = 16 cells. Every wrong cell sits at least 11% from the answer. The nearest is
  rung 0 (−11.4%), and the only cell above the answer, every lapser returning, lands at $3,782,100 (+15.4%) against a return share three
  closed winters pin at 0.70.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The KPI definitions cover active, continuing and first-trip drivers. No document mentions returning drivers, a
   return interval or a return share, and the insurer's file is a roster acknowledgement with no reason codes.
2. **Corpus blind to the wave's size.** The acknowledgement file pins the rule but has never seen this wave: *in every closed January
   the returners came from an organic winter cohort of 2,700–3,700 spring lapsers, because the operator had never recruited in winter
   before January 2026.*
3. **No arithmetic symptom.** Declarations reconcile to the KPI report's active counts, approvals to first-trip drivers, and both payout
   files to their qualifying drivers on every rung.
4. **Not a row predicate.** A returner is a set difference across two monthly acknowledgements joined to first-declared dates, and its
   forward count needs the cohort of drivers whose first winter month was a year earlier and who lapsed by spring.
5. **The enumeration is arithmetic.** No column says "returning" or "seasonal"; the January 2027 returners are computed from last
   winter's cohort and the return share.
6. **No cutover date in the decisive cause.** The campaign is dated and loud, and it points the wrong way: its recruits visibly vanish by
   May. The return is a twelve-month interval from each driver's own first winter, and no outcome series steps on any date because of it.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The insurer's acknowledgement of every monthly roster declaration from January 2024 to December 2026: each declared driver,
  with the date they were first declared on any roster.
* **What it certifies.** The stock-flow terms: continuing drivers reconcile to consecutive declarations, and first-trip drivers to
  first-declared dates in the month.
* **What it pins.** The residual: drivers declared in a month, first declared a year or more earlier, absent from the month before. Every
  one in the three closed winters reappeared in the calendar month of their first trip a year on, and 70% of each winter's spring
  lapsers did (2,600 of 3,714 in January 2025; 1,900 of 2,714 in January 2026). No returner appears in any non-January month.
* **Twin pair.** The North Shore and Lakeview supply zones are identical on every KPI column from June to November 2026 and on their
  January pipeline. Their forecast January qualifying drivers differ 2.1×, because 1,640 of last winter's spring lapsers live in one and
  150 in the other. Only the residual and its interval separate them.
* **Resemblance points at the decoy.** January 2027's KPI profile (December actives, pipeline, retention) most resembles January 2026's,
  which rung 2 reproduces exactly.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The incentive policy: a driver who completes 40 trips in the four January weeks receives $350. Finance's funding note:
  the guarantee is pre-funded in full on the first Monday of January. The KPI definitions of active, continuing and first-trip drivers.
* **Empirical pins.** Qualification rates by population (continuing 0.30, first-trip 0.15, returning 0.80), from the two payout files
  joined to the acknowledgements. The return share (0.70) and the twelve-month interval, from the acknowledgement file.
* **Voices.** The head of driver operations: "January is January; last year's payout plus growth has always been close." The supply
  analyst: "The campaign recruits were a one-off. Most of them had quit by April." The finance partner: "The stock-flow model is the
  one we sign off; it has matched every month this year."
* **Licensed wrong basis.** The funding note records that finance budgets the guarantee as last January's payout grown at the December
  active-driver growth rate and will present that figure at the funding review.

## 8. Determinism by construction

* **Interval.** Every returner in the closed winters reappeared in the same calendar month as their first trip a year earlier, so
  monthly, 52-week and 365-day readings select the same drivers.
* **Return share.** Exactly 0.70 in each closed winter, so no smoothing choice moves it.
* **Qualification.** No driver in either closed January finished within two trips of 40, so trip-counting conventions (cancelled or
  re-dispatched trips) select the same qualifiers.
* **Maturity.** The extract was taken on 2 January, after December's roster was declared and acknowledged, so December is complete.
* **Rounding.** The fund ($3,278,100) rounds to $3,280,000; only a shift of nine qualifying drivers down or twenty up would change the rounded figure.

## 9. Prompt sketch and deliverables

> Finance pre-funds the January winter guarantee on Monday the 4th and wants one number from me. Our head of driver operations is sure
> January will look like last January. Tell me what the guarantee will pay out across the four January weeks, to the nearest $10,000, in
> a line finance can put straight on the funding request. Send `guarantee_fund.xlsx` with the build and the sheets below, a chart
> `january_drivers.png`, and a one-page `fund_memo.pdf`.

* `guarantee_fund.xlsx` — the fund build, the wait-time sheet (ask A) and the surge sheet (ask B).
* `january_drivers.png` — stacked bars of qualifying drivers for January 2025, January 2026 and the January 2027 forecast, split into
  continuing, first-trip and returning drivers, with markers for the rung 0 and rung 2 forecasts, the $350 rate in the subtitle, and the
  committed fund annotated.
* `fund_memo.pdf` — the committed fund and the alternatives finance will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine supply zones, the median rider wait from request to pickup in each of the
  four December weeks. *Device:* a request re-dispatched after a driver cancels keeps its original request time under a new dispatch
  record, as the dispatch guide documents; measuring from the re-dispatch understates waits in four zones. Rider waits enter no part of
  the fund.
* **Ask B (device-carried).** For each zone, the share of December trips priced with surge and their median multiplier. *Device:* a fare
  re-quoted after a route change stores the second quote in the fare-adjustment table, as the pricing guide documents; reading the
  request-time quote misstates the multiplier in three zones.
* **Ask C (validity).** The fund under each of the four rung constructions, and whether each reproduces the qualifying-driver counts in
  the January 2025 and January 2026 payout files.
* **Decoupling.** Clearing the returning-driver term changes no figure in asks A or B.

## 11. Rubric arithmetic

9 zones × 4 weeks (ask A) + 9 zones × 2 (ask B) + 4 constructions × 3 (ask C) + the committed fund, the returner count and the qualifying
count + 5 named chart parts + 3 files ≈ 77 criteria.

## 12. World-building constraints

* January 2025: 17,000 continuing, 2,800 first-trip, 2,600 returning drivers. January 2026: 18,000 continuing, 6,600 first-trip (the
  campaign), 1,900 returning; 7,910 qualified. January 2027 forecast: 19,020 continuing, 2,000 first-trip, 4,200 returning (0.70 × 6,000);
  9,366 qualify, a fund of $3,278,100.
* Spring lapsers by winter cohort: 3,714 (2024), 2,714 (2025), 6,000 (2026). Returners appear only in January.
* Rung funds: $2,904,200 / $2,102,100 / $2,634,100 / $3,278,100; every other grid cell at least 11% away.
* The twin zones are identical on every KPI and pipeline column from June to November 2026.
* Re-dispatches and fare re-quotes touch no driver, trip count or qualification in the fund build.
