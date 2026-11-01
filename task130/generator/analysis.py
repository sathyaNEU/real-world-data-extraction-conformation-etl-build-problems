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
    payouts = list(csv.DictReader(open(p("payouts"), newline="")))
    ws = openpyxl.load_workbook(p("plan"), read_only=True)["2027 hours"]
    plan = {}
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] in W.DISTRICTS:
            plan[(r[0], r[1])] = [float(x) for x in r[2:6]]
    return dict(legacy=legacy, new=new, assign=assign, register=register, hours=hours, payouts=payouts, plan=plan)


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
                           job=r["job_ref"], cls=CL[r["classification"]], recur=bool(r["recurrence_of"]), loc=r["district"])
    for r in D["new"]:
        k = ("N", r["case_id"])
        if k not in last or int(r["revision"]) > last[k]["rev"]:
            last[k] = dict(rev=int(r["revision"]), emp=r["employee_id"], date=d(str(r["injury_date"])[:10]),
                           job=r["job_reference"], cls=r["osha_class"], recur=bool(r["recurrence_of_case"]), loc=r["district"])
    out = [dict(v, case=k[1]) for k, v in sorted(last.items())]
    for c in out:
        c["pinewater"] = not c["job"].startswith("MA-")
    return out


def new_cases(cs):
    """Recurrences (29 CFR 1904.6) are not new cases."""
    return [c for c in cs if not c["recur"]]


def net_awards(D, at=None):
    """Each award as payroll finally holds it: every line placed on the crew the member was on on the milestone date
    (the payroll report carries the crew on the member's HR record when it was run), lines netted by crew, milestone
    and member, an award kept when its net is positive. at=None groups on the report's own crew code instead."""
    net = collections.defaultdict(float)
    for r in D["payouts"]:
        code = at(r["employee_id"], d(r["milestone_date"])) if at else r["crew_code"]
        net[(code, r["milestone_date"], r["employee_id"])] += float(r["amount_usd"])
    by = collections.defaultdict(float)
    for (code, ms, emp), v in net.items():
        by[(code, ms)] += v
    return {k: v for k, v in by.items() if v > 0.005}


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


def cycles(cs, D, H):
    """Each crew's position in its 90-day count, day by day, from its first anchor in the record (a recordable or
    a paid award): days since the later of its last recordable injury and its last award. Returns, per cycle day,
    the Pinewater hours worked (each pay period's hours spread over its working days) and the recordables."""
    info, canon = units(D)
    resets = collections.defaultdict(set)
    for c in cs:
        if c["crew"] and c["cls"] != "FA":
            resets[c["canon"]].add(c["date"])
    awards = collections.defaultdict(set)   # the awards paid, each on the crew that earned it, start the counts
    for (code, ms) in net_awards(D, assignment_lookup(D)):
        if code in info:
            awards[canon.get(code, code)].add(d(ms))
    per_day = collections.defaultdict(dict)
    for h in H:
        if h["type"] not in CREW_TYPES or h["worked"] <= 0:
            continue
        wd = working_days(h["ps"])
        for day in wd:
            per_day[h["canon"]][day] = per_day[h["canon"]].get(day, 0.0) + h["worked"] / len(wd)
    exp = np.zeros(W.MILESTONE)
    cnt = np.zeros(W.MILESTONE)
    cnt_cls = collections.defaultdict(lambda: np.zeros(W.MILESTONE))
    by_type_exp = collections.defaultdict(lambda: np.zeros(W.MILESTONE))
    by_type_cnt = collections.defaultdict(lambda: np.zeros(W.MILESTONE))
    pine = collections.defaultdict(list)
    for c in cs:
        if c["crew"] and c["cls"] != "FA" and c["pinewater"]:
            pine[c["canon"]].append(c)
    days_seen = 0
    for crew in sorted(per_day):
        anchors = sorted(resets[crew] | awards[crew])
        if not anchors:
            continue
        ctype = info[crew]["type"]
        start = anchors[0] + ONE
        ai = 1
        day = start
        last_day = max(per_day[crew])
        rset, aset = resets[crew], awards[crew]
        pos = {}
        while day <= last_day:
            n = (day - start).days
            pos[day] = n
            if day in rset or day in aset or n == W.MILESTONE - 1:
                start = day + ONE
            day += ONE
        for dd_, h in per_day[crew].items():
            if dd_ in pos:
                exp[pos[dd_]] += h
                by_type_exp[ctype][pos[dd_]] += h
                days_seen += 1
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


def asks(D, cs, H, report_codes=False, timesheet_district=False, posting_period=False, case_location=False):
    """CS-4 4(c) for 5 January to 27 September 2026, district by district, with the crews' own rate and the
    recognition awards earned in the same window. The flags price a response's handling: the payroll report's own
    crew codes, the timesheet's district column, prior-period adjustments left in the pay period they were posted
    in, the case record's location district."""
    info, canon = units(D)
    awards = net_awards(D, None if report_codes else assignment_lookup(D))
    if case_location:
        cs = [dict(c, district=c["loc"]) for c in cs]
    if posting_period or timesheet_district:
        H2 = []
        for h, r in zip(H, D["hours"]):
            h2 = dict(h)
            if posting_period:
                h2["ps"] = d(r["pay_period_start"])
            if timesheet_district:
                h2["district"] = r["district"]
            H2.append(h2)
        H = H2
    A = {}
    for dist in W.DISTRICTS:
        n = sum(1 for c in cs if ASK0 <= c["date"] <= ASK1 and c["cls"] != "FA" and c["pinewater"]
                and c["district"] == dist)
        da = sum(1 for c in cs if ASK0 <= c["date"] <= ASK1 and c["cls"] == "DA" and c["pinewater"]
                 and c["district"] == dist)
        hrs = sum(h["worked"] for h in H if ASK0 <= h["ps"] and h["ps"] + dt.timedelta(days=13) <= ASK1
                  and h["district"] == dist)
        nc = sum(1 for c in cs if ASK0 <= c["date"] <= ASK1 and c["cls"] != "FA" and c["pinewater"]
                 and c["district"] == dist and c["crew"])
        hc = sum(h["worked"] for h in H if ASK0 <= h["ps"] and h["ps"] + dt.timedelta(days=13) <= ASK1
                 and h["district"] == dist and h["type"] in CREW_TYPES)
        aw = {k: v for k, v in awards.items()
              if ASK0 <= d(k[1]) <= ASK1 and k[0] in info and info[k[0]]["district"] == dist}
        A[dist] = dict(cases=n, days_away=da, hours=hrs, rate=n * K / hrs, crew_rate=nc * K / hc,
                       milestones=len(aw), usd=sum(aw.values()))
    return A


def call_with_report_anchors(D, cs, H, plan, tech_rate):
    """The call when the counts are started from the payroll report's own crew codes (a solver who never places an
    award on the crew that earned it)."""
    info, canon = units(D)
    saved = net_awards

    def fake(Dx, at=None):
        return saved(Dx, None)
    globals()["net_awards"] = fake
    try:
        cyc = cycles(cs, D, H)
    finally:
        globals()["net_awards"] = saved
    clean = cyc["cnt"][:CLEAN].sum() * K / cyc["exp"][:CLEAN].sum()
    q, hq = forecast(plan, clean, tech_rate)
    return float(q.sum()), float(q.sum() * K / hq.sum()), clean


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
    A = asks(D, cs, H)
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
