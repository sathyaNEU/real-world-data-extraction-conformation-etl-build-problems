Primary task type: Experiment & Causal Analysis
Domain: Marketing & Consumer Research
Deliverables: 3 of max 3 - julbrevet_2028_plan.xlsx (workbook), julbrevet_mail_call.docx (memo), julbrevet_reach_2028.png (visual); visual: julbrevet_reach_2028.png

## 1. PROMPT

```
Using the 2028 channel planning guidance in the folder, work out the incremental December purchases per piece caused by the 2027 Julbrevet addressed mailing (Brannvik Plus), with the range the data supports, and make one keep-or-drop call on addressed mail for Julbrevet 2028. Count every purchase amount the way the BI warehouse counts purchases. Deliver an Excel workbook with two sheets on the receipts from 1 to 24 December 2027 that redeemed the BV27-13-O2 card offer (50 kr off a purchase over 700 kr) with a basket under 750 SEK before the discount: Sheet 1 gives, for each store format, the number of those receipts and the purchases paid on them in thousand SEK to one decimal; Sheet 2 gives the same two figures for each of ISO weeks 48 to 51. Deliver a short Word memo that opens with the call and closes with the total number of those receipts and the total paid on them in thousand SEK to one decimal. Deliver a PNG chart of those receipts per ISO week, split by store format.
```

ZIP: mkt-01_brannvik_plus_reach_2027_input_files.zip

## 2. DISTRACTOR FILE

```
meta_ads_daily_2027.csv
```

## 3. FINAL DETERMINISTIC RECOMMENDATION

```
Drop the addressed Julbrevet mailing from the 2028 plan: it caused 137 SEK of incremental December purchases per piece with a 90 percent range of minus 57 to plus 331 SEK, and the margin on the lower end, minus 14.25 SEK per piece, falls 25.65 SEK short of the 11.40 SEK piece cost
```

## 4. SUPPLEMENTARY ANSWERS

```
julbrevet_2028_plan.xlsx, sheet 1 (BV27-13-O2 receipts of 1 to 24 December 2027 with a basket under 750 SEK before the 50 kr discount, amounts as the BI warehouse counts purchases):
1. Stor stores: 37 receipts
2. Stor stores: 25.1 thousand SEK paid on them
3. Mellan stores: 59 receipts
4. Mellan stores: 39.9 thousand SEK paid on them
5. Nära stores: 3 receipts
6. Nära stores: 2.0 thousand SEK paid on them
julbrevet_2028_plan.xlsx, sheet 2 (the same receipts by ISO week):
7. Week 48: 21 receipts
8. Week 48: 14.1 thousand SEK paid on them
9. Week 49: 28 receipts
10. Week 49: 19.0 thousand SEK paid on them
11. Week 50: 34 receipts
12. Week 50: 23.1 thousand SEK paid on them
13. Week 51: 16 receipts
14. Week 51: 10.9 thousand SEK paid on them
julbrevet_mail_call.docx:
15. Opens with the call to drop addressed Julbrevet mail from the 2028 plan.
16. Closes with the total number of those receipts: 99.
17. Closes with the total paid on them: 67.0 thousand SEK.
julbrevet_reach_2028.png:
18. Bars of the receipts in each ISO week split by store format: week 48 21 (Stor 6, Mellan 15, Nära 0); week 49 28 (Stor 13, Mellan 13, Nära 2); week 50 34 (Stor 13, Mellan 20, Nära 1); week 51 16 (Stor 5, Mellan 11, Nära 0).
```

## 5. CRITICAL COMPONENTS

```
- Recover the control: 1,942 eligible households in the three held-back postcode areas (803, 805 and 852, which have no rows in the address file), counted as would-have-been-mailed by replaying post consent on the selection date; the 138 objectors in those areas are not control.
- Compute December purchases per household over all of each household's accounts, mailed versus control, giving 2,298.58 SEK against 2,161.36 SEK and an incremental 137.21 SEK per piece (one piece per household).
- Take the 90 percent range over the postcode areas the control was assigned by (24 mailed areas against 3 held-back areas, area means weighted by households, cluster-robust t with about 4.5 degrees of freedom): minus 56.99 SEK to 331.42 SEK per piece.
- Put the lower end through the plan's line: 25 percent gross margin gives minus 14.25 SEK per piece against the 11.40 SEK piece cost, a shortfall of 25.65 SEK per piece, so the mailing is not shown to pay and is dropped; the test needed to show 239.81 SEK per piece.
```

## 6. STEP-BY-STEP SOLUTION

```
1. Read the 2028 guidance and the media plan for the rules. Eligible households are those with an account open on 15 November 2027 and January to October purchases of at least 6,000 SEK summed over all of the household's accounts (17,200 households); incremental purchases are December purchases per household over all accounts less what the same households would have bought without the mailing; the control was three postcode areas drawn by lot and held back from printing; the mailing must show a lower 90 percent end whose 25 percent margin covers the 11.40 SEK per-piece cost, so break-even is 45.60 SEK of purchases per piece.
2. Identify the mailed households from the Julbrevet rows of the address file: 14,108 households in 24 postcode areas, all of them eligible. The campaign report's basket sheet (mailed 2,298.58 SEK against 817.77 SEK for everyone not mailed) is a descriptive pair and is not the test, because the unmailed include non-eligible households.
3. Recover the control, which is listed in no file. The address file and the calendar note show postcode areas 803, 805 and 852 have no Julbrevet rows; the 2,080 eligible households there are the would-have-been-mailed set. Replay the consent snapshot and log to the selection date (2027-11-14 23:00 UTC, midnight Swedish time) on each household's main card holder, the earliest-joined open account; 138 had objected and are removed, leaving 1,942 control households. Objectors across all areas number 1,150. [supplementary: group counts, control households]
4. Build the December purchase outcome per household from the member, store and month table, summed over every account in the household, with zero where there is none. Group means: mailed 2,298.58 SEK, control 2,161.36 SEK, objected 2,102.15 SEK. [supplementary: group rows]
5. Take the incremental purchases as the mailed-minus-control December difference: 137.21 SEK per household, the same per piece because one piece goes to each mailed household. [supplementary: incremental]
6. Put the interval where the assignment was made. The control was drawn by postcode area, so the households within an area are not independent observations; take each area's mean household December purchases, weight by households, and use a cluster-robust t interval with the 27 areas (24 mailed, 3 held back; about 4.5 degrees of freedom). The 90 percent range is minus 56.99 to plus 331.42 SEK per piece. A household-level interval on the same contrast gives 58.00 to 216.43 and wrongly clears the line. [supplementary: range]
7. Apply the line. At 25 percent gross margin the lower end is worth minus 14.25 SEK per piece against the 11.40 SEK piece cost, which it does not cover; the mailing is not shown to pay, so the call is to drop addressed Julbrevet mail from the 2028 plan. [supplementary: margin per piece]
8. Measure the miss and the needed lift. The margin falls short of the piece cost by 11.40 minus (minus 14.25), which is 25.65 SEK per piece. The test would have needed to show 45.60 plus the t critical value 2.0615 times the standard error 94.21, which is 239.81 SEK of incremental purchases per piece, for the lower end to cover the cost. [supplementary: shortfall and needed lift]
9. Workbook. Take every BV27-13-O2 redemption in the POS export (all dated 1 to 24 December, each 50 SEK off), the format of its store from stores.csv and the ISO week of redeemed_at, with amounts counted as the BI warehouse counts purchases (spend_sek, after offer discounts). 1,415 of the 2,841 O2 redemptions are written under BV27-13-O1: they are the O1 rows giving exactly 50 SEK off a basket over 700 SEK, the O2 terms, and each of the 219 accounts with two O1 rows, which the till's once-for-each-member rule (runbook 7.3) rules out, has one of them, while no other account redeems any offer twice. At BV101, BV104, BV106, BV110, BV113, BV114, BV115, BV118, BV119, BV128, BV129, BV132, BV138 and BV141 the POS receipt total is the amount before the discount: on every member, store and month whose receipts all redeemed an offer it exceeds spend_sek by exactly the discount (1,315 of 1,315 such months in December), while every other store's total equals spend_sek (671 of 671 in December). With both handled, the receipts with a basket under 750 SEK before the discount are Stor 37, Mellan 59, Nära 3 (25.1, 39.9, 2.0 thousand SEK paid) and weeks 48 to 51 21, 28, 34, 16 (14.1, 19.0, 23.1, 10.9 thousand SEK). [supplementary: both sheets, memo, chart]
10. Deliver the workbook with the two sheets, the short Word memo opening with the call and closing with 99 receipts and 67.0 thousand SEK, and the PNG of the receipts per ISO week split by store format.
```

## 7. GOLDEN DELIVERABLES

GOLDEN FILES (in mkt-01_brannvik_plus_reach_2027_golden_deliverables.zip): julbrevet_2028_plan.xlsx, julbrevet_mail_call.docx, julbrevet_reach_2028.png
(never inside the input ZIP)
