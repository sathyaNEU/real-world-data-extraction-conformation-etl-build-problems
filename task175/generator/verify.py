"""Independent verifier: reads only the bundle (target/) and the goldens, on its own code path (pandas, pypdf and a
Poisson GLM by iteratively reweighted least squares), and recomputes the call, the critical components and every ask
figure against generator/figures.json.

    python3 verify.py <target>"""
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def ok(label, cond, detail=""):
    print(("  ok   " if cond else "  FAIL ") + label + ("  " + detail if detail else ""))
    if not cond:
        FAIL.append(label)


def pdf(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


MON = {m: i + 1 for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split())}


def main(target):
    task = os.path.dirname(os.path.abspath(target))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    sched = pdf(os.path.join(target, "uep_program_schedule_rev12_2026.pdf"))
    conv = pdf(os.path.join(target, "revenue_sufficiency_forecast_conventions_fy2027.pdf"))
    ok("V0 positive control: the schedule and the conventions read back", "Lines accepted is the date" in sched
       and "calendar 2026 level" in conv)
    areas = {}
    for m in re.finditer(r"((?:Southwest|Central|North|Northwest) \d) (\d) ((?:\d+, )*\d+) ([\d,]+) (?:scheduled |planned )?(\d{1,2} \w{3} \d{4}|\d{4})", sched):
        nm, ph, units, lots, when = m.groups()
        acc = None
        if " " in when:
            d, mo, y = when.split()
            acc = pd.Timestamp(int(y), MON[mo], int(d))
        areas[nm] = (ph, [int(x) for x in units.split(", ")], acc)
    core = re.search(r"plat units (\d+) to (\d+)", sched)
    core_units = set(range(int(core.group(1)), int(core.group(2)) + 1))
    ok("V1 the schedule lists 22 areas", len(areas) == 22, str(len(areas)))
    unit_area = {u: nm for nm, (_, us, _) in areas.items() for u in us}
    roll = pd.read_csv(os.path.join(target, "pa_parcel_extract_2026.csv"), dtype=str, keep_default_na=False)
    roll["unit"] = roll.LEGAL_DESC.str.extract(r"UNIT (\d+)")[0].astype(int)
    roll["area"] = roll.unit.map(lambda u: "Core" if u in core_units else unit_area[u])
    roll["canal"] = (roll.WATERFRONT == "Y").astype(int)
    roll["yb"] = pd.to_numeric(roll.YR_BUILT, errors="coerce").fillna(0).astype(int)
    num = roll.SITE_ADDR.str.split(" ", n=1).str[0].astype(int)
    roll["seg"] = roll.SITE_ADDR.str.split(" ", n=1).str[1] + "|" + (num // 100).astype(str)
    roll = roll.reset_index(drop=True)
    by_addr = pd.Series(roll.index, index=roll.SITE_ADDR)
    by_strap = pd.Series(roll.index, index=roll.STRAP)
    # permits
    leg = pd.read_csv(os.path.join(target, "bldg_permits_legacy_2008_2018.csv"), dtype=str, keep_default_na=False)
    new = pd.read_excel(os.path.join(target, "bldg_permits_2019_2026.xlsx"), dtype={"Legacy Permit #": str})
    carried = set(new["Legacy Permit #"].dropna())
    leg = leg[(leg.PERMIT_TYPE == "RES NEW SFR") & ~leg.PERMIT_NBR.isin(carried)].copy()
    abbr = {"STREET": "ST", "TERRACE": "TER", "PLACE": "PL", "LANE": "LN", "COURT": "CT"}
    leg["addr"] = leg.SITE_ADDR.map(lambda a: " ".join(a.split()[:-1] + [abbr.get(a.split()[-1], a.split()[-1])]))
    leg["lot"] = leg.addr.map(by_addr)
    leg["iss"] = pd.to_datetime(leg.ISSUE_DT, format="%m/%d/%Y")
    leg["co"] = pd.to_datetime(leg.FINAL_DT, format="%m/%d/%Y", errors="coerce")
    new = new[new["Work Class"] == "Residential New Single Family"].copy()
    new["lot"] = new["Parcel ID"].map(by_strap)
    new["iss"] = pd.to_datetime(new["Issued Date"])
    new["co"] = pd.to_datetime(new["CO Issued"])
    pm = pd.concat([leg[["lot", "iss", "co"]], new[["lot", "iss", "co"]]]).sort_values(["lot", "iss"]).drop_duplicates("lot")
    ok("V2 every single-family permit placed on a lot", pm.lot.notna().all(), "%d permits" % len(pm))
    roll["iss"] = pd.NaT
    roll.loc[pm.lot.values, "iss"] = pm.iss.values
    roll["co"] = pd.NaT
    roll.loc[pm.lot.values, "co"] = pm.co.values
    roll["pre"] = (roll.yb > 0) & roll.iss.isna()
    # seasonal shares from permits on lots served the whole year
    def acc_of(a):
        return pd.NaT if a == "Core" else areas[a][2]
    roll["acc"] = roll.area.map(acc_of)
    full = roll[roll.iss.notna() & ((roll.area == "Core") | (roll.acc.dt.year < roll.iss.dt.year))]
    season = full.iss.dt.month.value_counts().sort_index().values.astype(float)
    season /= season.sum()
    cum = np.r_[0, np.cumsum(season)]

    def frac(d):   # seasonal weight of the year before day d
        dim = d.days_in_month
        return cum[d.month - 1] + season[d.month - 1] * (d.day - 1) / dim

    rows = []
    for y in range(2008, 2027):
        jan1 = pd.Timestamp(y, 1, 1)
        done = ((roll.yb > 0) & (roll.yb < y)) | (roll.co < jan1)
        homes = done.groupby(roll.seg).transform("sum")
        vac = ~roll.pre & (roll.iss.isna() | (roll.iss >= jan1))
        served = (roll.area == "Core") | (roll.acc.dt.year <= y)
        sel = roll[vac & served].copy()
        sel["n"] = homes[sel.index]
        start = sel.acc.map(lambda a: 0.0 if pd.isna(a) or a.year < y else frac(a))
        end = sel.iss.map(lambda d: 1.0 if pd.isna(d) or d.year > y else frac(d) + season[d.month - 1] / d.days_in_month)
        ev = sel.iss.map(lambda d: (not pd.isna(d)) and d.year == y) & ((sel.area == "Core") | (sel.iss >= sel.acc) | sel.acc.isna())
        sel["exp"] = (end - start).clip(lower=1e-6)
        sel["ev"] = ev.astype(float)
        sel["y"] = y
        rows.append(sel[["y", "canal", "n", "exp", "ev"]])
    ly = pd.concat(rows, ignore_index=True)
    edges = [1, 2, 3, 4, 6, 9, 13, 18]
    ly["bin"] = np.digitize(ly.n, edges)
    # Poisson GLM: log mu = log exp + year + canal + bin, by IRLS
    X = pd.get_dummies(ly.y.astype(str), prefix="y").astype(float)
    X["canal"] = ly.canal.astype(float)
    for b in range(1, len(edges) + 1):
        X["b%d" % b] = (ly.bin == b).astype(float)
    Xv = X.values
    off = np.log(ly.exp.values)
    yv = ly.ev.values
    beta = np.zeros(Xv.shape[1])
    beta[:19] = np.log(max(yv.sum() / ly.exp.sum(), 1e-6))
    for _ in range(40):
        eta = Xv @ beta + off
        mu = np.exp(eta)
        z = eta - off + (yv - mu) / mu
        W = mu
        A = Xv.T @ (Xv * W[:, None])
        beta = np.linalg.solve(A, Xv.T @ (W * z))
    coef = dict(zip(X.columns, beta))
    # forecast
    jan27 = pd.Timestamp(2027, 1, 1)
    done = ((roll.yb > 0) & (roll.yb < 2027)) | (roll.co < jan27)
    homes = done.groupby(roll.seg).transform("sum")
    fw = roll[roll.area.isin(["North 6", "North 7", "Northwest 3"]) & ~roll.pre & roll.iss.isna()].copy()
    fw["bin"] = np.digitize(homes[fw.index], edges)
    uns_area = roll.area.map(lambda a: a != "Core" and (pd.isna(areas[a][2]) or areas[a][2].year > 2026))
    nu = du = 0
    for y in (2023, 2024, 2025, 2026):
        vacu = uns_area & (roll.yb == 0) & (roll.iss.isna() | (roll.iss.dt.year >= y))
        du += vacu.sum()
        nu += (uns_area & (roll.iss.dt.year == y)).sum()
    u = nu / du
    out = {}
    for nm in ["North 6", "North 7", "Northwest 3"]:
        s = fw[fw.area == nm]
        a = areas[nm][2]
        wserved = 1 - frac(a)
        lam = np.exp(coef["y_2026"] + coef["canal"] * s.canal + s.bin.map(lambda b: coef.get("b%d" % b, 0.0)))
        out[nm] = float((1 - np.exp(-(lam * wserved + u * (1 - wserved)))).sum())
    tot = sum(out.values())
    ok("V3 the total recomputes (expected distinct lots, nearest 50)", int(50 * round(tot / 50.0)) == fig["call_total_permits_2027"],
       "%.2f" % tot)
    ok("V4 the total sits 8 or more from its bin edges", 25 - abs(tot - 50 * round(tot / 50.0)) >= 8)
    ok("V5 vacant lots recompute", len(fw) == fig["cc1_vacant_lots_total"] and all(
        int((fw.area == nm).sum()) == fig["cc1_vacant_lots_" + nm.lower().replace(" ", "")] for nm in out), str(len(fw)))
    ok("V6 lots on streets with no home recompute", int((homes[fw.index] == 0).sum()) == fig["cc2_vacant_lots_subset_total"])
    # asks
    prem = pd.read_csv(os.path.join(target, "cis_premise_extract_20261231.csv"), dtype=str, keep_default_na=False)
    acct = pd.read_csv(os.path.join(target, "cis_account_history_20261231.csv"), dtype=str)
    ami = pd.read_csv(os.path.join(target, "ami_headend_installs_fy25_fy26.csv"), dtype=str)
    sa = prem.SVC_ADDR.map(lambda a: " ".join(a.split()[:-1] + [abbr.get(a.split()[-1], a.split()[-1])]))
    prem["lot"] = np.where(prem.PARCEL_ID != "", prem.PARCEL_ID.map(by_strap), sa.map(by_addr))
    ok("V7a every premise placed on a lot", prem.lot.notna().all())
    prem["phase"] = prem.lot.map(lambda i: "Core" if roll.area[int(i)] == "Core" else areas[roll.area[int(i)]][0])
    acct["lot"] = acct.PREMISE_ID.map(prem.set_index("PREMISE_ID").lot)
    first = acct.groupby("lot").SVC_START.min()
    ami["lot"] = ami.PREMISE_ID.map(prem.set_index("PREMISE_ID").lot)
    ami["d"] = pd.to_datetime(ami.INSTALL_DATE)
    firstset = ami.groupby("lot").d.transform("min")
    ami = ami[(ami.d >= "2025-10-01") & (ami.d < "2026-10-01")].copy()
    ami["first"] = ami.lot.map(first)
    newc = ami[(ami.d == firstset[ami.index]) & (ami["first"].isna() | (pd.to_datetime(ami["first"]) >= ami.d))].copy()
    newc["phase"] = newc.lot.map(lambda i: "Core" if roll.area[int(i)] == "Core" else areas[roll.area[int(i)]][0])
    cnt = newc.groupby("phase").size()
    good = all(int(cnt.get(ph, 0)) == fig["ask_connections_fy2026_phase" + ph] for ph in ["1", "2", "3", "4"])
    ok("V7 every fiscal 2026 phase connection total recomputes", good)
    fees = pd.read_excel(os.path.join(target, "capacity_fee_receipts_fy2026.xlsx"))
    allp = pd.read_excel(os.path.join(target, "bldg_permits_2019_2026.xlsx"), dtype={"Legacy Permit #": str})
    lot_of = allp.set_index("Permit Number")["Parcel ID"].map(by_strap)
    rec = fees.drop_duplicates(["Receipt No", "Payer"]).copy()
    rec["q"] = ((pd.to_datetime(rec["Receipt Date"]).dt.month - 10) % 12) // 3 + 1
    rec["phase"] = rec["Permit No"].map(lot_of).map(lambda i: "Core" if roll.area[int(i)] == "Core" else areas[roll.area[int(i)]][0])
    fq = rec.groupby(["phase", "q"]).Amount.sum()
    ok("V8 every fiscal 2026 fee cell recomputes", all(int(round(fq[(ph, q)])) == fig["ask_capacity_fees_fy2026_%s_q%d" % (
        "core" if ph == "Core" else "phase" + ph, q)] for ph in ["Core", "1", "2", "3", "4"] for q in (1, 2, 3, 4)))
    # goldens read back
    gx = os.path.join(task, "golden", "uep_2027_permit_forecast.xlsx")
    wb = pd.read_excel(gx, sheet_name=None, header=None)
    flat = " ".join(str(v) for df in wb.values() for v in df.values.ravel() if str(v) != "nan")
    ok("V9 the golden workbook carries the call and every ask figure",
       all(str(fig[k]) in flat for k in fig if k.startswith(("call_", "ask_", "cc"))))
    ok("V10 the golden chart exists", os.path.getsize(os.path.join(task, "golden", "fy2026_capacity_fees.png")) > 20000)
    print("\n%d failed" % len(FAIL))
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
