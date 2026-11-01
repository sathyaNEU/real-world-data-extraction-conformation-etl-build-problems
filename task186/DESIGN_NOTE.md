# task186 design note

Architecture 2, drawn 2026-11-01 at the Batch 3 queue reset. The author had every queued task rebuilt as a fresh,
unique architecture on what the approved builds share, so architecture 1 (the provincial fuel price monitor, shipped
2026-10-13 with no portal result) was re-rooted. One architecture per world: the fuel-price pass-through world is
closed, and the slot moves to another client domain (Human Factors & Ergonomics) and a new world, an airport's X-ray
screening workforce. Architecture 1's record is under `## Architecture 1 record`.

## Draw

1. **Card:** `.claude/skills/fingerprint/cards/task186.json`, architecture v2, registered 2026-11-01 at WARN with no
   BLOCK (`shell.repeat` read the old prompt and clears with the new one; `driver.near` 0.13 against task190 arch 3,
   probability-proportional-to-size sampling, a different mechanism; `overuse.gate_g`, method_or_model_selection is
   the honest key for a step that decides which records measure the estimand). Architecture 1 moved into `lineage`
   with its fate. Axes drawn free of the live window at the draw (the last three cards were then task452, task123 and
   task160, which ban professional_services, cooperative_or_member_body and manufacturer, executive_team,
   council_or_assembly and operations_desk, budget_or_appropriation, season_or_peak and launch_or_rollout,
   compliance_or_audit, capacity_planner and operations_director, monitoring_export, register and operations_log,
   and three strategies): organisation `utility_or_infrastructure` (an airport operator running its own passenger
   screening), forum `line_manager_or_team` (the head of security screening decides the list), forcing event
   `audit_or_inspection` (the annual recertification of screening officers), role `field_unit_lead` (the screening
   training and standards lead), context artifact `other` (the stakeholder works from the CT system's projection
   export, the library catalogue and the login register together; `monitoring_export`, the nearest label, is banned
   against task452). Gap `time` first (the decisive structure is each officer's own history of showings of each
   object), pattern none with G10 decisive (an object recurring across its scans and across projections is one
   real-world item shown again), G14 and G6 supporting; the gap/pattern pair (population, E) and every population
   pairing with method_or_model_selection were spent inside the batch.
2. **Pairing:** Human Factors & Ergonomics / `safety-incident-error-analysis` / Anomaly Detection & Diagnostics, a
   pairing never built. The deciding quantity is a human performance measure the field estimates: each X-ray
   screening officer's probability of detecting a threat item, read from threat image projection (TIP), the tool
   human factors uses to measure screener detection in live operation. Missed projections are the errors analysed;
   the anomaly is an officer whose detection is genuinely below standard rather than an artefact of how the measure
   was taken.
3. **Niche:** the year-end recertification of a regional airport's CT X-ray screening officers, at the end of the
   first full screening year on new CT scanners whose 3D TIP library is a fixed set of 360 threat objects, each in
   three scans.
4. **Call and shape:** who among the screening officers comes off X-ray duty at the January 2027 recertification
   (`designation_set`, question form `who`), the officers whose detection performance over the screening year to 30
   November 2026 is below the competency standard's 80 per cent. Shape 10, a scorecard of one measure checked against
   its threshold for every endorsed officer; criteria: the ten officers coming off (10), recertifying the rest (1),
   the call (1), the chart with its parts (5), the files (2), and two asks of 12 and 28 figures (40). About 59.
5. **Strategy and mechanism:** `composition_mix` (an officer's hit rate over the year is a mixture of first and
   repeat showings in proportions that differ by officer, and only one component measures the estimand), Gate G
   `method_or_model_selection`, Layer 2 `estimand_identification`, pattern `own:recognition-of-recurring-test-
   objects-lifts-a-detection-proxy`. Calibration `none`.
6. **Data-native sentence:** the CT lanes' TIP library holds 360 threat objects, each in three scans, and a full-time
   officer is shown about 740 projections in the year, each followed by the system telling them it was a threat, so
   by the screening year about four in five of a full-time officer's projections show an object they have already
   been shown; officers detect those 99.5 per cent of the time against 88.5 per cent for objects new to them, so the
   year's raw hit rate measures recognition of the library for the officers shown it most, and only first showings of
   an object, any of its scans counting, measure detection of an item a passenger carries.
7. **Abstraction sentence** (the one sentence a reviewer holding this build and its nearest approved build would say
   is the same): none writable. Against task281 (a validated sensitivity is a mixture over two capture devices
   recovered from an equipment history): there the latent factor is a property of the record (which camera took the
   image) and the transport is device by device; here no attribute of the record changes, the officer's own history
   with each object changes what a hit means. Against task170 (a failure probability falling with each operator's own
   count of attempts): there the practice is general and forecast forward; here the lift is specific to the item
   shown and the call is a designation now. Against task196 (capture-recapture with a contaminated second channel):
   no second source, no count of unrecorded events. Against task271 (a venue's post-fill move read on fills free of
   the desk's own later orders): there the actor's continuing trading contaminates the outcome window and the clean
   subset is found by time; here nothing contaminates a window, the officer's response to an item is lifted by having
   met that item before, and the subset is found only through the image-to-object link over the whole history.
8. **Four candidates, written before choosing** (the three set aside are in `## Tried and rejected`):
   (a) TIP recognition of recurring library objects (chosen); (b) an epidemiology surveillance baseline aligned on
   each area's school return; (c) interviewer falsification found through informative back-check non-response;
   (d) signals passed at danger per approach at red reconstructed from consecutive trains' headways; (e) resistance
   prevalence under cascade susceptibility testing.
9. **People** from `guard.py names --geo Australia --locale en_AU --seed 186`: Teresa Malone (Head of Security
   Screening, approves SCS-04 and keeps the officer register), Keith Keller (screening systems coordinator, keeps the
   TIP library). Officers' names come from a second draw at the build (same seed, `--n 100`), frozen in params.py
   and assigned through a seeded permutation. Invented names: Silverwattle Coast Airport,
   Kestrine Imaging (CT unit maker), the Kestrine CTX-6 unit, the Kestrine 3D TIP library.
10. **Pack** (twelve files, four formats): the TIP event export, 1 July 2025 to 30 November 2026, UTC (CSV, 74,704
    rows, the spine); the TIP library catalogue (XLSX: objects, images); the CT operator login register (CSV); the
    screening officer register (XLSX); SCS-04 revision 6 (PDF, the governing WHAT); the lane roster for the screening
    year (CSV, 31,616 rows); the payroll export of leave taken (CSV); the CT units' hourly image counts, UTC (CSV,
    38,103 rows); the CT unit register (CSV); distractors declared in `metadata.json`: daily checkpoint queue times
    (CSV), computer-based X-ray training sessions (CSV) and the TIP manager's projection settings (JSON).
11. **Sources, one line each:**
    - Threat image projection: CT and X-ray screening systems insert fictional threat images into real bag images at a
      configured rate and record whether the screener marked each; after the decision the screener is shown the item.
      Regulators and operators read a screener's detection from it.
    - Recognition memory: an image or object seen once with confirmation is recognised far more reliably the next time
      it is seen, which is why test libraries are built large and refreshed; a library small against the projection
      volume measures recognition for heavy users.
    - The client's two-layer standard: the analysis decides on correct data, every reported figure complete and
      correct (the FINE-numbers test, the coordinator's task123 lesson, passed: nothing is missing from the TIP log).
    - This lane's approved anatomy (task196, task236): the WHAT names the quantity in the organisation's words and the
      field's method for it is the rung a precondition of this dataset breaks.

## Survivor anatomy

- **Actor:** the deciding property, whether the officer had already been shown the projected object, has no column in
  any file: the TIP export holds a login, an image number and a result per projection; the library holds which object
  each image shows; the property is a relation between an officer's earlier and later rows through the object behind
  the image, across two files.
- **Link:** the image number to object link sits in the library catalogue (three images per object, no object code in
  the TIP export), the login to officer link in the login register (two login schemes before 1 March 2026); no key in
  the TIP export offers the object, and no sentence invites asking whether an officer had seen it.
- **Reflex:** the field's method, each officer's TIP hit rate over the assessment year against the standard (with
  category balancing or the image-level first showing as refinements), is rung 0 and files three officers off: the
  three casual officers whose raw rates are 76 to 78 per cent.
- **Back-test:** the textbook route validates: the pooled hit rate rises from 90.8 per cent in July 2025 to 98.6
  in November 2026, as a learning curve on new scanners would; officers' rates in the two halves of the
  screening year correlate at 0.87; and the lowest four are the casual officers endorsed between August and October
  2025, which reads as expected.
- **Second use:** the TIP export is the spine every route reads; the library catalogue's image list is what the
  conformation step checks image numbers against (the international server's unpadded numbers match nothing until
  padded) and its object sheet names the categories behind the export's codes; the login register is needed to
  name any officer at all. Delete the decisive step and every file stays.
- **Shock:** five of the six full-time officers the step adds sit inside the recertified officers' hit-rate range
  (91.9 to 99.5 per cent) and the sixth just under it at 91.0, and the ten are not an interval of any shipped
  statistic's sort (hit rate, projections, endorsement date, category-balanced rate, image-level first showings),
  asserted.
- **Pins:** SCS-04 revision 6 files the WHAT (detection performance as the probability of detecting a prohibited item
  carried in a passenger's cabin bag, the screening year in Sydney time, every officer endorsed on 30 November, below
  80 per cent comes off); no filed sentence names repeats, first showings, objects, memory or the library's size.

## Default path

1. Read SCS-04 rev 6: detection performance over the screening year 1 December 2025 to 30 November 2026, every
   officer endorsed on 30 November (the register's Current, 91 officers), below 80 per cent comes off X-ray duty.
2. Conform the TIP export: drop the re-sent D3 day, move UTC to Sydney time, map OP1 and OP7 logins to staff numbers.
3. Take each officer's TIP hit rate over the screening year's projections, the field's measure of a screener's
   detection (checked by threat category, and against each image's first showing, which changes nothing).
4. List the officers under 80 per cent.

Ends on: three officers off X-ray duty, SC17045, SC42948 and SC46133, every full-time officer recertified
Golden: ten officers off X-ray duty, SC16884, SC17045, SC19116, SC19645, SC29369, SC42948, SC43647, SC46133, SC46282 and SC46312

## Stump sentence

A competent analyst takes each officer's TIP hit rate over the screening year and withdraws three casual officers,
SC17045, SC42948 and SC46133, recertifying every full-time officer; the step that lands it there is reading the hit
rate as detection when four in five of a full-time officer's projections show an object they have already been shown
and told was a threat, which officers detect 99.5 per cent of the time, so six full-time officers who detect only 56
to 74 per cent of objects new to them clear 80 per cent on recognition.

## Three rules

- **Task type:** human-factors-ergonomics / safety-incident-error-analysis, which serves anomaly-detection: the
  analysis of screening officers' missed threat items, separating a genuine detection deficit from an artefact of how
  the measure was taken.
- **Domain test:** the deciding quantity is each officer's probability of detecting a prohibited item a passenger
  carries, which human factors estimates from threat image projection; recognition memory of an object shown and
  confirmed after every projection lifts each later projection of it, so the estimate has to be read on what measures
  detection of an unseen item.
- **Swap:** "which transformers' protection relays fail to detect a fault, read from injected test faults drawn from a
  fixed set" keeps the arithmetic and loses the step: a relay does not remember a test fault it has met, so its hit
  rate on a repeated test is its hit rate on a new one; the sentence stops needing the decisive step.
- **Layer 1:** the CT system stamps projections in UTC against a standard written in Sydney time across two daylight
  saving changes; the international TIP server issued its own OP7 logins until the servers merged on 1 March 2026;
  image numbers lost their leading zero on that server; D3's records for 17 February 2026 were re-sent after a network
  outage; category codes in the export against category names in the catalogue; each written by the system named,
  none placed to be caught, each neutral on the call (the R2 block in checks.py).
- **Layer 2:** estimand identification, family `estimand_identification`: the measure in hand is a mixture of two
  components in proportions that differ by officer, and the estimand is one of them; the call flips on reading
  detection from the records that measure it.
- **Decisive step:** reading each officer's detection on the projections of threat objects new to that officer, an
  object counting as already shown once any of its three scans was projected to them since the CT lanes opened.
- **Not semantics:** every field read correctly (the result codes, logins, image numbers, categories, dates and the
  standard's terms) still leaves the easy route on three officers, because no field records whether the officer had
  been shown the object, and the FINE-numbers test holds: the TIP log is complete and correct.
- **Not rule application:** no filed rule or procedure names first showings, objects or memory; executing SCS-04 word
  for word with the field's measure files three officers. The enumerated family (raw hit rate, category-balanced
  rate, the last quarter alone, first showings of each image, first showings counted inside the year only, first
  showings of each object, the same reweighted to the library's category mix, a logistic fit on prior showings read at
  none) spans three to ten officers off; the standing family once the data are read (object-level first showings over
  the whole log, raw, category-reweighted or fitted) spreads zero officers, with every officer coming off below 74.3
  per cent and every other at least 83.3 per cent under each form; what rules out the rest is loud only for a reader
  who links images to objects: repeat showings detected 99.5 per cent, an image new to the officer but of an object
  already shown 99.3, a new object 88.5.
- **Analyst test:** a strong analyst who conforms the TIP export, maps every login and reads SCS-04 correctly takes
  each officer's hit rate over the screening year and files three officers off X-ray duty, SC17045, SC42948 and
  SC46133, every full-time officer recertified; R3a in checks.py runs it on the clean truth.
- **Estimand:** SCS-04 revision 6 sections 3 and 4 (SCS-04_screening_officer_competency_standard_rev6.pdf):
  detection performance is the probability that the officer detects a prohibited item carried in a passenger's cabin
  bag at the X-ray screen of a CT lane, assessed over the officer's screening in the screening year 1 December to 30
  November in Sydney time, for every officer holding an X-ray endorsement on 30 November, below 80 per cent comes off.
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure states a hit rate, a ranking or a
  verdict; the TIP manager's settings file states a projection probability and no result; no block of records is
  copied or withheld; the memory effect is how people recognise what they have been shown.
- **No certified replay:** no certified or published detection figure exists in the pack to reproduce; the method is
  not hidden behind a figure the solver backs out.
- **Lesson:** a hit rate on a test drawn again and again from a fixed set with feedback measures recognition for the
  people shown the set most; before reading it as detection, ask what each person had already been shown, and read the
  measure on the items new to them. No build on file teaches memory contaminating a performance measure.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 raw hit rate over the year | SCS-04 detection term | result column | the field's measure | none | none | yes | no | readable |
| R1 category-balanced hit rate | none | category column | a known refinement | none | none | yes | no | readable |
| R2 first showing of each image file | none | image_no column | a careful refinement | none | duplicate-image check | yes | no | readable |
| R3 first showing of each object over the whole log (decisive) | no sentence names repeats, objects or memory | no object column in the TIP export; the object sits in the catalogue's image list | the field's measure takes every projection as a fresh test | no control scores it | no battery item links images to objects across an officer's history | one filter and a ratio, but only once the relation is seen | the catalogue and logins serve every route | silent |

## Semantic fork table

| Id | Term or convention | Readings | Ruled out by |
|---|---|---|---|
| SF1 | the screening year's dates | Sydney dates, UTC dates | SCS-04 section 3 (Sydney time throughout); same call either way (checks.py) |
| SF2 | who is assessed | endorsed on 30 November, anyone who screened | SCS-04 section 4; the register's Current column (91) |
| SF3 | what counts as already shown | the same image, any scan of the same object | the data: an image new to the officer of an object already shown is detected 99.3 per cent against 88.5 for a new object (checks.py) |
| SF4 | how far back an earlier showing counts | the whole CT log, inside the year only, recent showings only | the data: the lift is 99.5 within 30 days and 99.3 after 120 days, and objects first shown before the year are recognised in it at 99.2 (checks.py) |
| SF5 | category weighting | each first showing equally, the library's category mix | same ten officers (checks.py) |
| SF6 | the estimator on first showings | the share detected, a logistic fit read at no prior showing | same ten officers (checks.py) |
| SF7 | the re-sent D3 day | kept twice, once | same call (checks.py) |
| SF8 | the currency population | endorsed for the whole month, endorsed at any point in it | SCS-04 section 5 (the whole of a calendar month) |
| SF9 | X-ray time resolution | moment by moment, five-minute slots | identical counts (checks.py) |
| SF10 | quarters | Sydney quarters from 1 December, UTC quarters | SCS-04 section 3; UTC moves figures (checks.py) |
| SF11 | passenger bags | every image a unit counts, images while officers screen passengers | SCS-04 section 3 (bags passengers put through a lane); one rostered-time rule separates them (C1 in checks.py) |
| SF12 | below 80 per cent | strictly below, at or below | no officer within 3.3 points of the line under any licensed form (checks.py) |
| SF13 | an officer with few first showings | assessed, held over | every endorsed officer has 107 or more first showings in the year (checks.py) |

## Ladder

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| R0 | each officer's hit rate over the year's projections (the default path) | three casual officers off (SC17045, SC42948, SC46133) | repeat showings are detected 99.5 per cent against 88.5 for new objects |
| R1 | the hit rate balanced across the four threat categories | the same three | the same lift, in every category |
| R2 | each image's first showing to the officer | four casual officers off (adds SC16884, 0.776) | an image new to the officer but of an object already shown is detected 99.3 per cent |
| R2b | first showings counted inside the screening year only | the same four | objects first shown before the year are recognised in it at 99.2 per cent |
| R3 | each object's first showing over the whole CT log (golden) | ten officers off, six of them full-time | golden |

- Separation: R0 and R1 file three, R2 and R2b four, R3 ten; R3 differs from R0 in seven members (asserted by name).
- Margins: every officer coming off below 74.3 per cent under every licensed form (raw 74.22, category-reweighted
  74.06, logistic 73.96); every other officer at least 83.3 per cent (83.54, 83.34, 83.5); the nearest any officer
  sits to the line is 3.3 points. The masked full-time officers' raw rates run 91.0 to 95.0 per cent against a
  recertified range of 91.9 to 99.5, five of the six inside it.
- Pricing: the step moves seven of ten designations; the lift is 11 points of hit probability on a repeat; every
  endorsed officer has 107 to 263 first showings in the year, so a designated officer's estimate carries a standard
  error of 3.4 to 4.7 points, and the decision is the filed comparison of that estimate with 80 per cent. The world's
  free parameters (library size 360, projection probability 1.3 per cent, the memory multiplier 0.12, competent
  officers 0.89 to 0.95 on unseen items, deficient full-time officers 0.64 to 0.72) were set so that every officer
  clears the line by at least 3 points under each licensed form; on nine other seeds (187 to 195) the object-level
  first showings designate exactly the world's ten deficient officers every time while the raw hit rate designates
  one to three.

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | every officer holding an X-ray endorsement on 30 November 2026 | filed (SCS-04 section 4); SF2 |
| 2 Unit of account | the officer | filed |
| 3 Attribution window | the screening year, 1 December 2025 to 30 November 2026 | filed (SCS-04 section 3); SF1 |
| 4 As-of dating | each projection by its Sydney date | filed (Sydney time throughout); SF1 |
| 5 Version basis | the TIP export, library release 1.0, the register as exported 1 December | one version shipped |
| 6 Denominator | the officer's first showings in the year | forced by the data (SF3, SF4) |
| 7 Weighting | each first showing equally | C1: category weighting files the same officers (SF5) |
| 8 Window length | twelve months | filed |
| 9 Boundary inclusivity | 1 December and 30 November inside | filed |
| 10 Rounding path | detection compared with 80 per cent unrounded | C2: no officer within 3.3 points (SF12) |
| 11 Tie-break | none needed | C2 (SF12) |
| 12 Maturity and censoring | none: the log runs to 30 November and the year is closed | C1 |
| 13 Order of operations | conform, link images to objects, order each officer's showings, read the year | C1 |
| 14 Row order | by time within officer | C1: the export is time-ordered; ties at one second never share an object |
| 15 Duplicate resolution | the re-sent D3 day is exact | neutral (SF7) |
| 16 Identity normalisation | OP1 and OP7 logins to staff numbers; image numbers padded | the login register and the catalogue; neutral (R2) |
| 17 Netting against gross | none | C1 |
| 18 Dimensional units | per cent; hours; bags | filed |
| 19 Code and status semantics | HIT and MISS; GUN, KNF, IED, OTH against category names | the export's own codes; the catalogue's names |
| 20 Integerisation | counts of officers and bags | filed (whole officers, nearest thousand bags) |
| 21 Clause scope | currency covers officers endorsed for the whole month; the annual assessment covers the endorsed on 30 November | filed (SCS-04 sections 4 and 5); SF8 |
| 22 Forward window contents | X-ray duty from 1 January 2027 for the officers below standard | filed (SCS-04 section 4) |

## Literal reader

Executed word for word, SCS-04 asks for each endorsed officer's probability of detecting a prohibited item carried in a
passenger's cabin bag over the screening year and takes off X-ray duty every officer below 80 per cent. Nothing filed
says how the probability is estimated. A literal reader who takes every projection as a fresh test files three
officers; one who asks what each projection measures finds that an object already shown is recognised, that a
passenger's item is never one the officer has been shown, and files the ten. Every licensed estimator on first showings
files the same ten.

## Oracles

none: no control, published figure, certified rate or reconciliation column confirms either reading; the TIP manager's
settings state a projection probability and nothing about results, and no file reports an officer's detection.

## Layer 1 inventory

| Item | System that writes it | File | Natural mishandling and its effect |
|---|---|---|---|
| UTC timestamps against a Sydney-time standard | the CT TIP manager | TIP export | the year read on UTC dates; the call unchanged (SF1) |
| OP7 logins before the 1 March 2026 server merge | the international TIP server | TIP export, login register | OP7 rows unmatched and dropped; the call unchanged (R2) |
| image numbers without a leading zero on the international server | the international TIP server | TIP export | rows unmatched to the catalogue and dropped; the call unchanged (R2) |
| D3's 17 February 2026 records sent twice | the TIP manager's resend after an outage | TIP export | kept twice; the call unchanged (SF7) |
| category codes against category names | the TIP manager and the library manager | TIP export, catalogue | read as different categories; only R1 moves |
| roster times local, unit counts in UTC | the rostering system, the CT units | roster, unit counts | ask hazards only (SF10) |

## Ask sheet

Two asks on records the call never reads (the roster, the payroll leave export, the units' hourly counts and the unit
register), both owed by SCS-04's own reporting sections.

**Ask A, for each month from December 2025 to November 2026, how many endorsed officers fell short of the standard's
20 hours of X-ray time (12 figures, whole officers).** Home: SCS-04 section 5, the monthly currency report.
- Primary device (D6, cardinality): X-ray time is the officer's lane time divided by the officers working on the lane at
  each moment, and the roster's rows on a lane-day start and finish at different times (late joiners, early leavers),
  so the divisor changes inside a block; one divisor per roster block files 10, 7, 14, 7, 11, 11, 10, 10, 8, 8, 8, 8.
- Second device (D4, absence in a file no habitual join reaches): an officer on Personal leave in the payroll export is
  still on the roster and was not working, so they take none of the lane and their colleagues' shares rise; leaving
  leave out files 17, 16, 20, 11, 16, 15, 15, 19, 15, 14, 12, 13 (eight months wrong).
- Hazard: no division at all files zero every month.
- Golden: 19, 17, 20, 14, 16, 17, 16, 17, 15, 15, 12, 16 (equal to the clean truth, asserted).
- Pin test: the sentence pins the population (endorsed for the whole month), the unit and the standard's definition of
  X-ray time; no pin names a block, a leave record or a divisor.

**Ask B, the passenger bags each CT lane screened in each quarter of the screening year (28 figures, nearest
thousand).** Home: SCS-04 section 6, the year-end throughput return.
- Primary device (D7, the true key elsewhere): the units' counts are keyed by serial and the unit register keeps only
  where each unit stands now, while KX6-0413 stood on D2 until 2 March 2026, KX6-0416 on D5 until 19 April and on each
  lane for its two retrofit days, and KX6-0590 on D2 only from 5 March; placing units by the register misses 17 of 28.
- Second device (D5, scope): after each unit's retrofit it counts its daily performance-test images in the hour before
  the lane's first rostered start, which are not passenger bags; with every unit placed right and those counts kept, 12
  of 28 figures are wrong.
- Hazard: counts in UTC hours against Sydney quarters.
- Golden: equal to the clean truth lane by lane and quarter by quarter (asserted), and to an independent exhaustive
  placement in verify.py.
- Pin test: the sentence pins the lanes, the quarters and passenger bags (SCS-04 section 3); no pin names a serial, a
  retrofit or a test.

Main population zero-counts: the TIP export, the catalogue, the login register and the officer register carry no ask
device row (asserted); the call reads none of the ask files (asserted from the code).

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| A, 8 of 12 months moved by personal leave | shares each lane among the officers rostered at each moment; the payroll leave export not joined | miss |
| B, 12 June-to-November figures carrying pre-opening test counts | places every unit right and keeps every hourly count | miss |

Pair ceiling: 52.6 ((38 + 7 + 55 x 0.500) and (5 + 7 + 55 x 0.375), averaged)
Mirror leakage: 37.5 per cent of ask weight
Measured by: generator/ceiling.py (run on the cut pack)

## Leak sweep

- `leak.py --asof 2026-12-02`: REVIEW, one line, harmless. Sweep 4 finds four stump-paragraph terms in SCS-04
  (projection, threat, records, return): "threat image projection system" and "records" in section 7 name the system
  and what it records, and "return" is the year-end throughput return in section 6; nothing in the standard names
  repeats, first showings, objects, memory or the library.
- `guard.py surface`: three pairs promoted on surface similarity alone (0.100 to 0.101, corpus top 1 per cent), task462,
  task172 and task271, each with a differentiation line on the card; the people screen is WARN only, the officers named
  in the goldens drawn with `guard.py names`.

## Architecture 1 record (re-rooted 2026-11-01)

A provincial statistics bureau's fuel price monitor (survey-research-official-statistics / anomaly-detection, Canada):
which brand the Fuel Price Commissioner's inquiry examines before the 1 January 2027 carbon levy rise, each station's
28-day margin change across the January 2026 rise tested for excess pass-through with the false discovery rate held at
5 per cent. Golden Tallis Petroleum (30 per cent of its examined stations found); the default path, a within-window
test of each station's margin change, filed Harbourline Fuels, whose areas' price cycles restored over the turn of the
year. Shipped 2026-10-13 (pending review, no portal result). Measured spent on 2026-10-21 at stage 2: the decisive step
was the scale a one-dimensional per-station statistic is read against, so the golden's 28 stations were the top 28 by
the margin change and seven of fifteen data-free cuts filed the call; the three dials that move the gap each traded
Gate F against Gate C one for one. Re-rooted 2026-11-01 at the Batch 3 queue reset.

## Tried and rejected

- General Statistics & Data Science, multiple testing and selective inference, as the domain: blocked by
  `ban.pairing` against task185 (General Statistics & Data Science x Anomaly Detection in this draw's window).
- The seed's panel rule fitted to the closed levy changes: a corpus-fit withheld rule (the guard's banned
  architecture), and the ownership-flag question it rests on is a field reading.
- Brand-level pass-through with town-clustered errors as the filed measure: a brand-level test is not what the
  standard files and its clustered errors leave Tallis short of significance, a competing answer.
- A pooled empirical null with some areas not cycling: the null distribution is a spike and a slab, central matching
  fits the spike and finds the cycling areas' stations, so the empirical null and the placebo null disagree; every
  urban area cycles in the build.
- Pellow's dealer mix with as many company-owned dealer sites as commission agents (6 against 5 and a new company
  site): its ownership count equalled its brand-priced count, so the ownership read hit Pellow's scope figure; two of
  Pellow's company dealer sites made dealer-owned.
- The litres golden reading a station's brand on the first of the month: it dropped the Wexcombe station opened on 9
  March 2026; the brand is read from the station's first day open in the month.
- Survey returns naming the station by its trading name (brand, town and street): the brand could be read off the
  return, which bypassed the reissued references; a dealer's return names its operator's business and carries the
  site address.
- Stations priced by the brand read from minute stamps shared with three or more of the brand's submissions: Garrow's
  five stations change together in twos and threes on quiet days, so a bar of four or a share of four in five dropped
  them; read from the brand's push times (minutes of the day), which every priced station keeps whatever the bar.
- A Canadian-level rack price (0.96 dollars a litre): the price stream moved and Tallis's share on the default path
  fell into the golden's 30 per cent bin; the rack stays at the record's level (pump prices 92 to 132 cents a litre in
  a province whose only fuel taxes are the levy and the sales tax).
- Cairnmore Energy, Pembry, Fennick and Cresswold: each a letter or two from a real company or place (Cairn Energy,
  Pembrey, Fenwick, Cresswell); renamed Strathlowe Energy, Duncarrow, Marrowby and Brindlecote.
- Eight closing dealers on one day (1 April 2026) and new stations opened to take their references: the shared day
  read as a batch marking the device's rows, and a holder with no brand in January failed loudly on the brand join;
  the dealers close on eight days from April to early June and their references go to stations trading all year that
  joined the frame from August, so the frame join succeeds and is wrong.
- The complaints register naming the brand of each complaint: Tallis, the largest brand, drew most complaints, an
  attractor toward the golden; the register keeps area and category only.
- Tallis's dealers placed 42 in the five towns whose cycles were falling at the change and 6 in the three rising
  Pellow towns: Tallis's share on the default path sat at 35.9 per cent, a point from the edge of the golden's 30 per
  cent bin; 38 and 10 put it at 39 per cent.
- One random stream for every station's prices: moving one dealer's closing day moved every later station's prices,
  so each fix to the asks re-rolled the main call's default path; each station now draws its own stream.
- A closed station's brand row left open in the register: a literal read of PM-04 3.2 (the price standing until the
  next change) examined a Wexcombe station closed in June 2025 (370 stations, judge pass 1); the register ends a closed
  station's brand the day before it closed and the extract notes end a price at the closing day.
- Critical components carrying the count of stations found: the same-area null finds 29 Tallis stations where the
  stations' own changes find 28, both 30 per cent; the components state the shares.
- Widening the magnitudes at stage 2, which is what a `FAILED_TO_STUMP` on measurement normally takes: refused on
  measurement. The golden's 28 found stations are exactly the top 28 of 369 by the standard's own 28-day margin change
  and clear of the 29th by 1.2233 cents a litre, so any cut in a 1.2233-cent-wide window reproduces the found set
  exactly; 7 of 15 data-free cuts on that one column file the call and all seven printed bins at a maximum absolute
  difference of 0.0000 percentage points, three of them plain outlier reflexes (median plus three MAD, median plus 1.5
  interquartile ranges, mean plus two standard deviations). The same seven land it on the shipped bundle read through
  `generator/verify.py`. The decisive step is arithmetic, so no magnitude repairs it.
- The signal dial (Tallis's excess pass-through) as the way to widen the separation: one-ended, both ends read, at
  exA10 (no call, the golden finds nothing, 0 of 13 agree, 0 of 5 crude routes land it), exA15 (gap -0.348, 2 of 13
  agree, 0 of 5 crude routes land it), exA20 (gap 0.225, 9 of 13 agree, 1 of 5 crude routes land it), exA25 (gap
  0.720, 12 of 13 agree, 4 of 5 crude routes land it), base (gap 1.223, 12 of 13 agree, 4 of 5 crude routes land it),
  exA40 (gap 2.225, 13 of 13 agree, 4 of 5 crude routes land it), exA50 (gap 3.223, 13 of 13 agree, 4 of 5 crude
  routes land it), exA60 (gap 4.225, 13 of 13 agree, 4 of 5 crude routes land it). No setting has the step both needed
  and determinate.
- The cycle-amplitude dial as the way to widen it: the same one-ended curve from the other side, at ampB050 (gap
  2.120, 13 of 13 agree, 4 of 5 crude routes land it), ampB075 (gap 1.687, 13 of 13 agree, 4 of 5 crude routes land
  it), base (gap 1.223, 12 of 13 agree, 4 of 5 crude routes land it), ampB150 (gap 0.357, 9 of 13 agree, 1 of 5 crude
  routes land it), ampB200 (gap -0.578, 5 of 13 agree, 0 of 5 crude routes land it).
- The phase-spread dial (how far the coastal areas' cycle phase at the change sits above Tallis's four towns'), which
  is the only axis that moves the default path at all: one-ended too, at phC040 (gap 2.050, 13 of 13 agree, 4 of 5
  crude routes land it), phC070 (gap 1.544, 12 of 13 agree, 4 of 5 crude routes land it), base (gap 1.223, 12 of 13
  agree, 4 of 5 crude routes land it), phC130 (gap 0.970, 10 of 13 agree, 4 of 5 crude routes land it), phC160 (gap
  0.972, 10 of 13 agree, 3 of 5 crude routes land it), and it fails three ways as it widens. Compressed to 0.40 the
  default path itself files Tallis (Harbourline no longer leads: Tallis first at 30.4 per cent, lead 3.17 times), so
  the ladder inverts. Widened to 1.30 and 1.60 the default path's own lead over Pellow falls to 1.14 and 1.13 times,
  under the 1.15 times floor, while the licensed family drops to 10 of 13 and 4 of 5 then 3 of 5 crude routes still
  land the golden.
- Tuning any of the three dials to find a cell where the separation is wide and the licensed family still unanimous:
  there is no such cell, and the reason is algebraic rather than a matter of search. The decisive step is the choice
  of the scale a one-dimensional unit statistic is read against, so the licensed constructions differ only in the
  location and spread they divide that statistic by. They agree on the found set exactly when no admissible scale
  reorders the units, which is exactly when one sort on the statistic is the answer. Measured over 16 settings,
  Spearman corr(crude routes landing the golden, licensed constructions agreeing) = +0.8837.
- The default path's own separation as the thing to widen, which is what this build's resume line ordered: the
  within-window route is insensitive to the signal dial (Harbourline 88.5 per cent, lead 1.27 times over Pellow,
  Tallis seventh of seven at 40.2 per cent at every excess from 1.0 to 5.0 cents a litre), so nothing on that axis
  moves a reader's crossing.
- The readability screen's reflex row on the decisive rung, accepted at the first stage 2: measured on an incomplete
  enumeration. The row lists t-tests, robust errors, rank tests and stratifying by brand or area, every one of them a
  within-window test, and omits two reflexes that each file the golden's exact printed answer: the cross-section's own
  robust spread, which is the Hidiroglou-Berthelot move this note's `## Draw` names as official statistics' anomaly
  detection, and the default path's own Welch test run after the town's daily mean margin is removed (30 stations
  found, Tallis 31.5 per cent, printed bins 30 and six zeros, the golden's bins exactly). Removing the town mean is
  the first control anyone reaches for against town-level cycles; `checks.py` tested the area-relative margin only
  against the placebo null, never against the within-window test.
- **(2026-10-25, measured) THE ONE BUILD IN THIS LANE WHOSE CALL HELD.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **Harbourline Fuels** against the golden **Tallis Petroleum**, and filed 195 of 369 stations found against the golden 28, with every brand's share wrong (HBL 90 per cent against a golden 0, TAL 40 against 30). It ran a one-sided Welch t-test of daily margins after against before and Benjamini Hochberg at 5 per cent across all 369 stations pooled, and read "more than the levy rise" as a margin increase above zero because the margin already subtracts the levy. It took **34 of 59 ask figures, 57.6 per cent**. With both top responses missing the call the pair sits at about 12 plus 55 times the ask keep, so this build measures at about **43.7 and already clears the 50 bar**; at the asks' own spec it sits near 23. So this is the one FAILED_TO_STUMP number the measurement does not condemn: its repair is `/fix-rubric` on the ask layer with the call frozen, not a re-root.
- **(2026-10-25, /fix-rubric pass 1) The pack narrated two of ask V's four elements, and that sentence is removed.** The shipped `extract_notes_2026-11-16.md` carried "In the survey, reference_month is the month a return reports and processing_month the run that processed it; a later revision of a return replaces the earlier one", which hands over both of ask V's hazards in one line and is `supplemental-stumping` ban 1, nothing narrates a device. It is cut. The convention still converges without it, because a `revision` column beside `reference_month` and `processing_month` admits one sensible reading, so no fork opens. The remaining three notes lines (the UTC and DST rule, the price-stands rule, the 8 June renumbering) serve the main call and stay. Rebuild clean: 1,289 assertions, `verify` agreeing on an independent recomputation, `figures_check` 51, `voice-check` PASS, `leak.py` REVIEW with no new line, and `freeze.py check --mode rubric` PASS with the main call, the stump and every frozen figure unchanged. It moves no graded figure by design, so `freeze.py` warns that nothing on the ask side moved: correct, since the repair makes the ask harder to reach rather than changing its answer, and the test is a re-read.
- **(2026-10-25, measured) Where ask V's 21 of 21 came from, and what is still owed.** The leak is ask V alone: asks C and P held at 0 of 14 together (the shares and found-counts ride the missed call, and the priced-by-brand counts held outright), while ask V's litres went 21 of 21. Four candidate replacements for its D7 primary were worked and refused, each for a stated reason: a dealership-grain return needing an allocation weight (no exact remedy, and allocation is not determinate); a multi-site dealership whose second station is off the frame (an unmatched join, which the hygiene battery runs); a four-weekly trading period against the calendar month (the apportionment is a method choice, so the ask stops being determinate); and a rejected-revision device evidenced by a control total (a control that ties only under the golden is ban 3, an oracle). **The one that survives screening is the sample-grossing device:** a monthly fuel sales survey is a stratified sample, the frame carries a stratum rather than a weight, and the stratum populations sit in the published bulletin, so the grossing factor has to be reconstructed as population over sample count before any figure appears. Its remedy is multi-purpose under readability test 7 (a bulletin states its coverage and a frame records its strata for reasons entirely their own), no hygiene sweep asks whether a file is a census, and it moves all 21 figures per brand and month. It needs the ask's wording loosened from "the fuel sales survey's litres" to "the litres", keeping all 21 figures, the unit and the rounding, because as worded the raw reported sum is the defensible reading and the ask must stay determinate.
- **(2026-10-25, measured) Rubric pass 1 is measured INEFFECTIVE, and that is the useful result.** A fresh blind reader on the de-narrated pack scored **34 of 59, 57.6 per cent, identical to the first run**, with the call missed again on the same default-path shares. It found the primary unaided: it listed all eight reissued references by number (FS-17107, 22715, 33539, 38736, 41398, 42271, 42751, 47901), matched returns on `site_address` rather than `survey_reference`, and gave its own reason, that the references were reissued and the reporting name is the operator rather than the brand. It also handled the revisions (about 70 pairs in the quarter), the 1 February Pellow to Oxbury move at KEL-0158 and KEL-0170, and 58104's 16 March closure counted in full. So the narration was never what handed ask V over, and the real defect is structural: **noticing that eight references each serve two stations is the same act as deciding to join on the address, because the address is the only other identifier on the row.** Discovery and remedy collapse, and the hygiene battery does the discovering. Filed as `supplemental-stumping` 1.0. The narration stays cut, since it was ban 1 regardless, but pass 2 must replace the primary and the sample-grossing device is the one that separates discovery from remedy: learning that the frame is a sample does not tell you the grossing factor, which has to be rebuilt as stratum population over sampled count before any figure appears.
- **(2026-10-25) The sample-grossing device is refused on determinism, and pass 2 stops here.** Worked through before any code: if the frame is a stratified sample carrying a stratum, with the stratum populations published in the bulletin so the factor is rebuilt as population over sampled count, then two estimators are both defensible on the shipped pack and give different answers. A Horvitz-Thompson grossing weights each sampled return by its own stratum's factor and sums by brand; a post-stratified grossing takes the mean litres of each brand's sampled stations within a stratum and multiplies by the count of all that brand's stations in it, **which the register supplies, because the register lists every station and its brand**. The ask would then not be determinate, which the asks must be whatever else they may turn on, and it is `stumping` 1.1c (the grouping dichotomy) reappearing inside the ask layer: the remedy is a choice among estimators, so the data either separate them, making the choice a reflex, or they do not, making the ask forked. Closing it by construction needs single-brand strata, which is a degenerate design. **The general lesson, worth more than the device: a remedy that is an ESTIMATOR cannot satisfy 1.0 and stay determinate at the same time; the remedy has to be a RECONSTRUCTION, a definition applied to records with one correct form**, which is what the lane's two lowest-leaking ask layers both are (a weekly profile fitted to interval-censored windows under its own fixed point, and a per-regulation delay attribution over flights that operated). The one reconstruction-shaped candidate left for this ask, the returns reporting year-to-date rather than monthly litres so the month is a difference of consecutive returns, with the work sitting in a missing month, a revision and a reference handed over mid-series, is recorded here for a later pass and not built now: it rewrites every litres value in the file, and this build already measures a pair near 43.7, under the 50 bar, with every gate green and its pack reproducing. Pass 1's cut stands, because the narration was ban 1 regardless.
- (2026-11-01, Batch 3 re-root) Architecture 1, the fuel price pass-through monitor, re-rooted at the queue reset with no
  portal result: its decisive step was a one-dimensional outlier scale (measured above), and the world is closed under
  one architecture per world.
- (2026-11-01, draw) An emergency-department surveillance baseline aligned on each area's school return, the field's
  Farrington baseline taken on calendar weeks: the WHAT cannot file the expected count without naming the school clock
  (rule application) or leaving it to "comparable weeks" (a fork), so the decisive step sits in the comparison, which
  is WHAT.
- (2026-11-01, draw) Interviewer falsification found through informative back-check non-response: fabricated interviews
  are wrong records, so catching them is a planted defect (task125's ruling), and the estimator for the unreachable
  share is a model of the verification.
- (2026-11-01, draw) Signals passed at danger per approach at red, the red approaches rebuilt from consecutive trains'
  headways: the exposure built from one unit meeting another's presence is task181 architecture 4's insight by the
  abstraction test, and the opportunity population would have to be filed (WHAT).
- (2026-11-01, draw) Resistance prevalence under cascade susceptibility testing (the second-line drug tested only on
  isolates resistant to the first): the decisive step settles the denominator (WHAT), and the plainest count over all
  isolates lands the golden, an inverted ladder.
- (2026-11-01, draw) The probe card at gap population with pattern E: `test.same_puzzle_older` and
  `test.same_driver_older` against twelve builds; and population with G10, G6, G14 or G2 decisive: `test.same_driver`
  inside the batch. Redrawn to gap time with G10 decisive, the honest reading of a structure carried by each officer's
  own history.
- (2026-11-01, prototype) A library of 600 objects with competent officers from 0.87: the masked full-time officers'
  raw rates sat below every recertified officer's (an interval at the bottom of the sort, the shock test failing) and a
  competent casual officer came within one point of the line; the library cut to 360 objects, the memory multiplier to
  0.12, competent officers raised to 0.89 and the deficient new hires made casual.
- (2026-11-01, build) Bags drawn for lane slots with nobody rostered on: a lane with no officer is not screening, and the
  counts sat outside the roster's hours; unstaffed slots now count nothing.
- (2026-11-01, build) Performance-test images timed from the lane's scheduled opening: on days a lane's first block was
  short the test fell inside rostered time; the test now runs before the first rostered start.
- (2026-11-01, build) An edge-distance assertion on the lane-quarter bag counts: exact counts with one licensed handling
  have no edge to clear; replaced by convergence assertions (every passenger bag inside rostered time, every test hour
  before it).
- (2026-11-01, build) Officers named from the Faker en_AU stream on the build seed: the surface screen blocked three of the
  names the goldens print (a first name and two surnames used in recent builds); the officers now take names drawn with
  `guard.py names`, frozen in params.py.
- (2026-11-01, build) The drawn names assigned in pool order: all ten officers coming off carried women's first names, a
  pattern with no cause in the world that a reader would ask about; assignment now runs through a seeded permutation.
