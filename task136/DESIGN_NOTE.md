# task136: Mirrabee Energy, the Yarrabin feeder that gets the FY2027-28 hosting-capacity augmentation (architecture 1, round 3)

Private, never ships. A wave 2 build numbered from seed FC07 (the seed's world, decision and quantity kept: one
accelerated feeder upgrade for rooftop solar above hosting capacity, eight feeders, the 2029 design year, two council
bulk-buys; its published-control architecture never used). Round 1 shipped on 2026-10-12 with the bulk-buys' yield
carried per owner-occupied house still without PV; round 2 (2026-10-14, the 10/10 audit's redesign) carried it per
first application in the year before sign-ups; round 3 (2026-10-15) is the rule 3 audit's rework. Nothing is filed
that recovers a rule, and no record blesses the wrong method.

## Round 3

- **Trigger.** The rule 3 audit (AT_RISK, `scratchpad/rule3/task136.md`): the prompt bound the call to NPP-114
  ("forecasting rooftop PV as NPP-114 sets out"); NPP-114 4.2 stated every step of the program component but the
  pooled rate's denominator; the winning basis was found only by a denominator search over seven campaigns; and the
  round-2 note called per eligible house the textbook method. It read as a hidden rule and as rule application.
- **What moved.** The pooling clause and the prompt's binding are gone. NPP-114 4.1 files only the estimand (the
  forecast is the base forecast plus "the impact on the feeder's connected capacity at the design point of each
  program"), and the prompt asks "how much each bulk-buy will raise its feeder's PV by that date". No sentence names a
  method, a comparison, a basis or a share. The decisive step is now the bulk-buys' net addition: a campaign signs up
  mostly households already on their way to PV, so its installed systems overstate what it adds by 2029, and uptake
  rose across the zone over the same years, so a suburb's own before and after overstates it too; each past campaign
  suburb read against the suburbs whose campaign had not yet run, over the same months (the staggered-adoption
  comparison), gives what it added. The world was regenerated for it: each campaign takes most of its suburb's
  near-term pipeline and brings in a few households from outside the market; uptake steps up across the zone from
  2022; the 2026 suburbs are established estates; houses whose owners never applied sit in every suburb.
- **What stayed.** The decision (one augmentation, eight feeders, the 31 August 2029 design point, the two spring 2026
  bulk-buys), NPP-114's definitions, base forecast, sizing, hosting basis and assignment, the people, the files and
  their layouts, the forum, the forcing event and the four DER Register asks with their devices.
- **Where it stands.** Stage 3 green (Build record); stage 4, the leak reader and the determinism judge, is run by the
  main session.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task136.json`, architecture v1 at round 3 (rounds 1 and 2 in `lineage`); `guard.py` results under Guard and Build record |
| Domain / task type | energy-systems-utilities / load-forecasting (a client domain): a distributor's forecast of rooftop PV on each feeder at the design point of an augmentation is the DER half of its demand forecast |
| Objective | Forecasting & Predictive Modeling: the rooftop PV connected on each feeder at 31 August 2029, a window not yet open, against the spring 2029 minimum-demand hosting capacity |
| Shape | other: the call and its six components (the feeder, its PV over hosting capacity, the runner-up, its excess, the gap, how much each 2026 bulk-buy raises its feeder's PV by the design point), the chart's named parts, and four per-feeder DER Register figures on rows the call never reads (32 figures); about 40 criteria, arithmetic in `## Ask sheet` |
| Decision | `pick_one_of_n`, answer unit `named_option` (with its MW figure): which feeder gets the one augmentation |
| Mechanism | gap time then population; pattern none; generators G9 (what a campaign leaves on the feeder at the design point against what it installed), G16 (the comparison the records support), G13 (the impact at the design point, after the pulled-forward installs would have come anyway); Gate G `method_or_model_selection`; strategy `population_selection` (which installed systems are the campaign's own: its participants are selected on imminent adoption) |
| Layer 2 family / pattern | `estimand_identification`; `own:bulk-buy-net-uplift-against-not-yet-treated-suburbs` (a program's addition at a horizon read against the areas whose program had not yet run, over the same calendar months) |
| Furniture | forum `line_manager_or_team` (NPP-114 section 6 assigns the one augmentation when the capital works program is compiled; no forum named anywhere), forcing event `budget_or_appropriation`, organisation family `utility_or_infrastructure`, role family `research_desk`, context artifact `capacity_report` (the 2026 hosting capacity assessment), calibration `none`, opening `question-first`, question form `which` |
| Spine | `eg_connection_applications_20260901.csv`, the embedded generation connection register: one row per micro EG connection application at an NMI, new systems and alterations, 2009 to 31 August 2026 (27,854 rows); constructed |
| Deliverables | `feeder_upgrade_2029.xlsx` (the call, the forecast by feeder, the Solar Streets estimate, the DER Register figures), `yarrabin_pv_vs_hosting_2029.png` (one bar per feeder for its PV at 31 August 2029, its hosting capacity marked) |
| People | drawn with `guard.py names --geo Australia --seed 136`: Wanda Thornton (DER forecasting analyst, the requester), Ian Fletcher (Manager Network Planning, owner of NPP-114; replaced Christopher Sheppard at round 2), Julie Cochran (council sustainability programs officer), Bryan Nichols (connections lead), Linda Ruiz (GIS analyst), Nicole Rocha (customer team leader), Tammy Buchanan (consulting engineer); none in the prompt |

**Guard.** `guard.py check` on the round-3 card: WARN, no BLOCK. `people.first`: Julie (Julie Cochran, drawn for this
build at round 1) appears in task139; one other build is a WARN, and renaming the council's officer would rewrite the
letter and the log for no gain. `driver.near` 0.16 against this slot's round 2, differentiated on the card. The honest
strategy key has two candidates: `causal_design` names the estimator (a comparison choice), `population_selection`
what the decisive step decides (which of a campaign's installed systems are its own). `causal_design` blocks on
`ban.strategy` against task128 v3 (task139 v1 holds it too), `decomposition_attribution` (the installed count split
into pulled-forward and added) against task127 v2, and G13 first on `test.same_driver` against task130 v4; the card
keys `population_selection` with G9 first and says so in its notes, so the author can force `causal_design` instead.

**Abstraction test.** Stripped of nouns: a scheduled intervention mostly enrols units already about to take up the
outcome on their own, so its enrolments overstate what it adds by a later horizon, and a common rise in the
outcome's pace inflates each site's own before and after; only past sites read against sites whose run had not yet
come, over the same months, give the addition, which carried per eligible unit shrinks the largest site's increment
most. The nearest drivers on file are this slot's rounds 1 and 2 (a transfer basis chosen among pools and uptake),
task139 (an assigned intervention read per assigned unit) and task128 v3 (a capacity-overflow natural experiment);
none reads a program's addition at a horizon against not-yet-treated sites.

**Data-native sentence.** Merindah's bulk-buys sign up the households already on their way to rooftop PV: for two
years after each opening a campaign suburb's other first applications run at a quarter of what its own year before
and the not-yet-treated suburbs' pace imply, then recover; and uptake rose across the zone between campaigns (over
each campaign's window the not-yet-treated suburbs lodged first applications at a yearly rate 4 to 28 per cent above
the year before it), so the installed count (9.32 systems per 100 owner-occupied houses without PV) and each suburb's own
before and after (5.68) both overstate what a campaign adds by the design point (4.09), and Bindarra Waters' large
pool turns the overstatement into megawatts on YRB24.

**Sources read, one line each.** The rule 3 audit and `stumping/references/client/two-layer-task-design.md`: the
decisive step must be analysis a strong analyst who read every rule still gets wrong; here a reader of 4.1's "impact"
still takes the installed count as the impact. Evaluations of community solar bulk-buys read a campaign against towns
whose campaign came later; that is the field's method here, and the forecaster's generic moves (the installed count,
the area's own before and after) are the trap. `guard.py mechanisms --objective forecasting`: hazards by time since
entry (134), selection on the outcome (124), claims maturity (130), recycling terms (501), conversion rates
recovered from a corpus (27, 29, 30, 78), censored delays (31, 99), an assigned intervention per assigned unit
(139), a class of money (137), a transfer basis (136 rounds 1 and 2); none reads an intervention's addition at a
horizon against not-yet-treated sites. `stumping/references/client/measured-drivers.md`: the held tasks put the
decisive rung upstream of every graded figure; the counterfactual here sits upstream of the call, the runner-up, the
gap and both bulk-buys. The seed's header (FC07) for the world only.

**World.** Mirrabee Energy is a regional electricity distributor in south-east Queensland. Its Yarrabin zone
substation supplies eight 22 kV feeders, YRB21 to YRB28, in Merindah's western growth corridor (62,990 NMIs).
Merindah City Council's Solar Streets program has run a bulk-buy in one suburb a year since 2018 (two in 2022, none
in 2020): a letterbox drop to every address, information sessions, one appointed installer, a twelve-week sign-up
window and installations over the following months. The council's 2026-27 budget runs two campaigns this spring
(sign-ups 1 September to 27 November 2026): Bindarra Waters on YRB24 (built 2005 to 2014, 4,537 owner-occupied
houses without PV) and Wattleview on YRB27 (built 2007 to 2014, 1,857). NPP-114 (revision 3, March 2026) defines the
forecast for an augmentation; the 2026 hosting capacity assessment gives each feeder's hosting capacity for the
spring 2029 minimum-demand case; the FY2027-28 capital works program funds one accelerated hosting-capacity
augmentation, assigned by NPP-114 section 6. As-of dates: the connection register, the network model and the DER
Register extract at 31 August 2026 (run 1 September 2026); the council's letter of 14 August 2026; the hand-off 12
October 2026.

## Default path

1. Read NPP-114. From the connection register take each NMI's latest connected configuration (an alteration carries
   the NMI's whole system), inverters of migrated rows from the legacy table, each NMI on its feeder in the network
   model at 31 August 2026: connected capacity at the base date.
2. Build NPP-114's trend (the FY2023-24 to FY2025-26 average yearly increase in connected capacity less the program
   systems first connected that year) and carry it three years to 31 August 2029.
3. Take 4.1's impact of each 2026 bulk-buy as the systems it will install, at the council's participation rate: the
   seven past campaigns' systems installed over their homes letterboxed (1,431 over 32,930), onto the letter's drops
   (10,477 in Bindarra Waters, 3,117 in Wattleview), each system at the feeder's FY2025-26 average new inverter (4.3).
4. Subtract each feeder's spring 2029 hosting capacity (5.1) and pick the largest excess (6.1).

Ends on: YRB24, about 4.2 MW over its hosting capacity at 31 August 2029 (Bindarra Waters adds 4.2 MW, Wattleview 1.3 MW; runner-up YRB27 at 2.5).
Golden: YRB27, about 1.9 MW over its hosting capacity (Bindarra Waters adds 1.7 MW, Wattleview 0.7 MW; runner-up YRB24 at 1.7, gap 0.2).

## Stump sentence

A competent solver builds NPP-114's base forecast, takes each 2026 bulk-buy's impact as the systems it will install
at the council's participation rate per home letterboxed and files YRB24 at about 4.2 MW over hosting capacity (Ends
on); per owner-occupied house still without PV it files YRB24 at 3.9, and each suburb's own before and after files
YRB24 at 2.4; the step that lands all three there is counting a campaign's installed systems, or its suburb's rise
over its own past, as what it adds, when more than half of the households the past campaigns signed up would have
gone solar within three years anyway and uptake rose across the zone over the same years: read against the suburbs
whose campaign had not yet run, the seven added 4.09 systems per 100 owner-occupied houses without PV, Bindarra
Waters adds 1.7 MW, and the golden is YRB27 at about 1.9 MW.

## Three rules

- **Task type:** energy-systems-utilities / load-forecasting, the DER component of a distributor's design-point
  feeder forecast for a hosting-capacity augmentation; load-forecasting serves Forecasting & Predictive Modeling.
- **Domain test:** the deciding quantity is each feeder's rooftop PV (micro EG inverter capacity) connected at 31
  August 2029 against its spring 2029 minimum-demand hosting capacity, with each council bulk-buy's contribution
  estimated as program evaluators estimate a solar bulk-buy's net effect: each past campaign suburb's first
  applications read against suburbs whose campaign had not yet run over the same months, so installs the campaign
  only pulled forward are not added on top of a trend that already carries them.
- **Swap:** "which of eight school catchments gets the extra classroom block, counting two enrolment drives":
  inverter ratings, connected capacity with alterations replacing configurations, hosting capacity at spring minimum
  demand and a purchase pulled forward from a later year have nothing to attach to; a child's enrolment is fixed by
  age, so a drive cannot harvest next year's enrolments the way a bulk-buy harvests next year's PV buyers.
- **Layer 1:** the connection register at application grain (alterations carrying the NMI's whole system;
  withdrawn, under-assessment and approved-not-connected applications; removals), 2019 migrated rows whose inverters
  sit in a legacy equipment table, the feeder recorded at application after five load transfers (2023 to 2025), the
  rates roll keyed by property number and joined to NMIs only through the GIS cross-reference (dual-occupancy NMIs,
  abolished NMIs of rebuilt houses), the council's workbook in its own layout; on the ask paths a device-grain DER
  Register extract (checksum NMIs from the newer portal, builders' temporary NMIs and the re-allocation log,
  decommissioned connections, the feeder stamped at lodgement, per-product battery lodgement, the older portal's
  per-inverter field). Each is what these systems produce; read by the filed rules and the dictionary each gives back
  the world's own figures (R2, asserted), and none decides the call.
- **Layer 2:** `estimand_identification`, staggered adoption: the counterfactual for a past campaign suburb is what
  its houses would have lodged over the same months without the campaign, read from the suburbs whose campaign had
  not yet run; the shortcut takes the installed systems as the addition, and the event-study reflex takes the
  suburb's own year before at its own pace, which counts the zone's rise as the campaign's.
- **Decisive step:** estimating what each past bulk-buy added by the end of its window as its suburb's first
  applications over the window less its year before scaled by the not-yet-treated suburbs' change over the same
  months (4.09 per 100 owner-occupied houses without PV, against 9.32 installed and 5.68 on the suburb's own before
  and after), and carrying that, not the installed systems, onto the 2026 suburbs.
- **Not semantics:** every field, code and definition (status, land use 02, rating R1, inverter_kw_ac, program_ref,
  received_date, systems installed, homes letterboxed) is read the same on every path, and so is the estimand: the
  default path reads 4.1's "impact" and the prompt's "raise its feeder's PV" correctly and still takes every installed
  system as additional, an analytical assumption the records refute, not a reading.
- **Not rule application:** NPP-114 4.1 files only the estimand and 4.3 the size of a system; no sentence names a
  comparison, a counterfactual, a pulled-forward install or an estimator, and no document states a campaign's
  addition, so executing every clause leaves the impact to be estimated, and the installed count executes them all
  and files YRB24.
- **Analyst test:** a strong analyst who collapses alterations, joins legacy inverters, places NMIs on the network
  model, builds NPP-114's trend and takes the bulk-buys' impact as their installed systems per home letterboxed files
  YRB24 at about 4.2 MW (Ends on); per owner-occupied house without PV YRB24 at 3.9; each suburb's own before and
  after YRB24 at 2.4 to 2.6; fitted models of installed systems on pool, letterboxes, houses and penetration YRB24 at
  3.7 to 5.0.
- **Estimand:** the prompt ("how far that feeder's PV will sit above its hosting capacity at 31 August 2029", "how
  much each bulk-buy will raise its feeder's PV by that date") and NPP-114 2.2, 2.4, 3.1, 3.2, 4.1, 4.3, 5.1 and 6.1
  fix the population (micro EG at NMIs the network model places on each Yarrabin feeder, each 2026 campaign's
  addition included though none is yet lodged), the outcome (connected capacity at 31 August 2029 with each
  campaign's impact, against the spring 2029 hosting capacity), the unit (MW to one decimal) and the comparison (the
  largest excess; a campaign's impact is with it against without it, 4.1).
- **No decoy:** no file states a 2029 forecast, an excess, a participation rate, a campaign's addition or a share of
  it; the council's summary reports its campaigns' history (letterboxed, registrations, assessments, contracts,
  systems installed), equal to the register's program-coded connections; no memo, draft, briefing or stakeholder
  figure argues for a feeder or a method.
- **No certified replay:** no certified or published figure pins the method; the installed counts are true history,
  what each campaign added is estimated from the register itself against suburbs whose campaign had not yet run, and
  nothing in the pack reproduces only under the golden.
- **Lesson:** a program's installed count is not what it adds: when its participants were about to adopt anyway, its
  addition by a later date is read against comparable areas not yet treated, over the same months, and an area's own
  before and after counts the market's rise as the program's; no build on file teaches the staggered-adoption
  counterfactual for a forecast (task139 reads a randomised intervention per assigned unit, this slot's earlier
  rounds a transfer basis).

## Gate G

- **Litmus.** No. Every file is correct; the council's installed counts are true and reconcile with the register;
  no file states a forecast, an addition, a share or an excess, and no stakeholder states a number the task overturns.
- **Primary mechanism:** `method_or_model_selection` (the counterfactual for a past campaign: the installed count,
  the suburb's own before and after, or the not-yet-treated suburbs over the same months; the records select the last
  through the post-opening dip and the comparison suburbs' pace).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test (asserted, R3a).** On the world's own records, before any file is written, installed systems per
  letterbox file YRB24 at 4.2 MW and per house without PV YRB24 at 3.9; the campaigns' true additions per house
  without PV file YRB27 at 1.9 with every golden figure (R3b).
- **Deletion test.** Delete the distractors, the DER Register extract and the re-allocation log: the call recomputes
  unchanged (asserted) and the default path is still wrong.
- **Lens swap.** The default and the golden are two estimates of one quantity (what a campaign adds by the design
  point) on the same rows, not one population at one moment under two lenses.
- **No artifact ranks or prices the decision.** The council's log reports what each campaign did; the assessment
  gives hosting capacity and minimum demand.

## Readability screen

Six tests per rung: 1 filed sentence; 2 schema; 3 reflex; 4 control or corpus; 5 hygiene battery; 6 linear. Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 installed systems per home letterboxed (the council's participation rate on the letter's drops) | the log and the letter carry both counts | the log's `Systems installed` and `Homes letterboxed` | yes | no | no | yes (a ratio of two reported figures) | readable |
| R1 installed systems per owner-occupied house without PV (the textbook transfer) | the program terms name owner-occupiers of houses | the rates roll's land use and rating | yes (eligible and not yet adopted) | no | no | no | readable |
| R2 each suburb's own before and after (first applications over the window less the year before at its own pace) | no | the register's received dates | yes (an event study's first move) | no | no | partly | readable |
| R2a fitted models of the installed systems on the obvious covariates (pool, letterboxes, houses, penetration) | no | the same columns | yes | no | no | no | readable |
| R3 (decisive) each past campaign suburb against the suburbs whose campaign had not yet run, over the same months, per house without PV | no sentence names a comparison, a counterfactual or a pulled-forward install; NPP-114 4.1 files only the impact at the design point | no column holds a campaign's addition; it is built per campaign and per window from received dates by suburb through the rates roll and the cross-reference | no: the reflexes are R0, R1 and R2 | nothing scores it; the council's installed counts tie under every estimate | no | no (a counterfactual from other suburbs over matching calendar months) | silent |

The decisive rung is silent because the installed count is true and reconciles: nothing in the pack is wrong, and
the pulled-forward installs show only as a dip in the campaign suburbs' other first applications for two years after
each opening, measured against suburbs a solver has to choose as the comparison.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. `checks.py` asserts each row (the
alternative computed and shown to move a figure or to converge, and the ruling sentence found in the pack).

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "rooftop PV" on a feeder | all micro EG (30 kVA or less) at NMIs the network model places on the feeder, residential and business | residential NMIs only | YRB27 at 1.2, runner-up YRB24 at 1.1 | NPP-114 2.1 ("at a residential or business NMI") and 2.2, asserted; every register system is 30 kW or less |
| SF2 | a system's capacity | the inverter capacity (kW AC) of the NMI's latest connected configuration | every connected application summed; panel capacity | summed: YRB22 at 4.3; panel: YRB24 at 6.1 | NPP-114 2.2 ("An alteration replaces the configuration it alters"; "inverter capacity (kW, AC rating)") and the dictionary's `inverter_kw_ac` |
| SF3 | migrated rows (blank `inverter_kw_ac`) | the inverter from the legacy equipment table on the legacy application number | the rows dropped; their panel capacity | dropped: YRB27 at -1.7; panel: YRB24 at 2.6 | NPP-114 2.2 and the dictionary ("Blank on applications migrated from the legacy system"), asserted |
| SF4 | "connected" at a date | status Connected, connection date on or before the date, not removed by it | approved but not connected counted | same call (YRB27 at 2.0); every base moves under 2 per cent | NPP-114 2.2 |
| SF5 | the feeder of an NMI | the network model at 31 August 2026 | the feeder recorded on the application | same call (YRB27 at 2.5, runner-up YRB23) | NPP-114 3.1 |
| SF6 | the base date | 31 August 2026, the extracts' as-at date | 30 June 2026 | same call (YRB27 at 1.7, gap 0.4); no record exists after 31 August | NPP-114 3.1 and the extracts' dates (the manifest) |
| SF7 | the trend | the average yearly increase in connected capacity over FY2023-24 to FY2025-26 less program systems first connected that year | new connections only; program systems left in | same call under both (1.8; 1.9 with runner-up YRB21) | NPP-114 3.2 |
| SF8 | the years carried | three | 3.25 or 2.92 | same call, figures move | NPP-114 2.4 and 3.2 |
| SF9 | a campaign's installed systems | the applications carrying its Solar Streets reference, equal to the council's systems installed for every campaign | contracts signed | YRB24 at 4.0 (an installed-count route) | NPP-114 2.3 and the log's footnote 3 (contracts include cancellations); the golden reads every first application, program or not, so no installed count enters it |
| SF10 | each added system's size | the feeder's FY2025-26 average new inverter | the past program systems' own average (6.74 kW) | same call (YRB27 at 1.7, runner-up YRB22) | NPP-114 4.3 |
| SF11 | a first application's date | the received date of the house's earliest application other than a withdrawn one | the first connection date | converges: every graded figure (asserted, four dated-by-connection constructions) | the records converge |
| SF12 | whose first applications | the suburb's owner-occupied houses (rates roll land use 02, rating R1, through the cross-reference) | every house, rented ones included; every residential address | YRB24 at 2.1 | the program terms ("owner-occupiers of houses"; tenants are not eligible), asserted: the population the campaign can reach |
| SF13 | a past campaign's window | 36 months from sign-ups opening, cut at 31 August 2026 for BNR23 and PBG24 | 24 months | converges (asserted) | the records converge |
| SF14 | a suburb | the rates roll's locality | the network model's locality | same rows | the records converge |
| SF15 | the estimator on the seven campaigns | pooled, total added over total houses without PV at the openings | the mean or median of the seven rates; through the origin; OLS; added regressed on pool, or on pool and penetration | converges (asserted) | the records converge |
| SF16 | the comparison suburbs | those whose campaign opens after the window closes (not yet treated, the 2026 suburbs included) | the suburbs that never had a campaign; both together | converges (asserted) | the records converge; every other suburb, treated ones included, is refused by the records (each treated suburb's other first applications run at a quarter of the expected level for two years after its opening, asserted): YRB27 at 2.0 with every figure off |
| SF17 | the year before | the 12 months before sign-ups opened | 24 or 36 months at a yearly rate | converges (asserted) | the records converge |
| SF18 | the counterfactual's form | counts: the year before times the comparison's change | hazards on the houses without PV; month by month with each suburb leaving the comparison when its campaign opens | converges (asserted) | the records converge |
| SF19 | how much a bulk-buy raises its feeder's PV by the design point | its feeder's PV at 31 August 2029 with the campaign against without it | the PV the campaign's installer connects | YRB24 (an installed-count route) | the prompt's "raise its feeder's PV by that date" and NPP-114 4.1's "impact on the feeder's connected capacity at the design point"; a reader who takes the golden reading still files YRB24 when it estimates the impact as the installed count, so the stump is the estimate, not this row |
| SF20 | the transfer basis | per owner-occupied house without PV at the opening | per home letterboxed; per owner-occupied house; per first application in the year before; per campaign | YRB24 at 1.8; YRB27 at 1.8 with every figure off; YRB24 at 2.8; YRB27 at 2.0 with runner-up YRB22 | the records: the seven additions spread 0.046 per house without PV and 0.146 to 0.244 on every other basis (asserted at 1.5 times or more) |
| SF21 | hosting capacity | the assessment's spring 2029 minimum-demand case | the 2026 case beside it | YRB24 by 0.1 MW | NPP-114 5.1 ("for the design year's spring minimum-demand case") and 2.4, asserted; the prompt's "at 31 August 2029" |
| SF22 | the excess, the runner-up and the gap | unrounded, ranked, rounded once to 0.1 MW | rounded figures subtracted | converges (asserted) | NPP-114 6.1 and 7.1 |
| SF23 | a migrated row's inverter | the equipment row with the register's legacy application number | file order, panel size, summed, first or last row | converges: every number issued once on each side | the records converge |
| SF24 | a withdrawn application | not a first application: nothing was connected under it | any status counted | same call (YRB27 at 1.8), figures move | the dictionary's status definition, asserted |
| SF25 | the two campaigns whose window the base date cuts (BNR23, PBG24) | kept, at their shorter windows | dropped | converges (asserted) | the records converge |
| SF26 | "how much each bulk-buy will raise its feeder's PV" | its systems at the feeder's FY2025-26 average new inverter, in MW | a count of systems | the prompt gives megawatts to one decimal; NPP-114 4.3 sizes each system | the prompt and NPP-114 4.3, asserted |
| SF27 | the feeder a DER site is on (asks 1 to 4) | the network model's feeder for the site's NMI | the DER extract's `feeder` (stamped at lodgement; 491 active connections at 431 sites differ) | the call unread; Ask 1 YRB27 1,933 and YRB23 2,336 (all 8 off) | the prompt's "sites it supplies" and the dictionary: the network model's feeder is the "Feeder supplying the NMI at 31 August 2026", the extract's only "added by Mirrabee's extraction" (asserted) |
| SF28 | "first lodged" (ask 2) | the site's earliest `registered_date` over every AC connection at it, decommissioned included | the earliest of the active connections only | the call unread; YRB27 170, YRB26 108 (all 8 off) | the prompt counts sites ("how many of them"); the dictionary dates each AC connection ("Date the installer lodged the AC connection") and keeps a replaced one as Decommissioned (asserted) |
| SF29 | a house with two NMIs | the earlier first application | the later | converges: no house in a campaign suburb has two NMIs (asserted) | the records converge |

The stump is none of these rows: a careful reader reads every one the same way, and the default path reads them all
correctly. SF15 to SF18 and SF20 are the decisive estimate's constructions and bases, listed so that each is either
shown to converge or priced and refused by the records. SF27 and SF28 are the asks' own terms (each ask's primary
device, `supplemental-stumping`); the call reads neither.

## Ladder

| Rung | Estimate of a 2026 bulk-buy's impact | Winner and excess | Runner-up | YRB27 | Bindarra Waters, Wattleview | Dies to |
|---|---|---|---|---|---|---|
| R0 (default) | installed systems per home letterboxed, pooled (4.35 per 100) | YRB24 4.164 | YRB27 2.456 (by 1.71 MW) | 2nd | 4.165 MW, 1.266 MW | the dip: each campaign suburb's other first applications run at 0.24 to 0.27 of the comparison-implied level for two years after its opening, then recover (0.98 to 1.01) |
| R1 (the reflex) | installed systems per owner-occupied house without PV (9.32 per 100) | YRB24 3.868 | YRB27 2.808 (by 1.06 MW) | 2nd | 3.870 MW, 1.618 MW | the same dip |
| R2 (the event study) | each suburb's own before and after (5.68 per 100 on 12 months) | YRB24 2.355 (2.482 and 2.599 on 24 and 36 months) | YRB27 2.175 (by 0.18 MW) | 2nd | 2.357 MW, 0.986 MW | over each window the not-yet-treated suburbs lodged first applications at a yearly rate 4 to 28 per cent above the year before it |
| R3 (decisive) | against the suburbs whose campaign had not yet run, per owner-occupied house without PV (4.09 per 100) | YRB27 1.900 | YRB24 1.696 (by 0.204 MW) | 1st | 1.698 MW, 0.710 MW | (golden) |

- **Position.** YRB27 is 2nd on R0, R1 and R2 and 1st only on R3; every correction before R3 leaves YRB24 first.
  Only two feeders carry a bulk-buy, so YRB27 (1.19 MW over before any campaign, second only to YRB22's 1.40) is
  second whenever Bindarra Waters' campaign is overstated by more than about 0.2 MW; no wrong route files YRB27 first
  with YRB24 second at 1.7 MW (asserted).
- **Margins.** R0 1.71 MW, R1 1.06, R2 0.18 to 0.32; the golden's gap 0.204 MW is about thirteen times the move one
  standard error of the pooled rate makes in it (0.015).
- **Dominance.** Before any campaign YRB27 leads YRB24 by 1.19 MW; Bindarra Waters' campaign adds 0.99 MW more than
  Wattleview's on R3 (1.20 times less than the lead) and 2.25 MW more on R1.
- **Rivals (each asserted).** Installed systems per letterbox, house without PV, owner-occupied house or first
  application in the year before, each pooled, as a mean, a median or OLS (YRB24 at 3.4 to 7.0); per campaign (YRB27
  at 3.1, every figure off); contracts per house (YRB24 at 4.0); installed systems regressed on pool, letterboxes,
  houses or penetration (YRB24 at 3.7 to 5.0, or YRB27 at 3.0 with every figure off); each suburb's own before and
  after on 12, 24 or 36 months (YRB24 at 2.4 to 2.6); the right comparison on another basis (per letterbox YRB24 at
  1.8; per owner-occupied house YRB27 at 1.8 with every figure off; per first application YRB24 at 2.8; per campaign
  YRB27 at 2.0 with runner-up YRB22); additions regressed on letterboxes, houses or first applications (YRB24 at 1.8 to
  3.1); every other suburb, treated ones included, as the comparison (YRB27 at 2.0, every figure off); the hazard of
  the houses left after the participants (YRB24 at 2.1); a two-way fixed-effects regression on yearly rates (YRB27 at
  1.5, runner-up YRB22); no campaign at all (YRB22 at 1.4). Each names another feeder or misses every graded figure.
- **Guesses (recorded, asserted where they miss).** An assumed share of the installed systems as additional: 30 and
  33 per cent file YRB27 at 1.7 with runner-up YRB22; 40 per cent files YRB27 at 1.8 with every figure off; between 40
  and 42.75 per cent the figures start to land one by one, 42.75 to 45.0 per cent lands every figure (the records give
  43.9) and 45.25 to 46.5 per cent three to five of them; 50 per cent files YRB27 at 2.0 with every figure off; 60 per
  cent and more file YRB24. Only a share inside two and a quarter points of the records' lands the call whole, and no
  data-driven route reaches it. Installed systems less a year of the suburb's own uptake files YRB27 at 2.0 with the gap
  only.
- **The construction corridor (asserted, 33 constructions).** The not-yet-treated, never-treated or both as the
  comparison; 12, 24 or 36 months before; counts or hazards; month by month; a 24-month window; dated by connection;
  pooled, mean, median, through the origin or OLS; without the cut-off campaigns: excess 1.896 to 1.909, runner-up
  1.687 to 1.720, gap 0.176 to 0.209, Bindarra Waters 1.688 to 1.722, Wattleview 0.706 to 0.719, each at least 0.026
  MW inside its bin. One standard error of the pooled rate either way: 1.911, 1.722, 0.189, 1.724, 0.721 and 1.889,
  1.670, 0.219, 1.672, 0.699, every figure in its bin (asserted).
- **Worth on the graded figures.** R0 to R3 moves the call, the runner-up (YRB27 to YRB24), the gap (1.7 to 0.2) and
  both bulk-buys (4.2 to 1.7, 1.3 to 0.7); R2 to R3 moves the same five.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | micro EG at NMIs on the eight Yarrabin feeders in the network model at 31 August 2026 (NPP-114 2.2, 3.1); members not yet observed (the trend's systems to 2029 and each 2026 campaign's addition) are the estimand, projected; filed literally |
| 2 | Unit of account | a system is an NMI's connected configuration (2.2); a campaign's addition counts first applications from owner-occupied houses (SF11, SF12); its MW are those systems at the feeder's average (SF26) |
| 3 | Attribution window | the trend's financial years, program systems leaving the trend in the year first connected (3.2); a past campaign's addition over 36 months from its opening, cut at the base date for BNR23 and PBG24 (SF13, SF25); the 2026 campaigns' impact at the design point, 36 months after their opening (4.1) |
| 4 | As-of dating | the base date 31 August 2026 (3.1); the 2026 openings are the next day, so the year before each ends on the base date (asserted) |
| 5 | Version basis | one register extract; alterations replace configurations (SF2) |
| 6 | Denominator | the decisive estimate's transfer basis, houses without PV at the opening, chosen by the records (SF20); not a reading |
| 7 | Weighting | pooled, total over total; mean, median, origin and OLS converge (SF15) |
| 8 | Window length | the trend window filed (three complete financial years); the campaign window 36 months with 24 converging (SF13); the year before 12 months with 24 and 36 converging (SF17) |
| 9 | Boundary inclusivity | connection dates on or before the base date; first applications in [opening less 12 months, opening) and [opening, window end); no first application sits on a window edge (asserted), and the base date read exclusively or the financial years a day late change no graded figure (asserted) |
| 10 | Rounding path | carried unrounded, rounded once (7.1); the gap equals the difference of the rounded excesses (SF22) |
| 11 | Tie-break | none needed: YRB27 leads by 0.204 MW and YRB24 leads YRB22 by 0.30 MW |
| 12 | Maturity and censoring | every past program system connected by the base date (none pending, asserted); BNR23 and PBG24's windows end at the base date and dropping them converges (SF25); the 2026 campaigns close on 27 November 2026, inside 4.1's six months before the design point; no 2026 program reference is lodged yet (asserted) |
| 13 | Order of operations | alterations collapsed before summing; one first application per house before counting; the comparison's change taken over the same calendar months as the window |
| 14 | Row order | changes nothing (asserted) |
| 15 | Duplicate resolution | one configuration per NMI (SF2); one first application per house; no house in a campaign suburb with two NMIs (SF29) |
| 16 | Identity normalisation | NMIs are ten characters in the register, the network model and the cross-reference (asserted); legacy numbers pair one to one (SF23) |
| 17 | Netting against gross | removals leave connected capacity (2.2); no export netting; a campaign's impact is with it against without it (4.1, SF19), and how much of its installed count would have come anyway is the decisive estimate, never a filed share |
| 18 | Dimensional units | kW AC, MW for reporting; panel kWp never enters (SF2, SF3) |
| 19 | Code and status semantics | status, land use and rating codes defined in the dictionary (SF24) |
| 20 | Integerisation | the 2026 campaigns' additions are expected counts, carried unrounded into MW |
| 21 | Clause scope | NPP-114 section 4 applies to each program scheduled on the feeder whose sign-up window closes at least six months before the design point, confirmed in writing (4.2): the two 2026 campaigns (the council's letter) |
| 22 | Forward window contents | the letter gives each 2026 campaign's suburb, sign-up dates (1 September to 27 November 2026, asserted) and letterbox drop; NPP-114 3.2 carries the trend to the design point |

## Literal reader

Every shipped sentence that bears on how the main figure is computed: the prompt (the feeder, "how far that feeder's
PV will sit above its hosting capacity at 31 August 2029", "the runner-up and the gap", "how much each bulk-buy will
raise its feeder's PV by that date", megawatts to one decimal); NPP-114 2.1 (micro EG), 2.2 (connected capacity, an
alteration replacing the configuration), 2.3 (program system), 2.4 (design point), 2.5 (financial year), 3.1 (base
date, the network model), 3.2 (base forecast and trend), 4.1 (the forecast is the base forecast plus each program's
impact at the design point), 4.2 (written confirmation), 4.3 (systems not connected at the base date at the feeder's
FY2025-26 average new inverter), 5.1 (hosting capacity), 6.1 (assignment to the largest excess) and 7.1 (rounding);
the council's letter (the two campaigns, their sign-up dates and drops); the program terms (owner-occupiers of
houses); the dictionary's field definitions. Executed word for word on the clean records they give connected
capacity, the base forecast at 31 August 2029 and the hosting capacities exactly (R2), and leave one quantity
unexecuted: each 2026 program's impact at the design point, which no sentence computes and no file states. The only
per-campaign counts a document gives are the council's systems installed and homes letterboxed; taking the impact as
the systems installed per home letterboxed executes every sentence and files YRB24 at 4.2 MW, and per house without
PV YRB24 at 3.9, so a literal execution does not give the golden. The golden needs the counterfactual, estimated from
the register against the suburbs whose campaign had not yet run. Every term in the fork table resolves to one reading
or converges.

## Oracles

- **The council's systems installed** equal the register's program-referenced connections for every campaign: a
  control on the installed count, true under every estimate (none confirms what a campaign added).
- **The council's homes letterboxed** and the letter's drops: R0's denominator; they tie under every estimate.
- **The hosting capacity assessment**: hosting capacity and minimum demand only; no connected capacity, excess or rank.
- **The DER Register extract and the re-allocation log** (the asks' path): no rung reads them. None ties only under
  the golden.

## Ask sheet

**Main call's declared row population:** every row of `eg_connection_applications_20260901.csv`,
`nmi_network_model_20260831.csv`, `nmi_property_xref_2026.csv`, `merindah_rates_roll_2026-27.csv` and
`legacy_inverter_equipment.csv`, the council's program summary and letter, NPP-114 and the hosting capacity assessment.
Device and hazard rows in it: 0. The four asks read `der_register_extract_yarrabin_20260901.csv` and
`nmi_reallocations_2019-2026.csv`, which no rung of the call reads, and the network model for placement (device-free);
the call is asserted unchanged with both ask files emptied, and the connection register carries no replaced or
eleven-character NMI. Each ask is a measure every feeder carries (its DER on the national register) that the call does
not turn on; none is keyed to the call, its construction or its figures; no two share a primary device. No sentence in
the pack adjudicates a device: the dictionary states each field flatly. Round 3 left the asks' wording, files, devices
and code unchanged; the regenerated world moved their figures, and every stop below is re-measured on the round-3 pack.

**Ask 1. For every feeder, how many active DER Register sites it supplies** (8 counts; `calc.ask_d`).
- H18 home: the market register's count of DER sites on each feeder, beside the distributor's own forecast; a measure
  every feeder carries that the call never reads.
- Golden: YRB21 3,443; YRB22 3,194; YRB23 2,128; YRB24 2,783; YRB25 3,680; YRB26 2,180; YRB27 1,838; YRB28 2,927.
- Construction: a site is the premises' NMI (ten characters; a builder's temporary supply NMI read at the NMI that
  replaced it in the re-allocation log) with at least one active AC connection, placed on the feeder the network model
  shows supplying it at 31 August 2026 ("it supplies"; the network model's `feeder`: "Feeder supplying the NMI at 31
  August 2026"). An abolished NMI no feeder supplies drops out.
- Primary device (D2, a label stored before a silent switch): Mirrabee's extraction stamps each AC connection with
  the feeder its NMI was on when the connection was lodged; five load transfers (2023 to 2025) moved streets between
  feeders, so 491 active connections at 431 sites carry a feeder that no longer supplies them, and every feeder gains or
  loses some. The dictionary says only "Feeder, added by Mirrabee's extraction." The tell is the register's
  `feeder_at_application` against the network model for the same NMIs, a cross-file cut.
- Hazards: H1 checksum NMIs (5,628 of 30,921 rows, at 3,678 connections, lodged through the newer portal with eleven
  characters); H2 temporary NMIs (70 rows at 61 connections lodged against a builder's supply); H3 several active
  connections at one site (an installer who left the old connection active after an alteration, beside a battery's own
  connection); H5 abolished NMIs (24 active connections at NMIs no feeder supplies).
- Path (5 files, 9 columns): the DER extract (`ac_connection_id`, `nmi`, `ac_connection_status`, `feeder`), the
  re-allocation log (`old_nmi`, `new_nmi`), the network model (`nmi`, `feeder`), the dictionary.
- Stops (measured, each off the golden on all 8): the extract's own feeder, YRB27 1,933 and YRB23 2,336; active AC
  connections counted, YRB26 2,335; NMIs not carried through the re-allocation log, YRB27 1,831 and YRB24 2,778; NMIs as
  lodged with the extract's feeder, YRB25 3,798.
- Lazy delta: the natural pipeline (filter Active, count distinct NMIs by the extract's feeder) misses 8 of 8.
- Realism: a distributor filters the national register to one zone substation by the feeder in its NMI history at
  each lodgement; a later load transfer leaves the stamp behind.

**Ask 2. How many of those sites were first lodged in FY2025-26** (8 counts; `calc.ask_a`).
- H18 home: the new DER sites on each feeder over the last financial year, the market register's view of the growth
  the trend carries.
- Golden: YRB21 98; YRB22 177; YRB23 91; YRB24 255; YRB25 204; YRB26 75; YRB27 158; YRB28 159.
- Construction: a site's first lodgement is the earliest `registered_date` of any AC connection at the site,
  decommissioned connections included; counted where it falls in 1 July 2025 to 30 June 2026.
- Primary device (D8, an anchor on the current record, not the first): an alteration lodges a new AC connection and the
  old one is decommissioned (2,800 decommissioned connections), so a site's active connection is often younger than
  the site; read off the active connections, every altered site counts as new. The tell is the decommissioned rows at
  the same NMI, which a pipeline filtering Active first never keeps.
- Over-cleaning half: none needed; the feeder stamp does not move this ask (every connection lodged after the last
  transfer is stamped right, asserted), so the stamp's repair earns nothing here.
- Hazards: H1 (an old connection under ten characters and its replacement under eleven read as two sites), H2.
- Path (5 files, 8 columns): the DER extract (`ac_connection_id`, `nmi`, `ac_connection_status`, `registered_date`),
  the re-allocation log, the network model, the dictionary.
- Stops: the active connections' own registration, YRB27 170, YRB26 108 (all 8 off); NMIs as lodged, YRB22 248 (all 8
  off); not carried through the re-allocation log, YRB22 170 (5 of 8 off).
- Lazy delta: the natural read misses 8 of 8.
- Realism: the DER Register keeps a replaced connection as Decommissioned beside its replacement; a register of AC
  connections dates each connection, never the site.

**Ask 3. The inverter capacity at those sites** (8 figures, kW to the nearest 10; `calc.ask_c`).
- H18 home: the market register's installed inverter capacity on each feeder, the reconciliation partner of NPP-114's
  connected capacity.
- Golden: YRB21 19,280; YRB22 18,950; YRB23 12,350; YRB24 18,110; YRB25 21,770; YRB26 12,200; YRB27 11,800; YRB28
  16,980 kW.
- Construction: each active AC connection's inverter ratings summed, except a two-inverter connection lodged on the
  older installer portal (before July 2024), whose every inverter row carries the connection's total (its rating is
  the model's nameplate times its rows), counted once.
- Primary device (D3, a field's meaning set by the portal's date): the older portal asked one rating per inverter and
  installers entered the connection's total there; 373 active two-inverter connections carry it, beside 261 newer ones
  rated per inverter. Summing rows doubles the old ones; the duplicate sweep (identical rows dropped) halves the new
  ones. The tell is the model name's rating (`Primo 5.0` on a 10.00 kW row) and the register's `inverter_kw_ac`, each in
  another column or file.
- Hazards: H2, H4 the feeder stamp (all 8), H3 (an old connection left active counts, both are active).
- Path (6 files, 11 columns): the DER extract (`ac_connection_id`, `nmi`, `device_type`, `model`, `rated_power_kw`,
  `ac_connection_status`, `registered_date`), the re-allocation log, the network model, the connection register
  (`inverter_kw_ac`, the referee), the dictionary.
- Stops: rows summed, YRB22 19,580 (all 8 off); duplicate rows dropped or one row per connection, YRB22 18,740 (all 8
  off); the extract's feeder, YRB25 22,130 (all 8 off); not carried through the re-allocation log, YRB27 11,740 (all 8
  off).
- Lazy delta: the natural sum misses 8 of 8; the hygiene repair misses 8 of 8.
- Realism: a portal form with one rating field per inverter, filled with the system's total until the form changed,
  is ordinary.

**Ask 4. The battery storage at those sites** (8 figures, kWh to the nearest 10; `calc.ask_b`).
- H18 home: storage that can absorb a feeder's midday PV, reported beside each feeder's PV.
- Golden: YRB21 3,260; YRB22 2,780; YRB23 2,000; YRB24 2,560; YRB25 3,080; YRB26 2,280; YRB27 1,560; YRB28 2,510 kWh.
- Construction: per active battery AC connection, the module rows summed, except a Sungrow SBR stack, whose installer
  app lodges one device per module each carrying the stack's total, counted once.
- Primary device (D6, an event's quantity on every line it covers, per product): BYD and GoodWe stacks lodge one row
  per module at the module's size; Sungrow SBR stacks (272 of 1,679 active battery connections) one row per module at
  the stack's total. Summing rows multiplies every SBR stack by its modules; one row per connection, or dropping the
  duplicate rows, drops every other stack's modules. The tell is an SBR site summing to several times the register's
  `battery_kwh` for the NMI.
- Hazards: H2 (3 of 8), H4 (8 of 8), H5.
- Path (6 files, 10 columns): the DER extract (`ac_connection_id`, `nmi`, `device_type`, `model`,
  `storage_capacity_kwh`, `ac_connection_status`), the re-allocation log, the network model, the connection register
  (`battery_kwh`, the referee), the dictionary.
- Stops: rows summed, YRB27 2,440 (all 8 off); one row per connection or duplicate rows dropped, YRB27 1,120 (all 8
  off); the extract's feeder, YRB22 2,720 (all 8 off); not carried through the re-allocation log, YRB27 1,530 (3 of 8
  off).
- Lazy delta: the natural sum misses 8 of 8; the hygiene repair misses 8 of 8.
- Realism: installer commissioning apps differ by brand in how they lodge a modular battery; a register holds what each
  app sends.

**Hazard table**

| Hazard | Root cause | Asks moved (measured) |
|---|---|---|
| H1 checksum NMIs | the newer installer portal lodges the NMI with its checksum digit | sites, first lodged, inverter, storage (as lodged: all 8 on each) |
| H2 temporary NMIs | builders' systems lodged against the temporary supply | sites 8, first lodged 5, inverter 8, storage 3 |
| H3 several active connections at a site | an installer left the old connection active; a battery's own connection | sites (counted by connection, all 8) |
| H4 the feeder stamped at lodgement | load transfers after lodgement | sites (primary), inverter 8, storage 8; first lodged 0 |
| H5 abolished NMIs | knock-down rebuilds; the DER record left active | sites, inverter, storage (with H4) |

**One reading of "at those sites".** The capacity and storage are the DER Register's own records for its active
connections at those sites (the register the sites are counted on); the connection register describes the same
systems on another population (approved installations not yet connected, removals the DER Register still shows
active, old connections an installer left active), so its totals at the same NMIs differ and serve only as the
referee below.

**Referee.** The connection register's `battery_kwh` and `inverter_kw_ac` for an NMI arbitrate the per-row conventions
(SBR rows against the NMI's battery, asserted for 90 per cent or more of matched stacks; old-portal rows against the
NMI's inverter capacity) without handing over a level: the register's totals at the DER sites differ from the golden
(asserted through the stops).

**The cracker sheet.** The cracker filed YRB27 at 1.9 MW, ran the hygiene battery (NMI formats normalised, unmatched
NMIs resolved through the re-allocation log, exact duplicates, fan-out, counts that tie) and executed every filed rule:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, 8 site counts | active connections, NMIs normalised and re-allocated, distinct sites by the extract's feeder | the feeder stamped at lodgement moved 431 sites | miss |
| Ask 2, 8 counts | the active connections' registration dates by site | the site's first lodgement sits on a decommissioned connection | miss |
| Ask 3, 8 capacities | inverter rows summed after dropping exact duplicate rows | the newer portal's per-inverter rows are halved; summing instead doubles the older portal's | miss |
| Ask 4, 8 storage totals | battery rows summed after dropping exact duplicate rows | every modular stack loses its modules; summing instead multiplies the SBR stacks | miss |
| Chart (recommendation block) | the bars from the forecast | carried by the main call, scored with it | outside |

The mirror sheet (the same response stopped at R0, R1 or R2, all YRB24) differs only on the recommendation criteria:
no ask couples to the call, and the mirror's runner-up (YRB27) is not the golden's.

Mirror leakage: 8 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 36 recommendation (the feeder, its excess, the runner-up and its excess, the gap,
the two bulk-buys, the chart's named parts), 9 instruction following, 55 asks over 32 figures (1.72 each). The cracker
keeps about 8 per cent of the ask weight: C = 36 + 9 + 4.4 = 49.4. The mirror keeps r of about 4 (the files and the
chart's structure; no wrong route files the golden's runner-up with its figure, asserted): S = 4 + 9 + 4.4 = 17.4, a
pair of 33.4. The most obvious device is Ask 1's stamp (a cracker who places sites on the network model's feeder after
joining it for the NMIs cracks it): it adds 12.65 (8 figures, a quarter of the ask weight, less the credit already
counted) and the pair rises to 39.7. Both top responses on the call with no device cracked: 49.4. A response that
lands the feeder by assuming a round share of the installed systems additional (a third, two fifths, a half) keeps
the feeder and at most the runner-up's name: about 12 of the 36.

Pair ceiling: 39.7

## Prompt

`prompt.txt`, rewritten at round 3 and gated by `voice-check.py` (in `precut.py`, 869 characters): the round-2
binding "forecasting rooftop PV as NPP-114 sets out" is gone, and "how much PV each bulk-buy will add" is now "how
much each bulk-buy will raise its feeder's PV by that date" (the estimand, with the design point); the call as a
question with its forcing facts (the FY2027-28 program, the council's spring 2026 bulk-buys), the workbook's figures
(the excess at 31 August 2029, the runner-up and the gap), the four per-feeder DER Register figures ("how many of
them", zero a grammatical answer, H23), the chart's named parts and the rounding once at the close.

## Build record

Stage 3 of round 3, built 2026-10-15 by `python3 task136/generator/build.py` (pack, goldens, `metadata.json`,
`generator/figures.json`, `checks.py`, `verify.py`, a second full build compared byte for byte, `target.zip`).

- **The call.** YRB27, 1.900 MW above its spring 2029 hosting capacity (forecast 16.090 MW against 14.19); runner-up
  YRB24 at 1.696 (25.346 against 23.65); gap 0.204; YRB22 third at 1.395. The seven campaigns added 627.8 systems on
  15,349 owner-occupied houses without PV at their openings (0.04090 a house, standard error 0.00063, spread 0.046),
  against 1,431 installed (0.09323); Bindarra Waters 185.6 systems (4,537 houses) at 9.15 kW, 1.698 MW; Wattleview 76.0
  (1,857) at 9.35 kW, 0.710 MW. Graded as 1.9, 1.7, 0.2, 1.7 and 0.7, the corridor of 33 constructions and one
  standard error either way inside every bin (Ladder).
- **Default path.** YRB24 at 4.164 MW, runner-up YRB27 at 2.456, gap 1.708; Bindarra Waters 4.165 MW and Wattleview
  1.266 MW. The reflex: YRB24 at 3.868, Bindarra Waters 3.870 MW. The event study: YRB24 at 2.355 to 2.599.
- **Clean truth (R1 to R3).** R1: the golden's decisive computation reads the register's rows through the rates roll
  and the cross-reference, and no shipped column holds a campaign's addition. R2: the pack read by its filed rules
  gives back the world's connected capacity, trend, averages, installed counts and pools exactly, and each campaign's
  estimated addition sits within seven per cent of the households it truly brought in. R3a: on the world's records,
  installed per letterbox files YRB24 at 4.2 and per house without PV YRB24 at 3.9. R3b: the true additions per house
  without PV file YRB27 at 1.9 with every golden figure. R3c: no plant (no document states a campaign's addition, a
  share, a rate or an excess; the assessment ranks nothing; the realism sweep's repeated-block check).
- **Gates.** `checks.py` 483 assertions; `verify.py` 97 checks from the bundle alone; two builds byte-identical
  (`target.zip` sha256 8e187f80ae5fea89...); `figures_check.py` 70 figures, none absent; `precut.py` 49 checks, 0 FAIL,
  0 WARN; `voice-check.py` PASS; container audit clean on the pack and the goldens; the archive's 15 members equal the
  pack. `guard.py validate` clean; `check` and `heart` WARN (`people.first`, answered under Guard), no BLOCK, nearest
  text 0.04; `surface` exit 0, one pair promoted (task450, surface proximity, retired), differentiated on the card.
- **Leak sweep** (`leak.py --asof 2026-10-12`, REVIEW, no LEAK, sweep 11 clean). Each REVIEW line, harmless: NPP-114
  carries the call's words because it is the procedure that assigns a hosting-capacity augmentation from the capital
  works program, and it names no feeder; NPP-114 (installed, systems, months, connected, window, impact), the letter
  (campaign, suburb, application) and the assessment (systems, connected, design) share the stump paragraph's ordinary
  nouns, and none names a comparison, a counterfactual, a pulled-forward install or a share; `device_type` is the DER
  Register's own device field.
- **Not run here.** The leak reader and the determinism judge (stage 4) are the main session's; nothing in this round
  has been read by either.

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
- Rewriting NPP-114's revision 3 note, the council letter's program-reference sentence or the program summary's footnote
  on SS references (the stage-4 reader's realism notes): not done at the reship; each is a document rewrite after the
  reader and the judge read the pack, needing another read, for no graded figure or call input. The revision note
  records what a procedure owner records (the clauses a revision added), and the letter and footnote say how the
  council's own campaigns are lodged, which the register's program references show anyway.
- Moving the hosting capacity assessment's customer counts or its cited model date (the judge's cosmetic note that they
  equal the 31 August model's counts): not done; the report, issued 24 July 2026, counts the NMIs energised by its 30
  June 2026 model, and no NMI was energised, abolished or moved between feeders in July or August 2026 (the latest first
  energisation is 14 June), so the two dates hold the same set; asserted in `checks.py`, and any other count would
  contradict the network model.
- Filing a 12-month window to close SF13's six-month reading (gap 0.428, a bin under the golden's 0.506, the call,
  runner-up and bulk-buys unchanged): rejected, a filed window names the first-application basis and hands over the
  stump; the reading is recorded and asserted as the same call.
- Round 2 shipped design: decisive step read as a hidden rule and as rule application per the rule 3 audit, because
  the prompt bound the call to NPP-114 ("forecasting rooftop PV as NPP-114 sets out"), NPP-114 4.2 filed the pooling
  formula with its denominator left blank, and the winning basis (first applications in the year before sign-ups) was
  a construct only a denominator search over seven campaigns recovers, which the round-2 note itself set against the
  textbook per-eligible-house transfer. Round 3 removes the pooling clause and the binding and moves the decisive step
  to the bulk-buys' net addition.
- Keeping round 2's uptake basis and deleting only the pooling clause and the binding: rejected; the basis would still
  be found only by searching denominators over seven points, the audit's own finding, against the field's standard
  per-eligible-house transfer.
- Filing the comparison (a sentence such as "a program's impact is read against areas where it has not yet run") in
  NPP-114 or the prompt: rejected, it files the method and makes the decisive step rule application; 4.1 files only the
  impact at the design point.
- The audit's two-year window ("total installs in the two years after its campaign"): the design point is three years
  after the 2026 openings, so each past campaign is read over 36 months, cut at the base date for the 2023 and 2024
  campaigns; 24 months converges (SF13) and dropping the cut campaigns converges (SF25).
- Each suburb's remaining waits after 2015 drawn independently, with small never-treated suburbs: the never-treated and
  not-yet-treated comparisons disagreed on Poisson noise alone; the never-treated suburbs were enlarged and every house
  still without PV on 1 January 2015 is laid on one even grid of its remaining hazard, so each window's count tracks
  its expectation within one.
- Organic connection lags of 18 to 95 days: the constructions dated by connection sat 6.4 per cent above the
  received-date reading; organic approvals now connect 8 to 24 days after approval, and every connection-dated
  construction sits inside the corridor.
- The month-by-month comparison keeping a suburb in the comparison through the month its own campaign opened: 3 per
  cent low; a suburb leaves the comparison from the month its campaign opens.
- Wattleview at its first size: an average campaign's addition (per campaign, not per house) landed every graded
  figure; Wattleview was resized, and the per-campaign route now files YRB27 at 2.0 with runner-up YRB22 and every
  figure off.
- A regression of each campaign's addition on its houses without PV and their penetration, first listed as a rival:
  it estimates the golden's own quantity with a covariate and lands every golden figure; it is listed with the
  constructions (SF15).
- Installed systems less one year of the suburb's own uptake, first asserted as a rival that misses every figure: it
  lands the call and the gap; a rule of thumb no record supports, now asserted as a guess that misses the excess and
  both bulk-buys.
- An assumed share of the installed systems as additional, first asserted as a rival: 42.75 to 45.0 per cent lands
  every figure (the records give 43.9); assumed shares are recorded as guesses, with 30, 33, 40, 50, 60 and 70 per cent
  asserted to miss the excess and both bulk-buys.
- Paperbark Grove's year-before count tied Silky Oak's at 58 (the realism sweep): its propensity moved from 0.0214 to
  0.0218 and its count to 59, nothing graded moving; a larger Paperbark Grove (2,440 houses) re-rolled every later
  locality's draws and moved the feeders' average new inverter by up to 0.3 kW.
- Round dwelling counts (3,600 residential addresses and 2,700 owner-occupied houses in Glenmorrow, the council's
  homes letterboxed all whole hundreds): a generator tell. Redrawing every locality's sizes re-rolled every later
  draw and put eight of the constructions and one-sigma moves across or within 0.010 MW of a bin edge (YRB24 to 1.648
  on the never-treated comparison, Bindarra Waters to 1.770 dated by connection); houses and units whose owners never
  applied for PV are now added last, on
  their own stream (6 to 38 owner-occupied houses, 2 to 19 rented houses and 3 to 27 units a locality), which leaves
  every earlier draw in place and every count non-round.
- The golden's note that most participating households "would have gone solar within two years anyway": two years is
  the generator's harvest window, which the records show only as the post-opening dip; the note now says what the
  records show, more than half of the seven campaigns' households within three years (asserted).
