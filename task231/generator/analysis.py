"""task231 architecture 2: the analysis, run on the shipped files alone. The golden figures, the ladder's rungs and
the two asks all come from here; nothing reads the world."""
import csv
import datetime as dt
import math
import os
import re

import numpy as np
from openpyxl import load_workbook

import params as P

TAU_C = 2.0            # agreement with the stations sharing the air (corridor 1.5 to 4.5 asserted in checks.py)
FA_RADIUS_KM = 50.0    # free-atmosphere neighbours of a station no cold pool holds
GROUP_KM, GROUP_DZ, GROUP_R, GROUP_SIG = 25.0, 80.0, 0.8, -0.5
LAPSE = P.SPATIAL_LAPSE_C_PER_KM


def fpath(target, key):
    return os.path.join(target, P.FILES[key])


def utc_of_local(s):
    """'2026-11-01 01:30:12 MST' -> naive UTC"""
    d, t, z = s.split(" ")
    base = dt.datetime.strptime(d + " " + t, "%Y-%m-%d %H:%M:%S")
    return base + dt.timedelta(hours={"MDT": 6, "MST": 7}[z])


def local_of_utc(u):
    if u < P.DST_OFF_UTC or u >= P.DST_ON_UTC:
        return u - dt.timedelta(hours=6)
    return u - dt.timedelta(hours=7)


def hour_of_obs(u):
    """the observation stamped at an hour's end -> the hour's index in the winter"""
    return int((u - P.WIN_START_UTC).total_seconds() // 3600) - 1


def parse_z(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def haversine(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    x = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(x))


def register(target):
    wb = load_workbook(fpath(target, "register"), read_only=True)
    sites = []
    for r in list(wb["Sites"].iter_rows(values_only=True))[1:]:
        sites.append({"site": r[0], "rpu": r[1], "name": r[2], "lat": r[5], "lon": r[6], "z": float(r[8])})
    sensors = [dict(zip(["site", "rpu", "port", "lane", "serial", "model", "units", "installed", "note"], r))
               for r in list(wb["Pavement sensors"].iter_rows(values_only=True))[1:]]
    firmware = {r[0]: (r[1], dt.datetime.strptime(r[2], "%Y-%m-%d %H:%M"))
                for r in list(wb["Firmware"].iter_rows(values_only=True))[1:]}
    codes = {}
    for tab, code, name in list(wb["Status codes"].iter_rows(values_only=True))[1:]:
        codes.setdefault(tab, {})[int(code)] = name
    sites.sort(key=lambda s: s["site"])
    n = len(sites)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = haversine((sites[i]["lat"], sites[i]["lon"]), (sites[j]["lat"], sites[j]["lon"]))
    return {"sites": sites, "idx": {s["site"]: k for k, s in enumerate(sites)},
            "rpu": {s["rpu"]: k for k, s in enumerate(sites)}, "Z": np.array([s["z"] for s in sites]), "D": D,
            "sensors": sensors, "firmware": firmware, "codes": codes}


def feed(target, reg):
    """air temperature per station and hour (C); a re-sent observation appears twice with the same values"""
    n = len(reg["sites"])
    val = np.full((n, P.NH), np.nan)
    seen = {}
    rows = dups = 0
    with open(fpath(target, "feed"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows += 1
            i = reg["rpu"][r["rpu_id"]]
            h = hour_of_obs(parse_z(r["obs_time_utc"]))
            key = (i, h)
            v = int(r["essAirTemperature"]) / 10.0
            if key in seen:
                dups += 1
                assert seen[key] == v
                continue
            seen[key] = v
            val[i, h] = v
    return val, {"rows": rows, "duplicates": dups}


def qc(target, reg):
    """the hours the spatial test withheld each station's air temperature, and every air-temperature row"""
    n = len(reg["sites"])
    wh = np.zeros((n, P.NH), bool)
    anyflag = np.zeros((n, P.NH), bool)
    rows = {"spatial": 0, "step": 0, "other": 0}
    with open(fpath(target, "qc"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["parameter"] != "air_temperature":
                rows["other"] += 1
                continue
            i = reg["idx"][r["site_code"]]
            h = hour_of_obs(parse_z(r["obs_time"]))
            anyflag[i, h] = True
            rows[r["test"]] = rows.get(r["test"], 0) + 1
            if r["test"] == "spatial":
                wh[i, h] = True
    return wh, anyflag, rows


def night_mask():
    out = np.zeros(P.NH, bool)
    for h in range(P.NH):
        loc = local_of_utc(P.WIN_START_UTC + dt.timedelta(hours=h))
        out[h] = loc.hour >= 18 or loc.hour < 9
    return out


def fa_line(val, Z):
    """each hour's free-atmosphere line: elevation fitted to the readings, refitted without stations far below it"""
    n, nh = val.shape
    res = np.full_like(val, np.nan)
    slope = np.full(nh, np.nan)
    for h in range(nh):
        ok = ~np.isnan(val[:, h])
        use = ok.copy()
        for _ in range(3):
            A = np.vstack([np.ones(use.sum()), Z[use]]).T
            c, *_ = np.linalg.lstsq(A, val[use, h], rcond=None)
            r = val[:, h] - (c[0] + c[1] * Z)
            use = ok & (r > -1.5)
        res[:, h] = r
        slope[h] = c[1]
    return res, slope


def sharing(val, wh, anyflag, reg, night, res=None, cth=GROUP_R, dz=GROUP_DZ, dk=GROUP_KM, sig=GROUP_SIG):
    """stations that share a cold pool: their night residuals from the free-atmosphere line move together on the
    hours both readings passed the QC, they sit within a few kilometres and metres of each other, and both run
    below the line on an average night"""
    Z, D = reg["Z"], reg["D"]
    n = len(Z)
    if res is None:
        res, _ = fa_line(val, Z)
    ok = ~np.isnan(res) & ~anyflag
    C = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(n):
            m = night & ok[i] & ok[j]
            C[i, j] = np.corrcoef(res[i, m], res[j, m])[0, 1]
    mres = np.array([res[i, night & ok[i]].mean() for i in range(n)])
    G = {i: [j for j in range(n) if j != i and C[i, j] > cth and abs(Z[j] - Z[i]) <= dz and D[i, j] <= dk
             and mres[i] < sig and mres[j] < sig] for i in range(n)}
    return G, C, mres


def judge(val, wh, reg, G, tau=TAU_C, rad=FA_RADIUS_KM, agg="median", floor_rule="median", lapse=None):
    """each withheld reading against the stations sharing its air that hour: a cold-pool floor against its pool
    mates, any other station against the free-atmosphere stations within reach, carried to its elevation"""
    Z, D = reg["Z"], reg["D"]
    n = len(Z)
    floor = {i for i in range(n) if G[i]}
    fa = [j for j in range(n) if j not in floor]
    right = np.zeros_like(wh)
    nopeer = np.zeros(n, int)
    for i in range(n):
        hs = np.where(wh[i])[0]
        if not len(hs):
            continue
        if G[i]:
            peers = G[i]
            pv = val[peers][:, hs]
        else:
            peers = [j for j in fa if j != i and D[i, j] <= rad]
            gam = (LAPSE / 1000.0) if lapse is None else -lapse[hs][None, :]
            pv = val[peers][:, hs] + gam * (Z[peers] - Z[i])[:, None]
        nopeer[i] = int(np.isnan(pv).all(0).sum())
        if G[i] and floor_rule == "any":
            ok = (np.abs(pv - val[i, hs][None, :]) <= tau).any(0)
        else:
            ref = np.nanmedian(pv, axis=0) if agg == "median" else np.nanmean(pv, axis=0)
            ok = np.abs(val[i, hs] - ref) <= tau
        right[i, hs] = ok
    return right, nopeer


def shares(mask):
    return mask.sum(1) / P.NH * 100.0


def retune(cnt_or_share, is_share=True):
    s = cnt_or_share if is_share else cnt_or_share / P.NH * 100.0
    return [k for k in range(len(s)) if s[k] > P.RETUNE_LINE_PCT]


def main_call(target):
    reg = register(target)
    val, fstat = feed(target, reg)
    wh, anyflag, qstat = qc(target, reg)
    night = night_mask()
    res, slope = fa_line(val, reg["Z"])
    G, C, mres = sharing(val, wh, anyflag, reg, night, res=res)
    right, nopeer = judge(val, wh, reg, G)
    fr = (wh & right).sum(1)
    sh = fr / P.NH * 100.0
    return {"reg": reg, "val": val, "wh": wh, "anyflag": anyflag, "night": night, "res": res, "slope": slope,
            "G": G, "C": C, "mres": mres, "right": right, "nopeer": nopeer, "withheld": wh.sum(1), "fr": fr,
            "share": sh, "retune": retune(sh), "feed": fstat, "qc": qstat}


# ---------------- the ladder's other rungs, on the same shipped files ----------------
def rungs(M, target):
    reg, val, wh, night = M["reg"], M["val"], M["wh"], M["night"]
    Z, D = reg["Z"], reg["D"]
    n = len(Z)
    out = {"R0 trust the QC": np.zeros(n), "R1 every withheld reading right": shares(wh)}
    r2 = np.zeros_like(wh)
    for h in range(P.NH):
        ok = ~np.isnan(val[:, h])
        A = np.vstack([np.ones(ok.sum()), Z[ok]]).T
        c, *_ = np.linalg.lstsq(A, val[ok, h], rcond=None)
        r2[:, h] = np.abs(val[:, h] - (c[0] + c[1] * Z)) <= 5.0
    out["R2 hourly lapse refit within 5 C"] = shares(wh & r2)
    r3 = np.zeros_like(wh)
    for i in range(n):
        cand = [j for j in np.argsort(D[i]) if j != i and abs(Z[j] - Z[i]) <= 150][:2]
        pm = np.nanmean([val[j] + LAPSE * (Z[j] - Z[i]) / 1000.0 for j in cand], axis=0)
        r3[i] = np.abs(val[i] - pm) <= 2.0
    out["R3 two nearest within 150 m"] = shares(wh & r3)
    out["R4 night and below 1,600 m"] = shares(wh & np.array([night & (Z[i] < 1600) for i in range(n)]))
    mon = np.array([local_of_utc(P.WIN_START_UTC + dt.timedelta(hours=h)).month for h in range(P.NH)])
    lh = np.array([local_of_utc(P.WIN_START_UTC + dt.timedelta(hours=h)).hour for h in range(P.NH)])
    r6 = np.zeros_like(wh)
    for i in range(n):
        for mm in sorted(set(mon)):
            for hh in range(24):
                sel = (mon == mm) & (lh == hh)
                v = val[i, sel]
                lo, hi = np.nanpercentile(v, 2), np.nanpercentile(v, 98)
                r6[i, sel] = (v >= lo) & (v <= hi)
    out["R6 own month-hour 2nd to 98th percentile"] = shares(wh & r6)
    r7 = np.zeros_like(wh)
    for i in range(n):
        nb = [j for j in range(n) if j != i and D[i, j] <= 30]
        r7[i] = wh[nb].any(axis=0)
    out["R7 withheld with a neighbour within 30 km"] = shares(wh & r7)
    nwp = np.full_like(val, np.nan)
    with open(fpath(target, "nwp"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            h = hour_of_obs(parse_z(r["valid_utc"]))
            nwp[reg["idx"][r["site_code"]], h] = float(r["t2m_c"])
    for i in range(n):           # the 3-hourly forecast carried to the hours between
        good = ~np.isnan(nwp[i])
        nwp[i] = np.interp(np.arange(P.NH), np.where(good)[0], nwp[i, good])
    out["R8 HRRR forecast within 5 C"] = shares(wh & (np.abs(val - nwp) <= 5.0))
    return out


# ---------------- ask A: unavailable hours under Schedule B ----------------
def sla(target, reg, val):
    """val: the feed's readings, which place a message from a modem the register gives no site"""
    n = len(reg["sites"])
    wb = load_workbook(fpath(target, "modems"), read_only=True)
    imei = {}
    for r in list(wb["Modems"].iter_rows(values_only=True))[1:]:
        if r[2]:
            imei[str(r[0])] = reg["idx"][r[2]]
    first = np.full((n, P.NH), np.inf)
    nmsg = {"SCHED": 0, "BACKLOG": 0, "REPOLL": 0}
    unplaced = {}
    with open(fpath(target, "messages"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rec = utc_of_local(r["server_received"])
            nmsg[r["kind"]] += 1
            a, b = hour_of_obs(parse_z(r["first_obs_utc"])), hour_of_obs(parse_z(r["last_obs_utc"]))
            if r["modem_imei"] not in imei:
                unplaced.setdefault(r["modem_imei"], []).append((rec, a, b))
                continue
            i = imei[r["modem_imei"]]
            for h in range(a, b + 1):
                late = (rec - (P.WIN_START_UTC + dt.timedelta(hours=h + 1))).total_seconds() / 60.0
                first[i, h] = min(first[i, h], late)
    placed = {}
    for im, ms in sorted(unplaced.items()):
        hs = sorted({h for _, a, b in ms for h in range(a, b + 1)})
        fits = [i for i in range(n) if all(not np.isnan(val[i, h]) and np.isinf(first[i, h]) for h in hs)]
        assert len(fits) == 1, (im, fits)
        placed[im] = fits[0]
        for rec, a, b in ms:
            for h in range(a, b + 1):
                late = (rec - (P.WIN_START_UTC + dt.timedelta(hours=h + 1))).total_seconds() / 60.0
                first[fits[0], h] = min(first[fits[0], h], late)
    excl = np.zeros((n, P.NH), bool)
    with open(fpath(target, "outages"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            i = reg["idx"][r["site_code"]]
            a = int((utc_of_local(r["starts"]) - P.WIN_START_UTC).total_seconds() // 3600)
            b = int((utc_of_local(r["ends"]) - P.WIN_START_UTC).total_seconds() // 3600)
            excl[i, max(a, 0):min(b, P.NH)] = True
    avail = (first <= P.SLA_GRACE_MIN) & ~excl
    unavail = P.NH - avail.sum(1) - excl.sum(1)
    return {"unavailable": unavail, "excluded": excl.sum(1), "available": avail.sum(1), "first": first,
            "excl": excl, "messages": nmsg, "placed": placed,
            "unplaced_rows": sum(len(v) for v in unplaced.values())}


# ---------------- ask B: travel-lane freezing hours and ice hours ----------------
def pavement(target, reg):
    n = len(reg["sites"])
    model, lane = {}, {}
    for s in reg["sensors"]:
        model[s["serial"]] = s["model"]
        lane[(reg["idx"][s["site"]], int(s["port"]))] = s["lane"]
        m = re.match(r"Replaced (\S+) serial (\S+)", s["note"] or "")
        if m:
            model[m.group(2)] = m.group(1)
    tab_old = [k for k in reg["codes"] if "3.4" in k][0]
    tab_new = [k for k in reg["codes"] if "4.1" in k][0]
    frz = np.zeros((n, P.NH), bool)
    ice = np.zeros((n, P.NH), bool)
    seen = set()
    rows = dups = 0
    with open(fpath(target, "pavement"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows += 1
            key = tuple(r.values())
            if key in seen:
                dups += 1
                continue
            seen.add(key)
            i = reg["rpu"][r["rpu_id"]]
            if lane[(i, int(r["port"]))] != "travel lane":
                continue
            mst = dt.datetime.strptime(r["obs_time_mst"], "%Y-%m-%d %H:%M")
            h = hour_of_obs(mst + dt.timedelta(hours=7))
            ser = r["sensor_serial"]
            md = model[ser]
            if md == "IRS-31":
                c = int(r["surface_temperature"]) / 10.0
                f_ = c * 9 / 5 + 32
            else:
                f_ = float(r["surface_temperature"])
            fw = reg["firmware"].get(ser)
            loc = local_of_utc(mst + dt.timedelta(hours=7))
            tab = tab_new if (md == "IRS-31" and fw is not None and loc >= fw[1]) else tab_old
            st = reg["codes"][tab][int(r["surface_status_code"])]
            frz[i, h] |= f_ <= 32.0 + 1e-9
            ice[i, h] |= st in ("ice warning", "ice watch")
    return {"freezing": frz.sum(1), "ice": ice.sum(1), "rows": rows, "duplicates": dups, "frz": frz, "icem": ice}


def solve(target):
    M = main_call(target)
    reg = M["reg"]
    A = sla(target, reg, M["val"])
    B = pavement(target, reg)
    return {"M": M, "A": A, "B": B, "reg": reg}
