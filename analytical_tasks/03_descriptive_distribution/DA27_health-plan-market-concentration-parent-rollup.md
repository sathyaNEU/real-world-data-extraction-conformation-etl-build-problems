# DA27 — Market concentration by county: contracts are not competitors when one parent owns them

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Competitive-intelligence and corporate-development teams measuring market concentration (HHI) where brands, subsidiaries or SKUs share an owner |
| Domain | Health insurance markets |
| Task shape | 01 · Ranked list under a cap (10 counties selected for a new-entrant plan launch: the least concentrated markets above a size floor) |
| Core method | Herfindahl–Hirschman Index on enrolment shares (in percent, squared, summed) after rolling contracts up to parent organisations; suppressed small cells (< 11 enrollees) handled by the memo's allocation rule; DOJ/FTC concentration bands |
| Analytical stump | Computing HHI over contracts treats sister contracts of the same parent as competitors and understates concentration; ignoring suppressed cells shifts shares upward for visible plans. The ranking of "least concentrated" counties changes after roll-up |
| Primary sources | CMS Medicare Advantage/Part D Contract and Enrollment Data — monthly enrollment by contract/plan/state/county; MA contract information (parent organisation) |

## 1. The real-world situation

A regional insurer plans to enter **10** counties with a new Medicare Advantage product, preferring the least concentrated markets with
enough eligible beneficiaries. Its strategy team computed HHI by county over contracts and found many "unconcentrated" markets. Market-access
staff noted that several large insurers operate multiple contracts in the same county.

## 2. The decision (one deterministic recommendation)

**The 10 counties selected for launch, ranked by lowest parent-level HHI among eligible counties, and the 11th.**

Rules (strategy memo):

* Data: CMS monthly enrollment by contract/plan/state/county for the month in the memo; MA contracts only (H, R, and the memo's other
  prefixes); exclude PDP-only and employer-only plans per memo.
* Parent roll-up: contract → parent organisation from the contract information file.
* Suppressed cells ("*", 1–10 enrollees): assign 5 enrollees each (the memo's convention) and include in the totals.
* Market share s_p = parent enrolment ÷ county MA enrolment × 100; HHI = Σ s_p².
* Eligibility: county MA enrolment ≥ 20,000 and MA penetration ≥ 35% (from the penetration file).
* Rank eligible counties by HHI ascending; top 10; report #11; label DOJ/FTC bands (< 1,000; 1,000–1,800; > 1,800 per memo).

## 3. Why capable analysts get it wrong

* Enrollment files are at contract/plan level; HHI is computed at the level of the file.
* Competition happens between owners; sister contracts do not compete on price in the same way.
* Suppressed cells are numerous in small markets; dropping them biases shares.
* Plan-level rows must be summed to contracts and parents before squaring.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `CPSC_Enrollment_Info_<yyyy>_<mm>.csv` | CSV | ~500k | CMS MA/Part D contract and enrollment data | U.S. Gov public domain | Enrollment by contract/plan/county |
| 2 | `CPSC_Contract_Info_<yyyy>_<mm>.csv` | CSV | ~8k | CMS | Public domain | Contract → parent organisation |
| 3 | `State_County_Penetration_MA_<yyyy>_<mm>.csv` | CSV | ~3.2k | CMS | Public domain | Eligibles, penetration |
| 4 | `ma_enrollment_readme.pdf` | PDF | — | CMS | Public domain | Suppression, definitions |
| 5 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `strategy_contract_hhi.xlsx` | XLSX | ~200 | Task author | — | Contract-level HHI |
| 7 | `doj_ftc_merger_guidelines_excerpt_citation.pdf` | PDF | — | DOJ/FTC (cite) | Public | HHI bands |
| 8 | `contract_prefix_rules.json` | JSON | — | Task author | — | MA filter |
| 9 | `county_fips_crosswalk.csv` | CSV | ~3.2k | Derived | Public domain | SSA ↔ FIPS county codes |

## 5. Deterministic solution path

1. Filter MA contracts and plan types; apply suppression convention.
2. Roll up to parents; county totals; shares; HHI.
3. Eligibility from penetration file; rank; top 10 + #11.
4. Contrast with contract-level HHI.

## 6. Wrong paths (method errors, not misreadings)

**A — contract-level HHI.** Concentration understated.

**B — dropping suppressed cells.** Shares inflated.

**C — shares as fractions without the ×100 convention mixed with bands.** Bands misapplied.

**D — eligibility on total Medicare eligibles instead of MA enrolment and penetration.** Different county set.

## 7. Why the stump is analytical, not semantic

The roll-up, suppression rule and formula are specified. The trap is the unit of competition and handling of censored cells.

## 8. Draft task prompt (prose)

> Which 10 counties should our new MA product enter? Rank eligible counties by parent-level HHI as the strategy memo specifies. Provide
> `county_hhi.csv` (county: MA enrolment, penetration, parents, HHI parent-level and contract-level, band, rank), `hhi_shift.png`
> (contract-level vs parent-level HHI), and a one-page `launch_counties.pdf`.

## 9. Deliverables

* `county_hhi.csv`, `hhi_shift.png`, `launch_counties.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 counties + #11; HHI for 10 counties on both bases; bands; eligibility exclusions; contrast.

## 11. Golden-output checklist

* MA filter; suppression convention; parent roll-up; HHI formula; eligibility; ranking.

## 12. Build notes (scope tuning)

* Confirm at least four of the contract-level top ten fall out after roll-up.
