# task139: Haverline Workers' Compensation Trust, where the seventeen Early Return Nursing teams work in 2027 and the indemnity they save (architecture 2)

Private, never ships. Re-rooted on 2026-10-26 after the portal result on architecture 1, where both responses filed its
golden placement and credit (`## Architecture 1 record`). The world, the decision and the quantity are kept: seventeen
nurse case-management teams of twenty places placed across eight claim units with at most three a unit, the ultimate
indemnity they save booked in the AY2027 pick, a randomised pilot verified by an independent actuarial review. Two
things change. The organisation is redrawn from a stock carrier to a member-owned group self-insurance trust, because
`financial_institution` is banned against task304 among the three live builds before this draw. And the decisive step
is new, re-found from how the pilot's two random draws came to exist: the triage screen drew one in three intakes at
random and a pilot nurse called every intake it drew before the pairs were split at random, so the register records only
the second draw, while the 2027 counterfactual, a unit with no team, sits on the far side of the first.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task139.json`, architecture v2, registered 2026-10-26; architecture 1 moved to `lineage` with its fate |
| Domain / task type | actuarial-science-insurance / claims-frequency-severity (a client domain): the deciding quantity is a workers' compensation pure premium per intake, the share of intakes paying indemnity times the verified ultimate severity, under three handlings (no call, the call, the call and a file) |
| Objective | Forecasting & Predictive Modeling: the ultimate indemnity the 2027 teams will save, booked at run rate in the AY2027 pick before the year opens, forecast from the pilot and the book, with each unit's 2027 intakes forecast for the calls and the fill limit |
| Shape | 05 (allocation to a fixed total): seventeen teams across eight units, each unit's teams and the indemnity they save there in a year, the credit, the note's opening and chart, and the asks |
| Decision | `allocation_to_total`, answer unit `count` (teams per unit), with each unit's saving and the credit in dollars |
| Mechanism | gap population (decisive: the register's two arms were both called, the counterfactual unit is not, and the uncalled intakes are outside the register), then objective (the call reaches every intake of a unit once one team works there, so a unit's first team is worth its whole intake stream and later teams only their places); pattern none, generators G1 (the unit of value: the call per intake reported, the file per place-day), G12 (a blank pilot reference on an intake is the record that it was never called, not an absence of evidence), G9 (architecture 1's per-claim reading, now a lower rung); Gate G `decomposition_attribution` (the programme's saving split between the call and the file, which scale on different units and decide the placement between them); strategy `causal_design` (the comparison the 2027 counterfactual needs) |
| Layer 2 family / pattern | `estimand_identification` (the right counterfactual: the randomised control arm received a component of the programme the counterfactual lacks); `own:randomised-contrast-nets-out-a-shared-opening-call` (Actuarial Science has no library card for it; the nearest is collections-loss-mitigation-strategy 1, compare by assignment, which is this build's rung 1) |
| Furniture | forum `trustees_or_governors` (the board of trustees approves the placement with the 2027 contributions), forcing event `vote_or_meeting` (the trustees' meeting of 19 November 2026), organisation family `cooperative_or_member_body` (a group self-insurance trust its member employers own), role family `programme_officer` (the trust's Early Return Nursing programme manager places the teams and supplies the credit to the pick), context artifact `register` (the pilot's assignment register), calibration `gold_standard_subsample` (the review's verified ultimates on stratified samples), opening `question-first`, question form `where` |
| Spine | `claims_extract_2021-01_to_2026-09.csv`, the claims system's listing: one row per claim reported January 2021 to September 2026 whose first report recorded time lost or that has paid or reserved indemnity; constructed |
| Deliverables | `ern_placement_ay2027.xlsx` (the placement, each unit's saving, the credit, the asks), `ern_placement_note_ay2027.pdf` (one page opening with the placement and charting each unit's saving with its teams) |
| People | drawn with `guard.py names --geo "United States" --seed 139`: Stephanie Gay (the trust's Early Return Nursing programme manager, the requester, in no file as the author of a figure), Samantha Hernandez (consulting actuary, Kellerman Pryce Actuarial: the review and the AY2027 pick memo), Kaitlyn Payne (ERN clinical lead, the case log), Alicia Oneal (claims operations, the triage screen and the register), Margaret York (data engineering, the upgrade and the extract), Kimberly Williams (chair of the trustees, signs the charter); none in the prompt |

**Guard.** `guard.py check` on the draft, then on the registered card: PASS with WARNs. Redrawn against the three live
builds before this one (task137 v4, task166 v3, task304): the organisation family off `financial_institution` (task304;
once the carrier is redrawn as a member-owned trust the honest label is `cooperative_or_member_body`, not a relabel of the
same carrier), the role family off `capacity_planner` (task137), the context artifact off `close_out_summary` (task137),
the forcing event off `launch_or_rollout` (task304), the decisive generator off G5 (task137) and G3 (task304), both of
which would also have described the mechanism; G1 is honest, since the step that finishes the golden is valuing the
first team on the unit's intakes and later teams on their places. The forum moved to the trustees because in a trust
the trustees decide. WARNs, answered: `people.first` on Stephanie (task133), Alicia (task87) and Margaret (task258), the
seed's list having no collision-free name left for those roles; `repeat.deliverables` (xlsx and pdf, as task304), kept
because a placement workbook and a one-page note are what a programme manager takes to trustees. After registration,
task141 v2 (registered ten minutes before this card) put `finance_controller` in the window, so the role was redrawn to
`programme_officer` and `check` re-run on the registered card: WARN only, the same four lines. The programme manager who
runs Early Return Nursing is the honester requester for a placement of its own teams in any case.

**Strategy label.** `causal_design`: the decisive step is the comparison the 2027 counterfactual implies, which the
pilot's own control arm is not. Nothing is transported (the 2027 teams call and file the same population the pilot
drew, by the same routine) and no population is chosen (the estimand files every intake of the eight units at run
rate).

**Same-puzzle and same-driver tests.** Gap population, decisive G1, decision `allocation_to_total`, Gate G
`decomposition_attribution`: `guard.py check` returns no structural block in the last twelve or older. Architecture 1
(population, G9, `method_or_model_selection`) differs in its decisive pattern and its Gate G mechanism.

**Abstraction test.** Stripped of nouns, the driver is: a pilot that randomised a service only among units that had all
first received the programme's opening contact measures what the service adds to a contacted unit, while a group the
programme does not reach gets no contact at all; the programme's saving is the contacted units' own gain over the units
the pilot never drew, which every unit of a group receives once one team works there, plus the service's increment on
the units the capacity takes. The nearest drivers on `check` (task128 v3 at 0.09, a contact's effect read where a queue
outran a team, a natural experiment in capacity; task103 v3 at 0.07, one record of contact standing for further units;
task127 v1 at 0.06, a team's throughput before a period closes) share no latent structure with it: none has a randomised
contrast netting out a component both arms received. Against task177 v2 (an average effect over a cycle carried to one
point of it) nothing here is conditioned on a covariate or transported, each of the pilot's two draws being read as
randomised; against task131 v1 and task249 (spillover inside a parent unit) no unit's outcome moves another's.
`guard.py slots` on the mechanism's words and on the setting's (opening call, nurse, triage, undrawn, intakes, waiting)
returns this slot's own architecture 1 only.

**Data-native sentence.** Haverline's triage screen drew one in three intakes at random each working morning and a
pilot nurse called every drawn intake that day, the worker and the employer's contact, before the drawn intakes were
paired and one of each pair kept on a file at random, so both arms of the register were called and the randomised
contrast is what a file adds to a called intake; the two in three the screen did not draw went to their adjusters on
report, uncalled, and they sit in the claims extract with no pilot reference and in the claim audit's sample that the
funding study verifies for its own ultimates.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: transports of a randomised test's
average (task177 v2), an upgraded level's gain on the untreated part (task165), marginal entrants (task163), a
protection's exposure overlap (task170 v3) and a capacity-overflow natural experiment (task128): none reads a control arm
as treated by a component the counterfactual lacks. `layer2-rigor-patterns.md`: collections-loss-mitigation-strategy 1
(compare by assignment) is architecture 1's reflex and this build's rung 1; frequency-severity 1 (frequency per unit of
exposure) is the per-intake frame. `measured-drivers.md`: held tasks put the decisive move upstream of every graded
figure and on a dimension in another file; the uncalled intakes are in the extract and the audit sample, not the
register, and all eight team counts, all eight savings and the credit move with the call. The portal result on
architecture 1: both responses read the register's two arms per intake, which is this build's default path.

**World.** Haverline Workers' Compensation Trust is a group self-insurance trust of Missouri employers in healthcare and
social assistance, retail and warehousing, manufacturing, construction, transportation and other industries, owned by
its member employers and administering its own claims from St. Louis and Kansas City; its claims are worked in claim
units by segment, an industry group crossed with an injury class (strains and sprains, other injuries). An intake is a
claim whose first report of injury records time lost from work. Missouri pays temporary total disability at two-thirds
of the average weekly wage up to the state maximum, nothing for the first three days unless the disability passes
fourteen days, temporary partial disability on reduced earnings, and permanent partial disability on a rating; an intake
whose worker is back inside the waiting period pays no indemnity.

Early Return Nursing (ERN) has two parts. The opening call: on the working day after the report a nurse calls the
worker and the employer's contact, assesses the time off to expect and asks the employer what suitable duties it can
offer. The file: the nurse keeps the intake, coordinates its care, arranges suitable duties and holds the file until the
worker is back at full duty. The pilot ran on triage dates 1 March 2023 to 28 February 2025: each working morning the
triage screen drew one in three intakes in the eight units at random, a pilot nurse made the opening call to every drawn
intake, and the drawn intakes were paired in triage order and one of each pair kept on a file at random, the other
passed to its adjuster (usual handling); the intakes the screen did not draw went to their adjusters on report.
Kellerman Pryce Actuarial reviewed the claims in 2026 at a 30 June valuation: for the pilot, 100 indemnity claims at
random from each unit and group; for the funding study's claim audit, 100 indemnity claims at random from each unit's
claims reported over the same two years outside the pilot; each verified blind to its group and the open ones projected
to ultimate. Its report says what it verified and how; it estimates no effect.

For 2027 the trustees funded seventeen teams of twenty places (the charter, signed 19 October 2026 by the chair): a unit
houses at most three teams and takes no more than its 2027 intakes keep in use over the year; a team's nurses make the
opening call to every intake their unit reports and take it into a place if one is free, an intake reported while every
place is taken going to its adjuster after the call; a unit with no team goes on as today, its intakes to their
adjusters on report; a file holds its place from the day it is taken to the day it closes, both counted, and again on a
reopening. The pick memo (Kellerman Pryce, 28 October 2026) books the credit as the AY2027 ultimate indemnity the eight
units' 2027 intakes will not pay because of the placement: what they would pay with no Early Return Nursing in 2027,
every intake going to its adjuster on report as today, less what they pay with the placement; at run rate (every place
in use every day of 2027, each unit's 2027 intakes at its intakes reported in the twelve months to September 2026); at
the review's verified ultimates with no trend; each unit at its own experience; indemnity only. The request is made on
Monday 9 November 2026 by the trust's ERN programme manager, for the trustees' meeting of 19 November.

**On paper, before any data.** This world's own courses (`generator/world.py`), 200,000 intakes a unit under each
handling, the call keeping most of what architecture 1's nurses kept at work and the file the rest with its shorter
disabilities and permanent awards (prototype `proto_call.py`):

| Unit | per intake, no call | the call | call and file | call's saving | file's saving | place-days | call over a year's intakes | a team's files a year |
|---|---|---|---|---|---|---|---|---|
| HC-SS | 2,857 | 2,317 | 1,972 | 540 | 345 | 24.2 | 891,000 | 104,000 |
| HC-OT | 6,387 | 6,277 | 5,217 | 110 | 1,059 | 43.0 | 97,000 | 180,000 |
| RW-SS | 2,297 | 1,811 | 1,535 | 486 | 276 | 21.0 | 482,000 | 96,000 |
| RW-OT | 6,776 | 6,661 | 5,751 | 114 | 910 | 51.1 | 94,000 | 130,000 |
| MF-SS | 3,497 | 2,980 | 2,580 | 516 | 401 | 25.3 | 738,000 | 116,000 |
| MF-OT | 8,211 | 8,070 | 6,828 | 141 | 1,242 | 45.4 | 116,000 | 199,000 |
| CN-SS | 4,939 | 4,570 | 4,203 | 369 | 367 | 30.2 | 443,000 | 89,000 |
| CN-OT | 13,269 | 13,167 | 11,471 | 101 | 1,697 | 61.7 | 72,000 | 201,000 |

Per indemnity claim the call is invisible (healthcare strains 3,357 dollars with no call against 3,429 with it, the
costlier remainder again), so the call's saving is a frequency effect read per intake. The placements every route
files (teams for HC-SS, HC-OT, RW-SS, RW-OT, MF-SS, MF-OT, CN-SS, CN-OT):

| Route | Teams | Credit |
|---|---|---|
| per verified claim, the file's contrast (architecture 1's rung 0) | 0 3 0 3 3 3 2 3 | 2.54 million |
| per assigned intake, the file's contrast (architecture 1's golden route; this build's default path) | 2 3 0 3 3 3 0 3 | 2.69 million |
| the call per indemnity claim over every intake, with the files | 0 3 2 3 3 3 0 3 | 2.51 million |
| the undrawn intakes against the file arm per served intake (architecture 1's golden placement) | 3 3 2 0 3 3 0 3 | 4.02 million |
| the call over every intake, units ranked on their average team at the cap | 3 0 2 0 3 3 3 3 | 5.06 million |
| golden: the call over every intake of a unit with a team, the files per place-day, placed on each team's marginal saving | 1 3 1 3 2 3 1 3 | 5.58 million |

The golden's cut on paper is MF-SS's second team (115,600) against HC-SS's second (104,000), 1.11 times; the build
widens it past the 1.15 floor before a pack is cut (stage 2).

## Three rules

- **Task type:** actuarial-science-insurance, claims-frequency-severity (serves Forecasting): the AY2027 indemnity a
  nurse programme will save, forecast as pure premiums per intake (frequency times severity) under no call, the call and
  the call with a file, carried to 2027 at run rate with each unit's 2027 intakes forecast for the calls and the places.
- **Domain test:** the quantity that decides the call is each unit's indemnity per intake under the three handlings,
  each the share of intakes paying indemnity times the verified ultimate severity, the claims actuary's frequency and
  severity build; the call works through the employer's suitable duties inside Missouri's three-day waiting period, so in
  the strain units it moves frequency (intakes that never pay) and leaves severity per indemnity claim where it was.
- **Swap:** "where should seventeen care-transition teams work across eight hospital service lines in 2027, and how many
  readmission days will they save" has no waiting period inside which a contact turns a reported absence into a claim
  that pays nothing, no conversion of a report into an indemnity claim and no accident-year ultimate across temporary
  total, temporary partial and permanent partial benefits; the call's saving, a frequency effect invisible per claim,
  has nothing to be in, and the task stops reading the same.
- **Layer 1:** claim numbers written four ways (the register's legacy numbers, the extract's new numbers with the legacy
  number beside converted claims, the review's numbers with Kellerman Pryce's control digit, the nurses' typed
  variants), produced by the 2025 claims-system upgrade and the review's referencing; segment codes recoded at the
  upgrade, joined through a crosswalk; the review workbook's sheet per unit with header blocks, three benefit columns
  and three strata; the case log's reopened files on second rows and US dates; an extract mixing intakes with later
  indemnity conversions, whose converted rows carry the legacy time-off flag; on the ask paths the parallel run's double
  listings, the EDI resends merged into their claims, a payment register at line grain, voided checks and the bank's
  returned transfers; a superseded charter draft. Each is what these systems write and none is placed to be caught.
- **Layer 2:** `estimand_identification`, the right counterfactual: the pilot's randomised contrast is what a file adds
  to a called intake, the 2027 counterfactual has no call, and the call's own saving is read from the pilot's first
  random draw (the intakes the screen drew against those it did not), then credited on the unit it reaches.
- **Decisive step:** read a unit with no team against the intakes the screen never drew rather than against the
  usual-handling arm, because both arms of the register had the opening call; then credit the call to every intake of a
  unit with a team and the files to their places, and place the teams on each team's marginal saving.
- **Not semantics:** every field, code and definition read correctly (the groups, the intake definition, the claim
  type, the verified TTD, TPD and PPD, the charter's call, the memo's counterfactual) still leaves the easy route on the
  register's two arms: no sentence defines the usual-handling arm as the counterfactual or excludes it, the call reads as
  the assessment that sets the pairs, and its saving exists only as an estimate the reader builds from intakes no pilot
  file lists.
- **Not rule application:** no filed rule or procedure computes the call's saving or says which intakes estimate a unit
  with no team: the memo files the counterfactual and the basis, the charter the operation. Enumerated family for the
  counterfactual, on paper (200,000 intakes a unit): the usual-handling arm per intake files 2 3 0 3 3 3 0 3 at 2.69
  million; the undrawn intakes per indemnity claim file 0 3 2 3 3 3 0 3 at 2.51 million (the call per claim is minus 72
  dollars in HC-SS); the undrawn intakes against the file arm per served intake file 3 3 2 0 3 3 0 3 at 4.02 million;
  the undrawn intakes per intake with the call over every intake file 1 3 1 3 2 3 1 3 at 5.58 million, a spread of 3.07
  million and four placements. The standing family (the undrawn intakes per intake, counted by report or by triage date,
  the audit's sample cut to intakes or not) is measured on the pack at stage 2 and must file one placement and one
  credit bin. What rules the usual-handling arm out is quiet: three sentences in three files (the pilot's protocol, the
  charter's call, the memo's counterfactual) and a gap of 17 points in the share of strain intakes paying indemnity that
  shows only once the undrawn intakes are counted.
- **Analyst test:** a strong analyst who reads the register, the review, the charter and the memo correctly reads the
  pilot per assigned intake, each arm's indemnity-claim rate times its verified severity, values each unit's teams at
  that saving over an ERN intake's place-days and files two teams in HC-SS, three in MF-SS, none in RW-SS or CN-SS and
  three in each other-injury unit with a credit of about 2,700,000 dollars (Ends on); on the generator's clean truth the same
  route files the same placement, and only the undrawn comparison with the call over every intake files the golden
  (asserted in `checks.py`).
- **Estimand:** the pick memo (`ay2027_indemnity_pick_ern_credit.pdf`): the credit is the AY2027 ultimate indemnity the
  eight units' 2027 intakes will not pay because of the placement, what they would pay with no Early Return Nursing in
  2027 (every intake to its adjuster on report, as today) less what they pay with the placement; at run rate (every
  place every day, each unit's 2027 intakes at its intakes reported October 2025 to September 2026); at the review's
  verified ultimates, no trend; each unit at its own experience; indemnity only. The charter files the teams, places,
  the three-a-unit limit, the fill rule, the call and the place-day. Population, outcome, window, unit and comparison
  are filed; which intakes estimate the comparison is not.
- **No decoy:** no memo, briefing, prior placement, scorecard or stakeholder figure states or argues a saving, an
  effect or a placement; the review states what it verified and estimates nothing; the usual-handling label is the
  pilot's own name for an arm handled by its adjuster after the call, not a planted misdirection; the charter draft, the
  worker survey and the staffing plan are declared distractors that rank nothing.
- **No certified replay:** no published saving, past placement, programme evaluation or certified figure ships, so the
  comparison cannot be recovered by matching certified numbers; the review's results are its verified amounts, which
  every route uses alike.
- **Lesson:** a randomised pilot whose arms both received an active component measures only the increment over that
  component; where the decision's counterfactual lacks the component, its value is read from the pilot's own earlier
  random draw and credited on what it reaches (every intake of a unit with a team), not on the capacity. No build on
  file reads a randomised control arm as treated by a component the counterfactual lacks (task131 v1 and task249 read
  spillover inside a parent unit, task177 v2 an average carried to one point of a cycle, task139 v1 the costlier
  remainder of the verified class).

## Default path

1. Read the charter (seventeen teams of twenty places, at most three a unit, the fill rule over the year, a place-day
   counted with its first and last days) and the pick memo (run rate, 7,300 place-days a team, the review's verified
   ultimates, each unit at its own experience).
2. Join the register's pilot intakes to the claims extract through the legacy claim number (normalised) for each
   intake's claim type, and to the crosswalk for its 2025 unit; in each unit, each arm's share of its assigned intakes
   that paid indemnity.
3. From the review's pilot strata (the control digit stripped, joined to the register for the arm), each arm's mean
   verified ultimate TTD plus TPD plus PPD; each arm's indemnity per assigned intake is its share times its severity, as
   the pilot was randomised, and the saving per intake is usual handling's less ERN's.
4. From the case log, the place-days an ERN intake held (both days counted, a reopening added); a team's year is 7,300
   place-days over that.
5. Each unit's saving per team-year is step 3 times step 4; its fill limit is its intakes over the twelve months to
   September 2026 times the place-days per ERN intake over 7,300, at most three.
6. Rank the units on saving per team-year and fill each to its limit in turn until seventeen teams are placed; the
   credit is each team's saving per team-year, summed.

Ends on: two teams to healthcare strains and sprains, three each to manufacturing strains and sprains and the four
other-injury units, none to retail and warehousing or construction strains and sprains; a credit of about 2,700,000
dollars (2,686,000 on paper).
Golden: one team each to healthcare, retail and warehousing and construction strains and sprains, two to manufacturing
strains and sprains, three to each other-injury unit; a credit of about 5,600,000 dollars (5,582,000 on paper).

## Stump sentence

A competent solver reads the pilot per assigned intake, values each unit's teams at usual handling's indemnity per
intake less ERN's over the place-days an ERN intake held, and files two teams in healthcare strains, three in
manufacturing strains, none in retail or construction strains and three in each other-injury unit with a credit of about
2,700,000 dollars (Ends on); the step that lands it there is taking the usual-handling arm as a unit with no team, when
every drawn intake had the opening call before its pair was split and a unit with no team has no calls: read against the
intakes the screen never drew, the call keeps about a fifth of the strain intakes from ever paying indemnity and reaches
every intake of a unit once one team works there, so each strain unit takes a team for its calls, manufacturing strains
a second for its files, the other-injury units three each, and the credit is about 5,600,000 dollars.

## Architecture 1 record (spent 2026-10-26)

Haverline Casualty Company, a stock carrier writing Missouri employers; drawn 2026-10-12, shipped 2026-10-15 (commit
1384f0e9, `target.zip` sha256 da3c19bf42dff8ef; checks.py 343 assertions, verify.py, byte-identical rebuilds,
figures_check 67, precut 49 with 0 FAIL, voice-check PASS, leak.py REVIEW answered, guard heart PASS, surface exit 0).
Stage 4: the leak reader found no leak (Q6 analytical); the judge returned NOT_DETERMINISTIC on supplementary 3 only,
FIX_NOW applied (the intake filed as a WHAT in the dictionary, Ask 1's silent device redrawn as EDI resends merged into
their claims), and the re-judge DETERMINISTIC and APPROVE, stump power moderate (`determinism_check_report.md`,
`determinism_check_report_pass2.md`).

**The design.** The pilot's nurses kept a fifth to a quarter of the strain intakes from ever paying indemnity, and the
review verified 100 indemnity claims a unit and group, so ERN's verified claims were the costlier remainder. The default
path compared the two groups' mean verified claim and valued a team per place-day of an indemnity claim; the decisive
step read the pilot per assigned intake (each group's share paying indemnity times its own verified severity) over an
ERN intake's place-days. The ladder: per verified claim 0 3 0 3 2 3 3 3 at 2,048,524 (booked 2,000,000); the per-claim
family 2.0 to 2.2 million; per assigned intake without the place-day 3,793,208, with an indemnity claim's place-days
3,398,667, without the fill check 4,200,799; the golden 3 3 2 0 3 3 0 3 at 4,105,562 (booked 4,100,000), RW-SS held to
the two teams its 944 intakes keep in use (teams listed HC-SS, HC-OT, RW-SS, RW-OT, MF-SS, MF-OT, CN-SS, CN-OT).

**Portal result, 2026-10-26.** Both responses placed three teams each in HC-SS, MF-SS, MF-OT, CN-OT and HC-OT, two in
RW-SS and none in RW-OT or CN-SS, and booked the 4.1 million dollar credit, with the workbook and the note: the golden
exactly.

**Why it was reachable, and it is not a near miss.** Reading a randomised pilot per assigned intake is the textbook
reading, analyse as randomised, which this note quoted as the client's pin, so readability test 3 fired on the decisive
rung where the screen had recorded it silent; the default path it overturned conditions on a status the treatment
moves, which a strong analyst refuses by reflex. And the whole ladder sat inside the register's two arms: once a reader
read the arms per intake, nothing in the pack was left to find.

**The constraint it leaves.** Inside the two arms the per-intake contrast is unbiased and the design forces it, so any
further step there is a stratification of it (the triage tier, the office), the opponent's first group-by, or a
transport of its average onto the intakes the 2027 teams reach, which is task177 v2's driver and needs that population
filed. Architecture 2 finds what the two arms share that the counterfactual lacks: the opening call.

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
- A twelve-month pilot drawing one in three intakes with 40 to 50 verified claims a stratum (2026-10-15): a segment's
  realised saving per team-year had a standard deviation of 120,000 to 300,000 dollars across draws against values of
  120,000 to 330,000, so the segment ranking was noise; the pilot runs 24 months and the review verifies 100 a stratum.
- The review as a census of every pilot indemnity claim (2026-10-15): it would cut the noise further, but the join of the
  review to the register would then show 451 usual-handling claims against 338 ERN claims in healthcare strains, the
  frequency effect on the surface of the file the default path reads; the review samples a fixed 100 a stratum.
- A check run sent twice with its cancellation only in a treasury register (Ask 2's first device, 2026-10-15): the
  register would have been a single-purpose file announcing the device, and a duplicate run whose checks are voided after
  the pull leaves "paid" indeterminate; replaced by the line grain and the bank's returns.
- The draft charter's "units with the most intakes would be considered first" (stage 3, 2026-10-15): a staff draft
  stating a placement basis reads as a decoy draft (R3c); the draft now leaves the basis to be settled with Pricing.
- Ask 1's two devices left silent (stage 4, 2026-10-15): the judge's literal reader took `time_off_at_report` as the
  dictionary then defined it and counted both listings of a parallel-run claim, so the golden held only under the
  author's reading (NOT_DETERMINISTIC, FIX_NOW); a silent label switch and an unkeyed double listing cannot be both
  silent and forced, so both are filed and the ask's silence is gone.
- Ask 1 regenerated to the flag as filed (stage 4, 2026-10-15): it would count later indemnity conversions and the
  parallel run's second listings as intakes against charter 4.1, mark the careful count wrong and leave the ask with no
  device; the organisation's definition is filed instead.
- The parallel-run note without its fields (stage 4, 2026-10-15): matched on office, segment, class, injury and report
  dates without `disability_began`, one converted claim listed once pairs a new-number claim; the note names all six.
- Memo paragraph 2's restated comparison (stage 4, 2026-10-15): "what those intakes would pay with their adjusters
  alone, less what they pay with a team" restated the credit as a subtraction over the intakes, which the judge read as
  the estimand stated nearly literally; the credit is stated once and the counterfactual left to charter 4.2.
- A second form for the review's control digit (stage 4 realism, 2026-10-15): the digit sits on the call's join of the
  review to the register, so a second form would be a main-path mess item; the references and remarks vary instead.
- The FIX_NOW pass's Ask 1 (stage 4, 2026-10-15): both devices filed for determinism and nothing silent left, the cracker
  landing all eight figures and a pair of 58.2; redrawn with the merge file.
- A state FROI filing log carrying the cancels of claims filed in error (Ask 1 redraw, 2026-10-15): a second source of
  reported lost-time claims in the state's voice, its originals counting later conversions as reports and a cancel for a
  wrong-carrier report not plainly outside "intakes"; the claims system's own merge file instead.
- A closed-outcome field on the extract (Ask 1 redraw, 2026-10-15): a value naming the device rows in the habitual file
  is a marker, and its denied or withdrawn outcomes in the call's window would move the fill count when mishandled.
- Legacy claims parked as unassigned (G9) and converted to GN-AL (Ask 1 redraw, 2026-10-15): the injury class cannot be
  recovered from the class code, so the true segment would be a guess.
- 2026-10-26, architecture 1's decisive step (the pilot read per assigned intake, each group's own indemnity-claim rate
  times its own verified severity, instead of per verified indemnity claim), after both portal responses landed the
  placement and the 4.1 million credit. Spent, not repairable: analysing a randomised pilot as randomised is the
  domain's own reflex, so readability test 3 fires on the decisive rung, and the whole ladder sat inside the register's
  two arms, so a reader who reads the arms per intake has nothing left to find. Every further step inside those arms is
  a stratification of the contrast or a transport of its average, both spent or filed. The re-root is recorded in
  `## Portal result and the stage 2 diagnosis`.
- 2026-10-26, at the architecture 2 draw: the triage tier as the decisive step (2027 teams take intakes highest
  predicted lost time first, so a unit's teams reach the top of its tier distribution, where the file saves least in the
  strain units and most in the other-injury units). Measured on paper (200,000 intakes a unit, five tiers): the golden
  4.28 million against the pilot average's placement at 4.16 million, both booking 4.3 million, so the credit did not
  separate; the stratification by tier is the opponent's first group-by, the teams' population has to be filed, and the
  driver is task177 v2's (a randomised average carried to the part of the population the deployment reaches).
- 2026-10-26, at the draw: employer spillover (a nurse's suitable-duty work at an employer also helping its
  usual-handling claimants), the randomised contrast understating the at-scale effect: the interference family of
  task131 v1 and task249, a parent unit's shared resource; dropped unmeasured.
- 2026-10-26, at the draw: the file's effect falling with the team's load (the pilot ran below the full load 2027
  teams will carry), a dose-response read from the pilot's daily open-file counts: a fitted curve with a free form,
  and a randomised average carried to one covariate value again; dropped.
- 2026-10-26, at the draw: the pilot's claims developed to ultimate arm by arm (a file closing claims sooner, so one
  set of book factors overstates ERN's ultimates): the chain-ladder variants a reader would defend fork the graded
  figures (stumping 1.6a's task194 death), and the review already projects the open claims; dropped.
- 2026-10-26, at the draw: segment savings blended by credibility before placing: shrinkage is the opponent's reflex,
  and the credibility standard would have to be filed, which is the method; dropped.
- 2026-10-27, architecture 2 spent at stage 2 before any pack was cut (the opening call both pilot arms received): the decisive
  step rests on one sentence of the pilot protocol, which a careful reader meets first, and the world is the one the portal
  already solved; re-rooted at the author's instruction for a fully fresh architecture.
