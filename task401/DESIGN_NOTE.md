# task401 design note

Architecture 3, drawn 2026-11-03. The number was handed out against seed RC07 (a supplier's January imbalance bill
blamed on low wind by the desk and on plant trips by operations). The seed's world could not carry an honest unbanned
draw; architecture 1 (a frailty virtual ward's prevented admissions against care home closures, Epidemiology and Public
Health) died at stage 2 on published admission rates, and architecture 2 (a canola hybrid blamed for a shortfall that
July heat in late-seeded fields' flowering windows caused, Economics and Econometrics) died at stage 2 when the golden's
own window variants straddled the bar and flexible seeding-date controls landed the golden (`## Tried and rejected`,
the card's `lineage`). Architecture 3 re-roots in another client domain, world, dataset and shell under the same
objective and number (`CLAUDE.md`, a dead design is re-rooted at once; one architecture per world).

The world: an invented GB domestic energy supplier (about 640,000 accounts, electricity and gas, credit and Direct
Debit customers, traditional and smart meters) that tracks every new customer's satisfaction six months after the
switch. Six-month satisfaction fell between the first halves of 2025 and 2026. In the same year the supplier relaunched
its quote and switch journey (May 2025), moved billing to a new platform (phase 1 live 1 September 2025: every customer
who joined from July 2025 is billed on it), raised its variable tariffs in October 2025 and moved its contact centre to
an outsourcer in November 2025. Phase 2 of the billing platform (the remaining legacy accounts) is due to cut over on
1 February 2027; the executive team wants the cause of the fall named before it signs the cutover off.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task401.json`, architecture v3 (v1 and v2 in `lineage` with their
  fates), registered 2026-11-03T16:08:03Z; `guard.py check` on the registered card returns WARN, exit 0, and `validate`
  reads 312 cards with none invalid. Two BLOCKs on the draft were cleared before registration: `ban.pattern` (the first
  decisive generator drafted, G9, repeats task402's) was redrawn to G6, which is the honest label (the per-customer
  satisfaction curve does not move; the 2026 pool shifted on a state no column holds), and `test.same_driver_older`
  against task181 v6 is answered on the card (task181 traces cases to a shared resource that handled them; nothing here
  handled customers differently). The WARNs: `overuse.objective` (root cause in 5 of the last 12; the number sits in
  the root-cause range); `repeat.gate_g` and `overuse.gate_g` against task400 and task402, answered under Strategy.
  NOTEs: `test.same_puzzle_older` and `test.same_driver_older` differentiated on the card against task121 v4 and v5 and
  task181 v6. Nearest driver 0.10 (task121 v4), under the 0.12 floor, screened below.
- **Pairing:** Marketing and Consumer Research (client domain) / `customer-satisfaction-driver-analysis` / Root-Cause
  Analysis. The task type serves Root-Cause Analysis only; `marketing-consumer-research x root-cause` has never been
  built (`guard.py coverage`, 2026-11-03), and the probe card passed the task-type rule. The supplier is the setting;
  the deciding quantity is the task type's own object, each driver's contribution to a fall in the share of satisfied
  customers.
- **Objective and call:** what pulled six-month satisfaction down between H1 2025 and H1 2026, and how much of the fall
  it carries, so the executive team knows whether the billing platform is to blame before phase 2 cuts over. The
  rivals on the record: the billing platform, the October tariff rise, the contact centre transfer and the quote
  journey relaunch. The attribution is retrospective because H1 2026 is the closed window the tracker has measured; the
  decision it feeds faces forward (the February 2027 cutover and what the 2027 quote journey does). It stays Root-Cause
  Analysis: the work is naming what produced the fall with the rivals ruled out on the record; nothing is forecast.
- **Shape:** `03`, a bridge between two totals: the H1 2025 share satisfied to the H1 2026 share, bridged by reconciling
  items (the quote journey's typical-use default, the billing platform, the tariff rise, the contact centre, the rest),
  by fuel; the criteria arithmetic is written at stage 2 with the asks' repeated units. Architecture 2 also carried a
  bridge; the shell is redrawn (question form what, a new second-sentence opener and a new deliverable set at stage 2).
- **Strategy and Gate G:** `decomposition_attribution` (F8: a correctly reported movement booked to the right driver),
  Gate G `decomposition_attribution`. The fall is real and the ratings report it correctly; they book it to billing
  accuracy and so to the platform, and the decisive move books it to the quote default through each customer's
  disconfirmation. `repeat.gate_g` against task400 and task402 is answered: it is the honest label, and the decisive
  families differ (task400 a staggered rollout's natural comparison, task402 courses broken off when an actor's block
  lapses, here the expectation a sale set against the use the meter then recorded). `causal_design` and
  `population_selection` are barred in the window, and neither is honest here: nothing in the platform's assignment
  needs repairing (every 2026 respondent is on it) and no one is missing from the tracker.
- **Gap, pattern, generators:** gap objective (the ratings and the driver analysis report the fall correctly and are
  not what the decision is scored on, the change that produced it); pattern none; generators G6 (composition shift: the
  2026 pool shifted on each customer's disconfirmation while the satisfaction curve held) and G14 (conditioned yield:
  the pooled driver weights do not apply to a pool conditioned on what each customer was quoted).
- **Furniture** (read off `guard.py check` against the live window task399, task400, task402): forum `executive_team`
  (the executive signs the phase 2 cutover off), forcing event `cutover_or_migration` (phase 2 on 1 February 2027),
  organisation `utility_or_infrastructure`, role `research_desk` (the head of customer insight owns the tracker),
  context artifact `close_out_summary` (the platform's phase 1 close-out report, which reports the programme's own
  defects and never ranks causes of the fall), calibration none. None is held by the window.
- **People** (`guard.py names --geo uk --seed 401`): Rita Fisher (head of customer insight), Joanne O'Brien (chief
  customer officer), Elliot Davies (billing programme director). The draw's first picks (Gerard Norris, Sylvia
  Phillips) were architecture 1's personas, unshipped, and are set aside with Aimee Williams. None appears in the prompt.
- **Data-native sentence:** a new customer's first bills and first Direct Debit review are set by what the meter records,
  while what the customer was told to expect was set at the switch from the use they gave or, from May 2025, from
  Ofgem's medium typical consumption when they gave none, so the six-month tracker measures the distance between the
  two, and the supplier keeps the quote and the meter in different systems under different keys.
- **Abstraction sentence:** a fall in a share of satisfied members is booked to the service the members' own ratings
  blame, when it comes from the gap between what each member was told to expect at joining and what their own later use
  then cost, visible only by setting the joining record against each member's measured use. It is not writable against
  any approved build.
- **Same-puzzle and library tests:** the stump sentence is not "use X on Y" with X a named correction. The field's
  method (key driver analysis with Shapley shares, the client card's first pattern) is rung 0 and files the wrong
  answer; the decisive step is the judgment that this fall was formed against an expectation the sale set, which the
  driver analysis cannot see because no rating measures it. The guard's same-puzzle and same-driver NOTEs (task121 v5,
  task181 v6) are differentiated on the card.
- **Semantic screen, one line per nearest build on the insight it spends** (`guard.py mechanisms --objective
  root-cause`, the brief's list and the guard's nearest drivers):
  - task121 v4 (a satisfaction fall read on the operating conditions each journey ran under, because ratings of every
    candidate move with the overall verdict): here the operating record is the default's own rung (bills, Direct Debit
    reviews); what decides is a sales record no conditions file carries. task121 (rest rebuilt from duty records): no
    rest or duty here.
  - task129 (exposure and surroundings under a reliability standard), task202 (a source's input reaching the layer a
    response draws on), task398 (a path-dependent rule re-run), task399 (an advocate's absence at each call), task400 (a
    staggered rollout's natural comparison), task402 (courses broken off when an actor's block lapses, the loss read as
    the wait's), task187 (a shortfall against a reference curve at matched conditions): none sets an expectation given
    at entry against the cost the member then met.
  - task401 v1 (a composition shift by closures behind a credited effect): no pool lost or gained members here; each
    respondent's own quote moved. task401 v2 (a dated shock meeting each unit's own sensitive phase): no shock, no phase.
  - task181 v6 (cases traced through time-ordered records to a shared resource that handled them): nothing handled the
    customers differently. task474 v7 (an instrument's change read through members who sat both): no instrument changed.
  - task13, task11, task36, task50, task72, task84, task111, task500 (labels against evidence, a threshold rebate, a
    filed exclusion, exposure inside a funded window, an owner across transfers, copies on a composite key, which cause
    operates forward, a matched-reference method): none is an expectation set at a sale.
- **The three go/no-go screens, measured on the clean truth before the card** (`scratchpad/t401/a3/proto_e2.py` to
  `proto_e5.py`, 20 seeds unless stated; levels set first and cited under Sources):
  1. **Realistic levels.** Ofgem's medium typical consumption (2,700 kWh electricity, 11,500 kWh gas) against household
     use spread as the national consumption statistics show (lognormal, about 0.5 and 0.45 in logs), 45 per cent of
     switchers giving no use, six-month satisfaction near 78 per cent, a 30 per cent overrun worth about 25 points. In
     the base-wide relationship tracker the quote default carries only 0.54 points (1.35 if 2025's joiners used a fifth
     more) against a fall whose draw-to-draw spread is 0.66 (`proto_e2.py`): it fails, so the build runs on the
     six-month new-customer tracker, where every respondent was quoted at the switch. There the quote default carries
     2.31 points (sd 0.23) of a 3.14-point fall (sd 0.62), the platform's own effect is 0.36, and the default's driver
     analysis books 1.61 (sd 0.22) to the platform: **lever 1.25 points (sd 0.22), 1.00 to 1.47 across overrun effects
     of 3.0 to 5.5 in the logit.**
  2. **The golden's method holds the call.** Every form of the disconfirmation that keeps the overrun's size names the
     quote default: kinked log cost ratio 2.59, pounds 2.41, kWh ratio 2.01, first-review Direct Debit rise 2.70,
     flags at 20 and 30 per cent 1.71 and 2.18, kinked linear probability 2.53; **the lowest, 1.71, against an
     unexplained residual (the fall less the quote default, the tariff rise and the contact centre) of at most 0.83.**
     A symmetric linear term (1.52) still clears it; a 10 per cent flag (0.93) falls inside it and is rejected by the
     data, since satisfaction keeps falling with the overrun's size inside the flagged group (stage 2 asserts the fit).
  3. **No easy completion.** The use each customer was quoted on enters no default rung; once it is in hand the call
     holds across the forms above; and the cracker's flexible rungs all land wrong: **Shapley key driver analysis puts
     62 per cent (sd 5) of the fall on billing accuracy (the platform); first-review Direct Debit rises over a quarter
     went from 8.8 to 14.2 per cent of respondents, every one on the new platform (the platform's reviews); a use-by-
     period model books the fall to high-use 2026 respondents (the October tariff rise).**
- **Sources:** Ofgem, typical domestic consumption values (medium 2,700 kWh electricity, 11,500 kWh gas, from April
  2023) for the quote default; the Department for Energy Security and Net Zero's sub-national and NEED domestic
  consumption statistics for the spread of household use; the CMA Energy Market Investigation final report (2016) on
  how many customers do not know their annual use; Ofgem's Direct Debit guidance (2023) for how payments are set and
  reviewed; Oliver (1980, Journal of Marketing Research) and Anderson and Sullivan (1993, Marketing Science) for
  expectation-disconfirmation and its asymmetry; Fornell and colleagues (1996, Journal of Marketing) for the ACSI's
  expectations construct; Ofgem's consumer perceptions research for the level of supplier satisfaction. Every row in
  the pack is constructed and declared synthetic in `metadata.json`; no real supplier, vendor or comparison site is
  named.

## Default path

1. Read the six-month tracker for H1 2025 and H1 2026 (the vendor's export changed layout in January 2026) and take
   the share satisfied the measurement framework files.
2. Run the field's key driver analysis: overall satisfaction on the attribute ratings (billing accuracy, bill clarity,
   value for money, ease of contact, resolution, the app), Shapley shares; carry each attribute's change through its
   share: billing accuracy and bill clarity carry about two thirds of the 8.7-point fall, value for money a quarter.
3. Link the respondents to their accounts and payments (account numbers re-mapped at migration): every H1 2026
   respondent is billed on the new platform, the platform's close-out report shows estimated bills rising after
   go-live, and the Direct Debit reviews moved little (the first payment is set from the meter point's industry
   quantity), so nothing on the payment side competes with the platform.
4. Check the other rivals: the October tariff rise (variable-tariff respondents), the contact centre transfer
   (respondents who called), use bands: each moves a few tenths.
5. Book the fall to the billing platform and hold phase 2 for remediation.

Ends on: the billing platform carries most of the fall, about 6 of the 8.7 points through the billing ratings, so
phase 2 is held.
Golden: from May 2025 the quote journey stopped pre-filling each meter point's industry annual quantity, so customers
were quoted on use they typed in or on typical values; those whose meter point's annual quantity cost more than their
quote carry most of the 8.7 points, while customers whose quote covered it were as satisfied in H1 2026 on the new
platform (81.0 per cent) as in H1 2025 on the old (79.1); the platform is not what pulled satisfaction down, phase 2 can
cut over, and the fix is the quote journey.

## Stump sentence

A competent solver runs key driver analysis on the six-month tracker, sees billing accuracy and bill clarity carry about
two thirds of the 8.7-point fall, finds every H1 2026 respondent billed on the new platform, and books about 6 points to
the billing platform, holding phase 2, because they never set the annual cost each customer was quoted at the switch
against the cost of the annual quantity their meter point then showed, which puts most of the fall on the May 2025
quote journey's quotes and leaves the platform about a point at most.

## Three rules

Task type: `customer-satisfaction-driver-analysis` (Marketing and Consumer Research), which serves Root-Cause Analysis
in the taxonomy; attributing a satisfaction movement to its drivers is the task type's core.
Domain test: the deciding quantity is each driver's contribution to the fall in the share of satisfied new customers,
estimated by a satisfaction driver model that carries each customer's disconfirmation (the cost of the use the meter
recorded against the cost the customer was quoted at the switch), the expectation-disconfirmation paradigm and the
ACSI's expectations construct.
Swap: "six-month satisfaction fell because customers' bills ran above the use they were quoted on" read with school or
grid nouns ("attainment fell because pupils' bills ran above their quote") no longer parses; no school, ward or
substation has a sale that set an expectation, a meter that later measured the thing quoted, and a tracker of how the
customer felt about the difference.
Layer 1: the tracker vendor's export changed in January 2026 (coded columns and dd/mm/yyyy dates with numeric answers,
then labels and UTC timestamps; partial responses and re-invited accounts answering twice in both) (the two survey
vendors); legacy eight-digit account numbers against the platform's ten-digit ones, the crosswalk held only in the load
log (the migration); registrations keyed by account and meter point, quotes by quote reference, the tracker by account
(the sales system and the platforms); industry annual quantities as several dated rows per meter point, revised after
reads (the industry data flows); dual fuel as two registration rows, gas often starting days later (the switching
process); tariffs by region with effective dates, variable rates stepping each quarter and fixed products holding
their launch rates (the pricing team); UTC in the platform's load log and the 2026 export against UK local dates in
the legacy exports across the clock changes. Each is produced by the system named; none is placed to be caught.
Layer 2: field method (the satisfaction driver model done right): the driver set must carry what each customer was led
to expect, the disconfirmation that satisfaction is formed against, which no attribute rating measures.
Decisive step: setting the annual cost each respondent was quoted at the switch against the cost, at the same tariff, of
the annual quantity their meter point showed six months on (negative disconfirmation, a quantity of each customer that
no file holds), and finding that customers whose quote covered that cost held their H1 2025 level on the new platform
while the fall sits with those it did not cover.
Not semantics: every field, code, unit and date can be read correctly (the reads' flags, the registers, kWh, pence
against pounds, UTC against local time, the re-mapped accounts) and the driver analysis still books the fall to the
platform, because the error is in which driver the model carries, not in reading any column.
Not rule application: no filed rule or procedure sets a quote against metered use or says satisfaction is formed
against expectation; executing the measurement framework, the cutover plan and the tariff terms files the
default. The enumerated family (key driver analysis linear and Shapley; the payment linkage; after the link, metered use
level, the Direct Debit change and the quote-basis split; the gap in seven forms) spans the platform at 5.5 to 8.1
points on every route that skips the gap and the quote at 5.0 to 9.0 on every gap form (`## Ladder`); the standing
family once the fit rules out the symmetric forms (twice the log-likelihood gap 119 and 225) spans 7.1 to 9.0 on the
quote with the platform's residual between -0.9 and 1.1; the ruling-out is the fit itself, quiet, on a construction
across three files the question gives no reason to join (the quotes, the meter point quantities, the tariffs).
Analyst test: a strong analyst who reads every rating, quote and meter record correctly runs key driver analysis with
Shapley shares, links the respondents to their accounts and payments, and books about 6 of the 8.7 points to the
billing platform, holding phase 2 (the default path's `Ends on:`).
Estimand: the supplier's satisfaction measurement framework (a governing document in its own genre) files the WHAT
only: the population (customers who answered the tracker's six-month survey), the two half-years (responses received 1
January to 30 June 2025 and 2026), the measure (the share answering 4 or 5 to the overall question) and the fall between
them as the movement a review explains; it files no counterfactual and names no driver model, quote, consumption or
expectation.
No decoy: nothing is planted to be caught; no memo, briefing, draft or stakeholder figure argues for the platform, the
close-out report states the programme's own defects and no cause of the fall, and no file computes a driver's share.
No certified replay: no certified or published figure is reproduced to recover a method; the tracker's published
monthly shares agree with the respondents' records under every route.
Domain close call: Energy Systems and Utilities carries load, capacity, reliability, tariffs, assets and savings, and
none of its task types reads customer satisfaction; the deciding quantity here is a satisfaction driver attribution, so
the build sits in Marketing and Consumer Research, with the supplier as the setting and the energy shown where it is
honest (metered use, tariffs, Direct Debit reviews).
Lesson: satisfaction is formed against expectation, so before a fall is booked to the service the ratings name, a
driver analysis must carry what each customer was led to expect at the sale; no build on file teaches
expectation-disconfirmation from a sales record.

## Survivor anatomy

Actor: the deciding property, how far the cost of each customer's metered annual quantity ran above the cost their quote
projected, has no column in any file; the quote log holds the quoted use and cost (no field says where the use came
from), the meter point file holds each MPAN's EAC and each MPRN's AQ with their effective dates, and the tariffs hold
the rates.
Link: the comparison of the quote's assumed use with metered annual use is a cross-file comparison the driver analysis
never asks for, joined through quote references and meter point numbers to accounts re-numbered at migration.
Reflex: the field's method, key driver analysis with Shapley shares, is rung 0 and books about three fifths of the fall
to billing accuracy, so to the platform.
Back-test: the driver analysis explains H1 2025's satisfaction well with stable weights, and the platform's close-out
report shows estimated bills rising after go-live (true and small); the textbook route validates.
Second use: the quote log and the registrations carry an ask on switches by channel; the meter point quantities carry
the phase 2 scope ask's annual quantities; the tracker carries the measure itself; the Direct Debit history is a declared
distractor (the default reads it, the golden does not).
Shock: the fall is modest, ordinary movement; the visible events of the year are the platform go-live, the October
tariff rise and the contact centre transfer, and no shipped statistic sorts the quote default's customers to an end.
Pins: the measurement framework files the population, the windows, the measure and the fall to be explained; the
cutover plan files the asks' scope and weeks; no
filed sentence names quotes, typical consumption, expectations, disconfirmation, a counterfactual or a comparison group.

## Readability screen

The reflex row is enumerated from the field's vocabulary for the deciding quantity (a driver's part in a satisfaction
movement): key driver analysis, relative importance, operational linkage of responses, segment drill-down.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | 7 Organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 key driver analysis, Shapley shares | the framework files the measure | ratings are columns | the field's method | none | n/a | n/a | n/a | readable |
| R1 payment linkage: platform, estimated bills, Direct Debit reviews | the close-out report states the estimated-bill rise | platform by account, reviews by row | operational linkage | close-out ties | n/a | n/a | n/a | readable |
| R2 after the link: use level, Direct Debit change, quote-basis split | none | each a column or one join | segment drill-down | none | n/a | one group-by | n/a | readable |
| R3 (decisive) quoted annual cost against the cost of the meter point's annual quantity | silent: no sentence names quotes against quantities | silent: no column holds the gap and no field says where a quote's use came from | silent: the reflex is R0 | silent: nothing scores the quotes | silent: the battery never sets one system's quote against another's quantity | silent: a ratio of a quoted cost to a cost built from two other files at the quote's rates | silent: the quote log ships for the switches ask, the quantities for the phase 2 ask | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternatives and the call under each | Ruled out by |
|---|---|---|---|---|
| SF1 | satisfied | 4 or 5 on the 1 to 5 overall question | top box only; mean score: quote leads under each | the framework's measure sentence; same call (asserted) |
| SF2 | the half-years | responses received 1 January to 30 June | invitations sent in the window; joined July to December: same call | the framework's window sentence; same call |
| SF3 | a response | an answered overall question | any started survey: same call | the framework's counting sentence |
| SF4 | a respondent twice in a wave | the first answered response | both, the last: same call | the framework's one-per-account sentence; same call |
| SF5 | the 2026 export's text labels | the vendor's label for each scale point | numeric order by file position: same call | the framework's scale table |
| SF6 | the quote that set the expectation | the accepted quote the registration names | the customer's latest or first quote: same call | the registration's quote reference; same call (asserted) |
| SF7 | the meter point's annual quantity | the EAC or AQ in force on the response date | at six months from supply start; the latest held: same call | same call (asserted over the three) |
| SF8 | dual fuel | the whole projected annual cost against the whole cost | fuel by fuel: same call | same call (asserted) |
| SF9 | the rates the gap is costed at | the quote's own rates | current rates (adds October's rise): same call | same call (asserted) |
| SF10 | two-rate meters | none: every tariff in the pack is single-rate | n/a | asserted (no two-rate tariff code) |
| SF11 | the cause's name | the quote journey's quotes from May 2025 | the typical values alone; the use customers typed alone: each names the quote journey | same call; the basis split alone does not name it (`## Ladder`, point 2) |
| SF12 | the fall | percentage points between the two shares | relative change: same call | the framework's reporting sentence |

## Ladder

Measured on the clean truth (`generator/world.py`, `generator/ladder.py`, 20 seeds, mean (sd); the shipped seed is
asserted in `checks.py` at the cut). Six-month satisfaction 76.1 to 67.4 per cent, a fall of 8.72 (0.60). Truth: the
quote journey's quotes 7.95 (0.18), the platform 0.37, the October tariff rise 0.31, the contact centre 0.32. Mean log
gap 0.00 in H1 2025 and 0.055 in H1 2026; respondents more than a tenth over their quote 10.0 and 44.2 per cent.

| Route | Quote | Platform (the 2026 term) | Tariff rise | Contact | Names |
|---|---|---|---|---|---|
| R0 key driver analysis, Shapley | 0 | billing accuracy 57.0 and clarity 11.0 per cent of the fall (about 6 points) | value 26.0 per cent | 1.8 per cent | platform |
| R2a metered use level | 0.00 (use) | 8.14 (0.74) | 0.27 | 0.42 | platform 20 of 20 |
| R2b Direct Debit change | 0.35 (the change) | 8.13 (0.75) | -0.07 | 0.42 | platform 20 of 20 |
| R2c quote-basis split | 2.89 (basis, collinear with 2026) | 5.54 (0.86) | 0.28 | 0.42 | platform 19 of 20 |
| R3 gap, kinked at zero (best fit) | 8.98 (0.38) | -0.92 | 0.25 | 0.38 | quote 20 of 20 |
| R3 gap, linear in the log | 5.22 (0.28) | 2.93 | 0.24 | 0.39 | quote 20 of 20 |
| R3 gap, pounds | 4.97 (0.29) | 3.21 | 0.24 | 0.38 | quote 20 of 20 |
| R3 gap, quintile bands | 7.63 (0.61) | 0.15 | 0.24 | 0.39 | quote 20 of 20 |
| R3 gap, over by 10, 20, 30 per cent | 7.91, 8.93, 7.12 | 0.27, -0.84, 1.09 | 0.26 | 0.40 | quote 20 of 20 each |
| Fall split on the kinked route, Shapley against every order | 8.99 (8.93 to 9.05) | -0.88 (-0.92 to -0.83) | 0.24 | 0.37 | quote |

The coordinator's five points, each closed on these rows:
1. **After the link the estimators still split.** With every respondent's quote joined to their meter point's quantity,
   metered use level names the platform 20 of 20, the Direct Debit change 20 of 20, the quote-basis split 19 of 20 (it is
   collinear with the 2026 platform), and only the gap names the quote, in every form. The rung where the link alone
   still leaves the platform is R2: a solver holding both files who builds a level, a payment change or a basis split
   files the platform. The analytical choice that survives the link is the expectation construct: the cost each customer
   was told against the cost their own quantity then carried.
2. **A default quote is not what decides.** No field says where a quote's use came from, and recognising Ofgem's medium
   values names only the typical-value half: in H1 2026 the typical-value respondents were 66.4 per cent satisfied and
   the typed-use respondents 68.1, both far under H1 2025's 76.1, with 40.3 and 47.3 per cent of them more than a tenth
   over their quote. The default-or-not split dilutes; the gap decides.
3. **The Direct Debit chain is quiet.** The first payment is set from the meter point's industry annual quantity (the
   supplier's practice under Ofgem's best-available-information rule; no file states it), so reviews move by the quantity's own
   revision and October's rise: the change books 0.35 points. The review records carry the codes a GB supplier's billing
   system writes (scheduled review, tariff change, customer request, payment failure, meter exchange); none says why use
   differed from a quote, and no record carries the quote.
4. **The call's rule and margin.** The named cause is the largest contributor to the fall. The quote leads every other
   candidate in every gap form, 20 of 20; the weakest form (pounds, symmetric) books 4.97 against a platform residual
   of 3.21; the 10 per cent flag books 7.91. The fit rejects the symmetric forms (twice the log-likelihood gap 119 for
   the linear form and 225 for pounds against the kinked form), asserted in `checks.py`. Shapley against every sequential
   order moves the quote's part by 0.12. Key driver analysis in both forms names the platform.
5. **The filed estimand is WHAT only.** The framework files the population, the windows, the measure and the fall; it
   files no counterfactual and names no driver construction (`## Three rules`, Estimand).

The graded set, at precisions every route that takes the step reproduces (asserted at the cut): the call (the May 2025
quote journey's quotes, not the platform); the share satisfied in each half-year; the share satisfied among respondents
whose quote covered the cost of their meter point's annual quantity, in each half-year (79.1 and 81.0 on the means
above; a comparison with no fitted parameter, the zero line set by the quote itself); the share of respondents whose
quote fell short, in each half-year; the quote's part of the fall stated as more than half (the weakest form gives 57
per cent, the standing forms 82 per cent and up); the tariff rise and the contact centre each under half a point. The
flip condition: the platform would carry the fall if respondents whose quote covered their cost had fallen as far as
the rest. No per-cause point figure is graded.

Pricing sequence, in the graded figure's units: (1) the residue the WHAT leaves is a method (which driver construction
carries the expectation), not a knob; (2) the move needs about 7 points of a 9-point fall, and the affected population
could produce 9; (3) the one-group-by routes are R2a to R2c, each measured above; (4) the gap's standard error on the
quote's part is about 0.3 to 0.4 points; (5) the call is a verdict on one named cause about 7 points from the
platform's, more than nine of its own standard errors; (6) n/a (no variance correction); (7) the zero line comes from
the quote itself, so no subset hands over a rate; (8) the reflex sweep is the table above, run as code.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | respondents who answered the overall question in each half-year | filed in the framework; C1 |
| 2 | Unit of account | the respondent (one account) | filed; SF4 one per account |
| 3 | Attribution window | the response date | filed; C1, no response on a boundary day moves a share across a bin (asserted) |
| 4 | As-of dating | the meter point quantity in force on the response date | C1 across three as-of rules (SF7, asserted) |
| 5 | Version basis | the quote as accepted; the quantity as held | C1 (SF6, SF7) |
| 6 | Denominator | answered overall questions | filed |
| 7 | Weighting | unweighted shares | filed (the framework reports unweighted shares) |
| 8 | Window length | half-years | filed |
| 9 | Boundary inclusivity | 1 January to 30 June inclusive | filed; C1 |
| 10 | Rounding path | shares to one decimal, once | filed in the prompt's rounding sentence |
| 11 | Tie-break | none needed: the quote leads by about 7 points | C1 |
| 12 | Maturity and censoring | none: every respondent has six months of supply | C1 |
| 13 | Order of operations | cost the quoted and metered quantities at the same rates, then compare | C1 (SF9, asserted) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | first answered response per account per wave | filed (SF4) |
| 16 | Identity normalisation | quote reference to registration to account (legacy and platform numbers) | the systems' own keys and the migration crosswalk; C4 |
| 17 | Netting against gross | customers under their quote are not netted against those over | the graded set reports both shares separately |
| 18 | Dimensional units | kWh in the quote and the quantities; pounds a year in the quote | units in the data; C4 |
| 19 | Code and status semantics | the vendor's scale labels; review reason codes | the framework's scale table; codes never decide |
| 20 | Integerisation | none | C1 |
| 21 | Clause scope | the framework's measure covers the six-month survey only | filed scope |
| 22 | Forward window contents | the call names a cause; nothing is forecast | n/a |

## Literal reader

Executed word for word, the framework's measure gives 76.1 per cent satisfied in H1 2025 and 67.4 in H1 2026 (the shipped
seed's values asserted at the cut); the question asks what pulled it down; the shipped documents name the year's
changes (the quote and switch journey relaunch, the billing platform, the October tariff rise, the contact centre move);
every reading of SF1 to SF12 names the quote journey's quotes as the largest contributor (asserted as a product over the
rows that touch the deciding quantity, SF6 x SF7 x SF9); the default comes from an easy method (key driver analysis, a
payment linkage) on the same literal estimand, never from another reading.

## Oracles

- The platform's phase 1 close-out report: estimated bills rose for six weeks after go-live (true, small); it confirms
  the wrong path and ties under every basis.
- The tracker vendor's monthly summary table: ties to the respondents' records under every route; arbitrates nothing.
- The Direct Debit history (a declared distractor): reviews move little under every route.
- Nothing ties only under the golden.

## Ask sheet

Measured on the cut pack by `generator/ceiling.py` (reads only `target/` and `figures.json`, shares no code with the
generator). Each ask sits on rows the call never reads, asserted in `checks.py` (no respondent in a reload chain or a
pilot row, none with a withdrawn or split registration). The contact centre ask planned at the draw was cut with its
two call logs: the contact rival is carried by the tracker's own contact question.
- **Ask A, phase 2's scope** (16 figures: accounts by region, total GWh electricity and gas). Files: the legacy
  accounts extract, the switching flows, the meter point quantities, the cutover plan (the WHAT: accounts still supplied
  on 1 November 2026 on at least one meter point; quantities in force that day). Primary (D2, a state rebuilt from an
  event log): a completed loss later returned as an erroneous transfer, so the meter point is ours again on 1 November
  while the legacy status still reads final bill pending. Hazards: withdrawn losses whose legacy status was never
  reverted; losses notified with an effective date after 1 November; a dual-fuel account lost on one fuel; later
  quantity revisions dated 3 to 12 November.
- **Ask B, phase 1's loads** (18 figures: nine UK weeks by electricity-only and dual fuel). File: the load log. The
  cutover plan files each account once in the week its last load completed, UK time. Primary (D7, the true key in a
  chain): a reload from the platform's exception queue carries the failed load's platform number as its source
  reference, so the account is one only through the chain; benign twin: pilot accounts whose source reference is also
  a platform number with no earlier load. Hazard: UTC stamps against UK weeks across 26 October.
- **Ask C, switches by channel** (24 figures: four channels by six months). Files: the registrations and the quote
  log. The asking sentence files one switch per customer in the month its first supply started, none withdrawn.
  Primary (D1, one event in two records): a gas registration rejected for a meter point mismatch and raised again under
  its own reference, days after the electricity one. Hazards: withdrawals in the cooling-off period, re-registrations
  after a withdrawal, dual fuel as two rows.

| Response (cracker sheet) | Ask A | Ask B | Ask C | Verdict |
|---|---|---|---|---|
| Cracker: lands the call, every filed convention, the hygiene battery | 0 of 16 | 0 of 18 | 0 of 24 | miss |
| Mirror: the most attractive wrong rung (Live status, rows by UTC week, registration rows) | 0 of 16 | 0 of 18 | 0 of 24 | miss |
| Full includer: notices and resolves each ask's primary | 16 of 16 | 18 of 18 | 24 of 24 | keeps |

Pair ceiling: 28.5 (cracker 45.0 on the call, mirror 12.0 off it), measured; with a full includer on the call it is 56.0.
Mirror leakage: 0.0 per cent.
Measured by: generator/ceiling.py on the cut pack (target digest bade64f2), 2026-11-03.
Owed before ship: a second device from another family on each ask with a figure block disjoint from the primary's, so
the full includer misses a block (`supplemental-stumping` Part 1, rule 2).

## Tried and rejected

- 2026-11-03, the seed's world (RC07, a supplier's January imbalance bill against plant trips and low wind), every
  candidate screened before the card. The trips' effect on the supplier's own imbalance volume at the system price is
  settlement accounting: each unit's metered shortfall against its notified output in the window before the desk can
  re-trade, priced per settlement period, reconciles exactly to the bill, so nothing is left to decide (rule
  application). The price the supplier would have faced without its own units' trips re-runs the system's price
  formation on the changed path, task398's spent insight in other nouns. Netting the desk's replacement trades out of a
  trip's cost is the same insight again (the cause owns the response it triggered). Which settlement periods a trip owns
  (gate closure, the share of an interval) is a market rule or a time-semantics read, banned as decisive. The cost
  spike's drivers identified from interval data need a driver the settlement data does not meter, and in this market
  every driver is metered. Dual imbalance pricing makes the portfolio's net position matter, but executing the price
  rule on the with-and-without positions is rule application. The honest strategy, `decomposition_attribution`, and the
  seed's forum (the board) are both held by task398 in the window. Moved, per `CLAUDE.md`.
- 2026-11-03, other moves screened and set aside before this draw: gas turbine inlet icing in freezing fog read against
  temperature (the winter measures on the table name the mechanism, so a reader checks each one's conditions and lands
  it; two cheap routes); a groundwater nitrate rise read against travel time through the unsaturated zone (task202's
  reach-the-receptor insight in other nouns, and the field's first move); a bathing water's sources separated by marker
  decay in transit (task202's reach and task248's transit loss); selective in-migration behind a widening mortality gap
  (task68's entrants and task134 v2's newcomers, and the prior-diagnosis read lands the decision without it); depletion
  of the frail by a winter's deaths before an intervention's evaluation (dead on lever at realistic excess mortality, as
  task173's screens found for mortality displacement, and its frailty proxy forks the expectation); the Will Rogers
  stage migration (the field's stage-specific comparison collapses into which stage field to read, data semantics);
  attenuation by a mediator's or a predictor's unreliability (task262's insight); regression dilution of a risk factor
  in a disparity decomposition (task262 again); a funnel's downstream rate falling when an upstream filter loosened (the
  end-to-end funnel is the field's reflex); a two-stage complaint escalation's selection (the per-complaint view lands it);
  a mode or non-response shift in a satisfaction tracker (task121 v4's linkage and halo).
- 2026-11-03, prototypes before the card (`scratchpad/t401/proto1.py` to `proto3.py`, expected values with Poisson draws):
  winter-only counts in a city of 600,000 left the default and the golden overlapping across draws (default 5th to 95th
  percentile 23 to 179, golden -38 to 119), so the build runs at integrated-care-system scale over October-to-September
  years with the closures in the year between the baseline and the pilot; there the default's expectation is 912 (spread
  208) against a golden of 392 (spread 215, truth 389), and the trend-adjusted golden forms agree within a median of 6.4
  admissions once the framework files the comparison; without the comparison filed, the no-trend form differs from them
  by a median of 77 (a fork the framework's comparison sentence closes, a WHAT naming no method).
- 2026-11-03, architecture 1 dies at stage 2 on the coordinator's realism check, before any data was cut. Set to published
  English levels (a care home resident aged 80 and over about 0.70 to 0.75 emergency admissions a year, community
  residents by band 0.24 to 0.58, a same-age ratio near two, not the prototype's five), the composition lever is about
  113 admissions for the 440 Core20 residents the closures moved (sd 26), against draw-to-draw spreads of 202 in the
  default and 214 in the golden on a one-year baseline and about 160 on three years (`scratchpad/t401/proto4.py`, 400
  draws). A bar at the midpoint separates default above from golden below in 22 per cent of draws (27 on three years);
  900 residents moved gives 41 to 51 per cent and 1,400 gives 58 to 72, and 1,400 is two fifths of Core20's care home
  places in one system closing in a year, which no honest care group failure produces. A larger 80 and over population
  scales the spread with the lever, and a bar nearer the truth only moves the coin flip. The stump was the noise. Re-rooted.
- 2026-11-03, the redraw's other candidates, set aside before the card: regression to the mean of units chosen on a
  noisy outcome (task130 v3 landed it; task149 and task174 rejected it on that lineage); a satisfaction fall read against
  the conditions each respondent met, or a tracker's mode or response shift (task121 v4); a storable good's purchases
  pulled forward before an announced price rise and paid back after (the pre-rise spike is the pack's largest movement
  and announces the step); a distributor's orders falling as channel stock is drawn down (sell-through is the field's
  reflex and lands it); a local policy confounded by a common shock loading on each unit's exposure (the council
  furniture is banned in the window and the exposure needs data no operator holds); transformer insulation ageing under
  new loads (electricity is spent, task129, task196, task201, task303, and F6's 46 already holds a rate stationary in a
  constructed exposure); in the crop world itself, a hybrid placed on clubroot or hail-struck fields (a lab result or an
  adjuster's claim names the field, readable), and a hybrid whose own later flowering met the heat (`crop2.py`: a three-day
  shift moves the season-long panel only 3 to 5 per cent, and the forward step then needs a climatology fork).
- 2026-11-03, prototypes for architecture 2 (`scratchpad/t401/crop1.py`, `crop3.py`, ten weather draws each, the
  hybrid's own effect nil and equal phenology): with most of the hybrid's seed late by 8 to 14 days, the season-long
  panel files minus 9.1 per cent (sd 9.8 across weather draws), farm-by-year effects minus 9.3, a linear seeding-date term
  minus 7.0, raw 2026 means minus 11.6, the flowering-window exposure minus 0.1 (sd 0.9), its variants (thresholds 28 and
  31 C, windows 14 and 22 days, 490 and 550 heat units to flower) minus 3.5 to plus 0.5, and fields seeded on the same
  days on the same farm minus 0.6 (the same insight by matching). The spread across draws is the weather's: the pack's
  July heat wave and seed delay are set by design, never picked from draws.
- 2026-11-03, architecture 2 dies at stage 2 on its own ladder (`generator/ladder.py`, seed 4012026, measured at commit
  7d3a3cd), before any data was cut. First, the golden's own method forks the main call: the flowering-window variants
  land +2.1 (28 C), -2.5 (31 C), -12.0 (a 14-day window), +3.4 (a 22-day window), -8.2 (490 heat units to flower) and
  +4.9 (550 units) against the 5 per cent bar, so two agronomically defensible variants drop the hybrid and four keep
  it; filing the window or the heat metric would name the decisive step, and the generator cannot close the spread under
  realistic catch-up (a 17-day seeding gap became a 6-day flowering gap). Second, the stump rests on a functional-form
  choice: the default path's own rung 4 already rebuilds seeding dates from the seeder's logs, and every flexible form of
  that variable then lands the golden (seeding-week bins +3.6, a cubic +4.4, same-day matching +9.3); only a linear term
  stays wrong (-10.1 in the season panel, -8.3 with farm-by-year effects), so Gate F would rest on the solver choosing a
  straight line. Spent; one architecture per world, so the crop and weather world is closed to this slot. Re-rooted at
  architecture 3 in another client domain, world and dataset.
- 2026-11-03, architecture 3's draw, candidates set aside before the card. In the never-built satisfaction cell, the
  client card's moves (Shapley shares, a Net Promoter change's multinomial error, penalty against reward, loyalty read
  on later behaviour) are reflexes, and reading a fall on the conditions each response was made under is task121 v4's.
  A broadband provider's speed promise against delivered speed died on the regulator's own reflex (the share of plan
  speed delivered is the standard metric). The energy quote mechanism in the supplier's base-wide relationship tracker
  carried 0.54 points (1.35 with 2025's joiners using a fifth more) against a fall whose draw-to-draw spread is 0.66
  (`scratchpad/t401/a3/proto_e2.py`), architecture 1's death in other nouns, so the build runs on the six-month
  new-customer tracker. In the concentrated form a first harness with the platform's own effect at 1.3 points left the
  golden's 10 and 20 per cent flags (0.98, 1.78) under the residual (`proto_e3.py`); at the platform's realistic small
  effect the standing forms clear it (`proto_e4.py`). Other cells screened: education multilevel (the client's three
  cards are reflexes; teacher reassignment and special-needs assessment waits fail screen 1 or repeat the actor family),
  health equity (an inhaler switch run practice by practice is task400's staggered rollout; discharge after a missed
  appointment repeats task402's broken-off cases), pollution source attribution (every wind, tide and capture-zone route
  is task202's reach), water network reliability (the isolation extent per burst is one group-by; transients read
  through topology sit beside task303), the human factors cells (the pairing is barred against task400), and
  interpretability (ruled a backdrop at task129 v1).
- 2026-11-03, stage 2 on architecture 3, three cuts. (a) The first world set the first Direct Debit from the quote, so
  the review rise was a near-copy of the gap and a solver asking why payments rose walked to the quote; the payment is
  now set from the meter point's industry quantity at registration, and the Direct Debit change books 0.35 points and
  names the platform (`## Ladder`, R2b). (b) A Direct Debit policy document stating that rule was drafted and dropped:
  its sentence on industry quantities would send a reader to set quotes against quantities, and the golden never needs
  it. (c) The contact centre ask and its two call logs were cut for budget; the contact rival stays on the tracker's own
  contact question. The asks' first devices as drafted (stale legacy status, re-runs keyed on the legacy reference,
  withdrawals) were each executable from the cutover plan's and the asking sentences' own pins, so they were re-sited
  onto an erroneous-transfer return, a reload chain with a pilot twin, and a gas registration raised under its own
  reference.
