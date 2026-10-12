"""The simulation behind the pack: traffic, the pairs in each sector, the occurrence record, the network manager's
regulations and slot allocations, and the configuration log. Deterministic (fixed seeds)."""
import numpy as np

import configs as CF
import nm as NM
import occurrences as O
import traffic as T
import world as W

SEED_IDS = 18159


def ifplids(n, rng):
    letters = "ABCDEFGHJKLMNPRSTUVWXYZ"
    out, seen = [], set()
    while len(out) < n:
        pid = "A%s%08d" % (letters[int(rng.integers(len(letters)))], int(rng.integers(10 ** 8)))
        if pid not in seen:
            seen.add(pid)
            out.append(pid)
    return out


def loss_constraints(t, fh_by):
    """The realised record stays near its expectation where a forecaster would lean on it: every sector's summer 2025
    and summer 2026 rate per 100,000 flight hours at least 6 per cent under the tolerance; the centre's rate per pair
    that changed order, on every window a forecaster might fit, within a few per cent of the rate that generated it;
    Tarvik's own rate within 12 per cent of it. Tarvik's two summer 2026 losses, Hallin's one and two losses in the
    summers either side of the March 2026 re-route, and a summer 2026 total at or under its expectation are the
    record's draw; each sector's own rate per pair differs from the next by ordinary chance, not by design."""
    def check(counts, cross_by):
        s25, s26 = [5, 6, 7], [17, 18, 19]
        for s in range(8):
            for win, key in ((s25, "s25"), (s26, "s26")):
                n = sum(counts[s][m] for m in win)
                if n / fh_by[s][key] * 1e5 > W.TOLERANCE / 1.06:
                    return False
        if sum(counts[0][m] for m in s26) != 2:
            return False
        if sum(counts[6][m] for m in s25) != 1 or sum(counts[6][m] for m in s26) != 2:
            return False
        if sum(counts[s][m] for s in range(8) for m in s26) > np.floor(W.LAMBDA_ATM * sum(cross_by[s][m] for s in range(8) for m in s26)):
            return False

        def lam(win, ss=range(8)):
            n = sum(counts[s][m] for s in ss for m in win)
            c = sum(cross_by[s][m] for s in ss for m in win)
            return n / c
        allw = list(range(21))
        for win, tol in ((allw, 0.02), (s25 + s26, 0.04), (s26, 0.06), (list(range(12, 21)), 0.04)):
            if abs(lam(win) / W.LAMBDA_ATM - 1) > tol:
                return False
        if abs(lam(allw, [0]) / W.LAMBDA_ATM - 1) > 0.12:
            return False
        own = [lam(allw, [s]) for s in range(8)]
        return 1.12 <= max(own) / min(own) <= 1.4
    return check


def ra_ok(ra, enc):
    """Every sector had at least two advisory encounters in summer 2026 and at least one that both crews reported."""
    a, b = W.season(2026)
    lo, hi = T.secs(a), T.secs(b)
    n = {s: 0 for s in range(8)}
    for e in enc:
        if lo <= e[3] < hi:
            n[e[0]] += 1
    rep = {}
    for r in ra:
        if lo <= r["tx"] < hi:
            rep[r["enc"]] = rep.get(r["enc"], 0) + 1
    both = {s: 0 for s in range(8)}
    for k, e in enumerate(enc):
        if rep.get(k, 0) == 2:
            both[e[0]] += 1
    return all(n[s] >= 2 and both[s] >= 1 for s in range(8))


def flight_hours(t):
    out = {}
    for s in range(8):
        m = t["sec"] == s
        d = {}
        for y, key in ((2025, "s25"), (2026, "s26")):
            a, b = W.season(y)
            mm = m & (t["t0"] >= T.secs(a)) & (t["t0"] < T.secs(b))
            d[key] = float((t["t1"][mm] - t["t0"][mm]).sum()) / 3600.0
        out[s] = d
    return out


def simulate():
    svcs, f, t = T.record()
    O.untie(f, t)
    fp, tp = T.planning(svcs)
    O.untie(fp, tp)
    pairs = O.pairs_of(t)
    fh = flight_hours(t)
    rng = np.random.default_rng(O.SEED)
    counts, cross_by, tries = O.schedule_losses(t, pairs, W.LAMBDA_ATM, rng, loss_constraints(t, fh))
    ev_atm = O.pick_events(t, pairs, counts, rng)
    used = {(e[0], e[5]) for e in ev_atm}
    counts_n, _, _ = O.schedule_losses(t, pairs, W.LAMBDA_NON, rng)
    ev_non = O.pick_events(t, pairs, counts_n, rng, exclude=used)
    used |= {(e[0], e[5]) for e in ev_non}
    occ = O.loss_rows(f, t, ev_atm, True, rng) + O.loss_rows(f, t, ev_non, False, rng)
    ra, enc = None, None
    for k in range(200):
        ra, enc = O.ra_rows(f, t, pairs, np.random.default_rng(O.SEED + 100 + k), used)
        if ra_ok(ra, enc):
            break
    else:
        raise SystemExit("no ACAS draw met the constraints")
    occ += ra + O.other_rows(f, t, rng)
    ids = ifplids(len(f["callsign"]), np.random.default_rng(SEED_IDS))
    regs = NM.regulations(np.random.default_rng(NM.SEED + 1))
    for k in range(300):
        slots = NM.allocations(f, t, ids, svcs, regs, seed=NM.SEED + 10 * k)
        g = NM.ask1(t, slots, regs)
        if all(abs((v * 100) % 1 - 0.5) >= 0.15 for v in g.values()):
            break
    else:
        raise SystemExit("no slot allocation draw put every delay per flight mid-bin")
    log = CF.log_rows()
    return dict(svcs=svcs, f=f, t=t, fp=fp, tp=tp, pairs=pairs, counts=counts, counts_n=counts_n,
                cross_by=cross_by, tries=tries, ev_atm=ev_atm, ev_non=ev_non, occ=occ, enc=enc, ids=ids, regs=regs,
                slots=slots, log=log, fh=fh)
