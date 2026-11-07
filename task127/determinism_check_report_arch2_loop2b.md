# determinism-check report, task127, 2026-10-16 (re-cut pass, loop 2b)

Judge thread run on the re-cut pack (right-skewed waits; packages 508/350/120/222/0, total 6,723 bed-days). Supersedes the cut-1 verdict in determinism_check_report_loop2.md for values and asks.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (no fix required; one optional prompt pin below)
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The fund note (sections 2 and 4) values a package at the nights it would have shortened a covered patient's stay and says a package removes the wait for a care provider to start. ices_export_notes.txt says hospital-discharge equipment is needed from the day the patient goes home; the ICES orders show no pathway-1 patient left before delivery. Valuing a package from the later of ready date and delivery gives 6.20, 5.83, 5.18, 4.09, 3.21 (RM, WB, HI, CP, AV). With caps 508/350/120/285/361 and 1,200 packages the split is 508/350/120/222/0, all values distinct, no ties. 

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Covered patients (1,624) | 508/350/120/285/361 | same; latest vs first submission identical | yes |
| Equipment join (Hospital discharge, spaceless NHS no., required_by = ready date) | 820 orders | 820 (794 delivered, 26 cancelled); order-in-stay join gives same 820 | yes |
| Nights saved per patient | 6.20/5.83/5.18/4.09/3.21 | 6.2047/5.8314/5.1833/4.0912/3.2105 | yes |
| Naive nights after ready | AV 10.68, CP 10.01 | same; 10,461.07 bed-days | yes |
| Bed-days | 3,152/2,041/622/908/0, 6,723 | same, unrounded 6,723.25 | yes |
| Referrals <=7 days (Marchford/Ashby/Teme Valley, Dec/Jan/Feb) | 194/222/171; 58/54/56; 95/109/94 | same (825 of 825 spot joins; 24-hour timestamp reading identical) | yes |
| SVG patients delayed (15 cells) | e.g. AV 294/292/256, RM 376/400/356 | all 15 | yes |
| SVG bed-days (15 cells) | total 23,554 | 13 of 15 cells by the golden's rule, 23,552 of 23,554 nights; RM Dec 2025 (1,880) and AV Dec 2025 (1,952) were one lower (1,879 / 1,951) on a strict ward_start <= midnight < ward_end join | yes, with the two boundary cells below |

**Boundary cells, resolved after the verdict.** The two strict-join cells came from two ward stays ending exactly at midnight with the next ward starting minutes later (RM spell 16147142, ward_end 2025-12-05 00:00, next ward 01:17; AV spell 27345888, ward_end 2025-12-08 00:00, next ward 00:44). After the verdict the generator closed every gap that holds a midnight, including one starting on it, and checks.py now asserts that the strict point-in-time join reproduces all 15 bed-day cells. No graded figure moved: figures.json is identical apart from the assertion count (now 28,057). This post-verdict generator change was not re-judged; it removes the only strict-join discrepancy the thread found and leaves the golden values as the thread already confirmed.

## Competing answers that survived
- Naive nights after ready (AV 361 first, 10,461): rejected by the fund note's own definition and the delivery evidence; this is the intended trap, not a fork.
- Brokerage "took" population: Started plus spot-start Closed (golden) vs a narrower "provider took" reading (Ashby 46/41/49, Marchford 164/204/141, Teme Valley 85/94/86). Golden judged more defensible; residual risk on 9 cells (SA5 only).
- "Patients delayed": golden = distinct spells with at least one delayed night in that hospital and month; alternatives (by discharge month AV Dec 221, by ready-date month 239, by discharge-site attribution 279) differ. Residual risk on 15 figures; optional prompt pin below.
- Bed-days at discharging site rather than ward at midnight (AV Dec 1,870 vs 1,952): rejected by the ward-stays file and the census note ("the census date is the date the night begins").

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | >=10 / >=3 | 16 / 4 (csv, txt, xlsx, pdf) | yes |
| Large file | >=25,000 rows | 138,606 (ward stays), 65,554 (discharges) | yes |
| Distractors | >=2 named in metadata, none in a file name | weekly return, bed census, reablement outcomes; names do not label them | yes |
| Distractor relevance | unused, weighs, ruled out by shipped fact | weekly return carries the naive nights after ready (AV 10.68, CP 10.01); ruled out by the fund note's package definition and the delivery data | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both present | yes |
| Asks | multi-dimensional, unit and rounding | 9-cell district x month grid, 15-cell hospital x month chart with two measures; whole numbers stated | yes |
| Prompt shape / rubric >=25 | shape 05 allocation; >=25 | shape named in metadata; gradable figures far above 25 (rubric itself generated later) | yes (inferred) |
| LLM-read / realism | none | thread found system-extract mess, no authoring disclosure; row counts match data_request_log.csv | yes |

## Gate G reconciliation
Thread: decomposition_attribution / analytical_non_defect / no / no. Card (.claude/skills/fingerprint/cards/task127.json): stump_class analytical; analyst_test = value a package at nights after the ready date, filling Ashby Vale and Cleeve Park first; domain_test = counterfactual length of stay with one discharge dependency removed. Design note (Three rules, Decisive step): counterfactual saving from the later of ready date and equipment delivery, sole defect none. All match. The declared distractor (weekly return) supplies the naive figure but does not carry the task: the same naive number comes directly from the discharges file, and the call stays hard with the return deleted. Thread's caveat: borderline against single_conceptual_flip, since the filed estimand is itself the lens; live runs should confirm it is attribution and not mere discovery of the ICES file. A matching reading, not a mismatch.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the design note and the card. Residual note from the thread: the fund note and extract notes never tell the solver to join the equipment file, which is what keeps the easy route live (analytical, not a withheld rule, because the estimand "nights by which a package would have shortened the stay" is filed).

## Stump power (Gate F)
Moderate to high. The easy route is a clean number (nights after ready, shipped in the weekly return) that flips the headline: Ashby Vale from 0 to 361 packages, 10,461 bed-days against 6,723. Asks add silent traps: resubmissions, mixed date formats, ward-at-midnight, spot-purchase care starts, postcode normalisation.

## Findings, ranked
1. Optional: pin "patients delayed" in the prompt (patients with at least one delayed night in that hospital and month). Files the WHAT, closes a 15-figure residual fork, costs a rerun and a prompt change; not required for the verdict.
2. Residual risk on the 9 brokerage cells ("took" population).
3. The two boundary chart cells are closed in the generator (see above); the post-verdict change is covered by the new checks.py assertion, not by a fresh thread.

## Next action for the author
Ship on this verdict. If the optional pin on "patients delayed" is wanted, apply it in prompt.txt and re-judge once under /fix-determinism; otherwise proceed to stage 5.
