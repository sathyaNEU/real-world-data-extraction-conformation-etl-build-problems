# task473 design note: Pembrook State's FY2028 high-range counties for impaired driving

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task473.json` (architecture v1), registered 2026-10-20 after a pull, so
  every card filed before it was in the check; `check` re-run on the registered card: WARN only. Redrawn at the draw:
  the decisive generator (G14 first repeats task249 v4 and G12 first task268 v2's lineage inside the batch, so G6, the
  BAC-band composition each county's impaired drivers carry, which is the decisive rung honestly), the decision type
  (a capped slate repeated task270's puzzle; the GHSO's high-range line is a designation), the strategy
  (population_selection is task268's; composition_mix names the decisive refinement), the organisation family
  (government_agency is task177's; the university center keeps the records and prepares the list) and, at
  registration, the pairing and the forcing event against task474 (Pairing, below). WARNs answered: shape 01 in 5 of
  the last 12 (the call is a list of candidates against a line, the shape the decision has); Gate G
  method_or_model_selection in 9 of 12 and in task468 v4 and task474 (the decisive step is the choice of completion
  between defensible estimators, pinned by the complete mechanism; no other Gate G mechanism carries it). The
  structural matches on older builds are differentiated on the card (task230 v1, task253 v1, task265 v0, task455 v1,
  task465 v1, task68). Nearest driver task458 at 0.06.
- **Seed:** ET30 (a regional federal highway-safety office sends three impaired-driving technical-assistance teams to
  the states with the highest 2020 to 2022 alcohol-impaired-driving fatality rate per 100 million VMT; the analyst
  counted only crashes in which a driver's tested BAC was .08 or more, so a state that tests few drivers came out
  best). Kept: the world (a highway safety program targeting impaired-driving help by the field's own statistic,
  alcohol-impaired-driving fatalities per 100 million vehicle miles, compiled from a fatal crash census whose drivers
  are not all tested), the decision (which jurisdictions get the help) and the quantity. Changed: the jurisdictions
  are one state's 14 counties, and the help is the governor's highway safety office's FY2028 County Impaired Driving
  Task Force grant, given to every high-range county (the federal 405(d) scale, 0.60 or more). Dropped as the
  decisive step: the seed's own moves, counting only tested drivers (rung 0 here) and the ten imputations read through
  a fan-out join (a reading of a supplied file; no imputation file ships).
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / Data
  Extraction & Conformation (ETL). The Center keeps the state's fatal crash census and conforms it each year, with the
  State Toxicology Laboratory's specimen results, the agencies' arrest records and the DOT's county vehicle miles, into
  the county file the GHSO designates from. The census holds the same item, each driver's blood alcohol, under two
  observation mechanisms: the State Patrol and two sheriffs test every surviving driver, every other agency tests a
  surviving driver only after an arrest at the scene. The deciding quantity is each county's 2023 to 2025
  alcohol-impaired-driving fatalities with the untested drivers completed, a data-integration estimate: the two
  mechanisms combined so the arrest-triggered positives are weighted by what the complete mechanism shows an arrest
  catches. Redrawn at registration: the draw was first filed in Survey Research & Official Statistics
  (census-register-administrative-data-quality), and task474's registration (the same domain and objective, and the
  same budget forcing event) put both axes inside the ban window; the replacement is honest because the decisive
  estimator is the integration of two observation mechanisms of one item, which is data integration's own object, not
  a register's coverage.
- **Shape:** 01 with a threshold instead of a cap: each of the 14 counties' 2023 to 2025 rate and its high-range
  verdict, the high-range list, the first county below the line and its shortfall, the bar chart with the 0.60
  line, the two files.
- **Strategy:** composition_mix. Officers' arrests at the scene catch drivers at .15 and above far more often than
  drivers between .08 and .149, and the counties differ in how their impaired drivers' BACs are spread, so neither the
  tested drivers' rate, one arrest share pooled over the agencies that test everyone, nor a model with one arrest
  effect fits a county whose impaired drivers sit nearer the limit. Decisive generator G6 (the band that moves
  against the rest), with G14 (the pooled catch rate does not fit this pool) and G12 (an untested driver is neither
  sober nor like the tested). Gate G method_or_model_selection: several defensible completions, the right one pinned
  by the agencies that test every driver.
- **World:** United States, an unnamed state. The Pembrook State University Center for Transportation Safety keeps
  the state's crash records system under contract with the Governor's Highway Safety Office (GHSO) and prepares its
  impaired-driving problem identification. The State Patrol's fatal crash procedure draws blood from every
  surviving driver; county sheriffs and city police draw blood from a surviving driver arrested at the scene for
  impaired driving (with a warrant when the driver refuses); the Corwin and Ossian county sheriffs follow the State
  Patrol's procedure. Coroners and the medical examiner submit blood or vitreous from killed drivers. The GHSO's
  FY2028 guidelines fund a task force in every high-range county.
- **Forcing fact:** the Center certifies the FY2028 high-range list to the GHSO by 1 May 2027 for the FY2028 Highway
  Safety Plan (due 1 July 2027); task forces start 1 October 2027. As-of: 22 March 2027. The call faces forward (the
  FY2028 grants); its quantity is the closed 2023 to 2025 window the guidelines name (a retrospective quantity with
  its reason: the grant designates on the latest three complete years).
- **Forum and forcing event:** funder_or_donor (the GHSO funds the task forces and the Center), launch_or_rollout
  (the FY2028 task forces start on 1 October 2027 and each needs its county certified for its application; redrawn from
  budget_or_appropriation, which task474 holds in the window). Organisation university_or_school (the university center that
  keeps the records and prepares the list); role programme_officer. Personas from `guard.py names --geo "United
  States" --seed 473`: Mary Mitchell (the Center's impaired driving program coordinator), Eduardo Chapman (the
  Center's crash records manager), Janet Brooks (the GHSO's impaired driving program manager).
- **Data-native sentence:** a surviving driver's blood is drawn by a county or city agency only after an officer
  arrests the driver at the scene, and an officer notices a driver at .20 far more often than one at .09, so the
  arrested positives hold almost every heavily impaired driver and only a minority of the near-limit ones, and a
  county whose impaired drivers sit near the limit (Tanager's college-town nightlife) hides far more untested
  impaired drivers per positive found than a county whose impaired drivers are heavily impaired (Brisbin).
- **The WHAT screen.** Population: every person who died within 30 days of a crash on a public road in the county in
  2023 to 2025 (crash date, local time) in which an identified driver of a motor vehicle in transport had a BAC of .08
  g/dL or more, whether or not that driver was tested (the guidelines). Outcome: those deaths. Window: calendar 2023
  to 2025. Unit: deaths per 100 million vehicle miles, the three years' deaths over the three years' miles.
  Comparison: 0.60 or more is high-range (the guidelines). The decisive step settles none of them: it is how the
  untested surviving drivers' BAC is completed, which nothing files.
- **Deliverables:** `county_impaired_driving_rates_2023_2025.csv` (each county's three-year deaths and rate, its
  verdict and its 2025 baselines) and `fy2028_high_range_certification.pdf` (the Center's certification letter to the
  GHSO with the bar chart of the 14 rates against the 0.60 line).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, General Statistics `missing-data-censoring-measurement-error`
    3 (nonignorable missingness, delta-adjusted): there a sensitivity grid is the pin; here the departure from MAR is
    not a stated offset but measured, an officer's arrest as a detector whose catch rate by BAC band the
    all-drivers agencies show, so no grid or offset is filed.
  - `census-register-administrative-data-quality` 1 (dual-system estimates within post-strata): the capture of an
    administrative record measured within strata where it is homogeneous; here the stratum is the BAC band the
    capture depends on, and the second "system" is the all-drivers procedure, not a second list.
  - `dataset-generation/references/layer1-messiness.md`: crash forms changing codes, lab results linked by agency case
    numbers, local time against the lab's timestamps, DVMT in thousands per day against annual miles; each to be
    asserted neutral on the call.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`): task470 (a sensor that misses whole units;
    there the capture share is the wrong route and the miss scales with units never detected) and task448 (a list's
    capture by filing route measured on the overlap) are capture problems where the capture is a property of the
    unit or route; here the capture is a property of each case's own level of the trait, so the right completion
    weights every positive found by the catch rate at its own level. task230 v2 (a human detector's hit rate falling
    as targets grow rarer) moves the rate with prevalence; here it moves with each case's severity.

## Default path

1. Read the 2023 crash and person files (2011 report form) and the 2024 to 2025 files (2024 form), kept each death
   within 30 days of a 2023 to 2025 crash, by crash county; drivers are the operators of motor vehicles in
   transport, motorcycle riders included, and a driver never identified is left out (guidelines 2.3).
2. Took each tested driver's blood alcohol from the person file (whole blood, g/dL) and read the agency procedures
   in the crash records manual: the State Patrol and the Corwin and Ossian sheriffs draw blood from every surviving
   driver, other county and city agencies only from a driver arrested at the scene.
3. Measured, at the agencies that draw every surviving driver, the share of drivers not arrested at the scene who
   were at .08 or more (about 7 per cent), and gave that probability to every untested, unarrested surviving driver
   of the other agencies; every killed driver and every arrested driver has a result.
4. Gave each crash the probability that at least one of its drivers was at .08 or more, summed its deaths, divided the
   three years' deaths by the three years' vehicle miles and compared with 0.60.

Ends on: Corwin, Hatchell, Ossian and Pruett high-range (Pruett in, Tanager out).

Golden: Corwin, Hatchell, Ossian and Tanager high-range.

## Stump sentence

The default path gives every unarrested surviving driver of the county and city agencies the share of unarrested
drivers at .08 or more where every driver is tested and certifies Corwin, Hatchell, Ossian and Pruett, because one
probability for every county treats a county's unarrested drivers as if its impaired drivers were spread across the
BAC bands the way the testing agencies' are, when officers miss most near-limit drivers and few heavily impaired ones;
it drops Tanager, whose impaired drivers sit near the limit, and certifies Pruett, whose few impaired drivers the
arrests already found.

## Three rules

Task type: data-integration-record-linkage-entity-resolution, integrating one item recorded under two observation
mechanisms (complete testing of surviving drivers at three agencies, arrest-triggered testing at the rest) into one
completed estimate, a task type serving Data Extraction & Conformation (ETL).

Domain test: general statistics, so the swap is of the method: the deciding quantity is a data-integration estimate,
each county's 2023 to 2025 alcohol-impaired-driving fatalities per 100 million vehicle miles with the untested
drivers completed by combining the two mechanisms, each arrest-triggered positive weighted by the inverse of the
arrest's catch rate at its own BAC band as the complete mechanism measures it; replacing that estimator with a generic
summary (the tested share, one unarrested share, a model with one arrest effect) certifies other counties.

Swap: put a generic completion in place of the integration estimator, "impute the untested drivers from the tested
ones" or "use the complete agencies' rate", and the call changes (Corwin, Hatchell, Ossian and Pruett, or Brisbin in
place of Tanager); put another field's nouns in ("which hospitals' infection rates put them on the watch list, when
wounds are swabbed only where a nurse suspects infection") and the setting's structure that fixes the estimator is
gone: the killed drivers tested by coroners whatever anyone suspects, the State Patrol drawing every survivor, the BAC
bands an officer's eye separates, the crash counted through any driver at .08, miles as the exposure.

Layer 1: the 2011 and 2024 crash report forms with different codes and person types (the census's own form change),
the toxicology laboratory's specimens keyed by agency case number with the medical examiner's and coroners' case
formats, resubmitted specimens and second draws (the laboratory's LIMS), whole-blood and serum results and
truncation to hundredths (the laboratory's reporting rules), crash times in local time against the laboratory's
timestamps, the DOT's county DVMT in thousands of daily miles by road class with a leap year (the DOT's HPMS
releases), agency codes renumbered with the 2024 form; each to be asserted neutral on the call.

Layer 2: estimand_identification (selection on the outcome): the surviving drivers county and city agencies test are
the ones officers arrested, and arrest depends on the BAC itself, more steeply than any recorded covariate carries,
so no imputation from the tested drivers is unbiased; the completion has to come from the catch rate by BAC band the
all-drivers agencies measure, applied to each positive found at its own band.

Decisive step: completing each county's county-and-city surviving drivers by counting every arrested driver found at
.08 or more as one over the share of drivers at that BAC band whom officers arrest at the scene where every driver
is tested (about 30 per cent from .08 to .149 and 88 per cent at .15 or more), which certifies Tanager and drops
Brisbin.

Not semantics: every field, code, unit and definition read correctly (the crash forms, the specimen types, whole
blood, the arrest flag, the case numbers, the dictionary's sentence on which agencies draw blood from whom) still
leaves the easy route on one share of unarrested drivers impaired, measured where every driver is tested, or on a
model of impairment on arrest fitted to the tested drivers; no field records how likely an officer was to notice a
driver, and the step is the choice of completion, not a reading.

Not rule application: the guidelines file the population (every death in a crash with a driver at .08 or more,
tested or not), the window, the unit, the ratio of the three years' totals and the 0.60 line; no filed rule or
procedure completes the untested drivers, and executing every filed rule with one share of unarrested drivers
impaired, taken where every driver is tested, certifies the default path's list.

Analyst test: a strong analyst who reads every file and rule correctly gives every unarrested surviving driver of
the county and city agencies the share of unarrested drivers at .08 or more where every driver is tested and
certifies Corwin, Hatchell, Ossian and Pruett (the default path's Ends on); a model of impairment on arrest and
county fitted to the tested drivers, or one arrest share pooled over the testing agencies, certifies Brisbin, Corwin,
Hatchell and Ossian; only the catch rate at each positive's own BAC band certifies Corwin, Hatchell, Ossian and
Tanager.

Estimand: the GHSO's FY2028 County Impaired Driving Task Force guidelines (section 2, in the pack): a county is
high-range when its 2023 to 2025 alcohol-impaired-driving fatalities, every death within 30 days of a crash in the
county in which an identified driver of a motor vehicle in transport had a BAC of .08 g/dL or more whether or not
that driver was tested, divided by its 2023 to 2025 vehicle miles, is 0.60 or more per 100 million vehicle miles.

No decoy: nothing is planted to be caught: the crash census, the laboratory's results, the arrest records and the
DOT's miles are what each system writes; no memo, draft, briefing, earlier list or stakeholder figure argues a method
or a list, and no file ranks the counties.

No certified replay: no published county rate, earlier designation or certified figure ships to back a method out
of; the all-drivers agencies are the records' own evidence on how arrests catch drivers, and they score a completion
only by the comparison a solver chooses to run.

Lesson: when a test is given only where an observer notices the trait and the observer notices strong cases far more
often than marginal ones, each positive found stands for one over the catch rate at its own level, measured where
everyone is tested; no build on file completes a selectively tested item by the catch rate at each found case's own
severity.

## Readability screen

(Stage 2.)

## Semantic fork table

(Stage 2.)

## Ladder

(Stage 2.)

## Closure table

(Stage 2.)

## Literal reader

(Stage 2.)

## Oracles

(Stage 2.)

## Ask sheet

(Stage 2.)

## Tried and rejected

- 2026-10-20, at the draw: the seed's own moves, counting only drivers with a tested BAC (kept as rung 0) and reading
  ten supplied imputations through a fan-out join (Rubin's rules over a shipped multiple-imputation file is a
  reading of the file and the textbook use of it); no imputation file ships.
- 2026-10-20, at the draw: imputing the untested survivors at the prevalence of the agencies that test every driver
  (a complete-testing subset transported): the common-exposure subset screen kills it (the all-drivers agencies'
  crashes are a filter and a divide), and county and city agencies' drivers differ in prevalence from the State
  Patrol's, so it is kept as a wrong rung, never the golden.
- 2026-10-20, at the draw: one arrest share for every BAC (a constant catch rate): with a constant catch rate the
  field's own imputation, a logistic model on arrest with a county effect, is exactly the right completion (the
  arrest odds ratio is then the same in every county), so a reader building the textbook model lands it; the catch
  rate must depend on the BAC band for the stump to exist.
- 2026-10-20, at the draw: BAC at the time of the crash from a delayed draw (retrograde extrapolation): turns on
  reading "at the time of the crash", data semantics, and the elimination rate is a knob.
- 2026-10-20, at the draw: results still pending at the file close, enriched in positives because a positive screen
  waits for confirmation: maturity completion again in a lane that has spent it (task451, task457, task469), and it
  moves only the last year of three.
- 2026-10-20, at the draw: serum against whole-blood results (a hospital's serum ethanol is about 1.16 times whole
  blood): a unit read correctly, data semantics; kept as Layer 1.
- 2026-10-20, at the draw: hit-and-run drivers, whose flight is selected on impairment: identified only through a
  later-identified subsample, a verified subsample whose rate the reader would transport directly; the guidelines
  count a crash through its identified drivers.
- 2026-10-20, at the draw: the guard's honest signatures: population with G14 first repeats task249 v4 inside the
  batch (same driver), G12 first repeats task268 v2's lineage inside the batch, E repeats task271 v1 and task268 v1's
  lineage; G6 first (the composition of each county's impaired drivers by BAC band) is the decisive rung honestly
  and blocks only on task268's recent G6 (ban.pattern, the last three live builds) and on older builds the card
  differentiates; the decision type is designation_set (the GHSO's high-range line), not a slate under a cap, which
  repeats task270's puzzle inside the batch.
