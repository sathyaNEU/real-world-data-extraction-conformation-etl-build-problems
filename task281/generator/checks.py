"""The generator's assertions for task281, run on the built pack, its goldens and the world's clean truth.

Every row of the design note's semantic fork table (SF1 to SF17) is asserted here, with the analyst test (R3a: the
easy route on the correctly read record files all ten phases; R3b: the at-risk maker's drivers alone file the
golden), the ladder's rungs and their clearances, the separation line, both asks against the world's own events, and
the input gates."""
import csv
import datetime as dt
import os
import re

import numpy as np
from scipy.stats import chi2

import analysis as A
import params as P
from world import EPOCH, d2i

AT_RISK, CURED = P.DRV["A"], P.DRV["B"]
RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((bool(cond), name, detail))
    return bool(cond)


def local(x):
    return dt.datetime(EPOCH.year, EPOCH.month, EPOCH.day) + dt.timedelta(minutes=int(round(x * 1440)))


def sh(d):
    return {pc: (v["share"] if isinstance(v, dict) else v) for pc, v in d.items()}


def setof(s):
    return [pc for pc in P.PHASE_CODES if s[pc] > P.TRIGGER]


def r5(s):
    return {pc: int(round(s[pc] * 100 / 5) * 5) for pc in P.PHASE_CODES}


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def maker_fits(rows):
    return {mk: A.weibull_mle([r["t"] for r in rows if r["maker"] == mk], [r["d"] for r in rows if r["maker"] == mk])
            for mk in (AT_RISK, CURED)}


def golden_shares(rows, age="age", cured=None):
    f = maker_fits(rows)
    return sh(A.phase_shares(rows, lambda r: (cured(r) if (cured and r["maker"] == CURED)
                                              else A.cond_fail(r[age], *f[r["maker"]]))))


def loglik(t, d, k, lam):
    t = np.maximum(np.asarray(t, float), 1e-9)
    d = np.asarray(d, bool)
    z = (t / lam) ** k
    return float((np.log(k / lam) + (k - 1) * np.log(t / lam))[d].sum() - z.sum())


# ---------------------------------------------------------------------------------------------- the truth
def truth_lifetimes(w):
    """Each conversion luminaire's original-driver record from the world's own events: failure and exit dated at
    their work orders' completion, an order still open at the close not a failure."""
    end = P.RECORD_END
    fd, ex = {}, {}
    for o in w.outages:
        if o.get("lum") is None or o.get("circuit"):
            continue
        c = local(o["completed"]).date()
        if c > end:
            continue
        i = o["lum"]
        if o["kind"] == "driver" and not o.get("second"):
            fd[i] = c
        if o["kind"] in A.EXIT_KINDS:
            ex[i] = min(ex.get(i, c), c)
    rows = []
    for i, L in enumerate(w.lum):
        t0, f, e = L["install"], fd.get(i), ex.get(i)
        failed = f is not None and (e is None or f <= e)
        stop = f if failed else min(e or end, end)
        rows.append(dict(pole=L["pole"], phase=L["phase"], maker=P.DRV[L["src"]], watts=L["watts"],
                         t=(stop - t0).days / P.YEAR_D, d=failed, alive=(not failed) and e is None,
                         age=(P.AS_OF - t0).days / P.YEAR_D, age_close=(end - t0).days / P.YEAR_D))
    return rows


def truth_energy(w, rc):
    """Each town's 2026 saving from the world's events: the removed fixture, the luminaire's output through the
    year (a glare reprogramming brings 110 W to 70 W on its completion day), the pole's removal, the node's record."""
    nlc = {}
    for row in rc.nlc_rows()[1]:
        nlc[(int(row[1][3:]), int(row[2][5:7]))] = (float(row[3]), float(row[4]))
    ev = {}
    for o in w.outages:
        if o.get("lum") is not None and not o.get("circuit") and o["completed"] <= d2i(P.RECORD_END) + 1:
            ev.setdefault(o["lum"], []).append(o)
    burn = P.BURN_H
    out = {}
    for i, L in enumerate(w.lum):
        hps = P.INPUT_W[("HPS", L["hps_w"])]
        steps, removed = [(L["install"], L["watts"])], None
        for o in sorted(ev.get(i, []), key=lambda o: o["completed"]):
            d = local(o["completed"]).date()
            if o["kind"] == "reprogram":
                steps.append((d, 70))
            elif o["kind"] in ("knockdown", "luminaire"):
                steps.append((d, 70 if L["reprog"] is not None else L["watts"]))
            elif o["kind"] == "pole_removed":
                removed = d
        if removed is not None and removed < dt.date(2026, 1, 1):
            continue
        tot = 0.0
        for m in range(1, 13):
            nd = A._days(2026, m)
            days = [dt.date(2026, m, x) for x in range(1, nd + 1) if removed is None or dt.date(2026, m, x) < removed]
            if not days:
                continue
            lw = np.array([P.INPUT_W[("LED", [s for s in steps if s[0] <= x][-1][1])] for x in days], float)
            h = burn[m - 1] / nd
            e_led = (lw * h).sum()
            rec = nlc.get((L["pole"], m))
            if rec:
                e_led -= lw.mean() * (1 - rec[1] / 100.0) * rec[0]
            tot += hps * h * len(days) - e_led
        out[L["town"]] = out.get(L["town"], 0.0) + tot
    return {P.TOWN_NAME[t]: v / 1e6 for t, v in out.items()}


def truth_repairs(w):
    late, tot = {}, {}
    gaps = []
    for o in w.outages:
        if o["kind"] in w.PLANNED or o["completed"] > d2i(P.RECORD_END) + 1:
            continue
        c = local(o["completed"])
        if c.year != 2026:
            continue
        rs = [r for r in o.get("reports", []) if not r.get("after")]
        first = min(r["t"] for r in rs) if rs else o["found"]
        mins = int(round(o["completed"] * 1440)) - int(round(first * 1440))
        t = P.TOWN_NAME[o["town"]]
        tot[t] = tot.get(t, 0) + 1
        late[t] = late.get(t, 0) + int(mins > 4320)
        gaps.append(abs(mins - 4320))
    return late, tot, min(gaps)


def rc_addr_rows(target):
    """The legacy orders whose location is written as an address with the pole's tag after it."""
    with open(os.path.join(target, P.FILES["wo_legacy"]), newline="", encoding="utf-8") as fh:
        return {r["WO_NO"] for r in csv.DictReader(fh) if not r["LOCATION"].startswith("TPL")}


# ---------------------------------------------------------------------------------------------- rules and realism
def pdf_text(path):
    import subprocess
    return " ".join(subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True,
                                   check=True).stdout.split())


def rules_and_realism(target, D, G, fig, b):
    import shutil
    import subprocess
    GSET = G["set"]
    rows = G["rows"]

    def same_call(D2):
        G2 = A.golden_call(D2, rows=A.lifetimes(D2))
        return G2["set"] == GSET

    # R1: the field's raw material ships, and no shipped column holds the decisive quantity
    heads = []
    for f in os.listdir(target):
        if f.endswith(".csv"):
            heads += next(csv.reader(open(os.path.join(target, f), encoding="utf-8")))
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, P.FILES["install"]), read_only=True)
    for ws in wb.worksheets:
        heads += [str(h) for h in next(ws.iter_rows(values_only=True))]
    bad = [h for h in heads if re.search(r"maker|vendor|manufactur|driver|supplier|share|cure", h, re.I)]
    n_lum = sum(p[3] for p in P.PHASES)
    check("R1 the golden reads every conversion luminaire's censored original-driver duration; no shipped column names "
          "a driver maker or holds a share", len(rows) == n_lum and not bad, "%d luminaires; columns hit: %s" % (
              len(rows), bad))
    # R2: each mess item mishandled leaves the call where it was
    tagless = {p: I for p, I in D["inst"].items() if not (I["date"].year <= 2022 and p % 25 == 0)}
    check("R2 the paper-form pole tags (TPL prefix or bare) partly unmatched: same call",
          same_call(dict(D, inst=tagless)))
    addr_lost = [x for x in D["wos"] if not (x["sys"] == "legacy" and x["pole"] is not None and x["pole"] % 20 == 0)]
    check("R2 legacy locations written as an address before the tag partly lost: same call",
          same_call(dict(D, wos=addr_lost)))
    dbl = D["wos"] + [dict(x, sys="legacy", completed=y["completed"]) for x in D["wos"] if x["sys"] == "legacy"
                      and x["completed"] is None for y in D["wos"] if y["source"] == "MIGRATED" and y["pole"] == x["pole"]
                      and y["opened"] == x["opened"]]
    check("R2 orders open at the cutover counted in both systems: same call", same_call(dict(D, wos=dbl)))
    last = {}
    for x in D["wos"]:
        if x["kind"] == "driver" and x["completed"] is not None:
            last[x["pole"]] = max(last.get(x["pole"], x["completed"]), x["completed"])
    wl = [x for x in D["wos"] if not (x["kind"] == "driver" and x["completed"] is not None
                                      and x["completed"] != last[x["pole"]])]
    check("R2 a service driver's failure taken for the original's (the last driver order kept): same call",
          same_call(dict(D, wos=wl)))
    swap = {p: dict(I, date=dt.date(I["date"].year, I["date"].day, I["date"].month))
            if (I["date"].year >= 2023 and I["date"].day <= 12) else I for p, I in D["inst"].items()}
    check("R2 the tablet export's text dates read day first where they can be: same call",
          same_call(dict(D, inst=swap)))
    # R3c: no plant: no copied block, no constant stream, no shared bound set
    nl = {}
    for (p, m), (dh, lv) in D["nlc"].items():
        nl.setdefault(p, {})[m] = dh
    vecs = [tuple(v.get(m) for m in range(1, 13)) for v in nl.values()]
    check("R3c no two nodes carry the same twelve months of dimmed hours", len(set(vecs)) == len(vecs),
          "%d nodes, %d distinct" % (len(vecs), len(set(vecs))))
    mode_share = max(np.unique([v for (p, m), (v, l) in D["nlc"].items() if m == 3], return_counts=True)[1]) / \
        sum(1 for (p, m) in D["nlc"] if m == 3)
    check("R3c no month's dimmed hours a constant across nodes", mode_share < 0.05, "modal share %.3f" % mode_share)
    # realism sweep: identifiers with no constant step, documents dated after what they state
    import pandas as pd
    ids = {}
    wn = pd.read_csv(os.path.join(target, P.FILES["wo_new"]), dtype=str)
    ids["successor order numbers (2026)"] = sorted(int(x[6:]) for x in wn["work_order"] if x.startswith("WO-26"))
    lg = pd.read_csv(os.path.join(target, P.FILES["wo_legacy"]), dtype=str)
    ids["legacy order numbers"] = sorted(int(x[1:]) for x in lg["WO_NO"])
    rp = pd.read_csv(os.path.join(target, P.FILES["reports"]), dtype=str)
    ids["report ids"] = sorted(int(x[3:]) for x in rp["report_id"])
    vg = pd.read_csv(os.path.join(target, P.FILES["vegetation"]), dtype=str)
    ids["patrol ids"] = sorted(int(x[3:]) for x in vg["patrol_id"])
    nn = pd.read_csv(os.path.join(target, P.FILES["nlc"]), dtype=str)
    ids["node ids"] = sorted({int(x, 16) for x in nn["node_id"]})
    coc = pdf_text(os.path.join(target, P.FILES["coc"]))
    ids["purchase orders"] = sorted({int(x) for x in re.findall(r"Purchase order (\d{10})", coc)})
    steps = {k: len(set(np.diff(v))) for k, v in ids.items()}
    check("realism: no identifier column runs at one constant step", all(s > 1 for s in steps.values()), str(steps))
    note = pdf_text(os.path.join(target, P.FILES["note"]))
    tariff = pdf_text(os.path.join(target, P.FILES["tariff"]))
    check("positive controls: the note, the tariff and the certificates read through the same extractor",
          "two-parameter Weibull distribution, fitted by maximum likelihood" in note and
          "within 72 hours of the first report" in tariff and "LED driver, programmable" in coc
          and len(note) > 1000 and len(tariff) > 1000 and len(coc) > 10000)
    words = r"cure|never wear|wear out|susceptib|immune|Vantrel|Corvane|driver maker|population at risk"
    check("no governing document names a driver maker, a cure or a population at risk",
          not re.search(words, note, re.I) and not re.search(words, tariff, re.I))
    check("the certificates say nothing of wear-out or cure (both makers' drivers under one rated life)",
          not re.search(r"cure|wear|susceptib", coc, re.I) and
          coc.count("rated life 100,000 hours") == len(D["coc"]))
    last_ship = max(L["ship"] for L in b["w"].lots)
    check("documents dated after what they state: certificates after the last shipment, the note after the "
          "record's close", last_ship <= dt.date(2025, 10, 2) and "6 January 2027" in note,
          "last shipment %s" % last_ship)
    # distractors: the golden and every ask unchanged with all three deleted
    scratch = os.path.join(os.path.dirname(target), ".distractor_check")
    if os.path.exists(scratch):
        shutil.rmtree(scratch)
    shutil.copytree(target, scratch)
    for k in P.DISTRACTORS:
        os.remove(os.path.join(scratch, P.FILES[k]))
    D3 = A.load(scratch)
    G3 = A.golden_call(D3)
    E3 = A.energy_saving(D3)[0]
    L3 = A.repairs(D3)[0]
    shutil.rmtree(scratch)
    check("distractors deleted: the call, every share and every ask unchanged",
          G3["set"] == GSET and all(abs(G3["phases"][pc]["share"] - G["phases"][pc]["share"]) < 1e-12
                                    for pc in P.PHASE_CODES)
          and all(int(round(E3[t])) == fig["towns"][t]["energy"] and L3[t] == fig["towns"][t]["late"]
                  for t in fig["towns"]))


# ---------------------------------------------------------------------------------------------- the run
def run(target, golden, b, fig, res):
    RESULTS.clear()
    w, rc = b["w"], b["rc"]
    D, G = res["D"], res["G"]
    rows = G["rows"]
    gold = sh(G["phases"])
    GSET = G["set"]
    T = P.TRIGGER

    # ---- input gates
    files = sorted(os.listdir(target))
    exts = {os.path.splitext(f)[1] for f in files}
    big = max(b["counts"].values())
    check("input gates: 10+ files, 3+ formats, a 25,000-row file",
          len(files) >= 10 and len(exts) >= 3 and big >= 25000, "%d files, %s, largest %d rows" % (len(files),
                                                                                             sorted(exts), big))
    check("input gates: two or more distractors, none named as such", len(P.DISTRACTORS) >= 2 and not any(
        "distract" in f for f in files), str([P.FILES[k] for k in P.DISTRACTORS]))
    check("no file describes the data (no dictionary, readme, manifest, notes)",
          not any(re.search(r"dictionar|readme|manifest|field_notes|extract_log", f, re.I) for f in files))

    # ---- the clean truth
    tr = truth_lifetimes(w)
    by_pole = {r["pole"]: r for r in tr}
    mism = sum(1 for r in rows if (by_pole[r["pole"]]["d"], round(by_pole[r["pole"]]["t"], 9), by_pole[r["pole"]]["alive"])
               != (r["d"], round(r["t"], 9), r["alive"]))
    check("the pack's lifetimes equal the world's, luminaire by luminaire", mism == 0, "%d mismatches" % mism)
    mk_ok = all(D["coc"][D["inst"][L["pole"]]["lot"]]["maker"] == P.DRV[L["src"]] for L in w.lum)
    check("every luminaire's lot finds its certificate and its driver maker", mk_ok)
    true_set = setof({pc: np.mean([(A.cond_fail(r["age"], P.K_A, P.LAM_A) if r["maker"] == AT_RISK else
                                    1 - np.exp(-P.RATE_B * (P.HORIZON_Y - r["age"])))
                                   for r in tr if r["phase"] == pc and r["alive"]]) for pc in P.PHASE_CODES})
    check("the golden set is the world's true set", GSET == true_set, "golden %s, truth %s" % (GSET, true_set))
    check("golden set is P1, P3, P5, P7, P9", GSET == ["P1", "P3", "P5", "P7", "P9"], str(GSET))

    # ---- R3a, R3b: the analyst test on the clean truth
    pooled, (kP, lP) = A.rung_pooled(rows)
    default_set = setof(sh(pooled))
    check("R3a: one Weibull over every conversion driver files all ten phases", default_set == P.PHASE_CODES,
          "default %s, shares %.1f to %.1f" % (default_set, min(sh(pooled).values()) * 100, max(sh(pooled).values()) * 100))
    fA = A.weibull_mle([r["t"] for r in rows if r["maker"] == AT_RISK], [r["d"] for r in rows if r["maker"] == AT_RISK])
    r3b = setof(sh(A.phase_shares(rows, lambda r: A.cond_fail(r["age"], *fA) if r["maker"] == AT_RISK else 0.0)))
    check("R3b: the at-risk maker's drivers alone file the golden", r3b == GSET, str(r3b))
    expB = sum((r["t"] / lP) ** kP for r in rows if r["maker"] == CURED)
    nB = sum(r["d"] for r in rows if r["maker"] == CURED)
    check("loudness after the join: the pooled fit expects hundreds of the cured maker's failures, the record has few",
          expB > 20 * max(nB, 1), "expected %.0f, recorded %d" % (expB, nB))

    # ---- clearances: golden and default at 1.15x, every designated phase above and every other below
    lo, hi = T / 1.15, T * 1.15
    check("golden clears the trigger by 1.15x both ways", all(v >= hi or v <= lo for v in gold.values()),
          "nearest %.3f" % min(gold.values(), key=lambda v: abs(v - T)))
    check("default clears the trigger by 1.15x", all(v >= hi for v in sh(pooled).values()),
          "lowest %.3f" % min(sh(pooled).values()))

    # ---- the ladder's rungs (sets), each a different named answer
    lad = {}
    lad["R1 failure share to date"] = setof(sh(A.rung_naive(rows)))
    lad["R2 one Weibull, the default"] = default_set
    lfp, par = A.rung_lfp(rows)
    lad["R2b limited-failure population, pooled"] = setof(sh(lfp))
    lad["R3 phase scale (violates 3.2)"] = setof(sh(A.rung_groups(rows, lambda r: r["phase"], True)))
    lad["R3b Weibull per phase (violates 3.2)"] = setof(sh(A.rung_groups(rows, lambda r: r["phase"], False)))
    lad["R4 maker split, unconditioned"] = setof(sh(A.rung_maker_uncond(D, G)))
    lad["R5 the golden"] = GSET
    check("R2b the cure model on the pooled record files all ten phases (one susceptible fraction for every phase)",
          lad["R2b limited-failure population, pooled"] == P.PHASE_CODES,
          "p = %.3f, shares %.1f to %.1f" % (par[2], min(sh(lfp).values()) * 100, max(sh(lfp).values()) * 100))
    lp = sh(A.rung_lfp_phase(rows))
    lad["R3c cure fraction per phase (violates 3.2)"] = setof(lp)
    check("R3c a susceptible fraction per phase (3.2) files another set", setof(lp) != GSET,
          "%s, shares %s" % (setof(lp), " ".join("%.0f" % (lp[pc] * 100) for pc in P.PHASE_CODES)))
    check("R1 files no phase (the record is young)", lad["R1 failure share to date"] == [])
    check("R3 and R3b file sets other than the golden", lad["R3 phase scale (violates 3.2)"] != GSET and
          lad["R3b Weibull per phase (violates 3.2)"] != GSET,
          "%s / %s" % (lad["R3 phase scale (violates 3.2)"], lad["R3b Weibull per phase (violates 3.2)"]))
    unc = sh(A.rung_maker_uncond(D, G))
    check("R4 lands the set with other figures", lad["R4 maker split, unconditioned"] == GSET and
          sum(r5(unc)[pc] != r5(gold)[pc] for pc in P.PHASE_CODES) >= 1,
          "%d of 10 nearest-5 figures differ" % sum(r5(unc)[pc] != r5(gold)[pc] for pc in P.PHASE_CODES))

    # ---- the shape and the figures
    e5 = min(edge(v * 100, 5) for v in gold.values())
    check("every share sits clear of its nearest-5 edge", e5 >= 0.3, "tightest %.2f points" % e5)
    check("figures.json carries the nearest-5 shares", all(fig["phases"][pc]["share5"] == r5(gold)[pc]
                                                           for pc in P.PHASE_CODES))

    # ---- the semantic fork table, every row asserted
    reg_phase = all(D["reg"][p]["conversion_phase"] == I["phase"] for p, I in D["inst"].items() if p in D["reg"])
    check("SF1 the installer's phase and the register's conversion_phase agree on every standing pole", reg_phase)
    yr_gap = np.mean([I["date"].year - int(D["reg"][p]["pole_set_year"]) for p, I in D["inst"].items() if p in D["reg"]])
    check("SF2 the register's pole_set_year is the pole's (decades before the retrofit), ruled out by 2.4",
          yr_gap > 10, "mean gap %.1f years" % yr_gap)
    alt = A.lifetimes(D, failure_kinds=("driver", "glare"))
    check("SF3 glare orders counted as driver events: same call", setof(golden_shares(alt)) == GSET)
    alt = A.lifetimes(D, date_field="opened")
    check("SF4 failures dated at the order's opening: same call", setof(golden_shares(alt)) == GSET)
    wos_open = [dict(x, completed=x["opened"]) if (x["completed"] is None and x["kind"] == "driver") else x
                for x in D["wos"]]
    alt = A.lifetimes(dict(D, wos=wos_open))
    check("SF5 an order open at the close counted as a failure: same call", setof(golden_shares(alt)) == GSET)
    alt = A.lifetimes(D, exits=())
    check("SF6 exits ignored (every luminaire kept to the close): same call", setof(golden_shares(alt)) == GSET)
    after_exit = 0
    for r in rows:
        pass
    ex_d = {}
    for x in D["wos"]:
        if x["kind"] in A.EXIT_KINDS and x["completed"] is not None and x["pole"] in D["inst"]:
            ex_d[x["pole"]] = min(ex_d.get(x["pole"], x["completed"]), x["completed"])
    after_exit = sum(1 for x in D["wos"] if x["kind"] == "driver" and x["completed"] is not None
                     and x["pole"] in ex_d and x["completed"] > ex_d[x["pole"]])
    check("SF7 no driver order follows an exit on its pole (a replacement luminaire's events never reach the fit)",
          after_exit == 0, "%d" % after_exit)
    leg_open = [x for x in D["wos"] if x["sys"] == "legacy" and x["completed"] is None]
    mig = [x for x in D["wos"] if x["source"] == "MIGRATED"]
    check("SF8 every legacy order open at the cutover is carried once into the successor",
          len(leg_open) == len(mig) and {(x["pole"], x["opened"]) for x in leg_open} ==
          {(x["pole"], x["opened"]) for x in mig}, "%d legacy open, %d migrated" % (len(leg_open), len(mig)))
    alt12 = sh(A.phase_shares(rows, lambda r: A.cond_fail(r["age"], *maker_fits(rows)[r["maker"]],
                                                          h=r["age"] + P.HORIZON_Y)))
    check("SF9 twelve years counted from 1 January 2027 instead of from installation: same call, other figures, "
          "ruled out by 2.1", setof(alt12) == GSET and r5(alt12) != r5(gold), str(r5(alt12)))
    cl = golden_shares(rows, age="age_close")
    check("SF10 conditioned at the record's close instead of 1 January: same call and nearest-5 figures",
          setof(cl) == GSET and r5(cl) == r5(gold))
    n_alive = {pc: G["phases"][pc]["n"] for pc in P.PHASE_CODES}
    check("SF11 the population on 1 January 2027: no failure and no exit by the close",
          sum(n_alive.values()) == sum(1 for r in rows if r["alive"]), str(n_alive))
    check("SF12 lifetimes phase by phase (3.2) file another set", lad["R3 phase scale (violates 3.2)"] != GSET)
    bz = golden_shares(rows, cured=lambda r: 0.0)
    fB = maker_fits(rows)[CURED]
    rate = sum(r["d"] for r in rows if r["maker"] == CURED) / sum(r["t"] for r in rows if r["maker"] == CURED)
    be = golden_shares(rows, cured=lambda r: 1 - np.exp(-rate * (P.HORIZON_Y - r["age"])))
    check("SF13 the cured maker at zero or at a constant rate instead of its own Weibull: same call and figures",
          setof(bz) == GSET and setof(be) == GSET and r5(bz) == r5(gold) and r5(be) == r5(gold),
          "Corvane shape %.2f, life %.0f years" % fB)
    ow = sh(A.rung_groups(rows, lambda r: (r["maker"], r["watts"]), shared_shape=False))
    ow2 = sh(A.rung_groups(rows, lambda r: (r["maker"], r["watts"]), shared_shape=True))
    check("SF14 a Weibull per maker and output setting: same call and nearest-5 figures",
          setof(ow) == GSET and r5(ow) == r5(gold), "max shift %.2f points" % max(abs(ow[pc] - gold[pc]) * 100
                                                                                  for pc in P.PHASE_CODES))
    rounded_set = [pc for pc in P.PHASE_CODES if r5(gold)[pc] > 45]
    check("SF15 the trigger read on the rounded share: same call", rounded_set == GSET)
    open_drv = sum(1 for x in D["wos"] if x["kind"] == "driver" and x["completed"] is None
                   and x["pole"] in D["inst"] and D["inst"][x["pole"]]["phase"] in GSET)
    check("SF16 the program's luminaires: every designated phase's luminaire on its original driver on 1 January "
          "(an open order is not yet a failure, 2.2)", fig["call"]["program_luminaires"] ==
          sum(n_alive[pc] for pc in GSET), "%d luminaires, %d with an open driver order" % (
              fig["call"]["program_luminaires"], open_drv))
    addr = [x for x in D["wos"] if not (x["sys"] == "legacy" and x["wo"] in rc_addr_rows(target))]
    G_a = A.golden_call(dict(D, wos=addr), rows=A.lifetimes(dict(D, wos=addr)))
    check("SF16 the program count reads the legacy orders located by address and tag (left unread, the count rises)",
          sum(G_a["phases"][pc]["n"] for pc in GSET) > fig["call"]["program_luminaires"],
          "%d with them unread" % sum(G_a["phases"][pc]["n"] for pc in GSET))
    alt = [dict(r, t=r["t"] * P.YEAR_D / 365.0, age=r["age"] * P.YEAR_D / 365.0) for r in rows]
    check("SF17 365-day years: same call and figures", setof(golden_shares(alt)) == GSET)

    # ---- groupings the data cannot separate, and the one they refute
    tA = [r["t"] for r in rows if r["maker"] == AT_RISK]
    dA = [r["d"] for r in rows if r["maker"] == AT_RISK]
    llA = loglik(tA, dA, *fA)
    llW = sum(loglik([r["t"] for r in rows if r["maker"] == AT_RISK and r["watts"] == wt],
                     [r["d"] for r in rows if r["maker"] == AT_RISK and r["watts"] == wt],
                     *A.weibull_mle([r["t"] for r in rows if r["maker"] == AT_RISK and r["watts"] == wt],
                                    [r["d"] for r in rows if r["maker"] == AT_RISK and r["watts"] == wt]))
              for wt in (40, 70, 110))
    pW = 1 - chi2.cdf(2 * (llW - llA), 4)
    check("the output settings share one lifetime (likelihood ratio, 4 df)", pW > 0.01, "p = %.3f" % pW)
    shared = A.weibull_groups(rows, lambda r: r["maker"], shared_shape=True)
    ll_sep = llA + loglik([r["t"] for r in rows if r["maker"] == CURED], [r["d"] for r in rows if r["maker"] == CURED],
                          *maker_fits(rows)[CURED])
    ll_sh = sum(loglik([r["t"] for r in rows if r["maker"] == mk], [r["d"] for r in rows if r["maker"] == mk],
                       *shared[mk]) for mk in (AT_RISK, CURED))
    check("one shape for both makers is refuted (likelihood ratio, 1 df)", 2 * (ll_sep - ll_sh) > 10.83,
          "2 dlogL = %.1f" % (2 * (ll_sep - ll_sh)))
    ll_pool = loglik([r["t"] for r in rows], [r["d"] for r in rows], kP, lP)
    check("one Weibull over every driver is refuted once the maker is read (likelihood ratio, 2 df)",
          2 * (ll_sep - ll_pool) > 100, "2 dlogL = %.1f" % (2 * (ll_sep - ll_pool)))

    # ---- not rule application: the family the note leaves open, enumerated and standing
    enum = {"pooled": default_set, "LFP pooled": lad["R2b limited-failure population, pooled"],
            "phase scale": lad["R3 phase scale (violates 3.2)"], "per phase": lad["R3b Weibull per phase (violates 3.2)"],
            "maker": GSET, "maker x output": setof(ow), "maker x output, shared shape": setof(ow2),
            "maker, cured at zero": setof(bz)}
    standing = {k: v for k, v in enum.items() if k in ("pooled", "LFP pooled", "maker", "maker x output",
                                                        "maker x output, shared shape", "maker, cured at zero")}
    check("enumerated family: the sets spread", len({tuple(v) for v in enum.values()}) >= 3,
          "; ".join("%s %d" % (k, len(v)) for k, v in enum.items()))
    check("standing family, once the maker is read: one set",
          len({tuple(v) for k, v in standing.items() if k not in ("pooled", "LFP pooled")}) == 1)

    # ---- the separation line: no ask device or hazard row is read by the call
    no_ask = dict(D, reports=[], nlc={}, wos=[x for x in D["wos"] if x["kind"] not in ("glare", "ug_cable")])
    G2 = A.golden_call(no_ask, rows=A.lifetimes(no_ask))
    check("separation: deleting the reports, the node records, the glare and cable orders leaves the call and every "
          "share unchanged", G2["set"] == GSET and all(abs(G2["phases"][pc]["share"] - gold[pc]) < 1e-12
                                                       for pc in P.PHASE_CODES))

    # ---- ask E: the energy saving against the world's own events
    E_t = truth_energy(w, rc)
    E_g = {t: v["energy_mwh"] for t, v in fig["towns"].items()}
    check("E: the golden equals the world's own saving, town by town (figures.json at three decimals)", all(abs(E_t[t] - E_g[t]) < 6e-4 for t in E_g),
          str({t: round(E_t[t] - E_g[t], 6) for t in E_g}))
    var = [A.energy_saving(D, removal_day_in=True)[0], A.energy_saving(D, change_day_new=False)[0]]
    ee = min(edge(v, 1) for v in E_g.values())
    check("E: whole MWh clear of the edge and the day conventions", ee >= 0.12 and all(
        round(V[t]) == round(E_g[t]) for V in var for t in E_g), "tightest %.3f MWh" % ee)
    reg_w = A.energy_saving(dict(D, inst={p: dict(I, catalog=re.sub(r"-\d+W-", "-%sW-" % D["reg"][p]["lamp_watts"],
                                                                     I["catalog"]) if p in D["reg"] else I["catalog"])
                                          for p, I in D["inst"].items()},
                                 wos=[x for x in D["wos"] if x["kind"] != "glare"]))[0]
    cat_w = A.energy_saving(dict(D, wos=[x for x in D["wos"] if x["kind"] != "glare"]))[0]
    check("E primary: the register's wattage or the installer's catalog all year misses every town",
          all(round(reg_w[t]) != round(E_g[t]) and round(cat_w[t]) != round(E_g[t]) for t in E_g))

    # ---- ask R: repairs against the world's own reports
    L_t, T_t, gap = truth_repairs(w)
    L_g = {t: v["late"] for t, v in fig["towns"].items()}
    check("R: the golden equals the world's own count, town by town", L_t == L_g and
          T_t == {t: v["repaired"] for t, v in fig["towns"].items()}, "%s vs %s" % (L_t, L_g))
    check("R: no repair within two minutes of 72 hours, on the wall clock or in elapsed time", gap > 2,
          "nearest %d minutes" % gap)
    own = A.repairs(D, circuits=False, lookback_days=10)[0]
    check("R primary: reports matched to the order's own pole (ten days back) miss every town",
          all(own[t] != L_g[t] for t in L_g),
          str({t: own[t] - L_g[t] for t in L_g}))
    unres = sum(1 for rp in A.report_poles(D) if rp["pole_res"] is None and rp["pole"] is None and
                any(r["nearest_address"] == rp["address"] and r["town"] == rp["town"] for r in D["reg"].values()))
    check("R: every report about a Company light resolves to one pole", unres == 0, "%d unresolved" % unres)

    # ---- the three rules, executed (R1 raw material, R2 each mess item neutral, R3c no plant)
    rules_and_realism(target, D, G, fig, b)

    # ---- the deliverables
    check("goldens written", all(os.path.exists(os.path.join(golden, f)) for f in P.DELIVERABLES))

    ok = all(r[0] for r in RESULTS)
    for good, name, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if good else "FAIL", name, (": " + detail) if detail else ""))
    print("checks: %d of %d pass" % (sum(r[0] for r in RESULTS), len(RESULTS)))
    return ok
