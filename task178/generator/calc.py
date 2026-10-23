"""task178 calculations shared by deliver.py and checks.py: the stage-discharge fits (the golden family and the
default path's single curve), the design standard's log-Pearson Type III and the alternative it selects."""
from __future__ import annotations

import numpy as np
from scipy import optimize, stats

import common as C


# ------------------------------------------------------------------------------- the design standard's LP3
def station_skew(x):
    n = len(x)
    m, s = x.mean(), x.std(ddof=1)
    return n * ((x - m) ** 3).sum() / ((n - 1) * (n - 2) * s ** 3)


def skew_mse(g, n):
    """the standard's Table 4.2 (Wallis, Matalas and Slack as tabulated in Bulletin 17B)"""
    ag = abs(g)
    a = -0.33 + 0.08 * ag if ag <= 0.90 else -0.52 + 0.30 * ag
    b = 0.94 - 0.26 * ag if ag <= 1.50 else 0.55
    return 10 ** (a - b * np.log10(n / 10.0))


def lp3(q_peaks, g_reg=C.REG_SKEW, mse_reg=C.REG_SKEW_MSE):
    x = np.log10(np.asarray(q_peaks, float))
    n = len(x)
    m, s = x.mean(), x.std(ddof=1)
    g = station_skew(x)
    mg = skew_mse(g, n)
    gw = (mse_reg * g + mg * g_reg) / (mse_reg + mg)
    return dict(n=n, mean=m, sd=s, g=g, mse_g=mg, gw=gw)


def lp3_q(fit, aep=C.AEP):
    k = stats.pearson3.ppf(1 - aep, fit["gw"])
    return 10 ** (fit["mean"] + k * fit["sd"])


def lp3_aep(fit, q):
    z = (np.log10(q) - fit["mean"]) / fit["sd"]
    return float(stats.pearson3.sf(z, fit["gw"]))


def pick(q100, alternatives=None):
    for name, cap in (alternatives or C.ALTERNATIVES):
        if cap >= q100:
            return name, cap
    return None, None


# ------------------------------------------------------------------------------------------- rating forms
def _pl_log(h, q, e0=None):
    """one power law Q = a (h - e)^b, least squares on log Q, offset fitted (or fixed)"""
    if e0 is None:
        def res(p):
            return np.log(q) - (p[0] + p[2] * np.log(np.clip(h - p[1], 1e-6, None)))
        p = optimize.least_squares(res, [4.5, min(h) - 0.5, 1.8], bounds=([-5, -5, 0.5], [15, min(h) - 1e-3, 5])).x
        a, e, b = np.exp(p[0]), p[1], p[2]
    else:
        X = np.log(h - e0)
        b, la = np.polyfit(X, np.log(q), 1)
        a, e = np.exp(la), e0
    return lambda x: a * np.clip(np.asarray(x, float) - e, 1e-9, None) ** b


def _pl_lin(h, q):
    def res(p):
        return q - p[0] * np.clip(h - p[1], 1e-6, None) ** p[2]
    p = optimize.least_squares(res, [100, min(h) - 0.5, 1.8], bounds=([0.01, -5, 0.5], [1e5, min(h) - 1e-3, 5])).x
    return lambda x: p[0] * np.clip(np.asarray(x, float) - p[1], 1e-9, None) ** p[2]


def single_log(h, q):
    return _pl_log(h, q)


def single_lin(h, q):
    return _pl_lin(h, q)


def quad_loglog(h, q):
    """a second-order polynomial in log Q against log (h - e), offset from the in-bank power law"""
    f = _pl_log(h, q)
    e = _offset(h, q)
    X = np.log(h - e)
    c = np.polyfit(X, np.log(q), 2)
    return lambda x: np.exp(np.polyval(c, np.log(np.clip(np.asarray(x, float) - e, 1e-9, None))))


def _offset(h, q):
    def res(p):
        return np.log(q) - (p[0] + p[2] * np.log(np.clip(h - p[1], 1e-6, None)))
    p = optimize.least_squares(res, [4.5, min(h) - 0.5, 1.8], bounds=([-5, -5, 0.5], [15, min(h) - 1e-3, 5])).x
    return p[1]


def channel_plus_floodplain(h, q, hb):
    """the channel's power law fitted below the bank, a floodplain term a d^p fitted on the measurements above it"""
    lo = h < hb
    fc = _pl_log(h[lo], q[lo])
    hi = ~lo

    def res(p):
        return np.log(q[hi]) - np.log(fc(h[hi]) + p[0] * (h[hi] - hb) ** p[1])
    p = optimize.least_squares(res, [1000, 1.6], bounds=([1, 0.5], [1e5, 4])).x
    return lambda x: fc(x) + p[0] * np.clip(np.asarray(x, float) - hb, 0, None) ** p[1]


def two_segment(h, q, hb):
    """a power law below the bank and a separate power law (own offset) above it"""
    lo = h < hb
    f1 = _pl_log(h[lo], q[lo])
    hi = ~lo

    def res(p):
        return np.log(q[hi]) - (p[0] + p[2] * np.log(np.clip(h[hi] - p[1], 1e-6, None)))
    p = optimize.least_squares(res, [6, hb - 3, 2.5], bounds=([-10, -10, 0.5], [20, hb - 0.01, 10])).x
    f2 = lambda x: np.exp(p[0]) * np.clip(np.asarray(x, float) - p[1], 1e-9, None) ** p[2]
    return lambda x: np.where(np.asarray(x, float) < hb, f1(x), f2(x))


def breakpoint_fit(h, q, grid=None):
    """the channel-plus-floodplain form with the bank stage itself fitted by least squares on log Q"""
    best = None
    for hb in (grid if grid is not None else np.arange(9.0, 11.5, 0.02)):
        lo = h < hb
        if lo.sum() < 30 or (~lo).sum() < 8:
            continue
        fc = _pl_log(h[lo], q[lo])
        hi = ~lo

        def res(p):
            return np.log(q[hi]) - np.log(fc(h[hi]) + p[0] * (h[hi] - hb) ** p[1])
        p = optimize.least_squares(res, [1000, 1.6], bounds=([1, 0.5], [1e5, 4])).x
        sse = (np.log(q[lo] / fc(h[lo])) ** 2).sum() + (res(p) ** 2).sum()
        if best is None or sse < best[0]:
            best = (sse, hb, fc, p)
    _, hb, fc, p = best
    f = lambda x: fc(x) + p[0] * np.clip(np.asarray(x, float) - hb, 0, None) ** p[1]
    f.hb = hb
    return f


def loess_loglog(h, q, frac=0.18):
    """a local linear smooth of log Q on log (h - e), evaluated by interpolation, extended at the top slope"""
    e = _offset(h, q)
    o = np.argsort(h)
    X, Y = np.log(h[o] - e), np.log(q[o])
    grid = np.linspace(X.min(), X.max(), 120)
    k = max(10, int(frac * len(X)))
    fit = []
    for g in grid:
        d = np.abs(X - g)
        idx = np.argsort(d)[:k]
        w = (1 - (d[idx] / d[idx].max()) ** 3) ** 3
        A = np.vstack([np.ones(k), X[idx] - g]).T
        beta = np.linalg.lstsq(A * w[:, None] ** 0.5, Y[idx] * w ** 0.5, rcond=None)[0]
        fit.append(beta[0])
    fit = np.array(fit)

    def f(x):
        xx = np.log(np.clip(np.asarray(x, float) - e, 1e-9, None))
        y = np.interp(xx, grid, fit)
        s = (fit[-1] - fit[-4]) / (grid[-1] - grid[-4])
        return np.exp(np.where(xx > grid[-1], fit[-1] + s * (xx - grid[-1]), y))
    return f


GOLDEN_FORMS = ("channel_plus_floodplain", "two_segment", "breakpoint_fit", "loess_loglog")


def golden_family(h, q, peaks, hb=10.2):
    out = {}
    for name, f in (("channel_plus_floodplain", channel_plus_floodplain(h, q, hb)), ("two_segment", two_segment(h, q, hb)),
                    ("breakpoint_fit", breakpoint_fit(h, q)), ("loess_loglog", loess_loglog(h, q))):
        out[name] = lp3_q(lp3(f(np.asarray(peaks))))
    return out


# ------------------------------------------------------------------------------------------------ pack readers
import csv as _csv
import datetime as _dt
import os as _os

import openpyxl as _xl


def _rows(path, skip_hash=True, preamble=0):
    with open(path, encoding="utf-8", newline="") as fh:
        lines = fh.read().splitlines()
    lines = [l for l in lines if not (skip_hash and l.startswith("#"))][preamble:]
    return list(_csv.reader(lines))


def read_stage(target):
    """(PST datetimes, stage) of the 15-minute export, re-sent rows collapsed"""
    rows = _rows(_os.path.join(target, C.F_STAGE))
    seen = {}
    for r in rows[1:]:
        seen[r[0]] = float(r[1])
    ts = sorted(seen)
    return [_dt.datetime.strptime(t, "%Y-%m-%d %H:%M") for t in ts], np.array([seen[t] for t in ts])


def _wy(d):
    return d.year + 1 if d.month >= 10 else d.year


def read_peaks(target, stage=None):
    """the 46 annual peak stages on the current datum, with each one's water year and time (PST for the record years)"""
    rows = _rows(_os.path.join(target, C.F_PEAKS), preamble=4)
    out = []
    for r in rows[1:]:
        wy = int(r[0])
        h = float(r[3]) + (C.DATUM_SHIFT if wy < 2010 else 0.0)
        out.append((wy, h, None))
    ts, h = stage if stage is not None else read_stage(target)
    wys = np.array([_wy(t) for t in ts])
    for wy in C.STAGE_WY:
        idx = np.flatnonzero(wys == wy)
        k = idx[int(np.argmax(h[idx]))]
        out.append((wy, float(h[k]), ts[k]))
    return out


def read_measurements(target):
    """(local time, gage height on the current datum, discharge cfs, quality) for every measurement"""
    wb = _xl.load_workbook(_os.path.join(target, C.F_MEAS_OLD), read_only=True)
    out = []
    for name in wb.sheetnames:
        rows = list(wb[name].iter_rows(values_only=True))
        head = rows[0]
        gi = [i for i, c in enumerate(head) if c in ("Gage ht (ft)", "Mean GH")][0]
        qi = [i for i, c in enumerate(head) if c in ("Discharge (cfs)", "Q (cfs)")][0]
        ri = [i for i, c in enumerate(head) if c in ("Rated", "Rating")][0]
        for r in rows[1:]:
            d = r[1]
            d = _dt.datetime.strptime(d, "%m/%d/%Y") if "/" in d else _dt.datetime.strptime(d, "%Y-%m-%d")
            out.append((d, float(r[gi]) + C.DATUM_SHIFT, float(r[qi]), str(r[ri])[0]))
    rows = _rows(_os.path.join(target, C.F_MEAS_NEW))
    head = rows[0]
    H = {c: i for i, c in enumerate(head)}
    for r in rows[1:]:
        d = _dt.datetime.strptime(r[H["meas_date"]] + " " + r[H["start_time"]], "%Y-%m-%d %H:%M")
        gh = float(r[H["mean_gh_ft"]]) + (C.DATUM_SHIFT if d.date() < C.DATUM_CHANGE else 0.0)
        q = float(r[H["discharge"]]) * (C.CFS_PER_CMS if r[H["discharge_unit"]] == "m3/s" else 1.0)
        out.append((d, gh, q, r[H["quality"]][0]))
    return out


def read_visits(target):
    rows = _rows(_os.path.join(target, C.F_VISITS))
    H = {c: i for i, c in enumerate(rows[0])}
    out = []
    for r in rows[1:]:
        day = r[H["visit_date"]]
        a = _dt.datetime.strptime(day + " " + r[H["arrive"]], "%Y-%m-%d %H:%M")
        b = _dt.datetime.strptime(day + " " + r[H["depart"]], "%Y-%m-%d %H:%M")
        out.append(dict(arrive=a, depart=b, staff=float(r[H["staff_gage_ft"]]), logger=float(r[H["logger_ft"]]),
                        work=r[H["work_done"]], notes=r[H["notes"]]))
    return out


def read_scada(target):
    rows = _rows(_os.path.join(target, C.F_SCADA), preamble=3)
    out = []
    for r in rows[1:]:
        out.append((_dt.datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S"), float(r[1]), float(r[2])))
    return out


# ------------------------------------------------------------------------------------------- the main call
def main_call(target, form="channel_plus_floodplain"):
    peaks = read_peaks(target)
    M = read_measurements(target)
    h = np.array([m[1] for m in M])
    q = np.array([m[2] for m in M])
    P = np.array([p[1] for p in peaks])
    f = {"channel_plus_floodplain": lambda: channel_plus_floodplain(h, q, 10.2), "two_segment": lambda: two_segment(h, q, 10.2),
         "breakpoint_fit": lambda: breakpoint_fit(h, q), "loess_loglog": lambda: loess_loglog(h, q),
         "single_log": lambda: single_log(h, q), "single_lin": lambda: single_lin(h, q),
         "quad_loglog": lambda: quad_loglog(h, q)}[form]()
    qp = f(P)
    g_reg, mse = read_skew(target)
    fit = lp3(qp, g_reg, mse)
    q100 = lp3_q(fit)
    alts = read_alternatives(target)
    return dict(peaks=peaks, qpeaks=qp, fit=fit, q100=q100, pick=pick(q100, alts), rating=f, h=h, q=q, alts=alts)


# ----------------------------------------------------------------------------------------------- ask A
def ask_a(target, stage=None, visits=None, visit_clock="local", fix_offset=True):
    """the highest river stage in each work window: readings while a hydrographer was on site dropped (visit times
    read on the local wall clock), the 2025 controller offset taken off between the swap and the reset"""
    ts, h = stage if stage is not None else read_stage(target)
    V = visits if visits is not None else read_visits(target)
    h = h.copy()
    tarr = np.array(ts, dtype="datetime64[m]")
    drop = np.zeros(len(h), bool)
    for v in V:
        a, b = v["arrive"], v["depart"]
        if visit_clock == "local":
            a, b = C.local_to_pst(a), C.local_to_pst(b)
        drop |= (tarr >= np.datetime64(a, "m")) & (tarr <= np.datetime64(b, "m"))
    if fix_offset:
        sw = [v for v in V if "Controller replaced" in v["notes"]][0]
        fx = [v for v in V if "offset reset" in v["notes"]][0]
        off = round(fx["logger"] - fx["staff"], 2)
        a = C.local_to_pst(sw["depart"]) if visit_clock == "local" else sw["depart"]
        b = C.local_to_pst(fx["depart"]) if visit_clock == "local" else fx["depart"]
        m = (tarr > np.datetime64(a, "m")) & (tarr < np.datetime64(b, "m"))
        h[m] = np.round(h[m] - off, 2)
    out = {}
    for y in C.ASK_A_YEARS:
        lo = np.datetime64(C.local_to_pst(_dt.datetime(y, 7, 15)), "m")
        hi = np.datetime64(C.local_to_pst(_dt.datetime(y, 9, 16)), "m")
        idx = np.flatnonzero((tarr >= lo) & (tarr < hi) & ~drop)
        k = idx[int(np.argmax(h[idx]))]
        out[y] = (round(float(h[k]), 2), C.pst_to_local(ts[k]).date().isoformat())
    return out


# ----------------------------------------------------------------------------------------------- ask B
def ask_b(target, stage=None, clock_fix=True, face_fix=True, as_local=False):
    ts, h = stage if stage is not None else read_stage(target)
    S = read_scada(target)
    up = C.SCADA_UPGRADE
    lev = {}
    for stamp, dist, level in S:
        if clock_fix:
            t = stamp - _dt.timedelta(hours=8) if stamp < up else C.local_to_pst(stamp)
        else:
            t = C.local_to_pst(stamp) if as_local else stamp
        face = (C.RADAR_FACE_NEW if t >= C.local_to_pst(C.BRACKET_DATE) else C.RADAR_FACE_INSTALL) if face_fix else None
        lev.setdefault(t, round(face - dist, 2) if face_fix else level)
    peaks = {p[0]: p for p in read_peaks(target, (ts, h)) if p[2] is not None}
    out = {}
    for wy in C.ASK_B_WY:
        _, hp, tc = peaks[wy]
        L = lev.get(tc)
        out[wy] = (L, round(C.DATUM_NAVD_NEW + hp - L, 2) if L is not None else None)
    return out


# --------------------------------------------------------------------------------------------- the documents
import re as _re
import subprocess as _sp


def pdf_text(path):
    return _sp.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


def read_alternatives(target):
    txt = pdf_text(_os.path.join(target, C.F_STUDY))
    out = []
    for m in _re.finditer(r"^\s*([A-G])\s{3,}.*?\s(\d{3}\.\d\d)\s+(\d{1,2},\d{3})\s*$", txt, _re.M):
        out.append((m.group(1), int(m.group(3).replace(",", ""))))
    return tuple(out)


def read_skew(target):
    txt = " ".join(pdf_text(_os.path.join(target, C.F_STANDARD)).split())
    m = _re.search(r"generalized skew for western Washington, (-?\d\.\d\d), whose mean square error is (\d\.\d+)", txt)
    return float(m.group(1)), float(m.group(2))
