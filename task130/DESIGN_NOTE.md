# task130: Corvane Health, the first-year contribution to its professional liability trust (architecture 4, rule 3 rework 3b)

Private, never ships. Architecture 4, drawn 2026-10-12 as the author's fourth root for a number retired with three
architectures spent; shipped 2026-10-12 at $784,000 (round 1); a round 2 redesign was sent back by the judge on
2026-10-14 and round 1 restored. On 2026-10-15 the rule 3 audit read round 1 AT_RISK: funding policy 3.4 ("used as
recorded ... no development or tail factor ... no distribution is fitted") filed the estimator by eliminating every
rival, 3.2 read as a cost-per-FTE-year recipe, and the headline wrong answer ($4,854,000) was a contract misreading,
not an analysis. Round 3a reworked it in the same world (Corvane Health, the trust, its four entities and their
Transition Dates, the 2027 Plan Year): the funding policy filed only the WHAT, the lag truncation became the default
path's own construction, and the decisive step was the cost each window Claim carries at its own report lag. The
judge read 3a DETERMINISTIC, APPROVE (Gate H analytical), and the rule 3 re-audit passed it with a moderate stump: the
field's loss-weighted claims-made step factor is the golden's own construction, so a strong solver lands it without
seeing the lag-cost link. This note is round 3b, a second analytical layer that the step factor on the whole
experience misses by a bin: the Early Resolution Program's disclosure settlements, the Claims a first claims-made year
catches most of, began at each entity on its own date between January and July 2019, none came from earlier
incidents and they run every year since, so the 2027 window inherits the claims process since each entity's start and
the 2016 to 2018 years, pooled in, understate it by a quarter. The earlier architectures' records are under
`## Retired` and `## Tried and rejected`; the card keeps every dead identity in `lineage`.

Carried forward as design rules: the default path is written first and must end wrong on the data in hand; no filed
sentence names or narrows the estimator or the experience period; no figure in the pack confirms the solver's
construction for free.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task130.json`, architecture v4 (rule 3 rework 3b, edited in place 2026-10-15); `guard.py validate` clean; `guard.py heart` WARN (one finding, `people.first` Lori against task129, an older build; Lori Williams stays, she signs the data dictionary); the driver sits at 0.32 against this slot's round 1 and 0.14 against round 2, both differentiated |
| Domain / task type | actuarial-science-insurance / pricing-ratemaking-credibility (a client domain): funding a self-insured professional liability programme's first claims-made year is pricing its cover |
| Objective | Forecasting & Predictive Modeling: the expected cost of the Claims that will first be made against a new trust in 2027, its first Plan Year, from the system's 2016 to 2024 claims experience valued 30 September 2026, on the claims process 2027 will run under |
| Shape | other: the contribution (one figure), then two reconciliation asks across the four entities (open claims under each expiring carrier's policies missing from its latest loss run, with our reserves on them; the covered clinician FTE the payroll paid in each of July, August and September 2026) and a chart of the second; 28 criteria before the files and rounding |
| Decision | `quantity_figure`, answer unit `currency`: the 2027 contribution the trustees put into the trust, to the nearest $250,000 |
| Mechanism | gap time (the trust pays only for Claims made inside its own opening window), then population (the Claims a short window catches are a different mix from the experience's average, and that mix began at each entity in 2019); pattern none; generators G13 (the window the decision covers), G14 (the cost of a Claim conditioned on how soon it is made) and G6 (the claims process shifted under the experience); Gate G `forecasting`; strategy `maturity_censoring` (the window censors each Claim's report lag, and the Claims it keeps carry a cost profile and a history of their own) |
| Layer 2 family / pattern | `field_method` (the professional liability actuary's claims-made pricing from the system's own report-lag experience, on the experience period that matches the claims handling the window will see); `own:claims-made-first-year-cost-conditioned-on-report-lag` |
| Furniture | forum `trustees_or_governors`, forcing event `launch_or_rollout` (the trust launches on 1 January 2027 and takes the entities in on their anniversaries; the first contribution has to be fixed before it; moved from `vote_or_meeting`, which task128's later re-root put among this card's last three), organisation family `hospital_or_health_provider`, role family `compliance_or_audit`, context artifact `register`, calibration `none`, opening `question-first`, question form `how-much` |
| Spine | `clinician_fte_by_month_2016-01_2025-12.csv`, the legacy payroll, 224,767 rows: one employee's paid FTE in one month on one cost centre, with the job code (two code sets, the 2020 set from July 2020), entity and status; constructed. The 2026 HCM pay lines (30,764 rows) carry Ask B |
| Deliverables | `trust_funding_2027.xlsx` (the contribution, the entities' Transition Dates, the experience behind it, the carrier loss run check, the paid covered FTE for July to September 2026, notes), `trustees_paper_2027.pptx` (slide 1 the contribution, slide 2 the grouped chart of each entity's paid covered FTE in the three months) |
| People | from round 1's draw (`guard.py names --geo "United States" --seed 130`): Nancy Holland (vice president, risk management and insurance; the requester; author of the premium history and the goldens), Derek White (chief financial officer; the staffing plan), Lori Williams (director of claims and litigation; the data dictionary), Walter Butler (chair of the trustees; signs the agreement and the policy). Elizabeth Nelson and Jerome Warren were dropped: no shipped file names them and Elizabeth now collides with task128 |

**Guard.** `guard.py heart task130`: WARN (Lori against task129, an older build). Round 3a first tried
`composition_mix` (ban.strategy against task125, and it would have banned task137), so the strategy stays
`maturity_censoring`; the forcing event is `launch_or_rollout` (no ban on this card or on task136 to task138, checked).
Round 3b adds generator G6 (the claims process shifted under the experience). The driver sits at 0.32 against this
slot's round 1 driver and 0.14 against round 2's, both carrying a differentiation line (round 2 split the history by
unit, every year pooled; here every unit's own history is used from its own start); nearest other driver task457 at
0.06.

**Data-native sentence.** Since 2019 Corvane's care teams disclose serious harm through the Early Resolution Program,
which meets the patient within days and settles within weeks at tens of thousands of dollars; each entity began on its
own date between January and July 2019, and before that the same harm surfaced a year or more later as a demand or a
suit, or not at all. Most other patients who ask for compensation do so through the program months after the care,
once treatment and bills are done, and settle for a few thousand; the demands and suits that carry nearly all the money
arrive a year or more after the incident. So the Claims a trust's first months can catch are the disclosure
settlements and the cheap program requests, in proportions set by how many days each entity has left in the year, and
only the years since each entity's first settlement show them at the rate 2027 will.

**World (as built, claims seed 3006).** Corvane Health, a nonprofit health system in western Oregon: three hospitals and
an employed medical group, about 1,800 covered clinician FTE paid in September 2026 (employed physicians and advanced
practice clinicians in Schedule B jobs, per-diem clinicians by the shifts paid). Each entity has insured its employed
clinicians with an annual occurrence policy on its own anniversary; the board resolved to let each run to expiry and
move the entity into the new Corvane Professional Liability Trust, claims-made, the retroactive date equal to the
transition date:

- Tolliver Falls Hospital (188.0 covered FTE paid in September 2026), with Quillan Mutual since 1 January 2021 (Halberd
  Hospital Mutual before): trust from 1 January 2027, the only full-year entity.
- Alderwick Medical Center, the flagship (465.4), Quillan Mutual since 1 April 2019 (Corrigan Lane before): trust from
  1 April 2027.
- Corvane Medical Group, the clinics (1,040.6), Stoneleigh Casualty since 1 July 2019 (Westerholm before): trust from
  1 July 2027.
- Brennick Community Hospital (108.2, affiliated 1 July 2019), Stoneleigh Casualty since 1 October 2022 (Tallis
  Reciprocal before): trust from 1 October 2027.

Seven specialty classes as Schedule B rates them. The Early Resolution Program has taken patients' requests since
September 2015; its disclosure arm (the care team discloses serious harm and the program settles within weeks) began
at Alderwick in January 2019, Tolliver Falls in March, the medical group in May and Brennick at its affiliation in
July (generator truth, `disclosure_from`); before an entity's start such a harm became a demand or a suit a year or
more later (55 per cent) or no claim. In the experience (incidents 2016 to 2024, valued 30 September 2026) there are
3,320 Claims, one per incident, against 13,747.1 covered FTE-years. By route (generator truth, not shipped): 320
disclosure settlements made a median of 17 days after the care at an average of $27,814 (2027 level), all from
incidents after their entity's start; 2,592 program requests made a median of 238 days after at $7,911; 408 direct
demands and suits made a median of 782 days after at $423,024. The register carries no route and no programme code:
it shows no Claim made within 40 days of a 2016 to 2018 incident, and from each entity's first such Claim (Alderwick
January 2019, Tolliver Falls April, the medical group May, Brennick July: the data's months) 40 to 64 a year made
within 30 days, 25 to 43 per 1,000 covered FTE-years in every year from 2020 to 2025 with no trend (asserted). Since
those months the experience is 2,288 Claims on 9,330.0 FTE-years (32.1 per cent of the exposure falls before them):
295 made within 30 days at $28,209, 38 in days 31 to 90 at $17,391, 1,768 in days 91 to 364 at about $9,300 and 187 a
year or more after at $420,503. The expected cost of the 2027 window is $1,281,536 (68.4 expected Claims at about
$18,700 each, four fifths of the cost in the disclosure settlements); on the whole 2016 to 2024 experience the same
construction gives $961,261.

As-of date: the claims register extract runs Friday 2 October 2026, valued 30 September 2026; the HCM pay lines run
through work month September 2026; the loss runs arrive 5 to 9 October; the pack is handed over on 12 October 2026.

## Default path

1. Read the claims register (one row per named defendant), keep the rows whose clinician is a Covered Clinician (a
   Schedule B job in the legacy payroll in the incident month), merge each incident's claim numbers into one Claim made
   on its earliest claim made date (trust agreement 1.3), class it by its first-named Covered Clinician (Schedule B
   Note 2), and take the experience the trust holds, incidents from 2016 to 2024 (funding policy 3.3): 3,320 Claims.
2. Value each Claim at paid plus case reserves on its Covered Clinicians' rows and trend it at 5 per cent a year from
   the incident year to 2027 (3.4); sum the payroll's covered paid FTE over 2016 to 2024 by class, each month one
   twelfth of an FTE-year: 13,747.1 FTE-years.
3. Read the claims-made window correctly: from each entity's Transition Date to 31 December 2027, only Claims made by
   year end count, so for each day of each entity's plan exposure take the class's experience Claims per FTE-year
   whose delay from incident to first making fits in the days left.
4. Price the window the field's way, with the loss-weighted report pattern: each experience Claim at its own trended
   cost, counted for the 2027 FTE-years of its class with at least its own delay left (the claims-made step factor on
   loss dollars, claim by claim or by month of delay), and add the classes.

Ends on: $1,000,000 ($961,261 unrounded; by whole months of delay at mid-month exposure, the re-audit's probe,
$970,859), the whole 2016 to 2024 experience priced at each Claim's own delay. The frequency-severity build of the same
window misses higher, on the whole experience $3,750,000 ($3,697,267) and since each entity's start $3,250,000
($3,283,884); a severity from the Claims made within a year gives $750,000 ($782,973).
Golden: $1,250,000 ($1,281,536 unrounded), the same construction on each entity's experience from the month of its
first disclosure settlement to December 2024 (2,288 Claims on 9,330.0 FTE-years).

## Stump sentence

A strong solver who reads the claims-made window correctly and prices it the field's way, each 2016 to 2024 Claim at
its own trended cost against the 2027 FTE-years with its own delay left (the loss-weighted claims-made step factor),
files $1,000,000 (Ends on); the step that lands it there is pooling the whole experience the trust holds, when the
Claims a first claims-made year catches are mostly the Early Resolution Program's disclosure settlements, made within
weeks (about $28,000 each), which began at each entity only between January and July 2019 and have run at the same
rate every year since: 2016 to 2018 and each entity's first months of 2019 carry the program's requests and the late
suits but none of the settlements, a third of the exposure at a fifth of the window's cost per FTE-year, so the pooled
pattern understates the window by a quarter. Costing the window on each entity's experience from its first settlement gives
$1,250,000; the count route at the class average misses on either experience ($3,750,000 whole, $3,250,000 since the
starts), so both layers are needed.

## Three rules

- **Task type:** actuarial-science-insurance / pricing-ratemaking-credibility, pricing the first claims-made year of a self-insured professional liability trust; the type serves Forecasting & Predictive Modeling in the taxonomy.
- **Domain test:** the deciding quantity is the expected cost of Claims first made inside a claims-made trust's opening window, built from each entity's covered exposure through the system's own report-lag experience, each Claim at its own cost and lag, on the experience period that matches the claims handling the window will run under, which is how a professional liability actuary prices a first claims-made year after a change in claims handling; the swap below breaks it.
- **Swap:** put warranty claims and units sold in for clinicians and FTE-years and the task stops making sense: there is no claims-made trigger, retroactive date, disclosure settlement, program request or late suit, so nothing makes a claim's cost depend on how soon it is reported or a disclosure programme change when claims are made.
- **Layer 1:** a register with one row per named defendant (residents and contracted clinicians in it, contracted rows unpriced), requests that become suits under new claim numbers, reopened claims, a legacy payroll across the July 2020 job codes with per-diem rows at two decimals, dual appointments, transfers and unpaid leave; each mishandled leaves the call in its bin (R2, asserted one line each), and none touches the claim dates the second layer lives in.
- **Layer 2:** two steps an expert takes and the field's reflexes skip. The window's Claims cost what their own lag says, high within weeks, low over the following months and highest after a year, so each window Claim is costed at its own lag (the count at an average misses); and the quick, costly Claims began at each entity in 2019 and run steadily since, so the window is priced on the experience from each entity's start, not the whole 2016 to 2024 pool (the loss-weighted step factor on every year misses by a bin).
- **Decisive step:** costing the 2027 window on each entity's experience from the month of its first disclosure settlement, each Claim's own trended cost counted for the 2027 FTE-years of its class with at least its own delay left, instead of the loss-weighted step factor on the whole experience the trust holds or the window's count at any average or fitted severity.
- **Not semantics:** no field, code or definition marks the change: the register carries no route, channel or programme code, matter type is Claim or Suit on both sides of 2019, and a solver who reads the trigger, the Claim definition, Schedules A and B, the policy and every column correctly, and truncates every lag right, still files $1,000,000 on the whole experience; the change is visible only in the claim dates, as the lag mix by incident year and entity.
- **Not rule application:** the funding policy files the estimand (the cost of the Claims first made in the Plan Year, as Claims will arise and be made in that year), how exposure is measured, the experience the trust holds (2016 to 2024, rated by class), the valuation and the trend; no sentence names a start date, a break, a weighting of years, a lag treatment or a severity, and executed word for word on the whole experience held the filed sentences give $1,000,000 or $3,750,000, never the golden (Literal reader, R3a asserted).
- **Analyst test:** a strong analyst who dedupes the register, merges claim numbers, reads the claims-made window and costs every window Claim at its own delay, the field's loss-weighted step factor, still files $1,000,000 on the whole 2016 to 2024 experience ($961,288 on the generator's clean truth, asserted), a full bin and more below the golden $1,250,000.
- **Estimand:** funding policy 3.1 (expected cost at 2027 level of Claims first made in the 2027 Plan Year, as Claims will arise and be made in that year) with trust agreement 1.3, 1.7, 2.1, 2.4 and Schedule A (claims-made from each Transition Date); the population includes Claims not yet observed (2027 incidents), projected from the experience of 3.3 on the exposures of 3.2, under the claims process the register shows every year since each entity's first disclosure settlement.
- **No decoy:** no memo, draft, briefing or stakeholder figure argues a contribution or an experience period; no file states a 2027 cost, a step factor, a lag table, a severity curve or the programme's dates; the safety events and the defence invoices are plain distractors no route reads.
- **No certified replay:** no certified or published figure is reproduced to recover the method; the window's cost is estimated directly from the register and the payroll, and nothing in the pack confirms the construction or the start months.
- **Lesson:** a first claims-made window inherits the claims process in force when it opens: when the quick, costly claims it catches began part way through the experience, unit by unit, the window is priced on each unit's experience since its start, each claim at its own lag; the whole history's loss-weighted step factor, round 3a's golden, is this build's default.

## Gate G

- **Litmus.** No. Every file is correct: the register, the payroll files, the staffing plan, the loss runs, the premium
  history, the trust agreement and the funding policy. No stakeholder states a number the task overturns and no file
  states the trust's 2027 cost or the programme's dates.
- **Primary mechanism:** `forecasting` (the correctly read past pins the 2027 window's cost only through the claims
  process since each entity's first disclosure settlement and the cost each window Claim carries at its own lag).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test.** On the generator's clean truth (true jobs, unrounded paid FTE, every escalation merged) the
  default path files $961,288 against the golden $1,281,570, every route on the whole experience still misses by a
  full bin except the two that offset (Ladder), and every round 1 route on the experience since the starts misses by
  a full bin (nearest a gamma GLM linear in the delay, $285,551 off), asserted (R3a).
- **Deletion test.** Delete the two distractors, the loss runs, the notice log, the premium history and the HCM pay
  lines: the call recomputes to the dollar (asserted) and the default path is still wrong.
- **Lens swap.** The default and the golden count the same window by the same construction; they differ only in the
  experience years each entity contributes, the whole held period against each entity's months since its start.
- **No artifact ranks or prices the decision.** No shipped file states a 2027 cost, a claims-made factor, a report-lag
  table, a severity by lag, a curve or a start month. The premium history prices occurrence cover (a mature year with
  carrier loads) and is read only by Ask A, for the carriers' terms.

## Readability screen

Six tests per rung: 1 filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a reflex
of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction, ratio or
half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the claims-made window: only Claims made in 2027 from incidents after each Transition Date count | fires: trust agreement 2.1 and 2.4 and the prompt's "first made against the trust that year" | the register's incident and claim made dates | yes, once read | no | no | the count share is a ratio | readable |
| R1 the window's expected count per day of exposure, each delay against the days left | the window is filed; the day count follows from dates | incident and made dates give each delay | yes, for an actuary who read R0 | no | no | a convolution, but the textbook one | readable |
| R2 each window Claim at its own cost (the loss-weighted step factor) | no sentence | incident and made dates and the amounts | yes: the field's claims-made pricing on loss dollars | no | no | a convolution | readable |
| R1y a severity from the Claims made within a year (or the same calendar year) | no sentence | the made date | partly: "use the severity of the claims that count" | no | no | yes (one filter) | readable |
| R3 (decisive) the experience from each entity's first disclosure settlement, not the whole period held | no sentence names a start, a break or a weighting of years; 3.3 says what the trust holds and 3.1 that the cost is of Claims as they will be made in 2027 | no column carries a route, a channel, a programme or a lag; matter type reads Claim or Suit on both sides | no: the reflex is to pool every year the policy names, and the step factor gives a smooth pattern on them | none ships | no: every row is complete and correct | no: each entity's own start read off the claim dates, then the whole construction re-run on its months | silent |

The decisive rung is silent because the change lives only in the claim dates: the register shows a Claim made within
weeks of its incident from no 2016 to 2018 incident and in every year from each entity's first month in 2019, but
nothing names the disclosure arm, its dates or the years it changed; only a reader who looks at the lag and cost mix
by incident year and entity sees that the experience the window inherits starts there, and that the pooled years
carry the window's cheap requests without its costly settlements.

## Semantic fork table

One row per term of the main ask and per convention the computation needs. `checks.py` asserts each row (the
alternative computed and shown to converge, or moved and closed by the sentence and data fact named).

| Id | Term or convention | Golden reading | Alternative (as built) | Ruled out by |
|---|---|---|---|---|
| SF1 | "contribute" | the expected cost, no margin, load or expense | a 5 per cent margin: $1,250,000, same call | funding policy 3.1 and 3.5 (no provision for expenses, investment income, excess insurance or a margin); same call |
| SF2 | "claims first made against the trust that year" | Claims made 1 January to 31 December 2027 from incidents on or after each Transition Date | every Claim from 2027 incidents whenever made (occurrence): $12,625,971 | trust agreement 2.1 and 2.4, Schedule A (claims-made, retroactive date the Transition Date) |
| SF3 | "Claim" | all claim numbers of one incident, one Claim, first made at the earliest | each claim number apart: $1,243,001 | trust agreement 1.3; same call |
| SF4 | "Covered Clinician" | employed physicians and APCs in Schedule B jobs | residents and fellows counted (their Claims, rows and FTE): $1,250,154 | trust agreement 1.5; same call |
| SF5 | the cost of a Claim | indemnity and defence paid plus case reserves on its Covered Clinicians' rows | paid only $1,259,015 (same call); indemnity only $902,246 | funding policy 3.4 (indemnity and defence, paid and case reserves) |
| SF6 | the trend base year | the incident year | the year the Claim was made: $1,272,987 | funding policy 3.4 ("from the calendar year of its Medical Incident"); same call |
| SF7 | the experience the window is costed on | each entity's Claims and exposure from the month of its first disclosure settlement (a Claim made within 30 days) to December 2024, inside the 2016 to 2024 experience the trust holds | the whole 2016 to 2024 experience $961,261; 2017 to 2024 $1,024,269; 2020 to 2024 $1,251,953 (same call) | funding policy 3.1 ("as Claims against the System's clinicians will arise and be made in that year") with the asserted data fact: no Claim from an incident before its entity's start was made within 40 days, none within 30 days from any 2016 to 2018 incident, and from each start 25 to 43 a year per 1,000 covered FTE-years in every year from 2020 to 2025 with no trend (`regime.*`); 3.3 states what the trust holds and no sentence pools, weights or drops years |
| SF8 | the rating unit | each specialty class of Schedule B, the System's experience | all classes pooled $1,210,173 (same call); each entity on its own experience $1,259,592 (same call) | funding policy 3.3 ("rated by the specialty classes of Schedule B"); same call |
| SF9 | the exposure's start | each entity's Transition Date | every entity from 1 January: $2,713,397 | funding policy 3.2 ("month from the entity's Transition Date") and Schedule A |
| SF10 | a month's exposure within the month | held through the month's days | mid-month $1,296,821, month end $1,159,029, calendar-day $1,285,212 (same call); all at the month's first day $1,405,046 | the staffing plan's note ("budgeted covered FTE for each month, held through the month"); the others same call |
| SF11 | a Claim's class | the first-named Covered Clinician's payroll job in the incident month | the register's specialty text | Schedule B Note 2; converges on all 3,320 Claims (asserted) |
| SF12 | entities and classes | four entities, seven classes | none | the staffing plan covers every pair it plans (asserted) |
| SF13 | the day count | made on its received date; the Transition Date in; 31 December in | each one-day variant: $1,273,418 to $1,289,665 | trust agreement 1.3, 1.7, 2.1, 2.4; every variant same call |
| SF14 | rounding | once, to the nearest $250,000 from unrounded | rounding parts first | funding policy 3.6 and the prompt |
| SF15 | Claims with no indemnity | counted at their defence cost | left out: $1,237,416 | trust agreement 1.3 (a demand, request or suit is a Claim) and 3.4; same call |
| SF16 | the per-Claim limit | cannot bind inside the window | capped at $2,000,000 | the largest Claim made within a year since the starts is $1,333,702; the cap changes nothing (asserted) |
| SF17 | a Claim's claim numbers | amounts added | the later claim number alone: $1,280,847 | the register's amounts are per claim number (no repeated amount set, asserted); same call |
| SF18 | per-diem payroll rows | paid FTE at their shifts | dropped: $1,287,639 | funding policy 3.2 (paid FTE); same call |
| SF19 | a month in FTE-years | one twelfth, as each payroll month in the experience | days over 365: $1,285,212 | funding policy 3.2 (the experience's months); same call |
| SF20 | 2025 and 2026 incidents | outside the experience | 2025 added: $1,336,835 | funding policy 3.3 (the experience held runs to 2024); same call |
| SF21 | an escalated suit's date | the request's (the Claim's first making) | the suit's own date: $1,243,001 | trust agreement 1.3; same call (as SF3) |
| SF22 | the experience's job codes | both code sets of Schedule B | the 2020 code set's exposure under every Claim: $1,622,763 | Schedule B (both code sets listed) |
| SF23 | Ask A "open" | OPEN or REOPENED | OPEN alone | same answer (asserted) |
| SF24 | Ask A "how many" | one per incident | one per claim number | no incident holds two open claim numbers (asserted) |
| SF25 | Ask A "latest loss run" | the latest valuation, 30 September 2026 | Quillan's revision 1 of its June run, received last | its own header (valuation 30 June 2026, "replaces the run of 07/08/2026") |
| SF26 | Ask A "under its policies with the carrier it is leaving" | Claims from incidents on or after the expiring carrier's first term | every open Claim on the coverage line | the premium history (each term's carrier) and trust agreement 2.2 |
| SF27 | Ask A "our reserves on them" | the register's indemnity and defence reserves on our rows | with contracted rows | contracted rows carry no amounts; same answer (asserted) |
| SF28 | Ask B paid FTE | hours paid over 173.33 | hours over 2,080 / 12 | the dictionary ("173.33 hours a month at 1.0 FTE"); same answer (asserted) |
| SF29 | Ask B trainees | a worker holding a resident or fellow position that month | any 2026 month | same answer (asserted) |
| SF30 | Ask B "at the entity" | the entity of the cost centre charged | none ships | the HCM lines carry no other entity (asserted) |
| SF31 | each entity's start | the first incident month with a Claim made within 30 days of its incident | within 14 or 39 days; a quarter or six months later; the latest or the earliest start for every entity; whole incident years from 2019, 2020 or 2021: $1,251,953 to $1,283,204 | same call on all ten (asserted); no sentence dates the program |
| SF32 | development of the 2023 and 2024 incident years | none for the window | a tail on the recent years' Claim counts or costs | every delay the window can use (under 365 days) is in the extract for every incident to 31 December 2024 (made by 30 December 2025, 274 days before the valuation; asserted); 3.4 values each Claim as recorded |
| SF33 | the trend's end point | the Plan Year's cost level from the incident's calendar year | trended to mid-2027: $1,313,183 | funding policy 3.4; same call |
| SF34 | the rows valued | the Covered Clinicians' rows | every priced defendant row: $1,289,264 | funding policy 3.4 ("against its Covered Clinicians"); same call |
| SF35 | how finely cost follows the delay | each Claim's own delay | 3, 6 or 8 equal delay bins and Gaussian kernels of 5 to 40 days: $1,225,392 to $1,287,100 | same call (asserted); a kernel of 80 days $1,138,463 lands too |

## Ladder (built, claims seed 3006; checks.py asserts every line)

Every rung is a complete pipeline on the same literal estimand, on the whole 2016 to 2024 experience the trust holds
and on each entity's experience from its first disclosure settlement; ratios are to the golden, $1,281,536.

| Rung | Construction | Whole experience | Rounds | Since the starts | Rounds | Dies to |
|---|---|---|---|---|---|---|
| R0 | a year of the experience's cost per FTE-year by class on each entity's 2027 FTE-years (no window) | $16,793,397 | $16,750,000 | $12,625,971 | $12,750,000 | trust agreement 2.1 and 2.4: only Claims made in 2027 count |
| R1 | the window's expected count (each delay against each day's days left) at each class's average cost | $3,697,267 | $3,750,000 | $3,283,884 | $3,250,000 | the window's Claims are not the average Claim |
| R1m | the same at the 2016 to 2020 average | $5,012,645 | $5,000,000 | $4,258,778 | $4,250,000 | as R1 |
| R1p / R1a / R1t | at the pooled average / by allegation / by matter type (Claim or Suit) | $3,398,119 / $3,689,491 / $2,419,721 | $3,500,000 / $3,750,000 / $2,500,000 | $3,108,864 / $3,321,213 / $2,155,997 | $3,000,000 / $3,250,000 / $2,250,000 | neither field separates the settlements from the requests |
| R1g | at a lognormal class mean | $2,034,110 | $2,000,000 | $1,776,083 | $1,750,000 | the fitted mean is still all Claims' |
| R1y | at the average of the Claims made within a year | $782,973 | $750,000 | $890,646 | $1,000,000 | the window weights the weeks-old Claims far more than the months-old |
| R1c | at the average of the Claims made in the incident's calendar year | $989,262 | $1,000,000 | $1,061,731 | $1,000,000 | as R1y (since the starts it rounds elsewhere inside a bin) |
| R1w | each entity's count at its classes' average within the entity's window length | $754,114 | $750,000 | $957,515 | $1,000,000 | as R1y, entity by entity |
| F1 / F3 | log cost on log delay, by class / pooled | $2,456,194 / $2,222,142 | $2,500,000 / $2,250,000 | $3,923,977 / $3,899,748 | $4,000,000 / $4,000,000 | the cost falls and then rises with the delay |
| F2 | log cost on the delay, by class | $945,548 | $1,000,000 | $1,169,811 | $1,250,000 | on the whole experience as the step factor; since the starts a smooth curve that happens to land (both steps taken) |
| F4 / F5 / F6 | gamma GLM: class factors and log delay / delay; quadratic in the delay by class | $1,603,762 / $846,127 / $801,949 | $1,500,000 / $750,000 / $750,000 | $1,694,809 / $995,990 / $995,066 | $1,750,000 / $1,000,000 / $1,000,000 | as F1 |
| S2 | a quadratic in the delay on log cost, by class | $1,079,244 | $1,000,000 | $1,754,748 | $1,750,000 | as F1; on the whole experience two errors that offset inside a bin (recorded, not asserted) |
| B1 | half-year delay bands, each band's average cost on its window count | $815,943 | $750,000 | $1,045,033 | $1,000,000 | the first band mixes the weeks with the months (rounds elsewhere inside a bin) |
| R2 | the in-year cost share of a full year (prorated delay) on the FTE-years | $1,365,675 | $1,250,000 | $1,699,021 | $1,750,000 | a part year catches a share that falls faster than its length; on the whole experience its over-count of the part-year entities offsets the missing settlements and lands (two errors, recorded, not asserted) |
| R2b | the same-calendar-year cost share on the FTE-years | $1,645,452 | $1,750,000 | $1,630,648 | $1,750,000 | as R2 |
| R3 | the Claims shorter than the entity's window, full cost, per FTE-year | $1,778,739 | $1,750,000 | $2,048,586 | $2,000,000 | a late incident has days, not the whole window, to be made |
| Default | each Claim at its own cost against the exposure with its own delay left (the loss-weighted step factor) | $961,261 | $1,000,000 | $1,281,536 | $1,250,000 | the whole experience pools three years and four entities' first months without the settlements |
| Default by month | the same by whole months of delay at mid-month exposure (the re-audit's probe) | $970,859 | $1,000,000 | $1,296,821 | $1,250,000 | as the default |

The constructions that cost each Claim at its own delay on the experience since the starts converge in the golden's
bin (asserted): 30-day bands $1,278,605; bands at 30, 90, 180 and 365 days $1,293,688; at 90, 180 and 365
$1,286,160; quarters $1,269,078; at 120 and 365 $1,264,430; 3, 6 and 8 equal bins $1,225,392, $1,280,469 and
$1,280,236; Gaussian kernels of 5, 10, 20 and 40 days $1,280,060 to $1,287,100; a gamma spline in log delay by class
$1,289,863; with the classes pooled $1,210,173 to $1,261,042. Every start handling converges too (SF31): each
entity's first Claim within 30 days $1,281,536 (the golden), within 14 days $1,283,204, within 39 days $1,281,536; a
quarter later $1,262,928; six months later $1,267,027; the latest start (July 2019) for every entity $1,265,507; the
earliest (January 2019) for every entity $1,253,730; incident years from 2019 $1,253,730, from 2020 $1,251,953, from
2021 $1,262,442. The judge's round 3a variants stay in the bin: every priced defendant row valued $1,289,264, the
trend to mid-2027 $1,313,183, claim numbers unmerged $1,243,001, one pooled class $1,210,173, the $2,000,000 limit
applied $1,281,536.

- **Margins.** The golden sits $31,536 above the bin's centre and $93,464 below its upper edge. The default misses by
  $320,275 (1.28 bins) and rounds to $1,000,000; the nearest asserted route on the whole experience is the bands at
  120 and 365 days, $267,981 (1.07 bins) off; the nearest round 1 route since the starts is the gamma GLM linear in
  the delay, $285,546 (1.14 bins) off. Two routes on the whole experience offset two errors and sit inside a bin: R2
  in the golden's bin ($84,139 above) and S2 rounding to $1,000,000; since the starts, R1c and B1 round to
  $1,000,000 inside a bin, and F2 and an 80-day kernel land, both after both steps.
- **Sampling.** The golden's Poisson standard error is $65,916 (5.1 per cent; bootstrap $65,247) on the 2,288 Claims
  since the starts: one sigma either way, $1,215,620 to $1,347,452, rounds to $1,250,000 (asserted). 2,101 Claims
  carry the window; the largest carries 1.1 per cent of the golden, the ten largest 6.4 per cent (asserted).
- **Dominance.** The regime step (the default to the golden, $320,275) is 5.8 times the largest Layer 1 slip's effect
  (claims and exposure from July 2020 only, $55,538) and the cost step (the count route to the golden on the same
  experience, $2,002,348) 36.1 times, asserted.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | Claims first made in 2027 from incidents on or after each entity's Transition Date (trust agreement 2.1, Schedule A), members not yet observed included (2027 incidents), projected from the Claims against Covered Clinicians of incidents from each entity's first disclosure settlement to 31 December 2024, inside the 2016 to 2024 experience the trust holds (3.1, 3.3) |
| 2 | Unit of account | one Claim per incident (1.3); FTE per employee-month (3.2); the contribution in dollars at 2027 level |
| 3 | Attribution window | the Plan Year, 1 January to 31 December 2027 inclusive (1.7, 2.1, 2.4); a day off at either end moves the unrounded figure under 1 per cent, same call (SF13) |
| 4 | As-of dating | the register extract valued 30 September 2026 (3.4); one extract ships |
| 5 | Version basis | paid plus case reserves at the extract (3.4); no other register valuation ships |
| 6 | Denominator | covered paid FTE-years by class over the same entity-months, both job code sets (3.2, Schedule B); the 2020 set alone moves the call (SF22) |
| 7 | Weighting | each window Claim at its own cost, each entity's months from its start at full weight and none before; the class average, the within-a-year average, fitted curves and the whole-period pattern are the ladder's rungs |
| 8 | Window length | the experience from each entity's first disclosure settlement (January to July 2019) to December 2024 (3.1, 3.3, the regime facts); each entity's window from its Transition Date (Schedule A); every start handling same call (SF31) |
| 9 | Boundary inclusivity | "on or after the Retroactive Date" and "during the Plan Year", both inclusive on dates; one-day variants same call (SF13) |
| 10 | Rounding path | the contribution rounded once to the nearest $250,000 (3.6, the prompt); ask dollars to the thousand, FTE to one decimal |
| 11 | Tie-break | a Claim naming two Covered Clinicians takes the first-named's class (Note 2); the specialty text converges (SF11) |
| 12 | Maturity and censoring | every experience Claim made within 365 days of its incident is in the extract (incidents to 31 December 2024, made by 30 December 2025, extract 30 September 2026), asserted; the window needs no later delays and the 2023 and 2024 incident years no development (SF32) |
| 13 | Order of operations | trend per Claim before summing; merge claim numbers before measuring a delay; any order of the class and day sums gives one figure |
| 14 | Row order | the register's row order changes nothing (asserted over three shuffles) |
| 15 | Duplicate resolution | defendant rows sum within a claim number; claim numbers of one incident add (SF17, no repeated amount set) |
| 16 | Identity normalisation | the register's clinician ids are the payroll's employee ids (asserted every covered id found) |
| 17 | Netting against gross | indemnity and defence add; no recovery or negative amount (asserted) |
| 18 | Dimensional units | dollars at 2027 level; FTE-years (a payroll month one twelfth) |
| 19 | Code and status semantics | open, closed or reopened never changes a cost (paid plus reserve); job codes through Schedule B, both sets |
| 20 | Integerisation | none on the call; the expected count (68.38) moves under one-day variants (67.80 to 68.83) and is not stated as a graded figure |
| 21 | Clause scope | claims-made from each entity's own Transition Date (Schedule A); 2.2 keeps earlier incidents with the occurrence policies |
| 22 | Forward window contents | the staffing plan covers every month of 2027 for every entity and class it plans (asserted) |

## Literal reader

Every shipped sentence bearing on how the contribution is computed, and what each fixes:

- Prompt: "fund the expected cost of the claims first made against the trust that year, with each hospital and the
  medical group moving into the trust on the day its occurrence policy expires": the estimand and the forcing fact.
- Funding policy 3.1: the expected cost at the Plan Year's cost level of the Claims first made during the Plan Year,
  "as Claims against the System's clinicians will arise and be made in that year". 3.2: exposure in FTE-years; in the
  experience, the paid FTE in the payroll; in the Plan Year, the staffing plan's FTE by entity, class and month from
  the Transition Date. 3.3: the claims experience the trust holds is the Claims from 2016 to 2024 incidents against
  Covered Clinicians, rated by the specialty classes of Schedule B. 3.4: each Claim at paid plus case reserves on its
  Covered Clinicians' rows at 30 September 2026, trended at 5 per cent from its incident year. 3.5: no loadings. 3.6:
  rounded once. Section 2 splits the instalments by exposure share.
- Trust agreement 1.3 (one Claim per incident, made when first received; a request through the Early Resolution
  Program is a Claim), 1.5 (Covered Clinician), 1.6 and Schedule A (Transition Dates), 1.7 (the calendar Plan Year),
  2.1 and 2.4 (claims-made, incident on or after the Retroactive Date, nothing made after the Plan Year), 2.2 (earlier
  incidents stay with the occurrence policies), 2.3 (limits), Schedule B with Note 2 (classes, both code sets).
- The staffing plan's note: "budgeted covered FTE for each month, held through the month".

Executed word for word these give no estimator and no experience period: they fix the population, the window, how
exposure is measured, the data the trust holds, the rating unit and the valuation, and leave open which years of what
is held stand for 2027 and how the window's expected cost is drawn from them. The executions a literal reader builds
on the whole experience held all miss: its cost per FTE-year on the Plan Year's FTE-years (the window dropped)
$16,793,397; the window's expected count at each class's average valued Claim $3,697,267; each Claim at its own delay
against the days left $961,261. The golden needs two analyst's choices no sentence states: reading off the claim dates
that the settlements a first window catches began at each entity in 2019 and run steadily since, so that 3.1's Claims
as they will be made in 2027 are priced on each entity's experience from its start, and costing each window Claim at
its own delay (asserted as R3a and R3b). Nothing instructs the reverse either: no sentence pools, weights, credits or
drops a year (`R3c.no_weighting_sentence`).

## Oracles

None ships. No file states a 2027 cost, a share of Claims made within any period, a claims-made or step factor, a
report-lag table, a severity by lag, a fitted curve or the dates the disclosure settlements began; the funding policy
carries no worked example; the premium history prices occurrence cover.

Outside the pack, the generator's own parameters give the population truth (never shipped, `oracle.population_truth`
in `checks.py`): the expected cost of the 2027 window from the claims world's frequencies, report lags and cost
distributions at the 2027 cost level, every entity past its disclosure start, is $1,282,953 on 66.85 expected Claims.
The golden is 0.999 of it, inside one standard error and in the same bin; the default path is 0.75 of it. The
estimator and its experience period are right, not merely filed.

## Ask sheet

**Main call's declared row population:** the register's rows for incidents from 1 January 2016 to 31 December 2024
(every defendant row, open and closed; the claim dates of every row read for each entity's start), the legacy
payroll's rows from January 2016 to December 2024, Schedule B, the staffing plan, the trust agreement and the funding
policy. Ask A's organs are the premium history's carrier terms, the
carriers' loss runs and the notice log, none of which the call reads, and the coverage line's meaning, which the call
uses only to set contracted rows aside; Ask B's are the 2026 HCM pay lines, which the call never reads. Asserted: the
call recomputes to the dollar with the runs, the notices, the premium history, the HCM lines and both distractors
deleted, and the register's coverage line recoded to each incident's own carrier leaves the golden to the cent
(`R2.ask_devices_off_the_call`). No ask figure reads any rung of the call: the call's figure is the contribution alone.

**Ask A. For each entity, whether any of our open claims under its policies with the carrier it is leaving is missing
from that carrier's latest loss run and, if so, how many and our reserves on them** (4 answers, 4 counts, 4 reserve
totals; counts whole, reserves to the nearest thousand dollars). Golden: Tolliver Falls 1, $1,465,000; Alderwick 3,
$7,000; the medical group 4, $54,000; Brennick none.
- H18 home: the trust covers no incident before a Transition Date (trust agreement 2.1, 2.2), so every open matter
  under an expiring carrier's policies stays with that carrier; the reconciliation is the audit trail of the trust's
  retroactive boundary, and the call does not turn on it.
- Construction: open claims (OPEN or REOPENED) on each entity's coverage line, one per incident, from incidents on or
  after the first day of the expiring carrier's unbroken run of terms in the premium history, not found by insured
  reference on that carrier's run valued 30 September 2026 (claim numbers; RMN notice numbers through the notice log;
  a suit under its earlier claim number).
- Primary device (D2, an attribute at the wrong vintage): the claims system holds each entity's current programme line
  on every defendant row, carrier code first (QM-TFH on a 2018 Tolliver Falls suit), so the coverage line reads as
  "insured by Quillan" or "by Stoneleigh" on claims that Halberd's, Corrigan Lane's, Westerholm's or Tallis's
  occurrence policies insure. Those claims are on no run of the expiring carrier and read as missing. Open claims
  under a former carrier: Tolliver Falls 4, Alderwick 6, the medical group 11, Brennick 1 (at least one each,
  asserted). The tells sit in other files: the runs' own policy periods begin at each carrier's first term, the
  premium history dates every term's carrier, and the notice log names the carrier each notice went to. Nothing
  narrates the changes of carrier; the dictionary describes the field as "the entity insurance programme line the
  claims system holds for this defendant".
- Hazards: HA1 (D7) noticed matters carried under their RMN notice numbers; HA2 (D7, the prior-id chain) an escalated
  suit carried under its request's claim number; HA3 (D2) Quillan's revision 1 of its June run, received 9 October,
  after the September run of 6 October; HA4 (D3) Stoneleigh strips punctuation from references; HA5 (D5) claims naming
  only contracted clinicians carry the CONTRACT line and are insured by the clinicians' own groups.
- True gaps: claims received from Thursday 24 September 2026 go to the carriers in the 2 October report (Tolliver
  Falls 1, a demand on a December 2023 incident reserved at $1,465,000; Alderwick 2; the medical group 3), and two
  program requests settled in house were never reported (Alderwick's IR-2026-02574, the medical group's
  IR-2025-08954); Brennick has none, so "none" is a graded answer.
- Path (7 files, 14 columns): the register, the premium history, the two Quillan runs, the Stoneleigh run, the notice
  log, the data dictionary; `claim_no`, `incident_no`, `incident_date`, `prior_claim_no`, `status`, `coverage_line`,
  `indemnity_reserve`, `defense_reserve`, the runs' insured reference, policy period, named insured and valuation date,
  the premium history's carrier and term.
- Stops (asserted): S1, the cracker's (every open claim on the coverage line, every key right): 5 ($2,906,000), 9
  ($679,000), 15 ($961,000), 1 ($1,676,000); S2 (notice numbers unmatched): 5, 8, 22, 2; S3 (claim numbers matched one
  by one, suits not through their earlier number): Tolliver Falls 2 ($1,634,000), Alderwick 7 ($447,000), the medical
  group 15 ($1,099,000); S4 (the June revision read as latest): Tolliver Falls 5, Alderwick 13; S5 (by entity of care,
  contracted claims in): Tolliver Falls 2, Alderwick 10, Brennick 1.
- Lazy delta: S1 wrong on 8 of 8 figures and on the "none" answer.
- Realism: health systems move their clinician programmes between carriers on anniversaries; a claims system that
  holds a programme line per entity carries the current one on converted claims; a carrier converting a notice keeps
  its first reference; a corrected run re-sent after the next quarter's is routine.

**Ask B. The covered clinician FTE the payroll paid at each entity in July, August and September 2026** (12 figures,
FTE to one decimal). Golden: Tolliver Falls 188.6, 187.1, 188.0; Alderwick 464.5, 463.6, 465.4; the medical group
1,037.1, 1,036.8, 1,040.6; Brennick 105.5, 106.7, 108.2.
- H18 home: the staffing plan's 2027 FTE, the exposure the contribution is costed on, was built from these positions;
  the figures are the plan's starting point as the payroll paid it (an input's reconciliation), shown to the trustees
  beside the contribution; the call reads only the plan.
- Construction: the HCM lines for the three work months; covered job profiles through the crosswalk into Schedule B;
  the hours on every line of each covered position (regular, per-diem shifts, paid time off; stipend and leave lines
  carry none) over 173.33; the entity of the line's cost centre; a worker who holds a resident or fellow position that
  month is not a Covered Clinician (trust agreement 1.5), so the additional position he holds is left out.
- Primary device (D5, a category crossed by label): since the HCM go-live, residents and fellows in their later years
  hold an additional paid position for moonlighting shifts (0.2 FTE, nocturnist and after-hours profiles JP-20182,
  JP-20162 and JP-20191, pay group PHYS, at their own or a sister entity's cost centre); 18 such positions, 3 to 6 at
  every entity in every month (asserted). The crosswalk maps the profile to a covered code and the position looks like
  any attending's; the tell is the same worker id on a GME line in the same month, and the rule is 1.5. Nothing
  narrates moonlighting.
- Hazards: HB1 per-diem clinicians with fte 0.00 and their shifts on PDM lines; HB2 paid time off on its own line; HB3
  one line per earning code repeating the position's FTE (stipend and leave lines with no hours); HB4 unpaid leave;
  HB5 fellows' clinical-sounding profiles ("Physician, Cardiology Fellow") that the crosswalk maps to GME; HB6 part
  months for starters and leavers.
- Path (6 files, 11 columns): the HCM extract, the crosswalk, the cost centre directory, the trust agreement (1.5,
  Schedule B), the data dictionary, the extract log; `worker_id`, `position_id`, `work_month`, `earning_code`, `hours`,
  `fte`, `job_profile_code`, `job_profile`, `cost_centre`, the crosswalk's `legacy_job_code`, the directory's
  `entity_code`.
- Stops (asserted on all 12 figures unless stated): S1, the cracker's (moonlighting positions kept): 189.8, 188.3,
  189.2; 465.1, 464.2, 466.0; 1,037.7, 1,037.4, 1,041.2; 106.7, 107.9, 109.4. S2 (the fte column once a position): 11
  of 12 off. S3 (regular hours only): every figure 7 to 9 per cent low. S4 (the fte column on every line): every figure
  1.5 to 1.8 times. S5 (per-diem clinicians left out): every figure 1.1 to 4.3 FTE low.
- Lazy delta: S1 wrong on 12 of 12.
- Realism: residents moonlight on paid shifts, and an HCM pays them through an additional job under the shift's
  profile while the legacy payroll paid such shifts as an earning on the trainee's own job; per-diem physicians are
  paid by the shift with no scheduled FTE.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta (asserted as built) |
|---|---|---|---|
| HA1 notice references | carriers keep a noticed matter's first reference | Ask A | S2 against the golden: 5, 8, 22, 2 against 1, 3, 4, 0 |
| HA2 escalation chain | a suit after a request opens a new claim number | Ask A (and the call's merge, same call there) | S3: Tolliver Falls, Alderwick, the medical group |
| HA3 re-issued June run | Quillan corrected and re-sent its June valuation | Ask A | Tolliver Falls 1 to 5, Alderwick 3 to 13 |
| HA4 reference formats | the carriers' own formats | Ask A | every Stoneleigh match |
| HA5 contracted claims | the clinicians' own groups insure them | Ask A | Tolliver Falls 1 to 2, Alderwick 3 to 10, Brennick 0 to 1 |
| HB1 per-diem | shift pay with no scheduled FTE | Ask B | S5 on 12 of 12; S2 on 11 of 12 |
| HB2 paid time off | the 2026 HCM's line grain | Ask B | S3 on 12 of 12 |
| HB3 line grain | one line per earning code | Ask B | S4 on 12 of 12 |

**The cracker sheet.** The cracker filed the golden contribution, ran the hygiene battery (keys unique, exact
duplicates, every join from the register and the HCM lines matched, no fan-out, counts tied), read the dictionary and
executed every filed rule. Every ask row misses:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 4 counts and 4 reserve totals | open claims on each coverage line, one per incident, matched to the latest valuation by reference, notices through the log, suits through `prior_claim_no` | the coverage line holds the current programme on claims the former carriers insure | miss |
| Ask A, "none" for Brennick | as above | it has an open claim under its former carrier, so the cracker answers yes | miss |
| Ask B, 12 FTE figures | paid hours over 173.33 on every covered position by cost centre, per-diem by shifts, paid time off in, GME profiles out | residents' additional moonlighting positions sit under attending profiles | miss |
| Slide 2, the chart's 12 values | the same figures | as Ask B | miss |

The cracker keeps the "yes" for Tolliver Falls, Alderwick and the medical group, where a grader scores it apart
from the count, and slide 2's structure (a chart of each entity's FTE in the three months).

Mirror leakage: 15 per cent of the ask weight (the mirror, off the call on the whole experience, lands Ask A on S1 or
S4 and Ask B on S1 or S2, and keeps the same three "yes" answers and the chart's structure).

**Pair arithmetic.** Planning weights: recommendation and components 38 (the contribution 30, the two experience
components 8: the experience the trust holds, and the settlements' start in 2019 with the window costed from it),
instruction following 7, asks 55 over 27 criteria (Ask A 12, Ask B 12, slide 2's chart 3). The cracker keeps the
three "yes" answers and two chart criteria, 5 of 27: C = 38 + 7 + 10.2 = 55.2. The mirror, on the whole experience,
keeps the first component (r = 4), the three "yes" answers and one chart criterion: S = 4 + 7 + 8.1 = 19.1. A response that lands Ask A's carrier
eras keeps its 12 criteria, one that reads 1.5 at the person keeps Ask B's 12: each device carries its whole ask, and no
ask figure rides on the call.

Pair ceiling: 37.2

If the generated rubric folds each "whether" into its count, the cracker keeps only the chart's structure and the pair
falls to about 34; recomputed from the generated rubric when it exists.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| Trust agreement 1.3 (Claim) | 2, the trust's governing contract | one Claim per incident, first made at the earliest, program requests included | anything about delay or cost |
| Trust agreement 2.1, 2.4 and Schedule A | 2 | claims-made from each entity's Transition Date, nothing made after the Plan Year | how a window is priced |
| Funding policy 3.1 to 3.6 | 1, the trustees' policy | the estimand (Claims as they will arise and be made in the Plan Year), how exposure is measured, the experience the trust holds and its rating by class, valuation, trend, no loadings, rounding once | a start date, a break, a weighting or dropping of years, a severity, a delay, a curve, a development or tail factor |
| Schedule B | 2 | covered jobs and classes, both legacy code sets, class by the first-named clinician | FTE totals |
| The staffing plan's note | 3, Finance's plan | each month's FTE held through the month; per-diem at budgeted average FTE | how exposure is weighted |
| The data dictionary | 5, semantics only | each field's meaning; 173.33 hours a month at 1.0 FTE | any device, any route, any carrier change |

## Prompt

`prompt.txt`, 881 characters, `voice-check.py` PASS: the call with its unit and the forcing fact (each entity moving in
on its occurrence policy's expiry), the workbook with Ask A ("whether any ... and, if so", no presupposition, H23) and
Ask B (the FTE "the payroll paid", which fixes paid FTE against the position's scheduled FTE), the deck with slide 2's
chart named, and the rounding once at the close (the contribution to the nearest $250,000, a budget-scale figure the
trustees set). The call sentence is round 1's word for word; the entity and class breakdowns, which rode on the call,
are gone. Round 3b changes nothing in the prompt: the second layer lives in the register and the funding policy's WHAT.

## Build record

- Claims seed 3006 (`build.py`), from searches of seeds 3000 to 3699 on the round 3b claims world (583 measured; 142
  passed the six criteria: the golden at most a quarter-bin from the centre with one sigma inside, the whole-experience
  step factor a full bin off and rounding elsewhere, the count route a full bin off on either experience, every
  start handling and banded or kernel construction in the bin, the within-a-year route rounding elsewhere, and Ask A's
  facts: an open claim under a former carrier at every entity, "none" for one entity and missing claims for at least
  two). 3006 holds the fewest whole-experience routes in the golden's bin (R2 alone) with every start handling and
  every judge variant inside it; the fallbacks are 3564 (no whole-experience route in the bin, but S2 and R2 within
  $10,000 of the bin's edges) and 3442 and 3603 (nearer the centre, the month-end convention within $4,000 of the
  edge). The payroll world, documents and Ask B use their own fixed streams (seed 1301012).
- The call: $1,250,000 (unrounded $1,281,536; Poisson SE $65,916, bootstrap $65,247). Experience: 3,320 Claims on
  13,747.1 covered FTE-years held; 2,288 Claims on 9,330.0 FTE-years since the starts (Alderwick January 2019,
  Tolliver Falls April, the medical group May, Brennick July). Asks: A as above; B as above (unchanged).
- Gates at stage 3: `checks.py` 275 of 275 (the claims-process block: every start in 2019, no Claim within 40 days before one, Claims within 30 days every year after at a steady rate, every delay the window uses complete; the three-rules block R1 to R3c with the analyst test on the clean truth and on the pack; 37 of the 39 routes on the whole experience a full bin off and rounding elsewhere, the two that offset recorded; the 18 round 1 routes since the starts a full bin off, two more rounding elsewhere; 16 converging constructions and 10 start handlings in the bin; the judge's round 3a variants in the bin; one sigma (Poisson and bootstrap), dominance, the population-truth oracle; SF1 to SF35; the asks' stops, fairness and convergences; separation, distractor deletion, realism, H5, H9, H16); `verify.py` (its own code path, bundle only: the starts, the golden, the whole-experience default, both asks) matches every golden figure; two builds byte-identical (target/, golden/, metadata.json, figures.json, target.zip: 17 members, 2,713,865 bytes, sha256 710fb603268fb100550d4d4d360898c87cbaeda2a291d61f54bdc000dba4b337); `figures_check.py` exit 0 (38 figures); `precut.py` exit 0 (49 checks, 0 WARN); `voice-check.py` PASS (881 characters, the prompt unchanged); `leak.py --asof 2026-10-12` REVIEW with no LEAK (lines below); `guard.py validate` clean (185 cards), `heart` WARN (Lori against task129, an older build), `surface` one promoted pair (task102, on the card axes only, answered by the card's differentiation line); the scrub audit clean on target/ and golden/. Stage 4 (a fresh reader and a fresh judge on this cut) is the main session's.
- Leak review: REVIEW, no LEAK, one line per REVIEW:
  - Sweep 3, a write-up figure in the pack: the premium history's "$1,000,000 / $3,000,000" is each occurrence
    policy's per-claim and aggregate limit, not the whole-experience figure the write-up rejects; and the call's
    distinctive words in the agreement, the policy and the dictionary: those files name the trust and Corvane Health,
    and none states a contribution or any 2027 figure.
  - Sweep 4, stump-paragraph terms in the funding policy (experience, record, register, incident), the agreement
    (register, period, incident, programme) and the dictionary (register, period, incident, change, programme,
    history): each document's own terms for the register, the experience the trust holds, the July 2020 job-code
    change and the programme line; no sentence names the disclosure settlements, their start, a break or a choice
    of years (`R3c.no_sentence_names_the_start`, `R3c.no_weighting_sentence`).
  - Sweep 6, entity names beside numbers in the agreement's schedules, the Quillan runs, the staffing plan, the
    cost centre directory and the premium history: dates, policy numbers, job codes, claim amounts, FTE and
    premiums; none ranks the entities on the contribution.
  - Sweep 9, 2027 dates in the premium history: the end dates of the 2026 policy terms.

## Pre-ship check

1. Domain: the task is a professional liability actuary's pricing of a claims-made trust's first year, the expected
   cost of the Claims first made inside each entity's opening window, from the system's own report lags with each
   Claim's cost tied to its own lag, on the experience period that matches the claims handling the window will see;
   with another field's nouns the trigger, the retroactive dates, the disclosure settlements, the program requests and
   the late suits have nothing to attach to.
2. Real work, nothing planted: a defendant-grain register with escalations under new claim numbers and contracted rows
   unpriced, a legacy payroll across the July 2020 job codes with per-diem rows, dual appointments, transfers and
   unpaid leave, HCM pay lines at earning-code grain with residents' moonlighting positions, two carriers' runs in their
   own layouts with a June run re-issued after September's, a notice log, a premium history across a change of carrier
   at each entity; each from the system's or the carriers' own systems, none on the decisive steps (R2 asserted). The
   disclosure arm's start is the program's own roll-out, recorded only as the claim dates it produced.
3. The flips are analysis: the experience period the window inherits, read off the lag mix by incident year and
   entity, and each window Claim at its own cost against the exposure with its own delay left; every rule in the pack
   is read the same on both paths, and the window's truncation is on both.
4. The analyst test holds: the field's loss-weighted step factor on the whole experience files $1,000,000, the count
   route at the class average $3,750,000 on the whole experience and $3,250,000 since the starts, a within-a-year
   severity $750,000; only the experience since each entity's first settlement, each Claim at its own cost, files
   $1,250,000 (R3a on the clean truth, asserted).
5. One defensible answer: the policy files the WHAT (the estimand as Claims as they will be made in 2027, the data
   held), every fork row is asserted (SF1 to SF35), every start handling and converging construction rounds to
   $1,250,000, and one standard error either way does too.
6. No decoy: no file states a 2027 cost, a factor, a lag table, a curve or the program's dates; no memo, draft or voice
   argues a figure or a period; the two distractors are plain.
7. Nothing hidden and recovered: no certified figure pins the method or the period; the window is estimated on the
   record, and the generator's population truth agrees with the golden to 0.1 per cent.
8. A new lesson: a first claims-made window inherits the claims process in force when it opens, so a change in how
   quickly claims are made, unit by unit, sets the experience period (`guard.py heart` WARN, Lori against an older
   build only).

## Retired

task130 was retired on 2026-10-11 with its third architecture spent (`build-pipeline`, Retirement), and put back in
the author's wave 1 on 2026-10-12 as a fourth root ("re-root: retired"). Every card stays filed so none of the earlier
architectures is drawn again.

- v1 failed on the portal on 2026-10-10: both top models filed the golden.
- v2 failed on the portal on 2026-10-11, and its hardening loop 1 was a Template of task73's world ten at the clone
  pre-flight.
- v3, the regression-to-the-mean baseline (an untreated cohort selected the same way a year earlier, trended), was
  cracked by the in-house solver in round 1: it filed the golden $4,060 PMPM and every tier figure in about four
  minutes (proxy 100). The pins that closed v3's forks (the any-list Risk Tier, the cancelled RFP, the bid list's
  programme year) pointed at the method, and the renewal letter's plan totals verified the solver's claims netting.
- Hardening loop 1 measured every candidate deeper rung on the shipped pack and found none forced, fork-free and
  moving the call; the only levers left were planting a rung or deleting the pins that close forks.

## Tried and rejected

v1 (large-holder designation, failed on the portal), carried over:

- The blueprint's stated-memo architecture (a methodology memo fixing the holdings rows, the amendment semantics, the unit-by-filing-date rule, CUSIP repair and the denominator source): rejected because a strong solver implements every stated clause, so the bridge becomes a computation; its traps are kept only as lower rungs.
- Capital-markets ownership kept literally (13F holders, issuers, shares outstanding) under an accepted domain label: rejected, markets trading is outside Economics and none of the nine owns a vendor's crowding flag without a relabel a reviewer would not accept.
- Confidentially omitted holdings recovered from another public disclosure as the decisive rung: rejected on the clean-data test, the public returns are a filtered file whose repair hands the natural pipeline the answer (sole_data_defect yes).
- Denominator timing (dwellings or shares outstanding taken at a later date than the holdings) as the decisive rung: rejected on the clean-data test (a stale file whose repair collapses the task) and as a single-fact flip.
- Holders whose returns are not yet due completed from the title register: rejected, the incomplete feed is a suspect file under the clean-data test, and the register-to-titles route is a schema-visible two-hop join a strong solver takes.
- Double reporting under a non-exclusive holding definition: rejected, the regime text that makes both returns correct concedes the overlap, and dwelling-level returns are deduplicated by reference by default.
- Agent-filed returns and nominee title holders as the decisive rung: rejected as a lens swap, registrant against owner of the same dwellings on the same date.
- Employer concentration with PEO look-through as the re-skin: rejected, it drops the ownership scenario and co-employment look-through is textbook.
- Passive holders re-derived at a forward date around an index change: rejected, out-of-scope domain and textbook.
- The agency's takeovers evidenced by preventive annotations in the deed extract: rejected, the evidence would sit in the forward roll's own source.
- Settled large-holder takeovers as the clock's evidence: rejected, a back-test mismatch sends the solver to the ledger.
- The programme order naming the first-offer programme: rejected, a sentence in the document that defines the quantity sends every solver looking.
- A bridge from the raw lodged rows to the conformed total, and a bridge with one bar per kind of movement: rejected, free weight and a taxonomy fork.
- Round 1 (plain) landed v1's six-section answer: the agency's first-offer takeovers in a budget ledger with a 120-day clock recovered from settled deeds died because the solver audited the ledger for transfers unprompted.
- Hardening loop 1's pre-registered repair (re-key the ledger by expedient in a second file): rejected before building, it only hides a step the solver completed.
- Portal 2026-10-10, the hardened v1 (holders inscribed after 30 June rung): failed, both top models filed the golden seven sections. Any rung that is a record a diligent solver can find and join is solved; the certified-bulletin reproduction blessed the path instead of hiding it.

Re-root (v2):

- Staying in the large-holder world with a property-against-dwelling grain stump (undivided buildings counted as one return row but holding several flats): rejected, the judge's lens-swap example (rank by logo count when the decision needs seats) is this move, and a dwelling-grain return collapses it.
- Staying in the large-holder world with any further hidden record (a licence register for new blocks, an inheritance date, a section split): rejected, the portal solvers join every record they can reach.
- The tensioned-zone rent burden from a deposit register (stock against flow, rents indexed on each anniversary): rejected, the update rules would have to be filed and a filed rule is a computation; the stock-and-flow reading is also close to a semantic fork on "rent".
- A survival-curve stump on the whole TA population (length-biased stock, pooled leaving rate as the decoy): rejected after simulation, in near steady state the pooled rate and the duration-conditional forecast agree within 4 per cent on the TA total because the stock's slow leavers and the new entrants' fast leavers offset; and "last year's stock survival" lands within 3 per cent.
- The same survival stump on a closed cohort: rejected, the gap opens (12 per cent against a rate) but a survival curve is the textbook answer to a closed-cohort question and a strong solver fits one; it is kept as a wrong rung (R3) because the departures are rationed, not hazards.
- Tenter House filled in order of each household's first move out of emergency accommodation: rejected after simulation, the block's positions in the lists were left to chance and swung from front-heavy to back-heavy between seeds, so the call was an accident of the history; the 2023 longest-in-nightly-paid lettings rule makes the positions a property of the world.
- v2 as first shipped: the move-on order left unfiled and recoverable only from the lets log; replaced by a filed allocations scheme extract under the client's two-layer standard, which caps a method hidden and recovered from records. A scheme clause letting main-duty households also bid through HomeChoice was drafted and cut, because it opens a second exit route the plan does not count.

Hardening loop 1 (after the v2 portal failure, 2026-10-11):

- Portal 2026-10-11, v2 as shipped: failed; the reported model built the filed duty-date queue on the case record's need against the revised plan, took the accepted October lets out once and filed the golden 46 (0 / 7 / 20 / 19) at GBP 21,615. Once the order was filed, the queue was a computation.
- Ageing alone (the members' birthdays inside the window moving households between lists) as the decisive device: rejected after measurement on seeds 130 to 166, it moves two to four Tenter House households in six months and leaves a solver who freezes need on 30 September within one unit, often on the same total; kept as the second-level rung R6.
- Exact-size lists for households needing five or more as the decisive device: rejected, it is one filed sentence and a plan row away and moves only the four-bed count; kept as R8.
- Tenter House flats let on the case record's need (the record then stale for 27 per cent of the block): rejected, it fills the block with families in flats too small for them, which reads as a data defect; flats go on the need checked on the day, as a TA move would.
- Reassessing the record for every household near the front of a list before each round, so that a replay on the record reproduces every let: rejected before building, the lets log would then bless the record until the forward rounds broke it, the validated-record shape the client bans; the record is reassessed only for the household offered.
- Hardening loop 1 as built (the move-on lists on Part 3 need worked out from the household members on each round day, against a case record that lags it; 52 units against the record's 66): rejected at the clone pre-flight, reject tier (Template, Track B) against task73 world ten, whose stump is the same move (carry the class the household's record holds, when a filed rule re-derives it from the circumstances on file); task86's v2 first cut carried the same move (the bedroom standard applied with ages on the offer date) and both platform responses solved it on 2026-09-12. Its realism read (birth histories, working-day dates, the 56-day relief period, TA sizing and voids, procedure dating) was not repaired, since the device is spent. With rate-against-queue (v2) and record-against-re-derived-class (loop 1) both gone, the Tenter House queue world has no honest decisive device left that a filed rule does not turn into a computation; v2 is spent and task130 is re-rooted as architecture v3 in the same objective.

v3 build (2026-10-11):

- The first acuity score (claims dollars with pharmacy at full weight): rejected after measurement, specialty-drug members dominated every list and persistence came out only 1.1 to 1.5 times the golden, because a specialty regimen persists; the score now weights pharmacy at 0.2 of medical and the world carries the one-off medical episodes a top-of-plan list really holds (major surgery, stroke, post-acute stays, readmissions, longer cancer courses).
- Model noise keyed by a member's position on the list: rejected, the draft and the final list scored the same member differently; noise is keyed by member and year.
- Tiers from a rank on the rounded score: rejected, it tied at place 140; ranks use the unrounded score and the lists show one decimal, as the cover sheets say.
- Scores on nominal dollars: rejected, the 2024 and 2026 scores drifted apart with prices and the bid and final tiers stopped meaning the same acuity; dollars are restated to a 2023 base.
- Model noise salted with the world seed: rejected, the seed sweep and the build drew different lists; the salt is fixed (41730).
- Seeds 100000 and 102002: passed every gate but their tier baselines fell out of order (a lower tier costing more than a higher one in total), which a board reads as a broken model; seed 101005 kept.
- A tier total column in the workbook: rejected, Schedule C.2 forbids intermediate rounding and tier 4's unrounded total rounds to 2,630 against 2,629 from its rounded parts; the medical and pharmacy figures stand alone and Note 1 says why.
- R3b, R5b and R6c land within 5 per cent of the golden total: accepted rather than forced apart, they are the arithmetic of 18 against 24 months of trend, weights only, and two offsetting errors; each still misses the whole-dollar tier cells it touches.
- R4b equal to the golden in tier 3: accepted as structural, no tier-3 bid member left the plan during the year; checks.py reports it.
- The renewal letter restating Schedule C's member-month and incurred-date rules: cut, each convention is stated once, in Schedule C.
- Procedure lines carrying diagnoses drawn at random: replaced by procedure-appropriate diagnosis maps for outpatient surgery and hospital services.
- context_artifact register, asked for at the card update to clear filed_model's collision with task133: BLOCK ban.artifact against task131; redrawn to operations_log, the plan's claims and eligibility feeds the baseline is built on.

Repair 1 (2026-10-11):

- Seed 101005 under the rebuilt claims engine: bid tier 1 fell to 8 members and the tier baselines fell out of order at every acuity base from 2,200 to 2,500; a sweep of seeds 101000 to 101053 at four bases kept 101050 at 2,500, which passes every gate at all four.
- A simulation that started in January 2024: the 2024 selection year had a shallower history than 2026, so the bid's tier 1 shrank against the final's; the simulation starts in January 2023 as burn-in.
- A plan-wide medical PMPM near $425 under the first fee schedule: low for a school district plan; facility charges, consults and the commercial multiple (1.14 of the reference schedule) bring it to $468.
- Home health priced as a case rate: allowed ran above billed; it is priced per visit at a share of charges.
- A wrong-member claim drawn from any family member: it put PSA tests on women and deliveries on men; the wrong member is drawn from the same sex and age band.
- Birth-date corrections drawn freely: five-year changes no conversion produces; one digit of the year, on two-child families.
- Pharmacy pickups on the day a fill fell due: a Monday spike; pickups spread over five days on a weekday profile.
- A hepatitis C first visit dated the first of the month: a Sunday office visit; moved to the next business day, no graded figure moved.
- The duplicate assertion counting a wrong-member claim that was later voided as a second payment: the assertion reads only live claims.
- The first rebuild's programme pharmacy ($1,689.88) rounded with the persistence rung's ($1,690.46): centring now holds the programme figures a dollar clear of persistence's, and checks.py asserts no rung lands on either programme figure.
- Centring that let one pharmacy fill move 7 per cent: a fill now moves at most 2.5 per cent and a facility claim 4 per cent.
- The memo's "a transplant, a premature baby, a cancer course or an accident" and the chart title "pharmacy moves much less": false on this seed (no enrolled member had a transplant in 2026; tier pharmacy baselines run 0.29 to 3.18 times 2026); rewritten to the enrolled members' own 2026 and to "pharmacy moves both ways", both asserted.
- Implementation plan tables that opened with the role and the milestone: the guard's name reader joined cells into "Ellery Final", "Ellery Welcome", "Kelley Enrolment" and "Santiago Direct" (a BLOCK on two Ellerys); the tables open with the name and the date.
- Jessica Petty from the draw as outreach supervisor: a first-name WARN against task104; Edward Miller from the same draw.
- LibreOffice's /DocChecksum left as exported: it hashes the run clock and broke byte identity between rebuilds; it is recomputed over the pinned file.

Repair 2 (2026-10-11, the second reader's forks and signposts):

- Seed 101050 with pharmacy at 0.2 of medical in the score: pharmacy persisted (0.99 of its selection-year level in real terms), so carrying the enrolled members' own 2026 pharmacy forward landed a dollar from the golden programme pharmacy; the score now counts pharmacy at 0.4 of medical and the world carries one-off pharmacy (hepatitis C cures, G-CSF and capecitabine with chemotherapy, fixed-length venetoclax and adjuvant oral oncology, CMV prophylaxis after a transplant, teriparatide after a hip fracture, biologic starts with a loading dose, stops and switches, weight-loss GLP-1s started and stopped).
- Recital C's "no agreement was executed and Northcourt provided no services": read as certifying the untreated control; the recitals are now procurement history, and the untreated status follows from the cancelled RFP, the second RFP and the implementation plan's dates.
- One member carrying 26 to 31 per cent of each bid tier's medical, and one or two specialty-drug members 63 to 89 per cent of its pharmacy: a credibility argument for pooling; the new seed and score hold the largest member to 25 and 22 per cent.
- r2's first seed choice, 102002 with pharmacy at 0.75 of medical: chosen on a world before the sim's last incidence fixes and never rebuilt; superseded by a 160-seed sweep of score weights, pharmacy weights and tier splits on the final simulation.
- Seed 102016 (the sweep's first pick: pharmacy at 0.4, persistence 2.44 times the golden): its world let a spouse dropped at open enrolment come back after the employee had remarried, two spouses on person code 02 at once, and the PBM join refused it. The re-add now waits for no other spouse on the plan; that changes the random stream of any world where it bites, so 102016's world was redrawn and dropped, and 102037, whose world the guard leaves unchanged, was taken.
- Centring blind to the full-year-only rung: tier 4's pharmacy baseline and R4c rounded to the same $2,114; baseline cells are now centred off R4c's whole dollar on a part-year member's claim, which leaves R4c in place.

Repair 3 (2026-10-11, the third reader's forks on the main call):

- Repair 2's eligibility churn under lists drawn on the simulation's own coverage: RCV8692544 left on 31 October 2026 and was rehired from 1 March 2027, so he scored onto the final list at rank 18, Tier 1, while the eligibility file, cut at 28 February, ends his coverage in October and Tier 1 read 35 or 34; the model now scores only members the eligibility file of the run carries on the list's date (the administrator's file of the first of the month, through the day before), which leaves the RFP and draft lists as they were and takes RCV9058604 (Tier 4, an RFP list member) onto the final list in his place.
- Schedule C.1(e) as repair 2 left it ("a member's Risk Tier is the tier assigned to the member on the Final Enrolment List"): it gave the members on both lists their final tier for the RFP cohort's year too, a reading that moves every tier cell and the programme total by 3.3 per cent; C.1(e) now defines a Risk Tier as the tier the model places a member in when it draws a list.

Repair 4 (2026-10-11, the tuner's round targets):

- The tuner's round-value targets (each tier baseline aimed at a two-decimal value such as 3,017.30 and landing within 0.00002 of it, each 2026 PMPM moved onto a quarter-dollar such as 4,335.25): a confirming bell, since a solver printing full precision saw a figure come out exact only under the intended method; each graded figure now lands at an offset drawn for it from a seeded generator, clear of the cent grid, and a draw is kept only once it is built and every rung's and fork's programme total sits off that grid too (taking the cheapest tier combination in every draw left R2 within 0.0005 of $4,427.31 in both draws tried, so a draw now takes one of the thirty cheapest).

Hardening loop 1 (after v3 round 1, 2026-10-11):

- v3 round 1: the analog cohort's tier PMPM, trended and count-weighted, landed in four minutes. The in-house solver read the selection on 2026 claims as regression to the mean, took the cancelled RFP 2025-07 cohort as the untreated comparison (Schedule C.1(e)'s Risk Tier "when it draws a list", Recital B's cancellation before an award, the bid cover's proposed programme year), measured its April 2025 to March 2026 allowed PMPM in its RFP tiers (41, 30, 23, 46), trended it 24 months, weighted by the final list's 34, 37, 38 and 31 and filed $4,060 ($1,438 medical, $2,622 pharmacy) with every ask figure; its netting tied to the renewal letter's Exhibit 1 to the dollar on claims paid through 31 January 2027, which confirmed it for free.
- Exposure weighting as the next rung (C.1(i) rewritten so the Programme Baseline is expected claims over expected Member Months, each tier weighted by its members times their expected months): rejected after measurement. The analog's Member Months per member enrolled at its start (1 April 2025) run 11.28, 11.48, 11.00 and 11.48 by tier and move the total 0.05 per cent ($4,058.14); per listed member (10.73, 11.10, 11.00, 11.48) they move it 0.59 per cent ($4,036.04). The effect is two dollars on the estimator a careful reader takes (every Enrolled Member is enrolled on 1 April 2027), the two estimators are a fork 0.54 per cent apart with no closure, and the count weighting it would replace is filed.
- Case-mix normalisation by age and sex (each analog tier indirectly standardised to the enrolled tier's ages in the Programme Year, the score being claims-only): rejected after measurement. Nothing in the pack forces it (C.1(h) takes a tier's experience from the members in that tier, and no clause or standard makes the unadjusted reading a violation), a consulting actuary's funding-rate letter carries no age and sex rating table, so the table is the solver's choice, and four defensible tables from the plan's own 2025 and 2026 experience move the total -3.56, -2.03, -1.20 and +0.18 per cent ($3,915.75, $3,977.78, $4,011.55, $4,067.64; raw and smoothed, by benefit and combined). The adjustment's size is the table, it is under 5 per cent in every reading, and the raw tables move the baseline away from the simulated truth ($4,348.19), not towards it.
- The analog's selection rule against the final list's (the top 140 of a different pool, cut into fixed score bands): rejected after measurement. The bid list's lowest score is 33.0 and the final list's 34.1, so tier 4 spans different bands; restricting the analog's tier 4 to the final list's floor (24 of 46 members) moves the total +1.39 per cent ($4,116.55), contradicts C.1(e) (a Risk Tier is the tier the model places a member in when it draws a list), and the gradient inside the band is noise (the analog's April 2025 to March 2026 allowed PMPM for tier-4 scores below 34.0, 34.0 to 34.4, 34.5 to 34.9 and 35.0 to 35.6: $2,056, $4,829, $2,143 and $2,840).
- Part of the analog treated by another programme: nothing in the world treats the bid cohort (no administrator or PBM programme reaches it in 2025-26), and adding one to make a rung bite would be a planted defect; not built.
- A bridge from the first two months after each selection year (the analog's January and February 2025 against the enrolled members' January and February 2027, as a ratio on the analog's year): rejected after measurement. It moves the total +8.98 per cent ($4,424.87) on tier ratios of 0.17 to 2.70, two months of a heavy-tailed cohort; nothing files it, and its medical half needs a completion factor for February 2027 that the renewal letter does not derive. The enrolled members' own January and February 2027 pharmacy, trended to the Programme Year's midpoint, runs 12.8 per cent above the golden programme pharmacy: a reading of C.1(h)'s "experience of members in that Risk Tier" the pack does not rule out, which any architecture that keeps this world has to close.
- Weakening the three pins that announce the analog as the hardening on its own: rejected, hardening by deletion. Each pin closes a fork (the comparator tier for the 20 members on both lists, the cohort's untreated status, the analog window), and the bid list in the folder still announces the analog to any solver who knows regression to the mean.
- Verdict: v3 is spent. With the analog construction forced and found, every deeper adjustment measured is optional with no shipped sentence the unadjusted reading violates (case mix, the bridge), contrary to a filed clause (the score floor) or worth two dollars (exposure); none moves the call by 5 per cent on a forced, fork-free path, and a plant is the only fix left. v3 is the number's third architecture, so the pipeline's cap retires task130 unless the author grants a fourth root.

Architecture 4 draw (2026-10-12):

- Draws weighed and not taken. A zone substation's peak after rooftop solar moves it into the evening: with
  half-hourly load and a solar profile in the pack, netting the two half-hour by half-hour is the solver's first move,
  so the default lands. A drought outlook whose evaporation scales with a shrinking lake's surface area: the planning
  scenario has to file evaporation as a depth to be deterministic, and a depth sends every solver to the area table.
  Bowel screening demand by prevalent and incident rounds: "first screen or repeat" is the first cut any screening
  analyst makes, and the colonoscopy yields of first-time and repeat attenders nearly cancel per invitation. Mortality
  after the end of a level term: the analog cohorts' post-level experience lands when it transfers, and a model is a
  fork when it does not. Fiscal drag under frozen thresholds: with taxpayer records in the pack the microsimulation is
  the first move. Increased limits factors after a minimum-limits change and leveraged trend in an excess layer:
  per-claim trending under the new limit or retention is the actuarial reflex. Override bias against a random
  low-side test: the decision reason code and the test's own description name the unbiased sample. Real-time data
  vintages and mixed flood populations: neither method is forced by the estimand, so both are forks. Group quarters
  in a cohort-change projection: the error moves only with the local cohort's size and stays a few per cent.
- Claims-made funding with one entity joining on 1 January: the decisive step collapses to one filter (the claims
  made in the same calendar year as their incident, costed on their own), which the coverage clause prompts and a
  careful solver writes in one line; the draw keeps the claims-made window but staggers the transitions on each
  entity's policy anniversary, so a part-year window catches a share of claims that falls faster than its length,
  and keeps the cost of each claim tied to how soon it is made.
- Card variants blocked at check: gap time with pattern E (test.same_puzzle and test.same_driver against task117,
  task37, task44, task97); gap population with pattern E (test.same_driver inside the window against task124's
  lineage); forcing event cutover_or_migration (it would have banned task180, drawn later today with that event).

Architecture 4 build (2026-10-12):

- Ask B as it stood at precut (each entity's covered FTE by specialty class, 22 cells): rejected at the build. The
  October movers moved only the hospitalist, emergency, family medicine and advanced practice cells, so the careful
  path that reads the home entity kept 14 of 22 cells; recast to one figure per entity, which the moves, the dual
  appointments and the earning-code lines all reach.
- Ask A worded "under its expiring policy": rejected before the build. An occurrence policy's last term covers only
  incidents since its last anniversary (Brennick's began on 1 October 2026, after the valuation), so the literal
  reading empties the ask; reworded "under its occurrence policies", the coverage line's programme.
- Early Resolution Program requests a median of six weeks after the incident: rejected after measurement. A part-year
  window then catches nearly the full-year share and the prorated full-year rung fell within 15 per cent of the golden
  for the six-month entity; requests come a median of about twelve weeks after.
- Escalation of 9 per cent of requests: rejected after measurement. The escalated suits carried most of the window's
  cost and the count at the average cost fell to 1.7 to 2.0 times the golden; 6.5 per cent keeps it above 2.
- Claims received, closed and noticed on any day of the week, and medical group incidents on weekends: rejected at the
  realism read of the first build (seed 5546). Risk management logs receipts on business days and the clinics see
  patients on weekdays; the seed search was re-run on the business-day world and 5546 was dropped.
- A claims transaction ledger and the Early Resolution Program's case log as separate files: not built. The ledger only
  splits paid amounts the register already carries, and the case log would mark the quick, cheap route as a population
  (a readable rung).
- Seed 843 ($480,000): dropped as a round headline total. Seeds whose rounded counts did not add to the rounded total
  count were passed over while one that adds was available.
- A check that no experience Claim exceeds the $2,000,000 limit: replaced by SF18, which asks only that no Claim able to
  be made inside the window reaches it. Seed 5546 carried a Claim valued above the limit at 2027 cost level, made more
  than a year after its incident, so a cap could not have moved its golden; on seed 3671 the largest Claim is
  $1,748,066.
- Ashgrove Medical Center as the flagship's name: renamed Alderwick Medical Center at the house-fix pass (H21), since an
  Ashgrove Medical Centre is a plausible real clinic name; the code AMC and every figure are unchanged.
- The trust's aggregate limit at $6,000,000: `leak.py` matched the medical group's Ask A reserve figure, $6,000, inside
  it; the aggregate is $4,000,000 (each Claim stays $2,000,000, so SF18 is unchanged).
- The forcing event `purchase_order_or_contract` (each entity's expiring policy): after the PAUSED commit's rebase,
  task127 v2 (drawn 2026-10-12, a lower number, so earlier in draw order) carried the same event and `guard.py check`
  blocked on `ban.forcing_event`; the card now names the trustees' November meeting (`vote_or_meeting`), which is what
  forces the call, and the check is back to WARN. No later-drawn build carries that event.

Round 2 and the author's decision (2026-10-14):

- Round 2 (PAUSED f44902f): the Early Resolution Program's class experience as the decisive step, $587,000; sent back by the judge, because funding policy 3.2's "the System's own claims experience" read literally gives the pooled $312,000 (a main-call fork) and two ask bases were left open; the author kept round 1 as shipped ($784,000) and every task130 file was restored to 9bf3cbc.
- The 10/10 audit's verdict on round 1: COMPLIANT_WEAK (domain, layers and the three rules hold, but the claim-by-claim lag truncation is close to a reflex once 3.1 to 3.4 are read and both asks were cracked by the judge unaided), from the audit file /tmp/claude-0/-home-user-real-world-data-extraction-conformation-etl-build-problems/98ff0d30-fbdb-590b-8f7a-decafc622b0e/scratchpad/audit/task130.md; its nine missing ## Three rules lines were added true to round 1.

Rule 3 rework (2026-10-15):

- Shipped design: decisive step read as rule application per the rule 3 audit, because funding policy 3.4 ("used as
  recorded ... no development or tail factor ... no distribution is fitted") eliminated every rival estimator and left
  the per-claim lag truncation as nearly the only admissible construction once 3.1 and agreement 2.1 and 2.4 were read,
  and 3.2's exposure sentence read as a cost-per-FTE-year recipe; measured on round 1's own world, a log-log severity
  curve landed 1.01 times its golden and the pooled lag share 0.99, so the cost carried no structure of its own and the
  window was the whole stump. 3.4 is cut back to valuation and trend, 3.2 defines the two exposures, 3.3 the
  experience period and its pooling within class.
- A costly early hump (the program's quick settlements dearer than its later ones) as the cost-by-lag structure:
  rejected on the prototype, the window's count at the class average fell to 1.2 to 1.7 times the golden and the
  golden's standard error rose to 9 to 11 per cent on the experience's size.
- Specialty timing alone (each class's lags its own, cost flat in the lag): rejected, a pooled construction landed
  within 2 to 4 per cent, so nothing but the class split decided.
- A clean step in cost at one lag: rejected, a gamma GLM linear in the lag landed 1.02 to 1.09 times the golden and a
  log-linear curve 1.08 to 1.15; a monotone curve fits a step.
- A cheap segment from patients who waive a claim at the prompt (very short lags, near nothing): rejected, a spline
  landed 0.89 and 90-day bands 1.09 to 1.11, both inside the bin at some seeds and outside at others.
- Program requests a median of six weeks to four months after the care: rejected, the prorated full-year share fell
  within 15 per cent of the golden; requests come a median of about eight months after, once treatment and bills are
  done.
- The experience at a smaller size (incidents from 2017, the establishment at 1.8 times round 1's): rejected, the
  golden's standard error was 6.5 to 7.5 per cent of it, too wide for one sigma to stay inside a $250,000 bin with
  room; the establishment is twice round 1's and the experience starts in 2016 (filed in 3.3): 6.0 per cent.
- Every pooled empirical build as a must-miss: rejected as infeasible, by linearity a construction that costs each
  Claim at its own lag lands within 6 to 8 per cent whether or not the classes are pooled, because each entity's class
  mix in 2027 is close to the experience's; the pooled builds of the frequency-severity reflex (a pooled average, a
  pooled curve) miss by a bin and more, and the filed pooling within class closes the rest (same call anyway).
- Escalation of 4.4 per cent of program requests: rejected after measurement, the escalation chain mishandled (each
  claim number its own Claim) moved the call a bin on some seeds (0.885 to 0.92 of the golden), a Layer 1 item carrying
  part of the stump; at 2.2 per cent it is neutral (0.94, asserted R2).
- Card strategy `composition_mix` for the new decisive step: blocked against task125 and it would have blocked task137;
  the strategy stays `maturity_censoring`, which still names the window's censoring.
- Forcing event `vote_or_meeting`: blocked against task128, whose later re-root carries it; `launch_or_rollout` (the
  trust's launch) blocks nothing on either side; Elizabeth Nelson and Jerome Warren, named in no shipped file, dropped
  for the same re-root's Elizabeth.
- The carriers' changes in 2018 at both Quillan entities and in 2020 at Brennick: rejected after measurement, Tolliver
  Falls and Brennick then held no open claim under a former carrier on most seeds, so the cracker would have kept their
  Ask A figures; moved to 2021 (Tolliver Falls) and 2022 (Brennick), Alderwick to 2019.
- Trust agreement 5.2 ("report every Claim ... to the carrier whose occurrence policy was in force on the date it
  occurred"): cut, a filed rule on Ask A's path that adjudicates its device; 2.2 keeps the occurrence policies' scope.
- The expected number of 2027 Claims (46.87) as a critical component: cut, the one-day day-count variants give 46.41
  and 47.22, so its whole number is not forced; the 2027 exposure total (1,105.75 FTE-years, a tie at one decimal) cut
  for the same reason; the goldens show months in the trust instead.
- Per-diem shifts on the regular salary earning code: an HCM pays shift work on its own code; PDM.
- Entity and class breakdowns of the call in the workbook and the ask list: cut, they rode on the call (the audit's
  22 coupled figures); the asks are now reconciliations the call does not reach.

Rule 3 rework, round 3b (2026-10-15):

- Round 3a: the dollar-weighted step factor lands the golden, per the rule 3 re-audit. The field's claims-made step
  factor on loss dollars, applied to the occurrence pure premium and convolved over each entity's days left, is the
  golden's own construction (the re-audit's monthly probe gave $1,263,621 on 3a's $1,263,838), so a strong solver
  landed 3a without seeing the lag-cost link; 3b keeps that construction as the default and adds the experience period
  as a second layer it misses by a bin.
- Claims seed 2077 (3a's) under the second layer: rejected, the golden $1,232,055 with every route right but Ask A
  answered yes at every entity, so "none" was no longer a graded answer.
- A larger world (the establishment scaled three to four times) to tighten the smaller post-start sample: rejected on
  the prototype, the golden's standard error in dollars grows with the square root of the scale, so a fixed $250,000
  bin holds one sigma less well; the disclosure settlements carry four fifths of the mean and nine tenths of the
  variance, so more and cheaper settlements (twice 3a's frequency at 0.41 of its cost) are what tighten it.
- Later starts (2020 and 2021 at the larger entities): rejected, the pooled-date constructions (incident years from
  2020 or 2021, the latest start for every entity) scattered 0.84 to 1.10 of the golden on the smaller post-start
  sample and incident years from 2019 took in a year of the old process; the starts sit between January and July
  2019 and every start handling lands within 3 per cent.
- The program's requests starting with the disclosure arm (no requests before each entity's start): rejected on the
  prototype, claim counts by incident year jump three to six fold at each start, a break any count by year shows, and
  the prorated full-year share on the whole experience still landed within 15 per cent of the golden; only the
  disclosure arm is staggered, the requests have run since 2015, and the change shows only in the lag mix.
- Requests later in the year (medians of nine to ten months, none before four) to push the prorated full-year share
  on the whole experience off the golden: rejected after four configurations, the share stayed within 5 per cent of the
  golden (its over-count of the part-year entities' requests is what offsets the pooled years' missing settlements)
  while the golden fell to $1.05 to $1.17 million and its error rose to 6 per cent.
- Every whole-experience route a full bin off: rejected as infeasible. With the pooled years at 0.75 of the golden, any
  round 1 route whose own error on that experience lies between 1.07 and 1.6 lands within a bin, and the round 1 routes
  fill that range (the quadratic on log cost 1.12, the prorated full-year share 1.42); they are recorded in the ladder
  as two errors that offset and never asserted to miss, and seed 3006 holds only the prorated share in the golden's
  bin.
- A programme or channel code on the register marking the disclosure settlements: rejected, the break would become a
  field reading (the call flipping on one code) and a column a schema test finds; the change lives only in the claim
  dates.
- Funding policy 3.3 "pooled within each specialty class" over 2016 to 2024: cut, it reads as an instruction to pool
  every year equally; 3.3 now says what the trust holds (2016 to 2024, rated by the classes of Schedule B), 3.1 files
  the estimand as the Claims as they will arise and be made in the Plan Year, and nothing instructs the reverse.
- Funding policy 3.2 "over the experience period": cut, it tied the exposure to the whole period held; 3.2 now says only
  how exposure is measured in the experience and in the Plan Year.
- The start read at 30 days alone: kept as the golden's reading with 14 and 39 days as constructions (they move one
  entity by a month and the call by under 0.2 per cent); 40 days or more would take in the earliest program requests,
  which are not the settlements.
