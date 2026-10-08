# AD49 — Which school's solar system gets the repair reserve this quarter, or does it carry forward, when repairs hold on one inverter model and relapse on the other

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Nonprofit & Grant-making · community energy programmes |
| Mirrors | Deciding whether a remediation budget should be spent at all when past fixes held for one equipment class and relapsed for another (server remediation in cloud fleets where one hardware model's fault returns after replacement, field-service programmes for network gear, battery repairs in device fleets) |
| Decision shape | Hold, forced by a blocking quantity: the quarter's single repair (an inverter or string repair of about $18,000) goes to one of five flagged systems, or the reserve carries forward |
| Committed call | The system repaired, or that the reserve carries forward, with the expected three-year energy recovery that decides it |
| Gap · Pattern | Gap 2 (population: which repairs hold) over Gap 1 (time: the three-year payback) · conditioned yield (repair recovery splits absolutely on inverter model, reached through the asset register), with two flawless grains (system meters and string currents) below it |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution support |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #1 reports a failed back-test, ships anyway |
| Calibration form | Parallel-run overlap: the twelve months in which string-level monitoring and a daily-cleaned reference pyranometer ran beside the revenue meters and the site pyranometer |
| Driving force | The reserve funds a repair only if it pays back over three years, and how much a repair gives back depends on the inverter, not the system. In the repair log, every repair on one inverter model held for three years, and on the other the fault came back within the first year every time; the pooled recovery is right for the log and true of neither model. The model sits in the asset register, not on the system list. C, whose two dark strings make the largest repairable deficit, has the relapsing model; on the model that holds, the best candidate recovers 48 MWh against a 60 MWh break-even, so the reserve carries forward. |

## 1. Situation

A community energy nonprofit runs 30 rooftop solar systems on schools and halls, monitored by its maintenance contractor. A foundation grant
holds a repair reserve that can fund one component repair this quarter. The grant terms fund a repair only where the energy it is expected
to recover over the three years after repair repays its cost at the community tariff (60 MWh), and otherwise carry the reserve forward. The
contractor flagged five systems. The nonprofit holds five-minute output per system, the revenue meters, string-current logs from the new
monitoring, the site pyranometer and the reference pyranometer from the overlap year, the asset register and the programme's repair log. The
contractor wants the reserve spent on its worst performance-ratio alarm.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the performance ratios as computed from the site pyranometer, the meters, the string currents, the
  register and each logged repair's outcome. The contractor is right that A alarms most. Nothing is overturned; the difficulty is which
  repair outcome applies to which candidate, and then that none of them pays back.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the contractor's alarms and both voices. A string-level deficit costed at the log's pooled recovery still funds
  C.
* **Instrument repair.** Suspect files: the site pyranometer, which read up to 9% low while soiled, and the repair log, where 16 of 41
  repairs are too recent for three-year follow-up. Use the cleaned reference throughout and complete the follow-up (the recent repairs split
  by model like the rest): rung 0 still funds A, whose shortfall is its technology's normal yield on either sensor, rung 1 B and rung 2 C at
  a pooled recovery that stays near 0.59. The recovery conditioned on inverter model is still needed, and on it the best candidate, D,
  recovers 48 MWh against 60.
* **Lens swap.** The naive recovery is the log's pooled share, true of no repair; the answer's is each candidate's model's share over the
  three years after repair, a different population of repairs at a different moment, and the verdict moves from a pick to a hold.

## 3. The driving force

A strong solver drops the performance-ratio alarms (the overlap shows the site pyranometer read low while soiled), compares each system's
daily yield with the site's median system, finds the sustained deficits, looks down to string currents to separate component faults (dark
strings, a tripped inverter) from uniform module ageing that no repair fixes, and costs each repairable deficit at the repair log's
recovery. C's two dark strings clear the break-even comfortably. Every step is correct, and the recovery share is the log's pool: 59% over
three years. The log does not record inverter models; the asset register does. Joined, the log splits absolutely: all 14 repairs on model X
with three years of follow-up kept 95–100% of the recovered energy, and all 11 on model Y lost it within the first year as the DC arcing
fault came back, keeping 12–20%. No repair recovered anything in between. C runs model Y. On model X the best candidate is D at 48 MWh.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Performance-ratio shortfall below the alarm line × 3 years × the log's pooled recovery (0.59): A 92 MWh | Fund A | The contractor's alarm and the industry's standard ratio | The overlap's reference pyranometer: the site pyranometer read up to 9% low while soiled, and A's shortfall is its technology's normal yield |
| 1 | Sustained deficit against the site's median system (each system against its own reference ratio) × 3 × 0.59: B 67 MWh | Fund B | Peer comparison cancels the shared sensor error | The string-current logs: B's deficit is spread evenly over all eight strings, module ageing that no component repair reverses |
| 2 | String-level component deficit (dark or low strings, tripped inverters) × 3 × 0.59: C 92 MWh | Fund C | The right grain, the right repair, a payback well clear of 60 MWh | The asset register joined to the repair log: every repair on C's inverter model lost its recovery within the first year |
| 3 | **Decisive:** component deficit × 3 × the recovery for the candidate's inverter model (X 0.97, Y 0.16): D 48, E 41, C 25, A and B 0 | **Hold: the reserve carries forward; the best candidate, D, recovers 48 MWh against 60** | — | — |

* **The blocking quantity.** The best expected three-year recovery among the five is D's 48 MWh, 12 MWh (20%) short of the 60 MWh
  break-even. E reaches 41, C 25, and A and B have no repairable component deficit, so every candidate fails on the same standard.
* **Partial correction priced (L3).** A solver who conditions on inverter model but carries the log's one-year recovery (X 0.98, Y 0.48)
  over three years credits C with 75 MWh, 15 MWh (1.25×) over the break-even and 1.56× D's 48, and funds it: a pick, not the hold.
* **Grid.** Monitoring basis (performance ratio, system peer, string level) × recovery (pooled or model-conditioned) = 6 cells. Five fund a
  system (A, A, B, B, C); only string-level deficits with model-conditioned recovery hold.
* **Falsifiable.** D would be funded with a component deficit of 20.6 MWh a year instead of 16.5, or a repair cost under about $14,400 at
  the same tariff.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The repair log lists systems, repair types and outcomes; no document mentions inverter models in connection with
   repairs or says that any fault recurs.
2. **Corpus blind for a computable reason.** *No repair took place on any system during the overlap year, because the reserve was frozen
   while the new monitoring was commissioned.* The overlap certifies the peer comparison and the string-level attribution (string currents
   sum to the meters within 0.5% every month) and cannot show what happens after a repair.
3. **No arithmetic symptom.** The pooled recovery is the log's exact mean, the string deficits reconcile to the meters, and every
   candidate's payback computes cleanly.
4. **Not a row predicate.** Recovery by model needs the repair log joined to the asset register, each repair's three-year outcome computed
   from output before and after, and the split carried to each candidate's inverter.
5. **The enumeration is arithmetic.** Which candidates' repairs would hold is computed; no column on the system list carries the model.
6. **No cutover date.** The decision rests on a split across 25 repairs over five years; no candidate's series steps.
7. **Survives deletion.** Remove the alarms and both voices: the pooled-recovery string build is still the natural one.

## 6. The calibration corpus

* **Form.** The overlap year: string currents, revenue meters, the site pyranometer and a reference pyranometer cleaned daily, observed side
  by side for twelve months.
* **What it certifies.** Peer-relative deficits are unaffected by the soiled site pyranometer, and string-level deficits sum to meter-level
  deficits; a back-tester is confirmed at rung 2.
* **What it is blind to.** Repair outcomes (above). The refusal sits in the less inviting record: the repair log, which joined to the asset
  register splits absolutely (model X 0.95–1.00, model Y 0.12–0.20 over three years, nothing between).
* **Twin pair.** Logged repairs R-2019-06 and R-2020-11 are identical on every log column: a 30 kW school system, two dark strings, a
  combiner and inverter repair in March, the same pre-repair deficit. One recovered 14.1 MWh in its first year and the other 6.8 MWh, 2.1×
  apart, separated only by the inverter model in the register.
* **Resemblance points at the decoy.** By system size, age and deficit, C most resembles the log's largest successful repairs.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The grant terms: a repair is funded only where its expected energy recovered over the three years after repair repays its
  cost at the community tariff, otherwise the reserve carries forward; the reserve funds component repairs, not module replacement. The
  community tariff and the repair quote. One sentence each.
* **Empirical pins.** Recovery by inverter model, from the repair log; the peer and string methods, from the overlap.
* **Voices.** The maintenance contractor: "A has alarmed every month; spend the reserve there." The programme manager: "Our repairs pay for
  themselves; the log proves it."
* **Licensed wrong basis.** The grant terms record that the foundation's programme officer reviews proposals on performance-ratio alarms and
  will look for one on the list.

## 8. Determinism by construction

* **Recovery shares.** Model X's 0.95–1.00 keeps D between 47.0 and 49.5 MWh, under 60 at either end; model Y's 0.12–0.20 keeps C between 19
  and 31.
* **Deficit window.** Component deficits are measured over the last 90 valid days; 60- and 120-day windows give the same order and keep D
  under 52 MWh.
* **Horizon.** The three years and the tariff are filed; every candidate's roof lease runs past the horizon under any reading of the lease
  register.
* **Rounding.** Recoveries are given to the nearest MWh; 48 sits clear of 60.

## 9. Prompt sketch and deliverables

> The repair reserve can pay for one fix this quarter, and the contractor has flagged five systems; it wants the money on A, which alarms
> every month. Tell me which system we repair, or that the reserve carries forward, in a line for the foundation, with the three-year energy
> figure that decides it. Send `reserve_case.xlsx`, a chart `repair_payback.png`, and a one-page `reserve_note.pdf`.

* `reserve_case.xlsx` — each candidate's expected recovery under each rung's basis (ask C), the lease sheet (ask A) and the curriculum sheet
  (ask B).
* `repair_payback.png` — expected three-year recovery per candidate as bars under pooled and model-conditioned recovery side by side, the 60
  MWh break-even drawn and labelled, the inverter model marked on each bar, and the verdict in the title.
* `reserve_note.pdf` — the committed verdict, the blocking quantity and what would have funded a repair.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 30 host sites, the roof lease's remaining term on 1 January. *Device:* a lease
  extension is an amendment record that supersedes the original term, as the lease register guide says; reading the original expiry
  misstates six sites. No candidate's horizon depends on it, because every candidate's lease runs past the horizon either way.
* **Ask B (device-carried).** For each of the five districts the programme serves, students reached by the solar curriculum and the share of
  schools with a completed module. *Device:* a student who changed school appears on both rosters under one student number, and the register
  guide counts each student at their school of record on census day; counting roster rows overstates three districts.
* **Ask C (validity).** Each candidate's expected recovery under each of the four rung bases.
* **Decoupling.** Clearing the model conditioning and the string grain changes no figure in asks A or B.

## 11. Rubric arithmetic

30 sites × 1 (ask A) + 5 districts × 2 (ask B) + 5 candidates × 4 bases (ask C) + the committed verdict, the blocking quantity, the
shortfall and the falsifiability figure + 5 named chart parts + 3 files ≈ 72 criteria.

## 12. World-building constraints

* Rung figures: A 92, B 67, C 92 under pooled recovery; model-conditioned D 48, E 41, C 25; the one-year partial C 75. Component deficits:
  C 52, D 16.5, E 14 MWh a year. C runs model Y and the other four model X, so the alarm and peer builds still fund A and B under
  model-conditioned recovery.
* The repair log: 41 repairs, 25 with three-year follow-up (14 model X at 0.95–1.00, 11 model Y at 0.12–0.20); pooled three-year recovery
  0.59, one-year 0.98 and 0.48.
* No repair in the overlap year; the soiled site pyranometer read up to 9% low.
* R-2019-06 and R-2020-11 are identical on every log column.
* Lease amendments and curriculum rosters never touch output, meters, string logs, the register or the repair log.
* The 16 repairs without three-year follow-up split by inverter model like the 25 with it.
