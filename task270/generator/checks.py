"""Assertions on the build: the input gates, the golden reproduced from the cut pack and from the generator's clean
truth (R1 the raw material ships, R2 each Layer 1 item neutral, R3a the analyst test, R3b the decisive step alone,
R3c nothing planted), the ladder, every shortcut a reader might take, the golden's estimator family and its
half-point grid, the two ask devices on the careful path and the over-cleaner's, the separation of the asks from the
call, and the realism sweep."""
import datetime as dt
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A      # noqa: E402
import common as K        # noqa: E402
import pack as PK         # noqa: E402
import routes as RT       # noqa: E402

FAILS = []
COUNT = [0]


def check(label, ok, detail=""):
    COUNT[0] += 1
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % (detail,)) if not (isinstance(detail, str) and detail == "") else ""))


def half(x):
    return np.floor(np.asarray(x, float) * 2 + 0.5) / 2


def half_edge(x):
    return 0.25 - abs(float(x) - float(half(x)))


def dec_edge(x, nd=1):
    q = 10 ** nd
    return 0.5 / q - abs(float(x) - round(float(x) * q) / q)


def top2(s):
    return frozenset(s.sort_values(ascending=False).index[:2])


def third(s):
    return s.sort_values(ascending=False).index[2]


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    w = b["w"]
    P = res["P"]
    GOLD = frozenset(fig["call"]["sites"])
    NAIVE = frozenset(["Thurlwick", "Penwardine"])
    below = fig["call"]["below"]
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
    check("GATE no file named after the stump", not any(re.search(r"practice|retest|gain|known|issue", f) for f in files))
    # ---------------------------------------------------------------- the golden from the pack and from the truth
    df = RT.frame(w)
    out = RT.routes(df)
    gold_truth = out["gold"]
    gold_pack = res["decline"]
    check("GOLDEN the pack's decline equals the clean truth's in every clinic",
          all(abs(gold_truth[c] - gold_pack[c]) < 1e-9 for c in K.NAMES),
          max(abs(gold_truth[c] - gold_pack[c]) for c in K.NAMES))
    check("GOLDEN the pack's population equals the clean truth's",
          all(int(out["_n"].get(c, 0)) == int(res["n"].get(c, 0)) for c in K.NAMES), res["n"].to_dict())
    check("GOLDEN the pack's gain equals the clean truth's", abs(out["_P"][0] - res["gain"]) < 1e-9, res["gain"])
    check("GOLDEN the recruiting pair is Quarndale and Thurlwick", GOLD == frozenset(["Quarndale", "Thurlwick"]),
          fig["call"]["sites"])
    check("GOLDEN the first clinic below is Mosswick", below == "Mosswick", below)
    # ---------------------------------------------------------------- R1 the raw material ships
    s = P["sittings"]
    check("R1 every sitting ships with its date, total and clinic", s.date.notna().all() and s.total.notna().all() and
          s.clinic.notna().all(), len(s))
    check("R1 the decisive computation reads each patient's dated totals (5,000 or more patients, 15,000 or more "
          "sittings in the population)", res["frame"].pid.nunique() >= 5000 and len(res["frame"]) >= 15000,
          (res["frame"].pid.nunique(), len(res["frame"])))
    for f in files:
        if f.endswith(".csv"):
            cols = re.split(r"[,_ ]", open(os.path.join(target, f)).readline().strip().lower())
            for wd in ("slope", "decline", "rate", "gain", "practice", "retest", "sitting", "visit"):
                check("R1 no shipped column names the deciding quantity (%s, %s)" % (f, wd), wd not in cols)
    # ---------------------------------------------------------------- R3 on the clean truth
    truth = out["truth"]
    check("R3 the clean truth's two fastest clinics (true rates) are the golden pair", top2(truth) == GOLD,
          truth.sort_values(ascending=False).round(3).to_dict())
    check("R3a the analyst test: the slope through every sitting on the clean truth files Thurlwick and Penwardine",
          top2(out["naive"]) == NAIVE, out["naive"].sort_values(ascending=False).round(3).to_dict())
    check("R3a Quarndale is fourth or lower on the slope through every sitting", RT.rank_of(out["naive"], "Quarndale") >= 4,
          RT.rank_of(out["naive"], "Quarndale"))
    check("R3b the decisive step alone (the gain separated) files the golden pair", top2(gold_truth) == GOLD)
    check("SF9 on the pack, the slope of the recorded totals names Thurlwick and Penwardine and the trend net of the "
          "gain names the golden pair (the decisive step, not a reading)",
          top2(res["naive"]) == NAIVE and top2(res["decline"]) == GOLD,
          ("+".join(res["naive"].sort_values(ascending=False).index[:2]),
           "+".join(res["decline"].sort_values(ascending=False).index[:2])))
    nv = out["naive"]
    check("R3a margin: the naive pair's second leads the third by 0.10 point or more",
          min(nv["Thurlwick"], nv["Penwardine"]) - nv.drop(["Thurlwick", "Penwardine"]).max() >= 0.10,
          round(min(nv["Thurlwick"], nv["Penwardine"]) - nv.drop(["Thurlwick", "Penwardine"]).max(), 3))
    g = gold_truth.sort_values(ascending=False)
    check("LADDER golden: the pair's second leads the first clinic below by 0.15 point or more",
          g.iloc[1] - g.iloc[2] >= 0.15, round(g.iloc[1] - g.iloc[2], 3))
    check("LADDER golden: the first clinic below leads the fourth by 0.08 point or more",
          g.iloc[2] - g.iloc[3] >= 0.08, round(g.iloc[2] - g.iloc[3], 3))
    # ---------------------------------------------------------------- shortcuts that skip the decisive step
    for k in RT.NO_INSIGHT:
        check("SHORTCUT %s does not name the golden pair" % k, top2(out[k]) != GOLD,
              "+".join(out[k].sort_values(ascending=False).index[:2]))
    check("SHORTCUT each patient's first completed sitting dropped (a practice guard that leaves out the patients "
          "with two sittings in the period) does not name the golden pair and puts Quarndale last",
          top2(out["dropfirst"]) != GOLD and RT.rank_of(out["dropfirst"], "Quarndale") == 8,
          "+".join(out["dropfirst"].sort_values(ascending=False).index[:2]))
    pop = RT.population(df)
    # ---------------------------------------------------------------- the write-up's words about the rivals (H3)
    new = (pop.groupby("pid").first_t.first() >= 0).groupby(RT.clinic_of(pop)).mean()
    check("WRITEUP Penwardine is fourth once the gain is out", list(g.index).index("Penwardine") == 3,
          list(g.index).index("Penwardine") + 1)
    check("WRITEUP nearly half of Penwardine's patients sat their first ACE-III before 2022 (40 to 50 per cent)",
          0.40 <= 1 - new["Penwardine"] < 0.50, round(1 - new["Penwardine"], 3))
    check("WRITEUP most of Mosswick's patients are new to the test (over 60 per cent)", new["Mosswick"] > 0.60,
          round(new["Mosswick"], 3))
    check("WRITEUP Quarndale is last on the slope through every sitting", RT.rank_of(nv, "Quarndale") == 8,
          RT.rank_of(nv, "Quarndale"))
    check("WRITEUP nearly all of Quarndale's patients are new to the test (95 per cent or more)",
          new["Quarndale"] >= 0.95, round(new["Quarndale"], 3))
    mm = RT.mixed_models(pop)
    for ax in RT.AXES:
        for kind, what in (("rs", "random intercepts and slopes"), ("ri", "random intercepts only")):
            key = "%s_%s" % (kind, ax)
            sr = mm[key].sort_values(ascending=False)
            check("SHORTCUT %s without the step (%s, each patient at the paper's clinic) converges and does not name "
                  "the golden pair" % (what, ax), mm["_conv_" + key] and top2(mm[key]) != GOLD, "+".join(sr.index[:2]))
            check("SHORTCUT %s without the step (%s): Quarndale 0.10 point or more below the second" % (what, ax),
                  sr.iloc[1] - mm[key]["Quarndale"] >= 0.10, round(sr.iloc[1] - mm[key]["Quarndale"], 3))
    acc = RT.accidental(pop)
    for key in ("pooled_t_win", "pooled_t_dx", "perrow_rs_t_cal", "perrow_rs_t_cal_stayers"):
        sr = acc[key].sort_values(ascending=False)
        print("INFO  ACCIDENTAL %s: %s (third %s, %.3f behind the second)" % (key, "+".join(sr.index[:2]), sr.index[2],
                                                                           sr.iloc[1] - sr.iloc[2]))
    check("ACCIDENTAL the calendar-time model with each sitting at its own clinic loses the golden pair once the "
          "patients seen at two clinics are left out (they carry it)", top2(acc["perrow_rs_t_cal"]) == GOLD and
          top2(acc["perrow_rs_t_cal_stayers"]) != GOLD and acc["_conv_perrow_rs_t_cal"], acc["_movers"])
    # ---------------------------------------------------------------- the golden's estimator family
    fam = family(df, pop, mm)
    for nm, sr in fam["declines"].items():
        check("FAMILY (SF11 least squares or first to last) %s names the golden pair and the first clinic below" % nm,
              top2(sr) == GOLD and third(sr) == below, "+".join(sr.sort_values(ascending=False).index[:3]))
    tab = pd.DataFrame(fam["declines"])
    lo, hi = tab.min(axis=1), tab.max(axis=1)
    for c in K.NAMES:
        check("FAMILY %s: every member lands on the golden's half point (%.1f), 0.01 or more inside the bin"
              % (c, fig["decline"][c]), half(lo[c]) == half(hi[c]) == fig["decline"][c] and
              min(half_edge(lo[c]), half_edge(hi[c])) >= 0.01,
              (round(lo[c], 3), round(hi[c], 3), round(min(half_edge(lo[c]), half_edge(hi[c])), 3)))
    gains = fam["gains"]
    check("FAMILY every estimate of the gain rounds to %.1f, 0.05 or more inside the bin" % fig["gain"],
          all(half(v) == fig["gain"] and half_edge(v) >= 0.05 for v in gains.values()),
          {k: round(v, 3) for k, v in gains.items()})
    for ax in RT.AXES:
        sr = mm["rs_step_" + ax].sort_values(ascending=False)
        print("INFO  RANDOM EFFECTS with the step (%s): gain %.3f, %s" % (ax, mm["_P_rs_step_" + ax],
                                                                       " ".join("%s %.3f" % (c[:4], v) for c, v in
                                                                                sr.items())))
        sr = mm["mundlak_" + ax]
        check("FAMILY the random-slopes model with the step and the patient's mean of it (%s) converges and names the "
              "golden pair and the first clinic below" % ax, mm["_conv_mundlak_" + ax] and top2(sr) == GOLD and
              third(sr) == below, "+".join(sr.sort_values(ascending=False).index[:3]))
    for ax in ("t_cal", "t_win"):
        check("FAMILY the patient's mean of the step is far from zero on %s (|z| 3 or more), so the random-effects step "
              "without it leans on comparisons between patients" % ax, abs(mm["_z_mstep_" + ax]) >= 3,
              round(mm["_z_mstep_" + ax], 1))
    cross = []
    for gn in np.arange(1.0, 4.001, 0.05):
        v = pop.copy()
        v["a"] = v.s - gn * v.step
        cross.append((round(gn, 2), top2(RT.cavg(v, RT.slopes(v, "a"))) == GOLD))
    lowest = min(gn for gn, _ in cross if all(o for q, o in cross if q >= gn))
    check("FAMILY every gain from 1.40 to 4.00 names the golden pair (lowest gain that does, on a 0.05 grid)",
          lowest <= 1.40, lowest)
    # ---------------------------------------------------------------- R2 each Layer 1 item, mishandled
    for name, sr in layer1_mishandled(target, P).items():
        check("R2 neutral: %s keeps the call" % name, top2(sr) == GOLD,
              "+".join(sr.sort_values(ascending=False).index[:3]))
    # ---------------------------------------------------------------- the semantic fork table
    sf_checks(target, P, fig, gold_pack)
    # ---------------------------------------------------------------- the asks
    asks(P, fig, w)
    # ---------------------------------------------------------------- separation
    check("SEPARATION the call reads no episode, appointment or tracker row (computed from the main files alone)",
          separation(target, P, fig))
    # ---------------------------------------------------------------- documents and realism
    documents(target)
    realism(target, P, w)
    containers(task)
    import cracker
    cr = cracker.run(task, quiet=True)
    check("CRACKER keeps none of the 32 ask figures", cr["cracker_hits"] == 0, cr["cracker_hits"])
    check("CRACKER the mirror keeps under 35 per cent of the ask figures", cr["mirror_hits"] < 0.35 * cr["total"],
          cr["mirror_hits"])
    check("CRACKER the pair ceiling is 40 or under", cr["pair"] <= 40.0, round(cr["pair"], 1))
    print("checks: %d, failed: %d" % (COUNT[0], len(FAILS)))
    for f in FAILS:
        print("  failed:", f)
    return 0 if not FAILS else 1


def family(df, pop, mm):
    """The gain from every licensed estimator and each clinic's average of its patients' own declines net of it."""
    gains = {"within, window": RT.fe(pop)[0], "within, whole record": RT.fe(RT.all_history(df))[0]}
    ww = pop.copy()
    ww["k2"] = (ww.k >= 2).astype(float)
    gains["within, third-sitting term"] = RT.fe(ww, ("step", "k2"))[0]
    gains["random slopes, time since first sitting"] = mm["_P_rs_step_t_dx"]
    for ax, nm in (("t_cal", "calendar time"), ("t_win", "time in the period"), ("t_dx", "time since first sitting")):
        gains["random slopes with the patient's mean of the step, %s" % nm] = mm["_P_mundlak_" + ax]
    declines = {}
    for nm, p in gains.items():
        v = pop.copy()
        v["a"] = v.s - p * v.step
        declines[nm + " / least squares"] = RT.cavg(v, RT.slopes(v, "a"))
        declines[nm + " / first to last"] = RT.cavg(v, RT.endpoint(v, "a"))
    return dict(gains=gains, declines=declines)


def sf_checks(target, P, fig, gold):
    GOLD = frozenset(fig["call"]["sites"])

    def call_with(sittings=None, dx=None, window=None, scope=None):
        Q = dict(P)
        if dx is not None:
            Q["dx"] = dx
        s = Q["sittings"]
        w0, w1 = window or K.WINDOW
        lat = PK.latest_dx(Q)
        f = s[s.completed & (s.date >= w0) & (s.date <= w1)].copy()
        f["latest"] = f.nhs.map(lat)
        keep = scope or PK.in_scope
        f = f[f.latest.fillna("").map(keep)]
        if scope == "ever":
            pass
        f = f[f.groupby("nhs").date.transform("size") >= 2].copy()
        f["t"] = (pd.to_datetime(f.date) - pd.Timestamp(K.WINDOW[0])).dt.days / 365.25
        f["step"] = (f.k >= 1).astype(float)
        f["s"] = f.total.astype(float)
        f["pid"] = f.nhs
        return A.call(f)["decline"]
    sr = call_with(scope=lambda c: (c.startswith("F00") or c.startswith("G30") or c == "F06.7") and c != "F00.2")
    check("SF1 mixed Alzheimer's and vascular dementia (F00.2) left out keeps the call", top2(sr) == GOLD,
          "+".join(sr.sort_values(ascending=False).index[:3]))
    d = P["dx"]
    Q = dict(P)
    lat_extract = d[d.date <= K.EXTRACT].groupby("nhs").tail(1).set_index("nhs").code
    s = P["sittings"]
    f = s[s.completed & (s.date >= K.WINDOW[0]) & (s.date <= K.WINDOW[1])].copy()
    f = f[f.nhs.map(lat_extract).fillna("").map(PK.in_scope)]
    f = f[f.groupby("nhs").date.transform("size") >= 2].copy()
    f["t"] = (pd.to_datetime(f.date) - pd.Timestamp(K.WINDOW[0])).dt.days / 365.25
    f["step"] = (f.k >= 1).astype(float)
    f["s"] = f.total.astype(float)
    f["pid"] = f.nhs
    sr = A.call(f)["decline"]
    check("SF2 the latest diagnosis on the record at the extract (2 October) keeps the call", top2(sr) == GOLD)
    ever = set(d[d.code.map(PK.in_scope) & (d.date <= K.WINDOW[1])].nhs)
    f = s[s.completed & (s.date >= K.WINDOW[0]) & (s.date <= K.WINDOW[1]) & s.nhs.isin(ever)].copy()
    f = f[f.groupby("nhs").date.transform("size") >= 2].copy()
    f["t"] = (pd.to_datetime(f.date) - pd.Timestamp(K.WINDOW[0])).dt.days / 365.25
    f["step"] = (f.k >= 1).astype(float)
    f["s"] = f.total.astype(float)
    f["pid"] = f.nhs
    sr = A.call(f)["decline"]
    check("SF2 any Alzheimer's or MCI diagnosis ever on the record keeps the call", top2(sr) == GOLD,
          "+".join(sr.sort_values(ascending=False).index[:3]))
    sr = call_with(window=(K.WINDOW[0], K.WINDOW[1] - dt.timedelta(days=1)))
    check("SF4 the period's last day left out keeps the call", top2(sr) == GOLD)
    w = PK.frame(P)
    v = w.copy()
    gn = A.gain(v)[0]
    v["a"] = v.s - gn * v.step
    b = A.slopes(v, "a")
    cl = A.clinic_of(v)
    wt = ((v.t - v.groupby("pid").t.transform("mean")) ** 2).groupby(v.pid).sum()
    sr = -((b * wt).groupby(cl).sum() / wt.groupby(cl).sum())
    check("SF7 each patient weighted by the spread of their assessment dates keeps the call", top2(sr) == GOLD,
          "+".join(sr.sort_values(ascending=False).index[:3]))
    sr = -(b.groupby(cl).median())
    check("SF8 the median patient in place of the average keeps the call", top2(sr) == GOLD,
          "+".join(sr.sort_values(ascending=False).index[:3]))
    g = gold.sort_values(ascending=False)
    check("SF10 the unrounded figures order the clinics with no tie (the pair's second 0.15 or more above the first "
          "clinic below)", g.is_unique and g.iloc[1] - g.iloc[2] >= 0.15, round(g.iloc[1] - g.iloc[2], 3))
    cis = pd.read_csv(os.path.join(target, K.FILES["cis_ace"]), dtype=str, keep_default_na=False)
    day = cis.assessment_date.str[:2].astype(int)
    check("SF13 a month-first read of the CIS dates fails loudly (40 per cent or more of days above 12)",
          (day > 12).mean() >= 0.4, round(float((day > 12).mean()), 3))


def layer1_mishandled(target, P):
    """The golden method with one Layer 1 item mishandled at a time."""
    out = {}
    base = P["sittings"]

    def golden_from(s, dxf=None):
        Q = dict(P)
        Q["sittings"] = s
        if dxf is not None:
            Q["dx"] = dxf
        w = PK.frame(Q)
        return A.call(w)["decline"]
    # abandoned forms and incomplete sets read as completed
    s = base.copy()
    s["completed"] = True
    s["k"] = s.groupby("nhs").completed.transform(lambda c: c.astype(int).cumsum().shift(fill_value=0))
    out["SF3 abandoned and incomplete sittings counted"] = golden_from(s)
    # sets entered in error kept
    obs = pd.read_csv(os.path.join(target, K.FILES["epr_obs"]), dtype=str, keep_default_na=False)
    eie = obs[(obs.set_status == "Entered in error") & (obs.item_code == "ACE3_TOTAL")].copy()
    eie["nhs"] = PK.digits(eie.nhs_number)
    eie["date"] = pd.to_datetime(eie.performed_at.str[:10]).dt.date
    eie["clinic"] = eie.site_code.map(P["site2clinic"])
    eie["completed"] = True
    eie["total"] = eie.value.astype(int)
    eie["system"] = "EPR"
    eie["set"] = eie.obs_set_id
    s = pd.concat([base[["nhs", "date", "clinic", "completed", "total", "system", "set"]],
                   eie[["nhs", "date", "clinic", "completed", "total", "system", "set"]]], ignore_index=True)
    s = s.sort_values(["nhs", "date", "set"]).reset_index(drop=True)
    s["k"] = s.groupby("nhs").completed.transform(lambda c: c.astype(int).cumsum().shift(fill_value=0))
    out["sets entered in error kept"] = golden_from(s)
    # merged hospital numbers left out of the join
    pmi = P["pmi"]
    merged = set(pmi[pmi.record_status != "Active"].hpn)
    cis = pd.read_csv(os.path.join(target, K.FILES["cis_ace"]), dtype=str, keep_default_na=False)
    drop_sets = set(cis[cis.hpn.str.strip().isin(merged)].form_id)
    s = base[~base.set.isin(drop_sets)].copy()
    s["k"] = s.groupby("nhs").completed.transform(lambda c: c.astype(int).cumsum().shift(fill_value=0))
    out["SF12 merged hospital numbers not joined"] = golden_from(s)
    # NHS numbers written with spaces not matched
    spaced = set(PK.digits(pmi[pmi.nhs_number.str.contains(" ")].nhs_number))
    s = base[~(base.nhs.isin(spaced) & (base.system == "CIS"))].copy()
    s["k"] = s.groupby("nhs").completed.transform(lambda c: c.astype(int).cumsum().shift(fill_value=0))
    out["spaced NHS numbers in the index not matched"] = golden_from(s)
    # the migrated problem-list entries left out
    ed = pd.read_csv(os.path.join(target, K.FILES["epr_dx"]), dtype=str, keep_default_na=False)
    mig = ed[ed.source == "CIS migration"]
    keyset = set(zip(PK.digits(mig.nhs_number), pd.to_datetime(mig.recorded_on).dt.date, mig.problem_code))
    d = P["dx"]
    dxf = d[~d.apply(lambda r: (r.nhs, r.date, r.code) in keyset, axis=1)]
    out["migrated diagnoses left out"] = golden_from(base, dxf)
    # each patient placed at their first clinic in the period
    Q = dict(P)
    w = PK.frame(Q)
    first_clinic = w.sort_values(["pid", "t"]).groupby("pid").clinic.first()
    w2 = w.copy()
    w2["clinic"] = w2.pid.map(first_clinic)
    out["SF5 patients placed at their first clinic in the period"] = A.call(w2)["decline"]
    # time in years of 365 days
    w3 = w.copy()
    w3["t"] = w3.t * 365.25 / 365.0
    out["SF6 years of 365 days"] = A.call(w3)["decline"]
    return out


def asks(P, fig, w):
    a, a_rows = A.ask_a(P)
    b, b_rows = A.ask_b(P)
    # the clean truth
    day = K.WINDOW[1]
    import records as RC
    tru = {c: [0, 0] for c in K.NAMES}
    for p in w["patients"]:
        c = RC.under_follow_up(p, day)
        if c is None:
            continue
        dxs = sorted([x for x in p["dx"] if x["entered"] <= day], key=lambda x: (x["entered"], x["given"]))
        if dxs and dxs[-1]["code"] in K.IN_SCOPE:
            bb = p["dob"]
            age = K.TRIAL_ENTRY.year - bb.year - ((K.TRIAL_ENTRY.month, K.TRIAL_ENTRY.day) < (bb.month, bb.day))
            tru[c][0] += 1
            tru[c][1] += age <= K.AGE_LIMIT
    for c in K.NAMES:
        check("ASK A the golden equals the clean truth (%s)" % c, [a[c]["under"], a[c]["age_ok"]] == tru[c],
              (a[c]["under"], a[c]["age_ok"], tru[c]))
    # the careful path: open episodes, Spine deaths, latest diagnosis, no look at the appointments
    careful = ask_a_careful(P)
    for c in K.NAMES:
        check("ASK A device: the careful path misses %s's patients under follow-up" % c,
              careful[c][0] != a[c]["under"], (careful[c][0], a[c]["under"]))
        check("ASK A device: the careful path misses %s's patients 85 or under" % c,
              careful[c][1] != a[c]["age_ok"], (careful[c][1], a[c]["age_ok"]))
    over = ask_a_careful(P, keyword=True)
    for c in K.NAMES:
        check("ASK A over-cleaner (every outcome naming a discharge) misses %s" % c,
              over[c][0] != a[c]["under"], (over[c][0], a[c]["under"]))
    # Ask B: the truth from the world
    a0, a1 = K.ASK_YEAR
    tb = {c: [] for c in K.NAMES}
    for p in w["patients"]:
        if not p["dx"]:
            continue
        g = p["dx"][0]["given"]
        if a0 <= g <= a1 and p["registered"] >= K.EPR_GO_LIVE - dt.timedelta(days=400):
            if p["registered"] < K.EPR_GO_LIVE and not (p.get("first") and p["first"] >= K.EPR_GO_LIVE):
                continue
            tb[p["clinic0"]].append((g - p["registered"]).days)
    for c in K.NAMES:
        v = np.array(tb[c])
        check("ASK B the golden equals the clean truth (%s)" % c,
              len(v) == b[c]["n"] and abs(100.0 * (v <= 42).mean() - b[c]["share"]) < 1e-9 and
              abs(v.mean() - b[c]["mean"]) < 1e-9, (len(v), b[c]["n"]))
        check("ASK B %s's figures sit off their rounding edges" % c,
              dec_edge(b[c]["share"]) >= 0.002 and dec_edge(b[c]["mean"]) >= 0.002,
              (round(b[c]["share"], 4), round(b[c]["mean"], 4)))
    careful_b = ask_b_careful(P)
    for c in K.NAMES:
        check("ASK B device: the tracker's own dates miss %s's share" % c,
              round(careful_b[c][0], 1) != fig["ask_b"]["within_42_days_pct"][c],
              (round(careful_b[c][0], 1), fig["ask_b"]["within_42_days_pct"][c]))
        check("ASK B device: the tracker's own dates miss %s's average" % c,
              round(careful_b[c][1], 1) != fig["ask_b"]["average_days"][c],
              (round(careful_b[c][1], 1), fig["ask_b"]["average_days"][c]))
    over_b = ask_b_feedback_only(P)
    for c in K.NAMES:
        check("ASK B over-cleaner (the feedback appointment only) misses %s" % c,
              round(over_b[c][0], 1) != fig["ask_b"]["within_42_days_pct"][c] and
              round(over_b[c][1], 1) != fig["ask_b"]["average_days"][c], over_b[c])
    vals = list(fig["ask_a"]["under_follow_up"].values())
    check("ASK A no two clinics share a figure", len(set(vals)) == len(vals))


def ask_a_careful(P, keyword=False):
    day = K.WINDOW[1]
    ep = P["episodes"].copy()
    ep["nhs"] = PK.digits(ep.nhs_number)
    ep["start"] = pd.to_datetime(ep.episode_start).dt.date
    ep["end"] = pd.to_datetime(ep.episode_end.replace("", None)).dt.date
    ep["clinic"] = ep.site_code.map(P["site2clinic"])
    op = ep[(ep.start <= day) & (ep.end.isna() | (ep.end > day))]
    if keyword:
        ap = P["appts"]
        hit = ap[ap.outcome.str.contains("discharge|care passed", case=False)]
        op = op[~op.nhs.isin(set(PK.digits(hit.nhs_number)))]
    pmi = P["pmi"][P["pmi"].record_status == "Active"].set_index("nhs")
    dod = pd.to_datetime(pmi.date_of_death.replace("", None)).dt.date
    op = op[~op.nhs.map(dod).apply(lambda d: d is not None and not pd.isna(d) and d <= day)]
    lat = PK.latest_dx(P, day)
    op = op[op.nhs.map(lat).fillna("").map(PK.in_scope)]
    dob = pd.to_datetime(pmi.date_of_birth).dt.date
    age = op.nhs.map(dob).apply(lambda b: K.TRIAL_ENTRY.year - b.year - ((1, 1) < (b.month, b.day)))
    op = op.assign(age=age.values)
    return {c: (op[op.clinic == c].nhs.nunique(), op[(op.clinic == c) & (op.age <= 85)].nhs.nunique())
            for c in K.NAMES}


def ask_b_careful(P):
    tr = P["tracker"].copy()
    tr["ref"] = pd.to_datetime(tr["Referral date"]).dt.date
    tr["dxd"] = pd.to_datetime(tr["Diagnosis date"]).dt.date
    a0, a1 = K.ASK_YEAR
    t = tr[tr.dxd.notna()]
    t = t[(t.dxd >= a0) & (t.dxd <= a1)].copy()
    t["days"] = [(d - r).days for d, r in zip(t.dxd, t.ref)]
    return {c: (100.0 * (t[t.Clinic == c].days <= 42).mean(), t[t.Clinic == c].days.mean()) for c in K.NAMES}


def ask_b_feedback_only(P):
    tr = P["tracker"].copy()
    tr["ref"] = pd.to_datetime(tr["Referral date"]).dt.date
    tr["nhs"] = PK.digits(tr["NHS number"])
    ap = P["appts"]
    fb = ap[(ap.appointment_type == "Diagnosis feedback") & ap.outcome.str.contains("diagnosis given")].copy()
    fb["nhs"] = PK.digits(fb.nhs_number)
    fb["date"] = pd.to_datetime(fb.appointment_start.str[:10]).dt.date
    tr["fb"] = tr.nhs.map(fb.groupby("nhs").date.first())
    a0, a1 = K.ASK_YEAR
    u = tr[tr.fb.notna()]
    u = u[(u.fb >= a0) & (u.fb <= a1)].copy()
    u["days"] = [(d - r).days for d, r in zip(u.fb, u.ref)]
    return {c: (round(100.0 * (u[u.Clinic == c].days <= 42).mean(), 1), round(u[u.Clinic == c].days.mean(), 1))
            for c in K.NAMES}


def separation(target, P, fig):
    """The call recomputed from the sittings, diagnoses, index and register alone."""
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    try:
        for k in ("cis_ace", "epr_obs", "cis_dx", "epr_dx", "pmi", "clinics"):
            shutil.copy(os.path.join(target, K.FILES[k]), os.path.join(tmp, K.FILES[k]))
        # stand-ins for the ask files so the loader runs: empty, with headers
        for k in ("episodes", "appts"):
            with open(os.path.join(target, K.FILES[k])) as f:
                head = f.readline()
            open(os.path.join(tmp, K.FILES[k]), "w").write(head)
        shutil.copy(os.path.join(target, K.FILES["tracker"]), os.path.join(tmp, K.FILES["tracker"]))
        Q = PK.load(tmp)
        r = A.main(Q)
        return r["sites"] == fig["call"]["sites"] and r["below"] == fig["call"]["below"] and \
            all(abs(r["decline"][c] - P_decl(P)[c]) < 1e-12 for c in K.NAMES)
    finally:
        shutil.rmtree(tmp)


def P_decl(P):
    return A.main(P)["decline"]


LEAK = ["practice", "retest", "re-test", "learning", "familiar", "gain", "repeat", "second assessment",
        "second sitting", "first sitting", "sat the test", "test effect", "exposure", "alternate version",
        "parallel form", "version a", "version b"]


def documents(target):
    from pypdf import PdfReader
    for k in ("paper", "questionnaire", "guide"):
        txt = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, K.FILES[k])).pages).lower()
        txt = re.sub(r"\s+", " ", txt)
        for wd in LEAK:
            check("DOC %s does not say '%s'" % (k, wd), not re.search(r"\b%s" % re.escape(wd), txt))
        check("DOC %s ranks no clinic on decline (no decline figure)" % k,
              not re.search(r"\d\.\d+ (ace-iii )?points a year", txt))
    txt = open(os.path.join(target, K.FILES["contents"])).read().lower()
    for wd in LEAK:
        check("DOC contents does not say '%s'" % wd, not re.search(r"\b%s" % re.escape(wd), txt))


def containers(task):
    """H1 and H16: no writer's name in any shipped container, and no stamp before the oldest clinic opened or after
    the pack was assembled (the goldens inside October 2026, after the extracts)."""
    import importlib.util
    path = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                        "scrub_producer_metadata.py")
    spec = importlib.util.spec_from_file_location("scrub_producer_metadata", path)
    sm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sm)
    for folder, floor, ceiling in (("target", "2014-04-01", K.ASSEMBLED.date().isoformat()),
                                   ("golden", "2026-10-02", "2026-10-31")):
        d = os.path.join(task, folder)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            r = sm.audit(os.path.join(d, f), floor, ceiling)
            check("CONTAINER %s/%s carries no writer's name and no stamp outside %s to %s" % (folder, f, floor, ceiling),
                  r is None or not (r[0] or r[1]), r)


def realism(target, P, w):
    # no copied block of rows: no run of five identical totals for one patient
    s = P["sittings"]
    runs = 0
    for _, g in s.groupby("nhs"):
        t = g.total.values
        if len(t) >= 5 and any(len(set(t[i:i + 5])) == 1 for i in range(len(t) - 4)):
            runs += 1
    check("R3c no patient's totals repeat five times running (no copied block)", runs == 0, runs)
    # every record dated on or before the extract, the booked appointments aside
    ap = P["appts"]
    late = ap[(ap.appointment_start.str[:10] > K.EXTRACT.isoformat()) & (ap.outcome != "")]
    check("REALISM no appointment after the extract carries an outcome", len(late) == 0, len(late))
    check("REALISM no ACE-III set after the extract", (s.date <= K.EXTRACT).all())
    booked = ap[ap.booked_on > K.EXTRACT.isoformat()]
    check("REALISM no appointment booked after the extract", len(booked) == 0, len(booked))
    # identities
    pmi = P["pmi"]
    check("REALISM NHS numbers are ten digits with a valid check digit",
          pmi.nhs.map(valid_nhs).all(), int((~pmi.nhs.map(valid_nhs)).sum()))
    check("REALISM NHS numbers come from a range the NHS does not issue (first digit 9)", pmi.nhs.str[0].eq("9").all())
    check("REALISM one NHS number per active hospital number", pmi[pmi.record_status == "Active"].nhs.is_unique)
    # containers
    for f in os.listdir(target):
        b = open(os.path.join(target, f), "rb").read()
        check("REALISM no writer's name in %s" % f, b"ReportLab" not in b and b"openpyxl" not in b.lower()
              and b"matplotlib" not in b.lower())
    # H21: invented names away from real places
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()]
    for nm in K.NAMES + ["Hollinsmere", "Arvenna"]:
        n = nm.lower()
        near = [p for p in places if edit(n, p) <= 2 or (len(p) >= 6 and p in n) or (len(n) >= 6 and n in p)]
        check("H21 %s is three or more edits from every reference place" % nm, not near, near[:3])
    # personas
    check("REALISM the personas are the ones drawn", set(K.PEOPLE.values()) == {"Georgina Khan", "Jeremy Hurst",
                                                                                "Nicola Lynch"})


def valid_nhs(n):
    if not re.fullmatch(r"\d{10}", n):
        return False
    s = sum((10 - i) * int(d) for i, d in enumerate(n[:9]))
    c = 11 - (s % 11)
    c = 0 if c == 11 else c
    return c != 10 and c == int(n[9])


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
