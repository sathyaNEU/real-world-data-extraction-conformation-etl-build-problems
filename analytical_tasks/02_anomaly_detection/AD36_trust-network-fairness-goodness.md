# AD36 — Rating fraud in a trust network: victims of bad raters look like bad actors

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Review and rating integrity at marketplaces and platforms (Amazon, Yelp, Airbnb, app stores) where coordinated raters distort averages |
| Domain | Trust & safety / marketplaces |
| Task shape | 01 · Ranked list under a cap (30 raters to suspend) |
| Core method | Fairness–Goodness iteration (Kumar et al., ICDM 2016): rater fairness f(u) ∈ [0,1], ratee goodness g(v) ∈ [−1,1]; g(v) = mean over incoming edges of f(u)·w(u,v); f(u) = 1 − mean |w(u,v) − g(v)| ÷ 2; iterate to convergence; suspend raters with lowest fairness under activity rules |
| Analytical stump | Ranking accounts by average rating *received* flags victims targeted by a ring of negative raters. Ranking raters by how negative they are flags honest raters of genuinely bad actors. Reliability must be estimated jointly: a rater is unfair when their ratings disagree with the reliability-weighted consensus |
| Primary sources | Bitcoin OTC trust weighted signed network (Stanford SNAP) |

## 1. The real-world situation

A peer-to-peer trading community moderates ratings (−10 to +10) users give each other after trades. Moderators can suspend **30** rating
accounts. A first list took raters who gave the most −10 ratings; another proposal suspended the accounts with the lowest average rating
received. Users complained that both lists punished people who had been targeted by, or had warned about, a known scam ring.

## 2. The decision (one deterministic recommendation)

**The 30 rater accounts suspended, ranked by lowest fairness, and the 31st.**

Rules (moderation memo):

* Data: all edges in the Bitcoin OTC network; weights scaled w = rating ÷ 10.
* Initialisation: f = 1 for all raters, g = 1 for all ratees.
* Update order per iteration: goodness from current fairness, then fairness from new goodness; stop when the maximum absolute change in
  both < 1e-6 or after 200 iterations.
* Eligibility: raters with ≥ 10 outgoing ratings.
* Suspension list: eligible raters with fairness < 0.6, sorted ascending by fairness (ties by more outgoing ratings first); top 30; report #31.
* Validation: share of listed raters who rated any account in `known_scammers.json` with ≥ +5 (ring members boosting each other).

## 3. Why capable analysts get it wrong

* Averages of received ratings are the natural reputation score and are easily manipulated.
* Negative ratings are not intrinsically suspicious; disagreement with a reliable consensus is.
* The joint estimation must iterate; one pass leaves raters judged against a contaminated consensus.
* Low-activity raters have unstable fairness; the memo excludes them.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `soc-sign-bitcoinotc.csv.gz` | CSV | ~35.6k edges | Stanford SNAP | Publicly available research dataset (cite Kumar et al.) | Ratings with time stamps |
| 2 | `snap_dataset_page.html` | HTML | — | SNAP | Same | Description |
| 3 | `kumar_2016_rev2_fairness_goodness_citation.pdf` | PDF | — | Cite | Cite | Algorithm |
| 4 | `known_scammers.json` | JSON | ~20 | Task author (accounts with ≥ 10 ratings of −10 from distinct raters, frozen list) | — | Validation |
| 5 | `moderation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `proposal_lists.xlsx` | XLSX | 2 × 30 | Task author | — | Naive lists |
| 7 | `user_activity_summary.parquet` | Parquet | ~5.9k | Derived | Same | In/out degree, dates |
| 8 | `iteration_reference.json` | JSON | ~10 | Task author | — | Check values after 1 and 5 iterations |
| 9 | `rating_scale.json` | JSON | — | Task author | — | Scaling |
| 10 | `edge_time_index.csv` | CSV | ~35.6k | Derived | Same | Time ordering (context) |

## 5. Deterministic solution path

1. Load edges; scale weights.
2. Iterate fairness and goodness in the specified order to convergence.
3. Eligibility; threshold; ranking; top 30 + #31.
4. Validation against known scammers; compare with proposal lists.

## 6. Wrong paths (method errors, not misreadings)

**A — lowest average received rating.** Suspends victims.

**B — most negative ratings given.** Suspends whistle-blowers.

**C — single pass.** Unconverged fairness.

**D — no activity floor.** One-rating accounts dominate.

## 7. Why the stump is analytical, not semantic

The algorithm and rules are specified. The trap is treating a level (rating given or received) as reliability.

## 8. Draft task prompt (prose)

> Which 30 rating accounts should we suspend? Run the fairness–goodness method in the moderation memo on the trade-rating network and give
> me the list. Provide `suspension_list.csv` (rater: outgoing ratings, fairness, rank), `fairness_vs_negativity.png` (fairness against share of
> negative ratings given, list highlighted), and a one-page `suspension_memo.pdf` with the validation result and why the proposal lists fail.

## 9. Deliverables

* `suspension_list.csv`, `fairness_vs_negativity.png`, `suspension_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 30 raters + #31; iterations to converge; fairness for 6 raters; validation share; overlap with two proposals.

## 11. Golden-output checklist

* Scaling; initialisation; update order; convergence; eligibility; threshold; ranking.

## 12. Build notes (scope tuning)

* Freeze the known-scammer list from a pre-specified rule and publish it.
* Confirm the naive lists overlap the final list by < 30%.
