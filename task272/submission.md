## Tags

> **Domain:** General Statistics & Data Science (exploratory data analysis and distribution assessment).
> **Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Configure 4 batch-compounded products for gravimetric verification of every dose at the April 2027 cutover: Cefazolin 2 g in 20 mL syringe; Cefoxitin 2 g in 20 mL syringe; Phenylephrine 100 mcg/mL 10 mL syringe; Midazolam 1 mg/mL 50 mL syringe.** Each made more than 10 out-of-tolerance doses per hundred thousand doses made in 2026 under PH-QP-07 3.1 once every dose is placed on its set at the litres the set had pumped. The other 8 stay on SC-SOP-12's checks. Not Cefoxitin 2 g in 20 mL syringe; Ampicillin 2 g in 50 mL bag; Piperacillin-tazobactam 4.5 g in 100 mL bag; Vancomycin 1 g in 200 mL bag; Midazolam 1 mg/mL 50 mL syringe, the products a normal fit to the weighed doses flags.

## 2. Critical Components

1. On PC-1, PC-2 and PC-3 a product's weighed doses fall in a straight line with the litres the set had pumped since its set-up, about a start that varies from set to set; on PC-4 they do not move.
2. Each completed dose's chance of lying outside its tolerance, taken at the litres its set had pumped and summed over every dose made, gives each product's 2026 rate per hundred thousand doses made:
   - Cefoxitin 2 g in 20 mL syringe: 451.2
   - Phenylephrine 100 mcg/mL 10 mL syringe: 266.6
   - Cefazolin 2 g in 20 mL syringe: 131.4
   - Midazolam 1 mg/mL 50 mL syringe: 43.7
   - Ampicillin 2 g in 50 mL bag: 0.2
   - Cefazolin 1 g in 10 mL syringe: under 0.1
   - Ephedrine 5 mg/mL 10 mL syringe: under 0.1
   - Ketamine 10 mg/mL 10 mL syringe: under 0.1
   - Piperacillin-tazobactam 4.5 g in 100 mL bag: under 0.1
   - Vancomycin 1 g in 200 mL bag: under 0.1
   - Ondansetron 8 mg in 50 mL bag: under 0.1
   - Heparin 1,000 units/mL 5 mL syringe: under 0.1
3. The products over 10 are Cefazolin 2 g in 20 mL syringe; Cefoxitin 2 g in 20 mL syringe; Phenylephrine 100 mcg/mL 10 mL syringe; Midazolam 1 mg/mL 50 mL syringe; every other product is under 3.

## 3. Step-by-Step Solution

1. Read compounding_equipment_register.csv's station for each serial (PC-3's two serials, before and after 14 July, are one compounder) and compounded_product_master.xlsx's tolerance, specific gravity and tare for each product.
2. Took the completed doses in compounder_dose_log_2026.parquet (fill times in UTC) and put each on the set its device had installed: the latest SET_UP in compounder_events_2026.csv before the dose, a re-seated set (the same set lot) being one set.
3. For each dose, the litres its set had pumped before it: the programmed volumes of the set's earlier completed doses.
4. Tied each weighed dose in gravimetric_check_register_2026.xlsx to its dose by batch and dose number; delivered volume is the net weight (gross weight less the container tare to 30 June) divided by the specific gravity, as a per cent of the labelled volume.
5. For each product fitted the weighed doses' per cent deviation as the set's start plus a loss per litre pumped (one slope across the product's sets, the start varying from set to set about its mean, a dose-to-dose scatter about the line).
6. Summed over every completed dose the normal chance of lying outside the tolerance at its litres pumped, with the start's spread and the scatter, per hundred thousand doses made; the call is the products over 10.
7. Counted each station's completed doses by Ontario-local month and each product's sets (distinct set lots on their devices, the product of the doses filled on them).

## 4. Deliverable Answers

### gravimetric_verification_2027.pdf

1. Products configured for gravimetric verification of every dose: Cefazolin 2 g in 20 mL syringe; Cefoxitin 2 g in 20 mL syringe; Phenylephrine 100 mcg/mL 10 mL syringe; Midazolam 1 mg/mL 50 mL syringe.
2. Every batch-compounded product marked in or out:
   - Cefoxitin 2 g in 20 mL syringe: in
   - Phenylephrine 100 mcg/mL 10 mL syringe: in
   - Cefazolin 2 g in 20 mL syringe: in
   - Midazolam 1 mg/mL 50 mL syringe: in
   - Ampicillin 2 g in 50 mL bag: out
   - Cefazolin 1 g in 10 mL syringe: out
   - Ephedrine 5 mg/mL 10 mL syringe: out
   - Ketamine 10 mg/mL 10 mL syringe: out
   - Piperacillin-tazobactam 4.5 g in 100 mL bag: out
   - Vancomycin 1 g in 200 mL bag: out
   - Ondansetron 8 mg in 50 mL bag: out
   - Heparin 1,000 units/mL 5 mL syringe: out
3. Chart: each product's 2026 out-of-tolerance rate per hundred thousand doses made against the limit of 10, the products going on verification in red.

### compounding_review_2026.csv

1. Each compounder's doses made in each month of 2026 (Ontario local time), whole numbers:
   - PC-1: Jan 16,917, Feb 18,158, Mar 17,563, Apr 17,705, May 17,407, Jun 17,684, Jul 18,396, Aug 17,238, Sep 17,974, Oct 19,300, Nov 17,743, Dec 17,131
   - PC-2: Jan 11,693, Feb 9,940, Mar 11,892, Apr 11,513, May 10,794, Jun 12,520, Jul 11,785, Aug 10,604, Sep 12,060, Oct 11,553, Nov 11,379, Dec 11,868
   - PC-3: Jan 4,977, Feb 4,196, Mar 5,718, Apr 5,105, May 4,820, Jun 5,179, Jul 5,379, Aug 4,686, Sep 5,105, Oct 5,297, Nov 5,111, Dec 4,806
   - PC-4: Jan 3,707, Feb 3,931, Mar 3,573, Apr 3,663, May 4,030, Jun 3,341, Jul 4,143, Aug 2,913, Sep 3,101, Oct 4,088, Nov 3,947, Dec 4,581
   - GC-1: Jan 1,673, Feb 1,539, Mar 1,898, Apr 2,063, May 1,617, Jun 1,483, Jul 1,674, Aug 1,669, Sep 1,846, Oct 1,560, Nov 1,458, Dec 1,536
2. The sets each product filled on PC-1 to PC-4 used in 2026, whole numbers:
   - Cefazolin 2 g in 20 mL syringe: 441
   - Cefazolin 1 g in 10 mL syringe: 148
   - Cefoxitin 2 g in 20 mL syringe: 354
   - Phenylephrine 100 mcg/mL 10 mL syringe: 420
   - Ephedrine 5 mg/mL 10 mL syringe: 169
   - Ketamine 10 mg/mL 10 mL syringe: 130
   - Ampicillin 2 g in 50 mL bag: 271
   - Piperacillin-tazobactam 4.5 g in 100 mL bag: 272
   - Vancomycin 1 g in 200 mL bag: 172
   - Ondansetron 8 mg in 50 mL bag: 114
   - Midazolam 1 mg/mL 50 mL syringe: 167
   - Heparin 1,000 units/mL 5 mL syringe: 166
