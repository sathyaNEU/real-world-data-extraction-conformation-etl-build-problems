## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (two remeasurements of a timber company's permanent inventory plots reconciled tree by tree where tags were lost between them).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Mark CF-112, CF-138 and CF-152 for the 2027 salvage program.**
Under Board Policy 7.4 their 2021 to 2026 losses are 27.0, 59.0 and 34.3 per cent of 2021 live basal area against the 15 per cent line, and the next highest stand is at 5.6. Not the five stands underburned in 2024 (CF-104, CF-118, CF-129, CF-144, CF-160): they read 21.5 to 27.2 per cent only when the 2026 tally is joined on tag numbers, because their trees not found are alive under the new tags the 2026 crews gave them, and they lost 3.5 to 5.6 per cent.

## 2. Critical Components

1. **371** trees tallied live in 2021 and coded not found in 2026 are the same trees the crews added under new tags, so they are tallied live in 2026.
2. The five underburned stands lost **3.5 to 5.6 per cent** of 2021 live basal area, not 21.5 to 27.2.
3. CF-138 lost **59.0 per cent**, its trees not found and not re-tallied counted as not tallied live (set aside, the stand would read **8.2**).
4. CF-152 lost **34.3 per cent** and CF-112 **27.0 per cent**.

## 3. Step-by-Step Solution

1. Took the trees tallied live in 2021 from `inventory/cfi_database.sqlite` (`tree_meas`, cycle 2021, status L): 6,859 trees, each placed in the stand of its condition through `inventory/plot_register.xlsx`.
2. Joined `inventory/trf_cfi_remeasurement_2026.csv` on plot and tag (padded strings to integers): every 2021 tag carries one 2026 status (L, D, C or M) and 1,135 records are coded N (added).
3. Placed every added record on its plot's 2021 stem map (`tree` azimuth and distance, both from true north): 371 stand within 2 feet of a tree coded not found, of its species (`inventory/species_codes.csv`) and a diameter consistent with five years of growth, and are that tree; 160 stand on a tree also recorded under its own found tag and are the same tree entered twice; the other 604 are trees new to the plot.
4. Applied Policy 7.4 section 2: 2021 basal area (0.005454 times DBH squared, field manual section 2) of the trees dead or not found and not re-tallied, cut trees aside, over each stand's 2021 live basal area by plot condition; CF-138, CF-152 and CF-112 are at 15 per cent or more and no other stand is above 5.6.
5. Live basal area per acre: every 2026 live record once (the 160 second entries dropped), by condition stand, over 0.2 acres times each condition's share in the plot register (field manual section 1).
6. Net Scribner volume per acre: live conifers of 11.0 inches and more (black oak excluded), merchantable height from the 2026 export or, for the plots measured July 20 to 24, from `inventory/trf_height_revisit_2026-09.csv`; height over 16.5 rounded down to the half log, at most six logs; Table 1 of the field manual at the 2-inch class, times 10 board feet, less cull; per acre of plot condition.
7. Wrote `tree_fates_2021_2026.csv` and `salvage_marking_2027.pdf`, marking CF-112, CF-138 and CF-152.

## 4. Deliverable Answers

### tree_fates_2021_2026.csv

1. 6,859 rows, one per tree tallied live in 2021, with plot, stand, 2021 tag, species, 2021 DBH, 2026 fate, 2026 tag and 2026 DBH.
2. 2026 fates: 6,278 live (371 of them under new tags), 330 dead, 237 missing (not found and not re-tallied), 14 cut.

### salvage_marking_2027.pdf

1. Stands to mark: CF-112, CF-138 and CF-152.
2. Stand table, share under Policy 7.4 (per cent), 2026 live basal area (square feet per acre), 2026 net Scribner volume (board feet per acre):
   - CF-101: 2.4, 165.4, 25,660
   - CF-104: 3.9, 202.4, 32,460
   - CF-107: 1.2, 196.9, 32,940
   - CF-112: 27.0, 172.7, 25,190
   - CF-115: 1.3, 179.1, 29,550
   - CF-118: 5.6, 201.9, 32,700
   - CF-121: 0.8, 207.5, 37,440
   - CF-126: 3.6, 176.7, 27,920
   - CF-129: 3.5, 184.8, 36,490
   - CF-133: 1.2, 203.9, 38,190
   - CF-138: 59.0, 73.6, 10,680
   - CF-141: 1.9, 197.6, 31,190
   - CF-144: 4.0, 180.8, 29,770
   - CF-149: 3.0, 172.1, 29,550
   - CF-152: 34.3, 137.2, 17,280
   - CF-156: 1.3, 165.4, 23,500
   - CF-160: 3.7, 167.8, 27,570
   - CF-163: 1.8, 181.3, 31,600
   - CF-167: 0.8, 171.6, 24,980
   - CF-170: 2.2, 163.4, 26,510
   - CF-174: 3.2, 228.2, 43,070
   - CF-178: 3.4, 171.2, 25,840
3. A bar chart of every stand's share against the 15 per cent line on page 1, the three stands to mark in red.
