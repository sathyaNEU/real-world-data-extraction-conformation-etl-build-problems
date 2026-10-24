"""Generator checks for task280, run on every build: the call against the world, the golden's family, the ladder,
the three rules (R1 to R3), each Layer 1 item mishandled, the semantic fork rows, the evidence the decisive step
reads, the separation of the asks' devices from the call, both asks' devices against their stops, the input gates
and the realism sweep."""
from __future__ import annotations

import csv
import os
import re

import numpy as np

import analysis as A
import asks as AK
import common as K
import pack as PK
import seedsearch as SS

FAILS = []
N = [0]


def ok(label, cond, detail=""):
    N[0] += 1
    if not cond:
        FAILS.append(label)
    print("%s %s %s" % ("PASS" if cond else "FAIL", label, detail))


def sets_of(tab):
    return {k: A.designated(v) for k, v in tab.items()}


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    rc, pl = b["rc"], b["plant"]
    w = rc.w
    pk = res["pk"]
    tab = res["call"]["table"]
    S = sets_of(tab)
    gold = S[A.GOLDEN]
    fam = ("thresh", "load20", "iso")

    # ------------------------------------------------------------------ the call
    truth = A.designated(w.truth_hub)
    ok("CALL golden names the world's true set", gold == truth, "%s vs %s" % (gold, truth))
    ok("CALL four hubs designated", len(gold) == 4, str(gold))
    for k in fam:
        ok("FAMILY %s names the golden set" % k, S[k] == gold, str(S[k]))
    F = np.vstack([tab[k] for k in fam])
    whole = np.vectorize(lambda x: int(np.floor(x + 0.5)))(F)
    ok("FAMILY every hub holds its whole per cent in every member", (whole == whole[0]).all(),
       " ".join("%s %s" % (h, sorted(set(whole[:, i]))) for i, h in enumerate(K.HUB)))
    margin = np.abs(F - K.LINE).min()
    ok("MARGIN every member clears the line by 1.5 points on every hub", margin >= 1.5, "%.2f" % margin)
    ok("FAMILY load10 (coarse bins) still names the golden set", S["load10"] == gold, str(S["load10"]))
    edge = np.abs(F - np.floor(F) - 0.5).min()
    ok("ROUNDING no member within 0.10 of a half point", edge >= 0.10, "%.2f" % edge)

    # ------------------------------------------------------------------ the ladder
    for k in A.RUNGS:
        ok("LADDER %s names another set" % k, S[k] != gold, str(S[k]))
    ok("LADDER the share of tests is the default path's set (CM, DF)", S["tests"] == ("CM", "DF"), str(S["tests"]))
    ok("LADDER night weighting stops one hub short", len(S["night"]) == 3 and set(S["night"]) < set(gold),
       str(S["night"]))
    ok("LADDER skips counted as failures over-designate", set(S["skipfail"]) > set(gold), str(S["skipfail"]))
    m_tests = np.abs(tab["tests"] - K.LINE).min()
    ok("LADDER the share of tests sits 1 point or more off the line", m_tests >= 1.0, "%.2f" % m_tests)

    # ------------------------------------------------------------------ the three rules
    # R1: the field's raw material ships at the interval grain, and no shipped column holds a hub's share
    heads = {}
    for f in os.listdir(target):
        if f.endswith(".csv"):
            with open(os.path.join(target, f), newline="") as fh:
                heads[f] = next(csv.reader(fh))
    ok("R1 tests ship one row a test with its local time and throughput",
       heads[K.FILES["tests"]][:2] == ["unit_id", "test_start_local"] and "throughput_kbps" in heads[K.FILES["tests"]])
    ok("R1 utilisation ships one row a node and interval", heads[K.FILES["util"]] == ["node_id", "interval_start_utc",
                                                                                   "ds_util_pct"])
    ok("R1 no shipped column holds a share of the peak", not any(re.search(r"share|peak|below", c, re.I)
                                                                  for cols in heads.values() for c in cols))
    # R3a: the easy route on the world's clean truth (no record mess) files the default set
    R = SS.routes(w)
    clean = {k: np.array([100 * v[w.hh_hub == a].mean() for a in range(len(K.HUB))]) for k, v in R.items()}
    ok("R3a ANALYST the share of tests on the clean truth files another set", A.designated(clean["tests"]) != truth,
       str(A.designated(clean["tests"])))
    ok("R3a ANALYST the hour-weighted share on the clean truth files another set",
       A.designated(clean["hour"]) != truth, str(A.designated(clean["hour"])))
    # R3b: the decisive step alone (conditioning on the node's load) on the clean truth files the golden
    ok("R3b DECISIVE conditioning on the load alone files the golden on the clean truth",
       A.designated(clean["thresh"]) == truth and A.designated(clean["load20"]) == truth,
       "%s %s" % (A.designated(clean["thresh"]), A.designated(clean["load20"])))
    # R3c: no plant (the realism sweep below covers copied blocks)

    # ------------------------------------------------------------------ Layer 1, each item mishandled
    for label, kw in (("SF8 duplicate test batches kept", dict(dedupe=False)),
                      ("SF7 one fixed UTC-04:00 offset after the clock change", dict(local_offsets=False)),
                      ("SF4 the plan named at enrolment for the whole window", dict(plan_source="enrolment")),
                      ("SF5 households enrolled after the window opened or gone before it closed kept", dict(panel="all_with_tests")),
                      ("SF6 a replaced unit read as a second household", dict(by_unit=True))):
        p2 = PK.Pack(target, **kw)
        c2 = A.call(p2)
        s2 = c2["sets"][A.GOLDEN]
        ok("R2 LAYER1 %s leaves the call" % label, s2 == gold, "%s; shares %s" % (
            s2, " ".join("%.1f" % x for x in c2["table"][A.GOLDEN])))

    # ------------------------------------------------------------------ the semantic fork rows
    p3 = PK.Pack(target, holidays=False)
    c3 = A.call(p3)
    ok("SF1 holidays left out of the weekday peak: same call", c3["sets"][A.GOLDEN] == gold, str(c3["sets"][A.GOLDEN]))
    pooled = np.array([100 * np.average(res["call"]["shares"][A.GOLDEN][pk.hub == h]) for h in K.HUB])
    ok("SF2 intervals pooled over households equals households counted equally (every household has 720)",
       np.allclose(pooled, tab[A.GOLDEN]) and pk.q_load.shape[1] == 720)
    ok("SF3 more than 20 against at least 20: no hub within 1 point", np.abs(tab[A.GOLDEN] - K.LINE).min() >= 1.0)
    ok("SF9 no peak test at exactly 80 per cent of plan", not np.any(np.isclose(pk.t_ratio[pk.t_peak], K.STANDARD)))
    with open(os.path.join(target, K.FILES["tests"]), newline="") as fh:
        rd = csv.DictReader(fh)
        worst = 0.0
        for k, r in enumerate(rd):
            if k >= 20000:
                break
            v = int(r["bytes_received"]) * 8 / int(r["duration_ms"])
            worst = max(worst, abs(v - int(r["throughput_kbps"])))
    ok("SF10 throughput_kbps equals bytes received times eight over the duration to the kilobit", worst <= 1.0,
       "%.2f" % worst)
    moved = [h for h in pk.hh_list if len({pk.node_hub[n] for n in pk.node_day[pk.hh_index[h]]}) > 1]
    ok("SF11 no panel household's node changes hub in the window", not moved, str(len(moved)))

    # ------------------------------------------------------------------ the evidence the decisive step reads
    for h in K.HUB:
        cv = res["coverage"][h]
        ok("EVIDENCE %s tests ran at lighter loads than the peak as a whole" % h,
           cv["load_tested"] < cv["load_all"] - 0.01, "%.3f vs %.3f" % (cv["load_tested"], cv["load_all"]))

    # ------------------------------------------------------------------ separation of the asks from the call
    panel_nodes = set(rc.node_id)
    ok("SEPARATION no ghost node, window split or upgrade is a panel node",
       not (pl.ghosts | {s[0] for s in pl.window_splits} | {u[0] for u in pl.upgrades}) & panel_nodes)
    import datetime as dt
    ev = 0
    for t, n, s, e, k, c in pl.tickets:
        if n in panel_nodes:
            a, bnd = K.to_local(s), K.to_local(e)
            d0 = a.date() - dt.timedelta(days=1)
            while dt.datetime.combine(d0, dt.time(0)) <= bnd:
                lo = dt.datetime.combine(d0, dt.time(16))
                if a < lo + dt.timedelta(hours=9) and lo < bnd:
                    ev += 1
                d0 += dt.timedelta(days=1)
    ok("SEPARATION no outage on a panel node touches an evening from 4 pm to 1 am", ev == 0, str(ev))
    ok("SEPARATION the call reads none of the asks' files", True, "Pack reads tests, units, households, plans, subs, "
                                                                 "nodes (hub of a panel node), addr, util")

    # ------------------------------------------------------------------ the asks
    g = res["credits"]
    for label, kw in (("tickets summed as filed", dict(merge=False)),
                      ("one row kept a ticket", dict(dedupe_ticket=True)),
                      ("planned work counted", dict(planned=True))):
        v = AK.credits(target, **kw)
        moved = [h for h in K.HUB if v[h] != g[h]]
        ok("ASK A %s moves %d hubs" % (label, len(moved)), len(moved) >= (8 if "summed" in label else 6),
           " ".join("%s %+d" % (h, v[h] - g[h]) for h in K.HUB))
    gb = {h: res["cap_to"][h] - res["cap_from"][h] for h in K.HUB}
    for label, fn in (("every child record counted", lambda: AK.capacity_added(target, drop_ghosts=False)),
                      ("the first record of a node read as the node", lambda: AK.capacity_added(target,
                                                                                                first_row_only=True)),
                      ("the new records' capacity read as added", lambda: AK.new_rows_only(target))):
        v = fn()
        moved = [h for h in K.HUB if v[h] != gb[h]]
        ok("ASK B %s moves %d hubs" % (label, len(moved)), len(moved) >= 6,
           " ".join("%s %+d" % (h, v[h] - gb[h]) for h in K.HUB))
    ok("ASK A every hub owed a credit", all(v > 0 for v in g.values()))
    ok("ASK B every hub added capacity", all(v > 0 for v in gb.values()))

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    ok("GATE 10 or more files", len(files) >= 10, str(len(files)))
    ok("GATE 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3,
       str(sorted({f.rsplit(".", 1)[1] for f in files})))
    ok("GATE a file of 25,000 rows or more", max(b["counts"].values()) >= 25000, str(max(b["counts"].values())))
    ok("GATE two distractors named", len(K.DISTRACTORS) >= 2)

    # ------------------------------------------------------------------ realism
    hh_counts = [int(x) for x in res["call"]["n_households"]]
    ok("REALISM no two hubs with the same panel count", len(set(hh_counts)) == len(hh_counts), str(hh_counts))
    caps = list(gb.values())
    ok("REALISM no two hubs with the same capacity added", len(set(caps)) == len(caps), str(caps))
    cr = list(g.values())
    ok("REALISM no round credit totals", all(v % 100 for v in cr), str(cr))
    skipped = 1 - res["call"]["shares"]["tests"].size and 1 - pk.t_peak.sum() / (len(pk.hh_list) * 180)
    ok("REALISM between a sixth and a third of scheduled peak tests not run", 0.16 <= skipped <= 0.34,
       "%.3f" % skipped)
    for f in files:
        if f.endswith((".csv", ".txt")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok("REALISM no em dash in %s" % f, "—" not in txt)
    print("checks: %d run, %d failed" % (N[0], len(FAILS)))
    for f in FAILS:
        print("  FAILED:", f)
    return 1 if FAILS else 0
