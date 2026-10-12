# determinism-check report, task449, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (one hygiene item, no analytic change; no re-judge needed for the figures)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The WPS-3 literal reading (Mon 3 Aug to Sun 27 Sep 2026, merged duplicates out, Schedule 7's four codes, 27.5 per analyst-week, round up) gives one answer on every committed figure. The only judgment step is the share of name-and-city matters arising from the failure. It is pinned by the 597 single-cardholder searches (478 affected, 80.07 per cent), and the dilution inversion against the 4.0 per cent portfolio rate agrees (0.79 to 0.81 for k up to 20). The rounded 500, 950 and 35 hold at portfolio rates of 3 to 5 per cent. All six committed answers reproduce. Thread: general-purpose, sonnet, medium, scratch /tmp/determinism-check-task449-r1/.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| New matters in window, merged out | 11,597 (1,450/wk) | 11,597 (1,449.6) | yes (matters, opened_at/status) |
| Four-code verified, account on Meridel list with posted date | 2,081 | 2,081 | yes |
| NAME_CITY four-code matters | 2,395 | 2,395 | yes |
| k=1 matters, affected | 478 of 597, 80% | 478/597 = 80.07% | yes |
| Failure matters a week | 500 | 499.8 | yes |
| Sustained base | 950 | 949.8 (34.5, up to 35) | yes |
| Month-end open Jan to Sep | 720,730,710,740,8260,5590,3230,2230,1850 | 721,728,710,739,8260,5589,3232,2232,1849 | yes, rounded |
| Flex hours Jan to Sep | 790,670,760,720,3430,4120,3440,2830,2170 | 791.5,671.75,761.25,721.5,3431.75,4121.25,3441.5,2831.75,2171.25 | yes, rounded; no boundary at a 5 |

## Competing answers that survived
None that are equal readings.
- Attached account at face value: 370/wk, base 1,080, 40 analysts. Ruled out: data dictionary says the account is the first of k returned (this is the default-path trap, not a fork).
- VERIFIED-only (confirmed account) as "covered": 260/wk, 44 analysts. Mild residual reading fork; Schedule 7.2 defines covered by the cardholder's account, 7.4 only the claim mechanic, and the prompt says "arose from". Closed in the design note's SF1(c).
- Inversion with b = 0: 516/wk, 34 analysts. Separated by the portfolio rate and the k-gradient in the data.
- Month-end from register closed_at: wrong by the status-history event log.
Thin spot (not a failure): asks 2 and 3 are estimates with about +/-10 a week sampling error; 500 and 950 hold across the n=1 route and the pooled inversion.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 4 (csv, pdf, xlsx, jsonl) | yes |
| Large file | 25,000+ rows | 77,145 register, 159,488 history | yes |
| Distractors | 2+ in metadata.json, none named in a file name | ivr_complaint_line_weekly_2026.csv, cfpb_public_complaints_bellcroft_card.csv; neither file name labels one | yes |
| Distractor weighs, unused, ruled out by a shipped fact | yes | both relevant to complaint volume and unused by the solution; neither carries the call (judge found no contamination). Not independently shown to reproduce a graded quantity | yes, light |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | nine-month series, base, share; one blanket rounding sentence in the prompt (nearest 10, analysts exact) | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape "other" in metadata; rubric not generated or checked here | not verified |
| Reads as real, not LLM generated | yes | judge: system-like mess (mixed dates, h.mm hours, re-sent export) | yes, with the flag below |
| License and source recorded | yes | CC0-1.0, dated, per file | yes |
| Hygiene | no file postdates the folder date | marlowby export_id MSX-20261010 (15 rows, week ending 3 Oct) postdates folder date 9 Oct | NO |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card/note: stump_class analytical, generators G17 first (statistical rigor), G3 second, gate_g method_or_model_selection, official_decoy false, no decisive rule filed. These match. The declared distractors (IVR, CFPB) are not named by the judge as carrying the task, so they are not too load-bearing. The judge's easy route (attached account at face value, 40 analysts) equals the note's default path (about 1,085 base, 40), and its imputation route (34) equals the note's R2. No mismatch. One borderline the judge notes: on clean attachments the call reduces to a join, but the attachment structure is native and documented.
Gate G line: PASS (no shipped artifact ranks the candidates wrongly; surface read does not carry the task).

## Gate H line
domain: pass (contact-centre workforce planning; incident-share estimate and sustained base are the field's quantities); layers: pass (Layer 1 Eastern/UTC, h.mm hours, re-sent export, reopens; Layer 2 the incident share behind first-of-k attachments); decisive_step: analytical (estimating the true share from single-result searches or by inverting the dilution). Agrees with the note's Three rules and card.

## Stump power (Gate F)
High on the main call: the easy join files 370/wk, 40 analysts and the matching 370 and 1,080 asks; the imputation route files 34. Flex-hour asks add h.mm hours, a re-sent export and Wrexley exclusions; the month-end replay adds reopens. The 45-point call bank per CLAUDE.md is held to one correct response by the estimate, not by a rule.

## Findings, ranked
1. Hygiene: marlowby_timesheets_fenwright_2026.csv export id MSX-20261010 and its week ending 3 Oct postdate the 9 Oct folder date and the 2 to 3 Oct as_of. Shift dates are 28 to 30 Sep, so no figure moves. Fix the export id and week metadata in the generator.
2. Optional: asks 2 and 3 are estimates (+/-10 a week); a one-step tolerance in grading would remove residual risk.
3. Residual mild reading fork on "covered" (VERIFIED-only, 44); closed in SF1(c), keep the closure asserted in checks.py.
4. Rubric size (25+ criteria) was not checked by this pass.

## Next action for the author
Change the Marlowby export id and week-ending metadata that postdate 9 Oct in the generator, rebuild twice byte-identical, and re-ship; no figure or golden changes.
