# Determinism review, task196 (judge thread, fresh unzip md5 58fea759d25de0f25cd583ff70449695)

Order kept: yes. My derivation was written to disk
(/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task196_derivation.md) before the graded blocks were opened.
Consequence worth knowing: that derivation did NOT reach the submitted call. I had filed fund_return_requests.csv as a
distractor and landed on 25 per million (count about 560). I reached 31 / 688 only after opening the blocks, then reproduced it.

## Verdict
NOT_DETERMINISTIC (taxonomy: underspecified_objective), on two supplementary asks, not on the main call.
Main call: forced and correct (31 per million, 688 indexed cases), with named residual risks below.
Disposition: FIX_NOW. Pin the population of the recovery-share ask and the count basis of the notified-cases ask in the prompt wording, and
qualify the indexed case count in the golden. Main call, pack and stump untouched. Any run graded on the old ask wording is graded on different text for those two asks only.

## Gate table
| Gate | Result | Line |
|---|---|---|
| A | PASS | Every graded figure reproduces (index 31/22/15/12, counts 400/395/125/270/157/288, 688/139/301/517, indemnity grid and quarter totals, notified grid, recovery shares) once each ask's population is the one the golden uses. |
| B | PASS (note) | Every deciding fact is in the pack. The mechanism that makes 125 matches self-caused (a return request prompts the holding firm to register) is stated in no sentence; it is evidenced by the data: registration falls 1 to 40 days after the request in 125 cases and 20 to 172 days before it in 95, nothing between, no ties, same pattern for peers. |
| C | FAIL (asks 5 and 6) | Main call survives. Recovery ask: four populations are licensed by the sentence and give different grids. Notified ask: row count vs distinct case_reference differs on four members. See below. |
| D | PASS | Main call separates on analysis (independence of the two sources), not on a word. |
| E | FAIL (asks 5 and 6) | "cases closed in each 2025/26 quarter" does not say scam cover or scheme year 2025/26; "cases each member notified" does not say rows or distinct references. |
| F | STRONG | Easy routes file 18 (record), 23 (record plus register-found), 25 (two-source on all 395 matches), 26/35 (peer pooled recall), 51 (drop every request). Only 31 uses the request dates. No hardening lever needed. |
| G | PASS | see line |
| H | PASS | see line |

Gate G: mechanism: statistical_rigor (dependence between the two sources of a two-source estimate; method choice on honest data); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. The reported 400 and 395 are right; the estimator's independence assumption is what breaks, a feature of how the data arose, not a defect to catch.
Gate H: domain: pass; layers: pass; decisive_step: analytical. Layer 1: padded vs unpadded account refs, preliminary vs revised returns, thousands vs units, two register layouts, main plus supplementary feeds. Layer 2: multiple-systems estimation of cases the record missed, with the dependent sightings removed. Swap test fails to preserve the task (it is an undercount estimate, not a list check). Easy route a strong analyst takes after cleaning everything: two-source estimate on all 395 matches, 400 x 395 / 282 = 560 cases, 25 per million.

## Evidence, main call (all recomputed from the pack)
Castlegate payments 22,233,300 (revised). Recorded 400 (register, payment-year basis; returns' 338 omit 62 notified after 31 March). Matches 395 (282 recorded, 113 not). Padding the account number changes no join (all 6,994 matches join after padding, all status reported). Fund-return request preceded registration on 125; independent 270, of which 157 recorded. 400 x 270 / 157 = 687.90, 30.940 per million. Walk 17.991 / +12.949 / 30.940 prints 18 / 13 / 31. Group: Saltmarch 139.28 / 21.88 (22), Trentmoor 301.44 / 15.07 (15), Brindlemere 517.37 / 12.11 (12). Clean split rule: strict or non-strict "request on or before registration" gives the same 125 (no ties, no values within 20 days either side).
Surviving alternatives on the main call: peer-pooled independent recall (0.307 vs Castlegate 0.3925, z about 3.4, so the data reject pooling) gives 767.75 / 34.5 (35); dropping every request gives 1,129 / 50.8. Both are weaker readings; I do not count them as surviving. Residual risk, not a failure: the index carries sampling error of about plus or minus 1.8 per million on 157 of 400; every solver who uses the member's own two-source form lands on 31.

## Item 1, the indemnity ask (the earlier defect)
Sentence: "unauthorised-fraud indemnity the advices settled, by member tier and the 2026/27 quarter each case closed in, totals unrounded."
Bases and grains enumerated:
- Case grain (indemnity_paid_gbp) by register closed_date quarter, all advice lines: A 389,667.22 / 349,939.20 / 343,190.44 / 339,633.35; B 390,380.41 / 277,917.53 / 237,744.26 / 181,103.67; C 204,473.45 / 101,819.98 / 92,670.03 / 75,823.30 (total 2,984,362.84). This is the golden.
- Same, by the line's settlement_month quarter: numerically identical (the 35 repeat lines carry the case's original month).
- Same, one line per case (35 repeat lines, 486,513.00, dropped; equals register reimbursed): A 311,087.84 / 309,881.88 / 317,028.59 / 339,633.35; B 271,791.35 / 228,966.01 / 222,672.81 / 181,103.67; C 81,499.33 / 83,191.04 / 75,170.67 / 75,823.30 (total 2,497,849.84).
- Advice grain (advice_total_gbp) by advice month: A 311,087.84 / 369,083.02 / 348,469.17 / 393,790.18 etc. Cannot be split by the case's closing quarter, so the sentence excludes it. Lines sum to advice totals to the penny and match the advice's stated case_lines.
- Tier: advices and register agree for all 12 members; Wrenhall is A in both ("held from the 2024 review"); the volume rule would make it B and is rebutted by tier_basis. Scheme quarters share calendar boundaries, so only labels could differ.
Survive the sentence as written: 1 grid (the golden). The old two-grain problem is gone: both advice fields sum to the same total, and the closing-quarter wording admits only the case-grain field. Residual: a solver who treats the 35 repeat lines (amounts up to 2,000 times the case's reimbursed amount) as errors gets the third grid; "the advices settled" and the advice's own case_lines and total make that a departure from the sentence, so I rate it forced with that named risk.

## Item 2, the indexed case count in the call sentence (ruling)
Count under every licensed form, Castlegate (index in brackets): two-source R x n / k 687.90 (30.94); Chapman 686.79 (30.89); Bailey 686.08 (30.86); R + U / own recall pooled over 2 years 688.10 (30.95); over 3 years 688.56 (30.97); quarter-stratified 688.46 (30.97); firm-type stratified 687.55 (30.92); channel stratified 687.79 (30.94). Rounded counts: 686, 687, 688, 689. The index is 31 under all of them. Other members spread the same way (Trentmoor 300.67 to 301.44; its golden 301 sits 0.06 case from the 301.5 edge under the plain form).
Ruling: the shipped text does not force one form (standard 4.2 says only "estimated on the evidence base"), so the count is NOT determinate to the case. It is NOT a Gate A failure (688 reproduces exactly under the form the golden names) and NOT a Gate C failure on the call as the prompt asks it, because the prompt asks for the index per million and the walk per million, never a count, and the index is invariant at 31. It is a precision claim the files do not force, sitting in the committed recommendation and in the deliverable answers (688, 139, 301, 517, 288). Do not cut it from the frozen call; the call sentence is golden text, not solver-facing, so qualifying it costs no stump and no rerun. Fix: state the form beside the count ("688 on the two-source estimate, 400 x 270 / 157") and have the rubric accept 686 to 689 (Trentmoor 300 to 302, Saltmarch 138 to 139, Brindlemere 516 to 517, not-held 286 to 289). If the author prefers to leave the call word for word, that is acceptable only with that tolerance in the rubric.

## Failing asks
Ask 6, recovery share (Gate C and E, underspecified_objective). Sentence: "share of reimbursement recovered by route on cases closed in each 2025/26 quarter, from case-level credits." Golden population: scam reimbursement cover, register scheme_year 2025/26, closed in the quarter, denominator register reimbursed_amount (it equals recovery_statement reimbursed_in_quarter to the penny, so the population is recoverable only by reconciling the statement the sentence tells the solver not to use). Literal alternatives, Q1 / Q2 / Q3 / Q4 beneficiary recall and route totals recall, repatriation, insurer:
- golden (scam, scheme year 2025/26): 6.5 15.1 8.5 5.4; totals 8.5, 2.7, 6.0
- all cases closed in the quarter, both covers: 8.6 10.0 7.2 5.4; totals 7.7, 3.5, 4.6
- scam cover, any scheme year: 9.9 11.7 8.1 5.6; totals 8.6, 3.4, 4.8
- payment_amount denominator, both covers: totals 7.2, 3.3, 4.4; credits dated inside 2025/26 only: totals 6.7, 2.9, 4.3.
The sentence names neither cover nor scheme year; the first reading most solvers take (closed_date in the quarter) is not the golden.
Ask 5, cases notified (Gate C): feed plus supplement rows give 193 / 121 / 109 / 93 for KM-101, 102, 104, 110 (equal to the revised returns); distinct case_reference gives 191 / 120 / 108 / 92 (the dictionary says a case is one case however many legs it covers; the repeats carry different payment and notified dates). Values are identical either way. Second, weaker risk: the register also holds 457 cases notified April to June 2027 (Castlegate 62 scam, 7 unauthorised) that are not in the feed.

## Item 3, distance from rounding edge (fraction of the stated unit; none prints round, none on a tie, all computed from pence or whole counts)
Index: Castlegate 30.940 (0.44), Saltmarch 21.879 (0.38), Trentmoor 15.070 (0.43), Brindlemere 12.110 (0.39). Walk lines 17.991 (0.49), 12.949 (0.45), total 30.940 (0.44).
Counts: 687.90 (0.40), 139.28 (0.22), 301.437 (0.063, nearest to an edge), 517.37 (0.13), not-held 287.90 (0.40).
Indemnity cells in pounds: closest 277,917.53 (0.03), 204,473.45 (0.05), 343,190.44 (0.06), 390,380.41 (0.09); others at least 0.15; quarter totals 984,521.08, 729,676.71, 673,604.73, 596,560.32 (0.18 or more).
Notified values: closest 153,759.53 (0.03), then 285,422.35 and 26,336.35 (0.15); rest at least 0.17.
Recovery shares in units of 0.1: closest Q4 recall 5.4461 (0.039, 0.004 points from 5.45), Q3 insurer 5.8579 (0.079), Q1 insurer 2.8365 (0.135), Q1 repatriation 3.3668 (0.168); route totals 8.5287, 2.7067, 5.9686 (0.21, 0.43, 0.19). No exact tie anywhere.

## Figures that did not reproduce
None as submitted. Under the literal readings above, ask 6 reproduces only on the scam / scheme-year-2025/26 population (my own pre-blocks derivation gave 8.584, 9.994, 7.225, 5.402 for recall), and ask 5's counts for KM-101, 102, 104, 110 reproduce only on rows (I derived 191, 120, 108, 92 as the dictionary-literal count). My pre-blocks main answer was 25 / 560, not 31 / 688.

## Hygiene (brief)
19 files; formats csv, xlsx, pdf, txt (4); mule_account_register.csv 28,394 rows; distractors present (national statistics, AML alerts, recovery statement). Dates coherent (feed notes and pack 2 July 2027, register to 30 June 2027). Licence and provenance records not in the pack, not checked. No authoring language seen in the notes or PDFs read. No exclusion-level finding.

## Fix
prompt: ask 6 add the population ("scam reimbursement cases from 2025/26 payments, by the quarter each closed in"); ask 5 add the count basis ("a case counted once however many legs"), or accept rows and say so in the golden if rows is kept. solution: qualify the indexed counts as above, rubric tolerance 686 to 689.
