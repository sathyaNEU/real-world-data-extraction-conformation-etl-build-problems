"""The slot figures and the slate: the constructions a tasking analyst can put on an occurrence window, and
the figures the paper and the workbook carry. Nothing here ships; the pack carries records, the goldens
carry answers.

The contract's covered-offence count is the number of offences of its classes that occurred in each slot,
and the record does not hold the time any windowed offence occurred, so the count has to be estimated from
the windows. Five constructions are available on the record alone and they give five different slates.
"""
import datetime as dt

import numpy as np

import offences as O
import world as W

HW = W.HOURS_WEEK
SLOT_OF = np.arange(HW) // W.SLOT_H
SLOT_KEY = [(h // 24, (h % 24) // W.SLOT_H * W.SLOT_H) for h in range(0, HW, W.SLOT_H)]


def slot_start(ts):
    """Midnight-anchored start of the four-hour slot ts falls in."""
    return ts.replace(minute=0, second=0, microsecond=0, hour=(ts.hour // W.SLOT_H) * W.SLOT_H)


def hours_of(r):
    """The hours of the week an offence's record admits: its window's hours, or the one hour it happened in."""
    a = O.hour_of_week(r["from"])
    span = int(round((r["to"] - r["from"]).total_seconds() / 3600.0))
    if span <= 0:
        return np.array([a], dtype=np.int64)
    return (a + np.arange(span, dtype=np.int64)) % HW


def as_slots(hour_vec):
    """A 168-hour vector folded into the week's 42 four-hour slots, keyed as the rest of the build keys them."""
    agg = np.bincount(SLOT_OF, weights=hour_vec, minlength=HW // W.SLOT_H)
    return {SLOT_KEY[i]: float(agg[i]) for i in range(len(SLOT_KEY))}


def _coverage(rows):
    """The record collapsed to its distinct window shapes, with how many offences carry each.

    Two offences recorded with the same window enter the record's likelihood the same way, so the iteration
    runs over the distinct shapes with counts rather than over the rows. Same fixed point to the last
    decimal, and the record carries about two and a half thousand shapes against twenty-five thousand rows.
    """
    shapes = {}
    for r in rows:
        a = O.hour_of_week(r["from"])
        span = int(round((r["to"] - r["from"]).total_seconds() / 3600.0))
        key = (a, max(span, 0))
        shapes[key] = shapes.get(key, 0) + 1
    keys = sorted(shapes)
    hrs = [np.array([a], dtype=np.int64) if ln == 0 else (a + np.arange(ln, dtype=np.int64)) % HW
           for a, ln in keys]
    flat = np.concatenate(hrs)
    owner = np.concatenate([np.full(len(h), i, dtype=np.int64) for i, h in enumerate(hrs)])
    mult = np.array([shapes[k] for k in keys], dtype=float)
    return hrs, flat, owner, mult


def _em(hrs, flat, owner, mult, start=None, tol=1e-13, iters=8000, group=None):
    """One self-consistent run over the record's distinct window shapes. group, when given, holds q constant
    inside each group of hours, which is how a grid coarser than the windows' own is fitted."""
    n = float(mult.sum())
    w = mult[owner]
    q = np.full(HW, 1.0 / HW) if start is None else np.asarray(start, float) / float(np.sum(start))
    for _ in range(iters):
        num = q[flat]
        den = np.bincount(owner, weights=num, minlength=len(hrs))
        nxt = np.bincount(flat, weights=w * num / den[owner], minlength=HW) / n
        if group is not None:
            tot = np.bincount(group, weights=nxt, minlength=int(group.max()) + 1)
            size = np.bincount(group, minlength=int(group.max()) + 1)
            nxt = (tot / size)[group]
            nxt = nxt / nxt.sum()
        if np.max(np.abs(nxt - q)) < tol:
            return nxt
        q = nxt
    return q


def ml_weights(rows, tol=1e-13, iters=8000):
    """The golden construction: the hour-of-week placement the record itself settles.

    An offence's record says the occurrence lies in its window and says nothing else about where, so the
    record's likelihood as a function of the quarter's hour-of-week shares q is the product over offences of
    the share of q inside that offence's own window. That is concave in q, so it has one maximiser, and the
    self-consistent iteration below reaches it from any interior start. The windows' ends sit on the hour, so
    the hour is the finest grid the record separates; every four-hour slot edge of the week is the end of
    some keeper's watch, so no cell the record separates straddles a slot edge and all 42 slot figures are
    settled rather than only their sums.

    Returns the expected number of offences in each slot, over the rows given.
    """
    hrs, flat, owner, mult = _coverage(rows)
    return as_slots(_em(hrs, flat, owner, mult, tol=tol, iters=iters) * mult.sum())


def ml_loglik(rows, q_hour):
    """The record's log likelihood under a stated hour-of-week placement, for the refutations in checks.py."""
    hrs, flat, owner, mult = _coverage(rows)
    q = np.maximum(np.asarray(q_hour, float), 0.0)
    q = q / q.sum()
    den = np.bincount(owner, weights=np.maximum(q, 1e-300)[flat], minlength=len(hrs))
    return float(np.sum(mult * np.log(np.maximum(den, 1e-300))))


def ml_hour_shares(rows, start=None, tol=1e-13, iters=8000, group=None):
    """The maximum-likelihood hour-of-week shares, optionally from a stated start or on a coarser grid."""
    hrs, flat, owner, mult = _coverage(rows)
    return _em(hrs, flat, owner, mult, start=start, tol=tol, iters=iters, group=group)


def ml_on_grid(rows, width, tol=1e-12, iters=8000):
    """The placement a competent analyst gets by fitting a grid of `width` hours instead of the hour the
    record's own window edges give. Returned as slot figures, for the licensed-variant spread."""
    hrs, flat, owner, mult = _coverage(rows)
    group = (np.arange(HW) // width).astype(np.int64)
    return as_slots(_em(hrs, flat, owner, mult, tol=tol, iters=iters, group=group) * mult.sum())


def ml_separable(rows, tol=1e-12, iters=8000):
    """The separable day-of-week times hour-of-day placement, the other model a competent analyst fits."""
    return as_slots(separable_hour_shares(rows, tol=tol, iters=iters) * _coverage(rows)[3].sum())


def separable_hour_shares(rows, tol=1e-12, iters=8000):
    """Its hour-of-week shares, so the record can be asked what it thinks of the model."""
    hrs, flat, owner, mult = _coverage(rows)
    w = mult[owner]
    d_of = np.arange(HW) // 24
    h_of = np.arange(HW) % 24
    q = np.full(HW, 1.0 / HW)
    for _ in range(iters):
        num = q[flat]
        den = np.bincount(owner, weights=num, minlength=len(hrs))
        cnt = np.bincount(flat, weights=w * num / den[owner], minlength=HW)
        a = np.bincount(d_of, weights=cnt, minlength=7)
        b = np.bincount(h_of, weights=cnt, minlength=24)
        nxt = (a[d_of] / a.sum()) * (b[h_of] / b.sum())
        nxt = nxt / nxt.sum()
        if np.max(np.abs(nxt - q)) < tol:
            return nxt
        q = nxt
    return q


def window_edges(rows):
    """The hours of the week at which some offence's window begins or ends, as the shipped record shows.

    The record separates exactly the cells these edges cut the week into: nothing finer, because no edge
    falls inside an hour, and nothing coarser, because each edge separates the cells either side of it. The
    42 slot figures are therefore settled rather than only their sums, which is what this returns the
    evidence for.
    """
    e = set()
    for r in rows:
        if r["to"] <= r["from"]:
            continue
        e.add(O.hour_of_week(r["from"]))
        e.add(O.hour_of_week(r["to"]))
    return e


def witnessed_profile(rows):
    """The hour-of-week profile of the classes the contract does not cover, which are reported as they
    happen and carry a time. Clause 4.4 keeps them out of the count: they are other offences."""
    prof = np.zeros(HW)
    for r in rows:
        if r["cls"] not in W.CONTRACTED and r["to"] <= r["from"]:
            prof[O.hour_of_week(r["from"])] += 1.0
    return prof


def flat_weights(rows):
    """Rung 3, the textbook aoristic weight: an offence recorded with a window contributes to every slot the
    window touches, in proportion to the share of the window that falls in it. It is the placement that
    assumes the offence is equally likely in every hour of its own window, which is the placement the
    record refutes."""
    w = {s: 0.0 for s in W.SLOTS}
    for r in rows:
        a, b = r["from"], r["to"]
        if b <= a:
            w[O.slot_of(a)] += 1.0
            continue
        span = (b - a).total_seconds()
        t = a
        while t < b:
            nxt = slot_start(t) + dt.timedelta(hours=W.SLOT_H)
            w[O.slot_of(t)] += (min(b, nxt) - t).total_seconds() / span
            t = min(b, nxt)
    return w


def point_weights(rows, key):
    """Each offence counted once, at one end of its window: `from` is the earliest it can have happened, `to`
    the latest. Rungs 0 and 1."""
    w = {s: 0.0 for s in W.SLOTS}
    for r in rows:
        w[O.slot_of(r[key])] += 1.0
    return w


def midpoint_weights(rows):
    """Each offence counted once, at the middle of its window. Rung 2."""
    w = {s: 0.0 for s in W.SLOTS}
    for r in rows:
        w[O.slot_of(r["from"] + (r["to"] - r["from"]) / 2)] += 1.0
    return w


def sampled_weights(rows, step_min):
    """The flat weight computed by sampling the window instead of integrating it: the same figures, because
    every window is recorded on the hour at both ends."""
    w = {s: 0.0 for s in W.SLOTS}
    for r in rows:
        a, b = r["from"], r["to"]
        if b <= a:
            w[O.slot_of(a)] += 1.0
            continue
        k = int(round((b - a).total_seconds() / (step_min * 60.0)))
        for i in range(k):
            w[O.slot_of(a + dt.timedelta(minutes=step_min * i + step_min / 2.0))] += 1.0 / k
    return w


def seen_profile(rows):
    """The hour-of-week profile of the covered offences the keeper saw, which carry a time instead of a
    window. They are the offences that fell in a watched hour, so the profile is a profile of the watched
    hours and holds nothing about the hours the slate turns on."""
    prof = np.zeros(HW)
    for r in rows:
        if r["to"] <= r["from"]:
            prof[O.hour_of_week(r["from"])] += 1.0
    return prof


def profile_weighted(rows, prof):
    """Each window spread in proportion to a supplied hour-of-week profile. Rung 3b when the profile is the
    covered offences' own seen hours, and the route clause 4.4 keeps out when it is anything else."""
    pr = np.maximum(np.asarray(prof, float), 1e-12)
    w = {s: 0.0 for s in W.SLOTS}
    for r in rows:
        hh = hours_of(r)
        x = pr[hh]
        x = x / x.sum()
        for h, v in zip(hh, x):
            w[(int(h) // 24, (int(h) % 24) // W.SLOT_H * W.SLOT_H)] += float(v)
    return w


def footfall_weighted(rows, counts, sensor_of):
    """Each window spread in proportion to the pedestrian feed's own hour-of-week footfall. Clause 4.4 keeps
    it out of the count; it is built here so checks.py can assert the clause is load bearing."""
    return profile_weighted(rows, footfall_profile(counts, sensor_of, rows))


def footfall_profile(counts, sensor_of, rows):
    """The pedestrian feed's hour-of-week profile at each offence's own location, as an hour-of-week vector
    weighted by where the covered offences sit. The feed is not the force's record of the covered offences,
    so clause 4.4 keeps it out of the count; it is built here so checks.py can assert the clause is load
    bearing."""
    tot = np.zeros(HW)
    for sid, stamp, n in counts:
        local = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=1)
        tot[O.hour_of_week(local)] += n
    return tot


def true_time_weights(rows):
    """The slate the offences' unobserved true times give. The generator holds them; the pack never ships
    them."""
    w = {s: 0.0 for s in W.SLOTS}
    for r in rows:
        w[O.slot_of(r["true"])] += 1.0
    return w


def per_season(w):
    n = len(W.SEASONS)
    return {s: v / n for s, v in w.items()}


def slate(w, cap=W.CAP):
    """The cap's worth of heaviest slots, heaviest first."""
    return [s for s, _ in sorted(w.items(), key=lambda kv: (-kv[1], kv[0]))[:cap]]


def covered(w, slots):
    return sum(w[s] for s in slots)


def ladder(rows):
    """Every rung's slate and what it files, plus what its eight slots actually meet on the golden's basis."""
    gold = per_season(ml_weights(rows))
    g_slate = slate(gold)
    out = {"golden": {"weights": gold, "slate": g_slate, "files": covered(gold, g_slate),
                      "meets": covered(gold, g_slate)}}
    rungs = {
        "rung0_window_start": per_season(point_weights(rows, "from")),
        "rung1_window_end": per_season(point_weights(rows, "to")),
        "rung2_midpoint": per_season(midpoint_weights(rows)),
        "rung3_flat_aoristic": per_season(flat_weights(rows)),
        "rung3b_seen_profile": per_season(profile_weighted(rows, seen_profile(rows) + 1e-9)),
    }
    for name, w in rungs.items():
        sl = slate(w)
        out[name] = {"weights": w, "slate": sl, "files": covered(w, sl), "meets": covered(gold, sl)}
    return out
