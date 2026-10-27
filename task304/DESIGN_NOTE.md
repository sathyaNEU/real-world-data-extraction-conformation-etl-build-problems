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
| People (guard.py names --geo uk --seed 304) | Katie Reynolds, director of services; Nathan Hewitt, outreach team lead (ran the 2018-19 pilot); Clare Stevenson, consultant hepatologist and the network's clinical lead |
| World | a hepatitis C charity running peer testing and a find-and-treat van with an NHS hepatitis C operational delivery network in an English city and its county; four candidate settings the van has not worked: the probation approved premises (people on licence after prison), the city's homeless hostels, the drug and alcohol service's new entrants to treatment, and the community pharmacy needle exchange's new registrants; records to 30 September 2026 |
| Deliverables | outreach_van_2027_trustee_paper.docx, outreach_van_2027_funnel.xlsx |
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

The strong analyst's route, every field read correctly and every filed rule applied (figures from the prototype; the
built pack's figures replace them at stage 3):
1. Take each setting's 2027 intake at the yearly average of its intake in the two years to 30 September 2026, from
   the settings' intake registers (the plan's pool).
2. Take the share of each setting's intake the van tests from the 2018-19 pilot's caseload, and the share of each
   setting's tested intake the peer programme found antibody positive.
3. Remove from each setting's antibody positives the people the network's treatment register shows cured (a course
   with a negative twelve-week RNA test), the field's own subtraction.
4. Carry the rest at the viraemic share the laboratory's first antibody positives show (0.74) and the 2018-19 pilot
   and the intake positives' own RNA results confirm, then at the pilot's share of viraemic people started on treatment
   within the year.
Ends on: the approved premises, about 130 people started on treatment in 2027
Golden: the needle exchange registrants, about 95 people started on treatment in 2027, the drug service entrants next
at about 78, once each positive's cure is read from whichever organisation treated it, the prison health provider's log
for courses given inside as well as the network's register.

## Stump sentence

A competent analyst takes each setting's 2027 intake, the share the peer programme found antibody positive, removes the
positives the network's treatment register shows cured and carries the rest at the three-quarters viraemic share the
laboratory and the 2018-19 pilot validate, and files the approved premises first at about 130 people started on
treatment; the step that lands it there is treating the network's register as the record of every cure, when most of
the approved premises' antibody positives were cured inside prison by the prison health provider, whose own treatment
log holds those cures, and an antibody stays positive for life.

## Three rules

Task type: epidemiology-public-health / screening-diagnostic-policy-evaluation, which serves Opportunity Sizing: a case-finding programme sized and placed by the people with active infection it finds and starts on treatment.
Domain test: the deciding quantity is each setting's count of people with active hepatitis C the van would find and start on treatment, the epidemiologist's antibody positives times the share still viraemic, where an antibody persists for life after a cure, the never-treated keep the natural three-quarters chronic share after spontaneous clearance, and a person treated in prison is cured in the prison health provider's record and not the network's.
Swap: "which ward should the falls team work, and how many patients with active fall risk would it treat" keeps a pick and a count, but an antibody that outlives the infection, a laboratory that never re-tests a known positive for antibody, spontaneous clearance setting the never-treated share, a cure confirmed twelve weeks after the course and a cure recorded by whichever organisation gave it have no ward equivalent; with the nouns swapped the active share stops being something to estimate.
Layer 1: the organisations' own systems produce every mess item: the laboratory's test codes renamed at its 2021 system change, results written as text (Reactive, Non-reactive, Equivocal, Detected, Not detected, below 15 IU/mL), rows the laboratory re-sent in a later extract, the prison log's day-first dates and its prison numbers beside the shared pseudonym, setting names written several ways in the peer log, re-admissions in the intake registers; the network's register and the prison health provider's log are each complete for the courses its own provider gave; none decides the call (each asserted not to move it).
Layer 2: field_method, the active pool among antibody positives built person by person from each positive's treatment record wherever the course was given, with the validated viraemic share carried only by the never-treated.
Decisive step: reading each antibody-positive arrival's cure from whichever organisation treated them, the network's register for community courses and the prison health provider's log for courses given inside, before carrying the validated viraemic share to the never-treated.
Not semantics: every field read correctly (a reactive antibody is a past or present infection, the register holds the network's courses, the prison log holds the prison provider's courses) still leaves the easy route on the approved premises, because no field says a positive was cured elsewhere: the cure is an event in another organisation's record that only a person-by-person join finds, and why it matters is the epidemiology, an antibody that persists after cure and a validated share that describes never-treated positives only.
Not rule application: no filed rule estimates the active share; the plan files the pool, the year, the outcome and the van's pilot rates, and executing every filed sentence leaves the active share open. Enumerated family (prototype, 20 seeds): antibody positives alone and positives at the validated share file the drug service entrants (20 of 20), positives less the network register's cures file the approved premises (20 of 20), the pilot's ratio for the laboratory's changes no call; standing family (four constructions that read each positive's cure from both records: reinfection from the laboratory or not counted, a course without a twelve-week result counted cured or not, either ratio) files the needle exchange registrants 20 of 20 with a spread of about 1.3 people on about 95, one printed bin; the ruling-out is quiet: no clause, flag or one-group-by on any shipped column separates the people cured in prison, only the join to the prison health provider's log.
Analyst test: a strong analyst takes each setting's 2027 intake at its 2025-26 average, the share the peer programme found antibody positive, removes the positives the network's register shows cured, carries the rest at the 0.74 viraemic share the laboratory's first positives and the 2018-19 pilot validate, and files the approved premises first at about 130 people started on treatment, while most of the approved premises' positives were cured inside prison and the needle exchange registrants, the least treated, lead at about 95.
Estimand: the van plan (outreach_van_2027_plan.pdf, sections 2 and 3) files the population (each setting's arrivals in calendar 2027, at the yearly average of its arrivals in the two years to 30 September 2026), the outcome (people the van tests, finds with active infection and starts on treatment in 2027), the window (calendar 2027), the unit (people started, each once) and the comparison (the setting with the most), with the van's contact and start rates from the 2018-19 pilot.
No decoy: nothing is planted to be caught: the prison health provider's log is its own record kept for its Health and Justice contract returns, no memo, draft or stakeholder figure argues for a setting, and no file ranks the settings on the decision.
No certified replay: no published or certified figure reproduces the method; the pilot report gives the pilot's own counts, which its caseload reproduces.
Lesson: after a curative programme an antibody-positive count measures past infection, and the share still infected is built person by person from each positive's treatment record wherever the course was given, the validated viraemic share applying to the never-treated only; no build on file teaches it (nearest drivers 0.07 and below).

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
