# task182 design note (architecture 1)

Seed AD05 (a prescriber's high-dose patient count from overlapping fills), objective Anomaly Detection & Diagnostics,
re-rooted at the draw. The seed's reviewer-determination corpus pins its construction by replaying settled figures,
which the client's 10/10 standard caps. Its world (a state programme-integrity unit referring a prescriber to a
medical board) repeats task180's role, forum and organisation family. The objective and the number are kept. A first
redraw (left-censored laboratory arsenic across a reporting-limit change) was dropped at the guard: it repeated
task134's gap, G-code and Gate G, and it would have made a third censoring stump in a row after task134 and task181.

## DRAW

```
Card filed with guard.py register before the ladder was written? yes (PASS)
Shape: 11 before and after with a control (each bore's level before and after the pit's dewatering, against the level
  the bore would be at without it)
Gate G mechanism: decomposition_attribution (each bore's change split between the dry seasons and the mine's take)
Gap: objective (the decline since the baseline is correct and is not what MG-02 scores)
Pattern: none (own); generator G16 (the method that builds each bore's level without the mine)
Domain: physical-environmental-sciences / environmental-monitoring-exceedance   Objective: anomaly-detection
Pairing repeated from a recent build? no (physical-environmental sciences x anomaly detection never built)
Stakeholder role: principal hydrogeologist at the mine (role family other), for the mine's executive team
Context artifact: register (the landholder bore register: aquifer, trigger, measuring point history, baseline)
Calibration form: other (reference bores outside the predicted drawdown show the climate-only model holds after July 2022)
Decision type: designation_set   Answer unit: set_of_items   Opening move: question-first
Stump strategy: decomposition_attribution   Decisive rule filed? yes (MG-02 4.1 files the test: the decline the mine's
  take has caused, at the September 2026 level, against the aquifer's trigger; nothing files how that decline is
  estimated)
Official decoy filed? no (no filed sentence defines the decline as the baseline minus the current level)
Validated decoy? no   stump_class: analytical
Forum: executive_team (the mine's executive team approves make-good offers on Monday 26 October 2026)
Forcing event: incident_or_complaint (four landholders complained in August and September 2026)
Org family: other (a coal mining company)
Layer 2: estimand_identification, own:counterfactual-groundwater-level-from-calibrated-climate-response
People (guard.py names, en_AU, seed 182): Rebecca Quinn (principal hydrogeologist, the requester), Stephen Anderson
  (general manager, chairs the executive team), Erika Martin (environment superintendent, wrote the network notes),
  Noah Carrillo (field technician who reads the bores), Ernest Walker and Clarence Lewis (landholders who complained)
```

**Data-native sentence.** A bore in the creek alluvium rises within weeks of a good wet season and falls through every
dry one, while a bore in the coal measures answers rain that soaked in at the outcrop years before, so in 2026 the coal
measures were still climbing on the 2019 to 2021 wet seasons when the pit's dewatering pulled them back down, and the
alluvium had been falling for three dry seasons whether the pit was there or not.

**Layer 1 (realistic mess and the systems that produce it).** A mine's groundwater monitoring network as the
environment team holds it:
- Manual dips recorded as depth to water below a measuring point. Two bores' headworks were rebuilt and their measuring
  points resurveyed, so a reduced level needs the measuring point in force on the reading date.
- Landholder dips sometimes taken with the stock pump running. The field form's "pump on" box reaches the export only as
  free-text remarks in several spellings, and a pumped level is not a static level.
- The 2012 to 2014 environmental-impact baseline was read by a consultant in feet.
- Unvented pressure loggers record absolute pressure. The site barometric logger has to be subtracted, the timestamps
  are UTC, and the day that counts is Queensland's (AEST, no daylight saving).
- Each logger is checked against a manual dip at download.
- A bore goes by its state registered number in one file, the company's monitoring code in another and the landholder's
  own name for it ("house bore", "yards bore") in the complaints.
- Some dips were keyed twice from the field sheets.

**Layer 2 (the analytical shortcut).** The shortcut is reading a bore's decline since its baseline assessment (or since
July 2022, or against the reference bores) as the mine's drawdown.
- What the data hold: the alluvial bores fell 2.5 to 4.5 m through the dry seasons on rainfall alone, and the
  coal-measure bores near the pit show 1.5 to 3.5 m of decline that hides 6 to 9 m of drawdown, because the wet seasons
  had started them on a rise.
- A careful analyst who sees the drought subtracts the reference bores' change, but every reference bore is in the
  alluvium or the basalt. Another fits one rainfall window to every bore.
- The expert fits each bore's own response to rainfall and evaporation on its record before July 2022. Run forward, that
  model is the level without the mine, and the drawdown is the gap between it and the September 2026 level.

**Similarity claim.** No build on file attributes a monitored level change between a shared climate driver and a
pumping stress through per-unit response functions. Nearest drivers on file (0.06): task115, task69 (lineage),
task51 (lineage).
- task51's cumulative decomposition is against a fixed reference year.
- task180 (architecture 3) is also a within-unit design, but its decisive step is a comparison against confounding by
  indication in registry data, not a fitted response to a driver that every unit shares.
- task135 (the same domain one draw back) is a sediment rating curve's retransformation bias in a forecast.

## THREE RULES (client, 2026-10-10)

- **Rule 1, the domain is used.** What decides the call is attributing groundwater-level change between climate-driven
  recharge and pumping. Hydrogeologists do this with response functions calibrated on each bore's pre-impact record (the
  shallow and deep units answer rain on very different time scales). Swap test: with another field's nouns there is no
  recharge, no aquifer memory that differs between shallow and deep bores and no drawdown cone, so the task does not
  survive the swap.
- **Rule 2, two layers.** Layer 1 is above: measuring points, pumped dips, feet, logger compensation, UTC, identities,
  duplicates. Layer 2 is each bore's own level without the mine.
- **Rule 3, the decisive step is analytical.** Class `analytical`.
  - Analyst test: a strong analyst turns every reading into a reduced level, drops pumped and duplicate dips,
    compensates the loggers for air pressure and applies each aquifer's trigger exactly. They still measure each bore's
    decline from its baseline (or against the reference bores) and designate the alluvial bores and the basalt bore.
  - Only a model of each bore's own response to rainfall and evaporation, calibrated before dewatering and run forward,
    shows which bores the mine has drawn down past their trigger.
  - Rule application (the triggers, static levels, the assessment month) and data semantics (measuring points, feet,
    compensation, UTC) sit on lower rungs and in the asks.

## GATE G

- **Litmus.** Nothing reported is overturned. Every reading is correct, every rainfall figure is right, the complaints
  are genuine (the bores did fall) and MG-02's triggers are the triggers. The difficulty is what lowered each bore.
- **Primary mechanism:** decomposition_attribution (each bore's change split between the seasons' effect and the
  mine's), with method selection (G16) carrying it.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Deletion test.** Delete the contact log and the network notes. The baseline comparison still names the alluvial
  bores and the basalt bore, and the per-bore model still names the coal-measure bores.
- **Clean-data and instrument test.** No file is incomplete or stale. A perfect instrument would still record the sum of
  the seasons' effect and the mine's. Nothing is repaired.
- **Lens swap.** Not one population under two lenses. The answer's quantity is the gap between each bore's September
  2026 level and its own modelled level without the mine, built from the climate record and the bore's pre-dewatering
  history. The naive quantity is the change from a reference level.

## STUMP SENTENCE

A competent solver converts every dip and logger reading to a reduced level and compares each bore's September 2026
level with its baseline assessment (or with the reference bores' change). It offers make good to the alluvial bores
that fell more than 2 m and the basalt bore that fell more than 5 m (or, net of the reference bores, to KV-LB12 alone).
The step that lands it there is reading the decline since the baseline as the mine's. In fact the alluvium and the
basalt fell through the dry seasons on rainfall alone. The coal-measure bores near the pit were still rising on the
2019 to 2021 wet seasons, and the mine drew them 8 to 9 m below where that rise was taking them while they show less
than 2.5 m of decline (shipped: 8.2 to 9.3 m drawn down, 2.21 to 2.49 m fallen).

## ENTITY AND UNIT OF VALUE

One landholder bore. MG-02 4.1's test: the decline in the bore's water level that the mine's take of associated water
has caused, at its September 2026 assessment level, against the trigger for its aquifer (2 m unconsolidated, 5 m
consolidated). An offer is an agreement with the bore's owner (deepen, replace or supply water).

## THE WORLD (as built; every figure is the generator's, and the ones the pack carries are asserted in `checks.py`)

**The mine.** Kelvale Mine, an open-cut coal mine of Tarrabool Resources in the northern Bowen Basin (Isaac region,
central Queensland). Pit dewatering began on 4 July 2022 (pit sump PS1; PS2 from 16 January 2023); the advance
dewatering bores AD01 to AD04 came on in March 2023 (AD03 and AD04 on temporary pumps until 14 August 2023 and 12 February
2024). The metered take averaged 1.86 ML a day
in July 2022, 5.62 in June 2023, 9.12 in June 2024, 10.49 in June 2025 and 12.60 in September 2026 (12.9 GL in all).

**Hydrogeology.** The Mundoora Creek alluvium (unconsolidated, trigger 2 m), the Tertiary basalt on the ridges and the
Permian coal measures (both consolidated, trigger 5 m). The coal measures subcrop beneath the alluvium at the pit's
eastern end, where the alluvial bore KV-LB12 (A1) is drawn down by leakage.

**Climate (shipped daily, 1 January 1990 to 30 September 2026; simulated from 1965, seeded).** Mean annual rainfall
579 mm over water years 1991 to 2022 (summer-dominant: December to March carries more than 2.2 times June to
September), Morton areal potential evapotranspiration 1,753 mm. Water-year rainfall (October to September): 2010 638,
2011 696, 2012 552, 2013 492, 2014 475, 2015 499, 2016 593, 2017 637, 2018 498, 2019 487, 2020 843, 2021 956, 2022 551,
2023 336, 2024 325, 2025 318, 2026 348 mm. So: wet 2010 to 2011, dry 2013 to 2015, average 2016 to 2017, dry 2018 to
2019, wet 2019-20 and 2020-21 seasons, an average 2021-22 season, failed seasons from 2022-23 to 2024-25 and a dry
2025-26 (each failed year asserted under 0.7 of the mean, each wet one over 1.3).

**Bore response (the simulation, never shipped).** Level = constant + gain x (gamma response to rainfall less f x
evaporation) - gain x (Hantush-type response to the metered take, leaky well function W(u, r/B) with a time scale and
leakage per bore) + AR(1) noise (sigma 0.05 to 0.09 m, daily autocorrelation 0.98 to 0.995). Each gain is set from a
target climate decline or rise between the bore's baseline date and September 2026, and from a target drawdown at
September 2026. Response times: alluvium 140 to 200 days (shapes 1.5 to 2), basalt 300 to 650 days (shapes 1 to 2), coal
measures 6.2 to 6.8 years (shape 16: little response in the first two years, the most at five to seven), which is what
keeps the coal measures' 2019 to 2021 rise running through 2026 while the drought is still on its way down to them.
Every bore's water table stays at least 1.5 m below ground and above the bore's bottom, and every logger stays
submerged (asserted).

**The 18 register bores as built.** Labels are the build's own; codes are shipped.

| Bore | Unit | Change, baseline to Sep 2026 (m) | True drawdown (m) | Shipped estimate (m) | Call |
|---|---|---|---|---|---|
| CM1 KV-LB04, CM2 KV-LB07, CM3 KV-LB05, CM4 KV-LB10 (3.4 to 5.7 km) | coal measures | -2.44, -2.46, -2.49, -2.21 | 8.73, 8.33, 9.37, 8.11 | 8.9, 8.4, 9.3, 8.2 | impaired |
| CM5 KV-LB16 (11 km) | coal measures | +1.74 | 2.28 | 2.4 | not impaired |
| A1 KV-LB12 (over the subcrop) | alluvium | -8.78 | 4.50 | 4.6 | impaired |
| A2 to A7 KV-LB01, 02, 03, 06, 08, 09 | alluvium | -4.63, -5.23, -4.64, -4.84, -4.81, -4.69 | 0.43 to 0.82 | 0.8, 0.7, 0.5, 0.6, 0.4, 0.3 | not impaired |
| A8, A9 KV-LB13, 14 (on the Coolibah Springs waterholes) | alluvium | -0.98, -0.87 | 0.15, 0.12 | 0.2, 0.1 | not impaired |
| B1 to B3 KV-LB11, 15, 17 | basalt | -2.59, -3.02, -2.68 | 1.16, 1.65, 1.00 | 1.1, 1.6, 0.9 | not impaired |
| B4 KV-LB18 (ridge bore) | basalt | -8.70 | 1.48 | 1.3 | not impaired |

**The other network bores.** Three state reference bores 20 to 30 km from the pit: KV-RF01 and KV-RF02 in the alluvium
(fell 4.84 and 5.02 m from their April to June 2022 mean to September 2026) and KV-RF03 in the basalt (5.16 m); none
in the coal measures. Six mine monitoring bores on the pit perimeter: two in the alluvium and four in the coal
measures, which fell 36.0, 29.4, 24.7 and 21.4 m (KV-MB03 to KV-MB06).

**Monitoring history.** EIS rounds quarterly from March 2012 to June 2014 (the consultant, feet, registered numbers);
monthly runs from July 2014 (codes, with the field team's variants); fortnightly at the landholder bores from 10 August
2026, so each has three September 2026 visits; baseline assessments on each landholder bore's date in April to June 2022
(coal measures in April, basalt in May, alluvium in June); hourly loggers from May 2015 at KV-LB04, KV-LB05, KV-LB12,
KV-LB02, KV-LB15, KV-LB18, KV-RF01, KV-RF03, KV-MB01 and KV-MB03 (two replaced; one 17-day gap at KV-LB15; the mine's two
loggers drift, step at re-hangs and have two outages each, outside what the evidence reads), downloaded quarterly
with a check dip and finally on 1 to 6 October 2026; the site barometric logger (one 9-hour gap in 2018).

## LADDER (shipped; each rung's set asserted by name in `generator/checks.py`, every bore at least 25 per cent of its trigger away from it at every rung)

Each figure is the rung's quantity in metres (a positive figure is a fall attributed to the mine on that reading).
Triggers: 2 m for the alluvium (A), 5 m for the basalt (B) and coal measures (CM).

| Rung | CM1 | CM2 | CM3 | CM4 | CM5 | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 | A9 | B1 | B2 | B3 | B4 | Set | Thinnest |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 complaints | | | | | | | x | x | | x | | | | | | | | x | A2, A3, A5, B4 | |
| 1 baseline | 2.44 | 2.46 | 2.49 | 2.21 | -1.74 | 8.78 | 4.63 | 5.23 | 4.64 | 4.84 | 4.81 | 4.69 | 0.98 | 0.87 | 2.59 | 3.02 | 2.68 | 8.70 | A1 to A7, B4 | 0.40 (B2) |
| 1b June 2022 | 2.53 | 2.56 | 2.59 | 2.25 | -1.70 | 8.55 | 4.77 | 5.25 | 4.79 | 5.09 | 5.07 | 4.69 | 1.07 | 0.93 | 2.52 | 3.04 | 2.66 | 7.99 | A1 to A7, B4 | 0.39 (B2) |
| 1b 2012-22 mean | 3.00 | 2.77 | 3.31 | 2.64 | -1.34 | 8.17 | 4.55 | 5.05 | 4.12 | 5.14 | 4.39 | 4.67 | 1.31 | 1.29 | 2.02 | 2.39 | 1.93 | 6.99 | A1 to A7, B4 | 0.34 (CM3) |
| 2 pooled refs | -2.57 | -2.55 | -2.52 | -2.80 | -6.75 | 3.77 | -0.38 | 0.22 | -0.37 | -0.17 | -0.20 | -0.32 | -4.03 | -4.14 | -2.42 | -1.99 | -2.33 | 3.69 | A1 | 0.26 (B4) |
| 2 matched refs | -2.72 | -2.70 | -2.67 | -2.95 | -6.91 | 3.85 | -0.30 | 0.30 | -0.29 | -0.09 | -0.12 | -0.25 | -3.95 | -4.06 | -2.57 | -2.14 | -2.49 | 3.54 | A1 | 0.29 (B4) |
| 2b trend 2017-22 | -1.03 | -0.34 | -1.81 | -1.06 | -4.21 | 15.50 | 11.64 | 13.49 | 11.22 | 13.90 | 11.96 | 12.06 | 3.35 | 3.25 | 3.51 | 3.64 | 3.36 | 15.60 | A1 to A9, B4 | 0.27 (B2) |
| 2b trend 2012-22 | 1.16 | 0.89 | 1.56 | 0.87 | -2.50 | 12.87 | 9.13 | 10.42 | 8.42 | 10.74 | 9.11 | 9.43 | 2.74 | 2.62 | 2.88 | 3.10 | 2.68 | 12.39 | A1 to A9, B4 | 0.31 (A9) |
| 3 one window, 12 months | 2.99 | 2.77 | 3.30 | 2.64 | -1.34 | 4.31 | 0.83 | 0.56 | 0.59 | 0.69 | 0.59 | 0.72 | 0.08 | 0.13 | 1.38 | 1.95 | 1.43 | 2.74 | A1 | 0.34 (CM3) |
| 3 one window, 3 years | 2.99 | 2.77 | 3.30 | 2.64 | -1.34 | 2.80 | -0.83 | -1.04 | -1.17 | -1.31 | -1.28 | -1.07 | -0.39 | -0.27 | 0.81 | 1.45 | 0.83 | 0.54 | A1 | 0.34 (CM3) |
| **4 own response (answer)** | **8.90** | **8.41** | **9.30** | **8.19** | 2.40 | **4.60** | 0.80 | 0.70 | 0.50 | 0.60 | 0.40 | 0.30 | 0.21 | 0.10 | 1.10 | 1.60 | 0.90 | 1.30 | **CM1 to CM4, A1** | see GRID |

"Thinnest" is the smallest distance from a trigger over the 18 bores, as a fraction of that trigger (0.25 is the floor).

- **Rung 0**, the complaints: KV-LB01, KV-LB02, KV-LB06, KV-LB18. Killed by MG-02 4.1 (a complaint is not the test); no
  complainant's bore is in the answer.
- **Rung 1 and 1b**, the decline from the baseline assessment (or from the June 2022 level, or from the mean of the
  monthly levels March 2012 to June 2022): A1 to A7 and B4. A strong analyst who cleans every reading stops here. Killed
  by the reference bores and the climate record: every alluvial reference fell about 5 m with no mine near it, and the
  coal measures were rising before July 2022 (0.65 to 0.72 m a year since 2021, asserted).
- **Rung 2**, the decline less the reference bores' change (April to June 2022 mean to September 2026: 4.84, 5.02 and
  5.16 m), pooled (5.01) or matched by unit (alluvium 4.93, the basalt reference for the basalt and the coal measures
  5.16): A1 alone. Killed by the register's network sheet: no reference bore is in the coal measures, whose path was a
  rise.
- **Rung 2b**, the pre-July 2022 straight line extrapolated to 15 September 2026 (monthly levels from January 2017 or
  from the first reading): A1 to A9 and B4. Killed by the climate file: the 2019 to 2021 rise in the alluvium was two wet
  seasons, not a trend; the coal-measure lines run flat because their pre-2022 path fell then rose.
- **Rung 3**, one summed rainfall-departure window for every bore (12 months or 3 years, no lag, calibrated on monthly
  levels to June 2022; a fitted slope below zero is read as no response and the bore's pre-July 2022 mean taken): A1
  alone, coal measures 2.64 to 3.30 m. Killed by the coal measures' own records: their levels move with the rain of four
  to eight years before, which no single short window sees.
- **Rung 4**, the answer: each bore's own gamma response to daily rainfall less f x Morton areal evaporation, fitted on its
  readings from the first reading to 3 July 2022 (logger daily means where the bore has a logger), run forward; the
  drawdown is the fitted level for September 2026 (mean of its days) less the assessment level. CM1 to CM4 and A1.

**Margins (shipped, asserted).** Every bore is at least 25 per cent of its trigger away from it at every rung (thinnest
0.26 of the trigger, B4 at rung 2 pooled) and in every answer cell (thinnest 0.306, CM4 6.53 m in the rainfall-departure
family). Rung 1 as targeted: A2 to A7 fell 4.63 to 5.23 m (at least 2.5), B4 8.70 (at least 6.25), CM1 to CM4 2.21 to 2.49
(at most 3.75, and inside 1.5 to 3.5). Five distinct sets on the ladder (rungs 2 and 3 share A1 alone, asserted).

**Evidence the pack carries (asserted).**
- The coal-measure bores were rising before 4 July 2022: 0.72 (CM1), 0.70 (CM2), 0.66 (CM3) and 0.65 m a year (CM4),
  least-squares slope of monthly levels January 2021 to June 2022 (target 0.5 to 1).
- The per-bore model fitted before 4 July 2022 tracks the three reference bores to September 2026: largest monthly
  residual 0.29 (KV-RF01), 0.24 (KV-RF02) and 0.14 m (KV-RF03) (target 0.5).
- The mine's coal-measure bores show the cone: they fell 36.0, 29.4, 24.7 and 21.4 m from April to June 2022 to
  September 2026 (target 20 to 40).
- The full-record model with the take as a second stress gives the same set in all eight of its cells.
- The world: the coal measures' climate path is still higher in September 2026 than in March 2026 at CM1 to CM4, and the
  golden's estimate is within 0.5 m of the true drawdown at each (asserted against the simulation).

## GRID (shipped, asserted cell by cell)

Five families, each numpy-only in `generator/models.py` (shared by `golden.py`; `verify.py` writes its own):
- **gamma**: shapes 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 20 x 40 mean response times from 20 days to 12 years (geometric) x
  evaporation factor 0 to 1 in steps of 0.025, gain and constant by least squares (gain positive);
- **exp**: an exponential response with a fitted delay (delays 0 to 6 years, 11 values, x 30 time constants);
- **crd**: summed rainfall departure over each bore's own window, 1 to 10 years, lagged 0 to 6 years in six-month
  steps, chosen by fit (slope positive);
- **ma**: regression on the 1, 3, 5 and 8-year moving averages of rainfall;
- **full**: the full record to September 2026 with the take as a second stress (gamma climate response x 45 gamma take
  responses x 21 evaporation factors); its take term at September 2026 is the drawdown.

Calibration from the first reading or from May 2015, to 3 July 2022 (the full record runs to 30 September 2026); daily
or monthly steps; manual dips only, or logger daily means where there are loggers. 5 x 2 x 2 x 2 = **40 cells, 0
misses**, each giving CM1 to CM4 and A1 with every bore 25 per cent clear. Thinnest margin per family (fraction of the
trigger): gamma 0.463 (A3 1.07 m, may2015/monthly/logger), exp 0.453 (CM5 2.73, may2015/daily/dips), crd 0.306 (CM4
6.53, may2015/monthly/dips), ma 0.419 (CM2 7.09, may2015/daily/dips), full 0.431 (A3 1.14, may2015/monthly/logger).

**Variants that keep every winner** (each re-run over all 40 cells; 120 cells, 0 misses):
- the assessment level as the last static September reading: thinnest crd 0.326, exp 0.448, full 0.431, gamma 0.372, ma 0.433;
- pumped dips removed by the robust outlier rule (more than 1.2 m below the median of up to two readings either side
  within 50 days) instead of by remark: crd 0.306, exp 0.597, full 0.431, gamma 0.453, ma 0.419;
- the 2012 to 2014 feet record dropped: crd 0.306, exp 0.453, full 0.431, gamma 0.463, ma 0.419.

The naive cells (rungs 1, 1b, 2, 2b, 3 in each of their variants) are the ladder rows above.

**Drawdown bands (min to max over the 40 cells, m):** CM1 6.9 to 9.3; CM2 7.1 to 9.1; CM3 7.6 to 10.5; CM4 6.5 to
9.0; CM5 1.2 to 2.7; A1 3.2 to 4.9; A2 -0.3 to 0.8; A3 -0.6 to 1.1; A4 -0.6 to 0.8; A5 -0.8 to 0.7; A6 -0.8 to 0.7;
A7 -0.5 to 0.7; A8 -0.2 to 0.2; A9 -0.1 to 0.2; B1 1.0 to 1.1; B2 1.4 to 1.7; B3 0.8 to 1.1; B4 0.7 to 2.7. Every
golden value sits inside its band and every bore's rung 1 decline sits outside it (asserted).

**Mess neutrality of the main call (primary cell re-run under each Layer 1 misstep).** Unchanged under: the measuring
point history ignored, duplicate dips kept, pumped dips kept, the 2012 to 2014 rounds dropped (registered numbers not
mapped), UTC days for the loggers, loggers left uncompensated (all six asserted; pumped dips kept, UTC days and
uncompensated loggers are also ask stops, which move the September levels and leave the call where it is). Recorded,
not asserted: the feet record read as metres moves the call to 16 bores (the 2012 to 2014 levels drop by about 40 m,
a step no analyst would keep).

## CLOSURE (the 22 axes, as shipped)

1 Population: the 18 landholder bores in the register (MG-02 1.2); the reference and mine bores are on a separate sheet
outside MG-02. 2 Unit: one bore. 3 Window: the September 2026 assessment level (MG-02 2.4, 4.2); the take from 4 July
2022. 4 As-of: water levels to 30 September 2026, loggers downloaded 1 to 6 October, the extract delivered Friday 9
October 2026, the request Tuesday 13 October, the executive team Monday 26 October 2026; no date after 13 October 2026
in any shipped file (asserted). 5 Version basis: one row per entry; a dip keyed twice (identical but for the entry
number) is one reading (C1: the call is unchanged with duplicates kept). 6 Divisor: none. 7 Weighting: a logged bore's
September level is the mean of its 30 Queensland-day means; a manual bore's is the mean of its September static dips
(three, or two where one was pumped). 8 Window length: one calendar month. 9 Boundary: every bore at least 25 per cent
of its trigger from it at every rung and in all 160 answer cells (thinnest 0.26 and 0.306). 10 Rounding: levels and
changes to the centimetre, the mine's share to 0.1 m, the call on unrounded values; every graded figure at least 0.15 of
its last printed unit from a rounding edge (levels and changes min 0.17, drawdowns min 0.44), no ties within a column
(asserted). 11 Tie-break: none needed. 12 Maturity: September is complete (30 logger days per logged bore, three
fortnightly runs). 13 Order: identity, units, measuring point in force, static readings, compensation and Queensland
days, the September level, the attribution, the trigger. 14 Row order: irrelevant. 15 Duplicates: identical double
entries, none in September 2026. 16 Identity: codes, code variants and registered numbers through the register (every
site maps; C1: dropping the registered-number rows leaves the call unchanged). 17 Netting: none. 18 Units: metres, feet
for the EIS rounds (0.3048); kPa to metres at 9.80665 (the notes; 9.81 moves no printed level, asserted). 19 Code
semantics: aquifer class from the register (alluvium unconsolidated, basalt and coal measures consolidated). 20
Integerisation: none. 21 Scope: water level only (yield and quality are not the test; the quality file is unused). 22
Forward window: none (MG-02 4.1 tests the September 2026 level).

Method axis (C4 grid separation): the five families, two calibration starts, two steps, two data sources and three
variants (160 cells) all give the same five bores 25 per cent clear. The two forms ruled out by the data: a plain
exponential (no delay) finds no positive response to rainfall at any time constant for any of the five coal-measure
bores, whose levels fall after wet years at short lags, so it has no fit (forced, it reads like rung 3: A1 alone, the
coal measures 2.8 to 3.7 m); the delayed exponential fits them to 0.66 to 0.74 m and the gamma to 0.09 to 0.29 m before
July 2022. A single short window with no lag is rung 3 itself.

## ASK SHEET (shipped)

| Ask | Figures | Shipped answer |
|---|---|---|
| The offers and their count (note; MG-02 6.1) | 1 set + 1 | Yarrowmere Pastoral Co Pty Ltd (KV-LB04, KV-LB05), Tondara Grazing Pty Ltd (KV-LB07), Bluebush Downs Pty Ltd (KV-LB10), Cypress Ridge Pastoral Trust (KV-LB12): four offers |
| September 2026 level, m AHD, two decimals (workbook) | 18 | LB01 209.51, LB02 205.24, LB03 204.86, LB04 207.77, LB05 214.47, LB06 209.61, LB07 195.44, LB08 201.27, LB09 199.16, LB10 203.49, LB11 238.12, LB12 209.50, LB13 202.33, LB14 201.88, LB15 241.33, LB16 209.84, LB17 243.13, LB18 245.75 |
| Change since the baseline assessment, m, two decimals | 18 | LB01 -4.63, LB02 -5.23, LB03 -4.64, LB04 -2.44, LB05 -2.49, LB06 -4.84, LB07 -2.46, LB08 -4.81, LB09 -4.69, LB10 -2.21, LB11 -2.59, LB12 -8.78, LB13 -0.98, LB14 -0.87, LB15 -3.02, LB16 +1.74, LB17 -2.68, LB18 -8.70 |
| The decline the mine caused, m, one decimal (graded on the band) | 18 | LB01 0.8, LB02 0.7, LB03 0.5, LB04 8.9, LB05 9.3, LB06 0.6, LB07 8.4, LB08 0.4, LB09 0.3, LB10 8.2, LB11 1.1, LB12 4.6, LB13 0.2, LB14 0.1, LB15 1.6, LB16 2.4, LB17 0.9, LB18 1.3 (bands in GRID) |
| Impaired capacity | 18 | yes at LB04, LB05, LB07, LB10, LB12; no elsewhere |
| What lowered each complainant's bore (note) | 4 | LB01 (Ernest Walker), LB02 (Brolga Plains Cattle Co), LB06 (Clarence Lewis), LB18 (Bottletree Holdings Pty Ltd): the dry seasons, with the mine's share 0.8, 0.7, 0.6 and 1.3 m against their falls of 4.63, 5.23, 4.84 and 8.70 m |

**Ask stops (each asserted to move exactly its figures):**
- Measuring point history ignored (the latest measuring point for every reading): KV-LB07's change -2.46 to -2.33,
  KV-LB08's -4.81 to -4.92 (resurveyed 14 November 2023 and 27 August 2025, after the baselines).
- Pumped dips kept: KV-LB06 209.61 to 208.88, KV-LB10 203.49 to 202.03, KV-LB11 238.12 to 236.65 (the three September
  pumped dips; the remark and the outlier rule agree on every September row, asserted).
- Loggers left uncompensated: the six logged bores move up about 10.02 m (KV-LB04 207.77 to 217.79 and five more).
- The last static reading instead of the September mean: 17 of the 18 levels move (KV-LB12 209.50 to 209.22, KV-LB18
  245.75 to 245.44, and fifteen more).
- UTC days instead of Queensland days: kept, it moves two printed levels (KV-LB12 209.50 to 209.49, KV-LB18 245.75 to
  245.74; both bores were falling fastest in September).

Recorded: 9.81 kPa per metre in place of the notes' 9.80665 moves no printed level. Every graded figure sits at least
0.15 of a unit from its rounding edge (a third of a centimetre for the three-dip means; logged levels placed 0.25 to
0.42 of a unit in), set by datum adjustments of 0 to 3.6 mm at six bores and by the drawdown targets; no two bores share
a printed figure in any column.

## PINS (shipped)

`MG-02_bore_assessment_and_make_good.pdf` (Tarrabool Resources, Kelvale Mine, revision 3, effective 01/03/2026; two
pages): 1.1 purpose; 1.2 scope (the register's landholder bores; reference and mine bores outside it); 2.1 static level
(pump off at least 12 hours; a pumped level is not used); 2.2 reduced level (the measuring point in force on the reading
date less the depth to water); 2.3 a logged bore's daily level (mean of the day's readings compensated for air pressure,
Queensland time); 2.4 the assessment level (mean of the static levels in the assessment month: daily levels for a logged
bore, manual dips otherwise); 3.1 triggers (2 m unconsolidated, 5 m consolidated, stated only here, asserted); 4.1
impaired capacity (the decline caused by the mine's take at the assessment level exceeds the trigger; "A decline with
another cause is not the mine's"); 4.2 the assessment month for a complaint; 4.3 the principal hydrogeologist recommends
and the executive team approves; 5.1 baseline assessments; 6.1 one agreement per owner covering every impaired bore of
theirs; 6.2 make-good measures; 7.1 complaints recorded in the register. Revision history 1 (07/03/2022), 2
(14/03/2023), 3 (01/03/2026).

Gate C sanity (asserted): MG-02 never defines the decline as a difference from the baseline and names no method (no
"model", "regression", "reference bore", "rainfall", "climate" or "method" anywhere in it).

`monitoring_network_notes.md` (Erika Martin, 9 October 2026): the network, identities, dip fields (feet for the EIS
rounds, Queensland time, remarks as written), the measuring point resurveys pointed to the register, logger compensation
(9.80665 kPa per metre, stated only here, asserted), UTC stamps, the check dips, the other files.

Banned in every shipped text, the xlsx cells, the prompt, the goldens and the submission (asserted): counterfactual,
transfer function, response function, TFN, cumulative rainfall departure, CRD, climate-adjusted, climate adjustment,
deseasonalise, detrend, recharge model, Pastas, Menyanthes, "without the mine", "would have been".

## PACK (shipped)

| File | Format | Rows | Role |
|---|---|---|---|
| `landholder_bore_register.xlsx` | xlsx | 18 + 29 + 9 | context artifact: the register, measuring points, network bores; labelled for the baseline assessments it records |
| `MG-02_bore_assessment_and_make_good.pdf` | pdf | | governing procedure (pins) |
| `monitoring_network_notes.md` | md | | field semantics, compensation, provenance of the extract |
| `water_level_dips_2012-2026.csv` | csv | 4,214 | manual dips as keyed (feet, variants, remarks, duplicates) |
| `logger_pressure_2015-2026.parquet` | parquet | 994,869 | hourly absolute pressure and water temperature, UTC (the volume gate) |
| `logger_installations.csv` | csv | 13 | serials, bores, times, sensor depths (with the barometric logger) |
| `barometric_logger_2015-2026.csv` | csv | 99,959 | hourly air pressure, UTC |
| `daily_climate_1990-2026.csv` | csv | 13,422 | gridded climate data for the point nearest the pit |
| `pit_dewatering_2022-2026.csv` | csv | 8,066 | daily metered take by source, with the meters' zero and estimated days |
| `landholder_contact_log_2026.xlsx` | xlsx | 61 | distractor (named in `metadata.json`) |
| `groundwater_quality_2012-2026.csv` | csv | 1,018 | distractor (named in `metadata.json`) |

Goldens: `golden/bore_impact_assessment.xlsx` (18 rows, the prompt's four figures with the register's identities, the
baseline level, the offer and the basis of each September level; a Method sheet with each bore's fitted response time,
shape and fit error) and `golden/make_good_recommendation.docx` (one page to Stephen Anderson from Rebecca Quinn: the
four offers by owner, bore and property, the coal-measure reasoning, one sentence for each complainant, the method in
plain words, a footnote on levels and rounding; rendered to one page through LibreOffice in scratch).

## PACK GATES (shipped)

| Gate | Requirement | Shipped |
|---|---|---|
| Files | 10 or more | 11 |
| Formats | 3 or more | 5 (csv, md, parquet, pdf, xlsx) |
| Volume | a file of 25,000 rows or more | logger parquet 994,869; barometric CSV 99,959 |
| Distractors | 2 or more, in `metadata.json`, golden unchanged without each | contact log and water quality; the call, offers, complainants and all 54 figures recompute identically with each removed (asserted) |
| Deliverables | the prompt's two | `bore_impact_assessment.xlsx`, `make_good_recommendation.docx` |
| Containers | no writer signature, in-fiction stamps | the pack's two workbooks rewritten in Excel's own dialect with in-fiction owners (Erika Martin) and fixed stamps, the goldens repacked with Rebecca Quinn and fixed stamps; MG-02 with its two fonts embedded and stamped Friday 27/02/2026 14:36:52, the library banner blanked at equal length; the producer audit clean |

The contact log carries the four complaints in the landholders' words, but the register already records each
complaint's date (MG-02 7.1), so the golden never reads the log.

## BUILD RECORD

- `generator/build.py` runs everything: the simulation (`world.py`, `sim.py`, `readings.py`), the pack (`records.py`,
  `docs.py`, `postprocess.py`), the goldens (`deliver.py` over `golden.py`, `analysis.py`, `models.py`), `metadata.py`,
  `checks.py`, `verify.py`, then a second full build into a scratch folder inside the task (`*.tmp`, gitignored,
  removed after) and the sha256 comparison. `target.zip` is not cut at this stage.
- Final run (stage 6b): `checks.py` **2,261 assertions passed**; `verify.py` OK; two consecutive builds byte-identical
  over `target/`, `golden/` and `metadata.json` (combined sha256 c4e345b30cdf9091); 1 minute 8 seconds. The goldens are
  byte-identical to the stage 3 build. MG-02 embeds Liberation Sans from the machine's
  `/usr/share/fonts/truetype/liberation/`, so a rebuild elsewhere needs those two font files to be byte-identical.
- `verify.py` (standard library, numpy, openpyxl, pyarrow, python-docx; imports nothing
  from the generator): recomputes the 18 September levels and 18 changes (match the workbook exactly), every naive rung, and
  the call with its own monthly gamma fit (12 shapes x 45 response times x 41 evaporation factors): the same five
  bores, drawdowns within 0.38 m of the workbook, offers and complainants matched in the note.
- Parameters chosen by search in scratch (never shipped): the climate sequence, the response shapes, the gains and the
  drawdowns, then datum adjustments and drawdown targets for the rounding edges (`world.SHIFT`, `world.BORES` dd).
- Invented names (H21): Kelvale Mine, Tarrabool Resources, Mundoora Creek (card); Yarrowmere, Tondara, Bluebush Downs,
  Kurrajong Park, Cypress Ridge, Saltbush Flat, Brolga Plains, Wilga Vale, Ghost Gum, Lancewood Flat, Bellbird Downs,
  Coolibah Springs, Gidgee Creek, Bottletree and their companies, each asserted against 80 real Queensland coal mines
  and mining companies (edit distance above 2, no containment); no check against a register of real pastoral
  properties was possible offline. The consultant appears only as IVH, the field officers only as initials.

## LEAK CHECK (mechanical half, re-run after the stage 6b repair)

`python3 .claude/skills/leak-check/leak.py task182 --asof 2026-10-13 --quiet` on the stage 6b cut: **REVIEW, no LEAK**
(19 REVIEW lines, the same four kinds as at stage 4; sweeps 1, 2, 5, 7, 8, 9 and 11 clean; the container audit finds no
writer signature). At stage 4 an earlier run also flagged the barometric file's `air_temp_c` column as a generator's
word; renamed `air_temperature_c` in the generator. Each REVIEW line:

- `MG-02_bore_assessment_and_make_good.pdf`, golden figures 2.4 and 1.1: these are MG-02's clause numbers (2.4 the
  assessment level, 1.1 the purpose); the golden's 2.4 and 1.1 are the drawdowns at KV-LB16 and KV-LB11, which MG-02
  never states. Harmless.
- `logger_pressure_2015-2026.parquet`, 17 golden figures (12 printed, "and 5 more"): the September levels of every
  bore but KV-LB12, whose 209.50 the text sweep cannot match. leak.py prints the first 12 of equal-length figures in
  set order, so which 12 it names changes between runs (this run 204.86, 203.49, 241.33, 209.61, 201.88, 195.44,
  201.27, 207.77, 205.24, 209.51, 214.47, 202.33; earlier runs also 199.16, 245.75, 238.12 and 243.13). They are
  hourly absolute pressures in kPa (195 to 250 kPa at these sensors) that coincide with September levels in m AHD
  (195 to 246 m), on other bores' loggers and on other dates (for example 207.77 kPa at 2041890, KV-LB12's logger, on
  24 July 2022, while 207.77 m AHD is KV-LB04's September level). No reading states a level. Harmless.
- Design-note vocabulary in MG-02 (8 of 25, among them reference, network, levels, measures, logger, reading) and in
  the notes (10 of 25, among them reference, network, levels, logger, reading, written): their own subject matter.
  The counts rose from 6 and 8 at stage 4 only because this note's stump paragraphs now carry "network", "written" and
  "record"; neither document's text changed (asserted by hash against the text the reader read). MG-02 names the
  monitoring network and the reference bores only to put them outside its scope; the notes say the reference bores
  sit outside the EIS predicted drawdown (a fact about where they are), that the field team has read the network
  monthly since July 2014 (a visit schedule), that remarks are kept as written, and call the climate file gridded
  climate data. Neither says what to do with a reference bore, the climate or the take, and no method word appears
  (asserted). Harmless.
- Ranking artifacts: the register names all 20 candidate names beside numbers, but its numbers are construction,
  coordinates and the baseline assessment as recorded, under a label that says so; it ranks nothing. The contact log
  names 13 (properties and owners) beside dates and times, and its routine notices name no bore; it records contacts
  and ranks nothing. Harmless.

**Solver's-eye read (pass 1, Sonnet; the answers are in `leak_check_report.md`).**
- **Q1, Q2 and Q4: none.**
- **Q3 names `monitoring_network_notes.md` as the file that briefs the analyst. Answered, no fix:**
  - it is the network's dictionary and the notes that go with the extract, required content written in the
    organisation's own voice (author, date, network history, field tables);
  - its logger formula is the standard field definition of a level (Layer 1 semantics), not the decisive step;
  - it never names the counterfactual, a lag or a reference-bore design.
- **No fork on the main call.** Nothing was fixed before the round; the realism notes are deferred.
- **Watch items for the solver round:**
  - The reader's rough model reached the answer unprompted. It fitted the pre-dewatering record to a lagged rainfall
    departure and found LB04, LB05, LB07, LB10 and LB12; the STOPPING RULE applies if the solver does the same.
  - The offer set separates by distance to the mine-bore ring (within 6.3 km, against beyond 6.9 km), so a
    proximity guess lands the call. If the round lands it that way, the hardening brief breaks the separation on
    the physics.

**Realism notes from pass 1, repaired at stage 6b in the generator** (every September level, change, drawdown, impaired
flag, offer, rung value, grid cell, evidence figure and ask stop recomputes bit for bit; the goldens are byte-identical;
the one value that moved is KV-MB01's own September level, which nothing graded reads). One line per note:
- **KV-MB03's logger typed 0-300 kPa reading 589.7:** fixed; the installation register types its sensor 0-1000 kPa, a
  deep sensor for the pit perimeter (about 50 m of water over it before dewatering); every logger's maximum is asserted
  inside its stated range.
- **Temperatures at 25.40 or 25.70 C:** fixed; each sensor reads the ground at its depth (23.6 C plus 2.8 C per 100 m,
  with the bore's own departure), a small annual swing at the shallow sensors, its own offset and slow drift, finer
  resolution on the two replacements and the first hours after installation cooling from the air (medians 23.85 to
  25.93 C, asserted).
- **Logger levels within 2 cm of every check dip, one outage:** fixed where nothing graded reads the record, answered
  where it does. KV-MB01's logger drifts about 4 cm from its check dips by 2026, steps at the downloads where it was
  re-hung, and was flat from 27 August to 8 October 2018 and out for a headworks repair from 9 to 22 May 2023;
  KV-MB03's was re-hung 4.5 cm high from the October 2019 download to the January 2020 one, stopped from 14 September
  to 7 October 2016 and was out for road works from 11 to 20 June 2024, all clear of April to June 2022 and September
  2026, the windows its cone evidence reads. The officers' remarks and the installation comments record each event.
  The eight landholder and reference loggers keep their record: every hour of theirs feeds a graded figure (the
  September levels, the fits behind every drawdown, the full-record grid family, the reference tracking), so a drift,
  a step or a gap there would move one.
- **The LB05 comment against data to 26 February 2019:** fixed on the data side; the comment now says the logger gave
  a low battery warning at the 11 February visit and was pulled for repair, which is what its record shows (asserted).
  Cutting the record at 11 February instead would take 15 days out of KV-LB05's fit.
- **Feet in the 2012 to 2014 rounds:** kept as the documented Layer 1 device, and plausible: dippers graduated in
  hundredths of a foot are standard imported field kit, and the consultant's own remarks now carry "ft dipper", with
  "MP marked TOC N side" at each bore's first round.
- **Remarks from a short fixed list:** fixed. Weather remarks only where the gridded rainfall and temperature bear them
  out (light rain, showers, heavy rain, wet tracks, dust, frost, heat; asserted row by row); headworks remarks only at
  bores with that headworks; pumped remarks that fit the pump; a few standing notes per bore (the Tondara dogs, the
  dam paddock gate); lease and road-reserve remarks at the mine and reference bores. No static dip's remark names the
  pump or reads as a dry reading, and the golden's and the verifier's pumped-dip rules agree on every row (asserted).
  This also closes two latent forks on September levels: "windmill turning" on KV-LB06's electric bore on 16
  September and "dry" on KV-LB17 on 3 September.
- **Quality sample_id in steps of 7:** fixed; numbers climb by one per sample and skip the duplicates and blanks sent
  with each laboratory batch; the consultant's samples keep their own EIS numbers.
- **No non-detects:** fixed; fluoride, nitrate as N and filtered iron added, and sulfate, nitrate and iron below the
  laboratory's limits reported as <1, <0.01 and <0.05 (866 non-detects, in the reduced coal measures and the oxic
  alluvium and basalt).
- **Every bore sampled in the same month:** fixed; the mine's bores quarterly, the landholder bores in March and
  September, the reference bores in September, each round a run of field days that can carry into the next month,
  one laboratory batch per dispatch.
- **Nothing moving at the pit-perimeter bores:** fixed; the four coal-measure mine bores take up sulfate (about 2.5
  mg/L to 2021, 108 to 171 in 2026), salt (EC up 19 to 25 per cent) and iron and lose about 0.3 to 0.6 of a pH unit as
  dewatering draws them down. Every bore off the lease moves less than 12 per cent in EC (asserted), so the file still
  points at no landholder bore.
- **Meters with no outage, zero or estimated day:** fixed; 233 zero days (83 with the reason, 150 the temporary pumps'
  idle days), telemetry outages split evenly from the totaliser and meter faults estimated from run hours (43 days
  flagged `estimated` in a new `volume_basis` column, beside a `comment` column).
- **AD03 and AD04 starting after March 2023:** fixed on the data side; both came on in late March 2023 on temporary
  pumps and meters (MAG-23-0110, MAG-23-0111) and went to their permanent pumps and meters on 14 August 2023 and 12
  February 2024, their volume coming out of the pit sumps on the same day. Every day's total is the simulated take to the
  last bit through the analysis's own pandas sum (asserted), so the full-record grid family reads the same take.
- **Contact log entries on weekends:** fixed; every entry is on a working day (asserted).
- **Lines pasted verbatim:** fixed; each routine notice carries its own particulars (the blast days and pit area, the
  bore run dates from the dips file, the road closure's dates, hours and reason, the month of the dust results), and no
  summary repeats (asserted).
- **"Three other landholders" on 7 September:** fixed; two (Saltbush Flat on 3 August, Brolga Plains on 19 August),
  counted from the register's complaint dates (asserted).
- **"Dipped 23/06" with no such dip:** fixed; the ridge paddock bore was dipped on the July run, 06/07, which the dips
  file holds (asserted). Two of the same kind fixed with it: the Yarrowmere logger visit sits on 9 April, the day of
  the KV-LB04 download dip, not 8 April; the Ghost Gum visit of 2 September is logged at 10:25 by Erika Martin, after
  the 10:09 dip she took there, not at 08:20 by the technician.
- **MG-02 effective on a Sunday, created at 08:30:00, base-14 Helvetica:** the effective date is MG-02's text and stays
  (a revision taking effect on the first of the month is ordinary); the PDF is now created on Friday 27 February 2026
  at 14:36:52 and modified at 14:37:05, and its two fonts are embedded subsets (Liberation Sans, Arial metrics, so
  every line breaks where it did) under ordinary subset tags. The extracted text is unchanged (asserted by hash).
- **MG-02 cites no Water Act:** not fixed. Naming the Water Act 2000 is a change to MG-02's text, which this repair
  may not make (it would need a second leak read); it rides with any later repair that has to touch MG-02.
- **openpyxl signatures under an Excel app.xml:** fixed; the two pack workbooks are written in Excel's own dialect
  (relative relationships and Excel's part order, a file version and calculation id 191029, full extended properties
  with the sheet titles, Excel's styles, cell and row records, page margins and column widths, the theme as Excel
  stores it); values, number formats, panes and filters are unchanged, LibreOffice reads both as before, and no
  openpyxl marker remains (asserted). The goldens keep their containers.
- **The register's line saying what it lacks:** fixed; A2 now says only what the register holds.

## SURFACE (`guard.py surface task182`)

2 pairs promoted of 126 in scope: task83 (surface 0.147, corpus percentile 100) and task132 (0.138, percentile 99).
Both rest only on the coarse axes: the pack layout (1.0), the format mix (0.67 and 0.43) and the deliverable species
(xlsx plus docx, 1.0, fixed by the prompt at stage 2). Filenames, schemas, same-seed tables, invented names, prompt
wording (masked and raw), the ask skeleton and the submission's steps share nothing (0.0; submission 0.005 against
task132). Not a rename or regeneration finding; reported to the author for the adjudicated check. Personas in the cut
pack: Clarence Lewis, Erika Martin, Ernest Walker, Rebecca Quinn, Stephen Anderson (all on the card; Noah Carrillo
appears in the contact log and as NC), and the checks' own scan of the pack, the goldens and the prompt finds only the
card's six.

## DEVIATIONS FROM THE DESIGN (as built)

- **Climate.** The wet seasons are 2019-20 and 2020-21 with an average 2021-22 (water years 2020 843, 2021 956, 2022
  551 mm), not wet through 2022, and the failed seasons are deeper (318 to 348 mm). A wet 2021-22 season put every
  alluvial and basalt baseline at a peak, so the decline from the 2012-2022 mean (rung 1b) could not clear its trigger
  with 25 per cent; and with any milder drought every coal-measure response short of a five-year delay was falling by
  2026.
- **Magnitudes.** A2 to A7 fell 4.63 to 5.23 m (target 2.5 to 4.5), B4 8.70 (6.5 to 7.5), A1 8.78 with a 4.6 m drawdown
  (5 to 6 and 2.8 to 3.5), the alluvial reference bores 4.84 and 5.02 (about 3) and the basalt reference 5.16 (about
  1.5). Rung 1b on the mean needs B4 at least 6.25 m below its 2012-2022 mean (its baseline sits 1.71 m above it), while
  rung 2 needs B4 less any reference at most 3.75, so the references must fall about 5 m; the pooled subtraction then
  needs A1 at least 2.5 m above the reference mean. The coal-measure drawdowns are 8.2 to 9.3 m (target 6.5 to 9)
  because the rainfall-departure family runs about 1.4 m low on the coal measures.
- **Response times.** The coal measures respond over 6.2 to 6.8 years with a strongly delayed shape (16); the alluvium
  140 to 200 days at shapes 1.5 to 2 (short shapes turned single storms into rises above ground at the gains the
  declines need).
- **Families.** The exponential family carries a fitted delay and the rainfall-departure family a fitted lag; without
  them neither can produce the coal measures' rise after the rain stops. Rung 3 reads a negative fitted slope as no
  response (the bore's pre-July 2022 mean).
- **Rung 2b** gives A1 to A9 and B4 (ten bores: every alluvial bore and the ridge bore), not every bore: the
  coal-measure lines run flat.
- **Rounding rule.** "No graded figure within half a unit of its last printed place of a rounding edge" read as: at
  least 0.15 of the last printed unit from the edge (the literal reading excludes every number). Shipped minimum 0.17
  for levels and changes, 0.44 for drawdowns.
- **Pumped dips.** None at the six logged landholder bores (their windmills and pumps draw a few centimetres, not
  simulated); three in September 2026 at KV-LB06, KV-LB10 and KV-LB11. The outlier rule matches the remarks on 80 of 93
  pumped dips and flags 10 others, identical in September.
- **Mess.** The feet record read as metres moves the call (recorded, not asserted).
- **Names.** Tea Tree Flat became Lancewood Flat (the people scan read "Tea Tree" as a person).
- **Complaints** are dated in the register (MG-02 7.1), so the contact log stays a distractor.
- **Prompt.** Unchanged.

## STOPPING RULE

Three hardening loops on this architecture, then a re-root in the same objective and number; three architectures, then
retire.

## Tried and rejected

- Seed AD05 as written: a prescriber's high-dose count pinned by the board's reviewer determinations, which is a
  certified-figure replay. Its world repeats task180's role, forum and organisation family.
- Left-censored arsenic results across a laboratory reporting-limit change (a bore watch list for a water company).
  It had the same gap, G-code and Gate G as task134, a third censoring stump in a row, and its forum, forcing event,
  organisation family and shape would have repeated task228 and task229, which sort after task182 in draw order.

- A wet 2021-22 season (the design's "wet 2020 to 2022"): every alluvial and basalt baseline then sat at a peak, so the
  decline from the 2012 to 2022 mean (rung 1b) fell under the trigger at most alluvial bores and at B4. The 2021-22
  season is average and the wet seasons are 2019-20 and 2020-21.
- Short alluvial responses (shape 1, 60 to 110 days) with each gain set from its baseline decline: single storms lifted
  the water table 10 to 30 m, above ground. Alluvial responses are 140 to 200 days at shapes 1.5 to 2, and six datums
  were deepened so every water table stays 1.5 m or more below ground.
- Coal-measure responses of shape 1 to 12 with means of 3.5 to 6.5 years: with failed seasons at 55 per cent of the
  mean rainfall, each had stopped rising by 2026 as the drought reached it, so the rise the mine hides was gone or
  turning. Shape 16 with means of 6.2 to 6.8 years keeps it rising through September 2026 (asserted).
- An exponential family without delay and a rainfall-departure family without lag: no positive rainfall response exists
  at short lags for the coal-measure bores, so a plain exponential has no fit and a no-lag window reads A1 alone. Both
  families carry a fitted delay or lag.
- The single-window regression taken at face value: its fitted slope is negative at every coal-measure bore, which
  forecasts a rise in the drought and put CM3 into rung 3's set at 4.5 m. A negative slope is read as no response (the
  bore's pre-July 2022 mean).
- A basalt reference falling about 1.5 m (the design's figure): B4 would then need at most 5.25 m of decline for rung 2
  and at least 6.25 m for rung 1. The basalt reference falls 5.16 m, the alluvial ones 4.84 and 5.02.
- A robust outlier rule on the median of all dips within 60 days (5 MAD): it flagged 31 fast seasonal falls and missed
  33 pumped dips. Replaced by the median of up to two readings either side within 50 days, with pumped drawdowns in the
  alluvium of 1.7 to 2.8 m.
- Coal-measure drawdowns of 7.4 to 9.2 m: the rainfall-departure family put CM4 at 5.9 to 6.1 m, inside the 25 per cent
  margin. Raised to 8.1 to 9.4 m.
- The property name Tea Tree Flat: the people scan reads "Tea Tree" as a person. Renamed Lancewood Flat.
- Cutting KV-LB05's first logger record at 11 February 2019 to match its "no data since" comment: it takes 15 days out
  of the fit behind KV-LB05's 9.3 m. The comment now agrees with the record (a low battery warning at that visit).
- AD04's temporary-pump volume carved out of pit sump 1 (AD03's out of pit sump 2), then a random litre nudged between
  meters until each day summed right: pandas sums a day's printed volumes with Kahan compensation, and on days such as
  17 April 2023 the six smaller volumes cannot land on the one-ulp-high double the four-meter file gave, whatever
  litre is moved between any two meters. Both carved out of pit sump 2 (pit sump 1 only when it ran low), which keeps
  the addends' error capacity, a deterministic search over meter pairs and shifts reproduces every day's double.
- The dip remark "dusty" (EM writes "Dusty"): the people scan read "Dusty Dogs" (beside "Dogs tied up") as a person.
  Renamed "dust about".
