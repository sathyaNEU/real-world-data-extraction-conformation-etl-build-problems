"""Assertions for task450, run on the built pack (and on the generator's clean truth where the three rules ask for
it): the input gates, the three rules executed, the corridor under every method, weight and sample, the ladder's
named sets, the grid, the semantic fork rows SF1 to SF12, the asks and their cracker sheet, the separation line, the
filed sentences, the realism and hygiene sweeps, and the goldens against figures.json."""
import csv
import json
import os
import re
import sys

import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C       # noqa: E402
import docs as DC      # noqa: E402
import golden as G     # noqa: E402
import pack as P       # noqa: E402
import reader as RD    # noqa: E402
import world as W      # noqa: E402

RESULTS = []


def ok(cond, label, detail=""):
    RESULTS.append((bool(cond), label, detail))
    print("  %s  %-70s %s" % ("ok  " if cond else "FAIL", label, detail))


def names(L, cs):
    return sorted(L["directory"][c]["name"] for c in cs)


def doc_text(target):
    from pypdf import PdfReader
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = " ".join(" ".join(pg.extract_text() for pg in PdfReader(p).pages).split())
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            out[f] = " ".join(str(c) for ws in wb for row in ws.iter_rows(values_only=True) for c in row if c is not None)
    return out


def run(target, golden, world=None, meta_path=None):
    print("task450 checks")
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else None
    # ------------------------------------------------------------------------------------------ input gates ----
    rows = {f: sum(1 for _ in open(os.path.join(target, f))) - 1 for f in files if f.endswith(".csv")}
    ok(len(files) >= 10, "input gate: ten or more files", str(len(files)))
    describing = re.compile(r"dictionar|manifest|readme|read_me|field_?notes|field_?guide|codebook|schema|definition|"
                            r"extract_?notes|export_?notes|notes", re.I)
    ok(not [f for f in files if describing.search(f)], "section 3: no file named as a dictionary, manifest, readme "
       "or notes ships")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gate: three or more formats",
       ",".join(sorted({f.rsplit(".", 1)[1] for f in files})))
    ok(max(rows.values()) >= 25000, "input gate: one file of 25,000 rows or more", str(max(rows.values())))
    if meta:
        ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]),
           "input gate: two distractors named in metadata.json", ", ".join(meta["distractor_files"]))
        ok(not any(w in f for f in files for w in ("distract", "decoy", "unused")), "input gate: no file named as a distractor")
    # ------------------------------------------------------------------------------- the golden from the pack ----
    L = RD.load(target)
    # the shared items' stability: every standard screen sets aside the same three, written to one standard
    fl, st = C.drift_screens(L["S25"], L["S26"], L["anchor"])
    drift = sorted(p - 1 for p in world["F"]["drift"]) if world else fl["robust z"]
    for nm_, f_ in fl.items():
        ok(f_ == drift, "SF13 the %s screen sets aside the three shared items that moved" % nm_,
           ", ".join(str(j + 1) for j in f_))
    scr = [j for j in L["anchor"] if j not in drift]
    ok(scr == C.screened(L["S25"], L["S26"], L["anchor"]) and len(scr) == 22, "SF13 the link runs through 22 shared items")
    bank_tags = {int(r[6]) - 1: r[2] for r in RD.bank_rows(target) if r[6] and r[7]}
    ok({bank_tags[j] for j in drift} == {W.DRIFT_TAG[1]}, "R1 data-native: the three are written to one standard (TEKS %s)"
       % W.DRIFT_TAG[1])
    gap = st["gap"]
    moved = [g for j, g in zip(L["anchor"], gap) if j in drift]
    held = [g for j, g in zip(L["anchor"], gap) if j not in drift]
    ok(min(moved) > 4 * max(abs(g) for g in held), "SF13 the three moved more than four times any other shared item",
       "%.3f against %.3f" % (min(moved), max(abs(g) for g in held)))
    out, rg, info = C.methods(L["S25"], L["S26"], scr, rasch=True)
    r_by = {k: C.passing(f) for k, f in out.items()}
    r_hi = {k: C.passing(f, cut=C.HI) for k, f in out.items()}
    ok(set(r_by.values()) == {25} and set(r_hi.values()) == {25},
       "SF2 every common-item method through the 22 gives passing raw 25", "%d methods" % len(out))
    lo, hi, E = C.corridor(out, 25)
    ok(lo >= 0.20 and hi >= 0.20, "SF1 SF2 the corridor holds at both edges of the rounding band",
       "e(25) - 26.5 >= %.3f, 26.4167 - e(24) >= %.3f" % (lo, hi))
    one_more = set()
    for j in scr:
        oj, _, _ = C.methods(L["S25"], L["S26"], [k for k in scr if k != j], rasch=False)
        one_more |= {C.passing(f) for f in oj.values()}
    ok(one_more == {25}, "SF14 any one more shared item set aside: passing raw 25 on every method")
    blind, _, _ = C.methods(L["S25"], L["S26"], L["anchor"], rasch=True)
    r_blind = {k: C.passing(f) for k, f in blind.items()}
    ok(set(r_blind.values()) <= {23, 24} and len(set(r_blind.values())) >= 1,
       "R2 linked through all 25 shared items: passing raw 23 or 24 on every method",
       ", ".join("%s %d" % kv for kv in sorted(r_blind.items())))
    rgr = {k: C.passing(f) for k, f in rg.items()}
    ok(rgr["identity (the 2025 conversion)"] == 27, "R0 the 2025 conversion: passing raw 27")
    ok(rgr["random groups linear"] == 26 and rgr["random groups equipercentile"] == 26,
       "R1 random groups (linear and equipercentile): passing raw 26")
    tab = RD.campus_table(L, 25)
    gold = RD.designated(tab)
    GOLD = names(L, gold)
    ok(len(gold) == 15 and len(tab) == 54, "golden: 15 of 54 rated campuses designated", ", ".join(x[:-11] for x in GOLD))
    d27 = RD.designated(RD.campus_table(L, 27))
    d26 = RD.designated(RD.campus_table(L, 26))
    d24 = RD.designated(RD.campus_table(L, 24))
    d23 = RD.designated(RD.campus_table(L, 23))
    ok(len(d27) == 32 and set(gold) < set(d27), "R0 default path: 32 campuses, the golden's 15 among them")
    ok(len(d26) == 23 and set(gold) < set(d26), "R1 random groups: 23 campuses, the golden's 15 among them")
    ok(len(d24) == 13 and len(d23) == 6 and set(d23) < set(d24) < set(gold),
       "R2 linked through all 25: 13 or 6 campuses, inside the golden's 15")
    # the sample variants
    tested_fay = np.array([RD.fay_campus(L["spells"].get(L["xw"][t], [])) is not None for t in L["takers"]])
    blank25 = ((L["R25"] == "") | (L["R25"] == "*")).any(1)
    blank26 = ((L["R26"] == "") | (L["R26"] == "*")).any(1)
    for nm, a, b in (("2026 full-academic-year only", L["S25"], L["S26"][tested_fay]),
                     ("complete tests only", L["S25"][~blank25], L["S26"][~blank26])):
        o2, _, _ = C.methods(a, b, scr, rasch=True)
        l2, h2, _ = C.corridor(o2, 25)
        ok(l2 >= 0.15 and h2 >= 0.15 and {C.passing(f) for f in o2.values()} == {25},
           "SF3 linking sample %s: passing raw 25" % nm, "margins %.3f / %.3f" % (l2, h2))
    # Rasch with blanks as missing
    X25 = L["S25"].astype(float)
    X25[L["R25"] == ""] = np.nan
    X26 = L["S26"].astype(float)
    X26[L["R26"] == ""] = np.nan
    uni = [j for j in range(W.N_ITEMS) if j not in scr]
    n1, n2 = len(X25), len(X26)
    M = np.full((n1 + n2, W.N_ITEMS + len(uni)), np.nan)
    M[:n1, :W.N_ITEMS] = X25
    M[n1:, scr] = X26[:, scr]
    M[n1:, W.N_ITEMS:] = X26[:, uni]
    bh = C._jml(M)
    bX = bh[:W.N_ITEMS]
    bY = bh[:W.N_ITEMS].copy()
    bY[uni] = bh[W.N_ITEMS:]
    e = C._tse(bY, bX)(np.arange(W.N_ITEMS + 1))
    ok(e[25] >= C.HI + 0.15 and e[24] <= C.LO - 0.15, "SF2 Rasch concurrent with blanks as missing: passing raw 25",
       "e(25) %.3f, e(24) %.3f" % (e[25], e[24]))
    # ---------------------------------------------------------------------------------------------- the rungs ----
    Lw = RD.load(target, corrected=False)
    ow, _, _ = C.methods(Lw["S25"], Lw["S26"], C.screened(Lw["S25"], Lw["S26"], Lw["anchor"]), rasch=False)
    rw = C.passing(ow[G.GOLD_METHOD])
    dw = RD.designated(RD.campus_table(Lw, rw))
    ok(rw == 25 and names(L, set(gold) - set(dw)) == ["Vance Avenue Elementary"] and set(dw) < set(gold),
       "R2a SF4 the bank's original key: passing raw 25, Vance Avenue out", "r %d" % rw)
    da = RD.designated(RD.campus_table(L, 25, merge_closed=False))
    ok(names(L, set(da) - set(gold)) == ["Delgadillo Elementary"] and names(L, set(gold) - set(da)) == ["Tobar Elementary"],
       "R2b SF7 the closed campus rated apart: Delgadillo in, Tobar out")
    dt_ = RD.designated(RD.campus_table(L, 25, use_fay=False))
    ok(set(dt_) > set(gold) and "Vereda Elementary" in names(L, set(dt_) - set(gold)),
       "R2c every tested student counted: the set grows", ", ".join(names(L, set(dt_) - set(gold))))
    dn = RD.designated(RD.campus_table(L, 25, n_min=1))
    ok(names(L, set(dn) - set(gold)) == ["Vereda Elementary"] and set(gold) <= set(dn), "R2d SF8 the n-size rule skipped: Vereda added")
    # the grid: conversion x key x full academic year x closure x n-size
    import itertools
    cells, distinct = 0, set()
    hits = []
    for key_ok in (True, False):
        LL = L if key_ok else Lw
        oo, rr, _ = C.methods(LL["S25"], LL["S26"], C.screened(LL["S25"], LL["S26"], LL["anchor"]), rasch=False)
        ob, _, _ = C.methods(LL["S25"], LL["S26"], LL["anchor"], rasch=False)
        conv = {"common-item": C.passing(oo[G.GOLD_METHOD]), "random groups": C.passing(rr["random groups equipercentile"]),
                "2025 conversion": 27, "common-item through all 25": C.passing(ob[G.GOLD_METHOD])}
        for cv, r in conv.items():
            for fay, merge, nmin in itertools.product((True, False), (True, False), (W.N_MIN, 1)):
                st = RD.designated(RD.campus_table(LL, r, use_fay=fay, merge_closed=merge, n_min=nmin))
                cells += 1
                if st == gold:
                    hits.append((cv, key_ok, fay, merge, nmin))
                else:
                    distinct.add(tuple(st))
    ok(cells == 64 and hits == [("common-item", True, True, True, W.N_MIN)],
       "grid: of 64 cells only the golden's handling designates the golden's 15", "%d distinct wrong sets" % len(distinct))
    # separation: every rated campus two or more students from the line at 25 and at 27
    for r in (25, 27):
        t = RD.campus_table(L, r)
        gap = min(abs(k - W.LINE * n) for n, k in t.values())
        ok(gap >= 2.0, "SF9 every rated campus two or more students from the line at passing raw %d" % r, "%.1f" % gap)
    # ------------------------------------------------------------------------------------------ the fork rows ----
    def fay_variant(spells, last=False, exclusive=False):
        snap = W.SNAPSHOT
        cover = [c for c, a, b, code in spells if (a < snap if exclusive else a <= snap) and
                 b >= (W.WINDOW[1] if last else W.WINDOW[0])]
        if len(cover) != 1:
            return None
        c = cover[0]
        for c2, a, b, code in spells:
            if c2 != c and a <= (W.WINDOW[1] if last else W.WINDOW[0]) and b >= snap:
                return None
        return c
    base = [RD.fay_campus(L["spells"].get(L["xw"][t], [])) for t in L["takers"]]
    v1 = [fay_variant(L["spells"].get(L["xw"][t], []), last=True) for t in L["takers"]]
    v2 = [fay_variant(L["spells"].get(L["xw"][t], []), exclusive=True) for t in L["takers"]]
    ok(base == v1 and base == v2, "SF5 full academic year through the window's end, or the snapshot exclusive: same students")
    ok(all((r != "").any() for r, f in zip(L["R26"], base) if f is not None),
       "SF6 every tested full-academic-year student answered at least one item")
    D = L["directory"]
    ok(all("Elementary" in v["name"] for v in D.values()), "SF10 every campus in the directory is an elementary campus")
    raw_drop = ((L["R26"] == np.array(L["key26"], dtype=object)[None, :]) & (L["R26"] != "") & (L["R26"] != "*")).sum(1)
    ok((raw_drop == L["S26"].sum(1)).all(), "SF11 blanks and multiple marks score zero either way")
    stud = {}
    for t in L["takers"]:
        stud.setdefault(L["merges"].get(L["xw"][t], L["xw"][t]), []).append(t)
    ok(all(len(v) == 1 for v in stud.values()), "SF12 one 2026 test per person, merges applied", str(len(stud)))
    # ---------------------------------------------------------------------------------------------- the asks ----
    a25 = G.ask_2025(L)
    a25c = G.ask_2025_by_code(L)
    by_name = {}
    for c, v in D.items():
        by_name.setdefault(v["name"].upper(), []).append(c)
    ok(all(len(v) == 1 for v in by_name.values()) and all(RD.expand(n) in by_name for n in set(L["name25"])),
       "Ask A every 2025 campus name resolves to one directory campus")
    miss_a = [k for k in W.COMMUNITIES if a25c[k][0] != a25[k][0]] + \
             [k for k in W.COMMUNITIES if "%.1f" % (100.0 * a25c[k][1] / a25c[k][0]) != "%.1f" % (100.0 * a25[k][1] / a25[k][0])]
    ok(len(miss_a) == 10, "Ask A cracker (codes joined as 2026 numbers) misses all ten figures",
       " ".join("%s %d/%.1f" % (k, a25c[k][0], 100.0 * a25c[k][1] / a25c[k][0]) for k in W.COMMUNITIES))
    moved = sum(1 for c, nm in zip(L["code25"], L["name25"]) if D.get(c, {}).get("name", "").upper() != RD.expand(nm))
    ok(moved > 0.8 * len(L["code25"]), "Ask A device: most 2025 codes name another campus in 2026", "%d of %d" % (moved, len(L["code25"])))
    ok(all(c in D for c in set(L["code25"])), "Ask A device is silent: every 2025 code joins a directory campus")
    for k in W.COMMUNITIES:
        v = 100.0 * a25[k][1] / a25[k][0]
        ok(abs(v * 10 - round(v * 10)) <= 0.3 and round(v, 1) * 10 % 50 != 0, "Ask A %s share mid-bin, off round values" % k,
           "%.3f" % v)
    un = G.ask_untested(L)
    unc = G.ask_untested(L, merged=False)
    miss_b = [k for k in W.COMMUNITIES if un.get(k, 0) != unc.get(k, 0)] + \
             (["district"] if sum(un.values()) != sum(unc.values()) else [])
    ok(len(miss_b) == 6, "Ask B cracker (ids counted apart) misses all six figures",
       " ".join("%s %d/%d" % (k, unc.get(k, 0), un.get(k, 0)) for k in W.COMMUNITIES) +
       " district %d/%d" % (sum(unc.values()), sum(un.values())))
    tested_ids = {L["xw"][t] for t in L["takers"]}
    ok(not (set(L["merges"]) & tested_ids), "zero-count: no merged id has a 2026 test")
    ok(all(RD.fay_campus(L["spells"].get(m, [])) is None or m not in tested_ids for m in L["merges"]),
       "zero-count: no merged id enters the main population")
    # the main call without the asks' device files and columns
    L2 = dict(L)
    L2["merges"] = {}
    L2["code25"] = ["000"] * len(L["code25"])
    L2["name25"] = [""] * len(L["name25"])
    ok(RD.designated(RD.campus_table(L2, 25)) == gold, "separation: the call is unchanged without the merges and the 2025 campus fields")
    # --------------------------------------------------------------------------- the three rules, executed ----
    if world is not None:
        F, Aw, Bw = world["F"], world["A"], world["B"]
        S25 = C.score(Aw["resp"], F["key25"])
        idx = [i for i, s in enumerate(Bw["stu"]) if s["tested"]]
        S26 = C.score(Bw["resp"][idx], F["key26"])
        tested = [Bw["stu"][i] for i in idx]
        fay_of = [C.fay(s["spells"]) for s in tested]
        camp = [s["spells"][-1][0] for s in tested]
        shared = [p - 1 for p in W.ANCHOR_POS]
        held = [p - 1 for p in W.ANCHOR_POS if p not in F["drift"]]
        oc, rc, _ = C.methods(S25, S26, shared, rasch=False)
        oh, _, _ = C.methods(S25, S26, held, rasch=False)
        rate = lambda r: C.designated(C.campus_rates(S26.sum(1), camp, fay_of, r))
        easy = rate(C.passing(oc[G.GOLD_METHOD]))
        lower = rate(C.passing(rc["random groups equipercentile"]))
        right = rate(C.passing(oh[G.GOLD_METHOD]))
        ok(sorted(easy) == names(L, d23), "three rules: the analyst's easy route on the clean truth (common-item linking "
           "through every shared item) files the 6 (R2)")
        ok(sorted(lower) == names(L, d26), "three rules: the lower rung (random groups) on the clean truth files the 23 (R1)")
        ok(sorted(right) == GOLD, "three rules: the decisive step alone (the shared items that moved set aside), on the "
           "clean truth, files the golden's 15")
    # --------------------------------------------------------------------------------------- the documents ----
    T = doc_text(target)
    allt = " ".join(T.values())
    for f_, s_ in ((DC.RULES, "on the District Mathematics Assessment's reporting scale, which the district set on its 2025 grade-5 form, is 300 or above. Results from later forms are reported on the same scale."),
                   (DC.RULES, "enrolled at the campus on the fall snapshot date, 31 October 2025, and on every day after it through the first day of the testing window, 20 April 2026, and was enrolled at no other campus in that time."),
                   (DC.RULES, "The students of a campus that closed at the end of 2025-26 count with the campus that takes in its attendance zone."),
                   (DC.RULES, "A campus with fewer than ten full-academic-year students tested is not rated."),
                   (DC.RULES, "A rated elementary campus whose rate is under 40 per cent is designated."),
                   (DC.REPORT, "On that form a raw score converts to a scale score as 141 + 6 x raw score, reported as a whole number (Table 4)."),
                   (DC.REPORT, "On the 2025 form it lies at a raw score of 26.5."),
                   (DC.REPORT, "The conversion applies to raw scores on the 2025 form only."),
                   (DC.REPORT, "An answer left blank, whether omitted or not reached, and an answer with more than one choice marked score zero.")):
        ok(s_ in T[f_], "pin filed once: %s" % s_[:60])
        ok(allt.count(s_) == 1, "pin stated once in the pack: %s" % s_[:40])
    ok("The conversion applies to raw scores on the 2025 form only." in T[DC.REPORT] and len(d27) == 32,
       "SF12 the 2025 conversion on the 2026 raw scores files 32 and the report scopes it to the 2025 form only")
    low = allt.lower()
    for word in ("anchor", "equat", "common item", "common-item", "linking", "link the", "shared item", "random group",
                 "nonequivalent", "non-equivalent", "cohort", "carried over", "renumber", "duplicate id", "ghost",
                 "drift", "screen", "invarian", "differential item", "curriculum"):
        ok(word not in low, "R3 no document names the decisive step or a device (%s)" % word)
    # -------------------------------------------------------------------------------------- realism, hygiene ----
    dates = []
    with open(os.path.join(target, P.FILES["resp26"])) as fh:
        rd = csv.DictReader(fh)
        mx = max(r["submitted_at"] for r in rd)
    ok(mx[:10] <= W.WINDOW[1].isoformat(), "realism: every 2026 answer submitted inside the window", mx)
    with open(os.path.join(target, P.FILES["merges"])) as fh:
        mm = [r["merged_on"] for r in csv.DictReader(fh)]
    ok(max(mm) <= W.PULL.isoformat(), "realism: nothing dated after the pull", max(mm))
    cnames = [v["name"] for v in D.values()]
    ok(len(cnames) == len(set(cnames)) == 56, "realism: 56 distinct campus names")
    for f_ in files:
        b = open(os.path.join(target, f_), "rb").read()
        ok(not re.search(rb"(?i)reportlab|openpyxl|python-docx|matplotlib", b), "H1 no writer's name in %s" % f_)
        ok("—".encode() not in b, "standing rule: no em dash in %s" % f_)
    for f_ in os.listdir(golden):
        import zipfile
        with zipfile.ZipFile(os.path.join(golden, f_)) as z:
            body = b" ".join(z.read(n) for n in z.namelist())
        ok(not re.search(rb"(?i)openpyxl|python-docx|matplotlib", body), "H1 no writer's name in golden %s" % f_)
        ok("—".encode() not in body, "standing rule: no em dash in golden %s" % f_)
    # ------------------------------------------------------------------------------------- the deliverables ----
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    ok(fig["designated"] == sorted(GOLD, key=lambda n: tab[[c for c, v in D.items() if v["name"] == n][0]][1] /
                                   tab[[c for c, v in D.items() if v["name"] == n][0]][0]),
       "figures.json: the designated campuses")
    wb = openpyxl.load_workbook(os.path.join(golden, G.XLSX), data_only=True)
    ws = wb["Campus results"]
    got = {r[1]: (r[3], r[4], r[5], r[6]) for r in ws.iter_rows(min_row=4, values_only=True) if r[0]}
    ok(len(got) == 54 and all(got[D[c]["name"]][:2] == tab[c] for c in tab), "xlsx: every rated campus's counts")
    ok(sorted(n for n, v in got.items() if v[3] == "Yes") == GOLD, "xlsx: the designated campuses marked")
    ws2 = wb["2025 by community"]
    g2 = {r[0]: (r[1], r[2]) for r in ws2.iter_rows(min_row=4, values_only=True)}
    ok(all(g2[k][0] == a25[k][0] and "%.1f" % g2[k][1] == "%.1f" % (100.0 * a25[k][1] / a25[k][0]) for k in W.COMMUNITIES),
       "xlsx: Ask A figures")
    ws3 = wb["No 2026 result"]
    g3 = {r[0]: r[1] for r in ws3.iter_rows(min_row=4, values_only=True)}
    ok(all(g3[k] == un.get(k, 0) for k in W.COMMUNITIES) and g3["District"] == sum(un.values()), "xlsx: Ask B figures")
    from docx import Document
    doc = Document(os.path.join(golden, G.DOCX))
    body = " ".join(p.text for p in doc.paragraphs) + " " + " ".join(c.text for t in doc.tables for r in t.rows for c in r.cells)
    ok(all(n in body for n in GOLD), "docx: every designated campus named")
    ok(all(fig["designated_rates"][n] in body for n in GOLD), "docx: every designated campus's share")
    ok(len(doc.inline_shapes) == 1, "docx: the campus chart is in the memo")
    # ------------------------------------------------------------------------------------------- distractors ----
    if meta:
        ok(set(meta["distractor_files"]) == {P.FILES[k] for k in P.DISTRACTORS}, "distractors: metadata names both")
    nfail = sum(1 for c, _, _ in RESULTS if not c)
    print("task450 checks: %d passed%s" % (len(RESULTS) - nfail, (", %d FAILED" % nfail) if nfail else ""))
    if nfail:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    TASK = os.path.dirname(HERE)
    run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), meta_path=os.path.join(TASK, "metadata.json"))
