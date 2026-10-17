"""task237 checks: the three rules executed on the simulator's clean truth (R1 to R3c), every semantic fork row (SF1 to
SF12), the golden against the generating model with its margins, the rungs, the ask devices and their stops, the
separation of the call from the devices, the documents' pins, the input gates and the realism sweep."""
import datetime as dt
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

import estim as E
import params as P
import sim

N = [0]
GOLD = {"pa": "release", "zh-Hans": "hold", "yue": "rework", "tl": "hold", "ar": "hold", "es": "release",
        "ur": "rework", "vi": "rework", "fa": "release", "ko": "hold"}
DEFAULT = {"pa": "release", "zh-Hans": "release", "yue": "hold", "tl": "release", "ar": "release", "es": "release",
           "ur": "rework", "vi": "release", "fa": "release", "ko": "release"}       # alpha: six wrong
WORDING = {"zh-Hans", "yue", "tl", "ar", "vi", "ko"}
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _pdf_text(path):
    from pypdf import PdfReader
    return " ".join(" ".join(pg.extract_text().split()) for pg in PdfReader(path).pages)


def bands(d):
    return {v: E.band(x) for v, x in d.items()}


def wrong(d):
    return {v for v in E.ORDER if d[v] != GOLD[v]}


# ------------------------------------------------------------------ the clean truth: the world before any record
def clean(W):
    """each version's valid completes straight from the simulator (keyed answers, unanswered items blank), no file"""
    R = W.respondents
    out = {}
    for v in E.ORDER:
        t = R[(R.version == v) & R.kind.isin(sim.VALID)]
        X = np.vstack(t.X.values).astype(float)
        X[np.vstack(t.miss.values)] = np.nan
        out[v] = X
    return out


def stats(X):
    S, n = E.full_answer_cov(X)
    ts = E.trait_share(S)
    return dict(n=n, golden=ts["share"], common=ts["common"], cu=E.trait_share_cu(S), moments=E.trait_share_moments(S),
                alpha=E.alpha(S), one_factor=E.one_factor(S), positive_only=E.one_factor(S[np.ix_(E.POS, E.POS)]))


def uls_share(S):
    """the bifactor model fitted by unweighted least squares instead of maximum likelihood"""
    idx = np.argwhere(np.c_[np.ones(12, bool), np.isin(np.arange(12), E.NEG)])

    def unpack(x):
        L = np.zeros((12, 2)); L[idx[:, 0], idx[:, 1]] = x
        return L
    f = lambda x: (((S - unpack(x) @ unpack(x).T) * (1 - np.eye(12))) ** 2).sum()
    L = unpack(minimize(f, np.full(len(idx), 0.4), method="L-BFGS-B").x)
    L[:, 0] *= np.sign(L[:, 0].sum()); L[:, 1] *= np.sign(L[:, 1].sum())
    th = np.diag(S) - (L ** 2).sum(axis=1)
    g, w = L[:, 0].sum(), L[:, 1].sum()
    return g ** 2 / (g ** 2 + w ** 2 + th.sum())


def run(target, golden, o, X):
    N[0] = 0
    W = o["W"]
    D = X["D"]
    import build as B
    files = {k: os.path.join(target, f) for k, f in B.FILES.items()}
    std = _pdf_text(files["std"])
    man = _pdf_text(files["manual"])
    dic = open(files["dict"]).read()
    dicf = " ".join(dic.split())
    rel, calls = X["rel"], X["calls"]
    shares = {v: rel[v]["golden"] for v in E.ORDER}

    # ------------------------------------------------------------ the golden
    ok(calls == GOLD, "golden: %s" % calls)
    ok(bands({v: W.truth[v]["trait_share"] for v in E.ORDER}) == GOLD,
       "golden: the generating model's own trait shares put every version in the same band")
    ok(all(abs(shares[v] - W.truth[v]["trait_share"]) < 0.06 for v in E.ORDER),
       "golden: every estimate within 0.06 of the generating model's share (five-point answers attenuate it)")
    edge = min(abs(shares[v] - e) for v in E.ORDER for e in (0.70, 0.80))
    ok(edge >= 0.035, "golden: every version 0.035 or more from a band edge (%.3f)" % edge)
    ok({v for v in E.ORDER if P.VERSIONS[E.ORDER.index(v)][6] > 0} == WORDING,
       "golden: the six wording-affected versions are the six whose translation carries a wording factor")

    # ------------------------------------------------------------ R1: the field's raw material ships, no deciding column
    banned = re.compile(r"reliab|alpha|omega|factor|decision|release|share|score|loading", re.I)
    for k in ("online", "ledger", "para", "capi", "bc", "wave5"):
        cols = pd.read_csv(files[k], nrows=1).columns
        ok(not [c for c in cols if banned.search(c) and c != "mean_score"],
           "R1 no column of %s holds a reliability, a factor or a decision" % B.FILES[k])
    ok(set(D["reg"].columns) == {"version", "language", "mode", "vendor", "forward_translators",
                                 "back_translation_reviewed", "reconciled", "pretest", "pilot_start", "pilot_end", "note"},
       "R1 the register records the translation process and the pilot dates only")
    ok(len(D["capi"]) >= 25_000 and len(D["online"]) > 3_000,
       "R1 the vendors' answers ship item by item (%d CAPI rows, %d online entries)" % (len(D["capi"]), len(D["online"])))

    # ------------------------------------------------------------ R3a: the analyst test on the clean truth
    T = clean(W)
    ts = {v: stats(T[v]) for v in E.ORDER}
    ok(bands({v: ts[v]["alpha"] for v in E.ORDER}) == DEFAULT, "R3a alpha on the clean truth files the default answer")
    ok(wrong(bands({v: ts[v]["alpha"] for v in E.ORDER})) == WORDING, "R3a alpha files the six wording versions wrong")
    ok(bands({v: ts[v]["one_factor"] for v in E.ORDER}) == DEFAULT, "R3a omega from a single factor: the same answer")
    ok(bands({v: rel[v]["alpha"] for v in E.ORDER}) == DEFAULT, "R3a alpha on the pack: the same answer")
    ok(min(abs(ts[v][k] - e) for v in E.ORDER for k in ("alpha", "one_factor") for e in (0.70, 0.80)) >= 0.02,
       "R3a alpha and the single-factor omega 0.02 or more from every band edge")
    # ------------------------------------------------------------ R3b: the decisive step alone, and the other rungs
    ok(bands({v: ts[v]["golden"] for v in E.ORDER}) == GOLD, "R3b the trait's share on the clean truth: the golden")
    ok(wrong(bands({v: ts[v]["common"] for v in E.ORDER})) == WORDING,
       "R3b omega total from the bifactor model (all common variance) files the six wording versions wrong")
    pos_wrong = wrong(bands({v: ts[v]["positive_only"] for v in E.ORDER}))
    ok(pos_wrong >= {"pa", "zh-Hans", "tl", "vi"} and len(pos_wrong) <= 5,
       "rungs: the positively worded items alone file %s wrong" % sorted(pos_wrong))
    ok(all(ts[v]["common"] - ts[v]["golden"] > 0.10 for v in WORDING)
       and all(abs(ts[v]["common"] - ts[v]["golden"]) < 0.04 for v in set(E.ORDER) - WORDING),
       "rungs: the wording factor carries 0.10 or more of the score's variance in the six, under 0.04 elsewhere")

    # ------------------------------------------------------------ R2: each mess item leaves the call where it is
    for name, kw in list(E.STOPS.items()) + [("all mess at once", dict(retakes=True, switchers=True, inside=True,
                                                                         pretest=True, unconfirmed=True, no_window=True,
                                                                         status_only=True, result_only=True,
                                                                         case_join=True))]:
        r2 = E.reliability(E.completes(D, **kw))
        ok(bands({v: r2[v]["golden"] for v in E.ORDER}) == GOLD, "R2 %s: same call" % name)

    # ------------------------------------------------------------ the semantic fork table, every row
    df = X["df"]
    pw = {}
    for v in E.ORDER:
        Xv = pd.DataFrame(E.item_scores(df[df.version == v]))
        pw[v] = E.trait_share(Xv.cov().to_numpy())["share"]
    ok(bands(pw) == GOLD and "who answered all twelve items" in std,
       "SF1 every valid complete's answered items (pairwise covariances): same call; s.6 pins the full answerers")
    ordn = E.ordinal_share(df)
    ok(bands(ordn) == GOLD, "SF2 polychoric correlations instead of covariances: same call")
    ok(bands({v: rel[v]["cu"] for v in E.ORDER}) == GOLD and bands({v: rel[v]["moments"] for v in E.ORDER}) == GOLD,
       "SF3 correlated residuals among the negatively worded items, or the moment estimator: same call")
    uls = {v: uls_share(E.full_answer_cov(E.item_scores(df[df.version == v]))[0]) for v in E.ORDER}
    ok(bands(uls) == GOLD, "SF4 unweighted least squares instead of maximum likelihood: same call")
    ok(all(abs(x - e) >= 0.02 for d in (ordn, uls, {v: rel[v]["cu"] for v in E.ORDER}) for x in d.values()
           for e in (0.70, 0.80)), "SF2 to SF4 every alternative estimate 0.02 or more from a band edge")
    ok("compared unrounded" in std, "SF5 the comparison is unrounded (s.6)")
    ok("the twelve items formed a single factor" in man and "The BCS-12 measures connectedness" in man,
       "SF6 connectedness is the source version's single factor (manual s.1, s.4)")
    wt = X["wording"]
    ok(all(wt[v]["p"] > 0.05 for v in set(E.ORDER) - WORDING) and all(wt[v]["p"] < 1e-15 for v in WORDING),
       "SF6 a single factor fits the four other versions (p over 0.05) and fails in the six (p under 1e-15)")
    ok("the item score is 6 minus the answer" in std and "BCS02, BCS04, BCS06, BCS08, BCS10 and BCS12" in std,
       "SF7 the total score as scored: the six negatively worded items reversed (s.5)")
    ok("prefer not to say, don't know or refused leaves the item unanswered" in std,
       "SF8 codes 9, -8 and -9 leave the item unanswered (s.5, the codebook)")
    ok("0.80 or more" in std and "0.70 to under 0.80" in std and "under 0.70" in std, "SF9 the bands' edges (s.6)")
    ok(all(v in E.ORDER for v in calls) and len(calls) == 10, "SF10 each version gated on its own pilot")
    gpe = {v: E.trait_share(np.cov(E.item_scores(df[df.version == v])[~np.isnan(E.item_scores(df[df.version == v])).any(axis=1)],
                                   rowvar=False, ddof=0))["share"] for v in E.ORDER}
    ok(bands(gpe) == GOLD, "SF11 the covariance divided by n or n - 1: same call")
    ok(not re.search(r"alpha|omega|factor|model|coefficient|Cronbach|correlat", std, re.I),
       "SF12 the standard names no coefficient or model: the estimation is the analysis")

    # ------------------------------------------------------------ the asks: fair, devices, stops
    R = W.respondents
    tA = {v: int(((R.version == v) & R.kind.isin(sim.VALID)).sum()) for v in E.ORDER}
    ok(tA == X["counts"], "ask A fair: the golden equals the world's valid completes")
    tB = {v: float(np.nanmean(E.total_scores(T[v]))) for v in E.ORDER}
    ok(all(abs(tB[v] - X["means_raw"][v]) < 1e-9 for v in E.ORDER), "ask B fair: the golden equals the world's mean scores")
    gA, gB, A, Bs = E.ask_stops(D)
    ncp = [v for v in E.ORDER if X["vendor"][v] == P.VENDORS["NCP"][0]]
    flr = [v for v in E.ORDER if v not in ncp]
    prim = "partials past the module dropped (vendor status)"
    ok(all(A[prim][v] < gA[v] for v in E.ORDER), "ask A primary: the vendors' status drops partials past the module, every version low")
    ok(all(Bs[prim][v] != gB[v] for v in E.ORDER), "ask B primary: the same moves every version's mean")
    ok(all(A["back-check joined by case"][v] < gA[v] for v in flr) and all(Bs["back-check joined by case"][v] != gB[v] for v in flr),
       "ask A and B secondary: the back-check joined by case drops each reissued case's replacement, every CAPI version")
    ok(all(A["merged accounts kept apart"][v] > gA[v] for v in ncp),
       "ask A secondary: merged accounts kept apart count each second account's completion, every online version")
    crack = E.completes(D, status_only=True, result_only=True, case_join=True)
    cA, cB = E.valid_counts(crack), E.mean_scores(crack)
    ok(all(cA[v] != gA[v] and cB[v] != gB[v] for v in E.ORDER), "cracker: the textbook path misses all twenty ask figures")
    for name in ("online dates read in UTC", "no window for the online pilots", "retakes counted", "switchers counted"):
        ok(all(A[name][v] != gA[v] for v in ncp), "ask A hazard: %s moves every online version" % name)
    for name in ("pretest interviews counted", "unconfirmed interviews counted", "unreached back-checks dropped"):
        ok(all(A[name][v] != gA[v] for v in flr), "ask A hazard: %s moves every CAPI version" % name)
    ok(all(A["partials inside the module counted"][v] > gA[v] for v in E.ORDER), "ask A hazard: partials inside the module")
    ok(all(Bs["no prorating"][v] - gB[v] >= 0.25 for v in E.ORDER), "ask B hazard: no prorating, every version 0.25 or more high")
    ok(sum(Bs["missing codes read as answers"][v] != gB[v] for v in E.ORDER) >= 9, "ask B hazard: missing codes read as answers")
    ok(all(0.0015 <= 0.005 - abs(((X["means_raw"][v] * 100) % 1) - 0.5) / 100 for v in E.ORDER),
       "ask B: every mean 0.0015 or more from a two-decimal rounding edge")
    # the devices are how the records come to exist
    on = D["online"]
    past = on[(on.status == "partial") & (on[E.CODES] != "").all(axis=1)]
    ok(len(past) >= 60 and (past[["sex", "hh_size", "yrs_in_canada"]] == "").any(axis=1).all()
       and (past.ui_language_at_end.str.lower() == past.survey_code.str.replace("CCS6-BCS-", "").str.lower()).all(),
       "device: %d online partials reached the end of the module and left in the background questions" % len(past))
    w = E.capi_interviews(D)
    ok(((w.RESULT == "2") & w[E.CODES].notna().all(axis=1)).sum() >= 20 and ((w.RESULT == "2") & w[E.CODES].isna().any(axis=1)).sum() >= 10,
       "device: CAPI partial interviews both past and inside the module")
    dup = w.groupby("case_id").filter(lambda g: len(g) > 1)
    ok(dup.groupby("case_id").interviewer_id.nunique().eq(2).all() and dup.groupby("case_id").size().eq(2).all(),
       "device: every case with two interviews has them from two interviewers")
    bc = D["bc"]
    srt = dup.sort_values(["case_id", "interview_date"])
    first = srt.drop_duplicates("case_id", keep="first").set_index("case_id")
    second = srt.drop_duplicates("case_id", keep="last").set_index("case_id")
    nc = bc[bc.outcome == "not confirmed"].set_index("case_id")
    reiss = [c for c in first.index if c in nc.index and nc.loc[c, "interviewer_id"] == first.loc[c, "interviewer_id"]]
    revis = [c for c in first.index if c not in reiss]
    ok(len(reiss) >= 40 and all(first.loc[c, "interview_date"] < nc.loc[c, "backcheck_date"] < second.loc[c, "interview_date"]
                                for c in reiss),
       "device: %d reissued cases, each after a not-confirmed back-check of the first interviewer" % len(reiss))
    ok(len(revis) >= 15 and all(first.loc[c, "RESULT"] == "2" and first.loc[c, E.CODES].isna().any() for c in revis),
       "no marker: %d other cases with two interviews, each revisited after a break-off inside the module" % len(revis))
    led = D["ledger"]
    mg = led[led.outcome == "merged"]
    root = E.surviving_member(led)
    comp = led[led.outcome == "complete"]
    second_acc = comp[comp.panel_member_id.isin(mg.panel_member_id)]
    dev = second_acc.assign(into=second_acc.panel_member_id.map(root))
    hits = dev.merge(comp, left_on=["into", "survey_code"], right_on=["panel_member_id", "survey_code"], suffixes=("", "_a"))
    ok(len(hits) >= 20 and (hits.activity_utc_a < hits.activity_utc).all(),
       "device: %d second accounts completed a version their first account had completed earlier" % len(hits))
    benign = mg[~mg.panel_member_id.isin(comp.panel_member_id)]
    ok(len(benign) >= len(hits), "no marker: %d merges of accounts with no completion beside the %d device merges" % (len(benign), len(hits)))
    ed = E.eastern_date(on.start_utc)
    soft = on[ed < P.PILOT["NCP"][0].isoformat()]
    ok(len(soft) >= 50 and (ed[soft.index] == (P.PILOT["NCP"][0] - dt.timedelta(days=1)).isoformat()).all()
       and (soft.start_utc.str[:10] == P.PILOT["NCP"][0].isoformat()).mean() > 0.6,
       "device: %d soft-launch entries the evening before the pilot, most dated the first day in UTC" % len(soft))
    ends = on[on.end_utc != ""]
    ok((E.eastern_date(ends.start_utc) == E.eastern_date(ends.end_utc)).all(),
       "SF13 every online entry starts and ends on the same Eastern date: the window reads the same by either")
    mem = led[led.respondent_id != ""].set_index("respondent_id").panel_member_id
    o2 = on[on.status == "complete"].assign(member=lambda d: d.respondent_id.map(mem).map(root)).sort_values("start_utc")
    rep = [g for _, g in o2.groupby(["survey_code", "member"]) if len(g) > 1]
    ok(len(rep) >= 100 and all((g.start_utc.iloc[1:].values > g.end_utc.iloc[:-1].values).all() for g in rep),
       "SF14 a member's later completion starts after the earlier one ends (%d members): first by start or by end alike" % len(rep))
    ok(not re.search(r"partial|status|reissue|merge|soft|UTC|account", std, re.I),
       "ban 1: the standard names no status, reissue, merge, soft launch or clock")
    # ------------------------------------------------------------ separation: the asks' devices never move the call
    rc = E.reliability(crack)
    ok(bands({v: rc[v]["golden"] for v in E.ORDER}) == GOLD, "separation: the cracker's population gives the same call")

    # ------------------------------------------------------------ the documents
    ok(not re.search(r"wording factor|method factor|bifactor|negation|response style", man + std, re.I),
       "the manual and the standard name no wording factor")
    notes = " ".join(D["reg"].note)
    ok(not re.search(r"negat|wording factor|reverse", notes, re.I), "the register's notes name no wording effect")
    neg_notes = [v for v, t in zip(D["reg"].version, D["reg"].note)
                 if re.search(r"[Ii]tem (2|4|6|8|10|12)\b", t)]
    ok(set(neg_notes) and not set(neg_notes) & WORDING, "the notes on negatively worded items sit in versions with no wording factor")
    ok("the panel merges a second account it finds a member holding" in dicf,
       "the dictionary describes the panel's merges flatly")
    ok("the interviewer whose interview was checked" in dicf, "the dictionary describes the back-check log's interviewer")

    # ------------------------------------------------------------ R3c, input gates, dates
    names = os.listdir(target)
    ok(len(names) >= 10 and len({f.rsplit(".", 1)[1] for f in names}) >= 3,
       "input gates: %d files, formats %s" % (len(names), sorted({f.rsplit(".", 1)[1] for f in names})))
    ok(max(sum(1 for _ in open(os.path.join(target, f))) for f in names if f.endswith(".csv")) >= 25_001,
       "input gate: a file of 25,000 rows or more")
    ok(on.start_utc.max() < P.EXPORT_UTC.strftime("%Y-%m-%dT%H:%M:%SZ") and led.activity_utc.max() < P.EXPORT_UTC.strftime("%Y-%m-%dT%H:%M:%SZ"),
       "no online entry or ledger row after the vendors' export")
    ok(D["capi"].interview_date.max() <= P.PILOT["FLR"][1].isoformat() and bc.backcheck_date.max() < P.AS_OF.isoformat(),
       "no interview after the CAPI pilot, no back-check after the sign-off")
    for f in B.DISTRACTORS:
        ok(os.path.exists(files[f]), "distractor %s ships; the golden and both asks read none of it" % B.FILES[f])
    for path in (os.path.join(os.path.dirname(target), x) for x in ("submission.md", "DESIGN_NOTE.md", "prompt.txt")):
        if os.path.exists(path):
            ok("\u2014" not in open(path).read() and "\u2013" not in open(path).read(), "no em or en dash in %s" % os.path.basename(path))
    for f in names:
        if f.endswith((".md", ".csv")):
            ok("\u2014" not in open(os.path.join(target, f)).read(), "no em dash in %s" % f)
    prof = {v: tuple(np.round(np.nanmean(T[v], axis=0), 3)) for v in E.ORDER}
    ok(len(set(prof.values())) == 10, "R3c no two versions share an item profile")

    # ------------------------------------------------------------ the pack's own registers (H9)
    readme = open(files["readme"]).read()
    listed = set(re.findall(r"`([^`]+\.(?:csv|xlsx|pdf|md))`", readme))
    ok(listed == set(names) - {"README.md"}, "H9 the readme lists every shipped file and nothing else")
    data_files = {f for f in names if f.endswith((".csv", ".xlsx"))}
    ok(data_files == set(re.findall(r"^## (\S+\.(?:csv|xlsx))$", dic, re.M)), "H9 the dictionary describes every data file")
    path = os.path.join(os.path.dirname(target), "submission.md")
    if os.path.exists(path):
        cited = set(re.findall(r"[\w.-]+\.(?:csv|xlsx|pdf)", open(path).read())) - {"bcs12_wave6_release_decisions.csv"}
        ok(cited <= set(names), "H8 every file the write-up cites ships: %s" % sorted(cited - set(names)))

    # ------------------------------------------------------------ realism sweep
    for k in ("online", "ledger", "para", "capi", "bc"):
        dfk = D[k]
        const = [c for c in dfk.columns if dfk[c].nunique() == 1]
        ok(not const, "realism: no constant column in %s (%s)" % (B.FILES[k], const))
    days = pd.Series(E.eastern_date(on.start_utc)).value_counts().values
    ok(len(set(days)) > 0.6 * len(days), "realism: daily online entries vary")
    ok(sum(X["counts"].values()) % 10 and X["entries"] % 10 and X["interviews"] % 10,
       "realism: no round headline total (%d valid completes, %d entries, %d interviews)" %
       (sum(X["counts"].values()), X["entries"], X["interviews"]))
    card = json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task237.json")))
    ok(set(P.PEOPLE.values()) == set(card["world"]["people"]), "realism: every persona drawn by guard.py names")
    scrub = os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    for folder in (target, golden):
        out = subprocess.run([sys.executable, scrub, folder], capture_output=True, text=True).stdout
        ok("clean, no producer signature" in out, "realism: containers scrubbed in %s" % os.path.basename(folder))
    return N[0]
