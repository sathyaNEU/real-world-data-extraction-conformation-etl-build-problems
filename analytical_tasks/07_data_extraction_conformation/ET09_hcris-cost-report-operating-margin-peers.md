# ET09 — Hospital margin peers from Medicare cost reports: one hospital, three reports, two periods

| Field | Value |
|---|---|
| Domain | Hospital finance / health-system strategy / benchmarking |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (top-5 best-practice peers) |
| Core technique | Report-version supersession; combining split cost-reporting periods at component level; worksheet/line/column coordinate extraction; provider-type eligibility from CCN ranges |
| Trap family (honest data) | Duplicate report versions summed; short periods after a change of ownership picked alone or margin-averaged; wrong year file loaded |
| Primary sources | CMS HCRIS Hospital 2552-10 cost report files (RPT, NMRC, ALPHA) |

## 1. The real-world project

A health system's CFO wants five **best-practice peers**: the in-state short-term acute hospitals with ≥100 staffed
beds and the highest operating margin for cost-reporting periods ending in 2022. The analyst loaded the 2022 HCRIS
files, pivoted Worksheet G-3, computed margin = line 5 ÷ line 3, and took the top five. Two of the five had margins above
25%; one had changed ownership mid-year.

## 2. The business decision (one deterministic recommendation)

**Which five hospitals are the CFO's best-practice peers, and which hospital is sixth?**

Rules (benchmarking method):

* Eligible: CCN facility-type digits in the short-term acute range (0001–0879), in-state, ≥100 beds per Worksheet S-3
  Part I (cell specified in the method), at least one cost-reporting period ending in calendar 2022.
* Version: for each `(PRVDR_NUM, FY_BGN_DT, FY_END_DT)` keep only the report with the latest `PROC_DT`.
* Periods: if a provider has more than one period ending in 2022 (change of ownership or fiscal-year change), **sum the
  dollar components** across those periods before computing the margin. Never annualize; never average margins.
* Operating margin = (G-3 line 3 net patient revenue − G-3 line 4 total operating expenses) ÷ G-3 line 3.
* Rank descending; ties by higher net patient revenue.

## 3. Why this gets overlooked in real projects

* HCRIS looks like a fact table, but each `RPT_REC_NUM` is one *version* of one *period*; amended, reopened and settled
  versions coexist. Pivoting without supersession sums versions.
* A change of ownership splits a year into two short reports. Taking one of them — often the profitable half — or
  averaging the two margins produces extreme values that rise to the top of a ranking.
* Line and column codes are zero-padded strings (`00300`); casting to integers and back, or reading the wrong worksheet
  code, silently picks sub-lines or other worksheets.
* Year files group reports by a fiscal-year convention, so a period ending in 2022 may sit in the adjacent year's file.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–3 | `HOSP10_2021_RPT.CSV`, `HOSP10_2021_NMRC.CSV`, `HOSP10_2021_ALPHA.CSV` | CSV | NMRC ≈ 20–30M | CMS Cost Reports (HCRIS) | U.S. Gov public domain | Reports that may end in 2022 |
| 4–6 | `HOSP10_2022_RPT.CSV`, `HOSP10_2022_NMRC.CSV`, `HOSP10_2022_ALPHA.CSV` | CSV | NMRC ≈ 20–30M | CMS | Public domain | Main year |
| 7 | `HCRIS_file_layout_2552-10.pdf` | PDF | — | CMS | Public domain | RPT/NMRC/ALPHA layouts, status codes |
| 8 | `PRM_15-2_chapter40_G3_S3_instructions.pdf` | PDF | — | CMS Provider Reimbursement Manual | Public domain | Line/column meanings |
| 9 | `pos_hospital_2022q4.csv` (Provider of Services file) | CSV | ~7k hospitals | CMS POS | Public domain | Names, state, CHOW dates |
| 10 | `ccn_facility_type_ranges.xlsx` | XLSX | ~30 | CMS State Operations Manual extract | Public domain | Eligibility |
| 11 | `hospital_general_information.json` | JSON | ~5k | CMS Provider Data Catalog | Public domain | Hospital type cross-check |
| 12 | `benchmark_method.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Load RPT from both years; filter `FY_END_DT` in 2022; dedupe versions on latest `PROC_DT`.
2. Apply CCN range, state and bed eligibility (beds from NMRC at the specified S-3 cell, summed across periods using the
   method's rule — e.g. the longest period's beds).
3. Pull G-3 lines 3 and 4 (column 1) for retained reports; sum per provider across 2022-ending periods.
4. Compute margins; rank; top five + sixth.
5. Recompute under the naive path (no dedupe; first or single period; margin averaging) to show differences.

## 6. The traps

**Trap A — versions summed.** Revenues and expenses double for amended hospitals; margin unchanged if both double, but
when only one version has a corrected expense line, margin jumps.

**Trap B — split periods.** Taking the post-acquisition short period alone (or averaging two margins) catapults a CHOW
hospital into the top five.

**Trap C — single year file.** Hospitals whose 2022-ending period sits in the other file disappear, opening a top-five slot.

**Trap D — CAHs / specialty hospitals.** Including critical-access or specialty CCNs that fail eligibility.

## 7. Why the data is honest

HCRIS reproduces each submitted and settled cost report exactly. Multiple versions and short periods are normal,
documented features of the Medicare cost-reporting process.

## 8. Draft task prompt (prose)

> The CFO wants five best-practice peers: in-state short-term acute hospitals with at least 100 beds and the highest
> operating margin for cost-reporting periods ending in 2022, following our benchmarking method. Using the HCRIS files
> in the folder, tell me the five and the hospital that just missed. Build `margin_peers.xlsx` listing every eligible
> hospital with the reports used (record numbers, period dates, status), net patient revenue, operating expenses, margin
> and rank. Add `margin_ranking.png`, a ranked dot plot of all eligible hospitals with the top five highlighted and the
> hospitals that had more than one 2022 period marked. In the workbook's cover sheet, state the five, the margin gap
> between fifth and sixth, and for any hospital with a change of ownership, what its margin would have been if only its
> latest short period had been used.

## 9. Deliverables

* `margin_peers.xlsx` (cover + detail), `margin_ranking.png`.

## 10. Where 25+ rubric criteria come from

* Top 5 + 6th + gap; margins for ~10 named hospitals; report record numbers used for 3 multi-version hospitals; CHOW
  hospital combined vs short-period margin; eligibility exclusions.

## 11. Golden-output checklist

* Latest-processed version per period; split periods summed at component level; both year files loaded; eligibility
  applied; decision stated.

## 12. Build notes (scope tuning)

* Pick a state with ≥25 eligible hospitals including at least one CHOW in 2022 and several amended reports; confirm the
  naive top five differs.
* Specify the exact S-3 bed cell (worksheet code, line, column) in the method memo after checking the 2552-10 layout.
