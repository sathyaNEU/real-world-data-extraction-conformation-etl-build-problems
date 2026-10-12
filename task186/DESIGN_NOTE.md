# task186 design note

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task186.json`, architecture v1, drawn 2026-10-12 from seed AD09 (a
  regulator deciding which fuel brands to examine for levy pass-through). The world, the decision and the quantity are
  the seed's; the seed's pitfall (the ownership flag is not who sets the price) is not used for the call, and the
  pitfall is re-found from the stations' margin record.
- **Pairing:** Survey Research & Official Statistics, anomaly detection (the task type serves Anomaly Detection &
  Diagnostics). The monitor sits in the provincial statistics bureau, which runs the mandatory price-reporting scheme;
  scoring each unit's period change against an empirical reference of comparable changes is official statistics' own
  anomaly detection (as Hidiroglou-Berthelot scores period ratios against the spread of the other units' ratios).
  Secondary domain Economics & Econometrics (retail fuel margins and levy pass-through). General Statistics & Data
  Science x Anomaly Detection was the first draw and is blocked against task185 (`ban.pairing`).
- **Niche:** the Provincial Statistics Bureau's Prices Division runs the fuel price monitor under the Fuel Price
  Transparency Act and recommends to the Fuel Price Commissioner the one brand the Commissioner's pass-through inquiry
  examines before each 1 January rise of the provincial carbon levy. The monitoring standard finds, station by
  station, where the January 2026 rise was passed on in excess, with the false discovery rate across every examined
  station held at 5 per cent, and the inquiry goes to the brand with the largest share of its examined stations found,
  if that share is at least one in ten.
- **Forcing and forum:** the 1 January 2027 levy rise; the inquiry notice is served before it
  (`statutory_or_regulatory_filing`); the Commissioner decides (`regulator_or_inspector`); the organisation is a
  statistics office (`research_or_statistics_office`); the stakeholder is the head of the Prices Division
  (`statistical_office_head`).
- **Call:** the brand the 2027 inquiry examines (or none), with each brand's share of examined stations found, to the
  nearest ten per cent.
- **Shape 01** (ranked list under a cap, each candidate): the inquiry is capped at one brand; each of the seven brands
  carries its share found (7), its stations priced by the brand on 1 December 2026 (7) and its regular litres in each
  month of the first quarter of 2026 (21); the call (1), a chart of the litres (4 parts), files and units (3). Criteria
  arithmetic: 43.
- **Strategy and mechanism:** `uncertainty_hold` family (signal against noise across many simultaneous tests); gap rule
  then time (the filed false discovery rate entitles only a null that holds it, and the data's time structure, the
  areas' price cycles, decides what that null is); decisive G2 (the unit of independent evidence is a 28-day period
  change of an area's cycle, not a station-day), G17 supporting; Gate G `signal_vs_noise_or_hold`; calibration
  `none` (the null comes from the record itself).
- **Data-native sentence:** every urban area's regular-gasoline margins cycle over five to nine weeks as stations
  undercut each other down and then restore together, so a 28-day before-and-after margin change carries the area's
  cycle phase, which no station's own day-to-day variation shows; only the changes between periods when the levy did
  not move (or the same-area competitors at the same dates) give the null that holds the error rate.
- **Mechanisms read** (`guard.py mechanisms --objective anomaly-detection`, 18 builds): 25 and 28 a second-source
  inflow and a reachable share; 33 forward yield cut by an intervention; 48 a two-sided grain; 54 exposure while in
  custody; 68 a matched panel through identity successions; 76 a look-back class with zero conversion; 85 a unit's own
  observation window; 103 a fan-out through authorisations; 104 a self-adapting scorer replayed at another setting;
  119 waits a unit could shorten; 182 a lagged response to a shared driver; 183 repeat failers in parts; 125 a
  recruitment filter's carried difference; 180 detection by the quiet hours; 181 crossings of moving units; 184 host
  stand-down crowd-out; 185 a reading-dependent instrument conversion. None tests many units at once, none turns on
  the null distribution of a period change under shared local cycles.
- **Guard:** WARN `overuse.objective` (this is the Anomaly Detection lane). Nearest drivers at 0.06 (task121 v3, a
  self-controlled exposure comparison for complaint attribution; task500 v2, a spillover through links): neither
  tests many units against a null; the abstraction test maps neither onto this driver.
- **Sources:** the seed (AD09) gives the world (a regulator's minute-stamped price log, a station register with an
  ownership flag, closed levy changes) and the decision; its corpus-fit panel rule is not used. The client's official
  statistics anomaly pattern (robust ratio tests against the cross-section, not raw z-scores) teaches that an anomaly
  is judged against the spread of comparable changes; this build moves that to many simultaneous tests whose
  theoretical null is wrong. The client's multiple-testing pattern (FDR on the whole family) is kept as a filed rule
  and is not the stump. The client's two-layer example "comparing against the right group, not a simple before and
  after" is the lesson, carried by the null rather than a control arm.

## Default path

1. Read the monitoring standard: the daily price (time-weighted, 06:00 to 22:00 local), the daily margin (price net of
   the 5 per cent sales tax, less the levy in force and the terminal rack price), the margin change (the 28 days from
   1 January 2026 against the 28 days before), the examined-station rule, findings at a 5 per cent false discovery
   rate, and the inquiry rule (largest share of a brand's examined stations found, at least one in ten).
2. Rebuild every station's daily regular price from the minute log (UTC stamps to local time, the June 2026
   renumbering through the crosswalk), join the rack prices and the levy, and keep the stations examined.
3. Test each examined station's margin change against its own day-to-day variation: a one-sided Welch t-test of the
   28 daily margins after against the 28 before (a Mann-Whitney test or Newey-West errors give the same findings).
4. Apply Benjamini-Hochberg at 5 per cent across every examined station and take each brand's share found.

Ends on: the inquiry goes to Harbourline Fuels, every one of whose stations is found (prototype), ahead of Pellow Gas
at about seven in ten; Tallis Petroleum sits fourth or fifth at about three in ten, with the other brands.
Golden: the inquiry goes to Tallis Petroleum, about three in ten of whose stations are found; no other brand has more
than one in twenty.

Every figure here is the prototype's (`generator/` replaces it with the built values at stage 3).

## Stump sentence

The default path tests each station's 28-day margin change against the station's own day-to-day variation, which
cannot see that every area's margins cycle over five to nine weeks, so it finds nearly every station in the two areas
whose cycles restored just after the change and sends the inquiry to Harbourline Fuels; a null built from the
stations' changes between periods when the levy did not move holds the false discovery rate and leaves only Tallis
Petroleum's company-run stations, which kept about 3 cents a litre more than the rise.

## Three rules

- Task type: survey-research-official-statistics / anomaly-detection, which serves anomaly-detection; the decisive
  step scores each unit's period change against the spread of comparable changes, as official statistics' anomaly
  detection does.
- Domain test: the deciding quantity is each station's evidence of a margin rise beyond full pass-through, held to a 5
  per cent false discovery rate across every station, which needs the reference distribution of a 28-day margin change
  when nothing changed; official statistics anomaly detection takes that reference from comparable units and periods
  (an empirical null), and a theoretical null built on day-to-day variation misses the areas' price cycles.
- Swap: rewrite the call with clinics and wait times and the setting survives, as it does in a methods domain; swap
  the method, the theoretical null for the empirical one, and the call moves (Harbourline against Tallis).
- Layer 1: a minute-stamped price-change log in UTC read against a local-time daily window across daylight-saving
  changes (how the reporting platform stores submissions); station numbers renumbered by the reporting system in June
  2026 with a crosswalk; terminal rack prices published per business day in dollars a litre, weekends and holidays
  carried; a station register whose brand changes are effective-dated; batches of changes resubmitted after reporting
  outages. None is placed to be caught; each is asserted neutral for the call.
- Layer 2: estimand_identification, the counterfactual movement of a station's margin without the levy change, which
  under the areas' price cycles is a 28-day phase effect that only between-period or same-area evidence measures.
- Decisive step: choosing the null for many simultaneous tests is an estimator choice on records the bureau keeps,
  not catching a plant (the cycles are every area's ordinary pricing), not reading a field (every field is read the
  same on both routes) and not applying a rule (the standard files the false discovery rate and the inquiry rule,
  never the null).
- Not semantics: every field, unit and code (UTC stamps, the crosswalk, the rack's dollars a litre, the sales tax, the
  levy in force, the register's brand on the day) is read the same on the easy route and the golden one; a reader who
  reads them all correctly and tests each station against its daily variation still sends the inquiry to Harbourline.
- Not rule application: the standard states the margin, the windows, the false discovery rate and the inquiry rule,
  but no filed rule says how to judge a margin change against what full pass-through would leave; executing every
  stated rule with a t-test still files Harbourline.
- Analyst test: a strong analyst who rebuilds every station's daily margin from the minute log, applies the standard's
  windows and examined-station rule and tests each margin change against the station's day-to-day variation before
  Benjamini-Hochberg at 5 per cent finds most stations in two areas and sends the inquiry to Harbourline Fuels, not
  Tallis Petroleum (prototype).
- Estimand: the monitoring standard's finding sentence (a station passed on more than the rise when its margin rose
  by more across the change than it would have had the levy not changed), with the false discovery rate across every
  examined station held at 5 per cent, and the inquiry rule.
- No decoy: no memo, bulletin, briefing or stakeholder figure names a brand, a share or a finding; the bureau's
  published weekly averages rank nothing on pass-through and are a distractor.
- No certified replay: no certified or published figure is reproduced to recover the method; the null comes from the
  record itself.
- Lesson: a change measured across an event carries every structure the series has between periods, so the evidence
  for many units at once must be judged against how much such changes move when nothing happened, not against
  within-period noise; no build on file teaches the null of many simultaneous tests (18 Anomaly Detection drivers read
  above).

## Tried and rejected

- General Statistics & Data Science, multiple testing and selective inference, as the domain: blocked by
  `ban.pairing` against task185 (General Statistics & Data Science x Anomaly Detection in this draw's window).
- The seed's panel rule fitted to the closed levy changes: a corpus-fit withheld rule (the guard's banned
  architecture), and the ownership-flag question it rests on is a field reading.
- Brand-level pass-through with town-clustered errors as the filed measure: a brand-level test is not what the
  standard files and its clustered errors leave Tallis short of significance, a competing answer.
- A pooled empirical null with some areas not cycling: the null distribution is a spike and a slab, central matching
  fits the spike and finds the cycling areas' stations, so the empirical null and the placebo null disagree; every
  urban area cycles in the build.
