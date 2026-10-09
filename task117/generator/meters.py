"""The two deck charging panels: lighting, panel energy, monthly reads and the electricians' log.

The sub-meters keep Pacific Standard Time all year; the log records the time the meter displays.
"""
from __future__ import annotations

import itertools
import math
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from common import GRID_T0, NQ, PST, QH, TZ, daterange, last_weekday_of_month, sun_times
from world import BACKFED_POS, BACKFEED

PANELS = {"CP-N": "CCN", "CP-S": "CCS"}
LIGHT_KW = {"CP-N": 2.4, "CP-S": 2.1}
METER = {"CP-N": "SM-2231", "CP-S": "SM-2232"}
R0 = {"CP-N": 41206.3, "CP-S": 38917.8}
# reads are logged to the minute as the meter displays it; no read falls on a quarter-hour boundary
READ_CANDIDATES = [(h, m) for h in (6, 7, 8, 9) for m in range(60) if (6, 46) <= (h, m) <= (9, 29) and m % 15]
# the quarter-hour a read falls inside: all before the read, all after it, pro rata, or the read moved to the nearest
# quarter-hour boundary
SPLITS = ("qb", "qa", "lin", "qn")


def meter_instant(d: date, h: int, m: int) -> int:
    """True instant of a read logged at meter time h:m on date d (meter on PST all year)."""
    return int(datetime(d.year, d.month, d.day, h, m, tzinfo=PST).timestamp())


def civil_misread(d: date, h: int, m: int) -> int:
    """The instant a reader gets by taking the logged time as local civil time."""
    return int(datetime(d.year, d.month, d.day, h, m, tzinfo=TZ).timestamp())


class Lighting:
    """Roof-level pole lights on a photocell: on at dusk, off at dawn, the switching times drifting
    with the weather. Holds each evening's on and off instants and the kWh per grid quarter-hour."""

    def __init__(self, rng, panel: str):
        self.kw = LIGHT_KW[panel]
        self.on, self.off = {}, {}
        self.arr = np.zeros(NQ)
        for d in daterange(date(2023, 12, 25), date(2027, 1, 3)):
            rise, sset = sun_times(d)
            nrise, _ = sun_times(d + timedelta(days=1))
            self.on[d] = sset + float(np.clip(rng.normal(9, 6), -6, 26)) * 60
            self.off[d] = nrise - float(np.clip(rng.normal(11, 6), -5, 28)) * 60
            self._apply(d, +1)

    def _apply(self, d, sign):
        a, b = (self.on[d] - GRID_T0) / QH, (self.off[d] - GRID_T0) / QH
        i0, i1 = int(math.floor(a)), int(math.floor(b))
        if i0 >= NQ:
            return
        i1 = min(i1, NQ - 1)
        kw = self.kw * sign
        if i0 == i1:
            self.arr[i0] += kw * (b - a) * 0.25
            return
        self.arr[i0] += kw * (i0 + 1 - a) * 0.25
        self.arr[i0 + 1:i1] += kw * 0.25
        self.arr[i1] += kw * (b - i1) * 0.25

    def partial(self, a, b):
        """Exact lighting kWh in [a, b) for an interval inside one quarter-hour."""
        tot = 0.0
        for d in (local_day(a) - timedelta(days=1), local_day(a)):
            if d in self.on:
                lo, hi = max(a, self.on[d]), min(b, self.off[d])
                if hi > lo:
                    tot += self.kw * (hi - lo) / 3600.0
        return tot

    def shift_on(self, d, seconds):
        """Switch on earlier (seconds > 0) or later on the evening of d."""
        self._apply(d, -1)
        self.on[d] -= seconds
        self._apply(d, +1)


def local_day(t) -> date:
    return datetime.fromtimestamp(int(t), TZ).date()


def panel_of(led: pd.DataFrame) -> pd.Series:
    """Panel each true ledger row is fed from (None for units off the deck panels)."""
    d = led["day"]
    on_house = (led["position"] == BACKFED_POS) & (d >= BACKFEED[0]) & (d <= BACKFEED[1])
    out = pd.Series(None, index=led.index, dtype=object)
    out[(led["garage"] == "CCN") & ~on_house] = "CP-N"
    out[led["garage"] == "CCS"] = "CP-S"
    return out


def qh_index(t):
    return ((np.asarray(t, dtype=np.int64) - GRID_T0) // QH).astype(np.int64)


def panel_kwh(rd: pd.DataFrame, rows_panel: pd.Series) -> dict:
    """kWh per grid quarter-hour on each panel from the readings of the given ledger rows."""
    out = {}
    for panel in PANELS:
        keep = rows_panel.index[rows_panel == panel]
        r = rd[rd["lrow"].isin(keep)]
        arr = np.zeros(NQ)
        np.add.at(arr, qh_index(r["interval_start"]), r["kwh"].to_numpy())
        out[panel] = arr
    return out


def cum(arr):
    c = np.zeros(len(arr) + 1)
    c[1:] = np.cumsum(arr)
    return c


def span(c, a, b):
    """Energy in [a, b) for a cumulative array over grid quarter-hours; a, b on quarter-hour boundaries."""
    return c[(b - GRID_T0) // QH] - c[(a - GRID_T0) // QH]


# ------------------------------------------------------------------------------------- reads
READ_DATES = [date(2023, 12, 29)] + [last_weekday_of_month(y, m) for y in (2024, 2025, 2026) for m in range(1, 13)]
DEC31_2025 = (7, 38)
DEC31_2026_SOUTH = ((7, 34), (9, 52))   # first read (register misread), later read stands


def month_start(y, m):
    return int(datetime(y, m, 1, tzinfo=TZ).timestamp())


class PanelBooks:
    """Cumulative quarter-hour energy on each panel under each combination of the B1 mishandlings
    that act on sessions: rd (re-deliveries kept), bf (back-feed missed), dd (repeats over-deduped)."""

    def __init__(self, led: pd.DataFrame, rd: pd.DataFrame, light: dict):
        deck = led["garage"].isin(["CCN", "CCS"])
        sub = led[deck]
        true = sub["true_row"] & ~sub["redelivered"]
        p_true = panel_of(sub)
        p_deck = pd.Series(np.where(sub["garage"] == "CCN", "CP-N", "CP-S"), index=sub.index)
        # over-dedup: keep the first session per permit (or fleet card), unit and local day
        keyday = sub["permit_no"].where(sub["permit_no"] != "", sub["fleet_card"]) + "|" + \
            sub["station_id"].astype(str) + "|" + sub["day"].astype(str)
        order = sub.sort_values("start").index
        first = ~keyday.loc[order].duplicated(keep="first")
        keep_dd = pd.Series(False, index=sub.index)
        keep_dd.loc[first.index[first.to_numpy()]] = True
        self.lighting = light
        self.tune_rng = np.random.default_rng(2231)
        self.refresh_light()
        self.c = {}
        self.sess = {}
        rdd = rd[rd["lrow"].isin(sub.index)]
        for rdf, bf, dd in itertools.product((False, True), repeat=3):
            inc = (true | (sub["redelivered"] & rdf)) & sub["version"].ge(1)
            inc = inc & (sub["true_row"] | sub["redelivered"])
            if dd:
                inc = inc & keep_dd
            panel = p_deck if bf else p_true
            kwh = panel_kwh(rdd[rdd["lrow"].isin(inc.index[inc.to_numpy()])], panel.where(inc))
            self.c[(rdf, bf, dd)] = {p: cum(kwh[p]) for p in PANELS}
            for p in PANELS:
                rr = sub[inc & (panel == p)].sort_values("start")
                st = rr["start"].to_numpy(np.float64)
                en = rr["end_charge"].to_numpy(np.float64)
                self.sess[(rdf, bf, dd, p)] = (st, en, rr["rate"].to_numpy(np.float64), float((en - st).max()))
        gold = panel_kwh(rdd[rdd["lrow"].isin(true.index[true.to_numpy()])], p_true.where(true))
        self.gold_qh = gold

    def refresh_light(self):
        self.light_raw = {p: self.lighting[p].arr for p in PANELS}
        self.light = {p: cum(self.lighting[p].arr) for p in PANELS}

    def partial(self, panel, variant, q0, t):
        """Session kWh in [q0, t), q0 the start of the quarter-hour holding t, on the constant-draw model."""
        st, en, rate, maxdur = self.sess[(*variant, panel)]
        i0 = np.searchsorted(st, q0 - maxdur - 1.0)
        i1 = np.searchsorted(st, t)
        s, e, r = st[i0:i1], en[i0:i1], rate[i0:i1]
        lo = np.maximum(s, q0)
        hi = np.minimum(e, t)
        return float(np.sum(np.where(hi > lo, r * (hi - lo), 0.0)) / 3600.0)

    def energy_to(self, panel, t, variant=(False, False, False), split="exact"):
        """Session kWh through the panel from the grid start to instant t. Readings give every whole quarter-hour;
        the quarter-hour holding t is split by the split rule (exact: the sessions' own constant draw)."""
        c = self.c[variant][panel]
        q = int((t - GRID_T0) // QH)
        q0 = GRID_T0 + q * QH
        if t == q0 or split == "qa" or (split == "qn" and t - q0 < QH / 2):
            return float(c[q])
        if split == "qn":
            return float(c[q + 1])
        if split == "qb":
            return float(c[q + 1])
        if split == "lin":
            return float(c[q] + (t - q0) / QH * (c[q + 1] - c[q]))
        return float(c[q]) + self.partial(panel, variant, q0, t)

    def light_to(self, panel, t):
        q = int((t - GRID_T0) // QH)
        q0 = GRID_T0 + q * QH
        return float(self.light[panel][q]) + (self.lighting[panel].partial(q0, t) if t > q0 else 0.0)

    def sessions(self, panel, a, b, rdf=False, bf=False, dd=False, split="exact"):
        v = (rdf, bf, dd)
        return self.energy_to(panel, b, v, split) - self.energy_to(panel, a, v, split)


def register_at(books: PanelBooks, panel: str, t: int) -> float:
    """True register value at instant t, before display truncation."""
    return R0[panel] + books.energy_to(panel, t) + books.light_to(panel, t)


def displayed(x: float) -> float:
    return math.floor(x * 10 + 1e-9) / 10


def b1_values(books, panel, reads_true, reads_civil, k, regs, subset, first_reg=None, first_t=None):
    """Unaccounted kWh for 2026 reading k (1..12) under a subset of mishandlings."""
    a_t, b_t = reads_true[k - 1], reads_true[k]
    if "clk" in subset:
        a_t, b_t = reads_civil[k - 1], reads_civil[k]
    reg_a, reg_b = regs[k - 1], regs[k]
    if "first" in subset and first_reg is not None and k == 12:
        reg_b = first_reg
        b_t = first_t if "clk" not in subset else first_t
    if "cal" in subset:
        a_t, b_t = month_start(2026, k), month_start(2026 + (k == 12), 1 if k == 12 else k + 1)
    split = next((x for x in subset if x in SPLITS), "exact")
    s = books.sessions(panel, a_t, b_t, rdf="rd" in subset, bf="bf" in subset, dd="dd" in subset, split=split)
    return (reg_b - reg_a) - s


B1_MISHANDLINGS = ("clk", "rd", "bf", "dd", "cal", "first") + SPLITS


def b1_subsets(appl):
    """Every non-empty subset of the applicable mishandlings, at most one quarter-hour split rule."""
    out = []
    for r in range(1, len(appl) + 1):
        for sub in itertools.combinations(appl, r):
            if sum(x in SPLITS for x in sub) <= 1:
                out.append(sub)
    return out


def round_half(x):
    return math.floor(x + 0.5)


def straddle_ok(books: PanelBooks, panel: str, t: int) -> bool:
    """The quarter-hour a read falls inside sits below the panel's maximum on both sides of the read, so the
    maximum-demand register reads the same whichever reset period that quarter-hour is given to."""
    j = int((t - GRID_T0) // QH)
    if t == GRID_T0 + j * QH:
        return True
    w = 20 * 96
    q = 4 * (books.gold_qh[panel] + books.light_raw[panel])
    return bool(q[j] < q[max(0, j - w):j].max() - 1e-6 and q[j] < q[j + 1:j + 1 + w].max() - 1e-6)


def choose_read_times(rng, books: PanelBooks):
    """Meter-clock read times for every read of each meter, none on a quarter-hour (the two decks' meters are read on
    the same day, each at its own minute). The 2026 times are searched, panel by panel, so the meter clock moves
    readings 3 to 11 by at least 2 kWh, every split of the quarter-hour a read falls inside moves every reading, and
    every subset of mishandlings lands on a different whole kWh from the golden (at least 1.5 kWh away unless the
    subset carries the pro rata split, at least 0.76 kWh then)."""
    times = {}
    for d in READ_DATES:
        if d.year == 2026:
            continue
        for panel in PANELS:
            for _ in range(500):
                hmv = READ_CANDIDATES[int(rng.integers(len(READ_CANDIDATES)))]
                if straddle_ok(books, panel, meter_instant(d, *hmv)):
                    break
            else:
                raise AssertionError(("straddle", d, panel))
            times[(d, panel)] = hmv
    for panel in PANELS:
        times[(date(2025, 12, 31), panel)] = DEC31_2025
        assert straddle_ok(books, panel, meter_instant(date(2025, 12, 31), *DEC31_2025))
    assert straddle_ok(books, "CP-S", meter_instant(date(2026, 12, 31), *DEC31_2026_SOUTH[0]))
    reads26 = [d for d in READ_DATES if d.year == 2026]
    report = {k: {} for k in range(1, 13)}
    for panel in PANELS:
        orders = {k: [READ_CANDIDATES[i] for i in rng.permutation(len(READ_CANDIDATES))] for k in range(1, 13)}
        if panel == "CP-S":
            orders[12] = [DEC31_2026_SOUTH[1]]
        path = []

        def dfs(k, budget=[200000]):
            if k > 12:
                return True
            d, prev = reads26[k - 1], (reads26[k - 2] if k > 1 else date(2025, 12, 31))
            for hmv in orders[k]:
                budget[0] -= 1
                if budget[0] < 0:
                    return False
                times[(d, panel)] = hmv
                if not straddle_ok(books, panel, meter_instant(d, *hmv)):
                    continue
                ok, info = check_reading(books, times, prev, d, k, panel, bin_test=False)
                if ok:
                    path.append(hmv)
                    if dfs(k + 1):
                        return True
                    path.pop()
            times.pop((d, panel), None)
            return False
        assert dfs(1), ("no read-time path", panel)
    # put every 2026 golden off a whole kWh and inside its bin by moving one evening's switch-on inside the span;
    # the registers display to 0.1 kWh, so the trim is repeated until the golden lands
    for panel in PANELS:
        prev = date(2025, 12, 31)
        for k, d in enumerate(reads26, start=1):
            tt, _ = read_pair(times, prev, d, panel)
            for attempt in range(25):
                regs = {k - 1: displayed(register_at(books, panel, tt[0])), k: displayed(register_at(books, panel, tt[1]))}
                gold = b1_values(books, panel, {k - 1: tt[0], k: tt[1]}, {k - 1: tt[0], k: tt[1]}, k, regs, ())
                frac = gold - math.floor(gold)
                if 0.07 <= frac <= 0.23 or 0.77 <= frac <= 0.93:
                    break
                target = float(books.tune_rng.uniform(0.11, 0.19))
                target = target if frac < 0.5 else 1 - target
                evening = prev + timedelta(days=12 + attempt % 9)
                books.lighting[panel].shift_on(evening, (target - frac) / books.lighting[panel].kw * 3600)
                books.refresh_light()
            else:
                raise AssertionError(("lighting trim", k, panel, gold))
            prev = d
    for panel in PANELS:
        prev = date(2025, 12, 31)
        for k, d in enumerate(reads26, start=1):
            ok, info = check_reading(books, times, prev, d, k, panel, bin_test=True)
            assert ok, (k, d, panel, info)
            assert straddle_ok(books, panel, meter_instant(d, *times[(d, panel)]))
            report[k][panel] = info
            prev = d
    return times, report


def read_pair(times, prev, d, panel):
    tt = (meter_instant(prev, *times[(prev, panel)]), meter_instant(d, *times[(d, panel)]))
    tc = (civil_misread(prev, *times[(prev, panel)]), civil_misread(d, *times[(d, panel)]))
    return tt, tc


def check_reading(books, times, prev, d, k, panel, bin_test=True):
    tt, tc = read_pair(times, prev, d, panel)
    regs = {k - 1: displayed(register_at(books, panel, tt[0])), k: displayed(register_at(books, panel, tt[1]))}
    rt = {k - 1: tt[0], k: tt[1]}
    rc = {k - 1: tc[0], k: tc[1]}
    first_reg = first_t = None
    if panel == "CP-S" and k == 12:
        first_t = meter_instant(d, *DEC31_2026_SOUTH[0])
        first_reg = misread(displayed(register_at(books, panel, first_t)))
    gold = b1_values(books, panel, rt, rc, k, regs, ())
    frac = gold - math.floor(gold)
    if bin_test and not (0.06 <= frac <= 0.24 or 0.76 <= frac <= 0.94):
        return False, ("bin", panel, gold)
    appl = ["rd", "bf", "dd", "cal"] + (["clk"] if 3 <= k <= 11 else []) + (["first"] if first_reg else []) \
        + list(SPLITS)
    worst = 99.0
    for sub in b1_subsets(appl):
        v = b1_values(books, panel, rt, rc, k, regs, sub, first_reg, first_t)
        dv = abs(v - gold)
        if dv < 1e-9:
            if not set(sub) <= {"rd", "bf", "dd", "first"}:
                return False, ("inert", panel, sub)
            continue
        worst = min(worst, dv)
        lim = 0.76 if "lin" in sub else 1.5
        if dv < lim or (bin_test and round_half(v) == round_half(gold)):
            return False, ("near", panel, sub, v - gold)
    if 3 <= k <= 11:
        clk = b1_values(books, panel, rt, rc, k, regs, ("clk",))
        if abs(clk - gold) < 2.0:
            return False, ("clk", panel, clk - gold)
    splits = {x: b1_values(books, panel, rt, rc, k, regs, (x,)) - gold for x in SPLITS}
    return True, {"golden": gold, "nearest_wrong": worst, "splits": splits}


CONFUSED = {"0": "8", "1": "7", "2": "7", "3": "8", "4": "9", "5": "6", "6": "8", "7": "9", "8": "9"}


def misread(reg: float) -> float:
    """The first 31 December reading as written: the hundreds digit read as a digit it is often mistaken for."""
    whole, frac = f"{reg:.1f}".split(".")
    d = list(whole)
    for i in (len(d) - 3, len(d) - 4):
        if d[i] in CONFUSED:
            d[i] = CONFUSED[d[i]]
            return float("".join(d) + "." + frac)
    raise ValueError(reg)


def build_log(books: PanelBooks, times: dict, rng) -> pd.DataFrame:
    rows = []
    readers = ["AC", "AC", "AC", "RM", "AC", "RM"]
    for j, d in enumerate(READ_DATES):
        for panel in PANELS:
            t = meter_instant(d, *times[(d, panel)])
            prev_t = meter_instant(READ_DATES[j - 1], *times[(READ_DATES[j - 1], panel)]) if j else None
            by = readers[int(rng.integers(len(readers)))]
            if panel == "CP-S" and d == date(2026, 12, 31):
                t1 = meter_instant(d, *DEC31_2026_SOUTH[0])
                qd1 = demand_max(books, panel, prev_t, t1)
                rows.append({"read_date": d, "read_time": "%02d:%02d" % DEC31_2026_SOUTH[0], "meter": METER[panel],
                             "panel": panel, "kwh": misread(displayed(register_at(books, panel, t1))),
                             "max_kw": qd1, "reset": "Y", "by": "RM"})
                qd2 = demand_max(books, panel, t1, t)
                rows.append({"read_date": d, "read_time": "%02d:%02d" % times[(d, panel)], "meter": METER[panel],
                             "panel": panel, "kwh": displayed(register_at(books, panel, t)), "max_kw": qd2,
                             "reset": "Y", "by": "AC"})
                continue
            qd = demand_max(books, panel, prev_t, t) if prev_t else None
            rows.append({"read_date": d, "read_time": "%02d:%02d" % times[(d, panel)], "meter": METER[panel],
                         "panel": panel, "kwh": displayed(register_at(books, panel, t)), "max_kw": qd, "reset": "Y",
                         "by": by})
    return pd.DataFrame(rows)


def demand_max(books, panel, a, b):
    i0, i1 = (a - GRID_T0) // QH, (b - GRID_T0) // QH
    q = 4 * (books.gold_qh[panel][i0:i1] + books.light_raw[panel][i0:i1])
    return round(float(q.max()) + 1e-9, 1)
