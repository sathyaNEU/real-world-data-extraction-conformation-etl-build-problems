"""The world as it happened, December 2024 to December 2027: sixteen stations' NO and NO2 hour by hour, the analyzers
that measured them, every converter each analyzer carried and the NO2 it reduced, the quarterly titrations and the
services. Nothing here is written to the pack; records.py turns it into files.

    world(seed) -> dict    (hourly arrays in solar time, UTC+1, the network's clock)"""
import datetime as dt

import numpy as np

import params as P

# code, name, type, mean NO2 (ug/m3), NO/NO2 mass ratio, analyzer serial, scheduled service (month, day)
STATIONS = [
    ("BP01", "Gazzolo Po - via Emilia", "T", 68.0, 1.10, "NX4210-1187", (1, 20)),
    ("BP02", "Casalbuono - piazzale Stazione", "T", 47.0, 0.95, "NX4210-1203", (9, 22)),
    ("BP03", "Corte Mezzana - tangenziale", "T", 44.0, 0.90, "NX4210-1166", (4, 13)),
    ("BP04", "San Fermo - viale Rimembranze", "T", 45.0, 0.80, "NX4210-1219", (11, 3)),
    ("BP05", "Gazzolo Po - parco Ducale", "U", 44.0, 0.45, "NX4210-1174", (6, 8)),
    ("BP06", "Casalbuono - scuole Pascoli", "U", 33.0, 0.40, "NX4210-1191", (7, 20)),
    ("BP07", "Ponte Ghiara - centro", "U", 31.0, 0.40, "CL62-0418", (3, 9)),
    ("BP08", "Borgo Lanzone - giardini", "U", 29.0, 0.35, "CL62-0433", (10, 13)),
    ("BP09", "San Fermo - quartiere Lido", "U", 30.0, 0.38, "NX4210-1228", (5, 18)),
    ("BP10", "Villa Saliceto", "S", 25.0, 0.30, "CL62-0402", (8, 25)),
    ("BP11", "Motta Baluffa", "S", 23.0, 0.28, "CL62-0441", (12, 6)),
    ("BP12", "Castelponzone", "S", 21.0, 0.25, "CL62-0427", (5, 5)),
    ("BP13", "Zona industriale Ponte Ghiara", "I", 43.0, 0.55, "NX4210-1235", (10, 5)),
    ("BP14", "Polo chimico Casalbuono", "I", 30.0, 0.50, "CL62-0450", (9, 9)),
    ("BP15", "Isola Pescaroli", "R", 17.0, 0.18, "CL62-0395", (4, 2)),
    ("BP16", "Bosco Fontana Morta", "R", 14.0, 0.15, "CL62-0459", (6, 28)),
]
SPARE = "CL62-0466"                 # the store spare
SWAP = ("BP07", dt.date(2027, 2, 8), dt.date(2027, 3, 1))   # BP07's analyzer in the workshop, the spare in its place
SWAP_2025 = ("BP12", dt.date(2025, 7, 14), dt.date(2025, 7, 25))
OVERHAUL = (dt.date(2024, 12, 2), dt.date(2024, 12, 20))    # every converter changed, station by station
POSTPONED = ("BP08", dt.date(2028, 2, 15))                 # the 2027 service put back to February 2028

HOURS = P.DAYS * 24
T0 = dt.datetime(P.START.year, P.START.month, P.START.day)


def day(k):
    return P.START + dt.timedelta(days=int(k))


def doy(d):
    return (d - dt.date(d.year, 1, 1)).days


def eta(D, s=1.0):
    """converter efficiency after reducing D ppm-hours of NO2, for a converter whose life scale is s"""
    x = np.asarray(D, dtype=float) / s
    return P.ETA0 - P.ETA_SLOPE * x - P.ETA_CURV * np.maximum(0.0, x - P.ETA_KNEE) ** 2


DIURNAL = {
    "T": np.array([.55, .45, .40, .38, .42, .60, .95, 1.35, 1.45, 1.20, 1.00, .95, .95, .95, 1.00, 1.10, 1.25, 1.45,
                   1.55, 1.40, 1.15, .95, .80, .65]),
    "U": np.array([.75, .68, .62, .60, .62, .72, .92, 1.15, 1.25, 1.12, .98, .92, .90, .90, .95, 1.02, 1.12, 1.25,
                   1.32, 1.28, 1.15, 1.02, .92, .82]),
}
DIURNAL["S"] = 0.5 * DIURNAL["U"] + 0.5
DIURNAL["I"] = 0.6 * DIURNAL["U"] + 0.4
DIURNAL["R"] = 0.3 * DIURNAL["U"] + 0.7
for k in DIURNAL:
    DIURNAL[k] = DIURNAL[k] / DIURNAL[k].mean()


def air(rng):
    """true NO2 and NO, ug/m3, hour by hour at every station (solar time)"""
    days = np.arange(P.DAYS)
    dates = [day(k) for k in days]
    season = np.array([1.0 + 0.55 * np.cos(2 * np.pi * (doy(d) - 12) / 365.25) for d in dates])
    # one regional weather factor (inversions) shared across the valley, plus each station's own
    reg = np.zeros(P.DAYS)
    e = rng.normal(0, 0.30, P.DAYS)
    for k in range(1, P.DAYS):
        reg[k] = 0.78 * reg[k - 1] + e[k]
    no2 = np.zeros((len(STATIONS), HOURS))
    no = np.zeros((len(STATIONS), HOURS))
    wd = np.array([d.weekday() for d in dates])
    for i, (code, name, typ, mean, ratio, serial, svc) in enumerate(STATIONS):
        own = np.zeros(P.DAYS)
        e2 = rng.normal(0, 0.16, P.DAYS)
        for k in range(1, P.DAYS):
            own[k] = 0.6 * own[k - 1] + e2[k]
        week = np.where(wd >= 5, 0.80 if typ in "TU" else 0.90, 1.0)
        daily = mean * season * week * np.exp(reg - 0.5 * 0.30 ** 2 / (1 - 0.78 ** 2) + own - 0.5 * 0.16 ** 2 /
                                              (1 - 0.6 ** 2))
        prof = DIURNAL[typ]
        h = np.repeat(daily, 24) * np.tile(prof, P.DAYS) * rng.lognormal(-0.5 * 0.18 ** 2, 0.18, HOURS)
        no2[i] = h
        # NO follows traffic and the winter's stagnant mornings more steeply than NO2
        no[i] = ratio * h * np.tile(prof, P.DAYS) ** 0.8 * np.repeat(season, 24) ** 0.6 * \
            rng.lognormal(-0.5 * 0.35 ** 2, 0.35, HOURS)
    return no2, no


def services(seed):
    """each station analyzer's overhaul day and scheduled service days (2025 to 2028); BP08's 2027 service, due in the
    weeks the calibration contract changed hands, was put back to February 2028, so its 2026 converter is still in"""
    rng = np.random.default_rng(seed + 11)
    out = {}
    span = (OVERHAUL[1] - OVERHAUL[0]).days
    order = rng.permutation(len(STATIONS))
    for j, i in enumerate(order):
        code, name, typ, mean, ratio, serial, (m, d) = STATIONS[i]
        ov = OVERHAUL[0] + dt.timedelta(days=int(round(j * span / (len(STATIONS) - 1))))
        while ov.weekday() >= 5:
            ov += dt.timedelta(days=1)
        sched, done = [], []
        for y in (2025, 2026, 2027, 2028):
            s = dt.date(y, m, d)
            while s.weekday() >= 5:
                s += dt.timedelta(days=1)
            sched.append(s)
            done.append(s)
        if code == POSTPONED[0]:
            done[2] = None
            sched[3] = POSTPONED[1]
        out[code] = {"overhaul": ov, "scheduled": sched, "done": done}
    return out


def world(seed=P.SEED):
    rng = np.random.default_rng(seed)
    no2, no = air(rng)
    svc = services(seed)
    crng = np.random.default_rng(seed + 23)
    # analyzers: serial -> list of converters {installed (day index), removed, D path, s, reason}
    analyzers = {}
    titr = []          # titrations: day, serial, station, D, true eta, measured eta, kind
    events = []        # service log: day, station, serial, what
    where = {}         # serial -> array of station index (or -1 store) per hour
    for i, st in enumerate(STATIONS):
        where[st[5]] = np.full(HOURS, i)
    where[SPARE] = np.full(HOURS, -1)
    # the spare's stints at stations
    for (code, d0, d1) in (SWAP_2025, SWAP):
        i = [s[0] for s in STATIONS].index(code)
        a, b = (d0 - P.START).days * 24 + 10, (d1 - P.START).days * 24 + 12
        where[STATIONS[i][5]][a:b] = -2          # in the workshop, switched off
        where[SPARE][a:b] = i
    # quarterly titration rounds: each analyzer once a quarter on its round day
    trng = np.random.default_rng(seed + 31)
    # the contractor's quarterly rounds: second to fourth week of January, April, July and October, each analyzer on its
    # own day of the round
    slot = {st[5]: int(trng.integers(0, 15)) for st in STATIONS}
    slot[SPARE] = 7
    for serial in [st[5] for st in STATIONS] + [SPARE]:
        loc = where[serial]
        i0 = [k for k, st in enumerate(STATIONS) if st[5] == serial]
        code = STATIONS[i0[0]][0] if i0 else None
        sched = svc[code]["scheduled"] if code else [dt.date(2025, 11, 18), dt.date(2026, 11, 17),
                                                      dt.date(2027, 11, 16), dt.date(2028, 11, 14)]
        ov = svc[code]["overhaul"] if code else dt.date(2024, 12, 11)
        installs = [(ov - P.START).days]
        reasons = ["revisione generale"]
        s_conv = [float(np.exp(crng.normal(0, P.CONVERTER_SD)))]
        # the air the converter sees, ppm-hours per hour (true NO2 entering, when the analyzer runs)
        flow = np.zeros(HOURS)
        on = loc >= 0
        flow[on] = no2[loc[on], np.arange(HOURS)[on]] / P.UGM3_PER_PPB_NO2 / 1000.0
        flow[: installs[0] * 24 + 9] = 0.0
        done = svc[code]["done"] if code else sched
        sched_days = [(s - P.START).days for s in done if s is not None and s <= P.END]
        visits = []
        for y in (2025, 2026, 2027):
            for m in (1, 4, 7, 10):
                v = dt.date(y, m, 8) + dt.timedelta(days=slot[serial])
                while v.weekday() >= 5:
                    v += dt.timedelta(days=1)
                visits.append((v - P.START).days)
        D = 0.0
        cur = 0
        k_last = installs[0] * 24 + 9
        conv = []
        hour_D = np.zeros(HOURS)
        pending = None
        for k in range(installs[0], P.DAYS):
            # accumulate the day's dose hour by hour
            a, b = k * 24, k * 24 + 24
            if k == installs[0]:
                a = k * 24 + 9
            seg = flow[a:b]
            hour_D[a:b] = D + np.cumsum(seg)
            D = hour_D[b - 1] if b > a else D
            # a titration on the round day (the analyzer at a station)
            if k in visits and loc[k * 24 + 10] >= 0:
                tr = eta(hour_D[k * 24 + 10], s_conv[cur])
                m = tr + crng.normal(0, P.TITRATION_SD)
                titr.append((k, serial, int(loc[k * 24 + 10]), hour_D[k * 24 + 10], float(tr), float(m), "trimestrale",
                             cur))
                if m < P.THRESHOLD and pending is None:
                    pending = k + int(crng.integers(P.FORCED_LAG[0], P.FORCED_LAG[1] + 1))
            change = None
            if k in sched_days and k != installs[0]:
                change = "manutenzione programmata"
            if pending is not None and k == pending:
                change = "sostituzione anticipata, rendimento sotto il 95 %"
            if change:
                at = k * 24 + 11
                tr = eta(hour_D[at], s_conv[cur])
                m = tr + crng.normal(0, P.TITRATION_SD)
                if loc[at] >= 0 or serial == SPARE:
                    titr.append((k, serial, int(loc[at]), hour_D[at], float(tr), float(m), "prima della sostituzione",
                                 cur))
                conv.append({"installed": installs[cur], "removed": k, "s": s_conv[cur], "D_removed": hour_D[at],
                             "reason": reasons[cur]})
                installs.append(k)
                reasons.append(change)
                s_conv.append(float(np.exp(crng.normal(0, P.CONVERTER_SD))))
                cur += 1
                D = float(flow[at:b].sum())
                hour_D[at:b] = np.cumsum(flow[at:b])
                pending = None
                tr = eta(0.0, s_conv[cur])
                titr.append((k, serial, int(loc[at]), 0.0, float(tr), float(tr + crng.normal(0, P.TITRATION_SD)),
                             "dopo la sostituzione", cur))
        conv.append({"installed": installs[cur], "removed": None, "s": s_conv[cur], "D_removed": None,
                     "reason": reasons[cur]})
        # the converter in the analyzer each hour and its efficiency
        idx = np.full(HOURS, -1)
        eff = np.full(HOURS, np.nan)
        for j, c in enumerate(conv):
            a0 = c["installed"] * 24 + (9 if j == 0 else 11)
            a1 = HOURS if c["removed"] is None else c["removed"] * 24 + 11
            idx[a0:a1] = j
            eff[a0:a1] = eta(hour_D[a0:a1], c["s"])
        analyzers[serial] = {"converters": conv, "D": hour_D, "flow": flow, "where": loc, "conv": idx, "eff": eff}
    return {"no2": no2, "no": no, "svc": svc, "analyzers": analyzers, "titrations": titr}
