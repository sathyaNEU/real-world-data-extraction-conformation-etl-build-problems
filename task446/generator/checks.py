"""Assertions for task446 (architecture 2, loop 1). Builds the pack twice, runs the independent solver on it
and checks the literal reading (5.2 files the estimand only; the back-test over the family of bases is the
design's, never filed), the ladder, the convergence of the
golden's variants, the bins, the ask devices and their grid, the separation of the main call from every
device, the inert texture on the main path, the realism repairs and the input gates.

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

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world      # noqa: E402
import solve      # noqa: E402
import make       # noqa: E402

N_ASSERT = 0
CALL = 133


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
        out += [r["groups"], r1(r["committed"] / 1e6), r1(r["exp_flagged"]), r1(r["exp_unflagged"]),
                r1(r["exp_exposure"] / 1e6)]
    return out


def n_moved(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


# design table, the out-of-sample back-test (each closed cohort from the other three; never filed): worst miss
# (per cent) and forward figure for each basis
DESIGN_TEST = {
    "hit_and_miss": (40.60, 72.92), "one_share": (55.58, 52.31), "arrivals_per_flagged": (35.64, 79.72),
    "every_flagged_reaches": (198.44, 175.64), "capture_false_alarm": (1.57, 133.04),
    "mean_capture_false_alarm": (2.03, 132.97), "share_on_flagged_share": (2.00, 132.83),
    "share_on_flagged_share_weighted": (2.00, 132.83), "arrivals_on_flagged_and_book": (2.01, 132.84),
    "hit_and_miss_trended": (7.97, 146.72), "mean_hit_and_miss": (39.60, 71.99),
    "latest_hit_and_miss": (30.78, 69.37), "most_stressed_hit_and_miss": (80.19, 97.91),
}
TAKEN_TOGETHER = {"hit_and_miss", "one_share", "arrivals_per_flagged", "every_flagged_reaches", "capture_false_alarm"}


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

    # ------------------------------------------------------------ cohorts as designed
    for c in range(4):
        ok(len(tab[c]["M"]) == world.N_TARGET[c], "cohort %d size" % c)
        ok(len(tab[c]["R"]) == world.P_REACH[c], "cohort %d reaching" % c)
        ok(len(tab[c]["R"] & tab[c]["F"]) == world.TP_FLAG[c], "cohort %d flagged and reaching" % c)
        ok(len(tab[c]["F"] - tab[c]["R"]) == world.FP_FLAG[c], "cohort %d flagged not reaching" % c)
    ok(len(tab[4]["M"]) == world.N_TARGET[4] and len(tab[4]["F"]) == world.F_FWD, "forward book 913 / 165")
    for c in range(5):
        want = {g.gid for g in w.groups.values() if g.flag.get(c) and w.active(g, world.COHORTS[c])
                and not w.on_list(g, world.COHORTS[c])}
        ok(want == tab[c]["F"], "flags in the pack match the design, cohort %d" % c)
    m = fc["measures"]
    ok(m["TP"] == 157 and m["P"] == 201 and m["FP"] == 259 and m["N"] - m["P"] == 3307, "pooled counts")

    # ------------------------------------------------------------ the data forces the basis: back-test over the family
    test = fc["test"]
    ok(len(test) == 13, "thirteen bases swept")
    for k, (err, fw) in DESIGN_TEST.items():
        ok(abs(test[k][1] * 100 - err) < 0.01 and abs(test[k][2] - fw) < 0.01,
           "basis %s as designed (%.2f, %.2f)" % (k, test[k][1] * 100, test[k][2]))
    ranked = sorted(test, key=lambda k: test[k][1])
    ok(ranked[0] == "capture_false_alarm" and fc["model"] == "capture_false_alarm", "the back-test ranks the golden's basis first")
    ok(test[ranked[1]][1] - test[ranked[0]][1] > 0.004, "unique minimum, margin over the next basis")
    for k in test:
        if k == ranked[0]:
            continue
        if round(test[k][2]) != CALL:
            ok(test[k][1] >= 0.0797, "non-convergent basis %s misses by 7.97 per cent or more" % k)
        if k in TAKEN_TOGETHER:
            ok(test[k][1] >= 0.356, "taken-together basis %s misses by 35.6 per cent or more" % k)
    worst = max(abs(x) for x in test["capture_false_alarm"][0])
    ok(abs(worst - 0.0157) < 0.0005, "answer's worst miss 1.6 per cent")
    ok(abs(test["hit_and_miss"][0][2] - 0.406) < 0.0005, "hit and miss rates miss 2024 by 40.6 per cent")

    # ------------------------------------------------------------ the call and its convergent routes
    call = fc["total"]
    ok(round(call) == CALL and margin(call, 1) > 0.45, "call 133, %.3f" % call)
    conv = [k for k in test if round(test[k][2]) == CALL]
    ok(sorted(conv) == sorted(["capture_false_alarm", "mean_capture_false_alarm", "share_on_flagged_share",
                               "share_on_flagged_share_weighted", "arrivals_on_flagged_and_book"]), "convergent set")
    for k in conv:
        ok(margin(test[k][2], 1) >= 0.33, "route %s mid-bin (%.2f)" % (k, test[k][2]))
    ok(r1(fc["flagged"]) == 103.9 and r1(fc["unflagged"]) == 29.1, "split figures 103.9 / 29.1")
    ok(margin(fc["flagged"]) >= 0.35 and margin(fc["unflagged"]) >= 0.25, "split mid-bin")
    # the mean-of-rates variant lands both totals and every band arrival figure in the golden's bin
    fcm = solve.forecast(tab, "mean_capture_false_alarm")
    ok(r1(fcm["flagged"]) == 103.9 and r1(fcm["unflagged"]) == 29.1, "mean-of-rates variant lands both totals")
    btm = solve.band_table(tab, fcm, G["exp"])
    for r, q in zip(G["bands"], btm):
        ok(r1(r["exp_flagged"]) == r1(q["exp_flagged"]) and r1(r["exp_unflagged"]) == r1(q["exp_unflagged"]),
           "SF7 mean-of-rates variant lands %s arrivals under the 5.3 split" % r["band"])
    # window violations of the answer's own basis
    cc = solve.cohort_counts(tab)
    win = {k: solve.predict(solve.basis_fit("capture_false_alarm", cs), 913, 165)
           for k, cs in dict(latest=cc[3:], last3=cc[1:], first3=cc[:3]).items()}
    ok(abs(win["latest"] - 126.82) < 0.01 and abs(win["last3"] - 132.44) < 0.01 and abs(win["first3"] - 135.01) < 0.01,
       "SF6 window violations of 4.3's last four closed cohorts taken together %s" % {k: round(v, 2) for k, v in win.items()})

    # ------------------------------------------------------------ the ladder
    rungs = dict(R0=test["hit_and_miss"][2], R0b=test["latest_hit_and_miss"][2],
                 R1=test["most_stressed_hit_and_miss"][2], R2=test["hit_and_miss_trended"][2],
                 R3=test["every_flagged_reaches"][2], V_base=test["one_share"][2],
                 V_flagged_only=test["arrivals_per_flagged"][2])
    ok(round(rungs["R0"]) == 73 and round(rungs["R2"]) == 147, "R0 73, R2 147")
    for k, v in rungs.items():
        ok(abs(v / call - 1) >= 0.06, "rung %s at least 6 per cent from the answer (%.2f)" % (k, v))
    nearest = min(rungs.items(), key=lambda kv: abs(kv[1] / call - 1))
    ok(nearest[0] == "R2" and 0.09 < nearest[1] / call - 1 < 0.12, "nearest wrong rung R2 at +10.3 per cent")
    ok(len({round(v) for v in rungs.values()}) == len(rungs), "every rung files a different whole number")
    P, TP, FP = map(np.array, (world.P_REACH, world.TP_FLAG, world.FP_FLAG))
    Ns = np.array(world.N_TARGET[:4])
    fl = TP + FP
    ppv, p = TP / fl, P / Ns
    se_c, f_c = TP / P, FP / (Ns - P)
    ok(ppv[0] > ppv[3] > ppv[1] > ppv[2] and p[0] > p[3] > p[1] > p[2], "hit rate tracks each year's share reaching")
    ok(max(se_c) - min(se_c) < 0.09 and max(f_c) - min(f_c) < 0.004, "capture and false-alarm rates hold")
    ok(abs(F1_PPV(world) - rungs["R0"]) < 1e-9, "R0 reproduces from the world counts")

    # ------------------------------------------------------------ bands, bins, fairness
    bt = G["bands"]
    ok([r["groups"] for r in bt] == world.BAND_N and [r["flagged"] for r in bt] == world.BAND_F, "band plan")
    for r in bt:
        for k, sc in (("exp_flagged", 1), ("exp_unflagged", 1), ("committed", 1e6), ("exp_exposure", 1e6)):
            ok(margin(r[k] / sc) >= 0.25, "%s %s mid-bin (%.3f)" % (r["band"], k, r[k] / sc))
    tot_com = sum(r["committed"] for r in bt) / 1e6
    tot_exp = sum(r["exp_exposure"] for r in bt) / 1e6
    ok(margin(tot_com) >= 0.25 and margin(tot_exp) >= 0.25, "exposure totals mid-bin")
    ok(abs(sum(r["exp_total"] for r in bt) - call) < 1e-9, "bands tie to the call")
    for col in ("committed", "exp_flagged", "exp_unflagged", "exp_exposure"):
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
                    B2=dict(clock="B2"), B3=dict(clock="B3"), B0=dict(clock="B0"), HZ=dict(hz=False))
    moved, totals = {}, {}
    for name, kw in readings.items():
        e2 = solve.exposures(pk, **kw)
        bt2 = solve.band_table(tab, fc, e2)
        f2 = band_figures(bt2)
        moved[name] = n_moved(golden_figs, f2)
        totals[name] = sum(r["committed"] for r in bt2) / 1e6
        if name in ("A1", "B2"):
            ok(moved[name] == 25, "%s moves all 25 band figures (%d)" % (name, moved[name]))
            ok(r1(sum(r["exp_exposure"] for r in bt2) / 1e6) != r1(tot_exp), "%s moves the arriving total" % name)
        else:
            ok(moved[name] >= 15, "%s moves at least 15 of the 25 (%d)" % (name, moved[name]))
        ok(abs(totals[name] - tot_com) >= 5, "%s moves the committed total by GBP 5m or more (%.1f)"
           % (name, totals[name] - tot_com))
        ok(round(solve.forecast(tab)["total"]) == CALL, "%s cannot move the call" % name)
    for k in ("A2f", "A3f", "B0"):
        ok(totals[k] < tot_com, "over-cleaner %s lands below the golden" % k)
    ok(len({round(totals[k], 1) for k in ("A2f", "A3f", "B0")}) == 3, "over-cleaners land on their own values")
    # single-device crossings as designed (A1 and B2: every band's flagged count by one or more, unflagged by three)
    base_counts = [(r["flagged"], r["groups"] - r["flagged"]) for r in bt]
    for name in ("A1", "B2"):
        bt2 = solve.band_table(tab, fc, solve.exposures(pk, **readings[name]))
        for r, (f0, u0) in zip(bt2, base_counts):
            ok(abs(r["flagged"] - f0) >= 1 and abs(r["groups"] - r["flagged"] - u0) >= 3,
               "%s moves %s's flagged and unflagged counts" % (name, r["band"]))

    # ------------------------------------------------------------ device grid
    A = dict(right={}, A1=dict(grain="rows"), A2f=dict(grain="fid"), A2l=dict(grain="fid", order="last"),
             A3f=dict(grain="bkfid"), A3l=dict(grain="bkfid", order="last"))
    B = dict(right={}, B0=dict(clock="B0"), B1=dict(clock="B1"), B2=dict(clock="B2"), B3=dict(clock="B3"))
    H = dict(right={}, drop=dict(hz=False))
    cells = 0
    for (ak, av), (bk, bv), (hk, hv) in itertools.product(A.items(), B.items(), H.items()):
        if ak == bk == hk == "right":
            continue
        kw = dict(av, **bv, **hv)
        bt2 = solve.band_table(tab, fc, solve.exposures(pk, **kw))
        f2 = band_figures(bt2)
        ok(n_moved(golden_figs, f2) >= 15, "grid cell %s/%s/%s misses at least 15 band figures (%d)"
           % (ak, bk, hk, n_moved(golden_figs, f2)))
        ok(abs(sum(r["committed"] for r in bt2) / 1e6 - tot_com) >= 5, "grid cell %s/%s/%s moves the committed total"
           % (ak, bk, hk))
        cells += 1
    ok(cells == 59, "59 grid cells")

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
    ok(all(cg[r["customer_id"]] in tab[4]["M"] for r in blank), "each reaches a monitored group through GLEIF")

    # ------------------------------------------------------------ zero-counts: devices outside the main call
    sept = set(solve.COHORTS)
    flagged_keys = set()
    with open(os.path.join(target, make.FILES["signals"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["publication_date"] in sept and r["signal"] != "GREEN":
                flagged_keys.add(r["entity_key"].upper())
    hz_leis = {r["lei"] for r in blank}
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
    inside = hz_leis & pop
    ok(len(inside) == 0, "zero hazard rows inside the main call's population (%d)" % len(inside))
    with open(os.path.join(target, make.FILES["signals"]), encoding="utf-8") as fh:
        hz_signal = sum(1 for r in csv.DictReader(fh) if r["entity_key"].upper() in hz_leis)
    ok(hz_signal == 0, "no publication row for a not-yet-grouped customer")
    for fname in (make.FILES["register"], make.FILES["watchlist"]):
        ok(filecmp.cmp(os.path.join(a, fname), os.path.join(nd, fname), shallow=False),
           "no device writes a row of " + fname)

    def sept_rows(t):
        with open(os.path.join(t, make.FILES["signals"]), encoding="utf-8") as fh:
            return [ln for ln in fh if ln[:10] in sept]
    ok(sept_rows(a) == sept_rows(nd), "no device writes a September-publication row")
    Gnd = solve.golden(nd)
    ok(Gnd["call"] == CALL and Gnd["fc"]["test"] == fc["test"], "the call and the test are the same without devices")

    # ------------------------------------------------------------ inert texture on the main path
    for kw in (dict(keep_lapsed=False), dict(case_fold=False), dict(follow_funds=True), dict(branches=False),
               dict(successors=False), dict(follow_direct=False)):
        t2 = pk.cohort_table(**kw)
        for c in range(5):
            ok(t2[c]["F"] == tab[c]["F"], "texture %s inert at cohort %d" % (kw, c))
    # SF1, SF2, SF3, SF4, SF5 (2.2 membership, design note semantic fork table): the amended clause names the ultimate parent a member; read literally it gives the
    # golden's 165 and every committed band figure. The pre-amendment reading (apex only when booked) is refused
    # by 2.2's own words; it would give 159 and move band arrivals, and leaves the call on 133.
    only = solve.check_membership(G, target)
    ok(only == [6, 5, 3, 5, 6], "apex-only flags counted by cohort %s" % only)
    t_na = pk.cohort_table(apex=False)
    ok(len(t_na[4]["F"]) == 159, "the old 2.2 reading gives 159 flagged")
    fc_na = solve.forecast(t_na)
    ok(round(fc_na["total"]) == CALL, "the call holds under the old reading (%.2f)" % fc_na["total"])
    ok(n_moved(golden_figs, band_figures(solve.band_table(t_na, fc_na, G["exp"]))) >= 5,
       "the old reading moves band arrivals, so the amended clause is load-bearing")
    for kw in (dict(branches=False), dict(follow_direct=False), dict(keep_lapsed=False)):
        ok(pk.cohort_table(apex=True, **kw)[4]["F"] == tab[4]["F"], "apex edge %s inert" % kw)
    ok("members are its ultimate parent, the customers the credit system books to it" in std_flat_22(target),
       "2.2 as amended")
    resolve_obl_only = 0
    for c in range(5):
        date = solve.d(solve.COHORTS[c])
        _, k2g = pk.group_of_key(date)
        ds = date.isoformat()
        F_obl = {k2g[r["entity_key"].upper()] for r in pk.signals if r["publication_date"] == ds and r["signal"] != "GREEN"
                 and r["entity_key"].upper() in k2g} & tab[c]["M"]
        resolve_obl_only += len(tab[c]["F"] - F_obl)
    ok(resolve_obl_only > 0, "groups flagged only through a non-borrowing member exist")

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
    dev_fac = set()
    for f in w.facilities:
        if f.dev - {"A1"} or (f.dev & {"A1"} and any(w.ents[e].gid in w.used_groups for e in f.obligors)):
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
                    ok(b"w:rsidR" in doc, "Word rsids in the agenda")
                c_ = re.search(rb"<dcterms:created[^>]*>([^<]+)<", meta).group(1)
                created[f] = c_
    ok(len(set(created.values())) == len(created), "no two input containers share a created stamp")
    import pypdf
    std = "".join(pg.extract_text() for pg in pypdf.PdfReader(os.path.join(target, make.FILES["standard"])).pages)
    std_flat = " ".join(std.split())
    for word in ("lapsed", "branch", "fund-management", "successor", "capture and false-alarm", "inversion",
                 "base rate"):
        ok(word not in std_flat.lower(), "the standard names no edge case or basis: " + word)
    ok("UK time (GMT or BST" in std_flat and "set against its cohort's actual arrivals" in std_flat, "5.2 and 1.3 as filed")
    for phrase in ("predicts those cohorts best", "smallest error", "same across the book", "depends only on whether",
                   "the other three", "probability of reaching", "set from the last four"):
        ok(phrase not in std_flat, "5.2 files no model, fitting window or selection rule: " + phrase)

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
    for f in files:
        ok("distractor" not in f.lower(), "no file named for its role")
        if f.endswith((".csv", ".md", ".txt")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok("—" not in txt and "distractor" not in txt.lower(), "no em dash or role word in " + f)
            ok("golden copy" not in txt.lower(), "no 'golden copy' in " + f)
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(tmp2, ignore_errors=True)
    goldens_and_writeup()
    return w, G, rungs, moved, totals, tot_com


def std_flat_22(target):
    import pypdf
    return " ".join("".join(pg.extract_text() for pg in pypdf.PdfReader(
        os.path.join(target, make.FILES["standard"])).pages).split())


def F1_PPV(w):
    P, TP, FP = map(np.array, (w.P_REACH, w.TP_FLAG, w.FP_FLAG))
    Ns = np.array(w.N_TARGET[:4])
    fl = TP + FP
    return w.F_FWD * TP.sum() / fl.sum() + (w.N_TARGET[4] - w.F_FWD) * (P - TP).sum() / (Ns - fl).sum()


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
    ok(F["call"] == CALL and r1(F["expected"]) == 133.0, "call and expected arrivals")
    with zipfile.ZipFile(os.path.join(gold, deliver.XLSX)) as z:
        meta = z.read("docProps/core.xml") + z.read("docProps/app.xml")
    ok(b"Jill Berry" in meta and b"HeadingPairs" in meta and b"openpyxl" not in meta, "golden workbook container")
    sub = open(os.path.join(HERE, "..", "submission.md"), encoding="utf-8").read()
    ok(sub == writeup.build(F), "submission.md is the current writeup.py output")
    body = re.sub(r"[A-Za-z0-9_\-]+\.(csv|xlsx|txt|pdf|docx|md|png|svg)", " ", sub)
    body = body.replace("task446", " ")
    body = re.sub(r"(?m)^(\s*)(?:##\s*)?\d+\.\s", r"\1", body)
    m = F["measures"]
    test = F["test"]
    owed = {str(F["call"]), str(F["N1"]), str(F["F1"]), "%.1f" % F["expected"],
            "%.1f%%" % (m["capture"] * 100), "%.2f%%" % (m["false_alarm"] * 100), "%.1f%%" % (F["a1"] * 100),
            "%.1f%%" % (F["p1"] * 100), "%.1f%%" % (F["p_flag"] * 100), "%.1f%%" % (F["p_unflag"] * 100),
            "%.1f%%" % (test[F["model"]][1] * 100), "%.1f%%" % (test["hit_and_miss"][1] * 100)}
    for row in F["rows"] + [F["total"]]:
        owed |= {"%.1f" % row["flagged"], "%.1f" % row["unflagged"], "£{:,.1f}m".format(row["exposure"]),
                 "£{:,.1f}m".format(row["committed"]), "{:,}".format(row["groups"])}
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
    for x, step in ((m["capture"], 0.1), (m["false_alarm"], 0.01), (F["a1"], 0.1), (F["p1"], 0.1),
                    (F["p_flag"], 0.1), (F["p_unflag"], 0.1), (test[F["model"]][1], 0.1),
                    (test["hit_and_miss"][1], 0.1)):
        ok(margin(x * 100, step) >= 0.15, "percentage %.4f clear of its rounding edge" % (x * 100))


if __name__ == "__main__":
    w, G, rungs, moved, totals, tot_com = main()
    print("assertions passed:", N_ASSERT)
    print("rungs:", {k: round(float(v), 2) for k, v in rungs.items()})
    print("band figures moved:", moved)
    print("committed total moves (GBP m):", {k: round(v - tot_com, 1) for k, v in totals.items()})
    print("movers planted:", {k: len(v) for k, v in w.movers.items()}, "tuning steps", w.tune_steps)
