# task249 design note

## Draw

Card `cards/task249.json`, architecture 3 (v1 and v2 in lineage), re-rooted 2026-10-19 at the author's request: a
fresh draw in another client domain whose task type serves Data Quality Monitoring, new world and new decisive step.
The re-root also clears architecture 2's pairing override against task247. Verdict: WARN, no BLOCK. Each WARN,
answered: overuse.objective (Data Quality Monitoring in 4 of the last 12): the lane is Data Quality Monitoring &
Alerting. repeat.question_form (which, after task268): the call is a set of client accounts, and a set asks which. repeat.gate_g (forecasting, after task468 v2, an ETL build in another lane): both calls project a quantity the record does not hold, but task468 projects cost by tenure through survival, and this build projects a check's false-referral rate through true-score regression on a selected pool; no mechanism is shared.
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
  score's 95 per cent band, and caps the genuine candidates an account's check may refer in a season.
- **The call.** Which client accounts' verification checks would refer more than 15 per cent of the genuine
  candidates they shortlist in the 2029 season, on their 2029 plans (shortlist size against expected applicants,
  selection-day timing); those accounts sit the 24-item MAT-V Extended (MAL-IS-04 s.3.3).
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
  score is ability plus error, so the shortlisted are the candidates whose error ran upward; the smaller the share an
  account shortlists the more the chosen scores overstate ability, and the more so where the item bank thins and the online
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

1. Read MAL-IS-04 (s.3.2 the referral rule, s.3.3 the 15 per cent cap and the population: the genuine candidates an
   account shortlists on its plan for the season), the 2029 plans, the equivalence study's pairs and its report, and
   the technical manual's Table 4.3.
2. Apply the s.3.2 rule to the study's supervised pairs (genuine by design) and read the referral rate by interval:
   2.3 per cent within three days, 6.6 per cent at six weeks or more (the report's Table 2 gives the same bands; the
   second sitting's retest gain lifts MAT-V most in the first days).
3. Carry each account's 2029 interval to it: the day-one and first-company drives (MAT-V two days after MAT-R) at
   2.3 per cent, the later drives and assessment centres (seven to sixteen weeks) at 6.6 per cent.
4. Compare each with 15 per cent: none passes it.

Ends on: 0 accounts to MAT-V Extended (every account at 2.3 or 6.6 per cent, all 28 under the cap).
Golden: 15 accounts to MAT-V Extended: KSP, VRD, ANV, PRM, SQR, ABH, MTL, TJM, SHY, TRG, PBH, KVR, RNJ, CHT, LVN.

## Stump sentence

A strong analyst who applies the referral rule to the equivalence study's supervised pairs and carries the study's
rates by interval (2.3 per cent within three days, 6.6 per cent at six weeks or more) to each account's 2029
selection days moves 0 accounts to MAT-V Extended, because the study's volunteers were not shortlisted: an account's
shortlisted candidates were chosen on the very MAT-R estimate the check compares against, so their MAT-V falls short of
it by regression to the mean, by an amount set by how small a share of its own applicant pool the account shortlists and how
wide MAT-R's standard error runs there (Table 4.3 widens above +1 logit), offset by the retest gain the study
measures; built that way, 15 accounts pass the cap, from 22.2 to 33.3 per cent, and the other 13 sit at 3.4 to 9.6.

## Three rules

Task type: psychometric-measurement-scale-validation (Psychology & Behavioral Science), which serves Data Quality Monitoring.
Domain test: the deciding quantity is a verification check's false-referral rate among candidates shortlisted on the score it verifies, built the way psychometrics builds it: each shortlisted candidate's ability given the online score, through the account's applicant pool and the adaptive test's conditional standard error (true-score regression), against the verification test's own error and the retest gain by days between sittings.
Swap: "which of our 28 stores' second stocktakes will flag more than 15 per cent of honest counts" stops making sense: no store is chosen for a high first count from a pool, no adaptive test's error grows where an item bank thins, no second sitting brings a retest gain that fades with the days between.
Layer 1: the platform export in UTC beside the client results feed in IST, day first; logits and standard errors in the platform export beside the whole-number scale score; an interrupted attempt and its completed restart, under one booking reference until release 5.3.2 and under a fresh one after it; the platform's synthetic monitoring sittings under identities the candidate register does not hold; Paisaghar Lending's campuses under PGL until the client record moved on 2 September 2028; the 14 August re-send of the results feed and withdrawn shares; a case log with one row per decision, the desk's appeals logged as cases of their own and booking references blank on the centre-run accounts' cases; registrants who never sat; the plans workbook's merged header rows and selection-day ranges typed as text; the study's interval as two dates in the file and as days in the report. Each is written by the system named and is neutral to the call (R2a to R2g).
Layer 2: estimand_identification: candidates chosen on a noisy score regress on a second reading, so a verification check's false-referral rate among the shortlisted is built through each account's applicant pool and shortlist depth with the adaptive test's conditional standard error, offset by the retest gain by timing; an unselected study's rate does not carry.
Decisive step: building each account's genuine referral rate for its 2029 shortlist through its own applicant pool (true-score regression on the online score, with the online test's error read at the candidate's ability from Table 4.3) with the verification test's error and the retest gain at the account's interval, rather than carrying the equivalence study's rates by interval.
Not semantics: every file, scale, clock, code and rule read correctly, the study's rates by timing still leave the most selective accounts under the cap; the step is that a rate measured on an unselected group does not apply to a group chosen on the score, which no field, code or definition fixes.
Not rule application: the standard files the referral rule, the cap and the population (the genuine candidates each account shortlists in 2029); nothing files how the rate among the shortlisted is built, and executing every stated rule on the study's pairs gives the study's rates, the wrong answer.
Analyst test: a strong analyst who reads every file correctly and carries the study's rates by interval (2.3 and 6.6 per cent) to the accounts moves 0 accounts, the default path's Ends on, asserted in checks.py (R3a); modelling the shortlist without the retest gain moves 18, with one MAT-R error 12 (R3b).
Estimand: integrity standard section on verification: for each client account, the share of its genuine shortlisted candidates in the 2029 season (candidates who sat their own online test, shortlisted on the account's 2029 plan from an applicant pool like its 2028 one) whom the referral rule refers at the account's 2029 selection days, against 15 per cent (s.3.3).
No decoy: nothing is planted; the equivalence study's report is correct about its volunteers and says who they were; no memo, draft or figure argues for carrying its rates.
No certified replay: no published or certified referral rate per account ships; the check is new in 2029, so no account has a referral history to reproduce.
Lesson: a check that compares a second reading with the first will refer honest units more often the harder the units were chosen on the first, so its false-alarm rate measured on unchosen units misstates every selected pool. No build on file teaches it (task130 v3 forecast a cohort chosen on a noisy outcome from an analog cohort the record held; task253 counts shrunken unit levels below a line).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or
corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of
a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the band read as a one-sided 2.5 per cent test: 0 accounts | s.3.2's 95 per cent band | none | yes, a nominal error rate | none | no | no | readable |
| 1 the study's rates by interval carried to each account: 0 accounts | the report's Table 2 | none | yes, a pilot's rate carried to the field | none | no | no | readable |
| 2 the shortlist modelled with one MAT-R error for every ability: 12 | the manual's 16-item test | none | yes, a test's headline error | none | no | no | readable |
| 2 the shortlist modelled without the retest gain: 18 | none | none | yes, two sittings of one test read as interchangeable | none | no | no | readable |
| 2 true-score shrinkage of each pool's top share with each candidate's reported error (the error at the estimate): 18 | the manual's s.4.2 (the reported error) | se_logit on every attempt | yes, Kelley's formula with the reported error | none | no | no | readable |
| 3 (decisive) each account's shortlisted candidates read through its own applicant pool (true-score regression on MAT-R at Table 4.3's error), with the study's retest gain at the interval: 15 | none (no document names the shortlisted candidates' overstatement or the choosing) | none (no column marks a candidate's selection or a shortfall's cause) | no (the reflex carries the study's rate) | none (no shortlisted candidate has sat MAT-V; the check is new in 2029) | no | no | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | client accounts | the 28 accounts of the 2029 plans, PGL inside NVK | PGL's 2028 campuses left out of NVK's pool | same call | client_accounts.csv (merged 2 September 2028); asserted (SF1, R2a) |
| SF2 | genuine candidates | candidates who sat their own MAT-R (s.2) | pools with the 2028 confirmed impersonations left in | same call | s.2; asserted (SF2, R2d) |
| SF3 | they shortlist on their 2029 plans | the plan's shortlist over its expected applicants | the 2028 shortlist depth over the 2028 pool | same call | s.3.3 names the season's plan; asserted (SF3) |
| SF4 | an applicant pool like the previous season | the candidates whose 2028 result was shared with the account | withdrawn shares left out | same call | asserted (SF4, R2b) |
| SF5 | refer | MAT-R above MAT-V plus 1.96 MAT-V standard errors (s.3.2) | a two-sided band | same call | s.3.2 names above; asserted (SF5) |
| SF6 | more than 15 per cent | strictly above | 15 per cent or more | same call | no account within 5.4 points of 15 per cent (SF6, C1) |
| SF7 | the verification check | the 12-item MAT-V | MAT-V Extended | the call is which accounts move to Extended | s.3.3 |
| SF8 | the interval to MAT-V | two days at day-one and first-company drives (the Calendar sheet: lab sitting on day 1, selection day on day 3); the plan's selection days otherwise | one or two days at the day-one drives; the study's six-week band for every later account | same call | asserted (SF8) |
| SF9 | estimates | logits as the platform holds them (s.3.2) | whole-number scale scores read back | same call | asserted (SF9, R2c) |
| SF10 | the pool's ability spread | the pool's variance less its mean squared standard error | the estimates taken as abilities | same call | asserted (SF10, C3) |

## Ladder

| Rung | Method | Accounts moved | Wrong by |
|---|---|---|---|
| 0 | the 95 per cent band read as a one-sided 2.5 per cent test | 0 | leaves off all 15 |
| 1 | the study's rates by interval (2.3, 6.6 per cent); the study's own regression of MAT-V on MAT-R carried to each shortlist keeps every account under the cap as well | 0 | leaves off all 15 |
| 2 | the shortlist modelled with one MAT-R error of 0.38 for every ability | 12 | leaves off ABH, KSP, VRD (11.4 to 11.6 per cent against 23.9 to 24.8) |
| 2 | the shortlist modelled without the retest gain | 18 | adds NVK, OJS, UJB (19.8 to 21.9 per cent against 8.4 to 9.6) |
| 2 | true-score shrinkage of each pool's top share with each candidate's reported error (the error at the estimate) | 18 | adds NVK, OJS, UJB (18.7 to 21.9 per cent) |
| 3 | golden: each pool's shortlist with MAT-R's error at the ability (Table 4.3) and the retest gain at the interval | 15 | none (flagged 22.2 to 33.3 per cent, kept 3.4 to 9.6) |

Separation: every rung names a different list or fails on different accounts, so each correction is needed. The
day-one accounts that shortlist most selectively reach where MAT-R's error is widest, and only the error read at the ability keeps
them over the cap against a 0.32 logit retest gain; the mid-sized day-one accounts sit under it only with the gain and
with the error read at the ability, not at the estimate. Every construction that reads the error at the ability files
the same 15: the estimates taken as abilities (flagged 20.8 per cent or more, kept 10.1 or less, C3, C4), the full
posterior per pool member (22.1 and 9.6, C6), shrinkage at the shrunken ability (28.9 and 13.8, C7), and the world's
own truth. The study's own top tenth of MAT-R scorers separates the shrinkage at the ability from the shrinkage at the
estimate (F2).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the 28 accounts of the 2029 plans; each account's genuine shortlisted candidates (s.3.3) |
| 2 | Unit of account | one client account (PGL inside NVK, SF1) |
| 3 | Attribution window | the 2029 campus season (s.3.3) |
| 4 | As-of dating | 14 May 2029; plans due 30 April, study report 19 January |
| 5 | Version basis | MAL-IS-04 issue 4; manual edition 2028.2; the plans as compiled |
| 6 | Denominator | the account's genuine shortlisted candidates (s.3.3) |
| 7 | Weighting | each candidate once (one booking a season, s.2) |
| 8 | Window length | one season |
| 9 | Boundary inclusivity | strictly above 15 per cent; no account within 5.4 points (SF6) |
| 10 | Rounding path | shares unrounded before the cap; logits as held (SF9) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | the 2028 season closed; every pool complete |
| 13 | Order of operations | pool, depth, interval, gain, projection, cap |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | a candidate's repeated shares count once in a pool (the 14 August re-send) |
| 16 | Identity normalisation | PGL to NVK (SF1); candidates by candidate_id |
| 17 | Netting against gross | none |
| 18 | Dimensional units | logits (s.3.2); scale scores 50 plus 10 per logit (SF9) |
| 19 | Code and status semantics | completed attempts carry estimates; interrupted ones none (R2f) |
| 20 | Integerisation | none in the call |
| 21 | Clause scope | s.3.2 and s.3.3 apply to every account; s.4 to s.6 to the asks |
| 22 | Forward window contents | the 2029 pools like 2028's (s.3.3); intervals from the plans and the calendar |

## Literal reader

Executed word for word, s.3.3 files the quantity (the share of an account's genuine shortlisted candidates the s.3.2
check would refer), the population (the account's plan for the season with an applicant pool like its previous one)
and the cap; nothing files how the share is built. Read literally, the candidates are the ones the account shortlists,
chosen on MAT-R, so the share is taken over them, not over unselected volunteers; their abilities, MAT-R's error at
each ability (Table 4.3), MAT-V's error and the gain at the interval (the study) are each in the folder. Every model of
the shortlist built from those parts (normal pool with its errors taken out, the estimates as abilities, the full
posterior per pool member, shrinkage with Table 4.3 read at the shrunken ability, the gain by plain interval means)
files the golden 15 (C2 to C4, C6, C7, F1), and so does the world's own truth; carrying the study's rate takes the
share over a population the clause does not name. The one shrinkage that differs reads MAT-R's error at each
candidate's estimate (the reported error, manual s.4.2) where Table 4.3 gives it at the ability; on the study's own
top tenth of MAT-R scorers it predicts MAT-V a tenth of a logit lower than scored while the shrinkage at the ability
lands within a fiftieth (F2), so the data rules it out and it stands as a rung, not a reading.

## Oracles

none. No account has a referral history (MAT-V is new in 2029) and no projected share, list or certified figure ships;
the study's referral rates are correct about its volunteers and rank no account.

## Ask sheet

Three asks, decoupled from the call: none reads a pool, a plan, the study or Table 4.3, and each runs over rows the
call never reads. Each carries one silent primary that moves every figure in it, with hazards beside it.

- **Ask A, item exposure** (MAL-IS-04 s.4; 5 figures: the items over 12 per cent in each July 2028 test week and the
  items rested for 2029). Primary: the platform's synthetic monitoring sittings, run through production early on each
  test week's Monday under identities the candidate register does not hold (6,400 sittings, desktop and laptop, each
  running QA's fixed sixteen-item regression script). Nothing on the exposure path joins the register, the attempts' items_shown ties
  the log row for row with them in, and the register holds more registrants than the attempts hold identities, so
  every count reconciles on the wrong path. Hazards: interrupted attempts dropped, sittings counted per attempt, UTC
  weeks.
- **Ask B, impersonations** (s.5; 8 figures: the sittings standing confirmed in each college tier and the rate per
  thousand candidates on any 2028 shortlist). Primary: the desk logs an appeal as a case of its own, opened after the
  sitting's last decision, so a sitting's standing is the latest decision across the candidate's cases; each case's
  latest row, the habitual read of a decision log, keeps the overturned confirmations and misses every figure. Hazards:
  "confirmed on appeal" read as not confirmed (moves every figure), sittings counted by booking reference (blank on the
  centre-run accounts' cases), shortlist rows for candidates.
- **Ask C, interrupted bookings** (s.6; 6 figures: the share interrupted and the count finished on another device, for
  desktop, laptop and tablet). Primary: from release 5.3.2 (9 July 2028) a restart carries a fresh booking reference
  against s.6's "under the same booking", so attempts grouped by reference split every later restart: the restart
  becomes a booking of its own and the interrupted booking never finishes, and every figure misses. Hazards: the
  suite's desktop and laptop sittings in the denominators, the device of the completed attempt for the first.

Separation: no device row is in the call's population. The suite holds no share (R2e), interrupted attempts carry no
estimate (R2f), every pool member has one completed estimate (S1), and the call reads no case, shortlist, exposure row
or booking reference. Deleting every device leaves the call as hard.

The cracker lands the call, runs the hygiene battery on its own path (key uniqueness, duplicates, unmatched joins,
fan-out, ties) and executes every filed rule that path points at. The mirror stops on the study's rates and is as
careful on the asks, also checking every identity against the register.

| Ask | Cracker's path | Figures kept | Verdict |
|---|---|---|---|
| A exposure | attempts joined to the log on booking and attempt, IST weeks, distinct candidates, no register join on the path | 0 of 5 | misses |
| B impersonations | each case's latest row, distinct candidates, both confirming findings | 0 of 8 | misses |
| C interruptions | attempts grouped by booking reference, as s.6 states | 0 of 6 | misses |

Pair ceiling: 35.7 (the cracker keeps 0 of 19 ask figures, C = 38 + 7 + 0 = 45.0; the mirror keeps 5 of 19, S = 5 +
7 + 55 x 0.263 = 26.5). A response that lands the call and also checks the exposure path against the register keeps
Ask A's 5, C = 59.5, a pair of 43.0 with the same mirror.
Mirror leakage: 26.3 per cent of ask weight (5 of 19 figures, all Ask A: the register check finds the suite; Ask B and
Ask C keep none). The next most careful paths keep 5, 4 and 2 of 19 (completed attempts only, sittings by candidate
with "confirmed impersonation" as the only confirming finding, UTC weeks with every confirmed row).
Measured by: task249/generator/pair.py on the cut pack (every path figure by figure, a hit within half a unit of the
stated rounding).

## Pre-ship check

The three rules re-read against the built pack (target.zip md5 3a097683ea6ff33166093c2ec837dbda):
- Domain: the deciding quantity is a verification check's false-referral rate among candidates shortlisted on the
  score it verifies, built through each pool with MAT-R's conditional error at the ability (Table 4.3) and the retest
  gain at the interval; no noun swap keeps the task. Holds.
- Layer 2 decides, Layer 1 only complicates: every Layer 1 item is asserted neutral to the call (R2a to R2g), and the
  call is the same under every construction that reads the error at the ability (C3, C4, C6, C7, the world's own truth).
- Rule 3: no planted defect (every device is a system's own behaviour: QA's suite through production, the desk's appeal
  cases, release 5.3.2's fresh references), no data semantics (the call turns on no field's reading), no rule
  application (MAL-IS-04 files the estimand; executing every stated rule on the study gives 0 accounts).
- Free gates: checks 0 failures; verify 0 failures from the zip (the exact posterior, a different construction, files
  the same 15 at 22.0 per cent or more and 9.5 or less); figures_check 43 of 43; precut 51 checks, 0 FAIL; leak.py
  REVIEW, every line answered; container audits clean; two byte-identical rebuilds (23 files); guard heart WARN, answered.
- Tightest figures and their flip conditions: the desktop interruption share, 1.644 per cent, 0.0008 from its rounding
  edge (one more interrupted desktop booking, or about 280 fewer desktop bookings, which only a reading that drops
  confirmed impersonations' bookings from "2028 bookings" gives, and nothing licenses it); the week of 10 July's
  nearest item, 0.108 points from the 12 per cent ceiling (every exposure count unchanged with confirmed
  impersonations' sittings left out, B4); the T1 impersonation rate, 0.0145 from its edge (a count of 5 over 1,972).
- Pair: measured 35.7 (cracker 0 of 19, mirror 5 of 19).

## Leak check

leak.py --asof 2029-05-14: REVIEW, no LEAK. Each REVIEW line, answered:
- Answer figures in the pack: 3.3 in MAL-IS-04 is the section number; 2.3 and 6.6 per cent are the equivalence study's
  own referral rates (report Table 2), true of its volunteers and the default path's reading, not the answer. Harmless.
- Stump vocabulary in the dictionary, the standard, the manual, the report and the prompt: the field's own nouns
  (candidate, shortlisted, sitting, selection, ability, interval, integrity); no sentence names the shortlisted
  candidates' overstatement or the choosing that causes it. Harmless.
- client_plans_2029.xlsx and client_accounts.csv name the accounts beside numbers: the plans' inputs (expected
  applicants, shortlist, selection days) and the register, ranking nothing on the referral share. Harmless.
- selection_venues_2029.csv carries dates after 14 May 2029: the venues' booking windows for the coming season, which
  a venue list states in advance. Harmless.

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
- Ask A's highest weekly exposure of any item (four figures): any response that checks the attempts against the
  register keeps it whole, so the ask's weight sat on the one device a careful response can find; replaced by the
  count of items rested for 2029, which the suite moves as well, and the ask cut to five figures.
- Appeal outcomes recorded as later rows of the original case: each case's latest row, the habitual read of a decision
  log, filed the golden, so the impersonation ask carried no device. The desk now logs an appeal as a case of its own,
  as its own sheet would, and a sitting's standing is the latest decision across the candidate's cases.
- The synthetic suite's sittings labelled release 5.3.2 in the week of 3 July, before the release went live: a marker
  isolating the device rows in one week. They now carry the release in service, as the platform stamps every attempt.
- Shrinkage of each pool's top share with each candidate's reported error (Kelley's formula at the estimate) taken as a
  competing reading: it adds NVK, UJB and OJS, but the study's own top tenth of MAT-R scorers refutes it (it predicts
  their MAT-V a tenth of a logit lower than scored) while the shrinkage at the ability, the full posterior and the
  world's own truth all file the 15. Kept as a rung and stated in the write-up's critical components, so a judge sees
  the refutation in the shipped data.
