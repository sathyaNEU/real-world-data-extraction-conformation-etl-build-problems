"""Every route on the shipped pack to the 2028 setting: the reflexes a careful analyst reaches for (the record replayed
as it ran, the whole network replayed, the record re-run with the network the quality control will have in 2028, the
replay with the drifts the record's alerts cut short added back) and the family that files the golden (the re-run with
the 2028 network plus one alert for every drift the re-run never alerted before its repair). Used by checks.py (the
ladder, the forcing and the fork rows) and pair.py."""
import numpy as np

import params as P
import solve as S

K28 = P.SETTINGS


def setting(per, budget):
    ok = [k for k in K28 if per[k] <= budget]
    return min(ok) if ok else None


def _count(S_, limit, stations, repairs=None, keep=None, lookback=14, every_repair=False):
    out = {}
    for k in K28:
        days = S.alert_days_by_station(S_, k * limit, stations)
        n = sum(len(v) for v in days.values())
        if repairs is not None:
            if every_repair:
                # the alerts of no drift episode, plus one for every drift
                ep = {(i, t) for (i, a, v) in repairs if keep[i] for t in days.get(i, []) if a - lookback <= t <= v}
                n = n - len(ep) + sum(1 for r in repairs if keep[r[0]])
            else:
                n += len(S.cut_short(days, repairs, keep, lookback))
        out[k] = n / 3.0
    return out


def all_routes(target, reg=None, A=None, Sx=None, q=None):
    reg = S.register(target) if reg is None else reg
    if A is None:
        q, A, Sx = S.qc_matrix(target, reg)
    xy = reg[["x_utm", "y_utm"]].to_numpy(float)
    keep = reg["baja_prevista"].isna().to_numpy()
    every = np.ones(len(reg), bool)
    cont = np.where(keep)[0]
    allst = np.arange(len(reg))
    sd = np.nanstd(Sx, axis=0, ddof=1)
    sd0 = np.nanstd(Sx, axis=0, ddof=0)
    _, S28 = S.rerun(A, xy, keep)
    rep = S.drift_repairs(target, reg, q)
    h = S.history(target)
    hh = h[h["error_encontrado_C"].notna()]
    col = {c: j for j, c in enumerate(reg["codigo"])}
    # every adjustment the history holds, read as a drift cut short at its own day (campaign visits included)
    rep_every = [(col[c], int((d - S.START).days), int((d - S.START).days)) for c, d in zip(hh["codigo"], hh["fecha"])]
    r = {}
    # the reflexes
    r["replay_record"] = _count(Sx, sd, cont)
    r["replay_whole_network"] = _count(Sx, sd, allst)
    r["rerun_2028_network"] = _count(S28, sd, cont)
    r["replay_plus_cut_short"] = _count(Sx, sd, cont, rep, keep)
    r["rerun_plus_every_adjustment"] = _count(S28, sd, cont, rep_every, keep)
    r["rerun_plus_cut_short_closing_too"] = _count(S28, sd, cont, rep, every)
    # the golden family
    r["golden"] = _count(S28, sd, cont, rep, keep)
    r["golden_lookback_30"] = _count(S28, sd, cont, rep, keep, lookback=30)
    r["golden_lookback_60"] = _count(S28, sd, cont, rep, keep, lookback=60)
    r["golden_lookback_90"] = _count(S28, sd, cont, rep, keep, lookback=90)
    r["golden_every_drift_once"] = _count(S28, sd, cont, rep, keep, every_repair=True)
    r["golden_ddof0"] = _count(S28, sd0, cont, rep, keep)
    return r


REFLEXES = ["replay_record", "replay_whole_network", "rerun_2028_network", "replay_plus_cut_short"]
# both keys turned, one of them too far: the call lands, the counts do not
OVER = ["rerun_plus_every_adjustment", "rerun_plus_cut_short_closing_too"]
GOLDEN_FAMILY = ["golden", "golden_lookback_30", "golden_lookback_60", "golden_lookback_90", "golden_every_drift_once",
                 "golden_ddof0"]
