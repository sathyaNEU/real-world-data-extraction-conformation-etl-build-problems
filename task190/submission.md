**Domain:** Accounting, Audit & Forensic (audit testing and sampling).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The misstatement in the capital programme payments population for the year to 31 December 2026 is 800,000 euro, and the population is referred for extended testing before the statements are certified.**
Dredging programme carries most of it at 200,000. Not the 19,801.79 the testing found in the lines it tested, which projects nothing. Not the 54,424.62 those findings give when scaled on recorded value, which is the obvious projection and understates by a factor of fifteen because the 31 lines certain of selection hold 15,846,000 of the 21,644,558 tested and were all found sound. Not the 149,040.12 from taking those 31 at their own error and scaling the rest on their stratum. Each of those three accepts the population at plan 4.3; only the projection the selection entitles refers it.

## 2. Critical Components

1. Capital programme payment lines in the population: **26,648**, recorded at **59,489,415.33** euro. Lines tested: **272**, recorded at **21,644,557.86**; of those, **31** were certain of selection and hold **15,846,000**.
2. Misstatement by work programme, to the nearest 50,000: Dredging programme **200,000**, Rail siding and yard **150,000**, Shore power installation **150,000**, Welfare and offices fit-out **150,000**, Security and access systems **100,000**, Terminal roof and cladding **50,000**, Deepwater berth renewal **0**, Quay 3 reconstruction **0**, Pavement and surfacing **0**
3. The projection before rounding: **813,779.66**. Basic precision **540,000**, the incremental allowance **342,933.23**, and the upper limit **1,696,712.89**, which exceeds the tolerable misstatement plan 4.2 sets.

## 3. Step-by-Step Solution

1. Built the population from `capital_payment_lines_2026.csv` in its own ledger sequence: dropped the two reversed lines and the credit notes that reverse them, collapsed the one payment run the bank feed delivered twice on its delivery sequence, and took each line's work programme from the register. 26,648 lines, 59,489,415.33 euro.
2. Lifted the 273 rows of the testing schedule out of `internal_audit_testing_schedule_2026.pdf`, carried their references onto the ledger through `supplier_number_crosswalk.csv`, and found one line the schedule carries twice after a query. 272 distinct lines tested.
3. Read manual 9.1: the misstatement is the amount by which recorded value exceeds the amount properly payable, over every line in the population, stated by work programme to the nearest 50,000. Read 9.2: no record holds it, because the records carry what was paid and the testing establishes the difference only for the lines tested.
4. Found the testing's own findings total 19,801.79, which is not the population's misstatement, and that scaling them on recorded value gives 54,424.62.
5. Looked at how the tested lines were chosen. Every one of the 31 population lines at or above about 180,000 euro is in the tested set and no smaller line is certain, and below that the share of lines tested rises in proportion to amount: the lines were selected by stepping a fixed amount of euro through the population in ledger sequence. Recovered that amount as the only one for which every tested line holds a step of cumulated recorded value under one common start and no untested line does: **180,000** euro, the only feasible value within 40 euro either side.
6. Projected on that: each tainting in a line below the interval at the interval, each line certain of selection at its own error. **813,779.66**, which is 800,000 to the nearest 50,000, and the work programme figures as stated sum to the same 800,000.
7. Evaluated against plan 4.3: basic precision 540,000, the incremental allowance 342,933.23 over 10 taintings, upper limit 1,696,712.89, which exceeds the tolerable misstatement plan 4.2 sets. Even the projection plus basic precision alone, at 1,353,779.66, exceeds it. The population is referred for extended testing.

## 4. Deliverable Answers

### projected_misstatement_2026.csv

1. Misstatement indicated, the authority: 800,000
2. The programme carrying most of it: Dredging programme, 200,000
3. One row per work programme, the payments recorded, the misstatement indicated and the share of recorded value certain of selection:
   - Dredging programme: 5,600,000.02 recorded, 200,000 misstated, 42.6 per cent certain
   - Rail siding and yard: 6,297,943.84 recorded, 150,000 misstated, 16.9 per cent certain
   - Shore power installation: 4,699,999.78 recorded, 150,000 misstated, 18.4 per cent certain
   - Welfare and offices fit-out: 3,200,000.09 recorded, 150,000 misstated, 14.0 per cent certain
   - Security and access systems: 3,500,000.07 recorded, 100,000 misstated, 13.8 per cent certain
   - Terminal roof and cladding: 8,400,000.17 recorded, 50,000 misstated, 18.5 per cent certain
   - Deepwater berth renewal: 13,899,999.86 recorded, 0 misstated, 35.2 per cent certain
   - Quay 3 reconstruction: 10,591,471.66 recorded, 0 misstated, 34.2 per cent certain
   - Pavement and surfacing: 3,299,999.84 recorded, 0 misstated, 15.6 per cent certain
   - Authority: 59,489,415.33 recorded, 800,000 misstated

### misstatement_by_population_2026.png

1. One bar per work programme of the misstatement indicated, in descending order, each labelled with its figure: Dredging programme 200,000, Rail siding and yard 150,000, Shore power installation 150,000, Welfare and offices fit-out 150,000, Security and access systems 100,000, Terminal roof and cladding 50,000, Deepwater berth renewal 0, Quay 3 reconstruction 0, Pavement and surfacing 0.
2. The largest bar, Dredging programme, is marked in the darker colour, and the title carries the authority total of 800,000 against the tolerable misstatement plan 4.2 sets.

### Also asked

1. Payment runs released, those past the cut-off in force and the net value reversed, by quarter, values to the cent:
   - 2026Q1: 26 runs, 4 past the cut-off, net value reversed 0.00
   - 2026Q2: 26 runs, 8 past the cut-off, net value reversed -10,584.67
   - 2026Q3: 26 runs, 12 past the cut-off, net value reversed 0.00
   - 2026Q4: 26 runs, 8 past the cut-off, net value reversed 0.00
2. Suppliers raised into the category, removed into it, and raised in then removed again, by supplier risk category:
   - Category 1 (R-A): 0 raised in, 25 removed into it, 0 raised then removed
   - Category 2 (R-B): 29 raised in, 24 removed into it, 16 raised then removed
   - Category 3 (R-C): 42 raised in, 36 removed into it, 11 raised then removed
   - Category 4 (R-D): 31 raised in, 26 removed into it, 16 raised then removed
   - Category 5 (R-E): 39 raised in, 0 removed into it, 0 raised then removed
3. Payment lines the testing schedule covers, by month:
   - 2026-01: 26
   - 2026-02: 22
   - 2026-03: 26
   - 2026-04: 20
   - 2026-05: 27
   - 2026-06: 19
   - 2026-07: 28
   - 2026-08: 21
   - 2026-09: 19
   - 2026-10: 28
   - 2026-11: 17
   - 2026-12: 20
4. Schedule lines absent from the ledger: none.
5. Ledger lines on the schedule twice: 1.
