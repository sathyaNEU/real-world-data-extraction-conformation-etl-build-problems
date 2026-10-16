"""The golden's code path: everything is computed from the shipped files under target/ (the ACD exports, the roster,
the board's workbook, the location records, the boundary, the directory and the callback log). checks.py runs the
rungs, rivals and stops through the same readers; verify.py recomputes the graded figures on its own code path."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os

import numpy as np

import common as K
import erlang as E
import model as M

UTC, TZ = K.UTC, K.TZ


def _p_legacy(s):
    """Legacy local time 'MM/DD/YYYY HH:MM:SS' to epoch seconds."""
    if not s:
        return math.nan
    d = dt.datetime.strptime(s, "%m/%d/%Y %H:%M:%S").replace(tzinfo=TZ)
    return d.astimezone(UTC).timestamp()


def _p_iso(s):
    if not s:
        return math.nan
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC).timestamp()


def _p_local(s):
    if not s:
        return math.nan
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ).astimezone(UTC).timestamp()


LEGACY_KIND = {"WPH1": "wireless", "WPH2": "wireless", "VOIP": "voip", "RESD": "fixed", "BUSN": "fixed",
               "PBXB": "mlts", "TLMA": "telematics", "TEST": "test"}


class Calls:
    """Every call in the two ACD exports, unified: presented, answered, ready, hang-up (epoch seconds), flags."""


def read_calls(target, legacy_name, i3_name):
    rows = []
    with open(os.path.join(target, legacy_name), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append((_p_legacy(r["SEIZE_TIME"]), _p_legacy(r["ANS_TIME"]), _p_legacy(r["RDY_TIME"]),
                         _p_legacy(r["DISC_TIME"]) if r["CALL_STATUS"] == "ABN" else math.nan,
                         r["CALL_STATUS"] == "ABN", r["CALL_STATUS"] == "TST", LEGACY_KIND[r["CLASS_OF_SVC"]],
                         bool(r["XFER_IN_FROM"]), r["XFER_OUT_TO"], r["CBN_REF"].lower(), r["CALL_ID"], "legacy",
                         _p_legacy(r["REL_TIME"]), ""))
    with open(os.path.join(target, i3_name), encoding="utf-8") as fh:
        for line in fh:
            o = json.loads(line)
            ab = o["disposition"] == "abandoned"
            test = o["serviceType"] == "test"
            rows.append((_p_iso(o["presented"]), _p_iso(o.get("answered", "")) if not ab else math.nan,
                         _p_iso(o.get("ready", "")), _p_iso(o.get("ended", "")) if ab else math.nan, ab, test,
                         o["serviceType"], "referredBy" in o, o.get("transferTo", ""),
                         o["callbackRef"][3:] if o["callbackRef"].startswith("cb-") else o["callbackRef"],
                         o["callId"], "i3", _p_iso(o.get("released", "")), o.get("incidentId", "")))
    rows.sort(key=lambda r: r[0])
    C = Calls()
    C.t = np.array([r[0] for r in rows])
    C.ans = np.array([r[1] for r in rows])
    C.ready = np.array([r[2] for r in rows])
    C.hang = np.array([r[3] for r in rows])
    C.ab = np.array([r[4] for r in rows], dtype=bool)
    C.test = np.array([r[5] for r in rows], dtype=bool)
    C.kind = np.array([r[6] for r in rows], dtype=object)
    C.xin = np.array([r[7] for r in rows], dtype=bool)
    C.xout = np.array([r[8] for r in rows], dtype=object)
    C.cbn = np.array([r[9] for r in rows], dtype=object)
    C.cid = np.array([r[10] for r in rows], dtype=object)
    C.layout = np.array([r[11] for r in rows], dtype=object)
    C.rel = np.array([r[12] for r in rows])
    C.iid = np.array([r[13] for r in rows], dtype=object)
    C.is911 = ~C.test
    C.wait = np.where(C.ab, C.hang - C.t, C.ans - C.t)
    locs = [K.to_local(x) for x in C.t]
    C.lhour = np.array([d.hour for d in locs], dtype=np.int64)
    C.lwd = np.array([d.weekday() for d in locs], dtype=np.int64)
    C.late = np.array([K.is_frisat_late(d) for d in locs], dtype=bool)          # the Friday and Saturday late shift
    C.wknight = np.array([K.is_weekend_night(d) for d in locs], dtype=bool)     # Friday and Saturday nights, 22:00-06:00
    C.lateblock = np.array([K.is_late(d) for d in locs], dtype=bool)            # 22:00-02:00, any night
    return C


def estimates(C, mask=None):
    """(mean busy time answer to ready, the patience by the exponential likelihood with answered calls censored, the
    hang-ups' own mean wait, number abandoned), seconds, over 911 calls in mask."""
    m = C.is911 if mask is None else (C.is911 & mask)
    ans = m & ~C.ab
    ab = m & C.ab
    busy = float(np.mean(C.ready[ans] - C.ans[ans]))
    pat = float(np.sum(C.wait[m]) / ab.sum())
    wab = float(np.mean(C.wait[ab]))
    return busy, pat, wab, int(ab.sum())


# ---------------------------------------------------------------------------------------------------- the forecast
def read_forecast(target, name, sheet="FY2028", psap="Tavish County ECA"):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, name), read_only=True, data_only=True)
    ws = wb[sheet]
    it = ws.iter_rows(values_only=True)
    head = None
    out = {}
    for row in it:
        if row and row[0] == "PSAP":
            head = list(row)
            break
    ix = {h: k for k, h in enumerate(head)}
    for row in it:
        if not row or row[0] is None:
            continue
        if row[ix["PSAP"]] != psap:
            continue
        mon = dt.datetime.strptime(row[ix["Month"]], "%b %Y")
        dow = K.DOW.index(row[ix["Day"]])
        h = int(row[ix["Hour beginning"]][:2])
        out[(mon.year, mon.month, dow, h)] = (float(row[ix["Forecast 911 calls per hour"]]),
                                               float(row[ix["Of which Halvorsen move"]]))
    return out


def fy2028(fc, busy, pat, model="A", c=K.LATE_C_FY2028, excl=True, use_halvorsen=True, flat=False):
    """{(y, m): compliance} for fiscal 2028 from the board's forecast cells (each night's hours on the forecast of the
    month the night starts)."""
    mu, th = 3600.0 / busy, 3600.0 / pat
    out = {}
    for y, m in K.fy_months(2028):
        def lam_of(dow, h, y=y, m=m):
            v, hv = fc[(y, m, dow, h)]
            return v if use_halvorsen else v - hv
        if flat:
            cells = [cell for _, cl in M.night_cells(y, m) for cell in cl]
            avg = sum(lam_of(d, h) for d, h in cells) / len(cells)
            out[(y, m)] = M.month_compliance(y, m, lambda d, h: avg, mu, th, c, model, excl)[0]
        else:
            out[(y, m)] = M.month_compliance(y, m, lam_of, mu, th, c, model, excl)[0]
    return out


def short_months(comp):
    return [ym for ym, v in sorted(comp.items(), key=lambda kv: (kv[0][0], kv[0][1])) if v < 0.90]


def label_set(months):
    return ", ".join("%s %d" % (K.MON3[m], y) for y, m in months) or "none"


# ---------------------------------------------------------------------------------------------------- history by hour
def hourly(C, t0, nh):
    k = ((C.t - t0) // 3600).astype(np.int64)
    m = C.is911 & (k >= 0) & (k < nh)
    kk = k[m]
    cnt = np.bincount(kk, minlength=nh).astype(float)
    ok15 = np.bincount(kk, weights=((~C.ab[m]) & (C.wait[m] <= 15.0)).astype(float), minlength=nh)
    ab5 = np.bincount(kk, weights=(C.ab[m] & (C.wait[m] <= 5.0)).astype(float), minlength=nh)
    abn = np.bincount(kk, weights=C.ab[m].astype(float), minlength=nh)
    return cnt, ok15, ab5, abn


def read_roster(target, name):
    ros = {}
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            ros[(dt.date.fromisoformat(r["date"]), r["block"])] = int(r["call_takers_on_911"])
    return ros


def hour_table(ros, t0, nh):
    """Per UTC hour index: (local year, month, hour, weekday, fiscal year of the block's date, Friday or Saturday
    late, call-takers)."""
    out = []
    for k in range(nh):
        loc = K.to_local(t0 + 3600 * k)
        d, blk = K.block_of(loc)
        out.append((loc.year, loc.month, loc.hour, loc.weekday(), K.fiscal_year(d), K.is_frisat_late(loc), ros[(d, blk)]))
    return out


def backtest(C, ros, t0, nh, busy, pat, select, models=("obs", "A", "C", "Ab"), wab=None):
    """Observed compliance and abandon share over the hours `select` picks, against each model's prediction with the
    hours grouped by (year, month, hour, weekday, call-takers) and each group's mean count as its arrival rate. `pat`
    (and `wab`) may be a number or a function of the group's (year, month, hour, weekday, call-takers)."""
    cnt, ok15, ab5, abn = hourly(C, t0, nh)
    HT = hour_table(ros, t0, nh)
    groups = {}
    for k in range(nh):
        if select(HT[k]):
            y, mo, h, wd, fy, late, c = HT[k]
            groups.setdefault((y, mo, h, wd, c), []).append(k)
    mu = 3600.0 / busy
    pat_of = pat if callable(pat) else (lambda key: pat)
    wab_of = wab if callable(wab) else (lambda key: wab)
    num = den = 0.0
    pA = dA = pB = dB = pC = n = abA = abB = oab = 0.0
    for key, ks in groups.items():
        y, mo, h, wd, c = key
        th = 3600.0 / pat_of(key)
        thb = 3600.0 / wab_of(key) if wab else None
        ks = np.array(ks)
        lam = cnt[ks].mean()
        w = len(ks) * lam
        num += ok15[ks].sum()
        den += cnt[ks].sum() - ab5[ks].sum()
        oab += abn[ks].sum()
        st, a5, pab = E.erlang_a(lam, mu, th, c)[:3]
        pA += w * st
        dA += w * (1 - a5)
        abA += w * pab
        pC += w * E.erlang_c(lam, mu, c)
        n += w
        if wab:
            st, a5, pab = E.erlang_a(lam, mu, thb, c)[:3]
            pB += w * st
            dB += w * (1 - a5)
            abB += w * pab
    return {"obs": num / den, "A": pA / dA, "C": pC / n, "Ab": (pB / dB) if wab else None,
            "ab_obs": oab / n, "ab_A": abA / n, "ab_Ab": (abB / n) if wab else None, "calls": n}


# ---------------------------------------------------------------------------------------------------- ask A
def read_boundary(target, name):
    gj = json.load(open(os.path.join(target, name), encoding="utf-8"))
    feat = [f for f in gj["features"] if f["properties"]["NAME"] == "Halvorsen Township"][0]
    g = feat["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    return polys


def _ring_in(x, y, ring):
    inside = False
    n = len(ring)
    for i in range(n - 1):
        x1, y1 = ring[i]
        x2, y2 = ring[i + 1]
        if (y1 > y) != (y2 > y):
            if x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
    return inside


def in_polys(lon, lat, polys, holes=True, all_parts=True):
    for p in (polys if all_parts else polys[:1]):
        if _ring_in(lon, lat, p[0]) and not (holes and any(_ring_in(lon, lat, h) for h in p[1:])):
            return True
    return False


def read_che(target, name):
    by = {}
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            by.setdefault(r["call_id"], []).append((int(r["seq"]), r["method"], float(r["latitude"]),
                                                     float(r["longitude"]), int(r["radius_m"])))
    for v in by.values():
        v.sort()
    return by


def read_directory(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return {r["uri"]: r["agency"] for r in csv.DictReader(fh)}


def ask_a(C, che, polys, directory, fix="handset", holes=True, all_parts=True, xfer="directory", quarter="local",
          key="both"):
    """{(fy, q): (reached, transferred)} for fiscal 2026; a call's location records are filed under its call
    identifier or its incident identifier (key="callid" reads the first alone)."""
    out = {(2026, q): [0, 0] for q in (1, 2, 3, 4)}
    lo = dt.datetime(2025, 7, 1, tzinfo=TZ).astimezone(UTC).timestamp()
    hi = dt.datetime(2026, 7, 1, tzinfo=TZ).astimezone(UTC).timestamp()
    sel = np.nonzero(C.is911 & (C.kind == "wireless") & (C.layout == "i3"))[0]
    for i in sel:
        recs = che.get(C.cid[i])
        if not recs and key == "both":
            recs = che.get(C.iid[i])
        if not recs:
            continue
        if fix == "handset":
            hs = [r for r in recs if r[1] != "cell"]
            pt = hs[-1] if hs else None
        else:
            pt = recs[0]
        if pt is None or not in_polys(pt[3], pt[2], polys, holes, all_parts):
            continue
        ts = C.t[i]
        if quarter == "local":
            d = K.to_local(ts).date()
            if not (lo <= ts < hi):
                continue
        else:
            d = dt.datetime.fromtimestamp(ts, UTC).date()
            if not (dt.date(2025, 7, 1) <= d < dt.date(2026, 7, 1)):
                continue
        fq = K.fiscal_quarter(d)
        out[fq][0] += 1
        u = C.xout[i]
        if u:
            if xfer == "directory":
                hit = directory.get(u) == K.NEIGHBOUR
            else:
                hit = "wexley" in u.lower()
            out[fq][1] += int(hit)
    return {k: tuple(v) for k, v in out.items()}


# ---------------------------------------------------------------------------------------------------- ask B
def read_callbacks(target, name):
    rows = []
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append({"line": r["line"], "created": _p_local(r["created"]), "ref": r["call_ref"],
                         "num": r["callback_number"].lower(), "first": _p_local(r["first_dial"]),
                         "result": r["result"], "closed": _p_local(r["closed"])})
    return rows


def ask_b(C, tasks, match="number", anchor="hangup", misdials=True, unmatched="not", tol=30.0, lines911=False,
          called_in="not"):
    """{(y, m): share} for January to June 2026, by the local month of the hang-up."""
    lo = dt.datetime(2026, 1, 1, tzinfo=TZ).astimezone(UTC).timestamp()
    hi = dt.datetime(2026, 7, 1, tzinfo=TZ).astimezone(UTC).timestamp()
    by_num = {}
    by_ref = {}
    for tk in tasks:
        if tk["line"] == "911" or not lines911:
            by_num.setdefault(tk["num"], []).append(tk)
        if tk["line"] == "911":
            by_ref[tk["ref"]] = tk
    num = {}
    den = {}
    if match == "tasks":
        # the task log alone: 911 tasks stamped in the month, first dial within two minutes of the stamp
        for tk in tasks:
            if tk["line"] != "911" or not (lo <= tk["created"] < hi):
                continue
            loc = K.to_local(tk["created"])
            key = (loc.year, loc.month)
            den[key] = den.get(key, 0) + 1
            num[key] = num.get(key, 0) + int(not math.isnan(tk["first"]) and tk["first"] - tk["created"] <= 120.0)
        return {k: num[k] / den[k] for k in sorted(den)}, den
    sel = np.nonzero(C.is911 & C.ab & (C.hang >= lo) & (C.hang < hi))[0]
    for i in sel:
        if not misdials and C.wait[i] <= 5.0:
            continue
        loc = K.to_local(C.hang[i])
        key = (loc.year, loc.month)
        hit = False
        if match == "number":
            firsts = [tk["first"] for tk in by_num.get(C.cbn[i], []) if not math.isnan(tk["first"])
                      and tk["first"] >= C.hang[i] and tk["created"] <= C.hang[i] + tol]
            if firsts:
                f = min(firsts)
                base = C.hang[i]
                if anchor == "created":
                    owner = [tk for tk in by_num[C.cbn[i]] if tk["first"] == f][0]
                    base = owner["created"]
                hit = f - base <= 120.0
            if not hit and called_in == "dialled":
                hit = any(tk["result"] == "caller called in" and tk["created"] <= C.hang[i] + tol
                          and 0.0 <= tk["closed"] - C.hang[i] <= 120.0 for tk in by_num.get(C.cbn[i], []))
        else:
            tk = by_ref.get(C.cid[i])
            if tk is None:
                if unmatched == "drop":
                    continue
            elif not math.isnan(tk["first"]):
                base = C.hang[i] if anchor == "hangup" else tk["created"]
                hit = tk["first"] - base <= 120.0
        den[key] = den.get(key, 0) + 1
        num[key] = num.get(key, 0) + int(hit)
    return {k: num[k] / den[k] for k in sorted(den)}, den
