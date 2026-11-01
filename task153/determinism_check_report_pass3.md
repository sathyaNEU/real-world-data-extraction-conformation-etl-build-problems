# determinism check, task153, pass 3 (11-01 re-check, repaired cut c2239b2d)

One isolated thread (sonnet, medium) on a fresh unzip of target.zip and the submission's graded blocks; the determinism-judge agent prepared the brief and the build session spawned the thread (the agent's runtime had no Agent tool).

**Main-thread ruling on the FIX_NOW:** the chart's graded answer (Deliverable Answers, yard_island_draw.png, item 6) grades the ticks and the load labels and states no bar gallons; the draws appear only in step 4, labelled with the 39 to 40 working-day scaling and the 10.2% reserve of step 3. The finding is closed in the shipped record as it stands; no sentence or figure changed, so no re-judge.

# Determinism verdict, task153 (Overton island loads, 14 Sep to 8 Nov 2026)

**Verdict:** DETERMINISTIC. I rebuilt the main call from the shipped files, without reading the author's scratch scripts in `w/`, and it holds. Load counts, the total, the dollar saving and the card and programme tables all reproduce. One residual fork touches only the numeric bar heights of the chart (ask 6), not the committed loads.

**Disposition:** FIX_NOW, with no model rerun and no change to any solver-facing file. Make the rubric grade the chart on load counts, ticks and bar ordering, with a tolerance on bar gallons (about 2.5 percent for the 40/39 scaling and up to about 10 percent for capped yards depending on the reserve). Otherwise APPROVE.

**Why:** The deciding quantity is each island's hand-out to our own vehicles. It is read from the geofence yard visits and the units' fuel burn, limited by each model's tank in `fleet_units_2026-08.xlsx`, and projected from 39 observed working days to the 40 in the window. My independent time-level replay gives Memphis 21,303, Jackson 44,697, Nashville 69,403, Cookeville 12,900, Knoxville 37,576 and Blountville 27,845 gallons, within 10 gallons of the golden. Floor to 8,000-gallon loads gives 2, 5, 8, 1, 4 and 3, so 23 in all, and the rates give USD 17,408.

The loads do not move under any reasonable variant. I varied the reserve (0, 5, 10.2, 15 and 20 percent), the 40/39 scaling, and counting or not counting each yard's pumpable heel. The smallest margin to a load boundary is about 2,400 gallons, at Knoxville and Nashville. Only the uncapped reading, where a vehicle takes more than its tank holds, changes the answer. That is a physical impossibility, not a fork.

## Evidence (recomputed from `target/`)

| Item | Golden | My recompute | Source |
|---|---|---|---|
| Yard draws (gal) | 21,303 / 44,695 / 69,402 / 12,898 / 37,575 / 27,835 | 21,303 / 44,697 / 69,403 / 12,900 / 37,576 / 27,845 | geofence events, `vehicle_days`, serial mapping from `telematics_device_assignments.csv`, UTC to local time, a day's fuel split by driving time around a midday visit, tank less reserve |
| Loads by yard | 2 / 5 / 8 / 1 / 4 / 3, total 23 | same | draw floored to 8,000 |
| Saving per load | USD 800 / 640 / 864 | same | Riverbend 0.119 less 0.019; Crossroads 0.084 + 0.015 less 0.019; SMPM 0.127 less 0.019, all times 8,000 gallons |
| Total saving | USD 17,408 | 7×800 + 9×640 + 7×864 = 17,408 | `card_programmes_pricing_schedules.pdf`, `overton_offer_2026-08-26.pdf` |
| Delta (Riverbend) May / Jun / Jul gal | 33,472 / 36,732 / 37,170 | 33,472.4 / 36,731.6 / 37,170.1 | UTC converted to Central; ULSD only; 12 reversal rows and the duplicates they reverse removed, dated by purchase |
| Keeble (Crossroads) May / Jun / Jul gal | 46,569 / 54,781 / 52,821 | 46,568.75 / 54,780.54 / 52,821.0 | a purchase at 22:00 or later is moved back one day to its true date; 9 reversals and their duplicates removed |
| Holston (SMPM) May / Jun / Jul gal | 46,391 / 51,215 / 53,258 | 46,391.1 / 51,214.8 / 53,258.0 | batch header 0088202 is a verbatim resend of 0088201 (identical trailer), removed; 7 credited details removed; 22:00 rule applied |
| Overton 2025 net gallons, Jackson Mar / Apr / May | 31,911 / 24,004 / 7,986 | same | one BOL gallon figure per BOL; split drops counted once |
| Overton 2025 net gallons, Knoxville Jun / Jul / Aug | 23,977 / 24,021 / 8,021 | same | delivery month; K004606 was lifted on 30 June but delivered on 1 and 2 July |
| USD billed over posted rack, Jackson | 891 / 811 / 254 | 891 / 811 / 254 | rack posting effective the lift date, or the next day for lifts at or after 18:00, per the programme letters |
| USD billed over posted rack, Knoxville | 446 / 542 / 191 | 446 / 542 / 191 | credit memos CM09072 and CM09074 net against invoices 260487 and 260494 and their rebills 260505 and 260509 (`overton_invoices_2025.csv`, `overton_credit_memos_2025.csv`); taxes excluded |

- Invoice unit prices equal the correct posted rack plus the programme adder exactly (for example 2.4246 = 2.4006 + 0.024), which confirms the rack timing rule from the files.
- Cross-check against 2025 (`fms_island_transactions_2025.csv`, `vehicle_days`):
  - Jackson islands took 97 percent of that yard's burn. The 2026 capped replay predicts 96.6 percent.
  - Knoxville took 99.7 percent in 2025, while the 2026 replay gives 89 percent. Route patterns changed, which is why the prompt says "as in the eight weeks to 23 August".
- Cross-yard visits: none. Every `KSC` yard event belongs to a unit of that yard, and the fobs-work-everywhere remark in the yard notes has no data effect.
- Naive route: take the yard's card gallons (or uncapped burn) as the island draw. This gives Cookeville 3, Knoxville 5 and Blountville 6 loads, against the golden 1, 4 and 3.

## Competing answers and forks

1. **Reserve (Gate C, chart bars only).**
   - The golden takes 10.2 percent off every tank, derived from the T680 fills over 225 gallons in 2025 (average 269.3 of 300).
   - The other models' 2025 fills reach 85 to 98 percent of tank.
   - A solver using full tanks gets Blountville 30,607 and Cookeville 13,556, against 27,845 and 12,900. Loads are unchanged.
2. **40/39 scaling (chart bars only).**
   - 3 July 2026 has no activity for any unit, but the yard notes list only Labor Day and Thanksgiving as company holidays.
   - Unscaled draws are 20,771 / 43,580 / 67,668 / 12,577 / 36,637 / 27,149. Loads are unchanged.
3. **Terminal spread (saving, low risk).**
   - The card programmes bill some gallons off a different terminal's TriState average: Riverbend Paducah at Nashville, Crossroads Georgia sites at Knoxville, SMPM Kentucky sites at Nashville.
   - Mixing the window's purchases through historical spreads moves the saving by about +USD 28 (0.16 percent), to about USD 17,436 against 17,408.
   - The offer says Overton's average is "the same average your three card programmes bill from", and the prompt says "at their agreement terms", so the premium-difference reading is the literal one. Future spreads are unknowable.
4. **Month of purchase (asks 4 and 5).**
   - Using UTC dates or the Crossroads business-day dates gives different monthly figures. Delta May would be 33,644 on UTC dates, and Keeble May 46,942 on stated dates.
   - The pricing PDF defines each clock, and "bought in" means the purchase moment, so the local-time reading is forced.
   - K004606 sits in July by delivery date and in June by lift date. "Delivered" forces July.
5. **Cookeville vans "stocked by shuttle".** Nothing in the files supports fuel being shuttled. They are in the Cookeville yard once a week and the golden uses those visits only.

## Gate results

- **Gate A:** pass. Every load-bearing figure reproduced.
- **Gate B:** pass. The tank sizes, geofence visits, burn, FMS fills, rack and TriState series, programme letters, invoices and credit memos are all shipped. The reserve is inferable from `fms_island_transactions_2025.csv`.
- **Gate C:** pass for the main call, loads, total and saving. Advisory on the chart's bar gallons (forks 1 and 2 above).
- **Gate D:** pass. Divergence among solvers would come from analysis (capture structure, midday visits, device swaps, timezone), not word meaning.
- **Gate E:** pass. One committed call is demanded, with unit and rounding stated.

## Files/Hygiene

**PASS.**
- 20 shipped files in 6 formats: csv ×8, xlsx ×4, pdf ×5, txt, md, and one fixed-width card file. `vehicle_days` has 79,042 rows and `geofence_events` has 42,446.
- Distractors: IFTA returns, tank-wagon prices, `yard_tank_register.xlsx`, credit memos.
- Dates cohere: yard notes 28 Aug, offer 26 Aug (the Monday call is 24 Aug), dips 24 Aug, data through 27 Aug.
- Realistic mess: mixed unit-number formats, a resent SMPM batch, device swaps with serial-only vehicle names, UTC against Central against Eastern, business-day clocks, split drops, credit and rebill pairs.
- No authoring or provenance disclosure was found in the shipped files.
- The bundle directory also holds a `w/` folder of scratch scripts outside `target/`. It is not shipped and I did not read it.
- No exclusion-level finding.

## Stump power (Gate F)

High. The work that does the stumping:
- Pairing yard Enter and Exit events through device-serial changes, and splitting a day's fuel around a midday visit.
- Seeing that Nashville's sleepers visit twice a week while Cookeville's lot vans and Blountville's sleepers visit once, so a tank cap binds.
- Reading the cap off the 2025 island fills.
- Resisting the shortcut of using card gallons or uncapped burn as the island draw, which gives a different load count at 3 of 6 yards.

## Stumping type (Gate G)

mechanism: forecasting (a capture and throughput projection that the trailing card gallons do not pin) | stumping_family: analytical_non_defect | surface_read_dependency: no | sole_data_defect: no

No reported number is misleading, and run on clean data the task still stumps on the capture structure.

## Three rules (Gate H)

domain: pass | layers: pass | decisive_step: analytical

- **Domain:** estimating yard-island throughput for a fuel-procurement commitment from telematics, tank limits and tariff terms is the field's own analysis.
- **Layer 1:** UTC against local time, a resent batch, duplicate and reversal pairs, device swaps and mixed unit keys.
- **Layer 2:** the tank-limited replay of vehicle visits, with the saving taken as the premium difference.
- **Easy route:** treat the yard's card or burn gallons as island draw. It gives Cookeville 3, Knoxville 5 and Blountville 6 loads, and a different saving.

## Fix

Location: solution and rubric, with no change to the prompt or input files.
- Grade the chart on load counts, white ticks and ordering, with a tolerance on bar gallons.
- Optionally keep the draw list in the critical components labelled as scaled to 40 working days with a 10.2 percent reserve.
