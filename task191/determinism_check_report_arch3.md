# determinism-check report, task191 (architecture 3), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** SEND_BACK (reconciliation confirms the thread's send-back on Gate G / Gate H3)
**Stumping type:** mechanism: planted_defect_flip, stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes

## Why
The call is forced: San Lazaro is the only depot at 1.3 times the fleet rate or more once non-genuine warnings are set aside (fleet 22.6 per cent, San Lazaro 45.2, ratio 2.00, La Ribera 1.14). Every graded figure reproduced from the shipped bundle (target.zip sha256 4cd23ce6...af24a). The send-back is on stump type, not on determinism: the decisive step is catching four fixed structures that inflate the raw rate, with the Plaza de Abastos as the genuine busy place that a count-based removal wrongly drops. Remove those structures and the surface read is already right.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Warnings kept (type, event_id, local window) | 71,247 | 71,247 | yes |
| Set aside at the four places | 17,968 | 17,968 (stable 15 to 150 m) | yes |
| Fleet rate (counted) | 22.6 | 22.59 | yes |
| Raw fleet rate / ratios | 38.9; Hornacho 1.41, Valdeolmos 1.48, San Lazaro 1.16 | same | yes |
| Per-depot counted, not braked, rate, ratio (7 rows) | as submission | all match | yes |
| Hours (28 cells) | as submission | all match | yes |
| Collisions (7) / claims (7) | 20,25,19,19,25,22,21 / 24,207; 25,850; 20,517; 33,737; 29,216; 22,579; 17,280 | all match | yes |
| Kilometres (28 cells) | as submission | all match, but 3 cells land on exactly .5 | yes, with rounding fork |

## Competing answers that survived
1. Literal 10 m bins (submission step 4, not filed in the shipped terms): removes only 17,708 warnings, giving 22.9 / 1.97 / 1.13 against golden 22.6 / 2.00 / 1.14. Any place-based removal (15 to 150 m radius, contiguous clusters) gives the golden. Call unchanged; graded figures change.
2. Half-way kilometre cells: San Lazaro July 75,126.5, Santa Clara July 82,442.5, Valdeolmos July 93,312.5. Golden rounds half up; round-half-even gives 75,126 / 82,442 / 93,312. No shipped rule closes it. Three graded cells at risk.
3. The 10 per cent threshold is unfiled but any threshold from about 3 to 25 per cent gives the same set: harmless.
No fork moves the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, txt) | yes |
| Large file | 25,000 rows | warnings csv 99,207 rows | yes |
| Distractors in metadata.json, none named by file | 2 or more | depot_absence_overtime_2026.xlsx, boardings_by_line_2026.csv; neutral file names | yes |
| Distractors unused yet weighable; one answering a graded quantity is ruled out | as stated | unused by the solution; the thread found no arithmetic route to a graded figure from them; I did not test relevance or a ruling fact beyond that | yes (partial check) |
| Deliverables | 1 to 3, all in golden | 3 (docx, xlsx, svg), all in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-depot x month/week cells; prompt states units and rounding, but not the half-way rule (finding 3) | partial |
| Prompt shape, 25 or more criteria | yes | not measurable before the rubric is generated | not checked |
| Reads as real work product, not LLM generated | yes | the thread found no authoring leakage; operational documents | yes |

## Gate G reconciliation
Thread: mechanism planted_defect_flip, family surface_read_rejection, surface_read_dependency yes, sole_data_defect yes. Gate H: domain pass, layers missing (Layer 1 mess carries the stump), decisive_step planted (H3 fails).
Design note and card: card stump_class analytical, with an analyst_test and domain_test; the card's mechanism, family and defect fields are empty. The note declares the family estimand_identification, "No decoy: nothing is planted", and the decisive step as per-pass classification of places. The note's own default path ends on Hornacho and Valdeolmos (rung 0, all warnings) or La Ribera (rung 1, busiest places dropped), and its Survivor anatomy says that no file marks a warning genuine.
Mismatch. The note calls the structures the network's own and no decoy. The thread's reading: the four 25 to 30 per cent structures are exactly what flips the surface read, and the Plaza de Abastos is a busy genuine place sized to defeat the count-based filter. The surface read is the raw pooled rate, and it carries the whole task. On clean data San Lazaro wins trivially. This is the retired surface_read_rejection scaffold, and under the CLAUDE.md rule 3 it is a planted defect (or hidden-classification) deciding the call. The thread names no declared distractor as the surface read, so the distractors are not too load-bearing.

## Stump power (Gate F)
Argument against the thread: per-pass exposure normalisation is a base-rate method, and the unfiled definition of "genuine" forces an inference. The data separate the candidates by a wide margin (25.0 to 30.3 per cent against under 3 per cent), so a strong solver who asks "does this place fire on every pass" lands the call. The thread judged that frontier solvers may fall for the pooled-rate or count-filter routes. Weighed against the design note's ladder (rung 3 only), this is a landable call for an analyst who checks exposure, and the difficulty sits in detecting the defect, not in a method choice. The reconciliation holds with the thread: send-back.

## Findings, ranked
1. Gate G / H3: the decisive step is the detection of planted-looking fixed structures plus the Plaza decoy; surface read wrong, sole data defect, Layer 1 carrying the stump. Redesign the decisive step so the reported numbers are fine and the difficulty is a method or estimand choice (cheap repairs below do not clear this).
2. Fork: submission step 4 (10 m bins, 10 per cent) does not reproduce the golden's 22.6 / 2.00 / 1.14 (gives 22.9 / 1.97 / 1.13). Correct the step to a place-based removal, or move the golden. Not filed in the terms either way.
3. Fork: three kilometre cells on exact .5 with no rounding rule shipped; round-half-even misses them. Nudge the data off .5, or file half up.
4. Housekeeping: the design note names the chart genuine_warning_response_2026.svg, while the prompt, metadata and submission use warning_response_2026.svg. Card mechanism, family and defect fields are empty.

## Next action for the author
Redesign the decisive step (finding 1) in a new architecture on data where the reported numbers are right; if the design is kept anyway, at minimum fix the place-based removal wording and the .5 kilometre cells first.
