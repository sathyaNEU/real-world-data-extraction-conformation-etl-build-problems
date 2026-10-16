## Tags

**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production: a quarter-start refiling effect in the Unemployment Insurance Board's weekly initial claims series, sized by region and by the month of the refusal).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The board will first report about 17,000 initial claims nationally for the claims week ended 10 October 2026.**
In Western, Coastal and Island between two thirds and nine tenths of the claimants refused in a quarter's last month file again in the next quarter's first claims week, under one in five of those refused earlier, and of the third quarter's 26,035 monetarily ineligible determinations 40.1 per cent sit in those regions, 55.3 per cent of theirs made in September against about a third at a usual turn, so 5,000 to 6,000 claims filed again lift a week that would otherwise be 11,000 to 12,000. Not each region's quarter taken whole at its average share, which weighs a July refusal like a September one and predicts past turns visibly worse out of sample. Not the national determinations at the national rate or the seasonal step of past first claims weeks, which miss where and when this quarter's refusals were made.

## 2. Critical Components

1. July to September 2026 left **26,035** monetarily ineligible determinations, **40.1 per cent** of them in Western, Coastal and Island, and **55.3 per cent** of those three regions' were made in September (about a third in a quarter's last month at a usual turn)
2. The share of a region's closing-quarter ineligible determinations filed again in the first claims week of the next quarter, over the 50 quarter turns from April 2014 to July 2026, depends on the month of the refusal: in Western, Coastal and Island between two thirds and nine tenths of those refused in the quarter's last month, under one in five of those refused in its first two months; few in the other five regions at any month
3. Claims filed again in the week ended 10 October 2026: between **5,000** and **6,000**, about nine tenths of them in Western, Coastal and Island
4. The rest of the week without them: between **11,000** and **12,000**

## 3. Step-by-Step Solution

1. Joined brs_weekly_initial_claims_2013-12-29_2021-06-20.csv (dates day first, region codes through regions_territorial_authorities_localities.csv) to uics_weekly_initial_claims_by_region_2021-06-27_2026-09-27.csv at the claims week of 27 June 2021: each region's initial claims by claims week to the week ended 3 October 2026 at its advance count, 11,814 nationally.
2. Read each region's monetarily ineligible determinations by claims-week month from ui_program_statistics_2026-09.xlsx (headed insufficient in the sheets to June 2021), the claimants technical notes 2.3 allow to file again once the base period moves, keeping each quarter's three months apart: 26,035 in July to September 2026, 40.1 per cent in Western, Coastal and Island, 55.3 per cent of those three regions' in September.
3. At each of the 50 first claims weeks of a quarter from April 2014 to July 2026, regressed each region's change from the week before on its ineligible determinations in each month of the quarter just closed, with one intercept per quarter of the year: in Western, Coastal and Island two thirds to nine tenths of a quarter's last-month refusals filed again and under one in five of its earlier months', few elsewhere.
4. Left one turn out at a time: this build predicts the national step better than each region's quarter taken whole, one share for every region or the national determinations at the national rate.
5. Added to each region's week ended 3 October its fourth-quarter intercept and its shares of its July, August and September determinations, and summed the eight regions: 5,000 to 6,000 claims filed again, about nine tenths of them in Western, Coastal and Island, on 11,000 to 12,000 for the rest of the week.
6. Counted every open layoff notice in es_layoff_notice_register_2025-26.xlsx and employer_portal_notices_export_2026-10-07.csv once (a register notice re-keyed onto the portal matches its portal copy on business number, first layoff and sites), amended notices in place of the ones they replace, notices withdrawn in es_case_notes_2026-07-01_2026-10-07.csv and reduced-hours notices left out, each site's workers in the region of its locality, by the period of the notice's first layoff (technical notes, section 5): the counts by region and period below.
7. From ic_open_data_by_industry_2023-2026.csv took new and additional claims in the claims weeks of July to September 2025 and 2026: before the claims week of 4 January 2026 the labels are the week's last day (a Saturday) and the division codes SIC 2006, mapped through sic_2006_sic_2023_concordance.xlsx to the groups in uib_industry_divisions_2026.csv; from that week the labels are the week's Sunday and the codes SIC 2023: the changes by group below.
8. The board will first report about 17,000 initial claims nationally for the claims week ended 10 October 2026.

## 4. Deliverable Answers

### ic_preview_2026-10-10.docx

1. The call in the opening line: about 17,000 initial claims for the claims week ended 10 October 2026, released Thursday 15 October 2026.
2. Line chart of national initial claims by claims week from the week ended 11 April 2026 to the week ended 3 October 2026, with the call for the week ended 10 October 2026 marked at 17,000.

### ic_preview_2026-10-10.xlsx

1. The call: 17,000 initial claims for the claims week ended 10 October 2026.
2. Workers to be laid off under layoff notices given to the board, by region and the period of the first layoff:
   - Northern: 11 to 31 October 111, November 121, December 230
   - Capital: 11 to 31 October 360, November 463, December 238
   - Eastern: 11 to 31 October 205, November 101, December 164
   - Midlands: 11 to 31 October 198, November 499, December 290
   - Western: 11 to 31 October 198, November 697, December 555
   - Southern: 11 to 31 October 136, November 548, December 139
   - Coastal: 11 to 31 October 300, November 828, December 242
   - Island: 11 to 31 October 350, November 277, December 139
3. Change in initial claims from July to September 2025 to July to September 2026, by industry group, per cent to one decimal:
   - Agriculture, forestry and fishing: 6.5
   - Mining, energy and utilities: 0.9
   - Manufacturing: -4.2
   - Construction: 60.3
   - Wholesale, transport and storage: 4.4
   - Retail trade: 4.1
   - Accommodation and food services: 26.1
   - Information and communication: -11.7
   - Financial, insurance and property services: -1.2
   - Professional, scientific and technical services: -6.3
   - Administrative and support services: 2.3
   - Public administration and safety: 6.7
   - Education and training: 4.9
   - Health care, social assistance and other services: -2.7
