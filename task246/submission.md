# task246 submission

## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: a county nutrition surveillance round's MUAC readings, each zone's wasting prevalence net of its anthropometrists' offset and error against the supervisor).
**Analytical objective:** Data Quality Monitoring & Alerting (which zones' 2027 long-rains wasting figures carry the measurement note into the early warning bulletin, with each zone's household response and death rates for the annex).

## 1. Final Recommendation

**Seven of the twelve zones' figures carry the measurement note: North Pastoral, North Lakeshore, Central Pastoral, Laga Town, East Pastoral, West Pastoral and West Riverine, whose figures from the readings and from their children's own arm circumference differ by 4.0, 4.1, 3.8, 5.2, 5.1, 2.9 and 4.5 points; the other five zones carry no note.**

In Central Pastoral the readings' figure is the lower one; in the other six it is the higher.

The children's own figure takes each anthropometrist's offset against the supervisor out of its readings and the variance of its single readings' departures from the supervisor about that offset out of the zone's spread. Not the four zones the test's repeat error gives (North Pastoral, Central Pastoral, Laga Town and East Pastoral), which misses North Lakeshore, West Pastoral and West Riverine: their anthropometrists' repeat error (TEM) is 1.7, 1.2 and 1.0 mm but they depart from the supervisor child to child by 5.8, 5.1 and 6.3 mm. Not the eight zones the mean squared departure gives, which counts the offset twice and adds East Riverine.

## 2. Critical Components

1. Each anthropometrist's offset against the supervisor, in mm: **Titus Ouma -2.1; Centrine Kinya +0.4; Steve Abdikadir -0.4; Halima Mohamud -0.5; Pius Kiplangat +2.9; Diana Kilonzo +0.2; Edwin Njoroge -0.3; Betty Jepchumba -2.9; Emmanuel Mutemi -2.5; Albert Bosire +3.7; Sharon Kinuthia -4.0; Cosmas Kibet -0.5; Joan Bashir -0.1**.
2. Each anthropometrist's departure from the supervisor about its offset, standard deviation in mm: **Titus Ouma 2.7; Centrine Kinya 2.1; Steve Abdikadir 5.8; Halima Mohamud 2.6; Pius Kiplangat 2.4; Diana Kilonzo 2.8; Edwin Njoroge 2.0; Betty Jepchumba 2.9; Emmanuel Mutemi 2.4; Albert Bosire 1.9; Sharon Kinuthia 2.3; Cosmas Kibet 6.3; Joan Bashir 5.1**.
3. The seven noted zones' figures from the readings and from the children's own arm circumference (accepted range), per cent: **North Pastoral 10.7 and 6.7 (6.5 to 6.8); North Lakeshore 17.8 and 13.7 (13.6 to 14.6); Central Pastoral 7.0 and 10.8 (10.8 to 10.8); Laga Town 12.1 and 6.9 (6.9 to 6.9); East Pastoral 14.5 and 9.4 (9.3 to 9.4); West Pastoral 17.4 and 14.5 (14.4 to 14.8); West Riverine 18.2 and 13.7 (13.6 to 14.7)**.

## 3. Step-by-Step Solution

1. Children from the two anthropometry exports: NCHA's MUAC in mm with the age in completed months from dob to today, team 2's rows of 22 June sent twice taken once (each child once, protocol section 6); PRK's MUAC in cm times ten with Age (months); children 6 to 59 months, MUAC from 75 to 220 mm or oedema; each cluster's zone from the cluster sample; the anthropometrist on duty from the teams workbook (PRK team 4's from the cluster of 28 June).
2. Each zone's figure from the readings (section 6): oedema counted, the rest's share below 125 mm read from the normal with the readings' mean and standard deviation.
3. The standardisation test (section 5): each anthropometrist's readings of the test children against the supervisor's mean of her two readings, both sessions together: the offset is the mean departure, and the random error the variance of the single readings' departures about it; the scattered three depart by 5.8, 5.1 and 6.3 mm with a repeat error (TEM) of 1.7, 1.2 and 1.0 mm.
4. Each zone's figure from the children's own arm circumference (sections 6 and 7): each reading less its anthropometrist's offset, the variance of those values less the mean random error of the readings' anthropometrists, the share below 125 mm read the same way; the accepted range runs over the standard variants (the correction made by zone, sessions apart, divisors n, the reference's own error, only offsets that stand out, the error through the children's means), seven readings that give the same notes.
5. The note (section 7): the two figures to one decimal differ by 2.0 points or more in North Pastoral (+4.0), North Lakeshore (+4.1), Central Pastoral (-3.8), Laga Town (+5.2), East Pastoral (+5.1), West Pastoral (+2.9) and West Riverine (+4.5) (the readings' figure less the children's own).
6. Household response (section 10) from the county's household visits: each selected household's last visit, interviewed over selected less empty dwellings; before 21 June the form coded an absent household 3 and an empty dwelling 4, the dictionary's version 4 the other way round (all 55 households coded 3 at a first visit before 21 June were visited again and none of the 32 coded 4; from 21 June none of 118 coded 3 and all 168 coded 4, section 2).
7. Death rates (section 9) from the member rosters and the births module: each member once (one cluster's forms were sent twice); a death is status D, a member who left because they died away from home, or a newborn who died on the births module; before 21 June the reasons 3 and 4 also ran the other way round (7 of the 10 members coded 3 then are 15 or older, and none coded 3 from 21 June is); the mid-point population times the recall days from the sub-county's start event (Annex B), per 10,000 a day; under-fives are the members aged in months.

## 4. Deliverable Answers

### lr2027_muac_measurement_review.xlsx

1. Zones, 12 rows in the protocol's order: figure from the MUAC readings, figure from the children's own arm circumference (accepted range), per cent to one decimal, and the measurement note:
   - North Pastoral: 10.7; 6.7 (6.5 to 6.8); note
   - North Agro-pastoral: 5.9; 6.0 (5.5 to 6.0); no note
   - North Lakeshore: 17.8; 13.7 (13.6 to 14.6); note
   - Central Pastoral: 7.0; 10.8 (10.8 to 10.8); note
   - Central Agro-pastoral: 5.2; 4.5 (4.5 to 4.6); no note
   - Laga Town: 12.1; 6.9 (6.9 to 6.9); note
   - East Pastoral: 14.5; 9.4 (9.3 to 9.4); note
   - East Riverine: 6.3; 4.8 (4.8 to 4.8); no note
   - East Agro-pastoral: 7.4; 6.5 (6.5 to 7.0); no note
   - West Pastoral: 17.4; 14.5 (14.4 to 14.8); note
   - West Agro-pastoral: 7.9; 7.4 (7.4 to 7.4); no note
   - West Riverine: 18.2; 13.7 (13.6 to 14.7); note
2. Household response rate, per cent to one decimal:
   - North Pastoral 96.4
   - North Agro-pastoral 96.6
   - North Lakeshore 94.8
   - Central Pastoral 97.9
   - Central Agro-pastoral 95.5
   - Laga Town 95.3
   - East Pastoral 97.1
   - East Riverine 96.9
   - East Agro-pastoral 95.5
   - West Pastoral 96.0
   - West Agro-pastoral 95.9
   - West Riverine 94.9
3. Crude death rate, deaths per 10,000 people per day to two decimals:
   - North Pastoral 0.83
   - North Agro-pastoral 0.84
   - North Lakeshore 0.48
   - Central Pastoral 0.80
   - Central Agro-pastoral 0.42
   - Laga Town 0.44
   - East Pastoral 0.51
   - East Riverine 0.56
   - East Agro-pastoral 0.70
   - West Pastoral 0.40
   - West Agro-pastoral 0.63
   - West Riverine 0.48
4. Under-five death rate, deaths per 10,000 children under five per day to two decimals:
   - North Pastoral 1.26
   - North Agro-pastoral 2.11
   - North Lakeshore 0.96
   - Central Pastoral 1.85
   - Central Agro-pastoral 0.84
   - Laga Town 1.11
   - East Pastoral 0.50
   - East Riverine 1.12
   - East Agro-pastoral 1.90
   - West Pastoral 0.64
   - West Agro-pastoral 0.68
   - West Riverine 1.70

### lr2027_gam_measurement_note.pdf

- One page for the bulletin desk: seven zones carry the note (North Pastoral, North Lakeshore, Central Pastoral, Laga Town, East Pastoral, West Pastoral and West Riverine), and a chart of each zone's figure from the readings and from its children's own arm circumference against the Normal, Alert, Alarm and Emergency bands, the noted zones marked.
