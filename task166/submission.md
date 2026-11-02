# task166: Marrowgate Books, the returns allowance at the 31 October 2026 year end

## Tags

**Domain:** Actuarial Science & Insurance, reserving and development triangles (a trade publisher's year-end allowance for sale-or-return book returns).  
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**We should hold a returns allowance of £1.75 million at 31 October 2026, of which £1.0 million is for hardbacks.**

Most of the autumn 2026 hardbacks have their own paperback due within 8 months of publication, so the stock shops hold comes back once each paperback is out, as it did for the earlier hardbacks with a paperback that close. Not the development of returns by format, channel and weeks since invoice on the history's pattern, which back-tests well at the 2024 and 2025 year ends but develops those hardbacks on hardbacks whose paperbacks came about a year later. Not a trailing twelve months' return rate, which carries the same history.

## 2. Critical Components

1. The returns allowance at 31 October 2026 is **£1,750,000** (to the nearest £250,000).
2. The hardback part of it is **£1,000,000** (to the nearest £250,000).
3. Hardbacks whose own paperback, matched on the title master by title and contributor, is published within **8 months** of them are developed on the earlier hardbacks with a paperback that close, not on the general hardback pattern.

## 3. Step-by-Step Solution

1. Read the sale-or-return accounts' invoice lines and returns credits (reason RET) from `marrowgate_sales_ledger_FY2022-FY2026.sqlite`, legacy account numbers mapped through `trade_accounts_2026-10-30.csv`, ISBN hyphens stripped and transit claims left out per `marrowgate_accounting_policies_FY2026.pdf`.
2. Matched each hardback on `title_master_2026-10-30.xlsx` to its own paperback, the later Paperback edition with the same contributor (surname-first names turned round) and the same title before any colon (lower case, & read as and, punctuation and a leading article dropped): most hardbacks published from August to October 2026 have a paperback within 8 months, few earlier ones do.
3. Built returned copies as a share of copies invoiced, by weeks from invoice to the credit quoting it, by format and channel, on invoices from 1 November 2021 at least 425 days old at 31 October 2026, with hardbacks whose paperback comes within 8 months as their own segment.
4. Took each sale-or-return invoice line of the twelve months to 31 October 2026 times its segment's share still to come after its age, at its own net price (the terms of trade let a return quote only an invoice three to twelve months old): £1,750,000, of which hardbacks £1,000,000.
5. Struck the same construction at 31 October 2024 and 31 October 2025 and compared it with the returns credited afterwards on the copies then open: 0.6% below and 0.2% above.
6. Copies received: from `tallowmere_returns_received_FY2025-FY2026.csv` dropped the re-sent export's exact duplicate rows and ISBNs not on the title master, then every delivery reference whose lines repeat an earlier one line for line (authorisation, ISBN, copies and grades) and take each of those lines past its authorised copies in `tallowmere_returns_authorisations_FY2025-FY2026.csv` by at least the copies repeated, keeping copies sent beyond an authorisation (held for collection per the terms); summed copies received from 1 November 2025 to 31 October 2026 by the channel of the authorisation's account and quarter: 504,983 copies in all.
7. Written off: resolved each tote in `tallowmere_hurts_reinspection_FY2026.xlsx` re-inspected by 31 October 2026 against the hurts the kept deliveries put into it (rows adding up to those hurts are sessions and add; rows each equal to them are recounts and the latest stands), shared each tote's pulped copies among its deliveries in proportion to their hurts, added the copies graded unsaleable and divided by the copies received: 6.6% overall.
8. Recommendation: hold £1,750,000 at 31 October 2026, £1,000,000 of it for hardbacks.

## 4. Deliverable Answers

### returns_allowance_FY2026.xlsx

1. Returns allowance at 31 October 2026, to the nearest £250,000: £1,750,000.
2. Of which hardbacks, to the nearest £250,000: £1,000,000.
3. Copies of Marrowgate titles received back by Tallowmere in the year to 31 October 2026, by channel and quarter of the financial year (Q1 November to January, Q2 February to April, Q3 May to July, Q4 August to October), whole copies:
   - Chain: Q1 46,357; Q2 124,658; Q3 63,697; Q4 68,018
   - Online: Q1 7,506; Q2 22,416; Q3 6,114; Q4 4,776
   - Wholesale: Q1 35,111; Q2 29,378; Q3 20,804; Q4 25,643
   - Supermarket: Q1 2,306; Q2 5,494; Q3 4,368; Q4 7,121
   - Independent: Q1 4,049; Q2 4,217; Q3 2,866; Q4 2,971
   - Export: Q1 3,195; Q2 7,521; Q3 2,657; Q4 3,740
4. Share of those copies written off by 31 October 2026 (graded unsaleable on receipt, or hurt and pulped at re-inspection), by channel, one decimal:
   - Chain: 5.7%
   - Online: 10.2%
   - Wholesale: 6.8%
   - Supermarket: 12.0%
   - Independent: 4.6%
   - Export: 8.8%
5. The same share by format, one decimal:
   - Hardback: 6.5%
   - Trade paperback: 7.2%
   - Paperback: 6.6%

### returns_allowance_note.pdf

1. One page stating the allowance of £1,750,000, its hardback part of £1,000,000 and how it was built: the development of returns by format, channel and weeks since invoice, with the hardbacks whose paperback is published within 8 months developed on the earlier hardbacks with a paperback that close.
