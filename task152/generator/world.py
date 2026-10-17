"""The world before any export is written: the weather, the plant hour by hour from commercial operation to the cut,
its washes, outages and alarms, the side-by-side test, the district's meters and the desk's hedges. Everything the
pack ships is read off this object; its laws are set here and no record is edited after it is drawn."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import solar as S

# ---------------------------------------------------------------------------------------------------- the world's laws
# the original modules' own wear: slow in the first year, fast from 2017 as the cells degraded under the summer heat,
# slow again from 2020 once that degradation had run its course (per year, by period)
WEAR_KNOTS = [(dt.date(2015, 11, 20), 0.0025), (dt.date(2017, 1, 1), 0.0330), (dt.date(2020, 1, 1), 0.0035)]
WEAR_SPREAD = 0.04          # inverter-to-inverter spread of the wear (module batches), relative
ETA_REF_OLD = 0.955         # DC side at 25 degrees: wiring, mismatch, reflection, spectrum
ETA_REF_NEW = 0.9652        # the new half-cut modules: lower mismatch and reflection, coated glass
# soiling: the share of light the dust takes, built up day by day (per day, by month) and cleared by washes and rain
SOIL_RATE = {1: 0.00016, 2: 0.00016, 3: 0.00018, 4: 0.00048, 5: 0.00052, 6: 0.00050, 7: 0.00032, 8: 0.00032,
             9: 0.00030, 10: 0.00024, 11: 0.00022, 12: 0.00016}
BLOCK_DUST = [1.12, 0.97, 0.95, 1.00]   # block 1 sits beside the county road
HEAVY_RAIN, HEAVY_KEEP, MOD_RAIN, MOD_KEEP, CEMENT = 25.0, 0.80, 6.0, 0.985, 0.0005
HABOOB_P, HABOOB_LO, HABOOB_HI = 0.020, 0.003, 0.008
SOIL_CAP = 0.30
CONSTRUCTION_DUST = 0.020   # the blocks not yet washed at handover
# the washes Tresco ran: six a year to 2018, four in 2019, two in 2020, one each November from 2021
WASH_MONTHS = {2015: [11], 2016: [1, 3, 5, 7, 9, 11], 2017: [1, 3, 5, 7, 9, 11], 2018: [1, 3, 5, 7, 9, 11], 2019: [2, 5, 8, 11],
               2020: [3, 11], 2021: [11], 2022: [11], 2023: [11], 2024: [11], 2025: [11]}
# inverters: AC-to-DC efficiency, failure rate and repair time. The maker left the US market in 2018; from then each
# power stage that failed was replaced with a refurbished third-party stage, which runs with higher losses
ETA_NEW_INV = 0.9800
STAGE_LOSS, STAGE_LOSS_SD = 0.0116, 0.0012   # efficiency lost when a stage is replaced with a refurbished one
REFURB_FROM = dt.date(2018, 3, 1)
ETA_INV07R = 0.9825
FAIL_RATE = [(dt.date(2018, 7, 1), 1.10), (dt.date(2020, 7, 1), 3.20)]       # outages per inverter-year
REPAIR_DAYS = [(dt.date(2018, 7, 1), 1.1), (dt.date(2020, 7, 1), 2.1)]       # mean days out
RIG_BASIS = 1.024           # a single table on its own string inverter: no array mismatch or DC feeder loss, open edge
REPAIR_SIGMA = 0.35
RELAY_TRIPS = [(dt.date(2018, 7, 1), 1.2), (dt.date(2020, 7, 1), 2.6)]       # AC relay nuisance trips a year
LINE_OUTAGES_PER_YEAR = 4.0
MV_LOSS = 0.0135            # collection cables and the main transformer, to the revenue meter
AUX_NIGHT_KW = 78.0         # transformers' no-load and the inverters' standby, drawn through the revenue meter
STATION_KW = {1: 18.0, 2: 17.0, 3: 18.0, 4: 22.0, 5: 28.0, 6: 34.0, 7: 36.0, 8: 35.0, 9: 30.0, 10: 23.0, 11: 19.0,
              12: 18.0}     # the control building and the ranch well, on the district's 12 kV retail service to 15 Sep 2025


def piecewise_rate(d, knots):
    """Integrated wear to date d from (start, rate per year) knots."""
    total = 0.0
    for i, (a, rate) in enumerate(knots):
        b = knots[i + 1][0] if i + 1 < len(knots) else dt.date(2100, 1, 1)
        if d <= a:
            break
        total += rate * ((min(d, b) - a).days / 365.25)
    return total


def eased(d, knots):
    """A level easing linearly from knots[0] to knots[1] between their dates."""
    (a, va), (b, vb) = knots
    if d <= a:
        return va
    if d >= b:
        return vb
    return va + (vb - va) * (d - a).days / (b - a).days


class World:
    pass


def _year_hours(y):
    """(local naive datetimes for the hour starts) of calendar year y as an array of dates and hours."""
    n = (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days
    return n


def simulate():
    W = World()
    W.wx = S.years(2001, 2026)
    plant_days = K.days(K.COD, K.HIST_END)
    W.plant_days = plant_days
    nd = len(plant_days)
    W.day_index = {d: i for i, d in enumerate(plant_days)}
    # hourly series over the plant days
    poa, ghi, dhi, rear, tmod, tamb, wind = [], [], [], [], [], [], []
    rain = []
    for d in plant_days:
        w = W.wx[d.year]
        j = (d - dt.date(d.year, 1, 1)).days
        sl = slice(24 * j, 24 * j + 24)
        poa.append(w["poa"][sl]); ghi.append(w["ghi"][sl]); dhi.append(w["dhi"][sl]); rear.append(w["rear"][sl])
        tmod.append(w["tmod"][sl]); tamb.append(w["tamb"][sl]); wind.append(w["wind"][sl])
        rain.append(w["rain"][j])
    W.poa = np.array(poa)          # (days, 24) W/m2 hourly means
    W.ghi, W.dhi, W.rear = np.array(ghi), np.array(dhi), np.array(rear)
    W.tmod, W.tamb, W.wind = np.array(tmod), np.array(tamb), np.array(wind)
    W.rain = np.array(rain)
    W.month = np.array([d.month for d in plant_days])
    _wear(W)
    _washes(W)
    _soiling(W)
    _outages(W)
    _inverters(W)
    _energy(W)
    _rig(W)
    _meters(W)
    _hedges(W)
    return W


def _wear(W):
    r = K.rng("wear")
    W.wear_k = np.clip(r.normal(1.0, WEAR_SPREAD, K.N_INV), 0.9, 1.1)
    base = np.array([piecewise_rate(d, WEAR_KNOTS) for d in W.plant_days])
    W.wear_base = base
    W.D = 1.0 - np.outer(base, W.wear_k)          # (days, inverters)


def _washes(W):
    """Each wash is a crew working one block a day on weekdays from a start day in the scheduled month; the work
    order records the block and the day."""
    r = K.rng("washes")
    W.wash_events = []        # (wash number, block, date)
    no = 0
    for y, months in sorted(WASH_MONTHS.items()):
        for m in months:
            # the first is Tresco's wash of the construction dust in the week the plant was handed over
            start = dt.date(2015, 11, 18) if y == 2015 else dt.date(y, m, int(r.integers(4, 16)))
            while start.weekday() >= 5:
                start += dt.timedelta(days=1)
            no += 1
            d = start
            blocks = [0, 1, 2, 3]
            for b in blocks:
                while d.weekday() >= 5:
                    d += dt.timedelta(days=1)
                W.wash_events.append((no, b, d))
                d += dt.timedelta(days=1)
    W.wash_day = {(b, d) for _, b, d in W.wash_events}


def _soiling(W):
    r = K.rng("soiling")
    nd = len(W.plant_days)
    haboob = np.zeros(nd)
    for i, d in enumerate(W.plant_days):
        if d.month in (6, 7, 8) and r.random() < HABOOB_P:
            haboob[i] = r.uniform(HABOOB_LO, HABOOB_HI)
    W.haboob = haboob
    W.soil = np.zeros((nd, 4))      # the day's mean loss, by block
    for b in range(4):
        washed = [d for (bb, d) in W.wash_day if bb == b and d < K.COD]
        cur = 0.003 + SOIL_RATE[11] * BLOCK_DUST[b] * (K.COD - washed[0]).days if washed else CONSTRUCTION_DUST
        for i, d in enumerate(W.plant_days):
            cur += SOIL_RATE[d.month] * BLOCK_DUST[b] + haboob[i]
            rr = W.rain[i]
            if rr > HEAVY_RAIN:
                cur = 0.004 + HEAVY_KEEP * cur
            elif rr > MOD_RAIN:
                cur *= MOD_KEEP
            elif rr > 0.5:
                cur += CEMENT
            cur = min(cur, SOIL_CAP)
            if (b, d) in W.wash_day:
                pre = cur
                cur = 0.003
                W.soil[i, b] = 0.25 * pre + 0.75 * cur     # the crew is done by mid-morning
            else:
                W.soil[i, b] = cur


def _inverters(W):
    """Each inverter's AC-to-DC efficiency: its own small offset, and from March 2018 a step down each time a failed
    power stage (two per inverter) was replaced with a refurbished one. Inverter 07's replacement is a new unit."""
    r = K.rng("inverters")
    nd = len(W.plant_days)
    W.eta_k = r.normal(0.0, 0.0010, K.N_INV)
    W.stage_events = []          # (inverter, day index the repair finished, stage, loss)
    step = np.zeros((nd, K.N_INV))
    for ev in sorted([e for e in W.events if e["cause"] == "fault"], key=lambda e: (e["inv"], e["start"])):
        i, d = ev["inv"], ev["start"].date()
        if d < REFURB_FROM or (i == K.INV07 and d >= K.INV07_SWAP - dt.timedelta(days=30)):
            continue
        done = [e for e in W.stage_events if e[0] == i]
        if len(done) >= 2:
            continue
        loss = float(np.clip(r.normal(STAGE_LOSS, STAGE_LOSS_SD), 0.008, 0.015))
        t_end = min((ev["end"].date() - W.plant_days[0]).days, nd - 1)
        W.stage_events.append((i, t_end, len(done) + 1, loss))
        step[t_end + 1:, i] += loss
    W.eta = ETA_NEW_INV + W.eta_k[None, :] - step
    swap = W.day_index[K.INV07_SWAP]
    W.eta[swap:, K.INV07] = ETA_INV07R


def _outages(W):
    """Outage events at minute resolution, local standard time: inverter power-stage faults (out until repaired), AC
    relay trips (latched until a technician resets the relay), the district's 69 kV line outages (every inverter, back
    a few minutes after the line), inverter 07's fire, stops the owner asked for, and power-stage derates (running on
    one stage, capped). No event touches an inverter in the three days after its block's wash. The 2025 logger gaps of
    the four block data loggers are drawn here too, clear of every event on their block."""
    r = K.rng("outages")
    nd = len(W.plant_days)
    guard = {j: set() for j in range(K.N_INV)}
    for (b, d) in W.wash_day:
        for k in range(1, 4):
            for j in range(4 * b, 4 * b + 4):
                guard[j].add(d + dt.timedelta(days=k))
    derate_guard = {j: set() for j in range(K.N_INV)}
    for (b, d) in W.wash_day:
        for k in range(0, 6):
            for j in range(4 * b, 4 * b + 4):
                derate_guard[j].add(d + dt.timedelta(days=k))
    W.events = []
    taken = {j: [] for j in range(K.N_INV)}

    def add(inv, start, end, cause, code, check=True):
        invs = list(range(K.N_INV)) if inv is None else [inv]
        if check:
            d = start.date()
            while d <= end.date():
                if any(d in guard[j] for j in invs):
                    return False
                d += dt.timedelta(days=1)
            pad = dt.timedelta(hours=2)
            for j in invs:
                if any(not (end + pad <= a or start - pad >= b) for a, b in taken[j]):
                    return False
        for j in invs:
            taken[j].append((start, end))
        W.events.append(dict(inv=inv, start=start, end=end, cause=cause, code=code))
        return True

    def working(end, r_=None):
        """A repair or a reset finishes in working hours: an end after 17:30 or before 07:00 moves to the next morning's
        round (07:30 to 10:30)."""
        if dt.time(7, 0) <= end.time() <= dt.time(17, 30):
            return end
        day = end.date() if end.time() < dt.time(7, 0) else end.date() + dt.timedelta(days=1)
        return dt.datetime(day.year, day.month, day.day, 7, 30) + dt.timedelta(minutes=int(r.integers(0, 180)))

    def at(t, lo_h, hi_h):
        d = W.plant_days[t]
        m = int(r.integers(lo_h * 60, hi_h * 60))
        return dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=m)

    # inverter 07's power-stage fire: out until its replacement was commissioned
    add(K.INV07, dt.datetime(2021, 3, 2, 10, 41), dt.datetime(2021, 4, 15, 13, 20), "fire", "F-305", check=False)
    # stops the owner asked for
    W.owner_stops = [
        ([0, 1, 2, 3], dt.datetime(2025, 2, 11, 9, 0), dt.datetime(2025, 2, 11, 14, 5), "the lender's engineer's IV-curve tests"),
        ([8, 9, 10, 11], dt.datetime(2025, 9, 29, 8, 10), dt.datetime(2025, 9, 29, 15, 0), "cabling for the side-by-side test"),
        ([0, 1], dt.datetime(2026, 3, 17, 9, 0), dt.datetime(2026, 3, 17, 14, 0), "the replacement contractor's string survey"),
    ]
    for invs, a, b, why in W.owner_stops:
        for j in invs:
            assert add(j, a, b, "owner", "S-020")
    y0 = W.day_index[dt.date(2025, 1, 1)]
    t = 0
    while True:
        t += int(r.exponential(365.25 / LINE_OUTAGES_PER_YEAR)) + 1
        if t >= nd:
            break
        if W.plant_days[t].year == 2025:
            continue
        st = at(t, 7, 17)
        add(None, st, st + dt.timedelta(minutes=int(r.uniform(1.2, 5.5) * 60)), "line", "F-217")
    rl = K.rng("line2025")
    placed = 0
    while placed < 4:
        t = y0 + int(rl.integers(0, 365))
        d = W.plant_days[t]
        st = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(rl.integers(7 * 60, 16 * 60)))
        if add(None, st, st + dt.timedelta(minutes=int(rl.uniform(1.2, 5.0) * 60)), "line", "F-217"):
            placed += 1
    for i in range(K.N_INV):
        t = 0
        while True:
            d = W.plant_days[min(t, nd - 1)]
            t += int(r.exponential(365.25 / eased(d, FAIL_RATE))) + 1
            if t >= nd:
                break
            d = W.plant_days[t]
            mean_rep = eased(d, REPAIR_DAYS)
            hours = max(2.5, r.lognormal(math.log(mean_rep * 24.0) - REPAIR_SIGMA ** 2 / 2, REPAIR_SIGMA))
            st = at(t, 6, 16)
            add(i, st, working(st + dt.timedelta(minutes=int(hours * 60))), "fault", "F-305")
        t = 0
        while True:
            d = W.plant_days[min(t, nd - 1)]
            t += int(r.exponential(365.25 / eased(d, RELAY_TRIPS))) + 1
            if t >= nd:
                break
            if W.plant_days[t].year == 2025:
                continue
            st = at(t, 8, 16)
            add(i, st, working(st + dt.timedelta(minutes=int(r.uniform(1.5, 9.0) * 60))), "relay", "F-217")
    # 2025's relay trips, drawn on their own so every inverter has at least one in daylight
    r25 = K.rng("relay2025")
    y0 = W.day_index[dt.date(2025, 1, 1)]
    for i in range(K.N_INV):
        n = 1 + int(r25.poisson(1.6))
        placed = 0
        while placed < n:
            t = y0 + int(r25.integers(0, 365))
            d = W.plant_days[t]
            m = int(r25.integers(8 * 60, 15 * 60))
            st = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=m)
            if add(i, st, working(st + dt.timedelta(minutes=int(r25.uniform(1.5, 7.5) * 60))), "relay", "F-217"):
                placed += 1
    # derates: one power stage of two out, the inverter capped near half its rating until the stage is replaced
    W.derates = []
    for i in range(K.N_INV):
        t = 0
        while True:
            t += int(r.exponential(365.25 / 0.6)) + 1
            if t >= nd:
                break
            dur = int(r.integers(2, 9))
            if any(W.plant_days[min(t + k, nd - 1)] in derate_guard[i] for k in range(dur)):
                continue
            W.derates.append((i, t, dur))
    # the online share of each hour (days, 24, inverters)
    W.online = np.ones((nd, 24, K.N_INV))
    first = dt.datetime(W.plant_days[0].year, W.plant_days[0].month, W.plant_days[0].day)
    for ev in W.events:
        invs = range(K.N_INV) if ev["inv"] is None else [ev["inv"]]
        a = max(ev["start"], first)
        b = ev["end"]
        cur = a
        while cur < b:
            hour_start = cur.replace(minute=0, second=0, microsecond=0)
            nxt = min(b, hour_start + dt.timedelta(hours=1))
            ti = (hour_start.date() - W.plant_days[0]).days
            if ti >= nd:
                break
            share = (nxt - cur).total_seconds() / 3600.0
            for j in invs:
                W.online[ti, hour_start.hour, j] = max(0.0, W.online[ti, hour_start.hour, j] - share)
            cur = nxt
    # the 2025 logger gaps: each block's data logger drops its link for a few hours at a time
    rg = K.rng("logger2025")
    W.logger_gaps = []
    busy = {b: [] for b in range(4)}
    for ev in W.events:
        invs = range(K.N_INV) if ev["inv"] is None else [ev["inv"]]
        for j in invs:
            busy[K.BLOCK_OF[j]].append((ev["start"] - dt.timedelta(hours=2), ev["end"] + dt.timedelta(hours=2)))
    for (i, t, dur) in W.derates:
        d = W.plant_days[t]
        busy[K.BLOCK_OF[i]].append((dt.datetime(d.year, d.month, d.day), dt.datetime(d.year, d.month, d.day) + dt.timedelta(days=dur)))
    for b in range(4):
        n = 5 + int(rg.integers(0, 5))
        placed = 0
        while placed < n:
            t = y0 + int(rg.integers(0, 364))
            d = W.plant_days[t]
            st = dt.datetime(d.year, d.month, d.day, int(rg.integers(5, 15)))
            hrs = int(rg.integers(2, 13))
            en = st + dt.timedelta(hours=hrs)
            if en.year != 2025 or any(not (en <= a or st >= c) for a, c in busy[b]):
                continue
            if any(not (en <= g[1] or st >= g[0]) for g in [(x[1], x[1] + dt.timedelta(hours=x[2])) for x in W.logger_gaps if x[0] == b]):
                continue
            W.logger_gaps.append((b, st, hrs))
            placed += 1
    W.logger_gaps.sort()


def _energy(W):
    nd = len(W.plant_days)
    r = K.rng("noise")
    tc = 1.0 + K.GAMMA_OLD * (W.tmod - 25.0)                 # (days, 24)
    W.tc = tc
    soil_inv = W.soil[:, K.BLOCK_OF]                          # (days, inverters)
    noise = 1.0 + r.normal(0.0, 0.0035, (nd, K.N_INV))
    dc = (W.poa[:, :, None] / 1000.0 * K.OLD_KWP_INV * ETA_REF_OLD * tc[:, :, None]
          * W.D[:, None, :] * (1.0 - soil_inv[:, None, :]) * noise[:, None, :] * W.online)
    ac = dc * W.eta[:, None, :]
    cap = np.full((nd, K.N_INV), K.INV_AC_KW)
    for (i, t, dur) in W.derates:
        cap[t:t + dur, i] = 0.52 * K.INV_AC_KW
    ac_c = np.minimum(ac, cap[:, None, :])
    W.clipped_share = float((ac - ac_c).sum() / ac.sum())
    dc = np.where(ac > ac_c, ac_c / W.eta[:, None, :], dc)
    W.dc_h, W.ac_h = dc, ac_c                                  # kWh in each hour
    W.dc_d = dc.sum(axis=1)                                    # (days, inverters) kWh
    W.ac_d = ac_c.sum(axis=1)
    feed = np.clip(W.poa / 40.0, 0.0, 1.0)                    # the share of the hour above the start-up threshold
    rj = K.rng("ophours")
    W.op_hours = (W.online * feed[:, :, None]).sum(axis=1) + rj.uniform(-0.03, 0.03, (nd, K.N_INV))
    W.op_hours = np.clip(W.op_hours, 0.0, None)
    W.online_hours = W.online.sum(axis=1)
    W.poa_d = W.poa.sum(axis=1) / 1000.0                       # kWh/m2
    w = np.maximum(W.poa, 0.0)
    W.tmod_w = np.where(w.sum(axis=1) > 0, (w * W.tmod).sum(axis=1) / np.maximum(w.sum(axis=1), 1e-9), 25.0)
    W.tamb_d = W.tamb.mean(axis=1)
    # the revenue meter: the inverters' output less collection and transformer losses, the night draw, and from
    # 15 September 2025 the station service behind the meter
    plant_h = ac_c.sum(axis=2) * (1.0 - MV_LOSS)              # kWh per hour
    night = (W.poa <= 0.5)
    aux = np.where(night, AUX_NIGHT_KW, 0.0)
    station = np.zeros_like(plant_h)
    for i, d in enumerate(W.plant_days):
        if d >= K.STATION_SERVICE_END:
            station[i, :] = STATION_KW[d.month]
    net_h = plant_h - aux - station
    W.del_h = np.clip(net_h, 0.0, None)
    W.rec_h = np.clip(-net_h, 0.0, None)
    W.del_d = W.del_h.sum(axis=1)
    W.rec_d = W.rec_h.sum(axis=1)
    W.station_d = np.array([STATION_KW[d.month] * 24.0 if d < K.STATION_SERVICE_END else 0.0 for d in W.plant_days])
    # the plant pyranometer: cleaned weekly, a small reading scatter
    r2 = K.rng("pyranometer")
    W.pyr_d = W.poa_d * (1.0 + r2.normal(0.0, 0.002, nd))


def _rig(W):
    """The side-by-side test inside block 3: a table of 12 new 450 W bifacial modules and a table of 18 unexposed
    original 315 W modules from the site store, each on its own string inverter with DC metering, washed weekly."""
    r = K.rng("rig")
    a, b = W.day_index[K.RIG_START], W.day_index[K.RIG_END]
    sl = slice(a, b + 1)
    soil = np.zeros(b - a + 1)
    cur = 0.002
    for k, d in enumerate(W.plant_days[sl]):
        cur += SOIL_RATE[d.month] * BLOCK_DUST[2] + W.haboob[a + k]
        if d.weekday() == 0:
            cur = 0.002
        soil[k] = cur
    poa, tmod, rear = W.poa[sl], W.tmod[sl], W.rear[sl]
    tc_old = 1.0 + K.GAMMA_OLD * (tmod - 25.0)
    tc_new = 1.0 + K.GAMMA_NEW * (tmod - 2.0 - 25.0)      # glass-glass bifacial runs a little cooler
    eff = poa + K.BIFACIALITY * rear
    ref = (poa / 1000.0 * 5.67 * ETA_REF_OLD * RIG_BASIS * tc_old * (1.0 - soil[:, None])).sum(axis=1)
    new = (eff / 1000.0 * 5.40 * ETA_REF_NEW * RIG_BASIS * tc_new * (1.0 - soil[:, None])).sum(axis=1)
    W.rig_days = W.plant_days[sl]
    W.rig_ref = ref * (1.0 + r.normal(0.0, 0.002, len(ref)))
    W.rig_new = new * (1.0 + r.normal(0.0, 0.002, len(new)))
    W.rig_gain = float((W.rig_new.sum() / 5.40) / (W.rig_ref.sum() / 5.67))


def _meters(W):
    """The district's account for the plant: the generation interconnection (service point 0417, the 69 kV revenue
    meter, channels DEL and REC as the plant sees them) and, to 15 September 2025, the station-service retail point
    (service point 0418, rate GS-3), whose DEL is the energy the district delivered to the control building and well."""
    r = K.rng("meters")
    W.sp417_del = W.del_d.copy()
    W.sp417_rec = W.rec_d.copy()
    W.sp418_del = W.station_d * (1.0 + r.normal(0.0, 0.06, len(W.station_d)))
    W.sp418_del = np.where(W.station_d > 0, W.sp418_del, 0.0)


def _hedges(W):
    """Each autumn the desk sold the next year's output forward at its P90 under the policy then in force: the
    performance ratio of the last five full years (the engineer's design ratio before there were any), the long-term
    record's P90 irradiation as then available, the original nameplate; rounded down to 1,000 MWh. Buy-backs in the
    blotter; two re-shapes after spring re-forecasts amended by confirmation."""
    W.sales = {}
    for y in range(2016, 2026):
        hist = [yy for yy in range(max(2016, y - 6), y - 1) if yy >= 2016]
        if hist:
            prs = []
            for yy in hist:
                idx = [i for i, d in enumerate(W.plant_days) if d.year == yy]
                prs.append((W.del_d[idx].sum() - W.rec_d[idx].sum()) / (W.pyr_d[idx].sum() * K.DC_OLD_KWP))
            pr = float(np.mean(prs[-5:]))
        else:
            pr = 0.812
        lt = [W.wx[yy]["poa"].sum() / 1000.0 for yy in range(2001, y - 1)]
        p90 = float(np.mean(lt) - K.POLICY_Z * np.std(lt, ddof=1))
        W.sales[y] = int(math.floor(pr * K.DC_OLD_KWP * p90 / 1000.0 / 1000.0)) * 1000
    W.buybacks = {2019: 1400, 2022: 1100}
    W.amendments = {2021: 2500, 2024: 1800}


def delivered(W, y):
    idx = [i for i, d in enumerate(W.plant_days) if d.year == y]
    return float(W.sp417_del[idx].sum() - W.sp417_rec[idx].sum()) / 1000.0
