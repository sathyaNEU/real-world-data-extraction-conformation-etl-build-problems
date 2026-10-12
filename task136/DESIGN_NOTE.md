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
| Furniture | forum `executive_team` (the executive leadership team locks the FY2027-28 capital works program at its investment review on Tuesday 24 November 2026), forcing event `budget_or_appropriation` (the program funds one accelerated hosting-capacity augmentation), organisation family `utility_or_infrastructure`, role family `research_desk` (the DER forecasting analyst in network planning), context artifact `capacity_report` (the 2026 hosting capacity assessment), calibration `none` (the past campaigns are the history the programme component is estimated from, not an organ), opening `question-first`, question form `which` |
| Spine | `eg_connection_applications_20260901.csv`, the embedded generation connection register: one row per micro EG (rooftop PV) connection application at an NMI, new systems and alterations, 2011 to 31 August 2026; constructed |
| Deliverables | `feeder_upgrade_2029.xlsx` (the call, the forecast by feeder, the two campaigns' installations, the two asks), `yarrabin_pv_vs_hosting_2029.png` (one bar per feeder for its rooftop PV connected at 31 August 2029, its hosting capacity marked) |
| People | drawn with `guard.py names --geo Australia --seed 136 --n 30`, keeping only names with an unused first name and surname: Wanda Thornton (DER forecasting analyst, the requester), Christopher Sheppard (manager, network planning, signs NPP-114), Julie Cochran (sustainability programs officer, Merindah City Council, keeps the bulk-buy log), Bryan Nichols (embedded generation connections lead, the register), Linda Ruiz (GIS analyst, the NMI-to-property cross-reference), Nicole Rocha (customer experience team leader, the case export), Tammy Buchanan (consulting engineer, the hosting capacity assessment); none appears in the prompt |

**Guard.** `guard.py check` on the scratch card: WARN, one finding. `overuse.gate_g` (`method_or_model_selection` in six
of the last twelve builds): it is the honest key, because the decisive step is choosing the basis on which past
campaigns' installations carry to a new suburb, and the seven past campaigns select exactly one basis; the mechanism
differs from every recent carrier (task501's eigenvalue, task134's inflow hazard, task135's asynchronous prices), and
the nearest driver on file is 0.07. The bans run against task125, task127 and task130 (the three builds drawn before
this one by draw key). A first draft blocked on `ban.pattern` (C, task127), then on `test.same_driver` (gap population,
pattern E, against task124's lineage and task500 v2) and `test.same_puzzle_older`; the decisive mechanism is carried
honestly by the G-code (G8, reachability), which no recent build carries. Sweeping the card through gap, pattern and
gate combinations confirmed gap population with pattern none and G8 first is clear under either Gate G key.

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
substation (110/22 kV) supplies eight 22 kV feeders, YRB21 to YRB28, serving about 38,000 premises in Merindah's
western growth corridor, with about 11,000 residential rooftop PV systems connected at 31 August 2026. Merindah City
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
the council's letter on the 2027 campaigns is dated 14 August 2026; the request is made on 12 October 2026; the
executive leadership team locks the program on 24 November 2026.

## Default path

1. Read NPP-114. From the connection register, keep residential applications, take each NMI's latest connected
   configuration (an alteration carries the NMI's whole system after the work), place each NMI on its feeder in the
   network model at 31 August 2026 and sum inverter ratings: the rooftop PV connected on each feeder.
2. Build the base trend as NPP-114 sets it: the yearly increase in connected residential PV over FY2023-24, FY2024-25
   and FY2025-26, less the systems connected through a program in that year, averaged and carried three years to 31
   August 2029.
3. For the two 2027 bulk-buys, take each past campaign's systems installed (the council's log, equal to the register's
   program-coded connections) over its homes letterboxed, average the seven participation rates and apply the average
   to the homes the 2027 letterbox drops will reach (Bindarra Waters 6,240, Wattleview 3,300), each system at the
   feeder's FY2025-26 average inverter rating.
4. Subtract each feeder's hosting capacity from the 2026 assessment and pick the largest excess.

Ends on: YRB22, about 1.5 MW over its hosting capacity at 31 August 2029 (Bindarra Waters adds about 115 systems,
Wattleview about 45).
Golden: YRB24, about 1.9 MW over its hosting capacity (Bindarra Waters adds about 240 systems, Wattleview about 33).

## Stump sentence

A competent solver collapses alterations, builds NPP-114's base trend, carries the past bulk-buys' systems per home
letterboxed onto the 2027 letterbox drops and files YRB22 at about 1.5 MW over hosting capacity (Ends on); the step that
lands it there is transferring each campaign's yield per contacted address instead of per owner-occupied house still
without rooftop PV in its suburb, which leaves YRB24's untouched Bindarra Waters estate with about half its campaign:
the golden is YRB24 at about 1.9 MW.

## Three rules

- **Domain test:** the deciding quantity is each feeder's design-point rooftop PV against its hosting capacity, with a
  bulk-buy's installations forecast from the rooftops that can still take it up (owner-occupied houses with no PV
  yet), which is how a distribution planner forecasts DER on a feeder for an augmentation; with another field's nouns,
  hosting capacity, inverter ratings, rooftop ownership and the embedded generation register have nothing to attach to.
- **Analyst test:** a strong analyst who reads NPP-114, collapses alterations to one system per NMI, places NMIs on the
  network model's feeders and counts each past campaign's installations correctly still carries them per home
  letterboxed (YRB22 at about 1.5 MW); per owner-occupied house, per home without PV, per feeder, as a rate ratio on the
  suburb's own adoption, or as an average count, each leaves Bindarra Waters at a third to two thirds of its campaign
  and the augmentation with YRB22.
- **Layer 1:** an embedded generation register at application grain (alterations carrying the NMI's whole system,
  withdrawn and approved-not-connected applications, rows migrated in 2019 with panel capacity only and the inverter
  in an equipment table), the feeder at application against the network model after a 2023 load transfer from YRB23 to
  YRB28, the council's rates roll keyed by property number joined to NMIs only through the GIS cross-reference
  (dual-occupancy and granny-flat NMIs), the council's program workbook in its own layout, and, on the ask paths, a
  national DER Register extract at device grain and a customer case export with repeat contacts and re-categorised
  cases. Each is something these systems produce; none decides the call.
- **Layer 2:** the shortcut is to carry a past campaign's yield per address it reached (the council's own
  participation rate), or to refine it one step (per owner-occupied house, per address without PV); the expert carries
  it per owner-occupied house still without PV in the suburb when the campaign opens, the only basis on which all seven
  past campaigns agree, and builds that pool for the 2027 suburbs from the rates roll, the cross-reference and the
  register.

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
