## Tags

**Domain:** Physical & Environmental Sciences (climate and weather extremes: the expected number of high waters reaching each candidate deck elevation of a temporary work trestle over a known April to May 2027 window at a Gulf of Maine harbor gauge, built from the window's own predicted high waters and the season's skew surges).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Cut the Granite Wharf trestle piles to a deck elevation of 11.60 ft MLLW.** High water is expected to reach that deck on 0.4 tides between 1 April and 31 May 2027 and the next elevation down, 11.35 ft, on 2.3, because the window's own high waters in the 2027 tide table sit low. Not 12.35 ft, the April and May record's exceedance rate moved to 2027 sea level, which expects 7.4 tides at 11.60 ft because it averages over tides much higher than this spring's.

## 2. Critical Components

1. Tides expected to reach the deck from 1 April to 31 May 2027 at 11.60 ft MLLW: **0.4**.
2. Tides expected to reach the next elevation down, 11.35 ft MLLW: **2.3**.
3. The 2027 design mean sea level the deck is set at: **5.40 ft MLLW**.

## 3. Step-by-Step Solution

1. Read ptg_verified_15min_1995-01_2026-06.csv (quality V readings, less the 4.21 ft station datum offset of the datum sheet) and, after June 2026, ptg_telemetry_6min_2026-05_2026-11.csv (metres to feet, less the 4.09 ft of STND 2026) as one ft MLLW series.
2. Converted every high water in port_tessaly_tide_tables_1995-2027.xlsx to UTC (EST all year to 2006, local EST/EDT from 2007) and took the series' highest reading within three hours of each.
3. For the April and May high waters of 1995 to 2026, took the skew surge (observed less predicted high water) less that year's mean sea level above the epoch's 5.12 ft from sea_level_guidance_2026.pdf.
4. For each of the 118 high waters of 1 April to 31 May 2027 in the 2027 sheet, took the share of those skew surges reaching each pile schedule elevation at the 5.40 ft design mean sea level, and summed them per elevation.
5. The lowest elevation with one tide or fewer is 11.60 ft (0.4 tides), 11.35 ft expecting 2.3: cut the piles to 11.60 ft.
6. Survival tides: the highest reading at each high water from 1 November 2016 to 30 November 2026, the verified readings between the bracket re-securing on 30 October 2017 and the sensor reset on 12 March 2018 raised 0.08 ft (station log and the datum sheet's levelling), the telemetry on STND 2026, five largest no two within three days.
7. Street closures: Front Street FLOOD work orders in dpw_street_closures_2016-2026.csv, the WOMS times read as UTC (they precede high water only so read), a work order opened within three hours of the previous one's closing counted as the same closure, the gauge's highest reading within three hours of each closure's start against 11.80 ft.

## 4. Deliverable Answers

### granite_wharf_trestle_deck.xlsx

1. Deck elevation: 11.60 ft MLLW.
2. Tides expected to reach the deck from 1 April to 31 May 2027: 0.4 at 11.60 ft, 2.3 at 11.35 ft.
3. Five highest tides at the gauge, 1 November 2016 to 30 November 2026, no two within three days:
   - 1. 28 October 2026, 14.68 ft MLLW
   - 2. 4 January 2018, 14.64 ft MLLW
   - 3. 13 January 2024, 14.59 ft MLLW
   - 4. 2 March 2018, 14.32 ft MLLW
   - 5. 23 December 2022, 14.27 ft MLLW
4. Front Street flooding closures by year, each closure once, and those with the gauge at 11.80 ft MLLW or higher within three hours either side of the start:
   - 2017: 30 closures, 24 with the gauge at 11.80 ft or higher
   - 2018: 42 closures, 36 with the gauge at 11.80 ft or higher
   - 2019: 47 closures, 33 with the gauge at 11.80 ft or higher
   - 2020: 36 closures, 30 with the gauge at 11.80 ft or higher
   - 2021: 26 closures, 20 with the gauge at 11.80 ft or higher
   - 2022: 30 closures, 18 with the gauge at 11.80 ft or higher

### trestle_deck_exposure.png

1. Bar chart of the tides expected to reach the deck at each pile schedule elevation, 10.60 to 12.60 ft, with a dashed line at one tide and the 11.60 ft bar marked.
