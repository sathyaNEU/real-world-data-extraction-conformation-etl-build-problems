"""task231 architecture 2: the independent verifier. Reads every shipped format back with its own code (pandas for
the CSVs, openpyxl for the workbooks, the PDFs' text, the email), recomputes the golden figures without the
generator's analysis module, and compares them with the golden workbook, the memo and submission.md.

    python3 task231/generator/verify.py
"""
import datetime as dt
import email
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from docx import Document
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
START = pd.Timestamp("2026-10-01 06:00")
NH = 5088
FAIL = []


def ok(label, cond, detail=""):
    print("%-4s %-4s %s" % (label, "ok" if cond else "FAIL", detail))
    if not cond:
        FAIL.append(label)


# ---- the register ----
wb = load_workbook(os.path.join(T, "sdhd_rwis_site_register.xlsx"), read_only=True)
sites = pd.DataFrame(list(wb["Sites"].iter_rows(values_only=True))[1:],
                     columns=[c for c in next(wb["Sites"].iter_rows(values_only=True))])
sites = sites.sort_values("Site code").reset_index(drop=True)
n = len(sites)
code = list(sites["Site code"])
z = sites["Elevation (m)"].to_numpy(float)
lat = np.radians(sites["Latitude"].to_numpy(float))
lon = np.radians(sites["Longitude"].to_numpy(float))
dlat = lat[:, None] - lat[None, :]
dlon = lon[:, None] - lon[None, :]
D = 2 * 6371.0 * np.arcsin(np.sqrt(np.sin(dlat / 2) ** 2 + np.cos(lat[:, None]) * np.cos(lat[None, :]) *
                                   np.sin(dlon / 2) ** 2))
rpu = dict(zip(sites["RPU"], range(n)))
ok("V0", n >= 20 and abs(z.max() - 2422) < 1, "register read: %d sites" % n)

# ---- the feed and the QC log ----
fd = pd.read_csv(os.path.join(T, "sdhd_ess_atmospheric_2026_27.csv"))
fd["h"] = ((pd.to_datetime(fd["obs_time_utc"]).dt.tz_localize(None) - START) / pd.Timedelta(hours=1)).astype(int) - 1
fd["i"] = fd["rpu_id"].map(rpu)
fd = fd.drop_duplicates(["i", "h"])
val = np.full((n, NH), np.nan)
val[fd["i"].to_numpy(), fd["h"].to_numpy()] = fd["essAirTemperature"].to_numpy() / 10.0
qc = pd.read_csv(os.path.join(T, "quillan_qc_withheld_log_2026_27.csv"))
qa = qc[qc["parameter"] == "air_temperature"].copy()
qa["h"] = ((pd.to_datetime(qa["obs_time"]).dt.tz_localize(None) - START) / pd.Timedelta(hours=1)).astype(int) - 1
qa["i"] = qa["site_code"].map(dict(zip(code, range(n))))
flag = np.zeros((n, NH), bool)
flag[qa["i"].to_numpy(), qa["h"].to_numpy()] = True
sp = qa[qa["test"] == "spatial"].drop_duplicates(["i", "h"])
wh = np.zeros((n, NH), bool)
wh[sp["i"].to_numpy(), sp["h"].to_numpy()] = True

# ---- local night (MDT to 1 Nov 08:00 UTC, MST to 14 Mar 09:00 UTC) ----
utc = START + pd.to_timedelta(np.arange(NH), unit="h")
off = np.where((utc >= pd.Timestamp("2026-11-01 08:00")) & (utc < pd.Timestamp("2027-03-14 09:00")), 7, 6)
lh = ((utc - pd.to_timedelta(off, unit="h")).hour).to_numpy()
night = (lh >= 18) | (lh < 9)

# ---- the free-atmosphere line, robustly, then the stations sharing a cold pool ----
res = np.full_like(val, np.nan)
for h in range(NH):
    okh = ~np.isnan(val[:, h])
    keep = okh.copy()
    for _ in range(3):
        b1, b0 = np.polyfit(z[keep], val[keep, h], 1)
        r = val[:, h] - (b0 + b1 * z)
        keep = okh & (r > -1.5)
    res[:, h] = r
passed = ~np.isnan(res) & ~flag
mean_res = np.array([res[i, night & passed[i]].mean() for i in range(n)])
mates = {}
for i in range(n):
    mates[i] = []
    for j in range(n):
        if i == j or abs(z[i] - z[j]) > 80 or D[i, j] > 25 or mean_res[i] >= -0.5 or mean_res[j] >= -0.5:
            continue
        m = night & passed[i] & passed[j]
        if np.corrcoef(res[i, m], res[j, m])[0, 1] > 0.8:
            mates[i].append(j)
pooled = {i for i in range(n) if mates[i]}
free = [j for j in range(n) if j not in pooled]

fr = np.zeros(n, int)
for i in range(n):
    for h in np.where(wh[i])[0]:
        if mates[i]:
            ref = np.nanmedian(val[mates[i], h])
        else:
            nb = [j for j in free if j != i and D[i, j] <= 50]
            ref = np.nanmedian(val[nb, h] + 0.0065 * (z[nb] - z[i]))
        fr[i] += abs(val[i, h] - ref) <= 2.0
share = fr / NH * 100
retune = [code[i] for i in range(n) if share[i] > 2.0]

# ---- the golden workbook ----
gb = load_workbook(os.path.join(G, "rwis_spatial_check_review_2027.xlsx"), read_only=True)
rows = [r for r in list(gb["Spatial test review"].iter_rows(values_only=True))[1:] if r[0] and r[0].startswith("SD-")]
gw = {r[0]: r for r in rows}
ok("V1", all(gw[c][4] == fr[k] for k, c in enumerate(code)), "false-rejection hours, every station")
ok("V2", all(gw[c][5] == int(np.floor(share[k] + 0.5 + 1e-9)) for k, c in enumerate(code)),
   "whole-per-cent shares, every station")
ok("V3", sorted(c for c in code if gw[c][6] == "Yes") == sorted(retune), "re-tune list %s" % retune)
ok("V4", all(gw[c][3] == wh[k].sum() for k, c in enumerate(code)), "withheld hours, every station")

# ---- Schedule B: unavailable hours ----
mw = load_workbook(os.path.join(T, "sdhd_cellular_modem_register.xlsx"), read_only=True)
modem = {str(r[0]): code.index(r[2]) for r in list(mw["Modems"].iter_rows(values_only=True))[1:] if r[2]}
ms = pd.read_csv(os.path.join(T, "sdhd_central_server_message_log_2026_27.csv"), dtype={"modem_imei": str})
tz = ms["server_received"].str[-3:].map({"MDT": 6, "MST": 7})
ms["rec"] = pd.to_datetime(ms["server_received"].str[:-4]) + pd.to_timedelta(tz, unit="h")
ms["a"] = ((pd.to_datetime(ms["first_obs_utc"]).dt.tz_localize(None) - START) / pd.Timedelta(hours=1)).astype(int) - 1
ms["b"] = ((pd.to_datetime(ms["last_obs_utc"]).dt.tz_localize(None) - START) / pd.Timedelta(hours=1)).astype(int) - 1
ms["i"] = ms["modem_imei"].map(modem)
first = np.full((n, NH), np.inf)


def take(i, rec, a, b):
    for h in range(a, b + 1):
        lag = (rec - (START + pd.Timedelta(hours=h + 1))) / pd.Timedelta(minutes=1)
        first[i, h] = min(first[i, h], lag)


for r in ms[ms["i"].notna()].itertuples():
    take(int(r.i), r.rec, r.a, r.b)
for im, grp in ms[ms["i"].isna()].groupby("modem_imei"):
    grp = grp.sort_values("rec")
    spell = (grp["rec"].diff() > pd.Timedelta(hours=48)).cumsum()
    for _, sp in grp.groupby(spell):
        hs = sorted({h for r in sp.itertuples() for h in range(r.a, r.b + 1)})
        cand = [i for i in range(n) if all(not np.isnan(val[i, h]) and np.isinf(first[i, h]) for h in hs)]
        ok("V5", len(cand) == 1, "modem %s with no site, %s to %s, serves %s" % (
            im, sp["rec"].iloc[0].date(), sp["rec"].iloc[-1].date(), [code[c] for c in cand]))
        for r in sp.itertuples():
            take(cand[0], r.rec, r.a, r.b)
po = pd.read_csv(os.path.join(T, "sdhd_rwis_planned_outage_notices_2026_27.csv"))
excl = np.zeros((n, NH), bool)
for r in po.itertuples():
    s_ = pd.Timestamp(r.starts[:-4]) + pd.Timedelta(hours={"MDT": 6, "MST": 7}[r.starts[-3:]])
    e_ = pd.Timestamp(r.ends[:-4]) + pd.Timedelta(hours={"MDT": 6, "MST": 7}[r.ends[-3:]])
    excl[code.index(r.site_code), int((s_ - START) / pd.Timedelta(hours=1)):int((e_ - START) / pd.Timedelta(hours=1))] = True
avail = (first <= 20) & ~excl
unav = NH - avail.sum(1) - excl.sum(1)
sv = load_workbook(os.path.join(G, "rwis_spatial_check_review_2027.xlsx"), read_only=True)["Service and pavement"]
srows = {r[0]: r for r in list(sv.iter_rows(values_only=True))[1:] if r[0]}
sec_of = dict(zip(code, sites["Maintenance section"]))
secs = sorted(set(sec_of.values()))


def bysec(v):
    return {x: int(sum(v[k] for k, c in enumerate(code) if sec_of[c] == x)) for x in secs}


un_s = bysec(unav)
ok("V6", all(srows[x][2] == un_s[x] for x in secs) and srows["Network"][2] == int(unav.sum()),
   "unavailable station-hours by section and network %s" % un_s)

# ---- pavement: freezing and ice hours ----
ps = pd.DataFrame(list(wb["Pavement sensors"].iter_rows(values_only=True))[1:],
                  columns=list(next(wb["Pavement sensors"].iter_rows(values_only=True))))
mdl = dict(zip(ps["Sensor serial"], ps["Model"]))
lane = {(r["RPU"], int(r["Port"])): r["Lane"] for _, r in ps.iterrows()}
fwv = {r[0]: pd.Timestamp(r[2]) for r in list(wb["Firmware"].iter_rows(values_only=True))[1:]}
cds = {}
for tab, c, name in list(wb["Status codes"].iter_rows(values_only=True))[1:]:
    cds.setdefault("new" if "4.1" in tab else "old", {})[int(c)] = name
pv = pd.read_csv(os.path.join(T, "sdhd_pavement_sensor_readings_2026_27.csv"), dtype={"surface_temperature": str}).drop_duplicates()
pv = pv[[lane[(a, b)] == "travel lane" for a, b in zip(pv["rpu_id"], pv["port"])]]
pv["utc"] = pd.to_datetime(pv["obs_time"].str[:-4]) + pd.to_timedelta(pv["obs_time"].str[-3:].map(
    {"MDT": 6, "MST": 7}), unit="h")
pv["h"] = ((pv["utc"] - START) / pd.Timedelta(hours=1)).astype(int) - 1
loc = pv["utc"] - pd.to_timedelta(np.where((pv["utc"] >= pd.Timestamp("2026-11-01 08:00")) &
                                           (pv["utc"] < pd.Timestamp("2027-03-14 09:00")), 7, 6), unit="h")
model = pv["sensor_serial"].map(lambda x: mdl.get(x) or {"IR": "IRS-31", "SC": "SCAN-16"}[x[:2]])
tempf = np.where(model == "IRS-31", pv["surface_temperature"].astype(float) / 10 * 9 / 5 + 32, pv["surface_temperature"].astype(float))
newtab = (model == "IRS-31") & np.array([s_ in fwv and l_ >= fwv[s_] for s_, l_ in zip(pv["sensor_serial"], loc)])
status = [cds["new" if nt else "old"][c] for nt, c in zip(newtab, pv["surface_status_code"])]
pv["frz"] = tempf <= 32.0 + 1e-9
pv["ice"] = [s_ in ("ice warning", "ice watch") for s_ in status]
pv["i"] = pv["rpu_id"].map(rpu)
agg = pv.groupby(["i", "h"])[["frz", "ice"]].any().groupby("i").sum()
fz_s = bysec([agg.loc[k, "frz"] for k in range(n)])
ic_s = bysec([agg.loc[k, "ice"] for k in range(n)])
ok("V7", all(srows[x][4] == fz_s[x] for x in secs) and srows["Network"][4] == sum(fz_s.values()),
   "freezing station-hours by section %s" % fz_s)
ok("V8", all(srows[x][5] == ic_s[x] for x in secs) and srows["Network"][5] == sum(ic_s.values()),
   "ice station-hours by section %s" % ic_s)

# ---- the memo and submission.md say the same ----
memo = "\n".join(p.text for p in Document(os.path.join(G, "spatial_check_retune_memo_2027.docx")).paragraphs)
names = dict(zip(sites["Site code"], sites["Site name"]))
ok("V9", all(names[c] in memo.split("\n")[5] if len(memo.split("\n")) > 5 else False for c in retune) or
   all(names[c] in memo for c in retune), "the memo names every re-tuned station")
sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
line = [l_ for l_ in sub.splitlines() if l_.strip().startswith("- SD-")][0]
pairs = dict(re.findall(r"(SD-\d{3}) (\d+)", line))
ok("V10", all(pairs[c] == str(int(np.floor(share[k] + 0.5 + 1e-9))) for k, c in enumerate(code)),
   "submission.md shares")
un_line = [l_ for l_ in sub.splitlines() if l_.startswith("2. Unavailable station-hours")][0]
ok("V11", all(("%s %s" % (x, format(un_s[x], ","))) in un_line for x in secs), "submission.md unavailable hours")
std = open(os.path.join(T, "sdhd_road_weather_data_quality_standard_rev2.pdf"), "rb").read()
ok("V12", std.startswith(b"%PDF") and b"D:2026082" in std, "the standard is a PDF with its own stamps")
em = email.message_from_bytes(open(os.path.join(T, "rwis_winter_review_request.eml"), "rb").read())
ok("V13", em["Date"] and "2027" in em["Date"], "the request is dated %s" % em["Date"])
print("verify: %d failures" % len(FAIL))
sys.exit(1 if FAIL else 0)
