# determinism-check report, task241, 2026-11-03

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (minor: one overclaim in Critical Component 3; the call and all 52 deliverable cells reproduce)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call (detection off on KR-2612, 2616, 2618, 2620, 2621, 2623) is forced by the shipped data. No file records who answered a machine-classed call, so the share is measured from the inbound switch: people ring back within minutes, machine owners hours later (median 141 min). Policy section 3 says an abandoned live answer hears the same recorded message, which makes each project's abandoned live answers the control for its people's return rate. Nearest values to the limit are 5.7% (KR-2619, on) and 16.8% (KR-2618, off), so the margin is wide and robust to window and basis. Larkspur and the 2025 audit are neither 2026 nor per project; the raw rung-back share is a lower bound. The only defect is that Critical Component 3 claims "every window from 5 to 40 minutes gives the same shares", which fails at W=5 (KR-2623 reads 29.51, rounds to 30, not 29) and at W=3 or 4 for a few cells.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Dialer rows / distinct calls | n/a | 291,895 rows, 10,273 repeats, 281,622 distinct | yes |
| False-machine share, 13 projects (W=20) | 3,18,2,4,3,20,4,17,6,18,32,2,29 | 3.1,17.7,1.9,3.6,2.6,20.0,3.7,16.8,5.7,17.8,31.9,2.3,29.2 | yes (13/13) |
| Verdicts | six off | six off | yes |
| Windows 6 to 60 min (start) / 3 to 60 (end) | same shares | same whole-per-cent shares | yes |
| Window 5 to 40 min, "same shares" (CC3) | same shares | W=5 KR-2623 30 not 29; W=3,4 move KR-2614, 2618, 2621 | NO (overclaim) |
| Calling hours (13) | 181,193,76,175,110,120,147,186,125,178,85,198,124 | identical | yes |
| Interviews (13) | 3488 ... 1971 | identical after excluding 26 inbound completes dated 2027-01-02 to 06 | yes |
| Interviewer hours (13) | 9,114.6 ... 5,418.5 | identical to 0.1 | yes |

## Competing answers that survived
Cell-level only, none moves the call:
1. "Rang" as AnswerTime instead of call start: KR-2611, 2612, 2622 read 1 higher (182, 194, 199). Policy section 2 wording favours call start.
2. US DST dates are in no file (state_time_zones.csv holds only a yes/no flag and the standard offset). A wrong rule moves cells by 1 to 4; ignoring DST by up to 27 (KR-2612).
3. The dialer export clock is never stated to be Central (implied by 651 caller-ID lines, the 09:00 to 21:38 call span, Minnesota-dominated sample).
4. The prompt does not say "every project" means the 13 registered; KR-2624 is in dialer, switch, hours and case records (6.7%, on) but not in the register. A 14th row is extra, not wrong on the call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 24 files | yes |
| Formats | 3 or more | csv, xlsx, docx, pdf | yes |
| Large file | 25,000 rows | case_records_2026.csv 128,940 rows | yes |
| Distractors | 2 or more in metadata, none labelled by file name | mobile_consent_log, qa_monitoring_scores, client_invoices named; file names do not label them | yes |
| Distractors unused yet weighable | yes | invoices count supervisor verification rows (ties to wrong interview count); consent log and QA scores unused. Larkspur and audit are weighed, not declared distractors, and are ruled out by section-3 scope and date | yes |
| Deliverables | 1 to 3, all in golden | xlsx and pdf, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 3 per-project asks, 13 rows each; unit and rounding in the prompt | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | shape 10 scorecard; design note says ask sheet clears 25 (not independently counted) | yes (stated) |
| Not LLM-generated | yes | judge found system-artifact texture, no authoring language; minor docx core.xml date 12 Nov vs "Issued 20 November 2026" | yes, with nit |
| Prompt | one paragraph, under 1,000 chars | 702 chars, one line | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card/design note: stump_class analytical, decisive step the per-project prompt-return ratio against the project's own abandoned control; the default path is the certified 2.1% / audit 2.25%. These match. The declared distractors (consent log, QA scores, invoices) are not the surface read carrying the task; the surface reads are Larkspur and the audit, which are correct for what they measure and are not shipped as a ranking of candidates. Gate G class: clean (no artifact ranks the projects wrongly). One divergence: the design note's Three rules and the judge disagree on the window corridor (note: "0 points on every graded share across 5 to 40 minutes"; judge: false at W=5 and below).

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Layer 1 mess (two export layouts, repeated days, legs, test calls, appointment numbers, July renumbering, hours.minutes, Arizona/DST) decides nothing; Layer 2 is the measurement-error estimate of a misclassification rate against a per-project control.

## Stump power (Gate F)
Good. Certified 2.1% and audit 2.25% give none off; raw rung-back share (0.5 to 8.2%) gives none off; pooling the abandoned control (28%) drops KR-2618 to 5.8% and files five off instead of six. Only the per-project abandoned-calibrated estimate gives the golden six. The decisive step is an estimator the data separate from candidates, not a stated rule or a field reading. Caution for the main thread: the pooled-control variant misses one project by a single flip, so the ladder should be weighed on whether a strong solver pools; the 52 ask cells are also hard to land in full.

## Findings, ranked
1. (FIX_NOW) Critical Component 3 in submission.md overclaims: "every window from 5 to 40 minutes gives the same shares" is false (W=5 moves KR-2623 29 to 30; W=3,4 move KR-2614, 2618, 2621). Honest range: 6 to 60 minutes from call start, or 3 to 60 from call end. The design note's Three rules corridor sentence ("5 to 40 minutes") carries the same claim and should be corrected too.
2. (Minor) The solution steps do not state the call-start convention for "rang" or the US DST dates (8 Mar and 1 Nov 2026), which no shipped file gives; they move cells by 1 to 4 (cell-level only). Optional note.
3. (Minor) Dialer export clock never stated as Central; implied only.
4. (Minor) KR-2624 appears in operational files but not the register; "every project" is read as the 13 registered.
5. (Nit) policy docx core.xml creation date 12 Nov 2026 vs "Issued 20 November 2026".
6. Letter codes in the old export layout map to LIVE/MACHINE and outcomes by inference (talk time, agent profile), undocumented but inferable; judge accepted.

## Next action for the author
Reword Critical Component 3 in submission.md (and the matching sentence in the design note's Three rules) to "every window from 6 to 60 minutes measured from the call start, or 3 to 60 from the call end"; no change to prompt, files or goldens, no rebuild; optionally add the call-start and DST conventions to the solution steps.
