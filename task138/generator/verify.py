"""Independent verifier for task138: reads only target/ (csv module, its own XLSX and PDF readers, no pandas, no
generator module) and recomputes every graded figure, then compares with generator/figures.json.

    python3 task138/generator/verify.py
"""
import base64
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
import zlib
from xml.etree import ElementTree as ET

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


# ----------------------------------------------------------------- readers
def pdf_strings(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[:-2])
            raw = zlib.decompress(raw)
        except Exception:
            continue
        for s in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", raw):
            out.append(s.replace(rb"\(", b"(").replace(rb"\)", b")").decode("latin-1"))
    return re.sub(r"\s+", " ", " ".join(out))


NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def xlsx_sheets(path):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for sh in wb.find("m:sheets", NS):
        rid = sh.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        x = ET.fromstring(z.read("xl/" + target[rid].lstrip("/").replace("xl/", "")))
        rows = []
        for r in x.iter("{%s}row" % NS["m"]):
            vals = {}
            for cl in r.findall("m:c", NS):
                col = re.match(r"[A-Z]+", cl.get("r")).group(0)
                v = cl.find("m:v", NS)
                t = cl.get("t")
                if t == "s":
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(e.text or "" for e in cl.iter("{%s}t" % NS["m"]))
                elif v is None:
                    val = None
                else:
                    val = float(v.text)
                vals[col] = val
            rows.append(vals)
        out[sh.get("name")] = rows
    return out


def read_csv(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def parse(s, fmt):
    return dt.datetime.strptime(s, fmt)


# ----------------------------------------------------------------- filed values
crit = pdf_strings(os.path.join(T, "BEC_distribution_planning_criteria_rev4.pdf"))
ok("PDF positive control: the criteria's own title reads back", "Distribution Planning Criteria" in crit)
m = re.search(r"Dunraith 2 x 75/100/125 MVA (\d+\.\d) Mossford Municipal Airport (\d+) F", crit)
FIRM, DESIGN = float(m.group(1)), float(m.group(2))
BLOCK = float(re.search(r"Switching block (\d\.\d) MW", crit).group(1))
THR = float(re.search(r"(\d+) F or more", crit).group(1))
ok("criteria: firm 104.0 MW, design 101 F, block 0.5 MW, line over days at 85 F or more",
   (FIRM, DESIGN, BLOCK, THR) == (104.0, 101.0, 0.5, 85.0))
ok("criteria 3.3 files the change's effect at the planning peak", "effect on the substation load at the planning peak"
   in crit)
plan = pdf_strings(os.path.join(T, "BEC_2027_operating_plan.pdf"))
ok("operating plan: CVR on every Dunraith feeder from 1 June 2027", "every Dunraith feeder from 1 June 2027" in plan)
tp = pdf_strings(os.path.join(T, "CVR_pilot_plan_Dunraith_2025.pdf"))
PILOT = re.findall(r"DUN-\d", re.search(r"Pilot feeders: (.*?)\.", tp).group(1))
COMP = ["DUN-%d" % i for i in range(1, 9) if "DUN-%d" % i not in PILOT]
ok("pilot plan: pilot feeders %s" % PILOT, PILOT == ["DUN-2", "DUN-5", "DUN-7"])
fc = xlsx_sheets(os.path.join(T, "BEC_load_forecast_2025.xlsx"))
G = [r["C"] for r in fc["Substations"] if r.get("A") == "Dunraith"][0] / 100.0
ok("XLSX positive control: the forecast's Dunraith base case reads 0.95", abs(G - 0.0095) < 1e-12)

# ----------------------------------------------------------------- loads (local hour-beginning)
load = {}
for r in read_csv("DUNRAITH_FDR_KW_2022-2023.csv"):
    t = parse(r["Date/Time"], "%m/%d/%Y %H:%M") - dt.timedelta(hours=1)
    load[t] = [float(r["DUNRAITH F%d KW" % i]) / 1000.0 for i in range(1, 9)]
newr = {}
for r in read_csv("dunraith_feeder_mw_2024-2026.csv"):
    if r["Quality"] != "Good":
        continue
    t = parse(r["TimeStamp"], "%Y-%m-%d %H:%M:%S")
    newr.setdefault(t, {})[r["TagName"].split(".")[0]] = float(r["Value"])
for t, d in newr.items():
    if len(d) == 8:
        load[t] = [d["DUN-%d" % i] for i in range(1, 9)]
ok("CSV positive control: both historian exports read, %d complete hours" % len(load), len(load) > 14000)

# ----------------------------------------------------------------- temperatures (export in LST)
tmax = {}
for r in read_csv("mossford_ap_obs_2022-2026.csv"):
    if not r["TMP_C"]:
        continue
    t = parse(r["DATE_LST"], "%Y-%m-%dT%H:%M:%S") + dt.timedelta(hours=1)
    fv = float(r["TMP_C"]) * 1.8 + 32.0
    d = t.date()
    tmax[d] = max(tmax.get(d, -999.0), fv)

# ----------------------------------------------------------------- 3.2 weather-normal peak
dmax = {}
for t, v in load.items():
    s = sum(v)
    dmax[t.date()] = max(dmax.get(t.date(), 0.0), s)
xs, ys = [], []
for d, L in dmax.items():
    if d.month in (6, 7, 8, 9) and d in tmax and tmax[d] >= THR:
        xs.append(tmax[d])
        ys.append(L)
slope, icpt = np.polyfit(np.array(xs), np.array(ys), 1)
B = icpt + slope * DESIGN

# ----------------------------------------------------------------- the pilot from the regulator log
ev = {}
for r in read_csv("VR_event_log_DUN_2025.csv"):
    if r["Event"] in ("CVR ON", "CVR OFF"):
        ev.setdefault(r["Device"].split(" ")[0], []).append((parse(r["EventTime"], "%Y-%m-%d %H:%M:%S"),
                                                             r["Event"] == "CVR ON"))


def state(f, t):
    s = False
    for when, on in sorted(ev.get(f, [])):
        if when <= t:
            s = on
    return s


p0, p1 = dt.datetime(2025, 6, 2), dt.datetime(2025, 9, 29)
on_r, off_r = [], []
for t in sorted(load):
    if not (p0 <= t < p1) or t.hour < 16 or t.hour > 20 or tmax.get(t.date(), 0) < 99:
        continue
    st = [state(f, t) and state(f, t + dt.timedelta(minutes=59, seconds=59)) for f in PILOT]
    sf = [state(f, t) or state(f, t + dt.timedelta(minutes=59, seconds=59)) for f in PILOT]
    v = load[t]
    ratio = sum(v[int(f[-1]) - 1] for f in PILOT) / sum(v[int(f[-1]) - 1] for f in COMP)
    if all(st):
        on_r.append(ratio)
    elif not any(sf):
        off_r.append(ratio)
RELIEF = 1 - (sum(on_r) / len(on_r)) / (sum(off_r) / len(off_r))

FIG = json.load(open(os.path.join(HERE, "figures.json")))
peaks, trs = [], []
for y in range(2027, 2032):
    p = B * (1 + G) ** (y - 2024) * (1 - RELIEF)
    peaks.append(int(math.floor(p + 0.5)))
    trs.append(0.0 if p <= FIRM else math.ceil(round((p - FIRM) / BLOCK, 9)) * BLOCK)
ok("weather-normal peak %.2f MW (figures %.1f)" % (B, FIG["weather_normal_2024_mw"]),
   round(B, 1) == FIG["weather_normal_2024_mw"])
ok("relief at the planning peak %.3f per cent (figures %.1f), %d CVR and %d normal hours"
   % (100 * RELIEF, FIG["relief_pct"]["golden"], len(on_r), len(off_r)),
   round(100 * RELIEF, 1) == FIG["relief_pct"]["golden"])
ok("planning peaks %s" % peaks, peaks == [FIG["call"][str(y)]["planning_peak_mw"] for y in range(2027, 2032)])
ok("transfers %s" % trs, trs == [FIG["call"][str(y)]["transfer_mw"] for y in range(2027, 2032)])

# ----------------------------------------------------------------- ask A
reg = xlsx_sheets(os.path.join(T, "DUN_transformer_register_2026-10.xlsx"))
txr = reg["Transformers"]
hdr = txr[0]
col = {v: k for k, v in hdr.items()}
mult, mset, prot = {}, {}, {}
for r in txr[1:]:
    x = r[col["XFMR_ID"]]
    mult[x] = int(r[col["METER_MULT"]])
    mset[x] = dt.datetime.strptime(r[col["METER_SET"]], "%Y-%m-%d").date()
    prot[x] = r[col["PROT_DEVICE"]]
dv = reg["Devices"]
dcol = {v: k for k, v in dv[0].items()}
kids = {}
for r in dv[1:]:
    kids.setdefault(r[dcol["UPSTREAM_DEVICE"]], []).append(r[dcol["DEVICE_ID"]])
so = pdf_strings(os.path.join(T, "SO-2026-114_Dunraith.pdf"))
old_feeder = {}
for sw, a, b in re.findall(r"(S-\d+) \((DUN-\d)\) Open Section beyond S-\d+ fed from (DUN-\d)", so):
    seen, todo = set(), [sw]
    while todo:
        n = todo.pop()
        for k in kids.get(n, []):
            seen.add(k)
            todo.append(k)
    for x, p in prot.items():
        if p in seen:
            old_feeder[x] = a
ok("switching order: three sections traced, %d transformers" % len(old_feeder), 15 <= len(old_feeder) <= 40)
energy = {}
for r in read_csv("mdms_xfmr_daily_kwh_20260601_20260930.csv"):
    x = r["XFMR_ID"]
    d = parse(r["READ_DATE"], "%m/%d/%Y").date()
    k = float(r["KWH"]) * (mult[x] if d >= mset[x] else 1)
    f = old_feeder[x] if (x in old_feeder and d < dt.date(2026, 7, 1)) else r["FEEDER"]
    energy[f] = energy.get(f, 0.0) + k
ea = {f: int(round(energy[f] / 1000.0 / 10.0)) * 10 for f in sorted(energy)}
ok("ask A feeder energy %s" % ea, ea == FIG["feeder_energy_mwh"])

# ----------------------------------------------------------------- ask B
ex = pdf_strings(os.path.join(T, "WPC_Exhibit_A_delivery_points.pdf"))
ok("Exhibit A: the two transformer recorders and the 69 kV line terminal", "41-2207 Dunraith T1, 24.9 kV low side" in ex
   and "41-2391 Dunraith 69 kV, line terminal L3" in ex)
rows = {}
for r in read_csv("MV90_DP0417_202606-202609.csv"):
    if r["RECORDER"] in ("41-2207", "41-2208"):
        rows.setdefault(r["RECORDER"], []).append((parse(r["INTERVAL_END_UTC"], "%Y-%m-%d %H:%M"), float(r["VALUE"])))
q = {}
for rec, lst in rows.items():
    seen, shift = set(), False
    for stamp, v in lst:
        if stamp in seen:
            shift = True
        seen.add(stamp)
        end = stamp + (dt.timedelta(minutes=15) if shift else dt.timedelta(0))
        start_local = end - dt.timedelta(hours=5) - dt.timedelta(minutes=15)
        q[start_local] = q.get(start_local, 0.0) + v
daily = {}
for t, v in q.items():
    daily[t.date()] = max(daily.get(t.date(), 0.0), v * 4.0 / 1000.0)
t26 = sorted(((v, d) for d, v in tmax.items() if d.year == 2026 and 6 <= d.month <= 9), reverse=True)
top = [d for _, d in t26[:10]]
pb = {d.strftime("%Y-%m-%d"): round(daily[d], 1) for d in top}
ok("ask B hottest days and peaks %s" % pb, pb == {k: v["peak_mw"] for k, v in FIG["hot_days"].items()})
ok("ask B: the eleventh day sits %.2f F below the tenth" % (t26[9][0] - t26[10][0]), t26[9][0] - t26[10][0] > 0.3)

bad = [o for o in OUT if not o[1]]
for label, good, detail in OUT:
    print("%s    %s" % ("OK  " if good else "FAIL", label))
print("verify: %d checks, %d failed" % (len(OUT), len(bad)))
sys.exit(1 if bad else 0)
