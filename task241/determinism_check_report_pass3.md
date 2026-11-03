# determinism-check report (pass 3), task241, 2026-11-03

Judge run r3, scratch /tmp/determinism-check-task241-r3/. Prompt now 740 characters (pass 1 had 702); target.zip 24 files.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
All four committed ask blocks and the main call reproduced with zero differences. Six off (KR-2607, 2622, 2631, 2638, 2644, 2651), seven on. Nearest shares to the 10% line are KR-2633 at 5.7% (on) and KR-2631 at 16.8% (off); verdicts hold for every window 2 to 120 min from call start or end and under month, hour, state, weekday and pre/post-July stratification of the calibration. Callback gaps are bimodal (7,085 within 2 min, 8,843 over 150 min). The 2025 audit, Larkspur certificate and raw callback rate are scoped or incomplete evidence and force no rival answer. The previous pass's interview mismatch is closed: the 26 inbound completes dated 2027 are excluded as outside 2026 (the judge now applies the cut, giving 1,380 inbound completes).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Dialer calls | n/a | 281,622 after 10,273 repeats | yes |
| Shares (13) | 3,18,2,4,3,20,4,17,6,18,32,2,29 | 3.1,17.7,...,16.8,...,5.7,17.8,31.9,...,29.2 | yes |
| Calling hours (13) | 181,193,76,175,110,120,147,186,125,178,85,198,124 | identical (start or answer time; >=21:00 or >21:00 same) | yes |
| Interviews (13) | 3488 ... 1971 | identical with 2027 completes excluded | yes |
| Interviewer hours (13) | 9,114.6 ... 5,418.5 | identical | yes |
| Pilot KR-2604 vs 2025 audit | 3% vs 9 of 400 | 3.1% vs 2.25% | yes |

## Competing answers that survived
1. Pooled calibration (about 0.29): KR-2631 reads about 5.6%, on, so five off instead of six. The policy's "on that project" wording and shares "measured on its own calls" close it; the only verdict that flips, judged reasonable but unlicensed.
2. "Answered calls" in the hours ask: every export row has an AnswerTime, so all rows are answered (policy section 3 uses it the same way). The "answered by a person" reading gives lower counts (175, 146, ...). Low risk.
3. Disp letter codes have no legend; fixed by structure (A machine-classed never connects, X live answer no agent, C longest talk and the only SUP code). Low risk.
4. Estimator choice (audit, certificate, raw callback share all give "all on"): closed by the data, not by a filed rule.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 24 | yes |
| Formats | 3 or more | csv, xlsx, docx, pdf | yes |
| Large file | 25,000 rows | 128,940 (case records) | yes |
| Distractors | 2 or more named, not in file names | invoices, QA scores, consent log named in metadata; Larkspur and audit also weighed | yes |
| Deliverables | 1 to 3 | xlsx and pdf | yes |
| Prompt | one paragraph under 1,000 chars | 740 chars, one line | yes |
| Rubric 25 or more | yes | design note states it clears 25 (not recounted) | yes (stated) |
| Not LLM-generated | yes | operational artifacts, no authoring language, hidden content or tracked changes | yes |

## Gate G reconciliation
Class: clean. The judge's stumping type matches the card and design note (stump_class analytical; default path the certified 2.1% and 2.25% audit, ending on no project). The declared distractors do not carry the task. Gate H: domain pass, layers pass, decisive_step analytical (calibrate callbacks on machine-classed calls against each project's own known-person callback rate). Judge notes the swap test does not substitute. Judge's one caution: borderline only in that the solver must see the audit does not cover the other projects, a scoping argument rather than a defect catch.

## Stump power (Gate F)
Moderate to good, resting on one analytical trap. Extending audit or certificate to all projects, or reading the raw callback share (max 8.2%), files "all on". A solver who finds the callback signal but pools the calibration flips KR-2631 (raw 1.62%, its own known-person callback rate only 9.6%). Asks add failure points (time zones with the pre-July case chain, inbound completes, hours by call mix). Main thread should weigh against the ladder that a strong model reading every file may build the ratio unprompted.

## Findings, ranked
1. None blocking. Reproduction is exact on all 52 ask cells and the call.
2. Optional pins (each changes what solvers see): define "answered calls" as every dialer export row; add a Disp-code legend. Only if a grader flags them.
3. Minor temporal oddities: policy issued 20 Nov 2026 and register modified 4 Dec 2026 against dialer data to 30 Dec and inbound to 6 Jan 2027; audit job KR-2511 tied to KR-2604 only by project name. Non-decisive.

## Next action for the author
No repair. Proceed to ship checks; the optional pins are not needed for determinism.
