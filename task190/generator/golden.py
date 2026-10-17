"""The figure the annual report carries, and every rung below it."""
import math

import estimators as E
import world as W

BAND_LO, BAND_HI = int(W.BAND_LO), int(W.BAND_HI)
FIT_LO, FIT_HI, STEP = 5000, 16000, 250
GRAIN = W.GRAIN


def r50(x):
    return int(math.floor(x / float(GRAIN) + 0.5) * GRAIN)


def canonical(amounts):
    """The segment's figure: the band's surplus and 10,000 to 11,000's deficit, reconciled."""
    return E.reconciled(amounts, FIT_LO, FIT_HI, STEP, "poisson", 1)


def compute(custs, bycust, rows):
    seg_of = {c["cust"]: c["seg"] for c in custs}
    win = [r for r in rows if r["year"] == "2027"]
    pri = [r for r in rows if r["year"] == "2026"]

    amt_by_seg, amt_by_seg_prior, all_amt = {}, {}, []
    for r in win:
        amt_by_seg.setdefault(seg_of[r["cust"]], []).append(r["amount"])
        all_amt.append(r["amount"])
    for r in pri:
        amt_by_seg_prior.setdefault(seg_of[r["cust"]], []).append(r["amount"])

    per_seg, per_seg_raw, sides = {}, {}, {}
    for k in W.SEG_KEYS:
        sides[k] = E.sides(amt_by_seg[k], FIT_LO, FIT_HI, STEP, "poisson", 1)
        v = canonical(amt_by_seg[k])
        per_seg_raw[k] = v
        per_seg[k] = r50(v)
    total = sum(per_seg.values())

    band_obs = {k: sum(1 for a in amt_by_seg[k] if BAND_LO <= a < BAND_HI) for k in W.SEG_KEYS}
    mirror_obs = {k: sum(1 for a in amt_by_seg[k] if BAND_HI <= a < E.MIRROR_HI)
                  for k in W.SEG_KEYS}
    deposits = {k: len(amt_by_seg[k]) for k in W.SEG_KEYS}

    # ---- the rungs -------------------------------------------------------
    # rung 0, the band counted as it stands: the near-threshold queue's own size
    band_all = sum(band_obs.values())

    # rung 1, the same-day screen a solver builds from the alert at handbook 3.2
    def day_map(rs):
        d = {}
        for r in rs:
            d.setdefault((r["cust"], r["date"]), []).append(r["amount"])
        return d

    dw = day_map(win)
    screened = {key for key, a in dw.items()
                if len(a) >= 2 and sum(a) >= W.THRESHOLD and any(x < W.THRESHOLD for x in a)}
    screen_seg = {k: 0 for k in W.SEG_KEYS}
    for (cust, day), a in dw.items():
        if (cust, day) in screened:
            for x in a:
                if BAND_LO <= x < BAND_HI:
                    screen_seg[seg_of[cust]] += 1
    screen = sum(screen_seg.values())

    # rung 2, the band fitted on its own, with the deficit above left in the fit
    one_seg, one_raw = {}, {}
    for k in W.SEG_KEYS:
        v = E.one_sided(amt_by_seg[k], FIT_LO, FIT_HI, STEP)
        one_raw[k] = v
        one_seg[k] = r50(v)
    one_total = sum(one_seg.values())

    # rung 3, each customer's band deposits against its own prior year
    bw_, bp_ = {}, {}
    for r in win:
        if BAND_LO <= r["amount"] < BAND_HI:
            bw_[r["cust"]] = bw_.get(r["cust"], 0) + 1
    for r in pri:
        if BAND_LO <= r["amount"] < BAND_HI:
            bp_[r["cust"]] = bp_.get(r["cust"], 0) + 1
    rise_seg = {k: 0 for k in W.SEG_KEYS}
    for c in set(list(bw_) + list(bp_)):
        d = bw_.get(c, 0) - bp_.get(c, 0)
        if d > 0:
            rise_seg[seg_of[c]] += d
    rise = sum(rise_seg.values())

    # the prior year on the same reading, which the report does not state but the pack supports
    prior_seg = {k: r50(canonical(amt_by_seg_prior[k])) for k in W.SEG_KEYS}
    prior_total = sum(prior_seg.values())

    largest = max(W.SEG_KEYS, key=lambda k: (per_seg[k], -W.SEG_KEYS.index(k)))
    largest_band = max(W.SEG_KEYS, key=lambda k: band_obs[k])
    largest_book = max(W.SEG_KEYS, key=lambda k: deposits[k])

    return dict(per_seg=per_seg, per_seg_raw=per_seg_raw, sides=sides, total=total,
                band_obs=band_obs, mirror_obs=mirror_obs, deposits=deposits, band_all=band_all,
                screen=screen, screen_seg=screen_seg,
                one_seg=one_seg, one_raw=one_raw, one_total=one_total,
                rise=rise, rise_seg=rise_seg,
                prior_seg=prior_seg, prior_total=prior_total,
                largest=largest, largest_band=largest_band, largest_book=largest_book,
                amt_by_seg=amt_by_seg, amt_by_seg_prior=amt_by_seg_prior, all_amt=all_amt,
                n_win=len(win), n_pri=len(pri), n_rows=len(rows))


def convergence(g):
    """Every specification the record leaves standing, and the segment figures each gives."""
    return E.sweep(g["amt_by_seg"], W.SEG_KEYS)


def rounded_sets(sw):
    """The eight stated segment figures each surviving specification gives, and their sum."""
    return [tuple(r50(v[k]) for k in W.SEG_KEYS) for _, v in sw]


def edges(sw):
    """How far every segment's figure sits from the nearest rounding edge, over the set."""
    out = {}
    for k in W.SEG_KEYS:
        vs = [v[k] for _, v in sw]
        cell = r50(sum(vs) / len(vs))
        out[k] = min(min(vs) - (cell - GRAIN / 2.0), (cell + GRAIN / 2.0) - max(vs))
    return out
