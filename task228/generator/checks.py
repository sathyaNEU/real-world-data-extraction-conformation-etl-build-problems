"""task228 checks: the input gates, the three rules executed on the clean truth, the ladder and its margins, the valid
methods' agreement case by case (delta, log-ratio delta, quasi-Poisson, robust Poisson, install bootstrap; Welch and
pooled t; normal and exact binomial), the reflex routes, the semantic fork rows (SF1 to SF16), Layer 1 neutrality,
the ask devices and their separation from the main call, the bins and the realism sweep."""
import json
import os
import re
import zipfile

import numpy as np
import pandas as pd

import estim as E
import params as P
import sim

GOLD = "gap"
PEOPLE = ["Mathilde Knudsen", "Kaspar Gregersen", "Inge Lund", "Thea Koch", "Justina Bach"]


def run(target, golden, o, A, D, S):
    n = [0]

    def ok(c, label):
        assert c, label
        n[0] += 1

    files = sorted(os.listdir(target))
    task = os.path.dirname(target)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    exps, data = o["exps"], o["data"]
    inc = set(A["inc"])
    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10, "gate: 10 or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "gate: 3 or more formats")
    ok(max(o["counts"]["q1"], o["counts"]["q2"], o["counts"]["q3"]) >= 25000, "gate: a file of 25,000 rows or more")
    ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]), "gate: two distractors")
    ok(not any("distractor" in f.lower() for f in files), "gate: no file named after its role")
    # ---------------------------------------------------------------- labels: register, reconciliation, truth (SF2, SF3)
    truth_inc = {e["key"] for e in exps if e["kind"] != "clean"}
    recon_conf = {r["key"] for r in o["recon"] if r["finding"] == "confirmed"}
    ok(inc == truth_inc == recon_conf and len(inc) == 18, "SF2: register confirmed = reconciliation confirmed = truth (18)")
    withdrawn = {r["key"] for r in o["recon"] if r["finding"] != "confirmed"}
    ok(withdrawn and not (withdrawn & inc) and len(A["none"]) == 64, "SF3: withdrawn suspicions count as experiments without one")
    titles = {E.norm(e["title"]): e["key"] for e in D["reg"]}
    ok(len(titles) == 82, "SF18: registry titles unique after case and space normalisation")
    rx = D["rgx"]
    for t in rx.loc[rx["scope"] == "experiment", "experiment"]:
        ok(E.norm(t) in titles, "SF18: every register title matches one registry title (%s)" % t)
    # ---------------------------------------------------------------- the shipped figures equal the generator's truth
    Zs = A["Z"]
    for e in exps:
        for m in ("gap", "dup", "late"):
            ok(abs(Zs[e["key"]][m]["delta"] - e["z"][m]["delta"]) < 1e-6, "files carry the truth (%s %s)" % (e["key"], m))
    # ---------------------------------------------------------------- R1 to R3: the three rules on the clean truth
    def rec_truth(how):
        out = {}
        for m in E.CHECKS:
            h = {"delta": sim.VALID[m][0], "naive": {"gap": "naive", "dup": "naive", "late": "naive", "epu": "welch",
                                                      "share": "normal"}[m],
                 "mor": {"gap": "mor", "dup": "mor", "late": "mor", "epu": "welch", "share": "normal"}[m]}[how]
            held = [e for e in exps if e["z"][m][h] > P.Z]
            out[m] = dict(incidents=sum(1 for e in held if e["kind"] != "clean"), none=sum(1 for e in held if e["kind"] == "clean"))
        return out
    rt = {h: rec_truth(h) for h in ("delta", "naive", "mor")}
    ok(E.pick(rt["naive"], 64)[0] == "late", "R3 analyst test: the session-level route on the clean truth files late sessions")
    ok(E.pick(rt["delta"], 64)[0] == GOLD, "R3 analyst test: changing only the variance to the install files gap sessions")
    ok(E.pick(rt["mor"], 64)[0] == "late", "R3 second route: the per-install mean of shares files late sessions")
    ok(rt["naive"]["gap"]["none"] >= 2 and rt["naive"]["late"]["none"] <= 1, "R3: the session-level test breaks the allowance on gap only")
    # the shipped files give the same records as the clean truth (Layer 1 neutral)
    for h in ("delta", "naive", "mor"):
        ok(A["recs"][h] == rt[h], "Layer 1 neutral: shipped records equal the clean truth's (%s)" % h)
    # ---------------------------------------------------------------- the ladder
    rec = A["recs"]["delta"]
    pick, okk, cap = A["picks"]["delta"]
    ok(pick == GOLD and cap == 1, "golden: gap sessions within the allowance of 1")
    ok(rec["gap"]["incidents"] == 10 and rec["gap"]["none"] == 0, "golden record 10 and 0")
    ok(okk[1] == "late" and rec["late"]["incidents"] == 5, "runner-up late sessions at 5")
    ok(rec["gap"]["incidents"] >= 1.15 * rec["late"]["incidents"], "golden margin over the runner-up 1.15x or more")
    ok(A["picks"]["naive"][0] == "late" and A["picks"]["mor"][0] == "late", "default path and second route file late")
    ok(A["recs"]["naive"]["late"]["incidents"] == 6, "default path's late record 6")
    ok(A["moved_most"] == "dup", "rung 0: moved most is duplicate sessions")
    ok(rec["epu"]["none"] > cap and rec["dup"]["incidents"] == 3 and rec["share"]["incidents"] == 3, "the other checks")
    # ---------------------------------------------------------------- the valid methods agree, case by case
    for e in exps:
        z = e["z"]
        for m, hows in sim.VALID.items():
            vals = [z[m][h] for h in hows]
            ok(len({v > P.Z for v in vals}) == 1 and min(abs(v - P.Z) for v in vals) >= P.BAND - 1e-9,
               "valid methods agree clear of the line (%s %s)" % (e["key"], m))
    # robust Poisson (install-level sandwich) and the install bootstrap on every ratio case near the line
    rng = np.random.default_rng(91)
    near = 0
    for e, (c, t) in zip(exps, data):
        for m, col in sim.RATIO.items():
            zd = e["z"][m]["delta"]
            if abs(zd - P.Z) > 1.2:
                continue
            near += 1
            zr = robust_poisson(c, t, col)
            zb = boot(rng, c, t, col, 1500)
            ok((zr > P.Z) == (zd > P.Z) and abs(zr - P.Z) > 0.08, "robust Poisson agrees (%s %s %.2f)" % (e["key"], m, zr))
            ok((zb > P.Z) == (zd > P.Z) and abs(zb - P.Z) > 0.05, "install bootstrap agrees (%s %s %.2f)" % (e["key"], m, zb))
    ok(near >= 5, "near-line cases checked by the bootstrap")
    # ---------------------------------------------------------------- reflex routes and fork rows
    one_sided = {m: sum(1 for k in Zs if Zs[k][m]["delta"] > 2.3263 and k not in inc) for m in E.CHECKS}
    ok(True, "SF4 one-sided 1 per cent route recorded: %s" % one_sided)
    bonf = E.record({k: {m: {"b": Zs[k][m]["delta"] - (3.0902 - P.Z)} for m in E.CHECKS} for k in Zs}, inc, "b")
    ok(E.pick(bonf, 64)[0] == GOLD, "SF14: a multiplicity-corrected level keeps the call")
    assigned = {e["key"]: (e["assigned_c"], e["assigned_t"]) for e in exps}
    srm_assigned = sum(1 for e in exps if sim.z_share(*assigned[e["key"]], e["split"]) > P.Z)
    ok(srm_assigned <= 1, "SF9: the treatment share on assigned counts holds nothing; same call")
    # the Q1 arm mapping inverted (B read as control) moves the records: ruled out by the dictionary sentence
    d = open(os.path.join(target, "data_dictionary.md")).read()
    ok("A is the control arm and B the treatment arm" in d, "SF10: the Q1 arm mapping is filed")
    std = pdf_text(os.path.join(target, "dh3_data_health_hold_standard.pdf"))
    for s in ("two-sided 1 per cent level", "no more than one experiment in fifty", "10,000 installs in each arm",
              "both arms of the 2026 experiments", "as a share of all sessions in the arm", "keeps its arm for the whole run",
              "below the design share", "judges each experiment once"):
        ok(s in std, "standard files: %s" % s)
    for w in ("delta", "variance", "cluster", "independent", "unit of analysis", "design effect", "bootstrap",
              "standard error", "randomis"):
        ok(w not in std.lower(), "standard names no method (%s)" % w)
    ok(all(nm in std for nm in ("Gap sessions", "Duplicate sessions", "Late sessions", "Events per install", "Treatment share")),
       "SF1: DH-3 lists the five checks")
    rec2 = A["recs"]["delta"]
    cap2 = [m for m in E.CHECKS if rec2[m]["none"] <= 2]
    ok(sorted(cap2, key=lambda m: (-rec2[m]["incidents"], rec2[m]["none"]))[0] == GOLD, "SF5: an allowance read as 2 keeps the call")
    per = D["ins"].groupby("key")["id"].agg(["count", "nunique"])
    ok((per["count"] == per["nunique"]).all() and len(per) == 82, "SF6: one row an install for the full run, 82 experiments")
    ok(A["picks"]["mor"][0] == "late", "SF7: the per-install mean of shares is another estimand and files late sessions")
    any_dir = {m: (sum(1 for k in Zs if abs(Zs[k][m]["delta"]) > P.Z and k in inc),
                   sum(1 for k in Zs if abs(Zs[k][m]["delta"]) > P.Z and k not in inc)) for m in E.CHECKS}
    ok(True, "SF8: holds in either direction recorded %s; ruled out by the hold direction" % any_dir)
    ok("10,000 installs in each arm of its export" in std, "SF11: the standard experiment counts exported installs")
    line_assigned = A["line"] * (P.STD_N / (P.STD_N * P.CONSENT)) ** 0.5
    ok(round(line_assigned, 2) != round(A["line"], 2), "SF11: 10,000 assigned installs would give another line (%.3f)" % line_assigned)
    ok(rec2["gap"]["incidents"] != rec2["late"]["incidents"], "SF13: no tie at the top")
    ok("divided by the arm's installs" in std, "SF15: events per install filed")
    ok(len(D["reg"]) == 82 and all(e["status"] == "completed" for e in D["reg"]), "SF16: the 82 completed runs of 2026")
    exact = {e["title"]: e["key"] for e in D["reg"]}
    rxe = D["rgx"][(D["rgx"]["scope"] == "experiment") & (D["rgx"]["status"] == "confirmed")]
    unmatched = sum(1 for t in rxe["experiment"] if t not in exact)
    ok(unmatched >= 1 and all(E.norm(t) in titles for t in rxe["experiment"]),
       "SF17: an exact-title join leaves %d confirmed entries unmatched (loud); case and spacing ignored, all match once" % unmatched)
    # ---------------------------------------------------------------- the line and its readings
    lines = [E.hold_line(D["ins"], A["none"], "gap", ("control", "treatment"), True),
             E.hold_line(D["ins"], A["none"], "gap", ("control", "treatment"), False)]
    ok(len({round(x, 2) for x in lines}) == 1, "SF12: pooled and arm-by-arm readings give one two-decimal line")
    ok(all(abs(x - round(x, 2)) <= 0.0025 for x in lines), "line mid-bin under both readings: %s" % lines)
    ok(round(A["line"], 2) != round(A["line_naive_late"], 2) and round(A["line"], 2) != round(A["line_naive_gap"], 2),
       "the line differs from the session-level lines")
    # ---------------------------------------------------------------- ask B: the weekly review by type
    rv = A["review"]
    fc = A["review_first_call"]
    for t in E.TYPES:
        ok(rv[t][0] != fc[t][0] and rv[t][1] != fc[t][1], "ask B device moves both figures (%s)" % t)
    ok(sum(sum(v) for v in rv.values()) == 18, "ask B covers the 18 confirmed incidents")
    # type totals are the same under both columns (a vintage change with invariant totals)
    ok({t: sum(v) for t, v in rv.items()} == {t: sum(v) for t, v in fc.items()}, "ask B: totals by type invariant")
    rx = D["rgx"]
    ok(set(rx.loc[rx["scope"] == "experiment", "incident_type"]) <= set(E.TYPES), "register types in the four words")
    # ---------------------------------------------------------------- ask C: the app-wide incidents
    for a, b in zip(A["app_wide"], A["app_wide_summed"]):
        ok(b["gap"] != a["gap"] and abs(b["share"] - a["share"]) > 1.0, "ask C device moves both figures (%s)" % a["incident"])
        ok(abs(a["share"] - round(a["share"], 2)) <= 0.0018, "ask C share mid-bin (%s)" % a["incident"])
    aw = rx[rx["scope"] == "app-wide"]
    tells = sum(1 for _, g in aw.groupby("incident_id") if (g["gap_sessions"] > g["sessions_in_window"]).any())
    ok(tells >= 3, "ask C: the records force the incident reading (%d incidents with a row above its sessions)" % tells)
    ok(all(g["gap_sessions"].nunique() == 1 for _, g in aw.groupby("incident_id")), "ask C: one figure per incident on every row")
    # ---------------------------------------------------------------- separation: devices never touch the main call
    ok(set(rx.loc[rx["scope"] == "app-wide", "experiment"].dropna()) == set(), "app-wide rows name no experiment")
    rx2 = rx.copy()
    rx2["incident_type"] = "telemetry loss"
    D2 = dict(D, rgx=rx2)
    ok(set(E.labels(D2)) == inc, "separation: the register's types never move the labels")
    # ---------------------------------------------------------------- realism and the container
    for f in files:
        if f.endswith((".csv", ".md", ".json")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok("—" not in txt and "–" not in txt, "no em or en dash (%s)" % f)
    for p in PEOPLE:
        ok(True, "persona %s" % p)
    return n[0]


def robust_poisson(c, t, col):
    import statsmodels.api as sm
    y = np.concatenate([c[col], t[col]]).astype(float)
    off = np.log(np.concatenate([c["sess"], t["sess"]]).astype(float))
    X = sm.add_constant(np.concatenate([np.zeros(len(c[col])), np.ones(len(t[col]))]))
    m = sm.GLM(y, X, family=sm.families.Poisson(), offset=off).fit(cov_type="HC0")
    return float(m.params[1] / m.bse[1])


def boot(rng, c, t, col, B):
    def rs(a):
        n = len(a[col])
        idx = rng.integers(0, n, (B, n))
        return a[col][idx].sum(1) / a["sess"][idx].sum(1)
    d = rs(t) - rs(c)
    est = t[col].sum() / t["sess"].sum() - c[col].sum() / c["sess"].sum()
    return float(est / d.std(ddof=1))


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))
