# FC18 — Forecasting hotel occupancy from bookings on hand: cancellations, stays and what was known at the snapshot

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Lodging and short-term-rental revenue management (booking-curve / pickup forecasting at hotel chains and marketplaces) |
| Domain | Hospitality revenue management / operations staffing |
| Task shape | 02 · Forecast across many periods (31 nightly occupancy forecasts → one committed staffing level) |
| Core method | Reconstructing on-the-books (OTB) inventory as of a snapshot date from booking and cancellation timestamps; additive net pickup by lead time and day of week; in-house (stay-night) occupancy |
| Analytical stump | The data show which bookings were eventually cancelled; excluding them from the snapshot OTB uses future information. Gross pickup ignores cancellations of bookings already on the books. Counting arrivals instead of occupied stay-nights mis-states occupancy for multi-night stays |
| Primary sources | Hotel booking demand datasets (Antonio, de Almeida & Nunes, 2019, Data in Brief) |

## 1. The real-world situation

A city hotel sets its **August housekeeping roster** on 1 July from a forecast of rooms occupied each night. Last year's
analyst counted current non-cancelled bookings for each arrival date and added the average number of bookings that came in
after the same lead time in earlier weeks. August was badly overstaffed on some nights and understaffed on others.

## 2. The decision (one deterministic recommendation)

**The committed roster level: the mean of the 31 nightly occupied-room forecasts for August 2017 (rounded up), as of 2017-07-01.**

Rules (revenue-management memo):

* Hotel: City Hotel file. Booking date = arrival date − lead time. Cancellation date = reservation-status date for cancelled
  bookings. A booking is on the books at snapshot s if booked ≤ s and not cancelled ≤ s.
* A booking occupies one room on each night from arrival through arrival + total nights − 1 (weekend + week nights). No-shows
  do not occupy.
* Actual occupancy for a past night = rooms occupied by bookings that checked out.
* Net pickup for night n at lead L = actual occupancy(n) − OTB rooms for n at snapshot (n − L).
* Forecast for August night n (lead L = n − 2017-07-01) = OTB(n, 2017-07-01) + mean net pickup at the same lead for the 8 most
  recent same-weekday nights with complete history before 2017-07-01.

## 3. Why capable analysts get it wrong

* The file carries the final outcome of every booking; filtering `is_canceled = 0` before building the snapshot silently uses
  information from after the snapshot.
* Gross pickup (new bookings only) ignores that some on-the-books bookings will cancel.
* Arrivals-by-date is the natural grouping; occupancy requires expanding stays across nights.
* Multiplicative pickup factors explode for nights with few bookings on hand.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `H2.csv` (City Hotel) | CSV | 79,330 | Data in Brief 2019 (Antonio et al.) | CC BY 4.0 | Bookings |
| 2 | `H1.csv` (Resort Hotel) | CSV | 40,060 | Same | CC BY 4.0 | Context / alternative |
| 3 | `hotel_bookings_data_dictionary.pdf` (article tables) | PDF | — | Same | CC BY 4.0 | Field definitions |
| 4 | `stay_nights_city_2015_2017.parquet` | Parquet | ~250k booking-nights | Derived | CC BY 4.0 | Expanded stays |
| 5 | `otb_snapshots_city.parquet` | Parquet | ~1M (night × snapshot) | Derived | CC BY 4.0 | Snapshot inventory |
| 6 | `portugal_holidays_2015_2017.json` | JSON | ~40 | Public calendar | Public | Context |
| 7 | `revenue_management_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `last_year_roster_method.xlsx` | XLSX | ~31 | Task author | — | Gross-pickup approach |
| 9 | `talluri_van_ryzin_pickup_reference.pdf` (citation) | PDF | — | Cite | Cite | Pickup method |
| 10 | `august_2017_actuals_holdout.csv` | CSV | 31 | Derived (for validation only) | CC BY 4.0 | Back-test check |

## 5. Deterministic solution path

1. Build booking and cancellation dates; expand non-no-show stays into nights.
2. Compute OTB for every night at every needed snapshot using only information up to the snapshot.
3. Compute net pickup by lead and weekday from historical nights; average the last 8 same-weekday nights.
4. Forecast August nights; mean; round up. Validate against actual August occupancy (reported, not used).
5. Contrast with gross pickup, outcome-filtered OTB and arrivals-based counts.

## 6. Wrong paths (method errors, not misreadings)

**A — OTB filtered by final status.** Look-ahead; OTB too low, pickup history inconsistent.

**B — gross pickup.** Ignores future cancellations; forecast too high.

**C — arrivals not stay-nights.** Weekday/weekend occupancy shapes wrong.

**D — multiplicative pickup.** Unstable on low-OTB nights.

## 7. Why the stump is analytical, not semantic

Every date needed to rebuild the snapshot is in the file and the memo defines occupancy and pickup. The error is temporal leakage
and the wrong unit of occupancy — analytical choices.

## 8. Draft task prompt (prose)

> Set the August 2017 housekeeping roster for the city hotel from a forecast made on 1 July, as the revenue-management memo
> describes: rooms on the books that day plus typical net pickup for the remaining lead time. Provide `august_forecast.csv` (night:
> lead, on-the-books, net pickup, forecast, later actual), `booking_curves.png` showing how occupancy for a few August nights built
> up versus lead time, and a one-page `roster_memo.pdf` with the committed level and how far last year's method would have been off.

## 9. Deliverables

* `august_forecast.csv` (31 rows), `booking_curves.png`, `roster_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 31 nightly forecasts (spot-check ~12); committed level; validation MAE; gross-pickup and outcome-filtered contrasts.

## 11. Golden-output checklist

* Snapshot-consistent OTB; stay expansion; net pickup by lead/weekday; 8-night average; rounding.

## 12. Build notes (scope tuning)

* Confirm the dataset's date fields allow cancellation timing (reservation status date) for all cancelled bookings; document any
  with missing dates.
* Check that the outcome-filtered OTB method changes the committed level by ≥ 5%.
