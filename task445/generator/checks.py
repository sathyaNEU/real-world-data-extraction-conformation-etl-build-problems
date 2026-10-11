"""Assertions over the built pack: the ladder by name, convergence of the rigorous variants, truth,
the back-test, mess neutrality on the main call, the ask devices and their stops, the bridge, the
separation counts, bins and the input gates. Every check counts; the run fails on the first miss."""
import datetime as dt
import json
import os
import re

import numpy as np
import pandas as pd

import golden as G
import world as W

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def flagset(d, cus, ids):
    return {ids[c] for c in cus if d[c] > 80.0}


def run(wd, g, target, golden_dir, meta):
    cus = g["cusips"]
    ids = {c: f"W{k + 1:02d}" for k, c in enumerate(cus)}
    ans = flagset(g["dec_io"], cus, ids)
    ok(ans == {"W01", "W02", "W03", "W06", "W10"}, f"answer {ans}")
    rungs = {k: flagset(g[k], cus, ids) for k in ("R0", "R1", "R2", "R3", "R3w", "R4dev")}
    expect = {"R0": {"W01", "W06"}, "R1": {"W01", "W02", "W06", "W07", "W10"},
              "R2": {"W01", "W02", "W03", "W04", "W05", "W06", "W07", "W09", "W10"},
              "R3": {"W01", "W04", "W05", "W06", "W07", "W10"}}
    for k, v in expect.items():
        ok(rungs[k] == v, f"rung {k} {rungs[k]}")
    ok(rungs["R3w"] == rungs["R3"], f"value-completion variants differ {rungs['R3w']}")
    ok(rungs["R4dev"] - ans and not (ans - rungs["R4dev"]) or rungs["R4dev"] != ans, "dev rung equals answer")
    seq = [rungs["R0"], rungs["R1"], rungs["R2"], rungs["R3"], rungs["R4dev"], ans]
    for a in range(len(seq)):
        for b in range(a + 1, len(seq)):
            ok(seq[a] != seq[b], f"rungs {a} and {b} name the same set")
    # margins on the answer
    for c in cus:
        ok(abs(g["dec_io"][c] - 80.0) >= 1.5, f"{ids[c]} answer within 1.5 of the line: {g['dec_io'][c]:.2f}")
    # every wrong rung misses on at least one issuer by 1.5 points of clearance from the line
    for k in ("R0", "R1", "R3"):
        wrong = [c for c in cus if (g[k][c] > 80) != (g["dec_io"][c] > 80)]
        ok(any(abs(g[k][c] - 80) >= 1.5 for c in wrong), f"rung {k} only flips at the line")

    # ---- the matched-panel variant of holder-level completion converges on the flags
    f, inf = G.load(target)
    wl = G.watch_table(target)
    inf["cusip9"] = G.normalise_cusips(inf, wl)
    h3 = G.holdings(f, inf, wl, G.PERIOD["Q3"], cusips=cus)
    h4 = G.holdings(f, inf, wl, G.PERIOD["Q4"], cut=G.EXTRACT, cusips=cus)
    both = set(h4.CIK) & set(h3.CIK)
    for c in cus:
        a4 = h4[(h4.cusip9 == c) & h4.CIK.isin(both)].SSHPRNAMT.sum()
        a3 = h3[(h3.cusip9 == c) & h3.CIK.isin(both)].SSHPRNAMT.sum()
        ratio = a4 / a3
        alt = 100 * (g["dec_onfile_shares"][c] + ratio * g["dec_carried_shares"][c]) / g["S_dec"][c]
        ok((alt > 80) == g["flag"][c], f"matched-panel variant flips {ids[c]}: {alt:.2f}")
        # carry-forward that drops the attrition register's inactive managers
    reg = pd.read_csv(os.path.join(target, "manager_register.csv"), dtype=str)
    inactive = set(reg[reg.status == "inactive"].cik.astype(int))
    for c in cus:
        alt = 100 * (g["dec_onfile_shares"][c] + h3[(h3.cusip9 == c) & h3.CIK.isin(set(g["pending_ciks"]) - inactive)].SSHPRNAMT.sum()) / g["S_dec"][c]
        ok((alt > 80) == g["flag"][c], f"inactive-excluded variant flips {ids[c]}")

    # ---- truth: the completed December set (simulation) gives the same flags, close figures
    tru = {}
    for i in wd.iss:
        if not i["watch"]:
            continue
        tot = sum(v for (mid, iid), v in wd.pos["Q4"].items() if iid == i["iid"])
        tru[i["cusip"]] = 100 * tot / i["S_oct"]
    for c in cus:
        ok((tru[c] > 80) == g["flag"][c], f"truth flag differs on {ids[c]}")
        ok(abs(tru[c] - g["dec_io"][c]) < 1.0, f"truth far from golden on {ids[c]}: {tru[c]:.2f}")

    # ---- back-test in the September window: holder-level completion beats every rival per issuer
    bt = g["backtest"]
    for c in cus:
        ok(abs(bt[c]["cf_err_pp"]) < 3.0, f"cf back-test error {ids[c]}")
        ok(abs(bt[c]["cf_err_pp"]) < abs(bt[c]["uni_err_pp"]), f"uniform beats cf in back-test {ids[c]}")
        ok(abs(bt[c]["cf_err_pp"]) < abs(bt[c]["dev_err_pp"]), f"dev beats cf in back-test {ids[c]}")
    ok(np.mean([abs(bt[c]["cf_err_pp"]) for c in cus]) < 1.0, "cf mean back-test error")
    ok(max(abs(bt[c]["uni_err_pp"]) for c in cus) > 10, "uniform back-test never misses badly")

    # ---- main-call mess neutrality (texture on the main path cannot move a flag)
    e4 = G.effective_lines(f, inf, G.PERIOD["Q4"], G.EXTRACT)
    e4 = e4.merge(f[["ACCESSION_NUMBER", "CIK"]], on="ACCESSION_NUMBER")
    opt = e4[(e4.PUTCALL != "") & e4.CUSIP.isin(cus)].groupby("CUSIP").SSHPRNAMT.sum()
    for c in cus:
        alt = 100 * (g["dec_shares"][c] + opt.get(c, 0)) / g["S_dec"][c]
        ok((alt > 80) == g["flag"][c], f"option lines flip {ids[c]}")
        alt = 100 * g["dec_shares"][c] / g["S_jan_latest"][c]
        ok((alt > 80) == g["flag"][c], f"latest share count flips {ids[c]}")
    # separation: the main call's declared rows carry no device rows
    main4 = e4[e4.CUSIP.str.upper().str.zfill(9).isin(cus) | e4.cusip9.isin(cus)]
    main4 = main4[main4.PUTCALL == ""]
    ok((main4.CUSIP != main4.cusip9).sum() == 0, "repaired CUSIPs inside the December rows")
    q4f = f[(f.period == G.PERIOD["Q4"]) & (f.fdate <= G.EXTRACT)]
    ok((q4f[q4f.ACCESSION_NUMBER.isin(set(main4.ACCESSION_NUMBER))].ISAMENDMENT == "Y").sum() == 0,
       "amendments inside the December rows")
    pend = set(g["pending_ciks"])
    p3f = f[(f.period == G.PERIOD["Q3"]) & f.CIK.isin(pend)]
    ok((p3f.ISAMENDMENT == "Y").sum() == 0, "amendments among pending managers' September reports")
    ok((p3f.fdate >= dt.date(2023, 1, 1)).sum() == 0, "pending managers filed September late")
    pl = inf[inf.ACCESSION_NUMBER.isin(set(p3f.ACCESSION_NUMBER)) & inf.cusip9.isin(cus)]
    ok((pl.CUSIP != pl.cusip9).sum() == 0 and (pl.PUTCALL != "").sum() == 0, "device rows in pending managers' September lines")
    roles = wd.roles
    for key in ("TK", "SP", "GA1", "GA2", "NH", "RS"):
        ok(wd.M[roles[key]]["cik"] not in pend, f"device manager {key} is pending")
    for mid in roles["LATE3"]:
        ok(wd.M[mid]["cik"] not in pend, "late September filer is pending")
    ok(len(g["thousands_after_switch"]) == 1, "one filing on the thousands basis after the switch")

    # ---- the September ask: every wrong stop moves several issuers by more than a rounding step
    for k in ("own_drop", "latest_wins", "sum_all", "exact_join", "later_count"):
        moved = [c for c in cus if abs(g["sep_wrong"][c][k] - g["sep_io"][c]) >= 0.15]
        ok(len(moved) >= (6 if k == "later_count" else 3), f"September stop {k} moves {len(moved)}")
    ok(abs(g["sep_wrong"][cus[7]]["later_count"] - g["sep_io"][cus[7]]) > 2.0, "W08 count device")
    # ---- the top-holder ask
    tk, sp = wd.M[roles["TK"]]["cik"], wd.M[roles["SP"]]["cik"]
    for k in (1, 7, 10):
        c = cus[k]
        ok(g["top"][c]["cik"] == tk, f"TK not top on {ids[c]}")
        ok(g["top_wrong"][c]["as_reported"] != tk, f"as-reported lands on TK {ids[c]}")
    for k in (3, 8):
        c = cus[k]
        ok(g["top"][c]["cik"] == sp, f"SP not top on {ids[c]}")
        ok(g["top_wrong"][c]["largest_line"] != sp, f"largest line lands on SP {ids[c]}")
    for k in (4, 11):
        c = cus[k]
        ok(not g["top_wrong"][c]["family"].isdigit(), f"family consolidation does not change top on {ids[c]}")
    for c in cus:
        ok(g["top"][c]["usd"] >= 1.08 * g["top"][c]["runner_usd"], f"top holder margin {ids[c]}")
        carried_max = g["pending_max_shares"][c] * wd.I[[i["iid"] for i in wd.iss if i["cusip"] == c][0]]["P4"]
        ok(carried_max < 0.8 * g["top"][c]["usd"], f"a pending manager could be top on {ids[c]}")
    # ---- the bridge
    b = g["bridge"]
    ok(b["conformed"] == b["conformed_check"], "bridge does not tie")
    ok(b["principal"] == 0, "principal lines on watchlist CUSIPs")
    for k in ("options", "superseded", "cusip_repaired"):
        ok(b[k] > 0.004 * b["raw"], f"bridge item {k} too small to read")
    # ---- bins: one-decimal figures away from the half step
    for c in cus:
        for v in (g["sep_io"][c], g["dec_io"][c]):
            frac = (v * 10) % 1
            ok(abs(frac - 0.5) > 0.02, f"{ids[c]} figure {v:.4f} on a rounding edge")
    # ---- input gates
    files = [os.path.join(dp, fn) for dp, _, fns in os.walk(target) for fn in fns]
    ok(len(files) >= 10, "file count")
    fmts = {os.path.splitext(p)[1] for p in files}
    ok(len(fmts) >= 3, f"formats {fmts}")
    biggest = max(sum(1 for _ in open(p, encoding="utf-8")) - 1 for p in files if p.endswith(".tsv"))
    ok(biggest >= 25_000, f"largest file rows {biggest}")
    ok(len(meta["distractor_files"]) >= 2, "distractors")
    src = open(os.path.join(os.path.dirname(__file__), "golden.py"), encoding="utf-8").read()
    for dfile in meta["distractor_files"]:
        ok(os.path.exists(os.path.join(target, dfile)), f"distractor missing {dfile}")
        ok(os.path.basename(dfile) not in src, f"golden reads distractor {dfile}")
    # ---- leak words in the pack's own documents
    for p in files:
        if p.endswith((".md", ".htm", ".txt", ".csv")) and "fsds" not in p:
            t = open(p, encoding="utf-8").read().lower()
            for wrd in ("distractor", "pending", "carry forward", "carried forward", "late filer", "censor",
                        "not yet filed", "complete filing set"):
                ok(wrd not in t, f"'{wrd}' in {p}")
    # ---- H9: the data-sources note registers every shipped file or folder; H11: one prompt, one submission
    src_note = open(os.path.join(target, "data_sources.md"), encoding="utf-8").read()
    for p in files:
        rel = os.path.relpath(p, target)
        top = rel.split(os.sep)[0]
        if rel != "data_sources.md":
            ok(("`" + top + ("/`" if os.sep in rel else "`")) in src_note, f"data_sources.md does not register {rel}")
    task = os.path.dirname(target)
    for nm in ("prompt.md", "submission.md"):
        hits = [os.path.join(dp, f) for dp, _, fns in os.walk(task) for f in fns if f == nm]
        ok(len(hits) <= 1, f"more than one {nm}")
    # ---- golden files exist
    for fn in ("crowded_flags_2022q4.csv", "sep_quarter_bridge.png"):
        ok(os.path.exists(os.path.join(golden_dir, fn)), fn)
    return N[0]
