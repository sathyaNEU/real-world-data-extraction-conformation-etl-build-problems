# task128 · Ferncliffe Trust Bank: the 2027 early-stage collections team

## Tags

**Domain:** Banking, Credit & Financial Risk (collections and recovery: a collections team funded on the rolls its calls prevent).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**No centre should get the new early-stage team in 2027; return budget line C-01.**

London's new team would have prevented about 500 rolls a year on its July 2025 to June 2026 lists, 200 short of the credit policy's 694, and every other centre is further short. Not the called against the uncalled accounts over the year, which credits the call with the rolls of accounts held off the list, records the dialler skipped and the campaign cycles' riskier days. Not the same-list comparison with the skipped records set aside, which leaves their undiallable share among the records left at shift end. Not London's effect on every record its team left, which the new team's 400 dials a day cannot reach. Not one comparison pooled over the year's lists, which sets the campaign cycles' records against every other day's.

## 2. Critical Components

1. London's new team would have prevented **500** rolls a year
2. Kingston's would have prevented **200**
3. Winnipeg's would have prevented **200**
4. Sudbury's would have prevented **100**
5. Thunder Bay's would have prevented **100**

## 3. Step-by-Step Solution

1. Marked each record on ES30_DIALLER_LISTS_2025-01_2026-09.csv with a list day from July 2025 to June 2026 as a roll where CARD_DELINQUENCY_HISTORY_2025-01_2026-10.parquet has the account 90 or more days past due on its cycle date two months after the list day (CP-14 6.3).
2. Found the lists the teams did not finish: records with no result appear only on the collections days of cycles 04 and 13, 24 days at every centre.
3. On each of those lists compared the roll rate of the records with no result against every record the dialler reached, the DNC and NDN records it skipped included, weighted by the records with no result, and divided by the dialled share of the records reached: London's calls prevent 5.2 rolls per 100 dials.
4. Sized the new team at the 400 accounts dialled a day of line C-01 in 2027_Collections_Budget_Request.xlsx (CP-14 6.4): London left more diallable records than 400 on all 24 days, 9,600 dials in the year, and every other centre left fewer each day, so its new team dials every diallable record left.
5. Multiplied each centre's effect per dial by those dials: London 500 rolls a year, Kingston 200, Winnipeg 200, Sudbury 100 and Thunder Bay 100, every one under CP-14 6.5's 694.
6. Counted right-party contacts per 100 accounts dialled and promises to pay per 100 contacts from the lists' results, reading AR before each centre's change to dialler version CX2.1 in ES_WORKFORCE_DIALLER_LOG_2025-01_2026-09.csv as the old dialler's arrangement, as the agent and minutes of talk on those calls in ES30_CALL_DETAIL_2025-07_2026-06.parquet show.
7. Summed the balances of ES30_PAYMENT_ARRANGEMENTS_2025-01_2026-09.csv set up from July 2025 to June 2026 by centre, VUSD card balances at TREASURY_BOOKING_RATES_USDCAD_2025-01_2026-10.csv's rate on the set-up day.
8. Recommendation: no centre reaches 694, so budget line C-01 is returned; London comes closest at 500, 200 short.

## 4. Deliverable Answers

### centre_call_effects_2025_2026.csv

1. Five rows: rolls the new team's calls would have prevented on the July 2025 to June 2026 lists to the nearest 100, whether that reaches the 694-roll line, right-party contacts per 100 accounts dialled and promises to pay per 100 right-party contacts to one decimal, balances on payment arrangements set up in that year to the nearest $100,000:
   - London: 500 rolls, below the line, 49.3 contacts per 100 accounts dialled, 37.6 promises per 100 contacts, $15,500,000
   - Kingston: 200 rolls, below the line, 57.2 contacts, 39.1 promises, $14,300,000
   - Winnipeg: 200 rolls, below the line, 52.8 contacts, 40.3 promises, $16,000,000
   - Sudbury: 100 rolls, below the line, 54.6 contacts, 36.4 promises, $10,100,000
   - Thunder Bay: 100 rolls, below the line, 50.4 contacts, 41.2 promises, $7,000,000

### centre_call_effects_2025_2026.png

1. One bar per centre for its rolls, largest to smallest (London, Kingston, Winnipeg, Sudbury, Thunder Bay), each bar labelled with its figure, with the 694-roll funding line drawn and labelled and London picked out as the closest

### sixth_team_decision_2027.docx

1. The decision: return budget line C-01, no centre's new team reaching the 694-roll line
2. The centre with the most rolls is London, 500, 200 short of the line
