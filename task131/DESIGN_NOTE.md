# task131 design note

Architecture 2, re-rooted 2026-10-13 under the 10/10 rules. Architecture 1 (a Swiss consumer co-operative's
card-randomised member offers) shipped 2026-10-10 and failed to stump on the portal; its task type
(crm-loyalty-retention) serves no objective in the client taxonomy and its question read the same with app or
subscription nouns, so the slot is redrawn into a new domain, world, decision and quantity. Its record is kept
at the end of this note.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | Energy Systems & Utilities / tariff-demand-response-evaluation (serves Experiment & Causal in the client taxonomy; the pairing has never been built) |
| Objective | Experiment & Causal Analysis: the call is a causal claim, what each trialled tariff design does to the 2027-28 planning maximum demand, read from a randomised trial |
| Niche | a State-owned regional power corporation running the isolated Murrandi system in inland Western Australia chooses which of three peak-window residential tariff designs, if any, its flat-rate households move onto from 1 July 2027, from a summer 2025-26 trial its load research team randomised household by household |
| Shape | 11 before and after with a control: each design's change in the 2027-28 50% POE maximum demand, the half-hour that maximum falls in, and the design's pre-trial gap against the control households, plus the call, the runner-up, the chart and the asks |
| Decision type / unit | pick one of three designs or none (named option); the graded figures are megawatts of the 50% POE maximum demand |
| Gap / pattern / generators | time (what the trial's evidence covers against the day the decision is scored on), then population; no A to E pattern; G13 decisive (the decision covers every half-hour of the design day, not the window on an average trial day), G7 (the deferred load physically comes back when the price falls), G14 (the response on days as hot as the design day, not the summer's average) |
| Gate G mechanism | method_or_model_selection: every reported figure is correct; the call turns on estimating ex-ante impacts at the design day's weather over the whole day rather than reading the window cut |
| Stump strategy | other: the trial's effect is a signed half-hourly profile whose after-window lobe grows with heat, and the decision is scored on the maximum of the design day's whole curve; no listed family names an ex-ante impact at design conditions on a non-linear planning quantity |
| Decisive rule filed / decoys | the estimand is filed (the forecast's maximum-demand definition and design day, the prompt's population and comparison); no official decoy, no validated decoy, no calibration corpus; the trial's own report is not shipped |
| Context artifact | capacity_report (the corporation's 2026 demand forecast and generation adequacy workbook) |
| Stakeholder | the corporation's pricing and tariffs manager, who advises the Minister for Energy which design, if any, flat-rate households move onto in the 2027-28 tariff schedule (the prompt names no one) |
| Forum / forcing event / org family | minister_or_cabinet / season_or_peak (the default has to be in place before the 2027-28 summer) / utility_or_infrastructure |
| World | Murrandi Regional Power, a State-owned corporation generating, distributing and retailing on the isolated Murrandi system (inland Western Australia, AWST, no daylight saving), AUD; personas drawn en_AU seed 131: Pamela Crawford (pricing and tariffs), Peter Huang (load research), Craig Jackson (system planning), Nathaniel Maxwell (metering services) |
| Deliverables | `tariff_default_advice_2027-28.pdf` (the advice: the call, each design's change in the maximum demand and its half-hour, the pre-trial gaps, a chart of each design's change); `tariff_trial_tables_2025-26.xlsx` (the asks) |
| Guard | WARN only: repeat.gate_g and overuse.gate_g (method_or_model_selection in 5 of the last 12; time, G13 and forecasting would collide with task501's lineage inside the batch, and the mechanism is honestly a method choice on correct figures), repeat.decision (pick_one_of_n after task501: the question picks a tariff design or none). Older same-puzzle and same-driver notes differentiated against task122 and task229 (v2); task124's dispatch lineage differentiated |

**Data-native sentence.** The trial's meters record each household's half-hours on the days the 2025-26 summer
brought, mostly ordinary ones, while the decision is scored on the 2027-28 design day, a 44.6-degree workday;
a house whose thermostat is set up through the peak window banks heat that its air conditioner pulls down the
moment the price falls, every responding house at once, and only on days as hot as the design day does that
pull-down outgrow the cut it repays, so a design's capacity value exists on the design day's whole curve and
nowhere in the trial's average day or inside its window.

**Sources, one line each.**
- The client's two-layer standard (`stumping/references/client/two-layer-task-design.md`): the field's own
  method decides (ex-ante load impacts at planning weather); here it is the design day's every half-hour, never a
  stated score or a window rule.
- The client's measured drivers, held group: a conjunction whose partial application scores worse than none; here
  conditioning on heat alone (the hot-day cut at the old maximum) files B with a larger figure, and the whole curve
  on the average day files A, so neither half climbs toward C.
- task124's dispatch lineage (heat-conditioned analogs, pre-cool and recovery hours, solved by reading peak days'
  own hours): here reading the hot days' hours is half the path and files B; the call is carried by the maximum of
  the whole design-day curve after the pull-down, and nothing is curtailed by the organisation.
- task117 (a forward peak of a summed load moved by re-timed follow-on operations): here a randomised tariff's
  deferred cooling returns at the price step, not a sequencing replay.
- Field practice: ex-ante load impacts reported for 1-in-2 (50% POE) weather, resource adequacy assessed over
  every hour of the worst day, and default time-of-use pilots that measured load increases in the hours after the
  peak period on hot days; the build carries the practice, not any one programme's figures.

## Default path

1. Parse the four monthly NEM12 files (300 records, kWh per half-hour, read as average kW times two) and keep the
   trial's workdays, the weekdays outside public holidays from 1 December 2025 to 27 February 2026, when the peak
   prices applied.
2. Join each meter's NMI to the trial register to give each household its assigned design, as assigned (the
   trial plan's intention to treat, households that returned to the flat rate kept in their arm).
3. For each design, take the mean over the trial workdays of the design households' mean demand less the control
   households' mean demand across the design's peak window: B cuts most per household, then A, then C.
4. Multiply each design's cut by the forecast's 2027-28 flat-rate residential customers and take it off the 50%
   POE maximum demand on the forecast's design day.
5. File the design that takes the most off.

Ends on: Design B, lowering the 2027-28 50% POE maximum demand by about 16 MW.

Golden: Design C, lowering it by about 11 MW (its maximum the half-hour from 8 p.m., at the design day's flat-rate
demand for that half-hour); A would raise it by about 5 MW (its maximum moves to the half-hour from 9 p.m.) and B
by about 18 MW (the half-hour from 8 p.m.). The figures are the paper ladder's; the build replaces them with the
generator's.

## Stump sentence

A competent solver takes each design's treatment-minus-control drop in household demand over its peak window
across the trial's workdays, scales it to the 2027-28 flat-rate residential customers and files Design B as
lowering the 50% POE maximum demand by about 16 MW (the `Ends on:` figure); the step that lands it there is reading
a design's effect as its cut inside the window on an average trial day, when the cooling put off past the peak
price comes back as one pull-down when the price falls and on the design day's heat outgrows the cut, so B's
maximum moves to the half-hour from 8 p.m. and rises, A's to the half-hour from 9 p.m., and only the stepped design
C lowers it.

## Three rules

Task type: energy-systems-utilities / tariff-demand-response-evaluation, which serves Experiment & Causal in the
client taxonomy; the call is the causal effect of each trialled tariff design on the planning maximum demand, read
from a randomised trial.

Domain test: the deciding quantity is each design's ex-ante load impact on the 2027-28 50% POE maximum demand, the
design day's highest half-hour once the design's half-hourly household response at the design day's heat is added
to the forecast profile, estimated from a randomised tariff trial, which is the core analysis of tariff and
demand-response evaluation.

Swap: "which of three appointment-pricing designs should the clinic move patients onto, judged by how far it
lowers next winter's busiest-hour arrivals" has no design day with a temperature trace, no cooling banked in a
building's fabric that returns as one pull-down when the price falls and grows with the day's heat, and no
half-hourly maximum demand against firm generation; the physics that moves the answer is gone, so the task stops
making sense.

Layer 1: NEM12 interval files as the meter data agent sends them (multi-record CSV, A, S, E, F and V quality, 400
records splitting a day by quality, a few 15-minute meters, days re-sent in a later month's file with actual reads
replacing estimates); the trial register keyed by customer account while meter data is keyed by NMI, with
move-outs during the trial; the gazetted prices GST-inclusive against the trial plan's GST-exclusive table;
interval-ending meter timestamps against tariff windows in clock time and a forecast labelled by trading interval;
Bureau-format weather with quality flags and a gap filled from a second station; public holidays charged off-peak.
Each is what the corporation's own systems produce; none is placed to be caught and none carries the call.

Layer 2: field_method: each design's intention-to-treat effect is estimated for every half-hour at the design
day's weather and added to the whole design-day profile, where the maximum is taken, rather than read as the cut
inside the peak window on an average trial day.

Decisive step: ex-ante load impacts at the 50% POE design day's weather, half-hour by half-hour, applied to the
forecast's design-day profile with the maximum taken over the whole day; on days as hot as the design day the
pull-down after the window outgrows the cut, so B's and A's maxima leave their windows and rise and only C's falls.

Not semantics: reading every field, code, unit and definition correctly (kWh per half-hour as average kW times two,
interval-ending times, assignment as the arm, the maximum demand as the highest half-hour on the design day) still
leaves the easy route on Design B, because no field says where a design's effect lands outside its window or how it
changes with heat.

Not rule application: no filed rule computes a design's effect on the design day; the forecast defines the maximum
demand and the trial plan defines the arms and the comparison, and executing both still files B; conditioning the
half-hourly effect on the design day's heat and taking the maximum of the whole curve is performed by no filed
procedure.

Analyst test: a strong analyst who parses every interval read, keeps the trial workdays, takes the
intention-to-treat difference against the control arm and scales it to the forecast's flat-rate customers subtracts
each design's peak-window cut from the 50% POE maximum demand and files Design B, about 16 MW lower (the `Ends on:`
figure), or with the average trial day's whole half-hourly profile files Design A; neither is what B or A does to
the design day's highest half-hour, which both raise.

Estimand: the change in the 2027-28 summer 50% POE maximum demand (the highest half-hourly system demand on the
forecast's 50% POE design day, `demand_forecast_2026.xlsx`, methodology sheet) if every flat-rate residential
customer were moved onto the design from 1 July 2027, free to return to the flat rate as trial households were (the
prompt and the trial plan, `trial_plan_summer_2025-26.pdf`); population, outcome, window, unit and comparison are
filed, the estimation is open.

No decoy: nothing is planted to be caught; the trial's own report is not shipped; no memo, briefing, staff draft
or stakeholder figure argues for B or A; the forecast does not rank the designs and no file states a design's
effect.

No certified replay: no certified or published figure reproduces only under the right method; the method is not
hidden behind controls; the trial plan names the arms, the dates and the intention-to-treat comparison and nothing
about how a design's effect carries to the design day.

Lesson: a peak-window tariff's capacity value is what it does to the maximum of the design day's demand curve, so
its response has to be estimated half-hour by half-hour at the design day's weather: the cooling households put off
returns as one pull-down when the price falls, grows with heat faster than the cut it repays, and can set a new,
higher maximum after the window; no build on file teaches an ex-ante tariff impact or a treatment effect read on the
maximum of a curve.

**Abstraction test.** Without the nouns: a randomised treatment's effect is a signed profile over a day's
intervals whose lobe after the treated window grows with the day's stress faster than the cut inside it, and the
decision is scored on the maximum of a target-day curve plus that effect at the target's stress. The nearest
drivers (task83 at 0.07, conditioning a holdout's effect on prior treatment; task258 at 0.05, units moved across a
threshold; task124 v3 at 0.05, an unintervened level recovered from analogs) share none of the latent structure,
default path or correction.

**Same-puzzle test.** Gap time, decisive G13, decision pick_one_of_n repeats task122 (older): task122 credits
outcomes logged after a session closed back to the exposures that produced them; here the outcome is a planning
maximum moved by a tariff's after-window pull-down. Gap time, G13 and method_or_model_selection repeats task229's
architecture 2 (a checked-state rate under reset checks); here a causal tariff effect at design conditions.

## Tried and rejected

- Store-randomised geo test with cross-store shopping as the interference: rejected at the draw, because the redemption file would show offer redemptions at control stores, a symptom the hygiene battery surfaces, and a store-level counterfactual needs a third group the pack would have to ship.
- Household-randomised offer delivered to the main card only: rejected at the draw, because an analyst who analyses at the randomisation unit (the membership) lands the answer by default.
- Per-membership planning basis in the standard: rejected at the draw, because a per-membership quantity sends the solver to group cards by membership, where the mixed arms are in plain view; the co-op budgets rewards per active card, which is the realistic basis and keeps the natural read at the card.
- Signature population + pattern D + method selection: blocked by the guard (spent in eight builds); the honest label is no A to E pattern with G10 decisive.
- Equal per-row forcing of a group's run-rate margin shift: put margin above sales on small baskets; the shift is now spread across cards and rows in proportion to their spend.
- Region-level forcing with the moved members sharing their new region's target: the January-register misreading then moved the St. Gallen cells only by sampling noise; forcing per area makes the device bite by construction.
- Plan total placed by stepping one region: grew St. Gallen 14 per cent against about 1 per cent elsewhere; the placement now walks totals outward and spreads the steps across regions.
- Architecture 1 (a Swiss co-operative's card-randomised member offers, household interference): shipped
  2026-10-10, left off the portal's approved list (the household read was solved), and its task type
  (crm-loyalty-retention) serves no objective in the client taxonomy; with app or subscription nouns the question
  read the same. Re-rooted 2026-10-13 into tariff evaluation.
- Draw options weighed and dropped on 2026-10-13 before the card: a clinical dose-selection trial read under its
  treatment-policy estimand (one known correction, retrieved-dropout or reference-based imputation, that strong
  solvers reach); a WASH trial's reported diarrhoea against a stool-PCR subsample (the reasoning reads the same for
  any self-reported outcome); hot-spot policing displacement (interference, the spent architecture-1 insight in new
  nouns); a stimulus-sampling power analysis (the decision is a design, not a causal claim).
- Shape 07 and budget_or_appropriation: blocked by the guard against task501 and task449; shape 11 and
  season_or_peak drawn instead. Time, G13 and forecasting: blocked inside the batch against task501's lineage;
  method_or_model_selection is the honest mechanism.

## Architecture 1 record (spent 2026-10-13)

Replaces task130 (failed on the portal 2026-10-10, both top models filed the golden). Drawn bespoke
under the template caps: no calibration corpus, no licensed wrong basis, no certified record to
reproduce.

### DRAW

| Axis | Value |
|---|---|
| Domain / subdomain | Marketing & Consumer Research / crm-loyalty-retention |
| Objective | Experiment & Causal Analysis |
| Niche | a regional consumer co-operative choosing which of four member-card reward offers its 2027 programme runs on every card, from a summer test its offer engine randomised card by card |
| Shape | 07 grid of cells: six regions by four offers, plus the four offers' 2027 programme values |
| Decision type / unit | pick one of four offers (named option), plus its 2027 programme value in CHF thousands |
| Gap / pattern / generators | population (the randomisation unit is not the economic unit), no A to E pattern; G10 cross-dimensional duplication (moved spend counted as gain on the offer card and as loss on its sibling), G4 attribution at transition |
| Gate G mechanism | method_or_model_selection (the unit of analysis an interference-affected test has to be read at) |
| Stump strategy | causal_design; decisive rule filed (the programme standard states the quantity, incremental net margin per active card-week under the offer against without it, and the prompt sets the full rollout); no official decoy; no validated decoy |
| Calibration form | none, because the strategy needs none |
| Context artifact | register (the offer engine's allocation register) |
| Stakeholder | head of the member programme, who puts the 2027 offer and its budget line to the executive board (Geschaeftsleitung) |
| Forum / forcing event / org family | executive_team / budget_or_appropriation (2027 budget round) / cooperative_or_member_body |
| World | Talwerk Genossenschaft, a consumer co-operative with 42 shops in six regions of eastern Switzerland, CHF; personas drawn de_CH seed 131 |
| Deliverables | `programme_offer_2027.docx` (commits), `offer_grid_2027.png` (reads at a glance) |
| Guard | PASS, no WARN; nearest driver 0.10 (task52) |

**Data-native sentence.** A Talwerk membership is a household that holds a main card and up to
three additional cards and buys from one household budget, while the offer engine allocates offers
card by card because rewards are credited to the card that is used; so the test's natural unit is the
card and its economic unit is the membership, and the inflation of every card-level lift by baskets
that only moved between cards of one membership is a property of how a co-operative's household
memberships shop, not of the test's arithmetic.

### Gate G

- **Litmus.** No reported number or stakeholder conclusion is overturned. The pack ships no test
  readout, no dashboard and no ranking of the offers; every figure in it is a correct record of
  card activity. The difficulty is choosing the unit at which a card-randomised test has to be read
  when cards of one membership share a budget. Answer: no.
- `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`
- **Primary mechanism:** method_or_model_selection.
- **Deletion test.** Delete every wrong number and every claim: nothing in the pack is wrong and no
  voice argues an offer, so the pack after deletion is the pack, and it is still hard.
- **Clean-data test.** The main call's rows carry no planted defect; the card-week facts are complete
  and correct. Asserted in the generator: the main path reads no device row.
- **Lens-swap test.** The naive reading and the answer are not one population under two lenses: the
  naive reading averages every allocated card, the answer averages only the cards of memberships whose
  cards all drew the same arm (about 64 per cent of memberships, 42 per cent of cards), and its
  figures are not a re-labelling of the naive figures.

### Stump sentence

A competent solver takes each card's change in net margin after reward cost from the spring baseline
weeks to the six run-rate weeks, differences each offer against the control cards as randomised, and
commits to the personalised weekly coupons (D); the step that lands it there is reading each card as an
independent shopper, when the cards of one membership share a household's baskets and a card carrying
an offer pulls them off its sibling cards, so the lift on the card is partly spend that only moved;
measured on memberships whose cards all drew the same arm, the fresh-produce bonus (A) leads.

### The decisive move, and why it survives the opponent

1. **Written in no sentence.** The standard defines the quantity (the change in net margin from the
   baseline to the run-rate weeks under the offer against the same change without it, per active
   card-week, every allocated card counting as active) and the windows; the full rollout is set only by
   the prompt (the offer goes on every member card); nothing says that cards of a membership
   share baskets, that the allocation mixes arms inside memberships, or that same-arm memberships are
   the clean comparison. The programme terms say a membership may carry additional cards, which is
   world furniture, not the move.
2. **No sweepable corpus nominates it.** There is no corpus.
3. **No arithmetic symptom.** Card-level totals tie to the week totals; the allocation is balanced
   20/20/20/20/20 by card and by region; pre-period balance holds; the control arm's run-rate decline
   sits inside the summer seasonal decline every arm shares.
4. **Not a per-row predicate.** It needs a group (membership), a property of the group (all cards in
   one arm), and a re-estimate on that subset; no column marks a pure membership.
5. **Enumeration is arithmetic.** The subset is defined by a group property computed over the
   allocation register joined through the card master.
6. **No cutover date.** The test start is dated, and the event study at the card level gives the
   wrong answer, so the date sits on the decoy's side.
7. **Survives the deletion** (above).

### Ladder (targets; realised values in the build record)

Chain-wide, per active card-week, CHF, run-rate unless stated.

| Rung | Construction | Winner | Killed by |
|---|---|---|---|
| 0 | card-level gross sales lift over the whole test | C monthly target voucher | the standard scores net margin after reward cost |
| 1 | card-level net margin lift over all twelve test weeks | B triple points | the standard scores the run-rate weeks (13 Jul to 23 Aug), and B's lift fades |
| 2 | card-level net margin lift, run-rate weeks (the filed basis, read at the randomisation unit) | **D weekly coupons, the stump** | a card's lift includes baskets moved off its membership's other cards, which nets to zero at a full rollout |
| 3 | same, on memberships whose cards all drew one arm | **A fresh-produce bonus** | answer |

Realised (CHF per active card-week, from the shipped bundle, asserted in `checks.py` and recomputed by
`verify.py`):

| Rung | A | B | C | D | Winner, lead |
|---|---|---|---|---|---|
| 0 gross sales, whole test | 9.14 | 10.90 | 13.29 | 10.43 | C, 1.22x (A 4th) |
| 1 net, whole test | 0.67 | 1.70 | 1.30 | 0.77 | B, 1.31x (A 4th) |
| 2 net, run rate, card level | 0.54 | 0.35 | 0.56 | 0.71 | D, 1.27x (A 3rd) |
| 3 net, run rate, same-cell memberships | **0.49** | 0.27 | 0.16 | 0.34 | **A, 1.45x over D** |

The partial correction (membership totals with mixed memberships kept, each in its main card's cell)
lands on A too but files every figure wrong (A 0.48); it is the decisive insight half applied, and the
graded figures separate it. Estimators on same-cell memberships converge at the stated rounding: card
weighted, membership weighted and single-card memberships only (C1, asserted on all four offers, the
gap and all 24 cells).

### Determinism: the 22 axes

| # | Axis | Disposition |
|---|---|---|
| 1 | Population | every allocated card; the register holds every card of every membership with a purchase in the baseline weeks (C1, asserted: no membership has an unallocated card) |
| 2 | Unit of account | the card for the quantity (per active card-week, filed), the membership for the comparison (the move); single-card-only, all-same-arm and size-reweighted estimators converge at the stated rounding (C1, asserted) |
| 3 | Attribution window | baseline W15 to W22 and run-rate W29 to W34 filed in the standard (pin) |
| 4 | As-of dating | the membership's home branch and card roles are static over the extract; region by the 1 July 2026 network (pin in the standard), only the grid reads it |
| 5 | Version basis | the branch register is January's; the network notice carries the 1 July changes (grid device, off the main path) |
| 6 | Divisor | active card-weeks, every week counted, weeks without a purchase as zero (pin in the standard and the field notes) |
| 7 | Weighting | pooled over cards (pin); card-weighted and membership-weighted per-card means converge (C1, asserted) |
| 8 | Window length | six run-rate weeks, eight baseline weeks (pin) |
| 9 | Boundary inclusivity | ISO weeks Monday to Sunday, both ends inclusive (pin in the field notes) |
| 10 | Rounding path | round once at the end; per card-week to two decimals, 2027 values to CHF thousands; every graded figure mid-bin (asserted distance to the bin edge) |
| 11 | Tie-break | no tie within 0.05 on any graded comparison (asserted) |
| 12 | Maturity and censoring | none: the windows are closed and the facts final at the extract (field notes) |
| 13 | Order of operations | net margin per card-week then averaged; averaging then netting gives the same figure (linear, C1) |
| 14 | Row order | irrelevant (sums) |
| 15 | Duplicate resolution | one row per card and week (asserted unique key) |
| 16 | Identity normalisation | card numbers are 13-digit strings with a leading zero in a minority; read as strings (field notes); integer reads keep the key unique (C1) |
| 17 | Netting against gross | net margin = gross margin minus reward cost (pin) |
| 18 | Dimensional units | CHF throughout; points converted at CHF 0.01 already in reward cost (field notes) |
| 19 | Code semantics | offer codes K, A, B, C, D in the register, described in the catalogue |
| 20 | Integerisation | none |
| 21 | Scope of a clause | the standard's 2027 value clause governs every offer, not only the pick |
| 22 | Forward window contents | 2027 value = run-rate per active card-week x 52 x planned active cards (pin in the standard; planned cards from the 2027 plan) |

Estimator forks the judge may raise, each closed by C1 convergence asserted in the generator: (a) single-card memberships only, (b) every same-arm membership pooled, (c) same-arm memberships reweighted to the population's card-size mix, (d) per-card means weighted by card against by membership.

### Ask sheet and ledger

**Main call row population.** Card-week rows of cards in memberships whose cards share one arm,
weeks W15 to W22 and W29 to W34, columns gross_margin and reward_cost; the allocation register; the
card master's membership link; the standard; the 2027 plan's total. Device rows inside it: zero
(asserted).

**Ask 1, the grid (24 figures).** Run-rate incremental net margin per active card-week for every
region by offer, CHF to two decimals. Construction layer: the membership-level read cut by region.
Devices, both off the main path (the main call reads no region):
- D2 vintage: three branches moved region on 1 July 2026; the branch register is the January edition, the network notice carries the move.
- D7 chain: two branches closed on 30 June 2026; memberships still carry the closed branch as home branch, and the notice names each successor.
Use: the board sequences the 2027 regional rollout and the regional managers' targets off the grid.

**Ask 2, the four 2027 programme values** (CHF thousands), the call's own figure for every
candidate, plus the gap between the pick and the runner-up per card-week. Decision furniture.

**Chart.** Heatmap of the 24 cells, rows regions, columns offers, the chosen offer outlined, the
runner-up labelled, chain-wide values in a header row, title stating the call.

**Pair arithmetic.** Responses that miss the decisive move file every grid cell wrong (the card-level
read moves every cell) and three of four 2027 values wrong; they keep instruction following and the
chart's structural parts. A response that lands the call loses the grid cells in the regions the two
devices touch (four of six regions, 16 of 24 cells) unless it also handles both devices.

### Build record (stage 3)

- Pack: 14 files, 8 formats, spine `card_week_sales_2026w15_w34.parquet` 611,400 rows; 37,298 cards in
  24,000 memberships; two consecutive builds byte-identical (zip entry times, xlsx core and app
  properties, PDF dates, document id and checksum pinned in `postprocess.py`).
- Golden: A 0.49, D 0.34, B 0.27, C 0.16 per active card-week; 2027 values CHF 972, 672, 528, 322
  thousand on 37,920 planned active cards; gap 0.15; 24 cells by 1 July 2026 region.
- Regional targets are forced per area (core region, the Rorschach group that moved to St. Gallen
  Stadt, the Degersheim group that moved to Appenzellerland), so the 2027 cells are true mixtures and
  both network devices move every cell of the four regions they touch (asserted).
- `checks.py` 149 assertions green; `verify.py` (no generator code) reproduces every figure and the
  memo's tables; surface screen 0 promoted (nearest task109, 0.096); heart PASS.
- `leak.py` REVIEW, no LEAK (the catalogue renamed from `st26_test_catalogue.json` after sweep 1 read
  `test_` as author vocabulary). The two REVIEW lines: `MP-3_measuring_offers_rev3.pdf` shares
  standard, margin, membership, reward, engine and run-rate with the stump paragraph because it is the
  standard that defines the quantity; it never says the cards of a membership share baskets or that a
  comparison should be made by membership. `crm_extract_field_notes.md` shares the world's nouns
  (membership, register, engine) and states one fact, that a membership has one main card and up to
  three additional cards, which is world furniture the card master shows anyway. Both harmless.
- Containers: no writer signature or out-of-band stamp in target/ or golden/ (H1 audit clean).

### Determinism check (stage 5)

Pass 1 (`determinism_check_report.md`): DETERMINISTIC, FIX_NOW; every graded figure reproduced; Gate G
statistical_rigor / analytical_non_defect, flags as filed. Fixed in the generator in one cycle: the
design note's description of MP-3 section 4 corrected to what ships (the full rollout is set by the
prompt); the prompt now rounds programme values to the nearest thousand; docx containers read as Word
with real counts (the zip normaliser had stamped every container as Excel); the standard and both
docx files set to A4. The judge's realism note (regional control means implausibly tight against
their standard errors) answered in the same cycle: the regional summer declines now spread from
-1.86 to -2.14, the moved areas sharing the decline of the region they joined, which keeps the pooled
estimators converging; the regional targets were re-placed for bin clearance, so the graded figures
moved (B 0.27, values CHF 972, 672, 528 and 322 thousand). Residual, recorded rather than fixed: the
A over D gap is about one standard error, and the same-cell subsets agree to the third decimal by
construction; a sharper test would need a rebuild on more cards.
