# task473 design note: Merrivale State's FY2028 high-range counties for impaired driving

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
- **World:** United States, an unnamed state. The Merrivale State University Center for Transportation Safety keeps
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
   were at .08 or more (7.5 per cent), and gave that probability to every untested, unarrested surviving driver of
   the other agencies; every killed driver and every arrested driver has a result.
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
is tested (28.6 per cent from .08 to .149 and 88.9 per cent at .15 or more), which certifies Tanager and drops
Pruett and Brisbin.

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

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, tested drivers only (Corwin, Hatchell, Ossian) | guidelines 2.2 says a crash counts whether or not its driver was tested: fires | the test status column beside the result: fires | none | none | none | one filter: fires | readable |
| R1, each untested driver at the county's tested share at .08 or more (seven counties) | none | the result column: fires | imputing a missing item at its observed rate: fires | none | none | one ratio per county: fires | readable |
| R6 (default path), one share of unarrested drivers impaired, from the agencies that test everyone, for every county (Corwin, Hatchell, Ossian, Pruett) | the manual's specimen sentence (blood after an arrest, or from every driver at the State Patrol and two sheriffs) sends the reader to the arrest flag: fires | the arrested-at-scene flag: fires | stratifying a missing item by the variable that selected it: fires | none | none | one ratio: fires | readable |
| R2, a logistic model of .08 or more on arrest and county fitted to the tested drivers (Brisbin, Corwin, Hatchell, Ossian) | none | the arrest flag: fires | the field's imputation of missing BAC on recorded covariates, police-reported involvement among them: fires | none | none | none | readable |
| R8, one arrest catch rate for every BAC (Brisbin, Corwin, Hatchell, Ossian) | none | the arrest flag against the results at the complete agencies: fires | none | none | none | one ratio: fires | readable |
| R5, the complete agencies' prevalence for every county and city survivor (Corwin, Hatchell, Ossian, Pruett) | the manual's specimen sentence: fires | the agency directory's type column: fires | transporting a completely observed subset: fires | none | none | one ratio: fires | readable |
| R4, untested survivors at the complete agencies' tested share (Corwin, Hatchell, Ossian, Pruett) | none | the agency type: fires | a completely observed subset's rate: fires | none | none | one ratio: fires | readable |
| R3, untested survivors at the county's killed drivers' share (seven counties) | none | the killed drivers' results: fires | the coroners' complete testing as the comparison: fires | none | none | one ratio: fires | readable |
| G (decisive), each arrest-triggered positive counted as one over the arrest's catch rate at its own BAC band, the band rates measured where every driver is tested (Corwin, Hatchell, Ossian, Tanager) | no clause names a catch rate, a BAC band, a weight or a detection model; the manual says only who draws blood from whom: silent | no column records how likely an officer was to notice a driver; the catch rate by band is a cross-tab of two columns at three agencies, applied to another population's positives by their own bands: silent | the reflexes are imputations from the tested drivers and transports of a complete subset's rate or prevalence: silent | no control, published rate or certified list scores a completion: silent | every file reconciles; nothing is missing that a sweep flags: silent | two band rates from one population applied to each county's positives band by band: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | high-range | a rate of 0.60 or more | more than 0.60 | same call: no county within 0.005 of 0.60 (asserted) | guidelines 2.4 "0.60 or more" |
| SF2 | 2023 to 2025 | the crash date in local time | the death date; the census file year | same call and every figure (asserted: no death in the window's crashes falls after 2025, and each file holds its own crash years) | guidelines 2.2 "a crash ... that occurred in 2023, 2024 or 2025" |
| SF3 | a death | a person who died within 30 days of the crash | any person with a date of death, the six recorded more than 30 days after a crash included | same call and every figure (asserted: those crashes had every driver tested below .08) | guidelines 2.2 "died within 30 days"; manual 3.1 |
| SF4 | a driver | an identified operator of a motor vehicle in transport, motorcycle riders included | pedalcyclists as drivers; pedestrians as drivers; unidentified drivers completed as untested ones | same call and every figure for pedalcyclists and the unidentified drivers (asserted); pedestrians as drivers move the call | guidelines 2.3 |
| SF5 | a BAC of .08 or more | the laboratory's whole-blood result as the census records it (three decimals, truncated) | more than .08; a serum value | same call and every figure (asserted: no driver's result sits on .080 or .150, and no census result is serum) | guidelines 2.2; manual 4.1 |
| SF6 | tested | a reported result in the person file (blood; vitreous humor only for some killed passengers and pedestrians) | vitreous read as no test | same call and every figure (asserted: no driver has a vitreous result) | manual 4.1 |
| SF7 | the county | where the crash occurred | the investigating agency's county; the driver's residence | same call and every figure (asserted: every census crash's agency is in the crash's county; residence is not recorded) | guidelines 2.2 "in the county" |
| SF8 | vehicle miles | the DOT's annual county VMT, daily miles times the year's days (366 in 2024) | 365 days every year | same call and every rate in its cell (asserted) | the DOT workbook's note on annual totals |
| SF9 | the rate | the three years' deaths over the three years' miles | the mean of three annual rates | same call (asserted) | guidelines 2.4 |
| SF10 | the catch rates | the two band rates pooled over the State Patrol and the Corwin and Ossian sheriffs | the State Patrol alone; the two sheriffs alone; four or six sub-bands | same call and every figure (asserted: the rates are equal at the State Patrol, at the two sheriffs together and in every sub-band) | the data's structure |
| SF11 | where the missed drivers sit | spread evenly over the county's untested surviving drivers | carried at each found driver's crash deaths; spread over the untested drivers in crashes not otherwise counted | same call and every figure (asserted) | guidelines 2.2 "each crash counts its deaths times the chance"; the data's structure |
| SF12 | a crash with two untested drivers | one minus the product of each driver's chance of being under .08 | the sum of the chances | same call and every figure (asserted) | guidelines 2.2 "at least one of its drivers" |
| SF13 | an untested killed driver | none: every killed driver was tested | the county's killed drivers' share | same call (asserted: none untested) | the records; manual 4.2 |
| SF14 | deaths in whole numbers | rounded from the completed count; the rate compared unrounded | the rate from rounded deaths; the rate rounded before the comparison | same call (asserted) | prompt "deaths ... as whole numbers" |

## Ladder

Built figures, read from the cut pack by `generator/checks.py` (rates per 100 million vehicle miles, 2023 to 2025).

- **R0, tested drivers only (Corwin, Hatchell, Ossian).** The seed's count; every crash with a driver whose result is
  .08 or more. Dies to guidelines 2.2: a crash counts whether or not its driver was tested. Tanager 0.44.
- **R1, each untested driver at the county's tested share (seven counties).** The arrest-only agencies' tested
  drivers are their arrested drivers, so their share at .08 or more is no guide to the drivers they let go. Dies to
  the manual's specimen sentence (4.2).
- **R6, the default path: one unarrested share for every county (Corwin, Hatchell, Ossian, Pruett).** 7.5 per cent of
  the complete agencies' unarrested surviving drivers were at .08 or more; given to every unarrested driver of the
  arrest-only agencies, it drops Tanager (0.51) and adds Pruett (0.63). Dies to the complete agencies themselves:
  their unarrested share differs between the State Patrol and the two sheriffs with their drivers' BAC mix, while the
  catch rate within each BAC band does not.
- **R2, a logistic model on arrest and county (Brisbin, Corwin, Hatchell, Ossian).** One arrest effect for every
  county; dies to the arrested positives' bands: Tanager's sit mostly below .15 and Brisbin's at .15 or more, and the
  complete agencies show an arrest catches 28.6 per cent of the first and 88.9 per cent of the second, so one arrest
  effect fits neither. Brisbin 0.63, Tanager 0.57.
- **R8, one catch rate for every BAC (Brisbin, Corwin, Hatchell, Ossian).** The complete agencies arrest 58.2 per cent
  of their impaired surviving drivers; dividing each county's arrested positives by it misprices every county whose
  positives sit at another mix of bands. Dies to the catch rate by band: 28.6 per cent at .08 to .149 and 88.9 per
  cent at .15 or more, the same at the State Patrol, at the two sheriffs and in every sub-band. Brisbin 0.72,
  Tanager 0.54.
- **R5 (Corwin, Hatchell, Ossian, Pruett), R4 (Corwin, Hatchell, Ossian, Pruett), R3 (seven counties).** Transports
  of a completely tested group's prevalence or tested share; each dies to the complete agencies' prevalence differing
  between them and from the killed drivers'.
- **G, the decisive move (Corwin, Hatchell, Ossian, Tanager).** Each county's missed impaired survivors are its
  arrested positives at .08 to .149 times five halves plus those at .15 or more times one eighth (one over 28.6 and
  88.9 per cent, less the positive itself); in Tanager 9 and 5 positives give 23.1 missed drivers over 89 untested
  ones.
- **Margins (cut pack):** the golden's nearest county is Kittredge, 5.4 per cent below the line, and Tanager sits 11
  per cent above it; R6 keeps Pruett 4.7 per cent above the line and every county at least 3 per cent from it, R2 and
  R8 likewise for Brisbin, and every one of R0, R6, R6c, R2, R8 and R5 leaves Tanager at least 2 points below the
  line.
- **Position, separation and dominance:** a designation, not a ranking: every rung names a set that differs from the
  golden in Tanager or adds Brisbin or Pruett; only the band-by-band completion brings Tanager in and keeps Brisbin
  and Pruett out together. The true deaths (every driver's BAC known, generator only) certify the same four.
- **Worth:** the call and the 14 rates; R6 keeps 2 of 14 rates and 1 of 14 deaths in their cells, so the asks carry
  the pair (Ask sheet).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | every death within 30 days of a 2023 to 2025 crash in the county with an identified driver at .08 or more, tested or not (guidelines 2.2, 2.3); the 14 counties |
| 2 | Unit of account | deaths per 100 million vehicle miles (guidelines 2.4); a death is a person, not a crash or a driver |
| 3 | Attribution window | the crash date in local time, 2023 to 2025 (SF2) |
| 4 | As-of dating | the census files as closed (each when its last 30-day window had passed, manual 1.2; the files dated 27 February 2025 and 25 February 2027), the DOT's final 2023 to 2025 DVMT (30 January 2027), the laboratory extract of 12 March 2027, the crash records extract of 8 March 2027 |
| 5 | Version basis | the closed census files; the 2024 report form from 2024 on |
| 6 | Denominator | the DOT's annual county VMT (SF8) |
| 7 | Weighting | the three years' totals (SF9) |
| 8 | Window length | three years (guidelines 2.4) |
| 9 | Boundary inclusivity | 0.60 or more (SF1) |
| 10 | Rounding path | rates computed and compared unrounded, reported to two decimals; deaths reported whole (SF14) |
| 11 | Tie-break | none: each county against the line |
| 12 | Maturity and censoring | the census files are closed with every death within 30 days and every tested driver's result |
| 13 | Order of operations | drivers' chances, each crash's chance that a driver was at .08 or more, its deaths, the county's sum, the rate |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | one person row per person; resubmitted specimens are the asks' (laboratory file), not the census's |
| 16 | Identity normalisation | agencies renumbered with the 2024 form (the directory's crosswalk); county codes in both forms |
| 17 | Netting | none |
| 18 | Dimensional units | BAC in g/dL (the 2011 form in thousandths); DVMT in thousands of miles a day |
| 19 | Code and status semantics | person types, injury codes and test codes in both forms (manual tables); never the stump |
| 20 | Integerisation | deaths whole after completion; rates two decimals |
| 21 | Clause scope | guidelines 2: the FY2028 designation on 2023 to 2025 |
| 22 | Forward window contents | the FY2028 designation on the closed window (a retrospective quantity with its reason, Draw) |

## Literal reader

Executed word for word, the guidelines fix the population (every death within 30 days of a 2023 to 2025 crash in the
county with an identified driver at .08 or more, tested or not), the unit, the ratio of the three years' totals and
the 0.60 line, and the manual says who is tested: coroners and the medical examiner test killed drivers, the State
Patrol and the Corwin and Ossian sheriffs every surviving driver, every other agency a surviving driver arrested at
the scene. One thing is left open: how the untested surviving drivers' BAC is completed. The candidates are the
tested share (R1), one unarrested share (R6), a model on arrest (R2), one catch rate (R8), a complete subset's
prevalence or share (R5, R4, R3) and the catch rate at each positive's band (G). The data separate them: at the
agencies that test every driver the catch rate is 28.6 per cent in every sub-band from .08 to .149 and 88.9 per cent
in every sub-band from .15, the same at the State Patrol and at the two sheriffs, while their unarrested share (7.1
against 12.0 per cent) and their prevalence differ with their drivers' mix, and the arrest-only counties' positives
sit at different bands (Tanager's 36 per cent at .15 or more, Brisbin's all); only the band rates are invariant, and
every member of G's family (pooled, the State Patrol alone or the sheriffs alone, two bands, four or six sub-bands,
missed drivers spread evenly, over the crashes not otherwise counted or at the found drivers' crash deaths, a crash's
chances combined or summed) gives the same four counties, every county's deaths in the same whole number and every
rate in the same two-decimal cell (checks.py). Guidelines 2.2 files the count as the number expected from the
records, each crash its deaths times the chance that a driver was at .08 or more, so the crash-level combination is
filed and the completion of each driver's chance is the open step. Every write-up step names the file and rule it
executes.

## Oracles

None that ties only under the golden. The complete agencies score a completion only by comparisons a solver chooses
to run; no published county rate, earlier designation or certified list ships. The laboratory's 2025 annual report
tables count kits received in 2025 by case type and the first reports' ethanol ranges statewide, a workload basis
(received dates, every kit) that ties with no county attribution and no arrest count, so it arbitrates nothing on
Ask A. Distractors: the licensed-driver counts by county (another denominator) and the 2026
preliminary census extract (another window), each named in metadata.json; neither ranks the counties on the
designation's basis.

## Ask sheet

- **Ask A, each county's 2025 impaired-driving arrests with a blood specimen at the State Toxicology Laboratory, and
  the per cent of those arrests at .15 or more: 28 figures.** H18 home: guidelines 3.1(a) makes them each task force
  application's baseline, so the certification carries them for every county; a measure every candidate carries
  that the call does not turn on. Path: the laboratory's specimen extract (case type, agency, agency case number,
  collection site, collection time in UTC, specimen type, analyte, result, report status), the agency directory (old
  and new agency numbers, county, State Patrol posts), the facilities list, the guidelines (3.1(a), the county where
  the arrest was made) and the laboratory's extract notes: five files, twelve columns.
  Primary device (re-sited after stage 4 reader 1): D1, the same records under two key schemes. A county jail's booking
  nurse draws some city police arrests and the jail submits its own kit under the sheriff's agency number and booking
  number beside the department's, so one draw sits in the extract twice, same collection site and minute, same
  result, under two agencies; one arrest per agency case number counts it twice. No sweep sees it (different lab
  numbers, agencies and case numbers). Kept as a hazard from the first cut: D7, the true key elsewhere. The State Patrol submits under one agency number for the whole state,
  and its arrests reach the county only through the post in its case number ("P07-25-01234") and the directory's
  post list; the laboratory's collection site is where the blood was drawn, and a rural arrest's blood is often
  drawn at the nearest hospital across the county line. Read by the agency's county or by the collection site, every
  county's arrests and share move; read by the post for the State Patrol and the agency's county for the rest, they
  are the golden. No sweep sees it: every specimen has an agency and a site, nothing repeats, and the statewide total
  is the same under every attribution.
  Hazards: collection times in UTC (New Year's Eve arrests change year; the lab number carries the year received),
  analyses reissued after review (the AMENDED report stands over the SUPERSEDED one), drug-only requests and
  cancelled requests (an arrest with a blood specimen and no ethanol result), two tubes in one kit, a second
  specimen under the same case number, serum results (whole blood is serum divided by 1.16), and the FATAL CRASH
  draws of drivers not arrested.
- **Ask B, each county's 2025 injury crashes in which no one died within 30 days and an officer reported a driver
  had been drinking: 14 figures.** H18 home: guidelines 3.1(b), the task forces' crash baseline. Path: the crash
  records system's 2025 report and unit extracts, the fatal crash census, the dictionary, the guidelines: four
  files, eleven columns. Primary devices: D1, the same crash under two agencies' reports (the State Patrol and a
  sheriff both report a crash on a state highway, two report numbers, the same vehicles and time, nothing linking
  them), and D9, a control true only in its scope. Re-sited after stage 4 reader 1, which merged the two agencies'
  reports and linked the census by report number: the census cites a county or city agency's death investigation
  number where a person died after the crash report, so a report-number link keeps those crashes as injury crashes;
  only date, road and time link them. Kept from the first cut (the crash extract keeps the severity the officer coded, so a crash
  whose injured person died within 30 days stays an injury crash there and is a fatal crash only in the census).
  Hazards: supplements under the same report number (the latest accepted stands, a rejected one never), a
  non-driver unit coded as drinking, crashes on private property, a supplement that lowers the severity to no
  injury, and a second agency's report of a crash that is in the census.
- **The construction layer:** the four counties, the 14 rates and deaths and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads no laboratory and no crash records row (the census
  carries each tested driver's result), so neither ask's device moves a call figure.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each county's 2025 arrests with a blood specimen and the per cent at .15 or more | one arrest per agency case number, the State Patrol's placed by the post in its case number, every documented hazard repaired (UTC, the amended report, drug-only requests, two tubes, second specimens, serum); the jail's second submissions counted as arrests, so every county's arrests and share fall outside their bins | miss |
| B, each county's 2025 injury crashes with no death within 30 days and a drinking driver | the latest accepted version, the two agencies' reports of one crash merged, drinking drivers on motor vehicle units, the census linked by agency and report number; the crashes the census holds under a death investigation number stay in, so every county's count falls outside its bin | miss |

- Mirror leakage: 0.0 per cent of ask weight (the asks read no rung's construction; every rung's response handles
  them as the cracker does).
- Pair ceiling: 28.5 on the cut pack (weights 38 / 7 / 55; the cracker keeps the main block and instructions, 45.0,
  and none of the 42 ask figures; the mirror, R6, keeps 2 of 14 rates and 1 of 14 deaths in their cells, 12.0).
- Measured by: generator/ceiling.py.

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** Domain: the deciding quantity is the field's own completed
  count, alcohol-impaired-driving deaths with the untested drivers completed, and the completion is a data
  integration of two observation mechanisms of one item (checks.py: every rung but G names another set). Layers: the
  mess (two report forms, renumbered agencies, thousandths against g/dL, DVMT in thousands a day with a leap year,
  the laboratory's UTC times, amended and serum results, second specimens and tubes, report supplements and a second
  agency's reports) is the systems' own and is neutral on the call (SF2 to SF8, the L1 assertions); the call reads no
  laboratory or crash records row. Three rules: no decoy or withheld rule ships (R3c), no field reading decides
  (every SF row converges or is ruled out by a filed sentence), and executing every filed rule with one share of
  unarrested drivers impaired certifies Corwin, Hatchell, Ossian and Pruett (R3a).
- **Free gates (2026-10-20):** checks.py 98 of 98, verify.py clean, two builds byte-identical, target.zip cut from
  the final build (18 files), figures_check.py 103 of 103, precut.py 51 checks clean, voice-check clean, guard.py
  surface clean and heart WARN after a pull (shape and Gate G overuse, answered at the draw), containers clean.
- **leak.py REVIEW lines, each harmless:** the guidelines carry the program's own name (high-range, FY2028, County
  Impaired Driving Task Force grants), which the call repeats; the manual, the guidelines and the laboratory's and
  crash records system's notes carry the domain's nouns (drivers, tested, arrest, agency, records), and none names a
  catch rate, a band, a weight or a completion (R3c asserts the absence through the same extractor as its control).

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
- 2026-10-20, at the build: each complete agency's band counts made whole multiples of the catch denominators, which
  left the Corwin sheriff with no impaired surviving driver in three years; replaced by the two sheriffs pooled for
  exactness beside the State Patrol, with catch rates 2/7 and 8/9 so that no rate reads as a round 30 or 87.5 per
  cent.
- 2026-10-20, at the build: the golden family spread up to 0.02 in a rate because untested survivors at county and
  city agencies sat in crashes already counted through a killed impaired driver and in two-survivor crashes; the
  arrest-only agencies' multi-vehicle shares lowered and their at-fault drivers made seldom the one killed, so every
  member of the family prints the same figures.
- 2026-10-20, at the build: fixed year shares gave every county the same crash count in 2024 and 2025; each county's
  years drawn from a multinomial instead.
- 2026-10-20, at the build: the manual stated the 2024 and 2025 files' closing dates although issued in March 2024;
  the dates cut, the rule kept.
- 2026-10-20, at stage 4: Ask A's State Patrol attribution and Ask B's two-agency duplicates as primaries; reader 1
  found both (the post in the case number, a time-and-place merge) and kept 17 of 70 ask figures, its only Ask A
  misses coming from dropping cancelled requests, a reading rather than a device. Both kept as hazards; cancelled
  requests kept out of 2025; primaries re-sited to the jail's second submissions (Ask A) and the census's death
  investigation numbers (Ask B).
