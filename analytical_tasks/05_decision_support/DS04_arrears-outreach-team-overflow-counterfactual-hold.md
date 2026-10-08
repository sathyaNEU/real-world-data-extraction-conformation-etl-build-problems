# DS04 — Which region gets the utility's extra arrears-outreach team, when the only fair comparison says none of them clears break-even

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · utility credit and collections |
| Mirrors | Funding a payment-recovery outreach team on outcomes of reached versus unreached accounts, where reach depends on who answers (pre-suspension collections calls at telecom carriers such as Verizon and Vodafone, overdue-invoice outreach before account suspension at AWS and Microsoft Azure, missed-instalment contact at Klarna and Affirm), with queue overflow supplying the natural experiment |
| Decision shape | Hold, forced by a blocking quantity: one team for one of five service regions, or the money back to the bad-debt reserve |
| Committed call | The region that gets the team, or that none does; and the defaults prevented per 100 customers called that the call rests on, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · S10, the governing verb is causal so the baseline is constructed from capacity overflow, with the population a flag suggests (#5) at rung 1 |
| Gate G mechanism | signal_vs_noise_or_hold, with decomposition_attribution |
| Measured traps engaged | #5 takes the population a flag or filter suggests · #15 follows the requester's hunch over the rule · #7 uses the ready-made measure · #13 validates on one population, applies to another |
| Calibration form | Gold-standard verification subsample: the revenue-assurance office's file review of a random 10% of flagged accounts, verifying list eligibility, contact and the 120-day default |
| Driving force | The board funds a team only where calls prevent at least 3.4 defaults per 100 customers called. Called customers do default far less often, but a caller reaches the customers who answer, and those customers were going to pay anyway. On days the list outruns the team, the accounts below the day's last attempted call are never attempted, and list order is set by the billing system's partition key alone. That overflow, built from list positions and the capacity log, is the only comparison in which a call is as good as random. On it the best region prevents 1.9 per 100, with a 90% upper bound of 3.0. |

## 1. Situation

A regional energy utility runs a payment-support programme. Its callers phone residential customers on the first business day after the
account turns 30 days past due, offering a payment arrangement and referrals to bill-assistance funds. Next year it can fund one more
outreach team in one of its five service regions, or return the money to the bad-debt reserve. The board's credit policy funds a team only
where outreach prevents at least 34 defaults per team-year, which is 3.4 per 100 customers called. A default is a disconnection order or a
collections-agency referral within 120 days of listing. The account register carries the nightly ageing job's arrears flag. The outreach
protocol defines who goes on the call list, and each team's capacity log records how many accounts it attempted each day. The head of
customer operations is convinced the calls work.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the register's arrears flag (correctly
  computed by the ageing job), the call log, the defaults in the ledger and the agency's placement file, the capacity log and the verified
  subsample. Called customers really do default less. The difficulty is that the policy's verb is "prevents", and the comparison that
  measures prevention has to be constructed from an operational file nobody reads as evidence.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of operations' belief and the subsample. Called against uncalled, risk-adjusted, still clears
  break-even in Ellesmere, and every number reconciles.
* **Instrument repair.** No file the ladder uses is suspect: the flag is a correct ageing status (a different attribute from list
  eligibility), the call and capacity logs are complete, and the verified subsample confirms that the ledger and the placement file capture
  every default. The deepest repair on offer, a recorded reason for every uncalled account, leaves rungs 0 to 2 at Kingsmere, Redbank and
  Ellesmere, because each compares called with uncalled accounts, and no record of the past observes a called customer's uncalled outcome.
  The overflow split is still needed for the hold.
* **Lens swap.** The naive comparison sets all called customers against all uncalled ones. The answer compares accounts on over-capacity
  days split at the day's attempt count: a different population, compared at a cut the naive read never forms.

## 3. The driving force

A strong solver compares called with uncalled customers and finds a 5.7 to 8.1 point gap. It restricts to the accounts the protocol
actually lists and adjusts for risk score, balance owed and prior arrears. Each step is competent, and Ellesmere still clears break-even at
3.9. But who gets a call is not random. Callers reach the customers who pick up, and those customers default less on dimensions no column
in the register carries. One file breaks the selection. Each team works its list from the top, the list is ordered by the billing system's
partition key, and the capacity log says how many accounts the team attempted that day. On over-capacity days every account below that
count was never attempted, for no reason connected to the customer's finances. Comparing attempted with never-attempted accounts on those
days, within each region, gives the effect of a call. It is 0.5 to 1.9 per 100, and no region's upper bound reaches 3.4.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Default rate of uncalled minus called among flagged accounts, per region | A, Kingsmere (8.1 per 100) | The programme's own outcomes; every region clears break-even | The protocol: the list holds residential accounts 30 days past due on the list date with no payment arrangement in force and no final bill issued, and 11% of flagged accounts never qualify |
| 1 | The protocol's listed population (#5), unadjusted | B, Redbank (5.6) | The right population, and Kingsmere's move-out final bills no longer inflate its uncalled group | The register: called customers carry lower risk scores, smaller balances and fewer prior arrears than uncalled ones in every region |
| 2 | Listed population, risk-adjusted called-versus-uncalled gap | C, Ellesmere (3.9, the only region above 3.4) | Population and confounders handled; Ellesmere clears the policy bar | The capacity log with list positions: on over-capacity days the never-attempted accounts default within 1.9 points of the attempted ones in Ellesmere |
| 3 | **Decisive:** within each region, on days the list exceeded attempts, compare attempted with never-attempted accounts split at the day's attempt count | **Hold: none of the five clears 3.4 (Ellesmere 1.9, 90% interval 0.8–3.0)** | — | — |

* **Position table.** Rung leaders are Kingsmere, Redbank, Ellesmere and then hold. Margins are 1.23 (Kingsmere over Redbank), 1.22
  (Redbank over Ellesmere) and 1.26 (Ellesmere over Redbank). On rung 3 Ellesmere still ranks first (1.9 against Stoneleigh's 1.4), so the
  hold is a refusal of the leader, not a tie.
* **Blocking quantity.** The best overflow effect is Ellesmere's 1.9 per 100 called, 56% of break-even. Its 90% upper bound is 3.0 and its
  95% bound 3.2, both under 3.4. The other four regions' upper bounds are 1.9 to 2.6.
* **Falsifiability.** Ellesmere would have been the pick at an overflow effect of 3.4 per 100, 1.79× its measured effect. Any region whose
  upper bound and point estimate cleared 3.4 would have been funded.
* **Partial correction priced (L3).** Using the over-capacity days but comparing called customers with every uncalled account on those
  days, refusals and unreachable numbers included, puts Ellesmere at 3.6 and funds it. The half-insight lands on a pick, further from the
  answer than rung 2's own figure. Pooling the overflow across regions mixes their baselines: the regions with the most over-capacity days
  also default most, so the pooled cut puts the effect at 3.6 per 100 everywhere, and the team goes where most customers are called,
  Kingsmere. No half-insight holds.
* **Grid.** Population (flag, protocol) × adjustment (none, risk) × comparison (all uncalled, overflow cut) gives 8 cells. Under the cut
  the population and adjustment toggles are idle (only listed accounts have list positions, and the cut is as good as random), so the four
  cut cells are one construction, and it holds. The four without it name Kingsmere, Redbank or Ellesmere. The nearest pick to the answer is
  the partial above (Ellesmere at 3.6), and it costs one error: an uncalled group the list cut never formed.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The protocol says the list is worked from the top. No document calls the never-attempted accounts a comparison
   group, or says that callers reach the customers who would have paid anyway.
2. **No sweepable corpus nominates it.** *The verification protocol records whether a customer was reached and never why an unreached
   account was not called.* So the subsample's called-versus-uncalled gap reproduces rung 2's adjusted gap within 0.2 points in every
   region, and it cannot see the overflow cut.
3. **No arithmetic symptom.** List lengths, attempts and calls reconcile with the capacity log, and defaults tie to the ledger and the
   placement file under every comparison.
4. **Not a row predicate.** Overflow status is a rank inside a team-day group, cut at that day's attempt count from a second file, and the
   effect is then a within-region difference on those days only.
5. **The enumeration is arithmetic.** No column marks an account as never attempted for capacity; it follows from position against the
   day's count.
6. **No cutover date.** Overflow days are scattered through the year, on 38–46% of days in every region, and no series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The revenue-assurance office's verified subsample: 2,140 flagged accounts drawn at random last year, each with verified list
  eligibility, verified contact (from call recordings) and a verified 120-day default (from the ledger and the agency's placement file).
* **What it certifies.** The measures every rung uses. The ledger's default flag agrees with the file review on 97.8% of records and the
  call log's contact field on 99.1%. The register flag disagrees with verified eligibility on 11%, every case a move-out final bill or an
  arrangement already in force, which confirms rung 1.
* **What it is blind to.** The reason an account went uncalled (above). A back-tester is confirmed at rung 2.
* **Twin pair.** Redbank's second quarter and Stoneleigh's third, both closed, are identical on every visible column: 612 listed accounts,
  410 customers reached, mean risk score 0.24, unadjusted gap 5.0 and adjusted gap 2.9. Their overflow effects are 2.2 and 1.0 per 100
  (2.2×). Only the overflow cut separates them, so no gap transferred by resemblance reproduces both.
* **Every rule exercised.** Thirty team-days had a list exactly as long as the attempts (no overflow), which tests the day-level cut. Two
  teams split a region's list by language line, so the cut is per team, not per region.
* **Resemblance points at the decoy.** Ellesmere's profile matches the flagship utility of the published outreach evaluation the head of
  operations cites.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board's credit policy: a team is funded only where outreach prevents at least 34 defaults per team-year, otherwise
  the funds return to the bad-debt reserve. The protocol: the list holds residential accounts 30 days past due on the list date with no
  payment arrangement in force and no final bill issued, and calls happen on the first business day after listing. The list specification:
  lists are built in billing-partition order. One sentence each, in three documents.
* **Empirical pins.** The call effect, from the overflow cut. Covariate balance between attempted and never-attempted accounts, from the
  same days.
* **Voices.** The head of customer operations: "Our called customers default half as often; the calls work." Ellesmere's team lead: "We
  run the tightest programme in the company." The finance lead: "If it clears break-even, fund it."
* **Licensed wrong basis.** The policy records that the state commission's consumer-protection staff judge arrears programmes on
  risk-adjusted outcomes of contacted against uncontacted customers and will see that comparison.

## 8. Determinism by construction

* **The cut.** The capacity log counts attempts per team-day, and attempts run strictly down the list, so the never-attempted set has one
  reading. No account is carried to a later day: the call window is the first business day after listing, and an unattempted account
  moves to the letter track.
* **Balance.** On overflow days attempted and never-attempted accounts match on risk score (0.31 against 0.31), balance owed and prior
  arrears to within 0.5%, so adjusted and unadjusted overflow effects agree to 0.1.
* **Intervals.** Every region's 90% and 95% upper bounds sit below 3.4, so the interval convention cannot turn the hold into a pick.
* **Maturity.** The extract is 150 days after the last listing, so every 120-day outcome has matured.

## 9. Prompt sketch and deliverables

> Next year I can fund one more payment-support outreach team in one of our five regions, or put the money back in the bad-debt reserve.
> Our head of customer operations is convinced the calls are working. Tell me where the team goes, or that it should not be funded, in one
> sentence for the board, with the defaults per hundred customers called you are relying on, to one decimal. Send `team_case.xlsx`, a
> chart `effect_by_region.png`, and a one-page `board_note.docx`.

* `team_case.xlsx` — the five regions' effects under each construction, the meter-installation sheet (ask A), the inbound-call sheet (ask
  B) and the balance sheet (ask C).
* `effect_by_region.png` — five regions with the overflow effect as points and 90% intervals, the risk-adjusted gap as hollow markers,
  break-even as a labelled reference line at 3.4, and the leader's distance to it annotated.
* `board_note.docx` — the committed call, the blocking quantity, and what would have made it a pick.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each region and quarter, the number of smart meters installed. *Device:* an installation
  that fails commissioning is revisited under the same work-order number with a new job ID, as the field-work data guide documents.
  Counting job IDs counts the failed visit and its revisit as two installations, which overstates the two regions with the most
  commissioning failures by 5–8%.
* **Ask B (device-carried).** For each region and quarter, the abandonment rate of inbound calls to the general service line. *Device:* a
  call transferred between queues leaves one record per leg under one call ID, as the telephony data guide documents. Counting legs as
  calls dilutes abandonment by 2–3 points in every region.
* **Ask C (validity).** Each region's effect under the four constructions, and the attempted-versus-never-attempted balance on risk score,
  balance owed and prior arrears.
* **Decoupling.** Clearing the overflow cut changes no figure in asks A or B. Meter jobs and inbound call legs never enter the arrears
  list, the capacity log or the default outcome.

## 11. Rubric arithmetic

5 regions × 4 quarters (ask A) + 5 × 4 abandonment rates (ask B) + 5 × 4 effects + 5 × 3 balance checks (ask C) + the hold, the blocking
quantity, break-even and the falsifying effect + 5 named chart parts + 3 files ≈ 87 criteria.

## 12. World-building constraints

* Effects per 100 called. Rung 0: 8.1 / 6.6 / 5.7 / 4.9 / 4.2. Rung 1: 4.1 / 5.6 / 4.6 / 2.9 / 3.6. Rung 2: 2.8 / 3.1 / 3.9 / 2.0 / 2.7.
  Overflow: 0.8 / 1.2 / 1.9 / 0.5 / 1.4 (Kingsmere, Redbank, Ellesmere, Lowfield, Stoneleigh). Break-even 3.4.
* Ellesmere's overflow standard error is 0.67 over three years of overflow days. Every region's list overflowed on 38–46% of days, and
  list position is unrelated to every register covariate.
* Called-versus-uncalled with every uncalled account on overflow days gives Ellesmere 3.6. Pooling the overflow across regions gives 3.6
  everywhere, because overflow days and default rates rise together across regions.
* Kingsmere's flagged population holds most of the move-out final bills. The twin quarters are identical on every visible column.
* Meter jobs and inbound call legs never touch the list, attempts, calls or defaults.
