# task458 submission

## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health-plan analytics (claims-based case identification against enrollment: each county's members with a serious mental illness and with an opioid use disorder estimated from the members a claim identifies, each weighted for the months it was enrolled, for need-based prescriber standards over a contract year).
**Analytical objective:** Data Extraction & Conformation (ETL) (the NPPES monthly file updated by its weekly files, the claims system's claim versions and the enrollment system's spans conformed to one row per county and eligibility group).

## 1. Final Recommendation

**The board should designate Adams, Douglas, Franklin, Grant and Okanogan for the 2027 Prescriber Service Award Pilot.**

Each fails at least two NP-31 standards once every member a claim identifies is counted for the months it was enrolled: Franklin has 14.1 and Grant 12.7 practising prescribers per 1,000 adult members with a serious mental illness against 16.5, and 20.4 and 19.6 per 1,000 with an opioid use disorder against 23.0. Not Yakima: carrying its full-year members' prevalence to all its members, eligibility group by group, counts 2,660 with a serious mental illness, 15.4 prescribers per 1,000 and a 64 per cent reach, but its members in short seasonal spells have the conditions far less often (2.1 per cent of expansion adults enrolled three months are identified with a serious mental illness, against 4.1 per cent of the full-year expansion adults within their first three months); counted for the months each member was enrolled it has 2,320, 17.7 per 1,000 and 73 per cent. Not the count of members a claim identifies, which designates only Adams, Douglas and Okanogan: NP-31 counts every member who has the condition.

## 2. Critical Components

1. NP-31 counts **4** practising behavioral-health prescribers in Adams, **3** in Douglas, **10** in Franklin, **10** in Grant and **4** in Okanogan on 1 November 2026 (**41** in Yakima).
2. Adult members with a serious mental illness: Adams **320**, Douglas **340**, Franklin **710**, Grant **790**, Okanogan **490** (Yakima **2,320**); with an opioid use disorder: **230**, **200**, **490**, **510**, **300** (Yakima **1,580**).
3. Adams, Douglas and Okanogan fail all three standards and Franklin and Grant both prescriber ratios; every other county meets all three, Yakima at **17.7** and **25.9** per 1,000 and a **73 per cent** reach.

## 3. Step-by-Step Solution

1. Updated npidata_pfile_wa_20050523-20261011.csv record by record with the three weekly files to 1 November 2026 and took NP-31 2.6 and 2.7's practising prescribers (primary taxonomy in Appendix B, NPI active on 1 November, practice ZIP code to the county with the larger BUS_RATIO in ZIP_COUNTY_062026.xlsx, rendering provider of a final claim or encounter): 131 in the ten counties.
2. Joined enrollment_spans_2025-07-01_2026-06-30.csv into 123,460 adult members by client_id, each in the county and eligibility group of the span covering the last enrolled day (2.2, 2.3), with the months enrolled; 70,377 were enrolled all twelve months.
3. Kept the final version of each claim in bh_claims_encounters_dos_2025-07-01_2026-06-30.csv (frequency 7 in place of the claim it replaces, frequency 8 and the claim it voids removed) and identified conditions by the Appendix A codes in any position (2.4), with the month of each member's first identifying service: 7,109 members with a serious mental illness, 4,421 with an opioid use disorder.
4. A condition shows only in services billed while a member is enrolled: of the members enrolled all year with a serious mental illness, 30.5 per cent are first identified in July 2025 and 66.7 per cent within three months. Members in short seasonal spells fall well short of that share (2.1 per cent of expansion adults enrolled three months against 4.1 per cent of the full-year expansion adults within their first three months), while those enrolled seven to eleven months are identified as often as the full-year members are within the same months, so the seasonal members have the conditions less often and the full-year prevalence is not carried to them.
5. Counted each identified member as 1 over the share of the full-year members with the condition identified within the same number of months as the member was enrolled (2.5 counts every member who has the condition), summed by county; counted the members with a serious mental illness who had an Appendix C service from a behavioral-health prescriber anywhere (2.8; every one is among the identified) and computed the three standards against 16.5, 23.0 and 68 per cent (3.1, 3.2).
6. Designated the counties failing two or more (4.1): Adams, Douglas, Franklin, Grant and Okanogan.
7. For the payments, took the final fee-for-service claims with a behavioral-health prescriber as rendering provider and each claim's paid_amt once (it repeats on every line of the claim and equals the sum of its lines' lesser of billed_amt and the allowable in bh_professional_fee_schedule_fy2026.csv), by the member's county and the quarter of the service date.
8. Recommendation: designate Adams, Douglas, Franklin, Grant and Okanogan.

## 4. Deliverable Answers

### prescriber_pilot_county_scorecard_2027.xlsx

1. Designated counties: Adams, Douglas, Franklin, Grant and Okanogan.
2. Each county's practising prescribers, adult members with a serious mental illness and with an opioid use disorder (nearest 10), and standing on the three standards:
   - Adams: 4 prescribers; 320 with a serious mental illness, 230 with an opioid use disorder; fails all three standards (12.5 and 17.4 per 1,000, 60 per cent reach); designated
   - Benton: 30 prescribers; 1,220 with a serious mental illness, 740 with an opioid use disorder; meets all three standards (24.6 and 40.5 per 1,000, 94 per cent reach); not designated
   - Chelan: 12 prescribers; 510 with a serious mental illness, 330 with an opioid use disorder; meets all three standards (23.6 and 36.5 per 1,000, 90 per cent reach); not designated
   - Douglas: 3 prescribers; 340 with a serious mental illness, 200 with an opioid use disorder; fails all three standards (8.8 and 14.9 per 1,000, 58 per cent reach); designated
   - Franklin: 10 prescribers; 710 with a serious mental illness, 490 with an opioid use disorder; fails both prescriber ratios, meets the reach (14.1 and 20.4 per 1,000, 74 per cent reach); designated
   - Grant: 10 prescribers; 790 with a serious mental illness, 510 with an opioid use disorder; fails both prescriber ratios, meets the reach (12.7 and 19.6 per 1,000, 75 per cent reach); designated
   - Kittitas: 7 prescribers; 290 with a serious mental illness, 140 with an opioid use disorder; meets all three standards (24.2 and 50.0 per 1,000, 91 per cent reach); not designated
   - Okanogan: 4 prescribers; 490 with a serious mental illness, 300 with an opioid use disorder; fails all three standards (8.2 and 13.3 per 1,000, 59 per cent reach); designated
   - Walla Walla: 10 prescribers; 560 with a serious mental illness, 350 with an opioid use disorder; meets all three standards (17.9 and 28.5 per 1,000, 74 per cent reach); not designated
   - Yakima: 41 prescribers; 2,320 with a serious mental illness, 1,580 with an opioid use disorder; meets all three standards (17.7 and 25.9 per 1,000, 73 per cent reach); not designated
3. Net fee-for-service payments for services behavioral-health prescribers rendered to each county's adult members, whole dollars, July to September 2025, October to December 2025, January to March 2026, April to June 2026:
   - Adams: $5,821, $5,345, $6,927, $5,549
   - Benton: $119,419, $118,586, $121,273, $112,600
   - Chelan: $62,795, $62,957, $65,288, $56,395
   - Douglas: $19,718, $25,262, $28,590, $21,141
   - Franklin: $66,817, $69,652, $74,333, $63,632
   - Grant: $47,310, $48,047, $50,514, $53,015
   - Kittitas: $10,719, $11,745, $12,989, $8,363
   - Okanogan: $28,660, $27,203, $25,646, $23,558
   - Walla Walla: $38,512, $35,014, $38,246, $35,999
   - Yakima: $164,868, $167,226, $165,363, $155,839

### county_adult_members_2026_conformed.csv

1. Adult members and net fee-for-service payments for behavioral-health prescribers' services (whole dollars), by county and eligibility group:
   - Adams, expansion adults: 4,142 members, $13,916
   - Adams, adults 65 and over: 280 members, $1,459
   - Adams, parents and caretaker relatives: 1,365 members, $3,071
   - Adams, disabled adults: 433 members, $5,196
   - Benton, expansion adults: 9,964 members, $250,651
   - Benton, adults 65 and over: 1,293 members, $23,219
   - Benton, parents and caretaker relatives: 4,171 members, $71,966
   - Benton, disabled adults: 2,477 members, $126,041
   - Chelan, expansion adults: 4,593 members, $129,327
   - Chelan, adults 65 and over: 602 members, $12,805
   - Chelan, parents and caretaker relatives: 1,901 members, $43,319
   - Chelan, disabled adults: 1,015 members, $61,983
   - Douglas, expansion adults: 2,731 members, $54,289
   - Douglas, adults 65 and over: 321 members, $4,384
   - Douglas, parents and caretaker relatives: 1,158 members, $18,618
   - Douglas, disabled adults: 644 members, $17,421
   - Franklin, expansion adults: 9,213 members, $147,975
   - Franklin, adults 65 and over: 605 members, $16,529
   - Franklin, parents and caretaker relatives: 3,618 members, $47,824
   - Franklin, disabled adults: 1,115 members, $62,105
   - Grant, expansion adults: 9,616 members, $103,286
   - Grant, adults 65 and over: 800 members, $17,242
   - Grant, parents and caretaker relatives: 3,510 members, $27,777
   - Grant, disabled adults: 1,302 members, $50,580
   - Kittitas, expansion adults: 2,441 members, $23,323
   - Kittitas, adults 65 and over: 310 members, $1,606
   - Kittitas, parents and caretaker relatives: 809 members, $6,151
   - Kittitas, disabled adults: 618 members, $12,736
   - Okanogan, expansion adults: 3,623 members, $61,516
   - Okanogan, adults 65 and over: 502 members, $5,228
   - Okanogan, parents and caretaker relatives: 1,405 members, $15,655
   - Okanogan, disabled adults: 900 members, $22,667
   - Walla Walla, expansion adults: 5,208 members, $97,061
   - Walla Walla, adults 65 and over: 301 members, $6,022
   - Walla Walla, parents and caretaker relatives: 1,505 members, $22,848
   - Walla Walla, disabled adults: 633 members, $21,840
   - Yakima, expansion adults: 21,869 members, $306,265
   - Yakima, adults 65 and over: 2,566 members, $40,772
   - Yakima, parents and caretaker relatives: 8,758 members, $102,027
   - Yakima, disabled adults: 5,143 members, $204,231
