# task152: Hadley Ranch Solar, the 2027 forward sale at the one-year P90 after the module replacement (architecture 1)

Private, never ships. A new build (wave 4), numbered from seed FC23. The seed (a corporate buyer's 40 MW solar plant,
hedged a year ahead at the one-year P90, its original modules replaced on the same racking and inverters, the work
finishing in December) was read at its header and Situation only. Its world, decision and quantity are kept. Its desk
memo, which files the P90 method (25 weather years, a performance ratio calibrated on five years, the sample standard
deviation), is not shipped: filing how the decisive figure is computed is rule application. The pitfall is re-found
from how a solar plant's monitoring records come to exist: the inverters log the DC energy the array delivers and the AC
energy they put out, the pyranometer logs the irradiation the array receives, and the array between them carries both
its modules' own wear and the dust it gathers between washes, which the washes and the heavier rains clear and the
months between them rebuild.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task152.json`, architecture v1, registered 2026-10-16; `guard.py check` WARN (overuse.objective, repeat.decision, repeat.question_form), answered below; the older same-driver signature (time, G4, decomposition_attribution) against task232 differentiated on the card, with lines against task127 v2, task187, task132, task185, task460, task136, task260, task30 and task68; nearest drivers 0.04 (task459, task230 v3, task132) |
| Domain / task type | `energy-systems-utilities` (client domain), task type `asset-condition-maintenance` (serves Forecasting): what an asset's condition is now, what a maintenance action restores and what the asset will produce after it. The seed's label (Economics, corporate energy procurement) is a backdrop the taxonomy places elsewhere: Economics is macro, labour, trade and fiscal reads, and the deciding quantity here is the plant's own performance after a module swap |
| Objective | Forecasting & Predictive Modeling: the plant's 2027 energy at its one-year P90, a calendar year not yet begun, built from the plant's own monitoring history and the long-term irradiance record |
| Shape | `single-figure`: the volume sold forward, with the P50 and standard deviation it rests on and the plant's 2027 output in each of the 25 weather years the P-values are taken over (25 + 3 criteria), the note's chart, and two ask tables (counted in `## Ask sheet`) |
| Decision | `quantity_figure`, answer unit `count` (MWh, rounded down to the nearest 1,000) |
| Mechanism | gap time (decisive: the plant's record is a statement about its original modules under a wash regime that changed; the sale bets on new modules under today's regime) with population (which part of the record's decline belongs to the part replaced); pattern none; generators G4 (attribution at the replacement: which losses leave with the old modules and which the plant keeps), G16 (the wear estimator the data entitles: the decline of the freshly washed states at the inverters' DC input, against the decline of every day's output), G13 (the hedge year, the first year of new modules under the current cleaning contract); Gate G `decomposition_attribution`; strategy `decomposition_attribution` |
| Layer 2 family / pattern | `estimation_fit` (decomposition: a soiling loss and a wear loss read apart, the way PV degradation studies read them); `own:module-wear-net-of-soiling-at-the-inverter-dc-boundary` |
| Furniture | forum `committee_or_panel` (the treasury risk committee approves the hedge volume), forcing event `purchase_order_or_contract` (the 2027 forward sale confirmation), organisation family `manufacturer`, role family `procurement_lead` (the energy and commodities manager), context artifact `monitoring_export` (the plant's SCADA export), calibration `none`, opening `question-first`, question form `how-much` |
| Spine | the plant SCADA's daily inverter export, one row per central inverter per day (DC energy in, AC energy out, hours online), with the plant pyranometer's plane-of-array irradiation and the back-of-module temperature: the original system's CSV to March 2020, then the replacement system's export (constructed, about 63,500 rows) |
| Deliverables | `hedge_volume_2027.xlsx` (the volume, the P50 and standard deviation, the 25 weather-year outputs, the performance build, the two ask tables) and `hedge_note_2027.pdf` (a one-page note for the risk committee with a chart of the weather-year outputs, the P50 and the volume); the format set rotates away from task151 (docx), task150 (png) and task148 (png) |
| People | drawn with `guard.py names --geo "United States" --seed 152 --n 70` (first names and surnames checked clean against every card): Kristopher Lara (energy and commodities manager, brings the request; not in the prompt), Selena Sloan (the company's solar asset manager, keeps the SCADA exports), Caroline Barnett (treasurer, owns the energy risk policy), John Davila (the O&M contractor's site supervisor, the work orders), Laurie Howell (the module supplier's field test engineer, the side-by-side test report), Isabel Shaw (the district's meter data analyst) |

**Guard.** `guard.py check` on the registered card: WARN `overuse.objective` (Forecasting in 8 of the last 12: this is
the Forecasting lane), `repeat.decision` (a quantity figure, as task151: the decision is a volume, and the two share no
other axis: task151 accrues a stepped bonus on season totals, here a plant's forward energy) and `repeat.question_form`
(how-much, as task151: a volume is asked as how much). The first draft blocked on the older same-driver signature (time,
G4, decomposition_attribution) against task232, which attributes later outcomes to an exposure by a delay window;
differentiated on the card (here a unit's own decline is split by where each loss arises and by the cycle that resets one
of them, and nothing is timed against an exposure). Two personas first drawn (first names used in task73 and task130)
were replaced from the same seed's list.

**Same-puzzle and same-driver tests.** Gap time, decisive G4, decision `quantity_figure`, Gate G
`decomposition_attribution`: no build in the last twelve (task144 to task151) carries either triple (task149 is time,
G14, quantity_figure, method_or_model_selection; task148 time, G16; task150 time, G6; task145 time, G16; task461 time,
G13). The one older same-driver match, task232, carries its differentiation.

**Abstraction test.** Stripped of nouns: the forward level after a worn part is replaced is the present output restored
by the part's own wear only; that wear is the decline of the unit's just-reset states read at the boundary inside the
unit that leaves out the losses the replacement keeps, because the average output also carries a loss that accumulates
between recurring resets and whose mean grew as the resets grew rarer. The nearest by mechanism, read for latent
structure rather than score:
- task127 v2 removes the replaced step's excess over a concurrent wait (a max of parallel steps found by joining two
  logs); here the losses are a serial chain and one of them cycles.
- task187 ranks units on a shortfall read at matched turbulence (a capped curve averaged over a spread); here one unit's
  level is rebuilt after a swap, and nothing is ranked.
- task132 forecasts failures through a renewal process (a replacement restarts the wear curve); here the restart is
  given and the question is which of the old losses it clears.
- task46 carries a rate stationary in cumulative exposure; here no rate is carried, a level is split.
- task185 converts a history across an instrument change at the value converted; here no history is converted.
None shares the latent structure, the default path and the correction.

**Data-native sentence.** Hadley Ranch's inverters log, every day, the DC energy its 128,000 original modules delivered
and the AC energy they put out, beside the irradiation the pyranometer saw: the DC energy per unit of irradiation falls
for two reasons the daily figure cannot tell apart, the modules' own backsheet wear, which only rises, and the dust the
array carries between washes, which each full wash clears and the dry spring rebuilds, and which grew as the washes fell
from six a year to one under the Colorado River shortage; the wear is the decline of the freshly washed days alone, and
the module replacement clears it while the dust regime, the inverters' lost efficiency and their lost availability stay.

**Sources read, one line each.**
- `guard.py mechanisms --objective forecasting` (63 builds): the nearest spent ground is renewal after replacement
  (task132), a rate in constructed exposure (task46), a shortfall read at matched conditions (task187, anomaly) and a
  removed step's excess over a kept one (task127 v2); none splits one unit's decline across an internal boundary and a
  reset cycle, and none is a plant performance level carried through a part swap.
- The kinship cards the brief names: task136 (staggered bulk-buy counterfactual), task460 (operating margin weighted by
  output), task185 (instrument conversion at the value), task260 (crossed-sample gain interval), task30 (a gap carried
  from parallel cases), task68 (a matched-panel change). The seed's own mechanism, a gain measured side by side, is kept
  only as a shipped measurement (the side-by-side test's gain is an input, read as given); the decisive step is not the
  comparison but what the measured gain multiplies.
- `two-layer-task-design.md`: "the data's real structure" and "the right comparison" are the client's frames; the soiling
  and wear split is estimation that fits the data (decomposition).
- `layer2-rigor-patterns.md`: Energy Systems & Utilities has no patterns; general statistics' "covariate error" and
  "resample the independent unit" lines were read and are not the move here.
- task148's design note and its `## Tried and rejected` (the one-scalar calibration family that landed its call): here
  the history-calibrated family is swept window by window in `## Ladder`.

**World.** Marden-Vail Building Products (fictional), a Phoenix-based maker of gypsum wallboard and joint compound with
plants in Arizona and New Mexico, built Hadley Ranch Solar (fictional), a 40 MWac fixed-tilt plant in Pinal County, in
2015 (commercial operation 20 November 2015) to hedge its own electricity cost: sixteen 2.5 MW central inverters, each
fed by 8,000 original 315 W polycrystalline modules (40.32 MWp), on south-facing tables at 25 degrees. The plant
exports to the Santa Rosa Irrigation and Power District's 69 kV substation and its output is sold at the Palo Verde hub;
each autumn the company's energy and commodities desk sells the next calendar year's output forward at its one-year P90,
under the treasury's energy risk policy, with the risk committee approving the volume. Tresco Field Services (fictional)
has run the plant's operations and maintenance since commercial operation; it has repowered five similar plants since
2019. From 2019 the original modules' backsheets began cracking and the plant's output fell faster each year; the
company is replacing every module with 93,700 bifacial 450 W modules from Tianrun New Energy (fictional) on the
existing tables, strings re-run to the same sixteen inverters (42.165 MWp), the work running from October to December
2026. Washing was cut as water became scarce: six full washes a year to 2018, four in 2019, two in 2020 and one each
November since 2021, the schedule the current O&M contract keeps to the end of 2027. From October 2025 to September 2026
Tianrun's field engineer ran a side-by-side test inside the array: one table of the new modules beside one table of
unexposed original modules from the site store, each on its own string inverter, both washed weekly.
