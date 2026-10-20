# task251 design note

## Draw

Card `cards/task251.json` (architecture 2, re-rooted 2026-10-20 from architecture 1, spent at stage 4; see Tried and
rejected and the card's lineage). Guard verdict WARN, no BLOCK. The WARNs, answered: overuse.org_family
(government_agency: a provincial environment agency runs the province's air quality network, and no other kind of body
would); repeat.gate_g and overuse.gate_g (method_or_model_selection: the decisive step is the choice of the clock and the
curve the converters' wear runs on; forecasting with gap time and G16 is a signature five builds have spent, so the
honest second label was taken rather than the blocked one). The structural notes are differentiated on the card against
task148, task241, task254 and task501. Nearest driver 0.06 (task133 v1, lineage). `guard.py slots` on the candidate
driver: no slot note holds the mechanism. Architecture 1 spent the seed's world as a reference chain read through
paired readings; this draw keeps the decision (which instruments go for recalibration ahead of time) and moves the
decisive step off the reference altogether.

- **Pairing.** Physical & Environmental Sciences / sensor-calibration-measurement, drawn for Data Quality Monitoring &
  Alerting. The object is the health of the network's NO2 measurements, which a chemiluminescence analyzer makes only
  through its molybdenum converter, and the call is a monitoring decision: which analyzers' converters are changed at
  the January bench rather than at their scheduled service.
- **The seed, re-found.** DQ24 gave the world (instruments checked against references, both noisy), the decision (which
  instruments go for recalibration) and the quantity (each instrument's calibration factor against a tolerance). Its
  pitfall, the attenuated slope between two noisy instruments, is spent (task249 v1), and architecture 1's span-gas loss
  was landed by both readers. The decisive step is re-found in the data's own structure: the converter's efficiency,
  checked by gas-phase titration (two noisy measurements of one delivered NO2 step), wears with the NO2 the converter
  reduces, so its clock is the station's load and not the calendar, and the curve steepens as the molybdenum nears
  exhaustion.
- **Niche.** The Agenzia Provinciale per l'Ambiente of a fictional lower Po valley province runs the province's air
  quality network: sixteen stations, each with one chemiluminescence NOx analyzer (traffic, urban background, suburban,
  industrial and rural sites), and a spare in store. A calibration contractor titrates every analyzer's converter each
  quarter; every converter is changed at the analyzer's scheduled annual service and, under the agency's QA manual,
  earlier when a titration reads below the EN 14211 minimum of 95 per cent. In January the regional laboratory opens a
  bench for the province's converters; the agency books on it the analyzers whose converters would fall below 95 per
  cent before their scheduled 2028 service, so that no NO2 hour of the coming winter is measured through a spent
  converter.
- **The call.** Which analyzers' converters go to the January 2028 bench: those whose converter efficiency would fall
  below 95 per cent before the analyzer's scheduled 2028 service date.
- **Shape.** other: each of the 16 analyzers' verdict (16), the bench list and its count (2), the chart of each
  converter's efficiency carried to its service date against the 95 per cent line (4 or more), each station's 2027 asks
  (to be fixed at stage 2, three figures a station), the two files (2): over 70 criteria.
- **Strategy.** `forecast_method_backtest` (strategies F6: the rate is stationary only in a constructed exposure, the NO2
  the converter has reduced, rebuilt from the hourly record and the service log, and the natural fit in time fails
  forward). Gate G method_or_model_selection; generators G16 (the clock and curve the data entitle), G13 (the months to
  the service date carry a load the converter's own months did not), G6 (stations' loads differ, so a pooled curve in
  time is a mixture); gap time, population; calibration physical_verification (the titration checks); context artifact
  monitoring_export; Layer 2 field_method (exposure windows: converter life counted in NO2 reduced), pattern
  own:converter-life-in-no2-converted.
- **Forum, event, organisation.** operations_desk (the network's instrumentation desk books the bench),
  purchase_order_or_contract (the laboratory's bench is booked by list), government_agency. Role field_unit_lead (the
  head of the network's instrumentation).
- **People** (`guard.py names --geo Italy --seed 251`, locale it_IT): Livia Saracino, head of instrumentation, who asks;
  Patrizio Gilardoni, the regional laboratory's bench coordinator; Jolanda Stefanelli, the calibration contractor's
  field lead. None appears in the prompt.
- **Data-native sentence.** A molybdenum converter is spent by the NO2 it reduces, so its efficiency follows the NO2 a
  station's air has carried through it since installation, along a curve that steepens as the molybdenum nears
  exhaustion; the titration checks of every converter the network has run collapse onto that curve in NO2 reduced and
  not in months, and a converter installed in spring has seen a light summer and faces the valley's heavy winter before
  its service, while one installed in autumn faces the light months.
- **As-of.** Tuesday 4 January 2028 (the laboratory's mail); the list is due Monday 10 January, the bench runs 17 to 21
  January. The call faces forward: each converter's efficiency at a service date the record has not reached.
- **Sources.** The client's two-layer standard; EN 14211 (chemiluminescence NO2 and NO: the converter efficiency check by
  gas-phase titration and its 95 per cent minimum); the molybdenum converter's consumption in reducing NO2 (manufacturers'
  service guidance, converter life in years depending on the sampled air); the Po valley's winter NO2 maximum under
  stagnant inversions.

## Tried and rejected

- The seed's own pitfall (the errors-in-variables slope between two noisy instruments): spent by task249 v1, landed
  by its reader.
- One key, the loss per supplier (the draw as filed, prototype 4): a single insight readers enumerate once they see the
  changes' jumps, the coin-flip shape of the measured drivers (task249's five architectures each landed on one reflex);
  prototype 5 sets the loss by the cylinder's interior, which one supplier changed in 2026, so the per-supplier rate is
  a mixture and is a rung.
- The ask layer with the check hour named invalid in the manual (valid hours and hours above 350): the counts do not
  move when a dropped hour shifts by one, so a reader executing section 5 on the stamps as written kept the valid hours
  whatever the clock; measured pair 76.0. The check hour is now left to the 45-minute rule and the check's times, the
  old firmware stored ppb, and the mean joins the asks.
- Physical & Environmental Sciences, sensor calibration and measurement, shape 10, monitoring_export: BLOCKed by
  task250's shipment (pairing, subdomain, artifact) and task471 (shape); redrawn as above.
- Architecture 1 (the SO2 analyzers' gain against true SO2 read through span gas that loses SO2 with its age since
  certification at a rate the cylinder's interior sets, fitted on the 31 cylinder changes): spent 10-20 at stage 4.
  Both scored readers landed the four analyzers, each by fitting the change readings' jumps to an exponential loss from
  the certificate date and splitting on the certificates' passivation once the per-supplier fit left a 4.5 per cent
  residual; reader B also kept 32 of 33 ask figures, finding the firmware update's 2.62 level jump, the standard-time
  stamps and the unmarked check hour. The estimand's own words (gain against true SO2) sent both straight to the
  reference's truth, and the change readings measured it in one division: a chain a careful reader models, with a
  misfit that points to its second link. Judge pass 1 DETERMINISTIC, FIX_NOW (the visit edge, pinned before the
  readers came back).
