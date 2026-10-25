"""task170 generator checks: input gates, the three-rules block on the clean truth (the analyst test executed), the
own-count family against the bin, the ladder and its clearances, every semantic fork row, every Layer 1 item, the
ask devices on every route, separation, documents and realism. Exit 1 on any failure.

    python3 task170/generator/checks.py [target]"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C      # noqa: E402
import calc             # noqa: E402
import deliver          # noqa: E402
import docs as D        # noqa: E402
import world as W       # noqa: E402

FAILS = []
N = [0]


def ok(name, cond, detail=""):
    N[0] += 1
    print("%s  %-60s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAILS.append(name)


def inbin(x, centre):
    return deliver.r250(x) == centre


def clearance(x, lo=1125.0, hi=1375.0):
    return lo / x if x < lo else (x / hi if x >= hi else 0.0)


# ------------------------------------------------------------------ the own-count family
FORMS = {
    "power": (lambda t, x: np.exp(t[2]) + np.exp(t[0]) * (x + 1) ** (-np.exp(t[1])), np.log([0.03, 0.6, 0.002])),
    "shifted_power": (lambda t, x: np.exp(t[3]) + np.exp(t[0]) * (1 + x / np.exp(t[2])) ** (-np.exp(t[1])),
                      np.log([0.02, 1.5, 50, 0.002])),
    "exp_floor": (lambda t, x: np.exp(t[2]) + np.exp(t[0]) * np.exp(-x / np.exp(t[1])), np.log([0.02, 80, 0.002])),
    "logit_log": (lambda t, x: 1 / (1 + np.exp(-(t[0] + t[1] * np.log1p(x)))), np.array([-3.0, -0.5])),
}


def fit_forms(T, E):
    k = np.arange(len(T))
    m = T > 0
    k, Tt, Et = k[m], T[m], E[m]

    def nll(p):
        p = np.clip(p, 1e-9, 1 - 1e-9)
        return -np.sum(Et * np.log(p) + (Tt - Et) * np.log(1 - p))
    out = {}
    for name, (f, t0) in FORMS.items():
        r = minimize(lambda t: nll(f(t, k)), t0, method="Nelder-Mead", options={"maxiter": 8000, "xatol": 1e-9, "fatol": 1e-9})
        r = minimize(lambda t: nll(f(t, k)), r.x, method="Nelder-Mead", options={"maxiter": 8000, "xatol": 1e-9, "fatol": 1e-9})
        out[name] = ((lambda x, f=f, t=r.x: f(t, np.asarray(x, float))), 2 * len(t0) + 2 * r.fun)
    return out


def pace_routes(s, e, p4):
    """each record driver's errors per start over the driver's own first twelve months against the driver's pace in
    them, Poisson on log pace (linear and quadratic), carried to each Phase 4 driver's pace"""
    import statsmodels.api as sm
    g = s.groupby("person")["t"].min()
    s2 = s.assign(t0=s["person"].map(g))
    in12 = s2["t"] < s2["t0"] + pd.Timedelta(days=365)
    fy = s2[in12].groupby("person").size()
    key = set(zip(s2.loc[in12, "person"], s2.loc[in12, "n"]))
    ee = e[[(p, int(n)) in key if n == n else False for p, n in zip(e["person"], e["n"])]]
    fe = ee.groupby("person").size().reindex(fy.index).fillna(0)
    pace = fy / 12.0
    fp = np.maximum(p4["starts"].values / 12.0, 0.5)
    X = sm.add_constant(np.log(pace.values))
    m1 = sm.GLM(fe.values, X, family=sm.families.Poisson(), offset=np.log(fy.values)).fit()
    X2 = sm.add_constant(np.column_stack([np.log(pace.values), np.log(pace.values) ** 2]))
    m2 = sm.GLM(fe.values, X2, family=sm.families.Poisson(), offset=np.log(fy.values)).fit()
    lf = np.log(fp)
    lin = float((np.exp(m1.params[0] + m1.params[1] * lf) * p4["starts"].values).sum())
    quad = float((np.exp(m2.params[0] + m2.params[1] * lf + m2.params[2] * lf ** 2) * p4["starts"].values).sum())
    return {"pace_poisson": lin, "pace_poisson_quadratic": quad}


def main(target):
    task = os.path.dirname(target)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    files = sorted(os.listdir(target))
    call_c = figs["call_tde_errors_phase4_first_12_months"]
    # ------------------------------------------------------------------ input gates
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted(set(f.rsplit(".", 1)[1] for f in files))
    ok("G2 three or more formats", len(fmts) >= 3, ", ".join(fmts))
    big = [f for f in files if f.endswith(".csv") and sum(1 for _ in open(os.path.join(target, f))) - 1 >= 25000]
    ok("G3 a file of 25,000 rows or more", bool(big), ", ".join(big))
    ok("G4 two or more distractors named", len(meta["distractor_files"]) >= 2, ", ".join(meta["distractor_files"]))
    src = open(os.path.join(HERE, "calc.py")).read()
    ok("G5 distractors unused by the golden", not any(x in src for x in ("F_PUNC", "F_WX", C.F_PUNC, C.F_WX)))
    ok("G6 every file has a source, date and licence", all(f in meta["sources"] for f in files))
    # ------------------------------------------------------------------ the call on the pack
    r = calc.compute(target)
    d, s, e, p4 = r["data"], r["starts"], r["errors"], r["p4"]
    call = r["call"]
    ok("R1 call printed", call_c == deliver.r250(call), "%.1f -> %d" % (call, deliver.r250(call)))
    lo, hi = call_c - 125, call_c + 125
    ok("R2 golden well inside its bin", lo + 60 <= call <= hi - 60, "%.1f in [%d, %d)" % (call, lo, hi))
    ok("CC1 drivers covered", figs["cc1_phase4_drivers"] == r["drivers"] == int((d["roster"]["Depot"].isin(C.P4_CODES)).sum()),
       "%d" % r["drivers"])
    st = r["starts_fwd"]
    ok("CC2 starts printed and mid-bin", figs["cc2_phase4_etcs_starts_first_12_months"] == deliver.r1000(st)
       and abs(st - deliver.r1000(st)) <= 400, "%.1f -> %d" % (st, deliver.r1000(st)))
    # ------------------------------------------------------------------ the three rules on the clean truth
    w = W.World()
    ok("R1a the recorder log ships every start at the driver's grain and no column holds a count of starts",
       set(d["som"].columns) == {"som_ref", "obr_utc", "unit", "cab", "driver_id", "som_type"}
       and len(d["som"]) == len(w.starts))
    ok("R1b no shipped column holds an error probability, a curve or a driver's practice",
       not any(re.search(r"prob|rate|curve|count_of|practice|experience|cumulative", c, re.I)
               for f in (d["som"], d["reg"], d["roster"], d["duty"]) for c in f.columns))
    T, E = r["T"], r["E"]
    fams = fit_forms(T, E)
    best = min(v[1] for v in fams.values())
    vals = {}
    for edges, nm in ((calc.BANDS, "bands of 50 (golden)"), ([0, 10, 25, 50, 100, 200, 400, 800, 1600, 10 ** 9], "bands, nine"),
                      ([0, 20, 60, 200, 600, 10 ** 9], "bands, five"), (list(range(0, 500, 25)) + [10 ** 9], "bands of 25"),
                      (list(range(0, 1000, 100)) + [10 ** 9], "bands of 100")):
        pf, _ = calc.band_rates(T, E, edges)
        vals[nm] = float(calc.run_along(pf, p4).sum())
    for nm, (pf, aic) in fams.items():
        vals[nm] = float(calc.run_along(pf, p4).sum())
    vals.update(pace_routes(s, e, p4))
    for nm, v in vals.items():
        ok("B1 own-count family: %s prints the call" % nm, inbin(v, call_c),
           "%.1f%s" % (v, (" (dAIC %.1f)" % (fams[nm][1] - best)) if nm in fams else ""))
    ok("B2 the family's spread inside one bin with margin", min(vals.values()) >= lo + 25 and max(vals.values()) <= hi - 25,
       "%.1f to %.1f" % (min(vals.values()), max(vals.values())))
    # truth: the world's own expected count for the Phase 4 drivers
    pid_of = {}
    for p in w.people:
        for _, num in p.numbers:
            pid_of[num] = p.pid
    last = calc.chain(d["xwalk"])
    prior_w = {p.pid: w.prior.get(p.pid, 0) for p in w.people}
    tru = 0.0
    for pers, n0, nn in zip(p4["person"], p4["prior"], p4["starts"]):
        pid = pid_of[pers]
        ok_prior = prior_w[pid] == n0
        if not ok_prior:
            ok("T0 prior starts agree with the world for %s" % pers, False, "%d vs %d" % (n0, prior_w[pid]))
        k = np.arange(int(n0), int(np.ceil(n0 + nn)))
        tru += float(W.p_err(k).sum()) * np.exp(W.CURVE["FRAIL"] ** 2 / 2)
    ok("T1 the golden sits by the world's expected count", inbin(tru, call_c) and abs(call - tru) / tru < 0.05,
       "golden %.1f, world %.1f" % (call, tru))
    # R3a the analyst test: the default path (the record's first-year errors per start, times the Phase 4 starts)
    rg = calc.rungs(d, s, e, p4)
    ok("R3a the analyst test files the default path's 750", deliver.r250(rg["pooled"]) == 750, "%.1f" % rg["pooled"])
    for nm in ("pooled", "month", "service"):
        ok("L1 rung %s prints outside the bin with clearance" % nm, clearance(rg[nm]) >= 1.15,
           "%.1f (clearance %.2f)" % (rg[nm], clearance(rg[nm])))
    for nm in ("per_driver", "slow_analogue"):
        ok("L2 rung %s prints outside the bin with clearance" % nm, clearance(rg[nm]) >= 1.15,
           "%.1f (clearance %.2f)" % (rg[nm], clearance(rg[nm])))
    # R3b the decisive step alone: the default path's population and exposure, with each start read at the driver's
    # own count (the golden) lands; the month clock instead of the count does not
    ok("R3b the count clock alone moves the default path onto the call", inbin(call, call_c) and not inbin(rg["month"], call_c))
    # the month clock against the count clock on the record's slow drivers: they err at their count, not their month
    ro = d["roster"]
    link = dict(zip(ro["Staff No"].map(last), ro["Link"]))
    slow = s["person"].map(lambda p: link.get(p) in calc.SLOW)
    dep, mi = calc.depot_windows(s)
    key = s.set_index(["person", "n"]).index
    err_set = set(zip(e["person"], e["n"].astype(int)))
    is_err = np.array([(p, int(n)) in err_set for p, n in zip(s["person"], s["n"])])
    for lo_n, hi_n in ((0, 50), (50, 200)):
        band = (s["n"] >= lo_n) & (s["n"] < hi_n)
        rs, rf = is_err[band & slow].mean(), is_err[band & ~slow].mean()
        ok("SF8 slow and regular drivers err alike at the same count (%d to %d starts)" % (lo_n, hi_n - 1),
           abs(rs / rf - 1) < 0.2, "%.4f vs %.4f" % (rs, rf))
    m6 = (mi >= 3) & (mi < 9)
    rs, rf = is_err[m6 & slow].mean(), is_err[m6 & ~slow].mean()
    ok("SF8 at the same months since go-live the slow drivers err far more", rs / rf > 1.8, "%.4f vs %.4f" % (rs, rf))
    # R3c no plant: no forecast, target, memo or earlier estimate ships; no repeated block in the log
    texts = " ".join(open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()
                     for f in files if f.endswith((".txt", ".csv")) and os.path.getsize(os.path.join(target, f)) < 5e6)
    ok("R3c no forecast, target or earlier estimate ships", not re.search(r"forecast of \d|target of \d|estimate[ds]? \d", texts))
    blocks = d["som"]["obr_utc"].str.slice(0, 10).value_counts()
    ok("R3c the log has no copied block (no day repeats another's rows)",
       not d["som"].duplicated(["obr_utc", "unit", "cab", "driver_id"]).any())
    # ------------------------------------------------------------------ semantic forks and Layer 1, each asserted
    flat = lambda txt: re.sub(r"\s+", " ", txt)
    from pypdf import PdfReader
    pdf = lambda f: flat(" ".join(p.extract_text() for p in PdfReader(os.path.join(target, f)).pages))
    conv, roll, guide, accept = pdf(C.F_CONV), pdf(C.F_ROLL), pdf(C.F_GUIDE), pdf(C.F_ACCEPT)
    for nm in ("COUNT_PIN", "WORK_PIN", "ROSTER_PIN", "CALL_PIN"):
        ok("D1 %s in the conventions" % nm, flat(getattr(D, nm)) in conv)
    ok("D1 ACCEPT_PIN in the acceptance note", flat(D.ACCEPT_PIN) in accept)
    ok("SF1 the window runs from each depot's go-live in the rollout plan",
       "from its go-live date in the rollout plan" in conv and all(C.DEPOT[c][1] in roll for c in C.P4_CODES))
    ok("SF2 the drivers are the 31 October 2026 rosters, no establishment change", "rosters at 31 October 2026" in conv
       and "no change to the six depots' establishments" in conv)

    def variant(**kw):
        dd = {k: v.copy() for k, v in d.items()}
        if kw.get("no_chain"):
            dd["xwalk"] = dd["xwalk"].iloc[0:0]
        reg = dd["reg"]
        if "cats" in kw:
            reg = reg[reg["Category"].isin(kw["cats"])].assign(Category="TDE")
        if kw.get("linked"):
            reg = reg.assign(**{"Linked To": np.nan})
        if kw.get("withdrawn"):
            reg = reg.assign(Status="Closed")
        dd["reg"] = reg
        if kw.get("cancelled"):
            dd["duty"] = dd["duty"].assign(status="Worked")
        if kw.get("issues"):
            du = dd["duty"].reset_index(drop=True)
            dd["duty"] = du.assign(duty_no=du["duty_no"] + "-" + du.index.astype(str))
        ss = calc.starts(dd)
        if kw.get("tst"):
            som = dd["som"].assign(person=dd["som"]["driver_id"].map(calc.chain(dd["xwalk"])),
                                   t=pd.to_datetime(dd["som"]["obr_utc"].str.slice(0, 19)))
            som = som.sort_values(["person", "t", "som_ref"], kind="mergesort")
            ss = som.assign(n=som.groupby("person").cumcount())
        ee = calc.tde_errors(dd, ss)
        if kw.get("utc_register"):
            ee = calc.tde_errors(dict(dd, reg=dd["reg"].assign(Received=pd.to_datetime(dd["reg"]["Received"]) + pd.Timedelta(hours=1))), ss)
        pp = calc.forward(dd, ss)
        if kw.get("prior_zero"):
            pp = pp.assign(prior=0)
        TT, EE = calc.tallies(ss, ee)
        pf, _ = calc.band_rates(TT, EE)
        out = float(calc.run_along(pf, pp).sum())
        if kw.get("rungs"):
            return out, calc.rungs(dd, ss, ee, pp)
        return out
    v = variant(cats=["TDE", "LTR", "BRK"])
    ok("SF3 every driver category read as data entry prints another count; COUNT_PIN names TDE",
       not inbin(v, call_c) and "category TDE" in conv, "%.1f" % v)
    v = variant(prior_zero=True)
    ok("SF4 drivers transferred in counted from their first Phase 4 start: same call", inbin(v, call_c), "%.1f" % v)
    v, rgl = variant(linked=True, rungs=True)
    ok("SF5 a linked report counted again prints another count; COUNT_PIN folds it",
       not inbin(v, call_c) and "links to an earlier report is the same error" in conv, "%.1f" % v)
    ok("SF5 linked reports counted again leave the default path off the call",
       not inbin(rgl["pooled"], call_c) and not inbin(rgl["month"], call_c), "%.1f, %.1f" % (rgl["pooled"], rgl["month"]))
    vc, rgc = variant(cats=["TDE", "LTR", "BRK"], rungs=True)
    ok("SF3 every driver category leaves the default path off the call",
       not inbin(rgc["pooled"], call_c) and not inbin(rgc["month"], call_c), "%.1f, %.1f" % (rgc["pooled"], rgc["month"]))
    # SF6 the expected count against a simulated count's median
    sims = np.random.default_rng(170).poisson(call, 20001)
    ok("SF6 the median of the count prints the same call", inbin(float(np.median(sims)), call_c), "%.0f" % np.median(sims))
    ok("SF7 the starts are twelve months at the ten months' average, filed", "average monthly number of cab activations" in conv)
    for nm, kw in (("SF11 L1-1 staff numbers not chained", dict(no_chain=True)), ("SF10 L1-2 withdrawn reports kept", dict(withdrawn=True)),
                   ("SF9 L1-3 test starts counted as starts", dict(tst=True)), ("SF13 L1-4 cancelled duties kept", dict(cancelled=True)),
                   ("SF14 L1-5 both issues of a re-issued duty kept", dict(issues=True)),
                   ("SF12 L1-6 the register's local time read as UTC", dict(utc_register=True))):
        v = variant(**kw)
        ok("R2 %s: same call" % nm, inbin(v, call_c), "%.1f" % v)
    # ------------------------------------------------------------------ separation
    reg = d["reg"]
    ok("S1 no recorder download report carries category TDE", not ((reg["Category"] == "TDE") & (reg["Reporter"] == "OBR download")).any())
    bare = {k: v for k, v in d.items() if k not in ("alloc", "works", "form", "renum")}
    bare["reg"] = d["reg"][d["reg"]["Category"] == "TDE"]
    s_b = calc.starts(bare)
    e_b = calc.tde_errors(bare, s_b)
    pf_b, _ = calc.band_rates(*calc.tallies(s_b, e_b))
    call_b = float(calc.run_along(pf_b, calc.forward(bare, s_b)).sum())
    ok("S2 the call is identical with the asks' files and the asks' register rows removed", abs(call_b - call) < 1e-9,
       "%.4f vs %.4f" % (call_b, call))
    # ------------------------------------------------------------------ ask A: the fitment programme's units
    gold_a = r["fleet"]
    truth_a = {}
    for c in C.P4_CODES:
        gl = w.golive[c]
        units = [u["now"] for u in w.units461 if u["depot"] == c]
        acc = sum(1 for u in units if all(w.veh461[v]["accepted"] <= gl for v in w.form461[u]))
        truth_a[c] = (acc, len(units) - acc)
    ok("A0 the golden handling reproduces the fleet's truth", gold_a == truth_a)
    for c in C.P4_CODES:
        k = c.lower()
        ok("A1 %s figures as filed" % c, (figs["ask_units_accepted_by_golive_%s" % k], figs["ask_units_not_accepted_by_golive_%s" % k]) == gold_a[c])
    for how in ("programme", "raw_unit", "any", "accepted_only"):
        st_ = calc.fleet(d, how)
        moved = [c for c in C.P4_CODES if st_[c] != gold_a[c]]
        ok("A2 stop %s misses every depot" % how, len(moved) == len(C.P4_CODES), ", ".join(sorted(set(C.P4_CODES) - set(moved))))
    prog = calc.fleet(d, "programme")
    ok("A3 the programme labels keep two driving vehicles a unit (no cardinality tell)",
       d["works"].groupby("Unit").size().eq(2).all())
    ok("A4 every depot has a reformed pair", all(sum(1 for x in w.reformed if x[0] == c) >= 2 for c in C.P4_CODES))
    # ------------------------------------------------------------------ ask C: level transitions and brake interventions
    gold_c = r["events"]
    win = (dt.datetime(2026, 1, 1), dt.datetime(2026, 11, 1))
    truth_c = {c: [0, 0] for c in C.REC_CODES}
    cutoff = dt.datetime.combine(C.RECORD_END, dt.time(23, 59, 59))
    seen = {}
    for rep in w.event_reports:
        if rep["event"][1] >= 0 and rep["when"] <= cutoff:
            seen[rep["event"]] = True
    for k, (cat, t, i) in enumerate(w.events):
        if not seen.get((cat, k)):
            continue
        loc = C.utc_to_local(t)
        if win[0] <= loc < win[1]:
            pid = w.starts[i][1]
            dep_ = w.depot_on(w.people[pid], loc.date())
            truth_c[dep_][0 if cat == "LTR" else 1] += 1
    truth_c = {k: tuple(v) for k, v in truth_c.items()}
    near = [c for c in C.REC_CODES if gold_c[c] != truth_c[c]]
    diff = sum(abs(a - b) for c in C.REC_CODES for a, b in zip(gold_c[c], truth_c[c]))
    ok("C0 the golden handling reproduces the events' truth", diff == 0, "off in %s by %d" % (", ".join(near), diff))
    for c in C.REC_CODES:
        k = c.lower()
        ok("C1 %s figures as filed" % c, (figs["ask_level_transition_errors_2026_%s" % k], figs["ask_brake_interventions_2026_%s" % k]) == gold_c[c])
    for how in ("all_rows", "fold_as_local", "obr_only", "manual_only", "fold_day"):
        st_ = calc.events(d, how)
        cells = [(c, j) for c in C.REC_CODES for j in (0, 1) if st_[c][j] == gold_c[c][j]]
        ok("C2 stop %s misses every cell" % how, not cells, ", ".join("%s %s" % x for x in cells))
    obr = reg[reg["Reporter"] == "OBR download"]
    ok("C3 the recorder downloads are never linked", obr["Linked To"].isna().all())
    # ------------------------------------------------------------------ documents
    dic = open(os.path.join(target, C.F_DICT), encoding="utf-8").read()
    banned = re.compile(r"practi[cs]e|experience|learning|learn|curve|cumulative|familiar|repetition|proficien|pace|"
                        r"count of starts|number of starts|starts (?:made|so far)|novice|new to", re.I)
    for nm, txt in (("conventions", conv), ("rollout plan", roll), ("guidance", guide), ("acceptance note", accept),
                    ("dictionary", dic)):
        hits = sorted(set(m.group(0).lower() for m in banned.finditer(txt)))
        ok("D2 %s carries none of the decisive step's words" % nm, not hits, ", ".join(hits))
    ok("D3 the guidance links signaller and fleet reports only, silent on recorder downloads' time",
       "recorder downloads" in guide and "UTC" not in guide and "UTC" not in conv)
    ok("D4 no em or en dash in documents or the write-up", not re.search("[–—]", conv + roll + guide + accept + dic +
                                                                          open(os.path.join(task, "submission.md")).read()))
    # ------------------------------------------------------------------ realism
    du = d["duty"]
    per = du[du["status"] == "Worked"].groupby("staff_no").size()
    ok("Q1 duties a driver plausible (150 to 220 worked in ten months for most)", per.between(120, 240).mean() > 0.8,
       "median %d" % per.median())
    mix = reg[reg["Category"] == "TDE"]["Reporter"].value_counts(normalize=True)
    ok("Q2 the TDE reporters mixed (driver, signaller, fleet data check)", mix.max() < 0.75 and len(mix) == 3, mix.round(2).to_dict())
    hrs = pd.to_datetime(d["som"]["obr_utc"].str.slice(0, 19)).dt.hour.value_counts(normalize=True)
    ok("Q3 recorder starts spread over the operating day", hrs.max() < 0.12)
    # the realism sweep: no identical counts across periods or sites, no round headline figures, no repeating block,
    # personas from guard.py names only, containers scrubbed, timestamps coherent
    drv_rows = d["som"][d["som"]["som_type"] != "TST"]
    som_m = drv_rows.assign(m=drv_rows["obr_utc"].str.slice(0, 7), dep=drv_rows["driver_id"].str.slice(0, 2))
    cnt = som_m.groupby(["dep", "m"]).size()
    # among some 200 depot-months of 3,000 to 5,000 starts, chance pairs, the odd triple (about a quarter expected) and
    # one equal pair of consecutive months in a depot (about 0.7 expected) are what independent months give; a
    # generated count would repeat in runs
    consec = sum(int((g.values[1:] == g.values[:-1]).sum()) for _, g in cnt.groupby(level=0))
    ok("Q4 monthly start counts repeat no more than chance gives (no run of equal months)",
       cnt.value_counts().max() <= 3 and consec <= 1, "%d pairs among %d, largest multiplicity %d, %d consecutive" % (
           cnt.duplicated().sum(), len(cnt), cnt.value_counts().max(), consec))
    regm = reg.assign(m=pd.to_datetime(reg["Received"]).dt.strftime("%Y-%m")).groupby(["Depot", "m"]).size()
    flat = [dp for dp, g in regm.groupby(level=0) if len(g) > 3 and g.std() == 0]
    ok("Q5 no depot's monthly register count is flat", not flat, ", ".join(flat))
    ok("Q6 no round headline figure", call % 50 > 1 and st % 1000 > 1, "%.1f, %.1f" % (call, st))
    people = {"Kate Potter", "Charlie Coles", "Gillian Armstrong", "Arthur Jackson"}
    named = set(re.findall(r"(?:Kate Potter|Charlie Coles|Gillian Armstrong|Arthur Jackson|[A-Z][a-z]+ [A-Z][a-z]+, (?:Human|ETCS|Safety))",
                           conv + roll + guide + accept))
    ok("Q7 every persona in the documents is drawn", named <= people | {x for x in named if "," in x}, ", ".join(sorted(named)))
    import zipfile
    meta_ok = True
    for f in files:
        if f.endswith(".xlsx"):
            core = zipfile.ZipFile(os.path.join(target, f)).read("docProps/core.xml").decode()
            meta_ok &= "openpyxl" not in core.lower() and "2026-11" in core
    ok("Q8 workbook containers carry the operator's authors and November 2026 stamps", meta_ok)
    late = pd.to_datetime(reg["Received"]).max()
    ok("Q9 no record after the record's end", late <= pd.Timestamp("2026-10-31 23:59")
       and pd.to_datetime(d["som"]["obr_utc"].str.slice(0, 19)).max() <= pd.Timestamp("2026-11-01 00:00"), str(late))
    print("checks: %d run, %d failed%s" % (N[0], len(FAILS), (": " + ", ".join(FAILS)) if FAILS else ""))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
