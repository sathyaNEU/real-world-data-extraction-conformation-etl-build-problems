"""Independent verifier: recompute the golden's forecast and the asks from target/ with pandas, on its own code
path (each crew's count walked day by day from HR-14 Revision 2's start on 11 January 2021, exposure from crew-days
weighted by each pay period's hours per working day; the first-aid cases deduplicated across the nurse line and the
supervisors' reports on the worker and a seven-day window), and require agreement with the golden workbook."""
import datetime as dt
import os
import sys

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as P   # noqa: E402  (file names only)

K = 200000
A0, A1 = pd.Timestamp("2026-01-05"), pd.Timestamp("2026-09-27")


def hol(y):
    import world as W
    return W.holidays(y)


def main(target, golden_dir):
    f = lambda k: os.path.join(target, P.FILES[k])
    leg = pd.read_csv(f("legacy"), dtype=str, keep_default_na=False)
    new = pd.read_excel(f("cases"), sheet_name="Cases", dtype=str).fillna("")
    reg = pd.read_excel(f("register"), sheet_name="Crews", dtype=str).fillna("")
    asg = pd.read_csv(f("assign"), dtype=str, keep_default_na=False)
    hrs = pd.read_csv(f("hours"), keep_default_na=False)
    # cases: the new system wins for migrated cases; latest revision; no recurrences
    leg = leg[~leg["case_no"].isin(set(new["legacy_case_no"]) - {""})]
    leg = leg.sort_values(["case_no", "revision"]).groupby("case_no").tail(1)
    cmap = {"First aid": "FA", "Medical treatment": "MT", "Restricted work": "RW", "Days away": "DA"}
    a = pd.DataFrame({"emp": leg["employee_no"], "date": pd.to_datetime(leg["injury_date"], format="%m/%d/%Y"),
                      "job": leg["job_ref"], "cls": leg["classification"].map(cmap), "recur": leg["recurrence_of"] != "",
                      "src": "Supervisor"})
    new["revision"] = new["revision"].astype(int)
    new = new.sort_values(["case_id", "revision"]).groupby("case_id").tail(1)
    b = pd.DataFrame({"emp": new["employee_id"], "date": pd.to_datetime(new["injury_date"].str[:10]),
                      "job": new["job_reference"], "cls": new["osha_class"], "recur": new["recurrence_of_case"] != "",
                      "src": new["source"]})
    allc = pd.concat([a, b]).reset_index(drop=True)
    allc["pine"] = ~allc["job"].str.startswith("MA-")
    asg["from"] = pd.to_datetime(asg["assigned_from"])
    asg["to"] = pd.to_datetime(asg["assigned_to"].replace("", "2099-12-31"))
    mall = allc.reset_index().merge(asg, left_on="emp", right_on="employee_id")
    mall = mall[(mall["from"] <= mall["date"]) & (mall["date"] <= mall["to"])]
    assert mall["index"].is_unique and len(mall) == len(allc), "every case on one crew or team on its day"
    m = mall[(~mall["recur"]) & (mall["cls"] != "FA")].copy()
    info = reg.set_index("unit_code")
    m["type"] = m["crew_or_team"].map(info["unit_type"])
    m["district"] = m["crew_or_team"].map(info["district"])
    canon = dict(zip(reg.loc[reg["status"] == "Recoded", "unit_code"], reg.loc[reg["status"] == "Recoded", "recoded_to"]))
    m["canon"] = m["crew_or_team"].map(lambda x: canon.get(x, x))
    crew_t = {"OH", "UG", "SUB", "VEG"}
    m["crew"] = m["type"].isin(crew_t)
    # hours: adjustments to the period they correct, the unit's own district
    hrs["ps"] = pd.to_datetime(np.where(hrs["adjusts_pay_period"] != "", hrs["adjusts_pay_period"], hrs["pay_period_start"]))
    hrs["worked"] = hrs["regular_hours"] + hrs["overtime_hours"]
    hrs["home"] = hrs["unit_code"].map(info["district"])
    hrs["canon"] = hrs["unit_code"].map(lambda x: canon.get(x, x))
    # rates over the history
    h0, h1 = pd.Timestamp("2021-01-11"), pd.Timestamp("2026-09-27")
    tech_h = hrs.loc[~hrs["unit_type"].isin(crew_t), "worked"].sum()
    tech_n = ((~m["crew"]) & m["pine"]).sum()
    tech_rate = tech_n * K / tech_h
    # counts: day by day per crew from HR-14 Revision 2's start, restarted after each recordable and each 90th day
    resets = {}
    for cr, g in m[m["crew"]].groupby("canon"):
        resets.setdefault(cr, set()).update(g["date"].dt.date)
    ch = hrs[hrs["unit_type"].isin(crew_t) & (hrs["worked"] != 0)]
    per_day = {}
    for (cr, ps), w in ch.groupby(["canon", "ps"])["worked"].sum().items():
        p = ps.date()
        wd = [p + dt.timedelta(days=k) for k in range(14)]
        wd = [x for x in wd if x.weekday() < 5 and x not in hol(x.year)]
        for x in wd:
            per_day.setdefault(cr, {})[x] = per_day.setdefault(cr, {}).get(x, 0.0) + w / len(wd)
    exp_e = exp_all = 0.0
    n_e = n_all = 0
    pine = m[m["crew"] & m["pine"]]
    pine_by = {cr: set(g["date"].dt.date) for cr, g in pine.groupby("canon")}
    pine_cnt = pine.groupby(["canon", pine["date"].dt.date]).size().to_dict()
    for cr, days in per_day.items():
        start = dt.date(2021, 1, 11)
        rs = resets.get(cr, set())
        day, end = start, max(days)
        while day <= end:
            n = (day - start).days
            h = days.get(day, 0.0)
            k = pine_cnt.get((cr, day), 0)
            exp_all += h
            n_all += k
            if n < 35:
                exp_e += h
                n_e += k
            if day in rs or n == 89:
                start = day + dt.timedelta(days=1)
            day += dt.timedelta(days=1)
    clean = n_e * K / exp_e
    ws = openpyxl.load_workbook(f("plan"), read_only=True)["2027 hours"]
    crew_plan = tech_plan = 0.0
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] in ("Blue Ridge", "Piedmont", "Lakes", "Coastal"):
            if r[1] in crew_t:
                crew_plan += sum(r[2:6])
            else:
                tech_plan += sum(r[2:6])
    total = (clean * crew_plan + tech_rate * tech_plan) / K
    # the asks: first-aid cases, each injury once. A nurse-line case goes with a supervisor's case for the same
    # worker dated within the seven days before its call; with none, it is an injury of its own.
    sup = mall[mall["src"] != "Nurse line"]
    nl = mall[mall["src"] == "Nurse line"]
    pair = nl[["index", "emp", "date"]].merge(sup[["emp", "date"]], on="emp", suffixes=("", "_s"))
    gap = (pair["date"] - pair["date_s"]).dt.days
    twinned = set(pair.loc[(gap >= 0) & (gap <= 7), "index"])
    inj = pd.concat([sup, nl[~nl["index"].isin(twinned)]])
    fa = inj[(inj["cls"] == "FA") & inj["pine"] & ~inj["recur"] & (inj["date"] >= A0) & (inj["date"] <= A1)].copy()
    fa["district"] = fa["crew_or_team"].map(info["district"])
    fa["q"] = np.where(fa["date"] <= pd.Timestamp("2026-03-31"), 0, np.where(fa["date"] <= pd.Timestamp("2026-06-30"), 1, 2))
    asks = {dist: [int(((fa["district"] == dist) & (fa["q"] == q)).sum()) for q in range(3)]
            for dist in ("Blue Ridge", "Piedmont", "Lakes", "Coastal")}
    # compare with the golden workbook
    gb = openpyxl.load_workbook(os.path.join(golden_dir, "recordables_forecast_2027.xlsx"), data_only=True)
    fc = gb["2027 forecast"]
    g_total = fc["C8"].value
    assert abs(round(total) - g_total) <= 1, "forecast %.2f against the golden %s" % (total, g_total)
    db = gb["2026 by district"]
    for row in db.iter_rows(min_row=4, max_row=7, values_only=True):
        dist = row[0]
        assert list(row[1:4]) == asks[dist] and row[4] == sum(asks[dist]), "first aid %s: %s against %s" % (dist, row, asks[dist])
    print("verify: match (forecast %.1f, clean %.3f, technicians %.3f; the four districts' first-aid cases by quarter)"
          % (total, clean, tech_rate))


if __name__ == "__main__":
    t = os.path.join(os.path.dirname(HERE), "target")
    main(t, os.path.join(os.path.dirname(HERE), "golden"))
