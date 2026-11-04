"""The yard's operations from December 2025 to early January 2027, minute by minute: coal delivered to the boiler
house on the reclaim conveyor CV-21, ships discharged by the grab unloader GU-1 onto the stacker feed CV-01, coal
moved between pile areas through the crossover (both belts weigh it), the plant historian's 15-minute record with its
communication losses, the control room's totaliser readings and the port's berth log. The receipts between surveys are
set so that the yard's true stock at each flight is the stock the surveys show."""
import datetime as dt

import numpy as np

import world as W
import yard as Y

FI, UTC = W.FI, W.UTC
T0 = W.local("2025-12-01 00:00")
T1 = W.local("2027-01-04 00:00")
NMIN = int((T1 - T0).total_seconds() // 60)
D = dt.timedelta


def mi(t):
    return int((t.astimezone(UTC) - T0.astimezone(UTC)).total_seconds() // 60)


def at(i):
    return (T0.astimezone(UTC) + D(minutes=int(i))).astimezone(FI)


# (interval, contract, share of the interval's receipts or tonnes, commence in Finnish time, crossover move in a stop)
CALLS = [
    (0, "RL-HK-2025-03", 21400.0, "2025-12-05 09:20", False),
    (1, "RL-HK-2025-03", 0.36, "2025-12-21 07:40", False), (1, "RL-HK-2026-02", 0.30, "2026-01-02 14:10", False),
    (1, "RL-HK-2026-03", 0.34, "2026-01-09 06:30", False),
    (2, "RL-HK-2026-03", 0.38, "2026-01-19 11:00", False), (2, "RL-HK-2026-01", 0.30, "2026-01-27 08:15", False),
    (2, "RL-HK-2026-03", 0.32, "2026-02-04 13:40", True),
    (3, "RL-HK-2026-03", 0.34, "2026-02-16 10:30", False), (3, "RL-HK-2026-02", 0.335, "2026-02-24 07:50", False),
    (3, "RL-HK-2026-03", 0.325, "2026-03-06 15:20", False),
    (4, "RL-HK-2026-03", 0.52, "2026-03-25 09:00", False), (4, "RL-HK-2026-01", 0.48, "2026-04-06 12:30", False),
    (5, "RL-HK-2026-02", 0.55, "2026-04-22 08:00", True), (5, "RL-HK-2026-03", 0.45, "2026-05-04 10:10", False),
    (6, "RL-HK-2026-01", 0.55, "2026-05-19 07:30", False), (6, "RL-HK-2026-03", 0.45, "2026-06-02 09:45", False),
    (7, "RL-HK-2026-02", 0.52, "2026-06-23 08:20", False), (7, "RL-HK-2026-01", 0.48, "2026-07-06 06:50", True),
    (8, "RL-HK-2026-07", 1.00, "2026-08-04 03:00", False),
    (9, "RL-HK-2026-03", 1.00, "2026-09-02 11:30", False),
    (10, "RL-HK-2026-02", 1.00, "2026-09-22 09:10", False),
    (11, "RL-HK-2026-01", 0.36, "2026-10-19 07:00", True), (11, "RL-HK-2026-03", 0.30, "2026-10-29 10:40", False),
    (11, "RL-HK-2026-09", 0.34, "2026-11-09 08:30", False),
    (12, "RL-HK-2026-03", 0.315, "2026-11-22 12:20", True), (12, "RL-HK-2026-02", 0.36, "2026-12-01 07:40", True),
    (12, "RL-HK-2026-03", 0.325, "2026-12-09 14:00", False),
    (13, "RL-HK-2026-03", 22600.0, "2026-12-21 10:30", False),
]
# coal moved between pile areas while a pile area was rotated to its pad (Finnish time, start and end)
CLEARANCE_MOVES = [("2026-03-12 13:10", "2026-03-12 16:40"), ("2026-03-15 09:00", "2026-03-15 11:30"),
                   ("2026-04-09 14:00", "2026-04-09 17:20"), ("2026-05-07 08:30", "2026-05-07 12:00"),
                   ("2026-05-09 13:00", "2026-05-09 15:10"), ("2026-06-11 09:15", "2026-06-11 13:05"),
                   ("2026-09-24 13:30", "2026-09-24 16:40"),
                   ("2026-10-08 10:20", "2026-10-08 14:10"), ("2026-10-10 08:40", "2026-10-10 11:00")]


def true_density():
    return {c: float(np.mean([d for _, cc, _, d in W.DENSITY_TESTS if cc == c])) * W.TRUE_DENSITY_BIAS[c]
            for c in W.COALS}


def true_stocks():
    rho = true_density()
    vols = {p[0]: [Y.true_volume(p[0], m) for m in range(len(W.SURVEYS))] for p in W.PILES}
    stock = [sum(vols[p[0]][m] * rho[p[7]] for p in W.PILES) for m in range(len(W.SURVEYS))]
    return vols, stock


def daily_burn(rng):
    stop0, stop1 = (dt.date.fromisoformat(d) for d in W.UNIT2_STOP)
    day, weather, out = T0.date(), 0.0, {}
    while day < T1.date():
        key = day.strftime("%Y-%m")
        level = W.BURN[key]
        if key in ("2026-06", "2026-09"):
            unit2 = not (stop0 <= day < stop1)
            level = (1350 if key == "2026-06" else 1640) if unit2 else (330 if key == "2026-06" else 245)
        weather = 0.7 * weather + rng.normal(0, 0.045)
        out[day] = max(0.0, level * (1.0 + weather))
        day += D(days=1)
    return out


def simulate():
    rng = np.random.default_rng(W.SEED)
    cv21_x = np.zeros(NMIN)         # coal on CV-21 bound for the crossover, true t/min
    cv01_gu = np.zeros(NMIN)        # coal from the unloader
    cv01_x = np.zeros(NMIN)         # crossover coal on CV-01
    gu_run = np.zeros(NMIN, bool)
    hold = np.zeros(NMIN, bool)     # CV-21 kept free of deliveries
    moves = []

    def move(a, b, rate):
        cv21_x[a:b] += rate / 60.0
        cv01_x[a + 3:b + 3] += rate / 60.0
        hold[a - 40:b + 43] = True
        moves.append((a, b, rate))

    for s, e in CLEARANCE_MOVES:
        move(mi(W.local(s)), mi(W.local(e)), float(rng.uniform(*W.RECLAIM_RATE)))
    hold[mi(W.local("2026-06-09 08:00")):mi(W.local("2026-06-09 14:05"))] = True
    for m in range(len(W.SURVEYS)):
        a, b = W.flight(m)
        hold[mi(a) - 30:mi(b)] = True

    # ------------------------------------------------------------------ pass 1: delivery runs to the boiler house
    burn = daily_burn(rng)
    runs = []
    taken = np.zeros(NMIN, bool)
    for day, tonnes in burn.items():
        starts = [1.0, 7.5, 14.0, 20.0] if tonnes > 1500 else ([3.0, 15.5] if tonnes > 400 else [10.5])
        for h in starts:
            each = tonnes / len(starts)
            rate = float(rng.uniform(*W.RECLAIM_RATE))
            dur = max(8, int(round(each / rate * 60)))
            a = mi(dt.datetime.combine(day, dt.time(0), FI)) + int(h * 60) + int(rng.integers(-25, 26))
            while hold[max(a - 5, 0):a + dur + 5].any() or taken[max(a - 20, 0):a + dur + 20].any():
                a += 30
            if a + dur >= NMIN:
                continue
            taken[a:a + dur] = True
            runs.append([a, dur, each])

    def deliveries():
        arr = np.zeros(NMIN)
        for a, dur, each in runs:
            arr[a:a + dur] += each / dur
        return arr

    cv21_del = deliveries()

    # ------------------------------------------------------------------ receipts that make the surveys' stock
    vols, stock = true_stocks()
    fl = [mi(W.flight(m)[0]) for m in range(len(W.SURVEYS))]
    recv = {m: stock[m] - stock[m - 1] + cv21_del[fl[m - 1]:fl[m]].sum() for m in range(1, len(W.SURVEYS))}

    calls = []
    for k, (iv, contract, share, commence, xmove) in enumerate(CALLS):
        size = share if share > 1000 else recv[iv] * share
        rate = float(rng.uniform(*W.UNLOADER_RATE))
        t = mi(W.local(commence))
        left = size
        events = [(t, "START", "")]
        running_since, ran = t, 0.0
        wind_done = not xmove
        next_hatch = int(rng.integers(230, 330))
        while left > 1e-6:
            lt = at(t)
            if lt.hour in (7, 15, 23) and lt.minute == 0 and t > events[-1][0] + 30:
                dur = int(rng.integers(18, 36))
                events += [(t, "STOP", "SHIFT"), (t + dur, "START", "")]
                t += dur
                continue
            if t - running_since >= next_hatch:
                dur = int(rng.integers(14, 42))
                events += [(t, "STOP", "HATCH"), (t + dur, "START", "")]
                t += dur
                running_since, next_hatch = t, int(rng.integers(230, 330))
                continue
            if not wind_done and ran > 0.42 * size:
                dur = int(rng.integers(255, 345))
                events += [(t, "STOP", "WIND"), (t + dur, "START", "")]
                move(t + int(rng.integers(38, 52)), t + dur - int(rng.integers(44, 58)),
                     float(rng.uniform(*W.RECLAIM_RATE)))
                t += dur
                running_since, wind_done = t, True
                continue
            q = min(rate / 60.0, left)
            cv01_gu[t] += q
            gu_run[t] = True
            left -= q
            ran += q
            t += 1
        events.append((t, "STOP", "END"))
        calls.append(dict(k=k, iv=iv, contract=contract, size=size, rate=rate, events=events,
                          commence=events[0][0], complete=t, xmove=xmove))

    # ------------------------------------------------------------------ pass 2: runs clashing with a move wait for it
    c_before = [cv21_del[fl[m - 1]:fl[m]].sum() for m in range(1, len(W.SURVEYS))]
    taken[:] = False
    for r in sorted(runs):
        a, dur, _ = r
        while hold[max(a - 5, 0):a + dur + 5].any() or taken[max(a - 20, 0):a + dur + 20].any():
            a += 15
        r[0] = a
        taken[a:a + dur] = True
    cv21_del = deliveries()
    c_after = [cv21_del[fl[m - 1]:fl[m]].sum() for m in range(1, len(W.SURVEYS))]
    assert np.allclose(c_before, c_after), "a delivery run moved across a survey flight"
    outs = [(mi(W.local(a)), mi(W.local(b))) for a, b in W.OUTAGES]
    for kk, (before, after) in sorted(W.CALL_OUTAGES.items()):
        end = calls[kk]["complete"]
        a = (end - int(before * 60)) // 15 * 15
        b = -(-(end + int(after * 60)) // 15) * 15
        outs.append((a, b))
    return dict(cv21_del=cv21_del, cv21_x=cv21_x, cv01_gu=cv01_gu, cv01_x=cv01_x, gu_run=gu_run, calls=calls,
                moves=moves, stock=stock, vols=vols, recv=recv, burn=burn, flights=fl, runs=runs,
                outs=sorted(outs), swap=mi(W.local(W.CV21_SWAP)))


def historian(x):
    """15-minute weighed tonnage per conveyor (UTC intervals), as the historian computes it from each integrator's
    totaliser: zero while the link is down, then the whole outage in the first interval after it returns."""
    out = {}
    for tag, flow in (("CV-01", x["cv01_gu"] + x["cv01_x"]), ("CV-21", x["cv21_del"] + x["cv21_x"])):
        q = flow * W.SCALE_ERR[tag]
        n = NMIN // 15
        iv = q[:n * 15].reshape(n, 15).sum(1)
        for a, b in x["outs"]:
            ia, ib = a // 15, b // 15
            iv[ib] += iv[ia:ib].sum()
            iv[ia:ib] = 0.0
        out[tag] = iv
    return out


def totalisers(x):
    """Each integrator's totaliser (t) at the end of every minute; CV-21's restarts at zero when its integrator is
    replaced."""
    c01 = 4218553.0 + np.cumsum((x["cv01_gu"] + x["cv01_x"]) * W.SCALE_ERR["CV-01"])
    c21 = 3907112.4 + np.cumsum((x["cv21_del"] + x["cv21_x"]) * W.SCALE_ERR["CV-21"])
    s = x["swap"]
    c21[s:] = c21[s:] - c21[s - 1]
    return c01, c21
