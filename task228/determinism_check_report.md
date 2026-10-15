# determinism-check report, task228, 2026-10-15

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (method selection under the allowance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) saw only a fresh unzip of target.zip and the extracted blocks. It reproduced every committed answer from the bundle. The decisive step is the unit of inference: DH-3 sec. 2 assigns arms by install and sec. 3 defines each share as sessions over all sessions in the arm. At install level, gap sessions holds 10 of 18 and 0 of 64, and events per install is the only check over the allowance (3 false holds against at most 1). Gates A, B, C and E pass. Full verdict: /tmp/determinism-check-task228-r1/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Labels, confirmed / none | 18 / 64 | 18 / 64 (7 withdrawn count as none) | yes |
| Holds, incident / none: gap, late, dup, treatment share, events per install | 10/0, 5/0, 3/0, 3/0, 0/3 | same | yes |
| Hold line | 0.28 pp | 0.2811 pooled, 0.2806 by mean variance | yes |
| Weekly review (flagged; never): telemetry, duplicate, late, consent | 5;5, 1;2, 0;2, 1;2 | same | yes |
| App-wide incident gap sessions | 10,152; 1,100; 12,630; 23,721; 34,141; 5,871 | same | yes |
| App-wide incident shares | 17.56, 30.53, 30.67, 20.28, 32.66, 29.45 per cent | same | yes |

## Competing answers that survived
None survived as an open fork. Two soft forks were noted by the judge:
1. Test unit. DH-3 does not name the test. A session-level binomial z test gives gap 11/4 and late 6/0, so it files late sessions. A Welch t test on unweighted install shares gives late sessions as well. Only the cluster-robust ratio estimator honours both the defined share and the assignment unit. It is a literal reading but a thin one, and it is also the stump, so it is by design.
2. Incident type. The register's incident_type (as opened) differs from the reconciliation PDF's cause established for 6 incidents, and telemetry would read 3;7 against 5;5. The data dictionary resolves it toward the PDF, but the prompt does not say so. Optional tightening, and it needs a model rerun.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 6 (csv, parquet, xlsx, pdf, json, md) | yes |
| Large file | 25,000 or more rows | install_summary_2026q1.csv, 238,808 rows | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | 3 (collector_daily, app_releases, booking_queue); the judge found them unused, and I saw no distractor label in a file name | yes |
| Distractor relevance | weighs, unused, ruled out by a shipped fact | judged unused; none answers a graded quantity | yes |
| Deliverables | 1 to 3 | 1 (xlsx), present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | pp and per cent to 2 decimals, counts whole | yes |
| Prompt shape and 25 or more criteria | identifiable, 25 or more | shape 10 (scorecard); 5 checks, 4 incident types and 6 app-wide incidents give well over 25 gradable figures; the generated rubric is not in the folder, so it is not counted here | yes (rubric count unverified) |
| Reads real, not LLM generated | clean | the judge saw no authoring leakage, and the goldens are business-realistic | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's stump sentence and `stump_class: analytical` match: the easy route is the session-level z test, which files late sessions (gap 4 of 64 false holds, late 6 of 18, line about 0.22 pp), and the correct step is install-clustered inference. The judge's binomial figures (gap 11/4, late 6/0) agree with the design note's 4 and 6. No declared distractor was named as the surface read carrying the task. No mismatch. One housekeeping item: the pipeline.json stump text says "5 of 64" and "5 of 18, about 0.21", which is stale against the design note.
Gate G line: no shipped artifact ranks the candidates wrongly on the decision question; classification analytical_non_defect, no planted defect.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's three rules. Layer 1 is the v1 to v2 export migration, title matching, and preliminary versus confirmed rows. Layer 2 is install-clustered inference plus selection under the allowance.

## Stump power (Gate F)
Plausible. A strong model may take the session-level binomial route and file late sessions with a line of about 0.16 pp, and that would be wrong on both the call and the line.

## Findings, ranked
1. Soft fork: the incident type for the weekly-review ask (register type vs reconciliation cause). It is not a send-back, and the dictionary resolves it.
2. The test unit is not named in DH-3. It is the intended stump, but the reading is thin, so a reviewer could call it underspecified. The judge passed it.
3. pipeline.json stump text is stale against the design note.

## Next action for the author
Proceed to ship. Optionally correct the stale pipeline.json stump text. Adding a prompt line on the incident type would need a rerun, so it is not recommended.
