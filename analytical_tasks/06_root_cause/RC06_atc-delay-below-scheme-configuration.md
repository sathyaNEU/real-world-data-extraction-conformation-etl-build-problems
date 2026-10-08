# RC06 — How the performance plan should characterise a summer of tripled en-route delay, when every regulation's reason code is right

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · air traffic flow management |
| Mirrors | Capacity incidents where every "capacity" alert is correct and the shortfall is self-inflicted upstream (cloud regions serving on fewer shards than the scaling plan calls for because on-call rosters were thin, fulfilment centres opening fewer pick lanes than the labour plan, contact centres staffed below the Erlang plan) |
| Decision shape | A structure the body adopts: the characterisation of the summer's regulated delay that the performance plan files |
| Committed call | The material mechanisms (10% or more of the summer's regulated delay) and each one's share, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S7 (every screen is right and the answer is what nothing flags: below-scheme configuration hours, a sequence construction), with E16 (finer controls separate constructions) at rung 2 |
| Gate G mechanism | decomposition_attribution, with method_or_model_selection |
| Measured traps engaged | #12 stops at the first control that passes · #11 beats the headline trap, misses the quiet one · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the network manager's close-out of last summer's delay for the centre, by class, month and weekday |
| Driving force | A regulation is coded "capacity" whenever demand exceeds the configuration actually open, which is correct under the coding guide. This summer the roster plan, thinned by retirements, often could not open the configuration the opening scheme sets for the forecast demand. No code, flag or column marks those hours; they appear only when the day's configuration sequence is rebuilt against the scheme, hour by hour, under its transition limit. Last summer's close-out cannot see them, because the roster plan covered the scheme in every closed hour. |

## 1. Situation

An area control centre's summer en-route delay tripled, from 410,000 to 1,240,000 minutes, on 4.5% more flights. The press has settled on sick calls;
the capacity planners say five per cent more traffic does this to a centre near saturation; the network manager's monitor codes most regulations
"capacity". The national supervisory authority requires the centre's performance plan to adopt one characterisation of the summer's delay: which
mechanisms matter and how much each carries. Corrective actions and their owners follow from it.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each regulation's reason code under the coding guide, the convective flags, the sick-call log, the
  configuration log, the opening scheme, the roster plan and last summer's close-out. The press, the planners and the network manager each
  describe something real. Nothing is overturned; the task is to find a population no screen expresses and file the structure it implies.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the press line, both voices and the licensed basis. The monitor's codes, the close-out's method and the saturation
  model still return complete, reconciling partitions without a configuration class.
* **Instrument repair.** Make every code perfect under the coding guide: it already is. A better reason-code instrument still codes the hours
  "capacity", because demand did exceed the configuration open; the shortfall lives in the sequence of configurations, not in any regulation.
* **Lens swap.** The monitor classifies regulations; the answer classifies regulated hours by what the roster plan let the centre open: a
  population built at a grain (configuration sequences) the monitor never records.

## 3. The driving force

A strong solver distrusts the codes, reproduces last summer's close-out, and finds that its finer cells (month by class, weekday by class) are
reproduced only when convective hours coded "capacity" move to weather and hours whose planned configuration failed on the day because of sick
calls move to staffing. Applied to this summer, that method gives a three-class structure led by capacity. It is the method the close-out
certifies, and it is incomplete. The opening scheme in the operations manual sets, for each hour's forecast demand band, the configuration to
open, moving at most two sectors an hour. This summer the roster plan itself often staffed six of the eight afternoon sectors the scheme
required. Those hours are regulated, correctly coded "capacity", and absent from the sick-call log because nobody called in sick. They emerge
only when the scheme's configuration sequence is rebuilt for each day from the forecast and set against the configuration log. Under the plan's
crediting rule (an hour belongs to the mechanism without which it would not have been regulated) they belong to the configuration shortfall,
which carries 54.0% of the summer.

## 4. The ladder

| Rung | Construction | Adopts | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Delay by the monitor's reason code | Capacity 66.9%, weather 21.8% (two classes) | The network manager's own coding, complete and reconciled | The close-out's month-by-class cells: raw codes miss 31 of its 40 finer cells |
| 1 | Last summer's delay–traffic curve, extrapolated to this summer's traffic at declared capacity, weather days split out | Traffic saturation 47.6%, unexplained 30.6%, weather 21.8% (three classes) | The planners' nonlinear argument, built properly | The close-out's finer cells again: the curve misses 36 of 40, and a 30.6% residual is not a mechanism |
| 2 | The close-out's own method: codes, with convective hours moved to weather and same-day sick-call hours moved to staffing | Capacity 50.8%, weather 25.0%, staffing 16.1% (three classes) | It reproduces all 40 finer cells of the close-out, which raw codes and the curve miss | The opening scheme and the roster plan: in 1,880 regulated hours the configuration open was below the scheme's for the forecast demand with no sick call behind it |
| 3 | **Decisive:** each day's scheme configuration sequence rebuilt from the forecast under the transition limit, set against the configuration log, and each regulated hour credited by the plan's rule | **Configuration shortfall 54.0%, weather 25.0%, saturation at scheme 12.9% (three classes)** | — | — |

* **Structure table.** The answer's leading class holds 0% on rungs 0–2, because no code, flag or log names it; it sits inside "capacity" and,
  for sick-call hours, inside "staffing". Every wrong structure differs from the answer in at least one material class, and every partition sums
  to the same 1,240,000 minutes.
* **Discriminator dominance.** Rung 2's capacity class carries a 2.03× lead over the next class into rung 3 (630,000 against weather's
  310,000 minutes). The rebuilt sequence moves 75% of it (470,000 minutes) and all 200,000 sick-call minutes into the shortfall, which then
  leads saturation at scheme by 4.19×, above the required 1.2 × 2.03 = 2.44; the net margin is 2.06×.
* **Partial correction priced (L3).** Comparing the open configuration with the centre's maximum rather than the scheme books forecast-band
  hours run correctly at seven sectors as shortfall: 63.7% shortfall and 3.2% saturation, a two-class structure. Rebuilding the scheme without
  its two-sectors-an-hour limit gives 58.1% and 8.9%, again two classes. Both land on a different structure from the answer.
* **Grid.** Classification (codes, curve, close-out method, sequence) × configuration reference (none, maximum, scheme without limit, scheme
  with limit) gives six feasible builds, because only the sequence construction uses a reference, and five distinct structures (the maximum
  and the unlimited scheme both file shortfall and weather alone, at 63.7% and 58.1%). Only the scheme with its limit yields shortfall, weather
  and saturation all at 10% or more.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The coding guide defines the codes, the operations manual files the opening scheme, the roster plan lists rostered
   positions. No document compares them or names a configuration class.
2. **Corpus blind for a computable reason.** *In every hour of last summer the roster plan covered the scheme's configuration, because the
   spring course had just qualified fourteen controllers, so the only below-scheme hours were same-day sick calls and the close-out cannot tell
   "sick call" from "below scheme".* Both rules reproduce its 40 finer cells exactly; they part company only this summer.
3. **No arithmetic symptom.** Every structure is a complete partition of the same regulated hours: the total, the flight counts and the
   regulation counts tie under all of them.
4. **Not a row predicate.** The scheme configuration for an hour depends on the forecast band and on the previous hour's configuration through
   the transition limit, so it is a sequence rebuilt day by day before any hour is compared.
5. **The enumeration is arithmetic.** The 1,880 below-scheme hours are built from the forecast, the scheme, the configuration log and the roster
   plan; no column marks them.
6. **No cutover date.** The roster was short from the first day of summer; the dated event in the window (a sector redesign on 15 July) is a
   decoy that steps two sectors' delay down.
7. **Survives deletion.** With every voice removed, the close-out method still files capacity, weather and staffing.

## 6. The calibration corpus

* **Form.** The network manager's close-out of last summer for the centre: season delay (410,000 minutes) by class, by month and class, and by
  weekday and class, labelled in-file as last summer's characterisation, with the corrective actions it adopted.
* **What it certifies.** The convective and sick-call reclassifications (rung 2): the season total is reproduced by every construction, the 40
  finer cells only by the close-out method and by the below-scheme rule, which coincide on last summer.
* **What it is blind to.** Planned shortfall (above).
* **Twin pair.** Two Tuesdays this summer, 9 and 16 July, carry identical traffic, forecast bands, code mixes and no convective hours or sick
  calls. Delay was 21,000 and 10,400 minutes (2.0×), because on the 9th the roster plan staffed six of the scheme's eight afternoon sectors.
  Only the rebuilt sequence separates them.
* **Resemblance points at the decoy.** This summer's worst days match last summer's high-traffic weekend days on every code and traffic column,
  and the close-out booked those to capacity.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The authority's plan template: a regulated hour is credited to the mechanism without which it would not have been regulated,
  and a mechanism is material at 10% of the season's regulated delay. The operations manual's opening scheme (forecast band to configuration,
  at most two sectors' change an hour).
* **Empirical pins.** The close-out's reclassification rules, recovered from its finer cells.
* **Voices.** The capacity planner: "We're at saturation; five per cent more traffic does exactly this to a convex curve." The network
  manager's liaison: "The codes are right. Capacity was what bound on those days."
* **Licensed wrong basis.** The template records that the network manager presents each centre's delay by regulation reason code and will
  table that view at the plan review.

## 8. Determinism by construction

* **Grain.** Regulated hours; a regulation spanning part of an hour is split by minute.
* **Scheme rebuild.** The forecast file is the D-1 forecast the scheme uses; the transition limit is applied from the night configuration at
  05:00; ties in the band table do not occur.
* **Exclusive credit.** By construction no convective hour is below scheme (the weather procedure opens the full scheme whenever convection is
  forecast), and every regulated hour has exactly one mechanism without which it would not have been regulated.
* **Materiality.** No class sits within two points of the 10% line under any construction.
* **Rounding.** Shares to one decimal; every committed share sits mid-bin.

## 9. Prompt sketch and deliverables

> The authority wants our summer characterised in the performance plan: which mechanisms mattered, and how much of the summer's regulated delay
> each one carries. The minister's office has decided it was sick calls. Give me the characterisation the plan should adopt, the mechanisms at
> 10% or more and each one's share to one decimal, as the paragraph I paste into the plan. Send `delay_characterisation.xlsx` and a chart
> `scheme_gap.png`.

* `delay_characterisation.xlsx` — the four structures with every class's minutes, the sector-entry sheet (ask A), the flight-efficiency sheet
  (ask B) and the close-out reproduction (ask C).
* `scheme_gap.png` — a heatmap of summer weekdays by hour showing sectors open minus the scheme's configuration, with regulated delay overlaid
  as contour lines, convective hours hatched, the 9 and 16 July rows outlined, and a side bar of the adopted shares.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 sectors and each summer week, flights entered. *Device:* the sector-entry log writes
  a row for every entry, and flights that leave and re-enter a sector on a climb-out appear twice under one flight id, as the log's
  specification documents; the performance report counts flights, and counting rows inflates three sectors by 6–9%.
* **Ask B (device-carried).** For each summer week, the horizontal en-route extension of flights through the centre. *Device:* replanned
  flights carry several flight-plan versions with a sequence number, and the extension indicator uses the last version filed before take-off, as
  the indicator's definition documents; using the first version overstates extension in the weeks with most re-routing.
* **Ask C (validity).** The close-out's 40 finer cells as published and as reproduced by each of the four constructions; and each construction's
  structure for this summer.
* **Decoupling.** Clearing the scheme rebuild changes no figure in asks A or B; sector entries and flight-plan versions never enter the
  regulated-hour credit.

## 11. Rubric arithmetic

14 sectors × 13 weeks (ask A) + 13 weeks (ask B) + 40 cells × 4 constructions (ask C) + the adopted classes and their three shares, the
below-scheme hours and the runner-up structure + 5 named chart parts + 2 files ≈ 375 criteria.

## 12. World-building constraints

* This summer 1,240,000 minutes: below-scheme 670,000 (470,000 planned, 200,000 on sick-call days), convective 310,000 (40,000 of it coded
  capacity), saturation at scheme 160,000, other 100,000. Codes: capacity 830,000, weather 270,000, staffing 40,000, other 100,000.
* The curve extrapolation predicts 590,000 from traffic at declared capacity; weather days 270,000.
* 1,880 regulated hours below scheme with no sick call; 120,000 minutes in forecast-band hours run at the scheme's seven sectors.
* Last summer the roster plan covered the scheme in every hour; its close-out's 40 finer cells are reproduced by the close-out method and the
  below-scheme rule alike, by raw codes in 9 and by the curve in 4.
* 9 and 16 July are identical on every traffic, forecast, code and sick-call column.
* Re-entry rows and flight-plan versions touch no regulated hour, configuration row or roster entry.
