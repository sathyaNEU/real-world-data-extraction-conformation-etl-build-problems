"""Independent recomputation of every graded figure from target.zip (or a target folder), by code that shares nothing
with solve.py, against figures.json and submission.md.   python3 verify.py [target.zip|target]"""
import io
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
FAILS = []


def check(cond, msg):
    print(("ok    " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def unpack(src):
    if os.path.isdir(src):
        return {f: open(os.path.join(src, f), "rb").read() for f in os.listdir(src)}
    with zipfile.ZipFile(src) as z:
        return {n: z.read(n) for n in z.namelist() if not n.endswith("/")}


def pdf_text(b):
    return "\n".join(p.extract_text() for p in PdfReader(io.BytesIO(b)).pages)


def report_loads(F):
    t = pdf_text(F["suspended_sediment_loads_2027.pdf"])
    check("Load 2027" in t, "report: the table header reads back")
    lines = [x.strip() for x in t.split("\n") if x.strip()]
    out = {}
    for i, x in enumerate(lines):
        if re.fullmatch(r"[A-Z]{3}", x):
            nums = [y for y in lines[i + 1:i + 12] if re.fullmatch(r"-?[\d,]+(\.\d+)?", y)]
            if len(nums) >= 6:
                out[x] = int(nums[5].replace(",", ""))
    return out


def grid(F):
    r = pd.read_parquet(io.BytesIO(F["sediment_stations_15min_2025-2027.parquet"]))
    r = r.drop_duplicates(subset=["station", "time_utc"])
    idx = pd.date_range("2025-01-01", periods=3 * 365 * 96, freq="15min", tz="UTC")
    out = {}
    for code, g in r.groupby("station"):
        out[code] = g.set_index("time_utc").reindex(idx)
    return out, idx


def bottles(F):
    f = pd.read_csv(io.BytesIO(F["field_samples_2025-2027.csv"]), keep_default_na=False)
    x = pd.ExcelFile(io.BytesIO(F["lims_ssc_results_2025-2027.xlsx"]))
    a = x.parse("2025")
    b = x.parse("2026-2027")
    b = b[b["status"].eq("final")]
    key_a = ["20%s/%d" % (p[:2], int(p[3:])) for p in a["Prøvenr"]]
    key_b = ["%s/%d" % (s[:4], int(s[5:])) for s in b["sample_id"]]
    res = dict(zip(key_a, a["SS mg/l"])) | dict(zip(key_b, b["ssc_mg_l"]))
    f["key"] = ["%s/%d" % (s[:4], n) for s, n in zip(f["sampled"], f["bottle_no"])]
    check(f["key"].isin(res.keys()).all(), "every field bottle has a laboratory result")
    f["c"] = f["key"].map(res).astype(float)
    t = pd.to_datetime(f["sampled"], utc=True)
    f["step"] = ((t - pd.Timestamp("2025-01-01", tz="UTC")).dt.total_seconds() / 900).round().astype(int)
    return f


def call(F, G, idx, f):
    pub = report_loads(F)
    check(len(pub) == 14, "report: 14 stations read")
    y27 = idx >= pd.Timestamp("2027-01-01", tz="UTC")
    verdict, refit_gap = {}, {}
    for code, r in G.items():
        q = r["discharge_m3s"].interpolate(limit_direction="both").to_numpy()
        tb = r["turbidity_fnu"].to_numpy()
        up = pd.Series(np.gradient(q) / 0.25 / q).rolling(4, center=True, min_periods=1).mean().to_numpy()
        s = f[f["station"] == code]
        k = s["step"].to_numpy()
        lt, lc = np.log10(tb[k]), np.log10(s["c"].to_numpy())
        # the published regression refitted
        A = np.vstack([np.ones_like(lt), lt]).T
        b0 = np.linalg.solve(A.T @ A, A.T @ lc)
        sm0 = np.mean(10 ** (lc - A @ b0))
        L0 = np.sum(10 ** b0[0] * tb[y27] ** b0[1] * sm0 * q[y27]) * 0.0009
        refit_gap[code] = 100 * (pub[code] / L0 - 1)
        # with rising water
        rz = (up[k] > 0.015).astype(float)
        A = np.vstack([np.ones_like(lt), lt, rz]).T
        b1 = np.linalg.solve(A.T @ A, A.T @ lc)
        sm1 = np.mean(10 ** (lc - A @ b1))
        L1 = np.sum(10 ** (b1[0] + b1[1] * np.log10(tb[y27]) + b1[2] * (up[y27] > 0.015)) * sm1 * q[y27]) * 0.0009
        m = 100 * (pub[code] / L1 - 1)
        verdict[code] = "over" if m > 15 else ("under" if m < -15 else "within")
    return verdict, refit_gap


def ask_a(F, G):
    reg = pd.read_excel(io.BytesIO(F["station_register.xlsx"]))
    check(len(reg) == 14 and "sensor_installed" in reg.columns, "register: 14 rows with the sonde's date")
    log = pd.read_csv(io.BytesIO(F["station_maintenance_log_2025-2027.csv"]), keep_default_na=False)
    sw = log[log["visit"] == "sensor replaced"].set_index("station")
    out = {}
    for code, r in G.items():
        d, t0 = sw.loc[code, "date"], sw.loc[code, "sonde_out"]
        swap = pd.to_datetime("%s %s" % (d, t0), format="%d.%m.%Y %H:%M").tz_localize("Europe/Oslo").tz_convert("UTC")
        part = r[r.index < pd.Timestamp("2027-01-01", tz="UTC")]
        bad = np.array(part["turbidity_fnu"].isna().to_numpy(), dtype=bool)
        bad = bad | part["flag"].fillna("").isin(["F", "M", "G", "O"]).to_numpy()
        bad = bad | ((part.index < swap) & (part["turbidity_fnu"].to_numpy() >= 1000.0))
        out[code] = int(round(bad.sum() / 4.0))
    return out


def ask_b(F):
    st = pdf_text(F["SMA_quality_statement_2027.pdf"])
    lots = dict((m.group(1), float(m.group(2))) for m in re.finditer(r"(KS-\d\d-\d\d)\s+kaolin in deionised water\s+([\d.]+)", st))
    check(lots == {"KS-26-11": 50.0, "KS-27-06": 54.0}, "quality statement: the two lots read back")
    e = pd.read_csv(io.BytesIO(F["lab_batch_export_2027.csv"]))
    f = pd.read_csv(io.BytesIO(F["field_samples_2025-2027.csv"]), keep_default_na=False)
    st27 = {"2027-%04d" % n: s for n, s, d in zip(f["bottle_no"], f["station"], f["sampled"]) if d.startswith("2027")}
    bad_batches = set()
    for bno, g in e.groupby("batch"):
        r = g.iloc[0]
        ref = lots[r["control_lot"]]
        c1 = r["control_1_mass_mg"] * 1000 / r["control_1_volume_ml"]
        c2 = r["control_2_mass_mg"] * 1000 / r["control_2_volume_ml"]
        fails = abs(r["blank_change_mg"]) > 0.5 or not (0.9 * ref <= c1 <= 1.1 * ref) or not (0.9 * ref <= c2 <= 1.1 * ref) \
            or abs(c1 - c2) > 0.1 * (c1 + c2) / 2
        if fails:
            bad_batches.add(bno)
    out = {}
    for sid, bno in zip(e["sample_id"], e["batch"]):
        s = st27[sid]
        out[s] = out.get(s, 0) + (bno in bad_batches)
    return out, sorted(bad_batches)


def main(src):
    F = unpack(src)
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    check(len(F) >= 10, "the pack holds %d files" % len(F))
    proc = pdf_text(F["SMP-03_surrogate_load_procedure_v3.pdf"]).replace("\n", " ")
    check("more than 15 per cent, over or under" in proc, "procedure: section 8's tolerance reads back")
    eml = " ".join(F["spring_review_request.eml"].decode("utf-8").split())
    check("Marianne" in eml and "15 per cent" in eml, "request: reads back")
    md = F["data_dictionary.md"].decode("utf-8")
    check("fouled optics" in md, "dictionary: reads back")
    G, idx = grid(F)
    check(len(G) == 14, "record: 14 stations")
    f = bottles(F)
    v, gap = call(F, G, idx, f)
    check(max(abs(x) for x in gap.values()) < 0.1, "the refitted procedure reproduces every published load")
    over = sorted(c for c, x in v.items() if x == "over")
    under = sorted(c for c, x in v.items() if x == "under")
    check(over == fig["call"]["over"] and under == fig["call"]["under"], "the call: %s over, %s under" % (over, under))
    for c in over:
        check("%s %s" % (c, "") in sub or c in sub, "submission names %s" % c)
    A = ask_a(F, G)
    for c, x in sorted(A.items()):
        check(x == fig["asks"]["hours_without_usable_reading"][c], "Ask A %s: %d hours" % (c, x))
        check(("   - %s: %s" % (c, "{:,}".format(x))) in sub, "Ask A %s in the submission" % c)
    B, bad = ask_b(F)
    check(bad == fig["asks"]["failed_batches"], "Ask B: %d failed batches" % len(bad))
    for c, x in sorted(B.items()):
        check(x == fig["asks"]["samples_in_failed_batches"][c], "Ask B %s: %d samples" % (c, x))
        check(("   - %s: %d" % (c, x)) in sub, "Ask B %s in the submission" % c)
    print("%d FAIL" % len(FAILS))
    return FAILS


if __name__ == "__main__":
    f = main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target.zip"))
    sys.exit(1 if f else 0)
