# determinism-check report, task476 (architecture 3), pass 2, 2026-11-04

## Verdict
NOT_DETERMINISTIC (competing_defensible_answer). The golden reproduces in full; the method for the 11 unmetered wells is not forced.
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle: target.zip sha256 80bcc4b90d89a30ac623be605d548423d0410d71d7aa309d4a4e02eab9699545. Judge thread: one pass, verdict at /tmp/determinism-check-task476-v3p2-74942/verdict.md. The thread had no sight of pass 1.

## Why
Notice section 3 says only that an unmetered well "reports the volume it pumped, calculated from the well's own records". Neither the prompt nor the notice says whether energy converts at the test's headline kWh/AF or at each interval's lift. Both are standard, and they give opposite calls.

| Method | Ranch total (AF) | vs 15,358.9 | Call |
|---|---|---|---|
| Head-adjusted per interval (golden) | 15,583 | 224 over | buy 250 |
| Test kWh/AF held constant | about 15,020 | 339 inside | no purchase |
| Run hours times tested flow | about 14,719 by the author's count (about 15,033 by kWh over test kW) | inside | no purchase |

The affected answers are the main call, the memo's total ask and the calculated wells' volumes.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Water available | 15,358.9 | 14,878.9 + 480 (notice sections 2 and 3) | yes |
| Metered W-01 / W-02 / W-03 / W-04 | 824 / 864 / 838 / 744 (total 3,270) | 823.96 / 864.45 / 837.8 / 744.06 | yes (rollover and exchange handled) |
| Unmetered W-05 to W-15 | 12,313 | 12,315.7 | yes, within rounding |
| Ranch | 15,583, 224 over | 15,586, 224 to 227 over | yes |
| Purchase | 250 | a total of 15,558.9 to 15,608.9 buys 250; the golden sits 24 AF above the lower bound | yes within the head method |
| Energy charges, 15 wells | as listed | all within 0.5 USD | yes |
| Static depths, 30 values | as listed | all reproduce | yes |
| Constant kWh/AF | 15,020 (author) | 15,020 | yes, and it is the competing answer |

## Competing answers that survived
- **Fork: energy to volume for the unmetered wells.** Constant test kWh/AF gives 15,020 and no purchase. Head-adjusted gives 15,583 and 250. The shipped rule meant to close it is SF16 and the reports' TDH definitions, but those only fix the head's reference once the head-adjusted method is chosen. They do not choose the method.
- **No other text-only competitor survived.**

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 41 per the judge; my own listing counted 45 entries, either way well over 10 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 or more rows | the logger files have 40,905 rows each; the 15-minute utility export has 308,220 | yes |
| Distractors | two or more, named in metadata.json, none labelled in a file name | the Alkali Slough deliveries (surface water) and the weather file. They are named in metadata.json and their file names do not label them. Both are unused by the solution and ruled out by shipped fact | yes |
| Deliverables | 1 to 3, all in the golden | 2: the return CSV and the memo docx. Both are present in `golden/` | yes |
| Asks | multi-dimensional, with unit and rounding stated | per-well volume and method, 12 monthly volumes, 30 depths, 15 charges. The prompt gives units and rounding | yes |
| Prompt shape and 25 or more criteria | identifiable | the shape is a conformation return plus a purchase memo. The count is generated and cannot be verified from the bundle; the graded cells number well over 25 | yes (not independently verifiable) |
| Not LLM-generated; goldens read as real work products | | The judge found the files read as real operational artifacts and found no disclosures. I did not re-read the goldens | yes (judge) |

## Gate G reconciliation
The thread's mechanism is method_or_model_selection, with stumping_family analytical_non_defect, surface_read_dependency no and sole_data_defect no. The card and the design note agree with that diagnosis: `stump_class: analytical`, and the note's decisive step is converting each interval at its own head. The thread names no shipped surface read that carries the task, so the declared distractors (surface-water deliveries and weather) are not too load-bearing. Gate G passes: no shipped artifact ranks the call and gets it wrong.

The mismatch is on determinism, not on the stump. The note's stump sentence and its `## Three rules` line both state that "no rule says how energy becomes water" and that the enumerated family spreads 0 to 450 AF of purchase. The note itself therefore records the open fork, and says the fork is the decisive step. Under the current spec the method may stay open only where the data separate the candidates. Here the metered wells do not: their recorded fit is head 1.16 / 1.81 / 0.97 against constant 1.28 / 1.77 / 1.06 monthly RMSE. Constant fits the meters slightly better (annual bias +0.7 percent against +1.1 percent), and the note's own default path says the meters "confirm" the constant method within 1.5 percent.

## Gate H line
- **domain:** pass. The deciding quantity is a pumping-plant energy-to-extraction estimate at operating lift, which is what the field estimates.
- **layers:** pass. Layer 1 is two utility export layouts, local time against UTC, a logger swap, meter rollovers and an exchange, and two report layouts. Layer 2 is the lift-dependent conversion.
- **decisive_step:** analytical, but only while the method stays unfiled and the data cannot adjudicate it. As shipped, that makes it a defensible alternative and not a valid stump. Filing the head adjustment would turn it into rule application.

## Stump power (Gate F)
The stump power is high. The test-rate route lands "no purchase", and many strong solvers would take it. But that route is defensible under a literal reading, so the stumping is not valid as shipped. The golden's 24 AF margin above the purchase window's lower bound is also thin, which matters for any redesign.

## Findings, ranked
1. **Main call not forced (blocking).** Constant test kWh/AF is a literal-reading answer and files no purchase.
2. **No shipped data separates the methods.** The four metered wells are all upper aquifer with small swings. No deep well is metered.
3. **The BHS reports lack the Gutierrez caveat.** Only the Gutierrez reports say "results are for the conditions measured on the test date". The eight BHS reports do not (parity issue, minor).
4. **The purchase-window margin is thin.** The golden sits 24 AF above the lower bound of the 250 window.

## Answers to the coordinator

**1. Does anything shipped force the head-adjusted conversion?** No. The thread is right that a literal reader may defensibly hold the test's kWh/AF constant.
- The BHS and Gutierrez definitions (kWh/AF = 1.0241 x TDH / OPE, with TDH built from PWL) tell the reader how the test-day figure was derived. That is a statement about the test day, and nothing makes it a rule for other days.
- The Gutierrez line "results are for the conditions measured on the test date" cuts both ways. A solver can read it as a warning, but it never says to re-derive at other conditions, and the BHS reports do not carry it.
- The loggers' pumping levels show that the head moved. They do not say that energy converts at the moved head. Constant kWh/AF is the field's common shortcut, and the metered wells agree with it within 1.5 percent.
- The design note's fork table does not close this. SF16 closes only the reference (pumping level, not standing level) once the interval-head method is chosen. The note's own `## Three rules` and readability row R2 call the step "silent" in every filed sentence. A rule that is silent cannot force a literal reader, and the note confirms the fork is the stump.

**2. Would a metered deep well with a large lift swing, or a dated multi-condition test series for one deep well, make the data separate the methods?**
- **Metered deep well (preferred).** Yes, it can separate them with margin and without naming the method. A deep well whose meter is read monthly, with pumping from spring to fall, is off by 4 to 6 percent under constant kWh/AF while the head-adjusted conversion tracks the meter. A solver who back-tests both on that well sees which fits. That is a recognisable organ: a filed back-test with the data picking the method.
  - It does open a third candidate: an empirical kWh/AF read off that meter and applied to the other deep wells. Applied as a single annual ratio it would approximate the head method, because all deep wells share the same seasonal pumping and swing. But its error across 11 wells of different efficiency could be 1 percent or more of about 12,300 AF, which is far more than the 24 AF margin. That could produce 200, 250 or 300 and recreate the fork.
  - The design has to be checked in `checks.py` before it ships. The meter must cover the same seasons and a similar pump class as the unmetered wells, and the margin has to widen so that a calibrated-ratio route and the head route land in the same block. Metering also moves every graded total, so the rebuild is a full one.
- **Dated multi-condition test series for one deep well.** It shows kWh/AF moving with PWL on dated tests, so the dependence is visible without a sentence. It separates the methods only weakly, because it gives a few points and no test of the year's volume, and the solver still has to decide to use the relationship. It opens no empirical-meter candidate, but a solver could interpolate by date or fit kWh/AF on PWL, which are further candidates. It also edges toward the filed relationship, which pulls the step toward rule application. This is the second choice.
- Either way, the Gutierrez caveat must be on every report for parity.

## Next action for the author
Re-root the separating evidence in the data: meter one or two lower-aquifer wells that have large lift swings (monthly reads, rollovers kept), regenerate, and assert in `checks.py` that head-adjusted fits those meters materially better than constant and that an empirical-ratio route lands in the same 50 AF block. Do not file the head adjustment in the notice, because that makes the decisive step rule application. Then rerun the free gates and the judge.
