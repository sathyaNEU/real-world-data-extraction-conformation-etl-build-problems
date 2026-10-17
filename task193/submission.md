# task193 submission

## Tags

**Domain:** Pharmacology, pharmacoepidemiology and safety (safety signal detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Refer 7 of the 20 candidate pairs to formal signal assessment in the quarter beginning 1 January 2027: Dalvextin and loop diuretic; Pirenoxol and acid-suppressant; Ternivast and gout treatment; Oxelumab and antidepressant; Hestroban and antiemetic; Kirunelle and hypnotic; Sovraxil and topical corticosteroid.**
The expected after-count comes from the window's own first-receipt dates, so the lowest referred multiple is 1.33 and the nearest pair on the wrong side of the line is Dalvextin and acid-suppressant at 1.02. Not the 10 pairs an equal-chance expectation refers, which adds Varenadol and antiemetic; Varenadol and acid-suppressant; Varenadol and hypnotic; Admirabin and loop diuretic; Admirabin and antidepressant. Not those 10 pairs less Ternivast and gout treatment; Oxelumab and antidepressant, which are the real signals an equal-chance expectation hides.

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
   - Dalvextin and acid-suppressant: 189 patients, 96 after, 93 before, referred no
   - Dalvextin and gout treatment: 204 patients, 110 after, 94 before, referred no
   - Dalvextin and loop diuretic: 338 patients, 240 after, 98 before, referred yes
   - Pirenoxol and acid-suppressant: 336 patients, 246 after, 90 before, referred yes
   - Pirenoxol and antidepressant: 168 patients, 94 after, 74 before, referred no
   - Pirenoxol and hypnotic: 174 patients, 92 after, 82 before, referred no
   - Ternivast and antiemetic: 349 patients, 71 after, 278 before, referred no
   - Ternivast and gout treatment: 547 patients, 273 after, 274 before, referred yes
   - Ternivast and hypnotic: 331 patients, 71 after, 260 before, referred no
   - Oxelumab and loop diuretic: 423 patients, 147 after, 276 before, referred no
   - Oxelumab and antidepressant: 692 patients, 381 after, 311 before, referred yes
   - Oxelumab and topical corticosteroid: 487 patients, 145 after, 342 before, referred no
   - Varenadol and antiemetic: 279 patients, 229 after, 50 before, referred no
   - Varenadol and acid-suppressant: 298 patients, 226 after, 72 before, referred no
   - Varenadol and hypnotic: 269 patients, 210 after, 59 before, referred no
   - Hestroban and antiemetic: 436 patients, 317 after, 119 before, referred yes
   - Hestroban and antipsychotic: 7 patients, 2 after, 5 before, below the 25-patient minimum
   - Kirunelle and hypnotic: 294 patients, 217 after, 77 before, referred yes
   - Kirunelle and antipsychotic: 13 patients, 7 after, 6 before, below the 25-patient minimum
   - Admirabin and loop diuretic: 213 patients, 162 after, 51 before, referred no
   - Admirabin and antidepressant: 267 patients, 214 after, 53 before, referred no
   - Sovraxil and topical corticosteroid: 536 patients, 401 after, 135 before, referred yes
   - Sovraxil and antipsychotic: 17 patients, 12 after, 5 before, below the 25-patient minimum
2. Pairs referred: 7.
3. Nearest pair on the wrong side of the referral line: Dalvextin and acid-suppressant.
4. Lines accepted, lines rejected and median days from dispensing to submission, by chain and quarter of dispensing, whole counts and days to one decimal:
   - APK, 2025 Q4: 5882 accepted, 52 rejected, 1.0 days
   - APK, 2026 Q1: 5453 accepted, 54 rejected, 2.0 days
   - APK, 2026 Q2: 5499 accepted, 43 rejected, 2.0 days
   - APK, 2026 Q3: 5661 accepted, 48 rejected, 2.0 days
   - DSA, 2025 Q4: 4620 accepted, 73 rejected, 3.0 days
   - DSA, 2026 Q1: 4167 accepted, 60 rejected, 3.0 days
   - DSA, 2026 Q2: 4137 accepted, 47 rejected, 4.0 days
   - DSA, 2026 Q3: 4379 accepted, 50 rejected, 4.0 days
   - NOR, 2025 Q4: 3343 accepted, 75 rejected, 4.0 days
   - NOR, 2026 Q1: 3059 accepted, 72 rejected, 5.0 days
   - NOR, 2026 Q2: 2895 accepted, 80 rejected, 6.0 days
   - NOR, 2026 Q3: 3204 accepted, 39 rejected, 6.0 days
   - VST, 2025 Q4: 2244 accepted, 38 rejected, 6.0 days
   - VST, 2026 Q1: 1984 accepted, 22 rejected, 7.0 days
   - VST, 2026 Q2: 1940 accepted, 18 rejected, 6.0 days
   - VST, 2026 Q3: 2003 accepted, 25 rejected, 8.0 days
5. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, doses to one decimal and fees to the nearest krone:
   - Nordlys Pharma A/S (H1): 256094.5 DDD, 329786 kroner
   - Bregnholt Laegemidler A/S (H2): 233630.2 DDD, 364993 kroner
   - Vindeby Therapeutics ApS (H3): 407568.0 DDD, 542674 kroner
   - Soegaard Medica A/S (H4): 159687.8 DDD, 236990 kroner
   - Kastholm Pharma A/S (H5): 80303.2 DDD, 120540 kroner
   - Ellevang Biosciences A/S (H6): 315988.0 DDD, 400858 kroner
   - Strandby Farma ApS (H7): 114198.0 DDD, 169013 kroner
6. Patients with a first receipt of a screened product in the window and the share of them with a first marker-treatment receipt in it, by region and age band at 1 October 2025, shares to one decimal:
   - Hovedstaden, 18-39: 868 patients, 68.0 per cent
   - Hovedstaden, 40-59: 787 patients, 77.8 per cent
   - Hovedstaden, 60-74: 551 patients, 80.8 per cent
   - Hovedstaden, 75 and over: 709 patients, 79.7 per cent
   - Midtjylland, 18-39: 667 patients, 67.2 per cent
   - Midtjylland, 40-59: 626 patients, 75.9 per cent
   - Midtjylland, 60-74: 458 patients, 79.7 per cent
   - Midtjylland, 75 and over: 529 patients, 76.7 per cent
   - Nordjylland, 18-39: 303 patients, 66.7 per cent
   - Nordjylland, 40-59: 285 patients, 75.8 per cent
   - Nordjylland, 60-74: 204 patients, 80.9 per cent
   - Nordjylland, 75 and over: 222 patients, 80.6 per cent
   - Sjaelland, 18-39: 391 patients, 72.6 per cent
   - Sjaelland, 40-59: 422 patients, 72.3 per cent
   - Sjaelland, 60-74: 303 patients, 78.9 per cent
   - Sjaelland, 75 and over: 338 patients, 80.8 per cent
   - Syddanmark, 18-39: 621 patients, 68.4 per cent
   - Syddanmark, 40-59: 550 patients, 74.9 per cent
   - Syddanmark, 60-74: 403 patients, 79.2 per cent
   - Syddanmark, 75 and over: 420 patients, 79.5 per cent
   - not stated, 18-39: 74 patients, 73.0 per cent
   - not stated, 40-59: 64 patients, 75.0 per cent
   - not stated, 60-74: 53 patients, 77.4 per cent
   - not stated, 75 and over: 46 patients, 80.4 per cent

### order_shares_by_pair.png

1. One horizontal bar per screened pair for the share of its patients who received the marker treatment after the product, longest first, with each pair's referral threshold marked at 1.25 times its expected share and the referred pairs in the darker fill.
2. Title states that 7 of the 20 candidate pairs clear the referral line.
