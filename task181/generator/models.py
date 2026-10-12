"""The main call computed from the pack in target/: each sector's exposures in the record and in the summer 2027
planning traffic, the losses of separation, the golden forecast and every rung of the ladder.

The golden: losses of separation follow the pairs of aircraft in one sector at once whose levels change order (one
climbs or descends through the other's level). The centre's rate of ATM-related losses per such pair, pooled over
every sector and the whole record (January 2025 to September 2026), times each sector's pairs in the summer 2027
planning traffic, over its planning flight hours, per 100,000 flight hours, against the plan's 40.0."""
import json
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import exposure as X
import world as W

TOL = W.TOLERANCE


def _sec(series):
    """UTC seconds since 1970 for a column of timestamps, whatever resolution pandas parses them at."""
    ts = pd.to_datetime(series, utc=True)
    return ((ts - pd.Timestamp("1970-01-01", tz="UTC")) // pd.Timedelta(seconds=1)).to_numpy().astype(np.int64)


def register(target):
    reg = json.load(open(os.path.join(target, "sector_register.json")))
    return {s["traffic_volume"]: s["code"] for s in reg["sectors"]}, {s["name"]: s["code"] for s in reg["sectors"]}


def fdps(target):
    tb = pq.read_table(os.path.join(target, "fdps_sector_traversals_2025-01_2026-09.parquet"))
    d = {c: tb.column(c).to_numpy(zero_copy_only=False) for c in ("ifplid", "callsign", "sector", "entry_fl", "exit_fl")}
    t0 = tb.column("entry_time_utc").cast(pa.timestamp("s", tz="UTC")).cast("int64").to_numpy()
    t1 = tb.column("exit_time_utc").cast(pa.timestamp("s", tz="UTC")).cast("int64").to_numpy()
    sidx = {s: k for k, s in enumerate(W.SECTORS)}
    return dict(ifplid=d["ifplid"], callsign=d["callsign"], sec=np.array([sidx[s] for s in d["sector"]]),
                t0=t0.astype(np.int64), t1=t1.astype(np.int64), a=d["entry_fl"].astype(np.int64),
                b=d["exit_fl"].astype(np.int64))


def planning(target):
    tv, _ = register(target)
    df = pd.read_csv(os.path.join(target, "planning_traffic_summer2027_issue1.csv"))
    sidx = {s: k for k, s in enumerate(W.SECTORS)}
    return dict(key=df["flight_key"].to_numpy(), sec=np.array([sidx[tv[x]] for x in df["tv"]]),
                t0=_sec(df["t_in"]), t1=_sec(df["t_out"]), a=df["fl_in"].to_numpy(np.int64),
                b=df["fl_out"].to_numpy(np.int64))


def occurrences(target):
    _, names = register(target)
    df = pd.read_csv(os.path.join(target, "occurrence_export_2025-01_2026-09.csv"), dtype=str, keep_default_na=False)
    df["code"] = df["sector"].map(names)
    df["sec"] = df["code"].map({s: k for k, s in enumerate(W.SECTORS)})
    df["ts"] = _sec(df["occurrence_date"] + " " + df["time_utc"])
    return df


def windows():
    s25, s26 = [tuple(int(x.timestamp()) for x in W.season(y)) for y in (2025, 2026)]
    allw = (int(W.ACTUAL_START.timestamp()), int(W.ACTUAL_END.timestamp()))
    y26 = (int(pd.Timestamp("2026-01-01", tz="UTC").timestamp()), allw[1])
    return {"all": [allw], "s25": [s25], "s26": [s26], "summers": [s25, s26], "y26": [y26]}


def _in(x, wins):
    m = np.zeros(len(x), bool)
    for a, b in wins:
        m |= (x >= a) & (x < b)
    return m


def exposures(t, wins):
    """Per sector and window: flight hours, climbing or descending flight hours, entries, the hourly entries squared,
    pairs that change order, pairs that meet at a level, pairs with an aircraft changing level, and such pairs within
    1,000 ft and 2,000 ft at the nearest."""
    out = {}
    for s, order, pt in X.by_sector(t):
        t0, t1, a, b = t["t0"][order], t["t1"][order], t["a"][order], t["b"][order]
        dur = (t1 - t0) / 3600.0
        meet = (pt["dlo"] * pt["dhi"] <= 0) & ~((pt["dlo"] == 0) & (pt["dhi"] == 0)) & pt["moving"]
        for name, wl in wins.items():
            m = _in(t0, wl)
            hours = (t0[m] // 3600)
            _, cnt = np.unique(hours, return_counts=True)
            px = _in(pt["tx"], wl)
            pl = _in(pt["lo"], wl)
            out[(s, name)] = dict(
                fh=float(dur[m].sum()), vfh=float(dur[m & (a != b)].sum()), n=int(m.sum()),
                nsq=float((cnt.astype(float) ** 2).sum()), cross=int((pt["cross"] & px).sum()),
                meet=int((meet & pl).sum()), mp=int((pt["moving"] & pl).sum()),
                n10=int((pt["moving"] & pl & (pt["gap"] < 10)).sum()), n20=int((pt["moving"] & pl & (pt["gap"] < 20)).sum()))
    return out


def losses(occ, wins, atm=True):
    smi = occ[occ["occurrence_type"] == "SMI"]
    if atm:
        smi = smi[smi["atm_contribution"].isin(["D", "I"])]
    out = {}
    for name, wl in wins.items():
        m = _in(smi["ts"].to_numpy(), wl)
        c = smi[m].groupby("sec").size()
        for s in range(8):
            out[(s, name)] = int(c.get(s, 0))
    return out


def compute(target):
    rec, plan, occ = fdps(target), planning(target), occurrences(target)
    wins = windows()
    ex = exposures(rec, wins)
    a27, b27 = (int(x.timestamp()) for x in W.season(2027))
    ex27 = exposures(plan, {"s27": [(a27, b27)]})
    L = losses(occ, wins)
    Lall = losses(occ, wins, atm=False)
    S = range(8)

    def rate27(lam, key="cross"):
        return {s: lam * ex27[(s, "s27")][key] / ex27[(s, "s27")]["fh"] * 1e5 for s in S}

    def pooled(win, key="cross", Ld=L):
        return sum(Ld[(s, win)] for s in S) / sum(ex[(s, win)][key] for s in S)
    r = {}
    lam = pooled("all")
    r["golden"] = rate27(lam)
    r["R0"] = {s: L[(s, "s26")] / ex[(s, "s26")]["fh"] * 1e5 for s in S}
    r["R1"] = {s: L[(s, "s26")] * ex27[(s, "s27")]["fh"] / ex[(s, "s26")]["fh"] / ex27[(s, "s27")]["fh"] * 1e5 for s in S}
    r["R1_record"] = {s: L[(s, "all")] / ex[(s, "all")]["fh"] * 1e5 for s in S}
    r["R1_summers"] = {s: L[(s, "summers")] / ex[(s, "summers")]["fh"] * 1e5 for s in S}
    r["R2_density"] = {s: L[(s, "s26")] * ex27[(s, "s27")]["nsq"] / ex[(s, "s26")]["nsq"] / ex27[(s, "s27")]["fh"] * 1e5
                       for s in S}
    r["R2b_own"] = {s: L[(s, "s26")] / ex[(s, "s26")]["vfh"] * ex27[(s, "s27")]["vfh"] / ex27[(s, "s27")]["fh"] * 1e5
                    for s in S}
    r["R2b_pooled"] = rate27(pooled("all", "vfh"), "vfh")
    r["R2b_pooled_s26"] = rate27(pooled("s26", "vfh"), "vfh")
    r["R2c_trend"] = {s: (r["R0"][s] ** 2 / (L[(s, "s25")] / ex[(s, "s25")]["fh"] * 1e5)) if L[(s, "s25")] else
                      float("inf") for s in S}
    r["R3_summers"] = rate27(pooled("summers"))
    r["R3_s26"] = rate27(pooled("s26"))
    r["R3_y26"] = rate27(pooled("y26"))
    r["R3_own"] = {s: L[(s, "all")] / ex[(s, "all")]["cross"] * ex27[(s, "s27")]["cross"] / ex27[(s, "s27")]["fh"] * 1e5
                   for s in S}
    r["R3_all_losses"] = rate27(pooled("all", Ld=Lall))
    r["R3_meet"] = rate27(pooled("all", "meet"), "meet")
    r["R3_moving_pairs"] = rate27(pooled("all", "mp"), "mp")
    r["R3_within_1000ft"] = rate27(pooled("all", "n10"), "n10")
    r["R3_within_2000ft"] = rate27(pooled("all", "n20"), "n20")
    sets = {k: sorted(W.SECTORS[s] for s, v in d.items() if v > TOL) for k, d in r.items()}
    exp27 = {s: lam * ex27[(s, "s27")]["cross"] for s in S}
    return dict(r=r, sets=sets, lam=lam, ex=ex, ex27=ex27, L=L, Lall=Lall, exp27=exp27, occ=occ, rec=rec, plan=plan)
