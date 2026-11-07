# task212 design note

**Status: architecture 1, drawn 2026-11-04; stage 2 resumed 2026-11-05 after a container restart, then stage 3; stage 4
round 1 on 2026-11-07 (leak reader CLEAN; judge NOT_DETERMINISTIC on two ask conventions, the main call forced, G and H
passing), both fixed in the generator (SF17, SF18); stage 4 round 2 pending.** Wave 8, Anomaly Detection & Diagnostics. The seed's
world (AD35, a public insurer's prepayment review team) was screened dead at stage 1 and set aside with its
measurements (`## Tried and rejected`); the number moved to another client domain, world and dataset under the same
objective (`CLAUDE.md`, A stuck build is unblocked): General Statistics & Data Science, a Spanish parcel carrier's
outbound cage audits.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task212.json`, registered 2026-11-04 after `guard.py check` (WARN only).
- **Pairing:** `general-statistics-data-science` / `exploratory-data-analysis-distribution-assessment`, which serves
  anomaly detection; the cell holds no live card (task182 and task185 sit there with `architecture_spent`), and
  `guard.py check` on a probe card raised no `three_rules.task_type`, `ban.pairing` or `ban.subdomain`. The other
  client domain's cells were read first: payment claims is the seed's dead world; grid reliability holds four cards
  and its transformer, EV-charging and coincident-peak ground is spent (task164, task117, task402); safety-incident
  and safety-signal sit in the window.
- **World:** Brújula Paquetería, a fictional Spanish parcel carrier with six sortation hubs: Zaragoza (Plaza),
  Ribarroja del Turia (Valencia), Dos Hermanas (Sevilla), San Fernando de Henares (Madrid), El Prat de Llobregat
  (Barcelona) and Basauri (Bilbao). Each night a hub sorts collected parcels into outbound roll cages, one or more per
  delivery depot, filled in scan order through the sorting night (about 21:00 to 04:00 local). The network's quality
  team audits about ten outbound cages per hub per night at the destination depots and records every parcel's
  condition. Four hubs carry a B2B account's heavy cartons in the same outbound cages as e-commerce parcels, because
  they have no heavy-goods chute: Zaragoza's auto-parts cartons come on the last trailer of the night, Ribarroja's
  tile cartons and Basauri's paper cartons (a customer since January 2026) on trailers before the sort opens, Dos
  Hermanas's olive oil and wine cases after midnight. Madrid and El Prat sort cartons to a heavy-goods chute with
  cages of their own.
- **Decision and call:** one sortation engineering survey (the hub engineering team with the sorter maker's
  technician, who inspect and repair merges, transfers, chutes and accumulation lines) is booked for one hub in the
  three weeks before the Black Friday peak. The call: which hub gets it, and how many damaged parcels a week its
  repairs would stop over the peak. Forward facing: the survey acts on the peak weeks, a window not yet open.
- **Objective:** Anomaly Detection & Diagnostics. The alarm is Zaragoza's audited damage rate standing furthest above
  the network's; the deciding analysis diagnoses what drives each hub's excess (the parcels, the load each parcel
  carried in its cage, the hub's own equipment) and what that implies for the one survey slot.
- **Shape 07, grid of cells:** each hub's audited damage and the damage its own equipment caused, by month (six hubs by
  three months), with the call, runner-up, gap and flip, a chart with named parts and the files; arithmetic in
  `## Ask sheet` at stage 2.
- **Strategy:** `composition_mix`, a Simpson's reversal across a constructed stratum (each audited parcel's crush load),
  never a grouping of shipped columns (`stumping` 1.1c). Gate G `method_or_model_selection`, gap `objective` then
  `population`, generators G6 (composition shift) and G3 (record against operation).
- **Furniture read off `guard.py check` on 2026-11-04 (window task210, task211, task403 after task401):** forum
  `executive_team`, forcing event `season_or_peak`, org family `logistics_or_3pl`, role `operations_director`,
  context artifact `capacity_report` (the peak plan; `monitoring_export` was blocked by task211 and redrawn), shape
  07, deliverables PDF case note and workbook (docx plus xlsx warned against task211 and was redrawn). Personas from
  `guard.py names --geo Spain --seed 212`: Julieta Barranco, Marcelo Castrillo, María Vélez.
- **WARN answered:** `repeat.decision` (pick_one_of_n after task211): the call is one survey slot, a pick by nature;
  shape, gap, strategy, Gate G, domain and world all differ from task211.
- **Data-native sentence:** each outbound cage is built in scan order through the night and a hub's heavy cartons enter
  it when their trunk arrives, so the weight sitting on any audited parcel is set by the trunk timetable and lives only
  in the order of the cage's load scans against the DWS weights, never in a column.
- **The abstraction sentence:** "a unit's excess is carried by the load each case takes from the cases placed on top
  of it in its container, an order relation read from the container's load sequence against a separate weight record;
  at equal load the excess sits at the unit that places its heaviest cases first." Not writable against an approved
  build: `guard.py mechanisms --objective anomaly-detection` (36 builds) and `slots` on the mechanism nouns (crush,
  stacked, load order, roll cage, carry-over) and the setting nouns (parcel, hub, sortation, sorter, damage) return no
  order relation inside a container and no parcel world; the nearest driver on file scores 0.09 (task181).
- **The two filters the seed screen asked of the next candidate:** the golden is a records-fixed figure over a per-case
  state rebuilt across two systems (each audited parcel's crush load from the sortation load scans against the DWS
  weights), and the mechanism-naive count rides a different quantity (cartons sharing the cage, unordered, or the
  cage's weight).
- **Sources (every one synthetic, the carrier and its people fictional, the six towns real; 21 files):** the audit
  app's headers and findings (the spine, one line per parcel of an audited cage), each hub's cage build log (the sorter
  control system, UTC: OPEN, LOAD, NOREAD, CLOSE), the DWS induction records (grams, millimetres, local time with
  offset), the shipment lines (sender declared kg), the accounts register (collection arrangement), the hub register,
  the peak plan, the survey programme (the governing document), the outbound cage audit procedure with both damage code
  lists, the 2025 Basauri survey report and the sorter maker's visit log (the two distractors), and for the asks the
  claims case export, the transfer runs, the card gateway's refund settlement report, the tracking history of every
  parcel with a case, the flat-rate terms, the claims note, the sorter historian's event log, the work orders and the
  stoppage standard. No trunk timetable ships: each night's cartons arrive as a block, which the DWS induction times
  and the accounts register's "dedicated trailer" show as an ordinary cause, and nothing states where they sit.
- **Levels, each cited:** carrier damage rates of 1 to 3 per cent of e-commerce parcels, about 3 per cent at holiday
  peaks (ShipMatrix via withanansi.com; alexanderjarvis.com; ajot.com); the generator's audited rate is 1.9 per cent
  overall, 1.1 to 3.2 by hub. Conveyor and sort impacts and drops at transfers are a named damage point in parcel
  sortation (ajot.com, designing e-commerce packaging for high-speed sortation); the equipment effect at Ribarroja is
  an odds ratio of 1.8. Stacking loads in parcel transit are dynamic and are what ISTA 3A's compression with vibration
  simulates for parcels of 70 kg or less (ista.org 3A overview; lso-inc.com); a small single-wall e-commerce box has a
  McKee box compression strength near 200 kg static and a usable stacking load of 40 to 70 kg after the 3 to 5
  distribution safety factor, so the crush response rises steeply around 60 kg on top and a light box under a carton
  batch of 105 to 190 kg takes an odds ratio of about 4.3. Sorter stoppages of 2.4 to 3.8 a night and a third of them
  safety stops, damage claims on 0.03 to 0.05 per cent of parcels sorted.
- **Screening harness:** `generator/screens.py` on the generator itself (world, records, the readers on the record
  tables as cut), 20 redraws (seeds 3000 to 3019), about 160,000 inspected parcels a redraw (six hubs, 66 nights, about
  ten cages a night), observed against expected per hub per 10,000 inspected, the pick and its lead over the runner-up.
  Output kept in scratch `t212/resume/screens20d.json` and, for the BIC sentence, `t212/resume/bic20_twin.json`.
- **Screen 1, levels and the lever against the rivals' estimates:** the golden family names Ribarroja 20 of 20 in
  every member, worst-seed leads: cells within the load stratum at 35 to 95 kg 2.97 to 3.79, load bands 3.61, logistic
  with the 60 kg step 3.78, Poisson 3.77, linear 2.51, carton count above 3.37, heaviest parcel above 3.74, sender
  sector added 3.81, each form without pack interactions 2.21 to 3.39; the true equipment excess names Ribarroja 20 of
  20. The supported family's spread at one seed is 3.0 to 4.9 per 10,000 (median 4.0, about 5 per cent of the figure),
  so the forward figure is graded to the nearest hundred parcels a week.
- **Screen 2, the golden's own method holds the call:** every specification above names Ribarroja 20 of 20; the log of
  the load holds 20 of 20 at a worst-seed lead of 1.37 with interactions and 1.20 without, and the record's own fit
  refutes it (deviance 66 or more above the 60 kg step at equal parameters, every redraw); a 30 kg edge holds the call
  (1.78) and is refuted by the fit too. The programme's lowest-BIC sentence picks a supported load form naming
  Ribarroja in 20 of 20 redraws (the 45, 60 or 80 kg step, once the heaviest parcel above), setting aside the log by 66
  or more, the step with position and cage terms by 41 or more and every rival by 278 or more. At the shipped seed every
  member, the log included, leads by 1.35 or more, the lowest BIC is the 60 kg step, and the forward figure sits in one
  hundred under every supported member (tightest 13.9 per cent of a bin clear).
- **Screen 3, the first look lands wrong:** the raw audited rate names Zaragoza 20 of 20 (lead at least 1.09).
- **Screen 4, the careful readers land wrong, each 20 of 20 on Zaragoza:** (a) field-decomposing (cells of shape,
  weight band, fragility and service) lead 1.29 or more; (b) constructing, position in the cage, cage weight, cartons
  in the cage and their interactions 1.47 or more, position bands 1.16, the top third of each cage alone 1.12; (c)
  per-record, every attribute two shipped files give with sender sector, cage fill and interactions, 1.27; (d)
  mechanism-naming, crush read the naive way as cartons sharing the cage and the cage's weight, 1.47; (d2) crush named
  and each parcel's load read from the scan order but weighed with the sender's declared kg, linear 1.58, as a 60 kg
  step 2.06, in bands 1.49; (e) literal replay of the programme's comparison on the parcels' attributes 1.29. A reader
  who sets Zaragoza aside for a reason other than the load lands Dos Hermanas 20 of 20 (lead 1.34 or more).
- **Screen 5, literal execution:** the filed WHAT (the parcels a hub's own sortation equipment damaged per 10,000
  inspected, measured against the damage the same parcels would suffer across the network) executed on the parcels'
  recorded attributes names Zaragoza 20 of 20; the golden needs each parcel's load in its cage, which no filed
  sentence asks for and no column holds.
- **The coordinator's five review points (2026-11-05), measured:** (1) the d2 reader names crush and orders the cage
  but weighs it with the declared kg: Zaragoza 20 of 20 in three forms; what separates it from the golden is the
  carrier's measured weight, the DWS weight the attribute model already joins, because three business accounts declare
  a flat default of 2.0, 5.0 and 4.0 kg on cartons that weigh 15 to 21 kg, so the declared load never reaches the crush
  range; the golden needs the DWS join for every parcel scanned after an audited one. (2) Every cage's load order is
  one order under first and last LOAD, no-read re-scans and ties (none share a second), every cage is opened and
  closed once; the DWS join is one set under the printed, the normalised and the barcode-and-hub keys; the call and the
  forward figure's hundred hold under each (SF6 to SF9, SF14). (3) The programme files the peak's window and volume as
  WHAT (the plan's weeks 48 to 52) and what the repairs stop (the hub's own equipment damage); the call's lead holds at
  1.2 or more under every member at the shipped seed (the log without interactions at 1.35), and the forward figure's corridor runs over the supported forms
  with the log and the sub-35 kg edges refuted by the fit. (4) Gate G: no shipped file summarises or ranks the hubs;
  the audits ship as records. (5) The asks were redrawn: each counting unit filed as WHAT, four primaries from four
  families each a reconstruction across two systems; the cracker keeps 0 of 24 figures and the worst full includer 6 of 24
  (`## Ask sheet`); Dos Hermanas is the wrong-reason landing 20 of 20. After the stage-4 fix (the flat-rate grain
  filed, the safety system on the controller's clock) the cracker keeps 6 of 24 and the deep cracker 12 (`## Ask sheet`).

## Default path

The field's method at rungs 0 and 1: audited damage per hub, then indirect standardisation (observed against expected
from a pooled model of the parcels' own attributes), cut every way, with the cartons in each cage allowed for.

1. Read the survey programme: the survey goes to the hub whose own sortation equipment damaged the most parcels per
   10,000 inspected in the July to September 2026 routine audits, and its value is the damaged parcels a week its repairs stop
   over the peak.
2. Build the audited parcels: keep the routine audits, drop lines for parcels not found, map hub numbers to names
   and the old damage codes to the new list, convert DWS grams to kilograms, join audits to DWS by barcode and accounts
   to sectors.
3. Raw audited damage per 10,000 parcels by hub: Zaragoza highest by about 1.5 times the network.
4. Standardise: a pooled logistic of damage on weight, size, packaging, service and sender sector; observed minus
   expected per 10,000 by hub puts Zaragoza furthest above, Dos Hermanas second, Ribarroja third.
5. Cut by packaging, weight band, sector, month, auditor and destination depot: Zaragoza's excess holds in every cut.
6. Allow for the heavy cartons that share three hubs' cages (cartons in the cage, cage weight): Zaragoza is still
   furthest above.
7. Book the survey to Zaragoza and size it on Zaragoza's excess times its peak volume.

Ends on: Zaragoza
Golden: Ribarroja del Turia

## Stump sentence

A competent analyst nets the re-audits, joins the audits to the weighing records, standardises each hub's damaged
parcels against the network's rates for parcels of the same weight, size, packaging, service and sender, allows for
the cartons sharing each cage and books the survey to Zaragoza; the step that lands them there is never reading each
parcel's crush load from the weight scanned into its cage after it, which accounts for Zaragoza's excess and leaves
Ribarroja del Turia, whose tile cartons go in first, with the damage the survey can remove.

## Three rules

- Task type: general-statistics-data-science / exploratory-data-analysis-distribution-assessment, which serves anomaly detection in the taxonomy; the anomaly is one hub's audited damage standing out, and the deciding analysis reads it within the structure that generates the damage before naming the hub whose sorter causes it.
- Domain test: the deciding quantity is each hub's sorter damage per 10,000 parcels inspected, a damage rate read within the structure that generates it, which is this task type's own object; the field's estimator for an excess is indirect standardisation, observed against the network's expected rate for like parcels.
- Swap: in General Statistics the swap is of the method: with the pooled or the attribute-standardised rate in place of the rate read within each parcel's load stratum the call moves from Ribarroja del Turia to Zaragoza; with hospital wards for hubs and patients for parcels nothing loads cases on top of other cases in scan order, so the task stops making sense.
- Layer 1: the cage build log in UTC against the audit app and the DWS in Spanish summer time (each hub's sorter control system against the audit app and the DWS); DWS weights in grams and dimensions in millimetres (the DWS); no-reads re-scanned by handheld and parcels scanned twice (the sorter control system); re-weighs at the DWS; the damage code list replaced on 1 August with two depots' handhelds still keying old codes (the audit app); hub numbers in the build log against hub names in the audit app; supervisors' check audits and NOT FOUND lines (the audit app); sender-declared weights as account defaults (the senders' shipment data). Each is produced by its own system, none is placed to be caught, none moves the call (R2 assertions in checks.py).
- Layer 2: estimand_identification, a Simpson's reversal across a constructed stratum: each audited parcel's load, the weight scanned into its cage after it, separates crush in the cage from the sorter's own damage; Zaragoza's excess is crush under the auto-parts cartons its last trailer brings, and Ribarroja's sorter damage hides because its tile cartons go into the cage first.
- Decisive step: rebuilding each audited parcel's load from the parcels scanned into its cage after it, weighed through the DWS records, and comparing the hubs' damage within load strata, which accounts for Zaragoza and Dos Hermanas and leaves Ribarroja's excess as the sorter's.
- Not semantics: every field read correctly (both damage code lists, check audits, NOT FOUND lines, the cage's build date, the DWS grams, the scan clock, the declared weights) still leaves the attribute-standardised excess on Zaragoza; no field, code or flag holds a parcel's load, and the declared weights a reader might weigh it with are account defaults that land Zaragoza too.
- Not rule application: no filed rule names a load, an order or a stratum, and executing the survey programme's comparison on the parcels' attributes files Zaragoza. The enumerated family (raw rate, field cells, attribute logit, per-record logit with sector, cage fill and interactions, position in the cage, cage weight, position bands, top third, unordered cartons in the cage, scan order weighed with declared weights in three forms, and the DWS-weighted order in cells at five edges, bands, steps at five edges, linear, log, carton count above, heaviest parcel above, each with and without pack interactions, Poisson and with sender sector) spreads the call over Zaragoza (eleven members) and Ribarroja (twenty-two); the standing family, the DWS-weighted order in the forms the record's own fit supports, names Ribarroja in every member at 47.6 to 51.7 per 10,000 at the shipped seed; the ruling-out is loud, the no-load model's deviance 860 above the 60 kg step's and the log's 145 above, and the programme's one selection sentence (the lowest BIC stands) chooses among the estimates an analyst builds and names no term: on the parcels' attributes alone it keeps an attribute model and files Zaragoza.
- Analyst test: a strong analyst who reads every field and rule correctly standardises each hub's audited damage on the parcels' weight, size, packaging, fragility and service, cuts it every way, allows for the cartons sharing four hubs' cages and books the survey to Zaragoza, the default path's `Ends on:`.
- Estimand: the survey programme (Network Operations, filed) fixes the population (parcels found in the routine audits of the regional outbound cages built on the sorting nights of 1 July to 30 September 2026), the outcome (the parcels a hub's own sortation equipment damaged), the unit (per 10,000 parcels inspected), the comparison (the damage the same parcels would suffer across the network's six hubs) and the forward value (that rate applied to the hub's planned parcels a week, averaged over peak weeks 48 to 52 of the 2026 peak plan).
- No decoy: nothing is planted to be caught; each business account's cartons arrive on its dedicated trailer at its own hour, no memo, draft, summary or ranking argues for a hub, the audits ship as records and the 2025 survey report records a closed survey at Basauri.
- No certified replay: no certified or published figure is reproduced to recover a method; the 2025 report's before and after rates are Basauri's own audits and every route reads them alike.
- Lesson: read a damage rate within the structure that generates it before naming the unit that causes it, here the weight each parcel carried in its cage, rebuilt from the order of the cage's load scans against the DWS weights; no build on file reads an order relation inside a container.

## Survivor anatomy

- Actor: the deciding property, the weight sitting on an audited parcel in its cage, has no column in any file; the parcel has rows (an audit line, a LOAD scan, a DWS record, a shipment line) and the property is a relation between its LOAD scan and the later LOAD scans of the same cage, weighed through the DWS.
- Link: the signal is read through a comparison no key offers: the order of a cage's LOAD scans set against the DWS weights of the parcels scanned after each audited one; the cage label joins the parcels but nothing orders or weighs them, and no sentence mentions a cage's order or load.
- Reflex: the field's method (indirect standardisation on the parcels' attributes, cut by every field) sits at rungs 0 and 1 and files Zaragoza, lead 1.38 at the shipped seed and 1.37 or more over 20 redraws.
- Back-test: the textbook route validates: the 2025 survey went to Basauri on its standardised excess, a worn transfer plate was replaced and Basauri's audited rate fell; Basauri's cages carried parcels only until its paper account arrived in January 2026, so both routes agree on that closed case.
- Second use: the build log is the audit's load list (the auditor scans against it, and NOT FOUND lines come from it), the DWS records carry the parcels' weights, sizes and shapes for the attribute comparison and for billing, the shipment lines the service and fragility; none ships for the decisive step alone.
- Shock: Ribarroja is third on the raw rate and third on the attribute-standardised excess, never first on any shipped statistic; the movement the step recovers reads as an ordinary middling hub.
- Pins: the survey programme files the population, outcome, unit, comparison, forward value and a selection rule (the lowest BIC stands) in Network Operations' own voice and names no cage order, load, weight on top, scan or stratum; deleting any of its sentences unforces nothing the decisive step rides on.

## Readability screen
| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 raw audited rate (Zaragoza) | fires (the programme's unit) | fires (audit lines) | fires | no | no | fires | no | readable |
| 1 attribute standardisation (Zaragoza) | fires (the comparison) | fires (DWS and shipment-line columns) | fires | no | no | no | no | readable |
| 2 cartons sharing the cage, cage weight, position (Zaragoza) | no | fires (cage label) | fires (crush named the naive way) | no | no | no | no | readable |
| 2b scan order weighed with the declared kg (Zaragoza) | no | fires (declared_kg on the shipment lines) | fires | no | no | no | no | readable |
| 3 each parcel's load from the build log's LOAD order against the DWS weights (decisive, Ribarroja) | no (no sentence names a load, an order or a stratum; the programme's BIC sentence chooses among estimates and names no term) | no (no column holds order, position or load) | no (the reflex for crush is rung 2) | no | no | no | no (the build log ships as the audit's load list, the DWS for the attributes) | silent |

## Semantic fork table
| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | damaged | any damage code, old or new list | crush codes only | same call | the audit procedure (any code records a damaged parcel); same call asserted |
| SF2 | inspected | found in the cage at a routine audit | NOT FOUND lines read as inspected and OK | same call and hundred | the audit procedure (a parcel NOT FOUND has not been inspected); asserted |
| SF3 | which audits | routine audits | routine and check audits | same call and hundred | the audit procedure (check audit lines are not counted as inspections); asserted |
| SF4 | the window | the sorting night printed on the cage label | the audit date | same call and hundred | the programme (a cage belongs to the sorting night printed on its label); asserted |
| SF5 | the comparison pool | the network's six hubs | the other five hubs | same call | the programme (across the network's six hubs); asserted |
| SF6 | a re-scanned parcel's place | its first LOAD | its last LOAD | same call and hundred | asserted |
| SF7 | ties and no-reads | no two parcels share a second; a no-read's handheld LOAD keeps its place | first against last LOAD | one order in every cage | asserted |
| SF8 | a re-weighed parcel's weight | its first DWS weighing | its last, or the mean | same call and hundred | asserted |
| SF9 | the DWS join key | the barcode as printed | normalised; with the hub number | one set | asserted |
| SF10 | the load stratum's edge | 60 kg on top | any edge from 35 to 95 kg | same call and hundred | asserted (a corridor); 20 and 30 kg refuted by the fit |
| SF11 | the forward volume | the mean planned week, weeks 48 to 52 | the five-week total over five | same figure | identical arithmetic, asserted |
| SF12 | the cartons' own damage | inside the hub's damage | light parcels only | same call | asserted |
| SF13 | the specification of the comparison at equal load | cells of shape, weight band, fragility and load | a fitted model with the load in it: sender sector, no pack interactions, Poisson | same call and hundred | asserted; the log of the load refuted by the fit |
| SF14 | a cage split across two trunks | one label, opened and closed once | two physical cages under one label | one load order | asserted (every cage one OPEN, one CLOSE, every LOAD between) |
| SF15 | the quarter's cages | build dates 1 July to 30 September | audits dated in the quarter | same population | asserted (every audited cage's build date in the window) |
| SF16 | the load's form and any added terms | the lowest-BIC estimate: the 60 kg step by packaging | the log of the load (about 640 a week); the step with position, cage weight and carton count added (about 640 a week); no pack terms; sender sector | same call; the graded hundred only under the lowest BIC | the programme (the estimate with the lowest BIC on the quarter's routine audits stands); asserted at the shipped seed (log +145, the step with position and cage terms +100, every rival +446 or more) and over 20 redraws (20 of 20) |
| SF17 | a flat-rate case's grain (ask: damaged parcels with an approved claim) | one case covers every damaged carton of its consignment, each a damaged parcel: the approved amount over the account's rate in the flat-rate terms (1,267 / 888 / 967 / 1,449 / 1,081 / 464) | one damaged parcel a tracking number (1,101 / 772 / 827 / 1,232 / 935 / 411, the stage-4 judge's) | same call; the six counts 53 to 217 apart | CS-FIN 07 section 2, after its first sentence: "A business account on flat-rate terms opens one case for all the damaged cartons of a consignment, under the tracking number of its first carton, and Customer Service approves it at the account's rate for each damaged carton."; asserted: every approved flat-rate amount an exact whole multiple of its rate (671 cases, 1 to 7 cartons), no case before its terms date, no ordinary, reopened or second case on a flat-rate account, the literal reading gives the six counts and the excluded reading the judge's six |
| SF18 | the safety system's times and the end of a spell the PLC lost (ask: stoppages and hours stood) | one clock: a TRIP lands in the PLC STOP's second or the next; a spell whose STOP the log lost runs from its TRIP to the PLC's next RUN, the RUN no STOP precedes; every corrective order keys its minutes inside its logged spell | (ii) earliest stop record to the latest RUN over every source, work orders included; (iii) TRIPs shifted by an offset from the paired stops (mean, median, nearest pair, straight line), each zero to the second; (iv) the raw TRIP times; a lost spell ended at a RESET; the order's minutes in place of the log's | same call; (i) to (iv) one count and the same hours to 0.002 h at every hub, each 0.33 of a bin from its edge; RESET readings closed by logging no RESET; the order's minutes 0.9 to 1.2 h lower | the world (one clock, TRIPs only, orders inside their spell) and ENG-11 ("from the moment it stops to the moment it runs again, whichever record shows it": an order's later minute is not the moment the sorter stopped); asserted, with RESETs measured on a re-cut log: a lost spell ended at its RESET puts San Fernando 0.04 of a bin from its edge, TRIP to RESET moves San Fernando, El Prat and Basauri |

Forward figure (the stage-4 judge's note, not a gate failure): filing the BIC candidate family would name the load, the thing the decisive step recognises, so that fork is the stump and is not pinned. Under the filed criterion the judge's own lowest-BIC model gives 787 a week, which is 800 to the hundred; the weaker forms it lists (739, 844) carry higher BIC and are set aside by the programme's sentence.

## Ladder

- Rung 0, raw audited damage per 10,000 parcels inspected (shipped seed 2120): Zaragoza 305.0, Dos Hermanas 272.2, Ribarroja 184.3, the other three 128.1, 120.3, 116.7. Ribarroja third.
- Rung 1, the field's method (attribute standardisation; the literal execution of the programme's comparison): Zaragoza +117.8, Dos Hermanas +85.1, Ribarroja -2.8; lead 1.38.
- Rung 2, crush named the naive way (cartons sharing the cage, cage weight, position, position bands, top third): Zaragoza in every form, leads 1.33 to 1.61; a reader who sets Zaragoza aside for another reason lands Dos Hermanas (lead infinite).
- Rung 2b, scan order weighed with the sender's declared kg: Zaragoza, leads 5.21, 2.08, 3.87 (three business accounts declare 2.0, 5.0 and 4.0 kg on cartons of 15 to 21 kg).
- Rung 3 (decisive), each parcel's load from the weight scanned into its cage after it, DWS-weighed: Ribarroja 51.7 per 10,000 under the programme's lowest-BIC estimate (the 60 kg step by packaging), 51.6 in cells within the 60 kg stratum, 47.6 to 51.7 across the supported forms, every other hub at or below the network; the log forms 39.6 and 37.3 (leads 1.65 and 1.35), refuted by the fit.
- Worth: the decisive rung moves the call across three places and Ribarroja's excess from third to sole; the forward value is Ribarroja's lowest-BIC excess times its planned 161,620 parcels a peak week: 836 to the hundred 800, every supported form inside it (769 to 836).
- Pricing: the step is a reconstruction over rows the records supply exactly (the weight above is arithmetic on LOAD scans and DWS weights); the stratum edge is a corridor (35 to 95 kg give the same strata to within the light-only stacks; 20 and 30 kg refuted by the fit); the forward bin test reads, in hundreds: the decisive step's worth (the default path would size Zaragoza's excess on Zaragoza's plan, 2,100 a week, 13 bins from the golden) against the supported family's spread (0.68 of a hundred) and the golden's binomial interval (plus or minus 2.5); the sampling interval of Ribarroja's excess is about plus or minus 15 per 10,000, inside its distance to the next hub (about 50).

## Closure table
| Axis | Reading | Closure |
|---|---|---|
| 1 Population | parcels found in routine audits of regional cages built 1 July to 30 September | filed in the programme; C1 asserted against check audits and NOT FOUND lines (SF2, SF3) |
| 2 Unit of account | a parcel inspected | filed (per 10,000 parcels inspected) |
| 3 Attribution window | the cage's sorting night on its label | filed; SF4 and SF15 asserted |
| 4 As-of dating | records as of the quarter's audit close (9 October) | static; nothing revised |
| 5 Version basis | old and new damage codes both mean damaged | filed in the procedure; SF1 |
| 6 Denominator | parcels inspected | filed |
| 7 Weighting | each parcel once | filed by the unit |
| 8 Window length | the whole quarter | filed |
| 9 Boundary inclusivity | 1 July to 30 September inclusive | filed |
| 10 Rounding path | the rate computed, applied to the plan, rounded once to the hundred | asserted mid-bin over the supported family |
| 11 Tie-break | none needed; between forms, the lowest BIC | the call's lead 1.2 or more under every member, asserted; SF16 |
| 12 Maturity and censoring | every audited cage audited the next morning | none open |
| 13 Order of operations | compare at equal load, then apply to the plan | C2, the programme's lowest-BIC sentence selects the form (SF16); every supported member in one hundred |
| 14 Row order | file order irrelevant; the LOAD time orders a cage | SF7 asserted |
| 15 Duplicate resolution | re-scans and re-weighs | C1 asserted (SF6, SF8) |
| 16 Identity normalisation | barcode as printed in every system | C1 asserted (SF9) |
| 17 Netting against gross | none on the main call | not applicable |
| 18 Dimensional units | grams in the DWS, kilograms declared, UTC build log | units and zones in the column names |
| 19 Code and status semantics | both damage code lists | the procedure's table |
| 20 Integerisation | parcels a week to the nearest hundred | asserted mid-bin |
| 21 Clause scope | the programme's survey covers induction to the chutes | filed |
| 22 Forward window contents | planned parcels a week, peak weeks 48 to 52 | the peak plan ships; SF11 |

## Literal reader
Executing the programme word for word on the parcels' recorded attributes (observed against the network's expected
damage for parcels of the same weight, size, packaging, fragility and service) files Zaragoza; the golden is the same
estimand with "the same parcels" taken to include the load each carried in its cage, read from the build log and the
DWS, and the programme's lowest-BIC sentence choosing among the estimates built (on the attributes alone it keeps
an attribute model and files Zaragoza; with the load it keeps the 60 kg step by packaging and files Ribarroja at 800). Every differing reading of a term (SF1 to SF15) gives the same call and the same hundred; nothing in the bundle
reads to another answer. The asks' two conventions the stage-4 judge found open are closed: CS-FIN 07 read literally
gives the six claims counts (SF17), and ENG-11 read under every reading of the safety system's TRIPs, the union of
every record included, gives each hub's stoppages and hours stood to 0.002 h (SF18); write-up steps 6 and 7 execute
to the same figures.

## Oracles
- The 2025 survey report (Basauri): records a closed survey at a hub whose cages carry parcels only, where both routes
  agree; it ties under every basis and names no 2026 hub.
- The hub register's heavy-goods chute column and the accounts register's collection column: an ordinary cause for
  where cartons travel and when they arrive; neither ranks hubs nor ties only under the golden.
- None ties only under the golden.

## Ask sheet
Rubric sum (about 35 criteria): the call (1), the parcels a week stopped (1), Ribarroja's own sorter damage per 10,000
(1), the rivals ruled out and why (2), the chart's named parts (each hub's audited damage, the part its own sorter
accounts for, the six hubs, the unit, the window: 5), the two files (2), and the asks (24). The asks are one grid of
six hubs by four measures, two asks of twelve figures, each a component of the survey's case on rows outside the main
population.

**Ask C: damage claims by hub.** For each hub, the damaged parcels with an approved claim and the euros paid on them,
over parcels collected on the July to September sorting nights (12 figures: counts whole, euros to the nearest euro).
H18 home: the survey's case in money, what damage costs each hub, read by the network operations meeting beside the
call. Files (7 on the path, 14 columns): the case export, the transfer runs, the card gateway's refund settlement report,
the tracking history, the flat-rate terms, the hub register, the claims note.
- The WHAT, filed in Customer Service and Finance's note CS-FIN 07: the hub (the first hub sort in the parcel's
  tracking history), the period (the quarter of that sorting night, dated by the evening, Spanish time), the counting
  unit (a damaged parcel counts once however many cases are opened on it; approved when Customer Service first
  approves a case), a flat-rate case's grain (one case for all the damaged cartons of a consignment, under its first
  carton's tracking number, approved at the account's rate for each damaged carton; filed after the stage-4 judge,
  SF17), the boundary (approvals and money up to and including 20 October), the money (paid to the claimant by
  transfer for business accounts, as a refund to the card for private senders; a returned transfer is not paid until
  made again).
- Primary 1, D6 (a row at another grain than its name), block = the six counts: a business account on flat-rate
  terms opens one case for a consignment's damaged cartons, under the first carton's tracking number, approved at its
  per-carton rate times the cartons. Remedy: the approved amount over the account's rate in the commercial team's
  flat-rate terms (a recorded allocation weight). Since the stage-4 judge counted one parcel a tracking number and no
  shipped sentence said otherwise, CS-FIN 07 files the case's grain and approval basis (never the arithmetic), so the
  block is now executed from the note: every careful reader keeps the six counts and the device holds nothing. Wrong
  path, the reading the sentence excludes: one parcel a tracking number misses every hub by 53 to 217 (checks.py,
  SF17).
- Primary 2, D7 (the true key elsewhere), block = the six euro figures: the card gateway's settlement report carries
  its own refund ids, amounts and UTC times and no case reference. Remedy: each private sender's approved case
  matched to the refund of its amount made on or after its decision, one refund a case, the label-price refunds
  (cancelled labels at the tariff's prices) left out. Measured: one set under windows of 2 to 10 days, earliest or
  latest first (checks.py, D7). Wrong paths: transfers only, every hub about a fifth low; the gateway total spread
  pro rata, every hub off by tens to hundreds of euros.
- Hazards (seen, repaired right by a careful reader): the case export's hub column is the customer-service area that
  handles the case (the delivering area); a reopened business case is a new reference whose approved amount carries
  the first approval while the transfer runs pay the top-up; returned and re-made transfers; the tracking history in
  UTC with the sorting night across Spanish midnight; parcels collected in late June and early October.
- Pin test: the sentence fixes the hubs, the period, the counting unit and the roundings; the note files the hub, the
  period, a flat-rate case's grain, the boundary and the money; the device left sits in which refund is which case's,
  which no sentence names (the grain, filed after the stage-4 judge, holds nothing).

**Ask S: sorter stoppages by hub.** For each hub, the sorter's stoppages and hours stood over the July to September
sorting nights (12 figures: counts whole, hours to one decimal). H18 home: the survey's engineering case, the
stoppage record of every candidate's sorter beside the one slot. Files (4 on the path, 12 columns): the sorter
historian's event log, the work orders, the stoppage standard ENG-11, the hub register.
- The WHAT, filed in ENG-11: a stoppage is a spell in which the sorter stands still during a sorting night, from the
  moment it stops to the moment it runs again, whichever record shows it, each spell once; a sorting night runs 20:30
  to 05:00 Spanish time, dated by the evening; hours stood are the spells' lengths added.
- Primary 1, D4 (absence evidenced in a file no habitual join reaches), block = the three older sorters (Zaragoza
  Plaza, Ribarroja, Dos Hermanas), both measures: the historian's collector loses its link to the older control
  network for an hour or more on some nights while its own ALIVE rows carry on, so the standstills in those spells
  are in the night engineer's corrective work orders only. Remedy: each corrective order whose machine-stopped and
  machine-running times (Spanish time, to the minute) match no logged spell is a stoppage (a keyless match across two
  systems and two clocks). Measured: one set under order windows of 1 to 5 minutes.
- Primary 2, D1 (the same records under two sources), block = the three newer sorters (San Fernando, El Prat,
  Basauri), both measures: the safety system logs every safety trip to the historian as a TRIP with its cause code, on
  the controller's clock, in the second of the PLC's STOP or the next; when a safety trip floods the PLC's event buffer
  the PLC's STOP is lost and its RUN stands alone. Remedy: set aside the TRIPs a PLC SAFETY stop echoes and start each
  RUN no STOP precedes at the TRIP before it. Measured: one set under TRIP tolerances of 1 to 40 s, and every reading
  of the TRIP's time one figure to 0.002 h (SF18). The drifting safety clock and its offset fit died at the stage-4
  judge (`## Tried and rejected`); with one clock the deep cracker reaches this block (the deep route below).
- Every corrective order keys its stop minute at or after the logged STOP and its run minute at or before the logged
  RUN (the minute the night engineer acknowledged the stop, the clock minute at the restart), so the union of every
  source's records is the golden (SF18); the stage-4 judge's earliest-stop-to-latest-run reading had added 0.2 to
  0.3 h at the older sorters through nearest-minute orders.
- Hazards: the event log in UTC against the orders in Spanish time; the sorting night across midnight; preventive
  orders with no stoppage; corrective orders for logged spells; SORT_START and SORT_END rows.
- Pin test: the sentence fixes the hubs, the nights and the roundings; ENG-11 files the spell, the night and the
  hours; the devices sit in which records are one standstill and where a lost spell is recorded, which no sentence
  names.

**Separation.** Zero ask rows in the main call's population: no claimed parcel is an audited parcel (checks.py,
asserted by set), stoppages and claims come from other systems' records, and no document the call reads carries an
ask organ (the programme and the audit procedure name neither claims nor stoppages).

**Hazard table.** UTC against Spanish time moves the claims and stoppages at the window's two edge nights only (a few
parcels and spells, every hub); a reopened case read as a second parcel moves each hub's count by its reopened cases
and the case export's approved amounts read as money by their first approvals; the case export's hub column read as
the sorting hub moves every national parcel. Each is seen and repaired right by a careful reader and none is a primary.

**Referee.** None: every route completes and reconciles to its own totals (the transfer runs to themselves, the
gateway report to itself, the PLC's spells to its own STOP and RUN pairs).

| Cracker sheet, on the cut pack (digest 8e3dda16f1beaea0, ceiling.py) | Claims counts, D6 | Claims euros, D7 | Stoppages and hours, older sorters, D4 | Stoppages and hours, newer sorters, D1 | Kept of 24 | Verdict |
|---|---|---|---|---|---|---|
| Cracker: lands the call, runs the battery, executes CS-FIN 07 (a flat-rate case's cartons included) and ENG-11, takes the PLC's spells and sets the TRIPs aside as an echo | 6 of 6 | 0 of 6 | 0 of 6 | 0 of 6 | 6 | miss |
| Full includer A: every file and stated fact; every source's records as spells (each TRIP to the next RUN), exact duplicates dropped; the card refunds spread over hubs pro rata | 6 of 6 | 0 of 6 | 0 of 6 | 0 of 6 | 6 | miss |
| Full includer B: the PLC's spells plus every corrective work order | 6 of 6 | 0 of 6 | 0 of 6 | 0 of 6 | 6 | miss |
| Full includer C: as A, and the flat rates read as cartons (now the filed reading, so C is A) | 6 of 6 | 0 of 6 | 0 of 6 | 0 of 6 | 6 | miss |
| No repair: every row as it stands, the case export's hub and approved amounts, every STOP and TRIP row a stoppage | 0 of 6 | 0 of 6 | 0 of 6 | 0 of 6 | 0 | miss |

| Deep route, measured beside the sheet and over the bar (same digest, ceiling.py) | Claims counts, D6 | Claims euros, D7 | Stoppages and hours, older sorters, D4 | Stoppages and hours, newer sorters, D1 | Kept of 24 | Over two fifths |
|---|---|---|---|---|---|---|
| Deep cracker: the cracker, and each PLC RUN no STOP precedes counted as a stoppage, timed from the TRIP before it | 6 of 6 | 0 of 6 | 0 of 6 | 6 of 6 | 12 | keeps half |

- Verdict: a responder misses when it keeps under two fifths of the 24 ask figures; the cracker and every full
  includer keep a quarter (the six counts CS-FIN 07 now files), the no-repair reader none. The deep cracker keeps half:
  with the safety system on the controller's clock, timing a lost spell from its TRIP is the golden, so the D1 block
  holds only against the cracker who sets the TRIPs aside. Reported as measured, no device tuned.
- Pair ceiling: 42.2 with the cracker on the call and the worst full includer off it (55 x 0.250 and 55 x 0.250 on 38 + 7
  and 5 + 7); 49.1 with the deep cracker on it and the full includer off; 58.8 with two crackers on the call; 72.5 with
  two deep crackers on it.
- Mirror leakage: 25.0 per cent of the ask weight (full includers A, B and C).
- Measured by: generator/ceiling.py, which reads only target/ and imports nothing from the generator; its golden (the
  log swept, a third route independent of asks.py and verify.py) equals the generator's on all 24 figures.

## Leak sweep
`leak.py --asof 2026-10-29` on the stage-4 fix cut, target.zip c782cfef: REVIEW, no LEAK, the same eight REVIEW lines
as on 7f4cee14 (the earlier LEAKs fixed in the generator: the shipment file no longer carries the word manifest, and
10,000 is the programme's filed unit, under `stated_inputs`). Three files changed from 7f4cee14 and every main-call
file is byte-identical: CS-FIN 07 (the flat-rate sentence), the event log (the safety rows as TRIPs on the controller's
clock, no RESET, and one ordinary spell a hub re-seated mid-bin) and the work orders (minutes inside the logged spell).
- The changed CS-FIN 07 raises no line: two of the stump paragraph's terms (parcel, cartons), and it names no load,
  order, cage, trailer or weight; "flat-rate" in it is exempt from the pack check the way the card-refund wording is,
  because the claims note is where Customer Service and Finance file the case's grain, and the word stays banned in
  every other PDF (asserted).
- Sweep 3, the programme carries the call's distinctive words: harmless; it files the survey, its worth and the
  comparison the call answers, and names no hub.
- Sweep 4, the procedure, the programme and the 2025 report carry 4 to 8 of the stump paragraph's words: harmless;
  they are the world's basic nouns (parcel, records, network, audits, programme, Basauri), and none names a load,
  an order, a stratum or a cage's contents.
- Sweep 6, the peak plan, the maker's visit log and the work orders name the hubs beside numbers: harmless; weekly
  parcels sorted and planned, technician hours and order times, none a damage figure or a ranking on the survey.
- Guard on the merged corpus at 63753fc (every card on the 20 batch4 refs already present, so none copied; task214
  has none): `heart` WARN (repeat.decision against task211, answered in `## Draw`; nearest driver or stump 0.06,
  task181 v6), `surface` promoted three pairs on percentile at an absolute similarity of about 0.10 (task213, task453,
  task277), each answered on the card's differentiation; task164 is now a neighbour only.

## Tried and rejected

- 2026-11-04, the seed's title mechanism (the FY2027 final rule's severity tables remove the largest excess by
  themselves): regrouping FY2026 claims under the published rule is rule application; it can stand only as a lower
  rung (the literal replay), never decide the call.
- 2026-11-04, the severity-validation family (peer benchmark on the MCC-level share, risk adjustment on observable
  case mix, length-of-stay and in-hospital mortality validators, one patient coded by two providers): every plain
  improper practice is visible to one of the validators or to the benchmark, so a strong analyst's own validator
  reaches whatever cell carries plain upcoding; task190 architecture 7 already measured the two-provider and
  look-back members dead (filter-and-difference reaches the designed set 18 to 20 of 20; the attaining subset is
  the fully enrolled patients).
- 2026-11-04, diagnoses repeated onto same-hospital readmissions from the patient's previous stay there (a
  documentation carry-over present at every hospital at its own rate), read against the same kind of patient
  readmitted to a different hospital, where the earlier record cannot carry over. Seven parameter sets, 20 redraws
  each. Truth named the designed cell 20 of 20 every time. The mechanism's naive count (every repeated diagnosis
  that moves the DRG on a same-hospital readmission) named the golden cell 17, 17, 19, 11 and 12 of 20 in the first
  five sets, and the acute-only naive count 15, 18, 15 and 16 of 20; the golden family (family by prior-diagnosis
  matching, pooled, by family, by class) held 15 to 20 of 20. The sixth set added large genuine-recurrence cells
  (dialysis patients' N18.6 on every stay, acute-on-chronic respiratory failure recurring at 0.75): the naive
  counts then landed wrong (20 and 19 of 20) but the golden collapsed to 1 to 8 of 20, because the matched
  other-hospital recurrence cannot subtract a recurrence volume that large. Earlier single-seed versions measured
  the deniable contrast at 20 to 36 claims a cell against binomial noise of 5 to 14 claims. It also sits beside the
  client's own example of a planted copied block, which a judge reading Gate H may take it for.
- 2026-11-04, bed occupancy on the admission day setting the admission threshold (a crowded hospital admits only
  its sickest medical patients on its full weekdays, so its genuine severity excess reads as upcoding, and every
  benchmark, the hospital's annual occupancy as a covariate and both validators land on it). On one seed the ladder
  formed exactly (flagged payment A, FY2026 decomposition B, every benchmark and the annual-occupancy reader C,
  golden D). Over 20 redraws it fails: truth split 10, 8 and 2 across three cells, the golden named the academic
  sepsis cell 9 of 20, because the benchmark excess of a cell of about 5,500 claims carries binomial noise of about
  36 claims, about 0.36 million at that cell's payment step, against a designed signal near 0.2 million; making the
  golden cell's upcoding loud enough to clear that noise makes every benchmark reader name it too.
- 2026-11-04, forward behaviour as the decisive step (the sentinel effect under review, code substitution after a
  severity downgrade, a coding programme's ramp): each is a practice a governing document would have to file, and
  filed it is executed (the withheld-rule trap the brief records from task211's architecture 1).
- 2026-11-04, probe-sample and close-out extrapolation (a targeted probe weighted back to its stratum,
  probability-proportional-to-size draws): spent as drivers (task482's lineage on stratified audit weighting,
  task190 architecture 3 on PPS draws).
- 2026-11-04, re-root screens on paper before the draw, each set aside before a harness: concurrency or crowding at
  the moment of each case (a sorter's throughput, a station's gate flow, a guard on shift) dies on granularity, since
  an hourly count either reaches the golden or breaks it, so the per-case state has to be categorical rather than a
  finer cut of a continuous one; a back-fed circuit's headroom at the fault time needs the control room's back-feed
  practice filed, and filed it is replayed to the golden; storm-overflow spills during pump trips are a visible
  breach of the pass-forward condition (rule application); transformer overload from EV clusters is task164's and
  task402's ground; a bathing water's spill transient and a stagnation clock are task211's live driver in other nouns.
- 2026-11-04, the stacking candidate's first calibrations (scratch `proto_stack.py` to `proto_stack6.py`): crush linear
  in the weight on top put audited damage at 6 to 9 per cent and split the golden's forms (the linear and banded
  forms named Zaragoza in some redraws); a steeper response made the linear forms worse (11 to 14 of 20); a Poisson
  number of cartons stretched the loaded cluster past saturation (linear forms 16 to 18 of 20); placing each cage's
  carton batch at a Beta-drawn position broke the masking, Ribarroja took crush of its own and its raw rate led in 13
  of 20. The kept calibration (`proto_stack7.py`): light e-commerce parcels near 0.6 kg so a light-only stack stays
  under the crush range, a consignment of seven to nine cartons of 15 to 21 kg placed by the trunk timetable 97 per
  cent of nights, a crush response centred on 60 kg on top.
- 2026-11-05, the first ask draft (sorter stoppages with one standstill recorded by both the PLC and the safety
  controller, and stoppages inside the event logger's heartbeat gaps; claims with a reopened case's cumulative
  approval and the case export's delivering hub): every device but the gaps was executed by a filed WHAT or the
  hygiene battery (the claims note files the sorting hub, the transfer runs pay only the top-up, a PLC that logs every
  standstill makes setting the safety rows aside correct), and heartbeats that stop announce the gap, so the cracker
  kept most of the layer; replaced by the four primaries in `## Ask sheet`.
- 2026-11-05, the three business accounts' own sectors (automotive parts, ceramic tiles, olive oil and wine) were each
  unique to one hub, so a sender-sector dummy absorbed that hub's cartons and moved Ribarroja's figure by 4.7 per
  10,000 at the shipped seed; the accounts now carry sectors e-commerce senders share and the sector reader holds.
- 2026-11-05, cartons placed at a fixed share of each cage's scan sequence put a hub's cartons into its cages over 42
  to 142 minutes a night, which one dedicated trailer cannot produce; each hub-night now has one trailer arrival and
  the cartons enter every cage as it is unloaded. With Dos Hermanas's trailer at 00:32 the wrong-reason reader landed
  Ribarroja 3 of 20; at 01:20 it lands Dos Hermanas.
- 2026-11-07, closing the forward figure's load form by "the best-fitting estimate stands" (raw fit or AIC): the
  step with the constructing reader's position, cage-weight and carton-count terms added fits best on both and puts
  Ribarroja at 16.6 per 10,000 (about 300 a week), because a cage of cartons with little on a parcel occurs almost
  only at Ribarroja, so cage terms stand in for the hub; a second carton-first hub (Basauri, tried in the world)
  narrowed it to 39.7 against 51.7. A sentence naming BIC alone, in the world without the twin, picked a supported
  load form in 18 of 20 redraws and the kitchen-sink in 2; with Basauri kept as a carton-first hub (its paper account a
  2026 customer) the lowest BIC picks a supported load form in 20 of 20, setting the kitchen-sink aside by 41 or more
  (100 at the shipped seed) and the log by 66 or more (145).
- 2026-11-07, a flat-rate case's grain left unfiled (D6 riding silent on the approved amount over the account's rate):
  died at the stage-4 judge, who counted one damaged parcel a tracking number (1,101 / 772 / 827 / 1,232 / 935 / 411),
  read the golden's counts as more than the approved parcels that exist and found nothing shipped saying a flat-rate
  case covers several cartons; CS-FIN 07 section 2 now files the case's grain and approval basis in Customer Service and
  Finance's voice (SF17), the golden counts unchanged, and the device holds nothing.
- 2026-11-07, the safety system on its own clock, its stamps 34 to 426 s earlier than the PLC's and drifting over the
  quarter, with the golden
  reading its STOPs through a straight line fitted to the paired offsets, beside work orders keyed to the nearest
  minute: died at the stage-4 judge, who put San Fernando at 38.0 h (earliest stop to latest run), 33.6 h (the raw
  safety STOP) or 32.8 to 33.0 h (a mean or median offset) against the golden's 32.7, El Prat and Basauri unpinned too,
  while the same earliest-to-latest reading added 0.2 to 0.3 h at the older hubs through the nearest-minute orders. The
  safety system now keeps the controller's time and logs TRIPs only (with RESET rows, a lost spell ended at its RESET
  left San Fernando 0.04 of a bin from its edge and TRIP to RESET moved three hubs), each order keys its minutes inside
  its logged spell, and every reading is one figure (SF18). Moved, accepted with `freeze.py --allow hours_ZAZ,hours_VLC`:
  Zaragoza Plaza's hours stood 32.2 to 32.0 and Ribarroja's 39.5 to 39.4, because the older hubs' spells recorded only
  in the orders (7 and 6) are now keyed inside their minutes, each about a minute shorter, and each hub is re-seated
  mid-bin; every other graded figure is unchanged.
