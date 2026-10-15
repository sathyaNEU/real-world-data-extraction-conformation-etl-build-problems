# determinism-check report (pass 2), task261, 2026-10-15

## Verdict
NOT_DETERMINISTIC (one supplementary item only: xlsx item 3, the customer household counts and dollars; the main recommendation, the docx, the chart and the other asks are forced and correct)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Fix applied after the verdict, NOT judged: the orchestrator filed the one open item in the generator. The data dictionary's nominations file now says a member's spouse or de facto partner who is not a client is known only from the nominations, and the register's household line says a household's partners at any date, clients or not, are those alive on that date. No thread has re-read the text since; this pass's verdict stands as returned.

## Why
The golden's customer figures (xlsx item 3, six households-and-dollars rows) held only if a partner missing from the register is taken from the spouse or de facto nominee on any nomination type of a household member's pension. No shipped text said so at judging time; the dictionary spoke of partners "alive on that date" among register clients, and the brief said "placed the same way". Three licensed readings gave three answers (table below). The survey half (main call, SEs, chart) is fully forced by user guide 7.2 and the brief.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Medians 55-64 / 65-74 / 75+ ($) | 790k / 1,048k / 815k | 790,343 / 1,048,229 / 815,286 | yes |
| Adjacent diffs / SE / ratio | 212,104/23,733/8.94; 252,663/45,354/5.57; 256,343/76,861/3.34; 257,885/95,175/2.71; -232,943/149,133/-1.56 | same | yes |
| Independent-sum SE, 55-64 vs 65-74 | 165k (1.6) | ~163k-164.5k (1.58) | yes |
| Replicate correlation | 0.70 | 0.699 | yes |
| Chart interval, 65-74 vs 75+ | -525k to +59k | same | yes |
| RIA households 55-64 / 65-74 / 75+ | 442 / 1,168 / 746 | same | yes |
| RIA balance | 207,655k / 520,479k / 249,568k | 207,654,585 / 520,479,069 / 249,567,875 | yes |
| RIA payments | 11,448k / 30,320k / 17,994k | 11,447,850 / 30,319,980 / 17,994,300 | yes |
| Annuity households / income | 176 / 467 / 284; 3,606k / 9,011k / 5,614k | 176 / 467 / 284; 3,606,196 / 9,011,085 / 5,613,884 | yes |

## Competing answers that survived
Partner not on the register (customer asks only, at judging time):
| Reading | RIA 55-64 / 65-74 / 75+ | Annuity households |
|---|---|---|
| Register only (literal dictionary reading) | 453 / 1,175 / 717 | 182 / 468 / 277 |
| Reversionary nominee only | 446 / 1,174 / 736 | not tested |
| Any spouse or de facto nominee (golden) | 442 / 1,168 / 746 | 176 / 467 / 284 |

Dollars move by $1.1m to $10m, so rounding does not hide it. The closing sentence is the post-verdict generator fix above, unjudged. The pull-date fork (take-back anniversaries to 12 Jan vs 31 Jan) is closed by "amounts as at the pull" and not counted as open.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | csv, pdf, xlsx, docx | yes |
| Large file | 25,000+ rows | household summary 29,940 rows (plus 5,988 x 200 replicate weights) | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | bulletin xlsx (declared wrong-basis, ruled out by the brief's older-partner rule) and customer research pdf | yes |
| Distractor relevance | unused by solution, weighs, ruled out by shipped fact | bulletin reproduces a reference-person grouping (1.6x-type error not drawn from it; brief closes it) | yes |
| Deliverables | 1 to 3, all in golden | docx, xlsx, svg, all in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | customer asks per group with count, balance, payments; "nearest thousand" in prompt | yes |
| Prompt shape | identifiable, rubric 25+ | shape 14 on the card; criteria count not checked here (rubric is generated downstream) | shape yes, count not verified |
| Reads as real, not LLM | clean | thread found no authoring language or banners | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump_class analytical; stump sentence is the independent-sum SE (four segments) against the difference's own replicate SE (five segments). Match. The declared distractor (bulletin) is not the surface read carrying the task; the easy route is the method, not a wrong shipped number. No Gate G finding.

Gate H (thread): domain: pass, layers: pass, decisive_step: analytical. Design note Three rules: complex-survey-estimation-variance, Layer 1 mess (implicates, person file, reference person, bulletin RSEs), Layer 2 variance of a contrast on shared clusters; matches. No mismatch.

## Stump power (Gate F)
Main call: independent-sum route gives ratio ~1.6 and four segments against the true five; recoverable from the guide's 7.3 area-sharing text and the 0.70 correlation. The asks add independent routes (register hygiene, reversionary survivor, deferred and January take-back); one was the unpinned partner fork, now filed in text but unjudged.

## Findings, ranked
1. xlsx item 3: non-client partner source unpinned at judging time (underspecified_objective). Fixed post-verdict in the generator, not re-judged.
2. Rubric criteria count not verified by this pass.

## Next action for the author
Rebuild and confirm the xlsx item 3 figures are byte-identical under the new dictionary and register wording, then re-run checks and reship; the main call, survey files, replicate weights and chart stay untouched.
