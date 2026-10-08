# OS21 — Time-of-use tariff savings: the average home's profile is nobody's profile, and switchers are not random

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Plan-migration sizing (moving customers to usage-based or tiered pricing) where savings depend on each customer's usage shape and only customers who benefit opt in |
| Domain | Energy retail |
| Task shape | 07 · Grid of cells (4 household groups × 2 tariffs → mean bill change per home; the expected annual saving of customers who would switch) |
| Core method | Compute each home's annual bill under flat and time-of-use tariffs from its own half-hourly profile; savings distribution by group; expected uptake = homes with savings > switching threshold (memo); total savings among switchers; contrast with bills computed on the average profile |
| Analytical stump | Applying the tariff to the group's average load profile gives the bill change of an average shape, but savings are nonlinear in shape (peak share); the average of per-home savings differs from savings of the average home. Opt-in tariffs attract homes that gain, so savings among switchers exceed the group mean |
| Primary sources | IDEAL Household Energy Dataset (University of Edinburgh; electricity readings for ~255 homes) |

## 1. The real-world situation

An energy supplier sizes the customer savings from offering a time-of-use (ToU) tariff. The analyst applied the tariff to the average
half-hourly profile of each household group and found savings near zero, concluding the product had little appeal. A pricing manager argued
that customers with flexible or low-peak usage would switch and save considerably.

## 2. The decision (one deterministic recommendation)

**The expected uptake share and annual savings per switching customer by group, and whether total customer savings among switchers exceed the
memo's launch threshold (£40 average per switcher with ≥ 15% uptake).**

Rules (pricing memo):

* Data: IDEAL electricity mains readings (1-second/aggregated per memo to 30-minute), homes with ≥ 300 days of valid data in the analysis year.
* Groups: household composition × heating type from the IDEAL metadata (4 groups per memo).
* Tariffs: flat p/kWh; ToU with peak 16:00–19:00 at a higher rate and off-peak lower (rates in memo); standing charges equal.
* Annual bill per home under each tariff from its own profile (gap-filled per memo).
* Savings = flat − ToU; switch if savings ≥ £25 per year.
* Uptake share = switchers ÷ homes; average savings per switcher.
* Launch if average per switcher ≥ £40 and uptake ≥ 15% overall.
* Contrast: savings computed on group-average profiles.

## 3. Why capable analysts get it wrong

* Average profiles are convenient and smooth.
* Bills are linear in each home's consumption but savings depend on peak shares that vary widely.
* Opt-in selection makes switchers different from the average.
* Gap-filling rules affect annualised bills.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `household_sensors/<home>_electric-mains*.csv.gz` | CSV | ~255 homes × millions of readings | IDEAL dataset (Edinburgh DataShare) | CC BY 4.0 | Electricity readings |
| 2 | `metadata/home.csv`, `metadata/person.csv`, `metadata/appliance.csv` | CSV | ~255 / ~600 / ~5k | IDEAL | CC BY 4.0 | Household attributes |
| 3 | `ideal_documentation.pdf` | PDF | — | Pullinger et al., Scientific Data 2021 (cite) | CC BY 4.0 | Dataset description |
| 4 | `tariffs.json` | JSON | 2 | Task author | — | Tariff definitions |
| 5 | `pricing_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `analyst_average_profile_result.xlsx` | XLSX | 4 | Task author | — | Naive sizing |
| 7 | `half_hourly_profiles.parquet` | Parquet | ~4M | Derived | CC BY 4.0 | Aggregated readings |
| 8 | `gap_fill_rules.json` | JSON | — | Task author | — | Imputation |

## 5. Deterministic solution path

1. Aggregate readings to 30 minutes; validity filter; gap-fill.
2. Per-home bills under both tariffs; savings; groups.
3. Uptake and savings per switcher; launch decision.
4. Average-profile contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — group-average profile.** Hides heterogeneity.

**B — mean savings over all homes as the per-switcher figure.** Ignores self-selection.

**C — no gap filling.** Bills understated for homes with missing data.

**D — peak window in UTC instead of local time.** BST months misassigned.

## 7. Why the stump is analytical, not semantic

Tariffs and the switching rule are specified. The trap is nonlinearity and selection in plan-migration sizing.

## 8. Draft task prompt (prose)

> Should we launch the time-of-use tariff? Compute per-home bills from IDEAL profiles, find who would switch and what they save, as the pricing
> memo specifies. Provide `tou_savings_grid.csv` (group: homes, mean savings, uptake, savings per switcher, average-profile savings),
> `savings_distribution.png`, and a one-page `tou_launch.pdf`.

## 9. Deliverables

* `tou_savings_grid.csv`, `savings_distribution.png`, `tou_launch.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 groups × 5 values = 20; overall uptake and savings; decision; average-profile contrast; validity counts.

## 11. Golden-output checklist

* Aggregation; local time; gap fill; per-home bills; switching rule; decision.

## 12. Build notes (scope tuning)

* Confirm the average-profile method shows < £10 savings while switchers average ≥ £40.
