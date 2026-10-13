"""task231 estimators: the September 2026 round's response rate per region under each route the ladder names, from the
simulation's records (the generator's view; verify.py recomputes the same from the shipped files)."""
from collections import defaultdict
from datetime import date

import params as P

REGS = [r[0] for r in P.REGIONS]
NAMES = {r[0]: r[1] for r in P.REGIONS}


def months_before(d, n):
    y, m = d.year, d.month - n
    while m <= 0:
        y, m = y - 1, m + 12
    return date(y, m, 1)


def known_closed(f, o, asof):
    return f["registered"] <= asof and f["ceased"] <= o["frame"]


def settled_share(pan, last_frame, key=lambda f, o: "all", first_frame=None, pool="close", exclude="close",
                  dead_by="frame", asof=P.EXTRACT):
    """Share of earlier rounds' non-returners that the register, as at `asof`, shows had ceased by the round's frame
    date. pool: non-returners at the main close ("close") or at the round's end ("end"); exclude: drop the ones the
    register already showed closed at the close ("close"), at the round's end ("end"), or none ("none"); dead_by:
    ceased on or before the frame date ("frame") or the close ("close")."""
    num, den = defaultdict(int), defaultdict(int)
    for o in pan.outcomes:
        fr = o["frame"]
        if fr >= P.CURRENT or fr > last_frame or (first_frame and fr < first_frame):
            continue
        f = pan.firms[o["fid"]]
        if pool == "close":
            if o["by_close"]:
                continue
        elif o["ret_day"] is not None:
            continue
        if exclude == "close" and known_closed(f, o, o["close"]):
            continue
        if exclude == "end" and known_closed(f, o, o["end"]):
            continue
        limit = fr if dead_by == "frame" else o["close"]
        dead = f["registered"] <= asof and f["ceased"] <= limit
        kx = key(f, o)
        den[kx] += 1
        num[kx] += dead
    return {k: num[k] / den[k] for k in den}, den


def current(pan):
    """Per region: invited, returns by the close, known closed, unknown non-returners with their records."""
    out = {r: dict(inv=0, R=0, known=0, nr=[], dead=0) for r in REGS}
    for o in pan.outcomes:
        if o["frame"] != P.CURRENT:
            continue
        f = pan.firms[o["fid"]]
        c = out[o["region"]]
        c["inv"] += 1
        if o["by_close"]:
            c["R"] += 1
            continue
        if known_closed(f, o, P.EXTRACT):
            c["known"] += 1
            continue
        c["nr"].append((f, o))
        c["dead"] += (not o["alive"])
    return out


SETTLED_WINDOWS = (36, 42, 48, 54, 60, 72)


def corridor_shares(pan):
    """Every settled-round estimator the closure table names: pooled over windows from 36 to 72 months, by region, by
    rounds silent, by region and rounds silent, by size band, pooled at the round's end, excluding closures known at
    the round's end, counting closures to the close, and with no exclusion."""
    last = months_before(P.EXTRACT, P.SETTLED_MONTHS)
    kk = lambda o: min(o["k"], P.RETIRE_AFTER)
    out = {}
    for w in SETTLED_WINDOWS:
        out["w%d" % w] = settled_share(pan, months_before(P.EXTRACT, w))[0]
    out["region"] = settled_share(pan, last, key=lambda f, o: f["region"])[0]
    out["k"] = settled_share(pan, last, key=lambda f, o: kk(o))[0]
    out["rk"] = settled_share(pan, last, key=lambda f, o: (f["region"], kk(o)))[0]
    out["size"] = settled_share(pan, last, key=lambda f, o: f["size"])[0]
    out["end"] = settled_share(pan, last, pool="end")[0]
    out["excl_end"] = settled_share(pan, last, exclude="end")[0]
    out["excl_none"] = settled_share(pan, last, exclude="none")[0]
    out["dead_close"] = settled_share(pan, last, dead_by="close")[0]
    return out


def corridor_rates(pan, cur=None, sh=None):
    """each corridor estimator's rate per region"""
    cur = cur or current(pan)
    sh = sh or corridor_shares(pan)
    kk = lambda o: min(o["k"], P.RETIRE_AFTER)
    res = {}
    for r in REGS:
        c = cur[r]
        R, nr = c["R"], c["nr"]
        n = len(nr)
        rate = lambda inscope: 100.0 * R / (R + inscope)
        v = {}
        for name, s in sh.items():
            if name == "region":
                v[name] = rate(n * (1 - s[r]))
            elif name == "k":
                v[name] = rate(sum(1 - s[kk(o)] for f, o in nr))
            elif name == "rk":
                v[name] = rate(sum(1 - s.get((r, kk(o)), sh["k"][kk(o)]) for f, o in nr))
            elif name == "size":
                v[name] = rate(sum(1 - s[f["size"]] for f, o in nr))
            else:
                v[name] = rate(n * (1 - s["all"]))
        res[r] = v
    return res


def routes(pan):
    cur = current(pan)
    settled_last = months_before(P.EXTRACT, P.SETTLED_MONTHS)
    s_set, _ = settled_share(pan, settled_last)
    s_all, _ = settled_share(pan, months_before(P.CURRENT, 3))
    s_recent, _ = settled_share(pan, months_before(P.CURRENT, 3), first_frame=months_before(P.CURRENT, 24))
    corr = corridor_rates(pan, cur)
    res = {}
    for r in REGS:
        c = cur[r]
        R, nr = c["R"], c["nr"]
        n = len(nr)
        alive_res = sum(1 for f, o in nr if o["call"] in ("refused", "promised"))
        closed_res = sum(1 for f, o in nr if o["call"] == "ceased")
        unob = sum(1 for f, o in nr if o["call"] == "unobtainable")
        unres = n - alive_res - closed_res
        e = alive_res / (alive_res + closed_res) if alive_res + closed_res else 1.0
        rate = lambda inscope: 100.0 * R / (R + inscope)
        res[r] = dict(
            inv=c["inv"], R=R, known=c["known"], nru=n, dead=c["dead"], e=e,
            R0=100.0 * R / c["inv"],
            R1=rate(n),
            casro=rate(alive_res + e * unres),
            unob=rate(n - closed_res - unob),
            allr=rate(n * (1 - s_all["all"])),
            recent=rate(n * (1 - s_recent["all"])),
            golden=rate(n * (1 - s_set["all"])),
            over=rate(alive_res),
            truth=rate(n - c["dead"]),
            inscope_golden=n * (1 - s_set["all"]),
            corridor=corr[r],
        )
    shares = dict(settled=s_set["all"], all=s_all["all"], recent=s_recent["all"])
    return res, shares
