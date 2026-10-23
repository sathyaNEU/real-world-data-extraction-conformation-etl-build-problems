## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (a state air agency's 2026 press VOC inventory of fourteen printing and converting plants, conformed from press logs, safety data sheets, capture determinations, oxidizer historians and performance tests, each oxidizer's outlet carried to each production day's inlet).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Rule 18-4 covers Ashcombe Flexible Packaging, Carrow Gravure, Kelvedon Laminates, Merrion Flexibles and Ravensbrook Gravure Packaging from 1 July 2027.**
Their presses emitted 29, 37, 28, 31 and 56 tons of VOC in 2026, Kelvedon Laminates the lowest at 28, against Larkmoor Graphics 21 (4 short). Not the oxidizers' tested efficiencies, which put Ashcombe Flexible Packaging and Kelvedon Laminates at 21 and 20 tons: every test ran at maximum production, and on the part-production days of 2026 the fixed-speed fans drew their full air, so the oxidizers' outlets held near their floor and destroyed less than the tests show.

## 2. Critical Components

1. Across the 28 tests the outlet holds near **45** ppmv as carbon below an inlet of about **2,500** ppmv and passes **1.8** per cent of the inlet above it.
2. Ashcombe Flexible Packaging's 2026 press VOC is **29** tons, against **21** on its latest test's efficiency.
3. Kelvedon Laminates' 2026 press VOC is **28** tons, against **20** on its latest test's efficiency.
4. Larkmoor Graphics, the nearest plant below the line, emitted **21** tons, **4** short.

## 3. Step-by-Step Solution

1. Converted every row of press_material_use_2026.csv (shift and job records alike, Thameside Laminating's facility 0117 rows to Kelvedon Laminates) to pounds of VOC through safety_data_sheet_master_2027-01.xlsx: per cent by weight times density, or pounds per gallon less water and exempt compounds times the share of the product that is neither, pound rows by density.
2. Split each controlled plant's VOC by the capture efficiency on the Capture sheet of deq_printing_plants_register_2027-02.xlsx; the four plants without an oxidizer emit what they used.
3. Put oxidizer_historian_hourly_2026.csv on Central time, took each production day's PROCESS hours and their mean airflow (fan speed times the register's rated airflow where the historian logs speed), and with the register's carbon content read each day's inlet as carbon from its captured VOC.
4. Put the 84 runs in oxidizer_performance_tests_2017_2026.pdf on one basis (Marlow's propane figures times 3) and took the outlet as the mean of the runs under 2,000 ppmv, about 45, and above the knee the mean share the runs over 3,000 ppmv pass, 1.8 per cent.
5. Read each day's outlet from its inlet, times its air and hours, for what the oxidizer let through, added the uncaptured VOC and compared each plant's year with 25 tons: Ravensbrook Gravure Packaging 56, Carrow Gravure 37, Merrion Flexibles 31, Ashcombe Flexible Packaging 29, Kelvedon Laminates 28, Larkmoor Graphics 21 and Garrowby Printing 19.
6. For cleaning, priced each stores_cleaning_issues_2026.csv issue away from the presses at the revision in force on its date (HW-CS-210 at 7.10 lb a gallon before its 1 June 2026 reformulation, per the revision log), less cantrell_bend_manifests_2026.csv weights under each plant's Cleaning profile (KG rows times 2.20462), plus each washer's added less removed solvent in wexcombe_service_tickets_2026.csv and in Ostrander's lines in solvent_vendor_payments_2026.csv.
7. For the gallons, took Corvane and Haldane lines shipped in 2026 (returns netted), read Haldane items on documents dated before 1 April 2026 through the replaces_item column of haldane_catalog_2026-04.csv, turned pound items into gallons by density, and set them against stock_counts_2026.csv and the press logs' use.
8. Listed the plants at 25 tons or more: Ashcombe Flexible Packaging, Carrow Gravure, Kelvedon Laminates, Merrion Flexibles and Ravensbrook Gravure Packaging.

## 4. Deliverable Answers

### deq_rule18-4_applicability_2027.xlsx

1. Plants Rule 18-4 covers from 1 July 2027: Ashcombe Flexible Packaging, Carrow Gravure, Kelvedon Laminates, Merrion Flexibles and Ravensbrook Gravure Packaging.
2. Each plant's 2026 press VOC, whole tons, and whether the rule covers it:
   - Ashcombe Flexible Packaging: 29, covered
   - Brinsley Label Works: 9, not covered
   - Carrow Gravure: 37, covered
   - Dunsford Folding Cartons: 7, not covered
   - Elsworth Film Converting: 16, not covered
   - Garrowby Printing: 19, not covered
   - Hartmoor Packaging: 18, not covered
   - Ivers Lane Press: 11, not covered
   - Kelvedon Laminates: 28, covered
   - Larkmoor Graphics: 21, not covered
   - Merrion Flexibles: 31, covered
   - Norhaven Converting: 17, not covered
   - Pellworth Label: 4, not covered
   - Ravensbrook Gravure Packaging: 56, covered
3. Nearest plant below the line: Larkmoor Graphics, 4 tons short.
4. Each plant's 2026 VOC from cleaning away from its presses, tons to one decimal:
   - Ashcombe Flexible Packaging: 5.2
   - Brinsley Label Works: 1.3
   - Carrow Gravure: 7.1
   - Dunsford Folding Cartons: 1.2
   - Elsworth Film Converting: 4.5
   - Garrowby Printing: 2.0
   - Hartmoor Packaging: 2.4
   - Ivers Lane Press: 1.6
   - Kelvedon Laminates: 3.9
   - Larkmoor Graphics: 3.9
   - Merrion Flexibles: 4.8
   - Norhaven Converting: 1.9
   - Pellworth Label: 1.1
   - Ravensbrook Gravure Packaging: 9.3
5. Gallons of inks, coatings and adhesives each plant received in 2026 that its stock counts and press logs leave unaccounted for, whole gallons:
   - Ashcombe Flexible Packaging: 11,835
   - Brinsley Label Works: 964
   - Carrow Gravure: 16,927
   - Dunsford Folding Cartons: 429
   - Elsworth Film Converting: 9,601
   - Garrowby Printing: 7,018
   - Hartmoor Packaging: 4,564
   - Ivers Lane Press: 419
   - Kelvedon Laminates: 31,109
   - Larkmoor Graphics: 9,409
   - Merrion Flexibles: 10,585
   - Norhaven Converting: 5,950
   - Pellworth Label: 436
   - Ravensbrook Gravure Packaging: 31,480

### deq_printing_press_voc_2026.csv

6. Fourteen rows, each with the facility number, the plant, its 2026 press VOC as in item 2 and Y or N for coverage.

### deq_printing_press_voc_2026.svg

7. Horizontal bar chart of the fourteen plants' 2026 press VOC, highest first, each bar labelled with its whole tons, a vertical line at 25 tons, the five covered plants in blue and the rest in grey.
