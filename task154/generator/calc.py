"""Read the shipped pack and compute everything the goldens, the checks and the ceiling need: the aquifer's
transmissivity and storage from the 2014 test, the derogation test under every aquifer model a solver could take,
the long record's verdict on each, and both asks with every stop a response could reach."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import re
from collections import defaultdict

import numpy as np
import openpyxl
from scipy.optimize import brentq, least_squares
from scipy.special import exp1

import common as K
import records as R


# ------------------------------------------------------------------------------------------------- reading the pack
def _csv(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


class Bundle:
    pass


def read_test(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    series = {}
    for bh in ("BH2", "OB1", "OB2", "OB3"):
        ws = wb[bh]
        rows = list(ws.iter_rows(values_only=True))
        if bh != "OB3":
            data = rows[7:]
            t = [dt.datetime.strptime("%s %s" % (r[0], r[1]), "%Y-%m-%d %H:%M:%S") for r in data]
            lvl = np.array([float(r[2]) for r in data])
        else:
            data = rows[7:]
            t = [K.local_to_utc(dt.datetime.strptime(r[0], "%d/%m/%Y %H:%M")) for r in data]
            lvl = np.array([float(r[1]) / 9.80665 for r in data])
        series[bh] = (t, lvl)
    fs = list(wb["Field sheet"].iter_rows(values_only=True))
    on = K.local_to_utc(dt.datetime.strptime(fs[1][1], "%d/%m/%Y %H:%M"))
    flows = [float(r[4]) for r in fs[7:] if r and r[2] == "BH2" and r[4] not in (None, "")]
    return series, on, flows


def bundle(target):
    b = Bundle()
    b.target = target
    b.test, b.pump_on, b.flows = read_test(os.path.join(target, R.F_TEST))
    b.q_test = float(np.mean(b.flows)) * 86.4                      # m3/d, the field sheet's flow checks
    b.survey = {}
    for r in _csv(os.path.join(target, R.F_SURVEY)):
        b.survey.setdefault(r["point"], (float(r["easting"]), float(r["northing"])))
    b.obs = _csv(os.path.join(target, R.F_OBS))
    b.rmb = _csv(os.path.join(target, R.F_RMB))
    b.telem = _csv(os.path.join(target, R.F_TELEM))
    b.pump = _csv(os.path.join(target, R.F_PUMP))
    b.runs = _csv(os.path.join(target, R.F_RUNS))
    b.qc = _csv(os.path.join(target, R.F_QC))
    wb = openpyxl.load_workbook(os.path.join(target, R.F_SKU), read_only=True, data_only=True)
    b.sku = {r[0]: (r[1], float(r[2])) for r in list(wb["SKU"].iter_rows(values_only=True))[1:]}
    wb = openpyxl.load_workbook(os.path.join(target, R.F_TICKETS), read_only=True, data_only=True)
    b.tickets = []
    for ws in wb.worksheets:
        for r in list(ws.iter_rows(values_only=True))[4:]:
            if r and r[0] and str(r[0]).isdigit():
                b.tickets.append(dict(sheet=ws.title, no=str(r[0]), date=dt.datetime.strptime(r[1], "%d/%m/%Y").date(),
                                      t_in=r[3], t_out=r[4], litres=int(r[5])))
    return b


def local_xy(b, point):
    e, n = b.survey[point]
    e0, n0 = b.survey["BH2"]
    return (e - e0, n - n0)


def protected(b):
    """The letter's table: name, local xy from the grid reference, available drawdown."""
    import docs as D
    out = []
    e0, n0 = b.survey["BH2"]
    for name, lic, holder, gr, rest, avail, qd in D.protected_rows():
        _, ee, nn = gr.split()
        out.append((name, (300000 + int(ee) - e0, 300000 + int(nn) - n0), float(avail)))
    return out


def fault(b):
    """The memoir's two points on the fault trace, local frame: the image of BH2 across the line through them."""
    import docs as D
    e0, n0 = b.survey["BH2"]
    (ea, na), (eb, nb) = D.fault_points()
    a = np.array([ea - e0, na - n0])
    c = np.array([eb - e0, nb - n0])
    d = (c - a) / np.linalg.norm(c - a)
    foot = a + np.dot(-a, d) * d                    # foot of the perpendicular from BH2 (origin)
    return a, c, 2.0 * foot


# ------------------------------------------------------------------------------------------------- aquifer models
def resp(xy, t, T, S, img=None, coef=1.0):
    t = np.atleast_1d(np.asarray(t, float))
    out = np.zeros_like(t)
    m = t > 0
    r2 = max(xy[0] ** 2 + xy[1] ** 2, 0.0225)
    out[m] = exp1(r2 * S / (4 * T * t[m])) / (4 * math.pi * T)
    if img is not None:
        ri2 = (xy[0] - img[0]) ** 2 + (xy[1] - img[1]) ** 2
        out[m] += coef * exp1(ri2 * S / (4 * T * t[m])) / (4 * math.pi * T)
    return out


def test_drawdowns(b, bh):
    t, lvl = b.test[bh]
    tm = np.array([(x - b.pump_on).total_seconds() / 60.0 for x in t])
    pre = lvl[(tm > -60) & (tm <= 0)].mean()
    return tm, pre - lvl


def fit_theis(b, obs=("OB1", "OB2", "OB3"), t_from=1.0, t_to=None, q=None, cj=False):
    """Theis (or the Cooper-Jacob straight line, cj, on the readings late enough for it: u under 0.02 at a first Theis
    fit) fitted to the observation boreholes' drawdown in the pumping phase; returns T (m2/d) and S."""
    q = q or b.q_test
    t_to = t_to or K.TEST_PUMP_H * 60.0
    xs = []
    for ob in obs:
        tm, s = test_drawdowns(b, ob)
        m = (tm >= t_from) & (tm <= t_to)
        xs.append((local_xy(b, ob), tm[m] / 1440.0, s[m]))
    if cj:
        T0, S0 = fit_theis(b, obs, t_from, t_to, q)
        sel = []
        for xy, td, s in xs:
            r2 = xy[0] ** 2 + xy[1] ** 2
            keep = r2 * S0 / (4 * T0 * td) < 0.02
            if keep.sum() > 30:
                sel.append((xy, td[keep], s[keep]))
        xs = sel

    def res(p):
        T, S = math.exp(p[0]), math.exp(p[1])
        out = []
        for xy, td, s in xs:
            if cj:
                r2 = xy[0] ** 2 + xy[1] ** 2
                u = r2 * S / (4 * T * td)
                out.append(q / (4 * math.pi * T) * (-0.5772 - np.log(u)) - s)
            else:
                out.append(q * resp(xy, td, T, S) - s)
        return np.concatenate(out)
    f = least_squares(res, [math.log(150.0), math.log(1e-4)])
    return math.exp(f.x[0]), math.exp(f.x[1])


def assessment(q_new, xy, T, S, img=None, coef=1.0, scale=1.0):
    t_tot = ((K.COMMON_END + dt.timedelta(days=1)) - K.LICENCE_START).days
    t_new = ((K.COMMON_END + dt.timedelta(days=1)) - K.NEW_FROM).days
    return scale * float(K.LICENSED_QD * resp(xy, t_tot, T, S, img, coef)[0]
                         + (q_new - K.LICENSED_QD) * resp(xy, t_new, T, S, img, coef)[0])


def largest(prot, T, S, img=None, coef=1.0, scale=1.0):
    per = {}
    for name, xy, avail in prot:
        per[name] = brentq(lambda q: assessment(q, xy, T, S, img, coef, scale) - avail, -50000.0, 500000.0)
    worst = min(per, key=per.get)
    return per[worst], worst, per


def nearest(x, unit):
    return float(math.floor(x / unit + 0.5) * unit)


def largest_passing_round(cont, unit=100.0):
    """The largest whole-hundred quantity that passes, given the continuous limit."""
    return float(math.floor(cont / unit) * unit)


# ------------------------------------------------------------------------------------------------- the long record
_OPS = {}


def ops_cached():
    import world as W
    if "O" not in _OPS:
        _OPS["O"] = W.ops()
    return _OPS["O"]


def returns_monthly(b):
    """Each month's volume abstracted (m3) as the returns give it, April 2015 to March 2026, read from the PDF."""
    from pypdf import PdfReader
    import docs as D
    text = "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(b.target, D.F_RETURNS)).pages)
    names = {dt.date(2000, m, 1).strftime("%B"): m for m in range(1, 13)}
    out = {}
    for mname, y, v in re.findall(r"^(%s) (\d{4})\s*\n\s*([\d,]+)\s*$" % "|".join(names), text, re.M):
        out[(int(y), names[mname])] = float(v.replace(",", ""))
    return out


def abstraction_history(b):
    """Monthly mean abstraction (m3/d) since April 2015, from the returns' monthly volumes."""
    import world as W
    return {k: v / W.month_days(*k) for k, v in returns_monthly(b).items()}


def ob_record(b):
    rec = defaultdict(dict)
    for r in b.obs:
        y, m = map(int, r["month"].split("-"))
        ct_now = None
        rec[r["borehole"]][(y, m)] = float(r["mean_depth_to_water_m_btoc"])
    return rec


def ob_levels(b):
    """Monthly mean levels (m above datum) at OB1 to OB3: depth to water from the casing top in force that month."""
    import common as KK
    surv = defaultdict(list)
    with open(os.path.join(b.target, R.F_SURVEY), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["casing_top_maod"]:
                surv[r["point"]].append((float(r["casing_top_maod"]), r["note"]))
    out = defaultdict(dict)
    rec = ob_record(b)
    for ob, months in rec.items():
        for (y, m), dtw in months.items():
            # OB2's casing top was raised on 18 February 2020: the March 2020 mean is the first read from it
            ct = surv[ob][1][0] if (ob == "OB2" and (y, m) >= (2020, 3)) else surv[ob][0][0]
            out[ob][(y, m)] = ct - dtw
    return out


def rmb_monthly(b):
    acc = defaultdict(list)
    for r in b.rmb:
        d = dt.datetime.strptime(r["Date"], "%d/%m/%Y").date()
        acc[(d.year, d.month)].append(float(r["Level (mAOD)"]))
    return {k: float(np.mean(v)) for k, v in acc.items()}


def model_series(xy, months, monthly, T, S, img=None, coef=1.0):
    out = []
    for (y, m) in months:
        mid = dt.datetime(y, m, 1) + dt.timedelta(days=(dt.date(y + (m == 12), 1 if m == 12 else m + 1, 1) -
                                                        dt.date(y, m, 1)).days / 2.0)
        s, prev = 0.0, 0.0
        for (yy, mm) in sorted(monthly):
            st = dt.datetime(yy, mm, 1)
            if st >= mid:
                break
            q = monthly[(yy, mm)]
            s += (q - prev) * float(resp(xy, (mid - st).total_seconds() / 86400.0, T, S, img, coef)[0])
            prev = q
        out.append(s)
    return np.array(out)


def long_record_verdict(b, T, S, img):
    """Each model's misfit to the observation boreholes' monthly levels once the regional movement (the Windle Cross
    record, de-meaned) is taken off: the unbounded aquifer with the test's T and S, the aquifer closed by the fault,
    an unbounded aquifer refitted to the long record, and a partly sealing fault."""
    lv = ob_levels(b)
    rm = rmb_monthly(b)
    monthly = abstraction_history(b)
    months = sorted(k for k in lv["OB1"] if k in rm)
    base_rm = rm[(2015, 4)] if (2015, 4) in rm else rm[months[0]]
    obs = {}
    for ob in ("OB1", "OB2", "OB3"):
        nat = np.array([rm[k] - base_rm for k in months])
        lev = np.array([lv[ob][k] for k in months])
        obs[ob] = (local_xy(b, ob), lev - nat)          # level less the regional movement
    out = {}

    def misfit(Tm, Sm, im, coef=1.0):
        res = []
        for ob, (xy, lev) in obs.items():
            pred = model_series(xy, months, monthly, Tm, Sm, im, coef)
            rest = np.mean(lev + pred)                   # the April 2015 rest level each model implies (least squares)
            res.append(lev - (rest - pred))
        r = np.concatenate(res)
        return float(np.sqrt(np.mean(r ** 2))), r
    out["unbounded, test T and S"] = misfit(T, S, None)[0]
    out["closed by the fault, test T and S"] = misfit(T, S, img)[0]

    def res_unb(p):
        return misfit(math.exp(p[0]), math.exp(p[1]), None)[1]
    f = least_squares(res_unb, [math.log(T), math.log(S)])
    Ta, Sa = math.exp(f.x[0]), math.exp(f.x[1])
    out["unbounded, refitted to the long record"] = misfit(Ta, Sa, None)[0]

    def res_coef(p):
        return misfit(T, S, img, p[0])[1]
    fc = least_squares(res_coef, [0.5], bounds=([0.0], [1.5]))
    out["fault coefficient fitted"] = float(fc.x[0])
    out["closed by the fault, coefficient fitted"] = misfit(T, S, img, float(fc.x[0]))[0]
    return out, (Ta, Sa), months


# ------------------------------------------------------------------------------------------------- the main call
def main_call(b):
    prot = protected(b)
    T, S = fit_theis(b)
    a, c, img = fault(b)
    g_cont, g_worst, g_per = largest(prot, T, S, img)
    t_cont, t_worst, t_per = largest(prot, T, S, None)
    at1800 = {name: assessment(K.APPLIED_QD, xy, T, S, img) for name, xy, _ in prot}
    at1800_theis = {name: assessment(K.APPLIED_QD, xy, T, S, None) for name, xy, _ in prot}
    return dict(T=T, S=S, img=img, prot=prot, golden=g_cont, worst=g_worst, per=g_per, theis=t_cont,
                theis_worst=t_worst, theis_per=t_per, at1800=at1800, at1800_theis=at1800_theis)


def term_series(b, T, S, img, q_new, name):
    """The limiting borehole's predicted drawdown at the end of each licence year, 2015-16 to 2038-39."""
    xy = [p[1] for p in protected(b) if p[0] == name][0]
    out = []
    for y in range(2016, 2040):
        end = dt.date(y, 3, 31)
        t_tot = ((end + dt.timedelta(days=1)) - K.LICENCE_START).days
        t_new = ((end + dt.timedelta(days=1)) - K.NEW_FROM).days
        s = K.LICENSED_QD * float(resp(xy, t_tot, T, S, img)[0])
        if t_new > 0:
            s += (q_new - K.LICENSED_QD) * float(resp(xy, t_new, T, S, img)[0])
        out.append((end, s))
    return out


# ------------------------------------------------------------------------------------------------- ask A
def telem_local(b):
    """Each 15-minute telemetry row with its local time and its FM-1 and line-meter volumes (m3)."""
    out = []
    prev = None
    for r in b.telem:
        t = dt.datetime.strptime(r["time_utc"], "%Y-%m-%dT%H:%MZ")
        loc = K.utc_to_local(t)
        regs = [float(r["fm_l%d_register_m3" % i]) for i in (1, 2, 3, 4)]
        lines = [0.0] * 4 if prev is None else [regs[i] - prev[i] for i in range(4)]
        prev = regs
        out.append((loc, float(r["fm1_flow_ls"]) * 0.9, lines))
    return out


def pump_runs(b):
    ev = [(dt.datetime.strptime(r["timestamp"], "%d/%m/%Y %H:%M:%S"), r["event"]) for r in b.pump]
    runs = []
    st = None
    for t, e in ev:
        if e == "PUMP START":
            st = t
        elif e == "PUMP STOP" and st is not None:
            runs.append((st, t))
            st = None
    return runs


def match_tickets(b):
    """Each ticket set against the wellhead controller's runs that start between its times in and out, read on the
    ticket's own date or on the next day (a window may cross midnight), with each candidate's litres per second of
    pumping. Re-sent copies of a ticket are counted once."""
    runs = pump_runs(b)
    starts = sorted(runs)
    seen = set()
    out = []
    for tk in b.tickets:
        key = (tk["sheet"], tk["no"], tk["date"], tk["t_in"], tk["t_out"], tk["litres"])
        if key in seen:
            continue
        seen.add(key)
        hi, mi = map(int, tk["t_in"].split(":"))
        ho, mo = map(int, tk["t_out"].split(":"))
        cands = []
        for day in (tk["date"], tk["date"] + dt.timedelta(days=1)):
            t_in = dt.datetime.combine(day, dt.time(hi, mi))
            t_out = dt.datetime.combine(day, dt.time(ho, mo)) + dt.timedelta(seconds=59)
            if t_out < t_in:
                t_out += dt.timedelta(days=1)
            for a, z in starts:
                if t_in <= a <= t_out:
                    cands.append((a, z, tk["litres"] / max((z - a).total_seconds(), 1.0)))
        out.append((tk, cands))
    return out


def bay_rate(b):
    """The bulk bay's filling rate (litres a second): the median over tickets with a single candidate run."""
    r = [c[0][2] for _, c in match_tickets(b) if len(c) == 1]
    return float(np.median(r))


def ticket_fills(b, tol=0.015):
    """Each ticket's fill on the one run whose litres per second matches the bay's rate."""
    rate = bay_rate(b)
    out = []
    for tk, cands in match_tickets(b):
        ok = [c for c in cands if abs(c[2] / rate - 1.0) <= tol]
        out.append((tk, ok))
    return out, rate


def shift_fills(b):
    """Each ticket's fill on the night shift its date names: a time in before noon is the next calendar day's (the
    shift began the evening before); the window from time in to time out may cross midnight. Returns, per ticket,
    the controller runs that start inside the window and each one's litres per second."""
    runs = sorted(pump_runs(b))
    seen = set()
    out = []
    for tk in b.tickets:
        key = (tk["sheet"], tk["no"], tk["date"], tk["t_in"], tk["t_out"], tk["litres"])
        if key in seen:
            continue
        seen.add(key)
        hi, mi = map(int, tk["t_in"].split(":"))
        ho, mo = map(int, tk["t_out"].split(":"))
        day = tk["date"] + dt.timedelta(days=1 if hi < 12 else 0)
        t_in = dt.datetime.combine(day, dt.time(hi, mi))
        t_out = dt.datetime.combine(day, dt.time(ho, mo)) + dt.timedelta(seconds=59)
        if t_out < t_in:
            t_out += dt.timedelta(days=1)
        cands = [(a, z, tk["litres"] / max((z - a).total_seconds(), 1.0)) for a, z in runs if t_in <= a <= t_out]
        out.append((tk, cands))
    return out


def ask_a(b, tankers=True, shift_dating=True):
    tl = telem_local(b)
    day_fm1 = defaultdict(float)
    for loc, v1, _ in tl:
        day_fm1[loc.date()] += v1
    day_tank = defaultdict(float)
    if tankers:
        for tk, cands in shift_fills(b):
            fill_day = cands[0][0].date() if shift_dating else tk["date"]
            day_tank[fill_day] += tk["litres"] / 1000.0
    out = {}
    import world as W
    for y, m in W.month_iter(dt.date(2026, 4, 1), dt.date(2026, 9, 1)):
        days = [dt.date(y, m, 1) + dt.timedelta(days=i) for i in range(W.month_days(y, m))]
        vol = sum(day_fm1[d] + day_tank[d] for d in days)
        over = sum(1 for d in days if day_fm1[d] + day_tank[d] > K.LICENSED_QD)
        out[(y, m)] = (vol, over)
    return out


# ------------------------------------------------------------------------------------------------- ask B
def true_sizes(b):
    """Each line 3 material's pack size during the 2025-26 licence year read off its QC net fill weights (still water
    weighs a gram a millilitre; the fills run a little over nominal), against the product master's current size."""
    acc = defaultdict(list)
    for q in b.qc:
        if q["line"] != "L3" or q["result"] != "PASS":
            continue
        t = dt.datetime.strptime(q["sample_time"], "%d/%m/%Y %H:%M")
        if dt.date(2025, 4, 1) <= t.date() <= dt.date(2026, 3, 31):
            acc[q["material"]].append(float(q["net_fill_g"]))
    out = {}
    for code, w in acc.items():
        out[code] = nearest(float(np.median(w)) / 1.0015, 50.0)
    return out


def ask_b(b, sizes="true"):
    return {k: w * 1000.0 / lit for k, (w, lit) in ask_b_parts(b, sizes).items()}


def ask_b_parts(b, sizes="true"):
    """Per local month of the 2025-26 licence year: line 3's water (m3, FM-L3's register, cleans included) and the
    litres it packed (good bottles at each material's size)."""
    import world as W
    tl = telem_local(b)
    water = defaultdict(float)
    for loc, _, lines in tl:
        water[(loc.year, loc.month)] += lines[2]
    if sizes == "true":
        sz = {c: v[1] for c, v in b.sku.items()}
        sz.update(true_sizes(b))
    elif sizes == "master":
        sz = {c: v[1] for c, v in b.sku.items()}
    else:                                            # every size read off the QC weights, sparkling included
        sz = {c: v[1] for c, v in b.sku.items()}
        acc = defaultdict(list)
        for q in b.qc:
            if q["line"] == "L3" and q["result"] == "PASS":
                acc[q["material"]].append(float(q["net_fill_g"]))
        for code, w in acc.items():
            sz[code] = float(np.median(w))
    litres = defaultdict(float)
    for r in b.runs:
        if r["line"] != "L3" or r["order_type"] != "PROD":
            continue
        t = dt.datetime.strptime(r["start_local"], "%Y-%m-%d %H:%M")
        litres[(t.year, t.month)] += int(r["qty_good"]) * sz[r["sku"]] / 1000.0
    out = {}
    for y, m in W.month_iter(dt.date(2025, 4, 1), dt.date(2026, 3, 1)):
        out[(y, m)] = (water[(y, m)], litres[(y, m)])
    return out
