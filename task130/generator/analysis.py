"""The golden, computed from target/ alone: the case records stacked and revised, each case on the injured worker's
crew or team on the day, the hours worked on Pinewater work, each crew's position in its 90-day recognition count
day by day, the rate crews record where the count exerts no pull, the 2027 forecast on the work plan, the rungs a
competent solver stops at, and the asks."""
import collections
import csv
import datetime as dt
import os
import sys

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P   # noqa: E402  (file names only)
import world as W  # noqa: E402  (the 2027 limit and the rate base, both filed in CS-4)

K = 200000
ONE = dt.timedelta(days=1)
ASK0, ASK1 = dt.date(2026, 1, 5), dt.date(2026, 9, 27)
CREW_TYPES = ("OH", "UG", "SUB", "VEG")
TECH_TYPES = ("MTR", "LOC")
CLEAN = 35            # cycle days 0 to 34: the stretch of each count before reporting falls away
PROGRAMME_START = dt.date(2021, 1, 11)   # HR-14 Revision 2: every crew's count started on this day
QUARTERS = ((ASK0, dt.date(2026, 3, 31)), (dt.date(2026, 4, 1), dt.date(2026, 6, 30)), (dt.date(2026, 7, 1), ASK1))
MATCH_DAYS = 3        # a nurse-line call comes on the day of the injury or up to three days after it
SEVERITY = {"FA": 0, "MT": 1, "RW": 2, "DA": 3}


def d(s):
    return dt.date.fromisoformat(s)


def mdy(s):
    m, dd, y = s.split("/")
    return dt.date(int(y), int(m), int(dd))


def load(target):
    p = lambda k: os.path.join(target, P.FILES[k])
    legacy = list(csv.DictReader(open(p("legacy"), newline="")))
    ws = openpyxl.load_workbook(p("cases"), read_only=True)["Cases"]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    new = [dict(zip(head, r)) for r in it]
    assign = list(csv.DictReader(open(p("assign"), newline="")))
    ws = openpyxl.load_workbook(p("register"), read_only=True)["Crews"]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    register = [dict(zip(head, r)) for r in it]
    hours = list(csv.DictReader(open(p("hours"), newline="")))
    ws = openpyxl.load_workbook(p("plan"), read_only=True)["2027 hours"]
    plan = {}
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] in W.DISTRICTS:
            plan[(r[0], r[1])] = [float(x) for x in r[2:6]]
    return dict(legacy=legacy, new=new, assign=assign, register=register, hours=hours, plan=plan)


def cases(D):
    """One row per case, as the case record finally classifies it: the legacy log's latest revision for cases that
    never reached the new system, the new system's latest revision for every other."""
    CL = {"First aid": "FA", "Medical treatment": "MT", "Restricted work": "RW", "Days away": "DA"}
    migrated = {r["legacy_case_no"] for r in D["new"] if r["legacy_case_no"]}
    last = {}
    for r in D["legacy"]:
        if r["case_no"] in migrated:
            continue
        k = ("L", r["case_no"])
        if k not in last or int(r["revision"]) > last[k]["rev"]:
            last[k] = dict(rev=int(r["revision"]), emp=r["employee_no"], date=mdy(r["injury_date"]),
                           job=r["job_ref"], cls=CL[r["classification"]], recur=bool(r["recurrence_of"]), loc=r["district"],
                           source="Supervisor", body=r["body_part"], nature=r["nature"])
    for r in D["new"]:
        k = ("N", r["case_id"])
        if k not in last or int(r["revision"]) > last[k]["rev"]:
            last[k] = dict(rev=int(r["revision"]), emp=r["employee_id"], date=d(str(r["injury_date"])[:10]),
                           job=r["job_reference"], cls=r["osha_class"], recur=bool(r["recurrence_of_case"]), loc=r["district"],
                           source=r["source"], body=r["body_part"], nature=r["nature_of_injury"])
    out = [dict(v, case=k[1]) for k, v in sorted(last.items())]
    for c in out:
        c["pinewater"] = not c["job"].startswith("MA-")
    return out


def new_cases(cs):
    """Recurrences (29 CFR 1904.6) are not new cases."""
    return [c for c in cs if not c["recur"]]


def units(D):
    info, canon = {}, {}
    for r in D["register"]:
        info[r["unit_code"]] = dict(type=r["unit_type"], district=r["district"])
    for r in D["register"]:
        if r["status"] == "Recoded":
            canon[r["unit_code"]] = r["recoded_to"]
    return info, canon


def assignment_lookup(D):
    by_emp = collections.defaultdict(list)
    for r in D["assign"]:
        by_emp[r["employee_id"]].append((d(r["assigned_from"]), d(r["assigned_to"]) if r["assigned_to"] else None,
                                         r["crew_or_team"]))

    def at(emp, day):
        for a, b, code in by_emp[emp]:
            if a <= day and (b is None or day <= b):
                return code
        return None
    return at


def attach(cs, D):
    info, canon = units(D)
    at = assignment_lookup(D)
    for c in cs:
        code = at(c["emp"], c["date"])
        c["code"] = code
        c["canon"] = canon.get(code, code)
        c["type"] = info[code]["type"]
        c["district"] = info[code]["district"]
        c["crew"] = c["type"] in CREW_TYPES
    return cs


def working_days(ps):
    out = []
    for k in range(14):
        day = ps + dt.timedelta(days=k)
        if day.weekday() < 5 and day not in W.holidays(day.year):
            out.append(day)
    return out


def hours_by(D):
    """Hours worked on Pinewater work (regular and overtime) per unit and pay period."""
    info, canon = units(D)
    rows = []
    for r in D["hours"]:
        w = float(r["regular_hours"]) + float(r["overtime_hours"])
        ps = d(r["adjusts_pay_period"]) if r["adjusts_pay_period"] else d(r["pay_period_start"])
        # CS-4 3.6: the district of the crew or team, not the district the hours were worked in
        rows.append(dict(ps=ps, code=r["unit_code"], canon=canon.get(r["unit_code"], r["unit_code"]),
                         district=info[r["unit_code"]]["district"], work_district=r["district"], type=r["unit_type"],
                         worked=w, aid=float(r["mutual_aid_hours"])))
    return rows


def cycles(cs, D, H, origin="programme", carry=True):
    """Each crew's position in its 90-day count, day by day: HR-14 Revision 2 started every count on 11 January 2021,
    and a count restarts on the day after a recordable injury to any member and on the day after its 90th day.
    Returns, per cycle day, the Pinewater hours worked (each pay period's hours spread over its working days) and the
    recordables on Pinewater work."""
    info, canon = units(D)
    key = "canon" if carry else "code"      # carry=False: a recoded crew read as a new crew (a stress reading)
    resets = collections.defaultdict(set)
    for c in cs:
        if c["crew"] and c["cls"] != "FA":
            resets[c[key]].add(c["date"])
    per_day = collections.defaultdict(dict)
    for h in H:
        if h["type"] not in CREW_TYPES or h["worked"] <= 0:
            continue
        wd = working_days(h["ps"])
        for day in wd:
            per_day[h[key]][day] = per_day[h[key]].get(day, 0.0) + h["worked"] / len(wd)
    exp = np.zeros(W.MILESTONE)
    cnt = np.zeros(W.MILESTONE)
    cnt_cls = collections.defaultdict(lambda: np.zeros(W.MILESTONE))
    by_type_exp = collections.defaultdict(lambda: np.zeros(W.MILESTONE))
    by_type_cnt = collections.defaultdict(lambda: np.zeros(W.MILESTONE))
    pine = collections.defaultdict(list)
    for c in cs:
        if c["crew"] and c["cls"] != "FA" and c["pinewater"]:
            pine[c[key]].append(c)
    for crew in sorted(per_day):
        ctype = info[crew]["type"]
        start = PROGRAMME_START if carry else max(PROGRAMME_START, min(per_day[crew]))
        if origin == "first":       # a stress reading: positions known only from the crew's first recordable
            if not resets[crew]:
                continue
            start = min(resets[crew]) + ONE
        day = start
        last_day = max(per_day[crew])
        rset = resets[crew]
        pos = {}
        while day <= last_day:
            n = (day - start).days
            pos[day] = n
            if day in rset or n == W.MILESTONE - 1:
                start = day + ONE
            day += ONE
        for dd_, h in per_day[crew].items():
            if dd_ in pos:
                exp[pos[dd_]] += h
                by_type_exp[ctype][pos[dd_]] += h
        for c in pine[crew]:
            if c["date"] in pos:
                cnt[pos[c["date"]]] += 1
                cnt_cls[c["cls"]][pos[c["date"]]] += 1
                by_type_cnt[ctype][pos[c["date"]]] += 1
    return dict(exp=exp, cnt=cnt, cls=dict(cnt_cls), type_exp=dict(by_type_exp), type_cnt=dict(by_type_cnt))


def rates(cs, H, a, b, crew=None, types=None):
    hrs = sum(h["worked"] for h in H if a <= h["ps"] and h["ps"] + dt.timedelta(days=13) <= b
              and (types is None or h["type"] in types))
    n = sum(1 for c in cs if a <= c["date"] <= b and c["cls"] != "FA" and c["pinewater"]
            and (types is None or c["type"] in types))
    return n, hrs, (n * K / hrs if hrs else float("nan"))


def forecast(plan, crew_rate, tech_rate, by_type=None):
    q = np.zeros(4)
    hq = np.zeros(4)
    for (dist, t), hrs in plan.items():
        r = (by_type or {}).get(t, crew_rate if t in CREW_TYPES else tech_rate)
        for k in range(4):
            q[k] += r * hrs[k] / K
            hq[k] += hrs[k]
    return q, hq


def injuries(cs, match_days=MATCH_DAYS):
    """One record per injury. A nurse-line case is the injury of the one supervisor's case of the same worker dated
    up to match_days days before it, which classifies it; a nurse-line case with no such case is an injury of its
    own. match_days=None groups the records on worker and injury date instead (the duplicate check a careful
    solver runs), each group taking its most serious class."""
    if match_days is None:
        groups = collections.defaultdict(list)
        for c in cs:
            groups[(c["emp"], c["date"])].append(c)
        out = []
        for k in sorted(groups):
            g = sorted(groups[k], key=lambda c: (-SEVERITY[c["cls"]], c["source"] == "Nurse line", c["case"]))
            out.append(g[0])
        return out
    sup = collections.defaultdict(list)
    for c in cs:
        if c["source"] != "Nurse line":
            sup[c["emp"]].append(c)
    out = [c for c in cs if c["source"] != "Nurse line"]
    for c in cs:
        if c["source"] == "Nurse line":
            if not any(0 <= (c["date"] - x["date"]).days <= match_days for x in sup[c["emp"]]):
                out.append(c)
    return out


def asks(D, cs, match_days=MATCH_DAYS):
    """CS-4 4(c)'s first-aid cases for 5 January to 27 September 2026: field employees on Pinewater work, each
    injury once, in the quarter of its injury date and the district of the worker's crew or team on that day.
    cs is every case record at its latest revision, recurrences included, each attached to its crew or team."""
    T = {dist: [0, 0, 0] for dist in W.DISTRICTS}
    for c in injuries(cs, match_days):
        if c["cls"] != "FA" or not c["pinewater"] or c["recur"]:
            continue
        for q, (a, b) in enumerate(QUARTERS):
            if a <= c["date"] <= b:
                T[c["district"]][q] += 1
    return {dist: dict(quarters=v, total=sum(v)) for dist, v in T.items()}


def main(target):
    D = load(target)
    cs = attach(new_cases(cases(D)), D)
    H = hours_by(D)
    plan = D["plan"]
    a0, a1 = W.HIST0, W.HIST1
    n_c, h_c, r_c = rates(cs, H, a0, a1, types=CREW_TYPES)
    n_t, h_t, r_t = rates(cs, H, a0, a1, types=TECH_TYPES)
    n_a, h_a, r_a = rates(cs, H, a0, a1)
    cyc = cycles(cs, D, H)
    exp, cnt = cyc["exp"], cyc["cnt"]
    clean = cnt[:CLEAN].sum() * K / exp[:CLEAN].sum()
    windows = {w: cnt[:w].sum() * K / exp[:w].sum() for w in (20, 25, 30, 35, 40)}
    by_type_clean = {t: cyc["type_cnt"][t][:CLEAN].sum() * K / cyc["type_exp"][t][:CLEAN].sum() for t in CREW_TYPES}
    bins = [(lo, hi, cnt[lo:hi].sum(), exp[lo:hi].sum(), cnt[lo:hi].sum() * K / exp[lo:hi].sum())
            for lo, hi in ((0, 15), (15, 35), (35, 50), (50, 65), (65, 90))]
    da_bins = [(lo, hi, cyc["cls"].get("DA", np.zeros(90))[lo:hi].sum() * K / exp[lo:hi].sum())
               for lo, hi in ((0, 35), (35, 60), (60, 90))]
    q, hq = forecast(plan, clean, r_t)
    total = float(q.sum())
    hours27 = float(hq.sum())
    gold = dict(total=total, rate=total * K / hours27, quarters=[float(x) for x in q],
                quarter_rates=[float(q[k] * K / hq[k]) for k in range(4)], hours=hours27,
                quarter_hours=[float(x) for x in hq], clean=clean, tech=r_t)
    # the rungs
    by_type_rec = {}
    for t in CREW_TYPES + TECH_TYPES:
        by_type_rec[t] = rates(cs, H, a0, a1, types=(t,))[2]
    r0_q, _ = forecast(plan, r_c, r_t, by_type=by_type_rec)
    r0 = float(r0_q.sum())
    r0_pooled = r_a * hours27 / K
    trail = rates(cs, H, dt.date(2025, 9, 29), a1)
    r0_trail = trail[2] * hours27 / K
    r3 = {w: float(forecast(plan, v, r_t)[0].sum()) for w, v in windows.items()}
    r3_type = float(forecast(plan, clean, r_t, by_type=dict(by_type_clean, MTR=by_type_rec["MTR"],
                                                            LOC=by_type_rec["LOC"]))[0].sum())
    da_share = dict(crew=sum(1 for c in cs if c["crew"] and c["cls"] == "DA" and c["pinewater"])
                    / max(1, sum(1 for c in cs if c["crew"] and c["cls"] != "FA" and c["pinewater"])),
                    tech=sum(1 for c in cs if not c["crew"] and c["cls"] == "DA")
                    / max(1, sum(1 for c in cs if not c["crew"] and c["cls"] != "FA")))
    A = asks(D, attach(cases(D), D))
    return dict(gold=gold, windows=windows, r3=r3, r3_type=r3_type, by_type_clean=by_type_clean,
                by_type_rec=by_type_rec, recorded=dict(crew=r_c, tech=r_t, all=r_a, n_crew=n_c, n_tech=n_t,
                                                       h_crew=h_c, h_tech=h_t),
                r0=r0, r0_pooled=r0_pooled, r0_trail=r0_trail, trail=trail, bins=bins, da_bins=da_bins,
                da_share=da_share, asks=A, cases=cs, plan=plan)


if __name__ == "__main__":
    F = main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    g = F["gold"]
    print("golden: %.1f recordables, rate %.3f on %.0f hours; quarters %s" % (g["total"], g["rate"], g["hours"],
          [round(x, 1) for x in g["quarters"]]))
    print("clean crew rate %.3f; windows %s; by type %s" % (g["clean"], {k: round(v, 3) for k, v in F["windows"].items()},
          {k: round(v, 3) for k, v in F["by_type_clean"].items()}))
    print("recorded crew %.3f tech %.3f all %.3f" % (F["recorded"]["crew"], F["recorded"]["tech"], F["recorded"]["all"]))
    print("rungs: R0 by type %.1f, pooled %.1f, trailing %.1f; R3 windows %s; R3 by type %.1f"
          % (F["r0"], F["r0_pooled"], F["r0_trail"], {k: round(v, 1) for k, v in F["r3"].items()}, F["r3_type"]))
    print("bins", [(lo, hi, int(n), round(r, 2)) for lo, hi, n, e, r in F["bins"]])
    print("DA by bin", [(lo, hi, round(r, 3)) for lo, hi, r in F["da_bins"]], "DA share", F["da_share"])
    for k, v in F["asks"].items():
        print(k, v)
