# determinism-check report, task186, 2026-10-13

## Verdict
DETERMINISTIC, SOLUTION_WRONG
**Disposition:** FIX_NOW (solution blocks only; no change to prompt or shipped files; no model rerun)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executing PM-04 literally from the bundle gives Tallis Petroleum, 28 of its 92 examined stations found (30 per cent), none of any other brand. The call held under every reasonable null tried (own non-levy 28-day history, plus-one p, 2025-only or 2026-only null dates, one or two sided, normal z, cross-sectional robust z, Bonferroni). Only the naive daily-variation t-test or a raw margin-rise count leaves it, and those name Harbourline, the intended easy route. Two block defects: Critical Component 1 (369 vs a literal 370) and Critical Component 2 ("every one a station Tallis prices itself" is false for one station).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Stations examined 1 Jan 2026 | 369 | 370 literal (station 59392, Wexcombe Kellow, closed 2 Jun 2025, brand-history row still open); 369 only with an unstated trading-status filter | No (block defect) |
| Stations found, BH 5% | 28 | 28, all Tallis (smallest non-found p 0.021; BH line for the 29th 0.004) | Yes |
| Tallis share | 30% | 28/92 = 30.4% | Yes |
| Other six brands | 0% | 0% each (min p GAR .056, HBL .033, OXB .021, PEL .118, STL .070, WEX .045) | Yes |
| Every found station priced by Tallis | all 28 | 27 of 28; HOL-0120 is a dealer site with 7 POS-only November changes | No (block defect) |
| Stations each brand prices itself, 1 Dec 2026 | 5/15/8/13/9/27/10 | identical; push-share per station is 0 to 0.1 or 0.9 to 1, none between 0.2 and 0.9 | Yes |
| Litres of regular, Jan/Feb/Mar, 7 brands | 21 cells | all 21 reproduce, under: latest revision per reference and month, 8 reassigned references joined by return site address, brand history in the month, QUA-0175 counted in March | Yes |

## Competing answers that survived
- Fork 1, station 59392: 370 examined (literal) vs 369 (golden). No share, call or BH outcome moves (its p is 0.69). Block repair only.
- Fork 3, "stations it prices itself" is not defined in a shipped file (PM-04 4.2 says "stations whose pump prices the brand sets"). site_ownership = Company gives TAL 26, GAR 7, HBL 14, OXB 10, PEL 11, STL 6, WEX 9; any API user gives 104 stations. The push cluster separates cleanly (87 stations at 0.9 to 1, 302 at 0 to 0.1) and the register defines ownership only, so the golden is better evidenced, but the text does not close it. Residual risk on xlsx ask 1 only; the main call is untouched.
- Fork 4, partial-month brand (QUA-0175, WEX, opened 9 Mar): any-day carrying gives WEX March 13,045 (golden); whole-month only gives 12,823. Low risk, one cell.
- Fork 5, the 8 reassigned survey references: joining to the frame holder instead of the return's site address moves every brand's cells (GAR January 12,463 vs 12,405). The return's address and on_frame_since (August to October 2026) support the golden; the extract notes do not say it. Layer 1, resolvable from the files.
- Main call: no competing brand survives. Harbourline (naive t-test or raw rise) is not defensible under PM-04 3.3.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | Yes |
| Formats | 3 or more | 5 (csv, json, md, pdf, xlsx) | Yes |
| Large file | 25,000 or more rows | price change log, 198,744 rows | Yes |
| Distractors in metadata.json | 2 or more, none labelled in a file name | weekly_price_bulletin_2026.xlsx, price_complaints_register_2026.csv; names are neutral | Yes |
| Distractor weighs, unused, ruled out by a shipped fact | each | Thread found both present and unused (also operations log, brand register partly used). It did not test whether either reproduces a wrong graded quantity arithmetically; the author should confirm | Partly confirmed |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx); both in golden/ | Yes |
| Asks multi-dimensional, unit and rounding stated | each | prompt states shares to nearest ten per cent and litres in whole thousands; counts are integers; 7 brands x several cuts | Yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 01 in metadata; about 7 shares + 7 counts + 21 litre cells + call + chart gives well over 25 candidate criteria. The rubric is not built here | Likely, not verified |
| Not LLM-generated, goldens real work products | yes | Thread found no authoring language, tool banners or disclosures. Golden realism not assessed by the thread | Not assessed |

## Gate G reconciliation
Thread: statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump is the empirical null (estimand_identification) against a theoretical day-to-day null; default path ends on Harbourline (92 per cent of its examined stations), golden Tallis. The two agree on the easy route, the wrong answer and the golden. The thread did not name either declared distractor (bulletin, complaints register) as the surface read carrying the task, so no distractor-too-load-bearing finding. No shipped artifact ranks brands on the decision question wrongly. Match: no mismatch.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note `## Three rules` agrees: the decisive step is choosing the null for many simultaneous tests, with Layer 1 as UTC against local time, the renumbering crosswalk, resubmitted batches and revised survey returns. Easy route Welch t-test or raw margin rise gives Harbourline. One caution: the design note's swap line concedes "rewrite with clinics and wait times and the setting survives, as it does in a methods domain". The thread judged the margin-change-against-price-cycle analysis the field's own, so no send-back, but a stricter reviewer could press H1. The standard files BH and the inquiry rule but not the null, so H3 does not fall to rule_application.

## Stump power (Gate F)
High and analytical. A capable analyst's first route flags 194 to 272 of 370 stations and recommends Harbourline. The correct route needs the station's own non-levy 28-day change history as the null plus BH across all stations, and Tallis leads by a wide gap. The asks add independent hard cells (reassigned survey references, push-time pricing, partial-month brand).

## Findings, ranked
1. Critical Component 2 and step 7 wording "every one a station Tallis prices itself" is false: 27 of 28 (HOL-0120 is dealer-priced). The design note line at about 295 repeats the claim. Repair in submission.md and the note.
2. Critical Component 1 says 369 examined; a literal PM-04 3.2 run gives 370 (station 59392 closed 2 Jun 2025 but with an open brand row). Say 370, or state the closed-station exclusion and its basis. No share or call moves. Check that checks.py and figures.json agree with whichever is chosen.
3. "Stations it prices itself" (xlsx ask 1) is an operationalisation no shipped file defines. Residual risk on that ask only. Optional hardening: file the WHAT in PM-04 4.2 or the extract notes (stations whose changes arrive on the brand's common schedule), never the method. This changes what solvers see, so it needs a rebuild and a re-run of the free gates.
4. Low-risk single-cell forks: QUA-0175 March, and the 8 reassigned survey references (extract notes silent).
5. Cosmetic: the register leaves closed station 59392 with an open brand row, which produces finding 2.

## Next action for the author
Edit submission.md (and the design note's matching line): set Critical Component 1 to 370 examined, or state the closed-station exclusion; change Critical Component 2 to "27 of the 28 are stations Tallis prices itself, one (HOL-0120) a dealer-priced station", and fix step 7 and the "every one" wording. Then re-run figures_check and checks.py. No prompt or target change is needed unless you take the optional hardening in finding 3. No second judge pass is required for the block edit.


---

# determinism-check report, task186, pass 2, 2026-10-13

## Verdict
DETERMINISTIC (SOLUTION_WRONG cleared: 369 now reproduces, the Tallis share wording is correct)
**Disposition:** FIX_NOW (prompt only: one clause; main call, ladder, data and solution blocks stay frozen)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
A literal PM-04 run on the rebuilt bundle examines 369 stations and finds 28 at 5 per cent FDR, all Tallis (28 of 92 = 30.4 per cent, nearest ten 30); every other brand is 0, next-smallest p 0.019 (BH q 0.24). The call held under plus-one p, nulls from all, post-2026-only, pre-Dec-2025-only and 2025-touching windows, a pooled null and a same-area-median control. The three pass-1 findings are closed: 369 reproduces, the critical components carry shares, and the memo claim is in the past tense. One open item remains, on xlsx ask 2 only: a station that opened or closed part-way through March (58104, HBL until 15 Mar; QUA-0175, WEX from 9 Mar) can be counted three ways. Golden reading (brand it traded under that month, litres in full) gives HBL 16,563 and WEX 12,851; brand-on-1-March gives WEX 12,636; brand-on-31-March gives HBL 16,374. No file states the rule.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Stations examined | 369 | 369 | Yes |
| Found at 5% FDR | 28, all Tallis | 28, all Tallis | Yes |
| Shares | TAL 30, others 0 | TAL 28/92, GAR 0/45, HBL 0/52, OXB 0/45, PEL 0/46, STL 0/46, WEX 0/43 | Yes |
| Priced by brand 1 Dec | 5/15/8/13/9/27/10 | identical (price_submissions push minutes, 3+ stations, station fractions exactly 0 or 1) | Yes |
| Litres Jan/Feb/Mar, 21 cells | as filed | all 21 identical, no rounding tie within 0.009 thousand | Yes, under the golden month rule |

## Competing answers that survived
- Fork A (xlsx ask 2, HBL and WEX March): the part-month rule above, three readings, two cells move. Closed by no shipped sentence. Repair: one parenthesis in prompt.txt. This is a rule the prompt must state; it is not data-derivable.
- Fork B (xlsx ask 1, "prices itself"): no file defines it; site_ownership (Company) gives a different count (TAL 26/27 pushers 16 Company-owned, 10 Company-owned do not push), but the push pattern is cleanly bimodal in the shipped submissions and refutes ownership. Closed by the data; residual risk on that ask only.
- Fork C (survey, 8 reassigned references): needs address normalisation ("St"/"Street"); derivable from the files. Layer 1.
- Main call: no competing brand survives. Harbourline (raw rise 100 per cent of stations up, Welch t 46/52) is the easy-route wrong answer, not a defensible reading of PM-04 3.3.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | Yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, json, md) | Yes |
| Large file | 25,000 or more rows | price change log, 198,870 rows (I counted) | Yes |
| Distractors | 2 or more in metadata.json, none named in a file | weekly_price_bulletin_2026.xlsx, price_complaints_register_2026.csv; neutral names | Yes |
| Distractor weighs, unused, ruled out by a shipped fact | each | Both present and unused by the solution; the design note says the bulletin ranks nothing on pass-through. The thread did not test whether either reproduces a graded quantity; author to confirm | Partly confirmed |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | Yes |
| Asks multi-dimensional, unit and rounding stated | each | shares to nearest ten per cent, litres whole thousands, 7 brands x cuts | Yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 01; roughly 7 shares + 7 counts + 21 litre cells + call + chart | Likely, rubric not built here |
| Not LLM generated; goldens real work products | yes | no authoring language found; golden realism not assessed by the thread | Not assessed |

## Gate G reconciliation
Thread: statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump is the empirical null (estimand_identification) against a day-to-day theoretical null; easy path ends on Harbourline, golden Tallis. They agree on route, wrong answer and golden. The thread named neither declared distractor as carrying the task. No shipped artifact ranks brands wrongly on the decision question. Match: none.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note `## Three rules` and card (`stump_class: analytical`, analyst_test, domain_test present) agree: Layer 1 is UTC and DST, renumbering, doubled receipts, survey revisions; Layer 2 is the counterfactual margin movement and the empirical null; the standard files FDR and the inquiry rule but not the null, so it is not rule application. Residual caution unchanged from pass 1: the note's swap line is conceded for a methods domain; the thread judged the margin-against-price-cycle analysis the field's own.

## Stump power (Gate F)
High and analytical. Raw margin rise or a Welch t on daily margins names Harbourline (46/52 stations, 100 per cent up); the correct route needs the station's own non-levy 28-day history as the null plus BH. The asks add independent hard cells.

## Findings, ranked
1. Part-month station rule is unstated (Fork A), two litres cells (HBL March, WEX March). Prompt clause needed.
2. "Prices itself" undefined in a file (Fork B); closed by clean 0/1 push data. Optional hardening: file the WHAT in PM-04 4.2.
3. Distractor arithmetic not tested by the thread (author to confirm).

## Next action for the author
Add one parenthesis to prompt.txt (litres counted under the brand each station traded under that month, in full, for a station that opened, closed or changed brand within the month), stay under 1,000 characters, rerun voice-check.py and the free gates. The thread's disposition is no model rerun and solution blocks unchanged; the prompt is a shipped file, so target.zip's bundle need not change but the prompt text does.
