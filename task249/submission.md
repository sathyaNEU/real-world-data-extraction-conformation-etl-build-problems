## Tags

**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: repeat-examinee exposure on a certification examination's forms).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Flag CC27-A, CC27-B, CC27-C, CC27-D, CC27-G and CC27-H: each gave its 2027 resit candidates more than one scored item per resit sitting from what an earlier sitting or results review had shown them (1.4 or more on every licensed estimate), so their 2027 resit results carry the exposure flag and the six forms are reassembled before they are used again.**
The other four forms are at 0.6 or less. Not the excess on the items shown alone, which flags only CC27-A, C, G and H: on CC27-B and CC27-D, where more than a third of first-time candidates run out of the four hours, it is about 0.5, and most of their gain is the items resit candidates reached only because the items they recognised took them less time. Not the gain over the previous sitting, which learning and the rebound after a failed sitting lift on nine forms.

## 2. Critical Components

1. An item a resit candidate recognises takes them less time than their own pace on the other items gives: about **0.6** of it on an item reached at a scored position at an earlier sitting, **0.7** on one reached there only as a trial item (since placed on a form), and **0.8** on an item written from the same item model.
2. The excess on recognised items per resit sitting is more than **1.0** scored item on CC27-A, C, G and H, and about **0.5** on CC27-B and CC27-D.
3. On CC27-B, CC27-D and CC27-I between **36** and **48 per cent** of first-time candidates run out of time; the time recognised items free lets CC27-B's and CC27-D's resit candidates answer about one more item correctly at the end of the form (**0.9** or more), against about **0.3** on CC27-I, where little had been shown to them.
4. The exposure gain per resit sitting is **1.4** or more on the six flagged forms and **0.6** or less on the other four, on a logit or additive baseline and with the mean or median time.

## 3. Step-by-Step Solution

1. Joined the two releases of the results export (release 4's latencies in milliseconds), linked candidates through the register's number changes, mapped the 2026 layouts' item numbers through the January 2027 renumbering and keyed every response from the bank snapshot; a 2027 sitting by a candidate who had sat before under any of their numbers is a resit sitting (6,373 in all).
2. Marked each resit sitting's delivered items an earlier sitting had shown the candidate: an item reached at an earlier sitting, scored or trial, or one written from the same item model as an item reached; a held review shows again items reached and answered wrongly, so it adds no item.
3. For each 2027 window, took each item's share correct and mean log seconds among the first-time candidates who answered it; for each resit sitting, the candidate's ability as a logit shift on the scored items nothing had shown them (blank items left out) and their pace as the mean log-time ratio on those items.
4. Summed each resit sitting's correct answers less the ability's expectation on the recognised scored items answered within the four hours as they would have run, and averaged per form (component 2).
5. Gave each recognised item the time the first-time candidates' mean log seconds and the candidate's pace give (the log-normal mean), reran the sitting's clock with those times and counted the correct scored answers beyond where four hours would have ended (component 3).
6. Added the two per resit sitting and averaged over each form's 2027 resit sittings; flagged above 1.0: CC27-A, CC27-B, CC27-C, CC27-D, CC27-G and CC27-H.
7. For each form, counted the 2027 sittings a failure of the workstation or its power interrupted, from each sitting's own events in the event log: a WS_FAIL where the sitting's next event is its SESSION_RESUME or its SESSION_END (not where its own client went on logging, a NET_LOST and NET_BACK no other client logged, nor after its SESSION_END, a finished candidate's workstation switched off); a SESSION_RESUME on the sitting's own workstation after that workstation's WS_REBOOT, a restart after a freeze whether or not it was reported; each failure of a computer, keyboard, mouse or screen the invigilators reported, through the spare and minute it names for the resume; and the sittings running at Kochi when the power cut of 19 August 2027 began at 11:05; pauses, changes of seat a candidate asked for and the two hall stops are not failures.
8. For each form, counted the 2027 sittings whose examination clock ran while the centre's link was down: each client's loss from its NET_LOST (or its login, where it logged in with the link already down and logged only NET_BACK) to its NET_BACK or the sitting's end, kept where other clients at the centre logged the same loss (a loss one client logged alone was that workstation's own connection), overlapped with the sitting's SESSION_START to SESSION_END less its stops (in the Chennai fire alarm of 14 May 2027 and the Hyderabad switch to the generator of 16 November 2027 every clock stopped before the router went off and restarted after the link was back); the Kochi sittings ran about four minutes on the UPS after the router went down at 11:05.

## 4. Deliverable Answers

### resit_exposure_review_2027.xlsx

1. Flagged forms, six: CC27-A, CC27-B, CC27-C, CC27-D, CC27-G and CC27-H.
2. 2027 sittings a failure of the workstation or its power interrupted, by form, whole numbers:
   - CC27-A: 39
   - CC27-B: 28
   - CC27-C: 19
   - CC27-D: 34
   - CC27-E: 31
   - CC27-F: 36
   - CC27-G: 41
   - CC27-H: 40
   - CC27-I: 44
   - CC27-J: 38
3. 2027 sittings that ran in part without the centre's link, by form, whole numbers:
   - CC27-A: 58
   - CC27-B: 77
   - CC27-C: 49
   - CC27-D: 69
   - CC27-E: 60
   - CC27-F: 77
   - CC27-G: 74
   - CC27-H: 74
   - CC27-I: 76
   - CC27-J: 65

### resit_exposure_2027.pdf

1. Bar chart of every form's exposure gain per 2027 resit sitting against the 1.0 line, the six flagged forms marked.
