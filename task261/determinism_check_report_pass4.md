# task261 determinism check, pass 4 (11-01 re-check reship)

Judge thread: one isolated general-purpose thread at medium on a fresh unzip of target.zip (13 files), spawned by the main session from the determinism-judge agent's brief (/tmp/determinism-check-task261-p4/judge_brief.md) because the agent's runtime had no Agent tool. Main-thread disposition of the residual ask forks: (1) the annuity income at the 12 January extract with anniversaries to that date taken back is the literal reading (an anniversary after the extract has not happened; the listing's extract_date column and the key facts' rule); (2) the plotted difference's sign is SF15, the call unchanged under either; (3) a reversion from a death before December is the PDS's from-the-date-of-death term read literally. None moves the call; none filed (a new sentence would narrate the asks' devices).

# Determinism verdict, task261 pass 4

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No rerun needed. Two optional wording pins below (sign convention of the plotted difference, annuity take-back cutoff) are low severity and sit on the asks, not the main call.

**Why:** Executing retirement_range_2027_brief.docx and nhws2025_user_guide.pdf s.7.2 word for word (older-partner placement, difference recomputed on each of the 200 replicates on implicate 1, plus 1.2 x variance of the five implicate differences, rule at 1.96 x SE) gives 258,000 / 95,000 = 2.7 at 55-64 vs 65-74 (apart) and -233,000 / 149,000 = -1.6 at 65-74 vs 75+ (shared), so five segments. The two decisive ratios (2.71 and 1.56) sit clear of 1.96 on their respective sides. All figures in the FINAL_RECOMMENDATION, all supplementary answers and the critical components reproduce. No gate A-E failure.

**Evidence (recomputed from target/):**
- Placement by older of rel 1 and rel 2/3 (nhws2025_persons.csv), weighted medians averaged over 5 implicates: 69,233 / 281,337 / 534,000 / 790,343 / 1,048,229 / 815,286. Reproduces 69/281/534/790/1,048/815 (thousands).
- Group SEs 6,655 / 24,831 / 50,385 / 92,827 / 135,820 / 139,158 round to 7/25/50/93/136/139k. Reproduced.
- Difference, SE, ratio: 212,104/23,733/8.94; 252,663/45,354/5.57; 256,343/76,861/3.34; 257,885/95,175/2.71; -232,943/149,133/-1.56. All reproduce, including rounding of differences from unrounded values.
- Independent-sum SEs (replicates run per group, summed in quadrature): 25,707; 56,171; 105,620; 164,511 (ratio 1.57); 194,453. The 55-64/65-74 boundary then fails the rule, giving four segments. Matches the golden's "165,000, 1.6x". Reproduced.
- Placing by reference-person age (the bulletin basis) gives 55-64 vs 65-74 diff 74,620, ratio 0.81, also four segments. The brief fixes older-partner placement, so this is not a live fork.
- SVG intervals diff +/- 1.96 SE: -525,244 to 59,358 for the last pair (crosses zero), the other four clear zero. Reproduced.
- Customer ask 3, literal reading of brief, PDS s.5 and key facts: alive at 31 Dec 2026 (death date, merged_into followed, annuity-lives 2026 deaths override CRM); non-client partner from Spouse/De facto nominations (DOB as given, de-duplicated against clients); repeated member rows with identical balance and payment taken once; a deceased holder's pension kept only where a Reversionary nomination exists and counted with the survivor household. Result 445 / 1,169 / 742 households, balances 210,509k / 521,126k / 249,685k, payments 11,589k / 30,350k / 18,003k. Exact match.
- Annuity: life in payment at 31 Dec 2026 (reversionary amount only after annuitant death; deferred not yet paying excluded), households 179 / 468 / 280 exact. Income after taking back anniversaries 1 to 12 Jan 2027 (extract_date 2027-01-12) at 3.1 percent CPI / 2.5 percent fixed: 3,653k / 9,041k / 5,510k. Exact match.

**Residual forks (low severity, asks only):**
1. Annuity take-back cutoff. Using every January anniversary (to 31 Jan) gives 3,651k / 9,032k / 5,508k; taking back none gives 3,655k / 9,045k / 5,515k. Only the extract_date column (12 Jan) selects the golden. Defensible and literal (the extract cannot contain increases after 12 Jan), and the key facts table has a "1 Nov 2026 to 31 Jan 2027" row pointing at the issue, but the third digit is sensitive.
2. Sign of the plotted/tabled difference is not stated (later minus earlier assumed). Reversing gives +233,000 and an interval of -59,000 to 525,000; the conclusion is unchanged.
3. Reversionary pension of a holder who died before December: the PDS ("from the date of your death") supports counting it; a December-only reading gives 445 / 1,166 / 741. The PDS wording favours the golden.

**Files/Hygiene:** PASS. 13 files; formats csv (7), pdf (4), xlsx, docx; household summary 29,940 rows. Distractors usable: nhws2025_results_bulletin.xlsx (reference-person bands, different cuts, RSE only), retirement_customer_research_2026.pdf (preferences, not finances). No authoring or synthetic disclosure found in PDFs, docx or xlsx metadata; dates coherent with a 12-13 Jan 2027 fiction. No exclusion-level finding. Real-looking mess (merged clients, duplicate rows, stale nominee DOBs, different keys across extracts) reads as system output.

**Stump power:** Strong. The easy route (each group's SE from the replicates, summed in quadrature, or placing by reference-person age as the bulletin does) is clean, uses correct numbers and files four segments, with the 55-64/65-74 boundary wrongly merged. Only treating the difference as a replicate-weighted statistic, which captures the 0.70 correlation from the shared areas, gives five. A model that merges 65-74 with 75+ is right; a model that also merges 55-64 is off the call. Customer-side ETL (merges, reversionary, non-client partners, annuity take-back) gives the asks several independent failure points.

**Stumping type:** `mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported numbers are fine; the difficulty is the SE of a difference between two medians drawn from the same clustered sample, which stays on clean data.

**Three rules:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: merged client numbers, a register that lags annuity deaths, partners known only from nominations, repeated rows, reversionary continuation. Layer 2: design-based inference on the difference of medians (replicate weights plus imputation variance with covariance retained) deciding segment boundaries, a survey-methods task. Swap test: a "visits" or "hospital" noun swap does not preserve the survey-inference content. Easy route: independent SE sum, ratio 1.57 at the 65 boundary, four segments instead of five.

**Fix:** none required. Optional (prompt or brief wording, no change to the stump): state "later group minus earlier group" for the plotted difference, and state that annuity amounts are as paid at the extract date.
