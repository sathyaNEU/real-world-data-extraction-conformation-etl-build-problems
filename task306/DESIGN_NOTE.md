# task306 design note

Architecture 5, drawn 2026-11-08 after the portal returned architecture 4 FAILED_TO_STUMP on 2026-11-07 (both
responses filed the golden capacity call and all 24 ask figures). One architecture per world: energy (EV packs),
urban (regional GVA), actuarial (windstorm reinsurance) and quantitative finance (market impact) are spent in this
slot, so the build moves to pharmacology with a new world, dataset, generator and prompt shell. The author's five
conditions of 2026-11-07 bind the design and are argued in `## Author's conditions` before any data is cut.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task306.json`, architecture 5, registered 2026-11-08; architecture 4 moved
   into the card's lineage with its fate (the four earlier architectures sit there as spent).
2. Pairing: Pharmacology, Pharmacoepidemiology & Safety, task type benefit-risk-assessment, objective Opportunity
   Sizing & Decision Support (never carded on this objective). The headline is a sized opportunity, pool to
   realisable: each review's eligible patients (the pool), the patients a year of pharmacist reviews would take off
   the medicine for good (the realisable part) and the serious harms that avoids, which decides the call.
3. World: Marches Primary Care Collaborative, a GP federation in the West Midlands whose clinical pharmacist team
   serves its member practices under NHS Severn Marches Integrated Care Board's medicines safety contract. The team
   can run one structured deprescribing review across every member practice in 2027-28. In the first half of 2026 it
   piloted all three candidate reviews in the Clun Valley Primary Care Network's practices (rural, far from the
   specialist services) and followed each reviewed patient for six months. Specialist letters reach the practices
   from Wrekinside Teaching Hospitals NHS Trust and Marches Mental Health NHS Trust. People from `guard.py names --geo
   "United Kingdom" --seed 306`: Leigh Bond (the federation's medicines optimisation lead, who puts the programme to
   the committee), Colin French (lead clinical pharmacist, ran the pilot), Sylvia McDonald (chair of the medicines
   optimisation committee).
4. Candidates: (A) antipsychotics in people with dementia; (B) long-term benzodiazepines and Z-drugs in people aged
   65 and over; (C) gabapentinoids taken with an opioid.
5. Quantity: for each review, the serious harms a year it would avoid if run across every member practice in 2027,
   the federation's eligible patients at 31 December 2026 who would be taken off the medicine for good times the
   attributable harm rate per patient-year of continued use at each patient's age (the programme specification's
   table). The call is which review the team runs.
6. Shape: other. Three reviews, each with its eligible patients, patients taken off and harms avoided; the call, the
   runner-up and the gap; a chart; and two asks on the federation's 2026 records (31 or more criteria).
7. Default path: carry each review's pilot take-off rate (the share of reviewed patients still off the medicine six
   months on) to the federation's eligible patients and weight them by the harm table; it files antipsychotics.
8. Data-native sentence: the practices' records carry each medicine's first issue and the specialists' letters carry
   each recommendation to start one, so who started a patient's medicine is a relation between two systems that no
   field stores; the pilot practices' patients were mostly practice-started because the Clun Valley is far from the
   memory and pain services, while across the federation most antipsychotic users in dementia were started by the
   mental health trust, and practice pharmacists almost never stopped a medicine a specialist service had started.
9. Abstraction sentence, written against the nearest approved builds and found not to be the same: task258 carries a
   playbook only where the mechanism's precondition holds (the preload in the served head) and task309 carries a cut
   by a physical intensity; here the review reaches every eligible patient, nothing in the mechanism is absent and
   nothing varies in intensity: the measured success rate depends on a provenance, who started the medicine, which
   the pilot's population nearly all shared and the federation's antipsychotic users mostly do not. The card carries
   differentiation lines against task258, task309, task124, task141, task303, task137, task128, task304 and task98.
10. Furniture: forum committee_or_panel (the federation's medicines optimisation committee), forcing launch_or_rollout
   (the 2027-28 programme starts in April 2027), org hospital_or_health_provider (a GP federation providing the
   pharmacist service), role programme_officer. Redrawn at the draw: forum executive_team, forcing
   budget_or_appropriation and the stump strategy composition_mix each repeated a build in the primary checkout's
   window (task204, task142), and decomposition_attribution repeated task185 there. Two strategy keys describe this
   design honestly, composition_mix (the pooled rate does not fit this pool's mix on a property no column names) and
   forecast_method_backtest (`strategies.md` F6: the rate is stationary only in a constructed exposure, rebuilt from a
   log, and the natural carry fails forward); the card takes the second because the window bars the first, and the
   design note's step is exactly F6's: the take-off rate is stationary only within the provenance rebuilt from the
   letters. No back-test picks it (condition 2 below).
11. Prompt shell: a how-much question (the harm each review would avoid), the second sentence opening on the paper
   for the committee, the rounding sentence opening "Patients"; deliverables pdf and csv. None repeats a shell in this
   slot's lineage. Guard on main: PASS. Guard from the primary checkout: WARN repeat.gate_g (forecasting against
   task142), answered: the forecast here is a take-off carried across provenance, task142's is a population
   projection.

## Author's conditions

1. The field's full textbook method, done carefully, files the wrong call. The field's method for a deprescribing
   review's value is absolute harm at each patient's age times the patients the review takes off, the take-off read
   from the review's own pilot (benefit-risk card 1: absolute risks at each subgroup's baseline). Done carefully (each
   review's own pilot rate at six months, the protocol's eligibility and exclusions applied, ages banded, practice
   mergers conformed, the pilot checked for homogeneity across its practices, ages and sexes, which it passes), it
   funds antipsychotics. Only the step the data's structure demands files the golden: the take-off rate is stationary
   only within provenance, so it must be carried by who started each medicine, rebuilt from the letters. No sentence
   in the pack says that a specialist-started medicine is harder to stop or that provenance should be read.
2. The data does not reveal the right method by fit. No model is fitted. The pilot's pooled rate reproduces the
   pilot exactly and so does the provenance-stratified rate; neither is tested on the federation, whose 2027 outcome
   does not exist yet; the pilot is homogeneous on every recorded attribute (practice, age band, sex), so no residual,
   R-squared, back-test or reconciliation on any shipped column prefers the golden route.
3. The asks are not executable from filed rules: each rides a reconstruction across two systems or grains no sentence
   states (designed in `## Ask sheet`, `supplemental-stumping` Part 2.1), and on paper each of the top two keeps under
   two fifths of the ask weight.
4. The ladder (`## Ladder`) keeps at least one of the top two off the call: every route that does not rebuild
   provenance files antipsychotics, including every reweighting by a recorded attribute; the pair is argued near 50
   and built under 60 against a bar of 70.
5. The three rules sit in `## Three rules`, each on its own line; `precut.py` exit 0 before data is cut.

## Default path

1. Read the federation's 2027 medicines safety programme specification: one review run across every member practice
   from April 2027, valued at the serious harms a year avoided by the eligible patients taken off for good, at the
   attributable harm rates per patient-year by age band in its table.
2. Read each review's protocol for its eligibility and exclusions, and apply them to the practices' prescribing and
   problem lists at 31 December 2026: about 1,000 patients for the antipsychotic review, 1,400 for the benzodiazepine
   review and 1,800 for the gabapentinoid review (design targets).
3. Read the 2026 pilot from its close-out summary and outcome log: the share of reviewed patients still off the
   medicine six months on, about 40 per cent for antipsychotics, 23 per cent for benzodiazepines and 28 per cent for
   gabapentinoids, the same across the pilot's practices, age bands and sexes.
4. Carry each review's pilot rate to its eligible patients and weight by the harm rates at each patient's age: about
   30 harms a year for antipsychotics against 15 for benzodiazepines and 14 for gabapentinoids.

Ends on: the antipsychotic review, about 30 harms a year avoided.
Golden: the benzodiazepine review, about 15 harms a year avoided against the antipsychotic review's 11 and the
gabapentinoid review's 9 (design targets; asserted at stage 3).

## Stump sentence

The default path carries each review's pilot take-off rate to the federation's eligible patients and funds the
antipsychotic review at about 30 harms a year; the step that lands it there is carrying the pilot's average rate to
every eligible patient, when practice pharmacists almost never stopped a medicine a specialist service had started,
the pilot practices' antipsychotic users were mostly practice-started and most of the federation's were started by
the mental health trust, so the antipsychotic review would avoid about 11 harms a year against the benzodiazepine
review's 15.

## Tried and rejected

- Pack 1 of the prototype (2026-10-24, seed 3061) hid each imported car's pack history before its Dutch registration (the log started at the Dutch registration), so a solver could not know an import's pack state and both probes repaired it differently (sonnet calibrated the imports down by 0.74, opus modelled the abroad replacements in expectation): a fork, not the stump. The log is now the OEMs' EU-wide record plus Voltwerk's own, and a car whose pack failed outside warranty abroad is scrapped there and never imported.
- The prototype's truth carried a scrappage and export rate that no file shows; the forecast now takes a car in use to stay in use through 2027, filed in the tooling plan.
- The first cut's imports arrived about six years old, inside the eight-year warranty, and moved the call by three per cent and one lot; the Mira city car is now the platform kept alive by old imports from abroad, as old cheap EVs are.
- A refurbished pack failing inside Voltwerk's two years was logged as an OEM warranty fit in the prototype (99 rows): fixed, a Voltwerk-warranty failure takes another refurbished pack under Voltwerk's cover.
- The first stage-2 world kept the Mira city car launched in 2014 with 520 imports a month and an eight-year warranty: its arrival stream still ramped through the replay windows, so the 6- and 24-month windows spread the Mira's forecast by 51 and the total straddled a hundred bin. The Mira is now launched in 2013 with a five-year warranty and a steeper wear-out, its stream flat over the last 36 months and its imports arriving as survivors on their original packs.
- An estimand counting only failures outside both warranties left out the packs Voltwerk itself replaces under its two-year warranty, which the line supplies too; the plan now counts every failure outside the OEM warranty.
- Grading each platform's forecast paid the wrong route: the register-only route files four of the five platforms' forecasts at the nearest hundred (only the Mira moves); the prompt grades the slots and the total.
- Ask B's re-keying first moved the naive share by under 0.1 point on the Volta hatch, the new ids passing at about the platform's own rate; the BMS is now replaced in seven reworks in ten and the line seed (31062, from 750 swept) keeps every platform's natural read and over-repair outside its bin on all three asks, worst golden edge 0.155 of a bin.
- The dealer rows of the replacement log first carried plates typed with dashes; a solver who joined without normalising them filed Mira 1,350 and Volta 1,000, so that mess could move the call (dataset-generation R2) and was cut: both sources now carry the register's own plate format.
- Ask C's first device, dock 2 setting its rejects aside without scanning them (absent from the intake export, present at the recycler without a core code), was landed 5 of 5 by the stage 4 reader: dock 2's zero rejects and the blank core codes sit on the path of anyone counting rejects, and the judge found the dock's practice stated in no file. Re-sited onto the grade's date (D2): the intake export carries each core's grade on 1 July 2026, so a core the line built on and scrapped reads AFGEKEURD, and only its work order in the MES shows it passed intake; every ask C figure is unchanged.
- The plan's "a car in use in the Netherlands is taken to stay in use through 2027" read to the stage 4 reader, and to the judge as its one soft spot, as freezing the register of 30 June 2026; the sentence now places the car in 2027 ("a car in use in the Netherlands in 2027 is taken to stay in use for the rest of the year"), the population the estimand already files, and names no import.
- The portal returned the build on determinism (both judges: Gates C, D and E, underspecified_objective, A, B and G passing): the plan as shipped named the register as its only source and its only dynamics clause was about exits, so both judges forecast the register of 30 June 2026 alone (3,448, 3,500 with a judge's renewals), and a judge also summed ask A's batch lines as written. Pinning the population to the register was refused (it makes the judges' answer the golden and spends the stump), and filing the projection (a twelfth a month at the trailing rate, mix and age) was refused (rule application, CLAUDE.md rule 3). Closed instead by the WHAT at authority: plan section 3 files the fleet of 2027 as the register and the cars first registered here from 1 July 2026 to the end of 2027 (SF25) and one pack per car (SF26), the projection left open and forced by C1 over 144 projections, and the line notes file the lot stock rule for ask A (SF27); no graded or stated figure moved (freeze.py). The cost: that the later registrations are in the fleet is now readable, so the decisive rung keeps only what no sentence says, which of them fall due; the default path's answer is now the easy route's on the literal estimand (the later registrations carried as new cars).
- 2026-10-31, architecture 1 spent at the batch 1 triage: shipped 10-24 and reshipped 10-26 after the portal's determinism block, its isolated cold reader reproduced the call cell for cell (Volta 900, Kestrel 250, Plover 350, Mira 1,450, Tern 50, 3,800) and named the decisive step a procedure, since the repair's population sentence and the plan's pack-age sentence read together as the method; the surviving risk the note recorded was that conditioning a survival curve on survival to the as-of date is reflex reachable. Re-rooted in a new world rather than hardened.
- 2026-10-31, re-root screen before this draw: an actuarial reinsurance-capital draw (a county mutual's 2027 windstorm programme, the vendor's year loss table loaded storm by storm for demand surge read off the market's index loss) cleared `guard.py check` and was set aside unregistered, because task309 (FORTIFIED roofs, one cut ratio across storms that varies with gust intensity, carried through a vendor event set) is the same insight in the same domain; regression to the mean in a health-services pilot and a healthy-adopter uptake were set aside as general statistical mechanisms readers name unprompted (task308's screen of six); stale-priced returns in a portfolio's risk budget were set aside as task135's cross-day covariance.
- 2026-10-31, architecture 2 (the development corporation's 2027 inward investment award between a logistics hub on the city region's boundary and an inland food plant, the induced round read where each project's staff live) drawn, registered and spent at stage 2 before any data was cut: the survivor anatomy's Actor test failed on paper, since where the hub's staff live is one join from a column (a roster postcode against the postcode directory's local authority), and every honest way to ship it (a roster, a travel plan's postcode survey, a commuting flow for the depot's zone) is a column or a sentence that sends a solver to it; the IO world offered no relation between rows that carries the induced round's leak.
- 2026-10-31, architecture 3 first cut (an occurrence cover against an annual aggregate cover): the two covers' releases separated by about 1.12 times under every loading of the storms, so no costing of the record moved the call; redesigned at stage 2 into the second-event cover, buy or not, on the occurrence cover's retained band.
- 2026-10-31, the second-event cover on the 50th worst year alone, an upper layer above the occurrence cover and a tall tower from 12 to 60 million were each priced: the single year was noisy enough to flip on the seed, the upper layer's release was small and noisy, and the tower closed the gap between the cheap routes and the golden; the capital policy's average of the 50 worst years and the 7.5 million xs 4 million band were kept.
- 2026-10-31, the first record draw (seed 498): the ratio of totals over the later storms of each season landed the call (worth plus 0.13 million) with the golden's release, and the mean of ratios over the later storms of each year landed it too; a stormier physics with more trains a season made the rank routes buy harder, and shifting a year's first train to clear the year end left nine gaps of exactly 70 days and one inside the window corridor. The record is now drawn with trains kept apart across the year end and searched over 7,500 seeds for one where every rank, year, season, size and pooled route under every estimator files the wrong call (seed 2703, worst route minus 0.06 million).
- 2026-10-31, an exposure ask on the home book (sums insured in force by county) was set aside: in-force by date, renewal terms under new numbers and lapses are rule application a careful solver executes, with no reconstruction left after noticing; the home extract ships as a distractor and the farm book carries the exposure ask.
- 2026-10-31, a reopened claim's further damage first came to some claims before they had been notified, which no claims system allows and which left the pairing of lines and instructions unrecoverable for those claims; further damage now comes only to a claim already open with its adjuster instructed.
- 2026-10-31, architecture 3 (Penwarden's second-event windstorm cover for the county mutual) spent at stage 4: the FIX_NOW failed its second pass. Pass 1 (DETERMINISTIC, FIX_NOW) found "worth" in two senses, cover B's one reinstatement missing from the working and the coinsurance share unpinned, all fixed; pass 2 (DETERMINISTIC, FIX_NOW) found the 2026 storms asks open, since 379 reopened /R1 claim lines with no instruction of their own took their original claim's instructed damage day in the golden, a rule filed nowhere, and the lines' own loss_date filed a recovery of 11,881,000 against 12,015,000. The main call (follow-on storms costing 1.62 times the model) held throughout. The lesson carried forward: a reopened, re-sent or amended record's date or owner is filed or unmistakable before any ask counts it. Reports kept as determinism_check_report_arch3.md and determinism_check_report_arch3_pass2.md.
- 2026-10-31, architecture 4 at its stage 4 judge (NOT_DETERMINISTIC, reconciled FIX_NOW): the call held in every variant, but the runner-up, the gap and the kept alpha moved with the curve's exponent (momentum 3.91 to 5.88 between 0.7 and 0.4), its weighting, a common intercept across the bands, the consolidation day left as a return and the ESG names dropped, because the desk's orders sat almost all under 3 per cent of a stock's day (1.2 per cent were event trades) and the data did not separate the forms (R2 0.4655 against 0.4630); the ESG list also took effect inside the log (15 January 2026) while 101 rebalance rows still traded listed names. Repaired in the generator, the call and the decisive step unchanged; the judge's verdict kept as determinism_check_report_arch4.md.
- 2026-10-31, the first repair raised liquid event trades to a tenth of the desk's orders (4 to 60 per cent of the day): the family converged, but those orders carried most of the desk's traded pounds, so the value-weighted band averages (57, 75 and 115 bps) converged on the curve and filed UK Mid Cap Value, and the default path no longer ended wrong. Rejected.
- 2026-10-31, kept: participation comes from thin names, as it does on a desk. Each lower band carries a tail of thinly traded names (52 in the FTSE 250, 100 in the SmallCap), where the books' ordinary orders, sized in pounds and scaled only mildly with liquidity, take a fifth to two thirds of the day; the desk's pounds stay in liquid names at about one per cent, so the band averages still file momentum (by 2.7 million) while about 1,550 small-cap orders above a tenth of the day pin the curve where momentum trades. The 12 least liquid small caps, which no book or candidate trades, carry the consolidations; the ESG list predates the log and no book or candidate trades a listed name; the books' orders begin on 1 April 2025 with 60 sessions of history; the Severnvale transition trades large and mid caps only, at five orders a day.
- 2026-10-31, a tail of 130 thin small caps was dropped: it left momentum's investable pool (5 million a day or more) too small to swap 18 names a month, and its kept alpha fell to under 1 million.
- 2026-10-31, a common intercept across the bands was not chased: the half-spread differs by band (3, 8.5 and 25 bps), so one intercept misprices each band's trades by 0.5 to 2.2 million, which no rounding bin absorbs; IC-07 now files the population a cost is estimated from (the desk's executions in the candidate's index band), the WHAT, and the golden fits band by band. A lower shortfall noise and a narrower or wider spread of order sizes were screened and left the family's width unchanged (it is form error, set by where the desk's orders sit), so the order sizes' spread was set at 0.6 for the wider stump margin.
- 2026-11-07, architecture 4 (Wealdmoor's GBP 400 million to one of three backtested UK strategies, the alpha each keeps once its rebalances are priced at that size) spent on its first portal round, FAILED_TO_STUMP: both responses filed the golden exactly (UK Mid Cap Value 8, UK Large Cap Quality 6, momentum 5, gap 2) by the field's own textbook, a per-band fit of shortfall on volatility times the square root of participation, validated on a July to November holdout where it beat the flat band costs (RMSE 13.6, 8.5 and 18.9 bps against 26.6, 12.7 and 40.2), so the data revealed the right method by fit; both also took all 24 ask figures, since the failover merge and the block allocation were filed in TCA standard section 1 and the allocation export. The participation-dependent cost carried to size is what a careful analyst executes by reflex; the market-impact world, the capacity driver and the which shell are spent.
- 2026-11-08, re-root screen before architecture 5 (paper only, no harness): a retention trial's spillover through referral or household ties (task127's reserved credit contagion is the same insight, and task131 v1 shipped household interference); an outpatient follow-up rollout netted of GP re-referrals and a DNA programme credited only with avoided rebookings (the first is a hidden overlap the author's lesson says both responses find, the second is one group-by once thought of); theatre overrun cancellations traced to a late start from the first patient's admission (task130, task111 and task137 screened the knock-on as a reflex); line infections split insertion against maintenance by days since insertion and an IV-to-oral switch netted of unswitchable courses (the options' own names announce the class, and the IVOS criteria are filed nationally); broadband full fibre's churn benefit by copper line length (the line's sync speed is one join from a column).
- 2026-11-08, architecture 5's first registered draft (a ward deterioration service, e-obs alerting with critical care outreach, validated at about a 43 per cent cut in arrest calls in two directorates and carried to an uncovered directorate whose arrests mostly had no e-obs escalation in the day before): rejected before registration on the abstraction sentence, because it is task258's insight in clinical nouns (a validated effect that works only through a per-unit precondition every past application met, carried to units that lack it, visible only by a join), and the guard put its structural signature on task127 v2 (the landed concurrent wait); the antecedent-arrest analysis is also the rapid-response literature's own (MERIT, NCEPOD), so a careful response would execute it.
- 2026-11-08, a shared-care rule filed in the federation's policy (practice pharmacists may not stop a specialist-started medicine without the specialist's agreement): rejected, because with the rule filed the decisive step becomes identifying a class from records under a filed rule, which is rule application; the provenance effect is left to the pilot's own outcomes.
