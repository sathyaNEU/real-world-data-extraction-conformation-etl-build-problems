# task253: 2027 Reading Partnership places

## Tags

**Domain:** Education & Learning Sciences (student growth and value-added modelling: school-effects estimation from NAPLAN results).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Commission 42 places for the 2027 Reading Partnership.**

The 264 primary schools' chances of an underlying Year 5 reading average below 480, added up under the LT-AS-04 model, come to 41.95. Not the 28 schools whose model average is below 480: those averages are pulled toward the system mean, so they are less spread than the underlying averages and count too few schools in the tail. Not the 56 schools whose 2024 to 2026 average is below 480: three sittings of small year groups carry noise that counts too many.

## 2. Critical Components

1. The LT-AS-04 model fitted by REML to the 30,956 participating Year 5 reading results: mean **496.5**, school SD **16.5**, year-group SD **9.3**, student SD **69.9**
2. The sum over the 264 primary schools of each school's chance of an underlying average below 480 is **41.95**

## 3. Step-by-Step Solution

1. Kept participating Year 5 reading results from naplan2024_legacy_extract.csv, the Year 5 sheet of NAPLAN2025_results_portal.xlsx (below its title block) and naplan_results_2026.csv, joined to the 264 primary schools in school_register_2026.xlsx: 30,956 results.
2. Fitted LT-AS-04 3.1 and 3.2 (fixed mean, school and year-group random effects, student residual, REML): mean 496.5, school SD 16.5, year-group SD 9.3, student SD 69.9.
3. Took each school's underlying average as normal given its three year-group means at the fitted values (LT-AS-04 3.4) and added the 264 chances of lying below 480: 41.95, so 42 places.
4. Divided each region's sum of chances by 41.95 for its share of the places.
5. Padded the census school numbers to four characters and took 2027 Years 3 to 6 as the August 2026 census Years 2 to 5, weighted by each school's chance: 7,072 students.
6. Assigned hubs from hub_visit_plan_2027.xlsx, matched to the register on school name and locality, and weighted twice each one-way distance in hub_school_road_distances.csv by the school's chance (guidelines 4): 8,327 km a fortnight.
7. Recommendation: commission 42 places.

## 4. Deliverable Answers

### reading_partnership_2027.xlsx

1. Places to commission: 42
2. Share of the places by region, per cent to one decimal:
   - Metropolitan North: 15.5
   - Metropolitan South: 25.6
   - Northern: 12.2
   - Western: 16.7
   - Southern: 14.1
   - Coastal: 15.9
3. Year 3 to 6 students the places will serve in 2027, by region:
   - Metropolitan North: 1,578
   - Metropolitan South: 3,530
   - Northern: 356
   - Western: 768
   - Southern: 431
   - Coastal: 409
   - All regions: 7,072
4. Each hub's students served in 2027 and road km of one fortnightly round of visits:
   - Brinrigg: 3,068 students, 813 km
   - Carnbrae: 2,243 students, 1,957 km
   - Kirkanby: 725 students, 1,826 km
   - Tullgate: 671 students, 1,593 km
   - Haskwick South: 365 students, 2,138 km
   - All hubs: 7,072 students, 8,327 km

### reading_partnership_2027_hubs.png

1. One bar per hub of its fortnightly road km, longest first: Haskwick South 2,138, Carnbrae 1,957, Kirkanby 1,826, Tullgate 1,593, Brinrigg 813, each bar labelled with its km and students.
2. The title names Haskwick South as the hub with the longest fortnightly round.
