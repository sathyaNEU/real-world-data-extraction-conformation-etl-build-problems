# determinism-check report, task146, 2026-10-16, round 2

The judge ran at stage 4, isolated, at medium effort, on a fresh unzip of the rule 3 repair's cut (commit 67e305d,
target.zip sha256 a040f6c10bb1b148); the call then was 16,000. The strengthening since added the month of the refusal
to the refiling and moved the call to 17,000, so this verdict is history; the shipped cut's verdict is
`determinism_check_report.md`. Verbatim:

# Verdict (task146, fresh re-judge)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. No repair needed; every graded figure reproduced from the shipped files, no rerun required.

**Why:** The main call (16,000) is the additive, region-by-region refiling model that the technical notes' mechanism (s2.3: a monetarily ineligible claimant may file again once the base period moves) and the history jointly force. Q3 2026 left 30,182 ineligible determinations, 48.5% in Western, Coastal and Island, and those three regions pass about 26 to 32% of their closing-quarter ineligibles into the next quarter's first claims week, against under 6% elsewhere. The competing answers (national-rate refiling about 13.6k, seasonal step about 13 to 14k, year-on-year about 12k) are rejected by the filed history, not by a reading choice. Supplementary tables (layoff notices by region and period, industry change) are forced by technical notes s2.1, s5 and the filed concordance and reproduce exactly.

## Literal reading
- Prompt: first report = advance count (notes s3.1), week ended Sat 10 Oct 2026 = claims week 4 to 10 Oct, belongs to October (s2.1), the first claims week of Q4. Method is open; the data separates the candidates (below). Rounding stated in the asking sentence. No population/window/unit silence found that moves an answer.
- Silent points and what each literal reading gives: (a) dedup of register vs portal copies (same business no., first layoff, sites): count once, golden; counting twice would double 73 notices (not licensed, same notice); (b) region of site, not employer region (s5 states it; portal `region` column is the employer's and mismatches the site locality on 158 rows); (c) a withdrawn amendment: notes say amended replaces the original and withdrawn counts nothing, so neither counts (LN-2026-00705 over 00641); (d) "may be kept on, will amend if so" notes: no amendment filed, full count stands; (e) week-month rule for industry (Sunday's month): Jul to Sep 2025 = weeks starting 6 Jul to 28 Sep, 13 weeks each year.

## Evidence (recomputed from target/)
| Item | Golden | Recomputed | Source |
|---|---|---|---|
| 3 Oct 2026 advance national | 11,695 | 11,695 | ui_weekly_claims_release PDF; uics csv (all 8 regions sum) |
| Q3 2026 monetarily ineligible, national | 30,182 | 30,182 (Jul+Aug+Sep, 8 regions) | ui_program_statistics FY2026-27 |
| W+C+I share | 48.5% | 14,641/30,182 = 48.5% (7,127 + 4,759 + 2,755); usual median 19.7%, mean 21.5% | same |
| Turns in regression | 50 | 50 (Apr 2014 to Jul 2026) | brs csv (day-first, region codes via regions csv) joined to uics at 27 Jun 2021; old FY sheets parsed (INSUFFICIENT block), 153 months |
| Slopes (per-region change on closing-quarter ineligible, intercept per quarter-of-year) | W ~1/4, C and I ~3/10, others <0.1 | W 0.263, C 0.302, I 0.319, N 0.039, Cap 0.014, E 0.037, M 0.010, S 0.052 | computed |
| Refiling in target week | 4,000 to 5,000, ~9/10 in W/C/I | about 4,590, 91% in W/C/I | computed |
| Rest of week | 11,000 to 12,000 | about 11,450 | computed |
| National call | 16,000 | 16,038 (region x qoy intercepts), 16,082 (common qoy intercept), 15,995 (2018+ only), 16,137 (2021Q3+), 15,973 (W/C/I vs other pooled slopes), 15,969 (level form with lag), 16,094 (W/C/I only), 16,247 (no intercept). Times the historic advance/revised ratio 0.994 these sit 15.9k to 16.15k. All round to 16,000 | computed |
| Out-of-sample (leave one turn out, national step RMSE) | region build best | region build 374, one national share 591, seasonal intercepts only 914; F-test region vs one share F=190, p<0.001 | computed |
| Layoff table (region x Oct 11-31 / Nov / Dec) | listed | all 24 cells identical (e.g. Western 198/697/555, Coastal 300/828/242) | register xlsx + portal csv + case notes: 89 open register layoffs, 73 re-keyed on portal and dropped, 34 withdrawal notes applied (3 register withdrawals incl. ES/26/0247, 0195, 0140, 0114, 0253), 9 superseded, reduced-hours out |
| Industry change (14 groups) | listed | all 14 identical (Construction 58.9, Accommodation 21.6, Information -11.8, Fin/ins/prop -7.0, ...). Totals 155,938 and 170,551 tie to the uics national initial claims for the same weeks | ic_open_data N+A, Saturday labels and SIC 2006 before 4 Jan 2026, Sunday and SIC 2023 after; groups via concordance + divisions csv; all 2006 divisions map to a single group |

Competing answers tested:
- National determinations at the national rate (6.5%): 13.4k to 13.6k, call 13,000 or 14,000. Loses out of sample (591 vs 374 RMSE) and ignores that the same file shows where the refusals sit.
- Seasonal first-week step only: about 13k. RMSE 914.
- Year-on-year (11,000 last year x 1.082): about 12k. Ignores the refusals mechanism entirely.
- Surviving thin alternative: a log-ratio (multiplicative, ineligible/base-week) region build gives 16,719, i.e. 17,000. Overall leave-one-out RMSE is close (390 vs 374) but it is worse on the highest-leverage turns (RMSE 381 vs 303 on the top eight W/C/I turns, over-predicting the three biggest) and has no mechanism (refilers are counts, not a share of the base week); 2026Q4 sits beyond the history's highest closing-quarter W/C/I count (14,641 vs 12,674), where the additive form is the better-validated one. Not treated as defensible; recorded as the one residual spec-sensitivity. Residual forecast SD about 340 to 370, so 16,000 has about 500 of room either side of the point estimate.
- Layoff notices with first layoff in the target week (305 workers) and the base week (670): small, not decisive, and not enough to move the thousand.

## Gates
- A: pass (all values reproduce; no overclaim; attribution correct; advance vs revised handled, effect under 100).
- B: pass. Mechanism, advance/revised, week-month rule, notice rules, region-of-site, amendment/withdrawal: all in technical notes (text) or in files. No external dependency. Note vocabulary (refile, ineligible, advance) present in notes and workbook.
- C: pass with the log-ratio caveat above. Margin of the call is robust across the licensed additive specifications.
- D/E: pass. The prompt fixes the week, the "first report", units and rounding; difficulty is the forecast model, not a word.

## Files/Hygiene
PASS. 16 files; formats csv (9), xlsx (3), pdf (2), json (1); one file 189,677 rows (ic_open_data), another 3,128 + 2,200 weekly rows; distractors present and unused: lfs_regional_unemployment, online_job_ads_index, public_holidays (no holiday in 4 to 10 Oct; Labour Day 26 Oct), desk_data_log is a provenance log, no README/benchmark language. Realistic mess: day-first dates, mixed d/mm/yyyy and dd.mm.yyyy strings in the register, UTC lodged stamps, system change in Jun 2021 with different layouts and headings (sufficient/insufficient), FY-sheet layout change, ES vs LN keys in free-text case notes, org-name case variants. Temporal coherence good (nothing after the 8 Oct release/7 Oct exports). Fictional jurisdiction, no public-data contamination. Case notes show templated phrasing but within normal officer-note variety; no exclusion-level finding. Cross-batch check not possible within the isolation rules (no other task folder readable); none seen.

## Stump power
Moderate and genuine. A strong model that cleans everything and reads the notes will still plausibly file a national-rate refiling (13 to 14k) or a seasonal step (12 to 13k) unless it tests whether refusals sit regionally and validates the region build out of sample; the notes flag the mechanism but never its regional pass-through. The asks (day-first/mixed-format register, duplicate, amend and withdraw logic from free-text notes, SIC 2006/2023 reclassification with Saturday vs Sunday labels) are heavy and independently graded, so total score should sit well below the call-only 45%.

## Stumping type
`mechanism: forecasting` (region-level method selection validated out of sample, etl_conformance for the asks), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Reported numbers are all correct (release, programme statistics, open data); the difficulty is a forward projection the correctly read past does not pin to the national average. On clean data the task would still stump.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Swap test: replace claims with "visits" or "megawatt-hours" and the regional refiling pass-through (benefit-eligibility base-period mechanics, refiler flow by region, advance vs revised publication) no longer reads the same; the deciding quantity is one a labour-statistics unit would estimate and back-test.
- Layer 1: day-first dates, regional codes, claims-system change, advance/revised, fiscal-year sheets, SIC reclassification, register vs portal re-keying, free-text notes. Layer 2: forecasting the first report of a quarter-turn week by region-level refiling shares validated leave-one-out.
- Easy route: take the national ineligible count at the national refile rate (about 6.5%) or the average Q4 first-week step and file 13,000 to 14,000 instead of 16,000, with every field and rule read correctly. Regional heterogeneity is a modelling choice, not a stated rule or a planted defect.

## Fix
none. Optional note for the author only: the solution text's "one intercept per quarter of the year" can be read as common or per-region (16,082 vs 16,038, both 16,000); no change needed.
