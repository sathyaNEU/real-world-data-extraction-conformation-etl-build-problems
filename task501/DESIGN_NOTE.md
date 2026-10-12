# task501 design note (architecture 4)

Private, never ships. Architecture 4 of the slot, re-rooted at stage 1 on 2026-10-12 after architecture 3 (the 2027
standby facility a Swiss pension foundation elects from expected capital calls) was spent at stage 4 on two failed judge
passes, both model-choice splits under the call (an unfiled fit window, then the remaining funds' call-rate base).
Architecture 2 had landed on the portal (a filed walk-forward executed by both responses) and architecture 1 was retired
on the client's rules (a hidden recycling term). Their records are the lines of `## Tried and rejected`; their files are
gone from the folder and live in git history. Carried forward from all three: the method that decides is forced by the
data's structure and never filed, every competing model is computed at design time and either lands on the golden bin or
is refused by a shipped sentence, and nothing in the pack names the step that decides. The re-root is a new domain, world
and driver (Epidemiology & Public Health); the author's brief asked for a fourth architecture rather than retirement
(precedent task130 and task180).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task501.json` (v4), registered 2026-10-12. `guard.py check`: WARN
  overuse.shape (07 in three of the last twelve: task447, task180 and this slot's own v3), answered: the grid here is
  scenario by winter figure, the native unit of a catch-up appraisal, where task447 graded claim cells and task180 plant
  quarters. NOTE test.same_driver_older (gap population, G16, method_or_model_selection) differentiated in the card
  against task104 (a self-adapting scorer replayed), task134 v1 (a competing-exit horizon probability) and task70 v2 (a
  per-record date under a class-conditional cut). Nearest driver 0.05 (task95).
- **Pairing:** Epidemiology & Public Health, task type `infectious-disease-transmission-modeling`, objective Forecasting &
  Predictive Modeling. The call is which one autumn 2027 MMR catch-up keeps measles' reproduction number in the region
  below one through winter 2027-28, a window not yet open, or whether none is needed: a forward value the field computes
  from the supplied immunity, population and contact data. Client rigor pattern
  `epidemiology-public-health/infectious-disease-transmission-modeling/2` (R is the next-generation matrix's dominant
  eigenvalue and interventions act on it; the client's pin is a contact matrix, age parameters and R per scenario).
- **Stakeholder, forum, forcing event:** Oriel Health Region's regional immunisation manager (role `programme_officer`,
  org `hospital_or_health_provider`) prepares the director of public health's recommendation to the executive management
  team (forum `executive_team`), which on 21 July 2027 funds at most one catch-up for September to November 2027.
  Forcing event `incident_or_complaint`: an imported measles case in April 2027 (a 31-year-old who attended a GP surgery
  and the emergency department in Navan) with two secondary cases in adults, after which the director asked for options.
  The incident points at adults, a reflex that lands wrong, and ranks no option.
- **People** (`guard.py names --geo Ireland --seed 501`): Eadaoin Bonner (regional immunisation manager, author of the
  options paper), Nigel Macmillan (director of public health, signs the planning standard), Therese McGann (surveillance
  scientist, the case export), Karl McLoughlin (register data manager, the extract notes). None is in the prompt.
- **Shape 07 (grid of cells):** six scenarios (no catch-up, options A to E) by the winter's reproduction number, the call
  on top (1 + 6); the deck's call slide and its chart of the six reproduction numbers against one (3); the asks per option:
  the register's residents born in its years, how many of them have no valid MMR dose and how many exactly one, the
  confirmed measles cases since 2019 in its years and the imported among them (5 options by 5 = 25); the two files (2).
  About 37 criteria, none stacked from simple asks.
- **Gap and generators:** gap population first (the region is not one pool; who meets whom decides the threshold), then
  time (the cohort the 2010-12 scare left exposed reaches the teenage band by the winter). G16 (the method the contact
  data forces), G13 (the cohort ageing into the band where mixing is densest), G6 (the composition of the susceptible pool
  by age). Gate G `method_or_model_selection`: two methods turn the same immunity into a reproduction number, and the
  survey's structure forces the eigenvalue. Strategy `other` (transmission structure); none of the listed strategies is
  honest. Calibration organ none.
- **Mechanism:** R = rho(q diag(s) C), where C is the national survey's contact matrix (mean daily contacts by participant
  age group and contact age group, corrected for reciprocity), s each five-year group's susceptible share on 1 January
  2028 (the national profile's per cent immune by year of birth, weighted by the department's projection of residents by
  year of birth), and q = 15 / rho(C), so that a wholly susceptible region has the standard's R0 of 15. Each option takes
  the options paper's expected people made immune off the susceptibles of its birth years. Built (generator, survey
  seed 9024): 94.6 per cent immune, R0 times the susceptible share 0.81, the contact-weighted share 0.88, the
  eigenvalue 1.31; options A 1.29, B 0.89, C 1.31, D 1.30, E 1.30.
- **Data-native sentence:** the 2008-2012 birth cohort, whose MMR uptake fell in the region's 2010-12 scare, is 15 to 19
  years old on 1 January 2028, the ages whose contacts the national survey shows falling mostly on each other, so the
  winter's reproduction number is set by how susceptible that group is and not by the region's average immunity.
- **World:** Oriel Health Region (counties Louth, Meath, Cavan and Monaghan; about 538,000 residents projected at 1
  January 2028; EUR). Its regional immunisation register holds MMR records from 1993; GP returns, the school
  immunisation team's sessions, hospital clinics and records from abroad feed it. A 2010-12 scare cut MMR uptake in the
  2008-12 births to 89 to 92.5 per cent immune; the 1990-97 births, schooled before the second dose moved to junior
  infants, sit at 86 to 93 per cent; the 2013-17 births recovered to 92.5 to 94.5 per cent. The national immunisation
  office's profile (May 2027) gives per cent immune by year of birth projected to 1 January 2028; the National Social
  Contact Survey 2023 gives the contact matrix; the national notifiable disease system (NDS, live from March 2021)
  holds the region's measles cases, including the 2019 outbreak's.
- **As-of:** the options paper is dated 9 June 2027; the register extract is at 30 June 2027 (run 3 July); the case
  export runs to onsets on 30 June 2027 (5 July); the executive team sits on 21 July 2027.
- **Sources read, one line each:** the client pattern /2 teaches that interventions act on the eigenvalue; here the
  intervention removes susceptibility from one cohort and the shortcut is the population-average susceptibility, not a
  population-weighted contact cut. `guard.py mechanisms --objective forecasting --gate-g method_or_model_selection` (11
  builds): corpus-recovered rules (27, 29, 30, 78), censored delays (99, 31), a slowest sub-unit (52), an anchor
  convention (55), rationed demand resubmitted (108), a conversion hazard by time since entry (134), a variance under
  asynchronous timing (135); none uses a transmission structure, and this draw spends the dominant eigenvalue of a
  who-infects-whom matrix. `guide-to-prompt` exemplars for depth only.
- **Abstraction test:** without nouns the driver is a chain process whose threshold is set by the dominant eigenvalue of
  a structured transfer matrix, so removing propensity where the structure concentrates moves the system across it while
  every average says it is already below; the three nearest drivers (task95, a two-class weighted conversion; task15, two
  corrections to a hold; task87, a cohort rebuilt from a second record) share no latent structure, default path or
  correction.
- **Same-puzzle test:** gap population, pattern none, decision pick_one_of_n: no build in the last twelve carries all
  three (guard PASS), and against the slot's lineage v1 (rule, B, binding_constraint), v2 and v3 (time-first forecasts
  of capital calls) differ in gap, mechanism and domain.

## Default path

1. Read the planning standard: the aim is a reproduction number below one through the winter, R0 is 15, the winter is
   assessed on 1 January 2028, immunity comes from the national profile, and an option counts for the people the options
   paper expects it to make immune.
2. Join the profile (per cent immune by year of birth) to the projection (residents at 1 January 2028 by county, age and
   year of birth): 538,039 residents, 29,096 susceptible, 94.6 per cent immune.
3. Compare with the herd immunity threshold for R0 15 (1 - 1/15 = 93.3 per cent), or equivalently take the reproduction
   number as R0 times the susceptible share: 15 x 0.054 = 0.81.
4. Apply the standard's choice rule (no catch-up when the reproduction number without one is below one): no catch-up is
   needed, and every option lowers the figure further (A 0.79, B 0.76, C 0.79, D 0.76, E 0.73).

Ends on: no catch-up needed (reproduction number 0.8 without one)
Golden: option B, the catch-up for those born 2008-2012 (reproduction number 1.3 without a catch-up, 0.9 under B, 1.3 under every other option)

## Stump sentence

A competent solver joins the immunity profile to the population projection, finds the region 94.6 per cent immune on 1
January 2028 against the 93.3 per cent measles at R0 15 needs, puts the reproduction number at 0.8 and files that no
catch-up is needed; the step that lands it there is treating the region as one well-mixed pool, when the national contact
survey shows the 15-19-year-olds' contacts falling mostly on each other, so the next-generation matrix's dominant
eigenvalue is 1.3 and only the catch-up for those born 2008-2012 brings it below one (0.9).

## Three rules

- **Domain test:** the deciding quantity is measles' reproduction number for winter 2027-28 under each option, which
  infectious-disease epidemiology computes as the dominant eigenvalue of the next-generation matrix built from
  age-specific susceptibility and a social contact matrix; with another field's nouns there is no transmission between
  age groups, no contact survey and no susceptibility left by a vaccine history, so the task stops making sense.
- **Analyst test:** a strong analyst who reads every dose, validity rule, profile basis and survey table right and
  compares the region's immunity with the herd immunity threshold, or computes R0 times the susceptible share (0.8), or
  weights each group's susceptible share by its contacts (0.9), files that no catch-up is needed; one who ranks cohorts by
  their immunity gap targets the 30-34-year-olds (D), or the most people made immune (E); none of them brings the
  reproduction number below one.
- **Layer 1:** realistic mess across the pack, none of it on the call's path as a decider: immunity by year of birth
  against contacts by five-year group, joined through a projection that carries both; a survey matrix published by
  participant row and contact column, corrected for reciprocity on the national population; options by birth years and
  setting; a register extract loaded as received from GP returns, school sessions, hospital clinics and records from
  abroad; GP return lines queried and corrected or withdrawn in a separate log; local health office codes revised on 1
  July 2024 with one retired code reassigned to another region; a surveillance system migrated in March 2021 with the
  2019 outbreak back-entered to its outbreak module; laboratory results keyed to case numbers; an extract run three days
  after its as-of date.
- **Layer 2:** the field's method for a structured population's reproduction number (client pattern /2): the shortcut a
  capable analyst takes is the population-average immunity against the herd immunity threshold (R0 times the
  susceptible share, or a contact-weighted share), which an expert rejects because the survey shows the region does not
  mix at random; the rigorous method, the dominant eigenvalue, is the only one consistent with every shipped fact.
- **Stump class:** analytical. The decisive step is choosing the estimator the data's structure requires; no plant, no
  field read, no filed rule decides, and every rule in the pack (R0, the aim, the assessment date, the immunity source,
  an option's effect, the choice rule) is executed the same way on the default path and the golden.

## Readability screen

Rungs as climbed (Ladder). The six tests: 1 a filed sentence names the decisive quantity or sends the solver looking;
2 a column, key or marker makes it a predicate or a header-found join; 3 an opponent reflex; 4 a control or corpus
scores the methods or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of a
reported figure.

| Rung (the step that refuses the rung below) | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R1: weight each group's susceptible share by its contacts (refuses R0's even mixing) | no sentence names contacts or mixing | the survey workbook is one file of means | reweighting is a reflex | none | no | one weighted mean | readable |
| R2: rank the option cohorts by their immunity gap or by people made immune (refuses "no catch-up" from averages) | no | per-year immunity and people made immune are columns | ranking by gap is a reflex | none | no | a sort | readable |
| R3 (decisive): the dominant eigenvalue of the next-generation matrix, contacts by group times each group's susceptible share, scaled so a wholly susceptible region gives the standard's 15 | no sentence names an eigenvalue, a next-generation matrix, mixing or a threshold method; the standard names the reproduction number and R0 only, and the survey's notes say what was measured and how it was weighted | no column, key or flag; the matrix is a table of means by age group | not an opponent default (its reflexes reweight and rank) | no control scores the methods: no published reproduction number, no age-specific threshold, no outbreak model, and the case export is not read by the call | the battery never touches it | an eigenvalue of a 15 by 15 matrix | silent |

The screen on the decisive rung holds because the pack's only sentences about the quantity are the standard's aim and
R0 definition, which read the same under both methods; the survey is a national publication and names no use. The
pitfall is the field's own: herd immunity thresholds are taught as 1 - 1/R0 against average immunity.

## Semantic fork table

One row per term in the main ask and per convention the main computation needs, and SF17, the one ask convention the
stage-4 judge found open. The stump (the estimator of the reproduction number) is not a reading and has no row: both
methods compute the same literal estimand, and only the survey's structure separates them (Literal reader).

| SF | Term or convention | Golden reading | Alternative and the call under it | Ruled out by |
|---|---|---|---|---|
| SF1 | R0 of 15 | the reproduction number at full susceptibility, so the matrix is scaled by 15 over its dominant eigenvalue | 15 as the transmission of an average person (scaled by 15 over the population's mean daily contacts): 1.6 without a catch-up and 1.1 under B, no option below one, the choice rule's fallback names B (same call, figures off) | standard 3.2, "the reproduction number measles would have in the region if nobody in it were immune"; under the alternative that number is 18.0 |
| SF2 | winter 2027-28 | the region as it stands on 1 January 2028 | another date in the winter: no projection or profile ships for it | standard 3.3 (1 January of the winter's second year); same call |
| SF3 | immunity | the national profile's per cent immune by year of birth | immunity rebuilt from the regional register's doses, or read from the national quarterly uptake report | standard 3.4 (the national immunisation office's latest profile for the region); the uptake report covers 2022-25 births only |
| SF4 | year of birth against age | the projection's own year of birth for each age at 1 January 2028 | age read as at 31 December 2028 | the projection file carries both columns (C1); same call |
| SF5 | survey matrix orientation | participant rows, contact columns, as published | read transposed | same call and the same eigenvalue for a reciprocal matrix (C1, asserted) |
| SF6 | the survey's population | the matrix as published (reciprocal on the national population) | re-corrected for reciprocity on the region's projection, or density-adjusted to the region's age structure | same call, every reproduction number within 0.01 and in its bin (C3, asserted) |
| SF7 | a group's susceptible share | susceptible people over people in the group, by the projection | a plain mean of the group's years | same call, within 0.01 (C3, asserted) |
| SF8 | the open 70+ group | the survey's 70+ against the projection's 70 and over | 70+ split or dropped | dropping the group moves no figure by 0.005 (C3); same call |
| SF9 | an option's effect | the options paper's expected people made immune, off the susceptibles of the option's birth years, E as the paper splits it between 1993-97 and 1998-2002 | spread over a group in proportion to population, or E's split recomputed | standard 3.5; same call, within 0.005 (C3, asserted) |
| SF10 | people made immune | previously susceptible people who become immune | doses given | the options paper's note to its table |
| SF11 | stays below one | strictly below one | at or below one | no scenario within 0.09 of one (C1); same call |
| SF12 | or is no catch-up needed | none only when the reproduction number without one is below one | none read as "nothing works" | standard 3.6 (otherwise the option bringing it lowest, reported to the national office); same call |
| SF13 | infants born 2027 | the profile's 50.0 per cent | wholly susceptible | the profile states the share; same call, within 0.01 (C3) |
| SF14 | more than one option below one | the cheapest | the lowest reproduction number | standard 3.6; only B is below one (C1) |
| SF15 | rounding | one decimal on the unrounded figure | rounding the inputs first | the profile's one-decimal per cent and the matrix's two decimals are the inputs; every figure at least 0.03 from a rounding edge (asserted) |
| SF16 | the region | the four counties' residents in the projection | the register's residents | standard 3.3 (the region's population); the register is not a population count |
| SF17 | Ask 2: a GP return line under a query | the line stands unless the query log shows it replaced or withdrawn | a line whose query is still open read as not standing: as built at stage 3, six confirmed queries were open at the pull and three sat on loaded events in the option cohorts, moving C none and one by 1 and D and E one by 2 (judge-task501c) | closed in the data, C1: the register chased every query still open when the 30 June extract was prepared, so each carries its outcome and a closing date by 30 June 2027 (the six confirmed as sent, closed 11 to 30 June), and dropping every line not closed as confirmed by then moves no figure (asserted in checks.py and verify.py) |

## Ladder

Measured on the built pack (generator/callmodel.py on the shipped files; asserted in checks.py).

| Scenario | R0: R0 x susceptible share | R1: contact-weighted share | R2: the option cohort's immunity, people made immune | R3: eigenvalue (golden) |
|---|---|---|---|---|
| no catch-up | 0.811 | 0.879 | | 1.311 |
| A born 2013-17 | 0.788 | 0.843 | 95.0 per cent, 820 | 1.291 |
| B born 2008-12 | 0.763 | 0.801 | 88.8 per cent, 1,740 | 0.888 |
| C born 2003-07 | 0.792 | 0.860 | 93.5 per cent, 700 | 1.305 |
| D born 1993-97 | 0.756 | 0.822 | 85.7 per cent, 1,980 | 1.302 |
| E born 1993-2002 | 0.731 | 0.797 | 88.9 per cent, 2,890 | 1.298 |

- **Rung 0 (default):** R0 times the susceptible share, 0.8: no catch-up needed. Dies to the survey's Table 2: the
  region does not mix at random (the 15-19-year-olds' contacts fall 55 per cent within their own group, against the
  group's 6.6 per cent of the population), so the average is not the threshold quantity.
- **Rung 1 (the obvious correction):** each group's susceptible share weighted by its share of all contacts, 0.9: still
  no catch-up, and E ranks first among the options. Dies to the eigenvalue: a weighted average still lets every
  susceptible meet every group, while the teenagers' susceptibles meet each other.
- **Rung 2 (the sophisticated wrong one):** the option cohort with the widest immunity gap (D, 85.7 per cent) or the
  most people made immune (E, 2,890): a catch-up for the adults. Dies to the eigenvalue: D and E leave it at 1.3.
- **Rung 3 (decisive):** the eigenvalue: 1.3 without a catch-up, 0.9 under B, 1.3 under A, C, D and E. B is the
  only option below one.
- **Margins:** B's 0.888 against the next option's 1.291 (A); B 0.112 under one; every other scenario 0.29 or more
  above it. Flip condition: B would have to make fewer than 1,166 people immune (the paper expects 1,740) for its
  reproduction number to reach one.
- **Position and dominance:** on rung 0 every scenario is under one and B is third among the options (E 0.731, D
  0.756, B 0.763); on rung 1 E is first; on rung 2 B is neither the least immune nor the largest; only rung 3
  reverses the ranking, and no correction short of it puts any scenario above one or B first.
- **Grid:** the cells are method by scaling by matrix treatment by share weighting by allocation: every cell with the
  eigenvalue and the R0 scaling lands on the golden bins (16 family members, largest move 0.006, nearest member 0.033
  from a rounding edge); every cell with the average or the weighted average files no catch-up at 0.8 or 0.9; the
  eigenvalue with the mean-contacts scaling files B with 1.6 and 1.1 (refused by SF1, 18.0 at full susceptibility).
  No cell files a wrong option below one.
- **Worth, on the graded name and the graded figure separately:** the call (B against none) and all six reproduction
  numbers move with rung 3; nothing short of it gets any of the seven, and no lower rung files B's 0.9 (rung 0 0.8,
  rung 1 0.8).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the region's residents on 1 January 2028, all ages, those born in 2027 included at the profile's share | standard 3.3 with the projection; C1 |
| 2 | Unit of account | a person; the reproduction number is per case | the profile is per cent of persons, the projection persons |
| 3 | Attribution window | winter 2027-28, assessed on 1 January 2028 | standard 3.3 |
| 4 | As-of dating | profile projected to 1 January 2028, projection at 1 January 2028, the catch-up delivered by November 2027 | the profile's title, the projection's title, the options paper's timetable |
| 5 | Version basis | the May 2027 profile, the one shipped | standard 3.4 (latest profile); one edition ships |
| 6 | Denominator | susceptible people in a group over people in the group | SF7; C3 against the plain mean |
| 7 | Weighting | each year of birth by its projected people | SF7, C3 |
| 8 | Window length | no rate is estimated from a history | does not arise |
| 9 | Boundary inclusivity | strictly below one | SF11; nothing within 0.09 of one |
| 10 | Rounding path | unrounded eigenvalue from the published inputs, rounded once | SF15, asserted |
| 11 | Tie-break | the cheapest of several options below one | standard 3.6; only B (C1) |
| 12 | Maturity and censoring | the 2026 and 2027 births are projected by the profile | the profile's basis column; C3 |
| 13 | Order of operations | options act on susceptibles; the scaling comes from the full-susceptibility matrix | SF1 |
| 14 | Row order | no step depends on it | sums and an eigenvalue |
| 15 | Duplicate resolution | none on the call's path: one row per year of birth, per county and age, per group pair | asserted in checks |
| 16 | Identity normalisation | years of birth match between profile and projection; the survey's groups cover the projection's ages | asserted in checks |
| 17 | Netting against gross | none | does not arise |
| 18 | Dimensional units | per cent against share; contacts per day, absorbed by the scaling | SF1 |
| 19 | Code and status semantics | the profile's basis column describes, never changes a value | the profile's notes |
| 20 | Integerisation | people made immune are whole numbers as filed; nothing else is integerised | the options paper |
| 21 | Clause scope | standard 3.6 covers the year's one catch-up | the standard |
| 22 | Forward window contents | the winter's population and immunity are filed for 1 January 2028; the options' effects in the paper | the projection, the profile, the options paper |

## Literal reader

Executed word for word: the prompt asks which option keeps measles' reproduction number in the region below one through
winter 2027-28, or whether none is needed; the standard fixes R0 with its definition (3.2), the assessment date (3.3),
the immunity source (3.4), an option's effect (3.5) and the choice (3.6); the survey supplies how the region mixes. Every
reading of every term is a row of the fork table and lands on B or is refused by a quoted sentence. The default's figure,
R0 times the susceptible share, is the same estimand computed under random mixing, which Table 3 contradicts (the
15-19-year-olds' contacts with their own group are several times that group's population share), so it is the easy
method on the same literal estimand, not another reading of it. Re-run on the finished pack at stage 3 (Build record).

Method (the stage-4 judge's optional pin, declined): nothing names the age-structured method because the data forces
it, since Table 2's contacts by five-year group, the profile's immunity by year of birth (PS-07 3.4), the projection by
age and year of birth on the assessment date (3.3) and R0 defined for the region with nobody immune (3.2) are used
together only by the eigenvalue, R0 times the average share leaves Table 2 unread, and a pin would file the decisive
step as a rule to execute.

## Oracles

- The options paper's people per option, estimated susceptible and expected people made immune: inputs every method
  uses the same way; they confirm no method.
- The profile's basis notes (serosurvey, uptake, projection): describe the per cent immune; no reproduction number.
- The survey's Table 1 (participants and the national population used for the correction): needed only by a
  re-correction (SF6); no reproduction number.
- The standard: R0 and the aim; no threshold computed, no immunity target by age.
- The national quarterly uptake report (distractor): uptake for 2022-25 births; no reproduction number.
- No published reproduction number, age-specific immunity target, outbreak model or past catch-up evaluation ships, so
  nothing ties only under the golden or only under the default, and none of the case data reaches the call.

## Ask sheet

The main call's declared row population: the profile's rows, the projection's rows, the survey's Table 1 and Table 3,
the options paper's table and the standard. Device and hazard rows in it: 0 (asserted by file: no ask reads a call file
and the call reads no ask file). The asks read the register extract (people and MMR events), the GP returns query log,
the local health office code list and the 2024 revision circular, the register's extract notes, the national
guidelines' MMR chapter excerpt, the case export, the laboratory results and the case export's field notes. Each ask is
a measure every option carries that the call does not turn on, or a reconciliation of a call input (H18 home); none is
keyed to the call, its construction or the option recommended; the three share no primary device and no primary file.
No sentence in the pack adjudicates a device: each is found only by an inconsistency across files.

**Ask 1. For each option, the people born in its years whom the register holds as living in the region at 30 June 2027
(5 whole numbers).**
- H18 home: an input the call consumes (the projection's people by year of birth) reconciled to another system's total,
  the gap made of the device; use: the deck shows how many of each cohort the register can invite.
- Construction: the register's people extract by year of birth, with each person's local health office read in the
  code scheme in force when it was recorded, kept where that office is in the region.
- Primary device (D7 codes reissued, with D2 a label stored before a silent switch): on 1 July 2024 the national
  revision merged LH27 Monaghan West into LH26 and gave the code LH27 to a new Portlaoise area in the Midlands; the
  register did not recode, so LH27 recorded before July 2024 is Monaghan West (in the region, 3,437 rows) and LH27
  recorded after it is Portlaoise (people who moved away, 273 rows). Only the `lho_recorded` date (a column the natural
  path never reads) with the circular finds it; no code is unmatched and nothing flags the rows. Every figure moves.
- Hazards: people who moved away untransferred (out-of-region codes; the extract notes say an active registration
  closes only on death or a completed transfer).
- Span (4 files, 6 columns): people extract (date_of_birth, lho_code, lho_recorded), code list (lho_code, health_region),
  circular, extract notes.
- Stops (measured, asserted): the current code list (the cracker) A -758, B -751, C -669, D -666, E -1,259; every LH27
  read as Monaghan West +55, +56, +52, +56, +110; every active row counted +866, +861, +1,674, +2,200, +4,141; golden
  35,346, 33,217, 29,398, 30,625, 57,865.
- Realism: national code revisions reuse retired codes, and a register keeps the code it set when an address last
  changed.

**Ask 2. For each option, how many of those residents have had no valid MMR dose and how many exactly one (10 whole
numbers).**
- H18 home: a second measure every option carries (its invitation list: people with no valid dose need two, people
  with one need one), on which the call does not turn; use: the delivery load per option in the deck.
- Construction: the register's MMR events re-pointed through the merge table to the registration each now belongs to,
  without the events loaded from GP return lines the query log shows replaced or withdrawn, counted for Ask 1's
  residents under the guidelines' 12.5 (on or after the first birthday, at least 28 days after the previous dose) up to
  30 June 2027.
- Primary device (D1, a resubmission that opens no second case): the register loads every GP return line as received;
  when the immunisation office queried a line and the practice sent a replacement (the dose keyed to a sibling, or a
  wrong date) or withdrew it (sent in error, or a dose already returned), the original line stays loaded as a dose. The
  log's `outcome` and `replaced_by` against the events' `source_ref` (a column the natural path never reads) find it.
  Every figure moves (none 5 to 11 low, one 3 to 20 low).
- Second device (D7, the true key in a prior-id chain): 3,945 duplicate registrations were merged (23 of them in a
  chain of two merges); the register records the merge and leaves each event on the registration it was loaded to, so
  the events of a retired registration do not join the active extract, where 22,358 events of transferred, deceased and
  retired registrations already fail to join for an ordinary reason. Joined directly, every figure is high (none 15 to
  39, one 495 to 1,031); one merge followed and the chain left, the one-dose counts stay 2 to 8 high.
- Over-cleaning half: lines queried and confirmed as sent are real doses; dropping every queried line puts every figure
  high (none 10 to 21, one 9 to 134).
- C1: the guidelines' interval read from the previous valid dose or from any previous dose gives the same count for
  every person (asserted); no dose sits within three days of a first birthday or 24 to 32 days after another.
- C1 (SF17): every query in the log has its outcome and a closing date by 30 June 2027, so a line under an open query
  never arises and keeping or dropping one moves no figure (asserted).
- Hazards: Ask 1's LH27 device (the population); infant doses from the 2014 outbreak response (before the first
  birthday, the guidelines' rule, seen and repaired right); a school-team dose keyed again by the GP from the card within
  28 days (the interval rule); pharmacy doses dated 1 and 2 July 2027 in the 3 July run (the as-of); four school
  sessions loaded twice under fresh event numbers (a re-sent batch).
- Span (7 files, 12 columns): events (person_number, date_given, source_ref), merges (retired_number,
  surviving_number), query log (line_ref, outcome, replaced_by), people extract (date_of_birth, lho_code,
  lho_recorded), guidelines excerpt, extract notes, code list.
- Stops (measured, asserted): the cracker (every loaded event joined directly) none +9 to +29, one +492 to +1,021 in
  every option; merges followed, queries ignored, none and one 3 to 20 low; every queried line dropped, every figure
  high; the current code list on the population, every figure 58 to 257 low; golden as in figures.json.
- Realism: GP payment returns are corrected by replacement lines and an append-only load keeps the line it replaced;
  registers record merges in a table and resolve events through it.

**Ask 3. For each option, how many of the region's confirmed measles cases with rash onset from 1 January 2019 to 30
June 2027 were born in its years, and whether any and if so how many of them were imported (10 whole numbers).**
- H18 home: a measure every option carries (its cohort's recent measles), on which the call does not turn; use: the
  deck's activity panel beside each option.
- Construction: the case export's confirmed cases with onset in the window, one per person and illness, by year of birth
  and importation status.
- Primary device (D1, the same records under two key schemes, with D7 the true key in a reference string): the system
  migrated in March 2021; in May 2021 the outbreak team back-entered the 2019 outbreak's 32 confirmed and probable cases
  into the new outbreak module from its line list, so each is in the export twice, once migrated (legacy number in
  `legacy_ref`) and once back-entered (the legacy number only inside `comments`, beside benign comments that also
  mention line lists and legacy numbers). Some back-entries carry the notification date as onset (6 to 11 days later)
  and eight carry a date of birth with day and month swapped from the line list; the year never moves. Only the
  comments, or the laboratory file (no specimen on a back-entry), find them. Every figure moves.
- Over-cleaning half: a twin pair in the 2024 outbreak (born 2010, same sex, the second epi-linked to the first, onsets
  12 days apart) merges under a date-of-birth-and-sex de-duplication; no key de-duplication lands any figure, because
  the swapped dates of birth survive every key and every option holds one.
- Hazards: probable, possible and discarded cases (the classification, seen); confirmed cases with a hospital
  laboratory result and no reference-laboratory specimen (a laboratory-only count is low); import-related against
  imported (the field notes, seen).
- Span (3 files, 9 columns): case export (case_id, legacy_ref, onset_date, date_of_birth, sex, classification,
  importation, epi_link, comments), laboratory results (case_id), field notes.
- Stops (measured, asserted): every row counted (the cracker) A 15 and 3, B 14 and 3, C 16 and 4, D 15 and 4, E 24 and
  6; de-duplicated on date of birth and sex, or within 14 days of onset, 11/3, 11/3, 12/4, 12/4, 19/6; on date of birth,
  sex and onset 13/3, 13/3, 13/4, 14/4, 23/6; positive reference-laboratory result only, every confirmed figure low;
  golden 9/2, 10/2, 11/3, 10/3, 16/5.
- Realism: a migration keeps legacy records, and an outbreak team re-keying a line list into a new module is ordinary.

**Hazard table.**

| Hazard | Asks moved | Per-ask movement (measured) |
|---|---|---|
| LH27 recorded before and after 1 July 2024 | 1, 2 | Ask 1 every figure 666 to 1,259; Ask 2 every figure 58 to 257 |
| Replaced and withdrawn GP return lines | 2 | every figure 3 to 20 |
| Duplicate registrations merged, events left on the retired one | 2 | none 15 to 39, one 495 to 1,031 |
| Infant doses before the first birthday (2014 outbreak response) | 2 | A only |
| Pharmacy doses dated 1 and 2 July 2027 in the 3 July run | 2 | a few in C to E |
| Back-entered 2019 outbreak cases | 3 | every figure |
| Twins in the 2024 outbreak | 3 | B under a date-of-birth-and-sex de-duplication |

**Referee.** None needed: no designed disagreement between two systems is arbitrated by a third file.

**The cracker sheet.** The cracker landed B with the six reproduction numbers, ran the hygiene battery (keys unique, no
exact duplicates, every join matched, no fan-out) and executed every filed rule (the guidelines' validity rule, the
confirmed classification, the onset window, the as-of date):

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask 1, residents per option (5) | people born in the option's years whose code the current list places in the region | LH27 recorded before July 2024 is Monaghan West; the current list reads it as Portlaoise | miss |
| Ask 2, no dose and one dose per option (10) | valid doses counted on every event joined to the active extract | retired registrations' events never join, replaced and withdrawn return lines are still loaded as doses, and the population is Ask 1's | miss |
| Ask 3, confirmed and imported cases per option (10) | confirmed cases with onset in the window, by year of birth, each row a case | the 2019 outbreak is in the export twice under two key schemes | miss |
| Deck chart and call slide (recommendation block) | the six reproduction numbers against one | carried by the call, scored with the recommendation | outside |

The mirror sheet (the same response stopped at no catch-up) differs from the cracker sheet only on the recommendation
criteria, so no ask is coupled to the call.

Mirror leakage: 8 per cent of the ask weight (method credit on the ask paths, no figure).

**Pair arithmetic.** Planning weights 38 recommendation (the call, six reproduction numbers, the deck's call slide and
chart), 7 instruction following, 55 asks over 25 figures. With r = 5 (the chart and slide structure a wrong call keeps)
and each top response keeping about 8 per cent of the ask weight: C = 38 + 7 + 4.4 = 49.4 for the cracker, S = 5 + 7 +
4.4 = 16.4 for the mirror.

Pair ceiling: 32.9

## Prompt

`prompt.txt` (891 characters, voice-check.py exit 0): which one of the five options, or none; winter_measles_2027.xlsx
with the reproduction number without a catch-up and under each option, and per option the register residents, the no-dose
and one-dose counts, and the confirmed and imported cases; measles_readiness_2027.pptx with the call and a chart of the
six reproduction numbers against one; reproduction numbers to one decimal, people and cases whole, in the last sentence.
It names no method, convention, input file, standard or person. The case ask carries "whether any and if so how many of
them were imported" (H23).

## Build record

- **Generator** (`task501/generator/`): `world.py` the fixed facts; `callsim.py` the national population, the reciprocal
  contact survey, the regional projection, the immunity profile and the options paper's arithmetic; `callmodel.py` the
  next-generation matrix, the golden, the family and the rungs; `sim.py` the register (people, events, merges) and the
  surveillance records; `asks.py` the three asks and every stop; `pack.py`/`docs.py` the files; `golden.py` the two
  deliverables, figures.json and metadata.json; `writeup.py` renders submission.md from figures.json; `checks.py` (212
  assertions) and `verify.py` (independent, csv + openpyxl + pdfplumber) recompute; `build.py` runs it and the
  byte-identical rebuild.
- **Main call, built:** 538,039 residents, 94.6 per cent immune. Reproduction number without a catch-up 1.311 (R0 x
  susceptible share 0.811, contact-weighted 0.879), B 0.888, A 1.291, C 1.305, D 1.302, E 1.298; graded to one decimal
  1.3 / 1.3 / 0.9 / 1.3 / 1.3 / 1.3, each at least 0.033 from a rounding edge. B is the only option below one; nearest
  scenario to one is 0.112 away. The 16-member defensible family (matrix as published / transposed / re-reciprocal on
  the region / density-adjusted, times weighted / plain share, times susceptible / population allocation) moves every
  figure by at most 0.006 and keeps the call; the mean-contacts scaling gives 18.0 at full susceptibility, refused by
  standard 3.2 (SF1).
- **Asks, built:** Ask 1 35,346 / 33,217 / 29,398 / 30,625 / 57,865. Ask 2 (none, one) 3,542/4,724, 4,285/6,094,
  2,859/3,960, 4,971/7,302, 8,530/11,788. Ask 3 (confirmed, imported) 9/2, 10/2, 11/3, 10/3, 16/5. Every stop asserted
  in checks.py; the main call computes from its five files alone and is unchanged with both distractors deleted.
- **Free gates (2026-10-12, rebuilt after the stage-4 fix):** generator checks 212 PASS; verify.py PASS, the open-query
  reading included; two builds byte-identical (19 pack files, 2 goldens, figures.json); input gates 19 files, 5 formats
  (csv, docx, pdf, txt, xlsx), 278,746-row events extract, 2 distractors; figures_check.py exit 0 (57 figures); precut.py
  exit 0 (17 fork rows); voice-check.py exit 0; realism sweep in checks.py (no round or uniform counts, no method word,
  no library name, personas from the card, Table 1's populations distinct); golden-realism editing pass done at stage 3
  (goldens byte-identical since), containers scrubbed (audit clean); leak.py REVIEW (no LEAK), sweep 11 clean; guard.py
  surface 0 hard tells (two card-axis pairs promoted, below); guard.py heart PASS; freeze.py check --mode determinism
  PASS.
- **Stage 4 (2026-10-12):** the leak reader quoted nothing for questions 1 to 4 and its own reconstruction named B; its
  realism notes were fixed in the generator: the options paper lists option E on one row with its split in the note
  under the table, and 4.3 says invitation lists for the option funded will be drawn from the register (the paper cited
  no extract; 4.3 was its only register sentence); the survey's Table 1 publishes the statistics office's populations,
  Table 2 unchanged; the standard's revision note kept. The judge (judge-task501c) found the main call forced (B 0.89
  against 1.29 to 1.31) and one ask fork, three open GP-return queries on loaded events, closed in the data (SF17) with
  no graded figure moved (determinism_check_report.md); its optional method pin declined (Literal reader). Changed under
  target/: gp_return_queries_mmr_2005-2027.csv (six rows), mmr_catch_up_options_autumn_2027.pdf and
  nscs_2023_published_tables.xlsx; every other pack file, both goldens, figures.json and submission.md byte-identical.
- **guard.py surface:** task104 and task70 promoted on the card axes only (gap population, pattern G16, Gate G
  method_or_model_selection, the same-driver signature), both already differentiated on the card (task104 replays a
  self-adapting scorer, task70 dates a record under a class-conditional cut; neither uses a transmission structure); no
  byte, schema, seed, name or prompt overlap. The 3 personas in the cut pack are all the card's.
- **guard.py heart:** PASS at the stage-4 rebuild (WARN overuse.shape at stage 3, 07 in three of the last twelve,
  answered at the draw); nearest driver 0.05 (task95), nearest stump 0.04 (task253 v3); no BLOCK.
- **leak.py REVIEW lines, answered:** the options paper and the standard carry the committed call's distinctive words
  (option B, catch-up, measles, reproduction number) because they are the decision's own vocabulary, not the method; the
  standard names R0 and the aim only, the options paper the cohorts and people made immune, neither the eigenvalue or the
  contact structure (the generator asserts no method word in any file). The stump-term overlaps are domain words
  (immune, health, cohort, national, manager, population, standard) in documents that must use them, the uptake report
  (a distractor) included. The stock return's expiry dates run past the as-of because a stock count lists future
  expiries (H16 allow-list).

## Tried and rejected

- v2 architecture (2026-10-11): the walk-forward selection with its mechanics filed in s.5.3 and the buffer as the largest end-of-horizon shortfall; both portal responses executed the filed test and landed CHF 250 million. Retired the same day: a validation whose mechanics are filed is a computation to a strong solver. v3 keeps the test and moves the deciding quantity to the buffer's estimand.
- Candidate set including a trailing twelve-month basis at v3: persistence won the honest test whenever recent vintages paced faster than history; left out.
- Seasonality at 1.35 to 0.65 (first half to second half): the path and end-of-horizon buffers sat 5 to 20 million apart, inside one tranche; set at about 70:30, which puts them 35 million apart.
- Seed sweep 118 to 149 under the sharper seasonality: nine seeds meet the honest margin, the leaky margin and the path separation; 118 kept (the persona draw's seed).
- Reserve at 50, 60 and 70 million with the 25-million menu: the fit-once path-buffer cell or the end-of-horizon cell sat within three million of the answer bin's edges; 75 million puts the answer 12 from both edges and every single-error cell at least 4 from them.
- v1 architecture (2026-10-10): the unfunded commitment restored by recallable proceeds under a term no document stated, pinned by reproducing 180 audited cells; retired 2026-10-11 under the client's 10/10 rules as data semantics and a hidden rule deciding the call (rule 3), and as a backdrop domain under the noun-swap (rule 1). The world, the pack and asks B and C were kept; the recycling term is now filed in the register and the stump moved into the validation.
- Candidate set with a trailing twelve-month basis: persistence won the honest test whenever the recent vintages paced faster than history and landed on the answer tranche; dropped, the three bases are band, strategy and band, manager's own.
- Strategy-coherent pacing shifts in the recent vintages: the strategy-and-band basis then won honestly by 11 per cent and the full-window fit tied the pooled bases, so the leak crowned nothing; replaced by manager-level and fund-year noise, under which the manager's-own basis memorises the past (full window 2.9 per cent against 6.0) and loses forward (17.2 against 9.1).
- Buffer as the second-largest shortfall: the truth and the leaky cell sat within three million of tranche edges at every reserve from 55 to 80; the largest shortfall with a CHF 60 million reserve puts the truth 10.8 and 39 from its edges and every wrong cell at least 4 from its own.
- Pooled rates as the mean of per-fund-month ratios: a fund in run-off with a small audited NAV and one large exit produced ratios above one and dominated the band; replaced by the ratio of sums at the plan-date rate (RL-PM-04 s.5.2, 5.3), which is also what a treasury would write.
- Estimator as rate on unfunded commitment (the Takahashi-Alexander form): the naive and true rates partly cancel because the naive denominator is smaller by the same recallables, and the Gate G label would have moved off binding_constraint; kept the cap form, where the construction is inert unless the cap bites, and built heterogeneous pacing so the recycling funds are the fast deployers whose cap bites.
- Uniform fast pacing: every fund fully drawn by month 24, the later age bands carried no history and the cap never bit under any construction (all constructions on one tranche); replaced by per-manager pacing (fast credit deployers, slower buyout and infrastructure).
- Distributions credited at one half: the programme's run-off distributions swamped the calls and the required facility sat at one tranche for every construction; the directive credits one quarter.
- Age bands 37 to 48 and 49 to 72: the recycling funds straddled the thin fourth band in 2027 and the band rate was too small for the restored commitment to matter; bands set to 37 to 54 and 55 to 78.
- The 2026 prepayment wave drawn from loans funded from January 2024: a third of the wave exited in 2025 and sat inside the audited cells, so the audited roll-forward reproduced most of the answer; the wave is drawn from loans funded in 2025 and exits in 2026 only.
- Short holds from the ordinary hold distribution: the normal draws put exits under eighteen months in half the funds, so commitment less calls missed 96 of 178 audited cells and was not the empirically excellent basis L7 requires; ordinary holds now start above the convergence gap and only the designed quick exits, the two historical flippers and the 2026 wave are short.
- Recallable proceeds attributed to the audited year by realisation date: an exit on 28 December with a January notice put the proceeds in different years under the two readings (one cell unreproduced); attributed by notice date, and no realisation now falls after the 15th of December.
- Reserve at CHF 30, 45 and 55 million: the truth or a wrong construction sat within five million of a tranche edge; CHF 65 million puts the truth 11.1 and 13.9 from its edges and the three wrong bases 8 to 15 from theirs.
- Producer string "Treasury & Liquidity" on the board paper's container: the raw ampersand broke the core-properties XML and the file no longer opened; the deliverables are stamped with the organisation's name.
- Context artifact as the H2 2025 semi-annual report (30 June to 31 December 2025): its closing NAV column is the opening column of ask B, five golden figures in a shipped document (leak.py LEAK); replaced by the H1 2025 report, which shares no figure with any ask.

- Signature rule / B / method_or_model_selection (any decision type): guard BLOCK, spent in 12 earlier builds (test.same_driver_older) and task71 (test.same_puzzle_older). Relabelled honestly: the forward regime is the decisive gap (time first) and the cap at remaining commitment is the Gate G mechanism (binding_constraint).
- Driver variant "late-close equalisation" (a midway entrant's first draw equals the process's draw-to-date on its own size): nearest driver task107 at 0.09, kept out because the catch-up is stated on every real notice and the rule reduces to a readable term.
- Driver variant "notices netted by some counterparties": kept out because the gross lines exist on the notice file and the move collapses to a file choice.
- v3 first decisive step (2026-10-11 to 10-12): the walk-forward kept as a filed execution layer and the buffer read on the month-end path ("at any point in a horizon", s.5.6) instead of the horizon totals; replaced on paper at the 2026-10-12 redesign before any portal test: s.5.3 filed the whole method (rule application, the step v2's responses executed) and s.5.6 named the decisive quantity (readability test 1), and the v3 world also carried a CIO and a portfolio manager each arguing a wrong basis (licensed voices). The redesign files the estimand only.
- Decisive step candidates weighed at the redesign (2026-10-12): a subscription-line overhang (investments closed but not yet called) died on the battery (an unmatched join between holdings and calls is a work order); a quantile of the year's calls with cross-fund dependence died on determinism (a quantile from eleven years of programme history straddles bins under reasonable estimators); a curve conditioned on each fund's position died as task133's driver; seasonality of calls inside the year died as task32's and the first v3's. The deadline drawdown kept: silent, analytical, and forced by every closed fund's path.
- Prototype with the deadline group's investment periods ending April to August 2027 (scratch proto2): the group started drawing down inside 2026, so the default's 2026 back-test missed by 17 per cent on some seeds and a fund's own recent rate reached half the drawdown; the group's deadlines moved to September to December 2027 and the six-month drawdown now starts inside the facility year.
- Card codings with pattern E (time, E, forecasting) and with G14 or G7 decisive: guard BLOCK (spent in task117, task37, task44, task97; G14 in task124; G7 in task229); coded G6 (the composition shift on the deadline position), which the strategy (composition_mix) names.
- Commitment wave of 2024-26 vintages at up to CHF 170 million each (prototype 3): the programme's 2026 calls ran so far above 2027's that the run rate landed inside the golden's bin on one seed in two; the later vintages were cut to a steady CHF 60 to 120 million a year.
- An expected-calls figure, or the next amount down's uncovered amount, as a graded ask: both are method figures that move by several million across the golden family; the prompt asks for the fees at the two amounts, which are exact.
- The look-through holdings as the pack's only 25,000-row file (stage 3): it is a distractor, so the bulk file did no work for the solution; the reference rates now ship in the custodian's long form for every currency it quotes (33,968 rows), which the call and the ask both read.
- Composed-mishandling target "nothing that includes P1 keeps a figure": the parallel run ended in September, so a response that dates by the custodian's credits but keeps both records is right in the five Q4 items; extending the parallel run into the fourth quarter would need a portal manager's fourth-quarter notice in every strategy, which the quarterly income pattern does not give; accepted at 5 of 25 ask items and priced into the pair ceiling.
- One random stream for every observation draw: the year totals of the ask then disagreed with the sums of their rounded quarters (Buyout 95,971 against 95,972), a rounding-path fork; the 2025-26 distribution timings got a stream of their own and streams 0 to 39 were scanned with every assertion plus the one-rounding-path test; 11, 12 and 23 pass, 12 kept (largest stop misses).
- Term sheet with the commitment fee "per annum ... quarterly in arrears" and the 2026 amount running until the election: a day count and a pro-rata January each gave another year's fee; the fee is now a share of the amount for the availability period and the elected amount runs for the whole period.
- The custodian statement's columns glossed only as "booking date" and "value date": reading the day the cash arrived as the booking date moved 19 of the 24 ask figures (credits booked a business day late, six across quarter or year ends); the field notes now say what Valuta is.
- Names within a word of real organisations (a growth manager named after a real biotech's brand, an infrastructure manager sharing a common corporate name, a real fund administrator as a paying agent): renamed Gosford Growth Partners, Juneau Infrastructure Partners and Corvisart Equity Gestion SAS; no figure moved.
- Container times left to the writer and the house scrub: openpyxl stamps the build clock, which sits inside the fiction's band and changed every build (two builds were not byte-identical), and every PDF carried the extract's date and reportlab's "(unspecified)" creator; each document now carries its own created and modified times.
- The v3 world as first built (stage-4 judge, 2026-10-12, NOT_DETERMINISTIC on margin_or_boundary_fragility): the golden's CHF 326.6 million of expected calls sat 8.4 million (2.6 per cent) above the floor of the CHF 225 million bin while RL-PM-05 left the estimation period unfiled, so rates fitted from 2024 gave the judge CHF 312.3 million and CHF 200 million, and the closed funds' drawn-share range (91.8 to 93.8 per cent) alone moved the total 13 million. Repaired by filing the period in s.5.2 (the programme's whole history since 2015) and tightening the world: each fund's spread around the managers' aim at a period end from 0.45 to 0.15 points of commitment, the four funds' pace from 0.38 to 0.36 (Tessin 0.35), which centres the golden at CHF 329.3 million against a bin midpoint of 329.5.
- Closing the fit windows by the world alone (no filed period): the 2024-onward fit stayed under the bin's floor in every world tried, because from 2024 the four slow funds carry 45 to 61 per cent of the unfunded commitment in the age bands of one to three years; milder 2023-24 market factors (0.85 and 0.90) moved it by under a million and pushed the 2026 back-test past 5 per cent. The period is filed instead; the recent windows are recorded, not family members.
- The six on-schedule funds moved out of 2027 (vintages a year earlier, closed by the plan date): the post-deadline and catch-up-set spreads fell under 2 million, but the 2025 back-test of the default went to +11 per cent and the golden fell to 323.9; the six were kept. Shrinking them to 0.5 or 0.7 of their commitments, or moving their deadlines to May to August 2027, lowered the golden 5 to 9 million or took the 2025 back-test past 7 per cent; kept as they were.
- The four funds' paces swept from 0.33 to 0.38 with Tessin's commitment at 170, 174 and 178: 0.34 and lower pushed the 2026 calls (R0) above CHF 317 million, inside 7 million of the golden bin; 0.36 with Tessin at 0.35 keeps R0 9.0 million below the floor and the family's narrowest careful member 2.23 per cent inside.
- The post-period rate as the canonical treatment after a deadline: kept as a family member (2.49 per cent inside), because as the canonical it would leave the lowest drawn share and the 24-month bands 1.6 and 1.5 per cent above the floor.
- Restoring the September 2026 facility draw (the new world's calls left the account CHF 3.3 million above zero) by cutting the pre-October reserve level from CHF 35 to 30 million: it changes a figure the minutes state; replaced by an operating minimum of CHF 5 million below which the treasury draws the facility (drawn CHF 6 million on 18 September). The minutes no longer report the October repayment, which the 24 September sitting could not know.
- The timing-stream rescan on the old arrival draws (streams 0 to 39 with the full checks): the Growth Q2 cell sat 12 francs from a rounding edge in 16 of the 18 streams run because the stream never touched its credits, and none passed. The 2025-26 distributions' arrivals are now drawn on the timing stream; 2,000 streams were screened in memory for the one-rounding-path constraints, six passed, four of them the full checks, and 360 was kept for the largest stop misses (s2 97.6, s3 26.6).
- Architecture after the portal landed v2 (facility election from expected 2027 calls; period-end completion for the four slow funds): spent at stage 4. Pass 1 found margin fragility (a 2024-onward fit window gave 200); the repair filed the whole-history period and tightened the world. Pass 2 found a fork under the call that the period does not close: once the ten funds complete to 92.6 per cent at period end, the remaining funds' base (call rate on unfunded, 329, 225; on commitment, 349, 250) is not separated by the filed records or by back-tests. Two judge passes failed, so the architecture is spent.

- Re-root candidates weighed at the 2026-10-12 draw (architecture 4): a screening programme's second-round yield (task132's reset and the v3 abstraction of a stage reached), an excess-of-loss frequency leveraged by trend (task446's driver in other nouns, and its predicate reads), a left-truncated stock forecast (the default passes the solver's own back-test), multiregional gross migration flows (forks between flow definitions, a nowcast, a small effect), a rule-of-85 retirement forecast (a filed rule read, the death of v3), saturable binding in a PK model (a table lookup), correlated polling errors and swing models (forks), regression dilution (a magnitude, and the tag drifts to causal), a survey design effect (the Kish reflex lands it). Kept: the next-generation matrix for a measles catch-up, where the default herd-immunity comparison files no catch-up and every reflex lands wrong.
- First next-generation prototype (scratch ngm1): infants under one dominated the dominant eigenvector, so the deciding group was the routine programme's and no catch-up option mattered; the under-ones are folded into 0-4 at the profile's maternal-antibody share and infant contacts follow the survey's 0-4 row.
- World prototype 2 with the 2013-17 cohort at 92 to 93 per cent immune: the 10-14 and 15-19 groups carried the eigenvalue together and no single option brought it below one (B 0.95); with teenagers' contacts concentrated within about two and a half years of their own age and the 2013-17 cohort recovering to 92.5 to 94.5 per cent, B alone takes it to about 0.89 and A, the next, leaves 1.28.
- Reproduction numbers graded to two decimals: the reasonable treatments of the survey matrix (as published, transposed, re-corrected for reciprocity on the region's population, density-adjusted to the region) and of each group's susceptible share (population-weighted or a plain mean of its years) move them by up to 0.005, inside a two-decimal bin; graded to one decimal with every value at least 0.03 from a rounding edge.
- Doses loaded the same month they were given (early prototype): a GP line given on the 20th was loaded on the 13th, before it existed; the return is now made and loaded the month after the dose month, and any line not loaded by the 3 July run is out of the extract.
- Ask 2 interval read from the previous valid dose against any previous dose (stage 3): the two readings could split a count; the generator spaces every pair of doses outside 20 to 36 days and keeps none within three days of a first birthday, so checks.py asserts the two readings give the same count for every person (C1), and the interval device rides the GP card re-key within 28 days only as a hazard.
- Ask 3 back-entries dated by swapping day and month of the date of birth and shifting onset (built): a key de-duplication on date of birth, sex and onset catches only the back-entries that kept both; asserted that no key de-duplication (date of birth and sex, or plus onset, or within 14 days) lands any option's figure, so only the comments or the laboratory file separate the 2019 outbreak's two copies.
- A European monthly-case summary as the second distractor (built, then cut): it shared the measles noun with the case ask and added no weighing a solver would do; replaced by the cold-chain stock return, which a reader might open for delivery capacity and the solution never reads.
- Confirmed GP-return queries left open at the pull (stage 3 build): six were open on 3 July, three on loaded events in the option cohorts, and reading an open query as not standing moved C's none and one by 1 and D's and E's one by 2 (judge-task501c, competing_defensible_answer on Ask 2). The register now chases every confirmed query still open when the extract is prepared and closes it by 30 June with its outcome (SF17, asserted); no figure moved.
- A one-line pin naming the age-structured method (the same judge's optional fix): declined, because it files the decisive step as a rule to execute; the data forces the method (Literal reader).
- Option E on three rows of the options paper (its 1993-97 span, its 1998-2002 span, its total): the first restated D's row under E's label and read as a copy (leak reader, judge); E is one row and the note under the table gives its split, the same figures.
- The survey's Table 1 population as the national shape's group totals: each group read as its thousands times 1000.446 and two groups were identical (310,138), so the column read generated (leak reader); Table 1 publishes the statistics office's estimates on a stream of their own, Table 2 unchanged and still reciprocal on them to its rounding (asserted), the family's largest move 0.006 and nearest edge 0.033 as before.
