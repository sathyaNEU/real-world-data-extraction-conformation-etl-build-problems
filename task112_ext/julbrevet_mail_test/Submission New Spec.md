Primary task type: Experiment & Causal Analysis
Domain: Marketing & Consumer Research
Deliverables: 3 of max 3 - julbrevet_2028_plan.xlsx (workbook), julbrevet_mail_call.docx (memo), julbrevet_reach_2028.png (visual); visual: julbrevet_reach_2028.png

## 1. PROMPT

```
Brannvik Plus, the loyalty programme of the Brannvik grocery chain, is setting its 2028 channel plan, and the open question is whether the addressed Julbrevet mailing stays in it. Julbrevet is the December campaign. The 2028 channel planning guidance in the folder sets out how a mailing's incremental purchases are measured for this decision and where the line sits. The number I need is the incremental December purchases per piece that the 2027 mailing caused, with the range the data supports, and from it one keep-or-drop call on addressed mail for Julbrevet 2028.

The campaign team needs an Excel workbook for the 2028 plan. One sheet should give, for each of the two Julbrevet card offers and each format of the store where the receipt was rung, the purchases paid on the receipts that redeemed the offer from 1 to 24 December 2027, on the BI warehouse's basis, in thousand SEK to one decimal. A second sheet should take the households mailed the Julbrevet in 2027 and, for each county, give how many of them could still be sent the 2028 Julbrevet by email, how many by SMS or app push but not by email, and how many by none of the three, each group with the purchases paid, on the same basis, on the receipts on which any card registered to its households redeemed a Julbrevet card offer, in thousand SEK to one decimal. A household counts for a channel when at least one of its accounts open at the end of 2027 held consent for that channel at that point and is one the channel's platform would still send to.

The campaign team also needs a short memo in Word. It should open with the call, the December purchases per household of the mailed and control households, the incremental purchases per piece with its range, and the margin per piece on the lower end against the 11.40 SEK piece cost. Next, it should say by how much the mailing missed or cleared the line per piece, what the test would have needed to show for it to pay, and how many control households the test rested on. It should close with how many of the mailed households none of the three channels could still send the 2028 Julbrevet to, and what those households paid on their Julbrevet card offer receipts on that basis, in thousand SEK to one decimal.

I also need a PNG chart for the planning meeting showing, for each county, the mailed households in each of the three groups. The rest of the design is up to you.
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
julbrevet_2028_plan.xlsx, sheet of the Julbrevet card offers (purchases paid on the receipts that redeemed the offer, 1 to 24 December 2027, thousand SEK):
1. BV27-13-O1 Julskinka 25 % billigare, Stor stores: 378.5
2. BV27-13-O1, Mellan stores: 621.7
3. BV27-13-O1, Nära stores: 28.6
4. BV27-13-O2 50 kr rabatt vid köp över 700 kr, Stor stores: 851.6
5. BV27-13-O2, Mellan stores: 1,514.6
6. BV27-13-O2, Nära stores: 60.3
julbrevet_2028_plan.xlsx, sheet of the households mailed the Julbrevet in 2027 by county and by the channels that could still send them the 2028 Julbrevet:
7. Gävleborg, by email: 3,913 households
8. Gävleborg, by email: 743.2 thousand SEK paid on the receipts on which a card registered to those households redeemed a Julbrevet card offer
9. Gävleborg, by SMS or app push but not by email: 1,798 households
10. Gävleborg, by SMS or app push but not by email: 283.4 thousand SEK paid on the receipts on which a card registered to those households redeemed a Julbrevet card offer
11. Gävleborg, by none of the three: 1,545 households
12. Gävleborg, by none of the three: 184.2 thousand SEK paid on the receipts on which a card registered to those households redeemed a Julbrevet card offer
13. Västernorrland, by email: 3,719 households
14. Västernorrland, by email: 665.5 thousand SEK paid on the receipts on which a card registered to those households redeemed a Julbrevet card offer
15. Västernorrland, by SMS or app push but not by email: 1,678 households
16. Västernorrland, by SMS or app push but not by email: 245.6 thousand SEK paid on the receipts on which a card registered to those households redeemed a Julbrevet card offer
17. Västernorrland, by none of the three: 1,455 households
18. Västernorrland, by none of the three: 160.2 thousand SEK paid on the receipts on which a card registered to those households redeemed a Julbrevet card offer
julbrevet_mail_call.docx:
19. Opens with the call to drop addressed Julbrevet mail from the 2028 plan, with December purchases per household of 2,298.58 SEK mailed against 2,161.36 SEK control, 137.21 SEK of incremental purchases per piece with a 90 percent range of minus 56.99 to 331.42 SEK, and a lower-end margin of minus 14.25 SEK per piece against the 11.40 SEK piece cost; then a miss of 25.65 SEK per piece, 239.81 SEK per piece the test would have needed to show, and 1,942 control households.
20. Mailed households none of the three channels could still send the 2028 Julbrevet to: 3,000.
21. What those households paid on their Julbrevet card offer receipts: 344.4 thousand SEK.
julbrevet_reach_2028.png:
22. Bars of the mailed households for each county in the three groups: Gävleborg 3,913 by email, 1,798 by SMS or app push only, 1,545 by none; Västernorrland 3,719, 1,678 and 1,455.
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
9. Card offers. Take the BV27-13-O1 and BV27-13-O2 receipts of the POS export (all dated 1 to 24 December) and the format of the store where each was rung from stores.csv, on the BI warehouse's basis the prompt sets (spend_sek, the amount paid after offer discounts, the table the guidance takes purchases from). The POS receipt totals equal that basis at every store except BV113, BV115, BV118, BV125, BV128, BV132 and BV141, whose totals from late October 2027 on exceed it by exactly the discount on every member, store and month whose receipts all redeemed an offer (643 of 643 in December). The discount is taken off there, giving O1 378.5, 621.7 and 28.6 and O2 851.6, 1,514.6 and 60.3 thousand SEK paid for Stor, Mellan and Nära. [supplementary: card offers]
10. Reach. Take the 14,108 BV27-13-D1 households by the county of their postcode area (postcode_areas.csv) and replay each channel's consent to 1 January 2028 00:00 Swedish time (31 December 23:00 UTC) on the accounts open at the end of 2027. Email leaves out the addresses on the email platform's suppression list, which keeps every address that ever hard-bounced (contact policy, section 7): the 238 members who hard-bounced in 2027, and the 252 whose addresses bounced before 2027, seen as the members who held email consent at one or more 2027 newsletter releases yet were sent no 2027 email (at every one of the 26 newsletters the consented open members not sent are exactly the earlier 2027 hard bounces and these members). The 11 members whose consent came after the last 2027 mailing stay in. SMS takes every consented account. App push needs a sign-in to the app and leaves out the 677 members whose last three notifications failed, whose tokens the January clean-up removes (runbook 5.2). Households by email, by SMS or app push only, and by none: Gävleborg 3,913, 1,798 and 1,545; Västernorrland 3,719, 1,678 and 1,455. [supplementary: households by group, chart]
11. Purchases by group. Sum the amounts paid from step 9 on the Julbrevet offer receipts of every account registered to each group's households: Gävleborg 743.2, 283.4 and 184.2; Västernorrland 665.5, 245.6 and 160.2 thousand SEK. The 3,000 households none of the three channels could send to paid 344.4 thousand SEK. [supplementary: purchases by group, memo close]
12. Deliver the three files: the workbook with the card offers sheet and the reach sheet, the short Word memo opening with the call and its figures and closing with the households no channel could send to and what they paid on Julbrevet offer receipts, and the PNG of the mailed households by county and group.
```

## 7. GOLDEN DELIVERABLES

GOLDEN FILES (in mkt-01_brannvik_plus_reach_2027_golden_deliverables.zip): julbrevet_2028_plan.xlsx, julbrevet_mail_call.docx, julbrevet_reach_2028.png
(never inside the input ZIP)
