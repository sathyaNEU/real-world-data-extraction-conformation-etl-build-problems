"""The Quillfield world: encounters, medication orders, the alerts each signing fires against the patient's active
orders, the prescribers' answers, the package's background log, Corvane's desk queue, and the replays the checks use
for the truth (never shipped).

Every answer to an alert is drawn from a hash of the order, the interacting order and the rule, so a replay of the
same orders with the package live changes only what the package's own alerts and their removals change."""
import datetime as dt
import math

import numpy as np

import params as P

M64 = (1 << 64) - 1
EPOCH = dt.datetime(2024, 11, 1)
RULE_CODE = {r: i + 1 for i, r in enumerate(P.RULES)}


def _mix(x):
    x = (x + 0x9E3779B97F4A7C15) & M64
    z = ((x ^ (x >> 30)) * 0xBF58476D1CE4E5B9) & M64
    z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
    return (z ^ (z >> 31)) & M64


def hu(*vals):
    """A uniform in [0, 1) keyed by the values, the same in every run and every replay."""
    x = P.SEED
    for v in vals:
        x = _mix(x ^ (v & M64))
    return x / 18446744073709551616.0


def tday(t):
    return (EPOCH + dt.timedelta(days=t)).date()


def tstamp(t):
    return EPOCH + dt.timedelta(seconds=int(round(t * 86400)))


class Enc:
    __slots__ = ("key", "unit", "utype", "adm", "dis", "orders")


# Prescribing follows the ward day: few signings overnight, a peak on the morning round. Every time in an encounter
# passes through one monotone map of the hour within its own day, so no ordering between two events, and no event's
# date, changes.
HOURLY = (0.40, 0.30, 0.25, 0.25, 0.30, 0.45, 0.80, 1.40, 2.00, 2.20, 2.00, 1.70, 1.50, 1.50, 1.60, 1.60, 1.50, 1.40,
          1.30, 1.20, 1.10, 1.00, 0.80, 0.60)
_TOT = sum(HOURLY)
_CUM = [0.0]
for _w in HOURLY:
    _CUM.append(_CUM[-1] + _w / _TOT)


def ward_clock(t):
    day = math.floor(t)
    u = t - day
    for h in range(24):
        if u < _CUM[h + 1] or h == 23:
            span = _CUM[h + 1] - _CUM[h]
            return day + (h + (u - _CUM[h]) / span) / 24.0
    return t


def _draw_encounters(rng, d0, d1, units, start_key):
    """Every encounter takes a fixed block of draws, so a change to one propensity moves only the orders it governs."""
    encs = []
    key = start_key
    ndays = (d1 - d0).days + 1
    for (code, _name, utype, rate, los, _pilot) in units:
        pr = P.PROP[utype]
        for i in range(ndays):
            day = d0 + dt.timedelta(days=i)
            n = rng.poisson(rate * P.SEASON[day.month])
            base = (dt.datetime.combine(day, dt.time()) - EPOCH).total_seconds() / 86400.0
            for _ in range(n):
                key += 1
                v = rng.random(12)
                x = rng.exponential(1.0, 12)
                z = rng.normal(size=2)
                n_oth = min(4, int(rng.poisson(P.LAMBDA_OTHER)))
                ou = rng.random(4)
                di = rng.integers(0, 10 ** 6, 14)
                e = Enc()
                e.key, e.unit, e.utype = key, code, utype
                hr = ((14.5 + 4.0 * z[0]) % 24.0) if v[0] < 0.65 else v[1] * 24.0
                e.adm = base + hr / 24.0
                e.dis = e.adm + max(0.4, math.exp(math.log(los) - 0.15 + 0.55 * z[1]))
                a, L = e.adm, e.dis
                orders = []
                slot = [0]

                def add(cls, t, dur):
                    j = slot[0]
                    slot[0] += 1
                    if t < L:
                        drug = P.DRUGS[cls][int(di[j]) % len(P.DRUGS[cls])]
                        orders.append((key * 64 + j + 1, cls, drug, t, min(L, t + dur)))
                if v[2] < pr[0]:
                    t1 = a + 0.30 * x[0]
                    add("OPI", t1, 0.5 + 2.5 * x[1])
                    if v[3] < pr[1]:
                        add("OPI", t1 + 0.60 * x[2], 0.5 + 2.2 * x[3])
                slot[0] = 2
                if v[4] < pr[2]:
                    t1 = a + 0.8 + 1.3 * x[4]
                    add("SED", t1, 0.5 + 2.0 * x[5])
                    if v[5] < pr[3]:
                        add("SED", t1 + 1.0 * x[6], 0.5 + 1.6 * x[7])
                slot[0] = 4
                if v[6] < pr[4]:
                    add("ACG", a + 0.30 * x[8], 99.0)
                slot[0] = 5
                if v[7] < pr[5]:
                    add("NSA", a + 0.2 + 1.0 * x[9], 0.5 + 1.5 * x[8])
                slot[0] = 6
                if v[8] < pr[6]:
                    t1 = a + 0.60 * x[10]
                    add("QTP", t1, 0.3 + 1.5 * x[11])
                    if v[9] < pr[7]:
                        add("QTP", t1 + 1.0 * x[7], 0.3 + 1.4 * x[6])
                slot[0] = 8
                for j in range(n_oth):
                    add("OTH", a + ou[j] * (L - a), 0.5 + 2.0 * x[(j + 3) % 12])
                orders = [(k_, c_, d_, ward_clock(t_), ward_clock(en_)) for (k_, c_, d_, t_, en_) in orders]
                e.adm, e.dis = ward_clock(e.adm), ward_clock(e.dis)
                orders.sort(key=lambda o: (o[3], o[0]))
                e.orders = orders
                encs.append(e)
    return encs, key


def _other_rule(key):
    x = hu(key, 11)
    acc = 0.0
    for r, w in P.OTHER_MIX:
        acc += w
        if x < acc:
            return r
    return P.OTHER_MIX[-1][0]


def run(enc, mode_of, salt):
    """Process one encounter's signings in time order. mode_of(t) is 'off', 'bg' or 'live' for the package.
    Returns the visible alert rows (key, rule, partner, t, action, cls, drug) and the background rows."""
    active = []
    rows, bg = [], []
    for (key, cls, drug, t, end) in enc.orders:
        active = [a for a in active if a[2] > t]
        ex = []
        if cls == "OTH":
            r = _other_rule(key)
            if r == "DDI_MODERATE":
                if active:
                    ex.append((r, active[-1][0]))
            else:
                ex.append((r, 0))
        else:
            for (k2, c2, _e2, _d2) in active:
                if (cls, c2) in P.SEVERE_PAIRS:
                    ex.append(("DDI_SEVERE", k2))
            if hu(key, 21) < P.P_ALLERGY:
                ex.append(("DRUG_ALLERGY", 0))
            if hu(key, 22) < P.P_DOSE:
                ex.append(("MAX_DOSE", 0))
        pkg = []
        if cls == "OPI":
            opi = [a for a in active if a[1] == "OPI"]
            if opi:
                pkg.append(("MSP26_DUP_OPIOID_PRN", opi[0][0]))
        if cls == "QTP":
            for (k2, c2, _e2, _d2) in active:
                if c2 == "QTP":
                    pkg.append(("MSP26_QT_COMBO", k2))
        mode = mode_of(t)
        visible = ex + (pkg if mode == "live" else [])
        removed = False
        acts = []
        for (rule, pid) in visible:
            x = hu(key, pid, RULE_CODE[rule], salt if rule.startswith("MSP26") else 0)
            if x < P.P_REMOVE[rule]:
                a = "remove"
                removed = True
            elif x < P.P_REMOVE[rule] + P.P_MODIFY.get(rule, 0.0):
                a = "modify"
            else:
                a = "override" if P.RULES[rule][1] == "High" else "ack"
            acts.append(a)
        for (rule, pid), a in zip(visible, acts):
            action = "Order removed" if removed else {"override": "Overridden", "modify": "Order modified",
                                                      "ack": "Acknowledged"}[a]
            rows.append((key, rule, pid, t, action, cls, drug))
        if mode == "bg":
            for (rule, pid) in pkg:
                bg.append((key, rule, pid, t, cls, drug))
        if not removed:
            active.append((key, cls, end, drug))
    return rows, bg


def logged_mode(enc):
    if enc.unit in P.PILOT:
        return lambda t: "live"
    bg0 = (dt.datetime.combine(P.BG_START, dt.time()) - EPOCH).total_seconds() / 86400.0
    return lambda t: "bg" if t >= bg0 else "off"


def reviews_in(rows, t0, t1):
    return sum(1 for r in rows if r[1] in P.REVIEW_RULES and r[4] == "Overridden" and t0 <= r[3] < t1)


def tnum(d):
    return (dt.datetime.combine(d, dt.time()) - EPOCH).total_seconds() / 86400.0


def build_world():
    rng = np.random.default_rng(P.SEED)
    encs, last = _draw_encounters(rng, P.SIM_START, P.LOG_END, P.UNITS, 0)
    out = {"encs": encs, "rows": {}, "bg": {}}
    for e in encs:
        rows, bg = run(e, logged_mode(e), 0)
        out["rows"][e.key] = rows
        out["bg"][e.key] = bg
    out["last_key"] = last
    return out


def forecast_world(seed_shift=1, plan_growth=1.0):
    """Encounters on the units going live over the forecast weeks (with the run-in before them), for the truth."""
    rng = np.random.default_rng(P.SEED * 1000 + seed_shift)
    units = [u for u in P.UNITS if not u[5]]
    units = [(c, n, t, r * plan_growth, l, p) for (c, n, t, r, l, p) in units]
    encs, _ = _draw_encounters(rng, P.FC_SIM_START, P.FC_END, units, 10 ** 9)
    return encs


def truth_net(encs, t0, t1, salts):
    """Expected reviews with the package live minus reviews without it, over [t0, t1), on these encounters."""
    off = 0
    on = [0] * len(salts)
    for e in encs:
        r0, _ = run(e, lambda t: "off", 0)
        off += reviews_in(r0, t0, t1)
        for i, s in enumerate(salts):
            r1, _ = run(e, lambda t: "live", s)
            on[i] += reviews_in(r1, t0, t1)
    return sum(on) / len(on) - off, off, on
