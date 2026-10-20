# determinism-check report, task251, 2026-10-20

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (on determinism; see Stump power for the Gate F outcome that spends the architecture)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One thread (sonnet, medium) judged the full blocks from a fresh unzip at /tmp/determinism-check-task251-r1/target/ (verdict at /tmp/determinism-check-task251-r1/verdict.md). POCT-GLU-02 sections 5 to 7, the plan and holiday sheet, the register and the laboratory note (C600 / 1.035) force one list of 8 meters. The margin is wide (nearest listed R842P -7.44, nearest unlisted J313P +3.41). All four asks were reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pairings read / kept | 13,938 / 5,590 (98 to 149 per meter) | same | yes |
| Listed meters' error | A564E -8.2, J921X -7.9, K532W +8.4, P722J +8.4, R842P -7.4, S959P +8.3, W228Y -8.2, W234L +11.0 | -8.17, -7.87, +8.42, +8.35, -7.44, +8.30, -8.17, +11.00 | yes |
| Largest unlisted | J313P +3.4 | J313P 3.41, A268A 3.18, U982T -3.03 | yes |
| Ward / hospital of the 8 | as golden | Storico shows no move of the 8 | yes |
| Ask 2, hospital by quarter | CM 27.3/27.7/27.9/27.3; RB 39.7/43.3/42.7/44.0; VD 66.3/66.8/68.3/65.1 | identical (181,141 rows after dedupe; not on a rounding edge) | yes |
| Ask 3, tests by ward | 13 ward counts | all 13 identical | yes |
| Ask 4, chart | 52 errors vs band | per-meter errors reproduce | yes |

## Competing answers that survived
None closing a different list. Tested and closed by shipped text: all pairings since calibration (K532W out at +4.79, M707F in at -5.75; the intended trap, closed by the selection-on-outcome reading of section 6), no C600 correction (U982T enters; closed by section 7 and the note), export presidio instead of Storico (asks 2 wrong; closed by dictionary and Storico), no dedupe (asks wrong; visible via shared n_memoria). Window, holiday shift and calibration-day variants keep the same 8. Residual, low: no sentence literally says "exclude the confirmation pairings"; the thread rates it an analytical estimand choice, not a semantic fork. Thinnest inference: the one-hour meter-clock offset is in no shipped file and is inferred from data (minimum lag, summer and winter meter-to-draw gaps); it touches ask 2 only, not the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 5 (xlsx, pdf, csv, eml, md) | yes |
| Large file | 25,000 rows or more | GlyLink_risultati csv, 185,844 rows | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | strisce_consegnate_reparti_2027.xlsx, VEQ_glicemia_laboratorio_2027.xlsx; names carry no label | yes |
| Distractors weigh but are unused | unused by solution, relevant | VEQ (lab shows no bias; the C600 to C900 step rides on the note) and strisce are unused; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | list with ward, hospital, error; hospital x quarter; per ward counts; chart; per cent to one decimal, whole counts | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | shape "other"; design note counts 48 | yes |
| Reads as real | no LLM tells, goldens real work products | thread found none; dates coherent | yes (golden-realism owns the finer read) |

Minor: the design note's default path cites 14,133 pairings; the shipped file has 13,938, which is the figure in submission.md. Note only; no graded figure moves.

## Gate G reconciliation
Thread: mechanism statistical_rigor (selection bias in the pairings), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and note: strategy population_selection, Gate G signal_vs_noise_or_hold, Layer 2 field_method, pattern confirmation-pairs-selected-on-the-meter-reading, stump class analytical. These match. The declared distractors (strisce, VEQ) are not the surface read carrying the task, so they are not too load-bearing. The thread's wrong-list route (all pairings, K532W out, M707F in) is exactly the note's default path and ladder row, including the +4.8 and -5.8 figures. Gate H: thread domain pass, layers pass, decisive_step analytical; the note's Three rules give the same decisive step (estimating on the pairs the plan drew) and Layer 1 (re-sent rows, solar-time clocks, current assignment, analyzer change, holidays, ward moves). No mismatch. The note's "Not rule application" line (section 7 names no pairings) is the one the thread's residual risk probes; it holds because the exclusion rests on analysis, not on a filed rule.

## Stump power (Gate F)
Thread assessment: strong. The easy route files a wrong list and catching it needs the selection-on-outcome insight, unannounced; the asks add layers (Storico locations, dedupe, clock offset). Measured outcome at the same stage 4, supplied by the main session: scored reader A landed the call (planned pairings only), and both readers kept all 25 ask figures. Under the two-reader rule the architecture is spent whatever the determinism verdict. Weigh the thread's reading with this: the planned-versus-confirmation distinction is the textbook route for a strong solver (section 5 and 6 describe the two kinds side by side), so the call is landable, and the asks, though layered, were all reached. The determinism and Gate H results do not change that.

## Findings, ranked
1. Gate F measured: call landed by reader A, 25 of 25 ask figures kept by both readers. Architecture spent; stump power is the open problem, not determinism.
2. Low residual determinism risk: the confirmation-pairing exclusion is not literally filed (analytical by design; a filed fix would turn it into rule application, so do not file the HOW).
3. Thin inference: the one-hour meter-clock offset appears in no file; it is inferable from the data and confined to ask 2.
4. Minor note mismatch: 14,133 versus 13,938 pairings in the design note.

## Next action for the author
Treat determinism as cleared and do not touch the filed text; take the Gate F result (reader A landed the call, all 25 ask figures kept) to the re-root decision for the spent architecture, hardening the asks and the decisive step from the data's own structure rather than by filing a rule.
