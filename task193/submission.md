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
   - Hovedstaden, 18-34: 678 patients, 69.6 per cent
   - Hovedstaden, 35-54: 800 patients, 73.9 per cent
   - Hovedstaden, 55-69: 558 patients, 80.8 per cent
   - Hovedstaden, 70 and over: 902 patients, 80.7 per cent
   - Midtjylland, 18-34: 513 patients, 67.1 per cent
   - Midtjylland, 35-54: 606 patients, 76.6 per cent
   - Midtjylland, 55-69: 469 patients, 77.4 per cent
   - Midtjylland, 70 and over: 682 patients, 77.7 per cent
   - Nordjylland, 18-34: 232 patients, 66.8 per cent
   - Nordjylland, 35-54: 290 patients, 72.4 per cent
   - Nordjylland, 55-69: 185 patients, 78.4 per cent
   - Nordjylland, 70 and over: 279 patients, 80.6 per cent
   - Sjaelland, 18-34: 297 patients, 72.7 per cent
   - Sjaelland, 35-54: 401 patients, 74.6 per cent
   - Sjaelland, 55-69: 303 patients, 79.5 per cent
   - Sjaelland, 70 and over: 449 patients, 80.4 per cent
   - Syddanmark, 18-34: 480 patients, 69.6 per cent
   - Syddanmark, 35-54: 557 patients, 73.2 per cent
   - Syddanmark, 55-69: 408 patients, 77.7 per cent
   - Syddanmark, 70 and over: 569 patients, 80.5 per cent
   - not stated, 18-34: 61 patients, 70.5 per cent
   - not stated, 35-54: 66 patients, 77.3 per cent
   - not stated, 55-69: 48 patients, 77.1 per cent
   - not stated, 70 and over: 62 patients, 79.0 per cent

### order_shares_by_pair.png

1. One horizontal bar per screened pair for the share of its patients who received the marker treatment after the product, longest first, with each pair's referral threshold marked at 1.25 times its expected share and the referred pairs in the darker fill.
2. Title states that 7 of the 20 candidate pairs clear the referral line.
