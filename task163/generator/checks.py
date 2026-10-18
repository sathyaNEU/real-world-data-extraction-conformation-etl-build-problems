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
    ok("FAMILY wide (the nine at their 2022-2023 rate too) rounds to the call",
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
    ok("SIGMA the added applications' relative yield rests on enough formations",
       0.14 <= rel - np.std(rel_boot) and rel + np.std(rel_boot) < 0.20, "%.3f, sigma %.3f" % (rel, np.std(rel_boot)))

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
    ok("COMPONENT about half a million added applications under every construction",
       set(comp["added"]) == {fig["components"]["added_ttm_about"]} == {500000})
    ok("COMPONENT about %s formations (nearest 5,000) under every construction" % fig["components"]["formations_ttm_about"],
       set(comp["F"]) == {fig["components"]["formations_ttm_about"]})
    ok("COMPONENT the three states carry about four fifths of the line under every construction",
       0.75 <= min(comp["share"]) and max(comp["share"]) <= 0.85, "%.3f to %.3f" % (min(comp["share"]),
                                                                                  max(comp["share"])))
    ok("COMPONENT the added applications' yield, pooled over the three states, under a fifth of the ordinary rate "
       "under every pooled estimator",
       max(comp["rel"]) < 0.20, "%.3f to %.3f" % (min(comp["rel"]), max(comp["rel"])))

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
    near = min(abs(v - G) for v in RG.values())
    ok("RIVALS every measured rival misses by a full bin or more", near >= 100,
       "nearest %.1f (%s)" % (near, min(RG, key=lambda k: abs(RG[k] - G))))
    ok("RIVALS the default path's answer", CA.round100(RG["latest_closed"]) == ENDS_ON, "%.1f" % RG["latest_closed"])
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
    # back-test on the closed cohorts: fit the split on go-live to December 2024, predict January to June 2025
    Pb = CA.Pack(TARGET)
    save = CA.LAST_CLOSED
    CA.LAST_CLOSED = CA.mi(2024, 12)
    gb = CA.plan(Pb)
    CA.LAST_CLOSED = save
    hold = list(range(CA.mi(2025, 1), CA.mi(2025, 6) + 1))
    err = {}
    obs = sum(P.bfs[(s, "BF_BF4Q", "no")][hold].sum() for s in P.changes)
    pred_split = 0.0
    pred_blend = 0.0
    pred_pre = 0.0
    for s in P.changes:
        L = CA.launch_index(P.changes[s][0])
        Gs = CA.counterfactual(P, s, "CF1", [o for o in CA.STATES if o not in P.changes], L)
        BA = P.bfs[(s, "BA_BA", "no")]
        F4 = P.bfs[(s, "BF_BF4Q", "no")]
        y = gb["yield"][s]
        r = gb["rel"][s][1]
        pred_split += y * (Gs[hold].sum() + r * (BA[hold] - Gs[hold]).sum())
        lo = CA.mi(2024, 1)
        pred_blend += F4[lo:CA.mi(2024, 12) + 1].sum() / BA[lo:CA.mi(2024, 12) + 1].sum() * BA[hold].sum()
        pred_pre += y * BA[hold].sum()
    err = {"split": pred_split / obs - 1, "latest blended rate": pred_blend / obs - 1, "pre-go-live rate":
           pred_pre / obs - 1}
    ok("BACKTEST the split fitted to December 2024 predicts January to June 2025 formations; the rivals do not",
       abs(err["split"]) < 0.02 and abs(err["latest blended rate"]) > 3 * abs(err["split"]) and
       abs(err["pre-go-live rate"]) > 3 * abs(err["split"]),
       ", ".join("%s %+.1f%%" % (k, 100 * v) for k, v in err.items()))

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
    ok("SF1 seasonally adjusted twelve-month total: same call", CA.round100(sa) == call)
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
    ok("SF9 a first-time employer is a business whose first payroll ever runs with us: the counting notes",
       "first payroll ever runs with us" in notes and "re-forms as a new entity" in notes)
    ok("SF10 counted in the state it first employed in, not the address state: the counting notes",
       "state it first employed in" in notes)
    ok("SF11 still with us: wages paid with a pay date in the quarter, any account: the counting notes",
       "we paid wages for it, on any of its accounts, with a pay date" in notes)
    ok("SF12 first quarter on payroll: the calendar quarter of the first pay date: the counting notes",
       "calendar quarter of its first pay date" in notes)
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
    ok("ASK mirror leakage under 35 per cent", res["mirror_leakage"] < 35, "%.1f" % res["mirror_leakage"])
    # devices present in every territory the asks grade
    inh = collections.Counter(R.TERRITORY[b.state0] for b in C.business.values() if b.kind == "inhouse" and
                              b.spells[0].flag_first and b.spells[0].start.year == 2024)
    suc = collections.Counter(R.TERRITORY[b.state0] for b in C.business.values() if b.kind in ("successor", "succ_ext")
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
    for name, cnt in (("self-run businesses flagged first-time", inh), ("successors flagged first-time", suc),
                      ("accounts on tax filing only by the fourth quarter of 2025", tax),
                      ("two-group legacy first quarters", two_g), ("movers", movers)):
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
    ok("REALISM no two territories share a count", len(set(signed)) == len(signed) and len(set(still)) == len(still))
    ok("REALISM no round totals among the graded figures",
       sum(signed) % 100 and sum(still) % 100 and all(T[t]["wages_cents"] % 100000 for t in T) and G % 10)
    accounts = [a["account_id"] for a in B.acc]
    ok("REALISM account numbers unique, every legacy client in the crosswalk and the export",
       len(set(accounts)) == len(accounts) and all(r["client_no"] in B.acct_of_legacy for r in B.leg) and
       all(r["account_id"] in B.by_acct for r in B.xw))
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
