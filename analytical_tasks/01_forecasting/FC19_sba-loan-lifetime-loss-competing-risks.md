# FC19 — Lifetime loss on small-business loans: borrowers who prepay can never default

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Lenders' lifetime expected-credit-loss (CECL) reserves for term-loan books (banks and fintech lenders) |
| Domain | Credit risk / loan-loss reserving |
| Task shape | 03 · Bridge between two totals (charge-offs to date → expected lifetime charge-offs, by vintage) |
| Core method | Competing-risks survival: Aalen–Johansen cumulative incidence of charge-off with paid-in-full as a competing event, estimated on mature vintages by loan age; conditional incidence applied to surviving loans of recent vintages |
| Analytical stump | Treating payoffs as censoring (1 − Kaplan–Meier) assumes prepaid loans would have kept their default risk — it overstates lifetime default. Reading charge-offs to date on young vintages understates it. Only cumulative incidence conditional on survival to the current age is consistent |
| Primary sources | U.S. SBA 7(a) loan-level FOIA data |

## 1. The real-world situation

A lender with a large SBA 7(a) book must set its lifetime loss reserve for loans approved in fiscal years 2019–2021. One analyst
used charge-offs to date ÷ originations (tiny, because the loans are young). Another estimated the default curve with
Kaplan–Meier, treating loans paid in full as censored, and got a reserve three times larger. The CFO asked which is right.

## 2. The decision (one deterministic recommendation)

**Expected remaining lifetime charge-off amount for active FY2019–FY2021 loans as of the data's as-of date (and the total
reserve).**

Rules (reserving memo):

* Estimation sample: 7(a) loans approved FY2010–FY2016 with a first disbursement date; events by months since first
  disbursement: charge-off (`LoanStatus = CHGOFF`, `ChargeOffDate`) and paid in full (`PIF`, `PaidInFullDate`); loans active at the
  as-of date are censored. Cancelled/never-disbursed loans excluded.
* Estimate, by loan-term class (≤ 120 months, > 120 months), the cumulative incidence of charge-off CIF(t) and overall event-free
  survival S(t) with the Aalen–Johansen estimator (monthly grid).
* For each active FY2019–FY2021 loan at age a: P(charge-off later) = [CIF(T) − CIF(a)] ÷ S(a), with T = loan term (capped at the
  last estimable month).
* Expected charge-off amount = P × severity × `GrossApproval`, where severity = Σ `GrossChargeOffAmount` ÷ Σ `GrossApproval` over
  charged-off loans in the estimation sample, by term class.
* Reserve = Σ over active loans; also report the bridge per vintage: charge-offs to date → expected remaining → lifetime.

## 3. Why capable analysts get it wrong

* Kaplan–Meier is the default survival tool; with competing events it estimates a counterfactual world where nobody prepays.
* Cumulative charge-off ratios on young vintages are "development" problems — the losses have not happened yet.
* Conditioning on survival to the current age is easy to forget; unconditional curves double count early risk already passed.
* Long-term (real-estate-backed) loans behave differently; pooling terms mixes hazards.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `foia-7afy2010-fy2019-asof-<date>.csv` | CSV | ~0.5M | U.S. SBA FOIA data | Public domain | Estimation and part of decision vintages |
| 2 | `foia-7afy2020-present-asof-<date>.csv` | CSV | ~0.3M | U.S. SBA | Public domain | Recent vintages |
| 3 | `foia-7afy2000-fy2009-asof-<date>.csv` | CSV | ~0.6M | U.S. SBA | Public domain | Context |
| 4 | `7a_504_foia_data_dictionary.xlsx` | XLSX | — | U.S. SBA | Public domain | Field definitions |
| 5 | `sba_7a_loan_program_overview.pdf` | PDF | — | U.S. SBA | Public domain | Terms, guarantees |
| 6 | `aalen_johansen_reference.pdf` (citation) | PDF | — | Cite | Cite | Competing-risks estimator |
| 7 | `fasb_asc326_cecl_summary.pdf` | PDF | — | FASB public summary (cite) | Cite | Lifetime-loss concept |
| 8 | `reserving_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `analyst_estimates.xlsx` | XLSX | ~10 | Task author | — | To-date and KM estimates |
| 10 | `naics_2017_titles.csv` | CSV | ~2k | Census | Public domain | Context |

## 5. Deterministic solution path

1. Filter loans; compute ages and event types; censor actives at the as-of date.
2. Aalen–Johansen CIF and S by term class on FY2010–FY2016 loans.
3. For each active FY2019–FY2021 loan, conditional remaining probability; expected amount; sum by vintage.
4. Bridge per vintage; total reserve; contrast with KM-based and to-date estimates.

## 6. Wrong paths (method errors, not misreadings)

**A — 1 − KM with prepayment censored.** Lifetime default overstated; reserve too high.

**B — charge-offs to date.** Reserve far too low.

**C — unconditional CIF for seasoned loans.** Double counts early-life risk.

**D — pooled term classes.** Mix-driven bias.

## 7. Why the stump is analytical, not semantic

Statuses, dates and formulas are specified. The trap is the survival model under competing risks and conditioning on survival —
core methodological choices.

## 8. Draft task prompt (prose)

> Set the lifetime loss reserve for our FY2019–FY2021 SBA 7(a) loans following the reserving memo. Estimate charge-off and payoff
> patterns on the mature vintages, apply them to the loans still active, and give me the reserve. Provide `reserve_bridge.xlsx`
> (per vintage: originations, charge-offs to date, expected remaining, lifetime; curves by term class) and
> `cumulative_incidence.png` comparing the charge-off cumulative incidence with 1 − Kaplan–Meier for each term class. On the first
> sheet, state the reserve and explain the gap to both analysts' numbers.

## 9. Deliverables

* `reserve_bridge.xlsx`, `cumulative_incidence.png`.

## 10. Where 25+ rubric criteria come from

* CIF at 12/36/60/120 months for 2 term classes (8); severity (2); 3 vintages × bridge bars (9); reserve; KM and to-date contrasts.

## 11. Golden-output checklist

* Correct events and censoring; Aalen–Johansen; conditional probabilities; severity; vintage bridge.

## 12. Build notes (scope tuning)

* Record the FOIA files' as-of date; confirm PIF and charge-off dates are populated for the estimation sample.
* Confirm the KM-based reserve exceeds the correct one by > 25%.
