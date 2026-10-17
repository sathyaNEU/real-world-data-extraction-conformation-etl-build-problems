"""Independent verifier for task152: reads only the shipped bundle (target/) and the goldens, on its own code path
(pandas and pypdf, no generator module but the file names), and recomputes the volume, the P50, the standard
deviation, each inverter's 2025 availability and each year's over or under, then compares them with the goldens
and figures.json."""
from __future__ import annotations

import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from pypdf import PdfReader

OLD = "hrs_scada_daily_report_2015-11-20_to_2020-03-02.csv"
NEW = "hadley_scada_daily_2020-03-03_to_2026-09-30.csv"
TAGS = "scada_tag_crosswalk.csv"
WO = "tresco_work_orders_hadley_ranch_2015-2026.xlsx"
LT = "clearfield_hadley_ranch_poa_hourly_2001-2025.csv"
RIG = "corvane_fa-2026-114_hadley_ranch_side_by_side.pdf"
HOURLY = "inverter_hourly_ac_2025.csv"
MET = "met_station_hourly_2025.csv"
INTER = "vsipd_interruptions_hadley_ranch_69kv_tap_2025.pdf"
LEGACY = "vsipd_acct_7731-0459_daily_legacy_2015-2020.txt"
MDM = "vsipd_acct_7731-0459_mdm_daily_2019-10-01_2025-12-31.csv"
BLOTTER = "power_forward_blotter_2015-2025.xlsx"
CONF = "westmark_confirmations_hadley_ranch_cy2016-cy2026.pdf"


def pdf_text(path):
    return "\n".join(pg.extract_text() or "" for pg in PdfReader(path).pages)


def daily(t):
    tags = pd.read_csv(os.path.join(t, TAGS), dtype=str).fillna("")
    tags = tags[tags.scada_tag.str.startswith("B")]
    col = {r.scada_tag: (r.original_tag or "INV07") for r in tags.itertuples()}
    o = pd.read_csv(os.path.join(t, OLD))
    o["day"] = pd.to_datetime(o["Date"], format="%m/%d/%Y")
    recs = []
    for k in range(1, 17):
        tg = "INV%02d" % k
        recs.append(pd.DataFrame({"day": o.day, "inv": tg, "dc": o[tg + "_DC_kWh"], "ac": o[tg + "_AC_kWh"],
                                  "op": o[tg + "_OpHrs"]}))
    inv_old = pd.concat(recs)
    met_old = pd.DataFrame({"day": o.day, "poa": o["POA_Irr_kWh/m2"], "tmod": o["TMod_IW_C"],
                            "exp": o["Meter_Export_kWh"], "imp": o["Meter_Import_kWh"]})
    n = pd.read_csv(os.path.join(t, NEW))
    n["day"] = (pd.to_datetime(n.day_start_utc.str[:19]) - pd.Timedelta(hours=7)).dt.normalize()
    iv = n[n.device.str.startswith("B")].copy()
    iv["inv"] = iv.device.map(col)
    iv = iv.pivot_table(index=["day", "inv"], columns="point", values="value", aggfunc="first").reset_index()
    inv_new = pd.DataFrame({"day": iv.day, "inv": iv.inv, "dc": iv.E_DC * 1000, "ac": iv.E_AC * 1000, "op": iv.T_OP})
    mt = n[~n.device.str.startswith("B")].pivot_table(index="day", columns="point", values="value", aggfunc="first")
    met_new = pd.DataFrame({"day": mt.index, "poa": mt.H_POA.values, "tmod": mt.T_MOD_IW.values,
                            "exp": mt.E_EXP.values * 1000, "imp": mt.E_IMP.values * 1000})
    inv = pd.concat([inv_old, inv_new]).reset_index(drop=True)
    met = pd.concat([met_old, met_new]).set_index("day").sort_index()
    inv = inv.merge(met[["poa", "tmod"]], left_on="day", right_index=True)
    inv["opmax"] = inv.groupby("day").op.transform("max")
    inv["full"] = inv.op >= inv.opmax - 0.1
    return inv, met


def golden(t):
    inv, met = daily(t)
    wo = pd.read_excel(os.path.join(t, WO))
    cl = wo[(wo.Type == "CLN") & wo.Asset.str.startswith("BLK")]
    clean = set()
    for a, d in zip(cl.Asset, pd.to_datetime(cl.Completed).dt.normalize()):
        blk = int(a[3:])
        for k in (1, 2, 3):
            for j in range(4 * (blk - 1) + 1, 4 * blk + 1):
                clean.add((d + pd.Timedelta(days=k), "INV%02d" % j))
    inv["clean"] = [(d, i) in clean for d, i in zip(inv.day, inv.inv)]
    inv["y"] = inv.dc / (inv.poa * 2520.0 * (1 - 0.0042 * (inv.tmod - 25)))
    base = (inv.day >= "2025-10-01") & (inv.day <= "2026-09-30")
    sel = inv.clean & inv.full
    wear = inv[sel & base].y.mean() / inv[sel & (inv.day.dt.year == 2016)].y.mean()
    mb = met.loc["2025-10-01":"2026-09-30"]
    pr = (mb.exp - mb.imp).sum() / (mb.poa.sum() * 40320.0)
    txt = pdf_text(os.path.join(t, RIG))
    m = re.search(r"Twelve months\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", txt)
    gain = float(m.group(3)) / float(m.group(2))
    lt = pd.read_csv(os.path.join(t, LT), comment="#")
    loc = pd.to_datetime(lt.period_end_utc) - pd.Timedelta(hours=8)
    H = lt.poa_wm2.groupby(loc.dt.year).sum() / 1000.0
    H = H.loc[2001:2025]
    E = pr * gain / wear * 37324.8 * H.values / 1000.0
    p50, sd = E.mean(), E.std(ddof=1)
    p90 = p50 - 1.2816 * sd
    return dict(volume=int(math.floor(p90 / 1000.0)) * 1000, p50=p50, sd=sd, p90=p90, wear=wear, pr=pr, gain=gain)


def ask_a(t):
    met = pd.read_csv(os.path.join(t, MET))
    prod = pd.to_datetime(met.loc[met.poa_wm2 >= 50, "hour_beginning_mst"])
    h = pd.read_csv(os.path.join(t, HOURLY))
    h["start"] = pd.to_datetime(h.interval_end_utc.str[:19]) - pd.Timedelta(hours=8)
    txt = pdf_text(os.path.join(t, INTER))
    grid = [(pd.Timestamp(pd.to_datetime(a, format="%m/%d/%Y %H:%M")), pd.Timestamp(pd.to_datetime(b, format="%m/%d/%Y %H:%M")))
            for a, b in re.findall(r"HR-25-\d{3}\s+(\d\d/\d\d/\d{4} \d\d:\d\d)\s+(\d\d/\d\d/\d{4} \d\d:\d\d)", txt)]
    wo = pd.read_excel(os.path.join(t, WO))
    own = []
    for desc, done in zip(wo[wo.Type == "OWN"].Description, wo[wo.Type == "OWN"].Completed):
        done = pd.Timestamp(done)
        if done.year != 2025:
            continue
        m = re.search(r"stop (.+?) for .+?Stopped (\d\d):(\d\d), restarted (\d\d):(\d\d)", desc)
        d0 = done.normalize()
        own.append(([x.strip() for x in m.group(1).split(",")], d0 + pd.Timedelta(hours=int(m.group(2)), minutes=int(m.group(3))),
                    d0 + pd.Timedelta(hours=int(m.group(4)), minutes=int(m.group(5)))))
    out = {}
    for tag, g in h.groupby("device"):
        g = g.set_index("start").sort_index()
        full = pd.DataFrame(index=prod)
        full["ac"] = g.ac_kwh.reindex(prod)
        reg_end = g.ac_register_kwh
        reg_start = g.ac_register_kwh - g.ac_kwh
        prev = reg_end.reindex(pd.date_range(g.index.min(), g.index.max(), freq="h")).ffill()
        nxt = reg_start.reindex(pd.date_range(g.index.min(), g.index.max(), freq="h")).bfill()
        miss = full.ac.isna()
        adv = (nxt.reindex(prod) - prev.reindex(prod)).values
        delivered = np.where(miss, adv > 0.5, full.ac.values > 0)
        P = len(prod)
        U = X = 0
        for ts, dlv in zip(prod, delivered):
            if dlv:
                continue
            e = ts + pd.Timedelta(hours=1)
            excl = any(ts < b + pd.Timedelta(minutes=10) and e > a for a, b in grid) or \
                any(tag in devs and ts < b and e > a for devs, a, b in own)
            if excl:
                X += 1
            else:
                U += 1
        out[tag] = 100.0 * (1.0 - U / (P - X))
    return out


def ask_b(t):
    rows = []
    with open(os.path.join(t, LEGACY), encoding="utf-8") as fh:
        for ln in fh:
            ln = ln.rstrip("\r\n")
            if ln:
                end = pd.to_datetime(ln[30:38], format="%Y%m%d")
                rows.append((ln[10:16].strip(), ln[26:30].strip(), end - pd.Timedelta(days=1), float(ln[43:57])))
    leg = pd.DataFrame(rows, columns=["sp", "ch", "day", "kwh"])
    m = pd.read_csv(os.path.join(t, MDM), dtype={"service_point": str})
    m = m.sort_values("version").groupby(["service_point", "channel", "read_date"]).tail(1)
    m = pd.DataFrame({"sp": m.service_point, "ch": m.channel, "day": pd.to_datetime(m.read_date), "kwh": m.kwh})
    m = m[m.day > "2020-02-29"]
    a = pd.concat([leg, m])
    a = a[a.sp == "0417"]
    a["s"] = np.where(a.ch == "REC", a.kwh, -a.kwh)
    net = a.groupby(a.day.dt.year).s.sum() / 1000.0
    b = pd.read_excel(os.path.join(t, BLOTTER))
    txt = pdf_text(os.path.join(t, CONF)).replace("\n", " ")
    am = {k: float(v.replace(",", "")) for k, v in re.findall(r"reference (MVB-\d{4}-\d{3})\. The Contract Quantity is amended to ([\d,]+) MWh", txt)}
    b["q"] = [am.get(i, q) for i, q in zip(b["Trade ID"], b["Quantity (MWh)"])]
    b["s"] = np.where(b["B/S"] == "S", b.q, -b.q)
    sold = b.groupby(b.Delivery.str[2:].astype(int)).s.sum()
    return {y: net[y] - sold[y] for y in range(2016, 2026)}


def rnd(x):
    return int(math.floor(x + 0.5)) if x >= 0 else -int(math.floor(-x + 0.5))


def main(target, golden_dir):
    task = os.path.dirname(os.path.abspath(target))
    F = json.load(open(os.path.join(task, "generator", "figures.json")))
    g = golden(target)
    a = ask_a(target)
    b = ask_b(target)
    fails = []
    if g["volume"] != F["call"]["volume_mwh"]:
        fails.append("volume %s" % g["volume"])
    if int(math.floor(g["p50"] / 1000 + 0.5)) * 1000 != F["components"]["p50_mwh"]:
        fails.append("P50 %.1f" % g["p50"])
    if int(math.floor(g["sd"] / 100 + 0.5)) * 100 != F["components"]["sd_mwh"]:
        fails.append("SD %.1f" % g["sd"])
    if abs(g["p90"] - F["unrounded"]["p90"]) > 0.05:
        fails.append("P90 %.2f against %.2f" % (g["p90"], F["unrounded"]["p90"]))
    for tag, v in a.items():
        if "%.2f" % v != F["ask_a_availability_pct"][tag]:
            fails.append("availability %s %.4f" % (tag, v))
    for y, v in b.items():
        if rnd(v) != F["ask_b_over_under_mwh"][str(y)]:
            fails.append("over or under %d %.2f" % (y, v))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(golden_dir, "hedge_volume_2027.xlsx"), data_only=True)
    if wb["Volume 2027"]["B4"].value != g["volume"]:
        fails.append("workbook volume")
    if fails:
        raise SystemExit("verify failed: " + "; ".join(fails))
    print("verify: volume %d MWh (P90 %.1f), P50 %.1f, SD %.1f, wear %.4f, gain %.4f, base ratio %.4f; 16 availabilities "
          "and 10 over-or-unders agree with figures.json and the workbook" % (g["volume"], g["p90"], g["p50"], g["sd"],
                                                                            g["wear"], g["gain"], g["pr"]))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    t = os.path.join(os.path.dirname(here), "target")
    main(t, os.path.join(os.path.dirname(here), "golden"))
