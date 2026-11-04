# determinism-check report, task193, 2026-11-04

## Verdict
NOT_DETERMINISTIC (supplementary ask 4 only; the main recommendation and asks 1, 2, 3 and 5 reproduce and are forced). Taxonomy: answer_contradicts_files. No SOLUTION_WRONG.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (choice of background comparison group), stumping_family: analytical_non_defect (borderline, thread), surface_read_dependency: no, sole_data_defect: yes (applies to ask 4 only, not the main call; see reconciliation)

## Why
Ask 4 requests specific conductance "at 25 degrees Celsius". The golden obtains 7 of 11 values (MW-1, 2, 3, 4, 6, 7, 9) by dividing the logged value by 1 + 0.0191 x (T - 25), solely because meter R-4471 is treated as logging uncorrected conductivity. No shipped file says so. FS-03 section 4 only defines specific conductance, the column is named `spc_us_cm`, and no remark, register or header marks the meter as non-compensating. Read literally the column is already specific conductance, so the literal answers are the raw values (MW-1 409, MW-6 826, ...). The only evidence is an inference from R-4471 days reading about 30 percent below the April 21C0847 readings of the same wells. That is a hidden-fact answer, not analysis. MW-6 and MW-7 carry no serial on 8 October (carried forward from R-4471 by FS-03 section 3), which is supportable once the first fact is filed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MW-1 below PZ-1 events | 10 of 17 | 10 | yes (gauging CSV + survey sheet) |
| MW-2 below PZ-2 | 6 | 6 | yes |
| MW-3 below PZ-3 | never | never | yes |
| Background counts Cl / Na / B | 34 / 34 / 33 | 34 / 34 / 33 | yes (EDDs, both layouts) |
| UPL chloride | 38.2 mg/L | 38.229 | yes |
| UPL sodium | 20.8 mg/L | 20.823 | yes |
| UPL boron | 68.3 ug/L | 68.316 | yes |
| October results, 8 compliance wells x 3 | as filed | match | yes |
| Exceedances | MW-6, MW-7, MW-9 | same (MW-7 Na 1.13x, MW-9 B 1.16x) | yes |
| Purge volume, 11 wells | 1.7 to 4.3 gal | all 11 | yes (fieldlog CSV; no rounding-boundary hits) |
| Specific conductance, 11 wells | 584 ... 1096 | reproduces only with R-4471 correction; literal raw values differ for 7 | NO under literal reading |

## Competing answers that survived
1. Ask 4, seven R-4471 wells: raw logged value (literal) vs corrected to 25 C (golden). Closing rule: none shipped. Fix required.
2. Ask 2 limits and counts: sample-level exclusion (golden, 38.2 / 20.8 / 68.3, n 34/34/33; SAP section 4 "every routine sample of that groundwater") vs whole-event exclusion when any well reverses (n=21, limits 37.6 / 22.3 / 74.2). The call is the same, the graded numbers differ. The thread accepted the sample-level reading, so this is a residual risk, not a failure.
3. Main call: pooling gives 55.5 / 34.8 / 109 and MW-6 alone (the intended wrong route); MW-3 only adds MW-10 and MW-7 chloride; the data do not support it (MW-1 and MW-2 are clean outside reversal events). Closed by domain analysis from heads.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 5 (pdf x3, csv x3, txt, json, xlsx x2) | yes |
| Large file | 25,000 rows or more | Ridgeline txt 25,141 rows (about 3.5 MB) | yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | 3 named (gas probe csv, precipitation json, site inspections xlsx); names carry no label | yes |
| Distractors unused yet weighty | unused by solution, ruled out by a shipped fact | not used in any recomputation; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | each states both | limits three sig figs; SC whole, uS/cm at 25 C; gallons one decimal; per-well across 11 wells | yes (ask 4 determinacy fails, above) |
| Prompt shape and 25 criteria | identifiable, 25 or more | shape 10 scorecard (24 checks plus counts, call, asks); rubric is generated downstream, not verifiable here | yes on shape; count unverified |
| Prompt form | one paragraph, under 1,000 characters | 805 characters, question first, no count the data hold | yes |
| Not LLM-looking, goldens realistic | n/a | no authoring language, coherent dates; golden realism covered by its own gate | yes (not re-verified) |

## Gate G reconciliation
- Thread: mechanism statistical_rigor; stumping_family analytical_non_defect, borderline; surface_read_dependency no; sole_data_defect yes; Gate H: domain pass, layers pass, decisive_step analytical.
- Card: stump_class `analytical`; analyst_test names the same easy route (every background result, limits 55.5 / 34.8 / 109, MW-6 alone) and the same cause (reversal-event results from MW-1 and MW-2); domain_test is the hydraulic-head background judgment. Design note `## Three rules` (No decoy, Not semantics, Not rule application) is consistent with the thread's Gate H line. Mechanism, family and decisive step match. No mismatch on the main call.
- Declared distractors (gas probes, precipitation, inspections): the thread names none as the surface read. No finding.
- `sole_data_defect: yes` is a scope slip, not a main-call defect. The main-call stump is not a planted defect, decoy or hidden rule: the reversals appear only as ordinary water levels, nothing is flagged, and the filter is derived from heads. The only defect-like hidden fact is the R-4471 uncorrected logging, and that sits in ask 4, which is free of rule 3 by design (design note device D3, "a label before a silent switch"). It is a finding only as the ask-4 determinism failure above. The thread's remark that the reversal structure is the whole difficulty restates the card's analyst_test and is the intended Layer 2, not a flag. Record the "analytical_non_defect, borderline" wording as a soft note: the portal could read the pumping-driven reversal as planted contamination, but nothing in the pack is planted.

## Stump power (Gate F)
Fair to high on the main call. A strong analyst who pools the background, or who does not compare heads with the boundary piezometers, files MW-6 alone and misses MW-7 and MW-9. MW-3-only is the other wrong route. Margins are thin but clean (1.13x and 1.16x; nearest non-flagged is MW-11 boron at 0.88 of its limit). The conductivity and purge asks add difficulty; ask 4 does so by a hidden fact, not by analysis. The decisive step is analytical (estimand and comparison group), not a standard-method landing.

## Findings, ranked
1. Ask 4 (answer_contradicts_files): R-4471's uncorrected logging is filed nowhere. Literal reading gives raw values for 7 of 11 wells. FIX_NOW.
2. Residual fork on ask 2: sample-level vs whole-event exclusion moves the graded limits and counts (not the call). SAP section 4 favours the golden reading. Close only if a sentence can be filed as WHAT (population) without filing HOW; otherwise leave.
3. Soft: thinnest link of the main call is that no file names PZ-1 to PZ-3 as boundary piezometers; the SAP calls them "water level points only". Thread accepted it as forced by domain analysis.

## Next action for the author
Add a shipped fact in the field log (a remark on R-4471's first set per day, or a meter register or header note) that R-4471 logs conductivity at sample temperature, uncorrected to 25 C, and that R-4468 corrects, keeping the serial no marker; rebuild twice for byte identity, re-run `figures_check.py` and `checks.py`, and have the golden for ask 4 re-asserted. Re-judge once (FIX_NOW). Leave the main call, limits and every other ask untouched.
