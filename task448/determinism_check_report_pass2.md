# determinism-check report, task448, 2026-10-12 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (coverage calibration of a partial extract against a reference census, then scaling), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline), sole_data_defect: yes (borderline)

## Why
One isolated sonnet thread (medium) saw only a fresh unzip and the graded blocks. Venridge captures 97% of reporters' mortgages recorded with the deed and 60% of those recorded after it. Group capture applied to Weyrauch (154) and Mennwell (121) gives 258 and 203, so 260 and 200. The raw-row and pooled-90% routes put Shunga fifth, and counting Heidebrecht's 43 quitclaim-to-trust rows (guidelines 7.3, 7.4) is excluded by a shipped rule. The pass-1 county-basis fork is closed: the dictionary files HMDA's county as the institution's geocode and the vendor guide the recording county as where the property lies, and guidelines 2.2 count a home where it stands.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Reporters: Corvane / Halverd / Arkhaven / Shunga / Tessaline / Saltfork / Ninnescah | 311 / 228 / 182 / 151 / 141 / 138 / 133 | same | Yes |
| Venridge rows: Weyrauch / Mennwell / Heidebrecht / Kessinger / Eisenbrandt | 154 / 121 / 82 / 80 / 47 | same | Yes |
| Capture with deed | 1,673 / 1,731 = 97% | 96.6% | Yes |
| Capture after deed | 236 / 395 = 60% | 59.7% | Yes |
| Weyrauch / Mennwell | 260 / 200 | 257.8 / 202.5 | Yes |
| County, 2024-25 | 1,360 / 580 / 360 / 270 / 440 | 1,359 / 578 / 362 / 270 / 442 | Yes |
| County, program year | 710 / 310 / 190 / 150 / 240, total 1,610 | 711 / 311 / 192 / 152 / 242, total 1,607.6 | Yes |

## Competing answers that survived
No fork flips the five or the order. Residual minor forks, each closed by inference or by the prompt's "round every count":
- Program-year total 1,610 (rounded once) against 1,600 (sum of rounded rows): the literal "round every count" gives 1,610; the golden states it; the prompt does not pin it.
- HMDA county_code taken directly (1,410 / 590 / 350 / 250 / 410): closed by the dictionary's geocode wording, guidelines 2.2 and the vendor guide.
- 60 business-purpose HMDA loans kept (guidelines: "whatever the buyer's plans"); dropping them would move Corvane to 300 and Halverd to 220, order unchanged.
- Farmstead second-county record (street-address row kept, land-only row dropped) and shared-deed smaller mortgage as a second lien: inferred, not stated; HMDA agrees for Arkhaven (185 raw against 182).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | Yes |
| Formats | 3 or more | 4 (csv, txt, pdf, xlsx) | Yes |
| Large file | 25,000 rows or more | hmda_lar_kansas_2024_2025.csv, 62,167 rows | Yes |
| Distractors | 2 or more, in metadata, not in file names | hmda_2023_county_summary_ks.csv, homebuyer_education_completions_2024_2026.csv; names do not label them | Yes |
| Distractor behaviour | unused, relevant, ruled out by a shipped fact | not load-bearing (design note: deletion moves nothing, asserted); the judge did not name either as the surface read | Yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | Yes |
| Asks | multi-dimensional, unit and rounding stated | county by period cuts; every ask says "round to the nearest 10" | Yes |
| Prompt shape and rubric 25 or more | identifiable | shape 01 ranked list under a cap; the criterion count was not recounted this pass (rubric is generated, precut passed 49 checks) | Yes, shape; count taken from precut |
| Not LLM-generated, realistic goldens | | judge found no authoring leakage; golden-realism ran at build | Yes |

## Gate G reconciliation
Thread: method_or_model_selection family reading as analytical_non_defect, borderline on sole_data_defect (the recorder file is honestly partial; the undercount is the object the method estimates, not a planted defect). Design note and card declare stump_class analytical with the same borderline flagged in pass 1. Match. Decisive step is the route-stratified capture, not either declared distractor. No finding.
Gate G classification: analytical_non_defect (borderline), route to live testing for the call.
Gate H line: domain pass, layers pass, decisive_step analytical.

## Stump power (Gate F)
Good. Counting rows after alias mapping gives Corvane, Halverd, Arkhaven, Weyrauch, Shunga. Mennwell is missed unless the solver compares the file with HMDA by recording route; a pooled 90% capture or counting the quitclaim rows also gives a wrong fifth.

## Findings, ranked
1. None blocking.
2. Optional: prompt does not pin the total's rounding or that counties are where the home stands. A prompt edit would invalidate the frozen run, so not recommended.
3. sole_data_defect borderline: watch in portal results.

## Next action for the author
Proceed to stage 5 (ship): target.zip is already cut from the final rebuild; write the ledger row and commit SHIPPED (task448).
