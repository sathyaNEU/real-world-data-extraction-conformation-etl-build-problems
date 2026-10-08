# AD26 — Suspicious score gains: thousands of schools, an overdispersed null, and small cohorts that swing

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Test-integrity screening at assessment providers and school systems; retail and franchise performance screens for units whose numbers jump and then revert |
| Domain | Education / assessment integrity |
| Task shape | 01 · Ranked list under a cap (30 school–grade cohorts for forensic review) |
| Core method | Cohort-matched gains (grade g in year t versus grade g−1 in year t−1); a "gain-then-reversal" statistic; standardisation by cohort size; Efron's empirical null (central matching of z-scores) and local FDR instead of the theoretical N(0,1) null |
| Analytical stump | With thousands of cohorts, ordinary year effects and test-form differences make z-scores overdispersed; the theoretical null flags hundreds. Small cohorts swing by chance and regress. The signal is a large gain *followed by a large reversal for the same students*, judged against an empirical null |
| Primary sources | California Assessment of Student Performance and Progress (CAASPP) research files (school × grade × subgroup mean scale scores) |

## 1. The real-world situation

A state assessment office reviews **30** school–grade cohorts per year for possible testing irregularities. Last year's screen flagged
every cohort whose mean scale score rose by more than two standard deviations of all school gains; it produced over 400 flags, mostly small
schools, and the review team could not separate noise from irregularities.

## 2. The decision (one deterministic recommendation)

**The 30 cohorts sent for forensic review, ranked by local false-discovery rate, and the 31st.**

Rules (assessment integrity memo):

* Data: CAASPP research files, ELA and mathematics, all students subgroup, years 2016–2019; school × grade rows with students tested ≥ 20.
* Cohort gain G1 = mean score(grade g, year t) − mean score(grade g−1, year t−1) for the same school; follow-on change G2 = mean
  score(grade g+1, year t+1) − mean score(grade g, year t).
* Standardise each against the state distribution for that grade pair and subject: z1, z2 scaled by √n ÷ √(median n).
* Statistic: s = (z1 − z2) ÷ √2 (large gain then reversal).
* Fit Efron's empirical null to s by central matching over the middle 50% (estimate δ0, σ0); compute local fdr with the memo's density
  estimator; candidates have fdr < 0.2.
* Rank candidates by fdr (ties by s); top 30; report #31.

## 3. Why capable analysts get it wrong

* One-year gain screens ignore that genuine improvement persists while irregular gains reverse.
* Theoretical null p-values assume the null is N(0,1); with common shocks and form effects it is wider and shifted.
* Small cohorts produce extreme gains by chance; scaling by size matters.
* Comparing grade g this year with grade g last year compares different students.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `sb_ca2016_all_csv_v3.txt` … `sb_ca2019_all_csv_v3.txt` | Delimited text | ~3.2M each | California Department of Education CAASPP research files | Public data (CDE terms; cite) | Scores by entity, grade, subgroup |
| 5–8 | `sb_ca20xx_entities_csv.txt` | Delimited text | ~11k each | CDE | Public | School/district identifiers |
| 9 | `caaspp_research_file_layout.pdf` | PDF | — | CDE | Public | Field definitions, suppression |
| 10 | `subgroup_codes.json` | JSON | ~200 | Task author from CDE layout | — | Subgroup mapping |
| 11 | `assessment_integrity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 12 | `last_year_flags.xlsx` | XLSX | ~400 | Task author | — | One-year gain flags |
| 13 | `efron_empirical_null_citation.pdf` | PDF | — | Efron (2004) JASA (cite) | Cite | Method |

## 5. Deterministic solution path

1. Load files; filter subgroup, minimum n; link cohorts across years and grades by school code.
2. Compute G1, G2, standardised z1, z2 and s.
3. Fit the empirical null by central matching; local fdr; candidates.
4. Rank; top 30 + #31; compare with last year's flags.

## 6. Wrong paths (method errors, not misreadings)

**A — one-year gains with a 2 SD cut.** Hundreds of noise flags.

**B — same-grade year-over-year comparisons.** Different students.

**C — theoretical null.** Overdispersion produces many false discoveries.

**D — no size scaling.** Small schools dominate.

## 7. Why the stump is analytical, not semantic

Linking, statistics and null-fitting rules are explicit. The traps are multiple testing under an overdispersed null and cohort mismatch.

## 8. Draft task prompt (prose)

> Give me this year's 30 cohorts for forensic review using the gain-then-reversal screen in the integrity memo, judged against an empirical
> null. Provide `cohort_screen.csv` (cohort: n, G1, G2, s, fdr, rank), `s_distribution.png` (histogram of s with the theoretical and empirical
> nulls), and a one-page `review_list.pdf` including how many of last year's flags would survive.

## 9. Deliverables

* `cohort_screen.csv`, `s_distribution.png`, `review_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 30 cohorts + #31; δ0 and σ0; s and fdr for 8 cohorts; count of theoretical-null flags; overlap with last year.

## 11. Golden-output checklist

* Cohort linking; scaling; statistic; central matching; fdr; ranking.

## 12. Build notes (scope tuning)

* Publish the density estimator settings so fdr is reproducible.
* Confirm σ0 > 1.2 so the theoretical null visibly over-flags.
