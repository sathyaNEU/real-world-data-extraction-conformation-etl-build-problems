"""The world behind task452 v3: a two-kiln cement works through calendar 2026, simulated minute by minute.

Everything is drawn from one fixed seed, so two runs give the same world to the byte. The simulation keeps the
true state of every kiln line (kiln feed, raw mill, meal silo, burner, filter dust silo) and the true mercury
released to air in every minute; the pack writer (pack.py) turns it into the records a works would hold, and the
analysis (analysis.py) works only from those records.
"""
import datetime as dt
import math
from zoneinfo import ZoneInfo

import numpy as np

SEED = 452
UTC = dt.timezone.utc
TZ = ZoneInfo("Europe/Dublin")
T0 = dt.datetime(2026, 1, 1, tzinfo=UTC)          # local midnight too: Irish winter time is UTC
NMIN = 365 * 24 * 60
MONTHS = list(range(1, 13))

# ---- kiln lines -------------------------------------------------------------------------------------------------
KILNS = {
    "K1": dict(feed=205.0, mill_cap=246.0, silo_cap=9000.0, silo0=6100.0, loi=0.355, nm3_per_t=2250.0,
               shutdown=((1, 12, 6), (2, 6, 18)), n_stops=6, nox=392.0, so2=118.0, o2=8.55, ratio_d=7.0,
               coal_per_clk=0.085, srf_per_clk=0.052, bleed_tph=1.25),
    "K2": dict(feed=140.0, mill_cap=176.0, silo_cap=6500.0, silo0=4300.0, loi=0.352, nm3_per_t=2320.0,
               shutdown=((2, 16, 6), (3, 9, 18)), n_stops=5, nox=358.2, so2=96.0, o2=8.85, ratio_d=6.5,
               coal_per_clk=0.128, srf_per_clk=0.0, bleed_tph=0.0),
}

# raw mix (share of dry raw meal) and the lab's typical composition of each input (dry basis)
MIX = {
    "K1": {"limestone": 0.790, "shale": 0.155, "sand": 0.025, "iron_ore": 0.015, "steel_slag": 0.015},
    "K2": {"limestone": 0.780, "shale": 0.100, "fly_ash": 0.090, "iron_ore": 0.015, "sand": 0.015},
}
#            Hg mg/kg  moist%  CaO   SiO2  Al2O3 Fe2O3 MgO  SO3  LOI
COMP = {
    "limestone":  (0.0200, 3.1, 51.6, 4.1, 1.0, 0.5, 1.30, 0.10, 41.5),
    "shale":      (0.1300, 9.4, 4.2, 58.0, 18.5, 6.9, 2.40, 0.60, 7.5),
    "sand":       (0.0080, 5.2, 0.6, 92.0, 3.1, 1.2, 0.20, 0.05, 1.2),
    "iron_ore":   (0.0450, 6.8, 2.1, 9.5, 3.2, 79.0, 0.80, 0.30, 3.0),
    "steel_slag": (0.0040, 4.5, 42.0, 15.0, 4.5, 24.0, 8.10, 0.40, 1.8),
    "fly_ash":    (0.4237, 0.6, 4.6, 52.0, 24.0, 8.5, 1.80, 0.80, 3.4),
}
QUARTERLY = {"sand", "iron_ore", "steel_slag"}
FUELS = {  # Hg mg/kg dry, moisture % ar, NCV GJ/t ar, ash % dry, S % dry
    "coal": (0.0850, 8.6, 26.10, 12.4, 0.95),
    "srf":  (0.2200, 15.5, 18.40, 14.8, 0.28),
}
CLINKER = (0.00125, 0.2, 65.6, 21.4, 5.2, 3.3, 1.85, 1.05, 0.30)   # Hg, moist, CaO, SiO2, Al2O3, Fe2O3, MgO, SO3, LOI
DUST_HG = 1.22          # mg/kg, K1 filter dust (the mercury the raw mill hands back is carried in it)

# the stack tests (local start of run 1); runs are 90 minutes with 30 minutes between them
TESTS = {
    "K1": [(2024, 9, 17, 9, 30), (2025, 9, 23, 9, 45), (2026, 9, 15, 9, 30)],
    "K2": [(2024, 10, 8, 10, 0), (2025, 10, 14, 9, 30), (2026, 10, 6, 10, 0)],
}
# the control system upgrade: the historian server was migrated and wrote nothing between these UTC instants
HIST_GAP = (dt.datetime(2026, 5, 11, 6, 0, tzinfo=UTC), dt.datetime(2026, 5, 20, 6, 0, tzinfo=UTC))
# the analyser data loggers' own export, read back after the migration (UTC instants of interval start)
BACKFILL = (dt.datetime(2026, 5, 8, 23, 0, tzinfo=UTC), dt.datetime(2026, 5, 21, 23, 0, tzinfo=UTC))
NOX_TRIAL = (dt.datetime(2026, 5, 11, 0, 0, tzinfo=UTC), dt.datetime(2026, 5, 21, 0, 0, tzinfo=UTC))
# the night the clocks go back: K1's raw mill stops at 01:05 IST and restarts at 01:50 GMT
FALLBACK_STOP = (dt.datetime(2026, 10, 25, 0, 5, tzinfo=UTC), dt.datetime(2026, 10, 25, 1, 50, tzinfo=UTC))


def minute(t):
    return int((t - T0).total_seconds() // 60)


def local_dt(year, month, day, hour, minute_=0):
    return dt.datetime(year, month, day, hour, minute_, tzinfo=TZ).astimezone(UTC)


def local_calendar():
    """Per minute: local month, weekday, hour (vectorised once)."""
    base = np.arange(NMIN, dtype=np.int64)
    out_month = np.zeros(NMIN, dtype=np.int8)
    out_wd = np.zeros(NMIN, dtype=np.int8)
    out_hr = np.zeros(NMIN, dtype=np.int8)
    # IST runs from 29 March 01:00 UTC to 25 October 01:00 UTC
    ist0, ist1 = minute(dt.datetime(2026, 3, 29, 1, tzinfo=UTC)), minute(dt.datetime(2026, 10, 25, 1, tzinfo=UTC))
    off = np.where((base >= ist0) & (base < ist1), 60, 0)
    loc = base + off
    days = loc // 1440
    d0 = dt.date(2026, 1, 1)
    # month and weekday per local day index (day 365 is 1 January 2027 for the last local hour, never reached)
    mon = np.array([(d0 + dt.timedelta(days=int(i))).month for i in range(367)], dtype=np.int8)
    wdy = np.array([(d0 + dt.timedelta(days=int(i))).weekday() for i in range(367)], dtype=np.int8)
    out_month[:] = mon[days]
    out_wd[:] = wdy[days]
    out_hr[:] = (loc % 1440) // 60
    return out_month, out_wd, out_hr, off


def simulate():
    rng = np.random.default_rng(SEED)
    mon, wd, hr, off = local_calendar()
    world = {"kilns": {}, "rng_state": None}
    peak = ((mon == 1) | (mon == 2) | (mon == 11) | (mon == 12)) & (wd < 5) & (hr >= 17) & (hr < 19)

    for k, p in KILNS.items():
        r = np.random.default_rng(SEED * 10 + (1 if k == "K1" else 2))
        # --- kiln feed availability: annual shutdown and random stops --------------------------------------
        kiln_on = np.ones(NMIN, dtype=bool)
        (m0, d0_, h0), (m1, d1, h1) = p["shutdown"]
        s0, s1 = minute(local_dt(2026, m0, d0_, h0)), minute(local_dt(2026, m1, d1, h1))
        kiln_on[s0:s1] = False
        protected = []
        for (y, mo, da, ho, mi) in TESTS[k]:
            if y == 2026:
                t = minute(local_dt(y, mo, da, ho, mi))
                protected.append((t - 12 * 60, t + 8 * 60))
        if k == "K1":
            protected.append((minute(FALLBACK_STOP[0]) - 24 * 60, minute(FALLBACK_STOP[1]) + 24 * 60))
        protected.append((minute(HIST_GAP[0]) - 3 * 1440, minute(HIST_GAP[1]) + 3 * 1440))
        stops = []
        while len(stops) < p["n_stops"]:
            st = int(r.integers(minute(dt.datetime(2026, 3, 20, tzinfo=UTC)), NMIN - 3 * 1440))
            du = int(r.integers(14 * 60, 60 * 60))
            if any(st < b + 1440 and st + du > a - 1440 for a, b in protected + stops):
                continue
            if any(abs(st - a) < 20 * 1440 for a, b in stops):
                continue
            stops.append((st, st + du))
        for a, b in stops:
            kiln_on[a:b] = False
        # burner heat-up: 10 h before every return to feed after a stop
        heat = np.zeros(NMIN, dtype=bool)
        starts = np.flatnonzero(kiln_on[1:] & ~kiln_on[:-1]) + 1
        for s in starts:
            heat[max(0, s - 600):s] = True
        heat &= ~kiln_on
        # --- feed rate -----------------------------------------------------------------------------------
        month_factor = {m: float(r.uniform(0.975, 1.02)) for m in MONTHS}
        hh = r.normal(0.0, 0.014, NMIN // 30 + 1)
        feed = np.array([month_factor[int(mm)] for mm in mon], dtype=float) * p["feed"]
        feed *= (1.0 + np.repeat(hh, 30)[:NMIN])
        # ramp after each start: 55 per cent of rate rising to full over six hours
        ramp = np.ones(NMIN)
        for s in starts:
            n = min(360, NMIN - s)
            ramp[s:s + n] = 0.55 + 0.45 * np.arange(n) / 360.0
        feed *= ramp
        feed[~kiln_on] = 0.0
        # --- raw mill and the meal silo ------------------------------------------------------------------
        forced_off = peak.copy()
        # fortnightly maintenance, Tuesdays 08:00-14:00 local, K1 on even ISO weeks, K2 on odd
        for day in range(365):
            date = dt.date(2026, 1, 1) + dt.timedelta(days=day)
            if date.weekday() == 1 and (date.isocalendar()[1] % 2 == (0 if k == "K1" else 1)):
                a = minute(local_dt(date.year, date.month, date.day, 8))
                forced_off[a:a + 360] = True
        # breakdowns: the mill out while the kiln runs on the silo
        bdown = []
        while len(bdown) < 5:
            st = int(r.integers(minute(dt.datetime(2026, 3, 15, tzinfo=UTC)), NMIN - 2 * 1440))
            du = int(r.integers(6 * 60, 15 * 60))
            if not kiln_on[st:st + du].all():
                continue
            if any(st < b + 3 * 1440 and st + du > a - 3 * 1440 for a, b in protected + bdown):
                continue
            bdown.append((st, st + du))
        for a, b in bdown:
            forced_off[a:b] = True
        forced_on = np.zeros(NMIN, dtype=bool)
        for (y, mo, da, ho, mi) in TESTS[k]:
            if y == 2026:
                t = minute(local_dt(y, mo, da, ho, mi))
                forced_off[t - 360:t] = True          # silo drawn down before the test
                forced_on[t:t + 5 * 60 + 30] = True    # three 90-minute runs with the mill on
        if k == "K1":
            a, b = minute(FALLBACK_STOP[0]), minute(FALLBACK_STOP[1])
            forced_off[a:b] = True
            forced_on[b:b + 120] = True
        # trips: the mill stops on a protection and restarts after 20 to 90 minutes
        trip_at = set()
        for _ in range(38):
            t = int(r.integers(0, NMIN))
            trip_at.add(t)
        mill_rate = p["mill_cap"] * (1.0 + np.repeat(r.normal(0.0, 0.02, NMIN // 60 + 1), 60)[:NMIN])
        mill_on = np.zeros(NMIN, dtype=bool)
        events = []          # (minute, second, kind) kind in START, STOP, TRIP
        level = p["silo0"]
        lev = np.zeros(NMIN)
        on = False
        trip_until = -1
        feed_cut = np.zeros(NMIN, dtype=bool)
        cut = False
        cap = p["silo_cap"]
        for m in range(NMIN):
            want_on = on
            if forced_on[m]:
                want_on = True
            elif forced_off[m] or m < trip_until:
                want_on = False
            else:
                if on and level >= 0.94 * cap:
                    want_on = False
                elif (not on) and level <= 0.45 * cap:
                    want_on = True
            if on and m in trip_at and not forced_on[m]:
                want_on = False
                trip_until = m + int(r.integers(20, 91))
                events.append((m, int(r.integers(0, 60)), "TRIP"))
                on = False
            elif want_on != on:
                events.append((m, int(r.integers(0, 60)), "START" if want_on else "STOP"))
                on = want_on
            mill_on[m] = on
            f = feed[m]
            if cut:
                f = 0.0
            level += ((mill_rate[m] if on else 0.0) - f) / 60.0
            if level <= 0.02 * cap and f > 0:
                cut = True
            if cut and level >= 0.20 * cap:
                cut = False
            if cut:
                feed_cut[m] = True
            level = min(level, cap)
            lev[m] = level
        feed = np.where(feed_cut, 0.0, feed)
        kiln_feed_on = feed > 0
        # --- production and fuel -------------------------------------------------------------------------
        loi_m = {m: p["loi"] + float(r.normal(0, 0.002)) for m in MONTHS}
        clk = feed * (1.0 - np.array([loi_m[int(mm)] for mm in mon])) / 60.0          # t per minute
        meal = np.where(mill_on, mill_rate, 0.0) / 60.0                                  # t dry meal per minute
        coal = clk * p["coal_per_clk"] * 60.0 / 60.0 + np.where(heat, 4.0 / 60.0, 0.0)  # t as fired per minute
        srf = clk * p["srf_per_clk"]
        # --- mercury released to air, before scaling to the year's balance --------------------------------
        rel_shape = np.where(kiln_feed_on, np.where(mill_on, 1.0, p["ratio_d"]) * feed / p["feed"], 0.0)
        # --- filter dust bleed (K1) ----------------------------------------------------------------------
        bleed = np.where(kiln_feed_on, p["bleed_tph"] / 60.0, 0.0)
        world["kilns"][k] = dict(kiln_on=kiln_feed_on, heat=heat, feed=feed, mill_on=mill_on, mill_events=events,
                                 silo=lev, clk=clk, meal=meal, coal=coal, srf=srf, rel_shape=rel_shape,
                                 bleed=bleed, stops=stops, bdown=bdown, loi_m=loi_m,
                                 month_factor=month_factor, starts=starts)
    world["mon"], world["wd"], world["hr"], world["off"] = mon, wd, hr, off
    world["rng"] = rng
    return world


def lab_values(world):
    """Monthly (or quarterly) composite analyses: the laboratory's results, which the world takes as the truth."""
    r = np.random.default_rng(SEED * 100 + 7)
    lab = {}
    for mat, c in COMP.items():
        periods = [1, 4, 7, 10] if mat in QUARTERLY else MONTHS
        for pm in periods:
            hg = c[0] * float(np.exp(r.normal(0, 0.10)))
            moist = max(0.3, c[1] * (1 + float(r.normal(0, 0.12))))
            vals = [c[i] * (1 + float(r.normal(0, 0.015))) for i in range(2, 9)]
            lab[(mat, pm)] = dict(hg=round(hg, 4), moist=round(moist, 1), cao=round(vals[0], 2),
                                  sio2=round(vals[1], 2), al2o3=round(vals[2], 2), fe2o3=round(vals[3], 2),
                                  mgo=round(vals[4], 2), so3=round(vals[5], 2), loi=round(vals[6], 2))
    for f, c in FUELS.items():
        for pm in MONTHS:
            lab[(f, pm)] = dict(hg=round(c[0] * float(np.exp(r.normal(0, 0.09))), 4),
                                moist=round(c[1] * (1 + float(r.normal(0, 0.06))), 1),
                                ncv=round(c[2] * (1 + float(r.normal(0, 0.02))), 2),
                                ash=round(c[3] * (1 + float(r.normal(0, 0.04))), 2),
                                s=round(c[4] * (1 + float(r.normal(0, 0.05))), 2))
    for k in KILNS:
        for pm in MONTHS:
            c = CLINKER
            lab[("clinker_" + k, pm)] = dict(hg=round(c[0] * float(np.exp(r.normal(0, 0.15))), 5),
                                             moist=0.2, cao=round(c[2] + float(r.normal(0, 0.25)), 2),
                                             sio2=round(c[3] + float(r.normal(0, 0.15)), 2),
                                             al2o3=round(c[4] + float(r.normal(0, 0.08)), 2),
                                             fe2o3=round(c[5] + float(r.normal(0, 0.06)), 2),
                                             mgo=round(c[6] + float(r.normal(0, 0.06)), 2),
                                             so3=round(c[7] + float(r.normal(0, 0.05)), 2),
                                             loi=round(c[8] + float(r.normal(0, 0.05)), 2))
    for pm in MONTHS:
        lab[("dust_K1", pm)] = dict(hg=round(DUST_HG * float(np.exp(r.normal(0, 0.12))), 3), moist=0.3,
                                    cao=round(44.0 + float(r.normal(0, 1.0)), 2), loi=round(28.0 + float(r.normal(0, 1.5)), 2))
    return lab


def mix_by_month(kiln, seed_off):
    """Each month's raw mix share (the quality laboratory trims the mix month to month), shares summing to one."""
    r = np.random.default_rng(SEED * 1000 + seed_off)
    out = {}
    for m in MONTHS:
        raw = {mat: s * (1 + float(r.normal(0, 0.03))) for mat, s in MIX[kiln].items()}
        tot = sum(raw.values())
        out[m] = {mat: v / tot for mat, v in raw.items()}
    return out
