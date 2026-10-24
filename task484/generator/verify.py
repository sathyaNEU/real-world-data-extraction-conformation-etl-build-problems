"""The independent verifier: reads only the shipped bundle (target/), the golden deliverables and figures.json, on its
own code path (pandas for the tables, pdfplumber for the documents, the fixed-width layout read from its own file),
and recomputes the call, every zone figure, the propane component and both asks.

    python3 task484/generator/verify.py
"""
import json
import math
import os
import re
import sys

import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GD = os.path.join(TASK, "golden")
OK, BAD = [0], []


def v(label, cond, detail=""):
    OK[0] += 1
    if not cond:
        BAD.append(label)
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  (" + detail + ")") if detail else ""))


def f(prefix):
    m = [n for n in os.listdir(T) if n.startswith(prefix)]
    assert len(m) == 1, prefix
    return os.path.join(T, m[0])


def pdf(prefix):
    with pdfplumber.open(f(prefix)) as d:
        return "\n".join(p.extract_text() or "" for p in d.pages)


def rnd(x, nd=0):
    k = 10 ** nd
    return math.floor(x * k + 0.5) / k


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    # documents, each with a positive control on the same extractor
    plan, tool, meth = pdf("maintenance_plan"), pdf("montana_rwc_tool"), pdf("heating_survey_2024_25_methods")
    v("pdf: the plan's Table 4-2 reads back", "Table 4-2" in plan and len(plan) > 1000)
    v("pdf: the tool documentation reads back", "Table 1" in tool and "seasonal heating efficiency" in " ".join(tool.lower().split()))
    v("pdf: the survey methods note reads back", "weighted mean" in meth)
    zones = ["Valley Floor North", "Valley Floor South", "East Bench", "West Bench", "Upper Valley"]
    allot = {z: float(re.search(z + r"\s+(\d+\.\d)", plan).group(1)) for z in zones}
    fund = int(re.search(r"USD\s+([\d,]+)", plan).group(1).replace(",", ""))
    flat = " ".join(tool.split())
    cord = float(re.search(r"holds ([\d.]+) million Btu and weighs ([\d.]+) tons", flat).group(1)) * 1e6
    tpc = float(re.search(r"holds ([\d.]+) million Btu and weighs ([\d.]+) tons", flat).group(2))
    pel = float(re.search(r"pellets holds ([\d.]+) million Btu", flat).group(1)) * 1e6
    sec = float(re.search(r"source are ([\d.]+) times", flat).group(1))
    eff, shm, shs, um, us = {}, {}, {}, {}, {}
    for line in tool.splitlines():
        m = re.search(r"(\d{10}) (not a heating appliance|\d+%) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)\s*$", line)
        if m:
            scc = m.group(1)
            eff[scc] = None if m.group(2).startswith("not") else int(m.group(2)[:-1]) / 100.0
            shm[scc], shs[scc], um[scc], us[scc] = (float(x) for x in m.groups()[2:])
    v("pdf: the tool's Table 1 parses six classes", len(eff) == 6, str(sorted(eff)))
    fuel = pd.read_csv(f("heating_fuel_equivalents"))
    lp = fuel[fuel.fuel == "Propane"].iloc[0]
    btu, afue = float(lp.btu_per_unit), float(lp.seasonal_efficiency_pct) / 100.0
    ef = pd.read_csv(f("emission_factors_2023"), dtype={"scc": str})
    pm_lb = ef[(ef.pollutant == "PM2.5") & ef.unit.str.startswith("lb/ton")].set_index("scc").factor.to_dict()
    nox = float(ef[(ef.category == "Commercial/institutional propane combustion") & (ef.pollutant == "NOx")].factor.iloc[0])

    # the registry, the crosswalk, the zones
    xw = pd.read_csv(f("device_code_scc"), dtype=str).set_index("device_code").scc.to_dict()
    reg = pd.read_csv(f("solid_fuel_device_registry"), dtype=str)
    reg["scc"] = reg.device_code.map(xw)
    inst = pd.to_datetime(reg.installed.where(reg.installed.str.len() > 4, reg.installed + "-01-01"))
    gone = pd.to_datetime(reg.status_date)
    inuse25 = (inst <= "2025-10-01") & (gone.isna() | (gone > "2026-04-30"))
    inuse24 = (inst <= "2024-10-01") & (gone.isna() | (gone > "2025-04-30"))
    n = reg[inuse25].groupby(["burn_zone", "scc"]).size()
    v("csv: the registry reads back", len(reg) > 10000 and n.sum() == figs["steps"]["appliances"], "%d in use" % n.sum())
    parcels = pd.read_csv(f("burn_zone_parcels"), dtype=str)
    zone_of = parcels.set_index("geocode").burn_zone.to_dict()
    geo_of = parcels.set_index("situs_address").geocode.to_dict()

    # the survey's estimates, as the methods note states them
    sv = pd.read_csv(f("heating_survey_2024_25_responses"), dtype={"device_id": str})
    conv = {"cords": 1.0, "face cords": 1 / 3.0, "pickup loads": 0.5, "tons": 1.0, "bags (40 lb)": 0.02}
    sv["units"] = sv.amount_burned_2024_25 * sv.unit.map(conv)
    sv = sv.merge(reg[["device_id", "scc"]], on="device_id")
    sv["wu"] = sv.weight * sv.units
    area = sv.groupby("scc").wu.sum() / sv.groupby("scc").weight.sum()
    cell = sv.groupby(["burn_zone", "scc"]).agg(wu=("wu", "sum"), w=("weight", "sum"), k=("units", "size"))
    mean = {}
    for z in zones:
        for s in pm_lb:
            if (z, s) in cell.index and cell.loc[(z, s), "k"] >= 10:
                mean[z, s] = cell.loc[(z, s), "wu"] / cell.loc[(z, s), "w"]
            else:
                mean[z, s] = area[s]
    pellet = [s for s in pm_lb if s == "2104008400"][0]

    def tons(s, u):
        return u if s == pellet else u * tpc

    # the propane accounts: three layouts to one table of season gallons by account
    seasons = {2023: ("2023-10-01", "2024-04-30"), 2024: ("2024-10-01", "2025-04-30"), 2025: ("2025-10-01", "2026-04-30")}
    acct = pd.read_csv(f("wapiti_propane_accounts"), dtype=str)
    acc = [pd.DataFrame(dict(key="W" + acct.account_no, cls=acct.account_class.str[:3].str.upper(), geo=acct.geocode))]
    tk = pd.read_csv(f("wapiti_propane_tickets"), dtype={"account_no": str})
    dl = [pd.DataFrame(dict(key="W" + tk.account_no, date=pd.to_datetime(tk.delivery_date, format="%m/%d/%Y"),
                            gal=tk.gallons))]
    lay = open(f("coldwater_export_record_layout")).read()
    spans = {m.group(3): (int(m.group(1)) - 1, int(m.group(2) or m.group(1))) for m in
             re.finditer(r"col\s+(\d+)(?:-(\d+))?\s+([A-Z-]+)", lay)}
    a_rows, t_rows = [], []
    for line in open(f("coldwater_activity_export")):
        line = line.rstrip("\r\n")
        cut = lambda k: line[spans[k][0]:spans[k][1]].strip()
        if line[0] == "A":
            g = cut("GEOCODE")
            a_rows.append(dict(key="C" + cut("ACCT-NO"), cls="COM" if cut("ACCT-CLASS") == "C" else "RES",
                               geo="-".join([g[0:2], g[2:6], g[6:8], g[8], g[9:11], g[11:13], g[13:17]])))
        else:
            ref = cut("TKT-REF")
            t_rows.append(dict(key="C" + cut("ACCT-NO"), date=pd.to_datetime("20" + ref[1:7], format="%Y%m%d"),
                               posted=pd.to_datetime(cut("TRANS-DT"), format="%Y%m%d"), gal=int(cut("QTY")) / 10.0))
    acc.append(pd.DataFrame(a_rows))
    cw = pd.DataFrame(t_rows)
    v("txt: the Coldwater export reads back on its own layout", len(cw) > 50000 and len(a_rows) > 4000)
    dl.append(cw[["key", "date", "gal"]])
    xl = pd.read_excel(f("halvard_coop_propane"), sheet_name=None, header=2)
    words = {"North": "N", "South": "S", "Street": "ST", "Avenue": "AVE", "Drive": "DR", "Lane": "LN", "Road": "RD",
             "Trail": "TRL", "Loop": "LOOP"}
    mon = dict(Jul=7, Aug=8, Sep=9, Oct=10, Nov=11, Dec=12, Jan=1, Feb=2, Mar=3, Apr=4, May=5, Jun=6)
    seen = {}
    for name, df in xl.items():
        fy = int(name[2:6])
        for _, r in df.iterrows():
            k = "H" + str(r["Member account"])
            seen[k] = dict(key=k, cls="COM" if r["Class"] == "Commercial" else "RES",
                           geo=geo_of.get(" ".join(words.get(w, w) for w in str(r["Service address"]).split()).upper()))
            for m, mi in mon.items():
                if pd.notna(r[m]) and r[m]:
                    dl.append(pd.DataFrame(dict(key=[k], date=[pd.Timestamp(fy if mi >= 7 else fy + 1, mi, 15)],
                                                gal=[float(r[m])])))
    v("xlsx: the cooperative's workbook reads back", len(seen) > 2000 and len(xl) == 3)
    acc.append(pd.DataFrame(list(seen.values())))
    A = pd.concat(acc, ignore_index=True)
    A["zone"] = A.geo.map(zone_of)
    D = pd.concat(dl, ignore_index=True)
    for t, (a, b) in seasons.items():
        D.loc[(D.date >= a) & (D.date <= b), "season"] = t
    G = D.dropna(subset=["season"]).groupby(["key", "season"]).gal.sum().unstack().fillna(0.0)
    R = A[(A.cls == "RES") & A.zone.notna()].set_index("key").join(G)
    heat = {g: s for g, s in reg[inuse25 & inuse24][["geocode", "scc"]].values if eff.get(s)}
    R["scc"] = R.geo.map(heat)

    # the inventory and the call
    pm, extra = {}, {}
    for z in zones:
        Rz = R[(R.zone == z) & R.scc.isna()]
        ratio = Rz[2025].sum() / Rz[2024].sum()
        tot = ex = 0.0
        for s in pm_lb:
            units = mean[z, s] * n.get((z, s), 0)
            trt = R[(R.zone == z) & (R.scc == s)]
            gal = (trt[2024] * ratio - trt[2025]).sum()
            add = gal * btu * afue / ((pel if s == pellet else cord) * eff[s]) if eff.get(s) else 0.0
            tot += tons(s, units + add) * pm_lb[s] / 2000.0
            ex += tons(s, add) * pm_lb[s] / 2000.0
        pm[z], extra[z] = tot, ex
    over = [z for z in zones if pm[z] > allot[z]]
    v("call: the zones over their allotments", over == figs["call"]["over"], str(over))
    v("call: each share of the fund", all(figs["zones"][z]["share"] == (fund // len(over) if z in over else 0) for z in zones))
    for z in zones:
        v("zone %s: %d tons, %d from the propane switch" % (z, rnd(pm[z]), rnd(extra[z])),
          rnd(pm[z]) == figs["zones"][z]["pm"] and rnd(extra[z]) == figs["zones"][z]["extra_pm"])
    det = pd.read_csv(os.path.join(GD, "zone_determinations_2026_27.csv"))
    v("golden csv: every row matches the recomputation", all(
        int(r.pm25_2025_26_tons) == rnd(pm[r.burn_zone]) and (r.exceeded_allotment == "Yes") == (r.burn_zone in over)
        for r in det.itertuples()))

    # ask A: commercial propane by delivery date
    C = A[(A.cls == "COM") & A.zone.notna()].set_index("key").join(G)
    for z in zones:
        g = C[C.zone == z][2025].sum()
        v("ask A %s: %s gallons, %.2f tons of NOx" % (z, format(int(rnd(g / 100) * 100), ","), rnd(g * btu / 1e6 * nox / 2000, 2)),
          int(rnd(g / 100) * 100) == figs["ask_a"][z]["gal"] and abs(rnd(g * btu / 1e6 * nox / 2000, 2) - figs["ask_a"][z]["nox"]) < 1e-9)

    # ask B: the county outside the area on the tool
    acs = pd.read_csv(f("acs5_2019_2023"), dtype=str)
    acs["bg"] = acs.GEO_ID.str[-12:]
    asr = pd.read_csv(f("assessor_housing_units"), dtype={"block_group": str})
    asr["out"] = asr.housing_units.where(asr.maintenance_area.isna(), 0)
    hu = asr.groupby("block_group").agg(out=("out", "sum"), tot=("housing_units", "sum"))
    rel = pd.read_csv(f("tab2020_tab2010"), dtype={"GEOID_BG_20": str, "GEOID_BG_10": str})
    rel = rel.merge(hu, left_on="GEOID_BG_10", right_index=True)
    rel["o"] = rel.HU_20_OVERLAP * rel.out / rel.tot
    share = rel.groupby("GEOID_BG_20").o.sum() / rel.groupby("GEOID_BG_20").HU_20_OVERLAP.sum()
    main_ = (acs.B25040_008E.astype(int) * acs.bg.map(share).fillna(0)).sum()
    for s in pm_lb:
        app = main_ * shm[s] + main_ * sec * shs[s]
        p25 = tons(s, main_ * shm[s] * um[s] + main_ * sec * shs[s] * us[s]) * pm_lb[s] / 2000.0
        v("ask B %s: %d appliances, %.1f tons" % (s, rnd(app), rnd(p25, 1)),
          rnd(app) == figs["ask_b"][s]["app"] and abs(rnd(p25, 1) - figs["ask_b"][s]["pm"]) < 1e-9)
    print("\n%d verified, %d failed%s" % (OK[0], len(BAD), (": " + "; ".join(BAD)) if BAD else ""))
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
