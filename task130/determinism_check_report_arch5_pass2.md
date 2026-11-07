# determinism-check report, task130, pass 2, 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (method selection on honest data), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Cut judged: target.zip sha256 prefix 2109442a0e453806 (plan section 4 now files the day sheet as the date of the first return inspection; the final recommendation no longer prints 458 and 451). Scratch: /tmp/determinism-check-task130-20261031214533/ (verdict.md there). One thread, one pass.

## Why
The forecast 693.4 (700) exceeds the plan's 540 and reproduces from the bundle; asks 4, 5 and 6 reproduce in all 11 districts. The finding-1 pin worked: the judge now re-dates pre-16-Sep returns through the day sheet as the filed record (all 352 sheet entries consumed once) and no longer lists the date source as a fork. Rival reads (risk-only 437, permit-level 355, a 2019-start window about 522 to 525) all fall under 540 and are refuted by the data; every familiarity-keeping read is 626 to 712.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Schedule inspections | 5,512 | 5,512 | yes |
| First / second / third+ | 1,277 / 1,031 / 3,204 | same | yes |
| First-visit rates cat 1/2/3 | 14.4 / 28.2 / 32.4 | 14.37 / 28.17 / 32.39 | yes |
| Third+ rates | 2.9 / 4.8 / 8.4 | 2.94 / 4.83 / 8.39 | yes |
| Forecast | 693.4 (700) | 693.40 | yes |
| Category-only | about 437 | 437.3 | yes |
| Ask 4 (11 districts) | 10, 10, 9, 9, 11, 8.5, 10, 9, 9, 8.5, 13 | identical | yes |
| Ask 5 (11) | 71.9 ... 66.3 | identical | yes |
| Ask 6 (11) | 1,416 ... 2,424 | identical | yes |

## Competing answers that survived
No fork flips a call.
1. Ask 4 working-day convention: counting both ends adds 1.0 in every district (11.0 for District 1). The plan's "from X to the day of the first return" and the elapsed-days reading support the golden; unfiled but natural. Residual risk, minor.
2. Ask 6 free visit: if the free visit were the first inspected one, Districts 3, 8, 10 change (2,712; 3,960; 2,712); the fee schedule's "whether the inspection is made or the premises are found closed" supports the golden.
3. Visit classes: two classes give 626 to 639 (rounds to 600, still over 540); the third class is data-supported. Ask 2 at nearest-100 is sensitive to this.
4. Rate window from 2019 gives about 522 and flips the call; the 50 percent first-visit share in 2019 is a visible start-of-record artefact (judge treats it as the trap, not a fork).

## Spec gates
Unchanged from pass 1 (13 files, 4 formats, 30,164-row file, two distractors named in metadata.json and not in file names, two deliverables both in golden, prompt 846 characters with no data count, no em dashes in prompt.txt or submission.md, about 39 criteria per the design note). All pass. The judge's format tally (7 csv, 3 xlsx) differs from the file list (6 csv, 4 xlsx); immaterial. Distractor relevance and realism taken from the judge.

## Gate G reconciliation
Judge: forecasting, analytical_non_defect, surface_read no, sole_data_defect no; Gate H domain pass, layers pass, decisive_step analytical. Card: stump_class analytical with analyst_test and domain_test; design note decisive step and easy route (437 to 458, no add) agree. The judge lists the capacity report Summary, the invoices, the illness file and the closure data as unused relevant distractors and names none as the surface read. No mismatch.

## Stump power (Gate F)
Moderate to good per the judge. Plan s.3's "as the inspector named in Table 1" points to the inspector level, which softens the stump, but the solver must still rebuild pair history through the initials crosswalk, UTC conversion and 2019 censoring and find the first-visit effect. The cut by visit number is loud, so a strong solver who tries it lands the call; the main thread should weigh that against the ladder (pass-1 note stands).

## Findings, ranked
1. Ask 4 working-day inclusivity (unfiled, +1.0 in every district if both ends counted). Optional fix: file the count basis (the plan's "from X to the day of" already supports the golden); filing would need a rerun.
2. Nothing else. The pass-1 findings (day-sheet date source, unreproduced 458/451) are closed.

## Next action for the author
Ship on this cut; optionally pin the working-day basis in the plan text, with a rerun of the judge if you do.
