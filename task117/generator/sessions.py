"""Session generation: background, constructed days, devices.

Every session is a constant-draw block from plug-in until its delivered energy is reached, then
connected with no draw until plug-out. The closed draw is min(unit rating, vehicle onboard rating),
which on every 6.6 kW unit is 6.6 kW because every vehicle in the fiction accepts at least 6.6 kW.
"""
from __future__ import annotations

import itertools
import math
from datetime import date, timedelta

import numpy as np
import pandas as pd

from common import CITY_HOLIDAYS, HOLIDAYS, daterange, last_weekday_of_month, lt_date
from world import (BACKFED_POS, BACKFEED, DECKS, GATEWAY_B_END, GATEWAY_B_POS, MIGRATION, N_UNITS, POS_PREFIX,
                   REISSUE, REISSUED_POS, RESTATED_POS)

H = 3600.0
SNAP = 36  # plug-in seconds are multiples of 36, so a first partial quarter-hour is exact at 0.001 kWh


def hm(h, m=0, s=0):
    return h + m / 60 + s / 3600


def snap(t):
    return int(SNAP * round(t / SNAP))


# --- the 2026 binding days: (date, North 7.2 kept, North 7.2 renewed, North 7.7, South 7.2, South 7.7, South 11.0
# finished before noon, South 11.0 still charging at noon). "Kept" North pool cars stay on their permits into 2027;
# "renewed" ones are the 2020 Bolt EVs the county replaced with 2023 Bolt EVs at the January 2027 renewal.
PEAK_2026 = {
    1: (date(2026, 1, 21), 8, 2, 0, 4, 0, 6, 1),
    2: (date(2026, 2, 17), 0, 10, 4, 2, 2, 6, 0),
    3: (date(2026, 3, 12), 7, 2, 1, 3, 1, 7, 0),
    4: (date(2026, 4, 14), 5, 3, 2, 1, 0, 8, 2),
    5: (date(2026, 5, 20), 7, 3, 0, 2, 0, 8, 1),
    6: (date(2026, 6, 18), 3, 3, 2, 1, 2, 5, 1),
    7: (date(2026, 7, 15), 1, 2, 4, 0, 2, 5, 1),
    8: (date(2026, 8, 11), 5, 3, 2, 0, 2, 9, 0),
    9: (date(2026, 9, 16), 2, 4, 3, 3, 1, 5, 1),
    10: (date(2026, 10, 13), 4, 4, 2, 4, 0, 6, 1),
    11: (date(2026, 11, 18), 5, 2, 3, 2, 1, 7, 1),
    12: (date(2026, 12, 8), 6, 0, 4, 1, 3, 5, 1),
}
# the binding days that carry a 7.2 kW car finishing between 12:20 and 12:27, so 12:15 sits below 12:00
EARLY_MONTHS = (2, 12)
RUNG2_DAY = date(2026, 6, 10)
RUNG2_SPEC = {"CCN": [7.2, 7.2, 7.2, 7.2], "CCS": [11.0, 11.0, 7.2, 7.7]}

# --- kW each device session adds to the 12:00 quarter-hour on the back-test days (it ends inside that
# quarter-hour; 0.004 kW resolution keeps every reading exact at 0.001 kWh)
P_R24 = 0.88    # reissued-identifier unit, 2024
P_G24 = 0.66    # gateway B unit, January to April 2024
P_R25 = 2.20    # reissued-identifier unit, January to March 2025
P_V2 = 1.76     # restated unit, accepted version; version 1 is 0.88 lower, version 3 0.88 higher
P_D25 = 0.88    # session re-delivered in the October and December 2025 batches
P_F = 0.70      # fleet-card top-up on every back-test day (before April 2025 it settled outside the export)
B3_LEVELS_24 = {1: 15, 2: 16, 3: 14, 4: 13, 5: 12, 6: 11, 7: 11, 8: 11, 9: 13, 10: 14, 11: 15, 12: 15}
B3_BANDS = {1: (-1.6, -0.4), 2: (1.5, 2.9), 3: (-2.2, -0.8), 4: (0.8, 2.2), 5: (-1.2, -0.2), 6: (1.6, 2.9),
            7: (-2.0, -0.6), 8: (1.0, 2.4), 9: (-2.2, -0.9), 10: (1.2, 2.7), 11: (0.6, 1.8), 12: (-1.2, -0.2)}
FACTOR_2025 = 1.08
B3_MEAN_GUARD = 2.0   # every subset of mishandlings keeps the naive mean miss inside this many points

OCC = {1: 0.90, 2: 0.91, 3: 0.88, 4: 0.86, 5: 0.84, 6: 0.80, 7: 0.76, 8: 0.77, 9: 0.84, 10: 0.87, 11: 0.89, 12: 0.85}
PUBLIC_RATE = {"LIB": 1.5, "FTG": 2.1, "MSG": 1.8, "CSG": 1.3, "SWG": 1.2, "ETG": 1.7}
D0, D1 = date(2024, 1, 1), date(2026, 12, 31)


def _frac_ok(x, lo=0.06, hi=0.24):
    f = x - math.floor(x)
    return lo <= f <= hi or 1 - hi <= f <= 1 - lo


def b3_misses(sel, sub=()):
    """Misses on the filed path (stated whole-kW forecast against recorded whole-kW demand) under a subset
    of mishandlings: F the fleet-card sessions that settled outside the export before April 2025 left out,
    Fx every fleet-card transaction added (so the ones the export already carries count twice), D7 raw
    identifier join, H6 gateway B left out, H2 the 1.09 revision, H3l/H3f the latest or first restated
    version, H1 re-deliveries kept."""
    out = {}
    for m, p in sel.items():
        base, A, fac = p["base"], p["A"], 1.09 if "H2" in sub else FACTOR_2025
        if "F" in sub:
            base -= P_F
            if m <= 3:
                A -= P_F
        if "Fx" in sub and m >= 4:
            A += P_F
        if "D7" in sub:
            base -= P_R24
            if m <= 3:
                A -= P_R25
        if "H6" in sub and m <= 4:
            base -= P_G24
        if "H3l" in sub and m in (5, 6, 7):
            A += 0.88
        if "H3f" in sub and m in (5, 6, 7):
            A -= 0.88
        if "H1" in sub and m in (10, 12):
            A += P_D25
        NF, NA = int(math.floor(fac * base + 0.5)), int(math.floor(A + 0.5))
        out[m] = (NF, NA, 100 * (NF - NA) / NA)
    return out


B3_DEVICES = ("F", "Fx", "D7", "H6", "H2", "H3l", "H3f", "H1")
B3_SUBSETS = [s for k in range(1, len(B3_DEVICES) + 1) for s in itertools.combinations(B3_DEVICES, k)
              if not ("H3l" in s and "H3f" in s) and not ("F" in s and "Fx" in s)]


def choose_b3_parameters():
    """Seeded search for the back-test days. Every 2024 base times 1.08 and every 2025 actual sits at a
    non-round position inside its whole-kW bin (0.06 to 0.24 kW from a whole kW), every miss on the filed
    path is at least 0.015 points inside its one-decimal bin, six months over and six under, and under every
    subset of mishandlings the misses stay two-signed with a mean inside +-2.0 points."""
    rng = np.random.default_rng(31117)
    grid = np.round(np.arange(0.4, 6.2, 0.004), 3)
    options = {}
    for m in range(1, 13):
        dev24 = P_R24 + P_F + (P_G24 if m <= 4 else 0.0)
        hi = 0.20 if m <= 4 else 0.24
        lo_b, hi_b = B3_BANDS[m]
        opts = []
        for n24 in [n for n in (B3_LEVELS_24[m], B3_LEVELS_24[m] + 1) if n <= 16]:
            for p24 in grid:
                base = round(6.6 * n24 + p24 + dev24, 3)
                F = FACTOR_2025 * base
                if not _frac_ok(F, 0.06, hi):
                    continue
                NF = int(math.floor(F + 0.5))
                for NA in range(NF - 4, NF + 5):
                    miss = 100 * (NF - NA) / NA
                    if lo_b <= miss <= hi_b and 0.004 <= abs(miss - round(miss, 1)) <= 0.035:
                        opts.append((n24, float(p24), base, F, NF, NA, miss))
        assert opts, m
        options[m] = opts
    for attempt in range(20000):
        sel = {}
        for m in range(1, 13):
            n24, p24, base, F, NF, NA, miss = options[m][int(rng.integers(len(options[m])))]
            dev25 = P_F + (P_R25 if m <= 3 else P_V2 if m in (5, 6, 7) else P_D25 if m in (10, 12) else 0.0)
            delta = float(rng.choice([-1, 1]) * rng.uniform(0.07, 0.23))
            A = round(round((NA + delta) / 0.004) * 0.004, 3)
            n25 = None
            for k in [k for k in (n24 + 1, n24, n24 + 2, n24 - 1) if k <= 17]:
                p25 = round(A - 6.6 * k - dev25, 3)
                if 0.4 <= p25 <= 6.2:
                    n25 = k
                    break
            if n25 is None or not _frac_ok(A):
                break
            sel[m] = {"n24": n24, "p24": p24, "base": base, "F": F, "n25": n25, "p25": p25, "A": A, "NF": NF,
                      "NA": NA, "miss": miss}
        if len(sel) < 12:
            continue
        if len({p["base"] for p in sel.values()}) < 12 or len({p["A"] for p in sel.values()}) < 12:
            continue
        ok = True
        for sub in B3_SUBSETS:
            v = [x[2] for x in b3_misses(sel, sub).values()]
            if abs(sum(v) / 12) > B3_MEAN_GUARD or min(v) >= 0 or max(v) <= 0:
                ok = False
                break
        # the primary device, the fleet-card charges outside the export, moves every forecast and every miss
        g, f = b3_misses(sel), b3_misses(sel, ("F",))
        if ok and all(f[m][0] != g[m][0] and round(f[m][2], 1) != round(g[m][2], 1) for m in range(1, 13)):
            return sel
    raise RuntimeError("no back-test configuration")


def pick_day(rng, y, m, avoid):
    last = date(y, m, 18) if (y, m) == (2024, 4) else date(y, m, 23)  # April 2024: before the gateway B retirement
    cands = [d for d in daterange(date(y, m, 8), last)
             if d.weekday() in (1, 2, 3) and d not in CITY_HOLIDAYS and d not in avoid]
    return cands[int(rng.integers(len(cands)))]


def plan_calendar(rng):
    cal = {}
    for m, spec in PEAK_2026.items():
        cal[spec[0]] = ("bind", m)
    cal[RUNG2_DAY] = ("rung2", 6)
    reads = {last_weekday_of_month(y, m) for y in (2024, 2025, 2026) for m in range(1, 13)}
    reads.add(date(2023, 12, 29))
    taken = set(cal) | reads
    for y in (2024, 2025):
        for m in range(1, 13):
            d = pick_day(rng, y, m, taken)
            cal[d] = ("b3", (y, m))
            taken.add(d)
    for y in (2024, 2025, 2026):
        for m in (1, 2, 3, 10, 11, 12):
            for _ in range(2 if y == 2026 else 1):
                cands = [d for d in daterange(date(y, m, 2), date(y, m, 27))
                         if d.weekday() < 5 and d not in CITY_HOLIDAYS and d not in taken]
                d = cands[int(rng.integers(len(cands)))]
                cal[d] = ("full", m)
                taken.add(d)
    return cal, reads


def blocked(deck, d):
    """Units that host no morning session on d: the North unit fed from the house panel."""
    if deck == "CCN" and BACKFEED[0] <= d <= BACKFEED[1]:
        return {BACKFED_POS}
    return set()


class Generator:
    def __init__(self, rng: np.random.Generator, pos: pd.DataFrame, veh: dict):
        self.rng = rng
        self.pos = pos
        self.pveh = veh["pveh"]
        self.fleet = veh["fleet"]
        self.permit_deck = veh["permits"].set_index("permit_no")["deck"].to_dict()
        self.changed = set(veh["changed_2027"])
        self._active_cache = {}
        self.rows = []
        self.fleet_busy = {c: [] for c in self.fleet["fleet_card"]}

    def fleet_free(self, card, t0, t1):
        return all(t1 + 1800 <= a or t0 >= b + 1800 for a, b in self.fleet_busy[card])

    # ------------------------------------------------------------------ book keeping
    def add(self, **kw):
        kw.setdefault("role", "bg")
        kw.setdefault("permit_no", "")
        kw.setdefault("fleet_card", "")
        kw.setdefault("car_kw", np.nan)
        start = kw["start"]
        assert start % SNAP == 0, kw
        e_end = start + kw["energy"] / kw["rate"] * H
        assert kw["plug_out"] >= e_end + 300, ("plug-out before delivery", kw)
        kw["end_charge"] = e_end
        if kw.get("fleet_card"):
            assert self.fleet_free(kw["fleet_card"], start, kw["plug_out"]), ("fleet unit double-booked", kw)
            self.fleet_busy[kw["fleet_card"]].append((start, kw["plug_out"]))
        self.rows.append(kw)
        return kw

    def frame(self):
        return pd.DataFrame(self.rows)

    # ------------------------------------------------------------------ permits by date
    def active(self, deck: str, d: date) -> pd.DataFrame:
        key = (deck, d)
        if key not in self._active_cache:
            dk = "North" if deck == "CCN" else "South"
            pv = self.pveh[(self.pveh["from"] <= d) & (self.pveh["to"] >= d)]
            pv = pv[pv["permit_no"].map(self.permit_deck) == dk]
            self._active_cache[key] = pv.reset_index(drop=True)
        return self._active_cache[key]

    def pick_permits(self, deck, d, k, exclude=(), kw=None, weights=False, pool=None):
        """pool: "renewed" keeps permits whose car the January 2027 renewal replaced, "kept" the others."""
        pv = self.active(deck, d)
        pv = pv[~pv["permit_no"].isin(list(exclude))]
        if kw is not None:
            pv = pv[pv["rating"] == kw]
        if pool == "renewed":
            pv = pv[pv["permit_no"].isin(self.changed)]
        elif pool == "kept":
            pv = pv[~pv["permit_no"].isin(self.changed)]
        k = min(k, len(pv))
        if k == 0:
            return []
        if weights and deck == "CCN":
            w = np.where(pv["rating"].to_numpy() == 7.7, 2.6, 1.0)
            idx = self.rng.choice(len(pv), size=k, replace=False, p=w / w.sum())
        else:
            idx = self.rng.choice(len(pv), size=k, replace=False)
        return pv.iloc[np.sort(idx)][["permit_no", "rating"]].values.tolist()

    def deck_positions(self, deck):
        p = POS_PREFIX[deck]
        return [f"{p}-{i:02d}" for i in range(1, N_UNITS[deck] + 1)]

    # ------------------------------------------------------------------ one deck session
    def add_deck(self, deck, d, position, t0h, energy, permit, car_kw, plug_out_h=None, role="bg", acct="PERMIT",
                 fleet_card=""):
        start = snap(lt_date(d) + t0h * H)
        energy = round(float(energy), 3)
        need = start + energy / 6.6 * H
        if plug_out_h is None:
            po = start + float(np.clip(self.rng.normal(8.6, 0.6), 6.8, 10.4)) * H
            po = max(po, start + energy / 7.2 * H + 2.15 * H, need + 1.6 * H)
        else:
            po = lt_date(d) + plug_out_h * H
        po = int(round(po))
        return self.add(garage=deck, position=position, start=start, energy=energy, rate=6.6, plug_out=po,
                        acct=acct, permit_no=permit, fleet_card=fleet_card, car_kw=car_kw, role=role, day=d)

    def commuter_energy(self):
        return float(np.clip(self.rng.lognormal(math.log(11.5), 0.36), 3.0, 21.0))

    def morning(self, deck, d, positions, end_by, exclude=(), role="fill"):
        """Ordinary morning sessions that finish charging by end_by at 6.6 kW."""
        chosen = self.pick_permits(deck, d, len(positions), exclude=exclude)
        out = []
        for position, (permit, kw) in zip(positions, chosen):
            t0 = float(np.clip(self.rng.normal(hm(7, 55), 0.4), hm(6, 40), hm(9, 0)))
            e = min(self.commuter_energy(), 6.6 * (end_by - t0) - 0.2)
            out.append(self.add_deck(deck, d, position, t0, max(e, 3.0), permit, kw, role=role))
        return out

    # ------------------------------------------------------------------ an ordinary deck day
    def deck_day(self, deck, d, occ, repeat=False, topup=False, blocked_pos=()):
        rng = self.rng
        positions = [p for p in self.deck_positions(deck) if p not in blocked_pos]
        if d.weekday() >= 5 or d in HOLIDAYS:
            n = int(rng.poisson(1.1))
            sel = list(rng.permutation(positions))[:n]
            for position, (permit, kw) in zip(sel, self.pick_permits(deck, d, n)):
                t0 = float(rng.uniform(hm(8, 30), hm(16, 30)))
                e = float(np.clip(rng.lognormal(math.log(8.5), 0.4), 2.5, 18.0))
                po = t0 + float(rng.uniform(e / 6.6 + 0.7, e / 6.6 + 3.5))
                self.add_deck(deck, d, position, t0, e, permit, kw, plug_out_h=po, role="wkend")
            return
        city_hol = d in CITY_HOLIDAYS
        p_occ = occ * (0.18 if city_hol else 0.55 if (d.month == 12 and d.day >= 22) or (d.month == 1 and d.day <= 2) else 1.0)
        occupied = [p for p in positions if rng.random() < p_occ]
        chosen = self.pick_permits(deck, d, len(occupied), weights=True)
        used = [c[0] for c in chosen]
        n_rep = 1 if repeat and len(occupied) > 3 else 0
        for j, (position, (permit, kw)) in enumerate(zip(occupied, chosen)):
            if j < n_rep:
                # unplugged before lunch and plugged back in on the same unit in the early afternoon
                t0 = float(rng.uniform(hm(7, 20), hm(8, 40)))
                e1 = min(self.commuter_energy(), 6.6 * (hm(10, 50) - t0))
                po1 = float(rng.uniform(hm(11, 5), hm(11, 50)))
                self.add_deck(deck, d, position, t0, max(e1, 3.0), permit, kw, plug_out_h=po1, role="repeat1")
                t1 = float(rng.uniform(hm(12, 25), hm(13, 40)))
                e2 = float(rng.uniform(2.4, 7.5))
                po2 = t1 + float(rng.uniform(3.0, 4.6))
                self.add_deck(deck, d, position, t1, e2, permit, kw, plug_out_h=po2, role="repeat2")
                continue
            t0 = float(np.clip(rng.normal(hm(8, 5), 0.5), hm(6, 30), hm(9, 40)))
            self.add_deck(deck, d, position, t0, self.commuter_energy(), permit, kw)
        free = [p for p in positions if p not in occupied]
        for bp in blocked_pos:
            # the unit on the temporary feed still serves afternoon arrivals
            if not city_hol and rng.random() < 0.8:
                pk = self.pick_permits(deck, d, 1, exclude=used)
                if pk:
                    permit, kw = pk[0]
                    used.append(permit)
                    t0 = float(rng.uniform(hm(11, 10), hm(14, 40)))
                    e = float(rng.uniform(5.0, 13.5))
                    po = t0 + float(rng.uniform(3.4, 5.2))
                    self.add_deck(deck, d, bp, t0, e, permit, kw, plug_out_h=po, role="late")
        if deck == "CCN" and d < GATEWAY_B_END:
            # the legacy gateway units carried permit charging only
            free_top = [p for p in free if p not in GATEWAY_B_POS]
        else:
            free_top = free
        if topup and free_top:
            position = free_top[int(rng.integers(len(free_top)))]
            free.remove(position)
            fl = self.fleet[self.fleet["department"].isin(["Facilities Maintenance", "Building Inspection"])
                            & (self.fleet["rating"] < 11.0)]
            f = fl.iloc[int(rng.integers(len(fl)))]
            t0 = float(rng.uniform(hm(9, 30), hm(10, 15)))
            e = float(rng.uniform(4.0, 8.5))
            po = t0 + float(rng.uniform(1.9, 3.2))
            if self.fleet_free(f["fleet_card"], lt_date(d) + t0 * H - 60, lt_date(d) + po * H + 60):
                self.add_deck(deck, d, position, t0, e, "", f["rating"], plug_out_h=po, role="topup", acct="FLEET",
                              fleet_card=f["fleet_card"])
        if free and not city_hol and rng.random() < 0.33:
            position = free[int(rng.integers(len(free)))]
            pk = self.pick_permits(deck, d, 1, exclude=used)
            if pk:
                permit, kw = pk[0]
                t0 = float(rng.uniform(hm(11, 0), hm(15, 30)))
                e = float(rng.uniform(4.0, 13.0))
                po = t0 + float(rng.uniform(3.2, 5.4))
                self.add_deck(deck, d, position, t0, e, permit, kw, plug_out_h=po, role="late")

    # ------------------------------------------------------------------ constructed 2026 binding day
    def long_session(self, kind, kw):
        """(t0 hours, energy) for a long session on a binding day.

        slow: still charging at 12:17 at its own draw and at 12:17 at 8.081 kW, finished by 11:56 at 9.75 kW.
        fast: finished by 11:42 at 11.0 kW and by 11:56 at 9.75 kW, still charging at 12:17 at 8.081 kW.
        early: a 7.2 kW car that finishes between 12:20 and 12:27 at its own draw, by 11:56 at 9.75 kW and by
        11:44 at 11.0 kW.
        longfast: an 11.0 kW car still charging at 12:17 at 11.5 kW and finished by 13:20 at it."""
        rng = self.rng
        for _ in range(5000):
            if kind == "early":
                E = float(rng.uniform(13.0, 16.0))
                end_r = float(rng.uniform(hm(12, 20), hm(12, 27)))
                t0 = end_r - E / kw
                # a renewed car draws 11.0 kW in the contract year: it must be done before the 11:45 quarter-hour
                if t0 + E / 9.75 > hm(11, 56) or t0 + E / 11.0 > hm(11, 44):
                    continue
            elif kind == "fast":
                E = float(rng.uniform(26.0, 38.0))
                lo = hm(12, 17) - E * (1 / 8.081 - 1 / 9.75)
                hi = min(hm(11, 56), hm(11, 42) + E * (1 / 9.75 - 1 / 11.0))
                if hi <= lo:
                    continue
                t0 = float(rng.uniform(lo, hi)) - E / 9.75
            elif kind == "longfast":
                E = float(rng.uniform(26.0, 40.0))
                t0 = float(rng.uniform(hm(12, 22), hm(13, 20))) - E / 11.5
            else:
                E = float(rng.uniform(24.0, 38.0))
                lo = hm(12, 17) - E * (1 / 8.081 - 1 / 9.75)
                hi = hm(11, 56)
                if hi <= lo:
                    continue
                t0 = float(rng.uniform(lo, hi)) - E / 9.75
            if hm(7, 40) <= t0 <= hm(10, 40):
                return t0, E
        raise RuntimeError(kind)

    def binding_day(self, d, k72, r72, n77, s72, s77, s110, s110l, early=False):
        north = [(7.2, k72, "kept"), (7.2, r72, "renewed"), (7.7, n77, None)]
        south = [(7.2, s72, None), (7.7, s77, None), (11.0, s110, None), (11.0, s110l, "longfast")]
        for deck, spec in (("CCN", north), ("CCS", south)):
            positions = list(self.rng.permutation([p for p in self.deck_positions(deck) if p not in blocked(deck, d)]))
            used, longs = [], []
            for kw, k, tag in spec:
                pool = tag if tag in ("kept", "renewed") else None
                picked = self.pick_permits(deck, d, k, exclude=used, kw=kw, pool=pool)
                assert len(picked) == k, (d, deck, kw, tag, k, len(picked))
                for permit, rating in picked:
                    used.append(permit)
                    longs.append((permit, rating, tag))
            for j, (permit, rating, tag) in enumerate(longs):
                kind = "longfast" if tag == "longfast" else "fast" if rating == 11.0 else "slow"
                if early and deck == "CCN" and j == 0:
                    kind = "early"
                    assert rating == 7.2
                t0, E = self.long_session(kind, rating)
                self.add_deck(deck, d, positions.pop(), t0, E, permit, rating, role="long_" + kind)
            nfill = min(len(positions), int(self.rng.integers(2, 5)))
            self.morning(deck, d, positions[:nfill], end_by=hm(11, 30), exclude=used)

    def rung2_day(self, d):
        for deck in DECKS:
            positions = list(self.rng.permutation([p for p in self.deck_positions(deck) if p not in blocked(deck, d)]))
            used = []
            for kw in RUNG2_SPEC[deck]:
                pool = "kept" if (deck == "CCN" and kw == 7.2) else None
                permit, rating = self.pick_permits(deck, d, 1, exclude=used, kw=kw, pool=pool)[0]
                used.append(permit)
                for _ in range(1000):
                    t0 = float(self.rng.uniform(hm(11, 5), hm(11, 55)))
                    E = float(self.rng.uniform(17.0, 26.0))
                    if t0 + E / 11.5 >= hm(12, 47):
                        break
                self.add_deck(deck, d, positions.pop(), t0, E, permit, rating,
                              plug_out_h=t0 + float(self.rng.uniform(4.6, 5.8)), role="rung2")
            nfill = int(self.rng.integers(8, 11))
            self.morning(deck, d, positions[:nfill], end_by=hm(10, 50), exclude=used)

    def full_morning(self, d):
        """Every unit on both decks charging through 09:15-09:30, all finished by 11:25."""
        for deck in DECKS:
            positions = [p for p in self.deck_positions(deck) if p not in blocked(deck, d)]
            for position, (permit, kw) in zip(positions, self.pick_permits(deck, d, len(positions))):
                t0 = float(self.rng.uniform(hm(7, 50), hm(9, 8)))
                end = float(self.rng.uniform(max(hm(9, 36), t0 + 0.8), hm(11, 25)))
                self.add_deck(deck, d, position, t0, 6.6 * (end - t0), permit, kw, role="fullmorning")

    # ------------------------------------------------------------------ 2024 and 2025 back-test days
    def b3_day(self, d, n_full, partials, protect_positions):
        """n_full sessions charging through 12:00-12:15 and partial sessions ending inside that quarter-hour.

        partials: list of (kW added to the 12:00 quarter-hour, position or None, role). Units in protect_positions host only their
        designated partial and morning sessions finished by 11:35."""
        used, made_pos = [], set()
        free = {deck: list(self.rng.permutation([p for p in self.deck_positions(deck) if p not in protect_positions]))
                for deck in DECKS}
        for p_kw, position, role in partials:
            if position is None:
                deck = DECKS[int(self.rng.integers(2))]
                position = free[deck].pop()
            else:
                deck = "CCN" if position.startswith("N") else "CCS"
            midnight = lt_date(d)
            noon = midnight + 12 * 3600
            t0 = snap(midnight + float(self.rng.uniform(hm(8, 40), hm(10, 30))) * H)
            E = round(6.6 * (noon - t0) / H + p_kw / 4, 3)
            if role == "F":
                # a city fleet car topping up on its fleet card, gone again within the hour after it finishes
                fl = self.fleet[self.fleet["department"].isin(["Facilities Maintenance", "Building Inspection"])
                                & (self.fleet["rating"] < 11.0)]
                po = (noon - midnight) / H + float(self.rng.uniform(0.5, 1.4))
                cards = [c for c in fl["fleet_card"] if self.fleet_free(c, t0 - 60, midnight + po * H + 60)]
                f = fl[fl["fleet_card"] == cards[int(self.rng.integers(len(cards)))]].iloc[0]
                s = self.add_deck(deck, d, position, (t0 - midnight) / H, E, "", f["rating"], plug_out_h=po,
                                  role=role, acct="FLEET", fleet_card=f["fleet_card"])
            else:
                permit, kw = self.pick_permits(deck, d, 1, exclude=used)[0]
                used.append(permit)
                s = self.add_deck(deck, d, position, (t0 - midnight) / H, E, permit, kw, role=role)
            assert abs(s["end_charge"] - (noon + p_kw * 900 / 6.6)) < 1e-3, (s["end_charge"], noon)
            made_pos.add(position)
        nN = min(len(free["CCN"]), (n_full + 1) // 2)
        split = {"CCN": nN, "CCS": n_full - nN}
        assert split["CCS"] <= len(free["CCS"]), (d, split)
        for deck in DECKS:
            for permit, kw in self.pick_permits(deck, d, split[deck], exclude=used):
                used.append(permit)
                position = free[deck].pop()
                made_pos.add(position)
                t0 = float(self.rng.uniform(hm(8, 20), hm(10, 20)))
                end = float(self.rng.uniform(hm(12, 22), hm(13, 30)))
                self.add_deck(deck, d, position, t0, 6.6 * (end - t0), permit, kw, role="b3full")
        for deck in DECKS:
            rest = [p for p in self.deck_positions(deck) if p not in made_pos]
            nfill = int(self.rng.integers(len(rest) // 3, len(rest) // 2 + 2))
            sel = list(self.rng.permutation(rest))[:nfill]
            self.morning(deck, d, sel, end_by=hm(11, 35), exclude=used)


def generate_decks(gen: Generator, cal, reads, b3):
    rng = gen.rng
    plan = {}
    for d in daterange(D0, D1):
        if d.weekday() < 5 and d not in CITY_HOLIDAYS and d not in cal and d not in reads:
            for deck in DECKS:
                u = rng.random()
                plan[(deck, d)] = "repeat" if u < 0.13 else "topup" if u < 0.13 + 0.045 else ""
    for d in daterange(D0, D1):
        tag = cal.get(d)
        if tag and tag[0] == "bind":
            m = tag[1]
            _, k72, r72, n77, s72, s77, s110, s110l = PEAK_2026[m]
            gen.binding_day(d, k72, r72, n77, s72, s77, s110, s110l, early=m in EARLY_MONTHS)
        elif tag and tag[0] == "rung2":
            gen.rung2_day(d)
        elif tag and tag[0] == "b3":
            y, m = tag[1]
            p = b3[m]
            if y == 2024:
                parts = [(p["p24"], None, "P"), (P_R24, REISSUED_POS[int(rng.integers(6))], "R")]
                protect = set(REISSUED_POS)
                if m <= 4:
                    parts.append((P_G24, GATEWAY_B_POS[int(rng.integers(4))], "G"))
                    protect |= set(GATEWAY_B_POS)
                parts.append((P_F, None, "F"))
                gen.b3_day(d, p["n24"], parts, protect)
            else:
                parts = [(p["p25"], None, "P"), (P_F, None, "F")]
                protect = set()
                if m <= 3:
                    parts.append((P_R25, REISSUED_POS[int(rng.integers(6))], "R"))
                    protect |= set(REISSUED_POS)
                elif m in (5, 6, 7):
                    parts.append((P_V2, RESTATED_POS[int(rng.integers(4))], "V"))
                    protect |= set(RESTATED_POS)
                elif m in (10, 12):
                    parts.append((P_D25, None, "D"))
                gen.b3_day(d, p["n25"], parts, protect)
        elif tag and tag[0] == "full":
            gen.full_morning(d)
        else:
            for deck in DECKS:
                kind = plan.get((deck, d), "")
                gen.deck_day(deck, d, OCC[d.month], repeat=kind == "repeat", topup=kind == "topup",
                             blocked_pos=blocked(deck, d))


# ==================================================================================== Library L-09
def generate_library_fast(gen: Generator):
    rng = gen.rng
    fl = gen.fleet
    vans = fl[fl["department"] == "Parking Enforcement"]
    pickup = fl[fl["model"] == "F-150 Lightning"].iloc[0]
    days = [d for d in daterange(date(2024, 1, 8), D1) if d.weekday() < 5 and d not in HOLIDAYS]
    # the pickup borrows the unit on a few days after the April 2025 move, when fleet cards settle in the export
    later = [i for i, d in enumerate(days) if d >= MIGRATION + timedelta(days=14)]
    pickup_days = sorted(rng.choice(later, size=13, replace=False).tolist())
    pickup_days = {days[i] for i in pickup_days}
    busy_until = 0
    for d in days:
        mid = lt_date(d)
        if d in pickup_days:
            t0 = snap(mid + float(rng.uniform(hm(10, 30), hm(12, 30))) * H)
            if t0 > busy_until:
                E = round(float(rng.uniform(24.0, 42.0)), 3)
                po = int(t0 + E / 11.5 * H + float(rng.uniform(0.4, 1.4)) * H)
                gen.add(garage="LIB", position="L-09", start=t0, energy=E, rate=11.5, plug_out=po, acct="FLEET",
                        fleet_card=pickup["fleet_card"], car_kw=pickup["rating"], role="lib_pickup", day=d)
                busy_until = po
        if rng.random() < 0.93:
            t0 = snap(mid + float(rng.uniform(hm(15, 30), hm(18, 15))) * H)
            if t0 <= busy_until + 600:
                continue
            E = round(float(rng.uniform(9.0, 27.0)), 3)
            nxt = d + timedelta(days=1)
            po = snap(lt_date(nxt) + float(rng.uniform(hm(6, 20), hm(7, 30))) * H)
            po = max(po, int(t0 + E / 11.0 * H + 1800))
            free_vans = [c for c in vans["fleet_card"] if gen.fleet_free(c, t0, po)]
            if not free_vans:
                continue
            v = vans[vans["fleet_card"] == free_vans[int(rng.integers(len(free_vans)))]].iloc[0]
            gen.add(garage="LIB", position="L-09", start=t0, energy=E, rate=11.0, plug_out=po, acct="FLEET",
                    fleet_card=v["fleet_card"], car_kw=v["rating"], role="lib_van", day=d)
            busy_until = po


# ==================================================================================== public garages
def generate_public(gen: Generator, pos: pd.DataFrame, deck_special_days: set):
    rng = gen.rng
    reissued_units = set(pos.loc[pos["reissued_id"].notna(), "position"])
    units = pos[(~pos["garage"].isin(DECKS)) & (pos["rating_kw"] == 6.6)]
    for _, u in units.iterrows():
        g, position = u["garage"], u["position"]
        lam = PUBLIC_RATE[g]
        for d in daterange(max(D0, u["installed"]), D1):
            f = 0.65 if d.weekday() >= 5 else 0.8 if d in CITY_HOLIDAYS else 1.0
            k = int(rng.poisson(lam * f))
            if k == 0:
                continue
            arr = np.sort(rng.uniform(hm(6, 45), hm(20, 30), size=k))
            mid = lt_date(d)
            free_at = mid + hm(6, 30) * H
            for a in arr:
                t0 = snap(max(mid + a * H, free_at + 120))
                if t0 > mid + hm(21, 0) * H:
                    break
                E = round(float(np.clip(rng.lognormal(math.log(7.5), 0.55), 0.8, 30.0)), 3)
                po = int(t0 + E / 6.6 * H + float(rng.uniform(0.12, 2.0)) * H)
                if position in reissued_units and d in deck_special_days:
                    if t0 < mid + hm(13, 0) * H and po > mid + hm(11, 30) * H:
                        continue
                fu = gen.fleet.iloc[int(rng.integers(len(gen.fleet)))] if rng.random() < 0.06 else None
                if fu is not None and gen.fleet_free(fu["fleet_card"], t0, po):
                    gen.add(garage=g, position=position, start=t0, energy=E, rate=6.6, plug_out=po, acct="FLEET",
                            fleet_card=fu["fleet_card"], car_kw=fu["rating"], role="fleet", day=d)
                else:
                    gen.add(garage=g, position=position, start=t0, energy=E, rate=6.6, plug_out=po, acct="PUBLIC",
                            role="public", day=d)
                free_at = po
