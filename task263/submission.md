## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (how far a state water infrastructure finance authority's $36 million of 2027 PFAS treatment-design grants reaches down its priority list, each grant sized on the wells whose own PFOA or PFOS is over 4.0 ng/L when every compliance sample is an entry-point blend of the wells pumping at collection).
**Analytical objective:** Descriptive & Distribution Analysis (each listed well's own PFOA and PFOS over 2024 and 2025, recovered from the blends at its entry point, and the grants and reach that follow).

## 1. Final Recommendation

**The $36 million reaches 16 of the 20 systems on the 2027 PFAS priority list, Torvik Water Utility through Valdahl Sanitary District; the Village of Nordvold is the first it cannot reach, and $451,200 is left.**
The grants rest on the 23 wells whose own water, solved from each entry point's samples as a mass balance of the wells pumping at collection, averaged over 4.0 ng/L of PFOA or PFOS; Nordvold's grant of $691,200 is more than the $451,200 left. Not 7 systems, which giving each well the average of the samples it ran in yields, because a clean well that runs beside a well over the line takes on that well's water. Not 8, from the same average weighted by each well's share of the flow, which still credits a well with its whole mixture. Not 11, from the average of the samples each well ran alone (and of every sample it ran in where it never ran alone), because the operators' peak wells only ever run beside a lead.

## 2. Critical Components

1. The listed systems' active wells whose own water averaged over 4.0 ng/L of PFOA or PFOS in 2024 and 2025: **23** of **53**
2. The sixteen grants funded total **$35,548,800**, leaving **$451,200**
3. The Village of Nordvold's grant of **$691,200** is more than the **$451,200** left

## 3. Step-by-Step Solution

1. Took the twenty systems of Table 6-1 in iup_2027_draft_section6_pfas_design_grants.pdf and their routine and confirmation samples collected in 2024 and 2025 in pfas_entry_point_results_2024-2026.csv (PFOA and PFOS at each sample's highest report revision, non-detects at half the reporting limit, blanks and duplicates set aside per the sampling guide): 302 samples at 24 entry points.
2. Read the wells in service and the entry point of each sample from pfas_field_collection_records_2024-2026.csv by state sample number (the 3 samples with none recorded left out), and each well's rated capacity and status from source_facility_inventory_2026.xlsx.
3. Solved each entry point's samples together by least squares, each sample's PFOA and PFOS the mix of the wells pumping in proportion to their rated capacities, for every active well's own PFOA and PFOS: 23 wells over 4.0 ng/L.
4. Sized each system's grant at $2.4 million per MGD of the rated capacity of those wells (gallons a minute times 1,440 over 1,000,000), capped at $6 million (section 6.3).
5. Funded Table 6-1 in order until the remaining set-aside did not cover the next grant (section 6.4): 16 systems, $451,200 left, Nordvold's $691,200 not covered.
6. Summed the 2025 gallons in monthly_operating_reports_2025.csv for the listed systems' wells (facility type Well in the inventory), each meter in source_meter_register_2026.csv counted once a month where two wells share it, by each system's county in Table 6-1.
7. Added to each listed system's population in community_water_system_register_2026.csv the populations of the systems that buy all their water from it, directly or through another buyer, on the in-service full-purchase connections in wholesale_connections_2026.csv (a buyer the register holds under an inactive id taken to the active system of the same name and county), each counted in the county where it is.
8. The $36 million reaches 16 systems, Torvik Water Utility through Valdahl Sanitary District.

## 4. Deliverable Answers

### pfas_design_grants_2027.xlsx

1. Each listed system's grant in Table 6-1's order, with the wells it rests on and whether the $36 million reaches it:
   - Torvik Water Utility: $1,728,000 (Well 1 over the line), funded
   - City of Halvorsen Water Department: $6,000,000 (Wells 1 and 2 over the line), funded
   - Lindvik Lake Municipal Water: $3,456,000 (Well 1 over the line), funded
   - Village of Wikstrom: $1,382,400 (Well 3 over the line), funded
   - Brekken Prairie Water Utility: $2,419,200 (Well 2 over the line), funded
   - Fjelstad Water and Light: $2,592,000 (Well 1 over the line), funded
   - Kesselring Waterworks: $2,764,800 (Well 1 over the line), funded
   - Village of Nesvold: $1,900,800 (Well 1 over the line), funded
   - Elvholm Falls Water Utility: $3,283,200 (Wells 2 and 4 over the line), funded
   - Ackerholt Creek Sanitary District: $1,555,200 (Well 1 over the line), funded
   - Village of Dalrud: $1,209,600 (Well 1 over the line), funded
   - Skogen Municipal Water: $3,801,600 (Wells 1 and 2 over the line), funded
   - Kjelland Bluff Water Utility: $1,036,800 (Well 2 over the line), funded
   - Isaksen Ridge Sanitary District No. 1: $864,000 (Well 1 over the line), funded
   - Village of Felsbach: $1,036,800 (Well 2 over the line), funded
   - Valdahl Sanitary District: $518,400 (Well 1 over the line), funded
   - Village of Nordvold: $691,200 (Well 2 over the line), not reached, the first it cannot reach
   - Glomstad Water Utility: $691,200 (Well 1 over the line), not reached
   - Town of Ekholm Sanitary District No. 2: $518,400 (Well 2 over the line), not reached
   - Opsahl Falls Water Utility: $1,209,600 (Well 2 over the line), not reached
2. Systems the $36 million reaches: 16
3. The first system it cannot reach: Village of Nordvold
4. Left of the $36 million: $451,200
5. Water the listed systems' wells pumped in 2025, million gallons to one decimal:
   - Granlund: 1,342.9
   - Engvall: 1,318.4
   - Hedstrom: 913.5
   - Sandholm: 714.6
6. People living in the county who get their water from any of those wells:
   - Granlund: 30,167
   - Engvall: 29,442
   - Hedstrom: 21,518
   - Sandholm: 17,614

### well_pfas_2027.png

1. A dot chart of the PFOA and PFOS of each of the listed systems' 53 active wells in list order against a dashed 4.0 ng/L line, on a log scale, the 23 wells over the line named in bold.
