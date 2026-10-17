# task193 submission

## Tags

**Domain:** Pharmacology, pharmacoepidemiology and safety (safety signal detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Refer 7 of the 20 candidate pairs to formal signal assessment in the quarter beginning 1 January 2027: Dalvextin and loop diuretic; Pirenoxol and acid-suppressant; Ternivast and gout treatment; Oxelumab and antidepressant; Hestroban and antiemetic; Kirunelle and hypnotic; Sovraxil and topical corticosteroid.**
The expected after-count comes from the window's own first-receipt dates, so the lowest referred multiple is 1.34 and the nearest pair on the wrong side of the line is Dalvextin and acid-suppressant at 1.12. Not the 10 pairs an equal-chance expectation refers, which adds Varenadol and antiemetic; Varenadol and acid-suppressant; Varenadol and hypnotic; Admirabin and loop diuretic; Admirabin and antidepressant. Not those 10 pairs less Ternivast and gout treatment; Oxelumab and antidepressant, which are the real signals an equal-chance expectation hides.

## 2. Critical Components

1. The screen's candidate pairs are **20** of the 23 pairs in Annexes A and B
2. The pairs referred are **7**
3. The pairs an equal-chance expectation refers are **10**
4. The pairs it refers that this run does not are **5**, and the pairs it hides are **2**

## 3. Step-by-Step Solution

1. Stacked dispensings_2023_2025.csv and dispensings_2025_2026.csv on the layouts register_release_notes.json gives and counted a re-sent line once, as those notes require: 12993 person keys appear across the extract.
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
   - Dalvextin and acid-suppressant: 152 patients, 81 after, 71 before, referred no
   - Dalvextin and gout treatment: 135 patients, 74 after, 61 before, referred no
   - Dalvextin and loop diuretic: 257 patients, 199 after, 58 before, referred yes
   - Pirenoxol and acid-suppressant: 295 patients, 218 after, 77 before, referred yes
   - Pirenoxol and antidepressant: 173 patients, 96 after, 77 before, referred no
   - Pirenoxol and hypnotic: 134 patients, 73 after, 61 before, referred no
   - Ternivast and antiemetic: 265 patients, 63 after, 202 before, referred no
   - Ternivast and gout treatment: 399 patients, 204 after, 195 before, referred yes
   - Ternivast and hypnotic: 284 patients, 58 after, 226 before, referred no
   - Oxelumab and loop diuretic: 313 patients, 96 after, 217 before, referred no
   - Oxelumab and antidepressant: 551 patients, 311 after, 240 before, referred yes
   - Oxelumab and topical corticosteroid: 369 patients, 132 after, 237 before, referred no
   - Varenadol and antiemetic: 240 patients, 187 after, 53 before, referred no
   - Varenadol and acid-suppressant: 264 patients, 212 after, 52 before, referred no
   - Varenadol and hypnotic: 236 patients, 204 after, 32 before, referred no
   - Hestroban and antiemetic: 354 patients, 248 after, 106 before, referred yes
   - Hestroban and antipsychotic: 8 patients, 1 after, 7 before, below the 25-patient minimum
   - Kirunelle and hypnotic: 249 patients, 180 after, 69 before, referred yes
   - Kirunelle and antipsychotic: 7 patients, 5 after, 2 before, below the 25-patient minimum
   - Admirabin and loop diuretic: 202 patients, 155 after, 47 before, referred no
   - Admirabin and antidepressant: 215 patients, 164 after, 51 before, referred no
   - Sovraxil and topical corticosteroid: 469 patients, 361 after, 108 before, referred yes
   - Sovraxil and antipsychotic: 9 patients, 5 after, 4 before, below the 25-patient minimum
2. Pairs referred: 7.
3. Nearest pair on the wrong side of the referral line: Dalvextin and acid-suppressant.
4. Lines accepted, lines rejected and median days from dispensing to submission, by chain and quarter of dispensing, whole counts and days to one decimal:
   - APK, 2025 Q4: 4500 accepted, 172 rejected, 2.0 days
   - APK, 2026 Q1: 4156 accepted, 152 rejected, 3.0 days
   - APK, 2026 Q2: 4068 accepted, 147 rejected, 3.0 days
   - APK, 2026 Q3: 4374 accepted, 152 rejected, 3.0 days
   - DSA, 2025 Q4: 3448 accepted, 132 rejected, 4.0 days
   - DSA, 2026 Q1: 3067 accepted, 134 rejected, 4.0 days
   - DSA, 2026 Q2: 2909 accepted, 113 rejected, 5.0 days
   - DSA, 2026 Q3: 3216 accepted, 98 rejected, 5.0 days
   - NOR, 2025 Q4: 2432 accepted, 74 rejected, 5.0 days
   - NOR, 2026 Q1: 2306 accepted, 79 rejected, 6.0 days
   - NOR, 2026 Q2: 2250 accepted, 63 rejected, 7.0 days
   - NOR, 2026 Q3: 2351 accepted, 58 rejected, 6.0 days
   - VST, 2025 Q4: 1706 accepted, 61 rejected, 7.0 days
   - VST, 2026 Q1: 1555 accepted, 59 rejected, 8.0 days
   - VST, 2026 Q2: 1496 accepted, 50 rejected, 7.0 days
   - VST, 2026 Q3: 1701 accepted, 45 rejected, 9.0 days
5. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, doses to one decimal and fees to the nearest krone:
   - Nordlys Pharma A/S (H1): 101540.2 DDD, 156088 kroner
   - Bregnholt Laegemidler A/S (H2): 92050.3 DDD, 144276 kroner
   - Vindeby Therapeutics ApS (H3): 333552.0 DDD, 443762 kroner
   - Soegaard Medica A/S (H4): 149580.0 DDD, 223139 kroner
   - Kastholm Pharma A/S (H5): 418008.0 DDD, 526452 kroner
   - Ellevang Biosciences A/S (H6): 457387.2 DDD, 594129 kroner
   - Strandby Farma ApS (H7): 51710.4 DDD, 76531 kroner
6. Patients with a first receipt of a screened product in the window and the share of them with a first marker-treatment receipt in it, by region and age band at 1 October 2025, shares to one decimal:
   - Hovedstaden, 18-39: 676 patients, 76.2 per cent
   - Hovedstaden, 40-59: 653 patients, 74.9 per cent
   - Hovedstaden, 60-74: 489 patients, 76.1 per cent
   - Hovedstaden, 75 and over: 506 patients, 75.1 per cent
   - Midtjylland, 18-39: 516 patients, 79.1 per cent
   - Midtjylland, 40-59: 484 patients, 78.9 per cent
   - Midtjylland, 60-74: 331 patients, 73.4 per cent
   - Midtjylland, 75 and over: 388 patients, 79.1 per cent
   - Nordjylland, 18-39: 245 patients, 77.6 per cent
   - Nordjylland, 40-59: 176 patients, 76.7 per cent
   - Nordjylland, 60-74: 164 patients, 81.1 per cent
   - Nordjylland, 75 and over: 168 patients, 75.6 per cent
   - Sjaelland, 18-39: 320 patients, 77.5 per cent
   - Sjaelland, 40-59: 274 patients, 74.5 per cent
   - Sjaelland, 60-74: 242 patients, 73.1 per cent
   - Sjaelland, 75 and over: 221 patients, 76.0 per cent
   - Syddanmark, 18-39: 445 patients, 78.9 per cent
   - Syddanmark, 40-59: 414 patients, 74.6 per cent
   - Syddanmark, 60-74: 332 patients, 75.0 per cent
   - Syddanmark, 75 and over: 363 patients, 77.7 per cent
   - not stated, 18-39: 48 patients, 72.9 per cent
   - not stated, 40-59: 63 patients, 87.3 per cent
   - not stated, 60-74: 35 patients, 68.6 per cent
   - not stated, 75 and over: 41 patients, 73.2 per cent

### order_shares_by_pair.png

1. One horizontal bar per screened pair for the share of its patients who received the marker treatment after the product, longest first, with each pair's referral threshold marked at 1.25 times its expected share and the referred pairs in the darker fill.
2. Title states that 7 of the 20 candidate pairs clear the referral line.
