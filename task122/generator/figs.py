"""Every owed figure, computed from target/ alone. The golden handling is the default of each switch; the other
settings are the readings the routes, the checks and the ceiling price.

    python3 task122/generator/figs.py [target]
"""
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P   # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
F = {"crossings": "fdps_sector_crossings_2026-04_2026-09.csv", "stca": "stca_activations_2026-04_2026-09.csv",
     "probe": "probe_m_planner_workstation_log_2026-04_2026-09.csv",
     "config": "sector_configuration_log_2026-04_2026-09.csv"}
S = P.SECTORS
EPOCH = pd.Timestamp(P.T0)
GOLD = {"revisions": "flight", "continuation": "drop", "status": "live", "attribution": "first", "months": "local",
        "probe_tz": "local", "presence": "midpoint"}


def utc_sec(series):
    return ((pd.to_datetime(series, utc=True) - EPOCH).dt.total_seconds()).astype(np.int64)


def local_sec(series, tz="local"):
    t = pd.to_datetime(series)
    if tz == "local":
        t = t.dt.tz_localize(P.NZ, ambiguous="raise", nonexistent="raise")
    else:
        t = t.dt.tz_localize("UTC")
    return ((t.dt.tz_convert("UTC") - EPOCH).dt.total_seconds()).astype(np.int64)


def month_edges(kind="local"):
    """Seconds since the trial start of each month's first instant, and the trial's end."""
    out = []
    for k, mo in enumerate(range(4, 11)):
        d = dt.datetime(2026, mo, 1, tzinfo=P.NZ if kind == "local" else P.UTC)
        out.append(int((d.astimezone(P.UTC) - P.T0).total_seconds()))
    return out


def load(target=TARGET):
    p = lambda k: os.path.join(target, F[k])
    cr = pd.read_csv(p("crossings"))
    st = pd.read_csv(p("stca"))
    pr = pd.read_csv(p("probe"))
    cf = pd.read_csv(p("config"))
    return {"cr": cr, "st": st, "pr": pr, "cf": cf}


def crossings(D, revisions="flight"):
    """The crossings flown. A revision re-issues the flight's whole crossing list, so the flown crossings are those of
    each flight's latest revision ('flight'); 'pair' keeps the latest revision of each flight and sector, 'all' keeps
    every row."""
    c = D["cr"].copy()
    if revisions == "flight":
        last = c.groupby("ifps_id")["plan_revision"].transform("max")
        c = c[c.plan_revision == last]
    elif revisions == "pair":
        last = c.groupby(["ifps_id", "sector"])["plan_revision"].transform("max")
        c = c[c.plan_revision == last]
    c = c.copy()
    c["a"] = utc_sec(c.entry_utc)
    c["b"] = utc_sec(c.exit_utc)
    c["trn"] = c.entry_fl != c.exit_fl
    return c.reset_index(drop=True)


def occupancy(c, presence="midpoint"):
    """Aircraft present in each sector at each minute, and how many climb or descend through it. 'midpoint' counts a
    crossing in a minute when the minute's midpoint falls inside it; 'start' uses the minute's first second; 'any'
    counts any overlap."""
    n = np.zeros((len(S), P.MINUTES + 2), np.int32)
    T = np.zeros((len(S), P.MINUTES + 2), np.int32)
    si = c.sector.map({s: i for i, s in enumerate(S)}).values
    a, b, tr = c.a.values, c.b.values, c.trn.values
    if presence == "midpoint":
        lo = np.ceil((a - 30) / 60.0).astype(int)
        hi = np.ceil((b - 30) / 60.0).astype(int)
    elif presence == "start":
        lo = np.ceil(a / 60.0).astype(int)
        hi = np.ceil(b / 60.0).astype(int)
    else:
        lo = np.floor(a / 60.0).astype(int)
        hi = np.ceil(b / 60.0).astype(int)
    lo = np.clip(lo, 0, P.MINUTES)
    hi = np.clip(hi, 0, P.MINUTES)
    for arr, mask in ((n, np.ones(len(a), bool)), (T, tr)):
        d = np.zeros((len(S), P.MINUTES + 2), np.int64)
        np.add.at(d, (si[mask], lo[mask]), 1)
        np.add.at(d, (si[mask], hi[mask]), -1)
        arr += np.cumsum(d, axis=1).astype(np.int32)
    return n[:, :P.MINUTES], T[:, :P.MINUTES]


def probe_on(D, tz="local", presence="midpoint"):
    """Minutes with the probe display on at the position covering each elementary sector."""
    pr = D["pr"]
    a = local_sec(pr.display_on, tz).values
    b = local_sec(pr.display_off, tz).values
    on = np.zeros((len(S), P.MINUTES + 2), np.int64)
    if presence == "midpoint":
        lo = np.ceil((a - 30) / 60.0).astype(int)
        hi = np.ceil((b - 30) / 60.0).astype(int)
    elif presence == "start":
        lo = np.ceil(a / 60.0).astype(int)
        hi = np.ceil(b / 60.0).astype(int)
    else:
        lo = np.floor(a / 60.0).astype(int)
        hi = np.ceil(b / 60.0).astype(int)
    lo = np.clip(lo, 0, P.MINUTES)
    hi = np.clip(hi, 0, P.MINUTES)
    for k, sec in enumerate(pr.sector.values):
        for s in sec.split("/"):
            i = S.index(s)
            on[i, lo[k]] += 1
            on[i, hi[k]] -= 1
    return (np.cumsum(on, axis=1)[:, :P.MINUTES] > 0)


def activations(D, c, continuation="drop", status="live", attribution="first"):
    """STCA activations counted as the safety performance report counts them: live only, once per event in the sector
    where it began (a record that opens as an alert carries into the next sector is the same event), combined-sector
    activations in the elementary sector that held the first-named aircraft when the alert began."""
    st = D["st"].copy()
    if status == "live":
        st = st[st.status == "LIVE"]
    st = st.copy()
    st["a"] = utc_sec(st.start_utc)
    st["b"] = utc_sec(st.end_utc)
    st["pair"] = [tuple(sorted(x)) for x in zip(st.callsign_1, st.callsign_2)]
    st = st.sort_values(["a", "alert_id"]).reset_index(drop=True)
    if continuation == "drop":
        last_end = {}
        keep = []
        for pair, sec, a, b in zip(st.pair, st.sector, st.a, st.b):
            prev = last_end.get(pair)
            cont = prev is not None and prev[1] != sec and 0 <= a - prev[0] <= 3
            keep.append(not cont)
            last_end[pair] = (b, sec)
        st = st[np.array(keep)].copy()
    # the elementary sector of each activation
    elem = []
    if attribution == "first":
        idx = {}
        for cs, sec, a, b in zip(c.callsign, c.sector, c.a, c.b):
            idx.setdefault(cs, []).append((a, b, sec))
        for cs, sec, a in zip(st.callsign_1, st.sector, st.a):
            if "/" not in sec:
                elem.append(sec)
                continue
            hit = [x[2] for x in idx.get(cs, []) if x[0] <= a < x[1] and x[2] in sec.split("/")]
            elem.append(hit[0] if hit else None)
    else:
        elem = [s if "/" not in s else s.split("/")[0] for s in st.sector]
    st["elem"] = elem
    return st[st.elem.notna()].reset_index(drop=True)


def panel(D, rules=None):
    R = dict(GOLD)
    R.update(rules or {})
    c = crossings(D, R["revisions"])
    n, T = occupancy(c, R["presence"])
    on = probe_on(D, R["probe_tz"], R["presence"])
    st = activations(D, c, R["continuation"], R["status"], R["attribution"])
    al = np.zeros((len(S), P.MINUTES), np.int32)
    m = (st.a // 60).astype(int).values
    ok = (m >= 0) & (m < P.MINUTES)
    np.add.at(al, (st.elem.map({s: i for i, s in enumerate(S)}).values[ok], m[ok]), 1)
    return {"c": c, "n": n, "T": T, "on": on, "al": al, "st": st}


def frame(pn):
    rows = []
    for i, s in enumerate(S):
        rows.append(pd.DataFrame({"sector": s, "m": np.arange(P.MINUTES), "n": pn["n"][i], "T": pn["T"][i],
                                  "on": pn["on"][i], "al": pn["al"][i]}))
    return pd.concat(rows, ignore_index=True)


def strata_table(df, keys=("sector", "n", "T")):
    g = df.groupby(list(keys) + ["on"]).agg(al=("al", "sum"), ex=("m", "size")).unstack("on").fillna(0)
    g.columns = ["%s_%s" % (a, "on" if b else "off") for a, b in g.columns]
    for k in ("al_on", "al_off", "ex_on", "ex_off"):
        if k not in g:
            g[k] = 0
    return g


def observed_expected(df, keys=("sector", "n", "T")):
    """The criterion's estimand: the activations the probe's running minutes raised against those the same sectors
    would have raised in those minutes without it, read from the minutes without it at the same sector, count of
    aircraft and count climbing or descending."""
    g = strata_table(df, keys)
    g = g[(g.ex_on > 0) & (g.ex_off > 0)]
    O = g.al_on.sum()
    E = (g.ex_on * g.al_off / g.ex_off).sum()
    return float(O), float(E), float(g.ex_on.sum())


def share_prevented(df, keys=("sector", "n", "T")):
    O, E, _ = observed_expected(df, keys)
    return 1.0 - O / E


def ask_hours(c, months="local"):
    """Flight hours by sector and New Zealand month, each crossing split at the month boundaries."""
    e = month_edges(months)
    out = {}
    for s in S:
        cs = c[c.sector == s]
        a, b = cs.a.values, cs.b.values
        row = []
        for k in range(6):
            lo, hi = e[k], e[k + 1]
            row.append(float(np.clip(np.minimum(b, hi) - np.maximum(a, lo), 0, None).sum()) / 3600.0)
        out[s] = row
    return out


def ask_rates(st, hours, months="local"):
    e = month_edges(months)
    out = {}
    for s in S:
        a = st[st.elem == s].a.values
        cnt = [int(((a >= e[k]) & (a < e[k + 1])).sum()) for k in range(6)]
        out[s] = [1000.0 * x / h for x, h in zip(cnt, hours[s])]
    return out


def ask_flights(c, reentry="once"):
    out = {}
    for s in S:
        cs = c[c.sector == s]
        out[s] = int(cs.ifps_id.nunique()) if reentry == "once" else int(len(cs))
    return out


def compute(target=TARGET, rules=None):
    D = load(target)
    pn = panel(D, rules)
    df = frame(pn)
    O, E, onmin = observed_expected(df)
    share = 1.0 - O / E
    hours = ask_hours(pn["c"])
    rates = ask_rates(pn["st"], hours)
    flights = ask_flights(pn["c"])
    # the paper's chart: by the number of aircraft climbing or descending, the share of minutes with the probe
    # running, and the probe's running time's activations as raised and as the same traffic raised without it
    g = strata_table(df).reset_index()
    g = g[(g.ex_on > 0) & (g.ex_off > 0)]
    g["E"] = g.ex_on * g.al_off / g.ex_off
    g["lvl"] = np.minimum(g["T"], 5)
    lv = g.groupby("lvl").agg(O=("al_on", "sum"), E=("E", "sum"))
    run = df.assign(lvl=np.minimum(df["T"], 5)).groupby("lvl").on.mean()
    levels = ["0", "1", "2", "3", "4", "5 or more"]
    chart = {"levels": levels, "share_running": [round(float(run.get(k, 0.0)), 4) for k in range(6)],
             "observed": [int(lv.O.get(k, 0)) for k in range(6)], "expected": [round(float(lv.E.get(k, 0.0)), 1) for k in range(6)]}
    by = {}
    gs = strata_table(df).reset_index()
    for s in S:
        x = gs[(gs.sector == s) & (gs.ex_on > 0) & (gs.ex_off > 0)]
        e = float((x.ex_on * x.al_off / x.ex_off).sum())
        o = int(x.al_on.sum())
        by[s] = {"hours": int(round(df[(df.sector == s) & df.on].shape[0] / 60.0)), "observed": o, "expected": round(e, 1),
                 "prevented": round(e - o, 1)}
    on_ = df[df.on]
    off_ = df[~df.on]
    rate_on = 1000.0 * on_.al.sum() / (on_.n.sum() / 60.0)
    rate_off = 1000.0 * off_.al.sum() / (off_.n.sum() / 60.0)
    fig = {
        "chart": chart, "by_sector": by,
        "probe_hours": int(round(onmin / 60.0)),
        "rate_on_per_1000fh": round(rate_on, 1), "rate_off_per_1000fh": round(rate_off, 1),
        "call": "mandatory" if share >= 0.20 else "discretionary",
        "share_prevented": round(share, 4),
        "share_prevented_pct_nearest5": int(5 * round(100 * share / 5.0)),
        "observed": int(O), "expected": round(E, 1), "prevented": round(E - O, 1),
        "probe_minutes": int(onmin),
        "activations_counted": int(len(pn["st"])),
        "flight_hours": {s: [int(round(v)) for v in hours[s]] for s in S},
        "flight_hours_exact": {s: [round(v, 3) for v in hours[s]] for s in S},
        "stca_rate": {s: [round(v, 1) for v in rates[s]] for s in S},
        "stca_rate_exact": {s: [round(v, 4) for v in rates[s]] for s in S},
        "flights_handled": flights,
        "months": P.MONTHS,
    }
    return fig


if __name__ == "__main__":
    import json
    t = sys.argv[1] if len(sys.argv) > 1 else TARGET
    f = compute(t)
    print(json.dumps({k: v for k, v in f.items() if k not in ("flight_hours_exact", "stca_rate_exact")}, indent=1))
