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
   - APK, 2025 Q4: 5985 accepted, 66 rejected, 1.0 days
   - APK, 2026 Q1: 5476 accepted, 67 rejected, 2.0 days
   - APK, 2026 Q2: 5554 accepted, 42 rejected, 2.0 days
   - APK, 2026 Q3: 5732 accepted, 58 rejected, 2.0 days
   - DSA, 2025 Q4: 4673 accepted, 66 rejected, 3.0 days
   - DSA, 2026 Q1: 4119 accepted, 71 rejected, 3.0 days
   - DSA, 2026 Q2: 4082 accepted, 39 rejected, 4.0 days
   - DSA, 2026 Q3: 4344 accepted, 62 rejected, 4.0 days
   - NOR, 2025 Q4: 3386 accepted, 73 rejected, 4.0 days
   - NOR, 2026 Q1: 3064 accepted, 64 rejected, 5.0 days
   - NOR, 2026 Q2: 2875 accepted, 82 rejected, 6.0 days
   - NOR, 2026 Q3: 3203 accepted, 35 rejected, 6.0 days
   - VST, 2025 Q4: 2260 accepted, 28 rejected, 6.0 days
   - VST, 2026 Q1: 2002 accepted, 18 rejected, 7.0 days
   - VST, 2026 Q2: 1933 accepted, 22 rejected, 6.0 days
   - VST, 2026 Q3: 1997 accepted, 18 rejected, 8.0 days
5. Defined daily doses dispensed in the screen window and the data fee due, by fee payer, doses to one decimal and fees to the nearest krone:
   - Nordlys Pharma A/S (H1): 255520.5 DDD, 329175 kroner
   - Bregnholt Laegemidler A/S (H2): 231565.7 DDD, 361748 kroner
   - Vindeby Therapeutics ApS (H3): 407656.0 DDD, 542791 kroner
   - Soegaard Medica A/S (H4): 159766.9 DDD, 237117 kroner
   - Kastholm Pharma A/S (H5): 80973.6 DDD, 121540 kroner
   - Ellevang Biosciences A/S (H6): 316685.2 DDD, 401744 kroner
   - Strandby Farma ApS (H7): 113515.5 DDD, 168003 kroner
6. Patients with a first receipt of a screened product in the window and the share of them with a first marker-treatment receipt in it, by region and age band at 1 October 2025, shares to one decimal:
   - Hovedstaden, 18-39: 868 patients, 68.5 per cent
   - Hovedstaden, 40-59: 788 patients, 77.5 per cent
   - Hovedstaden, 60-74: 552 patients, 81.9 per cent
   - Hovedstaden, 75 and over: 709 patients, 79.5 per cent
   - Midtjylland, 18-39: 667 patients, 68.1 per cent
   - Midtjylland, 40-59: 626 patients, 76.7 per cent
   - Midtjylland, 60-74: 457 patients, 79.6 per cent
   - Midtjylland, 75 and over: 529 patients, 77.3 per cent
   - Nordjylland, 18-39: 303 patients, 67.0 per cent
   - Nordjylland, 40-59: 285 patients, 75.1 per cent
   - Nordjylland, 60-74: 204 patients, 80.9 per cent
   - Nordjylland, 75 and over: 222 patients, 80.6 per cent
   - Sjaelland, 18-39: 391 patients, 73.4 per cent
   - Sjaelland, 40-59: 422 patients, 73.9 per cent
   - Sjaelland, 60-74: 303 patients, 80.2 per cent
   - Sjaelland, 75 and over: 338 patients, 81.1 per cent
   - Syddanmark, 18-39: 621 patients, 69.9 per cent
   - Syddanmark, 40-59: 550 patients, 75.6 per cent
   - Syddanmark, 60-74: 403 patients, 79.2 per cent
   - Syddanmark, 75 and over: 420 patients, 80.2 per cent
   - not stated, 18-39: 74 patients, 74.3 per cent
   - not stated, 40-59: 64 patients, 75.0 per cent
   - not stated, 60-74: 53 patients, 75.5 per cent
   - not stated, 75 and over: 46 patients, 80.4 per cent

### order_shares_by_pair.png

1. One horizontal bar per screened pair for the share of its patients who received the marker treatment after the product, longest first, with each pair's referral threshold marked at 1.25 times its expected share and the referred pairs in the darker fill.
2. Title states that 7 of the 20 candidate pairs clear the referral line.
