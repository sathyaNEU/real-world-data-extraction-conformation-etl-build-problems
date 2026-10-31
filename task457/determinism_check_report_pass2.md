# determinism-check report, task457, 2026-10-31 (pass 2, stage 4 keep-and-repair reship, target.zip 745e4bab)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Policy 5.4 turns the estimator choice into a back-test (closest total absolute difference to the largest single-manufacturer 2025 amount in the January 2027 publication). On the shipped files it selects one family and one weighting, n/(n+2). Every defensible form tested gives the same fifteen for 2026, and #15 (Baldwin 73.3K) is 22K clear of #16 (Gentry 51.0K). The two forms the back-test rejects (personal unweighted ratio, whole-year reading of each disclosure) are the ones that change the docket. The counts 1,696 and 91, the nature table and the 9,994 rows are literal executions of the filed text and reproduce. The thread was isolated (fresh unzip, blocks inlined, no design material) and ran once.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Owed a 2026 disclosure (appointments 31 Dec 2026, per NPI) | 1,696 | 1,696 | yes |
| Not submitted by 04:59:59Z 16 Jan 2027 | 91 | 91 (cut at 04:59:00, 05:00:00, first-submitted-only all 91) | yes |
| Table by nature, 2025 (USD thousand) | 4,463 / 1,366 / 819 / 325 / 198 | 4,463,425 / 1,366,178 / 819,112 / 325,242 / 197,888 | yes |
| Table by relationship type, 2026 (USD thousand) | 56 / 11 / 97 / 3 | same, only when Kilnworth and Quorvia (former Somnalis) are treated as reporting | yes, with fork 1 |
| Back-test population | 309 | 309 | yes |
| Best weighting | k=2 | k=2 score 523,180 (k=0 1,011,975; k=1 557,017; k=3 530,010) | yes |
| 2026 estimated faculty | 279 | 279 | yes |
| Docket and manufacturers | 15 named | same 15, estimates 139.5K to 73.3K | yes |
| Whole-year reading | rejected | 2025 score 708,830 vs 523,180, swaps the five | yes |
| Conformed CSV rows | 9,994 | 9,994 | yes |

## Competing answers that survived
Low grade, none flips a graded docket membership.
1. Relationship-type table: the list types Quorvia and Kilnworth "Other company" with no ID. Trusting that gives about 64/24/105/4; excluding only Kilnworth, 59/19/105/4; golden 56/11/97/3. Closed by policy 2.2 (a manufacturer is defined by reporting to Open Payments) and the register plus earlier items under the same entry. This is the weakest graded figure and the design's intended device for Ask C.
2. Conformed CSV column layout is unnamed in the prompt (row count is forced).
3. Chart order within the fifteen moves with k (k=1 Baldwin 11th, k=3 Luna 9th); membership does not.
4. Docket preparation date is unfiled; the set is insensitive to it (24 late filers, none on the docket), though the 279 count would be 256 if late filers were dropped (not asked in the prompt).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 12 files; csv, xlsx, pdf; 90,140-row register | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | 3 named (research extract, NIH awards, June 2026 release); none reproduces a graded quantity; file names do not label them | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | counts, five-nature and four-type tables, nearest thousand stated | yes |
| Prompt shape and rubric | shape identifiable, 25+ criteria | shape 01; design note counts about 35 plus about 14 ask criteria | yes (taken from the design note, rubric not generated here) |
| Not LLM-generated; goldens real work products | | judge found real-format columns, no provenance leakage; golden-realism is a separate gate | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; strategy forecast_method_backtest; the whole-year matched-line estimate is the easy route and files five wrong members (Blackwell, Gentry, Harper, Mahoney, Singleton for Black, Hampton, Leach, Luna, Valenzuela). Thread's five-swap and names match the card exactly. The declared distractors were not named as the surface read carrying the task. Match. Gate H line: domain pass, layers pass, decisive_step analytical, matching the note's `## Three rules` and the card's domain_test.

## Stump power (Gate F)
Strong on paper. The back-test separates candidates decisively (708K against 523K). The thread classed the decisive step analytical because the back-test is a computation nobody states the answer to; the correct estimator is not the field's off-the-shelf route (the leak reader's strong-analyst route lands the whole-year docket), so this is not the textbook-landable case. The main thread weighs it against the note's ladder (ceiling there: pair 45.4).

## Findings, ranked
1. Ask C (relationship-type table) is the weakest graded figure: a literal reader trusting the entity list's "Other company" type lands different numbers (fork 1). This is by design (device D2) and the register-reporting definition in policy 2.2 closes it.
2. Conformed CSV layout unpinned (supplementary deliverable only).
3. Chart order weakly pinned by k.
Optional cures (prompt pin of CSV columns; entity-list note) would force a rerun; the thread advised against taking them.

## Next action for the author
None required for determinism: proceed with the stage-4 pipeline (leak reader result and remaining checks), then ship.
