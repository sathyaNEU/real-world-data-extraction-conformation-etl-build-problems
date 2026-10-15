"""task257's generator checks: the input gates, the bundle against the generator's clean truth, the three rules
executed (R1 to R3c), every semantic fork row (SF1 to SF16), the ladder (counts, margins, placements under every
extraction and rotation), both asks' devices, stops and cracker sheet, the separation line, the goldens against
figures.json, and the realism sweep."""
from __future__ import annotations

import itertools
import json
import os
import re
import shutil
import tempfile

import numpy as np
import pandas as pd

import common as K
import deliver as G
import load as L
import psy


class Checks:
    def __init__(self):
        self.n = 0

    def __call__(self, label, cond, detail=""):
        if not cond:
            raise AssertionError("%s: %s" % (label, detail))
        self.n += 1


TOPIC_PARTITION = None


def topic_partition(order, S, groups):
    """A partition of item positions by topic groups, e.g. ['WT', 'MG', 'BR']."""
    key_of = {it["en_code"]: it["topic"] for it in S["items"]}
    return tuple(sorted(tuple(j for j, c in enumerate(order) if key_of[c] in g) for g in groups))


def clean_truth(S, order):
    """The generator's own answers, before any file is written: one row per respondent (late answers excluded), the
    items each employee gave across their submissions (the last web submission, every kiosk session, the form), coded
    as the golden codes them; and the continuous views behind them."""
    items = {it["en_code"]: it for it in S["items"]}
    idx = {it["en_code"]: j for j, it in enumerate(S["items"])}
    rows, Z, emp, dist, comp = [], [], [], [], []
    by_no = {s["site_no"]: s for s in S["sites"]}
    for x in S["resp"]:
        if x.get("late"):
            continue
        given = {}
        subs = x["subs"] if x["channel"] == "kiosk" else [x["subs"][-1]]
        for z in subs:
            for j, c, _ in z["answers"]:
                given[S["items"][j]["en_code"]] = c
        v = np.full(30, np.nan)
        for k, c in enumerate(order):
            if c not in given:
                continue
            a = given[c]
            it = items[c]
            if a == 6:
                continue
            if it["kind"] == "a5":
                v[k] = (4 - (a - 1)) if it["rev"] else a - 1
            else:
                v[k] = 1.0 if a == 1 else 0.0
        rows.append(v)
        Z.append([x["z"][idx[c]] for c in order])
        emp.append("%07d" % x["p"]["emp"])
        s = by_no[x["open_site"]]
        dist.append(s["district"])
        comp.append(len(given) == 30)
    Kc = np.array([2 if items[c]["kind"] == "yn" else 5 for c in order])
    return np.array(rows), np.array(Z), Kc, emp, dist, comp


def run(target, golden, st, meta_path):
    ck = Checks()
    res = st["res"]
    S = st["S"]
    fig = res["figures"]
    T, X, Kc, order = res["T"], res["X"], res["Kc"], res["order"]
    files = sorted(os.listdir(target))
    key_of = {it["en_code"]: it["topic"] for it in S["items"]}
    GOLD = topic_partition(order, S, ["WT", "MG", "BR"])
    FIVE = topic_partition(order, S, ["W", "T", "M", "G", "BR"])
    gold_part = psy.partition(res["groups"])

    # ---------------------------------------------------------------- input gates
    ck("gate: 10 or more files", len(files) >= 10, files)
    ck("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ck("gate: a file of 25,000 rows or more", st["counts"]["responses"] >= 25000, st["counts"]["responses"])
    meta = json.load(open(meta_path))
    ck("gate: two distractors named in metadata.json", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]), meta["distractor_files"])
    ck("gate: no distractor named as such", not any("distract" in f.lower() for f in files))
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(target, f), os.path.join(tmp, f))
        G._REF.clear()
        f2 = G.compute(tmp)["figures"]
        ck("gate: every distractor deleted, the golden and both asks unchanged", f2 == fig)
    finally:
        shutil.rmtree(tmp)

    # ---------------------------------------------------------------- the bundle against the clean truth
    Xt, Zt, Kt, emp_t, dist_t, comp_t = clean_truth(S, order)
    rows, _ = G.answer_rows(T)
    ok = G.before_close(T, rows)
    r_units = sorted(set(rows.loc[ok & rows["key"].notna(), "employee"]))
    ck("truth: the bundle's respondents are the generator's respondents", r_units == sorted(emp_t),
       (len(r_units), len(emp_t)))
    Xb = pd.DataFrame(X, index=res["units"])
    Xg = pd.DataFrame(Xt, index=emp_t).sort_index()
    ck("truth: every respondent's answers read from the bundle equal the generator's", np.array_equal(
        np.nan_to_num(Xb.to_numpy(), nan=-9), np.nan_to_num(Xg.to_numpy(), nan=-9)))
    A_t = {d: 0 for d, _, _ in K.DISTRICTS}
    B_t = {d: 0 for d, _, _ in K.DISTRICTS}
    for d, c in zip(dist_t, comp_t):
        if d in A_t:
            A_t[d] += 1
            B_t[d] += int(c)
    ck("truth: Ask A from the bundle equals the generator's respondents by opening-day district", res["A"] == A_t,
       (res["A"], A_t))
    ck("truth: Ask B from the bundle equals the generator's complete respondents", res["B"] == B_t, (res["B"], B_t))

    # ---------------------------------------------------------------- the call and its ladder on the bundle
    lat, pea = res["lat"], res["pea"]
    ck("call: three dimensions on the latent correlations (random data, 95th percentile)", lat["pa95"] == 3, lat["pa95"])
    ck("call: the golden partition is the generator's three dimensions", gold_part == GOLD, gold_part)
    ck("ladder R0: five on Pearson correlations (random data, 95th percentile)", pea["pa95"] == 5, pea["pa95"])
    ck("ladder R0: five at the random-data mean", pea["pamean"] == 5, pea["pamean"])
    ck("ladder R0: Kaiser's rule keeps five on Pearson correlations", pea["kaiser"] == 5, pea["kaiser"])
    ck("ladder R0: MAP keeps five on Pearson correlations", pea["map"] == 5, pea["map"])
    ck("ladder R2b: the revised MAP on Pearson correlations keeps three or four", pea["map4"] in (3, 4), pea["map4"])
    m4, m5 = pea["ev"][3] - pea["p95"][3], pea["ev"][4] - pea["p95"][4]
    ck("ladder margin: Pearson fourth and fifth eigenvalues at least 0.15 above random data", min(m4, m5) >= 0.15,
       (m4, m5))
    ml4 = lat["p95"][3] - lat["ev"][3]
    ck("ladder margin: latent fourth eigenvalue at least 0.2 below random data", ml4 >= 0.2, ml4)
    d3, d5 = pea["ev"][2] - pea["ev"][3], pea["ev"][4] - pea["ev"][5]
    ck("ladder: Pearson scree has a second elbow after five (drop after 5th >= 0.7 x drop after 3rd)", d5 >= 0.7 * d3,
       (d3, d5))
    combos = list(itertools.product(psy.EXTRACT.items(), psy.ROTATE.items()))
    for (en, ef), (rn, rf) in combos:
        p3 = psy.partition(psy.placements(rf(ef(lat["R"], 3))))
        ck("C1 SF13: latent, %s with %s, gives the golden placements" % (en, rn), p3 == GOLD, p3)
        p5 = psy.partition(psy.placements(rf(ef(pea["R"], 5))))
        ck("ladder R0: Pearson five-factor %s with %s splits tools and growth off" % (en, rn), p5 == FIVE, p5)
        q3 = psy.partition(psy.placements(rf(ef(pea["R"], 3))))
        ck("ladder R2b: Pearson three-factor %s with %s is not the golden" % (en, rn), q3 != GOLD, q3)
    ck("SF13: Kaiser's rule on the latent correlations keeps three", lat["kaiser"] == 3, lat["kaiser"])
    ck("SF13: MAP on the latent correlations keeps three", lat["map"] == 3, lat["map"])
    ck("SF13: the revised MAP on the latent correlations keeps three", lat["map4"] == 3, lat["map4"])
    ck("SF13: random data at the mean keeps three on the latent correlations", lat["pamean"] == 3, lat["pamean"])
    lev = lat["ev"]
    ck("SF13: the latent scree's elbow is after the third (drop 3 to 4 > 10 x every later drop)",
       lev[2] - lev[3] > 10 * max(lev[3:9] - lev[4:10]))
    Lp = psy.promax(psy.paf(lat["R"], 3))
    srt = np.sort(np.abs(Lp), 1)
    gap = srt[:, -1] - srt[:, -2]
    ck("SF3: every item's largest loading exceeds its second by at least 0.25", gap.min() >= 0.25, gap.min())

    def same_call(Xv, Kv, label, cols=None, correct=0.0, weights=None):
        dv = G.dimensions(Xv, Kv, "latent", correct=correct, weights=weights, reps=60)
        Lv = psy.promax(psy.paf(dv["R"], 3))
        part = psy.partition(psy.placements(Lv)[:30])
        ck(label, dv["pa95"] == 3 and part == GOLD, (dv["pa95"], part))
        return dv

    # ---------------------------------------------------------------- semantic forks and Layer 1 items (R2)
    Xe, Ke, ce = G.call_matrix(T, enps=True)
    de = G.dimensions(Xe, Ke, "latent", reps=60)
    Le = psy.promax(psy.paf(de["R"], 3))
    pe = psy.partition(psy.placements(Le)[:30])
    ck("SF2: the recommend question added as a 31st variable, three and the same placements",
       de["pa95"] == 3 and psy.partition(psy.placements(Le[:30])) == GOLD, (de["pa95"], pe))
    Xv, Kv, _ = G.call_matrix(T, tests=True, late=True)
    same_call(Xv, Kv, "SF4 R2: test tokens and late answers kept, the same call")
    Xv, Kv, _ = G.call_matrix(T, dna="category")
    same_call(Xv, Kv, "SF5 R2: does-not-apply scored as an extra category, the same call")
    Xr = X.copy()
    items_cb = T["items"].set_index("Item")
    for j, c in enumerate(order):
        if items_cb.loc[c, "Reversed"] == "yes":
            Xr[:, j] = 4 - Xr[:, j]
    same_call(Xr, Kc, "SF6 R2: negatively worded statements left as answered, the same call")
    Xy = X.copy()
    for j, c in enumerate(order):
        if items_cb.loc[c, "Scale"] == "yesno":
            Xy[:, j] = 1 - Xy[:, j]
    same_call(Xy, Kc, "SF7: yes and no in the export's order (yes 1, no 2), the same call")
    py_ = G.dimensions(Xy, Kc, "pearson")
    ck("SF7: a linear recode moves no Pearson correlation", np.allclose(np.abs(py_["R"]), np.abs(pea["R"])))
    for lang in ("EN", "FR"):
        Xv, Kv, _ = G.call_matrix(T, language=lang)
        if lang == "EN":
            same_call(Xv, Kv, "SF8 R2: English answers alone (French codes not mapped), the same call")
        ck("ladder R2: %s answers alone keep five on Pearson correlations" % lang,
           G.dimensions(Xv, Kv, "pearson", reps=60)["pa95"] == 5)
    Xv, Kv, _ = G.call_matrix(T, keep="all")
    same_call(Xv, Kv, "SF9 R2: every submission kept as a respondent, the same call")
    Xv, Kv, _ = G.call_matrix(T, kiosk="token")
    same_call(Xv, Kv, "SF10 R2: each kiosk session a respondent, the same call")
    Xv, Kv, _ = G.call_matrix(T, paper="answered_at")
    same_call(Xv, Kv, "R2 separation: printed forms keyed after the close dropped, the same call")
    # SF11: weighted to site headcounts (each respondent weighted by the site's employees over its respondents)
    opening = L.opening_site(T["hris"])
    head = {}
    for e, s in opening.items():
        head[s] = head.get(s, 0) + 1
    resp_site = [opening.get(u) for u in sorted(r_units)]
    nresp = pd.Series(resp_site).value_counts().to_dict()
    w = np.array([head[s] / nresp[s] for s in resp_site])
    same_call(X, Kc, "SF11: answers weighted to site headcounts, the same call", weights=w)
    Xc = X[~np.isnan(X).any(1)]
    same_call(Xc, Kc, "SF12: complete cases only (%d respondents), the same call" % len(Xc))
    ck("ladder R2: complete cases keep five on Pearson correlations", G.dimensions(Xc, Kc, "pearson", reps=60)["pa95"] == 5)
    same_call(X, Kc, "SF14: psych's 0.5 correction for empty cells, the same call", correct=0.5)
    ck("ladder R2: rank (Spearman) correlations keep five", G.dimensions(X, Kc, "spearman")["pa95"] == 5)
    five = np.array([items_cb.loc[c, "Scale"] == "agree5" for c in order])
    sub = X[:, five]
    straight = np.array([len(set(v[~np.isnan(v)])) == 1 and (~np.isnan(v)).sum() >= 10 for v in sub])
    Xs = X[~straight]
    ck("ladder R2: straight-liners (%d) dropped keep five on Pearson correlations" % straight.sum(),
       G.dimensions(Xs, Kc, "pearson", reps=60)["pa95"] == 5)
    same_call(Xs, Kc, "ladder R2: straight-liners dropped, the latent route keeps the golden")
    ck("SF1: the codebook carries no area, theme or grouping column", not any(
        re.search(r"theme|area|section|scale group|sub-?scale|dimension|factor", str(c), re.I)
        for c in T["items"].columns if c != "Scale"), list(T["items"].columns))
    ck("SF1: the questionnaire's order interleaves the six areas", max(
        len(list(g)) for _, g in itertools.groupby(key_of[c] for c in order)) <= 2)
    pulse = pd.read_csv(os.path.join(target, K.PULSE))
    ck("SF15: no pulse item is in the export", not set(T["resp"]["item"]) & set(pulse.columns))
    from pypdf import PdfReader
    std = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, K.STANDARD)).pages)
    std = re.sub(r"\s+", " ", std)
    ck("SF16: the standard fixes the questionnaire for 2026 and 2027", "used unchanged in the 2026 and 2027 surveys" in std)
    ck("SF1: the standard defines a sub-scale as a distinct dimension the items measure",
       "one distinct dimension of employees' views that the survey's items measure" in std)
    ck("R3 not rule application: no filed sentence names an estimator or a retention test", not re.search(
        r"polychoric|tetrachoric|pearson|correlat|eigen|parallel analysis|factor|random data", std, re.I))
    notes = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(target, K.EXPORT_NOTES)).pages))
    ck("R3 not rule application: the export notes name no estimator", not re.search(
        r"polychoric|tetrachoric|correlat|eigen|factor|sub-?scale|dimension", notes, re.I))

    # ---------------------------------------------------------------- the three rules on the clean truth (R1, R3)
    ck("R1: the spine is one row per answer (respondent by item), 25,000 rows or more",
       list(T["resp"].columns) == ["token", "submission", "item", "answer", "answered_at"] and len(T["resp"]) >= 25000)
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += [h for h in open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")]
    ck("R1: no shipped column holds a dimension, sub-scale, factor or loading", not any(
        re.search(r"dimension|sub-?scale|factor|loading|theme", h, re.I) for h in heads), heads)
    dt_ = G.dimensions(Xt, Kt, "pearson")
    p5 = psy.partition(psy.placements(psy.promax(psy.paf(dt_["R"], dt_["pa95"]))))
    ck("R3a: the easy route on the clean truth (Pearson, random data) files five sub-scales", dt_["pa95"] == 5, dt_["pa95"])
    ck("R3a: and splits tools and growth off as their own", p5 == FIVE, p5)
    dl = G.dimensions(Xt, Kt, "latent")
    pl = psy.partition(psy.placements(psy.promax(psy.paf(dl["R"], dl["pa95"]))))
    ck("R3b: the decisive step alone (latent correlations) on the clean truth files the golden",
       dl["pa95"] == 3 and pl == GOLD, (dl["pa95"], pl))
    Rz = np.corrcoef(Zt, rowvar=False)
    evz = psy.eigen(Rz)
    _, p95z = G.random_reference(len(Zt), 30)
    ck("R3b: the continuous views before they are cut keep three on Pearson correlations",
       psy.keep_above(evz, p95z) == 3, evz[:5])
    ck("R3c: no answer row repeated in the export", not T["resp"].duplicated().any())
    sig = T["resp"].sort_values(["token", "submission", "item"]).groupby(["token", "submission"]).apply(
        lambda g: hash(tuple(zip(g["item"], g["answer"], g["answered_at"]))), include_groups=False)
    ck("R3c: no submission's answers and times copied under another token", not sig.duplicated().any())

    # ---------------------------------------------------------------- empty cells (SF14) and the tools-growth tables
    tools = [j for j, c in enumerate(order) if key_of[c] == "T"]
    growth = [j for j, c in enumerate(order) if key_of[c] == "G"]
    mincell = min(int(((X[:, t] == 0) & (X[:, g] == 1)).sum()) for t in tools for g in growth)
    ck("SF14: every tools-by-growth table has at least 5 employees in its sparsest cell", mincell >= 5, mincell)
    R5 = psy.latent_corr(X, Kc, correct=0.5)[0]
    ck("SF14: the 0.5 correction moves no latent correlation by 0.02", np.abs(R5 - lat["R"]).max() < 0.02,
       np.abs(R5 - lat["R"]).max())

    # ---------------------------------------------------------------- the asks
    env = T["paper"]
    ck("ask A device: every envelope was sealed by the close", (pd.to_datetime(env["Sealed"]).dt.date <= K.CLOSE_DAY).all())
    pre = {}
    for paper in ("sealed", "answered_at"):
        for close in ("local", "utc_date", "eastern", "links"):
            pre[(paper, close)] = (rows, G.before_close(T, rows, paper=paper, close=close))
    Agold, Bgold = res["A"], res["B"]

    def off(D, gold):
        return sum(1 for d in gold if D[d] != gold[d])
    A_cr, B_cr = G.district_counts(T, paper="answered_at", complete="token", pre=pre[("answered_at", "local")])
    ck("cracker A: second-envelope forms dropped, every district off", off(A_cr, Agold) == 12, A_cr)
    ck("cracker B: one complete token required, every district off", off(B_cr, Bgold) == 12, B_cr)
    _, B_ls = G.district_counts(T, paper="answered_at", complete="last_session", pre=pre[("answered_at", "local")])
    ck("cracker B: the last kiosk session taken, every district off", off(B_ls, Bgold) == 12, B_ls)
    _, B_kio = G.district_counts(T, complete="token", pre=pre[("sealed", "local")])
    ck("ask B device: kiosk time-outs alone move every district", off(B_kio, Bgold) == 12, B_kio)
    A_p, B_p = G.district_counts(T, paper="answered_at", pre=pre[("answered_at", "local")])
    ck("ask A device: second-envelope forms alone move every district (A and B)", off(A_p, Agold) == 12 and
       off(B_p, Bgold) == 12)
    for d, _, _ in K.DISTRICTS:
        ck("ask devices: %s's second-envelope respondents (%d) and kiosk-joined completes (%d) both live" % (
            d, Agold[d] - A_p[d], Bgold[d] - B_kio[d]), Agold[d] - A_p[d] >= 10 and Bgold[d] - B_kio[d] >= 3)
    A_u, B_u = G.district_counts(T, close="utc_date", pre=pre[("sealed", "utc_date")])
    ck("hazard: UTC dates against the close move every district", off(A_u, Agold) == 12, A_u)
    A_l, _ = G.district_counts(T, site="list", pre=pre[("sealed", "local")])
    ck("hazard: the distribution list's site moves at least three districts", off(A_l, Agold) >= 3, A_l)
    A_t2, _ = G.district_counts(T, people="tokens", pre=pre[("sealed", "local")])
    ck("hazard: tokens counted as people move every district", off(A_t2, Agold) == 12, A_t2)
    _, B_d = G.district_counts(T, dna="missing", pre=pre[("sealed", "local")])
    ck("hazard: does-not-apply counted as missing moves every district (B)", off(B_d, Bgold) == 12, B_d)
    hits_a = hits_b = 0
    for paper, close, site, people in itertools.product(("sealed", "answered_at"), ("local", "utc_date", "eastern",
                                                                                     "links"), ("opening", "list"),
                                                        ("employees", "tokens")):
        if paper == "sealed":
            continue
        Av, _ = G.district_counts(T, paper=paper, close=close, site=site, people=people, pre=pre[(paper, close)])
        hits_a += 12 - off(Av, Agold)
    for paper, close, site, complete, dna in itertools.product(("sealed", "answered_at"), ("local", "utc_date",
                                                                                           "eastern", "links"),
                                                               ("opening", "list"), ("union", "token", "last_session"),
                                                               ("answer", "missing")):
        if paper == "sealed" and complete == "union":
            continue
        _, Bv = G.district_counts(T, paper=paper, close=close, site=site, complete=complete, dna=dna,
                                  pre=pre[(paper, close)])
        hits_b += 12 - off(Bv, Bgold)
    ck("no handling with the paper forms dropped lands on any Ask A cell", hits_a == 0, hits_a)
    ck("no handling with the paper forms dropped or the kiosk sessions apart lands on any Ask B cell", hits_b == 0,
       hits_b)
    subs = T["subs"]
    pap = rows[rows["channel"] == "paper"]
    ck("no marker: printed forms keyed both during the survey and after the close",
       (pap["answered_at"] < "2026-09-27").any() and (pap["answered_at"] > "2026-09-30").any())
    ck("no marker: saved submissions on the web and at the kiosk", set(subs.loc[subs["status"] == "saved", "channel"])
       >= {"web", "kiosk"})
    kio = T["kiosk"]
    to = kio[kio["close_reason"] == "timed out"]
    again = kio.groupby("employee")["session"].count()
    ck("no marker: time-outs with and without a later session", (to["employee"].map(again) > 1).any() and
       (to["employee"].map(again) == 1).any())
    late = rows[~pre[("sealed", "local")][1] & (rows["channel"] == "web")]
    ck("hazard live: answers recorded after a site's close and before Kestrava's links stopped", len(late) > 0,
       len(late))

    # ---------------------------------------------------------------- goldens against figures.json
    gx = pd.read_excel(os.path.join(golden, K.DELIVERABLES[0]), sheet_name=None)
    items_g = gx["Items"].dropna(subset=["Sub-scale"])
    ck("golden xlsx: 30 items, each under one of three sub-scales", len(items_g) == 30 and
       items_g["Sub-scale"].nunique() == 3)
    for nm, codes in fig["subscale_items"].items():
        ck("golden xlsx: %s holds the figures.json items" % nm, sorted(items_g.loc[items_g["Sub-scale"] == nm,
                                                                                      "Item"]) == sorted(codes))
    dd = gx["Districts"].dropna(subset=["Code"]).set_index("Code")
    for d in Agold:
        ck("golden xlsx: %s coverage matches figures.json" % d, int(dd.loc[d].iloc[1]) == fig["ask_a"][d] and
           int(dd.loc[d].iloc[2]) == fig["ask_b"][d])
    md = open(os.path.join(golden, K.DELIVERABLES[2]), encoding="utf-8").read()
    ck("golden note: states three sub-scales", "three sub-scales" in md)
    for d, nm, _ in K.DISTRICTS:
        ck("golden note: %s row" % d, "| %s | %s | %s |" % (nm, "{:,}".format(Agold[d]), "{:,}".format(Bgold[d])) in md)

    # ---------------------------------------------------------------- realism sweep
    ck("realism: no two districts share a respondent count", len(set(Agold.values())) == 12, Agold)
    ck("realism: no two districts share a complete count", len(set(Bgold.values())) == 12, Bgold)
    ck("realism: totals are not round", fig["ask_a_total"] % 100 and fig["ask_b_total"] % 100)
    ck("realism: every answer time inside 11 September to 9 October",
       T["resp"]["answered_at"].min() >= "2026-09-11" and T["resp"]["answered_at"].max() < "2026-10-10")
    ck("realism: kiosk sessions close after they open", (kio["closed"] > kio["signed_in"]).all())
    h = T["hris"]
    ck("realism: HR rows end on or after they start", ((h["effective_to"] == "") | (h["effective_to"] >= h["effective_from"])).all())
    texts = std + " " + notes
    names = set(re.findall(r"\b(Alexander Copeland|Maria Murray|Melissa Vang)\b", texts))
    ck("realism: the documents name only the drawn people", names <= set(K.PEOPLE.values()) and len(names) >= 2, names)
    ck("realism: no em or en dash in any document", not re.search("[–—]", texts + md))
    for f in files:
        if f.endswith((".csv", ".jsonl")):
            raw = open(os.path.join(target, f), encoding="utf-8").read()
            ck("realism: no em or en dash in %s" % f, not re.search("[–—]", raw))
    print("checks: %d assertions passed" % ck.n)
    return ck.n
