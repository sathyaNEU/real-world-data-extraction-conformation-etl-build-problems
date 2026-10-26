## Tags

> **Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
> **Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Start the 2027 pack programme in Lancashire.** Its HFC packs lost 16% of their full charge in 2026, 3 points more than Yorkshire's 13%. Not the North East, whose packs were charged 16% of their charge in 2026 but entered the year short of refrigerant they had lost in 2025, so they lost 13%; not Lancashire on the charges alone (9%), which leave out the refrigerant its packs had lost by the end of 2026 and not yet had replaced.

## 2. Critical Components

1. 2026 refrigerant lost as a share of the HFC packs' full charge: Lancashire 16%; Yorkshire 13%; North East 13%; Cumbria 11%
2. HFC packs in service throughout 2026: Yorkshire 56; Lancashire 48; North East 43; Cumbria 29
3. Refrigerant charged less recovered in 2026, as a share of full charge: Yorkshire 9%; Lancashire 9%; North East 16%; Cumbria 10%

## 3. Step-by-Step Solution

1. Took the HFC packs in service throughout 2026 from the Packs sheet of fgas_register_2026.xlsx (Refrigerant Strategy 2.3), each to its region by its store in hallowmere_stores.csv: 176 packs.
2. Summed each pack's 2026 refrigerant charged less recovered on its routine and breakdown jobs in kelbray_job_sheets_2024_2026.csv (the store number padded to three digits, trade names read as R448A and R449A).
3. Measured each pack's own receiver response from its 2024 to 2026 job sheets: the median of (departure level less arrival level) over (kilograms charged less recovered) on its charges over 0.5 kg, and its full level as the median departure level.
4. Read each pack's shortfall on 31 December 2025 and on 31 December 2026 from tarnley_receiver_levels_2024_2026.csv through tarnley_pack_tags.csv: full level less the day's mean level, over the response, and not below zero.
5. Each pack's 2026 loss is its net charge plus its shortfall at the end of 2026 less its shortfall at the end of 2025; each region's losses added up over its full charges added up (Strategy section 3): Lancashire 16%; Yorkshire 13%; North East 13%; Cumbria 11%.
6. Full charge in tonnes of CO2 equivalent at the strategy's GWP table, each pack at the refrigerant on its latest job sheet, which for packs retrofitted by the gas supplier is the new blend while the register still lists R404A: Yorkshire 14,087; Lancashire 13,056; North East 13,054; Cumbria 8,123; on R404A Yorkshire 2,506; Lancashire 3,744; North East 5,710; Cumbria 2,057.
7. Cabinet and cold room charges: each 2026 job on an asset of the register's Cabinets and cold rooms sheet counted once at the weight its cylinder lost in kelbray_cylinder_log_2026.csv, since some handheld jobs carry the job's total on every asset line: Yorkshire 38.9; Lancashire 28.7; North East 23.5; Cumbria 36.6 kg.
8. The programme starts in Lancashire, the region whose packs lost the largest share of their charge in 2026.

## 4. Deliverable Answers

### hfc_pack_replacements_2027.xlsx

1. First region of the 2027 programme: Lancashire
2. 2026 refrigerant loss as a share of full charge: Yorkshire 13%; Lancashire 16%; North East 13%; Cumbria 11%
3. HFC packs' full charge in tonnes of CO2 equivalent: Yorkshire 14,087; Lancashire 13,056; North East 13,054; Cumbria 8,123
4. Of which on R404A, in tonnes of CO2 equivalent: Yorkshire 2,506; Lancashire 3,744; North East 5,710; Cumbria 2,057
5. Refrigerant charged in 2026 into integral cabinets and cold rooms, kilograms: Yorkshire 38.9; Lancashire 28.7; North East 23.5; Cumbria 36.6

### pack_leakage_2026.png

1. Horizontal bars of the four regions' 2026 loss shares, Lancashire (16%) highlighted, Yorkshire 13%, North East 13%, Cumbria 11%
