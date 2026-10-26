## Tags

**Domain:** Energy systems and utilities (asset condition and maintenance).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Tool 2027 as Mira city car 1,450, Volta hatch 900, Plover saloon 350, Kestrel SUV 250, Tern van 50 slots: the 3,000 slots in proportion to the 3,800 pack failures outside the OEM warranty forecast for the five platforms in the Netherlands in 2027.**
The packs that fail in 2027 are those of the cars in use in the Netherlands in 2027: the register of 30 June 2026 and the used imports that keep arriving after it. The Mira city car's imports arrive about 8.1 years old, past its five-year pack warranty, and fail in their first months here: 360 of its 1,829 forecast failures are theirs. Summed over the register alone, the Mira city car would get 1,250 slots, the Volta hatch 1,000, the Kestrel SUV 300 and the Tern van 100.

## 2. Critical Components

1. The population whose packs fall due in 2027 is every car in use in the Netherlands in 2027: the register of 30 June 2026 holds the cars that had arrived by then, and the used imports registered after it are in the fleet of 2027 too. Cars registered new after it are inside their warranty all year.
2. The register shows the arrivals: in the twelve months to 30 June 2026, **1,394** Mira city cars were first registered here after a first admission abroad, about **116** a month at **8.1** years old on average, past the Mira's **5**-year warranty; the other platforms' imports arrive inside their **8** years.
3. The 2027 forecast is **3,448** failures for the cars on the register and **363** for the imports still to arrive (**360** of them Mira city cars): **3,800** to the nearest hundred.
4. In lots of 50 the shares give Mira city car 28, Volta hatch 18, Plover saloon 6, Kestrel SUV 5, Tern van 1 whole lots; the **2** lots left go to the two largest remainders, the Mira city car's **0.79** and the Plover saloon's **0.70**, ahead of the Tern van's **0.42**.

## 3. Step-by-Step Solution

1. Took each car on rdw_gekentekende_voertuigen_20260630.csv (its make is its platform) with the pack it carried at the end of 30 June 2026 from accuvervangingen_2014_2026.csv, one pack per car as the plan's section 3 files it: its last replacement on or before that day (an OEM nieuw pack on the platform's curve, a Voltwerk revisie pack on the refurbished curve), else the pack it was built with from its datum eerste toelating; the OEM warranty ends 8 years after datum eerste toelating, 5 for the Mira city car (garantievoorwaarden_tractieaccu_2026.pdf), whatever was fitted since.
2. Gave each car the chance its pack fails in 2027 after the warranty, given it works on 30 June 2026: F(a1) less F(a0), over 1 less F(a) on 30 June 2026, pack ages in days since fitting over 365.25, F the curve in levensduurcurves_tractieaccu.csv read by straight lines, a0 at the later of 1 January 2027 and the warranty's end, a1 at 1 January 2028 (a pack fitted in its place after 30 June 2026 is left out); summed by platform, 3,448 in all.
3. The plan's fleet of 2027 also holds the cars first registered here from 1 July 2026 to the end of 2027, each from the day it is registered; the new cars among them stay inside their warranty all year. Took the used imports first registered here from 1 July 2025 to 30 June 2026 (datum eerste toelating before datum eerste tenaamstelling in Nederland), each with the pack the log shows it arrived with (its last replacement before that registration, else its original pack), and carried them into July 2026 to December 2027 at that rate and mix: each month takes in a twelfth of them on the same day of the month (the month's last day if shorter), at the same age, pack age and warranty, each at its chance of failing in 2027 after its warranty given its pack works on arrival; 363 in all.
4. Added the two by platform (Mira city car 1,829, Volta hatch 1,144, Plover saloon 425, Kestrel SUV 322, Tern van 91; 3,800 to the nearest hundred) and split the 3,000 slots in proportion: 60 lots of 50, each platform's whole lots first and the lots left to the largest remainders (the plan, tooling_plan_2027_draft.docx, section 2).
5. Modules: took the stores movements booked from 1 July 2025 to 30 June 2026 in magazijn_mutaties_2025-26.csv, issues less returns, each line in modules by artikelstam_modules.xlsx (a Kestrel carrier is 2) and on its work order's platform; no lot's stock goes below zero (lijn_exports_toelichting.md), so on a supplier lot whose lines add up to more than magazijn_ontvangsten_2025-26.csv shows it received (the replacement lots for held packs), the one quantity a pick list carries against several work orders went out once, which brings the lot back to what it received; divided by the packs shipped in those months in verzendingen_2025-26.csv and multiplied by 50.
6. First-run passes: followed each pakket_id in eol_testlog_2025-26.csv to its work order through mes_bms_koppelingen_2025-26.csv (a BMS replaced on rework gives the pack a new pakket_id), took each work order's first run that was not an ABORT, kept the packs whose first run started from 1 July 2025 to 30 June 2026 and took the share that passed.
7. Intake rejects: took the cores received from 1 July 2025 to 30 June 2026 in kernen_inname_2025-26.csv at either dock; a core with a work order in mes_werkorders_2025-26.csv was built on, so it passed intake, and its AFGEKEURD is the grade its scrapped pack left on 1 July 2026 (its quarantine tag in afvoer_recycler_2025-26.xlsx is dated the day the line scrapped it, an intake reject's the day it arrived); the share rejected is the AFGEKEURD rows with no work order over all the cores received.

## 4. Deliverable Answers

### voltwerk_tooling_2027.xlsx

1. Slots in 2027, by platform:
   - Mira city car: 1,450
   - Volta hatch: 900
   - Plover saloon: 350
   - Kestrel SUV: 250
   - Tern van: 50
2. Pack failures outside the OEM warranty forecast for 2027, all five platforms: 3,800
3. Modules a lot of 50 should carry, by platform:
   - Volta hatch: 167
   - Kestrel SUV: 274
   - Plover saloon: 190
   - Mira city car: 149
   - Tern van: 224
4. Share of the packs with a first end-of-line run from July 2025 to June 2026 that passed it, by platform:
   - Volta hatch: 92.6 per cent
   - Kestrel SUV: 88.2 per cent
   - Plover saloon: 94.0 per cent
   - Mira city car: 88.3 per cent
   - Tern van: 90.5 per cent
5. Share of the cores received from July 2025 to June 2026 that were rejected at intake, by platform:
   - Volta hatch: 8.9 per cent
   - Kestrel SUV: 5.9 per cent
   - Plover saloon: 11.0 per cent
   - Mira city car: 14.7 per cent
   - Tern van: 8.3 per cent

### voltwerk_tooling_2027.png

1. Each platform's 2027 forecast beside its slots, the Mira city car's 1,450 slots the largest.
