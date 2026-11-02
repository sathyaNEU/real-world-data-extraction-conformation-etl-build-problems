# task238 design note

Architecture 2, drawn 2026-11-02 at the Batch 3 queue reset. Architecture 1 (the Halvreth Wellbeing Tracker's
mode-mix monitor band, Survey Research & Official Statistics) shipped 2026-10-17 with no portal result and is
re-rooted under the Batch 3 instruction; its world is closed and its record sits below as `## Architecture 1 record`.
This architecture is a new client domain, a new world, a new dataset, a new generator and a new shell: General
Statistics & Data Science / missing-data-censoring-measurement-error under Data Quality Monitoring & Alerting, in a
Nova Scotia grocery chain's price integrity monitoring.

## Draw

- **Card:** `cards/task238.json`, architecture v2, registered 2026-11-02T02:05Z at PASS (NOTE only: test.same_driver_older
  differentiated against task268 v3 and task453 v2, both lines on the card), checked again on the registered card at
  the end of the draw after sibling builders filed task159, task204, task449, task466 and task185: PASS.
- **Pairing:** General Statistics & Data Science / `missing-data-censoring-measurement-error`, which serves Data
  Quality Monitoring & Alerting. The object is the health of the chain's published price data (the price each shelf
  shows against the price each register charges), and the call is the monitoring decision the standard sets: which
  stores go on Price Watch, the intensified monitoring regime, for the first quarter of 2027.
- **World:** Saltmarsh Market Limited, a fictional fourteen-store Nova Scotia grocery chain (seven stores in the
  Halifax price zone, seven in Zone 2), its POS host, its pricing team, its shelf-edge label printer fleet, its Price
  Integrity team (weekly random audits off Thursdays, Thursday changeover checks), its service desks. Weekly flyers run
  Thursday to Wednesday; price changes take effect at 00:00 Thursday. Five stores have an overnight crew that prints
  and hangs the changeover labels on the Wednesday night; nine print the batch on the Thursday after opening. People
  drawn with `guard.py names --geo CA --locale en_CA --seed 238`: Melanie Donaldson (Director of Price Integrity,
  issues the list), Kimberly Welch (pricing analyst, the movement report), Brian Allison (store systems, the printer
  fleet). None appears in the prompt. As-of date of the fiction: 15 January 2027 (every export pulled 12 January).
- **The call:** whether any store goes on Price Watch for Q1 2027, and which, at what Q4 2026 price accuracy. Golden:
  Spryfield (102) 98.4%, Lower Sackville (107) 98.6%, Antigonish (203) 98.3%, Bridgewater (205) 98.7% and Yarmouth
  (206) 97.8%; Cole Harbour (106) the nearest store to stay off at 99.4%. The call faces forward (the Q1 2027 regime)
  and is measured on the closed quarter the standard fixes (PI-2 s.4.1), the retrospective measurement being the
  standard's own design.
- **Shape:** 10, a scorecard: every store's accuracy against the 99.0 line. Criteria: 14 store verdicts + 5 Price
  Watch accuracies + the nearest store off (2) + 14 Scanner Code payouts + 14 flyer-week counts + 14 flyer-week
  dollars + the chart's parts (dots per store, the 99.0 line labelled, Price Watch stores distinguished, the finding
  title, axis units: 5) + 2 files = 70.
- **Strategy:** population_selection with G6 decisive (the scans' composition over each changeover Thursday differs
  from the audits'), G7 (the label window each store's own printer job pins) and G14 (the audited rate does not carry to
  the scans); Gate G method_or_model_selection (the estimator of the label state at the scans); calibration
  physical_verification (the audits and checks are physical label checks); context artifact operations_log; layer 2
  family estimation_fit, pattern own:use-weighted-state-from-spot-checks. Redrawn at the draw: composition_mix (the
  reviewer's other honest key for the same move) is banned against task142 in the window, and monitoring_export
  against task484; population_selection names the same move as the substitution of the audit program's population of
  label-moments for the standard's population of scan-moments (the card's gap carries population), operations_log
  names the printer fleet log the decisive window is read from.
- **Forum, event, organisation:** operations_desk (the Director of Price Integrity issues the list under PI-2 s.4.2),
  period_close (the quarter's close), retailer_or_ecommerce. Shell: question form whether, second sentence opened by
  the deliverable ("I want ..."), rounding sentence opened by the verb ("Show accuracies as percentages ...": the first
  wording, "Accuracies are per cents ...", shared a construction with task470, task233 and task301), deliverables
  xlsx+svg; architecture 1's shell was what, xlsx+png.
- **Deliverables:** `price_watch_2027q1.xlsx` (the Price Watch call for every store with each Price Watch store's
  accuracy, the Scanner Code payouts by store, the flyer misses by week) and `price_accuracy_q4_2026.svg` (a dot chart
  of every store's accuracy against the 99.0 line).
- **Data-native sentence:** a grocery chain's shelf labels are paper, so the price a shelf shows at the moment of a
  scan is recorded nowhere: the Price Integrity team sees a label only when it checks one, the weekly random audits run
  on days with no changeover, and every Thursday each store's changed items carry last week's label from opening
  until the store prints its changeover batch (the printer fleet logs the moment) and hangs it, while flyer-day
  shoppers buy those very items in those hours.
- **Abstraction sentence (against task281 v3, the nearest approved build in kind, and task229 v2, task249 arch5):** this
  build weights a state observed only at spot checks by the moments the uses happen, inside a window each unit's own
  operating log opens; task281 carries a validated rate by a latent device mix the validation corpus over-holds, task229
  reads states seen just before a reset, task249 arch5 calibrates on samples timed by when samplers reach the site. No
  sentence fits this build and any of them: here the spot checks are random in time, and the rate is right where it was
  measured; what moves is which moments the standard counts.
- **Candidates written before the choice** (each dropped one has its line in `## Tried and rejected`):
  1. (taken) the scan-weighted shelf-label accuracy of a grocery chain's stores, the random audit's match rate at rung 0,
     the label window read from each store's own changeover print job.
  2. A seismic network's magnitude of completeness under daytime noise and station outages: spent by task180 v4.
  3. A data platform's staggered feed migration, each migrated feed's loss read against not-yet-migrated feeds the
     migration itself relieved: retaggable as Experiment & Causal, and task273's shared-store interference driver.
  4. A plant's gauge repeatability against production variation: the decisive step settles the comparison population.
  5. A sensor fleet's data capture over each asset's running hours: one join once the run log is in the pack.
  6. A contact file's decay by time since last verification: task132's renewal clock.
  7. A utility's estimated interval reads and billing demand peaks: the imputed-extremes family of task245 and task247.
  8. A weighbridge network calibrated from paired loads: task251's paired-stream driver.
  9. A drift monitor's population stability index biased at small segments: statistical rigor alone (Gate G illegal).
  10. Crusher carryover in an assay laboratory read from blanks after high-grade samples: a process recoverable only
      from residuals (task255's lesson).
- **Screens before the draw:** `guard.py recent`, `coverage`, `mechanisms --objective data-quality-monitoring`, `slots`
  on the mechanism nouns (spot check, changeover, stale, weighting, audit, label, print) and the setting nouns
  (grocery, shelf, flyer, scanner, price integrity, planogram): no build on file carries a shelf-label accuracy, a
  changeover window or a scan-weighted spot check; task463 (CPI shelf prices) and task115 (a grocery deal mechanic) share
  setting nouns only.
- **Sources** (what each teaches; how this build differs): the Retail Council of Canada's Scanner Price Accuracy
  Voluntary Code (the customer remedy filed in PI-2 s.5.1; here the ask on payouts); NIST Handbook 130 price
  verification (an inspector checks a random sample of items, the field's measure of price accuracy, here rung 0 and
  never shipped); retail pricing-integrity practice (weekly changeover batches, overnight against day crews); the
  missing-data frame (a state observed at sampled moments, missing at random only given the time since the store's
  changeover print).

## Survivor anatomy

- **Actor:** the deciding property, the label state at the moment of each scan, has no column in any file: the hourly
  report holds scans by store and hour, the movement report each changed item's Thursday units, the printer log each
  job's local time and label count, the checks and audits a label and a register price at the moment of a check; the
  state at a scan is a relation between a scan's hour, its store's batch time and the hanging pace.
- **Link:** the signal is read through an as-of relation no key offers: the changeover date in the movement report to
  the store's PCB job in the printer fleet log (device name to store through the directory, the job named by its
  changeover date), the job's time against each hour of that Thursday's scans, the pace from the Thursday checks' time
  since that same job; nothing in the standard or any file invites the join.
- **Reflex:** the field's measure of price accuracy, the share of randomly checked labels that match the register (the
  integrity team's weekly audit, the inspectors' method), sits at rung 0 and files no store (every store at 99.9% or
  more); adding the Thursday checks or carrying their old-label share to the changed items' scans (rungs 1 and 2) files
  six or seven stores.
- **Back-test:** the textbook route validates: the weekly audits agree quarter-long with near-perfect labels at every
  store (the stray share they show, 0.02%, is the same at every store within noise), and the overnight-crew stores'
  Thursday checks never find an old label, so the audit's picture of clean shelves holds wherever anyone looks at
  random.
- **Second use:** every file the decisive step reads ships for its own reason: the hourly report is the POS host's
  standard export, the movement report the pricing team's price-change impact report, the printer fleet log the store
  systems team's job record (it also carries tag replacements, new-item labels, aisle strips and test pages), the
  checks and audits the integrity team's own programs; delete the decisive step and every file still has its job.
- **Shock:** the five stores the step puts on read as ordinary on every shipped statistic: their audit accuracy is
  99.95% to 100.0%, their payouts and contacts sit inside the day-crew stores' spread, and no sort of the mean print
  hour, the checks' old-label share, the audit accuracy, the store's scans or its changed-item units puts the five
  together (asserted, shock.not_an_interval).
- **Pins:** PI-2 files the WHAT in the chain's own genre (s.3.1 the scans, the label at the moment of the scan; s.2.1
  item scans; s.2.4 when price changes take effect; s.2.5 the quarter by local time; s.4.1 the 99.0 line); no filed
  sentence names a changeover batch, a printer, a hanging pace, a check or an audit, and deleting any filed sentence only
  unfixes the population, the window or the line, never the step.

## Default path

1. Read PI-2: a store whose price accuracy for the quarter is below 99.0 per cent goes on Price Watch (s.4.1), price
   accuracy being the share of its item scans that rang up at the price on the item's shelf-edge label (s.3.1).
2. Estimate each store's price accuracy the field's way, from the Price Integrity team's weekly random audit
   (price_audit_results_2026Q4.csv): the share of audited labels whose shelf price matched the register price.
3. Apply s.4.1.

Ends on: no store on Price Watch (every store's audited accuracy 99.9% or more).

Golden: Spryfield, Lower Sackville, Antigonish, Bridgewater and Yarmouth on Price Watch (98.4, 98.6, 98.3, 98.7 and
97.8 per cent), Cole Harbour nearest above at 99.4.

## Stump sentence

A competent analyst reads each store's price accuracy off the weekly random price audit and files no store on Price
Watch (Ends on: every store at 99.9% or more); the step that lands it there is taking the audited labels for the scans,
when each Thursday's changed items carry last week's label from opening until the store prints and hangs its
changeover batch and the Thursday scans crowd into those hours, which puts Spryfield, Lower Sackville, Antigonish,
Bridgewater and Yarmouth below 99.0 per cent.

## Three rules

- **Task type:** general-statistics-data-science / missing-data-censoring-measurement-error, which serves Data Quality
  Monitoring & Alerting: the label state at each scan is missing data observed only at sampled moments, and the call is
  the monitoring regime the standard sets for each store.
- **Domain test:** the call turns on each store's share of scans that met a label showing another price, a state
  missing at every scan and observed only at the audit and check moments, which the missing-data analyst estimates as
  missing at random given the time since the store's own changeover print, with the hanging pace read from current
  status checks; swapping that estimate for the audited share changes the call.
- **Swap:** "which hospitals go on watch, judged on the share of doses given while the ward's drug chart showed a dose
  the pharmacy had changed" keeps the arithmetic but has no weekly changeover batch, no printed label hung at a pace,
  and no flyer-day crowd buying the changed items in the stale hours, so the step that moves five stores has nothing to
  act on.
- **Layer 1:** (1) the printer fleet log in local time with its UTC offset, the offset changing at the 1 November DST
  change (printer fleet console); (2) three namings of a store, POS number, audit name and printer device (POS host,
  handheld, fleet console); (3) audit and check EANs at 13 digits against 12-digit UPCs elsewhere (handheld); (4)
  designated retail closing days and two early-close Thursdays, absent or short in the hourly report (POS host); (5)
  jammed changeover jobs, voided and reprinted minutes later (printer); (6) the December check sheet with one more
  column than October's and November's (handheld export); (7) the weekly price change release as a Monday preliminary
  and a Tuesday revision (pricing; the flyer ask); (8) service desk receipt numbers typed three ways and register
  overrides in cents and UTC (service desk app, POS host; the payout ask). Nothing is placed to be caught; items 1 to 6
  leave the call and every printed figure where they were (asserted R2.1 to R2.7 and SF12), items 7 and 8 sit only in
  the asks' rows.
- **Layer 2:** estimation that fits the data (missing data and current-status censoring): the audited share treats the
  unobserved label states at the scans as missing completely at random; they are missing at random only given the time
  since each store's changeover print, and the scans are not spread like the audits over that time.
- **Decisive step:** reconstructing, for every changeover Thursday at every store, the window from opening until that
  store's own label batch printed and went up (its printer job's local time and label count, the pace the checks show),
  and counting the store's changed-item scans by their hour against that window, instead of carrying any rate read from
  labels checked at other moments.
- **Not semantics:** every field, code and unit read correctly (the three store namings, the EAN padding, the local
  offsets, the closing days, the voided jobs, s.2.1 to s.2.5) still leaves the label state at the scans in no column; on
  the clean truth the audit route files no store (R3a) and only the window reconstruction files the five (R3b).
- **Not rule application:** no filed rule names a batch, a printer, a pace or a weighting (R3c: the standard's text
  carries none of those words); executing s.3.1 and s.4.1 on the audits, on the audits with the checks, on the checks'
  share carried to the changed items' scans or on a chain-wide old-label curve by clock hour files none, seven, six and
  none. Enumerated family: those four plus the window reconstruction under every hanging treatment, hour mix, stray
  basis and pace (SF1 to SF6): from no store to seven. Standing family once the data rule out the others (the checks
  after the print show labels going up over about half an hour, not at once nor all at the end; the hourly report holds
  each Thursday's own hours; a store's own pace rests on three check visits at most): every member files the same five
  stores and the same printed accuracies, the tightest printed figure 0.04 inside its bin; the ruling-out is loud only
  for a reader who opens the printer log beside the checks (checks before the print 98% old, after the batch 0.2%).
- **Analyst test:** a strong analyst who cleans every file, reads PI-2 correctly and estimates each store's price
  accuracy from the weekly random price audit puts no store on Price Watch, every store at 99.9% or more, against the
  golden's five stores below 99.0% rebuilt from each changeover's window and the store's own Thursday scans.
- **Estimand:** PI-2 rev. 3 (PI-2_price_integrity_standard_rev3.pdf) s.3.1, 2.1, 2.4, 2.5 and 4.1: the population is
  the item scans at the store's registers in Q4 2026 by local date, the outcome whether each rang up at the price on the
  item's shelf-edge label at the moment of the scan (above or below counts), the unit per cent, the comparison below
  99.0 per cent for Price Watch the following quarter.
- **No decoy:** nothing is planted: no memo, draft, briefing or stakeholder figure argues a call; the audits and checks
  are the integrity team's real programs reporting what they saw; no block of records is copied, withheld or swapped;
  the contacts log and the markdown tags are declared distractors.
- **No certified replay:** no published or certified accuracy exists in the pack to reproduce; the method is not
  recovered by matching a shipped figure, and no shipped file ranks the stores on accuracy.
- **Lesson:** a quality rate is only as good as the moments it was measured at; when the standard counts uses, the
  state must be rebuilt at the moments of use, and the operating log that opens each window is the record of it. No
  build on file weights a spot-checked state by the moments of use inside windows a unit's own job log opens.

## Readability screen

| Rung | What the reader does | Test that could fire | Verdict |
|---|---|---|---|
| 0 random audit match rate | takes matched labels over labels checked at each store | the field's measure (reflex), test 3 | readable |
| 1 audits and Thursday checks pooled | adds the changeover checks to the labels checked | the hygiene battery's "use every record", test 5 | readable |
| 2 checks' old-label share on the changed items' scans | carries each store's Thursday old-label share to its changed items' Thursday units | a natural weighting once the checks are read, test 3 | readable |
| 3 chain-wide old-label curve by clock hour | bins every check by Thursday hour and applies it to each store's hourly scans | needs the hour idea; no column, no sentence | readable |
| 4 each store's own window from its printer job (decisive) | rebuilds every changeover's window from the store's PCB job time, label count and the checks' pace, against that Thursday's scans by hour | no column, no key, no filed sentence names the batch or the pace; no sort of any shipped statistic gives the five | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | how a batch's labels go up | over the minutes after the print, at the pace the checks show | all at the print; all at the batch's end | same call | same call; the checks before the print are 98% old and after the batch 0.2% |
| SF2 | the moment inside an hour | scans spread evenly through each hour | all at mid-hour | same call and figures | same call |
| SF3 | the hours of a changeover's scans | that Thursday's own hourly scans | the quarter's average Thursday; even trading hours | same call (figures move up to 0.07 under the average) | PI-2 s.3.1 "at the moment of the scan"; the hourly report holds that Thursday's hours |
| SF4 | the stray-label share | pooled over the chain's audits | each store's own audits | same call and figures | same call |
| SF5 | the hanging pace | one pace for the chain | each store's own pace | same call | same call; no store has more than three check visits inside its hanging |
| SF6 | the pace's own precision | the checks' estimate, 9.2 labels a minute | 15 per cent slower or faster | same call and figures | same call |
| SF7 | below 99.0 | compared unrounded | compared at one decimal | same call | same call; no store within 0.05 of the line |
| SF8 | a scan below the label price | not accurate | counted as accurate | other figures | PI-2 s.3.1 "above or below the label price was not accurate" |
| SF9 | the quarter | local date and time | UTC | same call | PI-2 s.2.5; every main-call file is local |
| SF10 | item scans | the POS host's item-scan count | every line rung, weighed and keyed included | other figures | PI-2 s.2.1 |
| SF11 | when a changed price takes effect | 00:00 Thursday | from the label's hanging | other call | PI-2 s.2.4 |
| SF12 | a jammed batch | the completed reprint's time | the voided job's time | same call and figures | same call |
| SF13 | the stray share's labels | every audited label | changed items' labels set aside | same call and figures | same call; the audits never run on a Thursday |
| SF14 | a printed accuracy | the unrounded estimate rounded once to one decimal | rounded from a rounded intermediate | same call and figures | the prompt's rounding sentence |

## Ladder

| Rung | Route | Price Watch stores |
|---|---|---|
| 0 | weekly random audit match rate (every store 99.9% or more) | none |
| 1 | audits and Thursday checks pooled | 102, 106, 107, 203, 205, 206, 207 |
| 2 | the checks' old-label share carried to each store's changed-item Thursday units | 102, 106, 107, 203, 205, 206 |
| 3 | a chain-wide old-label curve by Thursday clock hour on each store's hourly scans | none |
| golden | each store's own changeover window from its printer job and the checks' pace, on that Thursday's scans by hour | 102, 107, 203, 205, 206 |

Pricing on the clean truth: the true accuracies put the same five below the line and the golden estimate sits within
0.12 of the truth at every store (R3 assertions). Margins: every store at least 0.30 from the line (Bridgewater 98.694,
the tightest below; Cole Harbour 99.391, the tightest above); every standing variant keeps the set (SF1 to SF6) and the
printed accuracies (bins asserted, the tightest edge 0.04). Each lower rung differs from the golden at one store or
more (rung 2 by Cole Harbour, rung 1 by Cole Harbour and Amherst, rungs 0 and 3 by all five). The decisive move is
worth the whole set (no store to five); the late-printer heuristic (mean print after 10:30) files rung 2's six.

## Closure table

| Axis | Name | Reading here | Move |
|---|---|---|---|
| 1 | Population | item scans at the store's registers in Q4 2026 | filed, PI-2 s.2.1 and s.3.1 |
| 2 | Unit of account | the item scan | filed, s.2.1 |
| 3 | Attribution window | 1 October to 31 December 2026, local | filed, s.2.5 (SF9) |
| 4 | As-of dating | each scan's label at the moment of the scan | filed s.3.1; the window from the job's local time (SF12) |
| 5 | Version basis | the hourly report and movement report as pulled 12 January | C1: no revisions in the main files |
| 6 | Denominator | every item scan in the quarter | filed, s.3.1 |
| 7 | Weighting | each changeover's scans by that Thursday's own hours | C1 across even and mid-hour readings (SF2); SF3 |
| 8 | Window length | each changeover from opening to the batch up | C1 across hanging treatments (SF1) |
| 9 | Boundary inclusivity | below 99.0 goes on | filed, s.4.1; C1 (SF7) |
| 10 | Rounding path | compare unrounded, print one decimal | C1 (SF7, SF14) |
| 11 | Tie-break | none needed | C1: no store within 0.05 |
| 12 | Maturity and censoring | none: the quarter is closed and pulled | not applicable |
| 13 | Order of operations | window first, then weighting, then the stray share | C1: the stray share adds under either order |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | a jammed batch counts once, at its reprint | C1 (SF12) |
| 16 | Identity normalisation | three store namings, EAN against UPC | C1: one-to-one directory (R2.4), padding inert (R2.3) |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | per cents, scans, labels a minute | stated in the prompt and files |
| 19 | Code and status semantics | COMPLETED and VOIDED jobs, MATCH and MISMATCH | C1 (SF12) |
| 20 | Integerisation | scans are whole; accuracies continuous | C1 |
| 21 | Clause scope | s.3.1 per store per quarter, s.4.1 per store | filed |
| 22 | Forward window contents | Q1 2027 Price Watch from Q4 2026 accuracy | filed, s.4.1 and s.4.2 |

## Literal reader

Executing PI-2 word for word: s.3.1 asks for the label at the moment of each scan, which no file holds; the literal
reader must estimate it, and the audits (labels checked on days with no changeover) do not describe the scans' moments,
so the audit route is non-compliant on a literal reading (it measures labels at audit moments, not scans). Every
reading the text leaves open is listed in the fork table and either converges (SF1 to SF7, SF12, SF13) or violates a
quoted sentence (SF8 to SF11, SF14); executed literally with the window reconstruction, every licensed reading files the
five stores and the printed accuracies.

## Oracles

None ties only under the golden. The audits confirm clean shelves at every store under every reading (they never meet a
changeover); the Thursday checks confirm that labels go up after each store's print under every reading of the pace; the
service desk payouts and the customer contacts rank nothing and are not on the main call's path.

## Ask sheet

Two asks, 42 figures, both decoupled from the call (H18: qualifiers of the price integrity picture, the cost of the
stores' price errors to customers and the head office keying record), both sited on files the main call never reads
(the register override export, the service desk adjustments, the ad plan, the price change releases, the price
corrections, the flyer item daily units). The separation line holds by construction: the main call reads the hourly
report, the movement report, the printer fleet log, the checks, the audits and the directory, and none of the asks'
device rows sits in those files; the flyer keying errors make the label and the register agree (both printed from the
same release), so they move no main-call figure.

**Ask A, the Scanner Code payouts (14 figures, each store's dollars paid out in the quarter, nearest dollar).** Use: the
director's statement of what the stores' price errors cost under the Code. Files: pos_price_overrides_2026Q4.csv (9
columns), service_desk_adjustments_Q4_2026.xlsx (7 columns, three monthly sheets), the directory. Primary device (D1, a
reconstruction left after noticing): a supervisor who approves a register payout also logs it in the desk app, on a
receipt number typed three ways, so the same payout sits in both systems with no shared key; and a cashier who only
takes the line back to the shelf price leaves the rest of the Code remedy to the desk on the same receipt line, which is
a second payout. The repair needs a judgment the battery does not make (which records are one event): a desk entry on
a receipt line the register also paid is a duplicate only when it repeats that payout's amount. Hazards: the override
export in UTC with 30 September evening payouts inside its window (D8; a UTC-date reading moves 6 stores), the payout
as the original less the override price in cents (D3; the override price read as the payout moves 10), reason codes
(PM, MD, DM, MGR beside SC). Stops: adding both logs (misses 10 stores), dropping every desk entry that matches a register
line (misses 10), desk only (10), register only (14). Realism: a supervisor's approval log and a two-stage remedy are
how service desks run the Code. Pin test: the asking sentence pins the basis (paid out under the Code), the window (in
the quarter) and the unit (dollars); the device sits in which records are one payout, which no pin names.

**Ask B, the flyer price misses (28 figures, for each of the 14 flyer weeks that started in the quarter, the advertised
UPCs that rang up off the flyer price and the dollars customers paid above it that week, nearest dollar).** Use: the
head office keying record beside the shelf record. Files: flyer_ad_plan_wk40-wk53_2026.csv (5 columns),
weekly_price_change_releases_2026Q4.xlsx (9 columns, PRELIM and REVISED sheets), price_corrections_2026Q4.csv (7
columns), flyer_item_daily_units_2026Q4.csv (5 columns). Primary devices: an assorted flyer line lists only its lead
UPC, and its other varieties are found among the week's AD START items by the lead's abbreviated brand, product and size
(D7/D6: the true key elsewhere; matching on the lead's keyed price, the natural shortcut, drops exactly the mis-keyed
varieties: misses 10 weeks; the lead only misses 13); a mid-week correction fixes a register price from its own opening
date, so the overcharge runs only to the day before (D2 dated: the release price all week misses 14 weeks' dollars,
the correction taken for the whole week misses 14 weeks' counts and dollars). Hazards: the Monday preliminary against
the Tuesday revision (13 weeks' counts, 14 weeks' dollars), a multi-buy compared per unit (1 count, 10 dollar figures),
each zone's own units (13 dollar figures). Realism: a promotions ad plan keys an assorted line to its lead item, and a pricing desk corrects a
keying error mid-week with correction labels sent the night before. Pin test: the asking sentence pins the week (each
flyer week that started in the quarter, its seven days), the set (advertised UPCs), the comparison (the flyer price)
and the unit; the devices sit in which UPCs an assorted line covers and which days a register price was in force,
which no pin names. Unit price: a multi-buy's unit price taken exactly or to the cent gives every week the same
count and dollars (a three-for price is a whole number of dollars a unit; asserted askB.unit_price_to_the_cent_same_figures).

Main population zero counts: no device row in the hourly report, the movement report, the printer fleet log, the checks
or the audits (asserted: the main call reads no ask file, sep.main_call_reads_no_ask_file). Hazard table: UTC (ask A, 6
stores), cents (ask A, 10), preliminary release (ask B, 13 weeks' counts, 14 weeks' dollars), multi-buy (ask B, 1 count
and 10 dollar figures), zone units (ask B, 13 dollar figures). Referee: none; every repair is forced by an internal inconsistency (a receipt line paid
twice for the same amount; a variety in the week's AD START items sharing the lead's brand, product and size; a
correction dated inside the week).

| Ask | Figures | Cracker's route (call landed, battery run, every filed rule executed) | Cracker hits | Verdict |
|---|---|---|---|---|
| A payouts | 14 | both logs, UTC converted, SC only, original less override, every desk entry on a register-paid receipt line dropped | 4 of 14 | miss |
| B counts | 14 | revised release, per unit, zones, the corrections file applied as the latest version, varieties by the lead's keyed price | 0 of 14 | miss |
| B dollars | 14 | as above | 0 of 14 | miss |

The full includer (every device noticed and handled: amount-aware de-duplication, varieties by brand, product and size,
corrections from their own dates) keeps the whole ask layer; its pair against the mirror is 59.2, under 60 but with
little margin, which is the open risk this sheet carries (supplemental-stumping rule 2: no third device on a disjoint
block was found that it would miss without a fork).

Pair ceiling: 34.3 (cracker on the call 50.2, mirror off the call 18.4; 38 + 7 + 55)
Mirror leakage: 11.9 per cent of ask weight (the mirror adds both payout logs, reads each flyer line's lead UPC, keeps the release price all week)
Measured by: generator/ceiling.py on the cut pack (target/ of the final build, sha256 over its files 942540ae)

## Pre-ship check

- The 10/10 rules re-read against the built pack: the decisive step (each changeover's window from the store's own
  printer job against that Thursday's scans) is analysis no sentence performs; every Layer 1 item is neutral on the
  call (R2 assertions); no file is planted.
- Free gates on the final cut: generator checks, verify, two byte-identical builds, figures_check.py, precut.py,
  voice-check.py, leak.py, guard.py heart and surface (results in pipeline.json and the hand-back).

## Leak sweep

leak.py --asof 2027-01-15 on the final cut: REVIEW, no LEAK (sweep 2's one LEAK, the standard's "rung up" in s.2.1, was
reworded in docs.py to "sold"). Each REVIEW line, ruled:

- PI-2 standard, 4 stump terms (thursday, effect, weekly, report): harmless. They come from s.2.3 (the flyer week),
  s.2.4 (price changes take effect at the registers at 00:00 on the Thursday that opens the flyer week) and s.6.1, the
  standard's own calendar, which the flyer price ask also needs; the standard says nothing of labels being printed,
  hung or checked, and no sentence relates a changeover to the accuracy.
- price_audit_results_2026Q4.csv, 8 of 11 candidates beside numbers: harmless. One row per label checked (shelf price,
  register price, result), never a store figure; the audit route is the analyst's own computation (rung 0), not a
  shipped ranking.
- service_desk_adjustments_Q4_2026.xlsx: harmless. One row per desk adjustment on a receipt line, ask A's file; it ranks
  nothing and the main call does not read it.
- store_directory_2027-01.xlsx: harmless. Store number, name, zone, address and hours; no measure of accuracy.
- thursday_changeover_checks_Q4-2026.xlsx: harmless. One row per check visit (time, labels checked, labels still at the
  old price), raw spot checks; no store figure or ranking.

## Tried and rejected

- A mode change read across rotation groups (the newest groups moved to web first, a difference in differences
  against time in sample): too close to task453's rotating-panel measurement change and to task236's attribution.
- A parallel run of both modes on split samples: calibration form parallel_run_overlap is banned against task464.
- A censored laboratory panel for the quality alert: the defensible estimators for left-censored data spread across
  the bands, so the call forks.
- A sensor errors-in-variables calibration: the regulator's own method is ordinary least squares, which forks
  against an orthogonal regression.
- A paired-difference standard error for the alert: too close to task228's driver (variance at the randomised unit).
- Each index pooled, flagged or given a new series on the same mode effects: the guard's same-puzzle test blocked it
  inside the batch (task465 v1's gap, pattern and decision type), and a three-way band per member repeats task236's
  and task237's output; the decision is cut as the monitor's band instead.
- The seed's own pitfall (ordinal items, polychoric invariance testing across modes): psychometric invariance is
  task237's pairing, banned against the last three builds, and the estimator choice reads as a convention fork.
- Architecture 1 as shipped (the Halvreth Wellbeing Tracker's mode-mix monitor band, each index's mode effect read
  through the contact strategy test's randomly allocated letters): re-rooted 2026-11-01 at the Batch 3 queue reset;
  shipped 2026-10-17 with no portal result, its world closed under one architecture per world.
- 2026-11-02, architecture 2 draw, a seismic network's magnitude of completeness under daytime noise and station
  outages: spent by task180 v4 (small earthquakes lost to daytime noise), found by `slots`.
- 2026-11-02, a data platform's staggered feed migration read against not-yet-migrated feeds the migration relieved:
  retaggable as Experiment & Causal Analysis, and task273's shared-store interference driver.
- 2026-11-02, a plant's gauge repeatability against production variation: the decisive step settles the comparison
  population (the WHAT screen).
- 2026-11-02, a sensor fleet's data capture over each asset's running hours: one join once the run log ships (the
  task304 lesson, assembly).
- 2026-11-02, a contact file's decay by time since last verification: task132's renewal clock.
- 2026-11-02, a utility's estimated interval reads and billing demand peaks: task245's and task247's imputed-extremes
  family.
- 2026-11-02, a weighbridge network calibrated from paired loads: task251's paired-stream driver.
- 2026-11-02, a drift monitor's population stability index biased at small segments: statistical rigor alone, Gate G
  illegal.
- 2026-11-02, crusher carryover read from blanks after high-grade samples: a process recoverable only from residuals
  (task255's lesson, a hidden rule).
- 2026-11-02, price integrity with a changeover-completion log that timestamps each hung label: the state at every scan
  becomes one join, the literal execution of s.3.1 (assembly, task304's lesson); the build reads the batch's print time
  and estimates the hanging from the checks instead.
- 2026-11-02, the stray-label share taken from every audit mismatch while audits ran on Thursdays too: the changeover
  labels the audits met moved the printed accuracies by 0.05 (the double count crossed a one-decimal bin); the audits
  were moved off Thursdays, the integrity team's changeover check day.
- 2026-11-02, a printer fleet log in UTC: a misread clock moved the call by hours (R2 not neutral); the log carries
  local time with its offset, and the UTC clock sits only on the payout ask's register export.
- 2026-11-02, a two-crew hanging pace of about four labels a minute: the ramp carried a third of the exposure and the
  per-store pace variant forked the printed figures; the crews hang about nine a minute, so the window is set by the
  print time and the pace barely moves a figure.
- 2026-11-02, grading every store's accuracy: the stray-label basis (pooled or each store's own audits) forks the
  night stores and Amherst at one decimal; the prompt asks for the Price Watch stores' accuracies only, which every
  standing estimator prints alike.
- 2026-11-02, an assortment whose varieties, sizes and prices came from one list for every product (diapers in beef,
  garbage bags in dark roast, hummus in 12 x 355 mL cans at 99 cents): a realism tell any reader quotes; each family is
  now dressed by catalogue.py on its own stream (a brand's product in one of its real sizes, that product's own
  varieties, a price from the product's level), and the master stream is untouched, so the call did not move.
- 2026-11-02, three-for flyer prices at any whole-dollar total (3 for $10): one unit rings at a third of a cent, and
  taking the unit price to the cent moved one week's dollars across a bin; a three-for price now carries a whole-dollar
  unit and its keying errors move in steps of three cents.
- 2026-11-02, service desk refunds placed by adding hours to the scan: a third landed overnight (00:15, 23:57) when no
  desk is open; each desk entry now falls in desk hours, an overnight one the next morning.

## Architecture 1 record (re-rooted 2026-11-01 at the Batch 3 queue reset)

Shipped 2026-10-17 (judge APPROVE r2, no portal result); the mode-mix monitor world is closed. Kept as written then, its headings demoted.

Architecture 1, wave 3, seed DQ11 (whether a new survey mode's data can be pooled into the tracker): the seed's world
and quantity only, the pitfall re-found from the data under the 10/10 rules. Survey Research & Official Statistics,
nonresponse, calibration and measurement-error adjustment, Data Quality Monitoring & Alerting. The Halvreth Statistics
Office runs the Halvreth Wellbeing Tracker, a quarterly household survey of one adult per sampled address, collected
telephone-first since 2019 (an advance letter, interviewer calls, a web link in the reminder for households the calls
do not reach). From the fourth quarter of 2027 every sampled address gets a web-first letter instead (complete online,
telephone follow-up for households that have not). Before choosing, the office ran a contact strategy test through
the second and third quarters of 2027: each quarter's issued addresses were allocated at random to the web-first
letter (A) or the telephone-first letter (B), to compare response and cost per complete under the two designs. Once
the tracker is web-first, each quarter's indexes pool online and telephone completes, and an index whose answers
differ by mode moves whenever the quarter's share of completes made online moves. The office's continuity standard
for the web-first tracker sets a mode-mix monitor: when a quarter's web share departs from the reference share by
more than the monitor's band, that quarter's indexes are recalibrated to the reference mix before release. The band
is the widest whole-point departure that moves no headline index by more than its continuity tolerance. The head of
survey methodology sets it before the fourth-quarter estimates are processed.

### Draw

Card `cards/task238.json` (architecture 1, registered 2026-10-17). Guard verdict WARN: overuse.objective (the
objective in 4 of the last 12 builds) is this lane's own objective, the backlog wave being Data Quality Monitoring &
Alerting by assignment.

- **Pairing.** Survey Research & Official Statistics / nonresponse-calibration-measurement-error-adjustment, serving
  Data Quality Monitoring & Alerting. Not banned against the last three builds (task237, task155, task464). The object
  is the health of the tracker's published series through a change of collection mode (whether a quarter's mode mix
  has moved its indexes), the call a monitoring setting.
- **Niche.** Mode effects in a mixed-mode household survey: an interviewer's presence moves self-reports (heavy
  drinking and loneliness reported less, volunteering and life satisfaction more), and who completes online is
  self-selected on traits the same questions measure, some of which no field records.
- **The call.** The band, in whole percentage points of the web share, at which the mode-mix monitor runs from the
  fourth quarter of 2027.
- **Shape.** 04, setting one dial: the allowed settings are the whole-point bands, and each headline index's mode
  effect and widest band within tolerance stand behind the setting. Decision dial_setting, answer rate_or_share,
  question form what.
- **Strategy.** causal_design with G14 decisive (the telephone completes' level is not what the web completes would
  have answered by telephone), G16 (the estimator the random letter allocation entitles) and G6 (the two answerer
  groups' mix) supporting; Gate G decomposition_attribution (the web-telephone difference split into the mode's
  measurement effect and who chose the web); calibration none; context artifact close_out_summary (the test's
  close-out); layer 2 family estimand_identification, pattern own:mode-effect-through-a-randomized-contact-strategy.
- **Forum, event, organisation.** line_manager_or_team (the head of survey methodology sets the band under MS-14
  section 5, no formal forum), cutover_or_migration (the tracker's move to web-first collection),
  research_or_statistics_office. Guard WARN repeat.gate_g (decomposition_attribution against task266, a demography
  build): the mechanism there splits a life-course quantity, here a web-telephone difference into the mode's
  measurement and who chose the web; nothing else repeats.
- **People** (`guard.py names --geo en_NZ --seed 238`): Tania Nicholas, head of survey methodology, who sets the band;
  Bernard Johnstone, the tracker's fieldwork manager, who wrote the test's close-out; Leonard McMurray, data
  processing lead, who keeps the exports.
- **Deliverables.** `mwt_mode_mix_band_2027q4.xlsx` (the band, each index's mode effect and widest band within
  tolerance, and the asks' figures) and `mwt_mode_mix_band_2027q4.png` (each index's widest band against the band
  set).
- **As-of.** 2027-10-20: the test's fieldwork closed 30 September 2027, the close-out is dated 15 October 2027, the
  fourth-quarter fieldwork is under way and its estimates are processed in January 2028.
- **Data-native sentence.** Households choose their mode (under letter A they complete online if they get round to
  it before the follow-up calls, under letter B online only if the calls never reach them), and the households that
  end up online are younger and more often away from home, which is also what moves their answers on drinking,
  loneliness and volunteering; the one contrast in this dataset that no choice shapes is the one between the two
  letters, allocated at random by address, and it moved the web share by only about sixty points.

Sources, one line each (what it teaches; how this build differs):
- Survey methodology on mixed-mode designs (selection effects against measurement effects; the interviewer's presence
  and social desirability; recalibrating to a fixed mode mix to keep a series comparable): the field's frame for the
  quantity and the monitor; here the effect must be read through a contact strategy test run for response and cost,
  not a mode experiment built for it.
- Causal inference on encouragement designs (the Wald estimator, two-stage least squares with the assignment as the
  instrument): the method the design entitles; here it is never named in the pack, and the respondent comparison
  adjusted for every recorded characteristic is the reflex it has to beat.
- Seed DQ11: the world (a tracker adding a mode) and the quantity (each index's mode effect) only; its pitfall
  (ordinal items and polychoric invariance testing) belongs to psychometrics, which task237 holds.
- Spent on this objective (`guard.py mechanisms`): task229 (a convex conversion of a daily mean), task231 (a rate over
  active units with late exits), task232 (transmission from delayed mixed outcomes), task230 (a late channel's net
  classification bias), task228 (variance at the randomised unit), task233 (a missing-not-at-random departure on the
  logit scale), task234 (a source's output from a share a loss cannot move), task235 (a missing event censored until
  its device's next contact), task236 (a capture share against an independent fixed-protocol sample), task237 (the
  trait's share of a score with a wording factor). None reads a channel's effect through a randomized nudge's shift
  in uptake.

### Default path

1. Read the continuity standard: each headline index's mode effect (the difference answering online rather than by
   telephone makes to a household's answers), the mode-mix artefact of a departure (the departure times the mode
   effect), each index's tolerance and the band's rule (the widest whole-point departure keeping every index within
   tolerance).
2. Build the test's completes from the interview export under the test plan's rules (one complete per address,
   partials and late returns out) and score the twelve indexes as the codebook defines them.
3. Estimate each index's mode effect by comparing web with telephone completes, adjusted for age, sex, education,
   region, household size, tenure and employment (a regression with a web indicator).
4. Divide each index's tolerance by its mode effect, take the smallest widest band and round it down to whole points.

Ends on: 3 points (safe after dark binding at 3.42, its comparison carrying who chose the web; heavy drinking 3.67 next).

Golden: 4 points (heavy drinking binding at 4.53 points of web share, from each index's difference between the letters
divided by the letters' difference in the share of completes made online; two-stage least squares 4.62).

### Stump sentence

A competent analyst estimates each index's mode effect by comparing web with telephone completes adjusted for every
recorded characteristic and sets the monitor at 3 points (Ends on: 3 points, safe after dark binding); the step that
lands it there is reading the mode effect off households that chose their mode, when the randomly allocated letters
give a contrast that, divided by the letters' difference in web uptake, sets the band at 4.

### Three rules

- **Task type:** survey-research-official-statistics / nonresponse-calibration-measurement-error-adjustment, which
  serves Data Quality Monitoring & Alerting; the object is whether a quarter's mode mix has moved the tracker's
  published indexes, and the call is the monitor's setting.
- **Domain test:** the quantity that decides is each headline index's mode effect, the measurement difference
  between answering online and by telephone for the same households, which survey methodology separates from the
  selection effect of who answers online; here the field reads it from the randomized contact strategy contrast
  through the shift it causes in web uptake.
- **Swap:** with ward admissions or megawatt-hours for answers there is no interviewer whose presence moves a
  self-report, no household choosing its mode, no contact letter allocated at random to read the effect through and
  no mode mix to monitor on a published series; the call stops making sense.
- **Layer 1:** an issued-sample file at address grain and an interview export at record grain, joined by address;
  telephone interviews stamped in local time by the CATI system against web submissions stamped in UTC by the survey
  platform; web submissions after a quarter's fieldwork close kept in the export; households interviewed by telephone
  after they had already submitted online, or the reverse; web break-offs with answers to the early items only; item
  nonresponse codes that differ by mode. Each is how the system that writes it behaves; none is placed to be caught.
- **Layer 2:** estimand_identification: the mode effect identified from the random letter allocation (an
  encouragement design) rather than from the self-selected mode groups, however adjusted.
- **Decisive step:** dividing each index's difference between the two letters' completes by the letters' difference
  in the share of completes made online (the Wald estimator, or two-stage least squares with the letter as the
  instrument), rather than comparing web with telephone completes or taking the letters' difference as the effect.
- **Not semantics:** reading every field, code, timestamp and definition right (completes built under the plan's
  rules, the indexes scored per the codebook, the standard's definition of the mode effect read as written) still
  leaves the analyst comparing web with telephone completes, and that comparison, computed correctly and adjusted for
  every recorded characteristic, files 3 points.
- **Not rule application:** the standard files what the mode effect is, the artefact, the tolerances and the band's
  rule; no rule names an estimator or a comparison group, and executing every stated rule still leaves the
  estimation, where the adjusted comparison files 3 points and the letters' difference 6.
- **Analyst test:** a strong analyst who builds the test's completes under the plan's rules, scores each index as the
  codebook defines it, reads the continuity standard correctly and estimates each mode effect from web against
  telephone completes adjusted for every recorded characteristic files a band of 3 points (Ends on: 3 points, safe
  after dark binding); one who takes the two letters' difference as the mode effect files 6.
- **Estimand:** the continuity standard MS-14 (`mso_ms14_tracker_continuity_standard.pdf`) fixes the population (the contact
  strategy test's completes, both quarters and both letters), the outcome (each headline index as the codebook scores
  it), the window (the second and third quarters of 2027), the unit (index points; the band in whole percentage points
  of the web share) and the comparison (the same households answering online rather than by telephone).
- **No decoy:** nothing is planted: the close-out summary reports fieldwork, response and cost by letter and never a
  mode effect or a band; no memo, draft or briefing argues a band; the published series are the tracker's own
  releases.
- **No certified replay:** no certified or published mode effect or band exists for a method to reproduce.
- **Lesson:** when respondents choose the mode, a contact strategy allocated at random for another purpose is the
  lever: the mode effect is the arms' difference over the arms' difference in uptake, not the comparison of the
  modes' respondents however adjusted, and not the arms' raw difference; no build on file reads an effect through a
  randomized nudge's shift in uptake (task236 reads capture against an independent sentinel sample, task228 the
  variance at the randomised unit).

### Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0a web completes against telephone completes, as they stand: 2 (heavy drinking 2.57) | MS-14's "mode effect" read as the difference between the modes | the mode is a property of every complete | yes, the first comparison anyone runs | none | no | one subtraction per index | readable |
| 0 (default) the same comparison with every recorded characteristic held fixed (a regression with a web indicator): 3 (safe after dark 3.42) | MS-14's definition, the same households online and by telephone, invites holding them alike | age, sex, qualification, employment, tenure, household size and region ship on every complete | yes: adds the controls, reweights | none | no | one regression per index | readable |
| 1 letter A's online completes against letter B's telephone completes: 3 (heavy drinking 3.11) | the plan's two strategies, web-first and telephone-first | the letter joins from the issued sample | partly: a design-minded analyst compares the strategies' typical modes | none | no | one subtraction per index | readable |
| 2 the letters' raw difference (each index under letter A less under letter B): 6 (heavy drinking 6.82) | the plan's random allocation sends a design-minded analyst to the arms | the letter column | yes for an experimenter: compare the randomised arms | none | no | one subtraction per index | readable |
| 3 (decisive) each index's difference between the letters divided by the letters' difference in the share of completes made online (the Wald estimator; two-stage least squares with the letter as the instrument) | no sentence names an estimator, an instrument or uptake; MS-14 files the quantity (every household online against every household by telephone) and the plan files why the letters exist (response and cost) | no column holds a mode effect, an uptake or a band; the mode and the letter are separate facts in separate files | no: the reflexes hold covariates fixed or compare the arms; scaling a contrast by the shift it caused in the mode is neither | no control scores an estimator; the close-out gives uptake only in rounded words | no | not linear: two differences per index from record-level files, then a ratio, then the tolerances | silent |

### Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | mode effect | the index with every household in the measured population answering online, against every one of them by telephone | the difference between the web and the telephone completes | 2 | MS-14 s.3 ("every household in the population it is measured on answered online ... every one of those households answered by telephone") |
| SF2 | web share | the percentage of a quarter's completes made online | the share of issued addresses answering online (uptake per address) | 2 | MS-14 s.3 ("the percentage of a quarter's completes made online"); the effect's population is the completes |
| SF3 | the band | the widest whole-point band within every tolerance | the nearest whole point (5) | 5 breaches heavy drinking's tolerance | MS-14 s.5 ("the widest whole-point band at which ... stays within"); asserted |
| SF4 | the mode effect the band uses | the central estimate | a confidence bound | another band | MS-14 s.5 ("taken at the central estimate of its mode effect") |
| SF5 | the population the effects are measured on | the test's completes, both quarters and both letters | one quarter alone | same call (each quarter alone 4: 4.68 and 4.40) | MS-14 s.5 ("both quarters and under both letters"); same call (asserted) |
| SF6 | a complete | CST-27 s.5: section 6 reached by the close, coded C, an address once at its first-submitted complete, an address's highest result | late returns, partials, both records, the sample system's codes | same call (R2) | CST-27 s.5; same call (asserted) |
| SF7 | each index's score | codebook v9, sheet Indexes | none filed | same call | codebook (asserted) |
| SF8 | an index's base | answers on the scale | don't know, refused and prefer not to say kept in the base | same call | codebook Indexes note; same call (asserted) |
| SF9 | tolerance units | points on the 0 to 10 scores, percentage points on the percentages | none | same call | MS-14 Table 2 |
| SF10 | the artefact | d/100 times the mode effect, d in points of web share | d times the mode effect | a band a hundredth the size | MS-14 s.3 ("d/100 times the index's mode effect") |
| SF11 | controls in the estimator | none (the Wald estimator) | the recorded characteristics (two-stage least squares) | same call (4.53 and 4.62) | same call (asserted) |
| SF12 | the reference share | the fourth quarter's web share | the test's letter A share | the band does not use it | MS-14 s.3, s.5 |
| SF13 | the 9 to 12 August staff-entry returns | telephone interviews | web returns | same call | close-out; same call (asserted) |
| SF14 | a return giving an age under 18 | not the selected adult's: not a complete | a complete | same call | CST-27 s.3 ("aged 18 or over"); same call (asserted) |
| SF15 | the 345 addresses answering twice | one complete each, the first submitted | a within-household comparison of their two answers | 2 | CST-27 s.5 ("An address counts once"); MS-14 s.5 measures the effects on the test's completes, not on 345 households answering a second time |

### Ladder

Four rungs and a floor, each a defensible way to read a mode effect, each dying to one fact of the data (figures on
the cut pack, asserted in `checks.py`; the binding index and its widest band in points of web share).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0a | web against telephone completes, as they stand | 2 (heavy drinking 2.57; its effect 11.66 points) | the web completes are younger, more educated and more often employed: the recorded characteristics alone move every index |
| 0 (default) | the same with every recorded characteristic held fixed | 3 (safe after dark 3.42, effect 8.77; heavy drinking 3.67 next) | the letters moved web uptake by 66.3 points and moved safe after dark by -0.53: no index can carry a mode effect of 8.77 points and shift half a point the other way when two thirds of households change mode; the comparison carries who chose the web |
| 1 | letter A's online completes against letter B's telephone completes | 3 (heavy drinking 3.11) | the same: each arm's typical mode is still chosen within the arm |
| 2 | the letters' raw difference | 6 (heavy drinking 6.82; its difference 4.40) | the letters changed the mode for 66.3 per cent of completes, not all: the difference carries each effect only for the households a letter moved |
| 3 (golden) | each difference between the letters over the letters' difference in the share made online | 4 (heavy drinking 4.53, effect 6.62; volunteering 6.83 next); two-stage least squares 4 (4.62, 6.49) | |

- **Margins.** Heavy drinking's widest band sits 0.53 inside 4 to 5 under the Wald estimator and 0.38 under two-stage
  least squares; under every Layer 1 mishandling it stays between 4.40 and 4.83 (R2). The rivals sit inside their own
  bins: the adjusted comparison's 3.42, the letters' raw difference 6.82, the raw comparison 2.57.
- **Position and dominance.** Every easy route files 2, 3 or 6; only reading the effect through the letters lands 4,
  and the decisive step alone (the letters' contrast scaled by uptake, nothing else changed) moves the default path
  there on the clean truth (R3b). The generating model's own effects set 4 on heavy drinking.
- **Grid.** The corrections walk 2, 3, 6; only the decisive step reverses (6 to 4), so the golden is bracketed.
- **Worth.** Counted on the band, the one graded call; the binding index changes with the rung (safe after dark on the
  default path), so the default path misses the binding index too.

### Closure table

| # | Axis | Reading in this build | Closure |
|---|---|---|---|
| 1 | Population | the CST-27 completes, both quarters, both letters | MS-14 s.5; CST-27 s.5 (SF5, SF6) |
| 2 | Unit of account | the selected adult's answers; each index in its own units | codebook; MS-14 s.3 |
| 3 | Attribution window | the second and third quarters of 2027, to each quarter's close | CST-27 s.4 |
| 4 | As-of dating | exports of 11 October 2027; the band set before the fourth quarter is processed | dictionary; README; MS-14 s.5 |
| 5 | Version basis | MS-14 issued 8 October 2027; codebook version 9; the plan of 8 March 2027 | headers |
| 6 | Denominator | each index's valid answers; response rates over eligible addresses | codebook; CST-27 s.5 |
| 7 | Weighting | none: no weight ships with the test | data |
| 8 | Window length | two quarters | MS-14 s.5 |
| 9 | Boundary inclusivity | within tolerance means no more than it; the band the widest whole point within | MS-14 s.5 (SF3) |
| 10 | Rounding path | the band from unrounded effects; response rates rounded to one decimal once | MS-14 s.5; prompt |
| 11 | Tie-break | none: the narrowest widest band binds, no tie | asserted |
| 12 | Maturity and censoring | returns after a close do not count; both quarters closed | CST-27 s.5 |
| 13 | Order of operations | completes, letters, scores, effects, widest bands, band | MS-14 s.3, s.5 |
| 14 | Row order | irrelevant | C1 |
| 15 | Duplicate resolution | an address once, its first-submitted complete in Halvreth time | CST-27 s.5 (SF15) |
| 16 | Identity normalisation | web returns to addresses by login code, interviews by address | dictionary |
| 17 | Netting against gross | none | data |
| 18 | Dimensional units | index points; web share and band in percentage points | MS-14 s.3 (SF9, SF10) |
| 19 | Code and status semantics | valid answers per codebook; RESULT C; section 6; outcome codes 4.1 to 4.3 out of eligible | codebook; dictionary (SF8) |
| 20 | Integerisation | the band a whole number of points | MS-14 s.5 |
| 21 | Clause scope | the twelve headline indexes | MS-14 s.2 |
| 22 | Forward window contents | the band governs every release from the fourth quarter of 2027 | MS-14 s.4, s.5 |

### Literal reader

Executed word for word, MS-14 and the prompt fix the candidates (whole-point bands), the population (the CST-27
completes from both quarters and both letters, built under the plan's section 5), the outcome (each headline index as
the codebook scores it), the quantity (each index's mode effect: every one of those households online against every
one by telephone, at its central estimate), the artefact (d/100 times the effect) and the rule (the widest whole-point
band keeping every index within its tolerance). Executed, MS-14 leaves one question to the analysis: how large each
index's mode effect is, which no file states and no household shows, since each answered one way. A comparison of the
web with the telephone completes, however adjusted, answers it with households that chose their mode; the letters
were allocated at random and moved two thirds of completes from telephone to web, so each index's difference between
the letters over that shift is the effect. Every estimator of it (Wald, two-stage least squares, either quarter alone)
sets 4; every reading in the fork table gives 4 or breaks a quoted sentence. The asks execute the plan's section 5
and the codebook; their difficulty is how each system's records come to exist, not the words.

### Oracles

- No control, published figure or certified mode effect ships: nothing states a mode effect, an uptake by index, a
  band or a decision, and no field marks a household's reason for its mode.
- The close-out gives uptake in rounded words (about six in seven online under letter A, one in five under letter B)
  and response in words (much the same); both tie under every handling of every device.
- The published series (a distractor, named in `metadata.json`) is the telephone-first design throughout, its web
  share drifting between 7 and 20 per cent: a regression of an index on that drift is confounded with time and too
  thin to measure an effect, and it ties with no rung.
- The CATI call records (a distractor) carry contact attempts, not answers; their outage gap corroborates the
  close-out and scores nothing.
- The 345 addresses answering twice give a within-household comparison (SF15): 2, ruled out by the plan's one
  complete per address and MS-14's population.

### Ask sheet

Two asks, 28 figures, decoupled from the call: the call reads the letters' contrasts on the completes; the asks read
the issued addresses' outcomes and each index's valid answers by mode, through how each system's records come to
exist.

**Main population:** the call's population is the test's completes; every ask device either sits outside it (late
returns, under-18 returns, the addresses the field team locked, partials, second records) or moves a complete's mode
without moving the band (the outage interviews, the clock on twice-answered addresses). Each stop's handling leaves
the band at 4 with heavy drinking binding (R2): the call is mess-neutral, never pristine.

| Ask | Figures | H18 home | Use | Primary device (family) | Hazards | Path (files, columns) | Stops |
|---|---|---|---|---|---|---|---|
| A: the test's response rate under each letter in each quarter | 4 | the audit trail of the population the call reads: the completes against the addresses issued | MS-14 s.6 files the test's response with the band | D2, the record is the latest accepted, not the latest delivered: the sample system sets 1.1 on any web submission, after the close and from an under-18 respondent alike, but keeps a field team's 4.1 or 4.2 over a household's own later web complete; only a cross-file cut (submission time, age, the address's code) shows each | D8 the close at UTC+13 on 30 September (daylight time from 26 September); the close read on the UTC date; partials; eligibility codes | issued addresses (letter, quarter, final_outcome), web returns (login_code, submitted_utc, last_section, age), CATI interviews (ADDRESS_ID, RESULT, END_TIME), plan s.4 and s.5, dictionary: 5 files, 11 columns | the sample system's 1.1 codes (0.2 to 1.3 high); eligibility on the field codes alone (0.09 low, every cell); completes over field-coded eligibles (0.11 high); under-18 kept (0.07 to 0.38 high); the UTC date (0.04 to 0.30 high); UTC+12 at the third quarter's close (the two third-quarter cells 0.05 to 0.13 high); the answer |
| B: each index's completes with a valid answer, online and by telephone | 24 | a measure every index carries that the call does not turn on | the methods log's evidence table | D1, the same records under two sources: the 9 to 12 August interviews sit in the web platform's export as staff-opened sessions, a column whose other values are help-line link reissues; only the close-out's outage and the dates show they were interviews | D8 the CATI clock in Halvreth time against UTC stamps, decisive on 345 twice-answered addresses (naive 172, UTC+12 all year 51 moved); under-18 returns; late returns; partials; both records kept | web returns (opened_by, submitted_utc, age, Q01 to Q17), CATI interviews (END_TIME, Q01 to Q17), close-out, plan s.5, codebook, dictionary: 6 files, 16 columns | outage as web (every count, 487 to 494 across); CATI clock naive (every count, about 170 across); UTC+12 all year (every count, about 51 across); under-18 kept (online 157 to 164 high); late kept (online 414 to 430 high); the UTC date (online 116 to 120 high); UTC+12 at the close (online 30 to 32 high); both records (online 239 to 250, telephone 91 to 94 high); the answer |

- **Span:** eight files and 20 columns across the asks; the sample system's code device moves all four rates, the
  outage device all 24 counts, the clock device all 24 counts and both third-quarter rates.
- **Shared hazards:** under-18 returns (A every cell, B every online count); the close in Halvreth time (A, B online);
  partials (A none, B online).
- **Realism:** sample management systems overwrite a non-final status on any return and keep a field team's
  ineligibility code; web platforms accept returns past a fieldwork close; push-to-web letters reach whoever opens them;
  a CATI outage sends interviewers to whatever system takes keyed answers; an overnight suppression feed lets a
  household be called the day it completed online.
- **Referee:** none.

| Ask figure | Where the cracker's path goes | Mirror (stops at rung 0) | Cracker (lands the call, runs the battery) |
|---|---|---|---|
| A response rates (4) | builds completes from the exports for the call, then takes eligibility from the sample system's final codes, so the 144 locked addresses leave the denominator with their completes counted or not (every cell 0.09 to 0.11 off); a fixed UTC+12 moves both third-quarter cells; under-18 returns stay unless it screens ages | misses the same way | miss |
| B valid answers (24) | reads the staff-entry returns as the web returns the export calls them (every count off by 487 to 494 across the modes) and orders twice-answered addresses on a fixed offset (about 51 across); under-18 returns stay in its online counts | misses the same way | miss |

- **Cracker keeps:** about a tenth of the ask figures (a cracker handling every device at once). The chart's parts
  sit on the call (the band, the widest bands, the binding index): an eighth of the ask weight if the generated rubric
  files them there.
- Mirror leakage: 13 per cent of ask weight (the chart's frame and band line; the mirror's ask path is the cracker's).
- Pair ceiling: 37.8 (C = 38 + 7 + 55 x 0.21 = 56.7 with the chart's parts kept; S = 5 + 7 + 55 x 0.125 = 18.9; mean
  37.8).

### Pre-ship check

1. Domain: the call stands on each headline index's mode effect, the measurement difference between answering online
   and by telephone for the same households, read through the contact strategy test's random letter allocation (the
   letters' difference over their difference in the share of completes made online); the comparison of web with
   telephone completes, however adjusted, files 3 (safe after dark binding), the letters' raw difference 6. With ward
   admissions or megawatt-hours for answers there is no interviewer whose presence moves a self-report, no household
   choosing its mode and no mode mix on a published series.
2. Two layers: Layer 1 (two systems' exports at different grains and clocks, late returns past each close, under-18
   returns, twice-answered addresses, the outage interviews keyed through the web platform, partials, mode-specific
   item codes, the sample system's own outcome codes) is neutral on the call, each item asserted (R2: the band stays
   4, heavy drinking between 4.40 and 4.83); Layer 2 is the encouragement design, asserted alone to move the default
   path to the golden on the clean truth (R3b).
3. No banned stump decides: nothing is planted (no memo, draft or figure states a mode effect, an uptake by index or a
   band; the close-out's uptake is in rounded words); not semantics (the default path reads every field right and
   files 3 on the clean truth, R3a); not rule application (MS-14 files the quantity, the population, the artefact and
   the band's rule and names no estimator, asserted on its text).
4. Gate G: no shipped artifact ranks the bands or the indexes' mode effects; the two distractors (the call records and
   the published series) carry no answers by mode and letter.
5. Determinism: the list grades the band, the four response rates and the 24 valid-answer counts; the band is 4 under
   the Wald estimator, two-stage least squares, either quarter alone and every Layer 1 mishandling; the components are
   ranges every estimator lands in; every response rate sits 0.022 or more inside its rounding bin; counts are
   integers. Judge pass r1: DETERMINISTIC, FIX_NOW on asks 2 and 3 only (the 18-or-over rule sat in the letters, not
   in plan section 5, and the 164 returns aged 15 to 17 move three rates and the counts); fixed by filing in section 5
   that a return or interview counts only when it comes from the person the letters ask for, and step 1 cites it; Gate
   G method_or_model_selection, analytical_non_defect, no surface read, not a sole data defect; Gate H domain pass,
   layers pass, decisive step analytical; stump power credible (the covariate-adjusted route files 3, the letters' raw
   difference 6). Pass r2 on the fixed pack: DETERMINISTIC, APPROVE, every golden figure reproduced (40,821 completes,
   heavy drinking 6.63 and 4.53, the four rates, all 24 counts); every fork it ran leaves the band at 4 (the close at
   UTC+12 or ignored, staff entries online, CATI start against end time, the age filter after the deduplication); its
   residuals moved no committed answer: the chart's non-binding bars carry no rounding (visual only), two
   twice-answered addresses switch mode on the CATI start time (closed: the dictionary now says END_TIME is when the
   interviewer coded the result), and the 144 field-coded addresses rest on the plan's highest-result rule (filed).
   After r2 the published series' second quarter of 2027 was anchored on the letter B completes it was released from
   (a distractor's values; no graded figure moved).
6. Asks: A is moved in every cell by the sample system's codes (1.1 on any return, a field team's 4.1 or 4.2 kept)
   and the under-18 returns, and in both third-quarter cells by the close at UTC+13; B in every count by the outage
   interviews and by the CATI clock on the twice-answered addresses; no stop moves the band (asserted).
7. Input gates: 12 files in five formats (csv, docx, md, pdf, xlsx), the call records at 204,006 rows and the issued
   addresses at 76,000, two distractors named in metadata.json; 113 generator checks; the verifier (its own completes,
   its own Wald estimate from the PDF's tolerances and the codebook's scoring) green; two builds byte-identical;
   figures_check 58 of 58; containers clean.
8. Duplicate guard: `guard.py heart` WARN (repeat.gate_g against task266, answered in Draw), nearest driver task259 at
   0.10; `guard.py surface` clean; the forum redrawn to line_manager_or_team after task157 (filed earlier the same day)
   reached this checkout.

### Leak check

`leak.py --asof 2027-10-20`: REVIEW, no LEAK (the plan's first file name, `mwt_cst27_test_plan.pdf`, carried the author
word "test" and was renamed `mwt_cst27_plan.pdf`; the web export's `device` became `device_type`). The REVIEW lines:

- MS-14 carries 0.30: heavy drinking's filed tolerance in Table 2, an input every route reads, not an answer.
- MS-14 carries the call's words: it defines the monitor and the band's rule and states no band.
- The dictionary, README, MS-14, close-out and plan carry stump-paragraph words (letters, households, survey, sample,
  close-out, uptake, random): the fiction's own nouns; none names the estimator, an instrument or the uptake ratio.
- `device_type` in the web export: the device the session ran on, a field every web survey platform exports.

Isolated reads (Sonnet, medium, prompt and pack only): pass 1 found no decisive-step sentence, ranking file or answer
figure and judged the call analytical; its one realism finding (the close-out's "For processing" bullets reading as a
list of the cleaning steps) was fixed by retelling the outage as fieldwork history and dropping the bullets the plan
already covers. Pass 2, after the judge's section 5 fix, and pass 3, after the close-out's response and outage lines
were reworded, again found question 1 none and the call analytical; pass 3 read the close-out as "a fieldwork
manager's real, short memo". The outage paragraph stays as the corroborating evidence the staff-entry device needs
(supplemental-stumping law 2); it moves no figure on the call.
