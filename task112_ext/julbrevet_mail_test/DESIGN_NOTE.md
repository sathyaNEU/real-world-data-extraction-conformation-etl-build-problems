# Brannvik Plus Julbrevet mail test (built on task112_ext): rubric repair

The task was uploaded as a finished package (b43ae590-v1): Experiment & Causal Analysis in Marketing & Consumer
Research, the call to drop addressed Julbrevet mail because the lower end of the area-clustered 90 percent range,
minus 56.99 SEK per piece, is worth minus 14.25 SEK at 25 percent margin against the 11.40 SEK piece cost. The
portal passed the call, the stump and the determinism block and returned a rubric score of 62 per cent. This
repair re-sites the supplemental asks only.

## Frozen

The prompt is the author's one-paragraph rephrase with the call question first and no backstory. The Final
Recommendation, the Critical Components, steps 1 to 8 and the distractor are carried over byte for byte
(`generator/spec.py` asserts it). Every data file the call reads is byte-identical to v1:
`pos_offer_redemptions_2027.csv` moved only in `receipt_total_sek` and, on Julbrevet O2 rows, `offer_code`, and the
messaging runbook's offers paragraph (7.3) gained the loyalty engine's rule that the till honours an offer once for
each member, which every 2027 redemption keeps (`generator/checks.py`). The call recomputes unchanged: 14,108 mailed at 2,298.58, 1,942 control at 2,161.36, 1,150
objected at 2,102.15, incremental 137.21, standard error 94.21 on 4.54 degrees of freedom, range minus 56.99 to
331.42, margin minus 14.25, shortfall 25.65, needed 239.81.

## Rebuild

The generator reads the uploaded package's input zip (b43ae590-v1, `Brannvik Plus Reach 2027 Input Files.zip`, sha256
prefix d09e36c12403), which stays with the author as the source. Unzip it, then run `generator/patch.py <v1 inputs>
<out>`, `asks.py <out> figures.json`, `golden.py figures.json <deliverables>`, `spec.py`, and `zips.py`;
`checks.py <v1 inputs> <out>` asserts the freeze, both devices and the call. Two runs are byte-identical.

## Where the 62 and the 65 and 55 came from

v1's nine supplementary answers were all the call's own construction, so a response that landed the call banked
every ask (62). v2 hid two silent devices from two cold readers (0 of 20 exact) but graded figures the devices moved
by only 1 to 6 per cent, and the client's rubric grades numbers "allowing reasonable tolerance": scored that way the
same readers keep about nine tenths of the asks, which is the portal's 65 and 55. v3 graded the devices' own sets
(misses of half or more) and both cold readers found both devices, because each question named the place the
evidence sits. v4 kept the misses large with one device and hidden wording: one reader took the easy route (2 of 28)
and the other reconciled the POS export to the BI table and kept every figure, a pair in the sixties.

## Ask sheet

Two silent devices of different families under every graded figure, so a reader who cracks one lands where the
easy route lands.

| Ask | Figures | Devices | Routes and their misses |
|---|---|---|---|
| Sheet 1: BV27-13-O2 redemptions of 1 to 24 December with a basket under 750 SEK before the discount, and the purchases paid on them, by store format | 6 | D3: fourteen tills (BV101, BV104, BV106, BV110, BV113, BV114, BV115, BV118, BV119, BV128, BV129, BV132, BV138, BV141) send the total before the discount from their October and November upgrade. D7: the self-service tills write the campaign's first offer code for either Julbrevet card offer, so 1,415 of the 2,841 O2 redemptions (23 to 62 per cent of each store's) carry BV27-13-O1 | the code and the total read at face value: 4 receipts for 99; tills repaired, code trusted: 50 (43 per cent short at the closest figure); O2 recovered, tills not repaired: 12; O2 recovered and the discount taken off everywhere: 157 |
| Sheet 2: the same by ISO week 48 to 51 | 8 | the same | the same routes, every week missed |
| Memo close and chart | 2 + 12 bars | the same | each total misses the same way |

Neither device is announced: the prompt sets the purchase basis once for the whole prompt ("Count every purchase
amount the way the BI warehouse counts purchases"), the ask names the offer by its code and its terms, and nothing
points at the O1 rows. The relabel leaves no absence or marker: every store carries O2 redemptions under both codes,
receipt numbers run on unchanged, and the O1 code still carries every ham redemption.

Evidence a grader verifies. The tills: on every member, store and month whose receipts all redeemed an offer, the
fourteen stores' totals exceed spend_sek by exactly the discount (1,315 of 1,315 in December) and every other store's
equal it (671 of 671). The codes: the O1 rows giving exactly 50 SEK off a basket over 700 SEK are exactly the 1,415
recoded O2 redemptions (the one other 50 SEK O1 row is a 573.77 SEK basket, a ham at 200 SEK), and each of the 219
accounts with two O1 rows has one of them, while no other account in the export redeems any offer twice. Read at face
value, the codes would have 219 members redeem the ham offer twice, which runbook 7.3 rules out; that closes the code
reading, which the first judge pass had called a defensible second answer. Step 9 names both handlings.

## Measured

Pack 60af3988c3a6 (v5, input zip sha256 prefix). Determinism judge: DETERMINISTIC, APPROVE, every ask reproduced,
with the face-value code reading flagged as an open second answer (closed in v5.1 by the runbook clause). Two cold
readers at medium effort, each holding only the prompt and the 23 inputs:

- Both landed the drop call on their own area-level interval (randomisation inference over the 2,925 draws of three
  areas, minus 120 to 388), so the range, margin, shortfall and needed-lift figures miss the golden's.
- Both reconciled the POS export to the BI table, found the fourteen before-discount tills and repaired them, and
  neither looked at the O1 rows: each filed 50 receipts and 33.8 thousand SEK (Stor 19, Mellan 30, Nära 1; weeks 10,
  16, 16, 8), the one-device route, and kept 2 of 28 ask cells (the two empty Nära bars, inside the one chart
  criterion) and none of the 16 graded figures.

Pair on these reads: each keeps the call, the control, the means and the incremental, the memo's opening call and
nothing else of the asks, about 30 to 40 a response.

Pack d7aa35a54ac2 (v5.1, the shipped pack, with the runbook clause): determinism judge DETERMINISTIC, APPROVE, every
ask reproduced, no repair. A third cold reader did what the first two did: it reconciled the POS export to the BI
table, repaired the fourteen tills, never opened the O1 rows, and filed 50 receipts and 33.8 thousand SEK on its own
area-level interval (minus 94.8 to 369.2), 2 of 28 ask cells and none of the 16 graded figures. Three of three cold
readers have found the till device and none the offer codes.

## Repair of the December receipts

The v1 build scaled December `spend_sek` in the member, store and month table by area and mailing factors after the
receipts were written, so 69 per cent of December single-visit months had a receipt total below the month's spend.
The POS export's December totals are brought into line (the factor read from the months whose receipts all redeemed
an offer, 51 area and mailing cells, mailing factor 1.07143), so every such month now ties to the cent before the
till device is applied. The BI table is untouched.

## Tried and rejected

- v1 asks (group rows, incremental, range, margin, shortfall, needed lift, control count): every one was the call's own construction, so the call-lander banked all nine and the household-interval response banked the group rows; rubric 62.
- Devices in the email, SMS and push logs that change counts: the campaign report pins sent, delivered, failed, opens, clicks, STOPP and cost per drop and the member reach per campaign, so any such device makes the report an oracle on one handling; only uncovered grains (household, county, timing) can carry a device there.
- A second receipt-count device in the POS export: the BI table ties offers and discounts per member, store and month, so the POS rows and discounts are pinned; only the receipt total, the time inside the month and the offer code are free.
- Mail-cost or print-house files: a second piece-cost figure would open a fork on the call's line.
- v2 asks (offer purchases by offer and format, reach counts of whole groups, the offer purchases of each reach group): both silent devices held against two cold readers (0 of 20), but the figures moved by only 1 to 6 per cent and the steps listed the seen hazards as results; the portal's top two scored 65 and 55.
- A seven-store till rollout: the receipts-paid-under-700 band missed by only 19 to 36 per cent at Stor and Mellan, because the band sits mostly at BV110 and BV101; widened to ten stores.
- v3 asks (the devices' own sets: O2 receipts paid under 700 on the BI basis, email-consented households the platform would not send to): both cold readers found both devices, led by wording that named the evidence's place.
- The pre-2027 email suppression list as an ask device: hidden wording moves whole reach groups by 2 per cent at most, inside the grading tolerance, and wording that isolates it names the sends; retired from the asks.
- v4 (the threshold band on the till device alone): the BI pin sent one of two cold readers to reconcile single-visit months, where the fourteen stores show to the cent, and it kept all 28 figures; one device under a pin the call side needs cannot hold a careful reader.
- The O2 relabel confined to one county: an offer missing from every Västernorrland store is an absence a by-store count shows at once; spread across every store's self-service share instead.
