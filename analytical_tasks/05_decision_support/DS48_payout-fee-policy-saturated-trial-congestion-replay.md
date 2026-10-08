# DS48 — Which fee policy settles next quarter's stablecoin payouts, when every policy in the trial got 99% of payouts in on time

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · payment settlement costs |
| Mirrors | Choosing a bidding policy for priority in a congested queue from a trial run in quiet conditions (priority-fee policies at payment firms on public chains, bid strategies for ad slots and API priority tiers, spot-capacity bids at cloud providers), where every candidate passes the trial and only the stressed conditions separate them |
| Decision shape | Which of N gets one scarce thing: the single fee policy the payout engine runs next quarter, among five trialled |
| Committed call | The policy adopted, and its expected fee per payout next quarter, in cents |
| Gap · Pattern | Gap 4 (rule) over Gap 1 (time) · E21, a saturated tie (in a calm trial month every policy includes 99.4% or more within two blocks, and the memo's tie-break, the cheapest, picks P5; the SLA's every-regime clause breaks the tie through a replay against a year of clearing levels), with the quiet second trap (E15) at rung 1 |
| Gate G mechanism | method_or_model_selection, with forecasting |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another |
| Calibration form | Parallel-run overlap: the four-week trial, in which the payout engine computed all five policies' bids for every payout in shadow and sent only the assigned one, alongside the chain's block data |
| Driving force | A fee policy is judged on whether payouts get in when blocks are full, and the trial month barely had full blocks: every policy included 99.4% or more within two blocks, so the treasury memo's tie-break, the cheapest, decides. The memo's SLA must hold in every congestion regime of the past year. Replaying each policy's shadow-validated bid rule against a year of per-block clearing levels leaves one policy above 95% in congested blocks, and it is the most expensive in the trial. |

## 1. Situation

A payments company settles stablecoin payouts on a public chain whose blocks carry a base fee and a priority tip. It trialled five fee
policies (P1–P5) for four weeks on randomly assigned payouts, and next quarter's 600,000 payouts will run on one of them. The treasury memo
adopts the cheapest policy that includes at least 95% of payouts within two blocks of first broadcast; if none qualifies, the incumbent P1
stays. The trial dashboard reports each policy's median fee paid. The engineering lead considers the trial's cheapest policy the obvious
pick.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the payout ledger, the shadow-bid log, the assignment log, the block data and the dashboard's medians.
  No stakeholder read is overturned: every policy did include 99.4% or more within two blocks in the trial, and the cheap policies were
  cheap. The difficulty is that the trial month cannot show what each policy does when blocks are full.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and every voice. The trial's own inclusion rates still pass every policy, and the memo's
  tie-break still adopts P5.
* **Instrument repair.** Give the company a perfect record of every trial payout and broadcast. The trial's inclusion becomes exact and is
  still 99.4% or more for every policy, because the month was calm; no better record of the trial shows a congested block it did not have.
* **Lens swap.** The naive read and the answer differ in moment and condition: four calm weeks of live outcomes, against a year of blocks
  replayed under each policy's rule, regime by regime.

## 3. The driving force

A strong solver ignores the dashboard's median fee paid, which describes only payouts that got in at the price they got in at, measures
inclusion within two blocks of first broadcast for every assigned payout, and spots that the trial's random assignment broke for P2 in
week two. Every policy passes the SLA in the trial, at 99.4% or better, and the cheapest after reweighting is P5, the vendor's oracle. But
the trial month's blocks were full 0.6% of the time, and the memo's SLA must hold in every congestion regime the chain has had in the past
year, as the memo defines them by the previous block's gas-used ratio. The trial's shadow-bid log makes each policy's rule replayable:
replayed against the trial's own blocks, it reproduces every live outcome. Replayed against the past year's per-block clearing levels, it
gives each policy's inclusion in calm, normal and congested blocks. In congested blocks P5 includes 91.8%, P1 93.9%, P2 93.4% and P3 71.5%.
Only P4, which bids the regime's clearing level up front and bumps once, stays above 95%, at 97.6%.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The trial dashboard's median fee paid per payout; adopt the cheapest | P3, low start bids with bumping (30¢ against P2's 41¢) | The company's own trial, and the incumbent's own logic of reading paid fees | The treasury memo: a policy is eligible only at 95% of payouts within two blocks of first broadcast, and cost is the mean fee per payout |
| 1 | Inclusion within two blocks for every assigned payout (all five at 99.4% or more) and the mean fee as run; cheapest eligible | P2, the fee-history percentile (52¢ against P5's 66¢) | The SLA measured on every payout, survivorship gone | The assignment log: in week two a routing fault sent P2 no payouts between 13:00 and 21:00 UTC; reweighted to the trial's hour mix, P2's mean fee is 81¢ |
| 2 | The same with the assignment reweighted; every policy still eligible, so the memo's tie-break, the cheapest, decides | P5, the vendor's oracle (66¢ against P3's 79¢) | Clean measurement, a clean trial, and the memo's own rule | The memo's SLA: 95% must hold in every congestion regime of the past year, and the trial month's blocks were full 0.6% of the time |
| 3 | **Decisive:** each policy's rule, validated on the trial's shadow bids, replayed against the past year's per-block clearing levels, with inclusion within two blocks by regime; the cheapest policy at 95% in every regime | **P4, the regime clearing-level bid, 119¢ a payout** (5th of five on rung 0) | — | — |

* **Figure shape.** The answer is the extreme cell: every rung's pick is cheaper (30¢, 52¢, 66¢), and the decisive move lands on the dearest
  policy, at 119¢ under next quarter's regime mix.
* **Position table.** P4 is 5th of five on rung 0 (78¢), 5th on rung 1 (92¢) and 5th on rung 2; it is never second and leads only rung 3.
  Rung margins: P3 over P2 1.37×, P2 over P5 1.27×, P5 over P3 1.20×.
* **Discriminator dominance.** P5 carries a 1.39× cost advantage over P4 into rung 3 (66¢ against 92¢ in the trial). The decisive move is
  not a ratio but the SLA's gate: in congested blocks P5 misses 95% by 3.2 points and P4 clears it by 2.6, over 236,000 congested blocks
  each, so P5's eligible value is nil and no fee ratio can carry it back. The policy nearest the gate, P1, misses by 1.1 points.
* **Partial correction priced (L3).** No half-applied replay names P4. Pooling the year instead of testing each regime passes every
  policy (P3, the weakest, at 96.1%) and adopts P5 at 89¢. Replaying against the trial month's own blocks passes every policy and adopts
  P5 at 66¢. Replaying without the policies' bumps, or taking a block's clearing level as its median tip rather than its lowest, drops P4
  below 95% with the rest, so nothing qualifies and the incumbent P1 stays, at 106¢ (−11%).
* **Grid.** Fee measure (median paid, mean per payout) × assignment (as run, reweighted) × inclusion test (trial, pooled replay, replay by
  regime) = 12 cells. The trial and pooled cells name P3, P2 or P5. The replay by regime names P4 in each of its cells, because only P4
  qualifies and the replay depends on each rule rather than on who was assigned, and the replay's own fees give 119¢; the nearest other
  figure is the incumbent's 106¢.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo states the SLA and its regimes. The shadow-bid log stores bids. No document says the trial cannot test the
   SLA, or that the policies can be replayed against the chain's history.
2. **Corpus blind for a computable reason.** *The trial month's blocks were full 0.6% of the time, so in the trial every policy's first or
   bumped bid cleared almost every block, and its live inclusion is 99.4% or more whatever it would do in congestion.* It certifies the
   replay: each policy's rule replayed against the trial's blocks reproduces the inclusion block of 150,000 of 150,000 assigned payouts.
3. **No arithmetic symptom.** Ledger, broadcasts, shadow bids and blocks reconcile, and every policy's trial figures are plausible and
   inside the SLA.
4. **Not a row predicate.** Inclusion in the replay is a per-block comparison of a bid path, with bumps, against the lowest included tip in
   each of the next two blocks, over 2.6 million blocks, classed by the previous block's gas-used ratio.
5. **The enumeration is arithmetic.** No column holds a policy's congested-regime inclusion or a clearing level.
6. **No cutover date.** The year of blocks is a measurement population, and the decision rests on regimes that recur through it; nothing
   steps.
7. **Survives deletion.** No wrong number exists to delete. Without the dashboard or any voice, the trial still passes every policy.

## 6. The calibration corpus

* **Form.** The four-week trial: 150,000 payouts randomly assigned to the five policies, each with the five shadow bids the engine computed,
  the assigned policy's broadcasts and bumps, the settling block and fee, and the chain's blocks over the same weeks.
* **What it certifies.** The replay (above), exactly, and the reweighting of P2's week two from the assignment log.
* **What it is blind to.** Congestion (above).
* **Twin pair.** Two trial hours are identical on every dashboard column: 410 payouts, the same median fee paid, the same mean base fee and
  the same mean gas-used ratio. P3's payouts took a mean of 1.1 and 2.2 blocks to get in (2.0×): in the second hour eight consecutive full
  blocks lifted the clearing level above P3's first bids, which hourly averages smooth away. Only the per-block clearing level separates
  them.
* **Resemblance points at the decoy.** P5's vendor publishes a 99% inclusion figure from a quarter as calm as the trial.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The treasury memo: adopt the cheapest policy whose payouts are included within two blocks of first broadcast at least 95%
  of the time in every congestion regime of the past year (calm, normal and congested, by the previous block's gas-used ratio below 0.5,
  0.5 to 0.95, and above); cost is the mean fee per payout; if none qualifies, P1 stays. The trial design: random assignment, 20% each.
  The five policies' bid rules. The expected regime mix for next quarter is the past year's: 58%, 33% and 9% of blocks.
* **Empirical pins.** Each policy's rule, validated on the shadow bids; clearing levels per block, from the chain.
* **Voices.** The engineering lead: "The cheapest policy in the trial is the obvious pick." The vendor's account manager: "Our oracle gets
  99% in within two blocks." The treasury analyst: "The median fee paid is what the market charges."
* **Licensed wrong basis.** The memo records that the finance committee sees the trial dashboard's median fee per policy.

## 8. Determinism by construction

* **Clearing level.** The lowest effective tip among a block's included payments, excluding the builder's own payment transactions, which
  the block data marks; no policy's bid sits within 1% of a clearing level in more than 0.2% of replayed blocks.
* **Regimes.** The previous block's gas-used ratio, as the memo defines it; moving either boundary by 0.02 moves no policy across 95%.
* **Bumps.** Each rule's bump schedule is filed; the shadow log confirms it on every trial payout.
* **Rounding.** P4's expected fee is 118.85¢ (92¢ calm, 118¢ normal, 295¢ congested), clear of the half-cent edges.

## 9. Prompt sketch and deliverables

> We have to pick one of the five fee policies we trialled to run next quarter's stablecoin payouts, and treasury needs them in within
> two blocks. Our engineering lead thinks the cheapest policy in the trial is the obvious pick. Tell me which policy we adopt and what it
> will cost us per payout, in cents, as the line for the treasury memo. Send `fee_policy_choice.xlsx`, a chart `inclusion_by_regime.png`,
> and a one-page `treasury_memo.docx`.

* `fee_policy_choice.xlsx` — the five policies under each rung construction with the replay's reproduction count (ask C), the payout-value
  sheet (ask A) and the returns sheet (ask B).
* `inclusion_by_regime.png` — each policy's inclusion within two blocks in the trial and in calm, normal and congested blocks of the replay,
  as grouped bars, with the 95% line labelled and P5's congested-regime miss annotated.
* `treasury_memo.docx` — the policy adopted, its expected fee, and why the trial's cheapest policy is not eligible.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four trial weeks, the total value paid out in US dollars. *Device:* the ledger
  stores amounts in each token's base units, six decimal places for one stablecoin and eighteen for the other, as the token registry
  records. Summing raw amounts swamps every week with the second coin.
* **Ask B (device-carried).** For each of the twelve payout corridors, last month's returned payouts. *Device:* a return is recorded as a
  negative payout linked to the original, and a partial return as several, as the ledger guide documents. Counting negative rows as returns
  overstates the corridors where recipients' banks return in parts.
* **Ask C (validity).** For each policy, inclusion within two blocks in the trial and in each regime of the replay, its expected fee per
  payout next quarter, and the replay's reproduction count on the trial.
* **Decoupling.** Clearing the regime replay changes no figure in asks A or B. Token decimals and returns touch no bid, broadcast or block
  record.

## 11. Rubric arithmetic

4 weeks (ask A) + 12 corridors (ask B) + 5 policies × 4 inclusion figures + 5 fees + 1 reproduction count (ask C) + the policy, its fee,
the binding regime and its margin to 95% + 5 named chart parts + 3 files ≈ 54 criteria.

## 12. World-building constraints

* Trial inclusion within two blocks: P1 99.9%, P2 99.6%, P3 99.8%, P4 99.4%, P5 99.9%. Median fee paid: P3 30¢, P2 41¢, P5 52¢, P1 69¢,
  P4 78¢. Mean fee as run: P2 52¢, P5 66¢, P3 79¢, P1 84¢, P4 92¢; P2 reweighted 81¢.
* Replay, inclusion in calm / normal / congested blocks: P1 100 / 98.9 / 93.9; P2 100 / 98.2 / 93.4; P3 100 / 96.0 / 71.5; P4 99.8 / 99.1
  / 97.6; P5 100 / 98.5 / 91.8. Without bumps, or with median clearing levels, P4's congested figure falls below 95%.
* Expected fee next quarter (58% / 33% / 9% mix): P5 89¢, P2 98¢, P3 102¢, P1 106¢, P4 119¢. 236,000 congested blocks in the year.
* Token decimals and returns are independent of every main-call record.
