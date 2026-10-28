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
| SF14 | "a person" (s.2: a case is a person) | gateway keys that share a specimen are one person; a key carrying an infant's results and an adult's is two people; an age one higher on a later specimen is the same person | every gateway key a person; keys split at every age they show | same call: every changed row sits outside every window, and each of the 35 readings gives the four flags and every window's cases as shipped; only the asks move | a specimen is taken from one person; an infant of 0 and an adult of 19 or more are two people; the readings asserted |
| SF15 | the case's residential postcode (s.2: "a case whose residential postcode was not recorded") | the postcode recorded on any of the case's results | the first row's postcode, so a preliminary sent without the address falls to the requesting service's region | same call (every such preliminary is a week 36 row); only the asks move | s.2: the case's postcode was recorded, on its final report; same call (asserted) |

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

Two asks, 16 figures, decoupled from the call: the call reads each region's change window (its cases and tests in the
four report weeks before its change and the four from it), the South West and Far West in weeks 26 to 35 and the
sentinel data; the asks read the season to date (weeks 14 to 36) and week 36, which take in every region's weeks outside
its window, and the population. Rebuilt on the portal's return (2026-10-28: rubric 79, the call held, no ask figure
missed): every device of the first build was a sentence of CDB-FLU-03 s.2 or the dictionary, so the top responses
executed each one (see the tried-and-rejected lines). The asks now turn on what the gateway's person matching and the
laboratories' two reporting systems do to the records, which no sentence states and the clean truth does not see.

**Main population (zero device rows, asserted):** every device sits on people whose every result was collected outside
their region's window and reached the gateway by the cut-off: the 113 changed rows belong to 82 such people, and no
changed row belongs to a case in a window. The 115,176 results rows the call reads and every other file of the pack are
byte-identical to the shipped pack (`generator/shipped.json`: sha256 per file and of the call's rows), and each of the
35 readings below gives the four flags and every window's notified cases as shipped (SF14, SF15). The first build's
filed-rule hazards keep their separation (the cases notified after the cut-off and those whose final came after it are
week 36 cases; the moved postcodes' cases before the boundary review fall before week 26).

| Ask | Figures | H18 home | Use | Primary devices (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|---|
| A: each region's notified cases for the season to date (weeks 14 to 36) | 8 | a measure every region carries that the call does not turn on | the report's season table printed beside the flags | D7, the true key elsewhere: 28 specimens (20 in week 36) whose preliminary the gateway keyed to one person and whose final, with that person's later results at the laboratory, to a second, the laboratory having registered the specimen against its own patient record between the two reports; the specimen is the only link. D1, a key carrying two people: 16 infants registered under their mother's details and keyed to her, an age of 0 beside an adult's the only sign; its over-cleaning half, 10 people whose age rises by one between two specimens of one case (a birthday) | the first build's filed rules, kept: the concordance in force, the cut-off in UTC, the first result reporting influenza, blank and 0000 by the requester, residents of other states out, episodes anchored on the first | results (patient_key, specimen_id, result, result_status, age_years, collection_date, received_utc, residential_postcode, requester_postcode), concordance (postcode, region_code, effective_to), CDB-FLU-03 s.2, dictionary: 4 files, 12 columns | every gateway key a person (every region 1 or 2 high); keys joined through their specimens, none split (1 to 3 low); keys split at every age (1 or 2 high); the first row's postcode (every region 2 off); each specimen read off its first report or its latest final; the cracker, all three at once (FN, TB, MN, MS 1 low, NC, CW, MW, SC 4 high); the answer |
| B: each region's week 36 notified rate per 100,000 residents | 8 | as A | the report's week 36 rate column | the two above in week 36, and D4 with D7, a field on one report only: 16 week 36 preliminaries sent without the residential address from a requesting service in the next region, their finals carrying it (each pair of regions sends three one way and one the other: Far North and North Coast, Tablelands and Central West, Metropolitan North and Metropolitan West, Metropolitan South and South Coast) | as A, and the population's concordance rows | results (as A), concordance, population (postcode, erp_30_june_2026), CDB-FLU-03 s.2 and s.3, dictionary: 5 files, 14 columns | every gateway key a person (every region 1 case high); keys joined, none split (1 or 2 low); keys split at every age (1 high); the first row's postcode (every region 2 off); each specimen's latest final (the week 36 cases whose final came after the cut-off fall out); the cracker (FN 53.4, NC 39.7, TB 54.1, CW 51.4, MN 36.6, MS 24.8, MW 68.7, SC 104.8); the answer |

- **Span:** five files and 14 columns across the asks. The preliminary and its final are the hub: the second key rides on
  the final, the missing address on the preliminary, and reading a specimen off its first report or its latest final
  breaks one of the two while the infant's key breaks both.
- **Shared hazards:** the second key (A: every region 1 to 2 high; B: 1 case high), the infant under its mother's key
  (A: 1 to 3 low; B: 1 to 2 low), the missing address (A and B: every region 2 off, out of one region and into its pair),
  the birthday (A: 1 or 2 high, B: 1 high, for a reader who splits keys at every age), the preliminary straddling the
  cut-off (A and B: 2 to 27 low for a reader of latest finals). Every count asserted per region; the per-region counts
  were set so that no subset of mishandlings composes back to a golden figure, and the 35 readings below are the proof.
- **A reconstruction, not a work order (1.0):** a solver who notices a specimen under two keys still has to join the keys
  and rebuild every episode across them; one who notices a key with two ages has to separate the people while leaving a
  birthday's one-year rise alone, and on a joined key the two rules pull against each other; one who notices a
  preliminary without an address has to place the case by whichever of its results recorded one. No column, status or
  comment marks any device row; each sits beside thousands of ordinary rows of the same kind.
- **Realism:** a preliminary from a laboratory's rapid result interface with the details on the request and a final from
  its information system with the patient's details as the laboratory holds them; a gateway's person matching keying a
  mismatch to a second person; newborns registered under the mother's details; ages at collection moving on a birthday;
  patients attending an emergency department or a clinic across a regional border. Each is how notification feeds behave.
- **Fair (law 6):** the reading that reproduces the clean truth is asserted: the golden's season-to-date counts and week
  36 rates equal the clean truth's (`Records.positives`) and the shipped figures exactly; before the asks' rows no
  specimen sat under two keys and no key showed two ages, so the golden's person and postcode rules move no other case
  (asserted), and each instance leaves the inconsistency a grader can confirm (the specimen under two keys, the key with
  two ages, the preliminary without the address beside its final with it). Block 3 of `submission.md` names each handling.
- **Referee:** none.

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 0) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A season to date (8) | executes s.2 by gateway key over every result, the first row's postcode placing each case: a specimen under two keys counts twice, an infant under its mother's key once with her, a week 36 preliminary without the address goes to the requesting service's region (FN 3,559, NC 4,117, TB 1,504, CW 2,495, MN 12,036, MS 6,132, MW 11,234, SC 3,650 against 3,560, 4,113, 1,505, 2,491, 12,037, 6,133, 11,230 and 3,646) | misses the same way | miss |
| B week 36 rate (8) | the same week 36 cases over the ERP of the concordance in force (FN 53.4, NC 39.7, TB 54.1, CW 51.4, MN 36.6, MS 24.8, MW 68.7, SC 104.8 against 53.7, 39.1, 54.6, 50.6, 36.7, 24.9, 68.4 and 104.0) | misses the same way | miss |

Every careful reading of who a person is, which postcode places a case and which report a specimen is read off, scored
by `ceiling.py` on the cut pack (target.zip sha256 5ef00068c44e380a4bc2570bfe6d6e4a72f8139c4a56815cb15eb4a9a1f4e945):

| Reading (the cracker's first, then every careful variant) | Figures kept | Cracker sheet |
|---|---|---|
| every gateway key a person; the first row's postcode; every report | none | miss |
| every gateway key a person; the first row's postcode; each specimen's first report | none | miss |
| every gateway key a person; the first row's postcode; each specimen's latest final | none | miss |
| every gateway key a person; the postcode any of its results recorded; every report | none | miss |
| every gateway key a person; the postcode any of its results recorded; each specimen's first report | none | miss |
| every gateway key a person; the postcode any of its results recorded; each specimen's latest final | none | miss |
| keys sharing a specimen joined, no key split; the first row's postcode; every report | none | miss |
| keys sharing a specimen joined, no key split; the first row's postcode; each specimen's first report | none | miss |
| keys sharing a specimen joined, no key split; the first row's postcode; each specimen's latest final | none | miss |
| keys sharing a specimen joined, no key split; the postcode any of its results recorded; every report | none | miss |
| keys sharing a specimen joined, no key split; the postcode any of its results recorded; each specimen's first report | none | miss |
| keys sharing a specimen joined, no key split; the postcode any of its results recorded; each specimen's latest final | none | miss |
| each key split at every age it shows; the first row's postcode; every report | none | miss |
| each key split at every age it shows; the first row's postcode; each specimen's first report | none | miss |
| each key split at every age it shows; the first row's postcode; each specimen's latest final | none | miss |
| each key split at every age it shows; the postcode any of its results recorded; every report | none | miss |
| each key split at every age it shows; the postcode any of its results recorded; each specimen's first report | none | miss |
| each key split at every age it shows; the postcode any of its results recorded; each specimen's latest final | none | miss |
| keys split where ages jump, not joined; the first row's postcode; every report | none | miss |
| keys split where ages jump, not joined; the first row's postcode; each specimen's first report | none | miss |
| keys split where ages jump, not joined; the first row's postcode; each specimen's latest final | none | miss |
| keys split where ages jump, not joined; the postcode any of its results recorded; every report | none | miss |
| keys split where ages jump, not joined; the postcode any of its results recorded; each specimen's first report | none | miss |
| keys split where ages jump, not joined; the postcode any of its results recorded; each specimen's latest final | none | miss |
| keys joined, then split at every age; the first row's postcode; every report | none | miss |
| keys joined, then split at every age; the first row's postcode; each specimen's first report | none | miss |
| keys joined, then split at every age; the first row's postcode; each specimen's latest final | none | miss |
| keys joined, then split at every age; the postcode any of its results recorded; every report | none | miss |
| keys joined, then split at every age; the postcode any of its results recorded; each specimen's first report | none | miss |
| keys joined, then split at every age; the postcode any of its results recorded; each specimen's latest final | none | miss |
| keys joined and split where ages jump; the first row's postcode; every report | none | miss |
| keys joined and split where ages jump; the first row's postcode; each specimen's first report | none | miss |
| keys joined and split where ages jump; the first row's postcode; each specimen's latest final | none | miss |
| keys joined and split where ages jump; the postcode any of its results recorded; each specimen's first report | none | miss |
| keys joined and split where ages jump; the postcode any of its results recorded; each specimen's latest final | none | miss |

- **Cracker keeps:** 0 of the 16 figures; the best of the 35 careful readings keeps 0 (asserted in `checks.py`, one
  check per reading). What either response keeps of the ask weight is the chart's structural parts.
- Mirror leakage: 15.0 per cent of ask weight (the chart's three structural parts; the mirror's ask path is the
  cracker's, the asks consuming nothing the call's construction produces, and every figure misses).
- Pair ceiling: 38.1 (C = 38 + 7 + 55 x 0.20 = 56.0, the cracker keeping the chart's four parts; S = 5 + 7 + 55 x 0.15
  = 20.2; mean 38.1), against the portal's 79 on the first build.
- Measured by: generator/ceiling.py, run on the cut pack.

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
   Judge at the rubric reship (target.zip 5ef00068, `determinism_check_report_pass2.md`): DETERMINISTIC, APPROVE; Gate
   G method_or_model_selection, analytical_non_defect, no surface read, not a sole data defect; Gate H domain pass,
   layers pass, decisive step analytical. It rebuilt the cases from the raw results and reproduced every window count
   and every share-notified change exactly, finding from the data alone that keys sharing a specimen are one person and
   that a key whose ages jump by 21 to 40 years is two (the one-year rises left alone). Its own season-to-date and week
   36 figures came out 2 cases high in four regions and 2 low in the other four, netting to zero: exactly the deltas of the
   address device read off each case's first row, which it could not trace and did not escalate, reading
   s.2's fallback as unambiguous. Block 3 now names the handling (a preliminary sent without the address takes its
   final report's postcode) so a grader can confirm it.
6. Asks, rebuilt on the portal's return of 2026-10-28 (rubric 79, the call held): each region's two figures are moved
   for the cracker by the gateway's person matching (a specimen's preliminary and final under two keys, A 1 or 2 high
   and B 1 case high; an infant under its mother's key, A 1 to 3 low) and, in week 36, by the preliminary sent without
   the address from a requesting service in the next region (every region 2 off); the 35 careful readings miss all 16
   figures (`ceiling.py`, one assertion per reading). The call reads none of it: no changed row in any window, the call's
   115,176 rows and every other file byte-identical to the shipped pack, every reading giving the four flags and every
   window's cases as shipped (asserted). The first build's filed-rule devices stay as hazards.
7. Input gates: 13 files in four formats (csv, md, pdf, xlsx), the gateway results at 229,848 rows, two distractors
   named in metadata.json; 224 generator checks with the realism sweep; the verifier (its own case build, person
   matching and index) green; two builds byte-identical; figures_check 93 of 93; containers clean.
8. Duplicate guard: `guard.py heart` WARN (overuse.org_family; repeat.question_form against task235; same_puzzle_older
   differentiated against task453 and task463); the shape moved from 07 to 11 at stage 3 (task465's architecture 2 holds
   07). `guard.py surface` promoted task234, task235 and task233 (the same author's Data Quality builds: a README and
   dictionary layout and a designation set; task234 predicts a stream's tests from its positivity, task235 judges a
   missing event by its phone's next session, task233 a register statistic's departure under missing not at random)
   and task81, task95 and task73 (surface only), for the author's adjudicated read.
   At the rubric reship, `guard.py heart` BLOCKs on ban.role and ban.forum (task154) and test.same_puzzle (task463),
   all three drawn before this build and outside its window when it shipped (heart WARN then); the draw is a fact of
   the shipped build and is not relabelled. test.same_puzzle_older (task480 v1) and test.same_driver_older (task464 v8)
   are answered on the card. `guard.py surface` exit 0, eleven promoted pairs for the author's read.

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

Rubric reship (2026-10-28, target.zip 5ef00068): leak.py LEAK on DATA_DICTIONARY.md and README.md under the
describing-file rule added on 2026-10-27, after this build shipped; both were in the pack the portal judged, the
dictionary carries conventions the call and its critical components read (local time at UTC+10, 0000 as an unrecorded
address, the report status), and a rubric repair leaves the documents the call reads as they are: left as shipped, for
the author's call. Otherwise REVIEW as before. Reader pass 4 (a fresh copy of the pack and the prompt): Q1 s.4's flag
rule, the estimand (its Q6: nothing says how a region's infections are estimated); Q2 to Q4 none beyond the dictionary
and readme as orientation; Q5 s.3 and the Monday cut-off execute to the golden; Q6 an analytical choice; on the asks,
nothing states or narrates that two keys can be one person or one key two people, nothing beyond s.2 says which
result's postcode places a case, and no marker, stamp, code or comment singles out rows of the results.

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
- The first build's ask primaries, returned by the portal on 2026-10-28 (rubric 79 with the call held, no ask figure
  missed): the preliminary reports (D2, the first delivered, not the latest accepted) are s.2's "the first result
  reporting influenza", so the top responses kept every preliminary and dated each case by it; demoted to a hazard.
- The 28 June boundary review as ask A's primary (D2, an attribute at the wrong vintage): s.2's "under the postcode
  concordance in force at the report" files it, and the responses read every case under the current rows; a hazard.
- The cut-off in UTC, blank and 0000 by the requesting service and residents of other states as the asks' hazards of
  weight: each a sentence of s.2 or the dictionary's received_utc, executed by both responses; kept as hazards, the asks
  now carried by the person matching and by an address recorded on one report only.
- An amended result (a positive corrected to not detected) as an as-of device for the asks: whether a case withdrawn
  after the cut-off still counts in the week 36 report, and whether an address recorded after the cut-off places a
  case, are open readings of "as the week 36 report counts them" (s.2's Monday cut-off against the readme's Tuesday
  extract); dropped, and every device instance sits on people whose every result reached the gateway by the cut-off.
- One laboratory stamping receipt in local time as UTC (D8): it makes the dictionary's received_utc false for one
  service; dropped.
- A specimen under two keys with no later results under the second key, alone: a reader who collapses each specimen to
  its first report absorbs it, so the infant under its mother's key and the address on the final carry that reader.
- The birthday's over-cleaning half spread over every region's season: the South Coast has no person outside its
  window with two positive specimens before week 28, so its season keeps the week 36 birthday alone; the per-region
  counts were then re-set so that no subset of mishandlings composes back (the Central West's season keeps one birthday
  because its two straddling cases would cancel two).
