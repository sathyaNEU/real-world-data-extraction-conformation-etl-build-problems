"""The underground cable network and its failure history, 2012 to September 2026.

The history is scheduled, not drawn: each year, for each feeder and each section state (failures so far 0, 1, 2,
3 or more; the Quarry Hill 21 highway crossing kept apart), the number of cable-condition failures is the running
expected count under the network's failure rates, carried forward by error diffusion, so the totals follow the
rates exactly and no seed can move a feeder's history. The random draw only chooses which sections fail within a
scheduled count (weighted by their rates) and on which day.

Rates (per section year): a section with no failure fails at its insulation and age rate; after one failure at
three times that; after two at a third a year and after three or more at 45 per cent, whatever its cable. The
network splices a failed section in place; from 2019 it replaces a section at its second failure, and the
2019-2020 catch-up replaced every section that had already failed twice, except the Quarry Hill 21 sections in
the conduit under State Route 443, which crews splice in place."""
import datetime as dt
import math

import numpy as np

import world as W

YEARS = list(range(2012, 2027))
K1_MULT = 1.0
K1_INS = {"PILC": 1.0}        # a breached lead sheath lets water in: paper cable that has failed once keeps failing
K2_RATE = 0.33
K3_RATE = 0.7
HWY_K0 = 0.11
HWY_K1 = 0.22
HWY_START = 2016
K0_EPISODES = True           # the episodes below are first failures of original cable; a re-spliced section is not in them
PILC_REPL_FIRST = True       # paper cable is never spliced in place: a PILC fault is cut out and the section replaced
PILC_A, PILC_B, PILC_AGE0 = 0.0010, 0.0045, 55

# feeder: cohorts (insulation, first install year, last install year, sections, conduit share)
STOCK = {
    "HR12": [("PILC", 1955, 1964, 400, 0.85), ("TRXLPE", 2001, 2004, 40, 0.30)],
    "HR14": [("XLPE", 1981, 1988, 236, 0.20), ("EPR", 2004, 2008, 142, 0.25)],
    "ML03": [("XLPE", 1979, 1985, 212, 0.15), ("TRXLPE", 1999, 2002, 132, 0.20)],
    "ML07": [("XLPE", 1978, 1986, 226, 0.20), ("TRXLPE", 1996, 1999, 114, 0.25)],
    "QH21": [("XLPE", 1984, 1988, 160, 0.25), ("EPR", 2003, 2006, 114, 0.20)],
    "QH22": [("XLPE", 1980, 1985, 190, 0.25), ("TRXLPE", 1994, 1998, 58, 0.25)],
    "SP05": [("PILC", 1959, 1963, 12, 0.90), ("XLPE", 1979, 1984, 262, 0.15)],
    "SP09": [("EPR", 2005, 2009, 308, 0.30)],
}
HWY_SECTIONS = 33                # Quarry Hill 21's run in conduit under State Route 443 (XLPE, 1986)
LOOP_SECTIONS = 72               # Sutter Park 5's Kessler Avenue loop to the warehouse park (EPR, 2006-2010)
# the loop ran above its rating from the 2024 warehouse expansion until its second feed closed it on 15 September
# 2026; the history is scheduled to 19 September, and the last loop failure falls on 4 September
LOOP_ADD = {2024: 0.035, 2025: 0.12, 2026: 0.15}
LATERAL_SECTIONS = 24            # the Mill Lane 3 lateral moved to Mill Lane 7 on 14 June 2026 (TRXLPE, 2000)

# feeder-specific factors on the first-failure rate (Harrow Road 12's PILC, the oldest in the district, runs under
# the old trolley corridor)
FEEDER_K0 = {("HR12", "PILC"): 6.0, ("HR14", "XLPE"): 1.1, ("ML03", "XLPE"): 1.15, ("SP05", "PILC"): 1.0,
             ("SP05", "XLPE"): 1.2, ("QH21", "XLPE"): 0.4, ("QH21", "EPR"): 0.5, ("QH22", "XLPE"): 0.35}
# episodes of first failures with a local cause that has since passed: (multiplier by year, cause mix)
EPISODES = {
    # Mill Lane 7: splices and terminations made in the 2020 getaway and switchgear rebuild
    "ML07": ({2019: 1.6, 2020: 3.5, 2021: 6.8, 2022: 7.6, 2023: 6.0, 2024: 4.0, 2025: 2.0, 2026: 1.3},
             (0.30, 0.42, 0.28)),
    # Harrow Road 14: a batch of 200 A loadbreak elbows fitted 2017-2019, changed out in 2024
    "HR14": ({2020: 1.84, 2021: 3.8, 2022: 6.32, 2023: 5.76, 2024: 2.68}, (0.28, 0.20, 0.52)),
    # Mill Lane 3: insulation damaged by the 2021 fibre duct boring along Mill Lane, failing out
    "ML03": ({2022: 3.4, 2023: 5.32, 2024: 4.6, 2025: 2.2}, (0.74, 0.18, 0.08)),
    # Sutter Park 5: the warehouse load added in 2021 ran its old cable at full rating until the 2025 tie
    "SP05": ({2021: 1.5, 2022: 2.4, 2023: 2.3, 2024: 1.8, 2025: 1.25}, (0.62, 0.26, 0.12)),
}
ML07_BURST = EPISODES["ML07"][0]
# the 2022 and 2023 summers ran the district's cable at its highest loadings on record
HOT_SUMMERS = {2022: 1.15, 2023: 1.1}
DITHER_FEEDERS = ("SP09", "QH22")
DITHER = {}


def base_rate(ins, age):
    a = max(age, 0)
    if ins == "PILC":
        return PILC_A + PILC_B * max(a - PILC_AGE0, 0)
    if ins == "XLPE":
        return 0.0050 + 0.00050 * max(a - 18, 0)
    if ins == "TRXLPE":
        return 0.0028 + 0.00010 * a
    return 0.0022 + 0.00008 * a       # EPR


class Section:
    __slots__ = ("sid", "feeder", "ins", "installed", "length", "method", "hwy", "lateral", "fails", "retired",
                 "pred", "repl_reason", "loop")

    def __init__(self, sid, feeder, ins, installed, length, method, hwy=False, lateral=False, pred=None):
        self.sid, self.feeder, self.ins, self.installed, self.length, self.method = sid, feeder, ins, installed, length, method
        self.hwy, self.lateral, self.pred = hwy, lateral, pred
        self.loop = False
        self.fails = []          # (date, cause) of cable-condition failures
        self.retired = None
        self.repl_reason = None

    @property
    def k(self):
        return len(self.fails)

    def in_service(self, d):
        return self.installed <= d and (self.retired is None or self.retired > d)


def _days(y):
    return 365 if y % 4 else 366


def _rand_date(rng, lo, hi):
    n = (hi - lo).days
    return lo + dt.timedelta(days=int(rng.integers(0, n + 1)))


def build(seed=W.SEED):
    # one random stream per feeder and per kind of draw, so tuning one feeder's rates never reshuffles another's
    streams = {}

    def rs(*key):
        if key not in streams:
            code = [seed] + [sum((i + 1) * ord(c) for i, c in enumerate(str(k))) for k in key]
            streams[key] = np.random.default_rng(code)
        return streams[key]
    id_rng = rs("ids")
    DITHER.clear()
    for f in DITHER_FEEDERS:
        u = rs("dither", f).uniform(-0.48, 0.48, size=len(YEARS))
        DITHER[f] = {y: float(x) for y, x in zip(YEARS, u)}
    secs = []
    next_id = [104117]

    def new_id(step_lo=1, step_hi=4):
        next_id[0] += int(id_rng.integers(step_lo, step_hi + 1))
        return "UG%07d" % next_id[0]

    for f in W.FEEDERS:
        rng = rs("stock", f)
        for ins, y0, y1, n, conduit in STOCK[f]:
            for _ in range(n):
                yr = int(rng.integers(y0, y1 + 1))
                d = dt.date(yr, int(rng.integers(3, 12)), int(rng.integers(1, 29)))
                length = int(round(float(np.exp(rng.normal(5.75, 0.55))) / 5) * 5)
                length = min(max(length, 60), 2400)
                method = "CONDUIT" if rng.random() < conduit else "DIRECT BURIED"
                secs.append(Section(None, f, ins, d, length, method))
        if f == "QH21":
            rng = rs("stock", "hwy")
            for _ in range(HWY_SECTIONS):
                d = dt.date(1986, int(rng.integers(5, 9)), int(rng.integers(1, 29)))
                length = int(round(float(rng.uniform(180, 420)) / 5) * 5)
                secs.append(Section(None, f, "XLPE", d, length, "CONDUIT", hwy=True))
        if f == "SP05":
            rng = rs("stock", "loop")
            for _ in range(LOOP_SECTIONS):
                d = dt.date(int(rng.integers(2006, 2011)), int(rng.integers(3, 12)), int(rng.integers(1, 29)))
                length = int(round(float(np.exp(rng.normal(5.7, 0.45))) / 5) * 5)
                x = Section(None, f, "EPR", d, max(length, 60), "CONDUIT" if rng.random() < 0.4 else "DIRECT BURIED")
                x.loop = True
                secs.append(x)
        if f == "ML03":
            rng = rs("stock", "lateral")
            for _ in range(LATERAL_SECTIONS):
                d = dt.date(2000, int(rng.integers(4, 10)), int(rng.integers(1, 29)))
                length = int(round(float(np.exp(rng.normal(5.6, 0.4))) / 5) * 5)
                secs.append(Section(None, f, "TRXLPE", d, length, "DIRECT BURIED", lateral=True))
    # GIS facility ids were allocated at the 2009 data conversion, feeder by feeder, in network order
    order = sorted(range(len(secs)), key=lambda i: (W.FEEDERS.index(secs[i].feeder), secs[i].lateral, secs[i].hwy,
                                                   secs[i].installed, i))
    for i in order:
        secs[i].sid = new_id()
    next_id[0] = 612040                         # the post-2019 capital block
    acc = {}                                    # error diffusion accumulators
    done = {}

    def schedule(key, expected, y):
        acc[key] = acc.get(key, 0.0) + expected
        # the two quietest feeders fail about once a year; their years scatter around that instead of landing one
        # a year (a fixed offset on the rounding point each year, so the totals still follow the rates)
        off = DITHER[key[0]][y] if key[0] in DITHER and key[1:] == ("N", 0) else 0.0
        n = int(math.floor(acc[key] + 0.5 + off)) - done.get(key, 0)
        n = max(n, 0)
        done[key] = done.get(key, 0) + n
        return n

    def rate(s, y):
        age = y - s.installed.year
        if s.hwy:
            return [HWY_K0 if y >= HWY_START else 0.010, HWY_K1, K2_RATE, K3_RATE][min(s.k, 3)]
        if s.k >= 3:
            return K3_RATE
        if s.k == 2:
            return K2_RATE
        r = base_rate(s.ins, age) * FEEDER_K0.get((s.feeder, s.ins), 1.0)
        if s.loop:
            r += LOOP_ADD.get(y, 0.0)
        if s.feeder in EPISODES and not s.lateral and (s.k == 0 or not K0_EPISODES):
            r *= EPISODES[s.feeder][0].get(y, 1.0)
        r *= HOT_SUMMERS.get(y, 1.0)
        return r * (K1_INS.get(s.ins, K1_MULT) if s.k == 1 else 1.0)

    def replace(s, when, reason, ins=None):
        s.retired = when
        s.repl_reason = reason
        rng = rs("replace", s.feeder, s.hwy)
        length = s.length + int(rng.integers(-2, 3)) * 5
        if reason == "PROGRAM":
            # the program pulled new cable in new conduit along the street, off the old trolley-corridor alignment
            length = int(round(s.length * float(rs("program_route").uniform(1.03, 1.16)) / 5) * 5)
        n = Section(new_id(1, 9), s.feeder, ins or ("EPR" if s.feeder in ("HR12", "SP05") else "TRXLPE"), when,
                    max(length, 60), s.method, lateral=s.lateral, pred=s.sid)
        n.loop = s.loop
        secs.append(n)
        return n

    for y in YEARS:
        y_lo = dt.date(y, 1, 1)
        y_hi = dt.date(y, 12, 31) if y < 2026 else dt.date(2026, 9, 19)
        frac_year = ((y_hi - y_lo).days + 1) / _days(y)
        # catch-up replacements of twice-failed sections (2019-2020), Quarry Hill 21's highway run excepted
        if y == 2019:
            twice = sorted([s for s in secs if s.retired is None and s.k >= 2 and not s.hwy], key=lambda s: s.sid)
            for s in twice:
                when = _rand_date(rs("catchup", s.feeder), W.CATCHUP[0], W.CATCHUP[1])
                replace(s, when, "CATCHUP")
        # Harrow Road 12's PILC replacement program, 2025
        if y == 2025:
            for s in sorted([s for s in secs if s.feeder == "HR12" and s.ins == "PILC" and s.retired is None],
                            key=lambda s: s.sid):
                replace(s, _rand_date(rs("program"), dt.date(2025, 3, 31), dt.date(2025, 11, 14)), "PROGRAM", ins="EPR")
        groups = {}
        for s in secs:
            lo = max(s.installed, y_lo)
            hi = min(s.retired - dt.timedelta(days=1) if s.retired else y_hi, y_hi)
            if hi < lo:
                continue
            frac = ((hi - lo).days + 1) / _days(y)
            key = (s.feeder, "H" if s.hwy else "N", min(s.k, 3))
            groups.setdefault(key, []).append((s, frac, lo, hi))
        for key in sorted(groups):
            items = groups[key]
            w = np.array([rate(s, y) * fr for s, fr, _, _ in items])
            n = schedule(key, float(w.sum()), y)
            n = min(n, len(items))
            if n == 0:
                continue
            p = w / w.sum()
            rng = rs("fail", key[0], key[1])
            pick = rng.choice(len(items), size=n, replace=False, p=p)
            for i in sorted(pick):
                s, fr, lo, hi = items[i]
                d = _rand_date(rng, lo, hi)
                if s.fails and d <= s.fails[-1][0]:
                    continue
                kk = s.k
                ep = EPISODES.get(s.feeder)
                if kk == 0 and ep and not s.lateral and ep[0].get(y, 1.0) >= 1.5:
                    cause = rng.choice(["INS", "SPL", "TRM"], p=list(ep[1]))
                elif kk == 0:
                    cause = rng.choice(["INS", "SPL", "TRM"], p=[0.46, 0.34, 0.20])
                else:
                    cause = rng.choice(["INS", "SPL", "TRM"], p=[0.72, 0.22, 0.06])
                s.fails.append((d, str(cause)))
        # replacement at the second failure from 2019 (not on the highway run); paper cable at its first
        if y >= 2019 or PILC_REPL_FIRST:
            for s in sorted([s for s in secs if s.retired is None and not s.hwy and
                             ((s.k >= 2 and y >= 2019) or (PILC_REPL_FIRST and s.ins == "PILC" and s.k >= 1))],
                            key=lambda s: s.sid):
                last = s.fails[-1][0]
                rng = rs("lag", s.feeder)
                lag = int(rng.integers(12, 75))
                when = last + dt.timedelta(days=lag)
                if when > W.CUT:
                    when = W.CUT - dt.timedelta(days=int(rng.integers(1, 5)))
                    if when <= last:
                        when = last + dt.timedelta(days=1)
                replace(s, when, "SECOND")
    return secs, acc


def truth_2027(secs, ml07_2027=1.1):
    """The expected 2027 failures under the rates that generated the record (no hot summer; Mill Lane 7's run of
    first failures all but over)."""
    out = {f: 0.0 for f in W.FEEDERS}
    for s in secs:
        if not s.in_service(W.CUT):
            continue
        f = "ML07" if s.lateral else s.feeder
        if s.hwy:
            r = [HWY_K0, HWY_K1, K2_RATE, K3_RATE][min(s.k, 3)]
        elif s.k >= 3:
            r = K3_RATE
        elif s.k == 2:
            r = K2_RATE
        else:
            r = base_rate(s.ins, 2027 - s.installed.year) * FEEDER_K0.get((s.feeder, s.ins), 1.0)
            if s.feeder == "ML07" and not s.lateral:
                r *= ml07_2027
            r *= K1_INS.get(s.ins, K1_MULT) if s.k == 1 else 1.0
        out[f] += r
    return out


def summary(secs):
    out = {}
    for f in W.FEEDERS:
        live = [s for s in secs if s.feeder == f and s.in_service(W.CUT)]
        ks = [min(s.k, 3) for s in live]
        out[f] = {"in_service": len(live), "k": [ks.count(i) for i in range(4)]}
    return out


TPD_RATE = {"HR12": 0.3, "HR14": 1.3, "ML03": 1.4, "ML07": 0.4, "QH21": 0.3, "QH22": 0.4, "SP05": 0.3, "SP09": 0.5}
OTH_RATE = {"HR12": 0.5, "HR14": 0.4, "ML03": 0.5, "ML07": 0.4, "QH21": 0.3, "QH22": 0.4, "SP05": 0.5, "SP09": 0.3}


def other_events(secs, seed=W.SEED + 7):
    """Work orders on cable sections that are not failures of the cable itself: dig-ins by others (TPD) and other
    causes (OTH), each on a section in service on the day, scheduled by error diffusion like the failures."""
    rng = np.random.default_rng(seed)
    out = []
    for code, table in (("TPD", TPD_RATE), ("OTH", OTH_RATE)):
        for f in W.FEEDERS:
            acc = 0.0
            done = 0
            for y in YEARS:
                y_lo = dt.date(y, 1, 1)
                y_hi = dt.date(y, 12, 31) if y < 2026 else dt.date(2026, 9, 19)
                acc += table[f] * ((y_hi - y_lo).days + 1) / _days(y)
                n = int(math.floor(acc + 0.5)) - done
                done += n
                for _ in range(n):
                    for _try in range(50):
                        d = _rand_date(rng, y_lo, y_hi)
                        live = [s for s in secs if s.feeder == f and s.in_service(d)]
                        s = live[int(rng.integers(len(live)))]
                        if all(abs((d - x).days) > 3 for x, _ in s.fails):
                            out.append((s, d, code))
                            break
    out.sort(key=lambda e: (e[1], e[0].sid))
    return out
