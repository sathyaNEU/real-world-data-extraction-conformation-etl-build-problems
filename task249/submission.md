## Tags

**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: repeat-examinee exposure on a certification examination's forms).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Flag CC27-A, CC27-B, CC27-C, CC27-D, CC27-G and CC27-H: each gave its 2027 resit candidates more than one scored item per resit sitting from what an earlier sitting or results review had shown them (1.7 to 2.3), so their 2027 resit results carry the exposure flag and the six forms are reassembled before they are used again.**
The other four forms are at 0.6 or less. Not the excess on the items shown alone, which flags only CC27-A, C, G and H: on CC27-B and CC27-D, where about 40 per cent of candidates run out of the four hours, it is about 0.5 on each, and most of their gain is the items resit candidates reached only because the items they recognised took them less time. Not the gain over the previous sitting, which learning and the rebound after a failed sitting lift on nine forms.

## 2. Critical Components

1. An item a resit candidate recognises (the same item reached at an earlier sitting, a trial item since placed on a form, or an item written from the same item model) takes them about **70 per cent** of the time their own pace on the other items gives.
2. The excess on recognised items per resit sitting is CC27-A **1.4**, CC27-C **1.8**, CC27-G **1.2**, CC27-H **1.1**; on CC27-B and CC27-D it is **0.5** and **0.5**.
3. On CC27-B, CC27-D and CC27-I about 40 per cent of first-time candidates run out of time; the time recognised items free lets CC27-B's and CC27-D's resit candidates answer **1.2** and **1.3** more items correctly at the end of the form, against **0.3** on CC27-I, where little had been shown to them.
4. The exposure gain per resit sitting: CC27-A 1.7; CC27-B 1.7; CC27-C 2.3; CC27-D 1.7; CC27-E 0.6; CC27-F 0.2; CC27-G 1.7; CC27-H 1.8; CC27-I 0.4; CC27-J 0.5.

## 3. Step-by-Step Solution

1. Joined the two releases of the results export (release 4's latencies in milliseconds), linked candidates through the register's number changes, mapped the 2026 layouts' item numbers through the January 2027 renumbering and keyed every response from the bank snapshot; a 2027 sitting by a candidate who had sat before under any of their numbers is a resit sitting (6,717 in all).
2. Marked each resit sitting's delivered items an earlier sitting had shown the candidate: an item reached at an earlier sitting, scored or trial, or one written from the same item model as an item reached; a held review shows again items reached and answered wrongly, so it adds no item.
3. For each 2027 window, took each item's share correct and mean log seconds among the first-time candidates who answered it; for each resit sitting, the candidate's ability as a logit shift on the scored items nothing had shown them (blank items left out) and their pace as the mean log-time ratio on those items.
4. Summed each resit sitting's correct answers less the ability's expectation on the recognised scored items answered within the four hours as they would have run, and averaged per form (component 2).
5. Gave each recognised item the time the first-time candidates' mean log seconds and the candidate's pace give (the log-normal mean), reran the sitting's clock with those times and counted the correct scored answers beyond where four hours would have ended (component 3).
6. Added the two per resit sitting and averaged over each form's 2027 resit sittings; flagged above 1.0: CC27-A, CC27-B, CC27-C, CC27-D, CC27-G and CC27-H.
7. For each form, counted the 2027 sittings a failure of the workstation or its power interrupted: every sitting the event log shows a WS_FAIL on, every failure of a computer, screen, keyboard or mouse the invigilators' reports record (mapped to its sitting through the seat plan; the server logs no WS_FAIL when the centre's link is already down or the computer keeps running, and some failures it logged go unreported), and the sittings running at Kochi when the power cut of 19 August 2027 began at 11:05, which the log does not show until they resumed; the pauses and the changes of seat a candidate asked for, though they also resume on a spare, are not failures.
8. For each form, counted the 2027 sittings whose examination clock ran while their workstation's client had no link: from each NET_LOST to that client's next NET_BACK, or to the sitting's end where none came, and from the client's login (its tutorial, or its resume on a spare) to its NET_BACK where it logged in with the link already down and so logged no NET_LOST, overlapped with the sitting's SESSION_START to SESSION_END; a client still on its end screen logs the loss too, and the Kochi sittings ran about four minutes on the UPS after the router went down at 11:05.

## 4. Deliverable Answers

### resit_exposure_review_2027.xlsx

1. Flagged forms, six: CC27-A, CC27-B, CC27-C, CC27-D, CC27-G and CC27-H.
2. 2027 sittings a failure of the workstation or its power interrupted, by form, whole numbers:
   - CC27-A: 15
   - CC27-B: 15
   - CC27-C: 14
   - CC27-D: 13
   - CC27-E: 21
   - CC27-F: 22
   - CC27-G: 20
   - CC27-H: 25
   - CC27-I: 27
   - CC27-J: 31
3. 2027 sittings that ran in part without the centre's link, by form, whole numbers:
   - CC27-A: 60
   - CC27-B: 73
   - CC27-C: 58
   - CC27-D: 64
   - CC27-E: 71
   - CC27-F: 67
   - CC27-G: 70
   - CC27-H: 73
   - CC27-I: 81
   - CC27-J: 85

### resit_exposure_2027.pdf

1. Bar chart of every form's exposure gain per 2027 resit sitting, the part on the items shown before and the part in the time those items freed, against the 1.0 line, the six flagged forms marked.
