"""The estimators on the shipped pack: the golden (each card weighted by the inverse of the share of its wave's handed
cards whose handout day left room for its stay to end by the last box collection) and every rung of the ladder."""
import numpy as np

import bundle as B

WAVE_QUARTER = {1: 1, 2: 2, 3: 3, 4: 4}


def collect_weights(P, by="handed", close_shift=0):
    """W[(wave, lot or None, nights)]: the wave's cards handed over those handed on the days whose stays of these
    nights could end by the wave's last box collection. by='handed' (the log's counts), 'lot' (each lot's own counts)
    or 'days' (every handout day counted once)."""
    out = {}
    for w in sorted(P.wave_start):
        T = P.close_day[w] + close_shift
        for lot in ([None] if by != "lot" else B.LOTS):
            h = P.handed_by_day(w, lot)
            days = sorted(h)
            for L in range(0, 29):
                ok = [t for t in days if t + L <= T]
                if by == "days":
                    out[(w, lot, L)] = len(days) / len(ok)
                else:
                    out[(w, lot, L)] = sum(h[t] for t in days) / sum(h[t] for t in ok)
    return out


def card_weights(P, how="collect", by="handed", close_shift=0):
    n = len(P.cards)
    if how == "raw":
        return np.ones(n)
    if how == "collect":
        Wt = collect_weights(P, by, close_shift)
        lot_key = (lambda i: B.LOTS[P.lot[i]]) if by == "lot" else (lambda i: None)
        return np.array([Wt[(P.wave[i], lot_key(i), P.L[i])] for i in range(n)])
    if how == "day":           # each handout day's cards reweighted to the cards handed that day
        h = {}
        r = {}
        for w in sorted(P.wave_start):
            hd = P.handed_by_day(w)
            for t, v in hd.items():
                h[(w, t)] = v
        for i in range(n):
            r[(P.wave[i], P.t[i])] = r.get((P.wave[i], P.t[i]), 0) + 1
        return np.array([h[(P.wave[i], P.t[i])] / r[(P.wave[i], P.t[i])] for i in range(n)])
    if how == "inverse_nights":
        return 1.0 / np.maximum(P.L, 0.5)
    if how == "first14":
        return (P.t <= 14).astype(float)
    raise ValueError(how)


def estimate(P, how="collect", by="handed", unit="trips", party="written", post=False, pooled=False, garage=False,
             permits=False, close_shift=0, sa_only=False, airport=False, waves=None):
    """Each candidate market's 2026 trips (or passengers) from the service area: each wave's weighted share of its
    cards expanded to its quarter's transient entries in the long-stay lots, the four quarters added."""
    w = card_weights(P, how, by, close_shift)
    mult = np.ones(len(P.cards))
    if unit == "passengers":
        mult = {"written": P.party, "coded": P.party_coded, "summed": P.party_summed,
                "ones": np.ones(len(P.cards))}[party]
    E = P.quarter_entries(garage, permits)
    EL = P.lot_quarter_entries()
    mkt = P.dest if airport else P.mkt
    out = {}
    if pooled:
        tot = w.sum()
        base = sum(E.values())
        for m in set(mkt[P.sa]):
            sel = P.sa & (mkt == m)
            out[m] = base * float((w[sel] * mult[sel]).sum()) / tot
        return out
    for wave in sorted(P.wave_start):
        if waves is not None and wave not in waves:
            continue
        q = WAVE_QUARTER[wave]
        cells = [(None, P.wave == wave)] if not post else [(lot, (P.wave == wave) & (P.lot == li))
                                                          for li, lot in enumerate(B.LOTS)]
        for lot, cell in cells:
            base = E[q] if lot is None else EL[(q, lot)]
            tot = float(w[cell & P.sa].sum()) if sa_only else float(w[cell].sum())
            sel = cell & P.sa
            for m in set(mkt[sel]):
                s2 = sel & (mkt == m)
                out[m] = out.get(m, 0.0) + base * float((w[s2] * mult[s2]).sum()) / tot
    return out


def ranking(est, candidates):
    return sorted(((m, est.get(m, 0.0)) for m in candidates), key=lambda x: (-x[1], x[0]))


def top3(est, candidates):
    return [m for m, _ in ranking(est, candidates)[:3]]


RUNGS = [   # name, description, keyword arguments
    ("R0", "each wave's returned cards expanded to its quarter's entries", dict(how="raw")),
    ("R1", "R0 with each card reweighted to the cards handed on its handout day", dict(how="day")),
    ("R2", "R0 with each card weighted by one over its nights", dict(how="inverse_nights")),
    ("R3", "each card weighted by the inverse of the share of handed cards whose handout day left room for its stay",
     dict(how="collect")),
]
OTHER_ROUTES = [
    ("pooled", "the four waves' returned cards pooled and expanded to the year's entries", dict(how="raw", pooled=True)),
    ("first14", "only the cards handed on a wave's first 14 days", dict(how="first14")),
    ("post", "R0 post-stratified to each lot's entries", dict(how="raw", post=True)),
    ("garage", "R0 with the garage's entries in the base", dict(how="raw", garage=True)),
]
PARTIAL_FIXES = ("first14",)
GOLDEN_VARIANTS = [
    ("golden", dict(how="collect")),
    ("per_lot", dict(how="collect", by="lot")),
    ("post", dict(how="collect", post=True)),
    ("post_lot", dict(how="collect", by="lot", post=True)),
]
