# determinism-check report (pass 2), task241, 2026-11-03

Bundle rebuilt after pass 1: projects are now KR-2604 to KR-2651 (13 registered), CC3 reworded (window 2 to 120 min). Judge run r2, scratch /tmp/determinism-check-task241-r2/.

## Verdict
As returned by the thread: DETERMINISTIC, plus SOLUTION_WRONG (answer 3, interviews, did not reproduce).
After my reconciliation (below): the single SOLUTION_WRONG finding is a judge miss, not a key defect. Effective verdict: DETERMINISTIC, key reproduces.
**Disposition:** thread said FIX_NOW; reconciled recommendation APPROVE on determinism, with one optional wording fix (state "started in 2026" for interviews in the solution steps).
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call is forced by the files: per project, callback rate of machine-classed calls divided by callback rate of its own abandoned live answers gives 3.11, 17.71, 1.92, 3.63, 2.61, 20.04, 3.65, 16.76, 5.71, 17.84, 31.93, 2.35, 29.21%, matching the key; six off at 16.8% or more, seven on at 5.7% or less. Callbacks show a clean gap (nothing from 2 to 150 minutes after the call), so shares are identical for every window from 2 to 120 minutes from call start or end (CC3's new wording is now true). The thread's one failure, interviews, is explained by the switch log's tail: it runs to 2027-01-06 and holds 26 inbound COMPLETE calls started in 2027 (checked by me against the r2 bundle: 1,406 COMPLETE legs, 26 dated 2027, 26 distinct call ids). The thread's recount of 26,612 + 1,406 includes them; the key totals exactly 26 fewer, and the prompt asks for interviews "in 2026". Pass 1 found and resolved the same 26 (it reproduced all 13 once they were excluded).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Dialer rows / unique ids | n/a | 291,895 / 281,622 | yes |
| Shares, 13 projects | 3,18,2,4,3,20,4,17,6,18,32,2,29 | 3.11 ... 29.21 (as above) | yes |
| Calling hours | 181,193,76,175,110,120,147,186,125,178,85,198,124 | identical | yes |
| Interviewer hours | 9,114.6 ... 5,418.5 | identical to 0.1 | yes |
| Interviews | 3488,2311,1407,2745,1927,1982,2305,1877,2073,2034,1416,1868,1971 | recount 1 to 4 higher on 12 of 13 (26 in all) | thread: NO; reconciled: yes, the 26 are 2027-dated inbound completes (my check; also pass 1) |
| Window invariance (CC3) | 2 to 120 min, start or end | same shares | yes |

## Competing answers that survived
1. Pooled abandoned-callback rate (28.0%) as reference: KR-2631 falls to 5.8% (on), five off; moves whole-per-cent shares for KR-2607 (20), KR-2622 (23), KR-2626 (6). The prompt says "its share" per project, so per-project is literal; thread rates it a residual fork on KR-2631 only, not defensible.
2. Mean of monthly ratios instead of the year's calls: KR-2651 to 31, KR-2631 to 20; the prompt asks for the 2026 share of the year's calls. Decision unchanged.
3. Reading disposition code AA as abandoned (no legend shipped; recoverable from the shared 30 June day) flips the result; recoverable, not a fork.
4. Interviews counted without the "in 2026" cut: 26 higher in total (the reconciled finding).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 24 files (25 zip entries incl. folder) | yes |
| Formats | 3 or more | csv, xlsx, docx, pdf | yes |
| Large file | 25,000 rows | case_records 128,940 rows | yes |
| Distractors | 2 or more named, not by file name | invoices, consent log, QA scores in metadata; also audit, Larkspur weighed | yes |
| Deliverables | 1 to 3 in golden | xlsx and pdf | yes |
| Prompt | one paragraph under 1,000 chars | 702 chars | yes |
| Rubric 25 or more | yes | design note says clears 25 (not recounted) | yes (stated) |
| Not LLM-generated | yes | operational artifacts, no authoring language | yes |

## Gate G reconciliation
Thread matches the card and design note (stump_class analytical; default path the certified 2.1% and audit 2.25%). The declared distractors are not the surface read carrying the task. Gate G class: clean. Gate H: domain pass, layers pass, decisive_step analytical (calibrating callbacks against the project's own abandoned live answers). The AA/X code mapping is a semantic recovery step in Layer 1, not the decisive step.

## Stump power (Gate F)
Good. Certified rate, pilot audit or raw callback share all keep detection on everywhere; pooling the control files five instead of six; misreading AA moves every off-project to 41 to 52%. The asks are heavy multi-system reconstructions.

## Findings, ranked
1. Thread finding (interviews not reproducing, 1 to 4 per project, 26 total): reconciled as a judge miss; the 26 are inbound COMPLETE calls dated 2027-01-02 to 06, outside "in 2026". Recommend no key change; optionally add "started in 2026" to solution step 6 so the cutoff is on the record. Main thread may weigh this as a FIX_NOW for wording only.
2. Optional: state in the key that the appointment-number link is scoped to the job (258 appointment numbers repeat across jobs).
3. Optional: pooled versus per-project reference leaves KR-2631 as a residual fork; the thread suggests a few words such as "measured on its own calls" in the prompt without filing the method. Rule 3 caution: this must stay a WHAT (population) not a HOW.
4. Minor: no disposition legend shipped (mapping recoverable from the shared 30 June day); policy dated 20 Nov 2026 yet uses data to 30 Dec.
5. Carried from pass 1 (not re-tested in r2 beyond hours reproduction): DST dates and export clock unstated; KR-2624-type unregistered project rows.

## Next action for the author
Add the 2026 cutoff to solution step 6 (inbound completes started in 2027 are excluded, 26 in all) and the job scoping of the appointment link; no change to files, prompt or goldens. Consider a few words closing the pooled-reference fork on the prompt only if it stays a WHAT.
