"""task241 independent verifier: reads only the shipped bundle (target/), the goldens, figures.json and submission.md,
recomputes the call and every ask by its own code (bisection for the return calls, fixed offsets and the 2026 clock
changes for local time, its own payroll parser and shift walk), and requires the goldens and the write-up to carry
the same figures."""
import bisect
import csv
import datetime as dt
import glob
import json
import os
import re
import sys

from openpyxl import load_workbook

CODES = dict(C="COMPLETE", P="PARTIAL", R="REFUSAL", B="CALLBACK", I="INELIGIBLE", L="LANGUAGE", H="HANGUP", D="DNC",
             A="AMD_MACHINE", X="ABANDONED", AA="AGENT_MACHINE")
DST_ON, DST_OFF = dt.datetime(2026, 3, 8, 2, 0), dt.datetime(2026, 11, 1, 2, 0)   # US clock changes, local time
STD = {"Eastern": -5, "Central": -6, "Mountain": -7, "Mountain (Arizona)": -7, "Pacific": -8}
AREA = {"218": "MN", "320": "MN", "507": "MN", "612": "MN", "651": "MN", "763": "MN", "952": "MN", "608": "WI",
        "715": "WI", "515": "IA", "712": "IA", "701": "ND", "605": "SD"}


def ten(s):
    d = re.sub(r"\D", "", s)
    return d[-10:] if len(d) >= 10 else ""


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_calls(target):
    seen, out = set(), []
    for p in sorted(glob.glob(os.path.join(target, "dialer_exports", "*.csv"))):
        for r in rows(p):
            if "CallID" in r:
                x = dict(id=r["CallID"], job=r["JobNo"], phone=ten(r["Phone"]), case=r["CaseID"],
                         placed=dt.datetime.strptime(r["CallStart"], "%m/%d/%Y %H:%M:%S"), agent=r["AgentID"],
                         outcome=CODES[r["Disp"]], sec=int(r["TalkSec"]) + int(r["WrapSec"]), talk=int(r["TalkSec"]),
                         ended=dt.datetime.strptime(r["CallEnd"], "%m/%d/%Y %H:%M:%S"))
            else:
                x = dict(id=r["call_id"], job=r["job"], phone=ten(r["dialed_number"]), case=r["case_number"],
                         placed=dt.datetime.fromisoformat(r["placed_at"]), agent=r["agent"], outcome=r["outcome"],
                         sec=int(r["talk_seconds"]) + int(r["wrap_seconds"]), talk=int(r["talk_seconds"]),
                         ended=dt.datetime.fromisoformat(r["ended_at"]))
            if x["id"] not in seen:
                seen.add(x["id"])
                out.append(x)
    return out


def central_offset(t):
    return -5 if DST_ON <= t < DST_OFF else -6


def local(t, zone):
    utc = t - dt.timedelta(hours=central_offset(t))
    off = STD[zone]
    if zone != "Mountain (Arizona)":
        # the clock change happens at 2 am local in every zone; no call sits near one
        loc_std = utc + dt.timedelta(hours=off)
        if DST_ON <= loc_std < DST_OFF:
            off += 1
    return utc + dt.timedelta(hours=off)


def main(target, golden, figures, submission):
    fig = json.load(open(figures))
    reg = load_workbook(os.path.join(target, "project_register_2027.xlsx"), data_only=True).active
    jobs, line = [], {}
    for r in reg.iter_rows(min_row=4, values_only=True):
        if r[0] and str(r[0]).startswith("KR-"):
            jobs.append(r[0])
            line["+1" + ten(str(r[4]))] = r[0]
    calls = read_calls(target)
    # the main call
    by_phone = {}
    for c in calls:
        by_phone.setdefault(c["phone"], []).append((c["ended"], c["job"], c["outcome"]))
    for v in by_phone.values():
        v.sort()
    inb = rows(os.path.join(target, "inbound_switch_2026.csv"))
    first = [r for r in inb if r["leg"] == "1" and r["caller"].startswith("+1")]
    r_am, r_ab = {j: 0 for j in jobs}, {j: 0 for j in jobs}
    for r in first:
        ph, st = ten(r["caller"]), dt.datetime.fromisoformat(r["started"])
        lst = by_phone.get(ph)
        if not lst:
            continue
        k = bisect.bisect_right(lst, (st, "~", "~")) - 1
        if k < 0:
            continue
        ended, job, outcome = lst[k]
        if job in r_am and (st - ended).total_seconds() <= 1200:
            if outcome == "AMD_MACHINE":
                r_am[job] += 1
            elif outcome == "ABANDONED":
                r_ab[job] += 1
    n_am = {j: sum(1 for c in calls if c["job"] == j and c["outcome"] == "AMD_MACHINE") for j in jobs}
    n_ab = {j: sum(1 for c in calls if c["job"] == j and c["outcome"] == "ABANDONED") for j in jobs}
    share = {j: (r_am[j] / n_am[j]) / (r_ab[j] / n_ab[j]) for j in jobs}
    off = sorted(j for j in jobs if share[j] >= 0.10)
    assert off == sorted(fig["call"]["detection_off"]), ("verify: the call", off)
    for j in jobs:
        assert int(100 * share[j] + 0.5) == fig["components"]["share_per_cent"][j], ("verify: share", j)
        assert [n_am[j], r_am[j], n_ab[j], r_ab[j]] == fig["components"]["counts"][j], ("verify: counts", j)
    # case records and the household behind each call
    cases = rows(os.path.join(target, "case_records_2026.csv"))
    st_phone = {ten(r["phone"]): r["address_state"] for r in cases}
    st_case = {r["case_number"]: r["address_state"] for r in cases}
    id_phone = {ten(r["phone"]): r["case_number"] for r in cases}
    old_state, old_id = {}, {}
    for c in calls:
        if not re.fullmatch(r"\d{4}-\d{6}", c["case"]) and c["phone"] in st_phone:
            old_state.setdefault((c["job"], c["case"]), st_phone[c["phone"]])
            old_id.setdefault((c["job"], c["case"]), id_phone[c["phone"]])

    def household(c):
        if c["phone"] in st_phone:
            return st_phone[c["phone"]], id_phone[c["phone"]]
        if c["case"] in st_case:
            return st_case[c["case"]], c["case"]
        return old_state[(c["job"], c["case"])], old_id[(c["job"], c["case"])]

    zones = {r["state"]: r["time_zone"] for r in rows(os.path.join(target, "state_time_zones.csv"))}
    outside = {j: 0 for j in jobs}
    for c in calls:
        if c["job"] in outside:
            t = local(c["placed"], zones[household(c)[0]])
            h = t.hour + t.minute / 60 + t.second / 3600
            outside[c["job"]] += int(h < 8 or h >= 21)
    assert outside == fig["deliverables"]["outside_hours"], ("verify: ask A", outside)
    # completed interviews
    done = set()
    phone_id = dict(id_phone)
    for c in calls:
        phone_id.setdefault(c["phone"], household(c)[1])
        if c["job"] in outside and c["outcome"] == "COMPLETE":
            done.add((c["job"], household(c)[1]))
    legs = {}
    for r in inb:
        legs.setdefault(r["switch_call_id"], []).append(r)
    for sid, lg in legs.items():
        l1 = [x for x in lg if x["leg"] == "1"][0]
        if l1["caller"].startswith("+1") and l1["started"] < "2027-01-01" and any(x["wrap_code"] == "COMPLETE" for x in lg):
            if l1["dialed_line"] in line:
                done.add((line[l1["dialed_line"]], phone_id[ten(l1["caller"])]))
    comp = {j: sum(1 for (jj, _) in done if jj == j) for j in jobs}
    assert {j: f"{v:,}" for j, v in comp.items()} == fig["deliverables"]["completed_interviews"], ("verify: ask B", comp)
    # interviewer hours
    shifts = []
    for r in rows(os.path.join(target, "interviewer_hours_2026_h1.csv")):
        shifts.append((r["Employee"], dt.datetime.strptime(r["Work Date"] + " " + r["Time In"], "%m/%d/%Y %H:%M"),
                       float(r["Hours"])))
    for r in rows(os.path.join(target, "interviewer_hours_2026_h2.csv")):
        h, mnt = r["paid_hours"].split(".")
        shifts.append((r["employee"], dt.datetime.fromisoformat(r["shift_date"] + " " + r["clock_in"]), int(h) + int(mnt) / 60))
    mine = {}
    for c in calls:
        if c["agent"] and c["talk"] > 0:
            mine.setdefault((c["agent"], c["placed"].date()), []).append(c)
    hours = {j: 0.0 for j in jobs}
    for who, t0, h in shifts:
        t1 = t0 + dt.timedelta(hours=h)
        sec = {}
        for c in mine.get((who, t0.date()), []):
            if t0 <= c["placed"] < t1:
                sec[c["job"]] = sec.get(c["job"], 0) + c["sec"]
        tot = sum(sec.values())
        for j, s in sec.items():
            if j in hours:
                hours[j] += h * s / tot
    got = {j: f"{int(10 * v + 0.5) / 10:,.1f}" for j, v in hours.items()}
    assert got == fig["deliverables"]["interviewer_hours"], ("verify: ask C", got)
    # the goldens and the write-up carry the same figures
    ws = load_workbook(os.path.join(golden, "amd_review_2027.xlsx"), data_only=True)["2027 setup"]
    seen = 0
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] in share:
            j = r[0]
            assert round(r[6] * 100) == fig["components"]["share_per_cent"][j] and (r[7] == "Off") == (j in off)
            assert r[8] == outside[j] and r[9] == comp[j] and f"{r[10]:,.1f}" == got[j], ("verify: workbook", j)
            seen += 1
    assert seen == len(jobs)
    sub = open(submission).read()
    for j in jobs:
        assert f"{j}: {outside[j]}\n" in sub and f"{j}: {comp[j]:,}\n" in sub and f"{j}: {got[j]}\n" in sub, j
        assert re.search(r"%s [^\n]*: %d%%, detection %s" % (j, fig["components"]["share_per_cent"][j],
                                                            "off" if j in off else "on"), sub), j
    pdf = open(os.path.join(golden, "amd_review_2027.pdf"), "rb").read()
    assert pdf.startswith(b"%PDF") and pdf.count(b"/Type /Page\n") + pdf.count(b"/Type /Page ") + pdf.count(b"/Type /Page/") >= 1
    print("verify: the call (%d off), %d shares, the three asks, the workbook and the write-up agree" % (len(off), len(jobs)))


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(task, "target"), os.path.join(task, "golden"),
         os.path.join(task, "generator", "figures.json"), os.path.join(task, "submission.md"))
