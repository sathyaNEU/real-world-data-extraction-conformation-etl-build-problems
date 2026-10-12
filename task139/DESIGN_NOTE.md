# task139: Haverline Casualty Company, where the seventeen Early Return Nursing teams work in 2027 and the indemnity they save (architecture 1)

Private, never ships. A new build (wave 2), numbered from seed FC10: the seed's world, decision and quantity are kept
(a workers' compensation insurer funds seventeen nurse case-management teams of twenty places for the next accident
year, places them across eight claim segments with at most three teams a segment, and books the ultimate indemnity they
save in that accident year's pick; a randomised pilot verified by an independent actuarial review is the evidence). Its
architecture (a saving that exists only at employers with light-duty capacity, carried onto segments whose mix of such
employers differs from the pilot's) is not used: it is a conditioned yield under a composition shift, and pattern E and
`composition_mix` are spent on task137, one of the three builds before this one. The pitfall is re-found from how the
pilot's records came to exist: the pilot assigned intakes, the review verified indemnity claims, and the nurses decided
which intakes ever became indemnity claims.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task139.json`, architecture v1, registered 2026-10-12; `guard.py check` PASS (a first people draw carried four first names used in older builds and the question form repeated task137's `how-many`; both redrawn before registering); `guard.py validate` clean |
| Domain / task type | actuarial-science-insurance / claims-frequency-severity (a client domain, never drawn before): the saving is a workers' compensation pure premium, indemnity per intake as the indemnity-claim rate times the indemnity severity at ultimate, which is the frequency-severity build of the claims actuary |
| Objective | Forecasting & Predictive Modeling: the ultimate indemnity the 2027 teams will save, booked at run rate in the AY2027 indemnity pick before the year opens, forecast from the randomised pilot |
| Shape | 05 (allocation to a fixed total): seventeen teams across eight segments, each segment's teams and its saving, the total, the saving per place-day that ranks them, the note's opening and chart, and asks on rows the call never reads; arithmetic in `## Ask sheet` |
| Decision | `allocation_to_total`, answer unit `count` (teams per segment) with the saving in dollars to the nearest 10,000 |
| Mechanism | gap population (decisive: the review's file holds indemnity claims, the decision buys intakes, and which intakes become indemnity claims is the nurses' own effect), then objective (the twenty places are the scarce resource, so a team is valued per place-day, not per claim); pattern none, generators G9 (downstream survival against upstream acquisition: the measured class, indemnity claims, is the survivor of the acquired class, intakes, and survival depends on the arm) then G1 (unit of value: the place-day) and G14 (each segment's own yield); Gate G `method_or_model_selection` (two comparisons of one pilot, per verified indemnity claim and per assigned intake, the randomised design pinning the second); strategy `causal_design` (the comparison the design implies) |
| Layer 2 family / pattern | `estimand_identification` (selection on an outcome the treatment moves: comparing the arms on their indemnity claims conditions on a status the nurses changed); `own:indemnity-saving-read-per-assigned-intake` (Actuarial Science has no library patterns; the nearest lines are biomedical-clinical-research/clinical-trial-design-analysis/1, analyse as randomised, and healthcare-delivery-health-economics/payment-claims-health-plan-analytics/4, a ratio of totals over the exposure that bears it) |
| Furniture | forum `executive_team` (Haverline's executive committee approves the AY2027 plan and its indemnity pick at its December meeting), forcing event `launch_or_rollout` (the seventeen teams go live on Monday 4 January 2027), organisation family `financial_institution` (a stock workers' compensation carrier), role family `capacity_planner` (the director of medical case management places the teams), context artifact `close_out_summary` (the independent review of the pilot), calibration `gold_standard_subsample` (the review's verified ultimates on a random sample of the pilot's indemnity claims), opening `question-first`, question form `where` |
| Spine | `claims_extract_2021-2026.csv`, the claims system's listing of time-off and indemnity claims: one row per claim reported with time off work at first report, or one that later paid indemnity, January 2021 to September 2026 (about 58,000 rows); constructed |
| Deliverables | `ern_placement_ay2027.xlsx` (the placement by segment with its basis, the saving, the asks, a notes sheet), `ern_placement_note_ay2027.pdf` (a one-page note for the executive committee opening with the placement and charting each segment's saving per place-day) |
| People | drawn with `guard.py names --geo "United States" --seed 139 --n 30`, keeping only names the guard clears: Margaret York (director of medical case management, the requester), Joanna Sullivan (consulting actuary, Kellerman Pryce Actuarial, signed the pilot review), Kathleen Reilly (chief pricing actuary, owns the AY2027 indemnity pick), Joel Kelly (ERN clinical lead, ran the pilot's nurses), Kristen Hansen (claims operations, owns the triage screen and the assignment register), Juan Castillo (data engineering, the 2025 claims-system upgrade and its segment crosswalk); none appears in the prompt |

**Guard.** `guard.py check` on the scratch card: PASS after two redraws. The bans ran against task136, task137 and
task138, the three builds before this one by draw key: the strategy is off `population_selection`, `composition_mix`
and `time_semantics`, the decisive mechanism off G8, E and G16, the shape off `other` and 02, the forum off
`line_manager_or_team`, `committee_or_panel` and `customer_or_counterparty` (the seed's pricing committee became the
executive committee that approves the plan), the forcing event off `budget_or_appropriation`, `purchase_order_or_contract`
and `season_or_peak`, the organisation family off `utility_or_infrastructure`, `cooperative_or_member_body` and
`local_government` (so the carrier is a stock company, not a mutual), the role off `research_desk`, `product_manager` and
`procurement_lead`, the context artifact off `capacity_report`, `planning_thread` and `filed_standard`. A first people
draw (Kenneth, Connie, Paul, Danielle) drew four `people.first` warnings and was replaced; the question form moved from
`how-many` (task137) to `where`, which is the form of the decision (where the teams work).

**Strategy label.** Two keys were weighed for the decisive step. `population_selection` reads "who is in the
denominator", and the step does change the denominator; but every F7 build on record (25, 28, 124, 132, 229) turns on a
forward population that differs from the measured one, and here it does not: the 2027 teams take exactly the population
the pilot randomised (intakes at the daily triage). The error is the comparison, the two arms read on a status the
treatment changed, which is `causal_design` ("control or comparison choice"). The card says so in `notes`.

**Same-puzzle and same-driver tests.** Gap population, decisive G9, decision `allocation_to_total`, Gate G
`method_or_model_selection`: no build on file carries any two of the structural keys with G9 (task100 v2 and task133 v1
carry G9 under gap time). A first draft named G2 (grain) and collided on `test.same_driver` with task120's v1 lineage
(population, G2, method_or_model_selection) inside the batch; G9 is the honest code for the mechanism (the indemnity
claims are the downstream survivors of the intakes) and G2 is not on the card.

**Abstraction test.** Stripped of nouns, the driver is: an intervention assigned at random at intake changes how many of
its units go on to become the recorded costly cases as well as what those cases cost, so its effect is read per assigned
unit, each arm's own conversion times its own cost, and valued per unit of the capacity each assigned unit holds; read
per recorded case, it compares the costlier remainder of one arm with the ordinary cases of the other. The three nearest
drivers (`guard.py nearest`: task73 world ten 0.07, a capped slate bound by a processing allocation whose load depends
on re-assigned review intervals; task121 v1 lineage 0.06, a pooled effect conditioned on a state a unit holds until the
effect first strikes it; task131 0.06, a sub-unit's lift that carries spend moved from its siblings) share no latent
structure, default path or correction with it. Read by idea rather than by score, the card carries three
differentiation lines: task136 (a campaign's yield carried to new sites per member still able to respond: a
transport, and a pool built through a join; nothing here is transported), task128 (a call's effect read from a
capacity-overflow natural experiment with unmarked undiallable records: no natural experiment and no marking here, the
pilot is randomised and the bias is the nurses' own effect on which intakes pay indemnity), task124 (a rate measured on
units examined because they showed signs, carried to a population all of which will be examined: here the forward
population and the randomised one coincide).

**Data-native sentence.** Haverline's pilot assigned each intake at the daily triage, before anyone could know whether
the worker would lose more than the three-day waiting period, and an Early Return nurse's first call went to the
employer about suitable duties, so in the segments where employers can offer them a fifth to a quarter of the
programme's intakes never paid a day of indemnity; the independent review drew its verification samples from the
claims that paid indemnity, forty in each arm in each segment, so in those segments its two samples set the
programme's costlier remainder against an ordinary usual-handling group, and nothing in either file says so.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (49 builds): hazards by time since entry
(134), selection on the outcome by examination (124), a campaign's yield per untapped member (136), a retention share
conditioned on a repricing gap (137), the state at the forecast date (138), a capacity-overflow natural experiment
(128, read through its card), conditional survival (133): none reads a randomised pilot per assigned unit because the
treatment moves units out of the recorded class. `stumping/references/client/two-layer-task-design.md`: actuarial
science has no library patterns, so the pitfall comes from the `estimand_identification` family (selection on the
outcome) with the field's own frequency-severity build. `stumping/references/client/measured-drivers.md` and
`guide-to-prompt/references/exemplars.md`: under 0.25 the miss is the unit, a row taken as the decided unit while a
governing text defines another (the goods receipt, the applicant unit, the billable seat-month); here the review's row
is an indemnity claim and the protocol's unit is an intake. The seed's header and Situation (FC10) for the world only.

**World.** Haverline Casualty Company is a stock workers' compensation carrier writing Missouri employers from offices in
St. Louis and Kansas City; its claims are worked in claim units by segment, an industry group crossed with an injury
class: healthcare and social assistance, retail and warehousing, manufacturing, and construction, each split into
strains and sprains and other injuries (fractures, contusions, lacerations, crush and the rest). An intake is a claim
whose first report shows the worker off work; the claims system's triage screen sorts the day's intakes each morning.
Missouri pays temporary total disability at two-thirds of the average weekly wage up to the state maximum, nothing for
the first three days unless the disability passes fourteen days, and permanent partial disability on a rating after
maximum medical improvement; an intake whose worker is back at work inside the waiting period pays no indemnity.

Early Return Nursing (ERN) is Haverline's early-intervention nurse case management: a nurse takes an intake at triage,
calls the worker, the employer and the treating provider within a working day, arranges suitable duties where the
employer can offer them, coordinates care, and holds the file until the worker is back at full duty. The ERN pilot ran
in both offices from 1 March 2023 to 29 February 2024: the triage screen assigned each intake in the eight segments at
random, half to ERN and half to usual handling, about 1,600 intakes, and six two-nurse teams took every programme intake.
Kellerman Pryce Actuarial reviewed the pilot in 2026: it drew forty claims that had paid indemnity from each arm in each
segment (640 claims), verified each file blind to its arm, and projected each to ultimate at 30 June 2026. Its report
says what it verified and how; it does not estimate the programme's effect, which is the company's own analysis.

For 2027 the executive committee funded seventeen teams of twenty places (the programme charter, signed in October
2026). A segment's claims sit in one claim unit, and a unit can house at most three teams. Teams take their segment's
intakes at the daily triage in report order while a place is free, an intake not taken by the end of its second working
day stays with its adjuster, and a team holds a file until the worker is back at full duty. The AY2027 indemnity pick
books a programme saving at its run rate (every place in use for the full year) at the amounts the pilot verified, the
pick's severity trend and benefit-level factors applying to the whole indemnity pick afterwards (the pick memo, chief
pricing actuary).

As-of dates: the claims extract and the pilot's nurse case log were pulled on 30 September 2026; the review's
verification is at 30 June 2026 and its report is dated 14 August 2026; the charter was signed on 19 October 2026; the
request is made on Monday 9 November 2026, for the executive committee's plan meeting on 8 December 2026; the teams go
live on Monday 4 January 2027.

## Default path

1. Read the charter (seventeen teams of twenty places, at most three a segment, intakes taken at triage, held to full
   duty) and the pick memo (run rate, every place in use for the year, at the amounts the pilot verified).
2. Read the review's workbook (one sheet per segment, verified ultimate temporary total, temporary partial and permanent
   partial indemnity per claim, summed), join each verified claim to the assignment register for its arm through the
   claim number (reformatted at the 2025 claims-system upgrade) and its segment through the 2025 crosswalk.
3. In each segment, the saving per managed claim is usual handling's mean verified ultimate less ERN's.
4. From the nurse case log, the place-days an ERN claim held (file open to file close, a reopened file added) for the
   programme's indemnity claims in each segment; each segment's saving per place-day is step 3 over step 4.
5. Rank the segments on saving per place-day, three teams to each of the top five and two to the sixth; check that each
   segment's 2027 intakes keep its teams' places full; the saving is each team's 7,300 place-days at its segment's
   saving per place-day, summed.

Ends on: three teams each to construction other injuries, construction strains, manufacturing other injuries,
manufacturing strains and healthcare other injuries, two to healthcare strains, none to the retail segments; about 1.6
million dollars (design-stage estimate on a prototype; the build recomputes and asserts it).
Golden: three teams each to healthcare strains, manufacturing strains, retail strains, healthcare other injuries and
one of the construction segments, two to the sixth; about 4.9 million dollars (design-stage): the saving read per
assigned intake, each arm's indemnity-claim rate (from the register and the claims extract) times its verified mean,
over the place-days an assigned ERN intake held, the short files of intakes kept at work included.

## Stump sentence

A competent solver joins the review's verified ultimates to the assignment register, takes usual handling's mean
indemnity claim less ERN's in each segment, divides by the place-days an ERN indemnity claim held and files teams weighted
to construction and manufacturing with none in retail, about 1.6 million dollars (Ends on); the step that lands it there
is reading the saving per verified indemnity claim when the nurses kept a fifth to a quarter of the strain intakes from
ever paying indemnity, so ERN's indemnity claims there are the costlier remainder and the saving per claim reads as
three to five per cent: read per assigned intake, as the pilot was randomised, the teams go to the strain segments and
save about 4.9 million dollars.

## Three rules

- **Domain test:** the deciding quantity is a workers' compensation pure premium, indemnity per intake as the
  indemnity-claim rate times the indemnity severity at ultimate, compared between the arms of a randomised pilot as it
  was randomised and valued per nurse place-day; with another field's nouns there is no three-day waiting period, no
  intake turning into an indemnity claim and no stay-at-work on suitable duties, and the task stops reading the same.
- **Analyst test:** a strong analyst who reads the protocol, the review and the charter right, joins the verified
  ultimates to their arms, compares the two arms' mean indemnity claim in each segment and values each segment's teams
  per place-day still files construction-heavy teams and about 1.6 million dollars, because the review sampled only
  claims that paid indemnity and the nurses kept part of the strain intakes from ever paying any; the same analyst
  reading the saving per assigned intake but ranking on it per claim, not per place-day, files teams in construction too.
- **Layer 1:** claim numbers written three ways (the register's pre-2025 numbers, the claims system's new numbers, the
  review's numbers with a check digit), segment codes recoded at the 2025 upgrade and joined through a crosswalk, a
  review workbook of eight sheets with header blocks and three benefit-type columns, a nurse log with reopened files on
  second rows and dates in two formats, a claims extract that mixes intakes with later indemnity conversions that were
  never intakes, and a superseded draft of the charter beside the signed one. Each is something these systems produce;
  none decides the call.
- **Layer 2:** the shortcut is to read the pilot on the claims its gold-standard file holds; the expert reads a
  randomised pilot per assigned unit, frequency and severity together, because the treatment moves units between the
  classes the records keep, and values a capacity-bound team per unit of the capacity it holds.

## Tried and rejected

- The seed's light-duty conditioned yield (the saving exists only at employers with a record of temporary-partial
  payments, carried onto segments whose mix of such employers differs from the pilot's): a conditioned yield under a
  composition shift, pattern E and `composition_mix`, both spent on task137 inside the ban window; dropped at the draw.
- The saving per place-day alone (Little's law on the pilot's files, the teams valued per place-day rather than per
  claim): a strong solver computes a capacity-bound team's yearly throughput by segment by reflex once the charter
  states twenty places; kept as a rung, never the decisive step.
- An Erlang loss model on the triage stream (intakes lost when every place is taken): the effect is under a sixth of a
  team's value at matched load, it never moves a whole team, and a replay or a monthly fluid model files a different
  figure from the formula; rejected on determinism.
- A transient count of 2027 intakes from empty teams on 4 January (the first twenty in each team): the answer turns on
  the whole duration distribution and a reading of the AY window, `time_semantics` is spent on task138; closed instead by
  the pick memo's run-rate convention.
