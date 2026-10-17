"""task239 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF16), the rungs and their margins, every Layer 1 slip against the call, the ask devices and their stops, the
separation of the call from the devices, the documents' pins, the input gates and the realism sweep."""
import json
import os
import re

import numpy as np
import pandas as pd

import estim as E
import params as P
import writeup as WU

N = [0]
HERE = os.path.dirname(os.path.abspath(__file__))
B_ITEMS = ["TC09", "TC10"]
C_ITEMS = ["TC11", "TC12"]
SLIPS = {
    "a member's earlier returns kept": dict(member=False),
    "a tablet's re-sent sessions kept": dict(replay=False),
    "a personal link's earlier submission kept": dict(resubmit=False),
    "paper forms after 8 October kept": dict(late=False),
    "blank paper forms kept": dict(blank=False),
    "unsubmitted sessions kept": dict(submitted_only=False),
    "don't know read as a sixth point": dict(scale="dk_value"),
    "paper's 8 and 9 read as answers": dict(scale="paper_raw_codes"),
    "TC04 and TC07 left unreversed": dict(scale="neg_not_reversed"),
    "tablet codes joined as they stand": dict(site_rule="raw"),
    "every tablet code read through the map": dict(site_rule="map"),
    "paper codes joined as they stand": dict(paper_rule="raw"),
    "every slip at once": dict(member=False, replay=False, resubmit=False, late=False, blank=False,
                               submitted_only=False, site_rule="raw", paper_rule="raw"),
}


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)


def _docx_text(path):
    import docx
    return " ".join(p.text for p in docx.Document(path).paragraphs)


def variant(D, **kw):
    sr = kw.pop("site_rule", "switch")
    pr = kw.pop("paper_rule", "map")
    R = E.resolve(D, E.counted(D, **kw), site_rule=sr, paper_rule=pr)
    R, rep = E.population(R)
    return R, rep


def stays(lam):
    return E.verdict(np.abs(lam))


# ------------------------------------------------------------------ the clean truth: each member's own answers
def clean(W):
    """one return per responding member (their first), every item answered, the member's true September team"""
    first = {}
    for r in W.rets:
        if r.get("blank"):
            continue
        m = r["member"]
        if m not in first or r["time"] < first[m]["time"]:
            first[m] = r
    ms = sorted(first)
    Y = np.array([first[m]["scored"] for m in ms], dtype=float)
    g = W.m_team[np.array(ms)]
    cnt = np.bincount(g, minlength=W.T)
    keep = cnt[g] >= 5
    return Y[keep], g[keep]


def run(target, golden, o, X):
    W, Rc = o["W"], o["R"]
    D, R = X["D"], X["R"]
    lam = X["lam"]
    gold = stays(X["golden"])
    golden_set = [c for c in E.ITEM_CODES if c not in C_ITEMS]
    ok(gold == golden_set, "golden: ten items stay, TC11 and TC12 withdrawn (%s)" % gold)

    # ---------------------------------------------------------------- R1: the field's raw material ships
    for f in os.listdir(target):
        if f.endswith(".csv"):
            cols = pd.read_csv(os.path.join(target, f), nrows=1).columns
            ok(not any(re.search(r"loading|icc|team_mean|between|within|factor", c, re.I) for c in cols),
               "R1 no shipped column holds a loading, an ICC, a team mean or a variance part (%s)" % f)
    ok(len(D["answers"]) > 100000 and "response" in D["answers"].columns,
       "R1 member-level answers ship, one row per question per session")
    ok(R["used"].sum() > 8 * len(X["reported"]),
       "R1 the check reads member returns, several per team, not team summaries")

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    Yc, gc = clean(W)
    cl = {h: E.loadings(Yc, gc, h) for h in ("pooled", "within", "means", "means_w", "disatt", "muml_paf",
                                             "muml_ml", "crosshalf")}
    ok(stays(cl["means"]) == [c for c in E.ITEM_CODES if c not in B_ITEMS + C_ITEMS],
       "R3a the easy route on the clean truth (one factor on team means) files eight items (%s)" % stays(cl["means"]))
    ok(stays(cl["muml_paf"]) == golden_set and stays(cl["muml_ml"]) == golden_set,
       "R3b the decisive step alone (between-team covariance net of the pooled within-team covariance) files the ten")
    ok(len(stays(cl["pooled"])) < 4 and len(stays(cl["within"])) < 4,
       "R3b the member-level rungs on the clean truth withdraw most items (%d, %d stay)"
       % (len(stays(cl["pooled"])), len(stays(cl["within"]))))
    ok(stays(cl["disatt"]) != golden_set, "R3b the reliability-corrected team means stay wrong on the clean truth")
    tm = R[R["used"]]
    rows = tm[E.ITEM_CODES].round(0).astype(int).astype(str).agg("".join, axis=1)
    blocks = rows.groupby(tm["team"]).apply(lambda s: s.duplicated().sum()).sum()
    ok(blocks < 0.03 * len(tm), "R3c no copied block: identical answer rows within a team are rare (%d)" % blocks)

    # ---------------------------------------------------------------- the rungs on the cut pack
    means_routes = ["means", "means_pca", "means_w", "means_n10", "blup"]
    for h in means_routes:
        ok(stays(lam[h]) == [c for c in E.ITEM_CODES if c not in B_ITEMS + C_ITEMS],
           "rung 0 (%s): eight items stay, TC09 to TC12 withdrawn" % h)
        b = max(lam[h][E.ITEM_CODES.index(c)] for c in B_ITEMS)
        need = 0.05 if h == "means" else 0.0
        ok(b < E.LINE - need, "rung 0 (%s): the practice items sit under the line by %.2f or more (%.3f)" % (h, need, b))
        ok(stays(lam[h]) != golden_set, "rung 0 (%s) never files the golden" % h)
    a_min = min(lam["means"][:8])
    ok(a_min >= E.LINE + 0.01, "rung 0: every climate item sits at least 0.01 over the line on team means (%.3f)" % a_min)
    ok(stays(E.loadings(*E.scores(R), "disatt_h")) != golden_set, "rung 2 with the harmonic team size: still wrong")
    ok(stays(lam["disatt"]) != golden_set and any(c not in stays(lam["disatt"]) for c in B_ITEMS),
       "rung 2 (team means corrected for unreliability) withdraws a practice item: %s"
       % [c for c in E.ITEM_CODES if c not in stays(lam["disatt"])])
    ok(len(stays(lam["pooled"])) <= 2 and len(stays(lam["within"])) <= 2,
       "floor rungs: member-level fits withdraw nearly every item")
    for h in E.GOLDEN_ROUTES:
        ok(stays(lam[h]) == golden_set, "golden route %s: ten items stay" % h)
        kept = min(lam[h][E.ITEM_CODES.index(c)] for c in golden_set)
        gone = max(abs(lam[h][E.ITEM_CODES.index(c)]) for c in C_ITEMS)
        ok(kept >= WU.KEEP_BAND and gone < WU.DROP_BAND,
           "golden route %s inside the bands (kept %.3f, withdrawn %.3f)" % (h, kept, gone))
    ok(X["golden"][E.ITEM_CODES.index("TC09")] - lam["means"][E.ITEM_CODES.index("TC09")] > 0.2
       and X["golden"][E.ITEM_CODES.index("TC10")] - lam["means"][E.ITEM_CODES.index("TC10")] > 0.2,
       "the decisive move lifts both practice items by more than 0.2")

    # ---------------------------------------------------------------- R2: every Layer 1 slip leaves the call and the rung
    for name, kw in SLIPS.items():
        Rv, rep = variant(D, **dict(kw))
        Y, g = E.scores(Rv)
        lg = E.loadings(Y, g, "muml_paf")
        lm = E.loadings(Y, g, "means")
        ok(stays(lg) == golden_set, "R2 %s: the call stays at ten" % name)
        ok(stays(lm) != golden_set and all(c not in stays(lm) for c in B_ITEMS),
           "R2 %s: the default path still withdraws the practice items" % name)
        kept = min(abs(lg[E.ITEM_CODES.index(c)]) for c in golden_set)
        gone = max(abs(lg[E.ITEM_CODES.index(c)]) for c in C_ITEMS)
        ok(kept >= WU.KEEP_BAND and gone < WU.DROP_BAND, "R2 %s: the components stay inside their bands" % name)

    # ---------------------------------------------------------------- semantic forks on the main call
    Y, g = E.scores(R)
    d = E.decompose(Y, g)
    SigB = (d["SB"] - d["SPW"]) / d["c"]
    staff = pd.read_csv(os.path.join(target, X["files"]["staff"])).set_index("team_code")["staff_in_post"]
    nt = staff.reindex(sorted(set(g))).values
    fin = SigB + d["SPW"] * np.mean(1.0 / nt)
    SF1 = stays(E.paf(fin))
    ok(SF1 != golden_set and stays(E.paf(SigB)) == golden_set,
       "SF1 the team level read as the mean of the team's current staff files another call (%d stay), ruled out by "
       "4.1 (a level that stays the same as staff come and go)" % len(SF1))
    tot = np.sqrt(np.diag(SigB) / (np.diag(SigB) + np.diag(d["SPW"])))
    ok(len(stays(E.paf(SigB) * tot)) == 0, "SF2 loadings standardised on the whole answer withdraw every item, ruled out "
                                           "by 4.2's standardisation across teams")
    w, v = np.linalg.eigh(SigB / np.sqrt(np.outer(np.diag(SigB), np.diag(SigB))))
    two = v[:, -2:] * np.sqrt(w[-2:])
    from numpy.linalg import svd
    # varimax of the two-factor solution: the climate factor is the one the practice items load on
    def varimax(L, it=200):
        p, k = L.shape
        Rm = np.eye(k)
        for _ in range(it):
            Lr = L @ Rm
            u, s, vt = svd(L.T @ (Lr ** 3 - Lr @ np.diag(np.diag(Lr.T @ Lr)) / p))
            Rm = u @ vt
        return L @ Rm
    rot = varimax(two)
    clim = np.argmax(np.abs(rot[E.ITEM_CODES.index("TC09")]))
    lc = np.abs(rot[:, clim])
    ok(all(lc[E.ITEM_CODES.index(c)] < 0.4 for c in C_ITEMS) and all(lc[:10] > 0.75),
       "SF3 a second team-level factor leaves TC11 and TC12 off the climate factor: same call")
    ok(all(abs(x - E.LINE) > 0.05 for x in X["golden"]), "SF4 no item within 0.05 of the 0.75 line: inclusive or not, "
                                                           "same call")
    cnt = R[R["complete"] & R["team"].notna()].groupby("team").size()
    rep5 = set(cnt[cnt >= 5].index)
    Rv = R.copy()
    Rv["used"] = Rv["team"].isin(rep5) & Rv["complete"]
    Y5, g5 = E.scores(Rv)
    ok(stays(E.loadings(Y5, g5, "muml_paf")) == golden_set, "SF5 teams counted on complete returns: same call")
    pr = R[R["reported"]]
    Yp = pr[E.ITEM_CODES].values.astype(float)
    gp = pr["team"].values
    mask = ~np.isnan(Yp)
    J = Yp.shape[1]
    S_pw, S_b = np.zeros((J, J)), np.zeros((J, J))
    for a in range(J):
        for b in range(J):
            mm = mask[:, a] & mask[:, b]
            dd = E.decompose(np.column_stack([Yp[mm, a], Yp[mm, b]]), gp[mm])
            sb = (dd["SB"] - dd["SPW"]) / dd["c"]
            S_b[a, b] = sb[0, 1] if a != b else sb[0, 0]
    ok(stays(E.paf((S_b + S_b.T) / 2)) == golden_set, "SF6 pairwise returns instead of complete ones: same call")
    Yb = (Y >= 4).astype(float)
    ok(stays(E.loadings(Yb, g, "muml_paf")) == golden_set, "SF7 answers scored favourable or not: same call")
    ok(True, "SF8 paper codes 8 and 9 read as answers: same call (asserted in R2)")
    ok(True, "SF9 a member's returns across channels: same call (asserted in R2)")
    ok(True, "SF10 a tablet's re-sent session: same call (asserted in R2)")
    ok(True, "SF11 July codes and the reissued codes, however joined: same call (asserted in R2)")
    for h in ("muml_paf", "muml_ml", "muml_pca"):
        ok(stays(lam[h]) == golden_set, "SF12 one-factor estimator %s: same call" % h)
    for h in ("unweighted", "crosshalf"):
        ok(stays(lam[h]) == golden_set, "SF13 between-team covariance estimator %s: same call" % h)
    sub = D["sessions"][D["sessions"]["status"] == "submitted"]
    ok(sub["submitted_utc"].max() < "2027-10-04T20:59:59Z",
       "SF14 the close read in UK time or in UTC: no submission within two hours of either, same returns, same call")
    late = pd.to_datetime(D["paper"]["scanned_at"]).dt.date > __import__("datetime").date(2027, 10, 8)
    ok(late.sum() > 0, "SF15 late forms exist in the scan file")
    ok(True, "SF15 the survey's returns with late forms kept: same call (asserted in R2)")
    ok(stays(-X["golden"]) == golden_set, "SF16 loadings read as magnitudes: same call")

    # ---------------------------------------------------------------- the asks: devices, stops and separation
    G = dict(ledger=X["ledger"], fav=X["fav"], div=X["div"])
    devices = {
        "S1 a member's earlier returns kept": dict(member=False),
        "S7 a tablet's re-sent sessions kept": dict(replay=False),
        "S2 tablet codes joined as they stand": dict(site_rule="raw"),
        "S2 paper codes joined as they stand": dict(paper_rule="raw"),
        "S2 every tablet code read through the map": dict(site_rule="map"),
    }
    moved = {k: set() for k in ("ledger", "fav", "div")}
    for name, kw in devices.items():
        Rv, rep = variant(D, **dict(kw))
        L = E.ledger(Rv)
        F = E.favourable(Rv)
        Dv = E.divisions(D, Rv)
        Yv, gv = E.scores(Rv)
        ok(stays(E.loadings(Yv, gv, "muml_paf")) == golden_set, "separation: %s leaves the call" % name)
        for ch in L:
            for f in L[ch]:
                if L[ch][f] != G["ledger"][ch][f]:
                    moved["ledger"].add((ch, f))
        for it in F:
            for f in ("base", "fav"):
                if F[it][f] != G["fav"][it][f]:
                    moved["fav"].add((it, f))
        for dv in Dv:
            for f in Dv[dv]:
                if Dv[dv][f] != G["div"][dv][f]:
                    moved["div"].add((dv, f))
    for rule in ("current", "prefix", "previous"):
        Dv = E.divisions(D, R, rule)
        for dv in Dv:
            for f in Dv[dv]:
                if Dv[dv][f] != G["div"][dv][f]:
                    moved["div"].add((dv, f))
    ok(len(moved["ledger"]) == 12, "ask 1: every channel figure moves under at least one device (%d of 12)"
       % len(moved["ledger"]))
    ok(len(moved["fav"]) == 24, "ask 2: every item's two counts move under at least one device (%d of 24)"
       % len(moved["fav"]))
    ok(len(moved["div"]) == 12, "ask 3: every division figure moves under at least one device (%d of 12)"
       % len(moved["div"]))
    # the stops of ask 2: the check's own returns; don't know in the base
    used = R[R["used"]]
    for it in E.ITEM_CODES:
        v = used[it].dropna()
        ok(len(v) != G["fav"][it]["base"] and int((v >= 4).sum()) != G["fav"][it]["fav"],
           "ask 2 stop: the check's returns alone give other counts for %s" % it)

    # ---------------------------------------------------------------- documents and pins
    std = _pdf_text(os.path.join(target, X["files"]["standard"]))
    ok("a member of the team is expected to give" in std and std.count("0.75") == 2,
       "the standard files the team level once and the line in 4.3 only")
    ok("five or more returns that count" in std, "the standard files the reporting floor")
    ok("the return received last counts" in std, "the standard files the member rule")
    ok(not re.search(r"team mean|between-team|within-team|pooled|multilevel|two-level|MUML", std, re.I),
       "the standard names no estimator")
    note = _docx_text(os.path.join(target, X["files"]["note"]))
    ok("1 September 2027" in note and "every return that counts" in note, "the dashboard note files the ask organs")
    ok("factor" not in note and "loading" not in note, "the dashboard note carries nothing the call reads")
    close = _docx_text(os.path.join(target, X["files"]["close"]))
    ok(not re.search(r"twice|duplicate|team list|re-sent|resent|sync", close, re.I), "the close-out narrates no device")

    # ---------------------------------------------------------------- input gates and realism
    files = os.listdir(target)
    ok(len(files) >= 10 and len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gates: files and formats")
    big = max(sum(1 for _ in open(os.path.join(target, f))) for f in files if f.endswith(".csv"))
    ok(big >= 25000, "input gates: a file of 25,000 rows or more (%d)" % big)
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2, "input gates: two distractors declared")
    for f in meta["distractor_files"]:
        ok(not re.search("distract", f), "distractor %s not named as one" % f)
    ok(sorted(os.listdir(golden)) == sorted(["lfp_tci_items_2028.pptx", "lfp_tci_structure_check_2027.xlsx"]),
       "golden: the two deliverables")
    tot = sum(v["count"] for v in G["ledger"].values())
    ok(tot % 100 != 0 and tot % 50 != 0, "realism: the returns total is not round (%d)" % tot)
    for ch, v in G["ledger"].items():
        ok(len(set(v.values())) == 4, "realism: %s ledger figures distinct" % ch)
    ok(len({v["teams"] for v in G["div"].values()}) == 6, "realism: division team counts distinct")
    S = D["sessions"]
    ok(S["session_id"].is_unique and S["started_utc"].min() >= "2027-09-06T07:00:00Z", "sessions start at the opening")
    sub = S[S["status"] == "submitted"]
    ok(sub["submitted_utc"].max() <= "2027-10-04T22:59:59Z", "no submission after the close")
    gap = S[(S["link_type"] == "site") & (S["started_utc"] >= "2027-09-13T05:00:00Z")
            & (S["started_utc"] < "2027-09-13T06:20:00Z")]
    ok(len(gap) == 0, "no tablet session while the tablets were offline on 13 September")
    return N[0]
