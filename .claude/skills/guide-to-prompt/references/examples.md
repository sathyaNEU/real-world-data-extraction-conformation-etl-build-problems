# The best prompts on file

Three prompts under 1,000 characters whose main call held a strong model on the portal or in the client's own runs,
each asking for what a professional in the field would actually hand over. Quoted verbatim. They are idea seeds:
take the moves, never the scenario, entity, metric, file name or wording.

## 1. task133: the ECL allowance (Banking, Credit & Financial Risk, Forecasting, shape 02 with two grids)

> What collective expected credit loss allowance should we book on our PL36 and PL60 loans at 30 September 2026, built the way CRM-ECL-04 sets out with this quarter's approved scenarios? Put it with its stage 1 and stage 2 amounts in ecl_allowance_2026Q3.xlsx. Our LGDs will be set against what the loans that defaulted in 2023-24 have actually lost as a share of their balance at default, so add that to the workbook by product and quarter. I also need two slides in board_ecl_q3_2026.pptx. The first states the allowance. The second charts where each product's stage 1 and stage 2 loans at 30 June stood at 30 September, giving for each of those four groups the number in each stage and the number closed. Give the allowance and its stage amounts in Australian dollars to the nearest thousand and the loss shares in per cent to one decimal.

841 characters, `voice-check.py` PASS.
- **Call:** one AUD figure, booked for a forward window (each loan's next 12 months or remaining life).
- **Asks:** the stage 1 and 2 split; realised loss share by product and quarter (8 cells); the June book's stages at
  30 September (16 cells). Each is a credit-risk team's real quarter-end output.
- **Stump:** the model team's PD curve is the crude default share of every loan drawn, early repayers included. The
  textbook conditional PD divides by survival to date, 1 - C(a); the right divisor also removes loans repaid in
  full, 1 - C(a) - Cl(a), read from the development sample. No sentence in the pack says divide or condition.
- **Measured:** v1 (same call wording, different asks): one model stumped, the other landed AUD 13,773,000 at 100
  per cent by dividing by 1 - C(a), and every ask fell with it because each was an output of the call's
  construction. Loop 1 made that division a wrong rung and replaced the asks with two the call never reads.
- **Why the wording works:** the question is the call with its unit and as-of date; the method is named only as
  "the way the policy sets out", so the conditioning step stays the analyst's; the one motive ("our LGDs will be set
  against") is the only reason given; rounding once, at the close.

## 2. task181: the pertussis response area (Epidemiology & Public Health, Anomaly Detection, shape 17)

> Pertussis has been climbing across the district since August, and Janice Barker's response team works one local government area a week. Our pertussis response protocol, PR-07, says which area that is, and Monday's huddle, by phone this Labour Day, settles it off this morning's line-list extract. The call is one area.
>
> The huddle reads one slide, `response_team_brief.pptx`. It names the area the team goes to, then lists the schools in that area that the protocol counts as clusters this week, each with its number of cases.
>
> For the quarterly report, `pertussis_cases_by_lga.csv` has one row per area for 1 January to 31 August 2026: confirmed cases, probable cases, infants under six months, how many of those infants were admitted to hospital, and how many were born to a mother vaccinated against pertussis at least two weeks before the birth.

850 characters, written before the `prompt.txt` rules: today's gate fails it on the persona, the backticks, the
line breaks and the missing lead question. Fix those; keep everything else.
- **Call:** one area for this week's team, against the protocol's excess over expected.
- **Asks:** the slide's clusters in the chosen area; a 10-area by 5-measure CSV (50 cells) on a closed window the
  call never reads.
- **Stump:** counting specimens notified so far as specimens collected. One area's swabs go by courier to a Sydney
  laboratory and notify a week and a half late, so its last fortnight is several times what has arrived; the
  largest excess on file (Wagga Wagga) is the wrong area, and a pooled-delay nowcast still lands there. Only a
  nowcast by laboratory route, from the line list's own fill-in history, sends the team to Griffith.
- **Measured:** portal round 1, stump pass and determinism pass: the call, the fortnight figures and the slide
  failed (48 points); the CSV passed whole (42 points), so the score was 52. The asks gave way because each device
  was a stated rule or a hygiene step. The ask-only revision put silent devices on the CSV's rows; the prompt and
  the call stayed byte-identical.
- **Why the wording works:** the forcing fact (this morning's extract, a holiday Monday) bounds the computation; the
  protocol is named, its method is not; the call is four words ("The call is one area"); the CSV is a routine
  report a surveillance unit files every quarter.

## 3. Client exemplar: the go-to-market pod (Product Analytics, pick one of three, mean 0.47 over 4 runs)

> I run product analytics at Shiftline, the workforce-operations platform law-enforcement agencies use to schedule and manage their personnel, licensed per active seat. Our FY26 plan funds exactly one new-vertical sales pod, and leadership locks the vertical this week: County Sheriffs, State Agencies, or Campus Safety. Recommend which vertical gets the pod, one committed call, no splits.

388 characters (opens on a role and names no file: the client's older format; our gate fails both).
- **Call:** County Sheriffs, at 142,288 serviceable seats against State 117,850.
- **Stump:** the unit of analysis. The pod docket's universe keeps agencies with sworn officers above zero, which
  drops 700 county detention authorities that staff only civilians (133,517 people who work rostered shifts); a
  module closure looks like it kills their seats, while billing shows them migrating intact. Every run found the
  700 and still kept the docket's universe, so State won.
- **Why the wording works:** one decision, the candidate set named, "no splits" forbids hedging, and the forcing
  fact (one pod, locked this week) is the only context. The prompt never says what a market is: the analyst has
  to define who can be sold a seat, which is the analysis.

## What the three share

- The question is the committed call, with its unit and its date or window, in the first sentence or two.
- Every ask is a document the business really uses (a booked figure with its split, a board slide, a routine
  quarterly report), and the asks that held sit on rows the call never reads.
- The prompt names the standard or the decision, never the method, the trap word or the deciding file.
- The context is one forcing fact, not a backstory. Rounding is stated once, at the close.
- The stump is a step a careful analyst takes by default after reading every rule correctly: a divisor, a reporting
  delay, a universe definition. It is never a planted defect, a field reading or a rule to apply.
