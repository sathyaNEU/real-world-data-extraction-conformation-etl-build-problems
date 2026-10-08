# OS29 — Repowering old wind farms: nameplate added is not energy added

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Upgrade and refresh opportunity sizing (trade-in programmes, server refreshes, network equipment upgrades) where the gain is in performance per unit, not in counts or nominal capacity |
| Domain | Wind energy |
| Task shape | 01 · Ranked list under a cap (12 wind projects for a repowering partnership by incremental annual energy) |
| Core method | For projects with turbines ≥ 15 years old: current annual generation from plant-level reported generation (average of the last 3 years); post-repower energy = new capacity × modern capacity factor for the site's wind resource class (memo table, keyed by hub height and specific power); incremental energy = post − current; rank by incremental MWh |
| Analytical stump | Sizing by nameplate MW added (new turbine rating − old) ignores that modern rotors capture much more energy per MW at the same site, and that some old projects already perform well. Ranking projects by age or capacity picks the wrong ones; incremental energy relative to actual current output does not track either |
| Primary sources | U.S. Wind Turbine Database (USWTDB); EIA-923 plant-level net generation |

## 1. The real-world situation

An infrastructure fund partners with owners to repower **12** old wind projects. The analyst ranked projects by nameplate capacity added
(replacing 1.5 MW turbines with 3 MW turbines on the same pads) and picked the largest old projects. Engineers noted that energy uplift also
depends on rotor size, hub height and how poorly the existing turbines perform.

## 2. The decision (one deterministic recommendation)

**The 12 projects selected, ranked by incremental annual energy (MWh), and the 13th.**

Rules (investment memo):

* Turbines: USWTDB turbines in projects whose median commissioning year ≤ 2009 (≥ 15 years old) and project capacity ≥ 50 MW.
* Project → EIA plant mapping via `eia_id` in USWTDB.
* Current energy: mean annual net generation 2021–2023 (EIA-923).
* Repower scenario: same number of pads × 0.6 (spacing for larger rotors, memo) × 3.0 MW; capacity factor from `cf_by_class.csv` by wind
  resource class (from site mean wind speed at 100 m in the memo's lookup) for a 3 MW turbine with 130 m rotor.
* Post-repower energy = new MW × CF × 8,760.
* Incremental = post − current; rank; top 12; report #13.
* Report nameplate-added ranking for contrast.

## 3. Why capable analysts get it wrong

* Nameplate capacity is the headline number in project databases.
* Modern turbines have much higher capacity factors at the same site.
* Actual current output varies with availability and degradation; the uplift is relative to it.
* Fewer, larger turbines fit on the same land; pad count does not carry over.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `uswtdb_v<version>.csv` | CSV | ~74k turbines | USGS/LBNL/ACP U.S. Wind Turbine Database | Public domain | Turbines, projects, commissioning year, hub height, rotor |
| 2 | `EIA923_Schedules_2_3_4_5_M_12_<yyyy>.xlsx` (2021–2023) | XLSX | ~13k plants each | EIA-923 | U.S. Gov public domain | Net generation |
| 3 | `uswtdb_user_guide.pdf` | PDF | — | USGS | Public domain | Fields |
| 4 | `site_wind_speed_lookup.csv` | CSV | ~1k | Task author (from NREL Wind Toolkit summaries; cite) | CC BY 4.0 (source) | Mean wind speed by project |
| 5 | `cf_by_class.csv` | CSV | ~8 | Task author (from LBNL Wind Market Report curves; cite) | Public | Capacity factors |
| 6 | `investment_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `nameplate_ranking.xlsx` | XLSX | ~120 | Task author | — | Naive ranking |

## 5. Deterministic solution path

1. Aggregate turbines to projects; filter by age and size; map to EIA plants.
2. Current energy; repower capacity and CF; post-repower energy; increments.
3. Rank; top 12 + #13; contrast with nameplate ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — nameplate added.** Ignores CF uplift and current performance.

**B — CF of old turbines applied to new capacity.** Understated uplift.

**C — same pad count.** Overstated capacity.

**D — single-year generation.** Weather noise.

## 7. Why the stump is analytical, not semantic

Mappings and formulas are specified. The trap is sizing on nominal capacity rather than delivered output.

## 8. Draft task prompt (prose)

> Which 12 projects should our repowering partnership pursue? Size incremental annual energy relative to current output as the investment memo
> specifies. Provide `repower_candidates.csv` (project: age, current MWh, new MW, CF, post MWh, increment, rank), `uplift_vs_nameplate.png`, and a
> one-page `partnership_targets.pdf`.

## 9. Deliverables

* `repower_candidates.csv`, `uplift_vs_nameplate.png`, `partnership_targets.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 projects + #13; values for 10 projects; mapping coverage; contrast.

## 11. Golden-output checklist

* Project aggregation; filters; EIA mapping; scenario capacity; CF lookup; ranking.

## 12. Build notes (scope tuning)

* Confirm at least four nameplate top-12 projects drop out.
