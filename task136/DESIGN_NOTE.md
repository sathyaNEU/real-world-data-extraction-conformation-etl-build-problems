# task136: Mirrabee Energy, the Yarrabin feeder that gets the FY2027-28 hosting-capacity augmentation (architecture 1)

Private, never ships. A new build (wave 2), numbered from seed FC07: the seed's world, decision and quantity are kept
(one accelerated feeder upgrade for rooftop solar above hosting capacity, eight feeders, the 2029 design year, two
neighbourhood campaigns next spring); its published-control architecture (a filed forecast vintage a method must
reproduce) is not used, and the pitfall is re-found from how this dataset's rows come to exist. Nothing is filed that
recovers a rule, and no record blesses the wrong method.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task136.json`, architecture v1, registered 2026-10-12; `guard.py check` WARN on one finding (`overuse.gate_g`, answered below); `guard.py validate` clean |
| Domain / task type | energy-systems-utilities / load-forecasting (a client domain): a distributor's forecast of rooftop PV on each feeder at the design point of an augmentation is the DER half of its demand forecast |
| Objective | Forecasting & Predictive Modeling: the rooftop PV that will be connected on each feeder at 31 August 2029, a window not yet open, against the hosting capacity the 2026 assessment gives for the spring 2029 minimum-demand case |
| Shape | other: the call and its five components (the feeder, its PV over hosting capacity, the runner-up, the gap, the installations each 2027 bulk-buy adds), the chart's named parts and two per-feeder asks on rows the call never reads (16 figures); about 30 criteria, arithmetic in `## Ask sheet` |
| Decision | `pick_one_of_n`, answer unit `named_option` (with its MW figure): which feeder gets the one augmentation |
| Mechanism | gap population (decisive: the population a bulk-buy can still convert); pattern none, generators G8 (reachability: a house that already has PV, a rented house or a unit cannot take a bulk-buy, binary per dwelling) then G14 (the yield conditioned on that reachable pool); Gate G `method_or_model_selection` (the transfer basis is the method, and the seven past campaigns select exactly one); strategy `population_selection` |
| Layer 2 family / pattern | `field_method` (market definition: the addressable pool of a DER campaign); `product-analytics/feature-adoption-diffusion-modeling/2` (the eligible denominator at risk) on a new structure, a campaign's yield carried across suburbs behind a three-file join rather than a product's adoption rate (`two_layer.pattern_reused` does not fire: no card carries it) |
| Furniture | forum `line_manager_or_team` (no formal forum: the call is Network Planning's own, NPP-114 section 6 assigning the one augmentation when the FY2027-28 capital works program is compiled; no shipped file or prompt sentence names a forum), forcing event `budget_or_appropriation` (the program funds one accelerated hosting-capacity augmentation), organisation family `utility_or_infrastructure`, role family `research_desk` (the DER forecasting analyst in network planning), context artifact `capacity_report` (the 2026 hosting capacity assessment), calibration `none` (the past campaigns are the history the programme component is estimated from, not an organ), opening `question-first`, question form `which` |
| Spine | `eg_connection_applications_20260901.csv`, the embedded generation connection register: one row per micro EG (rooftop PV) connection application at an NMI, new systems and alterations, 2011 to 31 August 2026; constructed |
| Deliverables | `feeder_upgrade_2029.xlsx` (the call, the forecast by feeder, the two campaigns' installations, the two asks), `yarrabin_pv_vs_hosting_2029.png` (one bar per feeder for its rooftop PV connected at 31 August 2029, its hosting capacity marked) |
| People | drawn with `guard.py names --geo Australia --seed 136 --n 30`, keeping only names with an unused first name and surname: Wanda Thornton (DER forecasting analyst, the requester), Christopher Sheppard (manager, network planning, signs NPP-114), Julie Cochran (sustainability programs officer, Merindah City Council, keeps the bulk-buy log), Bryan Nichols (embedded generation connections lead, the register), Linda Ruiz (GIS analyst, the NMI-to-property cross-reference), Nicole Rocha (customer programs officer, receives the state battery rebate approvals), Tammy Buchanan (consulting engineer, the hosting capacity assessment); none appears in the prompt |

**Guard.** `guard.py check` on the scratch card: WARN, one finding. `overuse.gate_g` (`method_or_model_selection` in six
of the last twelve builds): it is the honest key, because the decisive step is choosing the basis on which past
campaigns' installations carry to a new suburb, and the seven past campaigns select exactly one basis; the mechanism
differs from every recent carrier (task501's eigenvalue, task134's inflow hazard, task135's asynchronous prices), and
the nearest driver on file is 0.07. The bans run against task125, task127 and task130 (the three builds drawn before
this one by draw key). A first draft blocked on `ban.pattern` (C, task127), then on `test.same_driver` (gap population,
pattern E, against task124's lineage and task500 v2) and `test.same_puzzle_older`; the decisive mechanism is carried
honestly by the G-code (G8, reachability), which no recent build carries. Sweeping the card through gap, pattern and
gate combinations confirmed gap population with pattern none and G8 first is clear under either Gate G key. At stage 4,
task128's architecture 3 (drawn the same day, so before this build by draw key) took `executive_team` and heart
blocked on `ban.forum`; no shipped file or prompt sentence named that forum, so the card now carries
`line_manager_or_team`, the honest label for what ships, and heart is WARN on `overuse.gate_g` (answered above) and
`repeat.question_form` (task128 also asks which; the form follows the decision, a pick of one feeder, and the call
sentence is frozen).

**Same-puzzle and same-driver tests.** Gap population, decisive mechanism G8, decision `pick_one_of_n`: no build in the
last twelve carries all three (task124 and task180 carry gap population and pattern none with G14 or G12 first; task501
carries G16). Older carriers of G8 (pattern C's form, task25 and task28, the share one intervention can reach behind a
join) are the nearest family: there the reachable share is a column-free share of a backlog a team can serve; here it
is the denominator on which a past intervention's yield transfers to a new site, and the decision turns on transfer
rather than on reach.

**Abstraction test.** Stripped of nouns, the driver is: a scheduled intervention's yield is carried to new sites from
its past runs, and it is stable only per member who can still respond (inside its area, qualifying, not already
responded), a pool built behind a three-file join, while every single correction fits the past runs no better than the
raw rate. The three nearest drivers (`guard.py nearest`: task86 v2 0.07, a second earlier draw on a shared pool run
forward member by member; task130 v1 0.05, a forward roll from a past snapshot of filed returns; task106 0.05, a shared
finite pool of spare capacity double-booked by per-candidate sizing) share no latent structure, default path or
correction with it. task29's interaction build (0.04), a forward yield from closed interventions whose slope differs by
instrument type, is the nearest idea in other words: there the slope on a visible covariate differs by a visible type;
here no covariate or type separates the past runs, and the move is the denominator itself.

**Data-native sentence.** Merindah's bulk-buys are letterbox drops to every address in a suburb, but only an
owner-occupier of a house with no rooftop PV can sign a contract; the seven past suburbs differed in how many of their
addresses were units, rented houses or houses that already had panels, so their systems per letterbox scatter while
their systems per untapped owner-occupied house do not, and Bindarra Waters, a new estate of owner-occupied houses with
almost no PV, is untapped on a scale no past suburb was.

**Sources read, one line each.** The client pattern `feature-adoption-diffusion-modeling/2` teaches that an adoption
rate needs the eligible denominator still at risk; here that denominator decides how a past campaign transfers, and it
has to be assembled from three files that were never designed to join. `guard.py mechanisms --objective forecasting`
(46 builds): hazards by time since entry (134), selection on the outcome (124), maturity of a claims window (130),
a recycling term (501 v1), corpus-recovered conversion rates (27, 29, 30, 78), censored delays (31, 99), a slowest
sub-unit (52), a fixed-plus-variable cost carried per unit (67), a two-class mix (95), a dated join to caps (117); none
transfers a campaign's yield on the population it can still reach. `stumping/references/client/measured-drivers.md`:
the held tasks are a conjunction whose halves fit no better than nothing, upstream of every graded figure, and a unit
composed behind a join; this build is built to that form (the eligible and the untapped halves each fit the seven
campaigns no better than per letterbox). The seed's header (FC07) for the world only.

**World.** Mirrabee Energy is a regional electricity distributor in south-east Queensland. Its Yarrabin zone
substation (110/22 kV) supplies eight 22 kV feeders, YRB21 to YRB28, serving 47,515 NMIs (47,026 residential) in Merindah's
western growth corridor, with 14,141 residential and 340 business rooftop PV systems connected at 31 August 2026. Merindah City
Council's Solar Streets program has run a bulk-buy in one or two suburbs a year since 2018 (none in 2020): a letterbox
drop to every address, information nights, one appointed installer at a negotiated price, a twelve-week sign-up window
and installations over the following months. The council's 2026-27 budget schedules two campaigns for spring 2027
(sign-ups 6 September to 26 November 2027): Bindarra Waters, a master-planned estate built 2019 to 2025 and supplied by
YRB24, and Wattleview, an established suburb on YRB27. Mirrabee's network planning procedure NPP-114 (revision 3, March
2026) sets how rooftop PV is forecast for an augmentation; the 2026 hosting capacity assessment (Buchanan Power
Engineering, July 2026) gives each feeder's hosting capacity for the spring 2029 minimum-demand case. The FY2027-28
capital works program funds one accelerated hosting-capacity augmentation, and NPP-114 section 6 sends it to the
feeder with the most forecast rooftop PV above hosting capacity at the design point.

As-of dates: the connection register and the network model are extracted at 31 August 2026 (run 1 September 2026);
the council's letter on the 2027 campaigns is dated 14 August 2026; the request is made on 12 October 2026; Network
Planning compiles the FY2027-28 capital works program by 24 November 2026.

## Default path

1. Read NPP-114. From the connection register, take each NMI's latest connected configuration, residential and
   business (an alteration carries the NMI's whole system after the work), place each NMI on its feeder in the
   network model at 31 August 2026 and sum inverter ratings: the rooftop PV connected on each feeder.
2. Build the base trend as NPP-114 sets it: the yearly increase in connected capacity over FY2023-24, FY2024-25
   and FY2025-26, less the systems connected through a program in that year, averaged and carried three years to 31
   August 2029.
3. For the two 2027 bulk-buys, take each past campaign's systems installed (the council's log, equal to the register's
   program-coded connections) over its homes letterboxed, average the seven participation rates and apply the average
   to the homes the 2027 letterbox drops will reach (Bindarra Waters 6,240, Wattleview 3,300), each system at the
   feeder's FY2025-26 average inverter rating.
4. Subtract each feeder's hosting capacity from the 2026 assessment and pick the largest excess.

Ends on: YRB22, about 1.5 MW over its hosting capacity at 31 August 2029 (Bindarra Waters adds about 90 systems,
Wattleview about 50).
Golden: YRB24, about 1.9 MW over its hosting capacity (Bindarra Waters adds about 240 systems, Wattleview about 30).

## Stump sentence

A competent solver collapses alterations, builds NPP-114's base trend, carries the past bulk-buys' systems per home
letterboxed onto the 2027 letterbox drops and files YRB22 at about 1.5 MW over hosting capacity (Ends on); the step that
lands it there is transferring each campaign's yield per contacted address instead of per owner-occupied house still
without rooftop PV in its suburb, which leaves YRB24's untouched Bindarra Waters estate with well under half its campaign:
the golden is YRB24 at about 1.9 MW.

## Three rules

- **Domain test:** the deciding quantity is each feeder's design-point rooftop PV against its hosting capacity, with a
  bulk-buy's installations forecast from the rooftops that can still take it up (owner-occupied houses with no PV
  yet), which is how a distribution planner forecasts DER on a feeder for an augmentation; with another field's nouns,
  hosting capacity, inverter ratings, rooftop ownership and the embedded generation register have nothing to attach to.
- **Analyst test:** a strong analyst who reads NPP-114, collapses alterations to one system per NMI, places NMIs on the
  network model's feeders and counts each past campaign's installations correctly still carries them per home
  letterboxed (YRB22 at about 1.5 MW); per owner-occupied house, per home without PV, per feeder, as a rate ratio on the
  suburb's own adoption, or as an average count, each leaves Bindarra Waters at 26 to 140 systems against about 240
  and the augmentation with YRB22.
- **Layer 1:** an embedded generation register at application grain (alterations carrying the NMI's whole system,
  withdrawn and approved-not-connected applications, rows migrated in 2019 with panel capacity only and the inverter
  in an equipment table), the feeder at application against the network model after a 2023 load transfer of Yarrabin North from YRB23 to
  YRB21, the council's rates roll keyed by property number joined to NMIs only through the GIS cross-reference
  (dual-occupancy and granny-flat NMIs), the council's program workbook in its own layout, and, on the ask paths, a
  national DER Register extract at device grain (builders' systems under temporary supply NMIs, NMIs with a checksum
  digit from the newer installer portal, decommissioned connections) and the NMI re-allocation log. Each is something these systems produce; none decides the call.
- **Layer 2:** the shortcut is to carry a past campaign's yield per address it reached (the council's own
  participation rate), or to refine it one step (per owner-occupied house, per address without PV); the expert carries
  it per owner-occupied house still without PV in the suburb when the campaign opens, the only basis on which all seven
  past campaigns agree, and builds that pool for the 2027 suburbs from the rates roll, the cross-reference and the
  register.

## Gate G

- **Litmus.** No. Every file is correct: the connection register, the network model, the cross-reference, the rates
  roll, the council's program log and letter, NPP-114 and the hosting capacity assessment. No stakeholder states a
  number the task overturns, and no file states a 2029 forecast, a campaign's expected yield or a participation rate.
- **Primary mechanism:** `method_or_model_selection` (the basis on which past campaigns carry to a new suburb is the
  method; seven past campaigns select exactly one, and the correctly read past does not pin the forecast without it).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test.** With every file clean (one row per NMI, no alterations, no migrated rows, the feeder of record
  on every row, a one-to-one cross-reference), the per-letterbox transfer still files YRB22 and the per-house transfer
  still files YRB22; the decisive step is untouched by any cleaning.
- **Deletion test.** Delete the distractors (the peak demand forecast and the battery rebate approvals), the DER
  Register extract and the NMI re-allocation log: the call recomputes
  unchanged (asserted) and the default path is still wrong. Nothing in the pack is wrong for the default to be wrong.
- **Lens swap.** The default and the golden are not one population at one moment under two lenses: they are two
  transfer bases for the same seven campaigns, and only one of them reproduces the seven.
- **No artifact ranks or prices the decision.** No shipped file states a 2029 forecast, an excess over hosting capacity,
  a campaign forecast, a participation rate or a conversion rate. The council's log reports what each past campaign
  did (letterboxed, registrations, contracts, systems installed), which is history, not a basis.

## Readability screen

Six tests per rung: 1 filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a reflex
of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction, ratio or
half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 per home letterboxed (the council's participation rate on the 2027 letterbox counts) | the council's log and letter carry the letterbox counts, and the letter gives the 2027 drops | the log's `Homes letterboxed` column | yes | no | no | yes (a ratio of two reported figures) | readable |
| R0a an average campaign (mean systems installed) | no | the log's `Systems installed` | yes | no | no | yes | readable |
| R0b the campaign as a rate ratio on the suburb's own adoption that year | no | no | partly (an event study's lift) | no | no | no | readable |
| R1 per owner-occupied house in the suburb | the program terms ("owner-occupiers of houses") make the solver ask how many there are | the rates roll's land use and rating category | yes, once eligibility is read | no: it fits the seven campaigns worse than R0 (spread 28 against 24 per cent) | no | no | readable |
| R1b per address with no PV in the suburb | no | the register's NMIs | yes (a home with panels cannot buy them again) | no: worse than R0 (26 per cent) | no | no | readable |
| R2 per untapped owner-occupied house on the whole feeder | no | no | yes (the feeder is the forecast's unit) | no: worse than R0 (35 per cent) | no | no | readable |
| R3 (decisive) per owner-occupied house still without PV in the suburb when its sign-ups open, built through the rates roll, the NMI-to-property cross-reference and the register | no sentence names the pool, the campaign's reach or a rate per house; NPP-114 says only that a program adds the systems the records of past programs indicate | no column flags an untapped or eligible dwelling; the rates roll carries no PV, the register no rating category, and the cross-reference is the only bridge | no: the reflexes are R0 to R2, and each single correction is rewarded by nothing | the seven campaigns fit it within half a per cent and fit every single correction worse than the raw rate, so no partial step is confirmed on the way | no | no: a pool composed across three files, per suburb, at each opening date | silent |

The decisive rung is silent because its two halves each look like a dead end: a solver who tries the owner-occupied
houses, or the addresses without PV, sees the seven campaigns scatter more than they did per letterbox and goes back
to the council's rate; only the conjunction, built behind the cross-reference, makes the seven agree.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. `checks.py` asserts each row (the
alternative computed and shown to move the call or its figures, or shown to converge).

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "rooftop PV" on a feeder | all micro embedded generation (inverter capacity 30 kVA or less) at NMIs the network model places on the feeder, residential and business; every register system is 30 kW or less (asserted) | residential NMIs only | YRB24 at 1.6 MW, runner-up YRB25, gap 0.9 (business systems are 4 to 10 per cent of a feeder's base) | NPP-114 2.1 ("at a residential or business NMI", asserted in the PDF) and 2.2 |
| SF2 | a system's capacity | the inverter capacity (kW AC) of the NMI's latest connected configuration; an alteration replaces the configuration it alters | every connected application summed; panel capacity (kWp) | summed alterations file YRB21 at 3.4 MW over YRB22's 3.2 under every transfer basis; panel capacity files YRB21 at 4.5 MW | NPP-114 2.2 ("An alteration replaces the configuration it alters"; "inverter capacity (kW, AC rating)", both asserted in the PDF); the dictionary's definition of `inverter_kw_ac` |
| SF3 | rows migrated in 2019 with panel capacity only | the inverter capacity from the legacy equipment table, joined on the legacy application number | panel capacity used for those rows; the rows dropped | same call (asserted) | NPP-114 2.2 (inverter capacity); the equipment table carries every migrated inverter |
| SF4 | "connected" at a date | an application with status Connected and a connection date on or before the date, not later Removed before it | approved but not connected included | same call; every base moves under 2 per cent (asserted) | NPP-114 2.2 |
| SF5 | the feeder of an NMI | the network model at 31 August 2026 | the feeder recorded on the application | same call (the 2023 transfer of Yarrabin North moves YRB21 and YRB23 only; asserted) | NPP-114 3.1 |
| SF6 | the base date | 31 August 2026, the register extract | 30 June 2026 (the last financial year end) | same call, figures move | NPP-114 3.1 (the last day of the month before the forecast is prepared) |
| SF7 | the trend | the average, over FY2023-24 to FY2025-26, of the year's increase in connected capacity less the capacity of program systems first connected in the year | new connections only; program systems left in; a fitted line | same call under the first two (asserted); a fitted line is not the trend 3.2 defines | NPP-114 3.2 |
| SF8 | the years carried | three (31 August 2026 to 31 August 2029) | 3.25 or 2.92 years | same call, figures move | NPP-114 2.4 (design point) and 3.2 |
| SF9 | "program system" | an application carrying a Solar Streets program reference; equal to the council's systems installed for every campaign (asserted) | the council's contracts signed (cancelled contracts included) | the contract count raises each campaign's rate by the same factor and leaves the call; it moves the two campaign figures (asserted) | NPP-114 2.3 (systems installed under a program) |
| SF10 | the systems a 2027 bulk-buy adds | a count of systems, each at the feeder's FY2025-26 average inverter capacity of systems first connected | systems at the past campaigns' own average size (6.68 kW against YRB24's 7.25) | same call (asserted); YRB24 at 1.8 MW, gap 0.2 | NPP-114 4.2 (the feeder's average for systems first connected in the last complete financial year) |
| SF11 | the date the 2027 pool is counted | the opening of sign-ups (6 September 2027), the base pool less a year of the suburb's FY2025-26 organic adoptions | the pool at 31 August 2026 | converges: 240 and 30 systems and 1.9 MW either way (asserted) | the records converge |
| SF12 | "owner-occupied house" | rates roll land use code 02 (single unit dwelling) with rating category Residential owner occupied | every house (code 02); every owner-occupied property | moves the transfer (R1 family) | the seven campaigns: only owner-occupied houses ever took a program system (asserted), and the program terms are for owner-occupiers of houses |
| SF13 | "without PV" at an opening | no application, other than a withdrawn one, received at any of the property's NMIs before the opening | approved-not-yet-connected counted as untapped; or no live connected system at the date (removed systems and pending applications count as without PV), at the openings and for the 2027 pools | converges (rate within 0.02 points; every graded figure unchanged under both, asserted) | the records converge |
| SF14 | a suburb | the rates roll's locality | the network model's address suburb | same rows (asserted equal in every campaign suburb) | the records converge |
| SF15 | the estimator on the seven campaigns | pooled (all systems over all pools) | the mean of the seven rates; a regression through the origin; with an intercept | converges: 4.57 to 4.58 per cent, 240 and 30 systems, 1.9 MW and a 0.4 MW gap under every estimator and either pool date (asserted) | the records converge |
| SF16 | transfer per letterbox (R0) | refused | the council's participation rate; the stage 4 reader's reading of NPP-114 4.1 (systems installed over homes letterboxed, pooled over the seven campaigns: 1.45 per cent) | YRB22 at 1.5 MW, Bindarra Waters 90 and Wattleview 50 systems, YRB24 fifth (both, asserted) | the records of past programs: spread 24 per cent; misses Bunya Ridge by 36 per cent; by sample coefficient of variation the seven rates vary 0.6 per cent per untapped owner-occupied house against 25.5 per letterbox, 30.1 per owner-occupied house and 27.5 per address without PV, the separation the judge confirmed (asserted) |
| SF17 | transfer per owner-occupied house (R1) | refused | | YRB22 | the records: spread 28 per cent; misses Tallowwood Rise by 38 per cent (asserted) |
| SF18 | transfer per address without PV (R1b) | refused | | YRB22 | the records: spread 26 per cent; misses Glenmorrow by 64 per cent (asserted) |
| SF19 | transfer per untapped owner-occupied house on the feeder (R2) | refused | | YRB22 | the records: spread 35 per cent; misses Glenmorrow by 102 per cent (asserted) |
| SF20 | an average campaign (R0a) or a rate ratio (R0b) | refused | | YRB22 | the records: systems installed spread 44 per cent and miss Tallowwood Rise by 51 per cent; the ratio to each suburb's own adoption misses Silky Oak by 78 per cent (asserted) |
| SF21 | hosting capacity | the assessment's figure for the spring 2029 minimum-demand case | the spring 2026 case beside it | same call, figures move | NPP-114 5.1 |
| SF22 | the excess, the runner-up and the gap | forecast connected capacity at 31 August 2029 less hosting capacity, unrounded, ranked; rounded once to 0.1 MW | rounded figures subtracted | converges (asserted) | NPP-114 6.1 and 7.1 |
| SF23 | a migrated row's inverter (the legacy join) | the equipment table's row with the register's legacy application number | rows paired by file order or by panel size; a number's rows summed; the first or the last row taken | converges: every legacy application number is issued once in the register and once in the equipment table, so every join selects the same inverter (C1, asserted in `checks.py` and `verify.py`); YRB22's connected capacity 13,690 kW under every join | the records converge |
| SF24 | a withdrawn application, for "without PV" at an opening and in the 2027 pools | the house is without PV: nothing was connected under it | an application of any status counted as PV | the seven campaigns fit it about as well (4.66 per cent, so the records do not separate it); same call, YRB24 1.9 MW; Bindarra Waters 244.6 (240), or 245.8 (250) with the pool at the base date (asserted) | the data dictionary's status definition ("Withdrawn: withdrawn by the applicant or lapsed before connection; nothing was connected under the application."), asserted |

The stump is none of these rows: every row is read the same way by a careful reader, and the default path reads them
all correctly. SF16 to SF20 are methods, not readings; they are listed so that each competing model is priced and
refused by the records, never by a reading.

## Ladder

Every rung is a complete pipeline on the same literal estimand (forecast connected capacity at 31 August 2029 less
hosting capacity). Built figures, printed by `checks.py` on every build. The base excesses before the campaigns:
YRB22 1.501, YRB25 1.238, YRB21 1.100, YRB27 0.806, YRB28 0.717, YRB23 0.447, YRB24 0.140, YRB26 -0.623 MW.

| Rung | Construction of the 2027 campaigns | Bindarra Waters systems | Wattleview systems | Winner | Excess (MW) | YRB24's place |
|---|---|---|---|---|---|---|
| T no campaign | the base forecast only | 0 | 0 | YRB22 | 1.501 | 7th |
| R0a average campaign | 51.1 systems each | 51.1 | 51.1 | YRB22 | 1.501 | 6th |
| R0b rate ratio on the suburb's own pace | a campaign's systems as 0.84 times (the mean of the seven) its suburb's own first applications in the twelve months before the opening, applied to the 2027 suburb's twelve months to the base date | 26.1 | 48.0 | YRB22 | 1.501 | 7th |
| R0 per letterbox (default) | 1.449 per cent of homes letterboxed | 90.4 | 47.8 | YRB22 | 1.501 | 5th |
| R1 per owner-occupied house | 2.518 per cent | 140.2 | 50.9 | YRB22 | 1.501 | 3rd |
| R1b per address without PV | 2.108 per cent | 125.5 | 40.3 | YRB22 | 1.501 | 5th |
| R2 per untapped owner-occupied house on the feeder | 2.531 per cent | 138.1 | 41.6 | YRB22 | 1.501 | 3rd |
| R3 golden | 4.580 per cent of owner-occupied houses without PV at the opening | 241.6 | 30.6 | YRB24 | 1.892 | 1st |

- **Position and margins.** YRB24 is 5th on the default (R0), 3rd at best below R3 (R1 at 1.157 MW, R2 at 1.142),
  never 1st or 2nd. Every rung below R3 names YRB22 by 1.21 times over YRB25; R3 names YRB24 by 1.26 times over YRB22.
- **Separation of the graded figures.** Every wrong rung lands both campaign figures in other tens: Bindarra Waters 26
  to 140 against 241.6, Wattleview 40 to 51 against 30.6 (asserted). The excess moves from 1.5 (YRB22's) to 1.9
  (YRB24's) and the runner-up from YRB25 to YRB22.
- **Dominance.** R3 adds 1.752 MW to YRB24 against 1.016 MW on the best wrong rung (R1); the 0.736 MW difference is
  2.1 times the 0.344 MW by which YRB22 leads YRB24 on R1.
- **Grid.** Transfer basis (none and the seven above) x capacity rule (latest configuration or alterations summed) =
  16 cells, plus R3's ten estimator and pool-date cells. Every latest-configuration cell below R3 files YRB22
  (asserted); every summed-alterations cell files YRB21 at 3.4 MW (printed; ruled out by NPP-114 2.2, SF2); R3's ten
  cells file YRB24 at 1.9 MW with a 0.4 MW gap and 240 and 30 systems (asserted). The nearest wrong figure for
  YRB24 is R1's 1.157 MW, 39 per cent below the golden.
- **Worth on the graded figures.** R3 moves the pick, the excess, the runner-up, the gap and both campaign figures;
  nothing graded on the main call survives the default.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | micro EG at NMIs on the eight Yarrabin feeders in the network model (NPP-114 3.1); members not yet observed (the 2027 campaign's systems and the trend's systems to 2029) are the estimand, projected; filed literally |
| 2 | Unit of account | a system is an NMI's connected configuration (NPP-114 2.2); a campaign's yield counts systems (program references, SF9); the pool counts owner-occupied houses (properties) through the cross-reference |
| 3 | Attribution window | the trend's financial years (1 July to 30 June); a program system is excluded in the year it is first connected (NPP-114 3.2), so a campaign whose systems straddle a year end subtracts each where it falls; the two campaigns inside the trend window (Bunya Ridge, Paperbark Grove) connected within one financial year each, and every past program system within nine months of its opening (asserted) |
| 4 | As-of dating | the base date 31 August 2026 (NPP-114 3.1); the network model at the same date |
| 5 | Version basis | one register extract; alterations replace configurations (SF2) |
| 6 | Denominator | the decisive method (R3), refused alternatives priced in SF16 to SF20; not a reading |
| 7 | Weighting | pooled over the seven campaigns; the mean of rates and the regressions converge (SF15) |
| 8 | Window length | the trend window is filed (three complete financial years); the campaign record is all seven campaigns (none before 2018, none in 2020) |
| 9 | Boundary inclusivity | connection dates on or before the base date (NPP-114 2.2); a pool counts applications received before an opening date. Records do sit on boundary days (9 connections on the base date, 18 on financial-year edges, applications received on the first day of five openings); moving each across its boundary (the base date exclusive, the financial years a day late, an opening inclusive) changes no graded figure (C1, asserted) |
| 10 | Rounding path | carried unrounded, rounded once (NPP-114 7.1); the gap is the difference of unrounded excesses and equals the difference of the rounded ones (asserted) |
| 11 | Tie-break | none needed: no two feeders within 0.1 MW at the top (asserted) |
| 12 | Maturity and censoring | every past program system is connected by the base date (the last campaign closed in November 2024; asserted none pending); the 2027 campaigns close in November 2027, inside NPP-114 4.3's six months before the design point |
| 13 | Order of operations | alterations collapsed before summing; pools built per campaign before pooling; C1 on the rest (asserted) |
| 14 | Row order | row order changes nothing (asserted over three permutations) |
| 15 | Duplicate resolution | one configuration per NMI by connection date (SF2); a property with two NMIs counts as one house, untapped if neither NMI has PV (no such property in a campaign suburb; asserted) |
| 16 | Identity normalisation | NMIs are ten characters in the register, the network model and the cross-reference (asserted); the rates roll's property numbers join the cross-reference exactly; every legacy application number is issued once in the register and once in the equipment table (SF23, asserted) |
| 17 | Netting against gross | removals subtract from connected capacity (NPP-114 2.2); no export netting |
| 18 | Dimensional units | kW AC throughout, MW for reporting; migrated rows' panel kWp never enter (SF3) |
| 19 | Code and status semantics | the register's status codes and the rates roll's land use and rating codes are defined in the dictionary (field semantics, never the stump) |
| 20 | Integerisation | the campaign systems are expected counts, graded to the nearest ten; no integer step inside the forecast |
| 21 | Clause scope | NPP-114 4 applies to each program scheduled on a feeder before the design point: the two 2027 campaigns |
| 22 | Forward window contents | the council's letter gives each 2027 campaign's suburb, sign-up dates and letterbox drop; NPP-114 3.2 carries the trend to the design point |

## Literal reader

Executed word for word, the prompt, NPP-114 (2.1 to 7.1) and the hosting capacity assessment define the call as the
feeder whose micro EG connected at 31 August 2029, forecast as the connected capacity at 31 August 2026 plus three
years of the filed trend plus the systems each 2027 program will add, exceeds its spring 2029 hosting capacity by the
most. Every term in the fork table resolves to one reading or converges. The one step the text leaves open is how many
systems each 2027 bulk-buy will add, which NPP-114 4.1 sends to the records of past programs; those records show each
of the seven past campaigns put systems on 4.55 to 4.63 per cent (4.58 pooled) of the owner-occupied houses in its
suburb that had no PV when its sign-ups opened, and no other basis reproduces them (every other basis misses at least
one campaign by a quarter, SF16 to SF20). The only number the records indicate for the 2027 campaigns is that rate on
their own suburbs' untapped owner-occupied houses, which is the golden. No filed sentence prices a program per
letterbox, per house or per feeder. A house whose only application was withdrawn is without PV, because the
dictionary says nothing was connected under a withdrawn application (SF24), and each migrated row's inverter is
the one equipment row carrying its legacy application number (SF23).

## Oracles

- **The council's systems installed** equal the register's program-referenced connections for every campaign: a
  control on the count, true under every transfer basis (it is the numerator of all of them).
- **The council's homes letterboxed** and the 2027 letter's letterbox drops: the numerator's denominator on R0; they
  tie under every basis because no basis changes them.
- **The hosting capacity assessment** states each feeder's hosting capacity and its spring minimum daytime demand: no
  connected capacity, no headroom, no ranking.
- **The DER Register extract** (the asks' path): no rung reads it. None ties only under the golden.

## Ask sheet

**Main call's declared row population:** every row of `eg_connection_applications_20260901.csv`,
`nmi_network_model_20260831.csv`, `nmi_property_xref_2026.csv`, `merindah_rates_roll_2026-27.csv` and
`legacy_inverter_equipment.csv`, the council's program summary and 2027 letter, NPP-114 and the hosting capacity
assessment. The asks' devices live in `der_register_extract_yarrabin_20260905.csv` and
`nmi_reallocations_2019-2026.csv`, which no rung of the call reads; the generator asserts the call unchanged with both
emptied, no temporary NMI in the connection register, and every ask figure computed without the call's transfer basis.

**Ask A. For each feeder, how many systems connected at 31 August 2026 the DER Register does not show, and how many
active DER Register sites have no connected system** (8 feeders by 2 counts, 16 whole numbers).
- H18 home: the DER Register is the market's record of each feeder's DER, and the forecast starts from the
  distributor's register; the reconciliation is the audit trail of the base the forecast stands on (an input
  reconciled to another system's total, the gap made of devices). The call does not turn on it (NPP-114 forecasts
  from the distributor's register).
- Construction: NMIs with a connected system at the base date against NMIs with an active DER Register AC connection
  at the extract, the extract's NMIs read at ten characters, registrations lodged under a builder's temporary
  supply NMI carried to the permanent NMI through the re-allocation log, counted by the network model's feeder (the
  extract's feeder column for an abolished NMI; the two agree on every known NMI, asserted in `verify.py`).
- Primary device (D1, the same records under two key schemes): a system a builder installs before handover is
  registered by the installer under the temporary supply NMI; at handover the distributor creates the permanent NMI and
  moves its connection record, while the DER Register keeps the temporary NMI. Matched on NMI, each such system is
  counted twice, once as connected but unregistered and once as a registered site with no connected system; the
  extract's feeder column (stamped by the distributor's extraction from its NMI history) places both on the right
  feeder, so nothing fails to join. Every feeder carries some (5 to 11 active connections under temporary NMIs on each
  established feeder, 121 on YRB24), so all 16 figures move. Nothing in the pack says how the DER Register keys
  builder systems; the tell is a DER Register NMI absent from the network model, which only the re-allocation log
  resolves.
- Hazards: HA1 (D6) the extract is at device grain, an AC connection's inverters and batteries on separate rows; HA2
  (D2) replaced systems remain on the extract as Decommissioned; HA3 (D3, key format) records lodged through the newer
  portal carry the NMI with its checksum digit (3,024 of 19,254 rows, eleven characters).
- True gaps: systems connected that the installer never lodged or lodged after the extract, DER Register sites for
  systems installed but not yet connected (the application still Approved at the base date), and sites whose system
  was removed with the DER record left active, including abolished NMIs of houses demolished for a rebuild (the
  over-cleaner who drops every NMI the network model lacks loses these).
- Converging readings (asserted): sites counted by AC connection instead of by NMI (no unconnected site has two active
  connections); the extract read as at 31 August 2026 (no connected system lodged after it; the one later
  decommissioning sits at a site with a connected system); a connected system whose only records are decommissioned
  (none).
- Path (6 files, 13 columns): the DER Register extract, the re-allocation log, the connection register, the network
  model, the dictionary, the export manifest; `nmi`, `ac_connection_id`, `device_type`, `ac_connection_status`,
  `registered_date`, `feeder`, the log's `old_nmi`, `new_nmi`, `reason`, the register's `status`, `connection_date`
  and `removal_date`, the network model's `feeder`.
- Stops (built; each off the golden on all 16 figures, asserted): S1 natural, raw NMI strings (YRB24 224 and 234); S2
  NMIs read at ten characters, no re-allocation (YRB24 121 and 129); S3 S2 with every NMI the network model lacks
  dropped as off-network (YRB24 121 and 6); S4 S2 with device rows counted for the second figure (YRB24 121 and 151);
  answer (YRB24 2 and 8; all feeders 79 and 63).
- Lazy delta: S1 wrong on 16 of 16.
- Realism: builder-installed systems on temporary supplies are routine in growth estates, and installers register DER
  against the NMI on the job sheet; a distributor's extract stamping each record with the feeder from its own NMI
  history is how it would filter the market register to one zone substation.

**Ask B. Each feeder's battery storage at the DER Register's active sites** (8 figures, kWh to the nearest ten).
- H18 home: a measure every candidate carries (storage that can absorb a feeder's midday PV) that the call does not
  turn on (NPP-114 forecasts PV without netting storage); the capital works paper reports it beside each feeder's PV.
- Construction: per active battery AC connection, its storage capacity once, by the extract's feeder column (equal to
  the network model's feeder through the re-allocation log, asserted).
- Primary device (D6, an event's quantity on every line it covers): the extract repeats each AC connection's storage
  capacity on every battery device row, and a modular battery has one device row per module (566 of 1,013 active
  battery connections), so summing device rows multiplies every modular system by its module count. Every feeder has
  modular systems, so all 8 figures move. The dictionary states the field flatly ("Storage capacity (kWh), battery
  rows."); the tell is a connection whose module rows each carry the whole system's capacity.
- Hazards: HA1 (shared, device grain); HA2 (shared) decommissioned batteries kept moves 5 of 8 feeders; HA4 (D1,
  shared with Ask A's primary) a solver who places batteries on feeders by joining NMIs to the network model without
  the re-allocation log drops builders' batteries (YRB23, YRB24 and YRB27 move).
- Path (5 files, 9 columns): the DER Register extract, the re-allocation log, the network model, the dictionary, the
  export manifest; `ac_connection_id`, `nmi`, `device_type`, `model`, `storage_capacity_kwh`, `ac_connection_status`,
  `feeder`, the log's `old_nmi` and `new_nmi`.
- Stops (built): S1 natural, storage summed over device rows (YRB21 6,124.7 against 2,439.7 kWh; all 8 off); S2 one
  value per connection with decommissioned connections kept (5 of 8 off); answer. Every golden total sits at least
  2.2 kWh inside its ten (asserted at 0.7).
- Lazy delta: S1 wrong on 8 of 8.
- Realism: a register extract that flattens AC-connection fields onto device rows is the normal shape of a device-grain
  export.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta (built) |
|---|---|---|---|
| HA1 device grain | inverters and batteries are separate devices of one AC connection | Ask A (sites counted by rows), Ask B | Ask A second figure on 2 of 8 feeders on its own; Ask B all 8 (S1) |
| HA2 decommissioned devices | replaced and removed systems keep their records | Ask A, Ask B | Ask B 5 of 8 feeders |
| HA3 NMI with checksum | the newer installer portal | Ask A | all 16 figures (S1) |
| HA4 temporary NMIs | builder-installed systems | Ask A (primary), Ask B | Ask A all 16 (S2); Ask B 3 feeders |

**The cracker sheet.** The cracker filed YRB24 at 1.9 MW, ran the hygiene battery (keys unique after normalising,
exact duplicates, every join matched or explained, no fan-out, counts that tie to the register) and executed every
filed rule. Every ask row misses:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 16 counts | NMIs normalised, active AC connections counted once per NMI, matched to connected NMIs, by the extract's feeder | builder systems registered under temporary NMIs count once on each side | miss |
| Ask B, 8 storage totals | active battery devices, decommissioned removed, storage summed by feeder | each modular system's capacity counted once per module | miss |
| Chart (recommendation block, not an ask) | the bars from the forecast | carried by the main call, scored with it | outside |

Mirror leakage: 8 per cent of the ask weight (the mirror files YRB22 and answers both asks as the cracker does; no ask
figure couples to the call).

**Pair arithmetic.** Planning weights 36 recommendation (the feeder, its excess, the runner-up, the gap, the two
campaigns' systems), 9 instruction following (the files, the chart's named parts), 55 asks over 24 figures. The cracker
keeps about 8 per cent of the ask weight: C = 36 + 9 + 4.4 = 49.4. The mirror (R0) keeps r of about 4 (the runner-up
named on R0 is YRB25, not graded right; the files and chart structure) and the same 4.4: S = 4 + 9 + 4.4 = 17.4.

Pair ceiling: 33.4

If the rubric grades the two campaign figures as asks, the cracker keeps them and the mirror does not: C rises by
about 5 and S is unchanged, a pair of about 36. Recomputed from the generated rubric when it exists.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| NPP-114 2.1 to 2.4 | 1, the distributor's planning procedure | micro EG, connected capacity, program systems, the design point | who a program can reach, a rate per anything |
| NPP-114 3.1 to 3.2 | 1 | the base date, the network model, the trend | a pool, a hazard |
| NPP-114 4.1 to 4.3 | 1 | programs add the systems the records of past programs indicate, at the feeder's average capacity, by the design point | how to carry a past program to a new suburb |
| NPP-114 5.1, 6.1, 7.1 | 1 | the hosting capacity case, the selection rule, rounding | any feeder's figure |
| The hosting capacity assessment | 2, the consultant's study the procedure names | each feeder's hosting capacity, spring 2029 case | connected capacity, headroom |
| The council's 2027 letter | 3, a counterparty's notice | the two 2027 suburbs, sign-up dates, letterbox drops | a forecast |

## Prompt

`prompt.txt`, drafted at stage 2 and gated by `voice-check.py` (in `precut.py`): the call with its unit and the
forcing facts (the FY2027-28 program, NPP-114, the council's two spring 2027 bulk-buys), the workbook's figures, the two
asks per feeder with "how many" (zero a grammatical answer, H23), the chart's named parts and the rounding once at the
close.

## Build record

Stage 3, built 2026-10-12 by `python3 task136/generator/build.py` (one command: pack, goldens, `metadata.json`,
`generator/figures.json`, `checks.py`, `verify.py`, a second full build compared byte for byte, `target.zip`).

- **The call.** YRB24, 1.892 MW above its spring 2029 hosting capacity (forecast 6.112 MW against 4.22 MW); runner-up
  YRB22 at 1.508 MW; gap 0.384 MW. Bindarra Waters 241.6 systems (5,275 owner-occupied houses expected without PV at
  the opening, at 4.580 per cent), Wattleview 30.6 (668). Graded as 1.9, 1.5, 0.4, 240 and 30; every one at least a third of
  a bin from an edge (nearest: the gap, 0.034 MW from 0.35, and Bindarra Waters, 3.4 systems from 245; asserted at
  0.07 of a bin).
- **Default path.** YRB22 at 1.508 MW, runner-up YRB25 at 1.238, gap 0.270; Bindarra Waters 90.4 and Wattleview 47.8
  systems (filed as 90 and 50); YRB24 5th at 0.796 MW.
- **Stage 4, the judge's FIX_NOW.** DETERMINISTIC, with YRB22's connected capacity in the write-up (13,683 kW) not
  reproducing: 40 legacy application numbers had been issued twice, so the lookup gave both applications the later
  equipment row while a file-order or panel pairing gave 13,690 and a summed join 13,766 (YRB22 at 1.6 MW, gap 0.3).
  Closed in the data: each legacy number is issued once (SF23, every join the same inverter); the dictionary defines
  the register's status values, closing the judge's withdrawn-as-PV variant that rounds Bindarra Waters to 250 (SF24);
  the stage 4 reader's per-letterbox reading is priced in SF16; the assessment's 2026 case now follows each feeder's
  minimum demand (the reader's realism tell). Step 1 of the write-up drops YRB22's figure, which no ask or component
  owes. Files changed under `target/`: `eg_connection_applications_20260901.csv` and `legacy_inverter_equipment.csv`
  (40 legacy numbers each, that column only), `data_dictionary.xlsx` (the status definition) and
  `yarrabin_hosting_capacity_assessment_2026.pdf` (the 2026 columns; the 2029 columns, route lengths and customers
  unchanged). Every graded figure is unchanged (`freeze.py check --mode determinism` PASS with the twelve step keys
  named in `## Tried and rejected` allowed). The `## Ladder` section keeps its stage 3 figures, frozen during the
  repair; after the fix the base excesses read YRB22 1.508, YRB21 1.110, YRB27 0.813, YRB23 0.438 and YRB26 -0.657
  (the rest unchanged), every rung names the same feeder with YRB24 in the same place, the margins are 1.22 below R3
  and 1.25 on R3, and YRB22 leads YRB24 on R1 by 0.351 MW (dominance 2.1), as `checks.py` prints.
- **Asks.** Ask A (connected not shown; active sites with no connected system): YRB21 12 and 11, YRB22 8 and 12, YRB23
  11 and 10, YRB24 2 and 8, YRB25 6 and 5, YRB26 14 and 4, YRB27 14 and 9, YRB28 12 and 4. Ask B (kWh): 2,439.7,
  1,767.9, 1,800.8, 392.5, 900.5, 1,588.4, 1,738.1, 1,311.2, graded to the nearest ten.
- **Gates.** `checks.py` 284 assertions; `verify.py` 123 checks from the bundle alone (csv, openpyxl, pypdf, no
  generator import); two builds byte-identical (15 target files, 2 goldens, `metadata.json`, `figures.json`,
  `target.zip`); `figures_check.py` PASS (50 figures); input gates 15 files, 3 formats (csv, xlsx, pdf), largest
  `merindah_rates_roll_2026-27.csv` at 48,876 rows, two distractors (`feeder_peak_demand_forecast_2027-31.xlsx`,
  `home_battery_rebate_approvals_fy2025-26.csv`, deletion asserted); container audit clean in the fiction's band
  (2018-06-01 to 2026-10-12) for the pack, and for the goldens to 2026-10-31 (the workbook carries the analyst's own
  13 and 16 October 2026 stamps, after the request); `target.zip` equal to `target/` by content; `guard.py surface` 0 promoted pairs (nearest 0.094);
  `guard.py heart` WARN only (`overuse.gate_g` and `repeat.question_form`, answered under Guard); `leak.py --asof
  2026-10-12` REVIEW, no LEAK (the same seven lines after the stage 4 rebuild).
- **leak.py REVIEW lines, each harmless.** (1) The letter's 6,240 contains the golden 240: the Bindarra Waters
  letterbox count, a different quantity, and the default path's denominator, not an answer. (2) The assessment's 4.22
  is YRB24's hosting capacity, an input the golden cites. (3) NPP-114 carries six of seven words of the call (hosting
  capacity augmentation, capital works program): the procedure's own vocabulary; it names no feeder. (4) Stump
  vocabulary in NPP-114, the letter and the assessment (forecast, network, connection, campaign, suburb, method):
  generic domain words; none names the pool, a rate per house or the conjunction. (5) `device_type` in the DER
  extract: the national DER Register's own field (Device Type).
- **Differentiation (abstraction test, read at the build).** task446 v2 carries a screen's yield across years by
  backing the base rate out through the screen's error rates (a Bayes inversion on a moving prevalence); here the
  yield's denominator is the reachable pool, built behind a three-file join, with no inversion and no base rate.
  task86 v2 runs an earlier draw on a shared pool forward member by member; here nothing is drawn down, and the pool
  is counted, not simulated.

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
