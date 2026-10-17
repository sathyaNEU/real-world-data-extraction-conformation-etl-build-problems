# task193 submission

## Tags

**Domain:** Pharmacology & Safety, safety signal detection (triaging which disproportionate reporting signals a capped assessment desk takes forward when one product holds two fifths of the quarter's reports).
**Analytical objective:** Anomaly Detection & Diagnostics (separating a real disproportion in reporting from what the database's own composition produces).

## 1. Final Recommendation

**Take 15 signals forward to the assessment desk, and the desk can take all of them: they fill 15 of its 16 slots for the quarter.**

The quarter's reports are dominated by one product. The autumn booster accounts for **40.2** per cent of the 7,483 cases the agency received between 1 July and 30 September, and it holds between **61.6** and **68.6** per cent of every report naming the four reactions its own reactogenicity produces. Measured against a database that includes it, four pairs that meet the standard's criteria sit below the threshold: their ratios run from **1.39** to **1.55** against the whole database and from **2.70** to **3.09** once the booster's reporting is out of what they are compared with. Those four are Keltaprin on headache, Serovane on fatigue, Noralvex on pyrexia, Ravistan on myalgia. The run that leaves the booster in the comparison takes only **11** forward and leaves five of the desk's slots idle.

## 2. Critical Components

1. **15** pairs meet all three criteria in paragraph 3.2 once the measure is taken against the reporting of the products the quarter is not dominated by, against **11** when it is taken against every report in the database.
2. The four the booster holds down are **Keltaprin** on headache, **Serovane** on fatigue, **Noralvex** on pyrexia, **Ravistan** on myalgia, at **204**, **166**, **113** and **80** reports.
3. The booster is **40.2** per cent of the quarter's reports, and on the four reactions in question it holds **61.6**, **64.7**, **68.1** and **68.6** per cent of every report naming them.
4. Reading the reporter's own words as the reaction, instead of the preferred term the dictionary gives, takes **19** pairs forward, more than the desk's **16** slots; the reporting odds ratio against the whole database takes **13**, which finds two of the four and not the other two.
5. The nearest pair to the threshold on the basis the answer rests on is **0.36** above it, and the lowest ratio taken forward is **2.36**, so no pair turns on the rounding.

## 3. Step-by-Step Solution

1. Kept the submissions in `report_master.csv` whose receipt date falls between 1 July and 30 September 2026, which is the run's window under paragraph 2.1 of `signal_standard.pdf`. The report date and the coding date do not bear on it.
2. Collapsed the submissions of one case onto one report on the case number, as paragraph 2.2 requires: 7,483 cases reached the agency through 10,082 submissions, many of them reported by the clinician and by the licence holder both.
3. Took each reaction as the preferred term `reaction_dictionary.csv` gives for the reporter's verbatim term at the dictionary version the case was coded at, per paragraph 2.3, and carried the product renamed on its licence transfer onto one code through `product_register.csv`, per paragraph 2.4.
4. Built the two by two table for every product and reaction pair named on 15 or more of those reports and computed the proportional reporting ratio and the chi-square of the same table.
5. Left out the pairs `product_information_listed.csv` already describes, which paragraph 3.3 keeps out of the run, and the pairs `closed_assessments_register.csv` closed inside the previous twelve months, which paragraph 3.4 keeps out: the register names no pair that meets the criteria on either basis.
6. Looked at what the comparison was carrying. One product holds **40.2** per cent of the quarter's reports, and on six reactions it holds between **61.6** and **86.8** per cent of every report naming them, so for those reactions the rate the rest of the database is said to report at is mostly that one product's own reactogenicity.
7. Recomputed every pair with that product's reports out of what the pair is compared with. **15** pairs meet the criteria, the **11** the whole-database comparison already took plus four it held below 2.00. The list is stable: leaving out the two largest products, the three largest, or every product holding more than a tenth or a twentieth of the quarter gives the same 15, and leaving out any single other product moves no pair across.
8. Checked the two readings a careful run would also take: pooling the ratio over the report's channel, reporter type, age band, region or sex lands on the same **11**, and the reporting odds ratio against the whole database lands on **13**. Neither reaches the four, because neither changes what the comparison is carrying.

## 4. Deliverable Answers

### signal_list_2026Q3.xlsx

| Product | Reaction | Reports | Ratio | Chi-square | Against the whole database |
|---|---|---|---|---|---|
| Keltaprin | Headache | 204 | 2.70 | 220.4 | 1.55, below 2.00 |
| Serovane | Fatigue | 166 | 2.97 | 211.5 | 1.55, below 2.00 |
| Noralvex | Pyrexia | 113 | 3.09 | 154.0 | 1.48, below 2.00 |
| Ravistan | Myalgia | 80 | 2.88 | 95.9 | 1.39, below 2.00 |
| Culavret | Nausea | 80 | 2.36 | 65.7 |  |
| Ardelpha | Dizziness | 55 | 2.37 | 44.8 |  |
| Mestoran | Diarrhoea | 47 | 2.53 | 42.7 |  |
| Doranzil | Hepatic enzyme increased | 46 | 4.05 | 75.1 |  |
| Vintorel | Rash | 45 | 2.57 | 44.2 |  |
| Thelbarin | Urticaria | 29 | 2.77 | 29.4 |  |
| Pelgorane Nordic | Alopecia | 22 | 7.01 | 89.3 |  |
| Imbracor | Thrombocytopenia | 21 | 5.28 | 52.7 |  |
| Quorendal | Arthralgia | 20 | 2.54 | 18.3 |  |
| Hestramyl | Syncope | 17 | 4.46 | 40.4 |  |
| Brazivane | Palpitations | 17 | 3.94 | 34.6 |  |

Pairs taken forward **15**, the desk's capacity **16**, slots left **1**. The whole-database comparison alone takes **11**.

### signal_overview.png

One horizontal bar for each of the 15 pairs taken forward, ordered by its ratio, with the paragraph 3.2 threshold drawn at 2.00. The four the booster held down are shown in a second colour, each with a marker at the ratio it reaches against the whole database (1.55, 1.55, 1.48 and 1.39), so the gap the comparison set makes reads at a glance.

### Submissions by channel and month

| Channel | Month | Submissions received | Could not be coded | Mean days to coding |
|---|---|---|---|---|
| clinician | 2026-07 | 1204 | 23 | 5.3 |
| clinician | 2026-08 | 1237 | 16 | 5.2 |
| clinician | 2026-09 | 1138 | 15 | 4.9 |
| licence holder | 2026-07 | 1420 | 17 | 3.9 |
| licence holder | 2026-08 | 1542 | 17 | 4.0 |
| licence holder | 2026-09 | 1418 | 15 | 4.0 |
| patient | 2026-07 | 466 | 9 | 5.6 |
| patient | 2026-08 | 500 | 16 | 5.3 |
| patient | 2026-09 | 522 | 14 | 5.1 |
| pharmacy | 2026-07 | 231 | 4 | 5.3 |
| pharmacy | 2026-08 | 274 | 7 | 5.0 |
| pharmacy | 2026-09 | 228 | 6 | 4.9 |

### Licence holders

| Licence holder | Submissions filed | Filed after the quarter closed | Fee due (DKK) |
|---|---|---|---|
| Aurelind Pharma A/S | 373 | 3 | 55204 |
| Brynholm Laegemidler ApS | 338 | 5 | 44616 |
| Castellan Nordic A/S | 298 | 1 | 52989 |
| Dalberg Therapeutics A/S | 295 | 2 | 35695 |
| Elvershoj Biotek A/S | 161 | 4 | 24794 |
| Fjeldgaard Pharma A/S | 197 | 3 | 27383 |
| Granvig Medical A/S | 187 | 3 | 22066 |
| Hvidsten Laboratorier A/S | 95 | 0 | 12065 |
| Kvistgaard Onkologi A/S | 87 | 3 | 13398 |
| Nordsund Vaccines A/S | 2414 | 41 | 231744 |

### Cases by region and age group

| Region | Age group | Cases | Share naming a serious reaction |
|---|---|---|---|
| Hovedstaden | 0 to 17 | 206 | 11.7 per cent |
| Hovedstaden | 18 to 39 | 693 | 18.3 per cent |
| Hovedstaden | 40 to 64 | 775 | 17.3 per cent |
| Hovedstaden | 65 and over | 605 | 13.7 per cent |
| Hovedstaden | not stated | 70 | 10.0 per cent |
| Midtjylland | 0 to 17 | 152 | 18.4 per cent |
| Midtjylland | 18 to 39 | 484 | 16.7 per cent |
| Midtjylland | 40 to 64 | 596 | 14.8 per cent |
| Midtjylland | 65 and over | 426 | 16.2 per cent |
| Midtjylland | not stated | 44 | 18.2 per cent |
| Nordjylland | 0 to 17 | 93 | 11.8 per cent |
| Nordjylland | 18 to 39 | 237 | 16.0 per cent |
| Nordjylland | 40 to 64 | 274 | 15.7 per cent |
| Nordjylland | 65 and over | 217 | 15.2 per cent |
| Nordjylland | not stated | 27 | 14.8 per cent |
| Sjaelland | 0 to 17 | 110 | 15.5 per cent |
| Sjaelland | 18 to 39 | 302 | 15.9 per cent |
| Sjaelland | 40 to 64 | 379 | 14.2 per cent |
| Sjaelland | 65 and over | 281 | 17.8 per cent |
| Sjaelland | not stated | 32 | 15.6 per cent |
| Syddanmark | 0 to 17 | 119 | 10.1 per cent |
| Syddanmark | 18 to 39 | 438 | 18.5 per cent |
| Syddanmark | 40 to 64 | 516 | 15.9 per cent |
| Syddanmark | 65 and over | 361 | 14.4 per cent |
| Syddanmark | not stated | 46 | 13.0 per cent |
