"""Independent verifier: recompute every figure in generator/figures.json from target/ alone, with pandas and the
time zone database, sharing no code with the generator's analysis.

    python3 task274/generator/verify.py"""
from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTIES = ["Wexmoor", "Corvale", "Lassiter", "Ulverne", "Vellance", "Quennel", "Yarrowmere", "Inskeep"]
DONE = {"COMPLETE", "PARTIAL", "COMPLETE - PROXY"}


def num(s):
    s = str(s)
    if s.startswith("<"):
        return float(s[1:]) - 0.05
    if s.startswith(">"):
        return float(s[1:]) + 0.05
    return float(s)


def main_call(T):
    persons = pd.read_csv(os.path.join(T, "mhnes_2025_examined_persons.csv"), dtype={"COUNTY_CODE": str})
    track = pd.read_csv(os.path.join(T, "mhnes_2025_specimen_tracking.csv"), usecols=["BARCODE", "SEQN"])
    track["SID"] = track["BARCODE"].str.replace("-", "", regex=False)
    sid = track.drop_duplicates("SID").set_index("SID")["SEQN"]
    reg = pd.read_csv(os.path.join(T, "instrument_register.csv")).set_index("LIS_CODE")["SERIAL_NO"]
    res = pd.read_csv(os.path.join(T, "lis_vitd_results_2025.csv"), dtype=str)
    res = res[res["RESULT_STATUS"] == "F"].copy()
    res["SEQN"] = res["SPECIMEN_ID"].map(sid).astype(int)
    res["v"] = res["RESULT"].map(num)
    res["t"] = pd.to_datetime(res["RESULTED_AT"], format="%m/%d/%Y %H:%M")
    res["sn"] = res["INSTRUMENT"].map(reg)
    br = pd.read_csv(os.path.join(T, "lis_vitd_bridging_run_2025-12-16.csv"), dtype=str)
    br["SEQN"] = br["SPECIMEN_ID"].map(sid).astype(int)
    br["b"] = br["RESULT"].map(num)
    ev = pd.read_csv(os.path.join(T, "analyzer_event_log_2025.csv"), dtype=str)
    cal = ev[(ev["EVENT_TYPE"] == "CALIBRATION") & (ev["OUTCOME"] == "ACCEPTED")].copy()
    tz = ZoneInfo("America/Denver")
    cal["t"] = pd.to_datetime(cal["EVENT_UTC"], utc=True).dt.tz_convert(tz).dt.tz_localize(None)
    cal = cal.sort_values("t").reset_index(drop=True)
    cal["cal_id"] = cal["INSTRUMENT_SN"] + "@" + cal["t"].dt.strftime("%Y-%m-%d %H:%M")
    res = res.sort_values("t")
    res = pd.merge_asof(res, cal[["t", "INSTRUMENT_SN", "cal_id"]].rename(columns={"INSTRUMENT_SN": "sn"}),
                        on="t", by="sn", direction="backward")
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(T, "accuracy_program_report_2025-B.pdf"), "-"],
                         capture_output=True, text=True).stdout
    mean = float(re.search(r"Mean\s+([+-][\d.]+)", txt).group(1))
    sn = re.search(r"Instrument\s+(\S+)", txt).group(1)
    day = pd.to_datetime(re.search(r"Date tested\s+(\d+ \w+ \d{4})", txt).group(1), format="%d %B %Y")
    c_chk = cal[(cal["INSTRUMENT_SN"] == sn) & (cal["t"] <= day + pd.Timedelta(hours=10))].iloc[-1]["cal_id"]
    m = res.merge(br[["SEQN", "b"]], on="SEQN")
    m["y"] = np.log(m["v"] / m["b"])
    shift = m.groupby("cal_id")["y"].mean()
    bias = math.log1p(mean / 100.0) - shift[c_chk] + res["cal_id"].map(shift)
    res["below"] = res["v"] / np.exp(bias) < 20.0
    res = res.merge(persons[["SEQN", "COUNTY_CODE", "WTMEC2025"]], on="SEQN")
    sh = res.groupby("COUNTY_CODE").apply(lambda d: (d["WTMEC2025"] * d["below"]).sum() / d["WTMEC2025"].sum(),
                                          include_groups=False)
    out = {COUNTIES[int(c) - 1]: float(v) for c, v in sh.items()}
    return out, mean


def asks(T):
    st = pd.read_csv(os.path.join(T, "mhnes_2025_sp_status.csv"), dtype={"COUNTY_CODE": str})
    ro = pd.read_csv(os.path.join(T, "mhnes_2025_screener_rosters.csv"), dtype={"COUNTY_CODE": str})
    sc = ro.drop_duplicates("SCREENER_ID")[["SCREENER_ID", "DWELLING_ID", "SCREEN_DATE"]]
    last = sc.sort_values(["DWELLING_ID", "SCREEN_DATE"]).groupby("DWELLING_ID").tail(1)["SCREENER_ID"]
    sp = st[st["SCREENER_ID"].isin(set(last))]
    sp = sp[~sp["INT_STATUS"].str.startswith("INELIGIBLE")]
    g = sp.groupby("COUNTY_CODE")
    rr_i = (g.apply(lambda d: d["INT_STATUS"].isin(DONE).mean(), include_groups=False) * 100).round(1)
    rr_e = (g.apply(lambda d: (d["EXAM_STATUS"] == "EXAMINED").mean(), include_groups=False) * 100).round(1)
    dsq = pd.read_csv(os.path.join(T, "mhnes_2025_dsq_products.csv"), dtype={"PRODUCT_ID": str})
    prod = pd.read_excel(os.path.join(T, "supplement_label_extract_2025.xlsx"), sheet_name="Products")
    ing = pd.read_excel(os.path.join(T, "supplement_label_extract_2025.xlsx"), sheet_name="Ingredients")
    vd = ing[ing["INGREDIENT"].str.lower().str.contains("vitamin d|calciferol")].copy()
    vd["iu"] = vd["AMOUNT_PER_SERVING"] * np.where(vd["UNIT"].str.lower() == "mcg", 40.0, 1.0)
    vd = vd.merge(prod[["DSLD_ID", "SERVING_SIZE"]], on="DSLD_ID")
    per_unit = (vd["iu"] / vd["SERVING_SIZE"]).groupby(vd["DSLD_ID"]).sum()

    def unit_iu(row):
        if row["PRODUCT_ID"] == "GENERIC":
            mm = re.search(r"([\d,]+)\s*(IU|MCG)", row["PRODUCT_NAME_REPORTED"])
            return float(mm.group(1).replace(",", "")) * (40.0 if mm.group(2) == "MCG" else 1.0) if mm else 0.0
        return float(per_unit.get(row["PRODUCT_ID"], 0.0))
    dsq["iu"] = dsq.apply(unit_iu, axis=1)
    # a generic line repeating one of the person's label lines in strength, days and units is that bottle again
    lab = dsq[(dsq["PRODUCT_ID"] != "GENERIC") & (dsq["iu"] > 0)][["SEQN", "iu", "DAYS_TAKEN_30D", "UNITS_PER_DAY"]]
    gen = dsq[dsq["PRODUCT_ID"] == "GENERIC"].merge(lab.drop_duplicates(), on=["SEQN", "iu", "DAYS_TAKEN_30D",
                                                                              "UNITS_PER_DAY"], how="left", indicator=True)
    drop_idx = set(dsq[dsq["PRODUCT_ID"] == "GENERIC"].index[(gen["_merge"] == "both").values])
    keep = dsq.drop(index=list(drop_idx))
    keep = keep.assign(d=keep["iu"] * keep["UNITS_PER_DAY"] * keep["DAYS_TAKEN_30D"] / 30.0)
    avg = keep.groupby("SEQN")["d"].sum()
    it = st[st["INT_STATUS"].isin(DONE)].copy()
    it["avg"] = it["SEQN"].map(avg).fillna(0.0)
    out = {}
    for t in (1000, 2000):
        out[t] = (it.groupby("COUNTY_CODE").apply(lambda d: (d["WTINT2025"] * (d["avg"] >= t - 1e-9)).sum()
                                                  / d["WTINT2025"].sum(), include_groups=False) * 100).round(1)
    return rr_i, rr_e, out


def run(task):
    T = os.path.join(task, "target")
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    ok = True
    sh, mean = main_call(T)
    G = [c for c in COUNTIES if sh[c] > 0.30]
    print("verify: counties above 30 per cent: %s" % ", ".join(G))
    ok &= G == fig["call"]["counties"]
    for c in COUNTIES:
        d = abs(100 * sh[c] - fig["counties"][c]["share_below_20"])
        if d > 0.051:
            print("verify FAIL share %s %.2f vs %.1f" % (c, 100 * sh[c], fig["counties"][c]["share_below_20"]))
            ok = False
    ok &= abs(mean - fig["check"]["mean_difference_pct"]) < 1e-9
    rr_i, rr_e, sup = asks(T)
    for i, c in enumerate(COUNTIES):
        code = "%02d" % (i + 1)
        pairs = ((rr_i[code], fig["asks"]["interview_rr"][c]), (rr_e[code], fig["asks"]["exam_rr"][c]),
                 (sup[1000][code], fig["asks"]["supplements_1000"][c]), (sup[2000][code], fig["asks"]["supplements_2000"][c]))
        for a, b in pairs:
            if abs(float(a) - float(b)) > 1e-9:
                print("verify FAIL ask %s %s vs %s" % (c, a, b))
                ok = False
    print("verify: %s" % ("PASS" if ok else "FAIL"))
    return ok


if __name__ == "__main__":
    sys.exit(0 if run(os.path.dirname(HERE)) else 1)
