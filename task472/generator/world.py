"""Ternmouth Port Authority's fiscal year 2026: six container terminals, their ship-to-shore cranes, the ships that
called, each call's crane runs, the pilot station's sailings under the Harbour Master's access rules (the deep-draught
window at Salt Point for the two river terminals, daylight for the longest ships in the harbour), the Salt Point tide
predictions, the maintenance year with its labour, and the AIS berth record. Every draw comes from a fixed seed; times
are held as UTC seconds and written out later in each system's own clock."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

UTC = dt.timezone.utc
ET = ZoneInfo("America/New_York")
LST = dt.timezone(dt.timedelta(hours=-5))
H, MIN, DAY = 3600, 60, 86400
SEED = 4772


def ts(y, m, d, hh=0, mm=0, tz=ET):
    return int(dt.datetime(y, m, d, hh, mm, tzinfo=tz).timestamp())


def local(t):
    return dt.datetime.fromtimestamp(t, ET)


def utc(t):
    return dt.datetime.fromtimestamp(t, UTC)


def mins(h):
    return int(round(h * 60)) * MIN


FY0, FY1 = ts(2025, 7, 1), ts(2026, 7, 1)             # fiscal year 2026, Eastern time
SPAN0, SPAN1 = ts(2025, 6, 4), ts(2026, 7, 12)          # calls generated around it
DST = (ts(2025, 11, 2, 6, 0, UTC), ts(2026, 3, 8, 7, 0, UTC))
REPEAT = (ts(2025, 11, 2, 5, 0, UTC), ts(2025, 11, 2, 7, 0, UTC))   # the Eastern 01:00 hour that runs twice
CUTOVER = (ts(2026, 2, 1), ts(2026, 3, 1))             # river cranes in the Authority's system from 1 February;
#                                                        SRT's log kept to 28 February (the parallel run)
AS_OF = dt.date(2026, 10, 5)
BOARD_MEETING = dt.date(2026, 10, 27)
AUTHORITY = "Ternmouth Port Authority"

# ---------------------------------------------------------------------------------------------- the port's rules
PASSAGE = dict(SLT=110 * MIN, MRW=160 * MIN)    # berth to Salt Point at the river speed limit
WIN = (-90 * MIN, 30 * MIN)                     # pass Salt Point from 1 h 30 before to 30 min after high water
DEEP_FT = 41.0                                  # a draught of 41 feet or more on sailing
LONG_FT = 1250.0                                # harbour unberthing in daylight for 1,250 feet or more
FT = 0.3048
DAYLIGHT = (6, 20)                              # 0600 to 2000 Eastern clock time
NOTICE = H                                      # a pilot needs an hour's notice

TERMINALS = [
    dict(code="ORD", name="Ore Dock", water="harbor", large=135, small=214, c=(5, 6), span=(19.0, 29.0),
         span_long=(16.0, 22.0)),
    dict(code="PNC", name="Pine Neck", water="harbor", large=168, small=196, c=(5, 6), span=(17.0, 29.0),
         span_long=(16.0, 22.0)),
    dict(code="GNP", name="Gannet Point", water="harbor", large=90, small=171, c=(4, 4), span=(17.0, 27.0),
         span_long=(16.0, 23.0)),
    dict(code="HLY", name="Halyard", water="harbor", large=118, small=203, c=(5, 6), span=(16.0, 28.0),
         span_long=(17.0, 29.0)),
    dict(code="SLT", name="Saltworks", water="river", large=153, small=158, c=(4, 5), span=(25.0, 35.0)),
    dict(code="MRW", name="Millrace", water="river", large=108, small=149, c=(4, 5), span=(18.0, 26.0)),
]
TERM = {t["code"]: t for t in TERMINALS}
CODES = [t["code"] for t in TERMINALS]
NAME = {t["code"]: t["name"] for t in TERMINALS}
GATED = dict(ORD=0.42, PNC=0.48, GNP=0.18, HLY=0.32, SLT=0.88, MRW=0.90)
PATTERNS = dict(ORD=[("dawn", 0.85), ("any", 0.15)], PNC=[("dawn", 0.88), ("any", 0.12)], GNP=[("dawn", 0.30), ("any", 0.70)],
                HLY=[("any", 1.0)], SLT=[("early", 0.92), ("missed", 0.08)],
                MRW=[("missed", 0.74), ("inwin", 0.18), ("early", 0.08)])
SLACK = dict(ORD=(0.3, 3.5), PNC=(0.0, 1.0), GNP=(0.8, 3.0), HLY=(0.6, 3.2), SLT=(0.5, 3.0), MRW=(0.6, 3.6))

# ---------------------------------------------------------------------------------------------- cranes
# id, Authority asset, SRT tag, make, model, commissioned, outreach rows, role, breakdowns per working hour,
# median repair hours, spread, longest repair hours, gross rate (moves per productive hour), home terminal
CRANES = [
    ("Q01", "300095", None, "Paceco", "Portainer PE-40", 1996, 16, "short", 1 / 90, 1.5, 0.6, 6.0, 22, "HLY"),
    ("Q02", "318201", "RQ-104", "Paceco", "Portainer PE-45", 1997, 20, "short", 1 / 11, 1.5, 0.6, 6.0, 25, "MRW"),
    ("Q03", "318218", "RQ-105", "Paceco", "Portainer PE-45", 1997, 20, "short", 1 / 11, 1.5, 0.6, 6.0, 25, "MRW"),
    ("Q04", "300114", None, "Paceco", "Portainer PE-50", 1998, 20, "short", 1 / 12, 1.0, 0.65, 6.0, 25, "ORD"),
    ("Q05", "300122", None, "Paceco", "Portainer PE-50", 1998, 20, "short", 1 / 12, 1.0, 0.65, 6.0, 25, "ORD"),
    ("Q06", "300235", None, "Paceco", "Portainer PE-60", 1999, 22, "long", 1 / 21, 1.6, 0.6, 6.0, 27, "GNP"),
    ("Q07", "318225", "RQ-106", "Paceco", "Portainer PE-45", 1999, 20, "short", 1 / 11, 1.5, 0.6, 6.0, 25, "MRW"),
    ("Q08", "300139", None, "Paceco", "Portainer PE-50", 2000, 20, "short", 1 / 12, 1.0, 0.65, 6.0, 25, "ORD"),
    ("Q09", "318233", "RQ-107", "Mitsubishi", "MHI 45LT", 2000, 20, "short", 1 / 11, 1.5, 0.6, 6.0, 25, "MRW"),
    ("Q10", "318240", "RQ-108", "Mitsubishi", "MHI 45LT", 2000, 20, "short", 1 / 11, 1.5, 0.6, 6.0, 25, "MRW"),
    ("Q11", "300141", None, "Mitsubishi", "MHI 50LT", 2001, 21, "short", 1 / 12, 1.0, 0.65, 6.0, 26, "ORD"),
    ("Q12", "300302", None, "Mitsubishi", "MHI 55LT", 2001, 21, "short", 1 / 58, 4.2, 0.4, 10.0, 27, "HLY"),
    ("Q13", "300319", None, "Mitsubishi", "MHI 55LT", 2001, 21, "short", 1 / 58, 4.2, 0.4, 10.0, 27, "HLY"),
    ("Q14", "300158", None, "Mitsubishi", "MHI 50LT", 2002, 21, "short", 1 / 12, 1.0, 0.65, 6.0, 26, "ORD"),
    ("Q15", "300327", None, "Mitsubishi", "MHI 55LT", 2003, 21, "short", 1 / 58, 4.2, 0.4, 10.0, 27, "HLY"),
    ("Q16", "300334", None, "Mitsubishi", "MHI 55LT", 2004, 21, "short", 1 / 58, 4.2, 0.4, 10.0, 27, "HLY"),
    ("Q17", "300417", None, "Kalmar", "STS 50", 2005, 20, "short", 1 / 80, 1.1, 0.6, 5.0, 27, "GNP"),
    ("Q18", "300425", None, "Kalmar", "STS 50", 2005, 20, "short", 1 / 80, 1.1, 0.6, 5.0, 27, "GNP"),
    ("Q19", "318112", "RQ-101", "Liebherr", "P2026", 2006, 22, "long", 1 / 40, 1.5, 0.6, 6.0, 28, "SLT"),
    ("Q20", "318129", "RQ-102", "Liebherr", "P2026", 2006, 21, "short", 1 / 66, 1.3, 0.6, 6.0, 28, "SLT"),
    ("Q21", "300538", None, "Kalmar", "STS 50", 2007, 20, "short", 1 / 80, 1.1, 0.6, 5.0, 28, "GNP"),
    ("Q22", "318136", "RQ-103", "Liebherr", "P2026", 2007, 21, "short", 1 / 66, 1.3, 0.6, 6.0, 28, "SLT"),
    ("Q23", "300706", None, "Liebherr", "P2238", 2008, 22, "even", 1 / 70, 2.0, 0.5, 6.0, 29, "PNC"),
    ("Q24", "300713", None, "Liebherr", "P2238", 2008, 22, "even", 1 / 70, 2.0, 0.5, 6.0, 29, "PNC"),
    ("Q25", "300721", None, "Liebherr", "P2238", 2009, 22, "even", 1 / 70, 2.0, 0.5, 6.0, 29, "PNC"),
    ("Q26", "300738", None, "Liebherr", "P2238", 2009, 22, "even", 1 / 70, 2.0, 0.5, 6.0, 29, "PNC"),
    ("Q27", "300546", None, "Kalmar", "STS 50", 2009, 20, "short", 1 / 80, 1.1, 0.6, 5.0, 28, "GNP"),
    ("Q28", "318144", "RQ-109", "Kalmar", "STS 45", 2010, 21, "short", 1 / 66, 1.3, 0.6, 6.0, 28, "SLT"),
    ("Q29", "318151", "RQ-110", "Kalmar", "STS 45", 2010, 21, "short", 1 / 66, 1.3, 0.6, 6.0, 28, "SLT"),
    ("Q30", "300744", None, "Konecranes", "STS 22R", 2011, 22, "even", 1 / 70, 2.0, 0.5, 6.0, 29, "PNC"),
    ("Q31", "300752", None, "Konecranes", "STS 22R", 2011, 22, "even", 1 / 70, 2.0, 0.5, 6.0, 29, "PNC"),
    ("Q32", "300769", None, "Konecranes", "STS 22R", 2012, 22, "even", 1 / 70, 2.0, 0.5, 6.0, 29, "PNC"),
    ("Q33", "318167", "RQ-111", "Kalmar", "STS 45", 2013, 21, "short", 1 / 66, 1.3, 0.6, 6.0, 28, "SLT"),
    ("Q34", "301018", None, "ZPMC", "STS 65t", 2015, 23, "long", 1 / 170, 1.2, 0.5, 4.0, 32, "HLY"),
    ("Q35", "301026", None, "ZPMC", "STS 65t", 2015, 23, "long", 1 / 170, 1.2, 0.5, 4.0, 32, "HLY"),
    ("Q36", "318174", "RQ-112", "ZPMC", "STS 50t", 2016, 22, "long", 1 / 40, 1.3, 0.6, 6.0, 30, "MRW"),
    ("Q37", "301207", None, "ZPMC", "STS 65t tandem", 2022, 24, "long", 1 / 170, 1.0, 0.6, 4.0, 33, "ORD"),
    ("Q38", "301215", None, "ZPMC", "STS 65t tandem", 2022, 24, "long", 1 / 170, 1.0, 0.6, 4.0, 33, "ORD"),
]
CRANE_KEYS = ("name", "asset", "tag", "make", "model", "year", "outreach", "role", "lam", "dmed", "dsig", "cap", "rate",
              "home")
CR = {c[0]: dict(zip(CRANE_KEYS, c)) for c in CRANES}
# three cranes travel the common rail to the neighbouring terminal during the year; they keep their numbers
MOVES = {"Q08": ("PNC", ts(2025, 11, 6, 7, 0), ts(2025, 11, 14, 15, 0)),
         "Q13": ("GNP", ts(2026, 2, 5, 7, 0), ts(2026, 2, 13, 15, 0)),
         "Q28": ("MRW", ts(2026, 4, 15, 7, 0), ts(2026, 4, 23, 15, 0))}
IDLE_LAM = 1 / 650


def term_at(crane, t):
    mv = MOVES.get(crane)
    if mv and t >= mv[1]:
        return mv[0]
    return CR[crane]["home"]


def moving(crane, a, b):
    mv = MOVES.get(crane)
    return bool(mv and a < mv[2] and b > mv[1])


def term_now(crane):
    return MOVES[crane][0] if crane in MOVES else CR[crane]["home"]


def cranes_at(code, t):
    return [c[0] for c in CRANES if term_at(c[0], t) == code]


# ---------------------------------------------------------------------------------------------- tides
TIDE_REF = ts(2025, 1, 1, 0, 0, UTC)
CONSTITUENTS = [(4.31, 12.4206012, 1.20), (0.92, 12.6583482, 0.40), (0.71, 12.0, 2.10), (0.36, 23.9344697, 0.90),
                (0.27, 25.8193417, 2.60)]
DATUM = 2.62


def tide_height(t):
    th = (np.asarray(t, dtype=np.float64) - TIDE_REF) / H
    return DATUM + sum(a * np.cos(2 * np.pi * th / p - ph) for a, p, ph in CONSTITUENTS)


def tide_table():
    """Predicted high and low waters at Salt Point, to the minute: [(utc seconds, 'H' or 'L', height in feet)]."""
    t = np.arange(SPAN0 - 4 * DAY, SPAN1 + 8 * DAY, MIN, dtype=np.int64)
    h = tide_height(t)
    d = np.diff(h)
    hi = np.where((d[:-1] > 0) & (d[1:] <= 0))[0] + 1
    lo = np.where((d[:-1] < 0) & (d[1:] >= 0))[0] + 1
    ev = [(int(t[i]), "H", round(float(h[i]), 2)) for i in hi] + [(int(t[i]), "L", round(float(h[i]), 2)) for i in lo]
    ev.sort()
    kinds = [k for _, k, _ in ev]
    assert all(a != b for a, b in zip(kinds, kinds[1:])), "high and low waters alternate"
    hws = [x for x, k, _ in ev if k == "H"]
    gaps = np.diff(hws) / H
    assert gaps.min() > 10.5 and gaps.max() < 14.5, (gaps.min(), gaps.max())
    return ev


def river_windows(hw, code):
    """Let-go windows at a river terminal for a deep-draught sailing: pass Salt Point inside the window."""
    hw = np.asarray(hw, dtype=np.int64)
    return np.stack([hw + WIN[0] - PASSAGE[code], hw + WIN[1] - PASSAGE[code]], axis=1)


def day_windows():
    out = []
    d = local(SPAN0 - 3 * DAY).date()
    while True:
        a = int(dt.datetime(d.year, d.month, d.day, DAYLIGHT[0], tzinfo=ET).timestamp())
        b = int(dt.datetime(d.year, d.month, d.day, DAYLIGHT[1], tzinfo=ET).timestamp())
        out.append((a, b))
        if a > SPAN1 + 10 * DAY:
            break
        d += dt.timedelta(days=1)
    return np.array(out, dtype=np.int64)


def earliest(t, wins):
    """The first time at or after t inside one of the windows."""
    i = int(np.searchsorted(wins[:, 1], t))
    return max(t, int(wins[i, 0]))


def edge_gap(t, wins):
    """Seconds from t to the nearest window edge."""
    i = int(np.searchsorted(wins[:, 0], t))
    cand = wins[max(i - 1, 0):i + 1].ravel()
    return int(np.min(np.abs(cand - t)))


# ---------------------------------------------------------------------------------------------- crane runs
class Run:
    """One crane's run on one call. Work clock: seconds of the crane's own planned run from its first move (0) to its
    last (D). Breakdowns sit at work-clock positions and push everything after them later by their length."""
    __slots__ = ("crane", "start", "D", "moves_w", "bk", "slack", "bays", "rate", "off", "sec")

    def __init__(self, crane, off, sec, D, slack):
        self.crane, self.off, self.sec, self.D, self.slack = crane, off, sec, D, slack
        self.start, self.moves_w, self.bk, self.bays, self.rate = None, None, [], None, None

    def to_clock(self, w):
        w = np.asarray(w, dtype=np.int64)
        add = np.zeros_like(w)
        for u, d in self.bk:
            add += np.where(w >= u, d, 0)
        return self.start + w + add

    @property
    def F(self):
        return sum(d for _, d in self.bk)

    @property
    def rel_end(self):
        return self.off + self.sec + self.D + self.F

    @property
    def end(self):
        return self.start + self.D + self.F

    def bk_clock(self):
        out, before = [], 0
        for u, d in sorted(self.bk):
            s = self.start + u + before
            out.append((s, s + d))
            before += d
        return out


def draw_repair(rng, spec):
    h = float(np.clip(rng.lognormal(np.log(spec["dmed"]), spec["dsig"]), 0.3, spec["cap"]))
    return mins(h)


def plan_moves(rng, run, spec):
    D = run.D
    npause = rng.poisson(D / H / 3.5)
    pauses = sorted((int(rng.uniform(0.05, 0.95) * D), mins(rng.uniform(8, 32) / 60)) for _ in range(npause))
    busy = sum(ln for _, ln in pauses)
    prod = max(D - busy, int(D * 0.6))
    rate = spec["rate"] * rng.uniform(0.94, 1.06)
    n = max(int(round(prod / H * rate)), 12)
    base = np.linspace(0, prod, n)
    jit = rng.uniform(-0.35, 0.35, n) * (prod / max(n - 1, 1))
    jit[0] = jit[-1] = 0
    p = np.sort(np.clip(base + jit, 0, prod)).astype(np.int64)
    scale = prod / D
    w = p.copy()
    for p0, ln in pauses:
        w = np.where(p >= int(p0 * scale), w + ln, w)
    w = np.clip(w, 0, D)
    w[0], w[-1] = 0, D
    run.moves_w, run.rate = np.unique(w), rate


def place_breakdowns(rng, run, spec, lo, hi):
    D = run.D
    if D / H - (lo + hi) / H <= 0.3:
        return
    n = rng.poisson(spec["lam"] * max(D / H - 3.0, 0.0))
    us = sorted(int(rng.uniform(lo, D - hi) / MIN) * MIN for _ in range(n))
    kept = []
    for u in us:
        if kept and u - kept[-1][0] < 25 * MIN:
            continue
        kept.append((u, draw_repair(rng, spec)))
    run.bk = kept


def draft_runs(rng, cranes, span, slack_rng, salt):
    """A call's crane runs relative to its first minute: the lead crane works the whole planned span, the others
    start within 36 minutes and finish earlier by their slack; breakdowns lengthen whichever run they fall on."""
    D_lead = mins(rng.uniform(*span))
    runs = []
    for i, c in enumerate(cranes):
        spec = CR[c]
        off = 0 if i == 0 else mins(rng.uniform(0, 0.6))
        slack = 0.0 if i == 0 else float(rng.uniform(*slack_rng))
        sec = 3 + (salt * 31 + i * 17 + sum(map(ord, c)) * 7) % 53
        D = max(D_lead - off - mins(slack), 3 * H)
        r = Run(c, off, sec, D, slack)
        plan_moves(rng, r, spec)
        place_breakdowns(rng, r, spec, 1.5 * H, 1.5 * H)
        runs.append(r)
    return runs


class Call:
    __slots__ = ("term", "large", "vessel", "t0", "runs", "visit", "arr_lag", "berth", "seq", "nbays", "gated",
                 "pattern", "prep", "notice", "sail", "draft", "anchor_before", "letgo_lag", "shift_from")

    def __init__(self, term, large, vessel, runs):
        self.term, self.large, self.vessel, self.runs = term, large, vessel, runs
        self.t0 = self.visit = self.arr_lag = self.berth = self.seq = self.nbays = None
        self.gated, self.pattern, self.prep, self.notice, self.sail, self.draft = False, None, None, None, None, None
        self.anchor_before, self.letgo_lag, self.shift_from = None, None, None

    def place(self, t0):
        self.t0 = t0
        for r in self.runs:
            r.start = t0 + r.off + r.sec

    @property
    def first(self):
        return min(r.start for r in self.runs)

    @property
    def last(self):
        return max(r.end for r in self.runs)

    @property
    def rel_last(self):
        return max(r.rel_end for r in self.runs)

    @property
    def rel_first(self):
        return min(r.off + r.sec for r in self.runs)

    @property
    def in_fy(self):
        return FY0 <= self.first < FY1

    @property
    def ready(self):
        return self.notice + NOTICE

    @property
    def span(self):
        return self.last - self.first


# ---------------------------------------------------------------------------------------------- vessels
CARRIERS = [("Corvane Shipping", "CORVANE"), ("Eastmere Container Line", "EASTMERE"), ("Hallvik Line", "HALLVIK"),
            ("Pacific Arrow Lines", "PACIFIC ARROW"), ("Tessaline", "TESSA"), ("Morrow Kade Container", "MK"),
            ("Brightwater Liner", "BRIGHTWATER"), ("Ostrel Marine", "OSTREL")]
STARS = ["ANTARES", "ALTAIR", "BELLATRIX", "CAPELLA", "DENEB", "ELNATH", "FOMALHAUT", "HADAR", "MIRFAK", "POLLUX",
         "RIGEL", "SADR", "SHAULA", "SPICA", "VEGA", "ALCOR", "MENKAR", "SABIK", "WEZEN", "ALNAIR", "MARKAB", "ACRUX",
         "MIMOSA", "ATRIA", "AVIOR", "DUBHE", "KOCHAB", "MERAK", "PHECDA", "ALHENA", "ALUDRA", "CASTOR", "NUNKI",
         "ALDERAMIN", "ANKAA", "CANOPUS", "DIPHDA", "ENIF", "GIENAH", "HAMAL", "IZAR", "KAUS", "MENKENT", "MINTAKA",
         "NAOS", "PEACOCK", "REGULUS", "SAIPH", "SCHEDAR", "TARAZED", "ZOSMA", "ALPHARD", "ARCTURUS", "ACHERNAR"]
PLACES = ["HALIFAX", "VALENCIA", "COLOMBO", "TANGIER", "SANTOS", "DAMIETTA", "PIRAEUS", "SALALAH", "KLANG", "ALGECIRAS",
          "GDANSK", "NINGBO", "XIAMEN", "LAEM CHABANG", "CARTAGENA", "MANZANILLO", "KINGSTON", "FREEPORT", "BALBOA",
          "CAUCEDO", "TEMA", "LOME", "DURBAN", "JEDDAH", "MUNDRA", "COCHIN", "QINGDAO", "BUSAN", "KAOHSIUNG",
          "MONTEVIDEO", "CALLAO", "VERACRUZ", "SAVONA", "ANTWERP", "LE HAVRE", "BREMEN", "AARHUS", "GOTHENBURG",
          "TRIESTE", "KOPER", "MERSIN", "SOHAR", "CHITTAGONG", "HAIPHONG", "MANILA", "DAVAO", "LYTTELTON", "NAPIER"]
FLAGS = [("Liberia", "636", "D5"), ("Marshall Islands", "538", "V7"), ("Panama", "352", "3E"), ("Panama", "370", "3F"),
         ("Singapore", "563", "9V"), ("Malta", "248", "9H"), ("Hong Kong", "477", "VR"), ("Portugal", "255", "CQ"),
         ("Cyprus", "209", "5B"), ("Denmark", "219", "OZ"), ("Greece", "241", "SV"), ("Germany", "211", "DD")]


def imo_number(rng, used):
    while True:
        d = [int(x) for x in str(int(rng.integers(930000, 990000)))]
        chk = sum(v * w for v, w in zip(d, (7, 6, 5, 4, 3, 2))) % 10
        n = int("".join(map(str, d)) + str(chk))
        if n not in used:
            used.add(n)
            return n


def make_fleet(rng):
    """Four classes: ships of 1,250 feet and more (18,000 TEU up), the other large ships the harbour takes, the
    large ships the river berths take (330 to 350 metres), and the feeders; a few renamed or re-flagged in the year."""
    used, names, out = set(), set(), []

    def name_for(prefix):
        for i in range(4000):
            if i >= 400:
                prefix = CARRIERS[int(rng.integers(len(CARRIERS)))][1]
            pool = STARS if rng.random() < 0.6 else PLACES
            nm = "%s %s" % (prefix, pool[int(rng.integers(len(pool)))])
            if nm not in names:
                names.add(nm)
                return nm
        raise RuntimeError("names")

    def call_sign(cs):
        return cs + "%s%d" % ("".join(chr(65 + int(rng.integers(26))) for _ in range(2)), int(rng.integers(1, 9)))

    def vessel(cls):
        carrier, prefix = CARRIERS[int(rng.integers(len(CARRIERS)))]
        if cls == "ulcv":
            teu = int(rng.choice([18300, 19100, 19900, 20400, 21400, 23500, 24200]) + int(rng.integers(-60, 61)))
            loa = float(rng.choice([399.0, 399.9, 400.0])) + float(rng.uniform(-0.4, 0.0))
            beam = 58.6 if teu < 21000 else 61.5
            built = int(rng.integers(2014, 2025))
            draft = 16.0
        elif cls == "harbor":
            teu = int(rng.choice([10400, 11000, 11400, 12200, 13100, 13800, 14400, 15000, 15200]) +
                      int(rng.integers(-60, 61)))
            loa = 330 + (teu - 10000) / 5300 * 36 + rng.uniform(-3, 1.5)
            beam = 48.2 if teu < 13000 else 51.0
            built = int(rng.integers(2009, 2024))
            draft = 15.0 + rng.uniform(-0.4, 0.5)
        elif cls == "river":
            teu = int(rng.choice([10200, 10600, 11000, 11400, 12000, 12400, 12800]) + int(rng.integers(-60, 61)))
            loa = 331 + (teu - 10000) / 3000 * 17 + rng.uniform(-2, 1.5)
            beam = 48.2
            built = int(rng.integers(2008, 2023))
            draft = 14.5 + rng.uniform(-0.3, 0.4)
        else:
            teu = int(rng.choice([1700, 2500, 2800, 3500, 4250, 4400, 5000, 6500, 6600, 8500, 8800, 9200, 9400])
                      + int(rng.integers(-40, 41)))
            loa = 170 + (teu - 1700) / 8000 * 130 + rng.uniform(-5, 5)
            beam = 27.3 if teu < 3000 else (32.3 if teu < 5200 else (40.0 if teu < 8000 else 45.6))
            built = int(rng.integers(2002, 2024))
            draft = 9.0 + teu / 9400 * 4.5
        flag, mid, cs = FLAGS[int(rng.integers(len(FLAGS)))]
        v = dict(imo=imo_number(rng, used), name=name_for(prefix), carrier=carrier, teu=teu, loa=round(loa, 1),
                 beam=beam, built=built, flag=flag, mmsi=int(mid + "%06d" % int(rng.integers(100000, 999999))),
                 call_sign=call_sign(cs), cls=cls, large=cls != "feeder", former=[], draft=round(draft, 1),
                 reflag=None)
        v["dwt"] = int(teu * rng.uniform(11.2, 13.4))
        return v

    for cls, n in (("ulcv", 34), ("harbor", 72), ("river", 46), ("feeder", 176)):
        out.extend(vessel(cls) for _ in range(n))
    for _ in range(64):                       # on the register, no call at Ternmouth in the year
        out.append(vessel(["ulcv", "harbor", "river", "feeder"][int(rng.integers(4))]))
    # renamed during or before the year (sold on, or the charter changed); the register keeps the former name
    for v in rng.choice(out[:328], size=14, replace=False):
        carrier, prefix = CARRIERS[int(rng.integers(len(CARRIERS)))]
        v["former"] = [dict(name=v["name"], until=str(dt.date(2025, 7, 1) + dt.timedelta(days=int(rng.integers(20, 330)))))]
        v["name"] = name_for(prefix)
        v["carrier"] = carrier
    # re-flagged in the year without a change of name: a new call sign and MMSI from the change
    cands = [v for v in out[:328] if not v["former"]]
    for v in rng.choice(cands, size=8, replace=False):
        flag, mid, cs = FLAGS[int(rng.integers(len(FLAGS)))]
        while flag == v["flag"]:
            flag, mid, cs = FLAGS[int(rng.integers(len(FLAGS)))]
        day = dt.date(2025, 8, 1) + dt.timedelta(days=int(rng.integers(0, 300)))
        v["reflag"] = dict(day=str(day), old_call_sign=v["call_sign"], old_mmsi=v["mmsi"], old_flag=v["flag"])
        v["flag"], v["call_sign"] = flag, call_sign(cs)
        v["mmsi"] = int(mid + "%06d" % int(rng.integers(100000, 999999)))
    for v in out:
        assert not (9700 <= v["teu"] <= 10300) or v["cls"] in ("harbor", "river") and v["teu"] >= 10140
        assert not (368.5 <= v["loa"] <= 398.0)
    return out


def call_sign_on(v, t):
    rf = v.get("reflag")
    if rf and local(t).date() < dt.date.fromisoformat(rf["day"]):
        return rf["old_call_sign"]
    return v["call_sign"]


def mmsi_on(v, t):
    rf = v.get("reflag")
    if rf and local(t).date() < dt.date.fromisoformat(rf["day"]):
        return rf["old_mmsi"]
    return v["mmsi"]


def name_on(v, t):
    for f in v.get("former", []):
        if local(t).date() <= dt.date.fromisoformat(f["until"]):
            return f["name"]
    return v["name"]


# ---------------------------------------------------------------------------------------------- the year's calls
def ft_in(feet):
    """A draught in feet to feet and whole inches."""
    f = int(feet)
    i = int(round((feet - f) * 12))
    if i == 12:
        f, i = f + 1, 0
    return f, i


def place_ready(pattern, code, r0, rng, wins, day):
    """The readiness (notice plus an hour) a call's pattern puts it at, the first at or after r0."""
    if pattern in ("early", "missed", "inwin"):
        W = wins[code]
        if pattern == "early":
            w = mins(rng.uniform(0.3, 2.0) if code == "SLT" else rng.uniform(0.3, 2.5))
            k = int(np.searchsorted(W[:, 0] - w, r0))
            return int(W[k, 0] - w)
        if pattern == "missed":
            late = mins(rng.uniform(0.4, 3.0) if code == "SLT" else rng.uniform(1.0, 4.4))
            k = int(np.searchsorted(W[:, 1] + late, r0))
            return int(W[k, 1] + late)
        k = int(np.searchsorted(W[:, 1] - 10 * MIN, r0))
        a = max(r0, int(W[k, 0]) + 3 * MIN)
        b = int(W[k, 1]) - 3 * MIN
        return a + mins(rng.uniform(0, max(b - a, 0) / H))
    if pattern == "dawn":
        d = local(r0).date()
        while True:
            hh = rng.uniform(4.0, 5.67)
            t = int(dt.datetime(d.year, d.month, d.day, int(hh), int(round((hh % 1) * 60)) % 60, tzinfo=ET).timestamp())
            if t >= r0:
                return t
            d += dt.timedelta(days=1)
    return int(-(-r0 // MIN) * MIN)


def permitted(c, wins, day):
    if not c.gated:
        return None
    return wins[c.term] if TERM[c.term]["water"] == "river" else day


def check_call(c, wins, day, prev_sail):
    """A placed large call is kept only if nothing in it sits on an edge the records could read two ways."""
    if not c.in_fy and SPAN0 + 2 * DAY < c.first < SPAN1 - 2 * DAY and False:
        return False
    for f in (FY0, FY1):
        if abs(c.first - f) < 6 * H:
            return False
    if TERM[c.term]["water"] == "river" and c.first - 2 * DAY < FY0 < c.sail + 2 * DAY:
        return False
    for x in (c.first, c.last, c.notice, c.sail):
        if REPEAT[0] - 10 * MIN <= x < REPEAT[1] + 10 * MIN:
            return False
    for r in c.runs:
        for s, e in r.bk_clock():
            if any(s - 30 * MIN < z < e + 30 * MIN for z in DST):
                return False
    W = permitted(c, wins, day)
    if W is not None:
        cut = c.span / 5.0
        for x in (c.ready, c.ready - cut):
            if edge_gap(int(round(x)), W) < 2 * MIN:
                return False
    if c.first - c.arr_lag < prev_sail + 40 * MIN:
        return False
    return True


def gold_saving(c, wins, day):
    cut = c.span / 5.0
    W = permitted(c, wins, day)
    if W is None:
        return cut / H
    return (c.sail - earliest(c.ready - cut, W)) / H


def edge_need(tot, rng, floor=0.15):
    """Hours to add so a whole-hour figure sits at least `floor` from the edge of its cell and does not print as a
    multiple of ten, landing it at a random point well off both the edge and the centre; 0 when it already does."""
    frac = tot - np.floor(tot)
    if abs(frac - 0.5) >= floor and int(round(tot)) % 10 != 0:
        return 0.0
    base = np.floor(tot) + (1 if int(round(tot)) % 10 == 0 and frac < 0.5 else 0)
    if int(base + 1) % 10 == 0:
        base += 1
    return float(base + rng.uniform(0.66, 0.84)) - tot


def tune_terminal(code, calls, wins, day, rng):
    """Move a terminal's berth hours saved off the edge of its whole-hour cell: the lead crane on one call that
    nothing holds starts earlier, which lengthens that call's cargo work and nothing else."""
    mine = sorted([c for c in calls if c.term == code and c.large], key=lambda c: c.t0)
    fy = [c for c in mine if c.in_fy]
    need = edge_need(sum(gold_saving(c, wins, day) for c in fy), rng)
    if not need:
        return
    k = int(round(need * 5 * 60)) * MIN
    for i, c in enumerate(mine):
        if not c.in_fy or c.gated or i == 0:
            continue
        lead = min(c.runs, key=lambda r: r.start)
        new_first = lead.start - k
        prev = mine[i - 1]
        if new_first - c.arr_lag < prev.sail + 40 * MIN:
            continue
        if any(abs(new_first - f) < 6 * H for f in (FY0, FY1)) or REPEAT[0] - 10 * MIN <= new_first < REPEAT[1] + 10 * MIN:
            continue
        lead.start = new_first
        lead.D += k
        lead.bk = [(u + k, d) for u, d in lead.bk]
        plan_moves(rng, lead, CR[lead.crane])
        tot = sum(gold_saving(x, wins, day) for x in fy)
        assert abs((tot - np.floor(tot)) - 0.5) >= 0.15 and int(round(tot)) % 10 != 0, (code, tot)
        return
    raise AssertionError("no call to tune at " + code)


def schedule(seed=SEED):
    rng = np.random.default_rng(seed)
    fleet = make_fleet(np.random.default_rng(seed + 1))
    tides = tide_table()
    hw = [t for t, k, _ in tides if k == "H"]
    wins = {code: river_windows(hw, code) for code in ("SLT", "MRW")}
    day = day_windows()
    calls, busy, free_at = [], {}, {}
    pools = {}
    prng = np.random.default_rng(seed + 2)
    for code in CODES:
        river = TERM[code]["water"] == "river"
        for cls in (["river"] if river else ["ulcv", "harbor"]):
            ships = [v for v in fleet[:328] if v["cls"] == cls]
            pools[(code, cls)] = [ships[i] for i in prng.choice(len(ships), size=min(len(ships), 26), replace=False)]
        pools[(code, "feeder")] = [v for v in fleet[:328] if v["cls"] == "feeder"]

    def ok(v, t, cls):
        gap = (21 if cls != "feeder" else 9) * DAY
        return all(abs(t - u) >= gap for u in free_at.get(v["imo"], ()))

    def pick_vessel(code, cls, t, trng):
        pool = pools[(code, cls)]
        start = int(trng.integers(len(pool)))
        for i in range(len(pool)):
            v = pool[(start + i) % len(pool)]
            if ok(v, t, cls):
                return v
        others = [v for v in fleet[:328] if v["cls"] == cls and ok(v, t, cls)]
        return others[int(trng.integers(len(others)))]

    for k, T in enumerate(TERMINALS):
        code = T["code"]
        trng = np.random.default_rng(seed * 10 + k)
        river = T["water"] == "river"
        gap = (FY1 - FY0) / T["large"]
        nominal = SPAN0 + int(trng.uniform(0, gap))
        prev_sail = SPAN0 - DAY
        salt = 0
        while nominal < SPAN1:
            salt += 1
            gated = bool(trng.random() < GATED[code])
            pats = PATTERNS[code]
            pattern = None
            if gated:
                u, acc = trng.random(), 0.0
                for nm, p in pats:
                    acc += p
                    if u < acc:
                        pattern = nm
                        break
                pattern = pattern or pats[-1][0]
            here = [x for x in cranes_at(code, nominal) if not moving(x, nominal - DAY, nominal + 3 * DAY)]
            longs = [x for x in here if CR[x]["role"] == "long"]
            shorts = [x for x in here if CR[x]["role"] != "long"]
            n = int(trng.integers(T["c"][0], T["c"][1] + 1))
            n = min(n, len(here))
            chosen = longs[:n] + list(trng.choice(shorts, size=max(n - len(longs), 0), replace=False))
            order = [c[0] for c in CRANES]
            chosen = sorted(chosen, key=lambda z: (CR[z]["role"] != "long", order.index(z)))
            span = T["span_long"] if (gated and not river) else T["span"]
            runs = draft_runs(trng, chosen, span, SLACK[code], salt)
            cls = ("ulcv" if gated else "harbor") if not river else "river"
            v = pick_vessel(code, cls, nominal, trng)
            c = Call(code, True, v, runs)
            c.gated, c.pattern = gated, pattern
            c.arr_lag = mins(trng.uniform(0.9, 2.4))
            prep_target = mins(trng.uniform(0.4, 1.6))
            rel_last = c.rel_last
            earliest_t0 = max(nominal, prev_sail + c.arr_lag + mins(trng.uniform(1.0, 5.0)))
            r0 = int(-(-(earliest_t0 + rel_last + prep_target + NOTICE + MIN) // MIN) * MIN)
            placed = False
            for attempt in range(40):
                r = place_ready(pattern if gated else None, code, r0, trng, wins, day)
                notice = r - NOTICE
                t0 = int(((notice - prep_target - rel_last) // MIN) * MIN)
                c.place(t0)
                c.notice = notice
                c.prep = notice - c.last
                W = permitted(c, wins, day)
                c.sail = earliest(c.ready, W) if W is not None else c.ready
                if c.first - c.arr_lag >= prev_sail + 40 * MIN and check_call(c, wins, day, prev_sail):
                    placed = True
                    break
                r0 = r + 20 * MIN
            assert placed, (code, nominal)
            if river:
                if gated:
                    c.draft = float(trng.uniform(41.09, 44.5))
                else:
                    c.draft = float(trng.uniform(36.0, 40.9))
            else:
                c.draft = float(trng.uniform(37.0, 48.0)) if v["cls"] != "ulcv" else float(trng.uniform(42.0, 50.5))
            c.letgo_lag = int(trng.uniform(2, 14)) * MIN
            calls.append(c)
            free_at.setdefault(v["imo"], []).append(nominal)
            for r in runs:
                busy.setdefault(r.crane, []).append((r.start - 30 * MIN, c.last + 3 * H))
            prev_sail = c.sail
            nominal = nominal + int(gap * trng.gamma(5.0, 1 / 5.0))
        tune_terminal(code, calls, wins, day, np.random.default_rng(seed * 10 + k + 500))
        # feeders, on the cranes the large calls leave free
        gap_s = (FY1 - FY0) / T["small"]
        t = SPAN0 + int(trng.uniform(0, gap_s))
        while t < SPAN1:
            salt += 1
            t = (t // MIN) * MIN
            n = int(trng.integers(2, 4 if river else 5))
            Hh = trng.uniform(6.0, 16.0)
            here = [x for x in cranes_at(code, t) if not moving(x, t - DAY, t + 2 * DAY)]
            free = [x for x in here if all(not (s < t + int((Hh + 9) * H) and e > t - 30 * MIN)
                                           for s, e in busy.get(x, ()))]
            if len(free) < n or (river and t - 2 * DAY < FY0 < t + int((Hh + 6) * H) + 2 * DAY):
                t += int(trng.uniform(1.5, 4.0) * H)
                continue
            chosen = list(trng.choice(free, size=n, replace=False))
            runs = draft_runs(trng, chosen, (Hh - 0.2, Hh + 0.2), (0.0, 3.0), salt)
            v = pick_vessel(code, "feeder", t, trng)
            c = Call(code, False, v, runs)
            c.place(t)
            c.arr_lag = mins(trng.uniform(0.6, 1.6))
            c.notice = int(-(-(c.last + mins(trng.uniform(0.3, 1.2))) // MIN) * MIN)
            c.prep = c.notice - c.last
            c.sail = c.ready
            c.draft = float(min(v["draft"] / FT * trng.uniform(0.82, 0.97), 38.5))
            c.letgo_lag = int(trng.uniform(2, 12)) * MIN
            if any(REPEAT[0] - 10 * MIN <= x < REPEAT[1] + 10 * MIN for x in (c.notice, c.sail)):
                t += 3 * H
                continue
            calls.append(c)
            free_at.setdefault(v["imo"], []).append(t)
            for r in runs:
                busy.setdefault(r.crane, []).append((r.start - 30 * MIN, r.end + 30 * MIN))
            t += int(gap_s * trng.gamma(3.0, 1 / 3.0))
    calls.sort(key=lambda c: (c.t0, c.term))
    return dict(calls=calls, fleet=fleet, busy=busy, tides=tides, wins=wins, day=day)


# ---------------------------------------------------------------------------------------------- the rest of the year
BERTHS = dict(ORD=["ORD B1", "ORD B2", "ORD B3", "ORD B4"], PNC=["PNC B1", "PNC B2", "PNC B3"],
              GNP=["GNP B1", "GNP B2"], HLY=["HLY B1", "HLY B2", "HLY B3", "HLY B4"], SLT=["SLT 1", "SLT 2"],
              MRW=["MRW 1", "MRW 2"])
PILOT_BERTH = {"ORD B1": "ORE DOCK 1", "ORD B2": "ORE DOCK 2", "ORD B3": "ORE DOCK 3", "ORD B4": "ORE DOCK 4",
               "PNC B1": "PINE NECK 1", "PNC B2": "PINE NECK 2", "PNC B3": "PINE NECK 3", "GNP B1": "GANNET PT 1",
               "GNP B2": "GANNET PT 2", "HLY B1": "HALYARD 1", "HLY B2": "HALYARD 2", "HLY B3": "HALYARD 3",
               "HLY B4": "HALYARD 4", "SLT 1": "SALTWORKS 1", "SLT 2": "SALTWORKS 2", "MRW 1": "MILLRACE 1",
               "MRW 2": "MILLRACE 2"}
ZONE = {"ORD B1": "ORE DOCK 1", "ORD B2": "ORE DOCK 2", "ORD B3": "ORE DOCK 3", "ORD B4": "ORE DOCK 4",
        "PNC B1": "PINE NECK 1", "PNC B2": "PINE NECK 2", "PNC B3": "PINE NECK 3", "GNP B1": "GANNET PT 1",
        "GNP B2": "GANNET PT 2", "HLY B1": "HALYARD 1", "HLY B2": "HALYARD 2", "HLY B3": "HALYARD 3",
        "HLY B4": "HALYARD 4", "SLT 1": "SALTWORKS WHARF", "SLT 2": "SALTWORKS WHARF", "MRW 1": "MILLRACE 1",
        "MRW 2": "MILLRACE 2"}
ANCHOR = dict(harbor=["TMH ANCH ALPHA", "TMH ANCH BRAVO", "TMH ANCH CHARLIE"], river=["LOWER REACH ANCH"])
SERVICES = dict(ORD=["AE7", "TPX", "NEU3"], PNC=["MEX2", "SAX", "AMX"], GNP=["CBX", "GAS"], HLY=["TA2", "ECX", "PSW"],
                SLT=["RVX", "SAF"], MRW=["MRV", "CLX"])


def finish(w, seed=SEED):
    rng = np.random.default_rng(seed + 31)
    calls = w["calls"]
    for code in CODES:
        seq = 0
        occupied = {b: [] for b in BERTHS[code]}
        for c in [c for c in calls if c.term == code]:
            seq += 1
            yy = local(c.t0).year % 100
            c.visit = ("%s%02d%04d" % (code, yy, seq)) if TERM[code]["water"] == "harbor" else (
                "%s-%d-%03d" % (code, local(c.t0).year, seq))
            c.seq = seq
            a, b = c.first - c.arr_lag - H, c.sail + c.letgo_lag + H
            order = BERTHS[code][:2] if c.large else BERTHS[code][::-1]
            for bth in order + BERTHS[code]:
                if all(not (x < b and y > a) for x, y in occupied[bth]):
                    c.berth = bth
                    occupied[bth].append((a, b))
                    break
            if c.berth is None:
                c.berth = order[0]
            teu = c.vessel["teu"]
            c.nbays = int(np.clip(round(teu / 1000 + 7 + rng.uniform(-1, 1)), 16, 25)) if c.large else int(
                np.clip(round(teu / 900 + 5 + rng.uniform(-1, 1)), 7, 16))
            assign_bays(c)
            if rng.random() < (0.45 if c.large else 0.3):
                wait = mins(rng.uniform(1.5, 30.0))
                transit = mins(rng.uniform(0.7, 1.4))
                end_a = c.first - c.arr_lag - transit
                c.anchor_before = (end_a - wait, end_a)
    w["maint"] = maintenance(w, seed)
    tune_ask_a(w, np.random.default_rng(seed + 61))
    w["labour"], w["oem"] = labour(w, seed)
    tune_ask_b(w, np.random.default_rng(seed + 62))
    w["ais"], w["outages"] = ais(w, seed)
    return w


def floor_min(t):
    return (int(t) // MIN) * MIN


def ask_a_truth(w):
    """Hours cranes stood out of service for breakdowns at each terminal over fiscal year 2026, at the minute the
    systems record: each crane's time out of service on any breakdown order (damage left out), a stop held on two
    orders at once counted once, each at the terminal where its crane stood."""
    tot = {code: 0.0 for code in CODES}
    per = {}
    for e in w["maint"]:
        if e["kind"] != "BD" or e.get("damage"):
            continue
        for a, b in e["periods"]:
            per.setdefault(e["crane"], []).append((floor_min(a), floor_min(b)))
    for cr, ps in per.items():
        for a, b in union(ps):
            tot[term_at(cr, a)] += max(0, min(b, FY1) - max(a, FY0)) / H
    return tot


def union(ps):
    out = []
    for a, b in sorted(ps):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def ask_b_truth(w):
    """Maintenance labor hours on cranes at each terminal over fiscal year 2026: every hour once (an engineer's day
    keyed into the ledger counts once), each at the terminal where the crane stood that day; a SRT job's hours
    fall on the day its crane went out of service, or the day it was raised."""
    tot = {code: 0.0 for code in CODES}
    d0, d1 = local(FY0).date(), local(FY1 - 1).date()
    for r in w["labour"]:
        e = r["ev"]
        if r["kind"] == "oem":
            continue
        if e["system"] == "legacy":
            s = e["periods"][0][0] if e["kind"] != "CM" else e["periods"][0][0] + e["reported_lag"]
            d = local(floor_min(s)).date()
        else:
            d = r["date"]
        if d0 <= d <= d1:
            tot[term_at(e["crane"], ts(d.year, d.month, d.day, 12))] += r["hours"]
    for o in w["oem"]:
        d = o["date"]
        if d0 <= d <= d1:
            tot[term_at(o["ev"]["crane"], ts(d.year, d.month, d.day, 12))] += o["hours"]
    return tot


def tune_ask_a(w, rng):
    """Each terminal's breakdown hours off the edge of its whole-hour cell: one stop found while the crane stood
    idle runs a few minutes longer."""
    for code in CODES:
        need = edge_need(ask_a_truth(w)[code], rng)
        if not need:
            continue
        k = int(round(need * 60)) * MIN
        for e in w["maint"]:
            if (e["kind"] == "BD" and e["src"] == "idle" and not e.get("damage") and e["term"] == code
                    and len(e["periods"]) == 1 and e["crane"] not in MOVES and e["system"] == "authority"
                    and FY0 + 10 * DAY < e["periods"][0][0] < FY1 - 10 * DAY):
                a, b = e["periods"][0]
                if any(a < x[0] < b + k + 2 * H for x in [p for f in w["maint"] if f["crane"] == e["crane"] and f is not e
                                                          for p in f["periods"]]):
                    continue
                if any(a < z < b + k + 30 * MIN for z in DST):
                    continue
                e["periods"][0] = (a, b + k)
                break
        v = ask_a_truth(w)[code]
        assert abs((v - np.floor(v)) - 0.5) >= 0.15 and int(round(v)) % 10 != 0, (code, v)


def tune_ask_b(w, rng):
    """Each terminal's labor hours off the edge of its cell: one technician's day on a planned job runs a quarter
    hour or more longer."""
    for code in CODES:
        v = ask_b_truth(w)[code]
        need = edge_need(v, rng)
        if not need:
            continue
        step = max(0.25, round(need * 4) / 4)
        for r in w["labour"]:
            e = r["ev"]
            if (r["kind"] == "own" and e["term"] == code and e["kind"] == "PM" and e["system"] == "authority"
                    and e["crane"] not in MOVES and local(FY0 + 20 * DAY).date() < r["date"] < local(FY1 - 20 * DAY).date()
                    and r["hours"] + step <= 12.0):
                r["hours"] += step
                break
        v = ask_b_truth(w)[code]
        assert abs((v - np.floor(v)) - 0.5) >= 0.15 and int(round(v)) % 10 != 0, (code, v)


def assign_bays(c):
    n = [len(r.moves_w) for r in c.runs]
    tot = sum(n)
    share = [max(1, int(round(c.nbays * x / tot))) for x in n]
    while sum(share) > c.nbays:
        share[share.index(max(share))] -= 1
    while sum(share) < c.nbays:
        share[share.index(max(share))] += 1
    b = 0
    for r, k in zip(c.runs, share):
        r.bays = [4 * i + 2 for i in range(b, b + k)]
        b += k


FAULTS = {
    "SPRDR": ["Spreader twistlock not locking", "Spreader telescopic fault", "Spreader flipper hydraulic leak",
              "Spreader landed-pin sensor fault", "Spreader cable plug damaged", "Spreader 20/40 not extending"],
    "HOIST": ["Hoist brake overheating", "Hoist motor overcurrent trip", "Hoist encoder fault", "Hoist brake pads worn",
              "Hoist rope damaged", "Hoist gearbox oil pressure alarm"],
    "TROL": ["Trolley drive fault", "Trolley wheel bearing noise", "Trolley rope tension alarm", "Trolley brake fault"],
    "GANT": ["Gantry drive trip", "Gantry rail clamp fault", "Gantry anti-collision sensor fault", "Gantry brake fault"],
    "ELEC": ["Main cable reel fault", "Drive cabinet cooling fault", "PLC communication loss", "Festoon cable damage",
             "Earth fault on main supply", "Emergency stop circuit fault"],
    "BOOM": ["Boom hoist limit switch fault", "Boom latch fault", "Boom hoist brake fault"],
    "CAB": ["Operator joystick fault", "Cab camera system fault", "Cab HVAC failure"],
}
FAULT_MIX = dict(ORD=["SPRDR", "SPRDR", "ELEC", "ELEC", "GANT", "CAB", "TROL"],
                 PNC=["SPRDR", "HOIST", "ELEC", "TROL", "GANT", "SPRDR"],
                 GNP=["SPRDR", "ELEC", "HOIST", "GANT", "BOOM"],
                 HLY=["HOIST", "HOIST", "HOIST", "SPRDR", "ELEC", "TROL"],
                 SLT=["SPRDR", "ELEC", "HOIST", "GANT", "TROL"],
                 MRW=["SPRDR", "SPRDR", "ELEC", "GANT", "CAB", "HOIST"])


def move_gaps(w):
    """For each moved crane, its last working minute at the old terminal and its first at the new one."""
    out = {}
    for cr, (to, a, b) in MOVES.items():
        before = [r.end for c in w["calls"] for r in c.runs if r.crane == cr and r.start < a]
        after = [r.start for c in w["calls"] for r in c.runs if r.crane == cr and r.start >= b]
        out[cr] = (max(before), min(after))
    return out


def maintenance(w, seed):
    """Every crane's year in the maintenance systems: the breakdowns on its runs, breakdowns found while it stood idle,
    a few long repairs, planned maintenance, inspections, corrective jobs that took it out of nothing, the time a
    moved crane stood out of service for its move, and repeat failures that reopened an order."""
    rng = np.random.default_rng(seed + 57)
    calls = w["calls"]
    ev = []
    occupied = {}
    for c in calls:
        for r in c.runs:
            occupied.setdefault(r.crane, []).append((c.first - c.arr_lag - H, c.last + 2 * H) if c.large
                                                     else (r.start - 20 * MIN, r.end + 20 * MIN))
            for s, e in r.bk_clock():
                ev.append(dict(crane=r.crane, kind="BD", periods=[(s, e)], src="run", large=c.large))
    lo, hi = SPAN0 - 10 * DAY, SPAN1 + 6 * DAY
    for x in ev:
        occupied[x["crane"]].append(x["periods"][0])
    gaps = move_gaps(w)
    for cr, (to, a, b) in MOVES.items():
        occupied.setdefault(cr, []).append((gaps[cr][0] - 2 * DAY, gaps[cr][1] + 2 * DAY))
        ev.append(dict(crane=cr, kind="MOVE", periods=[(a, b)], src="move", large=False))

    def place(cr, dur, near=None, margin=H, tries=80, inside=None):
        for _ in range(tries):
            if near is None:
                t = int(rng.uniform(*(inside or (lo, hi))))
            else:
                t = int(near + rng.uniform(-4, 9) * DAY)
            t = (t // MIN) * MIN
            s, e = t, t + dur
            if s < lo or e > hi:
                continue
            if any(x < e + margin and y > s - margin for x, y in occupied.get(cr, ())):
                continue
            if any(s - 30 * MIN < z < e + 30 * MIN for z in DST):
                continue
            if cr in gaps and s < gaps[cr][1] + 2 * DAY and e > gaps[cr][0] - 2 * DAY:
                continue
            if abs(s - FY0) < 3 * DAY or abs(e - FY0) < 3 * DAY or abs(s - FY1) < 2 * DAY or abs(e - FY1) < 2 * DAY:
                continue
            occupied.setdefault(cr, []).append((s, e))
            return (s, e)
        return None

    for cname in sorted(CR):
        spec = CR[cname]
        busy_h = sum(e - s for s, e in occupied.get(cname, [])) / H
        idle_h = (hi - lo) / H - busy_h
        for _ in range(rng.poisson(IDLE_LAM * idle_h)):
            pr = place(cname, draw_repair(rng, spec))
            if pr:
                ev.append(dict(crane=cname, kind="BD", periods=[pr], src="idle", large=False))
        t = lo + int(rng.uniform(0, 28) * DAY)
        while t < hi:
            pr = place(cname, mins(rng.uniform(4.0, 9.0)), near=t)
            if pr:
                ev.append(dict(crane=cname, kind="PM", periods=[pr], src="plan", large=False))
            t += int(rng.uniform(27, 34) * DAY)
        for j in range(2):
            pr = place(cname, mins(rng.uniform(3.0, 6.0) if j else rng.uniform(7.0, 11.0)))
            if pr:
                ev.append(dict(crane=cname, kind="INSP", periods=[pr], src="annual" if j == 0 else "plan",
                               large=False))
        for _ in range(int(rng.integers(2, 5))):
            for _ in range(50):
                t = (int(rng.uniform(lo, hi)) // MIN) * MIN
                g = gaps.get(cname)
                if g and g[0] - 3 * DAY < t < g[1] + 2 * DAY:
                    continue
                if CR[cname]["tag"] and CUTOVER[0] - 3 * DAY < t < CUTOVER[1] + 2 * DAY:
                    continue
                if abs(t - FY0) < 3 * DAY or abs(t - FY1) < 3 * DAY:
                    continue
                ev.append(dict(crane=cname, kind="CM", periods=[(t, None)], src="plan", large=False))
                break
    majors = dict(ORD=3, PNC=2, GNP=2, HLY=3, SLT=2, MRW=3)
    for code, n in majors.items():
        pool = [c[0] for c in CRANES if c[13] == code and c[7] != "long"]
        for _ in range(n):
            for _ in range(30):
                cname = pool[int(rng.integers(len(pool)))]
                dur = mins(rng.uniform(28, 150))
                pr = place(cname, dur, near=int(rng.uniform(FY0 + 10 * DAY, FY1 - 20 * DAY)), margin=2 * H)
                if pr:
                    ev.append(dict(crane=cname, kind="BD", periods=[pr], src="major", large=False))
                    break
    # each moved crane has stops at its old terminal in the year before it moves
    for cname, (to, a, b) in MOVES.items():
        have = [x for x in ev if x["crane"] == cname and x["kind"] == "BD" and FY0 + 3 * DAY < x["periods"][0][0] < a]
        for _ in range(max(0, 3 - len(have))):
            pr = place(cname, mins(rng.uniform(2.0, 9.0)), inside=(FY0 + 5 * DAY, a - 3 * DAY))
            if pr:
                ev.append(dict(crane=cname, kind="BD", periods=[pr], src="idle", large=False))
    # repeat failures that reopened the order: back in service, then down again on the same fault
    reopen = dict(ORD=3, PNC=2, GNP=2, HLY=3, SLT=2, MRW=2)
    for code, n in reopen.items():
        cands = [x for x in ev if x["kind"] == "BD" and x["src"] in ("idle", "run") and not x["large"]
                 and term_at(x["crane"], x["periods"][0][0]) == code
                 and FY0 + 5 * DAY < x["periods"][0][0] < FY1 - 9 * DAY
                 and (TERM[code]["water"] == "harbor" or x["periods"][0][0] >= CUTOVER[1] + DAY)
                 and x["crane"] not in MOVES]
        rng.shuffle(cands)
        done = 0
        for x in cands:
            if done >= n:
                break
            s, e = x["periods"][0]
            cr = x["crane"]
            for _ in range(30):
                t3 = (int(e + rng.uniform(6, 40) * H) // MIN) * MIN
                d2 = mins(rng.uniform(0.6, 4.5))
                if any(p < t3 + d2 + H and q > t3 - H for p, q in occupied[cr]):
                    continue
                if any(t3 - 30 * MIN < z < t3 + d2 + 30 * MIN for z in DST):
                    continue
                occupied[cr].append((t3, t3 + d2))
                x["periods"].append((t3, t3 + d2))
                x["reopened"] = True
                done += 1
                break
    # orders raised as breakdowns and re-typed as damage once the cause was found
    dmg = dict(ORD=2, PNC=3, GNP=2, HLY=2, SLT=2, MRW=2)
    for code, n in dmg.items():
        cands = [x for x in ev if x["kind"] == "BD" and x["src"] in ("idle", "run") and not x["large"]
                 and not x.get("reopened") and term_at(x["crane"], x["periods"][0][0]) == code
                 and FY0 + 5 * DAY < x["periods"][0][0] < FY1 - 9 * DAY
                 and (TERM[code]["water"] == "harbor" or x["periods"][0][0] >= CUTOVER[1] + DAY)
                 and x["crane"] not in MOVES]
        cands.sort(key=lambda x: -(x["periods"][0][1] - x["periods"][0][0]))
        for x in cands[:n]:
            x["damage"] = True
    # a second fault found while the crane stood down for the first, raised as its own breakdown order and taking the
    # crane out of service on that order too: inside the first stop, or running on after it
    second = dict(ORD=4, PNC=3, GNP=2, HLY=3, SLT=2, MRW=4)
    for code, n in second.items():
        river = TERM[code]["water"] != "harbor"
        cands = [x for x in ev if x["kind"] == "BD" and x["src"] in ("idle", "major") and not x.get("damage")
                 and not x.get("reopened") and len(x["periods"]) == 1 and x["crane"] not in MOVES
                 and term_at(x["crane"], x["periods"][0][0]) == code
                 and FY0 + 8 * DAY < x["periods"][0][0] < FY1 - 12 * DAY
                 and x["periods"][0][1] - x["periods"][0][0] >= 3 * H
                 and (not river or x["periods"][0][1] < CUTOVER[0] - 3 * DAY or x["periods"][0][0] > CUTOVER[1] + DAY)]
        cands.sort(key=lambda x: (x["periods"][0][0], x["crane"]))
        rng.shuffle(cands)
        done = 0
        for x in cands:
            if done >= n:
                break
            a, b = x["periods"][0]
            cr = x["crane"]
            s2 = floor_min(a + rng.uniform(0.2, 0.55) * (b - a))
            if done % 2 == 0:
                e2 = floor_min(b - rng.uniform(0.15, 0.4) * (b - s2))
            else:
                e2 = floor_min(b + rng.uniform(0.6, 3.2) * H)
                if any(p < e2 + H and q > b for p, q in occupied[cr] if (p, q) != (a, b)):
                    continue
                if any(b - 30 * MIN < z < e2 + 30 * MIN for z in DST):
                    continue
                occupied[cr].append((b, e2))
            if e2 - s2 < H:
                continue
            ev.append(dict(crane=cr, kind="BD", periods=[(s2, e2)], src="second", large=False, inside=e2 <= b))
            x["has_second"] = True
            done += 1
        assert done == n, (code, done)
    for x in ev:
        s0 = x["periods"][0][0]
        x["term"] = term_at(x["crane"], s0)
        water = TERM[x["term"]]["water"]
        if water == "harbor":
            x["system"] = "authority"
        elif s0 < CUTOVER[0]:
            x["system"] = "legacy"
        elif s0 < CUTOVER[1]:
            x["system"] = "both"
        else:
            x["system"] = "authority"
    ev.sort(key=lambda x: (x["periods"][0][0], x["crane"]))
    for i, x in enumerate(ev):
        x["fault"] = None
        if x["kind"] == "BD":
            fam = FAULT_MIX[x["term"]][int(rng.integers(len(FAULT_MIX[x["term"]])))]
            if x["src"] == "major":
                fam = ["HOIST", "GANT", "ELEC", "BOOM", "TROL"][int(rng.integers(5))]
            x["fault"] = fam
            x["text"] = FAULTS[fam][int(rng.integers(len(FAULTS[fam])))]
        x["reported_lag"] = int(rng.uniform(0, 7)) * MIN
        x["labour_lag"] = (int(rng.uniform(5, 40)) * MIN, int(rng.uniform(5, 25)) * MIN)
        x["closed_lag"] = int(rng.uniform(1, 12) * DAY)
        x["seq"] = i
    return ev


# ---------------------------------------------------------------------------------------------- labour
TECHS = dict(ORD=[("41027", "MECH"), ("41033", "MECH"), ("41058", "ELEC"), ("41062", "ELEC"), ("41071", "MECH"),
                  ("41104", "RIG")],
             PNC=[("42011", "MECH"), ("42019", "ELEC"), ("42026", "MECH"), ("42044", "ELEC"), ("42051", "MECH")],
             GNP=[("43008", "MECH"), ("43015", "ELEC"), ("43022", "MECH"), ("43037", "WELD")],
             HLY=[("44003", "MECH"), ("44012", "MECH"), ("44020", "ELEC"), ("44031", "ELEC"), ("44046", "RIG")],
             SLT=[("46014", "MECH"), ("46021", "ELEC"), ("46029", "MECH"), ("46035", "ELEC")],
             MRW=[("47006", "MECH"), ("47013", "ELEC"), ("47018", "MECH"), ("47024", "ELEC"), ("47030", "WELD")])
OEM = {"ZPMC": ("ZPMC", ["Todd Nguyen", "Michael Ramos", "Susan Maxwell"]),
       "Liebherr": ("Liebherr", ["Stephanie Brown", "Samuel Whitaker", "Cameron Salas"]),
       "Konecranes": ("Konecranes", ["Kevin Cooper", "Zachary Patton"]),
       "Kalmar": ("Kalmar", ["Sandra Harrison", "Jacob Cantu"]),
       "Mitsubishi": ("Mitsubishi", ["Matthew Jenkins", "David Duarte"]),
       "Paceco": ("Atlantic Portainer Services", ["William Thomas", "Ernest Medina"])}


def labour(w, seed):
    """Every hour booked to a crane order: the Authority's own technicians and resident contractors in the labour
    ledger (river jobs before the cut-over in SRT's log, as one total per job), and the crane makers'
    field-service engineers on their own signed timesheets; on the visits where an engineer worked beside the
    Authority's crew the planner also keyed the engineer's hours into the ledger."""
    rng = np.random.default_rng(seed + 91)
    lab, oem = [], []
    # the planner keys a maker's visit from its service report, one line per report on the visit's first day; at
    # each terminal the first maker's visit of two days or more in the Authority's system is one the planner keyed
    first_long = {}
    for x in w["maint"]:
        mk = CR[x["crane"]]["make"]
        long_ = (x["kind"] == "BD" and x["src"] == "major") or (
            x["kind"] == "INSP" and x["src"] == "annual" and mk in ("ZPMC", "Liebherr", "Konecranes", "Kalmar"))
        s0 = x["periods"][0][0]
        term = term_at(x["crane"], s0)
        river = TERM[term]["water"] != "harbor"
        if long_ and x["crane"] not in MOVES and FY0 + 20 * DAY < s0 < FY1 - 20 * DAY and (not river or s0 > CUTOVER[1]):
            first_long.setdefault(term, x)
    forced = {id(x) for x in first_long.values()}
    for x in w["maint"]:
        if x["kind"] == "MOVE":
            continue
        per = x["periods"]
        s = per[0][0]
        crew = []
        if x["kind"] == "CM":
            hrs = [round(rng.uniform(1.0, 5.0) * 4) / 4 for _ in range(int(rng.integers(1, 3)))]
            d = local(s + int(rng.uniform(1, 30) * H)).date()
            crew = [(d, h) for h in hrs]
        else:
            for a, b in per:
                dur = (b - a) / H
                ncrew = 1 if dur < 1.5 else (2 if dur < 8 else int(rng.integers(2, 4)))
                if x["kind"] in ("PM", "INSP"):
                    ncrew = 2
                if x["src"] == "major":
                    ncrew = int(rng.integers(2, 4))
                t = a
                while t < b:
                    dend = int(dt.datetime.combine(local(t).date() + dt.timedelta(days=1), dt.time(0), ET).timestamp())
                    seg = (min(b, dend) - t) / H
                    if seg >= 0.25:
                        for _ in range(ncrew):
                            hh = min(seg * rng.uniform(0.6, 1.0), 12.0)
                            h = max(0.5, round(hh * 4) / 4)
                            crew.append((local(t).date(), h))
                    t = dend
        techs = TECHS[x["term"]]
        rows = []
        for i, (d, h) in enumerate(crew):
            ot = "OT15" if (rng.random() < 0.12) else ""
            used = {r["code"] for r in rows if r["date"] == d}
            free = [k for k in range(len(techs)) if techs[k][0] not in used]
            if not free:
                # the whole crew is already on the order that day: the hours go to one of them
                r = [r for r in rows if r["date"] == d][i % len(used)]
                r["hours"] = min(12.0, r["hours"] + h)
                continue
            code, craft = techs[free[(x["seq"] + i * 3) % len(free)]]
            rows.append(dict(date=d, code=code, craft=craft, hours=h, ot=ot, kind="own"))
        # resident contractors (electrical, structural, testing), always keyed
        contract = []
        if (x["kind"] in ("BD",) and x["src"] == "major") or (x["kind"] == "INSP" and x["src"] == "annual") or \
                (x.get("damage") and rng.random() < 0.6):
            for j in range(int(rng.integers(1, 3))):
                d = local(per[0][0] + int(rng.uniform(0, max((per[0][1] - per[0][0]) / H - 1, 1)) * H)).date()
                contract.append(dict(date=d, code="CONTRACT", craft="CONTRACT",
                                     hours=round(rng.uniform(3.0, 10.0) * 4) / 4, ot="", kind="contractor"))
        visits = []
        mk = CR[x["crane"]]["make"]
        if x["kind"] == "BD" and x["src"] == "major" and (rng.random() < 0.85 or id(x) in forced):
            visits.append(int(rng.integers(2 if id(x) in forced else 1, 4)))
        elif x["kind"] == "INSP" and x["src"] == "annual" and mk in ("ZPMC", "Liebherr", "Konecranes", "Kalmar"):
            visits.append(2 if (rng.random() < 0.5 or id(x) in forced) else 1)
        elif x["kind"] == "BD" and mk in ("ZPMC", "Liebherr", "Konecranes") and rng.random() < 0.10:
            visits.append(1)
        mv = MOVES.get(x["crane"])
        if mv and per[0][0] < mv[2]:
            visits = []
        x["oem_days"] = visits[0] if visits else 0
        if visits and x["system"] != "both":
            maker, engineers = OEM[mk]
            eng = engineers[int(rng.integers(len(engineers)))]
            keyed = x["system"] == "authority" and (rng.random() < 0.45 or id(x) in forced)
            day0 = local(per[0][0]).date()
            last = day0 + dt.timedelta(days=visits[0] - 1)
            if any(day0 < edge <= last for edge in (local(FY0).date(), local(FY1).date())):
                keyed = False
            days = []
            for k in range(visits[0]):
                d = day0 + dt.timedelta(days=k)
                h = round(rng.uniform(5.5, 11.5) * 4) / 4
                oem.append(dict(ev=x, maker=maker, engineer=eng, date=d, hours=h, keyed=keyed))
                days.append(h)
            if keyed:
                rows.append(dict(date=day0, code="CONTRACT", craft="CONTRACT", hours=sum(days), ot="", kind="oem"))
            if keyed and rng.random() < 0.6:
                contract.append(dict(date=day0, code="CONTRACT", craft="CONTRACT",
                                     hours=round(rng.uniform(2.0, 6.0) * 4) / 4, ot="", kind="contractor"))
        mine = {(o["date"], o["hours"]) for o in oem if o["ev"] is x}
        mine |= {(r["date"], r["hours"]) for r in rows if r["kind"] == "oem"}
        visit_days = {o["date"] for o in oem if o["ev"] is x}
        for r in contract:
            # resident contractors attend on the days the maker's engineer is not on site
            while r["date"] in visit_days:
                r["date"] += dt.timedelta(days=1)
            while (r["date"], r["hours"]) in mine:
                r["hours"] += 0.25
            rows.append(r)
        for r in rows:
            r["ev"] = x
        lab.extend(rows)
    return lab, oem


# ---------------------------------------------------------------------------------------------- AIS
OUTAGE_SALT = 8


def ais(w, seed):
    """The Authority's AIS berth pipeline: one row per stretch of reports with the ship stopped inside one berth or
    anchorage polygon, cut at midnight UTC and wherever the reports stop for more than an hour."""
    rng = np.random.default_rng(seed + 211 + OUTAGE_SALT)
    outs = {}
    edges = {"harbor": [], "river": []}
    for c in w["calls"]:
        for t in (c.first - c.arr_lag, c.sail + c.letgo_lag):
            edges[TERM[c.term]["water"]].append(t)
    for water, n in (("harbor", 16), ("river", 12)):
        lst = []
        while len(lst) < n:
            day = int(rng.uniform(SPAN0, SPAN1) // DAY) * DAY
            s = day + int(rng.uniform(1.0, 9.5) * H)
            e = s + mins(rng.uniform(1.5, 8.5))
            if any(s - 20 * MIN < t < e + 20 * MIN for t in edges[water]):
                continue
            lst.append((s, e))
        outs[water] = sorted(lst)
    segs = []
    srng = np.random.default_rng(seed + 212)

    def emit(v, mm, zone, a, b, water):
        cuts = []
        day = (a // DAY + 1) * DAY
        while day < b:
            cuts.append((day, day))
            day += DAY
        for s, e in outs[water]:
            if s < b and e > a:
                cuts.append((max(s, a), min(e, b)))
        if srng.random() < 0.05:
            g0 = int(srng.uniform(a + 2 * H, max(a + 2 * H + 1, b - 3 * H)))
            if g0 + 2 * H < b:
                cuts.append((g0, g0 + int(srng.uniform(62, 95)) * MIN))
        cuts.sort()
        pieces, t = [], a
        for s, e in cuts:
            if s > t:
                pieces.append((t, s))
            t = max(t, e)
        if t < b:
            pieces.append((t, b))
        for i, (s, e) in enumerate(pieces):
            s2 = s + int(srng.uniform(1, 59)) if i == 0 else s + int(srng.uniform(4, 178))
            e2 = e - int(srng.uniform(1, 59)) if i == len(pieces) - 1 else e - int(srng.uniform(4, 178))
            if e2 - s2 < 120 and 0 < i < len(pieces) - 1:
                continue
            if e2 <= s2:
                s2, e2 = s, e
            nrep = int((e2 - s2) / 180 * srng.uniform(0.95, 1.03)) + 1
            segs.append(dict(mmsi=mm, vessel=v, zone=zone, start=s2, end=e2, n=nrep))

    for c in w["calls"]:
        v = c.vessel
        water = TERM[c.term]["water"]
        anch = ANCHOR[water][int(srng.integers(len(ANCHOR[water])))]
        b0 = c.first - c.arr_lag
        b1 = c.sail + c.letgo_lag
        if c.anchor_before:
            emit(v, mmsi_on(v, c.anchor_before[0]), anch, c.anchor_before[0], c.anchor_before[1], water)
        emit(v, mmsi_on(v, b0), ZONE[c.berth], b0, b1, water)
    segs.sort(key=lambda x: (x["start"], x["mmsi"]))
    return segs, outs


# ---------------------------------------------------------------------------------------------- the counterfactual
def saving(c, w, how="gold"):
    """Hours by which a call, all fast to let go, would have been shorter had its cargo work taken four fifths of its
    time: the sailing re-allocated from the earlier readiness under the windows that bind the call."""
    cut = c.span / 5.0
    if how == "naive":
        return cut / H
    W = permitted(c, w["wins"], w["day"])
    if W is None:
        return cut / H
    return (c.sail - earliest(c.ready - cut, W)) / H


def build(seed=SEED):
    return finish(schedule(seed), seed)


def routes(c, w):
    """Each route's credit for one call (hours): the ladder's rungs and the hazards' misreadings."""
    cut = c.span / 5.0
    river = TERM[c.term]["water"] == "river"
    W = permitted(c, w["wins"], w["day"])
    out = dict(naive=cut / H, fifth_alongside=(c.sail + c.letgo_lag - c.first + c.arr_lag) / 5.0 / H)
    out["tide_zero"] = 0.0 if (river and c.gated) else cut / H
    out["gated_zero"] = 0.0 if c.gated else cut / H
    out["waited_zero"] = 0.0 if c.sail > c.ready else cut / H
    if W is None:
        g = cut / H
        for k in ("gold", "daylight_missed", "no_passage", "lst_clock", "ready_last"):
            out[k] = g
        return out
    out["gold"] = (c.sail - earliest(c.ready - cut, W)) / H
    out["daylight_missed"] = out["gold"] if river else cut / H
    if river:
        hw = W[:, 1] - WIN[1] + PASSAGE[c.term]
        Wn = np.stack([hw + WIN[0], hw + WIN[1]], axis=1)                  # the window applied at the berth
        out["no_passage"] = (c.sail - earliest(c.ready - cut, Wn)) / H
        dstw = (W[:, 0] >= DST[1]) | (W[:, 0] < DST[0])                    # standard time read as the clock
        Wl = W - np.where(dstw, H, 0)[:, None]
        out["lst_clock"] = (c.sail - earliest(c.ready - cut, Wl)) / H
    else:
        out["no_passage"] = out["lst_clock"] = out["gold"]
    out["ready_last"] = (c.sail - earliest(c.last - cut, W)) / H
    return out


if __name__ == "__main__":
    import sys
    x = schedule(int(sys.argv[1]) if len(sys.argv) > 1 else SEED)
    fy = [c for c in x["calls"] if c.large and c.in_fy]
    print("calls", {code: sum(1 for c in fy if c.term == code) for code in CODES})
    tot = {}
    for c in fy:
        for k, v in routes(c, x).items():
            tot.setdefault(k, {code: 0.0 for code in CODES})[c.term] += v
    for k, t in tot.items():
        r = sorted(t, key=lambda z: -t[z])
        print("%-16s" % k, "  ".join("%s %7.1f" % (z, t[z]) for z in r), "  lead %.2f" % (t[r[0]] / t[r[1]]))
