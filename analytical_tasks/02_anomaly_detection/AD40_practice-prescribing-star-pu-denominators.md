# AD40 — Prescribing outliers: per-patient rates flag the practices with the oldest patients

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Medicines-optimisation teams in health systems and pharmacy-benefit managers flagging high prescribers; any per-customer usage outlier screen where customer age or segment drives usage |
| Domain | Primary care prescribing |
| Task shape | 01 · Ranked list under a cap (20 practices for a medicines-optimisation visit) |
| Core method | Age–sex weighted denominators (STAR-PU for the drug group) built from practice list-size age–sex bands; items per STAR-PU; funnel-style control limits on the ratio with overdispersion check; ranking by standardized excess |
| Analytical stump | Antibiotic and analgesic use rises steeply with age; practices serving older populations look like heavy prescribers per registered patient. Weighting the list by the drug group's age–sex prescribing weights (STAR-PU) removes demographic case mix; small practices need limits that widen with size |
| Primary sources | NHS Business Services Authority English Prescribing Dataset (EPD); NHS Digital "Patients Registered at a GP Practice" (age–sex quinary bands) |

## 1. The real-world situation

An integrated care board can visit **20** practices this quarter to review oral antibacterial prescribing. Its dashboard ranks practices by
items per 1,000 registered patients; the top of the list is dominated by practices in coastal retirement towns that, once demographics are
considered, prescribe normally.

## 2. The decision (one deterministic recommendation)

**The 20 practices selected for visits, ranked by standardized excess items per STAR-PU, and the 21st.**

Rules (medicines-optimisation memo):

* Prescribing: EPD rows for BNF section 5.1 (antibacterial drugs), 12 months in scope, summed `ITEMS` per practice; practices in the board's
  area; exclude non-GP settings per the memo's setting codes.
* List size: registered patients by sex and quinary age band at the mid-point month.
* STAR-PU weights for oral antibacterials (age–sex table in `starpu_weights.csv`); practice STAR-PU = Σ list in band × weight.
* Ratio R = items ÷ STAR-PU; board mean R̄ = Σ items ÷ Σ STAR-PU.
* Standardized z = (R − R̄) ÷ √(R̄ ÷ STAR-PU) × 1/√φ, where φ is the overdispersion factor estimated from winsorised z-scores (10%/90%)
  per the memo.
* Eligible: list size ≥ 2,000. Rank by z; top 20; report #21.

## 3. Why capable analysts get it wrong

* Per-1,000-patient rates are standard dashboard metrics.
* Age–sex structure explains much of between-practice variation for antibiotics.
* Without overdispersion adjustment, many large practices exceed Poisson limits for reasons unrelated to quality.
* Practice mergers and code changes split list sizes and prescribing; the memo's mapping must be applied.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `EPD_<yyyymm>.csv` (12 months, area extract) | CSV | ~1–2M each (area extract) | NHSBSA Open Data Portal | Open Government Licence v3 | Prescribing items |
| 13 | `gp-reg-pat-prac-quin-age.csv` | CSV | ~250k | NHS Digital | OGL v3 | Registered patients by age band and sex |
| 14 | `starpu_weights.csv` | CSV | 38 | Published STAR-PU tables (cite) | OGL (cite) | Weights |
| 15 | `epd_data_dictionary.pdf` | PDF | — | NHSBSA | OGL | Fields, setting codes |
| 16 | `practice_mergers_map.json` | JSON | ~40 | Task author (from NHS ODS successor data) | OGL-derived | Code continuity |
| 17 | `medicines_optimisation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 18 | `dashboard_per_1000_ranking.xlsx` | XLSX | ~150 | Task author | — | Current ranking |
| 19 | `spiegelhalter_overdispersion_citation.pdf` | PDF | — | Cite | Cite | Overdispersed funnels |

## 5. Deterministic solution path

1. Filter BNF section and settings; sum items per practice with merger mapping.
2. Build STAR-PU denominators from age–sex list sizes.
3. Ratios, z, overdispersion factor, adjusted z.
4. Eligibility; rank; top 20 + #21; compare with the dashboard.

## 6. Wrong paths (method errors, not misreadings)

**A — items per 1,000 patients.** Demographics dominate.

**B — Poisson limits without φ.** Too many flags among large practices.

**C — weights from a different drug group.** Wrong case-mix adjustment.

**D — ignoring mergers.** Split practices with distorted ratios.

## 7. Why the stump is analytical, not semantic

Weights, formula and ranking are given. The trap is denominator choice (case mix) and dispersion.

## 8. Draft task prompt (prose)

> Which 20 practices should our pharmacists visit about antibiotic prescribing? Follow the memo: STAR-PU-weighted denominators, an
> overdispersion-adjusted standardized excess, and the eligibility rule. Provide `practice_ranking.csv` (practice: items, list, STAR-PU, R, z,
> rank), `funnel_plot.png` (R against STAR-PU with adjusted limits), and a one-page `visit_list.pdf` showing how the dashboard's top ten fare.

## 9. Deliverables

* `practice_ranking.csv`, `funnel_plot.png`, `visit_list.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 practices + #21; R̄ and φ; STAR-PU and z for 6 practices; dashboard contrast; merger handling.

## 11. Golden-output checklist

* BNF filter; settings; weights; φ by winsorisation; eligibility; ranking.

## 12. Build notes (scope tuning)

* Choose a board with a mix of retirement and young urban practices.
* Confirm ≥ 5 of the dashboard's top ten drop out.
