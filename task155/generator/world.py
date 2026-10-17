"""The world behind task155: Kellaway's eight Victorian stores, their casuals and permanent staff, what each casual
can work, the rosters the stores publish, the call-ins those rosters and their absences raise, and the call-in
module's offer cascade with each casual's answer.

Inside the engine every time is minutes from 00:00 on Friday 29 August 2025, store time (the wall clock in
Melbourne and Ballarat); records.py converts to UTC where the workforce system writes UTC. Every random stream is
drawn from numpy.random.SeedSequence([SEED, k]) with a fixed stream number k per component (DESIGN_NOTE, World seed).
"""
from __future__ import annotations

import collections
import datetime as dt
import heapq
import math

import numpy as np

SEED = 155
D0 = dt.date(2025, 8, 29)                      # a Friday: roster weeks run Friday to Thursday
HIST_END = dt.date(2026, 11, 12)               # last shift date in the extract
AS_OF = dt.date(2026, 11, 13)
PEAK25 = (dt.date(2025, 11, 28), dt.date(2025, 12, 24))
PEAK26 = (dt.date(2026, 11, 27), dt.date(2026, 12, 24))
CLOSED = {dt.date(2025, 12, 25), dt.date(2026, 4, 3), dt.date(2026, 12, 25)}
ANZAC = dt.date(2026, 4, 25)                   # restricted trading until 13:00
KWS_ROSTERS_FROM = dt.date(2026, 2, 27)        # rosters built in the workforce system from this roster week
LEAVE_FREEZE = [(dt.date(2025, 11, 14), dt.date(2026, 1, 9)), (dt.date(2026, 11, 13), dt.date(2027, 1, 8))]
PUB25 = dt.datetime(2025, 11, 13, 10, 0)       # the 2025 Christmas rosters, published together
PUB26 = dt.datetime(2026, 11, 12, 10, 0)       # the 2026 Christmas rosters
POST26 = dt.datetime(2026, 11, 16, 9, 0)       # 2026 open shifts post to call-in after the crew is placed
CREW_STORE_25 = "W2"

# Victorian government school terms and the universities' teaching and exam periods
TERMS = [(dt.date(2025, 7, 14), dt.date(2025, 9, 19)), (dt.date(2025, 10, 6), dt.date(2025, 12, 19)),
         (dt.date(2026, 1, 27), dt.date(2026, 4, 2)), (dt.date(2026, 4, 20), dt.date(2026, 6, 26)),
         (dt.date(2026, 7, 13), dt.date(2026, 9, 18)), (dt.date(2026, 10, 5), dt.date(2026, 12, 18))]
SEMS = [(dt.date(2025, 7, 28), dt.date(2025, 11, 14)), (dt.date(2026, 3, 2), dt.date(2026, 6, 19)),
        (dt.date(2026, 7, 27), dt.date(2026, 11, 5))]


def stream(k):
    return np.random.default_rng(np.random.SeedSequence([SEED, k]))


def dnum(d):
    return (d - D0).days


def ddate(n):
    return D0 + dt.timedelta(days=n)


def tmin(t):
    """minutes from D0 00:00 for a naive store-time datetime"""
    return dnum(t.date()) * 1440 + t.hour * 60 + t.minute


def in_ranges(d, ranges):
    return any(a <= d <= b for a, b in ranges)


def in_peak(d, peak):
    return peak[0] <= d <= peak[1]


def is_peak(d):
    return in_peak(d, PEAK25) or in_peak(d, PEAK26)


def hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def paid(span):
    """paid minutes of a shift of `span` minutes: an unpaid 30-minute meal break on a shift over five hours"""
    return span - (30 if span > 300 else 0)


def daytype(d):
    wd = d.weekday()
    return "sat" if wd == 5 else ("sun" if wd == 6 else "wk")


# --------------------------------------------------------------------------- behaviour (the truth)
B = dict(ext=4.8, len=0.22, split=-2.0, cl=-0.85, load=-0.07, load_free=10.0, late=-0.35, early=-0.45, sun=0.25,
         sn=-0.45, re=-2.1, dec=-1.1)
TYPE_ALPHA = {"school": -2.05, "uni": -1.70, "parent": -1.75, "flex": -1.85}


def accept_logit(alpha, ext, len_h, split, cl, hours_wk, late, early, sun, short_notice, reoffer, dec):
    """the casual's propensity to take this shift: their own propensity plus additive terms, the largest being that
    the shift carries on from their own shift at the store, so no separate trip to work is needed"""
    z = alpha + (B["ext"] if ext else 0.0) + (B["split"] if split else 0.0) + (B["cl"] if cl else 0.0)
    z += B["len"] * (len_h - 5) + B["load"] * max(0.0, hours_wk - B["load_free"])
    z += (B["late"] if late else 0) + (B["early"] if early else 0) + (B["sun"] if sun else 0)
    z += (B["sn"] if short_notice else 0) + (B["re"] if reoffer else 0) + (B["dec"] if dec else 0)
    return z


def sigmoid(z):
    return 1.0 / (1.0 + math.exp(-z))


# --------------------------------------------------------------------------- stores, shifts, templates
STORE_NAMES = {"W1": "Altona", "W2": "Werribee", "W3": "Sunshine", "W4": "Williamstown", "E1": "Box Hill",
               "E2": "Camberwell", "E3": "Ringwood", "RG": "Ballarat"}
BANK = {
    "E06": ("06:00", "10:00"), "D06": ("06:00", "14:00"), "D08": ("08:00", "16:00"), "S10": ("10:00", "14:00"),
    "M10": ("10:00", "16:00"), "A12": ("12:00", "18:00"), "A14": ("14:00", "18:00"), "P16": ("16:00", "20:00"),
    "L16": ("16:00", "22:00"), "V18": ("18:00", "22:00"), "W08": ("08:00", "14:00"), "W14": ("14:00", "20:00"),
    "N18": ("18:00", "24:00"), "C10": ("10:00", "16:00"),
}
BASE = {
    "wk": {"D06": 3, "E06": 2, "D08": 5, "S10": 4, "M10": 4, "P16": 7, "L16": 4, "V18": 2},
    "sat": {"E06": 2, "D06": 3, "W08": 5, "D08": 4, "A12": 6, "L16": 6},
    "sun": {"E06": 2, "W08": 4, "D08": 4, "A12": 5, "L16": 5},
}
ALLYEAR = {"E1": {"wk": {"A14": 6}}}
PERM_CODES = {"wk": ["D06", "D08", "E06", "M10", "S10"], "sat": ["D06", "D08", "E06"], "sun": ["D08", "E06"]}
PERM_FRAC = {"wk": 0.42, "sat": 0.20, "sun": 0.14}
PEAK_BASE = 1.10
TYPES = ("school", "uni", "parent", "flex")

# mix: (school, uni, parent, flex) shares in August 2025; hires: (date, type, n) joining later;
# adds: Christmas positions rostered with the base; ups: Christmas positions listed open.
STORES = {
    "W1": dict(cluster="W", size=1.85, mix=(0.46, 0.24, 0.18, 0.12), hires=[(dt.date(2026, 2, 23), "uni", 18)],
               adds26={"wk": {"A14": 12}, "sat": {"A12": 6}, "sun": {"A12": 5}},
               up26={"wk": {"V18": 12, "P16": 4, "S10": 2}, "sat": {"V18": 6, "L16": 4}, "sun": {"V18": 5, "L16": 3}},
               up25={"wk": {"P16": 10, "S10": 4}, "sat": {"L16": 8}, "sun": {"L16": 6}}),
    "W2": dict(cluster="W", size=1.70, mix=(0.62, 0.10, 0.06, 0.22), hires=[(dt.date(2026, 2, 16), "uni", 64)],
               hire_alpha=-1.0, store_alpha=-0.5, hire_days=5, hire_target=(21, 27),
               adds26={"wk": {"W08": 20, "A14": 24}, "sat": {"W08": 18, "A12": 20}, "sun": {"W08": 17, "A12": 19}},
               up26={"wk": {"A14": 12, "N18": 12}, "sat": {"A14": 10, "N18": 11}, "sun": {"A14": 10, "N18": 11}},
               up25={"wk": {"P16": 12, "L16": 6}, "sat": {"L16": 10}, "sun": {"L16": 8}}),
    "W3": dict(cluster="W", size=2.00, mix=(0.40, 0.20, 0.22, 0.18), hires=[],
               adds26={}, up26={"wk": {"D08": 3, "P16": 5}, "sat": {"D08": 6}, "sun": {"D08": 5}},
               up25={"wk": {"D08": 5, "P16": 6}, "sat": {"D08": 8}, "sun": {"D08": 6}}),
    "W4": dict(cluster="W", size=1.70, mix=(0.50, 0.16, 0.20, 0.14), hires=[],
               adds26={}, up26={"wk": {"E06": 3, "P16": 3}, "sat": {"E06": 4}, "sun": {"E06": 3}},
               up25={"wk": {"E06": 6, "P16": 6}, "sat": {"E06": 6}, "sun": {"E06": 4}}),
    "E1": dict(cluster="E", size=1.90, mix=(0.36, 0.40, 0.12, 0.12), hires=[(dt.date(2026, 2, 23), "uni", 18)],
               adds26={"wk": {"A14": 26}, "sat": {"A12": 10}, "sun": {"A12": 8}},
               up26={"wk": {"V18": 24, "S10": 3}, "sat": {"V18": 10, "L16": 4}, "sun": {"V18": 8, "L16": 3}},
               up25={"wk": {"P16": 14, "S10": 4}, "sat": {"L16": 10}, "sun": {"L16": 8}}),
    "E2": dict(cluster="E", size=1.80, mix=(0.66, 0.04, 0.24, 0.06), hires=[(dt.date(2026, 8, 3), "parent", 8)],
               type_alpha={"school": 0.5},
               picking_from=dt.date(2026, 8, 3), picking={"wk": {"M10": 5, "S10": 3}},
               adds26={}, up26={"wk": {"M10": 5, "S10": 3}, "sat": {"W08": 4}, "sun": {"W08": 3}},
               up25={"wk": {"P16": 12, "L16": 4}, "sat": {"L16": 10}, "sun": {"L16": 8}}),
    "E3": dict(cluster="E", size=1.85, mix=(0.40, 0.28, 0.18, 0.14), hires=[],
               adds26={}, up26={"wk": {"P16": 6, "L16": 3}, "sat": {"W08": 8}, "sun": {"W08": 7}},
               up25={"wk": {"P16": 8, "L16": 4}, "sat": {"W08": 10}, "sun": {"W08": 10}}),
    "RG": dict(cluster=None, size=1.70, mix=(0.50, 0.12, 0.22, 0.16),
               hires=[(dt.date(2026, 2, 9), "school", 9), (dt.date(2026, 2, 9), "flex", 3)],
               adds26={}, up26={"wk": {"P16": 2, "S10": 2, "L16": 2}, "sat": {"L16": 3}, "sun": {"L16": 2}},
               up25={"wk": {"P16": 8, "S10": 6, "L16": 4}, "sat": {"L16": 10}, "sun": {"L16": 6}}),
}
ORDER = list(STORES)
SLACK = {"RG": 1.25, "E2": 1.32}
# school students leaving a store's books over the summer: (type, share, from, to)
LEAVE = {"W2": ("school", 0.45, dt.date(2025, 11, 20), dt.date(2026, 2, 6))}
TGT = {"school": (8, 14, 1.10, 1.35), "uni": (14, 24, 1.45, 1.90), "parent": (12, 20, 1.0, 1.08), "flex": (16, 28, 1.0, 1.12)}
OPT_IN = {"school": 0.10, "uni": 0.15, "parent": 0.25, "flex": 0.40}
# store moves during 2026: (from, to, n, first, last, type after the move or None)
MOVES = [("RG", "W1", 3, dt.date(2026, 2, 6), dt.date(2026, 2, 27), "uni"),
         ("RG", "W3", 3, dt.date(2026, 2, 6), dt.date(2026, 2, 27), "uni"),
         ("RG", "E1", 3, dt.date(2026, 2, 6), dt.date(2026, 2, 27), "uni"),
         ("RG", "E3", 2, dt.date(2026, 2, 6), dt.date(2026, 2, 27), "uni"),
         ("W1", "W4", 3, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("W4", "W1", 3, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("W3", "W2", 3, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("W2", "W3", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("W1", "W3", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("W4", "W2", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("E1", "E3", 3, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("E3", "E1", 3, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("E2", "E1", 3, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("E1", "E2", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("E3", "E2", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("W3", "E1", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("E3", "W1", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("W2", "E2", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None),
         ("E2", "W4", 2, dt.date(2026, 1, 9), dt.date(2026, 9, 25), None)]
N_REHIRES = 16
P_ABSENT = 0.045            # a rostered shift lost to a sickness or carer's absence
P_ABSENT_PEAK = 0.05
P_DROP = 0.035              # an accepted call-in later dropped by the casual
TRAVEL_MIN = 60             # minutes KWS leaves a casual to get between stores
P_DUP_REPORT = 0.12         # an absence reported twice (the app and a call to the store), each raising a call-in
P_LATE_LEAVE = 0.15         # a permanent's leave approved after the roster for those days was published


def positions_for(store, d, christmas):
    """(start, end, pri, code): pri 0 rostered, pri 1 Christmas uplift listed open. `christmas` is 25 or 26 or None."""
    if d in CLOSED:
        return []
    cfg = STORES[store]
    dtp = daytype(d)
    out = []
    for code, n in BASE[dtp].items():
        k = int(round(n * cfg["size"] * (PEAK_BASE if christmas else 1.0)))
        out += [(hm(BANK[code][0]), hm(BANK[code][1]), 0, code)] * k
    for code, n in ALLYEAR.get(store, {}).get(dtp, {}).items():
        out += [(hm(BANK[code][0]), hm(BANK[code][1]), 0, code)] * n
    if cfg.get("picking_from") and d >= cfg["picking_from"]:
        for code, n in cfg["picking"].get(dtp, {}).items():
            out += [(hm(BANK[code][0]), hm(BANK[code][1]), 0, code)] * n
    if christmas == 26:
        for code, n in cfg["adds26"].get(dtp, {}).items():
            out += [(hm(BANK[code][0]), hm(BANK[code][1]), 0, code)] * n
    if christmas:
        ups = cfg["up25"] if christmas == 25 else cfg["up26"]
        for code, n in ups.get(dtp, {}).items():
            out += [(hm(BANK[code][0]), hm(BANK[code][1]), 1, code)] * n
    if d == ANZAC:
        out = [p for p in out if p[0] >= 13 * 60]
    return out


def week_hours_needed(store):
    tot = 0.0
    cfg = STORES[store]
    for dtp, k in (("wk", 5), ("sat", 1), ("sun", 1)):
        pos = []
        for code, n in BASE[dtp].items():
            pos += [code] * int(round(n * cfg["size"]))
        nperm = int(round(len(pos) * PERM_FRAC[dtp]))
        hrs = [paid(hm(BANK[c][1]) - hm(BANK[c][0])) / 60 for c in pos]
        perm = sorted([h for c, h in zip(pos, hrs) if c in PERM_CODES[dtp]], reverse=True)[:nperm]
        tot += k * (sum(hrs) - sum(perm))
    return tot


# --------------------------------------------------------------------------- people
class Casual:
    __slots__ = ("idx", "store0", "typ0", "alpha", "target", "target_peak", "free_days", "off_days", "opt_in",
                 "start", "end", "moves", "gap", "hired")

    def home(self, d):
        h = self.store0
        for when, to, _ in self.moves:
            if d >= when:
                h = to
        return h

    def typ(self, d):
        t = self.typ0
        for when, _, nt in self.moves:
            if d >= when and nt:
                t = nt
        return t

    def active(self, d):
        if not (self.start <= d <= self.end):
            return False
        return not (self.gap and self.gap[0] < d < self.gap[1])


class Perm:
    __slots__ = ("idx", "store", "emp_type", "leave")


def make_people(rng):
    casuals = []
    end_far = dt.date(2027, 6, 30)
    idx = 0
    for store, cfg in STORES.items():
        need = week_hours_needed(store)
        mids = {t: (TGT[t][0] + TGT[t][1]) / 2 for t in TGT}
        avg_t = sum(cfg["mix"][i] * mids[t] for i, t in enumerate(TYPES))
        n = int(math.ceil(need * SLACK.get(store, 1.22) / avg_t))
        for i, t in enumerate(TYPES):
            for _ in range(int(round(n * cfg["mix"][i]))):
                c = _casual(rng, idx, store, t, D0 - dt.timedelta(days=int(rng.exponential(420 if t != "school" else 260))), end_far)
                lv = LEAVE.get(store)
                if lv and lv[0] == t and rng.random() < lv[1]:
                    c.end = lv[2] + dt.timedelta(days=int(rng.integers(0, (lv[3] - lv[2]).days)))
                c.alpha += cfg.get("store_alpha", 0.0) + cfg.get("type_alpha", {}).get(t, 0.0)
                casuals.append(c)
                idx += 1
        for hd, t, k in cfg["hires"]:
            for _ in range(k):
                c = _casual(rng, idx, store, t, hd + dt.timedelta(days=int(rng.integers(0, 21))), end_far)
                c.alpha += cfg.get("hire_alpha", 0.0) + cfg.get("store_alpha", 0.0)
                c.hired = True
                if cfg.get("hire_days"):
                    c.off_days = set(rng.choice(7, size=7 - cfg["hire_days"], replace=False).tolist())
                    c.target = rng.uniform(*cfg["hire_target"])
                    c.target_peak = c.target * rng.uniform(1.05, 1.2)
                casuals.append(c)
                idx += 1
    # store moves: Ballarat school leavers to Melbourne universities, and moves between stores
    for frm, to, k, first, last, nt in MOVES:
        pool = [c for c in casuals if c.store0 == frm and not c.moves and c.start < first and c.end > last
                and (c.typ0 == "school" if nt else c.typ0 in ("uni", "flex", "parent"))]
        pick = rng.choice(len(pool), size=k, replace=False)
        span = (last - first).days // 7
        for j in sorted(pick.tolist()):
            c = pool[j]
            when = first + dt.timedelta(days=7 * int(rng.integers(0, span + 1)))
            c.moves = [(when, to, nt)]
            if nt == "uni":
                c.opt_in = rng.random() < OPT_IN["uni"]
    # rehires: left and came back under a new payroll number
    pool = [c for c in casuals if not c.moves and not c.hired and c.end > dt.date(2026, 12, 31)
            and c.typ0 in ("uni", "flex", "school") and c.start < dt.date(2025, 6, 1)]
    for j in sorted(rng.choice(len(pool), size=N_REHIRES, replace=False).tolist()):
        c = pool[j]
        left = dt.date(2025, 10, 10) + dt.timedelta(days=int(rng.integers(0, 200)))
        back = left + dt.timedelta(days=int(rng.integers(35, 120)))
        c.gap = (left, back)
    perms = []
    pidx = 0
    for store, cfg in STORES.items():
        perday = {dtp: int(round(len([1 for code, n in BASE[dtp].items() for _ in range(int(round(n * cfg["size"])))])
                                 * PERM_FRAC[dtp])) for dtp in BASE}
        n = int(math.ceil((5 * perday["wk"] + perday["sat"] + perday["sun"]) / 4.6))
        for _ in range(n):
            p = Perm()
            p.idx = pidx
            pidx += 1
            p.store = store
            p.emp_type = "FT" if rng.random() < 0.55 else "PT"
            p.leave = []
            for _b in range(int(rng.integers(1, 3))):
                a = D0 + dt.timedelta(days=int(rng.integers(0, 420)))
                if in_ranges(a, LEAVE_FREEZE):
                    continue
                ln = int(rng.integers(5, 12))
                late = rng.random() < P_LATE_LEAVE
                p.leave.append((a, a + dt.timedelta(days=ln), int(rng.integers(3, 13)) if late else 0))
            perms.append(p)
    return casuals, perms


def _casual(rng, idx, store, typ, start, end):
    c = Casual()
    c.idx = idx
    c.store0 = store
    c.typ0 = typ
    c.alpha = TYPE_ALPHA[typ] + rng.normal(0, 0.6)
    lo, hi, plo, phi = TGT[typ]
    c.target = rng.uniform(lo, hi)
    c.target_peak = c.target * rng.uniform(plo, phi)
    c.free_days = set(rng.choice(5, size=2 if typ == "uni" else 3, replace=False).tolist())
    c.off_days = set(rng.choice(7, size=int(rng.integers(0, 2)), replace=False).tolist())
    c.opt_in = rng.random() < OPT_IN[typ]
    c.start = start
    c.end = end
    c.moves = []
    c.gap = None
    c.hired = False
    return c


def service_date(c, d=AS_OF):
    """the workforce system's service date on date d: the start of the engagement current then"""
    if c.gap and d >= c.gap[1]:
        return c.gap[1]
    return c.start


def windows(c, d):
    """the casual's declared availability on date d as (start, end) minute windows"""
    if not c.active(d):
        return []
    wd = d.weekday()
    if wd in c.off_days:
        return []
    t = c.typ(d)
    if t == "school":
        if wd < 5:
            return [(960, 1320)] if school_days(d) else [(480, 1320)]
        return [(480, 1320)]
    if t == "uni":
        if wd < 5 and in_ranges(d, SEMS) and wd not in c.free_days:
            return [(960, 1440)]
        return [(480, 1440)]
    if t == "parent":
        if wd < 5:
            return [(600, 840)]
        return [(480, 840)] if wd == 5 else []
    if wd >= 5:
        return [(360, 1320)]
    return [(360, 1080)] if wd in c.free_days else []


def school_days(d):
    """school students keep their term-time availability until Boxing Day, when they change it for the holidays"""
    return in_ranges(d, TERMS) or (d.month == 12 and 19 <= d.day <= 25)


def covers(ws, s, e):
    return any(a <= s and e <= b for a, b in ws)


# --------------------------------------------------------------------------- rosters
def christmas_of(d):
    return 25 if in_peak(d, PEAK25) else (26 if in_peak(d, PEAK26) else None)


def build_rosters(rng, casuals, perms, days, crew=None):
    """Publish each store's roster for the given days, week by week. A line is a dict: day, start, end, code, pri,
    who (('C', casual index), ('P', permanent index), ('R', crew number) or None for open)."""
    by_store = collections.defaultdict(list)
    perm_by = collections.defaultdict(list)
    for p in perms:
        perm_by[p.store].append(p)
    roster = {s: [] for s in STORES}
    weeks = sorted(set(n // 7 for n in days))
    for w in weeks:
        wdays = [n for n in days if n // 7 == w]
        fri = ddate(w * 7)
        pk = any(is_peak(ddate(n)) for n in wdays)
        for store in STORES:
            cl = [c for c in casuals if c.home(fri) == store and (c.active(ddate(wdays[0])) or c.active(ddate(wdays[-1])))]
            cl.sort(key=lambda c: (service_date(c, fri), c.idx))
            hours = {c.idx: 0.0 for c in cl}
            last = {}
            tgt = {c.idx: (c.target_peak if pk else c.target) * rng.uniform(0.9, 1.1) for c in cl}
            pdays = {p.idx: 0 for p in perm_by[store]}
            crew_hours = collections.Counter()
            for n in wdays:
                d = ddate(n)
                xm = christmas_of(d)
                pos = positions_for(store, d, xm)
                if not pos:
                    continue
                dtp = daytype(d)
                base = [p for p in pos if p[2] == 0]
                extra = [p for p in pos if p[2] == 1]
                nperm = int(round(len(base) * PERM_FRAC[dtp] / (PEAK_BASE if xm else 1.0)))
                permable = sorted([p for p in base if p[3] in PERM_CODES[dtp]], key=lambda p: PERM_CODES[dtp].index(p[3]))
                perm_pos = permable[:nperm]
                cnt = collections.Counter(base)
                avail_p = [p for p in perm_by[store] if pdays[p.idx] < 5
                           and not any(a <= d <= b and lead == 0 for a, b, lead in p.leave)]
                avail_p.sort(key=lambda p: (pdays[p.idx], (p.idx * 7 + n) % 11, p.idx))
                for k, ppos in enumerate(perm_pos):
                    if k < len(avail_p):
                        p = avail_p[k]
                        cnt[ppos] -= 1
                        pdays[p.idx] += 1
                        roster[store].append(dict(day=n, start=ppos[0], end=ppos[1], code=ppos[3], pri=0, who=("P", p.idx)))
                rest = sorted([p for p, k in cnt.items() for _ in range(k)], key=lambda p: (p[0], p[1]))
                for s, e, pri, code in extra:
                    who = None
                    if crew is not None and xm == 25 and store == CREW_STORE_25:
                        ln = paid(e - s) / 60.0
                        for m in crew:
                            if crew_hours[m] + ln <= 38.0 and (m, n) not in crew_hours:
                                crew_hours[m] += ln
                                crew_hours[(m, n)] = 1
                                who = ("R", m)
                                break
                    roster[store].append(dict(day=n, start=s, end=e, code=code, pri=1, who=who))
                today = set()
                for s, e, pri, code in rest:
                    ln = paid(e - s) / 60.0
                    best, bestv = None, None
                    for c in cl:
                        if c.idx in today or not c.active(d):
                            continue
                        if hours[c.idx] + ln > min(38.0, tgt[c.idx] + 2.0):
                            continue
                        if not covers(windows(c, d), s, e):
                            continue
                        lp = last.get(c.idx)
                        if lp and lp[0] == n - 1 and (n * 1440 + s) - (lp[0] * 1440 + lp[1]) < 600:
                            continue
                        v = (tgt[c.idx] - hours[c.idx]) + rng.uniform(0, 1.5)
                        if bestv is None or v > bestv:
                            best, bestv = c, v
                    if best is None:
                        roster[store].append(dict(day=n, start=s, end=e, code=code, pri=0, who=None))
                    else:
                        roster[store].append(dict(day=n, start=s, end=e, code=code, pri=0, who=("C", best.idx)))
                        hours[best.idx] += ln
                        today.add(best.idx)
                        last[best.idx] = (n, e)
    return roster


def publication(n):
    """minutes at which the roster for day n was published: Thursday 10:00, fifteen days before its roster week"""
    fri = (n // 7) * 7
    return (fri - 15) * 1440 + 600


# --------------------------------------------------------------------------- call-ins
def make_needs(rng, roster, casuals, perms, window, open_post=None, skip_open=None):
    """Every shift the rosters put out to call-in for days in `window` (a set of day numbers): open lines at
    publication (or at `open_post`), absences when reported, leave cover when approved after publication."""
    needs = []
    absent_day = collections.defaultdict(set)     # ('C', idx) -> days unavailable through absence
    vacated = set()
    perm_leave = {p.idx: p.leave for p in perms}
    for store in ORDER:
        for li, ln in enumerate(roster[store]):
            n = ln["day"]
            if n not in window:
                continue
            d = ddate(n)
            s, e = n * 1440 + ln["start"], n * 1440 + ln["end"]
            who = ln["who"]
            if who is None:
                if skip_open and store in skip_open:
                    continue
                if open_post is not None:
                    post = open_post
                elif in_peak(d, PEAK25):
                    post = tmin(PUB25)
                else:
                    post = publication(n)
                needs.append(dict(store=store, day=n, s=s, e=e, post=post, kind="OPEN", absent=None, line=(store, li)))
                continue
            if who[0] == "R":
                continue
            if who[0] == "P":
                lv = [x for x in perm_leave[who[1]] if x[0] <= d <= x[1] and x[2] > 0]
                if lv:
                    # leave approved after publication: the line is put out as leave cover
                    a, b, lead = lv[0]
                    post = max(publication(n) + 1440, s - lead * 1440 - int(rng.integers(0, 600)))
                    needs.append(dict(store=store, day=n, s=s, e=e, post=post, kind="LEAVE", absent=who, line=(store, li)))
                    vacated.add((store, li))
                # a permanent's sickness is covered inside the store's permanent team, not through call-in
                continue
            if rng.random() < (P_ABSENT_PEAK if is_peak(d) else P_ABSENT):
                u = rng.random()
                lead = rng.uniform(60, 300) if u < 0.65 else (rng.uniform(300, 960) if u < 0.9 else rng.uniform(1440, 4320))
                nd = dict(store=store, day=n, s=s, e=e, post=int(s - lead), kind="ABSENCE", absent=who, line=(store, li))
                needs.append(nd)
                vacated.add((store, li))
                if who[0] == "C":
                    absent_day[who[1]].add(n)
                if rng.random() < P_DUP_REPORT:
                    # the same absence reaches KWS a second time: a second call-in for the same line
                    p2 = nd["post"] + int(rng.uniform(8, 150))
                    if p2 < s - 60:
                        twin = dict(nd, post=p2)
                        nd["pair"] = twin["pair"] = len(needs)
                        needs.append(twin)
    return needs, vacated, absent_day


class Cascade:
    """The call-in module: one offer at a time, own casuals by service date then opted-in sister-store casuals by
    service date; offers 07:00 to 21:00 unless the shift starts within 12 hours; 60 minutes to answer (20 for a shift
    within 24 hours); a decline is final; the list run out, the shift is posted again at 07:00 the next day."""

    def __init__(self, casuals, roster, vacated, absent_day, rng, brng, drng, reserve_open=False):
        self.cas = casuals
        self.rng, self.brng, self.drng = rng, brng, drng
        self.book = collections.defaultdict(lambda: collections.defaultdict(list))   # idx -> day -> [(s, e, store)]
        self.wk = collections.defaultdict(float)                                       # (idx, week) -> paid hours
        self.dm = collections.defaultdict(int)                                         # (idx, day) -> paid minutes
        self.absent_day = absent_day
        for store in ORDER:
            for li, ln in enumerate(roster[store]):
                if ln["who"] is not None and ln["who"][0] == "C" and (store, li) not in vacated:
                    n = ln["day"]
                    self.add(ln["who"][1], n, n * 1440 + ln["start"], n * 1440 + ln["end"], store)
        self._orders = {}
        self.postings = []
        self.offers = []
        self.feats = []

    def add(self, idx, n, s, e, store):
        self.book[idx][n].append((s, e, store))
        pm = paid(e - s)
        self.wk[(idx, n // 7)] += pm / 60.0
        self.dm[(idx, n)] += pm

    def remove(self, idx, n, s, e, store):
        self.book[idx][n].remove((s, e, store))
        pm = paid(e - s)
        self.wk[(idx, n // 7)] -= pm / 60.0
        self.dm[(idx, n)] -= pm

    def order(self, store, n):
        d = ddate(n)
        key = (store, n // 7, n)
        o = self._orders.get(key)
        if o is None:
            cl = STORES[store]["cluster"]
            act = [c for c in self.cas if c.active(d)]
            own = sorted([c for c in act if c.home(d) == store], key=lambda c: (service_date(c, d), c.idx))
            oth = sorted([c for c in act if c.home(d) != store and cl and c.opt_in and STORES[c.home(d)]["cluster"] == cl],
                         key=lambda c: (service_date(c, d), c.idx))
            o = [c.idx for c in own] + [c.idx for c in oth]
            self._orders[key] = o
        return o

    def eligible(self, idx, nd):
        c = self.cas[idx]
        n = nd["day"]
        if n in self.absent_day.get(idx, ()):
            return False
        d = ddate(n)
        s, e = nd["s"], nd["e"]
        if not covers(windows(c, d), s - n * 1440, e - n * 1440):
            return False
        b = self.book.get(idx)
        if b:
            for bs, be, st in b.get(n, ()):
                if bs < e and s < be:
                    return False
                # no shift that leaves the casual under an hour to get from or to a shift at another store
                if st != nd["store"] and ((be <= s and s - be < TRAVEL_MIN) or (bs >= e and bs - e < TRAVEL_MIN)):
                    return False
            for bs, be, _ in b.get(n - 1, ()):
                if s - be < 600:
                    return False
            for bs, be, _ in b.get(n + 1, ()):
                if bs - e < 600:
                    return False
        ln = paid(e - s)
        if self.dm[(idx, n)] + ln > 660:
            return False
        if self.wk[(idx, n // 7)] + ln / 60.0 > 38.0:
            return False
        return True

    def features(self, idx, nd, t, reoffer):
        c = self.cas[idx]
        n = nd["day"]
        s, e = nd["s"], nd["e"]
        today = self.book[idx].get(n, ())
        ext = any(st == nd["store"] and (be == s or bs == e) for bs, be, st in today)
        split = (not ext) and bool(today)
        d = ddate(n)
        cl = c.home(d) != nd["store"]
        ls, le = s - n * 1440, e - n * 1440
        return dict(ext=ext, split=split, cl=cl, hours_wk=self.wk[(idx, n // 7)], len_h=paid(le - ls) / 60.0,
                    late=le > 1290, early=ls < 420, sun=d.weekday() == 6, short_notice=(s - t) < 240,
                    reoffer=reoffer, dec=is_peak(d))

    def at_work_until(self, idx, t):
        n = int(t // 1440)
        for bs, be, _ in self.book[idx].get(n, ()):
            if bs <= t < be:
                return be
        return None

    def new_posting(self, nd, t):
        pid = len(self.postings)
        self.postings.append(dict(pid=pid, need=nd["nid"], raised=t, closed=None, outcome=None, filled_by=None))
        nd["postings"].append(pid)
        return pid

    def run(self, needs, log=True):
        heap = []
        pairs = collections.defaultdict(list)
        for k, nd in enumerate(needs):
            nd["nid"] = k
            nd.update(ptr=0, declined=set(), asked=set(), filled=None, done=False, postings=[], cur=None, drop=None,
                      parent=nd.get("parent"))
            if nd.get("pair") is not None:
                pairs[nd["pair"]].append(k)
            heapq.heappush(heap, (nd["post"], 0, k, "post"))
        for ks in pairs.values():
            for j in ks[1:]:
                needs[j]["asked"] = needs[ks[0]]["asked"]          # the same shift: a second ask is a re-offer
        pending = {}
        seq = 1
        while heap:
            t, _, k, what = heapq.heappop(heap)
            nd = needs[k]
            if what == "drop":
                who = nd["filled"][0]
                self.remove(who, nd["day"], nd["s"], nd["e"], nd["store"])
                self.absent_day[who].add(nd["day"])
                nd["drop"] = t
                child = dict(store=nd["store"], day=nd["day"], s=nd["s"], e=nd["e"], post=t, kind="ABSENCE",
                             absent=("C", who), line=nd["line"], parent=k)
                child["nid"] = len(needs)
                child.update(ptr=0, declined={who}, asked=set(), filled=None, done=False, postings=[], cur=None, drop=None)
                needs.append(child)
                heapq.heappush(heap, (t, seq, child["nid"], "post"))
                seq += 1
                continue
            if nd["done"]:
                continue
            if what == "post":
                nd["cur"] = self.new_posting(nd, t)
            elif what == "repost":
                nd["cur"] = self.new_posting(nd, t)
            elif what == "resp":
                idx, resp, toff = pending.pop(k)
                if resp == "A" and not self.eligible(idx, nd):
                    resp = "D"
                if log:
                    self.offers.append((nd["cur"], idx, toff, t, resp))
                if resp == "A":
                    self.add(idx, nd["day"], nd["s"], nd["e"], nd["store"])
                    nd["filled"] = (idx, t)
                    nd["done"] = True
                    p = self.postings[nd["cur"]]
                    p.update(closed=t, outcome="FILLED", filled_by=idx)
                    for j in pairs.get(nd.get("pair"), ()):
                        tw = needs[j]
                        if j != k and not tw["done"]:
                            # booking the shift closes the other call-in out for it, FILLED with the casual booked
                            tw["done"] = True
                            if tw["cur"] is not None and self.postings[tw["cur"]]["outcome"] is None:
                                self.postings[tw["cur"]].update(closed=t, outcome="FILLED", filled_by=idx)
                    if nd["s"] - t > 300 and self.drng.random() < P_DROP:
                        td = t + 120 + self.drng.random() * max(0.0, (nd["s"] - 120) - (t + 120))
                        heapq.heappush(heap, (int(td), seq, k, "drop"))
                        seq += 1
                    continue
                if resp == "D":
                    nd["declined"].add(idx)
                nd["ptr"] += 1
            if t >= nd["s"] - 15:
                nd["done"] = True
                self.postings[nd["cur"]].update(closed=t, outcome="UNFILLED")
                continue
            lt = t % 1440
            if nd["s"] - t > 720 and not (420 <= lt < 1260):
                nxt = (t // 1440) * 1440 + 420 + (1440 if lt >= 1260 else 0)
                heapq.heappush(heap, (nxt, seq, k, "next"))
                seq += 1
                continue
            lst = self.order(nd["store"], nd["day"])
            found = None
            while nd["ptr"] < len(lst):
                cand = lst[nd["ptr"]]
                if cand not in nd["declined"] and self.eligible(cand, nd):
                    found = cand
                    break
                nd["ptr"] += 1
            if found is None:
                nxt = (t // 1440) * 1440 + 420
                if nxt <= t:
                    nxt += 1440
                self.postings[nd["cur"]].update(closed=t, outcome="UNFILLED")
                if nxt >= nd["s"] - 30:
                    nd["done"] = True
                    continue
                nd["ptr"] = 0
                heapq.heappush(heap, (nxt, seq, k, "repost"))
                seq += 1
                continue
            reoffer = found in nd["asked"]
            nd["asked"].add(found)
            f = self.features(found, nd, t, reoffer)
            if log:
                self.feats.append((nd["cur"], found, t, f))
            p = sigmoid(accept_logit(self.cas[found].alpha, **f))
            window = 60 if nd["s"] - t > 1440 else 20
            delay = float(np.exp(self.brng.normal(math.log(14.0), 1.0)))
            aw = self.at_work_until(found, t)
            if aw is not None:
                delay += (aw - t)
            if delay > window:
                resp, tr = "N", t + window
            else:
                resp, tr = ("A" if self.brng.random() < p else "D"), t + delay
            pending[k] = (found, resp, t)
            heapq.heappush(heap, (int(math.ceil(tr)) if resp == "N" else tr, seq, k, "resp"))
            seq += 1
        return needs


def settle(needs):
    """each root need (a shift first put out) -> the need that settled it, following drops to their re-raise"""
    child = {nd["parent"]: nd["nid"] for nd in needs if nd.get("parent") is not None}
    out = {}
    for nd in needs:
        if nd.get("parent") is not None:
            continue
        cur = nd
        while cur["drop"] is not None:
            cur = needs[child[cur["nid"]]]
        out[nd["nid"]] = cur
    return out
