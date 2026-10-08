# OS12 — Battery add-ons for solar owners: the attach rate on new installs is not the retrofit rate

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Upsell sizing to an installed base (add-on subscriptions, accessories, protection plans) where attach at purchase differs from later retrofit uptake |
| Domain | Distributed energy |
| Task shape | 02 · Forecast across many periods (annual retrofit battery installations to existing residential PV, 2025–2028; the sales-team headcount committed) |
| Core method | Separate co-installed batteries (commissioned within 90 days of the PV system at the same location/operator) from retrofits; cohort retrofit hazard by PV system age from historical retrofits; apply to the installed PV base by vintage; contrast with applying the new-install attach rate to the base |
| Analytical stump | The share of new PV systems sold with a battery (high and rising) is a point-of-sale decision. Retrofit uptake among existing owners is much lower and depends on system age and feed-in tariff expiry. Multiplying the installed base by the new-install attach rate overstates the retrofit market several-fold |
| Primary sources | Bundesnetzagentur Marktstammdatenregister (MaStR) — registered solar units and storage units (Germany) |

## 1. The real-world situation

An installer plans a retrofit-battery sales team for German homeowners who already have solar panels. The business case multiplied the
installed residential PV base by the current attach rate on new installations. Sales managers who had run retrofit campaigns reported much
lower uptake.

## 2. The decision (one deterministic recommendation)

**Annual retrofit battery installations 2025–2028 in the installer's region, and the sales headcount (one rep per 300 retrofits per year,
rounded up) committed for 2025.**

Rules (sales memo):

* Data: MaStR solar units (residential: ≤ 30 kWp, building-mounted) and storage units (battery, ≤ 30 kWh) in the region's postcodes,
  commissioned up to 2024.
* Linking: a storage unit is co-installed if commissioned within 90 days of a PV unit at the same location identifier (or operator + postcode per
  memo); otherwise a retrofit of the earliest PV unit at that location.
* Retrofit hazard by PV age a (years): retrofits at age a ÷ PV systems at risk at age a (no battery yet), pooled over 2020–2024.
* Projection: installed PV base without battery by vintage × hazard at age, rolling forward with the memo's growth adjustment for 2025–2028.
* Headcount = ceil(retrofits 2025 ÷ 300).
* Report the attach-rate method for contrast.

## 3. Why capable analysts get it wrong

* New-install attach rates are widely reported and impressive.
* Retrofit decisions are made years later, by a different population.
* Hazards by age capture triggers like feed-in tariff expiry (20 years).
* Systems that already have batteries leave the risk set.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `EinheitenSolar_*.xml` (MaStR full export) | XML | ~4M units | Bundesnetzagentur MaStR | Datenlizenz Deutschland – Namensnennung 2.0 | Solar units |
| 2 | `EinheitenStromSpeicher_*.xml` | XML | ~1.5M units | MaStR | DL-DE-BY-2.0 | Storage units |
| 3 | `Lokationen_*.xml` | XML | ~5M | MaStR | DL-DE-BY-2.0 | Location identifiers |
| 4 | `mastr_data_dictionary.pdf` | PDF | — | Bundesnetzagentur | DL-DE-BY-2.0 | Fields |
| 5 | `region_postcodes.json` | JSON | ~300 | Task author | — | Region |
| 6 | `sales_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `business_case_attach_rate.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 8 | `pv_storage_links.parquet` | Parquet | ~150k | Derived | DL-DE-BY-2.0 | Linked units |
| 9 | `growth_adjustment.json` | JSON | — | Task author | — | Projection assumption |

## 5. Deterministic solution path

1. Parse exports; filter residential units in the region.
2. Link storage to PV; classify co-installed versus retrofit.
3. Retrofit hazards by PV age; projection; headcount.
4. Contrast with the attach-rate method.

## 6. Wrong paths (method errors, not misreadings)

**A — base × new attach rate.** Overstated.

**B — not removing systems already with batteries.** Inflated risk set.

**C — linking by operator only.** Mislinks multi-site operators.

**D — hazard on calendar year instead of PV age.** Misses age triggers.

## 7. Why the stump is analytical, not semantic

Linking, hazards and projection rules are given. The trap is conflating point-of-sale attach with installed-base uptake.

## 8. Draft task prompt (prose)

> How many retrofit batteries can we sell to existing solar owners in our region through 2028, and how many reps do we need next year? Build
> the cohort-based retrofit projection in the sales memo from MaStR. Provide `retrofit_projection.csv` (year: base at risk, retrofits),
> `retrofit_hazard_by_age.png`, and a one-page `sales_team_plan.pdf`.

## 9. Deliverables

* `retrofit_projection.csv`, `retrofit_hazard_by_age.png`, `sales_team_plan.pdf`.

## 10. Where 25+ rubric criteria come from

* Hazards at 15 ages; 4 annual projections; headcount; linkage counts; contrast.

## 11. Golden-output checklist

* Residential filters; linking window; classification; risk sets; projection; headcount.

## 12. Build notes (scope tuning)

* Record the MaStR export date; confirm the attach-rate method overstates 2025 retrofits ≥ 3×.
