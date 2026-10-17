# task152: Hadley Ranch Solar, the 2027 forward sale at the one-year P90 after the module replacement (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC23. The seed (a corporate buyer's 40 MW solar plant,
hedged a year ahead at the one-year P90, its original modules replaced on the same racking and inverters, the work
finishing in December) was read at its header and Situation only. Its world, decision and quantity are kept. Its desk
memo, which files the P90 method (25 weather years, a performance ratio calibrated on five years, the sample standard
deviation), is not shipped: filing how the decisive figure is computed is rule application. The pitfall is re-found
from how a solar plant's monitoring records come to exist: the inverters log the DC energy the array delivers and the AC
energy they put out, the pyranometer logs the irradiation the array receives, and the array between them carries both
its modules' own wear and the dust it gathers between washes, which the washes clear and the months between them
rebuild.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task152.json`, architecture v1, registered 2026-10-16; `guard.py check` WARN (overuse.objective), answered below; the older same-driver signature (time, G4, decomposition_attribution) against task232 differentiated on the card, with lines against task127 v2, task187, task132, task185, task460, task136, task260, task30 and task68; nearest drivers 0.04 (task459, task230 v3, task132) |
| Domain / task type | `energy-systems-utilities` (client domain), task type `asset-condition-maintenance` (serves Forecasting): what an asset's condition is now, what a maintenance action restores and what the asset will produce after it. The seed's label (Economics, corporate energy procurement) is a backdrop the taxonomy places elsewhere |
| Objective | Forecasting & Predictive Modeling: the plant's 2027 energy at its one-year P90, a calendar year not yet begun, built from the plant's own monitoring history and the long-term irradiance record |
| Shape | `single-figure`: the volume sold forward with the P50 and standard deviation it rests on, the note's chart of the 25 weather-year outputs, and two row-set asks (16 inverters, 10 years); criteria counted in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (MWh, rounded down to the nearest 1,000) |
| Mechanism | gap time (decisive: the plant's record is a statement about its original modules under a wash regime that changed; the sale bets on new modules under today's regime) with population (which part of the record's decline belongs to the part replaced); pattern none; generators G4, G16, G13; Gate G `decomposition_attribution`; strategy `decomposition_attribution` |
| Layer 2 family / pattern | `estimation_fit` (decomposition: a soiling loss, an inverter loss and a wear loss read apart, the way PV degradation studies read them); `own:module-wear-net-of-soiling-at-the-inverter-dc-boundary` |
| Furniture | forum `executive_team` (the treasurer approves the volume, policy section 5.1), forcing event `purchase_order_or_contract` (the 2027 forward sale confirmation), organisation family `manufacturer`, role family `procurement_lead`, context artifact `operations_log` (Tresco's work orders, which carry the washes, and the inverters' event log; the SCADA exports are the spine), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the plant SCADA's daily exports: the original system's wide daily report to March 2, 2020 (1,562 days, 16 inverters by DC, AC and operating hours) and the replacement system's long export from March 3, 2020 (127,359 device-point-day rows), with the met station's plane-of-array irradiation and irradiance-weighted module temperature and the revenue meter's export and import (constructed) |
| Deliverables | `hedge_volume_2027.xlsx` (volume, P50, standard deviation, the build, the weather years, the two ask tables, notes) and `hedge_note_2027.pdf` (a one-page memo to the treasurer with the weather-year chart); the format set rotates away from task151 (docx), task150 (png) and task148 (png) |
| People | drawn with `guard.py names --geo "United States" --seed 152` (first names and surnames checked clean): Kristopher Lara (energy and commodities manager, the note's author; not in the prompt), Selena Sloan (solar asset manager, the README and the scope), Caroline Barnett (treasurer, the policy and the approval), John Davila (Tresco site supervisor), Laurie Howell (Corvane's field test engineer), Isabel Shaw (the district's meter data analyst, on the card only), Felicia Powers (Westmark's origination director, the confirmations), Ruben Yang and Howard Stout (Tresco technicians, user names in the work orders and event log), Sonia Whitehead (Tresco control room, user name) |

**Guard.** At the draw: WARN `overuse.objective`, `repeat.decision` and `repeat.question_form` (task151), answered: this
is the Forecasting lane, and task151 shares no other axis. At stage 3 `guard.py check` raised a new BLOCK, `ban.forum`
against task233, whose card was registered before this one but reached this worktree only with the DRAWN push; the forum
was redrawn from `committee_or_panel` to `executive_team` (the policy now has the treasurer approve the volume) and the
check is back to WARN `overuse.objective` alone. The pull at the PAUSED push brought task189 (registered before this card, a
`monitoring_export`), and `ban.artifact` blocked; the context artifact was redrawn to `operations_log`, the work orders
and event log the build already ships, and the check is WARN again. At the round-2 hardening the cards pulled since
(task151, task190, task464) were read and the check stays WARN `overuse.objective`. A persona first drawn for Westmark (first name in task41) was replaced
from the same seed's list. `guard.py surface` promotes one pair, task232, on the card signature already differentiated
(surface 0.083, corpus percentile 68); the people sweep reads two plant names (Hadley Ranch, Red Tank) as persons, not
added to the card. `guard.py heart`: WARN, nearest 0.07 (task132's ledger row).

**Same-puzzle and same-driver tests.** Gap time, decisive G4, decision `quantity_figure`, Gate G
`decomposition_attribution`: no build in the last twelve carries either triple; the one older same-driver match, task232,
carries its differentiation.

**Abstraction test.** Stripped of nouns: the forward level after a worn part is replaced is the present output restored
by the part's own wear only; that wear is the decline of the unit's just-reset states read at the boundary inside the
unit that leaves out the losses the replacement keeps, because the average output also carries a loss that accumulates
between recurring resets and whose mean grew as the resets grew rarer. The nearest by mechanism, read for latent
structure rather than score:
- task127 v2 removes the replaced step's excess over a concurrent wait (a max of parallel steps found by joining two
  logs); here the losses are a serial chain and one of them cycles.
- task187 ranks units on a shortfall read at matched turbulence; here one unit's level is rebuilt after a swap, and
  nothing is ranked.
- task132 forecasts failures through a renewal process; here the restart is given and the question is which of the
  old losses it clears.
- task46 carries a rate stationary in cumulative exposure; here no rate is carried, a level is split.
- task185 converts a history across an instrument change at the value converted; here no history is converted.
None shares the latent structure, the default path and the correction.

**Data-native sentence.** Hadley Ranch's inverters log, every day, the DC energy its 128,000 original modules delivered
and the AC energy they put out, beside the irradiation the pyranometer saw: the DC energy per unit of irradiation falls
for two reasons the daily figure cannot tell apart, the modules' own wear, which only rises, and the dust the array
carries between washes, which each full wash clears and the dry months rebuild, and which grew as the washes fell from
six a year to one; the wear is the decline of the freshly washed days alone, and the module replacement clears it while
the dust regime, the inverters' lost efficiency and their lost availability stay.

**Sources read, one line each.**
- `guard.py mechanisms --objective forecasting` (63 builds): the nearest spent ground is renewal after replacement
  (task132), a rate in constructed exposure (task46), a shortfall at matched conditions (task187) and a removed step's
  excess over a kept one (task127 v2); none splits one unit's decline across an internal boundary and a reset cycle.
- The kinship cards the brief names: task136, task460, task185, task260, task30, task68. The seed's own mechanism, a
  gain measured side by side, is kept only as a shipped measurement; the decisive step is what the gain multiplies.
- `two-layer-task-design.md`: "the data's real structure" and "the right comparison" are the client's frames.
- `layer2-rigor-patterns.md`: Energy Systems & Utilities has no patterns; the general statistics lines were read.
- task148's design note and its `## Tried and rejected` (the one-scalar calibration family that landed its call): here
  the history-calibrated family is swept window by window and every natural window misses (`## Ladder`).

**World.** Marden-Vail Building Products (fictional), a Phoenix maker of gypsum wallboard and joint compound, owns
Hadley Ranch Solar (fictional), a 40 MWac fixed-tilt plant in Pinal County (commercial operation November 20, 2015):
sixteen 2.5 MW central inverters, each fed by 8,000 Kellerman KS-315P modules (40.32 MWp), on south-facing tables at 25
degrees. It exports at 69 kV to the Vado Seco Irrigation and Power District (fictional); the output is sold at Palo
Verde, each calendar year forward at the one-year P90 under the treasury's energy risk policy, the treasurer approving
the volume. Tresco Field Services (fictional) has run operations and maintenance since commercial operation, under the
current agreement from 2021. The original modules lost power fast from mid-2017 to mid-2020 and slowly since; the 2019
survey found cracked backsheets. The inverters' maker left the US market in 2018 and each failed power stage was replaced with
a refurbished one, which runs with higher losses; inverter 07 burned in March 2021 and was replaced under a new tag.
Tresco washed six times a year to 2018, in the cool months (January to April, October and November; never in the summer
heat). Drought restrictions on the plant's well then cut the washes to four in 2019, two in 2020 and, under Schedule 2
of the 2021 O&M agreement, one each December, a block a week, the well's permitted weekly draw covering one block's
wash. In April 2024 the district retired the 12 kV station-service supply and the auxiliaries moved behind the
revenue meter. From October 2025 to September 2026 Corvane Solar (fictional) ran a side-by-side comparison in block 3:
a table of new CV-450BHC bifacial modules beside a table of unexposed KS-315P spares, both washed weekly. The
replacement (82,944 CV-450BHC modules, 288 strings of 18 per inverter, 37,324.8 kWp) runs from October 5 to December 18,
2026 on the same tables, cabling and inverters.

## Default path

Built figures (`generator/checks.py`).

1. Read the energy risk policy: the volume is the one-year P90 of the plant's 2027 net energy at the delivery point,
   the P50 less 1.2816 standard deviations over the full calendar years 2001 to 2025 of the long-term record, rounded
   down to the nearest 1,000 MWh; the base period is the twelve complete months before the sale.
2. Join the two SCADA layouts and take the plant's performance ratio over October 2025 to September 2026: net export
   over plane-of-array irradiation times the original 40,320 kWp (63.7 per cent).
3. Carry it onto the new modules with the side-by-side report's measured gain per kWp (14.7 per cent) and the new
   nameplate (37,324.8 kWp).
4. Run the 25 weather years' plane-of-array irradiation through it, take the mean and the sample standard deviation,
   and strike the P90 (60,891 MWh).

Ends on: a volume of 60,000 MWh (P90 60,891, 14 per cent under the golden).

Golden: a volume of 70,000 MWh (P90 70,620; P50 73,000; standard deviation 1,900): the same base period's performance,
restored only by the original modules' own wear (14 per cent: the inverters' DC input per kWp per unit of irradiation,
temperature-corrected, on fully available inverter-days 1 to 3 days after each block's wash, December 2025 against
2016), then the gain, the new nameplate and the weather years.

## Stump sentence

Carrying the plant's last twelve months' performance ratio onto the new modules with the side-by-side gain and running
the 25 weather years files 60,000 MWh against the golden 70,000; the step that lands it there is treating the plant's
present performance as the repowered plant's, when the original modules' own wear leaves with them; and restoring the
plant's whole decline since 2016 (76,000), its whole DC-side decline (73,000) or its decline after washes read at the
inverters' AC output (72,000) overshoots, because the inverters' lost efficiency and availability and the dust the array
carries between washes, which grew as the washes fell from six a year to one, stay with the plant: only the wear read on
the days after each wash at the inverters' DC input restores what the replacement removes.

## Three rules

- **Task type:** energy-systems-utilities, asset-condition-maintenance (serves Forecasting): what the plant's assets are
  worth in energy after a maintenance action, the module replacement, forecast for calendar 2027 from the plant's own
  monitoring history and the long-term irradiance record.
- **Domain test:** the deciding quantity is the repowered plant's 2027 performance level, which a solar asset analyst
  builds by separating the losses the module swap removes (the original modules' wear) from those it keeps (inverter
  efficiency and availability, and soiling under the cleaning contract), with the wear measured the way PV degradation
  studies measure it, at the DC side, temperature-corrected and on clean-module days, then run over the long-term
  plane-of-array record for the one-year P90.
- **Swap:** "how much of next year's flights a re-engined fleet can sell forward" keeps a part replaced and a decline in
  the record, but plane-of-array irradiation to normalise by, an inverter boundary that splits the DC losses from the AC
  losses, dust that a wash clears and the dry months rebuild, and a P90 struck over weather years have no counterpart,
  so what sets the forward level stops making sense.
- **Layer 1:** the SCADA replacement of March 2020 (the original system's wide CSV in local days and kWh with inverters
  01 to 16; the replacement's long export in UTC day starts and MWh with block-inverter tags); the original server's
  three lost days in 2018; inverter 07 replaced in 2021 under a new tag; the long-term record hourly in UTC under a
  header block; the work orders as free text, washes block by block among every other job; the station service moved
  behind the revenue meter in April 2024; the side-by-side report and the interruption report as PDF tables, the scope
  as a Word paper; the district's legacy fixed-width billing export and its meter data system with a history load and
  versioned reads. Each is what these systems write; none carries the stump (asserted per item, R2a to R2g).
- **Layer 2:** `estimation_fit` (decomposition): the plant's decline is a product of a monotone module wear, a soiling
  loss that the washes reset and whose mean grew as the washes grew rarer, and inverter losses on the AC side and in
  availability; the replacement removes only the first, so it is read apart from the others the way PV performance
  studies read soiling and degradation apart.
- **Decisive step:** measure the original modules' wear as the decline, from 2016 to the base period, of the inverters'
  DC input per kWp per unit of plane-of-array irradiation, temperature-corrected to 25 degC, on fully available
  inverter-days just after each block's wash, and restore the base period's output by that wear alone before the
  measured gain and the weather years are applied.
- **Not semantics:** every field (DC energy, AC energy, operating hours, irradiation, module temperature, the work
  orders' wash entries) and every filed definition (the P90, the volume's basis, the base period, the rounding, the
  cleaning schedule) is read the same way by the easy routes; no field, code or definition says which part of the
  decline is wear, and the default path and its refinements read them all and still file 60,000, 72,000, 73,000 or
  76,000.
- **Not rule application:** the shipped sentences that bear on how the figure is computed (the policy's P90, base period
  and volume sentences, the scope's capacity and its statement that the inverters stay, Schedule 2's one December wash a
  year, the report's measured gain) are executed word for word in `checks.py` (R3c): their only literal product is the
  base period carried with the gain, 60,000, never the golden; no filed sentence says which part of the decline the
  replacement removes or where to read it.
- **Analyst test:** a strong analyst who joins the two SCADA layouts, reads the policy, the scope, the O&M agreement
  and the side-by-side report correctly and runs the 25 weather years carries the base period's performance ratio onto
  the new modules with the report's gain and files 60,000 MWh; restoring the whole decline since 2016 files 76,000, the
  whole DC-side decline on available days 73,000, and the decline after washes read at the AC output 72,000 (executed
  on the clean truth: 60,756 against the golden construction's 70,456, both in their bins).
- **Estimand:** the energy risk policy (sections 3.1, 4.1, 4.2, 4.4) and the prompt: the one-year P90 of the plant's 2027
  net energy at the delivery point, the P50 (the mean of the plant's annual energy, as it will stand in 2027, under the
  weather of each full calendar year 2001 to 2025 of the long-term record) less 1.2816 sample standard deviations of
  the same energies, built from the plant's own monitoring record with the twelve complete months before the sale as
  the base period, rounded down to the nearest 1,000 MWh; the population, outcome, window, unit and rounding are filed,
  the method is not.
- **No decoy:** no vendor energy estimate, consultant study, prior-year hedge memo, desk draft or stakeholder figure
  states or argues a 2027 volume, a performance ratio for the repowered plant or a wear figure (R3c asserts no document
  carries one); the side-by-side report states its measured gain and says nothing about the plant.
- **No certified replay:** no certified or published figure for the repowered plant ships and nothing graded is
  reproduced; the desk's past volumes come from estimates no shipped file reproduces; Tresco's repowering summary gives
  five other plants' energy changes without a method (a distractor, asserted to miss at 65,457).
- **Lesson:** when part of an asset is replaced, the forecast restores only that part's own deterioration, measured where
  the losses the asset keeps separate out (here the inverter boundary) and on the days a recurring cleaning has reset the
  loss that cycles; the asset's whole decline mixes in losses the replacement keeps, which here grew as the cleaning grew
  rarer, and carrying the present output forward keeps a wear the replacement removes; no build on file teaches the split
  of one unit's decline across an internal boundary and a reset cycle.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Built figures.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the base period's performance ratio carried onto the new modules with the gain (60,000) | no | no | yes (a forecast from recent performance) | no | no | yes (one ratio) | readable |
| R0b the same on the new nameplate without the gain (53,000), or a recent window's ratio (60,000 to 61,000) | no | no | yes | no | no | yes | readable |
| R1 the plant's whole decline since 2016 restored: the first year carried with the gain (76,000); on the nameplate alone 66,000 | no | no | yes (repowering restores the plant) | no | no | yes (one ratio) | readable |
| R2 the whole DC-side decline on available days restored, inverters kept (73,000) | no | yes (the DC energy column) | yes (inverters stay, so measure at the DC side) | no | no | no | readable |
| R2b the decline after washes read at the inverters' AC output restored, soiling kept, inverter losses restored (72,000) | no | no | yes (the soiling-aware degradation analysis on AC energy) | no | no | no | readable |
| R2c a degradation rate times the plant's age: the year-on-year median (66,000), the last five years' trend (62,000), the warranty's rate (66,000), a round 1 per cent a year on the warranty's schedule (69,000) | no | no | yes (a degradation rate times age) | no | no | yes | readable |
| R2d the decline after washes without the temperature correction, at the DC input or the AC output, mean or median, or the plant's meter in the week after each wash (67,000 to 69,000) | no | yes (the energy columns) | yes (a soiling-aware read that skips the weather) | no | no | yes (one ratio) | readable |
| R3 (decisive) the wear read on the days after each block's wash at the inverters' DC input, temperature-corrected, the base period restored by it alone (70,000) | no (the policy files the estimand and the base period; the scope and the O&M agreement file what stays; nothing names the wear, a wash cycle or a boundary) | no (no column holds a soiling, wear or loss figure; no flag marks a clean day; the work orders log washes as free text among every other job) | no (the reflexes are recent performance, restoring the decline, measuring at the DC side, a soiling-aware AC analysis, a rate times age) | no (no forecast, model output or study of the repowered plant ships) | no (the battery is clean on it) | no (a split of a decline across two cuts of the record, then a ratio) | silent |

## Semantic fork table

Every term of the main ask and every convention the main computation needs, each asserted in `generator/checks.py`
under its id. Which part of the decline the replacement removes is the decisive step, a split the data force (the
inverter boundary and the wash cycle), never a reading.

| SF | Term or convention | Golden reading | Alternatives | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | 2027 | calendar 2027 | the company's fiscal year | other volume | the policy, section 2.1 ("The hedge year is the calendar year") |
| SF2 | the one-year P90 | the P50 less 1.2816 standard deviations | the empirical tenth percentile (70,145) | same call (70,000) | the policy, section 4.2 |
| SF3 | the standard deviation | the sample standard deviation | the population standard deviation (1,885) | same call (70,000; 1,900) | same call |
| SF4 | the weather years | the full calendar years 2001 to 2025 | 2026's months added | ruled out | the policy, section 4.2 ("each full calendar year") and the record's header |
| SF5 | the energy | net energy at the delivery point (revenue meter export less import) | the inverters' gross AC (72,000) | ruled out | the policy, section 3.1 |
| SF6 | the plant in 2027 | 37,324.8 kWp of CV-450BHC on the same tables and inverters, under the O&M agreement to 2027 | the original array; another cleaning schedule | ruled out | the scope ("What is replaced", "What stays") and Schedule 2 |
| SF7 | the base period | the twelve complete months before the sale, October 2025 to September 2026 | calendar 2025; the last 24 months; the one-wash years averaged | same volume (70,000 on each); ruled out for the P50 | the policy, section 4.4 |
| SF8 | the as-new reference | 2016's washed days | commercial operation to 2016 or 2017; the first twelve months; the handover wash; 2016 and 2017; 2016's winter washes against December | same call (70,000; 73,000; 1,900; C3) | same call |
| SF9 | a freshly washed day | 1 to 3 days after the block's wash, full operating hours | 1 to 1, 1 to 2, 1 to 5, 2 to 3, 2 to 4 days; full hours within 0.05 h | same call (C3) | same call |
| SF10 | the temperature basis | the irradiance-weighted back-of-module temperature (T_MOD_IW) at the KS-315P's -0.42 %/degC | NOCT cell temperature from the daily air temperature; a coefficient fitted on the record (each period's regression at 25 degC or at the base period's temperature, one slope for both periods, 2016's slope) | same call (C3: 70,329 to 70,690; P50 72,784 to 73,157) | same call; the Sandia model needs hourly wind, which ships for 2025 only |
| SF10b | the temperature basis | as SF10 | an uncorrected comparison (67,000 to 69,000) | ruled out | the README's field definition and the datasheet's coefficient of Pmax; the base period's post-wash days run 9 degC cooler than 2016's |
| SF11 | the measured gain | the twelve months' DC energy per kWp, table B over table A | the stated 14.7 per cent; the mean of the monthly ratios | same call | same call |
| SF12 | the gain's first year | the test's modules were new at its start, so its gain carries their first year; 2027 is the repowered array's first full year | a later-year gain | ruled out | the report, section 2 |
| SF13 | the new nameplate | 37,324.8 kWp | a flash-tested power | ruled out | the scope; no flash list ships |
| SF14 | clipping | immaterial: the original array's highest hour is 91.3 per cent of rating; the repowered array reaches its rating in one cloud-edge hour of the 25 years (101.3 per cent, April 2014, 0.0006 per cent of that year) | an hourly clipping loss | same call | same call |
| SF15 | the delivery point | the 69 kV revenue meter, the district's service point 0417, which the SCADA's PLANT-RM reads | the SCADA's read | same call for the call (agree within 0.004 per cent in every month of the base period); the asks take the district's files | the exhibit (C.1.2) and the README ("the meter of record") |
| SF16 | the long-term record's basis | the provider's site-adapted series | a raw satellite series | ruled out | the policy, section 4.3, and the record's header |
| SF17 | the layouts | both: 2016 in the original, the base period in the replacement | one layout | same call | the README |
| SF18 | the replaced inverter | inverter 07 continued by B2-INV3R | dropped | same call (asserted, R2b) | the crosswalk |
| SF19 | rounding | the volume down to the nearest 1,000 from the unrounded P90; the P50 to the nearest 1,000; the standard deviation to the nearest 100 | the volume to the nearest 1,000 (71,000) | ruled out | the policy, section 4.1, and the prompt |
| SF20 | the weather-year energy | the repowered plant's performance level times that year's plane-of-array irradiation | a temperature-adjusted level per year | same call (the record carries irradiance only) | same call |
| SF21 | the volume's rounding path | down from the unrounded P90 | the rounded P50 less 1.2816 rounded standard deviations (70,565) | same call | same call |

## Ladder

Built figures; P90 in MWh, the golden's floor bin 70,000 to 71,000 (the P90 at 70,620, 0.38 of a bin from the top edge).

| Rung | Construction | P90 | Volume | Dies to |
|---|---|---|---|---|
| 0 | the base period's ratio, the gain, the new nameplate | 60,891 | 60,000 | the original modules' own wear leaves with them: the DC input per kWp per unit of irradiation after each wash fell 14 per cent from 2016 to December 2025 |
| 0b | the same on the nameplate alone | 53,069 | 53,000 | the side-by-side report's gain and the wear |
| 1 | the first year carried with the gain (the whole decline restored) | 76,520 | 76,000 | the inverters' AC-to-DC ratio fell about 2 points as power stages were refurbished, their outages grew, and the dust carried between washes grew as washes fell from six a year to one; the plant keeps all three |
| 1b | the first year on the nameplate alone | 66,690 | 66,000 | the gain and the kept losses together |
| 2 | the whole DC-side decline on available days restored | 73,481 | 73,000 | the DC-side decline carries the soiling growth: on the days after each wash the decline is 14 per cent, on every available day 17 |
| 2b | the decline after washes read at the inverters' AC output restored | 72,191 | 72,000 | the inverters' conversion losses stay |
| 2c | a rate times age: year-on-year median, last five years' trend, the whole record's trend, the warranty | 66,687; 62,100; 76,780; 66,952 | 66,000; 62,000; 76,000; 66,000 | the wear was fast from mid-2017 to mid-2020 and slow since; no rate carries it |
| 2d | the decline after washes without the temperature correction: at the DC input (mean 67,814, median 68,071, ratio of sums 67,950), at the AC output (mean 69,323, median 69,557), December 2025 against 2016's winter washes (69,551), the plant's meter in the week after each wash (68,442) | 67,814 to 69,557 | 67,000 to 69,000 | the base period's post-wash days run 9 degC cooler than 2016's (31 against 41), 4 per cent at the datasheet's -0.42 per cent per degC; no reading at the AC side or the meter offsets it |
| 2e | a round rate times age, straight or on the warranty's schedule, at the base period's middle or at the sale: 0.5, 0.8, 1.0 and 1.5 per cent a year | 64,218 to 73,643 | none in 70,000 | the measured wear, 14 per cent, falls between 1.0 per cent a year on the warranty's schedule (69,086 and 69,492) and 1.5 per cent a year straight (72,097 and 72,763) |
| 3 (decisive) | the wear read on the days after each wash at the DC input, temperature-corrected, the base period restored by it alone | 70,620 | 70,000 | |

**The history-calibrated family** (task148's one-scalar route: a window's ratio carried with the gain or on the
nameplate), every natural window asserted to miss: the whole record 66,079; 2016 to 2025 66,356; the original SCADA's
years 73,384; the replacement SCADA's 61,370; the one-wash years 61,113; the last five years 61,138; the last three
61,212; 2025 60,691; the first twelve months 76,505; the six-wash years 74,940; the years before one wash a year 71,459
(the nearest, 459 MWh outside); on the nameplate every window between 52,895 and 66,678. The windows that land are
unmarked middle spans (2017 to 2020, 2018 to 2019) that no document, event or regime boundary marks; a solver has no
reason to carry them.

**Other rivals asserted to miss:** the plant's DC energy per kWp against the report's table A over twelve months
(77,382) or in its best month (73,366), the reference table's single-string basis sitting 2.4 per cent above an array's;
Tresco's mean repowering uplift on the base period (65,457). Every rival is asserted at least 300 MWh outside the
golden's bin; the nearest sit 443 (the AC output's median after the washes, uncorrected), 449 (December against 2016's
winter washes, uncorrected) and 508 (1 per cent a year on the warranty's schedule at the sale) outside.

**The corridor of the golden construction** (C3, asserted on the volume, the P50 and the standard deviation, each at
least 200 MWh inside its bin): the days after the wash (1 to 1: 70,714; 1 to 2: 70,686; 1 to 5: 70,630; 2 to 3: 70,572;
2 to 4: 70,624); the estimator (inverter by inverter 70,619; the median 70,603; the ratio of sums 70,601; full hours
within 0.05 h 70,632; the top 1 per cent envelope 70,507; a line through the one-wash years' levels 70,682; the last two
December washes 70,512); the reference (commercial operation to 2016 70,612; the first twelve months 70,612; the
handover wash 70,566; 2016 and 2017 70,357; commercial operation to 2017 70,372; December 2025 against 2016's January and
November washes 70,623, January alone 70,704, November alone 70,542); the temperature correction (the datasheet's
coefficient in its first-order translation form to 25 degC 70,344, to the base period's mean temperature 70,412, to
2016's 70,516; NOCT from the daily air temperature 70,340, its median 70,489; a regression on module temperature in each
period at 25 degC 70,690 or at the base period's mean temperature 70,678; one slope for both periods on log yield 70,660
or on yield at 25 degC 70,329; 2016's fitted coefficient 70,677; a regression on the NOCT temperature 70,502). The
corridor spans 70,329 to 70,714 and its P50s 72,784 to 73,182, the nearest 284 MWh from an edge. The Sandia
module-temperature model needs hourly wind, which ships for 2025 only, so it cannot be run for the 2016 reference. One
standard error on the wear and the gain together: 70,384 to 70,855. The base-period variants the policy rules out still
keep the volume (70,388 to 70,719). Counting the wash day itself as clean misses (71,104): the work orders show each
block washed until mid-morning.

**Position and margin:** the golden sits between rung 0 and rung 1, which bracket it; every rival lands in another floor
bin at least 300 MWh outside the golden's (asserted), the expert's AC-side route 1.6 bins over. P50 73,084.5 rounds to
73,000 with 415 MWh to its nearer edge; the standard deviation 1,923.4 rounds to 1,900 with 26.6 MWh to its edge (the
population standard deviation 1,884.5 with 34.5).

**Strength:** a solver lands the call only by splitting the decline three ways (the wear from the dust by the wash
cycle, from the inverters by the DC boundary) and correcting for the 9 degC between the base period's post-wash days and
2016's. Estimated chance one strong solver lands it 0.10 to 0.12, both of two 0.01 to 0.02. The routes the round-1
audit found landing by cancelling errors (temperature-blind reads after the washes at the AC output or the meter, the
uncorrected DC median, 1 per cent a year on the warranty's schedule) now file 67,000 to 69,000, each asserted 300 MWh or
more outside the bin (443 the nearest); the only round rates that land (1.2 to 1.3 per cent a year) are no default.

**Dominance and worth:** the decisive step moves the P90 from rung 2's figure down by the soiling growth and from rung
0's up by the wear; it carries the call, the P50 and the chart's level, so a response off it misses all three.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the plant's 2027 net energy at the delivery point, with the repowered array under the current O&M agreement | filed (the policy 3.1 and 4.2; the scope; Schedule 2); C1 on the layouts and the replaced inverter (SF17, SF18) |
| 2 | Unit of account | MWh of net energy at the delivery point | filed (the policy 3.1) |
| 3 | Attribution window | calendar 2027; the weather years 2001 to 2025 | filed (the policy 2.1 and 4.2) |
| 4 | As-of dating | the monitoring history to September 30, 2026; the long-term record to December 31, 2025 | filed (the README and the record's header) |
| 5 | Version basis | the provider's site-adapted series as last delivered; the report's issue 1 | filed (the policy 4.3; the report's header) |
| 6 | Denominator | the 25 annual energies, the sample standard deviation | filed (the policy 4.2); C1 (SF3) |
| 7 | Weighting | every weather year once | filed (the policy 4.2) |
| 8 | Window length | the base period, the as-new year, the days after each wash | filed (the policy 4.4); C1 across the as-new and wash-day windows (SF8, SF9) |
| 9 | Boundary inclusivity | the hedge year whole; the P-values over whole years | filed |
| 10 | Rounding path | the volume floored once to 1,000 from the unrounded P90; the P50 to 1,000; the standard deviation to 100 | filed (the prompt; the policy 4.1); asserted |
| 11 | Tie-break | none: a single figure | not applicable |
| 12 | Maturity and censoring | the base period complete; the record's years complete | asserted (no missing SCADA day in the base period; 2026 not in the record) |
| 13 | Order of operations | the performance level, then the weather years, then the P-values | C1 (the level scales every year alike) |
| 14 | Row order | the exports' order | C1 (the computation sorts by day) |
| 15 | Duplicate resolution | the two SCADA layouts meet on March 3, 2020 with no day in both | asserted |
| 16 | Identity normalisation | inverter numbers to block tags at the SCADA replacement; inverter 07's new tag | C1 (asserted, R2b) |
| 17 | Netting against gross | net export: delivered less received | filed (the policy 3.1) |
| 18 | Dimensional units | the original SCADA in kWh, the replacement in MWh; irradiation in kWh/m2 a day, the record hourly in W/m2 | the README and the record's header |
| 19 | Code and status semantics | operating hours; the work orders' job types | the README; never the stump |
| 20 | Integerisation | none | not applicable |
| 21 | Clause scope | Schedule 2 to December 31, 2027; the scope replaces the modules only | filed |
| 22 | Forward window contents | 2027 holds the repowered array under Schedule 2's December wash, a block a week, and the existing inverters; the scope keeps the December 2026 wash, so 2027's dust cycle is the base period's | filed (the scope; Schedule 2); asserted (AX22, AX23) |

## Literal reader

Executing the prompt and every filed sentence word for word fixes the population (the plant's 2027 net energy at the
delivery point, the policy 3.1 and 4.2), the outcome and its P-values (4.2), the weather years (the record's full years
2001 to 2025), the base period (4.4), the plant as it will stand (the scope and Schedule 2) and the rounding; each term
has one reading or readings that file the same volume (the fork table). No sentence says how the repowered plant's
performance level follows from the record: whether the base period carries forward as it is, with its whole decline
restored, with its DC-side decline restored or with only part of it, is HOW, and the data's structure forces it (on the
days after each wash the DC input per unit of irradiation falls 14 per cent from 2016, on every available day 17; the
AC-to-DC ratio and the availability decline on their own; the scope keeps the inverters and the December wash, and
Schedule 2 keeps one wash a year). The easy answers come from easy methods on the same literal estimand, never from
another reading; the filed sentences executed alone give only the base period carried with the gain (60,000).

## Oracles

- The SCADA history itself: no performance ratio, wear or soiling figure is stated; every split is built from it.
- The side-by-side report: one measured gain of the new modules over unexposed originals, the same under every basis
  the call could take (it multiplies every construction alike); its absolute specific yields sit on a single string's
  basis and no route through them lands (77,382 over twelve months, 73,366 in the best month).
- The work orders: washes among every other job, as free text; no soiling or yield figure.
- Tresco's repowering summary (a distractor): five other plants' energy changes; their mean on the base period misses
  (65,457). No forecast, model output or study of Hadley Ranch's repowered output ships: none for the call.

## Ask sheet

**Main call's declared row population:** the two daily SCADA exports, the CLN work orders, the long-term record, the
side-by-side report, the scope, the policy, the datasheet and Schedule 2. Device and hazard rows in it: 0 (asserted: the
daily export holds every 2025 inverter-day whole, its AC sums matching the registers across the 652 hourly rows the
loggers dropped). The asks read files the call never reads (the 2025 hourly export, the met station's hourly file, the
event log, the interruption report, the district's account exports and service points, the blotter, the confirmations,
the metering exhibit) and the work orders' OWN and CM rows. Neither ask is keyed to the call, and they share no primary
device or path.

**Ask A. Each inverter's 2025 availability as the O&M agreement defines it** (16 figures, per cent to two decimals;
96.70 to 99.82).
- H18 home: the inverters stay with the repowered plant and their outages are one of the losses the base period
  carries into 2027; the note says so, and the table is its audit trail. The call reads the kept losses from the
  plant's energy, not from the contract's hour count.
- Construction: Production Hours are the 2025 local hours whose mean plane-of-array irradiance at the met station is at
  least 50 W/m2 (3,981 a year); Unavailable is a Production Hour with no AC energy, unless the cause is the district's
  outage or a stop the owner requested; Availability is one less Unavailable over Production less Excluded (Schedule 4).
- Primary device A1 (D9, one alarm code, two causes): the district's 69 kV interruptions and the inverters' own AC
  relay trips both raise `F-217 AC GRID FAULT`. Excluding every F-217 hour credits the relay trips (every inverter has
  one or more in 2025). Fair: each interruption takes all sixteen inverters down within the minute and sits in the
  district's report; each relay trip takes one inverter and has a technician's reset in the CM work orders.
- Device A2 (D4, absence as the signal): the four block loggers dropped 652 inverter-hours in 25 gaps; the inverter's
  AC register at the next row shows the energy delivered across the gap. Counting a missing hour as no AC energy pulls
  every inverter low. Fair: no gap overlaps an outage (asserted).
- Hazards: HA1 the event log in UTC; HA2 the S-020 stop code shared by the owner's requests and the technicians'
  lockouts, only the OWN work orders naming the owner's; HA3 power-stage derates, in which the inverter delivers energy;
  HA4 the hourly AC file stamped at each hour's end in UTC against the met station's hour beginning in Arizona time.
- Stops (built, each a complete pipeline, misses of 16): S1 every zero or missing hour unavailable, nothing excluded,
  16; S2 every F-217 hour excluded, missing hours as zero, 16; S3 the district's outages excluded, missing hours as
  zero, 16; S4 every F-217 hour excluded, gaps read through the register, 16; S5 the event log read as local time, 16;
  S6 every S-020 stop excluded, 14; S7 derate hours unavailable, 4; S8 the hourly file's hour-ending stamps read as
  hour-beginning, 16; S9 its UTC stamps read as Arizona time, 16; golden.
- Span: the hourly export, the met station file, the event log, the interruption report, the work orders, the O&M
  agreement and the README (7 files); tag, interval end, AC energy, AC register, irradiance, code, raised, cleared,
  interruption and restoration, type and description (12 columns).
- Realism: a central inverter raises one grid-fault alarm whether the grid or its own AC protection tripped it; logger
  links drop for hours while the inverter's register keeps counting; contractors exclude the utility's outages and the
  owner's stops in their own reports.

**Ask B. For each year from 2016 to 2025, how far the plant's net energy at the delivery point came over or under the
volume sold forward for that year, net of any buy-backs** (10 figures, MWh; -2,923 to +10,084).
- H18 home: the hedge record of the policy the call executes, each year's sale settled against what the plant
  delivered; a reconciliation that qualifies the call, not a second decision.
- Construction: each calendar year's REC less DEL at service point 0417 (the legacy file to February 29, 2020, the meter
  data system after, the latest version of each day), less that year's sales net of the 2019 and 2022 buy-backs, with
  the 2021 and 2024 amendments from the confirmations. The README names the district's files the meter of record; the
  SCADA's PLANT-RM read differs by about 1 MWh a year and misses the three lost days of 2018.
- Primary device B1 (D9, one account, two services): the account exports carry the station-service retail point 0418
  (rate GS-3) under the same channel name, DEL, to April 17, 2024. Netting the whole account takes the station service
  out of the plant's delivery and moves every year from 2016 to 2024 (by about 218 MWh a year, 47 in 2024). Fair: the
  service-point list carries the rate and the premise, and the metering exhibit says 0418 was a separate retail supply.
- Device B2 (D2, the latest accepted, not the latest delivered): the 2021 and 2024 sales were amended by confirmation
  (by 2,500 and 1,800 MWh); the blotter keeps the trades as booked.
- Hazards: HB1 the meter data system's history load repeats October 2019 to February 2020 beside the legacy file; HB2
  the buy-backs booked with positive quantities and side B; HB3 the legacy file's daily totals stamped at the interval
  end (the next day's 0000), which moves a year's last day into the next; HB4 the June 2025 estimated reads kept beside
  the actual reads that replaced them.
- Stops (built, misses of 10): S1 the whole account netted and the blotter as booked, 9; S2 the whole account netted,
  9; S3 the blotter as booked, 2; S4 both meter files stacked, 2; S5 the buy-backs added, 2; S6 the legacy totals dated
  by their stamps, 5; S7 every meter data version summed, 1; S8 the meter data system's first version of each day, 1;
  golden.
- Span: the legacy file, the meter data system's file, the service points, the metering exhibit, the blotter, the
  confirmations and the README (7 files); service point, channel, interval end, read date, kWh, version, trade id, side,
  delivery, quantity (10 columns).
- Realism: utility account exports list every service point under the same channel names; station service at older
  plants was often a separate retail supply; desks amend hedges by confirmation and the blotter keeps the trade as
  booked; meter data systems keep every version of a read.

**Hazard table** (built deltas asserted in `checks.py`)

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 UTC events | the inverters' event server runs in UTC | A | 16 of 16 inverters move when the log is read as local time |
| HA2 S-020 shared | technicians lock inverters out with the same remote stop | A | 14 of 16 move when every S-020 hour is excluded |
| HA3 derates | power-stage faults | A | 4 inverters with 2025 derates move when derate hours count unavailable |
| HA4 hour alignment | the loggers stamp each hour's end in UTC, the met station its beginning in Arizona time | A | 16 of 16 move when the stamps are read as hour-beginning or left in UTC |
| HB1 history load | the meter data system's go-live | B | 2019 by 15,343 and 2020 by 9,133 when both files are stacked |
| HB2 buy-back sign | the blotter books every trade with a positive quantity | B | 2019 by 2,800 and 2022 by 2,200 when the buy-backs are added |
| HB3 interval-end stamps | the legacy system stamps a day's total at its end | B | 2016 to 2020 by 11 to 170 MWh |
| HB4 versioned reads | estimated reads replaced after a manual download | B | 2025 by 1,337 when every version is summed, by 106 when the first is kept |

**Referee:** the district's interruption report and the inverters' registers settle A1 and A2; the service-point list
and the metering exhibit settle B1, the confirmations B2. None hands over an inverter's or a year's figure.

**Cracker sheet**

| Ask row | Figures | Cracker's figures kept | Cracker (landed the call, ran the battery, executed every filed rule) |
|---|---|---|---|
| Ask A, each inverter's 2025 availability (F-217 excluded by its code, gaps read through the register) | 16 | 0 | miss |
| Ask B, each year's over or under (the account netted whole) | 10 | 1 | miss |
| the note's chart (weather-year bars, P50 and volume lines, labels) | 4 | not an ask | outside |

The cracker keeps 1 of the 26 ask figures (asserted). A solver who checks which hours all sixteen inverters lost together
and which service point the delivery point is lands both asks.

Mirror leakage: 6 per cent of the ask weight (the mirror, off the call, keeps the asks no better than the cracker, one
figure in 26, and the chart's form; no rival keeps the standard deviation: the AC-side mirror's rounds to 2,000).

Pair ceiling: 32 (C = 38 + 7 + 55 x 0.04 = 47.2 with the cracker keeping 1 of 26 ask figures; S = 8 + 7 + 55 x 0.04 = 17.2
with the best miss keeping the chart's form). If the cracker also resolves A1 and B1, C rises
to about 100 and the pair to about 60: the devices are the margin, and the ceiling is rerun from the generated rubric.

## Build record

- Generator: `world.py` (weather, plant, washes, outages, meters, hedges), `records.py`, `docs.py`, `calc.py`, `asks.py`,
  `deliver.py`, `metadata.py`, `checks.py` (198 assertions, the three-rules block R1 to R3c, every SF row, the ladder
  with every rival 300 MWh or more outside the bin, the corridor with every construction 200 MWh or more inside, the
  closure axes, both asks with their stops and devices, the separation line, the realism sweep, the input gates and the
  distractors' deletion), `verify.py` (pandas and pypdf, its own path), `build.py` (two byte-identical builds, the zip).
- Placement: the golden sits in its bin through the new modules' reference efficiency (0.9747, a constant of the
  comparison's table B and the repowered array); the world's laws are set before any record is drawn and no record is
  edited after. The stage 4 hardening reset the world's laws once, each before any record is drawn: the six-wash era's
  cool-season months and Schedule 2's December wash a block a week from 2021, the wear's fast phase (3.85 per cent a
  year, mid-2017 to mid-2020), the site's seasonal wind (calm December, windy March to June), the spring dust from
  February, the year-to-year spread of clear-sky transmittance (1.33 per cent) and the scope's December 2026 wash.
- Pack: 23 files in six formats (csv, txt, xlsx, pdf, docx, md); the largest 219,144 rows; distractors Tresco's
  repowering summary and the Palo Verde forward marks, named in `metadata.json`.
- Gates at the PAUSED commit (stage 4, round 2): checks 198/198; verify green; two builds byte-identical;
  `figures_check.py` exit 0 (62 figures); container audit clean on target and golden; `leak.py` REVIEW, no LEAK (a
  station-service day's 534.1 kWh in the legacy file matches 2021's over-under by chance); `guard.py check` WARN
  (overuse.objective) against every card on origin, validate clean; `guard.py surface` one pair promoted on the
  differentiated card signature (task232), no surface clone; `guard.py heart` WARN; `precut.py` exit 0;
  `voice-check.py` PASS.
- Stage 4, round 1: the determinism judge DETERMINISTIC, APPROVE (`determinism_check_report_round1.md`); the leak reader
  clean; the rule-3 audit PASS. Its notes and the reader's readings are answered in the generator: the corridor and the
  landers above, the pins (the README names the district's files the meter of record; the scope keeps the December 2026
  wash, a WHAT about the plant in 2027), and SF21, Ask A's S8 and S9 and Ask B's S3 and S8 asserted.

## Tried and rejected` (the one-scalar calibration family that landed its call): here
  the history-calibrated family is swept window by window and every natural window misses (`## Ladder`).

**World.** Marden-Vail Building Products (fictional), a Phoenix maker of gypsum wallboard and joint compound, owns
Hadley Ranch Solar (fictional), a 40 MWac fixed-tilt plant in Pinal County (commercial operation November 20, 2015):
sixteen 2.5 MW central inverters, each fed by 8,000 Kellerman KS-315P modules (40.32 MWp), on south-facing tables at 25
degrees. It exports at 69 kV to the Vado Seco Irrigation and Power District (fictional); the output is sold at Palo
Verde, each calendar year forward at the one-year P90 under the treasury's energy risk policy, the treasurer approving
the volume. Tresco Field Services (fictional) has run operations and maintenance since commercial operation, under the
current agreement from 2021. The original modules lost power fast from mid-2017 to mid-2020 and slowly since; the 2019
survey found cracked backsheets. The inverters' maker left the US market in 2018 and each failed power stage was replaced with
a refurbished one, which runs with higher losses; inverter 07 burned in March 2021 and was replaced under a new tag.
Tresco washed six times a year to 2018, in the cool months (January to April, October and November; never in the summer
heat). Drought restrictions on the plant's well then cut the washes to four in 2019, two in 2020 and, under Schedule 2
of the 2021 O&M agreement, one each December, a block a week, the well's permitted weekly draw covering one block's
wash. In April 2024 the district retired the 12 kV station-service supply and the auxiliaries moved behind the
revenue meter. From October 2025 to September 2026 Corvane Solar (fictional) ran a side-by-side comparison in block 3:
a table of new CV-450BHC bifacial modules beside a table of unexposed KS-315P spares, both washed weekly. The
replacement (82,944 CV-450BHC modules, 288 strings of 18 per inverter, 37,324.8 kWp) runs from October 5 to December 18,
2026 on the same tables, cabling and inverters.

## Default path

Built figures (`generator/checks.py`).

1. Read the energy risk policy: the volume is the one-year P90 of the plant's 2027 net energy at the delivery point,
   the P50 less 1.2816 standard deviations over the full calendar years 2001 to 2025 of the long-term record, rounded
   down to the nearest 1,000 MWh; the base period is the twelve complete months before the sale.
2. Join the two SCADA layouts and take the plant's performance ratio over October 2025 to September 2026: net export
   over plane-of-array irradiation times the original 40,320 kWp (63.7 per cent).
3. Carry it onto the new modules with the side-by-side report's measured gain per kWp (14.7 per cent) and the new
   nameplate (37,324.8 kWp).
4. Run the 25 weather years' plane-of-array irradiation through it, take the mean and the sample standard deviation,
   and strike the P90 (60,891 MWh).

Ends on: a volume of 60,000 MWh (P90 60,891, 14 per cent under the golden).

Golden: a volume of 70,000 MWh (P90 70,620; P50 73,000; standard deviation 1,900): the same base period's performance,
restored only by the original modules' own wear (14 per cent: the inverters' DC input per kWp per unit of irradiation,
temperature-corrected, on fully available inverter-days 1 to 3 days after each block's wash, December 2025 against
2016), then the gain, the new nameplate and the weather years.

## Stump sentence

Carrying the plant's last twelve months' performance ratio onto the new modules with the side-by-side gain and running
the 25 weather years files 60,000 MWh against the golden 70,000; the step that lands it there is treating the plant's
present performance as the repowered plant's, when the original modules' own wear leaves with them; and restoring the
plant's whole decline since 2016 (76,000), its whole DC-side decline (73,000) or its decline after washes read at the
inverters' AC output (72,000) overshoots, because the inverters' lost efficiency and availability and the dust the array
carries between washes, which grew as the washes fell from six a year to one, stay with the plant: only the wear read on
the days after each wash at the inverters' DC input restores what the replacement removes.

## Three rules

- **Task type:** energy-systems-utilities, asset-condition-maintenance (serves Forecasting): what the plant's assets are
  worth in energy after a maintenance action, the module replacement, forecast for calendar 2027 from the plant's own
  monitoring history and the long-term irradiance record.
- **Domain test:** the deciding quantity is the repowered plant's 2027 performance level, which a solar asset analyst
  builds by separating the losses the module swap removes (the original modules' wear) from those it keeps (inverter
  efficiency and availability, and soiling under the cleaning contract), with the wear measured the way PV degradation
  studies measure it, at the DC side, temperature-corrected and on clean-module days, then run over the long-term
  plane-of-array record for the one-year P90.
- **Swap:** "how much of next year's flights a re-engined fleet can sell forward" keeps a part replaced and a decline in
  the record, but plane-of-array irradiation to normalise by, an inverter boundary that splits the DC losses from the AC
  losses, dust that a wash clears and the dry months rebuild, and a P90 struck over weather years have no counterpart,
  so what sets the forward level stops making sense.
- **Layer 1:** the SCADA replacement of March 2020 (the original system's wide CSV in local days and kWh with inverters
  01 to 16; the replacement's long export in UTC day starts and MWh with block-inverter tags); the original server's
  three lost days in 2018; inverter 07 replaced in 2021 under a new tag; the long-term record hourly in UTC under a
  header block; the work orders as free text, washes block by block among every other job; the station service moved
  behind the revenue meter in April 2024; the side-by-side report and the interruption report as PDF tables, the scope
  as a Word paper; the district's legacy fixed-width billing export and its meter data system with a history load and
  versioned reads. Each is what these systems write; none carries the stump (asserted per item, R2a to R2g).
- **Layer 2:** `estimation_fit` (decomposition): the plant's decline is a product of a monotone module wear, a soiling
  loss that the washes reset and whose mean grew as the washes grew rarer, and inverter losses on the AC side and in
  availability; the replacement removes only the first, so it is read apart from the others the way PV performance
  studies read soiling and degradation apart.
- **Decisive step:** measure the original modules' wear as the decline, from 2016 to the base period, of the inverters'
  DC input per kWp per unit of plane-of-array irradiation, temperature-corrected to 25 degC, on fully available
  inverter-days just after each block's wash, and restore the base period's output by that wear alone before the
  measured gain and the weather years are applied.
- **Not semantics:** every field (DC energy, AC energy, operating hours, irradiation, module temperature, the work
  orders' wash entries) and every filed definition (the P90, the volume's basis, the base period, the rounding, the
  cleaning schedule) is read the same way by the easy routes; no field, code or definition says which part of the
  decline is wear, and the default path and its refinements read them all and still file 60,000, 72,000, 73,000 or
  76,000.
- **Not rule application:** the shipped sentences that bear on how the figure is computed (the policy's P90, base period
  and volume sentences, the scope's capacity and its statement that the inverters stay, Schedule 2's one December wash a
  year, the report's measured gain) are executed word for word in `checks.py` (R3c): their only literal product is the
  base period carried with the gain, 60,000, never the golden; no filed sentence says which part of the decline the
  replacement removes or where to read it.
- **Analyst test:** a strong analyst who joins the two SCADA layouts, reads the policy, the scope, the O&M agreement
  and the side-by-side report correctly and runs the 25 weather years carries the base period's performance ratio onto
  the new modules with the report's gain and files 60,000 MWh; restoring the whole decline since 2016 files 76,000, the
  whole DC-side decline on available days 73,000, and the decline after washes read at the AC output 72,000 (executed
  on the clean truth: 60,756 against the golden construction's 70,456, both in their bins).
- **Estimand:** the energy risk policy (sections 3.1, 4.1, 4.2, 4.4) and the prompt: the one-year P90 of the plant's 2027
  net energy at the delivery point, the P50 (the mean of the plant's annual energy, as it will stand in 2027, under the
  weather of each full calendar year 2001 to 2025 of the long-term record) less 1.2816 sample standard deviations of
  the same energies, built from the plant's own monitoring record with the twelve complete months before the sale as
  the base period, rounded down to the nearest 1,000 MWh; the population, outcome, window, unit and rounding are filed,
  the method is not.
- **No decoy:** no vendor energy estimate, consultant study, prior-year hedge memo, desk draft or stakeholder figure
  states or argues a 2027 volume, a performance ratio for the repowered plant or a wear figure (R3c asserts no document
  carries one); the side-by-side report states its measured gain and says nothing about the plant.
- **No certified replay:** no certified or published figure for the repowered plant ships and nothing graded is
  reproduced; the desk's past volumes come from estimates no shipped file reproduces; Tresco's repowering summary gives
  five other plants' energy changes without a method (a distractor, asserted to miss at 65,457).
- **Lesson:** when part of an asset is replaced, the forecast restores only that part's own deterioration, measured where
  the losses the asset keeps separate out (here the inverter boundary) and on the days a recurring cleaning has reset the
  loss that cycles; the asset's whole decline mixes in losses the replacement keeps, which here grew as the cleaning grew
  rarer, and carrying the present output forward keeps a wear the replacement removes; no build on file teaches the split
  of one unit's decline across an internal boundary and a reset cycle.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Built figures.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the base period's performance ratio carried onto the new modules with the gain (60,000) | no | no | yes (a forecast from recent performance) | no | no | yes (one ratio) | readable |
| R0b the same on the new nameplate without the gain (53,000), or a recent window's ratio (60,000 to 61,000) | no | no | yes | no | no | yes | readable |
| R1 the plant's whole decline since 2016 restored: the first year carried with the gain (76,000); on the nameplate alone 66,000 | no | no | yes (repowering restores the plant) | no | no | yes (one ratio) | readable |
| R2 the whole DC-side decline on available days restored, inverters kept (73,000) | no | yes (the DC energy column) | yes (inverters stay, so measure at the DC side) | no | no | no | readable |
| R2b the decline after washes read at the inverters' AC output restored, soiling kept, inverter losses restored (72,000) | no | no | yes (the soiling-aware degradation analysis on AC energy) | no | no | no | readable |
| R2c a degradation rate times the plant's age: the year-on-year median (66,000), the last five years' trend (62,000), the warranty's rate (66,000), a round 1 per cent a year on the warranty's schedule (69,000) | no | no | yes (a degradation rate times age) | no | no | yes | readable |
| R2d the decline after washes without the temperature correction, at the DC input or the AC output, mean or median, or the plant's meter in the week after each wash (67,000 to 69,000) | no | yes (the energy columns) | yes (a soiling-aware read that skips the weather) | no | no | yes (one ratio) | readable |
| R3 (decisive) the wear read on the days after each block's wash at the inverters' DC input, temperature-corrected, the base period restored by it alone (70,000) | no (the policy files the estimand and the base period; the scope and the O&M agreement file what stays; nothing names the wear, a wash cycle or a boundary) | no (no column holds a soiling, wear or loss figure; no flag marks a clean day; the work orders log washes as free text among every other job) | no (the reflexes are recent performance, restoring the decline, measuring at the DC side, a soiling-aware AC analysis, a rate times age) | no (no forecast, model output or study of the repowered plant ships) | no (the battery is clean on it) | no (a split of a decline across two cuts of the record, then a ratio) | silent |

## Semantic fork table

Every term of the main ask and every convention the main computation needs, each asserted in `generator/checks.py`
under its id. Which part of the decline the replacement removes is the decisive step, a split the data force (the
inverter boundary and the wash cycle), never a reading.

| SF | Term or convention | Golden reading | Alternatives | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | 2027 | calendar 2027 | the company's fiscal year | other volume | the policy, section 2.1 ("The hedge year is the calendar year") |
| SF2 | the one-year P90 | the P50 less 1.2816 standard deviations | the empirical tenth percentile (70,145) | same call (70,000) | the policy, section 4.2 |
| SF3 | the standard deviation | the sample standard deviation | the population standard deviation (1,885) | same call (70,000; 1,900) | same call |
| SF4 | the weather years | the full calendar years 2001 to 2025 | 2026's months added | ruled out | the policy, section 4.2 ("each full calendar year") and the record's header |
| SF5 | the energy | net energy at the delivery point (revenue meter export less import) | the inverters' gross AC (72,000) | ruled out | the policy, section 3.1 |
| SF6 | the plant in 2027 | 37,324.8 kWp of CV-450BHC on the same tables and inverters, under the O&M agreement to 2027 | the original array; another cleaning schedule | ruled out | the scope ("What is replaced", "What stays") and Schedule 2 |
| SF7 | the base period | the twelve complete months before the sale, October 2025 to September 2026 | calendar 2025; the last 24 months; the one-wash years averaged | same volume (70,000 on each); ruled out for the P50 | the policy, section 4.4 |
| SF8 | the as-new reference | 2016's washed days | commercial operation to 2016 or 2017; the first twelve months; the handover wash; 2016 and 2017; 2016's winter washes against December | same call (70,000; 73,000; 1,900; C3) | same call |
| SF9 | a freshly washed day | 1 to 3 days after the block's wash, full operating hours | 1 to 1, 1 to 2, 1 to 5, 2 to 3, 2 to 4 days; full hours within 0.05 h | same call (C3) | same call |
| SF10 | the temperature basis | the irradiance-weighted back-of-module temperature (T_MOD_IW) at the KS-315P's -0.42 %/degC | NOCT cell temperature from the daily air temperature; a coefficient fitted on the record (each period's regression at 25 degC or at the base period's temperature, one slope for both periods, 2016's slope) | same call (C3: 70,329 to 70,690; P50 72,784 to 73,157) | same call; the Sandia model needs hourly wind, which ships for 2025 only |
| SF10b | the temperature basis | as SF10 | an uncorrected comparison (67,000 to 69,000) | ruled out | the README's field definition and the datasheet's coefficient of Pmax; the base period's post-wash days run 9 degC cooler than 2016's |
| SF11 | the measured gain | the twelve months' DC energy per kWp, table B over table A | the stated 14.7 per cent; the mean of the monthly ratios | same call | same call |
| SF12 | the gain's first year | the test's modules were new at its start, so its gain carries their first year; 2027 is the repowered array's first full year | a later-year gain | ruled out | the report, section 2 |
| SF13 | the new nameplate | 37,324.8 kWp | a flash-tested power | ruled out | the scope; no flash list ships |
| SF14 | clipping | immaterial: the original array's highest hour is 91.3 per cent of rating; the repowered array reaches its rating in one cloud-edge hour of the 25 years (101.3 per cent, April 2014, 0.0006 per cent of that year) | an hourly clipping loss | same call | same call |
| SF15 | the delivery point | the 69 kV revenue meter, the district's service point 0417, which the SCADA's PLANT-RM reads | the SCADA's read | same call for the call (agree within 0.004 per cent in every month of the base period); the asks take the district's files | the exhibit (C.1.2) and the README ("the meter of record") |
| SF16 | the long-term record's basis | the provider's site-adapted series | a raw satellite series | ruled out | the policy, section 4.3, and the record's header |
| SF17 | the layouts | both: 2016 in the original, the base period in the replacement | one layout | same call | the README |
| SF18 | the replaced inverter | inverter 07 continued by B2-INV3R | dropped | same call (asserted, R2b) | the crosswalk |
| SF19 | rounding | the volume down to the nearest 1,000 from the unrounded P90; the P50 to the nearest 1,000; the standard deviation to the nearest 100 | the volume to the nearest 1,000 (71,000) | ruled out | the policy, section 4.1, and the prompt |
| SF20 | the weather-year energy | the repowered plant's performance level times that year's plane-of-array irradiation | a temperature-adjusted level per year | same call (the record carries irradiance only) | same call |
| SF21 | the volume's rounding path | down from the unrounded P90 | the rounded P50 less 1.2816 rounded standard deviations (70,565) | same call | same call |

## Ladder

Built figures; P90 in MWh, the golden's floor bin 70,000 to 71,000 (the P90 at 70,620, 0.38 of a bin from the top edge).

| Rung | Construction | P90 | Volume | Dies to |
|---|---|---|---|---|
| 0 | the base period's ratio, the gain, the new nameplate | 60,891 | 60,000 | the original modules' own wear leaves with them: the DC input per kWp per unit of irradiation after each wash fell 14 per cent from 2016 to December 2025 |
| 0b | the same on the nameplate alone | 53,069 | 53,000 | the side-by-side report's gain and the wear |
| 1 | the first year carried with the gain (the whole decline restored) | 76,520 | 76,000 | the inverters' AC-to-DC ratio fell about 2 points as power stages were refurbished, their outages grew, and the dust carried between washes grew as washes fell from six a year to one; the plant keeps all three |
| 1b | the first year on the nameplate alone | 66,690 | 66,000 | the gain and the kept losses together |
| 2 | the whole DC-side decline on available days restored | 73,481 | 73,000 | the DC-side decline carries the soiling growth: on the days after each wash the decline is 14 per cent, on every available day 17 |
| 2b | the decline after washes read at the inverters' AC output restored | 72,191 | 72,000 | the inverters' conversion losses stay |
| 2c | a rate times age: year-on-year median, last five years' trend, the whole record's trend, the warranty | 66,687; 62,100; 76,780; 66,952 | 66,000; 62,000; 76,000; 66,000 | the wear was fast from mid-2017 to mid-2020 and slow since; no rate carries it |
| 2d | the decline after washes without the temperature correction: at the DC input (mean 67,814, median 68,071, ratio of sums 67,950), at the AC output (mean 69,323, median 69,557), December 2025 against 2016's winter washes (69,551), the plant's meter in the week after each wash (68,442) | 67,814 to 69,557 | 67,000 to 69,000 | the base period's post-wash days run 9 degC cooler than 2016's (31 against 41), 4 per cent at the datasheet's -0.42 per cent per degC; no reading at the AC side or the meter offsets it |
| 2e | a round rate times age, straight or on the warranty's schedule, at the base period's middle or at the sale: 0.5, 0.8, 1.0 and 1.5 per cent a year | 64,218 to 73,643 | none in 70,000 | the measured wear, 14 per cent, falls between 1.0 per cent a year on the warranty's schedule (69,086 and 69,492) and 1.5 per cent a year straight (72,097 and 72,763) |
| 3 (decisive) | the wear read on the days after each wash at the DC input, temperature-corrected, the base period restored by it alone | 70,620 | 70,000 | |

**The history-calibrated family** (task148's one-scalar route: a window's ratio carried with the gain or on the
nameplate), every natural window asserted to miss: the whole record 66,079; 2016 to 2025 66,356; the original SCADA's
years 73,384; the replacement SCADA's 61,370; the one-wash years 61,113; the last five years 61,138; the last three
61,212; 2025 60,691; the first twelve months 76,505; the six-wash years 74,940; the years before one wash a year 71,459
(the nearest, 459 MWh outside); on the nameplate every window between 52,895 and 66,678. The windows that land are
unmarked middle spans (2017 to 2020, 2018 to 2019) that no document, event or regime boundary marks; a solver has no
reason to carry them.

**Other rivals asserted to miss:** the plant's DC energy per kWp against the report's table A over twelve months
(77,382) or in its best month (73,366), the reference table's single-string basis sitting 2.4 per cent above an array's;
Tresco's mean repowering uplift on the base period (65,457). Every rival is asserted at least 300 MWh outside the
golden's bin; the nearest sit 443 (the AC output's median after the washes, uncorrected), 449 (December against 2016's
winter washes, uncorrected) and 508 (1 per cent a year on the warranty's schedule at the sale) outside.

**The corridor of the golden construction** (C3, asserted on the volume, the P50 and the standard deviation, each at
least 200 MWh inside its bin): the days after the wash (1 to 1: 70,714; 1 to 2: 70,686; 1 to 5: 70,630; 2 to 3: 70,572;
2 to 4: 70,624); the estimator (inverter by inverter 70,619; the median 70,603; the ratio of sums 70,601; full hours
within 0.05 h 70,632; the top 1 per cent envelope 70,507; a line through the one-wash years' levels 70,682; the last two
December washes 70,512); the reference (commercial operation to 2016 70,612; the first twelve months 70,612; the
handover wash 70,566; 2016 and 2017 70,357; commercial operation to 2017 70,372; December 2025 against 2016's January and
November washes 70,623, January alone 70,704, November alone 70,542); the temperature correction (the datasheet's
coefficient in its first-order translation form to 25 degC 70,344, to the base period's mean temperature 70,412, to
2016's 70,516; NOCT from the daily air temperature 70,340, its median 70,489; a regression on module temperature in each
period at 25 degC 70,690 or at the base period's mean temperature 70,678; one slope for both periods on log yield 70,660
or on yield at 25 degC 70,329; 2016's fitted coefficient 70,677; a regression on the NOCT temperature 70,502). The
corridor spans 70,329 to 70,714 and its P50s 72,784 to 73,182, the nearest 284 MWh from an edge. The Sandia
module-temperature model needs hourly wind, which ships for 2025 only, so it cannot be run for the 2016 reference. One
standard error on the wear and the gain together: 70,384 to 70,855. The base-period variants the policy rules out still
keep the volume (70,388 to 70,719). Counting the wash day itself as clean misses (71,104): the work orders show each
block washed until mid-morning.

**Position and margin:** the golden sits between rung 0 and rung 1, which bracket it; every rival lands in another floor
bin at least 300 MWh outside the golden's (asserted), the expert's AC-side route 1.6 bins over. P50 73,084.5 rounds to
73,000 with 415 MWh to its nearer edge; the standard deviation 1,923.4 rounds to 1,900 with 26.6 MWh to its edge (the
population standard deviation 1,884.5 with 34.5).

**Strength:** a solver lands the call only by splitting the decline three ways (the wear from the dust by the wash
cycle, from the inverters by the DC boundary) and correcting for the 9 degC between the base period's post-wash days and
2016's. Estimated chance one strong solver lands it 0.10 to 0.12, both of two 0.01 to 0.02. The routes the round-1
audit found landing by cancelling errors (temperature-blind reads after the washes at the AC output or the meter, the
uncorrected DC median, 1 per cent a year on the warranty's schedule) now file 67,000 to 69,000, each asserted 300 MWh or
more outside the bin (443 the nearest); the only round rates that land (1.2 to 1.3 per cent a year) are no default.

**Dominance and worth:** the decisive step moves the P90 from rung 2's figure down by the soiling growth and from rung
0's up by the wear; it carries the call, the P50 and the chart's level, so a response off it misses all three.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the plant's 2027 net energy at the delivery point, with the repowered array under the current O&M agreement | filed (the policy 3.1 and 4.2; the scope; Schedule 2); C1 on the layouts and the replaced inverter (SF17, SF18) |
| 2 | Unit of account | MWh of net energy at the delivery point | filed (the policy 3.1) |
| 3 | Attribution window | calendar 2027; the weather years 2001 to 2025 | filed (the policy 2.1 and 4.2) |
| 4 | As-of dating | the monitoring history to September 30, 2026; the long-term record to December 31, 2025 | filed (the README and the record's header) |
| 5 | Version basis | the provider's site-adapted series as last delivered; the report's issue 1 | filed (the policy 4.3; the report's header) |
| 6 | Denominator | the 25 annual energies, the sample standard deviation | filed (the policy 4.2); C1 (SF3) |
| 7 | Weighting | every weather year once | filed (the policy 4.2) |
| 8 | Window length | the base period, the as-new year, the days after each wash | filed (the policy 4.4); C1 across the as-new and wash-day windows (SF8, SF9) |
| 9 | Boundary inclusivity | the hedge year whole; the P-values over whole years | filed |
| 10 | Rounding path | the volume floored once to 1,000 from the unrounded P90; the P50 to 1,000; the standard deviation to 100 | filed (the prompt; the policy 4.1); asserted |
| 11 | Tie-break | none: a single figure | not applicable |
| 12 | Maturity and censoring | the base period complete; the record's years complete | asserted (no missing SCADA day in the base period; 2026 not in the record) |
| 13 | Order of operations | the performance level, then the weather years, then the P-values | C1 (the level scales every year alike) |
| 14 | Row order | the exports' order | C1 (the computation sorts by day) |
| 15 | Duplicate resolution | the two SCADA layouts meet on March 3, 2020 with no day in both | asserted |
| 16 | Identity normalisation | inverter numbers to block tags at the SCADA replacement; inverter 07's new tag | C1 (asserted, R2b) |
| 17 | Netting against gross | net export: delivered less received | filed (the policy 3.1) |
| 18 | Dimensional units | the original SCADA in kWh, the replacement in MWh; irradiation in kWh/m2 a day, the record hourly in W/m2 | the README and the record's header |
| 19 | Code and status semantics | operating hours; the work orders' job types | the README; never the stump |
| 20 | Integerisation | none | not applicable |
| 21 | Clause scope | Schedule 2 to December 31, 2027; the scope replaces the modules only | filed |
| 22 | Forward window contents | 2027 holds the repowered array under Schedule 2's December wash, a block a week, and the existing inverters; the scope keeps the December 2026 wash, so 2027's dust cycle is the base period's | filed (the scope; Schedule 2); asserted (AX22, AX23) |

## Literal reader

Executing the prompt and every filed sentence word for word fixes the population (the plant's 2027 net energy at the
delivery point, the policy 3.1 and 4.2), the outcome and its P-values (4.2), the weather years (the record's full years
2001 to 2025), the base period (4.4), the plant as it will stand (the scope and Schedule 2) and the rounding; each term
has one reading or readings that file the same volume (the fork table). No sentence says how the repowered plant's
performance level follows from the record: whether the base period carries forward as it is, with its whole decline
restored, with its DC-side decline restored or with only part of it, is HOW, and the data's structure forces it (on the
days after each wash the DC input per unit of irradiation falls 14 per cent from 2016, on every available day 17; the
AC-to-DC ratio and the availability decline on their own; the scope keeps the inverters and the December wash, and
Schedule 2 keeps one wash a year). The easy answers come from easy methods on the same literal estimand, never from
another reading; the filed sentences executed alone give only the base period carried with the gain (60,000).

## Oracles

- The SCADA history itself: no performance ratio, wear or soiling figure is stated; every split is built from it.
- The side-by-side report: one measured gain of the new modules over unexposed originals, the same under every basis
  the call could take (it multiplies every construction alike); its absolute specific yields sit on a single string's
  basis and no route through them lands (77,382 over twelve months, 73,366 in the best month).
- The work orders: washes among every other job, as free text; no soiling or yield figure.
- Tresco's repowering summary (a distractor): five other plants' energy changes; their mean on the base period misses
  (65,457). No forecast, model output or study of Hadley Ranch's repowered output ships: none for the call.

## Ask sheet

**Main call's declared row population:** the two daily SCADA exports, the CLN work orders, the long-term record, the
side-by-side report, the scope, the policy, the datasheet and Schedule 2. Device and hazard rows in it: 0 (asserted: the
daily export holds every 2025 inverter-day whole, its AC sums matching the registers across the 652 hourly rows the
loggers dropped). The asks read files the call never reads (the 2025 hourly export, the met station's hourly file, the
event log, the interruption report, the district's account exports and service points, the blotter, the confirmations,
the metering exhibit) and the work orders' OWN and CM rows. Neither ask is keyed to the call, and they share no primary
device or path.

**Ask A. Each inverter's 2025 availability as the O&M agreement defines it** (16 figures, per cent to two decimals;
96.70 to 99.82).
- H18 home: the inverters stay with the repowered plant and their outages are one of the losses the base period
  carries into 2027; the note says so, and the table is its audit trail. The call reads the kept losses from the
  plant's energy, not from the contract's hour count.
- Construction: Production Hours are the 2025 local hours whose mean plane-of-array irradiance at the met station is at
  least 50 W/m2 (3,981 a year); Unavailable is a Production Hour with no AC energy, unless the cause is the district's
  outage or a stop the owner requested; Availability is one less Unavailable over Production less Excluded (Schedule 4).
- Primary device A1 (D9, one alarm code, two causes): the district's 69 kV interruptions and the inverters' own AC
  relay trips both raise `F-217 AC GRID FAULT`. Excluding every F-217 hour credits the relay trips (every inverter has
  one or more in 2025). Fair: each interruption takes all sixteen inverters down within the minute and sits in the
  district's report; each relay trip takes one inverter and has a technician's reset in the CM work orders.
- Device A2 (D4, absence as the signal): the four block loggers dropped 652 inverter-hours in 25 gaps; the inverter's
  AC register at the next row shows the energy delivered across the gap. Counting a missing hour as no AC energy pulls
  every inverter low. Fair: no gap overlaps an outage (asserted).
- Hazards: HA1 the event log in UTC; HA2 the S-020 stop code shared by the owner's requests and the technicians'
  lockouts, only the OWN work orders naming the owner's; HA3 power-stage derates, in which the inverter delivers energy;
  HA4 the hourly AC file stamped at each hour's end in UTC against the met station's hour beginning in Arizona time.
- Stops (built, each a complete pipeline, misses of 16): S1 every zero or missing hour unavailable, nothing excluded,
  16; S2 every F-217 hour excluded, missing hours as zero, 16; S3 the district's outages excluded, missing hours as
  zero, 16; S4 every F-217 hour excluded, gaps read through the register, 16; S5 the event log read as local time, 16;
  S6 every S-020 stop excluded, 14; S7 derate hours unavailable, 4; S8 the hourly file's hour-ending stamps read as
  hour-beginning, 16; S9 its UTC stamps read as Arizona time, 16; golden.
- Span: the hourly export, the met station file, the event log, the interruption report, the work orders, the O&M
  agreement and the README (7 files); tag, interval end, AC energy, AC register, irradiance, code, raised, cleared,
  interruption and restoration, type and description (12 columns).
- Realism: a central inverter raises one grid-fault alarm whether the grid or its own AC protection tripped it; logger
  links drop for hours while the inverter's register keeps counting; contractors exclude the utility's outages and the
  owner's stops in their own reports.

**Ask B. For each year from 2016 to 2025, how far the plant's net energy at the delivery point came over or under the
volume sold forward for that year, net of any buy-backs** (10 figures, MWh; -2,923 to +10,084).
- H18 home: the hedge record of the policy the call executes, each year's sale settled against what the plant
  delivered; a reconciliation that qualifies the call, not a second decision.
- Construction: each calendar year's REC less DEL at service point 0417 (the legacy file to February 29, 2020, the meter
  data system after, the latest version of each day), less that year's sales net of the 2019 and 2022 buy-backs, with
  the 2021 and 2024 amendments from the confirmations. The README names the district's files the meter of record; the
  SCADA's PLANT-RM read differs by about 1 MWh a year and misses the three lost days of 2018.
- Primary device B1 (D9, one account, two services): the account exports carry the station-service retail point 0418
  (rate GS-3) under the same channel name, DEL, to April 17, 2024. Netting the whole account takes the station service
  out of the plant's delivery and moves every year from 2016 to 2024 (by about 218 MWh a year, 47 in 2024). Fair: the
  service-point list carries the rate and the premise, and the metering exhibit says 0418 was a separate retail supply.
- Device B2 (D2, the latest accepted, not the latest delivered): the 2021 and 2024 sales were amended by confirmation
  (by 2,500 and 1,800 MWh); the blotter keeps the trades as booked.
- Hazards: HB1 the meter data system's history load repeats October 2019 to February 2020 beside the legacy file; HB2
  the buy-backs booked with positive quantities and side B; HB3 the legacy file's daily totals stamped at the interval
  end (the next day's 0000), which moves a year's last day into the next; HB4 the June 2025 estimated reads kept beside
  the actual reads that replaced them.
- Stops (built, misses of 10): S1 the whole account netted and the blotter as booked, 9; S2 the whole account netted,
  9; S3 the blotter as booked, 2; S4 both meter files stacked, 2; S5 the buy-backs added, 2; S6 the legacy totals dated
  by their stamps, 5; S7 every meter data version summed, 1; S8 the meter data system's first version of each day, 1;
  golden.
- Span: the legacy file, the meter data system's file, the service points, the metering exhibit, the blotter, the
  confirmations and the README (7 files); service point, channel, interval end, read date, kWh, version, trade id, side,
  delivery, quantity (10 columns).
- Realism: utility account exports list every service point under the same channel names; station service at older
  plants was often a separate retail supply; desks amend hedges by confirmation and the blotter keeps the trade as
  booked; meter data systems keep every version of a read.

**Hazard table** (built deltas asserted in `checks.py`)

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 UTC events | the inverters' event server runs in UTC | A | 16 of 16 inverters move when the log is read as local time |
| HA2 S-020 shared | technicians lock inverters out with the same remote stop | A | 14 of 16 move when every S-020 hour is excluded |
| HA3 derates | power-stage faults | A | 4 inverters with 2025 derates move when derate hours count unavailable |
| HA4 hour alignment | the loggers stamp each hour's end in UTC, the met station its beginning in Arizona time | A | 16 of 16 move when the stamps are read as hour-beginning or left in UTC |
| HB1 history load | the meter data system's go-live | B | 2019 by 15,343 and 2020 by 9,133 when both files are stacked |
| HB2 buy-back sign | the blotter books every trade with a positive quantity | B | 2019 by 2,800 and 2022 by 2,200 when the buy-backs are added |
| HB3 interval-end stamps | the legacy system stamps a day's total at its end | B | 2016 to 2020 by 11 to 170 MWh |
| HB4 versioned reads | estimated reads replaced after a manual download | B | 2025 by 1,337 when every version is summed, by 106 when the first is kept |

**Referee:** the district's interruption report and the inverters' registers settle A1 and A2; the service-point list
and the metering exhibit settle B1, the confirmations B2. None hands over an inverter's or a year's figure.

**Cracker sheet**

| Ask row | Figures | Cracker's figures kept | Cracker (landed the call, ran the battery, executed every filed rule) |
|---|---|---|---|
| Ask A, each inverter's 2025 availability (F-217 excluded by its code, gaps read through the register) | 16 | 0 | miss |
| Ask B, each year's over or under (the account netted whole) | 10 | 1 | miss |
| the note's chart (weather-year bars, P50 and volume lines, labels) | 4 | not an ask | outside |

The cracker keeps 1 of the 26 ask figures (asserted). A solver who checks which hours all sixteen inverters lost together
and which service point the delivery point is lands both asks.

Mirror leakage: 6 per cent of the ask weight (the mirror, off the call, keeps the asks no better than the cracker, one
figure in 26, and the chart's form; no rival keeps the standard deviation: the AC-side mirror's rounds to 2,000).

Pair ceiling: 32 (C = 38 + 7 + 55 x 0.04 = 47.2 with the cracker keeping 1 of 26 ask figures; S = 8 + 7 + 55 x 0.04 = 17.2
with the best miss keeping the chart's form). If the cracker also resolves A1 and B1, C rises
to about 100 and the pair to about 60: the devices are the margin, and the ceiling is rerun from the generated rubric.

## Build record

- Generator: `world.py` (weather, plant, washes, outages, meters, hedges), `records.py`, `docs.py`, `calc.py`, `asks.py`,
  `deliver.py`, `metadata.py`, `checks.py` (198 assertions, the three-rules block R1 to R3c, every SF row, the ladder
  with every rival 300 MWh or more outside the bin, the corridor with every construction 200 MWh or more inside, the
  closure axes, both asks with their stops and devices, the separation line, the realism sweep, the input gates and the
  distractors' deletion), `verify.py` (pandas and pypdf, its own path), `build.py` (two byte-identical builds, the zip).
- Placement: the golden sits in its bin through the new modules' reference efficiency (0.9747, a constant of the
  comparison's table B and the repowered array); the world's laws are set before any record is drawn and no record is
  edited after. The stage 4 hardening reset the world's laws once, each before any record is drawn: the six-wash era's
  cool-season months and Schedule 2's December wash a block a week from 2021, the wear's fast phase (3.85 per cent a
  year, mid-2017 to mid-2020), the site's seasonal wind (calm December, windy March to June), the spring dust from
  February, the year-to-year spread of clear-sky transmittance (1.33 per cent) and the scope's December 2026 wash.
- Pack: 23 files in six formats (csv, txt, xlsx, pdf, docx, md); the largest 219,144 rows; distractors Tresco's
  repowering summary and the Palo Verde forward marks, named in `metadata.json`.
- Gates at the PAUSED commit: checks 148/148; verify green; two builds byte-identical; `figures_check.py` exit 0;
  container audit clean on target and golden; `leak.py` REVIEW, no LEAK; `guard.py surface` one pair promoted on the
  differentiated card signature (task232), no surface clone; `guard.py heart` WARN; `precut.py` exit 0; `voice-check.py`
  PASS.

## Tried and rejected

- The seed's desk memo filing the P90 method (25 weather years, a performance ratio calibrated on five years, the
  sample standard deviation): shipping it files how the decisive figure is computed, rule application; not shipped, and
  its method is rung 0b.
- Inverter clipping after a DC-to-AC rise as the decisive step: task79's driver (a conversion that falls once a
  downstream capacity binds); the repowered array is kept under the inverters' rating (SF14).
- A repowering gain that varies with the weather (temperature, low light, bifacial gain by sky): task185's conversion
  at the value and task460's weighting by output; the measured gain is used as one twelve-month figure.
- The gain's measurement uncertainty as a shared component of the P90's spread: task143 and task260's ground, and worth
  a fraction of a bin.
- A pilot block with unrepresentative old modules (a ratio against a level): a strong solver checks representativeness;
  too shallow to carry the call.
- A P90 calibrated to a fleet's out-of-sample coverage: the repowering becomes a backdrop and a one-scalar calibration
  lands it.
- A tracker wind-stow threshold lowered by larger modules: a filed threshold applied to a wind record is rule
  application, and the gust conversion a reading.
- Prototype round 1 (daily, scratch): a soiling regime change swamped by rain resets left the DC-side route 0.3 bins from
  the golden; rain cleaning made partial and the dry spring's dust cleared only by washes.
- Prototype round 2: the whole-history window with the gain landed (0.0 to 1.1 bins on five seeds) because the decline
  was spread evenly; the decline front-loaded (fast wear to 2019, the kept losses changing 2018 to 2021 and then
  steady).
- Prototype round 3: the first year's ratio on the new nameplate landed while the measured gain nearly equalled the
  kept-loss growth; the gain is set clearly above it (bifacial modules) and the kept-loss growth held near 9 per cent.
- The SCADA tag mapping across the 2020 replacement as an ask device: it touches the main call's per-inverter path;
  rejected for the asks.
- The revenue meter's transformer-loss compensation and a metering-point change as an ask device: it moves the main
  call's volume basis; rejected.
- World round 1 (hourly generator): the inverters' efficiency eased by under a point, so the soiling-aware analysis on
  AC energy sat 0.55 bins from the golden; the loss made a step per refurbished power stage (about 1.2 points each, two
  per inverter from 2018), which puts that route 1.6 bins over.
- World round 2: the one-wash years' kept losses varied by 2.7 per cent with each year's rain, so calendar 2025 or a
  multi-year base fell a bin from the last twelve months; rain cleaning made weak (the caliche dust cakes), repairs less
  variable and the station-service move put in April 2024, and the policy now files the base period (4.4).
- The repowered array at 300 strings of 18 (2,430 kWp an inverter) peaked at 100.2 per cent of rating in the record's
  sunniest hour; cut to 288 strings, 99.0.
- The 25 weather-year outputs and the P50 and standard deviation to the nearest MWh as graded figures: every defensible
  variant of the wear reading moves them by tens of MWh, so they were not uniquely forced; the prompt now asks the P50 to
  the nearest 1,000 MWh and the standard deviation to the nearest 100, and the outputs only as the note's chart.
- The forum `committee_or_panel` (a risk committee approving the volume): blocked at stage 3 against task233, which was
  registered first; the treasurer approves instead.
- Invented names near real ones (H21): Tianrun New Energy (a real Chinese energy name), the Santa Rosa district (a real
  Pinal County canal), Saguaro, Cholla and Juniper Flat plant names; renamed Corvane Solar, Vado Seco Irrigation and
  Power District, Bisnaga Ridge, Palo Fierro and Tinaja Flat.
- Ask B's "volume sold forward" read gross of the buy-backs: a second licensed reading of 2019 and 2022; the ask now says
  "net of any buy-backs".
- Stage 4, round 1 (judge APPROVE; rule-3 audit PASS with notes): the November single wash left 4 degC between the base
  period's post-wash days and 2016's, so temperature-blind reads after the washes at the AC output or the revenue meter
  landed the volume by cancelling errors (70,868 and 70,844), the uncorrected DC median landed (70,445), and the NOCT and
  per-period regression corrections took the P50 to its rounding edge (72,507 and 72,378). The wash moved to December, a
  block a week: the base period's twelve post-wash days span three weeks, no base-period day has the whole plant freshly
  washed, the uncorrected reads fall a bin or more away, and 2027's dust cycle is the base period's.
- Wear of 12 per cent let 1 per cent a year on the warranty's schedule land (70,456 to 70,834); the fast phase steepened
  to 3.85 per cent a year (wear 14 per cent), so every round rate from 0.5 to 2 per cent a year sits a bin or more away,
  and it starts in mid-2017 so a 2016-and-2017 reference stays in the bin.
- A December wash on consecutive days: the plant's meter in the week after the wash had two base-period days and sat 0.2
  bins outside, and the base period's regression slope was confounded with the blocks; replaced by a block a week.
- The six-wash era washing every other month all year: 2016's post-wash days averaged 46 degC, 15 above the December
  base, and the datasheet's coefficient applied in its first-order translation form sat 0.8 per cent under the exact
  form, beside NOCT's 0.5; the six washes moved to the cool months (January to April, October and November, as desert
  O&M crews do), 2016's post-wash days average 41 degC and every correction form sits within 0.4 per cent of the golden.
- That move left the years before one wash a year 31 MWh over the bin when carried with the gain; the spring dust now
  starts in February (the site's spring winds), which the one-wash years carry to December and the six-wash years washed
  off monthly, and the window sits 459 MWh outside.
- NOCT on the daily air temperature against a December base sat 0.7 per cent under the golden with an all-season 2016
  (summer days' irradiance spread wider than December's); the site's spring winds (calm December, windy April and May)
  and the cool-season washes take it to 0.4 per cent.
- The record's year-to-year spread at 2.35 per cent left 690 MWh where the P50's bin and the volume's overlap; a wider
  clear-sky spread between years (2.63 per cent, standard deviation 1,900) gives 950. Widening the cloudy-day frequency's
  spread instead reshuffled December 2025's weather and let the winter-matched uncorrected comparison land; rejected.
- The strict no-clipping check at the wider spread: one cloud-edge hour in April 2014 reaches 101.3 per cent of the
  inverters' rating (under 20 kWh an inverter in 25 years); the check bounds the clipped energy and the scope says the odd
  cloud-edge hour reaches the rating.
- The P50 graded to the nearest 5,000 MWh (the fallback the round-1 notes allowed): its edge at 72,500 sits beside the
  golden's P50, so the call would have had to move; not needed once every correction holds the P50 284 MWh or more
  inside its bin.
