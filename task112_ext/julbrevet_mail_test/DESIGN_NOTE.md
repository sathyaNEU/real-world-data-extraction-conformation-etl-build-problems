# Brannvik Plus Julbrevet mail test (built on task112_ext): rubric repair

The task was uploaded as a finished package (b43ae590-v1): Experiment & Causal Analysis in Marketing & Consumer
Research, the call to drop addressed Julbrevet mail because the lower end of the area-clustered 90 percent range,
minus 56.99 SEK per piece, is worth minus 14.25 SEK at 25 percent margin against the 11.40 SEK piece cost. The
portal passed the call, the stump and the determinism block and returned a rubric score of 62 per cent. This
repair re-sites the supplemental asks only.

## Frozen

The prompt is the author's one-paragraph rephrase with the call question first and no backstory. The Final
Recommendation, the Critical Components, steps 1 to 8 and the distractor are carried over byte for byte
(`generator/spec.py` asserts it). Every input file the call reads is byte-identical to v1: only
`pos_offer_redemptions_2027.csv` moved, and only in `receipt_total_sek` (`generator/checks.py`). The call
recomputes unchanged on the v2 inputs: 14,108 mailed at 2,298.58, 1,942 control at 2,161.36, 1,150 objected at
2,102.15, incremental 137.21, standard error 94.21 on 4.54 degrees of freedom, range minus 56.99 to 331.42, margin
minus 14.25, shortfall 25.65, needed 239.81.

## Where the 62 came from

All nine v1 supplementary answers were the call's own construction (group rows, incremental, range, margin,
shortfall, needed lift, control count), so a response that landed the call banked every ask, and a response on the
household-level interval still banked the group rows and the incremental. No ask carried a device.

## Ask sheet

Three asks on rows the call never reads, each with its own silent primary, plus a cross ask that needs both.

| Ask | Figures | Primary (family) | Rows | Easy route and what it files |
|---|---|---|---|---|
| A card offers by format | 6 | the tills upgraded 26 October to 16 November 2027 (BV113, BV115, BV118, BV125, BV128, BV132, BV141, every format) send the loyalty engine the total before the discount (D3, per-source convention) | 1,890 Julbrevet offer receipts in the POS export | the column read as the amount paid, as the dictionary describes it: every cell high (O1 Stor 394.7 for 378.5); the discount taken off everywhere: every cell low (351.7) |
| B 2028 reach of the mailed households | 6 | the email platform's suppression list carries addresses that bounced before 2027: 252 members held email consent at a median of 26 newsletter releases and were sent no 2027 email (D4, absence as the signal, evidenced only in the send log) | email sends; the call reads no email row | 2027 hard bounces taken as the whole list: every cell moves (Gävleborg by email 3,960 for 3,913) |
| C offer purchases of each reach group | 6 + memo 2 | both of the above | POS and email sends | one device cracked keeps none of the six |

Hazards, each seen and each moving several asks: the January push token clean-up (677 members, moves B and C off
the email rows), 2027 hard bounces (238), the consent cut at 1 January 2028 00:00 Swedish time, accounts open at
the end of 2027, the 11 members whose email consent came after the last 2027 mailing (a crude "never sent" rule
drops them and moves eight cells), the O2 receipts under 700 SEK that a reader of "köp över 700 kr" drops as
invalid (moves the three O2 cells), and the household roll-up over every registered card (11 receipts by accounts
closed in December move five C cells if dropped).

Evidence a grader verifies: on every member, store and month whose receipts all redeemed an offer, the upgraded
stores' totals exceed `spend_sek` by exactly the discount (765 months) and every other store's totals equal it
(10,471 months); every O2 receipt is over 700 SEK before the discount. At every one of the 26 newsletter releases
the consented open members who were not sent are exactly the earlier 2027 hard bounces plus 240 to 250 of these
members, and no one else. Steps 9 to 11 name both handlings.

Pair on paper (a fifth of the ask weight each is the target): with each primary cracked independently at about one
in four by a strong reader, the call-lander keeps about 0.19 of the device figures and the best miss the same; the
memo's call line is the one free ask item. One primary cracked keeps a third, both (about one in sixteen) keep all.

## Measured

Pack 6e530ddeb010 (input zip sha256 prefix; the pack never changed after it was cut). Two cold readers at medium
effort, each holding only the prompt and the 23 inputs, the second on the prompt with the BI-basis pin:

- Both landed the drop call on their own area-level interval (weighted least squares on the 27 area means, 25 degrees
  of freedom, minus 94.78 to 369.21), so their range, margin, shortfall and needed-lift figures differ from the
  golden's 4.54-degree interval.
- Both kept 0 of 20 ask figures, on the same easy routes: the till totals summed as the amount paid (O1 Stor 394.7 for
  378.5; the second reader matched the POS export to the BI table on offers and discounts in every cell, found it
  tied, and took the totals as the BI basis) and only the 2027 hard bounces taken off email (Gävleborg 3,960 for
  3,913). The offer purchases by group missed on both.
- Neither quoted a sentence for the decisive step or named a file that ranks the options.

Pair on these reads: a response on the call keeps the call, the control, the means and the incremental and nothing
of the asks, about 35; a response on the household interval keeps the control and the means, about 22.

Determinism: pass 1 returned FIX_NOW on the offer purchases (the dictionary calls receipt_total_sek the amount after
the discount) and the prompt now pins them to the BI warehouse's basis. Pass 2 reproduced asks 1 to 18 and 20 to 22
and found them forced; its one small open point is the 11 members whose email consent came after the last 2027
mailing (kept in, as step 10 says). Its NOT_DETERMINISTIC verdict rests on the call side only: the interval
estimator and the 1,942 against 2,080 control reading, both in the frozen blocks as v1 shipped them.

## Repair of the December receipts

The v1 build scaled December `spend_sek` in the member, store and month table by area and mailing factors after the
receipts were written, so 69 per cent of December single-visit months had a receipt total below the month's spend.
The POS export's December totals are brought into line (the factor read from the months whose receipts all redeemed
an offer, 51 area and mailing cells, mailing factor 1.07143), so every such month now ties to the cent before the
till device is applied. The BI table is untouched.

## Tried and rejected

- v1 asks (group rows, incremental, range, margin, shortfall, needed lift, control count): every one was the call's own construction, so the call-lander banked all nine and the household-interval response banked the group rows; rubric 62.
- Devices in the email, SMS and push logs that change counts: the campaign report pins sent, delivered, failed, opens, clicks, STOPP and cost per drop and the member reach per campaign, so any such device makes the report an oracle on one handling; only uncovered grains (household, county, timing) can carry a device there.
- A second receipt-count device in the POS export: the BI table ties offers and discounts per member, store and month, so the POS rows and discounts are pinned; only the receipt total is free.
- Mail-cost or print-house files: a second piece-cost figure would open a fork on the call's line.
