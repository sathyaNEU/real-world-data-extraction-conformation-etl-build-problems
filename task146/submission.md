## Tags

**Domain:** Survey Research & Official Statistics (seasonal adjustment and official time-series production: the next value of the Unemployment Insurance Board's weekly initial claims series in the first claims week of a quarter, its quarter-start refiling by claimants refused in the closing quarter sized region by region, each region's monetarily ineligible determinations at the share its own past quarter turns sent back).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The board will first report about 16,000 initial claims nationally for the claims week ended 10 October 2026.**
About one refused claimant in four files again in the first claims week of a quarter in Western and three in ten in Coastal and Island, against fewer than one in ten in each other region, and the third quarter's 30,182 monetarily ineligible determinations sit 48.5 per cent in those three regions, so 4,000 to 5,000 claims filed again, about nine tenths of them there, lift a week that would otherwise be 11,000 to 12,000. Not the national determinations at the national rate, which size this quarter's refusals as if they sat where a usual quarter's do and predict past turns visibly worse out of sample. Not the seasonal step of past first claims weeks, which carries an average quarter's refusals.

## 2. Critical Components

1. July to September 2026 left **30,182** monetarily ineligible determinations, **48.5 per cent** of them in Western, Coastal and Island (about a fifth at a usual quarter turn)
2. The share of a region's closing-quarter ineligible determinations filed again in the first claims week of the next quarter, over the 50 quarter turns from April 2014 to July 2026: about one in four in Western, three in ten in Coastal and Island, fewer than one in ten in each of the other five regions
3. Claims filed again in the week ended 10 October 2026: between **4,000** and **5,000**, about nine tenths of them in Western, Coastal and Island
4. The rest of the week without them: between **11,000** and **12,000**

## 3. Step-by-Step Solution

1. Joined brs_weekly_initial_claims_2013-12-29_2021-06-20.csv (dates day first, region codes through regions_territorial_authorities_localities.csv) to uics_weekly_initial_claims_by_region_2021-06-27_2026-09-27.csv at the claims week of 27 June 2021: each region's initial claims by claims week to the week ended 3 October 2026 at its advance count, 11,695 nationally.
2. Summed each region's monetarily ineligible determinations in ui_program_statistics_2026-09.xlsx (headed insufficient in the sheets to June 2021) over the claims-week months of each calendar quarter, the claimants the technical notes allow to file again once the base period moves: 30,182 in July to September 2026, 48.5 per cent of them in Western, Coastal and Island.
3. At each of the 50 first claims weeks of a quarter from April 2014 to July 2026, regressed each region's change from the week before on that region's ineligible determinations in the quarter just closed, with one intercept per quarter of the year: about one in four filed again in Western, three in ten in Coastal and Island, fewer than one in ten in each other region; leaving one turn out, this region-by-region build predicts the national step better than one share for every region or the national determinations at the national rate.
4. Added to each region's week ended 3 October its fourth-quarter intercept and its share of its July to September determinations, and summed the eight regions: 4,000 to 5,000 claims filed again, about nine tenths of them in Western, Coastal and Island, on 11,000 to 12,000 for the rest of the week.
5. Counted every open layoff notice in es_layoff_notice_register_2025-26.xlsx and employer_portal_notices_export_2026-10-07.csv once (a register notice re-keyed onto the portal matches its portal copy on business number, first layoff and sites), amended notices in place of the ones they replace, notices withdrawn in es_case_notes_2026-07-01_2026-10-07.csv and reduced-hours notices left out, each site's workers in the region of its locality, by the period of the notice's first layoff (technical notes, section 5): the counts by region and period below.
6. From ic_open_data_by_industry_2023-2026.csv took new and additional claims in the claims weeks of July to September 2025 and 2026: before the claims week of 4 January 2026 the labels are the week's last day (a Saturday) and the division codes SIC 2006, mapped through sic_2006_sic_2023_concordance.xlsx to the groups in uib_industry_divisions_2026.csv; from that week the labels are the week's Sunday and the codes SIC 2023: the changes by group below.
7. The board will first report about 16,000 initial claims nationally for the claims week ended 10 October 2026.

## 4. Deliverable Answers

### ic_preview_2026-10-10.docx

1. The call in the opening line: about 16,000 initial claims for the claims week ended 10 October 2026, released Thursday 15 October 2026.
2. Line chart of national initial claims by claims week from the week ended 11 April 2026 to the week ended 3 October 2026, with the call for the week ended 10 October 2026 marked at 16,000.

### ic_preview_2026-10-10.xlsx

1. The call: 16,000 initial claims for the claims week ended 10 October 2026.
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
   - Agriculture, forestry and fishing: 3.6
   - Mining, energy and utilities: 1.3
   - Manufacturing: -4.8
   - Construction: 58.9
   - Wholesale, transport and storage: 0.8
   - Retail trade: 1.1
   - Accommodation and food services: 21.6
   - Information and communication: -11.8
   - Financial, insurance and property services: -7.0
   - Professional, scientific and technical services: -2.4
   - Administrative and support services: 1.3
   - Public administration and safety: -1.0
   - Education and training: 2.8
   - Health care, social assistance and other services: -5.1
