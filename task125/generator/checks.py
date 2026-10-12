"""Assertions on the built pack and goldens: the input gates, the golden path recomputed from the files equal to the
simulation's, every rung of the ladder at its named wrong answer and outside the tolerance, the semantic forks (SF1
to SF9), the separation line between the call and the asks, each ask device moving every region, the documents'
silence on the devices, and the goldens agreeing with figures.json."""
import json
import os
import re
import zipfile

import numpy as np
import openpyxl
import pandas as pd

import analysis as AN
import asks as A
import build as B
import models as M
import records as R
import world as W

N = [0]


def ok(cond, what):
    N[0] += 1
    if not cond:
        raise AssertionError(what)


def run(target, golden, world, meta_path):
    I = world["intakes"]
    d = AN.load(target)
    fig = json.load(open(os.path.join(os.path.dirname(golden), "generator", "figures.json")))
    tol_u, tol_e = float(fig["gap_tolerance_points"]["unemployment"]), float(fig["gap_tolerance_points"]["employment"])

    # ---- input gates
    meta = json.load(open(meta_path))
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    ok(meta["input_gates"]["largest_file_rows"] >= 25000, "a file of 25,000 rows or more")
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "two distractors")
    for f in meta["distractor_files"]:
        ok("distract" not in f, "distractor not named as such")
    src = "".join(open(os.path.join(os.path.dirname(__file__), m)).read() for m in ("analysis.py", "asks.py", "deliver.py"))
    for f in meta["distractor_files"]:
        ok(f not in src, "the solution never reads " + f)

    # ---- the golden path from the files equals the simulation's
    gf, gs = AN.gap_path(d), M.gap_path(I)
    for a, b in zip(gf, gs):
        ok(abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9, "file path equals simulation path")
    h = AN.headline(d)
    ok(abs(h["pub_q3"][0] - AN.published(d, (2026, 3), reweight="rake")[0]) < 2e-4, "file weights reproduce the raking")
    for q in W.qrange(W.FIRST_Q, W.LAST_Q):
        df = AN.quarter(d, q)
        ok(np.max(np.abs(df["weight"].to_numpy() - AN.rake(df, d["controls"][W.qlabel(q)]))) < 0.0051, "weights re-rake")

    # ---- the ladder, every rung at its named wrong answer, outside the tolerance in every 2027 quarter
    r0 = AN.gap_path(d, carry="wave1")
    r1 = AN.constant_gap_path(d)
    r2 = AN.gap_path(d, reweight="keep")
    for k in (2, 3, 4):
        ok(r0[k] == (0.0, 0.0), "rung 0 files zero from January 2027")
        ok(abs(gf[k][0] - r0[k][0]) > tol_u and abs(gf[k][1] - r0[k][1]) > tol_e, "rung 0 off the golden, %d" % k)
        ok(abs(gf[k][0] - r1[k][0]) > tol_u and abs(gf[k][1] - r1[k][1]) > tol_e, "rung 1 off the golden, %d" % k)
    for k in range(5):
        ok(abs(gf[k][1] - r2[k][1]) > tol_e, "rung 2 (weights kept) off the golden employment gap, %d" % k)
        ok(gf[k][0] > 0 and gf[k][1] < 0, "the gap's sign every quarter")
    ok(abs(gf[1][0] - r0[1][0]) > tol_u, "rung 0 off the golden in October to December")
    ok(max(range(5), key=lambda k: gf[k][0]) == 1, "the gap peaks in October to December 2026")
    ok(gf[4][0] > tol_u, "the gap is still over the tolerance in July to September 2027")
    world["ladder"] = dict(golden=gf, rung0=r0, rung1=r1, rung2=r2)

    # ---- semantic forks
    # SF1: the six-visit rate is the published estimator on six visits, the estimand of the prompt
    ok("six visits all along" in open(os.path.join(os.path.dirname(golden), "prompt.txt")).read(), "SF1 prompt wording")
    # SF2, SF3: definitions in the methods note, 15 and over
    meth = _pdf_text(os.path.join(target, B.FILES["methods"]))
    ok("population aged 15 and over" in meth and "labour force (employed plus unemployed)" in meth, "SF2 SF3 definitions")
    # SF4: the template quarter is the last full quarter before the change, filed once
    ok("last full quarter collected before it" in meth, "SF4 the methods note's assessment sentence")
    ok(W.qnext(W.TEMPLATE_Q) == W.LIMIT_FROM, "SF4 April to June 2026 is the last full quarter before July")
    # SF5: the households a three-visit cap would not have recruited are those interviewed at visits 4 to 6
    calls = d["calls"]
    q3c = calls[calls["intake"] == "2026Q3"]
    ok(q3c["visit_no"].max() == 3, "SF5 the capped intake has no fourth visit")
    pre = calls[(calls["intake"] < "2026Q3") & (calls["outcome"] == 110)]
    ok(pre["visit_no"].max() == 6 and (pre["visit_no"] >= 4).mean() > 0.12, "SF5 visits 4 to 6 interviewed before")
    tq = AN.quarter(d, W.TEMPLATE_Q)
    ok(tq["interview_visit"].notna().all(), "SF5 every template household has its interview visit")
    # SF6: re-raking is the methods note's estimator (rung 2 keeps weights)
    ok("Every estimate the office publishes from the HLS uses the raked weights" in meth, "SF6 raking filed")
    # SF7: six visits from January: no intake after 2026Q4 is capped
    ok(not W.capped((2027, 1)) and W.capped((2026, 4)), "SF7 the cap's intakes")
    # SF8: the real change is between April to June and July to September
    ok(abs(h["rise_u"] - (h["pub_q3"][0] - h["pub_q2"][0])) < 1e-12, "SF8")
    # SF9: rounding from unrounded estimates
    ok(fig["labour_market_share_of_rise_points"] == "%.2f" % round(h["real_u"], 2), "SF9 rounding")

    # ---- separation line: no device row in the main call's population
    rows = world["call_rows"]
    replays = [r for r in rows if r.get("_replay")]
    ok(len(replays) > 0 and all(r["outcome"] != 110 and r["intake"] == "2026Q3" for r in replays),
       "replays only on non-interview calls of the July to September 2026 intake")
    main_intakes = {W.qlabel(W.qnext(W.TEMPLATE_Q, -k)) for k in range(5)}
    ok(not any(r["intake"] in main_intakes for r in replays), "no replay in the template's intakes")
    inter = calls[calls["outcome"] == 110]
    ok(not inter.duplicated(["serial9"]).any(), "one interview row per address")
    # the main path never reads person_no or actual_hours: shuffling them leaves the path unchanged
    d2 = dict(d)
    p2 = d["person"].copy()
    p2["person_no"] = p2["person_no"].sample(frac=1, random_state=1).to_numpy()
    p2["actual_hours"] = 0.0
    d2["person"] = p2
    ok(AN.gap_path(d2) == gf, "the main path is blind to person numbers and hours")

    # ---- the asks: each device moves every region; the over-correction too
    a = world["deliver"]["asks"]
    for g in W.RCODES:
        v = a["visits"]
        ok(v["rows"][g] != v["golden"][g] and v["serial_day"][g] != v["golden"][g], "ask 1 device, " + g)
        f = a["flows"]
        ok("%.2f" % f["person_no"][g] != "%.2f" % f["golden"][g], "ask 2 device, " + g)
        ok("%.2f" % f["serial_only"][g] != "%.2f" % f["golden"][g], "ask 2 fan-out, " + g)
        hh = a["hours"]
        ok("%.1f" % hh["raw"][g] != "%.1f" % hh["golden"][g], "ask 3 device, " + g)
        ok("%.1f" % hh["all_converted"][g] != "%.1f" % hh["golden"][g], "ask 3 over-correction, " + g)
    # the devices' internal evidence exists and nothing else marks them
    p = d["person"]
    cati = p[(p["mode"] == "CATI") & p["actual_hours"].notna()]["actual_hours"]
    capi = p[(p["mode"] == "CAPI") & p["actual_hours"].notna()]["actual_hours"]
    ok(((cati * 100).round() % 100).max() <= 59, "telephone hours never past .59")
    ok(set(((capi * 100).round() % 100).astype(int)) <= {0, 25, 50, 75}, "face-to-face hours in quarter hours")
    dup = q3c.duplicated(["serial", "visit_no"], keep=False)
    ok(dup.sum() == 2 * len(replays), "each replay shares serial and visit number with its original")
    ok(not q3c.duplicated(["record_id"]).any(), "record ids unique")

    # ---- documents silent on the devices; no em dash anywhere
    texts = {f: (_pdf_text(os.path.join(target, f)) if f.endswith(".pdf") else
                 open(os.path.join(target, f), encoding="utf-8").read())
             for f in files if f.endswith((".pdf", ".md", ".json"))}
    for f, t in texts.items():
        for w_ in ("minutes", "oldest", "re-sent", "resent", "re-sync", "duplicate", "h.mm"):
            ok(w_ not in t.lower(), "%s silent on %s" % (f, w_))
        ok("—" not in t and "–" not in t, "no dash in " + f)

    # ---- release table reproduces the microdata
    wb = openpyxl.load_workbook(os.path.join(target, R.RELEASE), data_only=True)
    t1 = [r for r in wb["Table 1"].iter_rows(min_row=4, values_only=True) if r[0]]
    for (q, (u, e)), r in zip([(q, AN.published(d, q)) for q in W.qrange(W.FIRST_Q, W.TEMPLATE_Q)], t1):
        ok(abs(r[1] - u) < 0.051 and abs(r[2] - e) < 0.051, "release table %s" % W.qlabel(q))

    # the published hours referee: only the converted telephone hours reproduce it, every quarter
    ph = d["person"]
    emp = ph[ph["ilo_status"] == 1]
    conv = emp["actual_hours"].where(emp["mode"] != "CATI", emp["actual_hours"].apply(A.to_decimal))
    for q, r in zip(W.qrange(W.FIRST_Q, W.TEMPLATE_Q), t1):
        m = (emp["quarter"] == W.qlabel(q)).to_numpy()
        good = (emp["weight"][m] * conv[m]).sum() / 1000
        raw = (emp["weight"][m] * emp["actual_hours"][m]).sum() / 1000
        ok(abs(r[5] - good) < 0.051 and abs(r[5] - raw) > 50, "release hours referee %s" % W.qlabel(q))
    ok("a visit is identified by the address serial and its visit number" in meth, "ask 1 reading pin")
    ok("People not interviewed in the second quarter are left out" in meth and "unweighted" in meth, "ask 2 reading pin")
    ok("computed from unrounded estimates" in meth, "rounding pin")

    # ---- goldens agree with figures.json
    with zipfile.ZipFile(os.path.join(golden, "hls_visit_limit_note_2026q3.docx")) as z:
        doc = re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))
    for k in ("rise_unemployment_rate_points", "cap_share_of_rise_points", "labour_market_share_of_rise_points",
              "published_unemployment_rate_2026Q3", "unemployment_rate_2026Q3_without_cap",
              "published_employment_rate_2026Q3", "employment_rate_2026Q3_without_cap"):
        ok(fig[k].lstrip("-") in doc, "memo carries " + k)
    for q, v in fig["unemployment_rate_gap_points"].items():
        ok(v in doc, "memo carries the unemployment gap " + q)
    for q, v in fig["employment_rate_gap_points"].items():
        ok(v.lstrip("-") in doc, "memo carries the employment gap " + q)
    wx = openpyxl.load_workbook(os.path.join(golden, "hls_visit_limit_path_2027.xlsx"), data_only=True)
    gp = {r[0]: r for r in wx["Gap path"].iter_rows(min_row=5, max_row=9, values_only=True)}
    for q, v in fig["unemployment_rate_gap_points"].items():
        ok("%.2f" % gp[q][1] == v and "%.2f" % gp[q][2] == fig["employment_rate_gap_points"][q], "workbook " + q)
    rg = {r[0]: r for r in wx["Regions"].iter_rows(min_row=4, max_row=9, values_only=True)}
    for g in W.RCODES:
        nm = W.RNAME[g]
        ok(rg[nm][1] == fig["first_interview_visits_2026Q3_intake"][nm], "workbook visits " + nm)
        ok("%.2f" % rg[nm][4] == fig["unemployed_to_employed_share_pct"][nm], "workbook flows " + nm)
        ok("%.1f" % rg[nm][5] == fig["total_weekly_hours_thousand"][nm], "workbook hours " + nm)
    for f in (os.path.join(golden, x) for x in os.listdir(golden)):
        if f.endswith(".docx"):
            ok("—" not in doc and "–" not in doc, "no dash in the memo")

    # ---- the simulation's own truth (information, and a sanity bound)
    J = dict(I)
    J.update(world["counterfactual"])
    true_q3 = M.published(I, (2026, 3))[0] - M.published(J, (2026, 3))[0]
    ok(abs(true_q3 - gf[0][0]) < 0.12, "the July to September estimate near the simulation's own gap")
    world["true_q3_gap"] = true_q3
    print("checks: %d assertions passed (golden path %s; rung 0 %s; rung 1 %s; weights kept %s; simulated July to "
          "September gap %.2f)" % (N[0], _fmt(gf), _fmt(r0), _fmt(r1), _fmt(r2), true_q3))


def _fmt(p):
    return "/".join("%.2f" % x[0] for x in p)


def _pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(pg.extract_text() for pg in PdfReader(path).pages).replace("\n", " ")
