"""Centre the asks' figures in their rounding bins without touching the call, on rows the call never reads: one
facility's reported phosphorus for one month (the reports are outside the load inventory), and one unsplit cover crop
contract's acres (the contracts are outside it). Deterministic: the same rows are chosen on every build."""
import csv
import datetime as dt
import os

import numpy as np
import pandas as pd

import calc as C
import pack as P
import world as W

EDGE = 2.0      # kilograms or acres from a nearest-10 rounding edge


def _write(path, df):
    """rewrite a csv in place, keeping the export's '#' header lines"""
    with open(path, encoding="utf-8") as fh:
        head = [line for line in fh.read().splitlines() if line.startswith("#")]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        for line in head:
            fh.write(line + "\r\n")
        df.to_csv(fh, index=False, lineterminator="\r\n", quoting=csv.QUOTE_MINIMAL)


def _dist(v):
    frac = v / 10.0 - np.floor(v / 10.0)
    return abs(frac - 0.5) * 10.0


def wastewater(target):
    """nudge one upstream facility's reported phosphorus for the period ending 30 June 2026 (as first reported) so each
    tributary's figure sits mid-bin"""
    L = C.load(target)
    gold = C.ask_wastewater(L)
    path = os.path.join(target, P.FILES["dmr"])
    d = pd.read_csv(path, dtype=str, comment="#")
    walk = C.stream_to_tributary(L)
    reg = C.register(L)
    moved = {}
    for name, v in gold.items():
        if _dist(v) >= EDGE:
            continue
        want = (4.0 if (v / 10 - np.floor(v / 10)) < 0.5 else -4.0)
        for pid, fname, rw, rkm, mgd, tp, mode, resub, reloc in W.FACILITIES:
            trib, join = walk(rw)
            if trib != name or reloc:
                continue
            pos = rkm if join is None else join
            if pos <= reg[trib]["rkm"]:
                continue
            june = d["PERMIT_ID"].eq(pid) & d["MONITORING_PERIOD_END_DATE"].eq("2026-06-30")
            if d.loc[june, "SUBMISSION_TYPE"].eq("Resubmission").any():
                continue
            sel = june & d["STATISTICAL_BASE"].eq("MO AVG") & d["PARAMETER_DESC"].str.startswith("Phosphorus")
            i = d.index[sel][0]
            n_days = (dt.date(2026, 6, 30) - dt.date.fromisoformat(d.at[i, "MONITORING_PERIOD_START_DATE"])).days + 1
            if d.at[i, "DMR_UNIT"] == "lb/d":
                d.at[i, "DMR_VALUE"] = "%.2f" % (float(d.at[i, "DMR_VALUE"]) + want / (W.LB_KG * n_days))
            else:
                f = float(d.loc[june & d["PARAMETER_DESC"].str.startswith("Flow"), "DMR_VALUE"].iloc[0])
                d.at[i, "DMR_VALUE"] = "%.3f" % (float(d.at[i, "DMR_VALUE"]) + want / (f * W.GAL_L * n_days))
            moved[name] = (pid, want)
            break
    _write(path, d)
    return moved


def straddle(target):
    """where a watershed's overlay acres and the acres its contract lines are filed under round alike, move part of one
    straddling field across the divide on the overlay (the field the overlay draws differently from its line's watershed
    is the device; the call never reads the overlay)"""
    path = os.path.join(target, P.FILES["fields"])
    k10 = lambda v: int(round(v / 10.0)) * 10
    moved = {}
    for _ in range(8):
        L = C.load(target)
        gold, lab = C.ask_cover(L), C.ask_cover(L, "label_field")
        f = L["fields"].copy()
        c = L["contracts"]
        n = c["amendment_no"].astype(int)
        live = c[n.eq(n.groupby(c["contract_id"]).transform("max")) & (c["first_crop_year"].astype(int) <= W.WY)
                 & (c["last_crop_year"].astype(int) >= W.WY)]
        todo = [w for w in gold if k10(gold[w]) == k10(lab[w]) or abs(gold[w] - lab[w]) < 12]
        if not todo:
            break
        for name in todo:
            up = gold[name] >= lab[name]        # widen the gap the way it already leans
            fids = sorted(set(live.loc[live["watershed"].eq(name), "field_id"]))
            two = sorted((x for x in fids if (f["field_id"] == x).sum() == 2),
                         key=lambda x: -float(f.loc[f["field_id"].eq(x), "field_acres"].iloc[0]))
            for fid in two:
                idx = f.index[f["field_id"].eq(fid)]
                own = [i for i in idx if f.at[i, "watershed"] == name][0]
                oth = [i for i in idx if f.at[i, "watershed"] != name][0]
                a, s0 = float(f.at[own, "field_acres"]), float(f.at[own, "share_of_field"])
                sh = min(0.85, s0 + 24.0 / a) if up else max(0.52, s0 - 24.0 / a)
                if abs(sh - s0) < 0.1:
                    continue
                f.at[own, "share_of_field"] = "%.2f" % sh
                f.at[oth, "share_of_field"] = "%.2f" % (1 - sh)
                moved[name] = fid
                break
        _write(path, f)
    return moved


def cover(target):
    """nudge one wholly-inside, single-field, unamended contract so each watershed's figure sits mid-bin: the field's
    area in the overlay and the contract's acres move together"""
    L = C.load(target)
    gold = C.ask_cover(L)
    cpath, fpath = os.path.join(target, P.FILES["contracts"]), os.path.join(target, P.FILES["fields"])
    c = pd.read_csv(cpath, dtype=str, comment="#")
    f = pd.read_csv(fpath, dtype=str, comment="#")
    whole = set(f.loc[f["share_of_field"].eq("1.00"), "field_id"])
    lines = c.groupby(["contract_id", "amendment_no"])["field_id"].transform("count")
    amended = set(c.loc[c["amendment_no"].ne("0"), "contract_id"])
    pick = c[(c["first_crop_year"].astype(int) <= W.WY) & (c["last_crop_year"].astype(int) >= W.WY) & lines.eq(1)
             & ~c["contract_id"].isin(amended) & c["field_id"].isin(whole)]
    moved = {}
    for name, v in gold.items():
        if _dist(v) >= EDGE:
            continue
        rows = pick[pick["watershed"].eq(name)]
        if len(rows) == 0:
            continue
        want = (4.0 if (v / 10 - np.floor(v / 10)) < 0.5 else -4.0)
        i = rows.index[0]
        c.at[i, "contracted_acres"] = "%.1f" % (float(c.at[i, "contracted_acres"]) + want)
        j = f.index[f["field_id"].eq(c.at[i, "field_id"])][0]
        f.at[j, "field_acres"] = "%.1f" % (float(f.at[j, "field_acres"]) + want)
        moved[name] = (c.at[i, "contract_id"], want)
    _write(cpath, c)
    _write(fpath, f)
    return moved
