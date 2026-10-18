## Tags

**Domain:** Survey Research & Official Statistics (register and administrative data quality: a parking revenue control system's register of entries completed by a card survey of the parked cars, whose replies come back only when the car leaves).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**The 2027 pitch for new nonstop service from Kessick Valley Regional should carry Phoenix, Tampa and Washington.**
They carried 6,400, 6,300 and 5,900 of the service area's 2026 trips parked at Brennick International; New York, the first market left out, carried 4,700, 1,200 below Washington. Not Washington, New York and Dallas, which each wave's returned cards expanded to its quarter give, because a card comes back only when its car leaves and each wave's boxes were taken in on the night of the second day after its last handout, so the long stays' cards handed in a wave's later days never came back.

## 2. Critical Components

1. Transient entries in Economy C, Economy D and Long-Term, 2026: first quarter **205,095**, second **239,764**, third **262,549**, fourth **227,457**.
2. Trips, 2026: Phoenix **6,400**, Tampa **6,300** and Washington **5,900**.
3. First market left out: New York, **4,700** trips, **1,200** below Washington.

## 3. Step-by-Step Solution

1. Read brennick_parking_survey_2026_cards.csv, dropped the 110 rows that repeat a card number (keying batch 3-55 exported twice), kept the cards whose home ZIP's first five digits are on kvr_service_area_zip_codes.csv and gave each card the city market of its destination_code through bureau_city_markets.csv.
2. Took the candidates as Appendix A's shortlist in bureau_air_service_pitch_standard_2027.pdf less Orlando, served seasonally at Sanford in kvr_nonstop_schedule_2027.pdf (section 3.1): 14 markets.
3. Found each card's handout day from its number in brennick_parking_survey_2026_handout_log.pdf, and each wave's last box collection, day 30 of the wave, in Table 1 of brennick_parking_survey_2026_methods_report.pdf.
4. Weighted each card by its wave's cards handed over the cards handed on the days from which a stay of its nights could end by the last box collection, since a card comes back only when its car leaves.
5. Expanded each candidate's share of each wave's weighted cards (every card in the denominator) to its quarter's transient entries in Economy C, Economy D and Long-Term from the four extracts (standard 2.1, 2.4) and added the quarters.
6. Counted passengers the same way, each card's party being its Q4 answer in brennick_parking_survey_2026_verbatims.csv (the numbers written added, "me" one).
7. Ranked the candidates on trips: Phoenix, Tampa and Washington lead, and New York is first left out, 1,200 trips below Washington.
8. Recommended Phoenix, Tampa and Washington for the 2027 pitch (standard 4.1).

## 4. Deliverable Answers

### kvr_2027_pitch_markets.csv

1. Each candidate market's 2026 trips from the service area parked at Brennick and the passengers they carried, nearest hundred:
   - Phoenix (PHX): 6,400 trips, 11,200 passengers
   - Tampa (TPA): 6,300 trips, 10,400 passengers
   - Washington (WAS): 5,900 trips, 7,700 passengers
   - New York (NYC): 4,700 trips, 6,500 passengers
   - Dallas (DFW): 4,400 trips, 5,500 passengers
   - Myrtle Beach (MYR): 3,100 trips, 9,400 passengers
   - Boston (BOS): 2,900 trips, 3,700 passengers
   - Las Vegas (LAS): 2,800 trips, 5,500 passengers
   - Houston (HOU): 2,500 trips, 3,200 passengers
   - Nashville (BNA): 2,100 trips, 3,900 passengers
   - Fort Myers (RSW): 2,000 trips, 3,500 passengers
   - Denver (DEN): 2,000 trips, 3,400 passengers
   - San Diego (SAN): 1,600 trips, 3,300 passengers
   - Fort Lauderdale (FLL): 1,200 trips, 2,700 passengers

### kvr_2027_route_pitch_brief.docx

1. The three markets: Phoenix, Tampa and Washington.
2. First market left out: New York, 4,700 trips, 1,200 trips below Washington.
3. Bar chart of the 14 candidate markets' 2026 trips, the three marked.
