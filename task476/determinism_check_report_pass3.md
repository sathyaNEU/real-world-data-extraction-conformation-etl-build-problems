# determinism-check report, task476, 2026-10-20 (architecture 2, pass 2: the FIX_NOW re-judge)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no (matches the card)

## Thread verdict (verbatim)

# Verdict, task476 (run r3)

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair required, no rerun. One residual fork (dating survey-found leaks) is noted below as a watch item. The only repair worth considering is to file the estimand's WHAT in the guidelines, never the HOW.

**Why:** The main call (5 of 12: Brennan Hill, Elmwood, Fenwick, Harlow, Ivers) reproduces from the files. Guidelines 2.2 file the estimand as methane "from when the leak began", and survey-found leaks have no observed start. The shipped odor-call log gives 62.6% of known starts in Dec-Mar, against 33% if starts were uniform. That evidence rules out a uniform (midpoint) start. The expected start under the observed monthly profile is then the only estimator of expected emitted methane the data supports. Under it the margins are wide: designated districts sit at 3.68 to 3.77 against the 3.30 line, and the rest at 2.94 or below. The per-day weighting, a 2016-2025 profile and a 2022-2026 profile all give the same five.

**Evidence (recomputed from target/):**

| Item | Result |
|---|---|
| Leaks found in 2026 | Reproduced exactly, all 12 districts, total 891. These are 613 survey finds plus 278 confirmed odor calls, with calls converted from UTC to Central. All sit on cast-iron or bare-steel segments. |
| Dec-Mar share of odor-call starts | 62.6% reproduced. |
| 2026 cost per district | Reproduced to the dollar. Each line is the cost to date, per work order and cost type. The last line per type sums to the closeout total for 1231 of 1231 work orders (summing every line matches none). 2026 cost is the end-2026 value less the end-2025 value, assigned by the leak's segment district. Assigning by cost_center instead gives different numbers (for example Fenwick $306,115 against $350,452). The guidelines say a district's leaks are those on its own mains, which closes that. |
| Interruptions per district | Reproduced exactly for all 12. FLD tickets duplicate DSP tickets (112), deduped per leak and service line (668 left). Each deduped shut-off counts the meters of every premise on that service line. |
| Calls on the 31 Dec / 1 Jan boundary | Two calls fall in 2019/2020 and 2020/2021 local time, outside 2026. |
| Grades | The 2025 relabel (A, B, C to 1, 2, 3) maps cleanly. |

**Forks tested:**

| Fork | Methane per mile result | Designated |
|---|---|---|
| Midpoint start between surveys | Ashby 3.39, Elmwood 4.59, Ivers 3.47, Brennan Hill 3.13 | 3 (Ashby, Elmwood, Ivers) |
| Start at the find | All under 1.5 | 0 |
| Start at the 2025 survey | All over 4.3 | 12 |
| Median seasonal start (not the mean) | Elmwood 3.07 | 4 |
| Clip emission to 1 January 2026 | Elmwood 2.70 | 4 |
| Expected (mean) seasonal start, no clip | Five designated | 5 |

- **Midpoint** is the standard-looking default but is contradicted by the shipped start-month data, so it is the easy-route wrong answer rather than a licensed reading. This is the one watch item: a judge could call it an unfiled method.
- **Median seasonal start** is not the estimator of expected methane, so it does not stand.
- **Clipping** is excluded by the literal "from when the leak began" in guidelines 2.2.
- **Interruptions, ticketed address only:** a competing reading counts only the ticketed address's meters, for example Ashby 84 against 134. The premises file carries service_line_id, and "each customer's service shut off" on a shared line reaches every premise on it. This affects supplementary answers only, and the line-level reading is better supported.

**Files/Hygiene:** PASS.
- 13 files, in 4 formats: 9 CSV, 2 PDF, 1 xlsx, 1 txt.
- Distractors: the LAUF annual report (system-wide, not allocated to districts) and district_customer_counts_2026.xlsx.
- Operational mess is realistic: UTC call times, the grade relabel in 2025, cumulative cost postings, duplicate tickets, shared service lines.
- Dates are coherent with the 03/15/2027 extract. No authoring disclosure found. Not exclusion-level.

**Stump power:** Good. The easy route is the midpoint start, which files Ashby, Elmwood and Ivers (3 districts, Ashby wrongly in and Brennan Hill, Fenwick and Harlow missed). Setting the start to the find date or the 2025 survey gives 0 or 12. A strong model that reads the guidelines and does not tabulate the odor-call start months will plausibly take the midpoint. The cumulative cost-lines trap (sum of postings) and the shared-line meter count hit the asks.

**Stumping type:** mechanism: method_or_model_selection (start-date estimation from the observed seasonal profile), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. The reported inputs are all fine, and the difficulty is choosing the estimator for an unobserved start that the data's own seasonality supports.

**Three rules:** domain: pass, layers: pass, decisive_step: analytical. This is a methane emission inventory in which an LDAR (leak detection and repair) analyst estimates the unobserved start of survey-found leaks, so the swap test fails to make it generic. Layer 1 is UTC calls, the grade relabel, cumulative cost postings, duplicate tickets and shared service lines. Layer 2 is dating leaks from the observed season of starts. The easy route is the midpoint start, which files Ashby, Elmwood and Ivers (3 districts) instead of the golden five.

**Fix:** none. Optionally, the guidelines could file that survey-found leaks' starts are estimated rather than observed, so that the expected-emission estimand is explicit. They must not name the seasonal weighting.
