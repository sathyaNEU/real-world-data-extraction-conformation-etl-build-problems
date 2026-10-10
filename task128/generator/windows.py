"""Maintenance windows, the hourly transaction forecast, the per-window concurrent-drain capacity,
and the May-to-October change-request corpus with the provider's recorded outcomes.

The true rule: within a window, requests are taken in submission order and accepted up to the
window's concurrent drains times its cycles, less drains already accepted in that window, counting
every requested host separately. Concurrent drains are the whole hosts of headroom above the
forecast peak taken over the window's own hours, less one rack.

Rivals the back-test must refuse: the day's peak, the window average, a fixed tool parallelism, a
flat tenth of the estate, distinct hosts per window (sharing), no rack reserve, two racks reserved.
"""
import datetime as dt

from params import RACK, TPS, WINDOWS, N_BY_MONTH, COLO

D = dt.date
T = dt.timedelta
CYCLES = 8          # a 4-hour window, one drain cycle every 30 minutes
PARALLELISM = 7     # the drain tool's configured concurrency (a declared distractor rival)


def past_windows(estate):
    """All windows of the estate from 1 May to 22 October 2026, each (date, weekday)."""
    (wd_a, wd_b), _, _ = WINDOWS[estate]
    out = []
    d = D(2026, 5, 1)
    while d <= D(2026, 10, 22):
        if d.weekday() in (wd_a, wd_b):
            out.append(d)
        d += T(days=1)
    return out


def _needed(peak_tps, per_host):
    import math
    return math.ceil(peak_tps / per_host)


def forecast_peaks(rng):
    """Per-estate, per-date (window-hours peak tps, whole-day peak tps). The day peak is at least
    the window peak; on separator windows it is strictly higher so the day's-peak rule under-counts.
    """
    peaks = {}
    for estate in COLO:
        per = TPS[estate]
        base_n = N_BY_MONTH[estate]
        peaks[estate] = {}
        for i, d in enumerate(past_windows(estate)):
            n = base_n[d.month]
            # seasonal rise May->Oct; headroom (concurrent) falls from ~9 to ~4
            frac = 0.80 + 0.11 * ((d.month - 5) / 5.0) + rng.uniform(-0.01, 0.01)
            needed = int(round(frac * n))
            concurrent = n - needed - RACK
            concurrent = max(3, min(11, concurrent))
            needed = n - RACK - concurrent
            wpeak = needed * per
            # on ~ every third window the daytime peak is higher, so the day's-peak rule differs
            if i % 3 == 0:
                day_needed = needed + rng.randint(1, 3)
            else:
                day_needed = needed
            peaks[estate][d] = (wpeak, day_needed * per, concurrent, needed, n)
    return peaks


def nov_drains():
    """November drains per colocated estate under the two headroom readings.

    Window-hours (the true rule) gives payments 96, checkout 120; the day's-peak reading gives
    payments 88, checkout 48. Both are concurrent drains per window times eight 30-minute cycles.
    """
    from params import NOV_C, NOV_C_DAY
    wh = {e: sum(NOV_C[e]) * CYCLES for e in COLO}
    day = {e: sum(NOV_C_DAY[e]) * CYCLES for e in COLO}
    return wh, day


def _caps(concurrent, concurrent_day, n):
    """Capacity (host-drains) for the window under every headroom rule."""
    return {
        "truth": concurrent * CYCLES,
        "day_peak": max(0, concurrent_day) * CYCLES,
        "window_avg": (concurrent + 2) * CYCLES,
        "parallelism": PARALLELISM * CYCLES,
        "flat_tenth": int(0.10 * n) * CYCLES,
        "no_rack": (concurrent + RACK) * CYCLES,
        "two_rack": max(0, concurrent - RACK) * CYCLES,
    }


def build_requests(rng, hosts):
    """The May-to-October change requests and the provider's recorded outcomes.

    Each request names a team, a submission time and a set of host drains; within a window requests
    are taken in order and accepted up to the window's capacity. Returns (requests, rivals) where
    rivals[name] = number of requests whose accepted count the rule gets wrong (>= 20 each).
    """
    peaks = forecast_peaks(rng)
    requests = []
    # candidate drainable hosts per estate (recent/active pools), for the host identifiers listed
    drain_pool = {e: [h.hid for h in hosts[e] if h.kind in ("dense", "active")] for e in COLO}
    rid = 0
    for est in COLO:
        wd_hours = "20:00-24:00" if est == "payments" else "22:00-02:00"
        for d in past_windows(est):
            wpeak, dpeak, concurrent, needed, n = peaks[est][d]
            import math
            day_needed = math.ceil(dpeak / TPS[est])
            concurrent_day = n - needed_rack(n, day_needed)
            caps = _caps(concurrent, concurrent_day, n)
            cap_true = caps["truth"]
            # 2 to 6 requests; on ~45 per cent of windows the total requested exceeds capacity
            k = rng.randint(3, 7)
            bind = rng.random() < 0.45
            sizes = []
            if bind:
                base = cap_true + rng.randint(2, 14)
                for _ in range(k):
                    sizes.append(max(1, int(base / k) + rng.randint(-2, 3)))
            else:
                room = max(1, cap_true - rng.randint(0, 6))
                for _ in range(k):
                    sizes.append(max(1, rng.randint(1, max(2, room // k))))
            used = 0
            order = sorted(range(k))
            for j in order:
                rid += 1
                req = sizes[j]
                acc = max(0, min(req, cap_true - used))
                used += acc
                team = rng.choice(TEAMS_FOR[est])
                hid_list = rng.sample(drain_pool[est], min(req, len(drain_pool[est])))
                requests.append({"rid": f"CR-{rid:05d}", "estate": est, "date": d, "hours": wd_hours,
                                 "team": team, "order": j + 1, "requested": req, "accepted": acc,
                                 "hosts": hid_list, "n": n, "concurrent": concurrent,
                                 "concurrent_day": concurrent_day})
    requests = requests[:412] if len(requests) >= 412 else requests
    rivals = _sweep(requests)
    return requests, rivals


def needed_rack(n, needed):
    return needed + RACK


TEAMS_FOR = {"payments": ["Payments engineering", "SRE platform"],
             "checkout": ["Checkout engineering", "SRE platform"]}


def _sweep(requests):
    """Recompute accepted under each rival and count requests it gets wrong."""
    from collections import defaultdict
    bywin = defaultdict(list)
    for r in requests:
        bywin[(r["estate"], r["date"])].append(r)
    names = ["day_peak", "window_avg", "parallelism", "flat_tenth", "no_rack", "two_rack", "sharing"]
    miss = {nm: 0 for nm in names}
    for key, reqs in bywin.items():
        reqs = sorted(reqs, key=lambda r: r["order"])
        n = reqs[0]["n"]
        caps = _caps(reqs[0]["concurrent"], reqs[0]["concurrent_day"], n)
        for nm in names:
            if nm == "sharing":
                cap = caps["truth"]
                used, seen = 0, set()
                for r in reqs:
                    add = [h for h in r["hosts"] if h not in seen]
                    acc = max(0, min(len(add), cap - used))
                    used += acc
                    seen.update(r["hosts"][:r["requested"]])
                    if acc != r["accepted"]:
                        miss[nm] += 1
            else:
                cap = caps[nm]
                used = 0
                for r in reqs:
                    acc = max(0, min(r["requested"], cap - used))
                    used += acc
                    if acc != r["accepted"]:
                        miss[nm] += 1
    return miss


def nov_windows():
    """{estate: [(window_date, drains)]} for the November windows booked to the office, in date
    order: concurrent drains under the window-hours headroom times eight cycles."""
    from params import NOV_OFFICE, NOV_C
    return {e: [(d, c * CYCLES) for d, c in zip(NOV_OFFICE[e], NOV_C[e])] for e in COLO}


def mark_office(requests, seed):
    """Relabel some May to October requests as the office's own colocated change tickets: one
    request per ticket, at most one per window, a few of them part-accepted. Team labels do not
    enter the capacity rule, so the back-test is unchanged; a separate generator keeps every other
    draw where it was."""
    import random
    from params import OFFICE_TEAM, OFFICE_N, OFFICE_PART
    rng = random.Random(seed + 60)
    for est in COLO:
        rs = [r for r in requests if r["estate"] == est and r["accepted"] > 0]
        part = [r for r in rs if r["accepted"] < r["requested"]]
        full = [r for r in rs if r["accepted"] == r["requested"] and r["requested"] <= 20]
        chosen, days = [], set()
        for r in rng.sample(part, len(part)):
            if len([c for c in chosen if c["accepted"] < c["requested"]]) >= OFFICE_PART[est]:
                break
            if r["date"] not in days:
                chosen.append(r); days.add(r["date"])
        for r in rng.sample(full, len(full)):
            if len(chosen) >= OFFICE_N[est]:
                break
            if r["date"] not in days:
                chosen.append(r); days.add(r["date"])
        for r in chosen:
            r["team"] = OFFICE_TEAM
            r["office"] = True
    return requests


def nov_office_peaks():
    """Per November office window: (date, window_peak_tps, day_peak_tps). The window-hours peak
    yields the concurrent drains in NOV_C; the day peak yields the lower NOV_C_DAY."""
    from params import NOV_OFFICE, NOV_C, NOV_C_DAY, N_BY_MONTH, RACK, TPS
    out = {}
    for e in COLO:
        n = N_BY_MONTH[e][11]
        per = TPS[e]
        rows = []
        for d, c, cday in zip(NOV_OFFICE[e], NOV_C[e], NOV_C_DAY[e]):
            wpeak = (n - RACK - c) * per
            dpeak = (n - RACK - cday) * per
            rows.append((d, wpeak, dpeak))
        out[e] = rows
    return out
