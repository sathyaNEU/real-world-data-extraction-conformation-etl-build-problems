# task185 submission

## Tags

**Domain:** General Statistics & Data Science, exploratory data analysis and distribution assessment (a paired-instrument difference assessed across the range of the reading, for a weather-index cover priced off one station's record).
**Analytical objective:** Anomaly Detection & Diagnostics (separating the warming in Merrin Flat's heat days from the step its November 1995 change of instrument put into them).

## 1. Final Recommendation

**Quote Merrin Valley Winegrowers $525 a hectare for its 2027/28 heat-day cover, a premium that assumes 16.7 heat days and 4.1 severe heat days at Merrin Flat.**

The glass years, converted to today's probe at each half-degree reading, gain 54 heat days and 29 severe heat days, and the heat-day line rises 0.30 days a decade instead of 0.74. Not $567 a hectare, the unconverted record's premium, which converting the glass years by the average probe-minus-glass difference also files, because that difference moves no half-degree reading across 35.0 C or 40.0 C. Not one hot-day offset, which cannot carry 34.5 C over 35.0 C and 39.0 C over 40.0 C while leaving the reading below 34.5 C under 35.0 C.

## 2. Critical Components

1. Brought to the probe at each glass reading, the glass seasons gain **54** heat days and **29** severe heat days, the readings from **34.5** C and **39.0** C up crossing the two triggers.
2. On that basis the heat-day line rises **0.30** days a decade and the severe heat-day line **0.19**.
3. The two lines' values at 2027/28, the counts the premium assumes, are **16.7** heat days and **4.1** severe heat days.

## 3. Step-by-Step Solution

1. Joined the glass register in ncs_climatological_register_041207_1964_1995.xlsx to the approved TMAX of ncs_daily_041391_19951101_20270827.csv through the successor row of ncs_station_list_merrin_district.json: every day of the 62 seasons from 1965/66 to 2026/27 present, glass to 31 October 1995 and probe from 1 November 1995.
2. Averaged probe minus glass at each half-degree glass reading over every pair in ncs_parallel_observations_maxtemp.csv, the seven sites pooled: +0.72 C at 34.5 C and +1.35 C at 39.0 C.
3. Converted each glass day by the difference at its reading (linear between tabulated readings), the basis the heat-day clause of southward_weather_index_pricing_manual_rev3.pdf sets: the glass seasons gain 54 heat days and 29 severe heat days under the triggers of heat_cover_term_sheet_2027_28_quote.pdf.
4. Fitted each season's count against its first year by least squares, as the manual sets: the heat-day line rises 0.30 days a decade and reads 16.7 at 2027/28, the severe line 0.19 and 4.1.
5. Projected each season to 2027/28 by the slopes, paid it under the quotation term sheet, averaged the 62 payouts and loaded the burn by 1.32 as the manual sets: $525 a hectare.
6. Took the blocks on policy_schedule_HC104_merrin_valley_2027-08-26.csv in force on 1 December 2027, each once at its insured hectares, by the sub-district merrin_valley_block_register_2027-08.xlsx gives it (the co-operative's own sub-districts, as the extract notes say): 115 blocks and 722.7 hectares, priced at $525 a hectare to the nearest dollar, halves up, as the term sheet sets.
7. Summed gl6120_weather_claims_payments_FY2020_FY2028.csv by claim reference and gave each paid claim the season claims_register_heat_cover_2020_2027.csv records for it, so lodgements never paid drop out.
8. Quoted $525 a hectare.

## 4. Deliverable Answers

### heat_cover_quote_2027_28.pdf

1. Premium for 2027/28: $525 a hectare.
2. Counts the premium assumes for 2027/28: 16.7 heat days and 4.1 severe heat days.
3. The 2027/28 schedule by sub-district (member blocks, insured hectares to one decimal place, premium in whole dollars):
   - Upper Merrin: 28 blocks, 184.8 ha, $97,020
   - Lower Merrin: 17 blocks, 100.5 ha, $52,763
   - Kerrin Flats: 33 blocks, 178.7 ha, $93,818
   - Tolbin: 37 blocks, 258.7 ha, $135,818
4. Chart on the second page: heat days in each season from 1965/66 to 2026/27 on the probe's basis as bars, the least-squares line the premium is read from carried to 2027/28 with its 16.7 heat days marked, and the November 1995 changeover marked.

### heat_cover_payouts.csv

1. One row a season since 2019/20, claims paid and what they came to in whole dollars:
   - 2019/20: 25 claims, $80,344
   - 2020/21: 28 claims, $79,148
   - 2021/22: 36 claims, $50,260
   - 2022/23: 38 claims, $63,534
   - 2023/24: 45 claims, $195,809
   - 2024/25: 52 claims, $285,417
   - 2025/26: 54 claims, $433,200
   - 2026/27: 55 claims, $35,631
