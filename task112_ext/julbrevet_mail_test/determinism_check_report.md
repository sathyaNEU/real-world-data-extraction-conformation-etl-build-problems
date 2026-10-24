# Verdict: task112ext v51-1

- **Verdict:** DETERMINISTIC (all committed answers reproduce from the shipped files).
- **Disposition:** APPROVE. No repair required. Two watch items below (household-level interval fork on the main call; undisclosed mislabel and pre-discount till totals behind asks 1 to 18). Neither is a verdict-changing defect on the literal reading.
- **Why:** The main call is forced by the guidance's section 5 line (lower end of a two-sided 90 percent interval, 25 percent margin, 11.40 SEK per piece). The control is three areas drawn by lot, so the interval has to sit at area level. Done that way the lower end is negative (-56.99) and nowhere near the 45.60 break-even, so the mailing is dropped. The asks reproduce exactly, but only after two undisclosed adjustments (see Evidence).

## Evidence (recomputed with python3 -I from target/)
| Item | Result |
|---|---|
| Eligible households (open on 15 Nov 2027, Jan-Oct household spend >= 6,000) | 17,200 reproduced |
| Mailed (BV27-13-D1 rows) | 14,108 households in 24 areas, all eligible, reproduced |
| Non-mailed eligible in 803/805/852 | 2,080; post-consent replay on the main card holder (earliest-joined open account) at 2027-11-14 23:00 UTC gives 138 N, 1,942 control, reproduced |
| December purchases per household, all accounts, zero if none | mailed 2,298.58, control 2,161.36, difference 137.21, reproduced |
| Area-level interval (weighted area means, Welch/cluster, df 4.54, t 2.0615, SE 94.21) | -56.99 to 331.42, reproduced |
| Margin of the lower end | 25 percent x -56.99 = -14.25 vs 11.40 piece cost, shortfall 25.65; needed lift 45.60 + 2.0615 x 94.21 = 239.81 (arithmetic consistent) |
| Asks 1 to 18 | all reproduced: Stor 37 / 25.1, Mellan 59 / 39.9, Nära 3 / 2.0; weeks 48-51: 21/14.1, 28/19.0, 34/23.1, 16/10.9; total 99 receipts and 67.0 (67.01) thousand SEK; chart counts by week and format as stated (I confirmed week totals; the format-by-week splits come from the same set) |

Asks 1 to 18 rest on two things the dictionary does not tell the solver.
- **Mislabelled offer code.** 1,415 BV27-13-O2 receipts are coded BV27-13-O1. They are the O1 rows with discount exactly 50 and a pre-discount basket over 700. Each of the 219 accounts with two O1 rows has exactly one such row.
- **Till total before the discount at 14 stores.** At BV101, 104, 106, 110, 113, 114, 115, 118, 119, 128, 129, 132, 138 and 141, receipt_total_sek is before the discount. In the msm join it exceeds spend_sek by exactly the discount on all of the 1,232 member-store-months in December 1-24 whose receipts all redeemed offers. At every other store it equals spend_sek on all 634 such rows. The brief says 1,315 and 671 because it counts December through the 31st. I did not extend my check to those dates.
- **Dictionary contradicts the data on this.** The dictionary says receipt_total_sek is the amount paid after the discount, and that a receipt redeems one offer and offer_code is the offer's code. At the 14 stores that is false. The prompt's wording ("50 kr off a purchase over 700 kr", "the way the BI warehouse counts purchases") plus the msm join make the golden derivable, but nothing states it.

### Second readings left open (figure each gives)
- **Offer identification.** Offer_code = BV27-13-O2 only (1,426 rows): 50 receipts, 33.8 thousand SEK with the store adjustment (Stor 19 / Mellan 30 / Nära 1; weeks 10/16/16/8). Taking the dictionary literally (total = paid, pre = total + 50) gives 4 receipts, 2.7 thousand SEK. The prompt's offer terms (50 kr off over 700) point to the golden reading, but a code-literal reader differs on every ask.
- **Till total taken as paid, ignoring the 14-store issue.** Golden set 99 receipts, but 71.4 thousand SEK paid (Stor 26.6, Mellan 42.6, Nära 2.1; weeks 15.0, 20.2, 24.6, 11.6). With the dictionary's "after discount" applied to pre-discount basket for all stores: 12 receipts, 8.1 thousand SEK. The prompt's BI-warehouse sentence closes the paid basis; the pre-discount test is closed only by the msm join.
- **Basket test on the raw total <750 (no adjustment).** 165 receipts, 115.1 thousand SEK. Paid-after-discount <750: 445 receipts, 318.3 thousand SEK. The prompt says "before the discount", so this is not licensed.
- **Keeping the 573.77 BV132 row (a genuine O1 that happens to be 50)** is excluded by the over-700 test; including it would give a 100th receipt only if pre were <750, but its pre is 573.77 and the offer needs over 700, so it is correctly out (the 50-SEK O1 set with pre <= 700 is 1 row).
- Week and time zone: redeemed_at is Swedish local and all rows fall in 1-24 Dec; no row sits near a week or window edge on the UTC question (no redemptions at 23:00 or later). Fine. Rounding: 67.01 rounds to 67.0 consistently.
- 750 boundary: 5 receipts sit within 1 SEK of 750 (749.89, 750.12, 750.55 etc.); they are decided on the stated pre-discount amount, and rounding to one decimal in thousands does not move the totals.

### Competing answer on the main call
- **Household-level interval.** The household-level Welch 90 percent interval on the same contrast is 58.0 to 216.4. Its lower end clears 45.60, so this reading says keep.
- **Why it is not licensed.** The control was drawn by area (three areas), so an analyst who respects the assignment unit gets -57. The guidance does not file "cluster at area level"; it only states the draw by lot and says the interval is on incremental purchases per piece.
- **Unweighted area-mean Welch.** The contrast is 140.1, SE 91.9, df about 4, and the lower end is about -56. The call is the same.
- **Control with objectors not removed (2,080).** Would shift the mean slightly but the policy section 6 and guidance section 2 pin the objector exclusion; I did not recompute the interval. The call is not expected to move.

## Files/Hygiene
PASS. 23 files, formats csv, xlsx, docx, pdf, md. Realistic operational artifacts, with mixed time bases, semicolon and decimal-comma POS export, and a real-looking campaign report. No benchmark or authoring disclosures seen; DATA_DICTIONARY.md is a normal CRM note. The only defect worth a note is that the dictionary's statement on receipt_total_sek is false for 14 stores, which is a presentation of Layer 1 mess.

## Stump power
Good on the main call. The easy route is a household-level interval (58.0 to 216.4, keep) or the report's descriptive pair (2,298.58 vs 817.77), and a capable model plausibly takes it. The asks are hard through the undisclosed mislabel and the 14-store pre-discount totals, so a strong model that does not cross-check the till against the BI table will file 50 receipts or 71.4 thousand SEK.

## Stumping type
mechanism: statistical_rigor (unit of analysis for the interval, with a recovered control)
stumping_family: analytical_non_defect
surface_read_dependency: no (the report's basket pair is descriptive; the numbers are fine)
sole_data_defect: no (on clean data the area-level interval still decides the call)
The difficulty is the cluster-level interval on a three-area control; the asks carry the semantic and mess devices, which the rules allow.

## Three rules
domain: pass | layers: pass | decisive_step: analytical
The deciding quantity is an incremental-purchases estimate with a randomised-by-area control and a cluster-robust interval, which marketing measurement actually does. The easy route is a household-level interval, which gives 58.0 to 216.4, clears the 45.60 line, and files "keep the mailing". Layer 1 is the multi-system extracts (UTC against local time, consent replay, household keys, till and BI totals). Layer 2 is the interval at the assignment unit.

## Fix
none. Optional hardening: none required. If the author wants the main call tighter against the household-level reading, file the unit (purchases compared at the level the control was assigned) in the guidance, not the method.
