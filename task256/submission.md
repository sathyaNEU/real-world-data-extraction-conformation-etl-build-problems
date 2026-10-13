# task256 submission

## Tags

**Domain:** Human Factors & Ergonomics, anthropometric design fit (the share of a transit authority's bus operators each operator workstation configuration fits, from a reference survey of body dimensions carried to the operators through the stature and weight their DOT physicals record).
**Analytical objective:** Descriptive & Distribution Analysis (the share of the operators' joint body-dimension distribution that lies inside each configuration's fit envelope).

## 1. Final Recommendation

**Specify Configuration G (power-adjustable pedal set, extended-range seat riser, tilt-telescope steering column and deep-travel seat track, $4,450 per bus) for the 2027 order: it is the lowest-priced configuration that fits at least 95 per cent of our bus operators, 96.4 per cent of the 2,110 on the roster.**

E, the nearest cheaper configuration, fits 93.2 per cent and F 92.9. Not B, which fits 95.6 per cent of the survey's own workers at our sex mix but 82.3 per cent of our operators, who are heavier and more varied in stature than those workers. Not C, which counting each operator by their predicted dimensions puts at 95.2 per cent, nor E, which carrying the operators through stature alone puts at 95.1: each operator's weight and the spread of the five dimensions around the prediction both move the share.

## 2. Critical Components

1. The bus operators counted: **2,110** on the 30 September 2026 roster (**1,522** men and **588** women), each at the stature and weight of the latest DOT physical.
2. Configuration G fits **96.4** per cent of them.
3. The nearest cheaper configuration, E, fits **93.2** per cent; F, the next price down from G, **92.9** per cent.

## 3. Step-by-Step Solution

1. Counted the employees in the Bus Operator classification on hr_roster_transportation_maintenance_2026-09-30.xlsx, full-time and part-time and every duty status, the population tvrta_standard_ES-12_operator_workstation.pdf names: 2,110 (1,522 men, 588 women).
2. Took each operator's stature and weight from the latest DOT physical in ostrander_encounters_tvrta_2014-01_2021-06.csv or fernhill_visits_tvrta_2021-01_2026-09.csv, employee numbers matched across the formats, in millimetres (inches times 25.4) and kilograms (pounds times 0.45359237).
3. Took each sex's means, standard deviations and correlations of stature, weight and the five fit dimensions from brennard_working_adults_body_dimensions_2012_summary_tables.pdf, a joint normal within each sex as the report's percentiles are.
4. For each operator, took the normal distribution of the five fit dimensions given that operator's stature and weight within the operator's sex, and its probability of lying entirely within each envelope in halvard_fit_report_2027_order_operator_workstation.pdf; the average over the 2,110 operators is each configuration's accommodation: G 96.4 per cent.
5. Applied the standard's rule, the lowest-priced configuration at 95 per cent or more: G; A to F fall short (E 93.2, F 92.9).
6. Costed each option's maintenance from operator_area_work_orders_2019-01_2026-09.csv (parts on every line and each work order's labor once, orders billed to TVRTA and closed in 2021 to 2025 on the option's component) over its bus-years from fleet_roster_2026-09-30.csv, bus_disposals_2019-2026.csv and retrofit_campaigns_2019-2026.csv by the bus-month rule in exports_readme_fleet_maintenance.md.
7. Put each configuration's twelve-year cost per bus at its price plus twelve times the cost per bus-year of each option it carries.
8. Recommended Configuration G.

## 4. Deliverable Answers

### workstation_configurations_2027.xlsx

1. Recommended configuration: G, $4,450 per bus, fitting 96.4 per cent of the bus operators.
2. Each configuration's price per bus, the share of the bus operators it fits (per cent, one decimal) and whether it reaches 95 per cent:
   - A: $0, 79.4, no
   - B: $1,850, 82.3, no
   - C: $2,350, 90.1, no
   - D: $2,700, 82.6, no
   - E: $3,300, 93.2, no
   - F: $3,900, 92.9, no
   - G: $4,450, 96.4, yes
   - H: $5,900, 97.2, yes
3. Each option's maintenance on the 2021 to 2025 work orders (total to the dollar, bus-years fitted to one decimal, cost per bus-year to the dollar):
   - Power-adjustable pedal set: $368,370, 1,374.5 bus-years, $268
   - Extended-range seat riser: $111,523, 838.5 bus-years, $133
   - Tilt-telescope steering column: $74,873, 445.7 bus-years, $168
   - Deep-travel seat track: $5,692, 80.2 bus-years, $71
   - Raised header and visor: $2,793, 103.4 bus-years, $27
4. Each configuration's twelve-year cost per bus:
   - A: $0
   - B: $6,662
   - C: $4,366
   - D: $7,836
   - E: $6,168
   - F: $10,728
   - G: $12,130
   - H: $13,904

### operator_accommodation_2027.svg

1. Dot chart of each configuration's share of the bus operators it fits beside its price per bus, each labelled to one decimal, the 95 per cent line drawn and Configuration G marked as recommended.
