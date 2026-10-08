# DA10 — How long do credit unions last? A panel that starts in 1994 cannot see the ones that died before

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Customer- and account-lifetime analysis on CRM or billing systems migrated at a date (only accounts alive at migration are present), device-fleet lifetimes from a registry snapshot |
| Domain | Financial institutions / industry structure |
| Task shape | 14 · Cuts of a distribution (median and quartiles of institution lifetime by size class; the planning horizon the trade association adopts) |
| Core method | Kaplan–Meier with left truncation (delayed entry): each institution enters the risk set at its age on the first observed quarter (charter date to panel start), exits at merger/liquidation or is censored at the last quarter; comparison with naive KM from charter date ignoring truncation |
| Analytical stump | The call-report panel only contains credit unions alive at its start. Treating their age at entry as if they had been observed since charter counts years they could not have died in (immortal time), so survival is overstated. Delayed-entry risk sets correct it |
| Primary sources | NCUA quarterly Call Report data (5300) bulk files; NCUA merger and liquidation records |

## 1. The real-world situation

A credit-union trade association advises new charters on how long institutions in each size class typically remain independent before
merging or liquidating. Its analyst computed survival from charter dates for all credit unions appearing in the quarterly call-report files
since 1994 and reported a median independent lifetime above 70 years for small credit unions. Board members who had watched hundreds of small
credit unions merge in the 1990s found that implausible.

## 2. The decision (one deterministic recommendation)

**The median and interquartile lifetimes (years from charter to exit) by size class, and the planning horizon adopted for small credit
unions (the lower quartile lifetime, rounded down to whole years).**

Rules (research memo):

* Panel: quarterly call reports from 1994Q1 to the latest quarter in the memo; one record per charter number per quarter.
* Exit: last quarter observed before the latest quarter, with exit reason from the merger/liquidation file (merger, purchase and assumption,
  liquidation); others censored at the latest quarter.
* Charter date: from the institution profile; age at entry = (first observed quarter − charter date).
* Size class: total assets at first observed quarter, deflated to 2020 dollars; classes < $10M, $10–100M, ≥ $100M.
* Estimator: Kaplan–Meier on age scale with delayed entry at age at entry.
* Quartiles from the KM curve (first age where S ≤ 0.75, 0.5, 0.25); "not reached" if never.

## 3. Why capable analysts get it wrong

* Lifetime from charter seems natural when charter dates exist.
* Institutions that exited before the panel start are invisible; survivors are selected.
* Without delayed entry, each survivor contributes risk time from charter onward, inflating survival.
* Inflation-adjusted size classes matter over three decades.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–120 | `call-report-data-<yyyy>-<mm>.zip` (quarterly, 1994 onward) | CSV inside ZIP | ~5–12k institutions per quarter | NCUA | U.S. Gov public domain | Panel |
| 121 | `FOICU.txt` (institution profile per quarter) | Text | ~5–12k per quarter | NCUA | Public domain | Charter number, charter date, assets |
| 122 | `ncua_mergers_liquidations.xlsx` | XLSX | ~6k | NCUA merger/insurance reports | Public domain | Exit reasons |
| 123 | `cpi_u_annual.csv` | CSV | ~35 | BLS CPI-U | Public domain | Deflator |
| 124 | `research_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 125 | `analyst_naive_km.xlsx` | XLSX | 3 | Task author | — | Naive results |
| 126 | `call_report_account_descriptions.pdf` | PDF | — | NCUA | Public domain | Field definitions |
| 127 | `institution_spells.parquet` | Parquet | ~12k | Derived | Public domain | One row per charter: entry, exit, reason |
| 128 | `km_delayed_entry_check.json` | JSON | ~8 | Task author | — | Toy example values |

## 5. Deterministic solution path

1. Build spells per charter: first and last quarter, exit reason, charter date, entry assets.
2. Deflate assets; assign size classes.
3. KM with delayed entry by class; quartiles.
4. Naive KM for contrast; planning horizon.

## 6. Wrong paths (method errors, not misreadings)

**A — KM from charter ignoring delayed entry.** Survival overstated.

**B — only institutions chartered after 1994.** Discards information; young cohorts only.

**C — nominal size classes.** Class drift over time.

**D — treating the latest quarter as exit.** Censoring confused with exits.

## 7. Why the stump is analytical, not semantic

The spells, estimator and classes are defined. The trap is selection by survival to the panel start — left truncation.

## 8. Draft task prompt (prose)

> How long do credit unions of each size typically stay independent? Use the call-report panel and the delayed-entry estimator in the research
> memo, and give the planning horizon for small credit unions. Provide `lifetime_quartiles.csv` (class: institutions, exits, Q1, median, Q3 —
> corrected and naive), `survival_curves.png`, and a one-page `lifetime_brief.pdf`.

## 9. Deliverables

* `lifetime_quartiles.csv`, `survival_curves.png`, `lifetime_brief.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 classes × (Q1, median, Q3) corrected and naive = 18; counts; planning horizon; toy check.

## 11. Golden-output checklist

* Spell construction; deflation; delayed entry; quartile reading; horizon rounding.

## 12. Build notes (scope tuning)

* Confirm the naive median for small credit unions exceeds the corrected one by ≥ 20 years.
