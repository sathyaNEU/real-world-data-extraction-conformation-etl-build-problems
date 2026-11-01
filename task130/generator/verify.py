"""Independent verifier: recompute the golden's forecast and the asks from target/ with pandas, on its own code
path (counts rebuilt crew by crew from the awards and the recordables, exposure from crew-days weighted by each pay
period's hours per working day), and require agreement with the golden workbook."""
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
    pay = pd.read_csv(f("payouts"), keep_default_na=False)
    # cases: the new system wins for migrated cases; latest revision; no recurrences
    leg = leg[~leg["case_no"].isin(set(new["legacy_case_no"]) - {""})]
    leg = leg.sort_values(["case_no", "revision"]).groupby("case_no").tail(1)
    cmap = {"First aid": "FA", "Medical treatment": "MT", "Restricted work": "RW", "Days away": "DA"}
    a = pd.DataFrame({"emp": leg["employee_no"], "date": pd.to_datetime(leg["injury_date"], format="%m/%d/%Y"),
                      "job": leg["job_ref"], "cls": leg["classification"].map(cmap), "recur": leg["recurrence_of"] != ""})
    new["revision"] = new["revision"].astype(int)
    new = new.sort_values(["case_id", "revision"]).groupby("case_id").tail(1)
    b = pd.DataFrame({"emp": new["employee_id"], "date": pd.to_datetime(new["injury_date"].str[:10]),
                      "job": new["job_reference"], "cls": new["osha_class"], "recur": new["recurrence_of_case"] != ""})
    cs = pd.concat([a, b])
    cs = cs[(~cs["recur"]) & (cs["cls"] != "FA")].copy()
    cs["pine"] = ~cs["job"].str.startswith("MA-")
    asg["from"] = pd.to_datetime(asg["assigned_from"])
    asg["to"] = pd.to_datetime(asg["assigned_to"].replace("", "2099-12-31"))
    m = cs.reset_index(drop=True).merge(asg, left_on="emp", right_on="employee_id")
    m = m[(m["from"] <= m["date"]) & (m["date"] <= m["to"])]
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
    # counts: day by day per crew from its first award or recordable
    awards = pay.groupby(["crew_code", "milestone_date", "employee_id"])["amount_usd"].sum().reset_index()
    awards = awards[awards["amount_usd"] > 0.005].groupby(["crew_code", "milestone_date"]).size().reset_index()
    awards["canon"] = awards["crew_code"].map(lambda x: canon.get(x, x))
    anchors = {}
    for cr, g in awards.groupby("canon"):
        anchors.setdefault(cr, set()).update(pd.to_datetime(g["milestone_date"]).dt.date)
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
        an = sorted(resets.get(cr, set()) | anchors.get(cr, set()))
        if not an:
            continue
        start = an[0] + dt.timedelta(days=1)
        rs, aw = resets.get(cr, set()), anchors.get(cr, set())
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
            if day in rs or day in aw or n == 89:
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
    # the asks
    w = m[(m["date"] >= A0) & (m["date"] <= A1) & m["pine"]]
    hw = hrs[(hrs["ps"] >= A0) & (hrs["ps"] + pd.Timedelta(days=13) <= A1)]
    asks = {}
    for dist in ("Blue Ridge", "Piedmont", "Lakes", "Coastal"):
        n = int((w["district"] == dist).sum())
        hh = hw.loc[hw["home"] == dist, "worked"].sum()
        nc = int(((w["district"] == dist) & w["crew"]).sum())
        hc = hw.loc[(hw["home"] == dist) & hw["unit_type"].isin(crew_t), "worked"].sum()
        asks[dist] = (n, hh, n * K / hh, nc * K / hc)
    pw = pay.copy()
    pw["code_at"] = None
    am = pw.merge(asg, on="employee_id")
    md = pd.to_datetime(am["milestone_date"])
    am = am[(am["from"] <= md) & (md <= am["to"])]
    net = am.groupby(["crew_or_team", "milestone_date", "employee_id"])["amount_usd"].sum().reset_index()
    net = net[net["amount_usd"] > 0.005]
    net = net[(pd.to_datetime(net["milestone_date"]) >= A0) & (pd.to_datetime(net["milestone_date"]) <= A1)]
    net["district"] = net["crew_or_team"].map(info["district"])
    aw_n = net.groupby("district").apply(lambda g: len(set(zip(g["crew_or_team"], g["milestone_date"])))).to_dict()
    aw_usd = net.groupby("district")["amount_usd"].sum().to_dict()
    # compare with the golden workbook
    gb = openpyxl.load_workbook(os.path.join(golden_dir, "recordables_forecast_2027.xlsx"), data_only=True)
    fc = gb["2027 forecast"]
    g_total = fc["C8"].value
    assert abs(round(total) - g_total) <= 1, "forecast %.2f against the golden %s" % (total, g_total)
    db = gb["2026 by district"]
    for row in db.iter_rows(min_row=4, max_row=7, values_only=True):
        dist = row[0]
        n, hh, r, rc = asks[dist]
        assert row[1] == n and row[2] == round(hh) and abs(row[3] - round(r, 2)) < 1e-9 and abs(row[4] - round(rc, 2)) < 1e-9, \
            "asks %s: %s against %s" % (dist, row, asks[dist])
        assert row[5] == aw_n.get(dist, 0) and row[6] == round(aw_usd.get(dist, 0)), "awards %s" % dist
    print("verify: match (forecast %.1f, clean %.3f, technicians %.3f; four districts' asks and awards)"
          % (total, clean, tech_rate))


if __name__ == "__main__":
    t = os.path.join(os.path.dirname(HERE), "target")
    main(t, os.path.join(os.path.dirname(HERE), "golden"))
