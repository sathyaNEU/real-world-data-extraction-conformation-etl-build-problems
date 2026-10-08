# DA24 — Spending per household or per person? Neither: per equivalised adult

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Household-level versus per-user metrics in subscriptions and telecom (family plans), retail basket analytics, and affordability analyses |
| Domain | Consumer economics / affordability |
| Task shape | 14 · Cuts of a distribution (quintile boundaries of equivalised income and the median share spent on energy and broadband per quintile; the quintile defined as "burdened" for a discount programme) |
| Core method | OECD-modified equivalence scale (1 + 0.5 per additional adult + 0.3 per child) applied to household income; household weights × number of persons for person-level distributions per the memo; quintiles on equivalised income; median spending shares per quintile |
| Analytical stump | Household income ranks large households as richer than they are per person; per-capita income overstates the needs of each extra member. Quintiles on unadjusted household income put many large, low-income-per-person households in upper quintiles, changing who appears burdened |
| Primary sources | U.S. Bureau of Labor Statistics Consumer Expenditure Survey (CE) public-use microdata — Interview survey |

## 1. The real-world situation

A utility and broadband provider is designing a discount for customers in the most burdened income group. The analyst built quintiles on
household income from the CE Interview survey and found energy-plus-broadband shares highest in the bottom quintile and flat above. A policy
reviewer argued that households should be compared on an equivalised basis and that large families were misplaced.

## 2. The decision (one deterministic recommendation)

**The equivalised-income quintile designated "burdened" (the highest quintile whose median energy-plus-broadband share exceeds 8%), and the
equivalised income threshold that defines eligibility.**

Rules (affordability memo):

* Data: CE Interview FMLI files for the four quarters of the year in the memo; consumer units with complete income reporting (imputed values
  accepted as published).
* Spending: quarterly expenditures on electricity, natural gas, other fuels and internet services (UCC lists in the memo), annualised (×4 per
  quarter's interview).
* Income: after-tax income (`FINATXEM`).
* Equivalence: OECD-modified scale using household composition (adults = members 14+).
* Weights: `FINLWT21` ÷ 4 for pooling quarters; person-level quintiles use weight × persons (memo).
* Quintile boundaries on equivalised income; median share (spending ÷ income) per quintile; consumer units with income ≤ 0 excluded from
  share medians.
* Burdened = highest quintile with median share > 8%; eligibility threshold = its upper boundary.

## 3. Why capable analysts get it wrong

* Household income is the field on the record.
* Needs scale with household size, but not proportionally (economies of scale).
* Weighting quintiles by households versus persons changes boundaries.
* Quarterly interviews must be annualised and weights pooled correctly.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `fmli<yy>1x.csv` … `fmli<yy>4.csv` | CSV | ~5k each | BLS CE PUMD | U.S. Gov public domain | Consumer-unit characteristics, income, weights |
| 5–8 | `mtbi<yy>1x.csv` … `mtbi<yy>4.csv` | CSV | ~150k each | BLS CE PUMD | Public domain | Monthly expenditures by UCC |
| 9–12 | `memi<yy>1x.csv` … | CSV | ~12k each | BLS CE PUMD | Public domain | Members (ages) |
| 13 | `ce_pumd_interview_dictionary.xlsx` | XLSX | — | BLS | Public domain | Variables, UCCs |
| 14 | `ucc_energy_broadband.json` | JSON | ~10 | Task author | — | UCC list |
| 15 | `affordability_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 16 | `analyst_household_quintiles.xlsx` | XLSX | 5 | Task author | — | Naive quintiles |
| 17 | `oecd_equivalence_note.pdf` | PDF | — | OECD (cite) | Cite | Scale |
| 18 | `ce_published_quintile_tables.xlsx` | XLSX | — | BLS | Public domain | Validation |

## 5. Deterministic solution path

1. Stack quarters; attach members; compute equivalence scales.
2. Sum and annualise relevant UCC spending; shares.
3. Weighted quintiles on equivalised income (person-weighted per memo); median shares.
4. Designate burdened quintile and threshold; contrast with household quintiles.

## 6. Wrong paths (method errors, not misreadings)

**A — household income quintiles.** Large households misplaced.

**B — per-capita income.** Overcorrects.

**C — unweighted or household-weighted quintiles when the memo says persons.** Different boundaries.

**D — mean shares.** Skewed by near-zero incomes.

## 7. Why the stump is analytical, not semantic

Scales, weights and rules are specified. The trap is the unit of comparison in distributional analysis.

## 8. Draft task prompt (prose)

> Which income group should our energy-and-broadband discount target? Rebuild the quintiles on equivalised income as the affordability memo
> specifies and find the burdened group. Provide `burden_quintiles.csv` (quintile: boundaries, median share, by household and equivalised
> basis), `burden_by_quintile.png`, and a one-page `discount_eligibility.pdf`.

## 9. Deliverables

* `burden_quintiles.csv`, `burden_by_quintile.png`, `discount_eligibility.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 boundaries × 2 bases + 5 median shares × 2 bases = 18; designated quintile; threshold; validation; household-size composition by quintile.

## 11. Golden-output checklist

* Pooling weights; UCC list; annualisation; equivalence scale; quintile weighting; burden rule.

## 12. Build notes (scope tuning)

* Confirm the burdened quintile differs between household and equivalised bases.
