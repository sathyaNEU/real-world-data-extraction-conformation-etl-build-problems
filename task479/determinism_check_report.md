# determinism-check report, task479, 2026-10-21

Filed as evidence for the spent architecture 1 (the coordinator is re-rooting it because a stage 4 leak reader landed the call). One pass, one sonnet/medium thread; verdict at /tmp/determinism-check-task479-1792540801/verdict.md.

## Verdict
NOT_DETERMINISTIC (confined to supplementary Ask B, answer 5; main call, Ask A, the rate table and the CSV totals reproduce)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution / counterfactual exposure replay, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The pilot set (Wickmere, Amberjack Bay, Thornock, Lisgrove, Saltreach; Eastmarsh next) is forced: guidelines 3.1 read literally means replaying each claim against the present floor, and every replay threshold from any water above the floor to 3 inches gives the same five and the same sixth. Ask B is not forced: the Properties sheet has a column named `federal_share` whose sum differs from the golden's approved cost x project cost-share (Amberjack Bay $6,541,496 vs $6,681,525; Hensby $6,456,591 vs $6,244,320), and nothing filed says that column is unusable.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Elevated insured buildings | 11,060 | 11,060 (policy history, building coverage, LFE >= BFE on 30 Sep 2026) | yes |
| Building-years total | not stated | 162,471.1 | n/a |
| Rates, 14 counties | 2.6, 2.6, 2.8, 3.0, 3.0, 3.7 ... 23.0 | 2.60, 2.60, 2.79, 3.00, 3.01, 3.71 ... 23.01 | yes |
| Replayed claims (CSV) | 1,395 on 1,330 buildings | 1,395 on 1,330 | yes |
| Dunholme 352, Kettlemoor 276 (2016 replays) | 352, 276 | not separately extracted; their rates reproduce | partial |
| Ask A (answer 4), 14 counties | claims and dollars | exact, with the prior_policy_number merge (549 records) | yes (merge unwritten, minor risk) |
| Ask B counts and cost x pct dollars (answer 5) | as golden | reproduce under the golden's own method | yes |
| Ask B dollars under `federal_share` column | as golden | differ by county | no (fork) |

## Competing answers that survived
1. Ask B dollars: summing Properties.federal_share (even split of the project obligation for 148 of 184 projects; 487 properties exceed their approved cost) against approved cost x project cost-share percentage. Not closed by any shipped text.
2. Ask B "not completed": Properties status "Under construction" (stale for 93 properties on projects approved before 12 January 2026) vs no Final inspection passed by 30 Sep. Status-based gives Amberjack Bay 41 buildings instead of 35. The rule is supported only by status_date vs inspection dates.
3. Ask B county key: 37 properties where the applicant county differs from the county of the property's community; the prompt says only "for each county".
4. CSV "paid building claims as it stands": window unpinned; replayed 2001-2025 gives 1,395, actual claims or including 74 paid claims of 2026 losses give other counts. The golden follows guideline 3.1 and is defensible.
5. Not a surviving fork on the main call: claims as filed gives Wickmere, Lisgrove, Thornock, Ravensholt, Hensby, which ignores "as they stand".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, xlsx, pdf, txt | yes |
| Large file | 25,000 rows or more | policy history 117,772 rows (claims 37,859 and 22,301) | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | 3: CRS classes, FIRM revision log, property-building crosswalk; names do not label them | yes |
| Distractors unused yet weighable | unused, a shipped fact rules each out | declared reasons in metadata (class/discount, map revisions, property join); the judge flagged the outreach pdf, CRS and FIRM log as unused; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | all | 14-county asks, units and rounding in the prompt's last sentence | yes |
| Prompt shape, rubric 25 or more criteria | identifiable, 25+ | shape identifiable; rubric not in the folder, not counted here (14 counties x several figures plus 11,060-row CSV makes 25+ plausible) | not verified |
| Reads as real, not LLM generated | yes | judge found no disclosure and a real operational extract feel; golden realism not re-read by me | yes (judge) |

## Gate G reconciliation
Thread: analytical_non_defect, surface_read_dependency no, sole_data_defect no, mechanism counterfactual exposure replay. Design note: stump sentence is the same replay (default path drops pre-elevation claims and puts Dunholme and Kettlemoor in; claims as filed is the other wrong route). Match. The declared distractors are not named as carrying the task. No mismatch.
Gate H: domain pass, layers pass, decisive_step analytical. Matches the note's Three rules (domain test: flood loss avoidance replay of a mitigated building). Layer 1 (2023 layout change, UTC, NGVD29/NAVD88, re-entered NFIP Direct claims) does not carry the stump.

## Stump power (Gate F)
Moderate. The guideline wording "would bring ... as they stand" and the filed 365.25-day, datum and condo definitions pre-announce the estimand, so a strong model reading the PDF literally will likely replay. The thread reached the golden by that literal reading with no further judgment, so this is the textbook-route case: the main thread should weigh it with the scored readers' result. This is consistent with the stage 4 leak reader landing the call, which is why architecture 1 is being re-rooted.

## Findings, ranked
1. Ask B answer 5 is not determinate: dollar basis, completion test and county key all unfiled (FIX_NOW).
2. CSV claims window ("as it stands") is unpinned; the golden is defensible but unwritten.
3. Ask A's prior_policy_number merge (549 records) is forced by the data but unwritten (minor).
4. Stump power moderate: literal reading of the guideline reaches the call.

## Next action for the author
File the WHAT for Ask B in the data dictionary or prompt in one pass (a property's federal share is its approved cost times its project's federal cost-share percentage; a property is completed once a Final inspection has passed; a building belongs to the county of its community) and the CSV window (losses 2001 to 2025). Do not touch the main call, the ladder or any graded rate. Note the architecture re-root makes this repair moot if the build is redesigned.
