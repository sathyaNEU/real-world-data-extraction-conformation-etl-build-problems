# determinism-check report, task483, 2026-11-02 (pass 1)

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor (selection bias in the estimand) / etl_conformance, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Note: the runtime had no Agent tool; the main session spawned the single isolated thread from my brief (scratchpad determinism-check-task483-run1/judge_brief.md). Its verdict is determinism-check-task483-run1/verdict.md.

## Why
The main call is forced from the shipped files: Morrow Cross 73.3, Tamsey 67.5, Kesterby 47.8, Upper Lode 44.3, Ashwell Vale 42.6, Stanbridge North 29.7, Brackenholt 24.0 (rounded 70/70/50/40/40/30/20), pharmacists to Morrow Cross and Tamsey, Kesterby runner-up. One narrow Gate C fork touches the asks table only: specification 3.2 "a first course on it" read conditionally (chance among courses actually issued on the drug) moves four of seven nearest-10 figures (Ashwell Vale 40 to 44.8, Stanbridge North 40 to 39.2, Upper Lode 30 to 34.9, Brackenholt 30 to 26.2; Morrow Cross 60, Tamsey 60/57 vs 70), while the slate and runner-up hold. The counterfactual wording favours the pooled reading but the text does not close it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| First courses 2026 / 2024-26 | 16068 | 16068 / 48086 (27, 28, 29-day lookback identical) | yes |
| Other-drug first courses MC/T/K/UL/AV/SN/B | 1123/1098/543/610/521/1192/420 | same | yes |
| Same-day cultures | 4658 | 4658 (4678 rows; 20 same-result duplicates) | yes |
| NITR / MECI / FOSF chance | ~5 / 13 / 10 | 5.4 / 13.1 / 9.9 | yes |
| Courses stopped (nearest 10) | 70/70/50/40/40/30/20 | 73.3/67.5/47.8/44.3/42.6/29.7/24.0 | yes (pooled reading) |
| Enterococcus patients K/AV/MC/T/SN/UL/B | 129/84/143/122/133/92/110 | same | yes |
| Enterobacter patients K/AV/MC/T/SN/UL/B | 53/32/48/43/33/42/31 | same (old ENTC, new ECLO; KAER excluded) | yes |

## Competing answers that survived
- Conditional vs pooled chance (spec 3.2): pooled gives 70/70/50/40/40/30/20; conditional gives 60/60/50/44.8/39.2/34.9/26.2 style figures. Same call and runner-up; four asks figures differ. No shipped rule closed it.
- Minor: Enterobacter counting KAER (organism file names it Klebsiella, so literal reading excludes); naive ENTE+ENTC mapping (enterococcus Kesterby 162, Morrow Cross 174); hospital-requested cultures (excluded by "from a practice or the hub"). The old ENTE/ENTC swap is stated in no shipped document, identified by H-prefix and resistance profile; the prompt's "an Enterobacter" was the looser wording.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 10 | yes |
| Formats | 3+ | csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | 118,996 rows | yes |
| Distractors in metadata.json | 2+, none named in a file | 3 (icb prescribing, c_difficile, list sizes); no file name labels one | yes |
| Distractor unused, weighs, does not answer a graded quantity | yes | none answers a graded quantity (judge found no shipped ranking) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-network cuts, whole numbers, nearest 10 | yes |
| Prompt shape, 25+ criteria | yes | shape 01; rubric not generated here, count not verifiable by me | unverified |
| Not LLM-read, goldens realistic | yes | judge found no authoring disclosure; golden xlsx has Placement chart, Chances and Outside sheets | yes (judge) |

## Gate G reconciliation
Judge: mechanism statistical_rigor/etl_conformance, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (R3 decisive: cultures at the first consultation vs cumulative antibiogram): matches. No antibiogram or ranking ships, the declared distractors are not the surface read carrying the task. Gate G: clean. No mismatch.

Gate H line (judge): domain: pass, layers: pass, decisive_step: analytical. Matches the design note's `## Three rules` (domain test, Layer 2 estimand under selection on the outcome, "No filed rule says which cultures"). Main-thread caution: the stump rests on sample selection that no shipped field marks; weigh the ladder as the note does.

## Stump power (Gate F)
Good. About half of matched cultures follow a failed course (lag 3 to 13 days); the all-cultures route puts NITR at 14.5 to 14.8 per cent and names Kesterby 24, Ashwell Vale 19, a clearly separable wrong answer. Not a landable-by-textbook-method case: the CLSI M39 antibiogram is the wrong route here.

## Findings, ranked
1. Gate C (asks): spec 3.2 "a first course on it" conditional vs pooled moves four nearest-10 table figures. FIX_NOW.
2. Minor: Enterobacter ask wording (KAER); old ENTE/ENTC swap unstated in shipped documents (identifiable from H-prefix and resistance profile).
3. Rubric count not verified.

## Next action for the author
Pin the chance's population in specification 3.2 and name "Enterobacter cloacae" in the prompt (already applied by the main session); re-judge once on the rebuilt bundle (run 2).
