# task234 submission

## Tags

**Domain:** Epidemiology & Public Health (disease surveillance and outbreak anomaly detection: the completeness of a county's respiratory laboratory result feeds judged against the tests each laboratory ran, read from each stream's own positivity).
**Analytical objective:** Data Quality Monitoring & Alerting (which result streams the laboratory liaison escalates under the feed completeness protocol for MMWR week 3 of 2027).

## 1. Final Recommendation

**Escalate the influenza, RSV and SARS-CoV-2 streams of Wexmoor Regional Medical Center Laboratory and of Westmarch Reference Laboratory for MMWR week 3 of 2027, and no other stream.**

Against the tests each stream's own positivity says its laboratory ran in the week, Wexmoor's three streams (influenza, RSV, SARS-CoV-2) are 55, 57, 56 per cent complete and Westmarch's 55, 56, 61, while every other stream is at 87 per cent or more (Bluestem's RSV, the lowest). A lost result message drops a positive and a negative alike, so the week's received positivity is the laboratory's, and the laboratories' tests follow it. Not last week's aggregate report as the week's tests, which escalates 15 streams, 9 of them complete streams whose epidemic fell in the week (the SARS-CoV-2 streams of seven laboratories and Tamsen Children's Hospital's influenza and RSV). Not the seasonal baseline of the same weeks in earlier winters, which escalates the same SARS-CoV-2 streams and Tamsen Children's Hospital's RSV and misses Wexmoor's influenza, this winter's influenza running later and higher than any before it. Not the other laboratories' change this week, which misses Westmarch's influenza and SARS-CoV-2, the rural clinics' epidemics still rising, and escalates Tamsen Children's Hospital's influenza. Not the week's positives over last week's positivity, which misses Wexmoor's three streams and Westmarch's SARS-CoV-2, the lost messages taking their positives with them.

## 2. Critical Components

1. Week-3 tests on the platform: Wexmoor **3,128, 607, 1,234** (influenza, RSV, SARS-CoV-2), Westmarch **1,943, 621, 1,454**
2. Their week-3 positivity: Wexmoor **33.1, 7.9, 9.6** per cent, Westmarch **23.3, 9.0, 17.0** per cent
3. Tests that positivity predicts: Wexmoor **5,732, 1,061, 2,216**, Westmarch **3,521, 1,103, 2,381**
4. Completeness: Wexmoor **55, 57, 56** per cent, Westmarch **55, 56, 61** per cent; every other stream **87** per cent or more

## 3. Step-by-Step Solution

1. Collapsed the week-3 messages in elr_respiratory_results_extract_2027-01-25.csv to tests under FCP-2 section 2 (one per laboratory, accession and virus; RV-FLUA and RV-FLUB one influenza test; a corrected result in place of the one it corrects; cancelled orders out; the week by the county date of the first release; facilities to laboratories by respiratory_stream_register.xlsx): 80,671 tests across the 29 streams.
2. Took each stream's week-3 positivity from those tests (a test is positive when its standing result is DETECTED): Wexmoor 33.1, 7.9, 9.6 per cent, Westmarch 23.3, 9.0, 17.0 per cent.
3. For each stream, regressed the log of the weekly tests on the week's positivity and a linear time trend over every report of record in lab_weekly_aggregate_reports.csv (the latest version, 2022 week 40 to 2027 week 2, the weeks holding Thanksgiving, Christmas Day and New Year's Day left out), and read it at the week-3 positivity: Wexmoor 5,732, 1,061, 2,216 tests, Westmarch 3,521, 1,103, 2,381.
4. Divided each stream's tests on the platform by those tests (FCP-2 section 3) and escalated each stream below 80 per cent (section 4): Wexmoor at 55, 57, 56 per cent, Westmarch at 55, 56, 61, every other stream at 87 or more.
5. Week 2 (FCP-2 sections 3 and 5): receipt times before the state hub's broker migration (surveillance_platform_change_log.csv, 19 January 2027 06:00) are county time (read as UTC, most would come about six hours before the release of the result they carry) and later ones UTC, so the results each laboratory's interface held from Saturday evening and sent on Monday morning arrived after the 08:00 cutoff on 18 January; tests whose first result arrived by the cutoff over the week-2 report of record give 93.8 (Bluestem RSV) to 98.0 (Tamsen Children's Hospital influenza) per cent.
6. Specimens (FCP-2 section 6): distinct patient number and collection time among each laboratory's week-3 tests on the platform, whatever accessions its tests carry: 2,835 (Westmarch) to 9,204 (Bluestem).
7. Escalated the influenza, RSV and SARS-CoV-2 streams of Wexmoor Regional Medical Center Laboratory and Westmarch Reference Laboratory.

## 4. Deliverable Answers

### respiratory_feed_escalations_2027-W03.xlsx

1. Escalation for week 3, each laboratory's streams:
   - Tamsen Children's Hospital Laboratory: influenza no; RSV no; SARS-CoV-2 no
   - Ellery Memorial Hospital Laboratory: influenza no; RSV no; SARS-CoV-2 no
   - Wexmoor Regional Medical Center Laboratory: influenza escalate; RSV escalate; SARS-CoV-2 escalate
   - Corrigan Valley Hospital Laboratory: influenza no; RSV no; SARS-CoV-2 no
   - Brandmoor Hospital Laboratory: influenza no; RSV no; SARS-CoV-2 no
   - Bluestem Urgent Care Laboratory: influenza no; RSV no; SARS-CoV-2 no
   - Ridgeline Clinics Laboratory: influenza no; RSV no; SARS-CoV-2 no
   - Copperleaf Urgent Care Laboratory: influenza no; RSV no; SARS-CoV-2 no
   - Arbor Point Laboratory Services: influenza no; SARS-CoV-2 no
   - Westmarch Reference Laboratory: influenza escalate; RSV escalate; SARS-CoV-2 escalate
2. Week-2 completeness, per cent to one decimal place:
   - Tamsen Children's Hospital Laboratory: influenza 98.0; RSV 96.9; SARS-CoV-2 97.0
   - Ellery Memorial Hospital Laboratory: influenza 97.2; RSV 97.3; SARS-CoV-2 97.5
   - Wexmoor Regional Medical Center Laboratory: influenza 95.7; RSV 96.3; SARS-CoV-2 96.0
   - Corrigan Valley Hospital Laboratory: influenza 97.6; RSV 97.5; SARS-CoV-2 97.5
   - Brandmoor Hospital Laboratory: influenza 95.0; RSV 95.8; SARS-CoV-2 95.7
   - Bluestem Urgent Care Laboratory: influenza 94.0; RSV 93.8; SARS-CoV-2 94.9
   - Ridgeline Clinics Laboratory: influenza 96.9; RSV 97.6; SARS-CoV-2 97.0
   - Copperleaf Urgent Care Laboratory: influenza 96.2; RSV 97.9; SARS-CoV-2 96.0
   - Arbor Point Laboratory Services: influenza 95.4; SARS-CoV-2 95.2
   - Westmarch Reference Laboratory: influenza 94.3; RSV 94.0; SARS-CoV-2 94.1
3. Specimens tested in week 3 with results on the platform:
   - Tamsen Children's Hospital Laboratory: 2,850
   - Ellery Memorial Hospital Laboratory: 6,804
   - Wexmoor Regional Medical Center Laboratory: 4,046
   - Corrigan Valley Hospital Laboratory: 5,440
   - Brandmoor Hospital Laboratory: 4,408
   - Bluestem Urgent Care Laboratory: 9,204
   - Ridgeline Clinics Laboratory: 9,094
   - Copperleaf Urgent Care Laboratory: 7,219
   - Arbor Point Laboratory Services: 4,217
   - Westmarch Reference Laboratory: 2,835

### respiratory_feed_completeness_2027-W03.png

4. Horizontal bar chart of the 29 streams' week-3 completeness against the 80 per cent line, grouped by laboratory: the six bars of Wexmoor Regional Medical Center Laboratory and Westmarch Reference Laboratory below the line, every other bar above it.
