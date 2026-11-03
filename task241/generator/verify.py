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
ZT = {}       # the shipped time zone table: zone, standard offset, daylight offset, 2026 clock changes (local time)


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
                         answered=dt.datetime.strptime(r["AnswerTime"], "%m/%d/%Y %H:%M:%S"),
                         outcome=CODES[r["Disp"]], sec=int(r["TalkSec"]) + int(r["WrapSec"]), talk=int(r["TalkSec"]),
                         ended=dt.datetime.strptime(r["CallEnd"], "%m/%d/%Y %H:%M:%S"))
            else:
                x = dict(id=r["call_id"], job=r["job"], phone=ten(r["dialed_number"]), case=r["case_number"],
                         placed=dt.datetime.fromisoformat(r["placed_at"]), agent=r["agent"], outcome=r["outcome"],
                         answered=dt.datetime.fromisoformat(r["answered_at"]),
                         sec=int(r["talk_seconds"]) + int(r["wrap_seconds"]), talk=int(r["talk_seconds"]),
                         ended=dt.datetime.fromisoformat(r["ended_at"]))
            if x["id"] not in seen:
                seen.add(x["id"])
                out.append(x)
    return out


def load_zones(target):
    for r in rows(os.path.join(target, "state_time_zones.csv")):
        on = dt.datetime.fromisoformat(r["daylight_time_begins_2026"]) if r["daylight_time_begins_2026"] else None
        off = dt.datetime.fromisoformat(r["daylight_time_ends_2026"]) if r["daylight_time_ends_2026"] else None
        ZT[r["state"]] = (r["time_zone"], int(r["utc_offset_standard"]), int(r["utc_offset_daylight"]), on, off,
                          r["other_zone_areas"])


def offset(state, loc_std):
    zone, std, dst, on, off, _ = ZT[state]
    return dst if on and on <= loc_std < off else std


def local(t, state):
    """a Central clock reading taken to the household state's own clock, by the table's offsets and dates"""
    utc = t - dt.timedelta(hours=offset("MN", t - dt.timedelta(hours=0)))
    std = ZT[state][1]
    return utc + dt.timedelta(hours=offset(state, utc + dt.timedelta(hours=std)))


def docx_text(path):
    import zipfile
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return " ".join("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in re.findall(r"<w:p[ >].*?</w:p>", x, re.S))


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
    # the same tie at every window from 2 to 150 minutes, from the call's end and from its start
    by_start = {}
    for c in calls:
        by_start.setdefault(c["phone"], []).append((c["placed"], c["job"], c["outcome"]))
    for v_ in by_start.values():
        v_.sort()
    spread = set()
    for anchor in (by_phone, by_start):
        for w in (2, 3, 5, 10, 20, 40, 60, 90, 120, 150):
            ca, cb = {j: 0 for j in jobs}, {j: 0 for j in jobs}
            for r in first:
                lst = anchor.get(ten(r["caller"]))
                st = dt.datetime.fromisoformat(r["started"])
                if not lst:
                    continue
                k = bisect.bisect_right(lst, (st, "~", "~")) - 1
                if k >= 0 and lst[k][1] in ca and (st - lst[k][0]).total_seconds() <= 60 * w:
                    if lst[k][2] == "AMD_MACHINE":
                        ca[lst[k][1]] += 1
                    elif lst[k][2] == "ABANDONED":
                        cb[lst[k][1]] += 1
            spread.add(tuple(ca[j] for j in jobs) + tuple(cb[j] for j in jobs))
    n_am = {j: sum(1 for c in calls if c["job"] == j and c["outcome"] == "AMD_MACHINE") for j in jobs}
    n_ab = {j: sum(1 for c in calls if c["job"] == j and c["outcome"] == "ABANDONED") for j in jobs}
    share = {j: (r_am[j] / n_am[j]) / (r_ab[j] / n_ab[j]) for j in jobs}
    assert spread == {tuple(r_am[j] for j in jobs) + tuple(r_ab[j] for j in jobs)}, "verify: the window moves a count"
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

    load_zones(target)
    outside, outside_ans = {j: 0 for j in jobs}, {j: 0 for j in jobs}
    for c in calls:
        if c["job"] in outside:
            st = household(c)[0]
            assert ZT[st][5] == "", ("verify: a household in a state split between zones", st)
            for key, tally in (("placed", outside), ("answered", outside_ans)):
                t = local(c[key], st)
                h = t.hour + t.minute / 60 + t.second / 3600
                tally[c["job"]] += int(h < 8 or h >= 21)
    assert outside == fig["deliverables"]["outside_hours"], ("verify: ask A", outside)
    assert outside_ans == outside, ("verify: ask A moves when the ring is read at the answer", outside_ans)
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
    late = set()
    for sid, lg in legs.items():
        l1 = [x for x in lg if x["leg"] == "1"][0]
        if l1["caller"].startswith("+1") and l1["started"] >= "2027-01-01" and any(x["wrap_code"] == "COMPLETE" for x in lg):
            late.add(sid)
    assert late, "verify: the switch log's January 2027 interviews"
    # the golden's 2026 window is the only difference from counting every COMPLETE in the log: each 2027 interview adds
    # exactly one case to its own project and nothing else moves
    with_late = set(done)
    late_by_job = {j: 0 for j in jobs}
    for sid in late:
        l1 = [x for x in legs[sid] if x["leg"] == "1"][0]
        j = line.get(l1["dialed_line"])
        if j:
            with_late.add((j, phone_id[ten(l1["caller"])]))
            late_by_job[j] += 1
    comp_late = {j: sum(1 for (jj, _) in with_late if jj == j) for j in jobs}
    assert all(comp_late[j] - comp[j] == late_by_job[j] for j in jobs), ("verify: the 2027 interviews", comp_late)
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
    # the documents the call and the asks lean on, read back from the pack
    pol = docx_text(os.path.join(target, "dialer_policy_2027.docx"))
    assert "fewer than one in ten of the calls the dialer classed as answering machines on that project in 2026" in pol
    assert "Calls ring only between 8 am and 9 pm in the called household's own local time" in pol
    assert "stamp every call in the centre's own local time (Central time, with daylight saving time)" in pol
    assert "An interview counts once, when it is completed." in pol
    assert "in proportion to each project's talk and wrap time" in pol
    assert ZT["MN"][3] == dt.datetime(2026, 3, 8, 2, 0) and ZT["AZ"][3] is None, "verify: the table's clock changes"
    wb = load_workbook(os.path.join(target, "project_register_2027.xlsx"), data_only=True)
    closed = [r for r in wb["Closed 2026 jobs"].iter_rows(min_row=2, values_only=True) if r[0]]
    assert closed and all(r[0] not in jobs and "not recurring" in r[3] for r in closed), "verify: the closed jobs"
    seen_jobs = {c["job"] for c in calls}
    assert seen_jobs == set(jobs) | {r[0] for r in closed}, ("verify: a dialer job on neither sheet", seen_jobs)
    from pypdf import PdfReader
    spec = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, "larkspur_amd_release6.pdf"), strict=True).pages)
    assert "Balanced (default) 2.1%" in spec.replace("\n", " ") and "collected in 2023" in spec, "verify: the maker's sheet"
    pdf = open(os.path.join(golden, "amd_review_2027.pdf"), "rb").read()
    assert pdf.startswith(b"%PDF") and pdf.count(b"/Type /Page\n") + pdf.count(b"/Type /Page ") + pdf.count(b"/Type /Page/") >= 1
    print("verify: the call (%d off), %d shares, the three asks, the workbook and the write-up agree" % (len(off), len(jobs)))


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(task, "target"), os.path.join(task, "golden"),
         os.path.join(task, "generator", "figures.json"), os.path.join(task, "submission.md"))
