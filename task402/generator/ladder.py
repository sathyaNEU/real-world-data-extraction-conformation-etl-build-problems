"""Estimators on a normalised interruption frame: the golden and every rung of the ladder.

A normalised frame has one row per sustained interruption: sec (section, current key), level ('section' or
'transformer'), xf (transformer position or -1), start and end (minutes from 1 October 2020, local clock), ci
(customers interrupted), cause, cmi (customer minutes), plus the asset keys the replays read (site, riser, unit).
"""
import numpy as np
import pandas as pd

D0 = pd.Timestamp("2020-10-01")
def day(s):
    return (pd.Timestamp(s) - D0).days
Y1 = day("2024-10-01"); Y2 = day("2025-10-01"); YE = day("2026-10-01")
R_DAY = day("2025-11-01"); G_DAY = day("2025-12-01"); E_DAY = day("2026-01-01"); F_DAY = day("2026-02-01")
D_DAY = day("2025-10-01")


def med_days(daily, start_hist=day("2020-10-01"), end_hist=Y2):
    """IEEE 1366 2.5 beta: daily SAIDI (minutes) indexed by day number; returns (threshold, set of MED days)."""
    h = daily[(daily.index >= start_hist) & (daily.index < end_hist)]
    h = h[h > 0]
    lg = np.log(h.values)
    tmed = float(np.exp(lg.mean() + 2.5 * lg.std(ddof=1)))
    return tmed, set(daily.index[daily.values > tmed])


def frost_days(daymean, tmax=-3.0):
    return set(np.where(daymean <= tmax)[0])


def pair(F, W=10.0, dmin=60.0, frost=None, levels=("section",)):
    """For each interruption, minutes since the same section's previous restoration (section-level devices)."""
    S = F[F.level.isin(levels)].sort_values(["sec", "start"])
    prev_end = S.groupby("sec").end.shift(1)
    prev_dur = (S.end - S.start).groupby(S.sec).shift(1)
    prev_day = (S.start.groupby(S.sec).shift(1) // 1440)
    gap = S.start - prev_end
    ok = (gap >= 0) & (gap <= W) & (prev_dur >= dmin)
    if frost is not None:
        ok &= prev_day.isin(frost)
    out = pd.Series(False, index=F.index)
    out[S.index[ok.values]] = True
    return out


def qualifying(F, dmin=60.0, frost=None, levels=("section",)):
    q = F.level.isin(levels) & ((F.end - F.start) >= dmin)
    if frost is not None:
        q &= (F.start // 1440).isin(frost)
    return q


def golden_switching(F, med, frost, W=10.0, dmin=60.0, staged=(Y1, G_DAY), net=True, levels=("section",)):
    """The revision's cost: re-trips after its date in the review year, net of the staged-era re-trip rate."""
    F = F[~F.planned]
    keep = ~(F.start // 1440).isin(med)
    pr = pair(F, W, dmin, frost, levels) & keep
    q = qualifying(F, dmin, frost, levels) & keep & ~pr
    rest_min = F.end
    after = (rest_min >= G_DAY * 1440) & (F.start < YE * 1440)
    yr_pairs = F.ci[pr & (F.start >= G_DAY * 1440) & (F.start < YE * 1440)].sum()
    if not net:
        return float(yr_pairs)
    st = (F.start >= staged[0] * 1440) & (rest_min < staged[1] * 1440)
    rate = F.ci[pr & st].sum() / max(F.ci[q & st].sum(), 1)
    return float(yr_pairs - rate * F.ci[q & after].sum())


def in_year(F, med, start=Y2):
    return (F.start >= start * 1440) & (F.start < YE * 1440) & ~(F.start // 1440).isin(med) & ~F.planned


def replay_heat_pumps(F, med, rebate_xf):
    """Overload interruptions on service transformers serving members connected under the waiver, after connection."""
    m = in_year(F, med) & (F.level == "transformer") & (F.cause == "OVLD")
    cd = F.xf.map(rebate_xf)
    return float(F.ci[m & cd.notna() & (F.start >= cd.fillna(1e9) * 1440)].sum())


def replay_guards(F, med, sites_2026, start=E_DAY):
    m = in_year(F, med, start) & (F.cause == "ANML") & F.site.isin(sites_2026)
    return float(F.ci[m].sum())


def replay_risers(F, med, risers_2025, start=D_DAY):
    m = in_year(F, med, start) & (F.cause == "UGTERM") & F.riser.isin(risers_2025)
    return float(F.ci[m].sum())


def replay_supplier(F, med, unit_fit):
    """Failures of units fitted by the new supplier from 1 February 2026, on the position the unit held."""
    m = in_year(F, med, F_DAY) & (F.level == "transformer") & (F.cause == "XFMR")
    fd = F.xf.map(unit_fit)
    return float(F.ci[m & fd.notna() & (F.start >= fd.fillna(1e9) * 1440)].sum())


def category_rise(F, med, cause, y1=Y1, y2=Y2):
    a = F.ci[(F.start >= y1 * 1440) & (F.start < y2 * 1440) & ~(F.start // 1440).isin(med) & (F.cause == cause) & ~F.planned].sum()
    b = F.ci[in_year(F, med) & (F.cause == cause)].sum()
    return float(b - a)


def scope_did(F, med, treat_secs, cause="OVLD", bands=None, eheat=None):
    """The policy's sections against the rest, overload interruptions, year on year, scaled by section counts."""
    yr1 = (F.start >= Y1 * 1440) & (F.start < Y2 * 1440) & ~(F.start // 1440).isin(med) & ~F.planned
    yr2 = in_year(F, med)
    ov = F.cause == cause
    allsec = set(F.sec.unique())
    def did(t, c):
        ratio = len(t) / max(len(c), 1)
        it = F.sec.isin(t); ic = F.sec.isin(c)
        return (F.ci[yr2 & ov & it].sum() - F.ci[yr2 & ov & ic].sum() * ratio) - (F.ci[yr1 & ov & it].sum() - F.ci[yr1 & ov & ic].sum() * ratio)
    if bands is None:
        return float(did(set(treat_secs), allsec - set(treat_secs)))
    tot = 0.0
    b = np.digitize([eheat[s] for s in range(len(eheat))], bands)
    for k in range(1, len(bands) + 1):
        t = {s for s in treat_secs if b[s] == k}
        c = {s for s in range(len(eheat)) if b[s] == k and s not in treat_secs}
        if t and c:
            tot += did(t, c)
    return float(tot)
