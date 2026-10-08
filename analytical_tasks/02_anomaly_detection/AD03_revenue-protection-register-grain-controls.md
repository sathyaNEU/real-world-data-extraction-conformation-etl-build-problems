# AD03 — Which district gets the one revenue-protection crew, when two scoring methods match every acknowledged total and only one matches the register lines

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Economics · energy retail and revenue protection |
| Mirrors | Sending one investigation team where anomaly scores built on totals miss abuse that lives in one component (fee-line abuse at marketplaces, per-SKU billing anomalies at cloud providers, device-telemetry faults confined to one sensor channel at Apple and Google) |
| Decision shape | Which of N gets one scarce thing: the specialist crew's January–March quarter, worked in one of eight districts |
| Committed call | The one district the crew works next quarter |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · Pattern B with finer controls separating constructions (E16), and a saturated tie at the lower rung (E21) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #12 stops at the first control that passes · #19 breaks a big tie instead of questioning it · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the meter operator's acknowledgements of 210 revenue-protection visits over three winters, with per-register assessed unrecorded energy for every confirmed case |
| Driving force | A bypass on a two-rate meter's storage-heating circuit takes energy from the night register only, so the household's total consumption falls by a few per cent, inside ordinary variation. Totals are additive across registers, so a total-consumption score matches every acknowledged total exactly; only the register lines, rebuilt by splitting each meter's half-hours at its own switching regime, separate confirmed cases from no-fault ones, and they move the crew to the district built on storage heating. |

## 1. Situation

An electricity retailer's revenue-protection team has one specialist crew with bypass-detection kit for January to March, and to keep
travel down the crew works a single district. Eight districts are candidates. The policy judges a quarter by the cases its crew confirms.
The pack carries 36 months of half-hourly consumption for every credit meter, the meter registration file, daily register reads, the
meter event log, district degree-days, the meter operator's acknowledgement file and the retailer's disputes register. Every past
referral came from the team's standard score, a robust z after a population seasonal index.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: consumption, register reads, degree-days, the operator's assessments and the appeal outcomes in the
  disputes register. Nobody's figure is overturned; the team's score measures exactly what it says. The difficulty is which construction of
  a household's shortfall reproduces the operator's register lines.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the procedure note's tie-break. A total-consumption, weather-adjusted score still reproduces
  every acknowledged total and still names C.
* **Instrument repair.** Suspect files: the half-hourly file, which records a comms-loss gap as zeros, and the acknowledgement file, nine of
  whose confirmations the disputes register overturned. Repaired, every half-hour read and every outcome as it stands after appeal, rung 0
  still names A (its population index, not the gaps, is the error), rung 1 loses B's tie and names D (9 of 9 against H's 2 of 3), and rung 2
  still names C, which already refilled the gaps. Half-hours labelled by register at the meter add nothing the daily register reads do not
  hold, and with one population index per register they name A (48 against E's 39). Every visit made is in the file and a household no crew
  visited has no outcome to fill, so the per-household degree-day baseline per register is still needed for E.
* **Lens swap.** The naive read scores households on whole-house consumption. The answer scores registers: for a two-rate meter, a
  different population of measured quantities, each with its own baseline, not the same total under another lens.

## 3. The driving force

A strong solver sees that the team's score sends crews to no-fault visits, checks where referrals have confirmed, sets aside confirmations
the disputes register overturned, then rebuilds the forward score with a weather-adjusted baseline and fills comms gaps from register reads.
It back-tests against the acknowledgement file and every case total ties to the kilowatt-hour, so it stops. The totals tie because a
shortfall is additive across registers: any construction that gets the whole-house expectation right gets every case total right. District E
is built on storage heating behind two-rate meters, and a bypass there diverts part of the night register. Whole-house consumption drops
6–9%, which is where legitimate no-fault households also sit, while the night register drops 35–60%. Seeing it needs each meter joined to
its time-pattern regime, every half-hour assigned to a register, a weather-adjusted baseline per register per household, and a test on the
larger register shortfall. The operator's per-register lines are reproduced by that construction alone.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The team's standard score: robust z on whole-house weekly kWh after a population seasonal index; households at z ≥ 4 counted per district | A (46 households) | The textbook per-household baseline, robust to spikes and shared seasonality, and the team's own method | The acknowledgement file: this score sent 117 referrals over three winters and 64% came back no fault found |
| 1 | Where referrals confirm: each district's confirmed share of acknowledged visits, three winters | B, by the procedure note's tie-break (four districts at 100%; B has the most customers, 1.32× D) | An outcome measure from the counterparty's own record, with the documented tie-break applied | The retailer's disputes register: four of B's seven confirmations were overturned on appeal, and under the note's rule (the lowest rate consistent with every file of record) B's 7 of 7 is 3 of 7, so the tie breaks |
| 2 | Hygiene and weather: comms-loss zeros refilled from register reads, whole-house baseline fitted on district degree-days per household; candidates whose shortfall clears the best whole-house band (12%) counted per district | C (34 expected confirmations) | Clean, weather-adjusted, forward-looking, and it reproduces all 210 acknowledged case totals and all three winters' totals to the kilowatt-hour | The operator's per-register lines: this construction misclassifies all 9 two-rate night-register confirmations, which sit at 6–9% whole-house shortfall among no-fault households |
| 3 | **Decisive:** each meter's half-hours split at its own switching regime, a degree-day baseline per register per household, candidates whose larger register shortfall clears the band counted per district | **E (56)** (5th of 8 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0 (24), 7th on rung 1 (38%) and 3rd on rung 2 (16), and leads only rung 3. Intermediate leaders hold
  margins of 1.24×, 1.32× (the tie-break's customer ratio) and 1.26×.
* **Discriminator dominance.** C carries a 2.13× advantage over E into rung 3 (34 against 16). Register grain multiplies E's expected
  confirmations by 3.50 and C's, all single-register meters, by 1.00: an edge of 3.50 against the 1.2 × 2.13 = 2.55 required, 1.37× headroom.
  E leads C by 1.65×.
* **Partial correction priced (L3).** A solver who sets aside the overturned confirmations but keeps ranking on past rates names D (9 of 9
  against H's 2 of 3, 1.50×), a district with only 27 forward candidates and no two-rate stock. A solver who splits registers but fits one
  population index per register instead of a degree-day baseline per household names A (48 against E's 39, 1.23×), because A's retrofit
  heat pumps cut night use in a mild month. Neither half lands on E.
* **Grid.** Score basis (population index or degree-day) × grain (whole house or register) × comms gaps (zero or refilled) gives eight
  cells. Population-index cells name A; degree-day whole-house cells name C (refilled) or B (zeros left in); register grain with zeros
  left in names B, whose comms-loss zeros fill its night registers. Only register grain with refilled gaps on degree-day baselines names
  E, and the nearest wrong cell, C, needs only the register split dropped, which the 9 night-register lines refute.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The operator's assessment method is not in the pack. The registration file's dictionary defines the time-pattern
   regime as switching times; nothing links registers to revenue protection.
2. **The corpus pins a construction, not a menu.** Register grain reproduces 210 of 210 classifications and every per-register line within
   1%; the best rival, the whole-house degree-day score, reproduces 201 of 210 and every total, and every rival's misses are confirmed cases
   it calls clean. The reproducing rule is a construction: the register a half-hour belongs to exists in no column until each meter is joined
   to its regime and its half-hours are assigned.
3. **No arithmetic symptom.** Register reads tie to half-hourly sums, case totals tie to the operator's totals, and the winter totals tie
   under both rung 2 and rung 3. Additivity makes the salient control blind to the split.
4. **Not a row predicate.** It needs a join to each meter's regime, a split of every half-hour, a degree-day fit per register within each
   household, and a test on the larger of two register shortfalls.
5. **The enumeration is arithmetic.** Confirmed cases show a larger-register shortfall of at least 30% and no-fault cases at most 8% on
   every register, so every band from 9% to 29% classifies the corpus identically.
6. **No cutover date.** Bypasses begin at scattered dates across three winters; no district series steps. The only dated programme in the
   pack, A's heat-pump retrofit, sits under the decoy.
7. **Survives deletion.** With every voice and the procedure note removed, the answer and the difficulty are unchanged.

## 6. The calibration corpus

* **Form.** The meter operator's acknowledgement file: 210 visits over the winters of 2023/24 to 2025/26, each with an outcome code and,
  for each confirmed case, assessed unrecorded energy per register per week. With the disputes register applied, 61 confirmations stand and
  149 visits are no fault.
* **What it pins.** The salient control (case and winter totals) is met by any construction with the right whole-house expectation,
  rungs 2 and 3 alike. The finer controls, the 61 cases' register lines, are met only by register grain: 210 of 210 against 201 of 210 for
  the whole-house score and 131 of 210 for the team's standard score, which also misses the 2024/25 winter total by 11%.
* **Twin pair.** Cases 2024-117 and 2025-033 sit in the same district on two-rate meters with the same regime, the same 6,850 kWh baseline
  year, the same population-index z and the same 8.1% weather-adjusted whole-house shortfall. 2024-117 was confirmed with 1,620 kWh
  assessed on the night register; 2025-033 was no fault found. No whole-house field separates them.
* **Every rule exercised.** Nine confirmations overturned in the disputes register stand as no fault, so the corpus scores standing
  outcomes. Nine confirmed cases are night-register only. Four no-fault cases are two-rate meters whose shortfall is spread
  evenly across both registers, so a register split alone, without the per-register baseline, misclassifies them. Six cases span a
  comms-loss gap that register reads refill.
* **Resemblance points at the decoy.** On every whole-house column E's forward candidates most resemble the 2024/25 no-fault referrals; C's
  resemble the confirmed cases of the 2025/26 winter.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The revenue-protection policy: a crew's quarter is judged by the cases it confirms. The procedure note: a district's
  confirmation rate is the lowest rate consistent with every file of record, and ties go to the district with more customers. The crew
  works credit meters only. The disputes register is the record of appeals against tamper findings.
* **Empirical pins.** The register band and the per-register degree-day baseline, from the acknowledgement file.
* **Voices.** The revenue-protection manager: "Our score has found every bypass we've ever confirmed; send the crew where the scores
  are." The contractor's field supervisor: "Where referrals confirm, sweeps confirm."
* **Licensed wrong basis.** The procedure note records that the field contractor's account manager places crews on past confirmation rates
  and will present them at the planning meeting.

## 8. Determinism by construction

* **Register split.** Every two-rate meter's regime is in the registration file, no meter changed regime in the window, and every switching
  time falls on a half-hour boundary, so no half-hour straddles two registers.
* **Gap refill.** Register reads are taken at midnight, so spreading an advance evenly or by the household's profile gives the same weekly
  totals, which are all the baseline uses.
* **Weather.** Each district maps to one station; degree-day bases of 14, 15.5 and 16°C give the same confirmed set, because of the empty
  band between 8% and 30%.
* **Forward candidates.** Candidates are households whose larger register shortfall has held for the latest eight weeks of the extract, and
  six- or ten-week holds return the same households.

## 9. Prompt sketch and deliverables

> I have one specialist revenue-protection crew for January to March and it works one district. Our contractor's field supervisor is sure
> it belongs where referrals have confirmed best. Tell me the district, in a line I can put in the field plan, and send `crew_placement.xlsx`
> with the sheets below, the chart `register_shortfall.png`, and a short `placement_brief.pptx` for the planning meeting.

* `crew_placement.xlsx` — the placement build for all eight districts, the prepayment sheet (ask A), the complaints sheet (ask B) and the
  construction back-test (ask C).
* `register_shortfall.png` — paired bars of expected confirmations per district under the whole-house and register constructions, the chosen
  district marked, and an inset scatter of the 210 corpus cases' larger-register shortfall showing the empty band from 8% to 30%, with the
  twin cases labelled.
* `placement_brief.pptx` — the committed district and why the other seven fall away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each district, prepayment households that ran on emergency credit in more than three weeks of
  the last quarter, and their median weekly top-up. *Device:* a shop top-up is recorded on its vend date but applied on the meter at its
  next communication, as the prepayment guide documents. Matching vends to balances on the vend date overstates emergency-credit weeks in
  three districts. The crew's population is credit meters only.
* **Ask B (device-carried).** For each district, complaints about estimated bills in the last twelve months, as a count and per 1,000
  customers. *Device:* a complaint escalated to the ombudsman is re-logged under a new reference linked to the original, per the
  complaints-handling guide. Counting references double-counts escalations in two districts.
* **Ask C (validity).** For the team's standard score, the whole-house degree-day score and the register construction, the acknowledged
  visits each classifies correctly out of 210 and its error on the three winters' assessed totals.
* **Decoupling.** Clearing the register split changes no figure in asks A or B.

## 11. Rubric arithmetic

8 districts × 2 (ask A) + 8 districts × 2 (ask B) + 3 constructions × 2 (ask C) + the committed district, its expected confirmations and the
margin over C + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Rung leaders are A, B, C, E. E is 5th / 7th / 3rd / 1st; intermediate margins are at least 1.24×; E leads rung 3 by 1.65×.
* E's forward candidates: 16 whole-house plus 40 night-register cases (56). C's 34 are all single-register meters. D holds 27 and no
  two-rate stock.
* Night-register bypasses cut the register 35–60% and the whole house 6–9%; no-fault two-rate households sit at 4–11% whole-house and at
  most 8% on every register.
* Past rates: B 7 of 7 acknowledged (3 of 7 after the disputes register), D 9 of 9 (none overturned), F 4 of 4 (2 of 4), H 3 of 3 (2 of
  3). Customer bases: B 14,800, D 11,200. Nine confirmations in all were overturned, none of them on two-rate meters.
* Cases 2024-117 and 2025-033 are identical on every whole-house column. A's 2026 heat-pump retrofit sits under rung 0 only.
* Prepayment vends and ombudsman re-logs never touch credit-meter consumption or the acknowledgement file.
