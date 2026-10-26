# determinism-check report, task137, pass 2 (2026-10-26)

## Verdict
DETERMINISTIC, with a minor SOLUTION_WRONG on the stated intermediate figure (wording only).
**Disposition:** FIX_NOW (solution wording only; the call, the pack and every ask figure stay frozen)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The 45,000 call reproduces from the shipped files under every specification the judge swept (grown 44,047 to 45,151, inside the 43,750 to 46,250 rounding cell). The easy routes, 42,500 (seen plus turned away) and 40,000 (seen alone), are contradicted by the practice-level dip after run-out weeks. All 28 hospital-visit cells and all 8 sickness figures reproduce exactly. The write-up's "about 41,700 / 44,700 / about 2,000" does not reproduce to the unit under the judge's faithful base specification (41,817 / 44,795; 41,693 to 41,743 only under variants), so the intermediate wording needs a band. The filed 45,000 is unaffected.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| GP seen 2025-26 | 38,386 | 38,386 | yes |
| GP turned away | 1,345 on 58 days | 1,345 on 58 days | yes |
| Run-out coefficient | about -0.21, SE 0.014 | -0.209, SE 0.0137 | yes |
| Underlying 2025-26 demand | about 41,700 | 41,817 (range 41,119 to 42,149) | band only |
| Grown twice at 3.5% | about 44,700 | 44,795 (range 44,047 to 45,151) | band only |
| Kept in-house | about 2,000 | about 2,000 to 2,100 | band only |
| Plan, nearest 2,500 | 45,000 | 45,000 | yes |
| Hospital visits, 7 specialties x 4 quarters | table | 28 of 28 identical | yes |
| Sickness days and rates by quarter | 29/23/39/23; 6.8/5.6/8.7/5.2 | identical | yes |

## Competing answers that survived
None on the main call. Two soft spots on the asks, both judged forced by the files:
- Clinic-code map: the register's clinic_days give a wrong map, and the late-March 2026 weekday sets match exactly one old code each. No file states the April change in sessions, so the map is discoverable from data only.
- E-roster "Vacant line = Y" rows: long-sickness continuations sit beside the one real vacancy, which annual report section 4 dates (14 Jul to 12 Sep 2025). A dictionary-only reader files lower sickness numbers (Q1 11 days, 2.7%). This is the softest committed answer.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 rows or more | 311,893 and 87,958 | yes |
| Distractors | 2 or more, in metadata, no label in a file name | patient survey, hub session plan; neither file name labels one | yes |
| Distractors used? | unused, relevant, ruled out by a shipped fact | carry no demand figure (design note); judge found nothing in them that answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 36 ask figures; prompt states whole, one decimal, nearest 2,500 | yes |
| Prompt shape / rubric | identifiable, 25 or more criteria | shape "other" in metadata; 36 ask figures plus call and components exceed 25 | yes |
| Reads as real | no LLM tells | judge found none (one harmless Company string nit in xlsx app.xml) | yes |

No spec-gate failure.

## Gate G reconciliation
Thread: statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. The card and design note declare stump_class analytical, with the stump a lagged-displacement count model on the previous week's run-out share. This matches. The declared distractors are not named as the surface read. Gate H: domain pass, layers pass, decisive_step analytical. This matches the card's analyst_test and domain_test (the design's 41,714 / 44,685 sit inside the judge's sweep).
Note: the judge classes the decisive step analytical, and the thread reached the golden by applying the model with specification choices the data had to settle, so there is no "textbook method" caveat for the main thread.

## Stump power (Gate F)
Good on paper: the annual report hands over the 42,500 route. Scored readers so far: Reader E (Sonnet) missed the call at 42,500 and 0 of 36 ask figures, score_reader PASS. Reader F (Opus) still running. The asks (clinic-code map, roster vacant lines) carry the ask-side weight.

## Findings, ranked
1. (FIX_NOW, wording) Intermediate figures "about 41,700 / 44,700 / about 2,000" in submission.md do not reproduce under the faithful specification; restate as "about 41,800 (41,700 to 41,800 across specifications), grown about 44,800" and "about 2,000 to 2,100". Check that any golden or sheet text carrying these figures agrees. The call and all asks are unchanged.
2. (Soft, no action required) Roster vacant-line reading rests on annual report section 4 plus roster inference; the files never state the continuation rule.
3. (Soft, no action required) Clinic-code map is forced by data only; no file states the April session change.
4. (Nit) xlsx Company string "Hollinsfield and Brantmoor Hospitals NHS Foundation Trust" against "Hollinsfield General Hospital".
5. (Presentation) Chart partial weeks at the FY edges are a choice; no graded number depends on it.

## Next action for the author
Reword the intermediate figures in submission.md (and any golden text repeating them) to the bands in finding 1, keep 45,000 and every ask unchanged, then ship; no further re-judge is licensed.
