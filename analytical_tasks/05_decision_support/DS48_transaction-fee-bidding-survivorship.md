# DS48 — How much priority fee to bid: you only see the transactions that got in

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Bidding for priority in congested queues (ad slot bidding, API priority tiers, spot capacity) where only winning bids are observed |
| Domain | Payments / blockchain infrastructure |
| Task shape | 04 · Setting one dial (the priority fee (gwei) that achieves inclusion within 2 blocks with 95% probability under the memo's congestion regimes) |
| Core method | Use mempool-independent block data: for each block, the minimum effective priority fee among included transactions (the clearing level) and base-fee dynamics; inclusion probability within 2 blocks for a bid b = share of 2-block windows where b ≥ the clearing level of at least one block in the window, by congestion regime (base-fee change sign, gas used ratio); choose the smallest b meeting 95% |
| Analytical stump | Using the median priority fee *paid* by included transactions is survivorship: it reflects winners' bids (often overpaying wallets), not the clearing threshold, and ignores how congestion changes the threshold. Bids based on the paid distribution either overpay in calm periods or fail in congested ones |
| Primary sources | Ethereum mainnet blocks and transactions (Google BigQuery public dataset `crypto_ethereum`) |

## 1. The real-world situation

A payments company settles stablecoin transfers on Ethereum and needs 95% of transfers included within two blocks. Its wallet sets the priority fee
to the median priority fee paid in the last 100 blocks. During congestion, transfers wait many blocks; in calm periods the company overpays.

## 2. The decision (one deterministic recommendation)

**The priority fee bid (gwei, 0.1 steps) per congestion regime meeting 95% inclusion within 2 blocks, and the cost versus the median-paid rule over
the evaluation month.**

Rules (treasury memo):

* Data: blocks and transactions for 3 months (calibration) and the following month (evaluation); EIP-1559 type-2 transactions.
* Clearing level per block: the 1st percentile of effective priority fee (= min(max priority fee, max fee − base fee)) among included type-2
  transactions, excluding zero-fee and builder/MEV payment transactions per memo heuristics.
* Regimes by previous block: gas used ratio ≥ 0.95 ("congested"), 0.5–0.95 ("normal"), < 0.5 ("calm").
* Inclusion within 2 blocks for bid b at block t: b ≥ clearing(t) or b ≥ clearing(t + 1).
* Choose the smallest b per regime with inclusion ≥ 95% in calibration; evaluate in the evaluation month: inclusion rate and total priority fees
  for the company's 50,000 transfers (memo's timing distribution).
* Contrast: median paid priority fee over the previous 100 blocks.

## 3. Why capable analysts get it wrong

* Paid-fee distributions are visible on block explorers.
* Only included transactions appear; failed or delayed bids are invisible.
* Clearing levels, not average paid fees, determine inclusion.
* Congestion regimes shift thresholds sharply.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `eth_blocks_<period>.parquet` | Parquet | ~650k blocks | BigQuery `bigquery-public-data.crypto_ethereum.blocks` | Public blockchain data (Google public dataset terms) | Base fee, gas used |
| 2 | `eth_transactions_type2_<period>.parquet` | Parquet | ~120M | BigQuery `crypto_ethereum.transactions` | Same | Fees, block numbers |
| 3 | `eip1559_spec.md` | Markdown | — | Ethereum EIPs (CC0) | CC0 | Fee mechanics |
| 4 | `mev_payment_heuristics.json` | JSON | — | Task author | — | Exclusions |
| 5 | `treasury_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `wallet_median_rule_log.csv` | CSV | ~50k | Task author (replayed rule) | — | Current rule results |
| 7 | `extraction_queries.sql` | SQL | — | Task author | — | Reproducible queries |

## 5. Deterministic solution path

1. Extract blocks and type-2 transactions; compute effective priority fees; clearing levels.
2. Regime labels; inclusion curves by regime; choose bids.
3. Evaluate on the next month; costs; contrast with median-paid rule.

## 6. Wrong paths (method errors, not misreadings)

**A — median paid fee.** Survivorship; regime-blind.

**B — max priority fee instead of effective priority fee.** Overstates.

**C — including MEV/builder payments.** Distorted clearing levels.

**D — calibrating on the evaluation month.** Optimistic.

## 7. Why the stump is analytical, not semantic

Definitions and rules are specified. The trap is inferring thresholds from winners only.

## 8. Draft task prompt (prose)

> What priority fee should our wallet bid to get 95% of transfers in within two blocks? Estimate clearing levels by congestion regime as the treasury
> memo specifies and compare with the median-paid rule. Provide `bid_policy.csv` (regime: bid, calibration inclusion, evaluation inclusion, cost),
> `inclusion_curves.png`, and a one-page `fee_policy.pdf`.

## 9. Deliverables

* `bid_policy.csv`, `inclusion_curves.png`, `fee_policy.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 regimes × (bid, inclusion calib, inclusion eval, cost) = 12; inclusion curve points (10); contrast totals.

## 11. Golden-output checklist

* Effective fee; clearing definition; regimes; inclusion; evaluation.

## 12. Build notes (scope tuning)

* Confirm the median-paid rule fails 95% inclusion in the congested regime and overpays in the calm regime.
