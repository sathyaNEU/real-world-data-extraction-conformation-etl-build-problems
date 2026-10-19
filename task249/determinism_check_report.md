# determinism-check report, task249, 2026-10-19

Pack: target.zip md5 3a097683ea6ff33166093c2ec837dbda. Scratch: /tmp/determinism-check-task249-r1/. The thread's verdict is /tmp/determinism-check-task249-r1/verdict.md. One pass, one thread (spawned by the main session, since this runtime has no Agent tool); no re-run.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The 15 / 13 partition is forced by the shipped files: MAL-IS-04 s.3.2 and s.3.3, Table 4.3 (conditional error for MAT-R and MAT-V) and the equivalence study's retest gain. The gap to the 15 per cent cap is wide: the lowest Extended account refers about 22.3 per cent (CHT) and the highest Standard account about 9.6 per cent (UJB). No tested variant moves an account across the line. Asks 2 to 4 reproduce exactly. The two minor forks (booking_ref against candidate linking, and non-register identities) are closed by the standard's s.2 and s.6.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Extended set (15) | KSP VRD ANV PRM SQR ABH MTL TJM SHY TRG PBH KVR RNJ CHT LVN | same 15, shares 22.3 to 32.8 per cent | yes |
| Standard set (13) | NVK UJB OJS IDP RNG EKD PGT AKR BHM KTV UDN VKT MDN | same 13, shares 3.4 to 9.6 per cent | yes |
| Retest gain fit | 0.04 + 0.31 exp(-d/19.5) | 0.0381 + 0.3107 exp(-d/19.53) | yes |
| Exposure over 12 per cent, weeks 3/10/17/24 July | 31 / 10 / 5 / 5 | 31 / 10 / 5 / 5 | yes |
| Items to rest | 41 | 41 | yes |
| Confirmed impersonations T1 to T4 | 5 / 62 / 273 / 244 | 5 / 62 / 273 / 244 | yes |
| Per thousand shortlisted T1 to T4 | 2.5 / 3.5 / 10.8 / 22.6 | 2.54 / 3.5 / 10.8 / 22.6 (denominators 1972 / 17743 / 25265 / 10791) | yes |
| Interrupted share, desktop / laptop / tablet | 1.64 / 4.74 / 9.33 per cent | same | yes |
| Finished on another device | 29 / 209 / 88 | 29 / 209 / 88 | yes |
| Top-tenth validation, shrinkage miss | "within a fiftieth of a logit" (CC3) | about 0.04 (naive route misses by 0.35) | partly (see Findings) |

## Competing answers that survived
None on the main call or the asks. Closed forks:
- Linking interruptions by `booking_ref` gives 1.57 / 3.78 / 8.92 per cent and 7 / 76 / 24. The standard's s.2 ("a candidate's one booking") and s.6 ("restart under the same booking") make candidate the unit.
- Counting the 6,400 identities outside the register moves laptop to 3.85 per cent. s.2 defines a candidate as a person in the register.
- Exposure counts using non-register identities would give 30 / 12 / 6 / 13. s.2 excludes them.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 in the bundle (metadata.json file_count 17; the judge's "18" is a miscount of the nested folder) | yes |
| Formats | 3 or more | 5 (md, pdf, csv, xlsx, parquet) | yes |
| Large file | 25,000 rows or more | mat_r_exposure_2028.parquet 1,949,365 rows; results_shared_2028.csv 453,733 rows | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | selection_venues_2029.csv and candidate_feedback_2028.csv, both with relevance and non-use stated; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx and pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | exposure by week, impersonation by tier, device interruption; rounding stated | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 10 (scorecard of 28 accounts plus three tables); the 28 account verdicts plus the ask figures give well over 25. The rubric itself is generated later and not inspected here. | yes (shape), unverified (count) |
| Reads as real work, not LLM generated | no signs | judge found no authoring or benchmark disclosure; dates coherent | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical. Its analyst_test (study rates move 0 accounts; dropping the gain or using the reported SE moves NVK, UJB, OJS; one MAT-R error frees KSP, VRD, ABH) matches the judge's reproductions of the wrong routes. Metadata names selection_venues and candidate_feedback as distractors; the thread did not cite either as carrying the task. Gate G classification: pass, no shipped artifact ranks the accounts wrongly beyond the study's own rates, which are correct for their unselected volunteers, and the difficulty survives deleting them. No mismatch found.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. This matches the design note's `## Three rules` (decisive step: building each account's genuine referral rate through its own pool with true-score regression, Table 4.3 error at ability and the retest gain).

## Stump power (Gate F)
Good. Four plausible shortcuts each give a specific wrong answer with a wide margin: observed MAT-R as truth (all 28 Standard), the study's rates (no account moves), no gain (NVK, OJS, UJB over), and flat MAT-R error (ABH, KSP, VRD under).

## Findings, ranked
1. Minor, Critical Component 3 says shrinkage on the top-tenth volunteers predicts their MAT-V "within a fiftieth of a logit". The judge got about 0.04 (1.380 against 1.335) with a population-level draw. The conclusion is unchanged (naive route is off by 0.35), but the stated figure may not reproduce under the judge's method.
2. Minor, the design note says dropping the retest gain "moves 18" accounts in one framing, while the card, the submission and the judge report NVK, OJS, UJB going over the cap. These are likely different variants (modelling the shortlist with no gain at all, against the gain held at 0.04). Worth confirming that checks.py R3b and the submission wording describe the same variant.
3. Hygiene, the interruption ask rests on release 5.3.2 behaviour that is visible only in the data; the standard's wording closes it, so no change is required.

## Next action for the author
Either reword Critical Component 3 to a tolerance the files reproduce (for example "within about 0.05 of a logit", against 0.35 for the naive route) or confirm the "fiftieth" figure with the exact method in checks.py. Then ship; no determinism fix is needed.
