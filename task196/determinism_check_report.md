# task196 determinism judge report

Isolated review. File universe: the fresh unzip at
`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task196_judge_pack`
(19 files) plus the graded blocks inlined at the end of the judge brief. Nothing under the task
folder was opened: no design note, no generator, no pipeline.json, no earlier report, no skills or
guidelines directory, no other task folder. No git command run, no agent spawned. Every figure below
was recomputed from the shipped files with pandas / openpyxl / pdftotext, not checked against
arithmetic shown to me.

The derivation below was written before the graded blocks were read, as the brief directs.

---

## Verdict

**NOT_DETERMINISTIC** on the committed answer set. The **main recommendation is forced** (31 scam cases
per million payments sent) and every one of its critical components reproduces to the penny.
**Supplementary ask 4** (unauthorised-fraud indemnity by tier per 2026/27 quarter) is not forced: the
shipped files license two readings of "each line in the quarter it settles in" and all sixteen graded
figures differ between them, with the committed figures resting on the reading that the shipped
indemnity standard, read literally, contradicts.

**Disposition: SEND_BACK.** The repair pins the settlement-quarter basis for the advice-detail lines
(one prompt clause, or a data-dictionary row that says what the detail sheet's `settlement_month`
field IS) and, if the advice-month basis is the intended one, regenerates the sixteen ask-4 figures.
Either pin changes what solvers see, so a rerun is required.

**Governing taxonomy label: `underspecified_objective`.** Fix location: **prompt**.

## Gate table

| Gate | Result |
|---|---|
| A - solution correct on the shipped files | PASS for the main call and asks 1, 2, 3, 5, 6: all critical components and all index/walk/recovery figures reproduce exactly. Flagged on ask 4: the committed figures reproduce only on the stale detail-line month, which is provably the month of the case's *first* advice in all 35 affected lines. |
| B - every decisive fact in the shipped files | PASS. Estimand, window, denominator basis, walk order and rounding all come from `indemnity_standard_v6.pdf` Part 4; review-group membership from `member_register.csv` / `trustee_pack_2027_07.pdf`; the ask-6 population is pinned by `recovery_statement_2025_26.csv`. No external dependency. Action vocabulary ("scam incidence index", "walk", "per million payments sent", "revised quarterly returns") all appears in shipped text. |
| C - uniquely forced, no defensible alternative | **FAIL on supplementary 4.** Two licensed readings, 16 figures differ (table below). PASS on the main call and on asks 1, 2, 3, 5, 6. |
| D - difficulty is analytical, not semantic | PASS for the main call: the decisive step is the construction of the two-source estimator, not the meaning of a word. (The ask-4 split *is* semantic, which is a C/E finding, not a D one.) |
| E - prompt unambiguous on the decision | **FAIL on supplementary 4**: "each line in the quarter it settles in" does not fix whether "it" settles in its advice or in the month its own detail row states. PASS elsewhere. |
| F - stump power | PASS. Four distinct wrong landings enumerated below (25, 51, 33/32, 30), each reachable by a competent analyst who cleaned the data correctly. |
| G - stumping type | PASS. `method_or_model_selection` on honest numbers; no reported figure has to be caught as wrong. |
| H - the three rules | PASS. `domain: pass`, `layers: pass`, `decisive_step: analytical`. |

---

## Part 1 - the derivation, before the graded blocks were read

### 1.1 What the prompt and the standard pin

`indemnity_standard_v6.pdf` 4.2 defines the quantity exactly: scam cases **arising from payments the
member's own customers sent in the scheme year ended 31 March**, **whether or not the member's own
systems recorded them**, counted once a case however many payments it covers, **per million payments
sent as reported on the member's revised quarterly returns for that year**, **estimated on the
mutual's evidence base as it stands when the review is prepared, being the members' case registers
and the scheme's beneficiary account register**. 4.3 sets the window (scheme year ended the preceding
31 March, index applying from 1 October). 4.4 fixes the walk order (recorded, then cases the own
record did not hold, then indexed) and the rounding (nearest whole case per million). 4.1 limits the
exercise to members whose triennial review falls in the cycle.

So the estimand is a **population size with incomplete member-side reporting**, to be estimated from
two overlapping sightings lists. That is a two-source capture-recapture problem, and the standard
names both lists.

Review group, from `member_register.csv` `triennial_review_this_cycle = yes`: KM-104 Castlegate,
KM-101 Brindlemere, KM-112 Saltmarch, KM-108 Trentmoor. Four members.

### 1.2 The two sources and the dependence

Source 1, Castlegate's own register: `case_register_2024_27.csv`, member KM-104, cover
`scam reimbursement`, scheme year 2026/27 -> **400 cases**, 400 distinct references. Robust: the
`scheme_year` label and a payment-date filter on 2026-04-01..2027-03-31 select the identical 400 rows
(a notified-date filter would give 397, but 4.2 says "arising from payments ... sent in the scheme
year", so payment date governs and the two agree anyway).

Source 2, the scheme register: `member_payment_matches.csv`, KM-104, 2026/27 -> **395 matched
payments**, 395 distinct accounts, 282 carrying a case reference (all 282 distinct and all present in
Castlegate's own 2026/27 scam register), 113 with none.

The dependence is in `fund_return_requests.csv`. 220 of the 395 matched accounts carry a Castlegate
fund-return request. On **125** of them the request was sent **strictly before** the register
accepted the account (125 of 125 of those also post-date Castlegate's payment); on the other 95 the
account was already on the register when Castlegate asked. A registration that the member's own
request produced is the member's own case coming back, not a second, independent sighting of it, so
those 125 must leave source 2. The 95 where the register entry pre-dates the request cannot have been
caused by it and stay.

Remaining source 2: **270** sightings, of which **157** are also in Castlegate's own register
(cross-tab: preceded x in-own = 125/0 and 157/113).

### 1.3 Every estimator form, computed

Payments sent, `member_quarterly_returns.xlsx` sheet `returns 2024-25 onward`, KM-104, 2026/27, all
four quarters `revised`: 5,240,820 + 5,418,060 + 5,873,720 + 5,700,700 = **22,233,300**. The
`preliminary 2026-27` sheet sums to 22,227,042 and is superseded (`vintage` definition in
`data_dictionary.csv`); it gives 30.95 per million, the same index.

n1 = 400, n2 = 270, m = 157:

| estimator form | N | per million | nearest case |
|---|---|---|---|
| Lincoln-Petersen `n1*n2/m` | 687.898 | 30.9400 | **31** |
| Chapman `(n1+1)(n2+1)/(m+1)-1` | 686.791 | 30.8902 | **31** |
| Bailey `n1*(n2+1)/(m+1)` | 686.076 | 30.8580 | **31** |

The committed answer survives all three estimator forms at the precision the asking sentence states
(nearest whole case per million). Distance from the printed bin edge (30.5): **0.44 cases** on
Lincoln-Petersen, **0.39** on Chapman, **0.36** on Bailey. All exceed 0.3 of the rounding unit.

The walk also survives all three forms: recorded 400/22.2333 = 17.991 -> 18; not-held
287.898/22.2333 = 12.949 -> 13 (Chapman 286.791 -> 12.90 -> 13); indexed 30.94 -> 31; 18 + 13 = 31.

### 1.4 Every window, population and as-of reading the shipped text licenses

| reading | source of the licence | n2 / m | per million | index |
|---|---|---|---|---|
| evidence base as pulled, all register rows to the 2 Jul 2027 feed | 4.2 "as it stands when the review is prepared"; trustee pack "as pulled for this meeting on 2 July 2027"; prompt "the feed runs to the 2 July pull" | 270 / 157 | 30.94 | **31** |
| registrations on/before 30 Jun 2027 | last registered_date in the matches file is 2027-06-30 | 270 / 157 | 30.94 | 31 (same records) |
| registrations on/before 2 Jul 2027 | prompt's pull date | 270 / 157 | 30.94 | 31 (same records) |
| registrations on/before 31 Mar 2027 (scheme-year end) | a misreading of 4.3's measurement window as applying to the register too | 235 / 130 | 32.52 (Chapman 32.45) | 33, or 32 on Chapman |
| registrations on/before 30 Apr 2027 | - | 244 / 135 | 32.52 | 33 / 32 |
| registrations on/before 31 May 2027 | - | 254 / 142 | 32.18 | 32 |

The first three converge **on the records**, not by rounding: all register rows in Castlegate's
2026/27 match set are dated on or before 2027-06-30, so the three cut-offs select the identical 270
sightings and the identical 157 overlaps. The 31 March cut-off is a genuinely different record set
(35 registrations dropped) and gives a different answer, **and the estimator forms disagree with each
other under it** (33 on Lincoln-Petersen, 32 on Chapman). It is closed by three separate shipped
sentences: 4.2's "as it stands when the review is prepared", the trustee pack's "as pulled for this
meeting on 2 July 2027", and the prompt's own "the feed runs to the 2 July pull". The scheme-year
window in 4.2/4.3 attaches to the **payment** date, which is already applied. I record it as closed,
not open.

Whole-day variants: every date field in the pack is a whole date (no times anywhere, no time zone),
so there is no sub-day variant of any window to enumerate. Payment-date window 2026-04-01..2027-03-31
inclusive is the only reading of "the scheme year ended 31 March 2027"; the register's own
`scheme_year` label agrees row for row.

Population variants on source 2:

| reading | n2 / m | per million | index |
|---|---|---|---|
| exclude only register rows a Castlegate request preceded (committed) | 270 / 157 | 30.94 | **31** |
| as above, strict inequality request < registered | 270 / 157 | 30.94 | 31 (identical rows) |
| keep only `register_status = reported` | 270 / 157 | 30.94 | 31 (all 270 are `reported`) |
| keep only `report_reason = scam proceeds` | 177 / 103 | 30.92 | 31 |
| drop every account that carries any Castlegate request, ordering ignored | 175 / 62 | 50.78 (Chapman 50.34) | **51, or 50 on Chapman** |
| no exclusion at all, the full 395 | 395 / 282 | 25.20 | **25** |

Denominator variants: revised returns 22,233,300 -> 30.94 -> 31; preliminary returns 22,227,042 ->
30.95 -> 31; `member_register.notified_payments_next_indemnity_year` 23,123,000 -> 29.75 -> **30**
(closed by 4.2, which names the revised quarterly returns for the measured year, not the notified
forward volume).

### 1.5 The answer the prompt and the bundle lead to

**31 scam cases per million payments sent**, on 688 indexed cases and 22,233,300 payments, against 400
recorded (18 per million); walk 18 recorded + 13 not held = 31 indexed. Review group, same basis:

| member | recorded | n2 / m | indexed | index | Chapman | recorded index |
|---|---|---|---|---|---|---|
| KM-104 Castlegate | 400 | 270 / 157 | 688 | **31** (30.9400) | 30.89 | 18 |
| KM-112 Saltmarch | 109 | 46 / 36 | 139 | **22** (21.8801) | 21.79 | 17 |
| KM-108 Trentmoor | 246 | 87 / 71 | 301 | **15** (15.0700) | 15.04 | 12 |
| KM-101 Brindlemere | 443 | 160 / 137 | 517 | **12** (12.1100) | 12.10 | 10 |

Order by index: KM-104, KM-112, KM-108, KM-101. Castlegate's own record holds 400/688 = 58.1 per cent,
"under three in five", which is a true statement of the finding.

### 1.6 The asks, derived

**Ask 4, unauthorised-fraud indemnity by tier per 2026/27 quarter.** Tiers agree between
`member_register.csv` and the advices sheet. The detail sheet sums to its advice totals exactly: 0 of
288 advices show any gap between `advice_total_gbp` and the sum of its `indemnity_paid_gbp` lines, and
0 of 288 show a `case_lines` mismatch; `advice_date` is in the header `settlement_month` for all 288.
Grand totals tie: 14,616,718.57 both ways, unauthorised 2,984,362.84 both ways.

But **35 detail rows carry a `settlement_month` that differs from their advice's**, all of them
unauthorised fraud, all earlier than the advice, and in **35 of 35 cases the detail month is exactly
the month of that case's first advice**. These are top-up settlements on cases already part-settled
earlier, and the line's own month field was carried over from the first advice. This is the fork; see
Part 3.

| quarter | reading A: the advice that settles the line | reading B: the line's own `settlement_month` (committed) |
|---|---|---|
| Q1 | A 311,088 / B 271,791 / C 81,499 / total 664,379 | A 389,667 / B 390,380 / C 204,473 / total 984,521 |
| Q2 | A 369,083 / B 287,713 / C 150,242 / total 807,038 | A 349,939 / B 277,918 / C 101,820 / total 729,677 |
| Q3 | A 348,469 / B 308,956 / C 117,654 / total 775,080 | A 343,190 / B 237,744 / C 92,670 / total 673,605 |
| Q4 | A 393,790 / B 218,686 / C 125,391 / total 737,867 | A 339,633 / B 181,104 / C 75,823 / total 596,560 |

All sixteen figures differ. 486,513.00 of indemnity moves between quarters. The "totals unrounded"
instruction does real work in both readings: under B the Q1 rounded tiers sum to 984,520 against a
984,521 total, and under A the Q3 rounded tiers sum to 775,079 against 775,080.

**Ask 5, cases notified in the quarter to 30 June 2027.** `notifications_2027_28_q1.csv` runs
2027-04-01 to 2027-06-20 (837 rows), the supplement 2027-06-21 to 2027-06-30 (119 rows); no row falls
outside the quarter. Combined 956 rows over 951 distinct references: 2 reference collisions inside the
main feed and 3 across the two feeds, all five pairs carrying different payment dates, amounts and
statuses, so they are two notifications sharing a reference rather than duplicate rows (0 fully
identical rows). Counted raw: KM-101 193 / 460,362; KM-102 121 / 285,422; KM-103 60 / 153,760;
KM-104 109 / 307,226; KM-106 64 / 135,016; KM-108 111 / 243,325; KM-110 93 / 301,939; KM-112 28 /
72,566; KM-115 15 / 26,336; KM-118 37 / 94,158; KM-121 24 / 53,735; KM-124 101 / 231,542.
De-duplicating on `case_reference` instead gives KM-101 191 / 458,875, KM-102 120 / 282,003, KM-104
108 / 302,381, KM-110 92 / 301,198 and leaves the other eight members unchanged. The fork is closed
from inside the pack: `member_quarterly_returns.xlsx` sheet `return 2027-28 Q1` reports
`scam_cases_notified` of 193, 121, 60, 109, 64, 111, 93, 28, 15, 37, 24, 101, which is the raw count
member for member. The manifest's claim that the supplement "omits cases already in the main extract"
is strictly violated by the 3 cross-feed collisions; it is colour, not a rule, and does not move the
count.

**Ask 6, recovery share by route on cases closed in each 2025/26 quarter.** Computed from case-level
credits in `case_payments.csv` (`entry_type = recovery credit`) over the reimbursement on the closed
cases. The population is pinned by `recovery_statement_2025_26.csv`: its `reimbursed_in_quarter_gbp`
of 252,329.33 / 1,427,886.02 / 2,229,339.01 / 2,859,471.69 reproduces **to the penny** only as the sum
of `reimbursed_amount_gbp` over `cover_class = scam reimbursement`, `scheme_year = 2025/26` cases with
`closed_date` in that quarter of 2025/26 (60 / 328 / 556 / 644 cases). That shipped tie closes both
candidate forks: cover (scam only, not both covers) and vintage (2025/26 cases, not every case closed
in the quarter). Shares:

| quarter | beneficiary recall | repatriation | insurer contribution |
|---|---|---|---|
| Q1 | 6.4733 -> **6.5** | 3.3668 -> **3.4** | 2.8365 -> **2.8** |
| Q2 | 15.0884 -> **15.1** | 3.3157 -> **3.3** | 3.8108 -> **3.8** |
| Q3 | 8.5137 -> **8.5** | 2.4796 -> **2.5** | 5.8579 -> **5.9** |
| Q4 | 5.4461 -> **5.4** | 2.5212 -> **2.5** | 7.4087 -> **7.4** |
| four-quarter total | 8.5287 -> **8.5** | 2.7067 -> **2.7** | 5.9686 -> **6.0** |

The statement's own `recovered_stated_gbp` is useless as a source (Q1 recall 6,096.59 against 16,334.07
of actual credits; repatriation stated net of recovery agent charges), which is why the prompt says
"from case-level credits". A reading that also restricted the credits themselves to value dates inside
2025/26 would give Q3 8.2 / 2.4 / 5.8 and Q4 2.2 / 0.6 / 6.4; nothing in the ask or in 5.2 (credits are
taken "at the date the funds arrive", with no year limit) licenses that truncation, and the statement's
own basis is "recoveries on cases closed in the quarter", so I record it as closed.

### 1.7 Unit forcing and invariance

| quantity | unit forced by its asking sentence? | invariant across estimator forms at that unit? |
|---|---|---|
| member index | yes, "index and walk lines to the nearest whole case", "all per million" | yes: LP 30.94, Chapman 30.89, Bailey 30.86 all give 31; 22 / 15 / 12 likewise |
| Castlegate walk lines | yes, same sentence, and 4.4 restates it | yes: 18 + 13 = 31 under all three forms |
| indexed case counts (688 etc.) | not stated as a graded unit; they are narrative support for the index | no: 688 LP vs 687 Chapman vs 686 Bailey. Stating 688 as a committed figure pins one estimator form that the prompt does not pin. See finding 2. |
| tier/quarter indemnity | yes, "amounts to the nearest pound", "totals unrounded" | not estimator-dependent; it is a sum |
| notified cases and value | yes, "GBP to the nearest pound" | not estimator-dependent |
| recovery shares | yes, "round shares to one decimal" | not estimator-dependent |

### 1.8 Component-to-total checks

- Advice detail vs advice header: 288 of 288 tie exactly, gap 0.00; `case_lines` 288 of 288 tie. No gap to report.
- Advice grand total: detail 14,616,718.57 = headers 14,616,718.57. Unauthorised: 2,984,362.84 both ways.
- Quarter tier totals: taken from unrounded tier amounts as instructed, so the rounded components sum £1 short in reading-B Q1 (984,520 vs 984,521) and in reading-A Q3 (775,079 vs 775,080). Both are the instruction working, not a defect.
- Castlegate walk: 17.991 + 12.949 = 30.940, printed 18 + 13 = 31. The printed lines sum to the printed index; the unrounded lines sum to the unrounded index.
- Ask 5: member counts sum to 956 = the combined row count; member values sum to 2,365,387.84.
- `recovery_statement_2025_26.csv` `reimbursed_in_quarter_gbp` reconciles exactly to the case-level population (above). Its `recovered_stated_gbp` does **not** reconcile to case-level credits, by design and by its own `statement_basis` column: Q1 recall 6,096.59 vs 16,334.07 (gap 10,237.48), Q2 32,507.56 vs 215,444.62 (gap 182,937.06), Q3 223,976.38 vs 189,800.33 (gap -34,176.05), Q4 214,193.57 vs 155,730.29 (gap -58,463.28); repatriation 107,924.95 stated against 183,214.45 credited (gap 75,289.50); insurer 374,271.06 stated against 404,013.22 credited (gap 29,742.16). The prompt's "from case-level credits" is what resolves this, and it is a distractor rather than a reconciling item.

### 1.9 Distance from the printed bin edge, every graded figure

Rounding unit from the asking sentence in brackets. Distance is to the nearest rounding boundary,
expressed in units of that rounding unit; flagged if under 0.3.

| figure | value | printed | edge distance |
|---|---|---|---|
| Castlegate index [1 case] | 30.9400 | 31 | 0.440 |
| Saltmarch index [1] | 21.8801 | 22 | 0.380 |
| Trentmoor index [1] | 15.0700 | 15 | 0.430 |
| Brindlemere index [1] | 12.1100 | 12 | 0.390 |
| walk, recorded [1] | 17.9910 | 18 | 0.491 |
| walk, not held [1] | 12.9490 | 13 | 0.449 |
| recovery shares, 15 figures [0.1pp] | min 5.4461 (Q4 recall) | 5.4 | min 0.461, all 15 at or above 0.461 |
| ask 5 values, 12 figures [£1] | - | - | min 0.03 (KM-103 153,759.53) **flagged**; also KM-102 0.15, KM-115 0.15, KM-118 0.17 |
| ask 4 amounts, 16 figures [£1] | - | - | min 0.03 (Q2 tier B 277,917.53) **flagged**; also Q3 A 0.06, Q1 C 0.05, Q1 B 0.09, Q4 A 0.15, Q4 B 0.17, Q4 C 0.20, Q3 B 0.24, Q1 A 0.28, Q2 total 0.21, Q3 total 0.23, Q4 total 0.18 |

The flagged ones are all pound amounts whose fractional part sits near a half penny-rounding boundary.
They are **not** margin fragility: each is an exact decimal sum of exact decimal source values with no
estimation freedom, so every rigorous solver lands on the same penny and rounds the same way (a
thin-but-clean gap under Gate C). The figures that *could* have been fragile are the index figures,
and the tightest of those is 0.38 of a case, which survives all three estimator forms.

Not a graded figure, but worth naming because it sits inside the flag band: Trentmoor's walk gap is
2.7497 per million, 0.250 of a case from the 2.5 boundary. Only Castlegate's walk is asked for, so it
is not graded here; if the walk is ever widened to the whole review group, that line is fragile.

---

## Part 2 - what the graded blocks say, read after the above

Every critical component reproduces exactly: 400 recorded, 395 matches, 125 preceded by Castlegate's
own request, 270 independent sightings of which 157 also in its own register, 288 cases its record did
not hold (687.898 - 400 = 287.898 -> 288). 688 indexed on 22,233,300 payments, 30.94 per million, 31.
The four indices (31 / 22 / 15 / 12), the recorded counts (400 / 109 / 246 / 443), the indexed counts
(688 / 139 / 301 / 517), the walk (18 / 13 / 31), the csv order, the "under three in five" finding
(58.1 per cent), ask 5's twenty-four figures and ask 6's fifteen figures all reproduce as printed. The
solution's step 7 claim that "every licensed form of the estimate gives [the walk] alike" is true as
stated for the three estimator forms.

Ask 4's sixteen figures reproduce only on reading B.

---

## Part 3 - findings

### Finding 1 (disqualifying): supplementary ask 4 is not forced. Gates C and E.

The ask says "unauthorised-fraud indemnity by member tier per 2026/27 quarter, **each line in the
quarter it settles in**". Two readings are licensed and both are defensible:

- **Reading A, the advice that settles the line.** `indemnity_standard_v6.pdf` 5.1: "The mutual
  settles with each member monthly by advice, **one advice per cover per month**, and the advice states
  the amount settled and the number of case lines it covers." `data_dictionary.csv` on
  `indemnity_paid_gbp`: "The amount **the advice** settled for that case." So the 18,800.64 on
  `ADV-202607-108-U` was settled by a July advice and settles in Q2. Reading A also keeps the sheet
  coherent: 288 advices = 12 members x 12 months x 2 covers, one per member per cover per month.
- **Reading B, the detail row's own `settlement_month`** (the committed basis). The column carries that
  name, the dictionary never defines it, and the clause "each line in the quarter it settles in" only
  does work under this reading, since advice-level and advice-month line-level aggregation give the
  same table.

Reading B assigns 486,513.00 of indemnity to quarters in which, per 5.1, no advice settled it, and it
puts up to four advices into one member-cover-month (KM-108 unauthorised 2026-04 gets 4, KM-104 and
KM-124 get 3, twenty-eight more get 2), which 5.1 forbids. The detail month is demonstrably stale: in
35 of 35 affected lines it equals the month of that case's **first** advice. On a literal read of the
shipped standard, reading A is the better-grounded of the two, which means the committed figures may
also be wrong and not merely contested.

All sixteen graded figures differ between the readings (table in 1.6). Two rigorous solvers who clean
the data perfectly and read every field correctly land on two complete tables, so the ask is a
semantic lottery rather than an analysis. This is `underspecified_objective`.

**Repair.** Pin it. Either (a) a prompt clause naming the basis - "each line in the quarter the advice
that settled it falls in", or "each line in the quarter its own settlement month states" - or (b) a
`data_dictionary.csv` row for the advice-detail `settlement_month` field saying what it IS (the month
of the case's first advice, or the month the line settled). (b) is the lighter touch and is the
data-dictionary pin the standard allows in-house, but it still changes what solvers see, and if the
author concludes reading A governs, the sixteen figures have to be regenerated as well. Either way the
prior runs are invalidated and a rerun is required: **SEND_BACK**.

### Finding 2 (repairable in the blocks): 688 pins an estimator form the prompt does not pin.

The main recommendation and the deliverable both state the indexed case counts (688, 139, 301, 517) as
committed figures. These are not invariant: Castlegate is 688 on Lincoln-Petersen, 687 on Chapman, 686
on Bailey. The graded quantity, the index at the nearest whole case per million, is invariant across
all three, and so is the walk. Nothing in the prompt or in Part 4 of the standard asks for a case count
or fixes an estimator form, so a solver who used Chapman (the standard small-sample correction, and the
one a reviewer would expect for n2 = 46 on Saltmarch) files 687 and is marked wrong on a figure the
task never pinned. Keep the case counts out of the graded set, or state them as "about 690", or pin the
estimator form in the prompt. This is a blocks-and-rubric repair, not a determinism failure of the
decision.

### Finding 3 (note): the manifest over-claims on the notification supplement.

`export_manifest.csv` says the supplement omits "cases already in the main extract", but three
references appear in both feeds (101-Q12728-1538, 104-Q12728-8279, 110-Q12728-6550), with different
payment dates and amounts in each. The count is unaffected and the returns sheet corroborates the raw
count, so this is colour rather than a defect; a solver who takes the manifest literally and
de-duplicates files 191 for KM-101 instead of 193, which the shipped return contradicts. Leaving it is
acceptable; tightening the manifest sentence would remove a needless second reading.

### Finding 4 (note): the zero-padding warning is a no-op.

`register_feed_notes.txt` warns that the match "loses every account whose number starts with a zero"
unless the number is padded back to eight digits. In the shipped data the naive join loses nothing: all
6,994 match references resolve to a register account both padded and unpadded, and the matches file's
`registered_date` agrees with the register on all 6,994 rows. 42 of Castlegate's 2026/27 matches do
carry a short account number, so the mess is real; the warning simply has no consequence. Harmless, but
it is a documented-defect tell of the kind Gate F warns about, and it buys nothing.

---

## Files / Hygiene: PASS

19 files, 4 formats (14 csv, 2 xlsx, 2 pdf, 1 txt). Two files clear the large-file floor:
`case_payments.csv` 33,851 rows, `mule_account_register.csv` 28,394 rows. Distractors that read as
relevant and go unused: `aml_alert_summary.csv` (alert volumes per member per quarter, no bearing on
the index), `national_scam_statistics_calendar_year.csv` (losses per million **of payment value**, on
calendar quarters, explicitly "any count basis" omitted in the manifest), and
`recovery_statement_2025_26.csv`'s `recovered_stated_gbp` column, which is on a different basis from
the case-level credits the ask demands.

No authoring or benchmark leakage: a grep across every csv, txt, both PDFs' text, and both workbooks'
unzipped XML for "synthetic", "generated", "benchmark", "golden", "placeholder", "capture",
"recapture", "Lincoln", "Petersen", "Chapman", "estimator" and "independen" returns nothing. No hidden
sheets (4 and 2 sheet names, all in-fiction), no tracked changes, no README. Workbook and PDF metadata
carry only "Kelverstone Mutual secretariat" and a 2027-07-02T09:00:00Z timestamp, consistent with the
2 July pull. Temporal coherence holds: the latest date anywhere is 2027-07-01 (register and recovery
credits), inside the declared pull; the trustee pack is dated 14 July 2027 and issued 2 July; member
joining dates, tiers and covers agree between `member_register.csv` and the pack's membership table for
all twelve members. Layer 1 mess reads as genuinely operational: the 2023/24 register in pence with
dd/mm/yyyy dates against the 2024/25-onward layout, thousands against units across the returns sheets,
preliminary and revised vintages on separate sheets, hyphenated against zero-padded account
references, a quarter-end supplement to a mid-quarter feed, a stale month on top-up advice lines, a
recovery statement on a mixed basis. Nothing reads as LLM-authored. No public dataset, so no answer
contamination. One cosmetic wrinkle, not a finding: both PDFs carry a creation date of 2 July 2027
although the standard was approved 19 May 2026, which is consistent with the pack being printed for the
meeting. **No exclusion-level finding.**

## Stump power (Gate F)

Strong. The estimand in 4.2 is a population size with incomplete member-side reporting, and the
decisive work is deciding which register sightings are independent of the member's own detection. Four
wrong landings are live and all of them are reachable by an analyst who cleaned every file correctly:
run the two-source estimate on all 395 matches and file **25**; treat every account the member ever
chased as contaminated, ordering ignored, and file **51** (or 50 on Chapman); truncate the register at
the scheme-year end and file **33** (or 32); divide by the notified forward volume in
`member_register.csv` and file **30**. The naive 25 is the most likely: the matches file hands over a
`case_reference` column, so the 282-row overlap is one line of pandas and the dependence never comes
up unless the solver asks where a registration came from. The only too-easy signal is finding 4's
zero-padding note, which documents a mess that has no consequence; it does not touch the decisive step.
No lever needed.

## Stumping type (Gate G)

`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`.

Every reported number in the pack is fine and none has to be caught as wrong: the register's 400 is a
correct count of what Castlegate recorded, the matching run's 395 is a correct count of matched
payments, the revised returns are correct, and the walk's first line states the recorded figure as
true. Nothing is flipped away from; the standard simply defines a different estimand from the recorded
one, and the difficulty is building the estimator for it, which is method selection on honest data. The
clean-data test confirms it: on perfectly clean data the dependence between a member's own fund-return
request and the receiving firm's registration is still there, because it is a feature of the process
rather than a defect, so the task still stumps. The one artifact that *is* on a wrong basis, the
recovery statement's `recovered_stated_gbp`, sits on a supplementary ask and is neutralised by the
prompt's own "from case-level credits", so it is not a lever and not the stump.

## Three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

The field's own analysis decides it: a mutual's experience rating of a member's scam incidence, where
the member's register under-reports and the quantity to rate on is an estimated incidence per million
payments sent, corrected for the member's own detection capturing only part of its customers' cases.
Swap test: put a hospital's adverse events and patient encounters in and the task does not survive
intact, because the dependence that carries it is the member's own fund-return request causing the
receiving firm to register the account, which is specific to how sending-side APP-fraud recovery and an
industry beneficiary register interact. Layer 1: the 2023/24 register in pence with dd/mm/yyyy dates
against the 2024/25-onward layout, thousands against units in the returns, preliminary against revised
vintages, hyphenated against zero-padded account references, a mid-quarter feed plus a quarter-end
supplement with three reference collisions, a stale settlement month on top-up advice lines, a recovery
statement partly net of agent charges. Layer 2: the two-source estimator and the independence condition
it rests on. The easy route a strong analyst who read every field and rule correctly still takes: run
the estimate on all 395 matches, because the matches file hands over the case reference and the overlap
is 282 without any thought about provenance, and file **25 cases per million** instead of 31; a second
easy route, excluding every account the member ever chased, files **51**. Decisive step is analytical,
not planted, not data semantics and not rule application.

## Fix

**prompt.** Add the clause that pins which month an advice-detail line settles in, for the
unauthorised-fraud-by-tier ask, and confirm which of the two tables is the committed one (reading A,
the advice month, is the better-grounded on 5.1 and the dictionary, and would replace all sixteen
figures). Secondarily, in the blocks, drop the indexed case counts from the graded set or pin the
estimator form, since 688 is Lincoln-Petersen-only while the graded index is invariant. A rerun is
required.
