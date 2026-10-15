# task141: Dorrance County, the 2027 presumptive pretrial release tier (architecture 1)

Private, never ships. A new build (wave 2), numbered from seed FC12. The seed (a serverless platform's warm-pool memory
reservation for next quarter) was read at its header and Situation only, and its world, decision and quantity are not
kept: a quarterly compute reservation struck at a capacity cut-off reads as the same project as task140 (a compute
cell's quarterly batch guarantee, shipped the day before this draw), so the world is drawn fresh in a client domain no
forecasting build has used. The pitfall is found in how a release decision writes the outcome record: a pretrial
outcome exists only for a defendant a magistrate released.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task141.json`, architecture v1, registered 2026-10-15 after `git pull` (task139 in design and task458 drawn the same day both on file); `guard.py check` PASS, no BLOCK, no WARN; `guard.py validate` clean |
| Domain / task type | `criminology-justice` (client domain), task type `recidivism-risk-assessment` (forecasting): the call is the pretrial new-offence rate each score's eligible defendants would show in 2027 under a tier that releases every one of them, which pretrial research estimates past the selective labels of the outcome record |
| Objective | Forecasting & Predictive Modeling: the safety rate each Pretrial Assessment Scale score would show among the defendants the 2027 policy releases (first appearances from 1 January 2027), a population the outcome record has never seen whole |
| Shape | `04` (setting one dial): the tier's top score is the dial, scores 1 to 6 the settings; criteria from each setting (meets the floor or not, the defendants it covers, the bed-days and missed court dates beside it), plus the call, the runner-up setting, the gap and the flip, the chart's named parts and the three files: about 42 criteria, arithmetic under `## Ask sheet` |
| Decision | `dial_setting`, answer unit `index_or_score` (the highest score the tier reaches) |
| Mechanism | gap population (decisive: the defendants on file with an outcome are the ones magistrates released, the tier releases every eligible defendant at its scores) then time (the 365-day window to disposition, cases open at the extract); pattern none, generators G9 (the measured outcome exists only for the kept units) then G12 (a held defendant's missing outcome is a non-answer, never a zero) and G13 (the window); Gate G `forecasting`; strategy `population_selection` |
| Layer 2 family / pattern | `estimand_identification` (selection on what the decision-maker saw); `criminology-justice/recidivism-risk-assessment/5` (selective labels: outcomes exist only for the released) |
| Furniture | forum `other` (the district's senior resident superior court judge issues the local bail policy after consulting the chief district court judge: a judicial order, not a forum), forcing event `statutory_or_regulatory_filing` (the revised policy is issued and filed with the clerk of superior court by 1 December 2026 to take effect on 1 January 2027), organisation family `local_government` (Dorrance County Pretrial Services), role family `research_desk` (the office's research analyst prepares the tier), context artifact `filed_model` (the Pretrial Assessment Scale's scoring guide: items, points and the six-point new-criminal-activity scale, no outcome rate), calibration `none`, opening `question-first`, question form `what` |
| Spine | `first_appearances_2024-03-04_2026-09-30.csv`, the new case management system's first-appearance export: one row per first appearance before a magistrate, 4 March 2024 to 30 September 2026, beside the legacy system's export from 1 October 2021 to 3 March 2024 in another layout; constructed |
| Deliverables | `presumptive_release_tier_2027.docx` (the memo to the senior resident judge: the tier and each score's case), `presumptive_release_tier_2027.xlsx` (the per-score tables), `held_bed_days_by_score.png` (one chart) |
| People | drawn with `guard.py names --geo "United States" --seed 141` and `--seed 1411`, every name the guard clears: Lauren Mullins (research analyst, Pretrial Services, the requester), Teresa Diaz (director, Dorrance County Pretrial Services), Zachary Henson (senior resident superior court judge, issues the policy), Kristen Thompson (chief district court judge), Jeffrey Francis (chief magistrate), Gina Yoder (jail administrator, Sheriff's Office), Colleen Cameron (clerk of superior court, the court data); none appears in the prompt. The magistrates appear only in the court's roster workbook (a data table) |

**Guard.** `guard.py check` on the registered card: PASS. A first version carried two first names on file in task130
(Michael, Jonathan) and the question form `which` beside task458's; both redrawn before registration (`what`, two names
from the second draw). The bans ran against task456, task457 and task257, the three builds before this one by draw
key, and task458 drawn the same day: no pairing, subdomain, pattern, role, artifact, shape, strategy, forum, event or
organisation family repeats.

**Same-puzzle and same-driver tests.** Gap population, decisive G9, decision `dial_setting`, Gate G `forecasting`: no
build carries that gap, G-code and decision together, and none that gap, G-code and Gate G. The two G9 builds in the
last twelve differ on both: task452 (population, G9, a quantity, method selection: design weights after a sampling map
revision) and task139 (population, G9, an allocation, method selection: a randomised pilot read per assigned intake).

**Abstraction test.** Stripped of nouns, the driver is: outcomes are recorded only for the units a decision-maker let
through, the decision-makers sit by rota and let through different shares, and a rule that lets every unit at a level
through is priced at the rate the whole level would show, read from how outcomes per unit rise with each
decision-maker's let-through share out to all let through. The three nearest drivers on file: task116 v1 lineage (an
offer's realisable value from the groups whose existing purchases show it, 0.08), task60 v2 lineage (forward exposure
netted of outcomes already held, 0.06) and task124 v4 lineage (a rate measured on units examined because they showed
signs of the outcome, carried to a population all of which will be examined, with the groups examined whole giving the
rate, 0.06). task124 v4 shares the latent structure (a measured subset selected on what predicts the outcome) and the
default path (the subset's rate carried to the whole); its correction is a census subset that exists in the data (the
groups examined exhaustively), where here no magistrate releases every eligible defendant at any score, so no subset
of the record is unselected and the full-release rate exists only as the end of the leniency gradient, identified
because the rota assigns arrests to magistrates without regard to the defendant. The lesson differs: there, find the
part of the record that is complete; here, use the variation in who decided to see past a selection that touches every
record. task139 (in design) reads a randomised pilot per assigned intake; here nothing is randomised and no arm exists,
the assignment of decision-makers is the only lever.

**Data-native sentence.** Dorrance County's magistrates set release at first appearance from the arrest affidavit and
the defendant in front of them as well as the screen, and they hold the eligible defendants whose affidavits show what
the scale cannot (about one score-4 defendant in four), so every pretrial outcome on file belongs to a defendant a
magistrate chose to release; the duty rota sends each magistrate the same mix of arrests, and the magistrates hold
from about 2 to 30 per cent of score-4 defendants, so the outcome a whole score would show is read off how
new-offence arrests per eligible first appearance rise with each magistrate's release share, out to every defendant
released.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (51 builds): no build carries a
selective-labels outcome or a decision-maker rota; the nearest ideas are task124 v4's examined-because-of-signs rate
(a census subset fixes it) and task139's randomised pilot (an arm fixes it), and task133's left truncation and
task130's short window are clocks, not selection. `layer2-rigor-patterns.md`, criminology-justice: pattern 5 (selective
labels, the shortcut "evaluate on the released as if all") is the decisive step, pattern 2 (a fixed window from release,
time at risk) a lower rung; pattern 4 (validate on later cohorts) and the shuffled-split reflexes are not used.
`two-layer-task-design.md`: rule 1's swap is run on the call sentence under `## Three rules`; the decisive step is the
data's real structure (selection), which the client lists among the analytical shapes. `measured-drivers.md`: held
tasks sit upstream of every graded figure and outside the solver's hypothesis space; the selection sits upstream of the
tier and of every per-score safety figure, and the solver's own validation on released defendants is the habit it
meets. Seed FC12, header and Situation only, for the slot.

**World.** Dorrance County, North Carolina (fictional; county seat Garrison, about 1.1 million residents) forms one
judicial district. Arrestees are brought before the magistrate on duty at the county detention center's intake for
their initial appearance, where the magistrate sets the conditions of pretrial release (a written promise to appear,
an unsecured bond, release to a custodian, a secured bond) under the district's local bail policy. Dorrance County
Pretrial Services screens arrestees at intake with the Pretrial Assessment Scale (PAS), a points scale from the
statewide criminal record that gives a new-criminal-activity score from 1 to 6 and a failure-to-appear score from 1 to
6, and gives the magistrate the screen before the appearance. The magistrates (32 over the period) work a rotating
duty roster of twelve-hour shifts set by the chief magistrate. The clerk's case management system moved to a new
vendor on 4 March 2024. The district's revised bail policy for 2027 adds a presumptive release tier: eligible
defendants at or below a PAS new-criminal-activity score are released on a written promise to appear at first
appearance, without the magistrate's discretion, if the score meets the policy's 85 per cent safety floor.

As-of dates: the court exports and the state arrest extract run to 30 September 2026 and were pulled on 2 October
2026; the jail export runs to 30 September 2026 23:59 local; the draft revision is dated 6 October 2026 and the analyst
supplies the tier for the judge's 1 December filing; the policy takes effect on 1 January 2027.

## Default path

1. Read the draft revision: the tier covers eligible defendants (every charge a misdemeanor or a Class H or I felony,
   none on the excluded list, no hold for another jurisdiction) at or below a PAS new-criminal-activity score, and a
   score is included only if its safety rate (the share of the defendants the tier releases who are not arrested for a
   new offence within 365 days of release or before the case is disposed) is at least 85 per cent.
2. Stack the two first-appearance exports (legacy to 3 March 2024, new from 4 March), map the offence codes through the
   clerk's crosswalk, keep the eligible first appearances, and attach each one's screen (booking number, then name and
   date of birth) and its score.
3. Find each eligible defendant's release from the jail export (released within a day of the appearance) and the case's
   disposition date; keep first appearances to 30 September 2025 so every 365-day window has closed.
4. Count a new-offence arrest from the state extract (offence date after release, inside the window, warrant-only
   arrests and arrests for older offences out) for each released defendant.
5. Each score's safety rate is the share of its released defendants with no new-offence arrest; scores 1 to 4 clear 85
   per cent (score 4 at about 87), scores 5 and 6 do not; the tier is scores 1 to 4.

Ends on: scores 1 to 4 (the default path's tier; asserted in `checks.py` and recomputed by `verify.py`).
Golden: scores 1 to 3: each score's safety rate for every eligible defendant, released or held, read from the
new-offence arrests per eligible first appearance in each magistrate's caseload against that magistrate's release share
at the score, carried out to full release; score 4 falls to about 81 per cent and fails the floor.

## Stump sentence

A competent solver links the screens to the first appearances, keeps the eligible charges, counts a new-offence arrest
within 365 days of release or before disposition, takes each score's safety rate among the eligible defendants
magistrates released and files the tier at scores 1 to 4 (Ends on; score 4 at about 87 per cent); the step that lands
it there is reading the released defendants as the tier's population, when magistrates held the score-4 defendants they
judged riskiest and the tier releases them all: read from the magistrates' differing release shares, score 4 falls to
about 81 per cent and the tier is scores 1 to 3.

## Three rules

- **Task type:** `criminology-justice` / `recidivism-risk-assessment` (forecasting): the call rests on each PAS score's
  pretrial new-offence rate among the defendants a 2027 presumptive tier would release, a risk-assessment forecast
  for a population the outcome record covers only where a magistrate released.
- **Domain test:** the deciding quantity is the new-offence rate within the pretrial window that each score's eligible
  defendants would show if every one were released, which pretrial research estimates from the release shares and
  outcomes of magistrates the duty rota assigns without regard to the defendant (the selective-labels problem of risk
  assessment); validating the scale on the defendants magistrates released, the field's habit, files scores 1 to 4.
- **Swap:** "Dorrance County's presumptive release tier for 2027 reaches PAS score 3: score 4 falls below the 85 per
  cent safety floor once the defendants magistrates now hold are counted" read with a hospital's nouns ("the emergency
  department's discharge protocol reaches triage level 3") stops making sense: there is no pretrial window from release
  to disposition, no new-offence arrest recorded only for the released, and no duty rota of magistrates whose release
  shares identify the held defendants' risk; with the method swapped (the released defendants' own rate), the call moves
  to scores 1 to 4.
- **Layer 1:** two first-appearance exports from the clerk's old and new case management systems (layouts, case-number
  formats and magistrate keys differ across the 4 March 2024 change), screens keyed by booking number, name and date of
  birth against the court's party numbers, jail times in UTC against court times in Eastern local time, offence codes
  recoded at the system change and joined through the clerk's crosswalk, a state arrest extract that mixes new-offence
  arrests with warrant service and arrests for older offences, dispositions in their own export with cases still open
  at the extract; each is what these systems write, and none decides the call.
- **Layer 2:** family `estimand_identification`: the shortcut validates each score on the defendants with an outcome
  (the released) and carries that rate to every eligible defendant the tier will release; the expert reads each score's
  full-release rate from the variation in release shares across magistrates the rota assigns at random, the selection
  the outcome record carries.
- **Decisive step:** estimating each score's pretrial new-offence rate for all its eligible defendants from the
  leniency gradient (each magistrate's new-offence arrests per eligible first appearance against that magistrate's
  release share at the score, extended to full release) instead of from the released defendants alone: the
  selective-labels correction of pretrial risk assessment, done on the rota's quasi-random assignment.
- **Not semantics:** every field the call reads means one thing and the easy route reads each correctly (the release
  decision and the jail release time, the score, the offence and arrest dates, the disposition, the eligibility codes);
  the fork table's rows are closed and none is the stump, and with every field read right the released defendants'
  own rate still puts score 4 at about 87 per cent and files scores 1 to 4.
- **Not rule application:** the draft revision files the estimand (the eligible population, the 365-day window to
  disposition, the 85 per cent floor, the tier's defendants as the safety rate's population) and leaves the estimate to
  the analyst; executing every filed rule with the released defendants' rate files scores 1 to 4, and no rule,
  procedure or document performs the step that moves it to scores 1 to 3 (reading the full-release rate from the
  magistrates' release shares).
- **Analyst test:** a strong analyst who links every file correctly, applies the eligibility rules and the 365-day
  window and computes each score's safety rate among the eligible defendants magistrates released files scores 1 to 4
  (score 4 at about 87 per cent); with a logistic model on the released defendants' charges and records, a reweighting
  of them to the eligible population, or the latest year alone, the same; with the held counted as not arrested, the
  same; only each score's rate read from the magistrates' differing release shares out to full release files scores 1 to
  3.
- **Estimand:** the draft revision's sections on the presumptive tier and its safety floor (the eligible defendants
  the tier releases at a score, a new-offence arrest within 365 days of release or before disposition, at least 85 per
  cent with none) with the prompt's question (the 2027 policy); the draft is the filed standard for the estimand, the
  scoring guide and the extract notes carry the scale and the files.
- **No decoy:** nothing is planted to be caught: no copied or backfilled block, no hidden rule, and no memo, draft,
  briefing or stakeholder figure gives a per-score safety rate, a tier or a method; the scoring guide states the scale's
  items and points and no outcome rate, and the current policy, the statewide statistics and the crime series are
  context and declared distractors.
- **No certified replay:** the full-release rates are estimated from the first appearances, the jail releases and the
  arrests on file; no certified or published figure has to be reproduced to find them, and nothing in the pack reports a
  safety rate by score.
- **Lesson:** an outcome recorded only where a decision-maker let a unit through is selected on what that
  decision-maker saw, so a rule that lets every unit through is priced from the variation among decision-makers
  assigned at random (the outcome per case rising with the share let through), never from the units already let
  through; no build on file teaches selection by a decision-maker or the leniency design.

## Readability screen

Written at stage 2.

## Semantic fork table

Written at stage 2.

## Ladder

Written at stage 2.

## Closure table

Written at stage 2.

## Literal reader

Written at stage 2.

## Oracles

Written at stage 2.

## Ask sheet

Written at stage 2.

## Tried and rejected

- The seed's world, decision and quantity (a serverless platform's warm-pool memory to reserve for next quarter, a
  host released only when its last instance goes cold): a quarterly compute reservation at a capacity cut-off is the
  same project as task140 (shipped 2026-10-15, a compute cell's quarterly batch guarantee) to the guard's reader and a
  reviewer's, and the seed's mechanism (the union of keep-alive windows over an app's functions) is rule application;
  dropped at the draw for a client domain no forecasting build has used.
- An ML lab's compute-optimal model size from scaling-law runs (mid-schedule checkpoints overstate a short run's loss):
  "batch training", "compute budget" and "2027 Q1" echo task140's world; dropped at the draw.
- A school-age population projection with gross migration flows against net rates (Sociology & Demography): the
  cohort-component projection carries a fork for every component (fertility, mortality, international migration, the
  origin's own projection), and a net-rate method is a practice a judge could call defensible; dropped at the draw.
- A seat-majority probability from district polls with a correlated national error (Political Science): the national
  error component is sized from a handful of past elections (small counts); dropped at the draw.
- A shelter's nightly demand censored at its bed capacity (a Tobit on full nights): the cap is visible as a pile of
  nights at exactly capacity, so the censoring is a schema read; dropped at the draw.
- A per-score floor checked on the tier's whole population at once (the cumulative safety rate of scores 1 to k): the
  selection at score 4 is diluted by scores 1 to 3, leaving the full-release estimates within a point of the floor; the
  floor is applied score by score (each score included only if its own rate meets it), which keeps every leniency
  estimate on the same side.
