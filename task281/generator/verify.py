"""Independent verifier for task281 (pandas, its own code path): recomputes the placement and the three asks (hours
worked at each unit, the people who worked overtime at each unit, the people over 600 hours by title) from target/ and
compares them with generator/figures.json."""
from __future__ import annotations

import json
import math
import os

import numpy as np
import pandas as pd

UNITS = ["HRC", "ACF", "TWC", "PCN", "PCS", "FFH", "OXG", "KPG"]
TITLE = {"HRC": "CO", "ACF": "CO", "TWC": "CO", "PCN": "PCO", "PCS": "PCO", "FFH": "FSA", "OXG": "HMW", "KPG": "HMW"}
OFF = {"Annual leave", "Sick leave", "Injury on duty", "Training", "Family and medical leave", "Military leave"}
FY26, FY28 = pd.Timestamp("2025-07-01"), pd.Timestamp("2027-07-01")
DAYS = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}


def placement(t):
    ro = pd.read_csv(os.path.join(t, "merrimont_shift_rosters_fy2026.csv"), dtype=str).fillna("")
    ro = ro.sort_values("exported_at").drop_duplicates(["shift_date", "line_id"], keep="last")
    codes = pd.read_csv(os.path.join(t, "timekeeping_status_codes.csv"), dtype=str)
    ro = ro.merge(codes[["source_system", "status_code", "state_category"]], on=["source_system", "status_code"],
                  how="left")
    ro["off"] = ro.state_category.isin(OFF)
    ro["hrs"] = ro.scheduled_hours.astype(float)
    ro["week"] = (pd.to_datetime(ro.shift_date) - FY26).dt.days // 7 + 1
    emp = pd.read_csv(os.path.join(t, "hr_employee_extract_2026-10-01.csv"), dtype=str).fillna("")
    cls = emp[emp.academy_class.str.endswith(" 2025-1")].drop_duplicates("employee_id")
    held = ro[ro.employee_id.isin(cls.employee_id)].merge(cls[["employee_id", "academy_class"]], on="employee_id")
    held["t"] = held.academy_class.str.split().str[0]
    a1 = {t_: 1 - (g.hrs * g.off).sum() / g.hrs.sum() for t_, g in held.groupby("t")}
    pc = pd.read_csv(os.path.join(t, "position_control_fy2028_round_the_clock_units.csv"), dtype=str).fillna("")
    pc = pc[pc.status_fy2028_start == "Vacant"]
    out = {}
    for u in UNITS:
        a = a1[TITLE[u]]
        off = ro[(ro.unit_code == u) & ro.off & (ro.week <= 52)].groupby("week").hrs.sum()
        need = np.array([off.get(k, 0.0) for k in range(1, 53)])
        for _, r in pc[pc.unit_code == u].iterrows():
            first = pd.Timestamp(r.first_shift_on_post)
            dayoff = {DAYS[x] for x in r.days_off.split("/")}
            for i in range(364):
                d = FY28 + pd.Timedelta(days=i)
                if d.weekday() in dayoff:
                    continue
                need[i // 7] += 8.0 if d < first else 8.0 * (1 - a)
        out[u] = math.ceil(sorted(need, reverse=True)[4] / (40.0 * a) - 1e-9)
    return out


def asks(t):
    pay = pd.read_csv(os.path.join(t, "payroll_overtime_lines_checks_jul2025_jul2026.csv"), dtype=str).fillna("")
    emp = pd.read_csv(os.path.join(t, "hr_employee_extract_2026-10-01.csv"), dtype=str).fillna("")
    offers = pd.read_csv(os.path.join(t, "overtime_offer_log_fy2026.csv"), dtype=str).fillna("")
    spells = emp[["employee_id", "title_code", "title_effective_from", "title_effective_to"]]

    def title_on(e, d):
        s = spells[(spells.employee_id == e) & (spells.title_effective_from <= d) &
                   ((spells.title_effective_to == "") | (spells.title_effective_to >= d))]
        if len(s):
            return s.title_code.iloc[0]
        return spells[spells.employee_id == e].sort_values("title_effective_from").title_code.iloc[-1]
    tcache = {}

    def tt(e, d):
        if (e, d) not in tcache:
            tcache[(e, d)] = title_on(e, d)
        return tcache[(e, d)]
    for c in ("hours", "amount"):
        pay[c] = pay[c].astype(float)
    pay = pay.reset_index().rename(columns={"index": "n"})
    key = ["employee_id", "work_date", "start_time", "hours", "earn_code"]
    comp = {"CTE": 1.5, "CTS": 1.0}
    piece = pay[pay.earn_code.isin(["OT", "OTN", "CTE", "CTS"])].sort_values(["check_date", "n"])
    firsts = piece.groupby(key).check_date.transform("min")
    repeat = set(piece.n[piece.check_date != firsts])
    pay["infy"] = (pay.work_date >= "2025-07-01") & (pay.work_date <= "2026-06-30")
    once = pay[~pay.n.isin(repeat)]
    worked = once[once.infy & once.earn_code.isin(["OT", "CTE", "CTS"])].copy()
    worked["cr"] = worked.earn_code.map(comp).fillna(1.0)
    worked["w"] = worked.hours / worked.cr
    acc = offers[offers.response == "Accepted"].copy()
    acc["wh"] = acc.hours.astype(float).round(2)
    acc = acc.rename(columns={"post_date": "work_date"})
    worked["wh"] = worked.w.round(2)
    worked = worked.merge(acc[["employee_id", "work_date", "start_time", "wh", "post_unit"]],
                          on=["employee_id", "work_date", "start_time", "wh"], how="left")
    worked["unit"] = worked.post_unit.fillna("").where(worked.post_unit.fillna("") != "",
                                                        worked.home_timekeeper.replace({"SL-0410": "TWC"}))
    a = worked.groupby("unit").w.sum().round().astype(int).to_dict()

    cur = emp.sort_values("title_effective_from").drop_duplicates("employee_id", keep="last")
    canon = {}
    for _, r in cur.iterrows():
        if r.seniority_date and r.seniority_date < r.hire_date:
            m = cur[(cur.employee_id != r.employee_id) & (cur.seniority_date == r.seniority_date) &
                    (cur.separation_date != "") & (cur.separation_date < r.hire_date) &
                    (cur.title_code == r.title_code)]
            if len(m) == 1:
                canon[m.employee_id.iloc[0]] = r.employee_id
    worked["person"] = worked.employee_id.map(lambda e: canon.get(e, e))
    b = worked.groupby("unit").person.nunique().to_dict()

    # SF16: the literal reading joins a line to its accepted offer by employee, date and start alone (the hours of a
    # CTE line are credit, not the post's hours), and leaves an unoffered piece at the employee's own unit
    k3 = acc.drop_duplicates(["employee_id", "work_date", "start_time"])
    if len(k3) != len(acc):
        raise SystemExit("verify: FAIL an accepted offer repeats employee, date and start")
    alt = worked.drop(columns=["post_unit", "unit"]).merge(
        k3[["employee_id", "work_date", "start_time", "post_unit"]], on=["employee_id", "work_date", "start_time"],
        how="left")
    alt["unit"] = alt.post_unit.fillna("").where(alt.post_unit.fillna("") != "",
                                                  alt.home_timekeeper.replace({"SL-0410": "TWC"}))
    if (alt.unit.values != worked.unit.values).any():
        raise SystemExit("verify: FAIL the three-key join places a piece elsewhere than the four-key join")

    person = worked.groupby("person").w.sum().to_dict()
    c = {}
    for e, h in person.items():
        if h > 600:
            t_ = tt(e, "2026-06-30")
            c[t_] = c.get(t_, 0) + 1
    return a, b, c


def run(task):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    bad = []
    p = placement(t)
    if p != fig["call"]["positions"]:
        bad.append("placement %s vs %s" % (p, fig["call"]["positions"]))
    if sum(p.values()) != fig["call"]["total"]:
        bad.append("total")
    # SF16 and SF17 as the files carry them: the payroll's own headers, the earnings codes, no file describing the data
    head = open(os.path.join(t, "payroll_overtime_lines_checks_jul2025_jul2026.csv"), encoding="utf-8").readline()
    if "home_timekeeper" not in head or "home_cost_center" not in head:
        bad.append("payroll headers")
    codes = pd.read_csv(os.path.join(t, "payroll_earnings_codes.csv"), dtype=str)
    if not {"Comp time earned 1.5", "Comp time earned 1.0"} <= set(codes.description):
        bad.append("earnings codes")
    if [f for f in os.listdir(t) if any(w in f.lower() for w in ("dictionary", "readme", "manifest", "notes"))]:
        bad.append("a file describing the data ships")
    a, b, c = asks(t)
    if {u: a.get(u, 0) for u in UNITS} != fig["ask_a_overtime_hours_by_unit"]:
        bad.append("ask A %s" % a)
    if {u: b.get(u, 0) for u in UNITS} != fig["ask_b_people_by_unit"]:
        bad.append("ask B %s" % b)
    if {k: c.get(k, 0) for k in ("CO", "PCO", "FSA", "HMW")} != fig["ask_c_people_over_600_hours"]:
        bad.append("ask C %s" % c)
    print("verify: %s" % ("PASS" if not bad else "FAIL " + "; ".join(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    sys.exit(run(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
