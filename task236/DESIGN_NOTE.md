# task236 design note

Architecture 1, wave 2, seed DQ09 (whether a step in the case series is flagged as a series break caused by testing
volume): the seed's decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Epidemiology
& Public Health, disease surveillance, Data Quality Monitoring & Alerting. A state health department's communicable
diseases branch publishes a weekly influenza report with each health region's notified laboratory-confirmed influenza.
When a region's testing changes, its notified series can step for reasons that have nothing to do with influenza: the
report's data quality protocol puts a testing-change break flag on a region's series from the week of the change when
the change moved the share of the region's influenza infections that get notified by more than a quarter. Every Tuesday
the surveillance epidemiologist signs off the flags; the week 36 report of 2027 (the week of Monday 6 to Sunday 12
September) is the first to carry the flags for the eight testing changes the testing change register logged this winter.

## Draw

Card `cards/task236.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, two lines: `overuse.org_family`
(a government agency: the state's communicable diseases branch is the body that publishes notifications) and
`repeat.question_form` against task235 (asked as which: the decision's own form, a set of regions to flag).
`test.same_puzzle_older` (task453, task463) is cleared by the card's differentiation lines: neither reads a capture
share against an independent index that the change cannot reach. At stage 3 `guard.py heart` met task465's
architecture 2 (drawn minutes before this build, its card not yet on this checkout at the draw) on shape 07, and the
people screen read the regions Metro North, South and West as personas; the card moved to shape 11 and the regions
were renamed Metropolitan North, South and West, nothing else changing.

- **Pairing.** Epidemiology & Public Health / disease-surveillance-outbreak-anomaly-detection, serving Data Quality
  Monitoring & Alerting (the domain index lists this task type under AD and DQ). The seed's own domain; Epidemiology x
  Data Quality is not banned against the last three builds (task465, task264, task235). The seed's world (a laboratory
  joining a network) and its method (positivity) are not used: here positivity is the trap, and task234 spent
  positivity as an estimator.
- **Niche.** Influenza notifications rest on who gets tested. This winter point-of-care testing reached the general
  practices of some regions, others moved emergency departments to multiplex respiratory panels, one closed its
  drive-through clinics, and another merged two laboratories; RSV peaked early and hard in the north. The state's
  sentinel general practice network counts influenza-like-illness consultations against its practices' list sizes and
  swabs a fixed protocol sample of those patients, tested at the public health laboratory, whatever any region's
  testing does.
- **The call.** For each of the eight testing changes the register logged between weeks 30 and 32 (eight regions, one
  change each), flag the region's notified series from the change week or not.
- **Shape.** 11, before and after with a control: eight regions, each with its notified series either side of its
  change read against the sentinel network's influenza activity, its flag, and the per-region figures the asks owe.
  Decision designation_set, answer set_of_items, question form which.
- **Strategy.** causal_design with G16 decisive (the infection proxy the shipped data supports: the sentinel
  consultations attributed to influenza by the protocol swabs), G6 supporting (a testing change moves the population
  tested, so the region's own positivity moves with it: the default path's trap) and G14 (the influenza-like-illness
  rate pools influenza with RSV and the other viruses behind the same syndrome); Gate G decomposition_attribution
  (the step split into the testing change's share and the infections'); calibration none; context artifact
  filed_standard (the data quality protocol); layer 2 family field_method, pattern
  own:ascertainment-against-a-sentinel-syndromic-virological-index.
- **Forum, event, organisation.** operations_desk (the surveillance epidemiologist signs off the report's flags; no
  committee), period_close (the week 36 report), government_agency (a state health department).
- **People** (`guard.py names --geo "Australia" --seed 236`): Heidi Sparks, surveillance epidemiologist, who signs off
  the flags; Brendan Davis, sentinel network coordinator; Jane Suarez, laboratory liaison, who keeps the testing change
  register.
- **Deliverables.** `influenza_testing_break_flags_week36_2027.xlsx` (one row per region with a logged change: the flag,
  the season-to-date notified cases and the week 36 rate per 100,000) and `testing_change_breaks_week36_2027.png` (each
  region's weekly notified cases from week 26 with its change week marked and the flagged regions picked out). Shape
  arithmetic: 8 flags, 8 season-to-date counts, 8 rates, the chart's parts (8 panels, change weeks, flagged regions
  picked out, weeks 26 to 36) and the two files: 30 criteria.
- **Pack.** 13 files in four formats: the notification gateway's influenza results (229,848 rows, every laboratory's and
  point-of-care service's result with its report status and receipt time in UTC; the cases are built from them), the
  sentinel practices' weekly returns and protocol swabs, the testing change register (xlsx), the postcode concordance
  with the 28 June boundary review, postcode population, the reporting services, the report's data quality protocol
  CDB-FLU-03 and the network's protocol SGP-2027 (pdf), the dictionary and readme (md), and two distractors (vaccine
  doses by region and week, laboratory turnaround by week).
- **Data-native sentence.** A testing change alters who is tested as well as how many, so each region's positivity moves
  with the change itself (multiplex panels test every emergency department respiratory patient, point-of-care tests
  reach patients a laboratory never saw at the same pre-test probability); the sentinel practices swab a fixed protocol
  sample of their influenza-like-illness patients that no regional testing change reaches, so their consultations times
  their swab positivity follow the region's influenza infections, and notifications against that index give the change
  in the share notified, while raw notifications ride the season's rise and notifications per consultation ride RSV,
  which fills the same consultations.

Sources, one line each (what it teaches; how this build differs):
- Client pattern disease-surveillance-outbreak-anomaly-detection/3 (testing volume changes the count; positivity or a
  test-adjusted rate): here the testing change moves who is tested, so positivity is itself moved, and the change in
  ascertainment is read against a sentinel index no testing change reaches.
- Influenza surveillance practice: sentinel general practice networks report influenza-like-illness consultations per
  registered patient and swab a protocol sample; consultations times the share of swabs positive for influenza is the
  field's own index of influenza activity, separated from RSV and other viruses by the swabs.
- Seed DQ09: the decision and the quantity only; its decoy-era design is not read.
- Spent on this objective (`guard.py mechanisms`): task228 (a ratio metric's variance at the randomised unit), task229
  (a daily mean through a convex rating), task230 (net coding bias of a late channel), task231 (the closed share of
  silent units from rounds the register caught up with), task232 (transmission from delayed, mixed outcomes), task233
  (a missing-not-at-random departure on the odds scale), task234 (a source's output read from a share a loss cannot
  move), task235 (a missing event censored until its device's next contact). None reads a capture share against an
  independent fixed-protocol sample that the capture change cannot reach.

## Default path

1. Read the data quality protocol: a region's notified influenza series carries a testing-change break flag from the
   week of a change in the testing change register when the change raised or lowered the share of the region's
   influenza infections that are notified by more than a quarter of its level before the change, the four report weeks
   from the change week against the four report weeks before it.
2. Build the notified cases from the gateway's results under s.2 (positives within 14 days of a case's first positive
   specimen one case, the week of that specimen, the region of the residential postcode), and count each region's
   cases and tests by report week.
3. Adjust for testing: the share notified moves with testing, so compare each region's positivity (positive specimens
   per specimen tested, or notified cases per test) over the four weeks from its change week with the four weeks
   before, and flag a change of more than a quarter either way.

Ends on: seven regions flagged, 5 of the 8 wrong (North Coast, Tablelands, Central West and Metropolitan North flagged as
their positivity rose 1.61 to 2.03 times with the season and their changes, Far North missed at 1.03, its
point-of-care tests about as often positive as the referrals they replaced).

Golden: Far North, Metropolitan South, Metropolitan West and South Coast flagged (the share notified up 1.87, 1.53 and 1.53 times
where point-of-care testing came in, down to 0.45 in Metropolitan South when its drive-through clinics closed), the other four
not (0.99 to 1.01).

## Stump sentence

A competent solver adjusts for testing by comparing each region's positivity in the four weeks from its testing change
with the four weeks before and files 5 of the 8 regions wrong (Ends on: North Coast, Tablelands, Central West and Metro
North flagged, Far North missed); the step that lands it there is reading the share of infections notified off the
tests the region's own services ran, which the testing change itself moved, instead of off the sentinel practices'
influenza-like-illness consultations attributed to influenza by their protocol swabs, which no testing change reaches.

## Three rules

- **Task type:** epidemiology-public-health / disease-surveillance-outbreak-anomaly-detection, which serves Data
  Quality Monitoring & Alerting; the object is the comparability of a published notification series across a testing
  change, and the call is the report's break flag.
- **Domain test:** the quantity that decides is each region's change in influenza ascertainment (the share of its
  infections that are notified) across its testing change, read against the sentinel network's influenza-like-illness
  consultation rate times its protocol swabs' influenza positivity, the syndromic and virological index surveillance
  builds for exactly this.
- **Swap:** "which stores' sales series carry a till-change break flag, judged on the share of shoppers' purchases the
  tills record" has no syndrome that several viruses fill, no protocol swab that attributes it, and no testing change
  that moves who is tested; the analysis that decides here has nothing to act on.
- **Layer 1:** a preliminary and a final report for one positive specimen (laboratories send both); inpatients
  re-swabbed while they shed (hospitals' clearance swabs); a multiplex panel reporting influenza A and B on their own
  rows; result wording that differs by service and changes when two laboratories merge onto one system; the residential
  postcode blank or written 0000 (the requesting form had no address); residents of other states tested here; a
  boundary review that moved a postcode between each pair of the eight regions on 28 June; receipt times in UTC
  against a local cut-off; sentinel returns not received and list sizes revised for the July quarter; protocol swabs
  that could not be tested. Each is how the system that writes it behaves; none is placed to be caught.
- **Layer 2:** field_method, ascertainment against an independent index: the change in the share notified is read
  against the sentinel network's influenza-attributed consultations; positivity, raw notifications, a comparison with
  the unchanged regions and notifications per consultation or per swab positivity each mismeasure it.
- **Decisive step:** estimating each region's influenza infections either side of its change from the sentinel
  practices' influenza-like-illness consultation rate times the share of their protocol swabs positive for influenza,
  and reading the change in notified cases against that index rather than against the region's own tests.
- **Not semantics:** the default path reads every field, code and status right (episodes built, postcodes mapped,
  weeks by collection date, panel rows counted once per specimen, preliminary and final reports one specimen) and
  still files 5 of the 8 regions wrong; what it gets wrong is which quantity measures the region's infections, which
  no field states.
- **Not rule application:** the protocol files the flag's quantity (the change in the share of infections notified),
  the population (every infection, seen or not), the windows and the quarter; no rule says how a region's infections
  are to be estimated, and executing every stated rule still leaves that choice.
- **Analyst test:** a strong analyst who cleans the data and reads every rule, then judges each region's testing change
  on the change in its positivity, files 5 of the 8 regions wrong (Ends on: North Coast, Tablelands, Central West and
  Metropolitan North flagged, Far North missed); raw notifications file 5 wrong as the season rises, the unchanged South West
  and Far West as controls file 5 wrong, and notifications per influenza-like-illness consultation or per swab
  positivity flag all eight (4 wrong).
- **Estimand:** the data quality protocol (in the pack) fixes the population (each region's influenza infections,
  whether or not the person sought care or was tested), the outcome (notified as a confirmed or probable case), the
  window (the four report weeks from the change week against the four before), the unit (the region's notified
  series) and the comparison (a change in the share notified of more than a quarter either way).
- **No decoy:** nothing is planted: no memo, earlier report, draft or stakeholder figure states a region's ascertainment
  or a flag; the testing changes are the register's operational entries; the sentinel protocol describes the network as
  such protocols do and relates its figures to no notification count.
- **No certified replay:** no certified or published ascertainment exists for a method to reproduce.
- **Lesson:** a change in how cases are found moves the found share and the tested population together, so the found
  share has to be read against a measure of infection that the change cannot reach; no build on file reads a capture
  share against an independent fixed-protocol sample.

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 (default) each region's positivity, the four weeks from its change over the four before: 5 wrong | s.4 says the series depends on who is tested, which invites a testing adjustment | the results carry every test and its result | yes, a test-adjusted rate | none | no | two ratios | readable |
| 1 raw notified cases either side: 5 wrong | none | the results | yes, the series as published | none | no | one ratio | readable |
| 1 the change against the unchanged South West and Far West: 5 wrong | none | the register shows two regions with no change | yes, a comparison region | none | no | a ratio of ratios | readable |
| 2 notified cases per sentinel ILI rate, or per sentinel swab positivity: all eight flagged, 4 wrong | the network's protocol defines both figures and the report publishes them | the returns and the swabs | yes, a denominator from the network | none | no | a ratio of ratios | readable |
| 3 (decisive) notified cases against the sentinel ILI rate times the swabs' influenza positivity, summed over each four weeks | no sentence multiplies the two figures or relates either to notified cases; s.4 files the share and names no way of estimating infections | no column holds an index or a rate; the swabs carry no region and join through the practice | no: the reflexes use the region's own tests, a comparison region or one network figure | no control scores a way of estimating infections | no | not linear: a product per region and week, sums over each window, then a ratio of ratios | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "notified series" | confirmed and probable cases | confirmed cases only | Metropolitan South alone flagged (the point-of-care regions' probable cases drop out) | CDB-FLU-03 s.2 ("the notified series count confirmed and probable cases") |
| SF2 | a case | a person's positives within 14 days of the case's first positive specimen one case | anchored on the previous positive; one case per person | same call | s.2 anchors on the first; same call (asserted) |
| SF3 | the report week of a case | the ISO week of its first positive specimen's collection date | the week it was notified | same call | s.2; same call (asserted) |
| SF4 | the region of a case | the residential postcode under the concordance in force at the report | the concordance as at collection | same call: no moved postcode has a case in any window | s.2; C1 (asserted) |
| SF5 | residents and unknown addresses | residents of other states out; no postcode (blank or 0000) by the requesting service's postcode | interstate residents counted where tested; unknown addresses dropped | same call | s.2; same call (asserted) |
| SF6 | the cut-off | cases notified by 09:00 on Monday 13 September | none; 09:00 read as UTC | every case notified after the cut-off is a week 36 case: every window complete either way | s.2; C1 (asserted) |
| SF7 | "the four report weeks from the week of the change" | the change week and the three after it | the four weeks after the change week | same call | s.4; same call (asserted) |
| SF8 | "raised or lowered ... by more than a quarter of its level before the change" | above 1.25 or below 0.75 | below 0.80 (a quarter rise undone); 25 percentage points of the share | same call: Metropolitan South at 0.45, the unflagged at 0.99 to 1.01; no file gives a share's absolute level, and s.4 measures the quarter against the level before | s.4; same call (asserted) |
| SF9 | "the region's influenza infections" | every infection, seen by a service or not | the infections that reached a service or a test | the second is what the testing change moves: positivity's reading | s.4 ("Infections count whether or not the person sought care or was tested") |
| SF10 | the changes to judge | the register's eight entries from 26 July to 9 August, one per region | the three earlier entries (state-wide and the Far West courier) | the prompt's eight regions; the earlier entries are before the season's windows | register; prompt (asserted) |
| SF11 | the week of a change | the report week its effective date falls in | the week after | every change takes effect on a Monday | register (asserted) |
| SF12 | compared unrounded | unrounded | at two decimals | every region 15 per cent or more from the line | s.4; same call (asserted) |
| SF13 | "the first result reporting influenza" | every result reporting influenza, preliminary or final | the final report only | same call (every window's final reports arrived long before the cut-off); only the asks' week 36 cases move | s.2 (a preliminary positive is a result and reports influenza); same call (asserted) |

## Ladder

Four rungs, each a defensible way of reading the share notified across a change, each dying to one shipped fact
(figures measured on the cut pack, asserted in `checks.py`; ratios are the four weeks from the change over the four
before).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 (default) | positivity (positive specimens over specimens, or notified cases over tests) | NC 1.61, TB 2.00, CW 1.94, MN 2.03, MS 3.07, MW 2.45, SC 1.64 flagged, FN 1.03 not: 5 wrong | the register: each change moves who is tested (a multiplex panel tests every emergency respiratory patient, point-of-care tests reach patients a laboratory never saw, a closed drive-through clinic took its many negatives with it), and positivity rises with the season |
| 1 | raw notified cases; the change against the unchanged South West and Far West | raw: every region but Metropolitan South (2.35 to 5.59; MS 1.01): 5 wrong; against the controls: NC 0.57, CW 0.74, MN 0.54, MS 0.32, SC 1.72 flagged, FN 0.98 and MW 1.07 not: 5 wrong | the season rises through every window; the South West and Far West peak later and have their own seasons |
| 2 | notified cases per sentinel ILI rate; per sentinel swab positivity | all eight flagged (per ILI rate 0.60 to 3.26; per positivity 0.70 to 4.92): 4 wrong | the swabs: RSV filled the ILI consultations in the northern and metropolitan regions before the change weeks; positivity alone says nothing of how many were ill |
| 3 (golden) | notified cases against ILI rate times swab influenza positivity | FN 1.87, MS 0.45, MW 1.53, SC 1.53 flagged; NC 1.01, TB 1.00, CW 1.00, MN 0.99 not | |

- **Margins.** Every region sits 19 per cent or more from the line on the golden construction, the nearest North Coast
  at 1.01 against 1.25 (Metropolitan West and South Coast 1.53 against 1.25; Metropolitan South 0.45 against 0.75).
- **Corridor (C3).** The construction of the index moves no flag: ILI per 100,000 patients or per 1,000 consultations,
  ILI consultations counted, the practices' own positivity averaged, the mean of the weekly ratios, and the series
  under every Layer 1 handling (episodes anchored on the previous positive, final reports only, regions as at
  collection, unknown addresses dropped, no cut-off) all flag the same four; the nearest unflagged region is Tablelands
  at 0.84 on ILI counts, the nearest flagged Metropolitan West at 1.48 (asserted). No graded figure moves with it.
- **Position and dominance.** Every easy route files 4 or 5 regions wrong; only the attributed index lands the golden,
  and the decisive step alone (positivity's tests replaced by the index) moves the default path to it (R3b).
- **Grid.** The default moves 5 of 8 cells, the rungs 4 or 5.
- **Worth.** Counted on the cells, never on an intermediate.

## Closure table

| # | Axis | Reading in this build | Closure |
|---|---|---|---|
| 1 | Population | each region's influenza infections, seen or not, in the four report weeks either side of its change | CDB-FLU-03 s.4 (SF9) |
| 2 | Unit of account | the case (a person's episode) | s.2 (SF2) |
| 3 | Attribution window | the report week of the first positive specimen's collection date | s.2 (SF3) |
| 4 | As-of dating | the week 36 report's cut-off, 09:00 on Monday 13 September; the extract of 06:30 on Tuesday 14 September | s.2; README; C1 for the windows (SF6) |
| 5 | Version basis | the concordance in force at the report | s.2 (SF4) |
| 6 | Denominator | the region's infections, estimated; for the rate, the ERP at 30 June 2026 under the concordance in force | s.3 and s.4 |
| 7 | Weighting | none: a ratio of window sums | the design; corridor asserted |
| 8 | Window length | four report weeks from the change week and four before | s.4 (SF7) |
| 9 | Boundary inclusivity | raised or lowered by more than a quarter of the level before the change, unrounded | s.4 (SF8, SF12) |
| 10 | Rounding path | the flag on the unrounded ratio; the rate rounded half up to one decimal once | s.4; prompt |
| 11 | Tie-break | none: each region on its own | s.4 |
| 12 | Maturity and censoring | every window closed by the cut-off; week 36 counted as the report counts it | s.2; C1 (SF6) |
| 13 | Order of operations | build cases, place them, count by week, estimate infections, divide, compare | s.2 to s.4 |
| 14 | Row order | irrelevant to counts | C1 |
| 15 | Duplicate resolution | a specimen's preliminary and final reports and a panel's two rows are one specimen; repeat positives within 14 days of the first one case | s.2 (SF2) |
| 16 | Identity normalisation | the person by patient_key, the same at every service; postcodes through the concordance; services through the services list | dictionary; s.2 |
| 17 | Netting against gross | none | s.2 |
| 18 | Dimensional units | counts, ratios, rates per 100,000 | s.3, s.4 |
| 19 | Code and status semantics | result text by service, P and F report status, blank and 0000 postcodes | dictionary |
| 20 | Integerisation | case counts are integers | C1 |
| 21 | Clause scope | the eight regions with a change in late July and August | prompt; register (SF10) |
| 22 | Forward window contents | none for the call (every window closed); week 36's later notifications go to the next report | s.2 |

## Literal reader

Executed word for word, CDB-FLU-03 and the prompt fix the candidates (the eight regions whose testing changed in late
July and August, one register entry each), the case (s.2: confirmed and probable, a person's positives within 14 days
of the case's first positive specimen, the report week of that specimen, the region of the residential postcode under
the concordance in force at the report, the requesting service's postcode where none was recorded, residents of other
states out, notified when the first result reporting influenza reaches the gateway, counted by 09:00 on the Monday
after the report week), the flag's quantity and its population (s.4: the share of the region's influenza infections
notified, every infection counting whether or not the person sought care or was tested), the windows (the four report
weeks from the change week against the four before) and the line (more than a quarter either way). Executed, s.4
leaves one question for the analysis: how many infections each region had in each window, which no file counts. The
region's own tests are moved by its change; the sentinel network's practices record influenza-like illness by a
clinical definition whatever the region's testing does and swab a fixed protocol sample tested at one laboratory and
not notified, so their consultation rate times the swabs' influenza positivity follows the region's infections. Every
construction of that index flags the same four regions; every reading of a term in the fork table gives the same call
or violates a quoted sentence. The asks execute s.2 and s.3 for week 36 and the season to date; no reading of a term
moves the call, and the difficulty is the estimation, not the words.

## Oracles

- No control, published figure or certified ascertainment ships: nothing reports a region's share notified, a flag, a
  positivity, an ILI rate or an index, and no field marks a case, an episode or a region of a case.
- The register's three earlier entries (point-of-care services onboarded state-wide on 1 March, the Public Health
  Laboratory's new assay on 29 March, the Far West courier on 10 May) are operational history before every window.
- Vaccine doses by region and week, and laboratory turnaround by week (distractors, named in `metadata.json`): neither
  counts cases or infections; doses peak in May and turnaround is flat through the season.
- The sentinel network's returns and swabs are data, not a control: they tie under every way of reading them and score
  no method.

## Ask sheet

Two asks, 16 figures, decoupled from the call: the call reads the windows' cases (weeks 26 to 35) and the sentinel
data; the asks read the season to date (weeks 14 to 36) and week 36, the cut-off, the boundary review's pre-June rows,
the report status and the population.

**Main population (zero device rows, asserted):** no case of a designed device sits in a window: the 172 cases notified
after the cut-off and the cases whose final report came after it are all week 36 cases, and the 20 cases in moved
postcodes before the boundary review all fall before week 26. The Layer 1 items that run through the whole season
(inpatient re-swabs, unknown addresses, residents of other states) are on the call's path and leave every flag where
it is (R2, asserted).

| Ask | Figures | H18 home | Use | Primary device (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|---|
| A: each region's notified cases for the season to date (weeks 14 to 36) | 8 | a measure every region carries that the call does not turn on | the report's season table printed beside the flags | D2, an attribute at the wrong vintage: the 28 June boundary review moved a postcode between each pair of the eight regions, the concordance carries both assignments with their dates, and the report counts every week under the concordance in force at the report; the careful as-at-collection join for an effective-dated map puts the cases collected before 28 June in their old regions | the preliminary reports (shared with B); the cut-off; inpatient re-swabs anchored on the previous positive; unknown addresses; residents of other states | results (patient_key, collection_date, result, result_status, received_utc, residential_postcode, requester_postcode), concordance (postcode, region_code, effective_from, effective_to), CDB-FLU-03 s.2, dictionary: 4 files, 11 columns | regions as at collection (every region 3 to 7 off); final reports only (every region 2 to 27 low); episodes anchored on the previous positive (6 to 45 low); no cut-off (11 to 33 high); 09:00 read as UTC (7 to 24 high); unknown addresses dropped (27 to 148 low); residents of other states counted where tested (7 to 54 high); the answer |
| B: each region's week 36 notified rate per 100,000 residents | 8 | a measure every region carries that the call does not turn on | the report's week 36 rate column | D2, the first delivered, not the latest accepted: laboratories send a preliminary positive for emergency and inpatient specimens and for every positive at the Public Health Laboratory, then a final report hours to days later; a case is notified when the first result reporting influenza reaches the gateway, and the battery's latest-status collapse dates it by the final, dropping the week 36 cases whose preliminary came before the cut-off and final after | the cut-off; the population's concordance rows; unknown addresses; inpatient re-swabs | results (as A), concordance (as A), population (postcode, erp_30_june_2026), CDB-FLU-03 s.2 and s.3, dictionary: 5 files, 13 columns | final reports only (every region 0.3 to 2.4 per 100,000 low); no cut-off (1.5 to 7.0 high); 09:00 read as UTC (1.3 to 3.7 high); every concordance row summed (the four regions that lost a postcode 2.9 to 17.9 low); the old boundaries (every region 2.2 to 22.2 off); unknown addresses dropped (0.2 to 1.2 low); the answer |

- **Span:** five files and 13 columns across the asks. The preliminary reports move both asks in every region; the
  cut-off moves both in every region; the boundary review moves A's counts and B's denominators.
- **Shared hazards:** the preliminary reports (A 2 to 27 low, B 0.3 to 2.4 low, every region); the cut-off (A 7 to 33
  high, B 1.3 to 7.0 high); unknown addresses (A 27 to 148 low, B 0.2 to 1.2 low); inpatient re-swabs (A 6 to 45 low,
  B five regions 0.2 to 0.5 low).
- **Realism:** a preliminary positive followed by a final typed or subtyped report is how laboratories report urgent
  and reference specimens; a boundary review taking effect at the start of a quarter's first reporting week, with the
  concordance carrying both assignments, is how health regions change; clearance swabs of inpatients are how
  hospitals manage influenza wards.
- **Referee:** none.

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 0) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A season to date (8) | executes s.2 through the concordance in force, the requesting service's postcode for blank and 0000, residents of other states out and the cut-off converted to UTC; its battery collapses each specimen's preliminary and final reports to the final, so each case is dated by its final report and the week 36 cases whose final came after the cut-off fall out | misses the same way | miss |
| B week 36 rate (8) | the same week 36 cases over the ERP of the concordance in force: every region 0.3 to 2.4 per 100,000 low | misses the same way | miss |

- **Cracker keeps:** under 0.05 of the ask weight (every figure turns on the preliminary reports). A solver that keeps
  each specimen's first report and anchors episodes on the first positive lands both asks; A's boundary review and
  inpatient re-swabs and B's population rows remain on its path.
- Mirror leakage: 5 per cent of ask weight (the mirror's ask path is the cracker's; the asks do not touch the call's
  construction).
- Pair ceiling: 31.3 (C = 38 + 7 + 55 x 0.05 = 47.8; S = 5 + 7 + 55 x 0.05 = 14.8; mean 31.3).

## Pre-ship check

1. Domain: the call stands on each region's change in influenza ascertainment across its testing change, read against
   the sentinel general practice network's influenza-like-illness rate times its protocol swabs' influenza positivity;
   positivity flags seven regions (5 wrong), and the ILI rate or the swab positivity alone flags all eight. With tills,
   meters or wards for regions there is no syndrome several viruses fill, no protocol swab to attribute it and no testing
   change that moves who is tested.
2. Two layers: Layer 1 (preliminary and final reports, inpatient re-swabs, panel rows, service wording and the
   laboratory merger, blank and 0000 postcodes, residents of other states, the 28 June boundary review, UTC receipt
   against a local cut-off, returns not received, July list sizes, untested swabs) is neutral on the call, each item
   asserted (R2, SF rows); Layer 2 is ascertainment against the independent index, asserted alone to move the default
   path to the golden on the clean truth (R3b), its construction a corridor (C3).
3. No banned stump decides: nothing is planted (no memo, draft, earlier report or figure states a share or a flag); not
   semantics (the default path reads every field right and files 5 wrong on the clean truth, R3a); not rule application
   (s.4 files the share, its population, the windows and the quarter and names no way of estimating infections,
   asserted on the protocol's text).
4. Gate G: no shipped artifact flags, ranks or estimates a region; the two distractors count no case or infection.
5. Determinism: the list grades each region's flag, season-to-date cases and week 36 rate; the flags are the same under
   every construction of the index (the nearest unflagged region Tablelands at 0.84 on ILI counts, the nearest flagged
   Metropolitan West at 1.48); every rate sits 0.015 per 100,000 or more from a rounding edge; counts are integers.
   Judge (round 1): DETERMINISTIC, APPROVE; Gate G analytical_method (decomposition with an ascertainment adjustment), no
   surface read, not a sole data defect; Gate H domain pass, layers pass, decisive step analytical; stump power strong.
   Its low-risk note (the index is no filed formula; the ILI rate alone or the positivity alone flips four regions,
   readings it rules out under s.4's "infections") stays as it is: filing the formula would make the decisive step rule
   application. After the judge, the reader's notes were fixed in one pass (each register entry worded for its region
   with the merging laboratory named as in the services list, each region's point-of-care codes in their own block,
   s.4's quarter written against the level before the change); the flags, every graded figure and both goldens' figures
   are unchanged (125 checks and the verifier on the rebuilt pack).
6. Asks: A is moved in every region by the boundary review (3 to 7), the preliminary reports (2 to 27 low) and the
   cut-off (7 to 33 high); B in every region by the preliminary reports (0.3 to 2.4 per 100,000 low) and the cut-off (1.3
   to 7.0 high); the call reads neither device (no device row in any window, asserted).
7. Input gates: 13 files in four formats (csv, md, pdf, xlsx), the gateway results at 229,848 rows, two distractors
   named in metadata.json; 125 generator checks with the realism sweep; the verifier (its own case build and index)
   green; two builds byte-identical; figures_check 93 of 93; containers clean.
8. Duplicate guard: `guard.py heart` WARN (overuse.org_family; repeat.question_form against task235; same_puzzle_older
   differentiated against task453 and task463); the shape moved from 07 to 11 at stage 3 (task465's architecture 2 holds
   07). `guard.py surface` promoted task234, task235 and task233 (the same author's Data Quality builds: a README and
   dictionary layout and a designation set; task234 predicts a stream's tests from its positivity, task235 judges a
   missing event by its phone's next session, task233 a register statistic's departure under missing not at random)
   and task81, task95 and task73 (surface only), for the author's adjudicated read.

## Leak check

leak.py REVIEW, no LEAK (--asof 2027-09-14), after a first run's LEAK on a versioned file name (the protocol's `_v4`,
renamed). Reader pass 1: Q1 none ("No sentence names that route"); Q2 none; Q3 the two distractors, the dictionary and
the readme (ordinary furniture); Q4 none; Q5 s.2 and s.4 execute to the golden's quantities, the open choice being the
infection estimator (the analysis), and "a quarter" readable as relative or absolute (fixed: s.4 now measures the
quarter against the share's level before the change); Q6 an analytical choice. On the asks it read preliminary reports
as counting under "the first result reporting influenza" (SF13) and residents of other states as postcodes outside the
concordance (the dictionary: the postcodes of the state). Realism: the register repeated one wording across regions
(fixed, each entry worded for its region, the merging laboratory named as in the services list); point-of-care codes
overlapped across regions (fixed); its note that the services list lacks STH and the point-of-care codes was a misread
(both are listed). REVIEW lines, all harmless: the sentinel protocol's practices table names the regions; the
dictionary, readme and both protocols carry the domain's own words without naming the move; the register names each
region beside its change date and ranks nothing. Reader pass 2 (the reworded protocol and register): Q1 to Q4 none,
"a quarter of its level before the change" clearly relative, Q6 an analytical choice; the merger entry's "collection
centres and courier runs unchanged" came closest to a verdict and was cut; the sentinel protocol's clinical ILI
definition stays (every sentinel protocol states it, and it names no comparison with notified cases). Reader pass 3
(the register after the cut): Q1 to Q3 none, realism good.

## Tried and rejected

- The seed's laboratory joining a network, read on positivity: positivity as the estimator is spent (task234), and a
  laboratory joining moves the network's coverage rather than ascertainment within a region.
- Wastewater against notifications as the infection index: normalising by a faecal marker repeats task234's
  invariant-share insight, and the shedding lead adds a fork; the sentinel swab positivity alone is not proportional to
  infections when RSV fills the consultations, so it is a rung, not the index.
- The notification system's case extract shipped beside the results: the asks' counts read straight off it, leaving
  the episode rule, the cut-off and the report status with nothing to act on; the cases are built from the gateway's
  results, as the protocol counts them.
- A boundary review on 1 June moving two postcodes from Central West to Tablelands: influenza before June is so low that
  no case moved; the review moved to 28 June (the first window's start, so no window holds a moved case) with a
  postcode moved between each pair of the eight regions.
- A Tuesday 09:00 cut-off with laboratory results inside two days: 62 late cases, a few per region and none in some;
  the cut-off moved to Monday 09:00, with turnaround spread over one to five days and a morning validation round.
