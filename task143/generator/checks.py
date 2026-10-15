"""task143 checks, run on every build: the three-rules block (R1 to R3c) on the clean truth and the pack, every rung by
name with its bin, every construction of the golden in the golden's bin, every semantic fork row (SF1 to SF16), mess
neutrality on the call's path, the asks against the clean truth with every stop and the cracker's path, the separation
line, the distractors, the input gates, the realism sweep and the golden files. Any failure stops the build."""
from __future__ import annotations

import builtins
import csv
import datetime as dt
import itertools
import json
import math
import os
import re
import shutil
import tempfile
from collections import Counter, defaultdict

import numpy as np
import openpyxl
from scipy import stats

import calc as CA
import common as K
import field as FD
import world as WD

BIN = 50
GOLD_BIN = 400
DEFAULT_BIN = 500
MAIN_FILES = [K.F_POLICY, K.F_MEMO, K.F_SPEC, K.F_README, K.F_CYC_A, K.F_CYC_B, K.F_REG, K.F_LIFE, K.F_CELLS, K.F_GEN]
ASK_FILES = [K.F_README_SVC, K.F_CASES, K.F_SAP, K.F_RETURNS, K.F_CARRIER, K.F_FX, K.F_COST] + list(K.F_INV.values())


class Checks:
    def __init__(self):
        self.res = []

    def __call__(self, label, ok, detail=""):
        self.res.append((label, bool(ok), detail))
        return ok

    def report(self):
        bad = [r for r in self.res if not r[1]]
        for lab, ok, det in self.res:
            if not ok:
                print("FAIL %s %s" % (lab, det))
        print("checks.py: %d assertions, %d failed" % (len(self.res), len(bad)))
        if bad:
            raise SystemExit(1)


def b50(x):
    return K.round_to(x, BIN)


def mid(x, step):
    """Distance from the nearest rounding edge as a share of the bin (0.5 mid-bin, 0 on an edge)."""
    q = x / step + 0.5
    return min(q - math.floor(q), math.ceil(q) - q) if q != math.floor(q) else 0.0


class Reads:
    """Which pack files a computation opens."""

    def __init__(self, target):
        self.target = os.path.abspath(target)
        self.seen = set()

    def __enter__(self):
        self.orig = builtins.open
        self.orig_wb = openpyxl.load_workbook
        me = self

        def note(p):
            try:
                p = os.path.abspath(p)
                if p.startswith(me.target):
                    me.seen.add(os.path.basename(p))
            except TypeError:
                pass

        def o(p, *a, **k):
            note(p)
            return me.orig(p, *a, **k)

        def wb(p, *a, **k):
            note(p)
            return me.orig_wb(p, *a, **k)
        builtins.open = o
        openpyxl.load_workbook = wb
        CA.openpyxl.load_workbook = wb
        return self

    def __exit__(self, *a):
        builtins.open = self.orig
        openpyxl.load_workbook = self.orig_wb
        CA.openpyxl.load_workbook = self.orig_wb


def copy_without(target, drop):
    d = tempfile.mkdtemp(suffix=".t143")
    for f in os.listdir(target):
        if f not in drop:
            shutil.copy(os.path.join(target, f), os.path.join(d, f))
    return d


# ---------------------------------------------------------------------------------------------------- mishandled reads
def cycles_variant(target, mode):
    """Each cell's 100 protocol cycles read with one Layer 1 item mishandled."""
    rows = defaultdict(list)
    for r in CA._csv(os.path.join(target, K.F_CYC_A), delimiter=";"):
        cell = CA.norm_cell(r["Zelle"])
        t = dt.datetime.strptime(r["Zyklusende"], "%d.%m.%Y %H:%M:%S")
        if mode != "a_as_utc":
            t = t - dt.timedelta(hours=K.cet_offset(t - dt.timedelta(hours=1)))
        rows[cell].append(("A" + r["Test"], int(r["Zyklus"]), t, float(r["Entladekapazitaet_mAh"].replace(",", ".")),
                           float(r["DCIR_mOhm"].replace(",", ".")), "A"))
    for r in CA._csv(os.path.join(target, K.F_CYC_B)):
        cell = CA.norm_cell(r["cell_id"])
        t = dt.datetime.strptime(r["cycle_end_utc"], "%Y-%m-%dT%H:%M:%SZ")
        rows[cell].append(("B" + r["test_id"], int(r["cycle"]) - 1, t, float(r["discharge_mAh"]),
                           float(r["dcir_10s_mohm"]), "B"))
    out = {}
    for cell, lst in rows.items():
        if mode != "b_dupes":
            seen, ded = set(), []
            for x in lst:
                if (x[0], x[1]) not in seen:
                    seen.add((x[0], x[1]))
                    ded.append(x)
            lst = ded
        tests = defaultdict(list)
        for x in lst:
            tests[x[0]].append(x)
        if mode == "first_test_only" and len(tests) > 1:
            continue
        if mode == "b_dupes" and len(tests) == 1:
            # one test: its cycles picked by their numbers, a repeated row read twice changing nothing
            by_n = {}
            for x in lst:
                by_n.setdefault(x[1], x)
            q = [by_n[k][3] for k in sorted(by_n)]
            res = [by_n[k][4] for k in sorted(by_n)]
            out[cell] = (np.array(q), np.array(res))
            continue
        seq = sorted(tests.values(), key=lambda l: min(x[2] for x in l))
        q, res = [], []
        for l in seq:
            for x in sorted(l, key=lambda x: x[1]):
                q.append(x[3])
                res.append(x[4])
        if mode == "a_numbering" and seq[0][0][5] == "A":
            q = q[1:] + q[-1:]
            res = res[1:] + res[-1:]
        out[cell] = (np.array(q), np.array(res))
    return out


def features_loose(cyc):
    return {c: (math.log(q[9] - q[99]), res[99] - res[9]) for c, (q, res) in cyc.items() if len(q) >= 100}


def comp_of(target):
    return CA.composition(CA.genealogy(target), CA.tray_map(target))


# ---------------------------------------------------------------------------------------------------- the clean truth
def truth_reserves(W, m):
    """The default construction and the decisive step alone on the generator's clean truth: the release-test cells'
    features as the cell made them, RL-3 as QM-07 files it, the error's tray and cell parts as the world drew them."""
    new = [c for c in W.qcells if c.lot == K.NEW_LOT]
    yh = np.array([m["b0"] + m["b1"] * c.lnq + m["b2"] * c.dr for c in new])
    sd = m["rmse"]
    p = float(np.mean(stats.norm.cdf((CA.LN_W - yh) / sd)))
    comp = Counter(tuple(sorted(Counter(W.new.cells[s].tray_no for s in pk).values(), reverse=True))
                   for pk in W.new.packs)
    out = {"R0 truth: independent cells": K.MODEL_K_PACKS * (1 - (1 - p) ** 3)}
    out["R3 truth: the decisive step alone"] = CA.reserve(comp, CA.pack_probs(yh, WD.SD_TRAY ** 2, WD.SD_CELL ** 2))
    # R1's single correction: the tray structure of the release test's predictions
    g = defaultdict(list)
    for c, v in zip(new, yh):
        g[c.tray_no].append(v)
    msw = sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in g.values()) / sum(len(v) - 1 for v in g.values())
    tm = np.array([np.mean(v) for v in g.values()])
    s_sh = math.sqrt(max((6 * ((tm - tm.mean()) ** 2).sum() / (len(tm) - 1) - msw) / 6, 0.0))
    q1 = np.array([np.mean(stats.norm.cdf((CA.LN_W - yh - s_sh * z) / sd)) for z in CA.ZZ])
    out["R1 truth: the predictions' tray structure"] = K.MODEL_K_PACKS * (1 - np.trapezoid((1 - q1) ** 3 * CA.WZ, CA.ZZ))
    # R2's single correction: the finished lots' own tray-mate packs, as they lived
    obs = defaultdict(list)
    for c in W.qcells:
        if c.lot in K.TRAIN_LOTS:
            obs[(c.lot, c.tray_no)].append(c.lnlife)
    trip = [min(v[i] for i in t) < CA.LN_W for v in obs.values() for t in itertools.combinations(range(len(v)), 3)]
    out["R2 truth: the finished lots' tray-mate packs"] = K.MODEL_K_PACKS * float(np.mean(trip))
    return out


def ask_truth(W):
    """The asks from the field's own events, before any record is written: each partner's capacity replacements under
    the warranty carried out from October 2025 to September 2026 and their average cost; the month counts."""
    fx = W.fx
    win = set(CA.WINDOW)
    cons = {c.no: c for c in W.consignments}
    n, tot = Counter(), defaultdict(float)
    months = Counter()
    for ev in W.events:
        if not (ev.code == "CAP" and ev.warranty == "WTY" and ev.closed is not None and ev.fitted is not None):
            continue
        ym = (ev.closed.year, ev.closed.month)
        if ym not in win:
            continue
        months[ym] += 1
        if ev.region == "DACH":
            continue
        ip = FD.PARTNER[ev.region]
        p = FD.PARTNER_CODE[ip]
        cur, lab, hand, diag = FD.FEES[ip]
        rate = 1.0 if cur == "EUR" else fx[ym][cur]
        fr = 0.0
        if getattr(ev, "consignment", None):
            c = cons[ev.consignment]
            fr = c.charge / c.n
        pc = FD.valid(FD.PACK_COST, ev.closed.date())
        n[p] += 1
        tot[p] += (lab + hand) / rate + fr + pc
    return {p: (n[p], tot[p] / n[p]) for p in CA.PARTNERS}, {ym: months[ym] for ym in CA.WINDOW}


# ---------------------------------------------------------------------------------------------------- the run
def run(target, golden, W=None, meta_path=None):
    import build as B
    A = Checks()
    if W is None:
        W = B.world()
    with Reads(target) as rd:
        c = CA.main_call(target)
    main_reads = set(rd.seen)
    g = c["golden"]
    rungs, var = c["rungs"], c["variants"]

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    rows = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                rows[f] = sum(1 for _ in fh) - 1
    A("gate: 10 or more files", len(files) >= 10, len(files))
    A("gate: 3 or more formats", len(fmts) >= 3, sorted(fmts))
    A("gate: a file of 25,000 rows or more", max(rows.values()) >= 25000, max(rows.items(), key=lambda kv: kv[1]))
    meta = json.load(open(meta_path)) if meta_path and os.path.exists(meta_path) else {}
    dis = meta.get("distractor_files", [])
    A("gate: two or more distractors declared", len(dis) >= 2 and all(d in files for d in dis), dis)
    A("gate: no file named for the stump or a distractor",
      not any(re.search(r"distract|decoy|known_issue|answer|trap", f, re.I) for f in files), files)

    # ------------------------------------------------------------------ R1: the field's raw material ships
    need = {K.F_CYC_A, K.F_CYC_B, K.F_LIFE, K.F_REG, K.F_GEN, K.F_CELLS, K.F_MEMO}
    A("R1 the golden's decisive computation reads the cycler rows, the life tests, the register, the genealogy and "
      "the tray map", need <= main_reads, sorted(main_reads))
    A("R1 the call reads no ask file", not (main_reads & set(ASK_FILES)), sorted(main_reads & set(ASK_FILES)))
    heads = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                heads += next(csv.reader(fh, delimiter=";" if f == K.F_CYC_A else ","))
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            for ws in wb.worksheets:
                for r in ws.iter_rows(max_row=12, values_only=True):
                    heads += [str(x) for x in r if x is not None]
    A("R1 no shipped column holds a tray effect, a correlation, a pack probability or a reserve",
      not [h for h in heads if re.search(r"tray.?effect|correl|intraclass|icc|probab|reserve|predicted|n80", h, re.I)],
      [h for h in heads if re.search(r"tray.?effect|correl|intraclass|icc|probab|reserve|predicted|n80", h, re.I)][:5])
    from pypdf import PdfReader
    docs = {f: re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, f)).pages))
            for f in files if f.endswith(".pdf")}
    texts = dict(docs)
    for f in files:
        if f.endswith(".txt"):
            texts[f] = re.sub(r"\s+", " ", open(os.path.join(target, f), encoding="utf-8").read())
    A("R1 no document names a shared error, a tray effect, a correlation or a joint chance",
      not [f for f, t in texts.items() if re.search(r"tray effect|correlat|intraclass|random effect|share[sd]? (?:the|an|its) "
                                                    r"error|jointly|independen|weakest of", t, re.I)],
      [f for f, t in texts.items() if re.search(r"tray effect|correlat|intraclass|random effect|independen", t, re.I)])

    # ------------------------------------------------------------------ R2: every mess item neutral on the call
    m = c["model"]
    reg = CA.register(target)
    lifes = CA.life(target)
    comp = comp_of(target)
    new_cells = sorted(cl for cl, r in reg.items() if r["lot"] == "ZC2638")
    for mode, label in (("a_numbering", "fleet A's first cycle numbered 0 read as the protocol's"),
                        ("b_dupes", "fleet B's overlapping pulls kept"),
                        ("first_test_only", "a test continued on another channel read as a cell's whole test"),
                        ("a_as_utc", "fleet A's Bielefeld wall time read as UTC")):
        feat = features_loose(cycles_variant(target, mode))
        cells = [x for x in new_cells if x in feat]
        lf = {k: v for k, v in lifes.items() if k in feat}
        r_, _, _ = CA.reserve_from(m, feat, lf, reg, cells, comp)
        A("R2 %s: the call stays at %d" % (label, GOLD_BIN), b50(r_) == GOLD_BIN, "%.1f" % r_)
    feat = CA.features(CA.cycles(target))
    lf2 = {k: (dict(v, status="EOL") if v["status"] == "STOPPED" else v) for k, v in lifes.items()}
    r_, _, _ = CA.reserve_from(m, feat, lf2, reg, new_cells, comp)
    A("R2 a life test stopped by a fault read as the cell's life: the call stays", b50(r_) == GOLD_BIN, "%.1f" % r_)
    r_ = CA.reserve(Counter({(3,): K.MODEL_K_PACKS}), c["probs"])
    A("R2 packs completed from part trays read as three tray-mates: the call stays", b50(r_) == GOLD_BIN, "%.1f" % r_)
    raw_t = defaultdict(set)
    for cl, r in reg.items():
        raw_t[r["lot"]].add(r["tray"])
    A("R2 the tray key's two formats never meet inside a lot (grouping on the raw key is the grouping)",
      all(len({k[:2] for k in v}) == 1 for v in raw_t.values()), "")
    A("R2 every serial form joins: release cells in the cyclers, the register and the life tests",
      set(new_cells) <= set(feat) and all(k in feat for k in lifes), "")

    # ------------------------------------------------------------------ R3a, R3b: the analyst test on the clean truth
    tr = truth_reserves(W, c["model"])
    A("R3a the easy route on the clean truth files the default answer (%d)" % DEFAULT_BIN,
      b50(tr["R0 truth: independent cells"]) == DEFAULT_BIN, "%.1f" % tr["R0 truth: independent cells"])
    A("R3b the decisive step alone on the clean truth files the golden (%d)" % GOLD_BIN,
      b50(tr["R3 truth: the decisive step alone"]) == GOLD_BIN, "%.1f" % tr["R3 truth: the decisive step alone"])
    A("R3b R1's single correction on the clean truth stays wrong", b50(tr["R1 truth: the predictions' tray structure"])
      not in (GOLD_BIN,), "%.1f" % tr["R1 truth: the predictions' tray structure"])
    A("R3b R2's single correction on the clean truth stays wrong",
      b50(tr["R2 truth: the finished lots' tray-mate packs"]) not in (GOLD_BIN,),
      "%.1f" % tr["R2 truth: the finished lots' tray-mate packs"])
    A("R3a the pack's default and golden differ on the clean truth by one bin or more",
      abs(b50(tr["R0 truth: independent cells"]) - b50(tr["R3 truth: the decisive step alone"])) >= BIN, "")

    # ------------------------------------------------------------------ the ladder on the pack
    want = {"R-1 plug-in (cells predicted under 600)": 0, "R0 default: the cell chance at the model error, three "
            "independent cells": 500, "R0b the same at the in-sample residual error": 500,
            "R0c each cell with the residuals bootstrapped, independent cells": 500,
            "R1 the release test's own tray structure, model error independent": 500,
            "R2 the finished lots' tray-mate packs, as observed": 150,
            "R2b the finished lots' cell share, three independent cells": 200,
            "R2c the three weakest finished lots' tray-mate packs": 250,
            "Rover the whole pack as one cell": 200, "Rx the cell chance compounded over two cells": 350,
            "R3 golden: each pack's tray-shared joint chance": 400}
    for k, v in want.items():
        A("rung %s files %d" % (k, v), b50(rungs[k]) == v, "%.1f" % rungs[k])
    for k, v in rungs.items():
        if not k.startswith("R3"):
            A("rival %s misses the golden's bin by a bin or more" % k, abs(b50(v) - GOLD_BIN) >= BIN, "%.1f" % v)
    A("the default path's figure sits clear of its bin edges", mid(rungs["R0 default: the cell chance at the model "
      "error, three independent cells"], BIN) >= 0.2, "")
    for k, v in var.items():
        A("construction %s files %d" % (k, GOLD_BIN), b50(v) == GOLD_BIN, "%.1f" % v)
    A("the golden sits mid-bin (at least 0.35 of a bin from each edge)", mid(g, BIN) >= 0.35, "%.2f" % g)
    A("every construction of the golden within 3 per cent of it, a quarter of a bin", all(abs(v - g) / g < 0.03
                                                                                       for v in var.values()),
      {k: round(v, 1) for k, v in var.items()})
    # H14: the error's window. FIN-RS-04 3.3 files every finished lot; the halves a reader might split on agree
    res_all = CA.residuals(m, CA.features(CA.cycles(target)), lifes, reg)
    flots = sorted({x[0] for x in res_all}, key=K.LOTS.index)

    def on(sub):
        a_, b_ = CA.components([x for x in res_all if x[0] in sub])
        return CA.reserve(c["comp"], CA.pack_probs(c["yh"], a_, b_))
    A("H14 FIN-RS-04 3.3 files the error on every finished lot's life tests",
      "the model's error on the life tests of every earlier lot whose life tests have finished" in docs[K.F_POLICY], "")
    cut = K.LOTS.index(K.TRAY_KEY_CHANGE)
    pre, post = [l for l in flots if K.LOTS.index(l) < cut], [l for l in flots if K.LOTS.index(l) >= cut]
    A("H14 the lots before Zelvora's tray key change alone file 400", b50(on(pre)) == GOLD_BIN, "%.1f" % on(pre))
    A("H14 the lots from the tray key change alone file 400", b50(on(post)) == GOLD_BIN, "%.1f" % on(post))
    lo = [on([x for x in flots if x != l]) for l in flots]
    A("H14 every leave-one-lot-out estimate files 400", all(b50(v) == GOLD_BIN for v in lo),
      "%.1f to %.1f" % (min(lo), max(lo)))
    A("H14 the odd and the even lots each file 400", b50(on(flots[0::2])) == GOLD_BIN and b50(on(flots[1::2])) ==
      GOLD_BIN, "%.1f, %.1f" % (on(flots[0::2]), on(flots[1::2])))
    # the stump's data facts
    A("the finished lots' error is mostly the tray's (share above 0.7)", c["icc"] > 0.7, "%.3f" % c["icc"])
    A("the release test's predictions carry almost no tray structure (share under 0.05)", c["new_pred_icc"] < 0.05,
      "%.3f" % c["new_pred_icc"])
    lot_mean = defaultdict(list)
    for cl, L in lifes.items():
        lot_mean[L["lot"]].append(CA.predict(m, feat[cl]))
    new_mean = float(np.mean(c["yh"]))
    A("the lot under release predicts shorter lives than all but two finished lots",
      sum(1 for v in lot_mean.values() if np.mean(v) < new_mean) <= 2, "%.3f" % new_mean)
    A("every release-test cell's point prediction clears 600 cycles (the plug-in reserve is nil)",
      float(np.min(c["yh"])) > CA.LN_W, "%.3f" % float(np.min(c["yh"])))
    A("most packs are three tray-mates", c["comp"].get((3,), 0) > 0.95 * c["n_packs"], c["comp"])
    A("the genealogy holds the lot's 7,200 packs, three cells each",
      c["n_packs"] == K.MODEL_K_PACKS and all(len(v) == 3 for v in CA.genealogy(target).values()), c["n_packs"])

    # ------------------------------------------------------------------ the semantic fork table
    A("SF1 the population is the 7,200 Model K packs of the genealogy; Model J packs are another genealogy",
      c["n_packs"] == 7200 and not set(CA.genealogy(target)) & {r["pack_sn"] for r in CA._csv(os.path.join(
          target, K.F_MODEL_J))}, "")
    for lnw, lab in ((math.log(599.5), "below 600 cycles"), (math.log(600.5), "at or below 600 cycles")):
        r_ = CA.reserve(c["comp"], CA.pack_probs(c["yh"], c["s2t"], c["s2c"], lnw))
        A("SF2/SF3 the warranty line read as %s: same call" % lab, b50(r_) == GOLD_BIN, "%.1f" % r_)
    A("SF4 FIN-RS-04 makes gauge cycles QP-3 cycles", "which are the cycles of the reliability lab's qualification "
      "protocol QP-3" in docs[K.F_POLICY], "")
    # SF5: the pack's capacity as its cells' mean instead of its weakest cell
    qz = lambda z, k: None
    ys = c["yh"]
    st, sc = math.sqrt(c["s2t"]), math.sqrt(c["s2c"])
    rr = np.random.default_rng(143)
    T = rr.normal(0, st, 400000)
    C3 = rr.normal(0, sc, (400000, 3))
    Y = ys[rr.integers(0, len(ys), (400000, 3))]
    mean_rule = K.MODEL_K_PACKS * float(np.mean(np.log(np.exp(Y + T[:, None] + C3).mean(1)) < CA.LN_W))
    A("SF5 a pack's capacity as its cells' mean (ruled out by the specification's weakest-cell rule) misses",
      b50(mean_rule) != GOLD_BIN and "weakest cell" in docs[K.F_SPEC], "%.1f" % mean_rule)
    # SF6: the expected number against a percentile of the count (the count's spread from shared tray errors)
    pk = CA.genealogy(target)
    tm = CA.tray_map(target)
    tray_packs = Counter(tm[cells[0]] for cells in pk.values())
    sims = []
    rr = np.random.default_rng(1431)
    for _ in range(400):
        tot = 0
        for tray, npk in tray_packs.items():
            t_ = rr.normal(0, st)
            y_ = ys[rr.integers(0, len(ys), (npk, 3))] + t_ + rr.normal(0, sc, (npk, 3))
            tot += int((y_.min(1) < CA.LN_W).sum())
        sims.append(tot)
    p90 = float(np.percentile(sims, 90))
    A("SF6 the reserve as a high percentile of the count (ruled out by FIN-RS-04 3.2's expected number) lies above "
      "the golden", p90 > g and "The reserve is the expected number" in docs[K.F_POLICY], "%.1f" % p90)
    A("SF7 rounding to the nearest 50 (FIN-RS-04 3.4): 400, 23.9 or more from either edge",
      b50(g) == 400 and min(g - 375, 425 - g) > 20, "%.2f" % g)
    beta, *_ = CA.fit_ols(feat, lifes)
    m2 = {"b0": beta[0], "b1": beta[1], "b2": beta[2], "rmse": m["rmse"]}
    r_, _, _ = CA.reserve_from(m2, feat, lifes, reg, new_cells, comp)
    A("SF8 RL-3 as QM-07 publishes it and as refitted on the life tests: same call", b50(r_) == GOLD_BIN, "%.1f" % r_)
    A("SF9 the protocol's first cycle: fleet A's 0, fleet B's 1 (QM-07 section 2, the extracts note)",
      "Cycle 1 is the protocol's first full cycle" in docs[K.F_MEMO] and "numbers a test's first cycle 0" in
      texts[K.F_README], "")
    f10 = {k: (math.log10(math.exp(v[0])), v[1]) for k, v in feat.items()}
    r_, _, _ = CA.reserve_from(m, f10, lifes, reg, new_cells, comp)
    A("SF10 F1 on a common logarithm (QM-07 files the natural logarithm) misses", b50(r_) != GOLD_BIN and
      "natural logarithm" in docs[K.F_MEMO], "%.1f" % r_)
    A("SF11 the life tests cover the twenty finished lots and no open lot",
      sorted({L["lot"] for L in lifes.values()}) == sorted(K.TRAIN_LOTS), "")
    r_ = CA.reserve(Counter({(3,): 7200}), c["probs"])
    A("SF12 every pack taken as three tray-mates: same call", b50(r_) == GOLD_BIN, "%.1f" % r_)
    # SF13: the split from leave-one-lot-out residuals
    lots = sorted({L["lot"] for L in lifes.values()})
    res_lolo = []
    for lot in lots:
        b_, *_ = CA.fit_ols(feat, lifes, [l for l in lots if l != lot])
        for cl, L in lifes.items():
            if L["lot"] == lot and L["status"] == "EOL":
                f1, f2 = feat[cl]
                res_lolo.append((lot, reg[cl]["tray"], cl, math.log(float(L["cycles"])) - (b_[0] + b_[1] * f1 +
                                                                                           b_[2] * f2)))
    s2t_l, s2c_l = CA.components(res_lolo)
    r_ = CA.reserve(c["comp"], CA.pack_probs(c["yh"], s2t_l, s2c_l))
    A("SF13 the tray and cell parts split from the validation's own errors: same call", b50(r_) == GOLD_BIN,
      "%.1f" % r_)
    s2tot = m["rmse"] ** 2
    r_ = CA.reserve(c["comp"], CA.pack_probs(c["yh"], s2tot * c["icc"], s2tot * (1 - c["icc"])))
    A("SF13 the validation error split at the finished lots' tray share: same call", b50(r_) == GOLD_BIN, "%.1f" % r_)
    A("SF14 the release-test predictions as the lot's cells, or a normal fitted to them: same call",
      b50(var["normal fit to the predictions"]) == GOLD_BIN, "%.1f" % var["normal fit to the predictions"])
    A("SF15 a lot-level error component is nil on the finished lots (REML), so new trays share no lot draw",
      c["reml"][0] < 0.002 and b50(var["REML, the lot level shared too"]) == GOLD_BIN, c["reml"])
    A("SF16 FIN-RS-04 counts packs falling below the line, not claims: no claim rate enters",
      "probability that its full charge capacity falls below 80 per cent" in docs[K.F_POLICY], "")

    # ------------------------------------------------------------------ the asks
    A_, B_ = CA.ask_stops(target)
    at, bt = ask_truth(W)
    ga, gb = A_["golden"], B_["golden"]
    A("ask A fair: the golden handling reproduces the field's own replacements and costs exactly",
      all(ga[p][0] == at[p][0] and abs(ga[p][1] - at[p][1]) < 1e-6 for p in CA.PARTNERS),
      {p: (ga[p], at[p]) for p in CA.PARTNERS})
    A("ask B fair: the golden handling reproduces the field's own month counts exactly", gb == bt, (gb, bt))
    for p in CA.PARTNERS:
        A("ask A %s average mid-bin (within 0.2 of a whole euro)" % p, mid(ga[p][1], 1) >= 0.3, "%.4f" % ga[p][1])
    A("ask A the partners' counts all differ", len({ga[p][0] for p in CA.PARTNERS}) == 4, ga)
    A("ask B the twelve month counts all differ", len(set(gb.values())) == 12, gb)
    crack_a = A_["cracker: closing days and the log's freight"]
    for p in CA.PARTNERS:
        A("cracker misses ask A %s count" % p, crack_a[p][0] != ga[p][0], (crack_a[p], ga[p]))
        A("cracker misses ask A %s average" % p, K.round_to(crack_a[p][1], 1) != K.round_to(ga[p][1], 1),
          (crack_a[p], ga[p]))
        A("ask A primary (freight on every row) alone misses %s's average" % p,
          K.round_to(A_["A1 the returns log's freight on each battery's row"][p][1], 1) != K.round_to(ga[p][1], 1), "")
        A("ask A device (closing days) alone misses %s's count" % p,
          A_["A2 each case dated by its closing day"][p][0] != ga[p][0], "")
        A("ask A no freight misses %s's average" % p, K.round_to(A_["A7 no freight"][p][1], 1) !=
          K.round_to(ga[p][1], 1), "")
    crack_b = B_["cracker: closing months"]
    A("cracker misses every ask B month by 2 or more", all(abs(crack_b[ym] - gb[ym]) >= 2 for ym in CA.WINDOW),
      [(crack_b[ym], gb[ym]) for ym in CA.WINDOW])
    A("ask B hazard: the carried-over depot orders counted twice move October to February",
      all(B_["B2 the carried-over depot orders counted in both systems"][ym] != gb[ym] for ym in CA.WINDOW[:5]), "")
    A("ask B goodwill kept moves every month", all(B_["B3 goodwill replacements kept"][ym] != gb[ym]
                                                   for ym in CA.WINDOW), "")
    A("ask A goodwill kept moves every partner's count", all(A_["A6 goodwill replacements kept"][p][0] != ga[p][0]
                                                             for p in CA.PARTNERS), "")
    # the device's own data facts: freight on every row is the consignment's charge; a partner case closes after its
    # repair month; the carrier bills each consignment once
    carrier, by_ref = CA.freight(target)
    ok_rows = all(abs(float(v[1]) - carrier[v[0]][0]) < 0.005 for v in by_ref.values() if v[1] is not None
                  and v[0] in carrier)
    A("device D6: the returns log's freight on a battery's row is its whole consignment's carrier charge", ok_rows, "")
    multi = sum(1 for v in carrier.values() if v[1] > 1)
    A("device D6: most partner consignments carry several batteries", multi > 0.8 * len(carrier), multi)
    late = [e for e in CA.partner_replacements(target) if e["line"] is not None]
    cs = {r["case_no"]: r for r in CA.cases(target)}
    lag = [e for e in late if cs[e["case"]]["closed_utc"] and CA._d(cs[e["case"]]["closed_utc"]) >=
           dt.date(e["ym"][0] + e["ym"][1] // 12, e["ym"][1] % 12 + 1, 1)]
    A("device D8: every closed partner case closed after its service period ended",
      len(lag) == sum(1 for e in late if cs[e["case"]]["closed_utc"]), (len(lag), len(late)))
    A("device D8: no filed sentence says when a partner case closes",
      not re.search(r"clos\w* when|approv", texts.get(K.F_README_SVC, ""), re.I), "")
    with Reads(target) as rd2:
        CA.ask_a(target)
        CA.ask_b(target)
    A("separation: the asks read no file the call reads but the shared notes",
      not (rd2.seen & set(MAIN_FILES)), sorted(rd2.seen & set(MAIN_FILES)))
    d = copy_without(target, set(ASK_FILES))
    try:
        A("separation: the call computed with every ask file removed is the golden",
          abs(CA.main_call(d)["golden"] - g) < 1e-9, "")
    finally:
        shutil.rmtree(d)
    d = copy_without(target, set(MAIN_FILES) - {K.F_README})
    try:
        A("separation: the asks computed with every main-call file removed are the asks",
          CA.ask_a(d) == ga and CA.ask_b(d) == gb, "")
    finally:
        shutil.rmtree(d)

    # ------------------------------------------------------------------ distractors
    d = copy_without(target, set(dis))
    try:
        A("distractors: the call, the asks and every rung unchanged with both deleted",
          abs(CA.main_call(d)["golden"] - g) < 1e-9 and CA.ask_a(d) == ga and CA.ask_b(d) == gb, "")
    finally:
        shutil.rmtree(d)
    with Reads(target) as rd3:
        CA.compute(target)
    A("distractors: the golden pipeline opens neither", not (rd3.seen & set(dis)), sorted(rd3.seen & set(dis)))

    # ------------------------------------------------------------------ the realism sweep
    stamp = B.EXPORT_STAMP.timestamp()
    A("realism: every file stamped with the export time", all(abs(os.path.getmtime(os.path.join(target, f)) - stamp)
                                                              < 1 for f in files), "")
    dash = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith((".csv", ".txt")):
            if re.search("[\u2013\u2014]", open(p, encoding="utf-8").read()):
                dash.append(f)
        elif f.endswith(".pdf") and re.search("[\u2013\u2014]", docs[f]):
            dash.append(f)
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            for ws in wb.worksheets:
                for r in ws.iter_rows(values_only=True):
                    if any(isinstance(x, str) and re.search("[\u2013\u2014]", x) for x in r):
                        dash.append(f)
                        break
    A("realism: no en or em dash in any shipped file", not dash, dash)
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                       ".claude", "skills", "fingerprint", "cards", "task143.json")))
    people = {p["name"] if isinstance(p, dict) else p for p in card["world"]["people"]}
    A("realism: every persona the pack names is on the card", set(K.PEOPLE.values()) <= people, people)
    eol = Counter(L["lot"] for L in lifes.values() if L["status"] == "EOL")
    A("realism: the finished lots' cells reaching 80 per cent are not one count", len(set(eol.values())) > 3, eol)
    A("realism: the unrounded reserve is not a round number", abs(g - round(g / 5) * 5) > 0.5, "%.2f" % g)
    a_rows = CA._csv(os.path.join(target, K.F_CYC_A), delimiter=";")
    blocks = Counter(tuple(r["Entladekapazitaet_mAh"] for r in a_rows[i:i + 100]) for i in range(0, len(a_rows) - 100,
                                                                                                  100))
    A("R3c no copied block: no 100-cycle run of fleet A repeats", max(blocks.values()) == 1, max(blocks.values()))
    b_rows = CA._csv(os.path.join(target, K.F_CYC_B))
    keyc = Counter((r["test_id"], r["cycle"]) for r in b_rows)
    dups = [r for r in b_rows if keyc[(r["test_id"], r["cycle"])] > 1]
    full = Counter(tuple(r.values()) for r in dups)
    A("R3c fleet B's repeats are its overlapping weekly pulls: whole rows, twice, Mondays before 06:00 UTC",
      all(v == 2 for v in full.values()) and all(
          dt.datetime.strptime(r["cycle_end_utc"], "%Y-%m-%dT%H:%M:%SZ").weekday() == 0 and
          dt.datetime.strptime(r["cycle_end_utc"], "%Y-%m-%dT%H:%M:%SZ").hour < 6 for r in dups), len(dups))
    A("R3c no memo, draft or note states a reserve, a pack failure rate or a method for one",
      not [f for f, t in texts.items() if re.search(r"\breserve of \d|\d+ packs? (?:to|will) fail|pack failure rate", t,
                                                    re.I)], "")

    # ------------------------------------------------------------------ the golden files
    figs = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    wb = openpyxl.load_workbook(os.path.join(golden, K.GOLD_BOOK), data_only=True)
    ws = wb["Reserve"]
    A("golden: the workbook's reserve is the call", ws["B5"].value == b50(g) == int(figs["call"]["reserve_packs"]),
      ws["B5"].value)
    ws = wb["Partner cost"]
    got = {r[0]: r for r in ws.iter_rows(min_row=5, max_row=8, values_only=True)}
    import deliver as DL
    A("golden: the workbook's partner table is ask A", all(got[DL.PARTNER_NAME[p]][1] == ga[p][0] and
                                                           got[DL.PARTNER_NAME[p]][5] == K.round_to(ga[p][1], 1)
                                                           for p in CA.PARTNERS), got)
    ws = wb["Monthly replacements"]
    got = [r[6] for r in ws.iter_rows(min_row=5, max_row=16, values_only=True)]
    A("golden: the workbook's month table is ask B", got == [gb[ym] for ym in CA.WINDOW], got)
    A("golden: figures.json carries ask A and ask B as the workbook does",
      all(figs["ask_a"][p]["replacements"] == "{:,}".format(ga[p][0]) for p in CA.PARTNERS) and
      [int(figs["ask_b"][DL.month_label(ym)]) for ym in CA.WINDOW] == [gb[ym] for ym in CA.WINDOW], "")
    import docx
    note = docx.Document(os.path.join(golden, K.GOLD_NOTE))
    first = next(p.text for p in note.paragraphs if p.text.startswith("Book"))
    A("golden: the note opens with the reserve", "%d packs" % b50(g) in first, first)
    A("golden: the note carries the chart", len(note.inline_shapes) == 1, "")
    A.report()
    return A
