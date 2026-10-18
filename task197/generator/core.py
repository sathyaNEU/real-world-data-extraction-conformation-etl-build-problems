"""task197: the window's episodes, the per-site ladder figures and the ask quantities.

Every number the pack, the goldens and figures.json carry comes from here.
"""
import sys, os, numpy as np, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim

TOLERANCE_PCT = 90.0          # the performance standard's re-prequalification trigger
EXC_THRESH = 0.075            # |f - 50| at or beyond this triggers an operator deviation extract
EXC_MIN_SECS = 20
EXC_PAD = 15                  # the extract runs from the last second inside the dead band to the
                              # first second back inside it, padded by this many seconds
TRANS_STEP = 1.1              # MW: the platform keeps 1 Hz evidence for programme steps this large
TRANS_PRE, TRANS_POST = 30, 210
TRANS_RETENTION_DAYS = 14     # rate-of-change captures are kept for a fortnight

def local_to_utc(d, sec):
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(sec) - sim.LOCAL_OFFSET_H * 3600)

def window():
    """The window's arrays. Episodes are detected inside the published extract windows, which is the
    only frequency series at one second the pack carries, so the generator's population and a
    solver's are the same set by construction."""
    out = {}
    for d in sim.dates():
        f = sim.frequency_day(d)
        exc = extract_windows(f)
        under, over = [], []
        for (a, b) in exc:
            seg = np.full(len(f), np.nan)
            seg[a:b + 1] = f[a:b + 1]
            masked = np.where(np.isnan(seg), 50.0, seg)
            for (t0, t1, tstar, fx) in sim.qualifying_episodes(d, masked):
                if a <= tstar <= b:
                    under.append((t0, t1, tstar, fx))
            for (t0, t1, tstar, fx) in over_episodes(masked):
                if a <= tstar <= b:
                    over.append((t0, t1, tstar, fx))
        out[d] = dict(f=f, under=sorted(set(under)), over=sorted(set(over)), exc=exc,
                      prog={s["id"]: sim.programme(s, d) for s in sim.SITES})
    return out

def extract_windows(f):
    """The operator's deviation extracts: each run beyond EXC_THRESH, widened to the last second the
    frequency was inside the dead band and the first second it returns, padded and merged."""
    inside = np.abs(f - 50.0) <= sim.DEADBAND
    wins = []
    for (a, b) in sim.excursions(f, EXC_THRESH, EXC_MIN_SECS):
        lo = a
        while lo > 0 and not inside[lo]:
            lo -= 1
        hi = b
        while hi < len(f) - 1 and not inside[hi]:
            hi += 1
        wins.append((max(0, lo - EXC_PAD), min(len(f) - 1, hi + EXC_PAD)))
    merged = []
    for w in sorted(wins):
        if merged and w[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], w[1]))
        else:
            merged.append(list(w) if False else (w[0], w[1]))
            merged[-1] = (w[0], w[1])
    out, cur = [], None
    for w in sorted(wins):
        if cur and w[0] <= cur[1]:
            cur = (cur[0], max(cur[1], w[1]))
        else:
            if cur: out.append(cur)
            cur = w
    if cur: out.append(cur)
    return out


def over_episodes(f):
    """Qualifying over-frequency episodes: f at or above 50.080 Hz for at least 15 seconds. The
    threshold sits above the operator's extract trigger, so every qualifying episode of either sign
    has published one-second frequency and recorded power behind it."""
    above = f >= 50.080
    out, i, n = [], 0, len(f)
    while i < n:
        if not above[i]:
            i += 1; continue
        j = i
        while j < n and above[j]:
            j += 1
        if j - i >= sim.QUALIFY_SECS:
            seg = f[i:j]; k = int(np.argmax(seg))
            out.append((i, j - 1, i + k, float(seg[k])))
        i = j
    return out

# The platform's high-resolution captures. The archive is not a single-purpose file: it holds the
# operator's deviation windows, the platform's own rate-of-change captures at setpoint steps, the
# captures taken around logged alarms and reserve withdrawals, the captures around mode changes and
# manual overrides, and the ad hoc captures a desk engineer took. Every capture's length and start
# offset vary, and the length distribution is the same for every site, so no recording's length
# carries anything about that site's traverse span.
RING = [8, 12, 15, 18, 22, 25, 30, 35, 40, 45]   # the pre-roll each site's ring buffer holds
POST_MIN, POST_JIT = 206, 84                     # the settle window a capture runs on afterwards
TRUNC_RATE = 0.08                                # captures the platform's buffer wrapped on
MISS_RATE = 0.38                                 # steps the capture queue was too busy to take
MANUAL_PER_SITE = 2                              # ad hoc captures a desk engineer took


RING_SALT = 191          # the configuration the nine sites were commissioned with


def ring(sid):
    """The pre-roll a site's ring buffer holds, a platform configuration and nothing else. The
    assignment is held at rank correlation zero against the sites' traverse spans, so a capture's
    length and start offset carry nothing about the quantity the determination turns on; checks.py
    asserts the correlation rather than trusting the choice."""
    return RING[sim._stable("ring%d" % RING_SALT, sid) % len(RING)]


def fit_boundaries(W, sid):
    """The settlement period boundaries a solver can fit a site's traverse over: the setpoint steps
    by more than a megawatt, the period before it was already settled, no qualifying episode of
    either sign runs through the window, and the frequency sits inside the dead band across it. The
    generator computes the same set the solver does, so the organ's exactness is asserted rather
    than hoped for: the first two of these per site are always captured and never truncated, and
    the capture queue is free to miss or wrap on any of the rest."""
    out = []
    marked = {}
    for d in sim.dates():
        if d < sim.dates()[-1] - dt.timedelta(days=TRANS_RETENTION_DAYS - 1):
            continue
        if d not in marked:
            m = np.zeros(sim.DAY + 400, dtype=bool)
            for (t0, t1, tstar, fx) in W[d]["under"] + W[d]["over"]:
                m[max(0, t0 - 120):min(sim.DAY, t1 + 121)] = True
            marked[d] = m
        prog = W[d]["prog"][sid]
        f = W[d]["f"]
        for p in range(2, 96):
            t = p * 900
            if abs(prog[p] - prog[p - 1]) < 1.0:
                continue
            if abs(prog[p - 1] - prog[p - 2]) > 0.35:
                continue
            if marked[d][max(0, t - 30):t + 215].any():
                continue
            quiet = True
            for mk in range(0, 5):
                m0 = (t // 60) + mk
                if m0 * 60 >= sim.DAY:
                    quiet = False
                    break
                seg = f[m0 * 60:(m0 + 1) * 60]
                if seg.min() < 50.0 - sim.DEADBAND or seg.max() > 50.0 + sim.DEADBAND:
                    quiet = False
                    break
            if quiet:
                out.append((d, p))
    return out


FIT_FLOOR = 3            # usable boundaries per site the capture queue never misses or wraps on


def _extreme_seconds(W):
    """Every (local date, site, extreme second) a qualifying episode of either sign puts in the
    measured population. No capture added after the operator's deviation windows may cover one of
    these, or it would change which recording the response is read from."""
    out = {}
    for d in sim.dates():
        for kind in ("under", "over"):
            for (t0, t1, tstar, fx) in W[d][kind]:
                for s in sim.SITES:
                    if sim.contracted(s, np.array([float(tstar)]), d)[0]:
                        out.setdefault((d, s["id"]), set()).add(tstar)
    return out


def recordings(W, events=()):
    """Every 1 Hz capture the platform archive holds: (date, site_id, trigger, lo, hi).

    `events` is (site, local date, local second, trigger) for each logged event the platform took a
    capture around, read from the control platform's own event log so the two files agree.
    """
    out = []
    retention_from = sim.dates()[-1] - dt.timedelta(days=TRANS_RETENTION_DAYS - 1)
    extremes = _extreme_seconds(W)
    occupied = {(d, s["id"]): [] for d in sim.dates() for s in sim.SITES}

    def take(d, sid, trig, lo, hi, guard_extremes):
        """Add a capture unless it would overlap one already taken, in which case the platform's
        buffer was busy, or unless it would cover a second the response is read at."""
        lo, hi = max(0, int(lo)), min(sim.DAY, int(hi))
        if hi - lo < 20:
            return False
        if any(not (hi <= a or lo >= b) for (a, b) in occupied[(d, sid)]):
            return False
        if guard_extremes and any(lo <= x < hi for x in extremes.get((d, sid), ())):
            return False
        out.append((d, sid, trig, lo, hi))
        occupied[(d, sid)].append((lo, hi))
        return True

    # 1. the operator's deviation windows, which are where every graded response is read
    for d in sim.dates():
        for (a, b) in W[d]["exc"]:
            lo, hi = a, min(sim.DAY, b + 1)
            for s in sim.SITES:
                if sim.contracted(s, np.arange(lo, hi), d).any():
                    take(d, s["id"], "FREQ-DEV", lo, hi, False)

    # 2. the platform's rate-of-change captures at a setpoint step, kept for a fortnight
    floor = {s["id"]: set(fit_boundaries(W, s["id"])[:FIT_FLOOR]) for s in sim.SITES}
    for d in sim.dates():
        if d < retention_from:
            continue
        for s in sim.SITES:
            sid = s["id"]
            prog = W[d]["prog"][sid]
            pre = ring(sid)
            for p in range(1, 96):
                if abs(prog[p] - prog[p - 1]) < TRANS_STEP:
                    continue
                r = sim._rng("cap", sid, d.isoformat(), p)
                kept = (d, p) in floor.get(sid, ())
                if not kept and r.random_sample() < MISS_RATE:
                    continue
                post = POST_MIN + int(r.randint(0, POST_JIT + 1))
                if not kept and r.random_sample() < TRUNC_RATE:
                    post = int(r.randint(40, 191))
                # the capture fires when the rate of change crosses the platform's threshold, a
                # second or two after the setpoint it is following steps
                delay = int(r.randint(0, 7))
                if take(d, sid, "DPDT", p * 900 - pre + delay, p * 900 + post + 1, True):
                    continue
                # the buffer was busy or the window ran into a capture already held; on one of the
                # boundaries the traverse is fitted over the platform keeps the short window instead
                if kept:
                    take(d, sid, "DPDT", p * 900 - pre + delay, p * 900 + POST_MIN + 1, True)

    # 3. the captures taken around a logged event, over the whole window
    for (sid, d, sec, trig) in events:
        r = sim._rng("evcap", sid, d.isoformat(), sec)
        pre = ring(sid) + int(r.randint(0, 25))
        length = int(r.randint(55, 241))
        take(d, sid, trig, sec - pre, sec - pre + length, True)

    # 4. the ad hoc captures a desk engineer took
    for s in sim.SITES:
        sid = s["id"]
        for k in range(MANUAL_PER_SITE):
            r = sim._rng("manual", sid, k)
            d = sim.dates()[int(r.randint(0, len(sim.dates())))]
            sec = int(r.randint(600, sim.DAY - 900))
            length = int(r.randint(45, 601))
            take(d, sid, "MANUAL", sec, sec + length, True)

    out.sort(key=lambda r: (r[0], r[1], r[3]))
    return out


def power_cache(W, recs):
    """1 Hz net active power for every recording, keyed (date, site_id, lo)."""
    cache = {}
    for (d, sid, trig, lo, hi) in recs:
        s = sim.SITE_BY_ID[sid]
        cache[(d, sid, lo)] = sim.site_power(s, d, W[d]["f"], W[d]["prog"][sid], lo, hi)
    return cache

def _find(recs_by_site, d, sid, t):
    for (dd, ss, trig, lo, hi) in recs_by_site.get((d, sid), []):
        if lo <= t < hi:
            return (lo, hi)
    return None

def covered(recs):
    """Every (date, site, second) the archive carries power for."""
    out = {}
    for (d, sid, trig, lo, hi) in recs:
        out.setdefault((d, sid), set()).update(range(lo, hi))
    return out


_scope_gate = lambda s, d, t: True       # build.py installs the reserve-withdrawal scope gate


def episode_table(W, recs, cache, kind="under"):
    """One row per (site, qualifying episode the site was contracted for), with the response on each
    baseline. All of it reads the recorded 1 Hz power, exactly as the shipped archive carries it."""
    by_site = {}
    for r in recs:
        by_site.setdefault((r[0], r[1]), []).append(r)
    cov = covered(recs)
    rows = []
    for d in sim.dates():
        f = W[d]["f"]
        inside = np.abs(f - 50.0) <= sim.DEADBAND
        eps = W[d][kind]
        for (t0, t1, tstar, fext) in eps:
            k = t0
            while k > 0 and not inside[k]:
                k -= 1
            for s in sim.SITES:
                sid = s["id"]
                if not sim.contracted(s, np.array([float(tstar)]), d)[0]:
                    continue
                # clause 2: the parts of a delivery block the site was withdrawn from reserve for
                # are out of scope. On the under-frequency side every logged window is placed clear
                # of every qualifying episode, so this gate is inert there and checks.py asserts it.
                if not _scope_gate(s, d, tstar):
                    continue
                if tstar not in cov.get((d, sid), ()):
                    continue
                w = _find(by_site, d, sid, tstar)
                if w is None:
                    continue
                lo, hi = w
                P = cache[(d, sid, lo)]
                prog = W[d]["prog"][sid]
                p = min(95, tstar // 900)
                prev = prog[p - 1] if p > 0 else prog[0]
                cur = prog[p]
                dev = abs(50.0 - fext) - sim.DEADBAND
                cg = s["cap"] / sim.SPAN
                sgn = 1.0 if kind == "under" else -1.0
                v = P[tstar - lo]
                frac = min(1.0, max(0.0, (tstar - p * 900) / float(s["ramp_s"])))
                base_traj = prev + (cur - prev) * frac
                base_lin = prev + (cur - prev) * ((tstar - p * 900) / 900.0)
                has_pre = lo <= k < hi
                rows.append(dict(date=d, site=sid, t0=t0, tstar=tstar, fext=fext, dev=dev,
                                 period=int(p), prev=float(prev), cur=float(cur), p_at=float(v),
                                 p_pre=(float(P[k - lo]) if has_pre else None),
                                 resp_traj=sgn * (v - base_traj) / dev / cg,
                                 resp_pre=(sgn * (v - P[k - lo]) / dev / cg if has_pre else None),
                                 resp_sp=sgn * (v - cur) / dev / cg,
                                 resp_lin=sgn * (v - base_lin) / dev / cg,
                                 base_traj=float(base_traj)))
    return rows

_MET_CACHE = {}


# Each meter's own measurement stream. The index selects the stream, and the nine were chosen so
# that all twenty graded exposure figures sit at least 0.3 of their printed tenth of a megawatt
# hour from a bin edge; checks.py asserts the clearance rather than trusting the choice.
MDEV = {"VKF-DLK": 7, "VKF-HGZ": 0, "VKF-KPV": 20, "VKF-MPD": 7, "VKF-NWV": 4,
        "VKF-OOS": 1, "VKF-RDL": 8, "VKF-TRB": 10, "VKF-ZWT": 7}


def metered(W, d, sid):
    key = (d, sid)
    if key not in _MET_CACHE:
        _MET_CACHE[key] = _metered(W, d, sid)
    return _MET_CACHE[key]


def _metered(W, d, sid):
    """Settlement meter: net MWh per quarter hour for one site and local date. The meter sits at
    the connection and registers the site's own auxiliary draw, which the platform's net active
    power channel does not, so the registered energy sits a little under the integral of the
    recorded power and carries the meter's own measurement spread."""
    s = sim.SITE_BY_ID[sid]
    prog = W[d]["prog"][sid]
    f = W[d]["f"]
    out = np.zeros(96)
    for p in range(96):
        lo, hi = p * 900, (p + 1) * 900
        P = sim.site_power(s, d, f, prog, lo, hi)
        out[p] = P.mean() * 0.25
    r = sim._rng("meterdev%d" % MDEV[sid], sid, d.isoformat())
    out = out + r.normal(-0.0008 * s["pmax"], 0.0020 * s["pmax"], 96)
    return np.round(out, 4)

def site_scores(rows):
    """Mean of the per-episode ratios, per site, on each baseline, as percentages."""
    agg = {}
    for r in rows:
        a = agg.setdefault(r["site"], dict(n=0, traj=[], pre=[], sp=[], lin=[]))
        a["n"] += 1
        a["traj"].append(r["resp_traj"])
        if r["resp_pre"] is not None:
            a["pre"].append(r["resp_pre"])
        a["sp"].append(r["resp_sp"]); a["lin"].append(r["resp_lin"])
    out = {}
    for sid, a in agg.items():
        out[sid] = dict(n=a["n"], traj=100 * float(np.mean(a["traj"])),
                        pre=100 * float(np.mean(a["pre"])) if a["pre"] else float("nan"),
                        sp=100 * float(np.mean(a["sp"])), lin=100 * float(np.mean(a["lin"])))
    return out

def ranked(scores, key="traj"):
    return sorted(scores.items(), key=lambda kv: (round(kv[1][key], 1), kv[0]))

if __name__ == "__main__":
    W = window()
    recs = recordings(W)
    print("recordings", len(recs), "rows", sum(h - l for (_, _, _, l, h) in recs))
    cache = power_cache(W, recs)
    rows = episode_table(W, recs, cache, "under")
    sc = site_scores(rows)
    print("%-9s %4s %8s %8s %8s %8s" % ("site", "n", "GOLDEN", "pre", "setpoint", "linear"))
    for sid, v in sorted(sc.items()):
        print("%-9s %4d %8.1f %8.1f %8.1f %8.1f" % (sid, v["n"], v["traj"], v["pre"], v["sp"], v["lin"]))
    for key in ("traj", "pre", "sp", "lin"):
        o = ranked(sc, key)
        print("%-9s worst->: %s" % (key, " ".join("%s(%.1f)" % (k, v[key]) for k, v in o[:4])))
    ov = site_scores(episode_table(W, recs, cache, "over"))
    print("over-frequency:", " ".join("%s(%.1f,n=%d)" % (k, v["traj"], v["n"]) for k, v in sorted(ov.items())))
