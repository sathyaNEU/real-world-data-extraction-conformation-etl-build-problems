## Tags

**Domain:** Banking, Credit & Financial Risk (stress testing and capital: interest-rate risk in the banking book).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Designate the $1.2 billion overlay against the fixed-rate commercial real estate pool.**
Its +200 bp loss in economic value averaged over the month-ends of 2027 is $150 million, ahead of agency MBS at about $110 million. Not the 2023-24 mortgages, which lose most at last year's prepayment speed but are expected to prepay about 30 per cent a year at the planning cycle's 6.25 per cent. Not agency MBS, which leads only while the commercial real estate balloons due through 2027 are taken to repay when due or to extend at the share recent maturities showed.

## 2. Critical Components

1. About **$4.7 billion** of the pool's balloons fall due from December 2026 to December 2027, nearly all of them from the push of December 2021 to April 2022.
2. About **three-fifths** of that principal is expected to extend for **36** months at its note rate: at the planning cycle's 6.95 per cent the push's cash-out loans, sized at full leverage on pro forma rents, cannot carry a new loan of their balloon, while its lower-leverage refinances can.
3. Agency MBS, the runner-up, loses about **$110 million**.

## 3. Step-by-Step Solution

1. Per the hedging policy (section 3), each Schedule A pool's loss is the present value of its base-case expected cash flows from the positions at 30 November 2026, on the planning workbook's zero curve less the same 200 bp higher, averaged over the month-ends of the overlay's first twelve months, January to December 2027 as it starts on 4 January; every pool holds more than $1.2 billion.
2. The Treasury ladder as contracted, each 2020-21 agency pool at its own prepayment rate over its last twelve factor months (agency_pool_factors.csv, cash a month after each factor month) and indirect auto at the roll's prepayment rate over its last twelve months lose about $70 million, $110 million and $30 million.
3. For the 2023-24 mortgages, the two servicing extracts joined through servicing_conversion_xref.csv fit turnover by calendar month and loan age plus an S-curve in the note rate's excess over the posted jumbo rate a month earlier (rate_sheet_archive.csv); at 6.25 per cent the pool prepays about 30 per cent in 2027 and loses about $90 million.
4. Each maturity since 2015 in cre_maturity_log.xlsx, joined to the last operating statement reviewed before it, gives refinance cover: net operating income over a new loan of the balloon at that month's posted five-year rate on the sheet's 25-year amortization.
5. A logistic in cover fitted to the maturities to 2024 scores a Brier of 0.006 on those of 2025 and 2026, against 0.065 for the note-rate debt service cover, 0.068 for the debt yield, 0.104 for the last year's share, 0.111 for the rate gap and 0.112 for the pooled share.
6. Fitted on every maturity and applied at 6.95 per cent to each fixed-rate loan not yet extended (the latest statement reviewed by 3 December), an extended loan running 36 months more at its note rate, it extends about three-fifths of the $4.7 billion due through 2027 and puts the pool's averaged loss at $150 million.
7. For the hedge programme, the register's live ALM trades are parted by what each is designated against, amortizing swaps at the notional of the period in effect, the four bilateral trades the clearing statement holds as the client references of cleared trades counted once as cleared, and the new overlay counted at $1.2 billion at every 2027 quarter-end.
8. The largest averaged loss is the fixed-rate commercial real estate pool's, $150 million against about $110 million for agency MBS: designate the overlay against it.

## 4. Deliverable Answers

### overlay_designation_2027.xlsx

1. Designated pool: Fixed-rate commercial real estate.
2. Averaged +200 bp loss in economic value: $150 million.
3. Hedge programme notional in effect, $ millions:
   - 31 March 2027: overlays 3,127.8; funding hedges 437.5; loan hedges 2,047.5
   - 30 June 2027: overlays 3,114.3; funding hedges 437.5; loan hedges 1,647.5
   - 30 September 2027: overlays 3,101.2; funding hedges 537.5; loan hedges 1,313.2
   - 31 December 2027: overlays 3,088.4; funding hedges 537.5; loan hedges 1,313.2

### overlay_designation_alco.pptx

1. Slide 1 states the designation, fixed-rate commercial real estate, and its averaged loss, $150 million.
2. Slide 2 charts one stacked bar per 2027 quarter-end, overlays, funding hedges and loan hedges stacked, each segment labelled with its value as in the workbook.
