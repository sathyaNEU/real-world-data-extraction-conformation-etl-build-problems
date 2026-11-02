## Tags

**Domain:** Energy Systems & Utilities (load forecasting: the design-day flow a district heating station must carry as a housing corporation's 1960s blocks leave their gas boiler rooms for the network).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**OS West first runs short of design-day flow in the 2028-29 heating season.** The blocks connected by 1 October 2028 need about 200 m3/h against the 167 m3/h available, short by about 30 m3/h, while the 2027-28 blocks fit at about 150 m3/h. Not that the station holds in both seasons, which carries the blocks at the network's 40 K design drop, its 38.8 K metered drop or the 31.1 to 41.6 K of its pre-1985 buildings, drops their original radiators do not make. Not 2027-28, which carries them at a textbook radiator drop of 20 K.

## 2. Critical Components

1. The blocks keep their radiators, and the network's original-radiator connections (cold-day returns 63.7 to 66.3 C, against at most 54.7 C for every other connection) make a cold-day drop of **about 24 K** (24.1 K, the mean of their 19 drops).
2. Phases 1 to 3 (4,240 kW) need about **150 m3/h** in 2027-28, under the **167 m3/h** available.
3. Phases 1 to 6 (5,533 kW) need about **200 m3/h** in 2028-29, **30 m3/h** short.

## 3. Step-by-Step Solution

1. Read procedure_capaciteitstoets_aansluitingen_v3.pdf sections 3.2 to 3.4 and hydraulische_toets_os_west_2026-10-09.pdf: a block's design-day flow is its design heat load over 1.163 times the drop its installation makes at the connection on days with a daily mean of 0 C or lower, tested against the 167 m3/h available.
2. Took each complex's design heat loss from warmteverliesberekening_weidehaven_rev2_2026-09-18.xlsx (the most recent study, 3.4) and its phase from weidehaven_aardgasvrij_fasering_2027-2028.xlsx: 4,240 kW connected by 2027-28 and 5,533 kW by 2028-29.
3. Selected the 36 days with TG at or below 0 in weerstation_lekstede_dagwaarden_2025-2026.csv and mapped every meter in amr_warmtemeters_west_2025-10-01_2026-09-30.csv to its connection through the Meters sheet of aansluitregister_warmtenet_west_2026-10-01.xlsx.
4. The connections' mean cold-day returns split at a gap from 54.7 to 63.7 C, and the 19 connections above it are the network's original-radiator installations, the kind every block keeps (weidehaven_aardgasvrij_scope_2027-2028.docx section 2), with a mean cold-day drop of 24.1 K.
5. Divided each phase's load by 1.163 x 24.1 K: 151.3 m3/h for phases 1 to 3 and 197.5 m3/h for phases 1 to 6.
6. For gas, followed each complex's EAN to its boiler room's description in meterstamgegevens_gas_weidehaven_2026-10-01.xlsx to pick up the EANs re-registered in 2026, and took every meter's first and last register in the gas year from the 06:00 reads of 1 October in gas_telemetrie_ketelhuizen_weidehaven_2025-2026.csv or the master data's placement and removal readings.
7. For heat, ran each meter from its annual or connection read in driveby_opnames_warmtemeters_west_2024-10_2025-09.csv (GJ or MWh) to its AMR opening register on 1 October 2025, through the drive-by removal reading and the AMR placement reading in the Meters sheet where the meter was exchanged at migration, and took 2025-26 from the AMR registers per meter.
8. Applied 3.3: 2027-28 holds at 151.3 m3/h and 2028-29 needs 197.5 m3/h, 30.5 over the 167 available, so OS West first runs short in the 2028-29 heating season.

## 4. Deliverable Answers

### os_west_debiet_2027-2029.xlsx

1. First heating season short: 2028-29.
2. Design-day flow by phase, m3/h to the nearest 5:
   - Phase 1: 45
   - Phase 2: 50
   - Phase 3: 55
   - Phase 4: 20
   - Phase 5: 15
   - Phase 6: 10
3. Blocks connected by the start of each season, m3/h to the nearest 10:
   - 2027-28: 150 against 167 available, no shortfall
   - 2028-29: 200 against 167 available, shortfall 30
4. Column chart on the Seizoenen sheet: one bar per season (2027-28, 2028-29) labelled with its flow, the available 167 m3/h drawn as a line across both, axis in m3/h.
5. Boiler-room gas from 1 October 2025 to 1 October 2026, m3 to the nearest 1,000:
   - Phase 1: 238,000
   - Phase 2: 219,000
   - Phase 3: 231,000
   - Phase 4: 90,000
   - Phase 5: 72,000
   - Phase 6: 45,000
6. Heat taken by the connections, MWh (residential to the nearest 1,000, utility to the nearest 100):
   - Residential: 66,000 in the 2024-25 gas year, +8,000 in 2025-26
   - Utility: 11,800 in the 2024-25 gas year, +900 in 2025-26
