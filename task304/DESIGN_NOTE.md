# task304: where the charity's 2027 find-and-treat van works, and the people it starts on hepatitis C treatment there

Wave 6, Opportunity Sizing & Decision Support, perssathya. Architecture 2, drawn 2026-10-27 at a stage-1 re-root.
Architecture 1 (Calderbrook Building Society's 2027 financial support team, the first-time buyers' Charter term
extensions carried as a forbearance state) shipped 10-27 and came back on the portal's determinism block: the fork is
the stump (its lineage is on the card, its measurements in `## Tried and rejected`). The world moved from banking to
epidemiology under the same objective and number: the one in-world shape left was the probes' first move, and a second
build on a world the portal has seen risks a duplicate finding.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | epidemiology-public-health / screening-diagnostic-policy-evaluation (a case-finding programme placed where it finds the most people to treat; the task type serves Opportunity Sizing) |
| Objective | Opportunity Sizing & Decision Support: the headline is the people the van starts on treatment in 2027, built from the pool (each setting's 2027 intake) through tested, antibody positive and active infection to started, and the largest figure picks the setting |
| Decision / answer unit / question form | pick_one_of_n / count / where |
| Gap / pattern / generators | time, population / none / G6 (the antibody-positive pool's make-up moved from never-treated to cured), G3 (an antibody record that outlives the cure), G13 (a validating ratio from before the treatment push carried to 2027) |
| Gate G / strategy | forecasting / informative_censoring: the active share is observed only on positives who come forward for an RNA test, and the cured do not come forward, so the share the record shows is the never-treated share; each positive's cure has to be read from whichever organisation gave it |
| Layer 2 | field_method, own:active-infection-among-antibody-positives-after-curative-treatment |
| Forum / forcing event / org family | trustees_or_governors (the charity's trustees fund one van) / launch_or_rollout (the van starts in January 2027) / nonprofit_or_charity |
| Stakeholder | director of services at the charity (operations_director) |
| People (guard.py names --geo uk --seed 304) | Katie Reynolds, director of services; Robin Higgins, outreach team lead (ran the 2018-19 pilot); Clare Stevenson, consultant hepatologist and the network's clinical lead |
| World | a hepatitis C charity running peer testing and a find-and-treat van with an NHS hepatitis C operational delivery network in an English city and its county; four candidate settings the van has not worked: the probation approved premises (people on licence after prison), the city's homeless hostels, the drug and alcohol service's new entrants to treatment, and the community pharmacy needle exchange's new registrants; records to 30 September 2026 |
| Deliverables | van_2027_trustee_paper.docx (the call, the two figures per setting, the chart), van_2027_funnel.xlsx (the funnel and the clinic outcomes) |
| Guard | WARN only at the draw: overuse.objective (the lane's objective), repeat.gate_g (forecasting after task118 v3: a forward count the correctly read validating ratio does not pin, the honest key), repeat.decision (pick_one_of_n: the trustees fund one van and size it); test.same_puzzle_older and test.same_driver_older carry differentiation lines (task144, task268, task150, task179, task501) |

Axes redrawn at the check, each to the honest key the window left: the organisation from the NHS network
(hospital_or_health_provider, banned against task118 v3) to the charity that runs the van with it, which is who funds
and places a find-and-treat van in England; the forum from the network board to the charity's trustees, who fund the
van; the role from programme officer (task118 v3) to the director of services; the context artifact from register
(task464) to operations_log, the prison health provider's treatment log the call turns on; the strategy from
composition_mix (task118 v3) to informative_censoring, which names the mechanism more exactly: the RNA result that sets
the active share exists only for positives who come forward, and the cured do not.

Data-native sentence: the peer programme tests each setting's new arrivals for antibody, which stays positive for life
after a cure; the laboratory never repeats an antibody test on a known positive and the cured do not come forward for an
RNA test, so every RNA result the pack holds on an antibody positive is about someone never treated and shows about
three quarters viraemic; the network's register holds the courses its own clinics gave and the prison health
provider's log holds the courses given inside, and most of the approved premises' positives were treated inside.

Sources, one line each. `guard.py slots` on the mechanism's nouns (antibody, cured, treatment, register, RNA,
clearance): task171 (an antibody drug's clearance, pharmacokinetics) and task194 (a clearance register) only, neither
the insight; on the setting's nouns (hepatitis, HCV, outreach, hostel, needle, prison, drug): no slot. `measured-drivers.md`:
the held signature "the back-test passes by construction; the forward population differs on an axis the pack shows only
in another file" is the device, here carried by a second organisation's treatment record rather than by an
intervention's reach. `layer2-rigor-patterns.md` (screening-diagnostic-policy-evaluation, predictive value depends on
prevalence) gives the family; the pitfall is re-found from the data: an antibody count after a curative programme.
Forward facing: the van works calendar 2027 and the call is the people it starts on treatment in that year.

Prototype on clean truth (scratch, 20 seeds, person-level): R0 antibody positives and R1 positives at the validated
share both file the drug service entrants 20 of 20; R2, positives less the network register's cures, files the
approved premises 20 of 20; R3, positives less every cure in either record with the validated share on the rest, and
four standing variants (reinfection read from the laboratory or not counted, a course without a twelve-week result
counted cured or not, the pilot's ratio for the laboratory's) all file the needle exchange registrants 20 of 20, as
does truth; minimum clearance 1.21 (R3), 1.20 (R1), 1.17 (R2); the standing family's spread on the graded figure about
1.3 people on about 95; the RNA-positive share among tested intake positives sits at 0.70 to 0.81 in every setting.

## Default path

The strong analyst's route, every field read correctly and every filed rule applied (figures from the built pack,
seed 304230; people a year, rounded to the nearest ten as the prompt asks):
1. Take each setting's 2027 arrivals at the yearly average of its distinct arrivals in the two plan years to 30
   September 2026 (setting_arrivals_2023-10_to_2026-09.csv, as the van plan counts a year): approved premises 1,001,
   city hostels 1,005, Fenwold Recovery's new entrants 2,061, needle exchange registrants 494.
2. Take the van's rates from the 2018-19 pilot caseload: it tested 0.65 of arrivals and started 0.74 of the people
   with RNA detected within twelve weeks.
3. Take each setting's reactive share among the arrivals the peer team tested in the two years (the peer log joined
   to the arrivals by pseudonym).
4. For each reactive arrival read the network's own records before the test, the field's own subtraction: a course
   in the treatment register with a twelve-week result not detected means cured, Fenwold Pathology's latest RNA
   result decides where there is one, and anyone with no record carries the 0.74 the laboratory's first positives
   show (the pilot's 0.72 and the attending arrivals' own RNA results agree).
5. Multiply out: approved premises about 80 people started (75.0), needle exchange registrants about 60 (62.4),
   Fenwold Recovery's new entrants about 40 (42.9), city hostels about 40 (40.1).
Ends on: the approved premises, about 80 people started on treatment in 2027
Golden: the needle exchange registrants, about 50 people started on treatment in 2027 (53.4), Fenwold Recovery's new
entrants next at about 30 (29.8), once each positive's record is read from every organisation that tested or treated
them, Corvane Health's prison workbook (courses and reception tests) as well as the network's register and the
laboratory.

## Stump sentence

A competent analyst takes each setting's 2027 arrivals, the share the peer team found antibody positive, reads each
positive's status from the network's own treatment register and Fenwold Pathology's results, carries the rest at the
0.74 viraemic share the laboratory's first positives validate, and files the approved premises first at about 80
people started on treatment; the step that lands it there is treating the network's records as the record of every
cure, when 223 of the approved premises' 406 antibody-positive arrivals were cured inside prison by Corvane Health,
whose own workbook holds those courses and its reception tests, and an antibody stays reactive after a cure.

## Three rules

Task type: epidemiology-public-health / screening-diagnostic-policy-evaluation, which serves Opportunity Sizing: a case-finding programme sized and placed by the people with active infection it finds and starts on treatment.
Domain test: the deciding quantity is each setting's count of people with active hepatitis C the van would find and start, the epidemiologist's antibody positives times the share still viraemic, where an antibody stays reactive after a cure, a never-diagnosed infection is chronic about three times in four after spontaneous clearance, and a person treated in prison is recorded by the prison health provider and not the treatment network.
Swap: "which ward should the falls team work, and how many patients with active fall risk would it treat" keeps a pick and a count, but an antibody that outlives the infection, a laboratory that tests a known positive for RNA only, spontaneous clearance setting the never-diagnosed share and a cure recorded by whichever organisation gave it have no ward equivalent; with the nouns swapped the active share stops being something to estimate.
Layer 1: the organisations' own systems produce every mess item: Fenwold Pathology's test codes renamed at its March 2021 system change and a fortnight of results re-sent by the new system, results written as text with a viral load column, the network register's twelve-week results keyed by hand since its October 2024 go-live, people holding two NHS numbers whose laboratory samples sit under two pseudonyms joined only by the laboratory's own patient number while the register holds one, Corvane's workbook in two layouts, the older sheet with its own headers and day-first text dates, the peer log's setting written several ways with invalid kits, the hostels' day-first arrival dates and second stays in a year; each record is complete for its own producer; none decides the call (each asserted not to move it).
Layer 2: field_method, the active pool among antibody positives built person by person from every record of each positive's testing and treatment, wherever they were tested or treated, with the field's never-diagnosed share carried only by people no record speaks for.
Decisive step: reading each antibody-positive arrival's cures, courses and RNA results from Corvane Health's prison workbook as well as the network's register and Fenwold Pathology, because a prison leaver's antibody stays reactive after a course given inside that the network never saw.
Not semantics: every field read correctly (a reactive kit is a past or present infection, the register holds the network's courses, the workbook holds Corvane's) still leaves the easy route on the approved premises, because no field anywhere says a positive was cured elsewhere: the cure sits in another organisation's record that only a person-by-person join reaches, and why it matters is the epidemiology, an antibody that outlives the infection and a validated share that describes people nobody has tested.
Not rule application: no filed rule estimates the active share; the van plan files the pool, the year, the outcome and the pilot's rates, and executing every filed sentence leaves the active share open. Enumerated family (built pack): antibody positives alone and positives at the validated 0.74 file Fenwold Recovery's new entrants (1.20x), positives read against the network's register and the laboratory file the approved premises (1.20x), the pilot's ratio for the laboratory's changes no call; standing family (every construction that reads each positive's record from all three producers: the laboratory's 0.74 or the pilot's 0.72 for people with no record, a course completed without a twelve-week result read as a cure or not, a test matched within 42 or 60 days of arrival) files the needle exchange registrants in every member at about 50, spread under one person; the ruling-out is quiet: no clause, flag or one-group-by on a shipped column separates the people cured in prison, only the join of the peer log's positives to Corvane's workbook.
Analyst test: a strong analyst takes each setting's 2027 arrivals, the share the peer team found antibody positive, removes the positives the network's register and Fenwold Pathology show cured or clear, carries the rest at the 0.74 viraemic share the laboratory and the 2018-19 pilot validate, and files the approved premises first at about 80 people started on treatment, while most of the approved premises' positives were cured inside prison and the needle exchange registrants, the least treated, lead at about 50.
Estimand: the van plan (find_and_treat_van_2027_plan.pdf, sections 2 and 3) files the population (each setting's arrivals in calendar 2027, a person once in the year, at the yearly average of its arrivals in the two years to 30 September 2026, and taken to be like the people who arrived in those two years), the outcome (people the van tests, finds with RNA detected at that test, and starts on a course within twelve weeks), the window (calendar 2027), the unit (people started) and the comparison (the setting with the most), with the van testing and starting at the pilot's shares.
No decoy: nothing is planted to be caught: Corvane's workbook is its own record kept for its Health and Justice contract returns and carries the handovers the van takes on, no memo, draft or stakeholder figure argues for a setting, and no file ranks the settings on the decision.
No certified replay: no published or certified figure reproduces the method; the pilot evaluation gives the pilot's own counts, which its caseload reproduces.
Lesson: an antibody-positive count measures infection ever had, and after a curative programme the share still infected is built from every record of each person's testing and treatment, wherever it was given; the validated share describes people no record speaks for. No build on file teaches it (nearest drivers 0.07 and below).

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene battery | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 positives as starts (no viraemic share) | none | the peer log's result column | an epidemiologist's first correction is the viraemic share | none | no | yes, one multiplication | no | readable |
| R1 positives at the laboratory's 0.74 | the pathway's reflex RNA on a first reactive result | the laboratory's test codes | the field's chronic share | the laboratory's first positives, the pilot | no | yes | no | readable |
| R2 each positive read against the network's register and the laboratory (the default) | the pathway's twelve-week cure | the register's svr12 columns, the laboratory's RNA rows by pseudonym | the field's own subtraction of treated people | the attending arrivals' RNA results agree with 0.74 | the unmatched-join sweep finds nothing: every arrival's own records join | no | no | readable |
| R3 the prison workbook's cures, courses and reception tests joined person by person (decisive) | no sentence says a setting's positives were treated inside; the pathway names Corvane only for the handover | the workbook's columns are courses and reception results, no flag | the reflex stops at the network's own records | no control ranks the settings | no sweep joins a second organisation's courses to the peer log | no | no: the workbook ships for the van's continuity work, people released part-way through a course | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a 2027 year's arrivals | distinct people in each plan year, the two years averaged | arrival rows, a second stay counted again; distinct people over the two years, halved | same call (the second also same figures) | the plan, section 2 (a person once in the year; the yearly average); checks SF1 |
| SF2 | the share of arrivals the van tests | the pilot's tested over arrived (0.65) | the peer team's coverage of each setting (0.79 to 0.82); the mean of the two pilot sites' shares | same call (the second also same figures) | the plan, section 3 (the same share as the pilot tested of the people arriving at its two sites); checks SF2 |
| SF3 | antibody positive | a reactive kit; an invalid kit is no test | an invalid kit read as non-reactive | same call, same figures | checks SF3 |
| SF4 | active infection | RNA detected at the van's test, at arrival | the status at 30 September 2026, later cures counted | same call | the plan, section 2 (RNA detected at that test); checks SF4 |
| SF5 | started on treatment | a course started within twelve weeks of the test | any later start | same call | the plan, section 2; checks SF5 |
| SF6 | the share for a positive with no record | the laboratory's first positives (0.74) | the pilot's (0.72) | same call, same figures | checks SF6 |
| SF7 | which arrival a peer test belongs to | the arrival in the two years within 60 days before the test | within 42 days | same call | checks SF7 |
| SF8 | the comparison | the setting with the most people started | the most active infections | same call | the plan, section 2 (where it starts the most people); checks SF8 |
| SF9 | rounding | people to the nearest ten, once, at the end | every rate to two places and every count to whole people at each step | same call, same figures | the prompt; checks SF9 |
| SF10 | a cure | a course whose twelve-week RNA test is not detected | any course completed, whatever its result | same call, same figures | the pathway, section 3; checks SF10 |
| SF11 | a person on a course at the test | neither found nor started | counted at the viraemic share | same call, same starts (the approved premises' active figure moves from 10 to 20, 10.3 to 17.4, which the plan's sentence rules out; the same-figures assertion covers the starts) | the plan, section 2 (counted neither among the active infections it finds nor among its starts); checks SF11 |
| SF12 | a course completed with no twelve-week result | not a cure | read as a cure | same call, same figures | the pathway, section 3; checks SF12 |
| SF13 | a course finished in a half-year (ask) | its last dose: the planned end, or the date it stopped | the planned end for every course | ask figures only | the pathway, section 3 (the date it stopped for a course stopped early); checks SF13 |
| SF14 | a confirmed cure (ask) | the first RNA test twelve weeks or more after the last dose, not detected | any RNA test twelve weeks or more after, not detected | same ask figures (no course differs) | checks SF14 (records converge) |
| SF15 | the half-years (ask) | October 2024 to March 2025, April to September 2025, by the last dose | by the start | ask figures only | the prompt (the courses that ended in that half-year); checks SF15 |
| SF16 | the reactive share | per test matched to an arrival | per person, first test | same call, same figures | checks SF16 |
| SF17 | a positive with no earlier record and an RNA test after the kit | the 0.74 share, the status before the test | the RNA result in the 120 days after the kit | same call, same figures | checks SF17 |
| SF18 | the share for a positive with no record | the laboratory's first positives (0.74) | each setting's own share among its no-record positives tested for RNA after the kit (0.64 to 1.00) | same call, same figures | checks SF18 |
| SF19 | when the status is read | at the peer team's test | at the arrival it belongs to | same call, same figures | checks SF19 |
| SF20 | a course lost to follow-up (ask) | no last dose on record, so not a course finished in a half-year | finished on its planned end | one ask cell (one course with a later negative test) | the pathway, section 3 (a course lost to follow-up has no last dose on record); checks SF20 |
| SF21 | a cure on a course lost to follow-up (main call) | a twelve-week result not detected is a cure | no cure, the course having no last dose on record | same call, same figures (the person's own RNA results say the same) | checks SF21 |
| SF22 | the needle exchange registrants' arrivals | the provider returns in setting_arrivals | the pharmacies' paper registrations (the distractor) | same call (the second year alone moves the registrants' figures up a bin) | the plan, section 2 (from the returns each provider sends the commissioners); checks SF22 |
| SF23 | the courses that ended in a half-year (ask) | completed and stopped courses, each on its last dose | completed courses only | ask figures only (three cells) | the pathway, section 3 (the date it stopped for a course stopped early) and the prompt's ended; checks SF23 |
| SF24 | where the van works | the setting with the most people started | the venues the FibroScan sessions find with the most advanced liver disease (a distractor, venue-level, no pseudonym) | not a reading of the estimand | the plan, section 2 (where it starts the most people); checks SF24 |

## Ladder

| Rung | Construction | Approved premises | City hostels | Fenwold Recovery | Needle exchange | Call |
|---|---|---|---|---|---|---|
| R0 | positives as starts, no viraemic share | 121 | 78 | 145 | 91 | Fenwold Recovery |
| R1 | positives at the laboratory's 0.74 | 89 | 57 | 107 | 67 | Fenwold Recovery (1.20x) |
| R2 | the network's register and the laboratory read per positive (default) | 75 | 40 | 43 | 62 | approved premises (1.20x) |
| R3 | plus Corvane's workbook (golden) | 8 | 24 | 30 | 53 | needle exchange (1.79x) |

People started on treatment in 2027 before rounding. Every rung names a different candidate from the golden, the golden
is third on R1 and second on R2, every rung clears its runner-up by 1.15x or more, and the decisive rung moves the
approved premises from first to last. The approved premises' 406 antibody-positive arrivals: 28 cured on the network's
register, 223 more on Corvane's workbook. Active infections (golden): needle exchange 72, Fenwold Recovery 40, city
hostels 32, approved premises 10. Every rung, margin and bin distance is asserted in checks.py (77 assertions).

## Closure table

| # | Axis | Reading chosen | Closure move |
|---|---|---|---|
| 1 | Population | each setting's arrivals in calendar 2027, like those of the two years to 30 September 2026 | pinned (plan 2); C1 SF1 |
| 2 | Unit of account | a person, once in the year | pinned (plan 2) |
| 3 | Attribution window | calendar 2027; the two plan years October to September | pinned (plan 2) |
| 4 | As-of dating | status at the van's test, at arrival | pinned (plan 2); SF4 |
| 5 | Version basis | the records as extracted to 30 September 2026 | C1: one extract of each |
| 6 | Denominator | the arrivals the peer team tested | C1: SF3 |
| 7 | Weighting | each tested arrival once | C1 |
| 8 | Window length | two plan years | pinned (plan 2) |
| 9 | Boundary inclusivity | a test within 60 days after an arrival; twelve weeks or more after the last dose | C1 SF7; pinned (pathway 3) |
| 10 | Rounding path | unrounded counts, rounded once to the nearest ten | the prompt; every figure 1.25 or more from an edge, asserted |
| 11 | Tie-break | none needed | C1: golden margin 1.79x |
| 12 | Maturity and censoring | courses running at the test are not starts; twelve-week results after 30 September 2026 are not on record | pinned (plan 2); C1 |
| 13 | Order of operations | arrivals, tested, reactive, each positive's status, started | C1: multiplicative |
| 14 | Row order | not order-dependent | C1 |
| 15 | Duplicate resolution | the laboratory's re-sent rows dropped by lab number | C1: R2 mess check |
| 16 | Identity normalisation | the shared pseudonym, written the same way in all four producers' files; a person's two NHS-number pseudonyms at the laboratory joined by its lims_patient_id (the ask only) | C1: no arrival holds two pseudonyms (asserted) |
| 17 | Netting against gross | gross starts, not net of courses carried | pinned (plan 2) |
| 18 | Dimensional units | people, courses | C1 |
| 19 | Code and status semantics | the laboratory's old and new test codes; Reactive, Detected, Not detected | C1: never the stump |
| 20 | Integerisation | none: expected people, rounded once | C1 |
| 21 | Scope of a stated clause | "the van works as it did in the pilot": its test and start shares | pinned (plan 3) |
| 22 | Forward window contents | calendar 2027 arrivals from the two-year average | pinned (plan 2) |

## Literal reader

Executed word for word, the plan files who is counted (a 2027 year's arrivals at the two-year average, each person
once, like the arrivals of those two years), the outcome (RNA detected at the van's test, a course within twelve
weeks) and the van's two shares; it is silent on how each arrival's infection status is known, and every literal
execution that reads the shipped records of each positive (the register, the workbook, the laboratory) lands on the
needle exchange registrants at about 50; the routes that stop at the network's own records, or at the 0.74 share,
are easy methods on the same literal estimand, not other readings.

## Oracles

None ranks the settings. The pilot evaluation's counts reproduce from its caseload and confirm the van's shares on
every rung. Fenwold Pathology's first reactive results (0.74 RNA detected) and the attending arrivals' own RNA results
(0.72 to 0.94 by setting) confirm the viraemic share on R1 and R2 and, by construction, never see a cured positive: the
laboratory tests a known positive for RNA only and the cured do not come forward.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Path (files, columns) | Stops (lazy delta) | Realism |
|---|---|---|---|---|---|---|---|---|
| A, confirmed cures among the courses each of the network's five clinics finished, by half-year | 10 | an audit of an input the call consumes (the network's register), through rows the call never reads (courses finished after the October 2024 go-live, on people outside the four settings) | the trustees read the network's clinics' cure confirmation beside the van's placement | D7: people holding two NHS numbers; Fenwold Pathology keeps their samples under both pseudonyms, joined only by its own patient number (lims_patient_id), and the register carries one; for 27 courses finished in the year the twelve-week sample went in under the other pseudonym, so a join on the register's pseudonym finds the person's diagnosis and end-of-course tests and misses the twelve-week result; nothing names it: 64 laboratory patients hold two pseudonyms, 37 of them with no course in the year, and 19 other courses in the year genuinely have no twelve-week test, so the unmatched-join sweep reads the gap as follow-up lost | D4 (twelve-week results keyed by hand since the go-live: blank in the register, present in the laboratory); D8 (end-of-course tests within twelve weeks of the last dose); D2 (a course stopped early ends on the date it stopped) | hcv_treatment_register_2015-2026.csv (pseudonym, clinic_code, outcome, planned_end, stopped_on, svr12_date, svr12_result), virology_hcv_results_2015-01_to_2026-09.csv (lims_patient_id, pseudonym, sample_taken, test_code, result), fenwold_hcv_pathway_2026.pdf (3), network_clinic_list_2026.csv; 4 files, 13 columns | register only: every cell off (Fenwold Recovery October to March 23 against 43); pseudonym only: every cell off, by 1 to 6; any negative RNA after the course: 8 cells off; the planned end for stopped courses: 3 cells off | a person allocated two NHS numbers whom the laboratory's patient record joins and the clinic's register does not; a clinical system go-live that stopped results flowing into the register |
| C, each setting's active infections and starts, and the chart | 8 and the chart's parts | the construction | the call's own table | none | none | the golden model | R0 to R3 values | the plan's own measure |

- **Main population zero-counts:** no register row carrying a device (a person with a second pseudonym at the
  laboratory, or a twelve-week result left unkeyed while the laboratory holds it) belongs to an antibody-positive arrival
  with the row dated before their test (asserted, 0); no arrival holds two pseudonyms (asserted); deleting the ask's
  rows leaves the call and every Ask C figure unchanged.
- **Hazard table:** D4 moves every cell (register only); D8 moves eight cells; D2 moves three cells; the laboratory's
  re-sent rows (March 2021) move nothing.
- **Referee:** none; the pathway files the twelve-week rule and the last dose, which the cracker executes; nothing
  says the register's pseudonym is not the number the samples went in under.

| Ask figures | Cracker's path | Cracker's value | Verdict |
|---|---|---|---|
| A confirmed cures (10) | the pathway's last dose and twelve-week test, the laboratory searched where the register is blank, joined on the register's pseudonym | Fenwold Recovery 37 and 29, hospital hepatology 12 and 8, community 8 and 24, outreach 27 and 53, pharmacy 1 and 10: every cell off | miss |
| C active infections and starts (8) and the chart | the golden's construction | right | outside |

Mirror leakage: 5.0 per cent of the ask weight on the most attractive wrong rung (R2): the mirror misses all eight Ask C
figures and the chart's mark, and does Ask A as the cracker does.
Pair ceiling: 43.6 (the cracker at 72.5 with the call, Ask C and the chart; the R2 mirror at 14.8). A cracker that also
reads every pseudonym of a laboratory patient takes Ask A whole and the pair reaches 71.1, the ask's one exposure: the
link shows only as a cardinality nothing announces (two pseudonyms under one lims_patient_id), on 64 patients most of
whom have no course in the year, after the unmatched-join sweep has already explained the gap as courses with no
twelve-week test, which 19 courses in the year genuinely are.
Measured by: generator/cracker.py on the cut pack (target.zip md5 1382208d).

## Pre-ship check

- Free gates on target.zip 1382208d (2026-10-27, the shipped pack): checks.py 154 assertions, verify.py 27, two
  byte-identical builds, figures_check.py 21 of 21, precut.py 53 checks 0 FAIL 0 WARN (voice-check inside it).
- leak.py REVIEW, read: sweep 3, the plan names the four candidates, which are the call's words; sweep 4, the pathway and
  the plan carry the world's nouns (register, record, prison, antibody, Corvane) and name no move: the pathway's
  sentences that the register holds the courses the network starts and that Corvane provides healthcare in three
  prisons are true operational facts, and nothing says an antibody outlives a cure or that a setting's arrivals were
  treated inside; sweep 9, 31 register dates and 16 workbook dates after the 12 October 2026 compile, every one a
  planned course end (the register's planned_end on On treatment or Stopped rows, the workbook's Course end on courses
  running at the extract), forward by nature and allow-listed.
- Leak reader, three passes (a159a58b, b93a12c2 twice; the pathway and then the prompt changed): question 1 each time
  quoted the plan's filed comparison, the estimand, not a decisive step; questions 2 to 4 none; question 6 an
  analytical choice every time. Its forks were closed: a course lost to follow-up (SF20, the pathway now says it has no
  last dose on record), the needle exchange arrivals' source (SF22, the plan), completed courses only (SF23, the prompt
  now says ended, the pathway's word). Its one realism tell, sibling requesting sites with near-identical sample
  counts, was fixed in the generator (each person keeps a site, sites share by size) with figures.json byte-identical.
- Determinism judge. Pass 1 (a159a58b): NOT_DETERMINISTIC, SEND_BACK on Gate A and C, its thread recomputing the
  approved premises' prison-cured share at 29 to 30 per cent against 55. Reproduced before repairing: 28.1 per cent
  (114 of 406) is the older workbook sheet's lower-case pseudonyms left unmatched with cures counted to the as-of; joined,
  54.9 (223 of 406) per test and 54.6 (220 of 403) per person; its Gate C claim fails on its own mishandling (the
  approved premises 20.2 against the needle exchange 54.9). A join error, recorded and not built for; what it exposed
  was fixed (the older sheet's pseudonyms upper case, the newer sheets' dates real date cells, every mess variant
  asserted on every figure), and the write-up and the paper stopped narrating wrong-rung figures. Pass 2 (b93a12c2):
  DETERMINISTIC, FIX_NOW, Gate G method_or_model_selection, analytical_non_defect, surface_read_dependency no, Gate H
  analytical; the one defect a superlative of mine ("the highest share of the four"; the needle exchange's reactive
  share is higher), dropped, and the prison-cured component stated as more than half, which holds under every match
  window and either denominator (asserted) where its thread's own join gave 52.5. Pass 3, the FIX_NOW's one re-judge
  (b93a12c2): DETERMINISTIC, APPROVE, Gate G method_or_model_selection (borderline against single_conceptual_flip),
  analytical_non_defect, surface_read_dependency no; Gate H domain pass, layers pass, decisive step analytical; every
  committed figure and all ten clinic cells rebuilt exactly. The site-share realism fix after it is data-only and moves
  no graded figure, so the APPROVE stands on 1382208d. Its two informational notes: its thread verified the crude
  ignore-every-cure route rather than the default path (register and laboratory read, the workbook missed), which the
  ladder carries (R2 names the approved premises at 1.20x); and the FibroScan distractor's relevance is now a fork row
  (SF24). Rubric: the shape grades the call, eight setting figures, the chart and its mark, ten clinic cells, three
  components and the instruction lines, about 28 criteria.
- Container: the scrub audit is clean on target/ and golden/.
- House fixes: H16, every extract column asserted on or before its extract date (register and Corvane courses to 30
  September 2026, laboratory receipts and authorisations to the 12 October compile, the pilot's tests inside the pilot,
  the evaluation dated 17 January 2020 after every twelve-week window); H21, the city renamed from Tamberley (one letter
  from Camberley) to Fenwold and HMP Haverleigh (close to HMP Haverigg) to HMP Mardlow, asserted; H4 and H11,
  architecture 1's goldens and its second judge report removed; H6, the golden's stated rules and comparative words
  hold on the pack (asserted as words.*).
- Golden realism: a finding as title, a decision line, a source line under the table, a page-numbered footer,
  lopsided prose presenting the method forward, the chart opened and given a finding title, workbook number formats,
  frozen headers and a notes sheet.
- Fingerprint: the card is current; guard.py check WARN (overuse.objective, repeat.gate_g, repeat.decision,
  repeat.deliverables: docx and xlsx after task305 and task118 v3, kept because a charity's trustees' paper circulates as
  a Word document); heart WARN 2026-10-27, nearest driver 0.07 (task137); surface screened 299 builds and promoted 7
  pairs (surface 0.10 or under, and the card-level gap, pattern and decision collisions with task144, task150 and
  task268 the differentiation lines answer), left for the author's clone check.
- The 10/10 rules re-read against the built pack: the decisive step is still analytical (each positive's status built
  from every producer's record; no field, code or filed rule performs it), the mess is still only Layer 1 (every mess
  variant leaves every figure in its bin, asserted), and nothing is planted (the workbook is Corvane's own record).

## Tried and rejected

- Balance-point class (2026-10-24, probe seed 3041): households keeping their homes cold (balance points 49 to 54 F)
  took last year's retrofit as warmth; golden 24.75 GWh carrying the close-out by balance-point class. Coin flip:
  sonnet missed at 27.8, opus landed at 25.0 by fitting a variable-base balance point per premise and reading the
  close-out's savings by balance-point band. A heating state that a standard billing-analysis parameter reveals is a
  reflex stratification.
- Fuel substitution (2026-10-24, seed 3043): cold-kept homes heated one room with electric space heaters, so their gas
  looked tight and rose after the shell retrofit; golden 16.2 GWh against gas-only routes of 26 to 36. Landed by both
  probes (16.4): degree-day fits on each premise's electric reads split the units on the electric heating slope and the
  close-out's 139 negative-savings projects taught the class effect. A per-unit state the close-out labels with its
  outcome is carried by the supervised transport reflex, whatever file the state hides in.
- Income-qualified price response, documented (2026-10-24, seed 3044): Order 24-117 turned a rate discount into a fixed
  credit, so the close-out's before-and-after windows carried a price response the 2027 units will not show; golden
  42.5 GWh. Landed by both probes (43.1 and 42.8) reading the order and a load research sample.
- The same price response with no signal (seed 3044): sonnet found the step in the rate class's own bills against the
  other class in three minutes and filed 44.6 against same-rate routes of 44.2 to 44.3. A dated cause whose effect steps
  a series is found by an event study, unprompted, on the weaker model.
- Waiting list partly treated by the first stage (2026-10-25, seed 3041, county re-home): the 2027 scheduled units had
  their assessment visits (smart thermostat and weatherstripping, recorded in the field-visit register) during the
  months the 2025 installations are measured over, so the textbook not-yet-treated comparison understates the saving;
  the default (waiting list as comparison, or own year before) filed 23 to 24 GWh against a golden of 28 on clean truth
  (truth 28.1). Landed by both probes: opus compared the 2025 homes against the 834 homes with no visit in the window
  and took the assessment saving off the 2026-assessed baselines (27.47); sonnet fitted a panel with effect terms for
  post-assessment, post-install and a calendar shift (28.75). A dated per-unit event recorded in the pack is modelled by
  reflex as a covariate, whether it falls on the treated units or on the comparison. The clean family also spread 26.8
  to 28.7 GWh (total against heating-only normalized use, ratio of totals against mean of logs), because the common
  shift hit heating only; it would have needed a shift on total use to close Gate C.
- The lesson across the six: on this world the probes fit a degree-day model per premise, add a term for every recorded
  dated event, screen any comparison for recorded programme contact, stratify on every state the bills reveal, and
  carry the close-out's outcomes through every visible feature. The lane's builds that held turned instead on what the
  record counts (a shared upstream loss logged by every sibling, a population the demand model's origins omit, units
  still to arrive, records gone stale between recordings), so the next candidate here starts from what the bills,
  schedule or close-out double-count, omit or misstate, not from a per-unit effect, an event or a comparison group.
- Plan-only screens, rounds 2 to 5 (2026-10-26): fourteen candidates briefed to an opus plan reader (files and fields
  only, no data); every one was planned as the decisive step except meters without a lot file and mortgage concessions.
  A brief whose files and fields point at a mechanism gets it planned; only a mechanism living in an ordinary field's
  values that the default path has no reason to examine, with a forward implication, survived.
- Water meters by production run (2026-10-26, seed 1, Lowland Rivers Water, 2027 renewal district): a run of SJ-20s
  the 2021-22 renewals lost to stopped registers was partly held back and fitted in Holme from 2024. Probe B (opus) fitted
  stop rates by age, scanned the serials, found the defective batch and landed Holme; probe A (sonnet) filed Ashby 1,470.
  A strong pattern in the outcome record (failures clustered by serial) is found by a serial scan.
- Fixed five-to-ten-year extensions (2026-10-26): the payment after the extension spread the extended accounts across
  the payment-rise bands, so the chain with and without that band disagreed by up to 20 per cent on the first-time
  buyer figure; extensions are now sized as the Charter sizes them, the fewest whole years (up to ten) that bring the
  payment back, and the family closed to 25.4 to 34.0.
- Collections capitalisations that also lengthened the term (2026-10-26): a second kind of term increase, from
  accounts already in arrears, mixed into the state the decisive step reads and widened the family; capitalisation now
  re-spreads the arrears over the term left.
- Half the first-time buyer book extending (2026-10-26, budgets at 1.02 of the 2021 payment): 50 per cent of the live
  book took a longer term, more than a building society would see; budgets at 1.08 with a stronger fall into arrears
  bring it to 40 per cent and keep the call (seeds 1 to 9 measured: seed 3's rate-rise route filed the first-time buyer
  book, seeds 2, 4 to 9 put the golden or a family member on a bin edge; seed 1 holds every member in the 30 bin).
- Ask B over all four books, and the average loss with a surplus read as a gain (2026-10-26): buy to let had no
  shortfall in the window and its receivers' cross-reference is seen at once, so its figures leaked; the loss is now the
  policy's (nil on a surplus) and the ask covers the owner-occupied books.
- A pilot of six months (2026-10-26): about 300 borrowers an arm gave claim ratios from 0.4 to 1.0 by seed, too noisy
  for a report that halves the chance; the pilot now runs through 2024 (claims at 0.46 of the usual rate).
- Closing month rows that kept the balance and two payments of arrears (2026-10-26, stage 3): the month an account
  redeemed showed the full balance with the arrears grown by a payment, so the chain read a redemption as a fall into
  arrears; the closing row now clears both, and the fit leaves the month an account closes out.
- Halving the chance of possession (2026-10-26, stage 3): the call held under every construction but the first-time buyer
  figure ran 28 to 36 against the 35 edge (one curve for every extended account, by month, at 36; the book-level chains
  at 29 to 34), so the graded figure forked; at the pilot's 30 per cent cut the same constructions run 16.3 to 22.8,
  inside the 20 bin. The pilot's primary outcome moved to four payments behind within a year (about 120 an arm against
  50 claims), whose ratio (0.68) carries the cut, and its table is now rebuilt from the records.
- Accounts netted for closing first (2026-10-26): with the halving the closure-adjusted chains fell to 18 to 27, across
  the 25 edge; the plan now files the book as it stands with no allowance for accounts that close (SF21), and the netted
  chains, measured, still land in the 20 bin at the 30 per cent cut.
- Empty cells read as nothing (2026-10-26): with no smoothing and a band for every month an empty cell divided nought
  by nought and its accounts dropped out of the sum; an empty cell now takes its book's rate.
- Recoveries stream offsets 37, 43, 47, 59 and 61 (2026-10-26): on the final world each left an average loss within 20
  pounds of its rounding edge; 41 and 53 held their edges but let the careful cracker keep 3 and 2 of the 18 ask
  figures; offset 67 holds every edge at 29 or more and the cracker keeps 1.
- A projection window of twelve steps from October 2026 (2026-10-26, stage 4 round 1): the judge ran the chain twelve
  steps from October 2026 and mismatched the golden; the plan's year is January to December 2027, so the chain now runs
  October to December 2026 untallied and counts each account's first entry from January to December 2027 only.
- A 30 per cent cut on the chance of possession (2026-10-26): the pilot measures a cut in four payments behind, not in
  possessions, and a plan taking the whole arrears cut for possessions overreaches; the plan now takes 15 per cent, under
  half the pilot's cut in arrears, and the figures fall to the 10 bin and under 5.
- The first stage 4 asks (2026-10-26): open claims from the book's Litigation stage and the register's old book label
  were cracked at stage 4; ask A now turns on orders the courts re-seal and send again (one order) against genuine
  same-terms variations after a hearing, ask B on the loan parts (two register rows and two statements, one possession).
- The world after the window fix (2026-10-27, seed 1): High LTV's planning rate fell to 4.5 per cent and its figure to
  2.9, under the rate-rise route's first-time buyer figure (3.5), so the easy routes split; owner-occupied High LTV
  accounts now go to the panel solicitors faster once five payments behind (0.75 a month against 0.45), seeds 1 to 8
  scanned: seeds 1, 3, 4, 5 and 7 put High LTV or a family member over 5 or the first-time buyer family across an edge,
  seed 8 left High LTV 0.15 from 5, seed 6 left Shared ownership a planning rate near nothing; seed 2 holds every member
  (first-time buyer 8.0 to 11.9, High LTV 4.4 to 4.7, the easy routes' first-time buyer figure at most 3.7).
- Recoveries stream offsets 67, 71, 73, 79, 89 and 97 on seed 2 (2026-10-27): each left an average loss within 20 pounds
  of its rounding edge or let a re-sealed order fail to move the Shared ownership orders; 83 holds every check.
- The pilot's "half the cut in arrears, a 15 per cent cut" (2026-10-27): on seed 2 the stated arrears cut is about 35 per
  cent, whose half is not 15; the sentence now reads a 15 per cent cut, under half the cut in arrears, asserted.
- A data dictionary in the pack (2026-10-27, stage 3): the rule that no shipped file describes the data came in after
  the draw (leak.py LEAK on data_dictionary.csv); the dictionary is gone, the policy and the plan keep everything the
  Society defines (arrears, the court route, the loss, the four books), each export's own columns carry the rest, and
  the rate card's sheet of pricing terms is named Terms.
- Determinism closed by the data, after the portal's determinism return (2026-10-27; rubric and stump held; one judge
  unsure, one failed, competing_defensible_answer: a held-out-validated chain with no term-increase state, first-time
  buyer 316 against 325 observed, files High LTV, and the 2024 extensions read as small and possibly selected): on the
  shipped pack the September 2025 holdout at the first-time buyer book's own level does not separate the families (the
  payment-rise chain 396 and the term-state chain 409 against 389 observed), the separation lives only on the extended
  accounts (16 and 41 against 54), and the graded figure already forks among chains that carry the months since the
  switch (rate rise 3.7, months since the switch alone 3.7, payment rise 7.4, the term state 9.0; to the nearest ten 0,
  0, 10, 10). Enlarging the book's own earlier extensions to 1,500 to 1,800 unselected accounts (budgets tight from July
  2020, prior arrears 0.14 to 0.17 against the 2026 cohort's 0.16; twelve seeds over two origination profiles) took the
  time-static chain to z 2.4 to 6.3 in that holdout, but the rate-rise chain by months since the switch fitted it about
  as well as the term-state chain and filed High LTV in five seeds and the first-time buyer book in seven, and the
  default itself flipped in two (3.8 against 3.6 and 3.5). The fork is the stump: the 2027 figure rests on the extended
  accounts' share jumping, which no book-level holdout of a history where that share was small can pin, and any replica
  large enough to show at book level hands the switch-timing chains the answer. Architecture 1 spent.
- The ladder never enumerated the chain by the payment rise and the months since the switch: with no term state it
  files the first-time buyer book at 7.4 on the shipped pack (High LTV 4.6), so the write-up's step 5 clause (the same
  chain without the term-increase state puts High LTV first) held for one chain and not the family; a re-root enumerates
  switch-timing chains as a family of their own. Every model also under-predicts High LTV in that holdout (445 observed
  against 397 or 398, the young book's seasoning ramp), a bias any High LTV-side design in this world inherits.
- Re-root constraint (2026-10-27): the decisive 2027 quantity must be pinned by dynamics that played out at the
  contender book's own level in the history, the easy route failing because it lacks a covariate the data carries with
  known timing, not because a subgroup was rare before the forecast year. The one such shape seen in this world is a
  refix priced at product_end_date off the rate card the plan already names, and the prototype probes built a
  payment-shock model by months since the shock first, so it is a reflex: the re-root moves domain under the same
  objective and number unless a decisive step passes this constraint on paper.
- Architecture 2 draw screens (2026-10-27, no data cut), one clause each. A Help to Buy equity loan's year-six fee
  as a cost the lender's payment history cannot see passed the re-root constraint on paper but sits in the world the
  portal has already seen, so a second build there risks a duplicate finding. County input-output commuting leakage
  is task303's screen (both call-only probes landed on the Type II caveat). Bowel and lung first-round yields depleted
  by colonoscopies or CT scans done for other reasons are the prevalent-against-incident cut task130 and task135 set
  aside, and the depleted share is a few per cent in an English population. Regeneration decants carried as new
  tenancies and timing points that absorb a bus priority saving sit in urban x Opportunity Sizing, banned against
  task305, and the second is the max-of-two-steps family task127 spent. Public charging demand thinned by driveways
  needs address-level vehicle records no council holds. A hepatitis C antibody count read against the network's own
  treatment register alone is the field's own subtraction, so it went onto the default path as R2 rather than being
  the decisive step. Toll salience by payment channel (economics, elasticity) was kept as the fallback; its risk is
  Gate C on the elasticity family.
- A register whose coverage changes on a date (the prison health provider taking over in-prison treatment in April
  2022, so the network's register stops holding prison cures from then): dropped before the build at the advisor's
  reading, because a record that changes coverage on a date is a layout change across years and would read as Layer 1
  carrying the stump; the prison health provider's log is instead the standing arrangement, each record complete for
  its own provider, and R2 still lands the approved premises because their positives were treated inside.
- previous_pseudonym in the register (2026-10-27, stage 3): Ask A's primary carried by a register column holding the
  merged person's retired pseudonym. A column that isolates the device rows is a marker (supplemental-stumping ban 2),
  and noticing it is joining on it; the hygiene battery's re-keyed-records repair takes the ask whole and the pair to
  71.1. Re-sited: the register carries one pseudonym and only the laboratory's own patient number joins a person's two.
