"""Centre every graded figure of the agenda groups in its rounding bin by nudging one revolving
facility's drawn balance per group and quarter (whole pounds, inside the facility limit)."""
import math
import truth
import world

KNOB = {"X": "X2_RCF", "W": "W1_RCF", "A": "AB_RCF", "B": "B3_RCF", "C": "C1_RCF", "D": "D2_RCF"}
REQ_CCF = {"X": 1.0, "W": 1.0, "A": 1.0, "B": 0.5, "C": 1.0, "D": 0.5}


def bin_margin_1dp(v):
    """distance of v (pounds) from the nearest rounding edge at GBP 0.1m, in units of the bin"""
    f = (v / 1e5) % 1.0
    return abs(f - 0.5)


def floor_margin(v):
    f = v % 1.0
    return min(f, 1 - f)


class _Sub:
    pass


_SUBW = {}


def group_state(w, R, k, limits):
    top = w.groups[k]["top"]
    if k not in _SUBW:
        sw = _Sub()
        sw.fac = w.fac
        sw.sec = [s for s in w.sec if R.top(s["lei"]) == top]
        sw.drv = [n for n in w.drv if R.top(n["lei"]) == top]
        sw.facg = [f for f in w.fac if R.top(f.lei) == top]
        _SUBW[k] = sw
    sw = _SUBW[k]
    series, books = [], None
    for t in range(5):
        parts = {"loans_drawn": 0.0, "undrawn": 0.0, "securities": 0.0, "derivatives": 0.0}
        for f in sw.facg:
            if f.limit[t] is None:
                continue
            tot = truth.fac_exposure(f, t, all_facilities=w.fac)
            if tot == 0.0:
                continue
            dr = f.drawn[t] / truth.FX[f.ccy][t]
            parts["loans_drawn"] += dr
            parts["undrawn"] += tot - dr
        for s in sw.sec:
            parts["securities"] += truth.sec_exposure(s, t)
        for n in sw.drv:
            parts["derivatives"] += truth.drv_exposure(n, t)
        series.append(sum(parts.values()))
        if t == 4:
            books = parts
    return series, books


def ok_quarter(v, m=0.12):
    return bin_margin_1dp(v) >= m


def check(series, books, limit_m, req_m, ccf, final=True):
    for v in series:
        if not ok_quarter(v):
            return False
    if not final:
        return True
    slope = truth.ls_slope(series)
    proj = series[-1] + slope
    if not ok_quarter(proj):
        return False
    util = proj / (limit_m * 1e6) * 1000
    if abs((util % 1.0) - 0.5) < 0.12:
        return False
    for b in books.values():
        if b and not ok_quarter(b):
            return False
    room = (limit_m * 1e6 - proj) / ccf / 1e5
    if room > 0 and room / 10 < req_m:
        if floor_margin(room) < 0.18:
            return False
    return True


def tune(w, limits_agenda, requests):
    _SUBW.clear()
    truth._MS.clear()
    R = truth.Resolver(w, world.PROJ_DATE)
    out = {}
    for k, fk in KNOB.items():
        f = getattr(w, k)["fac"][fk]
        lim_m = limits_agenda[k]
        req_m = requests[k][2]
        ccf = REQ_CCF[k]
        for t in range(5):
            base = f.drawn[t]
            done = False
            for step in range(0, 400):
                for sgn in (1, -1):
                    d = sgn * step * 3700.0
                    v = round(base + d, 2)
                    if v < 0 or v > f.limit[t] * 1e6 * 0.98:
                        continue
                    f.drawn[t] = v
                    series, books = group_state(w, R, k, None)
                    final = (t == 4)
                    # quarters already fixed must stay fine; the quarter being tuned must pass
                    if final:
                        good = check(series, books, lim_m, req_m, ccf, True)
                    else:
                        good = ok_quarter(series[t])
                    if good:
                        done = True
                        break
                if done:
                    break
            if not done:
                raise SystemExit("tune failed for %s quarter %d" % (k, t))
        out[k] = [round(x, 2) for x in f.drawn]
    return out
