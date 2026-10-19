# Determinism check, task468 architecture 2 (target.zip f9f35f57b4293ef0)

Verdict DETERMINISTIC, disposition APPROVE, from one isolated judge thread (sonnet, medium) on a fresh unzip, 2026-10-19. The architecture 1 reports are in git history.

# Verdict, task468

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed; optional note only (see Fix). No rerun.

**Why:** The charter (2.1, 2.2, 3.1) files the estimand literally: caseload = members whose fill reaches June 30, 2026; spend = those members' class fills dispensed Jul 2026 to Jun 2027, priced at the Tallis 2026 schedule, reversals excluded; one pharmacist per $1.5M or part. The only open piece is the forward projection method, and the shipped history separates the candidates: forward 12-month spend per member rises steeply with months on therapy, and the June 2026 caseload for AST, CGR and GLP is 73 to 90 percent under 6 months on therapy (step therapy removed Jan 2026). Every duration-aware variant I ran returns the golden counts; the duration-blind routes do not.

**Evidence (recomputed from /target/):**
| Item | Result | Source |
|---|---|---|
| Conformance | Orrin NDC 5-3-2 to 11 digits (zero-pad middle segment) maps all 28 NDCs to the drug list; Orrin 2,700 REVERSAL lines match paid claims exactly (qty, date, member); Tallis 541 R lines each pair with a P; all member keys resolve in the crosswalk; 2,700 resubmitted duplicates survive as separate claim numbers | claims CSVs, crosswalk, drug list |
| Caseload at 6/30/2026 (fill date + supply - 1 >= 6/30) | IMM 433, MS 186, ONC 89, HCV 61, GLP 1,603, HIV 381, AST 220, CF 39, CGR 738. Reproduced exactly | claims, charter 2.1 |
| Projected managed spend, $M (duration-cell method, cap 36) | IMM 18.76, MS 9.75, ONC 6.64, HCV 0.34, GLP 6.93, HIV 8.28, AST 4.95, CF 5.27, CGR 3.69. Rounds to golden 19/10/7/0/7/8/5/5/4 | claims, price schedule |
| Pharmacists | 13/7/5/1/5/6/4/4/3 = 48. Reproduced. Robust to duration cap 12, 24, 36, 48, 60 and to treating the Q1-2019 left-censored members as cap cell or as lower-bound duration (counts identical, $M identical after rounding except ONC 6.9 and AST 5.4, still 7 and 5) | as above |
| Off-by-one on "reaches" (date + supply instead of date + supply - 1) | Caseload shifts slightly (GLP 1,611, ONC 91); pharmacists unchanged | as above |
| Rebates 2025 utilization, $K | IMM 4,735; MS 1,690; ONC 340; HCV 1,226; GLP 760; HIV 754; AST 722; CF 183; CGR 606. Reproduced, each product-quarter rebate counted once. Proof the repeated per-channel value is the product total: channel units sum to the claims' net units (Velmira 2025Q4: 3,732 = 3,732). Summing all lines would give 4x (IMM 14.2M), implausible | rebate statement, claims |

Competing routes and their answers (pharmacists IMM/MS/ONC/HCV/GLP/HIV/AST/CF/CGR):
- Trailing 12 months of caseload members: 13/7/5/1/3/6/3/4/2 (understates new starters).
- H1 2026 x 2: 14/7/6/1/5/6/5/4/4.
- Last 3 months x 4: 15/7/6/2/8/6/6/4/5.
- Last-fill annualized: 14/7/6/4/9/6/7/4/5.
- Duration-blind pooled forward ratio: 13/7/5/1/6/6/5/4/4 (differs on GLP, AST, CGR). Out-of-sample check from June 2025 and June 2024 origins: pooled GLP error -14 percent and -29 percent against duration method +9 and -10 percent, and the forward-spend-by-tenure table shows the heterogeneity plainly. This is a weaker method the data rejects, not an equally licensed one.
Margins to the $1.5M breakpoints are clean (smallest: AST 4.95 vs 4.5, about 0.45M; IMM 18.76 vs 18.0, 0.76M); no method variant crosses one. Minor residual: GLP has 38 caseload members at tenures longer than any cell with a 12-month follow-up; any sensible fill rule moves GLP by about 0.1M (6.93 vs bound 7.5). Not decisive.

**Files/Hygiene:** PASS. 11 files; formats csv, pdf, xlsx (3). One 114,301-row file plus a 19,453-row file. Distractors: Orrin trend report (plan paid at Orrin prices, all members, calendar years), medical_benefit_specialty_drugs_2025.xlsx (outside the program per charter 1.1), formulary bulletin (context). Dates consistent with a July 14, 2026 fiction (claims extracted July 13, notes July 14, charter May 28); no README or authoring language; PDF/xlsx metadata show business authors only. Fictional product names, no real-data contamination. Nothing exclusion-level. Cosmetic: PDFs are sparse but plausible.

**Stump power:** Strong. The plausible easy routes (annualize H1 2026 or recent quarter, or take the trailing year, or a duration-blind ratio) give different counts in 3 to 7 of 9 classes (GLP 3 to 9 vs 5; CGR 2 to 5 vs 3; AST 3 to 7 vs 4; ONC, IMM, HCV shift in some). The trap is the step-therapy-driven young caseload plus early drop-off, which the history exposes. A strong model that cleans everything correctly still fails with a run-rate projection.

**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no. Reported inputs (claims, schedule, trend report) are all fine; difficulty is a duration-conditional persistence forecast with left-censoring on honest data, and it would still stump on perfectly clean data.

**Three rules:** domain: pass, layers: pass, decisive_step: analytical. Domain: managed-care pharmacy forecasting a covered cohort's next-year drug spend by therapy duration (persistence/discontinuation, a survival-type question) to size clinical staffing; swap test fails to read the same elsewhere. Layer 1: PBM switch (two claim layouts, member keys via crosswalk, 10 vs 11-digit NDCs, reversal conventions, 2019-2025 contract prices vs 2026 schedule, rebate channel repeats, utilization vs invoice quarter). Layer 2: duration-conditional forward spend with left-censored starts. Easy route: annualize the current run rate or trailing year (or pool durations), giving e.g. GLP 8 or 3 instead of 5.

**Fix:** none. Optional, no rerun needed: none of the above requires prompt or file change. (If the author wants extra insurance on the one soft spot, nothing in the files should change; the GLP long-tenure cell gap is immaterial to the counts.)
