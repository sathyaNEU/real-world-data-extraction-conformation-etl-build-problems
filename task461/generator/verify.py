"""Independent verifier: reads only target/ and golden/, on its own code path (pandas, its own parsing and its own
hierarchy test), and recomputes every graded figure: the base building by month and for the year, the Scope 2 KPI
against the target, the generator's gas oil by quarter and each chiller's refrigerant; each format is read back."""
import os
import re
import sys

import numpy as np
import openpyxl
import pandas as pd
import pdfplumber

FAILS = []


def check(name, cond, detail=""):
    if not cond:
        FAILS.append("%s %s" % (name, detail))
    return cond


def main(target, golden):
    with pdfplumber.open(os.path.join(target, "corvane_rcf_schedule9_sustainability_kpis.pdf")) as p:
        sched = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in p.pages))
    factor = float(re.search(r"multiplied by ([\d.]+) kg CO2e per kWh", sched).group(1))
    nla = float(re.search(r"Net Lettable Area\s+means ([\d,]+) square metres", sched).group(1).replace(",", ""))
    target_v = float(re.search(r"2026 ([\d.]+) 2027", sched).group(1))
    dfac = float(re.search(r"at ([\d.]+) kg CO2e per litre", sched).group(1))
    gwp = float(re.search(r"potential of ([\d,]+) for R-134a", sched).group(1).replace(",", ""))
    hh = pd.read_csv(os.path.join(target, "supplier_hh_import_1600004417286_2026.csv"))
    hh["month"] = pd.to_datetime(hh["SETTLEMENT_DATE"], format="%d/%m/%Y").dt.month
    imp = hh.groupby("month")["IMPORT_KWH"].sum()
    b = pd.read_csv(os.path.join(target, "bms_energy_meter_registers_2026.csv"))
    b["kwh"] = np.where(b["Units"] == "Wh", b["Value"] / 1000.0, b["Value"])
    b["t"] = pd.to_datetime(b["Timestamp"], format="%d/%m/%Y %H:%M")
    reg = pd.read_excel(os.path.join(target, "pellow_house_meter_register.xlsx"), sheet_name="Meters")
    reg = reg[reg["Meter"].astype(str).str.startswith("EM-")]
    ten = [m for m in reg[reg["Recharged to occupier"] == "Yes"]["Meter"] if m != "EM-118"]
    # one continuous register per tenancy meter (EM-110 carried on by EM-118 from the swap)
    series = {}
    for m in ten:
        s = b[b["Point"] == m][["t", "kwh"]].reset_index(drop=True)
        if m == "EM-110":
            n = b[b["Point"] == "EM-118"][["t", "kwh"]].iloc[1:].copy()
            n["kwh"] += s["kwh"].iloc[-1]
            s = pd.concat([s, n], ignore_index=True)
        series[m] = s
    inc = {}
    for m, s in series.items():
        d = s["kwh"].diff().shift(-1)
        step = s["t"].diff().shift(-1) == pd.Timedelta(minutes=30)
        inc[m] = pd.Series(d[step].to_numpy(), index=s["t"][step].to_numpy()).groupby(level=0).first()
    nested = {}
    for c_ in ten:
        for p_ in ten:
            if c_ == p_:
                continue
            j = pd.concat([inc[c_], inc[p_]], axis=1, join="inner")
            j.columns = ["c", "p"]
            dark = j[j["p"] < 0.01]
            if (j["c"] <= j["p"] + 0.05).all() and len(dark) and (dark["c"] < 0.01).all():
                nested[c_] = p_
    check("hierarchy", nested == {"EM-102": "EM-101", "EM-105": "EM-104", "EM-108": "EM-107"}, str(nested))
    sup = [m for m in ten if m not in nested]
    bounds = pd.to_datetime(["2026-%02d-01" % m for m in range(1, 13)] + ["2027-01-01"])

    def at(s, t):
        return float(s.loc[s["t"] == t, "kwh"].iloc[0])
    base = {}
    for i in range(12):
        a, z = bounds[i], bounds[i + 1]
        tot = sum(at(series[m], z) - at(series[m], a) for m in sup)
        base[i + 1] = imp[i + 1] - tot
    year = sum(base.values())
    kpi = year * factor / nla
    wb = openpyxl.load_workbook(os.path.join(golden, "pellow_house_2026_kpi_report.xlsx"), data_only=True)
    ws = wb["KPI 2026"]
    for m in range(1, 13):
        check("month %d" % m, round(ws.cell(row=4 + m, column=4).value) == round(base[m] / 1000.0))
    check("year MWh", round(ws.cell(row=17, column=4).value) == round(year / 1000.0))
    check("KPI", round(ws.cell(row=22, column=4).value, 1) == round(kpi, 1), "%.3f" % kpi)
    check("target", ws.cell(row=23, column=4).value == target_v)
    check("result", ws.cell(row=25, column=4).value == ("Target missed" if kpi > target_v else "Target met"))
    # gas oil: dips through the chart, each dip week's burn placed on its runs
    cal = pd.read_excel(os.path.join(target, "generator_day_tank_calibration.xlsx"), sheet_name="DT-1")
    cal = cal[pd.to_numeric(cal["Dip (mm)"], errors="coerce").notna()]
    chart = dict(zip(cal["Dip (mm)"].astype(int), cal["Contents (litres)"].astype(float)))
    dp = pd.read_csv(os.path.join(target, "generator_tank_dips_2026.csv"))
    dp["t"] = pd.to_datetime(dp["dip_date"] + " " + dp["dip_time"], format="%d/%m/%Y %H:%M")
    dp["l"] = dp["product_mm"].map(chart)
    dk = pd.read_csv(os.path.join(target, "gas_oil_delivery_dockets_2026.csv"))
    dk["t"] = pd.to_datetime(dk["delivery_date"] + " " + dk["delivery_time"], format="%d/%m/%Y %H:%M")
    ev = pd.read_csv(os.path.join(target, "generator_controller_events_2026.csv"))
    ev["t"] = pd.to_datetime(ev["event_time"], format="%d/%m/%Y %H:%M:%S")
    starts = ev[ev["event"] == "ENGINE START"]["t"].to_numpy()
    stops = ev[ev["event"] == "ENGINE STOP"]["t"].to_numpy()

    def stock(when):
        i = dp[dp["t"] <= when].index.max()
        t0, s0, t1, s1 = dp.loc[i, "t"], dp.loc[i, "l"], dp.loc[i + 1, "t"], dp.loc[i + 1, "l"]
        add = dk[(dk["t"] > t0) & (dk["t"] <= t1)]["litres"].sum()
        pre = dk[(dk["t"] > t0) & (dk["t"] <= when)]["litres"].sum()
        burn = s0 + add - s1
        sel = (starts < np.datetime64(t1)) & (stops > np.datetime64(t0))
        tot = sum((min(e, np.datetime64(t1)) - max(a, np.datetime64(t0))) / np.timedelta64(1, "s")
                  for a, e in zip(starts[sel], stops[sel]))
        done = sum((min(e, np.datetime64(when)) - max(a, np.datetime64(t0))) / np.timedelta64(1, "s")
                   for a, e in zip(starts[sel], stops[sel]) if a < np.datetime64(when))
        return s0 + pre - burn * done / tot
    qb = pd.to_datetime(["2026-01-01", "2026-04-01", "2026-07-01", "2026-10-01", "2027-01-01"])
    s1 = wb["Scope 1 2026"]
    for q in range(4):
        dl = dk[(dk["t"] >= qb[q]) & (dk["t"] < qb[q + 1])]["litres"].sum()
        litres = stock(qb[q]) + dl - stock(qb[q + 1])
        check("diesel Q%d" % (q + 1), round(s1.cell(row=4 + q, column=2).value) == round(litres), "%.2f" % litres)
        check("diesel kg Q%d" % (q + 1), round(s1.cell(row=4 + q, column=3).value) == round(litres * dfac))
    fg = pd.read_csv(os.path.join(target, "fgas_log_chillers_2026.csv"))
    rc = pd.read_excel(os.path.join(target, "calbrook_recovery_record_2026.xlsx"), sheet_name="Recovery 2026")
    recovered = rc.groupby("Job")["Recovered (kg)"].sum()
    fg["rec"] = fg["job_ref"].map(recovered).fillna(0.0)
    fg["net"] = fg["kg_added"].fillna(0.0) - np.where(fg["activity"].str.startswith("Recharge"), fg["rec"], 0.0)
    net = fg.groupby("plant")["net"].sum()
    for i, ch in enumerate(sorted(net.index)):
        check("refrigerant %s" % ch, round(s1.cell(row=10 + i, column=2).value, 1) == round(net[ch], 1),
              "%.3f" % net[ch])
        check("refrigerant kg CO2e %s" % ch, round(s1.cell(row=10 + i, column=3).value) == round(net[ch] * gwp))
    with pdfplumber.open(os.path.join(golden, "pellow_house_2026_kpi_letter.pdf")) as p:
        letter = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in p.pages))
    check("letter states the KPI", ("%.1f kg CO2e per square metre" % kpi) in letter)
    check("letter states the margin", ("%.1f kg over the 2026 target" % (kpi - target_v)) in letter)
    if FAILS:
        raise SystemExit("verify failed: " + "; ".join(FAILS[:6]))
    print("verify: base building by month and year, the KPI, gas oil by quarter and refrigerant by chiller recomputed "
          "on the verifier's own path; every format read back")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
