"""task482's independent verifier: reads only the shipped bundle (target/), the golden deliverables and
generator/figures.json, recomputes every graded figure with its own code (pandas, no generator module), and compares.

    python3 task482/generator/verify.py
"""
import json
import os
import re
import subprocess
import sys
import warnings
from collections import defaultdict

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
FAILS = []


def say(name, ok):
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        FAILS.append(name)


def half_up(x):
    return int(np.floor(abs(x) + 0.5)) * (1 if x >= 0 else -1)


def utc_minutes(ts):
    """pandas timestamps (UTC) to minutes from 2026-01-01T00:00Z"""
    return ((ts - pd.Timestamp("2026-01-01", tz="UTC")).dt.total_seconds() // 60).astype(np.int64).values


def lag(u, x, tau):
    """the vaccine's estimate at each record's time stamp: each record holds over the interval it opens"""
    from itertools import accumulate
    c = np.exp(-np.diff(u) / tau)
    steps = zip(c.tolist(), ((1 - c) * x[:-1]).tolist())
    return np.array(list(accumulate(steps, lambda v, p: p[0] * v + p[1], initial=float(x[0]))))


def main():
    stores = pd.read_excel(os.path.join(T, "penwick_store_list_2027-01.xlsx"))
    roster = pd.read_excel(os.path.join(T, "refrigerator_monitoring_roster_2026.xlsx"))
    ser2store = dict(zip(roster["Serial or sensor id"], roster["Store"]))
    make = {r["Store"]: r["Make"] for _, r in roster.iterrows() if r["Device type"] == "Data logger"}
    # loggers
    fr = pd.read_csv(os.path.join(T, "frostline_temperature_logs_2026.csv"))
    fr_u = utc_minutes(pd.to_datetime(fr["Timestamp"], utc=True))
    kv = pd.read_csv(os.path.join(T, "kelvra_logger_export_2026.csv"), skiprows=3).drop_duplicates()
    kv_u = utc_minutes(pd.to_datetime(kv["Date"] + " " + kv["Time"], format="%m/%d/%Y %H:%M:%S").dt.tz_localize("UTC"))
    rows = []
    serial = None
    for line in open(os.path.join(T, "brumal_downloads_2026.txt"), encoding="utf-8"):
        m = re.match(r"Serial number:\s+(\S+)", line)
        if m:
            serial = m.group(1)
        elif re.match(r"\d\d/\d\d/2026\t", line):
            d, t, v = line.split("\t")
            rows.append((serial, d + " " + t, float(v)))
    pw = pd.DataFrame(rows, columns=["serial", "ts", "c"])
    pw_u = utc_minutes((pd.to_datetime(pw["ts"], format="%m/%d/%Y %H:%M") + pd.Timedelta(hours=6)).dt.tz_localize("UTC"))
    rec = pd.concat([pd.DataFrame({"store": fr["Serial"].map(ser2store), "u": fr_u, "c": fr["Temperature (C)"]}),
                     pd.DataFrame({"store": kv["Logger ID"].map(ser2store), "u": kv_u,
                                   "c": (kv["Temperature (F)"] - 32) * 5 / 9}),
                     pd.DataFrame({"store": pw["serial"].map(ser2store), "u": pw_u, "c": pw["c"]})])
    rec = rec.sort_values(["store", "u"]).drop_duplicates(["store", "u"])
    cl = pd.read_csv(os.path.join(T, "tellvane_sensor_readings_2026.csv"))
    cl["store"] = cl["sensor_id"].map(ser2store)
    cl["u"] = utc_minutes(pd.to_datetime(cl["reading_time_utc"], utc=True))
    cl = cl.sort_values(["store", "u"])
    y0, y1 = 360, 360 + 525600
    first = cl.groupby("store")["u"].min().to_dict()
    R = {no: (g["u"].values, g["c"].values) for no, g in rec.groupby("store")}
    C = {no: (g["u"].values, g["temperature_c"].values) for no, g in cl.groupby("store")}

    def sse(nos, tau):
        s = 0.0
        for no in nos:
            u, x = R[no]
            v = lag(u, x, tau)
            cu, cx = C[no]
            k = (cu >= first[no]) & (cu < u[-1] + 10)
            cu, cx = cu[k], cx[k]
            j = np.searchsorted(u, cu, side="right") - 1
            s += float(((x[j] + (v[j] - x[j]) * np.exp(-(cu - u[j]) / tau) - cx) ** 2).sum())
        return s

    taus = {}
    for mk in sorted(set(make.values())):
        nos = [no for no in first if make[no] == mk]
        a, b = 30.0, 60.0
        while b - a > 0.002:                                  # ternary search on the sum of squares
            m1, m2 = a + (b - a) / 3, b - (b - a) / 3
            if sse(nos, m1) < sse(nos, m2):
                b = m2
            else:
                a = m1
        taus[mk] = (a + b) / 2

    def count(u, y, end):
        d = np.clip(np.minimum(np.diff(np.append(u, end)), 10), 0, None)
        m = (u >= y0) & (u < y1)
        return float((d * (y > 8.0) * m).sum()) / 60.0

    hours = {}
    for no in sorted(R):
        u, x = R[no]
        v = lag(u, x, taus[make[no]])
        sw = first.get(no, y1)
        k = u < sw
        h = count(u[k], v[k], min(sw, y1))
        if no in C:
            h += count(C[no][0], C[no][1], y1)
        hours[no] = h
    f = json.load(open(os.path.join(HERE, "figures.json")))
    say("tau per make %s against figures.json %s" % ({k: round(v, 2) for k, v in taus.items()},
                                                     f["components"]["tau_minutes"]),
        all(abs(round(taus[k], 1) - f["components"]["tau_minutes"][k]) <= 0.1 for k in taus))
    say("every store's whole hours", all(half_up(hours[no]) == f["stores"][str(no)]["hours"] for no in hours))
    cov = sorted(no for no, h in hours.items() if h >= 24)
    say("the replaced stores %s" % cov, cov == f["call"]["stores"])
    nb = max((h, no) for no, h in hours.items() if h < 24)
    say("nearest below %d at %.2f, %d short" % (nb[1], nb[0], half_up(24 - nb[0])),
        nb[1] == f["components"]["nearest_below"]["store"] and half_up(24 - nb[0]) ==
        f["components"]["nearest_below"]["short_hours"])
    # ask A
    items = pd.read_excel(os.path.join(T, "vaccine_item_master_2026.xlsx"))
    dpp = dict(zip(items["NDC"], items["Doses per package"]))
    vial = dict(zip(items["NDC"], items["Package"].str.contains("vial")))
    n11 = {}
    for n in dpp:
        a, b, c = n.split("-")
        n11[a.zfill(5) + b.zfill(4) + c.zfill(2)] = n
    inv = pd.read_excel(os.path.join(T, "vaccine_physical_inventory_ye2025_ye2026.xlsx"), sheet_name=None)
    o = inv["YE 2025"].groupby("Store").agg(doses=("Doses on hand", "sum"), t=("Count closed", "max"))
    c = inv["YE 2026"].groupby("Store").agg(doses=("Doses on hand", "sum"), t=("Count closed", "max"))
    st = stores.set_index("Store")
    ship = {str(v): k for k, v in st["Meridale ship-to"].items()}
    former = {v: k for k, v in st["Former name"].dropna().items()}
    mer = pd.read_csv(os.path.join(T, "meridale_vaccine_invoices_2026.csv"), dtype={"SHIP_TO": str, "NDC": str})
    mer["store"] = [ship.get(a) or former["Lindqvist Apothecary #%d" % int(n.split("#")[1])]
                    for a, n in zip(mer["SHIP_TO"], mer["SHIP_TO_NAME"])]
    mer["t"] = pd.to_datetime(mer["DELIVERED"], format="%m/%d/%Y %H:%M")
    mer["doses"] = mer["QTY_SHIPPED"] * mer["NDC"].map(n11).map(dpp)
    adm = pd.read_csv(os.path.join(T, "pharmacy_vaccine_administrations_2026.csv"), parse_dates=["administered_at"])
    wo = pd.read_csv(os.path.join(T, "vaccine_writeoff_log_2026.csv"), parse_dates=["written_off_at"])
    wo["doses"] = np.where(wo["ndc"].map(vial) & (wo["written_off_at"] < "2026-06-01"),
                           wo["quantity"] * wo["ndc"].map(dpp), wo["quantity"])
    tr = pd.read_csv(os.path.join(T, "vaccine_store_transfers_2026.csv"), parse_dates=["shipped_at", "received_at"])
    gold_a = {}
    for no in st.index:
        a, b = o.loc[no, "t"], c.loc[no, "t"]
        w = lambda s: (s > a) & (s <= b)
        v = (o.loc[no, "doses"] + mer.loc[(mer["store"] == no) & w(mer["t"]), "doses"].sum()
             + tr.loc[(tr["to_store"] == no) & w(tr["received_at"]), "doses"].sum()
             - adm.loc[(adm["store"] == no) & w(adm["administered_at"]), "doses"].sum()
             - wo.loc[(wo["store"] == no) & w(wo["written_off_at"]), "doses"].sum()
             - tr.loc[(tr["from_store"] == no) & w(tr["shipped_at"]), "doses"].sum() - c.loc[no, "doses"])
        gold_a[no] = int(v)
    say("ask A, every store's doses unaccounted for", all(gold_a[no] == f["stores"][str(no)]["doses_unaccounted"]
                                                         for no in gold_a))
    # ask B
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(T, "brannon_service_agreement_2025.pdf"), "-"],
                         capture_output=True, text=True).stdout
    price = {m.group(1): float(m.group(2)) for m in
             re.finditer(r"(\w+ [A-Z]+-\d+)\s+(?:Pharmaceutical-grade|Household-style)\s+(\d+\.\d\d)", txt)}
    unit = dict(zip(st.index, st["Vaccine refrigerator"]))
    site = {v: k for k, v in st["Brannon site"].items()}
    ar = pd.read_excel(os.path.join(T, "brannon_service_history_2026-01_2027-01.xlsx"), skiprows=3)
    ar["store"] = ar["Site"].map(site)
    spend = defaultdict(float)
    for invno, g in ar.groupby("Invoice"):
        if g["Visit date"].max().year != 2026:
            continue
        amt = float(g["Invoice amount"].iloc[0])
        if g["Invoice date"].iloc[0] < pd.Timestamp("2026-07-01"):
            amt = round(amt + round(amt * 0.06 + 1e-9, 2), 2)
        ss = sorted(set(g["store"]))
        tot = sum(price[unit[s]] for s in ss)
        for s in ss:
            spend[s] += amt * (price[unit[s]] / tot if len(ss) > 1 else 1.0)
    say("ask B, every store's Brannon spend", all(half_up(round(spend[no], 2)) == f["stores"][str(no)]["service_usd"]
                                                for no in st.index))
    # the golden workbook carries the same figures
    gx = pd.read_excel(os.path.join(GOLD, "penwick_refrigerator_replacements_2027.xlsx"), sheet_name=None, header=None)
    rep = gx["2027 replacements"]
    body = rep.iloc[4:4 + len(st)]
    ok = all(int(r[2]) == f["stores"][str(int(r[0]))]["hours"] and (r[3] == "Yes") == f["stores"][str(int(r[0]))]
             ["replaced"] for _, r in body.iterrows())
    s2 = gx["Stock and service"].iloc[1:1 + len(st)]
    ok2 = all(int(r[2]) == f["stores"][str(int(r[0]))]["doses_unaccounted"] and int(r[3]) ==
              f["stores"][str(int(r[0]))]["service_usd"] for _, r in s2.iterrows())
    say("the golden workbook carries every store's hours, replacement, doses and spend", ok and ok2)
    svg = open(os.path.join(GOLD, "penwick_vaccine_hours_2026.svg"), encoding="utf-8").read()
    say("the golden chart labels the 24-hour line and every store", "24 hours" in svg and
        all(("%s %s" % (no, st.loc[no, "Town"])) in svg for no in st.index))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    say("submission.md states the call", ("stores %s" % ", ".join(map(str, cov[:-1]))) in sub)
    print("%d failed" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
