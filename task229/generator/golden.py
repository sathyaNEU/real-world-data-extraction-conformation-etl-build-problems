"""The golden: every graded figure computed from the shipped files under target/ alone.

This module reads only the bundle. It is the first solver: the generator's own world state is never
consulted here. The grid of wrong readings lives in readings(), so checks.py can assert every cell.
"""
import datetime as dt
import json
import math
import os

import numpy as np
import pandas as pd
import openpyxl

UTC = dt.timezone.utc
AEST = dt.timezone(dt.timedelta(hours=10))
WEEK_START = dt.datetime(2026, 10, 5, tzinfo=AEST)
WEEK_END = WEEK_START + dt.timedelta(days=7)
REFERENCE, K = 99.50, 3
RELEASES = ["EM3.10.9", "EM3.11.4", "EM3.12.0", "EM3.12.1", "EM3.12.2", "PX5.2.7", "PX5.3.0", "PX5.3.1"]


def nsw_tz(day):
    y = day.year

    def first_sun(m):
        x = dt.date(y, m, 1)
        return x + dt.timedelta(days=(6 - x.weekday()) % 7)
    off = 11 if (day >= first_sun(10) or day < first_sun(4)) else 10
    return dt.timezone(dt.timedelta(hours=off))


def parse_local(s):
    t = dt.datetime.strptime(s, "%d/%m/%Y %H:%M")
    return t.replace(tzinfo=nsw_tz(t.date()))


def load(target):
    p = lambda f: os.path.join(target, f)
    mdm = pd.read_csv(p("mdm_interval_receipts_20261005_20261011.csv"), dtype={"NMI": str, "READ_DATE": str})
    mdm["received"] = pd.to_datetime(mdm["RECEIVED_UTC"], utc=True)
    rd = pd.to_datetime(mdm["READ_DATE"], format="%Y%m%d")
    # cut-off: 06:00 AEST on the day after the read date = 20:00 UTC on the read date
    mdm["cutoff"] = (rd + pd.Timedelta(hours=20)).dt.tz_localize("UTC")
    mdm["expected"] = mdm["QTY_A"] + mdm["QTY_S"] + mdm["QTY_F"]
    cat = pd.read_csv(p("fw_release_catalogue.csv"))
    img2rel = dict(zip(cat["hes_image"], cat["release"]))
    hes = json.load(open(p("hes_meter_firmware_history.json")))
    wb = openpyxl.load_workbook(p("mp_installation_register_20261012.xlsx"), read_only=True)
    meters = []
    for row in list(wb["Meters"].iter_rows(values_only=True))[3:]:
        nmi11, serial, model, module, inst, rem = row
        meters.append(dict(nmi=str(nmi11)[:10], serial=str(serial).zfill(8), installed=parse_local(inst),
                           removed=parse_local(rem) if rem else None))
    meters = pd.DataFrame(meters)
    return dict(mdm=mdm, img2rel=img2rel, hes=hes, meters=meters, target=target)


def running_builds(hes, img2rel, dedupe=True, failed_moves=False, staged_moves=False):
    """Per meter: list of (from_utc, release) build spells, from the HES history."""
    out = {}
    for m in hes["meters"]:
        serial = m["meter_id"].replace("MTR-", "")
        seen, spells = set(), []
        for e in sorted(m["events"], key=lambda x: (x["ts_utc"], x["seq"])):
            if dedupe:
                if e["event_id"] in seen:
                    continue
                seen.add(e["event_id"])
            t = dt.datetime.strptime(e["ts_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            moves = e["type"] in ("COMMISSIONED", "FW_ACTIVATED") or (failed_moves and e["type"] == "FW_ACTIVATION_FAILED") \
                or (staged_moves and e["type"] == "FW_IMAGE_STAGED")
            if e["type"] == "FW_ROLLBACK_OK" and failed_moves:
                moves = True
            if moves and e["image"]:
                spells.append((t, img2rel[e["image"]]))
        out[serial] = spells
    return out


def build_at(spells, t):
    cur = None
    for (s, rel) in spells:
        if s <= t:
            cur = rel
    return cur


def assessed(D, mode="fullweek", spells=None):
    """Installation -> release, under a population reading.
    fullweek: one meter all week, on one build all week (the standard).
    start / end: every installation, on its build at the week start / end."""
    spells = spells or running_builds(D["hes"], D["img2rel"])
    mt = D["meters"]
    out = {}
    for nmi, g in mt.groupby("nmi"):
        g = g.sort_values("installed")
        if mode == "fullweek":
            ov = g[(g["installed"] < WEEK_END) & (g["removed"].isna() | (g["removed"] > WEEK_START))]
            if len(ov) != 1:
                continue
            m = ov.iloc[0]
            if m["installed"] > WEEK_START or (m["removed"] is not None and not pd.isna(m["removed"]) and m["removed"] < WEEK_END):
                continue
            sp = spells.get(m["serial"], [])
            b0 = build_at(sp, WEEK_START)
            if any(WEEK_START < s < WEEK_END for s, _ in sp) or b0 is None:
                continue
            out[nmi] = b0
        else:
            t = WEEK_START if mode == "start" else WEEK_END - dt.timedelta(seconds=1)
            live = g[(g["installed"] <= t) & (g["removed"].isna() | (g["removed"] > t))]
            if len(live) == 0:
                continue
            b = build_at(spells.get(live.iloc[0]["serial"], []), t)
            if b:
                out[nmi] = b
    return out


def versions(mdm, which="cutoff"):
    if which == "cutoff":
        x = mdm[mdm["received"] < mdm["cutoff"]]
        return x.sort_values("received").groupby(["NMI", "NMI_SUFFIX", "READ_DATE"]).tail(1)
    if which == "latest":
        return mdm.sort_values("received").groupby(["NMI", "NMI_SUFFIX", "READ_DATE"]).tail(1)
    if which == "first":
        return mdm.sort_values("received").groupby(["NMI", "NMI_SUFFIX", "READ_DATE"]).head(1)
    raise ValueError(which)


def score(v, pop, unit="installation", err="installation"):
    """Read health, n, standard error, lower limit and the alert, per release, under one reading."""
    x = v[v["NMI"].isin(pop.keys())].copy()
    x["release"] = x["NMI"].map(pop)
    res = {}
    for rel in RELEASES:
        g = x[x["release"] == rel]
        if len(g) == 0:
            res[rel] = None
            continue
        inst = g.groupby("NMI")[["QTY_A", "expected"]].sum()
        share = 100.0 * inst["QTY_A"] / inst["expected"]
        n = len(inst)
        if unit == "installation":
            rh = share.mean()
        elif unit == "pooled":
            rh = 100.0 * g["QTY_A"].sum() / g["expected"].sum()
        elif unit == "row":
            rh = (100.0 * g["QTY_A"] / g["expected"]).mean()
        elif unit == "stream":
            st = g.groupby(["NMI", "NMI_SUFFIX"])[["QTY_A", "expected"]].sum()
            rh = (100.0 * st["QTY_A"] / st["expected"]).mean()
        if err == "installation":
            se = share.std(ddof=1) / math.sqrt(n)
        elif err == "installation_ddof0":
            se = share.std(ddof=0) / math.sqrt(n)
        elif err == "binomial_reads":
            p = rh / 100.0
            se = 100.0 * math.sqrt(p * (1 - p) / g["expected"].sum())
        elif err == "binomial_installations":
            p = rh / 100.0
            se = 100.0 * math.sqrt(p * (1 - p) / n)
        elif err == "none":
            se = 0.0
        lcl = REFERENCE - K * se
        res[rel] = dict(n=n, rh=rh, se=se, lcl=lcl, fire=bool(rh < lcl))
    return res


def fire_set(res):
    return tuple(sorted(r for r, v in res.items() if v and v["fire"]))


# ------------------------------------------------------------------ the asks

def wave8_moves(D):
    wb = openpyxl.load_workbook(os.path.join(D["target"], "wave8_schedule_v2.xlsx"), read_only=True)
    rows = []
    for name in ("Batch A 13-10", "Batch B 14-10"):
        for r in list(wb[name].iter_rows(values_only=True))[2:]:
            if r[1] is None:
                continue
            rows.append(dict(serial=str(r[1]).zfill(8), target=r[5]))
    sched = pd.DataFrame(rows).drop_duplicates()
    spells = running_builds(D["hes"], D["img2rel"])
    mt = D["meters"]
    in_service = mt[mt["removed"].isna()].set_index("serial")["nmi"].to_dict()
    end = dt.datetime(2026, 10, 12, 4, 0, tzinfo=UTC)
    out = {}
    for tgt, g in sched.groupby("target"):
        nmis = set()
        for s in g["serial"]:
            if s not in in_service:
                continue
            if build_at(spells.get(s, []), end) == tgt:
                continue
            nmis.add(in_service[s])
        out[tgt] = len(nmis)
    return out


def wave7_cost(D, vcut=None, day_clock="AEST"):
    vcut = vcut if vcut is not None else versions(D["mdm"], "cutoff")
    mt = D["meters"]
    serial2nmi = mt.set_index("serial")["nmi"].to_dict()
    moved = {}
    for m in D["hes"]["meters"]:
        serial = m["meter_id"].replace("MTR-", "")
        seen = set()
        for e in m["events"]:
            if e["event_id"] in seen:
                continue
            seen.add(e["event_id"])
            if e["type"] == "FW_ACTIVATED" and (e["job"] or "").startswith("WAVE7"):
                t = dt.datetime.strptime(e["ts_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
                tz = AEST if day_clock == "AEST" else (dt.timezone(dt.timedelta(hours=11)) if day_clock == "AEDT" else UTC)
                moved[serial] = (D["img2rel"][e["image"]], t.astimezone(tz).strftime("%Y%m%d"))
    per = {}
    v = vcut.set_index(["NMI", "READ_DATE"])
    miss = (vcut["expected"] - vcut["QTY_A"]).groupby([vcut["NMI"], vcut["READ_DATE"]]).sum().to_dict()
    for serial, (rel, day) in moved.items():
        nmi = serial2nmi[serial]
        c = per.setdefault(rel, dict(installations=set(), missing=0))
        c["installations"].add(nmi)
        c["missing"] += int(miss.get((nmi, day), 0))
    return {k: dict(installations=len(v_["installations"]), missing=v_["missing"]) for k, v_ in per.items()}


def solve(target):
    D = load(target)
    pop = assessed(D, "fullweek")
    vc = versions(D["mdm"], "cutoff")
    res = score(vc, pop)
    return D, dict(scorecard=res, fire=fire_set(res), wave8=wave8_moves(D), wave7=wave7_cost(D, vc))
