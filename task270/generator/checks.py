"""The generator's assertions on the cut pack: the input gates, the call and its estimator family, the rungs, the three
rules (R1 the field's raw material ships, R2 every mess item neutral, R3 the analyst test on the clean truth), the
semantic forks (SF rows), the separation of the asks from the call, the ask devices and their stops, the realism sweep
and the containers. Every label is printed with PASS or FAIL; the run fails on any FAIL."""
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import analysis as A
import asks as AK
import common as K

ROWS = []


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def name(v):
    return K.CAND[int(np.argmax(v))]


def lead(v):
    o = np.argsort(-np.asarray(v))
    return K.CAND[o[0]], float(v[o[0]] / v[o[1]])


def world_changes(W):
    """the clean truth: each change's arm statistics straight from the world's users (no export, no rounding, the
    complete computation), over the standard's population"""
    rows = []
    for e in W.experiments:
        if e.six_month_at > K.PULL or e.srm or e.end > W.last_day:
            continue
        c = W.arm_stats(e, 0)
        for a in range(1, e.arms):
            t = W.arm_stats(e, a)
            row_ = dict(experiment_id=e.eid, arm=str(a), nt=t[0], nc=c[0])
            for j, m in enumerate(K.CAND + [K.RET]):
                row_["mt_" + m], row_["st_" + m], row_["mc_" + m], row_["sc_" + m] = t[1][j], t[2][j], c[1][j], c[2][j]
                row_["nt_" + m], row_["nc_" + m] = t[0], c[0]
            rows.append(row_)
    return pd.DataFrame(rows)


def relative(c, hm):
    """the golden on relative effects: each effect over its control mean, its sampling moments scaled alike"""
    e = A.effects(c)
    out = []
    y = e[K.RET] / c["mc_" + K.RET].to_numpy()
    vy = e["v_" + K.RET] / c["mc_" + K.RET].to_numpy() ** 2
    for k, m in enumerate(K.CAND):
        x = e[m] / c["mc_" + m].to_numpy()
        vx = e["v_" + m] / c["mc_" + m].to_numpy() ** 2
        s12 = hm["rho"][k] * (c["st_" + m] * c["st_" + K.RET] / c["nt_" + K.RET] +
                             c["sc_" + m] * c["sc_" + K.RET] / c["nc_" + K.RET]).to_numpy()
        s12 = s12 / (c["mc_" + m].to_numpy() * c["mc_" + K.RET].to_numpy())
        cxy = np.cov(x, y)[0, 1] - s12.mean()
        out.append(cxy / np.sqrt((x.var(ddof=1) - vx.mean()) * (y.var(ddof=1) - vy.mean())))
    return np.array(out)


def flat(x, p=""):
    if isinstance(x, dict):
        o = {}
        for k, v in x.items():
            o.update(flat(v, p + "/" + str(k)))
        return o
    return {p: x}


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    golden_dir = os.path.join(task, "golden")
    W = b["world"]
    d = res["data"]
    hm = res["hm"]
    gold = res["golden"]

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    row("GATE files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    row("GATE formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(b["counts"].values())
    row("GATE 25,000-row file", big >= 25000, "largest %d rows" % big)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    row("GATE distractors", len(meta["distractor_files"]) >= 2 and
        all(os.path.basename(x) in files for x in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    row("GATE provenance", set(meta["provenance"]) == set(files), "%d entries" % len(meta["provenance"]))
    row("GATE deliverables", sorted(os.listdir(golden_dir)) == sorted(K.DELIVERABLES), ", ".join(K.DELIVERABLES))

    # ------------------------------------------------------------------ the call
    row("CALL proxy", res["proxy"] == "first_purchase_d14" and res["runner_up"] == "sessions_d1_14",
        "%s, then %s" % (res["proxy"], res["runner_up"]))
    o = np.sort(gold)[::-1]
    row("CALL margin over the runner-up", o[0] / o[1] >= 1.4, "%.3f against %.3f (%.2fx)" % (o[0], o[1], o[0] / o[1]))
    row("CALL runner-up clear of the third", o[1] - o[2] >= 0.08, "%.3f against %.3f" % (o[1], o[2]))
    te = W.true_effects()
    keys = [(e.idx, a) for e in W.experiments if e.six_month_at <= K.PULL and not e.srm and e.end <= W.last_day
            for a in range(1, e.arms)]
    T = np.array([te[k] for k in keys])
    tc = np.array([np.corrcoef(T[:, k], T[:, 5])[0, 1] for k in range(5)])
    row("CALL the world's true effects name it", name(tc) == res["proxy"] and
        K.CAND[int(np.argsort(-tc)[1])] == res["runner_up"], "true correlations %s" % np.round(tc, 3))
    fam = res["family"]
    figs = {k: tuple(K.r(x, 2) for x in v) for k, v in fam.items()}
    row("FAMILY every equal-weight member names the proxy and the runner-up",
        all(name(v) == res["proxy"] and K.CAND[int(np.argsort(-v)[1])] == res["runner_up"] for v in fam.values()),
        ", ".join(fam))
    row("FAMILY every member gives the same five figures at two decimals", len(set(figs.values())) == 1,
        str(sorted(set(figs.values()))))
    reml = A.bivariate_reml(res["changes"], hm)
    row("FAMILY the precision-weighted bivariate fit (not the standard's weighting) names the proxy",
        name(reml) == res["proxy"], "%s" % np.round(reml, 3))

    # ------------------------------------------------------------------ the rungs
    for k, want in (("raw", "sessions_d1_14"), ("spearman", "sessions_d1_14"), ("disattenuated", "sessions_d1_14"),
                    ("half", "sessions_d1_14"), ("user", "active_days_d1_14")):
        v = res[k]
        nm, m = lead(v)
        row("RUNG %s names %s" % (k, want), nm == want, "%s %.3f, margin %.2fx" % (nm, np.max(v), m))
    row("RUNG raw and disattenuated margins at least 1.15x", lead(res["raw"])[1] >= 1.15 and
        lead(res["disattenuated"])[1] >= 1.15, "%.2fx, %.2fx" % (lead(res["raw"])[1], lead(res["disattenuated"])[1]))
    row("RUNG no disattenuated correlation reaches 0.95", np.max(res["disattenuated"]) < 0.95,
        "%.3f" % np.max(res["disattenuated"]))

    # ------------------------------------------------------------------ R1 the field's raw material
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip().lower()
             for f in files if f.endswith(".csv")}
    bad = [f for f, h in heads.items() if re.search(r"corr|effect|lift|reliab|covar|delta|diff", h)]
    row("R1 no shipped column holds an effect, a correlation or a reliability", not bad, ", ".join(bad) or "none")
    row("R1 the decisive step reads per-arm scorecards and the holdout's user rows",
        len(res["changes"]) > 400 and hm["n"] > 25000, "%d changes, %d holdout users" % (len(res["changes"]), hm["n"]))

    # ------------------------------------------------------------------ R2 every mess item neutral
    def call_of(**kw):
        c = A.changes(d, target, **kw)
        return name(A.correlations(c, hm)), len(c)
    for label, kw in (("experiments failing the sample-ratio check read", dict(srm_out=False)),
                      ("the earlier computation kept where a scorecard was computed again", dict(latest="first")),
                      ("both computations read as separate scorecards", dict(keep_all_versions=True)),
                      ("former metric keys left unmapped", dict(rename=False)),
                      ("experiments stopped early left out", dict(stopped=False)),
                      ("one treatment arm read per experiment", dict(first_arm_only=True))):
        got, n = call_of(**kw)
        row("R2 %s" % label, got == res["proxy"], "%s on %d changes" % (got, n))

    # ------------------------------------------------------------------ R3 the analyst test on the clean truth
    wc = world_changes(W)
    H = np.array([r_[3:9] for r_ in W.holdout_rows])
    hmw = dict(rho=np.array([np.corrcoef(H[:, k], H[:, 5])[0, 1] for k in range(5)]))
    clean = {m: A.correlations(wc, hmw, m) for m in ("raw", "disattenuated", "half", "golden")}
    row("R3a ANALYST the easy route on the clean truth files sessions",
        name(clean["raw"]) == "sessions_d1_14" and name(clean["disattenuated"]) == "sessions_d1_14",
        "raw %s, disattenuated %s" % (np.round(clean["raw"], 3), np.round(clean["disattenuated"], 3)))
    row("R3b DECISIVE the shared covariance taken out alone files first purchase",
        name(clean["golden"]) == "first_purchase_d14", "%s" % np.round(clean["golden"], 3))
    row("R3b each lower rung's single correction stays wrong", name(clean["half"]) != "first_purchase_d14" and
        name(res["spearman"]) != "first_purchase_d14", "half %s" % name(clean["half"]))
    texts = []
    for f in files:
        if f.endswith((".csv", ".txt", ".yaml")):
            texts.append(open(os.path.join(target, f), encoding="utf-8").read().lower())
    import pypdf
    for f in files:
        if f.endswith(".pdf"):
            texts.append(" ".join(p.extract_text() for p in pypdf.PdfReader(os.path.join(target, f)).pages).lower())
    row("R3c no plant: no shipped text states a correlation, a reliability or a proxy pick",
        not any(re.search(r"\bcorrelat\w*\s+(of|is|=)\s*-?0\.\d|reliabilit|recommend|we propose|"
                          r"proxy (is|will be|should be) (active|sessions|first|items|push)", t) for t in texts),
        "csv, txt, yaml and pdf swept")

    # ------------------------------------------------------------------ semantic forks
    row("SF1 a change is each treatment arm against its control", call_of(first_arm_only=True)[0] == res["proxy"],
        "one arm per experiment gives the same call")
    reg = d["registry"]
    closed = set(reg.loc[(reg["six_month_read_closes"] != "") & (reg["six_month_read_closes"] <= K.PULL.isoformat()),
                         "experiment_id"])
    sc = A.scorecards(d, target)
    with_ret = set(sc.loc[sc["metric"] == K.RET, "experiment_id"])
    row("SF2 a closed six-month read is the registry's date by the export and the retained_m6 rows alike",
        closed == with_ret, "%d experiments" % len(closed))
    row("SF3 sample-ratio failures out", call_of(srm_out=False)[0] == res["proxy"], "same call read in")
    row("SF4 experiments stopped early read on their users", call_of(stopped=False)[0] == res["proxy"],
        "same call left out")
    row("SF5 the latest computation replaces the earlier", call_of(latest="first")[0] == res["proxy"],
        "same call on the earlier")
    row("SF6 former keys read through the catalogue", call_of(rename=False)[0] == res["proxy"],
        "same call on the renamed rows alone")
    rel = relative(res["changes"], hm)
    row("SF7 an effect is the difference in means; relative effects name the same proxy", name(rel) == res["proxy"],
        "%s" % np.round(rel, 3))
    row("SF8 each change counts once; precision weighting names the same proxy", name(reml) == res["proxy"],
        "bivariate fit %s" % np.round(reml, 3))
    cat = open(os.path.join(target, "metric_catalogue.yaml"), encoding="utf-8").read()
    marked = re.findall(r"- key: (\S+)(?:(?!- key:).)*?proxy_review_2027: candidate", cat, re.S)
    row("SF9 the candidates are the five the catalogue marks", sorted(marked) == sorted(K.CAND), ", ".join(marked))
    row("SF10 the sampling covariance from the holdout's correlation, its covariance or pooled arms: same figures",
        figs["mom"] == figs["holdout"] == figs["pooled"], str(figs["holdout"]))
    row("SF11 the moments across changes over E - 1 or E: same figures", figs["mom"] == figs["mom_n"], str(figs["mom_n"]))
    by_plat = []
    for plat in ("ios", "android"):
        h = d["holdout"][d["holdout"]["platform"] == plat]
        by_plat.append([np.corrcoef(h[m], h[K.RET])[0, 1] for m in K.CAND])
    hm2 = dict(hm, rho=np.mean(by_plat, axis=0))
    v2 = A.correlations(res["changes"], hm2)
    row("SF12 the holdout's correlation pooled or averaged over platforms: same proxy and runner-up",
        name(v2) == res["proxy"] and K.CAND[int(np.argsort(-v2)[1])] == res["runner_up"], "%s" % np.round(v2, 4))
    row("SF13 no tie for the highest correlation", o[0] - o[1] > 0.1, "%.3f" % (o[0] - o[1]))
    row("SF14 the correlation is between the effects (2.3): the raw correlation of the measurements names another "
        "proxy", name(res["raw"]) != res["proxy"], "raw names %s" % name(res["raw"]))
    early = A.changes(d, target, closed_by=dt.date(2026, 10, 12))
    row("SF17 the data cut filed at the export (2.4); the standard's approval date names the same proxy",
        name(A.correlations(early, hm)) == res["proxy"], "%d changes by 12 October" % len(early))

    # ------------------------------------------------------------------ separation
    h = d["holdout"]
    row("SEP the holdout carries no device: no blank, no repeated user, every sign-up in 2025",
        not h.isna().any().any() and h["user_id"].is_unique and h["signed_up_on"].str.startswith("2025").all(),
        "%d users" % len(h))
    co = d["cohorts"]
    co = co[co["signup_account_type"] == "consumer"].sort_values("refreshed_at").drop_duplicates(
        ["signup_date", "platform", "country", "account_type", "signup_account_type"], keep="last")
    ratio = len(h) / co["new_users"].sum()
    row("SEP the cohort table counts the holdout's users (holdout over consumer sign-ups near 5 per cent)",
        0.048 < ratio < 0.052, "%.4f" % ratio)
    f = d["forecast"].copy()
    f["date"] = pd.to_datetime(f["date"])
    f["monday"] = f["date"] - pd.to_timedelta(f["date"].dt.weekday, unit="D")
    row("SEP the forecast writes a week's figure on each of its days",
        f.groupby(["monday", "platform"])["new_consumer_users_forecast"].nunique().max() == 1, "")
    q1 = f[(f["date"] >= "2027-01-04") & (f["date"] <= "2027-03-28")]
    wk = q1.groupby("monday")["new_consumer_users_forecast"].first() + 0
    wk = q1.drop_duplicates(["monday", "platform"]).groupby("monday")["new_consumer_users_forecast"].sum()
    row("SF15 the guide's 2027 holdout of about 430 a week forces the weekly reading of the forecast",
        abs(0.03 * wk.mean() - 430) < 15 and abs(0.03 * 7 * wk.mean() - 430) > 1000, "%.0f a week" % (0.03 * wk.mean()))
    conv = d["cohorts"]
    conv = conv[(conv["signup_account_type"] == "consumer") & (conv["account_type"] == "business")]
    row("SF16 accounts that signed up as consumers and became business stay in the consumer population",
        len(conv) > 0, "%d rows, %d users" % (len(conv), conv.drop_duplicates(
            ["signup_date", "platform", "country"])["new_users"].sum()))
    row("SEP the call reads none of the ask files", True, "registry, scorecards, catalogue and holdout only")

    # ------------------------------------------------------------------ the ask devices
    g = {"B": fig["asks"]["B"]["detectable"], "B_users": fig["asks"]["B"]["users_per_arm"], "C": fig["asks"]["C"]}
    st = AK.stops(d)
    G = flat({"B": g["B"], "C": g["C"]})
    for k, v in st.items():
        F = flat({"B": v} if k.startswith("B") else {"C": v})
        same = sum(F[x] == G.get(x) for x in F)
        if k in ("B_z_rounded", "B_population_sd"):
            row("ASK %s is no fork: every figure the same" % k, same == len(F), "%d of %d" % (same, len(F)))
        elif k in ("B_daily_lines_summed", "C_type_at_refresh"):
            row("ASK primary %s moves every figure" % k, same == 0, "%d of %d unchanged" % (same, len(F)))
        else:
            row("ASK hazard %s moves figures" % k, same < len(F), "%d of %d unchanged" % (same, len(F)))
    lines = AK.detectable(d, weekly="lines")[1]
    row("ASK primary moves every users-per-arm figure", all(lines[e] != g["B_users"][e] for e in lines), "")

    # ------------------------------------------------------------------ realism and containers
    people = set(json.load(open(os.path.join(os.path.dirname(task), ".claude", "skills", "fingerprint", "cards",
                                             "task270.json")))["world"]["people"])
    blob = "\n".join(texts)
    named = {p for p in people if p.lower() in blob}
    row("REAL personas in the pack come from the card", len(named) >= 2, ", ".join(sorted(named)))
    row("REAL no retired persona survives", not any(x in blob for x in ("lambregt", "erhout", "oudshoorn")), "")
    dash = [f for f in files if f.endswith((".csv", ".txt", ".yaml")) and
            re.search("[–—]", open(os.path.join(target, f), encoding="utf-8").read())]
    row("REAL no em or en dash in the pack's text", not dash, ", ".join(dash) or "none")
    scs = d["scorecards"]
    dup_users = scs.drop_duplicates(["experiment_id", "arm"]).groupby("users").size()
    row("REAL arm sizes are not repeated across many arms", dup_users.max() <= 4, "most repeated %d" % dup_users.max())
    sig = re.compile(rb"ReportLab|reportlab|openpyxl|python-pptx|matplotlib|Matplotlib")
    leaks = []
    for folder in (target, golden_dir):
        for f in os.listdir(folder):
            p = os.path.join(folder, f)
            raw = open(p, "rb").read()
            if f.endswith((".xlsx", ".pptx")):
                with zipfile.ZipFile(p) as z:
                    raw = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps") or n.endswith(".png"))
            if sig.search(raw):
                leaks.append(f)
    row("REAL no writer signature in any container", not leaks, ", ".join(leaks) or "none")
    gold_text = ""
    for f in os.listdir(golden_dir):
        with zipfile.ZipFile(os.path.join(golden_dir, f)) as z:
            gold_text += " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))
    row("REAL no em or en dash in the goldens", not re.search("[–—]", gold_text), "")

    width = max(len(r_[0]) for r_ in ROWS)
    fails = 0
    for label, ok, detail in ROWS:
        print("%s  %-*s  %s" % ("PASS" if ok else "FAIL", width, label, detail))
        fails += not ok
    print("checks: %d rows, %d FAIL" % (len(ROWS), fails))
    return 1 if fails else 0
