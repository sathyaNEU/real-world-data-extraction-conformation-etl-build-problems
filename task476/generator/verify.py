"""An independent verifier: recompute the call, every well's water year volume, the static depths and the energy
charges from target/ with pandas and its own parsing, and compare with golden/. Shares no code with golden.py."""
import csv
import io
import math
import os
import re
import zipfile

import numpy as np
import pandas as pd
import pdfplumber

LA = "America/Los_Angeles"


def _text(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join(p.extract_text() or "" for p in pdf.pages)


def main(target, gdir):
    reg = pd.read_excel(os.path.join(target, "ranch", "ochre_flats_well_register.xlsx"), sheet_name="Wells", dtype=str)
    reg = reg.set_index("Well")
    # power
    raw = open(os.path.join(target, "power", "vrp_usage_export_2025-09-01_2026-03-31.csv"), encoding="utf-8").read()
    body = raw[raw.index("SERVICE AGREEMENT"):]
    old = pd.read_csv(io.StringIO(body), dtype={"SERVICE AGREEMENT": str})
    old["rank"] = old.groupby(["SERVICE AGREEMENT", "DATE", "START TIME"]).cumcount()
    loc = pd.to_datetime(old["DATE"] + " " + old["START TIME"])
    amb = old["rank"].map({0: True, 1: False})
    old["start"] = loc.dt.tz_localize(LA, ambiguous=amb.values, nonexistent="raise").dt.tz_convert("UTC")
    old["mins"] = 60
    old["kwh"] = old["USAGE"].astype(float)
    sa_o = {v: k for k, v in reg["Electric SA (to Mar 31, 2026)"].items()}
    old["well"] = old["SERVICE AGREEMENT"].map(sa_o)
    new = pd.read_csv(os.path.join(target, "power", "vrp_interval_data_2026-04-01_2026-10-31.csv"))
    new["start"] = pd.to_datetime(new["interval_start"], utc=True)
    new["mins"] = new["interval_seconds"] // 60
    new["kwh"] = new["energy_wh"] / 1000.0
    sa_n = {v: k for k, v in reg["Electric SA (from Apr 1, 2026)"].items()}
    new["well"] = new["service_agreement_id"].map(sa_n)
    pw = pd.concat([old[["well", "start", "mins", "kwh"]], new[["well", "start", "mins", "kwh"]]], ignore_index=True)
    pw["local"] = pw["start"].dt.tz_convert(LA)
    wy = (pw["local"] >= pd.Timestamp("2025-10-01", tz=LA)) & (pw["local"] < pd.Timestamp("2026-10-01", tz=LA))
    # tests
    tests = {}
    for f in sorted(os.listdir(os.path.join(target, "pump_tests"))):
        t = _text(os.path.join(target, "pump_tests", f))
        sa = re.search(r"(?:Electric account|Utility SA) (\d{10})", t).group(1)
        well = sa_o.get(sa)
        if well is None:
            continue
        g = lambda pat: float(re.search(pat, t).group(1).replace(",", ""))
        if "GUTIERREZ" in t:
            rec = dict(pwl=g(r"Pumping water level \(ft\) ([\d.]+)"), th=g(r"Total head \(ft\) ([\d.]+)"),
                       ope=g(r"Overall plant efficiency \(%\) ([\d.]+)") / 100, rate=g(r"kWh per acre-foot ([\d,]+)"))
        else:
            rec = dict(pwl=g(r"PWL, ft bgs ([\d.]+)"), th=g(r"TDH, ft ([\d.]+)"), ope=g(r"OPE, % ([\d.]+)") / 100,
                       rate=g(r"Energy, kWh/AF ([\d.]+)"))
        tests[well] = rec
    # vented loggers by serial
    lv = {}
    for w in reg.index:
        if "vented" not in reg.loc[w, "Level logger"]:
            continue
        s = reg.loc[w, "Logger S/N"]
        lines = open(os.path.join(target, "levels", "%s.csv" % s), encoding="utf-8").read().splitlines()
        i0 = [i for i, l in enumerate(lines) if l.startswith("Date Time")][0]
        df = pd.read_csv(io.StringIO("\n".join(lines[i0:])))
        ts = pd.to_datetime(df.iloc[:, 0]).dt.tz_localize("Etc/GMT+8").dt.tz_convert("UTC")
        lv[w] = pd.Series(df.iloc[:, 1].values - float(reg.loc[w, "MP height above ground (ft)"]), index=ts)
    vol = {}
    for w in reg.index:
        if reg.loc[w, "Flow meter"] != "none":
            continue
        t = tests[w]
        p = pw[(pw["well"] == w) & wy & (pw["kwh"] > 0)].copy()
        s = lv[w]
        z = []
        for st, mins in zip(p["start"], p["mins"]):
            idx = pd.date_range(st, st + pd.Timedelta(minutes=int(mins)), freq="15min")
            vals = s.reindex(idx).dropna()
            z.append(vals.mean() if len(vals) else t["pwl"])
        p["z"] = z
        p["af"] = p["kwh"] * t["ope"] / (1.0241 * (t["th"] + p["z"] - t["pwl"]))
        vol[w] = p["af"].sum()
    # meters
    rd = pd.read_excel(os.path.join(target, "ranch", "totalizer_reads_wy2026.xlsx"), sheet_name="Reads")
    per = {"acre-feet": 1.0, "gal x 1000": 325.851, "gal x 100": 3258.51}
    for w, grp in rd.groupby("Well"):
        grp = grp.sort_values(["Read date", "Read time"])
        acc, last, sn_last, at = 0.0, None, None, {}
        for _, r in grp.iterrows():
            if last is not None and r["Meter S/N"] == sn_last:
                dlt = float(r["Totalizer"]) - last
                if dlt < 0:
                    dlt += 1_000_000
                acc += dlt / per[r["Units"]]
            last, sn_last = float(r["Totalizer"]), r["Meter S/N"]
            if str(r["Read date"]).endswith("-01") and (not isinstance(r["Note"], str)):
                at[str(r["Read date"])[:7]] = acc
        vol[w] = at["2026-10"] - at["2025-10"]
    rep = {w: int(round(v)) for w, v in vol.items()}
    nt = _text(os.path.join(target, "agency", "sallow_plains_gsa_wy2026_allocation_notice.pdf"))
    alloc = sum(float(m.group(1)) for m in re.finditer(r"^\d{3}-\d{3}-\d{2} [\d.]+ [\d.]+ [\d.]+ ([\d.]+)$", nt, re.M))
    carry = float(re.search(r"is (\d+) acre-feet\. The water", nt.replace("\n", " ")).group(1))
    total = sum(rep.values())
    excess = total - (alloc + carry)
    purchase = int(math.ceil(excess / 50.0) * 50) if excess > 0 else 0
    # compare with the golden return
    gr = list(csv.DictReader(open(os.path.join(gdir, "wy2026_extraction_return.csv"), encoding="utf-8")))
    byid = {reg.loc[w, "Agency well ID"]: w for w in reg.index}
    diffs = [abs(int(r["wy2026_af"]) - rep[byid[r["agency_well_id"]]]) for r in gr]
    ok = max(diffs) <= 1
    print("%s  verify: every well's water year volume within 1 AF of the golden (largest %d)" % ("PASS" if ok else "FAIL",
                                                                                                  max(diffs)))
    from docx import Document
    memo = " ".join(p.text for p in Document(os.path.join(gdir, "transfer_purchase_memo.docx")).paragraphs)
    m = re.search(r"Buy ([\d,]+) acre-feet", memo)
    ok2 = m is not None and int(m.group(1).replace(",", "")) == purchase
    print("%s  verify: the memo's purchase %s equals the recomputed %d (ranch %d, available %.1f)" % (
        "PASS" if ok2 else "FAIL", m.group(1) if m else None, purchase, total, alloc + carry))
    # energy charges, April to September 2026, recomputed from the schedule and the letter in pandas
    tt = _text(os.path.join(target, "power", "vrp_agricultural_tou_schedules_2026.pdf"))
    rates = {}
    for line in tt.splitlines():
        tok = line.split()
        if len(tok) >= 4 and tok[0].startswith("AG-") and tok[1] in ("Summer", "Winter"):
            nums = [float(x) for x in tok[2:]]
            keys = ["peak", "part", "off"] if tok[1] == "Summer" else ["part", "off"]
            rates[(tok[0], tok[1].lower())] = dict(zip(keys, nums))
    lt = _text(os.path.join(target, "power", "vrp_rate_change_confirmation_2026-05-14.pdf"))
    moved = set(re.findall(r"(SA-\d{7}) .*AG-2T AG-3T June 1, 2026", lt))
    hol = {pd.Timestamp("2026-05-25").date(), pd.Timestamp("2026-07-03").date(), pd.Timestamp("2026-09-07").date()}
    nw = new.copy()
    nw["local"] = nw["start"].dt.tz_convert(LA)
    nw = nw[(nw["local"] >= pd.Timestamp("2026-04-01", tz=LA)) & (nw["local"] < pd.Timestamp("2026-10-01", tz=LA))]
    mins = nw["local"].dt.hour * 60 + nw["local"].dt.minute
    summer = nw["local"].dt.month.between(6, 9)
    wk = (nw["local"].dt.weekday < 5) & ~nw["local"].dt.date.isin(hol)
    per = np.where(summer & wk & (mins >= 720) & (mins < 1080), "peak",
                   np.where(wk & ((summer & (((mins >= 510) & (mins < 720)) | ((mins >= 1080) & (mins < 1290)))) |
                                  (~summer & (mins >= 510) & (mins < 1290))), "part", "off"))
    nw["per"], nw["season"] = per, np.where(summer, "summer", "winter")
    cur = reg["Rate schedule"].to_dict()
    sa_now = reg["Electric SA (from Apr 1, 2026)"].to_dict()
    sch = [("AG-2T" if (sa_now[w] in moved and lc < pd.Timestamp("2026-06-01", tz=LA)) else cur[w])
           for w, lc in zip(nw["well"], nw["local"])]
    nw["rate"] = [rates[(s_, se)][p_] for s_, se, p_ in zip(sch, nw["season"], nw["per"])]
    usd = (nw["kwh"] * nw["rate"]).groupby(nw["well"]).sum()
    doc = Document(os.path.join(gdir, "transfer_purchase_memo.docx"))
    memo_usd = {}
    for row in doc.tables[0].rows[1:]:
        c = [x.text for x in row.cells]
        if c[0].startswith("W-"):
            memo_usd[c[0].split()[0]] = int(c[4].replace(",", ""))
    worst = max(abs(memo_usd[w] - int(round(usd[w]))) for w in memo_usd)
    ok3 = worst == 0 and len(memo_usd) == len(reg)
    print("%s  verify: every well's April to September energy charge equals the recomputed one to the dollar "
          "(largest gap %d)" % ("PASS" if ok3 else "FAIL", worst))
    return ok and ok2 and ok3


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    raise SystemExit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
