# task193 submission

## Tags

**Domain:** Pharmacology, pharmacoepidemiology and safety (safety signal detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Refer 7 of the 20 candidate pairs to formal signal assessment in the quarter beginning 1 January 2027: Dalvextin and loop diuretic; Pirenoxol and acid-suppressant; Ternivast and gout treatment; Oxelumab and antidepressant; Hestroban and antiemetic; Kirunelle and hypnotic; Sovraxil and topical corticosteroid.**
The expected after-count comes from the window's own first-receipt dates, so the lowest referred multiple is 1.31 and the nearest pair on the wrong side of the line is Dalvextin and acid-suppressant at 1.13. Not the 10 pairs an equal-chance expectation refers, which adds Varenadol and antiemetic; Varenadol and acid-suppressant; Varenadol and hypnotic; Admirabin and loop diuretic; Admirabin and antidepressant. Not those 10 pairs less Ternivast and gout treatment; Oxelumab and antidepressant, which are the real signals an equal-chance expectation hides.

## 2. Critical Components

1. The screen's candidate pairs are **20** of the 23 pairs in Annexes A and B
2. The pairs referred are **7**
3. The pairs an equal-chance expectation refers are **10**
4. The pairs it refers that this run does not are **5**, and the pairs it hides are **2**

## 3. Step-by-Step Solution

1. Stacked dispensings_2023_2025.csv and dispensings_2025_2026.csv on the layouts register_release_notes.json gives and counted a re-sent line once, as those notes require: 12995 person keys appear across the extract.
2. Folded the retired person keys in person_key_crosswalk.csv onto their current keys and mapped each package code to its treatment through package_index.csv at the date of the dispensing, per section 2.4.
3. Took each patient's earliest dispensing in each treatment as the first receipt and dropped first receipts falling in the clearance period, per sections 2.2 and 2.3.
4. Built each pair in screen_annexes.csv from the patients whose two first receipts both fall in the screen window and not on the same day, per section 2.5: 20 of the 23 pairs have at least 25 patients.
5. Took the number expected if the product had no bearing on when the marker treatment is first received from the pair's own first-receipt dates, which the window makes unequal because two products were first marketed inside it and two lose their authorisation inside it.
6. Applied section 3.2: 7 pairs reach 1.25 times that expected number and none of them is under assessment in signal_tracker_export.csv.
7. Compared with an equal-chance expectation, which refers 10 pairs: 5 of them fall below the line here and 2 pairs below its line clear this one.
8. Refer the 7 pairs for assessment in the quarter beginning 1 January 2027.

## 4. Deliverable Answers

### sequence_screen_2027Q1.xlsx

1. The 23 screened pairs in the order of the screen sheet, with the pair's patients, the patients in whom the marker treatment came after the product, the patients in whom it came before, and the referral:
   - Dalvextin and acid-suppressant: 137 patients, 75 after, 62 before, referred no
   - Dalvextin and gout treatment: 135 patients, 73 after, 62 before, referred no
   - Dalvextin and loop diuretic: 244 patients, 183 after, 61 before, referred yes
   - Pirenoxol and acid-suppressant: 271 patients, 196 after, 75 before, referred yes
   - Pirenoxol and antidepressant: 167 patients, 94 after, 73 before, referred no
   - Pirenoxol and hypnotic: 134 patients, 74 after, 60 before, referred no
   - Ternivast and antiemetic: 257 patients, 62 after, 195 before, referred no
   - Ternivast and gout treatment: 378 patients, 192 after, 186 before, referred yes
   - Ternivast and hypnotic: 251 patients, 53 after, 198 before, referred no
   - Oxelumab and loop diuretic: 298 patients, 87 after, 211 before, referred no
   - Oxelumab and antidepressant: 523 patients, 296 after, 227 before, referred yes
   - Oxelumab and topical corticosteroid: 350 patients, 123 after, 227 before, referred no
   - Varenadol and antiemetic: 226 patients, 179 after, 47 before, referred no
   - Varenadol and acid-suppressant: 245 patients, 198 after, 47 before, referred no
   - Varenadol and hypnotic: 235 patients, 203 after, 32 before, referred no
   - Hestroban and antiemetic: 329 patients, 231 after, 98 before, referred yes
   - Hestroban and antipsychotic: 7 patients, 1 after, 6 before, below the 25-patient minimum
   - Kirunelle and hypnotic: 229 patients, 164 after, 65 before, referred yes
   - Kirunelle and antipsychotic: 7 patients, 5 after, 2 before, below the 25-patient minimum
   - Admirabin and loop diuretic: 201 patients, 153 after, 48 before, referred no
   - Admirabin and antidepressant: 214 patients, 167 after, 47 before, referred no
   - Sovraxil and topical corticosteroid: 432 patients, 337 after, 95 before, referred yes
   - Sovraxil and antipsychotic: 8 patients, 4 after, 4 before, below the 25-patient minimum
2. Pairs referred: 7.
3. Nearest pair on the wrong side of the referral line: Dalvextin and acid-suppressant.
4. Lines accepted, lines rejected and median days from dispensing to submission, by chain and quarter of dispensing, whole counts and days to one decimal:
   - APK, 2025 Q4: 4588 accepted, 136 rejected, 1.0 days
   - APK, 2026 Q1: 4101 accepted, 128 rejected, 2.0 days
   - APK, 2026 Q2: 3966 accepted, 128 rejected, 2.0 days
   - APK, 2026 Q3: 4303 accepted, 136 rejected, 2.0 days
   - DSA, 2025 Q4: 3548 accepted, 103 rejected, 3.0 days
   - DSA, 2026 Q1: 3067 accepted, 119 rejected, 3.0 days
   - DSA, 2026 Q2: 3016 accepted, 96 rejected, 4.0 days
   - DSA, 2026 Q3: 3190 accepted, 86 rejected, 4.0 days
   - NOR, 2025 Q4: 2441 accepted, 74 rejected, 4.0 days
   - NOR, 2026 Q1: 2300 accepted, 65 rejected, 5.0 days
   - NOR, 2026 Q2: 2200 accepted, 66 rejected, 6.0 days
   - NOR, 2026 Q3: 2326 accepted, 53 rejected, 5.0 days
   - VST, 2025 Q4: 1678 accepted, 66 rejected, 6.0 days
   - VST, 2026 Q1: 1541 accepted, 39 rejected, 7.0 days
   - VST, 2026 Q2: 1483 accepted, 45 rejected, 6.0 days
   - VST, 2026 Q3: 1666 accepted, 41 rejected, 8.0 days
5. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, doses to one decimal and fees to the nearest krone:
   - Nordlys Pharma A/S (H1): 184847.5 DDD, 284155 kroner
   - Bregnholt Laegemidler A/S (H2): 176719.6 DDD, 275837 kroner
   - Vindeby Therapeutics ApS (H3): 309372.0 DDD, 411485 kroner
   - Soegaard Medica A/S (H4): 124630.3 DDD, 184942 kroner
   - Kastholm Pharma A/S (H5): 101506.8 DDD, 151463 kroner
   - Ellevang Biosciences A/S (H6): 283991.0 DDD, 362901 kroner
   - Strandby Farma ApS (H7): 75789.0 DDD, 112168 kroner
6. Patients with a first receipt of a screened product in the window and the share of them with a first marker-treatment receipt in it, by region and age band at 1 October 2025, shares to one decimal:
   - Hovedstaden, 18-39: 709 patients, 69.0 per cent
   - Hovedstaden, 40-59: 561 patients, 72.4 per cent
   - Hovedstaden, 60-74: 478 patients, 78.9 per cent
   - Hovedstaden, 75 and over: 568 patients, 80.8 per cent
   - Midtjylland, 18-39: 538 patients, 70.1 per cent
   - Midtjylland, 40-59: 456 patients, 74.1 per cent
   - Midtjylland, 60-74: 331 patients, 80.1 per cent
   - Midtjylland, 75 and over: 391 patients, 79.0 per cent
   - Nordjylland, 18-39: 244 patients, 69.7 per cent
   - Nordjylland, 40-59: 212 patients, 70.8 per cent
   - Nordjylland, 60-74: 123 patients, 79.7 per cent
   - Nordjylland, 75 and over: 172 patients, 82.0 per cent
   - Sjaelland, 18-39: 296 patients, 65.9 per cent
   - Sjaelland, 40-59: 272 patients, 74.6 per cent
   - Sjaelland, 60-74: 221 patients, 78.7 per cent
   - Sjaelland, 75 and over: 243 patients, 72.8 per cent
   - Syddanmark, 18-39: 440 patients, 63.0 per cent
   - Syddanmark, 40-59: 444 patients, 78.2 per cent
   - Syddanmark, 60-74: 282 patients, 75.2 per cent
   - Syddanmark, 75 and over: 379 patients, 79.9 per cent
   - not stated, 18-39: 65 patients, 72.3 per cent
   - not stated, 40-59: 46 patients, 69.6 per cent
   - not stated, 60-74: 46 patients, 78.3 per cent
   - not stated, 75 and over: 30 patients, 70.0 per cent

### order_shares_by_pair.png

1. One horizontal bar per screened pair for the share of its patients who received the marker treatment after the product, longest first, with each pair's referral threshold marked at 1.25 times its expected share and the referred pairs in the darker fill.
2. Title states that 7 of the 20 candidate pairs clear the referral line.
