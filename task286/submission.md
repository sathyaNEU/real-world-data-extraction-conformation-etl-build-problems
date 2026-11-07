## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**The 2027 Homes in Use pilot should go to Orrimouth, where 203 homes stood unused for at least 26 of the 52 weeks
from 29 September 2025 to 27 September 2026, 44 more than Ellingsea's 159.** Not Ellingsea, which comes first only
when a week with little water on the meter is taken as a week nobody used, so that empty homes whose cisterns or
supply pipes run on every day count as lived in; not Kittlesea or Tarnhithe, which lead on the council tax records
and the 2021 census, neither of which records a year of use.

## 2. Critical Components

1. A week is used only when the home's daily totals rise above that home's own steady level: **a week whose
   highest day is no more than 50 litres above its lowest is a week nobody used**, and any margin from 30 to 75
   litres gives the same count in every area.
2. Homes nobody used for 26 or more of the 52 weeks: **Orrimouth 203, Ellingsea 159**, Tarnhithe 119, Kittlesea 113,
   Brackwater 104, Quellby 55, Wennaby 51, Crackmoor 49.

## 3. Step-by-Step Solution

1. Added the two rows of each meter-exchange day in meter_reads_daily_2025-26.parquet and kept the 52
   Monday-to-Sunday weeks from 29 September 2025, as the terms of reference set the window and the week: every
   property has 52 complete weeks.
2. Placed each property in its community area through pw_property_uprn_match_2026-10.csv and
   county_gazetteer_extract_2026-10.csv, by postcode where the match has no UPRN: 5,730 homes, one meter each.
3. Read each week against the home's own steady level: a week is unused when its highest day is no more than 50
   litres above its lowest, so a home whose meter registers the same litres every day with nobody in shows no week
   of use, and every margin from 30 to 75 litres gives the same counts.
4. Counted the homes with 26 or more unused weeks in each area: Orrimouth 203, Ellingsea 159, a gap of 44.
5. Long-term empty homes: took each home's council tax liability covering 27 September 2026 in
   swanholt_ctax_extract_2026-10-06.csv and teversby_ctax_extract_2026-10-05.xlsx, followed each unoccupied and
   unfurnished spell back across consecutive accounts on the same dwelling and, for Teversby accounts carried
   across on 5 May 2026, into teversby_ctax_legacy_archive_to_2026-05-04.csv by valuation list reference, and
   counted the spells begun before 27 March 2026 that are not exempt, as council_taxbase_returns_october_2025.pdf
   defines them.
6. Self-catering homes: kept the entries of ndr_self_catering_entries_2026-10.csv in effect on 27 September 2026,
   joined each to the gazetteer through NDR_XREF and counted every dwelling a site entry covers (the dwellings
   under the site's parent shell).
7. Split each area's unused homes into 26 to 38, 39 to 51 and all 52 unused weeks for the chart.
8. Recommended Orrimouth, the area with the most homes nobody used for 26 or more weeks.

## 4. Deliverable Answers

### homes_in_use_pilot_2027.xlsx

1. Pilot area: Orrimouth, 203 homes nobody used for 26 or more of the 52 weeks; runner-up Ellingsea, 159 homes; gap
   44 homes.
2. Homes nobody used for 26 or more of the 52 weeks, by area, whole homes:
   - Orrimouth: 203
   - Ellingsea: 159
   - Tarnhithe: 119
   - Kittlesea: 113
   - Brackwater: 104
   - Quellby: 55
   - Wennaby: 51
   - Crackmoor: 49
3. Long-term empty homes on the council tax records on 27 September 2026, as the Council Taxbase return defines
   them, whole homes:
   - Orrimouth: 20
   - Ellingsea: 39
   - Tarnhithe: 14
   - Kittlesea: 6
   - Brackwater: 30
   - Quellby: 17
   - Wennaby: 10
   - Crackmoor: 15
4. Homes on the business rates list as self-catering holiday lets on 27 September 2026, whole homes:
   - Orrimouth: 9
   - Ellingsea: 23
   - Tarnhithe: 51
   - Kittlesea: 27
   - Brackwater: 13
   - Quellby: 6
   - Wennaby: 10
   - Crackmoor: 7

### empty_homes_by_area_2026.png

1. One bar per area of the homes nobody used for 26 or more weeks, split into 26 to 38 weeks, 39 to 51 weeks and
   all 52, each part labelled with its count:
   - Orrimouth: 15, 108 and 80 (203)
   - Ellingsea: 21, 97 and 41 (159)
   - Tarnhithe: 50, 60 and 9 (119)
   - Kittlesea: 22, 84 and 7 (113)
   - Brackwater: 18, 58 and 28 (104)
   - Quellby: 5, 28 and 22 (55)
   - Wennaby: 10, 37 and 4 (51)
   - Crackmoor: 9, 26 and 14 (49)
