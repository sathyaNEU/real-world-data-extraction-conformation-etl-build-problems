# P28 — Which routes are overpriced? Airfares from the 10% ticket sample without double counting round trips

| Field | Value |
|---|---|
| Domain | Air service development / airline network planning / consumer pricing analysis |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (three routes pitched to airlines) |
| Core technique | Choosing the right grain among Coupon/Market/Ticket tables; fare proration to markets; passenger weighting; credibility/bulk filters; city-market (multi-airport) conformance; non-directional aggregation |
| Trap family (honest data) | Ticket fare joined onto both market legs; unweighted averages; airport pairs instead of city markets; directional-only markets |
| Primary sources | BTS Airline Origin & Destination Survey (DB1B Market, Ticket, Coupon), BTS lookup tables |

## 1. The real-world project

A mid-size airport's air-service development team pitches **three routes** a year to airlines, choosing city pairs where
local travellers pay the most relative to a distance benchmark. The analyst joined DB1B Ticket fares to Market rows,
averaged fares per airport pair and compared them with an industry fare-per-mile curve. Round-trip-heavy leisure routes
looked twice as expensive as they were; the team's best opportunity was split across three New York airports and never
surfaced.

## 2. The business decision (one deterministic recommendation)

**Which three city pairs from the home city should be pitched for 2025, and which is fourth?**

Rules (route-pitch method):

* Data: DB1B Market, four quarters of 2023, domestic.
* Fare per market = `MktFare` (BTS prorates the itinerary fare: ItinFare ÷ (RoundTrip + 1)). Never join `ItinFare` from the
  Ticket table onto Market rows.
* Filters: credible fares only (Ticket `DollarCred = 1`, linked by `ItinID`), `BulkFare = 0`, `MktFare` ≥ $25.
* Weighting: averages are passenger-weighted (`Passengers`).
* Geography: city markets (`OriginCityMarketID`/`DestCityMarketID`), **non-directional** (A→B and B→A combined).
* Candidate set: the 20 destination city markets in the folder; minimum 1,000 sampled passengers (both directions) per
  pair.
* Benchmark: national passenger-weighted average fare per market mile (`MktFare ÷ MktDistance`) for the pair's
  `MktDistanceGroup`, × the pair's passenger-weighted mean `MktDistance`.
* Premium = pair average fare ÷ benchmark − 1. Rank; pitch the top three.

## 3. Why this gets overlooked in real projects

* DB1B has three tables at three grains. Ticket has the itinerary fare; Market has the prorated fare. Joining the
  itinerary fare onto each market doubles round-trip fares.
* The `Passengers` field is easy to ignore because each row "is a ticket".
* Airport pairs fragment multi-airport cities (NYC, Washington, Chicago, Bay Area, Los Angeles basin); demand and fares
  must be aggregated by city market to match how airlines evaluate routes.
* Directional markets halve volume and can fall under the minimum.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–4 | `Origin_and_Destination_Survey_DB1BMarket_2023_1..4.csv` | CSV | ~5–6M each | BTS TranStats | U.S. Gov public domain | Market-level fares |
| 5–8 | `…_DB1BTicket_2023_1..4.csv` | CSV | ~3–4M each | BTS | Public domain | Credibility flags |
| 9 | `…_DB1BCoupon_2023_1.csv` | CSV | ~9M | BTS | Public domain | Grain illustration (not needed for the answer) |
| 10 | `L_CITY_MARKET_ID.csv` | CSV | ~6k | BTS | Public domain | City markets |
| 11 | `L_AIRPORT_ID.csv` | CSV | ~6.5k | BTS | Public domain | Airports |
| 12 | `db1b_table_profiles.pdf` | PDF | — | BTS | Public domain | Field definitions (MktFare proration) |
| 13 | `route_pitch_method.pdf` | PDF | — | Task author | — | Rules in §2 |
| 14 | `candidate_destinations.json` | JSON | 20 | Task author | — | Scope |

## 5. Deterministic solution path

1. Load Market rows; join Ticket credibility by `ItinID`; apply filters.
2. Compute national benchmark fare-per-mile by distance group (all domestic markets).
3. Filter home-city pairs (both directions) to candidates; aggregate passenger-weighted fare and distance by city pair.
4. Compute benchmark fare and premium; apply minimum passengers; rank; top three + fourth.
5. Contrast: ticket-fare join, unweighted, airport-pair, directional variants.

## 6. The traps

**Trap A — itinerary fare on market rows.** Round-trip-heavy pairs show ~2× fares and dominate the top three.

**Trap B — unweighted averages.** Group tickets and multi-passenger records lose weight; premiums shift.

**Trap C — airport pairs.** Multi-airport destinations split and fall under the minimum.

**Trap D — no credibility/bulk filters.** Zero-dollar award tickets and bulk fares depress premiums.

## 7. Why the data is honest

DB1B is the DOT's official 10% ticket sample, with documented proration and flags. The structure is complex, not wrong.

## 8. Draft task prompt (prose)

> We pitch three routes to airlines each year: the city pairs from our city where travellers pay the biggest premium over
> a distance-based benchmark, per our route-pitch method. Using the DB1B files in the folder, rank the twenty candidate
> destinations and tell me the three to pitch and the one just behind. Deliver `route_premiums.csv` with each pair's
> sampled passengers, average fare, mean distance, benchmark fare, premium and rank; and `route_premium_chart.png`, a
> ranked bar chart of premiums with the top three highlighted and pairs under the passenger minimum greyed out. Add a
> one-page `route_pitch_memo.pdf` with the three routes, the gap between third and fourth, and which pairs would have made
> the top three if the itinerary fare had been attached to every market.

## 9. Deliverables

* `route_premiums.csv`, `route_premium_chart.png`, `route_pitch_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 premiums/ranks (top 8 checked), benchmark per distance group used, top 3 + 4th + gap, minimum exclusions,
  ticket-fare variant top 3.

## 11. Golden-output checklist

* MktFare; credible, non-bulk; passenger-weighted; city markets; non-directional; decision stated.

## 12. Build notes (scope tuning)

* Choose a home city with leisure (round-trip-heavy) and multi-airport destinations among the candidates; confirm Traps A
  and C change the three.
* Verify the MktFare definition text in the BTS table profile you include.
