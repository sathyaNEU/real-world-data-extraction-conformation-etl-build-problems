"""The ask ladder on the cut pack: each complete pipeline a careful solver could run for the two asks, scored figure by
figure against the golden; the cracker (the call landed, the natural route on each ask) and the mirror (the default
call, the same routes); the pair ceiling from the rubric arithmetic (supplemental-stumping Part 0)."""
import os
import sys

import pandas as pd

import build as B
import params as P
import solve as S


def routes(D):
    """every route: name -> (visits cells, failures cells), None where the route is about the other ask"""
    TZ = S.TZ
    out = {}
    lab = S._labour_days(D)
    lab2 = S._labour_days(D, dedup=False)
    e = S._events(D)
    eall = S._events(D, dedup=False)
    doors = e[e["event"].isin(["DOOR_OPEN", "DOOR_CLOSE"])]
    dd = set(zip(doors["station"], doors["day"]))
    t2 = [(s, d) for s, d in zip(lab["station"], lab["day"]) if not S.tcx4_on(D, s, d)]
    now = lambda s: D["reg"].set_index("station").loc[s, "controller"] == "TCX-4"
    o = D["orders"].copy()
    o["station"] = o["stations"].str.split("; ")
    o = o.explode("station")
    o["station"] = o["station"].map(lambda s: S.current(s, D))
    o["day"] = pd.to_datetime(o["opened"]).dt.date
    do = e[e["event"] == "DOOR_OPEN"]
    ddo = set(zip(do["station"], do["day"]))
    out["A labour days, one per station and day"] = S._cells(list(zip(lab["station"], lab["day"])), D)
    out["A labour lines, each a visit"] = S._cells(list(zip(lab2["station"], lab2["day"])), D)
    out["A each order at each of its stations"] = S._cells(list(zip(o["station"], o["day"])), D)
    out["A door days at TCX-4, labour days at TCX-2"] = S._cells(sorted(dd) + t2, D)
    out["A door rule, the register's controller all year"] = S._cells(
        [(s, d) for s, d in zip(lab["station"], lab["day"]) if not now(s) or (s, d) in dd], D)
    out["A door rule on DOOR_OPEN only"] = S._cells(
        [(s, d) for s, d in zip(lab["station"], lab["day"]) if not S.tcx4_on(D, s, d) or (s, d) in ddo], D)
    out["A door rule on UTC dates"] = S.visits(D, door_days="utc")
    out["A labour days where the cabinet opened at TCX-4 (the office resets out, the night out)"] = \
        S.visits(D, span=False)
    out["A the same with the night work's second day on UTC dates"] = S.visits(D, door_days="utc", span=True)
    ro = set(o.loc[o["resolution"].astype(str).str.startswith("Controller reset"), "order"])
    lr = S._labour_days(D, dedup=False)
    keep = {(s, d) for s, d, k in zip(lr["station"], lr["day"], lr["order"]) if k not in ro}
    out["A labour days less every controller reset order's labour"] = S._cells(sorted(keep), D)
    mf = eall[eall["event"] == "MAINS_FAIL"]
    mfd = e[e["event"] == "MAINS_FAIL"]
    out["B MAINS_FAIL rows"] = S._cells(list(zip(mf["station"], mf["day"])), D)
    out["B MAINS_FAIL, repeats removed"] = S._cells(list(zip(mfd["station"], mfd["day"])), D)
    cl = e[e["event"] == "COMMS_LOST"]
    out["B COMMS_LOST"] = S._cells(list(zip(cl["station"], cl["day"])), D)
    runs = S._missing_runs(D)
    swap = {(r["new_station"], pd.Timestamp(r["from_date"]).date()) for _, r in D["hist"].iterrows()}
    allr = [(s, t.tz_convert(TZ).date()) for s, t, n in runs]
    t2r = [(s, t.tz_convert(TZ).date()) for s, t, n in runs if not S.tcx4_on(D, s, t.tz_convert(TZ).date())
           and (s, t.tz_convert(TZ).date()) not in swap]
    mfp = list(zip(mfd["station"], mfd["day"]))
    out["B every break plus MAINS_FAIL"] = S._cells(allr + mfp, D)
    out["B TCX-2 breaks plus MAINS_FAIL, one per break"] = S._cells(t2r + mfp, D)
    out["B TCX-2 breaks plus MAINS_FAIL, replacements kept"] = S._cells(
        t2r + mfp + [k for k in allr if k in swap], D)
    loc = pd.date_range("2027-01-01 00:00", "2027-12-31 23:00", freq="h").strftime("%Y-%m-%d %H:%M")
    lr = []
    for s, g in D["hourly"].groupby("station"):
        miss = sorted(set(loc) - set(g["local_start"]))
        prev = None
        for m in miss:
            t = pd.Timestamp(m)
            if prev is None or t - prev != pd.Timedelta(hours=1):
                lr.append((s, t.date()))
            prev = t
    out["B breaks on the local clock at TCX-2, plus MAINS_FAIL"] = S._cells(
        [(s, d) for s, d in lr if not S.tcx4_on(D, s, d) and (s, d) not in swap] + mfp, D)
    out["B golden, quarters on UTC dates"] = S.failures(D, quarter_clock="utc")
    ep = []
    for s_, t0, n in runs:
        d0 = t0.tz_convert(TZ).date()
        if S.tcx4_on(D, s_, d0) or (s_, d0) in swap:
            continue
        k = int(((cl["station"] == s_) & (cl["t"] >= t0) & (cl["t"] < t0 + pd.Timedelta(hours=n))).sum())
        ep.extend([(s_, d0)] * k)
    out["B COMMS_LOST episodes in TCX-2 breaks plus MAINS_FAIL (round 1 readers, the portal's path)"] = \
        S.failures(D, tcx2_only=True)
    out["B every break of any controller, one per break, plus MAINS_FAIL"] = S._cells(allr + mfp, D)
    out["B the golden with the episodes at TCX-2 only"] = S._cells(ep + mfp, D)
    return out


def score(r, g):
    return sum(r[k] == g[k] for k in g)


def main(target, quiet=False):
    D = S.load(target, B.FILES)
    D = S.load_ops(target, B.FILES, D)
    gv, gf = S.visits(D), S.failures(D)
    R = routes(D)
    rows = []
    for k, r in R.items():
        g = gv if k.startswith("A") else gf
        rows.append((k, score(r, g)))
        if not quiet:
            print("%-72s %2d of 12" % (k, score(r, g)))
    crack = score(R["A labour days where the cabinet opened at TCX-4 (the office resets out, the night out)"], gv) + \
        score(R["B COMMS_LOST episodes in TCX-2 breaks plus MAINS_FAIL (round 1 readers, the portal's path)"], gf)
    Lc = crack / 24.0
    Ls = Lc
    C = 38 + 7 + 55 * Lc
    Sm = 5 + 7 + 55 * Ls
    ceiling = (C + Sm) / 2
    if not quiet:
        print("cracker keeps %d of 24; mirror the same; pair ceiling %.1f ((%.1f + %.1f) / 2)" % (crack, ceiling, C, Sm))
    return dict(rows=rows, cracker=crack, ceiling=ceiling, C=C, S=Sm)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                           "target")
    main(t)
