# task196 determinism judge report

Isolated judge. File universe: the fresh unzip at
`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task196_judge_pack/`
(19 members) plus the graded blocks inlined in the brief. Nothing under the repo was opened: no design
note, no generator, no pipeline.json, no earlier report, no skills, no guidelines, no other task folder.
No git command run, no agent spawned. Every load-bearing figure below was recomputed from the shipped
files with pandas / openpyxl / pdfplumber, not checked against arithmetic shown to me.

---

## Part 0. The answer the prompt and the bundle lead me to, written before the graded blocks were opened

Reading order: `prompt` -> `export_manifest.csv` -> `data_dictionary.csv` -> `indemnity_standard_v6.pdf`
-> `register_feed_notes.txt` -> `trustee_pack_2027_07.pdf` -> the data.

1. **What is asked.** Standard 4.2 defines the scam incidence index as "the number of scam cases arising
   from payments its own customers sent in the scheme year ended 31 March, **whether or not the member's
   own systems recorded them**, counted once a case however many payments it covers, per million payments
   sent as reported on the member's **revised** quarterly returns for that year", "estimated on the
   mutual's evidence base as it stands when the review is prepared, being the members' case registers and
   the scheme's beneficiary account register". 4.3 fixes the window (scheme year to 31 March 2027, index
   applies from 1 October 2027). 4.4 fixes the presentation (recorded -> cases its own record did not hold
   -> indexed, index to the nearest whole case).
2. **So the estimand is a population total including unobserved members**, with two named sightings lists.
   That is a dual-system / capture-recapture estimate, not a count. The register is industry-wide
   (`register_feed_notes.txt`), so it sights cases the member never recorded.
3. **The dependence problem.** `fund_return_requests.csv` holds the member's own outbound requests to the
   receiving firm. A request makes the receiving firm report the account, so a register row whose
   `registered_date` falls on or after the member's own request on that payment is the member's own case
   coming back, not an independent second sighting. Those must be dropped before the estimate.
4. **Review group** = the four members with `triennial_review_this_cycle = yes` in `member_register.csv`
   (KM-104, KM-101, KM-112, KM-108), corroborated by standard 4.1 and the trustee pack's item 4.
5. My own computation, before reading the blocks:

   | | KM-104 | KM-112 | KM-108 | KM-101 |
   |---|---|---|---|---|
   | recorded scam cases 2026/27 | 400 | 109 | 246 | 443 |
   | register matches 2026/27 | 395 | 85 | 162 | 302 |
   | matches preceded by own request | 125 | 39 | 75 | 142 |
   | independent sightings n2 | 270 | 46 | 87 | 160 |
   | overlap m | 157 | 36 | 71 | 137 |
   | payments sent, revised 2026/27 | 22,233,300 | 6,365,500 | 20,002,400 | 42,722,700 |
   | N (Lincoln-Petersen) | 687.90 | 139.28 | 301.44 | 517.37 |
   | index | 30.940 -> **31** | 21.880 -> **22** | 15.070 -> **15** | 12.110 -> **12** |

   **My call: 31 scam cases per million payments sent for Castlegate, indemnity year from 1 October 2027.**
   Walk: 400 recorded, +288 its own record did not hold, 688 indexed.

That is the committed answer, reached independently. Everything below is the adversarial test of it.

---

## Part 1. Gate table

| Gate | Result | One line |
|---|---|---|
| A - solution correct on the shipped files | **PASS** | Every critical component and every graded figure reproduced to the digit, including the three asks; one loose sentence in the Final Recommendation block (below). |
| B - every decisive fact in the shipped files | **PASS** | Estimand, window, denominator basis, review group, dependence evidence and as-of all located in named files; no external dependency; the recommendation's vocabulary ("scam incidence index", "cases per million payments sent", the walk, "review ... falls in the cycle") all appears in shipped text. |
| C - uniquely forced, no defensible alternative | **FAIL (two committed answers)** | (i) Supplementary ask 1 admits two licensed bases, `advice_total_gbp` vs case-level `indemnity_paid_gbp`, differing by GBP 815,235 on the year; (ii) the walk's case-count lines (288 / 688) are not invariant across standard capture-recapture estimator forms (686-689). The main index of 31 is forced. |
| D - difficulty is analytical, not semantic | **PASS** (main call) | The main call's decisive step is the dependence correction and the estimand, not a word; the ask-1 split is semantic and is reported under C/E, not credited as difficulty. |
| E - prompt unambiguous on the decision | **FAIL (ask 1)** | "unauthorised-fraud indemnity by member tier each 2026/27 quarter, totals from unrounded amounts" never names the grain, where the sibling ask 3 does say "from case-level credits"; the main ask and asks 2 and 3 are pinned. |
| F - stump power | **PASS, strong** | Four natural wrong answers sit on the easy routes (18, 23, 25, 33); only the dependence-corrected dual-system estimate gives 31. |
| G - stumping type | **PASS** | `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. |
| H - the three rules | **PASS** | `domain: pass`, `layers: pass`, `decisive_step: analytical`. |

**Verdict: NOT_DETERMINISTIC** (narrow: the main recommendation of 31 is forced and robust; two graded
figure sets are not uniquely forced).
**Taxonomy: underspecified_objective.** **Fix location: prompt** (one clause in ask 1, one clause on the
walk), with an optional supporting line in `data_dictionary.csv`.
**Disposition: SEND_BACK** - the repair is two pinning clauses and leaves the main call, the ladder, the
stump and every main-side figure frozen, but it changes the prompt solvers read, so prior runs are
invalidated and a rerun is required.

---

## Part 2. Gate A - what reproduced

### 2.1 The main chain (all exact)

| Figure | Committed | Recomputed | Source |
|---|---|---|---|
| Recorded scam cases, KM-104, scheme year 2026/27 | 400 | **400** | `case_register_2024_27.csv`, `cover_class == scam reimbursement`, `scheme_year == 2026/27` (and identically on `payment_date` in 2026-04-01..2027-03-31: 0 of 18,280 rows disagree between the two), 400 distinct `case_reference`, no duplicates, `side` is `sending` on every row |
| Payments sent, revised 2026/27 | 22,233,300 | **22,233,300** | `member_quarterly_returns.xlsx`, sheet `returns 2024-25 onward`, the only 2026/27 rows with `vintage == revised` |
| Register matches | 395 | **395** | `member_payment_matches.csv`, KM-104, `scheme_year == 2026/27`; 395 rows, 395 distinct accounts, 282 carrying a `case_reference` and 113 not |
| Matches preceded by own request | 125 | **125** | join to `fund_return_requests.csv` on `beneficiary_account_ref`; `registered_date >= request_sent_date` gives 125, and so does strict `>` (no date ties, so the "on or after" wording is not load-bearing) |
| Independent sightings | 270 | **270** | 395 - 125 |
| Overlap | 157 | **157** | of the 270, 157 carry a `case_reference` that is in the 400; all 157 are in the 2026/27 scam set, none in another year or cover; the complement 270-157 = 113 equals 395-282, i.e. every request-preceded match does carry a case reference, as it must |
| Indexed cases | 688 | **687.898 -> 688** | 400 x 270 / 157 |
| Index | 30.94 -> 31 | **30.9400 -> 31** | 687.898 / 22.2333 |
| Walk | 400 / 288 / 688 | **400 / 287.898 -> 288 / 688** | 4.4 order |
| "under three in five" chart title | - | **58.1%** (400/688) | holds |

The other three review-group members reproduce exactly as committed: 109 -> 139 -> **22**,
246 -> 301 -> **15**, 443 -> 517 -> **12**. The CSV ordering by index (31, 22, 15, 12) is correct.

### 2.2 Ask 1 - unauthorised-fraud indemnity by tier per 2026/27 quarter

Reproduced to the pound **on the case-detail basis**: Q1 A 311,088 / B 271,791 / C 81,499, total 664,379;
Q2 309,882 / 228,966 / 83,191, total 622,039; Q3 317,029 / 222,673 / 75,171, total 614,872; Q4 339,633 /
181,104 / 75,823, total 596,560. The "totals from unrounded amounts" instruction is load-bearing and the
submission obeys it: rounding the tier figures first gives 664,378 in Q1 and 614,873 in Q3. Tier is
time-invariant (the `advices` sheet and `member_register.csv` agree on all 288 advices). Quarter assignment
is unforked (`advice_date` is always the 25th of its own `settlement_month`). See 3.1 for why this answer
is not forced.

### 2.3 Ask 2 - cases notified in the quarter to 30 June 2027

All 24 figures reproduce exactly (KM-101 193 / 460,362.18 ... KM-124 101 / 231,542.05) on the union of
`notifications_2027_28_q1.csv` (cut 20 June, 837 rows) and
`notifications_2027_28_q1_supplementary.csv` (21-30 June, 119 rows), **counting rows, not distinct
`case_reference`**. This is a real fork that the pack closes properly: 5 references are shared (2 inside the
main extract, 3 across the two files) but the colliding rows are plainly different cases (different
`payment_date`, `payment_amount_gbp`, `notified_date`, `case_status`), and the `return 2027-28 Q1` sheet of
`member_quarterly_returns.xlsx` reports `scam_cases_notified` of 193 / 121 / 109 / 93 / ... which equals the
row counts member by member for all twelve. A solver who dedupes gets 191 / 120 / 108 / 92 and contradicts
the member's own revised return. The forks converge **on the records**, not by rounding.

### 2.4 Ask 3 - share of reimbursement recovered by route, cases closed in each 2025/26 quarter

All 15 figures reproduce exactly. The population is scam-reimbursement cases of **scheme year 2025/26**
whose `closed_date` falls in the quarter; numerator is `case_payments.csv` recovery credits on those cases
(any value date); denominator is their `reimbursed_amount_gbp`. This is pinned, not guessed: the
denominators 252,329.33 / 1,427,886.02 / 2,229,339.01 / 2,859,471.69 match
`recovery_statement_2025_26.csv`'s `reimbursed_in_quarter_gbp` **to the penny**, which fixes both the cover
restriction and the scheme-year restriction from a shipped artifact. Recomputed: Q1 6.5 / 3.4 / 2.8;
Q2 15.1 / 3.3 / 3.8; Q3 8.5 / 2.5 / 5.9; Q4 5.4 / 2.5 / 7.4; totals 8.5287 / 2.7067 / 5.9686 -> 8.5 / 2.7 / 6.0.
The statement's own `recovered_stated_gbp` is a declared-basis distractor (repatriation "net of recovery
agent charges") and does not reconcile to the credits on any route, so the prompt's "from case-level
credits" is doing necessary work.

### 2.5 The one Gate A blemish (solution wording, not a figure)

The Final Recommendation block rejects "a rule on the registration date, which cannot tell a sighting
another firm's victim produced from one Castlegate's own request produced", while Step 5 *is* a rule on the
registration date (registered on or after the member's own request). Read charitably it rejects a
date-only rule that ignores the requests, but as written the two blocks read as contradicting each other.
Repairable in the solution block; no figure moves.

---

## Part 3. Gate C - the forks, enumerated and computed

### 3.1 Open fork, governing: supplementary ask 1's basis

`settlement_advices_2026_27.xlsx` contains two licensed amount fields and they do not tie:

- `advices!advice_total_gbp` - data dictionary: "The amount the advice settled with the member";
  standard 5.1: "the advice states the amount settled and the number of case lines it covers".
- `advice detail!indemnity_paid_gbp` - data dictionary: "The amount the advice settled for that case".

For all 144 scam advices the detail sums to the advice total exactly. For unauthorised fraud, **49 of 144
advices do not tie**, always with the total exceeding the sum of its own lines, by amounts with no visible
structure (ratios 1.15x to 8.40x; mismatches spread across every month and every one of the twelve
members). Year totals: `advice_total_gbp` 3,313,084.58 against detail 2,497,849.84, a gap of **815,234.74
(33 per cent)**. Nothing in the pack explains it: no note column, no `sharedStrings`, no hidden sheet, no
defined name, no line in `data_dictionary.csv`, `export_manifest.csv` or either PDF, and
`case_lines` equals the detail row count for all 288 advices, so the detail is demonstrably complete.

The two answers the fork produces:

| | Q1 A / B / C (total) | Q2 total | Q3 total | Q4 total | year |
|---|---|---|---|---|---|
| case detail (committed) | 311,088 / 271,791 / 81,499 (664,379) | 622,039 | 614,872 | 596,560 | 2,497,850 |
| advice totals | 423,287 / 344,133 / 153,399 (920,819) | 791,082 | 837,971 | 763,213 | 3,313,085 |

The committed basis is the better-supported of the two: the prompt's word is "indemnity" and the only field
named indemnity is `indemnity_paid_gbp`; "totals from unrounded amounts" points at building up from
components; and the scam cover establishes the workbook's own invariant (total = sum of lines) that the 49
unauthorised totals violate while their line counts are right. But "better supported" is not "uniquely
forced". A rigorous analyst who takes the aggregate the governing standard names as "the amount settled"
commits no analytical error, and 16 graded figures move. Gate C fails on ask 1; Gate E fails on its asking
sentence, which omits the grain its own sibling ask 3 states ("from case-level credits").

### 3.2 Open fork, secondary: the estimator form behind the walk's case counts

The estimator is nowhere pinned. Grepping every file in every format (CSV, TXT, both PDFs' extracted text,
both workbooks' XML) for `petersen|lincoln|chapman|recapture|capture|estimator|two-source|multiplier|
independen*|uplift|gross-up` returns **zero hits**. Standard 4.2 names the two sighting lists and says
"estimated"; 4.4 names the presentation. Nothing selects a form, and no prior-year index or worked example
ships that would calibrate one (the trustee pack says expressly "No index is proposed in this pack").

Every form a competent analyst could use, computed:

| Form | N (KM-104) | indexed, whole | "did not hold" | index |
|---|---|---|---|---|
| Lincoln-Petersen / dual-system, N = n1 n2 / m (committed) | 687.898 | 688 | 288 | 30.9400 -> 31 |
| Chapman, N = (n1+1)(n2+1)/(m+1) - 1 | 686.791 | 687 | 287 | 30.8902 -> 31 |
| Bailey, N = n1 (n2+1)/(m+1) | 686.076 | 686 | 286 | 30.8580 -> 31 |
| capture-probability forms (n1/(m/n2), n2/(m/n1)) | 687.898 | 688 | 288 | 30.9400 -> 31 |
| LP on the stricter independence rule in 3.3 | 688.660 | 689 | 289 | 30.9740 -> 31 |

**The index survives all of them at the precision the asking sentence states** ("the index to the nearest
whole case"): the spread is 30.842 to 30.974 against a bin edge at 30.500, so the worst case clears the
printed edge by **0.358 cases per million**, about 8.0 indexed cases of headroom. Same for the other three
members: KM-112 21.591-21.880 against 21.500 (margin **0.091**, the tightest in the pack, about 0.6 cases),
KM-108 15.032-15.094 against 15.500 (margin **0.406**), KM-101 12.057-12.110 against 12.500
(margin **0.390**). All 24 estimator x independence-rule combinations give the same four indices 31 / 22 /
15 / 12, so the main recommendation and `incidence_index_2027_28.csv` are robust.

What does **not** survive is the thing standard 4.4 and the prompt both require in whole cases: the walk.
"Cases its own record did not hold" is 286, 287, 288 or 289 and "indexed cases" is 686, 687, 688 or 689
depending on an estimator the package never names. KM-112's indexed count likewise moves over 137-139.
These are committed, separately gradable figures with no tolerance, so Gate C fails here too. Note the
fork vanishes if the walk is expressed in index units: 17.991 -> 18 recorded, 12.949 -> 13 not held,
30.940 -> 31 indexed, and every estimator form gives the same 18 / 13 / 31.

### 3.3 Closed forks, with how each closes

| Fork | Options and what each computes | Closed by |
|---|---|---|
| **As-of of the register evidence** | sightings to the 2 July pull: n2 270, m 157, **index 31**. Sightings capped at the 31 March 2027 scheme-year end: n2 235, m 130, N 723.08, **index 32.52 -> 33**. Capped at 2 July or 30 June: identical to base (max `registered_date` is 2027-06-30 in the matches, 2027-07-01 in the register), so no whole-day variant of the pull bites. | Standard 4.2, "estimated on the mutual's evidence base **as it stands when the review is prepared**", plus 4.5/the trustee pack ("pulled for this meeting on 2 July 2027") and the prompt's "the feed runs to the 2 July pull". This is the single most load-bearing sentence in the pack: the two readings do **not** converge, they give 31 and 33, and closure rests entirely on that clause being read literally. It is stated in three places, so I call it closed. |
| **Which date puts a case in the scheme year** | `payment_date` / `scheme_year` field: 400 recorded, m 157, **index 31**. `notified_date`: 397 recorded, m 133, N 805.94, **index 36.25 -> 36**. | Standard 4.2, "cases **arising from payments** its own customers sent in the scheme year ended 31 March". The `scheme_year` column and `payment_date` agree on all 18,280 rows, so the two convergent readings converge **on the records**, not by rounding. |
| **Return vintage for the denominator** | revised 22,233,300 -> 30.9400 -> **31**. Preliminary 22,227,042 -> 30.9487 -> **31**. `notified_payments_next_indemnity_year` 23,123,000 -> 29.7495 -> 30. | 4.2 says "as reported on the member's **revised** quarterly returns for that year", and the dictionary's vintage line. The preliminary variant converges by arithmetic (the two denominators differ by only 6,258 payments), not on the records, but the governing text excludes it anyway; the member-register volume is next year's expectation and is not licensed at all. |
| **Register-status filter** | all accounts, or `register_status == reported` only: identical, 270 / 157 / **31**. All 395 of Castlegate's matched accounts are `reported`; the 4,040 `closed by firm` accounts never touch this member. Convergence is on the records. | `register_feed_notes.txt`, "An account stays on the register once it is reported". |
| **Account-reference normalisation** | padded join: 395 of 395 matched to `mule_account_register.csv`. Naive join without re-padding: 353, losing 42 accounts. | `register_feed_notes.txt` states the padding rule and names the failure. Layer 1 mess, non-decisive here because the matches file already carries the register's date, verified identical for all 395 rows. |
| **Quarter to 30 June 2027, endpoint** | inclusive: 956 rows, 193 / 121 / 109 / 93 etc. Exclusive of 30 June: 12 rows dropped across 9 members. (13 rows sit on 1 April.) | "the quarter to 30 June 2027" is the quarter ending that day, and the `return 2027-28 Q1` sheet pins the inclusive counts member by member. Converges on the records. |
| **Ask 1 quarter basis** | `settlement_month` or `advice_date`: identical for all 288 advices (every advice is dated the 25th of its own month). | Converges on the records. |
| **Ask 3 credit window** | all credits on cases closed in the quarter (committed) vs credits valued inside the same quarter (different figures on every route). | The prompt attaches the quarter to the closure ("on cases closed in each 2025/26 quarter"), `export_manifest.csv` describes the statement as "recoveries on cases closed in the year by route", and standard 5.2 credits recoveries against the case at the date funds arrive. The statement's penny-exact denominator match confirms the population. |
| **Ask 3 cover and scheme year** | scam + scheme year 2025/26 (committed, 6.5/3.4/2.8 ...). All covers, all years closed in quarter: 8.6/3.7/2.3 ... Scam only, all years: 10.9/4.8/2.9 ... | Pinned by `recovery_statement_2025_26.csv`, whose `reimbursed_in_quarter_gbp` equals the committed denominator exactly in all four quarters. Without that file this would be an open fork; with it, it is closed on the records. |
| **Independence rule for the second source** | committed: drop the 125 matches registered on or after the member's own request -> n2 270, m 157, **31**. Stricter: keep only the 167 accounts registered *before* the payment left -> N 688.66, **31**. Over-broad: drop all 220 accounts the member ever chased -> n2 175, m 62, N 1,129.03, index 50.78 -> 51. | The over-broad rule discards sightings that demonstrably predate the request and is not a reasonable choice; the committed and stricter rules both give 31. Sensitivity here is to an unreasonable choice only, which the gate permits. |

---

## Part 4. Figures I could not reproduce

None. Every committed figure in the four blocks reproduced exactly from the shipped files: the five
critical components, all eight solution steps, the four member indices, the three walk lines, the twelve
tier-quarter amounts and four quarter totals (on the case-detail basis), the twelve case counts and twelve
values for the June quarter, and all fifteen recovery shares. The defects above are forks and a wording
slip, not unreproduced numbers.

---

## Part 5. Files and hygiene - PASS

19 files; 4 formats (12 CSV, 2 XLSX, 2 PDF, 1 TXT) - clears the 5-file floor and the three-format bar, no
monoculture. Largest file `case_payments.csv` at 33,851 rows. All artifacts read as operational exports:
the 2023/24 register in the old layout with `dd/mm/yyyy` dates and amounts in pence, the pre-2024/25
returns sheet in thousands against whole payments after, preliminary and revised 2026/27 vintages
overlapping, a notification feed cut on 20 June plus a quarter-end supplement, account references written
two different ways on the two sides of a join, colliding case references, a recovery statement on a mixed
stated basis. Distractors are relevant and unused: `aml_alert_summary.csv`,
`national_scam_statistics_calendar_year.csv` (calendar quarters, loss value per GBP million, no count
basis), `recovery_statement_2025_26.csv`'s stated recoveries, the preliminary 2026/27 sheet, the 2023/24
register. No README or how-generated artifact, no "synthetic"/"generated"/"benchmark" language, no tool
banner; workbook `docProps` and both PDF `/Producer` strings read "Kelverstone Mutual secretariat", in
fiction. Data is fictional, so no public-data contamination and no canonical published finding. Dates are
coherent with a 2 July 2027 pull throughout.

Two minor, non-decisional findings, in-house FIX_NOW, neither exclusion-level and neither touching the
analytic surface:
- both PDFs carry `/CreationDate D:20000101000000`, which contradicts the 2027 fiction.
- the 49 non-tying unauthorised advice totals (3.1) read as an unintended data defect rather than
  authentic mess, because the scam cover ties perfectly and nothing in the pack accounts for the gap.
  Fixing it is what closes the ask-1 fork.

Nothing exclusion-level.

---

## Part 6. Stump power (Gate F) - strong

Four wrong answers sit on the natural easy routes and only the dependence-corrected dual-system estimate
reaches 31: report the recorded rate, 400 / 22.2333 = **18**; add the register's 113 unmatched sightings to
the register count, 513 -> **23**; run the two-source estimate on all 395 matches without the dependence
correction, 560.28 -> **25**; or confine the register evidence to the scheme year instead of the 2 July
pull, 723.08 -> **33**. The decisive insight is genuinely hard and genuinely in the data: the member's own
fund-return request is what makes the receiving firm report the account, so 125 of its 395 register
sightings are its own capture coming back, and using them inflates the overlap and collapses the estimate.
No documentation hands that out, the prompt does not gesture at it, and the correction needs a join
(`member_payment_matches` x `fund_return_requests` on the account, compared on dates) the prompt never
mentions. The asks each carry their own device as well: the rounding order in ask 1 (664,379 against
664,378), the colliding case references in ask 2 (193 against 191 if deduped), and the statement's
stated-basis recoveries in ask 3. I would expect a strong model to file 23 or 25.

## Part 7. Stumping type (Gate G)

`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`.

Every reported number in the pack is **fine**: the 400 recorded cases are correctly recorded, the 395
matches are correct matches, the revised returns are the right denominator, the 125 request-preceded
sightings are real sightings. Nothing the solver must catch is wrong or misleading, and no defect, decoy
or withheld rule carries the call. The difficulty is choosing the estimand the governing standard actually
defines (a population total including cases the member never recorded) and then the estimator's second
source correctly, which is method and estimand selection on honest data. Not banned; no
`banned_stumping_type` finding. The FINE-numbers method carrying the difficulty is dual-system
(capture-recapture) estimation with a source-dependence correction pinned by the member's own outbound
request log.

## Part 8. The three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

The field's own analysis decides it: an incidence rate per million exposure units for an indemnity year's
contribution loading, over cases **incurred but not recorded**, estimated from two sighting lists, which is
experience-rating work and is instituted as such by Part 4 of the mutual's own standard. Swap test: putting
another field's nouns in does not leave the task reading the same, because the quantity is an indemnity
index that an insurance instrument defines, measures over a scheme year and applies to an indemnity year
from the following 1 October; the estimation method generalises across fields, but the estimand, the
exposure base (revised returns of payments sent) and the use (loss-control placement and contribution
loading) are the domain's. Layer 1: layout and unit changes across register and return vintages (pence and
`dd/mm/yyyy` in 2023/24, thousands before 2024/25, preliminary against revised 2026/27), account
references written two ways across the register and the matching run, a notification feed cut mid-quarter
with a supplement, colliding case references, a recovery statement on a mixed stated basis, calendar-year
national statistics against a fiscal scheme year. Layer 2: the estimand includes cases the member never
recorded, and the second sighting list is dependent on the member's own fund-return requests.
The easy route a strong analyst who cleaned everything and read every rule correctly would still take: run
the two-source estimate on all 395 register matches, giving 560 cases and an index of **25**, or simply add
the 113 unmatched register sightings to the 400 recorded, giving 513 and **23**. Either is wrong and both
are reachable with perfect data hygiene, so H3 passes as analytical.

---

## Part 9. Fix

**Prompt**, two clauses, main-call side frozen:

1. Ask 1: name the grain, exactly as ask 3 already does. "...unauthorised-fraud indemnity by member tier
   each 2026/27 quarter, **from the case-level indemnity amounts on the advice detail**, totals from
   unrounded amounts". Optionally support it with one `data_dictionary.csv` line saying what
   `advice_total_gbp` carries beyond its case lines, so the 49 non-tying advices read as mess rather than
   as an error. This is the governing repair.
2. The walk: either state the walk in index units (cases per million, nearest whole case, which is
   invariant at 18 / 13 / 31 across every estimator form) or have the asking sentence state the estimate
   form once, without filing how the sightings are attributed. The latter keeps the walk in whole cases;
   either keeps the decisive step, the dependence correction, untouched.

Nothing else needs to move: the main recommendation of 31, the ladder, the four indices, the CSV
deliverable, ask 2 and ask 3 all stand as shipped. The Final Recommendation block's "not a rule on the
registration date" sentence should be reworded in the **solution** to stop contradicting Step 5.
