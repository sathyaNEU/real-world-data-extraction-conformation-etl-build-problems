"""An independent recomputation of figures.json from target/ alone, written apart from golden.py (pandas throughout,
its own parsing, joins, fit and integration), so a figure the two disagree on is found before a reader finds it.

    python3 task487/generator/verify.py
"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
TZ = "America/Edmonton"
BAND = [(36, "A", 330), (48, "B", 640), (60, "C", 950), (72, "D", 1360), (1e9, "E", 2000)]


def utc(series):
    """any of the pack's app times to UTC: naive strings are local, offset strings carry their own"""
    out = []
    for s in series:
        ts = pd.Timestamp(s)
        ts = ts.tz_localize(TZ) if ts.tzinfo is None else ts
        out.append(ts.tz_convert("UTC"))
    return pd.to_datetime(pd.Series(out, index=series.index), utc=True)


def hours(ts):
    return (ts - pd.Timestamp("2026-01-01", tz="UTC")).dt.total_seconds() / 3600


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    reg = pd.read_csv(os.path.join(T, "battery_register_20270108.csv"), dtype=str, keep_default_na=False)
    alias = {r.battery: r.battery for r in reg.itertuples()}
    alias.update({r.former_battery: r.battery for r in reg.itertuples() if r.former_battery})
    route = dict(zip(reg.battery, reg.route))
    tel = set(reg.battery[reg.tank_pressure_telemetry == "Y"])
    comb = set(reg.battery[reg.vapour_combustor == "Y"])

    # visits from both apps, one row a visit
    fl = pd.read_csv(os.path.join(T, "route_app_visits_20251215_20260630.csv"), dtype=str)
    fl = pd.DataFrame(dict(bat=fl.Site.map(alias), a=hours(utc(fl.Arrived)), d=hours(utc(fl.Departed)), app="FL"))
    sl = pd.read_json(os.path.join(T, "checkin_app_visits_20260615_20270112.jsonl"), lines=True, dtype=False)
    sites = pd.read_csv(os.path.join(T, "checkin_app_sites.csv"), dtype=str)
    sl = pd.DataFrame(dict(bat=sl.site.map(dict(zip(sites.site_id, sites.battery))), a=hours(utc(sl.check_in.astype(str))),
                           d=hours(utc(sl.check_out.astype(str))), app="SL"))
    v = pd.concat([fl, sl]).sort_values(["bat", "a"]).reset_index(drop=True)
    keep = []
    for bat, grp in v.groupby("bat", sort=False):
        cur = None
        for r in grp.itertuples():
            if cur is not None and ((r.app == "SL" and cur[3] == "SL" and r.a - cur[2] < 10 / 60) or
                                    (r.app != cur[3] and r.a < cur[2] + 15 / 60)):
                cur[2] = max(cur[2], r.d)
                cur[3] = cur[3] if r.app == cur[3] else "both"
                continue
            if cur is not None:
                keep.append(cur)
            cur = [bat, r.a, r.d, r.app]
        keep.append(cur)
    vis = pd.DataFrame(keep, columns=["bat", "a", "d", "app"]).sort_values(["bat", "a"]).reset_index(drop=True)
    vis["prev_d"] = vis.groupby("bat").d.shift()
    vis["w"] = vis.a - vis.prev_d
    vis["local_year"] = (pd.Timestamp("2026-01-01", tz="UTC") + pd.to_timedelta(vis.a, unit="h")).dt.tz_convert(TZ).dt.year

    # the register
    ev = pd.read_excel(os.path.join(T, "release_event_register_2026.xlsx"), dtype={"Found": str, "Closed": str})
    ev["bat"] = ev.Battery.map(alias)
    ev["found"] = hours(utc(ev.Found))
    ev["closed"] = hours(utc(ev.Closed))
    txt = ev.Event.str.lower()
    ev["kind"] = np.where(txt.str.contains("hatch"), "TH", np.where(txt.str.contains("pilot|combustor|ecd|vcu|flame"),
                                                                    "CP", "PV"))
    idx = []
    for r in ev.itertuples():
        g = vis[(vis.bat == r.bat) & (vis.a <= r.found + 10 / 60)]
        idx.append(g.index[-1])
    ev["vi"] = idx
    ev = ev.join(vis[["a", "prev_d", "w"]], on="vi")
    assert len(ev) == f["events.total"], (len(ev), f["events.total"])
    for k, nm in (("TH", "hatch"), ("CP", "pilot"), ("PV", "relief")):
        assert (ev.kind == k).sum() == f["events.%s" % nm], nm

    # windows of 2026 and the fit
    win = vis[(vis.local_year == 2026) & vis.w.notna()].copy()
    win = win.merge(ev[["vi", "kind"]], left_index=True, right_on="vi", how="left") if False else win
    kind_at = dict(zip(ev.vi, ev.kind))
    win["kind"] = [kind_at.get(i) for i in win.index]
    fits = {}
    for k in ("TH", "CP", "PV"):
        m = win.bat.isin(comb) if k == "CP" else (~win.bat.isin(tel) if k == "PV" else win.bat.notna())
        y = (win.kind[m] == k).astype(float).values
        w = win.w[m].values

        def nll(x):
            p, b = x
            F = 1 - (1 - p) * np.exp(-b * w)
            return -(y * np.log(np.maximum(F, 1e-300)) + (1 - y) * np.log(np.maximum(1 - F, 1e-300))).sum()
        r = minimize(nll, [0.005, 3e-4], method="L-BFGS-B", bounds=[(0, .5), (1e-9, .01)],
                     options=dict(ftol=1e-14, gtol=1e-12, maxiter=5000))
        fits[k] = r.x
    fit_th = (round(100 * fits["TH"][0], 2), round(100 * fits["TH"][1], 3))

    # the alarm journal on the RTU's clock
    aj = pd.read_csv(os.path.join(T, "scada_alarm_journal_20251215_20270112.csv"), dtype=str, keep_default_na=False)
    aj = aj[aj.State.isin(["ALARM", "NORMAL"])].copy()
    aj["rtu"] = hours(pd.to_datetime(aj.Message.str.extract(r"RTU (\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)")[0], utc=True))
    aj["code"] = aj.Point.str.split("/").str[1]
    aj = aj.sort_values(["code", "rtu"])

    # daily rates
    pr = pd.read_csv(os.path.join(T, "battery_daily_production_20251215_20261231.csv"))
    pr["bat"] = pr.Battery.map(alias)
    pr["day"] = pd.to_datetime(pr.ProdDate)
    va = pd.read_excel(os.path.join(T, "tank_vapour_analyses_2025_2026.xlsx"))
    va["bat"] = va.Battery.map(alias)
    va["day"] = pd.to_datetime(va.Sampled)
    pr = pd.merge_asof(pr.sort_values("day"), va.sort_values("day")[["day", "bat", "Flash GOR (m3/m3)", "C1"]],
                       on="day", by="bat", direction="backward")
    pr["kgh"] = pr.OilVol_m3 * pr["Flash GOR (m3/m3)"] * pr.C1 / 100 * 0.6785 / 24
    rate = {(b, d.date()): x for b, d, x in zip(pr.bat, pr.day, pr.kgh)}
    t0 = pd.Timestamp("2026-01-01", tz="UTC")

    def kg(bat, a, c):
        tot, t = 0.0, a
        while t < c - 1e-9:
            loc = (t0 + pd.Timedelta(hours=t)).tz_convert(TZ)
            nxt = (loc.normalize() + pd.Timedelta(days=1)).tz_localize(None).tz_localize(TZ, ambiguous=False)
            t2 = min(c, (nxt.tz_convert("UTC") - t0).total_seconds() / 3600)
            tot += rate.get((bat, loc.date()), 0.0) * (t2 - t)
            t = t2
        return tot

    scada = {r.battery: (r.former_battery or r.battery) for r in reg.itertuples()}
    total = 0.0
    for r in ev.itertuples():
        st = None
        if r.kind == "PV" and r.bat in tel:
            q = aj[(aj.code == scada[r.bat]) & (aj.rtu < r.found) & (aj.State == "ALARM")].rtu.values
            st = q[-1]
            for x in q[-2::-1]:
                if st - x < 5 / 60:
                    st = x
                else:
                    break
        if st is None:
            p, b = fits[r.kind]
            xw = b * r.w
            F = p + (1 - p) * (1 - np.exp(-xw))
            Es = (1 - p) * (1 - np.exp(-xw) * (1 + xw)) / b / F
            st = r.prev_d + Es
        total += kg(r.bat, st, r.closed)
    total /= 1000
    band = next((b, levy) for hi, b, levy in BAND if total < hi)
    checks = [("methane_t", round(total, 1), f["methane_t"]), ("band", band[0], f["call"]["band"]),
              ("events", len(ev), f["events.total"]),
              ("levy", band[1] * int((reg.status == "Active").sum()), f["call"]["levy_cad"])]

    # fugitives: each tag at its battery's last survey on or before the day it reached the tracker (a survey screened
    # the battery's points; the crews' re-checks of a few repaired fittings are not surveys); a tag on a point whose
    # earlier tag was still open at that survey continues that leak; a leak ends at the last leak repair naming any of
    # its tags, a contract order's on its field ticket's day; each half goes to the run that served the battery then
    lt = pd.read_excel(os.path.join(T, "ldar_leak_tracker_20270112.xlsx"))
    lt["bat"] = lt.Battery.map(alias)
    ls = pd.read_csv(os.path.join(T, "ldar_surveys_2025_2026.csv"))
    ls["bat"] = ls.Battery.map(alias)
    sessions = ls[ls.PointsScreened * 2 < ls.groupby("bat").PointsScreened.transform("max")]
    ls = ls.drop(sessions.index)
    ls["s"] = pd.to_datetime(ls.Surveyed)
    lt["t"] = pd.to_datetime(lt.Received)
    lt = pd.merge_asof(lt.sort_values("t"), ls[["bat", "s"]].sort_values("s"), left_on="t", right_on="s", by="bat",
                       direction="backward")
    wo = pd.read_csv(os.path.join(T, "maintenance_work_orders_2026.csv"))
    wo = wo[wo.Description.str.startswith("Leak repair")].copy()
    ticket = wo.Reference.str.extract(r"^FT (\d{6})-\d{2}$")[0]
    wo["day"] = pd.to_datetime(ticket, format="%y%m%d").fillna(pd.to_datetime(wo.Completed))
    named = wo.assign(Tag=wo.Description.str.findall(r"\((T-\d{5})\)")).explode("Tag")
    last_wo = named.groupby("Tag").day.max()
    lt["r"] = lt.Tag.map(last_wo).fillna(pd.to_datetime(lt.Closed))
    lt = lt.sort_values(["bat", "Component", "s"]).reset_index(drop=True)
    surveys = {b: sorted(g_.s) for b, g_ in ls.groupby("bat")}
    prev = lt.groupby(["bat", "Component"]).r.shift(1)
    prev_s = lt.groupby(["bat", "Component"]).s.shift(1)
    cont = prev_s.notna() & (prev.isna() | (prev >= lt.s))
    lt["leak"] = (~cont).cumsum()
    halves = (("h1", pd.Timestamp("2026-01-01"), pd.Timestamp("2026-07-01")),
              ("h2", pd.Timestamp("2026-07-01"), pd.Timestamp("2027-01-01")))
    fg = {}
    for _, g_ in lt.groupby("leak"):
        b, first = g_.bat.iloc[0], g_.s.iloc[0]
        before = [x for x in surveys[b] if x < first]
        start = before[-1] if before else halves[0][1]
        end = g_.r.iloc[-1]
        end = halves[1][2] if pd.isna(end) else end
        for h, lo, hi in halves:
            n = max(0, (min(end, hi) - max(start, lo)).days)
            fg[(b, h)] = fg.get((b, h), 0.0) + g_["CH4 rate (g/h)"].iloc[0] * 24 * n / 1000
    fl = pd.read_csv(os.path.join(T, "route_app_visits_20251215_20260630.csv"))
    run1 = fl.assign(bat=fl.Site.map(alias)).groupby("bat").Route.agg(lambda x: x.mode().iloc[0])
    ck = pd.read_json(os.path.join(T, "checkin_app_visits_20260615_20270112.jsonl"), lines=True)
    st = pd.read_csv(os.path.join(T, "checkin_app_sites.csv"))
    ck = ck.merge(st[["site_id", "battery"]], left_on="site", right_on="site_id")
    day = ck.check_in.astype(str).str[:10]
    run2 = ck[(day >= "2026-07-01") & (day <= "2026-12-31")].groupby("battery").run.agg(lambda x: x.mode().iloc[0])
    sched = {}
    for (b, h), v in fg.items():
        rt_ = (run1 if h == "h1" else run2)[b]
        sched[(rt_, h)] = sched.get((rt_, h), 0.0) + v
    for rt_ in sorted(set(run1)):
        for h, lo, hi in halves:
            checks.append(("fugitive %s %s" % (rt_, h), round(sched.get((rt_, h), 0) / 1000, 1),
                           f["schedule_b.%s.%s_t" % (rt_, h)]))
    checks.append(("runs changed 1 July", int((run1 != run2.reindex(run1.index)).sum()), f["schedule_b.moved_jul"]))
    reg_run = reg.set_index("battery").route
    checks.append(("runs changed for 2027", int((run2 != reg_run.reindex(run2.index)).sum()), f["schedule_b.moved_jan"]))
    redo = lt[lt.Tag.map(last_wo).notna() & ((lt.Tag.map(last_wo) > pd.to_datetime(lt.Closed)) | lt.Closed.isna())]
    checks.append(("re-checked tags", len(redo), f["schedule_b.rechecked_tags"]))
    checks.append(("re-check sessions", len(sessions), f["schedule_b.sessions"]))
    checks.append(("contract leak orders", int(ticket.notna().sum()), f["schedule_b.contract_orders"]))
    bad = [c for c in checks if c[1] != c[2]]
    for c in checks:
        print("%s  %-16s %s %s" % ("PASS" if c[1] == c[2] else "FAIL", c[0], c[1], c[2]))
    print("verify: %d of %d agree" % (len(checks) - len(bad), len(checks)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
