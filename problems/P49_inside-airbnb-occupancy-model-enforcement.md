# P49 — Short-let enforcement targeting: estimating nights from reviews, not from a calendar that hosts block

| Field | Value |
|---|---|
| Domain | Municipal housing enforcement / short-term rental regulation / platform data |
| Objective family | Anomaly Detection & Diagnostics |
| Task shape | 01 · Ranked list under a cap (25 host audits) |
| Core technique | Applying a documented occupancy-estimation model (review rate, length of stay, minimum-night override, occupancy cap); listing → host aggregation; single-snapshot discipline across repeated scrapes |
| Trap family (honest data) | Unavailable calendar days treated as booked; lifetime reviews instead of last-12-month reviews; repeated scrapes appended; host counts from the platform-wide field |
| Primary sources | Inside Airbnb (listings, calendar, reviews) for a city scrape; Inside Airbnb occupancy-model documentation; local short-let rules |

## 1. The real-world project

A London borough's housing enforcement team can open **25 host investigations** per quarter. Entire-home short lets in
London may not exceed **90 nights per calendar year** without planning permission. The analyst estimated nights as
calendar days marked unavailable, appended the last two quarterly scrapes "for coverage" and ranked hosts. The first
investigations found hosts whose calendars were blocked because they lived in the property.

## 2. The business decision (one deterministic recommendation)

**Which 25 hosts are investigated (largest estimated nights above 90 summed across their entire-home listings in the
borough), and which host is 26th?**

Rules (targeting method, using Inside Airbnb's published occupancy model):

* Snapshot: the single scrape in the folder (do not combine scrapes).
* Listings: `room_type = Entire home/apt` within the borough (`neighbourhood_cleansed`).
* Reviews in the last 12 months = reviews in `reviews.csv` dated within 365 days before the scrape date (equivalently
  `number_of_reviews_ltm`).
* Estimated bookings = reviews₁₂ ÷ 0.50 (review rate); nights per booking = max(average length of stay for London = 3.0 nights
  — use the value stated in the method — , `minimum_nights`); estimated nights = bookings × nights per booking, capped at
  70% × 365 = 255.5 → floor to 255.
* Excess nights per listing = max(0, estimated nights − 90); host score = Σ excess over the host's in-scope listings
  (`host_id`).
* Rank descending; ties by more in-scope listings, then lower `host_id`.

## 3. Why this gets overlooked in real projects

* The calendar file is the most "direct-looking" data, but `available = f` means *not bookable* — booked or blocked by the
  host. Inside Airbnb explicitly warns against using it as occupancy.
* `number_of_reviews` (lifetime) sits next to `number_of_reviews_ltm`; both are plausible.
* Quarterly scrapes repeat the same listings; appending doubles reviews and nights.
* `host_listings_count` counts listings platform-wide (other cities), not in the scrape.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `listings.csv.gz` (detailed, London scrape) | CSV | ~90k | Inside Airbnb | CC BY 4.0 | Listing attributes |
| 2 | `calendar.csv.gz` | CSV | ~30M | Inside Airbnb | CC BY 4.0 | Availability (decoy for occupancy) |
| 3 | `reviews.csv.gz` | CSV | ~1.8M | Inside Airbnb | CC BY 4.0 | Review dates |
| 4 | `listings_previous_scrape.csv.gz` | CSV | ~90k | Inside Airbnb | CC BY 4.0 | Prior scrape (must not be appended) |
| 5 | `neighbourhoods.geojson` | GeoJSON | 33 | Inside Airbnb | CC BY 4.0 | Borough boundaries |
| 6 | `inside_airbnb_data_assumptions.html` | HTML | — | Inside Airbnb "About"/data assumptions | CC BY 4.0 | Occupancy model |
| 7 | `deregulation_act_2015_s44_extract.pdf` | PDF | — | legislation.gov.uk | OGL v3.0 | 90-night rule |
| 8 | `data_dictionary.xlsx` | XLSX | — | Inside Airbnb | CC BY 4.0 | Fields |
| 9 | `targeting_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `scrape_metadata.json` | JSON | 1 | Inside Airbnb | CC BY 4.0 | Scrape date |

## 5. Deterministic solution path

1. Load the snapshot; filter borough and room type.
2. Count reviews in the 365-day window per listing; compute bookings, nights, cap; excess over 90.
3. Aggregate by host; rank; 25 + 26th.
4. Contrast: calendar-based, lifetime reviews, appended scrapes.

## 6. The traps

**Trap A — calendar unavailability as occupancy.** Owner-occupiers and dormant listings jump to the top.

**Trap B — lifetime reviews.** Long-running hosts dominate regardless of current activity.

**Trap C — appended scrapes.** Doubles estimates; ranking reshuffles where listing sets changed.

**Trap D — minimum-nights override or cap ignored.** Mis-estimates long-minimum listings and extreme reviewers.

## 7. Why the data is honest

Inside Airbnb publishes scraped public listing data with an explicit, documented occupancy model and caveats. The method
follows that documentation.

## 8. Draft task prompt (prose)

> We can open twenty-five short-let investigations this quarter: the hosts whose entire-home listings in the borough have the
> most estimated nights above the 90-night limit, under the targeting method in the folder. Using the Inside Airbnb snapshot,
> estimate nights per listing, aggregate to hosts and tell me the twenty-five and the twenty-sixth. Produce
> `host_targets.csv` (host_id, listings, reviews in last 12 months, estimated nights, excess, rank) and
> `excess_nights_chart.png`, ranked bars of host excess nights for the top forty with the cut after twenty-five. Add a
> one-page `targeting_memo.pdf` with the list, the margin at the cut, and how many of the twenty-five would differ under a
> calendar-based estimate.

## 9. Deliverables

* `host_targets.csv`, `excess_nights_chart.png`, `targeting_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 25 hosts + 26th + margin; estimates for ~8 spot-check listings; calendar-variant difference count.

## 11. Golden-output checklist

* Single scrape; entire homes; LTM reviews; model parameters; cap; host aggregation; decision stated.

## 12. Build notes (scope tuning)

* Use a borough with many multi-listing hosts; confirm Trap A replaces ≥ 5 of the 25.
* Quote the occupancy-model parameters exactly as Inside Airbnb documents them for London at the scrape date.
