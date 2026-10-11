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
measures were still climbing on the 2020 to 2022 wet seasons when the pit's dewatering pulled them back down, and the
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
that fell more than 2 m and the basalt bore that fell more than 5 m. The step that lands it there is reading the
decline since the baseline as the mine's. In fact the alluvium and the basalt fell through the dry seasons on rainfall
alone. The coal-measure bores near the pit were still rising on the 2020 to 2022 wet seasons, and the mine drew them
6 to 9 m below where that rise would have taken them while they show less than 4 m of decline.

## ENTITY AND UNIT OF VALUE

One landholder bore. MG-02 4.1's test: the decline in the bore's water level that the mine's take of associated water
has caused, at its September 2026 assessment level, against the trigger for its aquifer (2 m unconsolidated, 5 m
consolidated). An offer is an agreement with the bore's owner (deepen, replace or supply water).

## THE WORLD (build plan; every figure below is a target the generator asserts or replaces with its shipped value)

**The mine.** Kelvale Mine, an open-cut coal mine of Tarrabool Resources in the northern Bowen Basin (Isaac region,
central Queensland).
- The box cut started in June 2022 and pit dewatering began on 4 July 2022. Advance dewatering bores came on from March
  2023, and the take rises as the pit deepens.
- The take is metered daily by source (pit sumps, advance dewatering bores AD01 to AD04).

**Hydrogeology.** Three units:
- The Mundoora Creek alluvium: unconsolidated, trigger 2 m. Water table 5 to 15 m below ground. Responds to a wet
  season within weeks to months.
- The Tertiary basalt on the ridges: consolidated, trigger 5 m. Responds over months to a year or two.
- The Permian coal measures: consolidated, trigger 5 m. Confined, recharged at the outcrop. Levels respond over years.
  The pit dewaters this unit.

The coal measures subcrop beneath the alluvium at the pit's eastern end, so one alluvial bore there is drawn down
through leakage.

**Climate (shipped daily, 1990 to September 2026).**
- Summer-dominant rainfall averaging about 600 mm a year, with Morton areal potential evaporation of about 1,800 mm.
- Wet 2010 to 2011, dry 2013 to 2015, average 2016 to 2017, dry 2018 to 2019, wet 2020 to 2022, three failed wet
  seasons 2023 to 2025, and a dry 2026 to date.
- Synthetic, seeded, plausible against the region.

**Bore response (the simulation, never shipped).** Head = constant + response to recharge (rainfall less a fitted share
of evaporation, through a gamma response with its own gain and mean response time per bore) − response to the mine's
take (a Hantush-type response whose gain falls with distance and leakance, and whose lag grows with distance) + AR(1)
noise.
- Mean response times: alluvium 60 to 200 days, basalt 300 to 700 days, coal measures 3.5 to 7 years.
- The coal measures' 2020 to 2022 rise is still running in 2026 without the mine.

**The 18 landholder bores in the register (targets).**

| Bores | Unit | Observed change, baseline to Sep 2026 | Drawdown the mine caused | Call |
|---|---|---|---|---|
| CM1 to CM4 (3 to 6 km from the pit) | coal measures | −1.5 to −3.5 m | 6.5 to 9 m | impaired (answer) |
| CM5 (11 km) | coal measures | +1 to +2 m | 2 to 3 m | not impaired |
| A1 (above the subcrop, 2 km) | alluvium | −5 to −6 m | 2.8 to 3.5 m | impaired (answer) |
| A2 to A7 | alluvium | −2.5 to −4.5 m | 0.1 to 0.8 m | not impaired |
| A8, A9 (on the creek's permanent waterholes) | alluvium | −0.8 to −1.5 m | below 0.5 m | not impaired |
| B1 to B3 | basalt | −1 to −3.5 m | 0.5 to 2 m | not impaired |
| B4 (a ridge bore) | basalt | −6.5 to −7.5 m | about 1.5 m | not impaired |

**The other bores in the network (not in the decision).**
- Three state reference bores outside the predicted drawdown, 20 to 30 km from the pit: two in the alluvium (change
  about −3 m) and one in the basalt (about −1.5 m). None is in the coal measures.
- Six mine monitoring bores near the pit (two alluvium, four coal measures; drawdown 3 to 40 m).

**Monitoring history.**
- Environmental-impact baseline dips from March 2012, quarterly, read in feet by a consultant until June 2014.
- Monthly dips by the mine's field team from July 2014.
- Hourly unvented loggers from May 2015 at ten bores: six landholder bores (CM1, CM3, A1, A3, B2, B4), two reference
  bores and two mine bores.
- One site barometric logger.
- Baseline assessments under MG-02 in April to June 2022.
- Complaints in August and September 2026 from the owners of A2, A3, A5 and B4 (bores "sucking air").

## LADDER (planned; each rung asserted by name in `generator/checks.py`)

| Rung | Construction | Set | Killed by |
|---|---|---|---|
| 0 | The complaints | A2, A3, A5, B4 | a complaint is not a test |
| 1 (naive) | Decline from the baseline assessment level to the September 2026 level, against the trigger | A1 to A7, B4 | the decline since the baseline is the seasons' and the mine's together |
| 1b | Decline from the June 2022 level (or from the 2012 to 2022 mean) | as rung 1 | as rung 1 |
| 2 | Decline less the reference bores' change (pooled, or matched by unit with the basalt reference for the coal measures) | A1 only | no reference bore is in the coal measures, whose path was a rise |
| 2b | The pre-July 2022 trend extrapolated (linear, 2017 to 2022 or 2012 to 2022) | almost every bore | the 2020 to 2022 rise was the wet seasons, not a trend |
| 3 | One rainfall model for every bore (cumulative rainfall departure on one window, 12 months or 3 years), calibrated before July 2022 | A1 (CM bores well under 5 m) | the coal measures' response runs years longer than any one window |
| 4 (answer) | Each bore's own response to rainfall and evaporation, calibrated on its record before 4 July 2022 and run forward; drawdown = modelled level without the mine − September 2026 level | **CM1, CM2, CM3, CM4, A1** | |

**Margins (targets, asserted).** Every bore's quantity sits at least 25 per cent from its trigger at every rung, so no
set is decided at its edge.
- In every answer cell: CM1 to CM4 at 6.25 m or more; A1 at 2.5 m or more; every other coal-measure or basalt bore at
  3.75 m or less; every other alluvial bore at 1.5 m or less.
- At rung 1: A2 to A7 decline 2.5 m or more; B4 6.25 m or more; CM1 to CM4 3.75 m or less.

**Evidence the pack carries for the judge (asserted).**
- The coal-measure bores were rising before 4 July 2022 (0.5 to 1 m a year since 2021).
- The per-bore climate model fitted before dewatering tracks the three reference bores through September 2026 within
  0.5 m.
- The mine's coal-measure monitoring bores show the cone (20 to 40 m).
- A full-record model with the take as a second stress gives the same set.

## GRID (planned, asserted cell by cell)

Answer cells. Every cell gives the answer set with the 25 per cent margins.
- Model families:
  - a gamma response to rainfall and evaporation (evaporation factor fitted);
  - an exponential response;
  - a cumulative-rainfall-departure regression with each bore's window chosen by fit (1 to 10 years);
  - a regression on several rainfall moving averages (1, 3, 5 and 8 years);
  - a full-record model with the take as a second stress, whose take term is the drawdown.
- Calibration windows: from the first reading, or from May 2015, to 3 July 2022.
- Time steps: daily or monthly.
- Data: manual dips only, or logger daily means where there are loggers.

Naive cells give their rung's set:
- rungs 1 and 1b under every reference level;
- rung 2 pooled, and matched by unit;
- rung 2b on both trend windows;
- rung 3 on 12 months and 3 years.

Variants that must keep every winner:
- assessment level as the September mean or the last static reading in September;
- pumped dips removed by remark or by the robust outlier rule;
- the 2012 to 2014 feet record kept or dropped.

## CLOSURE (the 22 axes)

1 Population: the 18 landholder bores in the register (MG-02 1.2); the reference bores and the mine's own bores are
outside it. 2 Unit: one bore. 3 Window: the September 2026 assessment level; the take from 4 July 2022. 4 As-of: water
levels to 30 September 2026 (loggers downloaded 1 to 6 October, the extract delivered Friday 9 October 2026); the
request on Tuesday 13 October; the executive team on Monday 26 October 2026. 5 Version basis: one row per reading; a dip
keyed twice is one reading. 6 Divisor: none (a level difference). 7 Weighting: none; a logged bore's September level is
the mean of its daily means, otherwise the mean of its static dips (MG-02 2.4). 8 Window length: one calendar month. 9
Boundary: every bore at least 25 per cent from its trigger at every rung and in every answer cell. 10 Rounding: levels
to two decimals and the mine's drawdown to one decimal in the deliverable; the call on unrounded values. 11 Tie-break:
none needed. 12 Maturity: none (September is complete in the extract). 13 Order: identity, units, reduced level with the
measuring point in force, static readings only, logger compensation and AEST days, the September level, then the
attribution, then the trigger. 14 Row order: irrelevant. 15 Duplicates: identical double entries. 16 Identity: state
registered number, company code and landholder's name through the register. 17 Netting: none. 18 Units: metres (feet
before July 2014, 0.3048). 19 Code semantics: aquifer class from the register's unit (alluvium unconsolidated; basalt
and coal measures consolidated). 20 Integerisation: none. 21 Scope: water level (yield and quality are not this test).
22 Forward window: none (MG-02 4.1 tests the September 2026 level, not a projection).

## ASK SHEET (planned)

| Ask | Figures | Depends on the call |
|---|---|---|
| The bores and properties that get offers, and how many offers (memo; MG-02 6.1: one agreement per owner, covering every bore of theirs with impaired capacity) | 1 set + 1 | yes |
| Per bore (workbook, 18 rows): September 2026 level in m AHD, two decimals | 18 | no (Layer 1: measuring points, pumped dips, compensation, AEST days, feet do not reach September) |
| Per bore: change since its baseline assessment, m, two decimals | 18 | no (Layer 1: the baseline's measuring point) |
| Per bore: the decline the mine has caused, m, one decimal | 18 | yes (graded on the band the answer grid spans, plus or minus a tolerance the build sets) |
| Per bore: impaired capacity yes or no | 18 | yes (the call bore by bore) |
| For each complainant whose bore misses the test (A2, A3, A5 and B4, all four): what lowered it (memo) | 4 | yes |

Ask stops (each asserted to move its figures):
- Measuring point history ignored (the latest measuring point for every reading): two bores' baseline changes move.
- Pumped dips kept: the September levels of the bores with a September pumped dip move.
- Loggers left uncompensated: about 10 m.
- UTC days: the September means of logged bores move by a few millimetres; checked, and kept only if the shift clears a
  rounding edge.
- The last reading instead of the September mean.

## PINS (planned)

`MG-02_bore_assessment_and_make_good.pdf` (Tarrabool Resources, Kelvale Mine, revision 3, effective 1 March 2026):
- 1.1 purpose; 1.2 scope (the landholder bores in the register).
- 2.1 static level (pump off at least 12 hours; a reading with the pump running is a pumped level and is not used).
- 2.2 reduced level (the measuring point elevation in force on the reading date, less the depth to water).
- 2.3 a logged bore's daily level (the mean of the day's compensated readings, Queensland time).
- 2.4 the assessment level (the mean of a bore's static levels in the assessment month: daily means for a logged bore,
  manual dips otherwise).
- 3.1 trigger thresholds by aquifer class.
- 4.1 impaired capacity: the decline in the bore's water level caused by the mine's take of associated water, at its
  assessment level, exceeds its trigger. Declines with other causes are not the mine's.
- 4.2 the assessment month for a complaint is the last complete month before the assessment.
- 5.1 the baseline assessment records the bore's construction, static level, yield and water quality before the take
  began.
- 6.1 offers: one make-good agreement per owner, covering every bore of theirs with impaired capacity. Two of CM1
  to CM4 share an owner, so the answer's five bores make four offers.
- 7.1 complaints.

No sentence defines the decline as a difference from the baseline. No sentence names a method of attribution.

`monitoring_network_notes.md` (Erika Martin): field semantics, the feet era, measuring point resurveys, the logger
compensation (kPa to metres at 9.80665 kPa per metre of fresh water), UTC stamps, and how codes and numbers map.

Banned in every shipped text and the prompt (asserted): counterfactual, transfer function, response function, TFN,
cumulative rainfall departure, CRD, climate-adjusted, climate adjustment, deseasonalise, detrend, recharge model,
Pastas, Menyanthes, "without the mine", "would have been".

## PACK (planned; the builder may rename within the company's conventions)

1. `landholder_bore_register.xlsx` (context artifact: bores, owners and properties, landholder names for the bores,
   unit and class, trigger, construction, coordinates (GDA2020, MGA zone 55), baseline assessment date, level and
   yield; measuring point history on a second sheet; the network's reference and mine bores on a third)
2. `MG-02_bore_assessment_and_make_good.pdf` (pins)
3. `monitoring_network_notes.md`
4. `water_level_dips_2012-2026.csv` (manual dips: date, time, bore as recorded, depth to water, unit, remarks, officer)
5. `logger_pressure_2015-2026.parquet` (hourly absolute pressure, kPa, UTC, by logger serial; the volume gate)
6. `logger_installations.csv` (logger serial, bore, installed and removed, sensor depth below the measuring point)
7. `barometric_logger_2015-2026.csv` (hourly air pressure, kPa, UTC)
8. `daily_climate_1990-2026.csv` (rainfall and Morton areal potential evaporation for the mine's coordinates)
9. `pit_dewatering_2022-2026.csv` (daily metered take by source, ML)
10. `landholder_contact_log_2026.xlsx` (distractor: contacts and complaints, the forcing event's record)
11. `groundwater_quality_2012-2026.csv` (distractor: field EC, pH and major ions by sampling round)

Goldens:
- `golden/bore_impact_assessment.xlsx` (18 rows).
- `golden/make_good_recommendation.docx` (a realistic one-page memo to Stephen Anderson: the offers, the count, the
  complainants whose bores miss the test and why, and the method in plain words).

## STOPPING RULE

Three hardening loops on this architecture, then a re-root in the same objective and number; three architectures, then
retire.

## Tried and rejected

- Seed AD05 as written: a prescriber's high-dose count pinned by the board's reviewer determinations, which is a
  certified-figure replay. Its world repeats task180's role, forum and organisation family.
- Left-censored arsenic results across a laboratory reporting-limit change (a bore watch list for a water company).
  It had the same gap, G-code and Gate G as task134, a third censoring stump in a row, and its forum, forcing event,
  organisation family and shape would have repeated task228 and task229, which sort after task182 in draw order.
