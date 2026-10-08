# DS48 — Which fee policy settles next quarter's stablecoin payouts, when every policy in the trial got 99% of the overnight batch in on time

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · payment settlement costs |
| Mirrors | Choosing a bidding policy for priority in a congested queue from a trial run in quiet conditions (priority-fee policies at payment firms on public chains, bid strategies for ad slots and API priority tiers, spot-capacity bids at cloud providers), where every candidate passes the trial and only the conditions the new traffic will meet separate them |
| Decision shape | Which of N gets one scarce thing: the single fee policy the payout engine runs next quarter, among five trialled |
| Committed call | The policy adopted, and its expected fee per payout next quarter, in cents |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · E21, a saturated tie (every policy includes 99.4% or more of the overnight batch within two blocks, in the trial and in a year of payouts, so the memo's tie-break, the cheapest, picks P5; the memo's SLA counts next quarter's payouts, sent on demand at the marketplace's request hours, and a replay against a year of clearing levels at those hours breaks the tie), with the quiet second trap (E15) at rung 1 |
| Gate G mechanism | method_or_model_selection, with forecasting |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another |
| Calibration form | Parallel-run overlap: the four-week trial, in which the payout engine computed all five policies' bids for every payout in shadow and sent only the assigned one, alongside the chain's block data |
| Driving force | A fee policy is judged on whether payouts get in when blocks are full. The company pays out in an overnight batch, when blocks are almost never full, so in the trial and in a year of payouts every policy included 99.4% or more within two blocks, and the treasury memo's tie-break, the cheapest, decides. Next quarter a marketplace client takes payouts on demand, and its requests cluster in the afternoon hours when blocks fill. Replayed at those hours against a year of per-block clearing levels, one policy reaches 95%, and it is the dearest in the trial. |

## 1. Situation

A payments company settles stablecoin payouts on a public chain whose blocks carry a base fee and a priority tip. Every payout it has
made goes out in a batch at 02:00 UTC. It trialled five fee policies (P1–P5) for four weeks on randomly assigned payouts from that batch.
Next quarter a marketplace client brings 600,000 payouts, each sent within a minute of the recipient's request. The treasury memo adopts
the cheapest policy expected to include at least 95% of next quarter's payouts within two blocks of first broadcast; if none qualifies,
the incumbent P1 stays. The trial dashboard reports each policy's median fee paid, and the engineering lead considers the trial's cheapest
policy the obvious pick.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the payout ledger, the shadow-bid log, the assignment log, the block data, the marketplace's
  request log and the dashboard's medians. No stakeholder read is overturned: every policy did include 99.4% or more within two blocks in
  the trial, and the cheap policies were cheap. The difficulty is that next quarter's payouts go out at different hours.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and every voice. The trial's own inclusion rates still pass every policy, and the memo's
  tie-break still adopts P5.
* **Instrument repair.** Suspect file: the trial's assignment for P2, which in week two received none of the batch's second half, a
  routing fault the assignment log records. Repaired, rung 1 lands with rung 2 on P5, and rung 0 still names P3. No other file is
  suspect: the ledger holds a full year of payouts, all overnight, and the shadow log, block data and request log are complete. A
  year-long trial of the overnight batch would still show every policy at 99.4% or more; next quarter's on-demand payouts are a forward
  population built from the request log, so the replay at their hours is still needed.
* **Lens swap.** The naive read and the answer differ in population and moment: overnight batch payouts, measured live, against next
  quarter's on-demand payouts, replayed at the marketplace's request hours through a year of blocks.

## 3. The driving force

A strong solver ignores the dashboard's median fee paid, which describes only payouts that got in at the price they got in at, measures
inclusion within two blocks of first broadcast for every assigned payout, and spots that the trial's random assignment broke for P2 in
week two. Every policy passes the SLA in the trial, at 99.4% or better, and a year of overnight payouts says the same; the cheapest after
reweighting is P5, the vendor's oracle. But the memo's SLA counts next quarter's payouts, and those will not go out at 02:00: the
marketplace's request log puts 71% of its requests between 13:00 and 22:00 UTC, when the chain's blocks were full 22% of the time last
year, against 0.6% at 02:00. The trial's shadow-bid log makes each policy's rule replayable: replayed against the trial's own blocks, it
reproduces every live outcome. Replayed against the past year's per-block clearing levels at the marketplace's request times, it gives
each policy's inclusion for next quarter's payouts: P5 92.8%, P1 92.7%, P2 93.2%, P3 84.2%. Only P4, which bids the current clearing
level up front and bumps once, reaches 95%, at 98.8%.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The trial dashboard's median fee paid per payout; adopt the cheapest | P3, low start bids with bumping (30¢ against P2's 41¢) | The company's own trial, and the incumbent's own logic of reading paid fees | The treasury memo: a policy is eligible only at 95% of payouts within two blocks of first broadcast, and cost is the mean fee per payout |
| 1 | Inclusion within two blocks for every assigned payout (all five at 99.4% or more) and the mean fee as run; cheapest eligible | P2, the fee-history percentile (52¢ against P5's 66¢) | The SLA measured on every payout, survivorship gone | The assignment log: in week two a routing fault sent P2 none of the batch's second half, when its larger payouts go; reweighted to the batch's mix, P2's mean fee is 81¢ |
| 2 | The same with the assignment reweighted; every policy still eligible, so the memo's tie-break, the cheapest, decides | P5, the vendor's oracle (66¢ against P3's 79¢) | Clean measurement, a clean trial, a year of payouts agreeing, and the memo's own rule | The marketplace's request log: 71% of next quarter's payouts will be requested between 13:00 and 22:00 UTC, when last year's blocks were full 22% of the time, against 0.6% in the overnight batch |
| 3 | **Decisive:** each policy's rule, validated on the trial's shadow bids, replayed against the past year's per-block clearing levels at the marketplace's request times; the cheapest policy including 95% of next quarter's payouts | **P4, the clearing-level bid, 146¢ a payout** (5th of five on rung 0) | — | — |

* **Figure shape.** The answer is the extreme cell: every rung's pick is cheaper (30¢, 52¢, 66¢), and the decisive move lands on the dearest
  policy, at 146¢ for payouts sent at the marketplace's hours.
* **Position table.** P4 is 5th of five on rung 0 (78¢), 5th on rung 1 (92¢) and 5th on rung 2; it is never second and leads only rung 3.
  Rung margins: P3 over P2 1.37×, P2 over P5 1.27×, P5 over P3 1.20×.
* **Discriminator dominance.** P5 carries a 1.39× cost advantage over P4 into rung 3 (66¢ against 92¢ in the trial). The decisive move is
  not a ratio but the SLA's gate: for next quarter's payouts P5 includes 92.8%, 2.2 points under the line, and P4 98.8%, 3.8 over it, on
  a year of afternoon blocks, so P5's eligible value is nil and no fee ratio carries it back. The policy nearest the gate, P2, misses by
  1.8 points.
* **Partial correction priced (L3).** No half-applied replay names P4. Replaying at the year's block mix instead of the request times
  passes P1, P2, P4 and P5 (P5 at 96.3%) and adopts P5 at 87¢ (−40%). Replaying at the trial's own overnight blocks passes every policy and
  adopts P5 at 66¢. Replaying without the policies' bumps, or taking a block's clearing level as its median tip rather than its lowest,
  drops P4 to 94.1% with the rest, so nothing qualifies and the incumbent P1 stays, at 130¢ (−11%).
* **Grid.** Fee measure (median paid, mean per payout) × assignment (as run, reweighted) × inclusion test (trial, replay at the year's
  mix, replay at the request times) = 12 cells. The trial and year-mix cells name P3, P2 or P5. The replay at the request times names P4
  in each of its cells, because only P4 qualifies and the replay depends on each rule rather than on who was assigned; the replay's own
  fees give 146¢, and the nearest other figure is the incumbent's 130¢.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The memo states the SLA on next quarter's payouts, the request log stores request times, and the shadow-bid log
   stores bids. No document says the trial cannot test the SLA, or that the policies can be replayed against the chain's history at the
   marketplace's hours.
2. **Corpus blind for a computable reason.** *Every trial payout went out in the overnight batch, when blocks were full 0.6% of the time,
   so each policy's first or bumped bid cleared almost every block, and its live inclusion is 99.4% or more whatever it would do in the
   afternoon.* It certifies the replay: each policy's rule replayed against the trial's blocks reproduces the inclusion block of 150,000
   of 150,000 assigned payouts.
3. **No arithmetic symptom.** Ledger, broadcasts, shadow bids and blocks reconcile, and every policy's trial figures are plausible and
   inside the SLA.
4. **Not a row predicate.** Inclusion in the replay is a per-block comparison of a bid path, with bumps, against the lowest included tip in
   each of the next two blocks, at every request time in the marketplace's log mapped onto a year of blocks.
5. **The enumeration is arithmetic.** No column holds a policy's inclusion at an hour it never ran, or a block's clearing level.
6. **No cutover date.** The year of blocks is a measurement population and the request log a profile of hours; the decision rests on
   which blocks next quarter's payouts will meet, and no series steps.
7. **Survives deletion.** No wrong number exists to delete. Without the dashboard or any voice, the trial still passes every policy.

## 6. The calibration corpus

* **Form.** The four-week trial: 150,000 overnight payouts randomly assigned to the five policies, each with the five shadow bids the
  engine computed, the assigned policy's broadcasts and bumps, the settling block and fee, and the chain's blocks over the same weeks;
  beside it, the ledger's year of overnight payouts.
* **What it certifies.** The replay (above), exactly, and the reweighting of P2's week two from the assignment log.
* **What it is blind to.** Afternoon congestion (above).
* **Twin pair.** Two overnight batches are identical on every dashboard column: 410 payouts, the same median fee paid, the same mean base
  fee and the same mean gas-used ratio. P3's payouts took a mean of 1.1 and 2.2 blocks to get in (2.0×): during the second, a token launch
  filled eight consecutive blocks and lifted the clearing level above P3's first bids, which batch averages smooth away. Only the
  per-block clearing level separates them.
* **Resemblance points at the decoy.** P5's vendor publishes a 99% inclusion figure from clients who, like this company until now, pay
  out overnight.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The treasury memo: adopt the cheapest policy expected to include at least 95% of next quarter's payouts within two
  blocks of first broadcast; cost is the mean fee per payout; if none qualifies, P1 stays. The trial design: random assignment, 20% each.
  The five policies' bid rules. The marketplace contract: each payout sent within a minute of its request, 600,000 next quarter.
* **Empirical pins.** Each policy's rule, validated on the shadow bids; clearing levels per block, from the chain; request times, from
  the marketplace's six-month request log.
* **Voices.** The engineering lead: "The cheapest policy in the trial is the obvious pick." The vendor's account manager: "Our oracle gets
  99% in within two blocks." The treasury analyst: "The median fee paid is what the market charges."
* **Licensed wrong basis.** The memo records that the finance committee sees the trial dashboard's median fee per policy.

## 8. Determinism by construction

* **Clearing level.** The lowest effective tip among a block's included payments, excluding the builder's own payment transactions, which
  the block data marks; no policy's bid sits within 1% of a clearing level in more than 0.2% of replayed blocks.
* **Request times.** The request log's hour-of-week profile is laid over every week of the past year; using only the last three months of
  blocks moves no policy across 95%.
* **Bumps.** Each rule's bump schedule is filed; the shadow log confirms it on every trial payout.
* **Rounding.** P4's expected fee is 146.3¢ (92¢ in calm blocks, 118¢ in normal and 295¢ in full ones, met 41%, 37% and 22% of the time
  at the request hours), clear of the half-cent edges.

## 9. Prompt sketch and deliverables

> We have to pick one of the five fee policies we trialled to run next quarter's stablecoin payouts, and treasury needs them in within
> two blocks. Our engineering lead thinks the cheapest policy in the trial is the obvious pick. Tell me which policy we adopt and what it
> will cost us per payout, in cents, as the line for the treasury memo. Send `fee_policy_choice.xlsx`, a chart `inclusion_by_hour.png`,
> and a one-page `treasury_memo.docx`.

* `fee_policy_choice.xlsx` — the five policies under each rung construction with the replay's reproduction count (ask C), the payout-value
  sheet (ask A) and the returns sheet (ask B).
* `inclusion_by_hour.png` — each policy's replayed inclusion within two blocks by hour of day as five lines, with the 95% line labelled,
  the marketplace's request profile shaded and the 02:00 batch marked.
* `treasury_memo.docx` — the policy adopted, its expected fee, and why the trial's cheapest policy is not eligible.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the four trial weeks, the total value paid out in US dollars. *Device:* the ledger
  stores amounts in each token's base units, six decimal places for one stablecoin and eighteen for the other, as the token registry
  records. Summing raw amounts swamps every week with the second coin.
* **Ask B (device-carried).** For each of the twelve payout corridors, last month's returned payouts. *Device:* a return is recorded as a
  negative payout linked to the original, and a partial return as several, as the ledger guide documents. Counting negative rows as returns
  overstates the corridors where recipients' banks return in parts.
* **Ask C (validity).** For each policy, inclusion within two blocks in the trial, in the replay at the year's block mix and at the
  request times, its expected fee per payout next quarter, and the replay's reproduction count on the trial.
* **Decoupling.** Clearing the replay at the request times changes no figure in asks A or B. Token decimals and returns touch no bid,
  broadcast, request or block record.

## 11. Rubric arithmetic

4 weeks (ask A) + 12 corridors (ask B) + 5 policies × 3 inclusion figures + 5 fees + 1 reproduction count (ask C) + the policy, its fee,
its margin to 95% and the nearest policy's miss + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Trial inclusion within two blocks: P1 99.9%, P2 99.6%, P3 99.8%, P4 99.4%, P5 99.9%. Median fee paid: P3 30¢, P2 41¢, P5 52¢, P1 69¢,
  P4 78¢. Mean fee as run: P2 52¢, P5 66¢, P3 79¢, P1 84¢, P4 92¢; P2 reweighted 81¢.
* Replay, inclusion in calm / normal / full blocks: P1 100 / 97.0 / 72; P2 100 / 96.5 / 75; P3 100 / 90.0 / 45; P4 99.8 / 99.0 / 96.5;
  P5 100 / 96.0 / 74. Block mix at the request hours 41 / 37 / 22; over the year 58 / 33 / 9; at 02:00, 96 / 3.4 / 0.6. Next quarter's
  inclusion: P4 98.8, P2 93.2, P5 92.8, P1 92.7, P3 84.2; P4 without bumps or with median clearing levels 94.1.
* Expected fee per payout: at the request hours P4 146¢, P1 130¢; at the year's mix P5 87¢.
* Token decimals and returns are independent of every main-call record.
