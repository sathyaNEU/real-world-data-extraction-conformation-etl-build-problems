"""task249's generator checks: the input gates, the three rules (R1 to R3), the fork rows, the convergence of the
methods the data leaves open, the asks' devices and bins, and the realism sweep.

    python3 checks.py [target]"""
import json
import os
import sys
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build as B
import params as P
import solve as S
import pair as PR

FAIL = []


def ok(label, cond, info=""):
    print(("PASS " if cond else "FAIL ") + label + ("  " + str(info) if info else ""))
    if not cond:
        FAIL.append(label)


def flags_of(df, col="gold"):
    return set(df.loc[df[col] > P.CAP, "code"])


def variant(L, **kw):
    """the main call with one handling changed"""
    import copy
    L2 = dict(L)
    for k, v in kw.items():
        L2[k] = v
    return S.main_call(L2)[0]


def main(tgt):
    files = B.FILES
    L = S.load(tgt, files)
    df, rt, st = S.main_call(L, extra=True)
    gold = flags_of(df)
    fig = json.load(open(os.path.join(HERE, "figures.json")))

    # ---------------------------------------------------------------- input gates
    names = sorted(os.listdir(tgt))
    ok("G1 ten or more files", len(names) >= 10, len(names))
    ok("G2 three or more formats", len({n.rsplit(".", 1)[1] for n in names}) >= 3, sorted({n.rsplit(".", 1)[1] for n in names}))
    nrow = len(pd.read_parquet(os.path.join(tgt, files["exposure"]), columns=["item_id"]))
    ok("G3 a file of 25,000 rows or more", nrow >= 25000, nrow)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("G4 two distractors named and shipped", len(meta["distractors"]) >= 2 and all(d["file"] in names for d in meta["distractors"]))
    for d in meta["distractors"]:
        ok("G5 distractor %s unused by the solver" % d["file"], d["file"] not in open(os.path.join(HERE, "solve.py")).read())

    # ---------------------------------------------------------------- the call
    ok("C0 golden flags 15 accounts", len(gold) == 15, sorted(gold))
    margin = float((df["gold"] - P.CAP).abs().min())
    ok("C1 every account at least 4 points from the cap", margin >= 0.04, round(margin, 4))
    ok("C2 flagged at least 20 per cent, kept at most 11", df.loc[df.flag, "gold"].min() >= 0.20 and df.loc[~df.flag, "gold"].max() <= 0.11,
       (round(df.loc[df.flag, "gold"].min(), 4), round(df.loc[~df.flag, "gold"].max(), 4)))
    ok("C3 empirical pool (no deconvolution) gives the same list", flags_of(df, "emp_pool") == gold)
    ok("C4 empirical pool keeps the component bounds", df.loc[df.flag, "emp_pool"].min() >= 0.20 and df.loc[~df.flag, "emp_pool"].max() <= 0.11,
       (round(df.loc[df.flag, "emp_pool"].min(), 4), round(df.loc[~df.flag, "emp_pool"].max(), 4)))
    ok("C5 figures.json carries the golden list", set(fig["call"]["flagged"]) == gold)
    ok("C6 the full posterior per pool member (Table 4.3's error at each ability) files the same list", flags_of(df, "posterior") == gold,
       (round(df.loc[df.flag, "posterior"].min(), 4), round(df.loc[~df.flag, "posterior"].max(), 4)))
    ok("C7 true-score shrinkage with Table 4.3 read at the shrunken ability files the same list", flags_of(df, "kelley_ability") == gold,
       (round(df.loc[df.flag, "kelley_ability"].min(), 4), round(df.loc[~df.flag, "kelley_ability"].max(), 4)))

    # ---------------------------------------------------------------- R1 the field's raw material ships
    att = pd.read_parquet(os.path.join(tgt, files["attempts"]))
    ok("R1a per-sitting MAT-R estimates with standard errors ship", {"theta_logit", "se_logit"} <= set(att.columns))
    stu = pd.read_csv(os.path.join(tgt, files["study"]))
    ok("R1b study pairs carry both tests' estimates, errors and dates", {"mat_r_logit", "mat_r_se", "mat_v_logit", "mat_v_se", "mat_r_started_ist", "mat_v_started_ist"} <= set(stu.columns))
    banned = ("referral_share", "referral_rate", "projected", "regress", "shrink")
    cols = []
    for n in names:
        if n.endswith(".csv"):
            cols += list(pd.read_csv(os.path.join(tgt, n), nrows=1).columns)
        if n.endswith(".parquet"):
            cols += list(pd.read_parquet(os.path.join(tgt, n)).columns)
    ok("R1c no shipped column holds the deciding quantity", not any(any(b in c.lower() for b in banned) for c in cols))

    # ---------------------------------------------------------------- R3 the analyst test, the decisive step alone
    ok("R3a the study's rates by interval flag none of the 15", not (flags_of(df, "study_rate") & gold), sorted(flags_of(df, "study_rate")))
    ok("R3a the study's regression of MAT-V on MAT-R carried to each shortlist flags none", not flags_of(df, "study_reg"), sorted(flags_of(df, "study_reg")))
    ok("R3b the model without the retest gain adds NVK, UJB, OJS", flags_of(df, "no_gain") - gold == {"NVK", "UJB", "OJS"}, sorted(flags_of(df, "no_gain") - gold))
    ok("R3b one constant MAT-R error leaves KSP, VRD, ABH off", gold - flags_of(df, "const_se") == {"KSP", "VRD", "ABH"}, sorted(gold - flags_of(df, "const_se")))
    nr = df.loc[df.code.isin(["NVK", "UJB", "OJS"]), "no_gain"].min()
    cs = df.loc[df.code.isin(["KSP", "VRD", "ABH"]), "const_se"].max()
    ok("R3b the partial routes miss by at least 2.5 points", nr >= P.CAP + 0.025 and cs <= P.CAP - 0.025, (round(nr, 4), round(cs, 4)))
    ok("R3b shrinkage with each candidate's reported error (at the estimate) adds NVK, UJB, OJS",
       flags_of(df, "kelley_reported") - gold == {"NVK", "UJB", "OJS"} and not (gold - flags_of(df, "kelley_reported")),
       sorted(flags_of(df, "kelley_reported") - gold))
    kr = df.loc[df.code.isin(["NVK", "UJB", "OJS"]), "kelley_reported"].min()
    ok("R3b the reported-error route misses by at least 2.5 points", kr >= P.CAP + 0.025, round(kr, 4))
    sk = S.shrinkage_check(rt)
    ok("F2 the study's top tenth: shrinkage at the ability within 0.02 logit of the MAT-V scored",
       abs(sk["at_ability"] - sk["scored"]) <= 0.02, (sk["n"], round(sk["scored"], 3), round(sk["at_ability"], 3)))
    ok("F2 the study's top tenth: shrinkage at the reported error at least 0.08 logit too low",
       sk["scored"] - sk["at_reported"] >= 0.08, round(sk["scored"] - sk["at_reported"], 3))

    # ---------------------------------------------------------------- R2 every Layer 1 item neutral to the call
    sh = L["shares"]
    v1 = variant(L, shares=sh[sh["account_code"] != "PGL"])
    ok("R2a PGL left unfolded (NVK without its July and August campuses): same list", flags_of(v1) == gold)
    v2 = variant(L, shares=sh[sh["share_status"] == "active"])
    ok("R2b withdrawn shares left out of the pools: same list", flags_of(v2) == gold)
    a2 = att.copy()
    a2["theta_logit"] = (a2["scale_score"].astype(float) - 50.0) / 10.0
    v3 = variant(L, att=a2)
    ok("R2c whole-number scale scores read back to logits: same list", flags_of(v3) == gold)
    reg = L["reg"]
    cases = pd.read_excel(os.path.join(tgt, files["cases"]), sheet_name="Case log")
    bad = set(cases.loc[cases["finding"] == "confirmed impersonation", "candidate_id"])
    v4 = variant(L, shares=sh[~sh["candidate_id"].isin(bad)])
    ok("R2d 2028 confirmed impersonations taken out of the pools: same list", flags_of(v4) == gold)
    v5 = variant(L, keep_dupes=True)
    ok("R2g the 14 August re-send's repeated shares counted twice in the pools: same list", flags_of(v5) == gold)
    suite = set(att["candidate_id"]) - set(reg["candidate_id"])
    ok("R2e the synthetic suite's identities hold no share (outside every pool)", not (suite & set(sh["candidate_id"])), len(suite))
    ok("R2f interrupted attempts carry no estimate (outside every pool)", att.loc[att["attempt_status"] == "interrupted", "theta_logit"].isna().all())

    # ---------------------------------------------------------------- the semantic fork table, one assertion a row
    ok("SF1 PGL's 2028 campuses inside NVK's pool or left out: same list", flags_of(v1) == gold)
    ok("SF2 2028 confirmed impersonations kept in or taken out of the pools: same list", flags_of(v4) == gold)
    import datetime as _dt
    seu, sev = S.se_table()
    gain = S.gain_fn(rt)
    po, pl = S.pools(L), S.plan_rows(L)
    sl28 = pd.read_csv(os.path.join(tgt, files["shortlists"]))
    sl28["account_code"] = sl28["account_code"].replace({"PGL": "NVK"})
    cw = [_dt.date(2029, 7, 2), _dt.date(2029, 7, 9), _dt.date(2029, 7, 16), _dt.date(2029, 7, 23)]
    sf3, sf5, sf8 = {}, {}, {}
    for code, *_ in P.ACCOUNTS:
        row = pl.loc[code]
        q = float(row["Shortlist"]) / float(row["Expected applicants"])
        rng = np.random.default_rng(P.SEED + 701 + sum(map(ord, code)))
        gaps = S.gaps_for(row, rng, 4000, cw)
        q28 = sl28.loc[sl28["account_code"] == code, "candidate_id"].nunique() / len(po[code])
        sf3[code] = S.rate(po[code], q28, gaps, rng, gain, seu, sev, n=400000)
        # SF5: a two-sided band (MAT-R outside the band either way)
        e, s_ = po[code]["theta_logit"].values, po[code]["se_logit"].values
        th = rng.normal(e.mean(), np.sqrt(max(e.var() - np.mean(s_ ** 2), 0.01)), 400000)
        U = th + rng.normal(0, 1, len(th)) * S.interp(th, seu)
        sel = U >= np.quantile(U, 1 - q)
        V = th + gain(rng.choice(gaps, len(th))) + rng.normal(0, 1, len(th)) * S.interp(th, sev)
        sf5[code] = float((np.abs(U - V) > P.BAND_Z * S.interp(V, sev))[sel].mean())
        # SF8: the day-one drives' interval read as one or two days; the later drives at the study's six-week band
        if row["Selection format"] in ("Day-one campus drive", "First-company campus drive"):
            g2 = np.where(rng.random(4000) < 0.5, 1, 2)
        else:
            g2 = np.full(4000, 42)
        sf8[code] = S.rate(po[code], q, g2, rng, gain, seu, sev, n=400000)
    ok("SF3 the 2028 shortlist depth in place of the 2029 plan's: same list", {c for c, v in sf3.items() if v > P.CAP} == gold)
    ok("SF4 withdrawn shares left out of the pools: same list", flags_of(v2) == gold)
    ok("SF5 a two-sided band in place of s.3.2's 'above': same list", {c for c, v in sf5.items() if v > P.CAP} == gold)
    ok("SF6 no account within 5 points of the cap, so 'more than' against 'at least' cannot move one", margin >= 0.05, round(margin, 4))
    ok("SF7 the check is the 12-item MAT-V: Table 4.3's MAT-V column is the one the solver reads",
       abs(float(S.interp(np.array([0.0]), sev)[0]) - float(P.se_verify(0.0))) < 0.002)
    ok("SF8 day-one intervals of one or two days, later drives at the six-week band: same list", {c for c, v in sf8.items() if v > P.CAP} == gold)
    ok("SF9 whole-number scale scores read back to logits: same list", flags_of(v3) == gold)
    ok("SF10 the estimates taken as abilities (no deconvolution): same list", flags_of(df, "emp_pool") == gold)

    # ---------------------------------------------------------------- the retest gain: fits the data leaves open converge
    d = rt["pairs"]
    g2_mean = float(d.loc[d["days"] <= 3, "gain"].mean())
    ok("F1 the gain within three days by plain mean against the fit at two days within 0.03", abs(g2_mean - (rt["c"] + rt["a"] * np.exp(-2 / rt["tau"]))) <= 0.03, round(g2_mean, 3))

    # ---------------------------------------------------------------- the asks
    attx, ex, regx, casesx, slx, colx = PR.load(tgt)
    gold_asks, paths = PR.run(tgt, quiet=True)
    n = len(gold_asks)
    for k, v in paths.items():
        h = PR.score(v, gold_asks)
        ok("A0 path '%s' keeps under 35 per cent of the ask figures" % k, h / n < 0.35, "%d of %d" % (h, n))
    def moved(path, gold, prefix):
        g = {k: v for k, _, v in gold}
        return all(abs(v - g[k]) > PR.UNIT[u] / 2 + 1e-9 for k, u, v in path if k.startswith(prefix))
    ok("A1 the synthetic suite kept in moves every exposure figure", moved(PR.exposure(attx, ex, regx, registered=False), gold_asks, "A_"))
    ok("A2 each case's latest row moves every impersonation figure", moved(PR.impersonation(casesx, slx, regx, colx, latest="case"), gold_asks, "B_"))
    ok("A2 'confirmed impersonation' as the only confirming finding moves every impersonation figure",
       moved(PR.impersonation(casesx, slx, regx, colx, confirmed=("confirmed impersonation",)), gold_asks, "B_"))
    ok("A3 sittings linked by booking reference move every interruption figure", moved(PR.interrupted(attx, regx, by="booking"), gold_asks, "C_"))
    ex_un = S.ask_exposure(tgt, files)
    for e in ex_un:
        ok("B4 week %d: no item within 0.10 points of the 12 per cent ceiling" % (e["week"] + 1), e["nearest"] >= 0.001, round(100 * e["nearest"], 3))
    conf_c = set(casesx.loc[casesx["finding"].isin(["confirmed impersonation", "confirmed on appeal"]), "candidate_id"])
    alt = PR.exposure(attx[~attx["candidate_id"].isin(conf_c)], ex, regx)
    ok("B4 leaving confirmed impersonations' sittings out moves no exposure figure", PR.score(alt, [g for g in gold_asks if g[0].startswith("A_")]) == len(alt))
    for t_ in S.ask_impersonation(tgt, files):
        x = t_["per_thousand"]
        dist = 0.05 - abs(x - round(x, 1))
        ok("B2 %s rate clear of its one-decimal edge" % t_["tier"], dist >= 0.004, round(dist, 4))
    for dv in S.ask_interrupted(tgt, files):
        x = dv["share"]
        dist = 0.005 - abs(x - round(x, 2))
        ok("B3 %s share clear of its two-decimal edge" % dv["device"], dist >= 0.0004, round(dist, 5))
    # the separation line: no device row inside the call's population
    pools_ = S.pools(L)
    ok("S1 every pool member has one completed estimate (no restart or suite row reaches a pool)",
       all(v.index.is_unique for v in pools_.values()))

    # ---------------------------------------------------------------- realism sweep
    po = S.pools(L)
    sizes = [len(v) for v in po.values()]
    ok("X1 no two account pools of equal size", len(set(sizes)) == len(sizes))
    pl = S.plan_rows(L)
    ok("X2 no round shortlist sizes repeated", pl["Shortlist"].nunique() == len(pl))
    card = json.load(open(os.path.join(os.path.dirname(TASK), ".claude", "skills", "fingerprint", "cards", "task249.json")))
    ok("X3 every persona in the pack is a drawn persona", set(P.PEOPLE.values()) <= set(card["world"]["people"]), sorted(P.PEOPLE.values()))
    print("\n%d failure(s)" % len(FAIL))
    return len(FAIL)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")) else 0)
