"""task478's assertions on the cut pack and the generator's clean truth: the three rules (R1 to R3c), every semantic fork
row (SF1 to SF28), the ladder, the golden's licensed family and margins, the asks' devices, the separation line, the
distractors, the input gates and the realism sweep.

    python3 task478/generator/checks.py
"""
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import bundle as B    # noqa: E402
import pack as P      # noqa: E402
import world as W     # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLD = ["Ashgrove Refining", "Valmora Renewable Fuels", "Sedge Hollow Creamery", "Lindqvist Paperboard",
        "Merriwell Foods"]
DEFAULT = ["Ashgrove Refining", "Valmora Renewable Fuels", "Sedge Hollow Creamery", "Lindqvist Paperboard",
           "Tamsett State University"]
RESULTS = []


def check(name, ok):
    RESULTS.append((name, bool(ok)))
    print("%s  %s" % ("PASS" if ok else "FAIL", name))


def whole(f):
    return {n: B.hround(f[n]) for n in B.ORDER}


def margin(f):
    o = sorted(f, key=lambda n: -f[n])
    return f[o[4]] / f[o[5]]


def edge(f):
    """The least distance of any facility's figure from a rounding half."""
    return min(abs((f[n] % 1.0) - 0.5) for n in B.ORDER)


def subset(keys):
    d = tempfile.mkdtemp(prefix="t478_")
    for k in keys:
        shutil.copy(os.path.join(TARGET, P.FILES[k]), os.path.join(d, P.FILES[k]))
    return d


def pdf_text(key):
    import pypdf
    r = pypdf.PdfReader(os.path.join(TARGET, P.FILES[key]))
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in r.pages))


def fac_tons(I, unit_lb):
    lb = dict(unit_lb)
    lb.update(I.cems)
    out = {n: 0.0 for n in B.ORDER}
    for d, v in lb.items():
        out[I.facility[d]] += v / 2000.0
    return out


def carried(I, k, level="geo", form="exp", heat=None, annual=False, lag=0):
    """Each burner's tests carried to each 2026 month's heat content by the rise k. level: the unit's level from its
    carried tests (geometric or arithmetic mean, median, latest, last two or three, those since 2022); form: exp(k
    (h/HREF - 1)) or (h/HREF)^k; heat: another {(area, y, m): factor} table; annual: the year's fuel at the mean of the
    months' factors; lag: the table's month read as the month after the gas."""
    hc = heat or I.heatc

    def H(area, y, m):
        m2, y2 = m + lag, y
        if m2 > 12:
            m2, y2 = m2 - 12, y2 + 1
        return hc[(area, y2, m2)]
    f = (lambda h: (h / B.HREF) ** k) if form == "power" else (lambda h: np.exp(k * (h / B.HREF - 1)))
    out = {}
    for d in I.open:
        g = I.tests[I.tests["device"] == d]
        s, dates = g["lb_mmbtu"].to_numpy(), list(g["date"])
        months = I.hi_month[d]
        a = np.array([v / f(H(I.area[d], t.year, t.month)) for v, t in zip(s, dates)])
        lv = {"geo": lambda: float(np.exp(np.mean(np.log(a)))), "mean": lambda: a.mean(),
              "median": lambda: float(np.median(a)), "latest": lambda: a[-1], "last2": lambda: a[-2:].mean(),
              "last3": lambda: a[-3:].mean(),
              "since2022": lambda: float(np.exp(np.mean(np.log(a[[t.year >= 2022 for t in dates]]))))}[level]()
        if annual:
            out[d] = sum(months.values()) * lv * np.mean([f(H(I.area[d], B.YEAR, m)) for m in range(1, 13)])
        else:
            out[d] = sum(mm * lv * f(H(I.area[d], B.YEAR, m)) for m, mm in months.items())
    return fac_tons(I, out)


def k_fit(I, form="exp", lag=0, hourly=True):
    dev = [d for d in I.monitored if "burner" in I.control[d]][0]
    g = I.cems_df[(I.cems_df["device"] == dev) & (I.cems_df["nox_rate_modc"] == "01")]

    def x(m):
        m2, y2 = m + lag, B.YEAR
        if m2 > 12:
            m2, y2 = m2 - 12, y2 + 1
        h = I.heatc[(I.area[dev], y2, m2)]
        return np.log(h / B.HREF) if form == "power" else h / B.HREF - 1
    if hourly:
        return float(np.polyfit(np.array([x(int(m)) for m in g["month"]]), np.log(g["nox_rate_lb_mmbtu"].to_numpy()),
                                1)[0])
    mm = g.groupby("month")["nox_rate_lb_mmbtu"].mean()
    return float(np.polyfit(np.array([x(int(m)) for m in mm.index]), np.log(mm.to_numpy()), 1)[0])


def truth_routes(e):
    """The clean truth: every unit's measured tests, its true monthly heat input and the monitors' true hours, before
    any file is written."""
    U = e["units"]
    hc = e["heat_content"]

    def fac(unit_lb):
        f = {}
        for d in W.UNIT:
            v = unit_lb[d] if d in unit_lb else U[d]["nox_2026"]
            n = W.FAC_NAME[W.UNIT[d]["facility"]]
            f[n] = f.get(n, 0.0) + v / 2000.0
        return f
    hi = {d: {m: U[d]["mmbtu"][(W.YEAR, m)] for m in range(1, 13)} for d in W.OPEN}
    out = {"truth": fac({})}
    out["latest"] = fac({d: sum(hi[d].values()) * max(U[d]["tests"], key=lambda t: t["date"])["measured"]
                         for d in W.OPEN})
    out["mean"] = fac({d: sum(hi[d].values()) * np.mean([t["measured"] for t in U[d]["tests"]]) for d in W.OPEN})
    pb = [d for d in W.MONITORED if W.UNIT[d]["control"] != "SCR"][0]
    area = W.AREA[W.UNIT[pb]["facility"]]
    hrs = [(t, r) for t, _, _, r, sub in U[pb]["cems"] if not sub]
    k = float(np.polyfit([hc[(area, t.year, t.month)] / W.HREF - 1 for t, _ in hrs], [np.log(r) for _, r in hrs], 1)[0])

    def carry(d):
        a = W.AREA[W.UNIT[d]["facility"]]
        lv = np.exp(np.mean([np.log(t["measured"]) - k * (hc[(a, t["date"].year, t["date"].month)] / W.HREF - 1)
                             for t in U[d]["tests"]]))
        return sum(q * lv * np.exp(k * (hc[(a, W.YEAR, m)] / W.HREF - 1)) for m, q in hi[d].items())
    out["carried"] = fac({d: carry(d) for d in W.OPEN})
    out["k"] = k
    return out


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    I = B.Inputs(TARGET)
    k = I.k_pb1()
    gold = B.facility_tons(I, "golden", k)
    gw = whole(gold)
    five = B.five(gold)
    e = W.everything()
    pm = B.read_permits(TARGET)
    pmi = pm.set_index("DEVICE_NO")

    # ---------------------------------------------------------------- R1: the field's raw material ships
    cems = pd.read_csv(os.path.join(TARGET, P.FILES["cems"]), dtype=str)
    check("R1 the CEMS export ships one row per operating hour of the four monitored units (%d rows)" % len(cems),
          len(cems) > 25000 and cems.groupby(["facility_id", "unit_id"]).ngroups == 4)
    check("R1 the two source test databases ship %d tests of the %d unmonitored burners" % (len(I.tests), len(I.open)),
          len(I.tests) == f["components"]["tests"] and set(I.tests["device"]) == set(I.open) and
          all("burner" in I.control[d] for d in I.open))
    heat = pd.read_csv(os.path.join(TARGET, P.FILES["heat"]), dtype=str)
    check("R1 the utility's heat content table ships both BTU areas, January 2018 to February 2027 (%d rows)" % len(heat),
          len(heat) == 2 * 110 and set(heat["BTU_AREA"]) == {"WESTSIDE", "EASTSIDE"})
    heads = []
    for kk, fn in P.FILES.items():
        p = os.path.join(TARGET, fn)
        if fn.endswith(".csv"):
            heads += open(p, encoding="utf-8").readline().strip().lower().split(",")
        elif fn.endswith(".xlsx"):
            import openpyxl
            for ws in openpyxl.load_workbook(p, read_only=True).worksheets:
                for row in ws.iter_rows(min_row=1, max_row=2, values_only=True):
                    heads += [str(v).lower() for v in row if v is not None]
    check("R1 no shipped column holds a unit's 2026 rate, an adjusted or corrected rate, a sensitivity, a Wobbe index, "
          "an oxygen trim or a facility total",
          not any(re.search(r"wobbe|trim|adjust|correct(ed)? rate|sensitiv|2026 rate|\bannual\b|\btotal\b|represent|"
                            r"air.?fuel|excess air", h) for h in heads))
    docs = (pdf_text("plan") + " " + pdf_text("guidance")).lower()
    sent = [s for s in re.split(r"(?<=[.;:])\s", docs) if re.search(r"heat content|heating value|\bbtu\b|btu_|btu/", s)]
    check("R1 no document sentence on heat content names a NOx rate, a burner, an emission or a test (%d sentences "
          "read)" % len(sent), sent and not any(re.search(r"nox|burner|emi(t|ssion)|source test|rate in lb", s)
                                                   for s in sent))
    check("R1 neither document says a burner's NOx moves with its fuel, its air or its tuning, or that a test is "
          "unrepresentative", not re.search(r"wobbe|oxygen trim|air.fuel|excess air|richer|leaner|retun|tuning|"
                                            r"unrepresentative|flame temperature|interchangeab", docs))

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    tr = truth_routes(e)
    check("R3a the easy route on the clean truth (each burner's latest test across its 2026 heat input, the monitors' "
          "hours, every filed rule applied) files the default path's five: %s" % B.five(tr["latest"]),
          B.five(tr["latest"]) == DEFAULT)
    check("R3a the mean of each burner's tests on the clean truth files the same five", B.five(tr["mean"]) == DEFAULT)
    check("R3b the decisive step alone on the clean truth (the monitored burner's rise against its area's heat content, "
          "each burner's tests carried to each 2026 month's) files the golden five (rise %.2f)" % tr["k"],
          B.five(tr["carried"]) == GOLD)
    check("R3 the generator's true 2026 NOx puts the golden five on top (fifth over sixth %.3f)" % margin(tr["truth"]),
          B.five(tr["truth"]) == GOLD and margin(tr["truth"]) > 1.10)
    truth = {W.FAC_NAME[c]: v for c, v in e["facility_tons"].items()}
    dev = max(abs(gold[n] - truth[n]) for n in B.ORDER)
    check("R3 every golden facility figure sits within 0.25 tons of the true 2026 NOx (largest gap %.3f)" % dev,
          dev < 0.25 and gw == whole(truth))
    lat = B.facility_tons(I, "latest")
    check("R3a the default path on the cut pack files the same five", B.five(lat) == DEFAULT)
    keys = [(r.device, r.date) for r in I.tests.itertuples()]
    old_ = pd.read_csv(os.path.join(TARGET, P.FILES["tests_old"]), dtype=str)
    new_ = pd.read_excel(os.path.join(TARGET, P.FILES["tests_new"]), sheet_name="Results")
    check("R3c no plant: no unit has two tests on one day and no test repeats another's ppm and lb/hr",
          len(set(keys)) == len(keys) and not old_.duplicated(["NOX_PPMVD", "NOX_LB_HR"]).any()
          and not new_.duplicated(["NOx (ppmvd @ ref O2)", "NOx (lb/hr)"]).any())
    st_raw = pd.read_csv(os.path.join(TARGET, P.FILES["statements"]), dtype=str)
    rep = st_raw.groupby(["DEVICE_NO", "STMT_YEAR"])["HOURS"].apply(lambda s: ",".join(s)).reset_index()
    check("R3c no plant: no unit's year of monthly hours repeats another year's",
          not rep.duplicated(["DEVICE_NO", "HOURS"]).any())
    wy = heat[heat["BTU_AREA"] == "WESTSIDE"].assign(y=lambda d: d["MONTH"].str[:4])
    yr = wy.groupby("y")["BTU_FACTOR"].apply(lambda s: ",".join(s))
    check("R3c no plant: no year of the Westside heat content repeats another's, and the Eastside's stays within "
          "1.030 to 1.040", not yr.duplicated().any() and
          heat[heat["BTU_AREA"] == "EASTSIDE"]["BTU_FACTOR"].astype(float).between(1.030, 1.040).all())
    check("R3c no plant: every test passed its permit limit, so no notice, retest or repair sits beside any test",
          (old_["RESULT"] == "PASS").all() and (new_["Result"] == "PASS").all())

    # ---------------------------------------------------------------- R2: every Layer 1 item, mishandled
    Il = B.Inputs(TARGET, conv="lbhr")
    gl = B.facility_tons(Il, "golden")
    check("R2a the older tests as lb/hr over the device's rating times the test's load in place of Method 19 from ppm: "
          "the call and the 14 whole tons (SF6)", whole(gl) == gw)
    Ih = B.Inputs(TARGET, mmscf_hhv=1020.0)
    gh = B.facility_tons(Ih, "golden")
    check("R2b MMSCF at a fixed 1,020 Btu/scf in place of the area's monthly heat content: the call and the 14 whole tons "
          "(SF5)", whole(gh) == gw)
    ts = pd.to_datetime(cems["op_date"]) + pd.to_timedelta(cems["op_hour"].astype(int), unit="h") + pd.Timedelta(hours=8)
    keep = ts.dt.year == 2026
    key = {(r.FAC_NO, r.CEMS_UNIT_ID): r.DEVICE_NO for r in pm.itertuples() if isinstance(r.CEMS_UNIT_ID, str)}
    lb_utc = {key[(a, b)]: g["nox_mass_lb"].astype(float).sum() for (a, b), g in
              cems[keep].groupby(["facility_id", "unit_id"])}
    f_utc = fac_tons(I, {**B.unit_lb(I, "golden", k), **lb_utc})
    check("R2c the CEMS hours read as UTC: the call and the 14 whole tons (SF3)", whole(f_utc) == gw)
    meas = cems[cems["nox_rate_modc"] != "12"]
    sub = {key[(a, b)]: g["nox_mass_lb"].astype(float).sum() for (a, b), g in meas.groupby(["facility_id", "unit_id"])}
    f_sub = fac_tons(I, {**B.unit_lb(I, "golden", k), **sub})
    check("R2d the substitute data hours dropped: the call (SF4)", B.five(f_sub) == GOLD)
    check("R2e Haskett Ridge's tests and statements under its old number 0705 carry its device numbers (SF10)",
          set(old_[old_["FAC_NO"] == "705"]["DEVICE_NO"]) <= {"1501", "1502"} and
          set(st_raw[st_raw["FAC_NO"] == "0705"]["DEVICE_NO"]) == {"D-1501", "D-1502"})
    check("R2f the older database's keys without leading zeros or the D- prefix join every test to a permitted unit",
          set("D-" + old_["DEVICE_NO"]) <= set(I.open))

    # ---------------------------------------------------------------- the ladder
    check("L0 each burner's latest test across its 2026 heat input files %s" % ", ".join(n.split()[0] for n in
                                                                                        B.five(lat)),
          B.five(lat) == DEFAULT)
    reflex = {m: B.facility_tons(I, m) for m in ("mean", "median", "max", "last2", "limit", "caltrend")}
    for m, v in reflex.items():
        check("L1 the %s route misses the golden five (%s)" % (m, ", ".join(n.split()[0] for n in B.five(v))),
              B.five(v) != GOLD)
    for m in ("pb1_all", "pb1_area"):
        v = B.facility_tons(I, m)
        check("L2 the monitored boiler's 2026 months as an index on each latest test (%s) misses the golden five (%s)"
              % (m, ", ".join(n.split()[0] for n in B.five(v))), B.five(v) != GOLD)
    v = B.facility_tons(I, "limit_stale")
    check("L3 the permit limit where a unit was last tested before 2026 misses the golden five (%s)"
          % ", ".join(n.split()[0] for n in B.five(v)), B.five(v) != GOLD)
    kept = sum(whole(lat)[n] == gw[n] for n in B.ORDER)
    check("L the default path keeps %d of the 14 whole tons, at most 11" % kept, kept <= 11)

    # ---------------------------------------------------------------- the golden and its licensed family
    check("G1 the golden five: %s" % five, five == GOLD and f["call"]["facilities"] == GOLD)
    check("G1 figures.json carries the 14 whole tons", all(f["facilities"][n]["nox_tons"] == gw[n] for n in B.ORDER))
    ks = {"the monitored boiler's hours": k, "its monthly means": I.k_pb1(hourly=False),
          "the Westside burners' tests": I.k_tests(), "every burner's tests": I.k_tests(area=None)}
    fam = {}
    for kn, kv in ks.items():
        for lv in ("geo", "mean", "median", "latest", "last2", "last3", "since2022"):
            fam["%s, %s" % (kn, lv)] = carried(I, kv, lv)
    fam["power law"] = carried(I, k_fit(I, form="power"), form="power")
    fam["older tests from lb/hr"] = gl
    check("G2 every standing member (%d: the rise from the monitored boiler's hours, its monthly means, the Westside "
          "tests or every burner's tests, each unit's level from all its carried tests, their mean, median, latest, last "
          "two or three or those since 2022, the power law, the older tests from lb/hr) files the golden five" % len(fam),
          all(B.five(v) == GOLD for v in fam.values()))
    check("G2 every standing member prints the same 14 whole tons", all(whole(v) == gw for v in fam.values()))
    lm = min(edge(v) for v in fam.values())
    check("G3 every member's every figure sits 0.25 tons or more from a rounding half (least %.3f) (SF11)" % lm,
          lm >= 0.25)
    mm = min(margin(v) for v in fam.values())
    check("G4 fifth clears sixth by 10 per cent or more under every member (least %.3f) (SF12)" % mm, mm >= 1.10)
    kk = list(ks.values())
    check("G5 the rise: %.2f from the monitored boiler, %.2f to %.2f from the rest, within 3 per cent of one another and "
          "of the generator's %.1f" % (k, min(kk), max(kk), W.K_HV),
          max(kk) / min(kk) < 1.03 and abs(k - W.K_HV) < 0.03 * W.K_HV)
    r0, r1 = [], []
    for d_, g in I.tests.groupby("device"):
        if I.area[d_] != "WESTSIDE":
            continue
        h = np.array([I.hv(d_, t) / B.HREF - 1 for t in g["date"]])
        l_ = np.log(g["lb_mmbtu"].to_numpy())
        r0 += list(l_ - l_.mean())
        a_ = l_ - k * h
        r1 += list(a_ - a_.mean())
    check("G5 the heat content takes the Westside burners' within-unit test scatter from %.3f to %.3f in the log"
          % (np.std(r0), np.std(r1)), np.std(r1) < 0.5 * np.std(r0))
    six = sorted(B.ORDER, key=lambda n: -gold[n])[5]
    check("G6 sixth as figures.json states (%s, %d)" % (six, gw[six]),
          f["components"]["sixth"]["name"] == six and f["components"]["sixth"]["tons"] == gw[six])
    pct = [100 * (np.exp(kv * 0.01) - 1) for kv in kk] + [100 * (1.01 ** k_fit(I, form="power") - 1)]
    check("G7 the rise a per cent of heat content prints %d per cent under every construction (%.2f to %.2f)"
          % (int(round(pct[0])), min(pct), max(pct)), len({int(round(x)) for x in pct}) == 1 and
          f["components"]["rise_pct_per_pct"] == int(round(pct[0])))

    # ---------------------------------------------------------------- SF1 to SF24
    m19 = new_["NOx (ppmvd @ ref O2)"] * 1.194e-7 * 8710.0 * 20.9 / (20.9 - new_["Ref O2 (%)"])
    check("SF1 the newer database's lb/MMBtu is Method 19's NO2 figure from its ppm, within the columns' printed "
          "precision", (abs(m19 / new_["NOx (lb/MMBtu)"] - 1) < 0.004).all() and "expressed as no2" in docs)
    eng = B.engine_lb(TARGET)
    with_eng = {n: gold[n] + eng[n] / 2000.0 for n in B.ORDER}
    check("SF2 the emergency engines added to each facility leave the five; the Rule 4307 units have no fuel record",
          B.five(with_eng) == GOLD and not set(pm[pm["RULE"] == "4307"]["DEVICE_NO"]) & set(st_raw["DEVICE_NO"]))
    check("SF3 the CEMS hours on UTC (R2c)", whole(f_utc) == gw)
    check("SF4 the substitute data hours dropped (R2d)", B.five(f_sub) == GOLD)
    check("SF5 MMSCF at 1,020 Btu/scf (R2b)", whole(gh) == gw)
    check("SF6 the older tests from lb/hr (R2a)", whole(gl) == gw)
    klag = k_fit(I, lag=1)
    vlag = carried(I, klag, lag=1)
    check("SF7 the table's month is the month the gas was delivered (guidance section 7); read as the month after, %d of "
          "14 whole tons move and the boiler's rise drops to %.2f, so the data prefer the filed reading"
          % (sum(whole(vlag)[n] != gw[n] for n in B.ORDER), klag),
          "the average heat content of the gas it delivered to the area in the month" in pdf_text("guidance") and
          klag < 0.85 * k)
    hscf = {(r.BTU_AREA, int(r.MONTH[:4]), int(r.MONTH[5:])): float(r.HEAT_CONTENT_BTU_SCF) / 1000.0
            for r in heat.itertuples()}
    v8 = carried(I, k, heat=hscf)
    check("SF8 the carrying on the table's Btu/scf column in place of its therms a CCF: the same 14 whole tons",
          whole(v8) == gw)
    v9 = carried(I, k, annual=True)
    check("SF9 the year's fuel at the mean of the months' factors does not compute the NOx emitted (guidance section 3), "
          "moves %d of 14 whole tons and leaves the five" % sum(whole(v9)[n] != gw[n] for n in B.ORDER),
          B.five(v9) == GOLD and "the nox it emitted over the year's operation" in docs)
    check("SF10 every test and statement row joins a Rule 4306 device of the permit list",
          set(I.tests["device"]) <= set(I.devices) and set(st_raw["DEVICE_NO"]) <= set(I.devices))
    check("SF11 no figure at a half (G3)", lm >= 0.25)
    check("SF12 no tie for fifth (G4)", mm >= 1.10)
    dC = subset(["cems", "tests_old", "tests_new", "statements", "heat", "permits"])
    s13 = B.facility_tons(B.Inputs(dC), "golden")
    shutil.rmtree(dC)
    check("SF13 the call and the 14 whole tons from the CEMS export, the test databases, the statements, the heat content "
          "and the permit list alone", whole(s13) == gw)
    check("SF14 the rise as a power of the heat content in place of an exponential: the same 14 whole tons",
          whole(fam["power law"]) == gw)
    check("SF15 the rise from the monitored boiler's hours, its monthly means or the tests (G2)",
          all(whole(fam["%s, geo" % kn]) == gw for kn in ks))
    ga = B.gas_2026(TARGET)
    gwa = {n: B.hround(ga[n]) for n in B.ORDER}
    bl = B.read_billing(TARGET)
    comb = B.combined_accounts(bl)
    alt = {n: 0.0 for n in B.ORDER}
    seen = set()
    for r in bl.itertuples():
        if r.ACCOUNT_NO in comb:
            if (r.ACCOUNT_NO, r.READ_TO) in seen:
                continue
            seen.add((r.ACCOUNT_NO, r.READ_TO))
        therms = r.USAGE_THERMS if r.READ_TO >= B.CONVERSION else r.USAGE_THERMS * r.BTU_FACTOR
        n_ = (r.READ_TO - r.READ_FROM).days
        a_ = max(r.READ_FROM + dt.timedelta(days=1), B.D0)
        z_ = min(r.READ_TO + dt.timedelta(days=1), B.D1)
        alt[r.facility] += therms * max(0, (z_ - a_).days) / n_ / 10.0
    plan = pdf_text("plan")
    check("SF16 plan 4.2 spreads a bill from the day of its prior read to the day before its current read; the day after "
          "the prior read through the current read moves %d gas figures" % sum(B.hround(alt[n]) != gwa[n]
                                                                              for n in B.ORDER),
          sum(B.hround(alt[n]) != gwa[n] for n in B.ORDER) > 0 and "from the day of its prior read to the day before its "
          "current read" in plan)
    check("SF17 therms to MMBtu at 10 (guidance section 4)", "therms divided by 10" in pdf_text("guidance"))
    check("SF18 every billing line's service address matches exactly one Appendix A facility (%d lines)" % len(bl),
          bl["facility"].notna().all() and bl.groupby("METER_NO")["facility"].nunique().max() == 1)
    rr = {n: 0.0 for n in B.ORDER}
    seen = set()
    for r in bl.itertuples():
        if r.ACCOUNT_NO in comb:
            if (r.ACCOUNT_NO, r.READ_TO) in seen:
                continue
            seen.add((r.ACCOUNT_NO, r.READ_TO))
        therms = r.USAGE_THERMS if r.READ_TO >= B.CONVERSION else B.hround(r.USAGE_THERMS * r.BTU_FACTOR)
        n_ = (r.READ_TO - r.READ_FROM).days
        rr[r.facility] += therms * max(0, (min(r.READ_TO, B.D1) - max(r.READ_FROM, B.D0)).days) / n_ / 10.0
    ge = min(abs((ga[n] % 1.0) - 0.5) for n in B.ORDER)
    re_ = min(abs((rr[n] % 1.0) - 0.5) for n in B.ORDER)
    check("SF19 a line read before the conversion at its CCF times its factor, unrounded or to the whole therm: the same "
          "14 whole MMBtu (least distance from a half %.3f and %.3f)" % (ge, re_),
          all(B.hround(rr[n]) == gwa[n] for n in B.ORDER) and ge >= 0.15 and re_ >= 0.15)
    eb = B.engine_lb(TARGET)
    ebw = {n: B.hround(eb[n]) for n in B.ORDER}
    insp = pd.read_csv(os.path.join(TARGET, P.FILES["inspections"]), dtype=str)
    insp["date"] = [dt.date.fromisoformat(x) for x in insp["INSPECTION_DATE"]]
    insp["read"] = insp["HOUR_METER"].astype(float)
    logs = B.read_engine_logs(TARGET)
    mins = B.minutes_logged(TARGET)
    repl = B.replacements(TARGET)
    outs = B.outages(TARGET)
    meter_lb = {n: 0.0 for n in B.ORDER}
    for d_, g in insp.groupby("DEVICE_NO"):
        g = g.sort_values("date")
        n_ = B.FAC_OF_NO[g.iloc[0]["FAC_NO"]]
        bhp, tier = float(pmi.loc[d_, "RATING"]), pmi.loc[d_, "ENGINE_TIER"]
        span = float(np.interp(dt.date(2027, 1, 1).toordinal(), [x.toordinal() for x in g["date"]], g["read"]) -
                     np.interp(dt.date(2026, 1, 1).toordinal(), [x.toordinal() for x in g["date"]], g["read"]))
        meter_lb[n_] += span * bhp * B.ENGINE_LF * B.TIER_NOX[tier] / B.G_LB
    moved = sum(B.hround(meter_lb[n]) != ebw[n] for n in B.ORDER)
    check("SF20 guidance 6 takes the time the engine ran, which the logs record; the hour meters, which also count "
          "warm-up and cool-down, interpolated to the year move %d of 14" % moved, moved >= 12 and
          "also counts each start's warm-up and cool-down" in pdf_text("guidance"))
    alt_g = {n: eb[n] * B.G_LB / 453.59237 for n in B.ORDER}
    check("SF21 the guidance writes 453.6 g/lb; 453.59237 in its place moves %d whole pounds"
          % sum(B.hround(alt_g[n]) != ebw[n] for n in B.ORDER), "453.6 g/lb" in pdf_text("guidance"))
    near = [(d_, r.date) for d_, (rd, _, _) in repl.items() for r in logs[logs["device"] == d_].itertuples()
            if rd - dt.timedelta(days=4) <= r.date <= rd]
    check("SF22 no replaced engine has a run on its replacement date or in the four days before it", not near)
    half = {n: 0.0 for n in B.ORDER}
    banks = {d_: [x for x in W.ENGINE if W.ENGINE[x]["facility"] == W.ENGINE[d_]["facility"] and W.ENGINE[d_]["bank"]
                  and W.ENGINE[x]["bank"] == W.ENGINE[d_]["bank"]] for d_ in W.ENGINE}
    for r in logs.itertuples():
        h = B._as_hmm(r.value) if mins else r.value
        emer = r.purpose.startswith("Emergency") and r.facility in outs and r.date in outs[r.facility]
        if emer and h > outs[r.facility][r.date] + 1e-9:
            h = h / len(banks[r.device])
        bhp, tier = float(pmi.loc[r.device, "RATING"]), pmi.loc[r.device, "ENGINE_TIER"]
        if r.device in repl and r.date < repl[r.device][0]:
            bhp, tier = repl[r.device][1], repl[r.device][2]
        half[r.facility] += h * bhp * B.ENGINE_LF * B.TIER_NOX[tier] / B.G_LB
    check("SF23 a banked engine's emergency line at the compliance log's outage hours or halved: the same 14 whole "
          "pounds", {n: B.hround(half[n]) for n in B.ORDER} == ebw)
    raw_b = pd.read_csv(os.path.join(TARGET, P.FILES["billing"]), dtype=str)
    bdate = {bid: dt.datetime.strptime(x, "%m/%d/%Y").date() for bid, x in zip(raw_b["BILL_ID"], raw_b["BILL_DATE"])}
    straddle = [r for r in bl.itertuples() if r.READ_TO < B.CONVERSION <= bdate[r.BILL_ID]]
    check("SF27 the billing conversion read on the bill date in place of the read date: no line read before 1 July "
          "2026 was billed on or after it, so both boundaries put the same %d lines on each side" % len(bl),
          not straddle)
    est = bl[bl["READ_TYPE"] == "E"]
    check("SF24 the %d estimated reads stand as billed: each meter's next read is actual and the extract carries no "
          "adjustment line" % len(est), len(est) == len(W.ESTIMATED) and set(bl["READ_TYPE"]) == {"A", "E"})

    def k_own(devs):
        xs, ys = [], []
        for d_, g in I.tests.groupby("device"):
            if d_ not in devs:
                continue
            h = np.array([I.hv(d_, t) / B.HREF - 1 for t in g["date"]])
            l_ = np.log(g["lb_mmbtu"].to_numpy())
            xs += list(h - h.mean())
            ys += list(l_ - l_.mean())
        xs, ys = np.array(xs), np.array(ys)
        b_ = float(np.dot(xs, ys) / np.dot(xs, xs))
        return b_, float(np.sqrt(np.sum((ys - b_ * xs) ** 2) / (len(xs) - len(devs) - 1) / np.dot(xs, xs)))

    def by_unit(kmap):
        out = {}
        for d_ in I.open:
            kk_ = kmap(d_)
            g = I.tests[I.tests["device"] == d_]
            a_ = [v_ / np.exp(kk_ * (I.hv(d_, t) / B.HREF - 1)) for v_, t in zip(g["lb_mmbtu"], g["date"])]
            lv = float(np.exp(np.mean(np.log(a_))))
            out[d_] = sum(q * lv * np.exp(kk_ * (I.heatc[(I.area[d_], B.YEAR, m)] / B.HREF - 1))
                          for m, q in I.hi_month[d_].items())
        return fac_tons(I, out)
    lnb = [d_ for d_ in I.open if I.control[d_] == "low-NOx burner"]
    kl, sl = k_own(lnb)
    ku, _ = k_own([d_ for d_ in I.open if d_ not in lnb])
    v25 = [by_unit(lambda d_: kl if d_ in lnb else k), by_unit(lambda d_: kl if d_ in lnb else ku)]
    check("SF25 the rise by burner class (the low-NOx burners' own tests %.2f, se %.2f; the ultra-low NOx burners' %.2f "
          "or the monitored boiler's): the same five and 14 whole tons" % (kl, sl, ku),
          all(B.five(v_) == GOLD and whole(v_) == gw and edge(v_) >= 0.25 for v_ in v25))
    own = {n: k_own([d_ for d_ in I.open if I.facility[d_] == n]) for n in B.ORDER
           if I.area[[d_ for d_ in I.open if I.facility[d_] == n][0]] == "WESTSIDE"}
    ident = {n: kv for n, (kv, se) in own.items() if se < 1.0}
    v26 = by_unit(lambda d_: ident.get(I.facility[d_], k))
    check("SF26 a facility's own rise: Merriwell Foods' tests all sit on lean August gas, so its own rise is unidentified "
          "(se %.2f) and a fit pools; with each facility's own rise where its tests identify it (%s), the same five and 14 "
          "whole tons" % (own["Merriwell Foods"][1], ", ".join("%s %.2f" % (n.split()[0], v_) for n, v_ in ident.items())),
          own["Merriwell Foods"][1] > 2.0 and B.five(v26) == GOLD and whole(v26) == gw)

    # ---------------------------------------------------------------- ask A: the gas delivered
    truth_g = {W.FAC_NAME[c]: v for c, v in e["gas_2026"].items()}
    check("A the golden's gas figures are the generator's billed therms, spread by plan 4.2, on all 14",
          all(gwa[n] == B.hround(truth_g[n]) for n in B.ORDER) and
          all(f["facilities"][n]["gas_mmbtu"] == gwa[n] for n in B.ORDER))
    rungs = {h: B.gas_2026(TARGET, h) for h in ("as_labelled", "as_labelled_dedupe", "all_ccf", "no_dedupe", "no_split")}
    mv = {h: sum(B.hround(v[n]) != gwa[n] for n in B.ORDER) for h, v in rungs.items()}
    check("A every rung moves its facilities (%s)" % ", ".join("%s %d" % kv for kv in mv.items()),
          mv["as_labelled"] == 14 and mv["as_labelled_dedupe"] == 14 and mv["all_ccf"] == 14 and mv["no_split"] == 14
          and mv["no_dedupe"] == len(comb))
    check("A fair: the five combined-billing accounts are the only multi-meter accounts whose meters carry identical "
          "usage every period (%s)" % ", ".join(sorted(comb)), sorted(comb) == W.COMBINED)
    st26 = B.read_statements(TARGET)
    st26 = st26[st26["year"] == B.YEAR]
    unit_fac = {d_: I.facility[d_] for d_ in I.devices}
    st26["facility"] = st26["device"].map(unit_fac)
    mon = st26.groupby(["facility", "month"])["mmbtu"].sum()
    over_pre, over_post = 0, 0
    lab = {n: {} for n in B.ORDER}
    seen = set()
    for r in bl.itertuples():
        if r.ACCOUNT_NO in comb:
            if (r.ACCOUNT_NO, r.READ_TO) in seen:
                continue
            seen.add((r.ACCOUNT_NO, r.READ_TO))
        lab[r.facility][r.READ_TO] = lab[r.facility].get(r.READ_TO, 0.0) + r.USAGE_THERMS / 10.0
        lab[r.facility].setdefault("_from", {})[r.READ_TO] = r.READ_FROM
    pre_short, post_short = [], []
    for n in B.ORDER:
        for rt, v in lab[n].items():
            if rt == "_from":
                continue
            rf = lab[n]["_from"][rt]
            used = 0.0
            for i in range((rt - rf).days):
                d_ = rf + dt.timedelta(days=i)
                if d_.year == B.YEAR:
                    used += mon.get((n, d_.month), 0.0) / ((dt.date(2026 + d_.month // 12, d_.month % 12 + 1, 1) -
                                                            dt.date(2026, d_.month, 1)).days)
                else:
                    used = None
                    break
            if used is None or used == 0:
                continue
            (pre_short if rt < B.CONVERSION else post_short).append(v / used)
    check("A fair: read as labelled, the billed usage falls below the plan units' own fuel from their statements on %d "
          "of %d periods before the July 2026 reads and on %d of %d after (split evidence: billing, statements, heat "
          "content)" % (sum(x < 1 for x in pre_short), len(pre_short), sum(x < 1 for x in post_short), len(post_short)),
          sum(x < 1 for x in pre_short) >= 0.6 * len(pre_short) and sum(x < 1 for x in post_short) == 0)
    check("A no marker: the bill ids, rate codes, read types and columns run unchanged across the conversion, and the "
          "values are whole numbers on both sides",
          set(bl[bl["READ_TO"] >= B.CONVERSION]["RATE_CODE"]) == set(bl["RATE_CODE"]) and
          set(bl[bl["READ_TO"] < B.CONVERSION]["READ_TYPE"]) <= {"A", "E"} and
          (bl["USAGE_THERMS"] == bl["USAGE_THERMS"].round()).all())
    check("A every facility has lines on both sides of the conversion",
          all(((g["READ_TO"] < B.CONVERSION).any() and (g["READ_TO"] >= B.CONVERSION).any())
              for _, g in bl.groupby("facility")))
    fac_tab = {(a, y, m): v for (a, y, m), v in I.heatc.items()}
    check("A every line's BTU_FACTOR is the table's factor for its BTU area and the month its read closes",
          all(abs(r.BTU_FACTOR - fac_tab[(B.AREA_OF[r.facility], r.READ_TO.year, r.READ_TO.month)]) < 1e-9
              for r in bl.itertuples()))

    # ---------------------------------------------------------------- ask B: the emergency engines
    truth_e = {W.FAC_NAME[c]: v for c, v in e["engine_lb"].items()}
    check("B the golden's engine figures are the generator's on all 14",
          all(ebw[n] == B.hround(truth_e[n]) for n in B.ORDER) and
          all(f["facilities"][n]["engine_nox_lb"] == ebw[n] for n in B.ORDER))
    eh = {h: B.engine_lb(TARGET, h) for h in ("naive", "decimal", "no_bank", "current")}
    mvb = {h: sum(B.hround(v[n]) != ebw[n] for n in B.ORDER) for h, v in eh.items()}
    check("B the decimal reading moves all 14 facilities, the bank lines the four banked, the current engine the two "
          "with a replacement (%s)" % ", ".join("%s %d" % kv for kv in mvb.items()),
          mvb["naive"] == 14 and mvb["decimal"] == 14 and mvb["no_bank"] == 4 and mvb["current"] == 2)
    fr = ((logs["value"] - np.floor(logs["value"] + 1e-9)) * 100).round().astype(int)
    share = np.mean([(h % 1.0) >= 0.595 for dev in W.ENGINE for _, h, _ in W.engine_runs(dev)])
    check("B fair: no entry's fraction reaches .60 in %d entries, where the same runs in decimal hours would show one "
          "on %.0f per cent of entries (SF28)" % (len(logs), 100 * share), mins and (fr <= 59).all() and share > 0.2)
    exc, exd = [], []
    for d_, g in insp.groupby("DEVICE_NO"):
        if d_ in repl:
            continue
        g = g.sort_values("date")
        n_ = B.FAC_OF_NO[g.iloc[0]["FAC_NO"]]
        lg = logs[(logs["device"] == d_) & (logs["date"] < g.iloc[1]["date"])]
        span = g.iloc[1]["read"] - g.iloc[0]["read"]

        def ran(dec):
            t = 0.0
            for r in lg.itertuples():
                h = r.value if dec else B._as_hmm(r.value)
                if r.purpose.startswith("Emergency") and n_ in outs and r.date in outs[n_]:
                    h = min(h, outs[n_][r.date])
                t += h
            return t
        exc.append((span - ran(False)) / len(lg))
        exd.append((span - ran(True)) / len(lg))
    check("B fair: over the first inspection interval each engine's hour meter runs %.3f to %.3f hours a start beyond "
          "its log read as hours and minutes (warm-up and cool-down), against %.3f to %.3f read as decimal hours"
          % (min(exc), max(exc), min(exd), max(exd)), 0.02 < min(exc) and max(exc) < 0.11 and min(exd) > max(exc))
    obanks = {n for n in outs if any(len(banks[d_]) > 1 for d_ in W.ENGINE if W.FAC_NAME[W.ENGINE[d_]["facility"]] == n)}
    over = [r for r in logs.itertuples() if r.purpose.startswith("Emergency") and r.facility in outs and
            r.date in outs[r.facility] and r.value > outs[r.facility][r.date] + 1e-9]
    check("B fair: the %d emergency lines longer than the outage the compliance log records are the banked engines' at "
          "%s, each exactly twice the outage" % (len(over), ", ".join(sorted(obanks))),
          {r.facility for r in over} == obanks and
          all(abs(r.value - 2 * outs[r.facility][r.date]) < 1e-9 for r in over))
    check("B fair: the compliance log's EQUIPMENT entries name the replaced engines' old rating and tier",
          {d_: (v_[1], v_[2]) for d_, v_ in repl.items()} ==
          {d_: (en["replaced"][1], en["replaced"][2]) for d_, en in W.ENGINE.items() if en["replaced"]})
    first = insp.groupby("DEVICE_NO")["date"].min()
    check("B silent: no replaced engine's hour meter is read before its replacement, so no meter restarts",
          all(first[d_] > rd for d_, (rd, _, _) in repl.items()))
    check("B no marker: every sheet keeps one header ('Run hours') and one number format, and every outage the "
          "compliance log records is a whole number of hours, so no outage entry reads differently either way",
          all(float(h).is_integer() for v_ in outs.values() for h in v_.values()))

    # ---------------------------------------------------------------- separation and distractors
    dX = subset([kk_ for kk_ in P.FILES if kk_ not in ("cems", "tests_old", "tests_new", "statements", "heat")])
    check("X1 the asks read no CEMS hour, source test, emission statement or heat content row: both from the other files",
          {n: B.hround(v_) for n, v_ in B.gas_2026(dX).items()} == gwa and
          {n: B.hround(v_) for n, v_ in B.engine_lb(dX).items()} == ebw)
    shutil.rmtree(dX)
    check("X2 the call reads no billing line, engine log, inspection or compliance log row (SF13)", whole(s13) == gw)
    evd = B.read_events(TARGET)
    eqd = set(evd[evd["EVENT_TYPE"].isin(["EQUIPMENT"])]["DEVICE_NO"])
    check("X3 every ask device row sits outside the call's population: the billing extract, the engine logs and the "
          "EQUIPMENT and OUTAGE entries, the EQUIPMENT on Rule 4702 engines only",
          eqd <= set(pm[pm["RULE"] == "4702"]["DEVICE_NO"]) and
          (evd[evd["EVENT_TYPE"] == "OUTAGE"]["DEVICE_NO"] == "").all())
    dD = subset([kk_ for kk_ in P.FILES if kk_ not in ("no2", "onroad")])
    check("X4 the distractors deleted: the call, the 14 whole tons and both asks unchanged",
          whole(B.facility_tons(B.Inputs(dD), "golden")) == gw and
          {n: B.hround(v_) for n, v_ in B.gas_2026(dD).items()} == gwa and
          {n: B.hround(v_) for n, v_ in B.engine_lb(dD).items()} == ebw)
    shutil.rmtree(dD)

    # ---------------------------------------------------------------- input gates
    files = os.listdir(TARGET)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("I ten or more files (%d)" % len(files), len(files) >= 10)
    check("I three or more formats (%s)" % sorted({fn.rsplit(".", 1)[1] for fn in files}),
          len({fn.rsplit(".", 1)[1] for fn in files}) >= 3)
    check("I one file of 25,000 rows or more (CEMS %d)" % len(cems), len(cems) >= 25000)
    check("I two distractors named in metadata.json, none in a file name",
          len(meta["distractor_files"]) >= 2 and all(d_ in files for d_ in meta["distractor_files"]) and
          not any("distract" in fn for fn in files))

    # ---------------------------------------------------------------- realism
    hi_, r_ = cems["heat_input_mmbtu"].astype(float), cems["nox_rate_lb_mmbtu"].astype(float)
    tol = 0.05 * r_ + 0.00005 * hi_ + 0.006
    check("Z every CEMS hour's NOx mass is its heat input times its rate, within their printed precision",
          (abs(hi_ * r_ - cems["nox_mass_lb"].astype(float)) <= tol).all())
    o_lb = old_["NOX_LB_HR"].astype(float) / ([float(pmi.loc["D-" + d_, "RATING"]) for d_ in old_["DEVICE_NO"]] *
                                              old_["LOAD_PCT"].astype(float) / 100.0)
    o_pp = old_["NOX_PPMVD"].astype(float) * 1.194e-7 * 8710.0 * 20.9 / (20.9 - old_["O2_REF"].astype(float))
    check("Z the older tests' lb/hr over rating times load and their ppm through Method 19 agree within the load's whole "
          "per cent", (abs(o_lb / o_pp - 1) < 0.008).all())
    mh = st_raw["HOURS"].astype(float)
    dim = [((dt.date(int(y), int(m_), 28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)).day
           for y, m_ in zip(st_raw["STMT_YEAR"], st_raw["MONTH"])]
    check("Z no statement month's hours exceed the month's", (mh <= 24 * np.array(dim) + 1e-6).all())
    check("Z the newer database's reports arrive after their tests and before its 9 February 2027 extract",
          (pd.to_datetime(new_["Report Received"]) > pd.to_datetime(new_["Test Date"])).all() and
          pd.to_datetime(new_["Report Received"]).max() <= pd.Timestamp("2027-02-09"))
    bd = pd.to_datetime(pd.read_csv(os.path.join(TARGET, P.FILES["billing"]), dtype=str)["BILL_DATE"], format="%m/%d/%Y")
    check("Z no extract runs past its own date: bills issued by 8 February 2027, inspections by 12 February, the "
          "compliance log and the statements within 2026",
          bd.max() <= pd.Timestamp("2027-02-08") and insp["date"].max() <= dt.date(2027, 2, 12) and
          evd["date"].max() <= dt.date(2026, 12, 31) and st_raw["STMT_YEAR"].astype(int).max() == 2026)
    chain = all((g.sort_values("READ_FROM")["READ_FROM"].to_numpy()[1:] ==
                 g.sort_values("READ_FROM")["READ_TO"].to_numpy()[:-1]).all() for _, g in bl.groupby("METER_NO"))
    check("Z every meter's read periods chain from bill to bill", chain)
    check("Z the heat table's Btu/scf is its therms a CCF times 1,000 to the whole Btu",
          (abs(heat["BTU_FACTOR"].astype(float) * 1000 - heat["HEAT_CONTENT_BTU_SCF"].astype(float)) <= 0.5).all())
    under = []
    for d_, g in insp.groupby("DEVICE_NO"):
        if d_ in repl:
            continue
        g = g.sort_values("date")
        lg = logs[(logs["device"] == d_) & (logs["date"] >= g.iloc[0]["date"]) & (logs["date"] < g.iloc[1]["date"]) &
                  ~logs["purpose"].str.startswith("Emergency")]
        under.append(sum(B._as_hmm(v_) for v_ in lg["value"]) <= g.iloc[1]["read"] - g.iloc[0]["read"])
    check("Z every engine's log sums below its meter's advance over each inspection round", all(under))
    check("Z no facility figure is a round figure before rounding", all(abs(gold[n] - round(gold[n])) > 0.01
                                                                       for n in B.ORDER))
    import csv as _csv
    gcsv = list(_csv.DictReader(open(os.path.join(TASK, "golden", "tbapcd_nox_inventory_2026.csv"), encoding="utf-8")))
    check("Z the golden CSV carries the 14 whole tons in Appendix A order",
          [r["facility"] for r in gcsv] == B.ORDER and [int(r["rule_4306_nox_tons_2026"]) for r in gcsv] ==
          [gw[n] for n in B.ORDER])

    n_fail = sum(1 for _, ok in RESULTS if not ok)
    print("%s  task478 checks: %d assertions, %d failed" % ("PASS" if not n_fail else "FAIL", len(RESULTS), n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
