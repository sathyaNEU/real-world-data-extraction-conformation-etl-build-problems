# FC07 — Feeder upgrades for rooftop solar: growth curves bend, compound-growth lines do not

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Adoption forecasting with saturating diffusion (new device or feature adoption at consumer-tech companies, enterprise seat growth), where compound-growth extrapolation overshoots |
| Domain | Distribution utilities / DER integration / capital planning |
| Task shape | 13 · Scenarios and the flip point (A-or-B decision across a 2 × 3 scenario grid) |
| Core method | Bass diffusion fitted by the discrete OLS form (n_t on N_{t−1}, N_{t−1}²), recursive forecasting to 2030, scenario grid over market potential and innovation rate, flip-point search |
| Analytical stump | Early-phase adoption looks exponential; extrapolating a compound annual growth rate (or fitting a trend to cumulative installs) ignores saturation and imitation dynamics, and flips the capital decision |
| Primary sources | LBNL Tracking the Sun (installation-level PV data), NREL rooftop technical potential, Census ACS housing counts |

## 1. The real-world situation

A distribution utility must choose between **Plan A** (accelerated feeder and transformer upgrades sized for high rooftop
solar penetration by 2030) and **Plan B** (phased upgrades with a 2027 review). The rule: choose Plan A if forecast
cumulative residential PV systems in its service state reach **T** systems by 2030. The planning analyst fitted a
compound annual growth rate to 2016–2023 installations and projected it forward; Plan A won comfortably. The board asked
whether adoption could really keep compounding.

## 2. The decision (one deterministic recommendation)

**Plan A or Plan B, and at what innovation-rate reduction does the base-case decision flip?**

Rules (capital planning memo):

* Data: residential systems (customer segment RES) in the state from Tracking the Sun, counted by installation year
  2005–2023 (n_t = new systems in year t; N_t = cumulative).
* Model: Bass diffusion estimated by OLS on n_t = a + b·N_{t−1} + c·N_{t−1}² over 2006–2023; recover m (positive root), p =
  a/m, q = −c·m; forecast recursively n_t = (p + q·N_{t−1}/m)(m − N_{t−1}) for 2024–2030.
* Scenario grid: market potential ∈ {fitted m, min(fitted m, technical-potential cap)} × innovation multiplier ∈ {1.00,
  0.75, 0.50} applied to p from 2024 (policy change risk). Imitation q unchanged.
* Threshold T = 30% of the state's owner-occupied single-family detached homes (ACS 2022 5-year).
* Decision: Plan A if cumulative 2030 systems ≥ T in the **base cell** (fitted m, multiplier 1.00); report all six cells and
  the multiplier (to two decimals) at which the base case flips.

## 3. Why capable analysts get it wrong

* Growth rates are the lingua franca of planning; a CAGR line through eight years of rapid growth projects explosive
  adoption.
* Fitting a trend to *cumulative* installs or regressing n_t on N_t (not N_{t−1}) produces a mis-specified Bass model with
  very different m.
* Saturation is invisible in early data; only a model with a ceiling and an imitation term can bend.
* Scenario cells are often computed by scaling the base forecast instead of re-running the recursion.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `TTS_LBNL_public_file_<release>_<state>.csv` | CSV | 0.1–1M installations | LBNL Tracking the Sun | Public release (cite LBNL; verify terms) | Installation records |
| 2 | `tts_data_dictionary.xlsx` | XLSX | — | LBNL | Same | Field definitions |
| 3 | `tts_technical_brief.pdf` | PDF | — | LBNL | Same | Coverage notes |
| 4 | `nrel_rooftop_technical_potential_<state>.csv` | CSV | ~counties | NREL rooftop PV technical potential | NREL data terms (attribution) | Cap on suitable roofs |
| 5 | `acs5_2022_B25032_state.csv` | CSV | ~50 | Census ACS | Public domain | Owner-occupied single-family detached |
| 6 | `annual_installs_by_state.parquet` | Parquet | ~1k | Derived from #1 | Same | Aggregated n_t |
| 7 | `bass_1969_reference.pdf` | PDF | — | Published paper (cite) | Cite | Model and discrete OLS form |
| 8 | `eia861_net_metering_<state>.xlsx` | XLSX | ~3k | EIA-861 | Public domain | Cross-check of system counts |
| 9 | `capital_planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `analyst_cagr_projection.xlsx` | XLSX | ~20 | Task author | — | The CAGR projection to challenge |

## 5. Deterministic solution path

1. Aggregate residential systems by installation year; build n_t and N_t.
2. OLS fit; recover m, p, q; check the root selection.
3. Forecast 2024–2030 in each of the six scenario cells by recursion; compare 2030 cumulative with T.
4. Base-cell decision; flip point = the multiplier at which cumulative 2030 = T (bisection to 0.01).
5. Compare with the CAGR projection.

## 6. Wrong paths (method errors, not misreadings)

**A — CAGR extrapolation.** 2030 adoption far above T → Plan A.

**B — Bass regression on N_t instead of N_{t−1}.** Biased parameters; wrong m and decision.

**C — scaling the base path for scenarios.** Ignores the recursion; flip point wrong.

**D — capacity (kW) instead of system counts.** Threshold is in systems; larger systems inflate apparent adoption.

## 7. Why the stump is analytical, not semantic

Counts, model form, scenarios and threshold are explicit. The error is choosing a growth model that cannot saturate, or
mis-specifying the lag structure — a modelling error.

## 8. Draft task prompt (prose)

> The board will pick Plan A only if residential rooftop systems in the state reach the 2030 threshold in the capital
> planning memo. Fit the diffusion model the memo specifies to the Tracking the Sun data, run all six scenario cells, and
> tell me Plan A or Plan B and the innovation-rate reduction at which the base case flips. Provide `adoption_scenarios.csv`
> (fitted m, p, q; 2024–2030 forecasts per cell; 2030 cumulative versus threshold), `adoption_curves.png` showing history,
> the six scenario paths and the analyst's CAGR line against the threshold, and a one-page `plan_decision.pdf` with the
> decision, the flip point and why the CAGR projection disagrees.

## 9. Deliverables

* `adoption_scenarios.csv`, `adoption_curves.png`, `plan_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* m, p, q; 6 cells × 2030 cumulative + decision = 12; 7 base-case annual forecasts; flip point; CAGR contrast.

## 11. Golden-output checklist

* Correct regression form and root; recursion per cell; threshold from ACS; base decision; flip point to 0.01.

## 12. Build notes (scope tuning)

* Pick a state where the CAGR line crosses T before 2030 but the Bass base case does not (or vice versa); confirm the root
  selection yields a positive m above cumulative installs.
* Record the Tracking the Sun release year; later releases add records retroactively.
