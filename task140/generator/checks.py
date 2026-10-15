"""Assertions on the built pack and the goldens: the call and every rung reproduce from the shipped files, every
semantic-fork row (SF1 to SF38) is closed as the design note says, the asks' devices and stops land where the ask
sheet says, the context artifact recomputes, the input gates and the realism sweep hold. Run by build.py."""
from __future__ import annotations

import collections
import datetime as dt
import json
import math
import os
import random
import re
import shutil
import subprocess
import tempfile

import numpy as np
import openpyxl

import calc as C
import common as K
import docs as DOC

N = [0]


def ok(cond, msg):
    if not cond:
        raise AssertionError("CHECK FAILED: " + msg)
    N[0] += 1


def edge_near(x, step):
    """Distance to the nearer edge of the bin x rounds into (nearest-step rounding)."""
    q = x / step
    return (0.5 - abs(q - math.floor(q + 0.5))) * step


def edge_floor(x, step):
    f = x / step - math.floor(x / step)
    return min(f, 1 - f) * step


def run(target, golden, W=None, meta_path=None):
    M = C.load(target)
    lad = C.ladder(M)
    g = lad["R3"]
    G = g["G"]

    # ------------------------------------------------------------------ the call and its figures
    ok(G == 109000, "golden guarantee %d" % G)
    ok(M.M1 == 5220 and M.R1 == 726624 and abs(M.overcommit - 1.45) < 1e-9, "reservable inputs")
    ok(len(M.requests) == 11 and sorted(M.requests) == sorted(M.firm), "SF6 one request per firm tenant")
    ap = C.firm_approvals(M)
    held = sorted(t for t in M.firm if ap[t] < M.requests[t])
    ok(held == sorted(K.CAPPED), "three firm tenants held to their budgets: %s" % held)
    ok(g["F"] == 576972, "firm total %d" % g["F"])
    ok(abs(g["c"] - K.STORE_PER_MACHINE) < 0.01 and abs(g["beta"] - K.STORE_PER_BATCH) < 0.002,
       "the fit recovers the storage drivers: %.4f, %.4f" % (g["c"], g["beta"]))
    ok(55.0 < g["resid_sd"] < 70.0 and g["n"] > 16000, "fit residual sd %.2f on %d hours" % (g["resid_sd"], g["n"]))
    # graded figures inside their bins with margin
    ok(250 <= g["Gu"] - G <= 750, "guarantee mid-thousand: %.1f" % g["Gu"])
    for lab, v in (("cell-store", g["S"]), ("cell-ctl", g["ctl"]), ("firm", g["F"]), ("platform", g["platform"])):
        ok(edge_near(v, 1000) >= 300, "%s %.1f at least 300 cores from a rounding edge" % (lab, v))
    ok(edge_near(C.golden(M, G_in_store="unrounded")["S"], 1000) >= 300, "SF17 cell-store with the unrounded solve")
    ok(K.round_to(C.golden(M, G_in_store="unrounded")["S"], 1000) == K.round_to(g["S"], 1000), "SF17 same storage")
    for t, v in ap.items():
        ok(edge_near(v, 1000) >= 50, "approval of %s %d clear of a rounding edge" % (t, v))
    ok(0 < g["unreserved"] < 1000 * (1 + g["beta"]), "unreserved %.1f below one more thousand and its storage" %
       g["unreserved"])

    # ------------------------------------------------------------------ the three rules, executed (R1, R2, R3)
    _three_rules(target, M, g, lad, W)

    # ------------------------------------------------------------------ the ladder
    R0 = lad["R0"]
    ok(R0["G"] == 122000, "default path ends on 122,000: %d" % R0["G"])
    expect = {"R-1": 118000, "R0": 122000, "R0b": 122000, "R0c": 122000, "R0d": 122000, "R0e": 122000,
              "R1": 119000, "R1b": 118000, "R1c": 118000, "R2": 111000, "R2b": 106000, "R2c": 110000,
              "R2d": 110000, "R2e": 120000, "Monly": 120000, "O1": 101000, "LedgerFit": 110000, "QmaxFit": 109000,
              "R3": 109000}
    for k, v in expect.items():
        ok(lad[k]["G"] == v, "rung %s files %d (got %d)" % (k, v, lad[k]["G"]))
    for k in expect:
        if k not in ("R3", "QmaxFit"):
            ok(lad[k]["G"] != G, "route %s off the golden's thousand" % k)
            ok(abs(lad[k]["Gu"] - g["Gu"]) >= 600, "route %s at least 600 cores from the golden before the thousand" % k)
    ok(R0["G"] / G - 1 >= 0.10 and lad["R0b"]["G"] / G - 1 >= 0.10, "R0 and R0b at least 10 per cent over")
    ok(lad["R1"]["G"] / G - 1 >= 0.07, "R1 at least 7 per cent over")
    ok(lad["R2b"]["G"] < G < lad["R2"]["G"], "the golden bracketed by the one-pass and batch-only routes")
    ok(abs(lad["QmaxFit"]["Gu"] - g["Gu"]) < 200, "the busiest-hours fit converges on the hourly fit")
    # the grid: storage route x firm reading x rate card
    cells = {}
    for sroute in ("R0", "R1", "R2b", "R3"):
        for hold in (True, False):
            for rate in (M.rate_q1, C.rate_on(M.rates, dt.date(2026, 12, 1))):
                F = sum(C.firm_approvals(M, rate=rate, hold=hold).values())
                if sroute == "R3":
                    Gx = C.golden(M, F=F)["G"]
                else:
                    S = {"R0": lad["R0"]["S"], "R1": lad["R1"]["S"], "R2b": lad["R2b"]["S"]}[sroute]
                    Gx = C.guarantee_given_store(M, S, F=F)["G"]
                cells[(sroute, hold, rate)] = Gx
    gold_cells = [k for k, v in cells.items() if v == G]
    ok(gold_cells == [("R3", True, M.rate_q1)], "the golden cell alone files the golden: %s" % gold_cells)

    # ------------------------------------------------------------------ the semantic fork table, row by row
    ok(C.golden(M, R=M.M1 * K.CORES)["G"] < 0, "SF1 physical cores leave no guarantee (moves the call)")
    ok(K.round_to(g["Gu"], 1000) == G, "SF2 nearest thousand gives the same call (%.1f)" % g["Gu"])
    ok(min(M.t).date() == dt.date(2025, 1, 1) and len(M.machines_q) == 9, "SF3 calendar quarters on file")
    m_now = sum(n for _, d, n in M.racks if d is not None and C._d(d) < dt.date(2026, 12, 14))
    ok(m_now == 4640, "SF4 machines in service on the pull date %d" % m_now)
    ok(C.golden(M, R=int(round(m_now * K.CORES * M.overcommit)), machines=m_now)["G"] < 60000,
       "SF4 the pull date's machines move the call far")
    out26 = float(np.mean([(M.inst[M.q == q] - M.mach[M.q == q]).mean() for q in M.quarters[4:]]))
    ok(C.golden(M, machines=M.M1 - out26)["G"] == G, "SF4 a repair allowance (%.1f machines) gives the same call" % out26)
    ok(M.overcommit == 1.45, "SF5 the memo's overcommit")
    ok(C.golden(M, F=sum(C.firm_approvals(M, budget_month="avg2026").values()))["G"] != G,
       "SF7 the 2026 average month moves the call")
    q4b = all(M.budget_all[t]["Oct 2026"] == M.budget_all[t]["Nov 2026"] == M.budget_all[t]["Dec 2026"]
              == M.budget_all[t]["Jan 2027"] for t in M.firm)
    ok(q4b, "SF7 Q4 months equal under the freeze, so Q4 over three converges")
    r_sep = C.rate_on(M.rates, dt.date(2026, 12, 1))
    ok(abs(r_sep - 7.70) < 1e-9 and C.golden(M, F=sum(C.firm_approvals(M, rate=r_sep).values()))["G"] != G,
       "SF8 the rate in force at the review moves the call")
    for t in M.firm:
        x = M.budget[t]["Jan 2027"] / M.rate_q1
        ok(abs(x - round(x)) > 0.02 or x > M.requests[t] + 1, "SF9 %s budget over rate not on a whole core" % t)
    ok(sum(C.firm_approvals(M, rounding="nearest").values()) - g["F"] <= 3 and
       C.golden(M, F=sum(C.firm_approvals(M, rounding="nearest").values()))["G"] == G, "SF9 nearest core converges")
    ok(sorted(M.platform) == ["cell-ctl", "cell-store"], "SF10 the platform services")
    ok(set(M.use) == set(M.firm) | set(M.platform) | {"batch-train"}, "SF11 one series per tenant")
    last4 = [float(np.percentile(M.ctl[M.q == q], 99)) for q in M.quarters[-4:]]
    ok(K.round_to(C.line_forecast(last4), 1000) == K.round_to(g["ctl"], 1000), "SF12 99th percentile, same cell-ctl")
    ok(C.floor1000(g["Gu"] + (g["ctl"] - C.line_forecast(last4)) / (1 + g["beta"])) == G, "SF12 same call")
    for k in ("R0", "R0b", "R1", "R2", "R2b"):
        ok(lad[k]["G"] != G, "SF13 the %s forecast files another guarantee" % k)
    fills = [float(M.batch[M.q == q].max()) / M.ledger[(q, "batch-train")] for q in M.quarters]
    ok(min(fills) >= 0.998, "SF13/SF14 batch reached 99.8 per cent of its guarantee in every quarter: %.4f" % min(fills))
    af = float(np.mean([M.batch[M.q == q].mean() / M.ledger[(q, "batch-train")] for q in M.quarters]))
    Gaf = (M.R1 - g["F"] - g["ctl"] - g["a"] - g["c"] * M.M1) / (1 + g["beta"] * af)
    ok(C.floor1000(Gaf) == G, "SF14 the average fill (%.4f) converges" % af)
    ok(C.golden(M, allowance=g["resid_max"])["G"] == G and 80 < g["resid_max"] < 120,
       "SF15 the largest residual (%.1f) carried converges" % g["resid_max"])
    for how in ("last", "mean4", "machines"):
        gg = C.golden(M, ctl_how=how)
        ok(gg["G"] == G and K.round_to(gg["ctl"], 1000) == K.round_to(g["ctl"], 1000), "SF16 cell-ctl %s" % how)
    ok(C.floor1000(M.R1 - g["F"] - g["ctl"] - (g["a"] + g["c"] * M.M1 + g["beta"] * G)) == G,
       "SF17 the thousand first, then storage: same guarantee")
    ok(g["unreserved"] > 0, "SF18 the remainder unreserved")
    codes = [M.cc[t].split()[0] for t in M.firm]
    ok(len(set(codes)) == len(codes), "SF19 one cost centre per firm tenant")
    c22 = [x for x in M.budget_lines if x["Budget line"] == "MAD1 C-22 reserved cores"]
    ok(len(c22) == 11, "SF19 eleven C-22 budget lines")

    # ------------------------------------------------------------------ closure: windows, duplicates, gap, order
    for qs in (M.quarters[-4:], M.quarters[4:], M.quarters[2:]):
        ok(C.golden(M, mask=np.isin(M.q, qs))["G"] == G, "closure 8 fit window %s.. same call" % qs[0])
    M2 = C.load(target, dedupe=False)
    g2 = C.golden(M2)
    ok(g2["G"] == G and abs(g2["c"] - g["c"]) < 1e-3 and abs(g2["beta"] - g["beta"]) < 1e-4,
       "closure 7/15 the re-sent day kept moves nothing")
    n_dup = _count_dup_rows(os.path.join(target, K.USAGE))
    ok(n_dup == 24 * 14, "closure 15 the re-sent day: %d duplicate rows" % n_dup)
    M3 = C.load(target, gap="interpolate")
    ok(C.golden(M3)["G"] == G and len(M3.hours) == len(M.hours) + 7, "closure 12 the gap interpolated: same call")
    ok(C.golden(M, use_installed=True)["G"] == G, "closure 19 machines installed instead of in service: same call")
    idx = list(range(len(M.hours)))
    random.Random(140).shuffle(idx)
    X = np.column_stack([np.ones(len(idx)), M.mach[idx], M.batch[idx]])
    co, *_ = np.linalg.lstsq(X, M.store[idx], rcond=None)
    ok(abs(co[1] - g["c"]) < 1e-9 and abs(co[2] - g["beta"]) < 1e-9, "closure 14 row order")
    gap_rows = [h for h in M.hours if h.startswith("2026-08-19T0") and "01" <= h[11:13] <= "07"]
    ok(not gap_rows, "the collector gap has no rows")

    # ------------------------------------------------------------------ the context artifact recomputes
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, K.CAPREPORT), "-"], capture_output=True,
                         text=True).stdout
    txt = re.sub(r"\s+", " ", txt)
    q = "2026Q3"
    rep = {"reservable": M.ledger and int(round(M.machines_q[q] * K.CORES * M.overcommit)),
           "firm": sum(M.ledger[(q, t)] for t in M.firm), "ctl": M.ledger[(q, "cell-ctl")],
           "store": M.ledger[(q, "cell-store")], "G": M.ledger[(q, "batch-train")]}
    rep["unres"] = rep["reservable"] - rep["firm"] - rep["ctl"] - rep["store"] - rep["G"]
    for k, v in rep.items():
        ok("{:,}".format(v) in txt, "capacity report states %s %s" % (k, v))
    mq = M.q == q
    for name, ser in (("cell-ctl", M.ctl), ("cell-store", M.store), ("batch-train", M.batch)):
        v = float(ser[mq].max())
        ok("{:,.1f}".format(v) in txt, "capacity report busiest hour of %s %.1f" % (name, v))
    firm_h = sum(np.array([M.use[t][h] for h in M.hours]) for t in M.firm)
    ok("{:,.1f}".format(round(float(firm_h[mq].max()), 1)) in txt, "capacity report firm busiest hour")
    n99 = int(sum(1 for v in M.batch[mq] if v >= 0.99 * rep["G"]))
    ok(("in %s of the quarter" % "{:,}".format(n99)) in txt, "capacity report hours at 99 per cent: %d" % n99)
    ok("2027" not in txt.replace("2026", ""), "the capacity report states no 2027 figure")

    # ------------------------------------------------------------------ Ask A
    A = C.load_asks(target)
    red, share, heldh = C.ask_a(A)
    runs = {r["run_id"]: r for r in A.runs}
    succ = {r["resumed_from"]: r for r in A.runs if r["resumed_from"]}
    pre = [r for r in A.runs if r["end_state"] == "PREEMPTED" and C.Q3S <= C.tparse(r["ended_utc"]) < C.Q3E]
    ok(all(r["run_id"] in succ for r in pre), "every 2026 Q3 preemption resumed in the file")
    ok(all(C.tparse(succ[r["run_id"]]["started_utc"]) < C.Q3E for r in pre), "no resumption after 30 September")
    late = 0
    earlier = 0
    for r in pre:
        c = A.ckpt[succ[r["run_id"]]["restore_checkpoint"]]
        ok(C.tparse(c["write_started_utc"]) <= C.tparse(r["ended_utc"]), "restore point before its preemption")
        ok(c["committed_utc"] != "", "a restore point is a committed checkpoint")
        if c["run_id"] == r["run_id"]:
            ok(C.tparse(c["write_started_utc"]) >= C.Q3S, "no redone training before 1 July")
        else:
            ok(C.tparse(r["started_utc"]) >= C.Q3S, "no redone training before 1 July (whole run)")
        own = [x for x in A.ckpt_by_run.get(r["run_id"], []) if x["committed_utc"] and
               C.tparse(x["committed_utc"]) <= C.tparse(r["ended_utc"])]
        newest = max(own, key=lambda x: x["write_started_utc"]) if own else None
        if newest is None or newest["checkpoint_id"] != c["checkpoint_id"]:
            earlier += 1
    ok(len(pre) > 150 and 0.2 < earlier / len(pre) < 0.45, "restores earlier than the newest committed: %d of %d" % (
        earlier, len(pre)))
    ok(len(A.resizes) > 400, "elastic resizes on file")
    ok(sum(1 for c in A.ckpt.values() if not c["committed_utc"]) > 300, "HA2 writes that never committed")
    stops = {m: C.ask_a(A, m) for m in ("s1", "s2", "s2b", "s3")}
    for m, (r2, s2, _) in stops.items():
        miss_c = sum(K.round_to(r2[t], 100) != K.round_to(red[t], 100) for t in A.teams)
        miss_s = sum(_pct2(s2[t]) != _pct2(share[t]) for t in A.teams)
        ok(miss_c == 6 and miss_s == 6, "Ask A stop %s misses all 12 (%d, %d)" % (m, miss_c, miss_s))
    for t in A.teams:
        ok(edge_near(red[t], 100) >= 15, "Ask A %s redone %.1f clear of the edge" % (t, red[t]))
        ok(edge_near(share[t], 0.01) >= 0.0015, "Ask A %s share %.4f clear of the edge" % (t, share[t]))

    # ------------------------------------------------------------------ Ask B
    lost = C.ask_b(A)
    s1 = C.ask_b(A, "s1")
    s2 = C.ask_b(A, "s2")
    nd = C.ask_b(A, dedupe=False)
    ok(all(K.round_to(s1[k], 10) != K.round_to(lost[k], 10) for k in lost), "Ask B natural read misses all 6")
    miss_s2 = sum(K.round_to(s2[k], 10) != K.round_to(lost[k], 10) for k in lost)
    ok(miss_s2 >= 3, "Ask B rack pairing misses %d of 6" % miss_s2)
    ok(sum(K.round_to(nd[k], 10) != K.round_to(lost[k], 10) for k in lost) >= 1, "HB1 the re-sent removals move August")
    ev = A.mev
    keys = collections.Counter(tuple(r.values()) for r in ev)
    ok(sum(v - 1 for v in keys.values()) == (W.mev_resent if W is not None else sum(v - 1 for v in keys.values())),
       "HB1 re-sent removals are byte-identical rows")
    rem = [r for r in ev if r["event"] == "REMOVED"]
    by_asset = collections.defaultdict(list)
    for r in ev:
        by_asset[A.asset_of[int(r["machine_id"])]].append(r)
    for r in rem:
        nxt = [x for x in by_asset[A.asset_of[int(r["machine_id"])]] if x["event"] == "REGISTERED" and
               x["time_utc"] > r["time_utc"]]
        if nxt:
            ok(nxt[0]["time_utc"][:7] == r["time_utc"][:7], "SF24 no outage crosses a month boundary")
    n_new = sum(1 for r in rem if any(x["event"] == "REGISTERED" and x["time_utc"] > r["time_utc"] and
                                      x["machine_id"] != r["machine_id"]
                                      for x in by_asset[A.asset_of[int(r["machine_id"])]][:]))
    ok(n_new > 60, "re-imaged returns under a new id: %d" % n_new)
    retired_q3 = [t for t, s in A.status.items() if s == "retired"]
    ok(len(retired_q3) > 20, "retired assets in the inventory")
    for k in lost:
        ok(edge_near(lost[k], 10) >= 1.5, "Ask B %s %.1f clear of the edge" % (k, lost[k]))

    # ------------------------------------------------------------------ Ask C
    owe = C.ask_c(A)
    c1 = C.ask_c(A, "s1")
    c2 = C.ask_c(A, "s2")
    ok(all(K.round_to(c1[t], 100) != K.round_to(owe[t], 100) for t in A.firm), "Ask C request-time read misses all 11")
    ok(sum(K.round_to(c2[t], 100) != K.round_to(owe[t], 100) for t in A.firm) == 11, "Ask C opening rate misses all")
    for r in A.qruns:
        ok(r["run_started_utc"][11:16] != "00:00", "SF25 no change applied at 00:00")
        ok(r["run_started_utc"][:10] == r["run_finished_utc"][:10], "no reconciliation run spans midnight")
    ids = [x for r in A.qruns for x in filter(None, r["changes_applied"].split(";"))]
    ok(sorted(ids) == sorted(c["change_id"] for c in A.changes), "every change applied exactly once")
    gap = [r for r in A.qruns if "2026-08-19T06" <= r["run_started_utc"] < "2026-08-22T12"]
    ok(not gap, "HC3 no reconciliation run during the stop")
    for t in A.firm:
        ok(edge_near(owe[t], 100) >= 15, "Ask C %s %.2f clear of the edge" % (t, owe[t]))
    ok(abs(C.rate_on(A.rates, dt.date(2026, 9, 1)) - 7.70) < 1e-9, "SF26 the September rate")

    # ------------------------------------------------------------------ separation: the main call reads no ask row
    with tempfile.TemporaryDirectory() as tmp:
        for f in os.listdir(target):
            if f not in (K.RUNS, K.CHECKPOINTS, K.RESIZES, K.MEVENTS, K.INVENTORY, K.QCHANGES, K.QRUNS, K.CHARGEBACK,
                         K.SISTERS, K.BATCH_DEMAND, K.CAPREPORT, K.OPSLOG):
                shutil.copy(os.path.join(target, f), tmp)
        Mx = C.load(tmp)
        ok(C.golden(Mx)["G"] == G and C.ladder(Mx)["R0"]["G"] == R0["G"],
           "the call with every ask file, both distractors, the report and the log deleted")
    with tempfile.TemporaryDirectory() as tmp:
        for f in os.listdir(target):
            if f not in K.DISTRACTORS:
                shutil.copy(os.path.join(target, f), tmp)
        Ax = C.load_asks(tmp)
        ok(C.ask_a(Ax)[0] == red and C.ask_b(Ax) == lost and C.ask_c(Ax) == owe, "the asks with the distractors deleted")

    # ------------------------------------------------------------------ the goldens agree with calc
    wb = openpyxl.load_workbook(os.path.join(golden, K.GOLD_BOOK), data_only=True)
    vals = {r[0]: r for r in wb["2027 Q1"].iter_rows(values_only=True) if r and isinstance(r[0], str)}
    ok(vals["Batch training guarantee"][2] == G, "workbook guarantee")
    ok(vals["Firm tenants (eleven)"][2] == K.round_to(g["F"], 1000), "workbook firm")
    ok(vals["cell-store"][2] == K.round_to(g["S"], 1000) and vals["cell-ctl"][2] == K.round_to(g["ctl"], 1000),
       "workbook platform services")
    fp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    figs = json.load(open(fp))
    ok(figs["call"]["guarantee_cores"] == "{:,}".format(G) and figs["default_path"]["guarantee_cores"] ==
       "{:,}".format(R0["G"]), "figures.json carries the call and the default path")

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(files) >= 10 and len(fmts) >= 3, "input gates: %d files, %d formats" % (len(files), len(fmts)))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "a file of 25,000 rows or more (%d)" % big)
    ok(not any("distractor" in f.lower() for f in files), "no file named for its role")
    if meta_path and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        ok(sorted(meta["distractor_files"]) == sorted(K.DISTRACTORS) and all(d in files for d in K.DISTRACTORS),
           "distractors declared in metadata.json")
    for q in M.quarters:
        v = [M.ledger[(q, t)] for t in M.firm]
        ok(len(set(v)) == len(v), "no two firm reservations equal in %s" % q)
    for t in M.firm:
        v = collections.Counter(M.ledger[(q, t)] for q in M.quarters)
        ok(max(v.values()) <= 2, "no firm reservation repeated across three quarters (%s)" % t)
    for name in M.use:
        arr = np.array(list(M.use[name].values()))
        ok(arr.std() > 1.0, "no constant stream (%s)" % name)
    ok(len({r["run_id"] for r in A.runs}) == len(A.runs), "run ids unique")
    ok(len({c["change_id"] for c in A.changes}) == len(A.changes), "change ids unique")
    ok(all(C.tparse(r["ended_utc"]) > C.tparse(r["started_utc"]) for r in A.runs if r["ended_utc"]), "runs end after start")
    ok(all(c["committed_utc"] > c["write_started_utc"] for c in A.ckpt.values() if c["committed_utc"]),
       "checkpoints commit after the write starts")
    pull = "2026-12-14T06:10:00Z"
    ok(max(M.hours) < pull and max(r["time_utc"] for r in ev) < pull, "nothing recorded after the pull")
    # the people are the drawn personas
    ok(len(set(K.PEOPLE.values())) == len(K.PEOPLE), "personas distinct")
    # dates past the export: only the forward-looking plan and rates carry them (reduce-house-fixes H16)
    late = set()
    cut = dt.datetime(2026, 12, 14, 23, 59)
    for f in files:
        p = os.path.join(target, f)
        if f.endswith((".csv", ".json", ".txt")):
            for d in re.findall(r"\b(20\d\d-\d\d-\d\d)", open(p, encoding="utf-8").read()):
                if d > "2026-12-14":
                    late.add(f)
                    break
        elif f.endswith(".xlsx"):
            wbx = openpyxl.load_workbook(p, read_only=True)
            for wsx in wbx.worksheets:
                if any(isinstance(v, dt.datetime) and v > cut for row in wsx.iter_rows(values_only=True) for v in row):
                    late.add(f)
                    break
    ok(late == {K.HWPLAN, K.RATECARD}, "dates past the export only in the plan and the rate card: %s" % sorted(late))
    named = {f for f, _, _ in DOC.DICT}
    data_files = {f for f in files if f.rsplit(".", 1)[1] in ("csv", "json", "xlsx") and f != K.DICTIONARY}
    ok(named == data_files, "the dictionary names every data file: %s" % sorted(named ^ data_files))
    readme = open(os.path.join(target, K.README), encoding="utf-8").read()
    ok(all(f in readme for f in files if f != K.README), "the README lists every file")
    tag_rows = sum(1 for _ in A.status)
    ok(tag_rows > 5200, "inventory assets %d" % tag_rows)
    sf_ids = ["SF%d" % i for i in range(1, 28)]
    ok(len(sf_ids) == 27, "SF1 SF2 SF3 SF4 SF5 SF6 SF7 SF8 SF9 SF10 SF11 SF12 SF13 SF14 SF15 SF16 SF17 SF18 SF19 SF20 "
                          "SF21 SF22 SF23 SF24 SF25 SF26 SF27 asserted above or below")
    # SF20 to SF27: the asks' readings
    ok(all(C.ask_a(A, "s2")[0][t] != red[t] for t in A.teams), "SF20 own newest committed is another figure")
    ok(all(C.ask_a(A, "s3")[0][t] != red[t] for t in A.teams), "SF21 the commit time is another figure")
    redo = C.ask_a(A, "redo")[0]
    ok(sum(K.round_to(redo[t], 100) != K.round_to(red[t], 100) for t in A.teams) >= 3,
       "SF28 the resumed runs' redo core-hours are other figures (the wording counts the lost training's own)")
    ok(all(C.ask_a(A, "s1")[2][t] != heldh[t] for t in A.teams), "SF22 cores at start throughout is another figure")
    ok(all(K.round_to(s1[k], 10) != K.round_to(lost[k], 10) for k in lost), "SF23 same machine id is another figure")
    ok(all(K.round_to(c1[t], 100) != K.round_to(owe[t], 100) for t in A.firm), "SF25 request time is another figure")
    ok(all(K.round_to(c2[t], 100) != K.round_to(owe[t], 100) for t in A.firm), "SF26 the opening rate throughout")
    spares = [a for a in (W.assets if W is not None else []) if a["origin"] == "spare" and
              C.Q3S <= a["installed"] < C.Q3E]
    ok(W is None or len(spares) >= 3, "SF27 spares registered in Q3 (another asset, not a return): %d" % len(spares))
    _stage4_rows(target, M, g, lad, A, W, red, share, lost, owe, pre, succ, ev, rem, by_asset)
    _shared_precision(target, golden, M, g)
    print("checks: %d assertions passed" % N[0])
    return N[0]


def _shared_precision(target, golden, M, g):
    """The write-up and the goldens state each figure at the precision every converging variant shares (the fit
    windows, machines installed, the re-sent day kept, the gap interpolated, cell-ctl's forecast, the largest residual,
    the reservations rounded first); the golden path's own unrounded figures are stated nowhere a reader takes as a
    claim."""
    G = g["G"]
    variants = [g, C.golden(M, use_installed=True), C.golden(C.load(target, dedupe=False)),
                C.golden(C.load(target, gap="interpolate"))]
    for qs in (M.quarters[2:], M.quarters[4:]):
        variants += [C.golden(M, mask=np.isin(M.q, qs)), C.golden(M, mask=np.isin(M.q, qs), use_installed=True)]
    variants += [C.golden(M, ctl_how=h) for h in ("last", "mean4", "machines")] + [C.golden(M, allowance=g["resid_max"])]
    variants += list(C.other_fits(M).values())
    for v in variants:
        ok(("%.2f" % v["c"], "%.3f" % v["beta"], "%.3f" % (1 + v["beta"])) == ("2.94", "0.208", "1.208"),
           "shared precision: per machine %.5f, per batch core %.5f, per guaranteed core %.5f" % (
               v["c"], v["beta"], 1 + v["beta"]))
        ok(v["G"] == G and K.round_to(v["S"], 1000) == K.round_to(g["S"], 1000) and
           K.round_to(v["ctl"], 1000) == K.round_to(g["ctl"], 1000) and 0 < v["unreserved"] < 1000,
           "shared precision: the call, cell-store and cell-ctl to the thousand, under 1,000 left (%.1f)" %
           v["unreserved"])
    path_figures = ("{:,.0f}".format(g["Gu"]), "%.0f" % g["Gu"], "{:,.0f}".format(g["S"]), "%.0f" % g["S"],
                    "{:,.0f}".format(g["ctl"]), "%.1f" % g["ctl"], "%.4f" % g["c"], "%.5f" % g["beta"],
                    "%.5f" % (1 + g["beta"]), "%.1f" % g["a"], "%.1f" % g["unreserved"])
    sub = open(os.path.join(os.path.dirname(target), "submission.md"), encoding="utf-8").read()
    blocks13 = sub.split("## 4. Deliverable Answers")[0]
    ok(not [x for x in path_figures if x in blocks13], "the write-up's blocks 1 to 3 state no path figure: %s" %
       [x for x in path_figures if x in blocks13])
    ok(all(x in blocks13 for x in ("2.94 cores per machine", "0.208 per batch core", "**1.208**")),
       "the write-up states the shared precision")
    wb = openpyxl.load_workbook(os.path.join(golden, K.GOLD_BOOK), data_only=True)
    for name in ("2027 Q1", "cell-store"):
        flat = " ".join(str(v) for r in wb[name].iter_rows(values_only=True) for v in r if v is not None)
        ok(not [x for x in ("{:,.0f}".format(g["Gu"]), "%.4f" % g["c"], "%.5f" % g["beta"], "%.5f" % (1 + g["beta"]),
                            "%.1f" % g["S"], "%.1f" % g["ctl"], "%.1f" % g["platform"], "%.1f" % g["unreserved"])
                if x in flat], "golden sheet %s states no path figure" % name)
    top = {r[0]: r for r in wb["2027 Q1"].iter_rows(values_only=True) if r and isinstance(r[0], str)}
    ok(all(top[k][1] is None for k in ("cell-ctl", "cell-store", "Platform services", "Not reserved")) and
       "1.208" in top["Batch training guarantee"][3] and "2.94" in top["cell-store"][3],
       "golden: the platform services at the thousand only, the guarantee's note at the shared precision")
    terms = {r[0]: r[1] for r in wb["cell-store"].iter_rows(values_only=True) if r and r[0] in (
        "Intercept", "Per machine in service", "Per batch core running")}
    ok(terms["Per machine in service"] == 2.94 and terms["Per batch core running"] == 0.208,
       "golden cell-store sheet: the fit's terms at the shared precision")
    from pptx import Presentation
    deck = Presentation(os.path.join(golden, K.GOLD_DECK))
    cells = [c.text for sh in deck.slides[0].shapes if sh.has_table for r in sh.table.rows for c in r.cells]
    ok("under 1,000" in cells and "594" not in cells, "golden slide: the remainder stated as under 1,000")


def _charges(A, when_of, rate_of):
    """Each firm tenant's Q3 charge on this module's own path: a change counts on day d once when_of(change) <= d
    (00:00 UTC), the rate rate_of(day) divided by the days of its month."""
    out = {}
    for t in A.firm:
        base = A.ledger[("2026Q3", t)]
        ch = [(when_of(c), int(c["delta_cores"])) for c in A.changes if c["tenant"] == t]
        tot, d = 0.0, C.Q3S
        while d < C.Q3E:
            nxt = dt.date(d.year + (d.month == 12), 1 if d.month == 12 else d.month + 1, 1)
            tot += (base + sum(v for w, v in ch if w <= d)) * rate_of(d.date()) / (nxt - d.date().replace(day=1)).days
            d += dt.timedelta(days=1)
        out[t] = tot
    return out


def _stage4_rows(target, M, g, lad, A, W, red, share, lost, owe, pre, succ, ev, rem, by_asset):
    """SF29 to SF38 and the restated SF13, SF19, SF25 and SF26: the determinism judge's two risks, the leak reader's ask
    readings, and the three round-2 lessons (a filed sentence executing to the easy answer, a figure near its edge or
    moved by a defensible variant, an ask basis left unclosed)."""
    G = g["G"]
    gq = {q: M.ledger[(q, "batch-train")] for q in M.quarters}
    std = re.sub(r"\s+", " ", _text_of(os.path.join(target, K.STANDARD_PDF)))
    # SF29: the batch cores in cell-store's busiest hour are the reserved quarter's guarantee (CS-3 4.1 and 5.2)
    ok("is reserved for the quarter at the use forecast for its busiest hour of the quarter" in std and
       "Batch training runs inside its guarantee" in std,
       "SF29 CS-3 4.1 files the busiest hour of the quarter being reserved; 5.2 runs batch inside its guarantee")
    for i, q in enumerate(M.quarters):
        mm = M.q == q
        k = int(np.argmax(M.store[mm]))
        b = float(M.batch[mm][k])
        ok(b >= 0.996 * gq[q], "SF29 batch at cell-store's busiest hour of %s at its own guarantee (%.1f of %d)" % (
            q, b, gq[q]))
        if i:
            prev = gq[M.quarters[i - 1]]
            ok(prev != gq[q] and abs(b - gq[q]) < 200 and abs(b - prev) > 800,
               "SF29 %s: batch at its own quarter's guarantee %d, not the quarter before's %d" % (q, gq[q], prev))
    ok(lad["R2e"]["G"] == 120000 and lad["R2e"]["G"] != G, "SF29 batch at the last quarter's guarantee files 120,000")
    # SF30: the load read at another answer is not the guarantee that reading files; 109,000 is the one fixed point
    ok(lad["R2b"]["G"] == 106000 and lad["R2b"]["G"] != lad["R0"]["G"],
       "SF30 the load read at the default's 122,000 files 106,000, not the guarantee it was read at")
    fixed = [x for x in range(50000, 160001, 1000)
             if C.floor1000(M.R1 - g["F"] - g["ctl"] - (g["a"] + g["c"] * M.M1 + g["beta"] * x)) == x]
    ok(fixed == [G], "SF30 the one whole thousand whose own storage load leaves it: %s" % fixed)
    # SF13: the closed quarters do not separate the line from the drivers; the 640-machine step and the guarantee do
    steps = [M.machines_q[b] - M.machines_q[a] for a, b in zip(M.quarters, M.quarters[1:])]
    ok(max(steps) <= 60 and M.M1 - M.machines_q[M.quarters[-1]] == 640,
       "SF13 2027 Q1 opens 640 machines above 2026 Q4; no quarter on file stepped more than %d" % max(steps))
    for i in range(4, len(M.quarters)):
        q = M.quarters[i]
        actual = float(M.store[M.q == q].max())
        line = C.line_forecast([C.qmax(M, M.store, x) for x in M.quarters[i - 4:i]])
        co, _ = C.fit(M, [M.mach, M.batch], np.isin(M.q, M.quarters[:i]))
        drv = float(co[0] + co[1] * M.machines_q[q] + co[2] * gq[q])
        ok(abs(line - actual) < 500 and abs(drv - actual) < 500,
           "SF13 back-test %s: the line misses by %.0f, the drivers by %.0f; the closed quarters do not separate them" % (
               q, line - actual, drv - actual))
    r_m = float(C.fit(M, [M.mach])[1].std())
    r_b = float(C.fit(M, [M.batch])[1].std())
    ok(r_m > 600 and r_b > 300 and g["resid_sd"] < 70,
       "SF13 the hourly fit needs both drivers: residual s.d. %.1f on machines alone, %.1f on batch alone, %.1f on both"
       % (r_m, r_b, g["resid_sd"]))
    ok(lad["R2e"]["S"] - lad["R0"]["S"] > 1500,
       "SF13 the 640-machine step alone puts cell-store %.0f cores above the line" % (lad["R2e"]["S"] - lad["R0"]["S"]))
    # SF31: no filed sentence confines the platform forecast to the export (lesson 1)
    memo = re.sub(r"\s+", " ", _text_of(os.path.join(target, K.MEMO)))
    ok("from the cell monitoring export" not in memo and "prepares the cell-ctl and cell-store reservations." in memo,
       "SF31 the memo names no source for the platform reservations")
    ok("the hardware plan" in std and lad["R2d"]["G"] != G,
       "SF31 CS-3 6.2 lists the hardware plan; the export alone (4,640 machines) files %d" % lad["R2d"]["G"])
    # SF38: the reservations rounded to the thousand before the subtraction (rounding path)
    Gr = C.floor1000(M.R1 - K.round_to(g["F"], 1000) - K.round_to(g["ctl"], 1000) - K.round_to(g["S"], 1000))
    ok(Gr == G, "SF38 the reservations rounded first: the same call (%d)" % Gr)
    af = float(np.mean([M.batch[M.q == q].mean() / gq[q] for q in M.quarters]))
    spread = [C.golden(M, ctl_how=h)["Gu"] for h in ("trend4", "last", "mean4", "machines")]
    spread += [C.golden(M, mask=np.isin(M.q, M.quarters[2:]))["Gu"], C.golden(M, mask=np.isin(M.q, M.quarters[4:]))["Gu"],
               C.golden(M, use_installed=True)["Gu"], C.golden(M, allowance=g["resid_max"])["Gu"],
               (M.R1 - g["F"] - g["ctl"] - g["a"] - g["c"] * M.M1) / (1 + g["beta"] * af),
               M.R1 - K.round_to(g["F"], 1000) - K.round_to(g["ctl"], 1000) - K.round_to(g["S"], 1000)]
    ok(all(C.floor1000(x) == G for x in spread) and min(spread) - G > 400 and G + 1000 - max(spread) > 250,
       "SF38 every converging variant floors to %d (before the thousand %.0f to %.0f)" % (G, min(spread), max(spread)))
    s_spread = [C.golden(M, mask=np.isin(M.q, qs))["S"] for qs in (M.quarters[2:], M.quarters[4:])]
    s_spread += [C.golden(M, use_installed=True)["S"], C.golden(M, allowance=g["resid_max"])["S"],
                 C.golden(M, G_in_store="unrounded")["S"]]
    ok(all(K.round_to(x, 1000) == K.round_to(g["S"], 1000) for x in s_spread),
       "SF38 cell-store to the thousand under every variant (%.0f to %.0f)" % (min(s_spread), max(s_spread)))
    # SF19: the directory's cost-centre format against the workbook's number
    ok(all(re.fullmatch(r"CC-\d{4} .+", M.cc[t]) for t in M.firm) and
       all(re.fullmatch(r"\d{4}", str(x["CC"])) for x in M.budget_lines),
       "SF19 the directory's 'CC-dddd name' against the workbook's dddd: joined by number or by name, the same lines")
    # SF32: a checkpoint write with no commit time (under way at the preemption, or failed) is never the restore point
    mid = 0
    for r in pre:
        own = sorted(A.ckpt_by_run.get(r["run_id"], []), key=lambda c: c["write_started_utc"])
        if own and not own[-1]["committed_utc"]:
            mid += 1
            ok(succ[r["run_id"]]["restore_checkpoint"] != own[-1]["checkpoint_id"],
               "SF32 no resumption restores a write that did not complete")
    ok(mid >= 5, "SF32 preemptions whose newest write has no commit time: %d" % mid)
    ok(all(A.ckpt[s["restore_checkpoint"]]["committed_utc"] for s in succ.values() if s["restore_checkpoint"]),
       "SF32 every restore point in the file is a committed checkpoint")
    # SF33: runs still running at the snapshot hold core-hours to 1 October 00:00
    running = [r for r in A.runs if not r["ended_utc"]]
    ok(len(running) > 20 and all(r["end_state"] == "RUNNING" for r in running), "SF33 %d runs running at the snapshot" %
       len(running))
    held_nr = {t: 0.0 for t in A.teams}
    held_all = {t: 0.0 for t in A.teams}
    for r in A.runs:
        segs = C.segments(A, r)
        if r["ended_utc"]:
            held_nr[r["team"]] += C.core_hours(segs, C.Q3S, C.Q3E)
        held_all[r["team"]] += C.core_hours(segs, dt.datetime(2026, 1, 1, tzinfo=C.UTC), C.Q3E)
    ok(sum(_pct2(100.0 * red[t] / held_nr[t]) != _pct2(share[t]) for t in A.teams) == 4,
       "SF33 leaving the running runs out moves four teams' shares")
    # SF34: runs started before 1 July count from 1 July; no lost training before it
    ok(sum(1 for r in A.runs if C.tparse(r["started_utc"]) < C.Q3S) > 20 and
       sum(_pct2(100.0 * red[t] / held_all[t]) != _pct2(share[t]) for t in A.teams) == 2 and
       (_pct2(100.0 * red["reco-ml"] / held_all["reco-ml"]), _pct2(100.0 * red["nlp-ml"] / held_all["nlp-ml"])) ==
       (0.58, 0.76), "SF34 the runs' whole lives (from June) move two teams' shares (reco-ml 0.58, nlp-ml 0.76)")
    ok(all(C.tparse(r["started_utc"]) >= C.Q3S for r in pre) and
       all(C.tparse(A.ckpt[succ[r["run_id"]]["restore_checkpoint"]]["write_started_utc"]) >= C.Q3S for r in pre),
       "SF34 no lost training before 1 July: clipped or not, the lost core-hours are the same")
    # SF35: a removal with no return is a machine the inventory retired that day
    wbi = openpyxl.load_workbook(os.path.join(target, K.INVENTORY), read_only=True, data_only=True)
    retired_on = {r[0]: r[8] for r in wbi["Assets"].iter_rows(values_only=True)
                  if r and isinstance(r[0], str) and r[0].startswith("SRV-")}
    seen, open_rm = set(), []
    for r in rem:
        a = A.asset_of[int(r["machine_id"])]
        if tuple(r.values()) in seen:
            continue
        seen.add(tuple(r.values()))
        if not any(x["event"] == "REGISTERED" and x["time_utc"] > r["time_utc"] for x in by_asset[a]):
            open_rm.append(r)
            ok(A.status[a] == "retired" and retired_on[a] is not None and
               retired_on[a].date().isoformat() == r["time_utc"][:10],
               "SF35 a removal with no return (%s) is an asset retired that day" % a)
    ok(len(open_rm) >= 3, "SF35 removals of retired machines: %d" % len(open_rm))
    to_end = dict(lost)
    for r in open_rm:
        k = (r["cause"], int(r["time_utc"][5:7]))
        to_end[k] += (C.Q3E - C.tparse(r["time_utc"])).total_seconds() / 3600.0
    ok(all(K.round_to(to_end[("hw_fault", m)], 10) != K.round_to(lost[("hw_fault", m)], 10) for m in (7, 8, 9)),
       "SF35 counting them to 30 September moves every hardware-fault month")
    # SF23: every Q3 registration in the inventory's Cluster ids sheet is a cluster-manager event at the same minute
    q3ids = [(int(r[1]), r[2]) for r in wbi["Cluster ids"].iter_rows(values_only=True)
             if r and isinstance(r[0], str) and r[0].startswith("SRV-") and "2026-07-01" <= r[2] < "2026-10-01"]
    evk = {(int(x["machine_id"]), x["time_utc"][:16].replace("T", " ")) for x in ev if x["event"] == "REGISTERED"}
    ok(len(q3ids) > 200 and all(k in evk for k in q3ids) and all(int(x["machine_id"]) in A.asset_of for x in ev),
       "SF23 the Cluster ids sheet carries every Q3 registration (%d) and every event's machine id" % len(q3ids))
    # SF37: hours split by Madrid local month (CEST, UTC+2, from July to September) give the same six figures
    bounds = [dt.datetime(2026, 6, 30, 22, tzinfo=C.UTC), dt.datetime(2026, 7, 31, 22, tzinfo=C.UTC),
              dt.datetime(2026, 8, 31, 22, tzinfo=C.UTC), dt.datetime(2026, 9, 30, 22, tzinfo=C.UTC),
              dt.datetime(2026, 10, 31, 23, tzinfo=C.UTC)]
    seen2, loc = set(), {k: 0.0 for k in lost}
    evs = sorted((dict(x, t=C.tparse(x["time_utc"])) for x in ev), key=lambda x: x["t"])
    for x in evs:
        if x["event"] != "REMOVED" or tuple((k, x[k]) for k in sorted(x) if k != "t") in seen2:
            continue
        seen2.add(tuple((k, x[k]) for k in sorted(x) if k != "t"))
        a = A.asset_of[int(x["machine_id"])]
        y = next((y for y in evs if y["event"] == "REGISTERED" and y["t"] > x["t"] and A.asset_of[int(y["machine_id"])] == a),
                 None)
        if y is None:
            continue
        for m, (lo, hi) in zip((7, 8, 9, 10), zip(bounds[:-1], bounds[1:])):
            h = (min(y["t"], hi) - max(x["t"], lo)).total_seconds() / 3600.0
            if h > 0:
                loc[(x["cause"], m)] = loc.get((x["cause"], m), 0.0) + h
    ok(all(K.round_to(loc[k], 10) == K.round_to(lost[k], 10) for k in lost),
       "SF37 the outages split by Madrid local month: the same six figures")
    # SF36: 19 August: the power event removed no machine; the re-sent removals are byte-identical
    ok(not [r for r in ev if r["event"] == "REMOVED" and "2026-08-19T01:40" <= r["time_utc"] < "2026-08-19T07:00"],
       "SF36 no removal between the power event (01:40 UTC) and the day's maintenance wave")
    ok(W is None or W.mev_resent == 4, "SF36 the cluster manager re-sent four removals")
    # SF25: chargeback policy 2.2 files when a change counts; its literal reading is the golden
    pol = re.sub(r"\s+", " ", _text_of(os.path.join(target, K.CHARGEBACK)))
    ok("A release or grant counts from the first 00:00 UTC after the cell's quota service has applied it." in pol,
       "SF25 policy 2.2 files when a release or grant counts")
    fin, start = {}, {}
    for r in A.qruns:
        for cid in filter(None, r["changes_applied"].split(";")):
            fin[cid], start[cid] = C.tparse(r["run_finished_utc"]), C.tparse(r["run_started_utc"])
    day_rate = lambda d: C.rate_on(A.rates, d)
    nextmid = lambda t: dt.datetime(t.year, t.month, t.day, tzinfo=C.UTC) + dt.timedelta(days=1)
    lit = _charges(A, lambda c: nextmid(fin[c["change_id"]]), day_rate)
    ok(all(K.round_to(lit[t], 100) == K.round_to(owe[t], 100) for t in A.firm),
       "SF25 policy 2.2 read literally (the first 00:00 after the applying run finished) gives the golden for all 11")
    ok(all(nextmid(start[c]) == nextmid(fin[c]) for c in fin), "SF25 the applying run's start or finish: same midnight")
    for lab, when, n in (("the request time", lambda c: C.tparse(c["requested_utc"]), 11),
                         ("the request day's own 00:00", lambda c: C.tparse(c["requested_utc"]).replace(
                             hour=0, minute=0, second=0), 10),
                         ("the day the change was applied", lambda c: start[c["change_id"]].replace(
                             hour=0, minute=0, second=0), 10)):
        v = _charges(A, when, day_rate)
        miss = sum(K.round_to(v[t], 100) != K.round_to(owe[t], 100) for t in A.firm)
        ok(miss == n, "SF25 from %s misses %d of 11" % (lab, miss))
    # SF26: the September rate split
    pub = [r for r in C.rows(os.path.join(target, K.RATECARD)) if r["effective_from"] == "2026-09-01"]
    ok(len(pub) == 1 and pub[0]["published_on"] < "2026-09-01", "SF26 the September rate published before it applies")
    p0 = dt.date.fromisoformat(pub[0]["published_on"])
    for lab, rate in (("the September rate all quarter", lambda d: C.rate_on(A.rates, dt.date(2026, 9, 1))),
                      ("the rate from its publication", lambda d: C.rate_on(A.rates, dt.date(2026, 9, 1)) if d >= p0
                       else C.rate_on(A.rates, dt.date(2026, 7, 1)))):
        v = _charges(A, lambda c: nextmid(fin[c["change_id"]]), rate)
        ok(sum(K.round_to(v[t], 100) != K.round_to(owe[t], 100) for t in A.firm) == 11, "SF26 %s misses all 11" % lab)
    ok(C.rate_on(A.rates, dt.date(2026, 8, 31)) != C.rate_on(A.rates, dt.date(2026, 9, 1)),
       "SF26 the rate changes at a month boundary, so September is one rate")


def _text_of(path):
    if path.endswith(".pdf"):
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    if path.endswith(".docx"):
        import docx
        d = docx.Document(path)
        return "\n".join([p.text for p in d.paragraphs] + [c.text for t in d.tables for r in t.rows for c in r.cells])
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, read_only=True)
        return "\n".join(" ".join("" if v is None else str(v) for v in row) for ws in wb.worksheets
                         for row in ws.iter_rows(values_only=True))
    return open(path, encoding="utf-8").read()


def _three_rules(target, M, g, lad, W):
    """dataset-generation 7.1: the client's three rules asserted on the clean truth (the world before any mess or
    document) and on the pack."""
    G = g["G"]
    # R1: the field's raw material ships, and no shipped column or sentence holds the deciding quantity
    ok(g["n"] >= 16000, "R1 the decisive fit reads %d hourly rows of cell-store, batch-train and machines" % g["n"])
    texts = {f: _text_of(os.path.join(target, f)) for f in os.listdir(target)
             if not f.endswith(".csv") or os.path.getsize(os.path.join(target, f)) < 2_000_000}
    for f, t in texts.items():
        for pat in (r"\b2\.94\d*\b", r"\b0\.208\d*\b", r"\b109,?000\b", r"\b38,?0[0-9]{2}\b", r"\b1\.208\d*\b"):
            ok(not re.search(pat, t), "R1 %s states no deciding quantity (%s)" % (f, pat))
    with open(os.path.join(target, K.USAGE), encoding="utf-8") as fh:
        head = fh.readline().strip().split(",")
    ok(head == ["hour_start_utc", "cell", "tenant", "cores_in_use"], "R1 the export is one use series per tenant")
    # R2: every Layer 1 item, mishandled the natural way, leaves the call and its components where they were
    comps = (G, K.round_to(g["F"], 1000), K.round_to(g["S"], 1000), K.round_to(g["ctl"], 1000))

    def same(gx, lab):
        ok((gx["G"], K.round_to(gx["F"], 1000), K.round_to(gx["S"], 1000), K.round_to(gx["ctl"], 1000)) == comps,
           "R2 %s leaves the call and its components" % lab)
    same(C.golden(C.load(target, dedupe=False)), "the re-sent day of 17 March kept twice")
    same(C.golden(C.load(target, gap="interpolate")), "the collector's seven missing hours interpolated")
    same(C.golden(M, use_installed=True), "machines installed read for machines in service")
    by_name = {}
    for t in M.firm:
        name = M.cc[t].split(" ", 1)[1]
        line = [x for x in M.budget_lines if x["Cost centre"] == name and x["Budget line"] == "MAD1 C-22 reserved cores"]
        by_name[t] = min(M.requests[t], int(math.floor(line[0]["Jan 2027"] / M.rate_q1 + 1e-9)))
    ok(by_name == C.firm_approvals(M), "R2 cost centres joined by name instead of number: the same approvals")
    summed = {}
    for t in M.firm:
        code = M.cc[t].split()[0].replace("CC-", "")
        tot = sum(x["Jan 2027"] for x in M.budget_lines if str(x["CC"]) == code)
        summed[t] = min(M.requests[t], int(math.floor(tot / M.rate_q1 + 1e-9)))
    ok(summed == C.firm_approvals(M), "R2 every budget line of a cost centre summed: the same approvals")
    for m in ("Dec 2026", "Feb 2027", "Mar 2027"):
        ok(C.firm_approvals(M, budget_month=m) == C.firm_approvals(M), "R2 the %s column: the same approvals" % m)
    rates = C.rows(os.path.join(target, K.RATECARD))
    ok({(r["resource"], r["site"]) for r in rates} == {("reserved core", "MAD1")},
       "R2 the rate card carries MAD1 reserved cores only, so the 2027 row is the one row in force")
    # R3a: the easy route on the clean truth files the named wrong answer
    hrs = W.hours
    qidx = np.array([K.QUARTERS.index(K.q_of(t)) for t in hrs])
    smax = [float(W.store_h[qidx == i].max()) for i in range(len(K.QUARTERS))]
    cmax = [float(W.ctl_h[qidx == i].max()) for i in range(len(K.QUARTERS))]
    R1 = int(round(K.Q1_MACHINES * K.CORES * K.OVERCOMMIT))
    ctl0 = C.line_forecast(cmax[-4:])
    G0 = C.floor1000(R1 - W.q1_firm - ctl0 - C.line_forecast(smax[-4:]))
    ok(G0 == 122000 and G0 != G, "R3a the default path on the clean truth files %d" % G0)
    # R3b: the easy route with only the decisive step changed files the golden; single lower corrections do not
    X = np.column_stack([np.ones(len(hrs)), W.inservice_h, W.batch_h])
    co, *_ = np.linalg.lstsq(X, W.store_h, rcond=None)
    Gt = C.floor1000((R1 - W.q1_firm - ctl0 - co[0] - co[1] * K.Q1_MACHINES) / (1 + co[2]))
    ok(Gt == G, "R3b the decisive step alone, on the clean truth, files the golden %d" % Gt)
    m4 = qidx == len(K.QUARTERS) - 1
    k = int(np.argmax(W.store_h[m4]))
    per_machine = float(W.store_h[m4][k]) / float(W.inservice_h[m4][k]) * K.Q1_MACHINES
    Xb = np.column_stack([np.ones(len(hrs)), W.batch_h])
    cb, *_ = np.linalg.lstsq(Xb, W.store_h, rcond=None)
    for lab, Gx in (("storage per machine", C.floor1000(R1 - W.q1_firm - ctl0 - per_machine)),
                    ("storage on batch alone", C.floor1000((R1 - W.q1_firm - ctl0 - cb[0]) / (1 + cb[1]))),
                    ("the batch load once at the default's guarantee",
                     C.floor1000(R1 - W.q1_firm - ctl0 - (co[0] + co[1] * K.Q1_MACHINES + co[2] * G0)))):
        ok(Gx != G, "R3b %s alone stays wrong (%d)" % (lab, Gx))
    # R3c: no plant: no copied block in any series, no document carrying a 2027 guarantee or a storage method
    for name in M.use:
        v = [M.use[name][h] for h in M.hours]
        runs = max((len(list(grp)) for _, grp in __import__("itertools").groupby(v)), default=0)
        ok(runs < 6, "R3c no repeated block in the %s series (longest run %d)" % (name, runs))
    for f in (K.MEMO, K.STANDARD_PDF, K.CAPREPORT, K.OPSLOG, K.BATCH_DEMAND, K.README):
        t = re.sub(r"\s+", " ", texts[f]).lower()
        ok("per batch core" not in t and "per machine" not in t and "guarantee of" not in t,
           "R3c %s carries no storage method or 2027 guarantee" % f)


def _pct2(x):
    return math.floor(x * 100 + 0.5) / 100.0


def _count_dup_rows(path):
    c = collections.Counter(open(path, encoding="utf-8").read().splitlines())
    return sum(v - 1 for v in c.values())
