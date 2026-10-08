# DS42 — Which component gets this quarter's standby-capacity reservation, when analysts are weighted against the aggregate they form

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Supply Chain & Logistics · supply-risk contingency planning |
| Mirrors | Weighting forecasters or models by skill measured against a consensus they help form (peer-scored internal forecasting, ensemble weights in demand forecasting, analyst-weighted sales pipelines), where a weight cap binds only once the weights settle |
| Decision shape | Which of N gets one scarce thing: this quarter's single standby-capacity reservation with a backup supplier, among six at-risk components |
| Committed call | The component reserved, and its expected avoided loss next quarter, in $ millions to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 3 (objective) · S5, a ceiling that binds only after a self-referencing solve (analyst weights scored against the aggregate they form, capped at 15%), with a binding limit applied in the figure (E14) at rung 1 |
| Gate G mechanism | method_or_model_selection, with binding_constraint |
| Measured traps engaged | #22 solves a self-referencing rule in one pass · #10 notes a binding limit as a risk · #15 follows the requester's hunch over the rule |
| Calibration form | Counterparty acknowledgement file: the backup suppliers' acknowledgements of the standby capacity they held for each of the last eight quarters' reservations, and what they delivered when called |
| Driving force | The committee weights each analyst by how far their resolved forecasts beat the committee's own aggregate, and the aggregate is built from those weights. In one pass against the plain average, skill looks widespread and no weight nears the 15% cap. At the fixed point the aggregate is sharper, only two Asia-logistics analysts still beat it, both hit the cap, and their view of a port strike moves the reservation. |

## 1. Situation

An electronics manufacturer's supply-risk committee buys one standby-capacity reservation a quarter: a backup supplier holds capacity for
one critical component in case its main source is disrupted. Six components (C1–C6) are on the risk list. The committee's charter sends
the reservation to the component with the largest expected avoided loss: the committee's aggregate probability of disruption next quarter,
from 24 analysts' forecasts, times the loss the reservation would cover. The charter defines the aggregate's weights. The procurement
director considers the sanctions exposure the obvious choice.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the analysts' forecasts, the resolved questions, the exposure register, the acknowledgements and
  last quarter's minutes. No stakeholder read is overturned: the sanctions exposure is large and its probability high on most readings.
  The difficulty is computing the aggregate the charter actually defines.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and the audit committee's basis. The charter's weights computed in one pass still name C2.
* **Instrument repair.** Resolve every past question instantly and record every forecast perfectly. The weights are still defined against
  an aggregate that depends on them, so the one-pass reading still misses the fixed point.
* **Lens swap.** The naive read and the answer differ in population: an aggregate in which 19 analysts carry weight, against the one the
  charter defines, in which the weight concentrates on the few who beat it.

## 3. The driving force

A strong solver caps each component's avoided loss at the capacity its backup supplier has acknowledged, then builds the committee's
aggregate as the charter says: each analyst weighted by how far their Brier score on the last eight quarters' resolved questions beats the
aggregate's on the same questions, floored at zero and capped at 15%, with any excess shared among the rest. The natural computation
measures each analyst against the plain average, the only aggregate to hand, and 19 analysts beat it modestly, so the weights spread
thinly and nobody nears 15%. C2's sanctions risk tops the list. But the benchmark is the weighted aggregate itself. Recompute the
aggregate with those weights, re-score everyone against it, and repeat: the aggregate sharpens, most analysts stop beating it, and weight
flows to the two Asia-logistics analysts whose forecasts beat even the sharpened aggregate. Both hit the cap, the excess is redistributed,
and the iteration settles. The settled aggregate puts the port strike that would cut C4's main supplier at 0.52, against 0.31 in the
one-pass aggregate, and the sanctions action against C2's controller at 0.34, against 0.42.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Plain average of the analysts' latest probabilities × the component's full exposure | C1, a display driver ($9.6M against C2's $7.8M) | The committee's long-standing practice | The charter: a reservation covers only the capacity the backup supplier has acknowledged, and C1's backup acknowledged 30% |
| 1 | Plain average × exposure capped at acknowledged backup capacity | C3, a power module ($6.4M against C2's $5.2M) | The binding limit applied in the figure, not noted as a risk | The charter: the aggregate weights analysts by resolved skill, not equally |
| 2 | Charter weights measured against the plain average in one pass, capped exposure | C2, a sanctions-exposed controller ($6.3M against C3's $5.1M) | The charter's rule, applied with the only aggregate available | Last quarter's minutes publish all 24 weights; one-pass weights match 9 of them |
| 3 | **Decisive:** weights and aggregate solved together to the fixed point, cap and redistribution applied at each step; capped exposure | **C4, a memory part shipped through one port ($8.2M)** (4th of six on rung 0) | — | — |

* **Position table.** C4 is 4th on rung 0 ($6.0M), 3rd on rung 1 ($4.6M) and 3rd on rung 2 ($4.9M); it is never second and leads only rung
  3. Rung margins: C1 over C2 1.23×, C3 over C2 1.23×, C2 over C3 1.24×, C4 over C6 1.37× ($8.2M against $6.0M).
* **Discriminator dominance.** C2 carries a 1.29× advantage over C4 into rung 3 ($6.3M against $4.9M). The fixed point multiplies C4's
  probability by 1.68 (0.31 to 0.52) and C2's by 0.81 (0.42 to 0.34), a relative edge of 2.07, against the required 1.2 × 1.29 = 1.55 and
  past the 2.01 that headroom asks.
* **Partial correction priced (L3).** No half-applied solve names C4. Applying the cap to one-pass weights changes nothing, since no
  one-pass weight nears 15%, and names C2 at $6.3M. Re-scoring once against the one-pass weighted aggregate, a second pass rather than a
  solve, names C2 at $5.9M, 1.18× over C4's $5.0M. Iterating to the fixed point without the cap hands analyst 21 31% of the weight; her
  typhoon forecasts for C6's port carry the aggregate, and it names C6 at $9.6M, 1.20× over C4's $8.0M.
* **Grid.** Exposure (full, acknowledged) × weights (equal, one-pass, fixed point uncapped, fixed point capped) = 8 cells. They name C1, C3,
  C2 or C6; only acknowledged exposure with capped fixed-point weights names C4, and full exposure with the same weights names C1 ($12.0M
  against C4's $10.4M).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter defines weights against the aggregate; it never says the definition is circular or that it must be
   solved. The cap reads as a guard that, in one pass, never binds.
2. **Corpus blind for a computable reason.** *Every acknowledgement records capacity held and delivered, so it is the same under every
   weighting and cannot speak to the aggregate.* It certifies rung 1's limit exactly. The fixed point is pinned instead by the definition
   itself and by last quarter's published weights: 24 of 24 under the fixed point, 9 under one pass.
3. **No arithmetic symptom.** One-pass weights sum to one, sit under the cap, and give a sensible aggregate.
4. **Not a row predicate.** Weights, aggregate and skill scores are solved together over 212 resolved questions, with the cap and
   redistribution inside the iteration.
5. **The enumeration is arithmetic.** No column holds the settled weights.
6. **No cutover date.** The resolved questions span eight quarters; nothing steps.
7. **Survives deletion.** No wrong number exists to delete. Without the director, the one-pass reading still names C2.

## 6. The calibration corpus

* **Form.** The acknowledgement file: for each of the last eight quarters' reservations, the capacity requested, the capacity the backup
  supplier acknowledged, and the capacity delivered when called.
* **What it certifies.** Rung 1: delivered cover equalled acknowledged capacity in 8 of 8 reservations, never the request.
* **What it is blind to.** The aggregation (above).
* **Twin pair.** Analysts 07 and 15 are identical on every column the forecast file and the roster show: 44 resolved questions, a raw
  Brier score of 0.161, the same regions and tenure. At the fixed point their weights are 0.12 and 0.06 (2.0×): analyst 07's forecasts beat
  the aggregate on the questions where it was confident and wrong. Only the self-referencing solve separates them.
* **Resemblance points at the decoy.** By exposure and region, C4 most resembles last year's reservation for a component whose port
  disruption never came.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the reservation goes to the component with the largest aggregate probability of disruption next quarter
  times the loss the reservation would cover; a reservation covers only acknowledged capacity; the aggregate is the weighted mean of
  analysts' latest probabilities, each analyst weighted by the amount their Brier score on the last eight quarters' resolved questions
  beats the aggregate's on the same questions, floored at zero, with no analyst above 15% and any excess shared pro rata. The exposure
  register.
* **Empirical pins.** None beyond the published weights, which confirm the fixed point.
* **Voices.** The procurement director: "The sanctions exposure is the obvious one." The chief risk officer: "We have always averaged the
  analysts; weighting is a refinement." The treasury lead: "Hedges should follow the biggest exposure."
* **Licensed wrong basis.** The charter records that the board's audit committee reviews the reservation against the plain analyst
  average and will see that table.

## 8. Determinism by construction

* **Fixed point.** The map from weights to weights is a contraction under the floor and cap; iteration from equal, one-pass or random
  starting weights converges to the same weights within 10⁻⁶ in under 30 steps.
* **Forecasts.** Each analyst's latest probability on each question at the committee's cut-off; no analyst revised within an hour of it.
* **Exposure.** Acknowledged capacity times the component's loss rate per unit, both filed; no component's cap sits within 5% of its full
  exposure.
* **Rounding.** C4's $8.22M and C6's $6.00M sit clear of the rounding edges.

## 9. Prompt sketch and deliverables

> The committee buys one standby-capacity reservation this quarter, and six components are on the risk list. The procurement director's
> view is that the sanctions exposure is the obvious one. Tell me which component gets the reservation and the loss it should avoid next
> quarter, in $ millions to one decimal, as the line for the committee minutes. Send `reservation_case.xlsx`, a chart
> `aggregate_by_weighting.png`, and a one-page `committee_minute.docx`.

* `reservation_case.xlsx` — the six components under the four rung bases, the weight table at one pass and at the fixed point (ask C), the
  time sheet (ask A) and the supplier sheet (ask B).
* `aggregate_by_weighting.png` — each component's aggregate probability under equal, one-pass and fixed-point weights as grouped bars, with
  the two capped analysts' weights shown in an inset against the 15% line, and C4 marked.
* `committee_minute.docx` — the committed component and avoided loss, and why the one-pass aggregate is not the charter's.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 24 analysts, hours logged on forecasting last quarter. *Device:* entries that
  cross midnight are stored as two rows under one entry ID, as the time-system guide documents; summing rows and counting entries
  double-counts the night sessions of nine analysts.
* **Ask B (device-carried).** For each of the six backup suppliers, last year's on-time rate on regular orders. *Device:* promises are in
  the supplier's time zone and receipts in the warehouse's, a date line apart, as the receiving guide records. Comparing raw dates marks
  on-time Asian deliveries late.
* **Ask C (validity).** Each component's expected avoided loss under the four rung bases, and the number of analysts at the cap under one
  pass and at the fixed point.
* **Decoupling.** Clearing the fixed point changes no figure in asks A or B. Time entries and regular-order receipts touch no forecast,
  acknowledgement or exposure record.

## 11. Rubric arithmetic

24 analysts (ask A) + 6 suppliers (ask B) + 6 components × 4 bases + 2 cap counts (ask C) + the committed component, its avoided loss, the
runner-up and the margin + 5 named chart parts + 3 files ≈ 68 criteria.

## 12. World-building constraints

* Rung 0: C1 $9.6M, C2 $7.8M, C3 $7.1M, C4 $6.0M, C5 $4.4M, C6 $3.0M. Rung 1: C3 $6.4M, C2 $5.2M, C4 $4.6M, C5 $3.8M, C1 $2.9M. Rung 2: C2
  $6.3M, C3 $5.1M, C4 $4.9M, C6 $2.4M. Rung 3: C4 $8.2M, C6 $6.0M, C2 $5.1M, C3 $4.4M.
* Acknowledged exposure: C4 $15.8M, C2 $15.0M, C6 $24.0M (60% of its full $40M). Probabilities, one-pass / fixed point / uncapped fixed
  point: C4 0.31 / 0.52 / 0.506; C2 0.42 / 0.34; C6 0.10 / 0.25 / 0.40. Full exposure at the fixed point: C1 $12.0M, C4 $10.4M.
* 24 analysts, 212 resolved questions; one-pass: 19 analysts with positive weight, none above 9%; fixed point: analysts 03 and 21 at 15%,
  nine with positive weight; uncapped: analyst 21 at 31%.
* Last quarter's minutes: 24 weights, all reproduced by the fixed point. Analysts 07 and 15 match on every forecast and roster column.
* Time entries and receipts are independent of every main-call record.
