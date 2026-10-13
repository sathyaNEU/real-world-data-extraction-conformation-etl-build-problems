# task454 submission

## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (the acquisition cost of the pharmacy claims that do not link to a priced NDC, filled within product and package type).
**Analytical objective:** Data Extraction & Conformation (ETL) (the claims extract, the State AAC rate file, the drug file and the class list conformed into one table of each candidate class's ingredient spread; the FY2026 summary and the extract conformed into the budget table).

## 1. Final Recommendation

**We propose Anticonvulsants for the State Maximum Allowable Cost list from 1 July 2027: its ingredient spread over fills from April 2026 to March 2027 was $43,000, the largest of the twelve candidate classes and 1.43 times Antipsychotics' $30,000.**

Not Antipsychotics: it leads only when the claims no AAC rate covers are costed at their product's rate, which the retail bottles set, while 86 per cent of that unpriced cost is on unit-dose cartons that cost 1.90 times the bottle per unit, so the long-term care classes' cartons are booked below cost and Antipsychotics' spread rises to $65,000. Not Dementia agents or Antiparkinson agents, next at $24,000 and $23,000.

## 2. Critical Components

1. **43%** of the candidate classes' ingredient cost over the window was paid on NDCs with no AAC rate in effect, **86%** of it on unit-dose cartons.
2. A unit-dose carton costs **1.90** times the bottle of the same product per unit, the median carton-to-bottle rate ratio of the products with both priced.
3. Anticonvulsants' ingredient spread is **$43,000** and Antipsychotics' **$30,000**.

## 3. Step-by-Step Solution

1. Kept the 224,851 transactions of corvane_ffs_claims_paid_2026-04_2027-04.csv on fills from 1 April 2026 to 31 March 2027 (of 229,247), netted the B2 reversals, and placed each NDC in its class through state_drug_file_2027-04.xlsx (its ten-digit NDCs converted to eleven digits by their configuration) and state_drug_class_list_2027.xlsx.
2. Costed each claim's units at the AAC rate in effect for its NDC on the fill date (state_aac_rates_2025-04_2027-03.csv, Attachment C, C.2): 43 per cent of the ingredient cost was on NDCs with no rate in effect, 86 per cent of that on unit-dose cartons (the drug file's package description).
3. Costed each unpriced NDC's units at the median rate in effect that month for the priced NDCs of the same product and package type, and a carton with no priced carton at its bottles' median times 1.90, the median carton-to-bottle ratio of the products with both priced.
4. Summed each class's ingredient cost paid less acquisition cost (C.5), compared the classes unrounded (C.4) and rounded each to the nearest thousand dollars: Anticonvulsants $43,000, Antipsychotics $30,000, Dementia agents $24,000, Antiparkinson agents $23,000.
5. For the FY2026 workbook, took corvane_generic_utilization_fy2026.xlsx (the transactions paid through 20 April 2026) by NDC, placed each NDC through the drug file and the class list in force from 1 January 2027 (smac_update_request_2027-03-08.pdf), and added the extract's 1,265 transactions on FY2026 fills paid after 20 April 2026; its 3,131 earlier ones are already in the summary.
6. Recommendation: propose Anticonvulsants for the 1 July 2027 update.

## 4. Deliverable Answers

### smac_class_addition_2027-07.docx

1. The proposed class: Anticonvulsants (C107).
2. Each candidate class's ingredient spread, fills April 2026 to March 2027, nearest thousand dollars:
   - Anticonvulsants: $43,000
   - Antipsychotics: $30,000
   - Dementia agents: $24,000
   - Antiparkinson agents: $23,000
   - Urinary antispasmodics: $15,000
   - Loop diuretics: $9,000
   - Antiemetics: $5,000
   - Benzodiazepines: $3,000
   - Beta blockers: $3,000
   - Oral corticosteroids: $3,000
   - Antidepressants, SSRI: $2,000
   - Skeletal muscle relaxants: $2,000
3. A horizontal bar chart of the twelve classes' spreads, largest first, the proposed class in dark (Figure 1).

### smac_candidate_classes_fy2026.xlsx

4. Each candidate class's claims, units dispensed and ingredient cost paid, fills April 2025 to March 2026:
   - Anticonvulsants (C107): 40,046 claims, 2,412,350 units, $203,083
   - Antipsychotics (C114): 33,990 claims, 1,284,660 units, $214,917
   - Dementia agents (C121): 11,748 claims, 415,022 units, $102,160
   - Antidepressants, SSRI (C128): 17,547 claims, 876,403 units, $34,393
   - Beta blockers (C135): 19,706 claims, 919,853 units, $49,485
   - Loop diuretics (C142): 17,780 claims, 794,219 units, $50,911
   - Benzodiazepines (C149): 10,639 claims, 471,068 units, $24,878
   - Antiparkinson agents (C156): 11,403 claims, 472,508 units, $129,520
   - Urinary antispasmodics (C163): 9,414 claims, 400,145 units, $121,421
   - Skeletal muscle relaxants (C170): 16,105 claims, 760,304 units, $47,287
   - Antiemetics (C177): 10,653 claims, 504,780 units, $48,687
   - Oral corticosteroids (C184): 10,247 claims, 519,328 units, $54,960
