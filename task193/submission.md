# task193 submission

## Tags

**Domain:** Pharmacology, pharmacoepidemiology and safety (safety signal detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Refer 7 of the 20 candidate pairs to formal signal assessment in the quarter beginning 1 January 2027: Dalvextin and loop diuretic; Pirenoxol and acid-suppressant; Ternivast and gout treatment; Oxelumab and antidepressant; Hestroban and antiemetic; Kirunelle and hypnotic; Sovraxil and topical corticosteroid.**
The expected after-count comes from the window's own first-receipt dates, so the lowest referred multiple is 1.36 and the nearest pair on the wrong side of the line is Dalvextin and acid-suppressant at 1.03. Not the 10 pairs an equal-chance expectation refers, which adds Varenadol and antiemetic; Varenadol and acid-suppressant; Varenadol and hypnotic; Admirabin and loop diuretic; Admirabin and antidepressant. Not those 10 pairs less Ternivast and gout treatment; Oxelumab and antidepressant, which are the real signals an equal-chance expectation hides.

## 2. Critical Components

1. The screen's candidate pairs are **20** of the 23 pairs in Annexes A and B
2. The pairs referred are **7**
3. The pairs an equal-chance expectation refers are **10**
4. The pairs it refers that this run does not are **5**, and the pairs it hides are **2**

## 3. Step-by-Step Solution

1. Stacked dispensings_2023_2025.csv and dispensings_2025_2026.csv on the layouts register_release_notes.json gives and counted a re-sent line once, as those notes require: 16991 person keys appear across the extract.
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
   - Dalvextin and acid-suppressant: 195 patients, 99 after, 96 before, referred no
   - Dalvextin and gout treatment: 204 patients, 110 after, 94 before, referred no
   - Dalvextin and loop diuretic: 375 patients, 277 after, 98 before, referred yes
   - Pirenoxol and acid-suppressant: 363 patients, 273 after, 90 before, referred yes
   - Pirenoxol and antidepressant: 169 patients, 94 after, 75 before, referred no
   - Pirenoxol and hypnotic: 172 patients, 91 after, 81 before, referred no
   - Ternivast and antiemetic: 346 patients, 71 after, 275 before, referred no
   - Ternivast and gout treatment: 546 patients, 268 after, 278 before, referred yes
   - Ternivast and hypnotic: 324 patients, 63 after, 261 before, referred no
   - Oxelumab and loop diuretic: 423 patients, 147 after, 276 before, referred no
   - Oxelumab and antidepressant: 694 patients, 383 after, 311 before, referred yes
   - Oxelumab and topical corticosteroid: 502 patients, 143 after, 359 before, referred no
   - Varenadol and antiemetic: 279 patients, 227 after, 52 before, referred no
   - Varenadol and acid-suppressant: 301 patients, 229 after, 72 before, referred no
   - Varenadol and hypnotic: 269 patients, 208 after, 61 before, referred no
   - Hestroban and antiemetic: 480 patients, 346 after, 134 before, referred yes
   - Hestroban and antipsychotic: 7 patients, 3 after, 4 before, below the 25-patient minimum
   - Kirunelle and hypnotic: 339 patients, 252 after, 87 before, referred yes
   - Kirunelle and antipsychotic: 13 patients, 7 after, 6 before, below the 25-patient minimum
   - Admirabin and loop diuretic: 210 patients, 159 after, 51 before, referred no
   - Admirabin and antidepressant: 268 patients, 215 after, 53 before, referred no
   - Sovraxil and topical corticosteroid: 631 patients, 496 after, 135 before, referred yes
   - Sovraxil and antipsychotic: 17 patients, 11 after, 6 before, below the 25-patient minimum
2. Pairs referred: 7.
3. Nearest pair on the wrong side of the referral line: Dalvextin and acid-suppressant.
4. Lines accepted, lines rejected and median days from dispensing to submission, by chain and quarter of dispensing, whole counts and days to one decimal:
   - APK, 2025 Q4: 5985 accepted, 66 rejected, 3.0 days
   - APK, 2026 Q1: 5476 accepted, 67 rejected, 5.0 days
   - APK, 2026 Q2: 5554 accepted, 42 rejected, 4.0 days
   - APK, 2026 Q3: 5732 accepted, 58 rejected, 5.0 days
   - DSA, 2025 Q4: 4673 accepted, 66 rejected, 3.0 days
   - DSA, 2026 Q1: 4119 accepted, 71 rejected, 4.0 days
   - DSA, 2026 Q2: 4082 accepted, 39 rejected, 4.0 days
   - DSA, 2026 Q3: 4344 accepted, 62 rejected, 6.0 days
   - NOR, 2025 Q4: 3386 accepted, 73 rejected, 5.0 days
   - NOR, 2026 Q1: 3064 accepted, 64 rejected, 4.0 days
   - NOR, 2026 Q2: 2875 accepted, 82 rejected, 6.0 days
   - NOR, 2026 Q3: 3203 accepted, 35 rejected, 6.0 days
   - VST, 2025 Q4: 2260 accepted, 28 rejected, 7.0 days
   - VST, 2026 Q1: 2002 accepted, 18 rejected, 7.0 days
   - VST, 2026 Q2: 1933 accepted, 22 rejected, 7.0 days
   - VST, 2026 Q3: 1997 accepted, 18 rejected, 8.0 days
5. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, doses to one decimal and fees to the nearest krone:
   - Nordlys Pharma A/S (H1): 265159.0 DDD, 342547 kroner
   - Bregnholt Laegemidler A/S (H2): 402993.0 DDD, 530098 kroner
   - Vindeby Therapeutics ApS (H3): 407656.0 DDD, 544754 kroner
   - Soegaard Medica A/S (H4): 383410.0 DDD, 476809 kroner
   - Kastholm Pharma A/S (H5): 595520.0 DDD, 747311 kroner
   - Ellevang Biosciences A/S (H6): 1027098.0 DDD, 1067868 kroner
   - Strandby Farma ApS (H7): 227031.0 DDD, 332600 kroner
6. Patients with a first receipt of a screened product in the window and the share of them with a first marker-treatment receipt in it, by region and age band at 1 October 2025, shares to one decimal:
   - Hovedstaden, 18-29: 480 patients, 69.0 per cent
   - Hovedstaden, 30-49: 797 patients, 72.3 per cent
   - Hovedstaden, 50-64: 564 patients, 80.0 per cent
   - Hovedstaden, 65 and over: 1097 patients, 80.6 per cent
   - Midtjylland, 18-29: 357 patients, 68.6 per cent
   - Midtjylland, 30-49: 621 patients, 73.1 per cent
   - Midtjylland, 50-64: 459 patients, 76.9 per cent
   - Midtjylland, 65 and over: 833 patients, 77.9 per cent
   - Nordjylland, 18-29: 172 patients, 65.7 per cent
   - Nordjylland, 30-49: 277 patients, 72.9 per cent
   - Nordjylland, 50-64: 198 patients, 72.7 per cent
   - Nordjylland, 65 and over: 339 patients, 81.4 per cent
   - Sjaelland, 18-29: 206 patients, 73.3 per cent
   - Sjaelland, 30-49: 391 patients, 74.7 per cent
   - Sjaelland, 50-64: 311 patients, 75.9 per cent
   - Sjaelland, 65 and over: 542 patients, 80.8 per cent
   - Syddanmark, 18-29: 339 patients, 69.6 per cent
   - Syddanmark, 30-49: 550 patients, 72.9 per cent
   - Syddanmark, 50-64: 433 patients, 75.5 per cent
   - Syddanmark, 65 and over: 692 patients, 79.9 per cent
   - not stated, 18-29: 38 patients, 68.4 per cent
   - not stated, 30-49: 75 patients, 77.3 per cent
   - not stated, 50-64: 49 patients, 75.5 per cent
   - not stated, 65 and over: 75 patients, 78.7 per cent

### order_shares_by_pair.png

1. One horizontal bar for each of the 23 screened pairs for the share of its patients who received the marker treatment after the product, longest first, with the 7 referred pairs in the darker fill and the other 16 in the lighter one.
2. The bars in order, longest share first: Varenadol + antiemetic 81.4; Admirabin + antidepressant 80.2; Sovraxil + topical corticosteroid 78.6; Varenadol + hypnotic 77.3; Varenadol + acid-suppressant 76.1; Admirabin + loop diuretic 75.7; Pirenoxol + acid-suppressant 75.2; Kirunelle + hypnotic 74.3; Dalvextin + loop diuretic 73.9; Hestroban + antiemetic 72.1; Sovraxil + antipsychotic 64.7; Pirenoxol + antidepressant 55.6; Oxelumab + antidepressant 55.2; Dalvextin + gout treatment 53.9; Kirunelle + antipsychotic 53.8; Pirenoxol + hypnotic 52.9; Dalvextin + acid-suppressant 50.8; Ternivast + gout treatment 49.1; Hestroban + antipsychotic 42.9; Oxelumab + loop diuretic 34.8; Oxelumab + topical corticosteroid 28.5; Ternivast + antiemetic 20.5; Ternivast + hypnotic 19.4.
3. Title states that 7 of the 20 candidate pairs clear the referral line.
