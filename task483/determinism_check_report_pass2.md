# determinism-check report, task483, 2026-11-02 (pass 2, re-judge of the rebuilt bundle)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (selection bias in which cultures stand for a course), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Bundle: target.zip sha256 d8cd26685eb0f19b..., fresh unzip; one isolated thread, verdict at scratchpad determinism-check-task483-run2/verdict.md. Pass 1 (FIX_NOW) is in determinism_check_report.md.

## Why
Executed word for word, specification 2.1, 3.1, 3.2 (now pooled over all first courses "whichever antibacterial each was in fact issued"), 4.1, 4.2 plus the code lists and register reproduce the golden: 16,068 first courses in 2026, chances from the 4,658 first courses with a same-day culture, Morrow Cross and Tamsey about 70 each, Kesterby runner-up about 50. The pass-1 conditional-versus-pooled fork is closed. Residual forks are low grade and none touches the call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2026 first courses | 16068 | 16068 (lookback 14 to 30 days, acute-only, sex-keyed all identical) | yes |
| Other-drug first courses MC/T/K/UL/AV/SN/B | 1123/1098/543/610/521/1192/420 | same | yes |
| Same-day cultures | 4658 | 4658 (4,678 pairs, 20 duplicate LabNos); windows 0, +-1, +-2 identical | yes |
| Chances NITR/MECI/FOSF | 5/13/10 per cent | 5.39/13.12/9.88 (TRIM 15.24, CEPH 7.17, COAM 5.75, AMOX 24.32) | yes |
| Courses stopped, nearest 10 | 70/70/50/40/40/30/20 | 73.3/67.5/47.5/44.3/42.4/29.6/23.9 | yes |
| Enterococcus patients K/AV/MC/T/SN/UL/B | 129/84/143/122/133/92/110 | same | yes |
| Enterobacter cloacae patients | 53/32/48/43/33/42/31 | same | yes |

## Competing answers that survived
- Culture window: unstated in the specification. The data separate it (cultures only at gap 0 or +3 to +13 days; resistance to the issued drug 5.3 vs 31.2 per cent for nitrofurantoin), so 0 to 2 days all give the golden. A 0 to 3 day window moves Tamsey to 62.5 (rounds to 60); 0 to 5 gives Kesterby, Morrow Cross, Ashwell Vale, Tamsey; 0 to 7, 14, all cultures or the cumulative antibiogram give Kesterby and Ashwell Vale. These are the intended wrong routes, each using post-failure cultures. Low grade, data-separated.
- Ask 4 Fork B: cutover keyed by collection date 7 Sep 2026 instead of accession system moves Ashwell Vale 83/34, Stanbridge North 133/34, Upper Lode 91/44, Kesterby cloacae 54. The accession-system reading is the unique correct one but 7 Sep is not written in a shipped file.
- Ask 4 Fork C: age at the culture vs maximum 2026 age moves Brackenholt enterococcus 111 vs 110.
- Ask 4 Fork A (literal code table, ENTE unmapped) is avoided by a solver who spots the profile shift; no shipped document states the lab change.
- Sensitivities that do not flip: no-dedupe, row-level join, F-only, practice-matched, excluding CSU specimens; excluding first 28 days of 2024 gives Tamsey 65.0 (still 70). A "2026 only" chance flips the runner-up but 3.2 pins 2024 to 2026.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 10 | yes |
| Formats | 3+ | csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | 118,996 (issues), 73,705 (cultures) | yes |
| Distractors | 2+ in metadata.json, none named in a file | c_difficile_community_cases, gp_registered_list_sizes_2026-10, icb_antimicrobial_prescribing_2025-26; none labelled, none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx with Placement chart, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-network cuts, whole numbers, nearest 10 | yes |
| Prompt shape, 25+ criteria | yes | shape 01; rubric not generated in this pass, count not verifiable by me | unverified |
| Not LLM-read, goldens realistic | yes | judge found no authoring language; document properties name roles only | yes (judge) |

## Gate G reconciliation
Judge: statistical_rigor / analytical_non_defect / surface_read_dependency no / sole_data_defect no. Design note and card: decisive step is estimating the chance from cultures at the first consultation rather than a cumulative antibiogram (R3); no antibiogram or ranking ships. Match. The declared distractors are not the surface read carrying the task. Gate G clean.

Gate H (judge): domain: pass, layers: pass, decisive_step: analytical. Matches the design note's `## Three rules` (domain test, Layer 2 estimand under selection on the outcome, no filed rule says which cultures). The lab recode in ask 4 is data semantics in an ask only, which the rules allow.

## Stump power (Gate F)
Good. The pooled file is the natural default and sends the pharmacists to Kesterby and Ashwell Vale; only course-linked same-consultation chances give Morrow Cross and Tamsey. Thin point: nothing states that late cultures are post-failure, so a strong model that notices the 0 versus 3 to 13 day split and the issued-drug resistance jump will pass. That is the intended analytical bar, a landable route for a careful solver, to be weighed against the design note's ladder.

## Findings, ranked
1. Low: culture-link window unstated, data-separated (windows 0 to 2 identical; 3 or more days differ).
2. Low: ask 4 cutover keyed by accession system, 7 Sep not written in a shipped file (Fork B, up to 2 patients per cell).
3. Low: ask 4 age basis (Fork C, one patient in Brackenholt).
4. Rubric criterion count not verified here.

## Next action for the author
Ship. Optionally close Forks B and C with one sentence in the prompt or a data note (organism codes follow the issuing laboratory system by accession; age at the culture date); do not name the consultation-day culture in 3.2, which would hand over the stump.
