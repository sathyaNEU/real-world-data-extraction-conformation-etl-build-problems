"""The figure the annual report carries, and every rung below it."""
import math

import estimators as E
import world as W

BAND_LO, BAND_HI = int(W.BAND_LO), int(W.BAND_HI)
FIT_LO, FIT_HI, STEP = 5000, 16000, 250


def excess(amounts, lo=FIT_LO, hi=FIT_HI, step=STEP, family="poisson_log", side="both"):
    return E.excess(amounts, lo, hi, step, family, side)


def r10(x):
    return int(math.floor(x / 10.0 + 0.5) * 10)


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

    # the figure: each segment's own profile, its own band
    per_seg, per_seg_raw = {}, {}
    for k in W.SEG_KEYS:
        v = excess(amt_by_seg[k])
        per_seg_raw[k] = v
        per_seg[k] = r10(v)
    total = sum(per_seg.values())

    # the band as observed, and the year's deposits, per segment
    band_obs = {k: sum(1 for a in amt_by_seg[k] if BAND_LO <= a < BAND_HI) for k in W.SEG_KEYS}
    deposits = {k: len(amt_by_seg[k]) for k in W.SEG_KEYS}

    # ---- the rungs -------------------------------------------------------
    # rung 0, the same-day screen: a band deposit on a day the customer's cash reached
    # the threshold over two or more deposits, none of them at or above it
    def day_map(rs):
        d = {}
        for r in rs:
            d.setdefault((r["cust"], r["date"]), []).append(r["amount"])
        return d

    dw = day_map(win)
    # the screen a solver builds from handbook 3.2: two or more deposits on a customer's day
    # reaching the threshold between them, none of them reaching it alone
    screened_days = {key for key, a in dw.items()
                     if len(a) >= 2 and sum(a) >= W.THRESHOLD and
                     any(x < W.THRESHOLD for x in a)}
    rung0_seg = {k: 0 for k in W.SEG_KEYS}
    for (cust, day), a in dw.items():
        if (cust, day) in screened_days:
            for x in a:
                if BAND_LO <= x < BAND_HI:
                    rung0_seg[seg_of[cust]] += 1
    rung0 = sum(rung0_seg.values())

    # rung 1, the same screen with each customer's own habit netted out
    days_by_cust, screened_by_cust = {}, {}
    for (cust, day), a in dw.items():
        days_by_cust[cust] = days_by_cust.get(cust, 0) + 1
        if (cust, day) in screened_days:
            screened_by_cust[cust] = screened_by_cust.get(cust, 0) + 1
    habit = {c for c in days_by_cust
             if screened_by_cust.get(c, 0) > 0.5 * days_by_cust[c]}
    rung1_seg = {k: 0 for k in W.SEG_KEYS}
    for (cust, day), a in dw.items():
        if (cust, day) in screened_days and cust not in habit:
            for x in a:
                if BAND_LO <= x < BAND_HI:
                    rung1_seg[seg_of[cust]] += 1
    rung1 = sum(rung1_seg.values())

    # rung 2, each customer against its own prior year
    bw_, bp_ = {}, {}
    for r in win:
        if BAND_LO <= r["amount"] < BAND_HI:
            bw_[r["cust"]] = bw_.get(r["cust"], 0) + 1
    for r in pri:
        if BAND_LO <= r["amount"] < BAND_HI:
            bp_[r["cust"]] = bp_.get(r["cust"], 0) + 1
    rung2_seg = {k: 0 for k in W.SEG_KEYS}
    for c in set(list(bw_) + list(bp_)):
        rise = bw_.get(c, 0) - bp_.get(c, 0)
        if rise > 0:
            rung2_seg[seg_of[c]] += rise
    rung2 = sum(rung2_seg.values())

    # the band count itself, below rung 0
    band_all = sum(band_obs.values())

    # one profile fitted to the whole book: convergent here, kept as a reported figure
    pooled = excess(all_amt)
    pooled_seg = {}
    share = {k: band_obs[k] / float(band_all) for k in W.SEG_KEYS}
    for k in W.SEG_KEYS:
        pooled_seg[k] = r10(band_obs[k] - (band_all - pooled) * share[k])

    return dict(per_seg=per_seg, per_seg_raw=per_seg_raw, total=total,
                band_obs=band_obs, deposits=deposits, band_all=band_all,
                rung0=rung0, rung0_seg=rung0_seg, rung1=rung1, rung1_seg=rung1_seg,
                rung2=rung2, rung2_seg=rung2_seg, pooled=pooled, pooled_seg=pooled_seg,
                pooled_total=r10(pooled),
                amt_by_seg=amt_by_seg, amt_by_seg_prior=amt_by_seg_prior, all_amt=all_amt,
                n_win=len(win), n_pri=len(pri), n_rows=len(rows))


def convergence(g):
    """Every estimator in the sweep, per segment, and the book totals they imply."""
    out = {k: E.sweep(g["amt_by_seg"][k]) for k in W.SEG_KEYS}
    labels = [lab for lab, _ in out[W.SEG_KEYS[0]]]
    totals = [sum(out[k][i][1] for k in W.SEG_KEYS) for i in range(len(labels))]
    return out, totals, labels


def rounded_sets(out):
    """The eight rounded segment figures each estimator gives, and their sum."""
    sets = []
    for i in range(len(out[W.SEG_KEYS[0]])):
        sets.append(tuple(r10(out[k][i][1]) for k in W.SEG_KEYS))
    return sets
