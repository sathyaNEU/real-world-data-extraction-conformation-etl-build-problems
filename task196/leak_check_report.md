# leak check, task196

**Verdict: REVIEW.** 19 files read, 67 golden figures and 14 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: payment, clause, decisive, asserted, trustees, extract, scheme, members, registrations, registration, window, reference, nothing, volumes, capture, population, account, sighting, golden, graded, reading, return, detection, bridge, quantity

## 3 answer figures in the pack (REVIEW 14)
- **REVIEW** `indemnity_standard_v6.pdf`: golden figure 4.4 appears: ...ndex is not re-measured during an indemnity year. 4.4 The experience review presents the index as a wal...
- **REVIEW** `indemnity_standard_v6.pdf`: golden figure 5.1 appears: ...the scheme year. Part 5 Settlement and recoveries 5.1 The mutual settles with each member monthly by ad...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 121 appears: ...C 01 Apr 2019 scam, unauthorised Thrimby Money KM-121 C 01 Jan 2022 scam, unauthorised Trentmoor Money...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 124 appears: ...1 Apr 2016 scam, unauthorised Garnock Exchange KM-124 A 17 Oct 2023 scam, unauthorised Netherby Pay KM-...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 118 appears: ...A 17 Oct 2023 scam, unauthorised Netherby Pay KM-118 C 01 Apr 2021 scam, unauthorised Oakhanger Transf...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 110 appears: ...8 B 01 Jul 2017 scam, unauthorised Vellowe Pay KM-110 B 01 Apr 2018 scam, unauthorised Wrenhall Pay KM-...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 102 appears: ...Apr 2021 scam, unauthorised Oakhanger Transfer KM-102 A 01 Oct 2014 scam, unauthorised Pelbury Exchange...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 101 appears: ...Code Tier Joined Covers held Brindlemere Remit KM-101 A 01 Oct 2014 scam, unauthorised Castlegate Payme...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 106 appears: ...01 Jan 2020 scam, unauthorised Quayfield Remit KM-106 B 01 Oct 2016 scam, unauthorised Saltmarch Pay KM...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 108 appears: ...01 Jan 2022 scam, unauthorised Trentmoor Money KM-108 B 01 Jul 2017 scam, unauthorised Vellowe Pay KM-1...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 103 appears: ...B 01 Apr 2018 scam, unauthorised Wrenhall Pay KM-103 A 01 Apr 2015 scam, unauthorised The reviews at i...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 112 appears: ...B 01 Oct 2016 scam, unauthorised Saltmarch Pay KM-112 C 01 Apr 2019 scam, unauthorised Thrimby Money KM...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 115 appears: ...1 Oct 2014 scam, unauthorised Pelbury Exchange KM-115 C 01 Jan 2020 scam, unauthorised Quayfield Remit...
- **REVIEW** `trustee_pack_2027_07.pdf`: golden figure 104 appears: ...ct 2014 scam, unauthorised Castlegate Payments KM-104 B 01 Apr 2016 scam, unauthorised Garnock Exchange...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `indemnity_standard_v6.pdf`: 7 of 25 stump-paragraph terms appear (payment, trustees, extract, scheme, members, account); read whether the document names the move
- **REVIEW** `register_feed_notes.txt`: 5 of 25 stump-paragraph terms appear (payment, scheme, members, reference, account); read whether the document names the move
- **REVIEW** `trustee_pack_2027_07.pdf`: 4 of 25 stump-paragraph terms appear (payment, trustees, scheme, members); read whether the document names the move

## 6 ranking artifacts (REVIEW 5, INFO 1)
- **REVIEW** `case_register_2024_27.csv`: names 12 of 14 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `member_quarterly_returns.xlsx`: names 12 of 14 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `notifications_2027_28_q1.csv`: names 12 of 14 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `notifications_2027_28_q1_supplementary.csv`: names 12 of 14 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `trustee_pack_2027_07.pdf`: names 13 of 14 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `member_register.csv`: names 12 of 14 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader, medium effort, on a fresh unzip of the 19-member `target.zip` (md5
72c2b367aa54077806c3183825940d2b) and `prompt.txt` alone.

**It missed the call, which is the stump working.** It filed about 23 cases per million against the golden's
31, at about 55 per cent confidence, by the default path exactly: 400 recorded plus the matched blanks,
with a completeness and coverage adjustment of its own invention (87 / 0.899 / 0.799, about 121 unrecorded
cases, 521 indexed). It never reached the contamination of the second channel, and its own ranking put a
different member top. Its question 6 answer is an analytical choice, carried by the three register and
match files together.

**Question 1** quotes standard 4.2, which is the estimand rather than the decisive step: the population
(cases from payments the member's customers sent in the year, recorded or not, counted once a case), the
unit (per million payments on the revised returns) and the window. The reader notes in its own words that
4.2 "says to count cases the member never recorded but gives no method for estimating them", which is the
WHAT filed and the HOW open, as intended. **Question 2:** no file ranks the candidates. **Question 4:**
nothing reads as the answer.

**Question 3 named three helper files:** `export_manifest.csv`, `data_dictionary.csv` and
`register_feed_notes.txt`.

**What I checked against the pack before ruling on its realism list.**
- Its "87 blanks against 7 to 23 elsewhere" is right for 2026/27 and the pattern holds across all four
  years (KM-104 at 21.1 per cent of its matches against 3.4 to 14.4 per cent for the rest, rising from
  11.8 per cent in 2023/24). **Not a leak of the answer:** the prompt names Castlegate, so the graded call
  is the figure and not the member, and the blanks are the input every solver must use. The reader used
  them and still filed 23.
- Its Wrenhall finding is real and is a defect. `member_register.csv` puts Wrenhall Pay at contribution
  tier A with the basis "Tier A, over 25 million payments a year" on 12,376,000 notified payments, against
  Brindlemere 44.4m, Oakhanger 27.9m and Garnock 28.7m on the same tier. A tier-A member at under half the
  tier's floor reads as a planted error.
