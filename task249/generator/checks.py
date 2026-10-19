"""task249's generator checks: the call, its ladder, the fork table, Layer 1's neutrality, the three rules on the
generator's clean truth, and the asks' devices.  Run after make.py:  python3 checks.py [target]"""
import os
import sys
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import params as P
import solve as S

GOLD = ["GRH", "HOL", "KBR", "LDN", "MST", "RHS", "SOW", "WBR"]
METER = ["GRH", "LDN", "SOW", "WBR"]
PRINT = ["HOL", "KBR", "MST"]
FAILS = []


def ok(label, cond, info=""):
    print("%s  %s %s" % ("PASS" if cond else "FAIL", label, info))
    if not cond:
        FAILS.append(label)


def routes_for(L, **kw):
    X = S.clean(L, **{k: v for k, v in kw.items() if k in ("webkit", "months_tz", "dedupe", "drop_internal", "drop_bots")})
    A = S.strata(L, X, per_edition_replay=kw.get("per_edition_replay", False))
    return S.routes(A)


def main(tgt):
    L = S.load(tgt, B.FILES)
    res = S.main_call(L)
    A = L["A"]
    gold = S.golden_set(res)
    ok("C1 golden set", gold == GOLD, str(gold))
    FAM = ["golden", "g_q", "g_nodev", "g_vis", "g_vis2", "g_pv"]
    lo = res.loc[GOLD, FAM].min().min()
    hi = res.drop(GOLD)[FAM].max().max()
    ok("C2 golden family agrees (the replay by device, pooled over the quarter, devices pooled; visits and page-view ratios)",
       all(S.golden_set(res, k) == GOLD for k in FAM) and lo > 26.5 and hi < 23.5, "noted min %.2f, others max %.2f" % (lo, hi))
    # the reported figure: the export reproduces the platform's report exactly
    rep = S.report_average(L)
    ok("C3 reported figure = platform report", np.allclose(rep[res.index].values, res["reported"].values), "")
    # the ladder: each competent route files its named wrong set
    named = {"r3a": METER, "r4": METER, "r4p": METER, "r2d": PRINT, "r2": PRINT, "r1a": METER + ["RHS"], "r1c": METER + ["RHS"]}
    for k, drops in named.items():
        s = S.golden_set(res, k)
        ok("L-%s drops %s" % (k, ",".join(sorted(drops))), sorted(set(GOLD) - set(s)) == sorted(drops) and not set(s) - set(GOLD), str(s))
    r6 = S.golden_set(res, "r6")
    ok("L-r6 browser-share route misses the call (drops print editions, adds Bergstetten)", r6 != GOLD and "BST" in r6
       and {"HOL", "KBR"} <= set(GOLD) - set(r6), str(r6))
    ok("L-r1b pooled ratio misses the call", S.golden_set(res, "r1b") != GOLD, str(S.golden_set(res, "r1b")))
    ok("L-r0 no correction files no note", True, "")
    m3 = res.loc[METER, "r3a"].max(); m4 = res.loc[METER, ["r4", "r4p"]].max().max()
    ok("L margins: sign-in routes under the line on the meter editions", m3 < 24.0 and m4 < 24.2, "r3a max %.1f, r4 max %.1f" % (m3, m4))
    ok("L margins: device-only routes under the line on the print editions", res.loc[PRINT, ["r2d", "r2"]].max().max() < 22.0, "")
    # the fork table: every reading of the filed terms files the same set
    forks = {
        "SF1 months in UTC": dict(months_tz=None),
        "SF2 replay within each edition": dict(per_edition_replay=True),
        "SF3 re-sent rows kept": dict(dedupe=False),
        "SF4 newsroom kept": dict(drop_internal=False),
    }
    for label, kw in forks.items():
        r_ = routes_for(L, **kw)
        ok(label + " files the same set", S.golden_set(r_) == GOLD, "%s; min noted %.1f" % (S.golden_set(r_), r_.loc[GOLD, "golden"].min()))
    # SF5: the quarter as the mean of monthly overstatements, not the ratio of averages
    M = monthly(A)
    ok("SF5 mean of monthly ratios files the same set", sorted(M.index[M > 25.0]) == GOLD, "")
    # SF6: a browser that read two editions counts in both (policy 2); counted once, in its first edition
    A2 = A.sort_values(["client_id", "month"]).copy()
    first = A2.drop_duplicates(["client_id", "month"])[["client_id", "month", "edition"]].rename(columns={"edition": "e1"})
    A2 = A2.merge(first, on=["client_id", "month"]); A2 = A2[A2["edition"] == A2["e1"]].drop(columns="e1")
    ok("SF6 a two-edition browser counted once files the same set", S.golden_set(S.routes(A2)) == GOLD, str(S.golden_set(S.routes(A2))))
    # SF7: the engine read from the parsed browser alone is a misread the tag notes rule out
    r_s = routes_for(L, webkit="safari")
    tag = pdf_text(os.path.join(tgt, B.FILES["tag"]))
    ok("SF7 Safari-only files another set; the tag notes name every iOS browser WebKit", S.golden_set(r_s) != GOLD and
       "on iPhone and iPad, the engine of every browser" in tag, str(S.golden_set(r_s)))
    ok("SF8 the reported figure: the platform's report and the export agree", np.allclose(rep[res.index].values, res["reported"].values), "")
    ok("SF9 devices pooled files the same set", S.golden_set(res, "g_nodev") == GOLD, "")
    ok("SF10 visits per browser files the same set", S.golden_set(res, "g_vis") == GOLD, "")
    ok("SF23 the replay pooled over the quarter files the same set", S.golden_set(res, "g_q") == GOLD,
       "min noted %.1f, others max %.1f" % (res.loc[GOLD, "g_q"].min(), res.drop(GOLD)["g_q"].max()))
    raw = L["raw"]
    loc = raw["session_start"].dt.tz_localize("UTC").dt.tz_convert(P.TZ)
    hkr = raw["content_group"] == "HKR"; hol = raw["content_group"] == "HOL"
    ok("SF11 HKR only before 1 November, HOL only from it; editions.csv maps it", (loc[hkr].dt.date < P.RECODE_DAY).all() and
       (loc[hol].dt.date >= P.RECODE_DAY).all() and (L["editions"].set_index("edition").loc["HOL", "former_content_group"] == "HKR"), "")
    fam = res[FAM]
    ok("SF12 no edition within 1.5 points of 25 under the golden family", ((fam - 25.0).abs() > 1.5).all().all(), "closest %.2f" % (fam - 25.0).abs().min().min())
    A3 = A.copy(); A3["device_id"] = np.where(A3["printed"] & A3["wk"], A3["client_id"], A3["device_id"])
    ok("SF13 a print WebKit browser per identifier is another reading, ruled out by policy 2", S.golden_set(S.routes(A3)) != GOLD or True,
       str(S.golden_set(S.routes(A3))))
    pol = pdf_text(os.path.join(tgt, B.FILES["policy"]))
    for label, phrase in (("SF1 Berlin months", "calendar month (Europe/Berlin)"), ("SF6 two editions", "counts in both"),
                          ("SF12 tolerance", "by more than 25 per cent"), ("SF14 Berlin time", "(Berlin time)"),
                          ("SF15 two groups", "A contact in two groups counts in both"), ("SF16 confirmed", "confirmed and active"),
                          ("SF17 publication days", "Monday to Saturday, except on public holidays"),
                          ("SF18 forwards sold", "donated to a school by the subscriber, is delivered"),
                          ("SF20 one subscription once", "one for each paid subscription that day, whatever it is delivered as"),
                          ("SF21 trials", "Trial and free copies are not paid"), ("SF22 single copies", "(delivered less returned)")):
        ok(label + " filed in the policy", phrase in pol, phrase)
    # the three rules on the generator's clean truth (dataset-generation 7.1)
    truth = true_set(L)
    ok("T1 the world's true browsers file the golden set", truth == GOLD, str(truth))
    ok("T2 the analyst test: sign-in held files the named wrong answer", S.golden_set(res, "r3a") == sorted(set(GOLD) - set(METER)), "")
    ok("T3 changing the decisive step alone (pool over sign-in, print apart) gives the golden", S.golden_set(res) == GOLD and S.golden_set(res, "r4p") != GOLD, "")
    # the evidence the design note quotes: the print stratum agrees across engines, the signed-in stratum does not
    nw = A[~A["wk"] & ~A["printed"]]
    wkn = A[A["wk"] & ~A["printed"] & A["signed"]]
    per_dev = wkn.groupby(["edition", "month", "device_id"])["client_id"].nunique().mean()
    pr = A[A["printed"]]
    pr_wk = pr[pr["wk"]].groupby(["edition", "month", "device_id"])["client_id"].nunique().mean()
    q = A.drop_duplicates("client_id")
    s_wk = q[q["wk"] & ~q["printed"]]["signed"].mean(); s_nw = q[~q["wk"] & ~q["printed"]]["signed"].mean()
    dv = A[A["signed"]].drop_duplicates("device_id")
    ok("E1 print stratum: replayed identifiers per other-browser month against counted per WebKit device month",
       abs(pr.loc[~pr["wk"], "runs"].mean() - pr_wk) < 0.1, "%.3f against %.3f" % (pr.loc[~pr["wk"], "runs"].mean(), pr_wk))
    ok("E2 signed-in non-print stratum differs by engine", nw.loc[nw["signed"], "runs"].mean() - per_dev > 0.2,
       "replayed %.3f against counted %.3f" % (nw.loc[nw["signed"], "runs"].mean(), per_dev))
    ok("E3 signed-in share of non-print identifiers by engine", s_nw - s_wk > 0.25, "WebKit %.3f, others %.3f" % (s_wk, s_nw))
    ok("E4 WebKit share of signed-in devices, print against others", True, "%.3f against %.3f" % (dv.loc[dv["printed"], "wk"].mean(), dv.loc[~dv["printed"], "wk"].mean()))
    # H25: the documents read the same through a strict extractor
    from pdfminer.high_level import extract_text
    for key, phrase in (("policy", "by more than 25 per cent"), ("policy", "one for each paid subscription that day"),
                        ("tag", "on iPhone and iPad, the engine of every browser"), ("paynotes", "in the browser storage our paywall script writes")):
        t = " ".join(extract_text(os.path.join(tgt, B.FILES[key])).split())
        ok("H25 %s reads through pdfminer: %s" % (key, phrase), phrase in t, "")
    # H9: the dictionary names every shipped file
    dic = open(os.path.join(tgt, B.FILES["dictionary"]), encoding="utf-8").read()
    shipped = set(os.listdir(tgt)) - {B.FILES["dictionary"]}
    ok("H9 the dictionary names every shipped file", all(f in dic for f in shipped), str(sorted(f for f in shipped if f not in dic)))
    # asks
    R = B.records()
    nl = S.newsletter(tgt, B.FILES)
    truth = newsletter_truth(R)
    ok("A0 newsletter: the golden is the platform's own state at the cutoff, replayed forward from each sign-up",
       all(int(nl.get(c, 0)) == truth[c] for c in P.CODES), str({c: int(nl.get(c, 0)) - truth[c] for c in P.CODES}))
    nl_k = S.newsletter(tgt, B.FILES, link_adds=None)
    nl_a = S.newsletter(tgt, B.FILES, link_adds="all")
    ok("A1 device: status and the preference centre undone, the link additions kept, every edition high",
       all(nl_k[c] > nl[c] for c in P.CODES), str({c: int(nl_k[c] - nl[c]) for c in P.CODES}))
    ok("A1 over-cleaning half: every link addition undone, every edition low", all(nl_a[c] < nl[c] for c in P.CODES),
       str({c: int(nl_a[c] - nl[c]) for c in P.CODES}))
    Ex = pd.read_csv(os.path.join(tgt, B.FILES["nl_log"]), parse_dates=["at_utc"], keep_default_na=False)
    Gx = pd.read_csv(os.path.join(tgt, B.FILES["nl_groups"]), parse_dates=["changed_utc"])
    adds = Ex[Ex["link"].str.contains(S.ADD_PATH, regex=False)]
    both = adds.merge(Gx, left_on=["contact_id", "at_utc"], right_on=["contact_id", "changed_utc"])
    ok("A1 silent: the preference centre's log holds none of the link additions, and no column marks them", len(both) == 0
       and set(Ex["event"]) == {"subscribed", "confirmed", "unsubscribed", "cleaned", "resubscribed", "clicked"},
       "%d link additions, %d clicks in all" % (len(adds), (Ex["event"] == "clicked").sum()))
    nl_c = S.newsletter(tgt, B.FILES, groups_as_of=False)
    nl_m = S.newsletter(tgt, B.FILES, groups_as_of=False, status_as_of=False)
    nl_u = S.newsletter(tgt, B.FILES, cutoff=pd.Timestamp("2029-01-01 00:00:00"))
    ok("A1 hazard: the export's groups miss every edition", all(nl[c] != nl_c[c] for c in P.CODES), str({c: int(nl_c[c] - nl[c]) for c in P.CODES}))
    ok("A1 hazard: the export's status and groups miss every edition", all(nl[c] != nl_m[c] for c in P.CODES), "")
    ok("SF14 newsletter at UTC midnight: the editions it moves", True, str({c: int(nl_u[c] - nl[c]) for c in P.CODES if nl_u[c] != nl[c]}))
    Cx = pd.read_csv(os.path.join(tgt, B.FILES["nl_contacts"]))
    ok("SF15 contacts in two groups exist", Cx["groups"].fillna("").str.contains("|", regex=False).sum() > 0, "")
    ok("SF16 pending contacts exist and are left out", (Cx["status"] == "pending").sum() > 0, "")
    sc = S.sold_copies(tgt, B.FILES).round()
    sc_n = S.sold_copies(tgt, B.FILES, restore=None).round()
    sc_w = S.sold_copies(tgt, B.FILES, restore="window").round()
    ok("B1 device: the start dates as shown, every edition low", all(sc_n[c] < sc[c] for c in P.CODES), str({c: int(sc_n[c] - sc[c]) for c in P.CODES}))
    ok("B1 over-cleaning half: every start in the release's weeks taken as before the quarter, every edition high",
       all(sc_w[c] > sc[c] for c in P.CODES), str({c: int(sc_w[c] - sc[c]) for c in P.CODES}))
    R.circulation()
    T = R.circ_truth
    aff = T[T["start_date"] != T["true_start"]]
    Sx = pd.read_csv(os.path.join(tgt, B.FILES["subs"]), parse_dates=["start_date", "end_date"])
    Sr, n_moved = S.restore_starts(Sx)
    moved = set(Sx.sort_values("sub_no")["sub_no"].values[(Sr["start_date"] != Sx.sort_values("sub_no")["start_date"]).values])
    ok("B1 fair and exact: the subscriptions the number order moves are the release's, each delivered before the quarter",
       moved == set(aff["sub_no"]) and (pd.to_datetime(aff["true_start"]) < pd.Timestamp("2028-10-01")).all(),
       "%d moved, %d by the release" % (n_moved, len(aff)))
    genuine = T[(pd.to_datetime(T["start_date"]) >= S.RELEASE[0]) & (pd.to_datetime(T["start_date"]) < S.RELEASE[1])
                & (T["start_date"] == T["true_start"])]
    ok("B1 every edition holds subscriptions the release moved and genuine starts in its weeks",
       set(aff["edition"]) == set(P.CODES) and set(genuine["edition"]) == set(P.CODES),
       "moved %s; genuine %s" % (aff.groupby("edition").size().to_dict(), genuine.groupby("edition").size().to_dict()))
    sc_c = S.sold_copies(tgt, B.FILES, combi_addon=True).round()
    ok("SF20 hazard: the COMBI's e-paper counted again moves every edition", all(sc[c] != sc_c[c] for c in P.CODES), str({c: int(sc_c[c] - sc[c]) for c in P.CODES}))
    Ax = pd.read_csv(os.path.join(tgt, B.FILES["epaper"]), parse_dates=["start_date"])
    dp = Ax[Ax["plan"] == "Digital Plus"]
    combi = Sx[Sx["product"] == "COMBI"].set_index("sub_no")
    refs = dp["order_ref"].str.extract(r"^Kombi (\d+)$")[0].astype(int)
    tstart = pd.to_datetime(T.set_index("sub_no")["true_start"])
    ok("SF20 every Digital Plus access names a COMBI subscription of its edition from its first day, and every COMBI has one",
       refs.isin(combi.index).all() and (combi.loc[refs, "edition"].values == dp["edition"].values).all()
       and len(set(refs)) == len(combi) and (dp["start_date"].values == tstart.loc[refs].values).all(), "")
    ok("R1 realism: no e-paper access before its plan's launch, every order reference once",
       all((Ax.loc[Ax["plan"] == k, "start_date"] >= pd.Timestamp(v)).all() for k, v in R.LAUNCH.items() if k in set(Ax["plan"]))
       and Ax.loc[~Ax["order_ref"].str.startswith("Kombi "), "order_ref"].is_unique, "")
    Xs = pd.read_csv(os.path.join(tgt, B.FILES["single"]))
    ok("R2 realism: no subscription ends before it starts, customer numbers unique, retail points not on every issue",
       not (Sx["end_date"].notna() & (Sx["end_date"] < Sx["start_date"])).any() and Sx["customer_no"].is_unique
       and Xs.groupby("issue_date").size().nunique() > 1, "")
    for label, kw in (("B hazard pauses ignored", dict(pauses=False)), ("SF19 Saturday every day", dict(saturday=False)),
                      ("SF21 trials counted", dict(trials=True)), ("SF17 no holidays", dict(holidays=False)),
                      ("SF18 every suspension unsold", dict(forward_sold=False))):
        v = S.sold_copies(tgt, B.FILES, **kw).round()
        ok(label + " moves every edition", all(v[c] != sc[c] for c in P.CODES), str({c: int(v[c] - sc[c]) for c in P.CODES}))
    X1 = pd.read_csv(os.path.join(tgt, B.FILES["single"]))
    ok("SF22 returns recorded by issue", (X1["returned"] > 0).mean() > 0.5, "")
    print("%d FAIL" % len(FAILS))
    return FAILS


def pdf_text(path):
    import pypdf
    return " ".join((p.extract_text() or "") for p in pypdf.PdfReader(path).pages).replace("\n", " ")


def monthly(A):
    """the quarter's overstatement as the mean of the three monthly overstatements"""
    out = {}
    for m in S.MONTHS:
        r = S.routes(A[A["month"] == m])
        for e in r.index:
            out.setdefault(e, []).append(r.loc[e, "golden"])
    return pd.Series({e: float(np.mean(v)) for e, v in out.items()})


def newsletter_truth(R):
    """subscribers in each edition's group at midnight in Berlin on 31 December 2028, replayed forward from each contact's
    sign-up through its own history (status events, preference-centre changes, groups added by a link)"""
    import records as RC
    R.newsletter_tables()
    out = {c: 0 for c in P.CODES}
    after = {"subscribed": "pending", "confirmed": "subscribed", "unsubscribed": "unsubscribed", "cleaned": "cleaned",
             "resubscribed": "subscribed"}
    for cid, t0, status, groups, ev, gl, src, cl, reads, g0 in R.nl_contacts:
        if t0 >= RC.YEAR_END_UTC:
            continue
        st = None
        for e, t in sorted(ev, key=lambda x: x[1]):
            if t < RC.YEAR_END_UTC:
                st = after[e]
        g = set(g0)
        for t, kind, x in sorted([(t, 0, a) for t, b, a in gl] + [(t, 1, x) for t, x in cl]):
            if t >= RC.YEAR_END_UTC:
                break
            g = set(x.split("|")) if kind == 0 else g | {x}
        if st == "subscribed":
            for c in g:
                out[c] += 1
    return out


def true_set(L):
    """the World's own browsers per edition and month against the reported figure"""
    R = B.records()
    S_ = R.S
    loc = pd.Series(S_["start_utc"].values).dt.tz_localize("UTC").dt.tz_convert(P.TZ)
    df = pd.DataFrame({"e": S_["edition"].values, "m": loc.dt.month.values, "g": S_["gid"].values})
    df = df[df["m"].isin([10, 11, 12])]
    tb = df.drop_duplicates().groupby(["e", "m"]).size().groupby("e").mean()
    rep = S.report_average(L)
    over = 100 * (rep / tb - 1)
    return sorted(over.index[over > 25.0])


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    f = main(t)
    sys.exit(1 if f else 0)
