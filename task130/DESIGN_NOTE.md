# task130: Corvane Health, the first-year contribution to its professional liability trust (architecture 4, round 2)

Private, never ships. Architecture 4, drawn 2026-10-12 as the author's fourth root for a number retired with three
architectures spent (wave 1, "re-root: retired"); v1 to v3 are under `## Retired` and `## Tried and rejected`, and the
card keeps every dead identity in `lineage`. Round 1 of v4 shipped on 2026-10-12 (judge DETERMINISTIC, APPROVE, no
portal result). The 10/10 audit of 2026-10-14 found it compliant with the three rules but weak: its decisive step,
costing the claims-made window claim by claim and day by day, was visible (both claim dates are columns, the prompt
says "first made") and close to a reflex once funding policy 3.3 and 3.4 narrowed the method to the only computation
they allowed; the advertised default ($4,854,000) sat close to a misread of "first made"; both asks were cracked
unaided; 22 entity and class figures rode on the call.

Round 2 keeps the world, the estimand and the window, and moves the decisive step past the reflex. The window costed
day by day on the System's pooled experience, round 1's golden, is now the default path. The decisive step is the
claims process that window runs under: Corvane's Early Resolution Program has served only Tolliver Falls and
Alderwick (Stoneleigh adjusted the medical group's and Brennick's claims itself), and from each Transition Date every
entity's patients can come through it (trust agreement 5.2), so the window has to be costed on the experience of the
two hospitals that already ran it. The policy no longer narrows the method (3.4 now rates the entities alike, 3.5
says only that each Claim is taken as recorded), both asks carry silent devices, and the call's components are the
expected number of Claims and what each entity pays, which move only with the contribution.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task130.json`, architecture v4, round 2 updated in place on 2026-10-14 (the round 1 identity is in `lineage` as "v4 round 1"); `guard.py heart` WARN on one finding (answered below); `guard.py validate` clean |
| Domain / task type | actuarial-science-insurance / pricing-ratemaking-credibility (a client domain): funding a self-insured professional liability programme's first claims-made year is pricing its cover on experience adjusted to the claims handling it will run |
| Objective | Forecasting & Predictive Modeling: the expected cost of the claims that will first be made against a new trust in 2027, its first year, from the system's claims experience to 30 September 2026 |
| Shape | other: the contribution, the expected number of Claims and what each of the four entities pays toward it, the chart of each entity's expected cost by the month the Claims are made, and two reconciliation asks across the four entities (about 28 criteria) |
| Decision | `quantity_figure`, answer unit `currency`: the 2027 contribution the trustees put into the trust |
| Mechanism | gap population (decisive: which experience represents the Claims the window will see), then time (the claims-made opening window); pattern none; generators G13 (decisive: the decision window runs under a claims process the experience years saw at two of the four entities, inside a claims-made opening window) then G14 (does the pooled rate apply to this pool); Gate G `forecasting`; strategy `population_selection` (the experience population the window's rate is built on) |
| Layer 2 family / pattern | `field_method` (experience rating adjusted for a change in claims practice, in a claims-made exposure window); `own:claims-made-first-year-on-the-claims-process-the-trust-will-run` |
| Furniture | forum `trustees_or_governors` (the trust's board of trustees sets the contribution), forcing event `cutover_or_migration` (the trust goes live on 1 January 2027, when Tolliver Falls' occurrence policy expires and its clinicians move onto it; the contribution is fixed before that cutover, at the trustees' November meeting; moved at round 2 from `vote_or_meeting`, which task128 v3 now carries), organisation family `hospital_or_health_provider`, role family `compliance_or_audit`, context artifact `register`, calibration `none`, opening `question-first`, question form `how-much` |
| Spine | `clinician_fte_by_month_2016-01_2025-12.csv`, the legacy payroll, 121,415 rows: one employee's paid FTE in one month on one cost centre, with the job code (two code sets, the current one from July 2016), the cost centre's entity and status, January 2016 to December 2025; constructed. The 2026 HCM pay lines (16,439 rows) carry Ask B |
| Deliverables | `trust_funding_2027.xlsx` (the contribution, the expected Claims, what each entity pays, the cost by month made, the carrier loss run check, the September 2026 covered FTE), `trustees_paper_2027.pptx` (slide 1 the contribution and the payments, slide 2 the stacked chart of each entity's expected cost by the month the Claims are made) |
| People | drawn with `guard.py names --geo "United States" --seed 130`: Nancy Holland (vice president, risk management and insurance; the requester), Derek White (chief financial officer), Norma Hinton (director of claims and litigation; Lori Williams until round 2), Jerome Warren (consulting actuary), Walter Butler (chair of the trust's board of trustees); none appears in the prompt. Elizabeth Nelson, never named in the pack, was dropped at round 2 (task128 v3 drew the first name) |

**Guard.** `guard.py heart task130` on the round 2 card: WARN, one finding. `driver.near` (0.22) is this slot's own
round 1 driver in `lineage`: the world and the window are the same, and the decisive move differs (round 1 truncated the
report lag; round 2 prices the truncated window on the experience of the claims process it runs under). The
director of claims and litigation who signs the data dictionary was Lori Williams until `guard.py surface` blocked
the first name against task129; she is Norma Hinton, a fresh draw with no people finding.
Clearing the BLOCKs the first round 2 card met: G14 decisive repeated task124 (population, G14, forecasting) inside
the batch, G6 repeated task125 among the last three, and G12 would have blocked task133 v2's own checks
(population, G12, forecasting), so the decisive generator is G13, which no build within twelve either side carries
with this gap and Gate G; the older structural match with task98 v6 is answered by the card's differentiation line;
the forcing event moved off `vote_or_meeting` (task128 v3) to `cutover_or_migration`, which none of the three builds
on either side carries.

**Abstraction and same-puzzle tests.** Stripped of nouns, the driver is: a cover whose first window sees only the
events reported soon after they occur is priced on a history in which only some units ran the process that produces
those quick, cheap reports, while every unit runs it from the window's start; the window's cost is carried almost
entirely by the quick events only the process's units show, so the pooled history about halves it, and the process's
effect read over a full period of development, where it makes those units look cheaper, points the wrong way. The
nearest sibling insight is task501 v4 (a contact matrix rebuilt from the diaries kept in the season's own regime):
there the regime is a season of the same units and its effect has one sign; here it is a claims process carried to
units that never ran it, its effect reverses with the horizon (the Program hospitals cost 0.79 times the System per
FTE-year over full development and 1.88 times in the first window), and the quantity is a lag-truncated cost per day of
exposure. task136 (an intervention's increment carried to a new site as a multiple of the site's own rate) is the other
neighbour: here no unit's own rate can be scaled, since the medical group and Brennick have no early requests to
scale, and the trust rates every unit alike. Both lines are on the card.

**Data-native sentence.** Corvane's Early Resolution Program has met the Quillan hospitals' patients within weeks of
their care since September 2015 and turned their requests into quick, small settlements, while Stoneleigh's adjusters
handled the medical group's and Brennick's claims only when a demand or a suit arrived a year or more later; so the
System's 2017 to 2024 register holds 62 Claims made within 120 days of their incident, every one at Tolliver Falls or
Alderwick, and a first claims-made window, which can only catch Claims made that quickly, is priced on the medical
group's experience as if its patients had no Program, which from its Transition Date they will.

**World (as built, claims seed 1783).** Corvane Health, a nonprofit health system in western Oregon: three hospitals and
an employed medical group, 957.3 covered clinician FTE in September 2026 (employed physicians and advanced practice
clinicians in Schedule B jobs; residents, fellows, psychologists and contracted clinicians are not covered). Each entity
has insured its employed clinicians with a commercial occurrence policy on its own anniversary; the board resolved in
June 2026 to let each policy run to expiry and move the entity into the new Corvane Professional Liability Trust,
claims-made, with a retroactive date equal to its transition date:

- Tolliver Falls Hospital (106.9 covered FTE in September 2026), Quillan Mutual: trust from 1 January 2027.
- Alderwick Medical Center, the flagship (271.5), Quillan Mutual: trust from 1 April 2027.
- Corvane Medical Group, the clinics (525.0), Stoneleigh Casualty: trust from 1 July 2027.
- Brennick Community Hospital (53.9, affiliated 1 July 2019), Stoneleigh Casualty: trust from 1 October 2027.

Since September 2015 a patient of Tolliver Falls or Alderwick harmed by care can ask for compensation through the
Early Resolution Program: requests come a median of 90 days after the incident and mostly settle small, about one in
thirteen is declined and becomes a suit under a new claim number pointing back at the request, and the Program resolves
a quarter of the matters that would otherwise have come in later as demands or suits. Stoneleigh adjusts the medical
group's and Brennick's claims itself: there demands and suits arrive a median of about eighteen months after the
incident. The experience (incidents 2017 to 2024, valued 30 September 2026) holds 192 Claims against 6,553.3 covered
FTE-years: 123 at the Program hospitals on 2,655.2 FTE-years (62 made within 120 days, median cost $15,000, 15 per cent
of their cost; 22 made after a year, 46 per cent) and 69 at the medical group and Brennick on 3,898.2 (none within 120
days; 54 made after a year, 84 per cent). Built: the default path $312,000, the golden $587,000.

As-of date: the claims register extract runs Friday 2 October 2026, valued at 30 September 2026; payroll FTE runs
through September 2026; the trustees set the 2027 contribution at their meeting on Tuesday 10 November 2026, ahead of
the trust's go-live on 1 January 2027.

## Default path

The path a strong analyst takes once the claims-made window is seen (round 1's golden construction), every filed rule
read and applied:

1. Read the claims register extract (one row per named defendant), keep the rows of employed clinicians in Schedule B
   jobs, and collapse them to one Claim per incident, made on the date of its earliest claim number (trust agreement
   1.3), its cost the paid and reserves on its covered rows, trended at 5.0 per cent a year from the incident year to
   2027 (funding policy 3.2).
2. Take the incidents of 2017 to 2024 and the covered paid FTE-years of the same years from the legacy payroll, by
   specialty class (3.2, Schedule B).
3. Because the trust is claims-made from each entity's Transition Date (2.1, Schedule A), cost each entity's window day
   by day: each day's planned FTE (3.3) times the experience's trended cost per FTE-year of the Claims whose delay from
   incident to first making still lands by 31 December 2027, the experience taken across all four entities within each
   class, the same rate for every entity (3.4).
4. Add the entities.

Ends on: $312,000, the window costed day by day on the System's pooled 2017 to 2024 experience (5.6 expected Claims).
Golden: $587,000, the same window costed on the experience of Tolliver Falls and Alderwick, the two hospitals already
running the Early Resolution Program every entity's patients can use from its Transition Date (10.2 expected Claims).

## Stump sentence

A strong solver collapses the register to one Claim per incident, trends it, and costs each entity's claims-made window
day by day, every experience Claim counted where its own delay brings it in by 31 December 2027, on the System's pooled
2017 to 2024 experience by specialty class, and files $312,000 (Ends on); the step that lands it there is pricing the
window on experience in which the medical group's and Brennick's patients had no Early Resolution Program, when from
each Transition Date every entity's patients can come through it (trust agreement 5.2) and the window's cost is almost
all the quick requests that only Tolliver Falls' and Alderwick's experience shows: costed on those hospitals' experience
the contribution is $587,000.

## Three rules

- **Task type:** actuarial-science-insurance / pricing-ratemaking-credibility: pricing the first claims-made year of a
  self-insured professional liability trust, the task type the taxonomy tags for Forecasting.
- **Domain test:** the deciding quantity is the expected cost of the Claims first made inside each entity's claims-made
  opening window, a report-lag-truncated experience cost per day of covered clinician exposure by specialty class, which
  a professional liability actuary bases on experience generated under the claims handling the cover will run: the
  ratemaking adjustment for a change in claims practice, here the early resolution program every entity joins.
- **Swap:** rewritten as "how much should a water utility put into its new fund for 2027 to cover the main bursts
  first logged that year, each district moving in when its maintenance contract expires", the retroactive dates,
  report lags, early-offer requests, the program a district's patients gain at transition and the specialty classes
  have nothing to attach to: bursts are not reported months late through a resolution program, and the call stops
  making sense.
- **Layer 1:** a claims register at defendant grain (employed, resident and contracted clinicians in one extract, the
  contracted rows unpriced; a request that turns into a suit opens a new claim number pointing back; reopened claims
  keep their earlier closing date), written by the risk management claims system; a legacy payroll by employee, month
  and cost centre with job codes re-mapped in July 2016, dual appointments until the HCM go-live, transfers and
  Brennick's affiliation (payroll); HCM pay lines at earning-code grain with the worker's home entity on the record as
  it ran (HCM); two carriers' loss runs in their own layouts, listing the entities' own claims beside the clinicians',
  one re-issued for an earlier valuation (carriers); a notice log keyed by notice number (risk management). Each item
  mishandled the natural way leaves the call where it was (R2, asserted); none decides it.
- **Layer 2:** `field_method`, experience rating under a change in claims practice inside a claims-made window: the
  capable analyst costs the window claim by claim on the System's pooled experience; the expert sees that the window is
  carried by the early requests the Program produces, that the Program will run at every entity, and that only the
  Program hospitals' experience was generated under it.
- **Decisive step:** costing every entity's window on Tolliver Falls' and Alderwick's class experience (their Claims and
  their covered FTE-years), one rate per class for all four entities, instead of the System's pooled experience.
- **Not semantics:** every field and definition is read the same on both paths (the dictionary's matter type names the
  Program and the hospitals it serves; trust agreement 5.2 opens it to every entity), and the default reads them
  correctly; what flips the call is which experience generates the 2027 window's Claims, an estimation choice, never a
  reading of a field, code or unit.
- **Not rule application:** funding policy 3.1 to 3.7 and the trust agreement file the estimand, the experience's data,
  trend, exposure by day, one rate for every entity, the values as recorded and the rounding; none says which
  entities' experience to price on or that the Program changes the window's Claims, and executing every stated rule on
  the experience as a whole files $312,000.
- **Analyst test:** a strong analyst who dedupes the register, reads every filed rule and costs each entity's
  claims-made window claim by claim and day by day on the System's pooled experience files $312,000; adjusting for the
  Program by its full-year cost relativity files $273,000; the classic routes the audit measured file $3,617,000 (a
  mature year per FTE-year), $966,000 (the window's count at the average cost) and $466,000 (a full year's in-year share
  prorated); only the window on the Program hospitals' experience files $587,000.
- **Estimand:** funding policy 3.1 (the expected cost, at the Plan Year's cost level, of the Claims first made against
  the Trust during the Plan Year under the Trust Agreement), with trust agreement 1.3, 1.7, 2.1, 2.4, 5.2 and Schedule A
  (claims-made from each entity's Transition Date, the Program open to every entity from it) and funding policy 3.2 to
  3.4 (the experience's data, the plan's exposure by day, one rate for every entity); the 2027 Claims are unobserved and
  are the estimand.
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure argues a contribution or a basis; no
  file states a 2027 cost, a step factor, a lag table or a Program relativity; the Stoneleigh experience is the real
  record of how those claims were handled; the premium history is a declared distractor pricing occurrence cover.
- **No certified replay:** no certified or published figure is reproduced to recover the method; the window's cost is
  estimated directly from the register and the payroll, and nothing in the pack confirms either basis.
- **Lesson:** an early-offer program changes what a first claims-made year catches, so a trust that brings the program
  to new participants must price their opening window on the program's own experience, where the pooled experience
  halves the cost and the program's full-development saving points the wrong way; no build on file teaches pricing a
  claims-made window on the claims process the cover will run.

## Gate G

- **Litmus.** No. Every file is correct: the register, the payroll files, the staffing plan, the loss runs, the notice
  log, the trust agreement and the funding policy. No stakeholder states a number the task overturns, and no file
  states the trust's 2027 cost or a basis for it.
- **Primary mechanism:** `forecasting` (the correctly read past, every Claim's cost and delay and every year's FTE,
  does not pin the 2027 window: only the part of it generated under the claims process the window runs under does).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test.** On the simulation's own records (no mess, every filed rule applied) the window on the pooled
  experience files $312,000 and on the Program hospitals' experience $587,000 (R3a and R3b, asserted).
- **Deletion test.** Delete the two distractors, the loss runs, the notice log, the HCM lines and the dictionary: the
  call recomputes to the dollar (asserted) and the default path is still wrong. Nothing in the pack is wrong for the
  default to be wrong.
- **Lens swap.** The default and the golden are not one population at one moment under two lenses: they are two
  estimates of the same 2027 quantity from two experience populations, generated under two claims processes, and the
  golden needs each Claim's delay, cost and entity together with the payroll's exposure by entity.
- **No artifact ranks or prices the decision.** No shipped file states a 2027 cost, a claims-made or step factor, a
  report-lag table or a Program effect. The premium history ships as a plain distractor: it prices occurrence cover with
  the carriers' loads and no rung reads it.

## Readability screen

Six tests per rung: 1 a filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a reflex
of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction, ratio or
half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 claims-made recognised: only claims made in 2027 from incidents after each transition count | fires: the coverage clause and the prompt's "first made against the trust that year" | no | yes | no | no | the count share is a ratio | readable |
| R2 the window costed claim by claim, day by day, on the pooled experience (round 1's golden, now the default) | 3.3 earns exposure by day; 1.3 dates a Claim | both claim dates are columns | yes for a strong model (the audit's reading) | no | no | no | readable |
| L1 escalations merged into one Claim | 1.3 | prior claim number and incident number | yes | no | partly | no | readable |
| R3 (decisive) every entity's window costed on Tolliver Falls' and Alderwick's class experience, the claims process every entity runs from its Transition Date | no sentence ties the Program to a cost, a delay or the experience; 5.2 is a claims administration clause about patients' access, and the Program's history sits in the dictionary's definition of a matter type | no column names a route, a program or a regime; the entity column is ordinary | no: the reflexes pool the experience within class (3.4 rates the entities alike), segment by visible attributes or, once the Program is seen, adjust by a full-year relativity, which points the wrong way | none ships | no: every key, count and join ties on the pooled path | no: a re-basing of the window's rate on another experience population, by class and by day | silent |

The decisive rung is silent because its three facts live apart and none states the link: the Program's history is a
clause in a field definition, its extension is a claims administration clause, and the reason it decides the window
(the window catches only the quick, cheap requests the Program produces) shows only to a reader who looks at the
experience's delays by entity, which no rule, column or control asks for; the one adjustment an actuary reaches for
when a claims practice changes, a relativity read over full development, makes the call worse.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. `checks.py` asserts each row.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "fund the expected cost" | the expected cost of the Claims (funding policy 3.1), no margin, load or expense | the expected cost plus a margin or the trust's expenses | higher | funding policy 3.1 and 3.6 |
| SF2 | "claims first made against the trust that year" | Claims first made from 1 January to 31 December 2027 from incidents on or after the employing entity's Transition Date | claims from 2027 incidents whenever made (occurrence) | 4.86 times | trust agreement 2.1 and Schedule A: claims-made, the Retroactive Date is the Transition Date |
| SF3 | "claim" | all demands, requests and suits from one incident are one Claim, first made at the earliest | each claim number a claim | 0.48 times | trust agreement 1.3 |
| SF4 | a request made through the Early Resolution Program | a Claim | not a claim until a demand or suit | suits only 0.57 times | trust agreement 1.3(b) |
| SF5 | covered clinicians | employed physicians and advanced practice clinicians in Schedule B jobs | residents and fellows counted | 0.931 times | trust agreement 1.5 and Schedule B note 1 |
| SF6 | a Claim's cost | indemnity and defence paid plus case reserves on its covered clinicians' rows at the 30 September 2026 extract | paid only; indemnity only | moves | funding policy 3.2 |
| SF7 | trend | 5.0 per cent a year from the incident year to 2027 | from the year made | moves | funding policy 3.2 |
| SF8 | the experience years | incidents 2017 to 2024 | the latest years only | 2021 to 2024 only 1.107 times | funding policy 3.2 |
| SF9 | rating each entity | one expected cost per class for every entity's exposure | each entity on its own experience (0.800 times); each Program hospital on its own (1.062 times) | moves | funding policy 3.4: a Covered Clinician's exposure in a specialty class carries the same expected cost whichever Participating Entity employs the clinician |
| SF10 | exposure | the staffing plan's covered FTE by entity, class and month from the Transition Date, earned evenly over each day | from 1 January for every entity | 2.25 times | funding policy 3.3 |
| SF11 | the job code sets | both legacy code sets through Schedule B | the current code set alone | same call (C1: every experience month carries the July 2016 set) | asserted |
| SF12 | a Claim's specialty class | the first covered clinician's job in the incident month | the register's free-text specialty | same call (192 of 192 agree) | Schedule B note 2 |
| SF13 | "each entity" | the four Participating Entities of Schedule A | payroll entity codes | same call | Schedule A |
| SF14 | specialty classes | the seven classes of Schedule B | job families | same call | Schedule B |
| SF15 | Claims made on 31 December 2027 | in | out | moves | trust agreement 1.7 and 2.1 |
| SF16 | rounding | each figure rounded once from unrounded amounts; payments from the unrounded contribution | the sum of rounded parts; payments from the rounded contribution | same call (the rounded payments add to $587,000, and the rounded contribution gives the same payments) | funding policy 3.7 |
| SF17 | Claims without indemnity | counted at their cost | dropped | count 7.7 against 10.2 | trust agreement 1.3 |
| SF18 | the Trust's limit | no Claim able to be made inside the window reaches $2,000,000 at 2027 level (largest $1,489,000) | each Claim capped | same call | trust agreement 2.3 |
| SF19 | the day count | incidents from the Transition Date, each made on its incident date plus an experience Claim's delay, in when made by 31 December 2027, exposure earned evenly over each month's days | the days left counted with both ends; the delay counted with both ends; the Transition Date left out; the day before counted | $592,000; $582,000; $582,000; $592,000 | trust agreement 1.3, 1.7, 2.1, 2.2, 2.4 and Schedule A's note; funding policy 3.3 (each ruling sentence read from the shipped PDFs, asserted) |
| SF20 | a Claim's cost across its claim numbers | every claim number's rows added | the later claim number's rows alone | $585,000 | funding policy 3.2 with trust agreement 1.3 |
| SF21 | "how much of it each entity pays" | its share of the year's Contribution in proportion to its share of the 2027 exposure under 3.3 | its own expected cost; one quarterly instalment | every payment moves | funding policy section 2 |
| SF22 | "the expected number of those claims" | one per incident, the Claims of the window | claim numbers apart | 10.24 against 10.23, same at one decimal (the escalated suits fall outside the window) | trust agreement 1.3 |
| SF23 | a Claim's entity | where the care was given, the position its first clinician held (entity_at_incident) | the clinician's entity on another position that month | same call (every experience Claim's entity is one its first clinician was paid by that month) | asserted |
| SF24 | the Program's scope | open to every entity's patients from its Transition Date; until then Tolliver Falls' and Alderwick's | none (one reading) | n/a | trust agreement 5.2; the dictionary's matter type; the register (62 Claims made within 120 days, all at the two hospitals) |
| SF25 | Ask A, "open claims" | OPEN or REOPENED at 30 September 2026, one per incident | OPEN alone | same answer (asserted) | the register's status; no incident holds two open claim numbers (asserted) |
| SF26 | Ask A, "under its occurrence policies" | rows on the entity's own coverage line | every row of the entity's incidents, contracted ones included | same answer (asserted: each missing claim sits on its entity's line) | the dictionary's `coverage_line` |
| SF27 | Ask A, "its carrier's latest loss run" | the run with the latest valuation, 30 September 2026 | the most recently delivered file, Quillan's revision 1 of 30 June 2026 | Alderwick 4 ($75,000) | the runs' valuation dates and revision 1's header ("Revision 1 of the run valued 06/30/2026") |
| SF28 | Ask A, "our reserves on them" | the register's indemnity and defence reserves on our rows of the missing claims | the carrier's reserves | moves (the carrier holds no record of a missing claim) | "our" in the prompt; the register's reserve columns (asserted) |
| SF29 | Ask A, a carrier claim under a notice whose incident record holds no claim | the register claim with the notice's entity, event date and category, where exactly one exists | a notice-only file (the matter read as missing) | every entity moves (the careful path, S2) | asserted data fact: each such file matches exactly one register claim or none, the none being the entities' own claims the dictionary sends to the general liability register |
| SF30 | Ask B, "covered clinician FTE in September 2026" | one FTE per position held that month, covered through the crosswalk and Schedule B | FTE from the hours paid | same answer (asserted: no part month or unpaid leave in September, REG hours equal the FTE) | asserted |
| SF31 | Ask B, "each entity's" FTE | the entity of the cost centre a position's September lines are charged to | the home entity on the worker's record | every entity moves (S4) | asserted data facts: each September position has one cost centre; the home entity of two movers is Brennick's rural clinic, which the directory opens on 1 October 2026 |

The stump is none of these rows: every row is read the same way by a careful reader, and the default path reads them
all correctly. Pooled against Program-hospital experience is not a reading of any term: both are estimates of the same
filed estimand, and only one is generated under the claims handling the estimand's Claims will meet.

## Ladder (built, claims seed 1783; checks.py asserts every line)

Every rung is a complete pipeline on the same literal estimand; ratios are to the golden contribution, $587,072.

| Rung | Construction | Contribution | Ratio | Dies to |
|---|---|---|---|---|
| R0 | a year of the pooled experience's cost per FTE-year by class on each entity's FTE-years in the trust | $3,617,000 | 6.16 | the coverage clause: only Claims first made in 2027 count |
| R0m | the same on the mature years 2017 to 2020 | $4,738,000 | 8.07 | as R0 |
| R1a | the share of mature Claims made within twelve months at the mature cost | $2,369,000 | 4.04 | a December incident has days, not a year, to be made in 2027 |
| R1 | the window's expected count (by day) at the average trended cost | $966,000 | 1.65 | the Claims inside a short window are the cheap ones |
| R2 | a full year's cost-weighted in-year share, prorated | $466,000 | 0.79 | a part year catches a share that falls faster than its length |
| R2b | the same-calendar-year share | $432,000 | 0.74 | as R2 |
| Off-pack | a first-year step factor (0.30) on the mature cost | $1,422,000 | 2.42 | funding policy 3.2: the System's own experience |
| R3 default | the window costed day by day on the pooled experience | $312,000 | 0.53 | trust agreement 5.2: every entity's 2027 Claims come through the Program, whose experience only the two hospitals generated |
| Relativity | R3 adjusted by the Program hospitals' full-year cost relativity by class | $273,000 | 0.46 | as R3, and the full-year effect points the other way in a first window |
| By entity | each entity's window on its own experience | $470,000 | 0.80 | funding policy 3.4 (and 5.2 for the medical group and Brennick) |
| By carrier | Quillan entities on the Program experience, Stoneleigh entities on theirs | $433,000 | 0.74 | 3.4 and 5.2 |
| H1 | each Program hospital on its own experience, the medical group and Brennick on the Program experience | $623,000 | 1.06 | 3.4: one rate for every entity |
| H3 | the Program experience for the medical group and Brennick, the pooled for the hospitals | $405,000 | 0.69 | 3.4 and 5.2 |
| Mismatch | the Program hospitals' Claims over every entity's FTE-years | $305,000 | 0.52 | the experience's Claims and exposure from one population (3.2) |
| L0 | the golden basis with each claim number apart | $283,000 | 0.48 | trust agreement 1.3 |
| Program, classic | R0, R1, R2 and R2b on the Program hospitals' experience | $2,853,000; $1,221,000; $859,000; $955,000 | 4.86; 2.08; 1.46; 1.63 | as R0, R1 and R2 |
| R4 golden | the window costed day by day on Tolliver Falls' and Alderwick's class experience | $587,000 | 1 | none |

- **Position and margins.** The golden is bracketed: the classic rungs on either basis land above it, the default
  (the strong solver's round 1 construction) and every rival that keeps the medical group's and Brennick's experience
  land below it, and the relativity adjustment lands further below. Nearest named rival H1 at 6.2 per cent ($36,000,
  ruled out by 3.4); every other rival at least 20 per cent away.
- **Splitting the experience by delay.** The Program hospitals' Claims made within the window's reach (364 days) with
  the slower ones pooled converges on the golden exactly (C1: only those Claims can enter the window). Split below the
  reach, at 90, 120, 180, 270 or 330 days, it files $462,000, $475,000, $580,000, $590,000 and $589,000, each off the
  golden's bin (asserted) and each mixing Stoneleigh-era demands into a window every entity meets under the Program.
- **Grid.** Basis (pooled, Program hospitals) x window (mature, twelve months, full year prorated, by day) x weight
  (count at the average cost, each Claim's cost) x escalations (merged, apart) = 32 cells; every cell other than the
  golden is at least 20.7 per cent from it (nearest: the pooled basis, full year prorated, each Claim's cost, merged),
  asserted.
- **Worth on the graded figures.** The default moves the contribution, the expected count (5.6 against 10.2), every
  entity's payment and every entity's monthly cost on the chart.
- **Dominance.** The decisive correction applied to the default reaches the golden and moves it by $275,000 (47 per cent
  of the golden); every Layer 1 item is neutral to the call (R2); the filed-rule rung the default path already executes,
  escalations merged, would move it $304,000 on the right basis.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | Claims first made in 2027 from incidents on or after each entity's Transition Date (trust agreement 2.1, Schedule A); experience Claims from 2017 to 2024 incidents against covered clinicians; the 2027 Claims, not yet observed, are the estimand; filed literally |
| 2 | Unit of account | one Claim per incident (1.3); FTE per clinician-month (3.2); C1 on the count (SF22) |
| 3 | Attribution window | the Plan Year, Claims made 1 January to 31 December 2027 inclusive (1.7, 2.1, 2.4); one day off either end moves the rounded contribution against a filed sentence (C4, SF15, SF19) |
| 4 | As-of dating | the register extract valued 30 September 2026 (3.2); one extract ships |
| 5 | Version basis | paid plus case reserve at the extract (3.2, 3.5); no earlier register valuation ships |
| 6 | Denominator | covered paid FTE-years of the same entities as the Claims, by class, 2017 to 2024 (3.2); the mismatch rival (Program Claims over every entity's FTE) separated by 48 per cent (C4) |
| 7 | Weighting | each Claim at its own trended cost (the literal expected cost); count at the average cost separated (C4, 1.65 and 2.08 times) |
| 8 | Window length | the experience years are filed (3.2); each entity's plan window is filed (Schedule A, 3.3) |
| 9 | Boundary inclusivity | "on or after the Retroactive Date" and "during the Plan Year", both inclusive, counted on dates (SF19, asserted against the filed sentences) |
| 10 | Rounding path | rounded once from unrounded amounts (3.7); the payments' rounded sum equals the rounded contribution and the rounded contribution gives the same payments (SF16, asserted) |
| 11 | Tie-break | a Claim naming clinicians of two classes takes the first-named covered clinician's class (Schedule B note 2) |
| 12 | Maturity and censoring | every experience Claim made within 364 days of its incident is in the extract (incidents to 31 December 2024, extract 30 September 2026); asserted |
| 13 | Order of operations | trend per Claim before summing; merge escalations before measuring delay; the basis chosen before the window (C1 on the remaining orders) |
| 14 | Row order | the register's row order changes nothing (asserted) |
| 15 | Duplicate resolution | defendant rows collapse to one Claim by incident; claim numbers of one matter add, none repeating another's amounts (SF20) |
| 16 | Identity normalisation | clinician ids are payroll employee ids in both files (asserted) |
| 17 | Netting against gross | indemnity and defence add; no recovery exists (asserted no negative amount) |
| 18 | Dimensional units | dollars at the 2027 cost level; FTE-years |
| 19 | Code and status semantics | status never changes a cost (R2: reopened read as closed keeps the call); job codes through Schedule B, both sets (SF11, C1) |
| 20 | Integerisation | none: counts graded to one decimal, dollars to the nearest thousand |
| 21 | Clause scope | claims-made from each entity's own Transition Date (Schedule A); the Program from the same date (5.2); one rate for every entity (3.4) |
| 22 | Forward window contents | the staffing plan covers every month of 2027 for every entity (asserted) |

## Literal reader

Executed word for word, the prompt, the trust agreement (1.3, 1.5, 2.1, 2.2, 5.2, Schedules A and B) and the funding
policy (3.1 to 3.7) define the contribution as the expected cost, at 2027 cost level, of the Claims that will first be
made in 2027 under the Trust Agreement against clinicians of each entity from incidents on or after its Transition
Date, estimated from the System's 2017 to 2024 experience taken as recorded, on the staffing plan's FTE earned by day,
one rate per class for every entity. Every term in the fork table resolves to one reading or converges. No filed
sentence names the experience basis: 3.2 names the data the estimate is made from, and 3.1 says what is estimated, the
Claims as they will arise under the Trust Agreement, whose 5.2 opens the Program to every entity's patients; the
experience generated under that claims handling is the Program hospitals'. Pass on paper and on the built pack:
checks.py and the independent verifier (verify.py, its own code path from the bundle, reading the Program's hospitals
from the dictionary) both execute it to $587,000. The pooled estimate is not a second reading of a term but a biased
estimate of the same one: on the clean truth it files $312,000 (R3a), and no shipped sentence makes it the estimand.

## Oracles

None ships. No file states a 2027 cost, a share of Claims made within any period, a claims-made or step factor, a
report-lag or cost-lag table, a Program effect or the trust's expected Claims; the funding policy carries no worked
example; the premium history prices occurrence cover with carrier loads and ties to no rung. The carriers' loss runs
and the notice log carry the carriers' view of pre-transition matters (Ask A's path), which no rung of the call reads;
the HCM pay lines (Ask B's path) give 2026 FTE, which the call never reads (the staffing plan is the exposure).

## Ask sheet

**Main call's declared row population:** the register's rows for incidents from 1 January 2017 to 31 December 2024
(all defendant rows, open and closed), the legacy payroll's rows from January 2017 to December 2024, Schedule B, the
staffing plan, the trust agreement and the funding policy. Ask A's devices live in the notice log and the carriers'
loss runs and Ask B's in the 2026 HCM pay lines, none of which the call reads. Asserted: the call recomputes to the
dollar with the loss runs, the notice log, the HCM lines, the dictionary and both distractors deleted; the register
keeps every claim number of a duplicated matter on one incident number (the device row is the notice log's), so no
device or hazard row sits in the call's population; no ask figure reads any rung of the call.

**Ask A. For each entity, whether any of our open claims under its occurrence policies is missing from its carrier's
latest loss run and, if so, how many and our reserves on them** (4 counts with their "whether any", 4 reserve totals;
counts whole, reserves to the nearest thousand dollars). Golden: Tolliver Falls none; Alderwick 1, $7,000; the medical
group 1, $20,000; Brennick none.
- H18 home: every open claim from before a Transition Date stays with the expiring carrier (trust agreement 2.2 and
  5.3); the reconciliation is the audit trail of the trust's retroactive boundary, and the call does not turn on it.
- Construction: open claims at 30 September 2026 in the register under each entity's coverage line, one per incident,
  against the carrier's run with the latest valuation (30 September 2026), the carrier's insured reference matched to a
  claim number, or a notice number through the notice log.
- Primary device (D1, the same matter under two key schemes): a matter noticed to the carrier before any claim, whose
  claim risk management registered under a new incident record when it came in. The notice log keeps the incident number
  given at the notice, the register carries the new one on every claim number of the matter, and the carrier keeps the
  notice number as its reference. Matching through the notice log finds an incident record that holds no claim, and the
  register's open claim reads as missing. One at each entity: Tolliver Falls CL-2024-0060 (notice RMN-24-0002, $479,000
  reserved), Alderwick CL-2025-0071 (RMN-24-0088, $479,000), the medical group CL-2026-0045 (RMN-23-0075, $39,000),
  Brennick CL-2024-0079 (RMN-23-0011, $136,000).
- Silence: every key the careful path uses ties. Each carrier reference resolves to a claim number or a notice, each
  notice's incident number is a real record, and the notice files of Claim or Suit type that hold no clinician claim
  are normal on these runs: the claims against the entities alone (falls, nursing care, equipment), noticed first and
  carried by the same carriers, which the dictionary says are kept in the general liability register (38 such files on
  the September runs, at least one open at every entity). The only tell is a cross-file match of a notice's entity,
  event date and category with a register claim, which nothing invites. No sentence narrates the duplicate records.
- Fair: one handling reproduces the truth exactly: a carrier claim or suit under a notice number whose notice log
  incident record holds no register claim is the register claim with the notice's entity, incident date and allegation,
  where exactly one exists (asserted: 4 matched, 38 none, 0 ambiguous); the carrier's own date of loss and claim date
  corroborate it.
- Hazards: HA1 (D7, the prior chain): an escalated suit sits with the carrier under the request's claim number; HA2
  (D2): Quillan re-issued its 30 June 2026 run on 9 October 2026, after the 30 September run of 6 October; HA3 (D3):
  Stoneleigh strips punctuation from references; HA4 (D7): noticed matters carry notice numbers that only the notice log
  ties to an incident record (round 1's primary, now a hazard the careful path clears).
- True gaps: Alderwick's CL-2026-0049, a request handled in house and never reported; the medical group's CL-2026-0093,
  received on 29 September 2026 and so in the 2 October weekly report, after the run. Tolliver Falls and Brennick have
  none, so "none" is a graded answer there.
- Path (6 files, 13 columns): the register, the two Quillan runs, the Stoneleigh run, the notice log, the data
  dictionary; `claim_no`, `incident_no`, `prior_claim_no`, `status`, `coverage_line`, `entity_at_incident`,
  `incident_date`, `allegation`, the reserves, the runs' insured reference, claim type and valuation date, the notice
  log's incident number, entity, event date and category.
- Stops (asserted, each off on count and reserves): S1, claim numbers only: Tolliver Falls 2 ($1,681,000), Alderwick 3
  ($617,000), the medical group 9 ($494,000), Brennick 1 ($136,000); S1b, with the prior chain: 1 ($479,000), 3, 9, 1;
  S2, the careful path (notice numbers through the notice log, claim numbers grouped by incident): 1 ($479,000), 2
  ($486,000), 2 ($59,000), 1 ($136,000); S3, Quillan's re-issued June run read as the latest: Alderwick 4 ($75,000);
  answer: none, 1 ($7,000), 1 ($20,000), none.
- Lazy delta: S1 wrong on 8 of 8.
- Realism: hospital risk managers notice serious events to their carriers before any claim, a claims analyst who
  opens a fresh incident record for a demand rather than finding the noticed one is an everyday duplicate, and carriers
  keep the reference they were first given; hospital professional liability runs list the entity's own claims.

**Ask B. Each entity's covered clinician FTE in September 2026** (4 figures, FTE to one decimal). Golden: Tolliver Falls
106.9, Alderwick 271.5, the medical group 525.0, Brennick 53.9.
- H18 home: the staffing plan the contribution is costed on starts from these FTE; the figure is the audit trail of
  the plan's starting point (an input's reconciliation), and the call reads only the plan.
- Construction: the HCM pay lines for work month September 2026, one FTE per position, covered jobs through the HCM job
  profile crosswalk into Schedule B, on the entity of the cost centre each position's lines are charged to.
- Primary device (D2, an attribute at the wrong vintage): the HCM extract carries each worker's home entity from the
  HCM record as it stood when the extract ran on 2 October 2026; the ten clinicians who moved on 1 October 2026 (three
  Tolliver Falls hospitalists to Alderwick, two medical group family physicians to Brennick's new rural clinic, four
  Alderwick CRNAs to the medical group's surgery centre, a Brennick emergency physician to Tolliver Falls) carry their
  new entity on their September lines while the cost centres still charge the old. The dictionary defines the field as
  "The worker's home entity on their HCM record", with no date.
- Silence: since the HCM go-live on 1 January 2026 no clinician holds positions at two entities (the dual appointments
  closed into intercompany agreements), so the home entity and the cost centre's entity agree on every September line
  except the ten movers' (asserted); nothing invites the comparison, and a home entity read as the entity is the
  natural column.
- Hazards: HB1 (D6): one line per earning code, each repeating the position's FTE; HB2 (D5): fellows carry
  clinical-sounding profiles that the crosswalk maps to the excluded GME code; HB3 (D5): psychologists are paid in the
  APC pay group and are not covered.
- Path (6 files, 11 columns): the HCM extract, the crosswalk, Schedule B, the cost centre directory, the data
  dictionary, the extract log; `worker_id`, `position_id`, `work_month`, `earning_code`, `fte`, `job_profile_code`,
  `job_profile`, `cost_centre`, `home_entity`, the crosswalk's `legacy_job_code`, the directory's `entity_code`.
- Stops (asserted, every one off on all four unless stated): S1 (lines summed, home entity) 182.3, 466.3, 759.8,
  104.0; S4 (one FTE per position, home entity: the careful path) 105.7, 269.9, 527.2, 54.5; S3 (fellows read as
  specialists) moves Alderwick only, 281.5.
- Lazy delta: S1 wrong on 4 of 4.
- Realism: HR systems stamp the current organisation on historical lines in standard extracts, and an October
  reorganisation ahead of a January insurance transition is ordinary.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta (asserted as built) |
|---|---|---|---|
| HA1 prior chain | a suit after a request opens a new claim number | Ask A on the claim-number path | S1 against S1b: Tolliver Falls 2 against 1 |
| HA2 re-issued June run | Quillan corrected and re-sent its June valuation | Ask A | Alderwick 1 to 4 |
| HA3 reference formats | the carriers' own formats | Ask A | every Stoneleigh match |
| HA4 notice references | carriers keep the notice number | Ask A | S1 against S2 at every entity |
| HB1 earning-code lines | the 2026 HCM's line grain | Ask B | every figure (S1) |
| HB2 fellows | HCM profiles for trainees | Ask B | Alderwick, 271.5 to 281.5 |
| HB3 psychologists | the APC pay group | Ask B on a pay-group path | the medical group |

**The cracker sheet.** The cracker filed the golden contribution, ran the hygiene battery (keys unique, exact
duplicates, every join from the register matched, no fan-out, counts tied), used the notice log and the prior chain,
and executed every filed rule. Every ask row misses:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 4 counts (whether any, how many) | open register claims by incident, matched to the latest valuation on normalised claim numbers, the prior chain and notice numbers through the notice log | a noticed matter registered under a new incident record reads as missing at every entity: 1, 2, 2, 1 against none, 1, 1, none | miss |
| Ask A, 4 reserves | as above | the duplicated matters' reserves: $479,000, $486,000, $59,000, $136,000 against $0, $7,000, $20,000, $0 | miss |
| Ask B, 4 FTE figures | one FTE per position, fellows out through the crosswalk, by the line's home entity | the 1 October movers carry their new entity on September lines | miss |
| Slides | carried by the main call, scored with it | | outside |

If the generated rubric grades "whether any" apart from "how many", the cracker keeps Alderwick's and the medical
group's "yes" (2 of 12 Ask A criteria).

Mirror leakage: 12.5 per cent of the ask weight (the mirror stops at the default path, $312,000, answers both asks as
the cracker does and keeps only Alderwick's and the medical group's "yes").

**Pair arithmetic.** Planning weights 32 recommendation and components (the contribution, the expected Claims, the
four payments, the chart), 6 instruction following, 62 asks over 16 criteria (Ask A 12, Ask B 4), about 3.9 each. The
cracker on the call keeps the two "yes" criteria: C = 32 + 6 + 7.8 = 45.8; the mirror keeps r of about 4 (the files,
the slide structure, the method credit) and the same 7.8: S = 4 + 6 + 7.8 = 17.8.

Pair ceiling: 31.8

Assuming the strongest response also cracks the most obvious device (the home entity, Ask B's 4 criteria, 15.5): C =
61.3 and the pair with the mirror 39.5. If both top responses land the call and neither cracks a device, the pair is
45.8; if both land it and one cracks Ask B, 53.5, which needs the decisive step held by all but one response, which
the regime step is built for. Recomputed from the generated rubric when it exists.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| Trust agreement 1.3 (Claim) | 2, the trust's governing contract | one Claim per incident, first made at the earliest, Program requests included | anything about delay, cost or the Program's reach |
| Trust agreement 2.1 and Schedule A | 2 | claims-made from each entity's Transition Date | how a window is priced |
| Trust agreement 5.2 | 2 | the Early Resolution Program is open to every entity's patients from its Transition Date | the Program's history, its effect, or the experience to price on |
| Funding policy 3.1 to 3.7 | 1, the trustees' policy | the estimand under the Trust Agreement, the experience's data, trend, exposure by day, one rate for every entity, values as recorded, rounding | which entities' experience, delay, window share, step factors |
| Data dictionary, `matter_type` | 4, semantics | a Claim is a demand or a Program request; the Program has run for Tolliver Falls' and Alderwick's patients since September 2015 | anything about pricing |
| Schedule B | 2 | covered jobs and classes, both legacy code sets | FTE totals |

The Program's history (the dictionary) and its extension (5.2) sit in two documents, the layout fact apart from the
rule (`dataset-generation` 8.1); neither restates the other.

## Prompt

`prompt.txt`, 890 characters, `voice-check.py` PASS: the call with its unit and the forcing fact (each entity moving in
on its occurrence policy's expiry), the two files with what each holds, the components (the expected number of those
claims and how much of the contribution each entity pays), Ask A with "whether any ... and, if so" (no presupposition,
H23), Ask B, the chart's named parts and the rounding once at the close. Changed at round 2 only in the workbook's
components, from each entity's and each class's expected count and cost (22 figures riding on the call, all handed to
a response landing it, and the by-carrier rival landing two entities exactly) to the expected count and the payments.

## Build record

- Round 2, 2026-10-14. Claims seed 1783 (`build.py`), chosen from about 1,400 seeds swept on the round 2 world: the
  default at 0.70 of the golden or less (0.53); every named rival 6 per cent or more from the golden (H1 at 6.2, every
  other at 20 or more); the 32-cell grid at 6 per cent or more (20.7); the contribution and the count at least 15 per
  cent of a bin from a rounding edge (worst: the count at 16.7 per cent), each payment at least 12 per cent from an edge
  on the unrounded and the rounded contribution alike and the rounded payments adding to the rounded contribution; a
  contribution that is not within $1,500 of a multiple of $10,000; at least 110 Program hospital Claims (123); a
  duplicated incident record open at every entity; Ask A missing claims at one entity or more (two). The payroll world,
  documents and Ask B use their own fixed streams (seed 1301012).
- The call: $587,000 (unrounded $587,071.71), 10.2 expected Claims (10.233). Payments: Tolliver Falls $111,000 (113.4
  FTE-years, 18.9 per cent), Alderwick $201,000 (205.5, 34.3), the medical group $260,000 (265.4, 44.2), Brennick
  $15,000 (15.6, 2.6); 599.9 FTE-years. The chart's yearly totals: $183,000, $250,000, $149,000, $4,000.
- Asks: A as in the ask sheet; B 106.9, 271.5, 525.0, 53.9 (957.3 in all).
- Gates at stage 3: `checks.py` 182 of 182 (the three-rules block R1 to R3c, every rival route of the ladder and the
  audit, the 32-cell grid, SF1 to SF31, the asks' stops and devices, the separation line, the house fixes H5, H9 and
  H16); `verify.py` (its own path, bundle only, reading the Program's hospitals from the dictionary) matches every
  golden figure; two builds byte-identical with `target.zip`; `figures_check.py` exit 0; `precut.py` exit 0;
  `voice-check.py` PASS; `leak.py --asof 2026-10-12` REVIEW, no LEAK (lines answered below); `guard.py validate` clean,
  `heart` WARN (the slot's own round 1 driver only), `surface` 0 promoted pairs (nearest task73 at 0.100, not
  promoted).
- Leak review, one line per REVIEW:
  - Sweep 3, the call's words in the agreement, the policy and the dictionary: those files define the trust, its
    contribution and the register's fields; none states a cost, a basis or a 2027 figure. Two LEAKs at the first run
    (the agreement's $250,000 settlement consent and $4,000,000 aggregate matching the chart's yearly totals for
    Alderwick and Brennick in the write-up) were cleared by dropping those totals from block 4: the chart is graded on
    the slide, and the totals were not owed figures.
  - Sweep 4, stump-paragraph terms in the agreement, the policy and the dictionary (register, incident, system,
    report, exposure, experience, agreement, payroll, centre, family): the field's and the organisation's own nouns; no
    sentence names the experience basis, a delay or a window share. The two sentences carrying the decisive facts are
    trust agreement 5.2 (the Program open to every entity's patients from its Transition Date) and the dictionary's
    `matter_type` (the Program's history); neither names a cost, a rate or the experience to price on.
  - Sweep 6, entity names beside numbers in the agreement (Schedules A and B: dates, policy numbers, job codes), the
    staffing plan (FTE), the cost centre directory, the premium history and Quillan's runs (claim amounts): none ranks
    the entities on the contribution; the plan is the exposure the funding policy names.
  - Sweep 9, 2027 dates in the premium history: the end dates of the 2026 policy terms.
- Stage 4 (the reader and the judge) is the main session's; round 1's reports (`leak_check_report.md` from this run,
  `determinism_check_report.md` from round 1) stay as evidence until it runs.

## Pre-ship check

At stage 3 of round 2; the main session re-reads it against the reader's and the judge's reports.

1. Domain: the task is a professional liability actuary's funding of a claims-made trust's first year: the expected
   cost of the Claims first made inside each entity's opening window, on the experience generated under the claims
   handling the trust will run; with another field's nouns the retroactive dates, report lags, early-offer requests and
   specialty classes have nothing to attach to.
2. Real work, nothing planted: a claims register at defendant grain with escalations opening new claim numbers and
   contracted defendants unpriced; a legacy payroll by employee, month and cost centre across the July 2016 job codes,
   with dual appointments until the HCM go-live and Brennick's affiliation; HCM pay lines at earning-code grain with the
   home entity on the record as it ran; two carriers' loss runs carrying the entities' own claims, a June run re-issued
   after September's; a notice log keyed by notice number whose incident record a later claim no longer shares; each
   from the system's or the carriers' own systems, none on the decisive step, each neutral to the call (R2).
3. The flip is a method choice: which experience generates the 2027 window's Claims; every rule in the pack is read
   the same on both paths.
4. The analyst test holds: the window costed claim by claim on the System's pooled experience files $312,000, the
   Program's full-year relativity $273,000, the classic routes $3,617,000, $966,000 and $466,000; only the window on the
   Program hospitals' experience files $587,000.
5. One defensible answer: the agreement and the policy file the estimand (Claims first made in 2027 under the Trust
   Agreement from incidents on or after each Transition Date, at 2027 cost level, one rate per class for every entity),
   every fork row is asserted (SF1 to SF31), every rival is at least 6 per cent off and the grid at least 20.7 per cent.
6. No decoy: no file states a 2027 cost, a claims-made or step factor, a lag table or a Program effect; the premium
   history is a declared distractor; no memo, draft or voice argues for a figure or a basis.
7. Nothing hidden and recovered: no certified figure pins the method; the window's cost is estimated on the record.
8. A new lesson: an early-offer program changes what a first claims-made year catches, so the window is priced on the
   program's own experience, where the pooled experience halves it and the program's full-development saving points
   the wrong way (`guard.py heart` WARN on the slot's own round 1 driver only).

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

Round 2 (2026-10-14, after the 10/10 audit):

- Round 1 shipped design: weak per the 10/10 audit, because its decisive step, costing each entity's claims-made
  window claim by claim and day by day, was visible and near a reflex (the prompt says "first made", both claim dates
  are columns, and funding policy 3.3 and 3.4 narrowed the method to the one computation they allowed, so the judge
  expected strong models at $0.78 to $0.79 million); the advertised default ($4,854,000) sat close to a misread of
  "first made"; both asks were cracked unaided (RMN references beside a notice log; the home entity narrated as of the
  extract); and 22 entity and class figures rode on the call. Its golden construction is round 2's default path.
- Deepening the window itself (developing the open reserves, censoring the latest years, a fitted lag curve):
  rejected, each is an estimator choice the policy must either file, which makes it rule application, or leave open,
  which makes it a fork.
- Pooling across settings as the decisive step (each entity or each carrier on its own experience): rejected, a
  setting pool with no process to force it is a fork; kept as rivals the policy's one rate per class (3.4) rules out.
- Left truncation at Brennick's 2019 affiliation: rejected, it repeats task133 round 2's device (taken-over units
  counted only from the takeover).
- Seasonality of incidents and receipts inside the window: rejected, a calendar effect on a first window is small
  beside the window's own truncation, and building one in only to carry the call would be a plant.
- The Program's diversion of direct claims as the separating fact (the Program hospitals' requests added to every
  entity's own demands and suits): rejected as the decisive step, inside a first window the direct claims are few and
  the route split moves the call 0.94 to 1.10 times across eight seeds; the route is no column, and split at the window's
  reach (364 days) the experience converges on the golden. The diversion stays as the world's texture (a quarter).
- Seed 3671 (round 1's) under the Program regime: H1 (each Program hospital on its own experience) at 1.049 and the
  Program basis's step factor at 0.905; the seed search was re-run.
- Seeds 1120 and 1292, the first round 2 candidates: 1120's payments sat $26 and $31 from rounding edges; 1292's
  golden moved 2 per cent once reserves were capped at the policy limit (an open Program claim was reserved above
  $2,000,000 at 2027 level), leaving its payments on edges. 1783 kept.
- Reserves above the policy limit: adjusters reserve within the limits, so the generator caps an open claim's
  indemnity reserve at the limit at the incident's cost level; it moves only claims reserved above it.
- The July 2020 job-code remap: moved to July 2016, before the experience years. With the 2020 set alone (a natural
  mishandling) the pooled window landed near the golden (0.55 times 1.78), and Layer 1 mess must leave the call where
  it was (`dataset-generation` 7.1, R2); both code sets now converge (SF11).
- Ask B with the cross-entity dual appointments running into 2026: rejected, a clinician holding positions at two
  entities under one home entity shows any careful reader that the home entity is not the position's entity, which
  hands over the movers; the second positions close at the HCM go-live into intercompany agreements.
- Ask A's primary as two-hop escalation chains (request, demand, suit) with the carrier keeping the request's number:
  rejected, incident grouping clears it; the one-hop chain stays a hazard.
- Ask A's duplicated incident records without twins: rejected, the carriers' claim and suit files under notice
  numbers whose incident record holds no claim stood out; the entities' own claims (general liability), noticed and
  carried on the same runs, are now their benign twins, with at least one open at every entity.
- Ask A's duplicated incident records only from incidents outside the experience years: dropped, Brennick had no open
  matter to carry one on most seeds; the device row is the notice log's (the register keeps every claim number of the
  matter on one incident number, asserted), so the matters can sit in any year without a device row in the call's
  population.
- Grading each entity's expected cost (round 1's components): rejected, the by-carrier rival lands Tolliver Falls' and
  Alderwick's figures exactly; the components are the expected number of Claims and the payments, which move only
  with the contribution. The chart's yearly totals were dropped from the write-up after `leak.py` matched two of them
  to the agreement's $250,000 and $4,000,000.
- Card at round 2: G14 as the decisive generator blocked against task124 inside the batch, G6 against task125 among
  the last three, and G12 would have blocked task133 v2's own checks; G13 kept. The forcing event `vote_or_meeting`
  now repeats task128 v3 (re-rooted since, a lower number drawn the same day); `cutover_or_migration` (the trust goes
  live on 1 January 2027). Elizabeth Nelson, never named in the pack, dropped (task128 v3 drew the first name).
