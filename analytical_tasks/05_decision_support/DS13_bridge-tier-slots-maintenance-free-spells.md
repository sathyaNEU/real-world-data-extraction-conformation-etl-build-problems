# DS13 — Which 180 bridges get the 12-month inspection cycle, when a decade of repairs hides how fast the unrepaired ones decline

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · infrastructure inspection programmes |
| Mirrors | Risk-based inspection or audit frequency set from a history in which interventions reset the condition being modelled (Google and Meta hardware fleets whose failure curves include component swaps, Amazon supplier audits after corrective-action plans, cloud patch cadences fitted on remediated hosts) |
| Decision shape | An allocation under a cap: 45 in-depth 12-month slots for each of four district crews, 180 in all |
| Committed call | The 180 bridges by crew, and how many of them come out of the 48-month cycle |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · measured #11's architecture (the loud condition-only decoy beaten, the quiet repair contamination of the deterioration record missed), with crews attributed through the maintenance-agreement table (#17) at rung 2 |
| Gate G mechanism | decomposition_attribution, with forecasting |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #17 guesses an attribution the data can settle · #13 validates on one population, applies to another · #15 follows the requester's hunch over the rule |
| Calibration form | Prior-period close-out: the last cycle's inspection close-out (every inspection performed, with date, crew and findings), including the bridges whose scheduled repairs were deferred |
| Driving force | The policy ranks bridges on the probability that a component falls to 4 or below within 24 months. Transitions between inspections are exact, but the decade they cover ran a steel-girder repair programme whose deck overlays and bearing replacements reset component ratings upward. Pooled transitions mix deterioration with repair, so old steel girders on busy routes look four times more stable than an unrepaired girder is, and next cycle's capital programme funds no repairs on them. Only transitions measured over repair-free spells, cut at each work order's completion date, give their decline probability, and that puts 38 of them into the 12-month tier. |

## 1. Situation

A state DOT must decide which bridges go on the 12-month in-depth inspection cycle next cycle. Each of its four district crews can take 45.
The inspection policy ranks bridges on risk: the probability that a component falls to rating 4 or below within 24 months, times the
consequence (traffic times detour length). The DOT holds eleven years of inspection records (one record per inspection, with its date and
component ratings), the work-order file of every repair, next cycle's capital programme, the maintenance-agreement table, traffic and
detour data, and the last cycle's close-out. The chief bridge engineer wants the slots on every bridge rated 5 or worse.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The inspection ratings, the work orders, the capital
  programme, the agreements and the traffic counts are all right. The difficulty is that a rating after a repair is a correct observation
  of a repaired bridge, and a transition count over a decade of repairs cannot say how fast an unrepaired one declines.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chief engineer's view. Risk from pooled inspection-to-inspection transitions, with crews attributed through
  the agreements, still puts only 12 bridges from the 48-month cycle into the tier, and every count reconciles.
* **Instrument repair.** The one suspect field is the inventory's district code read as the inspecting crew (a correct district, not a
  crew). Recording each bridge's inspecting crew directly moves rung 1 to rung 2's 12 movers and leaves rung 0 at none and rung 2 at 12.
  No other file is suspect: every inspection, work order and close-out record is complete and dated, and no field claims a bridge's
  unrepaired decline rate. Inspecting every bridge every year would still record repaired bridges, so the repair-free spells are still
  needed for 38.
* **Lens swap.** The naive read estimates deterioration over every inspection interval in the record. The answer estimates it over
  repair-free spells (a different population of observations) and applies it to bridges next cycle leaves unrepaired.

## 3. The driving force

A strong solver rejects condition-only tiering, because the policy ranks on risk. It builds transition matrices by material, age and
traffic band from consecutive inspections, annualised over each interval's elapsed years, and it assigns bridges to crews through the
maintenance-agreement table, because the close-out shows a freeway corridor in District 3 inspected by District 2's crew. Each step is
competent, and only 12 bridges move up from the 48-month cycle. But the decade behind those transitions ran a steel-girder repair programme.
Deck overlays and bearing replacements restored components to 7 or 8, and the next inspection recorded the repaired bridge. Pooled, those
intervals read as stability or improvement, so old steel girders on busy routes show a 24-month decline probability of 0.031. Cut at each
work order's completion date, the repair-free spells give 0.121. Next cycle's capital programme funds no steel-girder repairs, so the
unrepaired rate is the one that applies. Thirty-eight steel girders displace prestressed bridges rated 5, whose risk barely changes, because
few of them were ever repaired.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Any component rated 5 or worse, worst first, crews by inventory district code | 0 bridges from the 48-month cycle | The draft policy, and the measure the federal review reads | The policy: tiers go on 24-month decline probability × consequence |
| 1 | Risk from pooled inspection-to-inspection transitions, annualised, crews by district code | 7 | A full risk model on eleven years of data | The close-out: District 2's crew inspected 31 District 3 bridges on a freeway corridor, under the agreement table |
| 2 | Crews attributed through the maintenance-agreement table (#17) | 12 | The caps now bind on the crews that actually do the work | The work-order file: 41% of the steel cohort's intervals span a deck overlay or bearing replacement, and the capital programme funds none next cycle |
| 3 | **Decisive:** transitions over repair-free spells (each spell cut at a work order's completion date), annualised, for every bridge the capital programme leaves unrepaired | **38** (D1 4, D2 9, D3 21, D4 4) | — | — |

* **Figure shape.** The count rises at every rung (0, 7, 12, 38), and the answer is the extreme cell. Expected declines covered move the
  same way: 24.9, 27.4, 28.1 and 41.3.
* **Partial correction priced (L3).** Dropping every bridge that ever had a work order, instead of cutting its spells, leaves estimates from
  low-traffic girders and moves 22 (−42%). Cutting spells at work orders but leaving each spell unannualised overstates long spells and
  moves 61 (+61%). The decisive construction with crews by district code moves 33 (−13%).
* **Grid.** Ranking (condition, risk) × crews (district code, agreement) × transitions (pooled, repair-free spells, never-repaired bridges
  only) gives 8 feasible cells, since condition ranking uses no transitions. The nearest wrong count is 33 (−13%), one omission away: the
  agreement table.
* **Why the cohort flips.** At rung 2 the marginal prestressed bridge carries a 2.1× risk advantage over the best old steel girder. The
  decisive rung raises the steel cohort's decline probability 3.9× and the prestressed cohort's 1.1×, a 3.5× relative swing, which leaves the
  steel girder 1.67× ahead.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The work-order file records repairs, and the policy records risk. No document says repairs sit inside the
   transition record, or that next cycle's girders will decline at the unrepaired rate.
2. **No sweepable corpus nominates it.** *In every inspection interval that spans a steel-girder repair, the rating after is at or above the
   rating before, because the programme restored components to 7 or 8.* Every pooled transition count reconciles, and the inspection record
   alone cannot show how fast an unrepaired girder declines. Only the work orders' dates separate repaired from unrepaired spells.
3. **No arithmetic symptom.** Bridges, inspections, ratings and work orders reconcile under every rung, and no rating is wrong.
4. **Not a row predicate.** It needs each bridge's inspections cut into spells at its work orders, transitions taken within spells,
   annualised by elapsed years, pooled by material × age × traffic band, applied to the bridges the capital programme leaves unrepaired, and
   then a capped allocation per crew.
5. **The enumeration is arithmetic.** No column marks an interval as repaired or a bridge's rate as unrepaired; both fall out of the join
   to the work orders.
6. **No cutover date.** The repair programme ran through the whole decade, and nothing steps in any series.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The last cycle's close-out: every in-depth and routine inspection performed, with date, crew, bridge and findings, against the
  eleven years of inspection records and the work-order file.
* **What it certifies.** Two things. Crew workloads are reproduced only by agreement-based attribution (four of four crew totals, against
  one of four by district code). And the 38 steel girders whose scheduled repairs were deferred last cycle, a natural control, showed a
  component drop in 14% of cases, against the 3.6% pooled transitions predict and the 13.8% the repair-free spells predict.
* **What it is blind to on its own.** It holds one cycle, so it cannot by itself give 24-month probabilities by band. It has to be married
  to the decade's spells.
* **Twin pair.** Two cohorts are identical on every inventory column: steel girders built 1966–70, 25,000–35,000 vehicles a day, all
  components rated 6, District 3, 48-month cycle. One sits on the corridor the repair programme overlaid and the other did not. Their pooled
  annual decline rates are 2.0% and 4.4% (2.2×), and their repair-free rates are 4.3% and 4.4%, the unrepaired cohort's two figures being
  the same spells. Only the spell construction reproduces both.
* **Every rule exercised.** Some bridges had two repairs in the decade, so spells of one to four years all occur, and some prestressed
  bridges had bearing work, so the construction is tested outside the steel cohort.
* **Resemblance points at the decoy.** The steel cohort's record (rated 6, ratings steady or rising) looks like the bridges the draft policy
  rightly leaves alone.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The inspection policy: the 12-month tier goes to the highest-risk bridges, risk being the 24-month probability of a
  component at 4 or below times traffic × detour, within each crew's 45 slots. The capital programme: next cycle's funded repairs. The
  maintenance-agreement table: which crew inspects each route segment. One sentence each.
* **Empirical pins.** Repair-free transitions, from the inspections, the work orders and the close-out.
* **Voices.** The chief bridge engineer: "The bridges rated 5 are where the risk is." The District 3 engineer: "Our crew knows our bridges;
  the district is the unit." The asset analyst: "Ten years of inspections is the cleanest deterioration data we have."
* **Licensed wrong basis.** The policy records that the federal division office reviews tier assignments on condition ratings and will see
  that basis.

## 8. Determinism by construction

* **Spell cuts.** A spell ends at a work order's completion date, and the first inspection after it opens the next spell. No work order and
  inspection share a date, so the cut is unambiguous.
* **Annualising.** A multi-year transition is converted to annual steps by matrix root within each band. Root and per-year-hazard
  conventions select the same 38 bridges, because no bridge sits within 4% of the cut.
* **Bands and consequence.** Material, age and traffic bands, the consequence formula and the 24-month horizon are filed in the policy.
* **Caps.** 45 per crew, with ties at the cut broken by bridge number, as the policy states. No tie occurs at any crew's cut.

## 9. Prompt sketch and deliverables

> Next cycle each of our four district crews can take 45 bridges on the 12-month in-depth cycle. The chief bridge engineer wants the slots
> on everything rated 5 or worse. Give me the 180 bridges by crew, and how many of them come out of the 48-month cycle, as the table for the
> inspection plan. Send `tier_plan.xlsx`, a chart `risk_by_cohort.png`, and a one-page `inspection_note.pdf`.

* `tier_plan.xlsx` — the 180 bridges by crew under each construction, the field-hours sheet (ask A), the posting sheet (ask B) and the
  transitions sheet (ask C).
* `risk_by_cohort.png` — decline probability by cohort under pooled and repair-free transitions as paired bars, each crew's cut-off risk as
  a labelled marker, the steel cohort annotated, and a panel of one steel girder's inspection ratings over the decade with its work orders
  marked.
* `inspection_note.pdf` — the plan, the count from the 48-month cycle, and why the rated-5 bridges give way.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each crew and structure type, last cycle's mean field hours per in-depth inspection.
  *Device:* an inspection spanning two days is logged as two timesheet rows under one inspection ID, as the timesheet dictionary documents.
  Averaging by row halves the steel-truss figures.
* **Ask B (device-carried).** For each district, the deck area of bridges load-posted on 1 October. *Device:* postings are effective-dated,
  and a posting lifted and reinstated appears twice. Reading the table as of the date, not by counting rows, avoids overstating two districts
  by 12–18%.
* **Ask C (validity).** Each cohort's 24-month decline probability under pooled and repair-free transitions, and the four crews' close-out
  workloads under district-code and agreement attribution.
* **Decoupling.** Clearing the spell construction changes no figure in asks A or B. Timesheets and postings never enter a transition or a
  risk.

## 11. Rubric arithmetic

4 crews × 3 structure types (ask A) + 4 districts (ask B) + 6 cohorts × 2 methods + 4 crews × 2 attributions (ask C) + the movers by crew
(4), the total and the expected declines covered + 5 named chart parts + 3 files ≈ 56 criteria.

## 12. World-building constraints

* 64 old steel girders on busy routes, all on the 48-month cycle. Their 24-month decline probability is 0.031 from pooled transitions and
  0.121 from repair-free spells. Prestressed bridges rated 5 on the 24-month cycle: 0.14 and 0.155.
* 41% of the steel cohort's intervals span a work order. The capital programme funds no steel-girder repair next cycle. The 38 deferred
  girders show a 14% drop rate in the close-out. 31 District 3 freeway bridges are inspected by District 2's crew.
* Movers 0 / 7 / 12 / 38. The partials give 22, 61 and 33. Expected declines covered: 24.9 / 27.4 / 28.1 / 41.3.
* The twin cohorts are identical on every inventory column. Timesheets and postings never touch ratings, work orders, crews or traffic.
