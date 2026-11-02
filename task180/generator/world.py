"""The clean truth of task180 architecture 5, simulated forward from params.py.

Gas bars: daily sales by hose, each meter's error as it drifts with the litres it passes and resets at a
calibration, the tank's true daily withdrawal (registered litres plus what the meters give away, plus
any release), deliveries against bills of lading, and the tank gauge's reading at each business-day close.

Cardlocks (the ask): minute by minute through October to December 2026, the fleet's transactions, the
drops (some short of their bills of lading), the gauge's delivery reports and its hourly inventory, and
one power cut.

Nothing here reads a shipped file. pack.py writes the shipped files from what this returns; analysis.py
and verify.py read only the shipped files.
"""
import datetime as dt
import math

import numpy as np

import params as P


def _rng(name):
    """One stream per component, so a change to one part of the world moves no other part's draws."""
    h = 0
    for ch in name:
        h = (h * 131 + ord(ch)) % (2 ** 31)
    return np.random.default_rng([P.SEED, h])


def days_between(a, b):
    n = (b - a).days + 1
    return [a + dt.timedelta(days=i) for i in range(n)]


DAYS = days_between(P.START, P.END)
ND = len(DAYS)
DIDX = {d: i for i, d in enumerate(DAYS)}


def _date(s):
    return dt.date.fromisoformat(s)


def manitoba_dst(d):
    """True when Manitoba's clocks read daylight time at 05:00 on day d (2nd Sunday March to 1st Sunday November)."""
    y = d.year
    mar = dt.date(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.date(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return mar <= d < nov


# ----------------------------------------------------------------- gas bars

def _season(kind):
    t = np.array([(d - dt.date(d.year, 1, 1)).days for d in DAYS], dtype=float)
    if kind == "truck":
        return 1.0 + 0.05 * np.sin(2 * np.pi * (t - 120) / 365.25)
    if kind == "farm":
        # seeding in May, harvest in September and October
        return 1.0 + 0.10 * np.exp(-((t - 135) / 18.0) ** 2) + 0.16 * np.exp(-((t - 252) / 17.0) ** 2) - 0.04
    return 1.0 + 0.05 * np.sin(2 * np.pi * (t - 105) / 365.25)


def _dow(kind):
    dow = np.array([d.weekday() for d in DAYS])
    if kind == "truck":
        f = np.array([1.12, 1.16, 1.15, 1.14, 1.08, 0.76, 0.59])
    else:
        f = np.array([0.92, 0.94, 0.97, 1.03, 1.19, 1.08, 0.87])
    return f[dow] / f.mean()


def _holidays():
    m = np.ones(ND)
    for i, d in enumerate(DAYS):
        if (d.month, d.day) == (12, 25):
            m[i] = 0.38
        elif (d.month, d.day) == (1, 1):
            m[i] = 0.62
        elif (d.month, d.day) == (12, 26):
            m[i] = 0.81
    return m


def hose_layout():
    """Fuelling points and hoses at each gas bar. Regular and premium on every fuelling point; diesel on
    the first dispenser's two sides, except Foam Lake, whose diesel is on the six truck lanes."""
    out = {}
    for code, town, prov, nfp, r, p, dsl, dfp, cap_r, cap_d, cap_p in P.SITES:
        hoses = []
        for fp in range(1, nfp + 1):
            hoses.append((fp, "R"))
            hoses.append((fp, "P"))
        if code == "GB-121":
            for fp in range(11, 11 + dfp):
                hoses.append((fp, "D"))
        elif code == "GB-142":
            for fp in range(9, 9 + dfp):                # Kamsack's diesel dispenser at the side island
                hoses.append((fp, "D"))
        else:
            for fp in range(1, dfp + 1):
                hoses.append((fp, "D"))
        out[code] = hoses
    return out


def dispenser_of(code, fp):
    if code == "GB-121" and fp >= 11:
        return 10 + (fp - 11) // 2 + 1     # truck island dispensers 11, 12, 13
    return (fp + 1) // 2                   # Kamsack's fuelling points 9 and 10 are dispenser 5


def calibration_events(code):
    """(date, dispensers or None for every dispenser at the site)"""
    out = []
    for e in P.CALIBRATIONS[code]:
        if isinstance(e, tuple):
            out.append((_date(e[0]), list(e[1])))
        else:
            out.append((_date(e), None))
    return out


def simulate_gasbars():
    rng_s = _rng("gasbar-sales")
    rng_h = _rng("gasbar-hoses")
    rng_m = _rng("gasbar-meters")
    rng_d = _rng("gasbar-deliveries")
    rng_g = _rng("gasbar-gauge")
    hol = _holidays()
    layout = hose_layout()
    tanks = {}
    for code, town, prov, nfp, r, p, dsl, dfp, cap_r, cap_d, cap_p in P.SITES:
        for prod, base, cap in (("R", r, cap_r), ("P", p, cap_p), ("D", dsl, cap_d)):
            kind = "truck" if (code == "GB-121" and prod == "D") else ("farm" if prod == "D" else "car")
            sd = 0.12 if kind == "truck" else (0.30 if prod == "P" else 0.19)   # premium sales are lumpier
            sales = base * _season(kind) * _dow(kind) * hol * np.exp(rng_s.normal(-sd * sd / 2, sd, ND))
            hoses = [h for h in layout[code] if h[1] == prod]
            nh = len(hoses)
            share = rng_h.dirichlet(np.full(nh, 60.0))
            jit = np.exp(rng_h.normal(0, 0.035, (nh, ND)))
            hl = share[:, None] * jit
            for (c, disp, s) in P.DISPENSER_SWAPS:
                if c == code:
                    for h, (fp, pr) in enumerate(hoses):
                        if dispenser_of(code, fp) == disp:
                            hl[h, DIDX[_date(s)]] = 0.0           # the dispenser is out for the day
            hl = hl / hl.sum(0, keepdims=True) * sales[None, :]
            hl = np.round(hl, 2)
            # meters: resets and drift
            resets = {h: [] for h in range(nh)}
            for s, disps in calibration_events(code):
                for h, (fp, pr) in enumerate(hoses):
                    if disps is None or dispenser_of(code, fp) in disps:
                        resets[h].append(s)
            for (c, disp, s) in P.DISPENSER_SWAPS:
                if c == code:
                    for h, (fp, pr) in enumerate(hoses):
                        if dispenser_of(code, fp) == disp:
                            resets[h].append(_date(s))
            for (c, fp0, pr0, s) in P.METER_SWAPS:
                if c == code and pr0 == prod:
                    for h, (fp, pr) in enumerate(hoses):
                        if fp == fp0:
                            resets[h].append(_date(s))
            err = np.zeros((nh, ND))
            krate = P.DRIFT_ML_PER_100K * np.exp(rng_m.normal(0, P.DRIFT_METER_SD, nh))
            for h in range(nh):
                rs = sorted(resets[h])
                pre = rng_m.uniform(1.5e5, 9.0e5)           # litres since the setting before the record
                a = rng_m.normal(0, P.AS_LEFT_SD_ML)
                L = pre
                ri = 0
                for i, d in enumerate(DAYS):
                    while ri < len(rs) and rs[ri] <= d:
                        L = 0.0
                        a = rng_m.normal(0, P.AS_LEFT_SD_ML)
                        ri += 1
                    err[h, i] = a + krate[h] * L / 1e5
                    L += hl[h, i]
            over = (hl * err / 20000.0).sum(0)               # litres the nozzles gave beyond the registered
            reg = hl.sum(0)
            tank_leak = np.zeros(ND)
            line_leak = np.zeros(ND)
            if (code, prod) in P.TANK_LEAK:
                d0, lph = P.TANK_LEAK[(code, prod)]
                tank_leak = np.array([lph * 24.0 if d >= d0 else 0.0 for d in DAYS])
            if (code, prod) in P.LINE_LEAK:
                d0, frac = P.LINE_LEAK[(code, prod)]
                line_leak = np.array([frac * (reg[i] + over[i]) if d >= d0 else 0.0 for i, d in enumerate(DAYS)])
            vac = np.zeros(ND)
            for (c, pr, s, water_l, product_l) in P.VACUUM_PUMPOUTS:
                if c == code and pr == prod:
                    vac[DIDX[_date(s)]] += product_l
            withdraw = reg + over + tank_leak + line_leak + vac
            tanks[(code, prod)] = dict(code=code, town=town, prov=prov, prod=prod, cap=cap, kind=kind,
                                       hoses=hoses, hose_litres=hl, err=err, krate=krate, resets=resets,
                                       reg=reg, over=over, tank_leak=tank_leak, line_leak=line_leak,
                                       vac=vac, withdraw=withdraw)
    # deliveries and the gauge, tank by tank
    carriers = list(P.CARRIERS_GB.keys())
    cw = np.array(list(P.CARRIERS_GB.values()))
    bol_rows = []
    for key in sorted(tanks):
        t = tanks[key]
        code, prod, cap = t["code"], t["prod"], t["cap"]
        w = t["withdraw"]
        mean_w = w.mean()
        V = np.zeros(ND + 1)
        V[0] = cap * rng_d.uniform(0.5, 0.8)
        recv = np.zeros(ND)
        drops = []
        site_carrier = carriers[0] if t["prov"] == "SK" and code not in ("GB-121",) else carriers[1]
        btrain = mean_w > 0.2 * cap                          # the truck stop's diesel comes by B-train
        for i, d in enumerate(DAYS):
            reorder = 0.62 * cap if btrain else max(0.42 * cap if mean_w > 0.12 * cap else 0.30 * cap, 2.2 * mean_w)
            if d.weekday() == 5 and not btrain:
                reorder += 1.2 * mean_w                   # no Sunday deliveries outside the truck stop
            if V[i] < reorder and (d.weekday() != 6 or btrain):
                target = 0.90 * cap
                q = target - V[i] + 0.45 * w[i]
                q = max(4000.0, min(q, 60000.0 if btrain else 44000.0))
                q = math.floor(q / 500.0) * 500.0
                bol_net = q
                delivered = bol_net * (1 + rng_d.normal(0, P.TERMINAL_SD))
                recv[i] = delivered
                hr = int(rng_d.integers(7, 17))
                mi = int(rng_d.integers(0, 60))
                lt = float(rng_d.uniform(1.0, 7.5))           # hours between loading and the drop
                temp_load = float(rng_d.normal(0, 1.5))       # loading temperature offset from the season, C
                drops.append(dict(day=d, hour=hr, minute=mi, net=bol_net, delivered=delivered, load_hours=lt,
                                  temp_offset=temp_load,
                                  carrier=site_carrier if rng_d.uniform() > 0.12 else carriers[1 - carriers.index(site_carrier)]))
            V[i + 1] = V[i] + recv[i] - w[i]
            if V[i + 1] < 0.05 * cap:
                raise AssertionError("tank %s %s ran dry on %s" % (code, prod, d))
        t["V"] = V
        t["recv"] = recv
        t["drops"] = drops
        # the gauge's shift-close reading at the business-day close, 05:00 on the site's wall clock (the
        # consoles follow the site's clock; in Manitoba that is daylight time from March to November)
        reading = V + rng_g.normal(0, P.ATG_NOISE_L, ND + 1)
        for (c, pr, s, step) in P.PROBE_REPLACEMENTS:
            if c == code and pr == prod:
                i0 = DIDX[_date(s)] + 1                       # the first close read by the new probe
                reading[i0:] += step
        t["atg"] = np.round(reading)
    return tanks


def gasbar_temperature():
    """Product temperature in the ground, degrees C, by day: a lagged, damped seasonal wave."""
    rng = _rng("gasbar-temp")
    t = np.array([(d - dt.date(d.year, 1, 1)).days for d in DAYS], dtype=float)
    base = 7.5 + 6.0 * np.sin(2 * np.pi * (t - 150) / 365.25)
    return base + rng.normal(0, 0.35, ND)


# ----------------------------------------------------------------- cardlocks, minute resolution
# The cardlock world runs a little either side of the quarter so that drops loaded on the last evening of a
# month (or of September) and dropped after midnight exist as they would in any quarter.

CL_T0 = dt.datetime(2026, 8, 1, 0, 0)                    # minute 0, Central Standard Time
CL_DAYS = days_between(dt.date(2026, 8, 1), dt.date(2027, 1, 8))
NMIN = len(CL_DAYS) * 1440


def minute_of(ts):
    return int((ts - CL_T0).total_seconds() // 60)


def time_of(m):
    return CL_T0 + dt.timedelta(minutes=int(m))


Q4_M0 = minute_of(dt.datetime.combine(P.Q4[0], dt.time(0)))
Q4_M1 = minute_of(dt.datetime.combine(P.Q4[1] + dt.timedelta(days=1), dt.time(0)))
O_S = minute_of(P.OUTAGE["start"])
O_E = minute_of(P.OUTAGE["end"])


def _hour_profile(prod):
    h = np.arange(24)
    if prod == "D":
        p = 0.30 + np.exp(-((h - 9.5) / 3.5) ** 2) + 0.8 * np.exp(-((h - 15.5) / 3.0) ** 2)
    else:
        p = 0.08 + np.exp(-((h - 8.0) / 2.5) ** 2) + 1.1 * np.exp(-((h - 16.5) / 2.5) ** 2)
    return p / p.sum()


def _next_window(t0, lo_h, hi_h, rng):
    """First minute at or after t0 inside the daily window [lo_h, hi_h) (hours, may wrap midnight), plus a
    random offset that keeps it inside the window."""
    for k in range(0, 3 * 1440):
        t = t0 + k
        h = (t % 1440) / 60.0
        inside = (lo_h <= h < hi_h) if lo_h < hi_h else (h >= lo_h or h < hi_h)
        if inside:
            span = int(((hi_h - lo_h) % 24) * 60)
            return t + int(rng.integers(0, max(1, span // 3)))
    raise AssertionError("no window")


def simulate_cardlocks():
    rng = _rng("cardlock")
    out = {}
    carriers = list(P.CARRIERS_CL.keys())
    cw = np.array(list(P.CARRIERS_CL.values()))
    for code, town, prov, ndp, nrp, dl, rl, cap_d, cap_r in P.CARDLOCKS:
        for prod, daily, npump, cap in (("D", dl, ndp, cap_d), ("R", rl, nrp, cap_r)):
            prof = _hour_profile(prod)
            mean_fill = 330.0 if prod == "D" else 58.0
            txns = []
            for di, d in enumerate(CL_DAYS):
                wk = 0.62 if d.weekday() == 6 else (0.82 if d.weekday() == 5 else 1.08)
                if (d.month, d.day) in ((12, 25), (1, 1)):
                    wk = 0.30
                expected = daily * wk * float(np.exp(rng.normal(0, 0.08)))
                n = int(rng.poisson(expected / mean_fill))
                hours = rng.choice(24, size=n, p=prof)
                secs = rng.integers(0, 3600, size=n)
                for k in range(n):
                    if prod == "D":
                        lit = float(np.clip(rng.gamma(4.0, mean_fill / 4.0), 40, 900))
                        flow = float(rng.uniform(55.0, 95.0))
                    else:
                        lit = float(np.clip(rng.gamma(5.0, mean_fill / 5.0), 12, 160))
                        flow = float(rng.uniform(30.0, 38.0))
                    lit = round(lit, 2)
                    start = di * 1440 + int(hours[k]) * 60 + int(secs[k]) // 60
                    dur = max(1, int(round(lit / flow)))
                    pump = int(rng.integers(1, npump + 1)) + (0 if prod == "D" else ndp)
                    txns.append([start, start + dur, lit, pump])
            if code == P.OUTAGE["site"]:
                txns = [x for x in txns if not (x[1] > O_S and x[0] < O_E)]
            txns.sort()
            out[(code, prod)] = dict(code=code, town=town, prov=prov, prod=prod, cap=cap, txns=txns, npump=npump)
    for key in sorted(out):
        c = out[key]
        code, prod, cap = c["code"], c["prod"], c["cap"]
        draw = np.zeros(NMIN + 60)
        for s, e, lit, pump in c["txns"]:
            draw[s:e] += lit / (e - s)
        draw = draw[:NMIN]
        level = np.zeros(NMIN + 1)
        level[0] = cap * float(rng.uniform(0.55, 0.8))
        inflow = np.zeros(NMIN + 120)
        reorder = 0.38 * cap
        maxq = 38000.0 if prod == "D" else 22000.0
        outage_tank = (code == P.OUTAGE["site"] and prod == "D")
        drops = []
        pending = None
        busy = -1
        m = 0
        while m < NMIN:
            if outage_tank and m == O_S + 40:
                pending = (m, "Whitesand Tankline")              # the drop that went in while the site was dark
            if pending is None and level[m] < reorder and m > busy:
                carrier = str(rng.choice(carriers, p=cw))
                if carrier == "Whitesand Tankline":
                    t0 = m + int(rng.integers(120, 600))
                    if rng.uniform() < 0.6:
                        t0 = _next_window(t0, 21, 7, rng)
                    else:
                        t0 = _next_window(t0, 7, 17, rng)
                else:
                    t0 = _next_window(m + int(rng.integers(90, 300)), 7, 17, rng)
                if outage_tank and O_S - 30 * 60 <= t0 <= O_E + 90:
                    pending = None                                 # the outage drop covers it
                    m += 1
                    level[m] = level[m - 1] + inflow[m - 1] - draw[m - 1]
                    continue
                elif code == P.OUTAGE["site"] and O_S - 60 <= t0 <= O_E + 30:
                    t0 = O_E + 30 + int(rng.integers(0, 60))       # no other drop while the site is dark
                pending = (t0, carrier)
            if pending is not None and m == pending[0]:
                carrier = pending[1]
                is_out = outage_tank and m == O_S + 40
                q = math.floor(min(0.92 * cap - level[m], maxq) / 500.0) * 500.0
                if q >= 6000:
                    short = 0.0
                    if carrier == P.SHORT_DROP["carrier"] and prod == "D" and rng.uniform() < P.SHORT_DROP["share"]:
                        short = float(round(rng.uniform(*P.SHORT_DROP["litres"])))
                    if is_out:
                        short = 245.0
                    delivered = q * (1 + float(rng.normal(0, P.TERMINAL_SD))) - short
                    rate = float(rng.uniform(640, 900))
                    dur = int(math.ceil(delivered / rate))
                    transit = int(rng.integers(150, 361)) if carrier == "Whitesand Tankline" else int(rng.integers(90, 241))
                    drops.append(dict(start=m, end=m + dur, bol=q, delivered=delivered, short=short, carrier=carrier,
                                      outage=is_out, load=m - transit, temp_offset=float(rng.normal(0, 1.5))))
                    inflow[m:m + dur] += delivered / dur
                    busy = m + dur + 30
                pending = None
            level[m + 1] = level[m] + inflow[m] - draw[m]
            if level[m + 1] < 0.04 * cap:
                raise AssertionError("cardlock %s %s ran low at %s" % (code, prod, time_of(m)))
            m += 1
        c["drops"] = drops
        c["inflow"] = inflow[:NMIN]
        c["level0"] = level[0]
    return out


def held_reports(drops, pulls, depth):
    """The console keeps its last `depth` delivery reports per tank; the office pulls them at each pull time.
    Returns the set of drop indices whose report reached at least one pull."""
    held = set()
    rep = sorted([i for i, d in enumerate(drops) if not d["outage"]], key=lambda i: drops[i]["rep_end"])
    for T in pulls:
        done = [i for i in rep if drops[i]["rep_end"] <= T]
        held.update(done[-depth:])
    return held


def settle_cardlock_windows(out):
    """The gauge opens a delivery report from the last steady reading before the level starts to rise and
    closes it once the level has held for a few minutes after the drop. No fuelling transaction runs across
    either edge (the next truck waits at the island while the tank is filled and is moved past the close
    here), nor across the hourly readings either side of a drop whose report never reached the office (the
    power cut, and reports the console had overwritten before a pull); the level series is rebuilt from the
    settled transactions."""
    rng = _rng("cardlock-settle")
    for key in sorted(out):
        c = out[key]
        txns = c["txns"]
        pulls = [minute_of(t) for t in P.REPORT_PULLS if (t, c["code"]) not in P.PULL_MISSED]
        seq = int(rng.integers(300, 900))
        for d in c["drops"]:
            d["rep_start"] = d["start"] - int(rng.integers(1, 4))
            d["rep_end"] = d["end"] + int(rng.integers(3, 6))
            if not d["outage"]:
                seq += 1
                d["delivery_no"] = seq
        held = held_reports(c["drops"], pulls, P.REPORT_DEPTH)
        for i, d in enumerate(c["drops"]):
            d["held"] = i in held
        edges = []
        for d in c["drops"]:
            if not d["outage"]:
                edges += [d["rep_start"], d["rep_end"]]
            if d["outage"] or not d["held"]:
                a = d["start"] - (d["start"] % 60)
                b = d["end"] - (d["end"] % 60) + 60
                if d["outage"]:
                    a = O_S - (O_S % 60)
                    b = O_E - (O_E % 60) + 60
                edges += [a - 60, a, b, b + 60]
                d["bracket"] = (a, b)
        changed = True
        guard = 0
        while changed:
            changed = False
            guard += 1
            assert guard < 50
            for edge in edges:
                for x in txns:
                    if x[0] < edge < x[1] or x[0] == edge or x[1] == edge:
                        dur = x[1] - x[0]
                        x[0] = edge + 1 + int(rng.integers(0, 4))
                        x[1] = x[0] + dur
                        if c["code"] == P.OUTAGE["site"] and x[1] > O_S and x[0] < O_E:
                            x[0] = O_E + 2 + int(rng.integers(0, 6))
                            x[1] = x[0] + dur
                        changed = True
            txns.sort()
        if c["code"] == P.OUTAGE["site"]:
            assert not any(x[1] > O_S and x[0] < O_E for x in txns), "a fill during the power cut"
        draw = np.zeros(NMIN + 120)
        for s, e, lit, pump in txns:
            draw[s:e] += lit / (e - s)
        draw = draw[:NMIN]
        level = np.zeros(NMIN + 1)
        level[0] = c["level0"]
        level[1:] = level[0] + np.cumsum(c["inflow"] - draw)
        assert level.min() > 0.03 * c["cap"], key
        c["draw"] = draw
        c["level"] = level
        c["txns"] = [t for t in txns if t[1] <= NMIN]
    return out


def build():
    gb = simulate_gasbars()
    cl = settle_cardlock_windows(simulate_cardlocks())
    return dict(gasbars=gb, cardlocks=cl, temp=gasbar_temperature())


if __name__ == "__main__":
    w = build()
    q4 = [i for i, d in enumerate(DAYS) if d >= P.Q4[0]]
    for k, t in sorted(w["gasbars"].items()):
        print(k, "sales/day %.0f" % t["reg"][q4].mean(), "over %.3f%%" % (100 * t["over"][q4].sum() / t["reg"][q4].sum()),
              "over L/h %.2f" % (t["over"][q4].sum() / (len(q4) * 24)), "drops", len(t["drops"]))
    for k, c in sorted(w["cardlocks"].items()):
        q4d = [d for d in c["drops"] if Q4_M0 <= d["start"] < Q4_M1]
        print(k, "txns", len(c["txns"]), "drops q4", len(q4d), "short", sum(d["short"] for d in q4d),
              "lost", sum(1 for d in q4d if not d["held"] and not d["outage"]),
              "outage", [time_of(d["start"]) for d in c["drops"] if d["outage"]])
