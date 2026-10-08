# AD33 — How many megawatts of frequency reserve the data-centre battery offers for January, when its activations all happen at a handful of hour boundaries

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · electricity balancing markets |
| Mirrors | Sizing a commitment against a usage cap when usage concentrates on scheduled boundary events that averages hide (battery fleets at Google and Microsoft data centres selling grid services, cloud reserved-capacity commitments where batch jobs fire on the hour, top-of-hour traffic spikes on content platforms) |
| Decision shape | One figure committed at a date: the FCR-D upward capacity offered for January's night hours, in whole MW |
| Committed call | The January FCR-D offer in MW, submitted to the system operator's monthly auction on 10 December |
| Gap · Pattern | Gap 2 (population: the battery's window is not the system's average hour) over Gap 4 (rule recovered by reproduction) · conditioned yield (activation splits absolutely on the scheduled flow ramp at each hour boundary), with a binding throughput limit applied in the figure below it |
| Gate G mechanism | binding_constraint, with method_or_model_selection support |
| Measured traps engaged | #10 notes a binding limit as a risk · #13 validates on one population, applies to another · #1 reports a failed back-test, ships anyway |
| Calibration form | Published control set with a reproduction clause: the system operator's 24 published monthly FCR-D activation figures (MWh per MW procured), which the risk policy requires any throughput forecast to reproduce within 1% |
| Driving force | FCR-D throughput is not spread over the hours. It comes from hour boundaries where scheduled interconnector flows change by 600 MW or more, which pull frequency below the activation level for about a minute every time, while smaller boundaries never do. In the summer pilot those reversals fell in daytime; in January they fall at 22:00, 23:00, 05:00 and 06:00, inside the battery's night window. Joining each boundary to the published flow schedule is the only construction that reproduces all 24 published months, and it puts the January night window at 14.8 MWh per MW against the 4.0 the pilot showed. |

## 1. Situation

A data-centre operator's 40 MW battery is prequalified for upward frequency containment reserve for disturbances (FCR-D). The data-centre
agreement frees it only from 22:00 to 06:00, so it offers night hours in the system operator's monthly auction; January's offer is due on
10 December. The warranty caps annual energy throughput, and the warranty register shows 120 MWh left for January after the battery's
other services. The risk policy requires every offer to hold within that figure and allows a throughput forecast only if its method
reproduces each of the last 24 published monthly activation figures within 1%. The operator holds its May–October pilot log (every hour
boundary and every activation, metered), the system frequency at 10 Hz, the published monthly figures and the published interconnector
schedules, including January's indicative schedule.

## 2. Gate G: why this is legal

* **Litmus.** Every number is correct: the pilot's metered activations, the published monthly figures, the warranty register and the
  schedules. The trading lead is right that the battery barely cycled in the pilot. Nothing is overturned; the difficulty is which activation
  intensity applies to January's night window.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices. The pilot rate under the cap still offers 30 MW, and the published January figure pro-rated to the
  night window still offers 20 MW.
* **Instrument repair.** Meter every activation perfectly and publish every month: they are. The pilot's rate is right for its own window,
  and no better meter of summer daytime ramps measures January nights.
* **Lens swap.** The naive intensity is the pilot's (summer, ramps in daytime) or the system's (all hours); the answer's is January's night
  window, whose boundaries carry most of the month's large reversals. A different population of hour boundaries at a different moment.

## 3. The driving force

A strong solver sees that the warranty cap binds, refuses to offer the full 40 MW, prefers the published series to its own summer pilot,
pro-rates January's published intensity to the night window, and offers 20 MW. Every step is correct, and each treats activation as
spread evenly over hours. The pilot log, joined to the published flow schedule at each hour boundary, shows an absolute split: all 186
boundaries where scheduled interconnector flow changed by 600 MW or more pulled frequency under the activation level for 40 to 110
seconds, and none of 4,130 smaller boundaries did; the remaining activations are 23 real disturbances. A per-hour rate, a per-month rate
and an hour-of-day profile are all correct for the pilot and apply to no other window. In winter the large reversals move to the night
hours when hydro exports switch direction, and January's indicative schedule puts 61% of the month's large boundaries in the battery's
33% of hours. Summing energy per large boundary plus the disturbance allowance reproduces all 24 published months.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Offer the full prequalified 40 MW, noting warranty throughput as a risk | 40 MW, +400% | Capacity revenue is linear in MW and the pilot shows light cycling | The risk policy and the warranty register: the offer must hold within 120 MWh for January |
| 1 | Cap applied with the pilot's pooled intensity (4.0 MWh per MW-month in the night window) | 30 MW, +275% | The battery's own metered record, cap respected | The published monthly series: winter months run 1.9× summer, and the pooled pilot rate reproduces 9 of 24 |
| 2 | Cap applied with the published January figure pro-rated to the night window (6.0 MWh per MW) | 20 MW, +150% | The official series, seasonally matched, cap respected | The schedules: January's night window holds 61% of the month's large flow reversals in a third of its hours |
| 3 | **Decisive:** activation energy per large-ramp boundary (from the pilot's absolute split) × January's large night boundaries, plus the disturbance allowance, then the cap: 14.8 MWh per MW | **8 MW** | — | — |

* **Figure shape.** The answer is the minimum cell of the grid. Every rung and every partial route over-offers, so a solver stopping short
  breaches the warranty in a known direction.
* **Partial correction priced (L3).** A solver who sees that the window matters but conditions on hour of day from the pilot log finds
  summer nights quiet (2.4 MWh per MW), lifts the cap's limit to 50 MW and offers the full 40, five times the answer and further from it than rung 2, because
  in summer the large reversals sat in daytime.
* **Grid.** Cap (noted or applied) × intensity source (pilot pooled, published pro-rated, pilot hour-of-day, boundary-conditioned) = 8 cells:
  40 / 40 / 40 / 40 with the cap noted and 30 / 20 / 40 / 8 with it applied. The nearest wrong cell is 20 MW, 150% above the answer.
* **Separation.** The decisive move takes the figure from 20 to 8 MW, 60% of the pre-decisive offer, so no rounding or window choice
  bridges it.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The schedules are filed as market information; no document links flow reversals to frequency or to activation,
   and the pilot log has no column naming a boundary type.
2. **The corpus pins a construction, not a menu (Pattern B).** The boundary-conditioned model reproduces 24 of 24 published months within 1%.
   The pooled per-hour rate reproduces 9 and an hour-of-day profile 13, both under-predicting every winter month, so they miss the 24-month
   total by 18% and 11%. The reproducing rule needs a join of 17,520 boundaries to the schedule file and a split recovered from the pilot,
   not a parameter on a list.
3. **No arithmetic symptom.** Metered activations tie to the battery's energy counters, the published figures tie to the system operator's
   settlement totals, and the pro-rated published figure is arithmetically exact.
4. **Not a row predicate.** Each boundary's net ramp is computed by differencing the schedule's flows across the boundary and summing across
   interconnectors, then joined to frequency; the intensity is a sum over boundaries in a window.
5. **The enumeration is arithmetic.** Which boundaries activate is computed from flows; no field names them.
6. **No cutover date.** Large reversals recur every day in both seasons; only where in the day they fall changes, smoothly with hydro
   conditions.
7. **Survives deletion.** Remove both voices and the pro-rated published figure remains the natural careful build.

## 6. The calibration corpus

* **Form.** The 24 most recent published monthly FCR-D activation figures, with the risk policy's clause that a forecast method must
  reproduce each within 1%.
* **What it pins.** The boundary-conditioned model (0.021 MWh per MW at each large boundary, plus disturbances) reproduces all 24. The rivals
  fail case by case and on the total (above).
* **The absolute split (O2).** In the pilot, every boundary with a scheduled net change of at least 640 MW activated and none at or below 410
  MW did; no boundary fell between, so any threshold in the gap selects the same 186.
* **Twin pair.** October 2024 and October 2025 publish the same procured volume, the same four listed disturbances and the same mean
  frequency deviation, yet their activation figures are 8.2 and 16.5 MWh per MW, 2.0× apart, because a dry autumn doubled the large
  boundaries (90 against 190). Only the boundary join separates them.
* **Resemblance points at the decoy.** January 2027 matches January 2026 on every published column, so a lookup carries last January's
  all-hours figure, which is rung 2.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The risk policy: an offer must hold within the warranty register's throughput for the month, and a throughput forecast
  must reproduce the last 24 published monthly figures within 1%. The data-centre agreement's 22:00–06:00 window. The warranty register's
  120 MWh. One sentence each.
* **Empirical pins.** The ramp split and the energy per boundary, from the pilot; the construction, from the published months.
* **Voices.** The trading lead: "Our own pilot proves the battery hardly cycles on FCR-D; offer the full forty." The asset manager: "Use the
  operator's own January number; it is the official series."
* **Licensed wrong basis.** The risk policy records that the battery's lender models FCR-D throughput at the published annual average
  intensity and will review the offer on that basis.

## 8. Determinism by construction

* **Threshold.** The empty gap from 410 to 640 MW makes the split threshold-free.
* **January's boundaries.** The indicative schedule, published on 1 December, fixes the hours of every large reversal in January; the
  daily pattern repeats on all 31 nights, so no day-type convention matters.
* **Disturbances.** The allowance is the published disturbance rate (four a month at 0.11 MWh per MW each), identical on every rung, so it
  separates nothing.
* **Rounding.** Offers are in whole MW and must hold within the cap: 8 MW uses 118 MWh and 9 MW would use 133, so floor and round agree.

## 9. Prompt sketch and deliverables

> The January reserve offer goes in on 10 December and the warranty leaves the battery very little room this winter. Our trading lead reads
> the pilot as proof the battery barely cycles. Tell me how many megawatts we offer, as a whole number I can put in the bid, and send
> `offer_build.xlsx`, a chart `boundary_activation.png`, and a one-page `offer_note.pdf`.

* `offer_build.xlsx` — the offer under each rung's construction with its 24-month reproduction count (ask C), the availability sheet
  (ask A) and the capacity-test sheet (ask B).
* `boundary_activation.png` — activation energy per hour boundary against scheduled net flow change for the pilot, the 410–640 MW gap
  shaded, and a second panel of January's night boundaries by hour with the large ones marked and the offer in the title.
* `offer_note.pdf` — the committed offer and why each larger offer breaches the warranty.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each month of 2026, the battery's availability for its other reserve product and its outage
  hours. *Device:* the availability log records outages in local time, and on the autumn clock change the repeated hour is marked with a
  suffix, as the log guide says; ignoring it double-counts or drops an hour of outage in October and misstates two months. The January offer
  never uses the availability log.
* **Ask B (device-carried).** For each of the last eight quarters, the battery's tested usable capacity and its temperature-corrected value.
  *Device:* the warranty's test protocol corrects each test to 25°C with a published factor table; raw values make the winter tests look like
  a 6% fade that the corrected series does not show.
* **Ask C (validity).** The January offer under each of the four rung constructions and each construction's count of reproduced months.
* **Decoupling.** Clearing the boundary conditioning and the cap changes no figure in asks A or B.

## 11. Rubric arithmetic

12 months × 2 (ask A) + 8 quarters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed offer, January's window throughput, the
window intensity and the count of large night boundaries + 5 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Pilot: 186 large boundaries (all activating), 4,130 small (none), 23 disturbances. Rung figures 40 / 30 / 20 / 8 MW; partial 40 MW.
* January's indicative schedule puts 61% of the month's large boundaries in the 22:00–06:00 window; summer's put them in daytime.
* Night-window intensities: pilot pooled 4.0, published pro-rated 6.0, pilot hour-of-day 2.4, boundary-conditioned 14.8 MWh per MW.
* The twin Octobers are identical on every published column.
* Availability logs and capacity tests never touch the pilot log, the frequency data or the schedules.
