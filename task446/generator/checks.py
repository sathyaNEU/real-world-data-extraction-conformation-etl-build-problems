"""Assertions for task446 (architecture 2). Builds the pack twice, runs the independent solver on it and
checks the ladder, the convergence of every rigorous route, the bins, the devices, the separation of the
main call from every device, the inert texture on the main path and the input gates.

    python3 task446/generator/checks.py
"""
import filecmp
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world      # noqa: E402
import solve      # noqa: E402
import make       # noqa: E402

N_ASSERT = 0


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


def main():
    target = os.path.join(HERE, "..", "target")
    # ------------------------------------------------------------ two builds byte-identical
    tmp = tempfile.mkdtemp()
    a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
    for t in (a, b):
        subprocess.run([sys.executable, os.path.join(HERE, "make.py"), t], check=True, capture_output=True)
    names = sorted(os.listdir(a))
    ok(names == sorted(os.listdir(b)), "file lists differ between builds")
    for n in names:
        ok(filecmp.cmp(os.path.join(a, n), os.path.join(b, n), shallow=False), "build differs: " + n)
    for n in names:
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
    ok(len(tab[4]["M"]) == world.N_TARGET[4] and len(tab[4]["F"]) == world.F_FWD, "forward book")
    for c in range(5):
        want = {g.gid for g in w.groups.values() if g.flag.get(c) and w.active(g, world.COHORTS[c])
                and not w.on_list(g, world.COHORTS[c])}
        ok(want == tab[c]["F"], "flags in the pack match the design, cohort %d" % c)

    m = fc["measures"]
    ok(m["TP"] == 158 and m["P"] == 201 and m["FP"] == 253 and m["N"] - m["P"] == 3307, "pooled counts")

    # ------------------------------------------------------------ the answer and its convergent routes
    call = fc["total"]
    ok(round(call) == 134 and margin(call, 1) > 0.35, "call 134, %.3f" % call)
    P, TP, FP = map(np.array, (world.P_REACH, world.TP_FLAG, world.FP_FLAG))
    Ns = np.array(world.N_TARGET[:4])
    N1, F1 = world.N_TARGET[4], world.F_FWD
    a1 = F1 / N1
    a = (TP + FP) / Ns
    p = P / Ns
    se_c, f_c = TP / P, FP / (Ns - P)
    b0, c0 = np.polyfit(a, p, 1)
    bw, cw = np.polyfit(a, p, 1, w=np.sqrt(Ns))
    routes = dict(pooled=call, ols=N1 * (c0 + b0 * a1), wls=N1 * (cw + bw * a1),
                  per_cohort=np.mean([N1 * (a1 - f_c[i]) / (se_c[i] - f_c[i]) for i in range(4)]),
                  averaged_rates=N1 * (a1 - f_c.mean()) / (se_c.mean() - f_c.mean()))
    for k, v in routes.items():
        ok(round(v) == 134 and abs(v - 134) < 0.33, "route %s files 134 (%.2f)" % (k, v))
    ok(margin(fc["flagged"]) >= 0.3 and margin(fc["unflagged"]) >= 0.3, "split mid-bin")
    ok(r1(fc["flagged"]) == 105.4 and r1(fc["unflagged"]) == 28.7, "split figures")

    # ------------------------------------------------------------ the ladder
    fl = TP + FP
    ppv, miss = TP / fl, (P - TP) / (Ns - fl)
    PPV0, M0 = TP.sum() / fl.sum(), (P - TP).sum() / (Ns - fl).sum()
    rungs = dict(
        R0_pooled_hit_miss=F1 * PPV0 + (N1 - F1) * M0,
        R0b_latest_cohort=F1 * ppv[3] + (N1 - F1) * miss[3],
        R1_stressed_cohort=F1 * ppv[0] + (N1 - F1) * miss[0],
        R2_trended_hit_rate=F1 * np.polyval(np.polyfit(a, ppv, 1), a1) + (N1 - F1) * np.polyval(np.polyfit(a, miss, 1), a1),
        R3_flags_plus_misses=F1 + (N1 - F1) * M0,
        V_base_rate=N1 * P.sum() / Ns.sum(),
        V_flagged_only=F1 * PPV0,
        V_error_rates_flagged_only=fc["flagged"],
    )
    yield_fc = solve.forecast(tab, "yield")
    ok(abs(yield_fc["total"] - rungs["R0_pooled_hit_miss"]) < 1e-9, "R0 reproduces from the pack")
    ok(round(rungs["R0_pooled_hit_miss"]) == 74, "R0 74")
    for k, v in rungs.items():
        ok(abs(v / call - 1) >= 0.06, "rung %s at least 6 per cent from the answer (%.2f)" % (k, v))
    nearest = min(rungs.items(), key=lambda kv: abs(kv[1] / call - 1))
    ok(nearest[0] == "R2_trended_hit_rate" and 0.09 < nearest[1] / call - 1 < 0.13, "nearest wrong cell R2")
    ok(len({round(v) for v in rungs.values()}) == len(rungs), "every rung files a different whole number")

    # ------------------------------------------------------------ the back-test the data carries
    loo_yield, loo_err = [], []
    for i in range(4):
        mm = [j for j in range(4) if j != i]
        nv = fl[i] * TP[mm].sum() / fl[mm].sum() + (Ns[i] - fl[i]) * (P[mm] - TP[mm]).sum() / (Ns[mm] - fl[mm]).sum()
        se = TP[mm].sum() / P[mm].sum()
        ff = FP[mm].sum() / (Ns[mm] - P[mm]).sum()
        rg = Ns[i] * (a[i] - ff) / (se - ff)
        loo_yield.append(nv / P[i] - 1)
        loo_err.append(rg / P[i] - 1)
    ok(max(abs(x) for x in loo_err) < 0.03, "error-rate model re-run one cohort out within 3 per cent")
    ok(np.mean(np.abs(loo_yield)) > 0.2 and min(abs(x) for x in loo_yield) > 0.08, "yield model fails every re-run")
    ok(ppv[0] > ppv[3] > ppv[1] > ppv[2] and p[0] > p[3] > p[1] > p[2], "hit rate tracks the deterioration rate")
    ok(max(se_c) - min(se_c) < 0.07 and max(f_c) - min(f_c) < 0.006, "capture and false-alarm rates hold")

    # ------------------------------------------------------------ bands
    bt = G["bands"]
    ok([r["groups"] for r in bt] == world.BAND_N and [r["flagged"] for r in bt] == world.BAND_F, "band plan")
    for r in bt:
        for k in ("exp_flagged", "exp_unflagged"):
            ok(margin(r[k]) >= 0.3, "%s %s mid-bin (%.3f)" % (r["band"], k, r[k]))
        ok(margin(r["exp_total"]) >= 0.15, "%s total mid-bin (%.3f)" % (r["band"], r["exp_total"]))
        ok(margin(r["exp_exposure"] / 1e6) >= 0.2, "%s exposure mid-bin" % r["band"])
    tot_exp = sum(r["exp_exposure"] for r in bt) / 1e6
    ok(margin(tot_exp) >= 0.2, "exposure total mid-bin (%.3f)" % tot_exp)
    ok(abs(sum(r["exp_total"] for r in bt) - call) < 1e-9, "bands tie to the call")
    for g in tab[4]["M"]:
        e = G["exp"].get(g, 0.0)
        ok(min(abs(e - x) for x in solve.EDGES) >= 0.25e6, "group %s clear of band edges" % g)
    wfig = world.band_exposure_figures(w, w.cohort)
    for i, r in enumerate(bt):
        ok(abs(wfig[i] - r["exp_exposure"] / 1e6) < 1e-6, "world and pack agree on band %d exposure" % i)

    # the naive model fails every band figure
    nb = solve.band_table(tab, yield_fc, G["exp"])
    for r, q in zip(bt, nb):
        for k in ("exp_flagged", "exp_unflagged", "exp_exposure"):
            sc = 1e6 if k == "exp_exposure" else 1
            ok(r1(r[k] / sc) != r1(q[k] / sc), "naive model misses %s %s" % (r["band"], k))

    # ------------------------------------------------------------ devices (exposure path only)
    dev = dict(D2=dict(scheduled=True), D4=dict(with_dac=False), D3=dict(fx_multiply=True),
               D8=dict(count_matured=True), H_status=dict(status_filter=False))
    device_moves = {}
    for name, kw in dev.items():
        e2 = solve.exposures(pk, **kw)
        bt2 = solve.band_table(tab, fc, e2)
        moved = []
        for r, q in zip(bt, bt2):
            for k in ("exp_flagged", "exp_unflagged", "exp_exposure"):
                sc = 1e6 if k == "exp_exposure" else 1
                if r1(r[k] / sc) != r1(q[k] / sc):
                    moved.append((r["band"], k))
        device_moves[name] = moved
        if name != "H_status":
            ok(sum(1 for x in moved if x[1] == "exp_flagged") >= 2, "%s moves at least two flagged-arrival figures" % name)
        ok(len(moved) >= 4, "%s moves at least four band figures" % name)
        tot2 = sum(q["exp_exposure"] for q in bt2) / 1e6
        ok(r1(tot2) != r1(tot_exp), "%s moves the exposure total" % name)
        # separation: the call and every cohort count are untouched by the device
        ok(round(solve.forecast(tab)["total"]) == 134, "%s cannot move the call" % name)
    w._device_moves = device_moves

    # ------------------------------------------------------------ inert texture on the main path
    for kw in (dict(keep_lapsed=False), dict(case_fold=False), dict(follow_funds=True), dict(branches=False),
               dict(successors=False), dict(follow_direct=False)):
        t2 = pk.cohort_table(**kw)
        for c in range(5):
            ok(t2[c]["F"] == tab[c]["F"], "texture %s inert at cohort %d" % (kw, c))
    # main-path conformance that is not texture: non-borrowing members and company-number keys matter
    resolve_obl_only = 0
    for c in range(5):
        date = solve.d(solve.COHORTS[c])
        _, k2g = pk.group_of_key(date)
        ds = date.isoformat()
        F_obl = {k2g[r["entity_key"].upper()] for r in pk.signals if r["publication_date"] == ds and r["signal"] != "GREEN"
                 and r["entity_key"].upper() in k2g} & tab[c]["M"]
        resolve_obl_only += len(tab[c]["F"] - F_obl)
    ok(resolve_obl_only > 0, "groups flagged only through a non-borrowing member exist")

    # ------------------------------------------------------------ clean-data test: repair the exposure files
    ok(round(solve.forecast(tab, "error_rates")["total"]) == 134 and round(yield_fc["total"]) == 74,
       "answer and naive do not read any exposure file")

    # ------------------------------------------------------------ input gates and hygiene
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "three or more formats")
    nrows = sum(1 for _ in open(os.path.join(target, make.FILES["signals"]), encoding="utf-8")) - 1
    ok(nrows >= 25000, "spine has 25,000 or more rows")
    for dfile in make.DISTRACTORS:
        ok(dfile in files, "distractor present: " + dfile)
    tmp2 = tempfile.mkdtemp()
    for f in files:
        if f not in make.DISTRACTORS:
            shutil.copy(os.path.join(target, f), tmp2)
    G2 = solve.golden(tmp2)
    ok(G2["call"] == 134 and abs(sum(r["exp_exposure"] for r in G2["bands"]) / 1e6 - tot_exp) < 1e-9,
       "golden unchanged with the distractors deleted")
    for f in files:
        ok("distractor" not in f.lower(), "no file named for its role")
        if f.endswith((".csv", ".md", ".txt")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok("—" not in txt, "no em dash in " + f)
            ok("distractor" not in txt.lower(), "no role word in " + f)
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(tmp2, ignore_errors=True)
    goldens_and_writeup()
    return w, G, rungs, routes, loo_yield, loo_err, device_moves


def goldens_and_writeup():
    """The goldens rebuild byte-identically and match the shipped copies; the write-up is the one writeup.py
    emits; every number in it is owed by a figure, a citation or a date (swept by unit class)."""
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
    ok(F["call"] == 134 and r1(F["expected"]) == 134.1, "call and expected arrivals")
    sub = open(os.path.join(HERE, "..", "submission.md"), encoding="utf-8").read()
    ok(sub == writeup.build(F), "submission.md is the current writeup.py output")
    body = re.sub(r"[A-Za-z0-9_\-]+\.(csv|xlsx|txt|pdf|docx|md|png|svg)", " ", sub)
    body = body.replace("task446", " ")
    body = re.sub(r"(?m)^(\s*)(?:##\s*)?\d+\.\s", r"\1", body)
    m = F["measures"]
    owed = {str(F["call"]), str(F["N1"]), str(F["F1"]), "%.1f" % F["expected"],
            "%.1f%%" % (m["capture"] * 100), "%.2f%%" % (m["false_alarm"] * 100), "%.1f%%" % (F["a1"] * 100),
            "%.1f%%" % (F["p1"] * 100), "%.1f%%" % (F["p_flag"] * 100), "%.1f%%" % (F["p_unflag"] * 100), "3%"}
    for row in F["rows"] + [F["total"]]:
        owed |= {"%.1f" % row["flagged"], "%.1f" % row["unflagged"], "£{:,.1f}m".format(row["exposure"])}
    for band in deliver.BANDS:
        owed |= set(re.findall(r"£\d+m", band))
    cites = {"2.2", "2.3", "3.2", "4.1", "4.2", "4.3", "5.2", "5.3", "6.1", "6.2", "07"}
    dates = {"30", "2022", "2025", "2026", "2027", "30/09", "23:05"}
    tokens = re.findall(r"£[\d,]+(?:\.\d+)?m|\d+(?:[.:/]\d+)?%?", body)
    stray = [t for t in tokens if t not in owed | cites | dates]
    ok(not stray, "every number in submission.md is owed: %s" % stray)
    for t in owed - {"3%"}:
        ok(t in body, "owed figure stated in submission.md: " + t)


if __name__ == "__main__":
    w, G, rungs, routes, ly, le, dm = main()
    print("assertions passed:", N_ASSERT)
    print("routes:", {k: round(float(v), 3) for k, v in routes.items()})
    print("rungs:", {k: round(float(v), 2) for k, v in rungs.items()})
    print("re-run one cohort out, yield model:", [round(x, 3) for x in ly], "error-rate model:", [round(x, 3) for x in le])
    for k, v in dm.items():
        print("device", k, len(v), v[:6])
    print("movers planted:", {k: len(v) for k, v in w.movers.items()}, "tuning steps", w.tune_steps)
