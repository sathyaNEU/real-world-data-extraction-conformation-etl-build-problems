"""task271 analysis from the shipped pack alone: every rung of the ladder, the golden, and the two asks.

The golden: each lake's season angler-hours are the anglers on it in each hour of the 05:00 to 22:00 angling day,
summed over the hours and the season's days. The flights count the anglers present at one moment of two hours a survey
day; the interviews say how a lake's anglers spread over the hours (each interviewed angler present in an hour for the
minutes the party fished in it). A count at a moment in hour h stands for the anglers present through hour h, which is
that day's angler-hours times the share of the lake's angler-hours that fall in hour h; so the day's angler-hours are
the count over that share. The survey's design (three survey days a stratum, month by weekday or weekend day) expands
the survey days to the season."""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import re

import numpy as np
import openpyxl

import common as K

HOURS = list(range(int(K.DAY_OPEN), int(K.DAY_CLOSE)))


# ------------------------------------------------------------------------------------------------- readers
def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def register(target):
    wb = openpyxl.load_workbook(os.path.join(target, "lake_register_2026.xlsx"), read_only=True, data_only=True)
    ws = wb["Lakes"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    out = {}
    for r in rows[1:]:
        if r[0] is None:
            continue
        d = dict(zip(hdr, r))
        out[d["PPFS code"]] = {"name": d["Lake"], "vno": int(d["Vellacott no."]), "reg": d["Regulation"],
                               "area": float(d["Surface area (ha)"]), "access": d["Access"]}
    return out


def counts(target, reg):
    by_vno = {v["vno"]: c for c, v in reg.items()}
    out = []
    for r in read_csv(os.path.join(target, "survey_flight_counts_2026.csv")):
        if r["boats"] == "" or r["time_over"] == "":
            continue
        out.append({"date": dt.date.fromisoformat(r["survey_date"]), "loop": r["loop"], "lake": by_vno[int(r["lake_no"])],
                    "t": K.parse_hm(r["time_over"]), "boats": int(r["boats"]), "shore": int(r["shore_anglers"])})
    return out


def interviews(target, reg):
    by_name = {v["name"].replace(" Lake", "").lower(): c for c, v in reg.items()}
    out = []
    for r in read_csv(os.path.join(target, "creel_interviews_2026.csv")):
        end = K.parse_hm(r["finished"])
        if r["started"]:
            start = K.parse_hm(r["started"])
        else:
            start = end - float(r["hours_fished"])
        out.append({"lake": by_name[r["lake"].strip().lower()], "date": dt.date.fromisoformat(r["date"]),
                    "size": int(r["party_size"]), "shore": r["fished_from"] == "shore", "start": start, "end": end,
                    "kept": int(r["rb_kept"]), "released": int(r["rb_released"]), "clipped": int(r["kept_ad_clipped"])})
    return out


# ------------------------------------------------------------------------------------------------- main call
def anglers_per_boat(rows):
    b = [r["size"] for r in rows if not r["shore"]]
    return float(np.mean(b))


def hour_shares(rows, weight="anglers"):
    """the share of the interviewed angler-hours falling in each hour of the angling day"""
    p = np.zeros(len(HOURS))
    for r in rows:
        w = r["size"] if weight == "anglers" else 1
        for i, h in enumerate(HOURS):
            lo, hi = max(r["start"], h), min(r["end"], h + 1)
            if hi > lo:
                p[i] += w * (hi - lo)
    return p / p.sum()


def strata_days():
    s = {}
    for d in K.SEASON_DAYS:
        s.setdefault(K.stratum(d), []).append(d)
    return s


def season_estimate(cts, area, apb, shares=None, combine="mean", interp=False, blanks_zero=None):
    """season angler-hours per hectare: shares None is the uniform day (count times the 17-hour day)"""
    byday = {}
    for c in cts:
        n = c["boats"] * apb + c["shore"]
        if shares is None:
            s = 1.0 / K.DAY_HOURS
        elif interp:
            mids = np.array(HOURS) + 0.5
            s = float(np.interp(c["t"], mids, shares))
        else:
            s = float(shares[int(math.floor(c["t"])) - int(K.DAY_OPEN)])
        byday.setdefault(c["date"], []).append((n, s))
    if blanks_zero:
        for d, k in blanks_zero:
            byday.setdefault(d, []).extend([(0.0, 1.0 / K.DAY_HOURS)] * k)
    tot = 0.0
    for key, days in strata_days().items():
        vals = []
        for d in days:
            if d not in byday:
                continue
            if combine == "mean":
                vals.append(float(np.mean([n / s for n, s in byday[d]])))
            else:
                vals.append(sum(n for n, s in byday[d]) / sum(s for n, s in byday[d]))
        tot += len(days) * float(np.mean(vals))
    return tot / area


def presence_share(rows, t, how, sh=None):
    """the share of a lake's interviewed angler-hours a count at clock time t stands for, read six ways: the hour bin
    the count falls in, the bin of the nearest whole hour, interpolated between bin midpoints or bin starts, the hour
    centred on the count, or the presence at the count's minute"""
    if how in ("bin", "nearest", "interp_mid", "interp_start"):
        sh = hour_shares(rows) if sh is None else sh
        if how == "bin":
            return float(sh[int(math.floor(t)) - int(K.DAY_OPEN)])
        if how == "nearest":
            i = min(max(int(math.floor(t + 0.5)) - int(K.DAY_OPEN), 0), len(HOURS) - 1)
            return float(sh[i])
        xs = np.array(HOURS) + (0.5 if how == "interp_mid" else 0.0)
        return float(np.interp(t, xs, sh))
    den = sum(r["size"] * (r["end"] - r["start"]) for r in rows)
    if how == "centred":
        lo, hi = t - 0.5, t + 0.5
        return sum(r["size"] * max(0.0, min(r["end"], hi) - max(r["start"], lo)) for r in rows) / den
    return sum(r["size"] for r in rows if r["start"] <= t < r["end"]) / den          # "minute"


def expand(cts, area, apb, share_of, combine="mean"):
    byday = {}
    for c in cts:
        byday.setdefault(c["date"], []).append((c["boats"] * apb + c["shore"], share_of(c)))
    tot = 0.0
    for key, days in strata_days().items():
        vals = []
        for d in days:
            if d not in byday:
                continue
            if combine == "mean":
                vals.append(float(np.mean([n / s for n, s in byday[d]])))
            else:
                vals.append(sum(n for n, s in byday[d]) / sum(s for n, s in byday[d]))
        tot += len(days) * float(np.mean(vals))
    return tot / area


READINGS = ("bin", "nearest", "interp_mid", "interp_start", "centred", "minute")


def presence_family(target):
    """every reading of each count against the lake's (or its regulation class's) interviewed presence: six ways of
    reading the count's hour, the lake's or the class's profile, the lake's, the class's or one pooled party size for
    boats, the mean of a survey day's count estimates or the ratio of its sums, plus shares weighted by parties and
    shares taken by day type"""
    reg = register(target)
    cts = counts(target, reg)
    iv = interviews(target, reg)
    by = {c: [r for r in iv if r["lake"] == c] for c in reg}
    cb = {c: [x for x in cts if x["lake"] == c] for c in reg}
    crow = {}
    for c in reg:
        crow.setdefault(reg[c]["reg"], []).extend(by[c])
    pooled_apb = anglers_per_boat(iv)
    out = {}
    for c in reg:
        rows_own, rows_cls = by[c], crow[reg[c]["reg"]]
        fam = {}
        for prof, rows in (("lake", rows_own), ("class", rows_cls)):
            sh = hour_shares(rows)
            for apbn, apb in (("lake", anglers_per_boat(rows_own)), ("class", anglers_per_boat(rows_cls)),
                              ("pooled", pooled_apb)):
                for how in READINGS:
                    cache = {}

                    def share_of(x, rows=rows, how=how, sh=sh, cache=cache):
                        k = round(x["t"], 6)
                        if k not in cache:
                            cache[k] = presence_share(rows, x["t"], how, sh)
                        return cache[k]
                    for comb in ("mean", "ratio"):
                        fam[(prof, apbn, how, comb)] = expand(cb[c], reg[c]["area"], apb, share_of, comb)
        apb = anglers_per_boat(rows_own)
        shp = hour_shares(rows_own, weight="parties")
        fam[("lake", "lake", "bin, parties", "mean")] = expand(cb[c], reg[c]["area"], apb,
                                                               lambda x: float(shp[int(math.floor(x["t"])) - 5]))
        shd = {k: hour_shares([r for r in rows_own if K.day_type(r["date"]) == k]) for k in ("weekday", "weekend")}
        fam[("lake", "lake", "bin, day type", "mean")] = expand(
            cb[c], reg[c]["area"], apb, lambda x: float(shd[K.day_type(x["date"])][int(math.floor(x["t"])) - 5]))
        out[c] = fam
    return out


def main_call(target):
    reg = register(target)
    cts = counts(target, reg)
    iv = interviews(target, reg)
    by_lake = {c: [r for r in iv if r["lake"] == c] for c in reg}
    cts_by = {c: [x for x in cts if x["lake"] == c] for c in reg}
    pooled_apb = anglers_per_boat(iv)
    pooled_sh = hour_shares(iv)
    cls = {c: v["reg"] for c, v in reg.items()}
    class_rows = {}
    for c in reg:
        class_rows.setdefault(cls[c], []).extend(by_lake[c])
    class_sh = {k: hour_shares(v) for k, v in class_rows.items()}
    class_apb = {k: anglers_per_boat(v) for k, v in class_rows.items()}
    res = {}
    for c, v in reg.items():
        a = v["area"]
        apb = anglers_per_boat(by_lake[c])
        sh = hour_shares(by_lake[c])
        r = {
            "R0": season_estimate(cts_by[c], a, pooled_apb),
            "R1": season_estimate(cts_by[c], a, apb),
            "R2": season_estimate(cts_by[c], a, apb, pooled_sh),
            "golden": season_estimate(cts_by[c], a, apb, sh),
        }
        fam = {
            "lake shares, mean of count ratios": r["golden"],
            "lake shares, ratio of summed counts": season_estimate(cts_by[c], a, apb, sh, combine="ratio"),
            "lake shares interpolated to the count's minute": season_estimate(cts_by[c], a, apb, sh, interp=True),
            "regulation-class shares": season_estimate(cts_by[c], a, apb, class_sh[cls[c]]),
            "regulation-class shares and anglers per boat": season_estimate(cts_by[c], a, class_apb[cls[c]], class_sh[cls[c]]),
            "lake shares, class anglers per boat": season_estimate(cts_by[c], a, class_apb[cls[c]], sh),
            "regulation-class shares, ratio of summed counts": season_estimate(cts_by[c], a, apb, class_sh[cls[c]], combine="ratio"),
        }
        r["family"] = fam
        r["apb"] = apb
        r["n_parties"] = len(by_lake[c])
        r["shares"] = sh
        res[c] = r
    out = {"reg": reg, "lakes": res}
    for k in ("R0", "R1", "R2", "golden"):
        out["set_" + k] = sorted(c for c in reg if res[c][k] >= K.THRESHOLD)
    return out


# ------------------------------------------------------------------------------------------------- ask A: releases
def _trip_sheets(target):
    wb = openpyxl.load_workbook(os.path.join(target, "quillet_creek_trip_sheets_2026.xlsx"), read_only=True, data_only=True)
    rows = list(wb["Trips 2026"].iter_rows(values_only=True))
    hdr = rows[0]
    trips = {}
    for r in rows[1:]:
        if r[0] is None:
            continue
        d = dict(zip(hdr, r))
        t = trips.setdefault(d["Trip"], {"date": dt.date.fromisoformat(str(d["Date"])[:10]), "raceway": int(d["Raceway"]),
                                         "load": float(d["Net load (kg)"]), "dests": [],
                                         "new_template": d["Tank temp (C)"] not in (None, "")})
        t["dests"].append(d["Destination"])
    return trips


def _samples(target):
    out = []
    for r in read_csv(os.path.join(target, "quillet_creek_raceway_samples_2026.csv")):
        out.append({"date": dt.date.fromisoformat(r["sample_date"]), "raceway": int(r["raceway"]),
                    "fpk": int(r["fish_counted"]) / (int(r["sample_g"]) / 1000.0), "onhand": int(r["fish_on_hand"])})
    return out


def _crosswalk(target):
    rows = read_csv(os.path.join(target, "quillet_creek_raceway_numbers.csv"))
    return {int(r["old_raceway"]): int(r["new_raceway"]) for r in rows}, dt.date.fromisoformat(rows[0]["from_date"])


def raceway_of_trip(t, cw, switch, mode="golden"):
    """the raceway each load came from, in the 2026 (new) numbering: the trip sheets kept the old numbers until their
    template changed (the tank temperature column); mode 'in_force' reads each trip's number in the numbering the
    crosswalk puts in force on the trip date"""
    if mode == "golden":
        return t["raceway"] if t["new_template"] else cw[t["raceway"]]
    return cw[t["raceway"]] if t["date"] < switch else t["raceway"]


def unified_samples(samples, cw, switch):
    """every sample under the 2026 (new) raceway numbers"""
    return [dict(s, raceway=(s["raceway"] if s["date"] >= switch else cw[s["raceway"]])) for s in samples]


def fpk_at(samples, raceway, d, how="latest"):
    ss = sorted((s for s in samples if s["raceway"] == raceway), key=lambda s: s["date"])
    before = [s for s in ss if s["date"] <= d]
    after = [s for s in ss if s["date"] > d]
    if how == "latest" or not after:
        return before[-1]["fpk"]
    a, b = before[-1], after[0]
    if how == "nearest":
        return a["fpk"] if (d - a["date"]).days <= (b["date"] - d).days else b["fpk"]
    w = (d - a["date"]).days / (b["date"] - a["date"]).days
    return a["fpk"] * (1 - w) + b["fpk"] * w


def releases(target, how="latest", raceways="golden", split="nets", doa=True):
    """catchable rainbow trout released alive into each lake: each load at its raceway's fish per kilogram, shared
    between the trip's drops by the nets the drop crew tallied, less the dead counted at the drop"""
    trips = _trip_sheets(target)
    cw, switch = _crosswalk(target)
    samples = unified_samples(_samples(target), cw, switch)
    drops = json.load(open(os.path.join(target, "quillet_creek_drop_tallies_2026.json")))["records"]
    by_trip = {}
    for x in drops:
        by_trip.setdefault(x["tripId"], []).append(x)
    fish = {}
    for tid, t in trips.items():
        rw = raceway_of_trip(t, cw, switch, raceways)
        f = fpk_at(samples, rw, t["date"], how)
        recs = by_trip[tid]
        nets = sum(x["nets"] for x in recs)
        for x in recs:
            share = x["nets"] / nets if split == "nets" else 1.0 / len(recs)
            fish[x["lakeCode"]] = fish.get(x["lakeCode"], 0.0) + t["load"] * share * f - (x["doaFish"] if doa else 0)
    return fish


# ------------------------------------------------------------------------------------------------- ask B: warm days
def _deployments(target):
    out = []
    for r in read_csv(os.path.join(target, "logger_deployments_2026.csv")):
        out.append({"serial": r["logger_serial"], "lake": r["lake_code"], "depth": float(r["depth_m"]),
                    "a": dt.datetime.strptime(r["deployed"], "%Y-%m-%d %H:%M"),
                    "b": dt.datetime.strptime(r["retrieved"], "%Y-%m-%d %H:%M") if r["retrieved"] else None})
    return out


def logger_clock_offsets(raw):
    """hours to add to each serial's stamps for Pacific daylight time: a 1 m logger's water is warmest in the late
    afternoon, so a serial whose warmest hour of the day sits near midnight was launched on UTC"""
    off = {}
    for s, recs in raw.items():
        prof = np.zeros(24)
        n = np.zeros(24)
        for t, v in recs:
            prof[t.hour] += v
            n[t.hour] += 1
        prof = prof / np.maximum(n, 1)
        off[s] = -7 if int(prof.argmax()) in (21, 22, 23, 0, 1, 2, 3) else 0
    return off


def warm_days(target, start=dt.date(2026, 7, 1), end=dt.date(2026, 8, 31), line=20.0, mode="golden", combine="pooled"):
    """for each lake with a logger at 1 m: the days in the window whose 1 m readings averaged above the line over the
    local day; each reading belongs to the deployment its serial was in at that moment (golden), or to the station
    the download names (mode 'site')"""
    dep = _deployments(target)
    raw = {}
    site = {}
    for r in read_csv(os.path.join(target, "lake_temperature_loggers_2026.csv")):
        raw.setdefault(r["Logger SN"], []).append((dt.datetime.strptime(r["Date Time"], "%Y-%m-%d %H:%M"),
                                                   float(r["Temp (C)"])))
        site[r["Logger SN"]] = (r["Site"], float(r["Depth (m)"]))
    reg = register(target)
    by_name = {v["name"].replace(" Lake", ""): c for c, v in reg.items()}
    off = logger_clock_offsets(raw)
    per = {}
    for s, recs in raw.items():
        for t, v in recs:
            tl = t + dt.timedelta(hours=off[s])
            if mode == "golden":
                hit = None
                for d in dep:
                    if d["serial"] == s and d["a"] <= tl and (d["b"] is None or tl <= d["b"]):
                        hit = d
                        break
                if hit is None or hit["depth"] >= 2:
                    continue
                lake = hit["lake"]
            else:
                nm, depth = site[s]
                if depth >= 2:
                    continue
                lake = by_name[nm]
            if start <= tl.date() <= end:
                per.setdefault((lake, tl.date()), {}).setdefault(s, []).append(v)
    lakes = sorted({c for c, d in per})
    out, means = {}, {}
    for c in lakes:
        k = 0
        for (cc, day), m in per.items():
            if cc != c:
                continue
            if combine == "pooled":
                mu = float(np.mean([v for vs in m.values() for v in vs]))
            else:
                mu = float(np.mean([np.mean(vs) for vs in m.values()]))
            means[(c, day)] = mu
            if mu > line:
                k += 1
        out[c] = k
    return out, means


def lake_day_logger_means(target, start=dt.date(2026, 7, 1), end=dt.date(2026, 8, 31)):
    """each logger's own mean for each lake-day at 1 m in the window, with every reading placed by the deployment its
    serial was in and read in Pacific time: the means a reader would take from one logger alone"""
    dep = _deployments(target)
    raw = {}
    for r in read_csv(os.path.join(target, "lake_temperature_loggers_2026.csv")):
        raw.setdefault(r["Logger SN"], []).append((dt.datetime.strptime(r["Date Time"], "%Y-%m-%d %H:%M"),
                                                   float(r["Temp (C)"])))
    off = logger_clock_offsets(raw)
    per = {}
    for s, recs in raw.items():
        for t, v in recs:
            tl = t + dt.timedelta(hours=off[s])
            for d in dep:
                if d["serial"] == s and d["a"] <= tl and (d["b"] is None or tl <= d["b"]):
                    if d["depth"] < 2 and start <= tl.date() <= end:
                        per.setdefault((d["lake"], tl.date()), {}).setdefault(s, []).append(v)
                    break
    return {k: {s: float(np.mean(v)) for s, v in m.items()} for k, m in per.items()}, per


def run(target):
    return {"main": main_call(target), "releases": releases(target), "warm": warm_days(target)}
