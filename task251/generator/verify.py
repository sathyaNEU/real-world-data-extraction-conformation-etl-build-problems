"""An independent recomputation of every graded figure from the shipped files alone (no generator module but the file
names), against figures.json: the list, the margin, the validation facts, the visits and the power failures."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TZ = "America/Toronto"
FILES = dict(hourly="trafficvault_hourly_counts_2027.csv", validation="Northline_validation_counts_2027.xlsx",
             register="count_station_register.xlsx", network="regional_road_network_2027.xlsx",
             events="trafficvault_station_events_2027.csv", orders="Carrick_work_orders_2027.xlsx")


def main(target):
    fails = []
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    p = lambda k: os.path.join(target, FILES[k])
    reg = pd.read_excel(p("register"), sheet_name="Stations")
    hist = pd.read_excel(p("register"), sheet_name="Code history")
    new = dict(zip(hist["old_station"], hist["new_station"]))
    h = pd.read_csv(p("hourly"), dtype={"occupancy": str})
    h["station"] = h["station"].replace(new)
    h["occ"] = pd.to_numeric(h["occupancy"])
    h["t"] = pd.to_datetime(h["local_start"] + h["utc_offset"], format="%Y-%m-%d %H:%M%z", utc=True)
    v = pd.read_excel(p("validation"), sheet_name="Counts")
    v["station"] = v["site"].map(dict(zip(reg["validation_site"], reg["station"])))
    sens = (v.groupby(["station", "direction"])["loops"].sum() / v.groupby(["station", "direction"])["video"].sum())
    # the bridges' two stations: nearest stations on the bridge's road either side
    sn = pd.read_excel(p("network"), sheet_name="Structures")
    vol = h.pivot_table(index="t", columns=["station", "direction"], values="vehicles")
    occ = h.pivot_table(index="t", columns=["station", "direction"], values="occ")
    xs, ys = [], []
    for _, b in sn[sn["type"] == "bridge"].iterrows():
        on = reg[reg["road"] == b["road"]].sort_values("km")
        s1 = on[on["km"] < b["km_from"]].iloc[-1]["station"]
        s2 = on[on["km"] > b["km_to"]].iloc[0]["station"]
        for d, up, dn in (("NB", s1, s2), ("SB", s2, s1)):
            a, c, o = vol[(up, d)], vol[(dn, d)], occ[(up, d)]
            k = a.notna() & c.notna() & (a > 50) & (c > 50)
            xs.append(o[k].to_numpy())
            ys.append((1 - (a[k] / sens[(up, d)]) / (c[k] / sens[(dn, d)])).to_numpy())
    x, y = np.concatenate(xs), np.concatenate(ys)
    # a loss curve by occupancy class (one point classes, none below the free-flow range), interpolated
    cls = np.floor(x)
    tab = pd.Series(y).groupby(cls).mean()
    tab = tab[pd.Series(y).groupby(cls).size() >= 20]
    grid = tab.index.to_numpy() + 0.5
    val = np.where(grid < 21, 0.0, np.maximum(tab.to_numpy(), 0.0))
    loss = lambda o: np.interp(o, grid, val)
    err = {}
    for s in reg["station"]:
        cols = [c for c in vol.columns if c[0] == s]
        num = den = 0.0
        for c in cols:
            r = vol[c].dropna()
            oo = occ[c].dropna()
            num += r.sum()
            den += (r / sens[c] / (1 - loss(oo.to_numpy()))).sum()
        err[s] = num / den - 1
    listed = sorted(s for s, e in err.items() if abs(e) > 0.05)
    if listed != fig["call"]["listed"]:
        fails.append(("list", listed, fig["call"]["listed"]))
    if not (min(abs(err[s]) for s in listed) > fig["call"]["listed_below_pct"] / 100 and
            max(abs(e) for s, e in err.items() if s not in listed) < fig["call"]["unlisted_within_pct"] / 100):
        fails.append(("margin", min(abs(err[s]) for s in listed), max(abs(e) for s, e in err.items() if s not in listed)))
    vdays = set(zip(v["station"], v["date"].astype(str).str[:10]))
    mx = h.loc[[(s, d) in vdays for s, d in zip(h["station"], h["local_start"].str[:10])], "occ"].max()
    if round(float(mx), 1) != fig["components"]["validation_max_occupancy_pct"]:
        fails.append(("validation max occupancy", mx))
    vs = (v.groupby("station")["loops"].sum() / v.groupby("station")["video"].sum() - 1)
    for s, want in fig["components"]["default_only_validation_pct"].items():
        if int(round(100 * vs[s])) != want:
            fails.append(("validation error", s, vs[s]))
    if sorted(vs[vs.abs() > 0.05].index) != fig["components"]["default_list"]:
        fails.append(("default list", sorted(vs[vs.abs() > 0.05].index)))

    # the asks
    dist = dict(zip(reg["station"], reg["district"]))
    swap = {r["new_station"]: pd.Timestamp(r["from_date"]).date() for _, r in hist.iterrows()}
    ctl = dict(zip(reg["station"], reg["controller"]))

    def tcx4(s, day):
        return ctl[s] == "TCX-4" and not (s in swap and day < swap[s])

    ev = pd.read_csv(p("events")).drop_duplicates()
    ev["station"] = ev["station"].replace(new)
    ev["t"] = pd.to_datetime(ev["logged_utc"], utc=True)
    ev = ev[ev["t"] >= pd.Timestamp("2026-12-31", tz="UTC")]
    ev["day"] = ev["t"].dt.tz_convert(TZ).dt.date
    orders = pd.read_excel(p("orders"), sheet_name="Orders")
    labour = pd.read_excel(p("orders"), sheet_name="Labour")
    st = orders.assign(station=orders["stations"].str.split("; ")).explode("station")[["order", "station"]]
    st["station"] = st["station"].replace(new)
    lab = labour.merge(st, on="order")
    lab["day"] = pd.to_datetime(lab["date"]).dt.date
    door = set(map(tuple, ev.loc[ev["event"].str.startswith("DOOR"), ["station", "day"]].to_numpy()))
    seen = {(s, d) for s, d in zip(lab["station"], lab["day"]) if not tcx4(s, d) or (s, d) in door}
    vis = {}
    for s, d in seen:
        k = (dist[s], str((d.month - 1) // 3 + 1))
        vis[k] = vis.get(k, 0) + 1
    for dd, q in fig["asks"]["visits"].items():
        for qq, n in q.items():
            if vis.get((dd, qq), 0) != n:
                fails.append(("visits", dd, qq, vis.get((dd, qq), 0), n))
    fail = {}
    mf = ev[ev["event"] == "MAINS_FAIL"]
    for s, d in zip(mf["station"], mf["day"]):
        k = (dist[s], str((d.month - 1) // 3 + 1))
        fail[k] = fail.get(k, 0) + 1
    hours = pd.date_range(pd.Timestamp("2027-01-01", tz=TZ), pd.Timestamp("2028-01-01", tz=TZ), freq="h",
                          inclusive="left").tz_convert("UTC")
    lost_ev = ev[ev["event"] == "COMMS_LOST"]
    for s, g in h.groupby("station"):
        have = pd.DatetimeIndex(g["t"].unique())
        miss = hours.difference(have)
        if not len(miss):
            continue
        run_id = (pd.Series(miss).diff() != pd.Timedelta(hours=1)).cumsum()
        for _, grp in pd.Series(miss).groupby(run_id.to_numpy()):
            t0, t1 = grp.iloc[0], grp.iloc[-1] + pd.Timedelta(hours=1)
            d0 = t0.tz_convert(TZ).date()
            if tcx4(s, d0) or (s in swap and swap[s] == d0):
                continue
            n = int(((lost_ev["station"] == s) & (lost_ev["t"] >= t0) & (lost_ev["t"] < t1)).sum())
            k = (dist[s], str((d0.month - 1) // 3 + 1))
            fail[k] = fail.get(k, 0) + max(1, n)
    for dd, q in fig["asks"]["failures"].items():
        for qq, n in q.items():
            if fail.get((dd, qq), 0) != n:
                fails.append(("failures", dd, qq, fail.get((dd, qq), 0), n))
    for f in fails:
        print("FAIL", f)
    print("verify: %d failures" % len(fails))
    return fails


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(1 if main(t) else 0)
