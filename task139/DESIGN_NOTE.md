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

Resumed on 2026-10-15 at stage 2 (the first build agent stopped after the draw on a usage limit). `guard.py check` re-run
after `git pull`: one BLOCK, `test.same_driver_older` against task452 v2 (population, G9, method_or_model_selection),
cleared by a differentiation line on the card (a stratified sample's design weights after a reclassification, against a
treatment that moves assigned units out of the recorded class); one WARN, `people.first` (Margaret, task258), answered by
redrawing the requester as Julie Winters from the same `guard.py names` list; Gregory Friedman added for the charter's
signature. No axis is banned against the builds filed before this one; the card is edited in place (no new filing stamp;
the draw dates from 2026-10-12). `guard.py check`: PASS.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task139.json`, architecture v1, registered 2026-10-12; re-checked 2026-10-15, PASS (above); `guard.py validate` clean |
| Domain / task type | actuarial-science-insurance / claims-frequency-severity (a client domain, never drawn before): the saving is a workers' compensation pure premium, indemnity per intake as the indemnity-claim rate times the indemnity severity at ultimate, the frequency-severity build of the claims actuary |
| Objective | Forecasting & Predictive Modeling: the ultimate indemnity the 2027 teams will save, booked at run rate in the AY2027 indemnity pick before the year opens, forecast from the randomised pilot, with each unit's 2027 intakes forecast to see how many teams it keeps in use |
| Shape | 05 (allocation to a fixed total): seventeen teams across eight segments, each segment's teams and its saving per team-year, the credit, the note's opening and chart, and two per-segment asks on rows the call never reads |
| Decision | `allocation_to_total`, answer unit `count` (teams per segment) with the credit in dollars to the nearest 100,000 |
| Mechanism | gap population (decisive: the review's file holds indemnity claims, the decision buys intakes, and which intakes become indemnity claims is the nurses' own effect), then objective (the twenty places are the scarce resource, so a team is valued per place-day, and a unit takes no more teams than its intakes keep in use); pattern none, generators G9 (downstream survival against upstream acquisition), G1 (unit of value: the place-day) and G14 (each segment's own yield); Gate G `method_or_model_selection` (two comparisons of one pilot, per verified indemnity claim and per assigned intake, the randomised design pinning the second); strategy `causal_design` |
| Layer 2 family / pattern | `estimand_identification` (selection on an outcome the treatment moves: comparing the arms on their indemnity claims conditions on a status the nurses changed); `own:indemnity-saving-read-per-assigned-intake` (Actuarial Science has no library patterns; the nearest lines are biomedical-clinical-research/clinical-trial-design-analysis/1, analyse as randomised, and healthcare-delivery-health-economics/payment-claims-health-plan-analytics/4, a ratio of totals over the exposure that bears it) |
| Furniture | forum `executive_team`, forcing event `launch_or_rollout` (teams live Monday 4 January 2027), organisation family `financial_institution` (a stock carrier), role family `capacity_planner`, context artifact `close_out_summary` (the independent review), calibration `gold_standard_subsample` (the review's verified ultimates on a stratified sample of the pilot's indemnity claims), opening `question-first`, question form `where` |
| Spine | `claims_extract_2021-01_to_2026-09.csv`, the claims system's listing: one row per claim reported January 2021 to September 2026 whose first report recorded time lost or that has paid or reserved indemnity (59,789 rows); constructed |
| Deliverables | `ern_placement_ay2027.xlsx` (placement, the pilot basis, the two asks, notes), `ern_placement_note_ay2027.pdf` (one page opening with the placement and charting each segment's saving per team-year with its teams) |
| People | drawn with `guard.py names --geo "United States" --seed 139`: Julie Winters (director of medical case management, the requester), Joanna Sullivan (consulting actuary, Kellerman Pryce Actuarial, signs the review), Kathleen Reilly (chief pricing actuary, the pick memo), Joel Kelly (ERN clinical lead, the case log), Kristen Hansen (claims operations, the triage screen and the register), Juan Castillo (data engineering, the upgrade, the extract), Gregory Friedman (president and CEO, signs the charter); none in the prompt |

**Guard.** At the draw, PASS after two redraws against task136, task137 and task138: strategy off
`population_selection`, `composition_mix` and `time_semantics`; decisive mechanism off G8, E and G16; shape off `other`
and 02; forum, forcing event, organisation family, role and context artifact each off the three. The question form
moved from `how-many` (task137) to `where`.

**Strategy label.** `causal_design`, not `population_selection`: the 2027 teams take exactly the population the pilot
randomised (intakes at the daily triage), so nothing is transported; the error is the comparison, the two arms read on a
status the treatment changed. The card says so in `notes`.

**Same-puzzle and same-driver tests.** Gap population, decisive G9, decision `allocation_to_total`, Gate G
`method_or_model_selection`: no build in the last twelve carries the structural keys together; task452 v2 (an ETL build
filed after this draw) shares gap, pattern and Gate G and is differentiated on the card.

**Abstraction test.** Stripped of nouns, the driver is: an intervention assigned at random at intake changes how many of
its units go on to become the recorded costly cases as well as what those cases cost, so its effect is read per assigned
unit, each arm's own conversion times its own cost, and valued per unit of the capacity each assigned unit holds; read
per recorded case, it compares the costlier remainder of one arm with the ordinary cases of the other. The nearest
drivers (`guard.py nearest`: task73 world ten 0.07, task121 v1 lineage 0.06, task131 v1 lineage 0.05) share no latent
structure, default path or correction with it.

**Data-native sentence.** Haverline's pilot assigned each intake at the daily triage, before anyone could know whether
the worker would lose more than the three-day waiting period, and an Early Return nurse's first call went to the
employer about suitable duties, so in the healthcare, retail and manufacturing strain segments the nurses kept about a
fifth to a quarter of their intakes from ever paying a day of indemnity (64.9 against 86.6 per cent paid in healthcare
strains); Kellerman Pryce drew its verification sample, 100 claims a segment
and group, from the claims that paid indemnity, so its two samples set the nurses' costlier remainder against an
ordinary usual-handling group, and nothing in either file says so.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting`: hazards by time since entry (134),
selection on the outcome by examination (124), a campaign's yield per untapped member (136), a retention share
conditioned on a repricing gap (137), the state at the forecast date (138), a capacity-overflow natural experiment (128),
conditional survival (133): none reads a randomised pilot per assigned unit because the treatment moves units out of the
recorded class. `two-layer-task-design.md`: the client's own pin, "a randomised design means an intention-to-treat
difference on the randomised unit", is this build's forcing organ (the design forces the method, `forcing-the-answer`
Part 5.1). `measured-drivers.md`: under 0.25 the miss is the unit or population a row stands for; here the review's row
is an indemnity claim and the decision's unit an intake. The seed's header and Situation (FC10) for the world only.

**World.** Haverline Casualty Company is a stock workers' compensation carrier writing Missouri employers from St. Louis
and Kansas City; its claims are worked in claim units by segment, an industry group crossed with an injury class
(healthcare and social assistance, retail and warehousing, manufacturing, construction; strains and sprains, other
injuries). An intake is a claim whose first report of injury records time lost from work. Missouri pays temporary total
disability at two-thirds of the average weekly wage up to the state maximum, nothing for the first three days unless the
disability passes fourteen days, temporary partial disability on reduced earnings, and permanent partial disability on a
rating; an intake whose worker is back inside the waiting period pays no indemnity.

Early Return Nursing (ERN) puts a nurse case manager on an intake from triage: calls within a working day, care
coordinated, suitable duties arranged where the employer can offer them, the file held until the worker is back at full
duty. The pilot ran on triage dates 1 March 2023 to 28 February 2025: each working morning the triage screen drew one in
three intakes in the eight segments into the pilot and assigned each segment's drawn intakes in pairs in triage order,
one of each pair to ERN at random: 5,227 pilot intakes, 2,613 to ERN, every one taken by a pilot team. Kellerman Pryce
Actuarial verified the pilot in 2026: from the 4,339 pilot claims with paid or reserved indemnity at 30 June 2026 it drew
100 at random from each segment and group (1,600 claims), verified each blind to its group and projected the open ones
to ultimate. Its report says what it verified and how; it does not estimate the programme's effect.

For 2027 the executive committee funded seventeen teams of twenty places (the charter, signed 19 October 2026): a unit
houses at most three teams and takes no more than its 2027 intakes keep in use over the year; teams take intakes at the
daily triage while a place is free; a file holds its place from the day it is taken to the day it closes, both counted,
and again on a reopening. The pick memo (chief pricing actuary, 28 October 2026) books the credit as the ultimate
indemnity the AY2027 intakes the teams take will not pay because the teams took them, at run rate (every place in use
every day of 2027), at the review's verified ultimates with no trend, each segment's teams at what the pilot measured in
that segment, indemnity only. The request is made on Monday 9 November 2026 (the pack's export stamp).

## Default path

1. Read the charter (seventeen teams of twenty places, at most three a unit, intakes taken at triage, a place-day counted
   with its first and last days, a unit given no more teams than its intakes keep in use) and the pick memo (run rate,
   7,300 place-days a team, the review's verified ultimates, each segment on its own pilot measure).
2. Read the review's workbook (one sheet per segment, verified ultimate TTD, TPD and PPD per sampled claim, summed), join
   each sampled claim to the register for its group through the claim number (the control digit stripped) and its
   segment through the 2025 crosswalk.
3. In each segment, the saving per managed claim is usual handling's mean verified ultimate less ERN's: 3.7 per cent in
   healthcare strains, 4.2 in retail strains, 5.8 in manufacturing strains and 4.5 in construction strains, 9.8 to 13.1
   per cent in the other-injury segments.
4. From the case log, the place-days an ERN indemnity claim held (file open to file close, both days, a reopening
   added); each segment's saving per team-year is 7,300 times step 3 over step 4.
5. Rank the segments on saving per team-year; three teams to each in turn, the unit's intakes over the twelve months to
   30 September 2026 keeping its places in use (they do, at an indemnity claim's place-days, in every unit); the credit
   is each team's saving per team-year, summed.

Ends on: three teams each to construction other injuries, manufacturing other injuries, healthcare other injuries,
retail and warehousing other injuries and construction strains and sprains, two to manufacturing strains and sprains,
none to healthcare or retail and warehousing strains and sprains; a credit of 2,000,000 dollars (2,048,524 unrounded).
Golden: three teams each to healthcare strains and sprains, manufacturing strains and sprains, manufacturing other
injuries, construction other injuries and healthcare other injuries, two to retail and warehousing strains and sprains;
a credit of 4,100,000 dollars (4,105,562 unrounded).

## Stump sentence

A competent solver joins Kellerman Pryce's verified ultimates to the pilot register, takes usual handling's mean
indemnity claim less ERN's in each segment, values each segment's teams at that saving over the place-days an ERN
indemnity claim held, and files teams weighted to the other-injury and construction segments with none in healthcare or
retail strains and a credit of 2,000,000 dollars (Ends on); the step that lands it there is reading the saving per
verified indemnity claim when the nurses kept a fifth to a quarter of the strain intakes from ever paying indemnity, so
ERN's indemnity claims there are the costlier remainder and the saving reads as four to six per cent: read per assigned
intake, as the pilot was randomised, each group's own indemnity-claim rate times its own verified severity over the
place-days an ERN intake held, the teams go to the strain segments, retail strains takes the two teams its intakes keep
in use, and the credit is 4,100,000 dollars.

## Three rules

- **Task type:** actuarial-science-insurance, claims-frequency-severity (serves Forecasting): the AY2027 indemnity a
  nurse programme will save, forecast from a randomised pilot as a pure premium per intake, frequency times severity,
  each arm's own, carried to 2027 at run rate with each unit's 2027 intakes forecast to see the teams it keeps in use.
- **Domain test:** the deciding quantity is a workers' compensation pure premium per intake (the share of intakes that
  pay indemnity, which the three-day waiting period and a return on suitable duties decide, times the verified ultimate
  indemnity severity) compared between the arms of a randomised pilot and valued per nurse place-day; the claims
  actuary's frequency-severity build decides, not a sort or a stated score.
- **Swap:** "place seventeen readmission coaching teams across eight wards from a randomised pilot verified on readmitted
  patients" keeps a pilot and a costly class, but an intake that pays nothing because the worker was back on suitable
  duties inside a three-day waiting period, a severity that is ultimate indemnity across temporary total, temporary
  partial and permanent partial benefits, and a file held to full duty have no meaning outside workers' compensation, so
  the mechanism that moves intakes out of the verified class, and with it the call, stops making sense.
- **Layer 1:** claim numbers written four ways (the register's legacy numbers, the extract's new numbers with the legacy
  number beside converted claims, the review's legacy numbers with Kellerman Pryce's control digit, the nurses' typed
  variants), segment codes recoded at the 2 June 2025 upgrade (the register in legacy codes, the extract and the review in
  2025 codes, a crosswalk between), a review workbook of eight sheets with header blocks, three benefit columns and sheet
  totals, a case log with reopenings on second rows and US dates, a claims extract mixing intakes with later indemnity
  conversions, and a superseded charter draft beside the signed one; on the ask paths, converted rows whose
  `time_off_at_report` carries the legacy lost-time indicator, claims keyed in both systems during the parallel run, a
  payment register that repeats a payment's amount on each weekly line, voided checks and the bank's ACH returns. Each is
  what these systems write; none decides the call (the call is unchanged with every ask file removed, and with the
  reopenings dropped, asserted).
- **Layer 2:** `estimand_identification`: the shortcut reads the pilot on the claims its gold-standard file holds; the
  expert reads a randomised pilot per assigned unit, frequency and severity together, because the treatment moves units
  between the classes the records keep, and values a capacity-bound team per unit of the capacity an assigned unit holds.
- **Decisive step:** read the pilot per assigned intake, as it was randomised: each group's indemnity per intake is its
  own share of intakes that paid indemnity times its own mean verified ultimate, and a team's year is 7,300 place-days
  over the place-days an ERN intake held (the short files of the intakes kept at work included), instead of the saving
  per verified indemnity claim over an indemnity claim's place-days; this moves healthcare strains from 34,106 to
  292,364 dollars a team-year and the credit from 2,000,000 to 4,100,000.
- **Not semantics:** every field, code, unit and definition can be read correctly, and the default path reads them all
  correctly (the groups, the verified TTD, TPD and PPD, the claim types, the place-day with both days counted, the
  crosswalk) and still files 2,000,000; nothing flips on what a field means, only on which comparison of a randomised
  pilot estimates the saving on the intakes the teams take.
- **Not rule application:** no filed sentence says to compare per intake, to multiply a group's indemnity-claim rate by
  its severity, that the nurses changed which intakes paid indemnity, or that the review's sample conditions on that;
  the pick memo files only what the credit is (the indemnity the teams' intakes will not pay because the teams took
  them) and the charter what a place-day is, and executing every filed rule leaves the estimator to the analyst, where
  the per-claim reflex files 2,000,000.
- **Analyst test:** a strong analyst who reads the protocol, the review, the charter and the memo correctly, joins the
  verified ultimates to their groups, takes usual handling's mean indemnity claim less ERN's in each segment and values
  each team per place-day of an indemnity claim files construction and other-injury teams and a credit of 2,000,000
  dollars (Ends on); on the generator's clean truth (every pilot intake's course under both groups, no sample) the same
  route files the same healthcare and retail strain units empty, and the per-intake route the golden allocation (R3a,
  R3b asserted).
- **Estimand:** the pick memo, paragraphs 2 to 5 (`ay2027_indemnity_pick_ern_credit.pdf`): the credit is the ultimate
  indemnity that the AY2027 intakes the teams take will not pay because the teams took them, what those intakes would pay
  with their adjusters alone less what they pay with a team, at run rate (every place every day, twenty places for 365
  days), at the verified ultimates (TTD, TPD and PPD, open and closed, no trend), each segment at its own pilot measure;
  the charter 2.1 to 5.3 files the teams, places, the three-a-unit limit, the fill rule over the year and the place-day.
  The population, outcome, window, unit and comparison are filed; the estimator of the comparison is not.
- **No decoy:** no memo, briefing, prior placement, scorecard or stakeholder figure states or argues a saving per claim,
  a per-segment saving or a placement; the review states what it verified and refuses an effect; the kept-at-work intakes
  are the nurses' own work, written in the claim types and the case log, not defects; the three distractors (the charter
  draft, the worker survey, the staffing plan) rank nothing.
- **No certified replay:** no published saving, past placement, programme evaluation or certified figure ships, so the
  comparison cannot be recovered by matching certified numbers; the review's only results are its verified amounts and
  their total, which every comparison uses alike.
- **Lesson:** a randomised intervention that changes which units become the recorded costly cases has to be valued per
  assigned unit, each arm's own conversion times its own severity, and a capacity-bound team per unit of the capacity an
  assigned unit holds; reading it on the recorded cases a gold-standard sample holds compares the treated arm's costlier
  remainder with the control's ordinary cases. No build on file reads a randomised pilot per assigned unit because the
  treatment moves units out of the verified class (task131 reads interference inside households; task124 a selection by
  examination carried to an unexamined population).

## Readability screen

Six tests per rung: 1 a filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a reflex
of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction, ratio or
half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 saving per verified claim over an indemnity claim's place-days (the default path) | the memo files amounts at the verified ultimates; the charter the place-day | the review's rows are verified indemnity claims | yes (compare the verified amounts of the two groups) | no | no | yes (one subtraction of two sample means) | readable |
| R1 the per-claim saving times ERN's indemnity-claim rate, over all of an ERN intake's place-days | the memo's credit is on the intakes the teams take | the register lists intakes | yes (scale the claim saving to intakes) | no | no | no | readable |
| R1b the per-claim saving over all of an ERN intake's place-days | charter 5.1 to 5.3 (every taken intake holds a place) | the case log lists every ERN file | yes | no | no | no | readable |
| R2 the per-intake saving ranked per intake, not per place-day | charter 2.2 (twenty places) | no | yes (a capacity-bound team is valued by throughput) | no | no | no | readable |
| R2b the per-intake saving over an indemnity claim's place-days | charter 5.1 (a file is held from the day it is taken) | no | no | no | no | no | readable |
| R3 the golden saving with no fill check | charter 3.3 | no | yes (check the places can be kept full) | no | no | no | readable |
| R4 (decisive) each group's own indemnity-claim rate times its own verified severity, per assigned intake, as randomised | no: the memo files what the credit is (the indemnity the teams' intakes will not pay because the teams took them) and the default path answers that sentence too, with the per-claim saving; no sentence names a rate, a frequency, a conversion, a kept-at-work intake or the review's sampling on the outcome | no: no column holds an intake's indemnity under either group; `claim_type` is every claim's current type in a 59,789-row listing the default path opens only for the units' volumes, and the review's sample is 100 per group in every segment, so its counts show no difference | no: the reflex on a verified gold-standard sample is to compare its amounts, and the per-claim saving reconciles (positive in every segment, four to thirteen per cent, a plausible nurse effect) | no: no saving, placement or evaluation ships | no | no: per segment, two group rates from a 5,227-intake register joined to a 59,789-row extract, times two sample means, over a place-day mean built from a log with reopenings | silent |

The decisive rung is silent because the question the pack raises (what does a team save on the intakes it takes) is the
one the default path believes it has answered: the per-claim saving is a real comparison of verified amounts, and
nothing in the review, the memo or the register points at the intakes that never reached the review's frame.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs, then the asks' rows. `checks.py`
asserts each. Ch is the charter; PM the pick memo; R the review report.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "where ... work" | teams per segment, each segment's claims in one unit | teams per office or per unit name | same call (Appendix A: one unit a segment) | Ch 3.1, Appendix A |
| SF2 | "seventeen teams" | all seventeen placed | fewer where a saving is low | same call (every segment's saving per team-year is positive, asserted) | Ch 2.1 |
| SF3 | at most three a unit | three | four (the draft's silence) | four would move the call | Ch 3.2; the draft is superseded (Ch heading) |
| SF4 | a unit's fill limit | the place-days its 2027 intakes would hold over the year fill every place: teams no more than intakes times place-days per ERN intake over 7,300 | a monthly or daily basis | RW-SS keeps 2 on every month (2.04 to 2.76, asserted); MF-OT's lowest month (2.80) would cap it at 2 | Ch 3.3 ("over the year") |
| SF5 | a unit's 2027 intakes | any forecast of the units' intakes: the latest twelve months, 2025, 2024, Jan to Sep 2026 annualised, a trend to 2027, the flag as filed | (a forecast that moves a cap) | converges: RW-SS 2.33 to 2.65 teams' worth, every other unit 3.97 or more (asserted on eight bases) | the records converge |
| SF6 | "ultimate indemnity" | TTD, TPD and PPD together, verified ultimate | TTD only | 2,900,000 and another allocation (asserted) | PM 4 |
| SF7 | "save" | what the intakes would pay with their adjusters alone less what they pay with a team | with medical, or net of the teams' cost | same estimand; medical out | PM 2, PM 6 |
| SF8 | the AY2027 window | run rate, 7,300 place-days a team | a fill-up transient from 4 January; accident-date shares | (none: the memo sets run rate) | PM 3 |
| SF9 | the amounts | verified at 30 June 2026, no trend | trended two years at 4 per cent | 4,400,000 (asserted) | PM 4 |
| SF10 | each segment's measure | the pilot's own in that segment | pooled or credibility-weighted across segments | (a pooled measure cannot place teams) | PM 5 |
| SF11 | a place-day | both the opening and the closing day counted | the day difference only | 4,300,000, five team savings a bin or two higher (asserted) | Ch 5.3 |
| SF12 | a reopening | holds a place again | the reopening rows dropped | converges: same allocation, 4,121,010, every team saving in its bin (asserted) | Ch 5.2; the records converge |
| SF13 | the pilot's groups | as assigned in the register | as treated | converges: every ERN intake has a file and no usual-handling intake has one (asserted) | the records converge |
| SF14 | an intake that paid indemnity | `claim_type` IND | a first indemnity date on file; the review's frame at 30 June 2026 | converges: the same 4,339 intakes (asserted) | the records converge |
| SF15 | a group's severity | the mean verified TTD + TPD + PPD of its 100 sampled claims | the sample weighted to the frame (the same within a stratum); closed claims only | weighting converges; closed only 4,200,000 (asserted) | PM 4 ("open and closed claims alike") |
| SF16 | a pilot intake's segment | the register's legacy code through the crosswalk | the extract's 2025 segment | converges (asserted for every pilot intake) | the records converge |
| SF17 | the estimate's grain | each segment as a whole | each office then pooled by intakes | converges: same allocation, 4,123,300 (asserted) | PM 5; the records converge |
| SF18 | the credit's rounding path | the unrounded team savings summed, rounded once | the rounded team savings summed | converges: 4,090,000 rounds to 4,100,000 (asserted) | the records converge |
| SF19 | ties at the cut | none: the last unit funded (HC-OT 191,656) stands 1.47 times the first left out (RW-OT 130,715) | (a tie-break) | n/a (asserted at 1.3) | the records converge |
| SF20 | what decides the call | an analytical choice: the memo and the charter file the WHAT, no sentence files how the saving per intake is estimated | executing the filed rules alone | (no credit: the rules leave the comparison open; the per-claim reflex files 2,000,000) | the estimand and the data: on the clean truth the two estimators of the same filed credit stand apart (R3a, R3b) |
| SF21 | Ask 1: an intake | a claim whose first report records time lost; for rows converted at the upgrade, time lost began on or before the report | `time_off_at_report` = Y as filed | every segment 24 to 80 high (asserted) | Ch 4.1; the dictionary's `time_off_at_report`; the data (no new-system row is inconsistent with its dates, and converted rows flag Y with time lost beginning after the report) |
| SF22 | Ask 1: the parallel-run copies | counted once | both copies | every segment 2 to 9 high (asserted) | the records converge: each copy shares office, segment, class and every date with a new-system claim |
| SF23 | Ask 1: "reported in 2025" | report date in 2025 | injury date in 2025 | five segments 2 to 9 off, three the same (asserted) | the prompt ("intakes reported in 2025") |
| SF24 | Ask 2: paid January to September 2026 | payments issued in the window, each once | each line summed | every segment 1.66 to 1.86 times (asserted) | the dictionary (a payment's lines are the weeks it covers; amount is the payment's amount); the records (a payment's lines all carry the same amount) |
| SF25 | Ask 2: returned EFTs | left out; the re-issued check counts | kept | every segment 10,300 to 50,186 dollars high (asserted) | the bank's return file |
| SF26 | Ask 2: voided checks | left out; the replacement counts | kept | every segment 3,814 to 15,519 dollars high (asserted) | the register's status |
| SF27 | Ask 2: a payment's segment | its claim's segment on the extract | (none) | n/a | the records converge (every payment's claim is on the extract, asserted) |

The stump is none of these rows: every term is read the same way by a careful reader, and the default path reads them
all as the golden does. SF20 is the reader's Q6 guard written down: the memo and the charter fix the population, outcome,
window, unit and comparison, and the per-intake estimator is forced by the design (the randomised unit is the intake),
not by a sentence.

## Ladder

Every rung is a complete pipeline on the same literal estimand, computed by `checks.py` from the pack (5,227 pilot
intakes, 1,600 verified claims, 2,613 ERN files); the golden and the default path again by `verify.py`.

| Rung | Saving | Place-days | Fill check | Teams (HC-SS HC-OT RW-SS RW-OT MF-SS MF-OT CN-SS CN-OT) | Credit (unrounded) | Booked |
|---|---|---|---|---|---|---|
| R0 (default) | per verified claim | an indemnity claim's | at an indemnity claim's | 0 3 0 3 2 3 3 3 | 2,048,524 | 2,000,000 |
| R0' | per verified claim | a sampled claim's | at a sampled claim's | 0 3 0 3 2 3 3 3 | 2,048,360 | 2,000,000 |
| R1 | per claim times ERN's rate | an ERN intake's | at an intake's | 0 3 0 3 2 3 3 3 | 1,985,501 | 2,000,000 |
| R1' | per claim times usual handling's rate | an ERN intake's | at an intake's | 0 3 0 3 3 3 2 3 | 2,081,829 | 2,100,000 |
| R1b | per verified claim | an ERN intake's | at an intake's | 0 3 0 3 3 3 2 3 | 2,248,360 | 2,200,000 |
| R2b | per assigned intake | an indemnity claim's | at an indemnity claim's | 3 2 3 0 3 3 0 3 | 3,398,667 | 3,400,000 |
| R2 | per assigned intake, ranked per intake | an ERN intake's | at an intake's | 3 3 0 2 3 3 0 3 | 3,793,208 | 3,800,000 |
| R3 | per assigned intake | an ERN intake's | none | 3 2 3 0 3 3 0 3 | 4,200,799 | 4,200,000 |
| R4 golden | per assigned intake | an ERN intake's | at an intake's | 3 3 2 0 3 3 0 3 | 4,105,562 | 4,100,000 |

- **Separation.** The per-claim family (R0 to R1b) files 2.0 to 2.2 million with healthcare and retail strains empty;
  the per-intake family without the place-day (R2) or with an indemnity claim's place-days (R2b) puts a team in retail
  other injuries or a third in retail strains and books 3.4 to 3.8 million; the golden saving without the fill check (R3)
  books 4.2 million. Every rival misses the credit by at least one 100,000 bin and the allocation by at least two teams.
- **Position.** The golden credit sits 44,438 under the 4,150,000 edge and 55,562 over 4,050,000; every team saving sits
  at least 1,892 dollars from its 10,000 edge (RW-SS 286,892), asserted at 1,500.
- **The decisive move.** R0 to R4 moves healthcare strains from 34,106 to 292,364 dollars a team-year, retail strains
  from 28,214 to 286,892, manufacturing strains from 56,016 to 281,996; it reverses the per-claim ranking (strains last
  to strains first) and no lower correction reaches it (R1, R1b, R2, R2b asserted).
- **The cut.** HC-OT (191,656) is the last unit funded and RW-OT (130,715) the first left out, 1.47 times apart; RW-SS
  keeps two teams' places in use (944 intakes in the twelve months to September 2026 at 18.85 place-days, 2.44 teams'
  worth), every other funded unit four or more.
- **Worth on the graded figures.** The default path keeps 3 of 8 team counts (HC-OT, MF-OT, CN-OT) and none of the eight
  team savings or the credit; R3 keeps the eight team savings and six team counts.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | the pilot: every intake on the register, as assigned (SF13); the 2027 credit: the AY2027 intakes the teams take (PM 2), at run rate (PM 3); members not yet observed: the 2027 intakes, carried at the pilot's per-intake measures (PM 5) |
| 2 | Unit of account | the intake (the randomised and the decided unit); teams per segment; dollars of ultimate indemnity; the team-year of 7,300 place-days (PM 3) |
| 3 | Attribution window | pilot triage dates 1 March 2023 to 28 February 2025 (the register); the review's valuation 30 June 2026; 2027 at run rate |
| 4 | As-of dating | extract and payments pulled 30 September 2026; the register 7 March 2025; the case log 4 August 2025 (every pilot file closed, asserted); verified amounts at 30 June 2026 |
| 5 | Version basis | the signed charter (supersedes the drafts); the review as issued |
| 6 | Denominator | each group's intakes on the register for the rate (SF13, SF14); each ERN intake for the place-days (Ch 5.1 to 5.3) |
| 7 | Weighting | none: group rates and sample means within a segment; a sample weighted to its frame gives the same mean within a stratum (SF15) |
| 8 | Window length | the whole pilot; the fill check on any forecast basis (SF5) |
| 9 | Boundary inclusivity | a place-day counts its first and last days (Ch 5.3, SF11); pilot triage dates inclusive |
| 10 | Rounding path | unrounded throughout; team savings to 10,000 and the credit to 100,000 once (SF18 converges) |
| 11 | Tie-break | none at the cut (SF19) |
| 12 | Maturity and censoring | every pilot file closed by the log's export; every pilot indemnity status fixed by 30 June 2026 (SF14); open claims projected by the review (PM 4: open and closed alike) |
| 13 | Order of operations | value, then rank, then three a unit, then the fill limit: a unit's teams are the least of three, its fill limit and the teams left |
| 14 | Row order | file order changes nothing (asserted: the register and the log reversed give the same figures) |
| 15 | Duplicate resolution | the log's reopening rows are added to their file (Ch 5.2, SF12); register claims unique (asserted) |
| 16 | Identity normalisation | the four claim-number forms resolve to one legacy number each (asserted: every review and log row matches exactly one register intake) |
| 17 | Netting against gross | none on the call; Ask 2's voids and returns (SF25, SF26) |
| 18 | Dimensional units | dollars and cents; place-days; 365 days and twenty places a team |
| 19 | Code and status semantics | claim types, groups, closure reasons, payment statuses in the dictionary (field semantics, never the stump) |
| 20 | Integerisation | whole teams; the fill limit floored (a team whose places would sit empty is not given) |
| 21 | Clause scope | PM 4's verified amounts are the credit's; the charter's fill rule over the year (SF4) |
| 22 | Forward window contents | 2027's intakes: the units' own history in the extract (SF5); the per-intake saving and place-days: the pilot's |

## Literal reader

Executed word for word, the pick memo defines the credit as the ultimate indemnity that the AY2027 intakes the teams take
will not pay because the teams took them, what those intakes would pay with their adjusters alone less what they pay
with a team, at run rate (7,300 place-days a team), at the review's verified ultimates, each segment at what its pilot
measured; the charter defines the places, the three-a-unit limit, the fill rule over the year and the place-day. The
literal reader must estimate, from the pilot, what a segment's intakes pay under each group: the register gives every
intake and its group, the extract which of them paid indemnity, the review the verified amount of a sample of those that
did, and the log the place-days each ERN intake held. Read literally, "what those intakes would pay with their adjusters
alone" is usual handling's indemnity per intake, its rate times its severity, and "what they pay with a team" ERN's;
the randomised design rules out every other comparison (SF20). Every term in the fork table resolves to one reading or
converges.

## Oracles

- **None on the call path.** No saving, evaluation, placement, scorecard or prior credit ships; the review states what it
  verified and refuses an effect (R 1.2).
- **The review's totals** (the 1,600 claims' $9,747,283.11 in R 5.1 and the sheet totals) are sums of the verified
  amounts every comparison reads alike; they tie under every basis.
- **The review's frame count** (4,339 pilot claims with indemnity, R 3.1) is the register's intakes that paid indemnity in
  both groups together; the per-claim and per-intake readings both reproduce it, and it does not split by group.
- **The ask paths** (the payments, the ACH returns, the 2025 intakes): no rung of the call reads them.

## Ask sheet

**Main call's declared row population:** every row of the register, the case log, the review workbook and the
crosswalk; the extract's `legacy_claim_no` and `claim_type` on the 5,227 pilot claims (all converted, reported March
2023 to February 2025) and its intakes reported October 2025 to September 2026 (all new-system rows, flag as written)
for the fill check; the charter and the memo. The asks' devices live in the extract's rows reported in 2025 (the
converted rows' flag, the parallel-run copies) and in the payment register and the bank's return file, which no rung of
the call reads. `checks.py` asserts the call unchanged with the payments, the returns and the three distractors removed,
and unchanged with every 2025 row's flag as filed and every copy kept in the fill check (SF5). Zero device rows sit in
the call's population.

Both asks, eight segments each (16 figures), are what the segments' claims cost now, set beside the credit in the note:
a measure every candidate carries that the call does not turn on.

**Ask 1. Each segment's intakes reported in 2025** (8 figures, whole numbers).
- H18 home: the volume each unit's teams would draw from, beside the placement; the call reads the units' latest twelve
  months and does not turn on 2025 (SF5).
- Construction: the extract's claims reported in 2025 in each segment whose first report recorded time lost: for the
  new-system rows the flag; for the rows converted at the 2 June 2025 upgrade, time lost beginning on or before the
  report date; each claim keyed in both systems in the 29 May to 1 June parallel run counted once.
- Primary device (D2, a label stored before a silent switch): the conversion filled `time_off_at_report` from the legacy
  LOST_TIME indicator, which the legacy system set for any claim with lost time on record, so every converted row carries
  Y, the later indemnity conversions among them; nothing narrates it, and the tell is a converted row flagged Y whose time
  lost began after its report (no new-system row is so).
- Second device (D1, the same records under two key schemes): first reports received 29 May to 1 June 2025 were keyed in
  both systems; the converted copy (legacy number, closed within a month, medical only) and the new-system claim share
  office, segment, class and every date, and no key links them.
- Path (4 files, 9 columns): the extract (`legacy_claim_no`, `segment`, `report_date`, `disability_began`,
  `time_off_at_report`, `office`, `class_code`, `injury_date`), the dictionary, the charter (4.1), the crosswalk.
- Stops (asserted): S1 the flag as filed, every row (1,621, 856, 991, 734, 1,442, 812, 1,178, 700): 8 of 8 off; S2 the
  flag fixed, copies kept (1,546, 827, 947, 710, 1,362, 773, 1,118, 669): 8 of 8 off; S3 copies dropped, flag as filed
  (1,612, 851, 983, 732, 1,436, 809, 1,169, 697): 8 of 8 off; answer 1,537, 822, 939, 708, 1,356, 770, 1,109, 666.
  Lazy delta: S1 wrong on 8 of 8.
- Realism: a conversion mapping a legacy status field into a new system's narrower field, and a parallel run's double
  keying left in the data, are what claims-system upgrades leave behind.

**Ask 2. The indemnity paid on each segment's claims, January to September 2026** (8 figures, nearest 1,000 dollars).
- H18 home: what each unit's claims pay now, beside the credit; the call reads the verified amounts and never the payments.
- Construction: each payment issued 1 January to 30 September 2026 once, its claim's segment on the extract; voided checks
  out and their replacements in; the EFTs the bank returned out and the checks re-issued for them in.
- Primary device (D6, an event's quantity on every line it covers): the register lists one line for each week a payment
  covers and carries the payment's amount on each line, so summing lines counts a two-week payment twice; the dictionary
  states the grain flatly, and the tell is a payment whose lines all show the same amount.
- Second device (D4, absence evidenced in a file no habitual join reaches): 275 EFTs the claimants' banks returned stay
  in the register as issued; the returns are only in the bank's file, keyed by trace number, and each was paid again by
  check.
- Hazard (seen, repaired right): 85 voided checks carry status VOID with their replacement as a new payment.
- Path (4 files, 10 columns): the register (`payment_no`, `line`, `claim_no`, `amount`, `status`, `method`,
  `check_or_trace`, `issue_date`), the bank's file (`trace_number`), the extract (`claim_no`, `segment`), the dictionary.
- Stops (asserted): S1 every line, returns in: 8 of 8 off (1.66 to 1.86 times); S2 each payment once, returns in: 8 of
  8 off (10,300 to 50,186 dollars high); S3 lines summed, returns out: 8 of 8 off; answer 3,725,000, 4,652,000,
  1,805,000, 3,993,000, 4,277,000, 5,233,000, 4,999,000, 7,282,000. Lazy delta: S1 wrong on 8 of 8.
- Realism: payment registers export at line grain with the header amount joined on, and ACH returns arrive in the bank's
  own file, not in the claims system.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 converted flag | the 2025 conversion mapping | Ask 1 | every segment, 24 to 80 |
| HA2 parallel-run copies | double keying 29 May to 1 June 2025 | Ask 1 | every segment, 2 to 9 |
| HB1 weekly lines | the register's export grain | Ask 2 | every segment, 1.65 to 1.84 times |
| HB2 ACH returns | claimants' closed or changed accounts | Ask 2 | every segment, 10,300 to 50,186 dollars |
| HB3 voids | lost and stale checks | Ask 2 (seen) | every segment, 3,814 to 15,519 dollars |

**The cracker sheet.** The cracker filed 4,100,000, ran the hygiene battery (keys unique, exact duplicates, every join
matched, no fan-out, counts that tie), executed every filed rule and definition (the charter's intake, the dictionary's
fields and statuses):

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, 8 intake counts | claims reported in 2025 with `time_off_at_report` Y, keys unique | the converted rows' flag carries the legacy indicator; the parallel-run copies share no key with their twins | miss |
| Ask 2, 8 paid totals | issued payments in the window, voids out, by the claim's segment | the amount repeated on each weekly line, and the returned EFTs only in the bank's file; either alone leaves every segment off | miss |
| The placement, team savings, credit and chart (recommendation block, not asks) | from the pilot | carried by the call, scored with it | outside |

The mirror sheet (the same response stopped at R0, 2,000,000) differs only on the recommendation criteria: no ask couples
to the call.

Mirror leakage: 8 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 38 recommendation (eight team counts, eight team savings, the credit, the note's
opening and chart), 7 instruction following, 55 asks over 16 figures (3.4 each). With no device cracked the cracker keeps
the method credit: C = 38 + 7 + 4.4 = 49.4; the mirror keeps r of about 5 (the files, the chart's form, the three team
counts it shares): S = 5 + 7 + 4.4 = 16.4, a pair of 32.9. Every figure needs both of its ask's devices, so cracking the
most obvious one alone (the repeated lines) banks nothing: the pair stays 32.9. Cracking both of one ask's devices adds
27.5: C = 76.9, a pair of 46.7, which needs a second device the battery does not see.

Pair ceiling: 32.9

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| Charter 2.1 to 5.3 and Appendix A | 2, the signed programme charter | seventeen teams, twenty places, one segment a team, three a unit, the fill rule over the year, the intake, the place-day, reopenings | how the saving is estimated, a rate, a kept-at-work intake |
| Pick memo 2 to 6 | 3, the chief pricing actuary's booking memo | the credit as the indemnity the teams' intakes will not pay because the teams took them; run rate; the verified amounts; each segment's own measure; indemnity only | a comparison of the groups, a frequency, a sample |
| Review report 3.1 to 4.4 | 5, the consultant's method notes | the frame, the strata and the sample, the blind verification, the projection of open claims | an effect, a group's frame size |
| The dictionary | 4 | field semantics: claim types, the flag, statuses, the payment register's grain | a device, a conversion mapping |

## Prompt

`prompt.txt`, 817 characters, gated by `voice-check.py` (PASS): the call as a question with its pick, the workbook's
placement (each segment's teams and what one team there saves in a year, the total), the note's opening and chart, the
two asks tied to the note by one motive (what the segments' claims cost now), rounding once at the close (team savings
to 10,000, the total to 100,000, the paid indemnity to 1,000, intakes whole).

## Build record

- **Generator.** `python3 generator/build.py` writes `target/` (15 files, 4 formats; the extract 59,789 rows, the
  payment register 63,135), `golden/` (2), `metadata.json`, `generator/figures.json` and `target.zip`; runs `checks.py`
  (282 assertions: the input gates, R1 to R3c on the clean truth, every SF row, the ladder and every figure this note
  states, the asks' stops, separation, bins, the realism sweep, the registers and the dates) and `verify.py` (the
  placement, the credit, the default path and both asks recomputed from the bundle alone with the csv module and
  openpyxl); then builds again and compares every byte: identical.
- **Write-up and gates.** `figures_check.py` 67 figures, none absent; `precut.py` 49 checks, 0 FAIL, 0 WARN;
  `voice-check.py` PASS.
- **golden-realism.** The note: memo block, a finding as title, the basis paragraphs lopsided toward the call, the
  table with its total, a true footnote from the memo (run rate, the 30 June 2026 valuation, indemnity only), the chart
  with direct labels and the funded, capped and unfunded bars told apart. The workbook: named sheets, frozen headers,
  formats per column, a Notes sheet with definitions, exclusions, rounding and the as-of.
- **reduce-house-fixes.** H1: the container audit is clean on `target/` (floor 2023-01-01, ceiling 2026-11-09) and
  `golden/`; the draft charter is saved as Word leaves it (the library template's bibliography part, effects styles,
  blank preview, Mac namespaces and fixed ids out, its styles cut to those used, its counts from its text). H3: the
  write-up's and the note's default-path clause now say the healthcare and retail strain units get no team (the per-claim
  reading still gives construction and manufacturing strains teams). H4: the zip's members equal `target/` byte for
  byte. H8: every citation resolves (charter 3.2, 3.3 and section 5, pick memo 3 to 5). H9: the manifest lists every
  shipped file and the dictionary's scope line names its six files, asserted. H11: one `prompt.txt`, one
  `submission.md`. H16: no extract, void, bank-return or survey date past its pull, asserted. H2: every figure in this
  note is asserted in `checks.py`. The charter's Appendix A writes each office with its code, so no city name runs into
  the next row's first word.
- **leak.py** (`--asof 2026-11-09`): REVIEW, seven lines, each harmless. The pick memo names Early Return Nursing, the
  programme the prompt names. The signed charter carries the call's distinctive words because Appendix A lists the eight
  segments and their units; it places no team. The pick memo, the draft, the signed charter and the review use the
  programme's own words (intake, verified, place-day, assigned, sample) and none names the comparison: the memo files
  what the credit is, the charter the place-day and the fill rule, the review its frame and sample and that it
  estimates no effect, the draft nothing on placement. The staffing plan's 2027 dates are the 2027 plan's own.
- **guard.py.** `check` PASS (NOTE `same_driver_older`, differentiated against task452 v2); `validate` clean; `surface`
  exit 0, its people Gregory Friedman, Joanna Sullivan, Julie Winters and Kathleen Reilly, all on the card ("Early
  Return" and "Missouri Early" are the programme's name and a heading after a place name), two pairs promoted for an
  adjudicated read: task229 (surface 0.102, a hydrometry monitoring build, no shared mechanism) and task452 (gap,
  pattern, Gate G and calibration form shared, differentiated on the card); `heart` PASS (nearest 0.06, task128's
  ledger row).
- **Stage 4** (the leak reader and the judge) has not run.

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
