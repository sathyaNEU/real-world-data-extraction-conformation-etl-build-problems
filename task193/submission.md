# task193 submission

## Tags

**Domain:** Pharmacology, pharmacoepidemiology and safety (safety signal detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Refer 7 of the 20 candidate pairs to formal signal assessment in the quarter beginning 1 January 2027: Dalvextin and loop diuretic; Pirenoxol and acid-suppressant; Ternivast and gout treatment; Oxelumab and antidepressant; Hestroban and antiemetic; Kirunelle and hypnotic; Sovraxil and topical corticosteroid.**
The expected after-count comes from the window's own first-receipt dates, so the lowest referred multiple is 1.36 and the nearest pair on the wrong side of the line is Dalvextin and acid-suppressant at 1.03. Not the 10 pairs an equal-chance expectation refers: it adds Varenadol and antiemetic; Varenadol and acid-suppressant; Varenadol and hypnotic; Admirabin and loop diuretic; Admirabin and antidepressant, which the dates refuse. And it misses Ternivast and gout treatment; Oxelumab and antidepressant, which are real signals it hides because both products were first marketed inside the window.

## 2. Critical Components

1. The screen's candidate pairs are **20** of the 23 pairs in Annexes A and B
2. The pairs referred are **7**
3. The pairs an equal-chance expectation refers are **10**
4. The pairs it refers that this run does not are **5**, and the pairs it hides are **2**

## 3. Step-by-Step Solution

1. Stacked dispensings_2023_2025.csv and dispensings_2025_2026.csv on the layouts register_release_notes.json gives and counted a re-sent line once, as those notes require: 16957 person keys appear across the extract.
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
   - Pirenoxol and hypnotic: 171 patients, 91 after, 80 before, referred no
   - Ternivast and antiemetic: 346 patients, 71 after, 275 before, referred no
   - Ternivast and gout treatment: 546 patients, 268 after, 278 before, referred yes
   - Ternivast and hypnotic: 322 patients, 63 after, 259 before, referred no
   - Oxelumab and loop diuretic: 423 patients, 147 after, 276 before, referred no
   - Oxelumab and antidepressant: 694 patients, 383 after, 311 before, referred yes
   - Oxelumab and topical corticosteroid: 501 patients, 142 after, 359 before, referred no
   - Varenadol and antiemetic: 278 patients, 227 after, 51 before, referred no
   - Varenadol and acid-suppressant: 301 patients, 229 after, 72 before, referred no
   - Varenadol and hypnotic: 269 patients, 208 after, 61 before, referred no
   - Hestroban and antiemetic: 480 patients, 346 after, 134 before, referred yes
   - Hestroban and antipsychotic: 7 patients, 3 after, 4 before, below the 25-patient minimum
   - Kirunelle and hypnotic: 339 patients, 252 after, 87 before, referred yes
   - Kirunelle and antipsychotic: 13 patients, 7 after, 6 before, below the 25-patient minimum
   - Admirabin and loop diuretic: 210 patients, 159 after, 51 before, referred no
   - Admirabin and antidepressant: 268 patients, 215 after, 53 before, referred no
   - Sovraxil and topical corticosteroid: 629 patients, 494 after, 135 before, referred yes
   - Sovraxil and antipsychotic: 17 patients, 11 after, 6 before, below the 25-patient minimum
2. Pairs referred: 7.
3. Lines accepted, lines rejected and median days from dispensing to submission, by chain and quarter of dispensing, whole counts and days to one decimal:
   - APK, 2025 Q4: 5568 accepted, 54 rejected, 2.0 days
   - APK, 2026 Q1: 5775 accepted, 88 rejected, 4.0 days
   - APK, 2026 Q2: 5874 accepted, 53 rejected, 4.0 days
   - APK, 2026 Q3: 4657 accepted, 44 rejected, 6.0 days
   - DSA, 2025 Q4: 3002 accepted, 42 rejected, 4.0 days
   - DSA, 2026 Q1: 2764 accepted, 55 rejected, 3.0 days
   - DSA, 2026 Q2: 3220 accepted, 35 rejected, 7.0 days
   - DSA, 2026 Q3: 2620 accepted, 30 rejected, 6.0 days
   - NOR, 2025 Q4: 4189 accepted, 93 rejected, 6.0 days
   - NOR, 2026 Q1: 3145 accepted, 67 rejected, 7.0 days
   - NOR, 2026 Q2: 2888 accepted, 92 rejected, 6.0 days
   - NOR, 2026 Q3: 4796 accepted, 78 rejected, 6.0 days
   - VST, 2025 Q4: 3550 accepted, 39 rejected, 6.0 days
   - VST, 2026 Q1: 2941 accepted, 46 rejected, 7.0 days
   - VST, 2026 Q2: 2441 accepted, 26 rejected, 9.0 days
   - VST, 2026 Q3: 3190 accepted, 34 rejected, 6.0 days
4. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, doses to one decimal and fees to the nearest krone:
   - Nordlys Pharma A/S (H1): 282746.0 DDD, 346853 kroner
   - Bregnholt Laegemidler A/S (H2): 502994.5 DDD, 619913 kroner
   - Vindeby Therapeutics ApS (H3): 434430.0 DDD, 552260 kroner
   - Soegaard Medica A/S (H4): 204660.0 DDD, 316874 kroner
   - Kastholm Pharma A/S (H5): 626952.0 DDD, 746051 kroner
   - Ellevang Biosciences A/S (H6): 1090310.0 DDD, 1109616 kroner
   - Strandby Farma ApS (H7): 121180.5 DDD, 187345 kroner
5. Patients with a first receipt of a screened product in the window and the share of them with a first marker-treatment receipt in it, by region and age band at 1 October 2025, shares to one decimal:
   - Hovedstaden, 18-24: 249 patients, 70.7 per cent
   - Hovedstaden, 25-44: 752 patients, 68.5 per cent
   - Hovedstaden, 45-54: 386 patients, 76.4 per cent
   - Hovedstaden, 55 and over: 1361 patients, 81.0 per cent
   - Midtjylland, 18-24: 208 patients, 69.2 per cent
   - Midtjylland, 25-44: 599 patients, 69.3 per cent
   - Midtjylland, 45-54: 277 patients, 78.7 per cent
   - Midtjylland, 55 and over: 1117 patients, 77.5 per cent
   - Nordjylland, 18-24: 94 patients, 69.1 per cent
   - Nordjylland, 25-44: 306 patients, 69.3 per cent
   - Nordjylland, 45-54: 175 patients, 73.7 per cent
   - Nordjylland, 55 and over: 523 patients, 79.5 per cent
   - Sjaelland, 18-24: 133 patients, 69.2 per cent
   - Sjaelland, 25-44: 386 patients, 76.9 per cent
   - Sjaelland, 45-54: 221 patients, 71.5 per cent
   - Sjaelland, 55 and over: 801 patients, 79.3 per cent
   - Syddanmark, 18-24: 194 patients, 71.6 per cent
   - Syddanmark, 25-44: 557 patients, 72.0 per cent
   - Syddanmark, 45-54: 294 patients, 73.5 per cent
   - Syddanmark, 55 and over: 989 patients, 79.8 per cent
   - not stated, 18-24: 29 patients, 72.4 per cent
   - not stated, 25-44: 82 patients, 76.8 per cent
   - not stated, 45-54: 37 patients, 73.0 per cent
   - not stated, 55 and over: 122 patients, 77.9 per cent

### order_shares_by_pair.png

1. One horizontal bar for each of the 23 screened pairs for the share of its patients who received the marker treatment after the product, with the 7 referred pairs in the darker fill and the other 16 in the lighter one.
2. The bars run longest share first, from Varenadol + antiemetic at 81.7 per cent to Ternivast + hypnotic at 19.6 per cent.
3. Title states that 7 of the 20 candidate pairs clear the referral line.
