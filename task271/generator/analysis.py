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
def releases(target):
    """rainbow trout released alive into each lake: each trip's load counted once at its raceway's fish per kilogram
    on the loading day, shared between its drops by the nets the drop crew tallied, less the dead at release; a trip
    the drop crew recorded as returned to the hatchery released nothing"""
    reg = register(target)
    by_name = {v["name"]: c for c, v in reg.items()}
    wb = openpyxl.load_workbook(os.path.join(target, "quillet_creek_trip_sheets_2026.xlsx"), read_only=True, data_only=True)
    rows = list(wb["Trips 2026"].iter_rows(values_only=True))
    hdr = rows[0]
    trips = {}
    for r in rows[1:]:
        if r[0] is None:
            continue
        d = dict(zip(hdr, r))
        t = trips.setdefault(d["Trip"], {"date": dt.date.fromisoformat(str(d["Date"])[:10]), "raceway": str(d["Raceway"]),
                                         "load": float(d["Net load (kg)"]), "dests": []})
        t["dests"].append(by_name[d["Destination"]])
    renum = {r["old_raceway"]: int(r["new_raceway"]) for r in read_csv(os.path.join(target, "quillet_creek_raceway_numbers.csv"))}
    switch = dt.date.fromisoformat(read_csv(os.path.join(target, "quillet_creek_raceway_numbers.csv"))[0]["from_date"])
    samples = {}
    for r in read_csv(os.path.join(target, "quillet_creek_raceway_samples_2026.csv")):
        samples[(dt.date.fromisoformat(r["sample_date"]), r["raceway"])] = int(r["fish_counted"]) / (int(r["sample_g"]) / 1000.0)
    drops = json.load(open(os.path.join(target, "quillet_creek_drop_tallies_2026.json")))["records"]
    by_trip = {}
    for x in drops:
        by_trip.setdefault(x["trip_id"], []).append(x)
    fish = {c: 0.0 for c in reg}
    for tid, t in trips.items():
        lab = t["raceway"]
        if t["date"] >= switch:
            key = str(renum[lab]) if lab in renum else lab
        else:
            key = lab
        fpk = samples[(t["date"], key)]
        recs = [x for x in by_trip.get(tid, []) if x["lake_code"] != "RETURNED"]
        nets = sum(x["nets"] for x in by_trip.get(tid, []))
        if nets == 0:
            continue
        for x in recs:
            fish[x["lake_code"]] += t["load"] * x["nets"] / nets * fpk - x["doa"]
    return {c: v for c, v in fish.items() if v > 0}


# ------------------------------------------------------------------------------------------------- ask B: warm days
def warm_days(target, start=dt.date(2026, 7, 1), end=dt.date(2026, 8, 31), line=20.0):
    """for each lake with a 1 m logger: the days in the window whose mean 1 m temperature (local day) was above the line;
    each reading belongs to the deployment its serial was in at that moment, and a logger launched on UTC is read in
    Pacific time"""
    dep = [{"serial": r["logger_serial"], "lake": r["lake_code"], "depth": float(r["depth_m"]),
            "a": dt.datetime.strptime(r["deployed"], "%Y-%m-%d %H:%M"), "b": dt.datetime.strptime(r["retrieved"], "%Y-%m-%d %H:%M")}
           for r in read_csv(os.path.join(target, "logger_deployments_2026.csv"))]
    raw = {}
    for r in read_csv(os.path.join(target, "lake_temperature_loggers_2026.csv")):
        raw.setdefault(r["logger_serial"], []).append((dt.datetime.strptime(r["date_time"], "%Y-%m-%d %H:%M"), float(r["temp_c"])))
    # each serial's clock: a logger whose warmest time of day sits near midnight was launched on UTC
    offset = {}
    for s, recs in raw.items():
        prof = np.zeros(24)
        n = np.zeros(24)
        for t, v in recs:
            prof[t.hour] += v
            n[t.hour] += 1
        prof = prof / np.maximum(n, 1)
        offset[s] = -7 if prof.argmax() in (22, 23, 0, 1, 2) else 0
    daily = {}
    for s, recs in raw.items():
        for t, v in recs:
            tl = t + dt.timedelta(hours=offset[s])
            for d in dep:
                if d["serial"] == s and d["a"] <= tl <= d["b"]:
                    if d["depth"] < 2:
                        daily.setdefault((d["lake"], tl.date()), []).append(v)
                    break
    lakes = sorted({d["lake"] for d in dep if d["depth"] < 2})
    out = {}
    means = {}
    for c in lakes:
        k = 0
        for i in range((end - start).days + 1):
            day = start + dt.timedelta(days=i)
            vals = daily.get((c, day))
            if not vals:
                continue
            m = float(np.mean(vals))
            means[(c, day)] = m
            if m > line:
                k += 1
        out[c] = k
    return out, means, offset


def run(target):
    return {"main": main_call(target), "releases": releases(target), "warm": warm_days(target)}
