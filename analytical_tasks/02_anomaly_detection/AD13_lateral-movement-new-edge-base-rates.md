# AD13 — Finding lateral movement in authentication logs: "first time this user touched this host" happens thousands of times a day

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Enterprise security operations centres (endpoint/identity analytics) triaging lateral-movement alerts under analyst capacity |
| Domain | Cybersecurity / insider and intrusion detection |
| Task shape | 01 · Ranked list under a cap (50 alerts per day for analysts) |
| Core method | Rarity-weighted graph novelty: new user→host edges weighted by how few users ever access the destination, with the user's own time-of-day baseline; daily ranking; evaluation by precision at the capacity cut |
| Analytical stump | New authentication edges are a normal part of work; a "first-time edge" rule has a tiny base rate of true attacks and buries analysts. Rarity must be judged against the population (a server only admins touch) and the user's own pattern, and evaluation must happen at the analysts' capacity, not by AUC |
| Primary sources | Los Alamos National Laboratory "Comprehensive, Multi-Source Cyber-Security Events" dataset (authentication events, red-team labels) |

## 1. The real-world situation

A SOC can investigate **50 lateral-movement alerts per day**. The detection engineer shipped a rule that alerts whenever a user
authenticates to a computer for the first time in 14 days, ranked by the number of new hosts that user touched. The queue held tens of
thousands of alerts per day; known red-team activity was in it, but nowhere near the top 50.

## 2. The decision (one deterministic recommendation)

**Adopt the rarity-weighted ranking or keep the current rule, based on red-team events caught in the daily top 50 over the evaluation
period.**

Rules (detection engineering memo):

* Events: successful network logons (authentication orientation LogOn, logon type Network) between distinct computers; user accounts
  only (machine accounts ending in `$` excluded).
* History window: the previous 14 days for each evaluation day; evaluation days = days 30–58 of the dataset.
* Candidate alerts: (user, destination computer) pairs not seen in the history window.
* Score S = [1 ÷ (1 + number of distinct users who authenticated to the destination in the history window)] × (2 if the event hour
  falls outside the user's 5th–95th percentile of logon hours in the history window, else 1). Daily top 50 by S (ties: earliest
  event).
* Current rule C: rank users by count of new destinations that day; alerts = their new edges, top 50 edges by user rank then time.
* Adopt S if it catches more red-team events (user + destination + day matches `redteam.txt`) in the daily top 50 over the evaluation
  period.

## 3. Why capable analysts get it wrong

* Novelty feels suspicious; in enterprises it is ordinary (new servers, shared drives, roaming users).
* The base rate of malicious edges among new edges is tiny; precision at the capacity cut is what matters.
* ROC-AUC rewards ordering across millions of benign edges the SOC will never look at.
* Rarity must be relative to the destination's user population, not just the user's own history.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `auth.txt.gz` | CSV (gz) | ~1.05B events | LANL cyber-security events (2015) | Public release (verify terms) | Authentication events |
| 2 | `redteam.txt.gz` | CSV | 749 | LANL | Same | Red-team compromise events |
| 3 | `proc.txt.gz` | CSV | ~426M | LANL | Same | Context |
| 4 | `flows.txt.gz` | CSV | ~130M | LANL | Same | Context |
| 5 | `dns.txt.gz` | CSV | ~40M | LANL | Same | Context |
| 6 | `auth_network_logons_user_only.parquet` | Parquet | ~100M | Derived | Same | Filtered events |
| 7 | `lanl_dataset_description.pdf` | PDF | — | LANL (Kent 2015) | Cite | Field definitions |
| 8 | `detection_engineering_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 9 | `current_rule_daily_queue_sizes.csv` | CSV | ~29 | Task author | — | Alert volumes |
| 10 | `soc_capacity.json` | JSON | — | Task author | — | 50/day |

## 5. Deterministic solution path

1. Filter events; for each evaluation day, build history-window edge sets, destination user counts and user hour profiles.
2. Generate candidate alerts; score S; daily top 50; match red-team events.
3. Implement C; daily top 50; matches.
4. Compare totals; decide; report daily precision for both.

## 6. Wrong paths (method errors, not misreadings)

**A — evaluate by AUC.** Not the operating point.

**B — novelty without destination rarity.** Common servers dominate.

**C — machine accounts included.** Floods candidates.

**D — history including the evaluation day.** Look-ahead hides novelty.

## 7. Why the stump is analytical, not semantic

Filters, scores and evaluation are defined. The traps are base rates and operating-point evaluation — methodological core of
detection engineering.

## 8. Draft task prompt (prose)

> Our SOC can work 50 lateral-movement alerts a day. Using the LANL authentication logs and the detection memo, compare the current
> first-time-edge rule with the rarity-weighted score at that capacity over days 30–58, counting red-team events caught. Provide
> `daily_alert_eval.csv` (day: candidates, S hits, C hits), `precision_at_50.png`, and a one-page `detection_decision.pdf` with the
> adopt/keep decision and totals.

## 9. Deliverables

* `daily_alert_eval.csv`, `precision_at_50.png`, `detection_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 29 days × (hits under S, hits under C) = 58 values (spot-check 20); totals; candidate volumes; decision.

## 11. Golden-output checklist

* Filters; 14-day windows; score formula; ties; red-team matching rule; decision.

## 12. Build notes (scope tuning)

* The full auth file is huge; ship the filtered parquet plus the extraction script.
* Confirm S catches more red-team events than C at 50/day; if not, still deterministic (keep), but check the setup.
