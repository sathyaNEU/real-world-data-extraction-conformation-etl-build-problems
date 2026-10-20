"""The golden, from the shipped files only: each station's 2027 load rebuilt from a turbidity relation conditioned on
whether the river was rising, against the published load; the hours of 2025 and 2026 without a usable turbidity
reading; the 2027 samples weighed in a batch that failed its quality control.   S.solve(target) -> dict"""
import io
import os
import re

import numpy as np
import pandas as pd
from pypdf import PdfReader

RISE = 0.015          # per hour: the rate of rise, smoothed over an hour, that separates the samples best
TOL = 15.0
FILES = dict(
    record="sediment_stations_15min_2025-2027.parquet",
    field="field_samples_2025-2027.csv",
    lims="lims_ssc_results_2025-2027.xlsx",
    report="suspended_sediment_loads_2027.pdf",
    register="station_register.xlsx",
    log="station_maintenance_log_2025-2027.csv",
    batches="lab_batch_export_2027.csv",
    statement="SMA_quality_statement_2027.pdf",
)
LOT_CONC = {"KS-26-11": 50.0, "KS-27-06": 54.0}     # the quality statement's table, read in read_lots()


def _p(target, k):
    return os.path.join(target, FILES[k])


def read_report(target):
    """each station's row of the report's table: code, name, regime, samples, a, b, smearing, R-squared, load"""
    text = "\n".join(p.extract_text() for p in PdfReader(_p(target, "report")).pages)
    toks = [t.strip() for t in re.split(r"\s*\n\s*", text) if t.strip()]
    out = {}
    num = re.compile(r"^-?[\d,]+(\.\d+)?$")
    for i, t in enumerate(toks):
        if re.fullmatch(r"[A-Z]{3}", t) and i + 8 < len(toks):
            vals = [x for x in toks[i + 1:i + 12] if num.match(x)]
            if len(vals) >= 6:
                n, a, b, bcf, r2, load = vals[:6]
                out[t] = {"n": int(n), "a": float(a), "b": float(b), "bcf": float(bcf), "r2": float(r2),
                          "load_t": int(load.replace(",", ""))}
    return out


def read_lots(target):
    text = "\n".join(p.extract_text() for p in PdfReader(_p(target, "statement")).pages)
    return {m.group(1): float(m.group(2)) for m in re.finditer(r"(KS-\d\d-\d\d)\s+kaolin in deionised water\s+(\d+\.\d)", text)}


def record(target):
    r = pd.read_parquet(_p(target, "record"))
    return r.drop_duplicates(["station", "time_utc"]).sort_values(["station", "time_utc"]).reset_index(drop=True)


def samples(target):
    f = pd.read_csv(_p(target, "field"), dtype={"callout_ref": str}, keep_default_na=False)
    f["utc"] = pd.to_datetime(f["sampled"], utc=True)
    f["year"] = f["sampled"].str[:4].astype(int)
    old = pd.read_excel(_p(target, "lims"), sheet_name="2025")
    new = pd.read_excel(_p(target, "lims"), sheet_name="2026-2027")
    new = new[new["status"] == "final"]
    res = pd.concat([
        pd.DataFrame({"year": 2000 + old["Prøvenr"].str[:2].astype(int), "bottle_no": old["Prøvenr"].str[3:].astype(int),
                      "ssc": old["SS mg/l"].astype(float)}),
        pd.DataFrame({"year": new["sample_id"].str[:4].astype(int), "bottle_no": new["sample_id"].str[5:].astype(int),
                      "ssc": new["ssc_mg_l"].astype(float)})])
    f = f.merge(res, on=["year", "bottle_no"], how="left", validate="one_to_one")
    assert f["ssc"].notna().all()
    return f


def station_series(rec, code):
    r = rec[rec["station"] == code].set_index("time_utc")
    full = pd.date_range("2025-01-01", "2027-12-31 23:45", freq="15min", tz="UTC")
    r = r.reindex(full)
    return r


def rising(q, rise=RISE):
    """the river's relative rate of rise per hour from the 15-minute discharge, smoothed over an hour"""
    q = pd.Series(q).interpolate(limit_direction="both").to_numpy()
    rate = np.gradient(q) / 0.25 / q
    return np.convolve(rate, np.ones(4) / 4, "same") > rise


def fit_limb(x, y, ind):
    X = np.c_[np.ones(len(x)), x, ind.astype(float)]
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    bcf = float(np.mean(10 ** (y - X @ b)))
    return b, bcf


def the_call(target, rec=None, S=None, rise=RISE, window_shift_steps=0):
    rec = record(target) if rec is None else rec
    S = samples(target) if S is None else S
    pub = read_report(target)
    out = {}
    for code in sorted(S["station"].unique()):
        r = station_series(rec, code)
        q, T = r["discharge_m3s"].to_numpy(), r["turbidity_fnu"].to_numpy()
        up = rising(q, rise)
        s = S[S["station"] == code]
        k = ((s["utc"].dt.round("15min") - pd.Timestamp("2025-01-01", tz="UTC")) / pd.Timedelta("15min")).astype(int)
        x, y, ind = np.log10(T[k]), np.log10(s["ssc"].to_numpy()), up[k]
        b, bcf = fit_limb(x, y, ind)
        start = pd.Timestamp("2027-01-01", tz="UTC") + pd.Timedelta(minutes=15 * window_shift_steps)
        y27 = (r.index >= start) & (r.index < start + pd.Timedelta(days=365))
        conc = 10 ** (b[0] + b[1] * np.log10(T[y27]) + b[2] * up[y27]) * bcf
        load = float(np.sum(conc * q[y27]) * 900 / 1e6)
        mis = 100 * (pub[code]["load_t"] / load - 1)
        out[code] = {"published_t": pub[code]["load_t"], "estimate_t": load, "misstatement_pct": mis,
                     "verdict": "over" if mis > TOL else ("under" if mis < -TOL else "within"),
                     "rising_samples": int(ind.sum()), "samples": int(len(s)), "coef": [float(v) for v in b],
                     "bcf": bcf}
    return out


def ask_a(target, rec=None):
    """hours in 2025 and 2026 without a usable turbidity reading: no row, fouled or out of the water (the flag letters
    F and M, G and O before the data team's migration), or a reading at the upper end of the sonde's range (1,000 FNU
    on the TS-10 sondes the stations ran until their TS-40W was installed)"""
    rec = record(target) if rec is None else rec
    reg = pd.read_excel(_p(target, "register"))
    swap = {c: pd.Timestamp(d) for c, d in zip(reg["station"], reg["sensor_installed"])}
    log = pd.read_csv(_p(target, "log"), keep_default_na=False)
    sw = log[log["visit"] == "sensor replaced"]
    swap_t = {c: pd.Timestamp("%s %s" % (pd.to_datetime(d, format="%d.%m.%Y").date(), t)).tz_localize("Europe/Oslo").tz_convert("UTC")
              for c, d, t in zip(sw["station"], sw["date"], sw["sonde_out"])}
    out = {}
    end = pd.Timestamp("2027-01-01", tz="UTC")
    for code in sorted(rec["station"].unique()):
        r = station_series(rec, code)
        r = r[r.index < end]
        assert swap[code].date() == swap_t[code].tz_convert("Europe/Oslo").date()
        missing = r["turbidity_fnu"].isna()
        flagged = r["flag"].isin(["F", "M", "G", "O"])
        ceiling = (r.index < swap_t[code]) & (r["turbidity_fnu"] >= 1000.0)
        n = int((missing | flagged | ceiling).sum())
        out[code] = {"intervals": n, "hours": n / 4, "missing": int(missing.sum()), "flagged": int(flagged.sum()),
                     "ceiling": int((ceiling & ~missing & ~flagged).sum())}
    return out


def ask_b(target, lots=None):
    """each station's 2027 samples weighed in a batch that failed a check: blank over 0.5 mg, a control aliquot outside
    90 to 110 per cent of its lot's concentration, the two aliquots more than 10 per cent of their mean apart"""
    lots = read_lots(target) if lots is None else lots
    b = pd.read_csv(_p(target, "batches"))
    f = pd.read_csv(_p(target, "field"), keep_default_na=False)
    f["year"] = f["sampled"].str[:4].astype(int)
    f27 = f[f["year"] == 2027].copy()
    f27["sample_id"] = ["2027-%04d" % n for n in f27["bottle_no"]]
    bt = b.drop_duplicates("batch").set_index("batch")
    conc = lambda m, v: m / v * 1000.0
    c1 = conc(bt["control_1_mass_mg"], bt["control_1_volume_ml"])
    c2 = conc(bt["control_2_mass_mg"], bt["control_2_volume_ml"])
    ref = bt["control_lot"].map(lots)
    fail = ((bt["blank_change_mg"].abs() > 0.5) | ((c1 / ref) < 0.9) | ((c1 / ref) > 1.1) | ((c2 / ref) < 0.9)
            | ((c2 / ref) > 1.1) | ((c1 - c2).abs() / ((c1 + c2) / 2) > 0.10))
    failed = set(bt.index[fail])
    lines = b.merge(f27[["sample_id", "station"]], on="sample_id", how="left", validate="one_to_one")
    assert lines["station"].notna().all()
    lines["failed"] = lines["batch"].isin(failed)
    out = {c: int(lines.loc[lines["station"] == c, "failed"].sum()) for c in sorted(f27["station"].unique())}
    return out, sorted(failed), {k: (float(c1[k]), float(c2[k]), float(ref[k]), float(bt.loc[k, "blank_change_mg"])) for k in bt.index}


def solve(target):
    rec = record(target)
    S = samples(target)
    call = the_call(target, rec, S)
    a = ask_a(target, rec)
    b, failed, qc = ask_b(target)
    return {"call": call, "ask_a": a, "ask_b": b, "failed_batches": failed, "qc": qc}


if __name__ == "__main__":
    import sys
    g = solve(sys.argv[1])
    for c, v in g["call"].items():
        print(c, v["verdict"], "%+.1f" % v["misstatement_pct"], v["published_t"], round(v["estimate_t"]), v["rising_samples"], v["samples"],
              "| A %.2f h" % g["ask_a"][c]["hours"], g["ask_a"][c], "| B", g["ask_b"][c])
    print("failed batches", g["failed_batches"])
