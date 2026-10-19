# task249 design note

## Draw

Card `cards/task249.json`, architecture 3 (v1 and v2 in lineage), re-rooted 2026-10-19 at the author's request: a
fresh draw in another client domain whose task type serves Data Quality Monitoring, new world and new decisive step.
The re-root also clears architecture 2's pairing override against task247. Verdict: WARN, no BLOCK. Each WARN,
answered: overuse.objective (Data Quality Monitoring in 4 of the last 12): the lane is Data Quality Monitoring &
Alerting. repeat.question_form (which, after task268): the call is a set of client accounts, and a set asks which.
The similarity notes are differentiated in the card: test.same_puzzle_older against task236, task453 (v1) and task463,
test.same_driver_older against task168, test.own_lineage against v2 (same labels, a different decisive rung: v1 and v2
read a sensor's gain against distant references, v3 has no sensor and no gain). The nearest driver is task242 at 0.06;
task130's v3 (lineage, 0.05) carried a group chosen on a noisy outcome forward and was landed in four minutes because
its record held a cohort chosen the same way a period earlier; this pack holds no selected cohort with a second
reading (one sitting per candidate per season, and the verification check is new in 2029).

- **Pairing.** Psychology & Behavioral Science / psychometric-measurement-scale-validation, a task type serving Data
  Quality Monitoring. The object is the health of a new integrity check in the results pipeline, the proctored
  verification test an assessment firm adds at its clients' 2029 selection days, judged on how often it will refer
  genuine candidates; the call is a monitoring decision: which client accounts get the extended verification before
  the 2029 campus season opens.
- **The seed.** DQ22 gave only the objective (which monitored units fail a quality tolerance before the next round);
  its world and its pitfall are not carried.
- **Niche.** An industrial-organisational psychology firm in India runs a common online aptitude test: a 16-item
  adaptive reasoning test, unproctored, sat once per candidate per season, the result shared with every client
  employer the candidate applies to. Each client account shortlists its own applicants on the score. After the 2028
  season's impersonation cases (a friend or a paid proxy sitting the online test), the firm adds a 12-item proctored
  adaptive verification test, from a separate secure bank, at every account's 2029 selection days. The integrity
  standard refers a candidate for investigation when the online score lies above the upper limit of the verification
  score's 90 per cent band, and caps the genuine candidates an account's check may refer in a season.
- **The call.** Which client accounts' verification checks will refer more than one genuine shortlisted candidate in
  eight in the 2029 season, on their 2029 plans (shortlist size against expected applicants, selection-day timing);
  those accounts move to the 24-item extended verification before the season opens.
- **Shape.** 10, a scorecard: each of the 28 accounts' genuine referral rate against the cap, the list, the count, and
  the asks; over 25 criteria. Decision designation_set, answer set_of_items, question form which.
- **Strategy.** causal_design (regression to the mean among candidates chosen on the noisy score the check verifies,
  with a retest gain as the second component). G16 decisive (which construction of the shortlisted candidates' honest
  shortfall), G17 supporting; gap population (the study's volunteers were not shortlisted) and time (the 2029 season);
  Gate G forecasting (a correctly read study does not pin the shortlisted pool's rate); calibration
  gold_standard_subsample (the equivalence study's supervised pairs, genuine by design and unselected); context artifact
  filed_standard (the integrity standard); Layer 2 family estimand_identification, pattern
  own:false-referral-rate-of-a-verification-check-among-candidates-shortlisted-on-the-score-it-verifies.
- **Forum, event, organisation.** customer_or_counterparty (the client accounts are told which get the extended
  verification), season_or_peak (the 2029 campus season), professional_services (an assessment firm). Role
  compliance_or_audit (the head of assessment integrity).
- **People** (`guard.py names --geo india --seed 249`, locale en_IN): Vasudha Padmanabhan, head of assessment integrity,
  who asks; Abhiram Sarin, the firm's psychometrician, who ran the equivalence study; Rachita Sunder, client services;
  Nachiket Sarna, selection-day operations; Ishwar Tella, platform data engineer. None appears in the prompt.
- **Data-native sentence.** A candidate is shortlisted because the online score is high, and an adaptive test's
  score is ability plus error, so the shortlisted are the candidates whose error ran upward; the deeper an account
  shortlists the more the chosen scores overstate ability, and the more so where the item bank thins and the online
  test's standard error grows, so a verification test taken by the same people falls short of their online scores
  for no reason but the choosing, while the gain a second sitting brings, largest when it follows within days, pulls
  the other way.
- **As-of.** Monday 14 May 2029, after the accounts' 2029 plans (due 30 April) and before the season opens on 1 July.
- **Sources.** The client's two-layer standard (estimand_identification: regression to the mean, selection on the
  outcome); the psychometric practice of unproctored internet testing with proctored verification (the ITC guidelines
  on computer-based and internet-delivered testing); true-score regression (Kelley) and the conditional standard error
  of an adaptive test; the retest gain of cognitive ability tests and its fading with the interval (Hausknecht and
  colleagues' meta-analysis). No build on file reads a verification check's false-referral rate among units selected
  on the score it verifies (nearest drivers 0.06 and below).

## Default path

1. Read the integrity standard (the referral rule, the one-in-eight cap on genuine referrals per account), the 2029
   plans (each account's shortlist, expected applicants, selection-day format and dates), the equivalence study's
   pairs and its report, and the technical manual's conditional standard errors.
2. Put both tests on one scale (the client files' 50 plus 10 per logit scale scores against the platform's logits),
   apply the referral rule to the study's supervised pairs (genuine by design) and read the referral rate by days
   between the two sittings: low for same-week sittings, where the second sitting's retest gain lifts the
   verification score, and higher at six weeks or more.
3. Carry the study's rate for each account's 2029 timing to the account (same-week campus selection days at the
   study's same-week rate, centralised selection days at its six-weeks-or-more rate).
4. Compare each with one in eight.

Ends on: no account, or only the centralised accounts whose study rate edges past the cap, against a golden that
flags every account whose shortlist reaches deep into its applicant pool with selection days weeks after the online
sitting, and some same-week accounts that shortlist very deep. The accounts, the rates and the golden list are fixed
in design (`## Ladder`).

## Stump sentence

A strong analyst who applies the referral rule to the equivalence study's supervised pairs and carries the study's
rates by timing to each account's 2029 selection days leaves off every account that shortlists deep, because the
study's volunteers were not shortlisted: an account's shortlisted candidates were chosen on the very online score
the check compares against, so their verification scores fall short of their online scores by regression to the
mean, by an amount set by how deep the account shortlists and how wide the adaptive test's standard error runs there,
and only each account's genuine referral rate built through its own applicant pool, offset by the retest gain the
study measures, reads which accounts will pass the cap.

## Three rules

Task type: psychometric-measurement-scale-validation (Psychology & Behavioral Science), which serves Data Quality Monitoring.
Domain test: the deciding quantity is a verification check's false-referral rate among candidates shortlisted on the score it verifies, built the way psychometrics builds it: each shortlisted candidate's ability given the online score, through the account's applicant pool and the adaptive test's conditional standard error (true-score regression), against the verification test's own error and the retest gain by days between sittings.
Swap: "which of our 28 stores' second stocktakes will flag more than one honest count in eight" stops making sense: no store is chosen for a high first count from a pool, no adaptive test's error grows where an item bank thins, no second sitting brings a retest gain that fades with the days between.
Layer 1: the platform export in UTC beside client exports in IST; scale scores in client files against logits and standard errors in the platform export; restarted sittings (an abandoned partial row and the completed row under one booking); an account under two codes after a July 2028 merger; the firm's QA and demo sittings under internal codes; campus codes in two formats; the plan workbook's merged headers and dates typed as text; the study's gap as two dates in the file and as days in the report. Each is written by the system named and is neutral to the call.
Layer 2: estimand_identification: candidates chosen on a noisy score regress on a second reading, so a verification check's false-referral rate among the shortlisted is built through each account's applicant pool and shortlist depth with the adaptive test's conditional standard error, offset by the retest gain by timing; an unselected study's rate does not carry.
Decisive step: building each account's genuine referral rate for its 2029 shortlist through its own applicant pool (true-score regression on the online score) with the verification test's error and the retest gain at the account's timing, rather than carrying the equivalence study's rates by timing.
Not semantics: every file, scale, clock, code and rule read correctly, the study's rates by timing still leave the deep-shortlisting accounts under the cap; the step is that a rate measured on an unselected group does not apply to a group chosen on the score, which no field, code or definition fixes.
Not rule application: the standard files the referral rule, the cap and the population (the genuine candidates each account shortlists in 2029); nothing files how the rate among the shortlisted is built, and executing every stated rule on the study's pairs gives the study's rates, the wrong answer.
Analyst test: a strong analyst who reads every file correctly and carries the study's rates by timing to the accounts files the default path's Ends on, executed on the clean truth in checks.py (R3a, R3b).
Estimand: integrity standard section on verification: for each client account, the share of its genuine shortlisted candidates in the 2029 season (candidates who sat their own online test, shortlisted on the account's 2029 plan from an applicant pool like its 2028 one) whom the referral rule refers at the account's 2029 selection days, against one in eight.
No decoy: nothing is planted; the equivalence study's report is correct about its volunteers and says who they were; no memo, draft or figure argues for carrying its rates.
No certified replay: no published or certified referral rate per account ships; the check is new in 2029, so no account has a referral history to reproduce.
Lesson: a check that compares a second reading with the first will refer honest units more often the harder the units were chosen on the first, so its false-alarm rate measured on unchosen units misstates every selected pool. No build on file teaches it (task130 v3 forecast a cohort chosen on a noisy outcome from an analog cohort the record held; task253 counts shrunken unit levels below a line).

## Tried and rejected

- Drift forecast from the cumulative particle load through an optical PM sensor (drift accrues with dose, not calendar
  time): the lesson is task46's (a rate law stationary only in cumulative service exposure), so the driver is spent.
- Seasonal confounding of a PM sensor's gain by humidity growth or aerosol type: the shape of task248's driver (a
  covariate moving over the year against a level comparison), one build earlier.
- An analyser ask (each analyser's 2027 days over 120 micrograms on the EU maximum daily 8-hour mean): every device it
  carried (span-check hours flagged N, the old analyser's parallel rows) is adjudicated by the station sheet, so the call-landing
  response executes it and keeps every figure; dropped for the node quarter's single silent device.
- Architecture 1 (each node's span read from its spread against the four distant analysers, the paired slope
  attenuated by the sites' partial hourly agreement): the stage 4 reader (medium effort, about two minutes) landed the
  call with an errors-in-variables slope instrumented by the other stations' mean, cued by plan 4's "true ozone
  concentration at its inlet", and kept all 36 ask figures after reading the vendor's firmware note. Regression dilution
  is textbook statistics, so the decisive step is readable to a strong model; and an ask one device deep falls to one
  document read. Realism tells it named: firmware dates cycling in ten-day steps, installation dates on a fixed
  five-week pattern, visit slots on a fixed cadence, the ES4104A analyser's model against its serial (T400 and API400E),
  head serials stepping by 37. The judge's pass on the same bundle: DETERMINISTIC (write-up wording only); its residual
  reading F1, the spread of the four stations' averaged series, gives 10 nodes, so architecture 2's write-up says the
  analysers' hours are pooled.
- Ask A on firmware 4.2's renumbered codes alone, the release note carrying a table of the codes up to 3.7 and from
  4.2: architecture 1's stage 4 reader read the note and kept 36 of 36. The note now gives 4.2's codes only (the records
  show the old meaning: before each node's update its status-1 records are the two warm-up hours after a restart), and
  the restart clocks stand beside it as a second primary, each moving all 36 figures alone.
- The firmware table without a date for OZ19 read as OZ19 never reaching 4.2: the spare's records after the 25 January
  rename lost their humid hours (OZ19 +89 against +18 to +24 elsewhere); OZ19 runs 4.2 from the spare's start at 11:00
  on 9 January, in the solver, the verifier and A1.
- Architecture 2 (each node's span read on the mixed afternoon hours, the hill villages above the night's surface
  layer): the stage 4 reader (Sonnet, medium, about four minutes) landed the call with a regression on the four
  analysers, the 900 m sites' night-time intercepts and the register's altitudes pointing it to the midday hours;
  the judge's pass on the same bundle was DETERMINISTIC, APPROVE, and Ask A held (0 of 36). A site's night-time
  decoupling shows in any residual by hour of day, so the decisive step is readable to a strong model.
- Architecture 3 draw, 2026-10-19, candidates that died before the card was filed: register coverage by dual-system
  estimation within post-strata after erroneous enumerations (task448 already runs capture estimated within route
  strata in the same task type); an adaptive item bank's drift under compromise read with purified anchors (filed as
  drift on the bank's scale, its literal reading is the contaminated thetas, so the estimand forks unless it names
  the purification, which files the method); rapid guessing read from item-specific response-time thresholds (the
  decisive step is a threshold choice, a coin flip in the client's measured runs); this world's forward referral rate
  under the SE-scaled rule (1.645 times the standard error of the difference: the rule's own scaling compresses every
  account into 2 to 9 per cent, too thin for a cap) and a fixed eight-point band (elite accounts at 40 to 60 per cent,
  no firm would adopt it, and a 2028 verification record would let a solver carry each account's empirical shortfall
  forward). The confidence-band rule on the verification score, with the check new in 2029, keeps the spread
  realistic and leaves no per-account history to carry.
