"""An independent recompute of task478's graded figures from the cut pack, sharing no code with bundle.py: each
facility's 2026 NOx from its Rule 4306 units, the five, the gas Tamsett Valley Gas delivered and the emergency engines'
NOx; then the same figures read back from figures.json, submission.md and the three goldens.

    python3 task478/generator/verify.py
"""
import csv
import datetime as dt
import json
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
OK = []


def say(name, ok):
    OK.append(bool(ok))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))


def half_up(x):
    return int(np.floor(x + 0.5))


def days_of(y, m):
    return (dt.date(y + m // 12, m % 12 + 1, 1) - dt.date(y, m, 1)).days


def main():
    p = lambda fn: os.path.join(T, fn)
    pm = pd.read_csv(p("tbapcd_permit_devices.csv"), dtype=str)
    app = {}
    for r in pm.drop_duplicates("FAC_NO").itertuples():
        app[r.FAC_NO] = r.FACILITY
    order = list(pd.read_csv(os.path.join(G, "tbapcd_nox_inventory_2026.csv"), dtype=str)["facility"])
    u = pm[pm["RULE"] == "4306"].set_index("DEVICE_NO")
    fac_of = u["FACILITY"].to_dict()
    fd = {"natural gas": 8710.0, "landfill gas": 9570.0, "digester gas": 9570.0}

    # monitored units: the hourly mass, joined through the monitoring plan's unit id
    cems = pd.read_csv(p("tbapcd_cems_hourly_2026.csv"), dtype={"facility_id": str, "unit_id": str})
    plan_id = u[u["MONITORING"] == "CEMS"].reset_index()[["FAC_NO", "CEMS_UNIT_ID", "DEVICE_NO"]]
    cems = cems.merge(plan_id, left_on=["facility_id", "unit_id"], right_on=["FAC_NO", "CEMS_UNIT_ID"], how="left")
    assert cems["DEVICE_NO"].notna().all()
    lb = cems.groupby("DEVICE_NO")["nox_mass_lb"].sum().to_dict()

    # unmonitored units: tests in lb/MMBtu, monthly heat input and hours spread by day, catalyst dates from the log
    o = pd.read_csv(p("tbapcd_source_tests_2018_2021.csv"), dtype=str)
    tests = pd.DataFrame({"dev": "D-" + o["DEVICE_NO"], "date": pd.to_datetime(o["TEST_DATE"], format="%m/%d/%Y"),
                          "lb": o["NOX_LB_HR"].astype(float) / (o["FUEL_FLOW_SCFH"].astype(float) *
                                                                o["FUEL_HHV"].astype(float) / 1e6)})
    n = pd.read_excel(p("tbapcd_source_tests_2022_2026.xlsx"), sheet_name="Results")
    tests = pd.concat([tests, pd.DataFrame({"dev": n["Device No."], "date": pd.to_datetime(n["Test Date"]),
                                            "lb": n["NOx (lb/MMBtu)"].astype(float)})], ignore_index=True)
    st = pd.read_csv(p("tbapcd_emission_statements_2017_2026.csv"), dtype=str)
    q = st["QUANTITY"].astype(float)
    hhv = pd.to_numeric(st["HHV_BTU_SCF"], errors="coerce").fillna(1037.0)
    st["mmbtu"] = np.select([st["UNIT"] == "THERMS", st["UNIT"] == "MMBTU", st["UNIT"] == "MMSCF"], [q / 10, q, q * hhv])
    st["hours"] = st["HOURS"].astype(float)
    ev = pd.read_csv(p("tbapcd_compliance_events_2017_2026.csv"), dtype=str)
    ev["d"] = [pd.Timestamp(dt.datetime.strptime(x, "%m/%d/%Y")) if "/" in x else pd.Timestamp(x) for x in ev["EVENT_DATE"]]
    cats = ev[ev["EVENT_TYPE"].isin(["SCR INSTALLED", "CATALYST"])].groupby("DEVICE_NO")["d"].apply(sorted).to_dict()
    open_units = [d for d in u.index if u.loc[d, "MONITORING"] != "CEMS"]
    daily = {}
    for d in open_units:
        s = st[st["DEVICE_NO"] == d]
        rows = []
        for r in s.itertuples():
            y, m = int(r.STMT_YEAR), int(r.MONTH)
            k = days_of(y, m)
            for i in range(k):
                rows.append((pd.Timestamp(y, m, 1) + pd.Timedelta(days=i), r.hours / k, r.mmbtu / k))
        df = pd.DataFrame(rows, columns=["day", "h", "q"]).sort_values("day").reset_index(drop=True)
        seg = np.searchsorted(np.array(cats[d], dtype="datetime64[ns]"), df["day"].to_numpy(), side="right")
        df["seg"] = seg
        df["cat"] = df.groupby("seg")["h"].cumsum() - df["h"]
        df.loc[df["seg"] == 0, "cat"] = 0.0
        daily[d] = df.set_index("day")
    tests["h"] = [daily[r.dev].loc[r.date, "cat"] for r in tests.itertuples()]
    devs = sorted(tests["dev"].unique())
    X = np.zeros((len(tests), len(devs) + 1))
    X[np.arange(len(tests)), [devs.index(d) for d in tests["dev"]]] = 1.0
    X[:, -1] = tests["h"]
    coef = np.linalg.lstsq(X, np.log(tests["lb"].to_numpy()), rcond=None)[0]
    beta = coef[-1]
    for d in open_units:
        df = daily[d]
        y = df[(df.index.year == 2026) & (df["q"] > 0)]
        lb[d] = float((y["q"] * np.exp(coef[devs.index(d)] + beta * (y["cat"] + y["h"] / 2))).sum())
    tons = {f: 0.0 for f in order}
    for d, v in lb.items():
        tons[fac_of[d]] += v / 2000.0
    five = sorted(sorted(order, key=lambda f: -tons[f])[:5], key=order.index)

    # ask A: billed usage in therms, the conversion date read off the meters billed from their index
    b = pd.read_csv(p("tvg_commercial_billing_extract_2027-02.csv"), dtype=str)
    for c in ("READ_FROM", "READ_TO"):
        b[c] = pd.to_datetime(b[c], format="%m/%d/%Y")
    for c in ("PRIOR_READ", "CURRENT_READ", "USAGE_CCF"):
        b[c] = b[c].astype(float)
    b["mult"] = pd.to_numeric(b["PRESSURE_MULT"], errors="coerce")
    b["btu"] = b["BTU_FACTOR"].astype(float)
    ix = b[b["mult"].notna()]
    corr = (ix["CURRENT_READ"] - ix["PRIOR_READ"]) * ix["mult"]
    therm = (ix["USAGE_CCF"] - corr * ix["btu"]).abs() < (ix["USAGE_CCF"] - corr).abs()
    cut = ix[therm]["READ_TO"].min()
    assert (therm == (ix["READ_TO"] >= cut)).all()
    b["therms"] = np.where(b["READ_TO"] >= cut, b["USAGE_CCF"], b["USAGE_CCF"] * b["btu"])
    key = lambda a: re.sub(r"[^A-Z0-9]", "", re.sub(r"\b(ROAD|AVENUE|STREET|BOULEVARD|LANE|DRIVE|WAY)\b",
                                                         lambda m: {"ROAD": "RD", "AVENUE": "AVE", "STREET": "ST",
                                                                    "BOULEVARD": "BLVD", "LANE": "LN", "DRIVE": "DR",
                                                                    "WAY": "WY"}[m.group(1)], a.upper()))
    import pypdf
    plan = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in pypdf.PdfReader(
        p("tbapcd_lowry_creek_cerp_2027.pdf")).pages))
    addr = {}
    for f in order:
        m = re.search(re.escape(f) + r" \d{4} (\d+ [A-Z][\w. ]+?(?:Road|Avenue|Street|Boulevard|Lane|Drive|Way|Row))", plan)
        addr[key(m.group(1))] = f
    b["fac"] = [addr[key(a)] for a in b["SERVICE_ADDRESS"]]
    y0, y1 = pd.Timestamp(2026, 1, 1), pd.Timestamp(2027, 1, 1)
    share = ((np.minimum(b["READ_TO"], y1) - np.maximum(b["READ_FROM"], y0)).dt.days.clip(lower=0) /
             (b["READ_TO"] - b["READ_FROM"]).dt.days)
    gas = (b["therms"] * share / 10.0).groupby(b["fac"]).sum().to_dict()

    # ask B: the logs, hours and minutes where the meters say so, replaced engines at the removed engine's rating
    xl = pd.ExcelFile(p("tbapcd_rule4702_engine_logs_2026.xlsx"))
    logs = []
    for sh in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sh, header=1)
        df.columns = ["date", "dev", "v", "why"]
        df["fac"] = app[sh]
        logs.append(df)
    logs = pd.concat(logs, ignore_index=True)
    logs["date"] = pd.to_datetime(logs["date"])
    hm = lambda v: np.floor(v + 1e-9) + np.round((v - np.floor(v + 1e-9)) * 100) / 60.0
    eq = ev[ev["EVENT_TYPE"] == "EQUIPMENT"]
    old = {}
    for r in eq.itertuples():
        m = re.search(r"removed .*?\(([\d,]+) bhp, (Tier [^)]+)\)", r.DESCRIPTION)
        old[r.DEVICE_NO] = (r.d, float(m.group(1).replace(",", "")), m.group(2))
    ins = pd.read_csv(p("tbapcd_engine_inspections_2025_2027.csv"), dtype=str)
    ins["d"] = pd.to_datetime(ins["INSPECTION_DATE"])
    ins["r"] = ins["HOUR_METER"].astype(float)
    hmm = set()
    for f, g in logs.groupby("fac"):
        e_dec = e_hmm = 0.0
        for d, gd in g.groupby("dev"):
            if d in old:
                continue
            i = ins[ins["DEVICE_NO"] == d].sort_values("d")
            w = gd[(gd["date"] >= i.iloc[0]["d"]) & (gd["date"] < i.iloc[1]["d"])]["v"]
            span = i.iloc[1]["r"] - i.iloc[0]["r"]
            e_dec += abs(w.sum() - span)
            e_hmm += abs(hm(w).sum() - span)
        if e_hmm < e_dec:
            hmm.add(f)
    tier = {"Tier 1": 6.9, "Tier 2": 4.8, "Tier 3": 3.0, "Tier 4 Final": 0.30}
    allp = pm.set_index("DEVICE_NO")
    lbs = {f: 0.0 for f in order}
    for r in logs.itertuples():
        h = hm(r.v) if r.fac in hmm else r.v
        bhp, t = float(allp.loc[r.dev, "RATING"]), allp.loc[r.dev, "ENGINE_TIER"]
        if r.dev in old and r.date < old[r.dev][0]:
            bhp, t = old[r.dev][1], old[r.dev][2]
        lbs[r.fac] += h * bhp * 0.74 * tier[t] / 453.6

    # read back
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    say("the five: %s" % five, fig["call"]["facilities"] == five)
    say("the 14 whole tons", all(fig["facilities"][f]["nox_tons"] == half_up(tons[f]) for f in order))
    say("the 14 gas figures, whole MMBtu", all(fig["facilities"][f]["gas_mmbtu"] == half_up(gas[f]) for f in order))
    say("the 14 engine figures, whole pounds", all(fig["facilities"][f]["engine_nox_lb"] == half_up(lbs[f]) for f in order))
    say("the climb: %.2f in the log a 10,000 hours" % (beta * 1e4), fig["components"]["climb_log_per_10000h"] ==
        "%.2f" % (beta * 1e4))
    rows = list(csv.DictReader(open(os.path.join(G, "tbapcd_nox_inventory_2026.csv"), encoding="utf-8")))
    say("the golden CSV's 14 rows", [int(r["rule_4306_nox_tons_2026"]) for r in rows] == [half_up(tons[f]) for f in order])
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(G, "tbapcd_cerp_facilities_2027.xlsx"))
    ag = [r[0] for r in wb["Agreements 2027"].iter_rows(min_row=5, max_row=9, values_only=True)]
    say("the workbook's agreements sheet names the five", ag == five)
    fr = {r[0]: r for r in wb["Facilities"].iter_rows(min_row=2, values_only=True) if r[0] in order}
    say("the workbook's facilities sheet: tons, agreement, gas and engines on all 14",
        all(fr[f][2] == half_up(tons[f]) and fr[f][3] == ("Yes" if f in five else "No") and fr[f][4] == half_up(gas[f])
            and fr[f][5] == half_up(lbs[f]) for f in order))
    svg = open(os.path.join(G, "tbapcd_facility_nox_2026.svg"), encoding="utf-8").read()
    say("the chart labels every facility and its whole tons", all(f in svg for f in order) and
        all(re.search(r">%d<" % half_up(tons[f]), svg) for f in order))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    say("submission.md block 4 carries every graded figure",
        all("%s: %d" % (f, half_up(tons[f])) in sub and "%s: %s" % (f, "{:,}".format(half_up(gas[f]))) in sub and
            "%s: %s" % (f, "{:,}".format(half_up(lbs[f]))) in sub for f in order))
    bad = sum(1 for x in OK if not x)
    print("%s  task478 verify: %d checks, %d failed" % ("PASS" if not bad else "FAIL", len(OK), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
