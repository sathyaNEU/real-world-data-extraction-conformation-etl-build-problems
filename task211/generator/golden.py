"""The golden, computed from target/ alone.

The call: an excess that rain washes down is radon progeny on the ground, which can lose at most about a
quarter of itself in ten minutes (lead-214 feeding bismuth-214); an excess that loses more than half of itself
from one ten-minute value to the next, and stays down, cannot be natural. Each station's increases of artificial
origin are the elevated runs that end in such a fall; their dates and the highest ten-minute value recorded in
them make the notification."""
import csv
import datetime as dt
import json
import os

import numpy as np
from openpyxl import load_workbook

import pack
import world as W

FALL, FLOOR, ELEV = 0.5, 30.0, 15.0
HALF = 30.05


def t_of(stamp):
    d = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    return int((d - W.Q_START).total_seconds() // 600)


def read_export(tgt):
    """station -> (values nSv/h with NaN, status array). Exact duplicate rows read once; microsieverts converted."""
    vals = {}; stat = {}; seen = set()
    with open(os.path.join(tgt, pack.FILES["export"]), newline="", encoding="utf-8") as f:
        rd = csv.reader(f); next(rd)
        for row in rd:
            key = tuple(row)
            if key in seen:
                continue
            seen.add(key)
            code, stamp, v, unit, st, probe = row
            if code not in vals:
                vals[code] = np.full(W.N10, np.nan); stat[code] = np.full(W.N10, "", dtype="<U1")
            t = t_of(stamp)
            x = float(v) * (1000.0 if unit == "uSv/h" else 1.0) if v != "" else np.nan
            vals[code][t] = x; stat[code][t] = st
    return vals, stat


def rolling_median(x, win=288, minp=60):
    import pandas as pd
    return pd.Series(x).rolling(win, center=True, min_periods=minp).median().bfill().ffill().values


def detections(vals, stat, fall=FALL, floor=FLOOR, persist=1, base="c48"):
    """station -> list of episodes (start t, end t exclusive, abrupt-fall t)."""
    import pandas as pd
    out = {}
    for code, v in vals.items():
        x = v.copy(); x[stat[code] != "V"] = np.nan
        if base == "c48":
            b = rolling_median(x)
        elif base == "t24":
            b = pd.Series(x).rolling(144, min_periods=60).median().bfill().ffill().values
        else:
            b = pd.Series(x).rolling(1008, center=True, min_periods=200).quantile(0.3).bfill().ffill().values
        ex = x - b
        a_, b_ = ex[:-1], ex[1:]
        ok = (~np.isnan(a_)) & (~np.isnan(b_)) & (a_ >= floor) & ((a_ - b_) > fall * a_)
        for p in range(1, persist + 1):
            c = np.full_like(a_, np.nan); c[:-p] = ex[1 + p:]
            ok &= (~np.isnan(c)) & (c < (1 - fall) * a_)
        eps = []
        for t in np.where(ok)[0] + 1:
            s = t - 1
            while s - 1 >= 0 and not np.isnan(ex[s - 1]) and ex[s - 1] > ELEV:
                s -= 1
            if eps and s <= eps[-1][1]:
                eps[-1] = (eps[-1][0], max(eps[-1][1], int(t)), eps[-1][2])
            else:
                eps.append((int(s), int(t), int(t)))
        if eps:
            out[code] = eps
    return out


def call_from(vals, stat, det):
    res = {}
    for code, eps in det.items():
        dates = sorted({(W.Q_START + dt.timedelta(minutes=10 * s)).date() for s, e, f in eps})
        peak = max(np.nanmax(vals[code][s:e]) for s, e, f in eps)
        res[code] = dict(dates=dates, peak=int(round(peak)), episodes=eps)
    return res


# ------------------------------------------------------------------ ask A: source checks

def read_rows(path, sheet):
    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    return rows[0], rows[1:]


def certs():
    return {s: [(c[0], c[1], c[2], c[3]) for c in v] for s, v in W.SOURCES.items()}


def source_checks(tgt, cert_table=None):
    """cert_table: serial -> list of (no, reference date, issue date, {jig: reading}); read from the PDF by the
    verifier, taken from the world here (the generator wrote the PDF from it)."""
    cert_table = cert_table or certs()
    mig = {}
    with open(os.path.join(tgt, pack.FILES["migration"]), newline="") as f:
        for r in list(csv.reader(f))[1:]:
            mig[r[0]] = r[1]
    kits, kit_src = {}, {}
    with open(os.path.join(tgt, pack.FILES["kits"]), newline="") as f:
        for r in list(csv.reader(f))[1:]:
            kits[r[0]] = r[3].split()[0]
            kit_src[r[0]] = r[2]
    away, seen_in = {}, []
    with open(os.path.join(tgt, pack.FILES["sources"]), newline="") as f:
        for r in list(csv.reader(f))[1:]:
            d = dt.datetime.strptime(r[0], "%d/%m/%Y").date()
            if r[3] == "transfer out":
                away[r[1]] = [d, None]
            elif r[3] == "transfer in":
                away[r[1]][1] = d
            else:
                seen_in.append((d, r[1], r[4]))

    def source_in(kit, day):
        """The kit's own source, unless that source was out of the store on the day; then the source the
        register found in the kit while it was away."""
        s = kit_src[kit]
        if s in away and away[s][0] <= day < away[s][1]:
            a, b = away[s]
            held = {src_ for d, src_, where in seen_in if a <= d < b and where == kit}
            assert len(held) == 1, (kit, day, held)
            return held.pop()
        return s

    path = os.path.join(tgt, pack.FILES["visits"])
    visits = {}
    h, rows = read_rows(path, "J French")
    for r in rows:
        d = dt.datetime.strptime(r[0], "%d/%m/%Y").date()
        visits.setdefault(r[2], []).append(dict(date=d, kit=r[4], source=source_in(r[4], d), jig=r[5], bg=float(r[6]),
                                                 with_=float(r[7]), note=r[8] or ""))
    h, rows = read_rows(path, "A Connolly")
    for r in rows:
        d = dt.datetime.strptime(r[0], "%d/%m/%Y").date()
        visits.setdefault(mig[r[2]], []).append(dict(date=d, kit=r[4], source=source_in(r[4], d), jig=kits[r[4]],
                                                      bg=float(r[5]) * 1000, with_=float(r[6]) * 1000, note=r[7] or ""))
    out = {}
    for code, lst in visits.items():
        chk = lst[-1] if len(lst) > 1 else lst[0]
        assert len({x["date"] for x in lst}) == 1
        net = chk["with_"] - chk["bg"]
        ok = [c for c in cert_table[chk["source"]] if c[2] <= chk["date"]]
        no, ref, issued, vals = ok[-1]
        y = (chk["date"] - ref).days / 365.25
        exp = vals[chk["jig"]] * 2 ** (-y / HALF)
        pct = net / exp * 100.0
        out[code] = dict(pct=pct, passed=abs(pct - 100.0) <= 10.0, net=net, expected=exp, cert=no, jig=chk["jig"],
                         source=chk["source"], kit=chk["kit"], date=chk["date"], repeated=len(lst) > 1)
    return out


# ------------------------------------------------------------------ ask B: air filters

def air(tgt):
    """A filter's volume is the air the pump drew through it: the controller's measured flow, integrated over the
    fifteen-minute rows from the filter going on to its coming off (the rows of a change are stopped)."""
    fpath = os.path.join(tgt, pack.FILES["field"])
    sheets = {}
    for sampler, code, flow, style in W.AIR:
        h, rows = read_rows(fpath, sampler)
        sheets[sampler] = (h, rows)
    log = {}
    with open(os.path.join(tgt, pack.FILES["pump"]), newline="") as f:
        rd = csv.reader(f); next(rd)
        for s, ts, st, fl, tot in rd:
            log.setdefault(s, []).append((dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"), st, float(fl),
                                          float(tot) if tot else None))
    lab = {}
    h, rows = read_rows(os.path.join(tgt, pack.FILES["beta"]), "Gross beta")
    for r in rows:
        key = r[1]
        if key not in lab or r[8] > lab[key][1]:
            lab[key] = (float(r[5]), int(r[8]))
    out = {}
    q15 = dt.timedelta(minutes=15)
    for sampler, code, flow, style in W.AIR:
        h, rows = sheets[sampler]
        rows_log = log[sampler]
        for r in rows:
            fid = r[0]
            on = dt.datetime.strptime(r[1], "%d/%m/%Y %H:%M") - W.BST
            off = dt.datetime.strptime(r[2], "%d/%m/%Y %H:%M") - W.BST
            vol = sum(fl * 0.25 for t, st, fl, tot in rows_log if on - q15 < t < off)
            act = lab[fid][0]
            out[fid] = dict(sampler=sampler, volume=vol, activity=act, conc=act / vol * 1000.0, on=on, off=off)
    return out


# ------------------------------------------------------------------ ask C: timeliness

def timeliness(tgt, vals):
    """An interval counts when the platform received the station's value for it (a record with a dose rate)
    within sixty minutes of the interval's end; fault records carry no value."""
    have = {c: ~np.isnan(v) for c, v in vals.items()}
    first = {c: np.full(W.N10, np.inf) for c in vals}
    with open(os.path.join(tgt, pack.FILES["ingest"]), newline="") as f:
        rd = csv.reader(f); next(rd)
        for bid, code, ch, a, b, n, rec in rd:
            if rec.endswith("Z"):
                when = dt.datetime.strptime(rec, "%Y-%m-%dT%H:%M:%SZ")
            else:
                when = dt.datetime.strptime(rec, "%d/%m/%Y %H:%M:%S") - W.BST
            m = (when - W.Q_START).total_seconds() / 60.0
            ta, tb = t_of(a), t_of(b)
            seg = first[code][ta:tb + 1]
            np.minimum(seg, m, out=seg)
    out = {}
    for code in vals:
        end = np.arange(W.N10) * 10.0 + 10.0
        ok = have[code] & (first[code] - end <= 60.0)
        out[code] = dict(pct=ok.sum() / W.N10 * 100.0, timely=int(ok.sum()), held=int(have[code].sum()),
                         margin=float(np.min(np.abs(first[code][have[code]] - end[have[code]] - 60.0))))
    return out


def falls(vals, stat, det, floor=FLOOR):
    """The largest one-step fall of a natural excess (outside the detections) and the smallest fall that ended a
    detection, both as fractions of the excess before the step."""
    nat, art = 0.0, 2.0
    for c, v in vals.items():
        x = v.copy(); x[stat[c] != "V"] = np.nan
        ex = x - rolling_median(x)
        a, b = ex[:-1], ex[1:]
        ok = (~np.isnan(a)) & (~np.isnan(b)) & (a >= floor)
        fr = np.where(ok, (a - b) / np.where(a == 0, 1, a), np.nan)
        nxt = np.full_like(a, np.nan); nxt[:-1] = ex[2:]
        stays = ok & ((a - b) > FALL * a) & (~np.isnan(nxt)) & (nxt < (1 - FALL) * a)
        if stays.any():
            art = min(art, float(np.nanmin(fr[stays])))
        inep = np.zeros(len(v), dtype=bool)
        for s, e, f in det.get(c, []):
            inep[s:e + 1] = True
        sel = ok & ~inep[1:] & ~inep[:-1]
        if sel.any():
            nat = max(nat, float(np.nanmax(fr[sel])))
    return nat, art


def compute(tgt):
    vals, stat = read_export(tgt)
    det = detections(vals, stat)
    call = call_from(vals, stat, det)
    g = dict(vals=vals, stat=stat, call=call, call_codes=sorted(call), det=det)
    nat, art = falls(vals, stat, det)
    g["nat_fall"], g["art_fall"] = nat, art
    g["nat_max_fall"] = int(np.ceil(100 * nat))
    g["art_min_fall"] = int(np.floor(100 * art))
    g["peak_day"] = {}
    for c in call:
        v = vals[c]
        best = max(((np.nanmax(v[s:e]), s + int(np.nanargmax(v[s:e]))) for s, e, f in det[c]))
        g["peak_day"][c] = (W.Q_START + dt.timedelta(minutes=10 * best[1])).date()
    g["checks"] = source_checks(tgt)
    g["air"] = air(tgt)
    g["timely"] = timeliness(tgt, vals)
    return g
