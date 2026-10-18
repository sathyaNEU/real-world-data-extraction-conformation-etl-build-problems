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
TRANS_RETENTION_DAYS = 6      # 1 Hz transition evidence is kept for six days

def local_to_utc(d, sec):
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(sec) - sim.LOCAL_OFFSET_H * 3600)

def window():
    out = {}
    for d in sim.dates():
        f = sim.frequency_day(d)
        out[d] = dict(f=f,
                      under=sim.qualifying_episodes(d, f),
                      over=over_episodes(f),
                      exc=extract_windows(f),
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
    """Qualifying over-frequency episodes: f at or above 50.080 Hz for at least 15 seconds."""
    above = f >= 50.060
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

def recordings(W):
    """Every 1 Hz recording the platform archive holds: (date, site_id, trigger, lo, hi)."""
    out = []
    first = sim.dates()[0]
    retention_from = sim.dates()[-1] - dt.timedelta(days=TRANS_RETENTION_DAYS - 1)
    for d in sim.dates():
        occupied = {s["id"]: [] for s in sim.SITES}
        for (a, b) in W[d]["exc"]:
            lo, hi = a, min(sim.DAY, b + 1)
            for s in sim.SITES:
                if sim.contracted(s, np.arange(lo, hi), d).any():
                    out.append((d, s["id"], "frequency_excursion", lo, hi))
                    occupied[s["id"]].append((lo, hi))
        if d < retention_from:
            continue
        for s in sim.SITES:
            prog = W[d]["prog"][s["id"]]
            for p in range(1, 96):
                if abs(prog[p] - prog[p - 1]) < TRANS_STEP:
                    continue
                lo, hi = max(0, p * 900 - TRANS_PRE), min(sim.DAY, p * 900 + TRANS_POST + 1)
                if any(not (hi <= a or lo >= b) for (a, b) in occupied[s["id"]]):
                    continue
                out.append((d, s["id"], "programme_transition", lo, hi))
                occupied[s["id"]].append((lo, hi))
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

def episode_table(W, recs, cache, kind="under"):
    """One row per (site, qualifying episode the site was contracted for), with the response on each
    baseline. All of it reads the recorded 1 Hz power, exactly as the shipped archive carries it."""
    by_site = {}
    for r in recs:
        by_site.setdefault((r[0], r[1]), []).append(r)
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
                w = _find(by_site, d, sid, tstar)
                if w is None:
                    continue
                lo, hi = w
                if not (lo <= k < hi):
                    continue
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
                rows.append(dict(date=d, site=sid, t0=t0, tstar=tstar, fext=fext, dev=dev,
                                 period=int(p), prev=float(prev), cur=float(cur), p_at=float(v),
                                 p_pre=float(P[k - lo]),
                                 resp_traj=sgn * (v - base_traj) / dev / cg,
                                 resp_pre=sgn * (v - P[k - lo]) / dev / cg,
                                 resp_sp=sgn * (v - cur) / dev / cg,
                                 resp_lin=sgn * (v - base_lin) / dev / cg,
                                 base_traj=float(base_traj)))
    return rows

def metered(W, d, sid):
    """Settlement meter: net MWh per quarter hour for one site and local date."""
    s = sim.SITE_BY_ID[sid]
    prog = W[d]["prog"][sid]
    f = W[d]["f"]
    out = np.zeros(96)
    for p in range(96):
        lo, hi = p * 900, (p + 1) * 900
        P = sim.site_power(s, d, f, prog, lo, hi)
        out[p] = P.mean() * 0.25
    return np.round(out, 4)

def site_scores(rows):
    """Mean of the per-episode ratios, per site, on each baseline, as percentages."""
    agg = {}
    for r in rows:
        a = agg.setdefault(r["site"], dict(n=0, traj=[], pre=[], sp=[], lin=[]))
        a["n"] += 1
        a["traj"].append(r["resp_traj"]); a["pre"].append(r["resp_pre"])
        a["sp"].append(r["resp_sp"]); a["lin"].append(r["resp_lin"])
    out = {}
    for sid, a in agg.items():
        out[sid] = dict(n=a["n"], traj=100 * float(np.mean(a["traj"])), pre=100 * float(np.mean(a["pre"])),
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
