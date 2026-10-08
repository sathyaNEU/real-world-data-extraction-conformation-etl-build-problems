# RC23 — Births fell 11% in the region: are women having fewer babies, or are there fewer women at peak childbearing ages?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Volume declines that separate per-capita behaviour from base size and composition (orders = customers × segment mix × order rate per segment; ad impressions = users × age mix × sessions per user) |
| Domain | Demography / maternity services and consumer products planning |
| Task shape | 03 · Bridge between two totals (births in the reference year → current year, bridged by female population size, age structure and age-specific fertility rates) |
| Core method | Das Gupta symmetric decomposition of births = population × Σ age share × age-specific fertility rate into three factor effects, using 5-year age groups 15–44 for women; regional totals built from local-authority data; comparison with a TFR-only reading |
| Analytical stump | The total fertility rate is the headline, but it is standardised for age structure, so it cannot explain a births count. A falling TFR is easily over-credited when the cohort of women aged 28–35 is also shrinking (a past birth trough echoing forward). Sequential substitution gives different answers depending on order; the symmetric decomposition is needed |
| Primary sources | Office for National Statistics — births in England and Wales by mother's age and area of usual residence; ONS mid-year population estimates by single year of age and sex for local authorities |

## 1. The real-world situation

A regional maternity network and a large nappy and baby-products manufacturer both track births. The region's births fell 11% over five years. The
manufacturer's strategy team attributed the decline to "the fertility crisis" and proposed cutting regional distribution capacity in line with a
falling TFR. The maternity network's planner argued that the number of women in their late twenties and early thirties was itself falling. Both
need to know which factor dominated.

## 2. The decision (one deterministic recommendation)

**The dominant factor of the births decline (size, age structure or age-specific rates) by Das Gupta effect, with the three effects in births.**

Rules (planning memo):

* Area: the memo's list of local authorities forming the region; reference year and current year.
* Births: live births by mother's age group (under 20, 20–24, 25–29, 30–34, 35–39, 40 and over) by local authority of residence; under-20 births
  assigned to 15–19 and 40-and-over births to 40–44.
* Women: mid-year female population by single year of age summed to 15–19, …, 40–44.
* Rates: r_a = births_a ÷ women_a (regional totals); structure s_a = women_a ÷ women 15–44; size N = women 15–44.
* Births B = N × Σ s_a r_a.
* Das Gupta three-factor effects (N, s, r): each factor's effect = the average of its change over the other factors at reference and current values
  with the standard 1/3, 1/6 weights; the three effects sum exactly to ΔB.
* Report TFR for both years (5 × Σ r_a).

## 3. Why capable analysts get it wrong

* TFR is the measure in every headline and is designed to remove age structure.
* Population ageing at the cohort level is slow and easy to overlook within five years.
* Sequential decompositions are order-dependent.
* Age groups in the births tables do not line up with population ages without explicit rules.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `births_by_area_mothers_age_<years>.xlsx` | XLSX | ~2k per year | ONS births by area of usual residence | Open Government Licence v3.0 | Births by age group and LA |
| 2 | `mye_lad_single_year_<years>.csv` | CSV | ~70k per year (LA × age × sex) | ONS mid-year population estimates | OGL v3.0 | Female population by age |
| 3 | `lad_codes_<year>.csv` | CSV | ~400 | ONS Open Geography Portal | OGL v3.0 | LA codes and boundary changes |
| 4 | `births_user_guide.pdf` | PDF | — | ONS | OGL v3.0 | Definitions |
| 5 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2, LA list |
| 6 | `strategy_tfr_slide.xlsx` | XLSX | — | Task author | — | TFR-based capacity proposal |
| 7 | `das_gupta_1993_citation.pdf` | PDF | — | Cite | Cite | Decomposition method |

## 5. Deterministic solution path

1. Map LAs across boundary changes; aggregate births and women to the region by age group.
2. Rates, structure, size; births reconciliation.
3. Das Gupta effects; closure; TFRs.
4. Dominant factor; contrast with the TFR slide and with sequential substitution in two orders.

## 6. Wrong paths (method errors, not misreadings)

**A — TFR change applied to births.** Attributes the whole decline to rates.

**B — crude birth rate (births ÷ total population).** Mixes age structure of both sexes and all ages.

**C — sequential substitution.** Results depend on order; the dominant factor can flip.

**D — ignoring LA boundary changes.** Areas do not match across years; size effect is wrong.

## 7. Why the stump is analytical, not semantic

The age mapping, area list and formulas are fixed. The trap is a standardised headline measure used to explain an unstandardised count.

## 8. Draft task prompt (prose)

> Births are down 11% in our region and strategy wants to cut capacity because fertility is falling. Decompose the decline using the planning memo's
> Das Gupta method and tell me which factor dominates. Provide `births_decomposition.csv` (factor: effect in births, share), `births_bridge.png`, and
> a one-page `births_decline_rca.pdf`.

## 9. Deliverables

* `births_decomposition.csv` — size, structure and rate effects, plus inputs by age group.
* `births_bridge.png` — waterfall from reference to current births, with the age-structure panel inset.
* `births_decline_rca.pdf` — dominant factor, TFRs, and why the TFR slide misleads.

## 10. Where 25+ rubric criteria come from

* Age-group rates, shares and size for both years (6 groups × 2 years for rates and shares): 24 cells, scored in groups of 6.
* Three effects and closure: 4.
* TFRs: 2.
* Dominant factor: 1.
* Sequential-order contrast and slide contrast: 3+.

## 11. Golden-output checklist

* Age-group mapping rules; female population aggregation.
* Region definition with boundary changes handled.
* Das Gupta weights; exact closure.

## 12. Build notes (scope tuning)

* Choose a region and years where the female population aged 25–34 fell noticeably; confirm that the structure plus size effects exceed the rate
  effect, while the TFR fell enough to make the strategy slide plausible.
