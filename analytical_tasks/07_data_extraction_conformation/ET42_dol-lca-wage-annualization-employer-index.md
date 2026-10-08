# ET42 — Entry-level wage reliance index from H-1B LCAs: units of pay, positions vs cases, and "Certified – Withdrawn"

| Field | Value |
|---|---|
| Domain | Immigration compliance / HR compensation benchmarking / labor policy research |
| Objective family | Anomaly Detection & Diagnostics |
| Task shape | 16 · Indicators into one score (composite index behind an eligibility screen) |
| Core technique | Unit-of-pay annualization on both sides of a ratio; position-weighted indicators; status-lifecycle semantics; deterministic employer-name normalization; min–max scaling and weighting |
| Trap family (honest data) | Hourly prevailing wage vs annual offered wage; case counts instead of positions; withdrawn certifications mis-classified; E-3/H-1B1 rows included |
| Primary sources | U.S. DOL OFLC LCA Disclosure Data (H-1B, H-1B1, E-3), OFLC record layout, prevailing-wage level guidance |

## 1. The real-world project

A labor-policy research group publishes an annual index of employers' reliance on entry-level (Level I) prevailing wages
in H-1B Labor Condition Applications and selects **one employer** for a deep-dive case study. Last year's pick was an
employer whose "offered wage was 40× the prevailing wage" — an hourly prevailing wage divided into an annual salary.

## 2. The business decision (one deterministic recommendation)

**Which employer has the highest Entry-Level Wage Reliance Index for FY2023, and by how much does it lead the second?**

Rules (index methodology):

* Records: `VISA_CLASS = H-1B`; `CASE_STATUS` in {Certified, Certified - Withdrawn}; full-time positions.
* Employer = `EMPLOYER_NAME` normalized: upper case, punctuation removed, whitespace collapsed, trailing legal-form tokens
  removed (INC, LLC, LLP, LP, CORP, CORPORATION, CO, LTD, PC). Eligibility: ≥ 200 positions (Σ `TOTAL_WORKER_POSITIONS`).
* Annualize wages: Hour × 2080, Week × 52, Bi-Weekly × 26, Month × 12, Year × 1 — offered wage from
  `WAGE_RATE_OF_PAY_FROM` with `WAGE_UNIT_OF_PAY`; prevailing wage from `PREVAILING_WAGE` with `PW_UNIT_OF_PAY` (units can
  differ within a record).
* Indicators (all weighted by positions):
  I1 share of positions at `PW_WAGE_LEVEL = I` (weight 0.40);
  I2 1 − median(offered ÷ prevailing) (weight 0.30);
  I3 share of positions with offered ≤ 1.02 × prevailing (weight 0.20);
  I4 Certified-Withdrawn positions ÷ all certified positions (weight 0.10).
* Each indicator min–max scaled across eligible employers (0–1, higher = more reliance); index = weighted sum.
* Rank descending; ties by more positions.

## 3. Why this gets overlooked in real projects

* Offered wage and prevailing wage each carry their own unit-of-pay field; a single annualization step applied to one side
  produces ratios in the tens.
* Case rows bundle multiple positions; counting cases understates large filings.
* "Certified - Withdrawn" is a certified LCA later withdrawn by the employer — neither simply certified nor simply withdrawn.
* E-3 (Australian) and H-1B1 (Chile/Singapore) LCAs share the file.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–4 | `LCA_Disclosure_Data_FY2023_Q1.xlsx` … `_Q4.xlsx` | XLSX | ~150–250k each | DOL OFLC Performance Data | U.S. Gov public domain | LCA records |
| 5 | `LCA_Worksites_FY2023_Q4.xlsx` (if published) | XLSX | ~100k+ | DOL OFLC | Public domain | Additional worksites (context) |
| 6 | `LCA_FY2023_Record_Layout.pdf` | PDF | — | DOL OFLC | Public domain | Field definitions, status values |
| 7 | `prevailing_wage_levels_guidance.pdf` | PDF | — | DOL ETA | Public domain | Wage-level meaning |
| 8 | `oflc_wage_library_extract_fy2023.csv` | CSV | ~50k | FLAG/OFLC Wage Search data | Public domain | Optional PW cross-check |
| 9 | `index_methodology.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `legal_suffix_tokens.json` | JSON | ~10 | Task author | — | Normalization list |
| 11 | `soc_2018_structure.xlsx` | XLSX | ~1.4k | BLS SOC | Public domain | Occupation context |

## 5. Deterministic solution path

1. Union quarters (latest quarter's file is cumulative — confirm and de-duplicate by `CASE_NUMBER`, keeping the latest
   decision).
2. Filter visa class, status, full-time; normalize employer names; apply the eligibility floor.
3. Annualize both wages per record; compute indicators position-weighted.
4. Min–max scale; weight; rank; top employer and lead.
5. Contrast: one-sided annualization; case counts; status handling; visa classes.

## 6. The traps

**Trap A — one-sided annualization.** Ratios explode for hourly-PW records; I2/I3 distorted; leader changes.

**Trap B — cases not positions.** Employers filing many multi-position LCAs move.

**Trap C — status mishandled.** I4 wrong; or withdrawn-only cases included.

**Trap D — cumulative quarterly files unioned.** If quarterly files are cumulative, unioning duplicates cases.

**Trap E — visa classes.** E-3/H-1B1 rows shift small employers over the floor.

## 7. Why the data is honest

The disclosure data are DOL's official records of filed applications; units and statuses are documented. The index method
is fully specified.

## 8. Draft task prompt (prose)

> We feature one employer each year: the highest scorer on our Entry-Level Wage Reliance Index. Using the FY2023 LCA files
> and the methodology in the folder, compute the four indicators for every eligible employer, combine them and tell me who
> we feature and by how much they lead. Deliver `wage_reliance_index.csv` (one row per eligible employer: positions, the
> four raw indicators, scaled indicators, index, rank) and `index_components.png`, a stacked bar chart of the top fifteen
> employers showing each indicator's weighted contribution. Add a one-page `feature_memo.pdf` naming the employer, its
> lead, and which indicator drives the lead.

## 9. Deliverables

* `wage_reliance_index.csv`, `index_components.png`, `feature_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Top 15 employers × (index, rank) + raw indicators for top 3; leader and lead; driving indicator; eligibility count.

## 11. Golden-output checklist

* Both wages annualized by their own units; positions; statuses; H-1B only; de-duplicated cases; decision stated.

## 12. Build notes (scope tuning)

* Verify whether FY2023 quarterly files are cumulative; design the union rule accordingly.
* Confirm Trap A changes the leader (look for employers with many hourly prevailing wages).
