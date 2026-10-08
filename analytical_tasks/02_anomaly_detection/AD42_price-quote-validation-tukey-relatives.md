# AD42 — Price-data validation: judge each quote against its own last price, not against other shops

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Price-intelligence and catalogue-quality teams at e-commerce companies catching pricing errors; statistical offices validating CPI price collection |
| Domain | Price statistics / retail |
| Task shape | 10 · Scorecard against thresholds (items × validation rules → flag rates; adopt the relative-change validation for the monthly run) |
| Core method | Price relatives (this month ÷ last month, same shop and product); log relatives; Tukey-style fences per item from the item's own distribution of relatives (quartiles with the memo's k); comparison with level-based rules (price outside item median ± 3 MAD across shops) |
| Analytical stump | Prices of the "same" item differ widely across shops and pack sizes, so level-based rules flag premium and discount shops every month while missing a shop whose price jumped tenfold within its normal range. Errors and genuine changes reveal themselves in the *relative* to the shop's previous quote |
| Primary sources | Office for National Statistics consumer price inflation item indices and price quotes (local collection microdata) |

## 1. The real-world situation

A statistics team validates around 100,000 local price quotes a month before compiling the index. Its legacy rule flags quotes more than
three median absolute deviations from the item's cross-shop median price; validators review thousands of flags, most of them legitimate
premium shops, and a misplaced-decimal entry slipped through last year.

## 2. The decision (one deterministic recommendation)

**Adopt relative-change validation for the monthly run or keep the level rule, judged on the memo's scorecard over 24 months of quotes.**

Rules (validation memo):

* Quotes: ONS price quotes for 24 consecutive months; match a quote to the previous month by shop code, item ID and region; unmatched quotes are
  excluded from relative checks (counted separately).
* Relative rule R: log relative r = ln(p_t ÷ p_{t−1}); per item and month, fences Q1 − 3·IQR and Q3 + 3·IQR of r; flag outside fences.
* Level rule L: flag p_t outside item-month median ± 3 × 1.4826 × MAD of prices across shops.
* Reference errors: quotes later revised or marked invalid (validity indicator in the files), plus the 40 decimal-shift cases in
  `known_entry_errors.csv`.
* Scorecard per rule: flag rate (target ≤ 2%), recall of reference errors (target ≥ 80%), share of flags in items with strong seasonal patterns
  (≤ 20%).
* Adopt R if it meets all three targets and L does not.

## 3. Why capable analysts get it wrong

* Cross-sectional outlier rules are the default for "unusual prices".
* Shop-level heterogeneity is large and persistent; relatives difference it out.
* Entry errors are discontinuities in a shop's own history.
* Fences must be item-specific; volatile items (fresh produce, fares) need their own spread.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–24 | `upload-pricequotes<yyyymm>.csv` (24 months) | CSV | ~100–130k each | ONS price quotes | Open Government Licence v3 | Quotes with shop code, item, region, price, validity indicators |
| 25 | `itemindices<yyyymm>.csv` (24 months) | CSV | ~700 each | ONS | OGL v3 | Item indices (context) |
| 26 | `price_quotes_glossary.xlsx` | XLSX | — | ONS | OGL | Field definitions, indicator codes |
| 27 | `known_entry_errors.csv` | CSV | 40 | Task author (identified decimal shifts, frozen list) | — | Reference errors |
| 28 | `seasonal_items.json` | JSON | ~60 | Task author (from ONS seasonal item lists) | — | Seasonal items |
| 29 | `validation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 30 | `legacy_level_rule_flags.parquet` | Parquet | ~50k | Task author | — | Legacy flags |
| 31 | `ons_cpi_technical_manual_excerpt_citation.pdf` | PDF | — | ONS (cite) | OGL | Validation context |

## 5. Deterministic solution path

1. Stack months; match quotes to previous month; compute relatives.
2. Apply R and L per item-month.
3. Build reference-error set; compute scorecard metrics per rule.
4. Decide; list examples of errors caught only by R.

## 6. Wrong paths (method errors, not misreadings)

**A — level rule.** Flags premium shops; misses within-range jumps.

**B — global fences across items.** Volatile items dominate flags.

**C — matching on item only (not shop).** Relatives meaningless.

**D — symmetric percent changes instead of log relatives.** Asymmetric fences.

## 7. Why the stump is analytical, not semantic

Matching, fences and scorecard are specified. The trap is choosing level versus within-unit change as the comparison.

## 8. Draft task prompt (prose)

> Should our monthly price validation switch to the relative-change rule in the validation memo? Evaluate both rules over 24 months of ONS
> quotes. Provide `validation_scorecard.csv` (rule × metric with targets), `relatives_vs_levels.png` (an example item: price levels by shop
> and log relatives with fences), and a one-page `validation_decision.pdf`.

## 9. Deliverables

* `validation_scorecard.csv`, `relatives_vs_levels.png`, `validation_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 2 rules × 3 metrics vs targets = 6; per-month flag rates for both rules (sampled 12); unmatched counts; decision; examples.

## 11. Golden-output checklist

* Matching keys; log relatives; item-month fences; level rule; reference set; scorecard; decision.

## 12. Build notes (scope tuning)

* Verify validity indicators in the chosen months; freeze the reference error list.
* Confirm L's flag rate exceeds 2% and its recall of decimal shifts is low.
