# OS34 — Capturing curtailed solar with batteries: a 4-hour battery cannot soak up a 9-hour surplus

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Capturing wasted capacity with constrained buffers (caching overflow traffic, storing surplus inventory) where buffer power and size cap what can be captured per cycle |
| Domain | Electricity / renewable integration |
| Task shape | 07 · Grid of cells (battery power × duration options → curtailed MWh captured per year; the configuration with the highest captured MWh per dollar) |
| Core method | Daily simulation over 5-minute curtailment: battery charges from curtailment up to its power limit, stops at full energy, discharges overnight (empties by next morning, memo); captured energy = Σ charged × round-trip efficiency; comparison with total curtailment |
| Analytical stump | Sizing the opportunity as total curtailed MWh (or curtailment ÷ days × duration) ignores that curtailment arrives in long midday blocks with high power: a battery is limited by power during the block and by energy per day. Captured energy saturates quickly; the most cost-effective configuration is not the one that "matches" annual curtailment |
| Primary sources | CAISO production and curtailments data (5-minute wind and solar curtailment) |

## 1. The real-world situation

A developer considers co-locating batteries to absorb curtailed solar in California. The pitch sized the opportunity as annual curtailed MWh ×
a price spread and proposed a 1,000 MW / 4,000 MWh build. Engineers asked how much curtailment each configuration could actually capture.

## 2. The decision (one deterministic recommendation)

**The configuration (from power 250/500/1,000 MW × duration 2/4/8 h) with the highest captured MWh per million dollars of capital cost, and its
captured share of total curtailment.**

Rules (development memo):

* Data: CAISO 5-minute system-wide solar curtailment (economic + self-scheduled, MW) for the year in memo.
* Battery: charges from curtailment only, at min(curtailment, power) until energy is full; round-trip efficiency 86%; fully discharged overnight
  (outside curtailment hours).
* Captured per day = energy charged × 0.86 (delivered later).
* Capital cost per configuration from `battery_costs.json` (power and energy components).
* Metric: annual captured MWh ÷ capital cost (million $); choose the maximum.
* Report the pitch's sizing for contrast.

## 3. Why capable analysts get it wrong

* Annual curtailment totals are widely reported.
* Curtailment is concentrated in spring middays; the battery's daily energy limit binds.
* Power limits bind in high-curtailment intervals.
* Returns diminish quickly with size.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ProductionAndCurtailmentsData_<year>.xlsx` | XLSX | ~105k intervals | CAISO (Managing oversupply page) | CAISO public data (verify terms) | 5-minute production and curtailment |
| 2 | `caiso_curtailment_notes.pdf` | PDF | — | CAISO | Public | Definitions |
| 3 | `battery_costs.json` | JSON | — | Task author (from NREL ATB; cite) | CC BY 4.0 (source) | Cost components |
| 4 | `development_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `pitch_sizing.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 6 | `daily_curtailment_profile.parquet` | Parquet | ~365 | Derived | Public | Daily summaries |

## 5. Deterministic solution path

1. Load 5-minute curtailment; build daily sequences.
2. Simulate each configuration; captured MWh per year.
3. Captured per $; choose; captured share.
4. Contrast with the pitch.

## 6. Wrong paths (method errors, not misreadings)

**A — total curtailment as capturable.** Overstated.

**B — daily energy ignoring power limit.** Overstated in peaks.

**C — no efficiency.** Overstated.

**D — choosing the largest battery.** Ignores diminishing returns per $.

## 7. Why the stump is analytical, not semantic

The simulation rules are specified. The trap is ignoring buffer constraints when sizing capture.

## 8. Draft task prompt (prose)

> Which battery configuration captures curtailed solar most cost-effectively? Simulate the nine options on CAISO 5-minute curtailment as the
> development memo specifies. Provide `capture_grid.csv` (power × duration: captured MWh, share, cost, MWh per $M), `capture_saturation.png`,
> and a one-page `configuration_choice.pdf`.

## 9. Deliverables

* `capture_grid.csv`, `capture_saturation.png`, `configuration_choice.pdf`.

## 10. Where 25+ rubric criteria come from

* 9 configurations × (captured MWh, MWh per $M) = 18; choice; shares; monthly capture for the chosen option (12); contrast.

## 11. Golden-output checklist

* Data extraction; simulation; efficiency; costs; metric; choice.

## 12. Build notes (scope tuning)

* Confirm the pitch's configuration is not the most cost-effective.
