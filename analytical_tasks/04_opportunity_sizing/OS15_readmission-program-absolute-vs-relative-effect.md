# OS15 — Rolling out a readmission programme: a relative reduction means different absolute gains at each hospital

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Transporting an experiment's effect to new markets or segments (a churn-reduction feature tested in one market applied to others with different base rates) |
| Domain | Hospital quality / care transitions |
| Task shape | 01 · Ranked list under a cap (8 hospitals receiving a transitional-care programme by readmissions avoided per year) |
| Core method | Apply the trial's relative risk (RR) to each hospital's own expected readmission rate for eligible discharges (from the CMS readmission program's predicted/expected rates and volumes): avoided = discharges × rate × (1 − RR); rank by avoided readmissions; compare with applying the trial's absolute risk difference uniformly |
| Analytical stump | The pilot reported "4.2 percentage points fewer readmissions". That absolute difference was measured at a hospital with a high baseline rate; in hospitals with lower baselines the same intervention avoids fewer readmissions. Applying the absolute difference to every hospital — or a national average rate — misallocates the programme |
| Primary sources | CMS Hospital Readmissions Reduction Program (HRRP) supplemental data file (condition-level discharges, predicted and expected readmission rates) |

## 1. The real-world situation

A health system piloted a transitional-care programme in one hospital: heart-failure readmissions fell from 24.0% to 19.8% (RR = 0.825). It can
fund the programme at **8** of its 20 hospitals. The planning team ranked hospitals by heart-failure discharges × 4.2 points.

## 2. The decision (one deterministic recommendation)

**The 8 hospitals funded, ranked by heart-failure readmissions avoided per year, and the 9th.**

Rules (planning memo):

* Data: HRRP supplemental file for the fiscal year in the memo; condition HF; the system's 20 hospitals (CCNs in memo).
* Eligible discharges per year = HRRP discharges for HF ÷ number of years in the performance period.
* Baseline rate = the hospital's predicted readmission rate (memo; uses the HRRP "predicted" rate, which reflects the hospital's own effect).
* Avoided per year = discharges × baseline × (1 − 0.825).
* Hospitals with discharges "Too Few to Report" excluded.
* Rank; top 8; report #9; report the absolute-difference ranking for contrast.

## 3. Why capable analysts get it wrong

* Absolute differences are the headline in pilot reports.
* Relative effects transport more stably across baselines (memo's assumption).
* Volume and baseline both matter; ranking by volume alone ignores baseline differences.
* The HRRP performance period spans multiple years; annualisation is required.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `FY_<yyyy>_Hospital_Readmissions_Reduction_Program_Hospital.csv` | CSV | ~19k (hospital × condition) | CMS Provider Data Catalog | U.S. Gov public domain | Discharges, predicted and expected rates, ERR |
| 2 | `hrrp_supplemental_file_<yyyy>.xlsx` | XLSX | ~3k hospitals | CMS | Public domain | Peer groups, details |
| 3 | `hrrp_methodology_report.pdf` | PDF | — | CMS/Yale CORE | Public domain | Definitions |
| 4 | `system_hospitals.json` | JSON | 20 | Task author | — | Scope |
| 5 | `pilot_results.json` | JSON | — | Task author (pilot figures) | — | RR and absolute difference |
| 6 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `planning_team_ranking.xlsx` | XLSX | 20 | Task author | — | Absolute-difference ranking |
| 8 | `effect_transportability_citation.pdf` | PDF | — | Cite (relative vs absolute effect transport) | Cite | Context |

## 5. Deterministic solution path

1. Filter the system's hospitals and HF rows; exclude too-few rows.
2. Annualise discharges; baseline rates.
3. Avoided readmissions with RR; rank; top 8 + #9.
4. Contrast with the absolute-difference ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — absolute difference applied uniformly.** Overstates low-baseline hospitals.

**B — national average baseline.** Ignores hospital differences.

**C — expected instead of predicted rate.** Removes the hospital's own effect (memo uses predicted).

**D — performance-period totals without annualising.** Scale error (ranking unaffected, totals wrong).

## 7. Why the stump is analytical, not semantic

The effect measure and baseline are specified. The trap is transporting an absolute effect across different baselines.

## 8. Draft task prompt (prose)

> Which eight hospitals should get the transitional-care programme? Translate the pilot's relative effect to each hospital's own baseline as the
> planning memo specifies. Provide `avoided_readmissions.csv` (hospital: discharges, baseline, avoided, rank), `baseline_vs_volume.png`, and a
> one-page `programme_rollout.pdf`.

## 9. Deliverables

* `avoided_readmissions.csv`, `baseline_vs_volume.png`, `programme_rollout.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 hospitals + #9; avoided for 12 hospitals; exclusions; totals; contrast.

## 11. Golden-output checklist

* Filters; annualisation; predicted rate; RR application; ranking.

## 12. Build notes (scope tuning)

* Confirm the absolute-difference ranking differs by at least two hospitals.
