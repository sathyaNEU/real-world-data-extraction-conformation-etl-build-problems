# leak check, task196

**Verdict: REVIEW.** 20 files read, 66 golden figures and 13 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: clause, payment, register, decisive, scheme, asserted, trustees, population, extract, registrations, registration, window, reference, nothing, meeting, evidence, account, sentence, members, golden, graded, reading, computed, return, volumes

## 3 answer figures in the pack (REVIEW 12)
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 101 appears: ...Code Tier Joined Covers held Brindlemere Remit KM-101 A 01 Oct 2014 scam, unauthorised Castlegate Payme...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 115 appears: ...1 Oct 2014 scam, unauthorised Pelbury Exchange KM-115 C 01 Jan 2020 scam, unauthorised Quayfield Remit...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 103 appears: ...B 01 Apr 2018 scam, unauthorised Wrenhall Pay KM-103 A 01 Apr 2015 scam, unauthorised The reviews at i...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 110 appears: ...8 B 01 Jul 2017 scam, unauthorised Vellowe Pay KM-110 B 01 Apr 2018 scam, unauthorised Wrenhall Pay KM-...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 124 appears: ...1 Apr 2016 scam, unauthorised Garnock Exchange KM-124 A 17 Oct 2023 scam, unauthorised Netherby Pay KM-...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 112 appears: ...B 01 Oct 2016 scam, unauthorised Saltmarch Pay KM-112 C 01 Apr 2019 scam, unauthorised Thrimby Money KM...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 121 appears: ...C 01 Apr 2019 scam, unauthorised Thrimby Money KM-121 C 01 Jan 2022 scam, unauthorised Trentmoor Money...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 102 appears: ...Apr 2021 scam, unauthorised Oakhanger Transfer KM-102 A 01 Oct 2014 scam, unauthorised Pelbury Exchange...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 118 appears: ...A 17 Oct 2023 scam, unauthorised Netherby Pay KM-118 C 01 Apr 2021 scam, unauthorised Oakhanger Transf...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 106 appears: ...01 Jan 2020 scam, unauthorised Quayfield Remit KM-106 B 01 Oct 2016 scam, unauthorised Saltmarch Pay KM...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 104 appears: ...ct 2014 scam, unauthorised Castlegate Payments KM-104 B 01 Apr 2016 scam, unauthorised Garnock Exchange...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 108 appears: ...01 Jan 2022 scam, unauthorised Trentmoor Money KM-108 B 01 Jul 2017 scam, unauthorised Vellowe Pay KM-1...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `indemnity_standard_v6.pdf`: 10 of 25 stump-paragraph terms appear (payment, register, scheme, trustees, extract, meeting); read whether the document names the move
- **REVIEW** `register_feed_notes.txt`: 6 of 25 stump-paragraph terms appear (payment, register, scheme, reference, account, members); read whether the document names the move
- **REVIEW** `trustee_pack_2027_07.pdf`: 7 of 25 stump-paragraph terms appear (payment, register, scheme, trustees, meeting, evidence); read whether the document names the move

## 6 ranking artifacts (REVIEW 5, INFO 1)
- **REVIEW** `case_register_2024_27.csv`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `member_quarterly_returns.xlsx`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `notifications_2027_28_q1.csv`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `notifications_feed_latest.csv`: names 12 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `trustee_pack_2027_07.pdf`: names 13 of 13 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `member_register.csv`: names 12 of 13 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read, wave 6 audit (the shipped pack, target.zip 9c54b440)

Run because `leak.py` overwrote this build's original reader section before that bug was fixed. Pack
and `prompt.txt` only, scored by `score_reader.py`.

### The call held. The ask layer did not.

| block | answered | hit |
|---|---|---|
| committed index and indexed cases | 2 | **0** |
| call inputs (recorded cases, payments sent) | 2 | 2 |
| ask figures | 29 | **29** |

It filed **25 cases per million** against a golden of **31**, on 560 indexed cases against 688, at
about 35 per cent confidence. It reached the right shape of the estimator and the wrong constant: it
grossed the register-matched unrecorded cases up by the member's own register coverage (282/400 =
0.705), where the golden takes the two-source estimate off the sightings no fund-return request of
the member's own preceded. It listed 23, 25 and 26 as the range it considered, so the decisive step
is doing its work.

Then it took all 29 ask figures exactly: the indemnity by tier and quarter to the penny, all twelve
members' Q1 notification counts and values, and the recovery shares by route.

### Three findings it volunteered that belong to whoever repairs this

1. **`register_feed_notes.txt` hands over a step.** Its sentence "pad the account number back to
   eight digits before matching anything against the register, or the match loses every account
   whose number starts with a zero" is not something an organisation writes down.
2. **`member_payment_matches.csv` is a pre-done join** that carries `case_reference`, so the match a
   solver would build is supplied.
3. **A possible data defect worth checking:** 213 cases in `notifications_2027_28_q1.csv` carry
   2026/27 payment dates and share no key with the 417 late-notified rows in the case register. The
   reader read it as generator noise and treated the register alone as the recorded set, noting that
   adding the 213 would move the recorded count by about 21 and the index by about 1.
4. Realism tell: Castlegate's unrecorded count rising 52, 71, 92, 113 over four years reads as too
   regular for an organisation's record.
