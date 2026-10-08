# DA19 — Attrition rates: the denominator is average headcount, and a transfer is not a loss to the enterprise

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | People-analytics dashboards at large companies (attrition by org, function and level; internal mobility counted as exits at the team level) |
| Domain | Human resources / public workforce |
| Task shape | 07 · Grid of cells (12 agencies × 3 occupational groups → enterprise attrition rate; the agency–group cell that receives a retention bonus pilot) |
| Core method | Attrition rate = separations ÷ average headcount (mean of start and end, or monthly average per memo); separate quits, retirements and transfers; agency-level rates count transfers out; government-wide (enterprise) rates exclude inter-agency transfers |
| Analytical stump | Dividing by end-of-year headcount inflates rates for shrinking units and deflates them for growing ones; counting inter-agency transfers as separations treats internal mobility as attrition, so the enterprise total is not the sum of unit-level losses. The pilot targets enterprise losses |
| Primary sources | U.S. Office of Personnel Management FedScope / Federal Workforce Data (employment cubes and separations/accessions data) |

## 1. The real-world situation

A federal workforce office will fund a retention-bonus pilot in one agency–occupational-group cell with the highest rate of losses to the
federal government. The dashboard computed separations ÷ September headcount and included transfers to other agencies. The top cell was a
small agency whose staff had mostly moved to a sister agency during a reorganisation.

## 2. The decision (one deterministic recommendation)

**The agency × occupational-group cell receiving the pilot, with its enterprise attrition rate and the rates on the dashboard's basis.**

Rules (workforce memo):

* Data: OPM separations and employment data for the fiscal year in the memo; 12 agencies and 3 occupational groups (by PATCO category or
  occupational family per the memo's mapping).
* Headcount: average of on-board counts at the start (prior September) and end (September) of the fiscal year, permanent full-time
  employees.
* Separation types: quits, retirements, RIF/termination, transfers out (inter-agency), deaths, other — as classified in the data.
* Enterprise attrition rate = (quits + retirements + RIF/termination + other, excluding inter-agency transfers and deaths) ÷ average
  headcount.
* Eligibility: average headcount ≥ 500.
* Pilot: eligible cell with the highest enterprise attrition rate (ties → larger headcount).

## 3. Why capable analysts get it wrong

* End-of-period headcount is the most visible denominator.
* Inter-agency transfers are losses for the agency but not for the enterprise.
* Reorganisations create transfer spikes that mimic attrition.
* Small cells produce volatile rates.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `SEPDATA_FY<yy>.txt` (separations cube) | Text | ~250k | OPM FedScope / data.opm.gov | U.S. Gov public domain | Separations by type, agency, occupation |
| 2 | `FACTDATA_<yyyymm>_start.txt` | Text | ~2M | OPM | Public domain | Employment at start |
| 3 | `FACTDATA_<yyyymm>_end.txt` | Text | ~2M | OPM | Public domain | Employment at end |
| 4 | `DTsep.txt`, `DTagy.txt`, `DTocc.txt` (lookups) | Text | ~3k | OPM | Public domain | Code tables |
| 5 | `fedscope_cube_definitions.pdf` | PDF | — | OPM | Public domain | Definitions |
| 6 | `occupational_group_map.csv` | CSV | ~650 | Task author | — | Occupation → group |
| 7 | `workforce_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `dashboard_attrition.xlsx` | XLSX | 36 | Task author | — | Dashboard rates |
| 9 | `reorganisation_notes.json` | JSON | ~3 | Task author (public announcements) | — | Context |
| 10 | `agency_scope.json` | JSON | 12 | Task author | — | Agencies |

## 5. Deterministic solution path

1. Filter permanent full-time; map occupations; select agencies.
2. Average headcount per cell.
3. Classify separations; enterprise and agency rates; eligibility.
4. Select the pilot cell; contrast with the dashboard.

## 6. Wrong paths (method errors, not misreadings)

**A — end-of-year denominator.** Shrinking units inflated.

**B — transfers as attrition.** Reorganisation flagged.

**C — deaths included.** Not retention-relevant per memo.

**D — no headcount floor.** Tiny cells win.

## 7. Why the stump is analytical, not semantic

Separation types and formulas are defined. The trap is denominator choice and enterprise versus unit-level aggregation.

## 8. Draft task prompt (prose)

> Which agency and occupational group should get the retention-bonus pilot? Compute enterprise attrition rates on average headcount per the
> workforce memo. Provide `attrition_grid.csv` (cell: headcount, separations by type, enterprise rate, dashboard rate), `attrition_heatmap.png`,
> and a one-page `pilot_selection.pdf`.

## 9. Deliverables

* `attrition_grid.csv`, `attrition_heatmap.png`, `pilot_selection.pdf`.

## 10. Where 25+ rubric criteria come from

* 36 cells' enterprise rates (sampled 24); selection; dashboard contrast; transfer share in the dashboard's top cell.

## 11. Golden-output checklist

* Population filter; average headcount; separation classification; floor; selection.

## 12. Build notes (scope tuning)

* Choose a fiscal year with a known reorganisation in one agency; confirm the dashboard's top cell is not the pilot cell.
