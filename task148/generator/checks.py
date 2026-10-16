"""task148 checks, run on every build: the input gates, the realism sweep, the three rules on the clean truth (R1 to
R3c), the rule-3 sentence audit, every semantic fork (SF1 to SF20), the rivals and their separation, the golden's
defensible constructions and one sigma, the out-of-sample back-test, and the asks (goldens, devices, stops, coverage,
separation and the distractors)."""
from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS           # noqa: E402
import calc as C            # noqa: E402
import common as K          # noqa: E402
import deliver as DL        # noqa: E402
import docs as DOC          # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
# constructions that combine two choices, or read a pinned sentence another way: asserted to round the same, not
# carried through one sigma
COMBOS = ("one-loan-ever rate, siblings' payoffs ignored", "SF9 exposure one instalment earlier")
MAIN_FILES = [R.F_CURRENT, R.F_LEGACY, R.F_CODES, R.F_MASTER, R.F_REGISTER, DOC.F_POLICY, DOC.F_TERMS, DOC.F_README]
ASK_FILES = [AS.F_CARES, AS.F_EAA, AS.F_CREDITS, AS.F_LEDGER, AS.F_PAYSBA]


class Ck:
    def __init__(self):
        self.n = 0
        self.fails = []

    def __call__(self, label, ok, detail=""):
        self.n += 1
        if not ok:
            self.fails.append("%s: %s" % (label, detail))
            print("FAIL  %s  %s" % (label, detail))
        else:
            print("ok    %s  %s" % (label, detail))

    def done(self):
        print("checks: %d assertions, %d failed" % (self.n, len(self.fails)))
        if self.fails:
            raise SystemExit("checks failed:\n" + "\n".join(self.fails))


def bin_of(x, step):
    return K.round_to(x, step)


def same_call(v, gold, step=1e6):
    return bin_of(v, step) == bin_of(gold, step)


def run(target, golden, Wd=None, G=None, meta_path=None):
    ck = Ck()
    W = Wd.W
    c = G
    P, B, co, hs, hp, hd = c["P"], c["B"], c["co"], c["hs"], c["hp"], c["hd"]
    rk = P.risk
    gold = c["allowance"]
    r = DL.rounded(c)

    # ------------------------------------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path))
    ck("gate files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ck("gate formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(x["rows"] or 0 for x in meta["files"])
    ck("gate 25,000 rows", big >= 25000, "%d rows in the largest file" % big)
    ck("gate distractors", len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]),
       ", ".join(meta["distractor_files"]))
    ck("gate no distractor in a name", not any("distract" in f.lower() for f in files))
    ck("gate deliverables", sorted(os.listdir(golden)) == sorted([DL.GOLD_BOOK, DL.GOLD_NOTE]))

    # ------------------------------------------------------------------------------------------------ realism sweep
    text_files = [f for f in files if f.endswith((".txt", ".csv"))]
    dash = [f for f in text_files if re.search("[\u2013\u2014]", open(os.path.join(target, f), encoding="utf-8").read())]
    ck("realism no em or en dash in text files", not dash, ", ".join(dash))
    from pypdf import PdfReader
    pdf_text = {f: "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(target, f)).pages)
                for f in files if f.endswith(".pdf")}
    ck("realism no em or en dash in the PDFs", not any(re.search("[\u2013\u2014]", t) for t in pdf_text.values()))
    banners = []
    for f in files:
        b = open(os.path.join(target, f), "rb").read()
        if f.endswith((".xlsx", ".docx", ".pdf")) and re.search(rb"ReportLab|openpyxl|python-docx|reportlab", b):
            banners.append(f)
    for f in os.listdir(golden):
        b = open(os.path.join(golden, f), "rb").read()
        if re.search(rb"ReportLab|openpyxl|python-docx|reportlab|Matplotlib", b):
            banners.append(f)
    ck("realism no writer banner in a container", not banners, ", ".join(banners))
    stamps = {int(os.path.getmtime(os.path.join(target, f))) for f in files}
    ck("realism one export stamp", len(stamps) == 1, str(stamps))
    for f in [x for x in files if x.endswith(".csv")]:
        d = pd.read_csv(os.path.join(target, f), dtype=str)
        ck("realism no duplicate row in %s" % f, not d.duplicated().any(), "%d duplicates" % d.duplicated().sum())
    ck("realism the allowance is not round", abs(gold / 1000 - round(gold / 1000)) > 1e-6 or gold % 1000 != 0,
       "%.2f" % gold)
    av = list(c["ask_a"].values())
    ck("realism Ask A quarters distinct", len(set(round(v) for v in av)) == len(av))
    bv = list(c["ask_b"].values())
    ck("realism Ask B cells distinct", len(set(round(v) for v in bv)) == len(bv))
    people = set(K.PEOPLE.values())
    found = set()
    for f, t in pdf_text.items():
        found |= {m for m in people if m in t}
    rd = open(os.path.join(target, DOC.F_README), encoding="utf-8").read()
    ck("realism the policy names only its owner", "Richard Fields" in pdf_text[DOC.F_POLICY] and
       not any(p in pdf_text[DOC.F_POLICY] for p in people - {"Richard Fields"}))

    # ------------------------------------------------------------------------------------------------ R1: raw material
    import pyarrow.parquet as pq
    cols = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            cols += list(pd.read_csv(p, nrows=1).columns)
        elif f.endswith(".parquet"):
            cols += pq.ParquetFile(p).schema.names
    bad = [x for x in cols if re.search(r"group|hazard|\bpd\b|allowance|reserve|probab|cluster|relationship", str(x), re.I)]
    ck("R1 no shipped column holds a group, hazard, probability or allowance", not bad, ", ".join(bad))
    ck("R1 the golden reads loan-month rows and the register", len(rk) > 1_000_000 and len(set(P.gid_of)) < len(P.gid_of),
       "%d loan-months at risk, %d loans in %d guarantor groups" % (len(rk), len(P.gid_of), len(set(P.gid_of))))

    # ------------------------------------------------------------------------------------------------ R3 on the clean truth
    PW = C.panel(W)
    BW = C.book(PW)
    rkw = PW.risk
    hsw = C.rate_table(rkw[rkw.k == 1], "dflt")
    hpw = C.rate_table(rkw, "po")
    hdw = C.rate_table(rkw, "dflt")
    easy = C.loan_level(BW, hdw, hpw, PW.co_share).sum()
    ck("R3a the easy route on the clean truth files the named wrong answer", bin_of(easy, 1e6) == 4e6,
       "default path %.2f million on the clean truth (Ends on: about $4 million)" % (easy / 1e6))
    dec = C.union(BW, hsw, hpw, PW.co_share).sum()
    ck("R3b the decisive step alone files the golden", bin_of(dec, 1e6) == r["allowance"] and abs(dec - gold) < 1.0,
       "%.2f million on the clean truth, %.2f from the pack" % (dec / 1e6, gold / 1e6))
    gk = BW.members.groupby("gid").size()
    BW.pool["k_now"] = BW.pool.gid.map(gk).fillna(1).astype(int)
    lower = {
        "rung 1 latest 12 months": C.loan_level(BW, C.rate_table(rkw[rkw.t > K.T_END - 12], "dflt"),
                                                C.rate_table(rkw[rkw.t > K.T_END - 12], "po"), PW.co_share).sum(),
        "rung 2 own rate times the count": C.loan_level(BW, hsw, hpw, PW.co_share, mult=lambda x: x.k_now).sum(),
        "rung 3 the pool's own union": C.union(BW, hsw, hpw, PW.co_share, pool_only=True).sum(),
    }
    for k_, v in lower.items():
        ck("R3b %s stays wrong on the clean truth" % k_, bin_of(v, 1e6) != r["allowance"], "%.2f million" % (v / 1e6))
    tr = C.truth(W, BW, reps=300)
    ck("R3b the golden is the world's own expectation within its sampling error", abs(dec / tr.sum() - 1) < 0.08,
       "golden %.2f, the world's expected charge-offs %.2f million" % (dec / 1e6, tr.sum() / 1e6))
    ck("R3c no plant: no memo, prior allowance, model output or stakeholder figure ships",
       not any(re.search(r"memo|prior|model|forecast|allowance_20|reserve", f, re.I) for f in files if f != DOC.F_POLICY))
    ck("R2 balances enter only at the reserve date, from the current system", set(B.pool.t) == {K.T_END})

    # ------------------------------------------------------------------------------------------------ rule 3, the sentences
    how = {"prompt": open(os.path.join(TASK, "prompt.txt")).read()}
    for key in ("scope", "estimate", "exposure", "experience", "runoff"):
        for s in DOC.policy_sentences(key):
            how["policy " + s[:3]] = s
    for key in ("crossdefault", "default", "rights"):
        for s in DOC.terms_sentences(key):
            how["terms " + s[:3]] = s
    flat = re.sub(r"\s+", " ", " ".join(pdf_text.values()))
    for k_, s in how.items():
        t = re.sub(r"\s+", " ", s)
        ck("rule3 the sentence is shipped: %s" % k_, k_ == "prompt" or t[:40] in flat)
    words = r"\bunion\b|months on book|hazard|sibling|standing alone|\bgroup of\b|\bits group\b|guarantor group|each member|\bage of\b"
    hits = [k_ for k_, s in how.items() if re.search(words, s, re.I)]
    ck("rule3 no sentence names a hazard, a group's union or a member's age", not hits, ", ".join(hits))
    allt = rd + " ".join(pdf_text.values())
    ck("rule3 no shipped document names the decisive quantity", not re.search(words, allt, re.I))
    ck("rule3 executing the sentences word for word (the loan-level experience) does not give the golden",
       bin_of(c["textbook"], 1e6) != r["allowance"], "the literal estimator files %.2f million" % (c["textbook"] / 1e6))

    # ------------------------------------------------------------------------------------------------ rivals and separation
    gkp = B.members.groupby("gid").size()
    B.pool["k_now"] = B.pool.gid.map(gkp).fillna(1).astype(int)
    kb = lambda k: np.select([k <= 1, k == 2, k == 3, k <= 5], [0, 1, 2, 3], 4)
    rivals = {"R0 textbook (pooled per-loan rates)": c["textbook"]}
    for w in (12, 24, 36):
        lt = rk[rk.t > K.T_END - w]
        hl, pl = C.rate_table(lt, "dflt"), C.rate_table(lt, "po")
        rivals["R1 latest %d months" % w] = C.loan_level(B, hl, pl, co).sum()
        rivals["R2 latest %d months times the count" % w] = C.loan_level(B, hl, pl, co, mult=lambda x: x.k_now).sum()
        rivals["over union at latest %d months' per-loan rates" % w] = C.union(B, hl, pl, co).sum()
    rivals["R1 by term"] = term_rival(P, B, co)
    for w in (None, 24, 60):
        src = rk if w is None else rk[rk.t > K.T_END - w]
        tabs = {b: C.rate_table(src[kb(src.k.values) == b], "dflt") for b in range(5)}
        rivals["R2 group size covariate %s" % (w or "all")] = C.loan_level(
            B, tabs, hp, co, by=lambda x: int(kb(np.array([x.k_now]))[0])).sum()
        tm = {0: C.rate_table(src[src.k <= 1], "dflt"), 1: C.rate_table(src[src.k > 1], "dflt")}
        rivals["R2 multi-unit flag %s" % (w or "all")] = C.loan_level(B, tm, hp, co, by=lambda x: int(x.k_now > 1)).sum()
    rivals["R2 pooled rate times the count"] = C.loan_level(B, hd, hp, co, mult=lambda x: x.k_now).sum()
    rivals["R2 standing-alone rate times the count"] = C.loan_level(B, hs, hp, co, mult=lambda x: x.k_now).sum()
    rivals["R3 the pool's own union"] = C.union(B, hs, hp, co, pool_only=True).sum()
    rivals["R3 the pool's own union at pooled rates"] = C.union(B, hd, hp, co, pool_only=True).sum()
    rivals["over the union at pooled per-loan rates"] = C.union(B, hd, hp, co).sum()
    rivals["R1 covariates (size and industry)"] = covariate_rival(target, P, B, co, hp)
    for k_, v in rivals.items():
        ck("separation %s" % k_, abs(v - gold) >= 1.0e6 and bin_of(v, 1e6) != r["allowance"],
           "%.2f million (golden %.2f)" % (v / 1e6, gold / 1e6))
    c["rivals"] = rivals
    below = max(v for v in rivals.values() if v < gold)
    above = min(v for v in rivals.values() if v > gold)
    ck("separation margins", gold / below >= 1.15 and above / gold >= 1.15,
       "nearest below %.2f (x%.2f), above %.2f (x%.2f)" % (below / 1e6, gold / below, above / 1e6, above / gold))

    # ------------------------------------------------------------------------------------------------ back-test out of sample
    bt = backtest(rk)
    ck("back-test per-loan rates miss loans in groups", bt["ll_group"] >= 2.0, "A/E %.2f" % bt["ll_group"])
    ck("back-test per-loan rates miss loans standing alone", bt["ll_alone"] <= 0.90, "A/E %.2f" % bt["ll_alone"])
    ok = all(abs(np.log(bt["un_" + s])) < abs(np.log(bt["ll_" + s])) for s in ("group", "alone"))
    ck("back-test the union misses less than the per-loan rates on both", ok and 0.85 <= bt["un_group"] <= 1.15 and
       0.85 <= bt["un_alone"] <= 1.15, "A/E %.2f in groups, %.2f standing alone" % (bt["un_group"], bt["un_alone"]))
    ck("back-test group defaults against the union", 0.80 <= bt["glev"] <= 1.30, "A/E %.2f on %d group defaults" % (
        bt["glev"], bt["g_defaults"]))
    c["backtest"] = bt

    # ------------------------------------------------------------------------------------------------ the golden: constructions, bins, sigma
    variants = constructions(target, P, B, co, hs, hp, W)
    c["variants"] = variants
    for k_, v in variants.items():
        ok = bin_of(v["total"], 1e6) == r["allowance"] and all(
            bin_of(v["split"][f], 5e5) == r["split"][f] for f in DL.FYS)
        ck("construction %s rounds the same" % k_, ok, "%.3f million, split %s" % (
            v["total"] / 1e6, ", ".join("%.3f" % (v["split"][f] / 1e6) for f in DL.FYS)))
    sig = sigma(P, B, co, hs, hp)
    c["sigma"] = sig
    ck("sigma measured", sig["total"] > 0, "one sigma %.3f million (%.1f per cent), split %s" % (
        sig["total"] / 1e6, 100 * sig["total"] / gold, ", ".join("%.3f" % (sig["split"][f] / 1e6) for f in DL.FYS)))
    single = [(k_, v) for k_, v in variants.items() if k_ not in COMBOS]
    for k_, v in [("golden", {"total": gold, "split": c["split"]})] + single:
        for sgn in (-1, 1):
            t_ = v["total"] + sgn * sig["total"]
            ok = bin_of(t_, 1e6) == r["allowance"] and all(
                bin_of(v["split"][f] + sgn * sig["split"][f], 5e5) == r["split"][f] for f in DL.FYS)
            ck("one sigma %s %s" % ("up" if sgn > 0 else "down", k_), ok)
    ck("bin clearance of the allowance", K.bin_clearance(gold, 1e6) >= 0.40, "%.3f of a bin" % K.bin_clearance(gold, 1e6))
    for f in DL.FYS:
        ck("bin clearance of FY%d's part" % f, K.bin_clearance(c["split"][f], 5e5) >= 0.35,
           "%.3f of a bin" % K.bin_clearance(c["split"][f], 5e5))
    ck("SF15 the rounded split sums to the rounded allowance", sum(r["split"].values()) == r["allowance"])

    # ------------------------------------------------------------------------------------------------ semantic forks
    sf(ck, target, c, P, B, Wd, pdf_text, rd, variants)

    # ------------------------------------------------------------------------------------------------ the asks
    ask_checks(ck, target, c, Wd)

    # ------------------------------------------------------------------------------------------------ distractors
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(target, f), os.path.join(tmp, f))
        P2 = C.panel_from_pack(tmp)
        B2 = C.book_from_pack(P2)
        g2 = C.union(B2, C.rate_table(P2.risk[P2.risk.k == 1], "dflt"), C.rate_table(P2.risk, "po"), P2.co_share).sum()
        ck("distractors deleted: the golden unchanged", abs(g2 - gold) < 0.01)
        ck("distractors deleted: the asks unchanged", C.ask_a_from_pack(tmp) == c["ask_a"] and
           C.ask_b_from_pack(tmp) == c["ask_b"])
        for f in ASK_FILES:
            os.remove(os.path.join(tmp, f))
        P3 = C.panel_from_pack(tmp)
        B3 = C.book_from_pack(P3)
        g3 = C.union(B3, C.rate_table(P3.risk[P3.risk.k == 1], "dflt"), C.rate_table(P3.risk, "po"), P3.co_share).sum()
        ck("separation line: the call computed with every ask file removed is the golden", abs(g3 - gold) < 0.01)
    finally:
        shutil.rmtree(tmp)
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        for f in files:
            if f not in (R.F_REGISTER, R.F_CURRENT, R.F_LEGACY):
                shutil.copy(os.path.join(target, f), os.path.join(tmp, f))
        ck("separation line: the asks computed with the register and both servicing extracts removed are the asks",
           C.ask_a_from_pack(tmp) == c["ask_a"] and C.ask_b_from_pack(tmp) == c["ask_b"])
    finally:
        shutil.rmtree(tmp)

    # ------------------------------------------------------------------------------------------------ figures.json
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    ck("figures.json carries the call", figs["call"]["allowance_usd"] == r["allowance"])
    ck("figures.json carries the split", all(figs["critical_components"]["split_usd"]["FY%d" % f] == r["split"][f]
                                              for f in DL.FYS))
    write_record(c)
    ck.done()
    return c


def term_rival(P, B, co):
    rk = P.risk
    term = np.where((P.mat_m - P.disb_m) > 100, 1, 0)
    t_r = term[rk.i.values]
    tabs = {t: C.rate_table(rk[t_r == t], "dflt") for t in (0, 1)}
    pz = C.rate_table(rk, "po")
    return C.loan_level(B, tabs, pz, co, by=lambda x: int(term[x.name] if hasattr(x, "name") else 1)).sum()


def covariate_rival(target, P, B, co, hp):
    """Per-loan rates by months on book scaled by a size and industry relative risk fitted on the history."""
    m = C._master(target).set_index("sba_loan_no").loc[P.sba_ids]
    big = (m.loan_amount.astype(float).values > 500000).astype(int)
    hard = m.naics.str[:2].isin(["72", "71", "61", "81"]).astype(int).values
    rk = P.risk
    cell = big[rk.i.values] * 2 + hard[rk.i.values]
    base = C.rate_table(rk, "dflt")
    rel = {}
    for k_ in range(4):
        s = rk[cell == k_]
        exp = base[C.band(s.mob.values)].sum()
        rel[k_] = s.dflt.sum() / exp if exp > 0 else 1.0
    cellp = {i: big[i] * 2 + hard[i] for i in B.pool.index}
    tabs = {k_: base * rel[k_] for k_ in range(4)}
    return C.loan_level(B, tabs, hp, co, by=lambda x: cellp[x.name]).sum()


def backtest(rk, months=24):
    cut = K.T_END - months
    hist = rk[rk.t <= cut]
    h_ll = C.rate_table(hist, "dflt")
    h_bs = C.rate_table(hist[hist.k == 1], "dflt")
    fut = rk[rk.t > cut].copy()
    fut["lq"] = np.log1p(-h_bs[C.band(fut.mob.values)])
    gsum = fut.groupby(["gid", "t"]).lq.sum()
    fu = 1 - np.exp(gsum.reindex(pd.MultiIndex.from_arrays([fut.gid.values, fut.t.values])).values)
    e_ll = h_ll[C.band(fut.mob.values)]
    multi = fut.k.values > 1
    a = fut.dflt.values
    gd = fut.groupby(["gid", "t"]).agg(d=("dflt", "max"), n=("i", "size"), lq=("lq", "sum"))
    big = gd[gd.n > 1]
    return {"glev": float(big.d.sum() / (1 - np.exp(big.lq)).sum()), "g_defaults": int(big.d.sum()),
            "ll_group": a[multi].sum() / e_ll[multi].sum(), "ll_alone": a[~multi].sum() / e_ll[~multi].sum(),
            "un_group": a[multi].sum() / fu[multi].sum(), "un_alone": a[~multi].sum() / fu[~multi].sum(),
            "actual_group": int(a[multi].sum()), "actual_alone": int(a[~multi].sum()),
            "ll_exp_group": float(e_ll[multi].sum()), "ll_exp_alone": float(e_ll[~multi].sum()),
            "un_exp_group": float(fu[multi].sum()), "un_exp_alone": float(fu[~multi].sum())}


def split_of(B, s):
    return {"total": float(s.sum()), "split": {f: float(s[B.pool.fy == f].sum()) for f in DL.FYS}}


def constructions(target, P, B, co, hs, hp, W):
    """Every defensible construction of the golden method, each computed from the pack."""
    rk = P.risk
    out = {}
    out["12-month bands"] = split_of(B, C.union(B, C.rate_table(rk[rk.k == 1], "dflt", 12, 13),
                                                C.rate_table(rk, "po", 12, 13), co, 12, 13))
    out["3-month bands"] = split_of(B, C.union(B, C.rate_table(rk[rk.k == 1], "dflt", 3, 49),
                                               C.rate_table(rk, "po", 3, 49), co, 3, 49))
    size = pd.Series(P.gid_of).value_counts()
    never = rk[pd.Series(P.gid_of[rk.i.values]).map(size).values == 1]
    out["business rate from guarantors with one loan ever"] = split_of(B, C.union(B, C.rate_table(never, "dflt"), hp, co))
    out["siblings' payoffs ignored"] = split_of(B, C.union(B, hs, hp, co, ignore_sib_po=True))
    out["one-loan-ever rate, siblings' payoffs ignored"] = split_of(
        B, C.union(B, C.rate_table(never, "dflt"), hp, co, ignore_sib_po=True))
    # failures identified on the loans that reached 90 days themselves (slow failures) scaled by the share of
    # group defaults the history shows starting that way is not identifiable; the group-level fit is:
    out["group-level fit of the failure rate"] = split_of(B, C.union(B, group_fit(P), hp, co))
    # charge-off share bases
    rs = P.resol[P.resol.res != "open"]
    gid = P.gid_of[rs.i.values]
    by_group = rs.assign(g=gid).groupby(["g", "t"]).res.first()
    co_g = float((by_group == "co").mean())
    out["charge-off share by groups"] = split_of(B, C.union(B, hs, hp, co_g))
    bal_at = P.df.set_index(["i", "t"]).bal
    w = bal_at.reindex(pd.MultiIndex.from_arrays([rs.i.values, rs.t.values])).values
    co_d = float(np.nansum(w * (rs.res.values == "co")) / np.nansum(w))
    out["charge-off share by dollars"] = split_of(B, C.union(B, hs, hp, co_d))
    # SF9: the exposure at the balance of the last instalment paid (one month earlier)
    out["SF9 exposure one instalment earlier"] = split_of(B, union_shift(B, hs, hp, co))
    # SF13: the Section 1112 months taken out of the risk sets by the agent's instalment months
    out["SF13 Section 1112 months out of the risk sets"] = split_of(B, union_wo_1112(target, P, B, co, hp))
    # Layer 1: the legacy extract dropped, and the parallel month counted twice
    out["R2 history from October 2017 only"] = split_of(B, union_from(P, B, co, t0=96))
    out["R2 the parallel-run month counted twice"] = split_of(B, union_dup(P, B, co))
    # delinquency at the reserve date: loans 30 or 60 days past due at their roll rates
    out["delinquency at the reserve date at roll rates"] = split_of(B, union_dq(P, B, co, hs, hp))
    return out


def group_fit(P, iters=60):
    """The failure rate by band fitted on every group-month by EM: a group defaults in a month when any of its loans at
    risk fails, each at the rate of its own band; a defaulted group-month's failure is shared among its loans in
    proportion to their rates."""
    rk = P.risk
    b = C.band(rk.mob.values)
    key = pd.MultiIndex.from_arrays([rk.gid.values, rk.t.values])
    codes, uniq = pd.factorize(key)
    d = np.bincount(codes, weights=rk.dflt.values.astype(float), minlength=len(uniq)) > 0
    den = np.bincount(b, minlength=C.NB).astype(float)
    h = C.rate_table(rk[rk.k == 1], "dflt").copy()
    for _ in range(iters):
        lq = np.log1p(-h[b])
        pdef = 1 - np.exp(np.bincount(codes, weights=lq, minlength=len(uniq)))
        e = np.where(d[codes], h[b] / np.maximum(pdef[codes], 1e-12), 0.0)
        new = np.bincount(b, weights=e, minlength=C.NB) / np.maximum(den, 1)
        new = np.where(den > 0, new, h)
        if np.max(np.abs(new - h)) < 1e-10:
            h = new
            break
        h = new
    return h


def union_shift(B, hs, hp, co):
    return C.union(B, hs, hp, co, ead_shift=True)


def union_from(P, B, co, t0):
    rk = P.risk[P.risk.t >= t0]
    return C.union(B, C.rate_table(rk[rk.k == 1], "dflt"), C.rate_table(rk, "po"), co)


def union_dup(P, B, co):
    rk = P.risk
    extra = rk[rk.t == 96]
    rk2 = pd.concat([rk, extra], ignore_index=True)
    return C.union(B, C.rate_table(rk2[rk2.k == 1], "dflt"), C.rate_table(rk2, "po"), co)


def union_wo_1112(target, P, B, co, hp):
    x = C.ask_a_lines(target)
    paid = set(zip(x.sba.values, x.m_due.values))
    sba = np.array(P.sba_ids, dtype=object)
    rk = P.risk
    mask = np.array([(s, t) not in paid for s, t in zip(sba[rk.i.values], rk.t.values)])
    rk2 = rk[mask]
    return C.union(B, C.rate_table(rk2[rk2.k == 1], "dflt"), C.rate_table(rk2, "po"), co)


def union_dq(P, B, co, hs, hp):
    df = P.df
    nx = df.groupby("i")["code"].shift(-1)
    nx2 = df.groupby("i")["code"].shift(-2)
    roll = {}
    for cd in (2, 3):
        m = (df.code == cd) & (df.t < K.T_END - 2)
        roll[cd] = float((nx[m].isin([4, 5]) | nx2[m].isin([4, 5])).mean())
    s = C.union(B, hs, hp, co).copy()
    mem = B.members
    dq = mem[mem.code.isin([2, 3])]
    for g, d in dq.groupby("gid"):
        pg = 1 - np.prod([1 - roll[int(cd)] for cd in d.code.values])
        for i in B.pool.index[(B.pool.gid == g) & B.pool.perf]:
            s[i] = pg * co * B.pool.at[i, "bal"] * B.pool.at[i, "ug"] + (1 - pg) * s[i]
    return s


def sigma(P, B, co, hs, hp, reps=24):
    """One sigma of the allowance and its split: loans standing alone resampled for the failure rate, defaulted groups
    resampled for the charge-off share."""
    rg = K.rng("sigma")
    rk = P.risk
    si = rk[rk.k == 1]
    ids = si.i.unique()
    rs = P.resol[P.resol.res != "open"].assign(g=lambda d: P.gid_of[d.i.values])
    gr = rs.groupby("g").agg(co=("res", lambda x: (x == "co").sum()), n=("res", "size"))
    tots, splits = [], {f: [] for f in DL.FYS}
    for b_ in range(reps):
        pick = rg.choice(ids, len(ids), replace=True)
        cnt = pd.Series(pick).value_counts()
        s2 = si[si.i.isin(cnt.index)]
        w = s2.i.map(cnt).values
        gg = pd.DataFrame({"b": C.band(s2.mob.values), "e": s2.dflt.values * w, "n": w}).groupby("b").sum()
        hb = (gg.e / gg.n).reindex(range(C.NB)).ffill().fillna(0).values
        pk = rg.choice(len(gr), len(gr), replace=True)
        cob = gr.co.values[pk].sum() / gr.n.values[pk].sum()
        s = C.union(B, hb, hp, cob)
        tots.append(s.sum())
        for f in DL.FYS:
            splits[f].append(s[B.pool.fy == f].sum())
    return {"total": float(np.std(tots)), "split": {f: float(np.std(splits[f])) for f in DL.FYS}, "reps": reps}


def sf(ck, target, c, P, B, Wd, pdf_text, rd, variants):
    W = Wd.W
    pol = " ".join(DOC.policy_sentences())
    terms = " ".join(DOC.terms_sentences())
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    pool = B.pool
    gold = c["allowance"]
    r = DL.rounded(c)
    m = C._master(target).set_index("sba_loan_no")
    ck("SF1 the allowance is lifetime: policy 2.1", "over each loan's remaining contractual term" in pol and "as the allowance" in prompt)
    ck("SF2 unguaranteed portions from the guaranty share", "unguaranteed portions" in prompt and
       np.allclose(pool.ug.values, 1 - m.loc[[P.sba_ids[i] for i in pool.index], "guaranty_pct"].astype(float).values / 100))
    ad = pd.to_datetime(m.loc[[P.sba_ids[i] for i in pool.index], "approval_date"])
    ck("SF3 the pool by SBA approval date, 1 October 2018 to 30 September 2021 (policy 1.2)",
       "from 1 October 2018 to 30 September 2021" in pol and ad.min() >= pd.Timestamp("2018-10-01") and
       ad.max() <= pd.Timestamp("2021-09-30"))
    nd = pd.to_datetime(m.first_disbursement_date)
    nd_fy = np.where(nd.dt.month >= 10, nd.dt.year + 1, nd.dt.year)
    ck("SF3 the disbursement-date reading selects another set (ruled out by 1.2)", int((nd_fy != m.fy).sum()) > 0,
       "%d loans change fiscal year" % int((nd_fy != m.fy).sum()))
    last = P.last
    closed_sep = last[(last.t == K.T_END) & last.code.isin((7, 8, 9))]
    ck("SF4 loans closed in September 2026 are off the books", not set(closed_sep.index) & set(pool.index),
       "%d loans closed that month" % len(closed_sep))
    ck("SF5 loans in default carried at the charge-off share (policy 2.1)", "loans in default not yet charged off included" in pol
       and int((~pool.perf).sum()) == sum(c["in_default"].values()))
    ck("SF6 recoveries not included (policy 2.1)", "Expected recoveries are not included" in pol)
    ck("SF7 the note rate at the reserve date (policy 3.1)", "note rate in effect at the reserve date" in pol and
       pool.rate.notna().all())
    ck("SF8 the bank's own experience from October 2009 (policy 4.1)", "from October 2009" in pol and
       P.df.t.min() == 0)
    v9 = variants["SF9 exposure one instalment earlier"]
    ck("SF9 the exposure reading is the same call", same_call(v9["total"], gold), "%.3f million" % (v9["total"] / 1e6))
    ck("SF10 default at 90 days or accelerated (policy 2.2)", "90 or more days past due or has been accelerated" in pol)
    nopo = C.union(B, c["hs"], np.zeros_like(c["hp"]), c["co"]).sum()
    ck("SF11 prepayments in the term (policy 2.1); the reading without them is ruled out", "adjusted for expected prepayments"
       in pol and not same_call(nopo, gold), "%.3f million without prepayments" % (nopo / 1e6))
    ck("SF12 loans made later are not projected (policy 5.1)", "Loans the bank may make after that date are not projected" in pol)
    v13 = variants["SF13 Section 1112 months out of the risk sets"]
    ck("SF13 the Section 1112 months are the same call", same_call(v13["total"], gold), "%.3f million" % (v13["total"] / 1e6))
    ck("SF14 book means the allowance balance", "book at 30 September 2026 as the allowance" in prompt)
    ck("SF15 rounding once (asserted above with the split)", sum(r["split"].values()) == r["allowance"])
    # SF16: every key that keeps surname with the TIN gives the same groups as the party number
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, R.F_REGISTER), read_only=True)
    rows = list(wb["Guaranties"].iter_rows(values_only=True))
    reg = pd.DataFrame(rows[1:], columns=rows[0])
    by_party = C.groups_from_register(reg)
    by_name = C.groups_from_register(reg, key=C.guarantor_key)

    def full_key(name, kind, tin):
        s = re.sub(r"[.,]", " ", str(name)).upper().split()
        s = [w for w in s if w not in C.SUFFIX and w not in ("LLC", "L", "C")]
        s = [w for w in s if len(w) > 1]
        return (kind, " ".join(s), str(tin))
    by_full = C.groups_from_register(reg, key=full_key)

    def partition(gm):
        d = {}
        for k_, v in gm.items():
            d.setdefault(v, set()).add(k_)
        return sorted(tuple(sorted(x)) for x in d.values())
    pp = partition(by_party)
    ck("SF16 groups by surname and TIN equal groups by party number", partition(by_name) == pp)
    ck("SF16 groups by name without initials and TIN equal groups by party number", partition(by_full) == pp)
    world_groups = {}
    sba_of = {}
    for i in range(W.n):
        if W.status[i] != 0:
            world_groups.setdefault(int(W.gid[i]), set()).add(i)
    I = Wd.I
    wp = sorted(tuple(sorted(I.sba[i] for i in s)) for s in world_groups.values())
    ck("SF16 the register's groups are the world's guarantor groups", wp == pp, "%d groups" % len(pp))
    ck("SF17 the cross-default's reach is the group (no guarantor bridges two groups)", wp == pp and
       "guaranteed by a Guarantor of this Loan" in terms)
    for k_ in ("charge-off share by groups", "charge-off share by dollars"):
        ck("SF18 %s is the same call" % k_, same_call(variants[k_]["total"], gold), "%.3f million" % (variants[k_]["total"] / 1e6))
    allr = P.resol
    co_o = float((allr.res == "co").sum() / len(allr))
    v_o = C.union(B, c["hs"], c["hp"], co_o).sum()
    open_liq = int((allr.res == "open").sum())
    ck("SF18 open defaults counted as not charged off is ruled out (policy 2.3: still in liquidation, not brought current "
       "or paid)", "unless the loan has been brought current or paid" in pol and open_liq > 0,
       "%d open defaults; that reading files %.3f million" % (open_liq, v_o / 1e6))
    ck("SF19 SBA's fiscal year is the bank's", "SBA's fiscal year is the same" in rd)
    perf_only = float((pool.bal * pool.ug)[pool.perf].sum())
    ck("SF20 the chart's unguaranteed principal includes loans in default (policy 2.1)",
       abs(sum(c["ugp"].values()) - float((pool.bal * pool.ug).sum())) < 1 and perf_only < sum(c["ugp"].values()))


def ask_checks(ck, target, c, Wd):
    A, B_ = Wd.A, Wd.B
    W = Wd.W
    gold_a, gold_b = c["ask_a"], c["ask_b"]
    qa, nb = AS.ask_goldens(W, A, B_)
    ck("Ask A golden equals the world's payments, every quarter", all(abs(qa[k] - gold_a[k]) < 0.01 for k in qa))
    ck("Ask B golden equals the world's net charge-offs, every cell", all(abs(nb[k] - gold_b[k]) < 0.01 for k in nb))
    pool = lambda i: K.POOL_FY[0] <= W.fy[i] <= K.POOL_FY[1]
    cu = {}
    for i, rd_, tr, months, tot, prog in A.disb:
        if pool(i) and len(months) > 1:
            for mm in months:
                if AS.ASK_A_FIRST <= mm <= AS.ASK_A_LAST:
                    cu[K.fq_label(mm)] = cu.get(K.fq_label(mm), 0) + 1
    ck("A1 catch-ups in every quarter", all(cu.get(k, 0) > 0 for k in gold_a), str(cu))
    stops_a = {}
    for how in ("lines", "remit", "first", "cents"):
        v = C.ask_a_from_pack(target, how=how)
        off = [k for k in gold_a if abs(K.round_to(v[k], 1000) - K.round_to(gold_a[k], 1000)) > 0]
        stops_a[how] = (len(off), min(abs(v[k] - gold_a[k]) for k in gold_a))
        ck("Ask A stop %s misses" % how, len(off) >= (4 if how == "cents" else 7) or (how == "first" and len(off) >= 5),
           "%d of 7 off, nearest %.0f" % stops_a[how])
    lines = C.ask_a_from_pack(target, how="lines")
    ck("Ask A the cracker (lines summed by the instalment's quarter) misses every quarter",
       all(K.round_to(lines[k], 1000) != K.round_to(gold_a[k], 1000) for k in gold_a))
    cov = {k: [0, 0, 0] for k in nb}
    old = AS.old_module(B_)
    for i, d, gross, bank, sba, kind in B_.receipts:
        k = (K.fy_of_date(d), int(W.fy[i]))
        if pool(i) and k in cov:
            cov[k][0 if i in old else 1] += 1
    for i, d, amt in B_.top:
        k = (K.fy_of_date(d), int(W.fy[i]))
        if pool(i) and k in cov:
            cov[k][2] += 1
    ck("B1 receipts from both modules in every cell", all(v[0] > 0 and v[1] > 0 for v in cov.values()), str(cov))
    ck("B2 Treasury offset shares in every cell", all(v[2] > 0 for v in cov.values()))
    stops_b = {}
    for how in ("ledger", "netall", "notop", "bydate"):
        v = C.ask_b_from_pack(target, how=how)
        off = [k for k in gold_b if K.round_to(v[k], 1000) != K.round_to(gold_b[k], 1000)]
        stops_b[how] = (len(off), min(abs(v[k] - gold_b[k]) for k in gold_b))
        ck("Ask B stop %s misses every cell" % how, len(off) == 12, "%d of 12 off, nearest %.0f" % stops_b[how])
    # the over-correction with the offsets found
    v = C.ask_b_from_pack(target, how="netall")
    ck("Ask B the cracker (offsets missed) misses every cell",
       all(K.round_to(C.ask_b_from_pack(target, how="notop")[k], 1000) != K.round_to(gold_b[k], 1000) for k in gold_b))
    c["stops_a"], c["stops_b"] = stops_a, stops_b
    # no filed sentence adjudicates a device: the documents never mention the agent's line amounts, the module or SBA's share
    txt = open(os.path.join(target, DOC.F_README), encoding="utf-8").read() + " ".join(DOC.policy_sentences()) + " ".join(
        DOC.terms_sentences())
    ck("ban 1 no shipped sentence narrates a device", not re.search(r"catch-up|disbursement total|module|bank's share|"
                                                                     r"gross|pro rata|Treasury offset", txt, re.I))
    ck("separation the main call's files carry no ask row", all(f not in MAIN_FILES for f in ASK_FILES))


def write_record(c):
    """The measured values the design note and the write-up quote, kept beside figures.json."""
    rec = {"allowance": c["allowance"], "split": c["split"], "textbook": c["textbook"],
           "rivals": {k: v for k, v in c["rivals"].items()},
           "variants": {k: v["total"] for k, v in c["variants"].items()},
           "sigma": c["sigma"]["total"], "sigma_split": c["sigma"]["split"], "backtest": c["backtest"],
           "stops_a": c["stops_a"], "stops_b": {k: list(v) for k, v in c["stops_b"].items()}}
    with open(os.path.join(HERE, "measured.json"), "w") as fh:
        json.dump(rec, fh, indent=1, default=float)
        fh.write("\n")
