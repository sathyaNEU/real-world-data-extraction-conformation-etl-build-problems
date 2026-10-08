# OS02 — Heat-pump retrofit market: multiplying percentages assumes the conditions are independent

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Top-down TAM built by multiplying segment percentages (share with X × share with Y × share with Z), used in product and go-to-market planning everywhere |
| Domain | Residential energy / HVAC |
| Task shape | 09 · Funnel or chain of stages (households → electric-resistance or fuel-oil heated → owner-occupied → single-family detached → income above threshold; the stage where a fixed marketing budget yields the most qualified households) |
| Core method | Weighted microdata counts of households satisfying the joint conditions at each stage (survey weights), conditional pass-through rates computed on the previous stage's population; comparison with the product of national marginal shares |
| Analytical stump | Heating fuel, tenure, housing type and income are strongly correlated (owner-occupied detached homes skew to higher incomes and to gas in some regions, oil in the Northeast). Multiplying marginal shares assumes independence and misstates the market by large factors; conditional rates must be computed in sequence from the joint distribution |
| Primary sources | U.S. EIA Residential Energy Consumption Survey (RECS) 2020 public-use microdata |

## 1. The real-world situation

A heat-pump installer sizes its retrofit market in four census regions. The strategy deck multiplied national percentages — households
heating with electric resistance or fuel oil, owner-occupied, single-family detached, income above $75,000 — by the region's household count.
The sales team found far fewer qualified leads in some regions and more in others.

## 2. The decision (one deterministic recommendation)

**The qualified-household count per region (weighted, millions, two decimals) and the funnel stage at which an additional $1M of targeted
marketing (which raises the stage's pass-through by the memo's assumed uplift) yields the most qualified households.**

Rules (strategy memo):

* Data: RECS 2020 microdata with final weight `NWEIGHT`; regions from `REGIONC`.
* Stages: (S0) all households; (S1) main space-heating fuel electricity with resistance equipment, or fuel oil (memo's codes); (S2)
  owner-occupied; (S3) single-family detached; (S4) household income ≥ $75,000 (income category variable).
* Pass-through rate at stage k = weighted count(S_k) ÷ weighted count(S_{k−1}), by region.
* Qualified households = weighted count at S4.
* Marketing lever: $1M raises one stage's pass-through by the uplift in `marketing_uplifts.json` (stage-specific, absolute points) in every
  region; choose the stage maximising added S4 households (recomputed through the chain).
* Report the deck's product-of-marginals estimate for contrast.

## 3. Why capable analysts get it wrong

* Top-down percentages are quick and familiar in decks.
* Correlated attributes make the product of marginals wrong; the joint distribution is needed.
* Conditional rates depend on the previous stage's population.
* Survey weights must be applied at every stage.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `recs2020_public_v7.csv` | CSV | ~18.5k households, ~800 columns | EIA RECS 2020 | U.S. Gov public domain | Microdata |
| 2 | `RECS 2020 Codebook for Public File - v7.xlsx` | XLSX | — | EIA | Public domain | Variable codes |
| 3 | `recs2020_methodology.pdf` | PDF | — | EIA | Public domain | Weights, replicate weights |
| 4 | `recs2020_published_tables_hc6.xlsx` | XLSX | — | EIA | Public domain | Validation of heating fuel shares |
| 5 | `stage_definitions.json` | JSON | 5 | Task author | — | Codes per stage |
| 6 | `marketing_uplifts.json` | JSON | 4 | Task author | — | Lever assumptions |
| 7 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `strategy_deck_marginals.xlsx` | XLSX | 4 regions | Task author | — | Naive TAM |
| 9 | `region_household_counts.csv` | CSV | 4 | EIA RECS totals | Public domain | Region totals |

## 5. Deterministic solution path

1. Apply stage filters sequentially with weights by region.
2. Pass-through rates and qualified counts.
3. Lever simulation per stage; choose stage.
4. Contrast with the product of marginals; validate fuel shares with published tables.

## 6. Wrong paths (method errors, not misreadings)

**A — product of national marginals.** Independence assumed.

**B — regional marginals multiplied.** Still independent within region.

**C — unweighted counts.** Sample, not households.

**D — lever applied to unconditional shares.** Wrong chain effect.

## 7. Why the stump is analytical, not semantic

Codes and rules are explicit. The trap is ignoring dependence among segment attributes.

## 8. Draft task prompt (prose)

> How big is our heat-pump retrofit market in each region, and which funnel stage should the next $1M of marketing target? Build the chain
> from RECS microdata as the strategy memo specifies and compare with the deck. Provide `retrofit_funnel.csv` (region × stage: weighted count,
> pass-through), `funnel_chart.png`, and a one-page `market_sizing.pdf`.

## 9. Deliverables

* `retrofit_funnel.csv`, `funnel_chart.png`, `market_sizing.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 regions × 5 stages counts = 20; pass-throughs; lever results for 4 stages; chosen stage; deck contrast.

## 11. Golden-output checklist

* Codes; weights; sequential filtering; conditional rates; lever recomputation; contrast.

## 12. Build notes (scope tuning)

* Confirm the deck overstates at least one region by ≥ 40% and understates another.
