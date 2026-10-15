"""The slot weights and the slate: the five constructions a tasking analyst can put on an occurrence window, and the
figures the paper and the workbook carry. Nothing here ships; the pack carries records, the goldens carry answers."""
import datetime as dt

import offences as O
import world as W


def slot_start(ts):
    """Midnight-anchored start of the four-hour slot ts falls in."""
    return ts.replace(minute=0, second=0, microsecond=0, hour=(ts.hour // W.SLOT_H) * W.SLOT_H)


def overlap_weights(rows):
    """The golden construction. An offence recorded with an occurrence window contributes to every slot the window
    touches, in proportion to the share of the window that falls in it; an offence recorded at a time contributes
    one to the slot that holds it. Windows are recorded on the hour, so every slot's share is exact."""
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
    """Each offence counted once, at one end of its window: `from` is the earliest it can have happened, `to` the
    latest. Rungs 0 and 1."""
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
    """The golden quantity computed by sampling the window instead of integrating it: the same figure, because every
    window is recorded on the hour at both ends."""
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


def profile_weighted(rows, allrows, step_min=15):
    """The refinement in the literature: spread each window in proportion to the quarter's own hourly profile of
    precisely timed offences rather than evenly. The same eight slots, because the quarter trades through the early
    morning."""
    prof = [0.0] * 24
    for r in allrows:
        if r["to"] <= r["from"]:
            prof[r["from"].hour] += 1.0
    tot = sum(prof)
    prof = [max(p / tot, 1e-6) for p in prof]
    w = {s: 0.0 for s in W.SLOTS}
    for r in rows:
        a, b = r["from"], r["to"]
        if b <= a:
            w[O.slot_of(a)] += 1.0
            continue
        k = int(round((b - a).total_seconds() / (step_min * 60.0)))
        pts = [a + dt.timedelta(minutes=step_min * i + step_min / 2.0) for i in range(k)]
        ws = [prof[p.hour] for p in pts]
        tw = sum(ws)
        for p, x in zip(pts, ws):
            w[O.slot_of(p)] += x / tw
    return w


def footfall_weighted(rows, counts, sensor_of):
    """The weighting the agreement's clause 4.4 rules out: each window spread in proportion to the pedestrian
    footfall at the offence's own location, hour of the week by hour of the week. It is here so the generator can
    assert that the clause is load bearing, that is, that this route files a different slate."""
    import datetime as dt
    prof = {}
    for sid, stamp, n in counts:
        local = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=1)
        key = (sid, local.weekday(), local.hour)
        prof[key] = prof.get(key, 0.0) + n
    w = {s: 0.0 for s in W.SLOTS}
    for r in rows:
        a, b = r["from"], r["to"]
        if b <= a:
            w[O.slot_of(a)] += 1.0
            continue
        sid = sensor_of.get(r["loc"])
        hours, weights = [], []
        t = a
        while t < b:
            nxt = t.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1)
            seg = (min(b, nxt) - t).total_seconds() / 3600.0
            p = prof.get((sid, t.weekday(), t.hour), 1.0) if sid else 1.0
            hours.append(t)
            weights.append(max(p, 1.0) * seg)
            t = min(b, nxt)
        tot = sum(weights)
        for t, x in zip(hours, weights):
            w[O.slot_of(t)] += x / tot
    return w


def true_time_weights(rows):
    """The slate the offences' unobserved true times give. The generator holds them; the pack never ships them."""
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
    gold = per_season(overlap_weights(rows))
    g_slate = slate(gold)
    out = {"golden": {"weights": gold, "slate": g_slate, "files": covered(gold, g_slate),
                      "meets": covered(gold, g_slate)}}
    rungs = {
        "rung0_window_start": per_season(point_weights(rows, "from")),
        "rung1_window_end": per_season(point_weights(rows, "to")),
        "rung2_midpoint": per_season(midpoint_weights(rows)),
    }
    for name, w in rungs.items():
        sl = slate(w)
        out[name] = {"weights": w, "slate": sl, "files": covered(w, sl), "meets": covered(gold, sl)}
    return out
