# task452 submission

## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (a lowland forest program's 2024-2025 activity data, the area of forest converted to other land, estimated from a stratified reference sample of points interpreted on high-resolution imagery and turned into the emission reductions a results-based payment agreement pays for).
**Analytical objective:** Data Extraction & Conformation (ETL) (the laboratory's main interpretation campaign, the ministry's quality-control re-interpretation on its own form and the adjudication of their differences conformed into one reference class per point on the national forest definition and the reporting period, with the final change map's classes, statistics and polygons joined across the 2019 and 2025 district layers).

## 1. Final Recommendation

**The Lowland Forest Emission Reductions Program can offer the Rainforest Results Facility 23,229,780 tonnes of emission reductions for 2024-2025, for which the Facility will pay USD 116,148,900.**

The tonnes rest on 122,900 hectares of deforestation, estimated from the reference sample on the strata it was drawn from, against the reference level's 179,900 for the two years. Not the final change map's error matrix with its own class areas as weights: the points drawn from the preliminary map's deforestation class that the final map moved into stable forest would each stand for a stable-forest point's area, which puts the deforestation within a few thousand hectares of the reference level and offers a seventh of the tonnes. Not the final map's own deforestation: it leaves out the clearings the map missed and would offer nearly twice the tonnes.

## 2. Critical Components

1. Each reference point stands for its sampling stratum's area over the points drawn there: **329, 2,469 and 4,785 hectares** for the preliminary map's deforestation, stable-forest and non-forest strata.
2. The area of deforestation in the accounting area over 2024-2025 is **122,900 hectares** (122,882.7 before rounding to the nearest hundred).
3. The emission reductions are **28,329,000 tonnes** of CO2e: reference level emissions of 89,410,300 tonnes less monitored emissions of 61,081,300.

## 3. Step-by-Step Solution

1. Applied the adjudicated fields of adjudication_log_2026-04.xlsx to reference_points_main_campaign_2026.csv and classed each point on the monitoring plan's section 3 (forest on 1 January 2024 and other land on 31 December 2025, canopy cover of 30 per cent or more, plantations excluded): 224 points are deforestation in 2024-2025.
2. Weighted each point by its stratum's area over the points drawn in it, from the strata of the preliminary change map of 15 January 2026 in section 2 of reference_sampling_design_2026-01.pdf: 329, 2,469 and 4,785 hectares.
3. Summed the weights of the deforestation points: 122,882.7 hectares, 122,900 to the nearest hundred (agreement article 4(2)); the stratified sampling variance gives a 90 per cent interval of 100,000 to 140,000 hectares to the nearest ten thousand.
4. Set monitored emissions of 122,900 hectares at 497.0 tonnes of CO2e a hectare, 61,081,300 tonnes, against reference level emissions of 89,950 hectares a year for two years at the same factor, 89,410,300 tonnes (articles 1, 2 and 4): emission reductions of 28,329,000 tonnes.
5. Set aside the 18 per cent buffer and dropped the fraction of a tonne: 23,229,780 tonnes offered, which the Facility pays for at USD 5.00 a tonne, USD 116,148,900 (articles 5 and 6).
6. Took each district's area as the part of the estimate its points contribute, as section 4 of monitoring_plan_extract.pdf sets the district figures, the points' 2019 district codes being the accounting area's layer.
7. Placed each polygon of final_change_map_v2_polygons.parquet in its 2019 district through district_concordance_2019_2025.csv, LT-05 and LT-06 both falling in La Esperanza and the highland districts SR-01 to SR-06 left out as outside the accounting area, and summed area_ha over patch_ha, each polygon's share of the patch it delivers, by the patch's size: 30,548 patches, 12,206 under 1 hectare and 3,221 of 5 hectares or more.
8. Recommendation: offer 23,229,780 tonnes for USD 116,148,900.

## 4. Deliverable Answers

### er_monitoring_report_2024-2025.pdf

1. Tonnes offered: 23,229,780.
2. Payment: USD 116,148,900.
3. Area of deforestation the tonnes rest on: 122,900 hectares; 90 per cent confidence interval 100,000 to 140,000 hectares.
4. Each district's area of deforestation, to the nearest hundred hectares:
   - Caoba Alta: 7,600
   - Caoba Baja: 23,500
   - Cerro Azul: 6,600
   - El Encanto: 8,900
   - La Esperanza: 12,700
   - Las Palmas: 18,100
   - Llano Grande: 10,500
   - Montealto: 3,300
   - Puerto Viejo: 4,600
   - Río Verde: 15,600
   - Tres Ríos: 6,400
   - Arroyo Hondo: 5,100
5. Horizontal bar chart on page 1: for each of the twelve districts, the area estimated from the reference sample beside the deforestation on the final change map of 22 April 2026, in thousand hectares, titled with the final map's share of the estimated area.
6. Deforestation patches on the final map by district, in all, under 1 hectare and of 5 hectares or more:
   - Caoba Alta: 1,806, 729, 205
   - Caoba Baja: 4,892, 1,982, 494
   - Cerro Azul: 996, 404, 99
   - El Encanto: 2,851, 1,118, 290
   - La Esperanza: 5,083, 1,972, 539
   - Las Palmas: 3,368, 1,365, 359
   - Llano Grande: 2,610, 1,069, 259
   - Montealto: 797, 333, 75
   - Puerto Viejo: 2,025, 803, 225
   - Río Verde: 3,932, 1,579, 431
   - Tres Ríos: 1,263, 500, 145
   - Arroyo Hondo: 925, 352, 100
   - Accounting area: 30,548, 12,206, 3,221

### reference_sample_conformed_2024-2025.xlsx

7. One row for each reference point with its 2024-2025 reference class (224 deforestation, 2,491 stable forest, 1,285 non-forest) and its class on the final change map (216 deforestation, 2,516 stable forest, 1,268 non-forest).
