"""The terminal as it ran: ships' receipts into the tanks, the diesel header's line-up between TK-4 and TK-5, the
transfers, the vapour recovery unit (outlet and the product its absorber returns to a petrol tank), the tank stocks and the 06:00 AEST
dips, all driven by the loads sim.py made. Every quantity is a true movement; pack.py writes each system's record."""
import datetime as dt
import heapq

import numpy as np

import sim as S
import world as W

D = dt.timedelta
ALL_TANKS = ["TK-1", "TK-2", "TK-3", "TK-4", "TK-5"]
PET_TANK = {"ULP": "TK-1", "P95": "TK-2", "P98": "TK-3"}
TRANSFER_PLAN = [(dt.datetime(2026, 3, 11, 13, 20), "TK-5", "TK-4", 640_000),
                 (dt.datetime(2026, 5, 27, 9, 50), "TK-4", "TK-5", 410_000),
                 (dt.datetime(2026, 7, 22, 15, 5), "TK-5", "TK-4", 780_000),
                 (dt.datetime(2026, 9, 9, 10, 35), "TK-4", "TK-5", 520_000),
                 (dt.datetime(2026, 11, 18, 14, 10), "TK-5", "TK-4", 455_000),
                 (dt.datetime(2026, 12, 9, 8, 40), "TK-4", "TK-5", 690_000)]
# VRU-1's absorber draws its lean petrol from a tank and returns it, with the product it recovered, to the same tank:
# TK-1 except while a valve on TK-1's absorber connections was out for repair (local start, local end, tank, asset).
ABSORBER_PLAN = [(dt.datetime(2026, 7, 14, 10, 25), dt.datetime(2026, 8, 4, 15, 10), "TK-2", "HV-118"),
                 (dt.datetime(2026, 9, 8, 9, 40), dt.datetime(2026, 9, 25, 13, 55), "TK-3", "TK-1-N7"),
                 (dt.datetime(2026, 11, 16, 8, 50), dt.datetime(2026, 12, 7, 16, 20), "TK-3", "HV-119")]
EVAP_KG_DAY = {"TK-1": 6.0, "TK-2": 4.2, "TK-3": 3.6, "TK-4": 0.9, "TK-5": 0.9}


def boundary_windows():
    """Local windows around each quarter's opening midnight (22:00 the night before to 09:00) where no receipt or
    transfer runs, so every quarter's stock at midnight is the 06:00 AEST dip less the loads and returns between."""
    out = []
    for y, m in ((2026, 1), (2026, 4), (2026, 7), (2026, 10), (2027, 1)):
        mid = dt.datetime(y, m, 1)
        out.append((W.local_to_utc(mid - D(hours=2)), W.local_to_utc(mid + D(hours=9))))
    return out


def absorber_tank(utc):
    loc = W.to_local(utc)
    for a, b, tk, _ in ABSORBER_PLAN:
        if a <= loc < b:
            return tk
    return "TK-1"


def clear_of(windows, a, b):
    return all(b <= s or a >= e for s, e in windows)


def run(x, seed=W.SEED + 7):
    rng = np.random.default_rng(seed)
    loads = x["loads"]
    wins = boundary_windows()
    ours = [l for l in loads if l["terminal"] == "WARRENBY"]
    stock = {"TK-1": 4_310_000.0, "TK-2": 2_870_000.0, "TK-3": 1_620_000.0, "TK-4": 7_960_000.0, "TK-5": 2_140_000.0}
    hist = {k: [(W.SIM_START_UTC, stock[k])] for k in ALL_TANKS}
    heap = []
    seq = [0]

    def push(t, pri, kind, pay):
        seq[0] += 1
        heapq.heappush(heap, (t, pri, seq[0], kind, pay))

    for l in ours:
        push(l["utc"], 3, "load", l)
    # ---------------------------------------------------- VRU: what each petrol load sent it, hour by hour
    vru_eff = {m: 0.9885 + rng.normal(0, 0.0009) for m in range(1, 13)}
    hourly, outlet_15 = {}, {}
    for l in ours:
        if l["product"] == "DSL":
            continue
        kg = S.load_vapour(l)
        eff = vru_eff[W.to_local(l["utc"]).month] + rng.normal(0, 0.0006)
        rec = kg * eff
        hk = l["utc"].replace(minute=0, second=0, microsecond=0)
        hourly[hk] = hourly.get(hk, 0.0) + rec
        qk = l["utc"].replace(minute=(l["utc"].minute // 15) * 15, second=0, microsecond=0)
        outlet_15[qk] = outlet_15.get(qk, 0.0) + (kg - rec)
    returns = []
    for hk in sorted(hourly):
        litres = int(round(hourly[hk] / 0.641))
        if litres < 1:
            continue
        t = hk + D(hours=1, minutes=int(rng.integers(2, 40)), seconds=int(rng.integers(0, 60)))
        returns.append(dict(utc=t, litres=litres, tank=absorber_tank(t)))
        push(t, 2, "vru_return", (absorber_tank(t), litres))
    # ---------------------------------------------------- ships: a coastal tanker call about every nine days
    t = W.SIM_START_UTC + D(days=3, hours=7)
    vessels = ["MT Kestrel Spirit", "MT Coral Venture", "MT Argyle Star"]
    k = 0
    while t < W.SIM_END_UTC - D(days=2):
        push(t, 1, "call", vessels[k % 3])
        k += 1
        t = t + D(days=float(rng.uniform(7.2, 10.6)))
    for loc, src, dst, litres in TRANSFER_PLAN:
        push(W.local_to_utc(loc), 1, "transfer", (src, dst, litres))
    day = W.SIM_START_UTC + D(days=1)
    while day < W.SIM_END_UTC:
        push(day, 0, "evap", None)
        day = day + D(days=1)

    def apply(tk, delta, when):
        stock[tk] += delta
        hist[tk].append((when, stock[tk]))
    receipts, lineups, transfers = [], [], []
    header = ["TK-4"]
    last_dsl = [W.SIM_START_UTC]
    meter_total = [18_204_531]
    while heap:
        when, _, _, kind, pay = heapq.heappop(heap)
        if when > W.SIM_END_UTC:
            break
        if kind == "evap":
            for tk in ALL_TANKS:
                apply(tk, -EVAP_KG_DAY[tk] / 0.70, when)
        elif kind == "inc":
            tk, litres = pay
            apply(tk, litres, when)
        elif kind == "vru_return":
            apply(pay[0], pay[1], when)
        elif kind == "transfer":
            src, dst, litres = pay
            hours = litres / 245_000.0
            assert clear_of(wins, when, when + D(hours=hours))
            m0 = meter_total[0]
            meter_total[0] += litres
            actual = litres * (1 + rng.normal(0, 0.00035))
            transfers.append(dict(start=when, end=when + D(hours=hours), src=src, dst=dst, litres=litres,
                                  meter_start=m0, meter_end=meter_total[0]))
            steps = max(1, int(round(hours * 4)))
            for i in range(steps):
                ti = when + D(hours=hours * (i + 1) / steps)
                push(ti, 0, "inc", (src, -actual / steps))
                push(ti, 0, "inc", (dst, actual / steps))
        elif kind == "call":
            plan = []
            for p, tk in PET_TANK.items():
                cap = W.TANKS[tk]["capacity_kl"] * 1000.0
                if stock[tk] < 0.46 * cap:
                    plan.append((tk, p, int(round((0.93 * cap - stock[tk]) * float(rng.uniform(0.9, 1.0)) / 1000) * 1000)))
            off = "TK-5" if header[0] == "TK-4" else "TK-4"
            if stock[off] < 3_200_000.0:
                plan.append((off, "DSL", int(round((8_700_000 - stock[off]) * float(rng.uniform(0.92, 1.0)) / 1000) * 1000)))
            ts = when
            for tk, p, vol in plan:
                rate = 520_000.0 if p == "DSL" else 410_000.0
                hours = vol / rate + float(rng.uniform(0.3, 1.1))
                tries = 0
                while not clear_of(wins, ts, ts + D(hours=hours)):
                    ts = ts + D(hours=3)
                    tries += 1
                    assert tries < 40
                shore = int(round(vol * (1 + rng.normal(0, 0.0011))))
                bl = int(round(vol * (1 + rng.normal(0.0018, 0.0009))))
                receipts.append(dict(vessel=pay, tank=tk, product=p, start=ts, end=ts + D(hours=hours), shore=shore,
                                     bl=bl, call=when))
                actual = shore * (1 + rng.normal(0, 0.0004))
                steps = max(1, int(round(hours * 4)))
                for i in range(steps):
                    push(ts + D(hours=hours * (i + 1) / steps), 0, "inc", (tk, actual / steps))
                ts = ts + D(hours=hours) + D(minutes=float(rng.uniform(40, 110)))
        else:
            l = pay
            if l["product"] == "DSL":
                tk = header[0]
                if stock[tk] < 1_380_000.0:
                    other = "TK-5" if tk == "TK-4" else "TK-4"
                    # the change sits on a whole minute strictly after the old tank's last diesel load and at least
                    # half a minute before this one, so the shift log's HH:MM places every load on one tank; with no
                    # such minute between the two loads the change waits for the next load
                    lo = (last_dsl[0] + D(minutes=1)).replace(second=0, microsecond=0)
                    hi = (when - D(seconds=30)).replace(second=0, microsecond=0)
                    if stock[other] > 3_800_000.0 and lo <= hi:
                        span = int((hi - lo).total_seconds() // 60)
                        sw = lo + D(minutes=int(round(span * float(rng.uniform(0.15, 0.85)))))
                        assert last_dsl[0] < sw < when
                        lineups.append(dict(utc=sw, frm=tk, to=other))
                        header[0] = other
                        tk = other
                l["tank"] = tk
                last_dsl[0] = when
            else:
                l["tank"] = PET_TANK[l["product"]]
            apply(l["tank"], -l["actual_net"], when)
    vno = {}
    for r in receipts:
        if r["call"] not in vno:
            vno[r["call"]] = "V%03d" % (len(vno) + 214)
        r["voyage"] = vno[r["call"]]
    for tk in ALL_TANKS:
        lo = min(s for _, s in hist[tk])
        hi = max(s for _, s in hist[tk])
        assert lo > W.TANKS[tk]["heel_kl"] * 1000 * 0.9, (tk, lo)
        assert hi < W.TANKS[tk]["capacity_kl"] * 1000, (tk, hi)
    return dict(receipts=receipts, lineups=lineups, transfers=transfers, hist=hist, returns=returns,
                outlet_15=outlet_15, vru_eff=vru_eff)


def stock_at(hist, tk, utc):
    """True stock of a tank at a moment (after every change at or before it)."""
    h = hist[tk]
    if utc < h[0][0]:
        return h[0][1]
    lo, hi = 0, len(h) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if h[mid][0] <= utc:
            lo = mid
        else:
            hi = mid - 1
    return h[lo][1]
