# OS40 — Refinance opportunity: the average outstanding rate hides the loans that would benefit

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Upgrade or migration opportunities sized from a distribution (customers on legacy expensive plans, devices past a threshold), where the average suggests no opportunity |
| Domain | Mortgage lending |
| Task shape | 14 · Cuts of a distribution (share and count of outstanding mortgages with rates ≥ market + 75 bp by origination cohort; the marketing budget allocated to refinance campaigns) |
| Core method | Distribution of outstanding mortgage interest rates from bucketed aggregates (share of loans in rate buckets by quarter); interpolate within buckets to the threshold (market rate + 0.75); multiply by outstanding loan counts; apply the memo's minimum balance and seasoning filters via provided shares |
| Analytical stump | When the average outstanding rate is below the current market rate, the deck concludes there is no refinance market. A minority of loans — recent originations at peak rates — sit well above market. The opportunity is a tail share of the distribution, not a comparison of averages |
| Primary sources | FHFA National Mortgage Database (NMDB) aggregate statistics — outstanding mortgage rate distribution and counts |

## 1. The real-world situation

A lender's strategy team concluded that there is no meaningful refinance market because the average rate on outstanding mortgages is well
below the current market rate. Marketing pointed out that loans originated during the rate peak carry rates above today's market.

## 2. The decision (one deterministic recommendation)

**The number of outstanding loans with rates ≥ current market + 0.75 percentage points (refinance-eligible), and the refinance campaign budget
(memo: $40 per eligible loan in the lender's market share).**

Rules (strategy memo):

* Data: NMDB aggregate series for the latest quarter: share of outstanding mortgages by interest-rate bucket (e.g., < 3%, 3–4%, 4–5%, 5–6%,
  ≥ 6% per published buckets) and number of outstanding mortgages.
* Market rate: the memo's 30-year fixed average for the quarter.
* Threshold T = market + 0.75.
* Share above T: sum of buckets entirely above T plus the linear share of the bucket containing T (uniform within bucket; the open top bucket
  entirely above if its lower bound ≥ T).
* Eligible loans = share × outstanding count × the memo's filters (balance ≥ $100k share, seasoning ≥ 6 months share).
* Lender's market share 4%; budget = eligible × 4% × $40.
* Report the average-rate comparison for contrast.

## 3. Why capable analysts get it wrong

* Average rates are widely reported and easy to compare.
* Refinance incentive is loan-specific; a tail of the distribution qualifies.
* Bucketed data require interpolation at the threshold.
* Filters for balance and seasoning reduce eligibility.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `nmdb_outstanding_residential_mortgage_statistics.csv` | CSV | ~quarterly series × measures | FHFA NMDB aggregate statistics | U.S. Gov public domain | Rate-bucket shares, counts |
| 2 | `nmdb_data_dictionary.pdf` | PDF | — | FHFA | Public domain | Definitions |
| 3 | `pmms_30yr_weekly.csv` | CSV | ~2.8k | Freddie Mac PMMS (public historical series) | Public (cite) | Market rate |
| 4 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `strategy_average_rate_slide.xlsx` | XLSX | — | Task author | — | Naive conclusion |
| 6 | `filter_shares.json` | JSON | — | Task author | — | Balance and seasoning shares |

## 5. Deterministic solution path

1. Extract latest-quarter bucket shares and counts; market rate; T.
2. Interpolate share above T; apply filters; eligible loans.
3. Budget; contrast with the average-rate conclusion.

## 6. Wrong paths (method errors, not misreadings)

**A — average comparison.** Concludes zero opportunity.

**B — counting the whole bucket containing T.** Overstated.

**C — ignoring filters.** Overstated.

**D — origination rates instead of outstanding.** Different population.

## 7. Why the stump is analytical, not semantic

Data, threshold and interpolation are specified. The trap is comparing averages when the decision depends on a tail.

## 8. Draft task prompt (prose)

> Is there a refinance market worth a campaign? Size eligible outstanding loans from the NMDB rate distribution as the strategy memo specifies.
> Provide `rate_distribution_cut.csv` (bucket: share, share above T), `rate_distribution.png`, and a one-page `refinance_campaign.pdf`.

## 9. Deliverables

* `rate_distribution_cut.csv`, `rate_distribution.png`, `refinance_campaign.pdf`.

## 10. Where 25+ rubric criteria come from

* Bucket shares (6); T; interpolation; eligible count; filters; budget; average contrast; trend of share above T over 8 quarters.

## 11. Golden-output checklist

* Latest quarter; T; interpolation; filters; market share; budget.

## 12. Build notes (scope tuning)

* Confirm the average outstanding rate is below market while eligible share is ≥ 5%.
