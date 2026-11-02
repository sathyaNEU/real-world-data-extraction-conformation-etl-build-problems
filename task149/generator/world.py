"""The Kilcarrow world from a fixed seed: the catchment's commuters, the operator's mobility panel, the census
place-of-work tables and the Ardnagree line's gate entries since 2018.

Everything the pack ships is drawn here; pack.py only writes it out. Times are naive local (Europe/Dublin)
until pack.py converts the panel's stays to UTC."""
import datetime as dt
import hashlib
import math

import numpy as np

import params as P

DAY = dt.timedelta(days=1)


def weekdays(a, b):
    d, out = a, []
    while d <= b:
        if d.weekday() < 5:
            out.append(d)
        d += DAY
    return out


def ordinary_2027():
    hol = set(P.BANK_HOLIDAYS_2027) | set(P.MIDTERM_2027)
    return [d for d in weekdays(P.PANEL_START, P.PANEL_END) if d not in hol]


def _pick(rng, pairs):
    keys = [k for k, _ in pairs]
    w = np.array([v for _, v in pairs], float)
    return keys[int(rng.choice(len(keys), p=w / w.sum()))]


def _t(d, minutes):
    return dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(minutes=float(minutes))


class Device:
    def __init__(self, did, home, kind, dest=None, regime=None):
        self.did, self.home, self.kind, self.dest, self.regime = did, home, kind, dest, regime
        self.work_cell = None
        self.acts = []          # (cell, start, end, tag)
        self.parent = False
        self.first = None
        self.last = None


def _hybrid_week(rng, k, dow_w):
    w = np.array(dow_w, float)
    idx = rng.choice(5, size=k, replace=False, p=w / w.sum())
    return set(int(i) for i in idx)


def _schedule(rng, dev, days):
    """Work shifts for one worker over the simulated days: list of (date, start_min, end_min, kind)."""
    reg = dev.regime
    out = []
    base_dep = float(np.clip(rng.normal(475, 22), 410, 560))   # minutes after midnight, leaving home
    travel = P.TRAVEL_MIN[dev.dest] + rng.integers(-6, 7)
    dev.travel = int(travel)
    if reg.startswith("hybrid"):
        dist = P.HYBRID_DAYS[reg]
        k0 = int(rng.choice(list(dist.keys()), p=np.array(list(dist.values())) / sum(dist.values())))
        weeks = {}
        for d in days:
            wk = d.isocalendar()[1]
            if wk not in weeks:
                k = int(np.clip(k0 + rng.choice([-1, 0, 0, 0, 0, 0, 1]), 1, 5))
                weeks[wk] = _hybrid_week(rng, k, P.HYBRID_DOW)
            if d.weekday() < 5 and d.weekday() in weeks[wk]:
                dep = base_dep + 20 + rng.normal(0, 9)
                out.append((d, dep + travel, dep + travel + rng.uniform(450, 560), "day"))
    elif reg == "fixed5":
        for d in days:
            if d.weekday() < 5:
                dep = base_dep + rng.normal(0, 8)
                out.append((d, dep + travel, dep + travel + rng.uniform(480, 545), "day"))
    elif reg == "parttime":
        pdays = set(int(i) for i in rng.choice(7, size=int(rng.choice([3, 4, 4, 5])), replace=False))
        start = float(rng.choice([540, 600, 720, 780]))
        for d in days:
            if d.weekday() in pdays:
                s = start + rng.normal(0, 6)
                out.append((d, s, s + rng.uniform(335, 450), "day"))
    elif reg == "roster4on4off":
        phase = int(rng.integers(0, 8))
        for i, d in enumerate(days):
            pos = (i + phase) % 8
            if pos in (0, 1):
                out.append((d, 420 + rng.normal(0, 4), 1140 + rng.normal(0, 6), "day"))
            elif pos in (2, 3):
                out.append((d, 1140 + rng.normal(0, 4), 1860 + rng.normal(0, 6), "night"))
    elif reg == "nurse3x12":
        nights = rng.random() < 0.35
        for wk_start in range(0, len(days), 7):
            block = days[wk_start:wk_start + 7]
            pick = rng.choice(len(block), size=min(3, len(block)), replace=False)
            for j in pick:
                d = block[int(j)]
                if nights and rng.random() < 0.5:
                    out.append((d, 1200 + rng.normal(0, 4), 1920 + rng.normal(0, 5), "night"))
                else:
                    out.append((d, 480 + rng.normal(0, 4), 1200 + rng.normal(0, 5), "day"))
    elif reg == "shift5of7":
        early = float(rng.choice([360, 480, 840, 1320], p=[0.35, 0.25, 0.30, 0.10]))
        for wk_start in range(0, len(days), 7):
            block = days[wk_start:wk_start + 7]
            pick = rng.choice(len(block), size=min(5, len(block)), replace=False)
            for j in pick:
                d = block[int(j)]
                s = early + rng.normal(0, 4)
                out.append((d, s, s + 480 + rng.normal(0, 5), "night" if early >= 1320 else "day"))
    sh = P.DEP_SHIFT.get(dev.dest, 0)
    if sh:
        out = [(d, a + sh, b + sh, k) for d, a, b, k in out]
    return out


def _absent(rng, dev, d):
    if d in P.BANK_HOLIDAYS_2027 and dev.regime in ("hybrid_a", "hybrid_b", "hybrid_c", "fixed5", "parttime"):
        return True
    p = 0.09
    if dev.parent and d in P.MIDTERM_2027:
        p += 0.35
    return rng.random() < p


def _errands(rng, dev, d, busy, n_max=2, long_ok=False):
    """Short stays away from home on a day: shops, school runs, visits."""
    acts = []
    pw = np.array([0.40, 0.42, 0.18][:n_max + 1])
    n = int(rng.choice(n_max + 1, p=pw / pw.sum()))
    for _ in range(n):
        start = rng.uniform(570, 1170)
        dur = rng.uniform(22, 140)
        if long_ok and rng.random() < 0.04:
            cell, dur = rng.choice(["KH301", "KH302"]), rng.uniform(70, 200)
        else:
            cell = str(rng.choice(P.LOCAL_CELLS))
        if cell == dev.home:
            continue
        a, b = start, start + dur
        if any(not (b + 25 <= s or a >= e + 25) for s, e in busy):
            continue
        busy.append((a, b))
        acts.append((cell, _t(d, a), _t(d, b), "errand"))
    return acts


def build_panel(rng):
    """Devices resident in the catchment and their activities over the panel weeks (local naive times)."""
    sim_days = [P.PANEL_START - 3 * DAY + i * DAY for i in range((P.PANEL_END - P.PANEL_START).days + 7)]
    devices = []
    n = 0
    home_cells = [c for c, _ in P.HOME_CELLS]
    home_w = np.array([w for _, w in P.HOME_CELLS])

    def new_dev(kind, dest=None, regime=None):
        nonlocal n
        n += 1
        home = home_cells[int(rng.choice(len(home_cells), p=home_w / home_w.sum()))]
        return Device(None, home, kind, dest, regime)

    for code, _name, _prov, cens, _share in P.DEST:
        m = int(rng.poisson(cens * P.SAMPLE))
        for _ in range(m):
            dev = new_dev("worker", code, _pick(rng, P.REGIMES[code]))
            cells = P.WORK_CELLS[code]
            cw = [c for c in cells if c != dev.home] or cells
            if code == "KW04" and "KU309" in cw and rng.random() < 0.04:
                dev.work_cell = "KH309"
            elif code == "KW03" and "KH309" in cw:
                dev.work_cell = "KH309" if rng.random() < 0.03 else str(rng.choice([c for c in cw if c != "KH309"]))
            else:
                dev.work_cell = str(rng.choice([c for c in cw if c != "KU309"] or cw))
            dev.parent = rng.random() < 0.30
            devices.append(dev)
    for _ in range(int(rng.poisson(880 * P.SAMPLE))):
        devices.append(new_dev("wfh"))
    for _ in range(14):
        dev = new_dev("nofixed")
        dev.sites = list(rng.choice(["CO111", "CO112", "RG10", "RG11", "BM701", "AP801", "XO001", "LS901", "KC103"],
                                    size=7, replace=False))
        devices.append(dev)
    for _ in range(int(rng.poisson(260 * P.SAMPLE))):
        dev = new_dev("outside")
        dev.work_cell = str(rng.choice(P.OUTSIDE_CELLS))
        dev.regime, dev.dest = "fixed5", "KX03"
        devices.append(dev)
    for _ in range(330):
        devices.append(new_dev("nonworker"))

    order = rng.permutation(len(devices))
    devices = [devices[i] for i in order]
    for i, dev in enumerate(devices):
        dev.did = hashlib.sha1(("rmp114-%d" % i).encode()).hexdigest()[:16]

    for dev in devices:
        if dev.kind in ("worker", "outside"):
            if dev.kind == "outside":
                dev.travel = 55 + int(rng.integers(0, 20))
                dev.dest_travel = dev.travel
            shifts = _schedule(rng, dev, sim_days) if dev.kind == "worker" else [
                (d, 470 + 55 + rng.normal(0, 8), 470 + 55 + rng.uniform(480, 540), "day")
                for d in sim_days if d.weekday() < 5]
            worked = set()
            for d, s, e, kind in shifts:
                if _absent(rng, dev, d):
                    continue
                dev.acts.append((dev.work_cell, _t(d, s), _t(d, e), "work"))
                worked.add(d)
                if s - dev.travel > 630 and rng.random() < 0.5:
                    a = rng.uniform(485, 530)
                    dev.acts.append((str(rng.choice(P.LOCAL_CELLS)), _t(d, a), _t(d, a + rng.uniform(24, 50)), "errand"))
            for d in sim_days:
                busy = []
                for c, s, e, tag in dev.acts:
                    if s.date() == d or e.date() == d:
                        a = (s - _t(d, 0)).total_seconds() / 60
                        b = (e - _t(d, 0)).total_seconds() / 60
                        busy.append((a - dev.travel - 10, b + dev.travel + 10))
                dev.acts += _errands(rng, dev, d, busy, n_max=2 if d not in worked else 1)
        elif dev.kind == "nofixed":
            for d in sim_days:
                if d.weekday() < 5 and rng.random() > 0.10:
                    s = 470 + rng.normal(0, 12)
                    dev.acts.append((str(rng.choice(dev.sites)), _t(d, s), _t(d, s + rng.uniform(380, 520)), "work"))
            dev.travel = 30
        else:
            dev.travel = 10
            for d in sim_days:
                dev.acts += _errands(rng, dev, d, [], n_max=2, long_ok=True)
        dev.acts.sort(key=lambda a: a[1])
        # remove overlaps (keep the earlier activity)
        clean, last_end = [], None
        for a in dev.acts:
            if last_end is not None and a[1] < last_end + dt.timedelta(minutes=12):
                continue
            clean.append(a)
            last_end = a[2]
        dev.acts = clean

    # SIM replacements: a device reissued under a new identifier part-way through the weeks.
    extra = []
    for dev in devices:
        if rng.random() < 0.04:
            cut = P.PANEL_START + int(rng.integers(12, 70)) * DAY
            twin = Device(hashlib.sha1(("rmp114-sim-%s" % dev.did).encode()).hexdigest()[:16], dev.home, dev.kind,
                          dev.dest, dev.regime)
            twin.work_cell, twin.travel, twin.parent = dev.work_cell, dev.travel, dev.parent
            cut_t = _t(cut, 0)
            twin.acts = [a for a in dev.acts if a[1] >= cut_t]
            dev.acts = [a for a in dev.acts if a[1] < cut_t]
            twin.split_from = dev.did
            extra.append(twin)
    devices += extra
    return devices


def home_stays(dev):
    """Fill the gaps between a device's activities with stays at its home cell."""
    out = []
    acts = dev.acts
    for i in range(len(acts) - 1):
        a, b = acts[i], acts[i + 1]
        tr_back = dev.travel if a[3] == "work" else 10
        tr_out = dev.travel if b[3] == "work" else 10
        s = a[2] + dt.timedelta(minutes=tr_back)
        e = b[1] - dt.timedelta(minutes=tr_out)
        if (e - s).total_seconds() >= 20 * 60:
            out.append((dev.home, s, e, "home"))
    return out


def census(rng):
    """Census 2022 place-of-work counts, catchment small area by workplace zone: final and provisional releases."""
    rows_final, rows_prov = [], []
    sa_codes = [c for c, _ in P.SMALL_AREAS]
    sa_w = np.array([w for _, w in P.SMALL_AREAS])
    cats = [(c, n, pn, tot) for c, n, pn, tot, _s in P.DEST] + [(c, n, n, tot) for c, n, tot in P.SPECIAL]
    for code, name, pname, tot in cats:
        split = rng.multinomial(tot, sa_w / sa_w.sum())
        for sa, k in zip(sa_codes, split):
            rows_final.append((sa, code, name, int(k)))
            miss = rng.uniform(0.010, 0.034)
            rows_prov.append((sa, code, pname, int(round(k * (1 - miss)))))
    return rows_final, rows_prov


def _era(station, d, ratio):
    """Share of the station's 2019 level carried on date d."""
    if d < dt.date(2019, 1, 1):
        return 0.975
    if d < dt.date(2020, 3, 13):
        return 1.0
    pts = [(dt.date(2020, 3, 13), 1.0), (dt.date(2020, 3, 27), 0.12), (dt.date(2020, 6, 1), 0.10),
           (dt.date(2020, 9, 7), 0.33), (dt.date(2020, 12, 31), 0.22), (dt.date(2021, 3, 1), 0.17),
           (dt.date(2021, 9, 6), 0.46), (dt.date(2022, 3, 1), 0.55), (dt.date(2022, 9, 5), 0.60 * ratio / 0.70),
           (dt.date(2023, 9, 4), ratio * 0.93), (dt.date(2024, 9, 2), ratio * 0.965), (dt.date(2025, 9, 1), ratio * 0.985),
           (dt.date(2026, 9, 7), ratio * 0.995), (dt.date(2027, 9, 6), ratio), (dt.date(2027, 12, 31), ratio)]
    for (a, va), (b, vb) in zip(pts, pts[1:]):
        if a <= d <= b:
            f = (d - a).days / max(1, (b - a).days)
            return va + (vb - va) * f
    return ratio


def gate_entries(rng):
    """Daily gate entries at each station code since 1 January 2018, to 30 November 2027."""
    rows = []
    hol = set(P.BANK_HOLIDAYS_2019 + P.BANK_HOLIDAYS_2027)
    extra_hol = {dt.date(y, m, dd) for y in range(2018, 2028) for (m, dd) in [(1, 1), (12, 25), (12, 26), (3, 17)]}
    hol |= extra_hol
    for y in range(2018, 2028):
        for m in (5, 6, 8):
            first = dt.date(y, m, 1)
            mon = first + dt.timedelta(days=(7 - first.weekday()) % 7)
            hol.add(mon)
        oct_last = dt.date(y, 10, 31)
        hol.add(oct_last - dt.timedelta(days=(oct_last.weekday()) % 7))
    midterms = set()
    for y in range(2018, 2028):
        oct_last = dt.date(y, 10, 31)
        mon = oct_last - dt.timedelta(days=oct_last.weekday())
        for i in range(5):
            midterms.add(mon + dt.timedelta(days=i))
    d0, d1 = dt.date(2018, 1, 1), dt.date(2027, 11, 30)
    for code, _name, opened, closed, base, ratio, office in P.STATIONS:
        d = max(d0, opened)
        end = min(d1, closed) if closed else d1
        while d <= end:
            wd = d.weekday()
            post = d >= dt.date(2022, 3, 1)
            if wd < 5:
                if office and post:
                    dow = [0.84, 1.11, 1.13, 1.07, 0.80][wd]
                elif post:
                    dow = [0.95, 1.03, 1.04, 1.02, 0.94][wd]
                else:
                    dow = [0.97, 1.03, 1.04, 1.02, 0.94][wd]
            else:
                dow = 0.42 if wd == 5 else 0.27
            season = {1: 0.95, 2: 0.99, 3: 1.0, 4: 0.97, 5: 0.99, 6: 0.97, 7: 0.86, 8: 0.84, 9: 1.0, 10: 1.0,
                      11: 1.0, 12: 0.90}[d.month]
            f = _era(code, d, ratio)
            if code == "LSG":
                wk = (d - opened).days
                if wk < 28:
                    f *= 0.72 + 0.28 * wk / 28.0
            if d in hol:
                f *= 0.33
            elif d in midterms:
                f *= 0.93
            mu = base * dow * season * f
            val = int(max(0, round(rng.normal(mu, 0.028 * mu + 6))))
            for parent, gid, a, b, lo, hi in P.GATELINES:
                if code == parent and a <= d <= b:
                    tmp = int(round(val * float(rng.uniform(lo, hi))))
                    rows.append((d, gid, tmp))
                    val -= tmp
            rows.append((d, code, val))
            d += DAY
    return rows


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    devices = build_panel(rng)
    cf, cp = census(np.random.default_rng(seed + 1))
    gates = gate_entries(np.random.default_rng(seed + P.GATE_SEED))
    return {"devices": devices, "census_final": cf, "census_prov": cp, "gates": gates}
