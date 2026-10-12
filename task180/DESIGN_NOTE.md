# task180 design note (architecture 4)

Seed AD03, objective Anomaly Detection & Diagnostics, re-rooted a fourth time on the author's rule (no retiring).
Architecture 1 (revenue protection, the screen grain) was spent at in-house round 1, architecture 2 (a transformer
inspection slate, main-tank acetylene attributed to its source) at judge pass 2, architecture 3 (pharmacovigilance
signal refinement, channelling against a self-controlled comparison) at hardening loop 1 under the literal-determinism
rule; their records are the lines in `## Tried and rejected`, and their files are gone from the folder. Carried
forward from all three: the decisive separation sits far above the noise of every lens a reviewer can bring, every
graded figure is stated with its window and method, and nothing in the pack files the comparison that decides.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task180.json` (v4), registered 2026-10-12. `guard.py check`: WARN
  repeat.gate_g only (forecasting in the last two builds, task124 and task181), answered in the card's notes: the
  forecast here is pinned once the 2026 record's detection is modelled, with no change to the generating process. A
  first card (strategy population_selection, pattern E) was blocked against task124 (ban.strategy and
  test.same_driver); the move is a property of the recording process, so the honest labels are strategy `other`
  (detection completeness on a daily noise cycle) and pattern `none`, with the G-codes carrying it.
- **Pairing:** Physical & Environmental Sciences, task type `environmental-monitoring-exceedance` (AD), objective
  Anomaly Detection & Diagnostics. The anomaly is a geothermal plant whose induced seismicity will run over the mining
  authority's traffic-light amber in 2027; the diagnosis is that its quiet 2026 record is an artifact of daytime
  noise at its town stations, not a quiet reservoir.
- **Stakeholder and forum:** the state survey's seismological service (org `research_or_statistics_office`), which
  runs the plants' monitoring networks and reports the traffic-light counts quarterly; its induced-seismicity lead
  (role `research_desk`) tells the mining authority (forum `regulator_or_inspector`) before the 2027 operating plans
  are approved which plants the new networks will locate over amber. Forcing event `cutover_or_migration`: from
  1 January 2027 the monitoring ordinance requires borehole stations at every plant. People (guard.py names, de_DE,
  seed 180): Gundula Atzler, Eugen Scheel, Amalie Mende, Arndt Ernst.
- **Shape 07 (grid of cells):** plant by quarter of 2027, each cell an expected count of located earthquakes of ML
  1.0 or more within 5 km of the injection well and its place against amber (5 plants x 4 quarters = 20 cells), with
  the call (which plants, which quarters) on top; the asks add their own grids (sized in `## Ask sheet` at design).
- **Gap and generators:** gap population (the catalogue is not the earthquakes), then time (the 2027 network records
  what the 2026 one missed). G12 (absence against record of absence: a daytime hour with no small events is a
  non-answer), G14 (the detection yield conditioned on the hour), G16 (which completeness method the record
  supports), G13 (the horizon: the network the forecast is counted on). Gate G `forecasting`.
- **Data-native sentence:** the 2026 networks record an earthquake only when it rises above the ground noise at the
  stations around the plant, and in town that noise follows the working day, so the town plant's small events reach
  the catalogue mostly in the night hours while its magnitude-frequency curve still looks complete on the usual test.
- **World (targets; the generator asserts or replaces each with its built value):** five deep geothermal
  district-heating doublets in the southern Bavarian Molasse basin, each injecting cooled brine into the Upper Jurassic
  carbonate at 3 to 4 km. Injection follows heat demand (winter quarters high, summer low) and the filed 2027
  operating plans repeat each plant's 2026 quarterly volumes. Traffic-light rule (the authority's 2024 scheme): amber
  when the plant's monitoring network locates more than 120 earthquakes of ML 1.0 or more within 5 km of the
  injection well in a calendar quarter; red on any located earthquake of ML 2.5 or more within 5 km (none in the
  record). Monitoring ordinance (2026): from 1 January 2027 at least three borehole stations (150 m or deeper) within
  5 km of each injection well, the network designed to locate every earthquake of ML 0.6 or more within 5 km.
  - **Q (the town plant):** surface stations in a school basement, the waterworks and the fire station; true rate of
    ML 1.0 or more about 175 in a winter quarter and 75 in a summer one; working-day noise hides most events below
    ML 1.8 (half detected near ML 1.45 by day, everything above ML 0.7 by night), so the catalogue holds about 60 per
    cent of them (about 105 in a winter quarter) and the maximum-curvature test reads it complete near ML 0.7.
  - **P (rural, the busiest catalogue):** quiet stations, complete above ML 0.7 at every hour; about 92 in a winter
    quarter.
  - **R (rural):** a station added nearer the well in July 2025; its first-half-2025 catalogue misses about a quarter
    of its small events, so year-on-year growth projects it over amber in the first quarter of 2027 (about 130) while
    its true rate stays about 95.
  - **S and T (rural, small):** 25 to 45 a quarter, each with a quarry within 5 km whose daytime blasts the reviewed
    catalogue types as explosions.

## Default path

1. Take the survey's reviewed catalogue, 1 January 2025 to 30 September 2026, event type earthquake, ML 1.0 or more,
   within 5 km of each plant's injection well (well coordinates from the plant register).
2. Count each plant's events in each calendar quarter, local time.
3. Carry each quarter's count into the same quarter of 2027, the operating plans repeating 2026's volumes (for the
   fourth quarter, 2025's).
4. Compare each cell with amber's 120.

Ends on: no plant over amber in any quarter of 2027 (Q's winter quarters at about 105, P's first quarter at about 92).
Golden: Q over amber in the first and fourth quarters of 2027 (about 175 and 165), no other plant in any quarter.

## Stump sentence

A competent solver counts each plant's earthquakes of ML 1.0 or more within 5 km of its injection well in the reviewed
catalogue quarter by quarter, carries the counts into 2027 on the repeated operating plans and files that no plant
goes over amber (Q's winter quarters at about 105, P's first quarter at about 92); the step that lands it there is
reading the 2026 catalogue as complete at ML 1.0 when the town stations around Q lose most daytime events below ML
1.8, so Q's true rate, recovered from its night hours or from its magnitudes above 1.8, is about 175 a winter quarter,
which the borehole stations will locate from January.

## Three rules

- **Domain test:** the decisive analysis is the seismologist's own: the completeness of an earthquake catalogue by
  place and hour, and the Gutenberg-Richter rate it supports above the counting magnitude; with another field's nouns
  there is no magnitude-frequency law, no detection threshold set by ambient ground noise and nothing to recover from
  the quiet hours.
- **Analyst test:** a strong analyst who reads the counting rule and the reviewed catalogue correctly counts each
  plant's 2026 events per quarter, confirms completeness with the maximum-curvature test (about ML 0.7 at every
  plant), carries the counts into 2027 and files that no plant goes over amber; wrong, because Q's completeness changes
  with the hour of the day.
- **Layer 1:** origin times in UTC against a rule counted in local calendar quarters across the daylight-saving
  changes; a preliminary catalogue (the one the quarterly reports were counted on) superseded by the reviewed one,
  with relocations, magnitude revisions and blasts retyped at review; the federal agency's catalogue duplicating the
  larger events under its own ids and moment magnitudes; quarry blasts in the working day near S and T; station
  outages and a sensor swap that changes a station code; operators' injection reports with corrected resubmissions.
  Each is something these systems produce, and none decides the call.
- **Layer 2:** the shortcut is to take the located events as the earthquakes; the expert tests the catalogue's
  completeness by hour as well as by magnitude before using it as a rate, and recovers the true rate where the network
  is blind part of the day.

## Tried and rejected

- **Draws weighed for architecture 3 and not taken (2026-10-11).** A labour force survey movement read on the people
  interviewed in both quarters against the rotation groups: the guard's same-puzzle test and the driver both put it on
  task68 (a matched panel of continuing units against an aggregate moved by entrants), the same insight in the same kind
  of office. An airline's landing gear alert traced to one station's wheel changes within each airframe: with forty
  aircraft and many defects each, the chronically defective tails show in any per-aircraft table and controlling for the
  aircraft is a reflex, so the confounder announces itself. Signals passed at danger per approach at danger: the exposure
  either has to be named in the question (rule application) or is a fork against trains passing. An air-quality rise
  normalised for meteorology and a groundwater rise read within each well: attribution of a signal to its drivers, the
  architecture-2 move, and trends any analyst plots. A disproportionality signal unmasked by removing a dominant drug
  from the background: the comparator would have to be filed (rule application) or is a fork. Pre-bid abnormal returns
  under thin trading: the bias from a synchronous beta is swamped by the noise of the thinly traded share.

- **Judge pass 2 (architecture 2, loop 2, 2026-10-11): NOT_DETERMINISTIC, SEND_BACK; architecture 2 spent.** Gate C,
  competing_defensible_answer, in the judge's words: "LST-T2's hydrogen increments track its tap operations: r 0.81,
  permutation p 0.005. Rolleston T2's (RLS-T2) do not: r 0.14." The submission's own increment method, applied to
  hydrogen, keeps Leeston T2 as a main-tank fault, so SBG-T2 and LST-T2 (tied at 8.0674) then RLS-T2 is a defensible
  slate on these files. Companions: the 9.7 ppm-a-year pre-onset pace does not reproduce (9.63 by OLS over the year
  before 9 June 2025), the exact SBG-T2/LST-T2 tie reads as constructed, and the gas-source rule, stated nowhere in the
  pack, can be pressed as an external dependency. The loop-2 radiator hydrogen sat at the noise floor of the tap-linked
  increments, so the hardening that stopped round 4's ratio step opened a fork. Under build-pipeline (Retirement) a
  judge SEND_BACK spends the architecture; re-rooted to architecture 3, the slot's last. Carried forward: a decisive
  separation far above measurement noise under every lens a reviewer can bring, every graded pace stated with its window
  and method, and no exact ties among graded figures.

- **Round 4 landed (architecture 2, loop 1, the re-run the judge's FIX_NOW required, 2026-10-11); hardened as loop
  2.** One solver, proxy 74.8, the slate exact. Its deciding step: "Main-tank fault screen (s5.1-5.2): DSL-T1 and
  LST-T2 (in-oil arcing tap changers) show C2H2 +9.8 and +8.2 ppm with H2 +1 ppm, read as tap-changer contamination
  and excluded; SBG-T2 (vacuum tap changer, H2 +16) and RLS-T2 (H2 +8) kept". The plain gas ratio carried the call.
  Brief: build the next rung so that exactly this step completes and returns the wrong slate. Leeston T2's radiators
  were replaced with new hot-dip galvanised panels on 12 November 2024 (in service, through the isolating valves; the
  log carries it as capital work under the projects office's own job number, so no work-order number moves), and new
  zinc gives off hydrogen, fast at first and easing (26 ppm towards saturation, time constant 0.8 years). Its hydrogen
  was rising at 9.7 ppm a year in the year before its first acetylene (June 2025), so the twelve-month C2H2/H2 reads
  0.91 and the ratio step keeps it (rung 3c: LST-T2 and SBG-T2 tied at 8.07, RLS-T2). What the ratio cannot see is
  that the acetylene brought no hydrogen of its own: over and above the pace it already had, Leeston T2's hydrogen
  did not move when the acetylene came, while Rolleston T2's hydrogen was flat for the year before its acetylene and
  rose with it. The decisive step is now per gas: tracking for the acetylene, the timing of the hydrogen against it.
  Every golden figure stays (asserted against the round-4 values); the verifier carries its own version of the rule.

- **Judge pass 1 (2026-10-11): DETERMINISTIC, FIX_NOW on hygiene.** The maintenance log's 176 annual inspections
  reused one sentence and five remarks ("T2 fan 3 noisy bearing, raised WO." 25 times at 16 sites with no follow-up
  order) and Burnham's battery bank was "8 years old" in 2019 and again in 2022. The remarks now vary on a random stream
  of their own (the draws that number the work orders are untouched, so every OLTC, breather and oil-processing row is
  byte-identical, asserted), defects are dealt with on the visit, a second battery job at a site is a discharge test,
  and the bookings sheet carries its 9 October save stamp. The judge's watch item stays a defence, not a change: the
  RLS-T2 split rests on the field's gas knowledge, and the in-pack contrasts are hydrogen flat at DSL-T1 and LST-T2
  through acetylene rises of about 22 and 13 ppm, RLS-T2 hydrogen from about 33 to 54 ppm after its onset, and SBG-T2
  as the control.

- **Round 2 landed (architecture 2, loop 0, 2026-10-11); hardened as loop 1.** One solver, proxy 74.6, the slate exact
  and every ask figure right. Its deciding step: "Main-tank test (5.2): joined monthly samples with tap ops from
  scada_tap_counters_daily (rollovers +100000; counters replaced -> reset). DSL-T1 and LST-T2 acetylene rises at a
  constant ~0.6 ppm per 1,000 ops in every interval (in-oil tap-changer leak) -> excluded; SBG-T2 (vacuum tap changer)
  and RLS-T2 acetylene rise in steps unrelated to ops." The confirming reader (pass 3, run beside the round) planned the
  same step off the 5.2 rewording: "Keep only code 3 units with a main-tank fault (s.5.1-5.2). That means dropping in-oil
  tap-changer units whose acetylene or hydrogen rise tracks tap operations." 5.2 stays as worded, because without it the
  literal reading is rung 1; the attribution is a work order and the hardening deepens it instead. Brief: build the next
  rung so that exactly this step completes and still returns the wrong slate. Rolleston T2's arc is now at the tap
  selector, which works in the main-tank oil: a little gas at every operation, so its acetylene follows its counter as
  closely as the leaks' (r 0.999 raw, 0.992 per day) and the tracking step drops it (rung 3b: Southbridge T2, Coalgate T1,
  Springston T2). What it cannot copy is the gas: an arc in the main-tank oil makes 1.6 times as much hydrogen as
  acetylene (twelve-month C2H2/H2 0.64), where the leaks bring diverter oil at 9.8 and 8.2. Construction: the gas per
  operation is held constant through the arc, the onset is just after the December 2024 sample, and Rolleston's tap
  changer follows the step loads of the processing plant on its feeder (its own random stream, so no other unit's
  draws move; plant seed chosen so all 18 grid columns keep the order with at least 5.3 per cent margin and the
  tracking r is at least 0.985 in every window and below-detection reading). Only RLS-T2's tap-operation figure moves
  in the goldens (27,534 to 49,897, still inside the interval). A first draw on the substation's ordinary load-swing
  switching, with the onset in January 2025, fell to r 0.884 from the last below-detection result and let Coalgate T1
  pass it on a 400-day base; both rejected.

- **Architecture 1 spent at round 1 (2026-10-11): screen grain (metering system against supply number).** Plain
  solver 81.3 and skeptic 85.6, both on Caithness 54 against Elgin 35. Plain: "rp_mart_weekly_import was rejected for
  screening because it sums each related point into its primary's metering system: mart = primary + related reads to
  within 0.2 kWh." Skeptic: "Supplies sheet (2,960 main MPANs) plus Related metering points sheet (699 heating-only
  MPANs, each with its own supply number) gives 3,659 supplies, matching the 3,659 MPANs in the reads parquet." The
  grain the procedure screens has to be filed for determinism, and once filed it is a work order: both rebuilt per
  supply from the reads and reconciled the mart before rejecting it. The ask devices (re-keyed jobs, appeals keyed to
  the raising system, the Scottish calendar, a mid-quarter start) were each executed off a filed rule. Not hardened:
  the only rung that would stop this step is a plant (withholding the glossary makes the grain a fork). Re-rooted.

- Seed AD03 as written (register split by each meter's switching regime, recovered from an operator acknowledgement
  corpus): the decisive rule withheld and recovered from a closed corpus is the capped Pattern B pin, and the
  acknowledgement file would refute the whole-house screen case by case (an alarm, not a stump).
- Register split from half-hourly data by time-of-use regime: if daily register reads ship the split is a lookup, and
  if they do not, the realistic route is the separate heating supply, which is how north-of-Scotland storage heating
  is actually metered, so the build uses related supply numbers.
- Account-level shortfall of heating diversions above 25 per cent (first parameter pass, heating 0.62 to 0.86 kWh per
  degree day): too close to the 30 per cent band for convergence across weather readings; heating sensitivity cut to
  0.42 to 0.62.
- Strathspey at 9 heating diversions tied Inverness City at 19 referrals, an ordering fork in the ranked chart; cut to 6.
- First cut of the pack (mart keyed by billing account and described as "the account's metered import", heating-only
  supply numbers listed inline on the Supplies sheet with a `related_mpan` column): the solver's-eye leak reader's plan
  of attack, before any solve, was "screen each MPAN separately, including the related heating-only ones" and "use the
  mart only as a sanity check, since it is per account". The decisive grain was announced by the file layout. The mart
  is now the metering-system table it would be at a supplier, keyed by the primary supply number, and the related
  metering points sit on their own CIS sheet, so the natural pipeline (Supplies sheet plus mart, or plus the reads) is
  keyed by supply number and silent everywhere. The same reader flagged RP-07's revision table (its two lines named the
  own-history degree days and the occupier window) and the DNO loss file ranking Lochaber top, echoing the belief; both
  rewritten.

- **Leak reader pass 1 on architecture 2 (2026-10-11), hardened before any solve.** The reader quoted nothing for
  question 1, but its plan of attack read "check that no code 3 rise looks like gas from the tap-changer compartment
  (1.2, 5.1)": the standard's scope sentence (the coding applies to the gases generated in the main tank), its
  clause on annual compartment sampling and the compartment results file together turned the attribution into a work
  order. Removed: the scope sentence, the sampling clause (and its revision-history mention) and the compartment file,
  which no ask needed. What stays filed is the remedy (5.1, an internal inspection is the remedy for a fault in the main
  tank) and the allocation to transformers whose main-tank gases point to such faults (5.2); the attribution rests on
  the tap-changer type, the counter tracking and the acetylene-to-hydrogen ratio, all of which the main call already
  reads for other reasons, and on IEC 60599, which the standard cites.

- **Section 5.2 reworded for determinism (2026-10-11).** With the scope sentence gone, section 4 codes the main-tank
  results as reported, so DSL-T1 and LST-T2 are code 3, and the old 5.2 ("the outages go to the transformers whose
  main-tank gases point to the most severe such faults") could be read as plain code 3 by severity, which lands rung 1.
  5.2 now allocates the outages "to the code 3 transformers with such a fault", the fault being 5.1's fault in the
  main tank, and the goldens report the literal section 4 code, so the code column has one reading and the slate turns
  only on where the fault is. The board paper says both stay code 3 and need tap-changer work instead.

- **Re-root candidates weighed for architecture 2 and not drawn (2026-10-11).** A heat-pump drop told from a diversion
  by its day and night registers, with the heating measures register as the convenient record: the register would be
  the narrower file the clean-data test repairs, so the defect would carry the stump. A weekly referral queue replayed
  run by run: a filed lifecycle is a filed formula, executed. Re-tampers hidden by a baseline that includes the earlier
  diversion: the use-versus-recorded distinction has to be filed in RP-07's glossary, which is where architecture 1 was
  read. Evaluating a new screen on a verification sample: inverse weighting is reflexive once the sampling is stated.
  Revenue protection was left for a transformer fleet, where the decisive step is a diagnostic attribution no filed
  sentence names.

- **Build of architecture 2 (2026-10-11), approaches dropped on the way to the shipped pack.** Leeston T2's last
  tap-changer service in February 2022 put both leaking units past their tap-changer interval (72,409 and 87,696
  operations), so the ask table pointed at the two tap changers the main call turns on; the service moved to May 2023
  (54,294, not past). Attribution signatures computed for every unit with detectable acetylene swept in stable traces
  (SBG-T1, GLT-T1) and the thermal units' crumbs, with C2H2/H2 undefined where hydrogen fell; the signatures are now taken
  only where acetylene rises faster than its rate limit. Thermal survey temperatures to the half degree collided with
  graded figures (33.1, 34.9, 12.5, 27.0, 28.5) inside a document; whole-degree maxima and fixed rises now, with a sweep
  asserting no graded figure in any shipped document. The extract log's "first hour 01/01/2021 00:00" against a parquet
  whose first timestamp reads 2020-12-31 11:00 announced the UTC export in one line; dropped. Interval-length confounding:
  with quarterly and monthly samples mixed, any steady gas source correlates with tap operations through interval
  length, so the vacuum unit's increments are designed in bursts and asserted uncorrelated raw and per day.
- **Severity distance "at least 0.005 from a two-decimal edge" (the build brief).** 0.005 is the half-width of a
  two-decimal bin, so only an exactly round severity meets it, which determinism-check reads as a receipt. Asserted at
  least 0.002 from the edge and at least 0.0003 off the round value instead (worst 0.0021, BNM-T1; naive 9.6415 and
  8.0674).
- **Personas the guard's people sweep read into the pack (2026-10-11).** The substation at Tai Tapu read as a person
  (first name Tai) and blocked against task123, and "Karl Fischer" in the water-content method line read as another
  persona; the substation is Ladbrooks (LDB) and the method line cites IEC 60814. No figure moved (per-unit draws are by
  fleet position, not by name).
- **Architecture 3, round 6 (2026-10-11): landed, proxy 81.6, decision harden (loop 1).**
  - **The solver's own sentence:** "Comparisons between different people ... give tasorexant 2.27 / 3.77 / 3.51,
    but tasorexant users already had 3.43 times the national rate in the year before starting and corinurad users
    0.60, so these mix up who starts the drug with what the drug does; rejected."
  - **Its landing step:** a self-controlled case series over all observed time, age-adjusted: corinurad 2.58 (2.10
    to 3.18), tasorexant 0.99, velaglutide 0.93.
  - **Why the between-person rungs fell:** the national-rate table lets a solver measure the channelling directly.
  - **Why the plain SCCS was enough:** it needed none of rung 3's exposure anchoring, because the event-dependent
    starts moved it only from 2.52 to 2.58.
  - **Stopping-rule count:** 1 of 2.

- **Hardening loop 1, the brief's contraindication at the shipped effect size (2026-10-11): rejected on its
  arithmetic.** Velaglutide starters' pancreatitis before the start thinned to a share q, measured on the simulated
  world with the self-controlled comparison over all observed time from 2018:
  - **The adjustment eats the deficit.** Every start sits in the last two years of a person's observation, so age
    bands (and the solver's age by calendar year) take up most of the step. At q 0.1: 3.02 unadjusted, 2.07 with
    five-year age bands, 1.97 with age by calendar year. At q 0 (no starter ever admitted with pancreatitis): 3.98,
    2.79 and 3.18, against corinurad 2.73, 2.59 and 2.55. No margin survives, and from 2022 velaglutide reaches only
    2.13 to 2.36.
  - **The alarms.** At q 0.05 and below, the comparison with days -365 to -31 alone reads 15 to 45 for velaglutide,
    and the 30-day profile shows nothing at all before the start.
  - **A 2024 to 2026 weight-loss boom helps but not enough.** It puts more of each starter's time before the start:
    q 0.015 gives 3.10, 2.98 and 2.89 (five-year bands, age by calendar year, bands with half-years), against
    corinurad 2.59, 2.55 and 2.57, which is 1.13 to 1.20 on an empty pre-start.
- **A lagged kidney injury to start dependence for corinurad (2026-10-11): rejected.** The idea was that an injury
  brings on a gout attack, and the attack gets urate lowering started 60 to 365 days later. Three times the start
  hazard deflated corinurad's all-time ratio only to 2.29, 2.24 and 2.23. It also painted kidney injury admissions
  before the start at twice the post-start level, the story of a medicine avoided in kidney disease turned upside
  down. Calendar adjustment still named corinurad.
- **Hardening loop 1, the paper half under the literal rule (2026-10-11): spent.** The rung loop 1 built (velaglutide
  not started after a pancreatitis, so the comparison with all observed time names it and only the comparison anchored
  at the start recovers corinurad) is rule application once the comparison is filed, which `determinism-check` §1
  requires. SOP-PV-14 1.2 asks whether starting the medicine raises the risk of the event in the month after the start
  and files no comparison. Measured on the a4261fe build with `golden.py`'s own estimators:
  - **Literal reader.** Each filing of the comparison, executed word for word:
    - other people (matched non-users; new users of the established medicine; both crude): tasorexant, by 2.48 and
      2.49;
    - the same new users before they started (days -365 to -31; all resident time before the start; against the
      matched non-users' same windows): velaglutide 11.17, 11.87 and 9.42, by 6.25, 5.72 and 4.97;
    - the same new users' other time (all observed time from 2018, unadjusted and by age and calendar year; from 2022
      by five-year age band): velaglutide, by 2.64, 1.38 and 1.53;
    - the same new users' time after the month after the start (days 61 to 180; day 31 on): corinurad 1.655 (1.221 to
      2.242), by 1.62 and 1.59 (tasorexant 0.985, velaglutide 1.023). The only filing whose literal execution is the
      golden's figure, and it names the reference window, which is the step.
  - **The counterfactual filing** ("the rate the same new users would have had over those days had they not
    started"). Read literally it either leaves the method open with nothing to select it, or points at the only time
    the same new users were without the medicine, before they started (the second reading, velaglutide). It also
    leaves velaglutide's step at the start live as an effect of starting: its pancreatitis runs at 0.24 admissions per
    1,000 person-years in the year before the start and 2.09 in the year after (18 admissions in the twelve 30-day
    blocks before the start, 103 in the twelve after). The golden's design compares two windows after the start and
    cannot see a step at day 0. Only a between-person argument rules it out (after the start velaglutide users match
    orlistat starters, 2.09 against 2.11), the kind of comparison this build teaches the solver to distrust.
  - **The counterfactual with a criterion** ("estimated by a design whose assumptions the registry data bear out", the
    closest general wording that closes the all-time reading without naming a window or an estimator). The data
    separate the candidates under it by wide margins. In the year before the start, tasorexant starters' fall rate ran
    at 3.99 times matched non-users' and 2.28 times zopiclone starters'. Corinurad starters' kidney injury ran at 0.45
    times allopurinol starters'. Velaglutide starters' pancreatitis ran at 0.12 times orlistat starters' and 0.17
    times matched non-users'. But executing the criterion is the decisive step. The assumption to check for the
    self-controlled comparison is the textbook one (the event must not change the chance of starting), and its data
    are the loudest pattern in the pack, in the 30-day block profile round 6 drew unprompted (its step 4). A criterion
    that names only a concept is a Gate C risk on its own (task44), and naming the observable ("time in which the
    event cannot have changed whether the person started") names the step.
  - **Rule 3, answered: no.** A strong analyst who reads that criterion correctly and cleans the data names corinurad.
    Naming velaglutide or tasorexant takes skipping the check the filed text orders. The only texts that close the
    all-time reading name the step or order it.
  - **Why no tuning rescues it.** To beat the age adjustment the deficit has to be deep and lasting (loop 1's
    arithmetic above), and a deficit that deep is an 8.5-fold step at day 0 in the event profile. So the separation
    determinism needs is the same symptom that hands over the step (`stumping`, Where the decisive move survives, 3 and
    6). A filed back-test on closed reference pairs (C2) separates the designs only with a contraindicated negative
    control in the corpus, and that corpus then nominates the anchored design to any solver that back-tests.
  - **The shipped ladder fails the same test.** The comparison is one of the estimand's five parts and is this
    architecture's whole decisive step (rungs 1 and 2 against rung 3). Filing "the same people's other time" makes
    round 6's method the literal execution (corinurad 2.58 in the shipped world) with nothing analytical left, as
    task181 found.
  - **State.** The WIP generator at a4261fe stays as committed (not green: caused 5.539 on its rounding edge). No pack
    is cut and nothing goes to a builder. Retiring the number is the author's decision.

- **Architecture 3 re-rooted (2026-10-12).** On the author's rule (no retiring) the number takes a fourth architecture;
  the pharmacovigilance files (generator, pack, goldens, write-up) are deleted, its rounds stay in `solver_rounds/`.
- **Draws weighed for architecture 4 and not taken (2026-10-12).**
  - Measles susceptible accumulation against the herd threshold: once the estimand is literal, the count of children
    without immunity is mechanical from the registry, and a record of past importations that forces a threshold is a
    search bench.
  - Two-source capture-recapture of surveillance records: an estimand saying "recorded or not" sends the solver to the
    textbook estimator, and without it the recorded count is the literal reading.
  - A first testing sweep finding the prevalent stock: the count found follows the time since a population was last
    looked at, the reset family task132 holds.
  - Repeat-tester incidence against new diagnoses: the population's incidence is not literal, and the repeat-tester
    rate is a proxy whose choice is the reading.
  - Crime displacement or ambulance diversion under a moved deployment: the displacement shares need a model the
    record fixes only once, a fork at the figures.
  - A correlation break in batch process data: an enumerable set of monitoring statistics behind closed batch
    outcomes is an answer key.
  - A pull-forward before a dated policy change: any solver anticipates the deficit after a filed deadline.
  - Site-specific magnitude-frequency slopes under a lowered counting magnitude: estimating each site's own b-value is
    standard practice and lands.
  - Lead surveillance stratified by housing age: reweighting tested children to all children is the stratify reflex.
  - A case-fatality ratio read before deaths mature: the reporting-delay family of task181 v2.
  - A VAT carousel traced through buffer traders: the swap test fails, any layered money flow reads the same.
