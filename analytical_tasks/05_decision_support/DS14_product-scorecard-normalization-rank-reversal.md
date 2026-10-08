# DS14 — Approved-product scorecards: min–max scaling lets an irrelevant model change the winner

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Vendor and product scorecards (procurement, cloud service selection, supplier ratings) built by normalising and weighting criteria |
| Domain | Building equipment procurement / energy programmes |
| Task shape | 16 · Indicators into one score (seasonal efficiency, cold-climate capacity and cold-climate COP → composite score behind an eligibility screen; the heat-pump models placed on the programme's approved list) |
| Core method | Eligibility screen (certification, refrigerant, size class); Pareto-dominance filter; criteria scaled on *fixed reference ranges* from the memo (not the candidate set's min–max), with direction; weighted sum; approve the top 10 per size class; test stability by adding/removing one extreme model |
| Analytical stump | Min–max normalisation over the candidate set makes each model's score depend on the extremes present; adding or removing one model at an extreme can reorder the others (rank reversal), even when that model is never chosen. Ratios with long tails also need capping at the reference range. Fixed reference scales and dominance filtering make the list stable and defensible |
| Primary sources | ENERGY STAR certified air-source heat pumps (data.energystar.gov) |

## 1. The real-world situation

A utility programme publishes an approved list of heat pumps eligible for its top rebate. The draft scorecard min–max scaled each criterion across
all certified models and weighted them. After one manufacturer certified a model with an extreme capacity ratio but poor efficiency, two previously approved
models dropped off the list, prompting complaints.

## 2. The decision (one deterministic recommendation)

**The approved list (top 10 per size class by composite score on fixed reference scales after eligibility and dominance screens), and the models
whose status changes between the draft method and the memo method.**

Rules (programme memo):

* Data: ENERGY STAR certified air-source heat pump dataset (snapshot date in memo): SEER2, HSPF2, capacity at 5 °F ÷ rated capacity at 47 °F
  (cold-climate capacity ratio) and COP at 5 °F, as certified.
* Eligibility: cold-climate designation, size class (2–3 ton, 3–4 ton, 4–5 ton), refrigerant allowed list.
* Dominance: remove models dominated on all four criteria within the size class.
* Scaling: fixed ranges per criterion from `reference_ranges.json` (e.g., HSPF2 7.5–11.0 → 0–1; COP at 5 °F 1.75–3.0 → 0–1), values capped at
  the range ends.
* Weights: HSPF2 0.30, SEER2 0.15, cold-climate capacity ratio 0.30, COP at 5 °F 0.25.
* Approve top 10 per size class; ties by higher HSPF2.
* Stability check: recompute with the draft method with and without the newly certified extreme model named in the memo; list changes.

## 3. Why capable analysts get it wrong

* Min–max scaling is the default normalisation.
* Scores relative to the set's extremes are unstable as the set changes.
* Dominated alternatives should not affect choices among non-dominated ones.
* Orientation (higher-is-better versus lower-is-better) and caps matter.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ENERGY_STAR_Certified_Air-Source_Heat_Pumps.csv` | CSV | ~30–60k model combinations | data.energystar.gov (EPA) | U.S. Gov public domain | Certified models and ratings |
| 2 | `energy_star_ashp_data_dictionary.pdf` | PDF | — | EPA | Public domain | Fields |
| 3 | `reference_ranges.json` | JSON | 5 | Task author | — | Fixed scales |
| 4 | `programme_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `draft_minmax_scorecard.xlsx` | XLSX | ~300 | Task author | — | Draft scores |
| 6 | `mcda_rank_reversal_citation.pdf` | PDF | — | Cite (Belton & Gear; MCDA texts) | Cite | Concept |

## 5. Deterministic solution path

1. Filter eligibility; derive criteria; size classes.
2. Dominance filter; fixed-range scaling; composite scores; top 10 per class.
3. Draft method with/without the extreme model; changes.

## 6. Wrong paths (method errors, not misreadings)

**A — min–max over candidates.** Rank reversal.

**B — z-scores over candidates.** Same set-dependence.

**C — no dominance filter.** Irrelevant alternatives influence scaling.

**D — uncapped criteria.** Outliers dominate the composite.

## 7. Why the stump is analytical, not semantic

The scales, weights and screens are specified. The trap is set-dependent normalisation in composite scoring.

## 8. Draft task prompt (prose)

> Build the approved heat-pump list using the fixed-scale scorecard in the programme memo, and show how the draft method's list changes when the one
> newly certified extreme model is added. Provide `approved_list.csv` (model: criteria, scaled scores, composite, rank, approved), `rank_stability.png`, and a one-page
> `approved_models.pdf`.

## 9. Deliverables

* `approved_list.csv`, `rank_stability.png`, `approved_models.pdf`.

## 10. Where 25+ rubric criteria come from

* 30 approved models (3 classes × 10); composite scores for 6 boundary models; dominance removals; status changes.

## 11. Golden-output checklist

* Eligibility; dominance; fixed scaling; weights; ties; stability test.

## 12. Build notes (scope tuning)

* Confirm the draft method's top-10 changes by ≥ 2 models when the extreme model is added, while the memo method's list does not.
