#!/usr/bin/env python3
"""task464: the four-year timed treatment record, built from the clean truth.

Each site runs its deliverable positions as continuous chains: a position takes a treatment, holds it for
the prescription's own length, turns over, and takes the next. Nothing in the record says how many
positions a site has; the count is recoverable only from the overlaps.

Three properties are built rather than hoped for, and `checks.py` asserts each:
  * the greatest number of a site's treatments running at one time equals its deliverable positions, in
    every one of the 48 months, and one more than that never runs;
  * no two of a site's treatments share an endpoint, and every position turns over strictly positively;
  * the round that saturates moves around the day, so the plateau is in the month without being the day's
    signature, and no count of treatments starting inside a fixed clock window returns the position count.
"""
import bisect
import collections
import datetime as dt
import random

import world

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# modality -> (durations in minutes with weights, turnover range, open-time range, ramp step range)
MIX = {
    # prescription lengths with weights, turnover range, opening-minute range, ramp step range.
    # The ramp is wide on purpose: the positions that run together start up to three hours apart, so no
    # count of treatments starting inside a clock window returns the position count.
    "dialysis": ([(210, 3), (225, 5), (240, 8), (255, 3), (270, 2)], (22, 34), (330, 420), (72, 190)),
    "infusion": ([(105, 3), (120, 6), (135, 4), (150, 3), (180, 2)], (16, 26), (465, 530), (66, 85)),
}
STATUS_COMPLETED = "completed"
CANCEL_WORDS = ["cancelled", "no show"]


def _pick(rnd, weighted):
    tot = sum(w for _, w in weighted)
    x = rnd.random() * tot
    for v, w in weighted:
        x -= w
        if x <= 0:
            return v
    return weighted[-1][0]


def weekly_targets(site, rnd):
    """Treatments a week over the 208 full weeks, hitting the 2026 target and the designed busiest week."""
    K = site["ceiling"]
    change = world.ROSTER_CHANGE_WEEK if site["closed_shift"] else 0
    rounds = [site["rounds_hist"] if w < change else site["rounds"] for w in range(world.REC_WEEKS)]
    cap = [K * r for r in rounds]
    amp = 0.17 if site["peak_fill"] == world.SEASONAL_FILL else 0.045
    ceil_fill = site["peak_fill"] - 0.014
    f = []
    for w in range(world.REC_WEEKS):
        iso = (world.REC_START + dt.timedelta(weeks=w)).timetuple().tm_yday
        seas = 1.0 + amp * (0.62 * _cos(iso / 365.0) + 0.38 * _cos(2 * iso / 365.0))
        f.append(min(ceil_fill, site["u"] * seas * (1.0 + rnd.uniform(-0.028, 0.028))))
    # the designed busiest week: pre-change where a shift has since closed, in season where seasonal
    if site["closed_shift"]:
        peak_w = 24 + (site["seq"] * 13) % 80
    elif site["peak_fill"] == world.SEASONAL_FILL:
        peak_w = [5, 57, 109, 161][site["seq"] % 4] + (site["seq"] % 3)
    else:
        peak_w = 17 + (site["seq"] * 29) % 180
    T = [max(1, min(cap[w], int(round(f[w] * cap[w])))) for w in range(world.REC_WEEKS)]
    T[peak_w] = site["R2"]
    hi = site["R2"] - 1
    for w in range(world.REC_WEEKS):
        if w != peak_w:
            T[w] = min(T[w], hi, cap[w])
    return T, rounds, peak_w


def _cos(x):
    import math
    return math.cos(2 * math.pi * x)


def _week_of(d):
    return (d - world.REC_START).days // 7


def open_days(site):
    """The weekdays the site treats on: six days means Monday to Saturday, five means Monday to Friday."""
    return list(range(site["days"]))


def build(sites, seed=world.SEED + 7):
    """Returns (encounters, panels). Position and round index are generator state and are never shipped.

    Two phases, so the 2026 contract year's treatment count lands exactly on the clean truth's figure:
    the weekly shape and the designed busiest week first, then the 2026 days adjusted to the target, then
    the chains.
    """
    out, panels = [], {}
    for site in sites:
        srnd = random.Random(seed * 131 + site["seq"])
        T, rounds_by_week, peak_w = weekly_targets(site, srnd)
        K = site["ceiling"]
        durs, turn, openrange, steprange = MIX[site["modality"]]
        site["ramp_span"] = srnd.randint(*steprange)
        panel_n = max(12, int(round(site["R3"] * site["u"] / (3.0 if site["modality"] == "dialysis" else 1.6))))
        panel = ["M%09d" % (400000000 + site["seq"] * 7919 + i * 13) for i in range(panel_n)]
        panels[site["site"]] = panel
        days_open = open_days(site)

        # phase one: a treatment count for every open day
        dayt, daycap = {}, {}
        for w in range(world.REC_WEEKS):
            rpd = rounds_by_week[w] // site["days"]
            cap = K * rpd
            base, rem = T[w] // len(days_open), T[w] - (T[w] // len(days_open)) * len(days_open)
            order = days_open[:]
            srnd.shuffle(order)
            got = {}
            for i, d in enumerate(order):
                got[d] = min(cap, base + (1 if i < rem else 0))
            left = T[w] - sum(got.values())
            for d in order:
                while left > 0 and got[d] < cap:
                    got[d] += 1
                    left -= 1
            for d in days_open:
                date = world.REC_START + dt.timedelta(weeks=w, days=d)
                if date.year > 2026:
                    continue
                dayt[date] = got[d]
                daycap[date] = cap

        # every month carries at least one day the site can fill every position on
        bymonth = collections.defaultdict(list)
        for d in dayt:
            bymonth[(d.year, d.month)].append(d)
        for mon, days in bymonth.items():
            if not any(dayt[d] >= K for d in days):
                d = max(days, key=lambda x: dayt[x])
                dayt[d] = min(daycap[d], K)

        # phase two: the 2026 contract year hits the clean truth exactly, the busiest week untouched,
        # and no other week is allowed to reach the busiest week's count
        peak_days = {world.REC_START + dt.timedelta(weeks=peak_w, days=d) for d in range(7)}
        wk = collections.Counter()
        for d, v in dayt.items():
            wk[(d - world.REC_START).days // 7] += v
        y26 = sorted(d for d in dayt if d.year == 2026 and d not in peak_days)
        diff = site["vol_2026"] - sum(v for d, v in dayt.items() if d.year == 2026)
        i, guard = 0, 0
        while diff != 0 and guard < 400000:
            d = y26[i % len(y26)]
            w = (d - world.REC_START).days // 7
            i += 1
            guard += 1
            if diff > 0 and dayt[d] < daycap[d] and wk[w] < site["R2"] - 1:
                dayt[d] += 1
                wk[w] += 1
                diff -= 1
            elif diff < 0 and dayt[d] > K:
                dayt[d] -= 1
                wk[w] -= 1
                diff += 1
        assert diff == 0, "%s could not reach its 2026 target, %d left" % (site["site"], diff)

        rows = []
        for date in sorted(dayt):
            n = dayt[date]
            if n <= 0:
                continue
            w = (date - world.REC_START).days // 7
            rpd = rounds_by_week[min(w, world.REC_WEEKS - 1)] // site["days"]
            rows += _day(site, date, n, K, rpd, durs, turn, openrange,
                         (site["ramp_span"], site["ramp_span"] + 28), srnd, panel, w, date.weekday())
        _separate_endpoints(rows)
        out += rows
    return out, panels


def _separate_endpoints(rows):
    """No treatment at a site starts on the minute another stops, so the endpoint convention cannot move
    the overlap count. A start that lands on a stop is pushed one minute later, which every turnover
    absorbs."""
    abs_min = {}
    for i, r in enumerate(rows):
        abs_min[i] = (r["date"] - world.REC_START).days * 1440
    for _ in range(6):
        stops = set(abs_min[i] + r["start"] + r["dur"] for i, r in enumerate(rows))
        clash = [i for i, r in enumerate(rows) if abs_min[i] + r["start"] in stops]
        if not clash:
            return
        for i in clash:
            rows[i]["start"] += 1
    stops = set(abs_min[i] + r["start"] + r["dur"] for i, r in enumerate(rows))
    assert not [i for i, r in enumerate(rows) if abs_min[i] + r["start"] in stops], \
        "endpoints could not be separated"


def _day(site, date, n, K, rpd, durs, turn, openrange, steprange, rnd, panel, w, d):
    """One day's chains. The saturating round moves around the day; positions idle in a varying subset."""
    quota = [0] * K
    left = n
    pos_order = list(range(K))
    rnd.shuffle(pos_order)
    sat = None
    if n >= K:
        sat = rnd.randrange(rpd) if (rpd > 1 and n >= K + max(1, (rpd - 1))) else 0
        for j in range(K):
            quota[j] = 1
        left = n - K
    for j in pos_order:
        while left > 0 and quota[j] < rpd:
            quota[j] += 1
            left -= 1
    span = rnd.randint(*steprange)
    step = span / float(max(1, K - 1))
    open_min = rnd.randint(*openrange)
    offs = [int(round(i * step)) for i in range(K)]
    rnd.shuffle(offs)
    block = (sum(v * wt for v, wt in durs) / sum(wt for _, wt in durs)) + (turn[0] + turn[1]) / 2.0
    rows = []
    for j in range(K):
        q = quota[j]
        if q <= 0:
            continue
        first = sat if sat is not None else 0
        a = first if q == 1 else max(0, min(rpd - q, first - rnd.randrange(q)))
        if sat is not None and not (a <= sat < a + q):
            a = max(0, min(rpd - q, sat))
        t = open_min + offs[j] + a * block
        prev_end = None
        for r in range(q):
            dur = _pick(rnd, durs)
            start = t if prev_end is None else max(t, prev_end + rnd.randint(*turn))
            start = int(round(start)) + (j % 3)            # no two positions share a minute
            end = start + dur
            mem = panel[(site["seq"] * 17 + j * 29 + (a + r) * 7 + d * 11) % len(panel)]
            rows.append(dict(site=site["site"], member=mem, date=date, start=start, dur=dur,
                             pos=j, rnd_ix=a + r, week=w))
            prev_end = end
            t = start + dur + rnd.randint(*turn)
    return rows


# ----------------------------------------------------------------------------- the measurements
def concurrency_profile(rows):
    """Per site: the maximum overlap, the monthly and yearly maxima, the time at each level, endpoints."""
    by_site = collections.defaultdict(list)
    for r in rows:
        by_site[r["site"]].append(r)
    out = {}
    for s, rs in by_site.items():
        ev = []
        for r in rs:
            t0 = (r["date"] - world.REC_START).days * 1440 + r["start"]
            ev.append((t0, 1, r))
            ev.append((t0 + r["dur"], -1, r))
        ev.sort(key=lambda e: (e[0], e[1]))
        hist = collections.Counter()
        monthly, yearly = collections.defaultdict(int), collections.defaultdict(int)
        cur, prev, mx = 0, None, 0
        starts, ends = collections.Counter(), collections.Counter()
        argmax_hours = collections.Counter()
        for t, k, r in ev:
            if prev is not None and cur > 0:
                hist[cur] += t - prev
            cur += k
            prev = t
            if k == 1:
                starts[t] += 1
                mon = (r["date"].year, r["date"].month)
                monthly[mon] = max(monthly[mon], cur)
                yearly[r["date"].year] = max(yearly[r["date"].year], cur)
                mx = max(mx, cur)
                if cur == 0:
                    pass
            else:
                ends[t] += 1
        for r in rs:
            t0 = (r["date"] - world.REC_START).days * 1440 + r["start"]
            pass
        coincident = sum(1 for t in starts if t in ends)
        tot = sum(hist.values())
        at = hist.get(mx, 0)
        cum, cross = 0, 1.0
        for lev in sorted(hist):
            if lev < mx:
                cum += hist[lev]
        cross = cum / float(tot) if tot else 1.0
        qs = {}
        for q in (0.75, 0.90, 0.95, 0.99):
            need, run = q * tot, 0
            for lev in sorted(hist):
                run += hist[lev]
                if run >= need:
                    qs[q] = lev
                    break
        out[s] = dict(max=mx, monthly=dict(monthly), yearly=dict(yearly), hist=dict(hist), quantiles=qs,
                      share_at_max=at / float(tot) if tot else 0.0, crossover=cross,
                      above=sum(v for k, v in hist.items() if k > mx), coincident=coincident,
                      treating_minutes=tot)
    return out


def argmax_hour_spread(rows):
    """For each site-day, the clock hour at which concurrency is highest: how concentrated is it."""
    by = collections.defaultdict(list)
    for r in rows:
        by[(r["site"], r["date"])].append(r)
    per_site = collections.defaultdict(collections.Counter)
    for (s, d), rs in by.items():
        ev = []
        for r in rs:
            ev.append((r["start"], 1))
            ev.append((r["start"] + r["dur"], -1))
        ev.sort()
        cur, best, bt = 0, 0, 0
        for t, k in ev:
            cur += k
            if cur > best:
                best, bt = cur, t
        per_site[s][int(bt // 60) % 24] += 1
    return {s: (max(c.values()) / float(sum(c.values())), len(c)) for s, c in per_site.items()}


def clock_window_counts(rows, widths=(60, 120, 180, 240)):
    """The most treatments starting inside any fixed clock block of each width, per site."""
    by = collections.defaultdict(collections.Counter)
    for r in rows:
        t = (r["date"] - world.REC_START).days * 1440 + r["start"]
        for w in widths:
            by[(r["site"], w)][t // w] += 1
    out = collections.defaultdict(dict)
    for (s, w), c in by.items():
        out[s][w] = max(c.values())
    return dict(out)


def start_window_counts(rows, widths=(60, 120, 180, 240, 300, 360, 480, 720)):
    """The most treatments starting inside any window of each width, per site."""
    by_site = collections.defaultdict(list)
    for r in rows:
        by_site[r["site"]].append((r["date"] - world.REC_START).days * 1440 + r["start"])
    out = {}
    for s, ts in by_site.items():
        ts.sort()
        res = {}
        for w in widths:
            best, j = 0, 0
            for i in range(len(ts)):
                j = bisect.bisect_right(ts, ts[i] + w - 1)
                best = max(best, j - i)
            res[w] = best
        out[s] = res
    return out


if __name__ == "__main__":
    sites, by_area = world.build()
    rows, panels = build(sites)
    print("encounters %d | members %d" % (len(rows), sum(len(p) for p in panels.values())))
    prof = concurrency_profile(rows)
    ok = agree = 0
    for s in sites:
        p = prof[s["site"]]
        if p["max"] == s["ceiling"] and p["above"] == 0:
            ok += 1
        if (set(p["monthly"].values()) == {s["ceiling"]} and set(p["yearly"].values()) == {s["ceiling"]}):
            agree += 1
    print("record maximum equals positions and never exceeds: %d of %d" % (ok, len(sites)))
    print("every month and every year maximum equals positions: %d of %d" % (agree, len(sites)))
    sh = sorted(prof[s["site"]]["share_at_max"] for s in sites)
    cr = sorted(prof[s["site"]]["crossover"] for s in sites)
    print("share of treating minutes at the ceiling: min %.3f median %.3f max %.3f" % (sh[0], sh[20], sh[-1]))
    print("smallest quantile returning the ceiling: worst %.3f median %.3f" % (cr[-1], cr[20]))
    print("coincident endpoints: %d" % sum(prof[s["site"]]["coincident"] for s in sites))
    am = argmax_hour_spread(rows)
    conc = sorted(v[0] for v in am.values())
    print("busiest hour of the day, share of site-days at the site's modal hour: median %.2f worst %.2f;"
          " distinct hours per site median %d" % (conc[20], conc[-1],
                                                 sorted(v[1] for v in am.values())[20]))
    for q in (0.75, 0.90, 0.95, 0.99):
        hit = sum(1 for s in sites if prof[s["site"]]["quantiles"].get(q) == s["ceiling"])
        print("  the %.2f quantile of concurrency returns the position count at %d of 40 sites" % (q, hit))
    sw = start_window_counts(rows)
    cw = clock_window_counts(rows)
    for w in (60, 120, 180, 240, 300, 360, 480, 720):
        eq = sum(1 for s in sites if sw[s["site"]][w] == s["ceiling"])
        print("  sliding %4d-minute window: the most starts equals the position count at %2d of 40 sites" % (w, eq))
    for w in (60, 120, 180, 240):
        eq = sum(1 for s in sites if cw[s["site"]][w] == s["ceiling"])
        print("  clock-aligned %3d-minute block: equals the position count at %2d of 40 sites" % (w, eq))
    perday = collections.Counter()
    for r in rows:
        perday[(r["site"], r["date"])] += 1
    worst = min((max(v for (s2, d), v in perday.items() if s2 == s["site"]) / float(s["ceiling"]), s["site"])
                for s in sites)
    print("  the most treatments a site takes in one day, over its position count: smallest ratio %.2f (%s)"
          % worst)
