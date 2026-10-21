## Tags

**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The 2027 private flood placement pilot should run in Wickmere, Amberjack Bay, Thornock, Lisgrove and Saltreach, with Eastmarsh next in line.**
The five have the lowest expected claim rates of the fourteen member counties, 2.6, 2.6, 2.8, 3.0 and 3.0 paid building claims per 1,000 building-years, against 3.7 for Eastmarsh. Not Kettlemoor or Dunholme, which fall to 1.7 and 2.1 only when every claim their buildings filed before they were elevated is dropped: the 2016 flood stood above the floors most of those buildings have now, and replayed on them the two counties stand at 21.7 and 23.0. Not the record as filed, which keeps the coast's floods that its elevated floors now clear.

## 2. Critical Components

1. Elevated insured buildings on 30 September 2026: **11,060**
2. Claims of 2016 that would come again on buildings elevated since: Dunholme **352**, Kettlemoor **276**
3. Expected claim rates per 1,000 building-years: Wickmere **2.6**, Amberjack Bay **2.6**, Thornock **2.8**, Lisgrove **3.0**, Saltreach **3.0**; Eastmarsh **3.7**; Kettlemoor **21.7**, Dunholme **23.0**

## 3. Step-by-Step Solution

1. From nfip_dsa_policy_history_2026-10-02.csv took the building policies the guidelines define and the buildings whose policy in force on 30 September 2026 shows the lowest floor at or above the base flood elevation, NGVD29 elevations converted with tsrfa_vertical_datum_offsets.csv: 11,060 buildings.
2. Counted each building's days of building cover from 1 January 2001 to 31 December 2025 once across its policies, each policy covering to the day before its expiration or cancellation date, over 365.25.
3. Joined the claims of nfip_dsa_claims_2001-2019.csv and nfip_dsa_claims_2020-2026.csv (UTC dates taken to Central time) under those buildings' building policies for losses of 2001 to 2025.
4. Replayed each claim on the building as it stands on 30 September 2026: its water stood at the claim's lowest floor elevation plus its depth in inches over 12, and it counts where that is an inch or more above the present lowest floor, as every building-policy claim with an inch or more of water above its floor was paid: Dunholme 352 and Kettlemoor 276 claims of 2016 count again, the coast's none.
5. Divided each county's counted claims by its building-years per 1,000 and took the five lowest and the sixth as the guidelines direct: Wickmere, Amberjack Bay, Thornock, Lisgrove, Saltreach, then Eastmarsh.
6. Ask A: among claims on 2026 losses with a building payment, merged each claim NFIP Direct entered under a policy not yet in force at the loss into the claim under the policy its prior_policy_number names for the same building and date of loss, counting it once at the later record's payments to date, unit owners' claims counted, as the guidelines direct.
7. Ask B: in tsrfa_hma_grants_export_2026-09-30.xlsx took the properties not withdrawn with no final inspection passed by 30 September 2026 in the Inspections sheet (the Properties status of projects approved before 12 January 2026 predates their later inspections), each at its approved cost times the project's federal cost-share percentage, by the county of its community.
8. Recommended Wickmere, Amberjack Bay, Thornock, Lisgrove, Saltreach for the pilot, Eastmarsh next in line.

## 4. Deliverable Answers

### tsrfa_2027_private_flood_pilot.xlsx

1. Expected claim rate per 1,000 building-years, the fourteen counties in rate order:
   - Wickmere: 2.6, pilot
   - Amberjack Bay: 2.6, pilot
   - Thornock: 2.8, pilot
   - Lisgrove: 3.0, pilot
   - Saltreach: 3.0, pilot
   - Eastmarsh: 3.7, next in line
   - Hensby: 4.6
   - Ravensholt: 5.4
   - Tesmond: 6.4
   - Menhaden Point: 7.1
   - Ivesby: 8.5
   - Gorran: 17.1
   - Kettlemoor: 21.7
   - Dunholme: 23.0
2. The five marked: Wickmere, Amberjack Bay, Thornock, Lisgrove, Saltreach; next in line: Eastmarsh.
3. Bar chart of the fourteen rates on the Pilot counties sheet, the five shaded dark.
4. Claims on losses in 2026 that carry a building payment, and the building payments made on them as of the extract, whole claims and whole dollars:
   - Amberjack Bay: 772 claims, $31,099,515
   - Dunholme: 446 claims, $17,948,675
   - Eastmarsh: 665 claims, $25,344,431
   - Gorran: 258 claims, $10,188,863
   - Hensby: 668 claims, $27,850,818
   - Ivesby: 285 claims, $12,820,441
   - Kettlemoor: 425 claims, $14,933,957
   - Lisgrove: 237 claims, $8,661,639
   - Menhaden Point: 744 claims, $30,873,950
   - Ravensholt: 234 claims, $9,030,331
   - Saltreach: 932 claims, $39,215,507
   - Tesmond: 167 claims, $7,362,347
   - Thornock: 201 claims, $9,551,979
   - Wickmere: 164 claims, $8,233,257
5. Buildings in elevation and acquisition projects not completed on 30 September 2026, and the federal share obligated to them, whole buildings and whole dollars:
   - Amberjack Bay: 35 buildings, $6,681,525
   - Dunholme: 29 buildings, $5,233,000
   - Eastmarsh: 56 buildings, $10,195,485
   - Gorran: 47 buildings, $7,247,655
   - Hensby: 37 buildings, $6,244,320
   - Ivesby: 26 buildings, $4,542,675
   - Kettlemoor: 28 buildings, $4,802,040
   - Lisgrove: 36 buildings, $6,424,755
   - Menhaden Point: 91 buildings, $15,273,270
   - Ravensholt: 22 buildings, $4,162,125
   - Saltreach: 34 buildings, $6,451,135
   - Tesmond: 40 buildings, $6,763,290
   - Thornock: 27 buildings, $4,530,945
   - Wickmere: 35 buildings, $6,036,255

### tsrfa_pilot_elevated_buildings_2026-09-30.csv

1. 11,060 rows, one per elevated insured building, with its county, its building-years to one decimal and its paid building claims as it stands: 1,395 claims in all, on 1,330 buildings.
