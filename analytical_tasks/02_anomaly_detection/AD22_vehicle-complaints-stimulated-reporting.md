# AD22 — Vehicle complaint spikes: an emerging defect, or an echo of the evening news?

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Automaker field-quality early-warning teams and the regulator's defect screening (the complaint surges around unintended acceleration and ignition-switch cases) |
| Domain | Automotive safety / field quality |
| Task shape | 18 · Hypotheses versus evidence (8 spiking make–model–component groups × lines of evidence → the one group sent to a preliminary engineering evaluation) |
| Core method | Re-index complaints from date received to date of incident; measure the share of "old" incidents in a spike (stimulated reporting); normalize incident-date counts by vehicles in service at the same vehicle age (EWR production volumes); compare with the same component on sister model years |
| Analytical stump | Counting complaints by the date they arrive makes every recall, news story or lawsuit look like a new failure wave: owners report incidents from years ago. The emerging defect is the group whose *incident-date* rate per vehicle rises at a vehicle age where sister model years stayed flat — often not the loudest spike |
| Primary sources | NHTSA Office of Defects Investigation complaints flat file (FLAT_CMPL), recalls flat file (FLAT_RCL), investigations file (FLAT_INV); NHTSA Early Warning Reporting (EWR) public production and aggregate claims data |

## 1. The real-world situation

A manufacturer's field-quality group watches public complaint filings weekly. Last quarter, eight make–model–component groups more than
doubled their monthly complaint counts. Engineering can open **one** preliminary evaluation this quarter. The analyst ranked the eight by
growth in complaints received and recommended the top group; the safety director wants to know whether any of the spikes is a genuinely
new failure mode rather than reporting stimulated by publicity.

## 2. The decision (one deterministic recommendation)

**The single make–model–component group that receives the preliminary evaluation, and the incident-rate increase that justifies it.**

Rules (field-quality memo):

* Candidate groups: the 8 listed in `spike_candidates.csv` (make, model, model-year range, ODI component text).
* Evidence lines, each pass/fail per group:
  1. **Recency (H: new failures).** Of complaints received in the spike window, the share with incident date within the previous 180 days
     is ≥ 60%.
  2. **Publicity (H: stimulated reporting).** A recall, investigation or campaign for the same make and component was opened within 120
     days before the spike window starts (from FLAT_RCL / FLAT_INV).
  3. **Incident-date rate.** Incidents per 100,000 vehicles in service, by incident month, rose by ≥ 50% versus the group's own trailing
     12-month average, with vehicles in service = EWR production for the model years in scope.
  4. **Age-matched contrast.** At the same vehicle age (months since model-year start), the rate exceeds the sister model years' rate by
     ≥ 50%.
  5. **Dispersion.** Incidents are spread across ≥ 15 states (not a single dealer cluster or lawsuit filing).
* A group is "emerging" if evidence 1, 3, 4 and 5 pass and evidence 2 fails or passes only with evidence 1 also passing. Choose the
  emerging group with the largest age-matched rate ratio.

## 3. Why capable analysts get it wrong

* Complaint counts arrive by date received; that is the series dashboards show.
* After publicity, owners file reports about incidents from months or years earlier; arrivals spike while incident rates do not.
* Raw counts grow with fleet size and age; a popular model with more vehicles on the road complains more without being worse.
* Defects that emerge with age need an age-matched comparison against other model years of the same platform.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `FLAT_CMPL.txt` | Tab-delimited text | ~2M complaints | NHTSA ODI downloadable files | U.S. Gov public domain | Complaints with incident date, received date, state, component |
| 2 | `CMPL.txt` (field layout) | Text | — | NHTSA | Public domain | Field definitions |
| 3 | `FLAT_RCL.txt` | Tab-delimited text | ~300k | NHTSA ODI | Public domain | Recall campaigns |
| 4 | `FLAT_INV.txt` | Tab-delimited text | ~10k | NHTSA ODI | Public domain | Investigations (PE, EA, RQ) |
| 5 | `ewr_production_by_make_model_my.csv` | CSV | ~60k | NHTSA EWR public data | Public domain | Production volumes |
| 6 | `ewr_aggregate_claims.csv` | CSV | ~200k | NHTSA EWR public data | Public domain | Warranty/field-report counts by component code (context) |
| 7 | `spike_candidates.csv` | CSV | 8 | Task author (from complaint arrivals) | — | Groups in scope |
| 8 | `component_text_map.json` | JSON | ~150 | Task author | — | ODI component strings → component families |
| 9 | `field_quality_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `analyst_growth_ranking.xlsx` | XLSX | 8 | Task author | — | Received-date growth ranking |
| 11 | `vehicle_age_calendar.parquet` | Parquet | ~100k | Derived | — | Model year × month → vehicle age |

## 5. Deterministic solution path

1. Filter complaints to each group; tabulate received-date and incident-date monthly counts.
2. Recency share for complaints received in the spike window.
3. Find recalls/investigations for the same make and component family opened in the 120 days before the spike.
4. Incident-date rate per 100k vehicles; trailing-12-month comparison.
5. Age-matched rate versus sister model years; state dispersion.
6. Fill the 8 × 5 evidence grid; apply the rule; choose the group.

## 6. Wrong paths (method errors, not misreadings)

**A — ranking by complaints received.** Picks a publicity echo.

**B — incident counts without exposure.** Picks the highest-volume model.

**C — no age matching.** Confuses ordinary wear-out with a new failure mode.

**D — dropping complaints with blank incident dates silently.** Changes recency shares; the memo's rule (exclude and report the
count) must be applied and disclosed.

## 7. Why the stump is analytical, not semantic

Dates, components and rules are explicit. The trap is the time index (arrival versus occurrence) and the denominator — the classic
surveillance distinction between reporting rate and event rate.

## 8. Draft task prompt (prose)

> Eight complaint groups spiked last quarter and we can open one engineering evaluation. Using NHTSA complaints, recalls, investigations
> and EWR production, work through the evidence grid in the field-quality memo and tell me which group gets the evaluation. Provide
> `evidence_grid.csv` (group × evidence line: value, pass/fail), `received_vs_incident.png` (small multiples of complaints by received and by
> incident month per group, with recall dates marked), and a one-page `evaluation_decision.pdf` naming the group, its age-matched rate
> ratio, and why the loudest spike was not chosen.

## 9. Deliverables

* `evidence_grid.csv`, `received_vs_incident.png`, `evaluation_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 groups × 5 evidence cells = 40; chosen group; its rate ratio; treatment of blank incident dates; contrast with the analyst ranking.

## 11. Golden-output checklist

* Incident-date re-indexing; recency share; publicity lookup by component family; exposure from EWR; age matching; rule application.

## 12. Build notes (scope tuning)

* Choose candidate groups so that the top received-date spike follows a recall announcement and fails recency, while a quieter group passes
  all evidence lines.
* Freeze the flat-file download date; ODI files are updated daily.
