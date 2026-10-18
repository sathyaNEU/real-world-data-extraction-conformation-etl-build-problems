"""task163 checks: the three rules executed on the generator's clean truth, the ladder and every rival, the construction
family and its bin, the one-sigma move, the out-of-sample check, every semantic fork row, the asks against the truth and
their devices, the separation line, the input gates and the realism sweep. Exit 1 on any failure."""
from __future__ import annotations

import collections
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as BL          # noqa: E402
import calc as CA           # noqa: E402
import common as K          # noqa: E402
import company as CO        # noqa: E402
import cracker as CR        # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
ENDS_ON = 2800
# the routes that sit inside a bin of the golden and round to the neighbouring hundred, each named in the ladder with its
# distance and why it misses (ROUTES below asserts that none rounds to the golden and that no other route is inside a bin):
# - before_after, the split against each reform state's own level before go-live (about -0.6 bins): it counts the early
#   2026 rise every state shared as added applications and prices it at the added yield;
# - volume_regression_months, each reform state's formations on its applications with calendar-month terms over every
#   closed cohort (about -0.6 bins): one slope through the months before and after go-live mixes the ordinary rate with
#   the added yield, so the twelve months' ordinary rise is priced below the ordinary rate;
# - 2025 grown with the nine states' applications from January to September 2025 (about -0.7 bins): the nine states'
#   growth leaves out the added applications that do form.
NEAR_ROUTES = {"before_after", "volume_regression_months",
               "2025 grown by the nine states' applications from January to September 2025"}
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, (": " + detail) if detail else ""))


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    return " ".join(re.sub(r"<[^>]+>", "", p) for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S))


def xlsx_strings(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    out = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            out.extend(str(v) for v in row if v is not None)
    return out


def main():
    cal = json.load(open(os.path.join(HERE, "calibration.json")))
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    W = WD.simulate()
    C = CO.build(W, cal["scale"])
    share_truth = BL.share_table(W, C)
    MP = BL.MemPack(W, share_truth)
    P = CA.Pack(TARGET)
    g = CA.golden(P)
    G = g["total"]
    call = CA.round100(G)

    # ------------------------------------------------------------------ the call and its bin
    ok("CALL golden reproduces the write-up", call == fig["call"] and abs(G - fig["call_exact"]) < 0.06,
       "%.1f -> %d" % (G, call))
    F = CA.family(P)
    vals = np.array(list(F.values()))
    ok("FAMILY every construction rounds to the call", all(CA.round100(v) == call for v in vals),
       "%d constructions, %.1f to %.1f" % (len(vals), vals.min(), vals.max()))
    edge = min(K.edge_distance(v, 100) for v in vals)
    ok("FAMILY every construction a quarter bin or more from an edge", edge >= 0.25, "nearest %.3f" % edge)
    Fw = CA.family(P, wide=True)
    ok("FAMILY wide (the nine at their 2021-2022 rate too) rounds to the call",
       all(CA.round100(v) == call for v in Fw.values()), "%.1f to %.1f" % (min(Fw.values()), max(Fw.values())))
    # one sigma of the deciding quantity: the release's counts redrawn as Poisson around themselves
    rr = np.random.default_rng(163)
    orig = {k: v.copy() for k, v in P.bfs.items()}

    def redraw():
        d = {k: v.copy() for k, v in orig.items()}
        for k, v in orig.items():
            if k[1] in ("BA_BA", "BF_BF4Q") and k[2] == "no":
                x = v.copy()
                m = ~np.isnan(x)
                x[m] = rr.poisson(x[m])
                d[k] = x
        return d

    boot = []
    for _ in range(200):
        P.bfs = redraw()
        boot.append(CA.golden(P)["total"])
    P.bfs = {k: v.copy() for k, v in orig.items()}
    sd = float(np.std(boot))
    first_ttm = CA.TTM[0]

    def redraw_estimation():
        """Formations everywhere and applications before the twelve months redrawn; the twelve months' applications
        are the estimand's own volume and stay as filed."""
        d = {k: v.copy() for k, v in orig.items()}
        for k, v in orig.items():
            if k[2] != "no" or k[1] not in ("BA_BA", "BF_BF4Q"):
                continue
            x = v.copy()
            m = ~np.isnan(x)
            idx = np.where(m)[0]
            if k[1] == "BA_BA":
                idx = idx[idx < first_ttm]
            x[idx] = rr.poisson(x[idx])
            d[k] = x
        return d

    boot2 = []
    for _ in range(300):
        P.bfs = redraw_estimation()
        boot2.append(CA.golden(P)["total"])
    P.bfs = {k: v.copy() for k, v in orig.items()}
    lo95, hi95 = np.percentile(boot2, 2.5), np.percentile(boot2, 97.5)
    margin = min(lo95 - (call - 50), (call + 50) - hi95)
    ok("SIGMA the bootstrap's 95 per cent interval sits inside the call's bin with margin",
       margin >= 3, "%.1f to %.1f in %d to %d, margin %.1f (sd %.1f)" % (lo95, hi95, call - 50, call + 50, margin,
                                                                       np.std(boot2)))
    ok("SIGMA one sigma of the release's counts keeps the call",
       CA.round100(G - sd) == call and CA.round100(G + sd) == call and CA.round100(vals.min() - sd) == call
       and CA.round100(vals.max() + sd) == call, "sigma %.1f on %.1f, family %.1f to %.1f" % (sd, G, vals.min(),
                                                                                           vals.max()))
    rel_boot = []
    for _ in range(100):
        P.bfs = redraw()
        rel_boot.append(CA.golden(P)["rel"]["OH"][1])
    P.bfs = {k: v.copy() for k, v in orig.items()}
    ok("SIGMA the pack is restored after the redraws", abs(CA.golden(P)["total"] - G) < 1e-9)
    rel = g["rel"]["OH"][1]
    ok("SIGMA the added applications' relative yield rests on enough formations (one sigma either side stays between "
       "a fifth and a third of the ordinary rate)",
       0.20 <= rel - np.std(rel_boot) and rel + np.std(rel_boot) < 1 / 3.0, "%.3f, sigma %.3f" % (rel, np.std(rel_boot)))

    # the critical components hold their printed values across the family
    reform = sorted(P.changes)
    comp = collections.defaultdict(list)
    import itertools
    for cf, y_, a_ in itertools.product(CA.CF_KINDS, CA.Y_KINDS, CA.A_KINDS):
        for ny in ("all", "latest"):
            for vol in ("no", "yes"):
                o = CA.plan(P, cf, y_, a_, ny, vol)
                comp["added"].append(K.round_to(sum(o["added_ttm"].values()), 100000))
                comp["F"].append(K.round_to(sum(o["F"].values()), 5000))
                comp["share"].append(sum(P.share[s]["share"] * o["F"][s] for s in reform) / o["total"])
                kind, v = o["rel"][reform[0]]
                if a_ in ("A1", "A4", "A5"):
                    comp["rel"].append(v)
                elif a_ == "A2":
                    comp["rel"].append(v / (sum(o["yield"][s] * o["added_ttm"][s] for s in reform) /
                                            sum(o["added_ttm"][s] for s in reform)))
                elif a_ == "A7":
                    comp["rel"].append(v[1] / np.mean([o["rel"][s][1][0] for s in reform]))
    ok("COMPONENT about %s added applications (nearest 100,000) under every construction" %
       fig["components"]["added_ttm_about"], set(comp["added"]) == {fig["components"]["added_ttm_about"]})
    ok("COMPONENT about %s formations (nearest 5,000) under every construction" % fig["components"]["formations_ttm_about"],
       set(comp["F"]) == {fig["components"]["formations_ttm_about"]})
    ok("COMPONENT the three states carry about four fifths of the line under every construction",
       0.75 <= min(comp["share"]) and max(comp["share"]) <= 0.85, "%.3f to %.3f" % (min(comp["share"]),
                                                                                  max(comp["share"])))
    ok("COMPONENT the added applications' yield, pooled over the three states, under a third of the ordinary rate "
       "under every pooled estimator",
       max(comp["rel"]) < 1 / 3.0, "%.3f to %.3f" % (min(comp["rel"]), max(comp["rel"])))

    # the write-up's stated shares and rise
    nine_ = [s_ for s_ in CA.STATES if s_ not in reform]
    Lx = {s_: CA.launch_index(P.changes[s_][0]) for s_ in reform}
    BAx = {s_: CA.series(P, s_, "BA_BA") for s_ in CA.STATES}
    Gx = {s_: CA.counterfactual(P, s_, "CF1", nine_, Lx[s_]) for s_ in reform}
    add_c = sum(sum(BAx[s_][t] - Gx[s_][t] for t in range(Lx[s_], CA.LAST_CLOSED + 1)) for s_ in reform)
    all_c = sum(sum(BAx[s_][t] for t in range(Lx[s_], CA.LAST_CLOSED + 1)) for s_ in reform)
    add_t = sum(g["added_ttm"].values()) / (sum(g["added_ttm"].values()) + sum(g["ordinary_ttm"].values()))
    ttm_ = list(CA.TTM)
    prior_ = [t - 12 for t in ttm_]
    rise9 = sum(BAx[s_][ttm_].sum() for s_ in nine_) / sum(BAx[s_][prior_].sum() for s_ in nine_) - 1
    rise_r = [Gx[s_][ttm_].sum() / Gx[s_][prior_].sum() - 1 for s_ in reform]
    ok("TEXT the added applications are about a fifth of the closed cohorts since go-live and about a third of the "
       "twelve months", 0.15 <= add_c / all_c <= 0.25 and 0.30 <= add_t <= 0.37, "%.3f, %.3f" % (add_c / all_c, add_t))
    ok("TEXT every state's ordinary applications rose about a tenth into the twelve months",
       all(0.08 <= v <= 0.12 for v in [rise9] + rise_r), "nine %.3f, reform %s" % (rise9, ", ".join(
           "%.3f" % v for v in rise_r)))

    # ------------------------------------------------------------------ the three rules on the clean truth
    r0_truth = CA.rung_latest_closed(MP)
    ok("R3a the easy route on the clean truth, every filed rule applied, files the named wrong answer",
       CA.round100(r0_truth) == ENDS_ON and ENDS_ON != call, "%.1f -> %d" % (r0_truth, CA.round100(r0_truth)))
    gt = CA.golden(MP)["total"]
    ok("R3b the easy route with only the decisive step changed files the golden", CA.round100(gt) == call,
       "%.1f" % gt)
    lower = {"all closed cohorts' rate": CA.rung_all_closed(MP), "latest closed quarter's rate":
             CA.rung_latest_quarter(MP), "pre-go-live rate on every application": CA.rung_pre_reform_rate(MP),
             "own before-and-after split": CA.rung_before_after(MP), "added never form": CA.rung_zero_added(MP)}
    ok("R3b each lower rung's single correction leaves a wrong answer",
       all(CA.round100(v) != call for v in lower.values()),
       ", ".join("%s %d" % (k, CA.round100(v)) for k, v in lower.items()))
    RG = CA.rungs(P)
    BY = CA.bypasses(P)
    regs = {k[1]: v for k, v in F.items() if k[0] == "regression"}
    ok("FAMILY the comparison read as a regression (state and month effects; each reform state after go-live) "
       "rounds to the call", all(CA.round100(v) == call for v in regs.values()),
       ", ".join("%s %.1f (%+.2f bins)" % (k, v, (v - G) / 100) for k, v in regs.items()))
    routes = dict(BY)
    routes.update(RG)
    ok("ROUTES no route outside the family rounds to the call", all(CA.round100(v) != call for v in routes.values()),
       "%d routes" % len(routes))
    inside = {k: v for k, v in routes.items() if abs(v - G) < 100}
    ok("ROUTES those inside a bin of the golden round to the neighbouring hundred, each named in the ladder",
       set(inside) <= NEAR_ROUTES and all(CA.round100(v) in (call - 100, call + 100) for v in inside.values()),
       "; ".join("%s %.1f (%+.2f bins)" % (k, v, (v - G) / 100) for k, v in sorted(inside.items(),
                                                                                key=lambda kv: kv[1])))
    nb = min(BY, key=lambda k: abs(BY[k] - G) if k not in NEAR_ROUTES else 1e9)
    ok("BYPASS every other straight line, growth carry and rate trend misses by a full bin or more",
       abs(BY[nb] - G) >= 100, "%d routes, nearest %s %.1f (%.2f bins)" % (len(BY), nb, BY[nb], (BY[nb] - G) / 100))
    nr = min((k for k in RG if k not in NEAR_ROUTES), key=lambda k: abs(RG[k] - G))
    ok("RIVALS every other measured rival misses by a full bin or more", abs(RG[nr] - G) >= 100,
       "nearest %s %.1f (%.2f bins)" % (nr, RG[nr], (RG[nr] - G) / 100))
    ok("RIVALS the default path's answer, two bins or more off", CA.round100(RG["latest_closed"]) == ENDS_ON and
       abs(RG["latest_closed"] - G) >= 200, "%.1f" % RG["latest_closed"])
    # R1: the decisive computation reads the state-month rows; no column holds the deciding quantity
    P2 = CA.Pack(TARGET)
    for s in P2.changes:
        x = P2.bfs[(s, "BF_BF4Q", "no")].copy()
        L = CA.launch_index(P2.changes[s][0])
        x[L:CA.LAST_CLOSED + 1] *= 1.05
        P2.bfs[(s, "BF_BF4Q", "no")] = x
    moved = CA.golden(P2)["total"] - G
    P3 = CA.Pack(TARGET)
    for s in CA.STATES:
        if s not in P3.changes:
            P3.bfs[(s, "BA_BA", "no")] = P3.bfs[(s, "BA_BA", "no")] * np.where(np.arange(CA.NMON) >= CA.mi(2024, 1),
                                                                               1.03, 1.0)
    moved9 = CA.golden(P3)["total"] - G
    ok("R1 the decisive computation reads the reform states' closed cohorts and the nine states' applications",
       moved > 20 and abs(moved9) > 10, "post-go-live formations +5%%: %+.1f; nine states' 2024+ applications +3%%: "
       "%+.1f" % (moved, moved9))
    heads = []
    for f in os.listdir(TARGET):
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            heads += next(csv.reader(open(p, encoding="utf-8")))
        elif f.endswith(".json"):
            rows = json.load(open(p))
            heads += rows[0] + sorted({r[1] for r in rows[1:]})
    bad = [h for h in heads if re.search(r"added|integrat|yield|conversion|incremental|reform", h, re.I)]
    ok("R1 no shipped column or series holds the added applications or a formation yield", not bad, ", ".join(bad))
    # R2: each mess item mishandled leaves the call
    Pv = CA.Pack(TARGET)
    apr = {}
    with open(os.path.join(TARGET, R.F_BFS_APR), encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["sa"] == "U" and row["series"] == "BA_BA":
                for m, mon in enumerate(R.BFS_APR_COLS[5:], start=1):
                    if row[mon]:
                        apr[(row["geo"], CA.mi(int(row["year"]), m))] = float(row[mon])
    for s in CA.STATES:
        x = Pv.bfs[(s, "BA_BA", "no")].copy()
        for t in range(CA.NMON):
            if (s, t) in apr:
                x[t] = apr[(s, t)]
        Pv.bfs[(s, "BA_BA", "no")] = x
    mixed = CA.golden(Pv)["total"]
    ok("R2 the April release's applications for the months it covers, October's for the rest: same call",
       CA.round100(mixed) == call, "%.1f" % mixed)
    sa = CA.plan(P, vol="yes")["total"]
    ok("R2 seasonally adjusted applications for the twelve months: same call", CA.round100(sa) == call, "%.1f" % sa)
    Ps = CA.Pack(TARGET)
    for s in Ps.share:
        Ps.share[s]["share"] = round(Ps.share[s]["share"], 4)
    shown = CA.golden(Ps)["total"]
    ok("R2 the share at its displayed precision: same call", CA.round100(shown) == call, "%.1f" % shown)
    quiet = [s for s in CA.STATES if s not in P.changes and s not in ("IN", "KY", "WI", "TN", "MO")]
    q4 = CA.plan(P, controls=quiet)["total"]
    ok("R2 comparison without the five states whose filing systems changed in other ways: same call",
       CA.round100(q4) == call, "%s: %.1f" % ("+".join(quiet), q4))
    ok("R2 Michigan's go-live part-month counted or left out: same call",
       CA.round100(CA.plan(P, a="A5")["total"]) == call, "%.1f" % CA.plan(P, a="A5")["total"])
    # R3c: nothing planted
    blocks = collections.Counter()
    same_state = False
    vecs = {}
    for s in CA.STATES:
        x = P.bfs[(s, "BA_BA", "no")]
        vecs[s] = tuple(x)
        for t in range(0, CA.NMON - 12):
            blocks[tuple(x[t:t + 12])] += 1
    same_state = len(set(vecs.values())) < len(vecs)
    ok("R3c no copied or backfilled block, no state's series another's", not same_state and max(blocks.values()) == 1)
    texts = []
    for f in os.listdir(TARGET):
        p = os.path.join(TARGET, f)
        if f.endswith(".docx"):
            texts.append(docx_text(p))
        elif f.endswith(".xlsx"):
            texts.append(" ".join(xlsx_strings(p)))
    joined = " ".join(texts)
    ok("R3c no document states a 2027 figure, a forecast or a method for the line",
       not re.search(r"(forecast|expect|estimate|projected|rate of)\b", joined, re.I) and str(call) not in joined
       and format(call, ",") not in joined)
    ok("R3c two governing documents only, no memo, draft or briefing",
       sorted(f for f in os.listdir(TARGET) if f.endswith(".docx")) ==
       ["first_time_employer_counting_notes.docx", "plan_2027_sizing_standard.docx"])

    # ------------------------------------------------------------------ out of sample
    tt = [K.midx(2025, 10) + i for i in range(12)]
    truth = sum(MP.share[s]["share"] * W.F4[s][tt].sum() for s in CA.STATES)
    ok("OUT-OF-SAMPLE the golden forecast lands near the formations the twelve months will produce",
       abs(G - truth) < abs(RG["latest_closed"] - truth) / 4 and abs(G - truth) / truth < 0.04,
       "golden %.1f, truth %.1f, default %.1f" % (G, truth, RG["latest_closed"]))
    # back-test on the closed cohorts across a change of mix: fit the split on the cohorts from a year after each
    # go-live, predict each state's first year after go-live (when its applications first took on added ones)
    reform = sorted(P.changes)
    others = [o for o in CA.STATES if o not in reform]
    Ls = {s: CA.launch_index(P.changes[s][0]) for s in reform}
    Gs = {s: CA.counterfactual(P, s, "CF1", others, Ls[s]) for s in reform}
    BAs = {s: CA.series(P, s, "BA_BA") for s in reform}
    F4s = {s: CA.series(P, s, "BF_BF4Q") for s in reform}
    ys = {s: F4s[s][:Ls[s]].sum() / BAs[s][:Ls[s]].sum() for s in reform}
    fit = {s: list(range(Ls[s] + 12, CA.LAST_CLOSED + 1)) for s in reform}
    r_fit = sum((F4s[s][fit[s]] - ys[s] * Gs[s][fit[s]]).sum() for s in reform) / \
        sum((ys[s] * (BAs[s][fit[s]] - Gs[s][fit[s]])).sum() for s in reform)
    hold = {s: list(range(Ls[s], Ls[s] + 12)) for s in reform}
    obs = sum(F4s[s][hold[s]].sum() for s in reform)
    pred_split = sum(ys[s] * (Gs[s][hold[s]].sum() + r_fit * (BAs[s][hold[s]] - Gs[s][hold[s]]).sum())
                     for s in reform)
    pred_rate = sum(F4s[s][Ls[s] - 12:Ls[s]].sum() / BAs[s][Ls[s] - 12:Ls[s]].sum() * BAs[s][hold[s]].sum()
                    for s in reform)
    err = {"split": pred_split / obs - 1, "latest closed rate": pred_rate / obs - 1}
    ok("BACKTEST across the go-live change of mix the split predicts each state's first year; the latest rate does not",
       abs(err["split"]) < 0.02 and abs(err["latest closed rate"]) > 0.08 and
       abs(err["latest closed rate"]) > 4 * abs(err["split"]),
       ", ".join("%s %+.1f%%" % (k, 100 * v) for k, v in err.items()) + ", yield fitted %.3f" % r_fit)

    # ------------------------------------------------------------------ the share tab and the separation line
    base = {s: int(np.nansum(P.bfs[(s, "BF_BF4Q", "no")][CA.mi(2024, 7):CA.mi(2025, 6) + 1])) for s in CA.STATES}
    ok("SHARE the tab's formations base ties to the October release", all(base[s] == P.share[s]["base"]
                                                                          for s in CA.STATES))
    B = CA.Book(TARGET)
    flag25 = collections.Counter()
    for a in B.acc:
        if a["first_time_employer"] == "Y" and a["first_pay_date"].startswith("2025"):
            flag25[B.first_state([a])] += 1
    true25 = collections.Counter()
    for e, accts in B.by_ein.items():
        first = min(accts, key=lambda r: (r["first_pay_date"], r["account_id"]))
        if first["first_pay_date"].startswith("2025") and e not in B.successor_eins and \
                not B.liable_before(accts, first["first_pay_date"]):
            true25[B.first_state(accts)] += 1
    ok("SHARE the tab's 2025 counts tie to the export read by the flag and read by the counting notes",
       all(flag25[s] == true25[s] == P.share[s]["count"] for s in CA.STATES))
    dev25 = [b for b in C.business.values() if b.kind != "first" and b.spells[0].flag_first and
             b.spells[0].start.year == 2025]
    ok("SEPARATION no ask device row in the call's population (2025 first-time employers)", not dev25,
       "%d" % len(dev25))
    ok("SEPARATION the call reads no company file", set(P.__dict__) == {"bfs", "share", "changes", "target"})

    # ------------------------------------------------------------------ semantic fork rows
    std = docx_text(os.path.join(TARGET, "plan_2027_sizing_standard.docx"))
    notes = docx_text(os.path.join(TARGET, "first_time_employer_counting_notes.docx"))
    ok("SF1 the twelve months' applications are the release's unadjusted counts (filed), and the adjusted give the "
       "same call", CA.round100(sa) == call and "unadjusted counts" in std)
    ok("SF2 the share as displayed or as stored: same call", CA.round100(shown) == call)
    ok("SF3 formations within four quarters, not eight: the standard's sentence",
       "business formations within four quarters" in std)
    fips = sorted({r[7] for r in json.load(open(os.path.join(TARGET, R.F_BFS)))[1:]})
    ok("SF4 the twelve core states: the release holds exactly the twelve the standard names",
       fips == sorted(CA.FIPS) and all(WD.BY[s].name in std for s in CA.STATES))
    apr_last = max(t for (_, t) in apr)
    ok("SF5 the April release cannot form the twelve months to September 2026", apr_last < CA.mi(2026, 4) and
       "October release" in std)
    annual = sum(P.share[s]["share"] * CA.plan(P)["F"][s] / P.bfs[(s, "BA_BA", "no")][CA.TTM].sum() *
                 4 * P.bfs[(s, "BA_BA", "no")][CA.mi(2026, 7):CA.mi(2026, 9) + 1].sum() for s in CA.STATES)
    ok("SF6 a year at the level of the twelve months, not the latest quarter annualised: the standard's sentence",
       "at the level of the twelve months to September 2026" in std, "latest quarter x 4 would give %.0f" % annual)
    ok("SF7 rounding to the nearest 100 sits clear of a half-hundred", K.edge_distance(G, 100) >= 0.25 and
       "nearest 100" in std)
    ok("SF8 the formations the year of applications will produce, not formations in calendar 2027: the standard",
       "will produce" in std)
    carry = sum(P.share[s]["count"] for s in CA.STATES)
    ok("SF16 the share's own base window against the twelve months: the share multiplies the twelve months' "
       "formations; read onto its base window it only returns the 2025 count",
       "over the state's business formations within four quarters from the applications of July 2024 to June 2025"
       in std and abs(carry - G) >= 100, "share on its base window gives %.0f" % carry)
    ok("SF9 a first-time employer is a business whose first payroll ever runs with us: the counting notes",
       "first payroll ever runs with us" in notes and "re-forms as a new entity" in notes)
    ok("SF10 counted in the state it first employed in, not the address state: the counting notes",
       "state it first employed in" in notes)
    ok("SF11 still with us: wages paid with a pay date in the quarter, any account: the counting notes",
       "we paid wages for it, on any of its accounts, with a pay date" in notes)
    ok("SF12 first quarter on payroll: the calendar quarter of the first payroll with us: the counting notes",
       "calendar quarter of its first payroll with us" in notes)
    ok("SF13 wages are the gross wages we ran on our payroll: the counting notes",
       "gross wages we ran on our payroll" in notes)
    grp = collections.defaultdict(dict)
    for r in B.leg:
        grp[(r["client_no"], r["tax_year"], r["tax_qtr"])][r["pay_group"]] = int(r["gross_wages"])
    two = [v for v in grp.values() if len(v) > 1]
    ok("SF14 group 00 is the client's total in every two-group client quarter, to the cent",
       two and all(v["00"] == sum(x for k, x in v.items() if k != "00") for v in two), "%d client quarters" % len(two))
    mism = [(a["signup_channel"], B.code_of[a["account_id"]]) for a in B.acc if a["account_id"] in B.code_of and
            CA.CODE_CHANNEL[B.code_of[a["account_id"]]] != a["signup_channel"]]
    ok("SF15 a migrated account's channel differs from its legacy code only where the load used the default",
       mism and all(ch == "web sign-up" and code in ("CPA", "BP", "TEL", "APX") for ch, code in mism),
       "%d accounts" % len(mism))
    guide = " ".join(xlsx_strings(os.path.join(TARGET, "plan_pack_field_guide.xlsx")))
    ok("SF17 a business bought by a new owner who carries it on is the same business: the counting notes",
       "bought by a new owner who carries it on, is the same business" in notes)
    ok("SF18 first-time status follows the state's liability record, not the onboarding answer: the counting notes",
       "matter of the state's record, not of its onboarding answer" in notes and
       "held liable for unemployment tax before its first payroll with us had paid wages before" in notes)
    ok("SF19 a quarter on tax filing only is not a quarter we paid: the counting notes",
       "A quarter an account spent on tax filing only does not count" in notes and
       "a quarter on tax filing only adds none" in notes)
    ok("SF20 a migrated account's channel is its legacy source code's: the field guide; a business's channel is its "
       "first account's: the counting notes", "the legacy source code in the crosswalk is the record of how the client "
       "came to us" in guide and "the channel of its first account" in notes)
    # SF21: the first payroll is the one we ran wages on; a migrated account's first_pay_date is its client-since date
    leg_rows = [a for a in B.acc if a["account_id"] in B.code_of]
    cur_rows = [a for a in B.acc if a["account_id"] not in B.code_of]
    since_eq = all(a["first_pay_date"] == CA.opened_date(a).isoformat() for a in leg_rows)
    off_leg = [a for a in leg_rows if a["account_id"] in B.first_q and
               B.first_q[a["account_id"]] != CA.quarter_of(a["first_pay_date"])]
    empty = all(B.wq.get((a["account_id"],) + CA.quarter_of(a["first_pay_date"]), 0) == 0 for a in off_leg)
    off_cur = [a for a in cur_rows if a["account_id"] in B.first_q and
               B.first_q[a["account_id"]] != CA.quarter_of(a["first_pay_date"])]
    ok("SF21 a migrated account's first_pay_date is its legacy client-since date; where its quarter differs from the "
       "first quarter with wages the account has no wages in it, and no current-system account differs (the counting "
       "notes count the year the first payroll ran)",
       since_eq and off_leg and empty and not off_cur and "the year its first payroll with us ran" in notes,
       "%d migrated accounts, %d with no wages in the field's quarter; %d current accounts differ" %
       (len(leg_rows), len(off_leg), len(off_cur)))
    named = collections.defaultdict(list)
    for a in B.acc:
        named[(a["legal_name"].upper(), a["dba_name"].upper(), a["naics"], a["entity_type"])].append(a)
    swaps = [(x, y) for rs in named.values() for x in rs for y in rs if x is not y and
             CA.transposed(CA.ein_key(x["ein"]), CA.ein_key(y["ein"]))]
    ein_pairs = {tuple(sorted((CA.ein_key(x["ein"]), CA.ein_key(y["ein"])))) for x, y in swaps}
    rk_pairs = {tuple(sorted(p_)) for p_ in B.rekeyed}
    ok("SF22 every pair of EINs on accounts with the same names, industry and entity that are one swap of adjacent "
       "digits apart belongs to a client re-opened the day after its first account was cancelled, a later account under "
       "the corrected EIN included (A business is the employer, whatever its account or EIN)",
       ein_pairs == rk_pairs and all(B.root[a_] == B.root[b_] for a_, b_ in ein_pairs) and
       "whatever its account or EIN" in notes,
       "%d re-keyed pairs; %d account pairs one swap apart, all on those EIN pairs" % (len(B.rekeyed), len(swaps) // 2))

    # ------------------------------------------------------------------ the asks against the truth
    T, CH, cohort = CA.asks(B)
    tT = {t: {"signed": 0, "still": 0, "wages_cents": 0, "wages_2024_cents": 0} for t in T}
    tCH = collections.Counter()
    for b in CO.first_time(C):
        if b.first_pay.year != 2024:
            continue
        t = R.TERRITORY[b.state0]
        tT[t]["signed"] += 1
        tT[t]["still"] += int(CO.paid_in(C, b, 2025, 4))
        y, q = (b.first_pay.year, (b.first_pay.month - 1) // 3 + 1)
        for x in CO.chain(C, b):
            for sp in x.spells:
                for row in CO.segments(x, sp):
                    a0 = CO.qbounds(row[1], row[2])[0]
                    if (row[1], row[2]) == (y, q):
                        tT[t]["wages_cents"] += int(round(row[5] * 100))
                    if row[1] == 2024 and sp.paid_by_us(a0):
                        tT[t]["wages_2024_cents"] += int(round(row[5] * 100))
        tCH[b.spells[0].channel] += 1
    ok("ASK the golden territory table equals the generator's truth", T == tT)
    ok("ASK the golden channel table equals the generator's truth", CH == dict(tCH))
    ok("ASK the write-up's tables are the golden's", all(
        fig["territories"][t]["signed"] == T[t]["signed"] and fig["territories"][t]["still"] == T[t]["still"] and
        fig["territories"][t]["first_quarter_wages"] == "%.2f" % (T[t]["wages_cents"] / 100) and
        fig["territories"][t]["wages_2024"] == "%.2f" % (T[t]["wages_2024_cents"] / 100) for t in T) and
       all(fig["channels"][c] == CH.get(c, 0) for c in fig["channels"]))
    res = CR.measure(TARGET)
    ok("ASK the cracker misses every ask figure", not res["paths"]["cracker"]["hits"],
       ", ".join(res["paths"]["cracker"]["hits"]))
    singles = {k: v["pair"] for k, v in res["paths"].items() if k.count("+") <= 1 and k != "every device"}
    ok("ASK pair ceiling 40 or under for the cracker and every single-device crack", max(singles.values()) <= 40,
       ", ".join("%s %.1f" % kv for kv in singles.items()))
    base_t = CR.path(B)[0]
    wf_t = CR.path(B, wages_first=True)[0]
    rk_t = CR.path(B, rekey=True)[0]
    ok("ASK the two silent count devices never offset: in every territory the 2024 starters the first pay date moves "
       "into 2023 outnumber the accounts a re-key adds, so the cracker's count falls short",
       all(base_t[t]["signed"] < T[t]["signed"] and rk_t[t]["signed"] < T[t]["signed"] and
           T[t]["signed"] - rk_t[t]["signed"] > wf_t[t]["signed"] - T[t]["signed"] for t in T),
       ", ".join("%s %d against %+d" % (t, T[t]["signed"] - rk_t[t]["signed"], wf_t[t]["signed"] - T[t]["signed"])
                 for t in sorted(T)))
    doubles = {k: v["pair"] for k, v in res["paths"].items() if k.count("+") == 2}
    print("INFO  two devices cracked at once: %s" % ", ".join("%s %.1f" % kv for kv in doubles.items()))
    ok("ASK mirror leakage under 35 per cent", res["mirror_leakage"] < 35, "%.1f" % res["mirror_leakage"])
    # devices present in every territory the asks grade
    inh = collections.Counter(R.TERRITORY.get(b.state0, "") for b in C.business.values() if b.kind == "inhouse" and
                              b.spells[0].flag_first and b.spells[0].start.year == 2024)
    suc = collections.Counter(R.TERRITORY.get(b.state0, "") for b in C.business.values() if b.kind in ("successor", "succ_ext")
                              and b.spells[0].flag_first and b.spells[0].start.year == 2024)
    tax = collections.Counter()
    tax_late = 0
    for b in CO.first_time(C):
        if b.first_pay.year != 2024:
            continue
        for x in CO.chain(C, b):
            for sp in x.spells:
                if sp.product == "Tax filing only" and sp.product_since <= dt.date(2025, 10, 1):
                    tax[R.TERRITORY[b.state0]] += 1
                if sp.product == "Tax filing only" and sp.product_since == dt.date(2026, 1, 1):
                    tax_late += 1
    two_g = collections.Counter(R.TERRITORY[b.state0] for b in CO.first_time(C) if b.first_pay.year == 2024 and
                                b.groups == 2 and b.first_pay <= CO.LEGACY_LAST_PAY)
    movers = collections.Counter(R.TERRITORY[b.state0] for b in CO.first_time(C) if b.first_pay.year == 2024 and
                                 b.moves)
    old_codes = collections.Counter(b.spells[0].channel for b in CO.first_time(C) if b.first_pay.year == 2024 and
                                    b.spells[0].legacy_code in ("CPA", "BP", "TEL", "APX"))
    shown = collections.Counter(R.TERRITORY[b.state0] for b in CO.first_time(C) if b.first_pay.year == 2024 and
                                b.spells[0].legacy and R.shown_first_pay(b.spells[0]).year == 2023)
    shown_ch = collections.Counter(b.spells[0].channel for b in CO.first_time(C) if b.first_pay.year == 2024 and
                                   b.spells[0].legacy and R.shown_first_pay(b.spells[0]).year == 2023)
    rek = collections.Counter(R.TERRITORY[b.state0] for b in CO.first_time(C) if b.first_pay.year == 2024 and b.rekey)
    ok("DEVICE a first payroll the field puts in 2023, in every signup channel", all(shown_ch[c] >= 1 for c in CH),
       ", ".join("%s %d" % kv for kv in sorted(shown_ch.items())))
    for name, cnt in (("self-run businesses flagged first-time", inh), ("successors flagged first-time", suc),
                      ("accounts on tax filing only by the fourth quarter of 2025", tax),
                      ("two-group legacy first quarters", two_g), ("movers", movers),
                      ("first payrolls the field puts in 2023", shown), ("clients re-opened under a corrected EIN",
                                                                         rek)):
        ok("DEVICE %s in every territory's 2024 cohort" % name, all(cnt[t] >= 1 for t in T),
           ", ".join("%s %d" % (t, cnt[t]) for t in sorted(T)))
    ok("DEVICE tax filing only from 1 January 2026 in the cohort (dropping every tax-only account over-cleans)",
       tax_late >= 3, "%d" % tax_late)
    ok("DEVICE legacy codes the load defaulted, in each channel they move",
       all(old_codes[c] >= 3 for c in ("accountant referral", "bank partner", "outbound", "partner marketplace")),
       ", ".join("%s %d" % kv for kv in sorted(old_codes.items())))

    # ------------------------------------------------------------------ input gates and deletion of distractors
    files = sorted(os.listdir(TARGET))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    big = max(meta["files"], key=lambda x: x["rows"] or 0)
    ok("GATE 10 or more files, 3 or more formats, a file of 25,000 rows or more",
       len(files) >= 10 and len(fmts) >= 3 and big["rows"] >= 25000, "%d files, %s, %s %d rows" %
       (len(files), sorted(fmts), big["path"], big["rows"]))
    dis = meta["distractor_files"]
    ok("GATE two distractors, named only in metadata.json", len(dis) >= 2 and all(d in files for d in dis) and
       not any("distract" in f for f in files))
    sand = tempfile.mkdtemp(prefix="t163_", dir=TASK)
    try:
        for f in files:
            if f not in dis:
                os.symlink(os.path.join(TARGET, f), os.path.join(sand, f))
        Pd, Bd = CA.Pack(sand), CA.Book(sand)
        ok("GATE the call and every ask unchanged with the distractors deleted",
           abs(CA.golden(Pd)["total"] - G) < 1e-9 and CA.asks(Bd)[:2] == (T, CH))
    finally:
        shutil.rmtree(sand)

    man = {r["file"] for r in csv.DictReader(open(os.path.join(TARGET, "pack_manifest.csv"), encoding="utf-8"))}
    ok("REGISTER the manifest names every shipped file but itself", man == set(files) - {"pack_manifest.csv"})
    dict_files = set(xlsx_strings(os.path.join(TARGET, "plan_pack_field_guide.xlsx")))
    data_files = [f for f in files if f.endswith((".csv", ".json")) or f in ("plan_2027_workbook.xlsx",
                                                                             "state_filing_changes_log.xlsx")]
    ok("REGISTER the dictionary names every data file", all(f in dict_files for f in data_files if
                                                            f != "pack_manifest.csv"))
    outside = []
    for f in files:
        p = os.path.join(TARGET, f)
        txt = open(p, encoding="utf-8").read() if f.endswith((".csv", ".json")) else (
            docx_text(p) if f.endswith(".docx") else " ".join(xlsx_strings(p)))
        if re.search(r"\b(fictional|fictitious|constructed|this exercise|invented|synthetic|simulated)\b", txt, re.I):
            outside.append(f)
    ok("REGISTER no shipped file steps outside the fiction", not outside, ", ".join(outside))
    norm_ = lambda x: re.sub(r"[.,]", "", x.upper())
    same = [r for r in B.suta if norm_(r["predecessor_name"]) == norm_(r["successor_name"])]
    ok("REALISM a successor never carries its predecessor's exact legal name", not same, "%d rows" % len(same))
    boolish = [a["legal_name"] for a in B.acc if re.search(r"\b(True|False|None|NaN|nan)\b", a["legal_name"] + " " +
                                                           a["dba_name"])]
    ok("REALISM no name reads as a null or a boolean", not boolish, ", ".join(boolish[:3]))
    reg_late = [r for r in B.suta if r["filed_on"] > "2026-03-02"]
    ok("REGISTER the successor register's dates sit on or before its own pull", not reg_late)

    # ------------------------------------------------------------------ realism sweep
    signed = [T[t]["signed"] for t in T]
    still = [T[t]["still"] for t in T]
    rows_ = list(zip(signed, still))
    ok("REALISM no two territories share a row (signed and still together)", len(set(rows_)) == len(rows_))
    ok("REALISM no round totals among the graded figures",
       sum(signed) % 100 and sum(still) % 100 and all(T[t]["wages_cents"] % 100000 for t in T) and G % 10)
    accounts = [a["account_id"] for a in B.acc]
    ok("REALISM account numbers unique, every legacy client in the crosswalk and the export",
       len(set(accounts)) == len(accounts) and all(r["client_no"] in B.acct_of_legacy for r in B.leg) and
       all(r["account_id"] in B.by_acct for r in B.xw))
    all_eins = [b.ein for b in C.business.values()] + [b.pred_ein for b in C.business.values() if b.pred_ein]
    ok("REALISM an EIN belongs to one business only", len(set(all_eins)) == len(all_eins))
    eins = [a["ein"] for a in B.acc]
    ok("REALISM EIN formats as the systems write them (hyphenated, plain, leading zero lost)",
       any("-" in e for e in eins) and any(e.isdigit() and len(e) == 9 for e in eins) and
       any(e.isdigit() and len(e) == 8 for e in eins))
    names = collections.Counter(a["legal_name"].upper() for a in B.acc)
    rep = sum(v for v in names.values() if v > 1) / len(B.acc)
    ok("REALISM legal names repeat at a real book's rate, not a pool's", rep < 0.25, "%.1f%% of accounts" % (100 * rep))
    dash = []
    for f in files:
        p = os.path.join(TARGET, f)
        if f.endswith((".csv", ".json")):
            txt = open(p, encoding="utf-8").read()
        elif f.endswith(".docx"):
            txt = docx_text(p)
        else:
            txt = " ".join(xlsx_strings(p))
        if "\u2014" in txt or "\u2013" in txt:
            dash.append(f)
    ok("REALISM no em or en dashes in any shipped file", not dash, ", ".join(dash))
    people = set(K.PEOPLE.values())
    named = set(re.findall(r"(Dominique Thomas|Charles Fernandez|Cheryl Mitchell|Calvin Garrett)", joined))
    ok("REALISM the personas are the four drawn names", named <= people and len(named) >= 3)
    late = []
    for f in files:
        if f.endswith(".csv"):
            for d in re.findall(r"\b(20\d\d-\d\d-\d\d)\b", open(os.path.join(TARGET, f), encoding="utf-8").read()):
                if d > "2026-10-16":
                    late.append((f, d))
    ok("REALISM no record dated after the as-of", not late, str(late[:3]))
    mt = {int(os.path.getmtime(os.path.join(TARGET, f))) for f in files}
    ok("REALISM every file's mtime is the pack's assembly time", mt == {BL.MTIME})
    core = []
    for f in files:
        if f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(os.path.join(TARGET, f)) as z:
                xml = z.read("docProps/core.xml").decode("utf-8")
            core.append(re.search(r"<dc:creator>(.*?)</dc:creator>", xml).group(1))
    ok("REALISM office files carry their owners, not the writing library", set(core) <= people, str(sorted(set(core))))

    n_fail = sum(1 for _, c, _ in RESULTS if not c)
    print("%d checks, %d failed" % (len(RESULTS), n_fail))
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
