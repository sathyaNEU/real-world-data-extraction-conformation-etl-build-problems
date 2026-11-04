"""Keep every graded hours figure a minute clear of its rounding line.

The return states each overflow's hours of discharge to one decimal and the chart each month's. A monitor's records
are exact to the second, so a figure can fall seconds from a rounding line, where a reader working to the minute
would round it the other way. Before the platform's log is written, each overflow's records are settled: where a
month's hours, or the year's, sit less than a minute from a line, the end of one discharge in that month (or, where
another unit's record of the same discharge holds the end, its start) is moved by the seconds that put the figure a
minute clear on the side it already rounds to.
No spill count, no rounded figure and no other month moves, and every shift is inside the monitors' own hold-off
spread (a few seconds to two minutes)."""
import math

import golden as G

CLEAR = 66.0          # seconds: the assertion is a minute, with six seconds to spare


def margin(h):
    """Seconds from the nearest one-decimal rounding line, and the side to move away from it (-1 down, +1 up)."""
    f = (h * 10) % 1
    return abs(f - 0.5) * 360.0, (-1 if f < 0.5 else 1)


def _lines(code, mons):
    log = {m["serial"]: [(float(a), float(b)) for a, b in m["events"]] for m in mons}
    site = {m["serial"]: code for m in mons}
    return G.returns({code: {}}, log, {}, site)[code]


def _month_of(a):
    return G.utc_to_local(a).month


def _try(code, mons, month, delta, base):
    """Change one stretch of discharge in `month` by `delta` seconds, at its end or failing that at its start. Where
    two units recorded the same discharge, every record whose end (or start) lies within the moved window moves
    with it, so the stretch changes by exactly `delta`; a move is kept only if the count and every other month
    hold."""
    recs = [(i, j, a, b) for i, m in enumerate(mons) for j, (a, b) in enumerate(m["events"])]
    spans = G.union([(a, b) for i, j, a, b in recs])
    cands = []
    for n, (ua, ub) in enumerate(spans):
        if _month_of(ua) != month or _month_of(ub) != month:
            continue
        inside = [(i, j, a, b) for i, j, a, b in recs if a < ub and b > ua]
        nxt = spans[n + 1][0] if n + 1 < len(spans) else float("inf")
        prv = spans[n - 1][1] if n > 0 else -float("inf")
        # the end
        if delta < 0:
            moves = [(i, j, a, b, a, b + delta) for i, j, a, b in inside if b > ub + delta - 5]
            ok = all(nb - na >= 300 for i, j, a, b, na, nb in moves)
        else:
            i, j, a, b = max(inside, key=lambda x: x[3])
            moves = [(i, j, a, b, a, b + delta)]
            ok = nxt - (b + delta) >= 900 and _month_of(b + delta) == month
        if ok:
            cands.append((0, -(ub - ua), moves))
        # the start
        if delta < 0:
            moves = [(i, j, a, b, a - delta, b) for i, j, a, b in inside if a < ua - delta + 5]
            ok = all(nb - na >= 300 for i, j, a, b, na, nb in moves)
        else:
            i, j, a, b = min(inside, key=lambda x: x[2])
            moves = [(i, j, a, b, a - delta, b)]
            ok = (a - delta) - prv >= 900 and _month_of(a - delta) == month
        if ok:
            cands.append((1, -(ub - ua), moves))
    for _, _, moves in sorted(cands, key=lambda x: (x[0], x[1])):
        for i, j, a, b, na, nb in moves:
            mons[i]["events"][j] = (na, nb)
        new = _lines(code, mons)
        if new["spills"] == base["spills"] and all(abs(new["months"][k] - base["months"][k]) < 1e-9
                                                   for k in range(12) if k != month - 1) \
                and abs(new["months"][month - 1] - base["months"][month - 1] - delta / 3600.0) < 1e-9:
            return new
        for i, j, a, b, na, nb in moves:
            mons[i]["events"][j] = (a, b)
    return None


def _bin(h):
    """The one-decimal figure h rounds to, as an integer number of tenths (the line sits half a tenth either side)."""
    return int(math.floor(h * 10 + 0.5))


def _safe(h, tenth, spare=0.0):
    """Seconds h must move to sit CLEAR (plus `spare`) inside the bin of `tenth` (0 when it already does)."""
    lo = (tenth - 0.5) / 10 + (CLEAR + spare) / 3600.0
    hi = (tenth + 0.5) / 10 - (CLEAR + spare) / 3600.0
    if h < lo - 1e-9:
        return math.ceil((lo - h) * 3600.0 - 1e-6)
    if h > hi + 1e-9:
        return -math.ceil((h - hi) * 3600.0 - 1e-6)
    return 0


def station(code, mons):
    """Settle one overflow's records in place; returns the number of stretches moved. Every month and the year keep
    the figure they rounded to before settling."""
    for m in mons:
        m["events"] = [(float(round(a)), float(round(b))) for a, b in m["events"]]
    base = _lines(code, mons)
    keep_months = [_bin(h) for h in base["months"]]
    keep_year = _bin(base["hours"])
    moved = 0
    for k in range(12):
        h = base["months"][k]
        if h <= 0:
            continue
        if not _safe(h, keep_months[k]):
            continue
        need = _safe(h, keep_months[k], spare=2.0)
        new = _try(code, mons, k + 1, need, base)
        if new is None:
            raise RuntimeError("cannot settle %s month %d" % (code, k + 1))
        base = new
        moved += 1
    if _safe(base["hours"], keep_year):
        need = _safe(base["hours"], keep_year, spare=2.0)
        for k in sorted(range(12), key=lambda k: -base["months"][k]):
            h = base["months"][k]
            if h <= 0 or _safe(h + need / 3600.0, keep_months[k]) or _bin(h + need / 3600.0) != keep_months[k]:
                continue
            new = _try(code, mons, k + 1, need, base)
            if new is not None:
                base = new
                moved += 1
                break
        else:
            raise RuntimeError("cannot settle the year's hours at %s" % code)
    assert _bin(base["hours"]) == keep_year and not _safe(base["hours"], keep_year)
    assert all(_bin(h) == keep_months[k] and not _safe(h, keep_months[k]) for k, h in enumerate(base["months"]) if h > 0)
    return moved
