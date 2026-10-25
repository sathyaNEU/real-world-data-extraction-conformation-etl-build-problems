"""Independent verifier for task121 (pandas, its own code path): links each questionnaire to its train and journey,
recomputes the four drivers' points of the fall and the plan's baselines from target/, and compares them with
generator/figures.json."""
from __future__ import annotations

import json
import os
import re
from datetime import date, timedelta

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
F = {k: v for k, v in [
    ("resp", "cst_responses_spring2025_spring2026.csv"), ("field", "cst_fieldwork_log_spring2025_spring2026.csv"),
    ("tt", "working_timetable_dec2024_dec2025.csv"), ("mv", "train_movements_2025_2026.csv"),
    ("lw", "loadweigh_departures_2025_2026.csv"), ("form", "daily_formations_2025_2026.csv"),
    ("fleet", "fleet_register_2026.xlsx"), ("crew", "onboard_crew_as_worked_mar2025_apr2026.csv"),
    ("roster", "onboard_roster_aug_sep_2026.csv"), ("amend", "onboard_roster_amendments_aug_sep_2026.csv"),
    ("fares", "fares_change_jan2026.csv"), ("st", "station_reference.csv")]}
HOLS = {"2026-04-03", "2026-04-06", "2026-08-31"}
GROUP_CODE = {"Marlvale Main Line": "MAIN", "Hollin Vale": "VALE", "Coastway": "COAST", "Pellow Branch": "BRANCH",
              "Corrington Link": "LINK"}


def m(t):
    h, mi = str(t).split(":")
    return int(h) * 60 + int(mi)


def runs_label(d):
    if d in HOLS:
        return "SUN"
    wd = date.fromisoformat(d).weekday()
    return {5: "SAT", 6: "SUN"}.get(wd, "MO-FR")


def norm(s):
    return re.sub(r"[^a-z]", "", str(s).lower())


def main():
    t = os.path.join(os.path.dirname(HERE), "target")
    rd = lambda k, **kw: pd.read_csv(os.path.join(t, F[k]), **kw)
    resp = rd("resp", dtype=str)
    field = rd("field", dtype=str).set_index("batch_id")
    tt = rd("tt", dtype=str)
    tt["seq"] = tt.call_seq.astype(int)
    mv = rd("mv", dtype=str)
    lw = rd("lw", dtype={"passengers_est": int})
    form = rd("form", dtype=str)
    units = pd.read_excel(os.path.join(t, F["fleet"]), sheet_name="Units", dtype={"Unit": str})
    mods = pd.read_excel(os.path.join(t, F["fleet"]), sheet_name="Modifications", dtype={"Unit": str})
    crew = rd("crew", dtype=str)
    fares = rd("fares")
    st = rd("st")
    fig = json.load(open(os.path.join(HERE, "figures.json")))

    names = {norm(n): c for c, n in zip(st.crs_code, st.station_name)}
    short = {"marlvale": "MVC", "marlvalecent": "MVC", "mvalecentral": "MVC", "marlvalec": "MVC", "ashcombepkwy": "ASP",
             "ashcombe": "ASP", "stcleerrd": "STC", "stcleer": "STC", "marlvalenth": "MVN", "marlvalesth": "MVS",
             "holbeck": "HBK", "farnley": "FRN", "wexleyx": "WXC", "trevose": "TRV", "pennick": "PNB", "carrow": "CRW",
             "radley": "RDL"}

    def code(written, coded):
        if isinstance(coded, str) and coded:
            return coded
        k = norm(written)
        if k.upper() in set(st.crs_code):
            return k.upper()
        if k in names:
            return names[k]
        if k in short:
            return short[k]
        import difflib
        mm = difflib.get_close_matches(k, list(names), n=1, cutoff=0.85)
        return names[mm[0]]

    seats = dict(zip(units.Unit, units["Standard seats"]))
    after = {r.Unit: (str(r[3])[:10], int(r[4])) for r in mods.itertuples(index=False)}

    def seat(u, d):
        if u in after and d >= after[u][0]:
            return after[u][1]
        return seats[u]

    sched = {}
    for uid, g in tt.groupby("train_uid"):
        g = g.sort_values("seq")
        f0 = g.iloc[0]
        sched[(f0.timetable, f0.headcode, f0.days_run, f0.station, f0.dep)] = (uid, list(g.station), f0.service_group)
    load = lw.groupby(["run_date", "headcode", "station"]).passengers_est.sum().to_dict()
    fm = form.groupby(["run_date", "headcode"]).unit_no.apply(list).to_dict()
    arr = mv[mv.event_type == "ARRIVAL"].set_index(["run_date", "train_uid", "station"])[["wtt_time", "recorded_time"]].to_dict("index")
    crewed = set(zip(crew.work_date, crew.headcode))
    pct = {}
    for r in fares.itertuples():
        x = (r.fare_from_04jan2026_pence / r.fare_before_pence - 1) * 100
        pct[(r.from_station, r.to_station, r.ticket_type)] = pct[(r.to_station, r.from_station, r.ticket_type)] = x
    rows = []
    for r in resp.itertuples():
        b = field.loc[r.batch_id]
        d = b.fieldwork_date
        tl = "Dec24" if d < "2025-12-14" else "Dec25"
        uid, calls, grp = sched[(tl, b.train_headcode, runs_label(d), b.origin_station, b.origin_dep)]
        bs, al = code(r.board_station_written, r.board_station_code), code(r.alight_station_written, r.alight_station_code)
        i, j = calls.index(bs), calls.index(al)
        cap = sum(seat(u, d) for u in fm[(d, b.train_headcode)])
        crowded = max(load[(d, b.train_headcode, calls[k])] for k in range(i, j)) > cap
        a = arr[(d, uid, al)]
        late = ((m(a["recorded_time"]) - m(a["wtt_time"]) + 720) % 1440 - 720) >= 5
        unstaffed = (d, b.train_headcode) not in crewed
        fare = pct[(bs, al, r.ticket_type)] if r.wave == "Spring 2026" else 0.0
        rows.append((r.wave == "Spring 2026", int(r.q1_overall) >= 4, float(r.weight), grp, int(crowded), int(late),
                     int(unstaffed), fare))
    J = pd.DataFrame(rows, columns=["w26", "sat", "wt", "grp", "crowded", "late", "unstaffed", "fare"])
    sh = {k: 100 * np.average(g.sat, weights=g.wt) for k, g in J.groupby("w26")}
    X = np.column_stack([np.ones(len(J)), J.crowded, J.late, J.unstaffed, J.fare, J.w26.astype(float)])
    W = J.wt.values
    beta = np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (W * J.sat.astype(float)))
    dlt = [np.average(J[c][J.w26], weights=J.wt[J.w26]) - np.average(J[c][~J.w26], weights=J.wt[~J.w26])
           for c in ("crowded", "late", "unstaffed", "fare")]
    pts = {n: -beta[k + 1] * dlt[k] * (100 if n != "fares" else 100)
           for k, n in enumerate(["crowding", "punctuality", "on-board staffing", "fares"])}
    top = max(pts, key=pts.get)
    bad = []

    def cmp(label, got, want):
        if got != want:
            bad.append("%s: %s against %s" % (label, got, want))

    half = lambda x, nd=0: float(np.floor(x * 10 ** nd + 0.5) / 10 ** nd) if nd else int(np.floor(x + 0.5))
    cmp("driver", top, fig["call"]["driver"])
    cmp("points", half(pts[top]), fig["call"]["points"])
    cmp("share 2025", half(sh[False], 1), fig["shares"]["spring_2025"])
    cmp("share 2026", half(sh[True], 1), fig["shares"]["spring_2026"])
    for n, v in pts.items():
        cmp("bridge " + n, half(v), fig["bridge_points"][n])

    # baselines, four weeks ending 19 September 2026
    days = [(date(2026, 8, 23) + timedelta(days=k)).isoformat() for k in range(28)]
    t25 = tt[tt.timetable == "Dec25"].sort_values(["train_uid", "seq"])
    tr = {uid: (g.iloc[0].service_group, g.iloc[0].days_run, g.iloc[0].headcode, list(g.station), list(g.arr))
          for uid, g in t25.groupby("train_uid")}
    ran = set(zip(mv.run_date, mv.train_uid))
    roster = rd("roster", dtype=str)
    amend = rd("amend", dtype=str)
    cov = set()
    for r in amend.itertuples():
        dd = date.fromisoformat(r.amend_date) + timedelta(days=1 if m(r.logged) >= 720 else 0)
        cov.add((dd.isoformat(), r.diagram))
    staffed = set()
    for r in roster.itertuples():
        if r.status == "Rostered" or (r.roster_date, r.diagram) in cov:
            staffed |= {(r.roster_date, h) for h in r.workings.split(";")}
    lw["unit_no"] = lw["unit_no"].astype(str)
    gu = lw.groupby(["run_date", "unit_no", "station", "departed"]).passengers_est.agg(["sum", "max", "nunique", "count"])
    # after the fleet system's move (17 May 2026) a class 166's three vehicle rows each carry the unit's figure
    once = (gu["count"] == 3) & (gu["nunique"] == 1) & (gu.index.get_level_values(0) >= "2026-05-17")
    by_unit = gu["max"].where(once, gu["sum"]).to_dict()
    depart = mv[mv.event_type == "DEPARTURE"].set_index(["run_date", "train_uid", "station"]).recorded_time.to_dict()
    on, sf, sd = {}, {}, {}
    for d in days:
        lab = runs_label(d)
        for uid, (g, dr, hc, calls, arrs) in tr.items():
            if dr != lab:
                continue
            a = arr.get((d, uid, calls[-1]))
            ot = a is not None and ((m(a["recorded_time"]) - m(arrs[-1]) + 720) % 1440 - 720) < 5
            on.setdefault(g, []).append(ot)
            if (d, uid) in ran:
                sf.setdefault(g, []).append((d, hc) in staffed)
            if calls[-1] == "MVC" and lab == "MO-FR" and 420 <= m(arrs[-1]) <= 599 and a is not None:
                left = depart.get((d, uid, calls[-2]))
                got = [by_unit.get((d, u, calls[-2], left)) for u in fm[(d, hc)]]
                if left is not None and None not in got:
                    sd[g] = sd.get(g, 0) + max(0, sum(got) - sum(seat(u, d) for u in fm[(d, hc)]))
    for g in GROUP_CODE.values():
        cmp("on time " + g, half(100 * np.mean(on[g]), 1), fig["ask_on_time_pct"][g])
        cmp("staffed " + g, half(100 * np.mean(sf[g]), 1), fig["ask_staffed_pct"][g])
        if g != "BRANCH":
            cmp("standing " + g, int(sd[g]), fig["ask_standing"][g])
    print("verify: %s (%d figures)" % ("PASS" if not bad else "FAIL", 4 + len(pts) + 14))
    for x in bad:
        print("  ", x)
    return 1 if bad else 0


def run(task):
    return main()


if __name__ == "__main__":
    raise SystemExit(main())
