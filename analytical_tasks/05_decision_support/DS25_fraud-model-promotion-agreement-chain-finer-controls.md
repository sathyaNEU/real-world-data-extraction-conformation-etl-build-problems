# DS25 — Which fraud model the platform promotes to checkout, when every evaluation matches the ledger's quarters and only one matches its months

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · payments risk and model governance |
| Mirrors | Promoting a model whose offline evaluation must reproduce settled outcomes at a finer grain than the headline (Amazon and Shopify checkout risk models, Apple and Google app-store subscription fraud screening, cloud marketplaces' metered-billing fraud) |
| Decision shape | Which of N gets one scarce thing: the single model promoted to score every checkout next quarter |
| Committed call | The model promoted, and its expected net loss per $1,000 of settled volume, to two decimals |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · measured #12's architecture (finer controls in the settled ledger separate evaluations that all pass the quarterly headline), with the checkout as the unit built from authorisation attempts (#2) at rung 1 |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution |
| Measured traps engaged | #12 stops at the first control that passes · #2 counts file rows instead of the real unit · #7 uses the ready-made measure · #15 follows the requester's hunch over the rule |
| Calibration form | Settled-transaction ledger: four quarters of settled card volume, chargebacks and representments, with each past promoted model's settled outcome by quarter, month and segment beside the offline evaluation that chose it |
| Driving force | The promotion policy judges a model on what its checkouts settle at: fraud it lets through plus margin on good checkouts it declines. A subscription signup approved on a stolen card does its damage on the renewals that follow, which no checkout model scores, and each chargeback names the renewal capture. Attached to the capture it names, that loss falls on no candidate, and the evaluation still reproduces every past quarter's settled total. Attached through the payment agreement to the checkout that created it, the evaluation also reproduces the ledger's months and its subscription segment, and the sequence model that stops fraudulent signups wins. |

## 1. Situation

A payments platform promotes one fraud model each quarter to score every checkout. Six candidates have been evaluated offline, and the head
of risk wants the one with the best recall at the platform's 1% decline rate. The model governance policy promotes the candidate with the
lowest expected net loss per $1,000 of settled volume, net loss being fraud chargebacks on approved checkouts plus the margin lost on good
checkouts declined, and it requires the evaluation method to reproduce the settled ledger for the models promoted before. The team holds
the authorisation-attempt log, the chargeback and representment file, the payment-agreement table for subscriptions, the settled ledger
for four quarters, and each candidate's scores on last quarter's checkouts.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. The recall figures, the attempt log, the chargebacks,
  the agreement table and the ledger are all right. The difficulty is that the quarterly headline admits two evaluations that pick different
  models, and only the ledger's finer cells choose between them.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the head of risk's view and the recall leaderboard. Net loss per checkout, with chargebacks attached to the
  captures they name, still promotes C and reproduces all four quarters.
* **Instrument repair.** No file the ladder uses is suspect: the attempt log records every authorisation with its payment intent, the
  chargeback file names the disputed capture and the agreement it billed under, and the ledger is complete. Keying every attempt to its
  checkout moves rung 1 to rung 2's C and leaves rung 0 at A. No lower rung names E, because no row records a checkout's later renewal
  losses, and the agreement chain is still needed.
* **Lens swap.** The naive evaluation charges each loss to the transaction it was disputed on. The answer charges it to the checkout that
  let the fraud in: a different population of checkouts, signups that went on to bill renewals.

## 3. The driving force

A strong solver sets aside recall, because the policy judges net loss. It builds checkouts from authorisation attempts, linking each retry
after a soft decline to its payment intent, because a declined attempt that is retried and approved is no lost sale. It then attaches every
settled chargeback to the capture it names and evaluates each candidate. Each step is competent, and C wins at $1.35 per $1,000. The
evaluation also reproduces all four quarterly settled totals of the models promoted before. But the ledger also settles by month and by
segment, and the capture-attached evaluation matches only 5 of 12 months and neither subscription figure. A fraudulent subscription signup
costs little at checkout; its chargebacks arrive on the monthly renewals, one to three months later, and name the renewal capture.
Renewals are billed under the payment agreement the signup created, and no checkout model scores them, so attached to their captures the
renewal losses are the same for every candidate. Attached through the agreement to the signup checkout, the evaluation reproduces every
month and segment, and it charges C $1.60 per $1,000 for the stolen-card signups it approves. E, the sequence model on the device graph,
stops most of them and wins at $1.81.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Recall at the 1% decline rate on last quarter's labelled checkouts | A, gradient-boosted v7 (0.62) | The platform's own leaderboard metric | The governance policy: promotion goes on expected net loss per $1,000 settled, fraud passed plus good margin declined |
| 1 | Net loss per authorisation attempt, chargebacks on the capture they name | B, rules-plus-tree hybrid ($1.65) | Every loss and every decline priced from the logs | The ledger's declined-checkout count: attempt rows overstate declines by 38%, because soft declines retried and approved count as lost sales (#2) |
| 2 | Net loss per checkout (attempts linked through the payment intent), chargebacks on the capture they name | C, challenge-flow model ($1.35) | The right unit, and the evaluation reproduces all four quarterly settled totals | The ledger's months and segments: this evaluation reproduces 5 of 12 months and neither subscription figure |
| 3 | **Decisive:** renewal chargebacks attached through the payment agreement to the signup checkout that created it; net loss per checkout | **E, device-graph sequence model ($1.81)** (4th of 6 on rung 0) | — | — |

* **Position table.** E is 4th on rung 0 (recall 0.46), 6th on rung 1 ($2.96, its challenges counted as lost sales) and 3rd on rung 2
  ($1.66, 1.23× behind C). It leads only rung 3, 1.33× ahead of D ($2.40). Rung margins: 1.17, 1.27, 1.22, 1.33 (lower loss leads).
* **Discriminator dominance.** C carries a 1.23× advantage into rung 3 ($1.35 against $1.66). On the decisive axis, renewal losses from
  approved signups, C carries $1.60 per $1,000 and E $0.15. Final margin: C at $2.95 against E at $1.81, 1.63×. The swing is 2.00, 1.36×
  the 1.48 it needs (1.2 × the carried 1.23).
* **Partial correction priced (L3).** Building the agreement chain on attempts instead of checkouts names B ($2.60, 1.20× under E's
  $3.11). Building it but counting only renewals settled inside a 30-day evaluation window leaves every renewal outside, because the first
  renewal bills at day 30, and names C again (1.23×). No half-insight names E.
* **Grid.** Unit (attempt, checkout) × attachment (capture, agreement) × horizon (30-day window, the policy's 180 days) gives 8 cells. The
  four attempt cells name B, the capture cells and the 30-day agreement cell name C, and only checkouts with the agreement over 180 days
  name E. The nearest wrong cells are one toggle away (C at 1.23×, B at 1.20×).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy says "what its checkouts settle at". The chargeback file names a capture, and no document says a
   renewal's loss belongs to the checkout that created the agreement.
2. **The reproducing rule is a construction, not a menu.** Agreement attachment reproduces 4 of 4 quarters, 12 of 12 months and 8 of 8
   segment cells; capture attachment reproduces 4 of 4, 5 of 12 and 4 of 8, every miss putting subscription losses in the wrong month; card
   fingerprint attachment reproduces 4, 7 and 6. The winning rule follows each renewal capture to its agreement and the agreement to the
   checkout that created it, a two-hop chain with no parameter to scan.
3. **No arithmetic symptom.** Attempts, checkouts, chargebacks and settled volume reconcile under every rung, and every attachment conserves
   the quarterly totals.
4. **Not a row predicate.** It needs attempts grouped into checkouts, renewal chargebacks chained to signup checkouts, each candidate's
   decisions on those checkouts, and the net loss summed over 180 days.
5. **The enumeration is arithmetic.** No column holds a checkout's renewal losses; E's $0.15 falls out of the chain.
6. **No cutover date.** Subscription fraud runs every month, and nothing steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The settled ledger: four quarters of settled volume, chargebacks net of representment wins, and declined-checkout counts, by
  month and by segment (subscription, one-off), with each past promoted model's offline evaluation beside its settled outcome.
* **What it pins.** The checkout unit, through the declined-checkout counts, and the agreement attachment, through the months and segments
  (property 2). The quarterly totals pass every attachment, which is why a solver who checks only the headline is confirmed at rung 2.
* **Twin pair.** Quarters Q2 and Q4 are identical on every visible ledger column: $412M settled, 1.9M checkouts, the same one-off fraud loss
  ($0.88 per $1,000) and the same chargeback count. Their subscription losses settled at $0.92 and $0.46 per $1,000 (2.0×). Only the chain
  separates them: Q2's renewals came from signups the model promoted in Q1 had approved.
* **Every rule exercised.** The ledger holds annual and monthly subscriptions, renewals that charge back in the first and the third month,
  and representment wins that reverse a chargeback, so every link in the chain is tested.
* **Resemblance points at the decoy.** On recall and one-off fraud, E looks like the models that ranked lowest on the leaderboard in the
  last two promotions.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The governance policy: promote the candidate with the lowest expected net loss per $1,000 settled, fraud passed plus
  margin lost on good checkouts declined, counted over 180 days, by a method that reproduces the ledger for the models promoted before. The
  margin schedule: lost margin per declined good checkout by segment. One sentence each.
* **Empirical pins.** The checkout unit and the agreement attachment, from the ledger.
* **Voices.** The head of risk: "Promote the model with the best recall." The payments product lead: "Challenges cost us conversion; keep
  them rare." The data-science lead: "Our offline evaluation has matched the quarterly settlement every time."
* **Licensed wrong basis.** The policy records that the model review board's dashboard compares candidates on recall at the 1% decline
  rate and will see that basis.

## 8. Determinism by construction

* **Checkouts.** Every attempt carries its payment intent, and every intent belongs to one checkout, so the grouping is exact.
* **Chain.** Every renewal capture carries one agreement ID, and every agreement one originating checkout.
* **Horizon.** The policy's 180 days covers every renewal chargeback in the ledger (the latest settles at day 141), so 150-, 180- and
  365-day horizons agree.
* **Rounding.** E's net loss is $1.81 per $1,000, and no rival is within 1.3×.

## 9. Prompt sketch and deliverables

> We promote one fraud model to checkout next quarter, and the head of risk wants the one with the best offline recall. Tell me which model
> we promote and its expected net loss per thousand dollars of settled volume, to two decimals, in a line for the model review board. Send
> `model_promotion.xlsx`, a chart `net_loss.png`, and a one-page `promotion_memo.pdf`.

* `model_promotion.xlsx` — the six candidates under each rung, the ledger reproduction under each attachment, the merchant sheet (ask A),
  the payout sheet (ask B) and the validity sheet (ask C).
* `net_loss.png` — each candidate's net loss split into one-off fraud, renewal fraud and declined margin as stacked bars, with the promoted
  model marked, and a panel of the ledger's twelve monthly subscription losses against the capture and agreement evaluations.
* `promotion_memo.pdf` — the committed model and figure, and why the recall leader and the rung-2 winner lose.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Monthly active merchants by segment over the last year. *Device:* a merchant with several
  storefronts holds one merchant ID per storefront under a parent account, as the merchant register documents. Counting IDs overstates the
  subscription segment by about a fifth.
* **Ask B (device-carried).** Median days from settlement to payout by month. *Device:* rolling reserves hold back 10% of a merchant's
  settlement and release it 90 days later as a separate payout row. Treating the release as its own payout puts a 90-day tail into every
  month.
* **Ask C (validity).** Each attachment's reproduction of the ledger (quarters, months, segments), and each candidate's net loss under the
  four rungs.
* **Decoupling.** Clearing the chain and the checkout unit changes no figure in asks A or B. Merchant IDs and payouts never enter a
  checkout, a chargeback or a net loss.

## 11. Rubric arithmetic

6 candidates × 4 rungs + 3 attachments × 3 control types (ask C) + 12 months × 3 segments (ask A) + 12 monthly medians (ask B) + the
committed model, its figure and the runner-up + 5 named chart parts + 3 files ≈ 92 criteria.

## 12. World-building constraints

* Per $1,000 settled (one-off fraud passed, margin lost per checkout, margin lost per attempt, renewal losses through the chain): A 1.10,
  0.60, 1.35, 0.90; B 0.95, 0.70, 0.70, 0.95; C 0.80, 0.55, 1.30, 1.60; D 1.00, 0.70, 1.20, 0.70; E 0.91, 0.75, 2.05, 0.15; F 1.20, 0.65,
  1.10, 0.60. Recall at 1%: 0.62, 0.53, 0.50, 0.44, 0.46, 0.40.
* Ledger reproduction: agreement 4/4, 12/12, 8/8; capture 4/4, 5/12, 4/8; card fingerprint 4/4, 7/12, 6/8. Attempt rows overstate declined
  checkouts by 38%.
* Q2 and Q4 are identical on every visible ledger column. Merchant IDs and payout rows never touch attempts, chargebacks or agreements.
