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
7. For each form, counted the 2027 sittings a failure of the workstation or its power interrupted: each WS_FAIL in the event log belongs to the sitting whose clock was running on that workstation when it failed, the last that started there that day before it (a workstation repaired at lunch carries the afternoon's booking on a morning failure, while the morning candidate resumes on a spare or, with a few minutes of work left, has the sitting closed on the saved responses), and the Kochi power cut of 19 August 2027 took down every sitting running there at 11:05 local time, though the log holds nothing until they resumed; the invigilators' pauses and the network losses are not failures.
8. For each form, counted the 2027 sittings whose examination clock ran while their workstation had lost the centre's link: each NET_LOST to the next NET_BACK on that workstation, or to the sitting's end where none came while it ran, overlapping the sitting's SESSION_START to SESSION_END; every seated workstation logs the loss, so a sitting already ended or not yet started is not counted, and a loss that began in the tutorial counts once the clock started inside it.

## 4. Deliverable Answers

### resit_exposure_review_2027.xlsx

1. Flagged forms, six: CC27-A, CC27-B, CC27-C, CC27-D, CC27-G and CC27-H.
2. 2027 sittings a failure of the workstation or its power interrupted, by form, whole numbers:
   - CC27-A: 14
   - CC27-B: 9
   - CC27-C: 8
   - CC27-D: 11
   - CC27-E: 10
   - CC27-F: 21
   - CC27-G: 20
   - CC27-H: 14
   - CC27-I: 11
   - CC27-J: 24
3. 2027 sittings that ran in part without the centre's link, by form, whole numbers:
   - CC27-A: 32
   - CC27-B: 31
   - CC27-C: 33
   - CC27-D: 39
   - CC27-E: 33
   - CC27-F: 42
   - CC27-G: 38
   - CC27-H: 40
   - CC27-I: 59
   - CC27-J: 53

### resit_exposure_2027.pdf

1. Bar chart of every form's exposure gain per 2027 resit sitting, the part on the items shown before and the part in the time those items freed, against the 1.0 line, the six flagged forms marked.
