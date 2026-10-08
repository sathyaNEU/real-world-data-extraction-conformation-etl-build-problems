# DA38 — Privacy-bucketed rates: report what the ranges allow, not what the midpoints suggest

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Analytics on privacy-protected outputs (k-anonymity buckets, ranges in public dashboards, bucketed ad-reach estimates) where only intervals are published |
| Domain | Education accountability |
| Task shape | 10 · Scorecard against thresholds (districts × subgroups → bounds on proficiency rate; which districts certainly, possibly or certainly not meet the 40% target) |
| Core method | Each school-level percentage is published as a range (e.g., "20-29", "GE50", "LT5") with the number of valid test-takers; district rate bounds = Σ (lower bound × n) ÷ Σ n and Σ (upper bound × n) ÷ Σ n; classification by whether the target lies above, below or inside the bounds |
| Analytical stump | Midpoint substitution produces a single number that looks precise and can misclassify districts near the target; wide ranges for small schools ("GE50", "LE10") carry little information. Bounds respect the published information and show which classifications are determined |
| Primary sources | U.S. Department of Education EDFacts assessment data files (school-level proficiency, range-coded) |

## 1. The real-world situation

A state accountability office flags districts whose students with disabilities fall below 40% proficiency in mathematics, using the public
EDFacts school files. An analyst replaced each range with its midpoint, averaged weighted by test-takers, and flagged 37 districts. A district
appealed, showing that its true rate (from internal data) was above 40%.

## 2. The decision (one deterministic recommendation)

**The classification of each district in scope (certainly below, certainly at or above, undetermined) for students with disabilities in
mathematics, and the list flagged for intervention (certainly below only).**

Rules (accountability memo):

* Data: EDFacts school-level mathematics assessment file for the school year in the memo; subgroup "children with disabilities (IDEA)";
  all grades combined (the "00" or memo-specified grade field).
* Range parsing: "a-b" → [a, b]; "GEa" → [a, 100]; "LEa" → [0, a]; "LTa" → [0, a); "GTa" → (a, 100]; exact values → [v, v]; suppressed
  ("PS") → [0, 100] with n retained; per the memo's parsing table.
* District bounds: Σ L_i n_i ÷ Σ n_i and Σ U_i n_i ÷ Σ n_i over schools with n_i > 0.
* Classification: upper < 40 → certainly below; lower ≥ 40 → certainly at or above; otherwise undetermined.
* Flag list: certainly below.
* Report the midpoint estimate for contrast.

## 3. Why capable analysts get it wrong

* Midpoints are the standard quick fix for ranged data.
* Ranges are deliberately coarse for small groups; midpoints manufacture precision.
* Open-ended ranges ("GE50") have no midpoint without assumptions.
* Suppressed schools still count toward denominators; dropping them biases bounds.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `math-achievement-sch-sy<yyyy-yy>.csv` | CSV | ~1–2M (school × subgroup × grade) | ED EDFacts data files | U.S. Gov public domain | Range-coded proficiency, valid counts |
| 2 | `math-achievement-lea-sy<yyyy-yy>.csv` | CSV | ~400k | ED EDFacts | Public domain | District-level ranges (validation) |
| 3 | `edfacts_assessment_documentation.pdf` | PDF | — | ED | Public domain | Range rules, suppression |
| 4 | `range_parsing_table.json` | JSON | ~20 | Task author | — | Parsing rules |
| 5 | `districts_in_scope.csv` | CSV | ~200 | Task author | — | State districts |
| 6 | `accountability_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `analyst_midpoint_flags.xlsx` | XLSX | 37 | Task author | — | Midpoint flags |
| 8 | `bounds_check.json` | JSON | ~5 | Task author | — | Toy district |

## 5. Deterministic solution path

1. Filter state, subgroup, subject, grade field.
2. Parse ranges into bounds; keep n for suppressed rows.
3. District bounds; classification; flag list.
4. Compare with district-level published ranges and with the midpoint flags.

## 6. Wrong paths (method errors, not misreadings)

**A — midpoints.** False precision; misclassification near the target.

**B — dropping suppressed schools.** Biased bounds.

**C — unweighted averaging of school bounds.** Ignores n.

**D — treating "GE50" as 50.** Lower bound used as a point.

## 7. Why the stump is analytical, not semantic

The parsing and bounds are specified. The trap is turning interval-censored information into points.

## 8. Draft task prompt (prose)

> Which districts must we flag for students with disabilities in mathematics? Use bounds from the range-coded school files as the accountability
> memo specifies, and only flag districts that are certainly below 40%. Provide `district_bounds.csv` (district: students, lower, upper,
> midpoint estimate, class), `bounds_chart.png` (interval per district with the 40% line), and a one-page `intervention_flags.pdf` addressing the
> appealing district.

## 9. Deliverables

* `district_bounds.csv`, `bounds_chart.png`, `intervention_flags.pdf`.

## 10. Where 25+ rubric criteria come from

* Flag list (each a criterion); classification counts; bounds for 10 districts; the appealing district; midpoint contrast.

## 11. Golden-output checklist

* Filters; parsing; suppressed handling; weighting; classification.

## 12. Build notes (scope tuning)

* Confirm that some midpoint-flagged districts are undetermined or certainly at/above under bounds.
