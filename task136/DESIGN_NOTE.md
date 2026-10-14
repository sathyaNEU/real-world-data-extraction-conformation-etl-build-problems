# task136: Mirrabee Energy, the Yarrabin feeder that gets the FY2027-28 hosting-capacity augmentation (architecture 1, round 2)

Private, never ships. A wave 2 build numbered from seed FC07 (the seed's world, decision and quantity kept: one
accelerated feeder upgrade for rooftop solar above hosting capacity, eight feeders, the 2029 design year, two council
bulk-buys; its published-control architecture never used). Round 1 shipped on 2026-10-12 with the yield carried per
owner-occupied house still without PV; round 2 (2026-10-14) is the 10/10 audit's redesign. Nothing is filed that
recovers a rule, and no record blesses the wrong method.

## Round 2

- **Trigger.** The 10/10 audit (COMPLIANT_WEAK, `scratchpad/audit/task136.md`): carrying a campaign's yield per eligible
  house not yet adopted is the textbook reflex for adoption forecasts and the program terms name the eligible class; a
  rough pool estimate landed the round-1 golden (YRB24 held down to a 3.6 per cent rate); the seven past campaigns
  agreed within 0.6 per cent, a generator constant a denominator search recovers; Ask A's temporary NMIs resolved
  through the re-allocation log and Ask B's repeated battery capacity fell to grouping by connection.
- **What moved.** The decisive step is now a choice a solver who already does the reflex still gets wrong: a bulk-buy's
  yield carried as a multiple of the suburb's own uptake (first applications from its owner-occupied houses in the 12
  months before sign-ups open), not as a share of any pool. The round-1 golden (per untapped owner-occupied house) is
  rung 1, the reflex, and files YRB24. The seven past rates scatter like field outcomes (coefficient of variation
  0.085, 1.03 to 1.35 systems per first application); every pool or contact basis scatters 0.61 to 0.80. The
  campaigns moved to spring 2026 (sign-ups open on 1 September 2026, the day after the base date), so no pool has to
  be projected to an opening. NPP-114 4.2 files the pooled rate (a general method naming no quantity). Four per-feeder
  asks replace the two, each on its own silent device.
- **What stayed.** The world, the decision, NPP-114's base forecast, the eight feeders, the people, the files and their
  layouts, the forum and the forcing event.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task136.json`, architecture v1 at round 2 (round 1 in `lineage`); `guard.py` results under Build record |
| Domain / task type | energy-systems-utilities / load-forecasting (a client domain): a distributor's forecast of rooftop PV on each feeder at the design point of an augmentation is the DER half of its demand forecast |
| Objective | Forecasting & Predictive Modeling: the rooftop PV that will be connected on each feeder at 31 August 2029, a window not yet open, against the spring 2029 minimum-demand hosting capacity |
| Shape | other: the call and its six components (the feeder, its PV over hosting capacity, the runner-up, its excess, the gap, the PV each 2026 bulk-buy adds), the chart's named parts, and four per-feeder DER Register figures on rows the call never reads (32 figures); about 40 criteria, arithmetic in `## Ask sheet` |
| Decision | `pick_one_of_n`, answer unit `named_option` (with its MW figure): which feeder gets the one augmentation |
| Mechanism | gap rule then population (no sentence states the basis; NPP-114 4.1 sends a program to the records of past programs, and the records settle it); pattern none, generators G16 then G14 (`strategies.md` F6: the rate is stationary only in a constructed exposure, each suburb's uptake rebuilt per opening from received dates through the rates roll and the cross-reference); Gate G `method_or_model_selection` (the transfer basis is the method; the seven past campaigns select one, with realistic scatter); strategy `forecast_method_backtest` |
| Layer 2 family / pattern | `field_method`; `own:program-increment-on-local-uptake` (a program's increment carried as an uplift on the area's own baseline adoption, the way DER forecasters model a program, against the addressable-pool reflex) |
| Furniture | forum `line_manager_or_team` (NPP-114 section 6 assigns the one augmentation when the capital works program is compiled; no forum named anywhere), forcing event `budget_or_appropriation`, organisation family `utility_or_infrastructure`, role family `research_desk`, context artifact `capacity_report` (the 2026 hosting capacity assessment), calibration `none`, opening `question-first`, question form `which` |
| Spine | `eg_connection_applications_20260901.csv`, the embedded generation connection register: one row per micro EG connection application at an NMI, new systems and alterations, 2009 to 31 August 2026; constructed |
| Deliverables | `feeder_upgrade_2029.xlsx` (the call, the forecast by feeder, the Solar Streets estimate, the DER Register figures), `yarrabin_pv_vs_hosting_2029.png` (one bar per feeder for its PV at 31 August 2029, its hosting capacity marked) |
| People | drawn with `guard.py names --geo Australia --seed 136`: Wanda Thornton (DER forecasting analyst, the requester), Ian Fletcher (Manager Network Planning, owner of NPP-114; replaced Christopher Sheppard at round 2, see Guard), Julie Cochran (council sustainability programs officer), Bryan Nichols (connections lead), Linda Ruiz (GIS analyst), Nicole Rocha (customer team leader), Tammy Buchanan (consulting engineer); none in the prompt |

**Guard.** `guard.py check` on the round-2 card: WARN, no BLOCK. `overuse.gate_g` (`method_or_model_selection` in five
of the last twelve builds): the honest key, because the decisive step is choosing the basis on which past campaigns
carry to a new suburb and the seven campaigns select one. `guard.py surface` on the round-2 pack blocked
`people.first` on Christopher Sheppard (task450, among the twelve most recent builds, took the first name after round
1); the Manager Network Planning is now Ian Fletcher, drawn by `guard.py names` and clear of every people rule. A first round-2 card (gap population, pattern E, G14 first) blocked on `test.same_puzzle_older` and
`test.same_driver` (pattern E with gap population is spent in eight builds, task500 v2 inside the batch); the honest
keys are gap rule, G16 first (`strategies.md` F6, method selection where the rate is stationary only in a constructed
exposure), which repeat two older builds' signature, differentiated on the card: task185 converts between two
measuring devices at the converted value and task80 v2 dates a status from its conferring event, neither a program's
increment carried on a site's own baseline rate. The nearest driver is this slot's round 1 (0.21, differentiated);
the nearest other is 0.06 (task94 v3).

**Abstraction test.** Stripped of nouns: a scheduled intervention's increment at a new site is carried from its past
runs as a multiple of the site's own recent rate of the outcome, rebuilt per site behind a three-file join, while every
share of a pool (contacted, eligible, eligible and not yet responded) scatters several-fold across the past runs and
hands the site with the biggest untouched pool several times its increment. The nearest drivers on file are the
eligible-pool transfer (this slot's round 1) and corpus-recovered conversion rates (27, 29, 30, 78); here the rate is
not recovered from a rule but chosen by fit among bases, and the basis that fits is the one the reflex skips.

**Data-native sentence.** Merindah's bulk-buys letterbox every address in a suburb, but what a campaign installs
follows the demand already moving there: households about to buy rooftop PV anyway take the negotiated offer and some
neighbours join them, so each past campaign installed about 1.17 systems for every first application its suburb's
owner-occupied houses lodged in the year before sign-ups opened, while Bindarra Waters (5,139 owner-occupied houses
without PV, 52 first applications a year) and Wattleview (2,676 without PV, 209 a year) sit at opposite ends of pool
and pace.

**Sources read, one line each.** `product-analytics/feature-adoption-diffusion-modeling/2` teaches the eligible
denominator at risk; here that is the reflex, and the move is the one beyond it (a program's increment rides the
area's own adoption rate). `guard.py mechanisms --objective forecasting`: hazards by time since entry (134), selection
on the outcome (124), claims maturity (130), recycling terms (501), conversion rates recovered from a corpus (27, 29,
30, 78), censored delays (31, 99), a slowest sub-unit (52), a class of money beside a drop (137 round 2), the eligible
pool (136 round 1); none carries an intervention's yield on the site's own baseline rate.
`stumping/references/client/measured-drivers.md`: the held tasks put the decisive rung upstream of every graded
figure, a construction behind a join whose partial versions fit no better than the raw rate; here every pool and
contact basis fits several-fold worse than the uptake basis, and the reflex itself is a rung. The seed's header (FC07)
for the world only.

**World.** Mirrabee Energy is a regional electricity distributor in south-east Queensland. Its Yarrabin zone
substation supplies eight 22 kV feeders, YRB21 to YRB28, in Merindah's western growth corridor (50,896 NMIs). Merindah
City Council's Solar Streets program has run a bulk-buy in one suburb a year since 2018 (two in 2022, none in 2020): a
letterbox drop to every address, information sessions, one appointed installer, a twelve-week sign-up window and
installations over the following months. The council's 2026-27 budget runs two campaigns this spring (sign-ups 1
September to 27 November 2026): Bindarra Waters, a 2018 to 2023 estate on YRB24, and Wattleview, a 2019 to 2023 estate
on YRB27. NPP-114 (revision 3, March 2026) sets how rooftop PV is forecast for an augmentation; the 2026 hosting capacity
assessment gives each feeder's hosting capacity for the spring 2029 minimum-demand case; the FY2027-28 capital works
program funds one accelerated hosting-capacity augmentation, assigned by NPP-114 section 6. As-of dates: the connection
register, the network model and the DER Register extract at 31 August 2026 (run 1 September 2026); the council's
letter of 14 August 2026; the hand-off 12 October 2026.

## Default path

1. Read NPP-114. From the connection register take each NMI's latest connected configuration (an alteration carries
   the NMI's whole system), inverters of migrated rows from the legacy table, each NMI on its feeder in the network
   model at 31 August 2026: connected capacity at the base date.
2. Build NPP-114's trend: the FY2023-24 to FY2025-26 average yearly increase in connected capacity less the program
   systems first connected that year, carried three years to 31 August 2029.
3. For the two 2026 bulk-buys take the council's participation rate, the seven past campaigns' systems installed over
   their homes letterboxed pooled as NPP-114 4.2 sets (505 over 26,090), onto the letter's drops (6,240 in Bindarra
   Waters, 5,240 in Wattleview), each system at the feeder's FY2025-26 average new inverter (NPP-114 4.3).
4. Subtract each feeder's spring 2029 hosting capacity and pick the largest excess (NPP-114 5.1, 6.1).

Ends on: YRB24, about 1.8 MW over its hosting capacity at 31 August 2029 (Bindarra Waters adds 0.8 MW, Wattleview 0.7 MW; runner-up YRB22 at 1.2).
Golden: YRB27, about 1.9 MW over its hosting capacity (Bindarra Waters adds 0.4 MW, Wattleview 1.7 MW; runner-up YRB24 at 1.4, gap 0.5).

## Stump sentence

A competent solver builds NPP-114's base forecast, carries the seven past bulk-buys onto the 2026 suburbs at the
council's pooled participation rate per home letterboxed and files YRB24 at about 1.8 MW over hosting capacity (Ends
on), and the textbook correction, per owner-occupied house still without PV when sign-ups open, files YRB24 at 3.0;
the step that lands both there is carrying a campaign's yield on a pool of houses instead of on the suburb's own
uptake (about 1.17 systems per first application its owner-occupied houses lodged in the year before sign-ups
opened), which gives Bindarra Waters' large, slow estate two to five times its campaign and Wattleview's fast one less
than half of its: the golden is YRB27 at about 1.9 MW.

## Three rules

- **Task type:** energy-systems-utilities / load-forecasting, the DER component of a distributor's design-point
  feeder forecast for a hosting-capacity augmentation; load-forecasting serves Forecasting & Predictive Modeling.
- **Domain test:** the deciding quantity is each feeder's forecast rooftop PV (micro EG inverter capacity) connected at
  31 August 2029 against its spring 2029 minimum-demand hosting capacity, with each council bulk-buy's increment
  forecast as an uplift on the suburb's own baseline uptake estimated from past programs, which is how DER forecasters
  carry a program's increment, not as a share of an addressable roof pool.
- **Swap:** "which of eight school catchments gets the extra classroom block, counting two enrolment drives": inverter
  ratings, NPP-114's connected capacity with alterations replacing configurations, hosting capacity at spring minimum
  demand, owner-occupied houses on a rates roll and first PV applications have nothing to attach to, and a drive's
  yield per first rooftop application stops making sense.
- **Layer 1:** the connection register at application grain (alterations carrying the NMI's whole system; withdrawn,
  under-assessment and approved-not-connected applications; removals), 2019 migrated rows whose inverters sit in a
  legacy equipment table, the feeder recorded at application after five load transfers (2023 to 2025), the rates roll
  keyed by property number and joined to NMIs only through the GIS cross-reference (dual-occupancy NMIs, abolished
  NMIs of rebuilt houses), the council's workbook in its own layout; on the ask paths a device-grain DER Register extract
  (checksum NMIs from the newer portal, builders' temporary NMIs and the re-allocation log, decommissioned connections,
  the feeder stamped at lodgement, per-product battery lodgement, the older portal's per-inverter field). Each is what
  these systems produce; read by the filed rules and the dictionary each gives back the world's own figures (R2,
  asserted), and none decides the call.
- **Layer 2:** `field_method`: the exposure on which a past program's increment transfers to a new area; the shortcut
  carries it per contacted home (the council's rate) or, as the textbook correction, per eligible house not yet
  adopted; the expert carries it on the area's own adoption pace, the only basis on which the seven past campaigns
  agree (coefficient of variation 0.085 against 0.61 to 0.80).
- **Decisive step:** carrying the Solar Streets yield as a multiple of each suburb's own first applications from
  owner-occupied houses in the 12 months before sign-ups open (1.172 pooled; Wattleview's 209 give 1.7 MW, Bindarra
  Waters' 52 give 0.4 MW) instead of per home letterboxed or per owner-occupied house still without PV.
- **Not semantics:** every field, code and definition (status, land use 02, rating R1, inverter_kw_ac, program_ref,
  received_date, homes letterboxed) is read the same on the default, reflex and golden paths; they differ only in the
  quantity the yield is carried on, and the per-letterbox and per-pool routes read everything correctly.
- **Not rule application:** NPP-114 4.1 sends a program to the records of past programs and 4.2 says only that a rate
  from them is pooled (total over total); no filed sentence names the quantity, so executing every clause leaves the
  basis open, and the per-letterbox rate executes them all and files YRB24.
- **Analyst test:** a strong analyst who collapses alterations, joins legacy inverters, places NMIs on the network model,
  builds NPP-114's trend and pools the past campaigns' rate per home letterboxed files YRB24 at about 1.8 MW (Ends on);
  per owner-occupied house without PV at the opening (the textbook reflex) files YRB24 at 3.0 MW, and fitted models on
  the obvious covariates (penetration, pool, letterboxes, houses) file YRB24 at 1.7 to 2.9 MW.
- **Estimand:** the prompt, NPP-114 2.2, 3.1, 3.2, 4.1 to 4.4, 5.1 and 6.1 and the council's letter fix the
  population (micro EG at NMIs the 31 August 2026 network model places on each Yarrabin feeder, the 2026 campaigns'
  systems included though none is yet lodged), the outcome (connected capacity at 31 August 2029 less the spring 2029
  hosting capacity), the unit (MW to one decimal), the comparison (the largest excess) and the pooling (4.2).
- **No decoy:** no file states a 2029 forecast, an excess, a participation rate, an uptake or a campaign forecast; the
  council's summary reports past campaigns' history, equal to the register's program-coded connections; no memo,
  draft, briefing or stakeholder figure argues for a feeder or a basis.
- **No certified replay:** no certified or published figure pins the method; the seven campaigns' installed counts are
  the history the program component is estimated from, the basis is chosen by how well each fits them (as a forecaster
  selects a model on past runs), and NPP-114 4.2 fixes only the pooling.
- **Lesson:** a program's increment transfers as a multiple of the demand already moving in its area, not as a share of
  who could still buy: a large untouched pool with slow uptake takes a small campaign and a fast-adopting suburb with
  half the pool a large one; no build on file teaches carrying an intervention's yield on the site's own baseline rate
  against the eligible-pool reflex (this slot's round 1 taught the pool, which is now the trap).

## Gate G

- **Litmus.** No. Every file is correct; no stakeholder states a number the task overturns; no file states a forecast,
  a rate, an uptake or an excess.
- **Primary mechanism:** `method_or_model_selection` (the transfer basis; the seven past campaigns select one).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test (asserted, R3a).** On the world's own records, before any file is written, the per-letterbox route
  files YRB24 at 1.8 MW and the reflex YRB24 at 3.0; the uplift alone files YRB27 at 1.9 (R3b).
- **Deletion test.** Delete the distractors, the DER Register extract and the re-allocation log: the call recomputes
  unchanged (asserted) and the default path is still wrong.
- **Lens swap.** The default and the golden are two transfer bases for the same seven campaigns, not one population
  under two lenses; only one reproduces the seven.
- **No artifact ranks or prices the decision.** The council's log reports what each campaign did (letterboxed,
  registrations, assessments, contracts, systems installed); the assessment gives hosting capacity and minimum demand.

## Readability screen

Six tests per rung: 1 filed sentence; 2 schema; 3 reflex; 4 control or corpus; 5 hygiene battery; 6 linear. Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 per home letterboxed (the council's participation rate on the letter's drops) | the log and the letter carry the counts | the log's `Homes letterboxed` | yes | no | no | yes (a ratio of two reported figures) | readable |
| R1 per owner-occupied house without PV when sign-ups open (the textbook reflex, round 1's golden) | the program terms name owner-occupiers of houses | the rates roll's land use and rating | yes (eligible and not yet adopted) | no: the seven scatter 0.71 on it | no | no | readable |
| R1a per owner-occupied house, per address without PV, per untapped house on the feeder, an average campaign | the terms; the register | the rates roll, the register | yes | no: 0.61 to 0.80 | no | partly | readable |
| R1b fitted models on the obvious covariates (penetration, pool, letterboxes, houses) | no | the same columns | yes (a regression on what the files carry) | no | no | no | readable |
| R2 (decisive) the yield as a multiple of each suburb's own first applications from owner-occupied houses in the 12 months before sign-ups open | no sentence names uptake, a first application or a quantity; NPP-114 4.1 sends to the records and 4.2 says only to pool | no column holds a suburb's uptake; it is built per suburb and per opening from received dates, the rates roll and the cross-reference | no: the reflexes are R0 and R1; uptake is the outcome being forecast, not a denominator a solver reaches for | the seven campaigns fit it (0.085) only once it is built; nothing scores it before | no | no | silent |

The decisive rung is silent because it is not a denominator in any file's vocabulary: every quantity the files name
(letterboxes, houses, houses without PV, addresses) is a pool, and each fails the seven campaigns several-fold; the
uptake that fits is the time series of the outcome itself, cut per suburb at each opening.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. `checks.py` asserts each row (the
alternative computed and shown to move a figure or to converge, and the ruling sentence found in the pack).

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "rooftop PV" on a feeder | all micro EG (30 kVA or less) at NMIs the network model places on the feeder, residential and business | residential NMIs only | YRB27 at 1.3, runner-up YRB24 at 1.0 | NPP-114 2.1 ("at a residential or business NMI") and 2.2, asserted in the PDF; every register system is 30 kW or less |
| SF2 | a system's capacity | the inverter capacity (kW AC) of the NMI's latest connected configuration | every connected application summed; panel capacity | summed: YRB22 at 3.9; panel: YRB27 at 6.2 over YRB22 | NPP-114 2.2 ("An alteration replaces the configuration it alters"; "inverter capacity (kW, AC rating)") and the dictionary's `inverter_kw_ac` |
| SF3 | migrated rows (blank `inverter_kw_ac`) | the inverter from the legacy equipment table on the legacy application number | the rows dropped; their panel capacity | dropped: YRB24 at 0.7; panel: YRB22 at 2.8 | NPP-114 2.2 (each NMI's micro EG, at inverter capacity) and the dictionary ("Blank on applications migrated from the legacy system"), asserted |
| SF4 | "connected" at a date | status Connected, connection date on or before the date, not removed by it | approved but not connected counted | same call (YRB27 at 2.1); every base moves under 2 per cent | NPP-114 2.2 |
| SF5 | the feeder of an NMI | the network model at 31 August 2026 | the feeder recorded on the application | same call (YRB27 at 2.5, runner-up YRB23) | NPP-114 3.1 |
| SF6 | the base date | 31 August 2026, the extracts' as-at date | 30 June 2026; 30 September 2026 | 30 June: same call (1.6, gap 0.3); no record exists after 31 August | NPP-114 3.1 and the extracts' dates (the manifest) |
| SF7 | the trend | the average yearly increase in connected capacity over FY2023-24 to FY2025-26 less program systems first connected that year | new connections only; program systems left in | same call under both (1.8; 1.9 with runner-up YRB21) | NPP-114 3.2 |
| SF8 | the years carried | three | 3.25 or 2.92 | same call, figures move | NPP-114 2.4 and 3.2 |
| SF9 | "program system" | an application carrying a Solar Streets reference; equal to the council's systems installed for every campaign | contracts signed | same call (2.0; Wattleview 1.8 MW) | NPP-114 2.3 (systems installed under a program) |
| SF10 | each added system's size | the feeder's FY2025-26 average new inverter | the past campaigns' own average (6.80 kW) | same call and figures | NPP-114 4.3 |
| SF11 | a first application's date | received date of the NMI's earliest application other than a withdrawn one | the first connection date | converges: every graded figure (asserted) | the records converge |
| SF12 | whose first applications | the suburb's owner-occupied houses (rates roll land use 02, rating R1, through the cross-reference) | every residential address in the suburb | converges | the records converge |
| SF13 | the window | the 12 months before sign-ups opened | the yearly average over 24 or 36 months | converges | the records converge |
| SF14 | a suburb | the rates roll's locality | the network model's locality | same rows | the records converge |
| SF15 | the estimator on the seven campaigns | pooled, total systems over total first applications | the mean or median of the seven rates; a regression through the origin or with an intercept | same call under every one (YRB27 at 1.81 to 1.92 across the windows) | NPP-114 4.2 ("total systems divided by their combined total of the quantity the rate is expressed per"), asserted in the PDF |
| SF16 | transfer per home letterboxed (R0, the default) | refused | the council's participation rate, pooled | YRB24 at 1.8 | the records: the seven rates scatter 0.715 and the pooled rate misses Glenmorrow by 222 per cent |
| SF17 | transfer per owner-occupied house | refused | | YRB24 at 2.2 | the records: 0.607; misses Bunya Ridge by 157 per cent |
| SF18 | transfer per owner-occupied house without PV at the opening (R1, the reflex) | refused | | YRB24 at 3.0 | the records: 0.713; misses Tallowwood Rise by 162 per cent |
| SF19 | transfer per address without PV; per untapped house on the feeder | refused | | YRB24 at 2.0 and 2.2 | the records: 0.797 and 0.786 |
| SF20 | an average campaign; a regression on penetration; a regression on pool, letterboxes and houses | refused | | YRB24 at 1.5, 1.7 and 2.9 | the records: an average campaign misses Glenmorrow by 280 per cent; the regressions fit seven points with two or four parameters and carry no stable rate |
| SF21 | hosting capacity | the assessment's spring 2029 minimum-demand case | the 2026 case beside it | YRB24 by 0.1 MW | NPP-114 5.1 ("for the design year's spring minimum-demand case") and 2.4, asserted; the prompt's "at 31 August 2029" |
| SF22 | the excess, the runner-up and the gap | unrounded, ranked, rounded once to 0.1 MW | rounded figures subtracted | converges (asserted) | NPP-114 6.1 and 7.1 |
| SF23 | a migrated row's inverter | the equipment row with the register's legacy application number | file order, panel size, summed, first or last row | converges: every number issued once on each side | the records converge |
| SF24 | a withdrawn application | not a first application: nothing was connected under it | any status counted | converges (same graded figures) | the dictionary's status definition, asserted |
| SF25 | the uplift as a hazard | first applications in the year before | the year-before hazard on the pool times the pool at the opening; first applications per house-year at risk | converges | the records converge |
| SF26 | "how much PV each bulk-buy will add" | its systems at the feeder's FY2025-26 average new inverter, in MW | a count of systems | the prompt asks how much PV and gives MW to one decimal; NPP-114 4.3 sizes each system | the prompt and NPP-114 4.3 |

The stump is none of these rows: a careful reader reads every one the same way, and the default path reads them all
correctly. SF16 to SF20 are methods, listed so that each competing basis is priced and refused by the records.

## Ladder

| Rung | Basis | Winner and excess | Runner-up | YRB27 | Bindarra Waters, Wattleview | Dies to |
|---|---|---|---|---|---|---|
| R0 (default) | per home letterboxed, pooled | YRB24 1.784 | YRB22 1.209 (margin 1.48) | 5th, 0.902 | 0.785 MW, 0.707 MW | the seven rates scatter 0.715 |
| R1 (the reflex) | per owner-occupied house without PV at the opening | YRB24 3.037 | YRB27 1.333 (margin 2.28) | 2nd | 2.038 MW, 1.138 MW | 0.713; the uptake of the 2026 suburbs is four to one against their pools |
| R2 (decisive) | per first application from owner-occupied houses in the 12 months before | YRB27 1.902 | YRB24 1.395 (margin 1.36) | 1st | 0.396 MW, 1.707 MW | (golden) |

- **Position.** YRB27 is 5th on R0, 2nd on R1 only (YRB24 leads it by 2.28 times), 1st on R2. Every correction from
  R0 to R1 raises YRB24 (Bindarra Waters' pool); only the decisive move reverses it.
- **Dominance.** Wattleview's uptake is 4.02 times Bindarra Waters' (209 against 52 first applications), Bindarra
  Waters' pool 1.92 times Wattleview's (5,139 against 2,676 houses without PV): 4.02 against 1.2 x 1.92 = 2.30.
- **Rivals (asserted, 39 routes).** Every pool and contact basis under every estimator (pooled, mean, median, through
  the origin, OLS), an average campaign, a regression on penetration, regressions on pool with letterboxes and houses,
  and one-campaign analogs (Tallowwood Rise, Paperbark Grove, Bunya Ridge per letterbox, house or pool) file YRB24
  (none files YRB22 or YRB27 except no campaign at all, YRB22 at 1.2); YRB27 sits at least 0.34 MW under each winner;
  none files the golden's runner-up with its figure.
- **The uplift corridor (asserted).** The seven readings of the uplift (12, 24 or 36 months; received or connected;
  owner-occupied or every address; the year-before hazard times the pool; house-years at risk) under NPP-114 4.2's
  pooling all file YRB27 1.9, YRB24 1.4, gap 0.5, Bindarra Waters 0.4 and Wattleview 1.7: excess 1.874 to 1.922, the
  runner-up 1.372 to 1.421, gap 0.476 to 0.530, Bindarra Waters 0.373 to 0.421, Wattleview 1.679 to 1.727, each at
  least 0.02 MW inside its bin.
- **Worth on the graded figures.** R0 to R2 moves the call, the runner-up (YRB22 to YRB24), the gap (0.6 to 0.5) and
  both bulk-buys (0.8 to 0.4, 0.7 to 1.7); R1 to R2 moves the same five.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | micro EG at NMIs on the eight Yarrabin feeders in the network model at 31 August 2026 (NPP-114 2.2, 3.1); members not yet observed (the 2026 campaigns' systems, the trend's systems to 2029) are the estimand, projected; filed literally |
| 2 | Unit of account | a system is an NMI's connected configuration (2.2); a campaign's yield counts systems (program references, SF9); the uplift counts NMIs' first applications (SF11, SF12) |
| 3 | Attribution window | the trend's financial years; program systems leave the trend in the year first connected (3.2); every past program system connected within nine months of its opening and the two inside the trend window within one financial year each (asserted) |
| 4 | As-of dating | the base date 31 August 2026 (3.1); the 2026 openings are the next day, so the year before each opening ends on the base date (asserted) |
| 5 | Version basis | one register extract; alterations replace configurations (SF2) |
| 6 | Denominator | the decisive method (R2); refused bases priced in SF16 to SF20; not a reading |
| 7 | Weighting | pooled (NPP-114 4.2; SF15) |
| 8 | Window length | the trend window filed (three complete financial years); the uplift's 12 months, with 24 and 36 converging (SF13) |
| 9 | Boundary inclusivity | connection dates on or before the base date; first applications in [opening less 365 days, opening). Records sit on the edges (connections on the base date, first applications on a window edge); the base date read exclusively, the financial years a day late and the window read (open, close] change no graded figure (C1, asserted) |
| 10 | Rounding path | carried unrounded, rounded once (7.1); the gap equals the difference of the rounded excesses (asserted) |
| 11 | Tie-break | none needed: YRB27 leads by 0.5 MW and the runner-up leads third place by 0.19 MW (asserted at 0.1) |
| 12 | Maturity and censoring | every past program system connected by the base date (none pending, asserted); the 2026 campaigns close on 27 November 2026, inside NPP-114 4.1's six months before the design point; no 2026 program reference is lodged yet (asserted) |
| 13 | Order of operations | alterations collapsed before summing; first applications per NMI before counting; C1 on the rest |
| 14 | Row order | changes nothing (asserted) |
| 15 | Duplicate resolution | one configuration per NMI (SF2); one first application per NMI; no property with two NMIs in a campaign suburb (asserted) |
| 16 | Identity normalisation | NMIs are ten characters in the register, the network model and the cross-reference (asserted); legacy numbers pair one to one (SF23) |
| 17 | Netting against gross | removals leave connected capacity (2.2); no export netting |
| 18 | Dimensional units | kW AC, MW for reporting; panel kWp never enters (SF2, SF3) |
| 19 | Code and status semantics | status, land use and rating codes defined in the dictionary (SF24) |
| 20 | Integerisation | the campaigns' systems are expected counts, carried unrounded into MW; no integer step |
| 21 | Clause scope | NPP-114 4 applies to each program scheduled before the design point and confirmed in writing (4.4): the two 2026 campaigns (the council's letter) |
| 22 | Forward window contents | the council's letter gives each 2026 campaign's suburb, sign-up dates (1 September to 27 November 2026, asserted) and letterbox drop; NPP-114 3.2 carries the trend to the design point |

## Literal reader

Executed word for word, the prompt, NPP-114 (2.1 to 7.1), the council's letter and the hosting capacity assessment
define the call as the feeder whose micro EG connected at 31 August 2029, forecast as the connected capacity at 31
August 2026 plus three years of the filed trend plus the systems each 2026 program will add at the feeder's FY2025-26
average new inverter, exceeds its spring 2029 hosting capacity by the most. Every term in the fork table resolves to
one reading or converges. The one step the text leaves open is how many systems each bulk-buy will add, which NPP-114
4.1 sends to the records of past programs and 4.2 pools; those records show each past campaign installing 1.03 to 1.35
systems (1.172 pooled) for every first application its suburb's owner-occupied houses lodged in the year before its
sign-ups opened, and scattering several-fold on every pool or contact basis (SF16 to SF20). The only number the records
indicate for the 2026 campaigns is that rate on their own suburbs' first applications in the year to 31 August 2026,
which is the golden. No filed sentence prices a program per letterbox, per house or per untapped house.

## Oracles

- **The council's systems installed** equal the register's program-referenced connections for every campaign: a control
  on the count, true under every basis (the numerator of all of them).
- **The council's homes letterboxed** and the letter's drops: R0's denominator; they tie under every basis.
- **The hosting capacity assessment**: hosting capacity and minimum demand only; no connected capacity, headroom or rank.
- **The DER Register extract and the re-allocation log** (the asks' path): no rung reads them. None ties only under the
  golden.

## Ask sheet

**Main call's declared row population:** every row of `eg_connection_applications_20260901.csv`,
`nmi_network_model_20260831.csv`, `nmi_property_xref_2026.csv`, `merindah_rates_roll_2026-27.csv` and
`legacy_inverter_equipment.csv`, the council's program summary and letter, NPP-114 and the hosting capacity assessment.
Device and hazard rows in it: 0. The four asks read `der_register_extract_yarrabin_20260901.csv` and
`nmi_reallocations_2019-2026.csv`, which no rung of the call reads, and the network model for placement (device-free);
the call is asserted unchanged with both ask files emptied, and the connection register carries no replaced or
eleven-character NMI. Each ask is a measure every feeder carries (its DER on the national register) that the call does
not turn on; none is keyed to the call, its construction or its figures; no two share a primary device. No sentence in
the pack adjudicates a device: the dictionary states each field flatly.

**Ask 1. For every feeder, how many active DER Register sites it supplies** (8 counts; `calc.ask_d`).
- H18 home: the market register's count of DER sites on each feeder, beside the distributor's own forecast; a measure
  every feeder carries that the call never reads.
- Golden: YRB21 2,323; YRB22 3,448; YRB23 1,713; YRB24 702; YRB25 717; YRB26 1,996; YRB27 2,729; YRB28 1,781.
- Construction: a site is the premises' NMI (ten characters; a builder's temporary supply NMI read at the NMI that
  replaced it in the re-allocation log) with at least one active AC connection, placed on the feeder the network model
  shows supplying it at 31 August 2026 ("it supplies"; the network model's `feeder`: "Feeder supplying the NMI at 31
  August 2026"). An abolished NMI no feeder supplies drops out.
- Primary device (D2, a label stored before a silent switch): Mirrabee's extraction stamps each AC connection with
  the feeder its NMI was on when the connection was lodged; five load transfers (2023 to 2025) moved streets between
  feeders, so 438 active connections at 432 sites carry a feeder that no longer supplies them, and every feeder gains or
  loses some. The dictionary says only "Feeder, added by Mirrabee's extraction." The tell is the register's
  `feeder_at_application` against the network model for the same NMIs, a cross-file cut.
- Hazards: H1 checksum NMIs (3,621 of 20,712 rows lodged through the newer portal with eleven characters); H2
  temporary NMIs (1,149 rows at 959 connections lodged against a builder's supply); H3 several active connections at
  one site (an installer who left the old connection active after an alteration); H5 abolished NMIs.
- Path (5 files, 9 columns): the DER extract (`ac_connection_id`, `nmi`, `ac_connection_status`, `feeder`), the
  re-allocation log (`old_nmi`, `new_nmi`), the network model (`nmi`, `feeder`), the dictionary.
- Stops (measured, each off the golden on all 8): the extract's own feeder, YRB27 2,830 and YRB23 1,904; active AC
  connections counted, YRB26 2,135; NMIs not carried through the re-allocation log, YRB27 1,977 and YRB24 586; NMIs as
  lodged with the extract's feeder, YRB25 794.
- Lazy delta: the natural pipeline (filter Active, count distinct NMIs by the extract's feeder) misses 8 of 8.
- Realism: a distributor filters the national register to one zone substation by the feeder in its NMI history at
  each lodgement; a later load transfer leaves the stamp behind.

**Ask 2. How many of those sites were first lodged in FY2025-26** (8 counts; `calc.ask_a`).
- H18 home: the new DER sites on each feeder over the last financial year, the market register's view of the growth
  the trend carries.
- Golden: YRB21 82; YRB22 130; YRB23 65; YRB24 68; YRB25 44; YRB26 35; YRB27 252; YRB28 62.
- Construction: a site's first lodgement is the earliest `registered_date` of any AC connection at the site,
  decommissioned connections included; counted where it falls in 1 July 2025 to 30 June 2026.
- Primary device (D8, an anchor on the current record, not the first): an alteration lodges a new AC connection and the
  old one is decommissioned (1,551 decommissioned connections), so a site's active connection is often younger than the
  site; read off the active connections, every altered site counts as new. The tell is the decommissioned rows at the
  same NMI, which a pipeline filtering Active first never keeps.
- Over-cleaning half: none needed; the feeder stamp does not move this ask (every connection lodged after the last
  transfer is stamped right, asserted), so the stamp's repair earns nothing here.
- Hazards: H1 (an old connection under ten characters and its replacement under eleven read as two sites), H2.
- Path (5 files, 8 columns): the DER extract (`ac_connection_id`, `nmi`, `ac_connection_status`, `registered_date`),
  the re-allocation log, the network model, the dictionary.
- Stops: the active connections' own registration, YRB27 278, YRB26 76 (all 8 off); NMIs as lodged, YRB22 200 (all 8
  off); not carried through the re-allocation log, YRB27 266 (4 of 8 off).
- Lazy delta: the natural read misses 8 of 8.
- Realism: the DER Register keeps a replaced connection as Decommissioned beside its replacement; a register of AC
  connections dates each connection, never the site.

**Ask 3. The inverter capacity at those sites** (8 figures, kW to the nearest 10; `calc.ask_c`).
- H18 home: the market register's installed inverter capacity on each feeder, the reconciliation partner of NPP-114's
  connected capacity.
- Golden: YRB21 14,000; YRB22 20,680; YRB23 10,860; YRB24 4,730; YRB25 4,850; YRB26 10,830; YRB27 18,040; YRB28
  10,340 kW.
- Construction: each active AC connection's inverter ratings summed, except a two-inverter connection lodged on the
  older installer portal (before July 2024), whose every inverter row carries the connection's total (its rating is
  the model's nameplate times its rows), counted once.
- Primary device (D3, a field's meaning set by the portal's date): the older portal asked one rating per inverter and
  installers entered the connection's total there; 326 active two-inverter connections carry it, beside 74 newer ones
  rated per inverter. Summing rows doubles the old ones; the duplicate sweep (identical rows dropped) halves the new
  ones. The tell is the model name's rating (`Primo 5.0` on a 10.00 kW row) and the register's `inverter_kw_ac`, each in
  another column or file.
- Hazards: H2 (all 8), H4 the feeder stamp (all 8), H3 (an old connection left active counts, both are active).
- Path (6 files, 11 columns): the DER extract (`ac_connection_id`, `nmi`, `device_type`, `model`, `rated_power_kw`,
  `ac_connection_status`, `registered_date`), the re-allocation log, the network model, the connection register
  (`inverter_kw_ac`, the referee), the dictionary.
- Stops: rows summed, YRB22 21,597 (all 8 off); duplicate rows dropped or one row per connection, YRB22 20,610 (all 8
  off); the extract's feeder, YRB25 5,260 (all 8 off); not carried through the re-allocation log, YRB27 13,012 (all 8
  off).
- Lazy delta: the natural sum misses 8 of 8; the hygiene repair misses 8 of 8.
- Realism: a portal form with one rating field per inverter, filled with the system's total until the form changed,
  is ordinary.

**Ask 4. The battery storage at those sites** (8 figures, kWh to the nearest 10; `calc.ask_b`).
- H18 home: storage that can absorb a feeder's midday PV, reported beside each feeder's PV.
- Golden: YRB21 1,940; YRB22 2,410; YRB23 1,310; YRB24 750; YRB25 650; YRB26 1,710; YRB27 2,950; YRB28 1,380 kWh.
- Construction: per active battery AC connection, the module rows summed, except a Sungrow SBR stack, whose installer
  app lodges one device per module each carrying the stack's total, counted once.
- Primary device (D6, an event's quantity on every line it covers, per product): BYD and GoodWe stacks lodge one row
  per module at the module's size; Sungrow SBR stacks (170 of 1,098 active battery connections) one row per module at
  the stack's total. Summing rows multiplies every SBR stack by its modules; one row per connection drops every other
  stack's modules; the duplicate sweep does both. The tell is an SBR site summing to 29 to 80 kWh against the
  register's `battery_kwh` for the NMI.
- Hazards: H2 (5 of 8), H4 (6 of 8), H5.
- Path (6 files, 10 columns): the DER extract (`ac_connection_id`, `nmi`, `device_type`, `model`,
  `storage_capacity_kwh`, `ac_connection_status`), the re-allocation log, the network model, the connection register
  (`battery_kwh`, the referee), the dictionary.
- Stops: rows summed, YRB27 4,689 (all 8 off); one row per connection, YRB27 2,237 (all 8 off); the extract's feeder,
  YRB22 2,388 (6 of 8 off); not carried through the re-allocation log, YRB27 2,342 (5 of 8 off).
- Lazy delta: the natural sum misses 8 of 8; the hygiene repair misses 8 of 8.
- Realism: installer commissioning apps differ by brand in how they lodge a modular battery; a register holds what each
  app sends.

**Hazard table**

| Hazard | Root cause | Asks moved (measured) |
|---|---|---|
| H1 checksum NMIs | the newer installer portal lodges the NMI with its checksum digit | sites, first lodged, inverter, storage (as lodged: all 8 on each) |
| H2 temporary NMIs | builders' systems lodged against the temporary supply | sites 8, first lodged 4, inverter 8, storage 5 |
| H3 several active connections at a site | an installer left the old connection active | sites (counted by connection, all 8) |
| H4 the feeder stamped at lodgement | load transfers after lodgement | sites (primary), inverter 8, storage 6; first lodged 0 |
| H5 abolished NMIs | knock-down rebuilds; the DER record left active | sites, inverter, storage (with H4) |

**One reading of "at those sites".** The capacity and storage are the DER Register's own records for its active
connections at those sites (the register the sites are counted on); the connection register describes the same
systems on another population (approved installations not yet connected, removals the DER Register still shows active,
old connections an installer left active), so its totals at the same NMIs differ on every feeder's inverter capacity
and on five of eight feeders' storage and serve only as the referee below.

**Referee.** The connection register's `battery_kwh` and `inverter_kw_ac` for an NMI arbitrate the per-row conventions
(SBR rows against the NMI's battery, asserted for 90 per cent or more of matched stacks; old-portal rows against the
NMI's inverter capacity) without handing over a level: the register's totals at the DER sites differ from the golden
on every feeder's inverter capacity and on 5 of 8 feeders' storage (asserted through the stops).

**The cracker sheet.** The cracker filed YRB27 at 1.9 MW, ran the hygiene battery (NMI formats normalised, unmatched
NMIs resolved through the re-allocation log, exact duplicates, fan-out, counts that tie) and executed every filed rule:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, 8 site counts | active connections, NMIs normalised and re-allocated, distinct sites by the extract's feeder | the feeder stamped at lodgement moved 432 sites | miss |
| Ask 2, 8 counts | the active connections' registration dates by site | the site's first lodgement sits on a decommissioned connection | miss |
| Ask 3, 8 capacities | inverter rows summed after dropping exact duplicate rows | the newer portal's per-inverter rows are halved; summing instead doubles the older portal's | miss |
| Ask 4, 8 storage totals | battery rows summed after dropping exact duplicate rows | every modular stack loses its modules; summing instead multiplies the SBR stacks | miss |
| Chart (recommendation block) | the bars from the forecast | carried by the main call, scored with it | outside |

The mirror sheet (the same response stopped at R1, YRB24) differs only on the recommendation criteria: no ask couples
to the call, and the mirror's runner-up (YRB27) is not the golden's.

Mirror leakage: 8 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 36 recommendation (the feeder, its excess, the runner-up and its excess, the gap,
the two bulk-buys, the chart's named parts), 9 instruction following, 55 asks over 32 figures (1.72 each). The cracker
keeps about 8 per cent of the ask weight: C = 36 + 9 + 4.4 = 49.4. The mirror keeps r of about 4 (the files and the
chart's structure; no wrong route files the golden's runner-up with its figure, asserted): S = 4 + 9 + 4.4 = 17.4, a
pair of 33.4. The most obvious device is Ask 1's stamp (a cracker who places sites on the network model's feeder after
joining it for the NMIs cracks it): it adds 12.65 (8 figures, a quarter of the ask weight, less the credit already
counted) and the pair rises to 39.7. Both top responses on the call with no device cracked: 49.4. A cracker who also
takes Ask 2's anchor reaches 46.0.

Pair ceiling: 39.7

## Prompt

`prompt.txt`, rewritten at round 2 and gated by `voice-check.py` (in `precut.py`, 888 characters): the call as a
question with its forcing facts (the FY2027-28 program, NPP-114, the council's spring 2026 bulk-buys), the workbook's
figures (the excess at 31 August 2029, the runner-up and the gap, how much PV each bulk-buy adds), the four per-feeder
DER Register figures ("how many of them", zero a grammatical answer, H23), the chart's named parts and the rounding
once at the close (megawatts to one decimal, inverter capacity to 10 kW, storage to 10 kWh).

## Build record

Stage 3 of round 2, built 2026-10-14 by `python3 task136/generator/build.py` (pack, goldens, `metadata.json`,
`generator/figures.json`, `checks.py`, `verify.py`, a second full build compared byte for byte, `target.zip`).

- **The call.** YRB27, 1.902 MW above its spring 2029 hosting capacity (forecast 25.202 MW against 23.30); runner-up
  YRB24 at 1.395; gap 0.506. Wattleview 244.9 systems (209 first applications at 1.172) at 6.97 kW, 1.707 MW;
  Bindarra Waters 60.9 (52) at 6.50 kW, 0.396 MW. Graded as 1.9, 1.4, 0.5, 1.7 and 0.4; every one at least 0.043 MW
  inside its bin, and every reading of the uplift at least 0.02 MW inside (the corridor, asserted).
- **Default path.** YRB24 at 1.784 MW, runner-up YRB22 at 1.209, gap 0.575; Bindarra Waters 0.785 MW and Wattleview
  0.707 MW; YRB27 5th at 0.902. The reflex: YRB24 at 3.037, runner-up YRB27 at 1.333, Bindarra Waters 2.038 MW.
- **Clean truth (R3).** On the world's records before any file is written: per letterbox YRB24 1.8 (runner-up YRB22
  1.2, gap 0.6), the reflex YRB24 3.0, the uplift YRB27 1.9 with every golden figure; the pack read by its filed rules
  reproduces the world's connected capacity, trend, averages, campaign counts and pools exactly (R2).
- **Gates.** `checks.py` 429 assertions; `verify.py` 88 checks from the bundle alone; two builds byte-identical
  (`target.zip` sha256 ac3475bd...); `figures_check.py` 72 figures, none absent; `precut.py` 49 checks, 0 FAIL;
  `voice-check.py` PASS; container audit clean on the pack and the goldens; the archive's 15 members equal the pack.
  `guard.py validate` clean; `heart` WARN (`overuse.gate_g`, answered under Guard), no BLOCK; `surface` exit 0, the
  cut pack's personas clear, four pairs promoted on card axes (task138, G16 two back; task185 and task80 v2, the
  same-driver signature; task450, surface proximity, retired), each differentiated on the card.
- **Leak sweep** (`leak.py --asof 2026-10-12`, REVIEW, no LEAK, sweep 11 clean). Each REVIEW line, harmless:
  the assessment's "a 0.5 MW lower minimum" is its own sensitivity sentence, equal to the gap by chance; NPP-114
  carries the call's words because it is the procedure that assigns a hosting-capacity augmentation from the capital
  works program, and it names no feeder; the procedure, the letter and the assessment share the stump paragraph's
  ordinary nouns (connected, systems, forecast, campaign, suburb, application, window, months, method, extract) and
  none names a first application, an uptake or a basis; `device_type` is the DER Register's own device field. The
  write-up no longer quotes YRB27's 2029 hosting capacity (23.30 MW, an assessment input that swept as LEAK).

## Tried and rejected

- The seed's architecture (a filed 2024 forecast vintage a method must reproduce cell by cell): not used; it is a
  published control set recovering a withheld method, and the guard blocks a validated decoy and a filed back-test in
  consecutive builds.
- A US electric cooperative in Texas or Arizona: rejected at the draw, because the conjunction needs past suburbs where
  a third to two thirds of owner-occupied houses already have PV, which only Australian suburbs show at realistic
  rates, and because `cooperative_or_member_body` with a board, a budget and a capacity report would have read as
  task124's furniture.
- Pattern C (serviceable share behind a join): blocked by `ban.pattern` against task127; pattern E with gap population
  blocked by `test.same_driver` against task124's lineage and task500 v2. The decisive mechanism is the G-code G8.
- A pull-forward (harvesting) campaign effect as the decisive step: rejected, the lazy solver who ignores the campaigns
  then lands on the golden pick, and an event-study solver sees the post-campaign dip by reflex.
- The pool's depletion under the base trend (a hazard on the untapped pool instead of NPP-114's trend): rejected as the
  decisive step, because every defensible baseline model then gives a different MW figure; the base trend is filed in
  NPP-114 and the decisive step lives only in the programme component.
- An SF1 claim that business micro EG was under 2 per cent of any feeder: false at the build (4 to 10 per cent); the
  row now rests on NPP-114 2.1, which names business NMIs, and the residential-only reading is priced (YRB24 at 1.6).
- Alterations taking a 30 kW business system to 31 kW: a micro EG limit a literal reader could apply; alterations are
  capped at 30 kW and every register system is asserted at 30 kW or less.
- Ask B's YRB26 total at 1,584.4 kWh, 0.6 kWh from a rounding edge: the battery products' market shares were moved
  (one draw per battery either way, so nothing else re-rolled) until every total sat at least 2.2 kWh inside its ten.
- A locality named Bindarra Road beside Bindarra Waters: a substring filter on the 2027 suburb would have caught it and
  moved the Bindarra Waters figure; renamed Myrtle Vale, its random streams kept.
- A locality named Mount Cotter: two letters from Mount Cotton, a real Redland City suburb (H21); renamed Bloodwood.
- Connected systems lodged with the DER Register between 1 and 4 September 2026: they split Ask A between the extract
  and an as-at-31-August reading; lodgements for systems connected by the base date are dated no later than it, and
  both readings are asserted equal.
- Withdrawals dated after the 1 September extract (two applications): a record the extract could not hold; withdrawals
  are dated no later than the base date.
- A 2023 load transfer the generator never made (Yarrabin North kept on YRB23 in the network model): the Layer 1 claim
  was untrue; Yarrabin North now sits on YRB21 with the applications before 15 May 2023 recording YRB23 (SF5 asserts
  exactly YRB21 and YRB23 move). The first target, YRB28, put three feeders on 14 for Ask A's first figure.
- Legacy application numbers drawn with replacement (stage 3): 40 numbers were issued twice, each pairing two
  applications with two equipment rows and no key between them; the lookup gave both applications the later row (YRB22
  13,683 kW), a file-order or panel pairing gave 13,690 and a summed join 13,766, which files YRB22 at 1.6 MW and the
  gap at 0.3 (the judge's FIX_NOW). A legacy system never reissues an application number: each is now issued once and
  every join selects the same inverter (SF23). Moved with it, all step intermediates and none graded, allowed in
  `freeze.py`: `steps.connected_kw` for YRB21, YRB22, YRB23, YRB26 and YRB27, `steps.trend_kw.YRB23` (575 to 576 kW),
  `steps.forecast_kw` for the same five feeders, and `steps.excess_mw.YRB26` (-0.6 to -0.7, from -0.657 unrounded).
- Keeping the reissued numbers with a pairing key on both sides (an install date or the legacy row's sequence):
  rejected; a solver joining on the number alone still fans out and files YRB22 at 1.6 MW, and the reissue was a
  generator artifact, not something the legacy system produced.
- Recomputing the 2029 hosting capacities from the stage 3 targets after the fix: rejected, five published inputs
  would have moved 0.01 to 0.04 MW; the targets were reset (YRB21 1.110, YRB22 1.508, YRB23 0.438, YRB26 -0.657,
  YRB27 0.813) so the assessment's 2029 case stands, asserted against `HC29_PUBLISHED`.
- The assessment's 2026 case drawn independently of its minimum demand (stage 3): every feeder stepped 0.27 to 0.53 MW
  lower in 2029, five of them below the report's own stated sensitivity (the reader's realism tell). The 2026 case now
  follows each feeder's minimum-demand change at a sensitivity of 0.6 to 1.2: hosting capacity falls by 2029 on six
  feeders by 0.04 to 0.70 MW and rises on YRB23 and on YRB24, whose minimum demand grows as Bindarra Waters fills; the
  2029 columns, route lengths and customers are unchanged, and the 2026 case still files YRB24 (SF21).
- The register's status values listed without definitions (stage 3): the judge's over-inclusive reading, a withdrawn
  application counted as PV, fits the seven campaigns about as well (4.66 per cent) and rounds Bindarra Waters to 250
  with the pool at the base date; the dictionary now defines each status, Withdrawn as nothing connected under the
  application (SF24). No NPP-114 or prompt change.
- Forum `executive_team` on the card (stage 3): task128's architecture 3, drawn the same day and so before this build by
  draw key, took the same forum and heart blocked on `ban.forum`; no shipped file or prompt sentence named a forum, so
  the card carries `line_manager_or_team`.
- The data dictionary dated 2 September 2026 (stage 3), three days before the 5 September DER Register extract it lists
  with its row count: a register cannot describe an extract not yet run (the re-judge's temporal note). It is dated
  Monday 7 September 2026 in its properties and in the manifest, nothing else in it changed, and `checks.py` asserts it
  on or after every extract it lists.
- A dictionary line saying the battery storage capacity repeats on each module row (the re-judge's optional input
  fix): declined, because it would announce Ask B's device, and the data already admits one reading (Ask sheet, Ask B,
  asserted).
- The reader's realism notes on the hosting capacity assessment after the FIX_NOW pass: not acted on, because each would
  change the document beyond a date after the judge and the reader had read it, for no graded figure or call input. The
  demand and capacity moves agree in sign on every feeder (each feeder's hosting capacity moves with its own minimum
  demand, inside the report's stated sensitivity once its two decimals are allowed for, asserted); they differ in sign
  across feeders by design (minimum demand rises on YRB24 as Bindarra Waters fills, and a little on YRB23). The round
  route lengths (YRB21 30.0, YRB22 15.0 and YRB25 21.0 km of eight) and the single page carry nothing a solver computes.
- Round 1 shipped design: weak per the 10/10 audit (COMPLIANT_WEAK), because the decisive step, a bulk-buy's yield
  per owner-occupied house still without PV, is the textbook addressable-pool reflex for adoption forecasts and the
  program terms name the eligible class; any rough pool estimate landed YRB24 (it held down to a 3.6 per cent rate);
  the seven campaigns agreed within 0.6 per cent, a generator constant a denominator search recovers; Ask A's
  temporary NMIs resolved through the re-allocation log and Ask B's repeated capacity fell to grouping by connection.
  Round 2 keeps the world and the decision and makes that basis rung 1.
- The round-1 basis kept with realistic scatter: rejected, it is still the reflex (the audit's first finding).
- Round-2 prototype 1 (each suburb's PV propensity constant from 2009): a regression of the per-pool rate on PV
  penetration landed YRB27 at 1.61, because penetration then tracked current uptake; each past suburb now carries its
  own Solar Bonus Scheme propensity (2009 to 2012), so penetration no longer predicts uptake.
- OLS with an intercept on first applications extrapolated Wattleview (158 against the past 31 to 72) to 1.79 to 1.83
  MW: Kurrajong Park was made the largest past campaign (162 first applications), so the transfer interpolates.
- Window variants wandering on Poisson noise in each suburb's yearly counts: latent adoption times and lags are laid
  along a low-discrepancy sequence in handover order, so each window's count tracks its expectation.
- An all-residential reading 3 per cent off the owner-occupied one: rented houses and townhouses take PV at a twentieth
  and a fiftieth of the owner-occupiers' propensity, so the population reading converges (SF12).
- Every estimator (mean, median, through the origin, OLS) converging on the bins: impossible at realistic scatter (a
  0.11 MW spread on Wattleview even with no campaign scatter, from the past suburbs' different depletion); NPP-114 4.2
  now files the pooled rate (total over total, a general method naming no quantity); the other estimators keep the call
  at 1.81 to 1.92 MW (SF15).
- Wattleview at 3,810 owner-occupied houses with a 9 per cent hazard: its window and hazard readings sat 2 to 4 per
  cent off the past campaigns' pooled ratios; enlarged to 4,790 houses at the past campaigns' pooled hazard, its seven
  readings agree within 0.05 MW.
- Bindarra Waters' bulk-buy at 0.56 MW: its readings (0.51 to 0.61) straddled 0.55; its propensity was lowered until
  the readings sat at 0.37 to 0.42.
- YRB22, a feeder with no campaign, as the golden runner-up at 1.5 MW: the reflex's runner-up was YRB22 at 1.5 too, so a
  response stopped at the reflex banked the runner-up criterion; the base excesses were moved so the runner-up is
  YRB24 at 1.4, which no wrong route files as its runner-up (asserted).
- Round 1's second Ask A count (active DER sites with no connected system): the drop-unknown route landed 8 of 8 and
  the feeder-stamp route 6 of 8; replaced by the sites first lodged in FY2025-26, an anchor on the first record.
- Round 1's Ask B (one capacity repeated on every module row): grouping by connection cracked it; the storage now
  follows each product's lodgement (Sungrow SBR stacks repeat the stack's total, the others lodge module by module),
  so the dedupe and the sum both miss every feeder.
- Three asks of eight figures: the most obvious device cracked lifted the pair to 42.6; a fourth per-feeder figure
  (active sites, on the feeder stamped at lodgement) holds it at 39.7.
- 2024 load transfers moving Hollow Creek streets off YRB22 and Ferndale Rise streets onto YRB27: the feeder recorded on
  the application (SF5) then filed YRB22; the 2024 transfers now move Coachwood Park streets onto YRB22 and Jacaranda
  Gardens streets off YRB27, so SF5 keeps the call while every feeder still gains or loses stamped sites.
- Enphase microinverter systems lodged as two inverter rows on the older portal (17 active): the nameplate rule could
  not see a total in "IQ8 system"; a microinverter system is lodged as one device.
- Ask totals within a kilowatt of a rounding edge (YRB22 storage 2,404.4 kWh): the generator records one left-active old
  connection on that feeder as decommissioned, or gives one modular battery a module more or fewer, touching nothing
  the call reads.
- R2 asserted as mishandling-neutral per item (the strict form): summing alterations (YRB22), dropping migrated rows
  (YRB24) and the 2026 hosting case (YRB24 by 0.1) each move capacity by megawatts against a 0.5 MW gap, as any
  capacity mishandling must; R2 is asserted as task137's is, the pack read by its filed rules and dictionary giving back
  the world's own figures, and each mishandling is an SF row ruled out by a quoted sentence (NPP-114 2.2, 5.1, the
  dictionary).
- Christopher Sheppard as the Manager Network Planning: `guard.py surface` blocked `people.first` on the round-2 pack
  (task450, among the twelve most recent builds, took the first name after round 1); renamed Ian Fletcher, drawn by
  `guard.py names`, and the pack rebuilt with every figure unchanged.
