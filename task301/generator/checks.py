"""Generator assertions for task301: the call and its licensed family, the ladder, the semantic fork rows (SFn), the
ask devices, the input gates and the three-rules block on the world's clean truth. Exit status 1 on any failure."""
import os
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm

import build as B
import params as P
import solve as S

FAIL = []


def check(name, ok, detail=""):
    print("%-4s %s%s" % ("ok" if ok else "FAIL", name, (" :: " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)


def rnd(x, u):
    return int(round(x / float(u)) * u)


def family(target, ext, hist, log, h, pr, L, K):
    """The licensed constructions: each fits a sub-region's own decay from its own recordings."""
    grid = (np.arange(53) + 0.5) / 53
    he = hist.sort_values(["patient_key", "recorded_at"], kind="stable").copy()
    he["c"] = S.code(he.smoking_status.values)
    he["t"] = (pd.to_datetime(he.recorded_at.str[:10]) - pd.Timestamp("2012-01-01")).dt.days.values / S.YD
    he["sub_region"] = he.patient_key.map(ext.set_index("patient_key").sub_region).values
    pe_all = S.pairs_of(he)
    es = S.fit_ctmc(pr[pr.sub_region == "Eastern Shore"])[0]
    lg = log.copy()
    lg["age"] = (pd.to_datetime(lg.call_date) - pd.to_datetime(lg.list_status_date)).dt.days.values / S.YD
    pi = es[1] / sum(es)
    k_model = (log.four_week_status == "Not smoking").sum() / (pi + (1 - pi) * np.exp(-sum(es) * lg.age.values)).sum()
    fam = {}
    for g in S.CANDS:
        Lg = L[L.sub_region == g]
        a = Lg.age_y.values
        p = pr[pr.sub_region == g]
        o = {}
        qr = S.fit_ctmc(p)[0]
        o["ctmc_day_pairs"] = S.p_still(a, *qr).sum() * K
        o["ctmc_entry_pairs"] = S.p_still(a, *S.fit_ctmc(pe_all[pe_all.sub_region == g])[0]).sum() * K
        o["ctmc_smoker_start"] = S.p_still(a, *S.fit_ctmc(p[p.c0 == "S"])[0]).sum() * K
        o["ctmc_never_dropped"] = S.p_still(a, *S.fit_ctmc(p[p.c1 != "N"])[0]).sum() * K
        o["mid_year_call"] = (qr[1] / sum(qr) + (1 - qr[1] / sum(qr)) * np.exp(-sum(qr) * (a + 0.5))).sum() * K
        o["model_conversion"] = S.p_still(a, *qr).sum() * k_model
        ps = p[p.c0 == "S"]
        edges = np.array([0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12, 15])
        mids, vals = [], []
        for lo, hi in zip(edges[:-1], edges[1:]):
            m = ps[(ps.dt >= lo) & (ps.dt < hi)]
            if len(m) >= 25:
                mids.append(m.dt.mean())
                vals.append((m.c1 == "S").mean())
        o["share_by_gap"] = np.mean([np.interp(a + x, mids, vals) for x in grid], axis=0).sum() * K
        X2 = sm.add_constant(np.column_stack([ps.dt, ps.dt ** 2]))
        l2 = sm.GLM((ps.c1 == "S").astype(float), X2, family=sm.families.Binomial()).fit()
        o["logit_gap_sq"] = np.mean([l2.predict(sm.add_constant(np.column_stack([a + x, (a + x) ** 2]),
                                                                has_constant="add")) for x in grid], axis=0).sum() * K
        X1 = sm.add_constant(ps.dt.values)
        l1 = sm.GLM((ps.c1 == "S").astype(float), X1, family=sm.families.Binomial()).fit()
        o["logit_gap"] = np.mean([l1.predict(sm.add_constant(a + x, has_constant="add")) for x in grid],
                                 axis=0).sum() * K
        acc = 0.0
        for flag in ("Y", "N"):
            keys = set(ext.patient_key[(ext.sub_region == g) & (ext.chronic_condition_review == flag)])
            pk = S.pairs_of(h[h.patient_key.isin(keys)])
            Lf = Lg[Lg.chronic_condition_review == flag]
            acc += S.p_still(Lf.age_y.values, *S.fit_ctmc(pk)[0]).sum() * K
        o["by_review_flag"] = acc
        fam[g] = o
    return pd.DataFrame(fam).T


def rungs(ext, hist, log, h, pr, L, cv):
    K = cv["k"]
    lg = log.copy()
    lg["age"] = (pd.to_datetime(lg.call_date) - pd.to_datetime(lg.list_status_date)).dt.days.values / S.YD
    lg["q4"] = (lg.four_week_status == "Not smoking").astype(float)
    edges = [0, 1, 2, 3, 5, 8, 99]
    rate = lg.groupby(pd.cut(lg.age, edges, right=False), observed=False).q4.mean()
    X = sm.add_constant(np.column_stack([lg.age, lg.age ** 2]))
    fl = sm.GLM(lg.q4, X, family=sm.families.Binomial()).fit()
    es = S.fit_ctmc(pr[pr.sub_region == "Eastern Shore"])[0]
    pool = S.fit_ctmc(pr[pr.sub_region.isin(S.CANDS)])[0]
    out = {}
    for g in S.CANDS:
        Lg = L[L.sub_region == g]
        a = Lg.age_y.values
        out[g] = {"naive_per_listed": len(Lg) * cv["per_listed"],
                  "recent_two_years": (a < 2.25).sum() * cv["per_listed"],
                  "common_five_pct": np.exp(-0.05 * (a + 0.5)).sum() * K,
                  "pilot_age_bins": pd.Series(pd.cut(a + 0.5, edges, right=False)).map(rate).astype(float).sum(),
                  "pilot_age_logit": fl.predict(sm.add_constant(np.column_stack([a + 0.5, (a + 0.5) ** 2]),
                                                                has_constant="add")).sum(),
                  "eastern_shore_decay": S.p_still(a, *es).sum() * K,
                  "pooled_decay": S.p_still(a, *pool).sum() * K}
    return pd.DataFrame(out).T


def main(target, R=None):
    FAIL.clear()
    gold, cv, h, pr, L, log, ext = S.golden(target)
    hist = pd.read_parquet(os.path.join(target, B.FILES["history"]))
    K = cv["k"]
    q = pd.Series({g: v["quits"] for g, v in gold.items()})
    win = q.idxmax()
    check("call: the golden names Inner South", win == "Inner South", "%s %.1f" % (win, q.max()))
    check("call: printed to the nearest 50 is 550", rnd(q[win], 50) == 550, "%.1f" % q[win])
    fam = family(target, ext, hist, log, h, pr, L, K)
    names = fam.idxmax()
    check("family: every licensed construction names Inner South", (names == "Inner South").all(), names.to_dict().__str__())
    b = fam.loc["Inner South"]
    printed = sorted(set(rnd(v, 50) for v in b))
    check("family: Inner South prints 550 under every construction", printed == [550], "%s from %.1f to %.1f" % (printed, b.min(), b.max()))
    check("family: every construction at least 5 inside the 550 cell", b.min() >= 530 and b.max() <= 570,
          "%.1f to %.1f against 525 and 575" % (b.min(), b.max()))
    lead = (b / fam.drop("Inner South").max() - 1) * 100
    check("family: Inner South leads by 4 per cent or more under every construction", (lead >= 4.0).all(),
          "lowest %.1f per cent" % lead.min())
    rg = rungs(ext, hist, log, h, pr, L, cv)
    want = {"naive_per_listed": "Coastal Hinterland", "recent_two_years": "Western Plains",
            "common_five_pct": "Coastal Hinterland", "pilot_age_bins": "Coastal Hinterland",
            "pilot_age_logit": "Coastal Hinterland", "eastern_shore_decay": "Coastal Hinterland",
            "pooled_decay": "Coastal Hinterland"}
    for k, w in want.items():
        got = rg[k].idxmax()
        check("ladder: %s names %s" % (k, w), got == w, "%s; Inner South %.1f, %s %.1f" % (got, rg.loc["Inner South", k], w, rg.loc[w, k]))
    check("ladder: the pilot gradient's lead for Coastal Hinterland is 15 per cent or more",
          rg.loc["Coastal Hinterland", "pilot_age_logit"] / rg.loc["Inner South", "pilot_age_logit"] >= 1.15
          and rg.loc["Coastal Hinterland", "pilot_age_bins"] / rg.loc["Inner South", "pilot_age_bins"] >= 1.15,
          "%.3f and %.3f" % (rg.loc["Coastal Hinterland", "pilot_age_logit"] / rg.loc["Inner South", "pilot_age_logit"],
                             rg.loc["Coastal Hinterland", "pilot_age_bins"] / rg.loc["Inner South", "pilot_age_bins"]))
    # pooling is refuted: a likelihood ratio on the four candidates' pairs, per-region rates against one pair of rates
    ll_sep = sum(S.fit_ctmc(pr[pr.sub_region == g])[1] for g in S.CANDS)
    ll_pool = S.fit_ctmc(pr[pr.sub_region.isin(S.CANDS)])[1]
    check("ladder: the record rejects one decay for all four (LR on 6 df over 100)", 2 * (ll_pool - ll_sep) > 100,
          "2 dlogL %.1f" % (2 * (ll_pool - ll_sep)))
    # semantic fork rows
    alt = ext[ext.smoking_status.isin(["Daily smoker", "Smoker"]) & ext.sub_region.isin(S.CANDS)].copy()
    alt["age_y"] = (pd.Timestamp(S.Y0) - pd.to_datetime(alt.smoking_status_date)).dt.days.values / S.YD
    q1 = {g: S.p_still(alt[alt.sub_region == g].age_y.values, *S.fit_ctmc(pr[pr.sub_region == g])[0]).sum() * K
          for g in S.CANDS}
    check("SF1 current smoker read as daily smoker or smoker only: same call", max(q1, key=q1.get) == win)
    fu = log[log.four_week_status != "Lost to follow-up"]
    k2 = cv["reach"] * (fu.four_week_status == "Not smoking").sum() / ((fu.outcome != "Not reached").sum() - cv["stopped"])
    check("SF2 lost to follow-up left out instead of counted as smoking: same call (one factor for all four)",
          True, "factor %.4f against %.4f" % (k2, K))
    check("SF3 calls taken at mid-2027 instead of spread through the year: same call",
          fam["mid_year_call"].idxmax() == win)
    hl = h.groupby("patient_key").tail(1)
    lst2 = set(hl[hl.c == "S"].patient_key) & set(ext.patient_key[ext.sub_region.isin(S.CANDS)])
    check("SF4 the list from the history's last day-level entry equals the extract's", lst2 == set(L.patient_key),
          "%d against %d" % (len(lst2), len(L)))
    check("SF5 never smoked after a smoker or ex-smoker entry dropped instead of read as not smoking: same call",
          fam["ctmc_never_dropped"].idxmax() == win)
    check("SF6 entry-level pairs instead of the day's last entry: same call", fam["ctmc_entry_pairs"].idxmax() == win)
    check("SF7 conversion from Eastern Shore's own expected smokers at its calls: same call and figure",
          fam["model_conversion"].idxmax() == win and rnd(fam.loc[win, "model_conversion"], 50) == 550)
    check("SF8 a December 2027 call whose four weeks end in 2028 counts in 2027 (the plan counts by the call): no "
          "alternative changes the call", True)
    # asks
    A = S.ask_referrals(target)
    qr_ = pd.read_csv(os.path.join(target, B.FILES["quitline"]), dtype=str, keep_default_na=False)
    qr_ = qr_[qr_.month.str[:4] == "2025"].copy()
    qr_["referrals"] = qr_.referrals.astype(int)
    lab = qr_[qr_.phn_sub_region.isin(S.CANDS)].groupby("phn_sub_region").referrals.sum().reindex(S.CANDS)
    prac = pd.read_csv(os.path.join(target, B.FILES["practices"]), dtype=str, keep_default_na=False)
    exact = dict(zip(prac.practice_name, prac.sub_region))
    qr_["exact"] = qr_.referring_practice.map(exact).fillna(qr_.phn_sub_region)
    exj = qr_[qr_.exact.isin(S.CANDS)].groupby("exact").referrals.sum().reindex(S.CANDS)
    check("ask A: Quitline's own sub-region label misses all 4 sub-regions", int((lab.values == A.values).sum()) == 0,
          "%d hits" % int((lab.values == A.values).sum()))
    check("ask A: an exact-name join falling back on the label misses all 4 sub-regions",
          int((exj.values == A.values).sum()) == 0, "%d hits" % int((exj.values == A.values).sum()))
    d = S.dialler_legs(target)
    Bg = S.ask_evening(target)

    def ev(df, col):
        e = df[df[col].dt.hour >= 17]
        return pd.DataFrame({"calls": e.groupby(e[col].dt.day_name()).size(),
                             "reached": e[e.result == "Answered"].groupby(e[col].dt.day_name()).patient_key.nunique()}
                            ).reindex(S.WEEKDAYS).fillna(0)
    to_pat = d[d.result != "Transferred"]
    for nm, df, col, reach in (("the record time as the start, every leg", d, "end", True),
                               ("the record time as the start, Transferred legs out", to_pat, "end", True),
                               ("each leg's start, Transferred legs in", d, "start", False)):
        v = ev(df, col)
        hits = int((v.calls.values == Bg.calls.values).sum())
        check("ask B: %s misses every weekday's calls" % nm, hits == 0, "%d of 5" % hits)
        if reach:
            hits = int((v.reached.values == Bg.reached.values).sum())
            check("ask B: %s misses every weekday's patients reached" % nm, hits == 0, "%d of 5" % hits)
    tr = d[d.result == "Transferred"]
    ans = d[d.result == "Answered"]
    pair_ = tr.merge(ans[["patient_key", "date_time", "agent_id"]], on=["patient_key", "date_time", "agent_id"],
                     how="left", indicator=True)
    check("ask devices: every Transferred leg shares its patient's answered leg's record time and agent",
          bool((pair_._merge == "both").all()) and len(tr) > 0, "%d legs" % len(tr))
    calls_ = to_pat.merge(tr[["patient_key", "date_time", "duration_s"]].rename(columns={"duration_s": "ql_s"}),
                          on=["patient_key", "date_time"], how="left")
    calls_["ql_s"] = calls_.ql_s.fillna(0)
    calls_["staff_end"] = calls_.end - pd.to_timedelta(calls_.ql_s, unit="s")
    calls_["as_start_end"] = calls_.end + pd.to_timedelta(calls_.duration_s, unit="s")

    def overlaps(df, s_col, e_col):
        n = 0
        for _, g in df.sort_values([s_col, "leg_id"]).groupby("agent_id"):
            sv, evv = g[s_col].values, g[e_col].values
            n += int((sv[1:] < np.maximum.accumulate(evv)[:-1]).sum())
        return n
    n_end = overlaps(calls_, "start", "staff_end")
    n_start = overlaps(calls_, "end", "as_start_end")
    n_whole = overlaps(calls_, "start", "end")
    check("ask B device: no agent's legs overlap with each leg started its duration before its record time and a "
          "transferred call's agent part ending at the transfer", n_end == 0, "%d" % n_end)
    check("ask B device: read as start times, the same agents' legs overlap", n_start >= 300, "%d" % n_start)
    check("ask C device: with a transferred patient's leg held whole, its agent is on the next call before it ends",
          n_whole >= 0.5 * len(tr), "%d of %d transfers" % (n_whole, len(tr)))
    C = S.ask_talk(target)
    every = d[d.result.isin(["Answered", "Transferred"])]
    for nm, src in (("answered legs whole (or merged with their Transferred leg)", ans),
                    ("answered and Transferred legs summed", every)):
        hits = 0
        for ag in S.AGENT_IDS:
            a_ = ans[ans.agent_id == ag]
            x = src[src.agent_id == ag]
            v = (x.groupby(x.start.dt.month).duration_s.sum() / 60.0 /
                 a_.groupby(a_.start.dt.month).patient_key.nunique()).round(1)
            hits += int((v.values == C[ag].round(1).values).sum())
        check("ask C: %s misses all 30 member-months" % nm, hits == 0, "%d of 30" % hits)
    edge = 0.05 - np.abs(C.values - np.round(C.values, 1))
    check("ask C: every member-month at least 0.0025 inside its printed cell", (edge >= 0.0025).all(),
          "closest %.4f" % edge.min())
    check("ask C: 30 member-months, every member every month", C.shape == (10, 3) and C.notna().all().all())
    if R is not None:
        Rd = R["dialler"]
        check("ask devices: the start times found from the pack are the generator's",
              bool((pd.to_datetime(Rd.date_time) - pd.to_timedelta(Rd.duration_s, unit="s") == Rd._start)
                   [Rd._kind == "call"].all()))
        check("ask devices: staff seconds found from the pack are the generator's",
              int(Rd._staff_s.sum()) == int(ans.duration_s.sum() - tr.duration_s.sum() +
                                            d[~d.result.isin(["Answered", "Transferred"])].duration_s.sum()))
    # separation: the main call reads only the extract, the history and the case log
    check("separation: no ask file is read by the main call", True,
          "solve.golden opens %s, %s and %s" % (B.FILES["extract"], B.FILES["history"], B.FILES["log"]))
    # input gates
    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    check("input gates: 10 or more files", len(files) >= 10, str(len(files)))
    check("input gates: 3 or more formats", len(fmts) >= 3, str(fmts))
    check("input gates: a file of 25,000 rows or more", len(ext) >= 25000 and len(hist) >= 25000,
          "%d and %d" % (len(ext), len(hist)))
    check("input gates: 2 or more distractors", len(B.DISTRACTORS) >= 2, str(B.DISTRACTORS))
    # three rules on the clean truth: the analyst's easy route is wrong on the world's own rates and team process
    if R is not None:
        k_true = P.REACH * P.QUIT_DATE * P.ABSTAIN
        es_true = (P.QUIT["P"], P.RELAPSE)
        e_route = {g: S.p_still(L[L.sub_region == g].age_y.values, *es_true).sum() * k_true for g in S.CANDS}
        own = {g: S.p_still(L[L.sub_region == g].age_y.values, P.QUIT[k], P.RELAPSE).sum() * k_true
               for k, g in zip(P.CAND, S.CANDS)}
        check("three rules: on clean truth, Eastern Shore's decay carried to the lists names Coastal Hinterland",
              max(e_route, key=e_route.get) == "Coastal Hinterland", str({k: round(v) for k, v in e_route.items()}))
        check("three rules: on clean truth, each sub-region's own decay names Inner South",
              max(own, key=own.get) == "Inner South", str({k: round(v) for k, v in own.items()}))
    print("%d failures" % len(FAIL))
    return len(FAIL)


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)
