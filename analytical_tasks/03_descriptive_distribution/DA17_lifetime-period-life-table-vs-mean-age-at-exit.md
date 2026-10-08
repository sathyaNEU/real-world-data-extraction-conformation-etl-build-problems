# DA17 — Expected lifetime versus average age at exit: the age structure answers a different question

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Customer-lifetime estimation at subscription companies (average tenure of churned customers versus expected lifetime from current churn hazards); employee tenure analytics |
| Domain | Demography / actuarial analytics |
| Task shape | 07 · Grid of cells (6 countries × 2 sexes → period life expectancy at 65 versus mean age at death among deaths 65+; the market whose annuity pricing assumption is revised) |
| Core method | Period life table from deaths and exposures by single year of age (mx → qx with the memo's ax convention, open interval at 110+); remaining life expectancy at 65; contrast with mean age at death of those dying at 65+ in the same year |
| Analytical stump | The mean age of people who die in a year reflects the population's age structure (past births, migration, cohort sizes), not current mortality. A growing older population or a large retiring cohort moves the mean age at death without any change in hazards. Life expectancy needs age-specific rates |
| Primary sources | Human Mortality Database (deaths and exposure-to-risk by single year of age) |

## 1. The real-world situation

An insurer prices annuities in six markets. A pricing analyst updated longevity assumptions using "average age at death among people who
died aged 65+" from death counts, concluding that longevity had barely improved in two markets. The actuarial reviewer insisted that the
annuity assumption must come from period life expectancy at 65 computed from age-specific death rates.

## 2. The decision (one deterministic recommendation)

**The market(s) whose annuity longevity assumption is revised: those where period e65 (latest year) differs from the current assumption by
more than 0.5 years, with e65 per sex.**

Rules (actuarial memo):

* Data: HMD Deaths_1x1 and Exposures_1x1 for the six countries; latest common year in the memo.
* mx = deaths ÷ exposure by age 65–109; open interval 110+: m = deaths ÷ exposure, a = 1 ÷ m.
* ax = 0.5 for ages 65–109; qx = mx ÷ (1 + (1 − ax) mx); lx from l65 = 100,000; Lx = lx+1 + ax dx; Tx and ex per standard life table.
* e65 per sex; compare with `current_assumptions.csv`.
* Mean age at death (contrast) = Σ (age + 0.5) × deaths ÷ Σ deaths over 65+.
* Revise where |e65 − assumption| > 0.5 for either sex.

## 3. Why capable analysts get it wrong

* Mean age at death is intuitive and available from death counts alone.
* It mixes mortality with population composition; it is not a survival measure.
* Exposures are needed; deaths alone cannot give hazards.
* The open age interval matters for e65 in long-lived populations.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–6 | `<CNTRY>.Deaths_1x1.txt` (6 countries) | Fixed-width text | ~10–25k each | Human Mortality Database | CC BY 4.0 (HMD terms; verify) | Deaths by age, year, sex |
| 7–12 | `<CNTRY>.Exposures_1x1.txt` | Fixed-width text | ~10–25k each | HMD | CC BY 4.0 | Exposures |
| 13–18 | `<CNTRY>.fltper_1x1.txt` | Fixed-width text | ~10–25k each | HMD | CC BY 4.0 | Published life tables (validation) |
| 19 | `hmd_methods_protocol.pdf` | PDF | — | HMD | CC BY 4.0 | Life-table conventions |
| 20 | `current_assumptions.csv` | CSV | 12 | Task author | — | Current e65 assumptions |
| 21 | `actuarial_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 22 | `analyst_mean_age_at_death.xlsx` | XLSX | 12 | Task author | — | Naive measure |

## 5. Deterministic solution path

1. Load deaths and exposures; select year and ages.
2. Build life tables by sex and country; e65.
3. Mean age at death for contrast; compare e65 with assumptions; revision list.
4. Validate against HMD published tables (small differences from ax conventions documented).

## 6. Wrong paths (method errors, not misreadings)

**A — mean age at death.** Age-structure driven.

**B — crude death rate 65+.** Composition again.

**C — ignoring the open interval.** e65 biased.

**D — using qx = mx.** Overstates survival at high mortality ages.

## 7. Why the stump is analytical, not semantic

The life-table construction is specified. The trap is substituting a composition-dependent mean for a hazard-based expectation.

## 8. Draft task prompt (prose)

> Which markets' annuity longevity assumptions need revising? Build period life tables from HMD following the actuarial memo and compare e65
> with our assumptions. Provide `e65_grid.csv` (country × sex: e65, assumption, gap, mean age at death), `e65_vs_mean_age.png`, and a one-page
> `assumption_review.pdf`.

## 9. Deliverables

* `e65_grid.csv`, `e65_vs_mean_age.png`, `assumption_review.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 cells × (e65, gap) = 24; mean ages; revision list; validation notes.

## 11. Golden-output checklist

* Age range; ax convention; open interval; Tx; comparison; list.

## 12. Build notes (scope tuning)

* Choose countries with different age structures (e.g., one with a large baby-boom cohort entering 65+).
* Confirm the naive measure suggests no change in at least one market that the life table revises.
