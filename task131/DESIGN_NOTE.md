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
| Gap / pattern / generators | time (what the trial's evidence covers against the day the decision is scored on), then population; no A to E pattern; G14 decisive (the response on days as hot as the design day, not the summer's average: the final flip, A to C), G13 (the decision covers every half-hour of the design day, not the window: B to A), G7 (the deferred load physically comes back when the price falls) |
| Gate G mechanism | forecasting: every reported figure is correct and the trial's average workday is read correctly; the decision turns on carrying the trial's response to the 2027-28 design day, which the trial's hottest workdays pin |
| Stump strategy | other: the trial's effect is a signed half-hourly profile whose after-window lobe grows with heat, and the decision is scored on the maximum of the design day's whole curve; no listed family names an ex-ante impact at design conditions on a non-linear planning quantity |
| Decisive rule filed / decoys | the estimand is filed (the forecast's maximum-demand definition and design day, the prompt's population and comparison); no official decoy, no validated decoy, no calibration corpus; the trial's own report is not shipped |
| Context artifact | capacity_report (the corporation's 2026 demand forecast and generation adequacy workbook) |
| Stakeholder | the corporation's pricing and tariffs manager, who advises the Minister for Energy which design, if any, flat-rate households move onto in the 2027-28 tariff schedule (the prompt names no one) |
| Forum / forcing event / org family | minister_or_cabinet / season_or_peak (the default has to be in place before the 2027-28 summer) / utility_or_infrastructure |
| World | Murrandi Regional Power, a State-owned corporation generating, distributing and retailing on the isolated Murrandi system (inland Western Australia, AWST, no daylight saving), AUD; personas drawn en_AU seed 131: Pamela Crawford (pricing and tariffs), Peter Huang (load research), Craig Jackson (system planning), Nathaniel Maxwell (metering services) |
| Deliverables | `tariff_default_advice_2027-28.pdf` (the advice: the call, each design's change in the maximum demand and its half-hour, the pre-trial gaps, a chart of each design's change); `tariff_trial_tables_2025-26.xlsx` (the asks) |
| Guard | WARN only: repeat.decision (pick_one_of_n after task501: the question picks a tariff design or none). Older same-puzzle and same-driver notes differentiated against task183 (time, G14, forecasting); differentiation also filed for task122, task124, task130, task134, task136 and task229. `guard.py surface` promotes two pairs on card axes and sector vocabulary, both different drivers (see Build record) |

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

Ends on: Design B, lowering the 2027-28 50% POE maximum demand by about 15 MW.

Golden: Design C, lowering it by 11 MW (its maximum the half-hour from 8 p.m., at the design day's Home Plan
demand for that half-hour less a hundredth of a kilowatt a household); A would raise it by 5 MW (its maximum moves
to the half-hour from 9 p.m.) and B by 20 MW (the half-hour from 8 p.m.).

## Stump sentence

A competent solver takes each design's treatment-minus-control drop in household demand over its peak window
across the trial's workdays, scales it to the 2027-28 flat-rate residential customers and files Design B as
lowering the 50% POE maximum demand by about 15 MW (the `Ends on:` figure); the step that lands it there is reading
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
records splitting a day by quality, 15-minute meters at the premises households moved to within Murrandi, days
re-sent in a later month's file with actual reads replacing estimates); the trial register keyed by customer account while meter data is keyed by NMI, with
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
each design's peak-window cut from the 50% POE maximum demand and files Design B, about 15 MW lower (the `Ends on:`
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

**Same-puzzle test.** Gap time, decisive G14, decision pick_one_of_n and Gate G forecasting repeat task183
(older): task183 carries each part's own failure history into a feeder's forward event count; here a randomised
tariff's half-hourly response on the hottest workdays is added to the design-day curve, where the pull-down after
the window sets a new maximum. G13 decisive was weighed first and dropped: it repeats task122's and task130's
decisive code (task130 numbered next to this slot), and time, G13 and forecasting repeats task501's lineage inside
the batch.

## Readability screen

Rungs in ladder order; the six tests of `stumping` 2.1 per rung, verdict last.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 1 population: the assigned arm and the forecast's flat-rate count (figures only) | the trial plan's comparison and the forecast's customer row name them | register arm column | intention to treat is a default | none | none | a product | readable |
| 2 heat: the response on days as hot as the design day, read at the forecast's maximum half-hour (files B, larger) | the forecast names the design day's weather | weather joins by date | building the analog is a reflex | none | none | a subtraction at one half-hour | readable |
| 3 whole curve: every half-hour's response on the average trial workday added to the design-day profile (files A) | the maximum-demand definition sends the solver to the design day's half-hours | none | taking the definition's maximum is a reading | none | none | a maximum over 48 half-hours | readable |
| 4 (decisive) the half-hourly response at the design day's heat over the whole design-day curve (files C) | no sentence says a design's response lands outside its window or changes with heat; the definition names the outcome only | no column marks the after-window half-hours or the hot days; the heat lives in a separate weather file | each reflex alone files B (heat at the old maximum) or A (the average day's whole curve); only their conjunction moves the maximum | no control or corpus scores the designs | keys, duplicates, joins and fan-out see nothing | a maximum over half-hours of a heat-conditioned profile, non-linear in the rows | silent |

The conjunction is the held signature (`client/measured-drivers.md`): applying either half alone lands further
from C than the default does on the graded figures (B's change moves from 15 to 24 MW on heat alone).

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | every flat-rate residential customer | the forecast's 2027-28 Home Plan (flat rate) customers, 41,860 | all residential customers (44,800); the trial's eligible pool | C (A and B figures move) | the prompt's "flat-rate" and the forecast's customer table, whose Daytime Saver row is not flat-rate |
| SF2 | move onto a design from 1 July 2027 | assignment with the right to return, the trial's assigned-arm difference | the effect on households that stayed on the design | C (A and B figures move) | the trial plan: households could return to the Home Plan at any time, as they would under a default; the prompt asks what moving them does |
| SF3 | 2027-28 summer maximum demand at 50% probability of exceedance | the highest half-hourly sent-out demand on the forecast's 50% POE design day (methodology sheet, design-day sheet) | the 10% POE day; the 2025-26 actual peak; the single MD figure less a cut | C | the forecast's methodology sentence and the prompt's "50%" |
| SF4 | how far it lowers | MD under the Home Plan less MD under the design, signed | an absolute change | same call | the prompt's "lowers"; a rise is reported as a negative lowering, stated in the advice |
| SF5 | each design's change to that maximum demand | the same signed quantity in MW | the MD level under each design | same call | the prompt's "change" |
| SF6 | the three peak designs we trialled last summer | A (3 to 9 p.m.), B (4 to 8 p.m.), C (stepped: shoulders 2 to 4 and 8 to 10 p.m., peak 4 to 8 p.m.), 1 December 2025 to 28 February 2026 | none | same call | the trial plan's design table and dates |
| SF7 | household demand in the trial | net of the meter's import, controlled-load and export channels | general supply import only | same call and same figures | asserted: after 6 p.m. the export channel reads zero and the controlled-load circuit is off, so every half-hour that sets a maximum is identical |
| SF8 | half-hour labels | interval n of a NEM12 day and trading interval n of the forecast both cover (n-1)/2 to n/2 hours after midnight AWST | interval-ending labels read as starting times | same call | the meter data notes and the forecast's notes state the numbering; asserted that a one-interval shift is the only error it can make and it moves every curve together |
| SF9 | kWh per half-hour against MW | average kW is kWh per half-hour times two; MW is kW times customers over 1,000 | kWh read as kW | every figure moves (A 8.2 and C 7.6 MW lower, B 4.7 MW higher) | the meter data notes give the unit and interval length, the forecast states MW averaged over the half-hour; a units error, not a reading |
| SF10 | workdays with peak prices | weekdays other than Western Australian public holidays | every weekday | same call | the tariff schedule; no public holiday falls in the trial's hot workdays (asserted) |
| SF11 | days like the design day | the trial workdays at the design day's heat: seven, 43.7 to 45.3 degrees; no other workday above 39.7 | any threshold from 40.0 to 43.5 degrees, within a degree of 44.6, or at least 44.6 (four days); the k hottest workdays for k from 3 to 7; the half-hourly file's daily maxima at 40 to 43 | same call and same figures (C1, asserted) | the design day's weather in the forecast; a threshold below 39.7 or k above 7 takes in ordinary days and moves A's figure; a straight line in the day's maximum over every workday keeps C but misses the hot workdays' own response by 0.12 kW, 25 standard errors (asserted), an easier method on the same literal estimand that the data rejects, not another reading |
| SF12 | the trial sample against the 2027 population | the trial's households are a random draw of Home Plan households with an interval meter | reweighting to another mix | same call | the trial plan's draw; every Home Plan customer has had an interval meter since 2024 (forecast notes) |
| SF13 | rounding | each change computed unrounded and rounded once to the nearest whole MW | rounding the per-household effect first | same call | the prompt's closing sentence; asserted that rounding the effect to 0.01 kW moves no figure across its bin |
| SF14 | sent-out demand against metered demand | a change in household demand is added to the forecast as metered | grossed up for network losses | same call (A and B figures move) | the forecast's Method sheet: a change in customers' demand is carried into the forecast as metered, without a loss adjustment |

## Ladder

Measured by the generator on the shipped pack (`generator/checks.py` asserts every row). Changes are MW lowered
(negative raises the maximum); 41,860 Home Plan customers, the forecast's 214.6 MW maximum.

| Rung | Construction | A | B | C | Winner | Margin |
|---|---|---|---|---|---|---|
| 0 default | window cut, all 61 trial workdays, times 41,860 | 12.5 | 15.0 | 9.7 | B | 1.20x over A |
| 0b default variant | cut at the forecast's maximum half-hour (6 pm), all workdays | 13.1 | 15.9 | 10.3 | B | 1.21x |
| 1 obvious correction | the heat: hot-workday cut at the forecast's maximum half-hour | 19.9 | 23.7 | 15.2 | B | 1.19x |
| 2 sophisticated | the whole curve with the average workday's half-hourly response | 13.1 | 3.3 | 10.3 | A | 1.28x over C |
| 3 decisive | the whole curve with the response on the seven hot workdays | -5.1 (max 9 pm) | -20.0 (max 8 pm) | 11.0 (max 8 pm) | C | 11.0 MW over the Home Plan, 16.1 over A |

- **Position.** C is last on rungs 0, 0b and 1 and second on rung 2; it leads only at the decisive rung.
- **Dominance.** The decisive move reverses A and B from lowering the maximum to raising it (13.1 to -5.1 and
  3.3 to -20.0, or 19.9 and 23.7 from rung 1); nothing below it reverses a sign.
- **Worth on the graded quantity.** The call moves B to A to C. From rung 2 the decisive move shifts A by 18 MW
  and B by 23 MW and carries C across a whole-MW boundary (10.3 to 11.0); from the default every graded figure moves
  by 1.2 (C) to 35 MW (B). Heat alone (rung 1) moves B's figure from 15 to 24 MW, further from the golden, the held
  signature.
- **Grid.** Two binary corrections (heat, whole curve) give four cells: B 15, B 24, A 13, C 11; each single error
  from the golden lands on a named wrong pick. Lower rungs at the golden cell: all residential customers (44,800)
  leave C at 11 and move A to -7 and B to -22; the stayers' effect (per protocol) leaves C first; kWh read as kW
  halves every response (A 8.2 and C 7.6 MW lower, B 4.7 MW higher). Hazards add path length and no cell.
- **Flip condition.** C's figure is the design-day Home Plan maximum less the 8 pm half-hour plus C's effect there
  (214.6 less 204.0, less 41,860 times -0.009 kW); C stops lowering the maximum only if its 8 pm effect on hot
  workdays reached +0.25 kW a household, against the trial's -0.01 kW.
- **Figures mid-bin.** A -5.10, B -20.05, C 10.99 against whole-MW bins; the difference-in-differences against
  November (-5.17, -20.06, 11.07), block-adjusted differences (-4.95, -19.95, 11.06), the five hottest workdays
  (-5.08, -20.00, 10.92), the six hottest (-5.16, -20.08, 10.93) and each hot day's maximum averaged all stay in the
  same bins (asserted).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 2027-28 Home Plan customers, 41,860, moved with the right to return | filed in the prompt and the forecast's customer table; SF1, SF2 |
| 2 | Unit of account | a household (account) in the trial and a customer in the forecast | C1: one account per household in both |
| 3 | Attribution window | the trial's peak-priced workdays; the design day | C1: the hot workdays sit in January and February, clear of holidays and of the trial's first week |
| 4 | As-of dating | the forecast as issued in 2026 | filed (issue date on the cover sheet) |
| 5 | Version basis | NEM12 re-sends, the latest version per meter-day | C1: no re-sent day on a hot workday (asserted) |
| 6 | Denominator | per assigned household | filed: the trial plan's comparison; SF2 |
| 7 | Weighting | equal households per arm, matched blocks of four | C1: block-adjusted and raw arm means agree inside the bin (asserted) |
| 8 | Window length | which trial days stand for the design day | C1 for thresholds 40.0 to 43.5, the four workdays at least as hot as the design day and the k hottest for k from 3 to 7 (SF11); C4 below 39.7 (ordinary days move A's figure) |
| 9 | Boundary inclusivity | interval numbering and the window edges | C1: both files number from midnight; windows start and end on half-hour boundaries |
| 10 | Rounding path | once, at the end | filed in the prompt; SF13 asserted |
| 11 | Tie-break | the maximum half-hour | C1: the top half-hour leads the next by 4.2 MW (C), 16.7 (B) and 20.4 (A) |
| 12 | Maturity and censoring | all trial data final | C1: the March file closes every February day (asserted) |
| 13 | Order of operations | mean response per half-hour, then the maximum | C1: the maximum of each hot day's curve, averaged, agrees inside the bin (asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | re-sends and exchange days | C1: none on a hot workday (asserted) |
| 16 | Identity normalisation | NMIs in the register and NEM12 | C1: the same ten-character NMIs |
| 17 | Netting against gross | net household demand against general supply | C1: SF7 asserted |
| 18 | Dimensional units | kWh per half-hour to MW, metered to sent-out | C4: SF9 (kWh as kW moves every figure); filed: SF14 (no loss adjustment) |
| 19 | Code and status semantics | NEM12 quality flags | C1: every hot-workday read is actual (asserted); dictionary semantics elsewhere |
| 20 | Integerisation | none on the main call | C1 |
| 21 | Clause scope | peak prices on workdays only | filed in the tariff schedule; the design day is a workday |
| 22 | Forward window contents | the 2027-28 design-day profile and customer count | shipped in the forecast workbook |

## Literal reader

Executed word for word (the prompt, the forecast's methodology and design-day sheets, the trial plan's design
table, dates, assignment and right to return, the tariff schedule's windows and holidays, the meter data notes):
each design's change is the Home Plan's 50% POE maximum, the highest half-hour of the design-day profile, less the
highest half-hour of that profile plus 41,860 times the design's effect per household in each half-hour of the
design day, the effect being the assigned arm's difference from the control households. The design day is a
44.6-degree workday; the trial's workdays at that heat are seven (43.7 to 45.3 degrees), with no other workday above 39.7,
so every reading of the design day's effect selects the same days and returns C at 11 MW lower, A 5 MW higher and
B 20 MW higher. Reading the cut inside each window, or the average workday's half-hours, is an easier method on the
same literal estimand, never another reading of a filed sentence.

## Oracles

- The forecast's 50% POE maximum (214.6 MW) and its design-day profile are inputs; they tie under every basis.
- The register's 400 households a design and 400 controls tie under every basis.
- No trial report, published impact, settlement figure or corpus ships; nothing states a design's effect.
- The 2025-26 zone substation loads (distractor) show the system's summer, neither ranking the designs nor
  reproducing any design figure.
- The asks' tables (retention, bills, survey) never touch the maximum demand.

None ties only under the golden.

## Ask sheet

Three asks, 18 figures, in `tariff_trial_tables_2025-26.xlsx`. Each is a component of the tariff case that the
maximum-demand call does not turn on (H18: a measure every candidate carries, or the audit trail of the trial
population the call consumes), on rows the call never reads.

**Ask A: where each design's households stood on 28 February 2026** (9 counts: per design, still billed on it,
back on the Home Plan at their own request, no longer our customers).
- Home: the audit trail of the trial population the call's intention-to-treat difference rests on.
- Use: the Minister's question of how many households kept a design they could leave.
- Primary device (D7, the true key elsewhere, silent): households that moved within Murrandi during the trial
  keep their household and, if they asked, their design, under a new account at a new NMI; the account history
  links the accounts only by the customer number (`customer_id`), never by account or NMI. Joining the register's
  account or NMI to the history files every in-town mover as no longer a customer, including those still on their
  design and those who had already asked to return. Each design carries at least two of each kind.
- Hazards: departure reasons in three spellings (`MOVE OUT`, `FINAL READ - VACATED`, `CLOSED`), returns keyed
  `CUSTOMER REQUEST` by the call centre and `SELF SERVICE` online, households the corporation moved back after a
  life-support registration (`INELIGIBLE - LIFE SUPPORT`, not at their own request), and a request withdrawn
  within the cooling-off period (a `CORRECTION` row restoring the design from the same date).
- Path: register, account history, trial plan (3 files; customer_id, account_id, nmi, register, tariff_code,
  valid_from, valid_to, change_reason, keyed_on).
- Stops: account join (still-on and back-on undercounted, no-longer overcounted); NMI join (the new occupant's
  Home Plan read as a return); state on the date without the reason (life-support moves counted as returns);
  reason rows counted without the state (the withdrawn request counted); the customer chain (golden).
- Realism: billing systems open a new account for each premise and keep the person's customer number; a trial
  tariff follows a household only when it asks.

**Ask B: what each design charged its households** (6 figures: per design, households charged more over the
trial than the Home Plan would have charged for the same metered use, and the mean difference per household).
- Home: a measure every design carries that the maximum-demand call does not turn on.
- Use: the bill impact the Minister is asked about first.
- Primary device (D6, a ledger at another grain than its name, silent): the account history's grain is account
  by meter register; a household's controlled-load hot-water register (E2) stays on the controlled-load tariff
  whatever its design, so its difference is zero; pricing every import register at the design's rates gives each
  controlled-load household (about a third) a spurious saving of about $45 over the trial.
- Secondary device (D1, repeated keys with opposite meanings, seen with a wrong reflex): on a rooftop PV
  installation the meter is exchanged, and that day arrives as two 300 records under two meter serials, each read
  only on its own side of the exchange; genuine re-sends repeat a meter-day under one serial in a later file. The
  reflex dedup on NMI, register and date deletes half of every exchange day; summing every record double counts
  the re-sends.
- Hazards: in-town movers' charges continue at the new premise (Ask A's primary, here a hazard); returns end the
  difference on the effective date; prices GST-inclusive in the gazette against the trial plan's GST-exclusive
  table; daily supply charges that differ by design; public holidays off-peak; exports credited at the buyback
  rate under every tariff (netting exports against imports is wrong).
- Path: four NEM12 files, account history, register, tariff schedule, trial plan (8 files).
- Stops: every register priced at the design (mean too favourable, count too low); E1 only with the reflex dedup
  (mean and count off on every design with an exchange day); E1 only with every record summed (re-sends doubled);
  the golden.
- Realism: Australian meters carry a separately switched hot-water circuit on its own tariff; a PV installation
  replaces the meter mid-day.

**Ask C: whether each design's households would stay** (3 shares: per design, the share of households answering
the March 2026 survey who said they were likely or very likely to stay on it).
- Home: a measure every design carries that the maximum-demand call does not turn on (acceptance).
- Use: whether a default would hold.
- Primary device (D3, a per-row convention that passes the identity check, silent): the online form lists the
  stay question's answers from very likely (1) to very unlikely (5) and the telephone script reads them from very
  unlikely (1) to very likely (5); both modes store 1 to 5 in one column beside a mode column, and only the two
  instruments in `trial_survey_instruments_2026-03.pdf` show the reversal.
- Hazards: households that answered online and again by telephone (the instruments count the first submitted
  response), responses started and never submitted, answers from households no longer on the register's account.
- Path: survey extract, survey instruments, register (3 files).
- Stops: codes read one way (every share wrong); codes reversed by mode but duplicates kept; the golden.
- Realism: telephone scripts often read a scale from the negative end while the web form lists the positive end
  first, and the coded value follows the order read.

**Main population zero-counts (asserted by count).** On the trial's seven hot workdays and the design-day
curve: in-town moves 0 (every move after 11 February 2026, the last hot workday), meter exchanges 0, re-sent days
0, substituted or estimated reads 0, survey and account-history rows not read. The controlled-load register is
present on hot workdays and changes no evening half-hour (SF7, asserted).

**Hazard table.**

| Hazard | Asks moved | Per-ask effect |
|---|---|---|
| in-town movers (customer chain) | A (primary), B | A: every count; B: the movers' designs' means |
| meter exchange days against re-sends | B | every design with an exchange day |
| reason spellings and life-support moves | A | back-on-the-Home-Plan counts |
| GST, supply charges, public holidays | B | every mean and count |
| survey duplicates | C | the designs with a duplicate |

**Referee.** None needed: no ask has a designed disagreement between two files.

| Ask | Figures | Cracker (lands the call, runs the battery, executes every filed rule) |
|---|---|---|
| A still billed on the design (A, B, C) | 3 | miss |
| A back on the Home Plan at own request (A, B, C) | 3 | miss |
| A no longer our customers (A, B, C) | 3 | miss |
| B households charged more (A, B, C) | 3 | miss |
| B mean difference per household (A, B, C) | 3 | miss |
| C share likely to stay (A, B, C) | 3 | miss |

The cracker joins on the register's account (Ask A), prices every import register at the design and dedups
exchange days (Ask B), and reads the stay codes one way (Ask C); each device touches every design.

Mirror leakage: 10 per cent of ask weight (the mirror stops at rung 2, files A, and runs the same ask paths as the
cracker; it keeps at most the back-on-the-Home-Plan count of a design whose returns no mover touched, which the
build forbids).

Pair ceiling: 31 (cracker 45 with no ask kept, mirror 5 + 7 + 6 = 18 at a tenth of the ask weight; rerun from the
generated rubric at stage 3).

## Build record

**Stage 3 (2026-10-13).** `generator/make.py`: 138 assertions green (the input gates and the H9 file list; the
call, the signs, the maximum half-hours with a 4 MW lead and every change 0.2 MW or more inside its whole-MW bin;
the ladder's winners, margins, positions, dominance and worth; R1, R2 for each mess item, R3a to R3c on the clean
truth; SF1 to SF14; the closure variants; the three asks against the world's own truth with the cracker's paths;
the separation count; the realism sweep); `verify.py` (bundle only: its own CSV, XLSX XML, NEM12 and Schedule 1
parsing, no generator import) 22 figures, all agree; two builds byte-identical (18 target files, 2 goldens,
figures.json), target.zip sha256 d5eca98d57dff965 from the final build; `figures_check.py` 0 absent; `precut.py` 49 checks, 0 FAIL; `leak.py --asof 2026-10-09` CLEAN;
`guard.py heart` WARN only (repeat.decision against task501: the call picks a tariff design or none), `surface`
one promoted pair (below); the container audit clean on the pack and the goldens.

**Stage 4 (2026-10-13).** Leak reader, read 1 (isolated, Sonnet at medium, first cut): no sentence names the
decisive step, no file ranks the designs, no figure reads as the answer, the deciding step an analytical choice;
five realism tells (the file list listed itself, one validation stamp on every NEM12 record, a 10% POE day equal to
the 50% day overnight, table cells spilling in the plan and the instruments, year rows rising too evenly) and two
ask forks (the survey denominator with Q4 blank on 25 submitted responses, the mean read over those charged more).
Determinism judge, pass 1 (isolated thread from the judge agent's brief, same cut): NOT_DETERMINISTIC on the survey
share alone (every submitted response as the denominator gives 53.8, 44.3 and 58.1), the main call and every other
figure reproduced, Gate G analytical_non_defect with no surface-read dependency and no sole defect, Gate H domain,
layers and decisive step pass, stump power strong; SEND_BACK by the judge's mapping, a determinism repair by the
wrapper's reading. The decisive path was untouched, so the build was repaired in one generator pass and re-judged
rather than re-rooted: Q4 required before a response can be submitted, the mean pinned to that difference per trial
household, the loss convention filed once in the forecast's Method (SF14), the five tells fixed. Pass 2 (second
cut): DETERMINISTIC, FIX_NOW on one clarifying pin, the retention counts read as each household's status on 28
February (a household that asked to return and then left counts once, as no longer a customer), with GST on the
bill means optional; every figure reproduced (C -10.99, A +5.10, B +20.04 under the raw, block-paired and ANCOVA
estimators alike), the pooled route files A, a straight line in temperature misses the hot workdays, Gate H pass,
stump power moderate (a strong reader of the forecast's design-day weather will condition on hot days, and must
still carry the response over the whole curve). Read 2 (second cut): nothing names the decisive step or ranks the
designs; it found the same 28 February anchoring and the file list's history line narrating the movers. Fixed in
one pass: the prompt puts the date on the households and the bill means carry GST, the file list says each
account's tariff by register and date.

Read 3 (final cut, target.zip sha256 3268095e5de8c813): no sentence names the decisive step, no file ranks the
designs, nothing reads as planted, the deciding step an analytical choice; the eight blank Q4 answers it counted are
all on the 28 unsubmitted rows, which the instruments do not count (every submitted response answers Q4), and its
other points are the asks' designed devices (the customer chain, the withdrawn request, the CATI order) or ordinary
texture. The judge's easy route in pass 2 (the pooled whole curve, files A at 13) is rung 2 of this ladder; the
default path is rung 0 (the window cut, files B at 15); both are wrong answers the decisive rung reverses.

Determinism judge, pass 3 (final cut, the re-judge of pass 2's FIX_NOW): DETERMINISTIC, APPROVE; every committed
figure reproduced, the call and the sign pattern held under every variant it ran (fixed register premise, stayers,
the five or three hottest days, a quadratic in temperature) except the pooled average, which files A; Gate G
analytical_non_defect, no surface-read dependency, no sole defect; Gate H domain, layers and decisive step pass.
Its optional pin (the design day's temperature named in the prompt) was declined: it would announce the heat
conditioning, half of the decisive step, and the judge reads the seven hot workdays as the literal design-day set.
The window it flagged rested on a half-hourly reading of 40.3 degrees on 9 February, a day whose maximum was 39.7;
spot readings now sit below their day's maximum, so either weather file puts the same seven workdays above every
threshold from 40 to 43 degrees (asserted), a data-only repair checked by `leak.py`.

**Measured** (`generator/figures.json`, the `note` block carries every ladder, fork and closure figure this note
quotes). The call: Design C lowers the 214.6 MW maximum by 10.99 MW, its maximum the half-hour from 8 p.m., 4.19 MW
clear of the next half-hour; A raises it by 5.10 MW (9 p.m., 20.4 clear) and B by 20.05 MW (8 p.m., 16.7 clear).
C's 8 p.m. effect on the hot workdays is -0.009 kW a household against the +0.253 kW that would stop it lowering
the maximum. Every estimator and day selection the fork table names lands in the same whole-MW bins: the November
difference-in-differences (-5.17, -20.06, 11.07), block-adjusted differences (-4.95, -19.95, 11.06), the three to
seven hottest workdays (C 10.92 to 11.35), the four workdays at least as hot as the design day (-5.01, -20.05,
11.04) and each hot day's maximum averaged; a straight line in the day's maximum keeps C (12.04) and misses the hot
workdays' own response by 0.12 kW, 25 standard errors. The decisive move is a conjunction: heat alone files B at
23.7 MW, the whole curve alone files A at 13.1. Asks: A 370, 22, 7; B 361, 29, 9; C 374, 18, 6 (the life-support
moves, one, one and two, in no column); charged more 123, 45 and 52, mean differences -$19.64, -$42.86 and -$31.61,
no household within 8 cents of zero; stay shares 60.3, 41.5 and 58.8 per cent.

**Knobs** (`knobs.py`). PRIOR_SD 0.04 kW, the year-to-year change in the 2024-25 evening use the blocks match on,
tight enough that the November difference-in-differences and the block-adjusted differences agree with the raw
arms. NOISE (log-normal sd 0.04 by day, 0.10 base, 0.05 air-conditioning) with COMMON (0.03, 0.08, 0.08), the
town-wide share every household meets on the day, so each household's reads stay as rough as a meter's while every
hot-day selection lands in one bin. EFF tuned so every change sits within 0.2 MW of a whole megawatt, rung 0 files
B at 15 MW and every rung's winner leads by 1.15x or more. OFFPEAK_NUDGE (-0.0002, -0.0044 and +0.0080 c/kWh on the
gazetted off-peak prices) so each mean bill difference sits a quarter cent or more inside its cent and no
household's difference sits within 8 cents of zero. SURVEY_STAY (0.567, 0.444, 0.604) so each stay share sits 0.02
points or more inside its one-decimal bin.

**leak.py REVIEW lines.** Sweep 4 at the final cut: the trial plan carries three of the stump paragraph's words
(control, effect, corporation: the control group, a request that takes effect the next day, the organisation's
name); it names no part of the decisive step. An earlier cut flagged the survey's count 112 inside the gazetted
supply charge (112.4381 c/day); the write-up's survey lines now carry only the shares the ask asks for.

**Surface promotion.** task183 on card axes only (time gap, G14 decisive, Gate G forecasting and pick_one_of_n
collide) at a surface score of 0.080, the corpus's 61st percentile. Different driver: task183 carries each part's
own failure history into a feeder's forward event count; here a randomised tariff's half-hourly response at the
design day's heat sets a new maximum on the whole design-day curve (differentiated in the card). task136, rooftop
PV in the same sector's vocabulary, is the nearest surface neighbour (0.100) and is not promoted.

**House fixes.** H1 container scrub audited clean (the corporation as producer, dates inside 2016 to 12 October
2026); H2 every derived figure in this note is printed by `checks.py` into the `note` block of `figures.json` or by
`verify.py`; H3 the write-up's hot-day sentence states the selection as the data has it (seven workdays at 43.7 to
45.3 degrees against the design day's 44.6, none other above 39.7), where an earlier cut said none reached 39.7;
H4 the zip holds exactly the 18 declared files; H7 two builds byte-identical and the zip cut from the final build;
H8 the write-up's citations resolve (section 6 of the trial plan is the as-assigned comparison, Schedule 1 the
charges); H9 the file list names every other shipped file and no longer lists itself; H16 no date after the
extracts (`leak.py` sweep 9); H23 every ask reads with none as an answer.

**Pre-ship check, the 10/10 rules re-read against the built pack.** Domain: the deciding quantity is each
design's ex-ante load impact on the 2027-28 50% POE maximum, estimated from the randomised trial at the design
day's weather and taken over the whole design-day curve, tariff and demand-response evaluation's own analysis;
with clinic or retail nouns there is no design day, no cooling banked through the peak price and pulled down at
the step, and no half-hourly maximum, so the swap breaks (both judge passes: domain pass). Two layers: the Layer 1
mess (NEM12 re-sends, quality-split days, exchange days on two serials, 15-minute meters at new premises, accounts
against NMIs, GST bases, interval-ending times, Bureau weather gaps, holidays) is neutral on the call by assertion
(R2: each item mishandled leaves every main figure in its bin), and Layer 2, the half-hourly response at the design
day's heat over the whole curve, decides it (R3a files B on the clean truth with every filed rule applied, R3b the
decisive step alone files C). Decisive step analytical: the pooled route files A and the window cut files B with
every field read and every rule executed (both judge passes: decisive_step analytical, analytical_non_defect, no
surface-read dependency, no sole defect); nothing planted, no decoy, no certified replay.

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
- G13 decisive under method_or_model_selection: dropped at the card, because the final flip (A to C) is the heat,
  not the whole curve; G14 decisive with forecasting as the Gate G mechanism, differentiated against task183 in
  the card.
- 15-minute meters at a share of the trial premises: dropping them (a natural reflex when a file mixes interval
  lengths) moved C's figure by half a megawatt, a mess item touching the call; they now sit only at the premises
  in-town movers moved to, every move after the last hot workday.
- Household day-to-day variation at log-normal sd 0.08 (day), 0.22 (base) and 0.15 (air-conditioning), all of it
  idiosyncratic, with blocks matched on a loose prior (sd 0.18 kW): the five hottest workdays put C's figure in
  another whole-MW bin (9.4 against 10.0) and the November difference-in-differences sat 0.7 MW off; most of the
  variation is now town-wide (cloud, wind, the evening's television), shared by every household, and the blocks
  match on a tighter prior, so every hot-day selection and estimator variant sits inside one bin.
- Q4 left blank on 25 submitted survey responses: with the instruments counting a response once it is submitted,
  "those answering the survey" read two ways (stage 4 reader); both modes now need Q4 answered before a response
  can be submitted, so every reading selects the same responses.
- "the mean difference per household" could be read over the households charged more (stage 4 reader); the prompt
  now says per trial household.
- A file list that listed itself, one validation stamp on every NEM12 record, a 10% POE day equal to the 50% day
  overnight and table cells spilling across columns in the trial plan and the instruments: realism tells from the
  stage 4 reader, each fixed in the generator.
- The file list described the account history as covering "a trial household's new premise", narrating Ask A's
  mover device (stage 4 read 2); it now says each account's tariff by register and date.
- The retention ask's date anchored only its first count, so a household that asked to return and then left
  Murrandi read as back on the Home Plan or gone (read 2); the date now sits on the households, one 28 February
  snapshot for all three counts.
- Half-hourly readings above their day's maximum (40.3 degrees in HM01X on 9 February against a 39.7 maximum): a
  solver taking each day's maximum from the half-hourly file at 40 degrees took in two ordinary days and moved A and
  B (judge pass 3); spot readings now sit below the day's maximum.

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
