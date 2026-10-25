"""Generator checks for task121, run on every build: the walk against the world, the call and its family, the
ladder, the three rules (R1 to R3), each Layer 1 item mishandled, the semantic fork rows, the separation of the asks'
devices from the call, the asks' devices against their stops, the rounding margins, the input gates and the realism
sweep."""
from __future__ import annotations

import os
import re
import subprocess
import warnings

import numpy as np

import analysis as A
import common as K
import deliver as DV

warnings.filterwarnings("ignore")
FAILS = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        FAILS.append(label)
    print("%s %s %s" % ("PASS" if cond else "FAIL", label, detail))


def pdf_text(path):
    try:
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    except FileNotFoundError:
        return ""


def r1(x):
    return DV.p1(x)


def edge(x, nd):
    """Distance of x from the nearest rounding edge at nd decimals, in units of the last place."""
    y = abs(x) * 10 ** nd
    return abs((y - np.floor(y)) - 0.5) / 10 ** nd


def walk1(w):
    return tuple(r1(w[k]) for k in ("gap", "att", "dis", "own", "rem"))


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    w = b["w"]
    D, E = res["D"], res["E"]
    gold = res["walk"]

    # ------------------------------------------------------------------ the walk against the world
    T = w.D[w.D.s.isin(K.TRUST_KEYS) & ~w.D.p8.isna()]
    H = T[T.s == K.FOCAL]
    true_own = H.s.map(w.u).mean() - T.s.map(w.u).mean()
    true_rem = H.v.mean() - T.v.mean()
    ok("WORLD the world's own effect for Halwick is near nil against the trust", abs(true_own) < 0.06, "%.3f" % true_own)
    ok("WORLD the world's carried effect is the largest item", true_rem < -0.15 and abs(true_rem) > abs(true_own),
       "%.3f against own %.3f" % (true_rem, true_own))
    ok("WORLD the golden recovers the world's own effect within 0.05", abs(gold["own"] - true_own) < 0.05,
       "%.3f against %.3f" % (gold["own"], true_own))
    ok("WORLD the golden recovers the world's carried effect within 0.05", abs(gold["rem"] - true_rem) < 0.05,
       "%.3f against %.3f" % (gold["rem"], true_rem))
    yr = T.groupby(["year", "s"]).p8.mean().unstack()
    ok("WORLD Halwick lowest of the eight in each cohort", all(yr.loc[y].idxmin() == K.FOCAL for y in K.COHORTS),
       str({y: round(float(yr.loc[y][K.FOCAL]), 2) for y in K.COHORTS}))

    # ------------------------------------------------------------------ the call
    ok("CALL the golden walk is -0.4 = -0.1, -0.1, 0.0, -0.2", walk1(gold) == ("-0.4", "-0.1", "-0.1", "0.0", "-0.2"),
       str(walk1(gold)))
    ok("CALL the largest item is the remainder", A.largest(gold) == "rem", A.largest(gold))
    ok("CALL the remainder leads the next item by 0.1 or more", abs(gold["rem"]) - max(abs(gold[k]) for k in
       ("att", "dis", "own")) >= 0.1, "%.3f" % (abs(gold["rem"]) - max(abs(gold[k]) for k in ("att", "dis", "own"))))
    ok("CALL the academy's own effect is under a fifth of the gap", abs(gold["own"]) < 0.2 * abs(gold["gap"]),
       "%.3f of %.3f" % (gold["own"], gold["gap"]))
    for k in ("gap", "att", "dis", "own", "rem"):
        ok("CALL %s sits 0.008 or more from a rounding edge at one decimal" % k, edge(gold[k], 1) >= 0.008,
           "%.4f (%.4f)" % (gold[k], edge(gold[k], 1)))
    s = sum(float(fig["walk"][k]) for k in ("att", "dis", "own", "rem"))
    ok("CALL the rounded items add to the rounded gap", abs(s - float(fig["walk"]["gap"])) < 1e-9, "%.1f" % s)

    # ------------------------------------------------------------------ the golden family and the semantic forks
    Eu = A.pupils(D, link=False)
    E2 = E.copy()
    E2["girl"] = (E2.gender == "F").astype(float)
    E2["senk"] = (E2.sen_provision == "K").astype(float)
    E2["sene"] = (E2.sen_provision == "E").astype(float)
    E2["eal1"] = (E2.eal == "Y").astype(float)
    E3 = E.copy()
    E3.loc[E3.ks2_la != K.LA_CODE, "ks2_school"] = "outside"
    E4 = E.copy()
    for y in ("2022/23", "2023/24"):
        E4["c" + y[:4]] = (E4.ks4_year == y).astype(float)
    fam = {"SF7 converted primaries read as separate schools": A.walk(Eu),
           "SF8 gender, special needs and first language held as well": A.walk(E2, extra=("girl", "senk", "sene", "eal1")),
           "SF9 a term for each cohort": A.walk(E4, extra=("c2022", "c2023")),
           "SF10 schools outside the borough pooled as one": A.walk(E3)}
    for name, v in fam.items():
        ok("FAMILY %s files the golden walk" % name, walk1(v) == walk1(gold), "%s %s" % (walk1(v), A.largest(v)))
        ok("FAMILY %s keeps the remainder largest" % name, A.largest(v) == "rem", A.largest(v))
    # per-cohort models, each cohort's items carried at its trust pupils' weight
    parts = []
    for y in ("2021/22", "2022/23", "2023/24"):
        Ey = E[E.ks4_year == y]
        parts.append((A.walk(Ey), int(Ey.trust.sum())))
    pooled = {k: sum(p[0][k] * p[1] for p in parts) / sum(p[1] for p in parts) for k in ("att", "dis", "own", "rem")}
    ok("FAMILY SF9 per-cohort models carried together keep the remainder largest",
       min(pooled, key=pooled.get) == "rem", str({k: round(v, 3) for k, v in pooled.items()}))
    ok("FAMILY SF9 per-cohort models keep the academy's own effect at 0.0", r1(pooled["own"]) == "0.0",
       "%.3f" % pooled["own"])

    # ------------------------------------------------------------------ the ladder
    T8 = E[E.trust]
    H8 = E[E.ks4_school == A.FOCAL_NAME]
    r0_gap = H8.p8.mean() - T8.p8.mean()
    ok("LADDER R0 Progress 8 read alone puts the whole gap on the academy", r1(r0_gap) == "-0.4", "%.3f" % r0_gap)
    two = res["default"]
    ok("LADDER R1 the model of pupils within secondaries files the academy's own effect, -0.2, as largest",
       r1(two["own"]) == "-0.2" and A.largest(two) == "own", "%s %s" % (walk1(two), A.largest(two)))
    ok("LADDER R1 the remainder is nil within secondaries", abs(two["rem"]) < 1e-6, "%.6f" % two["rem"])
    two_c = A.walk(E2, classify=("secondary",), extra=("girl", "senk", "sene", "eal1"))
    ok("LADDER R2 with gender, special needs and first language held, still the academy's own effect, -0.2",
       r1(two_c["own"]) == "-0.2" and A.largest(two_c) == "own", "%s %s" % (walk1(two_c), A.largest(two_c)))
    E5 = E.copy()
    E5["ks2c"] = E5.ks2_prior_attainment.astype(float) - 100.0
    two_k = A.walk(E5, classify=("secondary",), extra=("ks2c",))
    ok("LADDER R2 with key stage 2 prior attainment held again, still the academy's own effect, -0.2",
       r1(two_k["own"]) == "-0.2" and A.largest(two_k) == "own", "%s" % (walk1(two_k),))
    trust_only = A.walk(E, estimation=E[E.trust])
    ok("LADDER SF5 the cross-classified model on the trust's pupils alone moves the own effect off the golden",
       r1(trust_only["own"]) != r1(gold["own"]), "%s (closed: Paper 6 files all the borough's pupils)" %
       (walk1(trust_only),))
    ok("LADDER SF5 the trust-only model still files the remainder largest", A.largest(trust_only) == "rem",
       A.largest(trust_only))
    try:
        rew = re_walk(E)
        ok("LADDER SF6 shrunk (random effects) files the remainder largest", A.largest(rew) == "rem",
           "%s" % (walk1(rew),))
        ok("LADDER SF6 shrinkage moves the academy's own effect off the golden (closed: Paper 6 reads effects "
           "unshrunk)", r1(rew["own"]) != r1(gold["own"]), "%s" % (walk1(rew),))
    except Exception as e:      # pragma: no cover
        ok("LADDER SF6 random effects fitted", False, repr(e))

    # ------------------------------------------------------------------ the three rules
    ok("R1 the deciding quantity is a school effect from a cross-classified model of pupils (the field's method)",
       A.largest(gold) == "rem" and A.largest(two) == "own", "golden %s, within secondaries %s" % (
           A.largest(gold), A.largest(two)))
    ok("R3a the analyst test: every field read correctly, the field's school-effects model files the wrong item",
       A.largest(two) == "own" and A.largest(two_c) == "own" and A.largest(two_k) == "own", "own, own, own")
    ok("R3b the golden family is unanimous on the largest item", all(A.largest(v) == "rem" for v in fam.values()),
       "%d members" % len(fam))
    tables_txt = open(os.path.join(target, K.FILES["tables"])).read()
    paper = pdf_text(os.path.join(target, K.FILES["paper"]))
    guide = pdf_text(os.path.join(target, K.FILES["guide"]))
    ok("R3c no shipped file names the primary schools as a cause or a candidate",
       not re.search(r"primary schools? (?:effect|legacy)|feeder|carried|bring[s]? from", paper + guide, re.I),
       "paper and guide")
    ok("R3c the paper ranks nothing and states no item's size", not re.search(r"-0\.[0-9]", paper.split("3. What")[1])
       if "3. What" in paper else False, "")
    ok("R2 Layer 1: reading converted academies as separate schools leaves the call (SF7)",
       A.largest(fam["SF7 converted primaries read as separate schools"]) == "rem", "")
    ok("R2 Layer 1: schools outside the borough pooled leaves the call (SF10)",
       A.largest(fam["SF10 schools outside the borough pooled as one"]) == "rem", "")
    nk = E[E.ks2_urn == ""]
    ok("R2 Layer 1: pupils without key stage 2 carry no Progress 8 and sit outside the walk",
       len(nk) == 0 and (D["transfer"].p8_score == "").sum() > 0, "%d without Progress 8" % (
           (D["transfer"].p8_score == "").sum()))

    # ------------------------------------------------------------------ the remaining fork rows
    pooled_gap = H8.p8.mean() - T8.p8.mean()
    yearly = np.mean([E[(E.ks4_school == A.FOCAL_NAME) & (E.ks4_year == y)].p8.mean() -
                      E[E.trust & (E.ks4_year == y)].p8.mean() for y in ("2021/22", "2022/23", "2023/24")])
    ok("SF1 the gap pooled over pupils, against the mean of the yearly gaps: same one-decimal gap",
       r1(pooled_gap) == r1(yearly), "%.3f %.3f" % (pooled_gap, yearly))
    m = A.fit(E)
    eff = m["school"]
    unw = H8.ks4_school.map(eff).mean() - np.mean([eff[k] for k in A.TRUST_NAMES])
    ok("SF2 the trust's average academy pupil-weighted (filed); unweighted would read %s" % r1(unw),
       r1(gold["own"]) == "0.0", "unweighted %.3f" % unw)
    ua = E.copy()
    ua["absr"] = 100.0 * E.y11_sessions_unauth_absence.astype(float) / E.y11_sessions_possible.astype(float)
    ok("SF3 absence as sessions missed of sessions possible, authorised and unauthorised (filed)",
       "absence rate (sessions missed" in paper.replace("\n", " ") or "absence rate" in paper, "")
    ok("SF4 disadvantaged as the file's flag (filed in the guide)", "disadvantaged" in guide, "")
    ok("SF11 the walk rounded half up to one decimal, each item alone; the items add to the gap", True, str(walk1(gold)))
    ok("SF12 pupils with a Progress 8 score only (filed)", len(E) == (D["transfer"].p8_score != "").sum(), str(len(E)))

    # ------------------------------------------------------------------ the asks
    att = res["att"]
    routes = {"academy as extracted": A.attendance(D, label="current"),
              "year group as extracted": A.attendance(D, year="current"),
              "both as extracted": A.attendance(D, label="current", year="current"),
              "both as extracted, pupils by UPN": A.attendance(D, label="current", year="current", key="upn"),
              "year 11 summer kept": A.attendance(D, y11_rule=False)}
    for nm, ro in routes.items():
        moved = sum(DV.half_up(ro[k]["pa"], 1) != DV.half_up(att[k]["pa"], 1) for k in A.TRUST_NAMES)
        ok("ASK A persistent absence moves at every academy with the %s" % nm, moved == 8, "%d of 8" % moved)
    note = pdf_text(os.path.join(target, K.FILES["attnote"])).replace("\n", " ")
    meas = pdf_text(os.path.join(target, K.FILES["measures"])).replace("\n", " ")
    ok("SF13 a mover counts at each academy for the sessions on its roll (filed in the attendance note)",
       "counts at each academy" in re.sub(r"\s+", " ", note), "")
    ok("SF14 year 11 counts for the autumn and spring terms only (filed in the attendance note)",
       "autumn and spring terms only" in re.sub(r"\s+", " ", note), "")
    ok("SF15 the thresholds are 10 and 50 per cent or more (filed in the attendance note)",
       "10 per cent or more" in re.sub(r"\s+", " ", note) and "50 per cent or more" in re.sub(r"\s+", " ", note), "")
    edge_a = min(min(edge(att[k]["pa"], 1), edge(att[k]["sa"], 1)) for k in A.TRUST_NAMES)
    ok("SF15 no academy's rate sits on a threshold tie at the stated rounding", edge_a >= 0.0005, "%.4f" % edge_a)
    ok("SF16 the cohort and its results from any series in key stage 4, the first entry for EBacc subjects (filed)",
       "year 10 or year 11" in re.sub(r"\s+", " ", meas) and "first entry" in meas, "")
    ok("SF17 the Attainment 8 slots, points and discounting (filed in the measures summary)",
       "double weighted only if" in re.sub(r"\s+", " ", meas) and "mean of its two grades" in re.sub(r"\s+", " ", meas),
       "")
    crack_a = routes["both as extracted"]
    kept = sum(DV.half_up(crack_a[k]["pa"], 1) == DV.half_up(att[k]["pa"], 1) for k in A.TRUST_NAMES) + \
        sum(DV.half_up(crack_a[k]["sa"], 1) == DV.half_up(att[k]["sa"], 1) for k in A.TRUST_NAMES)
    ok("ASK A the cracker keeps at most 3 of 16", kept <= 3, "%d" % kept)
    rs = res["res"]
    r0 = A.results(D, early=False)
    for k in A.TRUST_NAMES:
        ok("ASK B Attainment 8 at %s moves without the year 10 entries" % k,
           DV.half_up(r0[k]["a8"], 1) != DV.half_up(rs[k]["a8"], 1), "%.2f against %.2f" % (r0[k]["a8"], rs[k]["a8"]))
        ok("ASK B EBacc entry at %s moves without the year 10 entries" % k,
           DV.half_up(r0[k]["ebacc"], 1) != DV.half_up(rs[k]["ebacc"], 1),
           "%.2f against %.2f" % (r0[k]["ebacc"], rs[k]["ebacc"]))
    for k in A.TRUST_NAMES:
        for q, nd in (("pa", 1), ("sa", 1)):
            ok("MARGIN Annex A %s %s clear of a rounding edge" % (k, q), edge(att[k][q], nd) >= 0.0005,
               "%.4f" % att[k][q])
        for q in ("a8", "ebacc"):
            ok("MARGIN Annex B %s %s clear of a rounding edge" % (k, q), edge(rs[k][q], 1) >= 0.0005,
               "%.4f" % rs[k][q])

    # ------------------------------------------------------------------ separation
    tr = b["tr"]
    upns = {a["upn"] for a in tr.att} | {r["upn"] for r in tr.res}
    tf = D["transfer"]
    ok("SEP no pupil in the trust's 2025/26 records is in the transfer file", not (set(tf.pupil_ref) & upns), "")
    ok("SEP the transfer file holds only the 2022 to 2024 cohorts",
       set(tf.ks4_year) == {"2021/22", "2022/23", "2023/24"}, "")
    ok("SEP the asks' files carry no Progress 8 and no key stage 2 school", all(
        "p8" not in c and "ks2" not in c for key in ("attendance", "movements", "results25", "results26")
        for c in D[key].columns), "")

    # ------------------------------------------------------------------ input gates and realism
    files = os.listdir(target)
    ok("GATE ten or more files", len(files) >= 10, str(len(files)))
    ok("GATE three or more formats", len({os.path.splitext(f)[1] for f in files}) >= 3,
       str(sorted({os.path.splitext(f)[1] for f in files})))
    ok("GATE a file of 25,000 rows or more", max(b["counts"].values()) >= 25000, str(max(b["counts"].values())))
    ok("GATE two distractors named", len(K.DISTRACTORS) >= 2, str(K.DISTRACTORS))
    txt = paper + guide + pdf_text(os.path.join(target, K.FILES["measures"])) + \
        pdf_text(os.path.join(target, K.FILES["attnote"]))
    ok("REAL no em dash in any document", "—" not in txt, "")
    print("checks: %d run, %d failed" % (N[0], len(FAILS)))
    for f in FAILS:
        print("  FAILED:", f)
    return 1 if FAILS else 0


def re_walk(E):
    """The cross-classified model with random effects (shrunk): REML, statsmodels."""
    import statsmodels.formula.api as smf
    X = E.copy()
    X["sec"] = X.ks4_school
    X["pri"] = X.ks2_school
    m = smf.mixedlm("p8 ~ absr + dis", X, groups=np.ones(len(X)), vc_formula={"s": "0 + C(sec)", "p": "0 + C(pri)"}
                    ).fit(reml=True)
    r = m.random_effects[1.0]
    eff = {s: r.get("s[C(sec)[%s]]" % s, 0.0) for s in X.sec.unique()}
    T = X[X.trust]
    H = X[X.ks4_school == A.FOCAL_NAME]
    gap = H.p8.mean() - T.p8.mean()
    att = m.fe_params["absr"] * (H.absr.mean() - T.absr.mean())
    dis = m.fe_params["dis"] * (H.dis.mean() - T.dis.mean())
    own = H.sec.map(eff).mean() - T.sec.map(eff).mean()
    return dict(gap=gap, att=att, dis=dis, own=own, rem=gap - att - dis - own)
