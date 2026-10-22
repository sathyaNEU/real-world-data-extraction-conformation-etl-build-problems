"""Assertions for task446 (architecture 3). Builds the pack twice, runs the independent solver on it and checks
the design: the cohorts and the forward book by where each flag was raised; the analyst test executed on the clean
truth (the easy route files 64, the decisive step alone gives 78); the convergence of every member of the family that
takes the decisive step and the spread of the family that skips it; the out-of-sample record; the literal reading
(CRM-07 files the estimand only); the semantic fork rows; the bins; the ask devices, alone and in a grid, the measured
pair ceiling, and the separation of the main call from every device; the inert texture on the main path; the realism
repairs and the input gates.

    python3 task446/generator/checks.py
"""
import csv
import datetime as dt
import filecmp
import itertools
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world      # noqa: E402
import solve      # noqa: E402
import make       # noqa: E402

N_ASSERT = 0
CALL = 78
EASY = 64


def ok(cond, msg):
    global N_ASSERT
    N_ASSERT += 1
    if not cond:
        raise AssertionError(msg)


def margin(x, step=0.1):
    y = x / step
    return 0.5 - abs(y - round(y))


def r1(x):
    return round(x + 1e-12, 1)


def band_figures(bt):
    """the 25 graded band figures, at their reported precision"""
    out = []
    for r in bt:
        out += [r["groups"], r1(r["committed"] / 1e6), r["flagged"], r1(r["exp_arrivals"]), r1(r["exp_exposure"] / 1e6)]
    return out


def n_moved(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def clean_truth():
    """the analyst test on the generator's own design counts, before any file is written (dataset-generation 7.1):
    the easy route (one rate for flagged groups and one for the rest, the four closed cohorts taken together) and
    the decisive step alone (a rate by where the flag was raised)"""
    N, D, I = world.N_TARGET, world.D_FLAG, world.I_FLAG
    U = [n - a - b for n, a, b in zip(N[:4], D, I)]
    F = [a + b for a, b in zip(D, I)]
    TP = [a + b for a, b in zip(world.D_REACH, world.I_REACH)]
    hit, miss = sum(TP) / sum(F), sum(world.U_REACH) / sum(U)
    u4 = N[4] - world.F_FWD
    easy = world.F_FWD * hit + u4 * miss
    pd_, pi, pu = world.probs()
    decisive = world.D_FWD * pd_ + world.I_FWD * pi + u4 * pu
    return easy, decisive


def main():
    target = os.path.join(HERE, "..", "target")
    # ------------------------------------------------------------ two builds byte-identical, target current
    tmp = tempfile.mkdtemp()
    a, b, nd = os.path.join(tmp, "a"), os.path.join(tmp, "b"), os.path.join(tmp, "nodev")
    for t in (a, b):
        subprocess.run([sys.executable, os.path.join(HERE, "make.py"), t], check=True, capture_output=True)
    subprocess.run([sys.executable, os.path.join(HERE, "make.py"), nd, "--no-devices"], check=True,
                   capture_output=True)
    names = sorted(os.listdir(a))
    ok(names == sorted(os.listdir(b)), "file lists differ between builds")
    for n in names:
        ok(filecmp.cmp(os.path.join(a, n), os.path.join(b, n), shallow=False), "build differs: " + n)
        ok(filecmp.cmp(os.path.join(a, n), os.path.join(target, n), shallow=False), "target/ is stale: " + n)

    w = world.build()
    G = solve.golden(target)
    pk, tab, fc = G["pack"], G["tab"], G["fc"]
    cc = fc["cc"]

    # ------------------------------------------------------------ cohorts and the forward book as designed
    for c in range(4):
        x = cc[c]
        ok(x["N"] == world.N_TARGET[c] and x["P"] == world.P_REACH[c], "cohort %d size and arrivals" % c)
        ok((x["D"], x["D_R"], x["I"], x["I_R"], x["U_R"]) ==
           (world.D_FLAG[c], world.D_REACH[c], world.I_FLAG[c], world.I_REACH[c], world.U_REACH[c]),
           "cohort %d flags by kind and arrivals by kind as designed %s" % (c, x))
    row = fc["row"]
    ok((row["N"], row["F"], row["D"], row["I"]) == (913, world.F_FWD, world.D_FWD, world.I_FWD), "forward book")
    for c in range(5):
        want = {g.gid: g.kind[c] for g in w.groups.values() if g.flag.get(c) and w.active(g, world.COHORTS[c])
                and not w.on_list(g, world.COHORTS[c])}
        got = {g: v["kind"] for g, v in tab[c]["det"].items()}
        ok(want == got, "flags and their kinds in the pack match the design, cohort %d" % c)
    m = fc["measures"]
    ok((m["D"], m["D_R"], m["I"], m["I_R"], m["U"], m["U_R"]) == (240, 120, 176, 11, 3092, 50), "pooled counts")
    # colour and covenant carry nothing beyond the kind: pooled over the cohorts, exact
    ok(m["D_RED_R"] * m["D"] == m["D_RED"] * m["D_R"] and m["I_RED_R"] * m["I"] == m["I_RED"] * m["I_R"],
       "within each kind RED and AMBER flags reach the list at the kind's rate exactly")
    ok(m["D_COV_R"] * m["D"] == m["D_COV"] * m["D_R"], "kind D flags with and without a covenant trigger alike")
    ok(m["COV"] == m["D_COV"], "covenant triggers only on customers")
    ok((row["D_RED"], row["I_RED"], row["D_COV"]) == (world.RED_FWD[0], world.RED_FWD[1], world.COV_FWD),
       "forward colour and covenant mix as planned")

    # ------------------------------------------------------------ the analyst test, executed on the clean truth
    easy, decisive = clean_truth()
    ok(round(easy) == EASY and round(decisive) == CALL, "clean truth: easy route %.2f, decisive step %.2f"
       % (easy, decisive))
    test = fc["test"]
    ok(round(test["hit_and_miss"][2]) == EASY and abs(test["hit_and_miss"][2] - easy) < 1e-9,
       "the pack's easy route files %d (%.2f)" % (EASY, test["hit_and_miss"][2]))
    call = fc["total"]
    ok(round(call) == CALL and abs(call - decisive) < 1e-9 and margin(call, 1) > 0.45, "call %d (%.3f)" % (CALL, call))
    Gnd = solve.golden(nd)
    ok(Gnd["call"] == CALL and round(Gnd["fc"]["test"]["hit_and_miss"][2]) == EASY,
       "the analyst test holds on the build without devices")

    # ------------------------------------------------------------ the family that takes the decisive step converges
    fam = {k: test[k][2] for k in ("split", "split_mean", "split_colour", "split_covenant", "direct_vs_rest",
                                   "split_trended")}
    for wnd in solve.WINDOWS:
        fam["window " + wnd] = solve.forecast(tab, window=wnd)["total"]
    for k, v in fam.items():
        ok(round(v) == CALL and margin(v, 1) >= 0.12, "SF3, SF4, SF5: %s files %d (%.3f)" % (k, CALL, v))
    ok(max(fam.values()) - min(fam.values()) < 0.45, "family spread under half a group")
    # the family that skips it lands elsewhere
    skip = {k: test[k][2] for k in test if k not in fam}
    for k, v in skip.items():
        ok(abs(v / call - 1) >= 0.15, "basis %s at least 15 per cent from the answer (%.2f)" % (k, v))
    ok(min(skip.values()) < 45 and max(skip.values()) > 130, "the skipping family spreads from %.1f to %.1f"
       % (min(skip.values()), max(skip.values())))
    # the out-of-sample record: each closed cohort predicted from the other three
    for k in ("split", "split_colour", "split_covenant", "split_mean"):
        ok(test[k][1] < 0.041, "%s misses no closed cohort by 4.1 per cent or more (%.4f)" % (k, test[k][1]))
    for k in skip:
        ok(test[k][1] >= 0.08, "skipping basis %s misses a closed cohort by 8 per cent or more (%.4f)" % (k, test[k][1]))
    ok(abs(test["split"][1] - 0.0392) < 0.0005 and abs(test["hit_and_miss"][1] - 0.1442) < 0.0005,
       "split 3.9 per cent, one flagged rate 14.4 per cent")
    ok(test["capture_false_alarm"][1] > 0.8, "the error-rate basis misses a closed cohort by more than 80 per cent")
    ok(round(test["direct_vs_rest"][2]) == CALL and abs(test["direct_vs_rest"][1] - 0.0477) < 0.0005
       and test["direct_vs_rest"][1] > test["split"][1] + 0.008,
       "SF9: the two-way split files %d and misses by 4.77 per cent, the three-way by 3.92" % CALL)
    # the mix the decisive step reads: customer-raised share of the flags
    shares = [x["D"] / x["F"] for x in cc]
    ok(max(shares) < 0.70 < row["D"] / row["F"], "this September's flags sit on customers far more than any cohort's")
    sh = [x["F"] / x["N"] for x in cc]
    ok(sorted(range(4), key=lambda i: sh[i]) != sorted(range(4), key=lambda i: shares[i]),
       "the flagged share does not track the customer-raised share across the cohorts")
    # SF2: the customer test read other ways (constructions the field reference refuses) moves the call
    for kw, label in ((dict(borrower="active"), "customers ACTIVE at the extract date only"),
                      (dict(borrower="facility"), "obligors on the 30 Sep 2026 extract only")):
        t2 = pk.cohort_table(**kw)
        v = solve.forecast(t2)["total"]
        ok(round(v) != CALL, "SF2: %s files %.2f, not %d" % (label, v, CALL))
    # SF1: 2.2's ultimate-parent clause read without the apex moves nothing (no flag sits on an unbooked apex)
    only = solve.check_membership(G, target)
    ok(only == [0] * 5, "SF1: no apex-only flag in any cohort")

    # ------------------------------------------------------------ bands, bins, fairness
    bt = G["bands"]
    ok([r["groups"] for r in bt] == world.BAND_N and [r["direct"] for r in bt] == world.BAND_D and
       [r["indirect"] for r in bt] == world.BAND_I, "band plan")
    n2, d2, i2 = world.band_plan()
    ok((n2, d2, i2) == (world.BAND_N, world.BAND_D, world.BAND_I), "band_plan() reproduces the fixed plan")
    fcm = solve.forecast(tab, "split_mean")
    for r, q in zip(bt, solve.band_table(tab, fcm, G["exp"])):
        ok(margin(r["exp_arrivals"]) >= 0.4 and r1(r["exp_arrivals"]) == r1(q["exp_arrivals"]),
           "SF4: %s arrivals mid-bin and the mean of cohort rates in the same bin" % r["band"])
        for k in ("committed", "exp_exposure"):
            ok(margin(r[k] / 1e6) >= 0.25, "%s %s mid-bin (%.3f)" % (r["band"], k, r[k] / 1e6))
    tot_com = sum(r["committed"] for r in bt) / 1e6
    tot_exp = sum(r["exp_exposure"] for r in bt) / 1e6
    ok(margin(tot_com) >= 0.25 and margin(tot_exp) >= 0.25, "exposure totals mid-bin")
    ok(abs(sum(r["exp_arrivals"] for r in bt) - call) < 1e-9, "bands tie to the call")
    for col in ("committed", "exp_arrivals", "exp_exposure"):
        sc = 1e6 if col in ("committed", "exp_exposure") else 1
        ok(abs(sum(r1(r[col] / sc) for r in bt) - r1(sum(r[col] for r in bt) / sc)) < 1e-6,
           "rounded %s rows tie to the rounded total" % col)
    in_force_groups = {g for g, v in G["exp"].items() if v > 0}
    for g in tab[4]["M"]:
        e = G["exp"].get(g, 0.0)
        ok(world.edge_dist(e) >= 0.25e6, "group %s clear of band edges" % g)
        ok(g in in_force_groups, "group %s has a facility in force" % g)
    wE = world.exposure(w)
    for g in tab[4]["M"]:
        ok(abs(wE.get(g, 0.0) - G["exp"].get(g, 0.0)) < 1e-3, "fairness: pack reproduces world exposure of %s" % g)
    golden_figs = band_figures(bt)

    # ------------------------------------------------------------ devices, alone
    readings = dict(A1=dict(grain="rows"), A2f=dict(grain="fid"), A2l=dict(grain="fid", order="last"),
                    A3f=dict(grain="bkfid"), A3l=dict(grain="bkfid", order="last"), B1=dict(clock="B1"),
                    B2=dict(clock="B2"), B3=dict(clock="B3"), B0=dict(clock="B0"), HZ=dict(hz=False),
                    C1=dict(member="booked"), C2=dict(member="gleif"), Dk=dict(dup="keep"), Dt=dict(dup="terms"),
                    Du=dict(dup="undrawn"))
    moved, totals = {}, {}
    for name, kw in readings.items():
        e2 = solve.exposures(pk, **kw)
        bt2 = solve.band_table(tab, fc, e2)
        f2 = band_figures(bt2)
        moved[name] = n_moved(golden_figs, f2)
        totals[name] = sum(r["committed"] for r in bt2) / 1e6
        if name in ("Dk", "Dt", "Du", "C1", "A1", "B2"):
            ok(moved[name] == 25, "%s moves all 25 band figures (%d)" % (name, moved[name]))
            ok(r1(sum(r["exp_exposure"] for r in bt2) / 1e6) != r1(tot_exp), "%s moves the arriving total" % name)
        else:
            ok(moved[name] >= 12, "%s moves at least 12 of the 25 (%d)" % (name, moved[name]))
        ok(abs(totals[name] - tot_com) >= 5, "%s moves the committed total by GBP 5m or more (%.1f)"
           % (name, totals[name] - tot_com))
    for k in ("A2f", "A3f", "B0", "C2", "Dt", "Du"):
        ok(totals[k] < tot_com, "over-cleaner %s lands below the golden" % k)
    ok(len({round(totals[k], 1) for k in ("A2f", "A3f", "B0", "C2", "Dt", "Du")}) == 6,
       "over-cleaners land on their own values")
    ok(totals["Dk"] > tot_com, "counting every facility number once lands above the golden")
    # DV-D: the facilities booked twice, beside genuine twin tranches; only the limit history tells them apart
    copies = [f for f in w.facilities if f.copy_of is not None]
    twins = [f for f in w.facilities if "TWB" in f.dev]
    ok(len(copies) == 22 and len(twins) == 22, "22 copies and 22 second tranches (%d, %d)" % (len(copies), len(twins)))
    ok(len(w.movers["R"]) == 12 and len(w.movers["TW"]) == 12, "twelve movers each way")
    drawn = defaultdict(float)
    for r in pk.fac:
        drawn[(r["booking_entity"], r["facility_id"])] += float(r["drawn_balance"])
    twice = solve.booked_twice(pk)
    ok(twice == {(f.booking, f.fid) for f in copies}, "the right reading drops exactly the copies")
    for f in copies:
        o = f.copy_of
        ok(pk.versions[(f.booking, f.fid)] == pk.versions[(o.booking, o.fid)] and drawn[(f.booking, f.fid)] == 0,
           "SF8: copy %s repeats %s's history stamp for stamp and is undrawn" % (f.fid, o.fid))
        ok(int(f.fid) == int(o.fid) + 1, "copy %s takes the next number after %s" % (f.fid, o.fid))
    near = defaultdict(list)
    terms = {}
    for r in pk.fac:
        k = (r["booking_entity"], r["facility_id"])
        terms.setdefault(k, [r["booking_entity"], set(), r["product"], r["currency"], r["committed_limit"],
                             r["start_date"], r["final_maturity_date"], r["facility_status"]])[1].add(r["customer_id"])
    for k, t in terms.items():
        near[(t[0], frozenset(t[1])) + tuple(t[2:])].append(k)
    genuine = [ks for ks in near.values() if len(ks) > 1 and not set(ks) & twice]
    ok(len(genuine) >= 22, "genuine near-duplicate pairs beside the copies (%d)" % len(genuine))
    for ks in genuine:
        ok(len({tuple(pk.versions[k]) for k in ks}) == len(ks), "SF8: genuine pair %s keyed apart" % (ks,))
    ok(sum(1 for f in twins if drawn[(f.booking, f.fid)] == 0) >= 12, "most second tranches undrawn")
    # the device cannot move the call: exposure never enters the forecast
    ok(round(solve.forecast(tab)["total"]) == CALL, "no exposure reading moves the call")
    # SF6: a company booked to one group and consolidated into another's ultimate parent is a member of both (2.2)
    cg = solve.customer_groups(pk)
    two = [c for c, gs in cg.items() if len(gs) == 2]
    jv = [e for e in w.ents.values() if e.booked]
    ok(len(two) == len(jv) == 21 and all(len(cg[e.cust]) == 2 for e in jv), "SF6: 21 two-group customers")
    for e in jv:
        ok(e.inert and all(r[2] == "GREEN" for r in w.signals if r[1] is e and r[0] in world.COHORTS),
           "SF6: the two-group customer %s is green at every cohort date" % e.cust)

    # ------------------------------------------------------------ device grid
    A = dict(right={}, A1=dict(grain="rows"), A2f=dict(grain="fid"), A3f=dict(grain="bkfid"))
    Bd = dict(right={}, B0=dict(clock="B0"), B1=dict(clock="B1"), B2=dict(clock="B2"), B3=dict(clock="B3"))
    H = dict(right={}, drop=dict(hz=False))
    C = dict(right={}, C1=dict(member="booked"), C2=dict(member="gleif"))
    Dd = dict(right={}, Dk=dict(dup="keep"), Dt=dict(dup="terms"), Du=dict(dup="undrawn"))
    cells, nearest = 0, (float("inf"), "")
    for (ak, av), (bk, bv), (hk, hv), (ck, cv), (dk, dv) in itertools.product(A.items(), Bd.items(), H.items(),
                                                                            C.items(), Dd.items()):
        if ak == bk == hk == ck == dk == "right":
            continue
        kw = dict(av, **bv, **hv, **cv, **dv)
        bt2 = solve.band_table(tab, fc, solve.exposures(pk, **kw))
        f2 = band_figures(bt2)
        cell = "%s/%s/%s/%s/%s" % (ak, bk, hk, ck, dk)
        ok(n_moved(golden_figs, f2) >= 12, "grid cell %s misses at least 12 band figures (%d)"
           % (cell, n_moved(golden_figs, f2)))
        move = abs(sum(r["committed"] for r in bt2) / 1e6 - tot_com)
        ok(move >= 3, "grid cell %s moves the committed total by GBP 3m or more" % cell)
        nearest = min(nearest, (move, cell))
        cells += 1
    ok(cells == 479, "479 grid cells")
    print("nearest grid cell: %s moves the committed total by GBP %.2fm" % (nearest[1], nearest[0]))
    # the measured pair ceiling on the cut pack (supplemental-stumping Part 0's weights)
    import cracker
    pair, leak = cracker.main(target)
    ok(pair <= 40 and leak < 35, "pair ceiling %.1f, mirror leakage %.1f" % (pair, leak))

    # ------------------------------------------------------------ hygiene battery on every wrong path
    keys = [(r["booking_entity"], r["facility_id"], r["customer_id"]) for r in pk.fac]
    ok(len(keys) == len(set(keys)), "extract unique at booking entity, facility and customer")
    custs = {r["customer_id"] for r in pk.obl}
    ok(len(custs) == len(pk.obl), "obligor master unique on customer")
    ok(all(r["customer_id"] in custs for r in pk.fac), "every extract customer joins the master")
    fkeys = {(r["booking_entity"], r["facility_id"]) for r in pk.fac}
    ok(set(pk.hist) == fkeys, "the limit history joins the extract on booking entity and number")
    for k, h in pk.hist.items():
        ok(len({t for t, _ in h}) == len(h), "one version per stamp, %s" % (k,))
    for r in pk.fac:
        v = solve.limit_on_clock(pk, (r["booking_entity"], r["facility_id"]), 0.0, "right")
        h = [val for t, val in pk.hist[(r["booking_entity"], r["facility_id"])] if t <= dt.datetime(2026, 10, 1, 0, 15)]
        want = h[-1] if (h and r["facility_status"] == "ACTIVE") else 0.0
        ok(abs(float(r["committed_limit"]) - want) < 0.005, "control: extract limit is the history at the run, %s"
           % r["facility_id"])
        if r["facility_status"] != "ACTIVE" and solve.d(r["final_maturity_date"]) > dt.date(2026, 9, 30):
            ok(v == 0.0, "cancelled or closed facility in date has a nil limit in force, %s" % r["facility_id"])
    plc = {r["facility_id"] for r in pk.fac if r["booking_entity"] == "HB-PLC"}
    dac = {r["facility_id"] for r in pk.fac if r["booking_entity"] == "HB-DAC"}
    ok(30 <= len(plc & dac) <= 55, "about 40 coinciding ledger numbers (%d)" % len(plc & dac))
    multi = {}
    for r in pk.fac:
        multi.setdefault((r["booking_entity"], r["facility_id"]), []).append(r["customer_id"])
    nm = sum(1 for v in multi.values() if len(v) > 1)
    ok(0.09 <= nm / len(multi) <= 0.15 and max(len(v) for v in multi.values()) <= 4, "multi-obligor share %d" % nm)
    stamps = [t for h in pk.hist.values() for t, _ in h]
    ok(sum(1 for t in stamps if t.minute == 30 and t.second == 0 and t.hour == 23) > 200 and
       sum(1 for t in stamps if t.minute == 30 and t.second == 0 and t.hour == 0) > 100,
       "the batch stamps 23:30Z in BST months and 00:30Z in GMT months")
    n_1oct = sum(1 for t in stamps if t == world.SOD_1OCT)
    ok(70 <= n_1oct <= 120, "1 October batch versions (%d)" % n_1oct)
    blank = [r for r in pk.obl if not r["group_id"]]
    ok(len(blank) == 14 and all(r["primary_booking_entity"] == "HB-DAC" and r["customer_since"] >= "2026-09-01"
                                for r in blank), "fourteen September HB-DAC customers not yet grouped")
    cg = solve.customer_groups(pk)
    ok(all(cg[r["customer_id"]] & tab[4]["M"] for r in blank), "each reaches a monitored group through GLEIF")

    # ------------------------------------------------------------ zero-counts: devices outside the main call
    sept = set(solve.COHORTS)
    flagged_keys = set()
    with open(os.path.join(target, make.FILES["signals"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["publication_date"] in sept and r["signal"] != "GREEN":
                flagged_keys.add(r["entity_key"].upper())
    hz_leis = {r["lei"] for r in blank}
    jv_leis = {e.lei for e in w.ents.values() if e.booked}
    parents = {}
    for r in pk.rr:
        parents.setdefault(r["Relationship.StartNode.NodeID"], set()).add(r["Relationship.EndNode.NodeID"])
    pop = set(flagged_keys)
    frontier = set(flagged_keys)
    while frontier:
        nxt = set()
        for k in frontier:
            nxt |= parents.get(k, set()) - pop
        pop |= nxt
        frontier = nxt
    ok(not (hz_leis & pop) and not (jv_leis & pop), "zero device rows inside the main call's population (%d, %d)"
       % (len(hz_leis & pop), len(jv_leis & pop)))
    with open(os.path.join(target, make.FILES["signals"]), encoding="utf-8") as fh:
        hz_signal = sum(1 for r in csv.DictReader(fh) if r["entity_key"].upper() in hz_leis)
    ok(hz_signal == 0, "no publication row for a not-yet-grouped customer")
    for fname in (make.FILES["register"], make.FILES["watchlist"]):
        ok(filecmp.cmp(os.path.join(a, fname), os.path.join(nd, fname), shallow=False),
           "no device writes a row of " + fname)

    def sept_rows(t):
        with open(os.path.join(t, make.FILES["signals"]), encoding="utf-8") as fh:
            rows_ = [ln for ln in fh if ln[:10] in sept]
        jv_keys = {k for k in jv_leis}
        return [ln for ln in rows_ if ln.split(",")[1].upper() not in jv_keys]
    ok(sept_rows(a) == sept_rows(nd), "no device writes a September-publication row the call reads")
    ok(Gnd["fc"]["test"] == fc["test"] and Gnd["call"] == CALL, "the call and the record are the same without devices")

    # ------------------------------------------------------------ inert texture on the main path
    for kw in (dict(keep_lapsed=False), dict(case_fold=False), dict(follow_funds=True), dict(branches=False),
               dict(successors=False), dict(follow_direct=False), dict(apex=False)):
        t2 = pk.cohort_table(**kw)
        for c in range(5):
            ok(t2[c]["det"] == tab[c]["det"], "SF7: texture %s inert at cohort %d" % (kw, c))

    # ------------------------------------------------------------ realism repairs
    red = {}
    for r in pk.signals:
        if r["signal"] == "RED":
            red[r["publication_date"]] = red.get(r["publication_date"], 0) + 1
    for y in (2023, 2024, 2025):
        s, a_, o = red["%d-09-30" % y], red["%d-08-31" % y], red["%d-10-31" % y]
        ok(abs(s / ((a_ + o) / 2) - 1) <= 0.15, "RED in September %d within 15 per cent of its neighbours" % y)
    ok(abs(red["2026-09-30"] / red["2026-08-31"] - 1) <= 0.25 and abs(red["2022-09-30"] / red["2022-10-31"] - 1) <= 0.25,
       "RED at the series ends in line with the next month")
    with open(os.path.join(target, make.FILES["facilities"]), encoding="utf-8") as fh:
        frows = list(csv.DictReader(fh))
    ok(frows == sorted(frows, key=lambda r: (r["booking_entity"], r["facility_id"], r["customer_id"])),
       "extract sorted by booking entity, facility number and customer")
    # the customers not yet grouped are September customers by the field reference (group_id blank until the
    # monthly grouping review), so their facilities are the newest HB-DAC numbers wherever the run falls
    hz_fac = [f for f in w.facilities if "HZ" in f.dev]
    ok(all(f.booking == "HB-DAC" and f.booked >= dt.date(2026, 9, 1) for f in hz_fac),
       "every facility of a customer not yet grouped is a September HB-DAC booking")
    dev_fac = set()
    for f in w.facilities:
        if f.dev - {"A1", "HZ"} or (f.dev & {"A1"} and any(w.ents[e].gid in w.used_groups for e in f.obligors)):
            dev_fac.add((f.booking, f.fid))
    seq = []
    for r in frows:
        k = (r["booking_entity"], r["facility_id"])
        if not seq or seq[-1][0] != k:
            seq.append((k, k in dev_fac))
    run = longest = 0
    for _, isdev in seq:
        run = run + 1 if isdev else 0
        longest = max(longest, run)
    ok(longest <= 3, "no run of more than three consecutive device facilities (%d)" % longest)
    pos = [i / len(frows) for i, r in enumerate(frows) if (r["booking_entity"], r["facility_id"]) in dev_fac]
    ok(0.40 <= sum(pos) / len(pos) <= 0.60, "device rows' mean position %.2f" % (sum(pos) / len(pos)))
    mat = [r for r in frows if r["final_maturity_date"] == "2026-09-30"]
    ok(mat and all(r["facility_status"] == "CLOSED" and float(r["committed_limit"]) == 0 for r in mat),
       "facilities maturing on 30 September show CLOSED with a nil limit")
    ok(not any(r["facility_status"] == "ACTIVE" for r in frows[-25:]) or
       len({r["final_maturity_date"] for r in frows[-25:]}) > 5, "the last rows are not one kind of facility")
    # containers
    created = {}
    for f in sorted(os.listdir(target)):
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                meta = z.read("docProps/core.xml") + z.read("docProps/app.xml")
                ok(not re.search(rb"openpyxl|python-docx|reportlab", meta, re.I), "no library signature in " + f)
                ok(b"<Company>Halstow Bank plc</Company>" in meta, "company in " + f)
                if f.endswith(".xlsx"):
                    ok(b"HeadingPairs" in meta and b"TitlesOfParts" in meta and b"16.0300" in meta, "full app.xml in " + f)
                else:
                    ok(b"Normal.dotm" in meta and b"16.0000" in meta and b"<cp:revision>4" in meta, "Word app.xml " + f)
                    ok("word/document.xml" in z.namelist() and "docProps/custom.xml" not in z.namelist(), "docx parts")
                    doc = z.read("word/document.xml")
                    ok(b"w:rsidR" in doc, "Word rsids in " + f)
                c_ = re.search(rb"<dcterms:created[^>]*>([^<]+)<", meta).group(1)
                created[f] = c_
    ok(len(set(created.values())) == len(created), "no two input containers share a created stamp")
    import pypdf
    std = "".join(pg.extract_text() for pg in pypdf.PdfReader(os.path.join(target, make.FILES["standard"])).pages)
    std_flat = " ".join(std.split())
    for word in ("lapsed", "branch", "fund-management", "successor", "capture and false-alarm", "inversion",
                 "base rate", "joint venture", "not lend", "borrowing member", "non-borrowing", "contagion"):
        ok(word not in std_flat.lower(), "the standard names no edge case or basis: " + word)
    ok("UK time (GMT or BST" in std_flat and "set against its cohort's actual arrivals" in std_flat, "5.2 and 1.3 as filed")
    for phrase in ("predicts those cohorts best", "smallest error", "same across the book", "depends only on whether",
                   "the other three", "probability of reaching", "set from the last four", "flag status, shared",
                   "in proportion to the band"):
        ok(phrase not in std_flat, "the standard files no model, fitting window or selection rule: " + phrase)
    ok("members are its ultimate parent, the customers the credit system books to it" in std_flat, "2.2 as amended")

    # ------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    nrows = sum(1 for _ in open(os.path.join(target, make.FILES["signals"]), encoding="utf-8")) - 1
    ok(nrows >= 25000, "spine has 25,000 or more rows")
    ok(len(make.DISTRACTORS) >= 2, "two or more distractors")
    tmp2 = tempfile.mkdtemp()
    for f in files:
        ok(f in files, f)
        if f not in make.DISTRACTORS:
            shutil.copy(os.path.join(target, f), tmp2)
    G2 = solve.golden(tmp2)
    ok(G2["call"] == CALL and band_figures(G2["bands"]) == golden_figs, "golden unchanged with the distractors deleted")
    # the distractors read as forecasts land elsewhere: the rating master scale's PD midpoints summed over the book
    wb = __import__("openpyxl").load_workbook(os.path.join(target, make.FILES["ratings"]), read_only=True)
    mid = {r[0]: r[4] for r in wb["Master scale"].iter_rows(min_row=4, values_only=True) if r and r[0]}
    gr = {r[0]: r[1] for r in wb["Group ratings 30-09-2026"].iter_rows(min_row=2, values_only=True) if r and r[0]}
    pd_sum = sum(mid[gr[g]] for g in tab[4]["M"] if g in gr)
    ok(abs(pd_sum / call - 1) >= 0.15, "the rating scale's PDs summed over the book land elsewhere (%.1f)" % pd_sum)
    for f in files:
        ok("distractor" not in f.lower(), "no file named for its role")
        if f.endswith((".csv", ".md", ".txt")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok("\u2014" not in txt and "distractor" not in txt.lower(), "no em dash or role word in " + f)
            ok("golden copy" not in txt.lower(), "no 'golden copy' in " + f)
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(tmp2, ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(tmp2, ignore_errors=True)
    goldens_and_writeup()
    return w, G, fam, skip, moved, totals, tot_com


def goldens_and_writeup():
    """The goldens rebuild byte-identically and match the shipped copies; the write-up is the one writeup.py
    emits; every number in it is owed by a figure, a citation or a date."""
    import deliver
    import writeup
    F = deliver.figures()
    gold = os.path.join(HERE, "..", "golden")
    builds = []
    for _ in range(2):
        d = tempfile.mkdtemp()
        deliver.workbook(F, os.path.join(d, deliver.XLSX))
        deliver.chart(F, os.path.join(d, deliver.CHART))
        builds.append(d)
    for f in (deliver.XLSX, deliver.CHART):
        a, b = (open(os.path.join(d, f), "rb").read() for d in builds)
        ok(a == b, "golden rebuilds byte-identical: " + f)
        ok(a == open(os.path.join(gold, f), "rb").read(), "shipped golden is the current build: " + f)
    for d in builds:
        shutil.rmtree(d, ignore_errors=True)
    ok(sorted(os.listdir(gold)) == sorted([deliver.XLSX, deliver.CHART]), "golden holds exactly the two deliverables")
    deliver.verify(F)
    ok(F["call"] == CALL and r1(F["expected"]) == 78.0, "call and expected arrivals")
    with zipfile.ZipFile(os.path.join(gold, deliver.XLSX)) as z:
        meta = z.read("docProps/core.xml") + z.read("docProps/app.xml")
    ok(b"Jill Berry" in meta and b"HeadingPairs" in meta and b"openpyxl" not in meta, "golden workbook container")
    sub = open(os.path.join(HERE, "..", "submission.md"), encoding="utf-8").read()
    ok(sub == writeup.build(F), "submission.md is the current writeup.py output")
    body = re.sub(r"[A-Za-z0-9_\-]+\.(csv|xlsx|txt|pdf|docx|md|png|svg)", " ", sub)
    body = body.replace("task446", " ")
    body = re.sub(r"(?m)^(\s*)(?:##\s*)?\d+\.\s", r"\1", body)
    m = F["measures"]
    owed = {str(F["call"]), str(F["N1"]), str(F["F1"]), str(F["D1"]), "%.1f" % F["expected"],
            "%.1f%%" % (F["p_d"] * 100), "%.2f%%" % (F["p_i"] * 100), "%.2f%%" % (F["p_unflag"] * 100),
            "%.1f%%" % (F["split"][1] * 100), "%.1f%%" % (F["single"][1] * 100), str(m["D"]), str(m["D_R"]),
            str(m["I"]), str(m["I_R"]), "{:,}".format(m["U"]), str(m["U_R"]), str(F["twice"])}
    for row in F["rows"] + [F["total"]]:
        owed |= {"%.1f" % row["arrivals"], "£{:,.1f}m".format(row["exposure"]), "£{:,.1f}m".format(row["committed"]),
                 "{:,}".format(row["groups"]), str(row["flagged"])}
    for band in deliver.BANDS:
        owed |= set(re.findall(r"£\d+m", band))
    cites = {"1.3", "2.2", "3.2", "4.1", "4.2", "4.3", "5.2", "5.3", "6.1", "6.2", "07"}
    dates = {"30", "2022", "2025", "2026", "2027"}
    tokens = re.findall(r"£[\d,]+(?:\.\d+)?m|\d[\d,]*(?:[.:/]\d+)?%?", body)
    tokens = [t.rstrip(",") for t in tokens]
    stray = [t for t in tokens if t not in owed | cites | dates]
    ok(not stray, "every number in submission.md is owed: %s" % stray)
    for t in owed:
        ok(t in body, "owed figure stated in submission.md: " + t)
    for x, step in ((F["p_unflag"], 0.01), (F["split"][1], 0.1), (F["single"][1], 0.1)):
        ok(margin(x * 100, step) >= 0.15, "percentage %.4f clear of its rounding edge" % (x * 100))


if __name__ == "__main__":
    w, G, fam, skip, moved, totals, tot_com = main()
    print("assertions passed:", N_ASSERT)
    print("family that takes the decisive step:", {k: round(float(v), 2) for k, v in fam.items()})
    print("family that skips it:", {k: round(float(v), 2) for k, v in sorted(skip.items(), key=lambda kv: kv[1])})
    print("band figures moved:", moved)
    print("committed total moves (GBP m):", {k: round(v - tot_com, 1) for k, v in totals.items()})
    print("movers planted:", {k: len(v) for k, v in w.movers.items()}, "tuning steps", w.tune_steps)
