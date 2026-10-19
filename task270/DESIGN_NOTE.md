# task270 design note

Architecture 1, drawn 2026-10-19 (wave 4, Descriptive lane, sathay3012). The slot's seed DA20 went to task269's third architecture, so task270 draws its own world. A mid-sized Ohio city's police department (fictional, like its civil service commission, academy, testing vendors and people) ran a validation trial in its 2024 and 2025 entry examinations: every candidate sat all five components (the written test, the oral board, the physical ability test, a situational judgement test and a personality inventory), while appointments went in rank order of the written test and oral board composite, with veterans' points, to candidates above the physical ability pass mark. For 2027 the examination keeps two scored components, and the Civil Service Commission's rules judge a component by its correlation with the police academy's final average across everyone who sat the examination. Only the appointees have an academy average.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task270.json`, architecture v1, registered 09:14 UTC on 2026-10-19. The police department is the city's (`local_government`); the Civil Service Commission (`committee_or_panel`) approves the 2027 entry examination announcement at its meeting (`vote_or_meeting`); the requester is the department's personnel research analyst, who runs the validation trial (`research_desk`); the working file is the Commission's rules for the police officer examination (`filed_standard`).
2. Pairing: Psychology & Behavioral Science (client domain) / psychometric-measurement-scale-validation / Descriptive & Distribution Analysis. The task type's own object decides the call: validity evidence for a selection procedure, here each component's predictive validity for academy performance across the candidate pool, which the validation sample shows only inside the band the appointment rule cut. The pairing has never carried this lane's objective.
3. Niche: a civil-service entry examination validated on the candidates it appointed, where the appointments were made on two of the components being judged and the outcome exists for no one else.
4. Call and shape: which two of the five components the 2027 examination keeps (`ranked_slate_under_cap`, question form which). Shape 01 (a ranked list under a cap): each component's standing across the pool, in or out, and the first component below the two; the cap is the two scored components the 2027 examination keeps.
5. Gate G `method_or_model_selection`, strategy `population_selection`: the decisive step is the model of who reached the academy, a correction for selection on the composite the appointments were ranked on, against the appointees' own correlations and the per-component correction a validity analyst applies first. Decisive generator G9 (the outcome is seen downstream only for those an upstream rule selected), with G17 (the correction's statistical premise) and G16 (the correction the design forces). Layer 2 family `estimation_fit`, pattern `own:indirect-range-restriction-on-a-selection-composite`.
6. Data-native sentence: every 2024 and 2025 candidate sat all five components, but only those appointed in rank order of the written test and oral board composite reached the academy, so the academy average exists only inside a band of the composite, and each component's own spread among the appointees no longer measures how much the appointment rule cut it.
7. Sources, one line each:
   - The client's rigor library, psychometric-measurement-scale-validation (alpha against omega, categorical estimators, parallel analysis): none works a validity under selection; this build's step is outside the cards.
   - task267 (verification bias), task268 (informative censoring), task182 v4 (length-biased snapshots), task139 (per assigned unit), task265 v1 (left truncation) and task452 v2 (revised inclusion probabilities), the guard's structural matches on selection into the record: differentiated on the card; none corrects a correlation through the covariance of the variables a deterministic cut was made on.
   - task269 v1 (a decision study for a new examining design, landed by a reader): differentiated; nothing here is projected to a new design.
   - task269's `## Tried and rejected` set range restriction aside on 2026-10-19 only because `population_selection` was then banned against task268; task268 has left the three-build window and this card registers clear of every axis ban.
   - `guard.py slots` on the driver: word overlaps only (task199, task229, task117, task124, task135), no screen of this mechanism.
8. People, drawn with `guard.py names --geo us --seed 270`: Melanie Howard (the department's personnel research analyst, the requester, author of the validation trial plan) and Julia Larson (the Civil Service Commission's executive secretary, author of the Commission's rules). Ryan Bartlett, drawn first, was replaced on the guard's `people.first` warning. Invented names (the city, its testing vendors and their products) screened by hand against Ohio cities and real public-safety testing vendors at stage 3.
9. WARNs answered: `overuse.shape` (01: the call keeps two of five, a capped list, and the shape fits it); `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection against task177: the correction the selection design forces is this build's mechanism, and no other key is honest for it); `repeat.question_form` against task269's spent third architecture (which: the call picks two of five).
10. Screens, run as code on a candidate-level simulation of the world before any card (scratch `t270/proto.py`, `proto_agree.py`, `rr_search2.py`):
    - WHAT screen: the population (everyone who sat the 2024 and 2025 examinations), outcome (the academy final average, a separated recruit's average at separation), window (the four administrations), unit (the candidate) and comparison (the two highest correlations) are all filed; the decisive step settles none of them, it decides how the unobserved correlation is estimated from the appointees.
    - 1.2a: the filed quantity is unobserved: no candidate outside the appointees has an academy average, so the pool's correlation is a counterfactual output, and the appointees' correlation, the per-component Case II correction and the multivariate correction are three estimators of it, the first two resting on premises the appointment rule breaks.
    - Reflex sweep over 300 world draws at police-department scale (about 3,650 candidates in four administrations, about 800 appointees): in the 210 draws where every licensed correction agrees, the appointees' correlations, the per-component Case II correction and a mixed correction (Case II for the two ranked components, Case III for the rest) keep another pair in every draw, usually the written test and the personality inventory.
    - The golden's own family: Lawley on the variables the appointments were made on, Lawley on everything recorded before appointment, Case III on the final score with the physical ability pass mark, Case III on the final score alone and Lawley on the two ranked components alone keep the written test and the oral board in all 210; the full order of the five agrees across the three complete corrections in 118 and across all five in 94.
    - The coefficients themselves differ between licensed corrections by a median 0.032 (10th to 90th percentile 0.018 to 0.059), so no coefficient is graded at two decimals: the graded construction is the call, the first component below and the order.
    - Variance-only: the step moves each component's level, the two ranked ones up and most; it is not an uncertainty correction.

## Default path

1. Read the trial plan: the 2027 examination keeps the two components with the highest validity, each component's
   correlation with the academy criterion across the candidate pool, everyone who sat all five components in the four
   2024 and 2025 examinations.
2. Put the five score files on the Commission's candidate numbers (Halvorsen's written test carries them; the
   crosswalk gives Pellwyn's and the inventory's identifiers), take the appointments from the eligibility lists and
   the criterion from the gradebook by employee number: 3,668 candidates sat all five, 787 of them were appointed.
3. Correlate each component's score with the criterion over the candidates who have one: the inventory 0.25, the
   written test 0.24, the oral board 0.14, the situational judgement test 0.14, the physical ability test 0.12.
4. Seeing that only the appointees have a criterion, correct each correlation for range restriction by that
   component's own spread in the pool over its spread among the appointees (Thorndike's Case II): the written test
   0.31, the inventory 0.25, the oral board 0.21.
5. Keep the two highest.

Ends on: the written test and the work style inventory.
Golden: the written test and the oral board.

On the built pack the default path keeps the written test and the inventory with the oral board third (Case II: the
inventory 0.25 against the oral board 0.21); the golden keeps the written test (0.50) and the oral board (0.46), the
inventory first below at 0.30, then the situational judgement test (0.26) and the physical ability test (0.22).

## Stump sentence

The default path keeps the written test and the work style inventory because it judges each component by its
correlation with the academy criterion among the 787 appointees, or corrects each correlation by that component's own
spread, when the lists appointed in rank order of the written test and oral board composite: the composite's spread
among the appointees is cut to less than half its spread in the pool (2.06 times), while each component's own spread
is cut only 1.32 times (the written test) and 1.45 times (the oral board), so only the correction on the variables
the appointments were made on gives the oral board back the validity the selection took from it (0.46, against the
inventory's 0.30) and keeps the written test and the oral board.

## Three rules

Task type: psychometric-measurement-scale-validation (Psychology & Behavioral Science), which serves Descriptive & Distribution Analysis in the taxonomy.
Domain test: the deciding quantity is each examination component's criterion-related validity (its correlation with academy performance) for the people the examination ranks, the selection-validation field's own object, estimated from a validation sample the appointment rule cut through the multivariate (Pearson-Lawley) correction for selection on the variables the appointments were made on.
Swap: "which two of five supplier audits a factory should keep, judged by their correlation with warranty returns" keeps a correlation and loses what the call turns on: a civil-service list that appoints in rank order of a weighted composite with a veterans' credit above a physical hurdle, a criterion that exists only for the appointed, and validity as personnel selection defines it for everyone the examination ranks, so with supplier nouns there is no selection rule to model and the task reads as a correlation table.
Layer 1: two written test forms Halvorsen equates by its scaled score (the raw score beside it); oral board ratings at member and dimension grain, a member standing down for a candidate they know (the panels' sheets); second runs of the course for first-run failures (the timing sheets); Pellwyn's own identifiers and a sheet an examination (its export); Halvorsen's inventory under Halvorsen identifiers with five scales (its export); the gradebook's new layout from class 25-3, separated recruits' average in its own column (the academy's new learning system); candidates who missed a component (attendance); eligibility lists carrying only listed candidates (the Commission's register). Nothing is placed to be caught.
Layer 2: the estimation-fit family; the correlation in the candidate pool is estimated from the appointees by modelling the selection, the pool's covariances of the written test, the oral board, the veterans' credit and the physical ability test's points with the appointees' covariances of every score and the criterion (Pearson-Lawley), where the per-component correction treats each component as if the appointments had been made on it alone.
Decisive step: modelling the appointments as selection on the composite, so the oral board's restriction runs through the written test and the trial components' through their covariance with both, with the multivariate correction for selection on several variables in place of the univariate correction of each component by its own spread.
Not semantics: every field read correctly (the scaled score, the oral board's mean of ratings, the faster run's points, Pellwyn's scaled score, the Dependability scale, the criterion with separations, the appointments on the lists) still leaves the analyst correlating among the appointees or correcting each component by its own spread, and both keep the work style inventory.
Not rule application: the trial plan files the population (every candidate who sat all five, appointed or not), the criterion and the decision (the two highest validities across the pool), and no filed rule says how to estimate a correlation whose criterion is observed for one candidate in five, so executing every stated rule leaves the estimator to the analyst and the field's reflex correction files the default answer.
Analyst test: a strong analyst who joins every file correctly and corrects each component's appointee correlation for its own restriction (Case II) files the written test and the work style inventory (Ends on), when the correction on the variables the appointments were made on files the written test and the oral board.
Estimand: the validation trial plan (sections 3 to 6) files the population (every candidate who sat all five components in the four 2024 and 2025 examinations, appointed or not), the outcome (the academy's final average, or the average at separation), the window (the four examinations, academy classes 24-2 to 26-2), the unit (the candidate) and the comparison (the two highest correlations of a component's score with the criterion).
No decoy: nothing is planted; no memo, draft, published validity, vendor report or stakeholder figure ranks the components, and the 2022 job analysis (a distractor) links knowledge and skills to the 2022 components without ranking them.
No certified replay: no file publishes a validity, a corrected correlation, a selection ratio or a restriction ratio, so the method is not recovered by reproducing a figure.
Lesson: when appointments are made on a composite, each component's spread among the appointees understates how hard the selection cut it, so the univariate correction under-corrects the components the composite was built from and leaves incidental predictors on top; correcting through the covariances of the selection variables is what the field's multivariate correction does, and no build on file teaches range restriction or selection on a composite.

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 (default) each component's correlation with the criterion among the appointees | the plan defines validity as the correlation with the criterion, and the criterion exists only for the appointees | the gradebook joins to the lists by employee number | yes: correlate where both are observed | none: no published validity | the battery finds nothing | yes: five correlations | readable |
| R1 each correlation corrected by the component's own spread in the pool over its spread among the appointees (Case II) | the plan's population is everyone who sat all five, appointed or not | every score file covers the pool | yes: the field's textbook correction for range restriction | none | none | yes: one ratio a component | readable |
| R2 Case II on the written test and the oral board, Case III on the final score for the three components the lists did not rank on | the rules rank on the final score | the lists carry the final score | yes: the textbook split between direct and indirect restriction | none | none | yes | readable |
| R3 (decisive) the pool's covariances of the variables the appointments were made on (the written test, the oral board, the veterans' credit, the course points) carried through the appointees' covariances of everything (Pearson-Lawley) | none names a correction, a selection variable or a restriction ratio; the rules state how the lists were made, the plan what validity is and for whom | no column holds a validity, a ratio or a covariance | no: the opponent corrects each component for its own restriction and treats the two ranked components as directly restricted | no published figure to reproduce | the battery (keys, joins, duplicates, forms, separations) never asks what the appointments were selected on | no: a covariance matrix of four selection variables against seven | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the candidate pool | every candidate who sat all five components in the four examinations, appointed or not (3,668) | the candidates with a criterion (the appointees) | another pair (the default path) | the plan (section 3): whether or not they were appointed |
| SF2 | the criterion | the academy's final average, or the average at separation for a recruit who left | graduates only | same call | the plan (section 4) and the handbook; asserted: same call without the 22 separated recruits |
| SF3 | the written test score | Halvorsen's scaled score | the raw score | same call | the rules (3.1) and the plan (section 5); asserted |
| SF4 | the oral board score | the mean of the ratings given, times 20 | the sum of the ratings | same call | the rules (3.2); asserted |
| SF5 | the physical ability test score | the points for the faster run | the first run's points; the faster time | same call | the rules (3.3) and the plan; asserted |
| SF6 | the situational judgement score | Pellwyn's scaled score | the raw score | same call | the plan (section 5); asserted |
| SF7 | the inventory score | the Dependability scale | another of the five scales | not a reading: the plan names the scale | the plan (section 5) |
| SF8 | the correction | the multivariate correction on the written test, the oral board, the veterans' credit and the course points | on every score recorded before appointment; Case III on the final score with the course points; on the final score alone; on the two ranked components alone | same call, same order of all five | the data: the five licensed selection models keep the written test and the oral board with the inventory first below and the same order (asserted) |
| SF9 | the veterans' credit | a selection variable (it moved candidates up the list) | left out | same call | asserted under the two-ranked-components model |
| SF10 | the physical ability test in the selection | its points (the list took the passers, and the points carry the time) | its pass, a 0 or 1 constant among the appointees | the pass cannot enter a correction (its covariance among the appointees is singular) | the data; the final-score models with the points agree (SF8) |
| SF11 | pooling the examinations | one pool of the four examinations | each examination corrected on its own, combined by its candidates | same call, same order | the plan (section 3); asserted (Fisher-z average weighted by candidates) |
| SF12 | the correlation | Pearson's product-moment correlation | a rank correlation | not a reading of validity across the pool: no rank correlation corrects for selection | the field's definition of a validity coefficient |
| SF13 | the appointees | pool members appointed and recorded in the gradebook (787) | every appointee, partial candidates included (804) | not the pool: partial candidates sat fewer than five | the plan (section 3) |
| SF14 | the separated recruits from class 25-3 | the average at separation from its own column | the weighted average column only | same call | the gradebook's own columns; asserted (SF2) |
| SF15 | the highest validities | the largest correlations, all five positive | the largest in absolute value | same call | every validity is positive under every route; asserted |

## Ladder

Values on the built pack (analysis.py; asserted in checks.py).

| Rung | Construction | Kept | Margin at the cut | Killed by |
|---|---|---|---|---|
| R0 (default) | each component's correlation among the 787 appointees | the work style inventory 0.25 and the written test 0.24 | the oral board third at 0.14, 0.10 below | the plan's population: everyone who sat all five, appointed or not |
| R1 | Case II for every component on its own spread | the written test 0.31 and the work style inventory 0.25 | the oral board third at 0.21, 0.05 below | the appointments ranked the composite, cut 2.06 times, not each component on its own |
| R2 | Case II for the two ranked components, Case III on the final score for the rest | the written test 0.31 and the work style inventory 0.30 | the situational judgement test 0.25, the oral board last at 0.21 | the two ranked components were selected through the composite, not each directly |
| R3 (decisive) | Pearson-Lawley on the written test, the oral board, the veterans' credit and the course points | the written test 0.50 and the oral board 0.46 (golden) | the work style inventory first below at 0.30, 0.16 below | the golden |

- **Position.** The oral board is third on R0 and R1 and last on R2; it is never in the pair before R3.
- **Dominance.** The decisive move raises the oral board 3.2 times (0.14 to 0.46) and the inventory 1.2 times (0.25 to
  0.30), an edge of 2.6, against the inventory's lead of 0.10 over the oral board among the appointees.
- **Reflexes.** A rank correlation among the appointees keeps the inventory and the written test (0.22, 0.21); the
  final score as the only selection variable keeps the golden pair (SF8); each examination corrected on its own and
  combined keeps the golden pair and order (SF11).
- **Convergence.** The five licensed selection models give the written test 0.49 to 0.50, the oral board 0.45 to 0.46,
  the inventory 0.30 to 0.31, the situational judgement test 0.25 to 0.26 and the physical ability test 0.21 to 0.22,
  the same order under each, adjacent gaps at least 0.035 (asserted). The coefficients are not graded; the call, the
  first component below and the order are.
- **Worth.** The pair moves at R3 and nowhere else; every graded construction (the pair, the first below, the order)
  differs between R0 or R1 and R3.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | every candidate who sat all five components in the four examinations, appointed or not | filed (the plan, section 3); SF1 |
| 2 | Unit of account | the candidate (a person who sat in two examinations is two candidates) | filed (the rules, Rule 7: a candidate number at registration) |
| 3 | Attribution window | the four 2024 and 2025 examinations; academy classes 24-2 to 26-2 | filed (the plan, the calendar) |
| 4 | As-of dating | the lists as certified, dispositions as recorded; the gradebook complete for class 26-2 | by construction (the last class graduated in August 2026) |
| 5 | Version basis | one release of every file | by construction |
| 6 | Denominator | the pool's spread of every score, estimated from the appointees for the criterion | filed (the estimand); the decisive step |
| 7 | Weighting | each candidate once, unweighted | filed (the plan: across the candidate pool) |
| 8 | Window length | four examinations, eight classes | filed |
| 9 | Boundary inclusivity | all five components sat; separated recruits in | filed (the plan, sections 3 and 4) |
| 10 | Rounding path | the call and the order from unrounded correlations; costs to the cent and rates to two decimals, computed unrounded | prompt; asserted margins |
| 11 | Tie-break | none needed: adjacent validities differ by 0.04 or more | asserted |
| 12 | Maturity and censoring | every trial recruit has a criterion (graduated or separated) | by construction |
| 13 | Order of operations | scores as the rules define them, then the correlations, then the correction | filed (the rules, the plan) |
| 14 | Row order | none matters | by construction |
| 15 | Duplicate resolution | one row a candidate in each score file (a rating, a run, a recruit at their own grain) | by construction; the asks' devices sit in the tracking exports and the ledger |
| 16 | Identity normalisation | candidate numbers across the score files, Halvorsen and Pellwyn identifiers through the crosswalk, employee numbers to the gradebook | filed (Rule 7); by construction |
| 17 | Netting against gross | for Ask A, what the work cost: accruals reversed are out, accruals relieved are in | filed (the plan, section 7); the device |
| 18 | Dimensional units | scores on their own scales, correlations unit-free; dollars; per cent | filed |
| 19 | Code and status semantics | dispositions, the gradebook's outcomes; for the asks, application statuses, ledger sources | the files' own columns; never the stump |
| 20 | Integerisation | people whole; dollars to the cent | prompt |
| 21 | Clause scope | the plan's sections 3 to 6 govern the call; sections 7 and 8 the asks | filed |
| 22 | Forward window contents | the 2027 examination ranks applicants like those of 2024 and 2025 on the components kept | filed (the plan, section 1) |

## Literal reader

Executed word for word, the prompt and the plan fix the estimand: for each component, the correlation between its
score (the rules' and the plan's definitions) and the academy criterion (the final average, or the average at
separation) across every candidate who sat all five components in the four 2024 and 2025 examinations, appointed or
not; keep the two highest and rank all five. Every literal reading of the terms gives the same population, scores and
criterion (SF1 to SF15). The criterion is observed for 787 of the 3,668, so the correlation has to be estimated, and
every model of the selection the rules describe (the lists ranked the final score of the written test and the oral
board with the veterans' credit, among the candidates who passed the course) names the written test and the oral
board with the inventory third; the work style inventory comes into the pair only from correlating among the
appointees or correcting each component by its own spread, never from another reading.

## Oracles

None on the main call: no file publishes a validity, a corrected correlation or a ranking of the components; the job
analysis (a distractor) links knowledge and skills to the 2022 components without a figure, and the campaign summary
(a distractor) reports channels and fairs. For the asks: no file publishes a component's cost, an invoice amount
beside the ledger or an applicant count; the campaign's "applications started" is the careers page's tracking pixel
and ties to no reading of the tracking exports.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops | Realism |
|---|---|---|---|---|---|---|---|---|
| A, each component's cost per candidate who sat it over the four examinations, in dollars to the cent | 5 | a measure every component carries that the call does not turn on (the plan, section 7) | the Commission prices the 2027 examination on the components it keeps | D6 and D2: the city's financial system changed on 1 July 2024; the old system's 30 June 2024 accruals for the spring 2024 invoices (all five components) were reversed by Finance in one line on 4410, while the invoices posted in full in July and August; from FY2025 the new system relieves the accrual and the invoice posts only its difference, so the 30 June 2025 accruals carry the spring 2025 cost | H1: payroll lines name a pay period, not an examination (mapped by the calendar's days); H2: the FOP agreement's retroactive pay of April 2025, one line a cost center; H3: a Pellwyn credit memo and a payment made twice and recovered; H4: autumn 2023 and spring 2026 lines on the same cost centers | the ledger (posting_date, cost_center, source, document_no, po_number, amount, line_description), the calendar, the plan, the five score files for the denominators; 8 files, 16 columns | every accrual and the reversal out (the uniform rule the 2024 pairs suggest): 43.29, 94.50, 14.85, 18.89, 10.74; every line kept, the reversal shared by minutes: 50.56, 98.37, 16.01, 24.96, 13.66; lines naming a trial examination only: 58.71, 16.25, 7.11, 29.01, 16.38; golden 52.07, 97.35, 16.18, 24.21, 13.69 | a financial system conversion that carries an accrued balance and a new system that relieves accruals at invoice match are what a city ledger holds across a cutover |
| B, the people who applied to each examination and each component's completion rate over the four, rates in per cent to two decimals | 9 | the attendance record each component carries (the plan, section 8) | the Commission weighs what each component costs the city in applicants | D3 and D7: the legacy system's mobile app stored dates of birth day first, read month first whenever both were 12 or under, and the new system's career fair batch upload did the same, so a person's two forms carry two dates of birth; a second form often carries a new email or a different number, and only joining on name and date of birth, on email or on name and phone gives one person each | H5: the spring 2025 legacy applications copied into the new system at go-live, some emails blank; H6: the autumn 2025 requisition took the lateral applicants after 4 August under the entry title; H7: times in UTC and applications after the closing time in autumn 2025; H8: forms never submitted; H9: people who withdrew and resubmitted | both tracking exports (posting or requisition, title, names, date of birth, email, phone, source, submitted, status, the officer question), the rules (Rule 2), the plan, the calendar, the five score files for the numerators; 9 files, 14 columns | name and date of birth only: over by 10 to 15 an examination; name and date of birth or email: over by 4 to 7; name and date of birth or name and phone: over by 3 to 4; email or name and phone: over by 11 to 19; laterals by title: autumn 2025 over by 32; no window: autumn 2025 over by 26; golden 2,141, 2,263, 2,058, 2,307 | two tracking systems across a cutover, a day-first app and a batch upload template, new addresses and numbers on a resubmission are what an applicant export holds |

- **Main population zero-counts.** No ask device or hazard sits in the score files, the crosswalk, the lists or the
  gradebook: the call computed from those files alone equals the golden, and the asks read the ledger and the
  tracking exports with the score files only for counts of who sat (asserted).
- **Hazard table.** H1 moves every A figure for a solver who keeps only lines naming an examination; H2 moves the
  written test, the oral board and the course; H3 moves the situational judgement test and every figure through 4410;
  H4 moves every A figure unless the calendar's days are used; H5 moves spring 2025 for a solver who adds the two
  exports; H6 and H7 move autumn 2025; H8 and H9 move every B figure for a solver who counts records or statuses.
- **Referee.** The plan files the WHAT for both asks (what a component's work cost the City, 4410 shared by minutes,
  the candidates who sat; a person counted once in each examination, submitted by the closing time, laterals out) and
  the rules file the closing time; no file says which accruals were reversed or relieved, or which forms are one
  person.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A cost per candidate (5) | each accrual paired with its invoice by purchase order and taken out with the 1 July 2024 reversal | 43.29, 94.50, 14.85, 18.89, 10.74 against 52.07, 97.35, 16.18, 24.21, 13.69 | miss |
| B applicants (4) | forms joined on name and date of birth or on email, the window in Eastern time, laterals out by the officer question | 2,147, 2,267, 2,065, 2,314 against 2,141, 2,263, 2,058, 2,307 | miss |
| B completion rates (5) | the same applicants as the base | 46.28, 44.99, 43.50, 44.26, 43.94 against 46.40, 45.11, 43.62, 44.38, 44.06 | miss |

Mirror leakage: 0.0 per cent of ask weight (the mirror, rung R1, takes the asks the same way and keeps none of the 14).
Pair ceiling: 28.5 (the cracker lands the call, 45 with instruction-following, and none of the 14 ask figures; the mirror 5 plus 7).
Measured by: `generator/cracker.py`, run on the cut pack after every change (checks.py runs it and asserts 0 of 14);
its other path (every line kept, the reversal shared; forms joined on name and date of birth or on name and phone)
also keeps 0 of 14.

## Build record

- **World.** Four administrations of 884 to 947 candidates who sat all five components and 89 to 111 who missed one
  or more (world.py, seed 270116): six latent standings with the 2023 rules' appointments (60 per cent written, 40
  per cent oral, five points for a veteran, the course's pass at 240 seconds, list order, passed over for background
  or declined) filling eight academy classes, 22 of the 787 pool appointees separating with an average at separation.
  The applicant draw (ATS_DRAW 11) keeps three or more pairs of forms in every examination that only an email, only a
  name and phone, or only a name and date of birth joins; the ledger draw (LEDGER_DRAW 17) keeps every cost per
  candidate a quarter cent or more from a rounding edge. Candidates who sat the online components were drawn on their
  own stream so the five sitting counts differ while the boards, the course and the appointments are untouched.
- **Pack.** 18 files: the Commission's rules, the trial plan, the calendar, the eligibility lists (3,183 listed),
  the crosswalk, Halvorsen's written test scores (4,069) and work style inventory (3,864), the oral board ratings
  (70,110, the spine), the course timing sheets (4,670 runs), Pellwyn's situational judgement scores (3,892, a sheet an
  examination), the academy gradebook (804 recruits, the new layout from class 25-3), the recruit handbook, both
  tracking exports (5,849 legacy forms, 5,030 new), the ledger (106 lines), the 2022 job analysis and the 2025
  campaign summary (the distractors), the contents list.
- **Gates.** checks.py 343 assertions (inputs, R1 to R3c, the ladder and the five licensed corrections, SF1 to SF15,
  the asks against the generator's truth with every stop missing, the identity graph exact, separation, the cracker
  at 0 of 14 and a pair of 28.5, the realism sweep, H21, the leak greps), verify.py 24 figures recomputed from the
  bundle alone with 0 disagreements, two builds byte-identical, target.zip from the final build, figures_check 30 of
  30, precut 51 checks, the H1 audit clean on target and golden, leak.py REVIEW (no LEAK), guard heart WARN (shape,
  Gate G and question form, answered at the draw), guard surface: five pairs promoted on card axes (task265, task139
  and task452 on gap, pattern and Gate G, task269 retired on gap and decision type, all answered by the card's
  differentiation lines) and task268 on prompt idiom at a surface of 0.100; no persona outside the card's two.
- **Renamed at stage 3.** The temporary staffing vendor (a real recruitment brand's name), the situational judgement
  vendor (Northgate, a real public-sector software brand) and two file names leak.py read as author vocabulary
  ("test_"); no figure moved.
- **leak.py REVIEW lines, each harmless.** Sweep 3: the rules, the plan, the contents list and the job analysis name
  the components the call keeps, as every document about the examination must; none ranks them. Sweep 4: the
  handbook, the rules, the plan, the contents list and the job analysis carry the examination's own nouns (written,
  academy, average, selection, criterion, appointments); none names a correction, a restriction or a selection
  model (the leak greps assert it).

## Tried and rejected

- Screens run at the draw on 2026-10-19 before this pairing, each set aside with its record: a yearly mean annualised against a continuous series where a monitoring network's missing months fall in one season (task245 teaches that gaps not at random are rebuilt from a shared driver); pooled-test prevalence, the minimum infection rate against the likelihood estimate (task188); distance sampling, whose detection function is the textbook reflex on recorded distances and whose size-biased cluster mean repeats task264's lesson; onsets interval-censored between screenings (a fourth survival build in this lane after task265, task266 and task268, and the nonparametric estimate is not identified between a clinic's screens, so parametric forms disagree); within- and between-person separation in experience sampling (person-mean centring is the textbook reflex); change of support from sample to block grades (ordinary kriging into blocks is the industry's ordinary computation and its smoothing gives a third answer); compound aggregate tails (the severity form decides the percentile); latent means under measurement invariance (the sum score is the ordinary computation of a group's level, a WHAT fork); a design effect carried through the intra-cluster correlation (task269 v1's decision-study lesson, landed); anchor-test equating (the anchor announces the design); roll-call ideal points (scaling forms and lopsided-vote cutoffs spread the median member).
- Range restriction with the appointments made on an old test outside the candidate set (screen, 2026-10-19): every candidate then indirectly restricted, but at realistic volumes the licensed corrections agreed with the truth in only about 80 per cent of draws.
