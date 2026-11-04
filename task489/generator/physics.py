"""task489: the separators' level control executed on the shipped inflow, and the sensitivity sweep the call must
survive. The makers' sheets file each controller's logic (the dump valve opens when the liquid reaches the upper
setting and shuts when it has fallen to the lower one); the plunger controller's specification files that the plunger
brings the liquid above it to surface as it arrives, and its history gives each arrival's time and the plunger's
travel; the allocations give each production day's liquid; the register gives the bore, the span, the lower setting,
the high level shutdown, the dump valve body, the tubing and the plunger depth. This module runs that logic, cycle by
cycle, over the plausible range of everything the pack leaves to physics: the dump valve's drain rate, the speed at
which a slug comes off the tubing, any liquid that follows in the afterflow, and the effective volume between the
settings."""
import collections
import datetime as dt
import itertools
import math

import sim as S
import world as W

TUBE_ID_M = {"60.3 mm": 0.0507, "73.0 mm": 0.0620}
# plausible ranges, each wider than the pack's own facts allow
DRAIN_M3H = {"1 in": (1.5, 7.0), "2 in": (3.0, 25.0)}   # dump valve drain rate across trims and separator pressures
ARRIVAL_SPEED = (0.6, 1.6)      # a slug's speed off the tubing, as a share of the plunger's average speed on its trip
AFTERFLOW_LIQ = (0.0, 0.15)     # share of each cycle's liquid that follows the plunger in the afterflow
BAND_SCALE = (0.9, 1.0, 1.1)    # the effective volume between the settings, against bore times span


def events(wd):
    """For each plunger well, its arrivals in the reporting year (each cycle once, on its own well, by valve open):
    (seconds from the window's start to the arrival, the cycle's liquid, the plunger's average speed, afterflow s)."""
    wells = {w["uwi"]: w for w in wd["wells"]}
    by = collections.defaultdict(list)
    for c in wd["cycles"]:
        if c["resent"] or c["result"] != "ARRIVE":
            continue
        if W.WINDOW_START_UTC <= c["open_utc"] < W.WINDOW_END_UTC:
            by[c["uwi"]].append(c)
    out = {}
    for uwi, cs in by.items():
        p = wd["prod"][uwi]
        liq = p["cond"] + p["water"]
        pday = lambda c: S.local_naive(c["open_utc"] - dt.timedelta(hours=W.PROD_DAY_HOUR)).date()
        per_day = collections.Counter(pday(c) for c in cs)
        w = wells[uwi]
        ev = []
        for c in cs:
            day = pday(c)
            q = float(liq[(day - W.DAYS[0]).days]) / per_day[day]
            if q <= 0:
                continue
            ev.append(((c["open_utc"] - W.WINDOW_START_UTC).total_seconds() + c["travel_s"], q,
                       w["depth_m"] / c["travel_s"], c["afterflow_min"] * 60.0))
        ev.sort()
        out[uwi] = ev
    return out


def _phase(lvl, is_open, q, dur, band, c, top):
    """Liquid in at rate q for dur seconds: the valve opens when the level reaches the band, shuts at zero."""
    n = 0
    while dur > 1e-9:
        if not is_open:
            if q <= 0:
                return lvl, is_open, n, top
            tf = (band - lvl) / q
            if tf >= dur:
                lvl += q * dur
                return lvl, is_open, n, max(top, lvl)
            dur -= tf
            lvl, is_open, n = band, True, n + 1
        else:
            net = q - c
            if net >= 0:
                lvl += net * dur
                return lvl, is_open, n, max(top, lvl)
            td = lvl / -net
            if td >= dur:
                return lvl + net * dur, is_open, n, top
            dur -= td
            lvl, is_open = 0.0, False
    return lvl, is_open, n, top


def openings(ev, band, drain_m3h, speed, af_share, area_tube):
    """The dump valve's openings over the year, and the highest level reached above the lower setting (m3)."""
    c = drain_m3h / 3600.0
    lvl, is_open, n, top, t = 0.0, False, 0, 0.0, None
    for ta, q, v, af in ev:
        slug = (1.0 - af_share) * q
        tau = slug / (area_tube * v * speed)
        t0 = ta - tau
        if t is not None and t0 > t:
            lvl, is_open, m, top = _phase(lvl, is_open, 0.0, t0 - t, band, c, top)
            n += m
        lvl, is_open, m, top = _phase(lvl, is_open, slug / tau, tau, band, c, top)
        n += m
        t = ta
        if af_share > 0 and af > 0:
            lvl, is_open, m, top = _phase(lvl, is_open, af_share * q / af, af, band, c, top)
            n += m
            t = ta + af
    return n, top


def sweep(wd, tr):
    """Run every plunger separator at every corner of the plausible box. Returns, per corner, each plunger level
    controller's openings and highest level, and the pads' intermittent-vent tonnes with the rest of the inventory
    as the golden has it."""
    ev = events(wd)
    wells = {w["uwi"]: w for w in wd["wells"]}
    gold_kg = {row["sep"]["lc_tag"]: row["kg"]["golden"] for row in tr["lc"]}
    plunger = [sp for sp in wd["seps"] if sp["group"] != "F"]
    out = []
    for b in BAND_SCALE:
        for i_c, speed, af_share in itertools.product((0, 1), ARRIVAL_SPEED, AFTERFLOW_LIQ):
            res = {}
            for sp in plunger:
                w = wells[sp["uwi"]]
                area = math.pi / 4.0 * TUBE_ID_M[w["tubing"]] ** 2
                n, top = openings(ev[sp["uwi"]], sp["band"] * b, DRAIN_M3H[sp["valve"]][i_c], speed, af_share, area)
                res[sp["lc_tag"]] = {"n": n, "top": top, "kg": n * sp["kpc"]}
            pads = {}
            for sp in wd["seps"]:
                kg = res[sp["lc_tag"]]["kg"] if sp["lc_tag"] in res else gold_kg[sp["lc_tag"]]
                pads[sp["site"]] = pads.get(sp["site"], 0.0) + kg / 1000.0
            out.append({"band": b, "drain": ("low", "high")[i_c], "speed": speed, "af_share": af_share, "lc": res,
                        "pads": pads, "set": sorted(cd for cd, v in pads.items() if v > W.LINE_T)})
    return out


def slug_rate_margin(wd):
    """For every big-slug separator, the slowest a slug comes off the tubing (m3/h, at the low end of the arrival
    speed range) against the fastest its dump valve can drain: the valve cannot keep up with the slug, so the level
    passes the upper setting with the slug still arriving."""
    ev = events(wd)
    wells = {w["uwi"]: w for w in wd["wells"]}
    out = {}
    for sp in wd["seps"]:
        if sp["group"] != "PB":
            continue
        w = wells[sp["uwi"]]
        area = math.pi / 4.0 * TUBE_ID_M[w["tubing"]] ** 2
        slowest = min(area * v * ARRIVAL_SPEED[0] * 3600.0 for _, _, v, _ in ev[sp["uwi"]])
        out[sp["lc_tag"]] = (slowest, DRAIN_M3H[sp["valve"]][1])
    return out


def vessel_room(sp):
    """Liquid the vessel holds between the lower setting and the high level shutdown, m3."""
    r = sp["bore"] * 0.0254 / 2.0
    return math.pi * r * r * (sp["lshh_in"] - sp["low_in"]) * 0.0254
