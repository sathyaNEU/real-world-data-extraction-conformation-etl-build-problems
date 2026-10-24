## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Raise the summer level first in Bovenmade, Zuidergeer and Ravenbroek.**
Their peat lost 6.0, 5.5 and 5.1 tonnes of carbon per hectare per year between the 1997 and 2024 corings; Ruigeland, Wedderkamp and Goorsloot follow at 3.7. Not Ruigeland, Hazelweer and Wedderkamp, which the surveyed lowering at the 1997 topsoil's carbon density gives (15.0, 11.3 and 11.4) and which the cores lined up on the surveyed lowering also give (11.8, 11.5 and 9.3): their surfaces fell 53.5 to 64.8 cm after the 2009 to 2013 water-level cuts, mostly peat compressing, and at Hazelweer the base of the 1997 top metre now lies 40.7 cm lower, below the level the 1997 core reached, with its carbon still in it. Not Hellerwaard, Lindeschot and Kortewaard either, which equal total soil mass gives: oxidation removes most of the peat's own mass, so the equal mass reaches into deeper peat and hides most of every unit's loss.

## 2. Critical Components

1. The 1997 top metre is found again in each 2024 core as the depth holding the same cumulative ash per square metre: Bovenmade **68.5** cm, Zuidergeer **74.7** cm, Ravenbroek **77.1** cm, Hazelweer **76.0** cm, Ruigeland **67.6** cm (means of three points).
2. Surface lowering at the monitoring points, 1997 to 2024: Hazelweer **64.8** cm, Ruigeland **60.6** cm, Wedderkamp **53.5** cm against Bovenmade **34.9** cm.
3. Carbon loss of the first raise against the first unit below the line: Bovenmade **6.0**, Zuidergeer **5.5**, Ravenbroek **5.1**, Ruigeland **3.7** tonnes of carbon per hectare per year.

## 3. Step-by-Step Solution

1. Took the estimand from veenmonitoring_protocol_2024.pdf (5.1, 5.2): the carbon the peat of the 1997 core's top 1.00 m lost by the 2024 coring, over the days between the corings divided by 365.25, in tonnes of carbon per hectare per year, a unit the mean of its three points; the first raise takes the largest three (6.1).
2. Paired each 1997 core with its 2024 core through meetpunten_veenmonitoring.csv and read veenkernen_1997_bodemlab_wageveld.txt (5 cm slices, g/cm3, decimal commas) and lims_export_veenkernen_2024.csv (10 cm slices, kg/m3, semicolons).
3. For every slice: dry mass per square metre (bulk density times thickness), ash (dry mass times 1 less loss on ignition) and carbon (dry mass times total carbon).
4. Summed the 1997 core's ash and carbon over its top metre; found the depth in the 2024 core where the cumulative ash reaches the same mass, read linearly within the slice; the loss is the 1997 carbon less the 2024 carbon above that depth.
5. Converted to tonnes per hectare per year with each point's own interval, averaged the three points of each unit and ranked the twelve units.
6. For the surface lowering, took each grid point in waterpassing_raster_1997_2024.csv levelled in 1997 and surveyed in 2024 at the same position, the 1997 level less 0.054 m (hoogteonderzoek_lageveen_2024.pdf), over its own interval in years; points re-shot in 2024 at a meadow edge 14 m or more from their 1996 position were left out.
7. For the GLG, took the logger's 08:00 depth of the 14th and 28th (the hand reading where the logger had none) in peilbuizen_reeksen_2014_2026.csv, less the tube top's height above the surface at the time: the 2018 to 2022 renewals in peilbuizen_onderhoud.csv give each tube's earlier height; the three deepest levels of each hydrological year 2017/18 to 2024/25, averaged, two dipwells a unit.

## 4. Deliverable Answers

### peat_carbon_loss_1997_2024.xlsx

1. Carbon loss, tonnes of carbon per hectare per year (one decimal), and the first raise, every unit:
   - Bovenmade (PG-126): 6.0, first raise
   - Zuidergeer (PG-118): 5.5, first raise
   - Ravenbroek (PG-137): 5.1, first raise
   - Ruigeland (PG-107): 3.7, not in the first raise
   - Wedderkamp (PG-129): 3.7, not in the first raise
   - Goorsloot (PG-133): 3.7, not in the first raise
   - Hazelweer (PG-111): 3.3, not in the first raise
   - Oudelaak (PG-104): 3.1, not in the first raise
   - Hellerwaard (PG-140): 3.0, not in the first raise
   - Meerkoog (PG-144): 2.6, not in the first raise
   - Kortewaard (PG-115): 2.5, not in the first raise
   - Lindeschot (PG-122): 2.4, not in the first raise
2. Surface lowering since 1997, millimetres per year (one decimal):
   - Oudelaak: 6.6
   - Ruigeland: 22.5
   - Hazelweer: 24.2
   - Kortewaard: 4.1
   - Zuidergeer: 11.3
   - Lindeschot: 4.8
   - Bovenmade: 13.6
   - Wedderkamp: 19.4
   - Goorsloot: 7.6
   - Ravenbroek: 10.4
   - Hellerwaard: 4.8
   - Meerkoog: 6.2
3. Mean lowest groundwater level (GLG) 2017/18 to 2024/25, whole centimetres below the surface:
   - Oudelaak: 63
   - Ruigeland: 80
   - Hazelweer: 86
   - Kortewaard: 75
   - Zuidergeer: 79
   - Lindeschot: 73
   - Bovenmade: 93
   - Wedderkamp: 80
   - Goorsloot: 59
   - Ravenbroek: 81
   - Hellerwaard: 71
   - Meerkoog: 64

### peilbesluit_2027_first_raise.png

1. One bar chart of the twelve units' carbon losses, ranked, with the line under the third and Bovenmade, Zuidergeer and Ravenbroek highlighted above it.
