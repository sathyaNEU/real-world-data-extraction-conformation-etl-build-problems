# DS33 — Which heart-bypass centres an employer designates inside its $14.0M cap, when all three proposed packages fail a condition

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Policy & Education · employer health-benefit purchasing |
| Mirrors | Designating a preferred-supplier set under quality, coverage and budget conditions when every proposed shortlist fails one (cloud and SaaS vendor panels, preferred-carrier lanes at Amazon and Walmart, centres-of-excellence networks at large tech employers) |
| Decision shape | An allocation under a cap: up to four designated centres, and the episodes routed to them, within the $14.0M programme cap |
| Committed call | The centres designated, and the programme's projected cost in $ millions to one decimal |
| Gap · Pattern | Gap 3 (objective) over Gap 2 (population) · measured #9's architecture (the admissible package sits off the slate), with a suppressed cell bounded by published totals (E25) killing rung 1 |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #9 picks from the offered options when none passes · #24 treats an unpublished figure as unknown · #10 notes a binding limit as a risk |
| Calibration form | Prior-period close-out: last plan year's programme close-out, with episodes by site and centre, bundled payments, travel paid and the total against that year's cap |
| Driving force | Each of the consultant's packages fails one condition, but only under constructions the policy and the state report force: one hospital fails on its risk-adjusted rate, a second on a rate the state suppressed and its regional totals pin above the line, the third on members routed by road miles to its dearest centre. The policy then designates the package that meets every condition from all eligible hospitals, and exactly one does. |

## 1. Situation

A self-insured employer with 118,000 members at nine sites designates up to four centres of excellence for heart-bypass episodes next
plan year. Members who use a designated centre pay nothing and have their travel paid, and the centre is paid a bundled price. The benefits
policy sets four conditions: each centre's risk-adjusted 30-day readmission rate, as the state publishes it, below the statewide 14.6%;
every site within 120 road miles of a designated centre; projected cost within the $14.0M cap; and each centre's routed episodes within
its bid capacity. The consultant has proposed three packages (P1–P3). The CFO's view is that if none fits, the closest will do.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the state report, its regional totals, the bids, the travel schedule, the road distances and last
  year's close-out. No stakeholder read is overturned. The consultant's raw rates are the rates hospitals report, and each package is
  close to compliant. The difficulty is that the choice set is wider than the slate, and the slate fails only once the conditions are
  built properly.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the CFO's view and the committee's raw table. The slate still reads as the choice set, and with the state's
  suppressed rate read as "no breach shown" one package still passes.
* **Instrument repair.** Suspect file: the state report, which suppresses H9's first-year rate. Repaired with the rate itself, 15.4%, rung 1
  can no longer pass P2 and lands with rung 2 on P3; rung 0 still names P1. Every slate package still fails a condition, so the search over
  all eligible packages is still needed to find H2, H6, H7 and H11.
* **Lens swap.** The naive read and the answer differ in population: the consultant's three packages against every package the eligible
  hospitals can form.

## 3. The driving force

A strong solver takes the policy's four conditions and checks the consultant's three packages against them. On raw rates P1 passes and is
cheapest. On the state's risk-adjusted rates, P1's hospital H3 sits at 15.2% and fails. P2 then passes, because its hospital H9 has no
published rate: the state suppresses a merged hospital's rate in its first year, and an unpublished rate shows no breach. But the state
publishes the region's observed and expected readmissions, and the region's other five hospitals publish theirs. H9's counts follow by
subtraction, up to the rounding of expected counts, and they put its rate between 15.1% and 15.8%. Every package now fails: routed by road
miles, as the policy routes members, P3 sends the river towns across the only bridge to its dearest centre, and its cost reaches $14.6M. The CFO's instinct (take the closest) is where most analyses stop. The policy
does not allow it. It designates the package that meets every condition, from all eligible hospitals, may not leave the programme empty,
and renews last year's package only if it qualifies. One package of four does: H2, H6, H7 and H11, at $13.8M.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The slate on the consultant's raw readmission rates, members routed by road miles; cheapest package that passes | P1 ($10.9M against P2's $12.6M) | The consultant's own measure, and the cheapest compliant option | The policy's quality condition is the state's risk-adjusted rate, on which H3 stands at 15.2% |
| 1 | Risk-adjusted rates; H9's suppressed rate read as no breach shown | P2 ($12.6M), the only package passing | A careful reading of the published report, which shows nothing against H9 | The state's regional totals and the region's other five hospitals bound H9's rate to 15.1–15.8% |
| 2 | Every slate package now fails one condition; recommend the closest, P3, with its 4.3% overrun flagged to the CFO | P3 ($14.6M) | Thorough, honest, and in line with the CFO's instruction | The policy's open-set clause: the plan designates the package that meets every condition, from all eligible hospitals, never none and never last year's unless it qualifies |
| 3 | **Decisive:** every package of up to four eligible hospitals, routed by road miles within bid capacities, tested on all four conditions | **H2, H6, H7 and H11 at $13.8M** (on rung 0's reading, the fifth-cheapest admissible package) | — | — |

* **Position table.** The answer package is never on the slate, so no intermediate rung names it. On rung 0's own reading it is admissible
  and fifth-cheapest, behind P1, P2 and two packages built on H3 and H9. Rung leaders are P1, P2, P3, then the answer. P1 leads rung 0 by
  1.16× on cost; rungs 1 to 3 each have exactly one admissible package under their reading.
* **Dominance.** Here dominance is admissibility, not size. The slate's failures sit where no convention closes them: H3 at 15.2% and H9 at
  no less than 15.1% against 14.6%, and P3 4.3% over the cap. The answer clears the cap by 1.4% and meets the other three conditions by
  margins of at least 0.6 points, 9 road miles and 11 episodes.
* **Partial correction priced (L3).** Each half-insight names a different wrong package. A solver who searches beyond the slate but reads
  H9's suppressed rate as no breach finds H2, H9, H7 and H11 at $13.2M, which under that reading beats the answer's $13.8M by 4.5%. One
  who routes by straight-line distance finds H2, H5, H7 and H11 clearing the cap on paper at $13.5M, and cannot reach the answer at all:
  by straight line the river towns go to H2, and H6 falls 24 episodes below the volume floor. Routed by road, that package sends the
  river towns to H5 instead of H2 and costs $14.3M, over the cap.
* **Grid.** Rates (raw, risk-adjusted) × H9 (no breach shown, bounded) × scope (slate, all packages) × routing (straight line, road miles)
  = 16 cells. They name P1, P2, P3, the H9 package or the straight-line package; only risk-adjusted, bounded, all packages and road miles
  names the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy states the conditions and that packages are not limited to those proposed. No document says the slate
   fails, which hospital's suppressed rate breaches, or which package qualifies.
2. **Corpus blind for a computable reason.** *Last year one of the consultant's packages met every condition, so the close-out holds a
   slate pick and has nothing to say about looking beyond the slate.* It certifies the cost model exactly.
3. **No arithmetic symptom.** Rates, counts, distances and costs reconcile under every reading, and a suppressed cell is a normal feature
   of the state report.
4. **Not a row predicate.** Each package's admissibility needs routing every site to its nearest designated centre by road miles within
   capacity, then cost and access over the whole package, with H9's rate recovered by subtraction across a region.
5. **The enumeration is arithmetic.** Which package qualifies is the result of testing every combination; no column marks one.
6. **No cutover date.** The merger that suppressed H9's rate is a reporting rule, not a step in any series the decision reads.
7. **Survives deletion.** No wrong number exists to delete. Without the CFO, the slate still reads as the menu.

## 6. The calibration corpus

* **Form.** Last plan year's close-out: the designated package, episodes by site and centre, bundled payments, travel paid per episode and
  the total against that year's cap.
* **What it certifies.** The cost model: episodes by site, routed to the nearest designated centre by road miles within capacity, at bid
  prices plus travel per the schedule, reproduce last year's total to the dollar and every site's travel to within $1. Straight-line
  routing misses the total by 6.8%, every miss low.
* **What it is blind to.** The open set (above).
* **Twin pair.** H9 and H12 both merged last year, so the state suppresses both rates, and they are identical on every column the report
  and the bid sheet show: 610 cases, bid price, capacity and region type. Bounded by their regions' totals, H9's rate is 15.1–15.8% and
  H12's 7.4–7.9% (2.0×). Read as "no breach shown" they are indistinguishable; only the subtraction separates them.
* **Resemblance points at the decoy.** P3 shares three of its four centres with last year's package, which closed out inside its cap.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The benefits policy: the four conditions; the plan designates the package of up to four centres that meets every
  condition, and packages are not limited to those proposed; the programme may not be left without a designated centre; last year's package
  is renewed only if it meets every condition. The travel schedule: $0.62 per road mile and two nights' lodging at $180 for centres beyond
  50 road miles. The routing rule: members go to the nearest designated centre by road miles, overflowing to the next nearest when a
  centre's bid capacity is reached. The cap: $14.0M.
* **Empirical pins.** Episode rates by site, from the close-out.
* **Voices.** The consultant: "Raw readmission rates are what employees understand." The medical director: "Risk adjustment is the only
  fair comparison." The CFO: "If none of them fits the budget, we take the closest."
* **Licensed wrong basis.** The policy records that the benefits committee will receive the consultant's raw-rate table with the
  resolution.

## 8. Determinism by construction

* **The bound.** H9's rate follows by subtraction; rounding of the published expected counts to one decimal gives the 15.1–15.8% interval,
  wholly above 14.6%, so the convention for rounding cannot rescue it.
* **Distances.** Road miles come from the shipped site-to-hospital distance table; no site sits within 5 road miles of the 120-mile access
  line or of an equal-distance tie between two candidate centres.
* **Uniqueness.** Of the 793 packages of one to four eligible hospitals, exactly one meets all four conditions. The nearest failures miss
  the cap by $0.3M or capacity by 6 episodes.
* **Episodes.** Episode rates by site come from the close-out's three-year average, which equals each single year to within one episode.

## 9. Prompt sketch and deliverables

> Our centres-of-excellence programme for heart-bypass episodes renews on 1 January inside its $14.0 million cap, and the consultant has
> put three packages in front of us. The CFO's view is that if none of them fits, we take the closest. Tell me which centres we designate
> and the programme's projected cost, in $ millions to one decimal, as the resolution for the benefits committee. Send
> `designation_case.xlsx`, a map `centres_and_sites.png`, and a one-page `committee_resolution.docx`.

* `designation_case.xlsx` — the three slate packages and the answer on all four conditions (ask C), the visit sheet (ask A) and the travel
  sheet (ask B).
* `centres_and_sites.png` — the nine sites and the eligible hospitals on a map, with the answer's centres marked, each site's routed centre
  drawn as a line labelled with road miles, the 120-mile access rings, and H9 flagged with its bounded rate.
* `committee_resolution.docx` — the committed centres and cost, and the condition each slate package fails.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine sites, the share of last year's bypass members with a primary-care visit in
  the 90 days before admission. *Device:* telehealth visits are stamped with their billing date, not their service date, and carry their own
  place-of-service code, as the claims guide documents. Reading every visit by its stamp moves 11% of telehealth visits outside or inside
  the window at four sites.
* **Ask B (device-carried).** For each of the nine sites, members who claimed travel for any covered procedure last year and the average
  reimbursed miles per trip. *Device:* travel claims are filed per leg, outbound and return, linked by a trip ID the travel guide
  documents. Counting legs doubles trips and halves miles per trip.
* **Ask C (validity).** For P1, P2, P3 and the answer, the value of each of the four conditions: the worst centre's rate, the farthest
  site's road miles, the projected cost and the tightest capacity margin.
* **Decoupling.** Clearing the open set and the bound changes no figure in asks A or B. Visit stamps and travel legs touch no rate, bid,
  distance or routing record.

## 11. Rubric arithmetic

9 sites (ask A) + 9 sites × 2 (ask B) + 4 packages × 4 conditions (ask C) + the four committed centres, the projected cost and the
condition each slate package fails + 5 named chart parts + 3 files ≈ 63 criteria.

## 12. World-building constraints

* Slate: P1 = H1, H3, H5, H11; P2 = H2, H5, H9, H11; P3 = H2, H4, H6, H11. Costs under road-mile routing: P1 $10.9M, P2 $12.6M, P3
  $14.6M; answer $13.8M; the H9 off-slate package $13.2M; the straight-line package $13.5M on paper and $14.3M by road.
* H3: raw 12.1%, risk-adjusted 15.2%. H4: raw 15.0%, risk-adjusted 13.8%. H9: suppressed, bounded 15.1–15.8% by the region's totals.
* Exactly one package of the 793 meets all four conditions. H9 and H12 match on every published and bid column. The river towns' road
  route to H2 runs to the only bridge, so road routing sends them to H6, the dearest eligible centre, which then clears the volume floor
  by 11 episodes; by straight line it falls 24 short.
* Last year a slate package qualified, and the close-out reproduces to the dollar under road-mile routing.
* Telehealth stamps and travel legs are independent of every main-call record.
