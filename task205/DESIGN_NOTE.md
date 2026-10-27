# task205 design note

Status: DESIGN. Architecture v1 is screened to a **measured refusal** before any row was cut. Nothing in
`target/` exists, no generator exists, and no card is registered. This note carries the draw I would
register, the ladder measured on a prototype, and the numbers that refuse it. Read `## Tried and rejected`
first: it holds the measurements.

## Draw

| Field | Value |
|---|---|
| Seed | `analytical_tasks/02_anomaly_detection/AD28_recommissioning-ticket-actuator-recovery.md`, header and Situation only. World, decision and quantity kept; the pitfall re-found from the data. |
| Objective | `anomaly-detection` |
| Domain (client) | `energy-systems-utilities` |
| Task type (`subdomain`) | `efficiency-savings-verification`, which is the honest task type for a measurement-and-verification call and which **serves `experiment-causal` only**. Measured: `guard.py check` returns `BLOCK three_rules.task_type`, "task type efficiency-savings-verification serves experiment-causal, not anomaly-detection: the domain would be a backdrop", with the fix "draw a task type of energy-systems-utilities that serves anomaly-detection (grid-reliability-outage-analysis), or another domain". |
| Niche | recommissioning ticket allocation across a flagged estate under a measurement-and-verification protocol |
| Shape | 03, bridge between totals, each candidate a reconciling item (`stumping` 1.1i: on this objective every build that shipped and held was a recovered quantity or a decomposition, and every build that died was a ranking) |
| Decision type | `quantity_figure` (the recovered energy the cycle's one ticket books, the building named as its consequence) |
| Strategy | `informative_censoring`, which is unspent: zero cards on file carry it, and it is not one of the five semantics-risk labels the guard flags |
| Gate G | `method_or_model_selection` |
| Stakeholder | the trust's energy and carbon programme officer, who places the recommissioning engineer booked for the next cycle (`programme_officer`) |
| World | England, GBP, an NHS foundation trust estates and facilities directorate (`hospital_or_health_provider`), five flagged buildings. Personas drawn with `guard.py names --geo England --seed 205`: Nigel Wilkinson, Bethan Stokes. |
| Forum / forcing event | `committee_or_panel` / `period_close` |
| Spine | `building_daily_energy_2023_2026.csv`, one building's metered energy on one day on one channel, about 32,000 rows before the context estate is added |
| Context artifact | `operations_log` |

**Shape arithmetic, 25 or more criteria.** Five candidate buildings x two figures each (the recoverable
energy and the excess rate in force) = 10; the bridge from the estate's reported year-over-year movement to
the recovered total, one reconciling line per candidate plus the two totals and the residual = 8; the call,
the runner-up, the gap and the flip = 4; a chart with named parts (one bar per candidate, the reported
movement and the recovered figure labelled, the ticket's candidate marked) = 5. Total 27.

**Why the world moved off the seed's own org family.** The seed's world is a university energy office.
Measured: `guard.py check` returns `BLOCK ban.org_family` on `university_or_school` against task204, and
`BLOCK ban.forcing_event` on `budget_or_appropriation` against the same card, both registered today. An axis
ban is cleared by redrawing the axis, never argued, so the estate becomes a hospital trust's and the forcing
event becomes the cycle's period close. The redraw is also the honester label here: the trust's charter, not
an academic calendar, is what books the engineer, and it takes the build a further step away from task204's
further-education campus.

**Why the domain tag moved off the seed's.** The seed names Economics. Measured: `economics` is a house
domain sitting in `economics-econometrics`, and `guard.py check` returns `BLOCK three_rules.task_type`,
"house domain economics sits in economics-econometrics, where no task type serves anomaly-detection". So the
seed's own domain cannot be registered on the seed's own objective at all.

**Sources, one line each.**
- `stumping` 1.2c and the author's own law: the decisive step may not be priced by a model of the
  measurement. This is the law the draw is screened against first, and the law that refuses it.
- `stumping` 1.1i: a recovered quantity rather than a ranking, shape 03. Taken.
- `stumping` 1.1b: the field's own method sits at rung 0 or rung 1 and the decisive step is the recognition
  that this dataset violates its precondition. Taken: weather-normalised year-over-year is rung 1.
- `determinism-check` section 3, the bin paragraph: the three quantities in bin units, and the rule that the
  second quantity is the WHAT screen read as a number. This is what closes the architecture.
- `guard.py mechanisms --objective anomaly-detection`, 35 builds. One line on the insight each spends is in
  `## Tried and rejected` under "the mechanisms screen".

**Data-native sentence.** On this estate every fault is a persistent step in a building's own metered rate
with its own onset date, and the office's alert compares two closed annual totals, so for a fault older than
a year the comparison period already contains the fault and the measured movement is the fault's growth
rather than its level: the fault that wastes most is the one the alert can least see.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' grain. Steps 1 to 5 are the
field's own method, which is where `stumping` 1.1b requires it to sit.

1. Read `building_daily_energy_2023_2026.csv`, conform the thermal channels (kWh against kBtu across the
   platform migration), and drop the duplicated preliminary monthly release where the revised release exists.
2. Join the daily outdoor air temperature series and form heating and cooling degree days at the base
   temperatures the estate's own protocol uses.
3. For each of the five flagged buildings fit consumption on degree days and a weekday term over the
   reporting year and again over the baseline year, which is the field's Option C routine adjustment.
4. Predict both years at the same normal-year weather and take the difference, which is the
   weather-normalised year-over-year movement, the quantity the office's alert and the protocol's own
   worked example both display.
5. Rank the five on that movement, take the largest as the ticket's building, and quote its movement as the
   energy the ticket gives back over the following twelve months.
6. Sanity-check against the equipment register and the closed-ticket book, neither of which contradicts the
   ranking.

Ends on: Quarrendon, about 82,000 kWh recoverable (measured on the prototype: 82,109 kWh at seed 11, and
the largest weather-normalised movement of the five in 20 of 20 seeds).
Golden: Netherby, about 140,000 kWh recoverable (measured: 140,258 kWh at seed 11 against a truth of
144,175 kWh; the golden's own construction names Netherby in 20 of 20 seeds).

## Stump sentence

The response files **Quarrendon at about 82,000 kWh**, because it sized each flagged building as a
weather-normalised difference between two closed annual totals, which measures how recently each building's
excess began rather than how large it is, and Quarrendon is the building whose metered load genuinely grew
last winter while Netherby's larger excess has run through both of the compared years and very nearly
cancels out of the difference.

## Three rules

- **Task type:** `energy-systems-utilities / efficiency-savings-verification`, the field's own
  measurement-and-verification task type. **This line fails its own gate:** that task type serves
  `experiment-causal` in the taxonomy, not `anomaly-detection`, measured as a `guard.py` BLOCK, and the only
  anomaly-detection task type in the domain is `grid-reliability-outage-analysis`, which is about outages and
  reliability rather than building energy. Taking it to pass the gate would be a card written to pass.
- **Domain test:** The deciding quantity is the avoided energy a controls repair books over the twelve months
  after it, which the field estimates as a persistent excess rate in force at the decision date, under a
  measurement-and-verification protocol, rather than as a difference between two closed annual totals; a
  generalist substitutes the year-over-year movement the alert already prints.
- **Swap:** "Which of the five flagged buildings gets the cycle's one recommissioning ticket, and how many
  kilowatt hours it gives back over the twelve months after the engineer leaves." Put a hospital's wards in
  for buildings and attendances in for kilowatt hours and the sentence still parses, but it stops making
  sense at "gives back over the twelve months after": a ward's attendances are not a rate that a repair
  switches off and leaves off, there is no continuously running waste whose level persists until someone
  changes a control sequence, and nothing in the attendance record plays the part the fault's onset date
  plays here. The swap test passes on the sentence. It is not what refuses the draw.
- **Layer 1:** billing periods that do not close on a month end (the supplier's invoicing cycle); thermal
  channels recorded in kWh in the later years and kBtu in the earlier ones (a metering platform migration);
  channel renames mid-series at that migration (the platform's own identifiers); a preliminary and a revised
  monthly release that overlap (the estate team's reporting cycle). Each is produced by a system the trust
  runs, none is placed to be caught, and none carries the decisive step.
- **Layer 2:** `estimand_identification`. The methodological choice that flips the call is whether the
  recoverable energy is read off a difference between two closed annual totals or off the excess rate in
  force at the decision date.
- **Decisive step:** Size each candidate on the excess rate still in force at the decision date, annualised
  over the ticket's own forward window, instead of on the normalised movement between the reporting year and
  the baseline year, because for the older faults the baseline year already contains the fault.
- **Not semantics:** Every field, code, unit and definition can be read correctly and the easy route still
  files Quarrendon. The channels conform, the releases deduplicate, the degree-day bases are the protocol's
  own, the register and the ticket book agree with the series, and nothing in the pack says which of the two
  comparisons the charter's quantity is. The flip is not a reading; it is which comparison estimates a
  forward counterfactual.
- **Not rule application:** No filed rule or procedure performs the step. The protocol files the quantity (the
  energy avoided over the twelve months after the measure) and not the comparison that estimates it, so a
  reader who executes every stated rule still has to choose. **Measured spread of the family the rule leaves
  open, which is the half of this line that counts:** with the measurement window filed, as
  `determinism-check` section 1 requires it to be, the eight remaining defensible constructions of the golden
  estimand (base temperatures 15.5/18, 18/18, 20/22, 12/16 and the weekday term on or off) spread the graded
  figure a mean of 6,015 kWh and a maximum of 18,394 kWh. **With the window left open, which is the only way
  the step stays non-trivial, three defensible windows (90, 180 and 365 days) spread it a mean of 74,258 kWh
  and a maximum of 97,833 kWh, against a decisive worth of 126,214 kWh.** So the step is a method rather
  than a knob only while the window is unfiled, and the window is one of the five parts section 1 requires
  filed. That is the refusal, in one number.
- **Analyst test:** A strong analyst reads every meter, register and protocol clause correctly and sizes each
  flagged building as its weather-normalised year-over-year movement, ranking the five by how recently their
  excess began rather than by how large it is, and files Ends on: Quarrendon at about 82,000 kWh.
- **Estimand:** "The electricity and heat the building would not consume in the twelve months beginning on the
  day the engineer leaves, had the condition the ticket corrects not been present, counted on the trust's own
  metered channels for that building and expressed in kilowatt hours." Filed once, in the recommissioning
  programme charter.
- **No decoy:** Nothing is planted to be caught. No copied block of readings, no withheld rule, no memo, draft,
  briefing or stakeholder figure written to carry the wrong answer. Quarrendon's rise is a real metered load
  increase with a real cause in the equipment register, and it is not ruled out by any document: the golden
  beats it on magnitude, not on a disclosure. No shipped artifact ranks the five.
- **No certified replay:** The method is not hidden and recovered by reproducing certified or published
  figures. There is no closed corpus of past tickets in the solution's path; the closed-ticket book is
  context and agrees with the series under both comparisons.
- **Lesson:** That a year-over-year comparison of two closed totals measures the growth of a persistent excess
  and not its level, so it ranks candidates by onset date. **This line also fails:** the signature is spent.
  `guard.py check` returns `BLOCK test.same_puzzle_older` against task102, task130 (three lineage
  architectures), task134 and task171, and `BLOCK test.same_driver_older` against task229, task242, task461,
  task476 and task501, on the triple (gap time, pattern G13, quantity_figure) and (gap time, pattern G13,
  method_or_model_selection) respectively. task33's architectures v1 and v2 spend the mirror insight on this
  objective ("the one whose shift is still in force, measured as forward yield over the action window,
  because the largest past exceedance has already resolved") and task182's architecture v1 spends it in the
  other direction and was solved on the portal.

## Readability screen

Six tests per rung, verdict last. The decisive row has to read `silent`. It does not.

| Rung | Construction | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 0 | raw year-over-year total difference | no | no | yes | no | no | yes, one subtraction | no | readable |
| 1 | weather-normalised year-over-year, the field's Option C routine adjustment | the protocol describes routine adjustment in general terms | the degree-day series is shipped | yes, the field's first move | no | no | no | no, the weather series is ordinary | readable |
| 2 | the same calendar quarter two years apart, times four | no | no | **yes** | no | **yes, a three-year daily plot shows the step and its onset date** | **yes, one filter, one subtraction, one multiply** | no | readable |
| 3 (decisive) | the excess rate in force at the decision date, annualised over the forward window | no | no | **yes** | no | **yes** | no | no | readable |

Tests 3, 5 and 6 fire on the decisive rung, and rung 2 is the cheapest licensed member of the decisive
rung's own family. Measured: rung 2 names the golden building in **20 of 20** seeds, and its graded figure
sits 14,379 kWh from the golden's on a figure of 144,175 kWh, a clearance of **1.10x** against the 1.15x
floor every rung owes. By `stumping`'s cheapest-licensed-member law, family unanimity here IS the easy route
landing, and the decisive rung is not a stopping point but a confirmation.

## Semantic fork table

Sketched only; no `generator/checks.py` exists, so `precut.py` will refuse these rows and should.

| id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the twelve months beginning on the day the engineer leaves" | the 365 days from the stated handover date | the next full financial year | same call | records clear of both boundaries (C1), to be asserted |
| SF2 | "the building's own metered channels" | every channel the meter register maps to the building at the as-of date | the channels named in the earlier platform's identifiers | same call | the register's own crosswalk (C4), to be asserted |
| SF3 | "would not consume ... had the condition not been present" | the counterfactual at the rate in force | the counterfactual at the baseline year's level | **the call flips to Quarrendon** | **nothing shipped closes this row.** This is the refusal restated as a fork: the row cannot be closed without filing the comparison, and the comparison is WHAT |
| SF4 | kilowatt hours on a thermal channel | the conformed kWh after the kBtu channels are converted | the raw channel value | same call after conformance; the naive read moves every candidate in the same direction | the channel dictionary (C4), to be asserted |
| SF5 | rounding path | once, at the end, to the nearest 100 kWh | per candidate per month then summed | same call | to be asserted mid-bin |

SF3 is an open row on the main recommendation. `precut.py` refuses it, and it should.

## Ladder

Measured on a prototype (`screen1.py`, `screen1b.py`, `screen1c.py` in the author's scratch directory, 20
seeds, five candidates, three years of daily data, faults of four distinct onset dates and one genuine load
increase). Figures in kWh. The designated building's truth is 144,175 kWh.

| rung | construction | names the truth | its own graded figure | share of the golden |
|---|---|---|---|---|
| 0 | raw year-over-year | 0 of 20 | 6,169 at the golden's building | 0.04 |
| 1 | weather-normalised year-over-year | 0 of 20 | 8,617 | 0.06 |
| 2 | same quarter two years apart, times four | **20 of 20** | 134,621 | **0.96** |
| 3 | single-step changepoint fit, step times 365 | 20 of 20 | 135,448 | 0.97 |
| golden | excess rate in force, annualised over the filed window | 20 of 20 | 140,258 | 1.00 |

**The bin arithmetic, in the graded figure's own units.**

| quantity | measured | notes |
|---|---|---|
| (a) the decisive step's worth | **126,214 kWh** mean, 115,525 minimum | golden less rung 1, over 20 seeds |
| (b) spread across defensible constructions, **window filed** | **6,015 kWh** mean, 18,394 maximum | 8 members: four degree-day base pairs x the weekday term |
| (b) spread across defensible constructions, **window open** | **74,258 kWh** mean, 97,833 maximum | 3 members: a 90, 180 or 365 day measurement window |
| (c) the golden estimator's own sampling interval | **6,909 kWh** mean, 7,354 maximum | standard error of the mean daily excess, annualised |
| (a) / ((b) + (c)), window filed | **10.49** mean, 5.29 worst seed | the inequality (a) > (b) + (c) holds |
| (a) / ((b) + (c)), window open | **1.29** mean | holds, barely |
| smallest rung gap | **14,379 kWh**, rung 2 to the golden | (a) is not the smallest gap; the smallest gap is the one that matters |
| golden bias against the clean truth | 753 kWh, 0.5 per cent | the golden estimator is honest |

So the draw **passes the bin inequality and fails the ladder**. The decisive step is worth 10.5 times the
readings and the noise together, and it buys nothing, because the rung beneath it reaches the same call 20
of 20 at 0.96 of the golden's figure and 1.10x of the decision boundary, under the 1.15x floor. (c) is real
rather than near zero because the golden's estimator is a fitted level over a chosen window rather than an
observed count over a constant, which is the condition `determinism-check` names as the one that sank
task157.

**The one-ended dial, which is why no tuning repairs it.** The single parameter that stops rung 2 reaching
the call is how much of the waste depends on the weather rather than running at a constant rate. Measured
(`screen3.py`, 20 seeds a cell, the annual waste held constant across the sweep):

| weather-coupled share of the waste | rung 2 names the truth | spread of the golden's own construction family | spread / figure |
|---|---|---|---|
| 0.00 | 20 of 20 | 13,077 kWh | 0.09 |
| 0.25 | 20 of 20 | 45,991 kWh | 0.33 |
| 0.50 | 19 of 20 | 87,310 kWh | 0.65 |
| 0.75 | 17 of 20 | 128,899 kWh | 0.99 |
| 1.00 | 13 of 20 | 170,488 kWh | 1.35 |

**0 of 5 cells** have the cheap rung missing and a determinate figure. The dial that buys Gate F spends
Gate C one for one, by a factor of 15 over its range, which is `stumping` 1.2c measured in this world's own
units: the only thing that makes the waste invisible to a like-for-like calendar comparison is the thing
that puts a baseline model in the deciding position.

## Closure table

The 22 axes of `determinism-check/references/forcing-the-answer.md` Part 1. Rows are written as the
architecture would close them; rows 3, 8 and 12 are where it dies.

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the five flagged buildings and their metered channels | estimand filed literally in the charter; the estate's other buildings are context and named out |
| 2 | Unit of account | one building | the question names the building; the channel-to-building map is the register's |
| 3 | Attribution window | which days the excess is measured over | **open.** C1 is unavailable: the three defensible window lengths spread the figure 74,258 kWh, and filing the window (which section 1 requires) drops the decisive step to rung 2's reflex |
| 4 | As-of dating | the state of the register and the series at the period close | filed as-of date in the charter |
| 5 | Version basis | preliminary against revised monthly release | C1: the revised release supersedes, every overlapping day identical in the solution's path, to be asserted |
| 6 | Denominator | none; the graded figure is a total, not a rate | not applicable, recorded for completeness |
| 7 | Weighting | pooled across days or equal by month | C1 across both, to be asserted |
| 8 | Window length | how far back the rate in force is measured | **open, same as axis 3.** This is the binding term in (b) |
| 9 | Boundary inclusivity | the forward window's first and last day | C1, nothing on the edge |
| 10 | Rounding path | once at the end, to the nearest 100 kWh | filed at authority in the charter |
| 11 | Tie-break | two candidates within the printed cell | no tie: the gap to the runner-up is 1.73x on the prototype |
| 12 | Maturity and censoring | a fault whose onset precedes the record's start | **partially open.** One candidate's onset would sit before the series begins; the architecture needs every onset inside the record, which narrows the world rather than closing the axis |
| 13 | Order of operations | conform channels before or after deduplicating releases | C1, commuting on the solution's path, to be asserted |
| 14 | Row order | file order | C1, asserted over permutations |
| 15 | Duplicate resolution | the preliminary and revised releases | filed rule in the reporting note plus C1 |
| 16 | Identity normalisation | channel identifiers across the platform migration | the platform's own crosswalk, C4 |
| 17 | Netting against gross | may a fall on one channel offset a rise on another | filed scope: the charter counts the building's channels summed |
| 18 | Dimensional units | kWh against kBtu on the thermal channels | the channel dictionary's own factor, C4 |
| 19 | Code and status semantics | the register's channel status codes | the register's crosswalk; never the stump |
| 20 | Integerisation | none; kWh to the nearest 100 at the end | C1 by construction |
| 21 | Clause scope | whether the charter's quantity is per building or per ticket | filed scope: per ticket, one building |
| 22 | Forward window contents | what the twelve months after the ticket hold | a shipped driver file for the span, which is where a weather assumption would have to enter and the second reason axes 3 and 8 cannot be closed without filing a model |

## Literal reader

A reader who executes the charter, the protocol and the prompt word for word, inferring nothing, is left
with the charter's quantity filed and **no sentence saying which comparison estimates it**. Enumerating the
options, the reader computes the weather-normalised movement between the two closed years and files
Quarrendon, or computes the excess rate in force and files Netherby, and nothing shipped rules either out.
That is SF3, and it is an open fork on the main recommendation. Filing the comparison makes the decisive
step executable; leaving it open fails Gate C as `underspecified_objective`. There is no third position,
which is `determinism-check` section 1's own wording: the comparison is WHAT.

## Oracles

`none` as drawn. The closed-ticket book and the equipment register both tie under rung 1 and under the
golden, so neither nominates. The protocol's worked example displays a normalised year-over-year movement
for a building outside the candidate set, which ties under every reading and ranks nobody. No published
figure, reconciliation column or control in the pack confirms either path over the other, which is the one
thing this architecture gets right and also why nothing closes SF3.

## Ask sheet

Not designed. The ladder is refused, and `supplemental-stumping` Part 0 is explicit that no ask work is
worth doing until the ladder holds: "where Gate F finds the call landable, the pair ceiling is not evidence,
the finding is in the ladder". `Pair ceiling:` not measured. `Mirror leakage:` not measured. `Measured by:`
no script exists. These fields are deliberately absent rather than filled with paper numbers, and
`precut.py` fails on them correctly.

What the layer would have to be, recorded for whoever takes the world forward: three asks over the estate's
other buildings and other channels, which the call never reads (`supplemental-stumping` 2.1, the separation
line), each routed through a reconstruction rather than an estimator (1.0b), with primaries from the D2
vintage and D6 grain families, since the D8 clock family is already the pack's Layer 1 texture here and a
device in the same family as the texture is seen rather than silent.

## Tried and rejected

- **The mechanisms screen, one line on the insight each spent driver on `anomaly-detection` already uses**
  (`guard.py mechanisms --objective anomaly-detection`, 35 builds). task25 inflow a second source holds;
  task28 the share of a flagged excess one intervention can reach; task33 forward yield truncated by a filed
  future intervention; task48 a two-sided pair grain invisible to the monitor; task54 an exposure integral
  over units still in custody; task68 a matched panel of continuing units across identity successions;
  task76 a class with zero observed conversion found by a per-unit look-back; task85 each unit's own
  observation window from an intermediary's lead time; task103 a permission against a record of service;
  task104 what a self-adapting scorer would have flagged at a setting it never ran; task119 waits a unit
  could itself have shortened; task125 a recruitment filter compounding through fixed later periods;
  task180 events recorded only above a diurnal noise floor; task181 crossings rather than time as the
  exposure; task182 duration summarised from snapshots of work in progress; task183 a unit's coming events
  arising in parts that have already failed; task184 a per-item rate behind a container-level indicator;
  task185 a conversion between two devices sized at the value converted; task186 local cycles shared within
  a place; task187 a capped curved response averaged over a spread of inputs; task188 a density from grouped
  tests; task189 an average over values known only as bounds; task190 a ratio whose numerator is complete
  and denominator a sample; task191 the largest of many shortfalls against the largest a quiet set
  produces; task192 a label by instrument whose validation batch covered only the window's opening;
  task193 orderings whose room depends on where a first exposure falls; task194 a count that crystallises
  after its own period, read through two vintages; task195 the uncertainty of a paired difference;
  task196 events recovered from the overlap of two capture channels; task197 the output a unit would have
  produced had a signal stayed in its dead band; task198 a reported value that is the lesser of an ask and
  an entitlement; task199 a rise read against the filing volume behind it; task201 an exposure span missing
  its opening interval; task202 a within-unit spread the record never states; task204 a transport rate from
  a unit's own unsteady balance across filed windows. **What they leave:** every one of them files something
  unobserved and recovers it from a structure the main file does not carry. Three of them (task28, task33
  v1 to v4, task182 v1) are the recommissioning seed's two obvious mechanisms outright, which is why both
  were refused on paper below before any code was written.
- **The share of each flagged building's excess that a controls ticket can actually reach** (the seed's own
  title). Refused twice over. Spent: it is task28's driver verbatim, and task185's own draw note lists "a
  reachable share" among the mechanisms it screened as spent. And dead by arithmetic: measured over 4,000
  redraws a cell at the decision's own size of five candidates, a bounded reach share gives
  **sd(log factor) 0.269 to 0.309** for a plausible estate (a Beta at mean 0.55) against the dispersion
  ceiling of about 1.4 the multiplicative-correction floor needs, with the reflex that ranks on the raw
  excess taking the top candidate **47.4 to 74.7 per cent** of the time and the realised correlation
  +0.53 to +0.87. Pushed to an implausible share (mean 0.23, sd(log) 0.88), the reflex still takes the top
  candidate **29.8 to 47.9 per cent** of the time. No bounded share reaches the dispersion the floor needs,
  so the correction cannot reorder the candidates.
- **Persistence read off the closed-ticket book** (fit the decay of past tickets' measured savings and apply
  it). Refused on sight: a corpus fit is `withheld_rule_corpus_fit`, which rule 3 bars from deciding a call,
  and task194's architecture v1 is this exact move ("fitting competing shapes of that effect to a closed
  corpus of past interventions"), spent at stage 4 on a NOT_DETERMINISTIC send-back.
- **Forward yield truncated by an already-funded capital project** that would end the fault anyway. Refused:
  task33's architectures v3 and v4, spent, with v3 failing the portal's determinism review.
- **The marginal rather than average plant conversion** (weight each building's thermal excess by the
  efficiency of the machine actually at the margin in that hour). Refused on two grounds without code: the
  conversion enters through a response function, so the exponent is a free method choice and the determinacy
  screen fires; and it is a model of the measurement, which the author's own law and `stumping` 1.2c bar.
- **Baseload recovered from the quiet hours** (take each building's overnight or vacation floor as the
  fault's rate). Refused: this is the null-region screen, which `stumping` closes with measurements, since
  the region where the signal vanishes publishes the nuisance and a one-group-by over the quiet days reaches
  the same answer at corr +0.9761 to +0.9998.
- **Days the metering platform's validation rules dropped** (put the excluded days back, since the fault is
  what trips the validation band). Refused: the exclusion is carried by a flag, so the answer flips on
  reading a field correctly, which is data semantics and banned as the decisive step; and the correction
  leaves most of the record alone, so the partial-coverage screen fires on the untouched subset.
- **A count of empty or part-loaded cycles from a batch traceability record** (sterile services or laundry,
  a record the trust keeps for infection control rather than for attribution, joined to the interval meter
  at each cycle's own timestamps). The most promising candidate found, and refused on readability test 2:
  the batch record ships with a key, so noticing the join and performing it are one act, and
  `supplemental-stumping` 1.0 is explicit that a device whose discovery and remedy are the same act is not a
  device. Its conversion coefficient is the second kill: stated, it is rule application; estimated from the
  meter, it is a model of the measurement.
- **The architecture this note carries, the excess rate in force against a baseline the fault already
  occupies.** Refused on measurement at stage 2, nothing cut. The bin inequality holds at 10.49 and the
  ladder does not: the cheapest licensed member of the decisive rung's own family (the same calendar quarter
  two years apart, times four, with no weather model anywhere in it) names the golden building **20 of 20**
  at 0.96 of the golden's figure and a clearance of **1.10x** against the 1.15x floor, so Gate F fails by
  the cheapest-licensed-member law. The one dial that removes it (making the waste weather-coupled rather
  than a constant rate) multiplies the golden's own construction spread from 0.09 to 1.35 of the figure over
  its range, **0 of 5 cells passing both**. And the binding term in (b) is the measurement window, which
  `determinism-check` section 1 requires filed, so closing it converts the decisive step into rung 2's
  reflex rather than repairing it: the second bin quantity is the WHAT screen read as a number, and it reads
  BLOCKED here.
- **The card's own structural tests, measured at the same time.** `guard.py check` on the drafted card
  returns BLOCK on `three_rules.task_type` (the honest M&V task type does not serve this objective), on
  `test.same_puzzle_older` against five earlier builds and on `test.same_driver_older` against five more,
  with WARNs on the deliverable format set against task204 and on the question form against task271. No axis
  ban fires on the redrawn axes (org family, forcing event, forum, role, artifact, shape, strategy, spine),
  and the nearest driver on file is 0.07, which is the lexical screen failing to see a mechanism repeat
  exactly as `fingerprint` Part 4 says it does. The structural tests see it.
- **What ground is left in this world, named rather than implied.** Everything measured above says the same
  thing: on this estate the deciding quantity is an energy estimate, and an energy estimate over a forward
  window has to pass through either a like-for-like calendar comparison, which is one group-by and reaches
  the call, or a baseline model, which forks every graded figure. So what is left is not a cleverer energy
  estimator. It is either (i) the same world and decision on the objective its task type actually serves,
  `energy-systems-utilities / efficiency-savings-verification / experiment-causal`, which `guard.py check`
  clears on the task-type rule and where the pairing has one card on file, and where the field's own
  method being the golden is legitimate rather than fatal; or (ii) a deciding quantity in this world that is
  not an energy estimate at all, recovered as an exact count or duration from a record the trust keeps for
  compliance, provenance or safety rather than for attribution, at a grain no grouping of the energy series
  reproduces, with no coefficient anywhere in its path. Candidate (ii) is where I would look next, and the
  cycle-count candidate above is the version of it that fails, so the next attempt has to put the join's
  discovery and its remedy in two different places.
- **Architecture 2 candidate A, criminology-justice / crime-incidence-hotspot-analysis: offences dated on
  the day a patrol found them, with the owner's statutory inspection register narrowing each occurrence
  interval exactly** (scratch `c1_screen.py`, `c1_dial.py`, `c1_bins.py`, 20 to 25 seeds a cell, five asset
  classes, 200 sites, 18 months of daily data; graded to the nearest 5 offences). Refused on measurement at
  stage 1, nothing cut. **The rung beneath the decisive one is rung 0, no construction at all:** counting
  the offences whose DISCOVERY date falls in the quarter hits the golden's printed cell **18 of 25** at a
  clearance of **1.046x** against the 1.15x floor, because discovery trails occurrence by one inspection gap
  and a quarter's discoveries are therefore a quarter's occurrences. The cheapest licensed member of the
  golden's own family, the midpoint of the NARROWED interval, hits **23 of 25** at **1.008x**. The field's own
  aoristic allocation over the stated window (rung 1) and its midpoint (rung 2) are the only routes that
  miss, 0 of 25 each at 1.879x and 2.017x, so **the ladder is inverted**: the crudest route is nearest the
  golden and the field's own method is furthest. The dial is one-ended and no tuning repairs it: sweeping the
  owner's actual inspection gap from 9 to 144 days, rung 0's hit rate falls 18, 16, 13, 7, 4 of 20 while rung
  3's only falls 19, 16, 15, 13, 10 of 20 and the golden's own placement family opens from 0.41 to 3.49 bins,
  so **0 of 5 cells** have both cheap routes missing. The bin arithmetic passes at the design cell ((a) 2.042
  bins, (b) 0.820, (c) 0.467, ratio 1.587) and fails from f=2 outward (0.767, 0.140, 0.172), and (a) is never
  the smallest rung gap only because the smallest gap is the golden to rung 3 at **0.108 bins**, which is the
  kill restated. Dead twice over on the guard besides: `guard.py check` returns BLOCK on `test.same_puzzle`
  (time, G12, quantity_figure) against task157, on `test.same_puzzle_older` against task192 and task482, and
  on `test.same_driver_older` against task192, task201, task445 and task482, four earlier builds on one
  signature; and the abstraction test puts the driver on **task487** verbatim in other nouns ("events found at
  a scheduled inspection began at unrecorded times since the previous one"), which the lexical screen scored
  at 0.08. `guard.py slots` adds that the aoristic family is declared closed on this cell in task182's note
  and that the occurrence window is "taken by task184" in task200's.
- **Architecture 2 candidate B, human-factors-ergonomics / safety-incident-error-analysis: a controlled-drug
  balance error persists in the running balance until the next pharmacy reconciliation, so the count of errors
  committed is the count of the level's own increments, read against the administration records' ampoule
  counts** (scratch `c2_screen.py`, `c2_dial.py`, `c2_bins.py`, 20 to 25 seeds a cell, five make-ready hubs,
  one quarter of two-person checks; graded to the nearest 5 errors). Refused on measurement at stage 1,
  nothing cut. The separation is real and large: the level count files **223** errors naming Barlby against a
  golden of **45** naming Netherwood, the incident count files 9, the page-net count 18, so (a) is **34.3
  bins** against (b) **0.920** and (c) **1.136**, a ratio of **16.7**, and three of the four cheap routes hit
  the golden's cell **0 of 25** and name its hub 8, 3 and 4 of 25. **The cheapest licensed neighbour kills it:**
  counting the DISTINCT non-zero levels a register page shows, one group-by and one distinct count on a
  shipped column, files 40.1 against the golden's 45.0, a clearance of **1.123x** under the 1.15x floor, and
  names the golden's hub **19 of 25**. The reason is an identity rather than a tuning accident, since each
  increment moves the level to a value the page has not shown before, so distinct levels and non-zero
  increments are the same construction up to a revisited value. The dial confirms it: multiplying the check
  frequency by 1, 2, 4, 8 and 16, that route names the golden's hub 14, 14, 13, 17 and 13 of 20 at clearances
  of 1.131, 1.177, 1.134, 1.167 and 1.164x, **0 of 5 cells** passing, while the golden's own bias against the
  filed estimand (errors committed, not errors observed) runs **12.8 per cent at f=1 and reaches 0.9 per cent
  only at f=16**, which is the setting where the cheap route is at its best. So the parameter that makes the
  golden honest is the parameter that hands the route over. `guard.py check` also returns BLOCK on
  `test.same_puzzle` (population, G2, quantity_figure) against task141, on `test.same_puzzle_older` against
  task148 and task173, and on `test.same_driver_older` against task120, task239, task264 and task269, with a
  WARN that `grain_or_unit` often decides on reading a field; no axis ban fired on any of its eight redrawn
  axes. task229's architecture 2 is the nearest insight on file at 0.06, a state seen only through checks that
  record it just before setting it right.
