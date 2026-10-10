# task126 · Morvane Patent Office, FY2022 headline pendency

## Tags

**Domain:** Policy & Education (public administration: a national patent office's statutory headline pendency, filed in its annual performance report to the Minister for Enterprise).
**Analytical objective:** Descriptive & Distribution Analysis (the distribution of time from filing to final decision for one fiscal year's applications, built from a docket-keyed production extract, with its median, lower quartile and 36-month share by technology group and the share still undecided).

## 1. Final Recommendation

**Print 28.9 months as the median pendency of FY2022 filings.**

It is the Kaplan-Meier median, 880 days, of filing to final decision over the 66,186 FY2022 applications. Not examiner docket pendency, which times dockets and ends an allowed docket at the grant. Not dockets ended at their decision notice, which takes a refusal whose file went on to a new docket as a final decision. Not CX dockets censored at the transfer, which never counts the decision a re-examined application reached. Not every CX docket chained into its parent, which reads continuing applications (first action credited 1N) as re-examinations, leaves them out of FY2022 and runs their parents on past the refusal that decided them.

## 2. Critical Components

1. FY2022 filings are **66,186** applications: **57,418** dockets opened in FY2022 not on a transferred file and **8,768** CX successor dockets opened in FY2022 whose first action on the merits is credited **1N**
2. **10.6%** of FY2022 filings are undecided at the 30 September 2026 extract, none waiting less than **1,461 days (48.0 months)**, so no later decision moves the median
3. The median is **880 days**, **28.9 months** at 30.4375 days a month

## 3. Step-by-Step Solution

1. From `office_actions_FY2016_FY2026.parquet` took each docket's decision notice (its one NOA, REF or ABN action; GRT decides nothing) and its first action on the merits (earliest EXR by `served_on`, then `action_id`), whose `credit_class` (1N or 1R) comes from `examiner_production_ledger_FY2016_FY2026.parquet` on `action_id`.
2. Read each CX edge in `docket_links.csv` by its successor's class: 1R is the same application re-examined, 1N is a new application filed on the successor's `docketed_on` (production standard: 1N is credited once per application; charter: a benefit claim does not move the filing date); CN and DV children are applications of their own.
3. FY2022 applications are the dockets in `examination_dockets_FY2016_FY2026.parquet` with `docketed_on` from 1 October 2021 to 30 September 2022 that are not CX children, plus the CX children there credited 1N: 66,186.
4. Final decision: from the application's docket follow CX edges while the successor is credited 1R and take the last docket's decision notice; where the next successor is credited 1N, the decision is the refusal notice on the docket it leaves; no notice by 30 September 2026 is still waiting at the extract (charter): 10.6% undecided, none under 1,461 days.
5. Days from `docketed_on` to the final decision, Kaplan-Meier with the undecided censored at the extract, months as days over 30.4375 (charter): median 880 days, 28.9 months.
6. Groups (report table notes): the docketing art unit is the `from_au` of the docket's earliest transfer in `docket_transfers.csv` (else its `art_unit`), mapped to the `tg` in force in `art_unit_groups.csv` (blank `valid_to`); per group the Kaplan-Meier lower quartile and median, and the share of all its applications decided within 36 × 30.4375 days of filing.
7. Recommendation: the headline prints 28.9 months.

## 4. Deliverable Answers

### fy2022_pendency_headline.docx

1. Headline sentence: "The median pendency of applications filed in FY2022, from filing to the office's final decision, was 28.9 months."
2. Technology groups, lower-quartile pendency in months, median pendency in months, share decided within 36 months:
   - 1600 Biotechnology and Organic Chemistry: 16.2, 23.4, 79.6%
   - 1700 Chemical and Materials Engineering: 17.5, 25.7, 74.1%
   - 2100 Computing and Software: 18.4, 26.8, 71.6%
   - 2400 Networks and Communications: 19.8, 28.6, 66.1%
   - 2600 Electrical Systems and Imaging: 20.6, 30.0, 63.0%
   - 2800 Semiconductors and Optics: 21.0, 30.6, 62.5%
   - 3600 Transport, Construction and Commerce: 21.8, 31.9, 58.6%
   - 3700 Mechanical Engineering and Medical Devices: 24.0, 35.2, 51.6%
3. Share of all FY2022 filings still undecided at the September 2026 extract: 10.6%

### fy2022_time_to_decision.svg

1. Title stating the figure: "FY2022 filings: median pendency 28.9 months from filing to final decision"
2. Step curve of the share of FY2022 filings decided by each completed month after filing, every filing in the denominator
3. A line at 50 per cent, labelled "50% decided"
4. The median marked on the 50 per cent line and labelled "Median 28.9 months"
5. The undecided share annotated where the curve stops: "10.6% still undecided at the 30 September 2026 extract"
