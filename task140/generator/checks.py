"""Assertions on the built pack and the goldens: the call and every rung reproduce from the shipped files, every
semantic-fork row (SF1 to SF27) is closed as the design note says, the asks' devices and stops land where the ask
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
    ok(12.0 < g["resid_sd"] < 14.0 and g["n"] > 16000, "fit residual sd %.2f on %d hours" % (g["resid_sd"], g["n"]))
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
    expect = {"R-1": 119000, "R0": 122000, "R0b": 122000, "R0c": 122000, "R0d": 122000, "R0e": 122000,
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
    ok(C.golden(M, allowance=g["resid_max"])["G"] == G and 30 < g["resid_max"] < 70,
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
    print("checks: %d assertions passed" % N[0])
    return N[0]


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
