# task248 submission

## Tags

**Domain:** Epidemiology & Public Health (disease surveillance and outbreak detection: a regional public health service's wastewater surveillance of SARS-CoV-2 at 24 treatment plants and the verification desk that checks every alert episode its dashboard raises).
**Analytical objective:** Data Quality Monitoring & Alerting (how many alert episodes the dashboard raises once it reads every sample on the shed load, with the RNA lost in the sewer restored, and so how many the verification desk plans for).

## 1. Final Recommendation

**Plan the verification desk for 26 alert episodes this winter.**

Last winter's samples (May to September 2027) raise 26 alert episodes on the shed load against the 30 the dashboard published: Ardenmouth South WWTP (ADS), Ardenmouth East WWTP (ADE), Tarnbrook WWTP (TRN), Cleaveland Flat WWTP (CLF) and Saltmarsh Point WWTP (SLT) each have one episode fewer and Ardenmouth West WWTP (ADW) one more; the other eighteen plants keep their counts.

Not the published 30, which any restoration that does not move over the year gives back (the paired study's single decay rate over each plant's travel time, or each sample divided by its PMMoV): it lifts a plant's winter samples and the samples that set its baseline alike. The RNA's decay rate rises with the water's temperature, so at the long trunk sewers the summer samples behind each baseline lost more than the winter samples, and restored at each composite's own temperature the winter rises that came from the colder water fall away. Not 28, restoring only the four plants of the paired study (Ardenmouth South and Cleaveland Flat move; Ardenmouth East, Ardenmouth West, Tarnbrook and Saltmarsh Point do not).

## 2. Critical Components

1. Over its 101 paired visits, the study's loss between the trunk's head and the plant fits first-order decay at **0.050 an hour at 20 degrees Celsius, rising about 9 per cent a degree** (theta 1.09).
2. The loss moves with the season: at Cleaveland Flat (1,615 minutes) the composites lost **0.69 log10 in December to February and 0.31 in June to August**; at Ardenmouth South (1,310 minutes) **0.52 and 0.24**.
3. A restoration constant over the year leaves every plant's count as published (**30**).

## 3. Step-by-Step Solution

1. Laboratory export: the accepted run of each sample and target (the export notes), the closure's composites from the contract laboratory's report; each sample's N1 load per person is the concentration times the composite's flow times 1,000 over the register's population served (methods note section 3).
2. Weekly values by the week (Monday to Sunday) of the day the composite ended, the baseline the 10th percentile (PERCENTILE.INC) of the weekly values of the weeks starting 6 April 2026 to 29 March 2027, levels the weekly value less the baseline; an episode opens at 1.0 or more and closes below 0.5, and winter 2027's episodes open in the weeks starting 3 May to 27 September 2027 (sections 4 and 5): 30 on the published basis, the dashboard's export.
3. Paired study: the three replicates of each point averaged, the loss the natural log of the plant's N1 over the upstream N1 (both in copies per millilitre), the travel time from the network memo in hours, the temperature the mean of the two points' readings; least squares of the loss on minus the travel time times k20 times theta^(T - 20) gives k20 0.050 an hour and theta 1.09.
4. Historian: each composite's mean inlet temperature over its 24 hours (08:00 to 08:00 local, start-of-hour stamps); each sample's shed load per person is its load times exp(k(T) times the travel time in hours).
5. Levels, baselines and episodes recomputed on the shed load per person (section 6.1): 26, with ADS -1, ADE -1, ADW +1, TRN -1, CLF -1 and SLT -1.
6. The same counts at every plant from a rate linear in temperature or fitted plant by plant, the plant's or the upstream reading or their mean, the composite's, the month's or the season's inlet temperature or that of the 24 hours a travel time earlier, and the historian's flow in place of the form's.
7. Historian hours, 1 April 2027 to 31 March 2028: the year's 8,784 real local hours (the clock skips 02:00 on 26 September 2027 and repeats 02:00 on 4 April 2027), exact duplicate rows removed; an hour lacks a valid inlet flow reading when it has no row, a blank flow, a flow of zero or below, or a held reading (after the first of four or more identical consecutive readings), as the export note defines.
8. Faecal-strength check (section 6.3): each composite's PMMoV load per person on the historian's inflow over its 24 hours (the mean of its valid hourly readings times 24); the contract laboratory's extract (100 microlitres) holds the copies of 200 microlitres of the 2 millilitres of resuspended pellet from 100 millilitres of wastewater, so a copy per microlitre of extract is 10,000 a litre; each composite against the median of the plant's composites of the 365 days before it, more than 0.5 log10 above or below failing.

## 4. Deliverable Answers

### winter_2027_episodes_shed_load.xlsx

1. Winter 2027 alert episodes: **30 on the published basis and 26 on the shed load**.
2. Six plants' counts move: Ardenmouth South WWTP (ADS) -1, Ardenmouth East WWTP (ADE) -1, Ardenmouth West WWTP (ADW) +1, Tarnbrook WWTP (TRN) -1, Cleaveland Flat WWTP (CLF) -1 and Saltmarsh Point WWTP (SLT) -1.
3. Each plant's hours from 1 April 2027 to 31 March 2028 with no valid inlet flow reading in the historian:
   - ASD Ashgrove Downs WWTP: 60
   - BRK Brackenridge WWTP: 36
   - CRF Carrisford WWTP: 56
   - DNK Dunkerley WWTP: 36
   - FNK Fennick WWTP: 33
   - GLO Glenorrin WWTP: 65
   - HOL Hollinsbury WWTP: 30
   - INB Inverbrack WWTP: 46
   - KSB Kestrel Bay WWTP: 64
   - LRF Larchfield WWTP: 29
   - MRB Marrowby WWTP: 45
   - NTL Netherleigh WWTP: 36
   - ORB Orrin Bay WWTP: 39
   - PLH Pellingham WWTP: 70
   - QRM Quarrymoor WWTP: 42
   - RVG Ravensgill WWTP: 52
   - ADN Ardenmouth North WWTP: 67
   - ADS Ardenmouth South WWTP: 13
   - ADE Ardenmouth East WWTP: 50
   - ADW Ardenmouth West WWTP: 34
   - TRN Tarnbrook WWTP: 44
   - UWD Upper Waldon WWTP: 52
   - CLF Cleaveland Flat WWTP: 44
   - SLT Saltmarsh Point WWTP: 40
4. Each plant's composites from 4 October 2027 to 30 March 2028 that fail the faecal-strength check:
   - ASD Ashgrove Downs WWTP: 0
   - BRK Brackenridge WWTP: 1
   - CRF Carrisford WWTP: 3
   - DNK Dunkerley WWTP: 0
   - FNK Fennick WWTP: 4
   - GLO Glenorrin WWTP: 3
   - HOL Hollinsbury WWTP: 5
   - INB Inverbrack WWTP: 2
   - KSB Kestrel Bay WWTP: 4
   - LRF Larchfield WWTP: 1
   - MRB Marrowby WWTP: 4
   - NTL Netherleigh WWTP: 4
   - ORB Orrin Bay WWTP: 2
   - PLH Pellingham WWTP: 3
   - QRM Quarrymoor WWTP: 1
   - RVG Ravensgill WWTP: 1
   - ADN Ardenmouth North WWTP: 7
   - ADS Ardenmouth South WWTP: 2
   - ADE Ardenmouth East WWTP: 2
   - ADW Ardenmouth West WWTP: 5
   - TRN Tarnbrook WWTP: 3
   - UWD Upper Waldon WWTP: 5
   - CLF Cleaveland Flat WWTP: 7
   - SLT Saltmarsh Point WWTP: 2

### verification_desk_winter_2028.docx

- The number to plan for, 26 alert episodes, and a chart of each plant's winter 2027 episodes on the published basis and on the shed load (ADS, ADE, TRN, CLF and SLT lower by one, ADW higher by one).
