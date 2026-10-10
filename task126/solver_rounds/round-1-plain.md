# solver round: round 1, plain

**Proxy score 46.0 / 100** (recommendation 0.0 of 35, instruction 7.0 of 7, asks 39.0 of 58). Main call missed. 3 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: Print 28.9 months as the median pendency of FY2022 filings.

solver: Report the median pendency of FY2022 filings as 34.0 months (1,035 days divided by 30.4375). This is measured per application across 57,418 FY2022 filings: each application is followed along its CX re-docket chain to the final decision (the notice-of-allowance date for allowances, the close date for refusals and abandonments), and the 15.8% still undecided at the 30 September 2026 extract count as still waiting. Thomas Kennedy's docket-pendency series should not be the basis, because it describes dockets rather than applications.

tokens matched 0 of 2 (28.9, Print)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| fy2022_pendency_headline.docx | 1 | 2 | 2 | 100% |
| fy2022_pendency_headline.docx | 2 | 27 | 50 | 54% |
| fy2022_pendency_headline.docx | 3 | 2 | 3 | 67% |
| fy2022_time_to_decision.svg | 1 | 1 | 2 | 50% |
| fy2022_time_to_decision.svg | 2 | 1 | 1 | 100% |
| fy2022_time_to_decision.svg | 3 | 2 | 2 | 100% |
| fy2022_time_to_decision.svg | 4 | 2 | 3 | 67% |
| fy2022_time_to_decision.svg | 5 | 0 | 3 | 0% |

## Solver's path

1. Read the charter and the report notes. The headline is the median number of days from filing to the office's final decision, for applications filed 1 Oct 2021 to 30 Sep 2022. A month is 30.4375 days. Undecided applications count as still waiting. Group tables use the art unit that docketed the application at filing, mapped to the group structure in force at the extract, and every application stays in the denominator.
2. examination_dockets plus docket_links: CX children (373,996 links) are re-dockets of the same application, while CN and DV children are new applications. An application is any docket that is not a CX child. Filtering to docketed_on in FY2022 gives 57,418 applications, all numbered 22-. Of these, 33,204 have no CX re-docket and 24,214 have one to three.
3. Each application was followed along its CX chain to the terminal docket. The decision date is the NOA served_on date from office_actions when the terminal docket is ALW or open with an NOA, and closed_on when the terminal docket is REF or ABN. A terminal docket that is open with no NOA is undecided.
4. Calibrated against the Saravel acknowledgements: all 6,300 programme cases match on decision date or open status (the allowance date is the NOA date, not the grant date), and all 16 quarterly medians reproduce exactly, using np.median with undecided cases counted as infinite.
5. Headline: the median of FY2022 days, with undecided cases as infinite, is 1,035 days, or 34.0 months. 48,341 applications are decided; 15.8% are undecided; 54.4% were decided within 36 months.
6. Technology group: the docketing art unit is the from_au of the first entry in docket_transfers (the transfer chains are consistent), otherwise the docket's art_unit. It is mapped through the art_unit_groups row with a blank valid_to. Lower quartile uses linear interpolation (2800 gives 24.8 to 24.9 depending on the quantile convention; 24.9 under the linear, Hazen and averaged conventions). Median and share within 36 months (days/30.4375 <= 36) are computed over all applications in each group.

confidence: high for the headline 34.0 months, the 15.8% undecided share and the group medians (the Saravel reconciliation is exact); medium-high for the 2800 lower quartile, which depends on the quantile convention (24.9 vs 24.8)

notes: The docket tg code (the group at opening) differs from the restated group because of the FY2024 art-unit regrouping; I used the restated group as the report notes require. The lower-quartile convention is not specified anywhere in the folder.

### fy2022_pendency_headline.docx (solver's answers)
- headline median pendency, FY2022 filings: 34.0 months (1,035 days; 57,418 applications, 48,341 decided at 30 Sep 2026)
- 1600 Biotechnology and Organic Chemistry: lower quartile 19.5 months; median 27.7 months; decided within 36 months 70.9% (n=5,749)
- 1700 Chemical and Materials Engineering: lower quartile 21.2 months; median 30.4 months; decided within 36 months 63.6% (n=6,326)
- 2100 Computing and Software: lower quartile 22.4 months; median 31.6 months; decided within 36 months 60.5% (n=9,233)
- 2400 Networks and Communications: lower quartile 23.8 months; median 33.7 months; decided within 36 months 54.9% (n=8,022)
- 2600 Electrical Systems and Imaging: lower quartile 25.0 months; median 35.4 months; decided within 36 months 51.1% (n=6,930)
- 2800 Semiconductors and Optics: lower quartile 24.9 months; median 35.4 months; decided within 36 months 51.1% (n=6,800)
- 3600 Transport, Construction and Commerce: lower quartile 26.6 months; median 37.7 months; decided within 36 months 46.4% (n=6,885)
- 3700 Mechanical Engineering and Medical Devices: lower quartile 29.0 months; median 41.0 months; decided within 36 months 39.6% (n=7,473)
- share of all FY2022 filings undecided at the September 2026 extract: 15.8%
- all-groups lower quartile and share within 36 months (context): lower quartile 23.8 months; decided within 36 months 54.4%

### fy2022_time_to_decision.svg (solver's answers)
- title figure / median marked on the curve: Median 34.0 months, where the cumulative decided share crosses the 50% line
- undecided share annotated where the curve stops: 15.8% undecided; the curve stops at 84.2% decided, with the last decision at about 59.7 months after filing
- reference line: 50% horizontal line; step curve of the cumulative share decided by month after filing, with all 57,418 FY2022 filings as the denominator
