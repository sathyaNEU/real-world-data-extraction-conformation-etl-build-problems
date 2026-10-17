# task193 submission

## Tags

**Domain:** Pharmacology, pharmacoepidemiology and safety (safety signal detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Refer 7 of the 20 candidate pairs to formal signal assessment in the quarter beginning 1 January 2027: Dalvextin and loop diuretic; Pirenoxol and acid-suppressant; Ternivast and gout treatment; Oxelumab and antidepressant; Hestroban and antiemetic; Kirunelle and hypnotic; Sovraxil and topical corticosteroid.**
The expected after-count comes from the window's own first-receipt dates, so the lowest referred multiple is 1.40 and the nearest pair on the wrong side of the line is Dalvextin and acid-suppressant at 1.07. Not the 10 pairs an equal-chance expectation refers, which adds Varenadol and antiemetic; Varenadol and acid-suppressant; Varenadol and hypnotic; Admirabin and loop diuretic; Admirabin and antidepressant. Not those 10 pairs less Ternivast and gout treatment; Oxelumab and antidepressant, which are the real signals an equal-chance expectation hides.

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
   - Dalvextin and acid-suppressant: 182 patients, 93 after, 89 before, referred no
   - Dalvextin and gout treatment: 188 patients, 103 after, 85 before, referred no
   - Dalvextin and loop diuretic: 333 patients, 242 after, 91 before, referred yes
   - Pirenoxol and acid-suppressant: 338 patients, 246 after, 92 before, referred yes
   - Pirenoxol and antidepressant: 176 patients, 97 after, 79 before, referred no
   - Pirenoxol and hypnotic: 165 patients, 89 after, 76 before, referred no
   - Ternivast and antiemetic: 336 patients, 68 after, 268 before, referred no
   - Ternivast and gout treatment: 540 patients, 275 after, 265 before, referred yes
   - Ternivast and hypnotic: 339 patients, 72 after, 267 before, referred no
   - Oxelumab and loop diuretic: 435 patients, 142 after, 293 before, referred no
   - Oxelumab and antidepressant: 700 patients, 406 after, 294 before, referred yes
   - Oxelumab and topical corticosteroid: 494 patients, 138 after, 356 before, referred no
   - Varenadol and antiemetic: 266 patients, 217 after, 49 before, referred no
   - Varenadol and acid-suppressant: 291 patients, 224 after, 67 before, referred no
   - Varenadol and hypnotic: 268 patients, 210 after, 58 before, referred no
   - Hestroban and antiemetic: 434 patients, 316 after, 118 before, referred yes
   - Hestroban and antipsychotic: 5 patients, 2 after, 3 before, below the 25-patient minimum
   - Kirunelle and hypnotic: 276 patients, 209 after, 67 before, referred yes
   - Kirunelle and antipsychotic: 12 patients, 6 after, 6 before, below the 25-patient minimum
   - Admirabin and loop diuretic: 216 patients, 166 after, 50 before, referred no
   - Admirabin and antidepressant: 255 patients, 201 after, 54 before, referred no
   - Sovraxil and topical corticosteroid: 556 patients, 430 after, 126 before, referred yes
   - Sovraxil and antipsychotic: 19 patients, 13 after, 6 before, below the 25-patient minimum
2. Pairs referred: 7.
3. Nearest pair on the wrong side of the referral line: Dalvextin and acid-suppressant.
4. Lines accepted, lines rejected and median days from dispensing to submission, by chain and quarter of dispensing, whole counts and days to one decimal:
   - APK, 2025 Q4: 5869 accepted, 175 rejected, 1.0 days
   - APK, 2026 Q1: 5325 accepted, 184 rejected, 2.0 days
   - APK, 2026 Q2: 5364 accepted, 167 rejected, 2.0 days
   - APK, 2026 Q3: 5674 accepted, 142 rejected, 2.0 days
   - DSA, 2025 Q4: 4564 accepted, 144 rejected, 3.0 days
   - DSA, 2026 Q1: 4087 accepted, 143 rejected, 3.0 days
   - DSA, 2026 Q2: 3966 accepted, 130 rejected, 4.0 days
   - DSA, 2026 Q3: 4361 accepted, 115 rejected, 4.0 days
   - NOR, 2025 Q4: 3293 accepted, 107 rejected, 4.0 days
   - NOR, 2026 Q1: 3031 accepted, 82 rejected, 5.0 days
   - NOR, 2026 Q2: 2905 accepted, 84 rejected, 6.0 days
   - NOR, 2026 Q3: 3257 accepted, 93 rejected, 5.0 days
   - VST, 2025 Q4: 2293 accepted, 70 rejected, 6.0 days
   - VST, 2026 Q1: 1967 accepted, 58 rejected, 7.0 days
   - VST, 2026 Q2: 1884 accepted, 38 rejected, 6.0 days
   - VST, 2026 Q3: 1959 accepted, 69 rejected, 8.0 days
5. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, doses to one decimal and fees to the nearest krone:
   - Nordlys Pharma A/S (H1): 249236.0 DDD, 384430 kroner
   - Bregnholt Laegemidler A/S (H2): 235701.2 DDD, 368225 kroner
   - Vindeby Therapeutics ApS (H3): 408294.0 DDD, 543525 kroner
   - Soegaard Medica A/S (H4): 156154.3 DDD, 231845 kroner
   - Kastholm Pharma A/S (H5): 134301.3 DDD, 200421 kroner
   - Ellevang Biosciences A/S (H6): 370231.0 DDD, 473009 kroner
   - Strandby Farma ApS (H7): 115878.0 DDD, 171499 kroner
6. Patients with a first receipt of a screened product in the window and the share of them with a first marker-treatment receipt in it, by region and age band at 1 October 2025, shares to one decimal:
   - Hovedstaden, 18-39: 879 patients, 66.9 per cent
   - Hovedstaden, 40-59: 868 patients, 75.0 per cent
   - Hovedstaden, 60-74: 603 patients, 76.9 per cent
   - Hovedstaden, 75 and over: 707 patients, 77.9 per cent
   - Midtjylland, 18-39: 671 patients, 68.1 per cent
   - Midtjylland, 40-59: 614 patients, 73.9 per cent
   - Midtjylland, 60-74: 445 patients, 78.7 per cent
   - Midtjylland, 75 and over: 513 patients, 82.7 per cent
   - Nordjylland, 18-39: 306 patients, 70.9 per cent
   - Nordjylland, 40-59: 308 patients, 75.6 per cent
   - Nordjylland, 60-74: 214 patients, 82.2 per cent
   - Nordjylland, 75 and over: 234 patients, 72.6 per cent
   - Sjaelland, 18-39: 448 patients, 70.3 per cent
   - Sjaelland, 40-59: 377 patients, 77.7 per cent
   - Sjaelland, 60-74: 278 patients, 80.2 per cent
   - Sjaelland, 75 and over: 304 patients, 76.3 per cent
   - Syddanmark, 18-39: 563 patients, 68.7 per cent
   - Syddanmark, 40-59: 517 patients, 77.2 per cent
   - Syddanmark, 60-74: 397 patients, 82.6 per cent
   - Syddanmark, 75 and over: 448 patients, 81.2 per cent
   - not stated, 18-39: 64 patients, 70.3 per cent
   - not stated, 40-59: 58 patients, 72.4 per cent
   - not stated, 60-74: 40 patients, 92.5 per cent
   - not stated, 75 and over: 60 patients, 78.3 per cent

### order_shares_by_pair.png

1. One horizontal bar per screened pair for the share of its patients who received the marker treatment after the product, longest first, with each pair's referral threshold marked at 1.25 times its expected share and the referred pairs in the darker fill.
2. Title states that 7 of the 20 candidate pairs clear the referral line.
