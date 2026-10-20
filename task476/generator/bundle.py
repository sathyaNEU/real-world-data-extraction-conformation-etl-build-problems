"""Readers of the shipped bundle (target/) and the golden's own path through them, for checks.py, verify.py and
ceiling.py. Nothing here imports the generator's state."""
import csv
import datetime as dt
import os

import methods as M

RATE = {1: 1.62, 2: 0.54, 3: 0.21}
LINE = 3.30
YEAR_END = dt.date(2026, 12, 31)


def find(target, prefix):
    for f in sorted(os.listdir(target)):
        if f.startswith(prefix):
            return os.path.join(target, f)
    raise FileNotFoundError(prefix)


def rows(target, prefix):
    with open(find(target, prefix), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _local(utc):
    """Central time from UTC (daylight time from the second Sunday of March to the first Sunday of November)."""
    t = dt.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
    for off in (5, 6):
        loc = t - dt.timedelta(hours=off)
        y = loc.year
        m = dt.date(y, 3, 8)
        start = m + dt.timedelta(days=(6 - m.weekday()) % 7)
        n = dt.date(y, 11, 1)
        stop = n + dt.timedelta(days=(6 - n.weekday()) % 7)
        if (start <= loc.date() < stop) == (off == 5):
            return loc
    return t - dt.timedelta(hours=6)


def grade(g):
    return {"A": 1, "B": 2, "C": 3}.get(g, None) or int(g)


def load(target, local=True):
    """Everything the inventory reads: segments, schedule, finds, odor-confirmed leaks, repairs."""
    seg = {r["segment_id"]: r for r in rows(target, "gis_main_segments")}
    sched = {}
    for r in rows(target, "leak_survey_schedule"):
        sched[(r["segment_id"], int(r["survey_year"]))] = dt.datetime.strptime(r["survey_date"], "%m/%d/%Y").date()
    leaks = {}
    for r in rows(target, "leak_survey_finds"):
        leaks[r["leak_no"]] = dict(lid=r["leak_no"], how="SURVEY", seg=r["segment_id"],
                                   found=dt.datetime.strptime(r["found_local"], "%Y-%m-%d %H:%M"), grade=grade(r["grade"]))
    odor_dates = []
    for r in rows(target, "odor_call_log"):
        if r["outcome"] != "LEAK CONFIRMED":
            continue
        t = _local(r["received_utc"]) if local else dt.datetime.strptime(r["received_utc"], "%Y-%m-%dT%H:%M:%SZ")
        leaks[r["leak_no"]] = dict(lid=r["leak_no"], how="ODOR", seg=r["segment_id"], found=t, grade=grade(r["grade"]))
        odor_dates.append(t)
    rep = {}
    first_grade = {}
    for r in rows(target, "leak_repair_orders"):
        t = dt.datetime.strptime(r["visit_local"], "%Y-%m-%d %H:%M")
        if r["action"] == "REPAIRED":
            rep[r["leak_no"]] = t
        first_grade.setdefault(r["leak_no"], (t, grade(r["grade"])))
        if t < first_grade[r["leak_no"]][0]:
            first_grade[r["leak_no"]] = (t, grade(r["grade"]))
    for k, L in leaks.items():
        L["repaired"] = rep.get(k)
        if L["grade"] is None:
            L["grade"] = first_grade[k][1] if k in first_grade else None
        s = seg[L["seg"]]
        L["district"] = s["district"]
        L["material"] = s["material"]
    return seg, sched, leaks, odor_dates


def inventory(target, route="golden", local=True, prof_years=None, prev_rule="schedule"):
    """{district: (leaks, tonnes, miles, per mile)} for leaks found in 2026 on cast-iron and bare-steel mains."""
    seg, sched, leaks, odor = load(target, local=local)
    if prof_years:
        odor = [t for t in odor if t.year in prof_years]
    prof = M.profile(odor)
    miles = {}
    for s in seg.values():
        if s["material"] in ("CAST IRON", "BARE STEEL"):
            miles[s["district"]] = miles.get(s["district"], 0.0) + int(s["length_ft"]) / 5280.0
    rs = []
    for L in leaks.values():
        if L["found"].year != 2026 or L["material"] not in ("CAST IRON", "BARE STEEL"):
            continue
        prev = sched.get((L["seg"], 2025)) if L["how"] == "SURVEY" else None
        rs.append(dict(district=L["district"], how=L["how"], found=L["found"], prev=prev, grade=L["grade"],
                       repaired=L["repaired"]))
    t = M.methane(rs, route, prof, RATE, YEAR_END)
    out = {}
    for d in miles:
        n = sum(1 for r in rs if r["district"] == d)
        out[d] = (n, t.get(d, 0.0), miles[d], t.get(d, 0.0) / miles[d])
    return out


def designated(inv):
    return sorted(d for d, v in inv.items() if v[3] >= LINE)


def ask_a(target, cumulative=True, by_leak=True):
    """Each district's leak repair cost posted in 2026. cumulative=False sums the 2026 lines as they stand; by_leak
    =False takes the cost center."""
    seg = {r["segment_id"]: r["district"] for r in rows(target, "gis_main_segments")}
    where = {}
    for r in rows(target, "leak_survey_finds"):
        where[r["leak_no"]] = seg[r["segment_id"]]
    for r in rows(target, "odor_call_log"):
        if r["leak_no"]:
            where[r["leak_no"]] = seg[r["segment_id"]]
    last = {}
    out = {}
    for r in rows(target, "work_order_cost_lines"):
        d = where[r["leak_no"]] if by_leak else r["cost_center"]
        y = int(r["posted"][:4])
        a = float(r["amount"])
        if not cumulative:
            if y == 2026:
                out[d] = out.get(d, 0.0) + a
            continue
        k = (r["wo_no"], r["cost_type"])
        last.setdefault(k, [d, {}])[1][y] = a
    if cumulative:
        for k, (d, v) in last.items():
            if 2026 in v:
                out[d] = out.get(d, 0.0) + v[2026] - v.get(2025, 0.0)
    return {d: round(v, 2) for d, v in out.items()}


def ask_b(target, meters=True, dedupe=True, by_line=True):
    """Each district's 2026 customer interruptions from leak repairs: each service address shut off for a leak
    repair, its meters counted (meters=False counts the tickets), once per leak (dedupe=False keeps both tickets
    where dispatch and the field crew each opened one)."""
    prem, on = {}, {}
    for r in rows(target, "meter_premises"):
        prem[r["service_address"]] = (int(r["meters"]), r["district"], r["service_line_id"])
        on.setdefault(r["service_line_id"], []).append((int(r["meters"]), r["district"]))
    seen = set()
    out = {}
    for r in rows(target, "service_interruption_tickets"):
        if not r["opened_local"].startswith("2026"):
            continue
        m, d, line = prem[r["service_address"]]
        k = (line if by_line else r["service_address"], r["leak_no"])
        if dedupe and k in seen:
            continue
        seen.add(k)
        if not meters:
            out[d] = out.get(d, 0) + 1
        elif by_line:
            for m2, d2 in on[line]:
                out[d2] = out.get(d2, 0) + m2
        else:
            out[d] = out.get(d, 0) + m
    return out
