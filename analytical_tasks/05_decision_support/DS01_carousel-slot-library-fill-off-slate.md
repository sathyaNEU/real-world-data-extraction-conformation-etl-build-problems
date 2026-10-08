# DS01 — Which ranking policy gets the home carousel's one test slot, when each of the three proposals fails a different launch condition

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · recommendation and ranking experimentation |
| Mirrors | Allocating a scarce online-experiment slot among ranking candidates scored offline from logged feedback (Amazon and Meta feed-ranking launches, YouTube and Google Play home-surface recommenders, marketplace search re-rankers), where the launch gate carries guardrails as well as a lift bar |
| Decision shape | Which of N gets one scarce thing: the carousel's single A/B slot for next quarter |
| Committed call | The registered policy that takes the slot, and its expected offline lift in orders per 1,000 sessions |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · measured #9's architecture (the admissible option sits off the slate), with Pattern B for the estimator the archive pins and a fine-segment guardrail (#14) at rung 1 |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #9 picks from the offered options when none passes · #14 coarsens the segment it was asked about · #1 reports a failed back-test, ships anyway · #10 notes a binding limit as a risk |
| Calibration form | Published control set with a reproduction clause: nine archived carousel tests, each with its pre-test offline estimate and its realised order lift |
| Driving force | Each proposal clears the launch gate on the numbers everyone starts from. Read at the charter's eight audience cells, and with the only estimator that reproduces all nine archived tests (one importance weight per session, because the logger drew one ranking per session, and orders attributed through the cart-source join), each proposal fails a different condition. The slot procedure then fills the slot from the policy library, and the one library policy that clears all three conditions has to be scored from its registered spec on current logs. It is fourth on the replay estimate. |

## 1. Situation

A fashion marketplace runs one A/B test at a time on its home carousel, and next quarter's slot is open. Three teams have proposed
policies: a two-tower personaliser (A), a trending-boost ranker (B) and a session-sequence model (C). The experimentation charter sets three
launch conditions for any policy taking a slot. A separate test-calendar procedure says what happens when no proposal qualifies. The policy
library holds three earlier registered policies (D, E, F), each filed as a scoring spec. Three months of logged carousel sessions carry the
logging policy's propensities. The personalisation lead believes the two-tower model has earned the slot.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The dashboard's coarse guardrails, the replay
  estimates, the archive's published estimates and realised lifts and the library's registration estimates are all correct for what they
  measure. The difficulty is that the admissible set is wider than the slate, and the slate fails only under constructions the archive and
  the charter force.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the lead's belief, the dashboard and the library's registration estimates. The replay estimate on the logs still
  ranks A first among the proposals, and nothing on the slate looks inadmissible.
* **Instrument repair.** Give the logger unlimited traffic and perfect attribution. A still loses 3.1% of orders in the app new-shopper cell,
  B's reproduced lift is still negative, C still gives fresh listings 5.4% of top-three impressions, and E is still the only policy clearing
  all three. Narrower intervals change no pass or fail.
* **Lens swap.** The naive read ranks the three proposals by replay lift. The answer is a policy nobody proposed, scored on a weighting of
  sessions that the replay estimate never forms: a different candidate population, not the proposals under another lens.

## 3. The driving force

A strong solver estimates each proposal's lift from the logs, checks the guardrails and picks the best qualifying proposal. Each step is
competent, and A qualifies. Three facts break that. First, the charter's guardrail is defined on eight audience cells (platform × tenure
band), and A's gain among returning web shoppers hides a 3.1% loss among app shoppers in their first 30 days. Second, the logger drew one
ranking per session and replayed it on every render. A per-request weight counts long sessions many times, and only one weight per
session, with orders reached through the order table's cart-source field, reproduces all nine archived tests. Under it B's lift is
negative. Third, C misses the seller commitment on fresh listings outright. With no proposal qualifying, the test-calendar procedure fills
the slot from the library under the same conditions. A library policy has no exported rankings; the solver must apply each registered spec
to every logged session before any condition can be tested. Only E clears all three.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Replay estimate of order lift for the proposals; guardrails read from the dashboard's new-versus-returning view; fresh-listing floor | A, two-tower personaliser | The natural offline evaluation, and A leads by 1.24× with every condition apparently met | The charter defines guardrail cells as platform × tenure band, and A loses 3.1% in the app under-30-day cell |
| 1 | Guardrails at the charter's eight cells (#14), replay estimate kept | B, trending-boost | A careful guardrail check that removes the obvious leader | The archive: replay reproduces 3 of 9 tests and the reproduction clause bars it; the estimator that reproduces all nine puts B at −0.3 |
| 2 | Session-grain estimator that reproduces the archive; no proposal clears all three conditions, so take the least-bad proposal and carry its fresh-listing shortfall as a risk (#10) | C, session-sequence model | Every number is now reproducible, and C has the largest reproduced lift on the slate | The test-calendar procedure: a slot no proposal qualifies for is filled from the library under the same conditions, never left empty, never given to the incumbent |
| 3 | **Decisive:** score every library spec on the current logs, apply the session-grain estimator, the eight cells and the floor to all six registered policies | **E, sequence ranker with fresh-listing interleave** (4th of the five admissible policies on rung 0) | — | — |

* **Position table.** E is 4th of the five policies admissible on rung 0 (A 4.2, B 3.4, D 2.2, E 1.9, F 1.5 orders per 1,000 sessions on
  replay; C fails the floor). It is 2nd on rung 1, 1.79× behind B. Rung 2 ranks proposals only, so E is not on its list. It leads only rung
  3, as the sole policy clearing all three conditions. Rung margins: A over B 1.24×, B over E 1.79×, C over A 1.26×.
* **Discriminator dominance.** C carries a 1.61× reproduced-lift advantage into rung 3 (2.9 against 1.8). On the fresh-listing floor E stands
  at 2.63× C's share (14.2% against 5.4%, floor 12%). Product: 0.62 × 2.63 = 1.63, clear of the 1.56 headroom bar (1.3 × 1.2), so no
  exposure convention rescues C, and C would need 2.22× its own share to qualify.
* **Partial correction priced (L3).** A solver who reaches rung 2 and turns to the library but takes each entry's filed registration
  estimate for condition 1 names F (2.4 at registration against E's 1.6). F's reproduced lift on current logs is −0.4, so the half-insight
  lands on a policy with negative lift, further from the answer than C.
* **Grid.** Guardrail grain (coarse, fine) × estimator (replay, request-grain weights, session-grain weights) × scope (proposals, registry)
  gives 12 cells. Coarse cells name A under every estimator and scope (A's lead never falls below 1.28×). Fine cells with replay or
  request-grain weights name B (B over E at least 1.25×). Fine cells with session-grain weights name C on the proposals and E on the
  registry. The nearest wrong cell is the fine-cell, session-grain, proposals-only cell (C), and reaching it costs one omission: never
  opening the test-calendar procedure.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter states three conditions. The procedure says how an empty-handed slot is filled. No document says the
   proposals fail, which cells bind, what the weighting unit is, or that any library policy qualifies.
2. **No sweepable corpus nominates it.** *In every archived cycle at least one proposal cleared all three conditions, because the
   library-fill clause has never been exercised, so the archive holds nine proposal fills and no library fill.* It pins the estimator at
   rung 2: session-grain weights reproduce 9 of 9 tests within ±0.25, and the best rival (request-grain weights) reproduces 6 of 9. It is
   silent on which library policy qualifies.
3. **No arithmetic symptom.** Impressions, sessions, orders and cart-source links reconcile under every estimator. Replay is a correct
   matched-impression average, and nothing fails a check.
4. **Not a row predicate.** It needs a per-session weight (a group construction), a join from orders to impressions through the cart-source
   field, per-cell order totals under each policy, and each library spec applied to every logged session.
5. **The enumeration is arithmetic.** Which registered policy qualifies is computed from rankings the solver generates. No column flags a
   policy as admissible.
6. **No cutover date.** The logging policy and the conditions are unchanged across the window, and no series steps.
7. **Survives deletion.** No wrong number exists to delete, and without any voice the slate still reads as the whole choice set.

## 6. The calibration corpus

* **Form.** Nine archived tests (T1–T9): each tested policy's spec, its logging window, the offline estimate published before the test and
  the realised online order lift with its interval. The charter's reproduction clause makes an estimator citable against condition 1 only
  if it returns every archived realised lift within ±0.25 orders per 1,000 sessions.
* **What it pins.** Session-grain self-normalised weights with cart-source attribution reproduce 9 of 9. Request-grain weights reproduce 6
  of 9 and replay 3 of 9. Both rivals overstate every miss, so they fail on the archive total too: request-grain by 16%, replay by 41%.
* **What it is blind to.** The library route (above): no archived slot was filled from the library.
* **Twin pair.** T3 and T7 are identical on every archive column: sequence-model family, all cells in scope, 10% traffic, 28 days, replay
  estimate +2.6, same logger version. Their realised lifts are +2.4 and +1.1 (2.2× apart). T7 ran in the gift season, when sessions averaged
  6.8 carousel renders against 1.9, so request-grain weights count its sessions several times over. Only session-grain weights reproduce
  both.
* **Every rule exercised.** One archived test changed only the web cells, so a guardrail read at platform grain is tested. One test's
  orders arrived mostly through the saved-for-later list, so cart-source attribution (not same-session matching) is tested.
* **Resemblance points at the decoy.** The archive's three largest realised lifts were two-tower personalisers like A. E's family
  resembles T7, the low realised lift.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: a slot policy must clear the lift, guardrail and fresh-listing conditions. The charter's cell table: eight
  audience cells, platform × tenure band. The test-calendar procedure: a slot no proposal qualifies for is filled from the library under the
  same conditions, and is never left empty or given to the incumbent. One sentence each, in three places.
* **Empirical pins.** The weighting unit and the attribution route, from the archive.
* **Voices.** The personalisation lead: "The two-tower model has earned the slot; it wins every offline comparison we run." The merchandising
  lead: "The fresh-listing floor is a promise to sellers, not a ranking signal." The data-science manager: "Replay is what we have always
  shown the council."
* **Licensed wrong basis.** The charter records that the growth council reviews slot decisions on replay lift among the proposals and will
  see that table.

## 8. Determinism by construction

* **Session unit.** The log dictionary's session key is the logger's draw unit, so the session-grain weight needs no inactivity convention.
* **Interval convention.** The charter fixes a 90% one-sided bound. B and F fail on their point estimates (−0.3, −0.4) and E's bound is +0.6,
  so the delta method, a bootstrap at any seed, and 90% or 95% all return the same pass or fail for all six policies.
* **Guardrail and floor margins.** Failing cells sit at −3.1% (A) and −2.6% (D) against −1.5%. The worst passing cell is −1.2%. Fresh shares
  of qualifying policies are at least 12.9% against 12%.
* **Library scoring.** Specs are deterministic over logged features, with ties broken by item ID as the spec format states.
* **Maturity.** The logs end 21 days before extract, and cart-source attribution closes 14 days after a session, so no order is censored.

## 9. Prompt sketch and deliverables

> We get one A/B slot on the home carousel next quarter, and three teams have put policies forward. Our personalisation lead is sure the
> two-tower model has earned it. Tell me which policy takes the slot, in one sentence I can paste into the test calendar, with the lift you
> expect in orders per thousand sessions to one decimal. Send `carousel_slot.xlsx`, a chart `slot_conditions.png`, and a one-page
> `slot_decision.pdf`.

* `carousel_slot.xlsx` — every registered policy against the three conditions, the cell sheet (ask A), the seller sheet (ask B) and the
  estimator sheet (ask C).
* `slot_conditions.png` — three panels, one per condition, with the six registered policies as bars, proposals and library entries in two
  colours, each condition's threshold as a labelled reference line, and the chosen policy annotated.
* `slot_decision.pdf` — the committed policy and its lift, and the condition each proposal fails.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eight audience cells, last quarter's share of sessions reaching checkout and the
  median minutes from first carousel render to checkout. *Device:* the checkout service emits a second checkout event on every payment
  retry, carrying the original checkout ID and a retry counter, as the event dictionary documents. Counting events instead of checkout IDs
  inflates the share by 6–11% in the four app cells.
* **Ask B (device-carried).** For each of the 12 merchandise categories, the distinct sellers with at least one position-1 impression in the
  last 28 days. *Device:* storefront consolidations keep both seller IDs live for 90 days, linked in the seller-merge table. Counting raw IDs
  double-counts 140 sellers across five categories.
* **Ask C (validity).** The archive hit count (of 9) for each of the three estimators, and all six policies' lift under each estimator.
* **Decoupling.** Clearing the session-grain weighting, the eight-cell guardrail and the library fill changes no figure in asks A or B.
  Checkout events and seller IDs never enter the lift, guardrail or floor computations.

## 11. Rubric arithmetic

8 cells × 2 (ask A) + 12 categories (ask B) + 3 hit counts + 6 policies × 3 estimators (ask C) + the committed policy, its lift and the
condition each proposal fails + 6 named chart parts + 3 files ≈ 60 criteria.

## 12. World-building constraints

* Replay lifts: A 4.2, B 3.4, C 2.6, D 2.2, E 1.9, F 1.5. Session-grain lifts: A 2.3, B −0.3, C 2.9, D 1.4, E 1.8 (bound +0.6), F −0.4.
  Request-grain lifts keep every bound above zero.
* Worst fine cells: A −3.1% (app, under 30 days), D −2.6% (web, under 30 days), all others no worse than −1.2%. On the dashboard's coarse
  view every policy is no worse than −0.8%. Fresh shares: C 5.4%, E 14.2%, all others at least 12.9%.
* Library registration estimates: D 3.0, E 1.6, F 2.4.
* The archive: 9 tests, 9 of 9 under session-grain weights, 6 under request-grain and 3 under replay, with every rival miss overstating.
  T3 and T7 are identical on every archive column. Every archived cycle had a qualifying proposal.
* Rung leaders A, B, C, E. Checkout retries and seller merges never touch sessions, rankings, propensities or orders.
