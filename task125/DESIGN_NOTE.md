# task125 design note (architecture 4, the Mountjoy hot spot patrols)

Architectures 1 to 3 are spent and in the card's lineage; their measured deaths are in the last section of this note.
Architecture 3 died as a planted-defect flip, so this draw is held to one test before anything else: every recorded
number in the pack is accurate as recorded, and the easy route uses accurate numbers the wrong way.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task125.json`, architecture v4, registered 2026-10-31T22:06:02Z after
  `guard.py recent`, `coverage` and `mechanisms --objective anomaly-detection`. `check` PASS: the one older structural
  match (task178 v3, gap time, pattern G5, method selection) is differentiated on the card, and the bans against the
  last three builds (task306 v4, task191 v4, task482 v16: committee_or_panel and other forums, launch, audit and
  purchase-order events, financial and manufacturing organisations) are clear.
- **Pairing:** Criminology & Justice, task type crime-incidence-hotspot-analysis, objective Anomaly Detection &
  Diagnostics, a pairing never built: which street segments of a city are its 2027 hot spots, the places whose patrol
  crime stands far above the rest, for a two-car directed-patrol programme with room for 20 segments.
- **Shape:** 01, a ranked list under a cap: each candidate segment's expected 2027 patrol crimes, the cut at 20, the
  designated set; the asks' ward-by-quarter and ward grids supply the rest of the criteria.
- **Strategy:** `composition_mix`; Gate G `method_or_model_selection`; gap time then population; generators G5 (the
  crowds that raise a segment's crime are provided elsewhere in 2027), G6 (each segment's crime is a mix of a steady
  part and an event-night part whose weights move), G13 (the record's horizon is not the window's).
- **Data-native sentence:** the five street segments around the Memorial Gardens and the five around the Lakeshore
  Centre record about half their street crime on their venue's event nights, and from January 2027 the Mariners play
  their home games at the Lakeshore Centre, so the Gardens keep a handful of shows and the Lakeshore takes the season.
- **World:** the City of Mountjoy, Ontario, a fictional lakeshore city of about 120,000; the Mountjoy Police Service,
  which also polices the Township of Elmvale under contract; the Mountjoy Mariners, a junior hockey team; the Memorial
  Gardens (the old arena) and the Lakeshore Centre (the city's events centre, reopened to take the team). People from
  `guard.py names --geo Canada --seed 125`: Lindsey Turner (Superintendent, Patrol Operations, the requester), Eric
  Gordon (Manager, Crime Analysis Unit, the protocol's owner), Ruben Stafford (Chief of Police, who approved the
  protocol and chairs the command team).
- **Forum and forcing event:** the Chief's command team (executive_team) adopts the 2027 designation with the
  deployment plan on 12 January 2027; the designation is made once the year has closed, for the calendar year ahead
  (period_close; vote_or_meeting was banned against task172 v2, drawn just before, and the card was re-registered at
  2026-10-31T23:51:44Z); the extracts are of 6 January 2027; the organisation is a municipal police service
  (local_government).
- **Sources:** synthetic throughout, modelled on how Ontario police services keep records-management occurrence
  exports, paid-duty registers, CAD exports and tour rosters, and on street-segment hot spot practice (Weisburd's law of
  crime concentration, the Brantinghams' crime generators); no real dataset, person or organisation.

## Default path

1. Read the protocol: the command team designates the 20 street segments with the highest expected patrol crimes in
   calendar 2027; patrol crimes are the Table 1 codes, each occurrence once on its latest version, unfounded out, dated
   by occurrence.
2. Conform mps_rms_occurrences_2022_2026.csv: latest versions, legacy codes through the 2023 crosswalk, the legacy
   versions' day-first dates, unfounded dropped, the report date where there is no occurrence date.
3. Count each segment's founded patrol crimes by year, and back-test the field's forecast of next year's hot spots
   (last year's counts, crime at places being stable): the 2025 ranking recovers 20 of 2026's top 20.
4. Take each segment's 2027 expectation from its own record (its 2026 count, its 2022 to 2026 mean or that mean shrunk
   to the city's) and designate the top 20: the 14 chronic segments, King St from Wellington to Albert, and the five
   segments around the Memorial Gardens (Albert St King to Queen, Queen St Wellington to Albert, Wellington St King to
   Queen, Wellington St Queen to Princess, King St Water to Wellington).

Ends on: the five Memorial Gardens segments in and the five Lakeshore Centre segments out
Golden: the five Lakeshore Centre segments in and the five Memorial Gardens segments out

## Stump sentence

The default path designates the 14 chronic segments, King St from Wellington to Albert and the five Memorial Gardens
segments, leaving the five Lakeshore Centre segments out; the step that lands it there is forecasting each segment's
2027 from its own record, when about half of the venue segments' street crime falls on their venue's event nights and
the paid-duty register's 2027 sheet books the Mariners' home games at the Lakeshore Centre from January.

## Three rules

Task type: crime-incidence-hotspot-analysis (Criminology & Justice), which serves Anomaly Detection & Diagnostics: the hot spots are the street segments whose patrol crime stands far above the city's, diagnosed by what generates it there.
Domain test: the quantity that decides is each street segment's expected count of founded patrol crimes in 2027, the hot spot forecast place-based policing rests on, and environmental criminology reads an arena as a crime generator whose crowds raise street crime on the segments around it on event nights; put a hospital ward in for the segment and nothing generates on a published calendar, so the forecast has nothing to move.
Swap: "Which hospital wards get the 2027 infection-control nurses, by expected infections?" reads differently, because a ward's infections do not come from a building next door whose crowds arrive on a published calendar and move to another building in January.
Layer 1: the records system's export as it writes it (one row per report version, later versions reclassifying, correcting the segment or recording an occurrence unfounded; legacy codes and day-first dates on versions entered before the March 2023 migration; occurrences with no occurrence time dated by their report; reports of 2021 and 2027 occurrences inside the extract), the paid-duty register in two layouts (one row per booking to 2023 with abbreviated venue names, one row per officer line from 2024), the CAD's UTC stamps and the township's events in the dispatch export; each is produced by the system that records it and none is placed to be caught.
Layer 2: composition_mix in the estimation_fit family: each segment's count is a steady part plus a part tied to its venue's event nights, the 2027 calendar moves the second part, and the comparison is decided by forecasting each part on its own calendar.
Decisive step: splitting each segment's record into its steady rate and its excess on each venue's event nights, and carrying the excess by the venues' 2027 calendar instead of by the segment's own past.
Not semantics: every field, code, unit and date read right still leaves each segment's 2026 count and its five-year mean, which are correct counts and put the Gardens segments on top; no column says which crimes came with a crowd or where the crowds go in 2027.
Not rule application: the protocol files the estimand and no method, and executing every filed rule with the field's forecast (last year's count or a multi-year mean) files the default; enumerated family, 40 constructions (counts, means, shrunk mean, trend, last 365 days, the 2026 count scaled by nights, the Gardens' excess removed, the proximity swap, the event-aware fits), 5 distinct designations, spread of five segments; standing family (the event-aware fits on three to five years, three 2027 calendars, with and without day-of-week terms), 18 members, one designation; the ruling-out is quiet, the venues' event nights in the register against the occurrence dates, with no sentence.
Analyst test: a strong analyst conforms the export (latest versions, crosswalk, day-first legacy dates, unfounded out), reads the protocol, back-tests last year's counts as the forecast (20 of 20) and designates the 14 chronic segments, King St from Wellington to Albert and the five Memorial Gardens segments, leaving the five Lakeshore Centre segments out; every field is read and every rule applied, and the call is wrong because those segments' 2027 crimes follow the venues' 2027 calendar.
Estimand: hot_spot_patrol_protocol_2027.pdf sections 2 and 3: population, the street segments in the City's street segment file; outcome, founded patrol crimes (Table 1 codes, each occurrence once on its latest version, dated by occurrence) expected in calendar 2027; unit, crimes per segment; comparison, the 20 highest.
No decoy: nothing is planted to be caught; no memo, briefing or earlier designation ranks the segments; the ward profiles and the streetlight requests are context; the register is the paid-duty office's own record.
No certified replay: no certified or published figure reproduces the method; no file carries an expected count, a hot spot list or an event effect.
Lesson: a hot spot forecast built on a place's own record assumes what generates its crime stays put; a model that learns to split a place's count into its steady part and the part a scheduled generator brings, and to carry each by its own calendar, forecasts the way environmental criminology reads crime generators, which no build on file teaches.

## Survivor anatomy

Actor: the deciding property, how much of a segment's crime comes on a venue's event nights, has no column; occurrences carry a date and a segment, the register carries duties at addresses, and the property is a relation between the two.
Link: no key ties an occurrence to a duty; the comparison that reads it (a segment's crimes on a venue's event nights against its other nights) is one the field's ranking never asks for, and no sentence invites it.
Reflex: the field's forecast of next year's hot spots, last year's count or a multi-year mean (crime at places is stable), sits at rungs 0 and 1 and files the default.
Back-test: the textbook route validates: the 2025 ranking recovers 20 of 2026's top 20, because the Mariners played at the Gardens in both years.
Second use: the register is the paid-duty office's own record of every duty in the city (traffic control, escorts, film, security and events) and comes in Information Management's standard extract set; the occurrences carry the ranking, the street file the ranking and both asks.
Shock: the Lakeshore segments' 2026 counts (30 to 38, ranks 21 to 29) read as ordinary; the golden 20 is the top of no single statistic among nine sorted (checks.py SHOCK).
Pins: the WHAT sits in the protocol (the segments, the codes, the counting, the date, the year, the 20) and Directive PO-14's measures; no filed sentence names events, venues, a calendar, crowds or how to forecast (R0, SF1 to SF11).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 each segment's 2026 count | the protocol's estimand | the occurrence columns | the field's forecast | none | the battery cleans the export | one count | yes | readable |
| R1 the five-year mean, or shrunk to the city's | none | the occurrence columns | crime at places is stable | the 2025 back-test confirms it | the battery | one mean | yes | readable |
| R2 trend, or the last 365 days | none | the occurrence columns | a forecaster's habit | none | the battery | one fit | yes | readable |
| R3 (decisive) each segment's steady rate and venue excess carried by the 2027 calendar | none names events, venues, crowds or a calendar | no column holds a crime's crowd or a segment's venue | not the hot spot reflex | no file prices any segment's 2027 count | the battery stops at clean counts | not affine in any shipped column | the register is the paid-duty office's own record of every duty | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | founded | not unfounded on the latest version | unfounded on any version | same call (asserted) | protocol section 3, Founded |
| SF2 | legacy codes | read through the 2023 crosswalk | not patrol codes | same call (asserted) | protocol section 3, Patrol crime |
| SF3 | counting | each occurrence once, latest version | every version | same call (asserted) | protocol section 3, Counting |
| SF4 | an occurrence's date | occurred_from, the report date where none | the report date | same call (asserted) | protocol section 3, Date |
| SF5 | an occurrence's segment | the latest version's | the first version's | same call (asserted) | protocol section 3, Counting |
| SF6 | legacy dates | day first | month first | same call (asserted) | convergence |
| SF7 | the 2027 calendar | 2026's nights with the Mariners at the Lakeshore Centre | the 2027 bookings alone; the five-year average with the move | same call (asserted, C2 and C3) | convergence |
| SF8 | the fitting window | 2022 to 2026 | three or four years | same call (asserted) | convergence |
| SF9 | day-of-week terms | none | in the fit | same call (asserted) | convergence |
| SF10 | the designation's population | every segment | the candidates | same call (asserted) | protocol sections 2 and 3 |
| SF11 | a tie at the cut | none | none | margin 23 asserted | M1 |
| SF12 | a call | a request received, not an officer-started event | every event | moves the asks only | Directive PO-14, section 2 |
| SF13 | a call's date | the local receipt date | the UTC date | moves the asks only | Directive PO-14, section 2 |
| SF14 | a tour's date | the date it starts | the dispatch's date | moves ask A only | the roster's only 2025 rows, the night tour of 31 December 2025 (asserted) |
| SF15 | a call's ward | the ward its address lies in, by the street file | the CAD district | moves asks A and B | Directive PO-14, section 2: a ward counts the calls at addresses in it |
| SF16 | priority 1 | the dispatched priority | none | same figures | Directive PO-14, section 2 |
| SF17 | the first officer's arrival | the earliest onscene of any unit | the first unit dispatched | moves ask B | the prompt's words (asserted) |
| SF18 | a venue's event night | any EVENT duty at the venue, games and shows | the Mariners' games alone | the Lakeshore excess unidentified | the data: the Lakeshore Centre held no hockey night before 2027 (asserted) |
| SF19 | the venues in the old layout | MEM GARDENS and LAKESHORE CTR read as the venues | missed | same call (asserted, a 2024 to 2026 fit) | convergence |
| SF20 | a night with both venues busy | counted for both | for neither | same call (asserted) | convergence |
| SF21 | officer-hours | dispatch to clear times the officers on the unit | unit-hours | moves ask A | Directive PO-14, section 2 |
| SF22 | a crew across a tour change | none crosses | none | same figures | no assignment crosses a change (asserted) |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 0 | each segment's 2026 count | the default: the 14, King St Wellington to Albert, the Gardens five | the venue segments' crime follows their venue's nights |
| 1 | the 2022 to 2026 mean, or shrunk to the city's | the default | the same |
| 2 | trend, or the last 365 days | the default | the same |
| 2b | the 2026 count scaled by each venue's 2027 nights over its 2026 nights | another wrong set (King St Wellington to Albert out, a warm segment in) | the steady part does not move with the calendar |
| 2c | the Gardens' excess removed, nothing added at the Lakeshore Centre | another wrong set (three warm segments, one Lakeshore) | the crowds go to the Lakeshore Centre |
| 2d | the Gardens five swapped for the six segments nearest the Lakeshore Centre | another wrong set (17 of the golden) | the crowds walk to the terminal and the bars, not to the nearest blocks |
| 3 (decisive) | steady rate plus each venue's excess, carried by the 2027 calendar | the golden: the 14, King St Wellington to Albert, the Lakeshore five | the golden |

- **Margins on the cut pack** (checks.py): the golden's 20th (Simcoe St, Sherbrooke to Hunter) expects 57 and its 21st
  (Lake St, McDonnel to Parkhill) 34, a gap of 23; every member of the standing family files the same 20 (C2, C3), as do
  the same calendars fitted on one or two years (8 of 8, INFO). Every count route files the default (R0), on the clean
  truth too (R0t).
- **Pricing sequence.** (1) The residue the filed WHAT leaves is how 2027 is expected, a method. (2) The Gardens five
  must fall from 48 to 65 recorded in 2026 to 27 to 31 expected, and the Lakeshore five rise from 30 to 38 to 76 to 82:
  about half their crime falls on their venue's nights (801 of 1,345 on the Gardens' 200 nights, 410 of 822 on the
  Lakeshore Centre's 61). (3) No one-group-by reaches it; the two half-aware routes miss (2b, 2c). (4) The standing
  family is unanimous; the easy route sits outside it because the event nights refute a stable forecast for these ten
  segments. (5) and (6) No variance is corrected. (7) No subset of rows prints a segment's 2027 count. (8) The reflex
  sweep runs as code (R0, R1, R2, SHOCK).

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the street segments in the City's street segment file | filed (protocol section 3) |
| 2 Unit of account | founded patrol crimes per segment | filed (protocol section 3) |
| 3 Attribution window | calendar 2027 | filed (protocol section 3, Expected patrol crimes) |
| 4 As-of dating | an occurrence's occurred-from date, the report date where none | filed (protocol section 3); SF4 |
| 5 Version basis | the latest version of each occurrence | filed (protocol section 3); SF3, SF5 |
| 6 Denominator | none: a count | filed |
| 7 Weighting | none | filed |
| 8 Window length | the record 2022 to 2026; one calendar year forward | filed; SF8 |
| 9 Boundary inclusivity | 1 January to 31 December | filed; the 2021 and 2027 reports fall outside (asserted) |
| 10 Rounding path | whole crimes on the chart, from unrounded expectations | C1; no graded expected count |
| 11 Tie-break | none needed: the gap at the cut is 23 | M1, SF11 |
| 12 Maturity and censoring | occurrences reported by the extract; 2026 complete to 31 December | asserted (C0) |
| 13 Order of operations | conform, count by day, fit, carry, rank | C0, C1 |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | each occurrence once | filed; SF3 |
| 16 Identity normalisation | legacy codes through the crosswalk | filed; SF2 |
| 17 Netting against gross | unfounded occurrences out | filed; SF1 |
| 18 Dimensional units | crimes a year | filed |
| 19 Code and status semantics | Table 1 codes, UNFOUNDED, the legacy CLR codes | filed (protocol section 3, the crosswalk) |
| 20 Integerisation | whole crimes on the chart only | C1 |
| 21 Clause scope | the protocol binds the call; Directive PO-14's call, ward, tour and officer-hour definitions bind the asks | filed scope |
| 22 Forward window contents | 2027's event nights at each venue from the register (2026's calendar with the Mariners at the Lakeshore Centre, or the bookings, or the five-year average) | SF7, convergence |

## Literal reader

Executed word for word, the protocol designates the 20 segments with the highest number of founded patrol crimes each
is expected to record in calendar 2027. A literal reader has to expect a 2027 count; the register's 2027 sheet books the
Mariners' home games at the Lakeshore Centre and the record shows the venue segments' crime on their venue's nights,
so the expectation that uses what the pack holds about 2027 files the golden; an expectation that carries 2026 forward
reads 2027 as 2026, which the pack's own 2027 bookings contradict.

## Oracles

None on the main call: no file carries an expected count, a hot spot list, an event effect or a ranking. The verifier
(generator/verify.py) recomputes the designation by cell means and every ask figure with pandas from target/ alone.

## Ask sheet

Two asks on the deployment plan's 2026 picture, each by ward, neither reading the occurrences the call ranks nor the
register the call reads.

**Ask A, each ward's officer-hours on calls for service in each quarter of 2026 (32 figures, whole hours).**
- H18 home: the patrol workload the command team deploys against. Files: mps_cad_calls_2026.csv,
  mps_patrol_roster_2026.csv, mountjoy_street_segments.csv (12 columns on the path).
- Primary device (D8, a recorded date for the event date): the roster dates each night tour by the evening it starts,
  so a unit dispatched between midnight and 07:00 is crewed by the previous date's night tour; joined on the
  dispatch's own date it takes the next evening's crew, and crews change from night to night. Moves 32 of 32 alone.
- Second primary (D5, out-of-scope rows known by structure): the Communications Centre also dispatches for Elmvale,
  whose events carry its patrol zones in the district column under the same numbers 1 to 8; only the segment, outside
  the street file, shows them. Moves 32 of 32 alone.
- Hazards: UTC stamps (a call's date is its local receipt date), officer-started events (not calls), cancelled units
  (dispatch to clear).
- Pin test: the asking sentence pins the ward, the quarter and the unit; Directive PO-14 pins a call, its date, the
  tours' hours and officer-hours; neither names a tour's date or the township.

**Ask B, each ward's median minutes in 2026 from the receipt of a priority 1 call to the first officer's arrival
(8 figures, one decimal).**
- Primary device: Elmvale's events in the district column (D5), moving 8 of 8 by 0.1 to 0.5 minutes.
- Hazards: officer-started events (zero minutes), cancelled calls with no arrival, UTC stamps, sergeants first on
  scene.

| Ask row | The cracker (landed the call, hygiene battery, every filed definition executed) | Verdict |
|---|---|---|
| A, 32 ward-quarter officer-hours | crews each unit from the roster's tour of the dispatch's own date and reads wards from the district | miss |
| B, 8 ward medians | reads wards from the district, Elmvale's zones included | miss |

Pair ceiling: 28.5 ((38 + 7 + 55 x 0) and (5 + 7 + 55 x 0), averaged)
Mirror leakage: 0.0 per cent of ask weight
Measured by: generator/ceiling.py (run on the cut pack, target.zip 5e01ea0a)

## Leak review

`leak.py task125 --asof 2027-01-06` on target.zip 5e01ea0a: REVIEW, no LEAK; each line ruled.
- Sweep 3, golden figures in the pack: every hit is a segment number (the designated segments' ids) in the geography
  files (the street file, the occurrences, the CAD export, the streetlight requests), where every segment's id
  appears; harmless.
- Sweep 4 on the protocol (calendar, occurrence, record, counts): the protocol's own nouns for its estimand (the
  calendar year, occurrences, the records system, counting); it names no event, venue, schedule or method; harmless.
- Sweep 9, the register's dates after the extract: the paid-duty register's bookings for duties still to come
  (status BOOKED), the register's own content; harmless.
- Sweep 12 first refused a field guide to the exports (a document naming the files' columns, LEAK); it was replaced by
  Directive PO-14, which defines the measures in the Service's own words and names no file field.

## Pre-ship check

1. The three rules re-read against the built pack: the decisive step is the split of each segment's record into its
   steady rate and its venue excess, carried by the 2027 calendar, analytical; every recorded number is accurate, and
   the mess is Layer 1 only, each piece asserted not to move the call (SF1 to SF6, SF18 to SF20).
2. Determinism: the WHAT filed in the protocol and Directive PO-14; every standing member files the same 20 (C2, C3);
   no expected count is a graded figure.
3. Gates on the final cut (target.zip 5e01ea0a): generator checks (58, none failed), the verifier, two
   byte-identical builds, figures_check.py (94 of 94), precut.py (61 checks, no FAIL or WARN), voice-check.py,
   leak.py (REVIEW, ruled above), guard.py heart (WARN only) and surface (exit 0; one pair promoted for the author's
   adjudicated read, task178 at surface 0.090 on card axes the card already differentiates).
4. Guard WARN repeat.gate_g (method_or_model_selection against task172 v2, drawn just before): task172 chooses how an
   interim's conditional power carries a trial's treatment effect over its remaining follow-up; here the method is a
   forecast's split of each place's count by a venue calendar. The labels share a Gate G mechanism, not a driver;
   the heart's nearest driver sits at 0.11.

## Tried and rejected


- The source note's decisive rung (Housing Support's cohort run off on the 2021 intake's 30-instalment term) as the decisive rung: the pilot's plain solver replays records at the finest grain and runs event studies on staggered cohorts, and the 2021 intake's full rise and run-off sits in the same flagged-cell series, so a strong solver constructs it; kept as rung 3.
- Re-pricing Adult Social Care's standing stream at a 2027/28 tariff filed in the council's budget (band 2 from 366 to 399 a week, out of cell 14): honestly labelled (time, A) or (time, G13), which the guard blocks inside the batch (task121 v1 lineage) and as spent in ten older builds, with G13 task122's decisive generator; a relabel to G11 or G6 would not name the move as a reviewer would. It also hangs on a stated rate one multiplication from the digit consequence.
- An upward entrant move with the cohort drop under about a sixth of the closed-year figure: the run-off (down) and the entrants (up) cancel near the closed-year carry-forward, which then lands inside 10 per cent of the answer (L4); the targets keep the drop near 30 per cent.
- Step-down hosts inside the flagged cell, paid the same 1,464 as long-term band 2 hosts and separable only by the turnover pattern in their payment histories (a downward decisive move): its honest label is G3 (record versus operation), task121's decisive generator, and the affected payments sit in the very cell the solver is already examining.
- A guest-level arrangements register in the pack: it turns the carers' composition into a schema-visible join from payee to guests, RC01 v2's death (a two-hop join found from the schema alone) and FC01 loop 2's (a dated attribute of an entity the chain already joins); not shipped.
- Landlord-consolidated remittances in the Tenancy Sustainment scheme (a landlord's monthly payment falling into cell 14 once one household remains): the forward entrants are a few per cent of the answer at any realistic landlord mix, too small for a decisive rung.
- A fourteenth four-weekly cycle in 2027/28 (a 366-day year with a payment date on 1 April 2027) or a 53-Thursday year as a rung: worth 2 to 8 per cent of one stream, a knife-edge hazard; the design picks cycles that add no plan-year date unless it prices the cell.
- A plan-year move from four-weekly to monthly payment, or to fortnightly payment runs: a stated change the solver applies at first order, and its amount consequence sits on the remittance grain a screen rung already validates.
- The filter's own examination holds merging held payments into the next run: a council's digit filter examines after payment, and the merge timing opens forks the judge would read as unpinned.
- The 2025/26 screen close-out as the context artifact (close_out_summary): blocked at registration by ban.artifact against task124, drafted in parallel; the same closed-year figures ship in the filter's 2025/26 run log (operations_log).
- One step-down rate with 70 dual carers on one combined amount (3,044): 910 payments a year land in Adult Social Care cell 30, which then flags itself on the 2025/26 screen (paper ratio about 1.4), so the closure moves payments from one flagged cell to another and the decisive rung is worth zero; three tiers and 60 carers keep every Shared Lives cell under 0.86 of threshold.
- Twins identical on every statement figure (payments tested and MAD as well as the cell-14 count): Housing Support would need about 50,000 payments a year in range, which a county's housing-related support service cannot carry; the twin is held on the run log's 2025/26 line only.
- A second plan-year monthly series for the department that moves most (the draw's criteria arithmetic): a denser split of the committed figure, twelve more criteria the cracker banks free; replaced by the two 2025/26 tables.
- Annotating the plan-year month furthest from the closed-year line: January, February and March 2028 tie at 476 routed payments, an ungradable part; the busiest month (December 2027, 638 by run month) is annotated instead.
- The 2027/28 payment-run calendar on the main path, with "four weeks ending on the run date" as the pin against a 12-run reading: unnecessary, since the 28-day cadence fixes 13 runs and a 12-run reading files the same hundred; kept for the monthly ask only, so the main path carries no file an ask device lives in.
- The spending file from April 2021 with every department's background (build): about 100 MB of CSV; the file starts April 2023 and the 2021 round's histories ship in the Housing Support case extract, which is where the term pin lives anyway.
- Waste & Environment cell 25 as the run log's extra cell (build): a cell-25 count near 500 under 0.86 of its threshold needs a Waste department of more than 22,000 payments a year; cell 11 reaches it with 11,000.
- The rung-1 lever at net cell 20 with Property & Facilities at 7,400 invoices (build): rung 1 landed 8,348, and the net basis with the run-off applied then filed 6,458, inside the answer's hundred; the gross cells 20 to 25 had no room for more bills, so the lever moved to net cell 15 and rung 1 to 8,992.
- Rung 4 (Shared Lives carers' combined amounts decomposed against the weekly rate schedule, step-down placements dropped) as the decisive rung, round 1: the plain solver landed 6,522, filed 6,500, by listing the carer amounts against the rates at its step 4 in its own words, "On each carer pay date, 102 payments are £1,464, and 22 + 20 + 18 more are £1,464 plus a step-down rate (£3,044, £3,272, £3,524). When Home First step-down closes on 31 March 2027 those 60 drop to £1,464". The noisy amount universe did not hide them: the three combined amounts are the only carer amounts equal to 1,464 plus a step-down rate, so the decomposition is one subtraction, not a construction.
- Harden loop 1 (opening line), rung 4 as the decisive rung measured by round 1 plain (proxy 80.2, call landed at path step 4): the solver read every "Shared Lives carer payments" row as one carer's whole fee, summed at the carer grain in its own words, "ASC total: 115 x 12 + 162 x 13 = 3,486", having climbed rungs 2 and 3 and stepped over the side cell by taking the 2025/26 cells; a louder pin, a second decoy or a noisier amount list would only lengthen the same subtraction, so the repair attacks the assumption the sentence holds fixed (one row is one carer's fee) rather than the decomposition itself.
- Rung 5 (joint households' half-fees at the household grain) as the decisive rung, round 2 plain (proxy 85.1, call landed at path step 4, filed 6,700): the solver never constructed the household grain; it decomposed each half against the rate card on its own, read the 2,274, 2,388 and 2,514 halves as two weeks of each rate, dropped the step-down weeks and got 1,484 per vendor, in its own words "2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run". The halves are linear in the household fee, so halving the rates gives the same result as re-summing the household and halving it again; the grain gap never moves a single vendor's post-closure amount, and the rung cannot change the answer (discriminator dominance failed, not silence).
- Harden loop 2 (opening line), rung 5 as the decisive rung measured by round 2 plain (proxy 85.1 after the --landed yes regrade, call landed at path step 4): the solver treated each joint half as two weeks of each weekly rate, in its own words "2,274/2,388/2,514, which leave 1,484 (16). That gives 178 per run", so a grain step whose arithmetic is linear in the fee (halve, then subtract the halved step-down rate) can never move a vendor's post-closure amount; the repair has to make the household grain change the result, which only a non-linear step at that grain (a household-level threshold, cap or rate that a half cannot see) can do.
- Centring the loop 2 answer at 6,902 by trimming a flat stream by one payment a month (Property & Facilities 81 to 80, or Highways cell 49 66 to 65): the 2025/26 batch returns are drawn per payment, so the trim reshuffled the examined counts and put both unused-volume charges 2 pence off a half-pound edge (1,604.48 and 603.52 or 655.04); loop 1's stream counts were kept, the answer is 6,914 (36 from its upper edge) and asks B1, B2 and C are unchanged.
- The whole build after harden loop 2 (rung 6, the joint-household one-guest payment rule, as the decisive rung; round 3 plain missed at 43.3): the determinism judge returned SEND_BACK on 2026-10-10 with the mechanism matching the note on every field, so the build was retired and not submitted.
- Architecture 1 as a whole (2026-10-12, at the re-root): spent by two in-house solves and a judge SEND_BACK; the
  author's no-retirement rule re-roots the slot to architecture 2 on a new pairing.
- Interviewer falsification in a victimisation survey (2026-10-12, at the draw, never registered): fabricated
  interviews are wrong records, so catching them is a planted defect under the three rules whatever the method.
- A sample boost entering all at wave 1 against rotation-group bias (2026-10-12, at the draw): the first-interview
  bias moves a regional rate by about 0.1 point at any realistic boost, too small to carry a call.
- A staggered web-first rollout read by event time (2026-10-12, at the draw): the arm comparison and the per-wave
  phasing are what a survey-literate solver does first, and every estimator choice opens a numeric fork.

- Architecture 2's first ladder (2026-10-20, at this re-root): the methods note's section 5 stated the procedure the
  decisive step executes ("applying the change to the last full quarter collected before it and re-running the
  estimation as in section 4"), so a blind Sonnet reader at medium effort, holding only a fresh unzip of target.zip,
  the prompt and the figure names, took 2 of 2 call figures and 38 of 53 ask figures and quoted that sentence as what
  told it the step. Under rule 3 that is rule application, not analysis. Not repairable by deleting the sentence
  alone, because the base quarter it pinned would then be an open knob (measured: up to 0.085 point of movement on a
  figure printed to 0.01); the re-root deletes the sentence, lets the call-record app's coverage settle the base
  quarter, and moves the cap's timeline so the decisive step carries the headline.
- Keeping the cap on one intake and removing section 5 only (2026-10-20, at the re-root, measured): with the cap
  issued for a single quarter before the released one, the wave-1 route and the golden give the same cap share of the
  April to June to July to September change, because only one of the two quarters has a capped wave 1. The decisive
  step then carries no graded figure of the headline, only the forward path, which is exactly the half the measured
  reader took last. Rejected for the field-year timeline, which puts a capped intake in both compared quarters and
  makes the wave-1 route file 0.00 of the 0.27-point rise.
- Grading the non-contact bias of the published rate instead of the six-visit counterfactual (2026-10-20, at the
  re-root): the level of the bias is genuinely unobserved (measured at +0.78 to +0.84 point of unemployment in every
  pre-cap quarter against the eligible population, and +0.99 under the cap), which would put an estimated quantity in
  the deciding position. Rejected on the determinacy screen: it needs the never-contacted households, whose outcomes
  are reached only by extrapolating a level-of-effort gradient past the sixth visit, and the geometric contact process
  behind the pack is a three-class mixture whose tail mass is identified only to within a wide band, so the estimator
  family would be open on a figure printed to 0.01.
- Making the wave structure something the solver infers from the sample's own composition rather than from the methods
  note's section 1 (2026-10-20, at the re-root): a methods note that does not document a rotating panel's rotation is
  not a methods note, and the person file carries a `wave` column besides, so the rotation is schema-visible whatever
  the documents say. Readability test 2 fires. The re-root leaves the rotation filed and moves the decisive step to
  the unit the change acts on instead.
- Identifying the capped-out households from the capped intakes rather than from a pre-cap quarter, so that the
  counterfactual is estimated rather than subset (2026-10-20, at the re-root): with the pre-cap call records removed
  the forward path is unidentified, because nothing then measures how the selected households' outcomes persist
  across the telephone waves; with them shipped the counterfactual is exactly recoverable by subsetting and the step
  is arithmetic. Same dial, both ends. Recorded as the architecture's structural ceiling: no stage-2 move puts an
  estimated quantity in the deciding position on this draw, and a third measured Gate F failure retires the number
  rather than hardening it.

- Architecture 2 as a whole (2026-10-31, at the batch audit, re-rooted rather than repaired): it shipped before the survivor-anatomy gates and falls short on all three of them. The actor is schema-visible (the person file's `wave` and `intake` columns, the visit number reaching the later waves through the household serial, a key that invites the join), so there is no actor without a column and no link without a key; and the field's method (re-running the calibrated estimator on the capped subset) is the golden rather than the bottom of the ladder, which its own "Not rule application" line conceded by calling the decisive step exact arithmetic on recorded fields, argued rather than measured. Architecture 3 draws a new domain and world.
- Architecture 3 (2026-10-31, the Umzimela sulfate load directives, at stage 4): the determinism judge returned
  NOT_DETERMINISTIC with SEND_BACK and the reconciliation confirmed it. The decisive step was catching four boundary
  samples taken in unmixed plumes and swapping in the sum of the inflows' loads (mechanism planted_defect_flip,
  family surface_read_rejection, sole_data_defect yes): the schedule executed literally files MZ2 and NY3 over and MZ4
  and NY2 within, the reverse of the golden, and no shipped sentence says a sample is unrepresentative. The asks also
  rode unfiled methods (drift removal additive or proportional, a sulfate basis change from SO4 to S). Lesson: every
  recorded number must be accurate as recorded and the governing text executed word for word must give the golden;
  a stump that catches a wrong measurement is a planted flip at any depth. Report kept as
  determinism_check_report_arch3.md.
- Architecture 4, ask A first drafted as each ward's founded patrol crimes by quarter of 2026 (the first prompt, 2026-10-31, at the design): it reads the occurrences the call ranks, so any device on it would move the call or ride the call's own cleaning; re-sited onto the CAD and the patrol roster.
- Architecture 4, a payroll export as ask A's device, its night hours split at midnight onto a next-day line with no booking reference (2026-10-31, at the design): pairing a record's halves is in the hygiene battery, so the cracker links them and keeps the ask; replaced by the roster's night tour dated by the evening it starts.
- Architecture 4, the 2027 calendar with the reopened Lakeshore Centre's season unbooked at the extract (2026-10-31, at the build): the Lakeshore segments' bookings-only expectation sat level with the warm segments and that member filed another 20; the Lakeshore Centre's first season is on sale at the extract (18 shows booked) and every 2027 calendar now files one designation.
- Architecture 4, the first parameter sets and seeds 125043 to 125045 (2026-10-31, at the build): increments near one crime a night put two thirds of the Gardens segments' crime on event nights, and the narrower gaps let a Lakeshore or warm segment into the count routes or let a one-year fit swap King St, Wellington to Albert, for a Gardens segment; the steady rates were raised, the gaps widened and the seed taken from a search of the ladder's conditions (125054: the gap at the cut 23, every count route on the default).
- Architecture 4, a third ask on each ward's paid-duty hours worked in 2026 (2026-10-31, at the design gate): every hazard on its path (overnight duties, cancelled and no-show lines, intersections) is in the hygiene battery, so the cracker kept all eight figures and the gate's per-ask miss rule refused it; a midnight-split payroll, a ward stored at booking and reissued booking numbers were each weighed as its device and set aside (pairing halves is in the battery, a stored ward forks the ward set, the reissued numbers bite in January only); the ask was dropped and the register stays in Information Management's standard extract set.
- Architecture 4, a field guide to the six exports (2026-10-31, at the leak sweep): leak.py sweep 12 refused it as a document describing the data (39 columns named, every column of the roster); its definitions of a call, its date, officer-hours and the tours moved into Directive PO-14, a governing document in the Service's genre, the codes and counting stayed in the protocol, and the formats were left to the files.
