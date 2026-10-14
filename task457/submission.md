# task457 submission

## Tags

**Domain:** Survey Research & Official Statistics, census, register and administrative data quality (the clinical faculty's annual disclosures, a timely self-report, validated against the Open Payments register on the years both cover: each disclosure compared with the payments the register shows made by the day it was submitted, each faculty member's amount-reporting error weighted by how many matched manufacturer-years they have, and carried to 2026, which the register has not yet published).
**Analytical objective:** Data Extraction & Conformation (ETL) (Open Payments payment records tied to the faculty through covered-recipient profiles, the disclosure system's versions, submission times, typed company names and two form editions, and the roster's appointments across the 2025 reorganisation and changed employee numbers conformed to one row per faculty member, manufacturer and year).

## 1. Final Recommendation

**The docket for the committee's meeting of 11 February 2027 is Adam Andersen, Kyle Avery, Fernando Baldwin, Stacie Black, Alexis Drake, Henry Grimes, Pedro Hampton, Johnathan Kaiser, Kerry Leach, Jillian Luna, Kirsten Middleton, Vickie Nolan, Ruth Rosario, Judith Valenzuela and Traci Ware.**

Stacie Black, Pedro Hampton, Kerry Leach, Jillian Luna and Judith Valenzuela submitted their 2026 disclosures in December 2026, before the year's last payments, and are estimated with the share of the year each manufacturer had paid by that date; Fernando Baldwin, Johnathan Kaiser, Vickie Nolan, Ruth Rosario and Traci Ware disclose about half of what the register publishes for them. Not Melvin Blackwell, Angelica Gentry, Cory Harper, Hector Mahoney and Carly Singleton, whom the corrections that read every disclosure as covering its whole year put on the docket: their earlier December disclosures make them look like under-reporters, and those corrections reproduce 2025 less closely. Not faculty with a single matched manufacturer-year reported low, whom an unweighted personal ratio promotes, nor faculty who leave small relationships out, whom the share of all published remuneration disclosed promotes.

## 2. Critical Components

1. **278** faculty members holding an appointment on 31 December 2026 filed a 2026 disclosure naming a manufacturer that reports to Open Payments, and each is estimated.
2. **Five** of the fifteen submitted the 2026 disclosure in force in December 2026, before part of the year's payments were made.
3. Compared on 2025 with the largest single-manufacturer remuneration the register published for each of the **308** faculty members estimated, the estimate that counts each disclosure to the day it was submitted comes closer than any that reads a disclosure as covering its whole year.

## 3. Step-by-Step Solution

1. Tied each record in open_payments_general_2021-2025_jan2027_extract.csv to a faculty member through its covered-recipient profile's NPI (open_payments_covered_recipient_profiles.csv) and the NPI in clinical_faculty_appointments.csv, and kept the five remuneration natures paid to the faculty member personally (policy 2.1 and 2.2), each payment with its Open Payments manufacturer ID and date of payment.
2. Took the version in force of each disclosure in coi_disclosures_2021-2026_export.xlsx with the Eastern date it was submitted, kept its remuneration items and gave each company its Open Payments ID from coi_entity_list.csv, a typed name or a listed company without an ID through the names manufacturers reported under in the register.
3. On each manufacturer-year from 2021 to 2025 that both sources carry, compared the amount disclosed with the payments the register shows made by the day that disclosure was submitted, and weighted each faculty member's disclosed-to-paid ratio toward the faculty-wide ratio by n/(n+2), n their manufacturer-years: the weighting of this estimate that comes closest under policy 5.4 when the 308 faculty members' 2025 estimates are compared with their largest 2025 single-manufacturer remuneration in the January 2027 publication.
4. Divided each 2026 amount disclosed for a manufacturer by the faculty member's weighted ratio and, where the disclosure in force was submitted in December 2026, by the share of the same manufacturer's 2025 payments to them made by that month and day (the faculty-wide share where it paid them nothing by then in 2025); took the largest for each of the 278 faculty members and ranked them: the fifteen above lead, and the sixteenth is Angelica Gentry.
5. Counted the faculty holding an appointment on 31 December 2026, one per NPI, by the department of the primary appointment that day (department_codes.csv giving the Department of Medicine's successors), and those with no submission of the 2026 disclosure under any of their employee numbers in coi_submission_history.csv by 11:59 p.m. Eastern on 15 January 2027: 1,695 owed, 91 not submitted.
6. Summed by nature the 2025 remuneration records tied through the profiles to the faculty holding an appointment at any time in 2025, payments made to the university excluded: $7,131,000.
7. Summed by relationship type the 2026 remuneration items in force whose company appears in the register under no name: $197,000.
8. Recommendation: the fifteen above form the docket for 11 February 2027.

## 4. Deliverable Answers

### coi_committee_docket_2027-02.docx

1. The fifteen faculty members on the docket, each with the manufacturer of their largest 2026 remuneration:
   - Adam Andersen: Glenarde Joint Technologies, Inc.
   - Kyle Avery: Norvell Therapeutics, Inc.
   - Fernando Baldwin: Ambrell Biologics, Inc.
   - Stacie Black: Clevedon Surgical, Inc.
   - Alexis Drake: Fallowfield Therapeutics, Inc.
   - Henry Grimes: Dunmere Neurotherapeutics, Inc.
   - Pedro Hampton: Morvanne Pharmaceuticals, Inc.
   - Johnathan Kaiser: Pinewold Vascular, LLC
   - Kerry Leach: Kelsall Vascular, LLC
   - Jillian Luna: Varrick Pharmaceuticals, Inc.
   - Kirsten Middleton: Tilbrook Heart Technologies, Inc.
   - Vickie Nolan: Carrowmore Pharmaceuticals, Inc.
   - Ruth Rosario: Pallister Neurotherapeutics, Inc.
   - Judith Valenzuela: Yarrowby Oncology, Inc.
   - Traci Ware: Saltmere Joint Technologies, Inc.
2. Horizontal bar chart on page 2: the fifteen members' estimated 2026 remuneration from a single manufacturer and, in grey below a dashed line, the sixteenth, Angelica Gentry.
3. Faculty who owed a 2026 disclosure and, of them, those who had not submitted it by 11:59 p.m. Eastern on 15 January 2027, by department:
   - Anesthesiology: 144 owed, 11 not submitted
   - Cardiovascular Medicine: 116 owed, 6 not submitted
   - Dermatology: 45 owed, 1 not submitted
   - Emergency Medicine: 95 owed, 2 not submitted
   - Gastroenterology and Hepatology: 69 owed, 6 not submitted
   - Hematology and Oncology: 95 owed, 5 not submitted
   - Internal Medicine: 203 owed, 9 not submitted
   - Neurology: 91 owed, 7 not submitted
   - Obstetrics and Gynecology: 107 owed, 4 not submitted
   - Ophthalmology: 55 owed, 1 not submitted
   - Orthopaedic Surgery: 98 owed, 6 not submitted
   - Pediatrics: 198 owed, 12 not submitted
   - Psychiatry: 100 owed, 4 not submitted
   - Radiology: 114 owed, 6 not submitted
   - Surgery: 127 owed, 10 not submitted
   - Urology: 38 owed, 1 not submitted
   - All departments: 1,695 owed, 91 not submitted
4. The 2025 remuneration Open Payments last published to faculty with appointments in 2025, by nature of payment, to the nearest thousand dollars:
   - Consulting fees: $4,531,000
   - Services other than consulting, including speaking outside continuing education: $1,387,000
   - Honoraria: $768,000
   - Faculty or speaker, accredited or certified continuing education: $254,000
   - Faculty or speaker, unaccredited continuing education: $190,000
   - All five natures: $7,131,000
5. 2026 remuneration the faculty disclosed from companies that do not report to Open Payments, by relationship type, to the nearest thousand dollars:
   - Consulting or advisory board: $57,000
   - Speaking or teaching: $11,000
   - Expert testimony: $126,000
   - Other paid services: $3,000
   - All types: $197,000

### faculty_remuneration_2026_conformed.csv

1. 9,987 rows, one per faculty member and year from 2021 to 2026 in which they owed a disclosure, under the employee number holding the appointment that 31 December, each with the remuneration disclosed, the number of manufacturers disclosed, the remuneration published (blank for 2026) and the number of manufacturers published.
