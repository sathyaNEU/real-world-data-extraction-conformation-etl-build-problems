# ET08 — Aid-flow ranking from IATI: value-dates, inherited currencies and dollars counted twice

| Field | Value |
|---|---|
| Domain | International development / philanthropy data platform |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (top 3 recipient countries get coordination offices) |
| Core technique | Attribute inheritance (transaction → activity defaults), FX conversion at the standard's value-date, percentage-split geographic attribution, de-duplication of pass-through flows between publishers |
| Trap family (honest data) | Converting at transaction-date or annual average; counting donor→NGO→country flows twice; assigning multi-country activities wholly to the first country |
| Primary sources | IATI Datastore (activity/transaction data), IATI codelists, ECB euro reference rates, U.S. Treasury Reporting Rates of Exchange |

## 1. The real-world project

A consortium of donors and the NGOs they fund publish to the International Aid Transparency Initiative (IATI). The
consortium secretariat builds a dashboard that converts every 2023 disbursement and expenditure to USD and ranks
recipient countries. The board will open **three country coordination offices** in the top three countries.

The first build used each transaction's date and an annual-average FX rate, attributed each activity to its first listed
recipient country, and summed every publisher's spending. Two NGOs and their donors were all in scope.

## 2. The business decision (one deterministic recommendation)

**Which three recipient countries receive coordination offices (top three by 2023 consortium spending in USD), and
which country is fourth?**

Rules (secretariat data standard):

* Transactions: types 3 (Disbursement) and 4 (Expenditure) with `transaction-date` in calendar 2023.
* Currency: `value/@currency` if present, else the activity's `@default-currency`.
* FX: convert at the rate for `value/@value-date` (the IATI standard defines value-date as the date to be used for
  currency conversion). ECB euro reference rate for that date (most recent prior TARGET business day if no fixing),
  cross-rated to USD; for currencies the ECB does not publish, the U.S. Treasury Reporting Rate for the quarter
  containing the value-date.
* Pass-through de-duplication: a transaction whose `receiver-org/@ref` is another in-scope publisher is excluded (that
  money is counted when the receiving publisher disburses or spends it).
* Geography: transaction-level `recipient-country` if present; otherwise split by activity-level `recipient-country`
  percentages; the share allocated to `recipient-region` is not attributed to any country.
* Eligibility: country must be on the OECD DAC list of ODA recipients for 2023.

## 3. Why this gets overlooked in real projects

* Most pipelines treat XML attributes as optional decorations; missing `@currency` becomes null instead of inheriting
  from the activity.
* FX "at transaction date" is the default instinct; the standard's explicit value-date attribute is rarely read.
* Pass-through funding is the normal structure of aid; each publisher's data is individually correct, so double
  counting only appears when several publishers are combined.
* Percentage splits across countries and regions are tedious; "first country" or "equal split" shortcuts look harmless on
  small activities.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `iati_transactions_consortium_2023.csv` | CSV | 50k–300k | IATI Datastore (transaction core) | Publisher licences (commonly CC BY 4.0 / ODbL / PDDL — record per publisher) | Transactions |
| 2 | `iati_activities_consortium.xml` | XML | ~10k activities | IATI Datastore / publisher XML | Same | Default currency, country/region percentages |
| 3 | `iati_activities_consortium.json` | JSON | ~10k | IATI Datastore | Same | Same, for cross-check |
| 4 | `publishers_in_scope.csv` | CSV | ~15 | IATI Registry | CC BY 4.0 (registry metadata; verify) | Org refs of in-scope publishers |
| 5 | `codelist_TransactionType.json`, `codelist_Currency.json`, `codelist_Country.json`, `codelist_Region.json` | JSON | small | IATI codelists | IATI codelist licence (open; verify) | Code meanings |
| 6 | `eurofxref-hist.csv` | CSV | ~6.5k days | European Central Bank | ECB statistics reuse with attribution | Daily EUR reference rates |
| 7 | `treasury_reporting_rates_2022_2024.csv` | CSV | ~1.5k | U.S. Treasury Fiscal Data | Public domain | Fallback FX |
| 8 | `target_holidays_2023.csv` | CSV | ~6 | ECB | Attribution | No-fixing days |
| 9 | `dac_list_oda_recipients_2022_2023.xlsx` | XLSX | ~140 | OECD | OECD terms (free reuse with attribution) | Eligibility |
| 10 | `iati_standard_2.03_transaction_reference.pdf` | PDF | — | IATI | CC BY 4.0 | value-date definition |
| 11 | `secretariat_data_standard.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Parse activities; build lookups for default currency, recipient-country and recipient-region percentages.
2. Filter transactions (types 3/4, 2023); resolve currency by inheritance.
3. Remove transactions to in-scope publishers.
4. Convert at value-date (ECB with prior-business-day rule; cross-rate to USD; Treasury fallback).
5. Allocate to countries (transaction-level country, else activity percentages; region share unallocated).
6. Filter to DAC-eligible countries; rank; top three + fourth; compute gap.
7. Compute the naive variant (transaction-date FX, no de-dup, first-country) for comparison.

## 6. The traps

**Trap A — missing-currency rows.** Treated as USD (or dropped). Large EUR/GBP-denominated publishers are mis-scaled.

**Trap B — wrong FX date or average rate.** Moves countries with large year-end or early-year flows in volatile
currencies; the third/fourth places swap.

**Trap C — pass-through double counting.** Countries served through consortium NGOs are counted twice and leap into the
top three.

**Trap D — first-country attribution.** Regional and multi-country programmes inflate one country.

**Trap E — ECB quote direction.** ECB quotes units of currency per 1 EUR; dividing the wrong way inverts amounts.

## 7. Why the data is honest

Each publisher's IATI file is a faithful report of its own transactions; the value-date attribute and inheritance rules
are in the published standard. The combination problem is structural, not planted.

## 8. Draft task prompt (prose)

> The board will open three country coordination offices in the countries where the consortium spent the most in 2023.
> Using the IATI data, exchange-rate files and our data standard in the folder, convert every in-scope disbursement and
> expenditure to dollars, attribute it to countries, make sure no dollar is counted twice as it moves between our
> members, and tell me the three countries and the one just behind them. Produce `country_ranking_2023.csv` with every
> eligible country's USD total, the split between donor-direct and NGO-delivered spending, and its rank. Create
> `country_ranking.png`, a ranked bar chart of the top ten with the cut after three and the fourth-place gap annotated.
> Finally a one-page `office_decision.pdf` with the decision, the gap between third and fourth, and what the top three
> would have been without removing pass-through flows.

## 9. Deliverables

* `country_ranking_2023.csv`, `country_ranking.png`, `office_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* Top-10 country totals and ranks; top-3 + 4th + gap; donor-direct vs NGO split for top 3; count/amount of removed
  pass-through flows; naive-variant top 3; USD value for 3–4 spot-check transactions (currency inheritance, value-date FX).

## 11. Golden-output checklist

* Currency inheritance, value-date FX with prior-business-day rule, pass-through removal, percentage allocation, DAC
  filter; decision and gap stated.

## 12. Build notes (scope tuning)

* Choose a consortium (real IATI publishers that fund each other — check `receiver-org/@ref` against publisher refs)
  where de-duplication changes the top three.
* Ensure some publishers omit transaction-level currency and some use value-dates different from transaction dates.
