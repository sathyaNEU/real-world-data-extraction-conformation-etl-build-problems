# DA30 — The share of a cable provider's households that get their plan speed at peak, when peak belongs to each household's network node

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Policy & Education · telecom consumer-protection regulation |
| Mirrors | Service-level reporting where "peak" is a property of the shared resource rather than the clock (cloud region capacity windows, CDN edge busy hours, marketplace and ride-hail demand zones), so a fixed reporting window misses the hours that bind |
| Decision shape | One figure committed at a date: the household figure the agency publishes for Coastline Cable in the annual broadband report |
| Committed call | The share of Coastline Cable's panel households receiving at least 80% of their plan speed at peak, to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B (a reproduction gate over the pilot's filed decisions), with a saturated tie broken by a documented rule at rung 2 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #1 reports a failed back-test, ships anyway · #19 breaks a big tie instead of questioning it · #5 takes the population a flag suggests |
| Calibration form | Pilot log: 1,200 households in two states, each with the agency's filed decision (meets or does not meet) under the household standard |
| Driving force | The pilot judged each household at its own node's four busiest hours that month, not on the panel's 19:00–23:00 flag. That is a property of a different entity, reached by joining the node register to the node traffic file. Every fixed window stalls at the same 1,121 of 1,200 filed decisions. Coastline's student-housing and shift-worker nodes congest outside the evening window, so their households pass on the flag and fail at their node's peak. |

## 1. Situation

The broadband agency publishes, for each provider, the share of panel households whose median download at peak reaches 80% of the plan
speed. Last year a pilot in two states filed a decision for each of 1,200 households, and the standard says the national figure is computed
the way those decisions were made. Coastline Cable has 1,140 households in the national panel. The pack holds the panel's test results and
unit profiles, the panel methods note, the pilot log, Coastline's node register and node traffic file from its transparency filing, and the
standard.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each test, each plan speed, each pilot decision and each node's hourly traffic. Nobody publishes a
  wrong share and nothing is overturned. The difficulty is which hours count as a household's peak.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete Coastline's submission and both voices. Household medians on the panel's peak flag still give 93.4%, and the
  back-test still ties every fixed window.
* **Instrument repair.** Make every test perfect and add tests every minute: the household's figure still depends on which hours are its
  peak, and that comes from the node it shares, not from any test.
* **Lens swap.** The naive figure scores each household's evening tests. The answer scores each household's tests in its node's busiest
  hours, a different set of tests that for a third of households barely overlaps the evening.

## 3. The driving force

A strong solver builds household medians from valid tests in the panel's peak window and back-tests against the pilot log. It reproduces 1,121
of 1,200 decisions. It then tries 18:00–22:00 and 20:00–24:00 and gets 1,121 again, a tie at the most a fixed window can reach. The panel
methods note breaks window ties toward the window ending latest, so the solver files 20:00–24:00. The tie is the signal. The 79 decisions no
fixed window returns all belong to households whose node is busiest outside the evening, around student housing after 22:00 and estates of
shift workers before 19:00. Taking each household's peak as its node's four busiest hours that month returns all 1,200. Coastline has many
such nodes, and its share falls to 84.6%.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Pooled share of valid peak-flag tests at or above 80% of plan | 95.6%, +13.0% | The panel's rows, read straight | The standard judges households, not tests |
| 1 | Household medians on the panel's peak flag (19:00–23:00 local) | 93.4%, +10.4% | The right unit on the panel's own window | The pilot log: 1,121 of 1,200 filed decisions |
| 2 | Fixed windows back-tested: 18–22, 19–23 and 20–24 all reproduce 1,121; the methods note's tie-break picks 20:00–24:00 | 92.4%, +9.2% | The window is tested and the tie is broken by the written rule | The node traffic file: every one of the 79 unreturned decisions sits on a node busiest outside 18:00–24:00 |
| 3 | **Decisive:** each household's peak is its node's four busiest consecutive hours that month (node register joined to node traffic) | **84.6%** | — | — |

* **Figure shape.** Every correction walks the share down and the answer is the minimum cell, so a solver who stops anywhere publishes
  too favourable a figure.
* **Partial correction priced (L3).** A solver who takes peak as Coastline's network-wide four busiest hours (20:00–24:00 Eastern,
  applied to every household) lands at 92.9% (+9.8%), further away than rung 2.
* **Grid.** Unit (tests or households) × window (19–23 local, 20–24 local, network-wide hours, node hours) = 8 cells: 95.6, 95.0, 95.3,
  92.0 and 93.4, 92.4, 92.9, 84.6. The nearest wrong cell is pooled tests on node hours, 92.0% (+8.7%), which needs the decisive
  construction with the standard's household unit ignored.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The standard says "at peak" and points to the pilot's method. The methods note defines the peak flag as 19:00–23:00
   local. The node register ships with the transparency filing to weight Coastline's subscriber counts, not to define a window.
2. **Pattern B, a gate passed by a construction.** Node windows reproduce 1,200 of 1,200 filed decisions. Every fixed window reproduces 1,121,
   and network-wide hours 1,133, all erring the same way (calling failing households passing). The construction is not a menu: it needs
   the register join, an argmax of four-hour utilisation per node, and per-household test selection.
3. **No arithmetic symptom.** Test counts tie to the collector's summaries, every household clears the validity floor under every window,
   and no ratio is out of range.
4. **Not a row predicate.** Whether a test is a peak test depends on a computed property of the household's node, and the four hours are
   recovered per node from its traffic.
5. **The enumeration is arithmetic.** No column names a node's busy hours or marks a test as node-peak.
6. **No cutover date.** Busy hours are stable through the month and nothing steps.
7. **Survives deletion.** With every voice removed, the back-test still ties at 1,121 and the tie-break still files 20:00–24:00.

## 6. The calibration corpus

* **Form.** The pilot log: 1,200 households across Coastline and two other providers in two states, each with plan speed, node, test
  history for the pilot month, and the agency's filed decision.
* **What it certifies.** The household unit and the 80% median test, which every household-level construction honours.
* **What pins the rule.** The 79 households whose node peaks outside 18:00–24:00, returned only by node windows.
* **Twin pair.** Pilot households 0417 and 0952 share plan, provider, state, test count, evening median (0.93) and off-peak throughput.
  Their node-window medians are 0.92 and 0.46 (2.0×), and the filings say meets and does not meet. 0952's node serves a student block
  busiest from 22:00 to 02:00.
* **Resemblance points at the decoy.** On every panel column, Coastline's national households resemble the pilot households that fixed
  windows already return.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The standard: a household receives its speed when its median download at peak is at least 80% of its plan speed; the
  annual figure is computed by the method the pilot's filed decisions were made on, and a method that misses any filed decision is not
  that method. The methods note: the panel's peak flag and its tie-break for windows that perform equally.
* **Empirical pins.** The node windows, from the pilot log.
* **Voices.** Coastline's regulatory lead: "Peak is seven to eleven at night everywhere; that's the industry convention." The panel
  manager: "We have scored households on the evening window since the panel began, and the pilot was the same panel."
* **Licensed wrong basis.** The standard records that Coastline will present its share on the evening window at the publication hearing.

## 8. Determinism by construction

* **Busy hours.** Every node's busiest four consecutive hours lead the next candidate by at least 3% utilisation, so there are no ties.
* **Assignment.** The register is stable for the month: no household was re-homed and every household maps to one node.
* **Clock.** The month has no daylight-saving change, and the unit profiles' time zones agree with the node file's.
* **Plans.** Every household's plan speed is the same in the unit profile and the transparency filing for the whole month.

## 9. Prompt sketch and deliverables

> The broadband report goes to the printer on 14 March, and Coastline's household figure is the one people will quote. Coastline says peak
> means the evening everywhere. Give me the share of its households that got at least 80% of their plan speed at peak, to one decimal, as
> the sentence we print, with `coastline_figure.xlsx`, a chart `peak_windows.png`, and a one-page `method_note.pdf`.

* `coastline_figure.xlsx` — the household build, the upload sheet (ask A), the usage sheet (ask B) and the pilot reproduction table
  (ask C).
* `peak_windows.png` — a heat map of hourly utilisation for Coastline's nodes sorted by busy-hour start, with the panel's evening window
  outlined, each node's own four hours marked, and the share under each construction in the margin.
* `method_note.pdf` — the committed share and why each fixed window fails the standard's gate.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 providers, the median household upload ratio at the panel's evening window.
  *Device:* the upload results file records throughput in bytes per second while the download file uses bits, as the dictionary states;
  a solver who mixes them understates upload ratios eightfold in every provider.
* **Ask B (device-carried).** For each provider, the median monthly data usage per household. *Device:* older whitebox firmware reports a
  32-bit byte counter that wraps, flagged in the usage file; summing raw deltas produces negative usage for 6% of units. Usage never
  enters the speed figure.
* **Ask C (validity).** Decisions reproduced and Coastline's share under each of the four rung constructions.
* **Decoupling.** Clearing the node windows changes no figure in asks A or B.

## 11. Rubric arithmetic

12 providers (ask A) + 12 providers (ask B) + 4 constructions × 2 (ask C) + the committed share, households counted and decisions
reproduced + 5 named chart parts + 3 files ≈ 43 criteria.

## 12. World-building constraints

* Coastline shares: 95.6 / 93.4 / 92.4 / 84.6; grid cells 95.0, 95.3, 92.0 and 92.9. 31% of Coastline's households sit on nodes busiest
  outside 18:00–24:00.
* Pilot: fixed windows 1,121 of 1,200, network-wide hours 1,133, node windows 1,200. Households 0417 and 0952 match on every panel column.
* Busy-hour leads of at least 3%, no re-homing, no daylight-saving change in the month.
* Upload units and counter wraps never touch a download test or a node.
