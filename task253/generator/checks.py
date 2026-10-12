"""Every assertion the design note owes: the semantic fork rows SF1 to SF17, the ladder's stage 3 acceptance
criteria, the grid, the closures, the hazard ledger, the ask stops and their composition, the chart, the bin
distances, the input gates, the counter-pin sweep and the realism sweep."""
import itertools
import json
import os
import re
import shutil
import tempfile
import zipfile

import numpy as np

import asks as A
import core
import model as M
import names as NM
import pack as P

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))


def clear(x, unit=1.0):
    f = (x / unit) % 1.0
    return abs(f - 0.5)          # distance from the rounding boundary, in steps


def off(a, g, pct=0.06):
    return abs(a - g) >= pct * g


def run(W, tables, fd, figs, grid, fam_out, fam_probs, st, target, task_dir, docs_text):
    del RESULTS[:]
    p, mean, var, n = fd["p"], fd["mean"], fd["var"], fd["n"]
    G = figs["places_exact"]
    gold = figs["places"]
    reg = W["region"]

    # ---------------------------------------------------------------- the call and its bin
    ok("call is 42", gold == 42, G)
    ok("call clears its bin by 0.25", clear(G) >= 0.25, G)
    ok("call not on the round value", abs(G - gold) >= 0.02, G)

    # ---------------------------------------------------------------- semantic fork rows
    gtext, stext = docs_text["guidelines"], docs_text["standard"]
    ok("SF1 one place per partner school", "One place is commissioned for each partner school" in gtext)
    codes_in_results = set()
    for df in tables:
        codes_in_results |= set(np.unique(df.school))
    ok("SF2 secondary colleges carry no results", len(codes_in_results) == 264 and len(W["sec"]) == 58)
    ok("SF3 three-year averages refused (many years)", "over many years" in gtext and grid["R0_raw_points"] != gold,
       grid["R0_raw_points"])
    # SF4: exempt students at the bottom of the scale
    y5 = fd["y5"]
    lo = float(y5.score.min())
    ex = []
    for j, df in enumerate(tables):
        d = df[(df.year == 5) & (df.test == "RD") & (df.part == "E")]
        ex.append((d.school.to_numpy(), j))
    n2, yb2 = n.copy(), fd["ybar"].copy()
    for s, j in ex:
        for i in s:
            yb2[i, j] = (yb2[i, j] * n2[i, j] + lo) / (n2[i, j] + 1)
            n2[i, j] += 1
    f4, m4, v4, p4 = M.golden_probs(n2, yb2, fd["SSW"], fd["N"] + sum(len(s) for s, _ in ex))
    ok("SF4 exempt at the bottom of the scale moves the call 6 per cent", off(p4.sum(), G), p4.sum())
    ok("SF4 refused by standard 2.1", "have no scale score and do not enter an analysis" in stext)
    ok("SF5 no school's model average sits on 480", np.min(np.abs(mean - 480)) > 0.01 and
       np.min(np.abs((n * fd["ybar"]).sum(1) / n.sum(1) - 480)) > 0.01)
    ok("SF6 2026 only, every cell 6 per cent off",
       all(off(grid[k], G) for k in ("y26_raw_points", "y26_raw_probs", "y26_school_points", "y26_school_probs")),
       [grid[k] for k in ("y26_raw_points", "y26_raw_probs", "y26_school_points", "y26_school_probs")])
    ok("SF7 a whole number of places", isinstance(gold, int))
    ok("SF8 school level only refused by standard 3.1", "a random effect for the year group within the school" in stext
       and off(grid["R3_points"], G) and off(grid["R3_probs"], G))
    for k in ("ml", "sitting", "school_s2", "mean_unc", "integrated"):
        ok("SF9-12,17 %s same call, 0.10 inside the bin" % k, round(fam_out[k]) == gold and clear(fam_out[k]) >= 0.10,
           fam_out[k])
    ok("SF9 REML filed", "Variance components are estimated by restricted maximum likelihood." in stext)
    ok("SF10 one scale filed", "analysed together without adjustment" in stext)
    ok("SF11 one student residual filed", "and the student residual." in stext)
    ok("SF12 and SF17 fitted values filed", "at their fitted values" in stext)
    ok("SF13 population share in the bin", round(fam_out["population_share"]) == gold and
       clear(fam_out["population_share"]) >= 0.10, fam_out["population_share"])
    ok("SF14 no school trend in the world; a fixed effect per sitting gives the same call",
       round(fam_out["sitting"]) == gold and W["w"]["v"].shape == (264, 3))
    ok("SF15 posterior median and mode", fam_out["median"] == gold and fam_out["mode"] == gold,
       (fam_out["median"], fam_out["mode"]))
    ok("SF16 other tests not added (standard 3.5)", "Results in other tests or year levels" in stext)

    # ---------------------------------------------------------------- ladder acceptance
    ok("R0 at least 1.25 times", grid["R0_raw_points"] >= 1.25 * G, grid["R0_raw_points"])
    ok("R1 at most 0.80 times", grid["R1_points"] <= 0.80 * G, grid["R1_points"])
    ok("R2 off", off(grid["R2_bound90"], G), grid["R2_bound90"])
    ok("R3 points at most 0.88 times", grid["R3_points"] <= 0.88 * G, grid["R3_points"])
    ok("R3 probabilities at least 1.08 times", grid["R3_probs"] >= 1.08 * G, grid["R3_probs"])
    for k in ("raw_bound90", "raw_probs", "R3_bound90", "y2526_raw_points", "y2526_points", "y2526_probs"):
        ok("grid %s 6 per cent off" % k, off(grid[k], G), grid[k])
    true = int(((core.MU + W["w"]["shift"] + W["w"]["u"]) < 480).sum())
    ok("realised count within 2 of the golden", abs(true - G) <= 2, true)
    ok("decomposition exact", abs(grid["R1_points"] - grid["mass_above_among_below"] + grid["mass_below_among_above"] - G)
       < 1e-9)
    ok("predictions less spread than the underlying averages",
       grid["sd_predictions"] < grid["sd_underlying"] < grid["sd_raw"])
    ok("probability does not track size", abs(grid["corr_p_size"]) < 0.15, grid["corr_p_size"])
    f = fd["fit"]
    ok("components near design", 15.5 < f["tu"] ** 0.5 < 18 and 8 < f["tv"] ** 0.5 < 12 and 68 < f["s2"] ** 0.5 < 72,
       (f["tu"] ** 0.5, f["tv"] ** 0.5, f["s2"] ** 0.5))
    ok("cohorts 4 to about 160, median about 29", n[:, 2].min() >= 4 and 140 <= n.max() <= 170 and
       25 <= np.median(n[:, 2]) <= 33, (n.min(), n.max(), np.median(n[:, 2])))

    # ---------------------------------------------------------------- closures
    ok("C1 population 264 primaries with results in every sitting", n.shape == (264, 3) and (n > 0).all())
    for j, df in enumerate(tables):
        ok("C1 no duplicate student-test rows %d" % j, not df.duplicated(["student", "year", "test"]).any())
        ok("C1 non-participants scoreless %d" % j, df[df.part != "P"].score.isna().all() and
           df[df.part == "P"].score.notna().all())
    yb24 = fd["ybar"].copy()
    d24 = y5[y5.sitting == 0]
    s = np.zeros(264)
    np.add.at(s, d24.school.to_numpy(), np.round(d24.score.to_numpy()))
    yb24[:, 0] = s / n[:, 0]
    _, m24, v24, p24 = M.golden_probs(n, yb24, fd["SSW"], fd["N"])
    ok("C1 2024 scores rounded, same call", round(p24.sum()) == gold, p24.sum())

    # ---------------------------------------------------------------- shares, asks and bins
    for r in core.REGIONS:
        ok("share %s clears 0.02" % r, clear(figs["shares"][r], 0.1) >= 0.2, figs["shares"][r])
        ok("students %s clears 0.2" % r, clear(figs["students_region"][r]) >= 0.2, figs["students_region"][r])
    for h in A.HUBS:
        ok("hub students %s clears 0.2" % h, clear(figs["students_hub"][h]) >= 0.2, figs["students_hub"][h])
        ok("hub km %s clears 0.2" % h, clear(figs["km_hub"][h]) >= 0.2, figs["km_hub"][h])
    ok("totals clear 0.2", clear(figs["students_total"]) >= 0.2 and clear(figs["km_total"]) >= 0.2)
    ok("rounded shares add to 100.0", abs(sum(round(v, 1) for v in figs["shares"].values()) - 100.0) < 1e-9)
    ok("hub totals equal region totals", abs(sum(figs["students_hub"].values()) - figs["students_total"]) < 1e-6)
    pts_sh = st["points_shares"]
    ok("point-count shares leave every bin", all(round(pts_sh[r], 1) != round(figs["shares"][r], 1)
                                                 for r in core.REGIONS), pts_sh)

    gold_key = ("golden", "plan", "probs", 2)
    mess = {"B1": ("golden", "directory", "probs", 2),
            "H2": ("golden", "plan", "probs", 1), "pts": ("golden", "plan", "points", 2)}
    g0 = st[gold_key]
    # A1 (a filed reading): the notes say year level is as the student system held it on the day of the run and
    # that students move up one level at the start of each school year. A2 (the device, D8): at the rolled
    # schools the system had already been moved to 2027 before the run, so their rows run Year 1 to Year 7 with
    # no Foundation; only that inconsistency, against the register's F-6, finds them. SF18 is the ask's row.
    notes_flat = " ".join(docs_text["notes"].split()).lower()
    ok("SF18 A1 filed: year level as the student system held it on the day of the run",
       "year level is as the student system held it on the day of the run" in notes_flat)
    ok("SF18 A1 filed: students move up one level each school year",
       "students move up one year level at the start of each school year" in notes_flat)
    cen_entry = notes_flat.split(P.FILES["census"].lower())[1].split("the run writes the school number")[0]
    ok("A2 unflagged: the census entry names no rollover, no school and no count",
       not any(w in cen_entry for w in ("rolled", "rollover", "roll over", "2027", "moved", "already", "some school",
                                        "except")) and
       not re.search(r"\d", re.sub(r"(7 august 2026|4 november 2026)", "", cen_entry)), cen_entry)
    rolled = W["rolled"]
    cen_lines = open(os.path.join(target, P.FILES["census"])).read().splitlines()[1:]
    idx = {int(c): i for i, c in enumerate(W["codes"])}
    held = {}
    for ln in cen_lines:
        _, sc, lv, hc = ln.split(",")
        if int(sc) in idx:
            held.setdefault(idx[int(sc)], {})[lv] = int(hc)
    ok("A2 every primary has seven census rows", all(len(held[i]) == 7 for i in range(264)))
    sig = np.array(["7" in held[i] and "F" not in held[i] for i in range(264)])
    ok("A2 the rolled schools are exactly those running Year 1 to 7 with no Foundation",
       np.array_equal(sig, rolled) and all(("F" in held[i]) != bool(rolled[i]) for i in range(264)))
    ok("A2 school totals invariant", all(sum(held[i].values()) == int(W["census"][i].sum()) for i in range(264)))
    ok("A2 every school has Foundation and Year 6 students (the signature is never empty)",
       (W["census"][:, 0] > 0).all() and (W["census"][:, 6] > 0).all())
    ok("A2 no marker: one census date on every row, colleges untouched",
       len({ln.split(",")[0] for ln in cen_lines}) == 1 and
       {ln.split(",")[2] for ln in cen_lines if int(ln.split(",")[1]) not in idx} == {str(k) for k in range(7, 13)})
    ok("A2 a realistic share, 15 to 25 per cent, four or more schools in every region",
       0.15 <= rolled.mean() <= 0.25 and min((rolled & (reg == r)).sum() for r in core.REGIONS) >= 4,
       int(rolled.sum()))
    ok("A2 not tied to the schools' results", abs(np.corrcoef(rolled.astype(float), p)[0, 1]) < 0.10,
       np.corrcoef(rolled.astype(float), p)[0, 1])
    # split evidence: the 2026 NAPLAN Year 3 and Year 5 cohorts match the census's 2026 Years 3 and 5 (the file's
    # Years 4 and 6 at a rolled school) within the March to August movement, at every school
    d26 = tables[2]
    for yl in (3, 5):
        nap = np.bincount(d26[(d26.year == yl) & (d26.test == "RD")].school.to_numpy(), minlength=264)
        fl = np.array([held[i][str(yl + 1 if rolled[i] else yl)] for i in range(264)])
        ok("A2 split evidence: 2026 NAPLAN Year %d cohorts within 2 of the census's 2026 Year %d" % (yl, yl),
           np.abs(nap - fl).max() <= 2, np.abs(nap - fl).max())
    lit = np.array([sum(held[i].get(str(k), 0) for k in ((3, 4, 5, 6) if sig[i] else (2, 3, 4, 5)))
                    for i in range(264)])
    ok("SF18 literal read of the notes, the register and the census = golden students per school",
       np.array_equal(lit, A.students(W["census"], "golden")))
    lit_reg = A.by_region(p, lit, reg)
    ok("SF18 literal read gives the golden students by region",
       all(round(lit_reg[r]) == round(figs["students_region"][r]) for r in core.REGIONS)
       and round(float((p * lit).sum())) == round(figs["students_total"]))
    # the cracker reads the file's Years 2 to 5 everywhere (A1 executed, A2 missed): every students figure off
    crk = A.students(W["census"], "cracker", rolled)
    ok("A2 the cracker's read differs from the golden only at the rolled schools",
       np.array_equal(crk != A.students(W["census"], "golden"), rolled & (W["census"][:, 1] != W["census"][:, 5])))
    cr_reg, cr_hub = A.by_region(p, crk, reg), A.by_hub(p, crk, W["plan"])
    for r in core.REGIONS:
        dlt = cr_reg[r] - figs["students_region"][r]
        ok("A2 cracker moves students %s by 4 students and 1 per cent" % r,
           abs(dlt) >= max(4.0, 0.01 * figs["students_region"][r]), (cr_reg[r], figs["students_region"][r]))
    for h in A.HUBS:
        ok("A2 cracker moves hub students %s by 4 students" % h,
           abs(cr_hub[h] - figs["students_hub"][h]) >= 4.0, (cr_hub[h], figs["students_hub"][h]))
    ok("A2 cracker moves the students total by 20", abs(float((p * crk).sum()) - figs["students_total"]) >= 20.0,
       float((p * crk).sum()))
    for name, key in mess.items():
        s1 = st[key]
        if name == "pts":
            for r in core.REGIONS:
                ok("%s moves students %s 3 per cent" % (name, r),
                   abs(s1["students_region"][r] - g0["students_region"][r]) >= 0.03 * g0["students_region"][r],
                   (s1["students_region"][r], g0["students_region"][r]))
        if name in ("B1", "pts"):
            for h in A.HUBS:
                ok("%s moves hub students %s 3 per cent" % (name, h),
                   abs(s1["students_hub"][h] - g0["students_hub"][h]) >= 0.03 * g0["students_hub"][h],
                   (s1["students_hub"][h], g0["students_hub"][h]))
        if name in ("B1", "H2", "pts"):
            for h in A.HUBS:
                ok("%s moves hub km %s 3 per cent" % (name, h),
                   abs(s1["km_hub"][h] - g0["km_hub"][h]) >= 0.03 * g0["km_hub"][h], (s1["km_hub"][h], g0["km_hub"][h]))
    # stops and every subset of mishandlings: each graded figure leaves its bin
    reads = A.READS
    n_cells = 0
    for read, hubs, wt, mult in itertools.product(reads, ("plan", "directory"), ("probs", "points"), (2, 1)):
        key = (read, hubs, wt, mult)
        if key == gold_key:
            continue
        s1 = st[key]
        if read != "golden" or wt != "probs":
            for r in core.REGIONS:
                ok("subset %s students %s out of bin" % (key, r),
                   round(s1["students_region"][r]) != round(g0["students_region"][r]))
                n_cells += 1
            ok("subset %s students total out of bin" % (key,), round(s1["students_total"]) != round(g0["students_total"]))
        if read != "golden" or wt != "probs" or hubs != "plan":
            for h in A.HUBS:
                ok("subset %s hub students %s out of bin" % (key, h),
                   round(s1["students_hub"][h]) != round(g0["students_hub"][h]))
                n_cells += 1
        if hubs != "plan" or wt != "probs" or mult != 2:
            for h in A.HUBS:
                ok("subset %s hub km %s out of bin" % (key, h), round(s1["km_hub"][h]) != round(g0["km_hub"][h]))
                n_cells += 1
            ok("subset %s km total out of bin" % (key,), round(s1["km_total"]) != round(g0["km_total"]))
    # the chart
    ok("chart: the new coastal hub leads only on the golden path", figs["chart_title_hub"] == "E" and
       g0["km_hub"]["E"] >= 1.05 * sorted(g0["km_hub"].values())[-2])
    for name in ("B1", "pts"):
        s1 = st[mess[name]]
        ok("chart title hub changes under %s" % name, s1["chart_order"][0] != "E", s1["chart_order"])
        ok("chart order changes under %s" % name, s1["chart_order"] != figs["chart_order"])
    ok("B1: every hub's list changes", all((W["dir_hub"] == h).sum() != (W["plan"] == h).sum() or
                                          set(np.where(W["dir_hub"] == h)[0]) != set(np.where(W["plan"] == h)[0])
                                          for h in A.HUBS))
    ok("B1: 6 pilots, 38 to E, 7 between A to D", len(W["pilots"]) == 6 and len(W["near_e"]) == 38 and
       len(W["moves"]) == 7 and int((W["dir_hub"] != W["plan"]).sum()) == 45)

    # ---------------------------------------------------------------- separation and hazards
    dev_files = [P.FILES[k] for k in ("census", "directory", "plan", "road")]
    main_files = [P.FILES[k] for k in ("r2024", "r2025", "r2026", "register")]
    ok("hazard rows on the main path: zero (device files disjoint from the main call's files)",
       not set(dev_files) & set(main_files))
    cen = open(os.path.join(target, P.FILES["census"])).read().splitlines()[1:]
    ok("H1 integer codes in the census", any(re.match(r"[^,]*,\d{1,3},", ln) for ln in cen))
    lead0 = sum(1 for c in W["codes"] if c.startswith("0"))
    ok("H1 about a third of codes start with zero", 0.25 <= lead0 / 264 <= 0.40, lead0)

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    ok("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    big = max(len(open(os.path.join(target, f)).read().splitlines()) for f in files if f.endswith(".csv"))
    ok("gate: a file of 25,000 rows", big >= 25000, big)
    meta = json.load(open(os.path.join(task_dir, "metadata.json")))
    ok("gate: two distractors named in metadata", len(meta["distractor_files"]) >= 2 and
       all(d in files for d in meta["distractor_files"]))
    ok("gate: no file named as a distractor", not any("distract" in f.lower() for f in files))
    ok("gate: every file has source, date and licence", all(x.get("source") and x.get("date") and x.get("license")
                                                            for x in meta["files"]))

    # ---------------------------------------------------------------- counter-pin sweep
    allt = "\n".join(docs_text.values())
    for wd in ("predict", "probabilit", "expected number", "interval", "flag", "credibl", "shrink", "posterior"):
        ok("counter-pin: no '%s' in the filed text" % wd, wd not in allt.lower())
    ok("counter-pin: 'estimat' only in standard 3.2", allt.lower().count("estimat") == 1)
    ok("counter-pin: 480 named once, in guidelines 2", allt.count("480") == 1)

    # ---------------------------------------------------------------- realism sweep
    part = n.sum(0)
    ok("realism: participants differ across sittings", len(set(part)) == 3, part)
    rows = [len(t) for t in tables]
    ok("realism: row counts differ across sittings", len(set(rows)) == 3, rows)
    ok("realism: no round headline totals", all(int(round(x)) % 10 != 0 for x in
                                                [figs["students_total"], figs["km_total"]]))
    ok("realism: localities pass the real-name check", all(not NM.clashes(L, NM.reference()) for L in
                                                          sorted({NM.remainder(x) for x in W["loc"]})))
    ok("realism: town-named parishes pass the real-name check",
       all(not NM.clashes(t, NM.reference()) for t, L in zip(W["title"], W["loc"]) if t == L))
    ok("realism: dedications unique inside a locality", len({(t, L) for t, L in zip(W["title"], W["loc"])}) == 264)
    ok("realism: college names unique", len({x["name"] for x in W["sec"]}) == len(W["sec"]))
    notes = docs_text["notes"]
    ok("realism: notes carry no licence line and no row counts",
       "CC BY" not in notes and not re.search(r"\d rows\.", notes))
    with zipfile.ZipFile(os.path.join(target, P.FILES["guidelines"])) as z:
        nl = z.namelist()
        ok("realism: docx carries no template parts",
           not any(x.startswith("customXml/") or x in ("word/stylesWithEffects.xml", "docProps/thumbnail.jpeg")
                   for x in nl))
        ok("realism: docx declarations as Word writes them", all(b"<?xml version='1.0'" not in z.read(x) for x in nl))
    rd = open(os.path.join(target, P.FILES["road"])).read().splitlines()[1:]
    ok("realism: road file is not a full matrix", len(rd) < 5 * 264, len(rd))
    plan_hubs = {(P.hub_names(W)[W["plan"][i]], int(W["codes"][i])) for i in range(264)}
    road_pairs = {(r.split(",")[0], int(r.split(",")[1])) for r in rd}
    ok("road file carries every planned and directory pair", plan_hubs <= road_pairs and
       {(P.hub_names(W)[W["dir_hub"][i]], int(W["codes"][i])) for i in range(264)} <= road_pairs)
    hub_loc = {W["hubs"][h]["locality"] for h in A.HUBS}
    ok("realism: hubs are towns in the pack", hub_loc <= set(W["loc"]))
    for f in files:
        b = open(os.path.join(target, f), "rb").read()
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                b = b"".join(z.read(x) for x in z.namelist())
        for tag in (b"openpyxl", b"python-docx", b"ReportLab", b"matplotlib", b"\xe2\x80\x94", b"Williams"):
            ok("container scrubbed: %s in %s" % (tag[:12], f), tag not in b)
    bad = [(a, c) for a, b, c in RESULTS if not b]
    if bad:
        raise AssertionError("%d failed:\n" % len(bad) + "\n".join("%s: %s" % x for x in bad))
    return len(RESULTS), n_cells
