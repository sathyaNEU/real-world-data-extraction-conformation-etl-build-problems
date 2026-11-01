# determinism-check report (pass 3), task264, 2026-10-18

Judge thread: one, sonnet, medium, isolated to /tmp/determinism-check-task264-1792288337/target/target/ (fresh unzip of target.zip). Spawned by the main session from judge_brief.md; verdict at /tmp/determinism-check-task264-1792288337/verdict.md. Scope: the reship that added Q9 per-park visits (multi-park multiplicity) and re-cut the levy-collection ask.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one residual estimator fork flagged below; optional hardening only)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Resolution 14/2026 (levy_papers_2027-28.pdf, App. A paras 2, 4, 5, 6) counts residents aged 16+ once each, however many times or parks they visited, and excludes outside and unplaceable homes. Summing expansion weight over the respondent's visits to all six parks (Q9) across the 3,973 member-council interviews gives the golden levies to the pound, a 50.7 per cent valley share, and all asks reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Interviews (wave1 + wave2, weights joined) | 4,470 | 2,349 + 2,121 = 4,470, weights sum 2,349,510 | yes |
| Member-council interviews | 3,973 | 3,973 (473 OUT, 24 NK) | yes |
| Residents, nine councils (nearest 100) | 45,500 / 55,900 / 35,200 / 26,000 / 26,900 / 24,500 / 19,900 / 17,900 / 17,500 | same | yes |
| Nine levies | 1,252,070 ... 480,746, total 7,416,300 | same (10,349,900 less 2,933,600) | yes |
| Valley three share and levies | 50.7%, 3,761,141 | 50.7145%, 3,761,141 | yes |
| Parking income net of VAT | 439,313 / 543,124 / 449,759 / 400,761 (1,832,957) | same | yes |
| Vehicles | 171,505 / 134,156 / 166,487 / 126,385 (598,533) | same | yes |
| Levy on time / late, 9 councils (18 figures) | e.g. KDM 498,214 / 166,071; GRB 190,819 / 381,638 | all 18 | yes |

## Competing answers that survived
1. **Multiplicity estimator (main call, residual).** No shipped text names the estimator. Golden: weight / total visits to the six parks. A second unbiased route, weight / (number of parks visited x visits to the interview park), gives KDM 1,239,360; RVW 1,571,080; SNG 970,904; LKS 707,854; GRB 724,596; HNM 677,440; CHD 549,014; WDS 486,044; FNC 490,009 (valley share 51.0%, smallest council Wendstow, not Ferncote). Both are unbiased under the design, so the data cannot separate them. The judge rates it an unusual route for an on-site exit survey, and the resolution's "counted once however many times" and the note's approach-every-eighth-adult wording point to total visits, so it was not judged disqualifying. Note that the design note's SF5 row closes only the per-park-alone variant (R4, 55.5%), not this one. It is a reviewer risk at pound level.
2. Rounded residents as the apportionment basis (levies move up to about 1,200): closed by the resolution's "its number" and the prompt's rounding clause being presentation.
3. Cash-book posting date against bank value date (ask 5): closed by the manifest's definitions (value date vs posting date, one day lag).
Closed in the files: PM-2103 placement by tariff match (register gives 565,515 / 416,922, wrong), app income already net of VAT, C-09 halving, C-05/C-10 overlap, C-07 placement, Grinbury Q4 credited nowhere, Chaldale Q3 short pay, combined Hornmere/Wendstow credit split by cash-book allocation, 1 Apr 2025 receipts excluded (2024-25 invoices).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 19 | yes |
| Formats | 3 or more | 3 (csv 12, xlsx 5, pdf 2) | yes |
| Large file | 25,000 or more rows | pay_machine_transactions about 246,000 rows (pass 2 count; counts file 53,063) | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | 3 (annual_permits, population_estimates, supplier_payments); none labelled by name | yes |
| Distractors weigh yet are unused | yes | judge: present and unused; population basis ruled out by the resolution | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 9-council, 4-park and 18-figure asks, units and rounding in the prompt sentence | yes |
| Prompt shape, 25+ criteria | yes | 9 + 1 + 8 + 18 + report graded figures, well over 25 (rubric itself not generated here) | yes |
| Not LLM-generated; goldens real work products | yes | judge found no authoring leakage; golden realism not re-run by me | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: estimation_fit family, analytical, Layer 2 = person total from a visit-weighted exit sample with multiplicity across the six parks; analyst test lands on 25.0 / 55.5 / 85.1 / 53.4 per cent against the golden 50.7. The thread names the same rival answers (55.5 and 85.1), so there is no mismatch. Declared distractors (permits, population estimates, supplier payments) were not the surface read. Gate G: passes, no shipped artifact ranks the candidates wrongly on the decision question (Appendix B's 2026-27 population basis is the superseded basis, not a wrong ranking of the 2027-28 question).
Gate H: domain pass, layers pass, decisive_step analytical. This matches the design note's Three rules.

## Stump power (Gate F)
Good. Easy routes fail with every council wrong: visits share 85.1% (levy 6,310,493 for the valley three), per-interview-park frequency 55.5% (4,119,122), mean-visit division 25.0%, unweighted 1/visits 53.4%, against 50.7% (3,761,141). The asks add independent devices (PM-2103, C-09, C-07, value dates).

## Findings, ranked
1. Residual fork: the multiplicity-estimator variant (see above), not in the SF table; optional to close.
2. The design note's SF5 asserts only R4; there is no asserted row for the variant above.
3. No hygiene or spec findings.

## Next action for the author
Ship as is, or (optional, would change what solvers see and need a rerun) add one fieldwork-note sentence describing the sample as one sample of adult visits across the six parks, filing the design (the WHAT), not the formula, and add an SF row for the variant. Either way, record the variant in the design note's fork table.
