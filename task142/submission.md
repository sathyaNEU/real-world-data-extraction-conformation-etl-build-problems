## Tags

**Domain:** Sociology & Demography (population projection: a primary school's roll at its next three 1 October counts, each child of its catchment counted by whether a brother or sister is already on the roll).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**De Kwikstaart exceeds its buildings' capacity at the 1 October 2029 count, so the board should request extra accommodation from the 2029-30 school year.** The forecast roll is about 630 pupils against 604 places, while the 2027 count (510) and the 2028 count (580) stay within them. Not that the school stays within its places, which counts every coming child at the pooled 48 per cent of the last five intakes (571 at 2029-30), by neighbourhood (574) or on the share's trend (553). Not 2028-29, which counts every catchment child as an entrant (695 at 2028-29).

## 2. Critical Components

1. Of the last five intakes' 755 catchment children, the 71 with a brother or sister from the same household on the roll at their first count entered at **97 per cent** (69) and the 684 without one at **43 per cent** (293).
2. The children who first count in 2027, 2028 and 2029 number 146, 148 and 141, of whom **50, 47 and 52** have a brother or sister on the 2026 roll still there at their count.
3. The forecast roll is **510, 580 and 630** at the 2027, 2028 and 2029 counts against **604** places.

## 3. Step-by-Step Solution

1. Read spov_procedure_leerlingenprognose_v2.pdf sections 2.3 and 3.1 to 3.5 and huisvestingsplan_kwikstaart_2026.pdf: capacity 604, catchment 3841 and 3842, each coming child at the share of the last five intakes' children in its circumstance, taken together.
2. Took each intake's catchment children from brp_uittreksel_veenhaven_noord_2026-10-01.csv (living there on that 1 October, turned four in the twelve months to it) and matched them to leerlingtellingen_kwikstaart_1okt_2020-2026.csv by birth date, postcode, house number and addition: 362 of 755 entered.
3. Marked a child's circumstance when another member of its household in the register was on the roll at the child's first count: 69 of 71 such children entered (97 per cent), 293 of 684 others (43 per cent).
4. Took the 2026 roll (442 pupils) ageing through group 8 and the out-of-catchment entrants at their five-intake average (3.2 a count).
5. Counted the 435 catchment children who first count in 2027 to 2029 at their circumstance's share, 149 of them with a brother or sister on the 2026 roll still there at their count.
6. For gas, followed the plan's EANs to their buildings' descriptions in meterstamgegevens_gas_kwikstaart_2026-10-01.xlsx to pick up the dependance's EAN re-registered in January 2025, and took every meter's first and last register in each school year from the 06:00 reads of 1 August in gas_telemetrie_kwikstaart_2023-2026.csv or the master data's placement and removal readings.
7. For after-school care, kept the locations at Molenwiek 4 in bso_locaties_contracten_2026-10.xlsx (BSO-KWS to 11 October, BSO-MLW2 from 12 October) and the De Kwikstaart families in its contracts, and summed the children on each family row of bso_aanwezigheid_oktober_2026.csv.
8. Applied 3.5: 511.9 and 580.1 stay under 604 and 629.9 exceeds it, so the school is short from the 2029-30 count.

## 4. Deliverable Answers

### kwikstaart_leerlingenprognose_2027-2029.docx

1. Short of accommodation: yes, from the 1 October 2029 count (2029-30).
2. Forecast pupils against the capacity of 604, to the nearest 10:
   - 2027-28: 510, within
   - 2028-29: 580, within
   - 2029-30: 630, short
3. Entry shares: 97 per cent with a brother or sister on the roll, 43 per cent without.
4. Children first counting, and those with a brother or sister on the roll:
   - 1 October 2027: 50 of 146
   - 1 October 2028: 47 of 148
   - 1 October 2029: 52 of 141
5. Column chart of the forecast pupils at each count, the capacity of 604 drawn as a line.
6. Gas use of both buildings, m3 to the nearest 1,000: 2023-24 36,000; 2024-25 35,000; 2025-26 36,000.
7. After-school care attendances of De Kwikstaart pupils in the dependance, October 2026:
   - Monday: 157
   - Tuesday: 196
   - Wednesday: 182
   - Thursday: 246
   - Friday: 191
