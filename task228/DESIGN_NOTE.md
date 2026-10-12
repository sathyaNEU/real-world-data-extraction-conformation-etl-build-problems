# task228 design note

Architecture 2 (re-rooted 2026-10-11), spent at hardening loop 2. Physical & Environmental Sciences, sensor
calibration and measurement, Data Quality Monitoring & Alerting. A prairie soil moisture reference network
(Coteau Agroclimate Research Centre, Saskatchewan) chooses which eight of its 56 stations the April 2027
crew re-installs before the Prairie Drought Service starts anchoring its satellite soil moisture layer on
the network. Architecture 1 (the experiment platform's paging alert) is spent; its record is in
`## Tried and rejected` and in the card's lineage. Round 3 landed the call on plain triple collocation;
loop 1 deepens that step rather than replacing it (the brief and the answer are in `## Ladder`). Round 4
landed loop 1's rung, and loop 2's phase A found no further rung (`## Hardening loop 2, phase A`), so
architecture 2 is spent. The re-root to architecture 3, the number's last, found no architecture at phase A
(`## Architecture 3, phase A`); nothing was registered, and retiring the number is the author's call. The
author then granted a fourth architecture as an exception to the cap, in a new world; its phase A also found
no architecture (`## Architecture 4, phase A`). The author paused the number rather than retire it
(`## Paused`): architecture 4 is redrawn once task229 or task230 ships. Nothing was registered for
architecture 4, and the card on file is still architecture 2's.

## DRAW

| Axis | Draw |
|---|---|
| Card | `task228.json` architecture v2, re-keyed 2026-10-11 for hardening loop 1 (the driver changed: cross-correlated reference errors through a shared input, broken by a fourth independent series); the round-3 driver is in the card's lineage. `guard.py check` and `heart`: BLOCK only `ban.pattern` G16 against task134 (the author's waiver, same ban), WARN `repeat.gate_g` against task134 (answered below); nearest driver on file is this slot's own round-3 cut at 0.26 (differentiated), every other card at or under 0.07 |
| Shape | 01, ranked list under a cap (56 stations, 8 slots) |
| Gate G mechanism | `method_or_model_selection` (which collocation the data's error structure admits), with `statistical_rigor` support (G17); stump strategy `decomposition_attribution` |
| Gap / pattern | objective / none (the metric everyone would compute is correct and is not the one the standard scores) |
| Generators | G16 decisive (the field's standard three-way collocation assumes independent reference errors, which fails where both products share the soil map's texture; only an independent fourth series estimates the defined quantity there), G13 lower rung (current probe only), G17 (the eighth and ninth held apart) |
| Domain, task type | physical-environmental-sciences, sensor-calibration-measurement (in-situ reference validation of a satellite product) |
| Role | statistical office head (the head of the network's data office, who signs the re-installation list and the delivery statement) |
| Forum, forcing event, org | the counterparty (the Drought Service's anchor coordinator), a launch (anchoring from 15 April 2027), a research or statistics office |
| Context artifact | planning thread (the crew's campaign plan) |
| Calibration form | none: the estimand is stated in the standard and the method follows from the design (independent observing systems of one field); nothing is recovered from settled cases |
| Stump strategy | `decomposition_attribution`; decisive rule filed (NS-03 s.2.1 states the estimand), no official decoy, no validated decoy |
| Layer 2 | `own:collocation-with-cross-correlated-reference-errors` (field_method) |
| Repeats | `ban.pattern` against task134 (decisive G16), waived by the author; `repeat.gate_g` WARN against task134: the shared label is an estimator choice pinned by a stated estimand, on a different driver (competing exits against cross-correlated reference errors) and domain. Later seeds task249 to task252 (sensor calibration; task251 "both instruments noisy") are near in subject: none of them turns on two references sharing an ancillary input |

Author waiver, 2026-10-11: ban.pattern (decisive G16) against task134 waived by the author after pre-flight pass 4; the drivers differ, different domains, and task134 was registered after this draw. The adjudicated pre-flight is owed again because loop 1 changed the driver.

**Data-native sentence.** A soil moisture station is one point in a 36 km cell, and the only other views of
that cell, the L-band retrieval and the land-surface model, are estimates whose errors are largest where the
network's pothole, parkland, irrigated and clay sites sit; over the heavy clay plains both products take
their soil texture from the same provincial soil map, so even the field's standard three-way separation
charges those stations with an error the products share, and only a second station in the cell, a separate
probe on its own field and rain, separates it.

## The three rules

1. **Domain (swap test).** Separating a station's own random error from a retrieval's and a model's by
   collocation, and seeing from their ancillary inputs that two of the three share a soil texture map and
   so are not independent where that map is wrong, is the core of in-situ reference validation in remote
   sensing. With another field's nouns there are no independent observing systems of one geophysical field
   whose error structure follows from what each ingests; the task stops reading the same.
2. **Two layers.** Layer 1: UTC logger tables against a UTC-6 delivery day, re-sent hours after logger
   restarts, -9999 failed reads, lost hours, frozen-soil hours, catch-up hours received 26 to 44 hours late,
   a backlog loaded at a site visit, probe and logger replacements in the register and a visit log with two
   date formats, satellite rows dated by local solar date with J2000 seconds, bit-packed quality and surface
   flags, a superseded version 4 extract, model water in millimetres over 0 to 10 cm at six-hourly UTC,
   coordinates to be placed on two grids, station gauges run April to October. Layer 2: the station's own
   error has to be separated from two references whose errors are not independent over the clay plains.
3. **Analyst test.** A strong analyst who cleans all of it, reads every rule and runs the field's standard
   triple collocation of station, morning retrieval and model files Balgonie S, Grand Coulee and Regina W
   in place of Watrous S, Melfort N and Kandahar (three swaps, asserted); one who stops at a single
   comparison files a list holding 2 to 6 of the eight. The step that decides is analytical: whether two
   references can be taken as independent is a judgement about their inputs, and no rule makes it.

`stump_class: analytical`.

## Gate G

**Litmus.** No reported number in the pack is wrong and none is overturned: the pack ships no ranking, no
tracking figure and no stakeholder conclusion about any station. Each provider documents its product
honestly in its own voice: the Ninox notes name the 1:1 million provincial soil maps as the source of the
clay fraction (Ancillary data); the PLSM note names the same map under Soils and lists "the heavy clay plains
come out of the soil map as clay loam" among its known limits. Nothing says the two products' errors co-vary,
names an estimator, or gives a second station a role.

`surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.

**Delete every wrong number.** There are none to delete; every naive figure is computed by the solver from
correct data. **Clean-data test** (asserted): repairing the logger tables changes no tracking row; deleting
the three distractors and the gauge file leaves every golden figure unchanged. **Instrument repair.** No
instrument mis-reports: the shared texture error is the products' documented behaviour over heavy clay, not
a defect, and no instrument observes the decision's quantity. **Lens swap.** No relabelling turns a
three-way covariance figure into the station's own error over the clay plains; it takes a fourth,
independent series.

## Stump sentence

A competent solver who reads NS-03 s.2.1 as asking for each station's own error separates it by triple
collocation of the station, the morning retrieval and the PLSM model, and re-installs Spiritwood N, Swift
Current E, Pense, Kindersley W, Davidson W, Balgonie S, Grand Coulee and Regina W (ninth Watrous S). The step
that lands it there is treating the retrieval and the model as independent references over the heavy clay
plains, where both take their texture from the same provincial soil map and err together, so the products'
shared error is charged to the stations: Balgonie S, Grand Coulee and Regina W (own errors 0.008, 0.007,
0.011) come out at 0.039, 0.038 and 0.037, and Pense at 0.050 for its own 0.038. A second station in the
cell, collocated with the station and the retrieval in the model's place, separates it and drops all three
below the ninth.

## Entity, unit and decision

The network re-installs stations, and a station is scored on its own random error against the true 0 to 5
cm soil moisture of its cell, in its own units (NS-03 s.2.1). Its disagreement with a reference, or a
three-way figure that assumes independent references, differs from that by an error the station does not own.

**Decision.** Exactly eight of 56 stations, largest own error first (NS-03 s.3.1; campaign plan: 8 slots).

**Answer.** Spiritwood N 0.061, Swift Current E 0.054, Kindersley W 0.048, Davidson W 0.043, Pense 0.038,
Watrous S 0.034, Melfort N 0.031, Kandahar 0.027 (m³/m³; targets 0.06108 to 0.02711). Ninth Craik E 0.020
(0.01991), gap 0.007, eighth over ninth 1.36x, ninth over tenth (Wadena S 0.01491) 1.34x. Anchors from 15
April: Brown 12, Dark Brown 22, Black 9, Dark Gray 4 (Aylsham sits out on the 60-day silence clause: nothing
delivered for 206.5 days; the next longest silence is 23.7 days). Delivery 2025-26: 10,444 station-days.

## The estimand pins, and the filed sentences

NS-03 s.2.1 defines tracking error as the standard deviation of the station's own random error, the part of
its 5 cm readings that does not follow the true 0 to 5 cm soil moisture of its satellite cell, once its own
offset and scale are allowed for, in the units of its own readings. It pins what is measured and never how.
s.2.3 defines tracking mornings as a sample (recommended-quality descending retrievals over the cell, the
station's reading nearest the overpass); s.2.4 the current probe and the three seasons. The products' errors
are stated only in their own documents (Ninox accuracy target and its degradation with vegetation and open
water; the PLSM known limits). The shared input is filed as each provider would file it, and the second
station's independence is in the pack's own records: the register's coordinates (sisters at least 14.1 km
apart, separate fields) and `coteau_gauges_daily_2024-2026.csv` (sister gauges correlate 0.73 to 0.96 on daily
totals, every pair with 2 to 11 days of a storm at one gauge, 10 mm or more, with the other under 2 mm).

| Route (checks.py name) | Overlap | Its wrong picks | What it misses |
|---|---|---|---|
| unbiased RMSE against the retrieval (`ubrmse_satellite`) | 2 | Avonlea W, Briercrest, Dafoe, Dirt Hills, Wynyard E, Yorkton W | the retrieval's own error (Ninox notes: degrades with vegetation and open water) |
| the same less the 0.04 target (`minus_accuracy_target`) | 2 | as above | a constant cannot remove a cell-dependent error |
| against the model (`ubrmse_model`) | 5 | Avonlea W, Rokeby, Wynyard E | the model's own error (PLSM known limits) |
| the better of the two (`ubrmse_better_reference`) | 5 | Avonlea W, Rokeby, Wynyard E | still a reference's error |
| against their mean (`ubrmse_mean_reference`) | 6 | Avonlea W, Balgonie S | half of each error, and over the clay their shared error whole |
| regression residuals (`residual_satellite`, `residual_model`, `residual_mean_reference`) | 5, 6, 6 | Dirt Hills, Muenster, Yorkton W; Avonlea W, Rokeby; Balgonie S, Grand Coulee | the reference's error, attenuated |
| against the other stations in the cell (`ubrmse_neighbour_stations`) | 5 | Flaxcombe, Leoville S, Wymark | the neighbours' own errors |
| triple collocation of station, retrieval and model (`plain`) | 5 | Balgonie S, Grand Coulee, Regina W | the products' shared texture error over the clay plains |

`checks.py` asserts per route: not the eight, at most 6 of them, every wrong pick below the definition's
ninth, charged at least 1.8 times its own error, never read below its own error less 0.002; plain collocation
adds only clay stations, charges them at least 2.5 times their own error, and matches the definition within
6e-5 outside the clay cells.

**Every rigorous estimator lands the eight, in order, and every three-decimal figure for all 56** (10,
asserted): a second station in the model's place (the golden, mean of error variances over the cell's
other stations), the first or the last sister alone, a second station in the retrieval's place, quadruple
collocation with the retrieval-model error covariance left free, extended collocation fitted by least
squares on the five usable covariances, a covariance-corrected form (the retrieval-model error covariance
estimated from the sister), the sister only in the clay cells, difference notation, the model in
millimetres. The three stations alone in their cells (Maple Creek NE, Kerrobert, Assiniboia N) are the only
ones on the model leg, and none sits in a shared-texture cell (asserted). **Implementation variants** (8,
asserted with the eight and the ninth held, eighth over ninth at least 1.12): model at 18 UTC 0.0271/0.0199,
every quality flag 0.0270/0.0200, ignoring the probe change 0.0271/0.0199, last two seasons 0.0283/0.0206,
trimmed at 3 SD 0.0265/0.0196, season-demeaned 0.0271/0.0199, an independent re-match 0.0271/0.0199, version 4
for 2024 0.0250/0.0199. **Screens:** a 2 per cent open-water screen keeps the eight, their order and the
ninth; the evening pass (excluded by s.2.3) keeps the eight in order; a dry-morning screen off each station's
own gauge (drops the 20 per cent of mornings after a day of 1 mm or more) keeps the eight in order and the
ninth (Craik E 0.0168 against Wadena S 0.0146). **Block bootstrap** (300 draws, 10-day blocks within seasons,
golden estimator): the eight hold in 0.990 of draws, the ninth in 0.883.

Construction behind the convergence: each station's error (an AR term, its own storm wet-up, white noise) is
orthogonalised at the tracking hour, per season, against the cell truth, the retrievals, every model box in
the cell and earlier sisters' errors, and its amplitude tuned so the definition hits the target (tolerance
1e-5); the clay cells' products carry a shared AR(0.85) texture term at weight 0.83 (error correlation 0.69);
readings at four decimals. Sisters' own errors correlate under 0.0005 on their common mornings (asserted).

## Ladder

| Rung | Construction | Eight it files | Overlap | Killed by | Why a careful analyst stops here |
|---|---|---|---|---|---|
| 0 | unbiased RMSE against the morning retrieval | Kandahar, Spiritwood N + six pothole stations | 2 | s.2.1 with the Ninox accuracy note | the standard in-situ validation metric, and the satellite is what the Drought Service corrects |
| 1 | against the model, or the better-matching reference | + Avonlea W, Rokeby, Wynyard E | 5 | s.2.1 with the PLSM known limits | the model has no satellite noise; the better match looks like a fair allowance |
| 2 | against their mean, or a residual on them | + Avonlea W, Balgonie S (mean); + Balgonie S, Grand Coulee (residual on both) | 6 | s.2.1: half of each error stays | it uses all the evidence |
| 3 | triple collocation of station, retrieval and model | + Balgonie S, Grand Coulee, Regina W | 5 | the shared soil map (Ninox ancillary data, PLSM soils and known limits) | it is the field's textbook answer to rungs 0 to 2, and it matches the definition everywhere but the clay plains |
| 4 | a second station in the cell as the independent series (model only where a station is alone) | the answer | 8 | (survives) | |

**The brief answered.** Round 3's step 6 (extended triple collocation of station, Ninox v5 morning retrieval
and PLSM sw1 over 255 to 382 mornings per station) now completes and returns the rung-3 eight, three swaps
off. The hardening deepens the analysis: the products' errors co-vary only where they share an input the
providers document, and the fourth series that separates them is ordinary network data. Nothing is planted:
no filed sentence ranks, names a method or points at the clay.

**Seven survival properties.** 1 the decisive step (are the references independent here?) is written nowhere.
2 no corpus. 3 no arithmetic symptom: rung 3's figures are finite, plausible and match the definition
outside two cells. 4 not a per-row predicate. 5 its enumeration is arithmetic (a sister's covariances per
station). 6 no cutover date. 7 survives the deletion (nothing to delete).

## Determinism: the 22 axes

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 56 stations of the register | pinned (NS-03 s.1; register) |
| 2 | Unit of account | each station, sisters scored separately | pinned (s.2.1) |
| 3 | Attribution window | the overpass's local solar date, same UTC date at about 13 UTC | C1 |
| 4 | As-of dating | the current 5 cm probe | pinned (s.2.4); C1 (`ignore_probe_change`) |
| 5 | Version basis | Ninox version 5 | pinned (notes); C1 (`version4_for_2024`) |
| 6 | Divisor | n-1 against n | C1 on every three-decimal figure (`difference_notation`) |
| 7 | Weighting | pooled mornings; sisters averaged as error variances | pinned (s.2.4); C1 (first, last and mean sister give every figure) |
| 8 | Window length | three seasons | pinned (s.2.4); C1 (`last_two_seasons`) |
| 9 | Boundary inclusivity | 1 May to 30 September; 0.02 to 0.60 | pinned; no tracking reading within 0.01 of either bound (asserted) |
| 10 | Rounding path | unrounded, then three decimals | C1 (gap equal both ways, asserted) |
| 11 | Tie-break | unrounded, no ties among the top ten | C3 |
| 12 | Maturity | 2026 season closed 30 September, data to 5 October | n/a |
| 13 | Order of operations | de-duplicate and filter in either order | C1 (re-sent hours identical) |
| 14 | Row order | first or last copy | C1 |
| 15 | Duplicate resolution | an hour counts once | pinned (anchor terms); no re-sent hour on a tracking hour (asserted) |
| 16 | Identity | site codes everywhere | C1 |
| 17 | Netting | n/a | n/a |
| 18 | Dimensional units | model mm over 0 to 10 cm | C1 (`model_left_in_mm`) |
| 19 | Code semantics | bit 0 of `retrieval_qual_flag` | pinned (notes); C1 (`all_quality`) |
| 20 | Integerisation | day counts whole | n/a |
| 21 | Scope of a clause | evening overpasses make no tracking mornings | pinned (s.2.3); C1 on the eight and order (`evening`) |
| 22 | Forward window | anchors from 15 April: re-installed, under 120 days, or silent 60 days or more | pinned (anchor terms); C3: the 120-day line is at least 25 days from every station on every counting path, the silence clause takes only Aylsham (206.5 days, next 23.7), and receipt lines from 46 to 50 hours move no station's days or silence (asserted) |

Plus: which collocation (sister everywhere, sister only on the clay, quadruple, extended, covariance-corrected,
sister in the retrieval's place) is C1 on every figure; the cell by bounds and the model box by 0.1 degree box
are held clear of their edges.

## Ask sheet and ledger

Main call's rows: 5 cm logger rows at the tracking hour, 1 May to 30 September 2024 to 2026; recommended
morning v5 retrievals for the 25 cells; the model at 12 UTC; the register's Stations and Probes sheets; the
grid file. Zero-counts asserted on those rows: no re-sent hour, no failed read, no lost hour, no late row.

| Ask | Enters the call as | Answer | Device | What the wrong path does |
|---|---|---|---|---|
| The eight with their errors, the ninth, its error and the gap (docx) | the call and its flip margin | above | the decisive construction | plain collocation: three wrong stations, a wrong ninth (Watrous S), wrong figures for Pense and the clay picks |
| Anchors each zone keeps from 15 April (docx) | qualifier: what the eight leave the Drought Service's weekly correction, zone by zone | 12, 22, 9, 4 | the eight, and the anchor terms' 48-hour receipt rule with the 60-day silence clause (Aylsham's modem outage, its backlog loaded at the 28 April 2026 visit) | the plain eight takes five Dark Brown stations (22 becomes 20, Black 9 becomes 11); a receipt-blind count keeps Aylsham (Dark Gray 5) |
| Per station: tracking error, anchors from 15 April, 2025-26 delivery days (CSV, by site code) | audit trail: the error behind each station's place in the ranking and the delivery count behind each anchor flag | 56 rows | the decisive construction (the five clay-cell errors), the anchor flags, and the delivery count (UTC-6 day, 48-hour receipt, an hour once, valid range, soil above 0 °C, 20 readings) | wrong paths move delivery days: UTC days 27 stations, a 24-hour receipt cut 10, every transmission 4, frozen hours counted 56, 0 °C counted 34, more than 20 readings 35, receipt-blind only Aylsham (+21 days, then an anchor) |
| Chart (PNG) | the call, displayed | 56 bars largest first, zone colours, the ninth's line at 0.020 | inherits the call | the plain ninth's line and order |

**Pair arithmetic.** Recommendation block (the eight, order, figures, ninth, gap) about 38; instruction
following about 7; asks about 55. A response on rung 3 loses the call, the ninth and gap, three or more zone
anchor counts, the clay rows' errors and six anchor flags, and keeps the delivery days if it handles the
devices: roughly 25 to 30. A response that lands rung 4 keeps nearly everything, so the build stands on the
main ladder: the bar holds while no top response lands the second-station collocation.

## Pack gates

18 files, 6 formats (parquet, xlsx, csv, docx, md, txt); largest `coteau_sm_hourly_2024.parquet` 982,928 rows;
distractors in `metadata.json`: `ninox_l3sm_v4_2024.csv` (superseded, still lands the eight),
`hydromet_qpe_daily_2024-2026.csv`, `site_soil_survey.csv`. Deleting them, and the gauge file, changes no golden
figure (asserted). Deliverables: `reinstall_list_2027.docx`, `station_review_2027.csv`, `station_review_2027.png`.
Prompt 989 characters, 164 words, constraint-first; `voice-check.py` clean.

**Criteria arithmetic (shape 01).** The eight by name and order (9), their figures (8), the ninth, its figure
and the gap (3), anchors by zone (4), the CSV (errors, anchor flags, delivery days, site order: 4 to 6), the
chart (bars, order, colour, line, value: 5), the files (3): about 36.

## Assertion regime

`checks.py`: 388 assertions (two builds byte-identical and equal to `target/`; the eight against the
simulation's truth; every naive route and plain collocation against s.2.1; 10 rigorous estimators to three
decimals on all 56; 8 variants and 3 screens holding the eight and the ninth; the block bootstrap; sister
separation, own rain and independent own errors; the single-station cells off the clay; every logger row
received at or after its hour and by the pull; the delivery ask, its seven wrong paths, the receipt-line
corridor and the silence clause; clean-data and distractor deletion; gates; mtimes). `verify.py`: 252 checks
reading only `target/`, `golden/`, `prompt.md` and `submission.md` on an independent code path (merge-based
matching, the golden route and the sister in the retrieval's place agreeing to three decimals, the delivery
rules from the anchor terms' text, every figure in the write-up, and the house-fix checks below).

**House-fix pass** (`reduce-house-fixes`, before leak read a2-4). H16: the logger tables' receive times were
written as microseconds read as nanoseconds, so every row except the catch-up, re-sent and backlog rows carried
an `rx_time` in January 1970; `extracts.py` now puts the hourly index in nanoseconds first, and `checks.py` and
`verify.py` assert that every row is received at or after its hour and by the end of the pull's day, and that
every dated extract runs from 2024 to the pull. Only the three logger tables moved: every golden file is
byte-identical and every printed check figure is unchanged. H3: plain collocation charges Grand Coulee 0.038
(0.03846), not 0.039, corrected above. H18: the ask ledger names how each ask enters the call. H11, H19 and
H20 are wired into `verify.py` (one write-up and one prompt; every file the write-up names ships and the golden
folder holds exactly the prompt's three files; the prompt carries the subdomain's nouns and none of the
collocation terms or the anchor thresholds). H1: the metadata audit is clean on `target/` and `golden/`
(band 2019 to 11 October 2026). H4, H8, H9, H12 and H22 hold as built (no real download ships); H7 holds by
cutting `target.zip` from the final tree, compared by content.

## Realism debts

The station and product errors are orthogonalised per season at the tracking hour, so every rigorous estimator
meets the definition; nothing in the shipped bytes shows it. Pothole-cell retrieval errors of 0.052 to 0.060
m³/m³ sit at the high end of published L-band performance. The clay cells' shared texture error correlates the
two products at 0.69, at the strong end of what a common texture map produces. Leoville S, the only second
station beside the network's worst, is set at the bottom of the sound range so the ninth slot does not ride on
its noisy estimate. Sister gauges carry a local afternoon storm three or four times a season (3.5 expected) at a mean of 9.6 mm,
which the cell average and the hydromet analysis do not see; May to September totals run 141 to 393 mm (median
261), the wettest day 79 mm.

## Stopping rule

A round that commits to the golden eight by a second-station collocation is a landed call: loop 2 would deepen
the decomposition again (for example a sister pair that shares a station-scale input), never plant. A round that
files a rung-3 or lower eight passes. Three landed loops spend the architecture; this is loop 1 of 3. Round 4
was that landed call, and the sister pair sharing an input is the third independence layer ruled out at loop 2,
which spent the architecture on paper (`## Hardening loop 2, phase A`).

## Leak check (stage 4, architecture 2, loop 1)

`leak.py --asof 2026-10-09` on the final cut (after the house-fix pass): REVIEW, no LEAK. Each REVIEW line:

- `NS-03_reference_stations_rev2.docx`, 7 of 25 design-note terms (season, readings, record, mornings,
  retrieval, reference): the estimand pin (s.2.1) and the sample rules (s.2.3, s.2.4); it states what tracking
  error is and never how to estimate it, and names no product's error, no second station, no covariance.
  Harmless.
- `ninox_l3sm_v5_user_notes.md`, 5 of 25 (surface, record, retrieval, reference, product): the product's field
  list, quality rule, accuracy statement and ancillary data, the documentation a real L3 product ships; its
  soil-map sentence is the provider's own account of its clay fraction (condition 1, pin what) and says
  nothing about co-varying errors. Harmless.
- `station_register_2026-09.xlsx` names 10 of the 11 candidates beside numbers: coordinates, elevations,
  commissioning dates, logger serials; nothing in it scores a station on tracking. Harmless.
- `retrieval_qual_flag`, `surface_flag` in both Ninox extracts: the product's own documented field names.
  Harmless.

The reader read a2-4 is staged for the main session (four questions, these REVIEW lines verbatim, a fork line).

Earlier reads, kept: **a2-1** quoted a third s.2.1 sentence naming the model as the third estimate (cut);
**a2-2** found "It belongs to the station alone." pointed at the method (cut) and the 170-day delivery line
forked (moved to 120); **a2-3** (round 3) raised the ninth-slot fork, the 3-decimal ties in the CSV ranks, the
7/8 order under screens, the asks banked on a landed path and two container tells, all repaired in loop 1: the
ninth sits 1.34x above the tenth and holds under every variant, screen and 88 per cent of bootstrap draws; the
CSV is by site code with no rank column; the order holds under the open-water and evening screens; the anchor
counts now depend on the eight and on the delivery device; NS-03, the golden note and the register are
rewritten byte-level to the package Word and Excel save (Office 1980 zip stamps, double-quoted declarations,
per-document rsids and paragraph ids, Word 2013 settings and en-CA theme language, no Mac namespaces or
Japanese fonts; Excel's relationships, workbook view, styles, column widths, margins and properties), every
text run and cell asserted unchanged.

## Duplicate check (stage 5, architecture 2, loop 1)

`guard.py surface task228`: 0 of 126 pairs promoted, nearest task131 at 0.090; `guard.py heart task228`: nearest
text 0.04 (task229's stump), every ledger row at or under 0.03; the only BLOCK is the waived `ban.pattern`.
**The adjudicated pre-flight is owed**: loop 1 changed the driver (build-pipeline stage 5 re-runs it when the
driver changes), and it runs alongside the leak read.

**Pre-flight pass 5** (`clone_check_report_task228_5.md`, loop 1): no reject-tier finding. Track A none; Track B
only the author-waived `ban.pattern` G16 against task134, the same ban and not a Template, closer to task134 in
form since loop 1 (both hinge on an independence-type assumption failing in one segment) but not in claim. The card
keys the loop-1 rung honestly; its four lines still naming plain triple collocation are rewritten, and `guard.py
check` and `heart` return the same verdicts.

## Hardening loop 2, phase A (on paper)

Round 4 landed on its step 6: plain collocation of station, retrieval and model, then the same collocation with a
second station of the cell in the model's place in every multi-station cell, identical everywhere but the two clay
cells, where it adopted the station-station-retrieval triple (the golden eight, ninth Craik E, gap 0.007). The loop-2
rung had to let that step complete and still return a wrong eight, in a direction other than a third independence
layer, planting nothing.

**What the step estimates.** When the three series' errors are mutually independent, collocation's error variance for
the station is a consistent estimate of NS-03 s.2.1 over the mornings it runs on: the spread of the station's readings
about one offset and one scale on the cell truth. A generic Monte Carlo (330 mornings, 400 replications, no pack data;
`phaseA_probe.py` in the build's scratch) keeps the mean estimate within 0.0001 of that estimand for an iid error
(0.0299), a persistent AR(0.97) error, an error that grows with wetness, a station lagging the truth by a morning, a
saturating response, a sister whose probe changes offset and scale mid-sample, a sister missing a whole season, and a
third series whose own error tracks the truth (a timing offset). It misses only when two of the series share the
component (station and sister both lagging: 0.0197 against 0.0311) or when the sister's missing season is exactly the
station's worst one (0.0297 against 0.0452).

**The window (what s.2.1 to s.2.4 ask).** One standard deviation over the tracking mornings of three seasons, about one
offset and one scale: pooled collocation is exactly that, so round 4's estimator is the filed estimand. Any other reading
has to be written into s.2.1 to exist. Per-season offsets would turn on reading "the station's own offset" (data
semantics). The error the Drought Service's weekly correction inherits (the station's error in its weekly mean, which
persistence decides and collocation's variance does not show) is a new estimand: written in, it is executed by one
aggregation to anchor weeks (rule application), and about 66 anchor weeks per station against 250 to 382 mornings cannot
hold the eighth over the ninth, which holds in only 0.883 of block-bootstrap draws on mornings already.

**The sampling (which mornings exist), the strongest candidate, written out in full.**
- Stump sentence: a competent solver runs the station-sister-retrieval triple on the mornings all three share and files
  the eight it returns; the step that lands it there is reading a clay station's error off its sister's mornings, when
  s.2.4 asks for it over the station's own tracking mornings.
- Why step 6 completes and still errs: only where the sister misses mornings on which the station's own error differs
  from the rest. A stationary error leaves the common-mornings estimate unbiased (sister missing a season: 0.0300 against
  0.0299); it errs when the sister's gap is the station's worst season (0.0297 against 0.0452).
- Data-native sentence: none survives. Sisters sit at least 14.1 km apart on their own fields, rain and loggers, so a
  sister's outage and the other station's bad season share no cause; the coincidence would be authored.
- Analyst test: fails. A strong analyst who runs the triple on the common mornings is right whenever the error is
  stationary, and nothing in the records says it is not; the rung would trip only this solver's sentence.
- Rigorous variants: they do not converge. Over the clay plains the only series on the sister's missing mornings are the
  retrieval and the model, which share the soil map's texture, so the station's error there needs the retrieval-model
  error covariance carried across seasons (a stationarity assumption) or a third station: back to independence.
- Pin: none that fixes what without a withheld rule; the convergence would have to be planted.

**The error's properties (what the identity does not separate).** Persistence, wetness-dependent spread, a lag behind the
truth, a saturating response and a reference's own breaks leave collocation on the estimand while the references are
independent, so none can carry a rung. What biases it is a component two series share: the 5 cm lag behind the 0 to 5 cm
truth, which the sister shares; a nonlinearity common to probes in heavy clay; a sub-cell signal on the clay plain. Each
is the third independence layer, and the shared lag is not even identifiable from the pack (no second 0 to 5 cm series
besides the retrieval). Separating what a re-installation fixes (the probe) from what it cannot (the plot's place in the
cell) needs a co-located fifth series and moves s.3.1's ranking basis.

**Verdict: SPENT.** No loop-2 rung exists without another independence layer, an authored coincidence in the records (a
plant), or a new filed estimand a reader of pins executes. Architecture 2 is spent at hardening loop 2; the re-root to
architecture 3, task228's last, waits for the main session (`pipeline.json`).

## Architecture 3, phase A (on paper)

The re-root kept the world (56 stations, the register, the field visits, the logger feeds, the delivery record), the
requester's role (head of the network data office) and the objective (a forward monitoring or alerting call on the
network's data). The draw had to clear three fences at once.

- **The guard window.** A card drawn on 2026-10-11 as task228 sorts after task133, task134 and task135, so decisive G9,
  G16 and G17 are banned (`ban.pattern`), as are stated_rule_hard_construction and maturity_censoring, shapes 07 and 14,
  and those builds' roles, artifacts, forums, events and organisations. The slot's lineage blocks (population, G6 or E)
  on pick_one_of_n or signal_vs_noise_or_hold, and (objective, G16) on ranked_slate_under_cap or
  method_or_model_selection.
- **The spent list.** Collocation and comparator independence (any shared-error or errors-in-variables layer),
  regression to the mean and shrinkage of unit rates (raw rates over unequal exposure included), repeated looks and serial
  correlation in an alert threshold, clustered errors, late-arrival maturity, competing exits, selection into
  observation, the comparison pool in a staggered switch, and the seeds task231, task235 and task248 to task252.
- **The three rules.** The decisive step is analysis the field would recognise, so it survives the swap test and is
  neither a field reading nor a stated rule.

**Where that leaves this world.**
1. Every estimator-choice stump the measurement record supports (which estimate of a station's error, noise, temperature
   sensitivity or wear the data can carry) is honestly keyed G16 method selection, which `ban.pattern` blocks against
   task134. Architecture 2's waiver does not extend to it.
2. The anchor terms define delivery completely: 48-hour receipt, one delivery per hour, the valid range and temperature,
   20 valid readings per Saskatchewan day, 120 days, the 60-day silence and two anchors per zone. A stump on the delivery
   record is rule application. Its forward forms (2026-27 countable days, the delivery a call-out could recover) are a
   replay a solver runs on the record, or a lens swap from lost days to recoverable days.
3. The decision-structure keys still open (pattern A, pattern C, G1, G7, G11 and G13) need a domain quantity that no
   rule files. Here they reduce to crew reach, logger memory and upload arithmetic, which read the same for any
   telemetry fleet (the swap test fails), or to the exposure-clock driver that task46 already carries.

**Candidate 1, the frost clock (closest).** The call: which stations' 5 cm probes the crew swaps from the spare SP-3
stock at the spring 2027 visits, most likely to fail in the 2027 season first. The data-native sentence: frost jacking
ratchets a shallow probe loose with each freeze-thaw cycle at its depth. The bare, chinook-swept southwest cycles dozens
of times a winter, while the snow-insulated north freezes once, so neither register age nor the length of the frozen
season measures wear. Only each station's own 5 cm temperature record counts it. The textbook move, probe survival on
register age with the surviving probes censored (or on frozen-season length), completes and lands on the oldest
northern SP-2 probes. It fails for four reasons:
- Its driver is task46's: a rate law stationary in cumulative service exposure, under which register-age and trailing
  routes miss the cohort crossing a step. The draft card returns BLOCK `test.same_driver_older` on (time, A,
  forecasting), a signature spent in seven builds, and an honest differentiation line would call it the same move.
- Narrowed to "cycles, not frozen duration", the decisive step becomes an exposure-metric choice, keyed G16 and banned.
- The probe-failure history is a sweepable corpus. A solver that fits more than one frost metric sees failures cluster
  on cumulative cycles. A history built blind to the metric leaves frozen duration (the field's freezing index) equally
  defensible, so stump power and determinism cannot both hold.
- The call reads as a failure forecast, which risks a Forecasting retag.

**Candidate 2, the reversible part of the diurnal swing.** The call: which stations' dawn readings the network holds
from the 2027 anchor feed, because their 5 cm probe carries a soil-temperature artifact that peaks at the 06:00 overpass,
the daily temperature minimum. The textbook move, regressing the reading on soil temperature over rain-free days,
completes and charges daytime evaporative drying, which tracks warming, to the probe. It fails for three reasons:
- The decisive step is an identification choice (which hours identify the sensitivity), keyed G16. The draft card
  returns BLOCK `ban.pattern` against task134 and BLOCK `test.own_lineage` against architecture 2's (objective, G16,
  method_or_model_selection).
- It is not deterministic. Nights are not still either: upward redistribution and condensation move water, and the
  artifact's sign turns on clay-bound water. Night-only, evening-fall and radiation-proxy estimates therefore disagree at
  any tolerance worth filing.
- The artifact is an authored per-probe property, with no record a network keeps that would make its tolerance natural.

**Persona.** The requester's role stands. Both drafts also return BLOCK `people.first`, because the requester's first
name (Michael) sits in task130 inside the last twelve. A further draw keeps the role and redraws the name with
`guard.py names --geo "Canada, Saskatchewan" --seed 228`.

**Verdict: NO ARCHITECTURE.** No Layer 2 pitfall in this world is analytical, domain-native, outside the spent list and
clear of the guard. Neither candidate is rescued by a waiver alone: candidate 1 also repeats task46's driver and cannot
hold stump power and determinism together, and candidate 2 is not deterministic. Retiring task228 is the author's call.
The phase A drafts were checked in scratch and never registered; the card on file is still architecture 2's.

## Architecture 4, phase A (on paper)

**The exception.** On 2026-10-11 the author granted task228 a fourth architecture as an exception to the
three-architecture cap: a fresh dataset and domain, nothing kept from the experiment platform or the Coteau
network, the objective kept (a forward monitoring or alerting call on the health of the data or the pipeline
that delivers it), and the number retired if no draw clears. Phase A ran on main at 3966e83 after merging
PR #39 (determinism is literal) and PR #43 (methodology-first stumping, `precut.py`), with task182 newly on
file. Architecture 2's generator, metadata, prompt, write-up and leak report were removed first.

**The fences the draw had to clear at once.**
- **The guard window** is now task135, task181 and task182. Decisive G12 (task181), G16 (task182) and G17
  (task135) are banned by `ban.pattern`, as are the strategies `decomposition_attribution` and
  `maturity_censoring`, the forums `executive_team`, `operations_desk` and `regulator_or_inspector`, the
  forcing events `incident_or_complaint`, `shift_or_daily_cycle` and `statutory_or_regulatory_filing`, the
  organisation families `hospital_or_health_provider` and `cooperative_or_member_body`, the artifacts
  `register`, `filed_standard` and `published_series`, the roles `operations_director` and
  `field_unit_lead`, shapes 11 and 17, and the calibration form `censored_or_lagged_release`.
- **The two draws that must clear this card.** task230 architecture 2 (Human Factors, shape 07, pattern A
  decisive, signal detection's low-prevalence effect on human verification, `compliance_or_audit`,
  `operations_log`, `committee_or_panel`, `purchase_order_or_contract`, `professional_services`) and task229
  architecture 2 (General Statistics, the missing-data task type, pick-face stock-record accuracy decided by
  the stock-control field's count-reset logic). A draw that blocks either sends that build back to its draw.
- **The brief's spent and taken list.** Repeated looks; conditioning on a run attribute and reweighting to a
  season's mix; collocation, comparator independence and errors in variables; regression to the mean and
  shrinkage; late-arrival maturity; selection into observation; comparison pools in a staggered switch;
  clustered errors over shared parents; competing exits as censoring; transport; and the seeds task231 to
  task252 (DQ04 to DQ25), which spread this objective's seed worlds across laboratory feeds, registers,
  survey pipelines and sensor networks.
- **The new spec.** The estimand filed literally and the method open only behind a filed criterion the data
  settles; the default competent path written and ending on a wrong answer; the decisive rung silent on all
  six readability tests; no semantic fork; `precut.py` exit 0.

**What the fences leave.** In almost every field, the field's own method for a data-health quantity is an
estimator of that quantity, and honestly keyed that is G16 (which estimate the data supports, banned through
task182) or G12 (whether a missing record means nothing happened, banned through task181). The forms that
are not estimator choices are constructions of the unit or population the call is scored on. In this
objective those are either readable from the schema or completeness estimates (the chance a record is
captured), which sit beside the taken selection draw. The forward forms (a data-health quantity generated by
a process the closed window never saw) are task230's pattern A or the spent maturity, transport and
season-mix drivers. Two candidates came closest.

**Candidate 1 (closest): exit-validator capture at a light-rail operator** (Urban & Regional Science, task
type other; drafted in the Netherlands). The call: which stations' exit-validator banks go on the 2027
replacement list, ranked on the share of alightings whose check-out the validators fail to record. The fare
system logs an incomplete journey against its check-in station, but the failure belongs to the alighting
station, which only the card's next check-in shows (for the day's last journey, the day's first check-in).
That is the transit planner's trip-chaining inference (Barry 2002, Trépanier 2007), and the generic move
(each station's check-ins against its check-outs) completes and lands on the one-way interchange and
park-and-ride stations. It fails three ways:
- **Readability, test 2, and the default path.** The card key and the tap times make the alighting station a
  self-join found by inspecting headers, and chaining is the sequence move a competent analyst makes the
  moment the origin attribution is seen to be wrong, so the honest default path (stumping Part 1.5) ends on
  the golden. Removing the card key removes the field's method with it.
- **The domain test.** "The next entry shows where the previous exit was" reads the same for library returns
  or ward transfers. Only the tour-closure and walking-distance rules are transit's own, and they are
  refinements a chaining solver adds unprompted.
- **The estimand** is a capture rate (the share of exits the system records), the chance-of-being-counted
  family architecture 3 left reserved, which sits beside task229's selection draw.
Its draft card (keyed G3, gap population, strategy `grain_or_unit`) drew two BLOCKs a design could answer,
`card` (`client_domain` empty) and `test.same_driver_older` against task101 and task121 v2 (answerable by a
differentiation entry), and three WARNs: `three_rules.strategy_risk`, `overuse.org_family` and
`repeat.gate_g` against task182. Nearest driver text 0.05 (task66, task126, task104, task50).

**Candidate 2: oldest-old register over-coverage** (Sociology & Demography, life-table estimation; drafted
in Sweden). The call: which regions' registered population aged 90 and over the 2027 life tables replace
with reconstructed survivors, because the register keeps residents whose deaths abroad were never recorded.
The field's method is the extinct-generation and survivor-ratio reconstruction from deaths by year of birth;
the generic move (each region's 90+ death rate standardised against the national schedule) flags the
long-lived regions. It fails four ways:
- **The guard.** Honestly keyed it is G12 (whether a missing death record means the resident is alive) or
  G16 (which estimator of the living count), BLOCK `ban.pattern` against task181 or task182. The draft,
  keyed G12, also drew BLOCK `ban.forum` (`executive_team` against task182) and BLOCK `card`
  (`client_domain` empty), both fixable, and WARNs `overuse.org_family` and `repeat.decision` against
  task182. Nearest driver text 0.09 (task91, task133).
- **Readability and the default path.** For "how many of the registered 90+ are alive", a demography-literate
  solver's default is the survivor-ratio method itself (the Human Mortality Database's protocol), which is
  the golden. The one refinement that could separate them, the cohort's recorded emigrations added to its
  exits, is the cohort-balancing reflex, and the excess is one subtraction from a cohort sum (tests 5 and 6).
- **Gate G.** Over-coverage is a coverage-gap defect on the judge's `planted_defect_flip` list, and the
  instrument repair (a register that records every death abroad) collapses the call.
- **The seeds.** DQ16 (task243's seed: a register coverage alert by local area) shares the surface.

**Other worlds screened, each dead in one line:**
- Evaluated bond prices' information age (Quantitative Finance): a frozen spread shows at once in a
  regression of price changes on the matched Treasury move, so the field's curve-and-spread decomposition
  is a generic factor regression, and lagged-beta staleness is the same move.
- Imprecision at a clinical decision limit (high-sensitivity troponin rule-out): the estimand names the
  concentration (test 1), extrapolating a precision profile below the QC levels forks between variance
  models, and it ranks measuring units by random error again, architecture 2's dimension.
- Careless responding in panel suppliers' data (Psychology): reversed-item checks and Mahalanobis distance
  catch the acquiescent pattern, and the task type's library patterns are seeds DQ10 to DQ12.
- Case-reserve adequacy against settlement speed (Actuarial, Berquist-Sherman): two dated changes an
  alignment of diagonals finds, and the mix repair is a stratification by claim size (test 3).
- Selective editing of survey returns (Official Statistics): the weighted-impact score is the field's
  textbook move, and what remains (impact relative to each published cell, expected amendment by edit type)
  is a filed rule or conditioning on a visible attribute.
- Carry-forward imputation in a price index: recomputing under class-mean imputation is the obvious move once
  the bias is named; rule application.
- Adverse-event under-reporting at trial sites against a front-loaded hazard: the visit-matched comparison is
  a stratification by time on study (test 3).
- Human detection of seeded errors by signal detection theory: task230 architecture 2's pitfall.
- Potassium leak in cold specimen transport: a rate law in cumulative cold exposure, task46's driver.
- A smart meter's clock offset aligned to solar noon: an estimator choice (G16) in task229 architecture 1's
  smart-meter world.
- Broker execution timestamps checked against trade prints or quotes: the deciding fact (consolidated prints
  carry report times) is a field reading.
- Item compromise in a computer-adaptive bank: the purified ability is an independent comparator,
  architecture 2's spent independence move.

**Verdict: NO ARCHITECTURE.** No Layer 2 pitfall in a fresh domain is the field's own method, silent on the
readability screen, off the default path, keyed to a code the window allows, outside the spent and taken
list and clear of task229's and task230's draws. The author paused the number instead of retiring it
(`## Paused`).
Nothing was registered, so the card on file is still architecture 2's, and task229 and task230 clear the
card they already planned against. The two draft cards are in scratch
(`/home/user/orch/buildwork-task228/arch4/`) and were never registered.

## Tried and rejected

- Verification bias as the decisive rung (tracker labels against the audit): rejected at the draw,
  because it is the incompleteness of a filtered record, so it collapses under the instrument repair
  (every experiment labelled) and the judge would read `sole_data_defect: yes`; kept as rung 0 only.
- The seed's shortcut (largest percent movement across incidents) as rung 0: rejected, because the
  movement has no single computation a reviewer could reproduce across checks in five different units.
- Detection at any time during the run: rejected as the catch rule, because cumulative checks then
  catch every launch-night defect eventually and the run-length move cannot flip the call; the filed
  window (onset night and two after) is what an on-call desk acts on.
- Drawing the 28-night runs' bot bursts at random: the four-week page count rode on sampling luck
  (5 to 9 of 125 at one setting across seeds); the run maximum is now placed on stratified quantiles of
  its law per run length.
- `test.same_puzzle` against task122 with gap time first: redrawn to population first, which is the
  honest reading (the runs the record holds are not the runs the season books).
- **Architecture 1, round 1 (hardening loop 1 opened).** Plain 50.4, missed: it stopped at rung 1
  (evpu_dev_pct at 12, 29 of 68 on all 452 sound runs) and never weighed run length; its path reads the
  budget as "at most 1 in 20 sound experiments paged on any night of the run, read off the full audit year"
  with no word on the season. Skeptic 97.6, landed, on its step 7: "Peak runs are all 28 nights (handbook
  6.2), and the budget applies over the season the setting is live. So sound runs were counted on the 123
  sound 28-night audit experiments from all four quarters." It executed rung 2 as a work order and called it
  a judgement in its notes, so the clause pair (DQ-07 s.4 with handbook s.6.2) is a pin a reader of pins
  takes, not a fork. Both cracked Ask B and Ask C: the prompt itself named each device's handling ("by
  quarter of the night it paged for", "under the squad owning the surface on the launch night"), the
  tracker JSON's `imported_from` pointed at every migration duplicate, the skeptic reproduced all 58 alert
  tickets from Vigia, and the queue's status column announced its versions. Mean 74, gate failed.
- **Architecture 1, round 2 (passed under the rule change).** Plain 48.9 and skeptic 47.5, both off the
  call at rung 2 of that cut: "Peak runs are 28 nights, so I read the page budget on the 166 sound
  audited experiments that ran 28 nights" (plain); "The peak budget is therefore read on 28-night runs"
  (skeptic). Neither split the season by surface. Both reproduced the incumbent's record by quarter and
  the routing; on peak coverage they split on BK27-103 and BK27-129 (plain 43, skeptic 42), a fork now
  pinned. Under the old gate the asks failed it (mean 48.2); under the gate of 11 October the round
  passes.
- **The season's surface mix as the decisive rung** (loop 1): each surface's sound four-week page rate
  weighted by the queue's standing tests on that surface, with app tests' release-spanning batches as
  the physics. Pre-flight pass 2 keyed it `composition_mix` (a reweighting changes the comparison), which
  `ban.strategy` blocks against task129 three draws back. Retired with the app physics at the
  strategy-axis redraw; the queue stays for the coverage ask.
- **Set aside at the redraw:** a catch-side rung (only the defects a frozen test can suffer count) makes
  the asked catch counts ambiguous between last year's defects and the peak's; unequal splits move only
  the percentage checks, while the z and p-value checks are normalised against them, so the call cannot
  flip; a peak with no app tests puts a zero weight on one surface, which is the same reweighting; a
  revision effect on the assignment ratio would fill the incumbent's tracker with revision-night false
  alarms that differ by season; a freeze in last winter's record would make the quarters themselves
  announce the move.
- **Architecture 1 spent, re-rooted (2026-10-11).** The peak paging-alert check-and-setting call on the experiment platform: its decisive rung was redrawn twice to get past guard bans and, keyed honestly, is composition_mix (round 2) and then pattern E with G14 decisive (the redraw, clone_check_report_task228_3.md), both BLOCK against task129; round 2 passed the solver gate, but a fork stayed open (dropping only the nights after a configuration revision gives beacon_loss_z about 2.9, dropping revised runs whole gives 3.0). Architecture 2 re-roots at stage 1 in the same objective and number with a new card; architecture 1's identity is kept in the card's lineage.
- **Architecture 2: errors drawn independently with no orthogonalisation.** Triple collocation's sampling
  noise in the pothole cells (product errors near 0.05) moved the estimate up to 0.017 off the definition
  and the definition's own eight differed from the estimator's; the errors are now orthogonalised on the
  tracking mornings.
- **Architecture 2: orthogonalised over the pooled sample only.** The probe-change stations' two-season
  samples drifted (Rokeby 0.0075 off the definition); orthogonalising within each season keeps every union
  of whole seasons exact.
- **Architecture 2: station scale 0.88 to 1.18.** The unscaled-difference variant closed to 0.0348 against
  0.0331 at the cut; narrowed to 0.84 to 1.06.
- **Architecture 2: pothole product errors 0.045 to 0.052 (retrieval) and 0.040 to 0.047 (model).** The
  mean-of-references route reached 7 of the eight; raised to 0.052 to 0.060 and 0.046 to 0.054, now 4.
- **Architecture 2: readings clipped at the probe floor on tracking mornings** (Swift Current E, eight
  mornings at 0.005): the 0.02 validity filter dropped them and moved the figure by 0.0006, across a
  rounding edge; the tracking sample is now held inside 0.03 to 0.565 by construction.
- **Architecture 2: a PM retrieval-error ask** (each cell's evening retrieval error): dropped, because
  asking for a product's own error hands the solver the decomposition.
- **Architecture 2: the delivery statement as a stand-alone report.** It read as a second decision in the
  note (H18); the anchor terms now carry a delivery line (170 days) that decides which stations sit out,
  so the statement feeds the anchor count.
- **Architecture 2: NS-03 s.2.3 as "each morning retrieval is paired with the station's reading".** A
  ranking by agreement with the retrieval literally satisfied it; rewritten as a sampling rule, and s.2.1
  now states that the products' errors are not the station's.
- **Architecture 2: NS-03 s.2.1's third sentence** ("the Ninox retrieval and the Hydromet model both
  estimate it, each with errors of its own, and those errors are not part of any station's tracking
  error"): the leak reader read it as the decisive step, named the model as the third estimate and ran the
  separation from it; dropped, so the standard pins what is measured and never how a reference's error is
  separated.
- **Architecture 2: the drought service as "Prairie Drought Watch"**: its distinctive words are a real
  federal drought programme's name; renamed Prairie Drought Service before the first leak read.
- **Architecture 2: the decisive generator keyed G3** (record versus operation): pre-flight pass 4 found the
  pack carries no record that charges the error to anyone; re-keyed G16 (method selection), with the
  `ban.pattern` against task134 waived by the author.
- **Architecture 2: the requester as the network lead (field_unit_lead)**: `ban.role` against task135, which
  reached main after this draw; the author chose a persona change, so the requester heads the network's data
  office.
- **Architecture 2: "It belongs to the station alone." in NS-03 s.2.1**: reader a2-2 read it as pointing at the
  method; cut, the estimand stays fixed by "the station's own random error".
- **Architecture 2: a delivery line of 170 days in the anchor terms**: Star City (169) and Nipawin W (171) sat on
  it, so the anchors each zone keeps forked on counting conventions; the line is 120 days, which no kept
  station comes within 45 days of.
- **Architecture 2, round 3 (hardening loop 1 opened): triple collocation of station, retrieval and model as the
  decisive rung.** Landed on the solver's step 6, verbatim: "Error formula σ² = Cxx − Cxy·Cxz/Cyz on station, Ninox and
  PLSM over 255 to 382 mornings per station gives top eight CS187 0.0479, CS108 0.0450, CS133 0.0421, CS118 0.0399, CS182
  0.0381, CS121 0.0369, CS148 0.0351, CS173 0.0340; ninth CS160 0.0241; gap 0.0099 rounds to 0.010; result identical with
  ±0.5 h and ±1 h match limits". The rung is now plain collocation, wrong over the clay plains where both products take
  texture from one soil map; the sister station in the model's place recovers the eight.
- **Loop 1: station readings at three decimals, model water at 0.1 mm, probe white noise left as drawn.** The rounding
  and the 0.0003 noise left covariances of about 1e-6 with every series, which moved low-error stations by up to 0.0002
  between rigorous estimators (a three-decimal fork); readings now carry four decimals, sw1_mm two, and the noise is made
  orthogonal at the tracking hour.
- **Loop 1: product values clipped on tracking mornings** (pothole and clay retrievals at 0.6, models at 0.55): biased
  collocation by up to 0.0003 against the definition; each cell's offset (and scale if needed) is now moved so no
  tracking-morning value clips.
- **Loop 1: Kandahar mid-list.** A 2 per cent open-water screen keeps only drier pothole mornings, where its
  wetness-scaled error is smaller, and drops its estimate 12 per cent, swapping it with the station below; it is now eighth.
- **Loop 1: Spiritwood N seventh.** The evening pass (excluded by NS-03 s.2.3) shrinks the parkland station's estimate
  about 4 per cent against 17 to 19 for the open stations and swapped it with Melfort N; it now heads the list.
- **Loop 1: a day-count delivery line carried by an off-season backlog.** The delivery year's months outside the
  tracking season hold only about 20 countable days, too few to move a station across any line with margin on both
  sides; the backlog now trips the anchor terms' 60-day silence clause instead.
- **Loop 1: "Readings recovered later from a logger's memory ... are not delivered" in the anchor terms.** It announced
  the device's population; cut, the 48-hour receipt rule alone decides it.
- **Loop 1: local afternoon storms at a 2.4 mm mean.** Sister gauges correlated 0.978 to 0.998 on daily totals
  and showed 0 or 1 days of their own storms in three seasons, so the pack could not show that a second station
  has its own rain; storm amounts are now four times larger and the soil wet-up per millimetre four times
  smaller, which leaves every station reading byte-identical and the sister gauges at 0.73 to 0.96.
- **Loop 1: Leoville S at the top of the sound range (0.0132).** Its only second station is Spiritwood N, the
  network's worst, so its estimate swung (bootstrap SD 0.0085) and took the ninth slot in 39 of 200 draws (the
  ninth held 0.755); drawn as usual and then set at 0.00688, the ninth holds in 0.883 of 300 draws.
- **Loop 1: asserting that no reading arrives within two hours of the 48-hour line.** Aylsham's backlog dump
  carries its last two days, so its lags run through 48 hours by nature; the assertion is now the corridor
  (receipt lines from 46 to 50 hours move no station's countable days and no silence verdict).
- **Architecture 2 spent at hardening loop 2, phase A (2026-10-11).** Round 4 landed the golden eight on its own
  independence check (a second station of the cell in every multi-station cell, the station-station-retrieval triple
  adopted over the two clay cells). On paper no loop-2 rung survives: with independent references collocation stays on
  NS-03 s.2.1 under persistence, wetness-dependent spread, lag, saturation and reference breaks (a generic Monte Carlo,
  within 0.0001); it errs only on a component two series share (the third independence layer ruled out) or on a sister
  gap authored to fall on the station's worst season (tuning to the solver); and a weekly-anchor or per-season window is
  a new filed estimand a reader of pins executes. Re-root pending: architecture 3, the number's last
  (`## Hardening loop 2, phase A`).
- **Architecture 3, phase A: the frost clock** (spring probe swaps ranked on wear from freeze-thaw cycles at 5 cm, not
  register age or frozen-season length). Rejected for four reasons. It repeats task46's driver (a rate law stationary in
  cumulative service exposure), and its draft card returns BLOCK `test.same_driver_older` on (time, A, forecasting).
  Narrowed to "cycles, not duration", it becomes a G16 metric choice, which is banned against task134. The probe-failure
  history is a sweepable corpus that nominates the metric, and a history built blind to it leaves frozen duration
  equally defensible. And the call reads as a failure forecast.
- **Architecture 3, phase A: the reversible diurnal swing** (dawn readings held where a probe's soil-temperature artifact
  peaks at the 06:00 overpass, identified on nights). Rejected because it is a G16 identification choice: BLOCK
  `ban.pattern` against task134 and BLOCK `test.own_lineage` against architecture 2. It is also not deterministic:
  redistribution and condensation move water at night, so the night, evening-fall and radiation-proxy estimates
  disagree at the tolerance.
- **Architecture 3, phase A: stumps on the delivery record** (2026-27 countable days, the 20-of-24 day threshold, the
  48-hour line, the 60-day silence, the delivery an in-season call-out could recover). Rejected because the anchor terms
  define delivery completely, which makes each of these rule application. The forward forms are a replay of the record
  or a lens swap from lost days to recoverable days, and the call-out forms read the same for any telemetry fleet.
- **Architecture 3, phase A: the remaining statistical forms.**
  - Probe noise as the variogram nugget against first differences: a G16 choice and generic signal processing.
  - A QC flag's prevalence corrected for sensitivity and specificity, or a hold rule's predictive value at the 2027 fault
    rate: textbook moves on visit-selected labels (selection into observation, reserved).
  - A dual-system count of undetected faults, and faults per check run: chance of being counted (reserved).
  - Gap-fill validation on random holdouts: the autocorrelation family (spent).
  - The treatment paradox (call-outs shortened the attended stations' losses): confounding with no domain physics
    (the swap test fails).
- **Architecture 3, phase A: defect hunts and lineage repeats.**
  - Logger clock drift, frost-heaved probe depth from thermal damping, and thermistor offsets from the zero curtain:
    each is a defect to catch (`sole_data_defect` yes) or cannot be identified without a third depth.
  - A forward probe, logger or wetness mix: architecture 1's season-mix driver, re-skinned.
  - Pit settling after re-installation that runs on wetting cycles: an authored law that aligns to the install date,
    so an event study solves it.
- **Architecture 1 revival, phase A (2026-10-11, at the author's decision): not revivable.** Its decisive step, the sound
  four-week runs split on `config_rev` and the budget held on the 106 unrevised ones because no revision crosses the
  change freeze, is a generic correction stumping Part 2 names as spent (stratify by a visible attribute), as the rung it
  replaced was (reweight, the season's surface mix). The field's own move in this world, a per-run false-alarm rate that
  grows with the nights a run is checked, sits a rung lower and was executed by the round 1 skeptic and both round 2
  solvers; a generalist reaches the revision split without knowing what a revision does to a check, so no honest
  `domain_test` can be written, and the noun swap leaves the step unchanged (a line alarm calibrated for a production
  freeze, recipe changes as the revisions). It is also proven-in-production's dead "forward population named by a filed
  clause" (the freeze sits in handbook s.6.1 directly above the 28-night clause in s.6.2, and the class is a labelled
  column) and pattern E's own signpost case. Round 2 is no evidence for it: that cut had no `config_rev`, its golden was
  the exposure gap at 3.5 by surface-mix reweighting, and the redrawn cut never met a solver; the one cold read of it
  (leak read 3) rebuilt the split from the freeze clause and the column alone and named beacon_loss_z at about 2.9, or 3.0
  with revised runs dropped whole. Of the guard's blocks, `stump_class`, `analyst_test` and `test.same_puzzle_older`
  (task28, task30, task32, task53) could take honest entries; `domain_test` could not.
- **Architecture 4, phase A (2026-10-11, the author's exception to the cap): no architecture; the author paused the number.**
  - Exit-validator check-out capture at a light-rail operator, by trip chaining: the card key and the tap times make the
    alighting station a self-join read off the headers (readability test 2); chaining is the sequence move a competent
    analyst makes once the origin attribution is seen to be wrong, so the default path ends on the golden; the swap test
    leaves the step unchanged (library returns, ward transfers); and a capture rate is the chance-of-being-counted family.
  - Oldest-old register over-coverage by extinct-generation and survivor-ratio reconstruction: honestly G12 or G16 (BLOCK
    `ban.pattern` against task181 and task182); the survivor-ratio method is a demography-literate solver's default and
    the golden at once; over-coverage is a coverage-gap defect on Gate G's flip list; and DQ16 holds the surface.
  - Evaluated bond prices' information age: a frozen spread shows in one regression on the matched Treasury move, a
    generic factor regression.
  - Imprecision at a clinical decision limit: the estimand names the concentration (test 1), extrapolating the precision
    profile forks between variance models, and units ranked by random error repeat architecture 2's dimension.
  - Careless responding in panel suppliers' data: reversed-item checks and Mahalanobis distance are the textbook catch,
    and the seeds DQ10 to DQ12 hold the task type's patterns.
  - Case reserves against settlement speed (Berquist-Sherman): dated changes an alignment of diagonals finds, and the mix
    repair is a stratification by claim size.
  - Selective editing of survey returns: the weighted-impact score is the textbook move, and what remains is a filed rule
    or a split on a visible attribute.
  - Carry-forward imputation in a price index: rule application once the bias is named.
  - Adverse-event under-reporting against a front-loaded hazard: a stratification by time on study.
  - Taken or spent: human detection by signal detection theory (task230 architecture 2), potassium leak in cold transport
    (task46's driver), a smart meter's clock against solar noon (G16, task229 architecture 1's world), broker timestamps
    against trade prints (a field reading), and item compromise in an adaptive bank (an independent comparator,
    architecture 2's move).

## Paused

The author paused task228 on 2026-10-11 after architecture 4 drew no architecture. It is out of the build
slots. Once task229 or task230 ships, a designer at Opus max redraws architecture 4: under a waiver of the
estimator-pattern ban (G12 and G16, held by task181, task182, task445 and task446 in the draw window) if the
author grants one then, or without one if the window has moved. Every candidate already screened is under
`## Architecture 4, phase A` and `## Tried and rejected`.
