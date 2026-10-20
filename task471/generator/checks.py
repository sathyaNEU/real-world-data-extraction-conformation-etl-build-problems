"""The generator's assertions on the built pack: the input gates, the ladder (every route's cut and set, the golden
family's agreement and margins), the clean-truth analyst test, the adjustment's convergence (C1) and the forms ruled
out (C4), every semantic fork row (SF1 to SF12), the separation of the ask from the call (S1 to S5), the ask's stops,
the figures in the golden workbook, and the program margins."""
import csv
import json
import os
import sys

import numpy as np
import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bundle as B      # noqa: E402
import calibrate as C   # noqa: E402
import docs as DC       # noqa: E402
import golden as G      # noqa: E402
import methods as M     # noqa: E402
import pack as P        # noqa: E402
import sim as S         # noqa: E402
import world as W       # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def run(target, gdir, x=None, meta_path=None, fig_path=None, quiet=False):
    del RESULTS[:]
    fig = json.load(open(fig_path, encoding="utf-8"))
    pk = B.Pack(target)
    comp = pk.completers()
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path, encoding="utf-8"))

    # ---------------------------------------------------------------------------------------------- input gates
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    check("G2 three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, str(sorted({f.rsplit(".", 1)[1] for f in files})))
    check("G3 a file of 25,000 rows or more", max(rows.values()) >= 25000, "%d rows" % max(rows.values()))
    check("G4 two or more distractors named in metadata.json, none named so",
          len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"])
          and not any("distract" in f.lower() for f in files), str(meta["distractor_files"]))

    # ------------------------------------------------------------------------------------------------ the ladder
    fam = pk.cut("golden", "all")
    g = fig["raw_cut"]
    check("L1 the golden family agrees on one cut", {v[0] for v in fam.values()} == {g}, str({k: v[0] for k, v in fam.items()}))
    lo = min(v[1] - (W.PASS_RAW_25A - 0.5) for v in fam.values())
    hi = min((W.PASS_RAW_25A - 0.5) - v[2] for v in fam.values())
    check("L2 every method crosses 55.5 with 0.25 or more on both sides", min(lo, hi) >= 0.25, "%.2f / %.2f" % (lo, hi))
    gset = {k for k, (n, p) in pk.rates(g, comp).items() if p / n < W.REVIEW_LINE}
    routes = {"no equating": [pk.cut("no equating")[0]], "raters adjusted, no equating": [pk.cut("raters adjusted, no equating")[0]]}
    for r in ("as scored", "every assignment's papers", "multiple-choice anchor"):
        routes[r] = sorted({v[0] for v in pk.cut(r, "all").values()})
    expect = {"no equating": [56], "raters adjusted, no equating": [53], "as scored": [52],
              "every assignment's papers": [51], "multiple-choice anchor": [46, 47]}
    check("L3 every rung's cut as the ladder states it", routes == expect, str(routes))
    for r, cuts in routes.items():
        for c in cuts:
            st = {k for k, (n, p) in pk.rates(c, comp).items() if p / n < W.REVIEW_LINE}
            check("L4 %s at raw %d names its own set" % (r, c), st != gset, "%d programs" % len(st))
    as_scored = {W.PROGRAMS[k][0] for k, (n, p) in pk.rates(52, comp).items() if p / n < W.REVIEW_LINE}
    check("L5 the default path's set is the five plus Delacourt, Marisford and Riverbend",
          as_scored == {W.PROGRAMS[k][0] for k in gset} | {"Delacourt University", "Marisford State University",
                                                          "Riverbend Teaching Fellows"}, str(sorted(as_scored)))
    for c in (46, 47):
        st = {W.PROGRAMS[k][0] for k, (n, p) in pk.rates(c, comp).items() if p / n < W.REVIEW_LINE}
        check("L6 the multiple-choice anchor at raw %d takes Eastridge off" % c, "Eastridge State University" not in st,
              str(sorted(st)))
    rt = pk.rates(g, comp)
    near = min(abs(p - W.REVIEW_LINE * n) for n, p in rt.values())
    check("L7 no program within 1.5 completers of the line", near >= 1.5, "%.1f" % near)

    # -------------------------------------------------------------------- the clean truth and the generating truth
    w = x["sim"] if x and "sim" in x else S.world()
    X, VX, VXm, Y, VY, VYm = C.arrays(w)
    Xp, VXp, VXmp, Yp, VYp, VYmp = pk.arrays()
    check("T1 the pack's anchor and totals are the simulation's", np.array_equal(np.sort(X), np.sort(Xp)) and
          np.array_equal(np.sort(VX), np.sort(VXp)) and np.array_equal(np.sort(Y), np.sort(Yp)) and
          np.array_equal(np.sort(VY), np.sort(VYp)))
    b = M.validity_shift(w["papers"], w["vreads"], "WA2")
    easy = {M.cut(e)[0] for e in M.family(X, VX, Y, VY).values()}
    right = {M.cut(e)[0] for e in M.family(X, VX, Y, VY, -4 * b).values()}
    check("T2 analyst test on the clean truth: the anchor as scored files raw 52 and its set", easy == {52}, str(easy))
    check("T3 changing only the anchor's written assignment files the golden", right == {g}, str(right))
    tr = C.truth(w)[0]
    check("T4 the generating truth within one raw point of the golden", abs(tr - g) <= 1, "truth %d" % tr)

    # ---------------------------------------------------------------------------------------- C1 and C4, the adjustment
    bp = pk.validity_bias(per_paper=True)
    c_pp = {M.cut(e)[0] for e in M.family(Xp, VXp, Yp, VYp, -4 * bp).values()}
    check("C1a the per-paper mean gives the golden", c_pp == {g}, str(c_pp))
    sx = -4 * pk.validity_bias() * W.N_WA
    c_all = {M.cut(lambda v, e=e: e(v + sx))[0] for e in M.family(Xp + sx, VXp - 4 * pk.validity_bias(), Yp, VYp).values()}
    check("C1b every 2026 assignment moved, the cut read on the scores as Arcwright reported them", c_all == {g}, str(c_all))
    c_y = {M.cut(e)[0] for e in M.family(Xp, VXp, Yp, VYp + 4 * pk.validity_bias()).values()}
    check("C1c the 2025 anchor moved to the 2026 standard gives the golden", c_y == {g}, str(c_y))
    pairs = np.array([(v, pk.papers[p]["consensus"]) for p, a, v in pk.vreads if a == "WA2"])
    emap = {v: (pairs[pairs[:, 0] == v, 1].mean() if (pairs[:, 0] == v).any() else float(v)) for v in range(1, 5)}
    s26 = w["scored"][2026]
    f = s26["first"]
    r1, r2, res = s26["r1"][f][:, 1], s26["r2"][f][:, 1], s26["res"][f][:, 1]
    mp = np.vectorize(lambda v: emap[int(v)])
    wa2 = np.where(res > 0, 2 * mp(np.where(res > 0, res, 1)), mp(r1) + mp(r2))
    VXc = s26["mc"][f][:, :W.N_SHARED].sum(1) + 2 * wa2
    c_map = {M.cut(e)[0] for e in M.family(X, VXc.astype(float), Y, VY).values()}
    check("C4 a regression map onto the 2025 scores (expected score on file given a read) shrinks the 2026 reads "
          "only: raw %s" % sorted(c_map), c_map != {g} and c_map <= {46, 47, 48}, str(c_map))
    Fr = np.array([(pairs[:, 0] <= v).mean() for v in range(1, 5)])
    Fc = np.array([(pairs[:, 1] <= v).mean() for v in range(1, 5)])

    def eqmap(v):
        pr_ = ((Fr[v - 2] if v >= 2 else 0.0) + Fr[v - 1]) / 2
        return float(np.interp(pr_, np.concatenate([[0.0], Fc]), np.concatenate([[0.5], np.arange(1, 5) + 0.5])))
    mq = np.vectorize(lambda v: eqmap(int(v)))
    wa2q = np.where(res > 0, 2 * mq(np.where(res > 0, res, 1)), mq(r1) + mq(r2))
    VXq = s26["mc"][f][:, :W.N_SHARED].sum(1) + 2 * wa2q
    c_q = {M.cut(e)[0] for e in M.family(X, VXq.astype(float), Y, VY).values()}
    check("C1d an equipercentile map of the reads onto the scores on file gives the golden", c_q == {g}, str(c_q))

    # ------------------------------------------------------------------------------------------- semantic forks
    std = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs.py"), encoding="utf-8").read()
    early = sum(1 for ids in comp.values() for e in ids if pk.first.get(e, "9999") < W.PROGRAM_YEAR[0].isoformat())
    check("SF1 Rule 8.4.3 counts a first attempt made before completion, and such completers exist",
          "including an attempt before the program was completed" in std and early > 0, "%d completers" % early)
    lists = openpyxl.load_workbook(os.path.join(target, P.FILES["completers"]), read_only=True)
    raw_rows = out_year = other = dupes = dual = 0
    for k, pr in enumerate(W.PROGRAMS):
        rows_ = list(lists[pr[1]].iter_rows(values_only=True))
        head = rows_[4]
        seen = set()
        for r in rows_[5:]:
            if not r or r[0] is None:
                continue
            raw_rows += 1
            eid, area, done = B.parse_row(dict(zip(head, r)))
            out_year += int(not (W.PROGRAM_YEAR[0] <= done <= W.PROGRAM_YEAR[1]))
            other += int(not B.is_elementary(area))
            dual += int(B.is_elementary(area) and any(t in str(area).upper() for t in ("SPED", "SPECIAL")))
            dupes += int((eid, done) in seen)
            seen.add((eid, done))
    check("SF2 the lists carry rows outside the program year that Rule 8.4.2 leaves out", out_year > 0, "%d rows" % out_year)
    check("SF3 the lists carry dual-pathway completers, whom Rule 8.4.2 counts, and other pathways, which it does not",
          dual > 0 and other > 0 and "(Elementary, or Elementary and Special Education)" in std,
          "%d dual, %d other-pathway rows" % (dual, other))
    exact = {k for k, (n, p) in rt.items() if p / n < 0.70}
    rounded = {k for k, (n, p) in rt.items() if G.r1(p, n) < 70.0}
    check("SF4 below 70 per cent on the exact fraction and on the rounded rate give the same set", exact == rounded == gset)
    voids = sum(1 for r in csv.DictReader(open(os.path.join(target, P.FILES["history"]), encoding="utf-8"))
                if r["RESULT"] == "VOID" and r["TEST_DATE"] >= "2025-01-01")
    check("SF5 no voided attempt in 2025 or 2026, so counting voids changes nothing", voids == 0, "%d" % voids)
    unr_all = {min(v for v in range(W.MAX_RAW + 1) if e(v) >= W.PASS_RAW_25A)
               for e in M.family(Xp, VXp, Yp, VYp, -4 * pk.validity_bias()).values()}
    unr_sets = {c_: frozenset(k for k, (n, p) in pk.rates(c_, comp).items() if p / n < W.REVIEW_LINE) for c_ in unr_all}
    check("SF6 the unrounded reading files raw %s, the same programs; report section 4 rounds each equated score"
          % sorted(unr_all), unr_all != {g} and all(s_ == frozenset(gset) for s_ in unr_sets.values())
          and "each equated raw score is rounded to a whole number" in std)
    Xall = np.array([s["raw"] for s in pk.s26], float)
    VXall = np.array([s["mc_anchor"] + 2 * s["wa"][pk.shared_wa] for s in pk.s26], float)
    Yall = np.array([s["raw"] for s in pk.s25], float)
    VYall = np.array([s["mc_anchor"] + 2 * s["wa"][pk.shared_wa] for s in pk.s25], float)
    c_allc = {M.cut(e)[0] for e in M.family(Xall, VXall, Yall, VYall, -4 * pk.validity_bias()).values()}
    check("SF7 every candidate who sat files raw %s, the same call; report section 4 names the first-attempt "
          "candidates" % sorted(c_allc), c_allc == {g} and "equating samples are each form's first-attempt candidates" in std)
    check("SF8 the cut on the adjusted scale less the shift is the golden", c_all == {g})
    listed = sum(len(v) for v in comp.values())
    check("SF9 Rule 8.4.4 drops the untested: completers counted are fewer than completers listed",
          sum(n for n, p in rt.values()) < listed, "%d of %d" % (sum(n for n, p in rt.values()), listed))
    tie = all((s["raw"] >= W.PASS_RAW_25A) == (pk.first_result.get(s["eid"]) == "PASS") for s in pk.s25 if s["first"])
    check("SF10 the history's June 2025 results tie to Form 25A raw 56", tie)
    check("SF11 pasted duplicate rows exist and each educator counts once", dupes > 0, "%d" % dupes)
    reg24 = [r for r in csv.DictReader(open(os.path.join(target, P.FILES["register"]), encoding="utf-8"))
             if r["PROGRAM_YEAR"] == "2024-25" and B.is_elementary(r["PATHWAY"])]
    by_nm = {}
    for e_, nm in pk.names.items():
        by_nm.setdefault(nm, []).append(e_)
    firsts = []
    for r in reg24:
        e_ = r["EDUCATOR_ID"]
        if e_ not in pk.hist:
            c_ = by_nm.get((B.norm(r["LAST_NAME"]), B.norm(r["FIRST_NAME"]), B._date(r["BIRTH_DATE"])), [])
            e_ = c_[0] if len(c_) == 1 else e_
        firsts.append(pk.first.get(e_))
    n24 = sum(1 for f_ in firsts if f_ and f_ < "2025-06-14")
    nun = sum(1 for f_ in firsts if f_ is None)
    late = sum(1 for f_ in firsts if f_ and f_ > "2025-06-14")
    check("SF12 the ask's completers: %d first tested before June 2025 (counted), %d untested (not counted), %d first "
          "tested later" % (n24, nun, late), n24 > 0 and nun > 0 and late == 0)

    # ---------------------------------------------------------------------------- separation and the ask's stops
    py, pid = pk.prior_year(), pk.prior_year(match="id")
    miss = sum(int(py[k][0] != pid[k][0]) + int(G.r1(py[k][1], py[k][0]) != G.r1(pid[k][1], pid[k][0])) for k in py)
    check("S1 the register's educator ID (the cracker) misses all 32 ask figures", miss == 32, "%d of 32 differ" % miss)
    ndup = sum(py[k][0] - pid[k][0] for k in py)
    check("S2 every program has at least two completers under a second record", min(py[k][0] - pid[k][0] for k in py) >= 2,
          "%d in all" % ndup)
    reg = list(csv.DictReader(open(os.path.join(target, P.FILES["register"]), encoding="utf-8")))
    reg_ids = {r["EDUCATOR_ID"] for r in reg}
    check("S3 no register-only record is in any 2026 or 2025 equating sample", not ({s["eid"] for s in pk.s26 if s["first"]}
                                                                                   | {s["eid"] for s in pk.s25 if s["first"]})
          & (reg_ids - set(pk.hist)))
    check("S4 the call reads no register row (no 2025-26 completer is a register row)",
          not ({e for ids in comp.values() for e in ids} & {r["EDUCATOR_ID"] for r in reg if r["PROGRAM_YEAR"] == "2025-26"}))
    dup_people = [p for p in (x["rows"] if x else []) + (x["extra"] if x else []) if p.get("dup")]
    check("S5 the second records' attempts are first attempts in June 2025 or June 2024 under the original record",
          all(pk.first.get(p["eid"]) in ("2025-06-14", "2024-06-08") for p in dup_people), "%d people" % len(dup_people))

    # ---------------------------------------------------------------------------------- the golden's own figures
    wb = openpyxl.load_workbook(os.path.join(gdir, G.GOLDEN["workbook"]), data_only=True)
    sh = wb["Reviews 2027"]
    got = {r[0]: r for r in sh.iter_rows(min_row=5, values_only=True) if r[0]}
    okw = all(got[q["code"]][2] == q["counted"] and got[q["code"]][3] == q["passed"] and got[q["code"]][4] == q["rate"]
              and (got[q["code"]][5] == "Yes") == q["review"] for q in fig["programs"])
    check("W1 the workbook's review sheet is figures.json", okw)
    pr = {r[0]: r for r in wb["2024-25 completers"].iter_rows(min_row=2, values_only=True)}
    check("W2 the workbook's 2024-25 sheet is figures.json", all(pr[q["code"]][2] == q["prior_tested"] and
                                                                 pr[q["code"]][4] == q["prior_rate"] for q in fig["programs"]))
    check("W3 figures.json's set is the pack's", {W.PROGRAMS[k][0] for k in gset} == set(fig["review"]))
    # reads in reverse order give the same shift (row order)
    rev = [d for _, _, d in sorted(((p, a, v - pk.papers[p]["consensus"]) for p, a, v in reversed(pk.vreads) if a == "WA2"),
                                   reverse=True)]
    check("O1 row order: the shift is the same over a reversed read file", abs(np.mean(rev) - pk.validity_bias()) < 1e-12)
    good = all(ok for _, ok, _ in RESULTS)
    if not quiet:
        for name, ok, detail in RESULTS:
            print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  (%s)" % detail) if detail else ""))
        print("checks: %d of %d pass" % (sum(ok for _, ok, _ in RESULTS), len(RESULTS)))
    return good
