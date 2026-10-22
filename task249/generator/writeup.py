"""submission.md from figures.json: tags, the recommendation, the critical components, the steps, the deliverable
answers. Every figure is read from figures.json."""
import json
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))


def one(v):
    return "%.1f" % v


def words(fs):
    fs = list(fs)
    return ", ".join(fs[:-1]) + " and " + fs[-1] if len(fs) > 1 else fs[0]


def write(path, fig):
    c, a, k = fig["call"], fig["asks"], fig["components"]
    flagged = c["flagged"]
    others = [f for f in P.F27 if f not in flagged]
    lo = min(c["gain"][f] for f in flagged)
    hi_flag = max(c["gain"][f] for f in flagged)
    hi = max(c["gain"][f] for f in others)
    gains = "; ".join("%s %s" % (f, one(c["gain"][f])) for f in P.F27)
    direct = ", ".join("%s **%s**" % (f, one(c["direct"][f])) for f in ("CC27-A", "CC27-C", "CC27-G", "CC27-H"))
    ints = "\n".join("   - %s: %d" % (f, a["interrupted"][f]) for f in P.F27)
    offs = "\n".join("   - %s: %d" % (f, a["offline"][f]) for f in P.F27)
    db, dd = one(c["direct"]["CC27-B"]), one(c["direct"]["CC27-D"])
    bd = "about %s on each" % db if db == dd else "about %s and %s" % (db, dd)
    fam = fig["family"]
    text = f"""## Tags

**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: repeat-examinee exposure on a certification examination's forms).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Flag {words(flagged)}: each gave its 2027 resit candidates more than one scored item per resit sitting from what an earlier sitting or results review had shown them ({one(fam["lo_flagged"])} or more on every licensed estimate), so their 2027 resit results carry the exposure flag and the six forms are reassembled before they are used again.**
The other four forms are at {one(fam["hi_other"])} or less. Not the excess on the items shown alone, which flags only CC27-A, C, G and H: on CC27-B and CC27-D, where more than a third of first-time candidates run out of the four hours, it is about {one(fam["direct_bd"])}, and most of their gain is the items resit candidates reached only because the items they recognised took them less time. Not the gain over the previous sitting, which learning and the rebound after a failed sitting lift on nine forms.

## 2. Critical Components

1. An item a resit candidate recognises takes them less time than their own pace on the other items gives: about **{one(fam["time_same"])}** of it on an item reached at a scored position at an earlier sitting, **{one(fam["time_trial"])}** on one reached there only as a trial item (since placed on a form), and **{one(fam["time_sib"])}** on an item written from the same item model.
2. The excess on recognised items per resit sitting is more than **{one(fam["direct_acgh_min"])}** scored item on CC27-A, C, G and H, and about **{one(fam["direct_bd"])}** on CC27-B and CC27-D.
3. On CC27-B, CC27-D and CC27-I between **{k["speeded_lo"]}** and **{k["speeded_hi"]} per cent** of first-time candidates run out of time; the time recognised items free lets CC27-B's and CC27-D's resit candidates answer about one more item correctly at the end of the form (**{one(fam["reach_bd_min"])}** or more), against about **{one(fam["reach_i"])}** on CC27-I, where little had been shown to them.
4. The exposure gain per resit sitting is **{one(fam["lo_flagged"])}** or more on the six flagged forms and **{one(fam["hi_other"])}** or less on the other four, on a logit or additive baseline and with the mean or median time.

## 3. Step-by-Step Solution

1. Joined the two releases of the results export (release 4's latencies in milliseconds), linked candidates through the register's number changes, mapped the 2026 layouts' item numbers through the January 2027 renumbering and keyed every response from the bank snapshot; a 2027 sitting by a candidate who had sat before under any of their numbers is a resit sitting ({c["n_resit"]:,} in all).
2. Marked each resit sitting's delivered items an earlier sitting had shown the candidate: an item reached at an earlier sitting, scored or trial, or one written from the same item model as an item reached; a held review shows again items reached and answered wrongly, so it adds no item.
3. For each 2027 window, took each item's share correct and mean log seconds among the first-time candidates who answered it; for each resit sitting, the candidate's ability as a logit shift on the scored items nothing had shown them (blank items left out) and their pace as the mean log-time ratio on those items.
4. Summed each resit sitting's correct answers less the ability's expectation on the recognised scored items answered within the four hours as they would have run, and averaged per form (component 2).
5. Gave each recognised item the time the first-time candidates' mean log seconds and the candidate's pace give (the log-normal mean), reran the sitting's clock with those times and counted the correct scored answers beyond where four hours would have ended (component 3).
6. Added the two per resit sitting and averaged over each form's 2027 resit sittings; flagged above 1.0: {words(flagged)}.
7. For each form, counted the 2027 sittings a failure of the workstation or its power interrupted, from the event log: a WS_FAIL where the sitting's next event is its SESSION_RESUME or its SESSION_END (not where its own client went on logging, a NET_LOST and NET_BACK no other client logged, nor after its SESSION_END, a finished candidate's workstation switched off); a SESSION_RESUME on the sitting's own workstation after that workstation's WS_REBOOT; a SESSION_RESUME on a spare where the workstation the sitting left logged a WS_REBOOT before the session's last sitting ended, reported or not (the technician restarts a workstation left over a freeze or a faulty keyboard, mouse or screen, and never one left at a candidate's request over glare, noise, a desk or a chair); and the sittings running at Kochi when the power cut of {a["power_day"]} began at 11:05; pauses, those changes of seat and the two hall stops are not failures.
8. For each form, counted the 2027 sittings whose examination clock ran while the centre's link was down: each client's loss from its NET_LOST (or its login, where it logged in with the link already down and logged only NET_BACK) to its NET_BACK or the sitting's end, kept where other clients at the centre logged the same loss (a loss one client logged alone was that workstation's own connection), overlapped with the sitting's SESSION_START to SESSION_END less its stops (in {a["hall_stops"]} every clock stopped before the router went off and restarted after the link was back); the Kochi sittings ran about four minutes on the UPS after the router went down at 11:05.

## 4. Deliverable Answers

### resit_exposure_review_2027.xlsx

1. Flagged forms, six: {words(flagged)}.
2. 2027 sittings a failure of the workstation or its power interrupted, by form, whole numbers:
{ints}
3. 2027 sittings that ran in part without the centre's link, by form, whole numbers:
{offs}

### resit_exposure_2027.pdf

1. Bar chart of every form's exposure gain per 2027 resit sitting against the 1.0 line, the six flagged forms marked.
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
