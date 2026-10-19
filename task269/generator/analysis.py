"""The analysis, shared by checks.py (on the generator's clean truth) and verify.py (on the shipped files): excess
wait in cells (timing point, peak, census day, set of departures), each corridor boarding given its cell, and every
route's figure under the golden, every reflex of the sweep and every member of the golden's own family.

Tables: deps has one row per departure at a timing point (day, route, direction, trip, variant, stop, sched, actual,
minutes after midnight); jour one row per journey (day, route, direction, trip, variant, board, alight or None, on);
geo holds each route-direction's corridor stops in order, which of them are timing points, and which variants serve
every stop of the route in that direction."""
import collections

import numpy as np
import pandas as pd

import common as K

PEAKS = K.PEAKS


def awt(h):
    h = np.asarray(h, float)
    return float((h ** 2).sum() / (2 * h.sum())) if len(h) else float("nan")


def geometry(patterns, corridor, is_tp):
    """corridor[(route, dir)]: stops in travel order; is_tp: stop -> bool; patterns[(route, dir, variant)]: stops.
    Returns per route-direction: the corridor list, its timing points, each corridor stop's timing point, and each
    stop's serving variants."""
    geo = {}
    for (rt, d), cor in corridor.items():
        tps = [s for s in cor if is_tp(s)]
        tp_of, cur = {}, None
        for s in cor:
            if is_tp(s):
                cur = s
            tp_of[s] = cur
        serve = collections.defaultdict(set)
        for (r2, d2, v), pat in patterns.items():
            if r2 == rt and d2 == d:
                for s in pat:
                    serve[s].add(v)
        geo[(rt, d)] = dict(cor=cor, cor_set=set(cor), tps=tps, tp_of=tp_of, serve=dict(serve))
    return geo


def _window(x, t0, t1):
    x = np.sort(np.asarray(x, float))
    return x[(x >= t0) & (x < t1)]


def cells(deps, pooled=False, sched_col="sched", act_col="actual"):
    """Excess wait per (day, route, direction, peak, timing point, set) with set 'ALL', 'A' or 'B' (branched routes),
    worked from the departures inside the peak: the random-arrival wait over the actual headways less the same over
    the timetable's. pooled=True pools each cell's headways over the census days (a family member)."""
    out = {}
    g = deps.groupby(["route", "direction", "stop"] + ([] if pooled else ["day"]), sort=True)
    for key, df in g:
        rt, d, stop = key[:3]
        day = None if pooled else key[3]
        sets = ["ALL"] + (["A", "B"] if rt in K.BRANCHED else [])
        for pk, (t0, t1) in PEAKS.items():
            for st in sets:
                sub = df if st == "ALL" else df[df["variant"] == st]
                if pooled:
                    ha, hs = [], []
                    for _, dd in sub.groupby("day"):
                        ha.append(np.diff(_window(dd[act_col], t0, t1)))
                        hs.append(np.diff(_window(dd[sched_col], t0, t1)))
                    a = awt(np.concatenate(ha)) if ha else float("nan")
                    s = awt(np.concatenate(hs)) if hs else float("nan")
                else:
                    a, s = awt(np.diff(_window(sub[act_col], t0, t1))), awt(np.diff(_window(sub[sched_col], t0, t1)))
                out[(day, rt, d, pk, stop, st)] = (a - s, a, s)
    return out


def peak_of(t):
    for pk, (t0, t1) in PEAKS.items():
        if t0 <= t < t1:
            return pk
    return None


def corridor_boardings(jour, geo):
    """The corridor boardings in the census peaks, each with its timing point, its peak and the set of departures
    that can carry it (the golden's usable set: from the tap-off stop outbound, every bus inbound; "?" when the
    tap-off is missing)."""
    rows = []
    for r in jour.itertuples(index=False):
        G = geo[(r.route, r.direction)]
        if r.board not in G["cor_set"]:
            continue
        pk = peak_of(r.on)
        if pk is None:
            continue
        if r.route in K.BRANCHED and r.direction == "out":
            if r.alight is None or (isinstance(r.alight, float) and np.isnan(r.alight)):
                use = "?"
            else:
                sv = G["serve"].get(int(r.alight), set())
                use = "ALL" if sv == {"A", "B"} else (next(iter(sv)) if len(sv) == 1 else "?")
        else:
            use = "ALL"
        rows.append((r.day, r.route, r.direction, pk, G["tp_of"][r.board], r.trip, r.variant, use))
    return pd.DataFrame(rows, columns=["day", "route", "direction", "peak", "tp", "trip", "variant", "use"])


def figures(cb, cl, method="golden", missing="impute"):
    """Each route's excess wait per corridor boarding under a method:
    golden  each boarding over its usable set (outbound tap-off; inbound every bus)
    R0      every boarding over all of the route's departures
    R1      every boarding over the branch of the bus it boarded
    R2      inbound over all departures, outbound over the boarded bus's branch
    R2b     outbound over its usable set, inbound over the boarded bus's branch
    Rx      the golden with the branch-bound boardings left out
    missing (golden family): impute (a boarding with no tap-off takes the average of its cell's tapped-off
    boardings), drop, all (as if corridor-bound), boarded (its bus's branch)."""
    tot = collections.defaultdict(float)
    cnt = collections.defaultdict(float)
    grp = cb.groupby(["day", "route", "direction", "peak", "tp"], sort=True)
    for (day, rt, d, pk, tp), df in grp:
        def e(st):
            return cl[(day, rt, d, pk, tp, st)][0]
        vals = []
        n_missing = 0
        for u, v in zip(df["use"], df["variant"]):
            br = rt in K.BRANCHED
            if method == "R0":
                vals.append(e("ALL"))
            elif method == "R1":
                vals.append(e(v) if br else e("ALL"))
            elif method == "R2":
                vals.append(e(v) if (br and d == "out") else e("ALL"))
            else:
                if u == "?":
                    if missing == "drop":
                        continue
                    if missing == "all":
                        vals.append(e("ALL"))
                        continue
                    if missing == "boarded":
                        vals.append(e(v))
                        continue
                    n_missing += 1
                    continue
                if method == "Rx" and u in ("A", "B"):
                    continue
                if method == "R2b" and br and d == "in":
                    vals.append(e(v))
                    continue
                vals.append(e(u))
        if n_missing and vals:
            vals.extend([float(np.mean(vals))] * n_missing)
        tot[rt] += float(np.sum(vals)) if vals else 0.0
        cnt[rt] += len(vals)
    return {rt: tot[rt] / cnt[rt] for rt in K.ROUTES if cnt[rt]}


def figures_unweighted(cl):
    """R0u: the route-level excess wait with every cell (timing point, peak, day) counted once."""
    acc = collections.defaultdict(list)
    for (day, rt, d, pk, tp, st), (e, a, s) in cl.items():
        if st == "ALL" and not np.isnan(e):
            acc[rt].append(e)
    return {rt: float(np.mean(v)) for rt, v in acc.items()}


def figures_peak_direction(cb, cl):
    """R0p: the route-level measure on the peak direction only (morning inbound, afternoon outbound)."""
    keep = cb[((cb["peak"] == "AM") & (cb["direction"] == "in")) | ((cb["peak"] == "PM") & (cb["direction"] == "out"))]
    return figures(keep, cl, "R0")


def figures_half_gap(cb, deps, cl, usable=False):
    """Rh (usable=False): each boarding credited half the gap before the bus it took at its timing point, over all
    the route's departures, less the timetable's random-arrival wait over all of them; usable=True takes the gap and
    the timetable over the boarding's usable set (a member of the golden's family, not the standard's formula)."""
    prev = {}
    for (day, rt, d, stop), df in deps.groupby(["day", "route", "direction", "stop"], sort=True):
        df = df.sort_values("actual")
        t = df["actual"].to_numpy()
        trips = df["trip"].tolist()
        var = df["variant"].tolist()
        gap_all = np.concatenate([[np.nan], np.diff(t)])
        for i, tr in enumerate(trips):
            prev[(day, tr, stop, "ALL")] = gap_all[i]
        for v in ("A", "B"):
            idx = [i for i, x in enumerate(var) if x == v]
            for a, b in zip(idx[:-1], idx[1:]):
                prev[(day, trips[b], stop, v)] = t[b] - t[a]
    tot = collections.defaultdict(float)
    cnt = collections.defaultdict(float)
    for r in cb.itertuples(index=False):
        st = (r.use if r.use != "?" else "ALL") if usable else "ALL"
        g = prev.get((r.day, r.trip, r.tp, st))
        if g is None or np.isnan(g):
            continue
        tot[r.route] += g / 2 - cl[(r.day, r.route, r.direction, r.peak, r.tp, st)][2]
        cnt[r.route] += 1
    return {rt: tot[rt] / cnt[rt] for rt in K.ROUTES if cnt[rt]}


def top(fig, n=K.TEAMS):
    return sorted(fig, key=lambda r: -fig[r])[:n]


def ranking(fig):
    return sorted(fig, key=lambda r: -fig[r])
