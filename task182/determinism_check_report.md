# determinism-check report, task182, 2026-10-11

Pass 1, run at `/build` stage 7.

**How this pass was run:** this session had no `Agent` tool, so the judge pass ran in the orchestrator's own context instead of in a spawned thread. Isolation was kept by order of work:
- Before the verdict, only `prompt.md`, the graded blocks of `submission.md`, a fresh copy of `target/` at `/tmp/determinism-check-task182-20261011T182952Z/target/` and `guidelines/determinism_judge_system_prompt.md` were read.
- The verdict was written to `/tmp/determinism-check-task182-20261011T182952Z/verdict.md` before `metadata.json`, the fingerprint card or `DESIGN_NOTE.md` was opened.
- The design note was then read only for the Gate G and Gate H reconciliation.
- `generator/`, the verifier, `solver_rounds/` and the earlier reports were never opened.

Every figure below was recomputed with pandas and numpy from the bundle. If you want the verdict from a separate thread, re-invoke in a session that has the `Agent` tool.

## Verdict
DETERMINISTIC, SOLUTION_WRONG

**Disposition:** FIX_NOW

**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

**Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical

## Why

**The offer list is forced.** I fitted each bore's own gamma response to daily rainfall less a fitted share of Morton evaporation on its record to 3 July 2022, then ran it forward. The mine's drawdown at the September 2026 level comes out at:
- 8.3 to 9.4 m at KV-LB04, LB05, LB07 and LB10 (trigger 5 m);
- 4.4 to 4.6 m at KV-LB12 (trigger 2 m);
- 2.4 m or less at the other 13 bores.

That holds in every fitting variant I tried and in a full-record fit with the metered take as a second stress. MG-02 6.1 turns those five bores into four agreements.

**The rival reading fails on the data.** The in-house solver used KV-LB16 as an unaffected coal-measures control. KV-LB16's own pre-take response fits at R2 0.998 and puts it 2.38 m above its September 2026 level. That departure is nil until 2023, then grows with the take and lags the near bores, so the control is itself drawn down. The solver's other claim, "the rainfall file could not reproduce the hydrographs", only holds for short-memory models. Rain lagged up to two years reaches R2 0.19 to 0.23 on the coal measures, while a gamma response with a 6 to 7 year mean lag reaches 0.998 or better.

**What is wrong is in the solution blocks.** Eleven of the 18 one-decimal "decline the mine has caused" values in the golden do not reproduce. The golden's fits come off a coarse grid (the Method sheet gives KV-LB04 an RMSE of 0.22 m, where a continuous fit reaches 0.027 m). This is solution_incorrect at figure level, repairable in the blocks without touching the prompt or the bundle.

## Recomputation ledger

**How the inputs were built.**
- Levels and changes: the dips were mapped across all three naming schemes, the 2012 to 2014 EIS rounds converted from feet, 35 double-keyed rows dropped, and pumped dips excluded by remark (MG-02 2.1). Each dip was reduced to the measuring point in force on the day.
- Loggers: compensated hourly against the barometric file and averaged by Queensland day. They agree with every check dip to within 0.01 m.
- Attributed decline: the best continuous fit, with the range across these variants in brackets:
  - all readings, monthly or weekly thinning, dips only;
  - calibration from 2015, or to mid-2021;
  - assessment taken at the dip dates;
  - AR(1) noise;
  - a full-record fit with the take as a second stress.

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| KV-LB01: level, change, mine decline, impaired | 209.51, -4.63, 0.8, no | 209.51, -4.63, 0.64 (0.53 to 0.68), no | level, change, call yes; decline no (0.6) |
| KV-LB02 | 205.24, -5.23, 0.7, no | 205.24, -5.23, 0.77 (0.75 to 0.81), no | decline no (0.8) |
| KV-LB03 | 204.86, -4.64, 0.5, no | 204.86, -4.64, 0.63 (0.61 to 0.64), no | decline no (0.6) |
| KV-LB04 | 207.77, -2.44, 8.9, yes | 207.77, -2.44, 8.71 (8.65 to 8.75), yes | decline no (8.7) |
| KV-LB05 | 214.47, -2.49, 9.3, yes | 214.47, -2.49, 9.33 (9.32 to 9.37), yes | yes |
| KV-LB06 | 209.61, -4.84, 0.6, no | 209.61, -4.84, 0.50 (0.23 to 0.58), no | decline no (0.5) |
| KV-LB07 | 195.44, -2.46, 8.4, yes | 195.44, -2.46, 8.39 (8.38 to 8.40), yes | yes |
| KV-LB08 | 201.27, -4.81, 0.4, no | 201.27, -4.81, 0.54 (0.47 to 0.56), no | decline no (0.5) |
| KV-LB09 | 199.16, -4.69, 0.3, no | 199.16, -4.69, 0.42 (0.36 to 0.46), no | decline no (0.4) |
| KV-LB10 | 203.49, -2.21, 8.2, yes | 203.49, -2.21, 8.32 (8.29 to 8.32), yes | decline no (8.3) |
| KV-LB11 | 238.12, -2.59, 1.1, no | 238.12, -2.59, 1.09 (1.07 to 1.12), no | yes |
| KV-LB12 | 209.50, -8.78, 4.6, yes | 209.50, -8.78, 4.45 (4.39 to 4.55), yes | decline no (4.4 or 4.5) |
| KV-LB13 | 202.33, -0.98, 0.2, no | 202.33, -0.98, 0.14 (0.13 to 0.18), no | decline no (0.1) |
| KV-LB14 | 201.88, -0.87, 0.1, no | 201.88, -0.87, 0.10 (0.09 to 0.14), no | yes |
| KV-LB15 | 241.33, -3.02, 1.6, no | 241.33, -3.02, 1.60 (1.60 to 1.69), no | yes |
| KV-LB16 | 209.84, +1.74, 2.4, no | 209.84, +1.74, 2.38 (2.36 to 2.41), no | yes |
| KV-LB17 | 243.13, -2.68, 0.9, no | 243.13, -2.68, 0.93 (0.91 to 0.94), no | yes |
| KV-LB18 | 245.75, -8.70, 1.3, no | 245.75, -8.70, 1.47 (1.47 to 1.57), no | decline no (1.5) |
| CC1: coal-measure falls since baseline | 2.44, 2.49, 2.46, 2.21 m | 2.44, 2.49, 2.46, 2.21 m | yes |
| CC2: mine's drawdown, coal measures and KV-LB12 | 8.9, 9.3, 8.4, 8.2; 4.6 m | 8.7, 9.3, 8.4, 8.3; 4.4 to 4.5 m | partly (LB04, LB10, LB12 no) |
| CC3: complainants' falls, then mine's share | 4.63, 5.23, 4.84, 8.70; 0.8, 0.7, 0.6, 1.3 m | falls the same; shares 0.6, 0.8, 0.5, 1.5 m | falls yes, shares no |
| CC4 and docx ask 2: impaired bores, owners, offers | 5 bores, 4 owners, 4 offers | 5, 4, 4 (MG-02 6.1, one agreement per owner) | yes |
| Docx ask 1: offers | Yarrowmere (LB04 and LB05), Tondara (LB07), Bluebush Downs (LB10), Cypress Ridge (LB12) | same, owners as in the register | yes |
| Docx ask 3: what lowered each complainant's bore | the dry seasons, all four | the climate-only path explains all but 0.5 to 1.5 m of each fall; water years 2022-23 to 2025-26 had 382, 373, 318 and 343 mm against about 560 mm | yes |
| Step 4: response memory | coal measures six to seven years, alluvium about half a year | coal measures 6.2 to 6.8 yr (shape about 16), alluvium 0.38 to 0.55 yr | yes |
| Step 6: fit tracks reference bores within 0.3 m | within 0.3 m | RF01 -0.04, RF02 -0.12, RF03 +0.01 m | yes |
| Step 6: take as a second stress gives the same five bores | same five | LB04 8.65, LB05 9.35, LB07 8.38, LB10 8.29, LB12 4.55; LB16 2.41; complainants 0.23 to 1.57 | yes |
| Golden Method sheet: fit RMSE | LB04 0.22, LB10 0.29, LB16 0.13 m | continuous fit 0.027, 0.040, 0.036 m | no, the golden fits are coarse |
| In-house solver's KV-LB16 control route | 5.1, 5.5, 4.9, 4.8 m (LB04, 05, 07, 10) | 5.0, 5.5, 4.7, 4.7 m | route reproduced; refuted below |

## Competing answers that survived

**One fork survives, at figure precision only. It does not affect the call.**
- **The fork:** the "decline the mine has caused" column is asked to one decimal. The coarse-grid gamma fit the golden uses gives one set of values; a continuously optimised gamma, and the other legitimate fitting choices, give another. Examples: KV-LB04 8.9 against 8.7, KV-LB18 1.3 against 1.5, KV-LB12 4.6 against 4.4, KV-LB01 0.8 against 0.6.
- **Extent:** 11 of the 18 cells differ at one decimal, and 8 differ by more than 0.1 m.
- **Why nothing closes it:** MG-02 pins no estimation method. The design note's own GRID gives bands as wide as -0.8 to 1.1 m for the alluvial bores and 6.9 to 9.3 m for KV-LB04, so the column is not pinned at 0.1 m by construction.
- **The repair:** a stated acceptance band in the solution blocks, not a prompt change.

**Rivals on the main call. All are defeated by shipped facts.**

1. **Decline since baseline.** It names KV-LB01, 02, 03, 06, 08, 09, 12 and 18 and misses the coal measures. Closed by MG-02 4.1: "a decline with another cause is not the mine's".
2. **Decline less the same-aquifer reference bore's fall.** It names KV-LB12 alone. Closed because the register's network sheet puts no reference bore in the coal measures. The alluvial and basalt references fell 4 to 5 m while the coal measures were rising about 0.7 m a year into mid-2022.
3. **KV-LB16 as an unaffected coal-measures control (the in-house solver's reading).** It names KV-LB04, LB05 and LB12, so two agreements. It is closed by the bundle, in five ways:
   - **Its own record shows the drawdown.** KV-LB16's pre-take response (97 static dips, R2 0.998, RMSE 0.036 m) runs to 212.22 m AHD for September 2026 against 209.84 observed.
   - **The timing fits drawdown spreading outward.** The departure is nil through 2022Q4 and then grows steadily: 0.12 m in 2023Q2, 0.54 in 2024Q1, 1.32 in 2025Q1, 2.34 in 2026Q3. The near bores were already 0.24 to 0.60 m down by 2022Q4.
   - **Two other tests agree.** The full-record take term gives 2.41 m at KV-LB16. A fit calibrated only to June 2019 validates on July 2019 to June 2022 with a bias of -0.05 m and still gives 2.31 m.
   - **No shipped fact makes it a control.** It is a register bore inside MG-02 1.2, in the aquifer being dewatered, 12.4 km from the pit. The network notes reserve "outside the EIS predicted drawdown" for RF01 to RF03 alone.
   - **On its own terms the route is fragile.** It leaves KV-LB04 at 5.0 m against a 5 m trigger. Its regressions (R2 0.93 for LB07 on LB16) are weaker than every bore's own climate fit.
4. **"The rainfall file cannot reproduce the hydrographs."** This is a fitting failure, not a gap in the data:
   - An exponential response reaches R2 0.21 to 0.73 on the coal measures, and rain lagged 0 to 23 months reaches 0.19 to 0.23.
   - My own first optimiser pass, started on shapes up to 2.5, fell into the same local minimum for KV-LB10 and KV-LB16 (R2 0.23 and 0.42).
   - Once the starting grid reaches shape 16, the fit is R2 0.998 or better.
5. **Cap "the decline caused by the mine" at the observed fall since baseline.** It names KV-LB12 alone. This is a weak semantic fork:
   - MG-02 4.1 attributes the decline among its causes.
   - The prompt asks for the change since baseline and the mine-caused decline as separate columns.
   - Read additively, the climate raised the coal measures about 6.3 m and the take lowered them about 8.7 m.
   - The golden note already defines the share as the gap to the climate-only level.

   Watch it, but it is not equally licensed.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 11 | yes |
| Distinct formats | 3 or more | 5 (pdf, csv, xlsx, parquet, md) | yes |
| Largest row count | 25,000 or more, or a large database | `logger_pressure_2015-2026.parquet` 994,869 rows (barometric CSV 99,959) | yes |
| Distractors named in metadata.json, none labelled in the pack | 2 or more, unlabelled | `landholder_contact_log_2026.xlsx`, `groundwater_quality_2012-2026.csv`; the network notes list both plainly | yes |
| Distractors unused but relevant | same world, has to be weighed | both cover the same bores and the same complaints; the solution uses neither; coal-measure EC rose 44 to 279 uS/cm after the take but ranks nothing | yes |
| A distractor that answers the decision reproduces and is ruled out | when applicable | neither answers the decision or a graded figure | n/a |
| Deliverable count | 1 to 3 | 2 (xlsx, docx) | yes |
| Multi-dimensional asks | not stacked lookups | an 18-bore by 4-figure grid, plus offers, count and four complainant explanations | yes |
| Golden deliverables present | every one named | `golden/bore_impact_assessment.xlsx`, `golden/make_good_recommendation.docx`; their figures match submission.md | yes |
| Units and rounding stated | every figure | level "metres AHD to two decimals"; the change ("two decimals") and the decline ("one decimal") take metres from the same clause | yes (weakest point, see finding 6) |
| Prompt shape and the 25-criteria floor | shape identifiable, 25 or more | shape 11 (before and after with a control); 72 grid cells plus the docx asks | yes |
| Prompt length | under 1,000 characters | 901 | yes |
| Realism, pack and goldens | nothing LLM-generated | pack reads as system exports, field sheets and a controlled procedure; the memo and workbook read as work products; no em dashes, no authoring language (the one "generat" hit is "generator service") | yes, with a wording item in finding 3 |

## Gate G reconciliation

**Gate G matches across all three sources.**

| Field | Judge | Design note | Card |
|---|---|---|---|
| mechanism | decomposition_attribution | decomposition_attribution, method selection (G16) carrying it | gate_g and stump_strategy: decomposition_attribution |
| stumping_family | analytical_non_defect | analytical_non_defect | n/a |
| surface_read_dependency | no | no | n/a |
| sole_data_defect | no | no | n/a |

**Gate H matches on all three rules.** domain pass, layers pass, decisive_step analytical. The card's `stump_class` is analytical, and its `domain_test` (climate-against-pumping attribution with calibrated response functions) is the same analysis the judge named.

**What the match implies.** The build reads as the same shape from inside and outside, so there is no send-back predictor here.

**The one gap is in the easy-route inventory.**
- **What is registered:** the design note's ladder (complaints, baseline, reference subtraction, straight-line trend, a single rainfall window, own response) and the card's `analyst_test` cover the baseline and reference routes.
- **What is missing:** the KV-LB16 control route. The in-house solver took it and the judge found it independently, so the outside sees one wrong route the inside never registered.
- **Why it matters:** the ladder's assertion that every bore sits at least 25 per cent of its trigger away at every rung does not cover this route. On it, KV-LB04 sits at 5.0 to 5.1 m against 5 m.

The data kill the route, so determinism holds, but the rung is unasserted.

**Distractor check.** The judge did not name either declared distractor as the surface read carrying the task.

## Stump power (Gate F)

**Strong.** Each easy route produces a specific wrong committed answer:
- the decline since baseline: eight bores, coal measures missed;
- reference subtraction: KV-LB12 alone;
- a short-memory climate fit, which fails on the coal measures and pushes the solver into reference subtraction or a control bore;
- the KV-LB16 control: KV-LB04, LB05 and LB12, two agreements.

The trap that does the work is the coal measures' 6 to 7 year rainfall memory. It kept them rising on the 2019 to 2021 wet seasons after the take began, so a net fall of 2.2 to 2.5 m hides 8 to 9 m of drawdown. The in-house round is consistent with this: the solver took the control route and missed the call.

**Too-easy signals.** None decisive. The network notes hand out the Layer 1 corrections (feet, barometric compensation, Queensland days), but none of those is the stump. The prompt's MG-02 4.1 sentence pins the estimand without hinting at the method.

**Wrong-reason risk.** It sits only in the asks. The one-decimal attributed-decline cells lie inside fitting noise, so graded at face value they turn into a lottery even for a solver on the right method.

## Findings, ranked

1. **The attributed-decline figures do not reproduce at one decimal (SOLUTION_WRONG, FIX_NOW).**
   - **Cause:** the golden fits come off a coarse grid. The Method sheet gives KV-LB04 shape 12 and RMSE 0.22 m, and KV-LB10 RMSE 0.29 m. A continuous fit of the same model reaches 0.027 and 0.040 m.
   - **Effect:** a reviewer who recomputes gets different values in 11 of 18 cells. Those cells are LB01, 02, 03, 04, 06, 08, 09, 10, 12, 13 and 18 in the ledger, and the same values appear in CC2, CC3, step 5 and the Final Recommendation's ranges.
   - **Fix, part one:** refit with a continuous optimiser (or a much finer shape and time grid), then restate the figures in:
     - `submission.md`: Final Recommendation, CC2, CC3, step 5 and Deliverable Answers;
     - the golden workbook: column M of the Assessment sheet and the Method sheet's fit table;
     - the docx: the offers table and the four complainant sentences.
   - **Fix, part two:** give every attributed-decline cell an acceptance band in the Deliverable Answers, so the generated criteria grade the method rather than the optimiser. A band of ±0.3 m covers my variant spread and the gap between the golden and the best fit. KV-LB06 needs about ±0.4 m, because its two-stress estimate is 0.23 m.
   - The call, the yes/no column and the offers do not move. The prompt and the bundle stay as they are.
2. **Register the KV-LB16 control rung (design note and checks only, no pack change).** Add it to the ladder and to the card's `analyst_test` as the route the solver took. Assert KV-LB16's own-response departure in `checks.py` (about 2.4 m at September 2026, nil before 2023), so a regeneration cannot quietly weaken the evidence that kills the rung. Record its knife-edge at KV-LB04 (5.0 to 5.1 m) as a known coin-flip for solvers on that route.
3. **The golden note asserts geology that is not in the pack (FIX_NOW wording).**
   - "Answer rain at the outcrop" and "the alluvium over the coal-measure subcrop east of the pit": neither "outcrop" nor "subcrop" appears in any shipped file. Restate them as what the pack supports, for example "the coal measures answer rain over six years or more" and "the creek bore, about 2.6 km from the pit".
   - "Reference bores 20 to 30 km from the mine": KV-RF02 is about 31.7 km from the perimeter bores' centroid, so say 25 to 32 km.
4. **Accept ±0.01 m on the change column.** For KV-LB04, LB05 and LB15, taking a logged bore's baseline from the logger's daily mean instead of the register's recorded baseline gives -2.45, -2.48 and -3.03 m. The register is the recorded baseline assessment (MG-02 5.1), so the golden figures stand. The tolerance just stops a cent-level reading choice from costing a cell.
5. **The card is stale against the shipped build (bookkeeping).**
   - Spine: `bore_water_levels_2008-2026.csv` with 0 rows is not a shipped file.
   - `driver_concrete` says the alluvium fell 2 to 4 m, the coal measures were held 5 to 8 m below and fell under a metre net. Shipped: 4.6 to 5.2 m, 8.2 to 9.3 m and 2.2 to 2.5 m.
   - Layer 1 lists "pre-2012 readings in feet" (shipped: 2012 to 2014) and "logger drift corrected" (the pack has no drift).

   `guard.py` compares cards across builds, so the card should carry the shipped spine and numbers. This does not touch the verdict.
6. **Unit wording (no change now).** The change and the decline take "metres" from the level clause. That passes, but it is the weakest unit statement in the prompt. Changing it now would change what solvers saw, so leave it.

## Next action for the author

Re-run the per-bore climate fits with a continuous optimiser, then restate the 18 attributed-decline figures, with an acceptance band on each, in `submission.md`, `golden/bore_impact_assessment.xlsx` and `golden/make_good_recommendation.docx`. Re-judge once after that.

The fix moves graded golden figures but nothing solvers see. The judge needs no rerun; whether a fresh round is needed first is for the pipeline's FIX_NOW rule to decide.
