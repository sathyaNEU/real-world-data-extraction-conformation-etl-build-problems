# task185 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task185.json`, architecture v1, drawn 2026-10-12 from seed AD08 (a
  heat-index cover priced off one weather station with a break). The world, the decision and the quantity are the
  seed's; the pitfall is re-found from the station record.
- **Pairing:** General Statistics & Data Science, exploratory data analysis and distribution assessment (primary;
  the task type serves Anomaly Detection & Diagnostics in the taxonomy). Secondary domain Physical & Environmental
  Sciences, whose own Layer 1 technique (station histories with moves and instrument swaps, documented in station
  metadata) supplies the record's mess. Objective: Anomaly Detection & Diagnostics, a real event (the warming in the
  station's heat days) separated from an artifact (the 1995 change of instrument and screen).
- **Niche:** Southward Mutual, an agricultural mutual insurer, quotes Merrin Valley Winegrowers Co-operative its
  vineyard heat-day cover for the 2027/28 season. The cover pays per hectare on the days from 1 December to the last
  day of February whose maximum at Merrin Flat reaches 35.0 C (heat days, after a deductible) and 40.0 C (severe
  heat days). Merrin Flat went automatic on 1 November 1995: an electronic probe in a small plastic shield replaced
  the glass maximum thermometer in the large wooden screen, and the glass was read beside it until 30 April 1998.
- **Forcing and forum:** the co-operative's cover renews on 1 November 2027 and the quote is due to it first
  (`purchase_order_or_contract`, `customer_or_counterparty`); the organisation is a `financial_institution`; the
  stakeholder is the mutual's weather portfolio manager (`portfolio_manager`).
- **Call:** the premium per hectare for the 2027/28 season, with the season's expected heat days and severe heat
  days on the present instrument's basis.
- **Shape 08** (rule replayed on history: each period's cells). The cover's terms replayed season by season are the
  burn the premium is built from, and the broker's exhibit of the recent seasons is the replay the asks grade.
  Criteria arithmetic (provisional, fixed at the ask sheet): the call and its two expected counts (3), the critical
  components (glass-era days the present probe would have counted over each trigger, the heat-day trend per decade
  on the present basis: 3), the replayed seasons (10 seasons by heat days, severe days and payout: 30), the chart's
  named parts (4), the files (2): about 42.
- **Strategy and mechanism:** `population_selection` (the conversion estimated on the days like the one being
  converted, not on all days); gap rule over population (the manual's basis, each past day as the present instrument
  would have recorded it, selects a conversion sized at each reading once the paired readings show the difference
  grows with the reading); G16 then G14; Gate G `method_or_model_selection`; calibration `parallel_run_overlap` (the
  station's own two and a half summers of paired readings and the network's comparison programme at other sites).
- **Data-native sentence:** the small shield heats on still, sunny afternoons, so the probe reads the same as the
  glass on ordinary days and runs warmer only on the hot ones, and the glass register was kept to the half degree, so
  the change is invisible in the mean, invisible against neighbours that changed in the same rollout, and invisible to
  any single offset: only a conversion sized at each reading carries the 34.5 C days over 35.0 C and the 39.0 C days
  over 40.0 C while leaving the 34.0 C and 38.5 C days where they were.
- **Mechanisms read** (`guard.py mechanisms --objective anomaly-detection`, 17 builds): 25 and 28 a second-source
  inflow and a reachable share; 33 forward yield cut by an intervention; 48 a two-sided grain; 54 exposure while in
  custody; 68 a matched panel through identity successions; 76 a look-back class with zero conversion; 85 a unit's own
  observation window; 103 a fan-out through authorisations; 104 a self-adapting scorer replayed at another setting;
  119 waits a unit could shorten; 182 a lagged response to a shared driver; 183 repeat failers in parts; 125 a
  recruitment filter's carried difference; 180 detection by the quiet hours; 181 crossings of moving units; 184 host
  stand-down crowd-out. None sizes an instrument change by the reading, none turns on a threshold count whose trend a
  changeover step inflates.
- **Guard:** WARN `overuse.objective` (Anomaly Detection in 4 of the last 12): the lane is Anomaly Detection, and the
  mechanism, domain and shape are each new to it (General Statistics & Data Science has never carried an Anomaly
  Detection build; shape 08 is not in the last 12). The older signature (gap rule, G16, quantity figure) is task80 v2
  only, differentiated on the card: a time rule executed over records there, a distributional estimate here.
- **Sources:** the seed (AD08) gives the world and decision, its hold-on-tolerance design is not used (a filed
  tolerance applied to a size is rule application); the client's distribution-assessment techniques (outliers on the
  right scale, stratify before a correlation) teach that the distribution's shape, not its centre, decides, and this
  build moves that to a paired-instrument difference whose shape is reading-dependent; the client's Physical &
  Environmental Sciences technique 1 (station histories, changes documented as real networks do, never hidden to make
  a step) sets the rule that the change is documented and only its size at the reading is the analysis.

## Default path

1. Read the pricing manual: the record is Merrin Flat's daily maximum from the 1965/66 season to 2026/27, each day as
   the present instrument would have recorded it; heat and severe heat days counted per season; a least-squares line
   per count against the season's year, each season detrended to 2027/28; the cover's 2027/28 terms applied season by
   season; the burn loaded by the manual's factor.
2. Join the glass register (old station number, one sheet per year) to the automatic station's daily file (new
   number) through the station register; keep approved readings.
3. Read the station history: the 1995 change to the probe in the small shield, with paired readings to April 1998.
4. Bring the glass era to the probe's basis with the comparison readings' mean difference, probe minus glass, about
   +0.1 C (+0.2 C on summer days); no half-degree reading crosses 35.0 C or 40.0 C, so the glass era's counts stand.
5. Count heat and severe heat days per season, fit the two lines, detrend, replay the terms, average and load.

Ends on: about $725 a hectare (prototype), the raw record's premium, with the heat-day line rising about 1.0 day a
decade.
Golden: about $670 a hectare (prototype), with the heat-day line on the present basis rising about 0.6 days a decade.

Every figure here is the prototype's (`generator/` replaces it with the built values at stage 3).

## Stump sentence

The default path converts the glass era with the comparison readings' mean probe-minus-glass difference (about +0.1 C,
+0.2 C on summer days), which moves no half-degree reading across 35.0 C or 40.0 C, so the 1995 step stays in the
heat-day line and it quotes about $725 a hectare, the raw record's premium; a solver who sizes one hot-day offset
moves the 34.5 C days but not the 39.0 C days and quotes a third figure.

## Three rules

- Task type: general-statistics-data-science / exploratory-data-analysis-distribution-assessment, which serves
  anomaly-detection; the decisive step assesses the distribution of a paired-instrument difference across the range
  of the reading.
- Domain test: the deciding quantity is the probe-minus-glass difference as a function of the glass reading (a
  reading-dependent shift, estimated conditionally or by quantile matching), which distribution assessment estimates
  and a location summary misses.
- Swap: rewrite the call with a blood-pressure cuff replaced mid-record and hypertension days, and the setting survives,
  as it does in a methods domain; swap the method, the mean difference or one pooled hot-day offset for the
  reading-dependent conversion, and the call moves (about $725 or a third figure against about $670).
- Layer 1: the two station numbers joined through the network register (the network renumbers a site when it goes
  automatic); the glass register as one wide sheet per year, days by months, with the observer's header block (how the
  network digitised paper registers); half-degree glass readings (the observers' practice, stated in the station
  history); provisional and approved automatic readings overlapping for the months after the latest approval run
  (outside every cover window); neighbour stations' monthly series with gaps and their own changes; the term sheet's
  history of deductible and day rates by season; the co-operative's member schedule with endorsements and
  cancellations. None is placed to be caught.
- Layer 2: estimation_fit, the conversion between instruments estimated at each reading because the paired difference
  grows with the reading and the record is rounded to the half degree.
- Decisive step: sizing the conversion at each reading is a choice of estimator for a documented change, not catching
  a plant (the change and its paired readings are filed as the network files them), not reading a field (every field
  is read the same on both routes) and not applying a rule (the manual states the basis, never the method).
- Analyst test: a strong analyst who joins the two station numbers, reshapes the register, keeps approved readings,
  reads the station history and applies the manual exactly still converts the glass era with the comparison readings'
  mean difference and quotes about $725 a hectare (prototype), the raw record's premium.
- Estimand: the pricing manual's basis sentence (each past day's maximum as the present instrument would have recorded
  it; heat days and severe heat days counted per season from 1965/66), filed in the manual, with the cover's terms in
  the term sheet.
- No decoy: no memo, draft, briefing or stakeholder figure carries a premium, a conversion or a count; the network
  publishes no adjusted series for Merrin Flat (it is not a reference station), and the station history states the
  change and the paired readings without a size.
- No certified replay: no certified or published figure is reproduced to recover the method; the method is the
  estimator's choice on paired readings the network files.
- Lesson: an instrument change can leave the mean untouched and stretch the upper tail, so a threshold count needs the
  conversion sized at each reading, and a mean conversion leaves the changeover step in the count to be read as
  climate; no build on file teaches a reading-dependent conversion (17 Anomaly Detection drivers read above).

## Tried and rejected

- Physical & Environmental Sciences, environmental monitoring exceedance, as the domain: blocked by `ban.pairing`
  (task180 is the same domain and objective in this draw's window).
- Actuarial Science & Insurance as the domain: none of its task types serves Anomaly Detection, so the domain would
  be a backdrop for the objective.
- The seed's hold design (the tail break's interval wider than a filed tolerance, so the rate holds): the decisive
  step would be applying a stated tolerance, rule application.
- Gap population with pattern E: `test.same_puzzle_older` and `test.same_driver_older` against seven older builds;
  the honest label is the rule gap (the filed basis selects the per-reading conversion once the data show the
  difference depends on the reading), G16.
- One trigger (35.0 C only): one live degree of freedom, since any single hot-day offset between 0.5 C and 1.0 C
  lands the golden; the 40.0 C severe tier makes every single offset miss (34.5 C needs 0.5 C or more, 34.0 C under
  1.0 C, 39.0 C 1.0 C or more).
- A Fahrenheit era before 1972 in the pricing record: whole-degree readings put 102 F (38.9 C) one bin from the
  severe trigger with a 0.14 C margin; the record starts in 1965 in Celsius instead.
- A 1989 changeover with the overlap to 1992: the glass era held 24 of 62 seasons and the premium moved under 5 per
  cent on some draws; the 1995 changeover balances the eras (30 and 32 seasons).
