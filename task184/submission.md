## Tags

**Domain:** Accounting, Audit & Forensic (a wholesale group's continuous monitoring of its general ledger: the population exception rate the internal audit plan is sized against).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**15,000 postings in Drumcondra Provisions Group's general ledger tripped the continuous monitoring ruleset in FY26 P1 to P9, to the nearest thousand.**
The platform raised 7,481 journal entries as exceptions over the same window. The two are not alternative counts of one thing: the platform writes one verdict for a journal entry, and an entry in this ledger carries between 1 and 2,347 postings, so the entry count is a count of vouchers. Recovering the posting count means inverting the entry-level indicator entry by entry, on each trading unit's own population.

## 2. Critical Components

1. Postings that tripped the ruleset, group, FY26 P1 to P9: **15,000** (to the nearest thousand; unrounded 14989.3).
2. Journal entries raised as exceptions over the same window: **7,481**.
3. Postings in the window: **1,225,763** across **313,678** journal entries.
4. Postings that tripped the ruleset by trading unit, to the nearest hundred:

| Trading unit | Postings that tripped | Entries raised | Postings |
|---|---|---|---|
| DPG-110 Drumcondra Central Cash and Carry | 1,700 | 792 | 120,384 |
| DPG-120 Finglas Cash and Carry | 2,100 | 920 | 123,438 |
| DPG-130 Naas Road Cash and Carry | 1,500 | 732 | 116,460 |
| DPG-210 Cork Kinsale Road Cash and Carry | 1,300 | 659 | 114,990 |
| DPG-220 Mallow Cash and Carry | 1,100 | 599 | 112,734 |
| DPG-310 Galway Oranmore Cash and Carry | 1,200 | 623 | 114,870 |
| DPG-320 Castlebar Cash and Carry | 1,400 | 695 | 115,806 |
| DPG-410 Limerick Raheen Cash and Carry | 1,000 | 560 | 107,172 |
| DPG-420 Waterford Belview Cash and Carry | 1,600 | 754 | 118,608 |
| DPG-510 National Contracts | 900 | 514 | 89,374 |
| DPG-610 Drumcondra Bakery | 800 | 502 | 68,967 |
| DPG-900 Group Services | 400 | 131 | 22,960 |
| **Group** | **15,000** | **7,481** | **1,225,763** |


## 3. Step-by-Step Solution

1. Read general_ledger_data_dictionary.pdf: a posting is one source document's entry into the ledger and item_count is the number of postings recorded under a journal entry, while line_count is the entry's debit and credit lines. Confirmed on the sampled vouchers in journal_lines that the distinct source_doc_ref on an entry numbers the same as its item_count.
2. Read monitoring_platform_operating_guide.pdf: every posting on an entry is evaluated against every live rule and the platform then writes one verdict for the entry, retaining no posting-level detail. So monitoring_exceptions_fy26.csv holds one row per entry raised, not one per posting that tripped.
3. Took the window from period_calendar.csv and extract_manifest.txt (FY26 P1 to P9, closed 2026-06-28) and resolved the two unit-code vintages in journal_entries through trading_unit_register.csv, whose renumbering took effect 2026-03-30. Kept the nine rules continuous_monitoring_rule_catalogue.pdf marks live in FY26.
4. Reconciled the register to the exception summary in monitoring_platform_operating_guide.pdf: 7,481 entries raised, tying by unit and period.
5. Rejected the two routes the entry count supports. Reporting the 7,481 raised entries as the posting count understates it, because an entry carrying 2,347 postings raises the same one verdict as a manual journal carrying one. Taking the entry flag rate and grossing it up by the group's postings gives 29,234, because the indicator cannot fire twice on one voucher, so the entry rate is an upper bound on the posting rate and not an estimate of it.
6. Recovered the rate instead. An entry of k postings is raised when at least one of them trips, with probability 1 - (1 - r) ** k, so r is the root of the per-entry likelihood over that unit's own entries. The root is unique because the score is monotone. Inverting once on the group's mean entry size instead returns 7,548, which is the raised-entry count again: the mean of the inverses is not the inverse of the mean, and entry sizes here run from 1 to 2,347.
7. Multiplied each unit's recovered rate by that unit's postings and summed: 15,000 for the group, unrounded 14989.3. Method of moments on the total and the complementary log-log form give 15,006 and 15,102, and one rate pooled across the group gives 14,712, all within the same thousand.
8. Built the three FY25 reconciliations: the payables accrual, where a restatement supersedes an earlier accrual without reversing it; the till takings, where the EPOS interface uploads a trading day on the next working day; and the monitoring coverage, where the in-scope population comes from the ledger's own period summary filtered to the streams the ruleset covers, not from the run log's completion flag.

## 4. Deliverable Answers

### exception_population_bridge.xlsx

Bridge, by trading unit: journal entries, postings, entries raised as exceptions, postings that tripped the ruleset, and the bridge between the last two.

| Trading unit | Entries raised | Postings that tripped | Bridge |
|---|---|---|---|
| DPG-110 | 792 | 1,700 | 908 |
| DPG-120 | 920 | 2,100 | 1,180 |
| DPG-130 | 732 | 1,500 | 768 |
| DPG-210 | 659 | 1,300 | 641 |
| DPG-220 | 599 | 1,100 | 501 |
| DPG-310 | 623 | 1,200 | 577 |
| DPG-320 | 695 | 1,400 | 705 |
| DPG-410 | 560 | 1,000 | 440 |
| DPG-420 | 754 | 1,600 | 846 |
| DPG-510 | 514 | 900 | 386 |
| DPG-610 | 502 | 800 | 298 |
| DPG-900 | 131 | 400 | 269 |
| **Group** | **7,481** | **15,000** | **7,519** |

Payables reconciliation, FY25 close, EUR.

| Trading unit | Subledger accrual | Control account | Difference | Goods received not invoiced | Posted to another unit |
|---|---|---|---|---|---|
| DPG-110 | 3,370,438.09 | 3,412,118.20 | 41,680.11 | 54,803.60 | -13,123.49 |
| DPG-120 | 3,407,688.00 | 3,461,176.89 | 53,488.89 | 73,058.34 | -19,569.45 |
| DPG-130 | 3,312,527.91 | 3,316,519.24 | 3,991.33 | 41,250.86 | -37,259.53 |
| DPG-210 | 3,478,211.77 | 3,535,634.67 | 57,422.90 | 17,078.05 | 40,344.85 |
| DPG-220 | 4,164,592.26 | 4,238,891.02 | 74,298.76 | 88,713.56 | -14,414.80 |
| DPG-310 | 3,534,676.56 | 3,577,895.89 | 43,219.33 | 33,459.16 | 9,760.17 |
| DPG-320 | 3,748,141.41 | 3,712,758.85 | -35,382.56 | 51,749.21 | -87,131.77 |
| DPG-410 | 3,771,488.85 | 3,817,464.80 | 45,975.95 | 22,014.52 | 23,961.43 |
| DPG-420 | 3,634,085.04 | 3,666,082.98 | 31,997.94 | 36,242.37 | -4,244.43 |
| DPG-510 | 2,714,983.45 | 2,805,791.30 | 90,807.85 | 89,978.86 | 828.99 |
| DPG-610 | 2,089,129.61 | 2,200,255.03 | 111,125.42 | 44,326.07 | 66,799.35 |
| DPG-900 | 1,830,264.68 | 1,933,427.08 | 103,162.40 | 69,113.72 | 34,048.68 |
| GROUP | 39,056,227.63 | 39,678,015.95 | 621,788.32 | 621,788.32 | 0.00 |

Till takings against the sales control account, FY25, EUR.

| Trading unit | Quarter | Till takings | Sales control account | Gap |
|---|---|---|---|---|
| DPG-110 | Q1 | 3,892,571.63 | 3,831,436.75 | 61,134.88 |
| DPG-110 | Q2 | 3,695,028.78 | 3,719,617.00 | -24,588.22 |
| DPG-110 | Q3 | 3,977,306.04 | 3,972,112.03 | 5,194.01 |
| DPG-110 | Q4 | 3,942,129.51 | 3,949,584.66 | -7,455.15 |
| DPG-120 | Q1 | 3,184,113.42 | 3,142,791.37 | 41,322.05 |
| DPG-120 | Q2 | 3,147,509.53 | 3,135,867.28 | 11,642.25 |
| DPG-120 | Q3 | 3,148,904.39 | 3,161,621.23 | -12,716.84 |
| DPG-120 | Q4 | 3,130,858.67 | 3,139,257.21 | -8,398.54 |
| DPG-130 | Q1 | 3,060,694.54 | 3,021,359.42 | 39,335.12 |
| DPG-130 | Q2 | 3,329,948.40 | 3,331,268.63 | -1,320.23 |
| DPG-130 | Q3 | 3,086,151.56 | 3,084,290.77 | 1,860.79 |
| DPG-130 | Q4 | 3,173,317.76 | 3,170,546.76 | 2,771.00 |
| DPG-210 | Q1 | 3,908,169.45 | 3,875,412.66 | 32,756.79 |
| DPG-210 | Q2 | 3,944,018.25 | 3,928,526.39 | 15,491.86 |
| DPG-210 | Q3 | 4,102,729.56 | 4,096,231.08 | 6,498.48 |
| DPG-210 | Q4 | 4,014,399.22 | 4,037,486.04 | -23,086.82 |
| DPG-220 | Q1 | 2,285,912.29 | 2,255,361.39 | 30,550.90 |
| DPG-220 | Q2 | 2,338,916.92 | 2,335,763.87 | 3,153.05 |
| DPG-220 | Q3 | 2,498,366.27 | 2,499,112.65 | -746.38 |
| DPG-220 | Q4 | 2,437,131.08 | 2,444,094.11 | -6,963.03 |
| DPG-310 | Q1 | 3,973,533.17 | 3,939,215.18 | 34,317.99 |
| DPG-310 | Q2 | 3,910,980.27 | 3,876,874.83 | 34,105.44 |
| DPG-310 | Q3 | 3,814,259.55 | 3,794,490.02 | 19,769.53 |
| DPG-310 | Q4 | 3,964,897.68 | 4,001,674.69 | -36,777.01 |
| DPG-320 | Q1 | 3,811,395.72 | 3,754,663.56 | 56,732.16 |
| DPG-320 | Q2 | 4,004,106.03 | 4,004,786.38 | -680.35 |
| DPG-320 | Q3 | 3,852,938.33 | 3,848,282.17 | 4,656.16 |
| DPG-320 | Q4 | 3,858,949.37 | 3,864,728.72 | -5,779.35 |
| DPG-410 | Q1 | 3,098,132.98 | 3,060,194.89 | 37,938.09 |
| DPG-410 | Q2 | 3,163,465.56 | 3,167,705.97 | -4,240.41 |
| DPG-410 | Q3 | 3,066,279.96 | 3,056,985.13 | 9,294.83 |
| DPG-410 | Q4 | 3,233,400.44 | 3,229,661.87 | 3,738.57 |
| DPG-420 | Q1 | 4,010,073.59 | 3,978,408.02 | 31,665.57 |
| DPG-420 | Q2 | 3,850,666.18 | 3,823,971.56 | 26,694.62 |
| DPG-420 | Q3 | 4,079,601.62 | 4,075,256.41 | 4,345.21 |
| DPG-420 | Q4 | 3,939,078.50 | 3,943,591.04 | -4,512.54 |

Entries in scope of the ruleset not evaluated, FY25, by trading unit and period.

| Trading unit | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 | P11 | P12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| DPG-110 | 19 | 13 | 34 | 32 | 22 | 19 | 33 | 301 | 574 | 798 | 29 | 48 |
| DPG-120 | 16 | 19 | 19 | 37 | 54 | 24 | 18 | 301 | 624 | 1,097 | 18 | 39 |
| DPG-130 | 36 | 36 | 21 | 20 | 21 | 44 | 11 | 262 | 814 | 1,018 | 24 | 14 |
| DPG-210 | 36 | 17 | 36 | 25 | 10 | 23 | 18 | 328 | 610 | 867 | 33 | 41 |
| DPG-220 | 30 | 40 | 30 | 16 | 38 | 49 | 47 | 270 | 540 | 975 | 40 | 16 |
| DPG-310 | 28 | 16 | 28 | 45 | 45 | 30 | 26 | 279 | 576 | 893 | 31 | 10 |
| DPG-320 | 39 | 33 | 11 | 27 | 37 | 19 | 34 | 283 | 695 | 1,152 | 32 | 12 |
| DPG-410 | 25 | 22 | 43 | 35 | 17 | 29 | 22 | 335 | 649 | 784 | 44 | 46 |
| DPG-420 | 12 | 22 | 14 | 23 | 35 | 50 | 27 | 358 | 730 | 1,100 | 12 | 41 |
| DPG-510 | 50 | 39 | 47 | 24 | 26 | 32 | 72 | 525 | 1,362 | 1,698 | 66 | 79 |
| DPG-610 | 31 | 17 | 16 | 15 | 12 | 39 | 18 | 290 | 667 | 793 | 33 | 17 |
| DPG-900 | 2 | 2 | 4 | 1 | 4 | 2 | 3 | 26 | 58 | 108 | 3 | 3 |

### audit_plan_paper.pdf

15,000 postings tripped the continuous monitoring ruleset in FY26 P1 to P9, against 7,481 journal entries raised as exceptions. Per unit figures as in the bridge above.

### recovered_exceptions_by_unit.png

One pair of bars per trading unit: entries raised as exceptions against postings that tripped the ruleset, every bar labelled with its figure.

