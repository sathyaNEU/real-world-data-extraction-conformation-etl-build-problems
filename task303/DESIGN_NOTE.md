# task303: design note

Architecture 2 (re-rooted 2026-10-25 from architecture 1, the pet insurer's renewal increase, spent at stage 4).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task303.json`, architecture v2, registered 2026-10-25 17:59 UTC and
  re-checked against the registered card: WARN only, each answered below.
- **Pairing:** Energy Systems & Utilities / `asset-condition-maintenance`, drawn for Opportunity Sizing & Decision
  Support. The task type sizes what an asset investment buys: here the customer-minutes of sustained interruption a
  year that converting one feeder's three-phase backbone to covered conductor removes, pool (the candidate's recorded
  customer-minutes outside major event days) to realisable (nine in ten of those from vegetation, wind and wildlife
  faults on the backbone the conversion replaces).
- **Niche:** Shenmore Valley Electric (fictional investor-owned distribution utility in the US south-east, 18 feeders on
  six substations) files its 2027 storm-hardening plan with the state commission by 1 December 2026. The 2027 budget
  converts one feeder's backbone, from the feeder breaker to the end of the three-phase line, from bare conductor on
  wood poles to covered conductor on steel poles; six feeders on three substations are candidates.
- **The call:** F-205 (Sorrel Hill), about 263,000 customer-minutes a year on the prototype (seed 42; frozen at stage
  3), worth about USD 553,000 a year at the commission's USD 2.10. Every route that credits each feeder-breaker
  ticket to the feeder's own backbone converts F-112 (Pell Creek) at about 356,000.
- **Shape 01:** the six candidates ranked by their figure (six graded figures), the call, the incentive value, then the
  asks (stage 2). Shape `other` is banned against task166 and task301.
- **Strategy:** `decomposition_attribution` (a feeder's recorded customer-minutes split by where each interruption
  began: its own backbone, its taps, or its substation's supply), gap population (what one breaker-level ticket is),
  generators G8 (the conversion cannot reach a loss of the substation's supply, decided ticket by ticket) and G3 (the
  ticket names the feeder's own breaker while the interruption began upstream); Gate G `decomposition_attribution`.
  Pattern none: pattern C's serviceable share behind a join is not the form here.
- **Furniture:** forum regulator_or_inspector (the commission reviews the filing), forcing statutory_or_regulatory_filing
  (the plan due 1 December 2026), organisation utility_or_infrastructure, role capacity_planner (the distribution
  planning engineer who prepares the filing), context artifact operations_log (the outage system's exports),
  calibration none.
- **People** (`guard.py names --geo US --seed 303`): Zachary Sanders, distribution planning engineer, author of the
  valuation guidance. Not in the prompt.
- **Spent mechanisms on the objective** (`guard.py mechanisms --objective opportunity-sizing-decision`, twelve builds):
  task105 the part of a catchment nearer the new outlet; task106 candidates drawing on one shared pool; task116 a group
  offer reachable through one signatory; task118 the gain on volume a unit does not already treat; task120 a supply
  system's draw net of what accumulated inside it; task127 the part of a fused wait the intervention removes; task128 a
  contact's effect read only on over-capacity days; task306 an asset base taking in units the roll does not hold yet;
  task305 short-stay occupants who sit in no origin; task302 a stocked-out line's loss net of diversion and rebound;
  task301 a recorded state decaying between recordings; task303 v1 the owners a renewal increase drives away. None
  attributes a unit's recorded losses to their origin through the minute its sibling units share.
- **Abstraction test:** nearest driver task127 v2 at 0.08 (the part of a recorded wait the intervention removes,
  because the wait fuses the replaced step with a concurrent one): there the fusion is inside one unit's own record and
  the replaced step's excess is read from its timestamps; here the record is complete and correct for its feeder, and
  the part the conversion cannot reach shows only across the sibling feeders' tickets. task252 v2 at 0.05 (error
  arising upstream of every channel) reads an error common to channels against a truth; here nothing is in error.
- **Probes before the draw:** four concept probes (sonnet, medium, no files) on four candidate designs; three applied
  their decisive step unprompted (Tried and rejected), the fourth, this design, filtered by major event day, cause and
  device, shrank the history and never asked where a breaker ticket began. Then two call-only probes, isolated, sonnet
  at medium, on a prototype pack (scratch `p303uo/`, /tmp/r303ua and /tmp/r303ub: both OMS exports, the major event
  days, the inventory, the plan's valuation guidance, the export notes and the vegetation work orders): both converted
  F-112 at 356,000 customer-minutes a year (USD 748,000), the default path to the figure; neither looked across the
  sibling feeders.
- **WARNs answered:** `people.first` (Zachary, one older build); `repeat.gate_g` (task121 v5, spent); `repeat.decision`
  and `repeat.question_form` (task166 v2): the decision is a pick of one of six feeders, so the question asks which.
- **Data-native sentence:** Pell Creek's three feeders open their breakers in the same minute sixteen times in the
  2019 to 2025 record outside major event days, and the outage system records each as an interruption on that
  feeder's breaker with the cause the crew found on the line feeding the substation (a tree, wind, lightning), so
  eleven of F-112's sixteen vegetation, wind and wildlife breaker and recloser tickets, 73 per cent of their
  customer-minutes, are losses of the substation's supply that no backbone conversion can prevent.

## Three rules

Task type: asset-condition-maintenance (Energy Systems & Utilities), tagged in the taxonomy for Opportunity Sizing &
Decision Support: the customer-minutes of sustained interruption a backbone conversion removes from each candidate
feeder, pool (its recorded customer-minutes outside major event days) to realisable (nine in ten of those from
vegetation, wind and wildlife faults on the backbone it replaces).
Domain test: The deciding quantity is the customer-minutes a backbone conversion removes, which reliability engineering
attributes interruption by interruption to where it began (the feeder's own backbone, its taps, or the substation's
supply) from the protective device that cleared it and, for a loss of supply, the sibling feeders that all lose supply
in the same minute; only the interruptions that began on the converted backbone from the causes it addresses are
credited.
Swap: "the feeder whose backbone conversion removes the most customer-minutes once the breaker tickets every feeder at
its substation opened in the same minute are traced to the substation's supply" put into a hospital's wards or a
retailer's stores loses its mechanism: no ward or store records a shared upstream loss of supply under its own
protective device, and no refit of one ward is credited with the minutes of the circuits it carries.
Layer 1: the outage system migrated on 1 January 2023 (legacy tickets with feeder numbers, codes, Eastern local dates
and clock times and minutes of duration; current tickets with feeder ids, worded categories and UTC start and
restoration stamps); major event days as Eastern calendar days against UTC stamps; vegetation work by feeder section on
a four-year cycle; an inventory with LiDAR canopy shares, pole counts and ages; nothing is placed to be caught.
Layer 2: field_method: interruptions are attributed to their origin before an investment on one feeder is credited; a
loss of the substation's supply, which every feeder there records at its breaker in the same minute, is not a fault on
any feeder's backbone and the conversion removes none of it.
Decisive step: separating, among each candidate's feeder-breaker tickets, those every feeder at its substation opened
in the same minute (losses of the substation's supply) before crediting the conversion with nine in ten of the
remaining vegetation, wind and wildlife customer-minutes on the backbone.
Not semantics: every field reads as what it is (the breaker is the feeder's breaker, the cause is the cause on the
ticket, the customers are the customers who lost power); no field, code or note says where an interruption began, and
an analyst who maps both exports, converts every clock and drops the major event days exactly still credits every
breaker ticket to the feeder's backbone, as both call-only probes did.
Not rule application: the guidance files the WHAT (the conversion's scope, faults on the converted backbone from
vegetation, wind or wildlife, nine in ten prevented; the 2019 to 2025 record outside the accepted major event days
divided by seven; customer-minutes as customers times minutes) and nothing about where a ticket's interruption began.
Enumerated family on the prototype: crediting every breaker and recloser ticket (the probes' route) files F-112 at
356,000 and F-205 third at 263,000; removing the shared-minute tickets files F-205 at 263,000 and F-112 at 97,000, a
spread of 259,000 on F-112's figure, 2.7 times its value once the shared tickets are removed. Standing family (the constructions that remove
the shared-minute tickets: the same start minute, within 1, 2 or 5 minutes, at least two sibling feeders): an
identical figure for every candidate, spread zero, F-205 every time. What rules the crediting route out is no filed
clause but the record: a fault on one feeder's backbone cannot interrupt its sibling feeders' customers.
Analyst test: A strong analyst who reads every file correctly sums each candidate's feeder-breaker and line-recloser
tickets caused by vegetation, wind or wildlife outside the accepted major event days over 2019 to 2025, takes nine in
ten of their customer-minutes divided by seven and converts F-112 at about 356,000 customer-minutes a year, where the
golden is F-205 at about 263,000; checks.py runs both on the generator's clean truth and on the pack (stage 3).
Estimand: the customer-minutes of sustained interruption the conversion would have removed from the 2019 to 2025 record
had it been in place, outside the major event days the commission accepted, divided by seven, the conversion preventing
nine in ten of the faults on the converted backbone from vegetation, wind or wildlife and nothing else
(storm_hardening_plan_2027.docx, sections 1 and 3).
No decoy: nothing is planted: the outage exports are the utility's tickets as its two systems kept them, the major event
days the commission's; no memo, draft or figure argues for a feeder, no file ranks the candidates, no past plan or
valuation is in the pack, and no stakeholder figure is set up to be overturned.
No certified replay: no certified or published figure sits in the pack; no file states a reliability index, a past
valuation or a past plan to be reproduced, and the attribution is not recovered from any figure.
Lesson: a feeder's outage record carries every interruption its customers suffered, wherever it began, and an
investment in the feeder is worth only the interruptions that began on the part it changes; a loss of the substation's
supply shows only as the same minute on every sibling feeder's breaker. No build on file attributes a unit's recorded
losses to their origin through the minute its sibling units share.

## Default path

The pipeline a strong analyst builds from the prompt, the guidance and the exports' fields:

1. Stack the two outage exports: legacy feeder numbers to F-nnn, legacy codes to the current wording, current UTC
   stamps to Eastern time; customer-minutes are customers times minutes (legacy duration, or restoration less start).
2. Drop the tickets that began on an accepted major event day (Eastern dates).
3. Keep the backbone tickets (feeder breaker and line recloser) and drop the fuses (taps and laterals).
4. Keep vegetation, wind and wildlife.
5. Sum each candidate over 2019 to 2025, take nine in ten and divide by seven.
6. Rank: F-112 about 356,000, F-114 about 271,000, F-205 about 263,000, F-301 about 118,000, F-208 about 107,000,
   F-303 about 21,000.

Ends on: convert F-112 (Pell Creek) at about 356,000 customer-minutes a year, about USD 748,000 at the incentive.

## Stump sentence

A competent solver credits every feeder-breaker and line-recloser ticket caused by vegetation, wind or wildlife outside
the major event days to the feeder's own backbone and converts F-112 at about 356,000 customer-minutes a year, where
the golden is F-205 at about 263,000; the step that lands it there is reading each Pell Creek breaker ticket as a fault
on F-112's backbone, when the tickets all three Pell Creek feeders open in the same minute are losses of the
substation's supply, which the conversion cannot prevent.

## Tried and rejected

- Permit centre standard plans (the seed's world, municipal permitting x Opportunity Sizing: ten funded positions across
  intake, plan review, corrections and issuance, plan review's 2027 load driven by the builders entering the city with
  their plan libraries): both call-only probes landed the allocation (intake 3, plan review 3, corrections 1, issuance
  3) from the builders' outlook; and staffing a stage pipeline reads the same in any office, so the swap test fails.
- A world with the Lifetime Dog tariff at its first level and narrow claim costs: marking a continuing condition only
  once it recurs in a second policy year put Lifetime Dog above Essentials in 21 of 144 constructions, and raising the
  tariff 10 per cent instead let the claims-paid route land Essentials; claim costs were given a wider spread and the
  tariff 5 per cent, with a larger Essentials book, so every split names Essentials and every route Lifetime Dog.
- A policy history from 2014 instead of 2019: the lifetime books' held owners piled up, and the recurrence and span
  markings named Lifetime Dog.
- Architecture 1, the lifetime owners held by a continuing condition (Essentials at CAD 0.5 million, every one-response route on Lifetime Dog), spent at stage 4: reader A named Essentials with a retention logit carrying claims in the expiring and prior terms by product (lifetime claimants almost never leave), a covariate reflex that reaches the split without marking a condition; the judge returned SEND_BACK because the printed addition ran from CAD 0.32 to 0.51 million across condition markings, flag timings and response fits; both readers took all 48 ask cells (the wrap codes against the menu option, the case-number gaps against the letters, a same-amount debit 10 to 14 days after each return).
- 2026-10-25, architecture 2 screen, three concept probes (sonnet, medium, no files), each landed by the probe applying
  the decisive step unprompted: a winter-peaking utility's efficiency programmes at the peak hour (the lamps' heat
  made up by electric heat in resistance-heated homes, the pilot's gas-heated homes measuring the gross saving); a
  water company's meter cohorts (bench errors at four test flows weighted by each cohort's consumption profile from
  the logger panel); a card issuer's collections team (the treated cures valued against the recoveries the control's
  charge-offs bring in after charge-off, the immature vintages completed).
- 2026-10-25, architecture 2 screen, earlier in the re-root: county input-output commuting leakage (both call-only
  probes landed on the Type II caveat); an excise's efficiency cost on a partial-adjustment path with the existing
  wedge's rectangle (a concept probe applied both moves; economics x Opportunity Sizing banned against task302).
- 2026-10-25, architecture 2 screen, dead on paper with the reason in one clause each: a card cure's re-default
  (task177); a deflated Sharpe ratio (task175); win-back waves (task157, task134 v2); a bonus's pull-forward (task161,
  task180); depletion of responsive members (task124, task176); deadweight (task136); regression dilution (task200);
  traffic assignment (task253's lineage); common-cause redundancy (task201); transformer thermal ageing (task121's
  screen); private equity commitment pacing (task167, task501); EV home-charging composition (a stratification reflex);
  stormwater green infrastructure timing and annuity late reporting (earlier probes and task181 v2); housing moving
  chains; the bus wait inspection paradox; a pension sleeve's market impact; a design-effect boost; refinance
  burnout; catastrophe as-if (the replay law); transmission N-1 (the capacity-credit pincer); a vegetation trim cycle's
  phase (task129's world); wind farm wakes and long-term mast correction (named caveats the setting cues); technical
  against non-technical losses (a named caveat); tap-changer wear per operation (task46's driver).
