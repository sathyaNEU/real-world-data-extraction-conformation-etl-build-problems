"""The truth: every tree on every plot from 2006 to 2026, its identity, growth and fate, what each crew recorded,
the plots split across stand boundaries, the tags lost and found, and the 2026 field days. golden.py never reads
this; checks.py reads it as the clean truth."""
import math

import numpy as np

import world as W

MIX = {"pine": [0.47, 0.14, 0.13, 0.08, 0.12, 0.06], "mixed": [0.22, 0.10, 0.28, 0.18, 0.16, 0.06]}
SEP = 7.0          # minimum stem spacing on a plot, feet


def _xy(az, d):
    return d * math.sin(math.radians(az)), d * math.cos(math.radians(az))


def _place(rng, pts, r_max=W.PLOT_R * math.sqrt(0.992), sep=SEP):
    for _ in range(400):
        az, d = float(rng.uniform(0, 360)), float(r_max * math.sqrt(rng.uniform(0.0006, 1.0)))
        x, y = _xy(az, d)
        if all((x - a) ** 2 + (y - b) ** 2 >= sep * sep for a, b in pts):
            pts.append((x, y))
            return az, d
    raise RuntimeError("plot full")


def _grow(rng, dbh):
    return float(rng.uniform(0.5, 2.2) if dbh < 20 else rng.uniform(0.4, 1.6))


def _chord_offset(share):
    if share >= 1.0:
        return 9e9
    lo, hi = -W.PLOT_R, W.PLOT_R
    for _ in range(60):
        m = (lo + hi) / 2
        a = math.acos(max(-1.0, min(1.0, m / W.PLOT_R)))
        seg = (a - math.sin(2 * a) / 2) / math.pi
        if 1 - seg > share:
            hi = m
        else:
            lo = m
    return (lo + hi) / 2


def _merch(rng, dbh):
    return int(round(float(np.clip(6 + 2.6 * dbh + rng.normal(0, 7), 17, 112))))


def plots_layout(rng):
    plots = []
    pno = 100
    splits = {}
    for sid in W.SIDS:
        st = W.STAND[sid]
        nb = W.neighbours(sid)
        for k in range(st["n_plots"]):
            pno += 1 + (1 if rng.random() < 0.07 else 0) + (1 if rng.random() < 0.03 else 0)
            split = rng.random() < 0.13
            other = nb[int(rng.integers(0, len(nb)))] if split else None
            share = round(float(rng.uniform(0.52, 0.86)), 2) if split else 1.0
            splits.setdefault(sid, 0)
            plots.append(dict(plot=pno, stand=sid, nb=other, share=share, bearing=float(rng.uniform(0, 360)),
                              off=_chord_offset(share),
                              x=st["cx"] + rng.normal(0, 380), y=st["cy"] + rng.normal(0, 330),
                              slope=int(rng.integers(4, 52)), aspect=int(rng.integers(0, 360)),
                              est=2011 if sid in W.ACQUIRED else 2006))
    for p in plots:
        p["elev"] = int(round(3650 + (4418800 - p["y"]) * 0.21 + (p["x"] - 676200) * 0.09 + rng.normal(0, 120)))
    return plots


def simulate():
    rng = np.random.default_rng(W.SEED + 1)
    plots = plots_layout(rng)
    trees = []
    for p in plots:
        pts = []
        sid = p["stand"]

        def cond_of(az, d):
            if p["nb"] is None:
                return 1, sid
            along = d * math.cos(math.radians(az - p["bearing"]))
            return (2, p["nb"]) if along > p["off"] else (1, sid)

        n = int(rng.integers(15, 34))
        for t in range(n):
            az, d = _place(rng, pts)
            cid, cst = cond_of(az, d)
            kind, ft = W.STAND[cst]["kind"], W.STAND[cst]["ftype"]
            sp = int(rng.choice(6, p=MIX[ft]))
            dbh21 = float(np.clip(rng.lognormal(2.55, 0.45), 5.0, 44.0))
            hist = {2021: dbh21}
            dd = dbh21
            for yr in (2016, 2011, 2006):
                dd -= _grow(rng, dd)
                hist[yr] = dd
            g26 = _grow(rng, dbh21)
            tr = dict(plot=p["plot"], cond=cid, cst=cst, sp=sp, az=az, d=d, hist=hist, dbh26=dbh21 + g26, alive21=True)
            _fate(rng, tr, kind, cst)
            trees.append(tr)
        # trees that died or were cut in an earlier interval: tallied live, then dead or cut at the next cycle
        for (y0, y1) in ((2006, 2011), (2011, 2016), (2016, 2021)):
            if y0 < p["est"]:
                continue
            k = int(rng.integers(0, 3))
            if y1 == 2016 and sid in W.THINNED_2012:
                k += int(rng.integers(3, 7))
            for t in range(k):
                az, d = _place(rng, pts)
                cid, cst = cond_of(az, d)
                sp = int(rng.choice(6, p=MIX[W.STAND[cst]["ftype"]]))
                dl = float(np.clip(rng.lognormal(2.45, 0.45), 5.0, 36.0))
                hist = {y0: dl}
                dd = dl
                for yr in [c for c in W.CYCLES if c < y0][::-1]:
                    dd -= _grow(rng, dd)
                    hist[yr] = dd
                cut = y1 == 2016 and sid in W.THINNED_2012 and t >= k - 6 and rng.random() < 0.8
                trees.append(dict(plot=p["plot"], cond=cid, cst=cst, sp=sp, az=az, d=d, hist=hist, alive21=False,
                                  end=y1, end_code="C" if cut else "D", dbh26=None))
        # 2026 ingrowth: stems that crossed 5.0 inches since 2021
        for t in range(int(rng.integers(0, 5))):
            az, d = _place(rng, pts)
            cid, cst = cond_of(az, d)
            sp = int(rng.choice(6, p=MIX[W.STAND[cst]["ftype"]]))
            trees.append(dict(plot=p["plot"], cond=cid, cst=cst, sp=sp, az=az, d=d, hist={}, alive21=False,
                              ingrowth=True, dbh26=float(rng.uniform(5.0, 7.1)), end=None))
        # a tree the 2021 crew passed over, tallied for the first time in 2026
        if rng.random() < 0.05:
            az, d = _place(rng, pts, sep=10.0)
            cid, cst = cond_of(az, d)
            sp = int(rng.choice(6, p=MIX[W.STAND[cst]["ftype"]]))
            trees.append(dict(plot=p["plot"], cond=cid, cst=cst, sp=sp, az=az, d=d, hist={}, alive21=False,
                              missed=True, dbh26=float(rng.uniform(9.5, 19.0)), end=None))
    _found_tags(rng, trees)
    _tags(rng, plots, trees)
    for t in trees:
        t["merch"] = _merch(rng, t["dbh26"]) if (t["dbh26"] and t["dbh26"] >= 11.0 and t["sp"] not in W.HARDWOOD) else None
        t["cull"] = int(rng.choice([0, 0, 0, 0, 0, 0, 10, 10, 20])) if t["merch"] else None
        t["merch21"] = (math.floor(min(6, _merch(rng, t["hist"][2021]) / 16.5) * 2) / 2
                        if t["alive21"] and t["hist"][2021] >= 11.0 and t["sp"] not in W.HARDWOOD else None)
    _visits(rng, plots)
    return dict(plots=plots, trees=trees)


def _fate(rng, t, kind, cst):
    """2021 to 2026: death, cutting, and what happened to the tag of a survivor."""
    dbh = t["hist"][2021]
    t.update(dies=False, cut=False, found_dead=False, tagloss=None, char=False)
    if kind == "plain":
        p_die = 0.024 * (1.4 if dbh < 9 else 1.0)
        p_lost = 0.045
    elif kind == "beetle":
        p_die = 0.52 if (t["sp"] in W.PINES and dbh >= 13) else 0.035
        p_lost = 0.045
    elif kind == "burn":
        t["char"] = rng.random() < 0.70
        if t["char"]:
            p_die = 0.46 if dbh < 9 else 0.03
            p_lost = 0.50 if dbh >= 9 else 0.0
        else:
            p_die, p_lost = 0.022, 0.02
    else:   # the 2025 lightning fire
        p_die = 0.50 if dbh >= 9 else 0.7
        p_lost = 0.36
    if rng.random() < p_die:
        t["dies"] = True
        t["found_dead"] = rng.random() < (0.05 if kind == "wild" else 0.85)
        return
    if cst in W.ROAD_2023 and rng.random() < 0.025:
        t["cut"] = True
        return
    if dbh >= 8.0 and rng.random() < p_lost:
        u = rng.random()
        t["tagloss"] = "retag" if u < 0.58 else ("dup" if u < 0.86 else "renailed")


def _found_tags(rng, trees):
    by = {}
    for t in trees:
        if t.get("alive21") and not t["dies"] and not t["cut"]:
            by.setdefault(t["cst"], []).append(t)
    for sid in W.SIDS:
        pool = by.get(sid, [])
        ok = [t for t in pool if t["tagloss"] == "dup" and t["hist"][2021] >= 10.5 and t["sp"] not in W.HARDWOOD]
        if ok:
            continue
        cand = sorted([t for t in pool if t["tagloss"] in ("renailed", None) and t["hist"][2021] >= 10.5
                       and t["sp"] not in W.HARDWOOD], key=lambda t: (t["plot"], t["az"]))
        if cand:
            cand[int(rng.integers(0, len(cand)))]["tagloss"] = "dup"


def _tags(rng, plots, trees):
    """Tags issued in order of first tally, cycle by cycle, from the company's bags (a damaged tag now and then is
    thrown away, so the series has gaps)."""
    by_plot = {}
    for t in trees:
        by_plot.setdefault(t["plot"], []).append(t)
    nxt = 10001
    for yr in W.CYCLES:
        for p in plots:
            if yr < p["est"]:
                continue
            first = []
            for t in by_plot[p["plot"]]:
                cyc = [c for c in t["hist"] if t["hist"][c] >= 5.0 and c >= p["est"]]
                if cyc and min(cyc) == yr:
                    first.append(t)
            first.sort(key=lambda t: (t["az"], t["d"]))
            for t in first:
                if rng.random() < 0.025:
                    nxt += int(rng.integers(1, 4))
                t["tag"] = nxt
                nxt += 1
    for t in trees:
        t.setdefault("tag", None)
    # the contract crew's series in 2026, in the order the crews worked the plots
    new = W.NEW_TAG0
    for p in plots:
        for t in sorted(by_plot[p["plot"]], key=lambda t: (t["az"], t["d"])):
            if t.get("ingrowth") or t.get("missed") or t.get("tagloss") in ("retag", "dup"):
                t["new_tag"] = new
                new += 1


def _visits(rng, plots):
    """2026 field days: two contract crews, weekdays from 8 June to 28 August; the smoke week stops heights."""
    import datetime as dt
    days = []
    d = dt.date(2026, 6, 8)
    while d <= dt.date(2026, 8, 28):
        if d.weekday() < 5 and d != dt.date(2026, 7, 3):
            days.append(d)
        d += dt.timedelta(days=1)
    order = sorted(plots, key=lambda p: (W.STAND[p["stand"]]["idx"] % 2, W.STAND[p["stand"]]["idx"], p["plot"]))
    half = len(order) // 2
    for ci, crew in enumerate(("TRF-2", "TRF-3")):
        sub = order[:half] if ci == 0 else order[half:]
        di = 0
        left = int(rng.integers(2, 5))
        for p in sub:
            p["crew26"] = crew
            p["date26"] = days[min(di, len(days) - 1)].isoformat()
            left -= 1
            if left == 0:
                di += 1
                left = int(rng.integers(2, 5))
    v = dt.date(2026, 9, 14)
    for p in sorted(plots, key=lambda p: p["plot"]):
        if p["date26"] in W.SMOKE_DAYS:
            p["revisit"] = v.isoformat()
            if rng.random() < 0.18:
                v += dt.timedelta(days=1)
