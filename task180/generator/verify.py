"""Independent recomputation of every graded figure from target/ alone, on its own code path (pandas, no import
of analysis.py, world.py or params.py), compared with figures.json. Exit 1 on any difference."""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
FIGS = json.load(open(os.path.join(HERE, "figures.json")))
fails = []


def say(label, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, (" | " + detail) if detail else ""))
    if not ok:
        fails.append(label)


# ----------------------------------------------------------------- gas bars
pos = pd.read_csv(os.path.join(T, "pos_fuel_sales_by_hose_2024_2026.csv"))
pos = pos.sort_values("exported_at").drop_duplicates(["site", "business_date", "fp", "grade"], keep="last")
pos["prod"] = pos["grade"].map({"REG 87": "R", "PREM 91": "P", "DSL": "D"})
pos["day"] = pd.to_datetime(pos["business_date"])
atg = pd.read_csv(os.path.join(T, "atg_shift_close_inventory_2024_2026.csv"))
atg["prod"] = atg["product"].map({"UNLEADED": "R", "PREMIUM": "P", "DIESEL": "D"})
atg["day"] = pd.to_datetime(atg["read_at"].str[:10])
bol = pd.read_csv(os.path.join(T, "bills_of_lading_2024_2026.csv"), keep_default_na=False)
gb = bol[bol["consignee"].str.startswith("GB-") & (bol["delivered_at"] != "")].copy()
gb["site"] = gb["consignee"].str.split().str[0]
gb["prod"] = gb["product"].map({"Regular Unleaded": "R", "Premium Unleaded": "P", "ULS Diesel": "D"})
wall = pd.to_datetime(gb["delivered_at"].str[:16])
gb["day"] = (wall - pd.Timedelta(hours=5)).dt.normalize()
cfg = json.load(open(os.path.join(T, "forecourt_controller_config_2027-01-05.json")))
import openpyxl  # noqa: E402
reg = openpyxl.load_workbook(os.path.join(T, "tpc_site_tank_register.xlsx"), data_only=True)
serial_no = {r[2]: r[1] for r in list(reg["Dispensers"].iter_rows(values_only=True))[1:]}
prov = {r[0]: r[2] for r in list(reg["Tanks"].iter_rows(values_only=True))[1:]}
fp_disp = {(s["site"], f["fp"]): serial_no[f["dispenser_serial"]] for s in cfg["sites"] for f in s["fuelling_points"]}
wo = pd.read_excel(os.path.join(T, "service_work_orders_2024_2026.xlsx"), sheet_name="Work orders")
wo["site"] = wo["Site"].str.split().str[0]
wo["day"] = pd.to_datetime(wo["Date"])
resets = []                         # (site, fp, prod, day)
for _, r in wo.iterrows():
    fps = sorted(fp for (s, fp) in fp_disp if s == r["site"])
    txt = r["Work done"]
    if r["Category"] == "Meter calibration":
        if "all meters" in txt or "all disps" in txt:
            disps = {fp_disp[(r["site"], fp)] for fp in fps}
        else:
            m = re.search(r"D(\d+)-D(\d+)", txt)
            disps = set(range(int(m.group(1)), int(m.group(2)) + 1)) if m else set()
            m = re.search(r"dispensers ([\d, ]+) \(", txt)
            if m:
                disps = {int(x) for x in m.group(1).split(",")}
        for fp in fps:
            if fp_disp[(r["site"], fp)] in disps:
                resets += [(r["site"], fp, p, r["day"]) for p in "RPD"]
    elif r["Category"] == "Dispenser replacement":
        d = int(re.search(r"dispenser (\d+)", txt).group(1))
        resets += [(r["site"], fp, p, r["day"]) for fp in fps if fp_disp[(r["site"], fp)] == d for p in "RPD"]
    elif r["Category"] == "Meter replacement":
        m = re.search(r"FP ?(\d+) (REG 87|PREM 91|DSL)", txt)
        resets.append((r["site"], int(m.group(1)), {"REG 87": "R", "PREM 91": "P", "DSL": "D"}[m.group(2)], r["day"]))
rs = pd.DataFrame(resets, columns=["site", "fp", "prod", "day"]).drop_duplicates()

# litres since the hose's last reset, at the start of each day: cumulative volume minus the cumulative volume
# at the reset, by an as-of merge
pos = pos.sort_values(["site", "fp", "prod", "day"])
pos["cum_before"] = pos.groupby(["site", "fp", "prod"])["volume_l"].cumsum() - pos["volume_l"]
rs = rs.sort_values("day")
merged = pd.merge_asof(pos.sort_values("day"), rs.rename(columns={"day": "reset_day"}), left_on="day",
                       right_on="reset_day", by=["site", "fp", "prod"], direction="backward")
base = pos[["site", "fp", "prod", "day", "cum_before"]].rename(columns={"day": "reset_day", "cum_before": "cum_at_reset"})
merged = merged.merge(base, on=["site", "fp", "prod", "reset_day"], how="left")
merged["L"] = merged["cum_before"] - merged["cum_at_reset"]
merged["Z"] = merged["volume_l"] * merged["L"] / 2e9
merged["q"] = merged["day"].dt.year * 10 + (merged["day"].dt.month - 1) // 3 + 1
tq = merged.groupby(["site", "prod", "q"]).agg(S=("volume_l", "sum"), X=("Z", "sum"),
                                               unknown=("L", lambda s: s.isna().any())).reset_index()
rec = gb.groupby(["site", "prod", "day"])["net_l_15c"].sum().reset_index()
rec["q"] = rec["day"].dt.year * 10 + (rec["day"].dt.month - 1) // 3 + 1
recq = rec.groupby(["site", "prod", "q"])["net_l_15c"].sum()
close = atg.set_index(["site", "prod", "day"])["net_volume_l"]


def qstart(q):
    y, n = divmod(q, 10)
    return pd.Timestamp(dt.date(y, 3 * (n - 1) + 1, 1))


def qend(q):
    y, n = divmod(q, 10)
    return pd.Timestamp(dt.date(y + (n == 4), (3 * n) % 12 + 1, 1))


rows = []
for _, r in tq.iterrows():
    a, b = qstart(r["q"]), qend(r["q"])
    try:
        c0, c1 = close[(r["site"], r["prod"], a)], close[(r["site"], r["prod"], b)]
    except KeyError:
        continue
    short = c0 + recq.get((r["site"], r["prod"], r["q"]), 0.0) - r["S"] - c1
    hrs = (b - a).days * 24 + ((1 if r["q"] % 10 == 4 else -1 if r["q"] % 10 == 1 else 0) if prov[r["site"]] == "MB" else 0)
    rows.append(dict(site=r["site"], prod=r["prod"], q=r["q"], short=short, X=np.nan if r["unknown"] else r["X"], hrs=hrs))
Q = pd.DataFrame(rows)
fit = Q[(Q["q"] <= 20263) & Q["X"].notna()]
k = float((fit["X"] * fit["short"]).sum() / (fit["X"] ** 2).sum())
q4 = Q[Q["q"] == 20264].copy()
q4["loss"] = (q4["short"] - k * q4["X"]) / q4["hrs"]
names = {"R": "regular", "P": "premium", "D": "diesel"}
got = sorted("%s %s" % (r.site, names[r.prod]) for r in q4.itertuples() if r.loss > 0.75)
say("main: the designated set", got == FIGS["designated"], str(got))
say("main: the drift rate", abs(k - FIGS["drift_rate_ml_per_20l_per_100k"]) < 0.0005, "%.4f" % k)
for r in q4.itertuples():
    key = "%s %s" % (r.site, names[r.prod])
    if key in FIGS["designated"]:
        say("main: %s loss %.1f" % (key, FIGS["loss_lph"][key]), round(r.loss, 1) == FIGS["loss_lph"][key] and
            abs(r.loss - FIGS["loss_lph_exact"][key]) < 1e-3, "%.4f" % r.loss)

# ----------------------------------------------------------------- cardlocks
cl = bol[bol["consignee"].str.startswith("CL-")].copy()
cl["site"] = cl["consignee"].str.split().str[0]
cl["prod"] = np.where(cl["product"] == "ULS Diesel", "D", "R")
lt = cl["loaded_at"].str[:16]
cl["loaded"] = pd.to_datetime(lt) - pd.to_timedelta(np.where(cl["loaded_at"].str.endswith("CDT"), 1, 0), unit="h")
rep = pd.read_csv(os.path.join(T, "cardlock_gauge_delivery_reports_q4_2026.csv"))
rep = rep.drop_duplicates(["site", "tank", "delivery_no"])
rep["prod"] = np.where(rep["product"] == "DIESEL", "D", "R")
rep["start"] = pd.to_datetime(rep["start_cst"])
rep["end"] = pd.to_datetime(rep["end_cst"])
hr = pd.read_csv(os.path.join(T, "cardlock_gauge_hourly_inventory_q4_2026.csv"))
hr["prod"] = np.where(hr["product"] == "DIESEL", "D", "R")
hr["t"] = pd.to_datetime(hr["read_cst"])
tx = pd.read_csv(os.path.join(T, "cardlock_transactions_q4_2026.csv"))
tx["prod"] = np.where(tx["product"] == "DIESEL", "D", "R")
tx["s"] = pd.to_datetime(tx["started_utc"].str[:19]) - pd.Timedelta(hours=6)
tx["e"] = pd.to_datetime(tx["ended_utc"].str[:19]) - pd.Timedelta(hours=6)
TX = {k_: g.sort_values("s") for k_, g in tx.groupby(["site", "prod"])}
HR = {k_: g.set_index("t")["net_volume_l"].sort_index() for k_, g in hr.groupby(["site", "prod"])}


def drawn(site, prod, a, b):
    g = TX[(site, prod)]
    return float(g.loc[(g["e"] <= b) & (g["s"] >= a), "litres"].sum())


q0, q1 = pd.Timestamp("2026-10-01"), pd.Timestamp("2027-01-01")
out = []
taken = set()
for r in rep.sort_values("start").itertuples():
    c = cl[(cl["site"] == r.site) & (cl["prod"] == r.prod) & (cl["loaded"] < r.start) &
           (cl["loaded"] > r.start - pd.Timedelta(hours=12)) & (~cl["bol_no"].isin(taken))]
    if c.empty:
        continue
    b = c.sort_values("loaded").iloc[-1]
    taken.add(b["bol_no"])
    if q0 <= r.start < q1:
        out.append((b["carrier"], r.site, r.start.month, b["net_l_15c"] - r.increase_net_l - drawn(r.site, r.prod, r.start, r.end)))
for b in cl[(cl["loaded"] >= q0 - pd.Timedelta(hours=12)) & (cl["loaded"] < q1) & ~cl["bol_no"].isin(taken)].itertuples():
    s = HR[(b.site, b.prod)]
    s = s[(s.index >= b.loaded - pd.Timedelta(hours=1)) & (s.index <= b.loaded + pd.Timedelta(hours=16))]
    ts = list(s.index)
    rise = [(t0, t1) for t0, t1 in zip(ts, ts[1:]) if s[t1] - s[t0] + drawn(b.site, b.prod, t0, t1) > 500]
    if not rise:
        continue
    a, z = rise[0]
    for t0, t1 in rise[1:]:
        if t0 == z:
            z = t1
    when = a + (z - a) / 2
    if q0 <= when < q1:
        out.append((b.carrier, b.site, when.month, b.net_l_15c - (s[z] - s[a] + drawn(b.site, b.prod, a, z))))
D = pd.DataFrame(out, columns=["carrier", "site", "month", "short"])
byc = D.groupby(["carrier", "month"])["short"].sum()
bys = D.groupby(["site", "month"])["short"].sum()
r10 = lambda x: int(np.floor(x / 10.0 + 0.5)) * 10
for kk, v in FIGS["cardlock_short_by_carrier"].items():
    c, m = kk.split("|")
    say("ask: %s month %s" % (c, m), r10(byc[(c, int(m))]) == v, "%.2f" % byc[(c, int(m))])
for kk, v in FIGS["cardlock_short_by_site"].items():
    s_, m = kk.split("|")
    say("ask: %s month %s" % (s_, m), r10(bys[(s_, int(m))]) == v, "%.2f" % bys[(s_, int(m))])
print("\n%d failures" % len(fails))
sys.exit(1 if fails else 0)
