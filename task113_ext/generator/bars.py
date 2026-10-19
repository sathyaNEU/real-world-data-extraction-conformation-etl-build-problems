"""The daily bar per security as an exchange-listed stock trades: the close rounded to the tick, the open, high and
low, the closing bid and ask, volume, shares outstanding as the vendor carries it (stepping on each filing date
and on each split's ex-day), and the vendor's total and price returns recomputed from the rounded prices."""
import math

import numpy as np

import prices as PR
import universe as U


def _tick(p):
    return 0.01 if p >= 1.0 else 0.0001


def _rnd(p):
    return PR._round_px(p)


def _down(p):
    t = _tick(p)
    return round(math.floor(p / t + 1e-9) * t, 4)


def _up(p):
    t = _tick(p)
    return round(math.ceil(p / t - 1e-9) * t, 4)


def build(secs, paths, sched):
    rng = U.rng_for(5)
    out = {}
    for s in [s for s in secs if s["kind"] == "spin"] + [s for s in secs if s["kind"] != "spin"]:
        out[s["k"]] = _one(s, paths[s["k"]], sched[s["k"]], paths, out, rng)
    return out


def _one(s, p, sc, paths, done, rng):
    n, i0 = p.n, p.i0
    raw = p.P / p.S
    C = np.array([_rnd(v) for v in raw])
    # spin-off value per parent share from the child's rounded first close
    V = np.zeros(n)
    for e in s["events"]:
        if e[0] == "spinoff":
            ch = done[e[2]]
            V[p.j(e[1])] = p.spin_ratio * ch["close"][0]
    D = p.D.copy()
    F = p.F.copy()
    ret = np.full(n, np.nan)
    retx = np.full(n, np.nan)
    ret[1:] = (C[1:] * F[1:] + D[1:] + V[1:]) / C[:-1] - 1
    retx[1:] = (C[1:] * F[1:]) / C[:-1] - 1
    # shares outstanding: economic units stepping at each filing, times the split factor
    sh_econ0 = (10 ** s["logcap"]) / s["price0"]
    steps = np.zeros(n)
    for r in sc["periods"]:
        fd = r["filed"]
        i = U.day_on_or_after(fd)
        if i0 < i <= p.i1:
            jj = p.j(i)
            if s.get("distress") and i >= s["distress"]["start"]:
                steps[jj] += rng.normal(0.055, 0.02)
            elif s.get("deal") and i >= s["deal"]["announce"]:
                steps[jj] += 0.0
            else:
                steps[jj] += rng.normal(-0.0035, 0.007)
    sh_econ = sh_econ0 * np.exp(np.cumsum(steps))
    shares = np.round(sh_econ * p.S).astype(np.int64)
    # open, high, low
    sd = p.sd
    phi = rng.uniform(0.1, 0.5, n)
    phi[p.reaction] = rng.uniform(0.7, 0.95, int(p.reaction.sum()))
    deal = s.get("deal")
    if deal and deal["announce"] <= p.i1:
        phi[p.j(deal["announce"])] = 0.98
    O = np.zeros(n)
    H = np.zeros(n)
    L = np.zeros(n)
    for jj in range(n):
        if jj == 0:
            base = (s["ipo_offer"] or C[0]) if s["kind"] == "ipo" else C[0] / math.exp(rng.normal(0, sd[0] * 0.6))
            o = base * (math.exp(rng.normal(0.06, 0.08)) if s["kind"] == "ipo" else 1.0)
        else:
            prev = (C[jj - 1] - D[jj] - V[jj]) / F[jj]
            move = math.log(C[jj] / prev) if prev > 0 and C[jj] > 0 else 0.0
            o = prev * math.exp(phi[jj] * move + rng.normal(0, sd[jj] * 0.25))
        o = _rnd(o)
        hi = max(o, C[jj]) * math.exp(abs(rng.normal(0, sd[jj] * 0.55)))
        lo = min(o, C[jj]) * math.exp(-abs(rng.normal(0, sd[jj] * 0.55)))
        hi, lo = _up(hi), _down(lo)
        hi = max(hi, o, C[jj])
        lo = min(lo, o, C[jj])
        O[jj], H[jj], L[jj] = o, hi, lo
    # closing quote
    hs = C * s["spread_bp"] / 2e4 * np.exp(rng.normal(0, 0.3, n))
    if s.get("distress"):
        hs *= np.where(np.arange(i0, i0 + n) >= s["distress"]["start"], 2.5, 1.0)
    bid = np.array([_down(C[j] - hs[j] * rng.uniform(0.2, 1.0)) for j in range(n)])
    ask = np.array([_up(C[j] + hs[j] * rng.uniform(0.2, 1.0)) for j in range(n)])
    for j in range(n):
        if bid[j] >= ask[j]:
            ask[j] = round(bid[j] + _tick(bid[j]), 4)
        if bid[j] <= 0:
            bid[j] = _tick(C[j])
    # volume
    mult = np.ones(n)
    mult[p.reaction] *= rng.uniform(2.2, 4.0, int(p.reaction.sum()))
    nxt = np.roll(p.reaction, 1)
    nxt[0] = False
    mult[nxt] *= 1.4
    if deal and deal["announce"] <= p.i1:
        a = p.j(deal["announce"])
        mult[a] *= rng.uniform(6, 12)
        for k in range(1, 8):
            if a + k < n:
                mult[a + k] *= 1 + 4 * 0.7 ** k
        if deal.get("close") and deal["close"] - 1 == p.i1:
            mult[-1] *= 3.0
    for sp in p.splits:
        mult[p.j(sp["ex"])] *= 1.4
    for e in s["events"]:
        if e[0] in ("spinoff", "spun"):
            mult[p.j(e[1])] *= 3.0 if e[0] == "spinoff" else 6.0
    if s.get("distress"):
        mult *= np.where(np.arange(i0, i0 + n) >= s["distress"]["start"], 1.8, 1.0)
    x = np.zeros(n)
    x[1:] = np.log(np.maximum(C[1:] * F[1:] + D[1:] + V[1:], 1e-9) / C[:-1])
    vol = shares * s["turnover"] * np.exp(rng.normal(0, 0.38, n)) * (1 + 1.6 * np.abs(x) / sd) ** 0.8 * mult
    if s["kind"] == "ipo":
        vol[0] = shares[0] * rng.uniform(0.22, 0.4)
        vol[1:6] *= 2.5
    vol = np.round(vol).astype(np.int64)
    ctype = np.array(["T"] * n, dtype=object)
    if s["logcap"] < 8.62:
        quiet = (rng.random(n) < 0.004) & ~p.reaction & (p.F == 1.0) & (D == 0)
        quiet[0] = False
        for j in np.nonzero(quiet)[0]:
            vol[j] = 0
            mid = (bid[j] + ask[j]) / 2
            C[j] = round(mid, 4)
            O[j] = H[j] = L[j] = np.nan
            ctype[j] = "M"
        ret[1:] = (C[1:] * F[1:] + D[1:] + V[1:]) / C[:-1] - 1
        retx[1:] = (C[1:] * F[1:]) / C[:-1] - 1
    return dict(close=C, open=O, high=H, low=L, bid=bid, ask=ask, volume=vol, shares=shares, ret=ret, retx=retx,
                ctype=ctype, F=F, D=D, V=V, S=p.S.copy(), i0=i0, i1=p.i1)
