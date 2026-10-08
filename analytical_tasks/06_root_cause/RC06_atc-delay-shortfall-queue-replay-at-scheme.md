# RC06 — How the performance plan should characterise a summer of tripled en-route delay, when every regulation's reason code is right

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · air traffic flow management |
| Mirrors | Capacity incidents where every "capacity" alert is correct and part of the shortfall is self-inflicted upstream (cloud regions serving on fewer shards than the scaling plan calls for because on-call rosters were thin, fulfilment centres opening fewer pick lanes than the labour plan, contact centres staffed below the Erlang plan), and where the backlog a short hour builds outlives it while some of the short hours would have queued anyway |
| Decision shape | A structure the body adopts: the characterisation of the summer's regulated delay that the performance plan files |
| Committed call | The material mechanisms (10% or more of the summer's regulated delay) and each one's share, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S7 (every screen is right and the answer is what nothing flags: each day's queue replayed hour by hour at the opening scheme's configuration, a sequence construction that separates the minutes a configuration shortfall added from those the scheme would have produced), with E16 (finer controls separate constructions) at rung 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #12 stops at the first control that passes · #11 beats the headline trap, misses the quiet one · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the network manager's close-out of last summer's delay for the centre, by class, month and weekday |
| Driving force | A regulation is coded "capacity" whenever demand exceeds the configuration open, which is correct; this summer the roster plan often could not open the configuration the opening scheme sets for the forecast demand. Rebuilt hour by hour, the hours below scheme carry 62% of the delay. The plan template credits each minute to the mechanism without which it would not have occurred. In the afternoon peaks demand exceeded even the scheme's configuration, and queues built in short hours before the peak carried into hours run at scheme. Only each day's queue replayed at the scheme configuration, unserved flights carried forward, separates the minutes the shortfall added from those the scheme would have produced. |

## 1. Situation

An area control centre's summer en-route delay tripled, from 410,000 to 1,240,000 minutes, on 4.5% more flights. The press has settled on sick calls;
the capacity planners say five per cent more traffic does this to a centre near saturation; the network manager's monitor codes most regulations
"capacity". The national supervisory authority requires the centre's performance plan to adopt one characterisation of the summer's delay: which
mechanisms matter and how much each carries. Corrective actions and their owners follow from it.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each regulation's reason code under the coding guide, the convective flags, the sick-call log, the
  configuration log, the opening scheme and its declared capacities, the roster plan, the flight-level delays and last summer's close-out. The
  press, the planners and the network manager each describe something real. Nothing is overturned; the task is to find a population no screen
  expresses and file the structure it implies.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the press line, both voices and the licensed basis. The monitor's codes, the close-out's method and the hourly
  rebuild still return complete, reconciling partitions, none with saturation at scheme material.
* **Instrument repair.** Suspect file: the regulation reason code, which records what bound in the hour (demand over the configuration open),
  not why the configuration was what it was. Repaired so that every regulated hour carries the mechanism binding in it (below scheme by the
  roster plan or by a sick call, convection, saturation at scheme), rung 0 files the shortfall at 62.1% and weather at 25.0%, as rung 3 does;
  rung 2 files the planned shortfall at 46.0%, weather 25.0% and staffing 16.1%; rung 1 reads no codes and is unchanged. None files the answer.
  The template credits minutes, not hours: no hourly label, however exact, splits an hour's delay between the shortfall and what the scheme
  would have produced, or moves a queue's minutes back to the hour that built it.
* **Lens swap.** The monitor classifies regulations; the answer classifies delay minutes by the queue the scheme configuration would have
  carried: a population built at a grain (each day's replayed queue) the monitor never records.

## 3. The driving force

A strong solver distrusts the codes, reproduces last summer's close-out, and finds that its finer cells are reproduced only when convective hours
coded "capacity" move to weather and hours whose planned configuration failed on the day because of sick calls move to staffing. That method is
certified and incomplete. The opening scheme sets, for each hour's forecast demand band, the configuration to open, moving at most two sectors an
hour, and this summer the roster plan itself often staffed six of the eight afternoon sectors the scheme required. Rebuilding each day's scheme
sequence against the configuration log finds those hours, correctly coded "capacity" and absent from the sick-call log, and credits them 62.1% of
the summer. The plan template credits minutes, not hours. In 41% of the below-scheme hours demand exceeded even the scheme configuration's
declared capacity, so part of their delay would have occurred at scheme; and queues built in short hours before the afternoon peak carried into
hours run at scheme. Replaying each day's queue hour by hour at the scheme configuration, flights not served carried forward in arrival order,
credits the configuration shortfall with 41.9% of the summer, saturation at scheme with 27.4% and weather with 25.0%.

## 4. The ladder

| Rung | Construction | Adopts | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Delay by the monitor's reason code | Capacity 69.4%, weather 21.8% (two classes) | The network manager's own coding, complete and reconciled | The close-out's month-by-class cells: raw codes miss 31 of its 40 finer cells |
| 1 | Last summer's delay–traffic curve, extrapolated to this summer's traffic at declared capacity, weather days split out | Traffic saturation 47.6%, unexplained 30.6%, weather 21.8% (three classes) | The planners' nonlinear argument, built properly | The close-out's finer cells again: the curve misses 36 of 40, and a 30.6% residual is not a mechanism |
| 2 | The close-out's own method: codes, with convective hours moved to weather and same-day sick-call hours moved to staffing | Capacity 53.2%, weather 25.0%, staffing 16.1% (three classes) | It reproduces all 40 finer cells of the close-out, which raw codes and the curve miss | The opening scheme and the roster plan: in 1,880 regulated hours the configuration open was below the scheme's for the forecast demand with no sick call behind it |
| 3 | Each day's scheme configuration sequence rebuilt from the forecast under the transition limit, set against the configuration log, each regulated hour below scheme credited to the shortfall | Configuration shortfall 62.1%, weather 25.0% (two classes) | Every hour the roster left short is found, and the close-out's 40 cells still reproduce | The declared capacities: in 41% of below-scheme hours demand exceeded even the scheme configuration's capacity |
| 4 | **Decisive:** each day's queue replayed hour by hour at the scheme configuration, unserved flights carried forward, each minute credited by the plan's rule | **Configuration shortfall 41.9%, saturation at scheme 27.4%, weather 25.0% (three classes)** | — | — |

* **Structure table.** Saturation at scheme is material only in the answer: it holds 0% on rungs 0–2, where no code, flag or log names it, and
  7.3% on rung 3, which files the shortfall 20.2 points above the answer. Every wrong rung differs from the answer in a material class, and every
  partition sums to the same 1,240,000 minutes.
* **Discriminator dominance.** Rung 3 carries the shortfall at 2.48× weather into rung 4 (770,000 against 310,000 minutes), with saturation at
  scheme at 90,000. The replay moves 330,000 of the shortfall's minutes to saturation and 80,000 carried minutes back, so saturation rises 3.8×
  to 340,000 while weather stays put, and crosses the 10% line by 17.4 points.
* **Partial correction priced (L3).** Splitting each below-scheme hour's minutes by the demand above the scheme's capacity, hour by hour, without
  carrying the queue, leaves the carried minutes with saturation: shortfall 35.5%, saturation 33.9%, weather 25.0%, each share 6.4 to 6.5 points
  off. Replaying at the centre's maximum configuration rather than the scheme books hours run correctly at seven sectors as shortfall: shortfall
  66.9% and weather 25.0%, two classes.
* **Grid.** Construction (codes, curve, close-out method, hourly rebuild, minute replay, minute split without carry) × configuration reference
  (scheme with its limit, scheme without it, maximum; rebuild and replay only) gives ten feasible builds. Without the limit the replay files
  46.8%, 22.6% and 25.0%; at the maximum the rebuild and the replay both file two classes. Only the replay at the scheme with its limit,
  carrying the queue, files 41.9%, 27.4% and 25.0%.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The coding guide defines the codes, the operations manual files the opening scheme and its capacities, the roster plan
   lists rostered positions, and the template credits minutes by the mechanism without which they would not have occurred. No document compares
   the configurations, replays a queue or names a configuration class.
2. **Corpus blind for a computable reason.** *In every hour of last summer the roster plan covered the scheme's configuration, because the
   spring course had just qualified fourteen controllers, so no closed hour was below scheme without a sick call and no queue built by a planned
   shortfall carried into a later hour.* The close-out method, the hourly rebuild and the minute replay all reproduce its 40 finer cells; they
   part company only this summer.
3. **No arithmetic symptom.** Every structure is a complete partition of the same regulated minutes: the total, the flight counts and the
   regulation counts tie under all of them.
4. **Not a row predicate.** The scheme configuration for an hour depends on the previous hour's through the transition limit, and an hour's
   delay at scheme depends on the queue the replay carries into it, so both are sequences rebuilt day by day.
5. **The enumeration is arithmetic.** The 330,000 minutes that would have occurred at scheme and the 80,000 carried into later hours come out
   of the replay; no column marks them.
6. **No cutover date.** The roster was short from the first day of summer; the dated event in the window (a sector redesign on 15 July) is a
   decoy that steps two sectors' delay down.
7. **Survives deletion.** With every voice removed, the close-out method still files capacity, weather and staffing.

## 6. The calibration corpus

* **Form.** The network manager's close-out of last summer for the centre: season delay (410,000 minutes) by class, by month and class, and by
  weekday and class, labelled in-file as last summer's characterisation, with the corrective actions it adopted.
* **What it certifies.** The convective and sick-call reclassifications (rung 2): the season total is reproduced by every construction, the 40
  finer cells only by the close-out method, the hourly rebuild and the minute replay, which coincide on last summer.
* **What it is blind to.** Planned shortfall and the queues it carries (above).
* **Twin pair.** Two Tuesdays this summer, 9 and 16 July, carry identical traffic, forecast bands, code mixes, delay totals and below-scheme
  hours, and no convective hours or sick calls. The shortfall's minutes were 14,000 and 7,000 (2.0×): on the 9th the short hours fell before
  the afternoon peak and their queue carried into it, on the 16th they fell inside the peak, where demand exceeded even the scheme. The hourly
  rebuild gives both days the same figure; only the replay separates them.
* **Resemblance points at the decoy.** This summer's worst days match last summer's high-traffic weekend days on every code and traffic column,
  and the close-out booked those to capacity.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The authority's plan template: a minute of regulated delay is credited to the mechanism without which it would not have
  occurred, and a mechanism is material at 10% of the season's regulated delay. The operations manual's opening scheme (forecast band to
  configuration, at most two sectors' change an hour) and each configuration's declared capacity.
* **Empirical pins.** The close-out's reclassification rules, recovered from its finer cells.
* **Voices.** The capacity planner: "We're at saturation; five per cent more traffic does exactly this to a convex curve." The network
  manager's liaison: "The codes are right. Capacity was what bound on those days."
* **Licensed wrong basis.** The template records that the network manager presents each centre's delay by regulation reason code and will
  table that view at the plan review.

## 8. Determinism by construction

* **Grain.** Regulated delay minutes, flight by flight; a regulation spanning part of an hour is split by minute.
* **Scheme rebuild.** The forecast file is the D-1 forecast the scheme uses; the transition limit is applied from the night configuration at
  05:00; ties in the band table do not occur.
* **Replay.** Each day's demand is replayed hour by hour at the scheme configuration's declared capacity, flights not served in an hour carried
  to the next in arrival order; the shortfall's minutes are the actual delay less the replayed delay.
* **Exclusive credit.** By construction no convective hour is below scheme (the weather procedure opens the full scheme whenever convection is
  forecast), convective queues clear within their hours, and every minute has exactly one mechanism without which it would not have occurred.
* **Materiality.** No class sits within two points of the 10% line under any construction.
* **Rounding.** Shares to one decimal; every committed share sits mid-bin.

## 9. Prompt sketch and deliverables

> The authority wants our summer characterised in the performance plan: which mechanisms mattered, and how much of the summer's regulated delay
> each one carries. The minister's office has decided it was sick calls. Give me the characterisation the plan should adopt, the mechanisms at
> 10% or more and each one's share to one decimal, as the paragraph I paste into the plan. Send `delay_characterisation.xlsx` and a chart
> `scheme_gap.png`.

* `delay_characterisation.xlsx` — the five structures with every class's minutes, the sector-entry sheet (ask A), the flight-efficiency sheet
  (ask B) and the close-out reproduction (ask C).
* `scheme_gap.png` — a heatmap of summer weekdays by hour showing sectors open minus the scheme's configuration, with actual and replayed delay
  overlaid as contour lines, convective hours hatched, the 9 and 16 July rows outlined, and a side bar of the adopted shares.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 sectors and each summer week, flights entered. *Device:* the sector-entry log writes
  a row for every entry, and flights that leave and re-enter a sector on a climb-out appear twice under one flight id, as the log's
  specification documents; the performance report counts flights, and counting rows inflates three sectors by 6–9%.
* **Ask B (device-carried).** For each summer week, the horizontal en-route extension of flights through the centre. *Device:* replanned
  flights carry several flight-plan versions with a sequence number, and the extension indicator uses the last version filed before take-off, as
  the indicator's definition documents; using the first version overstates extension in the weeks with most re-routing.
* **Ask C (validity).** The close-out's 40 finer cells as published and as reproduced by each of the five constructions; and each construction's
  structure for this summer.
* **Decoupling.** Clearing the replay changes no figure in asks A or B; sector entries and flight-plan versions never enter the credited
  minutes.

## 11. Rubric arithmetic

14 sectors × 13 weeks (ask A) + 13 weeks (ask B) + 40 cells × 5 constructions (ask C) + the adopted classes and their three shares, the
replayed minutes and the runner-up structure + 5 named chart parts + 2 files ≈ 410 criteria.

## 12. World-building constraints

* This summer 1,240,000 minutes: below-scheme hours 770,000 (570,000 planned, 200,000 on sick-call days), convective 310,000 (40,000 of it coded
  capacity), regulated hours at scheme 90,000, other 70,000. Codes: capacity 860,000, weather 270,000, staffing 40,000, other 70,000.
* The replay: 330,000 of the below-scheme minutes would have occurred at scheme, and 80,000 of the at-scheme minutes are queues carried from
  below-scheme hours. Answer: shortfall 520,000, saturation at scheme 340,000, weather 310,000, other 70,000.
* Partials: hourly split without carry 440,000 and 420,000; scheme without its limit 580,000 and 280,000; maximum configuration 830,000 and
  30,000 (shortfall and saturation).
* The curve extrapolation predicts 590,000 from traffic at declared capacity; weather days 270,000.
* 1,880 regulated hours below scheme with no sick call; in 41% of below-scheme hours demand exceeded the scheme configuration's capacity.
* Last summer the roster plan covered the scheme in every hour; its close-out's 40 finer cells are reproduced by the close-out method, the hourly
  rebuild and the replay alike, by raw codes in 9 and by the curve in 4.
* 9 and 16 July are identical on every traffic, forecast, code, sick-call, delay-total and below-scheme-hour column.
* Re-entry rows and flight-plan versions touch no regulated minute, configuration row or roster entry.
