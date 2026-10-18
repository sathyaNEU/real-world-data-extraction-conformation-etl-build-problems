## Tags

**Domain:** General Statistics & Data Science, missing data, censoring and measurement error (which of six haddock grounds the Dunvarra Fish Producers' Organisation closes to its members' towed gear in 2027, by each ground's haddock stock in 2026 against its 2019 to 2021 average, estimated over the whole stock area from the autumn survey's fixed stations when the members' logbooks cover only the cells the boats chose to tow).
**Analytical objective:** Descriptive & Distribution Analysis (how each ground's haddock stock is distributed over its depth bands and how far each ground's total has fallen against its base).

## 1. Final Recommendation

**We should close Halmorie Deep to members' towed gear for 2027.**
Its haddock stock in 2026 was 63% below its 2019 to 2021 average, 11 points more than Brettach Bank's 52%, the next largest fall. Not Brettach Bank on the members' catch per hour towed, which ranks it first because on Halmorie Deep the boats followed the shrinking stock into the deep band and stopped towing the cells it left, so the catch rate held up while the stock fell. Not Brettach Bank on the survey's plain average of every tow either, which counts Halmorie Deep's deep band, 9% of its stock area, as a third of the ground.

## 2. Critical Components

1. Halmorie Deep's haddock stock fell **63%** from its 2019 to 2021 average to 2026.
2. Brettach Bank's fell **52%**, the next largest fall.
3. Halmorie Deep's fall exceeds Brettach Bank's by **11 points**.

## 3. Step-by-Step Solution

1. Per the recovery plan (stock_recovery_plan_2026.pdf, 4.1 and 4.2) the 2027 closure goes to the ground whose 2026 haddock stock, the weight of haddock on the Annex A cells of its stock area, has fallen furthest below its 2019 to 2021 average.
2. Placed each tow in survey_tows_2019_2026.csv in its grid cell by its shot position and took the cell's ground and depth band from ground_grid_annex_a.csv; the survey puts twelve stations in each depth band of every ground whatever the band's area (autumn_survey_manual_rev3.pdf, section 2).
3. For each ground and year, averaged haddock_kg over each band's tows and weighted each band by its share of the ground's stock area (the sum of its cells' area_km2), so Halmorie Deep's deep band, 9% of its area, counts for 9%.
4. Divided each ground's 2026 stock by its 2019 to 2021 average: falls of 63% for Halmorie Deep, 52% for Brettach Bank, 34% for Skiravie Bank, 32% for Moraskie Ground, 23% for Vallaskie Hole and 5% for Cullardy Patch.
5. Halmorie Deep's fall exceeds Brettach Bank's by 11 points, worked from the unrounded falls.
6. Took the haddock lines of sales_notes_2026.csv landed from 1 January to 30 September 2026 by member vessels under the letters member_vessels.xlsx's registration history gives them on the landing day, each re-issued note (same buyer, vessel and landing, the same lots, issued later) in place of the note it corrects, every presentation put on live weight by conversion_factors.csv, summed by port.
7. Summed quota_ledger_2026.csv by pool over the entries with effect on or before 30 September 2026 (quota rules, section 3), the blank-licence 1 January allocation of each pool, which equals the sum of its licences' allocations, counted once.
8. Recommended closing Halmorie Deep for 2027, its fall of 63% the largest of the six grounds.

## 4. Deliverable Answers

### ground_closure_2027.xlsx

1. Each ground's fall in haddock stock from its 2019 to 2021 average to 2026, whole percent:
   - Skiravie Bank: 34%
   - Halmorie Deep: 63%
   - Moraskie Ground: 32%
   - Brettach Bank: 52%
   - Vallaskie Hole: 23%
   - Cullardy Patch: 5%
2. Haddock members landed at each port from 1 January to 30 September 2026, in tonnes live weight, and its value at first sale:
   - Eastquay: 1,257 t; £2,512,050
   - Kelmoor: 1,833 t; £3,582,185
   - Tolsetter: 1,213 t; £2,387,574
   - Haldness: 1,550 t; £3,059,583
3. Haddock quota each pool had left on 30 September 2026, in tonnes:
   - North trawl (N): 1,503
   - East trawl (E): 1,079
   - Twin rig (T): 670
   - Seine net (S): 713
   - Inshore (I): 250

### closure_committee_2027.pptx

1. The recommendation on slide 1: close Halmorie Deep to towed gear in 2027, its fall 11 points more than Brettach Bank's.
2. Line chart on slide 2 of each ground's haddock stock from 2019 to 2026 as a percentage of its 2019 to 2021 average, with the base drawn at 100 and Halmorie Deep highlighted.
