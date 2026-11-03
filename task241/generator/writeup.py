"""The owed figures (figures.json), the golden note's text and submission.md, all from the solver's results."""
import json
import math
import os

import golden as GD


def pct(x):
    return int(math.floor(100.0 * x + 0.5))


def one_dp(x):
    return math.floor(10.0 * x + 0.5) / 10.0


def fmt_int(n):
    return f"{n:,}"


def fmt_h(x):
    return f"{x:,.1f}"


def answers(S):
    reg, jobs, m = S["reg"], S["jobs"], S["main"]
    names = dict(zip(reg["Job"], reg["Project"]))
    rows = []
    for i, j in enumerate(jobs):
        r = m.iloc[i]
        rows.append(dict(job=j, name=names[j], n_am=int(r["n_am"]), r_am=int(r["r_am"]), n_ab=int(r["n_ab"]),
                         r_ab=int(r["r_ab"]), share=float(r["share"]), pct=pct(r["share"]), off=bool(r["off"]),
                         outside=int(S["askA"][j]), completes=int(S["askB"][j]), hours=one_dp(float(S["askC"][j]))))
    off = [r for r in rows if r["off"]]
    on = [r for r in rows if not r["off"]]
    near_on = max(on, key=lambda r: r["share"])
    low_off = min(off, key=lambda r: r["share"])
    pilot = next(r for r in rows if r["job"] == "KR-2611")
    A = dict(rows=rows, off=[r["job"] for r in off], on=[r["job"] for r in on], near_on=near_on, low_off=low_off,
             pilot=pilot, answered=int(len(S["calls"][S["calls"]["job"].isin(jobs)])),
             off_lo=min(r["pct"] for r in off), off_hi=max(r["pct"] for r in off),
             on_lo=min(r["pct"] for r in on), on_hi=max(r["pct"] for r in on))
    A["call"] = ("Open six recurring projects in 2027 with answering machine detection switched off: " +
                 ", ".join(f"{r['job']} {r['name']}" for r in off[:-1]) + f" and {off[-1]['job']} {off[-1]['name']}"
                 + "; the other seven keep it on.")
    six = ", ".join(f"{r['job']} {GD.short(r['name'])}" for r in off[:-1]) + f" and {off[-1]['job']} {GD.short(off[-1]['name'])}"
    A["note_paragraphs"] = [
        f"Detection goes off at 2027 setup for <b>{six}</b>. In 2026 between {A['off_lo']} and "
        f"{A['off_hi']} per cent of the calls the dialer closed as answering machines on these projects had been "
        f"answered by a person, against the policy's limit of one in ten. The other seven keep detection on; their "
        f"shares ran from {A['on_lo']} to {A['on_hi']} per cent.",
        "The call detail records only what the detector decided, so the share has to be measured. A person the "
        "detector hangs up on hears the project's recorded message, and many ring the project's line straight back, "
        "nearly all within five minutes; answering machine owners ring back from their messages three quarters of an "
        "hour or more later. "
        "Abandoned live answers hear the same message and ring back at the same speed, which gives each project's own "
        "rate of calling back. Each project's share is its machine-classed calls rung back within 20 minutes, as a "
        "rate, divided by its abandoned answers' rate of ringing back within 20 minutes. Any window from 5 to 40 "
        "minutes gives the same shares.",
        "The maker's 2.1 per cent and our 2025 listening audit (9 people in 400 machine-classed calls) were measured "
        f"on short greetings on household landlines, and the pilot still reads {pilot['pct']} per cent in 2026. "
        "Detection mistakes people who answer with a long greeting, and the six projects call older households, farms "
        "and small businesses, where long greetings are common. A high machine-classed share is not the signal: "
        "large employers and retired educators have higher machine-classed shares than most of the six, and few of "
        "those calls were people.",
        f"Nearest the limit: {near_on['job']} {GD.short(near_on['name'])} at {near_on['pct']} per cent stays on; "
        f"{low_off['job']} {GD.short(low_off['name'])} at {low_off['pct']} per cent is the lowest of the six.",
    ]
    A["note_footer"] = ("Per-project counts, calling-hours exceptions, completed interviews and interviewer hours are in "
                        "amd_review_2027.xlsx.")
    return A


def figures(A):
    rows = A["rows"]
    return {
        "call": {"detection_off": A["off"], "detection_on": A["on"], "off_count": len(A["off"]),
                 "on_count": len(A["on"]), "limit_per_cent": 10},
        "components": {
            "share_per_cent": {r["job"]: r["pct"] for r in rows},
            "off_range": [A["off_lo"], A["off_hi"]], "on_range": [A["on_lo"], A["on_hi"]],
            "nearest_on": {A["near_on"]["job"]: A["near_on"]["pct"]},
            "lowest_off": {A["low_off"]["job"]: A["low_off"]["pct"]},
            "pilot_per_cent": A["pilot"]["pct"], "window_minutes": [5, 20, 40],
            "certified_per_cent": 2.1, "listening_audit": [9, 400],
            "answered_calls": A["answered"],
            "counts": {r["job"]: [r["n_am"], r["r_am"], r["n_ab"], r["r_ab"]] for r in rows},
        },
        "deliverables": {
            "outside_hours": {r["job"]: r["outside"] for r in rows},
            "completed_interviews": {r["job"]: fmt_int(r["completes"]) for r in rows},
            "interviewer_hours": {r["job"]: fmt_h(r["hours"]) for r in rows},
            "clock": [8, 21],
        },
        "pack_constants": {"test_extension": "6517", "hours_minutes_example": "4.30"},
    }


def submission(A):
    rows = A["rows"]
    off = [r for r in rows if r["off"]]
    L = []
    L.append("# task241 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: each project's "
             "error rate of a dialer's answering machine detection, measured from what the people it hung up on did next).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting (which recurring telephone projects have the "
             "dialer's answering machine detection switched off for 2027 because the answering-machine outcomes it "
             "records are not trustworthy, with each project's calling-hours exceptions, completed interviews and "
             "interviewer hours for the 2027 setup).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**" + A["call"] + "**\n")
    L.append(f"On the six, {A['off_lo']} to {A['off_hi']}% of the calls the dialer classed as answering machines in 2026 "
             f"had been answered by a person, against the 2027 policy's one in ten; the other seven ran {A['on_lo']} to "
             f"{A['on_hi']}%. Not the maker's certified 2.1% or the 2025 listening audit's 9 of 400, which describe the "
             "pilot's short household greetings and keep every project on. Not the four projects with the highest "
             "machine-classed shares, which picks large employers and retired educators for ordinary voicemail.\n")
    L.append("## 2. Critical Components\n")
    L.append("1. Each project's share of machine-classed calls answered by a person, measured on its own calls: " +
             "; ".join(f"{r['job']} **{r['pct']}%**" for r in rows) + ".")
    L.append(f"2. Nearest the limit: {A['near_on']['job']} at **{A['near_on']['pct']}%** stays on; "
             f"{A['low_off']['job']} at **{A['low_off']['pct']}%** is the lowest switched off.")
    L.append(f"3. The pilot, KR-2611, reads **{A['pilot']['pct']}%**, in line with the 2025 listening audit; people "
             "who ring back mostly do so within five minutes and machine owners three quarters of an hour or more "
             "later, so every window from 5 to 40 minutes gives the same shares.\n")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read the twelve exports in dialer_exports (letter codes and US dates to June, words and ISO dates from "
             "July) and dropped the day each export repeats from the month before by call id.")
    L.append("2. Collapsed inbound_switch_2026.csv to one call per switch_call_id (its first leg's time and caller), "
             "dropped the test calls from extension 6517 and tied each call from a dialed number to the latest outbound "
             "call to that number, numbers normalised to ten digits.")
    L.append("3. For each project in project_register_2027.xlsx, divided the share of its machine-classed calls rung "
             "back within 20 minutes by the share of its abandoned live answers rung back within 20 minutes.")
    L.append("4. Applied section 3 of dialer_policy_2027.docx: detection off where the share is one in ten or more, six "
             "projects; on for the other seven.")
    L.append("5. Calling hours: each answered call's household state from case_records_2026.csv, by the number dialed, "
             "else by the case number the dialer wrote from July, else (an appointment number the record lacks, before "
             "July) through the same case's calls to its recorded number; Central time converted with "
             "state_time_zones.csv, Arizona on standard time all year; counted calls before 8:00 or from 21:00 local.")
    L.append("6. Completed interviews: the dialer's COMPLETE rows and the inbound calls with COMPLETE on any leg, each "
             "case counted once across the July case-number change (matched to its case record), a supervisor's "
             "verification call adding none (policy section 5).")
    L.append("7. Interviewer hours: interviewer_hours_2026_h1.csv (decimal hours) and interviewer_hours_2026_h2.csv "
             "(hours.minutes, 4.30 being four and a half hours), each shift's hours shared by each project's talk and "
             "wrap time on the interviewer's calls inside the shift, shifts with no calls not charged (policy section 5).")
    L.append("8. Detection is switched off for 2027 on " + ", ".join(r["job"] for r in off[:-1]) + f" and {off[-1]['job']}.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### amd_review_2027.xlsx\n")
    L.append("1. Each project's 2026 share of machine-classed calls answered by a person (whole per cent) and its 2027 "
             "detection:")
    for r in rows:
        L.append(f"   - {r['job']} {r['name']}: {r['pct']}%, detection {'off' if r['off'] else 'on'}")
    L.append("2. Answered calls in 2026 that rang before 8 am or after 9 pm in the called household's own local time:")
    for r in rows:
        L.append(f"   - {r['job']}: {r['outside']}")
    L.append("3. Interviews completed in 2026:")
    for r in rows:
        L.append(f"   - {r['job']}: {fmt_int(r['completes'])}")
    L.append("4. Interviewer hours used in 2026 (one decimal place):")
    for r in rows:
        L.append(f"   - {r['job']}: {fmt_h(r['hours'])}")
    L.append("")
    L.append("### amd_review_2027.pdf\n")
    L.append("5. One-page note: detection switched off for " + ", ".join(r["job"] for r in off[:-1]) +
             f" and {off[-1]['job']} because a tenth or more of their machine-classed calls were people, measured from "
             "the calls rung back within minutes against each project's abandoned answers; the certified rate and "
             "the listening audit hold only for short household greetings; a bar chart of the projects' shares "
             "against the one-in-ten limit.")
    return "\n".join(L) + "\n"


def write(task, here, A):
    fig = figures(A)
    with open(os.path.join(here, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
