"""task257's generator checks: the input gates, the bundle against the generator's clean truth, the three rules
executed (R1 to R3c), every semantic fork row (SF1 to SF16), the ladder (counts, margins, placements under every
extraction and rotation), the department ask's device, stops and cracker sheet, the separation line, the goldens
against figures.json, and the realism sweep."""
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
        ck("gate: every distractor deleted, the golden and the department ask unchanged", f2 == fig)
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
    import world as W
    _, hr_truth = W.hr_extract(S)
    by_no = {s["site_no"]: s for s in S["sites"]}
    resp_t = set(emp_t)
    D_t = {d: [0, 0] for d in G.STORE_DEPARTMENTS}
    team_t = {}
    for e, (s, d) in hr_truth.items():
        if by_no[s]["type"] != "store":
            continue
        D_t[d][1] += 1
        if e in resp_t:
            D_t[d][0] += 1
            team_t[(s, d)] = team_t.get((s, d), 0) + 1
    DF = res["DF"]
    ck("truth: the department respondents read from the bundle equal the generator's",
       all(DF["resp"][d] == D_t[d][0] for d in D_t), (DF["resp"], D_t))
    ck("truth: the department headcounts on the opening day read from the bundle equal the generator's",
       all(DF["head"][d] == D_t[d][1] for d in D_t), (DF["head"], D_t))
    ck("truth: the stores showing each department equal the generator's", all(
        DF["shown"][d] == sum(1 for (s, dd), n in team_t.items() if dd == d and n >= 10) for d in D_t))

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
    ck("SF6: the negatively worded statements read from the answers are the questionnaire's four",
       T["neg"] == {it["en_code"] for it in S["items"] if it["rev"]}, sorted(T["neg"]))
    for j, c in enumerate(order):
        if c in T["neg"]:
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
    ck("SF1: the questionnaire carries no area, theme or grouping column", not any(
        re.search(r"theme|area|section|scale group|sub-?scale|dimension|factor", str(c), re.I)
        for c in T["items"].columns if c != "Scale"), list(T["items"].columns))
    ck("SF8: the questionnaire maps every French code to one item", len(set(T["items"]["French code"])) == 31 and
       all(T["items"].set_index("Item").loc[it["en_code"], "French code"] == it["fr_code"] for it in S["items"]))
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
    quest = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(os.path.join(target, K.QUESTIONNAIRE)).pages))
    ck("R3 not rule application: the questionnaire names no estimator, grouping or area", not re.search(
        r"polychoric|tetrachoric|correlat|eigen|factor|sub-?scale|dimension|theme|section", quest, re.I))
    ck("SF5 SF7: the questionnaire's options carry the codes the export records",
       "Yes (1), No (2), Does not apply to me (6)" in quest and "Strongly agree (5), Does not apply to me (6)" in quest)
    ck("SF9: the standard counts a personal link's last submission", "its last submission counts" in std)
    ck("no describing file ships: no codebook, dictionary, notes, readme or manifest by name",
       not any(re.search(r"codebook|dictionar|notes|readme|manifest|schema", f, re.I) for f in files), files)

    # ---------------------------------------------------------------- the three rules on the clean truth (R1, R3)
    ck("R1: the spine is one row per answer (respondent by item), 25,000 rows or more",
       list(T["resp"].columns) == ["token", "submission", "item", "answer", "answered_at"] and len(T["resp"]) >= 25000)
    heads = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                line = fh.readline()
                while line.startswith("#"):
                    line = fh.readline()
            heads += line.strip().split(",")
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

    # ---------------------------------------------------------------- the department ask
    hris = T["hris"]
    sites = T["sites"]
    store_no = set(sites.loc[sites["site_type"] == "store", "site_no"].astype(int))
    code, pairs = G.renumbering(hris, sites)
    ck("device forcing: every store code in force on 30 September passes to one department on 1 October",
       pairs.groupby(level=0).size().max() == 1 and len(code) == 8, pairs)
    sep30 = L.in_force(hris, K.RENUMBER_DAY - __import__("datetime").timedelta(days=1))
    sep30 = sep30[sep30["site_no"].astype(int).isin(store_no)]
    oct_rows = hris[hris["effective_from"] == K.RENUMBER_DAY.isoformat()]
    ck("device forcing: every store employee in force on 30 September has a 1 October row at the same site",
       set(zip(sep30["employee_id"], sep30["site_no"])) <= set(zip(oct_rows["employee_id"], oct_rows["site_no"])),
       len(sep30))
    named = {c: d for c, d in zip(hris["department_code"], hris["department"])}
    ck("device silent: every September store code has a name on the report (the run date's table)",
       all(named.get(c) for c in code))
    swapped = sum(1 for c in code if named[c] != code[c])
    ck("device mass: every September store code is named after another department on the report", swapped == 8,
       swapped)
    ck("no marker: the 1 October rows carry the July reorganisation's action (and the day's leavers theirs)",
       set(hris.loc[hris["effective_from"] == K.RENUMBER_DAY.isoformat(), "action"]) <=
       {"reorganisation", "transfer", "termination"} and
       set(hris.loc[hris["effective_from"] == K.REORG_DAY.isoformat(), "action"]) == {"reorganisation"})
    dc_ho = hris[~hris["site_no"].astype(int).isin(store_no)]
    ck("no marker: distribution centre and head office codes keep their names on both sides of 1 October",
       dc_ho.groupby("department_code")["department"].nunique().max() == 1 and
       not (dc_ho["effective_from"] == K.RENUMBER_DAY.isoformat()).any())
    before = L.in_force(hris, K.RENUMBER_DAY - __import__("datetime").timedelta(days=1))
    before = before[before["site_no"].astype(int).isin(store_no)]
    oct1 = hris[(hris["effective_from"] == K.RENUMBER_DAY.isoformat()) & (hris["action"] == "reorganisation")]
    m = before.merge(oct1, on=["employee_id", "site_no"], suffixes=("_b", "_a"))
    moved_named = int((m["department_b"] != m["department_a"]).sum())
    ck("forcing number: read by the report's names, every paired store employee changes department on 1 October "
       "(%d of %d); read through the renumbering, none does" % (moved_named, len(m)),
       moved_named == len(m) and all(code[c] == d for c, d in zip(m["department_code_b"], m["department_a"])))
    rs = G.respondents(T)
    F0 = DF
    stops = {}
    for mode in ("named", "latest", "own_next"):
        F = G.department_figures(T, rs, mode=mode)
        stops[mode] = sum((F["resp"][d] != F0["resp"][d]) + (F["rate"][d] != F0["rate"][d]) +
                          (F["shown"][d] != F0["shown"][d]) for d in G.STORE_DEPARTMENTS)
        if mode == "named":
            Fn = F
    ck("cracker (the opening-day row as the report names it): every one of the 24 cells off", stops["named"] == 24,
       stops)
    ck("cracker margins: respondents 20 or more, rates 0.2 points or more, stores 2 or more off in every department",
       min(abs(Fn["resp"][d] - F0["resp"][d]) for d in G.STORE_DEPARTMENTS) >= 20 and
       min(abs(Fn["rate"][d] - F0["rate"][d]) for d in G.STORE_DEPARTMENTS) >= 0.2 - 1e-9 and
       min(abs(Fn["shown"][d] - F0["shown"][d]) for d in G.STORE_DEPARTMENTS) >= 2, Fn)
    ck("stop: each employee's latest row (the current department) misses 22 or more of the 24 cells",
       stops["latest"] >= 22, stops)
    ck("stop: each employee's own 1 October row misses 18 or more of the 24 cells", stops["own_next"] >= 18, stops)
    # hazards: moves inside a store before and after the opening day, the 5 October promotions, leavers
    tr = hris[(hris["action"] == "transfer")]
    ck("hazard live: department moves inside a store before the opening day",
       ((tr["effective_from"] < K.OPEN_DAY.isoformat()) & (tr["effective_from"] >= "2026-08-15")).sum() >= 150)
    ck("hazard live: department moves inside a store after the opening day",
       (tr["effective_from"] > K.OPEN_DAY.isoformat()).sum() >= 600)
    ck("hazard live: the 5 October moves into store management",
       ((tr["effective_from"] == "2026-10-05") & (tr["department"] == "Store Management")).sum() >= 150)
    late_leave = hris[(hris["action"] == "termination") & (hris["effective_from"] > K.OPEN_DAY.isoformat())]
    ck("hazard live: employees assigned on the opening day who left afterwards", len(late_leave) >= 40, len(late_leave))
    # the separation line: the call reads no HR row
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f != K.HRIS:
                shutil.copy(os.path.join(target, f), os.path.join(tmp, f))
        G._REF.clear()
        f3 = G.compute(tmp)["figures"]
        ck("separation: with the HR report deleted, the call's respondents, eigenvalues and placements are unchanged",
           all(f3[k] == fig[k] for k in ("respondents", "latent_eigen", "pearson_eigen", "random_p95", "subscale_items",
                                         "call_subscales", "yes_share")))
    finally:
        shutil.rmtree(tmp)
    rows_all, _ = G.answer_rows(T)
    ok_hr = G.before_close(T, rows_all, site_from="hr")
    ok_tok = G.before_close(T, rows_all, site_from="token")
    ck("separation: the close read from the HR site and from the token's own site keeps the same answer rows",
       bool((ok_hr == ok_tok).all()))
    edge = min(abs((F0["rate_exact"][d] * 10) % 1 - 0.5) / 10 for d in G.STORE_DEPARTMENTS)
    ck("rounding edges: each department's response rate 0.01 points or more from its tenth's edge (closest %.4f)"
       % edge, edge >= 0.01, F0["rate_exact"])

    # ---------------------------------------------------------------- goldens against figures.json
    gx = pd.read_excel(os.path.join(golden, K.DELIVERABLES[0]), sheet_name=None)
    items_g = gx["Items"].dropna(subset=["Sub-scale"])
    ck("golden xlsx: 30 items, each under one of three sub-scales", len(items_g) == 30 and
       items_g["Sub-scale"].nunique() == 3)
    for nm, codes in fig["subscale_items"].items():
        ck("golden xlsx: %s holds the figures.json items" % nm, sorted(items_g.loc[items_g["Sub-scale"] == nm,
                                                                                      "Item"]) == sorted(codes))
    dd = gx["Departments"].dropna(subset=["Store department"]).set_index("Store department")
    for d in G.STORE_DEPARTMENTS:
        ck("golden xlsx: %s matches figures.json" % d, int(dd.loc[d].iloc[0]) == fig["dept_respondents"][d] and
           abs(float(dd.loc[d].iloc[2]) - fig["dept_rate"][d]) < 1e-9 and
           int(dd.loc[d].iloc[3]) == fig["dept_stores_shown"][d])
    md = open(os.path.join(golden, K.DELIVERABLES[2]), encoding="utf-8").read()
    ck("golden note: states three sub-scales", "three sub-scales" in md)
    for d in G.STORE_DEPARTMENTS:
        ck("golden note: %s row" % d, "| %s | %s | %s | %.1f | %d |" % (
            d, "{:,}".format(fig["dept_respondents"][d]), "{:,}".format(fig["dept_headcount"][d]), fig["dept_rate"][d],
            fig["dept_stores_shown"][d]) in md)

    # ---------------------------------------------------------------- realism sweep
    ck("realism: store department respondents sum to the store respondents",
       fig["dept_respondents_total"] == sum(fig["dept_respondents"].values()))
    ck("realism: totals are not round", fig["dept_respondents_total"] % 100 != 0)
    ck("realism: every answer time inside 11 September to 9 October",
       T["resp"]["answered_at"].min() >= "2026-09-11" and T["resp"]["answered_at"].max() < "2026-10-10")
    kio = T["kiosk"]
    ck("realism: kiosk sessions close after they open", (kio["closed"] > kio["signed_in"]).all())
    h = T["hris"]
    ck("realism: HR rows end on or after they start", ((h["effective_to"] == "") | (h["effective_to"] >= h["effective_from"])).all())
    texts = std + " " + quest
    names = set(re.findall(r"\b(Alexander Copeland|Maria Murray|Melissa Vang)\b", texts))
    ck("realism: the documents name only the drawn people", names <= set(K.PEOPLE.values()) and len(names) >= 2, names)
    ck("realism: no em or en dash in any document", not re.search("[–—]", texts + md))
    for f in files:
        if f.endswith((".csv", ".jsonl")):
            raw = open(os.path.join(target, f), encoding="utf-8").read()
            ck("realism: no em or en dash in %s" % f, not re.search("[–—]", raw))
    print("checks: %d assertions passed" % ck.n)
    return ck.n
