"""task118 world: the clean truth behind every shipped file, drawn under params.SEED.

Calendar and weather for the 2024 to 2026 seasons, OP-7's event days, each event day's run position, the design
year, each programme's per-unit reduction, the evaluation samples, and the records the three asks read. build.py
writes the files; figs.py never imports this module."""
import datetime as dt
import hashlib
import math

import numpy as np

import params as P


def rng(*key):
    return np.random.default_rng([P.SEED] + [int(hashlib.sha256(str(k).encode()).hexdigest()[:8], 16) for k in key])


def days(y0, m0, d0, y1, m1, d1):
    d, end = dt.date(y0, m0, d0), dt.date(y1, m1, d1)
    while d <= end:
        yield d
        d += dt.timedelta(days=1)


# ---------------------------------------------------------------- weather, events and runs (2024 to 2026)

def _spell_map(spells):
    out = {}
    for d0, temps in spells:
        for i, t in enumerate(temps):
            out[d0 + dt.timedelta(days=i)] = t
    return out


def weather():
    """One row per day, 1 June to 30 September of each season: actual high and low, the day-ahead forecast high,
    whether OP-7 called the programmes, and the run position of an event day."""
    sp = _spell_map(P.SPELLS)
    out = []
    for yr in P.SEASONS:
        r = rng("weather", yr)
        x = 0.0
        prev = None
        for d in days(yr, 6, 1, yr, 9, 30):
            x = 0.62 * x + r.normal(0, 2.1)
            if d in sp:
                hi, lo = sp[d]
            else:
                hi = min(P.SUBTRIGGER_CAP - abs(r.normal(0, 0.25)), P.SUBTRIGGER_BASE[d.month] + x)
                lo = 77.5 + 0.56 * (hi - 100) + r.normal(0, 2.0)
                hi, lo = round(hi, 1), round(min(lo, hi - 14.0), 1)
            fc = hi + r.normal(0, 0.7)
            fc = max(fc, P.TRIGGER_F + 0.2) if hi >= P.TRIGGER_F else min(fc, P.TRIGGER_F - 0.6)
            wk = d.weekday() < 5 and d not in P.HOLIDAYS
            ev = wk and fc >= P.TRIGGER_F
            pos = (prev["pos"] + 1 if (prev and prev["event"]) else 1) if ev else 0
            row = dict(date=d, season=yr, high=round(hi, 1), low=round(lo, 1), forecast=int(round(fc)), event=ev,
                       pos=pos)
            out.append(row)
            prev = row
    return out


def events(wx=None):
    wx = wx or weather()
    return [w for w in wx if w["event"]]


# ---------------------------------------------------------------- the design year (Appendix B)

TEMP_SHAPE = [0.30, 0.24, 0.18, 0.12, 0.06, 0.00, 0.05, 0.17, 0.32, 0.47, 0.61, 0.73, 0.83, 0.91, 0.97, 1.00,
              0.99, 0.96, 0.90, 0.80, 0.66, 0.55, 0.45, 0.37]
LOAD_BASE_WD = [612, 588, 571, 562, 566, 598, 655, 702, 731, 752, 768, 781, 792, 801, 809, 815, 821, 829, 856, 842,
                801, 752, 701, 651]
LOAD_COOL = [6.2, 5.8, 5.5, 5.2, 5.0, 5.0, 5.4, 6.4, 7.6, 8.7, 9.7, 10.6, 11.4, 12.1, 12.8, 13.3, 13.8, 14.1, 14.6,
             14.0, 12.6, 11.0, 9.4, 7.6]


def design_year():
    sp = _spell_map(P.DESIGN_SPELLS)
    r = rng("design-year")
    daily = []
    x = 0.0
    for d in days(2027, 6, 1, 2027, 9, 30):
        x = 0.62 * x + r.normal(0, 2.0)
        if d in sp:
            hi, lo = sp[d]
        else:
            hi = min(P.SUBTRIGGER_CAP - abs(r.normal(0, 0.3)), P.SUBTRIGGER_BASE[d.month] + x)
            lo = min(77.5 + 0.56 * (hi - 100) + r.normal(0, 2.0), hi - 14.0)
        daily.append((d, round(hi, 1), round(lo, 1)))
    rows = []
    for i, (d, hi, lo) in enumerate(daily):
        prev3 = np.mean([daily[j][1] for j in range(max(0, i - 3), i)]) if i else hi
        wkend = d.weekday() >= 5 or d in P.HOLIDAYS
        day_noise = r.normal(0, 9.0)
        for h in range(24):
            t = round(lo + (hi - lo) * TEMP_SHAPE[h] + r.normal(0, 0.25), 1)
            base = LOAD_BASE_WD[h] * (0.93 if wkend else 1.0)
            load = base + LOAD_COOL[h] * max(0.0, t - 75.0) + 1.9 * max(0.0, prev3 - 104.0) + day_noise \
                + r.normal(0, 4.0)
            rows.append(dict(ts=dt.datetime(d.year, d.month, d.day, h), temp=t, load=int(round(load))))
    return rows


# ---------------------------------------------------------------- the programmes' reductions (clean truth)

def fresh(p, high, season):
    if p == "HBN":
        return P.HBN_SETTING_KW[season]
    a, b = P.FRESH[p]
    return a + b * (high - 112.0)


def reduction(p, ev, hour=P.PEAK_HOUR):
    """The expected reduction per enrolled unit in an event hour, kW (batteries: per battery dispatching)."""
    k = min(ev["pos"], 4) - 1
    if p == "HBN":
        return fresh(p, ev["high"], ev["season"])
    return fresh(p, ev["high"], ev["season"]) * P.DEPLETION[p][k] * P.HOUR_SHAPE[p][hour]


def design_truth(p):
    """Each programme's expected 18:00 reduction per enrolled unit on the design peak day (fourth day, 117.3F)."""
    ev = dict(pos=4, high=117.3, season=2026)
    if p == "HBN":
        return P.HBN_SETTING_KW[2026] * P.HBN_RESPONSE
    return reduction(p, ev)


# ---------------------------------------------------------------- identifiers

LETTERS = "ACDEFGHJKLMNPQRTUVWXY"
DIGITS = "0123456789"


def code(r, n, alphabet=LETTERS + DIGITS):
    return "".join(alphabet[int(i)] for i in r.integers(0, len(alphabet), n))


def luhn_digit(s):
    tot = 0
    for i, ch in enumerate(reversed(s)):
        v = int(ch)
        if i % 2 == 0:
            v *= 2
            if v > 9:
                v -= 9
        tot += v
    return str((10 - tot % 10) % 10)


def premise_id(r):
    body = "3" + "".join(str(int(v)) for v in r.integers(0, 10, 8))
    return body + luhn_digit(body)


STREETS = ["Mesquite Bend", "Palo Verde", "Ironwood", "Saguaro Ridge", "Desert Willow", "Agave", "Cholla Vista",
           "Brittlebush", "Creosote", "Ocotillo", "Javelina", "Coyote Wash", "Quail Run", "Roadrunner", "Sotol",
           "Mariposa", "Tumbleweed", "Sidewinder", "Canyon Wren", "Gila", "Verbena", "Juniper Mesa", "Arroyo Seco",
           "Pinnacle Peak", "Sunrise", "Copper Hill", "Old Mine", "Hohokam", "Silverbell", "Granite Dells",
           "Thunderbird", "Cactus Flower", "Whitetail", "Dove Valley", "Lone Cactus", "Rancho Vista"]
SUFFIX = [("Dr", "DRIVE"), ("Rd", "ROAD"), ("Ln", "LANE"), ("St", "STREET"), ("Way", "WAY"), ("Ave", "AVENUE"),
          ("Ct", "COURT"), ("Pl", "PLACE"), ("Blvd", "BOULEVARD"), ("Trl", "TRAIL")]
DIRS = [("W", "WEST"), ("E", "EAST"), ("N", "NORTH"), ("S", "SOUTH")]


def address(r):
    num = int(r.integers(1000, 12900))
    d = DIRS[int(r.integers(0, 4))]
    st = STREETS[int(r.integers(0, len(STREETS)))]
    sf = SUFFIX[int(r.integers(0, len(SUFFIX)))]
    unit = None
    if r.random() < 0.06:
        unit = str(int(r.integers(1, 40)))
    cis = "%d %s %s %s" % (num, d[0], st, sf[0]) + (" Unit %s" % unit if unit else "")
    vendor = "%d %s %s %s" % (num, d[1], st.upper(), sf[1]) + (" #%s" % unit if unit else "")
    return cis, vendor


# ---------------------------------------------------------------- Cool Credit evaluation panel

def cc_panel(evs):
    """Ridgeway's sample: per season, premises with a stratified holdout; per event day and panel hour, kWh."""
    out = []
    shape = {14: (2.55, 0.100), 15: (2.85, 0.110), 16: (3.05, 0.118), 17: (3.18, 0.124), 18: (3.15, 0.125),
             19: (2.92, 0.116)}
    for yr in P.SEASONS:
        r = rng("cc-panel", yr)
        n = P.CC_PANEL_HOMES
        scale = np.exp(r.normal(0, 0.28, n))
        scale = scale / scale.mean()
        order = np.argsort(scale)
        group = np.empty(n, dtype=object)
        for s in range(0, n, 20):                       # strata of twenty by size, five held out in each
            idx = order[s:s + 20]
            pick = r.permutation(len(idx))
            for j, ii in enumerate(idx):
                group[ii] = "holdout" if pick[j] < round(len(idx) * P.CC_HOLDOUT_SHARE) else "treatment"
        keys = set()
        names = []
        while len(names) < n:
            k = "R%s-%s" % (str(yr)[2:], code(r, 6))
            if k not in keys:
                keys.add(k)
                names.append(k)
        for ev in [e for e in evs if e["season"] == yr]:
            x = ev["high"] - 105.0
            k = min(ev["pos"], 4) - 1
            day = r.normal(0, P.CC_DAY_NOISE, n)
            for h in P.PANEL_HOURS:
                a, b = shape[h]
                kwh = scale * (a + b * x) + day + r.normal(0, P.CC_HOUR_NOISE, n)
                if h in P.PRECOOL_HOURS:
                    eff = P.PRECOOL_KWH[h] * P.DEPLETION["CC"][k] * scale
                    kwh = kwh + np.where(group == "treatment", eff, 0.0)
                else:
                    eff = reduction("CC", ev, h) * scale
                    kwh = kwh - np.where(group == "treatment", eff, 0.0)
                kwh = np.maximum(kwh, 0.05)
                ts = dt.datetime(ev["date"].year, ev["date"].month, ev["date"].day, h) + dt.timedelta(hours=7)
                for i in range(n):
                    out.append((yr, names[i], group[i], ts, round(float(kwh[i]), 3)))
    return out


# ---------------------------------------------------------------- Peak Time Rewards evaluation (group means)

def ptr_means(evs):
    out = []
    base = {14: (2.05, 0.070), 15: (2.22, 0.076), 16: (2.36, 0.082), 17: (2.45, 0.086), 18: (2.47, 0.088),
            19: (2.31, 0.082)}
    for yr in P.SEASONS:
        r = rng("ptr", yr)
        enrolled = P.PTR_ENROLLED[yr]
        sev = [e for e in evs if e["season"] == yr]
        for i, ev in enumerate(sev):
            grow = 1.0 + 0.035 * i / max(1, len(sev) - 1)
            n_all = int(enrolled * (0.985 + 0.015 * grow) + r.integers(-90, 90))
            n_c = int(round(n_all * P.PTR_CONTROL_SHARE)) + int(r.integers(-12, 12))
            n_t = n_all - n_c
            x = ev["high"] - 105.0
            for h in P.PANEL_HOURS:
                a, b = base[h]
                mu = a + b * x
                se_t, se_c = P.PTR_CUSTOMER_SD / math.sqrt(n_t), P.PTR_CUSTOMER_SD / math.sqrt(n_c)
                eff = reduction("PTR", ev, h) if h in P.EVENT_HOURS else (0.012 if h == 15 else 0.0)
                mt = mu - eff + r.normal(0, se_t)
                mc = mu + r.normal(0, se_c)
                out.append((yr, ev["date"], h, "alerted", n_t, round(mt, 4)))
                out.append((yr, ev["date"], h, "holdout", n_c, round(mc, 4)))
    return out


# ---------------------------------------------------------------- Business Demand Partners verification

def bdp_verified(evs):
    out = []
    for yr in P.SEASONS:
        r = rng("bdp", yr)
        n = P.BDP_SITES[yr]
        scale = np.exp(r.normal(0, 0.5, n))
        scale = scale / scale.mean()
        keys = []
        while len(keys) < n:
            k = "S%s%s" % (str(yr)[2:], code(r, 5, DIGITS + "BCDFGHJK"))
            if k not in keys:
                keys.append(k)
        for ev in [e for e in evs if e["season"] == yr]:
            out_today = r.random(n) < 0.035
            for h in P.EVENT_HOURS:
                v = scale * reduction("BDP", ev, h) + r.normal(0, P.BDP_SITE_NOISE, n)
                v = np.where(out_today, r.normal(0, 2.5, n), v)
                for i in range(n):
                    out.append((yr, ev["date"], keys[i], h, round(float(v[i]), 1)))
    return out


# ---------------------------------------------------------------- Home Battery Network fleet summary

def hbn_fleet(evs):
    out = []
    for yr in P.SEASONS:
        r = rng("hbn-fleet", yr)
        a, b = P.HBN_FLEET[yr]
        d0, d1 = dt.date(yr, 6, 1), dt.date(yr, 9, 30)
        for ev in [e for e in evs if e["season"] == yr]:
            f = (ev["date"] - d0).days / (d1 - d0).days
            enrolled = int(round(a + (b - a) * f)) + int(r.integers(-6, 7))
            setting = P.HBN_SETTING_KW[yr]
            drop = P.HBN_DROP_EVENTS.get(ev["date"])
            for h in P.EVENT_HOURS:
                share = P.HBN_RESPONSE + r.normal(0, 0.004)
                if drop and h >= 17:
                    share = drop + r.normal(0, 0.006)
                disp = int(round(enrolled * share))
                kw = disp * setting * (0.994 + r.normal(0, 0.003))
                out.append((ev["date"], h, enrolled, disp, setting, round(kw, 1)))
    return out


# ---------------------------------------------------------------- ask A: Cool Credit enrolment and Halvern's records

def utc(d, h, m=0, s=0):
    """An MST wall-clock time on date d as a naive UTC datetime."""
    return dt.datetime(d.year, d.month, d.day, h, m, s) + dt.timedelta(hours=7)


def _hours(r, a, b):
    return dt.timedelta(seconds=int(r.uniform(a, b) * 3600))


QUIET = (dt.datetime(2026, 7, 1), dt.datetime(2026, 7, 7))


def thermostats():
    """CIS enrolments, Halvern's registry, its change-only status log for 2026 and its 2026 acknowledgements.

    Returns a dict with rows for each file and, for checks, the premise-level truth inputs."""
    r = rng("cc-enrol")
    n = 10_640
    prem, seen = [], set()
    while len(prem) < n:
        p = premise_id(r)
        if p not in seen:
            seen.add(p)
            prem.append(p)
    serials, sseen = [], set()

    def new_serial(model):
        while True:
            s = ("H1" if model == "HC-100" else "H2") + code(r, 7)
            if s not in sseen:
                sseen.add(s)
                return s
    start = dt.datetime(2021, 3, 1)
    span = (dt.datetime(2026, 9, 15) - start).total_seconds()
    cis, devices, status, acks = [], [], [], []
    premises = []
    called = {e["date"] for e in events()}

    def off_event(d):
        while d in called:                                      # the CIS books changes on non-event days
            d += dt.timedelta(days=1)
        return d
    taken = set()
    for i, p in enumerate(prem):
        while True:
            cis_addr, ven_addr = address(r)
            key = cis_addr.upper()
            if key not in taken:
                taken.add(key)
                break
        u = r.random() ** 0.62                                  # enrolment grew over the years
        enrolled = off_event((start + dt.timedelta(seconds=u * span)).date())
        unen = None
        q = r.random()
        if enrolled < dt.date(2025, 10, 1) and q < 0.085:
            unen = enrolled + dt.timedelta(days=int(r.integers(120, 1300)))
        elif q < 0.110 and enrolled < dt.date(2026, 6, 1):
            unen = dt.date(2026, 6, 1) + dt.timedelta(days=int(r.integers(0, 120)))
        if unen:
            unen = off_event(unen)
        if unen and unen > dt.date(2026, 10, 15):
            unen = None
        model = "HC-100" if enrolled < dt.date(2024, 3, 1) else "HC-200"
        s1 = new_serial(model)
        reg1 = dt.datetime.combine(enrolled, dt.time(0)) - dt.timedelta(days=int(r.integers(0, 6))) + _hours(r, 8, 18)
        devs = [dict(serial=s1, model=model, addr=ven_addr, registered=reg1, retired=None, first=True)]
        if r.random() < P.CC_TWO_ZONE_SHARE:
            devs.append(dict(serial=new_serial(model), model=model, addr=ven_addr, registered=reg1 + _hours(r, 0.1, 2),
                             retired=None, first=False))
        replaced = None
        if r.random() < P.CC_REPLACED_SHARE * 1.15 and (unen is None or unen > dt.date(2026, 6, 1)):
            lo_t = max(dt.datetime(2025, 3, 1), reg1 + dt.timedelta(days=120))
            hi_t = dt.datetime(2026, 9, 5)
            if lo_t < hi_t:
                replaced = lo_t + dt.timedelta(seconds=int(r.uniform(0, (hi_t - lo_t).total_seconds())))
                devs[0]["retired"] = replaced
                a2 = ven_addr
                v = r.random()
                if v < 0.35:
                    a2 = a2.replace(" #", " UNIT ") if " #" in a2 else a2 + ""
                elif v < 0.55:
                    a2 = a2.title()
                elif v < 0.70:
                    a2 = a2.replace(" WEST ", " W ").replace(" EAST ", " E ").replace(" NORTH ", " N ")\
                        .replace(" SOUTH ", " S ")
                devs.append(dict(serial=new_serial("HC-200"), model="HC-200", addr=a2,
                                 registered=replaced + _hours(r, 0.2, 30), retired=None, first=False, replaces=s1))
        cis.append(dict(premise_id=p, service_address=cis_addr, account_no="%09d" % int(r.integers(10**8, 10**9)),
                        enrolled_serial=s1, enrolled_on=enrolled, unenrolled_on=unen))
        for d in devs:
            d["premise"] = p
        if unen:
            for d in devs:
                if d["retired"] is None and r.random() < 0.6:
                    d["retired"] = dt.datetime.combine(unen, dt.time(0)) + _hours(r, 24, 24 * 20)
                    if d["retired"] >= dt.datetime(2026, 10, 16, 14):      # not yet retired at Halvern's export
                        d["retired"] = None
        devices.extend(devs)
        premises.append(dict(premise=p, enrolled=enrolled, unen=unen, devs=devs))
    # status log: a snapshot at 2026-01-01 00:00 UTC for every device registered before it, then changes
    r2 = rng("cc-status")
    t0, t1 = dt.datetime(2026, 1, 1), dt.datetime(2026, 10, 1)
    state_at = {}
    for d in devices:
        if d["retired"] is not None and d["retired"] < t0:
            continue
        begin = max(t0, d["registered"])
        st = "ONLINE"
        if r2.random() < 0.04:
            st = "OFFLINE"
        chronic = r2.random() < 0.035
        if chronic:
            st = "OFFLINE"
        seq = [(begin, "ONLINE" if d["registered"] >= t0 else st)]
        t = begin
        end = min(t1, d["retired"]) if d["retired"] else t1
        sleepy = d["model"] == "HC-100" and r2.random() < 0.62
        while True:
            gap = dt.timedelta(hours=float(r2.exponential(880 if not chronic else 1400)))
            t = t + gap
            if t >= end:
                break
            cur = seq[-1][1]
            if cur in ("OFFLINE", "IDLE"):
                nxt = "ONLINE"
            else:
                pre = t.date() < P.HALVERN_IDLE_SWITCH
                p_idle = (0.64 if sleepy else 0.04) if pre else 0.46
                nxt = "IDLE" if r2.random() < p_idle else "OFFLINE"
                if nxt == "IDLE" and QUIET[0] <= t < QUIET[1]:
                    nxt = "OFFLINE"
            seq.append((t, nxt))
            if nxt != "ONLINE":
                back = dt.timedelta(hours=float(r2.exponential(42 if nxt == "OFFLINE" else 230))) + _hours(r2, 0.2, 3)
                if chronic and nxt == "OFFLINE":
                    back = dt.timedelta(days=float(r2.uniform(20, 120)))
                if t + back < end:
                    t = t + back
                    seq.append((t, "ONLINE"))
                else:
                    break
        if d["retired"] and d["retired"] < t1:
            seq.append((d["retired"] - _hours(r2, 0.5, 6), "OFFLINE"))
            seq.sort(key=lambda x: x[0])
        # the 6.0 rollout week: Halvern held radios awake from 1 July while the push went out on 6 July, so no
        # sleeping episode runs into July and no device reports IDLE until the new firmware is on
        push = QUIET[0]
        fixed = []
        for j, (ts, s) in enumerate(seq):
            nxt = seq[j + 1][0] if j + 1 < len(seq) else end
            if s == "IDLE" and ts < push < nxt:
                if push - ts < dt.timedelta(hours=2):
                    continue
                fixed.append((ts, s))
                span = (push - ts).total_seconds()
                wake = ts + dt.timedelta(seconds=int(r2.uniform(0.15, 0.97) * span))
                fixed.append((max(wake, ts + dt.timedelta(minutes=45)), "ONLINE"))
                continue
            fixed.append((ts, s))
        seq = sorted(fixed, key=lambda x: x[0])
        seq = [x for j, x in enumerate(seq) if j == 0 or x[1] != seq[j - 1][1]]
        for (ts, s) in seq:
            status.append((d["serial"], s, ts))
        state_at[d["serial"]] = seq
    return dict(cis=cis, devices=devices, status=status, premises=premises, state=state_at)


def online_at(seq, t, idle_online):
    last = None
    for ts, s in seq:
        if ts <= t:
            last = s
        else:
            break
    if last is None:
        return False
    return last == "ONLINE" or (last == "IDLE" and idle_online)


def cc_acks(th, evs):
    """Halvern's unreachable-device report for each 2026 event: every device of an enrolled premise outside the
    evaluation holdout that did not answer the 14:00 pre-cooling command."""
    r = rng("cc-acks")
    hold = set()
    act = [p for p in th["premises"]]
    idx = r.permutation(len(act))[:375]
    for i in idx:
        hold.add(act[int(i)]["premise"])
    out = []
    for ev in [e for e in evs if e["season"] == 2026]:
        t = utc(ev["date"], 14)
        post = ev["date"] >= P.HALVERN_IDLE_SWITCH
        for pm in th["premises"]:
            if pm["premise"] in hold or pm["enrolled"] > ev["date"] or (pm["unen"] and pm["unen"] <= ev["date"]):
                continue
            for d in pm["devs"]:
                if d["registered"] > t or (d["retired"] and d["retired"] <= t):
                    continue
                seq = th["state"].get(d["serial"])
                if seq is None:
                    continue
                if not online_at(seq, t, post) or r.random() > 0.996:
                    out.append((ev["date"], d["serial"], t + dt.timedelta(minutes=int(r.integers(15, 25)))))
    return out, hold


# ---------------------------------------------------------------- ask B: Brightwell's 2026 dispatch records

def batteries(evs):
    r = rng("hbn-records")
    a, b = P.HBN_FLEET[2026]
    reg = []
    pseen = set()
    n_prem = 3_330
    e_no = int(r.integers(410000, 412000))
    for i in range(n_prem):
        while True:
            p = premise_id(r)
            if p not in pseen:
                pseen.add(p)
                break
        meter = "4%07d" % int(r.integers(0, 10**7))
        two = r.random() < 0.031
        member = r.random() < 0.978
        u = r.random()
        if u < a / b:
            energised = dt.date(2021, 9, 1) + dt.timedelta(days=int(r.integers(0, 1700)))
            energised = min(energised, dt.date(2026, 5, 20))
        else:
            energised = dt.date(2026, 6, 1) + dt.timedelta(days=int(r.integers(0, 110)))
        for j in range(2 if two else 1):
            e_no += int(r.integers(3, 41))
            make = ["Halberd", "Lumenstor", "Pinyon"][int(r.choice(3, p=[0.55, 0.30, 0.15]))]
            reg.append(dict(premise=p, meter=meter, serial="%s-%s" % (make[:2].upper(), code(r, 8, DIGITS)),
                            make=make, usable_kwh=[13.5, 10.0, 16.0][["Halberd", "Lumenstor", "Pinyon"].index(make)],
                            enrolment=("HBN%06d" % e_no) if member else "", energised=energised))
    recs = []
    rid = int(r.integers(5_000_000, 5_100_000))
    for ev in [e for e in evs if e["season"] == 2026]:
        drop = P.HBN_DROP_EVENTS.get(ev["date"])
        start = utc(ev["date"], 16)
        stop = utc(ev["date"], 20)
        settle = ev["date"] + dt.timedelta(days=1)
        while settle.weekday() >= 5:
            settle += dt.timedelta(days=1)
        for bat in reg:
            if not bat["enrolment"] or bat["energised"] > ev["date"]:
                continue
            if r.random() > P.HBN_RESPONSE + 0.01:
                continue
            setting = P.HBN_SETTING_KW[2026]
            s0 = start + dt.timedelta(seconds=int(r.integers(4, 70)))
            e0 = stop - dt.timedelta(seconds=int(r.integers(0, 50)))
            cut = None
            if drop is not None and r.random() < (1 - drop) / P.HBN_RESPONSE:
                cut = start + dt.timedelta(minutes=int(r.integers(62, 120)))
                resume = r.random() < P.HBN_DROP_SPLIT
            elif r.random() < P.HBN_SPLIT_SHARE:
                cut = start + dt.timedelta(minutes=int(r.integers(35, 175)))
                resume = True
            if cut is None:
                rid += int(r.integers(1, 9))
                hours = (e0 - s0).total_seconds() / 3600
                recs.append(dict(rid=rid, enrolment=bat["enrolment"], serial=bat["serial"], start=s0, end=e0,
                                 kwh=round(setting * hours * float(r.uniform(0.985, 1.0)), 2), settled=settle))
                continue
            rid += int(r.integers(1, 9))
            h1 = (cut - s0).total_seconds() / 3600
            recs.append(dict(rid=rid, enrolment=bat["enrolment"], serial=bat["serial"], start=s0, end=cut,
                             kwh=round(setting * h1 * float(r.uniform(0.985, 1.0)), 2), settled=settle))
            if resume:
                back = cut + dt.timedelta(minutes=int(r.integers(14, 38)))
                if back < e0 - dt.timedelta(minutes=20):
                    rid += int(r.integers(1, 9))
                    h2 = (e0 - back).total_seconds() / 3600
                    recs.append(dict(rid=rid, enrolment=bat["enrolment"], serial=bat["serial"], start=back, end=e0,
                                     kwh=round(setting * h2 * float(r.uniform(0.985, 1.0)), 2), settled=settle))
    return reg, recs


# ---------------------------------------------------------------- ask C: Arroyo's 2026 nominations

BUSINESS = ["Medical Plaza", "Cold Storage", "Self Storage", "Office Park", "Distribution Center", "Community College",
            "Middle School", "Grocery", "Hotel", "Credit Union", "Fitness Club", "Church", "Auto Center",
            "Data Center", "Dental Group", "Bottling", "Printing", "Furniture Outlet", "Cinema", "Senior Living"]
PLACE = ["Desert Willow", "Saguaro Ridge", "Palo Verde", "Mesquite Bend", "Ironwood", "Copper Hill", "Agave",
         "Granite Dells", "Hohokam", "Silverbell", "Coyote Wash", "Quail Run", "Thunderbird", "Sunrise", "Gila",
         "Canyon Wren", "Juniper Mesa", "Cholla Vista", "Pinnacle Peak", "Rancho Vista"]


def nominations():
    r = rng("arroyo")
    sites = []
    refs = set()
    def ref():
        while True:
            x = "ADS-%05d" % int(r.integers(10000, 99999))
            if x not in refs:
                refs.add(x)
                return x
    meters = []
    for i in range(1_920):
        meters.append(dict(meter="4%07d" % int(r.integers(0, 10**7)), premise=premise_id(r),
                           rate=["GS-2", "GS-3", "LGS-1", "LGS-2", "TOU-C"][int(r.choice(5, p=[.38, .27, .15, .08, .12]))],
                           addr=address(r)[0]))
    pool = [m for m in meters if m["rate"] != "GS-2"]
    pick = r.permutation(len(pool))[:166]
    for j, k in enumerate(pick):
        m = pool[int(k)]
        nm = "%s %s" % (PLACE[int(r.integers(0, len(PLACE)))], BUSINESS[int(r.integers(0, len(BUSINESS)))])
        if r.random() < 0.18:
            nm = nm + [" LLC", " Inc", " #2", " (North)", " Bldg B"][int(r.integers(0, 5))]
        joined = 6 if j < 140 else int(r.choice([7, 8, 9], p=[0.4, 0.35, 0.25]))
        sites.append(dict(ref=ref(), name=nm, addr=m["addr"], meter=m["meter"], kw=float(round(r.uniform(22, 190), 0)),
                          joined=joined, outside=False))
    for j in range(27):
        nm = "%s %s" % (PLACE[int(r.integers(0, len(PLACE)))], BUSINESS[int(r.integers(0, len(BUSINESS)))])
        sites.append(dict(ref=ref(), name=nm, addr=address(r)[0], meter="1%08d" % int(r.integers(0, 10**8)),
                          kw=float(round(r.uniform(25, 160), 0)), joined=P.ARROYO_OUTSIDE_FROM, outside=True))
    rows = []
    owners = {6: 2, 7: 3, 8: 2, 9: 2}
    changed = {}
    for mth in (6, 7, 8, 9):
        live = [s for s in sites if s["joined"] <= mth and s["ref"] not in changed]
        cand = [s for s in live if not s["outside"]]
        moved = [cand[int(i)] for i in r.permutation(len(cand))[:owners[mth]]]
        for s in live:
            kw = s["kw"] * float(r.uniform(0.94, 1.06))
            sub = dt.datetime(2026, mth, 1) - dt.timedelta(days=int(r.integers(2, 16))) + _hours(r, 8, 18)
            rows.append(dict(month=mth, ref=s["ref"], name=s["name"], addr=s["addr"], meter=s["meter"],
                             kw=round(kw, 1), sub=sub, outside=s["outside"], dup=False, restated=False))
            if r.random() < 0.05:
                rows.append(dict(month=mth, ref=s["ref"], name=s["name"], addr=s["addr"], meter=s["meter"],
                                 kw=round(kw * float(r.uniform(0.85, 1.12)), 1), sub=sub + _hours(r, 20, 200),
                                 outside=s["outside"], dup=False, restated=True))
        for s in moved:
            new = dict(s)
            new["ref"] = ref()
            new["name"] = s["name"].replace(" LLC", "").replace(" Inc", "") + [" Holdings", " LLC", " Group"][int(r.integers(0, 3))]
            kw = s["kw"] * float(r.uniform(0.95, 1.05))
            sub = dt.datetime(2026, mth, 1) - dt.timedelta(days=int(r.integers(1, 5))) + _hours(r, 8, 18)
            rows.append(dict(month=mth, ref=new["ref"], name=new["name"], addr=s["addr"].upper(), meter=s["meter"],
                             kw=round(kw, 1), sub=sub, outside=False, dup=True, restated=False))
            changed[s["ref"]] = new
            sites.append(dict(new, joined=mth + 1))
    return meters, rows


# ---------------------------------------------------------------- the rest of the pack

def event_log(evs):
    r = rng("event-log")
    tk = int(r.integers(1100, 1300))
    out = []
    for ev in evs:
        notice = dt.datetime.combine(ev["date"] - dt.timedelta(days=1 if ev["date"].weekday() else 3), dt.time(13)) \
            + _hours(r, 0.3, 1.9)
        for p in P.PROGRAMS:
            tk += int(r.integers(1, 12))
            out.append(dict(ticket="SO-%s-%04d" % (str(ev["season"])[2:], tk % 10000), programme=P.NAME[p],
                            date=ev["date"], forecast=ev["forecast"], notice=notice + dt.timedelta(minutes=int(r.integers(0, 9)))))
    return out


def capacity_prices():
    r = rng("cap-prices")
    out = []
    for yr in (2025, 2026, 2027):
        for m in range(1, 13):
            summer = m in (6, 7, 8, 9)
            out.append((yr, m, round((9.8 if summer else 2.6) * (1 + 0.07 * (yr - 2025)) + r.normal(0, 0.35), 2),
                        round((6.1 if summer else 1.9) * (1 + 0.05 * (yr - 2025)) + r.normal(0, 0.3), 2)))
    return out


def satisfaction():
    r = rng("survey")
    out = []
    for p in P.PROGRAMS:
        n = {"CC": 612, "PTR": 1408, "BDP": 47, "HBN": 388}[p]
        base = {"CC": 7.6, "PTR": 7.9, "BDP": 7.2, "HBN": 8.4}[p]
        for q, adj in [("Overall satisfaction (0 to 10)", 0.0), ("Likely to stay enrolled next summer (0 to 10)", -0.3),
                       ("Incentive is worth taking part (0 to 10)", -0.6), ("Event notices arrive in good time (0 to 10)", 0.2)]:
            out.append((P.NAME[p], q, n - int(r.integers(0, 25)), round(base + adj + r.normal(0, 0.18), 1)))
    return out
