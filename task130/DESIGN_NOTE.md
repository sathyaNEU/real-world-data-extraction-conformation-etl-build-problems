# task130: Corvane Health, the first-year contribution to its professional liability trust (architecture 4)

Private, never ships. Architecture 4, drawn 2026-10-12 as the author's fourth root for a number retired with three
architectures spent (wave 1, "re-root: retired"). v1 (a 2027 large-holder designation) and v2 (the Tenter House
replacement-unit call-off) failed on the portal; v2's hardening loop was a Template of task73 world ten at the clone
pre-flight; v3 (Red Cedar Valley's care-management baseline, regression to the mean against an untreated analog
cohort) was landed by the in-house solver in round 1 because its default construction, the analog, was the golden.
Their records are under `## Retired` and `## Tried and rejected`; the card keeps all four dead identities in
`lineage`. v3's generator, pack, goldens, write-up, metadata, prompt and its leak and clone reports were removed from
this folder at the re-root (in history at 15fab18); `solver_rounds/` stays as its evidence. Nothing of v3's world,
pack, prompt or asks is reused: v4 moves from a health plan's claims baseline to professional liability pricing, from
a selected cohort to a claims-made window, and from a school district to a health system.

Carried forward from v3's death, as design rules: the default path is written first and must end wrong on the data in
hand; no pin may point at the method; no figure in the pack confirms the solver's construction for free.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task130.json`, architecture v4, registered 2026-10-12; `guard.py check` WARN on one finding (`repeat.gate_g`, answered below); `guard.py validate` clean |
| Domain / task type | actuarial-science-insurance / pricing-ratemaking-credibility (a client domain): funding a self-insured professional liability programme is pricing its cover |
| Objective | Forecasting & Predictive Modeling: the expected cost of the claims that will first be made against a new trust in 2027, its first year, from the system's claims experience to 30 September 2026 |
| Shape | other (registered 02 at the DRAWN commit; task125, drawn minutes earlier today with a lower number and shape 02, then put 02 among this build's last two, so the card was moved before any design): the contribution and its two cuts, the expected number and cost of claims first made in 2027 for each of the four entities and for each of the seven specialty classes (one figure each way adds back to the contribution), 23 criteria before the chart and the asks; no period structure, no grid of cells (07 would block task180) and no percentile cut |
| Decision | `quantity_figure`, answer unit `currency`: the 2027 contribution the trustees put into the trust |
| Mechanism | gap time (decisive: the trust pays only for claims made inside its own opening window), then population (the claims a short window can catch are a cheap subset); pattern none; generators G13 (decisive: the horizon, the claims-made window against an annual incurred cost) then G14 (the cost of a claim conditioned on how soon it is made); Gate G `forecasting`; strategy `maturity_censoring` (the window truncates the report lag: only the claims made soon after their incident arrive in time) |
| Layer 2 family / pattern | `field_method` (exposure windows and report-lag development, the professional liability actuary's claims-made method); `own:claims-made-opening-window-cost-by-report-lag` |
| Furniture | forum `trustees_or_governors` (the trust's board of trustees sets its annual contribution), forcing event `vote_or_meeting` (the trustees fix the 2027 contribution at their 10 November 2026 meeting, funding policy section 2; registered `purchase_order_or_contract`, each expiring occurrence policy, until task127 v2 drew it the same day with a lower number), organisation family `hospital_or_health_provider`, role family `compliance_or_audit` (the system's risk management and insurance lead), context artifact `register` (the risk management claims register the stakeholder works from), calibration `none` (the system's own claims experience is the evidence, no organ), opening `question-first`, question form `how-much` |
| Spine | `clinician_fte_by_month_2016-01_2025-12.csv`, the legacy payroll, 114,499 rows: one employee's paid FTE in one month on one cost centre, with the job code (two code sets, the 2020 set from July 2020), entity and status payroll held that month, January 2016 to December 2025; constructed. The 2026 HCM pay lines (15,665 rows, January to September 2026) carry Ask B |
| Deliverables | `trust_funding_2027.xlsx` (the contribution with the expected Claims and cost by entity and by specialty class, the cost by month made, the carrier loss run check, the September 2026 covered FTE), `trustees_paper_2027.pptx` (slide 1 the contribution, slide 2 the stacked chart of each entity's expected cost by the month the Claims are made) |
| People | drawn with `guard.py names --geo "United States" --seed 130 --n 40`, skipping every name v3 used: Nancy Holland (vice president, risk management and insurance; the requester), Derek White (chief financial officer), Lori Williams (director of claims and litigation), Jerome Warren (consulting actuary), Elizabeth Nelson (director of the early resolution program), Walter Butler (chair of the trust's board of trustees); none appears in the prompt |

**Guard.** `guard.py check` on the scratch card: WARN, one finding (after the shape move, two: `repeat.gate_g` and `repeat.decision`, quantity_figure repeating task125: the call is one contribution in dollars, which is what the trustees set, and nothing else of task125's structure is shared). `repeat.gate_g` (forecasting repeats task124, one
of the last two builds in draw order): forecasting is the honest mechanism, because the contribution is a bet on the
claims that will be made in 2027 and the correctly read past (every claim's cost, every year's FTEs) pins it only
through the window the trust's cover defines. Bans run against task120, task121 and task124, the three builds drawn
before this one; a first draft blocked on `ban.artifact` (operations_log, task120), `ban.forum` (board_of_directors,
task124) and the structural tests against task102 and task501 v3. The artifact and forum were redrawn (`register`,
`trustees_or_governors`); the forcing event was moved off `cutover_or_migration` so that this card adds no block to
task180, drawn later today with that event; the structural tests are answered by the card's differentiation lines
(task102 moves payments across a period boundary by a release rule; task501 v3 sized a buffer on a cumulative path's
furthest overrun; neither costs a lag-truncated window claim by claim). Gap time with pattern E was tried and blocked
against four older builds (task117, task37, task44, task97); gap population with pattern E against task124's lineage.
Nearest driver on file 0.07 (task121 v3); task50 v4 at 0.06 (a slow-surfacing failure projected with a run-out law) is
the opposite move: there the unsurfaced part has to be added, here only the part surfaced inside the window counts.

**Abstraction and same-puzzle tests.** Stripped of nouns, the driver is: a cover that pays only for events that both
occur and are first reported inside its own window is costed from a full period's cost per unit of exposure, when
inside a short window only the events reported soon after they occur can count, and here those are the cheap ones;
the expected cost is the exposure at each point of the window times the cost of past events reported within the time
then left. The three nearest drivers (task121 v3, events set against the same unit's exposure at the same clock hours;
task93 v3, what raising a floor obliges a flat-rate unit to pay; task88, displaced full-rate demand on nights capacity
fills) share no latent structure, default path or correction with it. On the maturity family's record (task181: a
pooled reporting delay against each route's own, where the forecast needs the complete count), the move here runs the
other way: the decision is the truncated count, and its cost, never the complete one.

**Data-native sentence.** Corvane's early resolution program meets most patients harmed by care within weeks, with an
apology and a modest offer, and turns their requests into quick, small settlements, while the lawsuits that carry
most of the money are filed a year or more after the incident; so a trust that each hospital and the medical group
joins on its own policy's anniversary sees, in its first months, mostly the cheap early claims from a few months of
incidents, and almost none of the suits.

**World (as built, claims seed 3671).** Corvane Health, a nonprofit health system in western Oregon: three hospitals and
an employed medical group, 907.5 covered clinician FTE in September 2026 (employed physicians and advanced practice
clinicians in Schedule B jobs; residents, fellows, psychologists and contracted clinicians are not covered). Each entity
has insured its employed clinicians with a commercial occurrence policy on its own anniversary; the board resolved in
June 2026 to let each policy run to expiry and move the entity into the new Corvane Professional Liability Trust,
claims-made, with a retroactive date equal to its transition date (incidents before it stay with the occurrence policy
that was in force):

- Tolliver Falls Hospital (96.3 covered FTE in September 2026), Quillan Mutual: trust from 1 January 2027, the only
  full-year entity.
- Alderwick Medical Center, the flagship (234.3), Quillan Mutual: trust from 1 April 2027.
- Corvane Medical Group, the clinics (522.0), Stoneleigh Casualty: trust from 1 July 2027.
- Brennick Community Hospital (54.9, affiliated 1 July 2019), Stoneleigh Casualty: trust from 1 October 2027.

Seven specialty classes as Schedule B rates them. Since September 2015 a patient harmed by care can ask for
compensation through the Early Resolution Program: requests come a median of 82 days after the incident and mostly
settle small, and about one in thirteen is declined and becomes a suit (a median of 370 days after the request), which
risk management opens as a new claim number pointing back at the request; demand letters and suits that come in
directly arrive a median of about nineteen months after the incident (obstetrics about twenty-eight) and carry the large
indemnity payments. Risk management logs receipts, closings and notices on business days, and the medical group's
clinics see patients on weekdays. The experience (incidents 2017 to 2024, valued 30 September 2026) holds 328 Claims,
one per incident, against 6,188.6 covered FTE-years: the 159 made within 120 days of their incident have a median cost
of about $19,500 at 2027 cost level and carry 16 per cent of the experience's cost, while the 103 made more than a year
after carry 56 per cent. Built: the default path $4,854,000, the golden $784,000.

As-of date: the claims register extract runs Friday 2 October 2026, valued at 30 September 2026; payroll FTE runs
through September 2026; the trustees set the 2027 contribution at their meeting on Tuesday 10 November 2026.

## Default path

1. Read the claims register extract (one row per named defendant) and keep the rows for employed clinicians;
   collapse them to one claim per incident, summing each claim's paid indemnity, paid defence and case reserves.
2. Take incidents from 2017 onward, value each claim at paid plus reserve and trend it to 2027 at the funding
   policy's rate.
3. Sum the trended cost by specialty class, take each class's FTE-years of covered clinicians from the payroll file,
   and form each class's annual cost per FTE-year over 2017 to 2024 as recorded (funding policy 3.2 and 3.4).
4. Multiply by each entity's 2027 FTE by class for the months it is in the trust (twelve, nine, six, three) and add
   the four entities; spread each entity's cost evenly over its quarters for the emergence schedule.

Ends on: $4,854,000, a year of the experience's claims cost per FTE-year applied to each entity's FTE-years in the
trust (with the mature years 2017 to 2020 alone, $5,013,000).
Golden: $784,000, the cost of the claims made by 31 December 2027 from incidents after each entity's transition, each
past claim's trended cost counted for the share of the window's exposure from which it would have been made in time.

## Stump sentence

A competent solver collapses the register's defendant rows to one claim per incident, values and trends every claim
from 2017, takes the system's annual claims cost per clinician FTE-year by specialty class, applies it to each entity's
FTE-years in the trust and files a contribution of $4,854,000 (Ends on); the step that lands it there is costing the
trust's opening months as a mature year, when only the claims made by 31 December 2027 from incidents after each
entity's transition count, and those are mostly the quick, cheap requests: the golden is $784,000.

## Three rules

- **Domain test:** the deciding quantity is the expected cost of the claims first made inside a claims-made trust's
  opening window, built from each entity's covered clinician exposure through the system's own report-lag and
  cost-by-lag experience, which is how a professional liability actuary funds a first claims-made year; with another
  field's nouns the retroactive dates, report lags, early resolution settlements and specialty classes have nothing
  to attach to.
- **Analyst test:** a strong analyst who dedupes the register and reads the trust agreement and the funding policy
  correctly still multiplies a year's cost per FTE-year by each entity's FTE-years of cover ($4,854,000), or, having
  seen that the cover is claims-made, prices the expected number of claims made inside each window at the average
  claim cost ($1,784,000) or prorates a full calendar year's in-year cost share to each part year ($1,075,000); each is
  wrong, because inside a first claims-made window only the claims made quickly count, they cost a fraction of the
  average, and the share a part year catches falls faster than its length.
- **Layer 1:** a claims register with one row per named defendant (employed clinicians, residents and contracted
  clinicians in one extract, the contracted rows unpriced), claim stages that move (a request that becomes a suit is a
  new claim number pointing back at the request; a reopened claim keeps its earlier closing date); the legacy payroll
  by employee, month and cost centre with job codes re-mapped in July 2020 (both sets in Schedule B), dual
  appointments on two cost centres, transfers between entities and Brennick's July 2019 affiliation; the 2026 HCM pay
  lines at earning-code grain with the home entity stamped as of the extract; two carriers' loss runs in their own
  layouts, one re-issued for an earlier valuation after the latest. Each is something these systems produce; none
  decides the call.
- **Layer 2:** the shortcut is to cost the trust's first year as a mature year, or as a share of a mature year's
  claims at the average cost; the expert costs the claims-made window claim by claim, each past claim's trended cost
  counted for the share of the window's exposure from which it would have been made before the year ends, entity by
  entity from its own transition date.

## Gate G

- **Litmus.** No. Every file is correct: the claims register, the payroll files, the staffing plan, the carriers' loss
  runs, the trust agreement and the funding policy. No stakeholder states a number the task overturns, and no file
  states the trust's 2027 cost.
- **Primary mechanism:** `forecasting` (the correctly read past, every claim's cost and every year's FTE, does not pin
  the trust's first-year cost; the claims-made window does).
- **Flags:** `surface_read_dependency: no` · `stumping_family: analytical_non_defect` · `sole_data_defect: no`.
- **Clean-data test.** With a perfectly clean register (one row per Claim, every escalation already merged) and one
  payroll code set, a year's cost applied to the FTE-years is still the natural cost at 6.2 times the golden, and the
  count at the average cost is still 2.3 times it.
- **Deletion test.** Delete the two distractors (the patient safety event extract and the premium history), the
  carrier loss runs, the notice log and the HCM pay lines: the call recomputes to the dollar (asserted) and the default
  path is still wrong. Nothing in the pack is wrong for the default to be wrong.
- **Lens swap.** The default and the golden are not one population at one moment under two lenses: they are two
  different quantities (a mature year's claims, by incident, against the claims made inside each entity's first
  window), and the golden needs each claim's delay and cost together.
- **No artifact ranks or prices the decision.** No shipped file states a 2027 cost, a claims-made factor, a report-lag
  table or an industry step factor. The premium history ships as a plain distractor (`metadata.json`): it prices
  occurrence cover with the carriers' loads, which the funding policy (3.1, 3.5) does not fund, and no rung reads it.

## Readability screen

Six tests per rung: 1 filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a reflex
of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction, ratio or
half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1 claims-made recognised: only claims made in 2027 from incidents after each transition count, priced as the share of claims made in the window at the average claim cost | fires: the trust agreement's coverage clause and the prompt's "first made against the trust that year" send every reader to it | no | yes, once asked | no | no | the count share is a ratio | readable |
| R2 the cost-weighted share of a full year, prorated to each entity's months | no sentence prices a part year | no | partly: proration is the reflex for a part year | no | no | yes (one proration) | readable |
| L1 escalations merged (a program request and the suit that follows it are one claim, made at the request) | the claim definition says one claim per incident, first made at the earliest request | the register's prior claim field and incident number | yes, under the definition | no | partly | no | readable |
| R3 (decisive) each entity's window costed claim by claim: every experience claim's trended cost counted for the share of the entity's covered days from which its own delay would bring the claim in before 31 December 2027 | no sentence names the delay, the window share or the cost of early claims; the policy only pools the experience and fixes exposure by day | no column carries a claim's delay, a window share or a route; the register has no claim-source field | no: the reflexes are proration, the count share at the average cost, a step factor from memory, or a same-year filter | none ships | no | no: a convolution of each claim's delay against each entity's covered days, weighted by each claim's own cost | silent |

The decisive rung is silent because the two facts it joins live apart: the window is filed (coverage and transition
dates) and the cost of a claim is in the register, but the link between a claim's delay and its cost (the early
resolution program's quick, small settlements against the late, large suits) is named by no sentence, no column and
no file, and appears only to a reader who costs the window claim by claim instead of applying a rate.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. `checks.py` asserts each row (the
alternative computed and shown to move the call, or shown to converge).

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "contribute" | the expected cost of the claims (funding policy 3.1), no margin, load or expense | the expected cost plus a confidence margin or the trust's expenses | higher | funding policy 3.1 and 3.5: the Contribution is the expected cost; the trust's expenses are a separate budget line and no confidence margin applies in the first Plan Year |
| SF2 | "claims first made against the trust that year" | Claims first made from 1 January to 31 December 2027 arising from services on or after the employing entity's Transition Date | claims arising from 2027 incidents whenever made (occurrence) | the default family | trust agreement 2.1 and Schedule A: claims-made, the Retroactive Date is the Transition Date |
| SF3 | "claim" | all demands and requests arising from one incident, one Claim, first made at the earliest | each claim number (a program request and the suit after it as two) | lower (the escalated suit's cost leaves the window) | trust agreement 1.3: all Claims arising from the same incident are one Claim, first made on the date the earliest was made |
| SF4 | a request made through the early resolution program | a Claim | not a claim until a demand or suit | lower | trust agreement 1.3 names a request for compensation made through the Early Resolution Program as a Claim |
| SF5 | "covered clinician" | an employed physician or advanced practice clinician in a Schedule B job | every clinician on payroll, residents and fellows included; contracted clinicians | exposure and experience move | trust agreement 1.5 and Schedule B; residents, fellows and contracted clinicians are excluded by name |
| SF6 | a claim's cost | indemnity plus defence on its covered clinicians' rows, paid plus case reserve at the 30 September 2026 extract | paid only; indemnity only; every defendant row of the claim | lower or higher | funding policy 3.2 |
| SF7 | trend | 5.0 per cent a year compounded from the calendar year of the incident to 2027 | from the year the claim was made, closed or valued | moves every figure | funding policy 3.2 |
| SF8 | the experience | incidents 1 January 2017 to 31 December 2024 against clinicians covered on the incident date | all years in the register; the latest years only | moves | funding policy 3.2 |
| SF9 | pooling | within each specialty class, across years, months and entities, claims as recorded | by entity; by incident season; a fitted delay or cost curve | moves (noise) | funding policy 3.4 |
| SF10 | exposure | the staffing plan's covered FTE by entity, class and month from the Transition Date, earned evenly over each day of the month | from 1 January for every entity; mid-month timing; the September payroll | from 1 January 2.13 times; mid-month timing converges on the contribution (1.0009 times) and moves 7 of the 11 entity and class costs (asserted) | funding policy 3.3 |
| SF11 | base exposure | covered paid FTE in the legacy payroll, 2017 to 2024, each month's FTE one twelfth of an FTE-year | headcount; FTE of every job | moves | funding policy 3.2 and Schedule B |
| SF12 | a claim's specialty class | the class of the first covered clinician the claim names, from that clinician's job code in the month of the incident | the register's free-text specialty; the clinician's current job | converges (asserted: the two agree on every experience claim) | Schedule B note 2 |
| SF13 | "each entity" | the four Participating Entities of Schedule A | the payroll's entity codes, legacy cost-centre roll-ups | same call (the forecast reads only the staffing plan, by Participating Entity) | Schedule A |
| SF14 | "specialty class" | the seven classes of Schedule B | the payroll's job families | same call | Schedule B |
| SF15 | claims made on 31 December 2027 | in | out (the window closing a day early) | moves the contribution 0.8 per cent (asserted) | trust agreement 1.7 and 2.1: first made during the Plan Year, a calendar year |
| SF16 | rounding | each figure rounded once from unrounded parts; the contribution is the sum of the unrounded entity costs | the sum of rounded parts | converges (asserted: the sum of rounded entity costs equals the rounded contribution) | funding policy 3.6 |
| SF17 | claims closed or held without indemnity | Claims, counted at their cost (defence only, or nothing) | dropped | 110 experience Claims; the count falls from 11.5 to 8.6 and the cost moves (asserted) | trust agreement 1.3: a Claim is the demand or request, whatever it costs |
| SF18 | the Trust's limit | no cap reaches the window: the largest Claim that can be made within 364 days of its incident is $1,748,066 at 2027 cost level | each experience Claim capped at $2,000,000 | same call (asserted) | trust agreement 2.3 |

The stump is none of these rows: every row is read the same way by a careful reader, and the default path reads them
all correctly.

## Ladder (built, claims seed 3671; checks.py asserts every line)

Every rung is a complete pipeline on the same literal estimand; ratios are to the golden contribution, $783,667.

| Rung | Construction | Contribution | Ratio | Dies to |
|---|---|---|---|---|
| R0 default | a year of the experience's cost per FTE-year by class (2017 to 2024 as recorded) on each entity's FTE-years in the trust | $4,854,000 | 6.19 | the coverage clause: only claims first made in 2027 count |
| R0m | the same on the mature years 2017 to 2020 | $5,013,000 | 6.40 | as R0 |
| R1a | the share of mature claims made within twelve months, at the mature cost, on the FTE-years | $3,221,000 | 4.11 | a claim from a December incident has days, not a year, to be made in 2027 |
| R1 | the expected number of claims made inside each entity's window (claim by claim, by day) at the average trended cost of a claim | $1,784,000 | 2.28 | the claims inside a short window are the cheap ones |
| R2 | the cost-weighted in-year share of a full calendar year, on each entity's FTE-years | $1,075,000 | 1.37 | a part year catches a share that falls faster than its length |
| R2b | the cost of claims made in their incident's calendar year, per FTE-year, on each entity's FTE-years | $1,100,000 | 1.40 | as R2 |
| L0 (below) | the golden construction with each escalated suit kept apart from the request it follows | $378,000 | 0.48 | trust agreement 1.3: one Claim per incident, first made at the earliest request |
| Off-pack | a first-year step factor from memory (0.30) on the mature cost | $1,504,000 | 1.92 | funding policy 3.2: the System's own experience |
| Base FTE | the golden construction on the 2020 job codes alone | $1,314,000 | 1.68 | Schedule B lists both code sets |
| R3 golden | each entity's window costed claim by claim | $784,000 | 1 | none |

- **Position and margins.** The golden is bracketed: every rung that misses the window or the cost link lands above it
  (R0, R1a, R1, R2, R2b), the one Layer 1 slip that splits escalations lands below it (L0), and the off-pack step
  factor lands above it. The nearest rung is R2 at 1.37 times; no rung lands within 15 per cent (nearest 37 per cent).
- **By entity.** R2 is near exact for Tolliver Falls, the full-year entity (1.02 times its $227,000), and 1.27, 1.83 and
  3.96 times the golden for Alderwick, the medical group and Brennick; R0 is 4.5 to 15.7 times each entity's figure.
- **Grid.** Window (mature, twelve months, full year on the FTE-years, by day per entity) x weight (count at the average
  cost, each claim's cost) x escalations (merged, apart) x base FTE (both code sets, 2020 codes only) = 32 cells; every
  cell other than the golden is at least 19.3 per cent from it (nearest: by day, each claim's cost, escalations apart,
  2020 codes only, the two opposite errors), asserted.
- **Worth on the graded figures.** R0 and R2 move all four entity costs, R1 all seven class costs, L0 the contribution
  and every figure an escalation reaches (all 15 experience escalations were requests made within 364 days).
- **Dominance.** The decisive construction (R0 to the golden, $4,070,000) is 7.7 times the largest Layer 1 rung's effect
  on the contribution (the 2020 code set, $530,000), asserted.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | Claims first made in 2027 from services on or after each entity's Transition Date (trust agreement 2.1, Schedule A); experience claims from 2017 to 2024 incidents against covered clinicians; filed literally; members not yet observed (2027 claims) are the estimand, projected from the experience |
| 2 | Unit of account | one Claim per incident (trust agreement 1.3); FTE per clinician-month (funding policy 3.2); converge asserted on counts |
| 3 | Attribution window | the Plan Year, claims made 1 January to 31 December 2027 inclusive (trust agreement 1.7, 2.1); the window closing a day early moves the contribution 0.8 per cent (C4 against the sentences, asserted) |
| 4 | As-of dating | the register extract valued 30 September 2026 (funding policy 3.2); a single extract ships |
| 5 | Version basis | paid plus case reserve at the extract; no earlier valuation of the register ships |
| 6 | Denominator | covered paid FTE-years by class, 2017 to 2024, both job-code sets mapped (Schedule B); C4 against the 2020-only reading (asserted at least 6 per cent) |
| 7 | Weighting | each claim at its own trended cost (the literal expected cost of those claims); the count-at-average rung separated (C4, about 2.5 times) |
| 8 | Window length | the experience window is filed (2017 to 2024); the plan window per entity is filed (Schedule A) |
| 9 | Boundary inclusivity | "on or after the Retroactive Date" and "during the Plan Year", both inclusive; a day off at the year end moves the rounded contribution (C4 against the sentences, asserted) |
| 10 | Rounding path | each graded figure rounded once from unrounded parts (funding policy 3.6); sums of rounded entity costs equal the rounded contribution (asserted) |
| 11 | Tie-break | a claim naming two covered clinicians of different classes takes the first-named clinician's class (Schedule B note 2) |
| 12 | Maturity and censoring | every experience claim made within 365 days of its incident is in the extract (incidents to 31 December 2024, extract 30 September 2026); the window needs no later delays; asserted |
| 13 | Order of operations | trend per claim before summing; merge escalations before measuring delay; C1 on the remaining orders (asserted) |
| 14 | Row order | the register's row order changes nothing (asserted over three permutations) |
| 15 | Duplicate resolution | defendant rows collapse to one Claim by incident; reopened claims carry one row per defendant with their totals; asserted counts |
| 16 | Identity normalisation | clinician ids are payroll employee ids in both the register and payroll (no normalisation needed on the main path; asserted) |
| 17 | Netting against gross | indemnity and defence add; no salvage or recovery exists on clinician claims (asserted zero) |
| 18 | Dimensional units | dollars at the 2027 cost level; FTE-years; asserted in the generator |
| 19 | Code and status semantics | claim status (open, closed, reopened) never changes a cost (paid plus reserve); job codes through Schedule B |
| 20 | Integerisation | none: expected counts are graded to one decimal and costs to the nearest thousand |
| 21 | Clause scope | the claims-made coverage applies entity by entity from its own Transition Date (Schedule A) |
| 22 | Forward window contents | the staffing plan covers every month of 2027 for every entity from its Transition Date (asserted) |

## Literal reader

Executed word for word, the prompt, the trust agreement (1.3, 1.5, 2.1, Schedule A, Schedule B) and the funding policy
(3.1 to 3.6) define the contribution as the expected cost, at 2027 cost level, of the claims that will first be made in
2027 against clinicians of each entity from services on or after its Transition Date, projected within each class from
the 2017 to 2024 experience taken as a whole and used as recorded, on the staffing plan's FTE earned by day; every term
in the fork table resolves to one reading or converges, and the only computation those sentences license is to cost
each entity's window from the experience claim by claim, which is the golden. Pass on paper and on the built pack:
checks.py and the independent verifier (verify.py, its own code path from the bundle) both execute it to $784,000.

## Oracles

None ships. No file states a 2027 cost, a share of claims made within any period, a claims-made or step factor, a
report-lag or cost-lag table, or the trust's expected claims; the funding policy carries no worked example; the premium
history prices occurrence cover with carrier loads and ties to no rung. The carriers' loss runs and the notice log carry
the carriers' view of pre-transition matters (Ask A's path), which no rung of the main call reads; the HCM pay lines
(Ask B's path) give 2026 FTE, which the call never reads (the staffing plan is the exposure).

## Ask sheet

**Main call's declared row population:** the register's rows for incidents from 1 January 2017 to 31 December 2024
(all defendant rows, open and closed), the legacy payroll's rows from January 2017 to December 2024, Schedule B, the
staffing plan, the trust agreement and the funding policy. Ask A's devices live in the carriers' loss runs and the
notice log, which no rung of the call reads; Ask B's live in the 2026 HCM pay lines, which the call never reads.
Asserted: the call recomputes to the dollar with the loss runs, the notice log, the HCM lines and both distractors
deleted (zero device and hazard rows in its population), and no ask figure reads any rung of the call.

**Ask A. For each entity, whether any of our open claims under its occurrence policies is missing from its carrier's
latest loss run and, if so, how many and our reserves on them** (4 counts, 4 reserve totals; 8 figures; counts whole,
reserves to the nearest thousand dollars). Golden: Tolliver Falls none; Alderwick 2, $178,000; the medical group 1,
$6,000; Brennick none.
- H18 home: every open claim from before a Transition Date stays with the expiring carrier (trust agreement 2.2 and
  5.2); the reconciliation is the audit trail of the trust's retroactive boundary, and the call does not turn on it.
- Construction: open claims at 30 September 2026 in the register under each entity's coverage line, one per incident,
  against the carrier's run with the latest valuation (30 September 2026), matched on the carrier's insured reference.
- Primary device (D7, the true key elsewhere): risk management sends the carriers precautionary notices of serious
  incidents, and when a noticed incident turns into a claim the carrier keeps the notice number as its insured
  reference; those claims sit on the runs under RMN numbers, which only the notice log ties to an incident number.
  Matching on claim numbers reports every one of them missing. Open noticed claims: Tolliver Falls 5, Alderwick 6, the
  medical group 8, Brennick 2 (at least two each, asserted). Nothing in the pack says how the carriers reference them;
  the tell is a run row whose reference matches no claim number.
- Hazards: HA1 (D7, the prior-id chain): an escalated suit sits with the carrier under the request's claim number (open
  escalated suits: Alderwick 4, the medical group 2); HA2 (D2): Quillan re-issued its 30 June 2026 run on 9 October
  2026, after the 30 September run of 6 October, so the most recently delivered file is not the latest valuation; HA3
  (D3): Stoneleigh strips punctuation from references ("CL20190142").
- True gaps: a claim received from Thursday 24 September 2026 goes to the carrier in the 2 October weekly report and is
  on no run (Alderwick's CL-2026-0177, a request received 29 September), and two 2026 requests handled in house were
  never reported (Alderwick's CL-2026-0098 and the medical group's CL-2026-0133). Tolliver Falls and Brennick have none,
  so "none" is a graded answer.
- Path (6 files, 12 columns): the register, the two Quillan runs, the Stoneleigh run, the notice log, the data
  dictionary; `claim_no`, `incident_no`, `prior_claim_no`, `status`, `coverage_line`, `indemnity_reserve`,
  `defense_reserve`, the runs' insured reference, valuation date, named insured, carrier claim number and claim type.
- Stops (asserted): S1 natural (open claim numbers matched on normalised claim numbers, latest valuation): 5, 12, 11
  and 2 missing; S2 (S1 plus the prior chain): 5, 8, 9 and 2; S3 (every key right, Quillan's re-issued June run read as
  the latest): Tolliver Falls 3 ($472,000) and Alderwick 5 ($274,000); answer: 0, 2 ($178,000), 1 ($6,000), 0.
- Lazy delta: S1 wrong on 8 of 8.
- Realism: hospital risk managers send precautionary incident notices to their professional liability carriers, and a
  carrier converting a notice to a claim keeps the reference it was first given; a carrier's corrected run re-sent
  after the next quarter's is routine.

**Ask B. Each entity's covered clinician FTE in September 2026** (4 figures, FTE to one decimal). Golden: Tolliver Falls
96.3, Alderwick 234.3, the medical group 522.0, Brennick 54.9.
- H18 home: the staffing plan the contribution is costed on starts from these FTE; the figure is the audit trail of the
  plan's starting point (an input's reconciliation), and the call reads only the plan.
- Construction: the HCM pay lines for work month September 2026, one FTE per position, covered jobs through the HCM job
  profile crosswalk into Schedule B, on the entity of the cost centre each position's lines are charged to.
- Primary device (D2, an attribute read current): the HCM extract stamps every line with the worker's home entity as
  it stood when the extract ran (2 October 2026); the clinicians who moved on 1 October 2026 (three Tolliver Falls
  hospitalists into Alderwick's hospitalist group, two medical group family physicians into Brennick's new rural clinic,
  four Alderwick CRNAs into the medical group's surgery centre, a Brennick emergency physician to Tolliver Falls) carry
  their new entity on their September lines while the cost centres still charge the old one. No document narrates the
  moves; the dictionary states the field's date flatly and the tell is a September line whose cost centre belongs to
  another entity.
- Hazards: HB1 (D6): one line per earning code, each repeating the position's FTE, so summing lines overstates (a
  clinician above 1.0 FTE is the tell); HB2 (D5): fellows carry clinical-sounding profiles ("Physician, Cardiology
  Fellow") that the crosswalk maps to the excluded GME code; HB3: dual appointments hold two positions on two entities'
  cost centres.
- Path (6 files, 11 columns): the HCM extract, the crosswalk, Schedule B, the cost centre directory, the data
  dictionary, the extract log; `worker_id`, `position_id`, `work_month`, `earning_code`, `fte`, `job_profile_code`,
  `job_profile`, `cost_centre`, `home_entity`, the crosswalk's `legacy_job_code`, the directory's `entity_code`.
- Stops (asserted, every one off the golden on all four figures unless stated): S1 (lines summed, home entity) 174.7,
  426.7, 759.2, 98.2; S2 (one FTE per worker, home entity) 93.6, 233.2, 524.1, 54.5; S4 (one FTE per position, home
  entity, the careful path that misses the moves) 93.6, 233.8, 525.6, 54.5; S3 (fellows read as specialists by title)
  moves Alderwick only, 244.3.
- Lazy delta: S1 wrong on 4 of 4.
- Realism: HR systems stamp the current organisation on historical lines in standard extracts, and an October
  reorganisation ahead of a January insurance transition is ordinary.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta (asserted as built) |
|---|---|---|---|
| HA1 escalation chain | a suit after a request opens a new claim number | Ask A (and the call's merge, where it is the L0 rung) | S1 against S2: Alderwick 12 against 8, the medical group 11 against 9 |
| HA2 re-issued June run | Quillan corrected and re-sent its June valuation | Ask A | Tolliver Falls 0 to 3, Alderwick 2 to 5 |
| HA3 reference formats | the carriers' own formats | Ask A | every Stoneleigh match |
| HB1 earning-code lines | the 2026 HCM's line grain | Ask B | every figure (S1) |
| HB2 fellows | HCM profiles for trainees | Ask B | Alderwick, 234.3 to 244.3 |
| HB3 dual appointments | clinicians on two entities' cost centres | Ask B | every figure under one FTE per worker (S2) |

**The cracker sheet.** The cracker filed the golden contribution, ran the hygiene battery (keys unique, exact
duplicates, every join from the register matched, no fan-out, counts tied) and executed every filed rule. Every ask
row misses:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 4 counts and 4 reserves | open register claims merged per incident, matched to the latest valuation on normalised claim numbers and the prior chain | noticed claims sit under notice numbers on the carriers' runs | miss |
| Ask B, 4 FTE figures | one FTE per position, fellows out through the crosswalk, by the line's home entity | the 1 October movers carry their new entity on September lines | miss |
| Slides | carried by the main call, scored with it | | outside |

Mirror leakage: 10 per cent of the ask weight (the mirror stops at R2, answers both asks as the cracker does and keeps
only method credit; no ask figure couples to the call).

**Pair arithmetic.** Planning weights 38 recommendation (the contribution, each entity's and each class's count and
cost), 7 instruction following, 55 asks over 12 figures. The cracker keeps about 10 per cent of the ask weight:
C = 38 + 7 + 5.5 = 50.5. The mirror keeps r of about 3 (the files, the slide structure) and the same 5.5:
S = 3 + 7 + 5.5 = 15.5.

Pair ceiling: 33.0

If the generated rubric grades the entity and class figures as asks, the cracker keeps them and the mirror does not: C
rises to about 66 and S stays near 16, a pair of about 41; that case needs the call held by all but one response,
which the decisive rung is built for. A response that finds the notice log keeps Ask A's 8 figures, and one that reads
the cost centre's entity keeps Ask B's 4: each device carries its whole ask. Recomputed from the generated rubric when
it exists.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| Trust agreement 1.3 (Claim) | 2, the trust's governing contract | one claim per incident, first made at the earliest request, program requests included | anything about delay or cost |
| Trust agreement 2.1 and Schedule A | 2 | claims-made from each entity's Transition Date | how a window is priced |
| Funding policy 3.1 to 3.6 | 1, the trustees' policy | the estimand, the experience, the trend, exposure by day, pooling, rounding | delay, window share, cost by timing, step factors |
| Schedule B | 2 | covered jobs and classes, both legacy code sets | FTE totals |

## Prompt

`prompt.txt`, 908 characters, `voice-check.py` PASS: the call with its unit and the forcing fact (each entity moving in
on its occurrence policy's expiry), the two files with what each holds, Ask A with "whether any ... and, if so" (no
presupposition, H23), Ask B, the chart's named parts (each entity's expected cost by the month the claims are made),
and the rounding once at the close. Reworded at the build from the precut draft: Ask A's "under its expiring policy"
became "under its occurrence policies", Ask B lost "by specialty class", the chart names the month the claims are
made in, and the slide sentence no longer opens "I also need two slides in" (a rare construction `guard.py surface`
matched to task133's prompt).

## Build record

- Claims seed 3671 (`build.py`), chosen from 8,000 by the seed search: every rung's separation, the grid at 6 per cent
  or more, the 23 graded figures at least 7 per cent of a bin from a rounding edge (worst: Anesthesiology's cost at 8.6
  per cent), the rounded entity and class costs and counts adding to the rounded totals, a contribution that is not a
  multiple of $10,000, and Ask A's facts (two or more open noticed claims per entity, "none" for at least one entity,
  missing claims for at least two). The payroll world, documents and Ask B use their own fixed streams (seed 1301012).
- The call: $784,000 (unrounded $783,667). Entities: Tolliver Falls 2.9 Claims, $227,000; Alderwick 4.6, $336,000; the
  medical group 3.9, $214,000; Brennick 0.1, $7,000. Classes: Obstetrics 2.0, $148,000; Surgery 2.3, $291,000;
  Emergency Medicine 2.0, $68,000; Anesthesiology 0.5, $65,000; Hospital and Medical Specialties 2.3, $124,000; Primary
  Care 1.4, $26,000; Advanced Practice 1.0, $62,000. Total 11.5 Claims on 555.8 FTE-years.
- Asks: A as above; B 96.3, 234.3, 522.0, 54.9 (907.5 in all).
- Gates at stage 3: `checks.py` 121 of 121 (the house fixes H5, H9 and H16 wired in, and the records behind this note's
  world and ladder figures); `verify.py` (its own path, bundle only) matches every golden figure; two
  builds byte-identical; `figures_check.py` exit 0; `precut.py` exit 0; `leak.py` REVIEW with no LEAK (lines answered
  below); `guard.py surface` and `heart` as recorded in `pipeline.json`.
- Surface: `guard.py surface` promotes only task102, on the card axes (gap time, pattern G13, Gate G forecasting,
  decision quantity_figure), answered by the card's differentiation line; no surface overlap. Two surface tells were
  removed at the build: the extract log's column set copied task124's, and the prompt's "I also need two slides in"
  matched task133's.
- Leak review (`leak.py --asof 2026-10-12`: REVIEW, no LEAK), one line per REVIEW:
  - Sweep 3, golden figures 1.4 and 2.3 in the trust agreement: they are its clause numbers (1.4 Medical Incident, 2.3
    limits), not the Primary Care and Surgery counts.
  - Sweep 3, the call's words in the agreement, the policy and the dictionary: those files define the trust and its
    contribution; none states a cost, a share or a 2027 figure.
  - Sweep 4, 4 to 5 of the stump paragraph's words (register, exposure, experience, incident, payroll, program, family)
    in the agreement, the policy and the dictionary: the field's own nouns; no sentence names a delay, a window share
    or a cost by timing.
  - Sweep 6, entity and class names beside numbers in the agreement (Schedules A and B: dates, policy numbers, job
    codes), the staffing plan (FTE), the cost centre directory, the premium history and Quillan's runs (claim amounts):
    none ranks the entities or classes on the contribution; the plan is the exposure the funding policy names.
  - Sweep 9, 2027 dates in the premium history: the end dates of the 2026 policy terms.

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
