"""Independent verifier: reads only target/ and golden/, on its own code path (pandas, its own clock and parsing),
and recomputes every graded figure: the loading points by quarter, the year's release against the limit, the tanks'
releases by the protocol's method and the stock account's gains and losses; each format is read back."""
import datetime as dt
import math
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


def local_of_utc(ts):
    """Warrenby: AEDT (+11) until 03:00 on 5 April 2026 and again from 02:00 on 4 October 2026, AEST (+10) between."""
    end = pd.Timestamp("2026-04-04 16:00")
    start = pd.Timestamp("2026-10-03 16:00")
    off = np.where((ts >= end) & (ts < start), 10, 11)
    return ts + pd.to_timedelta(off, unit="h")


def protocol_tables(target):
    with pdfplumber.open(os.path.join(target, "CAQA_return_protocol_petroleum_premises_2026.pdf")) as p:
        txt = "\n".join(pg.extract_text() or "" for pg in p.pages)
    t = {}
    for key, label in (("ps", "Petrol, summer grade"), ("pw", "Petrol, winter grade"), ("d", "Diesel")):
        m = re.search(re.escape(label) + r"\s+(\d+\.\d+)\s+(\d+\.\d+)", txt)
        t[key] = (float(m.group(1)), float(m.group(2)))
    mw = {}
    for key, label in (("ps", "Petrol, summer grade"), ("pw", "Petrol, winter grade"), ("d", "Diesel")):
        ms = re.findall(re.escape(label) + r"\s+(\d+)\s*$", txt, re.M)
        mw[key] = float(ms[-1])
    rates = {}
    for label, key in (("Internal floating roof, primary seal only", "ifr1"),
                       ("Internal floating roof, primary and rim-mounted secondary", "ifr2"),
                       ("Fixed roof, distillate service, open vents", "fixed"),
                       ("Fixed roof, distillate service, pressure-vacuum vents", "fixed_pv"),
                       ("Petrol, floating roof", "w_pet"),
                       ("Distillate, fixed roof", "w_dsl")):
        rates[key] = float(re.search(re.escape(label) + r"\s+(\d+(?:\.\d+)?)", txt).group(1))
    lic = ""
    with pdfplumber.open(os.path.join(target, "EPL_20514_licence_conditions.pdf")) as p:
        lic = " ".join(pg.extract_text() or "" for pg in p.pages)
    limit = float(re.search(r"must not exceed (\d+) tonnes in any calendar year", re.sub(r"\s+", " ", lic)).group(1))
    return t, mw, rates, limit


def kg_per_kl(A, B, M, temp, sat):
    P = math.exp(A - B / (temp + 273.15))
    return sat * P * M / (8.314 * (temp + 273.15))


def main(target, golden):
    FAILS.clear()
    tab, mw, rates, limit = protocol_tables(target)
    check("protocol tables read", abs(tab["ps"][1] - 2952.8) < 1e-9 and mw["d"] == 130 and rates["ifr1"] == 0.31)
    reg = pd.read_excel(os.path.join(target, "tanker_register_2027-01.xlsx"), sheet_name="Units")
    plate_rows = []          # (plate, unit, trailer, valid from, valid to)
    for _, r in reg.iterrows():
        prev = r["Previous regos"] if isinstance(r["Previous regos"], str) else ""
        starts = {"lead": pd.Timestamp("2000-01-01"), "dog": pd.Timestamp("2000-01-01")}
        for m in re.finditer(r"(lead|dog) (\S+) until (\d\d)/(\d\d)/(\d{4})", prev):
            until = pd.Timestamp("%s-%s-%s" % (m.group(5), m.group(4), m.group(3))) + pd.Timedelta(days=1)
            plate_rows.append((m.group(2), r["Fleet unit"], m.group(1), pd.Timestamp("2000-01-01"), until))
            starts[m.group(1)] = until
        for tr, col in (("lead", "Lead trailer rego"), ("dog", "Dog trailer rego")):
            if isinstance(r[col], str) and r[col]:
                plate_rows.append((r[col], r["Fleet unit"], tr, starts[tr], pd.Timestamp("2100-01-01")))
    tms_map = dict(zip(reg["TMS tanker ID"], reg["Fleet unit"]))
    old = pd.read_csv(os.path.join(target, "tas_loads_legacy_2026-01-01_to_2026-06-30.csv"), dtype=str)
    old["t"] = pd.to_datetime(old["LOAD_DATE"] + " " + old["LOAD_TIME"], format="%d/%m/%Y %H:%M:%S")
    old = old[old["t"] < pd.Timestamp("2026-07-01")]

    def resolve(plate, t):
        for p, u, tr, lo, hi in plate_rows:
            if p == plate and lo <= t < hi:
                return u, tr
        raise KeyError(plate)
    res = [resolve(p, t) for p, t in zip(old["TRAILER_REGO"], old["t"])]
    old["unit"] = [a for a, _ in res]
    old["comp"] = [int(c) + (5 if tr == "dog" else 0) for c, (_, tr) in zip(old["COMP"], res)]
    old["gross"] = old["GROSS_L"].astype(float)
    old["temp"] = old["TEMPERATURE"].astype(float)
    old["net"] = old["gross"] * old["VCF"].astype(float)
    old["bay"] = old["BAY"].astype(int)
    old["prod"] = old["PRODUCT"].map({"ULP91": "ULP", "PULP95": "P95", "PULP98": "P98", "DIESEL": "DSL"})
    old["op"] = old["CARRIER"]
    new = pd.read_excel(os.path.join(target, "tas_loads_2026-06-29_to_2027-01-04.xlsx"), sheet_name="Transactions",
                        header=4)
    new = new[new["Status"] == "Complete"].copy()
    new["t"] = pd.to_datetime(new["Loaded (local)"])
    new = new[new["t"] >= pd.Timestamp("2026-07-01")]
    new["unit"] = new["Tanker"].map(tms_map)
    new["comp"] = new["Compartment"].astype(int)
    new["gross"] = new["Gross obs L"].astype(float)
    new["temp"] = new["Temp C"].astype(float)
    new["net"] = new["Net 15C L"].astype(float)
    new["bay"] = new["Bay"].astype(int)
    new["prod"] = new["Product"].map({"ULP": "ULP", "P95": "P95", "P98": "P98", "DSL10": "DSL"})
    new["op"] = new["Account"].map({"BRENNOCK": "BRN", "OAKHURST": "OAK"})
    cols = ["t", "unit", "comp", "gross", "temp", "net", "bay", "prod", "op"]
    loads = pd.concat([old[cols], new[cols]], ignore_index=True).sort_values(["t", "unit", "comp"])
    check("verifier read both TMS exports", len(loads) > 30000)
    dk = pd.read_csv(os.path.join(target, "dispatch_delivery_dockets_2025-12_to_2026-12.csv"), dtype=str)
    dk["done"] = pd.to_datetime(dk["completed_at"].str[:19], format="%Y-%m-%dT%H:%M:%S")
    dk["comp"] = dk["compartment"].astype(int)
    dk["petrol_vb"] = (dk["product"] != "Diesel") & (dk["vr1_hose"] == "Y")
    dk = dk.sort_values("done")
    dist = loads[(loads["bay"].isin([4, 5])) & (loads["t"] >= "2026-01-01") & (loads["t"] < "2027-01-01")].copy()
    dist = dist.sort_values("t")
    merged = pd.merge_asof(dist, dk[["done", "fleet_unit", "comp", "petrol_vb"]].rename(columns={"fleet_unit": "unit"}),
                           left_on="t", right_on="done", by=["unit", "comp"], direction="backward",
                           allow_exact_matches=False)
    check("every distillate load found its compartment's previous drop", merged["petrol_vb"].notna().all())
    summer = merged["t"].dt.month.isin([11, 12, 1, 2, 3])
    A = np.where(summer, tab["ps"][0], tab["pw"][0])
    B = np.where(summer, tab["ps"][1], tab["pw"][1])
    M = np.where(summer, mw["ps"], mw["pw"])
    T = merged["temp"].to_numpy()
    pet = merged["gross"].to_numpy() / 1000 * np.exp(A - B / (T + 273.15)) * M / (8.314 * (T + 273.15))
    own = merged["gross"].to_numpy() / 1000 * 0.6 * np.exp(tab["d"][0] - tab["d"][1] / (T + 273.15)) * mw["d"] / (
        8.314 * (T + 273.15))
    merged["kg"] = own + np.where(merged["petrol_vb"].astype(bool), pet, 0.0)
    merged["q"] = (merged["t"].dt.month - 1) // 3 + 1
    bayq = merged.groupby(["bay", "q"])["kg"].sum() / 1000
    cems = pd.read_csv(os.path.join(target, "vru1_outlet_cems_15min_2026.csv"), dtype=str)
    rate = pd.to_numeric(cems["value"], errors="coerce")
    rate = np.where(cems["unit"] == "g/min", rate * 60 / 1000, rate)
    rate = pd.Series(rate)
    valid = (cems["status"] == "OK") & rate.notna()
    fill = rate.copy()
    for i in np.where(cems["status"] == "CAL")[0]:
        lo, hi = max(0, i - 4), min(len(rate), i + 5)
        nb = [rate[j] for j in range(lo, hi) if j != i and valid[j]]
        fill[i] = sum(nb) / len(nb)
    fill[cems["status"] == "OFF"] = 0.0
    loc = pd.to_datetime(cems["interval_start"].str[:19])
    vq = pd.Series(fill.to_numpy() * 0.25 / 1000).groupby(((loc.dt.month - 1) // 3 + 1).to_numpy()).sum()
    ret = pd.read_csv(os.path.join(golden, "warrenby_2026_annual_return.csv"), dtype=str)
    for _, r in ret[ret["section"] == "LOADING"].iterrows():
        q = int(r["period"][1])
        v = vq[q] if r["point_id"] == "VRU-1" else bayq[(int(r["point_id"][-1]), q)]
        check("return %s %s" % (r["point_id"], r["period"]), "%.1f" % v == r["quantity"], "%s %.4f" % (r["quantity"], v))
    total = vq.sum() + bayq.sum()
    with pdfplumber.open(os.path.join(golden, "warrenby_2026_return_note.pdf")) as p:
        note = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in p.pages))
    check("note states the year's release", ("%.1f tonnes" % total) in note, "%.3f" % total)
    check("note states the exceedance", ("exceeded the limit by %.1f" % (total - limit)) in note)
    # tanks by the protocol's method
    treg = pd.read_excel(os.path.join(target, "tank_register_2027-01.xlsx"), sheet_name="Tanks")
    treg = treg[treg["Tank"].astype(str).str.startswith("TK-")]
    wo = pd.read_csv(os.path.join(target, "maintenance_work_orders_2026.csv"), dtype=str)
    seals = {r["asset_tag"]: pd.to_datetime(r["completed"], format="%d/%m/%Y %H:%M") for _, r in wo.iterrows()
             if "secondary seal" in r["description"] and isinstance(r["completed"], str)}
    pvs = {r["asset_tag"]: pd.to_datetime(r["completed"], format="%d/%m/%Y %H:%M") for _, r in wo.iterrows()
           if "pressure-vacuum vents" in r["description"] and isinstance(r["completed"], str)}
    outs = pd.read_excel(os.path.join(target, "ship_receipts_outturn_2026.xlsx"), sheet_name="Outturns 2026")
    days = pd.date_range("2026-01-01", "2026-12-31", freq="D")
    for _, t in treg.iterrows():
        tk = t["Tank"]
        dia = float(t["Diameter (m)"])
        if str(t["Roof"]).startswith("Fixed"):
            done = pvs.get(tk)
            open_days = int(sum(1 for d in days if done is not None and d < done))
            if not str(t["Vents"]).startswith("Pressure-vacuum"):
                open_days = len(days)
            standing = dia * (rates["fixed"] * open_days + rates["fixed_pv"] * (len(days) - open_days))
            w = rates["w_dsl"]
        else:
            done = seals.get(tk)
            primary_days = int(sum(1 for d in days if done is not None and d < done))
            standing = dia * (rates["ifr1"] * primary_days + rates["ifr2"] * (len(days) - primary_days))
            w = rates["w_pet"]
        ml = outs[outs["Shore tank"] == tk]["Shore received L15"].sum() / 1e6
        v = standing + w * ml
        row = ret[(ret["section"] == "TANKS") & (ret["point_id"] == tk)]
        check("tank %s" % tk, int(row["quantity"].iloc[0]) == int(round(v)), "%s %.2f" % (row["quantity"].iloc[0], v))
    # stock account
    log = pd.read_csv(os.path.join(target, "control_room_shift_log_2026.csv"), dtype=str)
    hh = log["time"].str[:2].astype(int)
    lt = pd.to_datetime(log["shift_date"], format="%d/%m/%Y") + pd.to_timedelta(hh, unit="h") + pd.to_timedelta(
        log["time"].str[3:5].astype(int), unit="m")
    lt = lt + pd.to_timedelta(np.where((log["shift"] == "N") & (hh < 18), 1, 0), unit="D")
    log["lt"] = lt
    lu = log[log["entry"].str.startswith("Diesel header changed over")].sort_values("lt")
    lu_to = lu["entry"].str.extract(r"over (TK-\d) to (TK-\d)")
    first = lu_to[0].iloc[0]
    times = lu["lt"].to_numpy()
    tos = lu_to[1].to_numpy()

    def header(t):
        i = np.searchsorted(times, np.datetime64(t), side="right") - 1
        return first if i < 0 else tos[i]
    pt = {"ULP": "TK-1", "P95": "TK-2", "P98": "TK-3"}
    loads["tank"] = [pt[p] if p in pt else header(t) for p, t in zip(loads["prod"], loads["t"])]
    canon = {"Unleaded 91": "ULP", "Premium 95": "P95", "Premium 98": "P98"}
    mb = dk[(dk["source_terminal"] == "WARRENBY") & dk["source_doc"].str.startswith("MB-")].drop_duplicates(
        ["source_doc", "fleet_unit", "comp"])
    manual = pd.DataFrame({"t": pd.to_datetime(mb["arrived_at"].str[:19], format="%Y-%m-%dT%H:%M:%S"),
                           "tank": [pt[canon[p]] for p in mb["product"]], "net": mb["bol_litres_15c"].astype(float)})
    loads = pd.concat([loads, manual], ignore_index=True)
    tr = log[log["entry"].str.startswith("Transfer ")].sort_values("lt")
    trx = tr["entry"].str.extract(r"Transfer (TK-\d) to (TK-\d) (commenced|completed), transfer meter ([\d,]+) L")
    trx["lt"] = tr["lt"].to_numpy()
    trx["m"] = trx[3].str.replace(",", "").astype(int)
    starts_ = trx[trx[2] == "commenced"].reset_index(drop=True)
    ends_ = trx[trx[2] == "completed"].reset_index(drop=True)
    check("transfers pair up", len(starts_) == len(ends_) and (starts_[0] == ends_[0]).all())
    moves = pd.DataFrame({"src": ends_[0], "dst": ends_[1], "end": ends_["lt"], "litres": ends_["m"] - starts_["m"]})
    plc = pd.read_csv(os.path.join(target, "vru1_plc_events_2026-01-01_to_2027-01-04.csv"), dtype=str)
    plc = plc[plc["event"] == "PRODUCT RETURN"].copy()
    plc["t"] = pd.to_datetime(plc["event_time"], format="%d/%m/%Y %H:%M:%S")
    plc["l"] = plc["litres_15c"].astype(int)
    ab = log[log["entry"].str.contains("VRU-1 absorber supply and return")].sort_values("lt")
    ab_to = np.where(ab["entry"].str.contains("back on TK-1"), "TK-1",
                     ab["entry"].str.extract(r"lined up from TK-\d to (TK-\d)", expand=False))
    ab_t = ab["lt"].to_numpy()
    idx = np.searchsorted(ab_t, plc["t"].to_numpy(), side="right") - 1
    plc["tank"] = np.where(idx < 0, "TK-1", np.asarray(ab_to, dtype=object)[np.maximum(idx, 0)])
    dips = pd.read_csv(os.path.join(target, "tank_gauging_daily_2025-12-31_to_2027-01-04.csv"), dtype=str)
    dips["utc"] = pd.to_datetime(dips["dip_time"], format="%d/%m/%Y %H:%M") - pd.Timedelta(hours=10)
    dips["lt"] = local_of_utc(dips["utc"])
    bounds = [pd.Timestamp(s) for s in ("2026-01-01", "2026-04-01", "2026-07-01", "2026-10-01", "2027-01-01")]

    def midnight_stock(tk, b):
        d = dips[(dips["tank"] == tk) & (dips["lt"].dt.normalize() == b)].iloc[0]
        out = loads[(loads["tank"] == tk) & (loads["t"] >= b) & (loads["t"] < d["lt"])]["net"].sum()
        back = plc[(plc["tank"] == tk) & (plc["t"] >= b) & (plc["t"] < d["lt"])]["l"].sum()
        return int(d["nsv_l"]) + out - back
    wb = openpyxl.load_workbook(os.path.join(golden, "warrenby_2026_stock_account.xlsx"), data_only=True)
    ws = wb["Stock account 2026"]
    shown = {(r[0], r[1]): r[9] for r in ws.iter_rows(min_row=5, values_only=True) if r[0]}
    for tk in ("TK-1", "TK-2", "TK-3", "TK-4", "TK-5"):
        for qi in range(4):
            a, b = bounds[qi], bounds[qi + 1]
            rec = outs[(outs["Shore tank"] == tk) & (outs["Commenced"] >= a) & (outs["Commenced"] < b)][
                "Shore received L15"].sum()
            disp = loads[(loads["tank"] == tk) & (loads["t"] >= a) & (loads["t"] < b)]["net"].sum()
            back = plc[(plc["tank"] == tk) & (plc["t"] >= a) & (plc["t"] < b)]["l"].sum()
            inq = (moves["end"] >= a) & (moves["end"] < b)
            tin = moves[inq & (moves["dst"] == tk)]["litres"].sum()
            tout = moves[inq & (moves["src"] == tk)]["litres"].sum()
            g = (midnight_stock(tk, b) - midnight_stock(tk, a) - rec - back - tin + disp + tout) / 1000
            check("stock %s Q%d" % (tk, qi + 1), shown[(tk, "Q%d" % (qi + 1))] == int(round(g)),
                  "%s %.2f" % (shown[(tk, "Q%d" % (qi + 1))], g))
    n_fig = len(ret) + 2 + len(shown)
    if FAILS:
        for f in FAILS:
            print("VERIFY FAIL", f)
        raise SystemExit("verify: %d failures" % len(FAILS))
    print("verify: %d graded figures recomputed from the bundle on the verifier's own path, every format read back"
          % n_fig)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
