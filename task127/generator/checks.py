"""task127's generator checks: the input gates, the ladder (every rung against the booked figure, the restatement's
variants converging on the carried figure), the three rules executed on the clean truth, every semantic fork row
(SF1 to SF13), both asks' goldens against the world and their stops, the separation line, the goldens against
figures.json, and the realism sweep."""
from __future__ import annotations

import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd

import analysis as A
import common as K
import load as L
import records as R
import world as W

BIN = 25e6


class Checks:
    def __init__(self):
        self.n = 0

    def __call__(self, label, cond, detail=""):
        if not cond:
            raise AssertionError("%s: %s" % (label, detail))
        self.n += 1


def carry(x):
    return A.round_to(x, BIN)


def bin_margin(x):
    """distance from a figure to the nearest edge of its $25 million rounding bin"""
    v = x / BIN
    return abs((v % 1) - 0.5) * BIN


# ------------------------------------------------------------------ the clean truth (stumping 1.1, dataset-generation 7.1)

def clean_triangles(feats):
    """The book straight from the world: every real feature, its true closing history and every payment and void at
    its true moment, with none of the two systems' recording."""
    real = [f for f in feats if f.kind != "dup"]
    starts = np.array([K.day(K.quarter_start(k)) for k in range(A.NQ + 1)])

    def q_of(t):
        return int(np.searchsorted(starts, t, side="right") - 1)
    pay_aq, pay_tq, pay_amt = [], [], []
    rep_aq, rep_tq = [], []
    tr_aq, tr_tq, tr_d = [], [], []
    for f in real:
        for p in f.pays:
            pay_aq.append(f.aq); pay_tq.append(q_of(p[0])); pay_amt.append(p[1])
            if p[4] is not None:
                pay_aq.append(f.aq); pay_tq.append(q_of(p[4])); pay_amt.append(-p[1])
        rep_aq.append(f.aq); rep_tq.append(q_of(f.rep))
        for close, disp, reopen in f.closings:
            tr_aq.append(f.aq); tr_tq.append(q_of(max(close, f.created))); tr_d.append(1.0)
            if reopen is not None:
                tr_aq.append(f.aq); tr_tq.append(q_of(reopen)); tr_d.append(-1.0)
    P = A._cum(np.array(pay_aq), np.array(pay_tq), np.array(pay_amt))
    Rr = A._cum(np.array(rep_aq), np.array(rep_tq), np.ones(len(rep_aq)))
    C = A._cum(np.array(tr_aq), np.array(tr_tq), np.array(tr_d))
    return P, C, Rr


def truth_unpaid(feats):
    """What the book will still pay after the valuation, on every real feature from accidents to 31 December 2026."""
    tot = 0.0
    for f in feats:
        if f.kind == "dup":
            continue
        tot += sum(p[1] for p in f.pays if p[0] >= W.VAL)
        tot -= sum(p[1] for p in f.pays if p[4] is not None and p[4] >= W.VAL and p[0] < W.VAL)
    return tot


# ------------------------------------------------------------------ Ask A from the world

def world_counts(feats):
    out = {y: dict(with_payment=0, without_payment=0) for y in range(2017, 2027)}
    for f in feats:
        if f.kind == "dup" or f.rep >= W.VAL:
            continue
        if W._open_at(f, W.VAL) or f.created >= W.VAL:
            continue
        paid = sum(p[1] for p in f.pays if p[0] < W.VAL) - sum(p[1] for p in f.pays
                                                                if p[4] is not None and p[4] < W.VAL)
        y = 2017 + f.aq // 4
        out[y]["with_payment" if paid > 0.005 else "without_payment"] += 1
    return out


def ask_a_stops(target, b):
    """The ask's stops: the disposition read as the payment, the platform's payments alone, every voided check netted
    whenever it was voided, the re-entered legacy features counted twice, the duplicates' payments dropped."""
    lc, pf, ev, pp, lp = b["lc"], b["pf"], b["ev"], b["pp"], b["lp"]
    net = b["trans"][b["trans"].tq < A.NQ].groupby("key").d.sum()
    f = b["feats"][(b["feats"].rq < A.NQ)]
    closed = f.key.map(net).fillna(0) > 0
    ay = 2017 + f.aq.to_numpy() // 4
    stops = {}
    # disposition: legacy ST and platform SETTLED as with a payment
    disp = dict(zip(lc.key, lc.DISP))
    disp.update(dict(zip(pf.feature_id, pf.disposition)))
    for k, ref in zip(pf.feature_id, pf.legacy_ref):
        if ref in b["re_keys"]:
            disp[ref] = pf.disposition[pf.feature_id == k].iloc[0]
    paid_by_disp = f.key.map(lambda k: disp.get(k, "") in ("ST", "SETTLED"))
    stops["disposition"] = _cells(ay, closed, paid_by_disp)
    # platform payments only for platform features, legacy only for legacy ones
    fp = A.feature_payments(b)
    plat_only = b["pays"][(b["pays"].sys == "platform") & (b["pays"].tq < A.NQ)].groupby("fid").amount.sum()
    leg_only = b["pays"][(b["pays"].sys == "legacy") & (b["pays"].tq < A.NQ)].groupby("fid").amount.sum()
    po = f.apply(lambda r: (plat_only.get(r.key, 0.0) if r.sys == "platform" else leg_only.get(r.key, 0.0)), axis=1)
    stops["one_ledger"] = _cells(ay, closed, po > 0.005)
    # every voided check netted, January voids included
    pays = b["pays"].copy()
    pays_all = pays[pays.tq < A.NQ].copy()
    pv = pp[pp.voided.notna() & (pp.voided >= pd.Timestamp(K.VAL))]
    extra = pd.Series(-pv.amount.to_numpy(), index=pv.feature_id.to_numpy()).groupby(level=0).sum()
    key_of = {}
    for fid, ref in zip(pf.feature_id, pf.legacy_ref):
        if ref and ref in b["re_keys"]:
            key_of[fid] = ref
    extra.index = [key_of.get(i, i) for i in extra.index]
    extra = extra.groupby(level=0).sum()
    vn = f.key.map(fp).fillna(0.0) + f.key.map(extra).fillna(0.0)
    stops["voids_netted"] = _cells(ay, closed, vn > 0.005)
    # payments on duplicate features dropped with the duplicates
    dups = set(pf.feature_id[pf.disposition == "DUPLICATE"]) | set(lc.key[lc.DISP == "XD"])
    pays2 = pays_all[~pays_all.fid.isin(dups)]
    key2 = pays2.fid.map(lambda x: {r: k for k, r in []}.get(x, x))
    fp2 = A.feature_payments({**b, "pays": pays2})
    stops["dup_payments_dropped"] = _cells(ay, closed, f.key.map(fp2).fillna(0.0) > 0.005)
    return stops


def _cells(ay, closed, paid):
    paid = np.asarray(paid, bool)
    closed = np.asarray(closed, bool)
    return {y: dict(with_payment=int(((ay == y) & closed & paid).sum()),
                    without_payment=int(((ay == y) & closed & ~paid).sum())) for y in range(2017, 2027)}


def recreated_doubled(b):
    """Ask A with each re-entered legacy feature counted twice: its closed archive row and its platform row."""
    lc = b["lc"]
    rows = lc[lc.key.isin(b["re_keys"])]
    fp = A.feature_payments(b)
    base = A.counts_by_year(b)
    out = {y: dict(v) for y, v in base.items()}
    leg = b["pays"][(b["pays"].sys == "legacy") & b["pays"].fid.isin(b["re_keys"])].groupby("fid").amount.sum()
    for k, acc in zip(rows.key, rows.acc):
        y = acc.year
        out[y]["with_payment" if leg.get(k, 0.0) > 0.005 else "without_payment"] += 1
    return out


def diff_cells(a, b_):
    return sum(1 for y in range(2017, 2027) for k in ("with_payment", "without_payment") if a[y][k] != b_[y][k])


# ------------------------------------------------------------------ Ask B from the world

def world_ledger(gl_lines, pays):
    """Each 2026 ledger line by what the generator put in it."""
    out = {}
    by_id = {}
    for r in pays:
        by_id[id(r)] = r
    for q in range(4):
        lo = dt.date(2026, 3 * q + 1, 1)
        hi = dt.date(2026, 3 * q + 4, 1) if q < 3 else dt.date(2027, 1, 1)
        earlier = other = 0
        for l in gl_lines:
            if not (lo <= l["posting_date"] < hi):
                continue
            if l["_kind"] == "feed":
                if l["_cover"] < lo:
                    earlier += l["cents"]
            elif l["_kind"] == "repost":
                if l["_cover"] < lo:
                    earlier += l["cents"]
            elif l["_kind"] == "wire":
                y, m = l["_cover"]
                st = l["state"]
                for r in pays:
                    if r["method"] != "WIRE" or r["_f"].state != st:
                        continue
                    v = R.value_date(r["issued"])
                    if (v.year, v.month) == (y, m) and K.at(r["issued"]).date() < lo:
                        earlier += r["cents"]
                other += l.get("_pd", 0)
            else:
                other += l["cents"]
        out[q + 1] = dict(earlier=round(earlier / 100.0, 2), other=round(other / 100.0, 2))
    return out


# ------------------------------------------------------------------ the run

def run(target, golden, st, meta_path):
    ck = Checks()
    fig = st["fig"]["figures"]
    m = st["fig"]["m"]
    b = m["b"]
    feats = st["feats"]
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- input gates
    ck("gate: 10 or more files", len(files) >= 10, files)
    ck("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ck("gate: a file of 25,000 rows or more", big >= 25000, big)
    meta = json.load(open(meta_path))
    ck("gate: two distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and
       all(d in files for d in meta["distractor_files"]))
    ck("gate: no file name says distractor", not any("distract" in f.lower() for f in files))
    ck("gate: every file accounted for", set(files) == set(meta["call_files"]) | set(meta["ask_files"]) |
       set(meta["distractor_files"]), set(files) ^ (set(meta["call_files"]) | set(meta["ask_files"]) |
                                                    set(meta["distractor_files"])))

    # ---------------------------------------------------------------- the call and the ladder
    booked = m["booked"]
    ind = float(m["bs"].sum())
    ck("booked figure read from the register", abs(booked - K.BOOKED) < 1.0, booked)
    ck("carried figure", fig["carried_musd"] == 400.0, fig["carried_musd"])
    ck("indicated mid-bin (at least $5 million from a $25 million edge)", bin_margin(ind) >= 5e6, bin_margin(ind))
    variants = {k: float(m[k].sum()) for k in ("bs", "bs_exp", "bs_rep", "bs_exp_rep", "bs_simple", "bs_last12")}
    for k, v in variants.items():
        ck("C1: the restatement variant %s carries the golden" % k, carry(v) == carry(ind), (k, v / 1e6))
        ck("separation: %s at least 1.06 above the booked figure" % k, v / booked >= 1.06, (k, v / booked))
    unrestated = {"chain_ladder": float(m["cl"].sum()), "latest_4": float(m["cl_last4"].sum()),
                  "latest_8": float(m["cl_last8"].sum()), "latest_12": float(m["cl_last12"].sum()),
                  "annual_chain_ladder": A.annual(b, restated=False)}
    for k, v in unrestated.items():
        ck("R0/R1: %s at least 1.06 below the booked figure" % k, booked / v >= 1.06, (k, v / 1e6))
        ck("R0/R1: %s carries a release" % k, carry(v) < booked, (k, carry(v)))
    act, exp = A.actual_vs_expected(m["P"])
    ck("R1a: the latest year's payments come in below the chain ladder's expectation", act / exp < 1.0, act / exp)
    fs_naive, fs_trend, trend = A.frequency_severity(b, m["n_ult"], m["P"])
    ck("R2: open features at the closed average lands far below", fs_naive < 0.5 * booked, fs_naive)
    ck("R2: the trended frequency-severity reading is recorded", 0.8 * booked < fs_trend < ind, fs_trend)
    ck("default path ends on a release", carry(unrestated["chain_ladder"]) < booked, unrestated["chain_ladder"])
    st["default_carry"] = carry(unrestated["chain_ladder"])
    D = m["D"]
    below = tot = 0
    for j in range(6, 23):
        pre = [D[i, j] for i in range(A.NQ) if i + j <= 29 and i >= 4]
        post = [D[i, j] for i in range(A.NQ) if i + j >= 31 and not np.isnan(D[i, j])]
        ck("closure: post-cutover mean below the history at age %d" % (j + 1), np.mean(post) < np.mean(pre),
           (j + 1, np.mean(post), np.mean(pre)))
        below += sum(p < min(pre) for p in post)
        tot += len(post)
    ck("closure: most post-cutover cells below the history's lowest", below / tot > 0.6, (below, tot))
    ck("closure rows in figures", fig["closed_share_8q_latest_pct"] < fig["closed_share_8q_history_pct"] and
       fig["closed_share_12q_latest_pct"] < fig["closed_share_12q_history_pct"])

    # ---------------------------------------------------------------- the three rules on the clean truth
    P0, C0, R0 = clean_triangles(feats)
    cl0 = float(A.chain_ladder(P0).sum())
    n0 = A.ultimate_counts(R0)
    rs0 = A.restate(P0, C0 / n0[:, None])
    lat0 = A.latest(P0)
    bs0 = float((A.project(A.factors(rs0), lat0) - lat0).sum())
    truth = truth_unpaid(feats)
    ck("analyst test: the easy route on the clean truth files a release", carry(cl0) < booked, cl0)
    ck("analyst test: the restatement on the clean truth carries the golden", carry(bs0) == carry(ind), bs0)
    ck("the golden sits nearer the book's true unpaid than the chain ladder", abs(ind - truth) < abs(cl0 - truth),
       (ind, cl0, truth))
    ck("the true unpaid is a strengthening", truth > booked * 1.06, truth)

    # ---------------------------------------------------------------- semantic forks
    lp = b["lp"]
    pp = b["pp"]
    ck("SF1: no adjusting expense in the pack", set(lp.PAYEE_TYPE) <= {"CLMT", "ATTY", "LIEN"} and
       set(pp.payee_type) <= {"CLAIMANT", "ATTORNEY", "LIENHOLDER"})
    late = sum(sum(p[1] for p in f.pays if p[0] >= W.VAL) for f in feats if f.kind != "dup" and f.rep >= W.VAL)
    ck("SF2: unreported features under 1 per cent of the unpaid", late / truth < 0.01, late / truth)
    texts = {f: open(os.path.join(target, f), encoding="utf-8", errors="replace").read()
             for f in files if f.endswith((".md", ".txt", ".csv"))}
    ck("SF3/SF4: no ceded data or discount rate shipped", not any(re.search(r"\bceded\b|discount rate", t, re.I)
                                                                  for t in texts.values()))
    utc = utc_restated(target)
    ck("SF5: platform events on UTC dates carry the golden", carry(utc) == carry(ind), utc)
    basis_text = open(os.path.join(target, K.F["basis"]), "rb").read()
    ck("SF6: annual development is ruled out by the basis's quarter-end ages", A.annual(b) > booked * 1.06 and
       carry(A.annual(b, restated=False)) < booked)
    def age_of(f, t):
        d = K.at(t)
        return (d.year - 2017) * 4 + (d.month - 1) // 3 - f.aq + 1
    longest = max(age_of(f, c[0]) for f in feats if f.kind != "dup" for c in f.closings)
    ck("SF7: every feature settles by age 40", longest <= 40, longest)
    claims = claims_restated(b)
    ck("SF8: claims instead of claimant features carry the golden", carry(claims) == carry(ind), claims)
    gross = gross_restated(b)
    ck("SF9: voids left gross carry the golden", carry(gross) == carry(ind), gross)
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(target, K.F["register"]), data_only=True).active
    bi = [r for r in ws.iter_rows(min_row=5, values_only=True) if r[1] == "Bodily injury"]
    ck("SF10: the register's bodily injury lines are labelled loss and expense", sorted(r[2] for r in bi) ==
       ["Adjusting and other", "Defence and cost containment", "Loss"])
    codes = open(os.path.join(target, K.F["codes"]), encoding="ascii").read()
    ck("SF11: the code list says a converted feature continues on the platform", "CONTINUES ON PLATFORM" in codes)
    latest_close = latest_close_restated(b)
    ck("SF12: closings read from the latest close alone carry the golden", carry(latest_close) == carry(ind),
       latest_close)
    ck("SF13: the accident quarters' rounded sum carries the golden",
       carry(sum(round(x, -6) for x in m["bs"])) == carry(ind))

    # ---------------------------------------------------------------- Ask A
    wc = world_counts(feats)
    gc = A.counts_by_year(b)
    gc2 = {y: {k: v[k] for k in ("with_payment", "without_payment")} for y, v in gc.items()}
    ck("Ask A: the golden equals the world's counts", gc2 == wc, (gc2, wc))
    stops = ask_a_stops(target, b)
    stops["recreated_doubled"] = recreated_doubled(b)
    for name, s in stops.items():
        n = diff_cells(s, gc2)
        ck("Ask A stop %s misses cells" % name, n >= 4, (name, n))
    cracker = cracker_counts(b)
    missed = diff_cells(cracker, gc2)
    st["ask_a_cracker_missed"] = missed
    ck("Ask A: the cracker's path misses at least 16 of 20 cells", missed >= 16, missed)

    # ---------------------------------------------------------------- Ask B
    wl = world_ledger(st["gl"], st["pays"])
    gl = A.ledger_quarters(target)
    for q in range(1, 5):
        ck("Ask B Q%d: earlier-quarter payments equal the world's" % q, abs(gl[q]["earlier"] - wl[q]["earlier"]) < 0.01,
           (gl[q], wl[q]))
        ck("Ask B Q%d: other entries equal the world's" % q, abs(gl[q]["other"] - wl[q]["other"]) < 0.01,
           (gl[q], wl[q]))
    for c in (13, 14, 16, 17):
        alt = A.ledger_quarters(target, cutoff_hour=c)
        res = A.ledger_lines(target, cutoff_hour=c)
        extra = res[res.kind == "unmatched"].amount.abs().sum() - R.PD_WIRE
        ck("Ask B: a %d:00 cutoff gives the golden or leaves a journal unreconciled" % c,
           alt == gl or extra > 0.5, (c, alt, extra))
    lines = A.ledger_lines(target)
    unmatched = lines[lines.kind == "unmatched"]
    ck("Ask B: under the 15:00 cutoff only the property damage wire fails to reconcile",
       len(unmatched) == 1 and abs(unmatched.amount.iloc[0] - R.PD_WIRE) < 0.005, unmatched)
    face = face_value_ledger(target)
    st["ask_b_face_missed"] = sum(1 for q in range(1, 5) for k in ("earlier", "other") if abs(face[q][k] - gl[q][k]) > 0.5)
    ck("Ask B: reading each Treasury journal as its posting month's previous month misses most cells",
       st["ask_b_face_missed"] >= 6, (face, gl))

    # ---------------------------------------------------------------- separation line: ask devices never move the call
    for name, v in separation_variants(b).items():
        ck("separation: %s leaves the carried figure" % name, carry(v) == carry(ind), (name, v))

    # ---------------------------------------------------------------- the goldens
    memo = open(os.path.join(golden, K.DELIVERABLES[0]), encoding="utf-8").read()
    ck("golden memo states the call", "Carry $400 million" in memo and "$344.6 million" in memo and
       "$55.4 million" in memo)
    csv_rows = open(os.path.join(golden, K.DELIVERABLES[1]), encoding="utf-8").read().strip().splitlines()
    ck("golden counts file has a row per accident year", len(csv_rows) == 11)
    for row in csv_rows[1:]:
        y, a, c = row.split(",")
        ck("golden counts %s" % y, int(a) == gc[int(y)]["with_payment"] and int(c) == gc[int(y)]["without_payment"])
    ck("golden chart written", os.path.getsize(os.path.join(golden, K.DELIVERABLES[2])) > 10000)

    # ---------------------------------------------------------------- realism sweep
    for f in files + list(K.DELIVERABLES):
        p = os.path.join(target, f) if f in files else os.path.join(golden, f)
        if p.endswith((".md", ".txt", ".csv")):
            t = open(p, encoding="utf-8", errors="replace").read()
            ck("no em or en dash in %s" % f, "\u2014" not in t and "\u2013" not in t)
    for f, t in texts.items():
        for w in ("Berquist", "disposal", "backlog", "restat", "slower", "slowed", "pace", "speed"):
            ck("no %s in %s" % (w, f), w.lower() not in t.lower(), (w, f))
    pf = b["pf"]
    ck("no platform timestamp after the run", max(pd.to_datetime(pf.created_at, utc=True)) <=
       pd.Timestamp(K.RUN).tz_localize(K.CENTRAL).tz_convert("UTC"))
    ck("no legacy transaction after the conversion", b["lp"].date.max() < pd.Timestamp(K.PLATFORM_LIVE))
    print("checks: %d passed (Ask A cracker misses %d of 20; Ask B face-value read misses %d of 8)" % (
        ck.n, st["ask_a_cracker_missed"], st["ask_b_face_missed"]))


# ------------------------------------------------------------------ variants used above

def _restated_from(P, C, Rr):
    n = A.ultimate_counts(Rr)
    rs = A.restate(P, C / n[:, None])
    lat = A.latest(P)
    return float((A.project(A.factors(rs), lat) - lat).sum())


def utc_restated(target):
    """The triangles with every platform timestamp read on its UTC date."""
    import load as LL
    old = LL._central
    LL._central = lambda s: pd.to_datetime(s, utc=True, errors="coerce").dt.tz_localize(None)
    try:
        b = A.book(target)
        P, C, Rr = A.triangles(b)
    finally:
        LL._central = old
    return _restated_from(P, C, Rr)


def claims_restated(b):
    """Closure ratios on claims (accidents) rather than claimant features: a claim is closed when all its features
    are."""
    lc, pf = b["lc"], b["pf"]
    f = b["feats"]
    claim_of = dict(zip(lc.key, lc.CLM_NO))
    for fid, cn, ref in zip(pf.feature_id, pf.claim_number, pf.legacy_ref):
        claim_of[fid] = claim_of.get(ref, cn) if ref else cn
    keys = f.key.to_numpy()
    idx = {k: n for n, k in enumerate(keys)}
    st = np.zeros((len(keys), A.NQ))
    tr = b["trans"]
    ok = tr.key.isin(idx) & (tr.tq < A.NQ)
    np.add.at(st, (tr.key[ok].map(idx).to_numpy(), tr.tq[ok].to_numpy()), tr.d[ok].to_numpy().astype(float))
    closed = np.cumsum(st, axis=1) > 0
    claim = np.array([claim_of.get(k, k) for k in keys])
    df = pd.DataFrame(closed, columns=range(A.NQ))
    df["claim"] = claim
    cl_closed = df.groupby("claim").min()
    first = f.groupby(claim).aq.min()
    rq = f.groupby(claim).rq.min()
    Cc = np.full((A.NQ, A.NQ), np.nan)
    Rc = Cc.copy()
    for i in range(A.NQ):
        members = first.index[first.to_numpy() == i]
        cc = cl_closed.loc[members]
        r = rq.loc[members].to_numpy()
        for j in range(A.NQ - i):
            q = i + j
            Rc[i, j] = int((r <= q).sum())
            Cc[i, j] = int(cc[q].sum())
    P, _, _ = A.triangles(b)
    return _restated_from(P, Cc, Rc)


def gross_restated(b):
    pays = b["pays"]
    g = pays[pays.amount > 0]
    P = A._cum(g.aq.to_numpy(), g.tq.to_numpy(), g.amount.to_numpy())
    _, C, Rr = A.triangles(b)
    return _restated_from(P, C, Rr)


def latest_close_restated(b):
    """Closings read from each feature's latest recorded closing alone (the register's closed_at, the archive's
    CLS_DT), with no reopening history."""
    pf, lc = b["pf"], b["lc"]
    f = b["feats"]
    keys = set(f.key)
    plat = pf[pf.closed.notna()]
    pk = np.where(plat.legacy_ref.isin(b["re_keys"]), plat.legacy_ref, plat.feature_id)
    rows = pd.DataFrame({"key": pk, "t": plat.closed.to_numpy()})
    rows = rows[rows.key.isin(keys)]
    leg = lc[lc.key.isin(keys) & ~lc.key.isin(b["re_keys"])]
    rows = pd.concat([rows, pd.DataFrame({"key": leg.key.to_numpy(), "t": (leg.cls + pd.Timedelta(hours=12)).to_numpy()})],
                     ignore_index=True)
    rows["aq"] = rows.key.map(dict(zip(f.key, f.aq)))
    rows["tq"] = A.qidx(rows.t)
    C = A._cum(rows.aq.to_numpy(), rows.tq.to_numpy(), np.ones(len(rows)))
    P, _, Rr = A.triangles(b)
    return _restated_from(P, C, Rr)


def cracker_counts(b):
    """The cracker's Ask A: payments read from both ledgers with each converted feature linked through its legacy
    reference, voids netted at 31 December, the CV and opened-in-error rows dropped with their payments; the closed
    archive rows of re-entered features kept beside their platform rows."""
    pays = b["pays"]
    pf, lc0 = b["pf"], b["lc"]
    dups = set(pf.feature_id[pf.disposition == "DUPLICATE"]) | set(lc0.key[lc0.DISP == "XD"])
    p = pays[(pays.tq < A.NQ) & ~pays.fid.isin(dups)]
    fp = A.feature_payments({**b, "pays": p})
    base = A.counts_by_year({**b, "pays": p})
    lc = b["lc"]
    leg = pays[(pays.sys == "legacy") & pays.fid.isin(b["re_keys"])].groupby("fid").amount.sum()
    out = {y: {k: v[k] for k in ("with_payment", "without_payment")} for y, v in base.items()}
    for k, acc in zip(lc.key[lc.key.isin(b["re_keys"])], lc.acc[lc.key.isin(b["re_keys"])]):
        out[acc.year]["with_payment" if leg.get(k, 0.0) > 0.005 else "without_payment"] += 1
    return out


def face_value_ledger(target):
    """Ask B read at face value: a feed line is its posting day's previous day's checks, a Treasury journal is the
    previous calendar month's wires, a manual journal is not a payment, and the repeated feed batch is a payment."""
    gl = L.ledger(target)
    out = {}
    for q in range(4):
        lo = dt.date(2026, 3 * q + 1, 1)
        hi = dt.date(2026, 3 * q + 4, 1) if q < 3 else dt.date(2027, 1, 1)
        g = gl[(gl.date.dt.date >= lo) & (gl.date.dt.date < hi)]
        earlier = other = 0.0
        for d, src, a in zip(g.date, g.source, g.amount):
            if src == "CLAIMS FEED":
                if (d - pd.Timedelta(days=1)).date() < lo:
                    earlier += a
            elif src == "TREASURY":
                prev = d - pd.DateOffset(months=1)
                if dt.date(prev.year, prev.month, 1) < lo:
                    earlier += a
            else:
                other += a
        out[q + 1] = dict(earlier=round(earlier, 2), other=round(other, 2))
    return out


def separation_variants(b):
    """The call under each of Ask A's devices mishandled."""
    out = {}
    pays = b["pays"]
    pf = b["pf"]
    dups = set(pf.feature_id[pf.disposition == "DUPLICATE"]) | set(b["lc"].key[b["lc"].DISP == "XD"])
    p2 = pays[~pays.fid.isin(dups)]
    P = A._cum(p2.aq.to_numpy(), p2.tq.to_numpy(), p2.amount.to_numpy())
    _, C, Rr = A.triangles(b)
    out["duplicates' payments dropped"] = _restated_from(P, C, Rr)
    lc = b["lc"]
    rows = lc[lc.key.isin(b["re_keys"])]
    f2 = pd.concat([b["feats"], pd.DataFrame({"key": rows.key + "#legacy", "acc": rows.acc, "rep": rows.rep,
                                              "sys": "legacy", "aq": A.qidx(rows.acc), "rq": A.qidx(rows.rep)})],
                   ignore_index=True)
    tr2 = pd.concat([b["trans"], pd.DataFrame({"key": rows.key + "#legacy", "t": rows.cls + pd.Timedelta(hours=12),
                                               "d": 1, "aq": A.qidx(rows.acc), "tq": A.qidx(rows.cls)})],
                    ignore_index=True)
    P0, C2, R2 = A.triangles({**b, "feats": f2, "trans": tr2})
    out["re-entered features counted twice"] = _restated_from(P0, C2, R2)
    pp = b["pp"]
    jv = pp[pp.voided.notna() & (pp.voided >= pd.Timestamp(K.VAL))]
    extra = pd.DataFrame({"acc": jv.feature_id.map(dict(zip(pf.feature_id, pf.acc))), "amount": -jv.amount})
    p3 = pd.concat([pays, pd.DataFrame({"aq": A.qidx(extra.acc), "tq": A.NQ - 1, "amount": extra.amount})],
                   ignore_index=True)
    P3 = A._cum(p3.aq.to_numpy(), p3.tq.to_numpy(), p3.amount.to_numpy())
    out["January voids netted at the year end"] = _restated_from(P3, C, Rr)
    return out
