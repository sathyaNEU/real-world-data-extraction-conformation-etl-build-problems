## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Designate four of the eight segments for the 2027 Selectivity Programme: TR1, TR2, NEP and BT.**
They discarded 12 to 14 per cent of their 2025 catch by weight, TR2 nearest the line at 12 per cent, and SN, the highest of the rest, discarded 8 per cent. Not NEP alone, which the observers' discards raised to every trip give (NEP 12.0 per cent, TR1 4.0, TR2 4.1, BT 2.9): an observed trip lands the undersized quota fish (BMS) that an unobserved trip throws back, so the observers record as kept what the rest of the fleet discards. TR1's observed trips declared 25.28 kg of BMS an hour fished and its unobserved trips 2.10. Not the observed trips' unwanted catch with the grounds pooled, which leaves BT under the line because observed beam trawl trips fish the inshore grounds less; and not every unobserved trip's BMS counted as discarded, which puts GN over it although most gillnetters land their BMS every trip.

## 2. Critical Components

1. Discard shares of 2025 catch by weight: TR1 **13** per cent; TR2 **12** per cent; NEP **14** per cent; BT **12** per cent; SN **8** per cent; GN **7** per cent; LL **5** per cent; POT **6** per cent.
2. BMS declared an hour fished, observed against unobserved trips: TR1 **25.28** against **2.10** kg; TR2 **9.97** against **0.84** kg; NEP **1.44** against **0.11** kg; BT **4.66** against **0.06** kg; SN **6.82** against **0.05** kg.
3. Of the **12,000** trips begun in 2025, **856** were observed; the others' discards are the unwanted catch (BMS and lawful discards) an hour fished that the same segment's observed trips show on the same ground, times their hours there, less the BMS they declared.
4. Observed beam trawl trips spent **39** per cent of their hours on WC14 and WC15 and unobserved ones **69** per cent, so the raising is done ground by ground.

## 3. Step-by-Step Solution

1. Took the terms in selectivity_programme_terms_2027.pdf: a segment is designated above 10 per cent of its 2025 catch by weight, catch being everything landed or returned on every trip begun in 2025, in live weight.
2. Built each trip from elogbook_trips_2025.csv (ground, hours fished) and elogbook_landings_2025.csv (live weight above MCRS and BMS), with its segment from vessel_register.csv: 12,000 trips.
3. Matched the 856 observed trips in observer_deployments_2025.csv to the logbook by vessel (port letters and number written alike) and notified departure in UK time, and summed observer_hauls_2025.csv by fraction.
4. Compared observed with unobserved trips on the same grounds: BMS declared an hour fished (TR1 25.28 against 2.10 kg) and hours on WC14 and WC15 (BT 39 against 69 per cent).
5. For each segment and ground, raised the observed trips' unwanted catch (BMS and DIS) an hour fished to the unobserved trips' hours there, took off the BMS those trips declared, and added the observed trips' DIS.
6. Divided each segment's discards by its catch (every trip's declared landings plus those discards) and designated the segments above 10 per cent: TR1, TR2, NEP and BT.
7. For first-sale value, summed sales_notes_2025.csv over 2025 landing dates, leaving out the lines Barlow & Hobbs filed at Kestlemouth and Brindlesea for lots the market sold (the vessel, landing date, species and grade of a market lot, the weight within 3 per cent of the lot's).
8. For days at sea, counted UK calendar days with a report outside port_limits.csv in vms_positions_2025.csv, each report given to the vessel that carried its terminal: a terminal vms_transponders.csv holds as one vessel's previous and another's current was the first vessel's until that vessel's own terminal began reporting, the second's after its previous terminal stopped.

## 4. Deliverable Answers

### segment_discards_2025.xlsx

1. Discard share of 2025 catch (whole per cent) and designation, every segment:
   - TR1 (demersal otter trawl, 18 m and over): 13 per cent, designated
   - TR2 (demersal otter trawl, 12 m to under 18 m): 12 per cent, designated
   - NEP (Nephrops trawl): 14 per cent, designated
   - BT (beam trawl): 12 per cent, designated
   - SN (seine): 8 per cent, not designated
   - GN (set gillnet): 7 per cent, not designated
   - LL (set longline): 5 per cent, not designated
   - POT (pots and creels): 6 per cent, not designated
2. First-sale value of 2025 landings (thousands of pounds, one decimal):
   - TR1: 12,062.3
   - TR2: 7,174.4
   - NEP: 8,053.4
   - BT: 9,649.8
   - SN: 3,561.4
   - GN: 1,719.9
   - LL: 693.8
   - POT: 2,332.9
3. Vessels' total days at sea in 2025 (whole days):
   - TR1: 2,236
   - TR2: 3,032
   - NEP: 3,517
   - BT: 2,128
   - SN: 1,737
   - GN: 2,419
   - LL: 1,362
   - POT: 2,593

### segment_discards_2025.png

1. One bar chart of the eight segments' discard shares against the 10 per cent line, the four designated segments (TR1, TR2, NEP and BT) highlighted.
