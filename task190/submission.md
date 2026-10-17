**Domain:** Accounting, Audit & Forensic (audit testing and sampling).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The misstatement in the capital programme payments population for the year to 31 December 2026 is 850,000 euro, and the population is referred for extended testing before the statements are certified.**
Security and access systems carries most of it at 250,000. Not the 21,004.93 the testing found in the lines it tested, which projects nothing. Not the 57,577.47 those findings give when scaled on recorded value, which is the obvious projection and understates by a factor of fifteen because the 31 lines certain of selection hold 15,826,540.07 of the 21,696,549.77 tested and were all found sound. Not the 156,183.24 from taking those 31 at their own error and scaling the rest on their own stratum. Each of those three accepts the population at plan 4.3; only the projection the selection design entitles refers it.

## 2. Critical Components

1. Capital programme payment lines in the population: **26,651**, recorded at **59,473,299.73** euro. Lines tested: **275**, recorded at **21,696,549.77**; of those, **31** were certain of selection and hold **15,826,540.07**.
2. Misstatement by work programme, to the nearest 50,000: Security and access systems **250,000**, Rail siding and yard **200,000**, Pavement and surfacing **150,000**, Shore power installation **150,000**, Terminal roof and cladding **50,000**, Welfare and offices fit-out **50,000**, Deepwater berth renewal **0**, Dredging programme **0**, Quay 3 reconstruction **0**
3. The projection before rounding: **840,096.72**. Basic precision **540,000.00**, the incremental allowance **227,684.83** over **26** taintings, and the upper limit **1,607,781.54**, which exceeds the tolerable misstatement plan 4.2 sets.

## 3. Step-by-Step Solution

1. Built the population from `capital_payment_lines_2026.csv` in its own ledger sequence: dropped the two reversed lines and the credit notes that reverse them, collapsed the one payment run the bank feed delivered twice on its delivery sequence, and took each line's work programme from the register. **26,651** lines, **59,473,299.73** euro.
2. Lifted the **276** rows of the testing schedule out of `internal_audit_testing_schedule_2026.pdf` and matched each to its ledger line. One line is on the schedule twice, re-tested after a query. **275** distinct lines tested, recorded at 21,696,549.77.
3. Read manual 9.1: the misstatement is the amount by which recorded value exceeds the amount properly payable, over every line in the population, stated by work programme to the nearest 50,000 with the authority's figure their sum. Read 9.2: no record holds it, because the records carry what was paid and the testing establishes the difference only for the lines tested.
4. Found the testing's own findings total 21,004.93, which is not the population's misstatement, and that scaling them on recorded value gives 57,577.47 and taking the certainty lines at their own error with the rest scaled on their stratum gives 156,183.24.
5. Read the basis of selection on the working paper: the sample was drawn with probability proportional to recorded value, by stepping one interval of **180,000** euro through the population's cumulated recorded value, the same interval for every work programme, so a line of 180,000 or more was certain of selection and a line below it was selected with probability equal to its amount over the interval. That fixes what one tested line stands for, which none of the three routes above uses.
6. Projected on the design: each tainting in a line below the interval at the interval, each line certain of selection at its own error. **840,096.72**, which is 850,000 to the nearest 50,000, and the work programme figures as stated sum to the same 850,000.
7. Evaluated against plan 4.3 on the manual's own definitions at 9.3 and its reliability factors at 9.5: basic precision 540,000.00, the incremental allowance 227,684.83, upper limit 1,607,781.54, which exceeds the tolerable misstatement plan 4.2 sets. Even the projection plus basic precision alone, at 1,380,096.72, exceeds it. The population is referred for extended testing.

## 4. Deliverable Answers

### projected_misstatement_2026.csv

1. Misstatement indicated, the authority: 850,000
2. The programme carrying most of it: Security and access systems, 250,000
3. One row per work programme, the misstatement indicated and the share of its recorded value certain of selection:
   - Security and access systems: 250,000 misstated, 13.8 per cent certain
   - Rail siding and yard: 200,000 misstated, 16.9 per cent certain
   - Pavement and surfacing: 150,000 misstated, 15.6 per cent certain
   - Shore power installation: 150,000 misstated, 18.4 per cent certain
   - Terminal roof and cladding: 50,000 misstated, 18.5 per cent certain
   - Welfare and offices fit-out: 50,000 misstated, 14.0 per cent certain
   - Deepwater berth renewal: 0 misstated, 35.2 per cent certain
   - Dredging programme: 0 misstated, 42.6 per cent certain
   - Quay 3 reconstruction: 0 misstated, 34.2 per cent certain
   - Authority: 850,000 misstated, 26.6 per cent certain

### misstatement_by_population_2026.png

1. One bar per work programme of the misstatement indicated, in descending order, each labelled with its figure: Security and access systems 250,000, Rail siding and yard 200,000, Pavement and surfacing 150,000, Shore power installation 150,000, Terminal roof and cladding 50,000, Welfare and offices fit-out 50,000, Deepwater berth renewal 0, Dredging programme 0, Quay 3 reconstruction 0.
2. The largest bar, Security and access systems, is marked in the darker colour, and the title carries the authority total of 850,000 and the 250,000 in the leading programme.

### Also asked

1. Payment runs released, those past the cut-off in force and the value those carried, by quarter, values to the cent:
   - 2026Q1: 25 runs, 9 past the cut-off, 4,103,782.83 released past it
   - 2026Q2: 26 runs, 8 past the cut-off, 5,633,782.71 released past it
   - 2026Q3: 27 runs, 5 past the cut-off, 2,342,669.74 released past it
   - 2026Q4: 26 runs, 6 past the cut-off, 3,603,482.20 released past it
2. Suppliers raised into the category, removed into it, and raised in then removed again, by supplier risk category:
   - Category 1 (R-A): 0 raised in, 25 removed into it, 0 raised then removed
   - Category 2 (R-B): 29 raised in, 24 removed into it, 16 raised then removed
   - Category 3 (R-C): 42 raised in, 36 removed into it, 11 raised then removed
   - Category 4 (R-D): 31 raised in, 26 removed into it, 16 raised then removed
   - Category 5 (R-E): 39 raised in, 0 removed into it, 0 raised then removed
3. Payment lines the testing schedule covers, by month:
   - 2026-01: 29
   - 2026-02: 21
   - 2026-03: 24
   - 2026-04: 27
   - 2026-05: 31
   - 2026-06: 16
   - 2026-07: 25
   - 2026-08: 12
   - 2026-09: 25
   - 2026-10: 23
   - 2026-11: 20
   - 2026-12: 23
   No schedule line is absent from the ledger. One ledger line is on the schedule twice, CPL-26-081376.
