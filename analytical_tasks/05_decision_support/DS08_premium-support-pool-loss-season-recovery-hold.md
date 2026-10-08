# DS08 — How to split the cooperative's crop-coverage support pool, when every past round was measured coming out of a loss season

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · agricultural credit and risk finance |
| Mirrors | Allocating a mitigation budget on a record of past interventions that were always triggered by a bad period (Google and Meta reliability investments credited with recoveries that would have happened anyway, Amazon seller-relief offered after disruptions, cloud service credits granted after outages) |
| Decision shape | An allocation under a cap, answered by a hold: the $2.4M pool across five county groups, or held to next season |
| Committed call | The dollars to each county group, or that the pool is held; and the covenant breaches avoided per $100,000 that the call rests on, to one decimal |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · hold forced by a computed blocking quantity (Part 6.4), with an implicit entity join (#18) at rung 2 |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution |
| Measured traps engaged | #18 joins only on the visible key · #4 never tests its reading against the control · #7 uses the ready-made measure · #26 picks a window across a documented confounder |
| Calibration form | Change-log natural experiments: the cooperative's record of eight past support rounds, each with its supported and unsupported members' covenant outcomes before and after |
| Driving force | The board funds support only where the cooperative's own record shows, at 90% confidence, at least one covenant breach avoided per $100,000. Every past round looks like a success, because support was only ever offered after a county loss season, so each round's before and after compares a disaster season with an ordinary one. Against the same group's unsupported members in the same season, the record shows 0.54 per $100,000 with a lower bound of −0.24, and no county group's lower bound reaches 1.0. |

## 1. Situation

A farm-credit cooperative has $2.4M to help member farms buy up their crop-revenue coverage from 70% to 80% this season. It can spread the
money across five county groups, each capped at its members' buy-up premium, or hold it to next season. The board's policy funds support
only where the cooperative's own record shows, at the 90% level, at least one covenant breach avoided per $100,000. The change log records
eight past rounds. Each has its support paid, its supported members, and covenant outcomes for supported and unsupported members of the
group in the seasons before and after. The credit committee chair is sure the support has paid for itself every time.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. Breaches really did fall after every round, and the
  insurer's loss-cost data, the entity-ownership table and the change log are all right. The difficulty is that the policy asks what the
  support caused, and the obvious comparison measures recovery from a loss season.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the chair's belief. Before-and-after effects from the change log still clear the bar at 2.61 per $100,000,
  lower bound 2.11, and the pool still goes to Bottoms, Ridge and Lakes.
* **Instrument repair.** The one field open to doubt is the change log's payee, which for 31% of supported members is their farming
  company. Recording the member beside the company moves rung 1 to rung 2's Bottoms, Ridge and Lakes and leaves rung 0 (indemnity, no join)
  at Prairie, Bottoms and Ridge; no lower rung holds. The loss-cost series, the ownership table and the outcomes are complete, and the
  same-season comparison is still needed for the hold.
* **Lens swap.** The naive read compares supported members with themselves a season earlier. The answer compares them with unsupported
  members of the same group in the same season: a different comparison population at a different moment.

## 3. The driving force

A strong solver sets aside the insurer's expected-indemnity ratios because the policy counts breaches, measures each group's breaches avoided
from the change log, and follows the entity-ownership table so that support paid to members' farming companies is attributed to them.
Each step is competent, and every group clears the bar. But the cooperative has only ever opened a round after a disaster. Joined to the
county loss-cost series, the season before support was a loss season in seven of eight rounds, so breaches would have fallen anyway. Each
round also left some members of the group unsupported, and their breaches fell almost as far. Measured against them, the rounds' effects
run from −0.9 to 2.6 per $100,000. The pooled effect is 0.54, its 90% interval runs from −0.24 to 1.33, and Bottoms, the best group, has a
lower bound of −0.22 on two rounds. Nothing clears the bar, so the pool is held.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Expected extra indemnity per support dollar from the insurer's county loss costs, filled by ratio to the caps | Prairie $1.2M, Bottoms $0.8M, Ridge $0.4M | The actuarial value of the buy-up, cleanly computed | The board policy: support is judged on covenant breaches avoided, not on indemnity |
| 1 | Before-and-after breaches avoided per $100,000 by group from the change log, payments joined to members by member ID | Ridge $1.0M, Lakes $0.9M, Bottoms $0.5M | The cooperative's own outcomes, all above the bar | The entity-ownership table: 31% of supported members held their cover through a farming company and were paid through it |
| 2 | Before-and-after with payments followed through the entity chain (#18) | Bottoms $0.8M, Ridge $1.0M, Lakes $0.6M | Complete attribution, pooled lower bound 2.11 against a bar of 1.0 | The county loss-cost series: the before season was a loss season in seven of eight rounds |
| 3 | **Decisive:** each round against the same group's unsupported members in the same season; pooled and by group, at the policy's 90% standard | **Hold the pool: no group's lower bound reaches 1.0 (Bottoms 1.35, lower bound −0.22)** | — | — |

* **Position table.** Rung leaders are Prairie (indemnity ratio 1.45 against 1.30), Ridge (3.6 against 2.9) and Bottoms (3.2, with Lakes
  the marginal group at 2.4 against Prairie's 1.7, 1.41×). On rung 3 Bottoms still has the highest point estimate, so the hold refuses the
  leader rather than breaking a tie.
* **Blocking quantity.** Pooled same-season effect 0.54 per $100,000, 90% interval −0.24 to 1.33. By group: Prairie −0.05, Ridge 0.85,
  Bottoms 1.35, Lakes 0.02, with one-sided lower bounds of −1.62 to −0.22. Uplands has no rounds and so no evidence.
* **Falsifiability.** Bottoms would have been funded had its two rounds averaged 2.58 per $100,000 at the record's spread, 1.9× what they
  show. A record of the same spread needs a pooled mean of 1.79 for its lower bound to reach 1.0.
* **Partial correction priced (L3).** Seeing the loss seasons but dropping their rounds, instead of comparing within season, leaves one
  round (Lakes, 2.6) and funds Lakes $0.9M. The half-insight lands on a pick, further from the answer than rung 2's. Same-season comparisons
  with the member-ID join drop the company-held farms from the supported group, because their covenant outcomes sit under the company's
  borrower ID, and those farms improved least; Bottoms' effect rises to 2.85 per $100,000 with a lower bound of 1.28, and the pool funds
  Bottoms $0.8M. No half-insight holds.
* **Grid.** Measure (indemnity, breaches) × join (member ID, entity chain) × comparison (before-and-after, same season) gives 5 feasible
  cells, since indemnity uses no join. The three before-and-after and indemnity cells allocate to different groups, the member-ID
  same-season cell funds Bottoms (above), and only the entity-chain same-season cell holds. The nearest pick is that member-ID cell
  (Bottoms, lower bound 1.28 against the bar of 1.0), one omission away: the entity chain.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The change log lists rounds and outcomes. No document says rounds followed loss seasons, or names the unsupported
   members as a comparison.
2. **No sweepable corpus nominates a pick.** *In seven of the eight rounds the season before support was a county loss season, because the
   cooperative has only ever opened a round after a disaster.* Every before-and-after in the record therefore measures recovery, and the
   record can show support's effect only against same-season unsupported members.
3. **No arithmetic symptom.** Payments, members and breaches reconcile under every join and every comparison. Before-and-after is an exact
   difference of correct rates.
4. **Not a row predicate.** It needs each round joined to the county loss-cost series, a same-season difference-in-differences within each
   round, and a pooled and per-group interval at the policy's standard.
5. **The enumeration is arithmetic.** Whether a group clears is a computed lower bound. No column marks a round as confounded.
6. **No cutover date.** Loss seasons recur across nine years in different counties, and no single date steps the record.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The change log: eight rounds (two each in Prairie, Ridge, Bottoms and Lakes; none in Uplands), with support paid, supported and
  unsupported members, and covenant outcomes before and after.
* **What it certifies.** The rounds' before-and-after declines, exactly as rung 2 computes them. Pooled 2.61 per $100,000 (sd 0.75 across
  rounds), so a solver who checks its rung against the record is confirmed.
* **What it holds that nothing invites.** The same-season comparison. Round effects: Ridge 2.6 and −0.9, Bottoms 0.9 and 1.8, Prairie 0.1
  and −0.2, Lakes 0.45 and −0.4; sd 1.18.
* **Twin pair.** Bottoms's first round and Lakes's first round are identical on every column a lookup sees: $310,000 paid, 64 supported
  members, before-season breach rate 9.4%, after-season 3.1%, so the same before-and-after effect of 2.6. Their same-season effects are 0.9
  and 0.45 (2.0×). Only the unsupported members' outcomes separate them.
* **Every rule exercised.** One round followed an ordinary season, which tests the loss-season join. In one group supported and unsupported
  members had different before-season rates, so the difference-in-differences differs there from a raw after-season gap.
* **Resemblance points at the decoy.** Bottoms's application profile matches the record's two largest before-and-after rounds.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board policy: support is funded only where the cooperative's record shows, at the 90% level, at least one covenant
  breach avoided per $100,000, and otherwise the pool is held. The programme note: group caps equal members' buy-up premium. One sentence
  each.
* **Empirical pins.** The same-season round effects, from the change log. The entity chain, from the ownership table.
* **Voices.** The credit committee chair: "Support has paid for itself every time we've offered it." The Bottoms field officer: "Our members
  were hit hardest; they need it most." A board member: "Money sitting in a pool helps nobody."
* **Licensed wrong basis.** The policy records that the farm-credit regulator reviews member-support programmes on before-and-after covenant
  outcomes and will see that table.

## 8. Determinism by construction

* **Comparison set.** Each round's unsupported members are the group's other members with operating loans tested on the same covenant date,
  listed in the change log.
* **Difference-in-differences.** Supported and unsupported members had the same before-season breach rates in seven rounds, so the DiD and
  the after-season gap agree there. The eighth tests the difference.
* **Interval.** The policy fixes 90%. Every lower bound sits at least 1.2 below the bar, so t or normal critical values, and pooled or
  per-group spread, return the same hold.
* **Maturity.** Every covenant outcome is from a closed test date.

## 9. Prompt sketch and deliverables

> We have $2.4M to help members buy up their crop coverage this season, to be split across the five county groups or held over to next
> year. Our credit committee chair is sure this support has paid for itself before. Tell me how the pool should be split, or that it
> should be held, in one sentence for the board, with the breaches avoided per $100,000 you are relying on, to one decimal. Send
> `support_case.xlsx`, a chart `round_effects.png`, and a one-page `pool_decision.pdf`.

* `support_case.xlsx` — the allocation under each construction, the leverage sheet (ask A), the insured-acres sheet (ask B) and the rounds
  sheet (ask C).
* `round_effects.png` — the eight rounds as paired points (before-and-after, same season) with the bar as a labelled reference line at 1.0,
  the pooled same-season interval as a band, and the loss seasons marked on the before side.
* `pool_decision.pdf` — the hold, the blocking quantity, and what would have funded Bottoms.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each county group, the members' mean debt-to-asset ratio at last year's annual reviews.
  *Device:* a member with several loans has one review per relationship but a row per loan, grouped in the relationship table. Averaging by
  loan row overweights multi-loan members and lifts two groups by four to six points.
* **Ask B (device-carried).** For each group and each of the last six seasons, acres insured at 80% coverage or above. *Device:* enterprise
  units span several farms and appear once per basic unit with a unit-structure code. Summing basic-unit rows double-counts 14–22% of acres
  in three groups.
* **Ask C (validity).** Each round's effect under before-and-after and same-season comparisons, the pooled interval, and each group's lower
  bound.
* **Decoupling.** Clearing the same-season comparison changes no figure in asks A or B. Reviews and insured acres never enter a round's
  effect.

## 11. Rubric arithmetic

5 groups (ask A) + 5 × 6 seasons (ask B) + 8 × 2 round effects + the pooled interval + 4 group lower bounds (ask C) + the hold, the
blocking quantity, the bar and the falsifying mean + 5 named chart parts + 3 files ≈ 68 criteria.

## 12. World-building constraints

* Caps: Prairie $1.2M, Ridge $1.0M, Bottoms $0.8M, Lakes $0.9M, Uplands $0.6M. Indemnity ratios: 1.45 / 1.10 / 1.30 / 0.85 / 0.80.
* Before-and-after by group, member-ID join: Ridge 3.6, Lakes 2.9, Bottoms 2.2, Prairie 0.8. With the entity chain: Bottoms 3.2, Ridge 3.15,
  Lakes 2.4, Prairie 1.7. Same-season round effects as listed; pooled 0.54 (−0.24 to 1.33).
* Seven of eight before seasons are county loss seasons in the loss-cost series. 31% of supported members are paid through an entity.
* The twin rounds are identical on every visible column.
* Loan reviews and unit structures never touch payments, members or covenant outcomes.
