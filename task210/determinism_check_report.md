# determinism-check report, task210, 2026-11-04

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, sonnet, medium, over a fresh unzip at /tmp/determinism-check-task210-run1/target/ (target.zip sha256 7cec1223...b0f9). Verdict file: /tmp/determinism-check-task210-run1/verdict.md.

## Why
The main call is forced by the shipped files. Gallowfen PS (EPRWW4412BK, condition 2.3.1) delivers a median 48 l/s against a 72 l/s permit and spilled 12 times. Every other station delivers at least its permit; the closest is Sallowholme at 57 against 50. The delivered rate is the wet-well volume between the duty pump's control levels over the pump-on time plus the same volume over the pump-off time before it, taken per cycle and as a station median. The thread checked it against the three rising-main meters (117.7, 83.8 and 66.6 l/s against 117.8, 83.8 and 66.8 by cycles). The rated duty (Gallowfen 85.3 l/s, which gives "none breached") was rejected: it is a nameplate figure, not the flow the station "was passing forward". V/t_on alone was rejected (it flags many stations and misses the meters). Hagworth Wold (dry-day, groundwater-fed) and Marram End (57 spills) both pass forward above their permits.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Gallowfen permit (consents csv, 2.3.1) | 72 l/s | 72 | Yes |
| Gallowfen delivered (pump_event + assets.xlsx plan area and levels) | 48 l/s | 48.0 (V = 15.975 m3; 158 exact duplicate events dropped) | Yes |
| Other 13 stations' delivered | 41, 36, 19, 45, 57, 118, 29, 84, 32, 52, 22, 67, 43 | 41.0, 36.0, 19.0, 44.9, 56.9, 117.8, 29.0, 83.8, 32.0, 51.9, 22.0, 66.8, 42.9 | Yes |
| Meter cross-check at 3 metered stations | n/a | 117.7 / 83.8 / 66.6 against cycles 117.8 / 83.8 / 66.8 | Yes |
| Retired-serial mapping, 11 serials | one overflow each | Unique; 70 to 100 percent of starts within 3 minutes; runner-up far lower; one-to-one inside the install-week batches | Yes |
| Spills, 14 overflows (12/24, serials pooled) | 17,12,26,57,16,15,14,14,13,17,10,21,12,12 | all 14 match | Yes (see fork 1) |
| Hours of discharge, 14 | 32.0 ... 15.7 (as filed) | all 14 match, none near a rounding boundary | Yes |
| Monitored percentage, 14 | 99.9 ... 99.8 (as filed) | all 14 match (daily maximum over 8,760 h) | Yes (see fork 2) |
| Monthly SVG cells | filed | Not checked cell by cell (golden withheld from the thread); Marram End total 198.2 h reproduced | Partly |

## Competing answers that survived
No fork touches the main call. Three minor forks, all on the return lines or chart, none open on the call.

1. **12/24 block membership (Marram End 57 or 54).** PR-014 section 3: "Any discharge in each following 24-hour block counts as one further spill". Literal reading: a block counts while a discharge is active in it, which gives 57. Reading "only when it starts there" gives 54. **Open in the text, confined to one supplementary cell**: the spills column of the Marram End line (A1). The other 13 overflows are unchanged. The design note's fork table has no row for this term (SF11 covers pooling only), so the fork is unrecorded. The call is untouched (Marram End passes forward above its permit either way).
2. **Monitored percentage (daily maximum or mean across monitors).** Not open in my read: section 5 asks for the hours "during which its discharges were being monitored", and an average of overlapping monitors does not measure that. The thread treats the maximum as forced. If a solver averaged, 11 of 14 A3 cells (the replaced overflows) move by 0.1. Confined to A3; design note SF13 records the cap and sum readings but not the mean.
3. **Unlabelled clock in the discharge log.** Closed by data, not text: against the UTC alarms the log sits at 0 h offset in winter and 1 h in summer, so it is UK local. A solver who read it as UTC would also misplace the monitors in the retired-serial matching. Moves only month-boundary cells of the chart (A4) directly. The design note's SF21 claims every cell is the same under UTC months at one decimal, which the thread's finding contradicts for boundary cells; worth a re-check, but it is an ask-only effect.

**Would a closure in the shipped procedure state an ask device in plain words?** The thread's suggestion (a sentence in the golden or submission notes) would not reach a solver, so the only closure that counts is in the shipped files (PR-014).
- Fork 1: a sentence in section 3 saying a block counts when any part of a discharge falls in it is a definition of the count. It does not state the serial mapping, the pooling or the clock. It is safe to add, and I recommend it (optional, not needed for approval). It also sits beside section 4's existing "any period of discharge counted once".
- Fork 2: a sentence such as "an hour is counted once however many monitors reported it" would state in plain words the pooling hazard (D1, the overlapping handover units). Leave open; the thread closed it on the existing section 5 text.
- Fork 3: "the platform records in UK local time" would state D8 (clock conversion) outright. Leave open; the data close it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | Yes |
| Formats | 3 or more | csv, sqlite, xlsx, pdf (4) | Yes |
| Large file | 25,000 rows or large database | pump_event 460,344; wet_well_level 489,818; meters and rainfall csv large; 40 MB sqlite | Yes |
| Distractors | 2 or more in metadata.json, none named in a file name | 4: radar rainfall, Hagworth borehole, improvement plan, work orders; file names are neutral | Yes |
| Distractors unused yet weighable | relevant, ruled out by a shipped fact | rainfall and borehole drive the Hagworth dry-day wrong answer, ruled out by its 36 against 31 l/s; plan and work orders rank nothing on the condition | Yes |
| Deliverables | 1 to 3, all in the golden, no format family | 3 (docx, csv, svg); all three present in golden/ | Yes |
| Asks | multi-dimensional, unit and rounding stated | 14-overflow return lines (spills, hours, percentage, flows) and a 14 by 12 chart; prompt states whole l/s and one decimal. Spill counts are counts | Yes |
| Prompt shape and 25 criteria | identifiable; 25 or more | shape 10; about 140 gradable figures (98 ask figures plus 42 scorecard cells) | Yes |
| Reads as real work product | nothing LLM-generated | thread found no authoring tells, no README, no temporal contradiction (monitor list dated 2027-01-15) | Yes (realism not re-judged by me) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, layer2_family field_method, gate_g binding_constraint, stump_strategy binding_constraint, decisive_rule_filed false, official_decoy false. These agree. The surface read the thread names is the register's rated duty, which is the design note's rung 0, not a declared distractor. The four declared distractors do not carry the call, so none is too load-bearing; the only distractor-driven wrong answer is Hagworth Wold on the dry-day screen, and the design note already expects it.

**Gate H line (thread):** domain pass, layers pass, decisive_step analytical. The design note's Three rules agree (Layer 2 field_method: delivered rate from wet-well fill and draw against the nameplate; No decoy, Not semantics, Not rule application present). No mismatch.

## Stump power (Gate F)
Thread: moderate to good. The easy routes are the rated duty ("none breached") and V/t_on (a long wrong list).

**Reflex risk (builder's flag).** The thread classed the step analytical and reached the golden by applying the recognised wet-well fill-and-draw timing. It did so with little judgment the data had to settle beyond one choice: read "was passing forward" as a measured flow instead of the nameplate, and cross-check against the meters. The files hold nothing that invites the method by name. The design note's pins confirm that no filed sentence names a delivered rate, cycle, drawdown, volume or meter. What nudges a careful reader is the phrasing in the prompt: "the flow the station was passing forward while it spilled" and "the flow its station passes forward beside the permit's". The register's `Duty flow` column (a nameplate, with mixed l/s and m3/h units) is the competing source, and the meters match the nameplate at their own three stations, so they rank nothing, as the design note says. The register also ships plan areas and control levels, the inputs the method needs. This is a landable call for a strong solver who treats "was passing forward" literally. The main thread should weigh it against the design note's ladder (stumping 1.3: textbook routes are what strong solvers take). The thread's own words ("the only one the files support") describe a route that, once chosen, is mechanical.

**Ceiling (builder's read).** The design note's ask sheet gives a pair ceiling of 55.4 (cracker 75.3 on the call, mirror 35.6 off it). The thread did not measure this. A solver who handles every device (retired-serial mapping, handover counted once, clock converted) keeps 98 of 98 ask figures; the cracker without the device keeps 55.1 percent of them (12 of 56 device figures). The ceiling is the design's own measurement, not the thread's.

## Findings, ranked
1. Reflex exposure on the decisive step: the field's textbook estimate lands the golden with little further judgment (see Stump power). Record, weigh on the ladder; not a determinism defect.
2. Fork 1 (57 or 54 for Marram End): open in the text and absent from the fork table. Optional one-sentence closure in PR-014 section 3.
3. Design note SF21 says UTC months give identical cells at one decimal; the thread found boundary-cell shifts. Re-check the claim in checks.py.
4. Forks 2 and 3: closed by data and existing text; do not close in the procedure, as that would state the ask devices.

## Next action for the author
Ship as is. Optionally add one definition sentence to PR-014 section 3 (a 24-hour block counts when any part of a discharge falls in it), add a fork-table row for it, and re-check SF21 against the thread's month-boundary note.
