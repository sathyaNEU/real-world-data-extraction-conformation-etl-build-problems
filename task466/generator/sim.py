"""Simulate the river and the town: each climatic year's 7-day low flow (the gauge's since 1951, the water-works
reports' before), the gauge's daily values that carry them, the reports' suspension seasons, and the town's operating
records from 2012 (the plant's SCADA days, Elm Hollow's master meter, the Hollow Road wells and the operator's log after
the radio failed)."""
import datetime as dt
import math

import numpy as np
from scipy import stats

import world as W

G = W.REGIONAL_SKEW
LT = math.log10(W.SUSPEND_CFS)


def _rng(*key):
    return np.random.default_rng([W.SEED] + [int(k) for k in key])


def lp3(mu, sd):
    return stats.pearson3(G, loc=mu, scale=sd)


# ---------------------------------------------------------------- each climatic year's 7-day low flow
GAUGE_MU, GAUGE_SD = 0.75, 0.22          # log10 cfs, the gauge era
REPORT_MU, REPORT_SD = 0.65, 0.25        # the earlier era, drier
GAUGE_DRY = [1965, 1964, 1963, 1966, 2002, 1957, 2016, 1980, 1995, 2023, 1999, 1962, 2020, 1991, 2024, 2022]
REPORT_DRY = [1930, 1913, 1899, 1932, 1941, 1914, 1908, 1949, 1911, 1931, 1894, 1935, 1910, 1939, 1921, 1897]
# years after 2011 that never reached the Stage 2 trigger stay above it with room
NO_STAGE2 = [2012, 2013, 2014, 2015, 2017, 2018, 2019, 2021]


TARGET_KEY = 36
OPS_KEY = 2292


def annual_targets():
    """{climatic year: target 7-day low flow, cfs} for the gauge's years 1951 to 2024 and the report years."""
    rng = _rng(TARGET_KEY)
    years = list(range(W.FIT_YEARS[0], W.FIT_YEARS[1] + 1))
    u = (np.arange(len(years)) + rng.uniform(0.3, 0.7, len(years))) / len(years)
    vals = np.sort(GAUGE_MU + GAUGE_SD * lp3(0, 1).ppf(u))
    order = GAUGE_DRY + [y for y in rng.permutation(years).tolist() if y not in GAUGE_DRY]
    gauge = dict(zip(order, vals))
    # the quiet years after 2011 keep their low season above the Stage 2 trigger with room: a low one swaps with the
    # earliest year before 2012 that is high enough
    used = set()
    for y in NO_STAGE2:
        if gauge[y] < math.log10(4.8):
            z = next(z for z in years if z < 2012 and z not in GAUGE_DRY and z not in used
                     and gauge[z] >= math.log10(5.2))
            used.add(z)
            gauge[y], gauge[z] = gauge[z], gauge[y]
    rng2 = _rng(TARGET_KEY + 1)
    ryears = [y for y in range(W.FIRST_REPORT, W.LAST_REPORT + 1) if y not in W.MISSING_REPORTS]
    uh = (np.arange(len(ryears)) + rng2.uniform(0.3, 0.7, len(ryears))) / len(ryears)
    hvals = np.sort(REPORT_MU + REPORT_SD * lp3(0, 1).ppf(uh))
    rorder = REPORT_DRY + [y for y in rng2.permutation(ryears).tolist() if y not in REPORT_DRY]
    report = dict(zip(rorder, hvals))
    return ({y: float(10 ** v) for y, v in gauge.items()}, {y: float(10 ** v) for y, v in report.items()})


# ---------------------------------------------------------------- the gauge's daily values
MONTH_LOG = [4.2, 4.1, 4.95, 5.25, 4.7, 3.75, 2.6, 1.95, 2.15, 2.95, 3.6, 4.05]   # ln cfs by month, Jan to Dec


def _template(days):
    """The seasonal log-flow curve, a smooth interpolation of the monthly values at mid-month."""
    doy = np.array([d.timetuple().tm_yday for d in days], float)
    knots = np.array([15.5 + 30.4 * m for m in range(12)])
    xs = np.concatenate([knots - 365.25, knots, knots + 365.25])
    ys = np.array(MONTH_LOG * 3)
    return np.interp(doy, xs, ys)


def _storms(n, rng, season):
    """Quickflow pulses: rain events arrive at a seasonal rate and recede over a few days (ln-space adds)."""
    q = np.zeros(n)
    rate = np.where(season == "summer", 0.12, 0.17)
    events = rng.random(n) < rate
    size = rng.lognormal(0.0, 0.8, n) * np.where(season == "summer", 0.7, 1.0)
    for i in np.nonzero(events)[0]:
        k = rng.uniform(0.25, 0.5)
        span = np.arange(0, min(25, n - i))
        q[i + span] += size[i] * np.exp(-k * span)
    return q


def daily_values(targets_by_year, extra):
    """Daily mean discharge from 1 April 1951 to the export day, every climatic year's 7-day low flow (from the
    published, rounded values) equal to its target to the rounding: the raw series, then a smooth multiplicative
    adjustment between the years' low seasons, iterated."""
    n = (W.EXPORT_DAY - W.GAUGE_START).days + 1
    days = [W.GAUGE_START + dt.timedelta(days=i) for i in range(n)]
    rng = _rng(3)
    base = _template(days)
    month = np.array([d.month for d in days])
    season = np.where((month >= 6) & (month <= 10), "summer", "other")
    # a slow anomaly (wet and dry spells) and the storms; the recession sharpens in the low season
    ar = np.zeros(n)
    eps = rng.normal(0, 0.035, n)
    for i in range(1, n):
        ar[i] = 0.985 * ar[i - 1] + eps[i]
    storm = _storms(n, rng, season)
    raw = np.exp(base + ar) * (1.0 + storm)
    cy = np.array([W.climatic_year(d) for d in days])
    targets = dict(targets_by_year)
    targets.update(extra)
    g_knot = {}
    centre = {}
    for it in range(40):
        knots_x, knots_y = [], []
        for y in sorted(targets):
            if y in centre:
                knots_x.append(centre[y])
                knots_y.append(g_knot.get(y, 0.0))
        g = np.interp(np.arange(n), knots_x, knots_y) if knots_x else np.zeros(n)
        q = raw * np.exp(g)
        m7 = np.convolve(q, np.ones(7) / 7, mode="full")[:n]
        m7[:6] = np.inf
        worst = 0.0
        for y, tgt in targets.items():
            idx = np.nonzero(cy == y)[0]
            if not len(idx):
                continue
            j = idx[np.argmin(m7[idx])]
            centre[y] = j - 3
            cur = m7[j]
            g_knot[y] = g_knot.get(y, 0.0) + math.log(tgt / cur)
            worst = max(worst, abs(math.log(tgt / cur)))
        if worst < 1e-7:
            break
    values = np.array([W.round_dv(v) for v in q])
    return days, values


def minima(days, values, approved_only=True):
    """{climatic year: (7-day low flow, the date its lowest window ends)} from the daily values, complete years."""
    n = len(values)
    m7 = np.convolve(values, np.ones(7) / 7, mode="full")[:n]
    out = {}
    cy = np.array([W.climatic_year(d) for d in days])
    for y in sorted(set(cy.tolist())):
        idx = np.nonzero(cy == y)[0]
        idx = idx[idx >= 6]
        last = dt.date(y + 1, 3, 31)
        if days[idx[-1]] < last:
            continue
        if approved_only and last > W.APPROVED_THROUGH:
            continue
        j = idx[np.argmin(m7[idx])]
        out[y] = (float(m7[j]), days[j])
    return out


# ---------------------------------------------------------------- the reports' suspension seasons
def report_seasons(report):
    """{year: season} for each report year: no suspension, or the suspension dates and the measured flow."""
    out = {}
    for y, v in sorted(report.items()):
        rng = _rng(4, y)
        if v >= W.SUSPEND_CFS:
            out[y] = dict(suspended=False, flow=v)
            continue
        depth = 1.0 - v / W.SUSPEND_CFS
        length = int(round(24 + 75 * depth + rng.uniform(-6, 6)))
        trough = dt.date(y, 8, 18) + dt.timedelta(days=int(rng.integers(0, 40)))
        start = trough - dt.timedelta(days=int(length * rng.uniform(0.5, 0.65)))
        end = start + dt.timedelta(days=length)
        spans = [(start, end)]
        if rng.random() < 0.3:                                # resumed after a rain, then suspended again
            cut = start + dt.timedelta(days=int(length * rng.uniform(0.35, 0.55)))
            gap = int(rng.integers(3, 8))
            spans = [(start, cut), (cut + dt.timedelta(days=gap), end + dt.timedelta(days=gap))]
        out[y] = dict(suspended=True, flow=v, spans=spans)
    return out


def reported_flow(y, v):
    """The flow as the report gave it: gallons a day to the nearest ten thousand before 1921, second-feet to the
    hundredth after."""
    if y < W.UNITS_CHANGE:
        return int(round(W.mgd(v) * 1e6 / 10000.0)) * 10000
    return round(v + 1e-12, 2)


def report_flow_cfs(y, rep):
    return W.cfs(rep / 1e6) if y < W.UNITS_CHANGE else float(rep)


# ---------------------------------------------------------------- the town's operating records, 2012 onward
OPS_START = dt.date(2012, 1, 1)


def stage_history(days, values, first=dt.date(2012, 1, 1)):
    """The select board's drought stages from 2012, as the Survey's real-time page drove them: a stage is declared
    when the 7-day mean falls below its level between 1 June and 30 November (Stage 1 below 6.0 cfs, Stage 2 below
    4.0) and stepped down once the 7-day mean has stood at or above the level for 14 days. Each change is posted one
    to three days after the day that triggered it and takes effect the day after posting; a step down keeps the
    higher stage in effect through the posting day. Returns the notices [(posted, stage, action, effective)]."""
    n = len(values)
    m7 = np.convolve(values, np.ones(7) / 7, mode="full")[:n]
    levels = {1: W.TRIGGER_STAGE1_CFS, 2: W.TRIGGER_STAGE2_CFS}
    state, run, changes = 0, 0, []
    for i in range(days.index(first), n):
        d = days[i]
        up = 0
        if 6 <= d.month <= 11:
            if state < 2 and m7[i] < levels[2]:
                up = 2
            elif state < 1 and m7[i] < levels[1]:
                up = 1
        if up:
            changes.append((i, state, up))
            state, run = up, 0
            continue
        if state:
            run = run + 1 if m7[i] >= levels[state] else 0
            if run >= 14:
                changes.append((i, state, state - 1))
                state, run = state - 1, 0
    notices = []
    for k, (i, old, new) in enumerate(changes):
        rng = _rng(6, i)
        posted = days[i] + dt.timedelta(days=1 + int(rng.integers(0, 3)))
        if posted > W.EXPORT_DAY:
            continue
        if new > old:
            notices.append((posted, new, "declared", posted + dt.timedelta(days=1)))
        else:
            notices.append((posted, old, "rescinded", posted))
    return notices


def periods(notices, stage):
    """[(in effect from, in effect through or None)] for one stage, from the notices, in order."""
    out, open_ = [], None
    for posted, st, action, eff in notices:
        if st == stage and action == "declared":
            open_ = eff
        elif st == stage and action == "rescinded" and open_:
            out.append((open_, eff))
            open_ = None
    if open_:
        out.append((open_, None))
    return out


def stage_on(d, table):
    for a, b in table:
        if a <= d <= (b or W.EXPORT_DAY):
            return True
    return False


def operations(days, values, stage2, stage1):
    """The town's own system demand, the wells, Elm Hollow's water and the plant's finished and raw water, by day."""
    rng = _rng(OPS_KEY)
    start = days.index(OPS_START)
    ds = days[start:]
    flow = values[start:]
    n = len(ds)
    t = np.arange(n)
    doy = np.array([d.timetuple().tm_yday for d in ds], float)
    yrs = np.array([(d - OPS_START).days / 365.25 for d in ds])
    summer = np.clip(np.sin((doy - 120) / 365.25 * 2 * math.pi * 0.98), 0, None) ** 1.4
    dryness = np.clip((np.log(40.0) - np.log(np.maximum(flow, 0.5))) / 2.4, 0, 1)
    indoor = 0.68 * (1 + 0.006 * yrs)
    outdoor = summer * (0.30 + 0.34 * dryness) * (1 + 0.004 * yrs)
    st2 = np.array([stage_on(d, stage2) for d in ds])
    st1 = np.array([stage_on(d, stage1) for d in ds])
    wk = np.array([d.weekday() for d in ds])
    outdoor = outdoor * np.where(st2, 0.30, np.where(st1, 0.82, 1.0)) * np.where(wk >= 5, 1.08, 0.98)
    indoor = indoor * np.where(st2, 0.965, 1.0)
    noise = rng.normal(0, 0.022, n)
    town = indoor + outdoor + noise
    # the Hollow Road wells: part-time support most of the year, both pumps round the clock in Stage 2
    wells = np.where(st2, 0.2885 + rng.normal(0, 0.0012, n), np.clip(0.11 + 0.10 * summer + rng.normal(0, 0.012, n), 0.06, 0.24))
    elm = 0.061 + 0.024 * summer + 0.004 * yrs / 14 + rng.normal(0, 0.0035, n)
    fin = town - wells + elm
    raw = fin * 1.034 + 0.018 + rng.normal(0, 0.004, n)
    return dict(days=ds, town=town, wells=wells, elm=elm, fin=fin, raw=raw, st2=st2)


def scada_wells(ops):
    """The wells' telemetered daily total: true until the radio failed, then the last value held."""
    out = ops["wells"].copy()
    i = ops["days"].index(W.RADIO_FAILED)
    held = round(float(out[i - 1]) * 0.55, 4)          # the station was on one pump at part load when the radio went
    out[i:] = held
    return out, held


# ---------------------------------------------------------------- everything
def everything():
    gauge_t, report_t = annual_targets()
    extra = {2025: 2.86, 2026: 4.62}                 # the 2025 low season (Stage 2) and this summer's (Stage 1 only)
    days, values = daily_values(gauge_t, extra)
    mins = minima(days, values)
    allmins = minima(days, values, approved_only=False)
    seasons = report_seasons(report_t)
    notices = stage_history(days, values)
    stage2 = periods(notices, 2)
    stage1 = periods(notices, 1)
    ops = operations(days, values, stage2, stage1)
    swells, held = scada_wells(ops)
    return dict(gauge_targets=gauge_t, report_targets=report_t, days=days, values=values, minima=mins,
                minima_all=allmins, seasons=seasons, notices=notices, stage2=stage2, stage1=stage1, ops=ops, scada_wells=swells, held=held)
