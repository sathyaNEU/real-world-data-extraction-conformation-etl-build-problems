# DA07 — Fleet fuel economy: averaging miles per gallon flatters the fleet

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Fleet-efficiency reporting at delivery and logistics companies; any "average of rates" where the denominator is the quantity consumed (average latency versus throughput, average speed over legs) |
| Domain | Automotive / fleet sustainability |
| Task shape | 10 · Scorecard against thresholds (manufacturer × model year → production-weighted fleet fuel economy versus the internal target; which manufacturers pass) |
| Core method | Fleet fuel economy = production-weighted *harmonic* mean of model MPG (total miles ÷ total gallons for equal miles per vehicle); comparison with production-weighted arithmetic mean; target thresholds applied to the harmonic figure |
| Analytical stump | MPG is a rate with fuel in the denominator. Averaging MPG arithmetically overweights efficient vehicles' savings and overstates fleet economy; for a fleet driving equal miles per vehicle, fuel used is Σ(miles ÷ MPG), so the correct average is harmonic. The ranking of manufacturers against a target flips near the line |
| Primary sources | U.S. EPA Automotive Trends Report data (model-level production and fuel economy); fueleconomy.gov vehicle data |

## 1. The real-world situation

A corporate fleet-procurement team scores manufacturers' model-year line-ups for eligibility on a sustainability framework: the
manufacturer's production-weighted fleet fuel economy must reach the framework's target for its fleet type. The analyst computed
production-weighted average MPG and found eight manufacturers eligible. A reviewer noted that regulators compute fleet averages
harmonically.

## 2. The decision (one deterministic recommendation)

**The list of manufacturers eligible for the framework in model year 2022, judged on production-weighted harmonic fleet fuel economy,
and the margin for each.**

Rules (procurement memo):

* Data: EPA Trends model-level records for MY 2022 (production volumes and real-world/label combined fuel economy as published).
* Scope: light-duty vehicles; split cars and trucks per the EPA regulatory class; electric vehicles counted with their MPGe per the memo
  (and also reported excluding EVs).
* Fleet fuel economy for a manufacturer and class: H = Σ production ÷ Σ (production ÷ MPG).
* Targets by class: cars 32.0 mpg, trucks 24.0 mpg (memo).
* Eligibility: H ≥ target in both classes in which the manufacturer has ≥ 5,000 units; margin = H − target.
* Report the arithmetic production-weighted mean for contrast.

## 3. Why capable analysts get it wrong

* Weighted arithmetic means are the default average.
* The fuel used depends on 1 ÷ MPG; averages of rates must respect what is summed.
* High-MPG electric or hybrid models raise arithmetic means disproportionately.
* Class-level computation matters; combining cars and trucks changes eligibility.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `epa_trends_model_level_my2022.csv` | CSV | ~1.5k model configurations | EPA Automotive Trends Report data | U.S. Gov public domain | Production, fuel economy |
| 2 | `vehicles.csv` | CSV | ~47k | fueleconomy.gov | Public domain | Label data (cross-check, MPGe) |
| 3 | `trends_report_methodology.pdf` | PDF | — | EPA | Public domain | Definitions, harmonic averaging |
| 4 | `manufacturer_groups.json` | JSON | ~15 | Task author | — | Brand → manufacturer |
| 5 | `procurement_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `analyst_arithmetic_scorecard.xlsx` | XLSX | ~14 | Task author | — | Naive scorecard |
| 7 | `regulatory_class_map.csv` | CSV | ~20 | Derived | Public domain | Class assignment |
| 8 | `harmonic_mean_check.json` | JSON | ~5 | Task author | — | Check values |
| 9 | `fuel_economy_trends_tables.xlsx` | XLSX | — | EPA Trends report tables | Public domain | Published aggregates for validation |
| 10 | `ev_mpge_rule.json` | JSON | — | Task author | — | EV treatment |

## 5. Deterministic solution path

1. Filter MY 2022; assign manufacturers and classes; apply EV rule.
2. Compute harmonic and arithmetic production-weighted means per manufacturer × class.
3. Apply volume floor and targets; eligibility and margins.
4. Validate against published aggregates; contrast with the analyst's scorecard.

## 6. Wrong paths (method errors, not misreadings)

**A — arithmetic weighted mean.** Overstates fleet economy.

**B — unweighted mean over models.** Ignores production.

**C — combining classes.** Different targets mixed.

**D — EVs included without the memo's rule.** Distorted averages.

## 7. Why the stump is analytical, not semantic

The averaging formula is specified; the trap is the reflexive arithmetic average of a rate whose denominator is what accumulates.

## 8. Draft task prompt (prose)

> Which manufacturers' MY2022 line-ups pass our fleet-efficiency gate? Compute production-weighted fleet fuel economy the way the procurement
> memo defines it, by class, and compare with the targets. Provide `fleet_scorecard.csv` (manufacturer × class: units, harmonic, arithmetic,
> target, margin, pass), `margin_chart.png`, and a one-page `eligibility_list.pdf` that explains any manufacturer whose status differs from the
> analyst's version.

## 9. Deliverables

* `fleet_scorecard.csv`, `margin_chart.png`, `eligibility_list.pdf`.

## 10. Where 25+ rubric criteria come from

* ~14 manufacturers × 2 classes harmonic values and pass/fail; eligibility list; flips versus the analyst; EV sensitivity.

## 11. Golden-output checklist

* Class assignment; harmonic formula; volume floor; targets; EV handling; validation.

## 12. Build notes (scope tuning)

* Set targets so at least two manufacturers pass on arithmetic but fail on harmonic means.
