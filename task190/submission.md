**Domain:** Accounting, Audit & Forensic (audit testing and sampling).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**The misstatement in the capital programme payments population for the year to 31 December 2026 is 800,000 euro, and the population is referred for extended testing before the statements are certified.**
Rail siding and yard carries most of it at 250,000. Not the 15,445.38 the testing found in the lines it tested, which projects nothing. Not the 43,648.52 those findings give when scaled on recorded value, which is the obvious projection and understates by a factor of nineteen because the 31 lines certain of selection hold 15,826,525 of the 21,043,847 tested and were all found sound. Not the 129,201.54 from taking those 31 at their own error and scaling the rest on their own stratum. Each of those three accepts the population at plan 4.3; only the projection the selection entitles refers it.

## 2. Critical Components

1. Capital programme payment lines in the population: **26,648**, recorded at **59,469,739.92** euro. Lines tested: **271**, recorded at **21,043,847.13**; of those, **31** were certain of selection and hold **15,826,525.00**.
2. Misstatement by work programme, to the nearest 50,000: Rail siding and yard **250,000**, Security and access systems **200,000**, Pavement and surfacing **150,000**, Welfare and offices fit-out **100,000**, Shore power installation **50,000**, Terminal roof and cladding **50,000**, Deepwater berth renewal **0**, Quay 3 reconstruction **0**, Dredging programme **0**
3. The projection before rounding: **811,170.09**. Basic precision **540,000**, the incremental allowance **347,797.48** over **10** taintings, and the upper limit **1,698,967.57**, which exceeds the tolerable misstatement plan 4.2 sets.

## 3. Step-by-Step Solution

1. Built the population from `capital_payment_lines_2026.csv` in its own ledger sequence: dropped the two reversed lines and the credit notes that reverse them, collapsed the one payment run the bank feed delivered twice on its delivery sequence, and took each line's work programme from the register. **26,648** lines, **59,469,739.92** euro.
2. Lifted the **272** rows of the testing schedule out of `internal_audit_testing_schedule_2026.pdf`, carried their references onto the ledger through `supplier_number_crosswalk.csv`, and found one line the schedule carries twice after a query. **271** distinct lines tested, recorded at 21,043,847.13.
3. Read manual 9.1: the misstatement is the amount by which recorded value exceeds the amount properly payable, over every line in the population, stated by work programme to the nearest 50,000 with the authority's figure their sum. Read 9.2: no record holds it, because the records carry what was paid and the testing establishes the difference only for the lines tested.
4. Found the testing's own findings total 15,445.38, which is not the population's misstatement, and that scaling them on recorded value gives 43,648.52 and taking the certainty lines at their own error gives 129,201.54.
5. Looked at how the tested lines were chosen. Every one of the 31 population lines at or above about 180,000 euro is in the tested set and no smaller line is certain, and below that the share of lines tested rises in proportion to amount: the lines were selected by stepping a fixed amount of euro through the population in ledger sequence. Recovered that amount as the only one for which every tested line holds a step of cumulated recorded value under one common start and no untested line does. It is **180,000** euro, and it is the only feasible value within 40 euro either side.
6. Projected on that: each tainting in a line below the interval at the interval, each line certain of selection at its own error. **811,170.09**, which is 800,000 to the nearest 50,000, and the work programme figures as stated sum to the same 800,000.
7. Evaluated against plan 4.3: basic precision 540,000, the incremental allowance 347,797.48, upper limit 1,698,967.57, which exceeds the tolerable misstatement plan 4.2 sets. Even the projection plus basic precision alone, at 1,351,170.09, exceeds it. The population is referred for extended testing.

## 4. Deliverable Answers

### projected_misstatement_2026.csv

1. Misstatement indicated, the authority: 800,000
2. The programme carrying most of it: Rail siding and yard, 250,000
3. One row per work programme, the misstatement indicated and the share of its recorded value certain of selection:
   - Rail siding and yard: 250,000 misstated, 16.9 per cent certain
   - Security and access systems: 200,000 misstated, 13.8 per cent certain
   - Pavement and surfacing: 150,000 misstated, 15.6 per cent certain
   - Welfare and offices fit-out: 100,000 misstated, 14.0 per cent certain
   - Shore power installation: 50,000 misstated, 18.4 per cent certain
   - Terminal roof and cladding: 50,000 misstated, 18.5 per cent certain
   - Deepwater berth renewal: 0 misstated, 35.2 per cent certain
   - Dredging programme: 0 misstated, 42.6 per cent certain
   - Quay 3 reconstruction: 0 misstated, 34.2 per cent certain
   - Authority: 800,000 misstated, 26.6 per cent certain

### misstatement_by_population_2026.png

1. One bar per work programme of the misstatement indicated, in descending order, each labelled with its figure: Rail siding and yard 250,000, Security and access systems 200,000, Pavement and surfacing 150,000, Welfare and offices fit-out 100,000, Shore power installation 50,000, Terminal roof and cladding 50,000, Deepwater berth renewal 0, Dredging programme 0, Quay 3 reconstruction 0.
2. The largest bar, Rail siding and yard, is marked in the darker colour, and the title carries the authority total of 800,000 and the 250,000 in the leading programme.

### Also asked

1. Payment runs released, those past the cut-off in force and the value those carried, by quarter, values to the cent:
   - 2026Q1: 25 runs, 9 past the cut-off, 5,303,327.24 released past it
   - 2026Q2: 26 runs, 8 past the cut-off, 5,217,457.85 released past it
   - 2026Q3: 27 runs, 5 past the cut-off, 3,433,308.73 released past it
   - 2026Q4: 26 runs, 6 past the cut-off, 3,470,389.62 released past it
2. Suppliers raised into the category, removed into it, and raised in then removed again, by supplier risk category:
   - Category 1 (R-A): 0 raised in, 25 removed into it, 0 raised then removed
   - Category 2 (R-B): 29 raised in, 24 removed into it, 16 raised then removed
   - Category 3 (R-C): 42 raised in, 36 removed into it, 11 raised then removed
   - Category 4 (R-D): 31 raised in, 26 removed into it, 16 raised then removed
   - Category 5 (R-E): 39 raised in, 0 removed into it, 0 raised then removed
3. Payment lines the testing schedule covers, by month:
   - 2026-01: 34
   - 2026-02: 19
   - 2026-03: 26
   - 2026-04: 17
   - 2026-05: 25
   - 2026-06: 23
   - 2026-07: 28
   - 2026-08: 14
   - 2026-09: 27
   - 2026-10: 24
   - 2026-11: 12
   - 2026-12: 23
4. Schedule lines absent from the ledger: none.
5. Ledger lines on the schedule twice: 1.
