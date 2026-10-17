"""How the record comes to exist: nine operations, each on its own calendar, sharing a stage.

Every action is real. Nothing is planted. What makes the count hard is that the operations share
locations, so a run of flagged location-days merges two of them wherever they coincide and splits one
wherever its own interval skips a beat.
"""
import datetime as dt
import hashlib
import random

import world as W


def days(lo, hi):
    d = lo
    while d <= hi:
        yield d
        d += dt.timedelta(days=1)


def assign_places():
    """which settlements each operation touches, and which it alone touches"""
    rng = random.Random(W.SEED * 7 + 11)
    codes = [p[0] for p in W.PLACES]
    sole, shared = {}, {}
    pool = list(codes)
    rng.shuffle(pool)
    i = 0
    for name, interval, start, n, k in W.OPERATIONS:
        sole[name] = pool[i:i + k]            # nobody else acts here, so the tempo reads unmixed
        i += k
    rest = pool[i:]
    for name, interval, start, n, k in W.OPERATIONS:
        extra = n - k
        picked = []
        for j in range(extra):
            h = int.from_bytes(hashlib.blake2b((name + str(j)).encode(), digest_size=8).digest(), "big")
            cand = rest[(h + j * 7) % len(rest)]
            if cand not in picked:
                picked.append(cand)
        while len(picked) < extra:
            cand = rest[rng.randrange(0, len(rest))]
            if cand not in picked:
                picked.append(cand)
        shared[name] = sorted(picked)
    return {n: sorted(set(sole[n] + shared[n])) for n, _, _, _, _ in W.OPERATIONS}, sole


def actions():
    """every action every operation carried out inside the reporting period"""
    places, sole = assign_places()
    rng = random.Random(W.SEED * 13 + 3)
    out = []
    for name, interval, start, n, k in W.OPERATIONS:
        d = start
        while d <= W.P_TO:
            if d >= W.P_FROM:
                # an operation does not always reach every location it touches on a given day
                hit = [p for p in places[name] if rng.random() < 0.82]
                for p in sole[name]:
                    if p not in hit:
                        hit.append(p)         # it always reaches the ones only it works
                for p in sorted(hit):
                    out.append({"operation": name, "day": d, "place": p, "interval": interval})
            d += dt.timedelta(days=interval)
    return out, places, sole


def location_days(acts):
    """the location-days the record holds, which is what the institute flags"""
    s = set()
    for a in acts:
        s.add((a["place"], a["day"]))
    return sorted(s)


def runs(flagged, places_of=None):
    """contiguous runs of flagged location-days, joined where they touch in time and place"""
    by_place = {}
    for p, d in flagged:
        by_place.setdefault(p, []).append(d)
    groups = []
    for p in sorted(by_place):
        ds = sorted(by_place[p])
        cur = [ds[0]]
        for d in ds[1:]:
            if (d - cur[-1]).days <= 1:
                cur.append(d)
            else:
                groups.append((p, cur))
                cur = [d]
        groups.append((p, cur))
    # join groups that overlap in time across places, which is what "touch in time and place" means
    merged = []
    used = [False] * len(groups)
    for i, (p, ds) in enumerate(groups):
        if used[i]:
            continue
        lo, hi = min(ds), max(ds)
        members = [i]
        used[i] = True
        changed = True
        while changed:
            changed = False
            for j, (q, es) in enumerate(groups):
                if used[j]:
                    continue
                if min(es) <= hi + dt.timedelta(days=1) and max(es) >= lo - dt.timedelta(days=1):
                    used[j] = True
                    members.append(j)
                    lo, hi = min(lo, min(es)), max(hi, max(es))
                    changed = True
        merged.append((lo, hi, members))
    return groups, merged
