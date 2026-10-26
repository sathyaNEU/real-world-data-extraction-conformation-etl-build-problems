# task306 design note

Architecture 1, drawn 2026-10-24. Seed `analytical_tasks/04_opportunity_sizing/OS08` (the world, the decision and the quantity only: a refurbishment plant tooling next year's out-of-warranty traction-battery replacements across five EV platforms in lots of 50).

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task306.json`, architecture v1, registered 2026-10-24. Guard verdict WARN after two axis redraws at check (below); `test.same_puzzle_older` and `test.same_driver_older` are cleared by differentiation lines against task468's lineage and task98's lineage; task132 and task133 are differentiated on the card. Nearest drivers on file sit at 0.05 (task183, task130 lineage, task138 lineage, task114, task479 lineage).
- **Pairing:** Energy Systems & Utilities / `asset-condition-maintenance`, drawn for Opportunity Sizing & Decision Support. The task type forecasts the failures an asset base will throw off from each asset's own condition and sizes the maintenance capacity to meet them; here the assets are traction-battery packs in cars on the Dutch register, and the opportunity is the year's out-of-warranty replacement demand the refurbisher's fixed line is tooled against, pool (every pack in use in the Netherlands in 2027) to realisable (the packs that fail in 2027 outside cover).
- **Niche:** Voltwerk Accu Revisie B.V. (fictional, Tilburg) refurbishes traction batteries for five platforms (Volta hatch, Kestrel SUV, Plover saloon, Mira city car, Tern van). Fixtures, module stock and end-of-line test programmes are platform-specific and are committed before the year in lots of 50; the 3,000 slots of 2027 are split in proportion to each platform's forecast of pack failures outside the OEM warranty in the Netherlands in 2027, by largest remainder; demand is about 3,800, so the split rations the line.
- **The call:** each platform's 2027 slots in lots of 50 and the total forecast to the nearest hundred: Mira city car 1,450, Volta hatch 900, Plover saloon 350, Kestrel SUV 250, Tern van 50, 3,800 failures (world seed 3448, line seed 31062). The register-only route files Volta 1,000, Kestrel 300, Plover 350, Mira 1,250, Tern 100 and 3,400, four of the five slot figures and the total wrong.
- **Shape:** other. The call is an allocation of 60 lots to five platforms with the sized total (5 + 1), three per-lot asks over the five platforms (15), the chart's parts and the two files: about 30 criteria. Shape 05 is the honest key and `ban.shape` holds it against task486, so the shape is filed as other with this arithmetic rather than relabelled. Per-platform forecasts are not graded: the register-only route files four of the five at the nearest hundred, so grading them would pay the wrong route.
- **Strategy:** `maturity_censoring`, Gate G `forecasting`, generators G13 (the register's horizon is 30 June 2026, the decision's is calendar 2027), G6 (the 2027 pool's mix shifts toward old imported Mira cars), G12 (the cars still to arrive are absent from the register, not absent from the fleet); gap population, then time; Layer 2 `estimand_identification`, pattern `own:installed-base-forecast-carrying-the-inflow-the-register-does-not-hold-yet`. F4's insight is this build's: the register is the count that has arrived, the decision needs an estimate of what will arrive, and the arrived count understates exactly the platform whose cars keep arriving. Redrawn at check and registration against the live window (task179, task275, task483): `population_selection` (the F7 reading, who is in the denominator) is banned against task275 and `composition_mix` against task179, and F4 is the honester of the free labels, since the error is an arrival stream left uncounted rather than a rate misapplied; the decisive generator moved from G12 to G13 (`ban.pattern` against task482 at the first check), G13 being the honester first code because the register is complete for its own date.
- **Forum, event, organisation:** line_manager_or_team (Voltwerk's head of operations signs the tooling plan; `executive_team` was banned against task179), purchase_order_or_contract (fixtures and module stock committed before the year), manufacturer. Role capacity_planner; context artifact `capacity_report` (the tooling plan; `register` and `filed_standard` were banned against task179 and task483).
- **People** (`guard.py names --geo NL --seed 306`): Imke Recers, operations planner, who asks; Maarten Cammel, finance controller. Neither appears in the prompt.
- **Probes before the draw:** call-only, isolated, medium effort, on two packs cut from the prototype (scratch `t306/`). Pack 1 (seed 3061, an imported car's pack history abroad hidden): sonnet tooled exactly the register-only split after calibrating the hidden abroad replacements down by 0.74; opus built a careful register forecast, back-tested it on 2024 and 2025, and left out "cars that will come onto the register after June 2026" in a caveat. Pack 2 (the history made complete, EU-wide): sonnet filed the register-only split to the slot (1,100, 300, 350, 1,150, 100); opus also forecast from the register alone (its own code compared microsecond and nanosecond timestamps, so it never applied the warranty end). Four of four missed the decisive step.
- **WARNs answered:** `overuse.gate_g` (forecasting in five of the last twelve): the decisive mechanism is a forecast's population, and no other key is honest. `repeat.deliverables` (xlsx and png against task275): a tooling workbook and a chart of the split are what an operations board takes; the deliverable names and contents are this build's own.
- **Data-native sentence:** the RDW register holds each car from the day it is first registered in the Netherlands and carries its first admission anywhere in the EU, so the used imports it shows arriving every month, about 116 Mira city cars a month at 8.1 years from first admission, are already past the Mira's five-year pack warranty when they arrive; a forecast summed over the register on 30 June 2026 is complete for that day and short of every car that arrives before or during 2027, and those cars' packs fall due in their first months here.

## Three rules

Task type: asset-condition-maintenance (Energy Systems & Utilities), tagged in the taxonomy for Opportunity Sizing & Decision Support: the out-of-warranty failures an asset base throws off in 2027, forecast from each asset's own condition (the pack it carries, the pack's age, its life curve, the car's warranty clock), sizing a refurbishment line's fixed capacity across five platforms.
Domain test: The deciding quantity is each platform's 2027 pack failures outside the OEM warranty in the Netherlands, the asset-condition analyst's installed-base forecast built from each pack's own condition; for a vehicle fleet the installed base keeps moving through used imports that the register records only as they arrive, so the 2027 base is the register plus the arrival stream its own registration dates show, and replacing it with the register's own sum moves four lots onto the Volta hatch, Kestrel SUV and Tern van from the Mira city car.
Swap: "the slots each platform needs once the used imports the register shows arriving, eight years old and past their pack warranty, are carried into 2027" put into a hospital's infusion pumps or a utility's distribution transformers loses its mechanism: no hospital takes in used pumps from abroad every month past their warranty, no transformer fleet grows by imported second-hand units, and no asset register carries both an asset's first service anywhere and its arrival date here.
Layer 1: the RDW open-data extract with Dutch field names, YYYYMMDD dates and two registration dates per car; trade names that vary by variant; a replacement log merged from the OEMs' EU-wide dealer records and Voltwerk's own, with the country, the cover and the source of each fit, and rows for cars scrapped or exported before the extract; life curves published as cumulative shares by whole year of pack age; per-platform warranties (the Mira's five years, the others' eight); the line's MES, stores, bench and recycler exports in their own codes and units; nothing is placed to be caught.
Layer 2: estimand_identification: the population whose packs fall due in 2027 is every car in use in the Netherlands in 2027, which the plan files as the register of 30 June 2026 and the cars first registered here from 1 July 2026 to the end of 2027; which of the later registrations' packs fall due is filed nowhere: the used imports among them are projected from the register's own arrival history (their rate, their age and the pack each arrived with) and carried at their conditional chance of failing outside the warranty after they arrive, while the new cars stay inside their warranty all year.
Decisive step: carrying the used imports the register shows arriving every month into the 2027 forecast, each at the pack it arrives with and its chance of failing in 2027 after its warranty once it is here, rather than taking the register of 30 June 2026 as the population whose packs fall due in 2027.
Not semantics: every field reads as what it is (first admission, first Dutch registration, each replacement's date and pack, the warranty years from first admission), the curves are read as the plan says, and the register is complete for its own date; the plan files that the cars first registered here after 30 June 2026 are in the 2027 fleet, and no field, code or sentence says that any of them is a used car or past its warranty, so the analyst who reads all of it correctly and carries them as the new cars most registrations are, or as the fleet's growth at its average chance, still files the register's split or Mira city car 1,300 to 1,400.
Not rule application: the plan files the WHAT (failures outside the OEM warranty on each platform in the Netherlands in calendar 2027, the fleet of 2027 as the register and the cars first registered here from 1 July 2026 to the end of 2027, one pack per car, a car in use taken to stay in use, the curves read by straight lines, the largest remainder) and nothing about how the later registrations are projected or which of them fall due. Enumerated family on the Mira city car: 1,250 slots (the register alone, or the later registrations carried as new cars), 1,350 (either half of the stream) and 1,450 (the full stream), a spread of four lots and 3,448 to 3,828 on the total. Standing family (SF25, 144 projections carrying the full stream: trailing windows of 3 to 48 months, calendar 2024 or 2025, straight-line trends over 12 to 48 months, each with the cars on their own day of the month, mid-month, on the first, on the last or spread through the month, on the pack they were registered with or built with; by quarter at each car's own month or mid-quarter; the last 12 or 18 months replayed): one call on all five platforms and one total, the Mira city car's import failures 320.2 to 395.5 inside the golden's corridor of 318 to 398.5, totals 3,771 to 3,848, all 3,800, worst remainder margin 0.029 lots; the conventions (the late-2026 renewal, warranty ends in calendar or 365.25-day years, pack age over 365 or 365.25 days) file the same call. The ruling-out is not loud: no filed sentence says which later registrations fall due; only the register's own two date columns do, about 116 Mira imports a month 8.1 years old, which no filed rule and no one group-by of the forecast's own inputs puts into the 2027 sum.
Analyst test: A strong analyst who reads every file correctly takes each registered car's pack from the log and its conditional chance of failing outside the warranty from the curves, counts the cars first registered here after 30 June 2026 as the plan files them, and carries them as the new cars most registrations are, inside their warranty all year, so they add nothing: Volta hatch 1,000, Kestrel SUV 300, Plover saloon 350, Mira city car 1,250, Tern van 100 against a total of 3,400, where the golden is 900, 250, 350, 1,450 and 50 against 3,800 (carried as the fleet's growth at its average chance instead, the Mira city car gets 1,300 to 1,400); checks.py runs it on the generator's clean truth and on the pack.
Estimand: each platform's pack failures outside the OEM warranty in the Netherlands in calendar 2027 (a pack failing on a car in use in the Netherlands after the OEM's warranty on that car has ended, Voltwerk refurbished packs included whether or not Voltwerk's own warranty covers them), over the fleet of 2027 (the register of 30 June 2026 and the cars first registered here from 1 July 2026 to the end of 2027, each from the day it is registered), one pack per car (the pack it carries at the end of 30 June 2026, or when it is registered if later), with the 3,000 slots split in lots of 50 in proportion by largest remainder (tooling_plan_2027_draft.docx sections 2 and 3).
No decoy: nothing is planted: the register is the RDW's as it stood on 30 June 2026, the log the recorded replacements, the curves the OEMs' and Voltwerk's own; no memo, draft or figure argues for a split, no file ranks the platforms, no past split or forecast is in the pack, and no stakeholder figure is set up to be overturned.
No certified replay: no certified or published figure sits in the pack; no file states a forecast, a past split or a past year's replacement count to be reproduced, and the method is not recovered from any figure.
Lesson: an installed-base forecast is a forecast of the base too; when the roll it is summed over is a snapshot of a base that keeps taking in old units, the units still to arrive are part of the population and the roll's own arrival dates show them; no build on file forecasts a population's units still to arrive from the roll's own arrival history.

## Default path

1. Maps each row of the RDW extract to its platform by make and reads the two dates; takes each car's pack on 30 June 2026 from the log: its last replacement, else the pack it was built with.
2. Ends the OEM warranty 8 years after first admission (5 for the Mira city car, the warranty terms' table) and reads each pack's age from its fitting.
3. Gives each car the chance its pack fails in 2027 after the warranty, given it works on 30 June 2026, from the curves read by straight lines.
4. Sums by platform over the register: Mira city car 1,469, Volta hatch 1,142, Plover saloon 425, Kestrel SUV 322, Tern van 91, 3,448 in all.
5. Splits the 60 lots by largest remainder and reports the total to the nearest hundred.

Ends on: Volta hatch 1,000, Kestrel SUV 300, Plover saloon 350, Mira city car 1,250, Tern van 100 slots, 3,400 failures
Golden: Volta hatch 900, Kestrel SUV 250, Plover saloon 350, Mira city car 1,450, Tern van 50 slots, 3,800 failures

## Stump sentence

A competent analyst forecasts 2027 from the register of 30 June 2026 alone, each car's pack from the log at its chance of failing after its warranty, and tools the Mira city car 1,250 slots and the Volta hatch 1,000, the Kestrel SUV 300 and the Tern van 100 against the golden 1,450, 900, 250 and 50, with a total of 3,400 against 3,800; the step that lands it there is taking the register as the population whose packs fall due in 2027, when the register's own arrival dates show about 116 used Mira city cars a month arriving past their five-year warranty, whose packs fail in their first months here.

## Readability screen

| Rung | What it needs | Verdict |
|---|---|---|
| warranty from first admission, not the Dutch registration | the warranty terms' sentence (wherever in the EU) and the field descriptions | readable |
| each car's pack from the log | the plan's pack-age sentence and a join on the plate | readable |
| the chance given the pack works on 30 June 2026 | standard conditioning of a life curve on survival | readable |
| the cars first registered after 30 June 2026 are in the 2027 fleet | the plan, section 3 (filed at the portal return, SF25) | readable |
| the full arrival stream, July 2026 to December 2027, carried at its own age, pack and warranty (decisive) | the register's two date columns; no sentence says any later registration is a used car or past its warranty | silent |

## Ladder

| Rung | Construction | Mira city car slots | Split (Volta, Kestrel, Plover, Mira, Tern) | Total, nearest hundred |
|---|---|---|---|---|
| R0 | warranty and pack age from the Dutch registration (a field misread) | 550 | 1,350, 400, 550, 550, 150 | 1,900 |
| R1 | the chance unconditioned on 30 June 2026 | 1,100 | 1,000, 350, 450, 1,100, 100 | 2,500 |
| R2 | every car on the pack it was built with (log ignored) | 1,600 | 850, 200, 300, 1,600, 50 | 5,400 |
| R3 | the register alone (default path) | 1,250 | 1,000, 300, 350, 1,250, 100 | 3,400 |
| R4 | half the stream (arrivals through December 2026 only, or in 2027 only) | 1,350 | 950, 250, 350, 1,350, 100 | 3,600 |
| R5 | the full stream (golden) | 1,450 | 900, 250, 350, 1,450, 50 | 3,800 |

R3 is the stump; R4 is the partial repair (the fleet of 1 January 2027, or only the year's own arrivals); every rung is asserted in checks.py.

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | next year, 2027 | calendar 2027 | Voltwerk's financial year July 2027 to June 2028 | another window | the plan, section 2: "in calendar 2027" |
| SF2 | outside the OEM warranty | Voltwerk-warranty failures count | left out | same slots (total 3,750) | the plan, section 3: a refurbished pack's failure counts whether or not our warranty covers it |
| SF3 | eight (five) years from first admission | calendar years | 365.25-day years | same call | same call |
| SF4 | pack age in years | days over 365.25 | days over 365 | same call | same call |
| SF5 | reading the curves | straight lines between whole years | steps (the share at the last whole year) | Kestrel 200, Mira 1,500 | the plan, section 3: read by straight lines |
| SF6 | the warranty's start | first admission anywhere | first Dutch registration | R0 | warranty terms, section 1: wherever in the EU, not restarting when the vehicle changes country |
| SF7 | a pack's age | from its fitting, or first admission for the original pack | from the Dutch registration | R0 | the plan, section 3 |
| SF8 | a pack replaced under the OEM warranty | covered to the original end | a new period | another call | warranty terms, section 1 |
| SF9 | cars leaving use | none in 2027 | a scrappage rate | another call | the plan, section 3: a car in use is taken to stay in use |
| SF10 | which cars are imports | first admission before first Dutch registration | another marker | same set | the field descriptions; no car is registered here before its first admission (asserted) |
| SF11 | the total's rounding | nearest hundred of the unrounded sum | sum of rounded parts | same (3,800) | same call |
| SF12 | largest remainder at a tie | none open | none | margin 0.27 lots | asserted |
| SF13 | the five platforms | the five makes, one platform each | another mapping | none | the field descriptions: each make is one platform |
| SF14 | in the Netherlands | cars on the Dutch register | none | none | the plan and the extract |
| SF15 | ask A, modules issued | net of returns | issues only | 173, 289, 198, 153, 238 | the asking sentence: net of returns |
| SF16 | ask A, modules | a Kestrel carrier is 2 | stores units | Kestrel 141 | artikelstam: modules per unit |
| SF17 | ask A, packs shipped | shipments in the year | work orders closed as shipped in the year | same counts (asserted) | same answer |
| SF18 | ask B, a run | an aborted run is no run | an ABORT as a failed first run | 91.4, 85.4, 91.4, 85.9, 90.5 | the line notes: an aborted run is no test of the pack |
| SF19 | ask B, the packs counted | packs whose first run was in the year | packs with any run in the year | another population | the asking sentence: packs that had their first run in those months |
| SF20 | ask C, cores received | every core received at either dock in the twelve months, by the day received | the cores the line scrapped left out of the count | 9.3, 6.2, 11.2, 15.1, 8.7 | the asking sentence: the cores we received |
| SF22 | the failure chance | the published curves | a curve rescaled to a year's realised fittings | another split | the plan, section 3: packs fail as the life curves say |
| SF21 | ask C, rejected at intake | graded AFGEKEURD with no work order on the core | every AFGEKEURD row on 1 July 2026 | 12.6, 10.1, 13.2, 17.6, 12.5 | the asking sentence (at intake) and the MES notes (the core the pack is built on); the quarantine tags' dates give the same rejects (asserted) |
| SF23 | ask A, the window | modules issued in the twelve months, per pack shipped in those months | the modules issued to the packs shipped in the year, whenever issued (the stores export of the year holds only part of it) | 158, 239, 180, 138, 224 | the asking sentence: issued them in the twelve months to June 2026, per pack we shipped in those months |
| SF24 | the forecast's rounding | the 2027 total to the nearest hundred, the split from the unrounded forecasts | each platform's forecast to the nearest hundred before the split | Plover 300, Tern 100 | the prompt: round the 2027 total |
| SF25 | the 2027 population (portal return, both judges) | the fleet of 2027: the register of 30 June 2026 and the cars first registered here from 1 July 2026 to the end of 2027, each from the day it is registered; the later registrations projected from the register's own used imports, the new cars among them inside their warranty all year | both judges: the register of 30 June 2026 alone, no entries projected (the plan as shipped: a car in use taken to stay in use, the register the only source named) | Mira city car 1,250, Volta hatch 1,000, Plover saloon 350, Kestrel SUV 300, Tern van 100, 3,400 (with SF26's renewals Mira 1,300, Tern 50, 3,500) | the plan, section 3: "those first registered here from 1 July 2026 to the end of 2027, each from the day it is registered" (the WHAT pinned at authority, no import, arrival or method named); the projection stays open and converges (C1: 144 projections file the golden split and total, asserted by name in checks.py, six recomputed in verify.py); outside the family each cell maps to what it violates: half streams the sentence, a quarter's cars all on its first or last day the register's own dates, copies kept at their first admission the register's steady age on arrival, one pooled age the platforms' own ages, an unconditioned chance the register's own conditioning |
| SF26 | which failures a car contributes (portal return, a judge) | one pack per car: the pack it carries at the end of 30 June 2026 (a fit that day included), or the pack a later registration carries when registered, and that pack's failure; a pack fitted in its place later left out | a judge: renewals in, the refurbished packs fitted after late-2026 failures failing again in 2027 (the judge's +25.3; the generator's late-2026 term is +16.2); also the pack at the start of 30 June (8 fits that day) | same call and total (asserted); the register's stated 3,448 becomes 3,465 or 3,450 | the plan, section 3: "The forecast follows one pack per car and counts its failure", "at the end of 30 June 2026", "a pack fitted in its place later is left out" |
| SF27 | ask A, a pick list serving several work orders on a replacement lot (portal return, a judge) | each held lot's replacement modules went out once: the quantity the list repeats counted once, which brings each of the eight replacement lots back to its receipt | a judge: every stores line summed as written | 171, 283, 195, 150, 238 against 167, 274, 190, 149, 224 | the line notes: "stores keeps its stock by lot, and no lot's stock goes below zero", one receipt row per lot: as written the eight replacement lots go below zero; every repair that keeps them at zero or above (the quantity counted once, the lot capped at its receipt, its lines scaled to it) files the golden to the module (C1, asserted); under the golden reading no lot goes below zero, so collapsing the other shared lists is called for by nothing |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | every car of the five platforms in use in the Netherlands in calendar 2027, cars still to arrive included | filed literally at authority (plan section 3: the register of 30 June 2026 and the cars first registered here from 1 July 2026 to the end of 2027, each from the day it is registered; SF25); the extract describes itself as the register of 30 June 2026 |
| 2 | Unit of account | a pack failure outside the OEM warranty; a slot is one pack | filed (plan sections 1 and 3) |
| 3 | Attribution window | failures from 1 January to 31 December 2027 | filed (plan section 2) |
| 4 | As-of dating | the register and log as of 30 June 2026; the line's exports of 1 July 2026 | filed (file names, field descriptions, line notes) |
| 5 | Version basis | the 2026 warranty summary; the published curves | filed |
| 6 | Denominator | the five platforms' forecast total for the shares; packs shipped, packs first run, cores received for the asks | filed (plan section 2; the asking sentences) |
| 7 | Weighting | each car once (plan section 3, one pack per car), each later registration at the window's rate per month | filed (SF26) and C1 (SF25: 144 projections file one call and one total, asserted) |
| 8 | Window length | twelve months of arrivals | C1 (trailing 3 to 48 months, calendar 2024 and 2025, trends over 12 to 48 months agree, asserted in SF25) |
| 9 | Boundary inclusivity | the year's first and last days in; a replacement on 30 June 2026 counts as fitted | filed (plan section 3: the pack a car carries at the end of 30 June 2026; SF26); the 8 fits of that day move the register's stated figure to 3,450 under the other reading, never the call (asserted) |
| 10 | Rounding path | shares from unrounded forecasts; total to the nearest hundred once | filed (the prompt) |
| 11 | Tie-break | none at the cut | asserted (margin 0.27 lots) |
| 12 | Maturity and censoring | cars still to arrive in the population | filed WHAT (axis 1, SF25); the construction (which later registrations fall due, carried at their own age, pack and warranty) is the stump |
| 13 | Order of operations | forecast, then shares, then lots | filed (plan section 2) |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | ask A's repeated batch quantity counted once (device); no duplicate in the call's files | filed fact (line notes: no lot's stock goes below zero, one receipt row per lot; SF27) and C1 over every repair that keeps the lots at zero or above (asserted) |
| 16 | Identity normalisation | plates in one format in both files; makes to platforms | filed (field descriptions); asserted |
| 17 | Netting against gross | ask A's returns netted | filed (the asking sentence) |
| 18 | Dimensional units | packs, modules (a Kestrel carrier 2), per cent | filed (artikelstam, the prompt) |
| 19 | Code and status semantics | OEM nieuw, Voltwerk revisie; PASS, FAIL, ABORT; AFGEKEURD | filed (log, line notes); never the stump |
| 20 | Integerisation | 60 lots by largest remainder | filed (plan section 2) |
| 21 | Clause scope | the warranty years per platform; the asks per platform | filed (warranty terms' table; the prompt) |
| 22 | Forward window contents | the cars first registered here from July 2026 to December 2027 (filed, SF25) | C1: projected from the register's own arrival history; 144 projections file one call and one total (asserted) |

## Literal reader

Executing the prompt and every filed sentence word for word (the plan's sections 1 to 3, the warranty terms, the field descriptions, the curves, the line notes): the plan's section 3 files the fleet of 2027 as the register of 30 June 2026 and the cars first registered here from 1 July 2026 to the end of 2027, each from the day it is registered, with one pack per car (the pack at the end of 30 June 2026, or the pack a later registration carries when registered, a pack fitted in its place later left out), so the register-only reading both portal judges filed violates a quotable sentence (SF25), as do the renewal and start-of-day readings (SF26). That leaves one open move on the call, a method and not a reading: how to project the later registrations, which no file can hold yet. The new cars among them are inside their warranty all year; the used imports are projected from the register's own arrival history, and every projection a competent analyst builds from it (144 cells, SF25) files the same five slots and the same total, while each cell outside that family violates a filed sentence or the register's own dates and ages. The default path's answer is what the easy method on this literal estimand files: the later registrations counted and carried as new cars inside their warranty. On ask A the line notes' lot stock rule rules out summing the replacement lots' lines as written, and every repair that respects it files the golden (SF27).

## Oracles

None on the call: no file ties only under the golden and no past split or forecast is shipped. The log lets a solver back-test, and neither back-test hands over the level: run on 2025 with the cars on the register now, the method over-forecasts the Mira city car (1,645 against the 1,519 fitted, the year's arrivals counted from January); with the cars registered by the end of 2024 it under-forecasts it (1,293), the gap the rigorous route reads as the arrivals, and a year's realised ratio does not carry to 2027 (SF22). On the asks, three referees each arbitrate a designed disagreement without handing over a level: the goods receipts (ask A, a replacement lot issued more than it received), the BMS pairings (ask B, two pakket_id values on one work order), the MES work orders (ask C, an AFGEKEURD core the line built on), with the recycler's quarantine dates agreeing.

## Ask sheet

**Ask A: the modules a lot of 50 should carry, by platform (5 figures, whole modules).** H18: the plan commits module stock with each lot; the call reads none of the line's files (asserted). Use: the module orders priced by finance. Primary device, silent (D6, an event's quantity on every line it covers): when a supplier's module lot is held, the line reworks the packs built with it together and stores books one replacement pick for the batch; the export writes the batch's quantity against every work order on that pick list (eight holds, every platform). Only a cut against the goods receipts shows it: those replacement lots issue three to five times what they received, and since the portal return the line notes file that stores keeps its stock by lot and no lot's stock goes below zero, with one receipt row per lot (SF27), which makes the natural read wrong in the record without naming a batch pick or a lot. Interior: same-day pick lists that carry equal quantities for several work orders are real (every platform), so collapsing lines alike on pick, lot and quantity over-repairs. Hazards: returns as negative issues, the Kestrel's two-module carriers, spares from the replacement lots issued later. Files: magazijn_mutaties, magazijn_ontvangsten, artikelstam, mes_werkorders, verzendingen (5 files, 12 columns). Stops: the natural read 171, 283, 195, 150, 238; the over-repair 160, 266, 178, 140, 217; issues only 173, 289, 198, 153, 238; golden 167, 274, 190, 149, 224. Realism: an ERP export joining a pick header's quantity to each linked work order line.

**Ask B: of the packs that had their first end-of-line run in the twelve months, the share that passed it, by platform (5 figures, one decimal of a per cent).** H18: the test programme committed per lot; the call reads none of it. Use: rework capacity per lot. Primary device, silent (D7, the true key elsewhere): the bench reads the pack's serial from its BMS, and seven reworks in ten after a failed run replace the BMS, so the reworked pack runs again under a new pakket_id; only the MES's BMS pairings tie the two ids to one work order. Interior: one work order in 25 replaces a BMS before the first run (two pairings, one id on the bench), and packs scrapped after failing twice. Hazards: ABORT runs (no run, the notes), packs first run in June 2025 and run again in the year (out). Files: eol_testlog, mes_bms_koppelingen, mes_werkorders (3 files, 9 columns). Stops: by pakket_id 92.3, 87.2, 94.2, 88.0, 91.3; an ABORT as the first run 91.4, 85.4, 91.4, 85.9, 90.5; golden 92.6, 88.2, 94.0, 88.3, 90.5. Realism: a bench that identifies the pack by what its electronics report.

**Ask C: the share of the cores received in the twelve months that were rejected at intake, by platform (5 figures, one decimal of a per cent).** H18: the cores to have on hand per lot, rejects included (the plan, section 5); the call reads none of it. Use: core purchasing. Primary device, silent (D2, an attribute at a later snapshot): the intake export carries each core's grade as it stands on 1 July 2026, and when the line scraps a pack (torn down beyond repair, or failing its end-of-line test twice) the core's grade becomes AFGEKEURD with the line's reason, drawn from the same reasons the docks use; only a join of the intake export's kerncode to the MES work orders (the core the pack is built on) shows those cores passed intake, and the recycler's quarantine tags agree, an intake reject's dated the day it arrived and a scrapped pack's the day the line scrapped it (every platform, 99 cores). Interior: the line also scraps packs built on cores received before the year, which the year's intake export does not hold. Hazards: both docks' rejects, cores bought in, the label's platform wording. Files: kernen_inname, mes_werkorders, afvoer_recycler, lijn_exports_toelichting (4 files, 11 columns). Stops: every AFGEKEURD row (the natural read) 12.6, 10.1, 13.2, 17.6, 12.5; every recycler line in the year a reject 12.7, 10.1, 13.6, 17.8, 12.5; after meeting the device, the scrapped cores out of both counts 9.3, 6.2, 11.2, 15.1, 8.7 and the year's scrapped work orders subtracted by count 8.8, 5.9, 10.6, 14.5, 8.3; golden 8.9, 5.9, 11.0, 14.7, 8.3. Realism: a core master whose grade field the line overwrites when it scraps the pack, exported as it stood on the pull day.

Main population zero-counts: the call reads the register, the log, the curves, the warranty terms, the plan and the field descriptions, and no line file; the asks read the ten line files and none of the call's (asserted, separation).

| Ask | Cracker (lands the call, runs the battery, executes every filed rule) | Verdict |
|---|---|---|
| A modules per lot | 0 of 5 on every path that does not meet the batch picks (natural read, over-repair, issues only, units); the filed stock rule is met only by the cut of each lot against its receipt, which is the device | miss |
| B first-run pass share | 1 of 5 at best (an ABORT as the first run lands the Tern van) | miss |
| C intake reject share | 0 of 5 on every path that does not meet the cores scrapped on the line (the natural read, every recycler line a reject) | miss |

Pair ceiling: 32.8 ((48.7 + 17.0) / 2), the cracker keeping 1 of the 15 ask figures on the call and the mirror the same on the register-only call (1 of 6 call figures, the Plover saloon's 350).
Mirror leakage: 6.7 per cent of ask weight.
Measured by: generator/pair.py on the cut pack (target.zip 7aa71d60; re-run on a89c9dea after the determinism repair, unchanged).

## Pre-ship check

- Free gates (stage 4 repair pass): generator checks 101 passed (R1 to R3c on the clean truth and on the pack, the
  standing family of seven constructions each filing the golden slots with the total in the 3,800 bin and the worst
  margin 0.263, the ladder, SF1 to SF24, the two back-tests, every ask figure's edge, the three devices with ask C's
  quarantine-date route converging on the golden, separation, the distractors unread, the bench and shipment realism,
  the input gates); verify.py 0 failures with the five documents read back; two builds byte-identical (target.zip
  a62fa349); figures_check, precut and voice-check as recorded at the gates.
- Stage 4 round 1 (on 4442d745): the leak reader filed the register-only split and 3,400 (Plover's 350 is shared by
  that rung and the golden), missed asks A and B on all ten figures and landed ask C's five through dock 2's zero
  rejects and the recycler's blank core codes; the judge returned DETERMINISTIC and APPROVE, Gate G
  analytical_non_defect, Gate H domain pass, layers pass, decisive step analytical, with three findings: the
  stay-in-use sentence as the one soft spot, dock 2's practice stated in no file, and recycler collections after the
  pull date.
- Repairs in one generator pass: ask C re-sited onto the grade's date (no graded figure moved); the stay-in-use
  sentence placed in 2027; the recycler's notes end with the 1 July 2026 collection; the reader's realism tells fixed
  (the plan rewritten as concept 3 for the operations meeting, saved by its author at revision 9; the register
  extract without its two constant columns, its filter stated in the field descriptions; the log's source column
  showing the dealer-reported fits of our packs; the item master with its superseded and repair articles; the lead
  times with the BMS boards, seal kit and carrier brackets; the price list with its other charges).
- Stage 4 round 2 (on a62fa349): the reader filed the register-only split and 3,400 again and kept 0 of the 15 ask
  figures (the natural read on all three asks); its two data tells were fixed with no figure moved (goods receipts
  numbered with the gaps of a shared sequence, the four benches coming on line one after another on the go-live
  morning), giving the shipped target.zip 7aa71d60 (101 checks, byte-identical, verify, precut 51/0/0, figures
  66/66, voice-check PASS).
- score_reader.py prints a call hit on both readers: it counts any one of the six call keys, and the one key hit is
  the Plover saloon's 350, which the register-only rung shares with the golden (the ladder); both readers filed
  that rung's split, four of five slots and the total wrong.
- leak.py REVIEW on 7aa71d60, four design-note vocabulary lines, each ruled harmless: the warranty terms state the
  first-admission clock, a filed convention on a lower rung; the price list carries prices and charges only; the RDW
  field descriptions are the publisher's field list; the plan files the estimand and the conventions and names no
  import. guard heart WARN (Gate G forecasting in 5 of the last 12; png and xlsx); containers clean; H4 the zip's 18
  members; H11 one submission and one prompt; H16 every extract ending by its pull date, the APK expiry dates as
  validity dates; H24 no generator word under target/.
- The 10/10 rules re-read against the built pack: the decisive step is the population whose packs fall due in 2027,
  the fleet as it will stand with the used imports still to arrive, which no filed rule names and which the field's
  installed-base forecast carries; the Layer 1 items move nothing (R2 asserted per item); nothing is planted (R3c).
- Pair ceiling 32.8 (cracker 48.7, mirror 17.0), mirror leakage 6.7 per cent of the ask weight; ask C's stops after
  meeting its device are printed apart (2 of 5 at most, by count).
- Open risk, stated: a reader who reads the import stream off the two registration dates and carries it through 2027
  lands the call; two stage 4 readers and the four pre-draw probes did not.
- Determinism repair after the portal return (target.zip a89c9dea, two full rebuilds byte-identical, figures.json
  byte-identical to the shipped one): generator checks 425 passed (SF25's 144 projection cells by name with the counts
  they are built from, each cell outside the family against what it violates, SF26's renewal and start-of-day readings,
  SF27's lot stock rule and its three repairs, the easy route now carrying the later registrations as new cars on the
  clean truth and on the pack); verify.py 0 failures, six SF25 cells, SF26 and SF27 recomputed on its own code path;
  figures_check 66 of 66; precut 51, 0, 0; voice-check PASS; leak.py REVIEW (five design-note vocabulary lines; the plan
  files the fleet of 2027 and one pack per car and names no import, arrival, age or warranty state of the later
  registrations, the line notes' new sentence names no batch pick or lot); guard validate 0 invalid; guard heart BLOCK
  on test.same_driver_older against task166 (v3, registered after this build shipped), cleared by a differentiation
  line on the card, then WARN as at ship; freeze.py determinism PASS. Owed before re-ship: the one re-judge and a leak
  reader, since the plan's wording changed at the decisive step.

## Tried and rejected

- Pack 1 of the prototype (2026-10-24, seed 3061) hid each imported car's pack history before its Dutch registration (the log started at the Dutch registration), so a solver could not know an import's pack state and both probes repaired it differently (sonnet calibrated the imports down by 0.74, opus modelled the abroad replacements in expectation): a fork, not the stump. The log is now the OEMs' EU-wide record plus Voltwerk's own, and a car whose pack failed outside warranty abroad is scrapped there and never imported.
- The prototype's truth carried a scrappage and export rate that no file shows; the forecast now takes a car in use to stay in use through 2027, filed in the tooling plan.
- The first cut's imports arrived about six years old, inside the eight-year warranty, and moved the call by three per cent and one lot; the Mira city car is now the platform kept alive by old imports from abroad, as old cheap EVs are.
- A refurbished pack failing inside Voltwerk's two years was logged as an OEM warranty fit in the prototype (99 rows): fixed, a Voltwerk-warranty failure takes another refurbished pack under Voltwerk's cover.
- The first stage-2 world kept the Mira city car launched in 2014 with 520 imports a month and an eight-year warranty: its arrival stream still ramped through the replay windows, so the 6- and 24-month windows spread the Mira's forecast by 51 and the total straddled a hundred bin. The Mira is now launched in 2013 with a five-year warranty and a steeper wear-out, its stream flat over the last 36 months and its imports arriving as survivors on their original packs.
- An estimand counting only failures outside both warranties left out the packs Voltwerk itself replaces under its two-year warranty, which the line supplies too; the plan now counts every failure outside the OEM warranty.
- Grading each platform's forecast paid the wrong route: the register-only route files four of the five platforms' forecasts at the nearest hundred (only the Mira moves); the prompt grades the slots and the total.
- Ask B's re-keying first moved the naive share by under 0.1 point on the Volta hatch, the new ids passing at about the platform's own rate; the BMS is now replaced in seven reworks in ten and the line seed (31062, from 750 swept) keeps every platform's natural read and over-repair outside its bin on all three asks, worst golden edge 0.155 of a bin.
- The dealer rows of the replacement log first carried plates typed with dashes; a solver who joined without normalising them filed Mira 1,350 and Volta 1,000, so that mess could move the call (dataset-generation R2) and was cut: both sources now carry the register's own plate format.
- Ask C's first device, dock 2 setting its rejects aside without scanning them (absent from the intake export, present at the recycler without a core code), was landed 5 of 5 by the stage 4 reader: dock 2's zero rejects and the blank core codes sit on the path of anyone counting rejects, and the judge found the dock's practice stated in no file. Re-sited onto the grade's date (D2): the intake export carries each core's grade on 1 July 2026, so a core the line built on and scrapped reads AFGEKEURD, and only its work order in the MES shows it passed intake; every ask C figure is unchanged.
- The plan's "a car in use in the Netherlands is taken to stay in use through 2027" read to the stage 4 reader, and to the judge as its one soft spot, as freezing the register of 30 June 2026; the sentence now places the car in 2027 ("a car in use in the Netherlands in 2027 is taken to stay in use for the rest of the year"), the population the estimand already files, and names no import.
- The portal returned the build on determinism (both judges: Gates C, D and E, underspecified_objective, A, B and G passing): the plan as shipped named the register as its only source and its only dynamics clause was about exits, so both judges forecast the register of 30 June 2026 alone (3,448, 3,500 with a judge's renewals), and a judge also summed ask A's batch lines as written. Pinning the population to the register was refused (it makes the judges' answer the golden and spends the stump), and filing the projection (a twelfth a month at the trailing rate, mix and age) was refused (rule application, CLAUDE.md rule 3). Closed instead by the WHAT at authority: plan section 3 files the fleet of 2027 as the register and the cars first registered here from 1 July 2026 to the end of 2027 (SF25) and one pack per car (SF26), the projection left open and forced by C1 over 144 projections, and the line notes file the lot stock rule for ask A (SF27); no graded or stated figure moved (freeze.py). The cost: that the later registrations are in the fleet is now readable, so the decisive rung keeps only what no sentence says, which of them fall due; the default path's answer is now the easy route's on the literal estimand (the later registrations carried as new cars).

## The determinism repair spent the stump: redesign, 2026-10-26

**The repair worked and the build still cannot ship.** All three forks closed, no method filed, every free gate green,
`freeze.py check --mode determinism` PASS, and 144 projection variants landing the committed split. Then one isolated
reader, holding only `prompt.txt` and the eighteen pack files and nothing else, reproduced the call cell for cell:
Volta 900, Kestrel 250, Plover 350, Mira 1,450, Tern 50, total 3,814 rounding to 3,800. It also reproduced the modules,
the first-pass yields and the core rejection shares.

Asked what decided its answer, it said: mainly following a rule a shipped document states, plus reading dates
correctly, and "I did not reach the answer by an analytical choice". Asked which sentence told it the decisive step,
it quoted the paragraph the repair added, together with the plan's existing pack-age sentence and the warranty
document's first-admission clause, and called them "a procedure". Asked which file exists only to help the analyst, it
named the tooling plan, because it "spells out the method".

**The diagnosis is the one `/fix-determinism` step 3 names, and it was missed at the start of the repair rather than
at the end.** The fork and the stump were the same object. Before the repair the stump was that no reader thought to
ask whether cars registered after the 30 June 2026 snapshot belong in the 2027 population; the portal's judges called
that an unpinned population, which it was. Pinning it is the only closure that makes the literal reading the golden,
and pinning it tells the reader the one thing they were not asking. The reader confirms both halves: omitting the
later registrations gives 3,400 and 1,250 Mira slots, which is the old default path, and the filed sentence now rules
that out.

**And underneath it, the decisive lever was never analytical.** The reader measured what moves its answer: taking the
warranty from the Dutch registration date instead of the date of first admission gives a total of 1,968 and 550 Mira
slots, and ignoring the logged pack replacements gives 5,752 and 1,700. Those are the two large levers, and both are
field readings. The one genuinely analytical element, extrapolating the new-registration cohort, the reader supplied
itself with an assumption of its own and still landed. So the call turns on reading `datum_eerste_toelating` rather
than `datum_eerste_tenaamstelling_in_nederland` and on applying a warranty table in which one platform alone carries
five years to the others' eight. That is data semantics plus rule application, which the client's rule 3 bans as the
decisive step whatever the determinism verdict.

**Status: back to stage 2, not re-shipped.** The repair's record closures are sound and are kept; what has to be
re-rooted is the decisive step. A pin cannot be removed to restore the stump, because the portal already failed the
unpinned version: this architecture has no position in which it is both deterministic and stumped, which is what
spent means.

**Two findings worth carrying into the redesign, from the same read.**

- **The modules ask reads as planted.** The reader called the eight over-posted pick lists out unprompted: bookings
  stepping through 07:05, 07:06 and so on, identical quantities repeated per work order, each lot's receipt equal to
  one copy plus the later small issues. `supplemental-stumping` law 1 and law 7 forbid exactly that signature. The
  device should survive, the regularity should not.
- **Realism tells across the pack.** Bookings stepping on exact consecutive minutes, life curves smooth to four
  decimals, round lot sizes (600, 1,200, 300), recycler weights banded per platform, and the register extract with
  "no real-world noise". That is a `golden-realism` sweep owed on the next cut.


- The determinism repair itself, as a way to keep this architecture: refused on measurement after the fact. The three
  record closures hold and no method was filed, but the fork and the stump were one object: the only closure that makes
  the literal reading the golden is a population pin, and that pin tells the reader the question they were not asking.
  One isolated reader then landed the call cell for cell and said it got there by following filed rules and reading
  dates, not by an analytical choice. `/fix-determinism` step 3's stop condition, read at the start of the repair
  rather than the end, would have sent this to stage 2 without the repair being built.
