"""Assertions on the build: the input gates, the golden reproduced from the cut pack and from the generator's clean
truth (R1 the raw material ships, R2 each Layer 1 item neutral, R3a the analyst test, R3b the decisive step alone,
R3c nothing planted), the ladder, every shortcut a reader might take, the golden's model family and its one-decimal
bins, the semantic fork table, the two ask devices against every stop, the separation of the asks from the call,
the documents, the containers and the realism sweep."""
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import warnings

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A      # noqa: E402
import common as K        # noqa: E402
import core as C          # noqa: E402
import models as M        # noqa: E402
import pack as PK         # noqa: E402
import routes as RT       # noqa: E402
from deliver import dollars, r1   # noqa: E402

FAILS = []
COUNT = [0]


def check(label, ok, detail=""):
    COUNT[0] += 1
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))


def edge1(x):
    """Distance of x from the nearest one-decimal rounding edge."""
    return 0.05 - abs(float(x) - round(float(x), 1))


def trio(s):
    return frozenset(s.sort_values().index[:3])


def names(s):
    return "+".join(K.NAME[h].split()[0] for h in s.sort_values().index[:3])


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    w = b["w"]
    P = res["P"]
    m = res["m"]
    code = {v: k for k, v in K.NAME.items()}
    GOLD = frozenset(code[n] for n in fig["call"]["centres"])
    NAIVE = frozenset(["C", "E", "G"])
    below = code[fig["call"]["first_below"]]
    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    check("GATE ten or more files", len(files) >= 10, len(files))
    exts = {f.rsplit(".", 1)[1] for f in files}
    check("GATE three or more formats", len(exts) >= 3, sorted(exts))
    big = max(b["counts"].values())
    check("GATE a file of 25,000 rows or more", big >= 25000, big)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    check("GATE two distractors named in metadata.json", len(meta["distractors"]) >= 2 and
          all(d in files for d in meta["distractors"]), meta["distractors"])
    check("GATE every file has provenance", set(meta["provenance"]) == set(files), len(meta["provenance"]))
    contents = open(os.path.join(target, K.FILES["contents"])).read()
    check("GATE contents lists every other file", all(f in contents for f in files if f != K.FILES["contents"]))
    check("GATE no file named after the stump",
          not any(re.search(r"redo|reoper|earlier|history|prior|previous|risk|expected", f) for f in files))
    # ---------------------------------------------------------------- the golden from the pack and the clean truth
    ix = w["ix"].set_index(["h", "year", "k"])
    bykey = {rec["key"]: rec for rec in w["index"]}
    df = m["df"]
    flags = ["male", "mal", "tot", "whip", "urg", "redo", "dead", "chf", "ckd", "copd", "liver", "dm", "af", "wtloss",
             "chole", "stent", "htn", "lipid", "gerd", "obese", "smoke", "osa", "thyroid", "depress"]
    bad = 0
    for _, r in df.iterrows():
        t = ix.loc[bykey[r.key]["core"]]
        if any(bool(r[f]) != bool(t[f]) for f in flags):
            bad += 1
    check("GOLDEN every operation in the pack carries the clean truth's pre-operative factors, earlier operation and "
          "death within 90 days (2,022 operations)", bad == 0 and len(df) == len(w["ix"]), (bad, len(df)))
    check("GOLDEN the pack's operations by hospital equal the clean truth's",
          all(int(m["operations"][h]) == int((w["ix"].h == h).sum()) for h in K.ELIGIBLE), m["operations"].to_dict())
    check("GOLDEN the three centres are Netherfold, Ferncastle and Aldermoor", GOLD == frozenset(["A", "E", "G"]),
          fig["call"]["centres"])
    check("GOLDEN Farrowmere is the first hospital below", below == "C", below)
    g = m["ratio"].sort_values()
    check("GOLDEN the third centre leads the first hospital below by 0.05 or more unrounded",
          g.iloc[3] - g.iloc[2] >= 0.05, round(g.iloc[3] - g.iloc[2], 4))
    for h in K.ELIGIBLE:
        check("GOLDEN %s's ratio sits 0.005 or more inside its one-decimal bin" % K.NAME[h],
              edge1(m["ratio"][h]) >= 0.005, round(edge1(m["ratio"][h]), 4))
        check("GOLDEN %s's figures agree (ratio = deaths / expected, rounded half up)" % K.NAME[h],
              r1(m["observed"][h] / m["expected"][h]) == fig["ratio"][K.NAME[h]])
    # ---------------------------------------------------------------- R1 the raw material ships
    keyed = sum(1 for rec in P["discharges"] if rec["key"])
    check("R1 the person key ships on 99 per cent or more of the discharge records", keyed / len(P["discharges"]) >= .99,
          round(keyed / len(P["discharges"]), 4))
    redo_keys = set(df.key[df.redo == 1])
    found = {k for rec in P["discharges"] if rec["key"] in redo_keys and rec["discharge"].year <= 2022
             for k in [rec["key"]] if any(c in A.EARLIER for c, _ in rec["px"])}
    check("R1 every patient with an earlier operation has it in a shipped file before 2023", found == redo_keys,
          (len(found), len(redo_keys)))
    for f in files:
        if f.endswith(".csv"):
            cols = re.split(r"[,_ ]", open(os.path.join(target, f)).readline().strip().lower())
            for wd in ("redo", "prior", "previous", "earlier", "history", "risk", "expected", "ratio", "reoperation"):
                check("R1 no shipped column names the deciding quantity (%s, %s)" % (f, wd), wd not in cols)
    # ---------------------------------------------------------------- R3 the analyst test on the clean truth
    truth = M.prep(w["ix"])
    tn = M.ratio(truth, M.INDEX)[0]
    tg = M.ratio(truth, M.GOLDEN)[0]
    check("R3a the analyst test: on the clean truth the model on the operation's own record files Netherfold, "
          "Ferncastle and Farrowmere", trio(tn) == NAIVE, names(tn))
    check("R3a Aldermoor is fifth or lower on the clean truth's index-record model",
          list(tn.sort_values().index).index("A") >= 4, list(tn.sort_values().index).index("A") + 1)
    check("R3b the decisive step alone (the earlier operation in the model) files the golden on the clean truth",
          trio(tg) == GOLD, names(tg))
    # ---------------------------------------------------------------- the ladder and the shortcuts
    L = RT.ladder(P)
    for k in ("raw", "index", "index_probit", "index_many", "index_comp", "index_min", "index_eb", "any_earlier",
              "history_from_2023", "volume"):
        check("SHORTCUT %s does not name the golden three" % k, trio(L[k]) != GOLD, names(L[k]))
    for k in ("index", "index_probit", "index_many", "index_min", "any_earlier", "history_from_2023"):
        check("LADDER %s names Netherfold, Ferncastle and Farrowmere" % k, trio(L[k]) == NAIVE, names(L[k]))
    ri = L["index"].sort_values()
    check("LADDER the default path: Aldermoor fifth, 0.05 or more above the third", list(ri.index).index("A") == 4 and
          ri["A"] - ri.iloc[2] >= 0.05, round(ri["A"] - ri.iloc[2], 4))
    d = RT.frame(P)
    g2 = d.assign(cp=d.pdx.str.startswith("K86.1").astype(float),
                  benign=(~d.pdx.str.startswith("C") & ~d.pdx.str.startswith("K86.1")).astype(float))
    sr = M.ratio(g2, M.INDEX + ["cp", "benign"])[0]
    check("SHORTCUT the diagnosis in groups on the operation's own record does not name the golden three",
          trio(sr) != GOLD, names(sr))
    for k in ("first_only", "history_from_2019"):
        print("INFO  WITH THE INSIGHT %s: %s (Aldermoor %.3f)" % (k, names(L[k]), L[k]["A"]))
        check("LADDER %s (the earlier operation found) names the golden three" % k, trio(L[k]) == GOLD, names(L[k]))
    # ---------------------------------------------------------------- the golden's family and its bins
    F = RT.family(d)
    for k, v in F.items():
        check("FAMILY %s names the golden three and Farrowmere first below" % k,
              trio(v) == GOLD and v.sort_values().index[3] == below, names(v))
    bn = RT.bins(F)
    for h in K.ELIGIBLE:
        check("FAMILY %s: every member lands on the golden's %.1f, 0.005 or more inside the bin"
              % (K.NAME[h], fig["ratio"][K.NAME[h]]),
              r1(bn["lo"][h]) == r1(bn["hi"][h]) == fig["ratio"][K.NAME[h]] and bn["edge"][h] >= 0.005,
              (round(bn["lo"][h], 4), round(bn["hi"][h], 4), bn["edge"][h]))
    for k, v in RT.shortcuts(d).items():
        print("INFO  OFF THE ESTIMAND %s: %s (Aldermoor %.3f)" % (k, names(v), v["A"]))
    # ---------------------------------------------------------------- R2 each Layer 1 item, mishandled
    for nm, sr in layer1_mishandled(P).items():
        check("R2 neutral: %s keeps the call" % nm, trio(sr) == GOLD, names(sr))
    # ---------------------------------------------------------------- the semantic fork table
    sf_checks(P, fig, m, GOLD, NAIVE)
    # ---------------------------------------------------------------- the asks
    asks(P, fig, w)
    # ---------------------------------------------------------------- separation
    sep_ok, sep_detail = separation(target, m)
    check("SEPARATION the call computes identically with the 2026 releases and the claims emptied", sep_ok, sep_detail)
    idx_keys = {rec["key"] for rec in w["index"]}
    check("SEPARATION no correction pair or re-operation is an operation of the main population",
          not any(x["key"] in idx_keys and x["discharge"] <= K.WINDOW[1] for x in w["first_sent"].values()))
    # ---------------------------------------------------------------- documents and realism
    documents(target)
    realism(target, P, w)
    containers(task)
    import cracker
    cr = cracker.run(task, quiet=True)
    check("CRACKER the battery finds nothing in the revised release or the claims",
          cr["battery"]["revised exact duplicates (all but the record number)"] == 0 and
          cr["battery"]["claims exact duplicates (all but the claim id)"] == 0 and
          cr["battery"]["claims naming a claim not in the extract"] == 0 and cr["battery"]["claims NPIs unmatched"] == 0,
          cr["battery"])
    check("CRACKER keeps none of the 16 ask figures", cr["cracker_hits"] == 0, cr["cracker_hits"])
    check("CRACKER the mirror keeps under 35 per cent of the ask figures", cr["mirror_hits"] < 0.35 * cr["total"],
          cr["mirror_hits"])
    check("CRACKER the pair ceiling is 40 or under", cr["pair"] <= 40.0, round(cr["pair"], 1))
    print("checks: %d, failed: %d" % (COUNT[0], len(FAILS)))
    for f in FAILS:
        print("  failed:", f)
    return 0 if not FAILS else 1


def golden_on(P, ops=None, hist_filter=None):
    """The golden's model on an altered reading of the pack."""
    saved_ops, saved_hist = A.operations, A.history
    try:
        if ops is not None:
            A.operations = lambda P_: ops
        if hist_filter is not None:
            def hist(P_):
                h = {}
                for rec in P_["discharges"]:
                    if not rec["key"] or not hist_filter(rec):
                        continue
                    for c, dd in rec["px"]:
                        if c in A.EARLIER:
                            h.setdefault(rec["key"], []).append(dd or rec["admit"])
                return h
            A.history = hist
        d = M.prep(A.frame(P))
        return M.ratio(d, M.GOLDEN)[0]
    finally:
        A.operations, A.history = saved_ops, saved_hist


def layer1_mishandled(P):
    """The golden method with one Layer 1 item mishandled at a time."""
    out = {}
    # the 2018 file read with the 2016-2017 layout: its procedure codes come out garbled, so nothing from 2018 links
    out["the 2018 file's county column missed (2018 lost to the history)"] = golden_on(
        P, hist_filter=lambda rec: rec["file"] != "2018")
    out["the fixed-width files skipped altogether (history from 2019)"] = golden_on(
        P, hist_filter=lambda rec: rec["file"] not in ("2016", "2017", "2018"))
    # the 2019-2022 file's procedure dates set aside (the admission date in their place)
    def no_dates(rec):
        if rec["file"] == "2019-2022":
            rec = dict(rec, px=[(c, None) for c, _ in rec["px"]])
        return rec
    Q = dict(P, discharges=[no_dates(r) for r in P["discharges"]])
    out["the 2019-2022 procedure dates set aside for the admission date"] = golden_on(Q)
    return out


def sf_checks(P, fig, m, GOLD, NAIVE):
    ops = A.operations(P)
    # SF1 the Appendix A code as the first procedure only
    first = [r for r in ops if r["px"] and r["px"][0][0] in K.RESECTION]
    sr = golden_on(P, ops=first)
    check("SF1 the code as the first procedure only keeps the call", trio(sr) == GOLD, names(sr))
    # SF2 the population by discharge date
    sr = golden_on(P, ops=RT.by_discharge(P))
    check("SF2 the population by discharge date keeps the call (the same operations)",
          trio(sr) == GOLD and len(RT.by_discharge(P)) == len(ops), (names(sr), len(RT.by_discharge(P)), len(ops)))
    # SF3 89 or 91 days
    fr = A.frame(P)
    d = M.prep(fr)
    for lim in (89, 91):
        dd = d.copy()
        dd["dead"] = [float(P["deaths"].get(k) is not None and 0 <= (P["deaths"][k] - o).days <= lim)
                      for k, o in zip(fr.key, fr.op)]
        sr = M.ratio(dd, M.GOLDEN)[0]
        check("SF3 deaths within %d days keep the call" % lim, trio(sr) == GOLD, names(sr))
    # SF4 a death after a transfer: the death follows the person, so the operating hospital keeps it
    tr = [r for r in ops if r["disp"] == "02"]
    check("SF4 deaths are linked to the operation's record (transfers out counted at the operating hospital)",
          all(r["hosp"] in K.ELIGIBLE for r in tr), len(tr))
    # SF5 a model per hospital gives each hospital a ratio of 1
    one = []
    for h in K.ELIGIBLE:
        sub = d[d.h == h]
        r_ = M.ratio(sub.assign(h=h), M.INDEX)[0][h]
        one.append(abs(r_ - 1) < 1e-6)
    check("SF5 a model fitted per hospital gives every hospital a ratio of 1 (not a comparison)", all(one))
    # SF6 the index admission's record only
    sr = M.ratio(d, M.INDEX)[0]
    check("SF6 the operation's own record names Netherfold, Ferncastle and Farrowmere; the golden the golden three "
          "(the decisive step, not a reading)", trio(sr) == NAIVE and trio(m["ratio"]) == GOLD, names(sr))
    import statsmodels.api as sm
    X0 = sm.add_constant(d[M.INDEX].astype(float), has_constant="add")
    X1 = sm.add_constant(d[M.GOLDEN].astype(float), has_constant="add")
    fam = sm.families.Binomial()
    dv0 = sm.GLM(d.dead.astype(float), X0, family=fam).fit().deviance
    m1 = sm.GLM(d.dead.astype(float), X1, family=fam).fit()
    check("SF6 the earlier operation lowers the deviance by 20 or more on one term and carries a coefficient near "
          "1.2 (1.0 to 1.4)", dv0 - m1.deviance >= 20 and 1.0 <= m1.params["redo"] <= 1.4,
          (round(dv0 - m1.deviance, 1), round(m1.params["redo"], 3)))
    # SF7 lumped against separate terms
    e = d.assign(any_earlier=((d.redo + d.chole + d.stent) > 0).astype(float))
    lump = M.ratio(e, M.INDEX + ["any_earlier"])
    sep = M.ratio(d, M.GOLDEN + ["chole", "stent"])
    check("SF7 lumped with the stent and the gallbladder removal: Netherfold, Ferncastle and Farrowmere; separate "
          "terms: the golden", trio(lump[0]) == NAIVE and trio(sep[0]) == GOLD, (names(lump[0]), names(sep[0])))
    check("SF7 the stent's own term is near zero (|z| under 1) and the lumped flag fits worse than separate terms",
          abs(sep[1].params["stent"] / sep[1].bse["stent"]) < 1 and lump[1].deviance - sep[1].deviance >= 5,
          (round(sep[1].params["stent"], 3), round(lump[1].deviance - sep[1].deviance, 1)))
    # SF8 the rounded tie
    check("SF8 Aldermoor and Farrowmere share 0.9 rounded; unrounded Aldermoor is lower by 0.05 or more",
          fig["ratio"][K.NAME["A"]] == fig["ratio"][K.NAME["C"]] == 0.9 and
          m["ratio"]["C"] - m["ratio"]["A"] >= 0.05, round(m["ratio"]["C"] - m["ratio"]["A"], 4))
    # SF9 adults
    check("SF9 every patient in the population is 18 or over at admission (25 or over)",
          min(r["age"] for r in ops) >= 25, min(r["age"] for r in ops))
    # SF10 Maplewick
    mw = [r for r in P["discharges"] if r["hosp"] == "G2" and A._res_date(r) and A._res_date(r).year >= 2023]
    check("SF10 Maplewick performed no resection from 2023", len(mw) == 0, len(mw))
    # SF11 a patient operated twice
    keys = [r["key"] for r in ops]
    check("SF11 no patient has two operations in the window", len(keys) == len(set(keys)))


def asks(P, fig, w):
    a = A.ask_a(P)
    b = A.ask_b(P)
    # Ask A: the clean truth from the world: distinct H1 resection stays at each hospital, recoded ones out
    truth = {h: 0 for h in K.ELIGIBLE}
    for rec in w["all"]:
        if rec["hosp"] in truth and K.H1_2026[0] <= rec["discharge"] <= K.H1_2026[1] and \
                any(c in K.RESECTION for c, _ in rec["px"]) and rec["rec_id"] not in w["recoded"]:
            truth[rec["hosp"]] += 1
    for h in K.ELIGIBLE:
        check("ASK A the golden equals the clean truth (%s)" % K.NAME[h], a[h] == truth[h] == fig["ask_a"][K.NAME[h]],
              (a[h], truth[h]))
    import records as R
    kind = w["first_kind"]
    for h in K.ELIGIBLE:
        ks = {kind[rid] for rid, x in w["first_sent"].items() if x["hosp"] == h and R._is_res(x)}
        check("ASK A device at %s: a corrected discharge date and a rebooked case stand twice" % K.NAME[h],
              {"dis", "adm_op"} <= ks, sorted(ks))
        n_re = sum(1 for x in w["background"] if x["kind"] == "reop" and x["hosp"] == h)
        check("ASK A over-cleaning half at %s: a completion pancreatectomy on the same patient" % K.NAME[h], n_re >= 1)
    for nm, got in ask_a_stops(P).items():
        hits = [h for h in K.ELIGIBLE if got[h] == fig["ask_a"][K.NAME[h]]]
        check("ASK A stop misses every hospital: %s" % nm, not hits, " ".join("%s:%d" % (h, got[h]) for h in K.ELIGIBLE))
    # Ask B: the clean truth from the world
    for h in K.ELIGIBLE:
        st = [s for s in w["plan_stays"] if s["hosp"] == h]
        tv = dollars(sum(s["allowed"] for s in st) / len(st))
        check("ASK B the golden equals the clean truth (%s)" % K.NAME[h],
              dollars(b[h][1]) == tv == fig["ask_b"][K.NAME[h]] and b[h][0] == len(st), (dollars(b[h][1]), tv))
        check("ASK B %s's average sits off its rounding edge (0.01 or more)" % K.NAME[h],
              abs(b[h][1] - round(b[h][1]) ) <= 0.49, round(b[h][1], 3))
    ch = w["plan_chains"]
    for h in K.ELIGIBLE:
        mine = [c for c in ch if c["stay"]["hosp"] == h]
        check("ASK B device at %s: a Medicare Advantage claim with two later versions naming it" % K.NAME[h],
              any(c["lob"] == "MA" and len(c["versions"]) >= 3 for c in mine))
        check("ASK B device at %s: a claim on the plan's own platform replaced twice in a chain" % K.NAME[h],
              any(c["lob"] != "MA" and len(c["versions"]) >= 3 for c in mine))
        check("ASK B hazard at %s: a replacement correcting the discharge date" % K.NAME[h],
              any(any(v["statement_through"] != c["root"]["statement_through"] for v in c["versions"]) for c in mine))
    for nm, got in ask_b_stops(P).items():
        hits = [h for h in K.ELIGIBLE if got[h] == fig["ask_b"][K.NAME[h]]]
        check("ASK B stop misses every hospital: %s" % nm, not hits, " ".join("%s:%d" % (h, got[h]) for h in K.ELIGIBLE))
    vals = list(fig["ask_a"].values())
    check("ASK A no two hospitals share a figure", len(set(vals)) == len(vals))
    check("ASK A every hospital's figure is 11 or more (the consortium's publication floor)", min(vals) >= 11, min(vals))


def _h1(recs):
    return [r for r in recs if r["hosp"] in K.ELIGIBLE and A._res_date(r) is not None and
            K.H1_2026[0] <= r["discharge"] <= K.H1_2026[1]]


def _count(rows, key=None):
    c = {h: 0 for h in K.ELIGIBLE}
    seen = set()
    for r in rows:
        if key is not None:
            k = key(r)
            if k in seen:
                continue
            seen.add(k)
        c[r["hosp"]] += 1
    return c


def ask_a_stops(P):
    rv = _h1(P["revised"])
    q1 = dt.date(2026, 3, 31)
    return {
        "the revised release's records (the cracker)": _count(rv),
        "a stay keyed on person, hospital, admission and discharge": _count(
            rv, lambda r: (r["key"], r["hosp"], r["admit"], r["discharge"])),
        "keyed on person, hospital and admission": _count(rv, lambda r: (r["key"], r["hosp"], r["admit"])),
        "keyed on person, hospital and discharge": _count(rv, lambda r: (r["key"], r["hosp"], r["discharge"])),
        "keyed on person, hospital and operation date": _count(rv, lambda r: (r["key"], r["hosp"], A._res_date(r))),
        "one resection per person at a hospital": _count(rv, lambda r: (r["key"], r["hosp"])),
        "the preliminary's first quarter with the revision's second": _count(
            [r for r in _h1(P["prelim"]) if r["discharge"] <= q1] + [r for r in rv if r["discharge"] > q1]),
        "both releases together": _count(_h1(P["prelim"]) + rv),
    }


def ask_b_stops(P):
    cl = P["claims"]

    def avg(stays):
        return {h: dollars(stays[stays.hosp == h].allowed.sum() / len(stays[stays.hosp == h])) for h in K.ELIGIBLE}
    voided = set(cl.original_claim_id[cl.bill_type == "0118"])
    named = set(cl.original_claim_id[cl.bill_type == "0117"])
    out = {}
    out["every claim summed"] = avg(cl.groupby(["hosp", "member_id", "admit_date"]).allowed.sum().reset_index())
    k = cl[(cl.bill_type != "0118") & ~cl.claim_id.isin(voided) & ~cl.claim_id.isin(named)]
    out["voids out, every named claim dropped, a stay's claims summed (the cracker)"] = avg(
        k.groupby(["hosp", "member_id", "admit_date"]).allowed.sum().reset_index())
    k2 = cl[(cl.bill_type != "0118") & ~cl.claim_id.isin(voided)].copy()
    k2["fam"] = [o if o else c for c, o in zip(k2.claim_id, k2.original_claim_id)]
    cur = k2.sort_values(["received_date", "claim_id"]).groupby("fam").tail(1)
    out["the latest claim per family keyed on original_claim_id"] = avg(
        cur.groupby(["hosp", "member_id", "admit_date"]).allowed.sum().reset_index())
    cur = k2.sort_values(["received_date", "claim_id"]).groupby(
        ["hosp", "member_id", "admit_date", "statement_from", "statement_through"]).tail(1)
    out["the latest version per stay and statement period"] = avg(
        cur.groupby(["hosp", "member_id", "admit_date"]).allowed.sum().reset_index())
    cur = k2.sort_values(["received_date", "claim_id"]).groupby(["hosp", "member_id", "admit_date"]).tail(1)
    out["the latest claim per stay"] = avg(cur)
    k3 = cl[~cl.bill_type.isin(["0117", "0118"]) & ~cl.claim_id.isin(voided)]
    out["every replacement dropped"] = avg(k3.groupby(["hosp", "member_id", "admit_date"]).allowed.sum().reset_index())
    return out


def separation(target, m):
    """The call recomputed with the 2026 releases and the plan's claims replaced by their header rows."""
    tmp = tempfile.mkdtemp()
    try:
        for f in os.listdir(target):
            shutil.copy(os.path.join(target, f), os.path.join(tmp, f))
        for k in ("prelim", "revised", "claims"):
            with open(os.path.join(target, K.FILES[k])) as fh:
                head = fh.readline()
            open(os.path.join(tmp, K.FILES[k]), "w").write(head)
        Q = PK.load(tmp)
        r = A.main_call(Q)
        same = r["centres"] == m["centres"] and all(abs(r["ratio"][h] - m["ratio"][h]) < 1e-12 for h in K.ELIGIBLE)
        return same, "+".join(r["centres"])
    finally:
        shutil.rmtree(tmp)


LEAK = ["re-operation", "reoperation", "redo", "earlier operation", "previous operation", "prior operation",
        "earlier admission", "previous admission", "prior admission", "surgical history", "history of",
        "referred on", "previous surgery", "prior surgery", "risk model", "logistic"]


def documents(target):
    from pypdf import PdfReader
    for k in ("criteria", "guide"):
        txt = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, K.FILES[k])).pages).lower()
        txt = re.sub(r"\s+", " ", txt)
        for wd in LEAK:
            check("DOC %s does not say '%s'" % (k, wd), wd not in txt)
        check("DOC %s states no ratio or expected death count" % k, not re.search(r"\b[01]\.\d{1,3}\b ratio", txt))
    txt = open(os.path.join(target, K.FILES["contents"])).read().lower()
    for wd in LEAK:
        check("DOC contents does not say '%s'" % wd, wd not in txt)


def containers(task):
    """H1 and H16: no writer's name in any shipped container, and no stamp outside the fiction's dates."""
    import importlib.util
    path = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                        "scrub_producer_metadata.py")
    spec = importlib.util.spec_from_file_location("scrub_producer_metadata", path)
    sm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sm)
    for folder, floor, ceiling in (("target", "2023-01-01", K.ASSEMBLED.date().isoformat()),
                                   ("golden", "2026-10-09", "2026-10-31")):
        d = os.path.join(task, folder)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            r = sm.audit(os.path.join(d, f), floor, ceiling)
            check("CONTAINER %s/%s carries no writer's name and no stamp outside %s to %s" % (folder, f, floor, ceiling),
                  r is None or not (r[0] or r[1]), r)


def realism(target, P, w):
    # dates: no discharge after the release's half-year, no claim received after the extract
    last = max(r["discharge"] for r in P["discharges"])
    check("REALISM the discharge files end by 31 December 2025", last <= dt.date(2025, 12, 31), last)
    check("REALISM the revised release ends by 30 June 2026", max(r["discharge"] for r in P["revised"]) <= K.H1_2026[1])
    check("REALISM the preliminary release ends by 31 March 2026",
          max(r["discharge"] for r in P["prelim"]) <= dt.date(2026, 3, 31))
    check("REALISM no claim received after 30 September 2026",
          P["claims"].received_date.max() <= K.PLAN_CLAIMS_THROUGH.isoformat(), P["claims"].received_date.max())
    check("REALISM no death after the linkage run", max(P["deaths"].values()) <= K.DEATHS_LINKED)
    # no stay discharged before it was admitted, no procedure outside its stay
    badd = sum(1 for r in P["discharges"] if r["discharge"] < r["admit"])
    check("REALISM every stay is discharged on or after its admission", badd == 0, badd)
    out_of = sum(1 for r in P["discharges"] if r["file"] not in ("2016", "2017", "2018")
                 for c, dd in r["px"] if dd and not (r["admit"] <= dd <= r["discharge"]))
    check("REALISM every dated procedure falls inside its stay", out_of == 0, out_of)
    # no copied block: no person key on two records with the same admission, discharge and hospital in the history
    seen, dup = set(), 0
    for r in P["discharges"]:
        if not r["key"]:
            continue
        k = (r["key"], r["hosp"], r["admit"], r["discharge"])
        dup += k in seen
        seen.add(k)
    check("R3c no stay stands twice in the 2016 to 2025 files (nothing copied)", dup == 0, dup)
    # containers
    for f in os.listdir(target):
        bts = open(os.path.join(target, f), "rb").read()
        check("REALISM no writer's name in %s" % f, b"ReportLab" not in bts and b"openpyxl" not in bts.lower()
              and b"matplotlib" not in bts.lower())
    # H21: invented names away from real places
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()]
    invented = [n.split()[0] for n in K.NAME.values()] + ["Corrisbrook"]
    for nm in invented:
        n = nm.lower()
        near = [p for p in places if edit(n, p) <= 2 or (len(p) >= 6 and p in n) or (len(n) >= 6 and n in p)]
        check("H21 %s is three or more edits from every reference place" % nm, not near, near[:3])
    check("REALISM the personas are the ones drawn", set(K.PEOPLE.values()) == {"Katrina Newman", "Luis Thomas"})


def edit(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]
