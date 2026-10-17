**Domain:** Accounting, Audit & Forensic (audit testing and sampling).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The misstatement in the capital programme payments population for the year to 31 December 2026 is 850,000 euro, and the population is referred for extended testing before the statements are certified.**
Security and access systems carries most of it at 250,000. Not the misstatement the testing found in the lines it tested, which projects nothing. Not those findings scaled on recorded value, the obvious projection, which understates by a factor of fifteen because the 31 lines certain of selection hold 15,826,540.07 of the value tested and were all found sound. Not the figure from taking those 31 at their own error and scaling the rest on their own stratum. Each of those three accepts the population at plan 4.3; only the projection the selection design entitles refers it.

## 2. Critical Components

1. Capital programme payment lines in the population: **26,651**, recorded at **59,473,299.73** euro. Of the lines the selection chose, **31** were certain of selection and hold **15,826,540.07**.
2. Misstatement by work programme, to the nearest 50,000: Security and access systems **250,000**, Rail siding and yard **200,000**, Pavement and surfacing **150,000**, Shore power installation **150,000**, Terminal roof and cladding **50,000**, Welfare and offices fit-out **50,000**, Deepwater berth renewal **0**, Dredging programme **0**, Quay 3 reconstruction **0**
3. The projection before rounding: **840,096.72**. Basic precision **540,000.00**, the incremental allowance **227,684.83** over **26** taintings, and the upper limit **1,607,781.54**, which exceeds the tolerable misstatement plan 4.2 sets.

## 3. Step-by-Step Solution

1. Built the population from `capital_payment_lines_2026.csv` in its own ledger sequence: dropped the two reversed lines and the credit notes that reverse them, collapsed the one payment run the bank feed delivered twice on its delivery sequence, and took each line's work programme from the register. **26,651** lines, **59,473,299.73** euro.
2. Lifted the **293** rows of the working paper out of `internal_audit_testing_schedule_2026.pdf`. Seventeen resolve to no line in the capital ledger: they are plan 4.4's revenue expenditure sample, on the same paper under their own cost centres and their own ledger prefix. Five are certified valuations recorded at invoice level, so each covers every payment line on its invoice rather than one line, and every line on those five invoices was found sound. One capital line is on the paper twice, re-tested after a query. The paper therefore covers **285** distinct capital ledger lines, while the selection itself chose the lines the basis of selection describes.
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

1. Payment runs released, those past the cut-off in force on the run's own date and the value those carried, by quarter of release, values to the cent:
   - 2026Q1: 24 runs, 9 past the cut-off, 6,974,178.95 released past it
   - 2026Q2: 24 runs, 9 past the cut-off, 4,480,460.44 released past it
   - 2026Q3: 26 runs, 7 past the cut-off, 4,397,928.34 released past it
   - 2026Q4: 24 runs, 7 past the cut-off, 4,650,297.66 released past it
2. Suppliers raised into the category, removed from it, and raised in then removed, by supplier risk category:
   - Category 1 (R-A): 0 raised into it, 31 removed from it, 0 raised in then removed
   - Category 2 (R-B): 29 raised into it, 69 removed from it, 16 raised in then removed
   - Category 3 (R-C): 42 raised into it, 49 removed from it, 11 raised in then removed
   - Category 4 (R-D): 31 raised into it, 76 removed from it, 16 raised in then removed
   - Category 5 (R-E): 39 raised into it, 27 removed from it, 0 raised in then removed
3. Distinct ledger lines the testing schedule covers, by month of payment:
   - 2026-01: 28
   - 2026-02: 20
   - 2026-03: 22
   - 2026-04: 24
   - 2026-05: 19
   - 2026-06: 27
   - 2026-07: 33
   - 2026-08: 17
   - 2026-09: 23
   - 2026-10: 25
   - 2026-11: 16
   - 2026-12: 21
   17 rows on the working paper resolve to no line in the capital payment ledger: they are the revenue expenditure sample plan 4.4 tests, on the same paper under their own cost centres and their own ledger prefix, and they are counted in no month. One capital ledger line is on the paper twice, CPL-26-172282, re-tested after a query, so the paper carries 293 rows against 276 distinct capital lines.
