# determinism-check report, task181 (architecture 6), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

target.zip sha256 2ba1a5636e3a2bf73fb58b4679e0a4664a85607dc88579dcf4b3d87d8e078e89. One judge thread, one pass; its verdict is /tmp/determinism-check-task181-a6/verdict.md.

## Why
Every graded figure recomputes from the bundle. The Centre's guide files the estimand ("own practice"). The scans, cycles and equipment log show that steriliser 3 loads after the 12 May 2027 repair carry 115 infections against 21.7 expected. With those procedures set aside only GS-16 and GS-21 are above the limit. Every reasonable alternative treatment (exclude all steriliser 3 items, price the exposure as its own stratum) gives the same pair. Only dropping all post-repair procedures differs (GS-21 alone), which the judge rates an unreasonable reading.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Procedures after cleaning | 30,700 | 30,700 | yes |
| Q2 notice (120 vs 59.894, UCL 76) | notice | same | yes |
| All-procedure Apr-Sep 2027 counts above UCL | GS-05, 12, 16, 21 | 43/22, 45/23, 35/22, 62/21 | yes |
| Exposed procedures / infections / expected | 362 / 115 / 21.7 | 362 / 115 / 21.706 | yes |
| 4.3 times the rate of other procedures | 4.3 | 5.3 observed to expected for exposed against about 1.24 for the rest (120 against 96.5, design note) | yes (note: the judge quotes the 5.3 ratio; the 4.3 is relative to the rest) |
| Unexposed GS-16 / GS-21 | 35 v 22 / 26 v 16 | same | yes |
| Unexposed GS-05 / GS-12 | 4 v 11 / 5 v 12 | same | yes |
| Ask CSV, 60 cells | as filed | all reproduce | yes |

## Competing answers that survived
None on the main call. Low-severity notes that change no named consultant:
1. GS-41 = GS-14 is stated in no shipped file. It is inferred from the handover and the CSSD register. Keeping them separate zeroes six GS-14 ask cells. The judge rates the separate reading poor, and the author placed it as Layer 1 mess.
2. Chart basis: the golden charts infections in the unreached procedures, while a literal reader could chart all-procedure counts. The red set and the call are the same either way, so only bar heights are exposed.
3. Notice cutoff: counting only infections entered by 30 September gives 210 against 235. The guide directs the full count.
4. The judge did not run the case where the 14:40 repair time is read as UTC. It estimated by inspection that only a few loads move.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 11 / 4 (CSV, PDF, XLSX, JSON) | yes |
| Large file | 25,000+ rows | 47,657 scans; 32,036 operations | yes |
| Distractors | 2+ in metadata, none labelled by name | hand_hygiene_audits_2027.csv, theatre_air_sampling_2027.json; names carry no label | yes |
| Distractors unused yet weighable | yes | flat monitoring records, no graded quantity answered | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | 10 consultants x 3 years x 2 measures, "whole numbers" in the prompt | yes |
| Prompt shape and 25+ criteria | yes | shape 10 (scorecard against a threshold); design note counts 61 ask criteria plus the call criteria. I did not re-derive the generated rubric. | yes (note-based) |
| Reads as real, not LLM generated | yes | judge found no authoring leakage in files read; I did not read the goldens | partly checked |

## Gate G reconciliation
The thread and the design note agree: mechanism decomposition_attribution, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The declared distractors (hand hygiene, air sampling) are not the surface read carrying the task; the thread named the all-procedure ratio against the limit as the easy route. The card has stump_class analytical, with analyst_test and domain_test filled in. The card's mechanism and strategy fields are None, so the design note is the declared source. Match, no finding.

Gate H: the thread gives domain pass, layers pass, decisive_step analytical. The design note's Three rules agree (No decoy, Not semantics, Not rule application all present). The thread's one borderline note is that the raw count is true and merely misattributed, so the call is not a flip away from a wrong number. That fits the design.

## Stump power (Gate F)
The easy route (the Centre's ratio against the limit) files four names. The decisive work is a three-step trace: scans to operations, operations to the last passed load, loads to the repair date. Nothing in the files names the fault, and every cycle prints a pass. Partial discounting can keep GS-05 or GS-12. The thread rates stump power real. The design note's pair ceiling is 33.9. Caution: the field's standard attribution step (set aside the common-source exposure, re-test against the limit) is a landable call for a strong solver once the trace is found. The stump is finding the trace, which the main thread should weigh against the design note's ladder.

## Findings, ranked
1. Low: GS-41 = GS-14 is unfiled. Optional fix: a roster line making the handover explicit in a shipped file. This would change solver inputs, so only if the author wants it.
2. Low: chart basis wording. Optional fix: say which counts the chart shows. This would also change what solvers see.
3. Informational: the repair-time UTC case was not run by the judge. The margins are wide.

## Next action for the author
Ship as is, unless you choose to close findings 1 and 2 with filed wording. If you do, the reshipped cut needs the usual re-run of the gates.
