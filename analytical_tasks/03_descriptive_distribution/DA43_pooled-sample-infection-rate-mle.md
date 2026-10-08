# DA43 — Infection rates from pooled tests: a positive pool may hold more than one positive

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Batch or pooled testing in quality assurance (composite sampling of lots, pooled lab tests), where a failed batch may contain several defects |
| Domain | Public health / vector control |
| Task shape | 01 · Ranked list under a cap (5 community areas receiving adulticide spraying, ranked by estimated infection rate per 1,000 mosquitoes) |
| Core method | Maximum-likelihood infection rate for pools of unequal size (P(pool negative) = (1 − p)^m); bias-corrected MLE per the memo; comparison with the minimum infection rate (MIR = positive pools ÷ mosquitoes tested × 1,000) |
| Analytical stump | MIR assumes at most one infected mosquito per positive pool; when prevalence is high or pools are large, it underestimates the rate and compresses differences between areas. Areas with large pools are hit hardest, changing the spraying list |
| Primary sources | City of Chicago West Nile Virus (WNV) mosquito test results (Chicago Data Portal) |

## 1. The real-world situation

A city health department sprays adulticide in **5** community areas when mosquito infection rates are highest late in the season. The
surveillance dashboard reports the minimum infection rate. Entomologists noted that in August, pools are often full (50 mosquitoes) and many
are positive, so MIR understates the rate.

## 2. The decision (one deterministic recommendation)

**The 5 community areas sprayed, ranked by MLE infection rate per 1,000 mosquitoes over the evaluation window, and the 6th.**

Rules (vector-control memo):

* Data: WNV mosquito test results for the evaluation window (weeks in memo); species Culex pipiens/restuans combined (memo's species list).
* Trap → community area via coordinates and boundaries.
* Pools: number of mosquitoes per test row (≤ 50), result positive/negative.
* MLE p per area maximising Σ [y_i log(1 − (1 − p)^{m_i}) + (1 − y_i) m_i log(1 − p)]; bias-corrected per Hepworth & Biggerstaff (memo
  formula); rate = 1,000 × p.
* Eligible: ≥ 1,000 mosquitoes tested and ≥ 10 pools in the window.
* Rank; top 5; report #6; MIR for contrast.

## 3. Why capable analysts get it wrong

* MIR is simple and widely reported.
* It is only accurate when prevalence is low and pools small.
* Pool sizes vary across traps and weeks; the likelihood handles unequal sizes.
* All-positive areas need the bias correction (MLE at boundary).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `West_Nile_Virus__WNV__Mosquito_Test_Results.csv` | CSV | ~30k | Chicago Data Portal | City of Chicago data terms (open) | Pools: date, trap, species, count, result, location |
| 2 | `community_areas.geojson` | GeoJSON | 77 | Chicago Data Portal | Open | Boundaries |
| 3 | `trap_locations.csv` | CSV | ~200 | Derived | Open | Trap coordinates |
| 4 | `vector_control_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `dashboard_mir.xlsx` | XLSX | 77 | Task author | — | MIR ranking |
| 6 | `cdc_pooledinfrate_citation.pdf` | PDF | — | Biggerstaff, CDC PooledInfRate (cite) | Public | Method |
| 7 | `mle_check_values.json` | JSON | ~5 | Task author | — | Worked examples |
| 8 | `evaluation_window.json` | JSON | — | Task author | — | Weeks |

## 5. Deterministic solution path

1. Filter window and species; assign traps to areas.
2. MLE (bias-corrected) and MIR per area.
3. Eligibility; rank; top 5 + #6.
4. Contrast with the MIR ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — MIR.** Underestimates at high prevalence.

**B — positive pools ÷ pools.** Ignores pool size.

**C — uncorrected MLE.** Boundary issues for all-positive areas.

**D — counting rows split by species as separate pools without species filter.** Wrong pool set.

## 7. Why the stump is analytical, not semantic

The likelihood and rules are given. The trap is the pooled-sampling model.

## 8. Draft task prompt (prose)

> Which five community areas should we spray? Estimate infection rates from pooled tests with the bias-corrected MLE in the vector-control memo.
> Provide `area_infection_rates.csv` (area: pools, mosquitoes, positive pools, MIR, MLE, rank), `mir_vs_mle.png`, and a one-page
> `spraying_list.pdf`.

## 9. Deliverables

* `area_infection_rates.csv`, `mir_vs_mle.png`, `spraying_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 areas + #6; MLE and MIR for 10 areas; eligibility; contrast; checks.

## 11. Golden-output checklist

* Species and window filters; spatial join; likelihood; bias correction; eligibility; ranking.

## 12. Build notes (scope tuning)

* Choose a late-season window with high positivity so MIR and MLE rankings differ.
