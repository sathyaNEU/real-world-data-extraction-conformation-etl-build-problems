# task156: a union branch, at which councils it applies for protected action ballot orders for March 2027 (architecture 3)

Private, never ships. Architecture 1 (Millrind's 2027 paid moderation pool) was returned FAILED_TO_STUMP on
2026-10-27 and re-rooted; architecture 2 (the Riverbank Road pump station's consented overflows) was returned
FAILED_TO_STUMP on 2026-11-07 with both responses on the hold call, because any full-record replay with the subdivision
already broke the consent. The slot is re-rooted again in a new domain: nothing of either architecture is carried
(world, decision, quantity, prompt shell, deliverables, asks and mechanism are all new), and both identities sit in the
card's `lineage` with their fates.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task156.json`, architecture v3, registered 2026-11-07 on a fresh pull of main; architectures 1 and 2 in `lineage`, their shells in `lineage_shells` |
| Domain / task type | `political-science-public-policy`, task type `election-polling-forecasting` (serves Forecasting): the deciding quantity is each council's expected turnout in a statutory ballot that is valid only if half the roll votes, forecast elector by elector the way turnout is forecast from vote history and calibrated on declared results |
| Objective | Forecasting & Predictive Modeling: turnout in ballots opening 1 March 2027, a window not yet open; the roll is fixed (members employed at each council on 15 January 2027), the outcome is whether half of it votes |
| Shape | `10` (scorecard against a threshold): every 2027 bargaining council carries an expected turnout and a side of the 50 per cent line, the call is the set of councils that clear it; asks on records the call never reads (arithmetic in `## Shape`) |
| Decision | `designation_set`, answer unit `set_of_items`: the councils at which the branch applies for protected action ballot orders in February 2027 |
| Mechanism | population: the members whose past votes the history records are not, at some councils, the electorate the 2027 ballot meets, because the delegate active at their worksite when they voted is no longer there or a new one is (pattern A, past exceedance against forward yield: the councils' past ballots cleared half, the forward yield at some does not); generators G14 (turnout conditioned on an active delegate at the member's worksite), G13 (the July 2026 delegate elections fall between the last online vote and the ballot), G4 (a member's past votes attributed to the member when part belongs to the delegate in post at the time); Gate G `forecasting`; strategy `forecast_method_backtest` (the vote-history model reproduces the last closed round and misses the next) |
| Layer 2 family / pattern | `forecast_uncertainty` (a forecast validated out of sample on the last round, whose precondition, the mobilisation the history embedded, fails in the forward window); `own:vote-history-turnout-carried-past-a-change-in-workplace-mobilisation` |
| Furniture | forum `board_of_directors` (the Branch Committee of Management, the branch's governing body, resolves which applications are lodged), forcing event `statutory_or_regulatory_filing` (the applications to the Fair Work Commission for protected action ballot orders, lodged in February 2027), organisation family `cooperative_or_member_body` (a registered trade union branch), role family `research_desk` (the branch's research and bargaining officer), context artifact `register` (the branch's delegate register), calibration `realised_outcome_roster` (the ballot agent's declared turnouts, which both routes reproduce), opening `question-first`, question form `which` |
| Spine | `online_vote_invitations_2022-2025.csv`, one row per invitation the branch's online voting service sent a member for one of its online votes (about 85,000 rows, UTC), beside the membership register, the delegate register, the worksite list and the ballot agent's declared results; constructed for this build, no real dataset |
| Deliverables | `pab_2027_turnout_forecast.xlsx` (the forecast and the asks), `pab_2027_recommendation_bcom.docx` (the memo to the Branch Committee of Management) |
| People | drawn with `guard.py names --geo australia --seed 156`: Samantha Taylor, Dennis Kim, Eric Goodwin (John Howard passed over, a former prime minister; Margaret Montgomery passed over, her first name already on task258) |

**Guard answers (registered card, `guard.py check` PASS on a fresh pull).** The first probe carried gap `time` with
pattern `E`, which BLOCKed as the same puzzle as task445 inside the batch and the same driver signature as eight older
builds; `time` with pattern `none` BLOCKed on task130's lineage (G14, then G13 and G4 as the decisive code). The
honest description is the population one: the electorate the forward ballot meets at the councils whose delegates
changed is not the electorate whose votes the history records, and the councils' past ballots cleared half while the
forward yield at some does not (pattern A). Forum, forcing event and organisation family are clear of the last three
builds (task232, task190, task456).

**The data-native sentence.** The branch's own online votes record who voted but not who was asked to by a delegate,
and the delegate register's elected terms, read against each member's worksite, are the only place the July 2026
delegate elections show; the history the forecast is carried on was all gathered under the delegates elected in 2020,
2022 and 2024.

## Shape

Shape 10, a scorecard against one threshold: the 24 councils in `bargaining_round_2027.xlsx` each carry an expected
turnout and a side of the 50 per cent line, and the call is the set on the right side. Criteria: the set (1), each
council's side (24), the councils whose side the decisive step moves named in the memo (8), the delegate lift and the
back-test as critical components (2); asks: each round council's 2025-26 dues (24) and organiser hours (24); the two
deliverables present (2). Well over 25, supplied by the answer's structure. The prompt names no count.

## Default path

1. Read `membership_register_extract_2026-11-02.csv`, place each member at their council (the worksite list maps the
   codes used before July 2024), and take each council's roll as the members employed on the extract.
2. Build each member's voting history from `online_vote_invitations_2022-2025.csv` (four online votes, 2022 to 2025).
3. Fit the field's vote-history turnout model: a logit of voting on vote, council, age, membership years and
   employment (or each member's own share of the votes they were asked to), and set it on the protected action
   ballots' level with the agent's declared 2021 and 2023-24 turnouts.
4. Back-test: the 2023-24 round, rebuilt from the online votes before it, lands within about 0.7 points of the
   declarations on average and within 3.5 points at every council.
5. Run the 2 November 2026 roll through the model; apply where the expected turnout is at least half (the guide's
   rule).

Ends on: 15 councils (Ardeen, Bellcourt, Corrigan Valley, Elmhurst Bay, Fairholme, Halston, Jerrick, Lindale, Marlow
Coast, Northvale, Rosedene, Stanwick, Tallis Creek, Valmont, Westhaven).
Golden: 11 councils (Ardeen, Copeland Downs, Corrigan Valley, Fairholme, Halston, Lindale, Northvale, Pellham,
Stanwick, Valmont, Westhaven).

## Stump sentence

Carrying each member's own voting history, calibrated to the 2021 and 2023-24 declared turnouts and checked on the
2023-24 round within a point, files 15 councils above half; the step that lands it there is reading each member's
past votes as theirs alone when they rode the elected delegate in post at their worksite at the time, and the July
2026 delegate elections left worksites at Bellcourt, Elmhurst Bay, Jerrick, Marlow Coast, Rosedene and Tallis Creek
without one and filled worksites at Copeland Downs and Pellham, so with the 2026-28 delegates the set is 11.

## Three rules

Task type: election-polling-forecasting (Political Science & Public Policy), which serves Forecasting: each council's turnout in a statutory ballot opening 1 March 2027, forecast elector by elector from vote history and set on declared results.
Domain test: the deciding quantity is each council's expected turnout against a participation threshold, worked the way turnout forecasting works it, a vote-history logit of each elector calibrated on declared results; the field's own mobilisation estimand (the lift personal contact gives turnout) carries the forecast once the contact network changes.
Swap: "megawatt-hours" for "ballots" or "patients" for "members" leaves no roll, no participation threshold under section 459 and no elected workplace delegate whose presence moves an elector's turnout; the call stops reading.
Layer 1: the membership system's July 2024 migration left leavers on the old worksite codes and employer names; the online votes are logged in UTC; the agent's two rounds use different declaration layouts inside PDFs; the delegate register keeps a term's delegates listed after they leave and carries the pre-2024 codes and council names for its older terms. Nothing is placed to be caught.
Layer 2: forecast_uncertainty: a forecast validated out of sample on the last round whose precondition, the mobilisation the history embedded, fails in the forward window; the choice that flips the call is conditioning each member's turnout on the delegate in post at the ballot, estimated from the online votes, rather than carrying the history.
Decisive step: recognising that a member's past participation was produced under the delegate then in post at their worksite, estimating the delegate lift from the online votes across the 2020, 2022 and 2024 terms, and running the 2027 roll with the delegates of the 2026-28 term still in post on the extract.
Not semantics: every field, code and date read correctly (worksite codes mapped, UTC handled, both declaration layouts parsed, leavers off the roll) still leaves the vote-history route on 15 councils; nothing in any file defines turnout by delegate presence or names the July 2026 elections as a change.
Not rule application: no filed rule or procedure says turnout depends on delegates; the guide files only the threshold, the roll and the window. Enumerated family: the vote-history logit, the member's own share, the last declared turnout, the fitted model with worksites carried at the 2024-26 delegates, the points shift, the residual-calibrated model, the listed-delegate variant, a level from one round: 11 to 15 councils. Standing family, once the July 2026 change is seen: every member of it files the same 11 (asserted, `checks.py`), the four cheap members 15, so the standing spread on the graded set is zero only after the step and the step is what decides; what rules the cheap members out is the change in the delegate register between terms, which no sentence points to.
Analyst test: a strong analyst who maps the codes, handles UTC, parses both layouts and reads the guide fits the vote-history model, confirms it rebuilds the 2023-24 round within 0.7 points, applies it to the 2 November 2026 roll and files 15 councils; six of those fall below half and two councils it leaves out clear it once the 2026-28 delegates are read in.
Estimand: `lsu_pab_guide_for_officials_2025.pdf` section 2 files the population (every member employed at the council on the round's register extract), the outcome (the share of that roll forecast to return a ballot), the window (the round's ballot period, opening 1 March 2027) and the comparison (at or above 50 per cent); the round is the "2027 round" sheet.
No decoy: nothing is planted: no memo, briefing, survey or stakeholder figure ranks the councils or argues a set; the member survey and the workforce returns are distractors that carry no turnout and no delegate figure; the delegate register is the organising coordinator's ordinary record.
No certified replay: the method is not hidden behind a certified figure to be reproduced; the declarations are realised outcomes the easy route reproduces too (the back-test), and the decisive step changes the forward window, not the fit to the declarations.
Lesson: a turnout model validated on the last round carries the organisation that produced its history; when the contact network moves between the last observation and the forecast window, the history must be re-read through the network, not carried; no build on file conditions an elector's turnout on a dated workplace contact.

## Survivor anatomy

Actor: members and worksites have rows, but whether an elected delegate was in post at a member's worksite on a vote's close is a relation between the register's dated terms, the member's worksite and the delegate's own membership dates: no column of any file holds it.
Link: the join is member to worksite (old codes through the worksite list) to the register's term for the vote's date, with the delegate checked against their own membership row; no shared key carries a delegate to an elector, and the field's vote-history method never asks for the comparison.
Reflex: the field's named method, a vote-history turnout logit calibrated on declared results (or each member's own share of past votes), sits at rung 1 and files 15 councils.
Back-test: the textbook route rebuilds the 2023-24 declarations within 0.7 points on average and 3.5 at worst (asserted), because the 2022 and 2024 delegates sat at much the same worksites; the validation record confirms the easy route.
Second use: the delegate register is the organising coordinator's term-by-term record and is what any solver reads to see who represents a worksite; the online votes are the vote-history route's own input; the declarations calibrate every route; the worksite list maps the 2024 code migration for the register itself. Deleting the decisive step drops no file.
Shock: the July 2026 elections' changes sit inside ordinary term-to-term churn (worksites gain and lose delegates every term); the golden set is not an interval of any shipped statistic (it holds Valmont at 36 per cent coverage and leaves out Darnley Plains at 82, and its turnouts run from 57 to 72 while Bellcourt's last declaration was 56).
Pins: the guide files the threshold, the roll, the window and the comparison; no sentence names delegates, mobilisation, the 2026 elections or any grouping; deleting any filed sentence leaves the decisive step where it was.

## Readability screen

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | 7 Organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0, the last declared turnout carried | no | yes, the declarations | yes, the record's own rate | the declarations tie | no | yes | no | readable |
| 1, the vote-history logit calibrated on the declarations | no | no | yes, the field's turnout model | the 2023-24 back-test passes | no | no | no | readable |
| 1', each member's own share of past votes, scaled | no | no | yes | the back-test passes | no | yes | no | readable |
| 2 (decisive), the delegate in post at the ballot, from the 2026-28 term | no sentence names it | no column holds it | not the field's default | no control scores it | the battery never builds it | not a ratio of shipped columns | the register is an ordinary record | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the roll | members employed on the 2 November 2026 extract | members expected still employed in March 2027 | same call | guide section 2, "on the membership register extract taken for the round" |
| SF2 | a delegate in post | elected for the term and still a member that day | every delegate the register lists for the term | same call | asserted in `checks.py` (SF2 variant) |
| SF3 | half the roll | at or above 50 per cent | strictly above | same call | no council within 3.5 points of half (asserted) |
| SF4 | turnout | ballot papers returned over the roll | formal votes over the roll | same call | section 459 counts employees who vote; asserted (SF4 variant) |
| SF5 | a member's worksite | the register's code, old codes mapped through the worksite list | leavers dropped where the code is old | same call | the worksite list's own column; leavers carry no 2027 weight |
| SF6 | a vote cast | any row with a vote time | votes inside the local window only | same call and figure | every vote time falls inside its window (asserted) |
| SF7 | the ballots' level | one shift over both rounds' declarations | the 2023-24 round alone | same call | asserted (SF7 variant) |
| SF8 | the round | the 24 councils on the "2027 round" sheet | every council with a past ballot | same call on the round | the tracker's sheet; the guide's "councils in the round" |

## Ladder

| Rung | Pipeline | Set | Golden's 11 kept | Others |
|---|---|---|---|---|
| 0 | last declared turnout carried, the model where a council has none | 15 | 9 | 6 |
| 1 | vote-history logit, no delegate term | 15 | 9 | 6 |
| 1' | each member's own share of the online votes, scaled to the 2023-24 ballots | 15 | 9 | 6 |
| 1'' | delegate term fitted, worksites carried at the 2024-26 delegates | 15 | 9 | 6 |
| 2 | the delegate in post at the ballot (2026-28 term) | 11 | 11 | 0 |

The margin, argued on paper and asserted on the cut pack: every council sits at least 3.5 points from half on the
golden (nearest Rosedene and Bellcourt) and at least 3 points under the 2024-26 delegates; the cheap rungs agree with
one another on one wrong set, so the strong solvers' easy route is the one designed, and no cheap rung reaches the
golden by a different road (Gate F counted: 0 of 4). The lift is large and measured tightly (log odds 1.05, standard
error 0.02; about 24 points at the 2027 rolls), so every member of the standing family files the same 11.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | members employed at each round council on the 2 November 2026 extract | guide section 2 |
| 2 Unit of account | a member returning a ballot | section 459; the declarations' count |
| 3 Attribution window | the ballot opening 1 March 2027 | prompt and guide |
| 4 As-of dating | the extract of 2 November 2026; delegates in post on it | guide section 2; the register's terms |
| 5 Version basis | the agent's final declarations | the two PDFs carry only declarations |
| 6 Denominator | the roll | section 459 |
| 7 Weighting | none: every member counts once | not applicable |
| 8 Window length | four online votes, two ballot rounds | the shipped record |
| 9 Boundary inclusivity | at or above half | no council within 3.5 points (asserted) |
| 10 Rounding path | turnout unrounded against half, reported whole | the side is graded; edges cleared |
| 11 Tie-break | none | not applicable |
| 12 Maturity and censoring | members who joined after the last vote carry no history | the model's covariates carry them |
| 13 Order of operations | worksite, delegate mark, model, level, roll | construction |
| 14 Row order | none | not applicable |
| 15 Duplicate resolution | one invitation per member per vote | the log's own key |
| 16 Identity normalisation | old worksite codes and employer names | the worksite list |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | shares of the roll | the declarations' counts |
| 19 Code and status semantics | a delegate still a member | the register against membership dates (SF2) |
| 20 Integerisation | none on the call | not applicable |
| 21 Clause scope | the guide's rule applies to every council in the round | guide section 2 |
| 22 Forward window contents | the 2026-28 delegates and the extract | shipped |

## Literal reader

Executed word for word, the guide forecasts the share of each council's 2 November 2026 roll returning a ballot in the
March 2027 ballot and applies at or above half; the literal reading leaves the forecast's method open, the data force
it (the history's precondition fails in the window), and every member of the standing family files the golden 11.

## Oracles

`generator/estim.py` (the golden and the four cheap rungs, from target/ alone), `generator/verify.py` (an independent
GLM through formulas, pdfplumber for the declarations and the bureau, pandas for the asks, imports nothing from the
generator), `generator/checks.py` (35 assertions on the clean truth and the cut pack, Gate F counted).

## Ask sheet

The call's population is the membership register, the online vote log, the delegate register, the worksite list, the
declarations and the round tracker. Every ask reads other rows: Ask A the councils' payroll remittance advices and
the bureau's statements; Ask B the organisers' diary export and the forum sign-ins (placed through the register,
which carries no device row). Zero device or hazard rows sit in the call's population.

**Ask A, dues each round council's payroll deducted for the branch for pay periods ending in 2025-26 (24 figures,
whole dollars).** H18: the branch's income from each council, which industrial action puts at risk. Construction: pay
periods ending 1 July 2025 to 30 June 2026; finance procedure FP-04 files the convention (every council pays
fortnightly in arrears, a pay period ends on a Sunday, a deduction is credited to the year its period ends in).
Primary: the twelve round councils on the regional payroll platform from January 2026 date each run by its pay day,
four days after the Sunday period end, so the run ending 28 June 2026 appears as 2 July and the date as carried drops
it: twelve figures miss by one run each. No sentence names the platform, a weekday or which advices are dated how;
only the weekday pattern in the advices shows it. Second: the bureau's three clients sit in
one payment per run, split only by its statements. Hazard: an advice re-sent with its own number. Pin test: the asking
sentence files the window by pay period, not which column carries it.

**Ask B, organiser hours at each round council in 2025-26 (24 figures, whole hours).** H18: where organising time went in
the year the delegates were re-elected. Construction: travel and administration out; the asking sentence files the unit
(a visit two organisers made counts for both, a moved booking once as held) and a regional forum's hours shared by
the sign-ins from each council. Primary: one diary event is one organiser on one invitation on one day; a
rescheduled booking leaves its superseded row (same organiser, invitation and day, earlier update), and about one
visit in nine is made by two organisers on one invitation, so keeping one row per invitation and day drops the
second organiser and keeping every row counts the superseded bookings: all 24 figures move either way. No field
marks a moved booking; only the repeat of one organiser, invitation and day with an earlier update shows it. Hazard:
weekly delegates' meetings share one invitation across weeks.

| Ask | Figures | Cracker path (lands the call, runs the battery, executes every filed rule) | Cracker keeps | Verdict |
|---|---|---|---|---|
| A, dues 2025-26 | 24 | one copy of each advice, the bureau split by its statements, each run by the date the advice carries | 12 of 24 | miss |
| B, organiser hours 2025-26 | 24 | travel and administration out, every organiser's rows counted, forums by sign-ins, no moved booking found | 0 of 24 | miss |

| Ask | Mirror (the vote-history set, same ask handling) | Mirror keeps |
|---|---|---|
| A | as the cracker | 12 of 24 |
| B | as the cracker | 0 of 24 |

Pair ceiling: 42.2 (one response on the call and one off it, both handling the asks the cracker's way).
Mirror leakage: 25.0 per cent of the ask weight.
Measured by: generator/ceiling.py (on the cut pack: the cracker keeps 12 of 48 ask figures; the full includer, a stress row, keeps all 48).

## Gates at stage 3

- `checks.py`: 39 assertions, 0 failed; `verify.py`: 0 disagreements; two consecutive builds byte-identical (target,
  golden, figures.json, submission.md); `figures_check.py` PASS (88 figures); `precut.py` 61 checks, 0 FAIL, 0 WARN;
  `voice-check.py` PASS (827 characters); `guard.py heart` PASS after a final fetch; `surface` promotes no pair.
- `leak.py` REVIEW, no LEAK, each line ruled: the answer-figure lines are small counts that coincide (a yes count in a
  2021 declaration, member counts in the bureau's statements), not golden figures in context; the call's council names
  appear in every file because every file is about those councils, and none ranks them on the 2027 question (the
  declarations are past realised turnouts, the easy route's own input and a past fact, never a forecast); the three
  stump-paragraph words in the 2023-24 declarations are "carried", "question" and "declarations", the agent's own
  ordinary wording; the dates after the setting are the agreements' nominal expiry dates in the round tracker and the
  2026-28 term's end date in the delegate register, both future by nature. After round 1: the tracker's and the
  survey's 'Notes' sheets are the organisation's own notes (the round's lodgement and ballot period; the survey's
  fieldwork dates), describing no column or file; FP-04's three stump-paragraph words are 'register', 'member' and
  'record' in finance's ordinary sense (the remittance register), naming no move.
- The PDFs are Writer exports (officepdf), Author the issuing organisation, a real Subject; the workbooks carry their
  owners' names and Excel's own dialect; no programming library appears in any container.

## Tried and rejected

- A mix shift by author tenure (new accounts' posts carry most review items, and AI took the newcomers): rejected at the
  draw, because the account-age column makes the segmentation a reflex the opponent runs on every visible attribute.
- Spam and flags scaling with page views rather than questions: rejected at the draw, because a per-queue trend of the
  flags already follows views, so the reflex lands, and the swap test reads it as generic demand forecasting.
- A volunteer pool with two retention types (veterans and casual reviewers) as a rung: dropped at the prototype, because
  the defensible retention estimators (tenure bands, pooled recent churn, a heterogeneity fit) split the per-site
  figures by up to 0.8 FTE; every site's pool now leaves at one steady rate since the pipeline dried up.
- Item and flag rates per question stepping up in 2023: dropped at the prototype, because a pooled ratio (over the
  step) and a reviewer trend over 2024 carry errors of opposite sign that cancel near the golden; both rates hold steady.
- Sizing the pool on the busiest 2027 month (shape 02): dropped at the prototype, because each late-2027 month's network
  hours carry about 300 hours of one-sigma spread, too wide for a monthly grid at any natural rounding.
- A volunteer pace with a wide spread across reviewers (KAPPA_SIG 0.60): the 2021 to 2023 and 2024 to 2026 saturated
  paces differed by 3.6 per cent, which moved Data & ML across its bin between eras; reviewers' own paces now spread at
  0.15.
- A Poisson trickle of new reviewers after the pipeline dried up: carried or dropped, it moved two sites by 0.4 FTE; the
  trickle is now a floor share (0.004) of the old inflow, and no construction moves a site.
- Pre-platform reviewers' grant dates drawn freely: they piled up at January 2013; tenure is now bounded by each site's
  launch on the register.
- Cover targets calibrated against random-walk inflows and exits: the calibration moved the wrong way; exits and inflow
  are now constructed (zero-sum swings within each quarter), and the January to September 2026 cover targets of
  Databases and Embedded & Hardware were set at 1.137 and 0.76 to centre their needs in their bins.
- Question moves drawn by source site: they ran the wrong way and reached 90,000 rows; moves are drawn into each
  destination at 0.55 of the first shares (49,530 rows).
- October to December 2026 on the chart with no question driver: a trend of each site's questions would be an open
  fork; the plan workbook carries the planning team's outlook sheet for those months, used only for the chart.
- WFM shifts of 7.5 paid hours: half the quarter totals ended on a half hour, a rounding fork at the nearest hour;
  shifts are now 8 paid hours, short days, overtime and corrections in whole hours.
- First actions on flags with an unbounded lognormal tail: some ran past the moderator tool's export run, dating rows
  after the as-of; a flag left past 90 hours is now escalated and taken within the next week of hours (no Ask A figure
  moves), and a review still open at the export keeps its first action as the handled time.
- The network first named Quernstone: a UK accounting firm carries that exact name (Companies House 04197485); the
  network is now Millrind (no company, network or software of that name found).
- Ask C's stop "each move applied in the month it moved": it files the golden's nine (no move straddles the window's
  edges enough to cross a rounding step), so it is recorded as a convergence, not a stop; Ask A's over-correction stop
  (reviewed flags dropped) misses 14 of 27, not 27.
- target.zip cut with a `target/` folder inside: the archive now carries the files at its root (house fix H4).
- Round 1, Ask C's device left silent (no file said how the old statistics job counted a moved question): the judge
  licensed three readings one decimal apart at every site (FIX_NOW). The warehouse notes now file the old job's counting
  and the comparison basis in the data team's voice; both other readings are asserted out. The device is no longer
  silent, so the cracker and the mirror both land Ask C (cracker sheet `hit`).
- Round 1, slide 2's series undefined (hours worked or need hours, flags in or out, which close standard, how October
  to December 2026 is counted): the operations notes now define paid review hours once, the prompt asks each year's
  actual hours totalled, and the three actual totals are graded and asserted (36,419, 36,233 and 29,626 hours); being
  construction figures, both top responses land them (cracker sheet `hit`). With Ask C, the pair ceiling moves from
  31.0 to about 41.0, over the 40 build target and under the 50 bar; precut fails its pair-ceiling and cracker rows on
  this alone, reported to the coordinator.
- Round 1, the roster missed the reviewers whose access lapsed in January or February 2024 without a platform review
  (its dictionary scope said every reviewer with access since 1 January 2024): a lapse rate read by lapse date then
  counted zero lapses in those months (1.92 per cent, 33). The 689 rows are now in the roster (first review blank), the
  dictionary's scope and lapse rule carry a worked example, and the lapse-date reading files the same nine.
- Round 1, the items no volunteer ever picks up drawn at one share for every item type: routed shares were identical
  across types in slack months, which read synthetic. Each type now has its own (close votes 0.91, low quality 0.72,
  edits 0.40, first posts 0.35 per cent); no graded figure moved. In saturated months the shares stay close across types
  because the 72-hour hand-off takes the oldest items first whatever their type; a per-type volunteer preference would
  change the routed mix that prices the frozen call, so it was not added.
- Round 1, the 24-hour share's denominator and the envelope's sign: the flag service standard now defines flag
  response as a share with the post-deleted closures out of both counts, the prompt names the measure (24-hour flag
  response), and the prompt asks how far above or below the envelope the request sits.
- Round 1, the question plan's 2026 actuals sheet stamped as pulled 8 October inside a workbook issued 18 September:
  the sheet now carries January to August 2026 as pulled on 14 September (no figure reads it).
- Round 2, Ask C held only less careful solvers once round 1 filed the old job's counting (the cracker landed it, precut
  failed): the 2022 sheet now carries the tag-sync undercount of May to August 2022 as first reported, with the
  statistics job's March 2023 restatement below its notes (sites down, months across); the careful-but-literal path
  misses all nine (nearest 0.27 points) and the golden's nine figures are unchanged.
- Round 2, the chart's three actual yearly totals (round 1): construction figures both top responses land; out of the
  prompt and the deliverable answers. The chart is graded on its content, its series filed in the operations notes and
  its months on the workbook's Monthly hours sheet. The pair ceiling is back to 31.4.
- Loop 3 (2026-10-27), the portal landed the call: both responses filed 35 FTE (the then golden) by building capacity
  against the inbox at the saturated pace and carrying each pool at its own lapse rate; the capacity framing was every
  strong solver's default, so it is now the default path and the decisive step moved to how the pool is carried.
- Two retention types with the pipeline drying in late 2024 or summer 2025: a trend of the network's lapse rate,
  extrapolated, landed the golden by coincidence (the closed pool's decline was already plain in the record); review
  access now closes on 1 September 2026, so the record shows only an open pool's flat rate.
- Grants following the question level squared (older pools at the sites AI hit hardest): the separations shrank and the
  trended-rate routes still tracked the golden; grants now follow the question level.
- Grants drying in January 2026 with the last twelve months' grants carried on: the two errors cancelled on the golden;
  with invitation-only access filed, no window of past grants is a reading of 2027.
- Invitations at 2 per cent of the old flow: carrying or dropping them moved a site by 0.44 FTE in all; invitations
  are now a handful a year and none fell in September.
- Covers calibrated by re-drawing the whole pool at each step: a site's need jumped by up to a whole FTE between
  iterations; each reviewer now draws from their own stream and each month's grants from a fixed quantile, so a cover
  change only adds or removes reviewers at the margin.
- The data dictionary, the file list, the operations notes and the warehouse notes (markdown): a file that describes the
  data is a leak (`dataset-generation` section 3); the conventions the asks and the chart need now sit in the operations
  handbook and the question count standard, and every export names its own columns.
- Annual netting at Databases and Infrastructure & DevOps 0.07 and 0.12 FTE from their bin edges, and the world's
  realised 2027 one bin lower at Data & ML (the 72-hour queue carries a short month's backlog into the next month's
  spare capacity): the three sites were re-centred slightly above their integers, and a day-by-day simulation of the
  hand-off on the forecast pool is asserted to file the same nine.
- Architecture 1 as a whole (2026-10-31, the batch 1 triage): the moderation pool's world, prompt and asks had been
  solved once on the portal and loop 3 kept them, so the slot is re-rooted in a new world with a new mechanism; the
  pool's leaving rate falling as fast leavers go first is spent for this slot.
- Re-root draw screens (2026-10-31), each rejected before any data was cut: a mixed-population flood frequency (spent
  in task273 and task130's notes); an event-driven trial's event count (task171 and task174 hold it); a dialysis
  cohort's eGFR slopes (a patient-level slope is the obvious route and the method forks); a vineyard's frost nights
  under inversions (dead in task170's notes); a health system's access change and a climate-extremes count (both
  measured dead in task174 and task170's notes); this slot's own frailty and tenure hazard (architecture 1).
- The first card probe for this draw carried `validated_decoy` true and Gap 1 first: BLOCKed on
  `two_layer.validated_decoy` (a closed record built to bless the wrong method) and on a structural signature spent in
  five builds. The design is drawn so the meter's own high-water-table storms and the overflow log refute one response
  per millimetre for anyone who checks them, and population (the meter's days are not the replay's) is the decisive gap.
- A June 2025 high river with storms in it (the spell centred in August): the meter logged three overflows in it that one
  response per millimetre misses, so the overflow log refuted the stop rung at the count level, a search signal; the spell
  now falls in a dry month of 2025 and the meter's logged overflows are dry-ground storms every rung reproduces.
- The spell's peak held below the replay's wettest days (12.6 km of sewer below the water table against 20): 812 replay
  days sat above anything the meter saw, so the deciding configuration was out of sample and the infiltration had to be
  extrapolated; the spell now reaches the replay's wettest days (one replay day above the meter's maximum).
- Pumps below the wet-winter base (92 to 100 L/s): the station spilled in dry weather on groundwater alone and the
  consent's 24-hour rule merged wet weeks into single long overflows, so more inflow could file fewer overflows and the
  count was not monotone in the flow; the pumps now sit above the wettest dry-weather peak and every overflow needs rain.
- Assumed unit hydrograph shapes and a crown or centreline reference for the submerged length: the replay spread 2.1 to
  5.0 a year, but only because those variants fit the meter two to three times worse; among fits within a few per cent of
  the best the figures agree inside the whole-number bin, so the figures are graded to whole overflows a year.
- Architecture 2 (the PS03 overflow replay with each day's own water table), returned FAILED_TO_STUMP on 2026-11-07:
  both responses landed the hold call. Response 1 replayed 2004 to 2023 and filed 48 overflows against the 40 the
  consent allows, then 2 after the upgrade; Response 2 filed the same hold. Any full-record replay with the subdivision
  already broke the consent, so the decisive step (each replay day's own water table) was never needed. Lesson: the easy
  route has to be the one strong solvers actually file, and it has to land on the wrong side; a count of rare
  exceedances spreads with every modelling choice, so the call now sits on a mean quantity whose naive family is tight.
- Judge round 1 (2026-11-07, FIX_NOW on the asks; the call forced, Gate G analytical_non_defect, Gate H pass). Ask A's
  window read literally dropped the platform councils' last run (a 2 July 2026 date in the period-end column): FP-04 now
  files the record's own convention (a pay period ends on a Sunday and is paid later that week; credited to the year it
  ends in), naming no platform and no weekday the advices carry. Ask B's unit was open (raw, per invitation and day, or
  per organiser, invitation and day): the asking sentence now files it (a visit two organisers made counts for both, a
  moved booking once as held). Both asks were scoped to the 30 councils the branch covers while the prompt read as the
  round: cut to the round's 24, the regional platform's twelve councils re-sited inside the round on the same pay
  cycles, so no in-round figure moved. Ask 1's turnout figures had no rounding and a refit evaluating members at the
  extract sat about 0.7 points under: the guide now files each member as they will stand when the ballot period closes
  and the tracker files that period (1 to 15 March 2027); whole-per-cent figures were not adopted because five councils
  sit within 0.05 of a half point (Corrigan Valley 62.53, Halston 59.53, Pellham 58.49, Rosedene 45.51, Underhill 40.54),
  so a worksite-effects refit (lift 1.027) can cross a rounding edge; the prompt asks only whether each council reaches
  half, the side being determinate under every refit. freeze.py: the main side unmoved; the twelve out-of-round ask
  figures and block 4's turnout percentages were dropped by the repair (allowed, this line).
- Hardening noted, not applied (the judge rated stump power moderate to good: a model that fits the delegate term lands
  the call): ship the 2026-28 term as the organising coordinator's separate July 2026 election return rather than a
  sheet of the delegate register, so the register a solver opens holds the terms the online votes cover and the new
  term sits in a file read for its own purpose; the call, the stump and every figure would stay frozen.
