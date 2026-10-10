# ET44 — Loyalty-tier thresholds from a wholesale order log: cancellations, overlapping extracts and the tempting de-dup

| Field | Value |
|---|---|
| Domain | Retail / B2B e-commerce / CRM and loyalty programs |
| Objective family | Descriptive & Distribution Analysis |
| Task shape | 14 · Cuts of a distribution (nested tier boundaries by segment) |
| Core technique | Transaction-ledger conformance (sales, cancellations, adjustments, non-product lines); de-duplicating overlapping extracts without removing legitimate repeated lines; weighted percentile cuts with rounding rules |
| Trap family (honest data) | Overlapping sheet periods double counted; legitimate identical lines removed by blanket de-dup; cancellations dropped or matched to original dates; postage/fees counted as spend |
| Primary sources | UCI Machine Learning Repository — Online Retail II (UK online wholesaler, 2009–2011) |

## 1. The real-world project

A UK online gift wholesaler launches a three-tier loyalty program for its trade customers. Tier thresholds are set from
the distribution of 12-month **net product spend**: Platinum = top 2% of customers, Gold = next 8%, Silver = next 20%,
computed separately for UK and non-UK customers. The CRM analyst combined the two Excel sheets of the order export,
dropped duplicate rows "to be safe", ignored cancellations ("they're returns, not spend") and set thresholds. Customer
service immediately got calls from customers placed in tiers above their net purchases.

## 2. The business decision (one deterministic recommendation)

**What are the six tier thresholds (Platinum/Gold/Silver × UK/non-UK) in £, and how many customers fall in each tier?**

Rules (program method):

* Window: invoices dated 2010-12-01 00:00 to 2011-11-30 23:59.
* Source rows: the "Year 2010-2011" sheet for all dates ≥ 2010-12-01; the "Year 2009-2010" sheet only for earlier dates (the two
  sheets overlap in early December 2010).
* Identical lines within an invoice are **legitimate separate order lines** and are kept.
* Customer required (`Customer ID` not null).
* Net product spend = Σ Quantity × Price over product lines, where invoices beginning with `C` (cancellations, negative
  quantities) are included **on their own dates**; invoices beginning with `A` (bad-debt adjustments) excluded; non-product
  stock codes excluded (POST, DOT, C2, M, m, D, S, B, BANK CHARGES, AMAZONFEE, CRUK, PADS, ADJUST, TEST*, gift_* — list in
  the method).
* Customers with net spend ≤ 0 are excluded from the distribution.
* Segment = UK if the customer's most frequent invoice `Country` in the window is United Kingdom.
* Thresholds per segment: the minimum net spend among the top ⌈2%⌉, top ⌈10%⌉, top ⌈30%⌉ customers (by count, ranked by
  spend, ties by lower Customer ID first), each **rounded down to the nearest £50**; tiers are nested.

## 3. Why this gets overlooked in real projects

* Exports split by fiscal year often overlap; concatenating them silently duplicates days.
* `drop_duplicates()` feels like hygiene, but in this log identical lines (same item, quantity and minute within an invoice)
  are real separate scans/lines; removing them understates spend.
* Cancellations live as separate invoices with negative quantities; analysts drop them or try to net them against "the
  original order", which may be outside the window.
* Postage, fees and manual adjustments are coded as stock codes and look like products.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `online_retail_II.xlsx` (sheets "Year 2009-2010", "Year 2010-2011") | XLSX | ~1.07M lines | UCI ML Repository (id 502) | CC BY 4.0 | Order log |
| 2 | `online_retail_II_2010_2011.csv` (sheet export) | CSV | ~0.54M | Derived from #1 | CC BY 4.0 | Same, CSV |
| 3 | `uci_online_retail_II_description.html` | HTML | — | UCI | CC BY 4.0 | Variable notes (C/A prefixes) |
| 4 | `non_product_stockcodes.json` | JSON | ~15 | Task author (from the data) | — | Exclusion list |
| 5 | `program_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `uk_bank_holidays.json` | JSON | ~100 | GOV.UK bank holidays API | OGL v3.0 | Context (calendar checks) |
| 7 | `boe_gbp_eur_usd_2010_2011.csv` | CSV | ~500 | Bank of England database | BoE terms (free with attribution) | Optional context |
| 8 | `iso3166_countries.csv` | CSV | ~250 | Public reference | Public domain | Country normalization |
| 9 | `customer_tier_template.xlsx` | XLSX | — | Task author | — | Output layout |
| 10 | `dataset_paper_chen_2012.pdf` (citation reference) | PDF | — | Chen, Sain & Guo (2012), J. Database Marketing | Cite per UCI | Background |

## 5. Deterministic solution path

1. Load sheets; apply the sheet-date rule; keep in-window rows.
2. Drop rows without customer; exclude `A` invoices and non-product codes; keep cancellations.
3. Compute net spend per customer; drop ≤ 0; assign segment.
4. Rank within segment; compute cut counts with ceilings; thresholds rounded down to £50; tier counts.
5. Contrast: sheets concatenated; blanket de-dup; cancellations dropped; fees included.

## 6. The traps

**Trap A — overlap.** Early-December 2010 lines double; heavy December buyers move up a tier.

**Trap B — blanket de-dup.** Removes legitimate lines; thresholds fall.

**Trap C — cancellations dropped.** Gross not net spend; thresholds rise; customers with big returns over-tiered.

**Trap D — non-product codes.** Postage and fees inflate small customers' spend, especially non-UK.

## 7. Why the data is honest

The UCI dataset is the retailer's actual transaction log; prefixes and codes are documented in its description. The program
method decides how to treat each line type — including keeping legitimate identical lines.

## 8. Draft task prompt (prose)

> Set the loyalty tier thresholds for UK and non-UK trade customers from twelve months of net product spend, following
> the program method in the folder. Using the order log, tell me the six thresholds and how many customers land in each
> tier. Produce `tier_thresholds.csv` (segment, tier, threshold, customers in tier, cumulative share) and
> `spend_distribution.png`, the net-spend distribution for each segment on a log scale with the three thresholds drawn.
> Add a one-page `tier_memo.pdf` with the thresholds, the count of customers whose tier would change if duplicate lines had
> been removed, and the segment most affected by including cancellations.

## 9. Deliverables

* `tier_thresholds.csv`, `spend_distribution.png`, `tier_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 thresholds, 6 tier counts, 2 segment sizes, net spend for 5 spot-check customers, de-dup and cancellation sensitivities.

## 11. Golden-output checklist

* Sheet-date rule; keep identical lines; cancellations on own dates; exclusions; ceiling counts; £50 rounding down.

## 12. Build notes (scope tuning)

* Verify the sheet overlap dates in the downloaded file and that Trap B changes at least two thresholds.
* Cite the dataset as UCI requires (CC BY 4.0).
