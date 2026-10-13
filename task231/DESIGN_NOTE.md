# task231 design note

The Brevland Central Bank's quarterly Business Conditions Survey (BCS), a panel of about 5,300 firms in twelve
regions. The September 2026 round's main fieldwork closes on Friday 25 September 2026; a region goes into the
two-week reminder-call extension (28 September to 9 October) when fewer than 55 per cent of its panel firms that were
still trading on the round's frame date, 1 September 2026, have returned the questionnaire.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task231.json`, architecture v1, drawn 2026-10-13. Survey Research &
  Official Statistics (client domain), task type `nonresponse-calibration-measurement-error-adjustment`, objective
  Data Quality Monitoring & Alerting. Shape 10 (each region's response rate checked against the 55 per cent line),
  decision `designation_set`, question form which. Gap time then population; no A to E pattern, decisive generator
  G12 (absence of a closure record is not a record of trading), then G11 (eligibility precondition). Gate G
  `forecasting`: the decisive figure is the share of this round's non-returners that the register will eventually
  show had already closed. Strategy `maturity_censoring`. Calibration `realised_outcome_roster` (the register's
  settled closures for earlier rounds). Stakeholder: the head of the business survey unit (`statistical_office_head`),
  deciding with her team (`line_manager_or_team`) at the close of main fieldwork (`period_close`).
- **Seed:** DQ04 (network-total shortfall alert with imputed missing reads), kept as an idea seed only: a network of
  reporting zones, a shortfall alert for the round being closed, a quantity completed for the units whose state is
  missing. The seed's Rubin's-rules pitfall is a reflex once implicates ship, and its GSD framing reads as a backdrop,
  so the pitfall is re-found in survey nonresponse: the missing state is whether a silent firm is still in scope.
- **Data-native sentence:** the business register learns of a closure only when the firm, its liquidator or the tax
  office notifies it, about a year after trading stops, and the call centre can confirm a closure only if someone
  still answers for the firm, so the round's non-returners hide closures that only the settled records of earlier
  rounds can count.
- **Guard:** `guard.py check` WARN only. `repeat.gate_g` (forecasting, against task229): the label repeats, the
  mechanism does not (task229 carries a convex rating curve's bias into 2027 months; task231 nowcasts the register's
  eventual closures among current non-returners). `repeat.question_form` (which, against task188): the call picks
  regions, so which is the form the decision takes. `test.same_puzzle_older` against task445 v1 is differentiated on
  the card (task445 completes amounts held by late reporters; task231 estimates membership of the denominator).
- **Sources, one line each.**
  - Client Layer 2 patterns for the task type (cells before calibration, raking to convergence, sensitivity and
    specificity of a classification): none is this build's step; it is the unresolved-eligibility estimate that
    AAPOR leaves to "the best available information".
  - Client measured drivers: the held tasks built an unfamiliar unit upstream of every graded figure; here the unit is
    the in-scope firm, and the construction is its scope at the frame date, not a replay of certified figures.
  - Family record: the maturity attack held where the graded object crystallised after the extract and the tail sat in
    a registry the natural pipeline never joins (73 world seven); task451 completes payments from the development in
    force and task255 truncates and censors a size distribution, neither estimates whether a unit belongs to the
    denominator.
- **Domain test:** the deciding quantity is the survey's response rate over in-scope panel firms with the eligibility
  of the unresolved non-respondents estimated, AAPOR's e, which the survey statistician takes from the register's
  settled closures of earlier rounds because nonresponse follow-up resolves closed firms far less often than trading
  ones. Swap in a meter fleet's read rate and there is no in-scope population fixed at a frame date by trading status,
  no follow-up whose resolution depends on the outcome and no e to estimate.

## Default path

1. Read the September 2026 invitation list (`bcs_invitations_2026q3.csv`: panel firms invited, by region) and the
   returns received by 17:00 on 25 September 2026 (`bcs_returns_2026q3.csv`), keeping one return per firm where a
   firm answered by web and by phone.
2. Join the invited firms to the business register's closure extract on company number (both the six-digit and the
   check-digit forms) and drop the firms whose recorded closure date is on or before 1 September 2026.
3. Take each region's response rate as its returns over the invited firms that remain.
4. Raise the alert where that rate is under 55 per cent.

Ends on: the alert for six regions, Capital, Harbour, North Coast, Islands, Border and Western Uplands.
Golden: the alert for two regions, Capital and Harbour.

## Stump sentence

The default path counts every non-returning firm without a business-register closure as still trading and sends six
regions into the extension (Capital, Harbour, North Coast, Islands, Border and Western Uplands); the register records a
closure about a year after trading stops, so most firms that closed before 1 September are not yet on it, and the
closure share of the round's non-returners, read from rounds old enough for the register to have recorded their
closures, leaves only Capital and Harbour under 55 per cent.

## Three rules

- Task type: `nonresponse-calibration-measurement-error-adjustment` (Survey Research & Official Statistics), which
  serves Data Quality Monitoring & Alerting.
- Domain test: the decisive quantity is each region's response rate over the panel firms still trading on 1 September
  2026, with the eligibility of the unresolved non-returners estimated (AAPOR's e for unknown-eligibility cases), the
  field's own estimator, here from the register's settled closures for earlier rounds.
- Swap: "which regions' meter read rate among connected meters falls below 98 per cent, with disconnections recorded
  late" keeps the arithmetic but loses the survey quantity: there is no in-scope population fixed by trading status at
  a frame date, no nonresponse follow-up whose success depends on the outcome, and no unresolved eligibility to
  estimate; the task stops being a survey-nonresponse question.
- Layer 1: closures carry a cessation date and a later registration date (the register's own process); company
  numbers changed format in 2021 and both forms circulate; the contact centre's outcome codes changed scheme in 2022;
  returns arrive by web, phone and post with cross-mode duplicates; round labels differ across files; timestamps are
  UTC against a local 17:00 close; a 2023 regional review recoded two regions. Each comes from the systems that make
  the files; none is placed to be caught, and none sits on the decisive path.
- Layer 2: `maturity_censoring` in the field-method family; the estimate of how many of this round's non-returners
  were still trading on 1 September decides which regions fall under 55 per cent.
- Decisive step: estimating the eligibility of the unresolved non-respondents from the settled outcomes of comparable
  earlier non-respondents (rounds old enough for the register to have recorded their closures), instead of treating
  the register as it stands as complete or carrying the call centre's resolved mix onto the unresolved.
- Not semantics: reading every field right (the two closure dates, both company-number forms, the outcome codes)
  still leaves the September non-returners' closures unrecorded; the register is read correctly and is simply not yet
  complete, so no reading fixes the denominator.
- Not rule application: the quality standard defines the response rate over firms trading on the frame date and
  leaves open how the trading status of a silent firm is established; no filed rule or procedure estimates it, so
  executing every stated rule still files the register-as-it-stands answer.
- Analyst test: a strong analyst who deduplicates the returns, drops the firms the register shows closed by
  1 September and divides each region's returns by the rest raises the alert in six regions (the default path's
  Ends on), and one who gives the unresolved non-returners the eligibility of the call centre's resolved cases still
  raises it in five, where only Capital and Harbour fall short.
- Estimand: the BCS quality standard (`BCS_fieldwork_quality_standard_v3.pdf`, section 4) defines the round's response
  rate as returns received by the main fieldwork close over the panel firms invited to the round that were trading on
  the round's frame date, and the alert as that rate under 55 per cent in a region; the frame date for September 2026
  is 1 September 2026 (the round calendar).
- No decoy: nothing is planted; the register's lag, the call centre's selective confirmations and the panel's
  history are the systems' own behaviour, no memo, draft or dashboard carries a wrong region list, and no artifact
  ranks the regions.
- No certified replay: no published or certified figure is reproduced to recover the method; the settled rounds are
  evidence for an estimate, not controls the method must match.
- Lesson: a response rate's denominator is a population fixed at a date, and when the register that defines it lags,
  the eligibility of silent units has to be estimated from cases whose fate has since become known, not taken from the
  record as it stands or from follow-up that reaches only the units still there; no build on file teaches the
  eligibility of non-respondents.

## Tried and rejected

- Seed pitfall kept (Rubin's rules over shipped implicates): a reflex for any strong solver once the implicates ship;
  rejected at the draw.
- GSD missing-data framing (meter reads imputed in a utility network): the deciding quantity reads the same in any
  field, the backdrop the author keeps getting returned; rejected at the draw.
- Product analytics SRM alert, psychometric reliability under a population change, consensual observer drift, SSI
  post-discharge ascertainment, AMR cascade testing, airport noise-monitor capture: each either read as a reflex (ramp
  SRM, a pilot alpha), split into competing defensible methods (CTT against IRT, drift indices), sat in a pairing the
  wave's epidemiology seeds need, or turned on a fleet mix (composition, banned in the window); rejected at the draw.
- Silence run as the decisive rung (closure share by rounds since the last return): prototype 2026-10-13 put the
  pooled and run-based estimates within 0.3 points of each other; the run is a corridor variant, not a rung.
- An insolvency wave to make the run decisive: the settled history stops transporting to the wave regions (the
  estimate misses the truth by about 5 points there); rejected.
