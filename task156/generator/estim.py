"""The golden method, run on the shipped files in target/ and nothing else.

The call: PS03's inflow on the 2024 to 2026 SCADA record is the town's dry weather flow, an infiltration that runs
with the length of the catchment's sewer lying below the terrace water table (the regional council's bore against the
asset register's inverts), and a storm response with a fast part and a slow part, the slow part again scaled by that
length. Fitted on the meter and checked on storms it was not fitted on, the model is run through every hour of the
consent's 2004 to 2023 record, each day with its own water table, with and without the subdivision's code of practice
flow and with the upgrade's storage, and the overflows are counted the consent's way. The asks are in asks.py."""
from __future__ import annotations

import csv
import datetime as dt
import functools
import os
import zoneinfo

import numpy as np

AKL = zoneinfo.ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc
NZST = dt.timezone(dt.timedelta(hours=12))
H0 = dt.datetime(2003, 12, 31, 12, tzinfo=UTC)
H1 = dt.datetime(2026, 10, 31, 11, tzinfo=UTC)
NH = int((H1 - H0).total_seconds() // 3600)

F_SCADA = "ps03_riverbank_rd_scada_15min_2024-2026.csv"
F_RAIN = "krc_rainfall_1187_hourly_2004-2025.csv"
F_RAIN26 = "krc_rainfall_1187_15min_2026_provisional.csv"
F_BORE = "krc_groundwater_72_1043_daily_2004-2026.csv"
F_ASSETS = "rauwhero_wastewater_assets_2026-10.xlsx"

QP = 112.0            # the 2023 drawdown test, both pumps (data sheet)
STORE = 350.0         # duty start to the weir crest (data sheet)
UPGRADE = 1100.0      # the brief's tank
WEIR = 4.20           # weir crest above the wet well floor (data sheet)
SUB_DWELLINGS = 260   # the servicing report, full development
OCC, LPD = 2.7, 200.0
TABLE_5_2 = [0.45, 0.38, 0.34, 0.33, 0.37, 0.52, 0.98, 1.55, 1.80, 1.62, 1.38, 1.20,
             1.10, 1.03, 0.97, 0.95, 1.00, 1.10, 1.26, 1.36, 1.27, 1.05, 0.82, 0.57]


def hidx(t):
    return int((t - H0).total_seconds() // 3600)


@functools.lru_cache(maxsize=4)
def clock():
    utc = [H0 + dt.timedelta(hours=i) for i in range(NH)]
    loc = [u.astimezone(AKL) for u in utc]
    nz = [u.astimezone(NZST) for u in utc]
    C = type("C", (), {})()
    C.year = np.array([x.year for x in nz])
    C.how = np.array([x.weekday() * 24 + x.hour for x in loc])
    C.how_nzst = np.array([x.weekday() * 24 + x.hour for x in nz])
    C.hour = np.array([x.hour for x in loc])
    C.day = np.array([(x.date() - dt.date(2004, 1, 1)).days for x in nz])
    C.nd = int(C.day[-1]) + 1
    C.meter = np.array([u >= dt.datetime(2023, 12, 31, 11, tzinfo=UTC) for u in utc])
    return C


def read_rows(path, skip_to_header):
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith(skip_to_header))
    return list(csv.reader(lines[i:]))


@functools.lru_cache(maxsize=4)
def rainfall(target, shift=0):
    """Hourly rain on the UTC hour index: the archive's NZST hour-ending totals to 2025, the provisional 15-minute
    telemetry (UTC, interval end) summed into hours for 2026. shift moves the archive's hours (a stamp misread)."""
    r = np.zeros(NH)
    for row in read_rows(os.path.join(target, F_RAIN), "Time (NZST)")[1:]:
        end = dt.datetime.strptime(row[0], "%d/%m/%Y %H:%M").replace(tzinfo=NZST)
        i = hidx(end - dt.timedelta(hours=1)) + shift
        if 0 <= i < NH:
            r[i] = float(row[1])
    for row in read_rows(os.path.join(target, F_RAIN26), "interval_end_utc")[1:]:
        if not row[1]:
            continue
        end = dt.datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        i = hidx(end - dt.timedelta(minutes=15))
        if 0 <= i < NH:
            r[i] += float(row[1])
    return np.round(r, 1)


@functools.lru_cache(maxsize=4)
def water_level(target):
    """Daily water table (m NZVD2016): the measuring point's level less the depth to water, gaps joined straight."""
    rows = read_rows(os.path.join(target, F_BORE), "Date")
    head = open(os.path.join(target, F_BORE), encoding="utf-8").read().split("Measuring point,Top of casing at ")[1]
    mp = float(head.split(" m NZVD2016")[0])
    C = clock()
    lv = np.full(C.nd, np.nan)
    for row in rows[1:]:
        d = dt.date.fromisoformat(row[0])
        k = (d - dt.date(2004, 1, 1)).days
        if row[1] and 0 <= k < C.nd:
            lv[k] = mp - float(row[1])
    ok = ~np.isnan(lv)
    lv[~ok] = np.interp(np.nonzero(~ok)[0], np.nonzero(ok)[0], lv[ok])
    return lv


@functools.lru_cache(maxsize=4)
def ps03_pipes(target, include_abandoned=False):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, F_ASSETS), read_only=True)
    out = []
    for i, row in enumerate(wb["Gravity mains"].iter_rows(values_only=True)):
        if i == 0 or row[0] is None:
            continue
        if not str(row[1]).startswith("PS03"):
            continue
        if row[10] != "In service" and not include_abandoned:
            continue
        out.append((float(row[4]), float(row[9]), float(row[8]), int(row[5]), str(row[6])))
    return tuple(out)


def lsub(levels, pipes, ref="invert", skip_pe=False):
    levels = np.asarray(levels, dtype=float)
    out = np.zeros_like(levels)
    for L, dsi, usi, dia, mat in pipes:
        if skip_pe and mat == "PE":
            continue
        off = {"invert": 0.0, "centre": dia / 2000.0, "crown": dia / 1000.0}[ref]
        out += L * np.clip((levels - dsi - off) / max(usi - dsi, 1e-6), 0.0, 1.0)
    return out / 1000.0


@functools.lru_cache(maxsize=4)
def scada_hourly(target):
    """The SCADA's calculated inflow averaged into UTC hours (all four quarters good), and the hours in which the
    wet well stood at or above the weir crest (the RTU's inflow then reads the pumps alone)."""
    q = np.full(NH, np.nan)
    spill = np.zeros(NH, dtype=bool)
    acc = {}
    for row in read_rows(os.path.join(target, F_SCADA), "timestamp_utc")[1:]:
        t = dt.datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
        i = hidx(t)
        a = acc.setdefault(i, [0.0, 0, False])
        if row[4] == "Good":
            a[0] += float(row[1])
            a[1] += 1
            if float(row[2]) >= WEIR:
                a[2] = True
    for i, (s, n, sp) in acc.items():
        if 0 <= i < NH:
            if n == 4:
                q[i] = s / 4
            spill[i] = sp
    return q, spill


def uh(tp, tb):
    t = np.arange(0, tb + 0.5, 1.0)
    u = np.clip(np.where(t <= tp, t / tp, (tb - t) / (tb - tp)), 0, None)
    return u / u.sum()


SHAPES_F = [(1.0, 4), (1.0, 6), (1.5, 6), (1.0, 8), (2.0, 8)]
SHAPES_S = [(6.0, 48), (9.0, 60), (9.0, 72), (12.0, 72), (12.0, 96)]


def fit(target, conditioned=True, ref="invert", skip_pe=False, shapes=None, train=None, include_abandoned=False,
        dry_h=72, keep_spill=False, profile_clock="local", rain_shift=0, exposure=None):
    """Fit on the meter's good hours (spill hours out). conditioned=False is the single response: the dry weather
    flow by hour of the week as the meter ran, and one fast and one slow response per millimetre. The other keywords
    are the conventions checks.py turns one at a time."""
    C = clock()
    rain = rainfall(target, rain_shift)
    q, spill = scada_hourly(target)
    lv = water_level(target)
    ls_d = lsub(lv, ps03_pipes(target, include_abandoned), ref, skip_pe) if exposure is None else exposure
    ls_h = ls_d[C.day]
    how = C.how if profile_clock == "local" else C.how_nzst
    good = C.meter & ~np.isnan(q) & (keep_spill | ~spill)
    if train is not None:
        good &= train
    r72 = np.convolve(rain, np.ones(dry_h + 1))[:NH]
    dry = good & (r72 == 0)
    if conditioned:
        X = np.zeros((int(dry.sum()), 169))
        X[np.arange(int(dry.sum())), how[dry]] = 1.0
        X[:, 168] = ls_h[dry]
        coef = np.linalg.lstsq(X, q[dry], rcond=None)[0]
        base = coef[:168]
        g = coef[168]
        base_h = base[how] + g * ls_h
    else:
        base = np.array([q[dry & (how == k)].mean() for k in range(168)])
        g = 0.0
        base_h = base[how]
    best = None
    for sf in ([shapes[0]] if shapes else SHAPES_F):
        F = np.convolve(rain, uh(*sf))[:NH] / 3.6
        for ss in ([shapes[1]] if shapes else SHAPES_S):
            S = np.convolve(rain * (ls_h if conditioned else 1.0), uh(*ss))[:NH] / 3.6
            A = np.vstack([F[good], S[good]]).T
            ab = np.linalg.lstsq(A, (q - base_h)[good], rcond=None)[0]
            pred = base_h + ab[0] * F + ab[1] * S
            rmse = float(np.sqrt(np.mean((q - pred)[good] ** 2)))
            if best is None or rmse < best["rmse"]:
                best = dict(rmse=rmse, sf=sf, ss=ss, a=float(ab[0]), b=float(ab[1]))
    best.update(base=base, g=float(g), ls_d=ls_d, conditioned=conditioned, ref=ref, profile_clock=profile_clock,
                rain_shift=rain_shift)
    return best


def model_flow(target, M, extra=None):
    C = clock()
    rain = rainfall(target, M.get("rain_shift", 0))
    ls_h = M["ls_d"][C.day]
    how = C.how if M.get("profile_clock", "local") == "local" else C.how_nzst
    F = np.convolve(rain, uh(*M["sf"]))[:NH] / 3.6
    S = np.convolve(rain * (ls_h if M["conditioned"] else 1.0), uh(*M["ss"]))[:NH] / 3.6
    q = M["base"][how] + M["g"] * ls_h + M["a"] * F + M["b"] * S
    if extra is not None:
        q = q + extra
    return q


def subdivision(dwellings=SUB_DWELLINGS, profile="table"):
    C = clock()
    f = np.array(TABLE_5_2) / np.mean(TABLE_5_2)
    if profile == "flat":
        f = np.ones(24)
    return dwellings * OCC * LPD / 86400.0 * f[C.hour]


def overflows(q, qp=QP, store=STORE, sep=24):
    s = 0.0
    hours = []
    for i in range(len(q)):
        s += (q[i] - qp) * 3.6
        if s < 0:
            s = 0.0
        elif s > store:
            hours.append(i)
            s = store
    ev = []
    last = -10 ** 9
    for i in hours:
        if i - last > sep:
            ev.append(i)
        last = i
    return np.array(ev, dtype=int)


def replay(target, M, extra=None, store=STORE):
    C = clock()
    q = model_flow(target, M, extra)
    ev = overflows(q, store=store)
    years = C.year[ev]
    per = np.array([int(np.sum(years == y)) for y in range(2004, 2024)])
    meter = [int(np.sum(years == y)) for y in (2024, 2025, 2026)]
    return dict(mean=float(per.mean()), per_year=per, meter=meter)


@functools.lru_cache(maxsize=2)
def golden(target):
    M = fit(target, True)
    sub = subdivision()
    ex = replay(target, M)
    su = replay(target, M, sub)
    up = replay(target, M, sub, STORE + UPGRADE)
    N = fit(target, False)
    nex = replay(target, N)
    nsu = replay(target, N, sub)
    C = clock()
    lv = water_level(target)
    md = np.array([dt.date(2004, 1, 1) + dt.timedelta(days=int(k)) >= dt.date(2024, 1, 1) for k in range(C.nd)])
    rd = np.array([dt.date(2004, 1, 1) + dt.timedelta(days=int(k)) <= dt.date(2023, 12, 31) for k in range(C.nd)])
    G = dict(model=M, naive=N, existing=ex, with_sub=su, with_upgrade=up, naive_existing=nex, naive_sub=nsu,
             lsub_meter_max=float(M["ls_d"][md].max()), lsub_replay_max=float(M["ls_d"][rd].max()),
             lsub_meter_median=float(np.median(M["ls_d"][md])),
             lsub_replay_median=float(np.median(M["ls_d"][rd])), level_meter_max=float(lv[md].max()))
    return G


def validation(target):
    """Out of sample: each model fitted on 2024 and 2025 but the June 2025 high-river weeks, scored on those weeks
    and on 2026; the score is the hourly root mean square error on the held-out good hours."""
    C = clock()
    q, spill = scada_hourly(target)
    utc0 = H0
    t = np.array([utc0 + dt.timedelta(hours=i) for i in range(NH)])
    spell = np.array([dt.datetime(2025, 5, 25, tzinfo=UTC) <= x < dt.datetime(2025, 7, 20, tzinfo=UTC) for x in t])
    late = np.array([x >= dt.datetime(2025, 12, 31, 11, tzinfo=UTC) for x in t])
    train = C.meter & ~spell & ~late
    out = {}
    for name, cond in (("conditioned", True), ("single", False)):
        M = fit(target, cond, train=train)
        pred = model_flow(target, M)
        good = ~np.isnan(q) & ~spill
        for part, sel in (("high river weeks", spell & good), ("2026", late & good)):
            out[(name, part)] = float(np.sqrt(np.mean((q - pred)[sel] ** 2)))
            out[(name, part, "bias")] = float(np.mean((q - pred)[sel]))
    return out
