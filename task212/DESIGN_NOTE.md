# task212 design note

**Status: DRAWN 2026-11-04, architecture 1 (stage 2 next).** Wave 8, Anomaly Detection & Diagnostics. The seed's
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
  condition. Three hubs carry a B2B account's heavy cartons in the same outbound cages as e-commerce parcels, because
  they have no heavy-goods chute: Zaragoza's auto-parts cartons come on the last trunk of the night, Ribarroja's
  ceramic tile cartons on the first, Dos Hermanas's olive oil and wine cases on a mid-wave trunk. Madrid, El Prat and
  Basauri sort cartons to a heavy-goods chute with cages of their own.
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
- **Sources (planned, every one synthetic, the carrier and its people fictional, the six towns real):** audit headers
  and audit findings (the quality team's audit app), sortation load scans (each hub's sorter control system, UTC),
  DWS records (the dimension and weight scanners that feed billing), the accounts register, the hub register, the
  trunk timetable and arrivals, the peak plan, the survey programme (the governing document), the audit procedure with
  its damage code list, customer damage claims, sorter maintenance work orders, and the 2025 survey report.
- **Levels, each cited:** carrier damage rates of 1 to 3 per cent of e-commerce parcels, about 3 per cent at holiday
  peaks (ShipMatrix via withanansi.com; alexanderjarvis.com; ajot.com); the prototype's audited rate is 1.9 per cent
  overall, 1.1 to 3.2 by hub. Conveyor and sort impacts and drops at transfers are a named damage point in parcel
  sortation (ajot.com, designing e-commerce packaging for high-speed sortation); the equipment effect at Ribarroja is
  an odds ratio of 1.7. Stacking loads in parcel transit are dynamic and are what ISTA 3A's compression with vibration
  simulates for parcels of 70 kg or less (ista.org 3A overview; lso-inc.com); a small single-wall e-commerce box has a
  McKee box compression strength near 200 kg static and a usable stacking load of 40 to 70 kg after the 3 to 5
  distribution safety factor, so the crush response rises steeply around 60 kg on top and a light box under a carton
  batch of 120 to 170 kg takes an odds ratio of about 4.3.
- **Screening harness (scratch, not shipped):** `t212/redraw/proto_stack7.py` with `multi_stack2.py`, clean truth, 20
  redraws (seeds 1 to 20), about 156,000 audited parcels a redraw (six hubs, 65 nights, ten cages a night), logistic
  observed against expected per hub per 10,000 parcels, the pick and its lead over the runner-up.
- **Screen 1, levels and the lever against the rivals' estimates:** the golden family names Ribarroja 20 of 20 with a
  lead of at least 2.04 (crush load as weight on top, 2.07; Poisson, 2.04; heaviest parcel on top, 2.41; cartons on
  top, 2.44; banded standardisation, 2.45); the true equipment excess names Ribarroja 20 of 20. Mid-bin figures and the
  pack size are asserted at the shipped seed in stage 3.
- **Screen 2, the golden's own method holds the call:** five of six specifications hold 20 of 20 with leads of 2 or
  more; the log of the weight on top holds 19 of 20 (lead 1.10 at the worst seed), so the shipped seed is chosen and
  asserted with every specification leading by 1.2 or more, the variant table in `checks.py`.
- **Screen 3, the first look lands wrong:** the raw audited rate names Zaragoza 20 of 20 (lead at least 1.13).
- **Screen 4, the careful readers land wrong, each 20 of 20:** (a) field-decomposing (standardisation within packaging,
  weight band, fragility and service cells) Zaragoza, lead 1.46 or more; (b) constructing, with position in the cage,
  cage weight, cartons in the cage and position times cage weight, Zaragoza, lead 4.18 or more; the same with position
  bands, Zaragoza, 1.42 or more; the top third of each cage alone, Zaragoza, 1.61 or more; (c) per-record, every
  attribute two shipped files give plus cage fill and interactions, Zaragoza, 1.65 or more; (d) mechanism-naming, crush
  read the naive way as cartons sharing the cage and the cage's weight, Zaragoza, 4.68 or more; (e) literal replay of
  the survey programme's comparison against like parcels, Zaragoza, 1.46 or more. A reader who rules Zaragoza out for a
  wrong reason (an auditor, a crew) lands on Dos Hermanas 18 of 20, Ribarroja 2 of 20: stage 2 widens Dos Hermanas.
- **Screen 5, literal execution:** the filed WHAT (equipment-caused damage per 10,000 parcels against the damage the
  same parcels suffer across the network) executed on the parcels' attributes names Zaragoza 20 of 20; the golden needs
  the crush load each parcel carried, which no filed sentence asks for and no column holds.

## Default path

The field's method at rungs 0 and 1: audited damage per hub, then indirect standardisation (observed against expected
from a pooled model of the parcels' own attributes), cut every way, with the cartons in each cage allowed for.

1. Read the survey programme: the survey goes to the hub whose own sortation equipment damaged the most parcels per
   10,000 it loaded in the July to September 2026 audits, and its value is the damaged parcels a week its repairs stop
   over the peak.
2. Build the audited parcels: keep each cage's first audit, drop lines for parcels not found, map hub numbers to names
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
- Layer 1: sortation load scans in UTC against audits and DWS records in Spanish summer time (each hub's sorter control system against the audit app and the DWS); DWS weights in grams and dimensions in millimetres (the DWS); re-scans of a parcel into its cage after a no-read (the sorter control system); re-weighs at the DWS; the damage code list replaced on 1 August with two depots' handhelds still keying old codes (the audit app); hub numbers in the sorter export against hub names in the audit app; supervisors' check audits and NOT FOUND lines (the audit app); sender-declared weights as account defaults (the manifest system). Each is produced by its own system, none is placed to be caught, none moves the call (R2 assertions).
- Layer 2: estimand_identification, a Simpson's reversal across a constructed stratum: each audited parcel's crush load, the weight scanned into its cage after it, separates crush in the cage from the sorter's own damage; Zaragoza's excess is crush under the auto-parts cartons it loads last, and Ribarroja's sorter damage hides because its tile cartons go into the cage first.
- Decisive step: rebuilding each audited parcel's load from the parcels scanned into its cage after it, weighed through the DWS records, and comparing the hubs' damage within load strata, which accounts for Zaragoza and Dos Hermanas and leaves Ribarroja's excess as the sorter's.
- Not semantics: every field read correctly (the damage codes and their crosswalk, check audits, NOT FOUND lines, the cage's build date, the DWS grams, the scan clock, the declared weights) still leaves the attribute-standardised excess on Zaragoza; no field, code or flag holds a parcel's load, and the declared weights a reader might use for it are account defaults.
- Not rule application: no filed rule names a load, an order or a stratum, and executing the survey programme's comparison on the parcels' attributes files Zaragoza. The enumerated family (raw rate, field cells, attribute logit, per-record logit with cage fill and interactions, position in the cage, cage weight, position bands, top third, unordered cartons in the cage, scan order weighed with declared weights, scan order weighed with DWS weights as a 60 kg step, bands, cartons on top, heaviest parcel on top, linear and log) spreads the call over Zaragoza (eleven members) and Ribarroja (twelve); the standing family, the DWS-weighted order in the forms the record's own fit supports (deviance 29,475 for the step, 29,494 to 29,511 for heaviest on top, cartons on top and linear, against 29,611 for the log and 30,410 with no load term), names Ribarroja in every member at 45.3 to 48.0 per 10,000 at the shipped seed; the ruling-out is loud, the no-load model's deviance about 935 above the step's.
- Analyst test: a strong analyst who reads every field and rule correctly standardises each hub's audited damage on the parcels' weight, size, packaging, fragility and service, cuts it every way, allows for the cartons sharing three hubs' cages and books the survey to Zaragoza, the default path's `Ends on:`.
- Estimand: the survey programme (Network Operations, filed) fixes the population (parcels found and inspected in routine audits of the regional outbound cages built on the sorting nights of 1 July to 30 September 2026), the outcome (the damaged parcels a hub's own sorting equipment accounts for, done between induction and the chute), the unit (per 10,000 parcels inspected), the comparison (the damage the same parcels take across the network's six hubs) and the forward value (that rate times the hub's planned parcels a week averaged over peak weeks 48 to 52 of the 2026 peak plan).
- No decoy: nothing is planted to be caught; Zaragoza's cartons arrive on the night's last trunk by the timetable, no memo, draft, summary or ranking argues for a hub, the audit records are records and the 2025 survey report records a closed survey at Basauri.
- No certified replay: no certified or published figure is reproduced to recover a method; the 2025 report's before and after rates are Basauri's own audits and every route reads them alike.
- Lesson: read a damage rate within the structure that generates it before naming the unit that causes it, here the weight each parcel carried in its cage, rebuilt from the order of the cage's load scans against the DWS weights; no build on file reads an order relation inside a container.

## Survivor anatomy

- Actor: the deciding property, the weight sitting on an audited parcel in its cage, has no column in any file; the parcel has rows (an audit line, a load scan, a DWS record, a manifest line) and the property is a relation between its load scan and the later load scans of the same cage, weighed through the DWS.
- Link: the signal is read through a comparison no key offers: the order of a cage's load scans set against the DWS weights of the parcels scanned after each audited one; the cage label joins the parcels but nothing orders or weighs them, and no sentence mentions a cage's order or load.
- Reflex: the field's method (indirect standardisation on the parcels' attributes, cut by every field) sits at rungs 0 and 1 and files Zaragoza, lead 1.88 at the shipped seed.
- Back-test: the textbook route validates: the 2025 survey went to Basauri on its standardised excess, a worn transfer plate was replaced and Basauri's audited rate fell; Basauri sorts its cartons to a heavy-goods chute, so both routes agree on that closed case.
- Second use: the load scans carry each cage's contents and build night (the audit's load list), the DWS records carry the parcels' weights, sizes and shapes for the attribute model and billing, the manifest the service and fragility; none ships for the decisive step alone.
- Shock: Ribarroja is third on the raw rate and third on the standardised excess, never first on any shipped statistic; the movement the step recovers reads as an ordinary middling hub.
- Pins: the survey programme files the population, outcome, unit, comparison and forward value in Network Operations' own voice and names no cage, order, load, weight on top, scan or stratum; deleting any of its sentences unforces nothing the decisive step rides on.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | 7 dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 raw audited rate (Zaragoza) | fires (the programme's unit) | fires (audit lines) | fires | no | no | fires | no | readable |
| 1 attribute standardisation (Zaragoza) | fires (the comparison) | fires (DWS and manifest columns) | fires | no | no | no | no | readable |
| 2 cartons sharing the cage, cage weight, position (Zaragoza) | no | fires (cage label) | fires (crush named naively) | no | no | no | no | readable |
| 2b scan order weighed with declared weights (Zaragoza) | no | fires (declared_kg) | fires | no | no | no | no | readable |
| 3 crush load from load scans against DWS weights (decisive, Ribarroja) | no | no (no column holds order or load) | no | no | no | no | no (scans and DWS ship for the load list and the attributes) | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | damaged | any damage code the auditor records, old or new list | crush codes only | same call | same call, asserted |
| SF2 | inspected | parcels found in the cage at a routine audit | NOT FOUND lines counted as inspected and OK | same call | audit procedure: a parcel not found is not inspected; same call asserted |
| SF3 | which audits | routine audits | routine and check audits | same call | audit procedure: a check audit verifies the auditor and does not replace the routine audit; same call asserted |
| SF4 | the window | cages built on the sorting nights of 1 July to 30 September (label build date) | audit date | same call | survey programme names the sorting nights; same call asserted |
| SF5 | the comparison pool | the network's six hubs | the other five hubs | same call | survey programme: across the network's six hubs |
| SF6 | a re-scanned parcel's place | its first load scan | its last load scan | same call and figures | same call asserted, figure moves under 0.1 |
| SF7 | ties in scan time | none in any cage | not applicable | same call | asserted: no two load scans in a cage share a second |
| SF8 | a re-weighed parcel's weight | first DWS record | last or mean | same call and figures | same call asserted |
| SF9 | the DWS join key | the barcode as printed | normalised barcode | same set | asserted: one set under both readings |
| SF10 | the load stratum's edge | 60 kg on top | any edge from 35 to 95 kg | same call | asserted over the corridor |
| SF11 | the forward volume | mean of planned parcels a week, weeks 48 to 52 | the five-week total over five | same figure | identical arithmetic |
| SF12 | the cartons' own damage | inside the hub's damage | light parcels only | same call | same call asserted |

## Ladder

- Rung 0, raw audited damage per 10,000 parcels inspected: Zaragoza 319.6, Dos Hermanas 258.2, Ribarroja 186.3 (shipped seed 2120). Ribarroja third.
- Rung 1, the field's method (attribute standardisation; the literal execution of the programme's comparison): Zaragoza +130.5, Dos Hermanas +69.5, Ribarroja third; lead 1.88.
- Rung 2, crush named naively (cartons sharing the cage, cage weight, position in the cage, position bands, top third): Zaragoza in every form, leads 1.64 to 9.3; a reader who rules Zaragoza out for a wrong reason lands Dos Hermanas.
- Rung 2b, scan order weighed with the sender's declared weights: Zaragoza, lead 9.84 (the declared weights are account defaults, 2.0 kg on every auto-parts carton).
- Rung 3 (decisive), each parcel's load from the weight scanned into its cage after it, DWS-weighed: Ribarroja +45.3 to +48.0 per 10,000 across the supported forms, every other hub at or below zero; lead infinite or 2.39 at the worst form (log).
- Worth: the decisive rung moves the call across three places and Ribarroja's excess from third to sole; the forward value is Ribarroja's excess times its planned parcels a peak week.
- Pricing: the step is a reconstruction over rows the records supply exactly (the weight above is arithmetic on scans and DWS weights); the stratum edge is a C3 corridor (35 to 95 kg give the same strata to within the light-only stacks); the sampling interval of Ribarroja's excess is about plus or minus 13 per 10,000, far inside its distance to the next hub (about 50).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | parcels found in routine audits of regional cages built 1 July to 30 September | filed in the survey programme; C1 asserted against check audits and NOT FOUND lines |
| 2 Unit of account | a parcel inspected | filed (per 10,000 parcels inspected) |
| 3 Attribution window | the cage's sorting night on its label | filed; no audit straddles a quarter edge by build date |
| 4 As-of dating | records as of the audit export | static; nothing revised |
| 5 Version basis | old and new damage codes both mean damaged | C1 asserted (SF1) |
| 6 Denominator | parcels inspected | filed |
| 7 Weighting | each parcel once | filed by the unit |
| 8 Window length | the whole quarter | filed |
| 9 Boundary inclusivity | 1 July to 30 September inclusive | filed |
| 10 Rounding path | rates computed then rounded once | asserted |
| 11 Tie-break | none needed, the lead is wide | asserted lead at least 1.2 under every supported form |
| 12 Maturity and censoring | every cage audited the next morning | none open |
| 13 Order of operations | standardise within load strata | C1, every supported form agrees |
| 14 Row order | file order irrelevant; scan time orders a cage | asserted over a shuffled read |
| 15 Duplicate resolution | re-scans and re-weighs | C1 asserted (SF6, SF8) |
| 16 Identity normalisation | barcode as printed in all systems | C1 asserted (SF9) |
| 17 Netting against gross | none | not applicable |
| 18 Dimensional units | grams in the DWS, kilograms declared | units in the column names |
| 19 Code and status semantics | the damage code crosswalk | shipped crosswalk; C1 |
| 20 Integerisation | counts are whole parcels | by construction |
| 21 Clause scope | the programme covers the sorter between induction and the chute | filed |
| 22 Forward window contents | planned parcels a week, peak weeks 48 to 52 | the peak plan ships |

## Literal reader

Executing the survey programme word for word on the parcels' own attributes (indirect standardisation against the network's like parcels) files Zaragoza; the golden is the same estimand computed with the parcels' load read from the records, and every differing reading of a term (SF1 to SF12) gives the same call; nothing in the bundle reads to another answer.

## Oracles

- The 2025 survey report (Basauri): confirms the standardised route on a hub with a heavy-goods chute, where both routes agree; it ties under every basis.
- The hub register's heavy-goods chute column and the trunk timetable: an ordinary cause for where cartons travel; neither ranks hubs nor ties only under the golden.
- None ties only under the golden.

## Ask sheet

- Ask 1, sorter stoppages and hours stood per hub (twelve figures). H18 home: the survey's own capacity case (the slot takes the sorter out of service). Files: the sorter event log (two controllers, UTC, heartbeats), the engineering work orders (local), the stoppage reporting standard. Primary 1, D1: one standstill recorded by both the PLC and the safety controller; primary 2, D4: stoppages inside the event logger's heartbeat gaps, held only by the work orders' machine stopped and running times. Pin test: the standard files a stoppage as a spell of standing still, from stop to restart, over the sorting nights of July to September; neither device's dimension is named.
- Ask 2, damage claims and euros paid per hub (twelve figures). H18 home: the survey's value in money terms for the network. Files: the customer service export, finance's payment lines, the claimed parcels' tracking history, the claims handling note. Primary 1, D2: a reopened claim takes a new reference whose approved amount carries the first approval, while finance pays only the top-up; primary 2, D7: the export's hub is the delivery hub, while the note charges a claim to the hub that sorted the parcel the night it was collected, read from the tracking history's first sort scan. Pin test: the note files the counting unit (a damaged parcel is one claim), the cost (money paid), the hub and the window; neither device's dimension is named.
- Separation: zero ask rows in the main call's population (stoppages and claims are other systems' records; claimed parcels are not audited parcels, asserted by count).
- Cracker and mirror sheets: pending `generator/ceiling.py` on the cut pack.
- Pair ceiling: pending
- Mirror leakage: pending
- Measured by: generator/ceiling.py (to be written; shares no code with the generator)

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
