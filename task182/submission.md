# task182 submission

## Tags

**Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (groundwater drawdown at landholder bores around an open-cut coal mine, attributed between climate and pumping).
**Analytical objective:** Anomaly Detection & Diagnostics (which bores show a decline the mine caused, as against the decline the dry seasons caused).

## 1. Final Recommendation

**Offer make-good agreements to four owners for five bores: Yarrowmere Pastoral Co Pty Ltd for KV-LB04 and KV-LB05 (one agreement), Tondara Grazing Pty Ltd for KV-LB07, Bluebush Downs Pty Ltd for KV-LB10 and Cypress Ridge Pastoral Trust for KV-LB12.**

The mine's drawdown at the September 2026 level is 8.2 to 9.3 m at the four coal-measure bores against a 5 m trigger and 4.6 m at KV-LB12 against 2 m. Not the four complainants' bores: they fell, but through the dry seasons, and the mine's share is 0.6 to 1.3 m. Not the decline since the baseline assessment, which names the alluvial bores and the ridge bore and misses the coal measures, which were still rising on the 2019 to 2021 wet seasons when dewatering began. Not the decline less the reference bores' fall, which keeps KV-LB12 alone, because no reference bore is in the coal measures.

## 2. Critical Components

1. The coal-measure bores KV-LB04, KV-LB05, KV-LB07 and KV-LB10 fell only **2.44, 2.49, 2.46 and 2.21 m** from their baseline assessments to September 2026
2. Each bore's own response to rainfall and evaporation, fitted before 4 July 2022 and run forward, puts the mine's drawdown at those four bores at **8.9, 9.3, 8.4 and 8.2 m**, and at KV-LB12 at **4.6 m**
3. The complainants' bores KV-LB01, KV-LB02, KV-LB06 and KV-LB18 fell **4.63, 5.23, 4.84 and 8.70 m**, of which the mine caused **0.8, 0.7, 0.6 and 1.3 m**
4. Five bores have impaired capacity, held by **four** owners

## 3. Step-by-Step Solution

1. Mapped every dip and logger to its bore through `landholder_bore_register.xlsx` (codes, registered numbers), converted the 2012 to 2014 EIS dips from feet, dropped entries keyed twice and dips whose remarks say the pump was running (MG-02 2.1), and reduced each dip to the measuring point in force on its date (MG-02 2.2).
2. Compensated each logger with `barometric_logger_2015-2026.csv` as the network notes set out, used the sensor depths in `logger_installations.csv`, and averaged the hours by Queensland day (MG-02 2.3).
3. Took each bore's September 2026 assessment level (MG-02 2.4) and its change since its baseline assessment in the register: the coal-measure bores near the pit fell only 2.21 to 2.49 m.
4. Fitted each bore's own gamma response to daily rainfall less a share of Morton areal evaporation (`daily_climate_1990-2026.csv`) on its readings to 3 July 2022: the coal-measure bores answer rain over six to seven years, the alluvium over about half a year.
5. Ran each fit forward to September 2026 and took the mine's drawdown as the fitted level less the assessment level: 8.2 to 9.3 m at the four coal-measure bores, 4.6 m at KV-LB12 and 2.4 m or less at the other 13.
6. Confirmed the fit on the three state reference bores, which it tracks within 0.3 m to September 2026, and with the take in `pit_dewatering_2022-2026.csv` fitted as a second stress over the full record: the same five bores.
7. Applied the triggers in MG-02 3.1 and the test in 4.1: KV-LB04, KV-LB05, KV-LB07, KV-LB10 and KV-LB12 have impaired capacity; the four complainants' bores do not.
8. Recommendation: four make-good offers under MG-02 6.1, with Yarrowmere's two bores in one agreement.

## 4. Deliverable Answers

### bore_impact_assessment.xlsx

1. Each register bore: September 2026 level, change since its baseline assessment, decline the mine caused, impaired capacity:
   - KV-LB01 (house bore, Saltbush Flat): 209.51 m AHD, -4.63 m, 0.8 m, no
   - KV-LB02 (yards bore, Brolga Plains): 205.24 m AHD, -5.23 m, 0.7 m, no
   - KV-LB03 (top bore, Wilga Vale): 204.86 m AHD, -4.64 m, 0.5 m, no
   - KV-LB04 (house bore, Yarrowmere): 207.77 m AHD, -2.44 m, 8.9 m, yes
   - KV-LB05 (Ten Mile bore, Yarrowmere): 214.47 m AHD, -2.49 m, 9.3 m, yes
   - KV-LB06 (garden bore, Ghost Gum): 209.61 m AHD, -4.84 m, 0.6 m, no
   - KV-LB07 (Tondara bore, Tondara): 195.44 m AHD, -2.46 m, 8.4 m, yes
   - KV-LB08 (windmill bore, Lancewood Flat): 201.27 m AHD, -4.81 m, 0.4 m, no
   - KV-LB09 (No. 2 bore, Bellbird Downs): 199.16 m AHD, -4.69 m, 0.3 m, no
   - KV-LB10 (dam bore, Bluebush Downs): 203.49 m AHD, -2.21 m, 8.2 m, yes
   - KV-LB11 (north bore, Gidgee Creek): 238.12 m AHD, -2.59 m, 1.1 m, no
   - KV-LB12 (creek bore, Cypress Ridge): 209.50 m AHD, -8.78 m, 4.6 m, yes
   - KV-LB13 (waterhole bore, Coolibah Springs): 202.33 m AHD, -0.98 m, 0.2 m, no
   - KV-LB14 (lagoon bore, Coolibah Springs): 201.88 m AHD, -0.87 m, 0.1 m, no
   - KV-LB15 (shed bore, Gidgee Creek): 241.33 m AHD, -3.02 m, 1.6 m, no
   - KV-LB16 (Kurrajong bore, Kurrajong Park): 209.84 m AHD, +1.74 m, 2.4 m, no
   - KV-LB17 (ridge paddock bore, Kurrajong Park): 243.13 m AHD, -2.68 m, 0.9 m, no
   - KV-LB18 (ridge bore, Bottletree): 245.75 m AHD, -8.70 m, 1.3 m, no

### make_good_recommendation.docx

1. Offers: Yarrowmere Pastoral Co Pty Ltd (KV-LB04 house bore and KV-LB05 Ten Mile bore, Yarrowmere); Tondara Grazing Pty Ltd (KV-LB07 Tondara bore, Tondara); Bluebush Downs Pty Ltd (KV-LB10 dam bore, Bluebush Downs); Cypress Ridge Pastoral Trust (KV-LB12 creek bore, Cypress Ridge).
2. Four offers.
3. What lowered each complainant's bore (none meets the test):
   - Ernest Walker, house bore KV-LB01: the four failed wet seasons since 2022-23; it fell 4.63 m, 0.8 m of it from the mine
   - Brolga Plains Cattle Co, yards bore KV-LB02: the dry seasons; it fell 5.23 m, 0.7 m of it from the mine
   - Clarence Lewis, garden bore KV-LB06: the dry seasons; it fell 4.84 m, 0.6 m of it from the mine
   - Bottletree Holdings Pty Ltd, ridge bore KV-LB18: the dry seasons draining the ridge basalt; it fell 8.70 m, 1.3 m of it from the mine
4. The method in plain words, in the note's last paragraph: each bore's own response to rainfall and evaporation fitted on its record before 4 July 2022, run forward, and the gap to the September 2026 level taken as the mine's share.
