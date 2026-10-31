# task181 design note (architecture 5: where the city's dengue is caught)

Architectures 1 to 4 are spent and in the card's lineage, with the weather draw that opened this re-root (v5a,
killed at the draw). This architecture leaves criminology: the cell's decisive-step space was enumerated closed
by task182's architecture 8 (sixteen candidates, each dead to a standing screen) and this pass's own screen added
the weather-conditioned violence draw to that list. The re-root directive's fallback moves the build to another
anomaly-detection client domain, and epidemiology carries an honest stump here.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task181.json` (v5), registered 2026-10-31. `guard.py check` on the
  registered card: PASS, one NOTE (test.same_driver_older, differentiated against task487, whose driver dates
  inspection-found events inside their windows); nearest driver 0.08 (task121 v3, lineage). No WARN.
- **Pairing.** `epidemiology-public-health` / `disease-surveillance-outbreak-anomaly-detection` (serves AD and DQ),
  objective Anomaly Detection & Diagnostics: a real outbreak separated from the place the records put it. Client
  domain epidemiology-public-health. The task type carries one anomaly-detection card on file (task188, West Nile
  pools) and this slot's own architecture 2 (pertussis, another world and dataset).
- **World.** Dalisay City, a component city in Laguna province, Philippines (PHP), about 720,000 residents in 30
  barangays (one split into two in 2025). The City Health Office's epidemiology and surveillance unit runs the
  dengue line list fed by the city's disease reporting units (two hospitals, six city health centres, private
  clinics). The Dalisay Industrial Estate, an export processing zone inside Barangay San Roque, employs a large
  share of the working residents of six barangays near it and houses almost nobody; San Roque's own residents
  live in its old village. People drawn with `guard.py names --geo PH --seed 181`: John Figueroa (city health
  officer), Tammy Orozco (surveillance unit head).
- **Decision.** On Monday 11 October 2027, the start of morbidity week 41, the city health officer sends the
  hotspot response (search-and-destroy of breeding sites, larviciding, targeted fogging, house-to-house case
  finding) for morbidity weeks 41 to 44 to every barangay that meets the dengue plan's trigger: 30 or more of the
  city's notified dengue cases with onset in morbidity weeks 37 to 40 were infected in the barangay. The decision
  faces forward (the next four weeks' response); the quantity is the closed window just behind it, because the
  plan triggers on the latest four complete weeks, so the call is retrospective by design.
- **Quantity.** Each barangay's count of the window's notified cases that were infected there.
- **Data-native sentence.** A dengue notification records the barangay the patient sleeps in, because the case
  investigation form takes the home address, while Aedes aegypti feeds in daylight, so a working adult's infection
  is caught where they spend the working day; in a city whose export zone employs a large share of several
  barangays' residents and houses almost none, an outbreak at the estate is recorded in the barangays its
  workforce sleeps in.
- **Default path's answer:** the six dormitory barangays and the two barangays with real residential outbreaks
  (residence counts at or over 30). **Golden:** San Roque and the two residential-outbreak barangays.
- **Shape.** `other`: a designation over every barangay. Criteria: each flagged barangay (3), each dormitory
  barangay correctly left out although its residence count is over the trigger (6), the rest left out (1), the
  chart's named parts (5 to 6), the files (2), and the asks' cells (supplemental-stumping).
- **Strategy and family.** `causal_design` (interference between units: outcomes recorded in one barangay caused by
  exposure in another through daily travel); Layer 2 family `estimand_identification` (contamination of each
  unit's record by exposure elsewhere); Gate G `decomposition_attribution` (each barangay's correctly reported
  cases assigned to the barangay where they were caught); gap population then objective; generators G7 (the
  vector's feeding hours decide where a case is caught) and G6 (the working-age band moves against the rest).
- **Axis values drawn against the window** (tasks 464, 273, 268): forum operations_desk (the dengue task force
  desk dispatches the teams), forcing_event period_close (the four-week morbidity window closes), org_family
  local_government, role operations_director (the city health officer), context artifact monitoring_export (the
  line list export). season_or_peak was the first value for the forcing event and is banned by task273; the
  window closing is the honester label anyway, since the trigger is read the Monday a window closes.
- **Abstraction sentence.** Written against every approved build, no shared sentence holds: task175 reads a unit's
  attribute at the neighbours it faces, task179 links two bodies' records person by person, task182 conditions
  each unit on its own response to an outside driver, task236 reads a notified share against a sentinel rate,
  task275 raises observed catch by unobserved effort, task303 removes events every sibling opened in one minute.
  Here the recorded unit is not where the event was caused, and the place is recovered through the daily travel
  of the people the events happen to. The spent family it sits nearest is task268's (people present against
  residents), which died because there the estimand named presence; here the estimand names the place of
  infection, and no file says where any infection happened.
- **Sources.** All data synthetic, generated by `generator/` (license: CC0 for this pack). The world follows the
  Philippine Integrated Disease Surveillance and Response notification practice (DOH), the Community-Based
  Monitoring System tables an LGU holds (Republic Act 11315), and the DOH dengue prevention and control programme's
  barangay response; no real person, office or zone is represented.

## Default path

1. Read the dengue plan's trigger: 30 or more notified cases with onset in morbidity weeks 37 to 40 infected in the
   barangay.
2. Load the line list (2022 to 2027), merge the re-notified cases (a case updated from suspect to confirmed
   arrives again), set aside the cases that travelled outside the city in the two weeks before onset and the
   non-resident patients the city's hospitals notified, map each barangay as the reporting units spell it to the
   2025 barangay list.
3. Take each barangay's cases with onset in morbidity weeks 37 to 40, by the barangay of residence the
   notification records, which is the surveillance system's place of a case and the field's standard reading of a
   locally acquired case.
4. Flag every barangay at or over 30.

Ends on: the six dormitory barangays and the two residential-outbreak barangays (residence counts 36 to 66)
Golden: San Roque and the two residential-outbreak barangays

## Stump sentence

The default path counts each barangay's notified cases by the barangay of residence and presents the six dormitory
barangays and the two residential-outbreak barangays; the step that lands it there is taking the home barangay as
the place of infection, when Aedes aegypti bites by day and the six barangays' excess is all among working
residents in proportion to how many of them work at the estate, so those cases were caught in San Roque, whose own
residence count stays under the trigger.

## Three rules

Task type: disease-surveillance-outbreak-anomaly-detection (Epidemiology & Public Health), which serves anomaly detection: a real outbreak separated from the place the records put it.
Domain test: the quantity that decides is each barangay's count of the window's notified dengue cases infected there, and vector-borne disease surveillance places an infection where the person was while the vector feeds; Aedes aegypti feeds in daylight, so a working adult is exposed mostly where the working day is spent.
Swap: "Which barangays need the malaria response?" reads differently, because Anopheles feeds at night and the home is then the place of infection; put influenza or road injuries in and there is no feeding window to place an infection at all, so the task stops making sense.
Layer 1: two reporting-unit layouts (the hospitals' and the city health centres'), re-notified cases, barangay names as each unit spells them and the 2025 split of one barangay, day-month-year text dates, morbidity weeks that cut across months, the CBMS workbook's multi-row headers and footnotes, non-resident patients notified by the city's hospitals; each is produced by the system that records it and none is placed to be caught.
Layer 2: estimand_identification, the place of infection: each barangay's record is contaminated by infections caught in another barangay, and the choice that flips the call is placing the working residents' excess where they spend the day.
Decisive step: placing each barangay's cases where the patients were during the mosquito's daylight feeding, through the CBMS place-of-work table, instead of at the home address the notification carries.
Not semantics: reading every field and the plan's "infected in the barangay" correctly still leaves the easy route on the residence counts, because no file records where any infection happened; the line list carries only the home barangay, and the place has to be estimated from the vector's feeding hours, the excess's working-age band and the place-of-work flows.
Not rule application: no filed rule says where an infection was caught, so executing the plan's trigger on any placement files whatever that placement gives; the enumerated family (home barangay; home with travellers and non-residents out; by consultation or report week; the non-working residents as a local-transmission marker; place-of-work placements at a fixed share of a worker's exposure from 0.5 to 1.0; the excess spread by the place-of-work shares; the inversion of the flows) files three different sets (dormitories with the two outbreaks, the two outbreaks alone, San Roque with the two outbreaks), the standing family (the placements that put working residents' exposure where they work, which daylight feeding requires) files San Roque with the two outbreaks at every member measured, its cheapest member (every working resident's case spread by the place-of-work shares) included, and no clause or column does the ruling-out, only the biting hours and the excess's proportion to each barangay's estate workforce.
Analyst test: a strong analyst merges the re-notified cases, sets travellers and non-residents aside, maps the barangay spellings, counts each barangay's cases with onset in morbidity weeks 37 to 40 by residence and flags the six dormitory barangays and the two residential-outbreak barangays; every field is read and the trigger executed, and the call is wrong because the cases are counted where people sleep while they were caught at the estate.
Estimand: dalisay_dengue_plan_2027.pdf, the hotspot trigger: population, the city's notified dengue cases with onset in morbidity weeks 37 to 40 as notified by 08:00 on Monday 11 October 2027; outcome, the barangay where each was infected; window, morbidity weeks 37 to 40; unit, the barangay; comparison, 30 or more.
No decoy: nothing is planted to be caught; no memo, draft, briefing or stakeholder figure argues the residence count, and the line list's home barangay is what the notification form records.
No certified replay: no certified or published figure reproduces the method; no file carries any barangay's infections by place, and the response log records where teams went, never where infections happened.
Lesson: a case record's location is where a person sleeps, and for a day-biting vector the place of infection is where the person spends the day; a model that gets this right learns to ask where exposure happens before reading a surveillance map, which no build on file teaches (task268 was about the people present, task188 about pooled mosquito tests).

## Survivor anatomy

Actor: the deciding property, where each case was infected, has no column in any file; the line list carries the home barangay, the CBMS table carries where each barangay's working residents work as counts and never per case, and the property is a relation between the cases' age band and home and the place-of-work flows.
Link: no key ties a case to a workplace, and the comparison that finds the place (each barangay's working-age excess against its estate workforce in the CBMS table) is one the residence-based surveillance method never asks for; no sentence invites it.
Reflex: the field's method, cases by barangay of residence against the trigger (the surveillance system's place of a case), is rung 0 and files the six dormitory barangays and the two residential-outbreak barangays.
Back-test: the textbook route validates; in every season 2022 to 2026 the barangays the residence count put over the trigger were the barangays whose larval surveys found the highest container indices and where the response log sent the teams, because transmission then was residential.
Second use: every file the decisive step reads has its own reason to be in the pack; the line list is the surveillance record, the CBMS workbook carries the population denominators the plan's incidence table and an ask need (its place-of-work sheet is part of the same LGU release), and the plan files the trigger.
Shock: San Roque's residence count is ordinary (about 15 cases), nowhere near the pack's largest, and the golden set is not an interval of any sort of the barangays (residence count, rate per resident, working-age share of cases, week-on-week growth), asserted in checks.py.
Pins: the WHAT sits in the dengue plan (population, place of infection, window, unit, trigger) and no filed sentence names where infections happen, the vector's biting hours, workplaces, the place-of-work table or any placement method; deleting the trigger sentence unforces the call and that sentence names no step.

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
