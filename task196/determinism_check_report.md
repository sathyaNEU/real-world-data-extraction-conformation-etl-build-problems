# Determinism review, task196 (re-judge of the repaired bundle)

Pack: fresh unzip, 19 members, zip md5 b857fbef40cc860f9beee3fe78869301.

**Order kept.** My derivation was written to disk (scratchpad task196_derivation.md) before the graded blocks were opened. It is incomplete on the main call: working blind I filed 25 per million for Castlegate (all 395 register matches treated as an independent second source) and never screened the matches against fund_return_requests.csv. I opened the graded blocks only after writing that. Everything below on the main call after that point was then recomputed from the files, not accepted.

**Verdict: DETERMINISTIC.**
**Disposition: APPROVE.** No repair required; a model rerun is not needed. Two soft points are listed under Gate C and E as watch items, neither blocks.

## Gate table

| Gate | Result | Line |
|---|---|---|
| A correct | PASS | Every critical component and every deliverable figure reproduces (400, 395, 125, 270, 157, 288, 400x270/157 = 687.9, 30.94, 18+13=31, the other three indices, unauthorised table, 12 notified rows, recovery grid). Blocks agree with each other. |
| B facts present | PASS | The decisive fact (a registration answering the member's own fund-return request) is recoverable from fund_return_requests.csv request_sent_date against member_payment_matches.csv registered_date, both shipped. No external rule needed. No file states the mechanism in words; the data shows it (see Gate C). |
| C uniquely forced | PASS, two watch items | Main call: 31 is the only value that survives the data. Competing 23, 25, 26, 34 are each refuted by the files (below). Supplementary asks: one reading each survives. Watch items: pooled-detection estimator form (34), and keep versus drop of repeat advice lines. |
| D analytical not semantic | PASS | The split runs on the analysis (are the two sightings independent), not on a word. |
| E prompt unambiguous | PASS, one soft point | Recovery ask now names cover, payment year and credit scope; notified ask is count-basis neutral. Soft point: "totals unrounded" beside "amounts to the pound" (Q1 and Q3 quarter totals differ by 1 pound under sum-of-rounded-tiers). |
| F stump power | STRONG | A blind capable pass (mine) filed 25, a clean wrong answer, with every file read and every field read correctly. 23, 25, 26 and 34 all file wrong. |
| G stumping type | PASS | see line below |
| H three rules | PASS | see line below |

**Gate G line:** `mechanism: method_or_model_selection (dual-system estimation with a dependence correction)`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No shipped figure is wrong or misleading: the 395 matches, 400 recorded cases and 22,233,300 payments are all correct as reported; the difficulty is that two sources are not independent, which is a property of how the process works and survives clean data. No shipped artifact ranks the members on the index (trustee pack says no index is proposed; national statistics and AML alerts do not carry it). Gate G passes.

**Gate H line:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Field's own analysis: two-source (capture-recapture) estimation of cases the member's record did not hold, run per member against an external register, with the independence assumption tested. Layer 1: 2023/24 layout against later layout (APP/UNAUTH, pence, dd/mm/yyyy, payments in thousands), preliminary and revised returns overlapping, sort code hyphenated against zero-padded account numbers, main feed plus a supplementary extract, scheme quarters against calendar quarters. Layer 2: the receiving firms register accounts after the member's own fund-return request, so those matches are the member's own cases coming back. Easy route a strong analyst takes after reading everything correctly: Lincoln-Petersen on all 395 matches, 400x395/282 = 560.3, 25 per million (not-held 7), or simply recorded plus unmatched sightings, 513, 23. Wrong answers; correct is 31. Swap test: replacing "payments" and "scam cases" with another field's nouns does not preserve the task, because the deciding quantity is an estimate of unseen cases from a second source with a source-dependence correction.

## 1. Recovery-share ask: every reading enumerated

Base reading (scam cover, payments in 2025/26, closed in scheme quarter Q1 = Apr-Jun to Q4 = Jan-Mar of 2025/26, denominator reimbursed_amount_gbp, every recovery credit whatever its value date, route totals pooled over the four): 

| Quarter | recall | repatriation | insurer |
|---|---|---|---|
| Q1 | 6.5 | 3.4 | 2.8 |
| Q2 | 15.1 | 3.3 | 3.8 |
| Q3 | 8.5 | 2.5 | 5.9 |
| Q4 | 5.4 | 2.5 | 7.4 |
| Four | 8.5 | 2.7 | 6.0 |

(unrounded 6.4733, 15.0884, 8.5137, 5.4461, 8.5287; 3.3668, 3.3157, 2.4796, 2.5212, 2.7067; 2.8365, 3.8108, 5.8579, 7.4087, 5.9686. Credits 577,309.31 / 183,214.45 / 404,013.22 on 6,769,026.05 reimbursed; quarter denominators 252,329.33, 1,427,886.02, 2,229,339.01, 2,859,471.69, which equal recovery_statement_2025_26.csv reimbursed_in_quarter to the penny, so the base scope is the pack's own.)

Other readings the pack licenses, and the four-quarter totals (recall / repatriation / insurer) each returns:
- cover unauthorised only: 4.1 / 3.6 / 4.1; both covers: 7.5 / 2.9 / 5.5
- payment year: cases closed in 2025/26 from any payment year: 8.6 / 3.4 / 4.8
- window: closed in calendar 2025 (only three quarters exist): 10.8 / 2.8 / 4.9
- denominator payment_amount_gbp (equals the summed payment legs): 8.0 / 2.5 / 5.6
- credit scope: credits dated by 31 Mar 2026 (drops 199 credits worth 187,263.81): 7.0 / 1.9 / 5.5; credits in the quarter of closure: 2.5 / 1.1 / 3.0; credits dated on or before closure: none exist
- totals as mean of the four quarterly shares: 8.9 / 2.9 / 5.0
- the recovery statement's own recovered_stated_gbp (net of agent charges, different basis): not a case-level credit

Quarter convention: scheme Q1 = Apr-Jun and calendar Q2 cut the same four buckets, so label only. **Surviving the sentence as written: 1.** "scam reimbursement" fixes cover and the reimbursed denominator; "cases from 2025/26 payments" fixes payment year; "closed in each 2025/26 quarter" with "the four" fixes the scheme year (calendar 2025 has three); "every case-level credit" fixes credit scope; "route totals over the four" is a total, so pooled, not a mean of shares. The pack's own statement uses the same scheme-quarter and reimbursed basis.

## 2. Notified-cases ask

Main file 837 rows, supplement 119, 956 rows in all. 956 distinct case_reference values; zero overlap between the two files; no duplicate under upper-casing, punctuation and zero stripping; no collision on member, payment date and amount. **Distinct cases and feed rows select the same rows, and no member differs.** Both series, members KM-101, 102, 103, 104, 106, 108, 110, 112, 115, 118, 121, 124: 193, 121, 60, 109, 64, 111, 93, 28, 15, 37, 24, 101 (total 956). The main file alone (cut 20 June, 837 rows) is excluded by "2027/28 Q1", the quarter to 30 June. The counts equal the returns sheet's scam_cases_notified exactly, not scam plus unauthorised, so the feed is the scam feed.

## 3. Indexed case counts under every estimator form

Matches screened for a preceding own request (KM-104: 395 matches, 125 preceded, 270 independent, 157 of which are recorded cases; screened detection 0.3925). Independent confirmations: cases never requested are in the register at 0.392 (62 of 158), the same rate as requested cases on independent matches (0.393); registrations after a request fall 1 to 40 days later with none beyond 45; "returned in part" outcomes sit on the registered-after side 1,262 of 1,483. The screened detection rate is a fixed member property: Castlegate 0.391, 0.390, 0.392, 0.392 across the four years, Brindlemere 0.311, 0.311, 0.309, 0.309 and so on, against a pooled 0.319.

Indexed cases (index per million in brackets), per form:

| Form | Castlegate | Saltmarch | Trentmoor | Brindlemere |
|---|---|---|---|---|
| Lincoln-Petersen, own member | 687.9 (30.94) | 139.3 (21.88) | 301.4 (15.07) | 517.4 (12.11) |
| Chapman | 686.8 (30.89) | 138.7 (21.79) | 300.9 (15.04) | 517.0 (12.10) |
| Seber-Bailey | 686.1 (30.86) | 138.5 (21.75) | 300.7 (15.03) | 516.8 (12.10) |
| recorded + independent-unmatched / own detection, 2, 3, 4 year | 688.1 to 688.7 (30.95 to 30.97) | 139.3 to 139.4 | 301.1 to 301.2 | 517.2 to 517.4 |
| firm-type strata, own | 687.5 (30.92) | 140.4 (22.05) | 301.8 (15.09) | 516.9 (12.10) |
| no-request cases only for detection | 688.0 (30.94) | 139.0 (21.84) | 301.2 (15.06) | 517.9 (12.12) |
| detection pooled over all members | 753.7 (33.90) | 140.3 (22.04) | 296.1 (14.80) | 515.0 (12.05) |
| not screened, LP on all matches | 560.3 (25.20) | 123.5 (19.41) | 273.0 (13.65) | 479.5 (11.22) |
| not screened, recorded + matches | 513 (23.07) | 119 (18.69) | 262 (13.10) | 466 (10.91) |

**The stated band** (686 to 689, 138 to 140, 300 to 302, 515 to 521) **holds every own-member screened form** (Seber 138.5 and strata 140.4 for Saltmarch are the edges, both inside). It does not hold the pooled-detection form for Castlegate (753.7) or Trentmoor (296.1), and it does not hold the unscreened forms. **The index moves nowhere inside the own-member family**: 31, 22, 15, 12 on all of them, nearest distance to a rounding edge 0.25 per million (Saltmarch under Seber-Bailey). It moves only under the pooled-detection form, Castlegate 31 to 34. That form is not licensed by the data: the pooled rate is rejected for Castlegate (z = 3.4) and every member's rate is constant across four years, so I treat it as a refuted form, not a surviving alternative. The shipped text is silent on estimator form, so this rests on the data, not on a sentence.

**Does naming the estimator form beside the count make the decisive step easier to find?** The prompt and the pack do not name one. In the deliverable answers, "two-source estimate" names only the method class, which any analyst would reach, so it gives away nothing. The clause "register sightings no fund-return request of its own preceded" names the decisive step; if it were ever placed beside the count in anything the solver sees, it would hand over the stump. As the blocks stand it sits only on the graded side. Keep it off the prompt, the CSV header and any sheet label.

## 4. Distance from the rounding edge, in units of the stated rounding

None prints round and none sits on a tie. Amounts are exact decimals, so no float tie is possible.
- Index (per case per million): Castlegate 30.94, 0.44; Saltmarch 21.88, 0.38; Trentmoor 15.07, 0.43; Brindlemere 12.11, 0.39.
- Walk lines: recorded 17.99, 0.49; not held 12.95, 0.45; indexed 30.94, 0.44. The two lines sum to the index with no rounding gap (18 + 13 = 31).
- Indexed counts as printed in the answers: 687.9 (0.4), 139.3 (0.22), 301.44 (0.06, the closest; 302 under strata, hence the band), 517.37 (0.13).
- Recovery shares (units of 0.1): closest recall Q4 5.4461, 0.04; insurer Q3 5.8579, 0.08; recall Q1 0.23, repatriation Q4 0.29; the remaining cells and the four-quarter totals 0.13 to 0.43.
- Notified values (pounds): KM-103 153,759.53, 0.03; KM-102 285,422.35, 0.15; KM-115 0.15; KM-118 0.17; KM-110 0.18; KM-112 0.34; rest 0.32 to 0.48; KM-104 307,225.98 and KM-106 135,015.97 are 0.48 and 0.47.
- Unauthorised table (pounds): B Q2 277,917.53, 0.03; C Q1 204,473.45, 0.05; A Q3 343,190.44, 0.06; B Q1 390,380.41, 0.09; rest 0.15 to 0.48. Quarter totals 0.18 to 0.42.

## 5. Repeated advice lines

35 lines (33 cases, two of them with three lines) repeat a case already on an earlier advice; all are unauthorised fraud. Every repeat carries an amount that differs from the case's reimbursed amount, and every first line equals it. The ask's wording forces **keeping them**: "unauthorised-fraud indemnity the advices settled" is the money the advices settled; advice_total_gbp is defined as "the amount the advice settled" and includes the repeats (case_lines counts them), and the unauthorised advice totals sum to 2,984,362.84, the same as keeping every line. The ask carries no "once each" or "distinct" for this item, unlike the notified item; dropping needs an unstated dedupe rule and an unstated choice of line.

**Totals:** keep = 2,984,362.84 (Q1 984,521.08, Q2 729,676.71, Q3 673,604.73, Q4 596,560.32). Drop later lines (keep first per case) = 2,497,849.84. Drop earlier lines (keep last) = 2,946,197.35. The repeat lines are worth 486,513.00. Watch item: a solver who sees 33 repeats with off-size amounts may dedupe. The wording and the advice totals argue against it, and it is an ask-level device, not the main call. Tier by quarter, kept: A 389,667.22 / 349,939.20 / 343,190.44 / 339,633.35; B 390,380.41 / 277,917.53 / 237,744.26 / 181,103.67; C 204,473.45 / 101,819.98 / 92,670.03 / 75,823.30. These match the graded answer.

## Figures that did not reproduce

None. Every graded figure reproduces from the files. My blind derivation differed on one item, the main call (25 versus the graded 31), and that was my omission of the request screen; after screening, 125, 270, 157, 688 and 30.94 all reproduce exactly. Nothing else differs; the notified table, recovery grid and unauthorised table matched my blind figures to the penny.

## Hygiene

PASS. 19 files, formats csv, xlsx, pdf, txt; case_payments.csv has 33,851 rows and the account register 28,394. Distractors in use: quarterly returns scam_cases_notified (338, a different basis), recovery statement (different basis, net of charges), member_register notified payments (1 Oct 2027 volume, would give 24 unscreened or 30 screened per million, a wrong-year denominator), national statistics, AML alerts. No authoring language found in the pack. No exclusion-level finding.

## Cross-batch

I did not read any other task folder, as instructed; no cross-batch fingerprint was run.

## Fix

none.
