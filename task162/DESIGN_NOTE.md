# task162 design note

Architecture 2, drawn 2026-10-28 (the Forecasting slot's re-root at the author's word, the same day architecture 1 was
spent on determinism). The world, the decision, the dataset and the generator are all new; architecture 1's record is
kept in its own section below, its card identity in the card's lineage and its ledger line under Earlier architectures.

## Draw

1. **Pairing.** energy-systems-utilities / asset-condition-maintenance, which serves Forecasting (`guard.py check`
   raises no task-type BLOCK). A water network's leakage is the standing condition of its mains and service pipes, and
   pressure management is the intervention whose effect the field forecasts by FAVAD (leakage rising with pressure to a
   district's N1). Client domain energy-systems-utilities; no house domain.
2. **World.** Lynmere Water, an English water company (invented), supplies its Northern zone from Thornholme service
   reservoir down the Thornholme to Brackenby trunk main. Coldbeck Network Partners (invented) is its pressure management
   and leakage delivery partner on an outcome contract: paid per megalitre a day of sustained reduction as Lynmere's own
   annual district leakage assessment measures it, with a reduction target per phase. Phase 3 is the 22 district metered
   areas at the trunk main's far end, each getting a fixed-outlet pressure reducing valve at its inlet, commissioned
   January to March 2027. The contract measures the phase against the 2025-26 assessment year, in the 2027-28 one.
3. **The call (forward, a window not yet open).** Will Phase 3's valves take the districts' leakage down by the
   contracted reduction in the 2027-28 assessment, and if not, how much must find-and-fix take out on top? A go/hold
   (mobilise find-and-fix gangs for 2027-28 or not) with the shortfall in megalitres a day; shape 02, the phase's
   assessed leakage month by month through April 2027 to March 2028.
4. **The decisive step (Layer 2, G7 operating window).** A fixed-outlet valve holds its outlet at its setting only
   while its inlet pressure is above the setting and stands fully open otherwise. At the trunk main's far end the
   morning and evening demand peaks pull the inlet down by 18 to 34 metres, below several valves' settings for hours a
   day and longer in summer, so the leakage Lynmere's assessment will measure in 2027-28 (net night flow times a
   night-day factor built from the 15-minute average zone pressures) comes from replaying each district's recorded
   inlet and average zone pressures through the setting, reading by reading, and rebuilding both the night flow and the
   night-day factor. The easy route carries the valve's night pressure reduction through every hour.
5. **Card.** shape 02; decision go_hold_or_stop; answer unit rate_or_share (megalitres a day); gap time then
   population; pattern none; generators G7 (decisive) and G13; Gate G forecasting; strategy binding_constraint (the
   setting binds only in the readings where the inlet exceeds it; the skill's objection that an applied published limit
   is rule application is answered under Three rules at stage 2: the level is filed, the readings it binds on are a
   physical consequence of recorded pressures no sentence states); calibration none; context artifact
   monitoring_export (Lynmere's monthly district leakage assessment, correct for the question it answers); Layer 2
   field_method, `own:fixed-outlet-valve-diurnal-bite`; forum customer_or_counterparty (the plan goes to Lynmere's
   contract manager); forcing event launch_or_rollout (the valves commission in the first quarter of 2027 and the
   2027-28 gangs are mobilised before the assessment year opens); org professional_services (the partner carries the
   contracted reduction); role operations_director.
6. **People** (`guard.py names --geo "United Kingdom" --seed 162`, on the card): Emily Fitzgerald (Coldbeck's Northern
   zone programme manager, the requester, not in the prompt), Annette Patel (Coldbeck's network modeller, the valve
   schedule), Clive Heath (Lynmere's contract manager), Louis Lee (Lynmere's leakage analyst, the assessment export),
   Mandy Austin (Coldbeck's commercial manager).
7. **Guard.** `check` before and after `register` (2026-10-28T04:48:39Z): WARN only. repeat.gate_g and overuse.gate_g
   answered on the card (forecasting carries this stump, a forward assessment of an intervention not yet installed,
   and the fine mechanism is no forecasting card's: nearest driver 0.07, task303). test.same_driver_older is
   differentiated on the card against task105 v1 (an outlet's season-ahead agreement window), task170 v1 (a first
   passage of scattered measurements over a level), task229 v3 (a daily mean passed through a convex rating, Jensen's
   gap inside the day, where averaging the replayed readings here is harmless) and task303 (shared upstream losses).
   The forcing event was redrawn from purchase_order_or_contract (task179 holds it) and the organisation from
   utility_or_infrastructure and the role from capacity_planner (task281 holds both); the partner's seat is the honest
   one, since the contracted reduction is the partner's to deliver.
8. **slots.** On the driver's words and on the setting's (valve setting, outlet, inlet pressure, trunk main): no slot
   note touches a valve, its setting or an inlet pressure. "water company" finds task182's arsenic results, task248's
   treatment plants and task303's feeders, none of them this mechanism; task120 (a campus water utility's well capacity
   read through its tank levels, in review) shares the water setting and nothing else.
9. **Prototype** (scratchpad `t162v2/proto/prv3.py`, 14 districts, night inlet 58 to 78 m, trunk main drop at the peak
   18 to 34 m, district head loss 6 to 16 m, N1 0.94 to 1.57, settings between each district's peak and night inlet):
   the valves control 65 to 96 per cent of readings; the phase's saving from the 15-minute replay 0.647 Ml/d, hourly
   0.634, a typical day 0.639 and the mean-pressure route 0.639 (the replay family inside 2 per cent), against the night
   pressure ratio carried through the day 0.937 (45 per cent over) and the night flow reduction times 24 at 1.153 (78
   per cent over). On settings that bite in every reading the night-ratio route lands within 3 to 8 per cent, so the
   generator places the phase where the far end of the main really sits: at the service level through the peaks.
10. **Screens on paper.** Estimand: the 2027-28 assessed leakage and its reduction are filed by the contract and the
   assessment method, and the decisive step is none of the five parts. Variance only: the step moves the point
   estimate. Common exposure and partial coverage: there is no attaining subset (Phase 3 is the partner's first scheme
   in the zone, no valve in the zone has run before) and the correction acts on every district's day, one per
   district, never one number. Designation: the call is a total against a contracted figure, no slate. 1.2c: the
   assessment is the filed measurement and the decisive construction is the valve's physics, no model of the
   measurement; N1 is filed per district, so nothing is fitted per group (1.1j) and no grouping decides (1.1c). Fourth
   clause: no file summarises the replay (the export's average zone night pressure and night-day factor are the
   pre-valve facts the easy route reads). Swap: patients and wards have no valve whose effect turns on an upstream
   pressure, no N1 and no night-day factor. Library: the field's shortcut for a scheme's benefit is the night pressure
   ratio raised to N1, which is the default path.
11. **Layer 1** (from Lynmere's own systems, none carrying the stump): district loggers in GMT against the SCADA
   export in local time across both clock changes; logger swaps with new serials mid-year; one logger make reporting
   bar and the other metres head; logger heights against the average zone point's ground level; battery gaps and
   duplicate re-transmissions; a district boundary moved by a valve operation in the record; inlet meters in litres a
   second against the bulk extract's cubic metres an hour.

## Architecture 1 record (spent 2026-10-28)

Drawn 2026-10-18 from seed FC33 in product-analytics / feature-adoption-diffusion-modeling: Usva Software's Tampere
bug-triage team filing its first-quarter 2027 triage headcount, staffed for the busiest week at 120 triage items per
triager-week, in its first quarter on a new tracker. The decisive step built each release's adoption from ordinary
restarts plus the Windows restart burst in the two days after Patch Tuesday, which falls inside every first-quarter
release week and never did in the record: 8 triagers, the busiest week near 900 items, against the default path's 6.
Shipped 10-18, repaired for determinism 10-27 (Ask B's "arrived in its components"), returned 10-28 on the portal's
second determinism round (a validated release-phase model filing 6). The re-cut of 10-28 (the autumn train moved
around the restart cycle, the staffing thread's forecast test filed) was judged three times, and each pass found a
competing defensible answer: the decisive configuration was out of sample, so no back-test over the record forced the
restart model, and the restart family's own spread (848 to 977) was wider than the 120-item band. Lessons carried into
architecture 2: the configuration that decides must be in the record; the golden family's spread must sit well inside
the band; no filed back-test (the consecutive-builds rule); the construction should close on arithmetic the records
supply rather than on a fitted behavioural model. The returned reship's pack is commit 6c612d30; the re-cut was never
committed and its measurements are the lines dated 10-28 under Tried and rejected.

## Tried and rejected
- 2026-10-18 draw: the seed's own route made analytical, a new-to-old conversion whose duplicate share rises with the
  spike, so the quiet parallel-run ratio fails in release weeks; its honest key is composition (task470 held it in the ban
  window), and with the counting basis filed and the old export holding every duplicate, rebuilding the new basis from
  the export bypasses the conversion and lands on any typical-quarter golden.
- 2026-10-18 draw: the December release's open regressions drawing duplicates until their fixes ship with the January
  release; carrying the December excess forward lands within a quarter bin of the golden, so persistence is a bypass.
- 2026-10-18 draw: the January release's beta-channel reports scaled to the release wave by the ratio earlier versions
  showed at the same beta age; it is task157's driver (the part already in times a ratio earlier waves kept) in other
  nouns, and the as-of leaves only days of beta.
- 2026-10-18 draw: each release's wave sized by the fixes it carries; one ratio (linear), a covariate reflex, and only the
  January version's size is known at the as-of.
- 2026-10-18 build: ask device A1 of the design stage (the bridge's history entries under the migration lead's account
  while she was on the rota): no literal rule separates her bridge entries from her own triage without a fork; the
  bridge runs under its service account and she is off the rota.
- 2026-10-18 build: Ask A's second figure as the items still untriaged when the run ended: zero in three of the four
  weeks, so the all-nil response kept them; replaced by the items closed by the run's end.
- 2026-10-18 build: the design stage's Ask B (closed items and closed duplicates by group): a careful replay of the
  changelog under the agreement's definitions cracks the Close transition and the moved reports.
- 2026-10-18 build: Ask B as the items in each group's components at the run's end: once the reports the bridge had not
  yet written at the run's end sit in no group, every cracker path kept 5 to 7 of 8 (pair 46.8 to 51.4).
- 2026-10-18 build: Ask B as the reports moved to the web-compatibility team by group: the created path kept 6 of 8.
- 2026-10-18 build: the bridge writing the old number into Legacy bug on every issue: a cracker joining the old export
  on it landed every ask figure (pair 59.1); a real bridge's catch-up writes through a short payload, now modelled.
- 2026-10-18 build: the portal's shares by exact version, point releases as their own rows: reading each point release
  as a new version moved the call to 6, a messy choice flipping the answer; the portal publishes major versions.
- 2026-10-18 build: a parallel-run report PDF with the weekly side-by-side of both trackers: its weekly items by filing
  week would tie only under the old tracker's filing times, an oracle for Ask A; not built.
- 2026-10-27 determinism repair: Ask B's "arrived in its components" read three ways by a portal judge (the component an
  item came in with, its components at the run's end, every component it held), closed by one agreement sentence on the
  WHAT (each report once, in the group of the component it comes in with) rather than by rewording the prompt; the
  judge's optional note that the write-up name the re-sent copies' exclusion declined, since the old bug number already
  excludes them and the write-up states no figure for them.
- 2026-10-28 portal round 2: a filed forecast test on the old record (two releases two weeks before Patch Tuesday) as
  the whole repair: the restart model led a release-phase model with a Patch Tuesday step by 13 per cent on the weeks to
  the next release, tied it with the next release's own week judged (4,204 against 4,223) and lost with the installs
  carried on from the week before (4,818 against 4,832), so the test needed a record that separates the families; the
  train was re-based instead (three releases three weeks before Patch Tuesday, every reading separated by at least 4 per
  cent and the plain one by 24).
- 2026-10-28 re-cut, first version: the train re-based on a fixed four-week cycle from 46.0 (three releases three weeks
  before Patch Tuesday in a row). The licensed judge (pass 2 on 92f9a766, NOT_DETERMINISTIC, SEND_BACK) found two holes:
  a profile carried from the last release fits a run of releases in the same place in the cycle, so the thread's test
  barely separated it from its own restart build; and holding active installs flat from December, against a seasonal
  swing of seven per cent, dropped the busiest week to 825 (7 triagers). Fixed by the autumn that moves at every
  release, the two per cent swing and the first-use share, every rival and every installs projection asserted.
- 2026-10-28, second re-cut: the forecast left at 920 with the e-mail's over-or-under clause alone: the pass-3 thread's
  own restart model fitted on the autumn files 972 to 976 (9 triagers) and on its August and September windows 953 to
  959 (1,000), and the test prefers the whole record to a 17-week window by under 2 per cent, too thin to rule those out.
- 2026-10-28, second re-cut: the first-use rate lowered directly (912 to 890 and 880) to centre the forecast: every
  day's Poisson draws are redrawn, and the pass-3 thread's autumn fit rose to 981 at 890 (9 triagers); the level is set
  by thinning on its own stream instead, which keeps the record as drawn.
- 2026-10-28, second re-cut: the per-release noise in the first-use rate lowered (0.05 to 0.03 and 0.02) so the
  autumn's excess shrinks: the short-window fits did not narrow (965 to 977 at the top), because the autumn fit's weak
  split between baseline and first-use reports carries as much as the draws do.
- 2026-10-28, judge pass 4 on 60e4764a: the thread left the old tracker's Web Compatibility product out of the triage
  items, reading it as the site tool's reports, and filed 7 (783); the runbook already kept moved reports, but the
  product sharing its name with the site tool's project carried a careful reader past it, and at the band's centre that
  misreading costs a triager; the runbook's counting sentence now names the Web Compatibility and Archive products.
- 2026-10-28, judge pass 5 on c898f73f: NOT_DETERMINISTIC, SEND_BACK. With the test pinned to weekly misses, its thread's
  count-based weekly phase model with a Patch Tuesday term fitted on the last 13 weeks missed fewest (1,121 against its
  restart model's 1,305 to 1,395), and its restart family spread 848 to 977. Measured in the generator: the count-based
  phase model with a Patch Tuesday term on the last 13 weeks misses 1,185, against the restart model's 1,434 with the
  installs carried from the week before; the restart model's 850 needs the judged weeks' own installs, which a forecast
  made the day before a release does not have.
- 2026-10-28, architecture 1 spent (each first-quarter release's adoption built from ordinary restarts plus the Windows
  restart wave after Patch Tuesday, 8 triagers against the default path's 6): the decisive configuration, a release
  shipped on Patch Tuesday, never occurs in the record, so no back-test over the record forces the restart model over a
  model that fits the record's releases as well, and the restart family's own spread across defensible builds (848 to
  977 over fit windows, installs projections and lag forms) is wider than the 120-item band the call sits in; each
  repair met a new competing answer at the next judge (the netted test, the autumn fit window, the moved reports'
  product, the count-based model under an honest installs projection). Re-rooted at the author's word: a forecast whose
  deciding configuration is out of sample can be forced only by naming the method, which files the HOW.
- 2026-10-28, architecture 2 draw: a battery fleet's 2027 fade under a move from frequency response to arbitrage, read
  by cycle depth (prototypes bess.py and bess2.py): throughput and equivalent-full-cycle routes landed within 0.3
  points of the truth on average, and the depth family's fitted exponent came out 1.0 to 1.3 against a true 2.0 on
  half-yearly capacity tests, so neither strength nor determinism.
- 2026-10-28, architecture 2 draw, paper: area burnt in 2027 by time since fire (the unburnt land is a filter and a
  divide, the partial-coverage screen, and megafire years spread the per-class rates); pipeline fatigue crack growth
  (a Paris exponent fitted on in-line inspection sizing noise is a fitted family); trial event projection,
  amounts-weighted pensioner mortality, competing exits, delayed entry, deposit betas and burnout, media reach
  (screened to death in task171, task133, task141, task170 and task174); an Erlang loss on beds, reservoir routing,
  tidal flood days, a dairy calving shift and airport show-up curves (task139, task148, task138, task137 and task178's
  drivers, or a calendar-locked schedule like architecture 1's).
