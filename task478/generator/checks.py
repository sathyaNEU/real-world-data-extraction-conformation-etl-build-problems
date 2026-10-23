"""task478's assertions on the cut pack and the generator's clean truth: the three rules (R1 to R3c), every semantic fork
row (SF1 to SF21), the ladder, the golden's licensed family and margins, the asks' devices, the separation line, the
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
GOLD = ["Wexley Point Energy Center", "Ashgrove Refining", "Valmora Glass Works", "Sedge Hollow Landfill Gas",
        "St. Aldric Medical Center"]
DEFAULT = ["Wexley Point Energy Center", "Ashgrove Refining", "Valmora Glass Works", "Haskett Ridge Compressor Station",
           "Lindqvist Paperboard"]
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


def power_law(I):
    rows = I.test_rows()
    keys = sorted({r[0] for r in rows})
    best = None
    for q in (0.7, 0.85, 1.0, 1.15, 1.3, 1.5):
        X = np.zeros((len(rows), len(keys) + 1))
        y = np.zeros(len(rows))
        for i, (d, h, m, _) in enumerate(rows):
            X[i, keys.index(d)] = 1
            X[i, -1] = (h / 1e4) ** q
            y[i] = np.log(m)
        c, *_ = np.linalg.lstsq(X, y, rcond=None)
        sse = float(np.sum((y - X @ c) ** 2))
        if best is None or sse < best[0]:
            best = (sse, q, {d: c[keys.index(d)] for d in keys}, c[-1])
    _, q, a, cc = best
    return fac_tons(I, {d: B.integrate(I, d, lambda h, day, a=a[d]: np.exp(a + cc * (h / 1e4) ** q)) for d in I.open})


def binned(I, width=2000):
    rows = I.test_rows()
    keys = sorted({r[0] for r in rows})
    edges = np.arange(0, 30001, width)
    nb = len(edges) - 1
    X = np.zeros((len(rows), len(keys) + nb - 1))
    y = np.zeros(len(rows))
    for i, (d, h, m, _) in enumerate(rows):
        X[i, keys.index(d)] = 1
        k = min(int(h // width), nb - 1)
        if k > 0:
            X[i, len(keys) + k - 1] = 1
        y[i] = np.log(m)
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    offs = np.concatenate([[0.0], c[len(keys):]])
    mids = edges[:-1] + width / 2
    return fac_tons(I, {d: B.integrate(I, d, lambda h, day, a=c[keys.index(d)]: np.exp(a + np.interp(h, mids, offs)))
                        for d in I.open})


def variant(I, test_shift=0.0, day_at=0.5, month_step=False):
    """The golden with its conventions moved: catalyst hours at a test read later in the day, the day's rate read at
    another point in the day, or each month's hours all counted at the month's start."""
    cat = I.cat
    if month_step:
        cat = {}
        for d in I.open:
            c, out = I.cat[d], {}
            for day in c:
                out[day] = c[day.replace(day=1)]
            cat[d] = out
    rows = []
    for r in I.tests.itertuples():
        if r.device in cat:
            rows.append((r.device, cat[r.device][r.date] + test_shift * I.hours[r.device].get(r.date, 0.0),
                         r.lb_mmbtu, r.date))
    lv, b, _ = B.fit_climb(rows)
    out = {}
    for d in I.open:
        tot = 0.0
        for day, hi in I.heat[d].items():
            if day.year == B.YEAR and hi > 0:
                tot += hi * np.exp(lv[d] + b[d] * (cat[d][day] + I.hours[d][day] * day_at))
        out[d] = tot
    return fac_tons(I, out)


def truth_routes(e):
    """The clean truth: every unit's tests, its true daily hours and its catalyst's hours before any file is written."""
    U = e["units"]
    hi26 = {d: sum(v for x, v in U[d]["hours"].items() if x.year == W.YEAR) * W.heat_rate(d) for d in W.OPEN}

    def fac(unit_lb):
        f = {}
        for d in W.UNIT:
            v = unit_lb[d] if d in unit_lb else U[d]["nox_2026"]
            n = W.FAC_NAME[W.UNIT[d]["facility"]]
            f[n] = f.get(n, 0.0) + v / 2000.0
        return f
    out = {"truth": fac({})}
    out["latest"] = fac({d: hi26[d] * max(U[d]["tests"], key=lambda t: t["date"])["measured"] for d in W.OPEN})
    rows = [(d, t["cat_hours"], t["measured"], t["date"]) for d in W.OPEN for t in U[d]["tests"]]
    lv, b, _ = B.fit_climb(rows)
    hr = {d: W.heat_rate(d) for d in W.OPEN}

    def integ(d):
        hrs, cat = U[d]["hours"], U[d]["cat"]
        return sum(hrs[x] * hr[d] * np.exp(lv[d] + b[d] * (cat[x] + hrs[x] / 2)) for x in hrs
                   if x.year == W.YEAR and hrs[x] > 0)
    out["climb"] = fac({d: integ(d) for d in W.OPEN})
    return out


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    I = B.Inputs(TARGET)
    gold = B.facility_tons(I, "golden")
    gw = whole(gold)
    five = B.five(gold)
    e = W.everything()

    # ---------------------------------------------------------------- R1: the field's raw material ships
    cems = pd.read_csv(os.path.join(TARGET, P.FILES["cems"]), dtype=str)
    check("R1 the CEMS export ships one row per operating hour of the nine monitored units (%d rows)" % len(cems),
          len(cems) > 25000 and cems.groupby(["facility_id", "unit_id"]).ngroups == 9)
    check("R1 the two source test databases ship %d tests of the %d unmonitored units" % (len(I.tests), len(I.open)),
          len(I.tests) == f["components"]["tests"] and set(I.tests["device"]) == set(I.open))
    heads = []
    for k, fn in P.FILES.items():
        p = os.path.join(TARGET, fn)
        if fn.endswith(".csv"):
            heads += open(p, encoding="utf-8").readline().strip().lower().split(",")
        elif fn.endswith(".xlsx"):
            import openpyxl
            for ws in openpyxl.load_workbook(p, read_only=True).worksheets:
                for row in ws.iter_rows(min_row=1, max_row=2, values_only=True):
                    heads += [str(v).lower() for v in row if v is not None]
    check("R1 no shipped column holds a unit's 2026 rate, its catalyst hours, a climb, an age or a facility total",
          not any(re.search(r"catalyst|\bage\b|climb|deterior|2026 rate|\bannual\b|\btotal\b|represent|degrad", h)
                  for h in heads))
    docs = (pdf_text("plan") + " " + pdf_text("guidance")).lower()
    check("R1 neither document says a rate moves with a catalyst's hours or that a test is unrepresentative",
          not re.search(r"catalyst (age|hours)|deteriorat|degrad|climb|unrepresentative|operating hours on", docs))

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    tr = truth_routes(e)
    check("R3a the easy route on the clean truth (each unit's latest test across its 2026 heat input, every filed rule "
          "applied) files the default path's five: %s" % B.five(tr["latest"]), B.five(tr["latest"]) == DEFAULT)
    check("R3b the decisive step alone on the clean truth (the units' tests fitted on their catalysts' hours, one "
          "climb, each unit its level, integrated over each day) files the golden five", B.five(tr["climb"]) == GOLD)
    check("R3 the generator's true 2026 NOx puts the golden five on top (fifth over sixth %.3f)" % margin(tr["truth"]),
          B.five(tr["truth"]) == GOLD and margin(tr["truth"]) > 1.15)
    truth = {W.FAC_NAME[c]: v for c, v in e["facility_tons"].items()}
    dev = max(abs(gold[n] - truth[n]) for n in B.ORDER)
    check("R3 every golden facility figure sits within 0.25 tons of the true 2026 NOx (largest gap %.3f)" % dev,
          dev < 0.25 and gw == whole(truth))
    lat = B.facility_tons(I, "latest")
    check("R3a the default path on the cut pack files the same five", B.five(lat) == DEFAULT)
    keys = [(r.device, r.date) for r in I.tests.itertuples()]
    old_ = pd.read_csv(os.path.join(TARGET, P.FILES["tests_old"]), dtype=str)
    new_ = pd.read_excel(os.path.join(TARGET, P.FILES["tests_new"]), sheet_name="Results")
    check("R3c no plant: no unit has two tests on one day and no test repeats another's ppm, lb/hr and fuel or heat "
          "input", len(set(keys)) == len(keys) and not old_.duplicated(["NOX_PPMVD", "NOX_LB_HR", "FUEL_FLOW_SCFH"]).any()
          and not new_.duplicated(["NOx (ppmvd @ ref O2)", "NOx (lb/hr)", "Heat Input (MMBtu/hr)"]).any())
    st = pd.read_csv(os.path.join(TARGET, P.FILES["statements"]), dtype=str)
    rep = st.groupby(["DEVICE_NO", "STMT_YEAR"])["HOURS"].apply(lambda s: ",".join(s)).reset_index()
    check("R3c no plant: no unit's year of monthly hours repeats another year's", not rep.duplicated(["DEVICE_NO", "HOURS"]).any())

    # ---------------------------------------------------------------- R2: every Layer 1 item, mishandled
    Ip = B.Inputs(TARGET, conv="ppm")
    check("R2a the older tests through Method 19 from ppm in place of lb/hr over heat input: the call and the 14 whole "
          "tons (SF6)", whole(B.facility_tons(Ip, "golden")) == gw)
    st_raw = pd.read_csv(os.path.join(TARGET, P.FILES["statements"]), dtype=str)
    bad = st_raw.copy()
    bad.loc[bad["HHV_BTU_SCF"].notna(), "HHV_BTU_SCF"] = "1037"
    dB = subset(list(P.FILES))
    bad.to_csv(os.path.join(dB, P.FILES["statements"]), index=False)
    check("R2b landfill and digester gas at the natural gas heating value leaves the call (SF5)",
          B.five(B.facility_tons(B.Inputs(dB), "golden")) == GOLD)
    shutil.rmtree(dB)
    utc = cems.copy()
    ts = pd.to_datetime(utc["op_date"]) + pd.to_timedelta(utc["op_hour"].astype(int), unit="h") + pd.Timedelta(hours=8)
    keep = ts.dt.year == 2026
    lb_utc = {}
    pm = B.read_permits(TARGET)
    key = {(r.FAC_NO, r.CEMS_UNIT_ID): r.DEVICE_NO for r in pm.itertuples() if isinstance(r.CEMS_UNIT_ID, str)}
    for (fa, un), g in utc[keep].groupby(["facility_id", "unit_id"]):
        lb_utc[key[(fa, un)]] = g["nox_mass_lb"].astype(float).sum()
    f_utc = fac_tons(I, {**B.unit_lb(I, "golden"), **lb_utc})
    check("R2c the CEMS hours read as UTC leave the call and the 14 whole tons (SF3)", whole(f_utc) == gw)
    sub = {k: g["nox_mass_lb"].astype(float).sum() for k, g in
           cems[cems["nox_rate_modc"] != "12"].assign(dev=[key[(a, b)] for a, b in zip(
               cems[cems["nox_rate_modc"] != "12"]["facility_id"], cems[cems["nox_rate_modc"] != "12"]["unit_id"])])
           .groupby("dev")}
    check("R2d the substitute data hours dropped leave the call (SF4)", B.five(fac_tons(I, {**B.unit_lb(I, "golden"),
                                                                                            **sub})) == GOLD)
    old = pd.read_csv(os.path.join(TARGET, P.FILES["tests_old"]), dtype=str)
    check("R2e Haskett Ridge's tests and statements under its old number 0705 carry its device numbers (SF10)",
          set(old[old["FAC_NO"] == "705"]["DEVICE_NO"]) <= {"1501", "1502", "1503"} and
          set(st_raw[st_raw["FAC_NO"] == "0705"]["DEVICE_NO"]) == {"D-1501", "D-1502", "D-1503"})
    ev = B.read_events(TARGET)
    cats_dm = {}
    for r in ev[ev["EVENT_TYPE"].isin(["SCR INSTALLED", "CATALYST"])].itertuples():
        d = r.date
        if "/" in r.EVENT_DATE and d.day <= 12:
            d = dt.date(d.year, d.day, d.month)
        cats_dm.setdefault(r.DEVICE_NO, []).append(d)
    Idm = B.Inputs(TARGET)
    Idm.cats = {k: sorted(v) for k, v in cats_dm.items()}
    Idm.cat = {d: B.cat_hours(Idm.hours[d], Idm.cats.get(d, [])) for d in Idm.open}
    check("R2f the event log's month-first dates up to 2020 read day first leave the call (SF13)",
          B.five(B.facility_tons(Idm, "golden")) == GOLD)

    # ---------------------------------------------------------------- the ladder
    check("L0 each unit's latest test across its 2026 heat input files %s" % ", ".join(n.split()[0] for n in B.five(lat)),
          B.five(lat) == DEFAULT)
    reflex = {m: B.facility_tons(I, m) for m in ("mean", "median", "max", "last2", "limit", "caltrend", "calendar_age")}
    for m, v in reflex.items():
        check("L1 the %s route misses the golden five (%s)" % (m, ", ".join(n.split()[0] for n in B.five(v))),
              B.five(v) != GOLD)
    since = {}
    for r in I.tests.sort_values("date").itertuples():
        since.setdefault(r.device, [])
        if r.date >= max(c for c in I.cats[r.device] if c <= r.date):
            since[r.device].append(r)
    post = {}
    for d in I.open:
        last_cat = max(I.cats[d])
        ok = [r for r in since[d] if r.date >= last_cat]
        r = ok[-1] if ok else I.tests[I.tests["device"] == d].sort_values("date").iloc[-1]
        post[d] = I.hi26[d] * (r.lb_mmbtu if ok else r["lb_mmbtu"])
    check("L2 the latest test on each unit's current catalyst (the latest test where none) misses the golden five",
          B.five(fac_tons(I, post)) != GOLD)
    check("L the default path keeps the five's whole tons at most at Wexley Point, Valmora and Ashgrove (%d of 14 "
          "whole tons)" % sum(whole(lat)[n] == gw[n] for n in B.ORDER), sum(whole(lat)[n] == gw[n] for n in B.ORDER) <= 11)

    # ---------------------------------------------------------------- the golden and its licensed family
    check("G1 the golden five: %s" % five, five == GOLD and f["call"]["facilities"] == GOLD)
    check("G1 figures.json carries the 14 whole tons", all(f["facilities"][n]["nox_tons"] == gw[n] for n in B.ORDER))
    fam = {"pooled": gold, "by kind": B.facility_tons(I, "bykind"), "since 2022": B.facility_tons(I, "since2022"),
           "anchored on the latest test": B.facility_tons(I, "anchor"), "power law": power_law(I),
           "binned": binned(I), "binned 3,000 h": binned(I, 3000), "Method 19": B.facility_tons(Ip, "golden")}
    check("G2 every licensed member (%s) files the golden five" % ", ".join(fam),
          all(B.five(v) == GOLD for v in fam.values()))
    check("G2 every licensed member prints the same 14 whole tons", all(whole(v) == gw for v in fam.values()))
    lm = min(edge(v) for v in fam.values())
    check("G3 every member's every figure sits 0.04 tons or more from a rounding half (least %.3f) (SF11)" % lm, lm >= 0.04)
    mm = min(margin(v) for v in fam.values())
    check("G4 fifth clears sixth by 15 per cent or more under every member (least %.3f) (SF12)" % mm, mm >= 1.15)
    lv, b, sd = B.fit_climb(I.test_rows())
    beta = list(b.values())[0]
    lin = [(d, h, lb, t) for d, h, lb, t in I.test_rows()]
    keys_ = sorted({r[0] for r in lin})
    X = np.zeros((len(lin), len(keys_) + 1))
    y = np.zeros(len(lin))
    for i, (d, h, lb, _) in enumerate(lin):
        X[i, keys_.index(d)] = 1
        X[i, -1] = h
        y[i] = lb
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    rel = float(np.std((y - X @ c) / y))
    check("G5 the tests refute an additive climb (relative residual sd %.3f against the log fit's %.3f)" % (rel, sd),
          rel > 2 * sd)
    check("G5 the fitted climb: %.2f in the log a 10,000 hours, %d per cent a 1,000 (figures.json)"
          % (beta * 1e4, f["components"]["climb_pct_per_1000h"]),
          "%.2f" % (beta * 1e4) == f["components"]["climb_log_per_10000h"] and abs(beta - W.BETA) < 0.05 * W.BETA)
    six = sorted(B.ORDER, key=lambda n: -gold[n])[5]
    check("G6 sixth as figures.json states (%s, %d)" % (six, gw[six]), f["components"]["sixth"]["name"] == six and
          f["components"]["sixth"]["tons"] == gw[six])

    # ---------------------------------------------------------------- SF1 to SF21
    new = pd.read_excel(os.path.join(TARGET, P.FILES["tests_new"]), sheet_name="Results")
    m19 = new["NOx (ppmvd @ ref O2)"] * 1.194e-7 * [B.FD[pm.set_index("DEVICE_NO").loc[d_, "FUEL"]] for d_ in new["Device No."]] \
        * 20.9 / (20.9 - new["Ref O2 (%)"])
    check("SF1 the newer database's lb/MMBtu is Method 19's NO2 figure from its ppm, within the two columns' printed "
          "precision", (abs(m19 / new["NOx (lb/MMBtu)"] - 1) < 0.004).all())
    eng = B.engine_lb(TARGET)
    with_eng = {n: gold[n] + eng[n] / 2000.0 for n in B.ORDER}
    check("SF2 the emergency engines added to each facility leave the call; the Rule 4307 units have no fuel record",
          B.five(with_eng) == GOLD and not set(pm[pm["RULE"] == "4307"]["DEVICE_NO"]) & set(st_raw["DEVICE_NO"]))
    check("SF3 the CEMS hours on UTC (R2c)", whole(f_utc) == gw)
    check("SF4 the substitute data hours dropped (R2d)", B.five(fac_tons(I, {**B.unit_lb(I, "golden"), **sub})) == GOLD)
    check("SF5 landfill and digester gas at 1,037 Btu/scf (R2b)", True)
    check("SF6 the older tests through Method 19 give the same 14 whole tons (R2a)", whole(fam["Method 19"]) == gw)
    v7 = variant(I, test_shift=1.0)
    check("SF7 catalyst hours at the end of the test day in place of its start: the same 14 whole tons", whole(v7) == gw)
    v8 = variant(I, day_at=0.0)
    check("SF8 each day's rate at the day's start in place of mid-day: the same 14 whole tons", whole(v8) == gw)
    v9 = variant(I, month_step=True)
    check("SF9 each month's hours counted at the month's start in place of spread over its days: the same 14 whole "
          "tons", whole(v9) == gw)
    check("SF10 every test and statement row joins a Rule 4306 device of the permit list",
          set(I.tests["device"]) <= set(I.devices) and set(st_raw["DEVICE_NO"]) <= set(I.devices))
    check("SF11 no figure at a half (G3)", lm >= 0.04)
    check("SF12 no tie for fifth (G4)", mm >= 1.15)
    check("SF13 the month-first dates read day first (R2f)", B.five(B.facility_tons(Idm, "golden")) == GOLD)
    ga = B.gas_2026(TARGET)
    gwa = {n: B.hround(ga[n]) for n in B.ORDER}
    reads = B.gas_2026(TARGET, "reads")
    check("SF14 plan 4.2 files the billed usage; the meter reads in its place move %d of 14 gas figures"
          % sum(B.hround(reads[n]) != gwa[n] for n in B.ORDER), sum(B.hround(reads[n]) != gwa[n] for n in B.ORDER) >= 9
          and "billed usage spread evenly over the days of its read period, from the day of its prior read to the day "
          "before its current read" in pdf_text("plan"))
    bl = B.read_billing(TARGET)
    cut = B.conversion(bl)
    alt = {n: 0.0 for n in B.ORDER}
    for r in bl.itertuples():
        therms = r.USAGE_CCF if r.READ_TO >= cut else r.USAGE_CCF * r.BTU_FACTOR
        n_ = (r.READ_TO - r.READ_FROM).days
        a_ = max(r.READ_FROM + dt.timedelta(days=1), B.D0)
        z_ = min(r.READ_TO + dt.timedelta(days=1), B.D1)
        alt[r.facility] += therms * max(0, (z_ - a_).days) / n_ / 10.0
    check("SF15 the read period from the day after the prior read through the current read moves gas figures, and plan "
          "4.2 files the other (%d moved)" % sum(B.hround(alt[n]) != gwa[n] for n in B.ORDER),
          sum(B.hround(alt[n]) != gwa[n] for n in B.ORDER) > 0)
    check("SF16 therms to MMBtu at 10 (guidance section 4)", "therms divided by 10" in pdf_text("guidance"))
    check("SF17 every billing line's service address matches exactly one Appendix A facility (%d lines)" % len(bl),
          bl["facility"].notna().all() and bl.groupby("METER_NO")["facility"].nunique().max() == 1)
    eb = B.engine_lb(TARGET)
    ebw = {n: B.hround(eb[n]) for n in B.ORDER}
    insp = pd.read_csv(os.path.join(TARGET, P.FILES["inspections"]), dtype=str)
    insp["date"] = [dt.date.fromisoformat(x) for x in insp["INSPECTION_DATE"]]
    insp["read"] = insp["HOUR_METER"].astype(float)
    logs = B.read_engine_logs(TARGET)
    hmm = B.hmm_facilities(TARGET)
    repl = B.replacements(TARGET)
    meter_lb = {n: 0.0 for n in B.ORDER}
    pmi = pm.set_index("DEVICE_NO")
    for d_, g in insp.groupby("DEVICE_NO"):
        g = g.sort_values("date")
        n_ = B.FAC_OF_NO[g.iloc[0]["FAC_NO"]]
        lg = logs[logs["device"] == d_]
        hrs_log = sum(B._as_hmm(v) if n_ in hmm else v for v in lg["value"])
        span = g.iloc[1]["read"] - g.iloc[0]["read"]
        if d_ in repl:
            continue
        scale = span / hrs_log if hrs_log else 1.0
        bhp, tier = float(pmi.loc[d_, "RATING"]), pmi.loc[d_, "ENGINE_TIER"]
        meter_lb[n_] += hrs_log * scale * bhp * B.ENGINE_LF * B.TIER_NOX[tier] / B.G_LB
    for d_, (rd, ob, ot) in repl.items():
        n_ = B.FAC_OF_NO[pmi.loc[d_, "FAC_NO"]]
        lg = logs[logs["device"] == d_]
        for r in lg.itertuples():
            h = B._as_hmm(r.value) if n_ in hmm else r.value
            bhp, tier = (ob, ot) if r.date < rd else (float(pmi.loc[d_, "RATING"]), pmi.loc[d_, "ENGINE_TIER"])
            meter_lb[n_] += h * bhp * B.ENGINE_LF * B.TIER_NOX[tier] / B.G_LB
    moved = sum(B.hround(meter_lb[n]) != ebw[n] for n in B.ORDER)
    check("SF18 guidance 6 takes the hours the logs record; the hour meters, which run through warm-up and cool-down, "
          "in their place move %d of the 13 facilities without a replacement-only engine set" % moved, moved >= 10 and
          "Operating hours are the hours the facility's Rule 4702 log records" in pdf_text("guidance"))
    alt_g = {n: eb[n] * B.G_LB / 453.59237 for n in B.ORDER}
    check("SF19 453.59237 g/lb in place of the guidance's 453.6 moves %d whole pounds, and the guidance writes 453.6"
          % sum(B.hround(alt_g[n]) != ebw[n] for n in B.ORDER), "453.6 g/lb" in pdf_text("guidance"))
    near = [(d_, r.date) for d_, (rd, _, _) in repl.items() for r in logs[logs["device"] == d_].itertuples()
            if rd - dt.timedelta(days=4) <= r.date <= rd]
    check("SF20 no replaced engine has a run on its replacement date or in the four days before it", not near)
    dC = subset(["cems", "tests_old", "tests_new", "statements", "permits", "events"])
    s21 = B.facility_tons(B.Inputs(dC), "golden")
    shutil.rmtree(dC)
    check("SF21 the call and the 14 whole tons from the CEMS export, the test databases, the statements, the permit "
          "list and the event log alone", whole(s21) == gw)

    # ---------------------------------------------------------------- ask A: the gas delivered
    truth_g = {W.FAC_NAME[c]: v for c, v in e["gas_2026"].items()}
    check("A the golden's gas figures are the generator's billed therms, spread by plan 4.2, on all 14",
          all(gwa[n] == B.hround(truth_g[n]) for n in B.ORDER) and all(f["facilities"][n]["gas_mmbtu"] == gwa[n]
                                                                        for n in B.ORDER))
    rungs = {h: B.gas_2026(TARGET, h) for h in ("all_ccf", "all_therms", "reads", "by_line", "no_split")}
    mv = {h: sum(B.hround(v[n]) != gwa[n] for n in B.ORDER) for h, v in rungs.items()}
    check("A every rung moves the corrector facilities' figures at least (%s)" % ", ".join("%s %d" % kv for kv in mv.items()),
          mv["all_ccf"] == 14 and mv["all_therms"] == 14 and mv["no_split"] == 14 and mv["reads"] >= 9 and
          mv["by_line"] >= 9)
    check("A fair: the index-billed meters' lines are CCF up to %s and therms from it, each line by its own identity"
          % (cut - dt.timedelta(days=1)), cut == W.CONVERSION and all(
              B.is_therm_line(r) == (r.READ_TO >= cut) for r in bl[bl["PRESSURE_MULT"].notna()].itertuples()))
    evc = bl[bl["PRESSURE_MULT"].isna()].sort_values(["METER_NO", "READ_TO"])
    jumps, cont, steps = [], [], []
    for m_, g in evc.groupby("METER_NO"):
        g = g[(g["CURRENT_READ"] > g["PRIOR_READ"])]
        after = (g["READ_TO"] >= cut).to_numpy()
        ratio = (g["USAGE_CCF"] / (g["CURRENT_READ"] - g["PRIOR_READ"])).to_numpy()
        adj = ratio / np.where(after, g["BTU_FACTOR"].to_numpy(), 1.0)
        i = int(np.argmax(after))
        if 0 < i:
            jumps.append(ratio[i] / ratio[i - 1] - 1)
            cont.append(abs(adj[i] / adj[i - 1] - 1))
            steps += [abs(adj[k] / adj[k - 1] - 1) for k in range(1, len(adj))]
    check("A fair: every corrector meter's usage per index unit steps up %.3f to %.3f at the first therm bill, and read "
          "as therms its series runs on (step at most %.4f, every month-to-month move at most %.4f)"
          % (min(jumps), max(jumps), max(cont), max(steps)),
          len(jumps) >= 9 and min(jumps) > 0.015 and max(cont) < 0.006 and max(steps) < 0.01)
    check("A no marker: the bill ids, rate codes, read types and columns run unchanged across %s" % cut,
          bl["READ_TYPE"].nunique() == 1 and set(bl[bl["READ_TO"] >= cut]["RATE_CODE"]) == set(bl["RATE_CODE"]))
    check("A every facility has lines on both sides of the conversion",
          all(((g["READ_TO"] < cut).any() and (g["READ_TO"] >= cut).any()) for _, g in bl.groupby("facility")))

    # ---------------------------------------------------------------- ask B: the emergency engines
    truth_e = {W.FAC_NAME[c]: v for c, v in e["engine_lb"].items()}
    check("B the golden's engine figures are the generator's on all 14",
          all(ebw[n] == B.hround(truth_e[n]) for n in B.ORDER) and all(f["facilities"][n]["engine_nox_lb"] == ebw[n]
                                                                        for n in B.ORDER))
    eh = {h: B.engine_lb(TARGET, h) for h in ("decimal", "current", "naive")}
    mvb = {h: sum(B.hround(v[n]) != ebw[n] for n in B.ORDER) for h, v in eh.items()}
    check("B the decimal reading moves the seven hours-and-minutes facilities, the current engine the seven with a "
          "replacement, both all 14 (%s)" % ", ".join("%s %d" % kv for kv in mvb.items()),
          mvb == {"decimal": 7, "current": 7, "naive": 14})
    check("B fair: the hour meters pick out the seven facilities whose logs hold hours and minutes",
          {n for n in hmm} == {W.FAC_NAME[c] for c in W.HMM})
    gap_d, gap_h = [], []
    for d_, g in insp.groupby("DEVICE_NO"):
        if d_ in repl:
            continue
        g = g.sort_values("date")
        n_ = B.FAC_OF_NO[g.iloc[0]["FAC_NO"]]
        lg = logs[(logs["device"] == d_) & (logs["date"] >= g.iloc[0]["date"]) & (logs["date"] < g.iloc[1]["date"])]
        span = g.iloc[1]["read"] - g.iloc[0]["read"]
        (gap_h if n_ in hmm else gap_d).append(sum(B._as_hmm(v) if n_ in hmm else v for v in lg["value"]) / span)
    check("B fair, no oracle: read their own way every engine's log sits 85 to 98 per cent of its meter (%.3f to %.3f), "
          "so the meter arbitrates and hands over no figure" % (min(gap_d + gap_h), max(gap_d + gap_h)),
          min(gap_d + gap_h) > 0.85 and max(gap_d + gap_h) < 0.98)
    check("B fair: the compliance log's EQUIPMENT entries name the seven replaced engines' old rating and tier",
          {d_: (v[1], v[2]) for d_, v in repl.items()} ==
          {d_: (en["replaced"][1], en["replaced"][2]) for d_, en in W.ENGINE.items() if en["replaced"]})
    first = insp.groupby("DEVICE_NO")["date"].min()
    check("B silent: no replaced engine's hour meter is read before its replacement, so no meter restarts",
          all(first[d_] > rd for d_, (rd, _, _) in repl.items()))
    vals = logs.assign(frac=(logs["value"] * 100).round().astype(int) % 100)
    check("B no marker: both log layouts hold values with a fraction under .60 (the hours-and-minutes sheets' values are "
          "a subset of what a decimal log writes)", (vals[~vals["facility"].isin(hmm)]["frac"] < 60).mean() > 0.5)

    # ---------------------------------------------------------------- separation and distractors
    dX = subset([k for k in P.FILES if k not in ("cems", "tests_old", "tests_new", "statements")])
    check("X1 the asks read no CEMS hour, source test or emission statement: both from the other files",
          {n: B.hround(v) for n, v in B.gas_2026(dX).items()} == gwa and
          {n: B.hround(v) for n, v in B.engine_lb(dX).items()} == ebw)
    shutil.rmtree(dX)
    check("X2 the call reads no billing line, engine log or inspection (SF21)", whole(s21) == gw)
    eqd = set(ev[ev["EVENT_TYPE"] == "EQUIPMENT"]["DEVICE_NO"])
    check("X3 every ask device row sits outside the call's population: the EQUIPMENT entries on Rule 4702 engines only",
          eqd <= set(pm[pm["RULE"] == "4702"]["DEVICE_NO"]))
    dD = subset([k for k in P.FILES if k not in ("no2", "onroad")])
    check("X4 the distractors deleted: the call, the 14 whole tons and both asks unchanged",
          whole(B.facility_tons(B.Inputs(dD), "golden")) == gw and
          {n: B.hround(v) for n, v in B.gas_2026(dD).items()} == gwa and
          {n: B.hround(v) for n, v in B.engine_lb(dD).items()} == ebw)
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
    o_lb = old["NOX_LB_HR"].astype(float) / (old["FUEL_FLOW_SCFH"].astype(float) * old["FUEL_HHV"].astype(float) / 1e6)
    o_pp = [float(p_) * 1.194e-7 * B.FD[pmi.loc["D-" + d_, "FUEL"]] * 20.9 / (20.9 - float(o2))
            for p_, d_, o2 in zip(old["NOX_PPMVD"], old["DEVICE_NO"], old["O2_REF"])]
    check("Z the older tests' lb/hr and ppm agree through Method 19 within their printed precision",
          (abs(o_lb / np.array(o_pp) - 1) < 0.01).all())
    mh = st_raw["HOURS"].astype(float)
    dim = [((dt.date(int(y), int(m_), 28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)).day
           for y, m_ in zip(st_raw["STMT_YEAR"], st_raw["MONTH"])]
    check("Z no statement month's hours exceed the month's", (mh <= 24 * np.array(dim) + 1e-6).all())
    chain = all((g["PRIOR_READ"].to_numpy()[1:] == g["CURRENT_READ"].to_numpy()[:-1]).all()
                for _, g in bl.sort_values("READ_FROM").groupby("METER_NO"))
    check("Z every meter's reads chain from bill to bill", chain)
    check("Z the newer database's reports arrive after their tests and before its 9 February 2027 extract",
          (pd.to_datetime(new["Report Received"]) > pd.to_datetime(new["Test Date"])).all() and
          pd.to_datetime(new["Report Received"]).max() <= pd.Timestamp("2027-02-09"))
    bd = pd.to_datetime(pd.read_csv(os.path.join(TARGET, P.FILES["billing"]), dtype=str)["BILL_DATE"], format="%m/%d/%Y")
    check("Z no extract runs past its own date: bills issued by 3 February 2027, inspections by 12 February, the "
          "compliance log and the statements within 2026",
          bd.max() <= pd.Timestamp("2027-02-03") and insp["date"].max() <= dt.date(2027, 2, 12) and
          ev["date"].max() <= dt.date(2026, 12, 31) and st_raw["STMT_YEAR"].astype(int).max() == 2026)
    nov = ev[ev["EVENT_TYPE"] == "NOV"]
    fails = int((new["Result"] == "FAIL").sum() + (old["RESULT"] == "FAIL").sum())
    check("Z every failed test has its notice of violation (%d) and a retest notification" % fails, len(nov) == fails and
          (ev["DESCRIPTION"].str.startswith("Retest")).sum() >= fails - 1)
    check("Z no facility figure is a round figure before rounding", all(abs(gold[n] - round(gold[n])) > 0.01 for n in B.ORDER))
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
