## Tags

**Domain:** Political science and public policy (election and polling forecasting).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Apply for protected action ballot orders at 11 councils: Ardeen Shire Council; Copeland Downs Shire Council; Corrigan Valley Shire Council; Fairholme Shire Council; Halston City Council; Lindale City Council; Northvale City Council; Pellham City Council; Stanwick Shire Council; Valmont City Council; Westhaven Shire Council.**
Not the 15 councils members' own voting records put above half: Bellcourt City Council, Elmhurst Bay City Council, Jerrick Rural City Council, Marlow Coast Shire Council, Rosedene City Council, Tallis Creek Shire Council fall below half once each member is read with the delegate in post at their worksite after the July 2026 delegate elections, and Copeland Downs Shire Council and Pellham City Council rise above it.

## 2. Critical Components

1. Members at a worksite with an elected delegate in post vote markedly more often: about **24 points** at the 2027 rolls (log odds 1.05).
2. Members' voting records alone reproduce the 2023-24 declared turnouts within about **1 point** on average, because the 2022 and 2024 delegates sat at much the same worksites.
3. Six councils that cleared half at their last ballot fall below it in 2027 (Bellcourt City Council, Elmhurst Bay City Council, Jerrick Rural City Council, Marlow Coast Shire Council, Rosedene City Council, Tallis Creek Shire Council), and two that did not now clear it (Copeland Downs Shire Council and Pellham City Council).

## 3. Step-by-Step Solution

1. Placed every member of membership_register_extract_2026-11-02.csv at their worksite, moving the codes used before July 2024 to today's through worksites_2026-11.csv.
2. Marked each member, on each online vote's close and on the extract, as at a worksite with a delegate of the term in force (delegate_register_2018-2028.xlsx) who was still a member that day.
3. Fitted a logit of voting on online_vote_invitations_2022-2025.csv: vote and council effects, age band, log years of membership, employment and the delegate mark.
4. Set the ballots' level with one shift returning every ballot the two Tallyhouse declarations report, each roll the members employed on its roll date.
5. Ran each member of the 2 November 2026 roll at the councils in bargaining_round_2027.xlsx with the 2026-28 delegates in post on the extract and averaged by council.
6. Applied the guide's rule: apply where expected turnout is at least 50 per cent.
7. Dues: one copy of each advice, the bureau's runs split by its statements, Thursday-dated platform runs moved back four days to their Sunday period end.
8. Organiser hours: travel and administration out, one row per organiser, invitation and day at its last update, each forum's hours shared by the sign-ins placed through the register.

## 4. Deliverable Answers

### pab_2027_turnout_forecast.xlsx

1. Each council's expected turnout and whether it reaches half the roll:
   - Ardeen Shire Council: about 66 per cent, reaches half
   - Bellcourt City Council: about 45 per cent, below half
   - Brackley Ranges Shire Council: about 38 per cent, below half
   - Copeland Downs Shire Council: about 57 per cent, reaches half
   - Corrigan Valley Shire Council: about 63 per cent, reaches half
   - Darnley Plains Shire Council: about 35 per cent, below half
   - Elmhurst Bay City Council: about 45 per cent, below half
   - Fairholme Shire Council: about 65 per cent, reaches half
   - Glenvale Hills Shire Council: about 41 per cent, below half
   - Halston City Council: about 60 per cent, reaches half
   - Jerrick Rural City Council: about 44 per cent, below half
   - Kelvale Shire Council: about 45 per cent, below half
   - Lindale City Council: about 62 per cent, reaches half
   - Marlow Coast Shire Council: about 43 per cent, below half
   - Northvale City Council: about 72 per cent, reaches half
   - Oakmere Shire Council: about 32 per cent, below half
   - Pellham City Council: about 58 per cent, reaches half
   - Quarrington Shire Council: about 39 per cent, below half
   - Rosedene City Council: about 46 per cent, below half
   - Stanwick Shire Council: about 61 per cent, reaches half
   - Tallis Creek Shire Council: about 45 per cent, below half
   - Underhill Rural City Council: about 41 per cent, below half
   - Valmont City Council: about 58 per cent, reaches half
   - Westhaven Shire Council: about 67 per cent, reaches half
2. Dues each council's payroll deducted for the branch, pay periods ending in 2025-26, whole dollars:
   - Ardeen Shire Council: 166,601
   - Ashby Shire Council: 155,544
   - Bellcourt City Council: 574,860
   - Brackley Ranges Shire Council: 105,135
   - Burnleigh City Council: 424,710
   - Carrow Shire Council: 110,825
   - Copeland Downs Shire Council: 240,851
   - Corrigan Valley Shire Council: 359,790
   - Darnley Plains Shire Council: 124,844
   - Denholm City Council: 328,920
   - Eastbourne Rural City Council: 139,989
   - Elmhurst Bay City Council: 505,092
   - Fairholme Shire Council: 75,422
   - Glenvale Hills Shire Council: 190,456
   - Greystone Shire Council: 217,632
   - Halston City Council: 636,735
   - Jerrick Rural City Council: 214,912
   - Kelvale Shire Council: 77,155
   - Lindale City Council: 538,832
   - Marlow Coast Shire Council: 270,358
   - Northvale City Council: 365,691
   - Oakmere Shire Council: 160,222
   - Pellham City Council: 428,717
   - Quarrington Shire Council: 116,900
   - Rosedene City Council: 339,517
   - Stanwick Shire Council: 174,757
   - Tallis Creek Shire Council: 233,411
   - Underhill Rural City Council: 94,016
   - Valmont City Council: 450,653
   - Westhaven Shire Council: 248,663
3. Organiser hours at each council in 2025-26, whole hours:
   - Ardeen Shire Council: 254
   - Ashby Shire Council: 263
   - Bellcourt City Council: 295
   - Brackley Ranges Shire Council: 277
   - Burnleigh City Council: 266
   - Carrow Shire Council: 273
   - Copeland Downs Shire Council: 266
   - Corrigan Valley Shire Council: 320
   - Darnley Plains Shire Council: 277
   - Denholm City Council: 346
   - Eastbourne Rural City Council: 281
   - Elmhurst Bay City Council: 260
   - Fairholme Shire Council: 242
   - Glenvale Hills Shire Council: 188
   - Greystone Shire Council: 241
   - Halston City Council: 247
   - Jerrick Rural City Council: 252
   - Kelvale Shire Council: 298
   - Lindale City Council: 260
   - Marlow Coast Shire Council: 284
   - Northvale City Council: 253
   - Oakmere Shire Council: 180
   - Pellham City Council: 354
   - Quarrington Shire Council: 327
   - Rosedene City Council: 274
   - Stanwick Shire Council: 249
   - Tallis Creek Shire Council: 239
   - Underhill Rural City Council: 246
   - Valmont City Council: 214
   - Westhaven Shire Council: 326

### pab_2027_recommendation_bcom.docx

1. Recommendation: apply at Ardeen Shire Council; Copeland Downs Shire Council; Corrigan Valley Shire Council; Fairholme Shire Council; Halston City Council; Lindale City Council; Northvale City Council; Pellham City Council; Stanwick Shire Council; Valmont City Council; Westhaven Shire Council; do not apply at the other 13 councils in the round.
