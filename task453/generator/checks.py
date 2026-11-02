"""task453's assertions, run on every build: the input gates and provenance, the goldens against figures.json, every
estimator form of the decisive step and every wrong route by name with its margin, the assumptions the golden's
method makes (lesson 7), every semantic-fork row (SF1 to SF22), the three-rules block (R1 to R3c) on the clean truth,
both ask devices (uniqueness, clearance, the literal readings of lesson 8, every stop missing every figure), the
separation of the asks from the call, the distractors' deletion test, no shipped file describing the data, and the
realism sweep."""
import collections
import datetime as dt
import json
import math
import os
import re
import shutil
import subprocess
import tempfile

import numpy as np
import pandas as pd

import ceiling as CE
import golden as G
import methods as M
import sim
import survey as S
import truth as T
import world as W

RESULTS = []
DESCRIBE_NAME = re.compile(
    r"(?<![a-z])(read_?me|data_?dictionar\w*|dictionar(y|ies)|codebook|field_?notes|field_?guide|fields?_(guide|notes|"
    r"list|descriptions?)|\w*_fields|manifest|extract_contents|file_list|file_layout|glossary|column_(notes|"
    r"descriptions?)|data_?notes|how_to_read|about_this|export_notes|extract_notes|feed_notes|definitions|schema|"
    r"layouts?_notes|release_notes)(?![a-z])", re.I)
DESCRIBE_SHEET = re.compile(r"^(read ?me|notes?|dictionary|data dictionary|definitions|glossary|fields|field notes|"
                            r"about|about this (file|workbook)|how to (read|use)( this)?|columns?)$", re.I)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def nm(i):
    return W.CREMATORIA[i][2]


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def cre_list(rows, keep=lambda r: r["cremation"].year == W.YEAR, abated=None):
    ab = abated or (lambda r: sim.abated(W.CREMATORIA[r["ci"]], r["cremation"]))
    return [(r["ci"], r["age"], r["sex"], ab(r)) for r in rows if keep(r)]


def order_margin(d, gold):
    hg = d["hg"]
    outs = [i for i in d["order"] if i not in gold]
    return min(hg[x] for x in gold) / max(hg[y] for y in outs) - 1


def run(target, golden_dir, world=None, meta_path=None):
    RESULTS.clear()
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    if world is None:
        import build as B
        world = B.simulate()
    rows, tab = world["rows"], world["tab"]
    gold_names = fig["call"]["designated"]
    gold = {i for i, c in enumerate(W.CREMATORIA) if c[2] in gold_names}

    # ------------------------------------------------------------ input gates and provenance
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("input gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    ok("input gate: 3 or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max((x["rows"] or 0) for x in meta["files"])
    ok("input gate: a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    ok("input gate: two or more distractors named in metadata.json, each shipped and none read by the goldens",
       len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), meta["distractor_files"])
    ok("provenance: every file in metadata.json with source, date and licence",
       sorted(x["path"] for x in meta["files"]) == files and all(x["source"] and x["date"] and x["license"]
                                                                  for x in meta["files"]))
    ok("no distractor named after its role", not any(re.search(r"distract|decoy|unused", f, re.I) for f in files))

    # ------------------------------------------------------------ the goldens against figures.json
    res = G.call(target, tab)
    ok("golden: the call recomputed from the bundle designates %s" % " and ".join(gold_names),
       [nm(i) for i in res["des"]] == gold_names)
    ok("golden: 2026 short of 55 per cent", not fig["call"]["met"] and res["share"] < W.SHARE_REQUIRED,
       "%.2f" % res["share"])
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(golden_dir, W.GOLDEN["book"]), data_only=False)
    lev_ws = {r[0]: r[5] for r in wb["Levy 2026"].iter_rows(min_row=2, values_only=True) if r[0]}
    ok("golden workbook: every levy equals figures.json", lev_ws == fig["levy"])
    byp_ws = collections.defaultdict(dict)
    for r in wb["Bypassed cremations 2026"].iter_rows(min_row=2, values_only=True):
        byp_ws[r[0]][r[2].split()[1]] = r[3]
    ok("golden workbook: every bypass count equals figures.json", dict(byp_ws) == fig["bypass"])
    ok("golden workbook: 20 levies and 24 bypass cells", len(lev_ws) == 20 and sum(len(v) for v in byp_ws.values()) == 24)
    cert = pdf_text(os.path.join(golden_dir, W.GOLDEN["cert"]))
    flat = " ".join(cert.split())
    ok("golden certificate: names both designated crematoria, the verdict and the share at its precision",
       all(n in flat for n in gold_names) and "about %d per cent" % fig["call"]["share_pct_whole"] in flat
       and "did not meet" in flat)
    ok("golden certificate: no share or mercury given finer than the data carry (no decimal per cent)",
       not re.search(r"\d+\.\d+ per cent", flat))

    # ------------------------------------------------------------ the decisive step: every form, every wrong route
    cre = cre_list(rows)
    gold_steps = None
    for f in M.FORMS:
        d = M.designate(cre, tab, f)
        mo = order_margin(d, gold) if set(d["des"]) == gold else -1
        ok("form %s designates the golden pair with the third crematorium 5 per cent or more behind" % f,
           set(d["des"]) == gold and mo >= 0.05, "margin %.3f, share %.2f" % (mo, d["share"]))
        ok("form %s: the steps clear 55 per cent by 2 points either side" % f,
           len(d["steps"]) >= 3 and d["steps"][1] <= 53.0 and d["steps"][2] >= 57.0,
           " ".join("%.2f" % x for x in d["steps"]))
        if f == M.GOLDEN_FORM:
            gold_steps = d["steps"]
    for f in M.SCALING + M.OFF_BY_ONE:
        d = M.designate(cre, tab, f)
        ok("form %s (refuted or off by a year) still designates the golden pair" % f, set(d["des"]) == gold,
           "margin %.3f" % (order_margin(d, gold) if set(d["des"]) == gold else -1))
    shares = [M.designate(cre, tab, f)["share"] for f in M.FORMS]
    ok("the standing family's share spans under 1.5 points, so the certificate states it whole",
       max(shares) - min(shares) < 1.5 and len({int(round(x)) for x in shares}) <= 2, "%.2f to %.2f" % (min(shares), max(shares)))
    wrong = {"count": {"Corbett Narrows Crematorium"},
             "age2016": {"Tallis Creek Crematorium", "Dunmore Falls Memorial Gardens"},
             "age2016_interp": {"Tallis Creek Crematorium", "Dunmore Falls Memorial Gardens"},
             "age2006": {"Tallis Creek Crematorium", "Dunmore Falls Memorial Gardens"},
             "age_trend": {"Tallis Creek Crematorium", "Dunmore Falls Memorial Gardens"},
             "age_trend3": {"Tallis Creek Crematorium", "Dunmore Falls Memorial Gardens"},
             "age_trend_prop": {"Tallis Creek Crematorium", "Dunmore Falls Memorial Gardens"},
             "cohort_noage": {"Ashgrove Cremation Centre", "Corbett Narrows Crematorium"},
             "cohort_along_2016": {"Tallis Creek Crematorium", "Dunmore Falls Memorial Gardens"}}
    landed = 0
    for f, want in wrong.items():
        d = M.designate(cre, tab, f)
        got = {nm(i) for i in d["des"]}
        landed += got == set(gold_names)
        x = sorted(gold, key=lambda i: -d["hg"][i])
        outs = [z for z in d["order"] if z not in gold]
        od = max(d["hg"][z] for z in outs) / d["hg"][x[1]] - 1
        ok("wrong route %s designates %s, the golden pair 5 per cent or more off it (or its count stops apart)" % (
            f, " and ".join(sorted(want))), got == want and (od >= 0.05 or len(d["des"]) != 2),
           "share %.2f, margin %.3f" % (d["share"], od))
    ok("Gate F: no cheap route lands the call (count, both waves' profiles, the bands' trends, the cohort unaged or "
       "aged along the cross-section)", landed == 0, "%d of %d" % (landed, len(wrong)))
    a16 = M.designate(cre, tab, "age2016")
    al = M.designate(cre, tab, "cohort_along_2016")
    ok("ageing the cohort along the 2016 cross-section returns the age profile at death exactly",
       np.allclose(a16["hg"], al["hg"]))

    # ------------------------------------------------------------ lesson 7: the golden method's assumptions
    xs, ys, dec = [], [], {1: [], 2: []}
    for s in "MF":
        for k, (y0, y1) in enumerate(((1996, 2006), (2006, 2016)), 1):
            for lo in range(45, 80, 5):
                c0, c1 = M.band(tab, y0, s, lo), M.band(tab, y1, s, lo + 10)
                xs.append(c0)
                ys.append(c1 - c0)
                dec[k].append(c1 - c0)
    b = np.polyfit(xs, ys, 1)
    prop_slope = np.mean(ys) / np.mean(xs)
    ok("lesson 7: a cohort's change between waves does not scale with its level (slope near nil, a proportional change "
       "would need %.3f)" % prop_slope, abs(b[0]) < 0.04 and abs(b[0] - prop_slope) > 0.08, "slope %.3f" % b[0])
    ok("lesson 7: the within-cohort change is the same over both decades (a constant rate, no period shock)",
       abs(np.mean(dec[1]) - np.mean(dec[2])) < 0.15, "%.2f and %.2f" % (np.mean(dec[1]), np.mean(dec[2])))
    fixed_age = [tab[(2016, s, lo)]["amalgam"] - tab[(2006, s, lo)]["amalgam"] for s in "MF" for lo in range(45, 90, 5)]
    ok("lesson 7: at a fixed age the change between waves swings both ways (the age bands' own trends are not "
       "stable, the cohorts' are)", max(fixed_age) > 1.5 and min(fixed_age) < -1.5 and np.std(ys) < 0.35,
       "%.1f to %.1f against a cohort spread of %.2f" % (min(fixed_age), max(fixed_age), np.std(ys)))
    ok("lesson 7: no background to subtract (the 18 to 24 band, born after amalgam's use fell away, carries the "
       "least), no offset (every mean at or above nil)",
       all(tab[(y, s, 18)]["amalgam"] <= 3.5 for y in (2006, 2016) for s in "MF") and
       all(c["amalgam"] >= 0 for c in tab.values()))
    ok("lesson 7: the survey's sampling error is plausible for its samples (each cell's interval from its own "
       "examined count)", all(0.08 <= c["se"] <= 0.5 for (y, s, lo), c in tab.items() if s in "MF"))
    # the realised noise against the stated error: chi-square per degree of freedom near 1, not far below
    z = []
    for (y, s, lo), c in tab.items():
        if s in "MF":
            hi = c["hi"]
            ages = np.arange(lo, hi + 1)
            wgt = np.exp(-np.maximum(0, ages - 86) / 4.0) * np.exp(-np.maximum(0, 30 - ages) / 40.0)
            v = float(np.average([S.truth(y - a, a, s) for a in ages], weights=wgt))
            z.append((c["amalgam"] - v) / math.sqrt(c["se"] ** 2 + 0.0289 ** 2))
    chi = float(np.mean(np.square(z)))
    ok("lesson 7: the published cells' dispersion about the truth is plausible (chi-square per cell 0.6 to 1.6)",
       0.6 <= chi <= 1.6, "%.2f" % chi)

    # ------------------------------------------------------------ the clean truth: R1, R2, R3
    true_cre = []
    for r in rows:
        if r["cremation"].year != W.YEAR:
            continue
        b0 = r["cremation"].year - r["age"] - 0.5
        v = 0.0 if r["age"] < 18 else S.truth(int(round(b0)), r["age"], r["sex"])
        true_cre.append((r["ci"], v, sim.abated(W.CREMATORIA[r["ci"]], r["cremation"])))
    n = len(W.CREMATORIA)
    thg, tab_ = np.zeros(n), np.zeros(n)
    for ci, v, abt in true_cre:
        thg[ci] += v * W.HG_PER_TOOTH_G
        if abt:
            tab_[ci] += v * W.HG_PER_TOOTH_G
    unab = sorted([i for i, c in enumerate(W.CREMATORIA) if c[8] == "U"], key=lambda i: -thg[i])
    tdes, cur = [], tab_.sum()
    for i in unab:
        if 100 * cur / thg.sum() >= W.SHARE_REQUIRED:
            break
        tdes.append(i)
        cur += thg[i]
    ok("R3b the decisive step recovers the truth: each decedent's own amalgam designates the golden pair",
       set(tdes) == gold, "true share %.2f" % (100 * tab_.sum() / thg.sum()))
    clean = {}
    for y in S.WAVES:
        for lo, hi in S.BANDS[y]:
            ages = np.arange(lo, hi + 1)
            wgt = np.exp(-np.maximum(0, ages - 86) / 4.0) * np.exp(-np.maximum(0, 30 - ages) / 40.0)
            for s in "MF":
                clean[(y, s, lo)] = {"lo": lo, "hi": hi,
                                     "amalgam": float(np.average([S.truth(y - a, a, s) for a in ages], weights=wgt))}
    d_easy = M.designate(cre, clean, "age2016")
    ok("R3a analyst test: on the clean truth the 2016 profile at age at death designates Tallis Creek and Dunmore Falls",
       {nm(i) for i in d_easy["des"]} == wrong["age2016"], "share %.2f" % d_easy["share"])
    d_gold = M.designate(cre, clean, M.GOLDEN_FORM)
    ok("R3b the decisive step alone: on the clean truth the cohort carried by its own change designates the golden pair",
       set(d_gold["des"]) == gold, "share %.2f" % d_gold["share"])
    d_half = M.designate(cre, clean, "cohort_noage")
    ok("R3b each lower rung's single correction stays wrong on the clean truth (the cohort unaged designates "
       "Ashgrove and Corbett Narrows)", {nm(i) for i in d_half["des"]} == wrong["cohort_noage"])
    ok("R1 the field's raw material ships: permits at the cremation grain and the survey's cells by wave, band and sex",
       len(world["permits"]) > 25000 and sum(1 for k in tab if k[1] in "MF") == 2 * sum(len(S.BANDS[y]) for y in S.WAVES))
    heads = []
    for f in files:
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            heads += list(pd.read_csv(p, nrows=1).columns)
        elif f.endswith(".parquet"):
            heads += list(pd.read_parquet(p).columns)
        elif f.endswith(".xlsx"):
            for sh in pd.ExcelFile(p).sheet_names:
                heads += [str(x) for x in pd.read_excel(p, sheet_name=sh, nrows=6, header=None).fillna("").values.ravel()]
    heads = [h.replace("Crematoria Mercury Fund", "") for h in heads]
    ok("R1 no shipped column holds a cremation's mercury, amalgam, birth cohort or a designation",
       not any(re.search(r"mercury|amalgam|cohort|birth|designat", h, re.I) for h in heads),
       [h for h in heads if re.search(r"mercury|amalgam|cohort|birth|designat", h, re.I)][:3])
    # R2: each Layer 1 item mishandled leaves the call where it was
    def call_with(keep=None, abated=None, tabx=None, form=M.GOLDEN_FORM, skip=()):
        kp = keep or (lambda r: r["cremation"].year == W.YEAR)
        cx = cre_list([r for k, r in enumerate(rows) if k not in skip], keep=kp, abated=abated)
        return {nm(i) for i in M.designate(cx, tabx or tab, form)["des"]}
    ok("R2 mess: Wexley Regional's permits under its old number dropped leaves the call (SF8)",
       call_with(keep=lambda r: r["cremation"].year == W.YEAR and not (r["code"] == "CM-1590" and
                 r["cremation"] < W.WEXLEY_RENUMBERED)) == set(gold_names))
    ok("R2 mess: the 2026 population by date of death leaves the call (SF1)",
       call_with(keep=lambda r: r["death"].year == W.YEAR) == set(gold_names))
    ok("R2 mess: infants aged in months read as years leaves the call (SF5)", True,
       "nil under 18 either way: %d infants" % sum(1 for p in world["permits"] if p["age_unit"] == "M"))
    ok("R2 mess: the commissioning day counted as abated leaves the call (SF2)",
       call_with(abated=lambda r: W.CREMATORIA[r["ci"]][8] != "U" and
                 r["cremation"] >= dt.date.fromisoformat(W.CREMATORIA[r["ci"]][9])) == set(gold_names))
    tab2 = {k: dict(v, amalgam=v["amalgam"] * (1 - v["edentulous_pct"] / 100)) for k, v in tab.items()}
    ok("R2 mess: the per-adult means multiplied again by the dentate share leaves the call (SF6)",
       call_with(tabx=tab2) == set(gold_names))
    ok("R3c no plant: no file computes or ranks any crematorium's mercury, no memo or earlier inventory ships",
       not any(re.search(r"(?<![a-z])(inventory|memo|draft|briefing|estimates?)(?![a-z])", f, re.I) for f in files))

    # ------------------------------------------------------------ the semantic fork table
    ok("SF1 cremations in 2026 by date of cremation; by date of death the same call",
       call_with(keep=lambda r: r["death"].year == W.YEAR) == set(gold_names))
    ok("SF2 abated strictly after commissioning; on the day the same call",
       call_with(abated=lambda r: W.CREMATORIA[r["ci"]][8] != "U" and
                 r["cremation"] >= dt.date.fromisoformat(W.CREMATORIA[r["ci"]][9])) == set(gold_names))
    bt = {(x["ci"], x["k"]) for ci, p in world["plants"].items() for x in world["cyc"]
          if x["ci"] == ci and x["type"] == "CREMATION" and any(x["start"] <= b1 and x["end"] >= b0
                                                                 for b0, b1 in p["auto"] + p["manual"])}
    byk = {k for ci, k in bt}
    byid = {id(rows[k]) for k in byk}
    ok("SF3 a cremation while the plant was bypassed is still abated; counted as not abated the same call",
       call_with(abated=lambda r: sim.abated(W.CREMATORIA[r["ci"]], r["cremation"]) and
                 id(r) not in byid) == set(gold_names), "%d bypassed cremations" % len(byk))
    ok("SF4 the factor is the Regulation's 0.55 grams a tooth", W.HG_PER_TOOTH_G == 0.55 and
       "0.55 grams" in " ".join(pdf_text(os.path.join(target, W.FILES["reg"])).split()))
    ok("SF5 nil under 18 (the Regulation); infants in months are under 18", all(
        p["age"] < 12 for p in world["permits"] if p["age_unit"] == "M"))
    ok("SF6 the survey's means are per adult with the edentulous counted as none; a second dentate factor the same call",
       call_with(tabx=tab2) == set(gold_names) and "count as having none" in " ".join(
           pdf_text(os.path.join(target, W.FILES["s2016"])).split()))
    ok("SF7 the decedent's sex reads the sex-specific table; the all-adult table the same call",
       {nm(i) for i in M.designate(cre, tab, "cohort_pooled_sex")["des"]} == set(gold_names))
    ok("SF8 Wexley Regional's F1984 permits key to CM-1590 through the register; dropped, the same call",
       call_with(keep=lambda r: r["cremation"].year == W.YEAR and not (r["code"] == "CM-1590" and
                 r["cremation"] < W.WEXLEY_RENUMBERED)) == set(gold_names))
    ok("SF9 the scheme year is the calendar year (Regulation s.1)", "scheme year" in " ".join(
        pdf_text(os.path.join(target, W.FILES["reg"])).split()))
    hg = M.designate(cre, tab, M.GOLDEN_FORM)["hg"]
    sec = sorted(gold, key=lambda i: -hg[i])[1]
    ok("SF10 Wexley Regional and Hollinsbrook (abated cremations in 2026) are not candidates; as candidates the same call",
       hg[5] < hg[sec] and hg[6] < hg[sec], "%.0f and %.0f grams against %.0f" % (hg[5], hg[6], hg[sec]))
    per = sorted([i for i, c in enumerate(W.CREMATORIA) if c[8] == "U"],
                 key=lambda i: -hg[i] / max(1, sum(1 for r in cre if r[0] == i)))
    ok("SF11 the designation order is by total mercury (s.4(2)); per cremation would be another order, not a reading",
       per[:2] != sorted(gold, key=lambda i: -hg[i]))
    ok("SF12 the stop 'at least 55 per cent' has nothing on its edge (strict the same call)",
       gold_steps[1] < 54.0 and gold_steps[2] > 56.0, " ".join("%.2f" % x for x in gold_steps))
    oop = {p["_k"] for p in world["permits"] if p["residence_region"] == "Out of province"}
    ok("SF13 out-of-province residents cremated in the province are in; left out, the same call",
       call_with(skip=oop) == set(gold_names), "%d such permits" % len(oop))
    ok("SF14 the survey age is age at examination, the 2016 wave ten years earlier; lags of 9 and 11 years and the "
       "single-year mixture the same call", all({nm(i) for i in M.designate(cre, tab, f)["des"]} == set(gold_names)
                                                for f in ("cohort_lag9", "cohort_lag11", "cohort_lagmix")))
    ok("SF15 the open top bands read whole; interpolated by single years of age the same call",
       {nm(i) for i in M.designate(cre, tab, "cohort_interp")["des"]} == set(gold_names))
    ok("SF16 cohorts not surveyed as adults in 2006: the youngest band, the 2016 profile, the unaged mean or nil, the "
       "same call", all({nm(i) for i in M.designate(cre, tab, f)["des"]} == set(gold_names)
                        for f in ("cohort_young_profile", "cohort_young_noage", "cohort_young_zero")))
    lev_gross = None
    L = G.ledger_lines(target)
    ok("SF17 the levy base excludes goods, disbursements and sales tax (scheme rules 2.2): the base and the excluded "
       "lines differ", (L[(L.doc == "INV") & ~L.fee].cents.sum() > 0))
    comm = G.register(target)[2]
    lev, matched = G.levies(target, comm)
    split_round = {}
    for c in W.CREMATORIA:
        v = lev[c[0]]
        split_round[c[0]] = int(round(v["income_unabated"] * W.LEVY_UNABATED)) + int(round(v["income_abated"] * W.LEVY_ABATED))
    diff = [k for k in lev if split_round[k] != lev[k]["levy"]]
    ok("SF18 the levy is rounded once on the year's income (scheme rules 2.3); rounding each rate's part first moves "
       "at most a dollar, only where a crematorium has both", all(abs(split_round[k] - lev[k]["levy"]) <= 1 and
       k in ("CM-1590", "CM-2251") for k in diff), "differs at %s" % (diff or "none"))
    ok("SF19 a credit takes the scheme year of the fees it was allowed against; the posting date is the device (Ask A)",
       CE.levy_route(target, "posted") != fig["levy"])
    et = G.ET
    q_et, q_utc = collections.Counter(), collections.Counter()
    for ci, p in world["plants"].items():
        for x in world["cyc"]:
            if x["ci"] == ci and x["type"] == "CREMATION" and any(x["start"] <= b1 and x["end"] >= b0
                                                                   for b0, b1 in p["auto"] + p["manual"]):
                q_et[(ci, (x["start"].month - 1) // 3)] += 1
                u = x["start"].replace(tzinfo=et).astimezone(dt.timezone.utc)
                q_utc[(ci, (u.month - 1) // 3 + 4 * (u.year - W.YEAR))] += 1
    ok("SF20 a bypassed cremation's quarter is the same read in Eastern time or in UTC", q_et == q_utc)
    clear_min = []
    for ci, p in world["plants"].items():
        edges = sorted([x["start"] for x in world["cyc"] if x["ci"] == ci] + [x["end"] for x in world["cyc"] if x["ci"] == ci])
        import bisect
        for b0, b1 in p["auto"] + p["manual"]:
            for t in (b0, b1):
                j = bisect.bisect_left(edges, t)
                cand = [abs((edges[k] - t).total_seconds()) for k in (j - 1, j) if 0 <= k < len(edges)]
                clear_min.append(min(cand) / 60)
    ok("SF21 'under way': no cycle starts or ends within 25 minutes of a bypass's ends, so cooling or the clock's "
       "minute never moves a count", min(clear_min) >= 25, "%.0f minutes" % min(clear_min))
    ok("SF22 Hollinsbrook's and Wexley Regional's partial third quarters are quarters in service (the prompt)",
       "Q3" in fig["bypass"]["CM-2251"] and "Q3" in fig["bypass"]["CM-1590"] and "Q2" not in fig["bypass"]["CM-1590"])

    d_q = M.designate(cre, tab, "cohort_quad3")
    d2 = [M.band(tab, 2016, s_, lo + 20) - 2 * M.band(tab, 2006, s_, lo + 10) + M.band(tab, 1996, s_, lo)
          for s_ in "MF" for lo in range(45, 70, 5)]
    se2 = float(np.std(d2, ddof=1) / math.sqrt(len(d2)))
    bt_rep, bt_none = {}, {}
    for s_ in "MF":
        rep, none = [], []
        for lo in range(25, 80, 5):
            c96, c06, c16 = (M.band(tab, 1996, s_, lo), M.band(tab, 2006, s_, lo + 10), M.band(tab, 2016, s_, lo + 20))
            rep.append(2 * c06 - c96 - c16)
            none.append(c06 - c16)
        bt_rep[s_], bt_none[s_] = math.sqrt(np.mean(np.square(rep))), math.sqrt(np.mean(np.square(none)))
    ok("SF23 a quadratic through each cohort's three waves (another set: %s) is ruled out: its curvature is untestable "
       "on three waves and the waves show none (mean second difference within two standard errors of nil), the "
       "back-test the waves allow favours repeating the last change over no change for both sexes, and it carries "
       "about twice the additive form's sampling error" % " and ".join(nm(i) for i in d_q["des"]),
       abs(float(np.mean(d2))) < 2 * se2 and all(bt_rep[x] < bt_none[x] for x in "MF")
       and math.sqrt(9 + 9 + 1) > 1.9 * math.sqrt(4 + 1),
       "share %.2f; second difference %.2f (sd %.2f, n %d); back-test RMSE repeat %.2f and %.2f, none %.2f and %.2f" % (
           d_q["share"], float(np.mean(d2)), float(np.std(d2, ddof=1)), len(d2), bt_rep["M"], bt_rep["F"],
           bt_none["M"], bt_none["F"]))

    # ------------------------------------------------------------ Ask A: the account credits
    lt = T.levy_truth(world["ar"])
    ok("Ask A: the golden levies from the bundle equal the simulation's own", lt == fig["levy"])
    inv = L[L.doc == "INV"]
    by_cust = {k: g for k, g in inv.groupby(["ledger", "cust"])}
    adj = L[(L.doc == "CRN") & L.adj]
    uniq_bad, single_bad, multi = 0, 0, 0
    for r in adj.itertuples():
        g = by_cust[(r.ledger, r.cust)]
        sv = pd.to_datetime(g.service)
        end = pd.Timestamp(r.posted)
        for days, k in ((200, 4), (10000, 3)):
            w = g[(sv <= end + pd.Timedelta(days=10)) & (sv >= end - pd.Timedelta(days=days))]
            grp = collections.Counter()
            for x in w.itertuples():
                d = dt.date.fromisoformat(x.service)
                grp[(x.cents, (x.code, d.year, comm.get(x.code) is not None and d > comm[x.code], x.fee))] += 1
            eff = G._effects(-r.cents, [(a, s_, c) for (a, s_), c in grp.items()], k)
            uniq_bad += len(eff) != 1
        w = g[(sv <= end) & (sv >= end - pd.Timedelta(days=200))]
        if not (w.cents == -r.cents).any():
            multi += 1
            refs = w.ref.unique()
            tot = inv[inv.ref.isin(refs) & (inv.ledger == r.ledger)].groupby("ref").cents
            single_bad += int((tot.sum() == -r.cents).any() or (inv[inv.ref.isin(refs) & inv.fee &
                              (inv.ledger == r.ledger)].groupby("ref").cents.sum() == -r.cents).any())
    ok("Ask A device: every account credit has one effect on the levies (up to four lines in 200 days, three on the "
       "whole account, across the ledger's sites)", uniq_bad == 0, "%d credits, %d unsettled" % (len(adj), uniq_bad))
    ok("Ask A device: no booking's total equals a credit that no single line explains (the battery's pairing misses)",
       single_bad == 0, "%d multi-line credits" % multi)
    ok("Ask A device: no marker: account credits carry the same document type, code and description as their benign "
       "single-line twins, and occur in every month", adj.posted.str[:7].nunique() >= 12)
    routes = {k: CE.levy_route(target, k) for k in ("posted", "month_before", "ignore", "year_before")}
    routes["by_posting"] = CE.levy_route(target, "posted", by_posting=True)
    for k, r in routes.items():
        miss = min(abs(r[c] - fig["levy"][c]) for c in fig["levy"])
        ok("Ask A stop %s misses every crematorium's levy (by 2 dollars or more; the cracker's by 5)" % k,
           miss >= (5 if k == "posted" else 2), "smallest miss %d" % miss)
    ok("Ask A: the full includer (credits matched to the lines they sum to) reproduces figures.json",
       CE.levy_route(target, "match") == fig["levy"])
    ok("Ask A realism: no levy a round hundred", all(v % 100 for v in fig["levy"].values()))

    # ------------------------------------------------------------ Ask B: the bypass trace
    bt_ = T.bypass_truth(world["cyc"], world["plants"])
    ok("Ask B: the golden counts from the bundle equal the simulation's own", bt_ == fig["bypass"])
    pl = pd.read_parquet(os.path.join(target, W.FILES["plant"]))
    rd = pl[pl.record == "READING"]
    iv, _ = G.bypass_intervals(target)
    cold_ok, warm_ok = True, True
    for code, ivs in iv.items():
        r_ = rd[rd.fund_code == code]
        t = r_.logged_utc.values
        v = r_.inlet_temp_c.values
        for b0, b1, kind in ivs:
            m = (t >= np.datetime64((b0 + pd.Timedelta(minutes=25)).tz_convert(None))) & (t <= np.datetime64(b1.tz_convert(None)))
            if m.any() and v[m].max() > 45:
                cold_ok = False
        ev = pl[(pl.fund_code == code) & (pl.record == "EVENT")].sort_values("logged_utc")
        rows_ = list(ev.itertuples())
        for i, e in enumerate(rows_):
            if e.event == "ALARM" and e.detail.startswith("DP HIGH"):
                clr = next(x for x in rows_[i + 1:] if x.event == "ALARM CLEARED" and x.detail == "DP HIGH")
                if clr.logged_utc - e.logged_utc <= pd.Timedelta(minutes=5):
                    m = (t >= np.datetime64(e.logged_utc.tz_convert(None))) & \
                        (t <= np.datetime64((e.logged_utc + pd.Timedelta(minutes=40)).tz_convert(None)))
                    if m.any() and v[m].min() < 100:
                        warm_ok = False
    ok("Ask B device: through every bypass the inlet runs at ambient (45 degrees or under from 25 minutes in)", cold_ok)
    ok("Ask B over-cleaning half: an alarm cleared within five minutes leaves the inlet warm (the plant stayed on line)",
       warm_ok)
    stops = sum(1 for e in pl[pl.record == "EVENT"].itertuples() if e.event == "PLANT STOP")
    ok("Ask B benign twins: weekend plant stops give a cold inlet with no cremation under way",
       stops >= 20 and all(not any(x["start"] < s1 and x["end"] > s0 for x in world["cyc"] if x["ci"] == ci)
                           for ci, p in world["plants"].items() for s0, s1 in p["stops"]), "%d stops" % stops)
    for mode in ("manual", "alarms_clear", "utc_as_local", "count_events"):
        r = CE.bypass_route(target, mode)
        kept = sum(1 for c in fig["bypass"] for q in fig["bypass"][c] if r[c].get(q) == fig["bypass"][c][q])
        lim = 0 if mode == "manual" else 2
        ok("Ask B stop %s keeps %s" % (mode, "no cell (the cracker)" if lim == 0 else "two cells at most"), kept <= lim,
           "%d of 24 kept" % kept)
    r = CE.bypass_route(target, "late_clear")
    kept = sum(1 for c in fig["bypass"] for q in fig["bypass"][c] if r[c].get(q) == fig["bypass"][c][q])
    ok("Ask B stop late_clear (the half-handled device) keeps under a third of the cells", kept <= 7, "%d of 24" % kept)
    ok("Ask B: the full includer reproduces figures.json", CE.bypass_route(target, "reset") == fig["bypass"])

    # ------------------------------------------------------------ separation and distractors
    reads = {"call": {W.FILES[k] for k in ("permits", "register", "s1996", "s2006", "s2016")},
             "asks": {W.FILES[k] for k in ("ar_halbrook", "ar_shoreline", "ar_members", "cycles", "plant", "register")}}
    ok("separation: no ask device row (account credits, plant alarms) sits in a file the call reads",
       not (reads["call"] & {W.FILES[k] for k in ("ar_halbrook", "ar_shoreline", "ar_members", "cycles", "plant")}))
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(target, f), tmp)
        r2 = G.call(tmp, tab)
        l2, _ = G.levies(tmp)
        b2 = G.bypassed(tmp)
        ok("distractors: with both deleted the call, every levy and every bypass count are unchanged",
           r2["des"] == res["des"] and {k: v["levy"] for k, v in l2.items()} == fig["levy"] and b2 == fig["bypass"])
        for f in [x for x in files if x not in meta["distractor_files"] and x not in reads["call"]]:
            os.remove(os.path.join(tmp, f))
        r3 = G.call(tmp, tab)
        ok("separation: the call recomputes with every ask-only file deleted", r3["des"] == res["des"])
    finally:
        shutil.rmtree(tmp)

    from openpyxl import load_workbook as _lw
    dw = _lw(os.path.join(target, W.FILES["deaths"]), read_only=True).worksheets[0]
    drows = [r for r in dw.iter_rows(min_row=5, values_only=True) if r and r[0]]
    ok("realism: the deaths table's counts are non-negative whole numbers and each total is men plus women",
       drows and all(isinstance(v, int) and v >= 0 for r in drows for v in r[2:5]) and all(r[4] == r[2] + r[3] for r in drows),
       "%d rows" % len(drows))

    # ------------------------------------------------------------ no shipped file describes the data
    ok("describing files: the name rule catches a dictionary and a manifest (positive control)",
       all(DESCRIBE_NAME.search(x) for x in ("field_dictionary", "export_manifest", "readme")))
    ok("describing files: no shipped file is a dictionary, manifest, readme or notes file by name",
       not any(DESCRIBE_NAME.search(f.rsplit(".", 1)[0]) for f in files))
    sheets = [sh for f in files if f.endswith(".xlsx") for sh in pd.ExcelFile(os.path.join(target, f)).sheet_names]
    ok("describing files: no workbook sheet is a readme, notes or definitions tab", not any(
        DESCRIBE_SHEET.match(s_) for s_ in sheets), sheets)
    docs_text = {f: " ".join(pdf_text(os.path.join(target, f)).split()).lower() for f in files if f.endswith(".pdf")}
    leak_words = re.compile(r"cohort|birth year|year of birth|\bborn\b|age profile|ageing|aging|carried (forward|along|"
                            r"to)|bypass damper|subset|statement query|without a booking")
    ok("no document names a cohort, an ageing path, the bypass damper or how credits are posted",
       not any(leak_words.search(t) for t in docs_text.values()),
       [f for f, t in docs_text.items() if leak_words.search(t)])

    # ------------------------------------------------------------ realism sweep
    card = json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task453.json")))
    ok("realism: every persona is the card's own, drawn from guard.py names and registered with the card",
       sorted(W.PEOPLE.values()) == sorted(card["world"]["people"]))
    per_month = collections.Counter((r["ci"], r["cremation"].month) for r in rows if r["cremation"].year == W.YEAR)
    ok("realism: no crematorium cremates the same number in every month", all(
        len({per_month[(ci, m)] for m in range(1, 13)}) >= 6 for ci in range(n)))
    ok("realism: no round crematorium totals (no 2026 cremation count a round hundred)",
       all(int(res["n"][i]) % 100 for i in range(n)))
    ns = [c["n"] for (y, s, lo), c in tab.items() if s in "MF"]
    ok("realism: the survey's examined counts are not round", sum(1 for x in ns if x % 10 == 0) <= len(ns) // 6)
    mt = {round(os.path.getmtime(os.path.join(target, f))) for f in files}
    ok("realism: the folder carries one assembly stamp, after the extract", len(mt) == 1)
    permit_nos = [p["permit_no"] for p in world["permits"]]
    ok("realism: permit numbers unique", len(set(permit_nos)) == len(permit_nos))
    fd_lines = collections.Counter(L[L.doc == "INV"].cust)
    ok("realism: funeral directors' shares of bookings vary (no flat split)", np.std(list(fd_lines.values())) >
       0.4 * np.mean(list(fd_lines.values())))

    # ------------------------------------------------------------ report
    fails = [r for r in RESULTS if not r[1]]
    for label, good, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))
    print("checks: %d assertions, %d failures" % (len(RESULTS), len(fails)))
    return not fails
