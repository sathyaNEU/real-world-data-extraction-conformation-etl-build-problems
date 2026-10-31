# task181 design note (architecture 5: where the city's dengue is caught)

Architectures 1 to 4 are spent and in the card's lineage, with the weather draw that opened this re-root (v5a,
killed at the draw). This architecture leaves criminology: the cell's decisive-step space was enumerated closed
by task182's architecture 8 (sixteen candidates, each dead to a standing screen) and this pass added the
weather-conditioned violence draw to that list. The re-root directive's fallback moves the build to another
anomaly-detection client domain, and epidemiology carries an honest stump here.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task181.json` (v5), registered 2026-10-31. `guard.py check` on the
  registered card: PASS, one NOTE (test.same_driver_older, differentiated against task487, whose driver dates
  inspection-found events inside their windows); nearest driver 0.08 (task121 v3, lineage).
- **Pairing.** `epidemiology-public-health` / `disease-surveillance-outbreak-anomaly-detection` (serves AD and DQ),
  objective Anomaly Detection & Diagnostics: a real outbreak separated from the place the records put it. Client
  domain epidemiology-public-health. The task type carries one anomaly-detection card on file (task188, West Nile
  pools) and this slot's own architecture 2 (pertussis, another world and dataset).
- **World.** Dalisay City, a component city in Laguna province, Philippines (PHP), about 840,000 residents in 36
  barangays (Santo Tomas Norte split from Santo Tomas in March 2025). The City Health Office's epidemiology and
  surveillance unit (CESU) keeps the dengue line list fed by two hospitals, six city health centres and three
  private clinics. The Dalisay Industrial Estate, an export processing zone inside Barangay San Roque, employs a
  large share of the working residents of six barangays of boarding houses beside it and houses almost nobody;
  San Roque's own residents live in its old village. Neighbouring towns (Pinagbuklod, Kalinaw, Sinagtala,
  Masilaw), the two hospitals, the three clinics and the Laguna Bay Inter-Local Health Zone are invented. People drawn with `guard.py names --geo PH
  --seed 181`: John Figueroa (city health officer), Tammy Orozco (CESU head).
- **Decision.** On Monday 11 October 2027, the start of morbidity week 41, the city health officer sends the
  hotspot response (search-and-destroy, larviciding, targeted space spraying, case finding, clean-up) for weeks 41
  to 44 to every barangay that meets the plan's trigger: 40 or more of the city's notified cases with onset in
  weeks 37 to 40 infected in the barangay. The decision faces forward (the next four weeks' response); the
  quantity is the closed window just behind it, because the plan triggers on the latest four complete weeks.
- **Quantity.** Each barangay's count of the window's notified cases that were infected there.
- **Data-native sentence.** A dengue notification records the barangay the patient sleeps in, because the case
  investigation form takes the home address, while Aedes aegypti feeds in daylight, so a working adult's infection
  is caught where the working day is spent; in a city whose export zone employs a large share of several
  barangays' residents and houses almost none, an outbreak at the estate is recorded in the barangays its
  workforce sleeps in.
- **Default path's answer:** the two outbreak barangays and the six barangays beside the estate (eight by home
  address at 47 to 86 cases). **Golden:** San Roque, Bagumbayan and Maligaya.
- **Shape.** `other`: a designation over every barangay. Criteria: each barangay sent the response (3), each of
  the six beside the estate correctly left out although over the trigger by home address (6), the rest left out
  (1), the chart's named parts (bars per barangay, the trigger line, the three in red: 3 to 4), the two files (2),
  and the asks' 40 figures (hospital admissions 16, house indices 12, laboratory first positives 12).
- **Strategy and family.** `causal_design` (interference between units: outcomes recorded in one barangay caused by
  exposure in another through daily travel); Layer 2 family `estimand_identification`; Gate G
  `decomposition_attribution` (each barangay's correctly reported cases assigned to the barangay where they were
  caught); gap population then objective; generators G7 (the vector's feeding hours decide where a case is
  caught) and G6 (the working-age band moves against the rest).
- **Axis values drawn against the window** (tasks 464, 273, 268): forum operations_desk (the dengue desk dispatches
  the teams), forcing_event period_close (the four-week window closes), org_family local_government, role
  operations_director (the city health officer), context artifact monitoring_export (the line list export).
  season_or_peak was the first forcing value and is banned by task273; the window closing is the honester label,
  since the trigger is read the Monday a window closes.
- **Abstraction sentence.** Written against every approved build, no shared sentence holds: task175 reads a unit's
  attribute at the neighbours it faces, task179 links two bodies' records person by person, task182 conditions
  each unit on its own response to an outside driver, task236 reads a notified share against a sentinel rate,
  task275 raises observed catch by unobserved effort, task303 removes events every sibling opened in one minute.
  Here the recorded unit is not where the event was caused, and the place is recovered through the daily travel
  of the people the events happen to. The spent family nearest it is task268's (people present against
  residents), which died because there the estimand named presence; here it names the place of infection, and
  no file says where any infection happened.
- **World selection.** The generator takes world seeds in order and keeps the first whose clean truth meets the
  design (`generator/design.py`: every placement that puts working residents' exposure at work files the golden,
  each easy route misses, no shock-sort interval) and whose cut pack keeps margins of 12 inside and 6 outside the
  trigger (3.5 at a half share). Seed 0 met the truth and missed the cut-pack half-share margin (1.8), seeds 1 and 2
  fail the clean truth (a barangay beside the estate under 40 by home address) and seed 3 is the first to meet both;
  `generator/seeds.py 0 1 2 3` prints the screen.
- **Sources.** All data synthetic, generated by `generator/` (CC0 for this pack). The world follows the Philippine
  notification practice for dengue, the Community-Based Monitoring System tables an LGU holds and the barangay
  response of the dengue programme; no real person, office, zone or town of the pack is represented.

## Default path

1. Read the plan's trigger: 40 or more of the window's notified cases infected in the barangay.
2. Load the line list (2022 to 2027), keep each case number's latest row, drop the notifications classified Not a
   case and the residents of other towns, merge the patients notified by two units, map the barangay spellings and
   the Santo Tomas split, date each case by onset (consultation where onset is blank).
3. Count each barangay's cases with onset in morbidity weeks 37 to 40 by the barangay the notification records,
   the surveillance system's place of a case and the field's reading of where a locally acquired case was caught.
4. Flag every barangay at or over 40.

Ends on: Bagumbayan, Maligaya, Tabing-Ilog, Pulong Bayabas, Malinta, Kanluran, Burol and Silangan
Golden: San Roque, Bagumbayan and Maligaya

## Stump sentence

The default path counts each barangay's notified cases by the barangay of residence and presents Bagumbayan,
Maligaya, Tabing-Ilog, Pulong Bayabas, Malinta, Kanluran, Burol and Silangan; the step that lands it there is
taking the home barangay as the place of infection, when Aedes aegypti bites by day and the six barangays' rise is
all among working-age residents, the six barangays sending the most workers to the estate in San Roque, so those cases
were caught in San Roque, whose own residents number 14 of the window's cases.

## Three rules

Task type: disease-surveillance-outbreak-anomaly-detection (Epidemiology & Public Health), which serves anomaly detection: a real outbreak separated from the place the records put it.
Domain test: the quantity that decides is each barangay's count of the window's notified dengue cases infected there, and vector-borne disease surveillance places an infection where the person was while the vector feeds; Aedes aegypti feeds in daylight, so a working adult is exposed mostly where the working day is spent.
Swap: "Which barangays need the malaria response?" reads differently, because Anopheles feeds at night and the home is then the place of infection; put influenza or road injuries in and there is no feeding window to place an infection at all, so the task stops making sense.
Layer 1: the online system's export with migrated 2022 to 2024 rows (codes S, P, C, X and blank travel fields), Update rows under a case number, patients notified by two units under two case numbers, barangay names as each unit spells them, Santo Tomas Norte written under its parent barangay before and sometimes after the 2025 split, dates day-month-year from the centres and year-month-day from the hospitals' online submissions, residents of other towns not yet forwarded, blank onsets, the CBMS workbook's multi-row headers, merged cells, dashes for zero and footnotes; each is produced by the system that records it and none is placed to be caught.
Layer 2: estimand_identification, the place of infection: each barangay's record is contaminated by infections caught in another barangay, and the choice that flips the call is placing the working residents' excess where they spend the day.
Decisive step: placing each barangay's cases where the patients were during the mosquito's daylight feeding, through the CBMS place-of-work table, instead of at the home address the notification carries.
Not semantics: reading every field and the plan's "infected in that barangay" correctly still leaves the easy route on the home-address counts, because no file records where any infection happened; the line list carries only the home barangay, and the place has to be estimated from the vector's feeding hours, the working-age band of the rise and the place-of-work table.
Not rule application: no filed rule says where an infection was caught, so executing the plan's trigger on any placement files whatever that placement gives; the enumerated family (home barangay; home with travellers out; by consultation week; the children's and older residents' rate as a home-transmission marker; place-of-work placements at a half, 0.6, 0.7, 0.8 and all of a working resident's exposure, with the outside-city share kept or dropped; the excess spread by the place-of-work shares; the inversion of the place-of-work table) files three different sets (the eight by home address, the two outbreaks alone, San Roque with the two outbreaks), the standing family (the placements that put working residents' exposure where they work, which daylight feeding requires) files San Roque, Bagumbayan and Maligaya at every member measured, its cheapest member (each working-age case split by the CBMS employment rate and place-of-work shares) included, and no clause or column does the ruling-out, only the biting hours and the rise's proportion to each barangay's estate workforce.
Analyst test: a strong analyst merges the re-notified patients, sets non-cases and residents of other towns aside, maps the spellings, counts each barangay's cases with onset in weeks 37 to 40 by home address and flags Bagumbayan, Maligaya, Tabing-Ilog, Pulong Bayabas, Malinta, Kanluran, Burol and Silangan; every field is read and the trigger executed, and the call is wrong because the cases are counted where people sleep while they were caught at the estate.
Estimand: dalisay_dengue_plan_2027_section4.pdf, section 4.3 with 4.1 and 4.2: population, the city's notified dengue cases (residents, not classified Not a case, one case per patient) with onset in morbidity weeks 37 to 40 as notified by 08:00 on Monday 11 October 2027; outcome, the barangay where each was infected; window, weeks 37 to 40 of the calendar the plan files; unit, the barangay; comparison, 40 or more.
No decoy: nothing is planted to be caught; no memo, draft, briefing or stakeholder figure argues the home-address count, the vector control log ends before any residence-based assignment of 2027, and the line list's home barangay is what the notification form records.
No certified replay: no certified or published figure reproduces the method; no file carries any barangay's infections by place, and the zone bulletin carries only city totals.
Lesson: a case record's location is where a person sleeps, and for a day-biting vector the place of infection is where the person spends the day; a model that gets this right learns to ask where exposure happens before reading a surveillance map, which no build on file teaches (task268 was about the people present, task188 about pooled mosquito tests).

## Survivor anatomy

Actor: the deciding property, where each case was infected, has no column in any file; the line list carries the home barangay and the age, the CBMS table carries where each barangay's working residents work as counts and never per case, and the property is a relation between the cases' age band and home and the place-of-work flows.
Link: no key ties a case to a workplace, and the comparison that finds the place (each barangay's working-age excess against its estate workforce in the CBMS table) is one the residence-based surveillance method never asks for; no sentence invites it.
Reflex: the field's method, cases by barangay of residence against the trigger (the surveillance system's place of a case), is rung 0 and files Bagumbayan, Maligaya, Tabing-Ilog, Pulong Bayabas, Malinta, Kanluran, Burol and Silangan.
Back-test: the textbook route validates; in every season 2022 to 2026 the barangays the residence count put over the trigger had surges across every age band, and the vector control log records the hotspot responses there, because transmission then was residential.
Second use: every file the decisive step reads has its own reason to be in the pack; the line list is the surveillance record, the CBMS workbook carries the population by age the plan's rates and the home-transmission comparisons need (its place-of-work sheet is part of the same LGU release), and the plan files the trigger.
Shock: San Roque's home-address count is ordinary (14 cases), nowhere near the pack's largest, and the golden set is not an interval of any sort of the barangays (home-address count, rate per resident, working-age share of cases, week-on-week growth, children's cases), asserted in checks.py.
Pins: the WHAT sits in the dengue plan (population, place of infection, window, unit, trigger) and no filed sentence names where infections happen, the vector's biting hours, workplaces, the place-of-work table or any placement method; deleting the trigger sentence unforces the call and that sentence names no step.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 home-address count | 4.3 is the trigger | the barangay column | the field's method | none refutes it | the battery runs it | one group-by | none | readable |
| 1 travellers and other towns out, onset dating | 4.1 and 4.2 file them | travel and town columns | battery item | none | yes | filter | none | readable |
| 2 children's and older residents' rate as a home marker | none | age column | an epidemiologist's check | none | a by-age table | one ratio | none | readable |
| 3 (decisive) working residents placed at their workplaces | none names a place, a workplace or biting hours | no column holds a place of infection | not the surveillance reflex | no file ties a barangay's infections by place | no battery item | not affine in a shipped column | the CBMS table carries the plan's denominators | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | notified dengue cases | suspect, probable and confirmed | confirmed only | different counts | plan 4.1: "A notification the CESU has classified Not a case is not a case" |
| SF2 | a patient notified by two units | one case | two cases | same call (asserted) | plan 4.1: "A patient notified by two units is one case" |
| SF3 | residents of other towns on the export | not the city's cases | counted at a same-named barangay | same call (asserted) | plan 4.1: "Cases among residents of other cities and municipalities ... are not the city's cases" |
| SF4 | the week of a case | onset week | consultation or report week | same call (asserted for consultation week) | plan 4.2: "A case belongs to the week of its onset of fever" |
| SF5 | blank onset | dated by first consultation | dropped | same call (asserted) | plan 4.2: "a case whose onset is not recorded is dated by its first consultation" |
| SF6 | as notified by 08:00 Monday | the export of 11 October | a later extract | not shipped | plan 4.3 and the export's last report date, 10 October |
| SF7 | morbidity week calendar | Sunday to Saturday, week 1 from 3 January 2027 | ISO weeks from Monday | same call (asserted) | plan 4.2 |
| SF8 | 40 or more | at least 40 | more than 40 | same call (asserted: no barangay at 40 under any placement) | plan 4.3 |
| SF9 | cases that travelled outside the city | placed with the rest | set aside | same call (asserted) | none needed |
| SF10 | Santo Tomas rows of Puroks 5 to 8 | Santo Tomas Norte | Santo Tomas | same call (asserted) | the register: Norte created from Puroks 5 to 8 |
| SF11 | infected in that barangay | the barangay where the infection happened | the barangay the notification records | the home barangay is where a case lives; 4.1 calls the line list's cases the city's residents and 4.3 counts where they were infected | plan 4.1 and 4.3 |
| SF12 | the CBMS outside-city column | kept as a share no city barangay receives | dropped and the rest renormalised | same call (asserted) | none needed |
| SF13 | a working resident's share of exposure at work | any from a half to all of it | none | same call (asserted at 0.5, 0.6, 0.7, 0.8, 1.0) | none needed |
| SF14 | the working-age band | 15 to 64 | 20 to 64 | same call (asserted) | CBMS Table 1 bands |
| SF15 | the history behind a barangay's usual age mix | 2022 to 2026, all weeks | the same weeks 37 to 40 of each year | same call (asserted) | none needed |
| SF16 | the window's cases that are not dengue after all (suspects not yet classified) | counted, as notified | dropped | same call (asserted, none identifiable) | plan 4.1 counts every notification not classified Not a case |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 0 | each barangay's window cases by the barangay the notification records (the surveillance system's place of a case) | Bagumbayan, Maligaya, Tabing-Ilog, Pulong Bayabas, Malinta, Kanluran, Burol, Silangan | the six beside the estate rose only in working-age residents (1 to 4 children's cases each against 44 to 57 working-age), and they send San Roque the most workers in CBMS Tables 3 and 4 (4,437 to 4,626 each, 29 to 39 per cent of their employed residents; the next barangay 864) |
| 1 | rung 0 with travellers set aside and cases dated by consultation | the same eight | the same fact |
| 2 | the children's and older residents' rate carried to each barangay's population (a home-transmission marker) | Bagumbayan, Maligaya | the working-age excess of the six has to be placed somewhere, and Table 4 puts their workers in San Roque |
| 3 (decisive) | each barangay's working-age cases placed where its workers work (any share of the day from a half to all of it, the excess spread by the shares, or the inversion of Table 4) | San Roque, Bagumbayan, Maligaya | the golden |

- **Margins on the cut pack** (asserted in checks.py): under every standing member the three are at least 17.0 cases
  over the trigger (Maligaya at 57.0, the whole working day at work with the outside-city share dropped) and every
  other barangay at least 8.8 under it (Silangan at 31.2, a share of 0.6), 4.4 under it at a half share (Silangan at
  35.6, the weakest member); San Roque's count runs 67.7 (a share of 0.6, the outside-city share dropped) to 465.2
  (inversion). checks.py prints each of these figures after its assertions. By home address the eight sit 7 to 46
  over the trigger and San Roque 26 under it.
- **Pricing sequence.** (1) The residue the filed WHAT leaves is the place of infection, a method rather than a
  knob. (2) San Roque has to move from 14 to over 40 and the six beside the estate from 47 to 58 down to under 40;
  the working-age excess the placement moves is 388 cases city-wide, 270 of them in the six, far past both. (3) The one-group-by route
  (cases by barangay and age band) shows the six barangays' working-age rise and does not produce San Roque, whose
  count comes only through Table 4; no route is affine in a shipped column. (4) Across the standing family San
  Roque's count spreads 67.7 to 465.2 and the six's 3.3 to 35.6, every member on the same side of 40; a
  barangay's working-age count has a Poisson spread of about 7 against outside margins of at least 8.8 from a share of 0.6 up (4.4 at a half share).
  (5) and (6) No variance is corrected. (7) No subset of rows prints a place of infection: the children's and older
  residents' rate gives each barangay's home transmission and misses San Roque (rung 2). (8) The reflex sweep runs
  as code: rungs 0 to 2, the five shares with the outside column kept and dropped, the excess spread and the
  inversion (checks.py R3 block).
- **Separation.** The default path is wrong on the clean truth (R3a) and the default path with only the placement
  changed files the golden (R3b); the children's marker, the one obvious correction, files the two outbreaks
  alone.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the city's notified cases, residents only, one per patient, not classified Not a case | filed in plan 4.1 and 4.3; C1 for re-notifications and other towns (asserted) |
| 2 Unit of account | a case (a patient) | filed in plan 4.1 |
| 3 Attribution window | onset in weeks 37 to 40 | filed in plan 4.2 and 4.3 |
| 4 As-of dating | notified by 08:00 Monday 11 October | filed in 4.3; the export ends at 10 October |
| 5 Version basis | each case number's latest row | the export's report order; C1 (classification changes move no barangay across 40) |
| 6 Denominator | none (a count) | the trigger is a count |
| 7 Weighting | none | the trigger is a count |
| 8 Window length | four weeks | filed in 4.3 |
| 9 Boundary inclusivity | 40 or more | C1: no barangay at 40 under any placement |
| 10 Rounding path | placed counts compared unrounded | C1: no placed count within 4 of 40 |
| 11 Tie-break | none needed | no ties at the trigger |
| 12 Maturity and censoring | cases not yet notified by the extract are out | filed in 4.3 |
| 13 Order of operations | clean, then place, then count | C1: placing before or after merging re-notifications gives the same set (asserted) |
| 14 Row order | export order | C1 over permutations (latest row by report date) |
| 15 Duplicate resolution | a patient notified twice is one case | filed in 4.1; C1 (asserted) |
| 16 Identity normalisation | barangay spellings, the Santo Tomas split | the register and the purok; C1 (asserted) |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | counts | not applicable |
| 19 Code and status semantics | S, P, C and X in migrated rows | the classification words in later rows; X is Not a case (plan 4.1) |
| 20 Integerisation | placed counts are fractional | C1: the set is the same rounded or not |
| 21 Clause scope | 4.3 applies to every barangay | filed |
| 22 Forward window contents | the response runs weeks 41 to 44 | the call is the set; nothing forward is graded |

## Literal reader

Executing plan 4.1 to 4.3 word for word gives the city's notified dengue cases (residents, one per patient, none
classified Not a case) with onset in weeks 37 to 40 as notified by 08:00 on 11 October 2027, counted by the
barangay where each was infected; no file records a place of infection, so every literal reading has to estimate
it, and every estimate that puts a working resident's exposure where the resident works files San Roque,
Bagumbayan and Maligaya, while taking the home as the place (an easy method on the same literal estimand, not a
reading of the sentence) files the eight by home address.

## Oracles

- The CBMS place-of-work table is the decisive input, not a control: it ties no barangay's infections to a place.
- The larval survey covers twelve ordinary barangays in September and none of the six beside the estate, the two
  outbreaks or San Roque, so no house index confirms or refutes a placement.
- The zone bulletin carries city totals only; the vector control log ends on 31 August 2027, before any 2027
  window put a barangay at 40 by home address, so it records no assignment for this decision.
- none ties only under the golden.

## Ask sheet

| Ask | Figures | H18 home and use | Primary devices (block) | Hazards | Files and columns on the path |
|---|---|---|---|---|---|
| A | each hospital's dengue admissions, weeks 33 to 40 (16, whole numbers) | the city's bed planning beside the response (plan 4.4) | D6/D1 a stay's ward segments under one hospital number with the disposition only on the last segment, readmissions as new stays (DMC block); D7 a patient moved from DMC to DDH admitted again under an DDH number with no shared key, matched by age, sex, address and hours (DDH block) | DDH's dates month first; DDH's weekly sheets closed at 17:00 Saturday | dmc_dengue_inpatient_census_2027.csv (hospital_no, ward_in, ward_out, disposition, age, sex, barangay, city), ddh_dengue_admissions_2027.xlsx (every sheet: Patient No., Age, Sex, Address, Date and Time Admitted), plan 4.4 |
| B | each surveyed barangay's house index, September 2027 round (12, per cent to one decimal) | a measure every barangay carries that the call does not turn on | D6 the VCU tablet's one row per container (VCU block); D7 the health workers' house numbers restarting in each purok, follow-up visits under the same number (BHW block) | follow-ups mostly negative after search-and-destroy | larval_survey_2027_09.csv (team, barangay, purok, household_code, larvae, pupae, containers_positive), plan 4.6 |
| C | patients whose first positive dengue test was an NS1, and an IgM, weeks 35 to 40 (12, whole numbers) | the laboratory's confirmations beside the response (plan 4.5) | D2 four NS1 runs rejected for a high negative control, their results left in the export beside the repeats (NS1 block); D7 a follow-up specimen from another facility under a new laboratory reference, the person known by initials, birth date and sex (IgM block) | equivocal IgM results | cho_lab_dengue_results_2027.csv (patient_ref, patient_initials, date_of_birth, sex, collected_on, test, result, run_id), cho_lab_run_log_2027.json (run_id, qc), plan 4.5 |

- **Stops (cut pack; each verdict is a checks.py assertion).** A, DMC: every segment an admission (misses every
  week), a patient once by hospital number (misses most weeks, readmissions lost), the golden stitch. A, DDH: every
  row by date admitted (moved patients counted twice, misses most weeks), the rows by sheet week, the golden match.
  B, VCU: rows as houses (a container index), houses by number (golden). B, BHW: houses by number across puroks
  (misses every barangay), the last visit kept, houses by purok and number (golden). C, NS1: every positive row with
  the rejected runs left in (misses at least four weeks), first positive with the run log applied (golden). C, IgM:
  every positive IgM specimen, first by laboratory reference (misses every week), first by person (golden). The
  ceiling (generator/ceiling.py) scores the cracker's stop per ask on the cut pack.
- **Pin test.** A's sentence carries the window and the hospitals; plan 4.4 files the WHAT (a patient moved between
  the hospitals is one admission at the first) and the device lives in which records are one patient, which no
  key settles. B's sentence carries the round; plan 4.6 files the house index, and the devices live in the grain
  and in which number is the house. C's sentence carries the window and the two tests; plan 4.5 files the week of a
  result, and the devices live in which runs reached the export validly and which references are one person.
- **Realism.** Each device is how the producing system writes its records: a census row per ward segment, a records
  clerk logging a transferred patient as a new admission, a tablet form with a row per container, health workers
  numbering houses within their purok, an ELISA plate repeated after failed controls, and a request form issued
  per facility.
- **Separation.** No ask file is read by the call; the line list's admitted and laboratory columns cannot rebuild
  any ask figure (the hospitals admit residents of other towns, the laboratory tests patients the line list does
  not hold), asserted in checks.py.

| Ask | Cracker (lands the call, runs the battery, reads the plan's definitions; hospital numbers as given, the hospitals' moved patients kept at both, the form's house numbers, the laboratory's references) | Verdict |
|---|---|---|
| A | counts each patient once by hospital number and every DDH row by its admission date: 1 of 16 figures kept | miss |
| B | groups the rows by household number within a barangay: the six VCU barangays kept, the six BHW barangays missed | miss |
| C | applies the run log at best and reads a patient by the laboratory reference: the NS1 block kept, every IgM figure missed | miss |

- Mirror leakage: 32.5 per cent of ask weight, measured on the cut pack (the residence-count response runs the same
  battery and keeps the same 13 of 40 ask figures).
- Pair ceiling: 46.4 (cracker 38 + 7 + 55 x 0.325 = 62.9; mirror 5 + 7 + 55 x 0.325 = 29.9), each response under
  two fifths of the ask weight.
- Measured by: generator/ceiling.py on the cut pack: each response's ask figures recomputed from target/ with its
  handling and scored against the golden handling on the same files; the full includer, resolving every device,
  keeps 40 of 40.

## Leak review

`leak.py task181 --asof 2027-10-11` on the final cut: REVIEW, no LEAK. Each line is ruled here; the stage 4 reader's
verdicts go to leak_check_report.md under its own heading.
- Sweep 3, a figure in the plan PDF: the number of the plan's laboratory section (4.5), which coincides with one house
  index; not a figure.
- Sweep 3, words of the call in the plan PDF: hotspot response, morbidity weeks and barangay are the plan's own terms
  for the response it governs; the plan names no barangay.
- Sweep 4, stump-paragraph words in the plan PDF (window, residents, record, records, vector, health): the plan's
  operational language (the case window, the residents it counts, the Vector Control Unit, the City Health Office);
  it names no move and never mentions work, travel, the estate or a home address.
- Sweep 6, barangays beside numbers in the PSGC register, the CBMS workbook, the DDH log, the line list and the VCU
  log: each carries its own quantity (codes and populations, census tables, admissions, notifications, operations to
  31 August); none counts the window's cases by barangay or ranks the barangays on where cases were infected.
- Sweep 12, column words in the plan PDF (Barangay, admitted, laboratory, larvae, pupae): the plan's definitions of
  the response, an admission, a result's week and the house index, in the organisation's governing document; it
  glosses no column.
- Single-use test: every file has its genre's other uses (the register its codes and boundary notes, the CBMS
  workbook its population, employment and place-of-work tables, the plan its six sections). Plan 4.3 files the WHAT
  (cases infected in the barangay), which the fork table needs: deleting it leaves the residence count a literal
  reading of the trigger (SF11).

## Pre-ship check

- **The three rules against the built pack.** The deciding quantity is each barangay's window cases placed where they
  were infected, worked as vector-borne surveillance works it (a day-biting vector, the census place-of-work flows).
  The mess is the online system's export and the CBMS workbook's form; cleaned, the residence count still files the
  eight (rung 1), so the stump is not Layer 1. The decisive step is the placement, an analytical choice (R1 to R3 in
  checks.py).
- **Gates on the final cut.** Generator checks 73 of 73, verifier 16 of 16, two byte-identical builds, figures_check
  81 of 81, precut 61 checks with 0 FAIL, voice-check PASS, leak.py REVIEW with every line ruled above,
  guard.py heart PASS (one NOTE, differentiated against task487), surface with one NOTE (Santo Tomas, a barangay, read
  as a persona), ceiling 46.4 for the pair with 32.5 per cent mirror leakage, target.zip cut by generator/zipcut.py.
- **Stage 4** (the leak reader and the determinism judge) runs from the main thread, because a fork cannot spawn them.

## Tried and rejected


- Architecture 1 (a credit union's counterfeit wave traced to two skimmed terminals behind a dominant common point):
  spent at in-house round 1, where a solver explained the co-visited sites away as subsets of the dominant source's
  victims and re-screened the residual; any further rung falls to the same subset check or opens a fork.
- Architecture 2 (a public health unit's pertussis line list, the fortnight completed by laboratory route): stumped
  in-house only while the estimand was open; the portal's determinism QC called it a fork, and once the eventual count
  was filed literally a per-laboratory completion landed it (96.8), and any filed criterion choosing the delay history
  names the step.
- Architecture 3 (a housing association's estates, near-repeat burglary runs against each estate's background):
  spent at design; a filed back-test on about ten break-ins per estate-quarter cannot select the background projection
  on honest data (the usual winter wins the back-test in most seeds), and nothing short of a planted smoothing closes it.
- An airspace-change safety case on losses of separation per flight hour against interactions, read retrospectively
  (which sector's 2026 losses most exceed its traffic): the industry keeps losses per 100,000 flight hours as its
  standard rate, so "beyond what its traffic explains" is a fork between that rate and the interaction rate; the
  forward count with the tolerance filed literally removes the fork.
- Forklift and pedestrian near misses scaled by the product of zone occupancies: the product of two counts is a
  mass-action reflex for a quantitative solver, so the decisive rung is readable.
- Rail signals passed at danger per approach at red: a stop-aspect exposure is the first thought once an aspect log
  ships (a solver reasons that only a red signal can be passed at danger).
- Hospital ward acquisitions of a resistant organism per colonised patient-day: colonisation pressure is infection
  prevention's own reflex, and under mass action it equals the colonised-day rate the reflex computes.
- A survey's regional estimate moved by a gradual shift to web interviewing, separated by its randomised-mode
  subsample: the randomised arm is a schema cue a solver uses at once.
- Excess deaths in a heatwave net of mortality displacement: once the window is filed literally the net excess is a
  reading, and the field is architecture 2's.
- Ambulance mileage, impossible days, upcoding against audit-log time, check kiting on uncollected funds: each turns on
  a filed rule or a field read correctly (rule application or data semantics).
- A workload ceiling crossed in saturated hours (errors by occupancy band applied to a 2027 staffing plan) and a queue's
  ageing into a 52-week breach: both are state-based forward projections, the family task183 and task132 already hold.
- The first cut shipped a workbook and a PNG chart as the goldens, the pair task183 shipped the same day; the surface screen put the two builds at 0.100, so the goldens became the review board deck and a measures CSV.
- The first cut graded every sector's forecast at one decimal: the seven sectors under the line fork between the
  pooled losses per pair and each sector's own ratio (Linmark 24.1 against 25.6, Lysvik 26.4 against 24.9), so the
  deck grades the set over the line and Tarvik's rate, and the other seven as under 30.
- The delay ask with the slot list's plans that never reached the flight data left unfiled: read literally, every
  sector's delay moved at two decimals; the extract notes now file the network manager's definition (counted for the
  flights that operated).
- A configuration log remark of a sector bandboxed briefly and reopened minutes later with no logged change: deducting
  it moved Tarvik's hours open alone to 1,531.7, so the remark left the log's vocabulary.
- Architecture 4's stage-2 magnitude repair (widen the separation at the decision with the call, the decisive step,
  the prompt's asking sentences and every ask figure's unit and rounding frozen): refused on measurement 2026-10-21.
  Screen 1 passed, 25 constructions spreading Tarvik 8.7 to 79.9 per 100,000 flight hours (spread 71.3), so the step
  is not a reflex. Screen 2 passed, the decisive construction is nothing like an identity in the one-group-by route
  (corr -0.5110 and max absolute difference 59.00 against each sector's 2026 rate per flight hour, affine R2 0.2611;
  the best cheaper route is the level-changing-traversal rate at corr 0.7593 and max absolute difference 36.22). Screen
  3 refused: the tolerance window that clears every easy route by 1.15x and keeps every licensed construction over by
  1.15x is empty by a factor of 2.11 at the shipped magnitudes and empty at every setting of the dial.
- Raising the safety plan's tolerance (40.0 to 45.0 or 47.0) so the line sits clear of the reflexes: dead. It fixes
  the near misses (hourly entries squared pooled 37.7, vertical hours pooled on 2026 36.6, level-changing traversals
  pooled on the record 36.2, all inside 1.15x of 40.0) and it cuts the licensed family in two, because the weakest
  licensed construction puts Tarvik at 26.5 and any line clearing the easy routes sits at 48.6 or above.
- Raising the new Brekka base (14, 20, 26, 33, 40, 50 flights a day each way, the record held and the whole generator
  re-simulated at each setting): dead. It widens the golden strongly (Tarvik 44.8, 55.9, 72.5, 78.5, 93.6, 107.1) and
  it widens the easy routes with it (37.0, 37.8, 42.0, 45.8, 50.4, 56.8), leaving the ratio that decides the window at
  0.654 to 0.749 throughout and never at the 1.3225 a window needs. The dial is one-ended: every setting with a real
  separation has a split licensed family and every setting with a unanimous family has no separation.
- Lowering the loss rate per pair that changes order to slide every figure away from the line: dead by arithmetic, not
  measured as a sweep. Every construction in the family is the record's losses over the record's exposure times the
  2027 exposure over the 2027 hours, so each one is linear in that rate and the whole family slides together; the
  ratio that decides the window is unchanged, which is the same refusal as raising the tolerance.
- Narrowing SF6 so only the pair definitions the record's across-sector test leaves standing are licensed (pairs that
  change order, pairs meeting at a level, moving pairs within 1,000 ft): would work on the dial from base 26 up
  (window [48, 51] at 26, [58, 67] at 40), and is not available. Narrowing the pair's definition means filing what a
  pair is, which files the HOW and makes the decisive step rule application (CLAUDE.md rule 3, determinism-check
  section 1); leaving it open forks the main recommendation. No third position, so the architecture is spent.
- Refuting the per-sector moving-pair fit from the record instead of from a filed sentence: dead, measured. The
  per-sector fit reproduces each sector's own count exactly, so no across-sector test touches it, and the only test
  left is the within-sector monthly profile, where the two bases are collinear: correlation 0.9951 to 0.9988 by
  sector, 0.9994 pooled, Poisson log-likelihood difference 0.22 on one degree of freedom against 3.84, and about
  40,782 losses needed against the record's 96.
- The two easy routes that already name Tarvik on the shipped pack, never asserted by the build: level-changing
  traversals pooled over the two summers (42.3) and over summer 2026 (41.4). The checks assert the vertical-flight-hour
  forms of that reflex (32.0 and 36.6) and never its count form, so Gate F was measured on a subset of the reflex.
- The in-house reader record that stood at the end of this section (architecture 4) was removed on 2026-10-31 under
  CLAUDE.md's STOP block; architecture 4's death is carried by the measurement lines above and the card's lineage.
- Architecture 4 moved to the card's lineage as spent on 2026-10-31 at the re-root (measured dead 2026-10-21).
- The weather-conditioned violence draw (v5a: a county constabulary's July to September 2027 exceptions against each
  area's own record for the weather, the night-time economy answering the warmth of Friday and Saturday nights),
  killed at the draw on 2026-10-31 before any data: its abstraction is task182's approved driver (each unit's level
  follows a shared outside driver through its own response, the effect is the gap to that path), and its
  separation needed a doubling of weekend-night violence per 4.6 degrees and a warm spell falling on ten weekends
  of thirteen with the weekdays between ordinary, which no weather record does and which reads as planted. Real
  weather moves a quarter's violence by a few per cent.
- The criminology cell (crime-incidence-hotspot-analysis x anomaly detection), closed at this re-root: task182's
  architecture 8 enumerated sixteen decisive steps there and found each dead to a standing screen (denominator,
  selection, coefficient or clean subset), and this pass screened nine more on paper before the weather draw
  (capture changes, which spends task199 and task236; exposure denominators, the client card's reflex; which
  records count, the WHAT pincer; a hospital or custody suite moving, Layer 1 geography; a tenure hazard, task149;
  temporary causes, task111; breach exposure, task169; school calendars, the WHAT pincer; multi-victim events, the
  unit). Moved under the directive's fallback to epidemiology, which is neither human factors, pharmacology nor
  marketing.
- A hospital's C. difficile wards by the ward of exposure through the bed-movement file: rejected at the draw. With
  the estimand naming the ward of acquisition, an infection-control analyst reads each patient's ward stays in the
  incubation window by reflex, the window is a free parameter, and ward colonisation pressure was already rejected
  above.
- An acquirer's merchants with descriptor-change disputes (cardholders who stopped recognising a renamed
  subscription): rejected; this slot's lineage already holds two fraud worlds, and an estimand naming third-party
  fraud sends a solver to the card's own history, one self-join.
- Storm overflows by spill threshold against radar rain, ozone exceedances read as total oxidant, river dissolved
  oxygen by time of sampling: rejected; the first is task182's abstraction with rain for climate, and the other two
  name the true quantity (the oxidant, the daily mean) in a way that hands over its one-step correction.
- Dengue with each case's workplace as a column of the line list: rejected; a per-case workplace makes the step a
  reading of a field, so the place comes only through the place-of-work flows.
- Dengue screen 1 (barangays of random size, a flat trigger of 30): every route failed, the golden included,
  because large barangays crossed 30 on ordinary transmission; recalibrated to season-peak counts of 5 to 18 in an
  ordinary barangay, with the estate a workplace inside its host barangay rather than a residential place.
- Dengue screen 2, first calibration: the fractional placements at a half share and the excess spread by the
  place-of-work shares missed in 11 to 14 of 20 seeds (the business district picking up spread cases, the
  dormitories keeping half their estate cases), while the inversion landed 19 of 20; a standing family split by a
  free share is a fork, so the world is built so every placement that puts working residents' exposure at work
  files the golden (estate cases near 36 a dormitory on a home baseline near 4, the business district a small
  employer of the dormitories), asserted across the placement family in checks.py.
- The trigger at 30 cases (dengue screens 3 to 5): a dormitory barangay had a window of about three cases between
  being over the trigger by home address and under it at a half share, so the placement family split by the share
  assumed; moved to 40 with the estate and Maligaya's outbreaks scaled, which widened the band to about 13 cases.
- Routes written on the employed group: the line list carries age and no occupation, so a route that knows which
  cases are workers is not one a solver can run; the routes now read age bands, the CBMS employment rate and the
  place-of-work table, and the barangays beside the estate became boarding-house barangays of young working
  residents (about 0.84 of working ages employed), which is what such barangays are.
- Job spread into the barangays beside the estate: residents of other barangays were given work there through the
  random spread of their place-of-work shares, which lifted the six under a half share; those barangays hold few
  jobs for anyone else, so the spread now skips them.
- World seed 0: met the design on the clean truth and kept only 1.8 cases under the trigger at a half share on the
  cut pack; seed 3 is the first seed in order to keep 3.5 there with 12 inside and 6 outside elsewhere.
- The first ask devices (a row per container, the household survey's follow-up visits, the private hospital's
  sheet weeks, the laboratory's first positive per reference, rejected runs worth one case): a careful solver
  holding the plan's definitions handles each in the same act that finds it, about 85 per cent of the ask figures
  kept; re-sited onto reconstructions across records with no shared key (a patient moved between the hospitals, a
  stay's ward segments without a movement code, house numbers restarting in each purok, a laboratory reference per
  facility) and a kit lot whose four failed runs leave a fifth of their negatives reading positive.
- The vector control log run to September 2027: it would have recorded the office's residence-based assignment of
  13 September, an official record of the wrong basis; the log ends on 31 August 2027, before any 2027 window put
  a barangay at 40 by home address.
- The plan's sentence giving the number of hotspot teams: it reads as a cap and invites a ranking; cut.
