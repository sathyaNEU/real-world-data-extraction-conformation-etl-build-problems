## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a clinically integrated network's 2027 two-sided risk elections for its thirteen primary care practices, conformed from three commercial payers' claim, coverage and attribution feeds in three layouts, the network's clinician roster and master patient index, its performance standard and the payers' care coordination remittances).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Enter Ostrelwood, Callowglen, Thornelfield, Raddelview, Jesselford, Nerrincreek, Torrinridge, Mallowcrest and Garrowdale in the 2027 two-sided track and keep Haddelcrest, Birrelhaven, Wexelmoor and Prestelglen one-sided.**
On the payers' final 2026 attribution each of the nine comes in 5.4 to 8.4 per cent under its threshold, its October interim measure carried to the year by its own 2025 run-out at the same cut. Not Ostrelwood, Thornelfield and Jesselford alone, the interim measure taken as it stands: the October runs attribute only the members whose qualifying visit has happened, and the year adds the members who visit late, with a whole year of member months and a fraction of the cost. Not Haddelcrest, Birrelhaven and Wexelmoor as well, one pooled network run-out of 0.881: their members come early, or cost what the practice's other members cost.

## 2. Critical Components

1. 2025 network measure on the payers' final 2025 runs, USD per member month: Ostrelwood **723.67**; Callowglen **376.20**; Thornelfield **469.78**; Haddelcrest **779.07**; Birrelhaven **169.90**; Raddelview **455.26**; Jesselford **530.47**; Nerrincreek **368.78**; Wexelmoor **903.02**; Torrinridge **386.49**; Mallowcrest **161.13**; Prestelglen **747.82**; Garrowdale **433.05**.
2. 2026 threshold, 98 per cent of the benchmark, the 2025 measure to the cent times 1.052 to the cent (standard, section 3.4): Ostrelwood **746.07**; Callowglen **387.84**; Thornelfield **484.33**; Haddelcrest **803.19**; Birrelhaven **175.16**; Raddelview **469.35**; Jesselford **546.89**; Nerrincreek **380.20**; Wexelmoor **930.98**; Torrinridge **398.46**; Mallowcrest **166.12**; Prestelglen **770.98**; Garrowdale **446.46**.

## 3. Step-by-Step Solution

1. Conformed the three payers' claims at their current version (Merrinlake's voided originals out, Kesselcrest's adjusted lines out and its cents in dollars, Pemberglen's latest version), member months from the coverage files, and every run's TIN to its practice through lpn_primary_care_roster_2026-10.xlsx.
2. Took each practice's 2025 network measure on the payers' final 2025 runs (standard, section 3: claims first paid by 31 March 2026, each member's year capped at USD 250,000) and its threshold at 98 per cent of its benchmark, the measure to the cent times 1.052 to the cent (section 3.4).
3. Computed each practice's interim measure on the October runs (section 4.1, the factors in payer_completion_factors_2026-09.csv): taken as the 2026 figure it enters Ostrelwood, Thornelfield and Jesselford alone.
4. Re-ran the standard's attribution (section 2) on the 2025 professional claims at the October run's cut, qualifying services incurred by 31 August 2025 and paid by 30 September 2025, and took each practice's 2025 run-out, its 2025 measure over the January to August 2025 measure of the members so attributed: 0.822 to 0.996.
5. Carried each practice's interim measure by its own run-out: nine come in under their thresholds.
6. For the level 5 share, read each visit's paid level from its allowed amount against the payer's 2026 rate for its setting in payer_em_fee_schedules_2026.xlsx: Kesselcrest's reviewed 99215 visits allowed at its 99214 rate are level 4, and Merrinlake's modifier-25 visits with a same-day minor procedure by the same clinician, allowed at half the rate, keep their level.
7. For the fees, summed the three remittance files by the month each line covers: Pemberglen's by the month in its payment reference (PMH-CCF-TIN-YYYYMM-sequence), not its posting period, and Kesselcrest's only at the standard's USD 2.80 (its USD 6.50 lines are its Medicare Advantage fees).
8. Entered the nine practices under their thresholds in the two-sided track for 2027.

## 4. Deliverable Answers

### two_sided_track_elections_2027.xlsx

1. Elections, one row per practice (2026 benchmark, threshold, election):
   - Ostrelwood Internal Medicine: benchmark USD 761.30, threshold USD 746.07, two-sided
   - Callowglen Family Practice: benchmark USD 395.76, threshold USD 387.84, two-sided
   - Thornelfield Family Medicine: benchmark USD 494.21, threshold USD 484.33, two-sided
   - Haddelcrest Internal Medicine: benchmark USD 819.58, threshold USD 803.19, one-sided
   - Birrelhaven Children's Clinic: benchmark USD 178.73, threshold USD 175.16, one-sided
   - Raddelview Family Physicians: benchmark USD 478.93, threshold USD 469.35, two-sided
   - Jesselford Family Medicine: benchmark USD 558.05, threshold USD 546.89, two-sided
   - Nerrincreek Family Practice: benchmark USD 387.96, threshold USD 380.20, two-sided
   - Wexelmoor Internal Medicine: benchmark USD 949.98, threshold USD 930.98, one-sided
   - Torrinridge Family Medicine: benchmark USD 406.59, threshold USD 398.46, two-sided
   - Mallowcrest Pediatrics: benchmark USD 169.51, threshold USD 166.12, two-sided
   - Prestelglen Internal Medicine: benchmark USD 786.71, threshold USD 770.98, one-sided
   - Garrowdale Family Practice: benchmark USD 455.57, threshold USD 446.46, two-sided
2. Share of established-patient visits January to August 2026 the payers paid at level 5, per cent:
   - Ostrelwood Internal Medicine: 18.6
   - Callowglen Family Practice: 15.5
   - Thornelfield Family Medicine: 17.3
   - Haddelcrest Internal Medicine: 18.5
   - Birrelhaven Children's Clinic: 8.9
   - Raddelview Family Physicians: 17.2
   - Jesselford Family Medicine: 17.6
   - Nerrincreek Family Practice: 15.9
   - Wexelmoor Internal Medicine: 19.8
   - Torrinridge Family Medicine: 16.7
   - Mallowcrest Pediatrics: 8.9
   - Prestelglen Internal Medicine: 19.8
   - Garrowdale Family Practice: 16.6
3. Care coordination fees paid under the standard, by coverage quarter, USD:
   - Ostrelwood Internal Medicine: Q1 USD 18,566.10, Q2 USD 18,440.50, Q3 USD 18,296.10
   - Callowglen Family Practice: Q1 USD 13,614.60, Q2 USD 13,665.85, Q3 USD 13,559.05
   - Thornelfield Family Medicine: Q1 USD 18,309.90, Q2 USD 18,236.05, Q3 USD 18,030.30
   - Haddelcrest Internal Medicine: Q1 USD 16,789.85, Q2 USD 16,647.20, Q3 USD 16,483.15
   - Birrelhaven Children's Clinic: Q1 USD 16,911.10, Q2 USD 16,899.05, Q3 USD 16,693.70
   - Raddelview Family Physicians: Q1 USD 13,136.15, Q2 USD 13,125.25, Q3 USD 13,081.15
   - Jesselford Family Medicine: Q1 USD 17,117.35, Q2 USD 17,086.50, Q3 USD 16,967.50
   - Nerrincreek Family Practice: Q1 USD 12,289.40, Q2 USD 12,303.45, Q3 USD 12,165.30
   - Wexelmoor Internal Medicine: Q1 USD 16,393.50, Q2 USD 16,407.50, Q3 USD 16,179.75
   - Torrinridge Family Medicine: Q1 USD 14,672.05, Q2 USD 14,662.55, Q3 USD 14,496.00
   - Mallowcrest Pediatrics: Q1 USD 13,769.60, Q2 USD 13,908.80, Q3 USD 13,673.70
   - Prestelglen Internal Medicine: Q1 USD 15,209.10, Q2 USD 15,065.05, Q3 USD 14,973.65
   - Garrowdale Family Practice: Q1 USD 12,455.45, Q2 USD 12,531.70, Q3 USD 12,438.95

### practice_cost_vs_benchmark_2026.png

1. Horizontal bar chart of each practice's projected 2026 network measure as the per cent above or below its threshold, the nine entering practices shaded apart, with each practice's October interim measure marked beside its bar.
