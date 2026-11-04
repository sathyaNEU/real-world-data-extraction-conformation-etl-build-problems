# determinism-check report, task313, 2026-11-04 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: other (transport of a trial effect to the readmissions a referral can still reach, with ETL linkage), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet medium thread on a fresh unzip (sha256 of target.zip 79a5e3bb...f71df32), brief at /tmp/determinism-check-task313-799078/judge_brief.md, verdict at /tmp/determinism-check-task313-799078/verdict.md. Pass 1's content was not shown to it.

## Why
Executed literally, SS-MAT-027 sections 3, 4, 5, 7 and 8, the trial report and the linked files give posts 7/9/6/3/5 and about 325 readmissions avoided. Reachable readmissions per unit are 132/166/109/62/91 (560); 57 per cent of 560 is 319.1, inside the 325 band (312.5 to 337.5). Remainders .90, .88 and .84 take the three extra posts; the next is .32, so no tie. Receipt-only timing gives the same posts (321 avoided). The pooled 0.43 holds on the mapped and the published counts.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Eligible babies (5 units) | 2,803 / 2,419 / 1,908 / 1,514 / 1,639 | same (RK csv + 3 SW sheets, twins kept, 24 blank NHS numbers via MPI) | yes |
| Eligible readmissions | (easy route 180/168/111/86/101) | 180/168/111/86/101 = 646 | yes |
| Reachable readmissions | not stated | 132/166/109/62/91 = 560 | yes |
| Trial cut | 57 per cent | 56/2,092 vs 134/2,134, RR 0.426; published counts 46/108 also 0.43 | yes |
| Posts | 7/9/6/3/5 | 7.07/8.90/5.84/3.32/4.88 shares, largest remainders 7/9/6/3/5 | yes |
| Readmissions avoided | 325 | 319.1 (to nearest 25: 325) | yes |
| Ask 3 rate, RR | 8.5/0.35, 6.1/0.63, 6.6/0.40, 6.9/0.24, 7.9/0.51, 6.2/0.54 | exact 8.4906/.3516, 6.0698/.6337, 6.6002/.3968, 6.8627/.2402, 7.8704/.5108, 6.1644/.5444 | yes |
| Ask 4 visits, calls | 1.80/2.93, 1.24/2.81, 1.20/2.60, 1.51/2.99, 1.46/2.52, 1.33/2.61 | 1.7960/2.9303, ..., 2.6016, 2.9945 (weight loss calls) | yes |
| Asks 1, 2 | match call | match | yes |

## Competing answers that survived
No fork on the main call survives per the thread. Readings 1 to 4, 7 and the main-call side of 6 are closed by files or by data (details in verdict.md). Three readings are open forks on the asks only, as the coordinator asked:

- **Reading 5, risk ratios from rounded rates (Ask 3).** Open fork, confined to Ask 3. It moves four of the six risk-ratio cells (0.35/0.62/0.39/0.23/0.51/0.55 against the golden 0.35/0.63/0.40/0.24/0.51/0.54: the second, third, fourth and sixth); no rate cell and no main-call figure moves. No file sentence closes it; the design note's SF21 closes it only by the prompt's rounding sentence (round the figures reported, not their inputs), which the thread judged not sufficient. The thread's closure, "risk ratios from the counts, rounded once at the end", states the computation path in plain words in the asking text. It is a rounding convention, not an ask device, and does not touch the main call; it does hand the careful route to every solver, so the author should weigh it against the ask's stump power.
- **Reading 6, mother-filed admissions mapped or unmapped.** Open fork, confined to the asks. Main call unaffected (no mother-filed row touches the five units; RR 0.43 either way, 46/108 unmapped, 56/134 mapped). Ask 3 moves all twelve cells: unmapped usual-care rates 6.6/4.9/5.1/6.4/6.5/4.1 and RRs 0.30/0.67/0.41/0.26/0.54/0.82. Ask 4 moves only through the contact log's calls filed under a mother's number, left unmapped giving calls 1.67/1.53/1.43/1.76/1.45/1.53 (the admission mapping itself does not enter a contacts-per-baby figure). The golden is the more literal reading: SS-MAT-027 section 5 ("emergency admission of the baby"), the rows' P and R diagnosis codes, and the Ask 4 sentence ("telephone calls that reached the family"). The report's published 46/108 reproduces under the unmapped reading, so an anchor on it is a defensible-looking wrong answer. The thread's closure (name the mother-filed rows in the report footnote, or state the trial counts per the spec definition) would put the ask's silent device into shipped text in plain words and would either remove the Layer 1 mess or contradict the report's table; it defeats the device the ask carries. This is the author's call: the asks are free of the determinism-by-silence rule only if the literal text closes them, and the thread judged the sentence plus codes enough ("closed by the specification and the diagnosis codes").
- **Reading 8, rounding ties.** No cell sits on a tie at its stated precision. One near miss: Ask 4 weight loss calls 2.9945 (0.0005 below 2.995). Under a calendar-day reading of the 28-day window it becomes 3.00; readmissions, posts and Ask 3 do not move. Open fork confined to Ask 4, one cell. The natural closure ("timestamp arithmetic, 28 times 24 hours after discharge") would state a window convention in plain words; it is not an ask device. The thread treated timestamp arithmetic as the natural reading and the risk as minor.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv (9), xlsx (3), pdf (2) | yes |
| Large file | 25,000 rows or more | notifications 60,840; MPI 59,808; RK 28,323 | yes |
| Distractors named, none labelled by file name | 2 or more | metadata.json names lmns_maternity_dashboard_2025-26.xlsx and community_midwifery_establishment_2026-10.csv; file names carry no label | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | dashboard (births, rates by unit) and establishment (WTE, vacancies by team) give no arithmetic route to a graded figure; births caseload is the design's rung 0 and files 8/7/6/4/5, ruled out by spec 7 | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 5 asks, 12-cell and 12-cell tables by risk reason; unit and rounding given in the prompt's closing sentence rather than inside each asking sentence | yes (note) |
| Prompt shape and 25 criteria | shape identified, 25 or more | shape 05 allocation to a fixed total; graded cells: 5 posts, total, 12 + 12 table cells, chart, call; rubric itself is generated at portal and not in the package | shape yes, count not checkable here |
| Not LLM-generated, goldens real work products | yes | pack layouts carry realistic mess per thread; golden realism not re-read here (golden-realism gate is separate) | not assessed beyond thread |

## Gate G reconciliation
Thread: mechanism other (transport of the trial effect to reachable readmissions), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump_class analytical, layer2_family estimand_identification, layer2 pattern "a trial effect re-based on the window after each baby's earliest outreach visit", gate_g decomposition_attribution, decisive_rule_filed false, official_decoy false. Match. The thread names no declared distractor as the surface read: the surface read is the trial ratio on every eligible readmission (8/8/5/4/5, about 375), the design's own default path and rung 1. Neither distractor (dashboard, establishment) carries the task.
**Gate G line:** matches the design; no shipped artifact ranks the units wrongly on the decision question; distractors are not load-bearing.

**Gate H line (thread):** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Matches the card's analyst_test and domain_test and the note's Three rules (decisive step: per-baby comparison of two instants held in two logs, after which the trial ratio applies). One divergence of wording: the note says no filed rule ties service start to receipt; the thread says section 4 of the spec (referral through the community midwifery office, which receives the notifications) forces it but "derived, not stated". The thread cautioned that the 08:00 to 19:00 hours rule is recovered from the contact log rather than stated; receipt-only gives the same 7/9/6/3/5, so it is not decisive.

## Stump power (Gate F)
Thread: plausible, mostly on the main call, needing three linkages (admissions to babies through MPI and check digit, UTC to local receipts, hours rule from the contact log) and seeing that Ravensby's and St Aldric's receipts lag (median 27.5 h and 17.8 h against 0.7 h). It did not class the decisive step as a textbook method a strong solver lands; the transport-with-exposure-window step is not the standard route (the standard route is the easy 8/8/5/4/5). The main thread should weigh this against the note's ladder: rungs 2 and 3 (one lag for all units, medians) each file other posts or other totals, which is good separation. The asks add friction through reading 6 (mother-filed rows) and the pooled-effect trap.

## Findings, ranked
1. Reading 1 is ruled out by derivation, not by a stated sentence ("derived, not stated", forced by spec section 4 and the trial report). A real reviewer could read the trial-ratio-on-every-readmission answer as a competing defensible answer. This is the main residual risk; the note's Three rules and the thread agree there is no explicit sentence.
2. Reading 6 is a real open fork on Ask 3 (12 cells) and the call-mapping cell set of Ask 4, with a published-table anchor (46/108) pointing the wrong way. Not on the call.
3. Reading 5 moves four Ask 3 RR cells; closure phrase exists but states the method.
4. Reading 8: Ask 4 weight loss calls 2.9945 flips to 3.00 under calendar days; margin 0.0005.
5. The contact log runs to 1 Nov 2026, after the specification's October 2026 issue; harmless.

## Next action for the author
Ship as is (APPROVE). Optional, author's call: decide whether to leave readings 5, 6 and 8 as silent ask devices (the asks are decoupled from the call and the thread found the golden the more literal reading in each) or add a plain-words pin to Ask 3 only if the regrade risk outweighs the loss of stump power; none of them moves the main call.
