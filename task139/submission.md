## Tags

**Domain:** Actuarial Science & Insurance (claims frequency and severity: a workers' compensation nurse programme's saving read from a randomised pilot as indemnity per assigned intake and valued per nurse place-day).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Haverline should place the seventeen Early Return Nursing teams three each in healthcare strains and sprains (HC-SS), manufacturing strains and sprains (MF-SS), manufacturing other injuries (MF-OT), construction other injuries (CN-OT) and healthcare other injuries (HC-OT), two in retail and warehousing strains and sprains (RW-SS) and none in RW-OT or CN-SS, and book an AY2027 indemnity credit of $4,100,000.**
A team saves $290,000 a year in HC-SS and RW-SS and $280,000 in MF-SS, read per assigned intake as the pilot was randomised, against $190,000 for HC-OT, the last unit funded, and $130,000 for RW-OT, the first left out. Not a placement on the saving per verified indemnity claim, which compares the nurses' remaining claims with all of usual handling's and leaves the healthcare and retail strain units without a team, because the nurses kept part of their strain intakes from ever paying indemnity. Not three teams in RW-SS, whose intakes keep only two teams' places in use.

## 2. Critical Components

1. Per assigned intake, HC-SS, RW-SS and MF-SS save **$857**, **$741** and **$889** of ultimate indemnity: the nurses' intakes paid indemnity at **64.9%**, **57.5%** and **68.1%** against usual handling's **86.6%**, **83.9%** and **86.7%**.
2. An ERN intake held **21.40**, **18.85** and **23.03** place-days in those segments, so a team there saves **$290,000**, **$290,000** and **$280,000** a year.
3. RW-SS's **944** intakes reported October 2025 to September 2026 fill **2.44** teams' places at 18.85 place-days, so it takes **2** teams and the seventeenth goes to HC-OT.

## 3. Step-by-Step Solution

1. Took each of the 5,227 pilot intakes and its group from ern_pilot_assignments_2023-25.xlsx, its segment through segment_code_crosswalk_2025.csv, and whether it paid indemnity from claim_type in claims_extract_2021-01_to_2026-09.csv on legacy_claim_no: 4,339 paid.
2. Took each group's mean verified ultimate TTD, TPD and PPD per sampled claim in each segment from kpa_ern_indemnity_verification_2026-06-30.xlsx (100 a group and segment), its claim numbers matched to the register with the control digit dropped.
3. Per the pick memo's credit (what the teams' intakes would pay with their adjusters alone, less what they pay with a team), each segment's saving per intake is usual handling's share of intakes paying indemnity times its mean, less ERN's: Critical Component 1.
4. Summed each ERN intake's place-days in ern_case_log_2023-25.csv, both days counted and reopenings added as the charter's files-and-places section sets out, and averaged them over the segment's ERN intakes: Critical Component 2.
5. Valued a team at 7,300 place-days a year (pick memo 3) times the saving per intake over the place-days per intake: the team savings in block 4.
6. Applied the charter's fill rule with each unit's intakes reported October 2025 to September 2026 in the claims extract times its place-days per intake over 7,300: RW-SS fills 2.44 teams, every other unit at least three.
7. Placed seventeen teams, highest saving per team-year first, at most three a unit (the charter) and within each unit's fill: three each to HC-SS, MF-SS, MF-OT, CN-OT and HC-OT and two to RW-SS.
8. Summed each team's saving per team-year for the AY2027 credit (pick memo 3 to 5): $4,100,000.

## 4. Deliverable Answers

### ern_placement_ay2027.xlsx

1. Teams and what one team there saves in a year, by segment:
   - HC-SS healthcare and social assistance, strains and sprains: 3 teams, $290,000
   - HC-OT healthcare and social assistance, other injuries: 3 teams, $190,000
   - RW-SS retail and warehousing, strains and sprains: 2 teams, $290,000
   - RW-OT retail and warehousing, other injuries: 0 teams, $130,000
   - MF-SS manufacturing, strains and sprains: 3 teams, $280,000
   - MF-OT manufacturing, other injuries: 3 teams, $210,000
   - CN-SS construction, strains and sprains: 0 teams, $120,000
   - CN-OT construction, other injuries: 3 teams, $200,000
2. Total AY2027 saving: $4,100,000
3. Intakes reported in 2025, by segment:
   - HC-SS: 1,537
   - HC-OT: 822
   - RW-SS: 939
   - RW-OT: 708
   - MF-SS: 1,356
   - MF-OT: 770
   - CN-SS: 1,109
   - CN-OT: 666
4. Indemnity paid on each segment's claims, January to September 2026:
   - HC-SS: $3,725,000
   - HC-OT: $4,652,000
   - RW-SS: $1,805,000
   - RW-OT: $3,993,000
   - MF-SS: $4,277,000
   - MF-OT: $5,233,000
   - CN-SS: $4,999,000
   - CN-OT: $7,282,000

### ern_placement_note_ay2027.pdf

1. One page that opens with the placement (three teams each in HC-SS, MF-SS, MF-OT, CN-OT and HC-OT, two in RW-SS, none in RW-OT or CN-SS) and the $4,100,000 credit.
2. Bar chart of each segment's saving per team-year, highest first, each bar labelled with the teams the segment gets.
