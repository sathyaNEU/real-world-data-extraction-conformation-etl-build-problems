# task473: start here

| | |
|---|---|
| Task | task473 |
| Objective (Axis 1) | Data Extraction & Conformation (ETL) |
| Block | task445 to task493 |
| Lane owner | unassigned (current owner and status: the root `START_HERE.md` on main) |
| Seed | ET30, `analytical_tasks/07_data_extraction_conformation/ET30_fars-alcohol-impaired-multiple-imputation.md` |

## Before you build

1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.
2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the same objective and keep `task473`.
3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, `stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess (`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.
4. A seed that names a house domain gets the client domain it sits in on its card (`guide-to-prompt/references/domains/README.md`).
5. Branch under your prefix (`.claude/authors/`), `<prefix>/task473-<slug>`, and set the task's Status in the root `START_HERE.md` on main when you start and when you ship.

## Seed index fields

- **title:** Alcohol-impaired-driving fatality rates from FARS: untested drivers, ten imputations and the fan-out join
- **objective:** Data Extraction & Conformation (ETL / Pipeline Build)
- **domain:** Highway safety / federal grant targeting / epidemiology
- **decision_shape:** 01 · Ranked list under a cap (three states receive technical-assistance teams)
- **committed_call:** Which three states in the region receive teams, and which state is fourth?
- **technique:** Multiple-imputation-aware estimation (classify per imputation, then average); crash-level classification from person-level data without fan-out; rate construction with external exposure (VMT)
- **trap:** Known-BAC-only counts; averaging imputed BACs before thresholding; summing crash fatalities over person rows; alcohol-involved (≥ .01) vs impaired (≥ .08)
- **sources:** NHTSA FARS (accident, vehicle, person, multiple-imputation BAC files), FHWA Highway Statistics VM-2

## Seed note

## ET30, Alcohol-impaired-driving fatality rates from FARS: untested drivers, ten imputations and the fan-out join

| Field | Value |
|---|---|
| Domain | Highway safety / federal grant targeting / epidemiology |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (three states receive technical-assistance teams) |
| Core technique | Multiple-imputation-aware estimation (classify per imputation, then average); crash-level classification from person-level data without fan-out; rate construction with external exposure (VMT) |
| Trap family (honest data) | Known-BAC-only counts; averaging imputed BACs before thresholding; summing crash fatalities over person rows; alcohol-involved (≥ .01) vs impaired (≥ .08) |
| Primary sources | NHTSA FARS (accident, vehicle, person, multiple-imputation BAC files), FHWA Highway Statistics VM-2 |

### 1. The real-world project

A regional federal highway-safety office can send intensive impaired-driving technical-assistance teams to **three**
states. Targeting uses the 2020–2022 average alcohol-impaired-driving fatality rate per 100 million vehicle miles
travelled. The analyst counted fatalities in crashes where a driver's *tested* BAC was ≥ .08. A state with very low BAC
testing rates came out with the region's best record.

### 2. The business decision (one deterministic recommendation)

**Which three states in the region receive teams, and which state is fourth?**

Rules (targeting method, following NHTSA's published approach):

* Alcohol-impaired-driving fatality = any fatality in a crash in which at least one **driver** had BAC ≥ .08 g/dL.
* Driver BAC from NHTSA's multiple-imputation file (10 imputed values per person). For each imputation k = 1…10, classify
  each crash by its drivers' imputed BAC in that imputation; count fatalities in classified crashes; the estimate is the
  **mean of the ten counts**.
* Fatalities per crash from the accident file (`FATALS`), attached once per crash (never summed across person or vehicle
  rows).
* Rate = (sum of three annual estimates) ÷ (sum of three annual state VMT from FHWA VM-2) × 100 million.
* Rank descending; teams to the top three; report fourth and the gap.

### 3. Why this gets overlooked in real projects

* Most fatally injured drivers are tested in some states and far fewer in others; known-BAC-only counts reward low
  testing.
* Imputation files look like ten copies of a column; averaging BAC across imputations and then applying .08 produces a
  different (biased) classification than the standard method.
* FARS is relational (crash → vehicle → person); joining crash-level `FATALS` to person rows and summing multiplies
  fatalities by persons per crash.
* "Alcohol-involved" (BAC ≥ .01) and "alcohol-impaired" (≥ .08) are both common terms.

### 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–3 | `FARS2020/accident.csv`, `FARS2021/accident.csv`, `FARS2022/accident.csv` | CSV | ~35–40k each | NHTSA FARS | U.S. Gov public domain | Crash-level FATALS, state |
| 4–6 | `FARS20xx/person.csv` (3 years) | CSV | ~80–90k each | NHTSA | Public domain | Person type, BAC test results |
| 7–9 | `FARS20xx/miper.csv` (3 years) | CSV | ~70–80k each | NHTSA | Public domain | 10 imputed BACs per person |
| 10–12 | `FARS20xx/vehicle.csv` (3 years) | CSV | ~55–60k each | NHTSA | Public domain | Vehicle–person linkage |
| 13 | `FARS_Analytical_Users_Manual_1975-2022.pdf` | PDF |, | NHTSA | Public domain | MI method, codes |
| 14 | `vm2_2020.xlsx`, `vm2_2021.xlsx`, `vm2_2022.xlsx` | XLSX | ~55 each | FHWA Highway Statistics | Public domain | State VMT |
| 15 | `nhtsa_tsf_alcohol_impaired_state_tables.pdf` | PDF |, | NHTSA Traffic Safety Facts | Public domain | Reconciliation targets |
| 16 | `targeting_method.pdf`, `region_states.json` | PDF/JSON |, | Task author |, | Rules, scope |

### 5. Deterministic solution path

1. For each year: identify drivers (person type = driver) and their 10 imputed BACs; compute crash-level max BAC per
   imputation.
2. Flag impaired crashes per imputation; join crash `FATALS` once; sum by state per imputation; average over imputations.
3. Sum three years; divide by three-year VMT; rank region states.
4. Reconcile state counts to NHTSA's published tables (should match closely).
5. Contrast with known-BAC-only, averaged-BAC, fan-out, and ≥ .01 variants.

### 6. The traps

**Trap A, known BAC only.** Low-testing states drop; the top three changes.

**Trap B, average BAC then threshold.** Misclassifies crashes near .08; shifts counts by several percent.

**Trap C, fan-out.** Multi-occupant crashes inflate fatalities.

**Trap D, ≥ .01 threshold.** Measures alcohol involvement, not impairment.

**Trap E, passengers' BAC.** Using any person's BAC instead of drivers'.

### 7. Why the data is honest

FARS is a census of fatal crashes; missing BAC is a real feature handled by NHTSA's published imputation, and NHTSA's own
state tables provide a reconciliation anchor.

### 8. Draft task prompt (prose)

> We can send impaired-driving teams to three states in the region: the three with the highest 2020–2022 average
> alcohol-impaired-driving fatality rate per 100 million VMT, estimated with NHTSA's multiple-imputation approach as our
> targeting method describes. Using the FARS and FHWA files in the folder, tell me the three states and the fourth.
> Deliver `impaired_rates.csv` with each state's annual estimates, three-year total, VMT and rate, and the share of
> fatally injured drivers with a known BAC test; `impaired_rate_chart.png`, ranked bars with the top three highlighted
> and each state's test rate annotated; and a one-page `targeting_memo.pdf` with the decision, the gap between third and
> fourth, and the ranking a known-BAC-only count would have produced.

### 9. Deliverables

* `impaired_rates.csv`, `impaired_rate_chart.png`, `targeting_memo.pdf`.

### 10. Where 25+ rubric criteria come from

* Region states (~8–10) × (3 annual estimates, rate, rank); top 3 + 4th + gap; known-BAC variant; reconciliation.

### 11. Golden-output checklist

* Per-imputation classification then averaging; drivers only; FATALS once per crash; ≥ .08; VMT rates; decision stated.

### 12. Build notes (scope tuning)

* Choose a region where BAC testing rates vary widely across states and confirm Trap A changes the three.
* Check the MI file names/columns for the years used (NHTSA has changed MI file structure over time).
