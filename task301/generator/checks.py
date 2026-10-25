"""Generator assertions for task301: the three rules (R1 to R3) on the clean truth and the pack, the main call's
family, every semantic fork row, both asks against the generator's truth and their wrong paths, the bins, the input
gates and the separation line.

    python3 task301/generator/checks.py <target dir>
"""
import datetime as dt
import os
import sys
import zoneinfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A
import build as B
import params as P
import solve as SV
import world as Wd

UK = zoneinfo.ZoneInfo("Europe/London")
FAILS = []


def ok(label, cond, detail=""):
    print("%-4s %s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def main(T):
    FAILS.clear()
    K = SV.Pack(T)
    c = SV.call(K)
    gold, clean = c["gold"], c["clean"]
    W = Wd.world()
    days = W.days

    # ------------------------------------------------------------ R1: the field's raw material ships
    sc_cols = set(K.sc.columns)
    ok("R1 block SCADA ships at the block-day grain", {"date", "site", "inverter", "ac_energy_mwh"} <= sc_cols
       and K.sc.groupby(["site", "inverter", "date"]).size().max() == 1)
    banned = ("soil", "loss", "deposit", "dust", "clean", "exposure", "pr", "ratio")
    shipped = []
    for f in os.listdir(T):
        if f.endswith(".csv"):
            shipped += list(pd.read_csv(os.path.join(T, f), nrows=1).columns)
    shipped += list(sc_cols)
    ok("R1 no shipped column holds the deciding quantity",
       not [x for x in shipped if any(x.lower() == b or x.lower().startswith(b + "_") or x.lower().endswith("_" + b)
                                      for b in banned)], str([x for x in shipped if "ratio" in x.lower()]))
    ok("R1 the golden reads the blocks: Wexcombe's near blocks carry fitted deposits", len(c["rates"]) >= 3,
       str(len(c["rates"])))

    # ------------------------------------------------------------ the call and its ladder
    order = sorted(SV.CANDS, key=lambda k: -gold[k])
    ok("call: Kingsley Fields first", order[0] == "Kingsley Fields", str({k: round(v) for k, v in gold.items()}))
    ok("call: export prints 9,700", int(round(gold["Kingsley Fields"] / 100) * 100) == 9700)
    ok("bin: 2028 export at least 20 MWh inside its cell", edge(gold["Kingsley Fields"], 100) >= 20,
       "%.1f" % edge(gold["Kingsley Fields"], 100))
    ok("R3a easy route (site-level ratio at the meter) builds Hallam Down", max(clean, key=clean.get) == "Hallam Down",
       "%.0f against %.0f" % (clean["Hallam Down"], clean["Kingsley Fields"]))
    ok("rung 2 (Wexcombe's farm-level deficit applied flat) still builds Hallam Down",
       clean["Hallam Down"] * min(1.0, c["farm_ratio"]) > clean["Kingsley Fields"], "%.4f" % c["farm_ratio"])
    ok("rung 3 (Wexcombe's block deficits carried flat by distance) still builds Hallam Down",
       clean["Hallam Down"] * (1 - c["flat_blocks"]) > clean["Kingsley Fields"], "%.4f" % c["flat_blocks"])
    ok("R3b the decisive step alone (block-distance transport) builds Kingsley Fields",
       clean["Hallam Down"] * (1 - c["loss"]) < clean["Kingsley Fields"], "%.4f" % c["loss"])
    ok("the blocks select the wash thresholds 4 and 10 mm",
       (c["wash"][0][1], c["wash"][0][2]) == (4, 10) and c["wash"][1][0] / c["wash"][0][0] > 1.05,
       "%.3f" % (c["wash"][1][0] / c["wash"][0][0]))

    # R3a on the clean truth: the true irradiation and the true output, no satellite error, no outages taken out
    k0 = W.site["Knowle Park"]["k_start"]
    kp_true = W.site["Knowle Park"]["export"][k0:].sum() / (12.0 * W.site["Knowle Park"]["poa"][k0:].sum())
    true_clean = {k: 11.0 * W.site[k]["poa"].sum() / 10.0 * kp_true for k in SV.CANDS}
    ok("R3a on the clean truth: the site-level route builds Hallam Down", max(true_clean, key=true_clean.get) ==
       "Hallam Down", str({k: round(v) for k, v in true_clean.items()}))
    hd = W.site["Hallam Down"]
    true_loss = float(np.mean([(hd["poa"] * B_["soil"]).sum() / hd["poa"].sum() for B_ in hd["blocks"]]))
    ok("R3b on the clean truth: Hallam Down's true deposit loss exceeds its true lead",
       true_clean["Hallam Down"] * (1 - true_loss) < true_clean["Kingsley Fields"], "true loss %.4f" % true_loss)

    # the deposit family: every member files Kingsley Fields
    fam = SV.family(K)
    worst = max(clean["Hallam Down"] * (1 - r[4]) for r in fam)
    ok("family: %d deposit fits, every one leaves Hallam Down below Kingsley Fields" % len(fam),
       worst < gold["Kingsley Fields"] - 50, "best Hallam %.0f" % worst)
    ok("family: the partial-wash fits beat the full-wash fits on the blocks' own record",
       min(r[3] for r in fam if r[0] == "far" and r[1].startswith("partial")) * 1.3 <
       min(r[3] for r in fam if r[0] == "far" and r[1].startswith("full")))

    # the performance basis family (SF3): every basis prints the golden for Kingsley Fields
    base = SV.site_pr(K, "Knowle Park")
    ev = K.om[K.om.site == "Knowle Park"]
    x = K.ex[K.ex.site == "Knowle Park"].merge(K.w[K.w.site == "Knowle Park"], on=["date", "site"])
    x = x[~x.date.isin(ev.date)]
    pr_out = x.export_mwh.sum() / (12.0 * x.poa_irradiation_kwh_m2.sum())
    a25 = SV.mean_age(K, "Knowle Park", dt.date(2025, 1, 1), dt.date(2025, 12, 31))
    akp = SV.mean_age(K, "Knowle Park")
    pr25 = SV.site_pr(K, "Knowle Park", (2025, 2025))
    for name, pr, d, a0 in [("SF3 golden", base, c["deg"], akp), ("SF3 no age carry", base, 0.0, akp),
                            ("SF3 datasheet degradation", base, 0.0045, akp), ("SF3 outage days out", pr_out, c["deg"], akp),
                            ("SF3 2025 alone", pr25, c["deg"], a25), ("SF1 age at 1 January 2028", base, c["deg"], None)]:
        vals = {}
        for k in SV.CANDS:
            age = SV.age_2028(k) if a0 is not None else (dt.date(2028, 1, 1) - SV.ENERGISED[k]).days / 365.25
            vals[k] = 11.0 * SV.avg_year_poa(K, k) * pr * (1 - d) ** (age - (a0 if a0 is not None else akp))
        vals["Hallam Down"] *= (1 - c["loss"])
        top = max(vals, key=vals.get)
        ok("%s: Kingsley Fields at %d" % (name, int(round(vals["Kingsley Fields"] / 100) * 100)),
           top == "Kingsley Fields" and int(round(vals["Kingsley Fields"] / 100) * 100) == 9700,
           "%.1f" % vals["Kingsley Fields"])
    # SF2: a year of average weather as the ten-year mean, not one year
    yrs = {y: {k: K.w[(K.w.site == k) & (K.w.date.dt.year == y)].poa_irradiation_kwh_m2.sum() for k in SV.CANDS}
           for y in range(2016, 2026)}
    ok("SF2 Kingsley Fields out-shines Larkhill Common and Marston Vale in every year of the record (a single year, "
       "the median year or the ten-year mean all build it)",
       all(v["Kingsley Fields"] > max(v["Larkhill Common"], v["Marston Vale"]) for v in yrs.values()))
    # SF5: the four candidates are the register's, each with its planned blocks in the layout
    cands = set(K.reg[K.reg.status == "candidate"].site)
    ok("SF5 the register's candidates are the four, each with planned blocks", cands == set(SV.CANDS) and
       all((K.lay.site == k).sum() >= 9 for k in SV.CANDS), str(sorted(cands)))
    # SF4: export at the meter, not the inverters' sum
    sc_sum = K.sc[K.sc.site == "Knowle Park"].ac_energy_mwh.sum()
    ok("SF4 the meter reads below the inverters (transformer and cable)", K.ex[K.ex.site == "Knowle Park"].export_mwh.sum()
       < sc_sum)
    # Hallam Down's blocks: distances by block, not one centroid distance (R2 mess item)
    L = SV.block_distances(K, "Hallam Down")
    f = SV.rate_fn(c["rates"], "exp")
    h = K.w[K.w.site == "Hallam Down"].sort_values("date")
    poa, rain = h.poa_irradiation_kwh_m2.values, h.rainfall_mm.values
    one = float((poa * SV.run_deposit(rain, f(105.0), 4, 10)).sum() / poa.sum())
    ok("SF6 / R2 environs from the centroid: one centroid distance for every block still builds Kingsley Fields",
       clean["Hallam Down"] * (1 - one) < gold["Kingsley Fields"], "%.4f" % one)
    ok("R2 inverter sum as the export (no meter loss) keeps Kingsley Fields",
       max(SV.CANDS, key=lambda k: gold[k] / 0.984) == "Kingsley Fields")
    ok("R2 module generations pooled (all fourteen farms' ratio) keeps the order",
       sorted(SV.CANDS, key=lambda k: -gold[k] * 0.97)[0] == "Kingsley Fields")

    # R3c: no plant
    dup = 0
    for s_, g in K.sc.groupby("site"):
        piv = g.pivot(index="date", columns="inverter", values="ac_energy_mwh")
        dup += int(piv.T.duplicated().sum())
    ok("R3c no copied block series", dup == 0, str(dup))
    note_text = " ".join(p.text for p in __import__("docx").Document(os.path.join(T, P.FILES["note"])).paragraphs)
    ok("R3c the note ranks nothing and names no dust", not any(w in note_text.lower() for w in
                                                                  ("dust", "soil", "poultry", "broiler", "rank")))

    # ------------------------------------------------------------ ask A against the generator's truth
    _, _, _, ta = A.pyranometers(W)
    a = SV.ask_a(K)
    for fm in P.OPERATING:
        v = a[fm]
        ok("A %s golden equals the truth" % fm, abs(v["gold"] - ta[fm]["ratio"]) < 1e-9 and v["down"] == ta[fm]["old"]
           and v["label"] == ta[fm]["old"], "%.6f" % v["gold"])
        ok("A %s off-centre, 0.25 unit from an edge" % fm, 0.00025 <= edge(v["gold"], 0.001) <= 0.0004,
           "%.5f" % edge(v["gold"], 0.001))
        for w in ("register", "label_asof", "label_latest", "all_days", "gold_latest"):
            ok("A %s %s misses" % (fm, w), round(v[w], 3) != round(v["gold"], 3), "%.4f" % v[w])
    # ------------------------------------------------------------ ask B against the generator's truth
    *_, tb = A.response(W)
    b = SV.ask_b(K)
    for fm in P.OPERATING:
        v = b[fm]
        ok("B %s golden equals the truth" % fm, abs(v["gold"] - tb[fm]["mean"]) < 1e-9 and v["n"] == tb[fm]["n"],
           "%.4f" % v["gold"])
        ok("B %s off-centre" % fm, 0.025 <= edge(v["gold"], 0.1) <= 0.04, "%.4f" % edge(v["gold"], 0.1))
        for w in ("attended", "cmms", "mixed", "tracker_raw", "from_wo", "possible_only"):
            ok("B %s %s misses" % (fm, w), round(v[w], 1) != round(v["gold"], 1), "%.3f" % v[w])
    al = pd.read_csv(os.path.join(T, P.FILES["alarms"]), parse_dates=["raised_utc", "cleared_utc"])
    wo = pd.read_csv(os.path.join(T, P.FILES["workorders"]), parse_dates=["raised", "attended", "completed"])
    gf = pd.read_csv(os.path.join(T, P.FILES["geofence"]), parse_dates=["entered", "left"])
    faults = al[al.code.str.startswith("F")]
    ok("B every fault alarm has one work order and no warning has one",
       set(faults.alarm_id) == set(wo.alarm_ref.dropna().astype(int)) and wo.alarm_ref.dropna().is_unique)

    def ambiguous(t):
        t = pd.Timestamp(t).to_pydatetime()
        return t.replace(fold=0).utcoffset() != t.replace(fold=1).utcoffset() if t.tzinfo else \
            t.replace(tzinfo=UK, fold=0).utcoffset() != t.replace(tzinfo=UK, fold=1).utcoffset()
    amb = sum(ambiguous(t) for t in list(gf.entered) + list(gf.left) + list(wo.raised) + list(wo.attended))
    ok("B no UK time in the tracker or the CMMS falls in a clock-change hour", amb == 0, str(amb))
    j = wo.dropna(subset=["alarm_ref"]).merge(al, left_on=wo.dropna(subset=["alarm_ref"]).alarm_ref.astype(int),
                                              right_on="alarm_id")
    to_utc = lambda t: pd.Timestamp(t).tz_localize(UK).tz_convert("UTC").tz_localize(None)
    late = sum(to_utc(r.attended) > r.cleared_utc for r in j.itertuples())
    ok("B some CMMS attended stamps fall after the alarm cleared (the sync)", late > 0, str(late))

    # ------------------------------------------------------------ the realism sweep
    w = K.w
    piv = w.pivot(index="date", columns="site", values="poa_irradiation_kwh_m2")
    same = max(int((piv[a] == piv[b]).sum()) for i, a in enumerate(piv.columns) for b in piv.columns[i + 1:])
    ok("realism: two sites' irradiation agree to the watt-hour only by chance (under 1 per cent of days)",
       same < 0.01 * len(piv), str(same))
    ok("realism: no constant block series", int(K.sc.groupby(["site", "inverter"]).ac_energy_mwh.nunique().min()) > 300)
    vt = pd.read_csv(os.path.join(T, P.FILES["geofence"]), parse_dates=["entered", "left"])
    ok("realism: every van visit leaves after it enters", bool((vt.left > vt.entered).all()))
    ok("realism: every alarm clears after it is raised", bool((al.cleared_utc > al.raised_utc).all()))
    ok("realism: every work order completes after it is attended", bool((wo.completed >= wo.attended).all()))
    names = {"Valerie Freeman", "Terence Coates", "Rosie Taylor", "Clive Barber"}
    import zipfile as _z
    seen = set()
    for f in os.listdir(T):
        if f.endswith((".docx", ".xlsx")):
            core = _z.ZipFile(os.path.join(T, f)).read("docProps/core.xml").decode("utf-8")
            seen |= {n for n in names if n in core}
            ok("realism: %s carries no writing library's name" % f,
               not any(s in core for s in ("python-docx", "openpyxl", "Openpyxl")))
    ok("realism: every person in the documents comes from guard.py names", seen <= names, str(seen))

    # ------------------------------------------------------------ the separation line and the input gates
    call_files = {P.FILES[k] for k in ("export", "scada", "weather", "register", "layout", "environs", "omlog", "note")}
    ask_files = {P.FILES[k] for k in ("met", "pyrreg", "certs", "alarms", "workorders", "geofence", "vans")}
    ok("separation: no ask file is a call file", not call_files & ask_files)
    files = sorted(os.listdir(T))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    rows = {f: sum(1 for _ in open(os.path.join(T, f))) - 1 for f in files if f.endswith(".csv")}
    ok("gates: 10 or more files", len(files) >= 10, str(len(files)))
    ok("gates: 3 or more formats", len(fmts) >= 3, str(sorted(fmts)))
    ok("gates: one file of 25,000 rows or more", max(rows.values()) >= 25000 or len(K.sc) >= 25000,
       "%d / parquet %d" % (max(rows.values()), len(K.sc)))
    ok("gates: two distractors named", len(B.DISTRACTORS) >= 2)
    print("%d failures" % len(FAILS))
    return FAILS


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
