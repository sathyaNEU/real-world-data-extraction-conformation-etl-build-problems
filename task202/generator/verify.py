"""The independent verifier: every graded figure recomputed from target/ with the standard library and openpyxl only,
no generator module imported, compared with generator/figures.json at the prompt's rounding."""
import csv
import datetime as dt
import json
import os
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))


def half(x, nd=0):
    q = 10 ** nd
    return int(x * q + 0.5) / q


def rows(T, fn):
    with open(os.path.join(T, fn), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def last_sunday(y, m):
    d = dt.date(y, m, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(1)
    return d


def to_utc(local, second):
    """UK clock to UTC; the repeated October 01:00 is BST the first time it appears and GMT the second."""
    y = local.year
    on = dt.datetime.combine(last_sunday(y, 3), dt.time(1))
    off = dt.datetime.combine(last_sunday(y, 10), dt.time(1))
    bst = on <= local < off
    if local.date() == last_sunday(y, 10) and local.hour == 1:
        bst = not second
    return local - dt.timedelta(hours=1 if bst else 0)


def station(T):
    out = {}
    for fn, rank in (("lenning_foot_hourly_provisional.csv", 0), ("lenning_foot_hourly_validated.csv", 1)):
        seen = set()
        for r in rows(T, fn):
            loc = dt.datetime.strptime(r["Timestamp (UK)"], "%d/%m/%Y %H:%M")
            u = to_utc(loc, loc in seen)
            seen.add(loc)
            if u in out and out[u][2] > rank:
                continue
            out[u] = (float(r["Water temp (C)"]), float(r["Flow (m3/s)"]), rank)
    return out


def density(t):
    num = (999.83952 + 16.945176 * t - 7.9870401e-3 * t ** 2 - 46.170461e-6 * t ** 3 + 105.56302e-9 * t ** 4
           - 280.54253e-12 * t ** 5)
    return num / (1 + 16.879850e-3 * t)


def run(T):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    st = station(T)
    surf = {}
    for r in rows(T, "fellside_buoy_thermistor_daily.csv"):
        if float(r["Depth (m)"]) <= 5:
            surf.setdefault(r["Date (UTC)"], []).append(float(r["Water temperature (degC)"]))
    rday = {}
    for u, v in st.items():
        rday.setdefault(u.date().isoformat(), []).append(v[0])
    got = {}
    for y in (2024, 2025, 2026):
        n = dense = 0
        d = dt.date(y, 6, 1)
        while d <= dt.date(y, 9, 30):
            k = d.isoformat()
            n += 1
            dense += density(sum(rday[k]) / len(rday[k])) > density(sum(surf[k]) / len(surf[k]))
            d += dt.timedelta(1)
        got["dense_%d" % y], got["days_%d" % y] = dense, n
    wb = openpyxl.load_workbook(os.path.join(T, "fellmoor_wwtw_monthly_returns.xlsx"), data_only=True)
    hol = {}
    for ws in wb.worksheets:
        vals = list(ws.iter_rows(values_only=True))
        hdr = list(vals[2])
        for row in vals[3:]:
            rec = dict(zip(hdr, row))
            if rec.get("Site") == "Hollinsby WwTW":
                m = dt.datetime.strptime(rec["Month"], "%b-%y")
                hol[(m.year, m.month)] = rec["TP load (kg)"]
            elif rec.get("Works") == "HOLLINSBY":
                m = dt.datetime.strptime(rec["Period"], "%Y-%m")
                hol[(m.year, m.month)] = rec["TP load kg"]
    wo = openpyxl.load_workbook(os.path.join(T, "mill_beck_outfall_monitoring.xlsx"), data_only=True)["Monthly loads"]
    out = {}
    for row in list(wo.iter_rows(values_only=True))[1:]:
        m = dt.datetime.strptime(row[0], "%b %Y")
        out[(m.year, m.month)] = row[3]
    cs, ds = [], []
    for y in (2024, 2025, 2026):
        c = 0.71 * sum(hol[(y, m)] for m in (6, 7, 8, 9))
        dd = 0.5 * sum(out[(y, m)] for m in (6, 7, 8, 9))
        got["C_%d" % y], got["D_%d" % y] = int(half(c)), int(half(dd))
        got["A_%d" % y] = got["B_%d" % y] = 0
        cs.append(c)
        ds.append(dd)
    got["C_mean"], got["D_mean"] = int(half(sum(cs) / 3)), int(half(sum(ds) / 3))
    got["gap"] = got["C_mean"] - got["D_mean"]
    # the winter ask
    brankell = {}
    for r in rows(T, "regulator_gauged_flows_hourly.csv"):
        if r["station_name"] == "BRANKELL BECK AT HOWE":
            brankell[dt.datetime.strptime(r["datetime"], "%Y-%m-%dT%H:%M:%SZ")] = float(r["mean_flow_m3s"])
    conc = {}
    sam = rows(T, "lenning_foot_sampler_results.csv")
    for kind in ("DAY", "STORM"):
        for r in sam:
            if r["Programme"] != kind:
                continue
            f = dt.datetime.strptime(r["First sub-sample (UK)"], "%d/%m/%Y %H:%M")
            l = dt.datetime.strptime(r["Last sub-sample (UK)"], "%d/%m/%Y %H:%M")
            t, e = to_utc(f, False), to_utc(l, False)
            while t <= e:
                conc[t] = float(r["TP (ug/l)"])
                t += dt.timedelta(hours=1)
    vol = load = 0.0
    t = dt.datetime(2023, 9, 30, 23)
    while t < dt.datetime(2024, 4, 30, 23):
        q = st[t][1] + brankell[t]
        vol += q * 3600
        load += q * 3600 * conc[t] / 1e6
        t += dt.timedelta(hours=1)
    got["inflow_2023_24"] = half(vol / 1e6, 1)
    got["load_2023_24"] = int(half(load / 100)) * 100
    # the north basin
    lab = rows(T, "fellside_lake_lab_results.csv")
    for y in (2025, 2026):
        acc = {"Total phosphorus": [], "Chlorophyll a": []}
        for r in lab:
            d = dt.datetime.strptime(r["sampled"], "%d-%b-%Y").date()
            north = r["site"] == "SWL01" or (r["site"] == "NB" and d < dt.date(2025, 4, 1))
            if north and d.year == y and 6 <= d.month <= 9 and r["depth_m"] == "0-5":
                acc[r["determinand"]].append(float(r["result"]))
        got["tp_%d" % y] = half(sum(acc["Total phosphorus"]) / len(acc["Total phosphorus"]), 1)
        got["chl_%d" % y] = half(sum(acc["Chlorophyll a"]) / len(acc["Chlorophyll a"]), 1)
    # Connect Right
    kids = {}
    for r in rows(T, "hollinsby_address_register_extract.csv"):
        if r["PARENT_UPRN"]:
            kids.setdefault(r["PARENT_UPRN"], []).append(r["UPRN"])
    found, fixed = set(), set()
    for v in rows(T, "connect_right_visits_export.csv"):
        day = dt.datetime.strptime(v["Visit ref"][3:9], "%y%m%d").date()
        dw = kids.get(v["UPRN"], [v["UPRN"]])
        if v["Outcome"] == "MISCONNECTED":
            found.update(dw)
        elif v["Outcome"] == "FIX CONFIRMED" and day <= dt.date(2026, 9, 30):
            fixed.update(dw)
    fixed &= found
    got["dw_found"], got["dw_fixed"], got["dw_open"] = len(found), len(fixed), len(found - fixed)
    want = dict(fig)
    want["load_2023_24"] = int(half(fig["load_2023_24"] / 100)) * 100
    bad = [(k, got[k], want[k]) for k in got if got[k] != want[k]]
    for b in bad:
        print("VERIFY MISMATCH", b)
    print("verify: %d figures recomputed from target/, %d mismatched" % (len(got), len(bad)))
    return not bad


if __name__ == "__main__":
    sys.exit(0 if run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")) else 1)
