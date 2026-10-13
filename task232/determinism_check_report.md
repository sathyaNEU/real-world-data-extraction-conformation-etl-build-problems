# determinism-check report, task232, 2026-10-13 (pass 2, re-judge after the secondary-case definition was filed)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection / decomposition, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One sonnet thread (scratch /tmp/determinism-check-task232-r2/, fresh unzip, 18 files, target.zip sha256 f97b0bc1...d9c6) executed the prompt and CD-ST-07 / GL-CD-11 literally and reproduced every committed figure from the bundle. CD-ST-07 sections 2 to 4 pin basis period, notifications, counterfactual call, booked-session exposure, division by three, the 1.00 rule and rounding. Every setting has a wide margin to 1.00 (Kestrel 0.74 vs 1.25, Larkspur 0.69 vs 1.29, Halden 0.81 vs 3.54). The pass 1 fork (what is a secondary case) is now closed by the filed GL-CD-11 section 2 definition (acquired from the index) plus its incubation table; the thread judged the golden forced. The alternative (all 319 follow-up cases) gives 2/2/8/2/1/24 hours and is not what the filed text yields.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Child-hours shig / STEC / crypto | 9,442.03 / 1,301.72 / 8,881.78 | 9442.033 / 1301.717 / 8881.783 | yes |
| Secondary cases | 75 / 4 / 62 (141 of 319) | 75 / 4 / 62 | yes |
| Rates per 1,000 child-hours | 7.94 / 3.07 / 6.98 | 7.943 / 3.073 / 6.981 | yes |
| Notifications in basis | 80 (13/22/22/11/10/2) | same | yes |
| Settings | 12/2/12/4/12/24 | same | yes |
| Expected cases at setting | .61/.69/.81/.74/.61/.15 | same at 2 dp | yes |
| Next longer | 1.33/1.29/3.54/1.25/1.57/none | 1.331/1.291/3.538/1.249/1.567/none | yes |
| Ask 2 reports | 2377/3884/2473/1041/1167/256 | identical (DR replay "^FACILITY" duplicates removed, NSW clock) | yes |
| Ask 2 >24h late | 12/22/19/8/11/4 | identical | yes |
| Ask 3 first to notify | 34/89/47/24/29/1 | identical (merges resolved) | yes |

## Competing answers that survived
None. Forks tested and closed: F1 secondary-case definition (closed by GL-CD-11 s2 and s3; no onset on a window edge); F2 others headcount, attendance (stated "who attended") versus bookings gives same settings, different values (Halden 0.99 vs 0.81), attendance governs by the text; F3 21:00 and session-start edges change nothing; F4 report identity (data dictionary and release notes pin the golden); NSW clock pinned by data dictionary; rounding pinned by 4.1.
Residual risk noted by the judge: a reader who does not apply the incubation table to the filed definition. The definition is now filed, so this is a reading effort, not an open fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 5 (csv, xlsx, json, pdf, docx) | yes |
| Large file | 25,000 rows or more | message log 45,728; signin export 29,071 | yes |
| Distractors | 2 or more in metadata.json, none named by file name | 3 named (ncp_condition_codes_2025.csv, lab_turnaround_returns_2025-26.csv, ecec_services_register.csv); no file name labels one | yes, see finding 2 |
| Distractors relevant, unused, ruled out | answer a graded quantity yet shipped fact excludes | lab_turnaround (collection-to-authorisation) and ecec register unused and weigh; the judge also found the case extract's notifying_facility and release-notes weekly >24h summary as unused wrong-basis reads | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, xlsx), both in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | each states unit and rounding (two decimals; counts) | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape "other" (a dial per feed plus basis asks); about 18 setting/rate cells plus 6x3 count cells, well over 25 gradable figures | yes (rubric not generated here) |
| Not LLM generated, goldens real | | judge found no authoring language; three real-looking export layouts; docx core date precedes its approval line (harmless) | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection / decomposition; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Design note: `decomposition_attribution`, stump = attribute room cases to the index through the incubation range, not every follow-up case, nor every case after onset, nor only those before the exclusion; nothing planted; the note's default path (cases ill after the index) is a processing choice, not a shipped ranking. Match. The thread found no shipped artifact that ranks the feeds or names a setting; the declared distractors are not the surface read carrying the task. The difficulty survives deleting every wrong number. Gate G: PASS.

## Gate H reconciliation
Thread: domain pass | layers pass | decisive_step analytical (borderline toward rule_application). Design note: domain test (secondary attack rate per child-hour by incubation window, a surveillance measure), Layer 1 (three attendance layouts, clocks, DR replays, merges, code sets), Layer 2 decomposition_attribution, decisive step analytical. Match on all three. The thread's caution stands: CD-ST-07 states most of the procedure, and a reviewer who treats the GL-CD-11 table as a stated filter could read the decisive step as rule application. The note's defence is that the standard and guideline define a secondary case by what it is (acquired from the index), not by how to find one.

## Stump power (Gate F)
Good. Counting all 319 follow-up cases sets 2/2/8/2/1/24 (five of six feeds wrong); counting cases after the index sets 12/1/4/2/12/24 (three wrong); only pre-exclusion cases sets all at 24. The asks carry independent Layer 1 traps (DR replay duplicates inflate Ask 2 by 4 to 30 per feed; merged cases and unit-entered cases in Ask 3; NSW clock). A fully careful solver reproduces everything, so the stump rests on the attribution step and the duplicates.

## Findings, ranked
1. Residual rule-application risk on the decisive step (thread caution and Gate H borderline). Do not add the onset filter to CD-ST-07; that would convert the step into a stated rule.
2. metadata.json lists ncp_condition_codes_2025.csv as a distractor, but the thread used the old/new condition codes to select the three enteric conditions for Ask 3 (and the design note calls the 2025 code-set update Layer 1). If the codes file is needed for Ask 3 it is not "unused by the solution"; either replace it in `distractor_files` or confirm the mapping is derivable without it. The spec gate still passes on the other two.
3. Pass 2 cross-batch comparison was not assessed by the thread.
4. Minor: CD-ST-07 docx core.xml creation date precedes its approval line.

## Next action for the author
Check finding 2 (is ncp_condition_codes_2025.csv used by the solution?) and correct `distractor_files` in metadata.json if it is; otherwise no change, and the build can proceed to ship.
