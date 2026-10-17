# task193 submission

## Tags

**Domain:** Pharmacology, pharmacoepidemiology and safety (safety signal detection).
**Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Refer 7 of the 20 candidate pairs to formal signal assessment in the quarter beginning 1 January 2027: Dalvextin and loop diuretic; Pirenoxol and acid-suppressant; Ternivast and gout treatment; Oxelumab and antidepressant; Hestroban and antiemetic; Kirunelle and hypnotic; Sovraxil and topical corticosteroid.**
The expected after-count comes from the window's own first-receipt dates, so the lowest referred multiple is 1.35 and the nearest pair on the wrong side of the line is Dalvextin and acid-suppressant at 1.02. Not the 10 pairs an equal-chance expectation refers, which adds Varenadol and antiemetic; Varenadol and acid-suppressant; Varenadol and hypnotic; Admirabin and loop diuretic; Admirabin and antidepressant. Not those 10 pairs less Ternivast and gout treatment; Oxelumab and antidepressant, which are the real signals an equal-chance expectation hides.

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
   - Dalvextin and acid-suppressant: 186 patients, 91 after, 95 before, referred no
   - Dalvextin and gout treatment: 192 patients, 106 after, 86 before, referred no
   - Dalvextin and loop diuretic: 364 patients, 263 after, 101 before, referred yes
   - Pirenoxol and acid-suppressant: 365 patients, 267 after, 98 before, referred yes
   - Pirenoxol and antidepressant: 167 patients, 96 after, 71 before, referred no
   - Pirenoxol and hypnotic: 163 patients, 82 after, 81 before, referred no
   - Ternivast and antiemetic: 337 patients, 62 after, 275 before, referred no
   - Ternivast and gout treatment: 547 patients, 270 after, 277 before, referred yes
   - Ternivast and hypnotic: 326 patients, 63 after, 263 before, referred no
   - Oxelumab and loop diuretic: 426 patients, 141 after, 285 before, referred no
   - Oxelumab and antidepressant: 708 patients, 386 after, 322 before, referred yes
   - Oxelumab and topical corticosteroid: 507 patients, 144 after, 363 before, referred no
   - Varenadol and antiemetic: 277 patients, 222 after, 55 before, referred no
   - Varenadol and acid-suppressant: 291 patients, 223 after, 68 before, referred no
   - Varenadol and hypnotic: 260 patients, 197 after, 63 before, referred no
   - Hestroban and antiemetic: 483 patients, 351 after, 132 before, referred yes
   - Hestroban and antipsychotic: 6 patients, 2 after, 4 before, below the 25-patient minimum
   - Kirunelle and hypnotic: 346 patients, 246 after, 100 before, referred yes
   - Kirunelle and antipsychotic: 12 patients, 6 after, 6 before, below the 25-patient minimum
   - Admirabin and loop diuretic: 211 patients, 159 after, 52 before, referred no
   - Admirabin and antidepressant: 262 patients, 209 after, 53 before, referred no
   - Sovraxil and topical corticosteroid: 640 patients, 491 after, 149 before, referred yes
   - Sovraxil and antipsychotic: 17 patients, 12 after, 5 before, below the 25-patient minimum
2. Pairs referred: 7.
3. Nearest pair on the wrong side of the referral line: Dalvextin and acid-suppressant.
4. Lines accepted, lines rejected and median days from dispensing to submission, by chain and quarter of dispensing, whole counts and days to one decimal:
   - APK, 2025 Q4: 6066 accepted, 54 rejected, 2.0 days
   - APK, 2026 Q1: 5536 accepted, 52 rejected, 3.0 days
   - APK, 2026 Q2: 5479 accepted, 42 rejected, 3.0 days
   - APK, 2026 Q3: 5734 accepted, 52 rejected, 3.0 days
   - DSA, 2025 Q4: 4711 accepted, 74 rejected, 5.0 days
   - DSA, 2026 Q1: 4236 accepted, 62 rejected, 4.0 days
   - DSA, 2026 Q2: 4129 accepted, 54 rejected, 4.0 days
   - DSA, 2026 Q3: 4399 accepted, 38 rejected, 5.0 days
   - NOR, 2025 Q4: 3378 accepted, 80 rejected, 4.0 days
   - NOR, 2026 Q1: 3020 accepted, 75 rejected, 5.0 days
   - NOR, 2026 Q2: 2914 accepted, 65 rejected, 6.0 days
   - NOR, 2026 Q3: 3232 accepted, 62 rejected, 4.0 days
   - VST, 2025 Q4: 2318 accepted, 30 rejected, 6.0 days
   - VST, 2026 Q1: 1966 accepted, 39 rejected, 5.0 days
   - VST, 2026 Q2: 1928 accepted, 22 rejected, 7.0 days
   - VST, 2026 Q3: 1950 accepted, 18 rejected, 6.0 days
5. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, doses to one decimal and fees to the nearest krone:
   - Nordlys Pharma A/S (H1): 273319.0 DDD, 353240 kroner
   - Bregnholt Laegemidler A/S (H2): 413680.0 DDD, 544566 kroner
   - Vindeby Therapeutics ApS (H3): 420908.0 DDD, 562301 kroner
   - Soegaard Medica A/S (H4): 367590.0 DDD, 457007 kroner
   - Kastholm Pharma A/S (H5): 599910.0 DDD, 752664 kroner
   - Ellevang Biosciences A/S (H6): 1016196.0 DDD, 1056474 kroner
   - Strandby Farma ApS (H7): 221550.0 DDD, 324571 kroner
6. Patients with a first receipt of a screened product in the window and the share of them with a first marker-treatment receipt in it, by region and age band at 1 October 2025, shares to one decimal:
   - Hovedstaden, 18-34: 670 patients, 70.1 per cent
   - Hovedstaden, 35-54: 800 patients, 74.6 per cent
   - Hovedstaden, 55-69: 551 patients, 81.9 per cent
   - Hovedstaden, 70 and over: 898 patients, 79.8 per cent
   - Midtjylland, 18-34: 512 patients, 69.1 per cent
   - Midtjylland, 35-54: 601 patients, 74.0 per cent
   - Midtjylland, 55-69: 465 patients, 78.7 per cent
   - Midtjylland, 70 and over: 672 patients, 79.0 per cent
   - Nordjylland, 18-34: 244 patients, 66.0 per cent
   - Nordjylland, 35-54: 290 patients, 72.1 per cent
   - Nordjylland, 55-69: 196 patients, 78.6 per cent
   - Nordjylland, 70 and over: 285 patients, 80.7 per cent
   - Sjaelland, 18-34: 299 patients, 71.9 per cent
   - Sjaelland, 35-54: 409 patients, 76.3 per cent
   - Sjaelland, 55-69: 306 patients, 79.1 per cent
   - Sjaelland, 70 and over: 453 patients, 78.6 per cent
   - Syddanmark, 18-34: 477 patients, 70.0 per cent
   - Syddanmark, 35-54: 553 patients, 74.0 per cent
   - Syddanmark, 55-69: 411 patients, 77.6 per cent
   - Syddanmark, 70 and over: 573 patients, 80.1 per cent
   - not stated, 18-34: 61 patients, 65.6 per cent
   - not stated, 35-54: 67 patients, 77.6 per cent
   - not stated, 55-69: 48 patients, 75.0 per cent
   - not stated, 70 and over: 62 patients, 77.4 per cent

### order_shares_by_pair.png

1. One horizontal bar per screened pair for the share of its patients who received the marker treatment after the product, longest first, with each pair's referral threshold marked at 1.25 times its expected share and the referred pairs in the darker fill.
2. Title states that 7 of the 20 candidate pairs clear the referral line.
