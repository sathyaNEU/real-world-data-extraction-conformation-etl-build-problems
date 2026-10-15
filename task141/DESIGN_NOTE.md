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
| Shape | `04` (setting one dial): the tier's top score is the dial, scores 1 to 6 the settings; criteria from each setting (meets the floor or not, the defendants it covers, the bed-days and missed court dates beside it), plus the call, the runner-up setting, the gap and the flip, the chart's named parts and the three files: about 47 criteria (the call and its components about 7, the files and the chart's title and axis about 4, the asks' 30 figures and the chart's six bars 36), arithmetic under `## Ask sheet` |
| Decision | `dial_setting`, answer unit `index_or_score` (the highest score the tier reaches) |
| Mechanism | gap population (decisive: the defendants on file with an outcome are the ones magistrates released, the tier releases every eligible defendant at its scores) then time (the 365-day window to disposition, cases open at the extract); pattern none, generators G9 (the measured outcome exists only for the kept units) then G12 (a held defendant's missing outcome is a non-answer, never a zero) and G13 (the window); Gate G `forecasting`; strategy `population_selection` |
| Layer 2 family / pattern | `estimand_identification` (selection on what the decision-maker saw); `criminology-justice/recidivism-risk-assessment/5` (selective labels: outcomes exist only for the released) |
| Furniture | forum `other` (the district's senior resident superior court judge issues the local bail policy after consulting the chief district court judge: a judicial order, not a forum), forcing event `statutory_or_regulatory_filing` (the revised policy is issued and filed with the clerk of superior court by 1 December 2026 to take effect on 1 January 2027), organisation family `local_government` (Dorrance County Pretrial Services), role family `research_desk` (the office's research analyst prepares the tier), context artifact `filed_model` (the Pretrial Assessment Scale's scoring guide: items, points and the six-point new-criminal-activity scale, no outcome rate), calibration `none`, opening `question-first`, question form `what` |
| Spine | `first_appearances_2024-03-04_2026-09-30.csv`, the new case management system's first-appearance export: one row per first appearance before a magistrate, 4 March 2024 to 30 September 2026, beside the legacy system's export from 1 October 2021 to 3 March 2024 in another layout; constructed |
| Deliverables | `presumptive_release_tier_2027.docx` (the memo to the senior resident judge: the tier and each score's case), `presumptive_release_tier_2027.xlsx` (the safety floor by score and the three ask tables), `missed_court_dates_by_fta_score.png` (Ask B's shares by failure-to-appear score) |
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
from about 1 to 36 per cent of score-4 defendants, so the outcome a whole score would show is read off how
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

1. Read the draft revision: the tier covers eligible defendants (every charge a misdemeanor, none on the excluded
   list in Appendix B, no hold for another jurisdiction) at or below a PAS new-criminal-activity score, and a score is
   included only if at least 85 per cent of the eligible defendants the tier releases at it complete the pretrial period
   (365 days from release or the last charge's disposition, whichever comes first) without a new-offence arrest.
2. Stack the two first-appearance exports (legacy to 3 March 2024 through the clerk's crosswalk and the roster's
   initials, new from 4 March), keep the eligible first appearances, and attach each one's screen (booking number,
   paper screens by state number) and its score.
3. Find each eligible defendant's release from the jail export (left within 24 hours of the appearance, the README's
   definition) and the cases' disposition dates; keep first appearances to 30 September 2025 so every window has closed.
4. Count a new-offence arrest from the state extract (type NEW, offence after the release day, inside the window) for
   each released defendant.
5. Each score's safety rate is the share of its released defendants with no new-offence arrest: 95.5, 93.9, 91.9 and
   87.9 per cent at scores 1 to 4, 78.0 and 73.8 at scores 5 and 6; the tier is scores 1 to 4.

Ends on: scores 1 to 4 (the default path's tier, score 4 at 87.9 per cent; asserted in `checks.py` and recomputed by
`verify.py`).
Golden: scores 1 to 3: each score's safety rate for every eligible defendant, released or held, read from the
new-offence arrests per eligible first appearance in each magistrate's caseload against that magistrate's release share
at the score, carried out to full release; score 4 falls to 75.8 per cent (under 80 on every construction of the
gradient) and fails the floor, score 3 holds at 90.3.

## Stump sentence

A competent solver links the screens to the first appearances, keeps the eligible charges, counts a new-offence arrest
within 365 days of release or before disposition, takes each score's safety rate among the eligible defendants
magistrates released and files the tier at scores 1 to 4 (Ends on; score 4 at 87.9 per cent); the step that lands it
there is reading the released defendants as the tier's population, when magistrates held 26 per cent of eligible
score-4 defendants, the ones they judged riskiest, and the tier releases them all: read from the magistrates'
differing release shares, score 4 falls to about 76 per cent and the tier is scores 1 to 3.

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
  birth (paper screens carry no booking number) against the court's party numbers, jail times in UTC against court
  times in Eastern local time, offence codes
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
  own rate still puts score 4 at 87.9 per cent and files scores 1 to 4.
- **Not rule application:** the draft revision files the estimand (the eligible population, the 365-day window to
  disposition, the 85 per cent floor, the tier's defendants as the safety rate's population) and leaves the estimate to
  the analyst; executing every filed rule with the released defendants' rate files scores 1 to 4, and no rule,
  procedure or document performs the step that moves it to scores 1 to 3 (reading the full-release rate from the
  magistrates' release shares).
- **Analyst test:** a strong analyst who links every file correctly, applies the eligibility rules and the 365-day
  window and computes each score's safety rate among the eligible defendants magistrates released files scores 1 to 4
  (score 4 at 87.9 per cent); with a logistic model on the released defendants' charges and records, a reweighting
  of them to the eligible population, or the latest year alone, the same; with the held counted as not arrested, the
  same; only each score's rate read from the magistrates' differing release shares out to full release files scores 1 to
  3.
- **Estimand:** the draft revision's sections on the presumptive tier and its safety floor (the eligible defendants
  the tier releases at a score, a new-offence arrest within 365 days of release or before disposition, at least 85 per
  cent with none) with the prompt's question (the 2027 policy); the draft is the filed standard for the estimand, the
  scoring guide and the extract notes carry the scale and the files.
- **No decoy:** nothing is planted to be caught: no copied or backfilled block, no hidden rule, and no memo, draft,
  briefing or stakeholder figure gives a per-score safety rate, a tier or a method; the scoring guide states the scale's
  items and points and no outcome rate; the current policy is context, and the advisory council's 2025 jail population
  report and the reported-crime series are declared distractors.
- **No certified replay:** the full-release rates are estimated from the first appearances, the jail releases and the
  arrests on file; no certified or published figure has to be reproduced to find them, and nothing in the pack reports a
  safety rate by score.
- **Lesson:** an outcome recorded only where a decision-maker let a unit through is selected on what that
  decision-maker saw, so a rule that lets every unit through is priced from the variation among decision-makers
  assigned at random (the outcome per case rising with the share let through), never from the units already let
  through; no build on file teaches selection by a decision-maker or the leniency design.

## Readability screen

Six tests per rung: 1 a filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a
reflex of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction,
ratio or half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R-1 eligibility on the lead charge only | draft 2.1 names every charge | the new export's charges file, the legacy charge list | no | no | no | yes | readable |
| R-1b the 365-day window with no disposition cap | draft 2.4 names both ends | the dispositions export | no | no | no | yes | readable |
| R0 each score's safety rate among the eligible defendants magistrates released (the default path) | no | no | yes (validate the scale on the defendants with an outcome) | no | no | yes | readable |
| R0b the same on the latest closed year (first appearances from 1 October 2024 to 30 September 2025) | no | no | yes | no | no | yes | readable |
| R0c the held counted as not arrested (every eligible defendant in the denominator, arrests only among the released) | no | no | yes | no | no | yes | readable |
| R1 a logistic model of a new-offence arrest on the released defendants' scale items, charge class and age, averaged over every eligible defendant at the score | no | the screen's items | yes (adjust for what is observed) | no | no | no | readable |
| R1b the released defendants reweighted to every eligible defendant on the same observed items (inverse probability of release) | no | no | yes | no | no | no | readable |
| R2 the held counted as all arrested (the worst case) | no | no | no | no | no | yes | readable |
| R3 (decisive) each score's rate for every eligible defendant, read from the new-offence arrests per eligible first appearance in each magistrate's caseload against that magistrate's release share at the score, extended to full release | no sentence names a selection, a magistrate's release share, a held defendant's risk or a gradient; draft 2.3 states the population (the defendants the tier releases) and the floor, and the current policy's 2.3 says only that magistrates sit by the chief magistrate's rota | the magistrate key is on every appearance, as on any first-appearance record, and nothing pairs it with an outcome; no column holds a release share, a risk the magistrate saw or a full-release rate | no: the reflexes are R0 to R1b, and each files its own tier | no closed record scores a method: nothing on file states a safety rate by score, by magistrate or for the held | no | no: a fitted gradient across 32 magistrates at each score, extended to a release share no magistrate reached | silent |

The decisive rung is silent because the defendants with an outcome look like the population: they are most of every
score (about 98 per cent at score 1, 74 per cent at score 4), every file joins cleanly, and the scale's
validation habit is to read its rates off them. Nothing in the pack says magistrates see more than the scale; the
records show it only to an analyst who compares the released defendants' outcomes across magistrates who released
different shares of the same mix of arrests.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs, then the asks' readings. `checks.py`
asserts each row (the alternative computed and shown to move the call or its figures, or shown to converge). The draft
is `bail_policy_revision_2027_draft.docx`; the current policy is `local_bail_policy_2024.pdf`.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the highest ... score" | the tier's top score: the highest score with every score from 1 to it meeting the floor | the highest score meeting the floor on its own | same call (asserted: scores 1 to 3 meet it, 4 to 6 do not, on every rung's estimate) | draft 2.5 |
| SF2 | "new-criminal-activity score" | the NCA score on the defendant's screen, 1 to 6 | the failure-to-appear score | moves the call (asserted) | the prompt; draft 2.2; the scoring guide's two scales |
| SF3 | "eligible defendants" | every charge at the first appearance a misdemeanor, none in Appendix B, no detainer from another jurisdiction | the lead charge only | same call (asserted) | draft 2.1 ("each charge") |
| SF4 | the tier's population | every eligible defendant at the score, all released on a written promise | the defendants magistrates released at the score | moves the call (it is the default path's estimate, R0) | draft 2.2 ("shall be released") and 2.3 ("of the eligible defendants the tier releases at that score") |
| SF5 | "safety floor" | at least 85 per cent of the tier's defendants at a score with no new-offence arrest in the window | no new arrest and no missed court date (a success rate) | moves the call (asserted) | draft 2.3 |
| SF6 | "new-offence arrest" | an arrest anywhere in North Carolina for an offence committed after the day of release; arrests on orders for arrest, on warrants for offences before release and for probation violations are not | every arrest in the extract after release (orders for arrest and warrants included) | moves the call (asserted) | draft 2.4 ("An arrest on an order for arrest, on a warrant for an offense committed before release, or for a probation violation is not a new-offense arrest") |
| SF7 | the window | from the day after release to 365 days after it or to the disposition of the last of the appearance's charges, whichever comes first | 365 days flat; to the first charge's disposition | 365 days flat moves the call (asserted); the first charge's disposition is the same call (asserted) | draft 2.4 ("whichever comes first", "the last of the defendant's charges") |
| SF8 | released at first appearance (the history's release, the window's start) | left the detention center within 24 hours of the appearance on the conditions set at it, a secured bond posted in that time included | the condition alone (a secured bond as held); within 48 hours | same call under each (asserted: no release between 24 and 48 hours after an appearance) | the README's release definition ("leaving the detention center within 24 hours of the first appearance on the conditions set at it, a secured bond posted in that time included") |
| SF9 | the history the projection is read from | first appearances from 1 October 2021 to 30 September 2025, every window closed at the extract | the last two closed years; the last closed year; all five years with the open windows counted as far as they run | same call under each (asserted) | the records converge; the README (arrests to 30 September 2026) |
| SF10 | "85 per cent" | at least 85.0 per cent | more than 85 | same call (asserted: no estimate of any score within 1.5 points of 85 under any leniency variant) | draft 2.3 ("at least") |
| SF11 | the 2027 population at a score | the eligible defendants at the score in the history's mix | the latest year's mix | n/a: the floor applies score by score, so the mix within a score does not enter | draft 2.5 |
| SF12 | a magistrate across the 4 March 2024 change | one decision-maker under the roster's initials and employee number | the legacy and new keys as two decision-makers | same call (asserted) | the roster; the records converge |
| SF13 | the estimate of each score's rate for every eligible defendant | the leniency gradient at full release (R3) | the released defendants' rate (R0), the latest year (R0b), the held as not arrested (R0c), a model on the released (R1), a reweighting (R1b), the held as arrested (R2) | each files its own tier (Ladder) | a method row, not a reading: the design forces it. The rota assigns arrests to magistrates without regard to the defendant (the current policy's 2.3; asserted: every magistrate's share of score-4-and-up appearances within four standard errors of the pooled share), and at every score from 3 up the released defendants' new-offence rate rises with the magistrate's release share (asserted: the most lenient fifth of magistrates' released defendants at score 4 show a new-offence rate of 19.8 per cent against the strictest fifth's 10.0), which can only be the held defendants' risk entering as release widens; the released defendants' rate is therefore not the tier's, and the gradient across the 32 magistrates is the record's own measure of it |
| SF14 | a defendant with several first appearances | each appearance a unit (the tier applies at each) | the first appearance per defendant | same call (asserted) | draft 2.2 ("at first appearance") |
| SF15 | a first appearance's screen | the screen run at that booking, matched on the booking number (legacy numbers without the B prefix), else on name and date of birth | (none: one screen per booking in the history) | n/a | asserted: every eligible first appearance in the history matches exactly one screen |
| SF16 | a first appearance with no screen | outside the tier (no score) | (none) | n/a | draft 2.2 ("whose screen shows a score") |
| SF17 | Ask A "bed-days" | one for each midnight (Eastern) at which the defendant is held | days or part of a day held (S6); UTC midnights (S4) | moves every figure (asserted) | the README's detention definition ("one bed-day is counted for each midnight count at which the person is held"; the jail export "is UTC") |
| SF18 | Ask A "in custody" | held at the detention center or boarded at Halsey County's jail | released when the jail records the defendant boarded out (S1) | moves every figure (asserted) | the prompt ("bed-days in custody"); the jail code list (`BO` boarded out to a contract facility, not a release) |
| SF19 | Ask A "held after a first appearance" and the stay counted | eligible, still in custody 24 hours after the appearance; the whole stay from booking to release | the nights from the appearance only | moves the figures where a booking crosses a midnight before the appearance | the README ("a stay runs from booking to release"; "A defendant still in custody 24 hours after the appearance is held after it") |
| SF20 | Ask A "to 30 September 2026" | the midnight counts dated up to 30 September 2026 (the count at 00:00 on 30 September the last) | the count at 00:00 on 1 October 2026 included | moves every score held at the extract (asserted) | the README's detention definition ("the count taken at midnight is dated with the day it begins") |
| SF21 | Ask A one defendant's custody | one stay from booking to final release across a boarding, a return booking or an annex move | each booking separately to its first release | moves every figure (asserted) | the jail code list (`BI` returned from a contract facility, `TRF` moved between housing sites); the records |
| SF22 | Ask B "a missed court date on that appearance's charges" | an order for arrest issued for a failure to appear (the current policy's 1.4) in a case carrying a charge from the appearance, the superior court case an indictment opens included | the appearance's district case numbers only (S1); every case under the defendant's district party number (S2) | S1 moves 5 of 6 counts and 5 of 6 shares, S2 all 12 (asserted) | the prompt ("on that appearance's charges"); the current policy's 1.4; the case index (a superior court case's `district_case_ref`) |
| SF23 | Ask B "within 90 days of release" | orders for court dates from the release day to the 90th day after it | the order's issue date in the 90 days | converges (asserted: every order issues on its court date) | the records converge |
| SF24 | Ask B the unit and the share | each release at a first appearance a unit (a defendant released twice counts twice); releases followed by a missed date over the releases at the score | defendants | n/a | the prompt ("how many releases", "what share of those releases") |
| SF25 | Ask C "days on electronic monitoring" | calendar days on which a monitor was on the defendant, each day counted once | the vendor's billable days summed (S1); each invoice line's enrollment dates counted (S2); each enrollment counted on its own (S3) | moves every figure (asserted) | the prompt ("the days ... of every defendant"); the vendor's invoice notes (billable days per enrollment, a day or part of a day); asserted: an equipment change ends one enrollment and opens another the same day |
| SF26 | Ask C the population | every defendant released within 24 hours of a first appearance from 1 October 2025 to 30 September 2026, any charge, by the screen's NCA score | eligible defendants only | moves the figures | the prompt ("every defendant released"); the README's release definition |
| SF27 | Ask C "to that date" | monitoring days through 30 September 2026, open enrollments counted to it | (none) | n/a | the prompt |
| SF28 | Ask C a vendor line with no case number | matched to the defendant by name and date of birth | dropped | moves the figures (asserted) | the records |
| SF29 | the chart | Ask B's share by failure-to-appear score, one bar each | (none) | n/a | the prompt |

The stump is none of these rows: every term is read the same way by a careful reader, and the default path reads
them all correctly. SF4 is the population row, and the draft fixes it (every eligible defendant at the score); the
default path keeps that population and estimates its rate from the released defendants, which SF13 lists as a method
and the records refute. SF17 to SF29 are the asks' readings, each closed by a cited sentence or an asserted data fact.

## Ladder

Every rung is a complete pipeline on the same literal estimand (draft 2.1 to 2.5), computed by `calc.ladder` from the
built pack and asserted by name in `checks.py`; the default path and the golden are recomputed by `verify.py`. Safety
rates in per cent:

| Rung | Score 3 | Score 4 | Score 5 | Tier |
|---|---|---|---|---|
| R0 (default) released defendants' rate | 91.9 | 87.9 | 78.0 | scores 1 to 4 |
| R0b latest closed year (first appearances from 1 October 2024) | 92.3 | 88.8 | 77.2 | scores 1 to 4 |
| R0c held as not arrested | 92.8 | 91.1 | 84.7 | scores 1 to 4 |
| R1 logistic on the released, averaged over the eligible | 91.9 | 87.9 | 78.0 | scores 1 to 4 |
| R1b reweighted to the eligible | 91.9 | 87.9 | 78.0 | scores 1 to 4 |
| R2 held as arrested | 81.7 | 65.1 | 54.4 | scores 1 and 2 |
| R3 golden, the leniency gradient at full release (caseload-weighted line) | 90.3 | 75.8 | 63.6 | scores 1 to 3 |
| Clean truth (the generator's counterfactual, never shipped) | 89.9 | 72.5 | 63.3 | scores 1 to 3 |

Every construction of the gradient files scores 1 to 3: the unweighted line (score 4 at 75.4), the leave-out
leniency instrument (73.3), the two halves' ratio (78.0), the quadratic line (70.5), the released defendants' rate on
the release share (73.9), the instrument over all scores (74.6) and the most lenient fifth's own released defendants
(80.2); score 3 sits between 89.1 and 91.3 on all of them.

- **Separation.** The golden is bracketed: every route that reads the released defendants as the tier's population
  (R0 to R1b) files scores 1 to 4, the worst case files scores 1 and 2, and only the magistrates' gradient files scores
  1 to 3. Every construction of the gradient puts score 4 at least 4.8 points under the floor (80.2 the highest) and
  score 3 at least 4.1 points over it (89.1 the lowest); every R0-family route puts score 4 at least 2.9 points over it
  and score 5 under it (asserted).
- **Position.** Score 4 decides: its full-release estimate sits 9.2 points under the floor on the golden path and its
  released-only rate 2.9 points over it; score 3 sits over the floor on every route but R2; score 5 under it on every
  route.
- **Grid.** The estimate routes (R0, R0c, R1, R3) by the two release definitions (24 hours, the condition) by the two
  window ends (the last charge's disposition, the first's) by the two histories (four closed years, the last closed
  year): 32 cells in `checks.py`; the eight R3 cells alone file scores 1 to 3 (asserted).
- **Worth on the graded figures.** R3 moves the tier and score 4's verdict; the asks' figures are the same on every
  rung (they read no estimate).
- **Why the gradient is the record's measure.** At score 4 the line's slope (0.59 new-offence arrests per eligible
  appearance per unit of release share) is five times the released defendants' own rate (0.12): the defendants a
  more lenient magistrate adds are far riskier than those every magistrate releases (asserted in `checks.py`).

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | every eligible first appearance at a score (draft 2.1), released or held; members not yet observed: the tier's 2027 defendants, projected from the first appearances whose windows had closed at the extract (1 October 2021 to 30 September 2025); the open windows of the last year counted as far as they run converge (SF9, asserted) |
| 2 | Unit of account | a first appearance (draft 2.2 applies the tier at each); per defendant converges (SF14, asserted) |
| 3 | Attribution window | an arrest belongs to an appearance when its offence date falls in that appearance's window (draft 2.4) |
| 4 | As-of dating | the extracts to 30 September 2026 (pulled 2 October); a score as screened at the booking |
| 5 | Version basis | offence codes before 4 March 2024 mapped through the clerk's crosswalk; the scale's version 2 throughout (the scoring guide) |
| 6 | Denominator | every eligible appearance at the score (draft 2.3) |
| 7 | Weighting | each appearance alike; the magistrate-level fit weighted by caseload or not converges (asserted) |
| 8 | Window length | the four closed years; two years or one converge (SF9, asserted) |
| 9 | Boundary inclusivity | "at least 85 per cent"; no estimate within 1.5 points of 85 (SF10, asserted) |
| 10 | Rounding path | estimates carried unrounded to the comparison; the call is a score |
| 11 | Tie-break | none: one score decides |
| 12 | Maturity and censoring | the history's windows closed by construction (appearances to 30 September 2025, arrests to 30 September 2026); cases open at the extract end their window at 365 days (asserted none of the history's windows is cut by the extract) |
| 13 | Order of operations | eligibility, then the screen, then the release, then the window and its arrests, then the estimate |
| 14 | Row order | file order changes nothing (asserted on shuffled rows) |
| 15 | Duplicate resolution | one appearance per booking (asserted); arrests repeated across the extract's two charge rows counted once per arrest (asserted) |
| 16 | Identity normalisation | the state identification number across the jail export, the new court export and the arrest extract; legacy appearances to the jail by booking number; screens by booking number, else name and date of birth (SF15); magistrates through the roster (SF12) |
| 17 | Netting against gross | none |
| 18 | Dimensional units | rates per appearance; days for the window |
| 19 | Code and status semantics | release conditions, jail release types, arrest types, disposition codes and offence classes, each in the README or a code list |
| 20 | Integerisation | none on the call |
| 21 | Clause scope | draft 2.1 to 2.5 apply to the tier; the current policy's definitions (1.4) where the draft cites them |
| 22 | Forward window contents | the 2027 appearances as the history's eligible defendants: the scale, the eligibility rules and the arrest mix unchanged (the draft changes only who decides release at scores in the tier) |

## Literal reader

Executed word for word, the prompt and the draft define the tier's top score as the highest score at which every
score from 1 up meets the floor (2.5), a score meeting it when at least 85 per cent of the eligible defendants the tier
releases at that score (2.3: every eligible defendant at the score, 2.2) have no new-offence arrest (2.4: an offence
committed after the day of release, within 365 days of release or before the last charge is disposed, whichever comes
first). The draft leaves the estimate for 2027 to the analyst and names no method; the only population with an outcome
on file is the defendants magistrates released, and the records show that population is not the tier's: magistrates who release more of the same
mix of arrests see more new-offence arrests among the defendants they release, so the held defendants are riskier and
the only estimate of the tier's rate the records support is the one read from that gradient out to full release. Every
term in the fork table resolves to one reading or converges; the only step the text leaves open is how to estimate the
rate of defendants never released, which the records then settle.

## Oracles

- **None on the call path.** No file states a safety rate, a new-offence rate or a release share by score, by
  magistrate or for the held, and no file states a tier. The scoring guide gives the scale's items and points only.
- **The Criminal Justice Advisory Council's 2025 jail population report (distractor)** gives the detention center's
  bookings, releases and midnight counts by month for 2025, not by score or for the held; the reported-crime series
  (distractor) gives offences reported by county agencies by year; neither scores a method, and the call and every ask
  read neither (asserted).
- **The current policy** has no presumptive tier and states no outcome figure.
- **The ask paths** (the jail's later stays and Halsey County's bills, the court events and the case index, the
  monitoring vendor's invoices): no rung of the call reads them (asserted: the call is unchanged with every ask file
  deleted), and nothing in the pack states a bed-day, missed-date or monitoring figure by score, so none ties only under
  the golden.

## Ask sheet

**Main call's declared row population:** the eligible first appearances from 1 October 2021 to 30 September 2025 in
both exports and their charges, their screens, their jail bookings' release times, their arrests in the state extract
to 30 September 2026 and their cases' disposition dates, with the crosswalk, the roster, the draft, the current policy
and the README. Device and hazard rows in it: 0 (asserted by count: no boarded-out release or return booking before 30
September 2025, since the boarding began on 3 November 2025; no eligible history appearance has an indicted case; the
call reads neither the court events, Halsey's bills nor the vendor's invoices). The asks read the jail export's later
stays and Halsey County's board bills (Ask A), the court events and the case index (Ask B), and the monitoring
vendor's invoices (Ask C), all on first appearances from 1 October 2025, outside the call's window. Each is a measure
every score carries that the call does not turn on; none is keyed to the call, its construction or its figures; the
three share no primary device and no primary file. No sentence in the pack adjudicates a device: the README states
each file's fields, the detention count and the release definition, the jail code list each code, the vendor's note
its billing basis.

**Ask A. For each new-criminal-activity score, the bed-days in custody to 30 September 2026 of eligible defendants held
after a first appearance from 1 October 2025 to 30 September 2026** (6 figures, nearest 10): 2,210, 4,660, 5,950,
8,330, 3,440 and 2,040 at scores 1 to 6 (unrounded 2,213, 4,661, 5,949, 8,329, 3,438, 2,037; each at least 0.2 of its
bin from an edge).
- H18 home: the jail use each score's held defendants carry (a measure every candidate tier sets free in part, which
  the call does not turn on); use: the memo's account of the custody the tier's scores carry.
- Construction: each eligible appearance not released within 24 hours; its custody from booking to final release,
  through annex moves (`TRF`, the next booking at the same minute), a boarding at Halsey County (`BO`) and a return
  (`BI`), or to the date out on Halsey's bills for a defendant released there; one bed-day for each Eastern midnight
  held, to the count of 30 September 2026; summed by score. Golden equals the clean truth at every score (asserted).
- Primary device (D4, absence as the signal, evidenced in a file no habitual join reaches): from 3 November 2025 the
  detention center boarded held defendants at Halsey County's jail; the jail export ends the stay at the boarding and
  books a return only for those who came back, while about two in five were released from Halsey, whose nights appear
  only on Halsey's monthly bills under Halsey's booking numbers (three lines in ten without Dorrance's booking number),
  matched by name and date of birth.
- Hazards: HA1 (D8) the jail's times are UTC and the count is Eastern; HA2 (D3) Halsey bills a day or part of a day;
  HA3 (D6) a stay crossing a month end sits on each month's sheet with its own date in; HA4 annex moves book the same
  defendant under a new booking number at the same minute.
- Stops (computed and asserted, each missing all 6): S1 `BO` read as the release 1,760, 3,300, 4,770, 6,640, 2,510,
  1,630; S2 `BO` chained to the next booking 4,590, 10,720, 10,840, 13,490, 6,790, 3,420; S3 Halsey's billed days for
  the boarded part 2,250, 4,740, 6,030, 8,450, 3,500, 2,070; S4 UTC midnights 2,190, 4,610, 5,890, 8,250, 3,400, 2,020;
  S5 `BO` chained to a return, else read as the release 1,980, 3,970, 5,360, 7,530, 2,960, 1,850; S6 days or part of a
  day 2,340, 4,950, 6,290, 8,800, 3,620, 2,160; S7 Halsey's month lines each counted from their dates 2,320, 5,040,
  6,320, 8,730, 3,670, 2,080.
- Span: the jail export, Halsey's bills, both first-appearance exports and the charges file, the screens, the
  crosswalk, the README, the jail code list (eight files; booking and release times, types, facility, Halsey's dates
  and names, eligibility codes, the score).
- Realism: boarding held defendants at a neighbouring county's jail under a per diem contract is how North Carolina
  detention centers handle a closed housing unit, and the host county bills by its own booking numbers.

**Ask B. For each failure-to-appear score, how many releases at a first appearance from 1 October 2025 to 30 June 2026
were followed within 90 days by a missed court date on that appearance's charges, and what share of those releases that
is** (6 counts and 6 shares, per cent to one decimal), charted in `missed_court_dates_by_fta_score.png`: 260 of 6,860
(3.8), 349 of 5,525 (6.3), 340 of 3,364 (10.1), 308 of 1,976 (15.6), 78 of 338 (23.1), 20 of 77 (26.0); every share at
least 0.24 of its bin from an edge.
- H18 home: the court's appearance record for released defendants at each failure-to-appear score (a measure every
  release decision carries that the safety floor does not turn on); use: the memo's account of the court dates the
  tier's written promises ask defendants to keep.
- Construction: each release within 24 hours, any charge; its cases, and the superior court case each indictment
  opens (the case index's `district_case_ref`); an FTA event (called and failed, order for arrest issued) in any of
  them for a court date from the release day to the 90th day after; releases with one or more, by failure-to-appear
  score, over the releases at the score. Golden equals the clean truth at every score (asserted).
- Primary device (D7, the true key elsewhere: a prior-id chain): a felony indicted in superior court continues under a
  new superior court case number and party number; the district case shows the indictment as its disposition, and the
  superior court case carries the district case number in `district_case_ref`. Joined on the appearance's own case
  numbers, every superior court failure is missed.
- Hazards: HB1 orders recalled and reissued (`OFAR`, `OFARI`) beside the one `FTA` event per missed date; HB2 orders in
  a defendant's other cases inside the 90 days; HB3 paper screens with no booking number (matched by state number).
- Stops (computed and asserted): S1 the appearance's case numbers only 246, 332, 311, 288, 73, 20 (3.6, 6.0, 9.2,
  14.6, 21.6, 26.0: 5 of 6 counts and 5 of 6 shares missed); S2 every case under the defendant's district party number
  253, 354, 354, 334, 93, 23 (3.7, 6.4, 10.5, 16.9, 27.5, 29.9: all 12 missed).
- Span: the court events, the case index, both first-appearance exports and the charges file, the screens, the jail
  export, the court code list, the current policy (1.4), the README (nine files).
- Realism: North Carolina's district and superior courts number a felony's file anew at indictment, and the superior
  court record carries the district file number.

**Ask C. For each new-criminal-activity score, the days on electronic monitoring to 30 September 2026 of every
defendant released at a first appearance from 1 October 2025 to 30 September 2026** (6 figures, nearest 10): 28,620,
26,820, 16,250, 10,380, 4,660 and 2,220 (unrounded 28,618, 26,818, 16,247, 10,382, 4,657, 2,220; each at least 0.2 of
its bin from an edge).
- H18 home: the monitoring each score's released defendants wear (a measure every release carries that the call does
  not turn on); use: the memo's account of the monitoring the county pays for at each score.
- Construction: the vendor's monthly invoice lines, each enrollment matched to its release (court case number, else
  name, date of birth and the latest release before the enrollment); each release's monitored days as the union of its
  enrollments, one per calendar day, to 30 September 2026; summed by NCA score. Golden equals the clean truth (asserted).
- Primary device (D1, the same records under two key schemes): an equipment change ends one enrollment and opens
  another under a new participant number the same day, and the vendor bills each enrollment a day or part of a day, so
  the change day is billed twice; every participant number is unique and no line repeats, so no duplicate check fires.
- Hazards: HC1 (D6) an enrollment open across months is on each month's invoice with its own enrollment date and no
  end until its last month; HC2 lines with no court case number (about one enrollment in eight); HC3 enrollments open
  at 30 September 2026.
- Stops (computed and asserted, each missing all 6): S1 billable days summed 29,370, 27,510, 16,660, 10,660, 4,790,
  2,280; S3 each enrollment counted on its own (the same figures: the change day twice); S2 each line's enrollment
  dates counted 182,160, 176,740, 100,710, 68,170, 31,880, 12,460.
- Span: the vendor's invoice lines, both first-appearance exports and the charges file, the screens, the jail export,
  the README (six files).
- Realism: monitoring vendors open a new enrollment for a replacement unit and bill per enrollment-day.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 UTC against Eastern midnights | the jail system's clock | Ask A | 20 to 80 bed-days a score (S4) |
| HA2, HA3 Halsey's day-or-part billing and month sheets | the boarding contract's invoice | Ask A | 30 to 400 a score (S3, S7) |
| HA4 annex moves | the detention center's housing sites | Ask A | every score, if each booking is ended at its first release |
| HB1 recalled and reissued orders | orders recalled and reissued | Ask B | none if counted per release |
| HB2 other cases' orders | defendants with older open cases | Ask B | 3 to 26 releases a score (S2) |
| HB3 paper screens | the screening system's outage entries | Asks B and C | releases dropped at every score if unmatched |
| HC1, HC3 month repeats and open enrollments | the vendor's invoice layout | Ask C | six times the days (S2) |
| HC2 lines with no case number | the vendor's intake form | Ask C | every score, if dropped |

**Referee.** None needed: no designed disagreement between two systems is arbitrated by a third file.

**The cracker sheet.** The cracker filed the golden tier, ran the hygiene battery (keys unique, exact duplicates, every
join matched or explained, no fan-out, counts that tie) and executed every filed rule. Every ask row misses:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 6 bed-day figures | jail stays from booking to release, Eastern midnights, annex moves chained, `BO` to the return booking, else read as the end of custody (S5) | about two in five boarded defendants were released at Halsey, their nights only on Halsey's bills | miss |
| Ask B, 6 counts | FTA events in the appearance's cases within 90 days, per release (S1) | indicted felonies continue under a superior court number found only through `district_case_ref` | miss |
| Ask B, 6 shares | the same over the releases | the same | miss |
| Ask C, 6 monitoring figures | each enrollment's days to its end or 30 September, summed per release (S3) | an equipment change opens a second enrollment the same day, so the change day counts twice | miss |

The tier and score 4's verdict belong to the recommendation block and are carried by the main call. The mirror sheet
(the same response stopped at R0) differs from the cracker sheet only on the recommendation criteria, so no ask is
coupled to the call.

Mirror leakage: 6 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 38 recommendation (the tier, score 4's verdict, the floor's comparison), 7
instruction following (the three files, the chart's title and axis), 55 asks over 30 figures and the chart's six bars.
The cracker keeps about 6 per cent of the ask weight: C = 38 + 7 + 3.3 = 48.3. The mirror (R0) keeps the released
score-4 rate it states and the same 3.3: S = 5 + 7 + 3.3 = 15.3. If the strongest response cracks the most obvious
device (Ask A's boarding, 6 of 36 ask criteria, about 9 of 55 points), C rises to about 57.5 and the pair to about 36.4.
Both top responses on the call with no device cracked: 48.3 each, under 50.

Pair ceiling: 36.4

Ask C cracked instead weighs the same as Ask A; Ask B with its chart is half the ask weight, so its device carries the
pair if a strong response finds the superior court continuation (pair about 46): it is the device to watch at the leak
read. Recomputed from the generated rubric when it exists.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| The draft revision, sections 2.1 to 2.5 | 1, the senior resident judge's draft local bail policy | eligibility, the tier's release on a written promise, the safety rate's population and window, the 85 per cent floor, the top score | how a score's rate is estimated, any magistrate, any held defendant's risk, any figure |
| The current local bail policy (2024) | 1 | the definitions the draft cites (1.4 a failure to appear), the conditions of release, the misdemeanor classes (the guideline bond table), that magistrates sit by the chief magistrate's rota (2.3) | any outcome, any tier |
| The scoring guide | 2 | the scale's items, points and the two six-point scores | any outcome rate |
| The README and code lists | 4 | each file's fields, the time zones, the detention definition (midnight count), the release at first appearance (within 24 hours on the conditions set, a secured bond posted in that time included; still in custody at 24 hours is held after it), the jail and court codes, the vendor's billing basis | anything about selection, a magistrate's release share, a boarding's billing or an indictment's renumbering beyond the codes' meaning |

## Prompt

`prompt.txt`, gated by `voice-check.py` (in `precut.py`): the call with its floor and the 2027 policy, the memo, the
workbook's three tables (bed-days in custody and monitoring days by NCA score; releases followed by a missed court date
on that appearance's charges, and their share, by failure-to-appear score), the chart, and the rounding once at the
close. 992 characters. Ask B counts releases (a defendant released twice in the period has two scores), and Ask A asks
for bed-days in custody, the custody a boarding at Halsey continues.

## Leak review

`leak.py task141 --asof 2026-10-14` on the built pack: REVIEW, no LEAK. Each REVIEW line answered:

- The draft revision carries 13 of 16 words of the committed call and sits "Pretrial Assessment Scale" beside "top
  score": it is the policy that defines the tier and its top score (2.2, 2.5) and names no score, rate or method; the
  answer (score 3) is nowhere in it.
- Stump-paragraph terms in the README (population, magistrates, arrests, disposition, export), the draft (magistrate,
  record, setting) and the 2024 policy (magistrates, record, disposition, setting): each is the files' own vocabulary
  (the jail's population count, the magistrate on duty, a case's disposition, the export's fields); none speaks of
  selection, a release share, a held defendant's risk or a gradient. The only sentences on assignment are the 2024
  policy's 2.3 (duty shifts by rota) and the roster's shift notes, which state how appearances are heard, not how a
  rate is estimated.

## Build record

Written at stage 3 green (figures from the final build):

- `python3 task141/generator/build.py`: the world, the pack (20 files, five formats, the state arrest extract at
  294,770 rows), the goldens, `figures.json` and `metadata.json`; `checks.py` 153 assertions, 0 failed (the three-rules block R1 to R3c on the clean truth and the pack, every rung by
  name and its margins, the 32-cell grid, SF1 to SF29, mess neutrality, the asks against the clean truth with every
  stop and each figure's bin distance, the separation line, the distractors, the input gates, the realism sweep); `verify.py` on its own path
  (the call, both tiers, every score's released and full-release rates, all 30 ask figures, figures.json and the golden
  workbook agree); a second full build byte-identical (target, golden, metadata.json, figures.json, target.zip).
- `target.zip` cut from the final build: 20 members, 28.5 MB, sha256 1bdba529a7b1acd5 (first 16 hex digits).
- `figures_check.py task141`: 61 figures in blocks 1 to 4, none absent. `precut.py task141`: 49 checks, exit 0.
  `voice-check.py task141`: PASS (992 characters).
- `guard.py surface task141`: 0 promoted pairs (nearest 0.101). `guard.py heart task141`: PASS (nearest 0.05).
- `scrub_producer_metadata.py` on target/ and golden/: clean. Realism sweep in `checks.py`: one export time on every
  file, no library banner in any container, no em dash, no repeated five-row block, personas from the card only.
- House fixes run: H16 (indictments returned after the extract kept out of the case index), H9 (the README lists every
  shipped file), H3 and H8 (the write-up's and memo's sentences against the figures and the draft's sections), H1.
- The call: scores 1 to 3 (score 4 at 75.8 per cent on the caseload-weighted line, under 80 on every construction;
  score 3 at 90.3). The default path: scores 1 to 4 (score 4 at 87.9 among the released).

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
- A first calibration of the selection at score 4 (the trait the magistrate sees on 30 per cent of score-4
  defendants, their new-offence rate 0.60 in the window): the lenient fifth of magistrates' own released defendants put
  score 4 at 86 per cent, on the default path's tier, and the weighted line sat a point from the floor in one draw; the
  trait's rate was raised to 0.80 at scores 4 to 6, so every construction of the gradient sits at least 4 points under
  the floor while the released defendants' rate stays near 88.
- Ask B counted defendants: a defendant released twice in the period carries two failure-to-appear scores, so the ask
  counts releases.
- One random stream per arrest keyed by the running count of every arrest: any change to one person's history moved
  every later person's draws, so the asks' year could not be set without moving the call; streams are keyed by person
  and the person's own arrest index, and the first appearances from 1 October 2025, the failures to appear and the
  monitoring each draw from their own stream.
