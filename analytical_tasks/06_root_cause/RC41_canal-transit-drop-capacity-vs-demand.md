# RC41 — Canal transits fell 30%: did shippers stop coming, or did the drought cap the canal?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Distinguishing a supply constraint from a demand drop (sales falling because of stock-outs vs fewer shoppers; API calls down because of rate limits vs fewer clients) |
| Domain | Maritime logistics |
| Task shape | 18 · Hypotheses versus evidence (demand slowdown, capacity restriction from low lake levels, vessel-size mix → evidence lines: binding daily caps, queue growth, cargo per transit, rerouting to alternatives; the cause a shipping line plans around) |
| Core method | Treat observed transits as min(demand, capacity): count days on which transits are at the published daily cap (binding), track the waiting queue and diversion of traffic to alternative routes, and cargo per transit under draft limits; estimate the capacity-constrained share of the drop as the decline in the cap times binding days versus the decline in transits on non-binding days |
| Analytical stump | Transits are a censored measure of demand when daily slots are capped. Correlating transits with global trade indicators and finding both falling suggests a demand story; but if the cap binds on most days and queues and diversions grow, demand is not the constraint. The two causes predict opposite queue behaviour, which a transits-only analysis never examines |
| Primary sources | IMF PortWatch daily chokepoint transit calls and trade volume estimates; Panama Canal Authority advisories to shipping (draft limits and daily transit slots) and Gatún Lake level data |

## 1. The real-world situation

A container line's network planning team saw Panama Canal transits fall about 30% over several months. The commercial team attributed it to weak
transpacific demand and proposed reducing services. Operations argued that drought-driven slot and draft restrictions were capping traffic and
that ships were diverting via Suez or the Cape. The two explanations imply opposite network decisions.

## 2. The decision (one deterministic recommendation)

**The cause the network plan assumes — capacity restriction or demand slowdown — by the evidence grid, with the capacity-constrained share of the
transit drop.**

Rules (network memo):

* Data: PortWatch daily transit calls for the Panama Canal (total and by vessel type) and for Suez and the Cape of Good Hope; daily slot caps and
  maximum drafts from the canal authority advisories (memo's compiled table with source advisory numbers); daily Gatún Lake level.
* Periods: reference (12 months before the first slot reduction) and restricted (the memo's restricted months).
* Binding day: transits ≥ 95% of that day's cap.
* Evidence lines:
  * E1 binding: binding days ≥ 70% of restricted-period days.
  * E2 queue: the memo's waiting-vessel count series rises by ≥ 50% from reference to restricted.
  * E3 diversion: Suez plus Cape container transits rise while Panama container transits fall (same months).
  * E4 cargo per transit: estimated cargo tonnes per transit fall in step with maximum draft (correlation ≥ 0.5).
  * E5 demand: transits on non-binding restricted days are ≥ 90% of the reference mean (no demand shortfall when capacity is available).
* Capacity restriction is chosen if at least 4 of 5 lines hold; demand slowdown if E1 and E2 fail.
* Capacity-constrained share = (normal daily capacity in the memo − restricted mean cap) × binding share ÷ (reference mean transits − restricted
  mean transits), capped at 100%.

## 3. Why capable analysts get it wrong

* Transits and trade indicators fell together.
* Observed volume is censored by the slot cap.
* Queues and diversions are in different datasets from transits.
* Draft limits reduce cargo per ship without reducing ship counts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `portwatch_daily_chokepoints.csv` | CSV | ~60k (chokepoint × day × type) | IMF PortWatch | IMF PortWatch data terms (free with attribution; verify) | Transits and trade volume estimates |
| 2 | `acp_advisories_slots_drafts.csv` | CSV | ~400 | Task author (compiled from Panama Canal Authority advisories to shipping; cite) | Cite | Daily caps and draft limits |
| 3 | `gatun_lake_levels.csv` | CSV | ~1,500 | Panama Canal Authority | Public (verify terms) | Lake levels |
| 4 | `acp_waiting_vessels.csv` | CSV | ~400 | Task author (compiled from canal authority daily reports; cite) | Cite | Queue series |
| 5 | `network_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `commercial_demand_note.xlsx` | XLSX | — | Task author | — | The demand explanation |

## 5. Deterministic solution path

1. Align daily transits with caps, drafts and lake levels; define periods.
2. Binding days; queue change; diversion comparison; cargo-per-transit correlation; non-binding-day transits.
3. Evidence grid; cause; capacity-constrained share.
4. Contrast with the commercial note's correlation.

## 6. Wrong paths (method errors, not misreadings)

**A — transits vs trade correlation.** Ignores the cap; demand blamed.

**B — monthly totals.** Hides binding days and queue dynamics.

**C — ship counts only.** Misses cargo-per-transit losses from draft limits.

**D — single-route view.** Diversion to Suez and the Cape is invisible.

## 7. Why the stump is analytical, not semantic

All lines are numeric thresholds on public series. The trap is treating a capacity-censored count as demand.

## 8. Draft task prompt (prose)

> Commercial wants to cut transpacific services because canal transits fell 30%. Evaluate the network memo's evidence lines and tell me whether the
> drop is demand or capacity. Provide `canal_evidence_grid.csv` (line: statistic, threshold, holds?), `transits_vs_cap.png`, and a one-page
> `network_plan_note.pdf`.

## 9. Deliverables

* `canal_evidence_grid.csv` — E1–E5 with values and outcomes; capacity-constrained share.
* `transits_vs_cap.png` — daily transits against the cap, with queue and lake level panels.
* `network_plan_note.pdf` — chosen cause and implications for the network plan.

## 10. Where 25+ rubric criteria come from

* Period definitions and alignment: 2.
* E1–E5 statistics and outcomes: 10.
* Capacity-constrained share: 2.
* Cause decision: 1.
* Contrast with the commercial note: 2.
* Chart elements (cap line, binding days, queue, lake level): 4.
* Data checks (type split, missing days): 4+.

## 11. Golden-output checklist

* Binding-day definition at 95% of cap.
* Same-month comparison for diversion.
* Decision rule on 4 of 5 lines.

## 12. Build notes (scope tuning)

* Use the 2023–2024 drought restrictions; confirm binding days exceed 70% and non-binding-day transits stay near the reference level.
