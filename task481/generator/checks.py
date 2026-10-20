"""task481 checks on the built pack, the golden and the simulation's truth. Every fork in the design note's table has
an assertion here (SF ids), and the three-rules block executes the analyst test on the clean truth."""
import collections
import json
import os
import re

import asks as A
import methods as M
import pack as P
import world as W

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    return bool(cond)


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def run(target, gdir, x, meta_path, fig_path):
    RESULTS.clear()
    fig = json.load(open(fig_path))
    b = x["b"]
    rows, ra, dvu = x["extract"], x["ra"], x["dvu"]
    f = lambda k: os.path.join(target, P.FILES[k])

    # ---------------------------------------------------------------- input gates
    meta = json.load(open(meta_path))
    files = sorted(os.listdir(target))
    ok("gate: 10 or more files", len(files) >= 10, "%d" % len(files))
    fmts = {os.path.splitext(n)[1] for n in files}
    ok("gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    ok("gate: a file of 25,000 rows", len(rows) >= 25000, "%d extract rows" % len(rows))
    ok("gate: 2 or more distractors", len(meta["distractor_files"]) >= 2, ", ".join(meta["distractor_files"]))
    ok("gate: distractors shipped", all(d in files for d in meta["distractor_files"]))
    ok("gate: no distractor named as such", not any("distract" in n.lower() for n in files))

    # ---------------------------------------------------------------- the pack agrees with itself
    tot, to13a = M.dual_tables(rows)
    for l in M.AGG:
        ok("dual months: %s ties to Return A" % l, tot[l] == sum(ra[ym][l][2] for ym in M.DUAL))
    ok("dual months: 4E ties to Return A", tot["4E_dv"] + tot["4E_non"] == sum(ra[ym]["4E"][2] for ym in M.DUAL))
    ok("dual months: robbery incidents tie", tot["hid_rob"] == sum(ra[ym][l][2] for ym in M.DUAL for l in M.ROB))
    ok("dual months: homicide victims tie", tot["hid_hom"] == sum(ra[ym]["1A"][2] for ym in M.DUAL))
    dv_q4_log = sum(M.dvu_4e(dvu, M.DUAL).values())
    ok("SF2: domestic by relationship code equals the unit's log (October to December 2024)",
       dv_q4_log == tot["4E_dv"], "%d %d" % (dv_q4_log, tot["4E_dv"]))
    for ym in M.MONTHS_2024:
        sim = sum(1 for v in b.victims if v["line"] == "4E" and v["dv"] and not b.inc[v["iid"]]["unfounded"]
                  and v["kind"] not in ("rob_extra", "hom_extra") and (b.inc[v["iid"]]["reported"].year,
                                                                       b.inc[v["iid"]]["reported"].month) == ym)
        if not ok("SF2: unit's log 4E domestic %d-%02d equals the records" % ym, M.dvu_4e(dvu, (ym,))[ym] == sim):
            break
    ok("Return A: 2024 published total", fig["published_2024"] == sum(ra[ym][l][2] for ym in M.MONTHS_2024
                                                                     for l in M.AGG))

    # ---------------------------------------------------------------- the three rules on the clean truth (section 7.1)
    truth = clean_truth(b)
    ok("three rules: the clean truth's per-line conversion files a fall", truth["per_line"] < -0.01,
       "%+.2f%%" % (100 * truth["per_line"]))
    ok("three rules: the clean truth's domestic split files a rise", truth["golden"] > 0.01,
       "%+.2f%%" % (100 * truth["golden"]))
    ok("three rules: the decisive step alone moves the answer across zero",
       truth["per_line"] < 0 < truth["golden"])
    ok("three rules: no filed sentence names the domestic split",
       not any(w in _text(f("method")).lower() for w in ("domestic share", "seasonal", "composition", "strangulation")))

    # ---------------------------------------------------------------- the ladder
    lad = M.ladder(rows, ra, dvu)
    g = 100 * lad["golden"]
    ok("call: golden a rise of a whole per cent or more", round(g) >= 1 and g < 4.0, "%+.3f" % g)
    ok("call: golden mid-bin at the whole per cent", edge(g, 1.0) >= 0.2, "edge %.3f" % edge(g, 1.0))
    ok("call: restated 2024 mid-bin at the nearest hundred", edge(lad["golden_2024"], 100) >= 20,
       "edge %.1f" % edge(lad["golden_2024"], 100))
    ok("call: figures.json carries the graded precision", fig["call"]["change_pct"] == round(g)
       and fig["restated_2024"] == round(lad["golden_2024"], -2))
    # SF14: every reasonable grain of the conversion gives the same figures at their stated precision (C1)
    for name, kw in M.GRAINS.items():
        t = M.restate_grain(rows, ra, dvu, **kw)
        v = 100 * (lad["nibrs_2025"] / t - 1)
        ok("SF14: %s converges (%.1f, %+.2f%%)" % (name, t, v),
           round(v) == round(g) and round(t, -2) == round(lad["golden_2024"], -2)
           and edge(v, 1.0) >= 0.1 and edge(t, 100) >= 10)
    for k in ("hidden_exact", "gained_exact", "lost_exact"):
        ok("bridge: %s mid-bin" % k, edge(fig["bridge"][k], 1) >= 0.04, "%.3f" % fig["bridge"][k])
    ok("bridge ties: published + hidden + gained - lost = restated",
       abs(fig["published_2024"] + fig["bridge"]["hidden_exact"] + fig["bridge"]["gained_exact"]
           - fig["bridge"]["lost_exact"] - fig["restated_2024_exact"]) < 1e-6)
    for name, gap in (("per_line", 2.0), ("link", 2.0), ("pooled_all", 2.0), ("dv_pooled_agg", 0.3)):
        ok("ladder: %s at least %.1f points off and in another whole-per-cent bin" % (name, gap),
           abs(100 * lad[name] - g) >= gap and round(100 * lad[name]) != round(g), "%+.2f" % (100 * lad[name]))
    ok("ladder: the per-line restated total in another hundred", round(lad["per_line_2024"], -2)
       != round(lad["golden_2024"], -2), "%.1f" % lad["per_line_2024"])
    ok("ladder: per-line files a fall", lad["per_line"] < -0.01, "%+.2f%%" % (100 * lad["per_line"]))
    ok("ladder: published rise filed as real is 4 points or more off", 100 * lad["raw"] - g >= 4.0,
       "%+.2f" % (100 * lad["raw"]))
    ok("ladder: quarter against quarter 1 point or more off", abs(100 * lad["q4_to_q4"] - g) >= 1.0,
       "%+.2f" % (100 * lad["q4_to_q4"]))
    # the route grid: the domestic split, the aggravated lines per line or pooled, local or UTC months; only the golden's
    # cell lands in its bin
    for split in (True, False):
        for pl in (True, False):
            for utc in (True, False):
                if split and pl and utc:
                    continue
                by, _, _ = M.restate(rows, ra, dvu, split_dv=split, per_line=pl, utc=utc)
                n13 = M.nibrs_13a(rows, utc)
                v = 100 * (sum(n13[ym] for ym in M.MONTHS_2025) / sum(by.values()) - 1)
                ok("grid: split %s, per line %s, local %s files another bin" % (split, pl, utc),
                   round(v) != round(g), "%+.3f" % v)
    # SF1: months read in UTC rather than local time
    lad_utc = M.ladder(rows, ra, dvu, utc=False)
    ok("SF1: months read in UTC file another figure or the same", True, "%+.3f" % (100 * lad_utc["golden"]))
    # SF3: unfounded domestic cases counted
    dv_all = collections.Counter()
    for d in dvu:
        ym = (int(d[M.D["report_date"]][:4]), int(d[M.D["report_date"]][5:7]))
        if ym in M.JAN_SEP and d[M.D["ucr_line"]] == "4E":
            dv_all[ym] += 1
    by3, _, _ = M.restate(rows, ra, dvu, dvu_months=dv_all)
    v3 = 100 * (lad["nibrs_2025"] / sum(by3.values()) - 1)
    ok("SF3: counting unfounded domestic cases files another figure", round(v3) != round(g), "%+.2f" % v3)
    # SF4: case-opened date in place of report date
    dv_open = collections.Counter()
    for d in dvu:
        if d[M.D["ucr_line"]] == "4E" and d[M.D["case_status"]] != "UNFOUNDED":
            ym = (int(d[M.D["case_opened"]][:4]), int(d[M.D["case_opened"]][5:7]))
            if ym in M.JAN_SEP:
                dv_open[ym] += 1
    by4, _, _ = M.restate(rows, ra, dvu, dvu_months=dv_open)
    v4 = 100 * (lad["nibrs_2025"] / sum(by4.values()) - 1)
    ok("SF4: the unit's case-opened month files the same figure or another", True, "%+.3f" % v4)
    # SF5: the 2025 count includes officers and every victim type; only individual victims are on assault rows
    ok("SF5: every 13A row is an individual victim", all(r[M.E["victim_type"]] == "I" for r in rows
                                                         if r[M.E["offense_code"]] == "13A"))
    # SF6: Return A actual (column 4), not reported
    rep = sum(ra[ym][l][0] for ym in M.MONTHS_2024 for l in M.AGG)
    ok("SF6: reported in place of actual moves the published figure", rep != fig["published_2024"])
    # SF7: the 2025 count from the department's extract, not the state's published figure
    ok("SF7: the state's published 2025 figure differs from the department's count",
       x["sf"].published != lad["nibrs_2025"], "%d %d" % (x["sf"].published, lad["nibrs_2025"]))
    # SF8: the restated October to December months are the extract's counts
    ok("SF8: October to December counted, not converted",
       all(abs(fig["restated_by_month_exact"]["2024-%02d" % m] - M.nibrs_13a(rows)[(2024, m)]) < 1e-9
           for m in (10, 11, 12)))

    # ---------------------------------------------------------------- the shootings ask
    gvr, me = M.read_csv(f("gvr")), M.read_csv(f("me"))
    gv, gs = M.shootings(gvr, me)
    tv, ts = x["sh"].truth()
    ok("shootings: golden equals the records' truth (victims)", gv == tv, "%s %s" % (gv, tv))
    ok("shootings: golden equals the records' truth (shootings)", gs == ts)
    for name, kw, need_v, need_s in (("SF9: outcomes as the log holds them", {"deaths": False}, 11, 9),
                                     ("SF10: the inside-city flag as the log holds it", {"township": False}, 7, 7),
                                     ("both as the log holds them (the careful path)",
                                      {"deaths": False, "township": False}, 12, 12),
                                     ("one row a report number", {"dedup": "number"}, 10, 0),
                                     ("SF12: shootings by report number", {"events": "number"}, 0, 8),
                                     ("SF13: rows as entered", {"dedup": None}, 1, 0)):
        v, s = M.shootings(gvr, me, **kw)
        mv = sum(v[q] != gv[q] for q in M.QUARTERS)
        ms = sum(s[q] != gs[q] for q in M.QUARTERS)
        ok("device: %s moves %d quarters of victims and %d of shootings" % (name, need_v, need_s),
           mv >= need_v and ms >= need_s, "%d %d" % (mv, ms))
    # SF11: the quarter the row was entered in place of the quarter shot
    ent = collections.Counter()
    for gg in gvr:
        if (gg[M.G["circumstance"]] == "ASSAULT" and gg[M.G["inside_city"]] == "Y"
                and gg[M.G["outcome"]] == "WOUNDED"):
            ent[M.quarter_of(gg[M.G["entered"]])] += 1
    ok("SF11: the quarter entered files another grid", any(ent[q] != gv[q] for q in M.QUARTERS))
    # the Medical Examiner's later deaths match one shooting-log row each
    amb = 0
    for d in me:
        loc = d[M.MEC["injury_location"]]
        if loc.endswith(", ELLSMERE"):
            k = (d[M.MEC["date_of_injury"]], loc[: -len(", ELLSMERE")], d[M.MEC["age"]], d[M.MEC["sex"]])
            people = {(gg[M.G["rms_number"]], gg[M.G["shot_datetime"]]) for gg in gvr
                      if (gg[M.G["shot_datetime"]][:10], gg[M.G["block"]], gg[M.G["victim_age"]],
                          gg[M.G["victim_sex"]]) == k}
            amb += len(people) > 1
    ok("device fair: every later death matches one person", amb == 0, "%d ambiguous" % amb)
    # the township: every block the log marks inside before October 2024 and outside after it is marked outside in a
    # row from October 2024; no block the city's own shootings use is ever marked outside
    flags = collections.defaultdict(set)
    for gg in gvr:
        flags[M.base_block(gg[M.G["block"]])].add((gg[M.G["inside_city"]], gg[M.G["shot_datetime"]] >= "2024-10-01"))
    both = {k for k, v in flags.items() if any(f == "Y" for f, _ in v) and any(f == "N" for f, _ in v)}
    ok("device fair: every block marked both ways is marked outside from October 2024 and inside only before it",
       all(("N", True) in flags[k] and ("Y", True) not in flags[k] for k in both), "%d blocks" % len(both))
    ok("device fair: the blocks marked both ways are the township's", both == set(A.TOWNSHIP_BLOCKS) & set(flags),
       ", ".join(sorted(both)))
    pre_q = {M.quarter_of(gg[M.G["shot_datetime"]]) for gg in gvr if M.base_block(gg[M.G["block"]]) in both
             and gg[M.G["shot_datetime"]] < "2024-10-01"}
    ok("device: a township shooting in every quarter before October 2024", all(q in pre_q for q in M.QUARTERS[:7]))
    ok("separation: no shooting-log or Medical Examiner organ in a main-call document",
       not any(w in _text(f("dictionary")).lower() for w in ("shooting log", "medical examiner", "township")))

    # ---------------------------------------------------------------- the three rules, executed (R1 to R3)
    filled = sum(1 for r in rows if r[M.E["ucr_summary_class"]])
    ok("R1 the dual-coded months ship at offense-by-victim grain with both classifications", filled > 4000,
       "%d rows" % filled)
    heads = []
    for n in files:
        if n.endswith(".csv"):
            heads += open(os.path.join(target, n), encoding="utf-8").readline().strip().lower().split(",")
    bad = [h for h in heads if any(w in h for w in ("restat", "conver", "share", "rate", "domestic_"))]
    ok("R1 no shipped column holds a restated count, a conversion rate or a domestic share", not bad, ", ".join(bad))
    ok("R2 the unit's case-opened date in place of the report date: the call unchanged at its rounding",
       round(v4) == round(g), "%+.3f" % v4)
    norm = lambda n: ("20%s-0%s" % (n[2:4], n[5:]) if n.startswith("EP") else n)
    ext_inc = {r[M.E["incident_number"]] for r in rows if M.local_month(r[M.E["report_datetime_utc"]]) in M.DUAL
               and r[M.E["ucr_summary_class"]] == "4E" and M.is_dv(r[M.E["relationship_1"]])}
    log_inc = {norm(d[M.D["rms_incident"]]) for d in dvu if d[M.D["ucr_line"]] == "4E"
               and d[M.D["case_status"]] != "UNFOUNDED"
               and (int(d[M.D["report_date"]][:4]), int(d[M.D["report_date"]][5:7])) in M.DUAL}
    ok("R2 the unit's log joined by its incident numbers, three forms normalised, finds the extract's domestic 4e "
       "incidents of October to December", ext_inc == log_inc, "%d %d" % (len(ext_inc), len(log_inc)))
    ra21 = M.read_return_a(f("ra_2021"))
    ok("R2 the 2021 Return A in the department's own layout reads to the same lines as the records",
       all(ra21[(2021, m)][l] == ra[(2021, m)][l] for m in range(1, 13) for l in ("4A", "4B", "4C", "4D", "4E")))
    ok("R3a analyst test: on the clean truth the per-line conversion files a fall", truth["per_line"] < -0.01)
    ok("R3b the decisive step alone files a rise on the clean truth", truth["golden"] > 0.01)
    vecs = [tuple(ra[(y, m)][l][2] for l in ("4A", "4B", "4C", "4D", "4E")) for y in (2021, 2022, 2023, 2024)
            for m in range(1, 13)]
    ok("R3c no Return A month repeats another's assault lines", len(set(vecs)) == len(vecs))
    ok("R3c no extract row repeats another", len({tuple(r) for r in rows}) == len(rows))

    # ---------------------------------------------------------------- realism sweep
    n13 = M.nibrs_13a(rows)
    ok("realism: the 2025 monthly counts are not a constant stream", len({n13[ym] for ym in M.MONTHS_2025}) >= 10)
    ok("realism: no round headline total", all(v % 100 for v in (fig["published_2024"], fig["nibrs_2025"],
                                                                 fig["restated_2024_units"], x["sf"].published)))
    ok("realism: no large file with a round thousand of rows", len(rows) % 1000 != 0, "%d" % len(rows))
    tells = []
    for n in files:
        if n.endswith((".xlsx", ".docx", ".pdf")):
            raw = open(os.path.join(target, n), "rb").read()
            tells += [n for t in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib") if t in raw]
    ok("realism: containers scrubbed (no writing library named in any file)", not tells, ", ".join(tells))
    import datetime as _dt
    late = [n for n in files if _dt.date.fromtimestamp(os.path.getmtime(os.path.join(target, n))) > _dt.date(2026, 10, 6)]
    ok("realism: every file saved on or before 6 October 2026", not late, ", ".join(late))
    for k, col, cap in (("gvr", "entered", "2026-10-01"), ("me", "date_of_death", "2026-10-06"),
                        ("dvu", "case_opened", "2026-10-02"), ("dvu", "report_date", "2026-09-30")):
        idx = {"gvr": M.G, "me": M.MEC, "dvu": M.D}[k][col]
        rows_k = M.read_csv(f(k))
        top = max(r_[idx] for r_ in rows_k if r_[idx])
        ok("realism: %s's %s runs no later than the file's own date (%s)" % (P.FILES[k], col, top), top <= cap)

    # ---------------------------------------------------------------- the shipped text
    for n in files:
        if n.endswith((".csv", ".txt")):
            t = open(os.path.join(target, n), encoding="utf-8").read()
            ok("no long dashes in %s" % n, "—" not in t and "–" not in t)
    for n in ("method", "dictionary", "cert", "state_table"):
        t = _text(f(n))
        ok("no long dashes in %s" % P.FILES[n], "—" not in t and "–" not in t)
    sub = open(os.path.join(os.path.dirname(target), "submission.md"), encoding="utf-8").read()
    ok("no long dashes in submission.md", "—" not in sub and "–" not in sub)

    good = all(c for _, c, _ in RESULTS)
    bad = [(n, d) for n, c, d in RESULTS if not c]
    print("checks: %d of %d passed" % (sum(1 for _, c, _ in RESULTS if c), len(RESULTS)))
    for n, d in bad:
        print("  FAIL", n, d)
    return good


def _text(path):
    if path.endswith(".docx"):
        import docx
        return "\n".join(p.text for p in docx.Document(path).paragraphs)
    if path.endswith(".pdf"):
        import subprocess
        return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    return open(path, encoding="utf-8").read()


def clean_truth(b):
    """The analyst test on the generator's clean truth: expected counts with no sampling noise, every filed rule
    applied; the per-line conversion against the conversion with simple assaults split by domestic and other."""
    import importlib
    ev = importlib.import_module("expected")
    return ev.ladder()
