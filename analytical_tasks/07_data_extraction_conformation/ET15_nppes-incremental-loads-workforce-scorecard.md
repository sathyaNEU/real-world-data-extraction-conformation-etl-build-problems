# ET15 — Behavioral-health workforce designation from NPPES: monthly snapshots, weekly deltas and dark records

| Field | Value |
|---|---|
| Domain | State Medicaid / workforce policy / provider master data management |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 10 · Scorecard against thresholds (county × workforce metric) |
| Core technique | Snapshot + incremental (upsert) + deactivation replay to an as-of date; primary-attribute selection from repeating column groups; address-role selection and ZIP→county assignment |
| Trap family (honest data) | Weekly files appended instead of upserted; deactivated "dark" NPIs counted; any-taxonomy matching; mailing address used |
| Primary sources | CMS NPPES Data Dissemination files (monthly full, weekly incremental, deactivation report, practice-location file), NUCC taxonomy, HUD ZIP–county crosswalk, Census population estimates |

## 1. The real-world project

A state Medicaid agency launches a loan-repayment pilot for behavioral-health prescribers. A county qualifies if it fails
at least two of three workforce ratios. The provider master is rebuilt from NPPES: the monthly full replacement file plus
weekly incremental files to reach the program's as-of date. The first build qualified the pilot county; a provider
association showed that the county's count included retired and deactivated clinicians and providers who only *mail*
from there.

## 2. The business decision (one deterministic recommendation)

**Does the pilot county qualify for designation as of 2024-06-30?**

Rules (designation standard):

* Build the NPI master as of 2024-06-30: start from the June monthly full file, **upsert** each weekly incremental file in
  date order by NPI (latest record wins), then remove NPIs deactivated on or before the as-of date unless reactivated
  after the deactivation and on or before the as-of date.
* Individuals only (`Entity Type Code = 1`).
* Specialty from the taxonomy slot whose `Healthcare Provider Primary Taxonomy Switch_n = Y`:
  M1 psychiatrists (2084P0800X and its psychiatry subspecialty codes listed in the standard) per 100k residents;
  M2 child & adolescent psychiatrists (2084P0804X) per 100k residents under 18;
  M3 psychiatric/mental-health nurse practitioners (363LP0808X) per 100k residents.
* County from the **primary practice location** ZIP (5-digit) via the HUD ZIP–county file of the as-of quarter, choosing the
  county with the largest `BUS_RATIO` (ties: lowest county FIPS). Secondary practice locations are ignored.
* Thresholds: M1 < 10.0, M2 < 15.0, M3 < 8.0 (per 100k) count as failures. Qualifies if ≥ 2 failures.
* Report the same scorecard for the pilot county's neighbours for context.

## 3. Why this gets overlooked in real projects

* Weekly incremental files have the same layout as the full file, so engineers `UNION` them; changed providers then exist
  twice — once with the old address and taxonomy, once with the new.
* Deactivated NPIs remain in the full file as **dark records** (NPI and dates populated, everything else blank), and
  reactivations carry both dates — row filters on blank names or on deactivation date alone get these wrong.
* Fifteen taxonomy slots invite "any slot matches" logic; many clinicians list secondary taxonomies they do not practise.
* The mailing address is often the billing office or home, in a different county.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `npidata_pfile_20240603-20240609.csv` (monthly full, state-filtered) | CSV | 0.3–1M (state) | CMS NPPES | U.S. Gov public domain | Snapshot |
| 2–5 | `npidata_pfile_2024061x-2024063x.csv` (weekly incrementals) | CSV | 5k–20k each | CMS NPPES | Public domain | Deltas |
| 6 | `NPPES_Deactivated_NPI_Report_202407.xlsx` | XLSX | ~300k | CMS NPPES | Public domain | Deactivations |
| 7 | `pl_pfile_20240603-20240609.csv` | CSV | ~0.5M | CMS NPPES | Public domain | Secondary locations (to be ignored, but present) |
| 8 | `NPPES_Data_Dissemination_Readme.pdf` + code values | PDF | — | CMS | Public domain | Dark records, reactivation semantics |
| 9 | `nucc_taxonomy_241.csv` | CSV | ~880 | National Uniform Claim Committee | NUCC terms (free use with attribution; verify) | Taxonomy codes |
| 10 | `ZIP_COUNTY_062024.xlsx` | XLSX | ~54k | HUD USPS crosswalk | Public domain (registration) | ZIP → county |
| 11 | `co-est2023-alldata.csv` + `cc-est2023-agesex.csv` | CSV | ~3k / ~70k | Census Population Estimates | Public domain | Total and under-18 population |
| 12 | `designation_standard.pdf` | PDF | — | Task author | — | Rules in §2 |

## 5. Deterministic solution path

1. Load the full file; upsert weeklies in order by NPI; apply deactivation/reactivation logic as of 2024-06-30.
2. Keep Type 1; pick the primary taxonomy; classify M1–M3.
3. Assign county from primary practice ZIP via max `BUS_RATIO`.
4. Count per county; compute ratios with the right denominators; compare to thresholds; count failures.
5. Decide for the pilot county; show neighbours; show counts under the union/any-slot/mailing variants.

## 6. The traps

**Trap A — union of weeklies.** Providers who moved into or out of the county appear in both; counts inflate.

**Trap B — dark records kept.** Deactivated NPIs with lingering taxonomy fields (from a prior snapshot) or reactivated
NPIs dropped; counts move across a threshold.

**Trap C — any taxonomy slot.** Adds primary-care physicians listing psychiatry as secondary; M1 passes.

**Trap D — mailing address / secondary locations.** Moves clinicians into the pilot county.

**Trap E — wrong denominator.** Using total population for M2.

## 7. Why the data is honest

NPPES is the official enumeration record; dark records, reactivations, weekly deltas and primary switches are all
documented. Each file is correct for its date.

## 8. Draft task prompt (prose)

> The pilot county gets the loan-repayment designation only if it fails at least two of the three workforce ratios in our
> designation standard as of 30 June 2024. Using the NPPES snapshot, weekly files, deactivation report and the
> crosswalk and population files in the folder, rebuild the provider master as of that date and tell me whether the
> county qualifies. Provide `workforce_scorecard.xlsx` with a row per county (pilot and neighbours) showing provider
> counts, populations, the three ratios, pass/fail against each threshold and the failure count; and `scorecard_grid.png`,
> a county-by-metric grid coloured by pass/fail with ratios printed. In the workbook's first sheet, state the decision,
> the binding metric and how many providers it would take to change it.

## 9. Deliverables

* `workforce_scorecard.xlsx`, `scorecard_grid.png`.

## 10. Where 25+ rubric criteria come from

* ~8 counties × 3 metrics (counts, ratios, pass/fail); pilot decision; binding metric; providers-to-flip figure.

## 11. Golden-output checklist

* Upsert replay, deactivation/reactivation, primary taxonomy, primary practice ZIP → county by BUS_RATIO, correct
  denominators; decision stated.

## 12. Build notes (scope tuning)

* Pick a county near the M1/M3 thresholds; verify that union-of-weeklies and any-slot each flip at least one metric.
* NPPES file naming and weekly cadence are fixed by CMS — record exact file names and dates downloaded.
