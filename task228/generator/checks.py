"""task228 checks: the input gates, the three rules executed on the clean truth, the ladder and its margins, the valid
methods' agreement case by case (delta, log-ratio delta, quasi-Poisson, robust Poisson, install bootstrap; Welch and
pooled t; normal and exact binomial), the reflex routes, the semantic fork rows (SF1 to SF18), Layer 1 neutrality,
the ask on SDK 9.4.1's installs (its truth, the link's forcing, every rival reading, its separation from the main call),
the describing-file screen, the as-of closure and the realism sweep."""
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
    # SF10: service 1's arms. The change log records the rename in order, and the rows leave one reading (C1), both
    # read through the verifier's own readers.
    import verify as V
    chg = " ".join(open(os.path.join(target, "platform_change_log_2026.md"), encoding="utf-8").read().split())
    ok("the arms are called control and treatment (service 1 called them A and B)" in chg,
       "SF10: the change log records service 1's arm names in order")
    vreg = {e["key"]: e for e in V.read_registry(target)["experiments"]}
    q1n = {}
    for r in V.q1_rows(target):
        q1n[(r["exp_id"], r["variant"])] = q1n.get((r["exp_id"], r["variant"]), 0) + 1
    q1k = sorted({k for k, _ in q1n})
    ok(len(q1k) == 30 and set(v for _, v in q1n) == {"A", "B"}, "SF10: service 1 exports 30 runs, arms A and B only")
    for k in q1k:
        ok(q1n[(k, "A")] <= vreg[k]["assigned"]["control"] and q1n[(k, "B")] <= vreg[k]["assigned"]["treatment"],
           "SF10 C1: with A the control, no service 1 arm exports more installs than the registry assigned it (%s)" % k)
    uneven = [k for k in q1k if vreg[k]["design"]["treatment"] != 0.5]
    ok(len(uneven) >= 3, "SF10 C1: %d service 1 runs with an uneven design split" % len(uneven))
    for k in uneven:
        a, b = q1n[(k, "A")], q1n[(k, "B")]
        ok(a > 3 * vreg[k]["assigned"]["treatment"],
           "SF10 C1: read the other way, arm A would export over three times the treatment's assigned installs (%s)" % k)
        ok(abs(b / (a + b) - vreg[k]["design"]["treatment"]) < 0.01,
           "SF10 C1: arm B holds the design's treatment share of the exported installs (%s)" % k)
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
    rx = D["rgx"]
    ok(set(rx.loc[rx["scope"] == "experiment", "incident_type"]) <= set(E.TYPES), "register types in the four words")
    # ---------------------------------------------------------------- the ask on SDK 9.4.1's installs (collector client summary)
    C = E.load_clients(target)
    truth = o["clients_truth"]
    days = E.DAYS941
    gold = {d: {p: 0 for p in E.PLATS} for d in days}
    for t in truth:
        if t["population"]:
            for k, d in enumerate(days):
                if t["first_942"] is None or t["first_942"] > P.CS_ASK_DAYS[k]:
                    gold[d][t["platform"]] += 1
    ok(A["sdk941"] == gold, "ask D: the shipped summary, each re-keyed client ID joined by its sequence, gives the installs' truth")
    popC = E.population(C)
    ok(set(popC) == {t["clients"][0] for t in truth if t["population"]},
       "ask D: the population read from the rows is the truth's (%d installs)" % len(popC))
    lk = E.links(C)
    ok(lk == {t["clients"][0]: t["clients"][1] for t in truth if t["rekeyed"]},
       "ask D: the sequence link joins every re-keyed install and nothing else (%d links)" % len(lk))
    ok(len(set(lk.values())) == len(lk), "ask D: no new client ID continues two older ones")
    rk_pop = {p: sum(1 for c in lk if popC.get(c) == p) for p in E.PLATS}
    ok(all(rk_pop[p] >= 300 for p in E.PLATS), "ask D: re-keyed installs in the population on each platform %s" % rk_pop)
    # the link is forced: a linked client ID continues its predecessor exactly and no other older client ID comes within a
    # million of it; an unlinked new client ID comes within a million of none, so any tolerant join files the same links
    has942 = set(C.loc[C["sdk_version"] == "9.4.2", "client_id"])
    older = C[C["sdk_version"] != "9.4.2"]
    newc = C[(C["sdk_version"] == "9.4.2") & ~C["client_id"].isin(set(older["client_id"]))]
    pred = {v: k for k, v in lk.items()}
    worst_linked, worst_free, exact = None, None, 0
    for p in E.PLATS:
        o_ = older[older["platform"] == p].sort_values("last_seq")
        ends = o_["last_seq"].to_numpy(np.int64) + 1
        who = o_["client_id"].to_numpy()
        n_ = newc[newc["platform"] == p]
        st = n_["first_seq"].to_numpy(np.int64)
        i = np.searchsorted(ends, st)
        for cid, x, j in zip(n_["client_id"], st, i):
            cand = [(abs(int(x - ends[k])), who[k]) for k in range(max(0, j - 2), min(len(ends), j + 2))]
            if cid in pred:
                d0 = [d for d, w in cand if w == pred[cid]]
                rest = [d for d, w in cand if w != pred[cid]]
                exact += 0 in d0
                m = min(rest) if rest else 10 ** 12
                worst_linked = m if worst_linked is None else min(worst_linked, m)
            else:
                m = min(d for d, _ in cand) if cand else 10 ** 12
                worst_free = m if worst_free is None else min(worst_free, m)
    ok(exact == len(lk), "ask D: every linked client ID continues its predecessor's sequence exactly (%d)" % exact)
    ok(worst_linked > 10 ** 6 and worst_free > 10 ** 6,
       "ask D: no second older client ID within a million of a linked one (nearest %d), none within a million of an "
       "unlinked new one (nearest %d)" % (worst_linked, worst_free))
    starts = C["first_seq"].to_numpy(np.int64)
    ok(starts.min() > 10 ** 9, "ask D: sequence numbers start at random values (lowest %d), so a start of one marks nothing" % starts.min())
    last_old = older[older["client_id"].isin(has942)].sort_values(["client_id", "last_batch"]).groupby("client_id").last()
    nxt = C[C["sdk_version"] == "9.4.2"].set_index("client_id")
    cont = nxt.loc[last_old.index, "first_seq"].to_numpy(np.int64) == last_old["last_seq"].to_numpy(np.int64) + 1
    ok(cont.all() and len(cont) > 20000, "ask D: an install updated in place carries its counter on (%d of %d)" % (cont.sum(), len(cont)))
    wait_in = (nxt.loc[last_old.index, "first_batch"].reset_index(drop=True) -
               last_old["last_batch"].reset_index(drop=True)).dt.total_seconds().to_numpy()
    lastb_old = older.groupby("client_id")["last_batch"].max()
    wait_rk = np.array([(nxt.loc[n_, "first_batch"] - lastb_old[o_]).total_seconds() for o_, n_ in lk.items()])
    ok(0.75 < np.median(wait_rk) / np.median(wait_in) < 1.33,
       "ask D: a re-keyed install's wait from its last old batch to its first 9.4.2 batch is an in-place updater's "
       "(median %.0f h against %.0f h)" % (np.median(wait_rk) / 3600, np.median(wait_in) / 3600))
    # rival readings: the careful solver's, the over-cleaners' and the window hazard, each off the golden
    r1 = E.still_on(C, {})
    r3 = E.still_on(C, {}, silent_days=7)
    r4 = E.still_on(C, E.timing_links(C))
    all941 = dict(zip(C.loc[C["sdk_version"] == "9.4.1", "client_id"], C.loc[C["sdk_version"] == "9.4.1", "platform"]))
    r6 = E.still_on(C, lk, pop=all941)
    for name, r, gap, ds in (("R1, a client ID read as an install (the careful solver)", r1, 50, days),
                             ("R3, an install silent for a week read as gone", r3, 3, days),
                             ("R4, a stopped 9.4.1 client joined to the next new 9.4.2 client", r4, 3, days),
                             ("R6, every 9.4.1 client whenever it first sent", r6, 1, days)):
        miss = sum(1 for d in ds for p in E.PLATS if abs(r[d][p] - gold[d][p]) >= gap)
        ok(miss == 2 * len(ds), "ask D: %s misses every figure by %d or more (%d of %d)" % (name, gap, miss, 2 * len(ds)))
    # convergence: tolerant joins (within a million) and UTC days file the golden
    ok(E.still_on(C, E.links(C, tol=0)) == gold, "ask D: the exact join files the golden")
    tod = lambda x: x.dt.hour * 3600 + x.dt.minute * 60 + x.dt.second
    ok(tod(C["first_batch"]).between(2 * 3600 + 600, 23 * 3600 + 3000).all() and tod(C["last_batch"]).between(2 * 3600 + 600, 23 * 3600 + 3000).all(),
       "ask D: every batch falls from 02:10 to 23:50 Copenhagen time, so day ends read inclusively, exclusively or in UTC agree")
    ok((tod(C["first_batch"]) < 6 * 3600).mean() > 0.01, "ask D: readers' batches before six in the morning (%.1f per cent of rows)" % (
        100 * (tod(C["first_batch"]) < 6 * 3600).mean()))
    utc = C.copy()
    for c in ("first_batch", "last_batch"):
        utc[c] = utc[c].dt.tz_convert("UTC").dt.tz_localize(None).dt.tz_localize("Europe/Copenhagen")
    ok(E.still_on(utc, E.links(utc)) == gold and set(E.population(utc)) == set(popC), "ask D: read on UTC days, the same figures")
    # mass: every figure moves by the device, and the over-count grows with the rollout
    ok(all(r1[d][p] - gold[d][p] >= 50 for d in days for p in E.PLATS), "ask D: the careful solver's count is high on every figure")
    # separation: the call reads none of it, and the files the call reads are the shipped pack's, byte for byte
    import hashlib
    shipped = {"dh3_data_health_hold_standard.pdf": "cc9fc970aed6e7ee9d592c54a7580a97fef65d3f894b68179688b0107cfdea54",
               "experiment_registry_2026.json": "a1d31c0a5366a6ef1d74f713378f1f180d67d4a3f7f7e66f9301fd719945c503",
               "install_summary_2026q1.csv": "c39de3da16e07646f40f73b4f6fa65be7e7b0acd20f5b47f05d0e1df6c079f55",
               "install_summary_2026q2.parquet": "10d87e6905fdc33f6379e42592672cc00f411f694ee0e7f0824e93bf37c6cc7d",
               "install_summary_2026q3.parquet": "13f88ab32c2aff5b57bee552c643937196cc67e563f4e738db7e5789100c9bae",
               "data_incident_register_2026.xlsx": "9b92dc8dee27b6586f15e38dac65162ddd761fd44769c44150c5bbc8c13bdd2d",
               "reconciliation_summary_2026.pdf": "04f7a6fae96a20b7fbf38e02a86346b89e5dd8d13cb89611fd1ee4459f6f6739",
               "platform_change_log_2026.md": "659d8c84dcde843505b83fd23322c335377d25c470d407124cb82ef7fe6b0c4d"}
    for f, h in shipped.items():
        ok(hashlib.sha256(open(os.path.join(target, f), "rb").read()).hexdigest() == h,
           "separation: %s is the shipped pack's, byte for byte" % f)
    import inspect
    src = inspect.getsource(E.load) + inspect.getsource(E.labels) + inspect.getsource(E.arm_stats) + inspect.getsource(E.hold_line)
    ok("client" not in src and "registry" in src, "separation: the call's loader and its tests never open the client summary")
    # the record's own world: the releases and the change log tell one SDK story
    rel = pd.read_csv(os.path.join(target, "app_releases_2026.csv"))
    r941 = rel[rel["sdk_version"] == "9.4.1"]
    ok(len(r941) == 2 and set(r941["released"]) == {"2026-07-30"} and set(rel.loc[rel["released"] == "2026-08-06", "sdk_version"]) == {"9.4.2"},
       "ask D: SDK 9.4.1 shipped in 11.2.1 on 30 July and 9.4.2 in 11.3.0 on 6 August, on both platforms")
    ok("SDK 9.4.1 batching regression; fixed in 9.4.2 on 6 August" in chg, "ask D: the change log records the regression and the fix")
    first942 = C.loc[C["sdk_version"] == "9.4.2", "first_batch"].min()
    ok(first942.strftime("%Y-%m-%d") == "2026-08-06", "ask D: no client sends from 9.4.2 before 6 August")
    ok(C.groupby(["client_id", "sdk_version"]).size().max() == 1 and C["client_id"].str.fullmatch(r"[0-9a-f]{16}").all(),
       "ask D: one row a client ID and SDK version, client IDs as the collector writes them")
    # separation from the call, as before
    ok(set(rx.loc[rx["scope"] == "app-wide", "experiment"].dropna()) == set(), "app-wide rows name no experiment")
    rx2 = rx.copy()
    rx2["incident_type"] = "telemetry loss"
    D2 = dict(D, rgx=rx2)
    ok(set(E.labels(D2)) == inc, "separation: the register's types never move the labels")
    # ---------------------------------------------------------------- no shipped file describes the data (section 3)
    describe = re.compile(
        r"(?<![a-z])(read_?me|data_?dictionar\w*|dictionar(y|ies)|codebook|field_?notes|field_?guide|fields?_(guide|notes|"
        r"list|descriptions?)|\w*_fields|manifest|extract_contents|file_list|file_layout|glossary|column_(notes|descriptions?)|"
        r"data_?notes|how_to_read|about_this|export_notes|extract_notes|definitions|schema|layouts?_notes|release_notes)(?![a-z])",
        re.I)
    ok(all(describe.search(os.path.splitext(x)[0]) for x in ("data_dictionary.md", "export_manifest.csv", "README.txt")),
       "describing-file screen: positive control, the retired names are caught")
    for f in files:
        ok(not describe.search(os.path.splitext(f)[0]), "no shipped file describes the data by name (%s)" % f)
    from openpyxl import load_workbook
    sheet_bad = re.compile(r"^(read ?me|notes?|dictionary|data dictionary|definitions|glossary|fields|field notes|about|"
                           r"how to (read|use)( this)?|columns?)$", re.I)
    ok(sheet_bad.match("Notes") and sheet_bad.match("Data dictionary"), "describing-sheet screen: positive control")
    for f in files:
        if f.endswith(".xlsx"):
            names = load_workbook(os.path.join(target, f), read_only=True).sheetnames
            ok(names and not any(sheet_bad.match(x.strip()) for x in names), "no describing sheet in %s (%s)" % (f, names))
    cols = set()
    for f in files:
        fp = os.path.join(target, f)
        if f.endswith(".csv"):
            cols |= set(open(fp, encoding="utf-8").readline().strip().split(","))
        elif f.endswith(".parquet"):
            import pyarrow.parquet as pq
            cols |= set(pq.read_schema(fp).names)
        elif f.endswith(".xlsx"):
            ws = load_workbook(fp, read_only=True).worksheets[0]
            cols |= {str(c) for c in next(ws.iter_rows(min_row=1, max_row=1, values_only=True)) if c}
        elif f.endswith(".json"):
            cols |= set(V.read_registry(target)["experiments"][0].keys())
    ident = sorted(c for c in cols if "_" in c or re.search(r"\d", c))
    ok(len(ident) >= 20, "describing-content screen: %d identifier column names in the data files" % len(ident))

    def named(text):
        return [c for c in ident if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(c), text)]
    ok(len(named(" ".join(ident))) == len(ident), "describing-content screen: positive control through the same search")
    for f in files:
        if f.endswith((".md", ".pdf")):
            txt = pdf_text(os.path.join(target, f)) if f.endswith(".pdf") else open(os.path.join(target, f), encoding="utf-8").read()
            ok(len(txt) > 400, "document read back (%s, %d characters)" % (f, len(txt)))
            ok(len(named(txt)) < 4, "no document names the data's columns (%s: %s)" % (f, named(txt)))
    # ---------------------------------------------------------------- closure 4: one pull, nothing after it
    pulled = V.read_registry(target)["pulled"]
    ok(pulled.startswith("2026-10-12") and "12 October.** Registry, install exports, incident register and review log pulled" in chg,
       "closure 4: the registry's pull stamp and the change log's 12 October entry agree")
    ok(max(e["end"][:10] for e in V.read_registry(target)["experiments"]) < "2026-10-12", "closure 4: every run ended before the pull")
    ok(max(D["rev"]["logged_at_utc"]) < "2026-10-12" and str(max(D["rgx"]["status_date"])) < "2026-10-12",
       "closure 4: no review or register entry after the pull")
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
