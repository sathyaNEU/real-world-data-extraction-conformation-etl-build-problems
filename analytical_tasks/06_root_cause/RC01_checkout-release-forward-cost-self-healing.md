# RC01 — The checkout release did cause the conversion drop. What will it cost next quarter if it stays?

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Product Analytics · e-commerce checkout and conversion |
| Mirrors | Release-regression triage at consumer platforms (Meta and Instagram Shopping checkout, Google Play billing flows, Apple account sign-in changes), where the cause is right and the decision turns on its forward cost |
| Decision shape | One figure committed at a date: the release's attributable lost orders per week over the next quarter |
| Committed call | Lost orders per week attributable to the address-validation release over the next 13 weeks if it is not rolled back |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · Pattern A (past exceedance against forward yield), with the driver behind a join (Pattern C) |
| Gate G mechanism | decomposition_attribution, with confirm_surface_read support |
| Measured traps engaged | #18 joins only on the visible key · #13 validates on one population, applies to another · #11 beats the headline trap, misses the quiet one |
| Calibration form | Change-log natural experiments: two prior flagged releases with their measured effects |
| Driving force | The release only hurts accounts whose saved address fails the new validation, a property of the address book two joins away from a session. Every affected account re-saves its address after one failed checkout. The pool of accounts still to be hit is draining, so the past effect, measured correctly, overstates every future week. |

## 1. Situation

An online merchandise store's conversion rate fell 0.7 points over four weeks. The product team traced it to a release that added address
validation at checkout and wants a sprint to roll it back. A marketing partnership began sending referral traffic in the same weeks. The
head of product will fund the rollback only if the release's forward cost exceeds that of the referral-quality fix the growth team is asking
for. The release went out behind a feature flag in account cohorts.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct, and the product team's claim is right: the release causes most of the drop so far. Nothing is
  overturned. The difficulty is the size of a forward cost the past drop does not measure.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the team's claim and the growth team's request. The flag log and session data still lead a competent solver to a
  correct past effect, projected forward as a constant.
* **Instrument repair.** Perfect session tracking changes nothing, because the past effect is already measured exactly. The forward pool is
  the issue.
* **Lens swap.** The answer is about accounts not yet hit, over weeks that have not happened: a different population at a different time.

## 3. The driving force

A strong solver removes the referral mix, uses the flag cohorts as a natural experiment, balances on account age, and gets the release's
effect right for the past four weeks. Then it multiplies forward. That carries a hidden assumption: that the exposed population next quarter
looks like the exposed population last month. It does not. The validation rejects one class of legacy-format saved addresses. That property
lives in the address book, reached as session → account → saved address. After one failed checkout an account re-saves its address and
never fails again. The address book's change timestamps show the pool of not-yet-failed legacy accounts draining week by week. The forward
cost is the expected first failures among the accounts still in the pool over the next 13 weeks.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Overall before-and-after drop × forward sessions, all of it the release | +118% above the answer | The team's diagnosis, quantified simply | Referral sessions convert far lower, and their share rose over the same weeks |
| 1 | Channel-mix standardised before-and-after drop, projected forward | +41% | Mix is removed; the textbook root-cause correction | The flag log shows exposure did not begin on one date; cohort timing matters |
| 2 | Flag-cohort exposure effect, balanced within channel × account age, projected forward as a constant weekly loss | +24% | A clean natural experiment, correctly balanced; it reproduces both prior releases' measured effects | Address-book timestamps show affected accounts re-saving their address after one failure, so the exposed pool is draining |
| 3 | **Decisive:** expected first failures over 13 weeks among accounts still holding a failing address, at the measured per-attempt effect | **The answer** | — | — |

* **Figure shape.** Every correction walks the figure down. The answer is the minimum cell of the grid, so every partial application
  overstates the forward cost.
* **Partial correction priced (L3).** A solver who models the drain from the aggregate weekly effect, not per account, fits an exponential
  decay to four noisy weeks and lands 31% above the answer. That is further away than rung 2.
* **Grid.** Mix (on/off) × exposure grain (date or cohort) × balance (on/off) × forward pool (constant or draining) = 16 cells. The nearest
  non-answer cell is 19% away and needs a draining pool without balancing, which the prior releases refute.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The release note describes the validation. No document says which saved addresses fail or that accounts self-repair.
2. **Corpus blind for a computable reason.** *Both prior flagged releases changed screens that touch no saved customer state, so no affected
   account could change its exposure.* A constant-effect projection reproduces both releases' measured follow-on weeks exactly.
3. **No arithmetic symptom.** Sessions, orders, cohorts and accounts reconcile on every rung.
4. **Not a row predicate.** It needs a two-hop join to the address book, a classification of address format from the validator's published
   rule set, and a within-account ordering of failure and re-save.
5. **The enumeration is arithmetic.** The remaining pool is computed per week; no column says "affected".
6. **No cutover date.** Exposure was staggered across cohorts, so no aggregate series steps on any date.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The change log's two prior flagged releases, each with cohort exposure dates and its measured effect over eight follow-on weeks.
* **What it certifies.** The cohort exposure method (rung 2). Both releases' effects reproduce exactly under cohort exposure with balance and
  miss by 30% or more under date-based or unbalanced comparisons.
* **What it is blind to.** Self-repair (above).
* **Twin pair.** Cohorts 7 and 9 are identical on exposure week, channel mix, device mix and account-age distribution, and their conversion
  drops differ 2.3×. Cohort 7 holds 2.4× more legacy-format saved addresses.
* **Resemblance points at the decoy.** The current release's first four weeks resemble prior release B's first four weeks, a release whose
  effect held flat.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The head of product's sprint rule: compare the forward 13-week cost of each candidate fix in lost orders per week. The
  validator vendor's rule set (shipped as its published specification) defines which address formats fail.
* **Empirical pins.** The per-attempt failure effect comes from the cohort comparison. Re-save behaviour comes from address-book timestamps
  (every failing account re-saves within two days of its failure).
* **Voices.** The product lead: "It broke checkout; every week we wait costs the same orders." The growth lead: "Referral traffic was always
  going to convert lower; that's not a bug."
* **Licensed wrong basis.** The sprint rule records that the platform review board sizes regressions as the measured weekly loss carried
  forward and will review the case on that basis.

## 8. Determinism by construction

* **Re-save lag.** Every failing account re-saves within two days and none checks out in between, so lag conventions converge.
* **Pool definition.** "Accounts holding a failing format and active in the last 180 days" or "in the last 365 days" give the same pool,
  because no account lapses between the two windows in the extract.
* **Forward sessions.** Forward session volume is pinned by the growth team's filed traffic plan, and the referral campaign's end date is in
  the partnership contract. Both convert the same way under every rung.
* **Rounding.** The committed weekly figure sits mid-bin at whole orders.

## 9. Prompt sketch and deliverables

> I'll fund one sprint next quarter: roll back the address check, or the growth team's referral filter. Product is sure the release broke
> checkout. Tell me how many orders a week, on average over the next 13 weeks, the release will cost us if it stays, as one figure. Send
> `regression_case.xlsx`, a chart `forward_cost.png`, and a one-page `sprint_decision.pdf`.

* `regression_case.xlsx` — the forward-cost build, the cohort table (ask A) and the payment sheet (ask B).
* `forward_cost.png` — weekly lost orders: four observed weeks and 13 forward weeks under the constant and draining bases, with the referral
  fix's weekly cost as a reference line.
* `sprint_decision.pdf` — the committed weekly figure and the sprint decision it implies.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 flag cohorts, sessions, orders and conversion in the four exposed weeks.
  *Device:* the session table carries bot sessions marked by the edge's bot-score field, which the analytics guide says are excluded.
  Leaving them in depresses conversion in three cohorts.
* **Ask B (device-carried).** Weekly payment-authorisation failures by card network. *Device:* retried authorisations post as new attempts
  with a retry flag. Counting attempts rather than orders overstates failures by a quarter.
* **Ask C (validity).** The forward weekly cost under each of the four rung bases.
* **Decoupling.** Clearing the address-book join changes no figure in asks A or B.

## 11. Rubric arithmetic

12 cohorts × 3 figures (ask A) + 4 weeks × 4 networks (ask B) + 4 bases (ask C) + the committed figure, the remaining pool and the referral
comparison + 5 named chart parts + 3 files ≈ 70 criteria.

## 12. World-building constraints

* 18% of active accounts held a failing format at release. After four weeks 61% of them have failed once and re-saved, and the rest drain at
  the rate their checkout frequency implies.
* The two prior releases touched no saved state, and their effects held flat for eight weeks.
* Rung figures are +118% / +41% / +24% / answer, and every other cell of the 16-cell grid sits at least 19% from the answer.
* Cohorts 7 and 9 are identical on every session-side column.
* Bot sessions and authorisation retries never touch the address-book population.
