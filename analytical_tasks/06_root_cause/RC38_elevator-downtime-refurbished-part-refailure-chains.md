# RC38 — Which cause of the elevator downtime rise the maintenance budget fixes, when every flag on the monitor is right and none shows it

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · transit asset maintenance |
| Mirrors | Incident triage where every dashboard alert has an owner and an explanation and the driver is a sequence no alert expresses (repeat incidents after a bad remediation at Google and Meta, warranty returns after refurbished-part repairs at Apple and Amazon, tickets re-opened after a vendor's fixes) |
| Decision shape | Which of N root causes gets the fix: this year's maintenance improvement budget funds one of five programmes |
| Committed call | The one cause the budget addresses, named in a sentence, with the rise in unplanned downtime hours each cause accounts for |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · S7 (every screen is right and the answer is what nothing flags): re-failure chains at the repair-sequence grain |
| Gate G mechanism | decomposition_attribution, with signal_vs_noise_or_hold support |
| Measured traps engaged | #18 joins only on the visible key · #11 beats the headline trap, misses the quiet one · #7 uses the ready-made measure |
| Calibration form | Settled-transaction ledger: the maintenance subcontractors' settled repair invoices for the four closed years, with parts lines and purchase-order references |
| Driving force | Every flag on the monitor is right and has an explanation: busy stations wear units out, discontinued models wait for parts, night callouts have a contractual window and street units flood. The downtime that grew is in none of them. It is in chains: a door operator replaced with a refurbished unit under this year's parts framework fails again within days, is replaced again and fails again. A chain shows only when each unit's repairs and failures are put in order and the failing component is matched to the part fitted, through the invoice's purchase order to the work order. |

## 1. Situation

The city transit authority's elevator availability fell from 97% to 94%, and unplanned downtime rose by 25,000 hours. This year's maintenance
improvement budget funds one programme: capital replacement of old units, a parts-inventory programme, a night-response staffing clause,
waterproofing of street-level units, or quality assurance on fitted parts. The maintenance contractor wants replacement and points to the
monitor's high-frequency flags. The asset manager suspects parts waits, and disability advocates cite night response times. The authority's
budget rule funds the programme whose cause accounts for the most added downtime.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the outage records, work orders, the monitor's four flags, the parts catalogue, the contract
  response windows and the settled invoices. Each flag is high for a documented, legitimate reason. Nothing is overturned. The difficulty is
  a cause the monitor's grain cannot express.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete every voice and the monitor itself. The outage and work-order records still decompose into the four
  familiar causes, and no unit-level or outage-level table shows a chain.
* **Instrument repair.** Record every outage and repair to the minute. Chains are still sequences across records, linked through the
  parts fitted, and no better per-outage instrument contains them.
* **Lens swap.** The naive causes are properties of units or outages. The answer is a population of repair-then-failure sequences tied to
  one part source, a different unit of analysis.

## 3. The driving force

A strong solver ignores the contractor's count, because availability is frequency times duration. It decomposes downtime into each
outage's existence and its response, parts-wait and repair time, and it links outages to work orders. The explicit key covers 82% of
outages. The rest are re-dispatches, logged under their parent ticket as the maintenance manual describes, and once those are linked the
parts waits lead. That is a satisfying, root-caused answer, and the parts-inventory programme looks right. But many of the outages it counts
are the same failure repeated. This year's parts framework introduced refurbished door operators. A unit whose door operator was
replaced with one fails on that component again within days, typically five times in a row, and every repeat has its own existence, response
and parts wait. Read one at a time, each repeat is an ordinary outage on a busy old unit, an ordinary parts wait or an ordinary callout.
Put in sequence by unit and component, and matched to the part fitted through the invoice's purchase order, they form chains carrying 9,600
of the added hours.

## 4. The ladder

| Rung | Construction | Names (added downtime, thousand hours) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Outage counts × average duration, by the monitor's flags | Capital replacement (12.6, 2.33×) | The contractor's dashboard and the reported KPI | Availability is frequency × duration, and the duration records split each outage into response, parts wait and repair |
| 1 | Downtime by duration component, outages linked to work orders on the explicit key | Night response (10.4, 1.53×) | Duration-aware, heavy tail included, every linked outage caused | The maintenance manual: re-dispatches carry only a parent-ticket reference, and 18% of outages link that way |
| 2 | Hygiene of the join: re-dispatches linked through their parent ticket | Parts inventory (9.2, 1.35×) | Every outage now caused, and the parts timestamps tie to the invoices | Each unit's repair sequence: the same component fails again within days of a refurbished door operator being fitted |
| 3 | **Decisive:** failures ordered by unit and component, chained to the prior repair, and matched to the part fitted through PO → work order | **Parts quality assurance (9.6, 1.60×)**, 5th on rung 0 | — | — |

* **Position table.** Parts quality assurance ranks 5th on rungs 0, 1 and 2 and leads only rung 3. The other four sizes at rung 3 are parts
  waits 6.0, ageing 3.8, response 3.2 and water 2.4.
* **Discriminator dominance.** Parts waits carry a 9.2 lead over the chains into rung 3. The chain construction takes 3.2 from parts waits
  and gives the chains 9.6, a 12.8 swing, 1.39× the carried lead.
* **Partial correction priced (L3).** A solver who sequences repeats by unit but not by component sweeps in coincident faults on busy old
  units and books the repeats to ageing. One who matches components but never reaches the invoice's parts lines cannot tell refurbished
  chains from waits on discontinued models, and books them to parts waits. Each half names a wrong programme.
* **Grid.** Join (explicit or parent) × measure (counts or downtime) × sequence (none, by unit, by component, by component and part) = 16
  cells. Only parent links, downtime and component-and-part chains name parts quality assurance.
* **Control totals.** Added downtime is 25.0 thousand hours on every rung, because each construction partitions the same outage hours.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The parts framework is a procurement record. No document links refurbished parts to failures or describes repeat
   sequences.
2. **Corpus blind for a computable reason.** *Every door operator fitted in the closed years was a new manufacturer part, because the
   refurbished-parts framework began this year, so no settled invoice belongs to a refurbished-part chain.* The ledger certifies the duration
   components and the parent-ticket links in all four closed years.
3. **No arithmetic symptom.** Outages, work orders, invoices and availability reconcile on every rung, and the 25.0 total is invariant.
4. **Not a row predicate.** A chain needs each unit's failures and repairs ordered, the failing component matched to the previous repair's
   component, and that repair's fitted part read from the invoice reached through its purchase order.
5. **The enumeration is arithmetic.** No outage carries "repeat" or "refurbished". Chains come out of the sequence and the join.
6. **No cutover date.** Refurbished operators were fitted as units happened to fail across the year, so no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The subcontractors' settled repair invoices for the four closed years: labour, parts lines with part numbers and suppliers, and
  the authority's purchase-order reference.
* **What it certifies.** The duration components and the join. Parts-receipt dates on invoices match the work orders' parts-wait end
  times, and re-dispatch invoices reference their parent ticket's purchase order, 100% in every closed year.
* **What it is blind to.** Refurbished-part chains (property 2).
* **Twin pair.** Units ELV-214 and ELV-388 are identical on age, station usage, model, outage count this year (9 each) and every monitor flag.
  Their added downtime is 410 and 205 hours (2.0×). ELV-214's door operator was replaced with a refurbished unit in February and failed in two
  chains. Only the component-and-part sequence reproduces both.
* **Resemblance points at the decoy.** The units carrying the most chain downtime most resemble the monitor's high-frequency units, old and
  at busy stations, so by resemblance ageing explains them.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The budget rule: "The improvement budget funds the programme whose cause accounts for the most added unplanned downtime."
  The maintenance manual: "A re-dispatch is logged against its parent ticket." The contract fixes the night response window.
* **Empirical pins.** Duration components come from work-order timestamps confirmed against invoices. Chains come from the sequence.
* **Voices.** Maintenance contractor: "These units are thirty years old; replace them and the outages stop." Asset manager: "We wait weeks for
  parts on the discontinued models." Disability advocates' coalition: "At night it takes hours for anyone to come."
* **Licensed wrong basis.** The budget rule records that the capital committee reads equipment condition from the monitor's high-frequency
  flag and will see the proposal on that basis.

## 8. Determinism by construction

* **Chain window.** Every repeat in a refurbished chain falls within 9 days of the prior repair, and no other same-component repeat falls
  within 30, so any window from 10 to 30 days gives the same chains.
* **Component matching.** Work-order component codes map one to one onto invoice part numbers, as the parts catalogue lists.
* **Attribution order.** A chained outage's whole downtime (existence, response, parts wait and repair) belongs to the chain, the convention
  under which the budget rule's causes partition the hours.
* **Censoring and scope.** Outages open at the extract are clipped at year-end, and none is in a chain. Planned outages are excluded by type.
* **Maturity.** This year's invoices are settled for every work order in the extract.

## 9. Prompt sketch and deliverables

> This year's maintenance improvement budget funds one programme, and I take the choice to the committee on the 12th. The contractor is sure
> old age is behind the downtime. Name the cause the budget should go to, as a sentence the committee can adopt, with the added downtime each
> of the five causes accounts for in thousands of hours. Send `downtime_causes.xlsx`, a chart `cause_downtime.png`, and a one-page
> `budget_choice.pdf`.

* `downtime_causes.xlsx` — the five causes on every construction, the escalator sheet (ask A), the usage sheet (ask B) and the ledger
  back-test (ask C).
* `cause_downtime.png` — each cause's added downtime as the ladder moves (counts, explicit key, parent links, chains), with a timeline inset
  of ELV-214's repairs and failures linked into its chains. The funded cause is marked, and the title names it.
* `budget_choice.pdf` — the named cause and why each other programme removes less.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Escalator availability for each of 12 station complexes in each half-year. *Device:* an escalator
  stopped and opened as stairs is logged as an outage status, and the authority's availability definition counts it as available, as the
  outage dictionary states. Counting it as an outage understates availability by 2 to 4 points at the complexes that use stair mode. No
  escalator record enters the elevator analysis.
* **Ask B (device-carried).** Average daily door cycles for the 30 busiest elevators this year. *Device:* cycle counters roll over at
  999,999, and the telemetry guide documents the correction. Raw differences go negative at seven units and wreck their averages. Usage
  counters never enter the downtime attribution.
* **Ask C (validity).** For each closed year, parts-wait hours from work-order timestamps beside those implied by invoice parts receipts.
* **Decoupling.** Clearing the chain construction changes no figure in asks A or B. Ask C runs on years with no refurbished parts.

## 11. Rubric arithmetic

12 complexes × 2 half-years (ask A) + 30 units (ask B) + 4 closed years × 2 measures (ask C) + the named cause, five sizes and the winning
margin + 5 named chart parts + 3 files ≈ 77 criteria.

## 12. World-building constraints

* Added downtime is 25.0 thousand hours. True causes are chains 9.6, parts 6.0, ageing 3.8, response 3.2 and water 2.4. The chains' 9.6
  appears under ageing 3.0, parts 3.2, response 2.4 and water 1.0 until sequenced.
* Re-dispatches are 18% of outages and carry 4.8 thousand hours of parts waits.
* Refurbished door operators were fitted from this year's framework only. Every chain repeat falls within 9 days, and no other
  same-component repeat within 30.
* ELV-214 and ELV-388 are identical on every monitor and inventory column.
* Stair-mode statuses and counter rollovers never touch elevator outages, work orders or invoices.
