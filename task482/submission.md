## Tags

**Domain:** Education & Learning Sciences, item response theory and test equating (an education technology company's partner district contracts, its platform's eligibility and roster records, the assessment delivery system's sessions and scored responses, the contractor's item parameters and plausible values, the professional learning scheduling export and the billing register conformed into the 2025-26 guarantee settlement and the billing system's credit memo import).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**16 of the 58 partner districts are owed the outcomes guarantee credit under their 2025-26 order forms, USD 25,493.75 in total: Alrowvale Elementary School District (LD-1182); Havleymoor Unified School District (LD-1047); Kelnorfield Elementary School District (LD-1153); Torsenford Unified School District (LD-1059); Merleywick School District 9 (LD-1026); Keltervale County School District (LD-1148); Saldledale County School District (LD-1179); Salnormere County School District (LD-1164); Belberbury City Schools (LD-1116); Torlanvale City Schools (LD-1181); Dardlestead Local School District (LD-1018); Havwinmont City School District (LD-1089); Balterdale Special School District (LD-1017); Dunrenmont City Schools (LD-1053); Fenlenbury City Schools (LD-1184); Merganwick Special School District (LD-1062).**
Each district's Outcome Share is estimated from its eligible students' own answers on the two modules they took, with the district in the population model. The contractor's plausible values were drawn for the national report from a model on grade, state, prior band and background with no district term, so they pull every district toward what its students' backgrounds predict: averaged by district they credit districts that met their benchmark and clear districts that did not.

## 2. Critical Components

1. Districts owed the outcomes credit: **16** of 58.
2. Outcomes credits: **USD 25,493.75** in total.
3. Professional learning shortfall credits: **USD 11,250.00** across **20** districts; all credits **USD 36,743.75**.

## 3. Step-by-Step Solution

1. Took each district's eligible students from guarantee_eligibility_2025_26.csv (the 1 May 2026 record flagged eligible) and linked them through student_id_crosswalk_2025_26.csv to their submitted session in lsoa_spring2026_sessions.csv: 26,497 eligible students assessed.
2. Scored each submitted session's responses (omitted items incorrect, items not reached left out) on the 2024 item parameters, two-parameter logistic with D = 1.
3. Fitted a latent regression of achievement on district, grade, prior state-test band (Table 5 of the technical report, read from the roster uploads) and the three status flags by EM on a grid, and took each district's Outcome Share as the mean posterior probability of its eligible assessed students being at or above 500, 520 or 540 for their grade.
4. Compared each share with the district's Guarantee Benchmark in order_forms_2025_26.xlsx; a district below it is credited its Credit Percentage of the 2025-26 Subscription Fee.
5. Summed each district's live sessions (virtual live and on site) in pd_sessions_2025_26.csv with status Delivered and a date in its subscription term, each session's hours read as hours and minutes after the point (the scheduling system's way of writing a session's time), joint sessions in full for every district attending, to the nearest half hour; any shortfall against the order form's hours is credited at USD 250 an hour under the agreement's professional learning clause.
6. Applied each credit to the open 2026-27 subscription invoice on the order form's bill-to account with the earliest due date in billing_invoices_2026_27.csv, or a refund by check where none is open, in the layout of credit_memo_import_layout.pdf.

## 4. Deliverable Answers

### lumenfold_guarantee_settlement_2025_26.xlsx

1. Outcomes guarantee: not met, and credited, at the 16 districts in the Final Recommendation; met at the other 42.
2. Live professional learning hours delivered in the subscription term, to the half hour, against the order form's hours:
   - Alrowvale Elementary School District (LD-1182): 8.5 of 9
   - Calleyfield Unified School District (LD-1055): 10 of 9
   - Darmerford Elementary School District (LD-1107): 5.5 of 6
   - Delmanwick Unified School District (LD-1033): 12 of 9
   - Havleymoor Unified School District (LD-1047): 10 of 9
   - Kelnorfield Elementary School District (LD-1153): 17.5 of 12
   - Malvermoor Unified School District (LD-1161): 15.5 of 18
   - Torsenford Unified School District (LD-1059): 23.5 of 18
   - Corrowbury School District 10 (LD-1036): 10 of 9
   - Dundlewood School District 2 (LD-1173): 19.5 of 15
   - Falrickwood School District 9 (LD-1028): 24.5 of 18
   - Garterfield School District RE-2 (LD-1157): 22 of 24
   - Haltinmont School District RE-1 (LD-1172): 8.5 of 6
   - Lorleyford School District 8 (LD-1109): 8.5 of 12
   - Malwinmont School District 1 (LD-1093): 13 of 12
   - Merleywick School District 9 (LD-1026): 8 of 12
   - Valdlewick School District 1 (LD-1091): 10 of 9
   - Balrickwood City Schools (LD-1043): 10.5 of 12
   - Corlengate City Schools (LD-1170): 10.5 of 12
   - Keltervale County School District (LD-1148): 7 of 6
   - Merberstead County School District (LD-1052): 22.5 of 18
   - Pellenwick County School District (LD-1045): 20.5 of 24
   - Pelrickbury County School District (LD-1166): 7 of 6
   - Saldledale County School District (LD-1179): 12 of 9
   - Salnormere County School District (LD-1164): 10.5 of 12
   - Talsenford County School District (LD-1155): 25.5 of 24
   - Alrickvale County Schools (LD-1183): 22.5 of 24
   - Belberbury City Schools (LD-1116): 15 of 15
   - Belwinwell City Schools (LD-1114): 18.5 of 18
   - Bransenwell County Schools (LD-1083): 26 of 24
   - Delrickmoor County Schools (LD-1139): 18 of 18
   - Dunganmere City Schools (LD-1076): 12.5 of 12
   - Fenwinmoor County Schools (LD-1130): 18 of 18
   - Lanmerwell City Schools (LD-1057): 25.5 of 24
   - Lorlenstead City Schools (LD-1056): 14 of 15
   - Malrowwell City Schools (LD-1151): 7.5 of 12
   - Torlanvale City Schools (LD-1181): 10 of 12
   - Valsenstead City Schools (LD-1112): 19 of 15
   - Branleymoor Local School District (LD-1016): 19 of 12
   - Calnormere City School District (LD-1039): 12 of 12
   - Corlinbury Local School District (LD-1127): 14 of 15
   - Dardlestead Local School District (LD-1018): 11.5 of 9
   - Delrowfield Local School District (LD-1136): 21 of 24
   - Faldlewood City School District (LD-1138): 17 of 12
   - Fenrickgate Local School District (LD-1025): 9.5 of 9
   - Havdenstead Local School District (LD-1073): 14 of 18
   - Havwinmont City School District (LD-1089): 16.5 of 18
   - Marrickmere Exempted Village School District (LD-1081): 7 of 6
   - Saltinmere City School District (LD-1110): 16 of 9
   - Alrickwood County Schools (LD-1040): 22.5 of 15
   - Balterdale Special School District (LD-1017): 13.5 of 12
   - Branlinvale City Schools (LD-1137): 24.5 of 15
   - Dunrenmont City Schools (LD-1053): 6.5 of 6
   - Fenlenbury City Schools (LD-1184): 21.5 of 18
   - Lorleywell City Schools (LD-1069): 20 of 18
   - Merganwick Special School District (LD-1062): 14 of 15
   - Peldleford City Schools (LD-1178): 14.5 of 12
   - Tortinfield Special School District (LD-1141): 7.5 of 12
3. Professional learning shortfall credit, USD to the cent (every other district nil):
   - Alrowvale Elementary School District (LD-1182): USD 125.00
   - Darmerford Elementary School District (LD-1107): USD 125.00
   - Malvermoor Unified School District (LD-1161): USD 625.00
   - Garterfield School District RE-2 (LD-1157): USD 500.00
   - Lorleyford School District 8 (LD-1109): USD 875.00
   - Merleywick School District 9 (LD-1026): USD 1,000.00
   - Balrickwood City Schools (LD-1043): USD 375.00
   - Corlengate City Schools (LD-1170): USD 375.00
   - Pellenwick County School District (LD-1045): USD 875.00
   - Salnormere County School District (LD-1164): USD 375.00
   - Alrickvale County Schools (LD-1183): USD 375.00
   - Lorlenstead City Schools (LD-1056): USD 250.00
   - Malrowwell City Schools (LD-1151): USD 1,125.00
   - Torlanvale City Schools (LD-1181): USD 500.00
   - Corlinbury Local School District (LD-1127): USD 250.00
   - Delrowfield Local School District (LD-1136): USD 750.00
   - Havdenstead Local School District (LD-1073): USD 1,000.00
   - Havwinmont City School District (LD-1089): USD 375.00
   - Merganwick Special School District (LD-1062): USD 250.00
   - Tortinfield Special School District (LD-1141): USD 1,125.00

### guarantee_credit_memos_2026.csv

4. 36 credit memos dated 2026-11-30 (memo reference, customer account, reason, amount, applied to):
   - OG-2526-1017, C-204814, OG, 787.50, CHECK
   - OG-2526-1018, C-204310, OG, 1530.00, CHECK
   - OG-2526-1026, C-205976, OG, 3225.00, INV-261702
   - OG-2526-1047, C-204898, OG, 2100.00, CHECK
   - OG-2526-1053, C-204667, OG, 1706.25, CHECK
   - OG-2526-1059, C-205640, OG, 810.00, CHECK
   - OG-2526-1062, C-204905, OG, 2040.00, INV-261680
   - OG-2526-1089, C-205108, OG, 1360.00, INV-261645
   - OG-2526-1116, C-204541, OG, 832.50, CHECK
   - OG-2526-1148, C-204821, OG, 860.00, INV-262428
   - OG-2526-1153, C-204632, OG, 1890.00, INV-262295
   - OG-2526-1164, C-205248, OG, 967.50, CHECK
   - OG-2526-1179, C-205122, OG, 3225.00, CHECK
   - OG-2526-1181, C-205577, OG, 945.00, INV-261491
   - OG-2526-1182, C-206375, OG, 1640.00, INV-262411
   - OG-2526-1184, C-205598, OG, 1575.00, INV-262340
   - PL-2526-1026, C-205976, PL, 1000.00, INV-261702
   - PL-2526-1043, C-204184, PL, 375.00, INV-262013
   - PL-2526-1045, C-205479, PL, 875.00, INV-261167
   - PL-2526-1056, C-205220, PL, 250.00, CHECK
   - PL-2526-1062, C-204905, PL, 250.00, INV-261680
   - PL-2526-1073, C-205626, PL, 1000.00, INV-261830
   - PL-2526-1089, C-205108, PL, 375.00, INV-261645
   - PL-2526-1107, C-206067, PL, 125.00, CHECK
   - PL-2526-1109, C-204646, PL, 875.00, INV-261203
   - PL-2526-1127, C-204254, PL, 250.00, INV-262226
   - PL-2526-1136, C-204758, PL, 750.00, INV-262145
   - PL-2526-1141, C-204128, PL, 1125.00, CHECK
   - PL-2526-1151, C-205955, PL, 1125.00, CHECK
   - PL-2526-1157, C-204520, PL, 500.00, INV-261475
   - PL-2526-1161, C-204282, PL, 625.00, CHECK
   - PL-2526-1164, C-205248, PL, 375.00, CHECK
   - PL-2526-1170, C-206102, PL, 375.00, CHECK
   - PL-2526-1181, C-205577, PL, 500.00, INV-261491
   - PL-2526-1182, C-206375, PL, 125.00, INV-262411
   - PL-2526-1183, C-204695, PL, 375.00, INV-261922
