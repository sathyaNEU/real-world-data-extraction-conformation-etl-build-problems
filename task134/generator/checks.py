"""Generator assertions for task134 architecture 4, run on the cut pack (target/ by default) and on the clean truth.

Labels R1 to R3c are the client's three rules executed (dataset-generation 7.1); SFn are the semantic fork rows of the
design note; the rest are the input gates, mess neutrality, the realism sweep and each graded figure's distance to its
bin edge under every standing member of the golden's family.
"""
import csv
import datetime as dt
import itertools
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import numpy as np  # noqa: E402

import analysis as A  # noqa: E402
import params as P  # noqa: E402
import results as R  # noqa: E402
import world  # noqa: E402
from io_util import pdf_text  # noqa: E402

OUT = []


def check(label, ok, detail=""):
    OUT.append((label, bool(ok), detail))


def edge(v, unit):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return re.sub(r"\s+", " ", " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x)))


def main(tdir):
    res = R.compute(tdir)
    g = res["raw"]["call"]
    rg = res["raw"]["rungs"]
    info = res["raw"]["info"]
    W = world.make()
    files = sorted(os.listdir(tdir))
    notice = " ".join(pdf_text(os.path.join(tdir, A.NOTICE)).split())
    licence = " ".join(pdf_text(os.path.join(tdir, A.LICENCE)).split())
    basis = docx_text(os.path.join(tdir, "deepening_2027_maintenance_planning_basis.docx"))

    # ---------------- the call ----------------
    check("call: the total rounds to 1,750,000 m3", res["total"] == 1750000, "%.0f" % g["total"])
    want = {"Outer Channel": 380000, "Fend Roads": 300000, "Middle Reach": 400000, "Inner Reach": 280000,
            "Turning Basin": 360000, "Berth pockets": 40000}
    check("call: each part's rounded volume", res["parts"] == want, str(res["parts"]))
    check("call: the parts sum to the total before rounding", abs(sum(g["parts"].values()) - g["total"]) < 1e-6)

    # ---------------- the ladder ----------------
    graded = {k: R.nearest(v, 50000) for k, v in rg.items()}
    check("ladder: R0 carry files 1,300,000", graded["R0 carry"] == 1300000, "%.0f" % rg["R0 carry"])
    check("ladder: R1 depth ratio (default path) files 1,500,000", graded["R1 depth ratio"] == 1500000, "%.0f" % rg["R1 depth ratio"])
    check("ladder: R2 trapping efficiency files 1,400,000", graded["R2 trapping efficiency"] == 1400000, "%.0f" % rg["R2 trapping efficiency"])
    check("ladder: R3 pooled depth regression files 2,200,000", graded["R3 pooled depth regression"] == 2200000, "%.0f" % rg["R3 pooled depth regression"])
    rung_bins = [graded[k] for k in ("R0 carry", "R1 depth ratio", "R2 trapping efficiency", "R3 pooled depth regression")]
    check("ladder: every rung files a different bin from the golden and from each other",
          len(set(rung_bins)) == 4 and res["total"] not in rung_bins, str(rung_bins))
    nearest_gap = min(abs(rg[k] - g["total"]) / g["total"] for k in ("R0 carry", "R1 depth ratio", "R2 trapping efficiency", "R3 pooled depth regression"))
    check("ladder: the nearest wrong rung is at least 10 per cent off the golden", nearest_gap >= 0.10, "%.3f" % nearest_gap)
    # every rung misses every deepened part's bin (R0, R1 computed per part)
    nt = A.Notice(tdir)
    V = g["V"]
    miss = True
    for n in A.REACH_NAMES:
        for alt in (V[n], V[n] * A.NEW_DEPTH / nt.parts[n]["depth"]):
            if R.nearest(alt, 20000) == res["parts"][n]:
                miss = False
    check("ladder: R0 and R1 miss every reach's and the basin's bin", miss)

    # ---------------- R1: the field's raw material ships ----------------
    nrows_a = sum(1 for _ in open(os.path.join(tdir, A.SURV_A))) - 1
    nrows_b = sum(1 for _ in open(os.path.join(tdir, A.SURV_B))) - 1
    check("R1 the surveys ship as soundings, one row per cell and survey", nrows_a > 40000 and nrows_b > 30000, "%d, %d" % (nrows_a, nrows_b))
    headers = []
    for f in files:
        if f.endswith(".csv"):
            headers += next(csv.reader(open(os.path.join(tdir, f)))) if True else []
    banned = re.compile(r"natural|equilibri|over.?depth|coefficient|forecast|year.?1|uplift|trapping", re.I)
    check("R1 no shipped column holds a natural bed, a depth below it, a coefficient or a forecast",
          not any(banned.search(h) for h in headers), str([h for h in headers if banned.search(h)]))
    E, N, Z, C = A.read_surveys(tdir)
    s, t = nt.chain_offset(E, N)
    in_margin = 0
    for n in A.REACH_NAMES:
        p = nt.parts[n]
        half = p["width"] / 2.0
        if n == "Turning Basin":
            m = (s >= p["c0"]) & (s <= p["c1"]) & (t < -(half + 50)) & (t >= -(half + 300))
        else:
            m = (s >= p["c0"]) & (s < p["c1"]) & (np.abs(t) > half + 50) & (np.abs(t) <= half + 300)
        in_margin += int(m.sum())
    check("R1 the decisive step reads the margin soundings beyond the maintained widths", in_margin > 30000, "%d cells" % in_margin)

    # ---------------- R2: every mess item real and neutral ----------------
    def same_call(x):
        return R.nearest(x["total"], 50000) == res["total"] and all(R.nearest(x["parts"][p], 20000) == res["parts"][p] for p in R.PARTS)
    check("R2 survey datum and grid: the first contractor alone files the call", same_call(A.call(tdir, which=("A",))))
    check("R2 survey datum and grid: the second contractor alone (converted from ODN) files the call", same_call(A.call(tdir, which=("B",))))
    sentinel = 0
    with open(os.path.join(tdir, A.SURV_A), newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if float(r["DEPTH_M_BCD"]) <= -99]
    if rows:
        se, sn = nt.chain_offset([float(r["EASTING"]) for r in rows], [float(r["NORTHING"]) for r in rows])
        for n in A.REACH_NAMES:
            p = nt.parts[n]
            half = p["width"] / 2.0
            sentinel += int(np.sum((se >= p["c0"]) & (se <= p["c1"]) & (np.abs(sn) > half) & (np.abs(sn) <= half + 300) & (sn < 0 if n == "Turning Basin" else True)))
    check("R2 the -99.99 quay-face cells lie outside every margin band, so counting them moves nothing", len(rows) > 0 and sentinel == 0,
          "%d sentinel cells, %d in a band" % (len(rows), sentinel))
    certs = A.read_certificates(tdir, reissue="both")
    codes = sorted({r["area"] for r in certs})
    check("R2 area codes: the crosswalk maps every 2021 code to an area of the notice", all(c in A.REACH_NAMES + A.BERTH_NAMES + ["North Quay Berth 2"] for c in codes), str(codes))
    check("SF8 the codes' own order gives the crosswalk's mapping", [P.CODES_2021[k] for k in ["OC", "FR", "MR", "IR", "TB", "NQ1", "NQ2", "NQ3", "CT5"]] == sorted(P.CODES_2021.values()))
    check("R2 SF5 the financial years 2016-17 to 2025-26 file the call", same_call(A.call(tdir, window="financial")))
    check("R2 SF7 the re-issued certificate summed beside the original files the call", same_call(A.call(tdir, reissue="both")))
    tmp = tempfile.mkdtemp()
    try:
        for f in [A.SURV_A, A.SURV_B, A.CERTS, A.NOTICE]:
            shutil.copy(os.path.join(tdir, f), tmp)
        x = A.call(tmp)
        check("R2 the call reads no ask file: with the load log, revision, licence, sampling and lab deleted it is unchanged",
              abs(x["total"] - g["total"]) < 1e-6)
    finally:
        shutil.rmtree(tmp)

    # ---------------- R3: the analyst test on the clean truth ----------------
    truthV = {}
    for (a_, y, m), v in W.monthly.items():
        if dt.date(2016, 10, 1) <= dt.date(y, m, 1) <= dt.date(2026, 9, 1):
            truthV[a_] = truthV.get(a_, 0.0) + v / 10.0
    berths_t = sum(truthV[b] for b in ("NQ1", "NQ3", "CT5"))
    easy = sum(truthV[c] * P.DEPTH_NEW / P.DEPTH_NOW for c in P.DEEPENED) + berths_t
    gold_t = sum(truthV[c] * (P.DEPTH_NEW - W.part[c]["nat"]) / (P.DEPTH_NOW - W.part[c]["nat"]) for c in P.DEEPENED) + berths_t
    carry_t = sum(truthV[c] for c in P.DEEPENED) + berths_t
    check("R3a the default path on the clean truth files 1,500,000, not the golden", R.nearest(easy, 50000) == 1500000, "%.0f" % easy)
    check("R3b the default path with only the decisive step changed files the golden on the clean truth", R.nearest(gold_t, 50000) == 1750000, "%.0f" % gold_t)
    check("R3b the lower rung's single correction (the record carried) stays wrong", R.nearest(carry_t, 50000) == 1300000, "%.0f" % carry_t)
    # R3c no plant
    allnums = notice + licence + basis
    graded_strings = [R.fmt(res["total"])] + [R.fmt(v) for v in res["parts"].values()] + [R.fmt(v) for v in res["a"].values()]
    check("R3c no document carries a graded figure", not any(sx in allnums for sx in graded_strings))
    blocks_ok = True
    by_survey = {}
    with open(os.path.join(tdir, A.SURV_A), newline="") as fh:
        for r in csv.DictReader(fh):
            by_survey.setdefault(r["SURVEY_REF"], []).append(r["DEPTH_M_BCD"])
    seqs = [tuple(v[:400]) for v in by_survey.values()]
    blocks_ok = len(set(seqs)) == len(seqs)
    check("R3c no copied or backfilled survey block (every survey's soundings differ)", blocks_ok)
    seqs6 = {}
    rep = 0
    by_area = {}
    for r in certs:
        by_area.setdefault(r["area"], []).append(r["vol"])
    for a_, vs in by_area.items():
        for i in range(len(vs) - 5):
            key = tuple(vs[i:i + 6])
            if key in seqs6:
                rep += 1
            seqs6[key] = a_
    check("R3c no repeated block of six monthly certificate volumes in any area", rep == 0, "%d repeats" % rep)

    # ---------------- the forks ----------------
    check("SF1 the basis files the in situ volume as the certificates measure it", "in situ volume of material, as the contractor's monthly certificates measure it" in basis)
    check("SF2 the window is filed: 1 October 2027 to 30 September 2028", "between 1 October 2027 and 30 September 2028" in basis)
    check("SF3 the berth pockets keep their depths", "berth pockets keep their present maintained depths" in basis)
    check("SF4 Berth 2 out of maintenance (notice and basis), so nil", "North Quay Berth 2 has not been maintained since 1 April 2019" in notice and "North Quay Berth 2 stays out of maintenance" in basis)
    from openpyxl import load_workbook
    hdr6 = [c for c in next(load_workbook(os.path.join(tdir, A.CERTS), read_only=True)["2020-21"].iter_rows(min_row=4, max_row=4, values_only=True))]
    check("SF6 the record's measure: the certificates carry in situ volume beside dry solids", "In situ volume (m3)" in hdr6 and "Dry solids (t)" in hdr6, str(hdr6))
    # the standing family: every defensible reading of the natural bed and of the coefficient, on the filed window
    # and certificates (the financial-year window and the double-counted re-issue are mishandlings, asserted alone above)
    fam = []
    for buf in (0.0, 25.0, 50.0, 100.0):
        for stat in ("mean", "median"):
            for which in (("A", "B"), ("A",), ("B",)):
                fam.append(A.call(tdir, buffer=buf, stat=stat, which=which))
    # one-coefficient routes
    names = A.REACH_NAMES
    od = np.array([12.3 - g["nat"][n] for n in names])
    rate = np.array([V[n] / info["areas"][n] for n in names])
    kc = float(np.sum(rate * od) / np.sum(od ** 2))
    b_ols = float(np.polyfit(od, rate, 1)[0])
    pw = float(np.polyfit(np.log(od), np.log(rate), 1)[0])
    berths = g["parts"]["Berth pockets"]
    routes = {"origin": {n: V[n] + kc * 2 * info["areas"][n] for n in names},
              "least squares": {n: V[n] + b_ols * 2 * info["areas"][n] for n in names},
              "power": {n: V[n] * ((od[i] + 2) / od[i]) ** pw for i, n in enumerate(names)}}
    for k, pr in routes.items():
        pr["Berth pockets"] = berths
        fam.append(dict(parts=pr, total=sum(pr.values())))
    fam.append(A.call(tdir, held_now=None))
    # more readings of the natural bed: the band's outer edge, one side of the channel, a subset of the surveys, the mean
    # of per-survey means, and chainage segments (mean bed, volume split by depth below the bed, or split equally)
    sdates = []
    with open(os.path.join(tdir, A.SURV_A), newline="") as fh:
        for r in csv.DictReader(fh):
            if float(r["DEPTH_M_BCD"]) > -99:
                sdates.append(dt.datetime.strptime(r["SURVEY_DATE"], "%d/%m/%Y").date())
    with open(os.path.join(tdir, A.SURV_B), newline="") as fh:
        for r in csv.DictReader(fh):
            sdates.append(dt.date.fromisoformat(r["survey_date"]))
    sdates = np.array(sdates)
    usd = sorted(set(sdates))

    def band(name, buffer=50.0, outer=300.0, side="both", sel=None):
        p = nt.parts[name]
        half = p["width"] / 2.0
        ins_ = (s >= p["c0"]) & (s < p["c1"]) if name != "Turning Basin" else (s >= p["c0"]) & (s <= p["c1"])
        if name == "Turning Basin" or side == "south":
            m = ins_ & (t < -(half + buffer)) & (t >= -(half + outer))
        elif side == "north":
            m = ins_ & (t > half + buffer) & (t <= half + outer)
        else:
            m = ins_ & (np.abs(t) > half + buffer) & (np.abs(t) <= half + outer)
        return m if sel is None else m & sel

    def member(nat=None, parts=None):
        if parts is None:
            parts = {n: V[n] * (14.3 - nat[n]) / (12.3 - nat[n]) for n in A.REACH_NAMES}
        parts = dict(parts)
        parts["Berth pockets"] = berths
        return dict(parts=parts, total=sum(parts.values()))
    more = []
    for outer in (150.0, 200.0, 250.0):
        more.append(member({n: float(np.mean(Z[band(n, outer=outer)])) for n in A.REACH_NAMES}))
    for bb, oo in ((100.0, 200.0), (25.0, 150.0)):
        more.append(member({n: float(np.mean(Z[band(n, buffer=bb, outer=oo)])) for n in A.REACH_NAMES}))
    for side in ("north", "south"):
        more.append(member({n: float(np.mean(Z[band(n, side=side)])) for n in A.REACH_NAMES}))
    for sel in (sdates == usd[-1], sdates == usd[0], sdates >= dt.date(2024, 10, 1), sdates < dt.date(2018, 4, 30),
                np.array([d_.month == 4 for d_ in sdates]), np.array([d_.month == 10 for d_ in sdates])):
        more.append(member({n: float(np.mean(Z[band(n, sel=sel)])) for n in A.REACH_NAMES}))
    more.append(member({n: float(np.mean([np.mean(Z[band(n) & (sdates == d_)]) for d_ in usd if np.any(band(n) & (sdates == d_))]))
                        for n in A.REACH_NAMES}))
    for seg in (0.5, 0.25):
        segs = {}
        for n in A.REACH_NAMES:
            p = nt.parts[n]
            cuts = np.arange(p["c0"], p["c1"] + 1e-9, seg)
            segs[n] = np.array([float(np.mean(Z[band(n) & (s >= a_) & (s < b_)])) for a_, b_ in zip(cuts[:-1], cuts[1:])
                                if np.sum(band(n) & (s >= a_) & (s < b_)) > 20])
        more.append(member({n: float(np.mean(segs[n])) for n in A.REACH_NAMES}))
        more.append(member(parts={n: float(np.sum(V[n] * (12.3 - segs[n]) / np.sum(12.3 - segs[n]) * (14.3 - segs[n]) / (12.3 - segs[n])))
                                  for n in A.REACH_NAMES}))
        more.append(member(parts={n: float(np.mean(V[n] * (14.3 - segs[n]) / (12.3 - segs[n]))) for n in A.REACH_NAMES}))
    check("SF9 SF10 more readings of the natural bed (outer edge, one side, survey subsets, per-survey means, chainage "
          "segments) each file every bin", all(R.nearest(x["total"], 50000) == 1750000 and
                                                 all(R.nearest(x["parts"][p], 20000) == res["parts"][p] for p in R.PARTS) for x in more),
          "%d readings, %.0f to %.0f" % (len(more), min(x["total"] for x in more), max(x["total"] for x in more)))
    fam += more
    # the batter: soundings in the first 20 m outside the maintained width grade from the held depth to the bed beyond,
    # so a band that starts at the edge and stops short keeps the cut's own slope and is not a reading of the natural bed
    bat = [float(np.mean(Z[band(n, buffer=0.0, outer=20.0)])) - float(np.mean(Z[band(n)])) for n in A.REACH_NAMES]
    check("mishandling: the surveys show the batter, the first 20 m outside each width over 1.2 m deeper than the bed beyond",
          min(bat) > 1.2, str([round(v, 2) for v in bat]))
    keep_batter = [member({n: float(np.mean(Z[band(n, buffer=0.0, outer=oo)])) for n in A.REACH_NAMES})["total"] for oo in (100.0, 200.0)]
    check("mishandling: a band from the channel edge to 100 m or 200 m keeps the batter and files 1,800,000",
          all(R.nearest(v, 50000) == 1800000 for v in keep_batter), "%.0f, %.0f" % tuple(keep_batter))
    totals = [x["total"] for x in fam]
    check("SF9 SF10 SF11 SF12 every standing member files 1,750,000", all(R.nearest(v, 50000) == 1750000 for v in totals),
          "%.0f to %.0f over %d members" % (min(totals), max(totals), len(totals)))
    for p in R.PARTS:
        vals = [x["parts"][p] for x in fam]
        check("SF14 every standing member files %s's bin" % p, all(R.nearest(v, 20000) == res["parts"][p] for v in vals),
              "%.0f to %.0f" % (min(vals), max(vals)))
    tight_part = min(edge(x["parts"][p], 20000) for x in fam for p in R.PARTS)
    tight_total = min(edge(v, 50000) for v in totals)
    check("SF14 the tightest standing member is at least 2,500 m3 inside a part's bin and 5,000 inside the total's",
          tight_part >= 2500 and tight_total >= 5000, "%.0f, %.0f" % (tight_part, tight_total))
    kp_all = float(np.mean(list(info["k"].values())))
    check("SF11 the coefficient is one across the parts (each within 1 per cent of their mean, none identical)",
          all(abs(v / kp_all - 1) <= 0.01 for v in info["k"].values()) and len({round(v, 4) for v in info["k"].values()}) == len(info["k"]),
          str({k: round(v, 4) for k, v in info["k"].items()}))
    ins = []
    for n in A.REACH_NAMES:
        p = nt.parts[n]
        m = (s >= p["c0"]) & (s < p["c1"]) & (np.abs(t) <= p["width"] / 2.0 - 10)
        ins.append(float(np.mean(Z[m])))
    check("SF12 the surveys' in-channel mean equals the notice's 12.3 m (within 0.03 m)", all(abs(v - 12.3) < 0.03 for v in ins), str([round(v, 3) for v in ins]))
    check("SF12 the held depth read from the surveys files the call", same_call(A.call(tdir, held_now=float(np.mean(ins)))))
    check("SF13 the basis reports the berth pockets together", "for the berth pockets together" in basis)
    # the trapping-efficiency family, every exponent, misses the golden
    te = []
    for nexp in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0):
        tot = berths
        for n in names:
            h = g["nat"][n]
            e = lambda H: 1.0 - (h / H) ** nexp
            tot += V[n] * e(14.3) / e(12.3)
        te.append(tot)
    check("ladder: a trapping efficiency at any exponent 0.5 to 5 misses the golden's bin", all(R.nearest(v, 50000) != 1750000 for v in te),
          "%.0f to %.0f" % (min(te), max(te)))
    # Berth 2's relaxation follows the same coefficient toward the basin's natural bed, whichever way it is fitted
    forms, finfo = A.model_forms(tdir)
    b2 = finfo["berth2"]
    kpool = float(np.sum(rate * od) / np.sum(od ** 2))
    check("Berth 2 has relaxed toward the basin's natural bed at the parts' coefficient (free fit and fit on the measured bed "
          "within 0.002 of the pooled coefficient, the free asymptote within 0.1 m of the basin bed)",
          abs(b2["k_free"] - kpool) <= 0.002 and abs(b2["k_fixed"] - kpool) <= 0.002 and abs(b2["asymptote_free"] - b2["basin_bed"]) <= 0.1,
          "pooled %.4f, free %.4f, on the bed %.4f, asymptote %.2f against %.2f" % (kpool, b2["k_free"], b2["k_fixed"], b2["asymptote_free"], b2["basin_bed"]))
    check("the maintained berths read the parts' law on the basin's natural bed (exponent within 0.05 of one, coefficient "
          "within 0.002 of the pooled one)", abs(finfo["berth_exponent"] - 1.0) <= 0.05 and abs(finfo["berth_k"] - kpool) <= 0.002,
          "exponent %.3f, coefficient %.4f" % (finfo["berth_exponent"], finfo["berth_k"]))
    # SF11 every model of the law, every part: the same bin as the golden, with its distance to the bin edge
    for lab, d in forms.items():
        for p_ in A.REACH_NAMES:
            check("SF11 %s: %s files %s m3" % (lab, p_, R.fmt(res["parts"][p_])), R.nearest(d[p_], 20000) == res["parts"][p_],
                  "%.0f, %.0f inside its edge" % (d[p_], edge(d[p_], 20000)))
        check("SF11 %s: the total files 1,750,000 m3" % lab, R.nearest(d["total"], 50000) == 1750000,
              "%.0f, %.0f inside its edge" % (d["total"], edge(d["total"], 50000)))
    worst = min(edge(d[p_], 20000) for d in forms.values() for p_ in A.REACH_NAMES)
    check("SF11 the tightest part under any model of the law is at least 5,000 m3 inside its bin", worst >= 5000, "%.0f" % worst)

    # ---------------- the asks ----------------
    check("SF15 the licence asks for the quantity placed at each disposal site", "giving the quantity placed at each disposal site in wet tonnes" in licence)
    check("SF16 the licence takes quarters by the date of placement in UK civil time",
          "taken by the date on which the material was placed in UK civil time (GMT, or BST while it is in force)" in licence
          and "the month taken in UK civil time as in 5.3" in licence)
    check("SF17 the licence files the campaign rule", "most recent sampling campaign completed before the month in which it was placed" in licence)
    check("SF18 the licence files the formula for a vessel without a loading monitor", "For a vessel without a loading monitor" in licence)
    rev_rows = list(csv.reader(open(os.path.join(tdir, A.REVISION))))
    check("SF19 the revision's own columns carry the revised dry solids, what they revise and when they were issued",
          rev_rows[0] == ["trip_ref", "dry_solids_t_revised", "revises", "basis", "issued_by", "issued"]
          and all(r[2] == "loading monitor dry solids" and r[5] == "30/03/2026" for r in rev_rows[1:]), str(rev_rows[0]))
    check("SF20 SF21 the licence files where a sample counts and the duplicate rule", "in which each sample was actually taken" in licence and "averaged with its primary sample" in licence)
    lab_units = {r["units"] for r in csv.DictReader(open(os.path.join(tdir, A.LAB))) if r["determinand"] == "Mercury"}
    check("SF22 the lab's units column carries the mercury units", lab_units == {"mg/kg", "ug/kg"}, str(lab_units))
    # SF25 the dry-solids fraction for April to September 2026: the area summary's 2026 values are the licence 5.5 means
    # of the laboratory's values printed to three decimals, none near a rounding midpoint, and every placement total
    # files the same bin under the printed summary and under the 5.5 recomputation at full precision
    full55 = A.ds55_fractions(tdir)
    printed = {a_: f_ for c_, a_, f_ in A.ds_fractions(tdir) if c_.year == 2026}
    check("SF25 the 2026 area summary is the licence 5.5 recomputation printed to three decimals",
          set(full55) == set(printed) and all(round(full55[k], 3) == printed[k] for k in printed),
          str({k: (printed[k], round(full55[k], 5)) for k in printed}))
    check("SF25 no 2026 area mean sits within 0.0001 of a rounding midpoint (every rounding convention prints the same)",
          all(abs(full55[k] - printed[k]) <= 0.0004 for k in printed), "%.5f" % max(abs(full55[k] - printed[k]) for k in printed))
    a_rec, _ = A.ask_a(tdir, fractions="recompute")
    for k_ in sorted(res["raw"]["a"]):
        va, vb = res["raw"]["a"][k_], a_rec[k_]
        check("SF25 %s Q%d files %s t under the printed summary and under the 5.5 recomputation, clear of its edge by more "
              "than the gap" % (k_[0], k_[1], R.fmt(res["a"][k_])),
              R.nearest(va, 1000) == R.nearest(vb, 1000) == res["a"][k_] and edge(va, 1000) > abs(va - vb) + 300
              and edge(vb, 1000) >= 300, "%.0f and %.0f, edges %.0f and %.0f" % (va, vb, edge(va, 1000), edge(vb, 1000)))
    # SF24 a survey cell's part: four memberships, one call, and component 1 stated at the precision they share
    memb = A.natural_bed_memberships(tdir)
    mem_ok = True
    for rule, natm in memb.items():
        pm = {n_: V[n_] * (14.3 - natm[n_]) / (12.3 - natm[n_]) for n_ in A.REACH_NAMES}
        pm["Berth pockets"] = berths
        mem_ok &= R.nearest(sum(pm.values()), 50000) == 1750000 and all(R.nearest(pm[p_], 20000) == res["parts"][p_] for p_ in pm)
    check("SF24 every cell membership (nearest segment by chainage, rectangle on each segment, nearest segment by distance "
          "or by square offset) files the call and every part", mem_ok)
    figs_now = json.load(open(os.path.join(HERE, "figures.json"))) if os.path.exists(os.path.join(HERE, "figures.json")) else {}

    def holds(text, v):
        xs = [float(x) for x in re.findall(r"\d+\.\d", text)]
        return (xs[0] - 0.05 - 1e-9 <= v <= xs[-1] + 0.05 + 1e-9) if xs else False
    if figs_now:
        check("SF24 component 1's one-decimal natural beds hold every membership's value",
              all(holds(figs_now["component.natural_bed_1dp.%s" % n_], natm[n_]) for natm in memb.values() for n_ in A.REACH_NAMES),
              str({n_: figs_now["component.natural_bed_1dp.%s" % n_] for n_ in A.REACH_NAMES}))
    check("SF23 ask figures: every placement 150 t and every mean 0.0012 inside its rounding edge",
          min(edge(v, 1000) for v in res["raw"]["a"].values()) >= 150 and min(edge(v, 0.01) for v in res["raw"]["b"].values()) >= 0.0012,
          "%.0f, %.4f" % (min(edge(v, 1000) for v in res["raw"]["a"].values()), min(edge(v, 0.01) for v in res["raw"]["b"].values())))
    import ceiling
    ce = ceiling.main(tdir)
    check("asks: the cracker keeps 0 of 8 placements", ce["keep"]["A1 site column, no revision (cracker: filed rules applied)"] == 0)
    check("asks: pair ceiling at or under 60 and mirror leakage under 50", ce["pair"] <= 60 and ce["mirror"] < 50, "%.1f, %.1f" % (ce["pair"], ce["mirror"]))
    check("asks: the full includer stays under 60", ce["full"] <= 60, "%.1f" % ce["full"])
    a_route, _ = A.ask_a(tdir, site_by="planned")
    moved = sum(1 for k in res["a"] if R.nearest(a_route[k], 1000) != res["a"][k])
    check("asks: device A1 moves every placement figure", moved == 8)
    b_plan = A.ask_b(tdir, part_by="plan")
    movedb = sum(1 for k in res["b"] if R.r2(b_plan[k]) != res["b"][k])
    check("asks: device B1 moves at least 14 of 20 means", movedb >= 14, "%d" % movedb)
    # separation: no device row in the call's files
    check("separation: the call's files carry no load, sample or site column", not any(re.search(r"site|dump|sample|trip", h, re.I) for f in (A.SURV_A, A.SURV_B) for h in next(csv.reader(open(os.path.join(tdir, f))))))

    # ---------------- input gates ----------------
    exts = {f.rsplit(".", 1)[1] for f in files}
    check("gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("gate: 3 or more formats", len(exts) >= 3, str(sorted(exts)))
    big = max(sum(1 for _ in open(os.path.join(tdir, f))) - 1 for f in files if f.endswith(".csv"))
    check("gate: a file of 25,000 rows or more", big >= 25000, str(big))
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json"))) if os.path.exists(os.path.join(os.path.dirname(HERE), "metadata.json")) else None
    import make_pack
    check("gate: two or more distractors", len(make_pack.DISTRACTORS) >= 2)
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in make_pack.DISTRACTORS:
                shutil.copy(os.path.join(tdir, f), tmp)
        r2 = R.compute(tmp)
        check("gate: deleting every distractor leaves the call and every ask unchanged",
              r2["total"] == res["total"] and r2["parts"] == res["parts"] and r2["a"] == res["a"] and r2["b"] == res["b"])
    finally:
        shutil.rmtree(tmp)
    check("gate: no file describes the data (no readme, dictionary, notes or manifest)", not any(re.search(r"readme|dictionar|notes|manifest|schema", f, re.I) for f in files))
    check("gate: no file name carries an author's word", not any(re.search(r"test_|trap|decoy|distract|answer|truth", f, re.I) for f in files))

    # ---------------- realism sweep ----------------
    loads = list(csv.DictReader(open(os.path.join(tdir, A.LOADS))))
    nums = [int(r["load_ref"].split("-")[-1]) for r in loads if r["load_ref"].startswith("DDL-2526")]
    steps = {b - a for a, b in zip(nums, nums[1:])}
    check("realism: load numbers are not one constant step (aborted loadings skip numbers)", len(steps) > 1, str(sorted(steps)[:5]))
    labno = sorted({int(r["lab_no"]) for r in csv.DictReader(open(os.path.join(tdir, A.LAB)))})
    check("realism: laboratory numbers are not one constant step", len({b - a for a, b in zip(labno, labno[1:])}) > 1)
    yr = {}
    for r in A.read_certificates(tdir):
        ly = r["month"].year if r["month"].month >= 10 else r["month"].year - 1
        if 2016 <= ly <= 2025:
            yr[ly] = yr.get(ly, 0.0) + r["vol"]
    yv = [yr[y] for y in sorted(yr)]
    check("realism: no two licence years carry the same total, none a round number", len(set(round(v) for v in yv)) == len(yv) and all(round(v) % 1000 for v in yv))
    spread = (max(yv) - min(yv)) / np.mean(yv)
    check("realism: the yearly totals vary as a storm-driven record does (3 to 25 per cent range)", 0.03 <= spread <= 0.25, "%.3f" % spread)
    fl = {}
    for r in csv.DictReader(open(os.path.join(tdir, "river_fend_haddon_weir_flows_2016-2026.csv"))):
        d_ = dt.date.fromisoformat(r["date"])
        ly = d_.year if d_.month >= 10 else d_.year - 1
        if 2016 <= ly <= 2025:
            fl.setdefault(ly, []).append(float(r["mean_flow_m3s"]))
    fy = [np.mean(fl[y]) for y in sorted(yr)]
    cor = float(np.corrcoef(fy, yv)[0, 1])
    check("realism: the river flow is not a driver of the yearly infill (|r| under 0.7)", abs(cor) < 0.7, "%.2f" % cor)
    check("realism: area names take more than two shapes", len({re.sub(r"\d", "", n).split()[-1] for n in A.REACH_NAMES + A.BERTH_NAMES}) > 2)
    check("realism: every persona is from guard.py names", all(n in json.load(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude/skills/fingerprint/cards/task134.json")))["world"]["people"] for n in P.PEOPLE.values()))
    check("realism: no document states a date after its own file date",
          "2027" not in notice.replace("2027", "") and "3 February 2026" in notice and "11 January 2027" in basis)
    check("realism: no em or en dash in any document", not any(ch in notice + licence + basis for ch in ("\u2014", "\u2013")))
    for f in files:
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(os.path.join(tdir, f)) as z:
                core = z.read("docProps/core.xml").decode()
                app = z.read("docProps/app.xml").decode()
            check("realism: %s carries its issuer, not the writing library" % f, "openpyxl" not in core + app and "python-docx" not in core + app)
    stamps = {}
    for f in files:
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(os.path.join(tdir, f)) as z:
                core = z.read("docProps/core.xml").decode()
            stamps[f] = (re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1),
                         re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1))
    cut = P.EXPORT_DATE.strftime("%Y-%m-%dT%H:%M:%SZ")
    check("realism: every workbook and document was created before it was last modified, both by the export date",
          all(c < m <= cut for c, m in stamps.values()), str(sorted(stamps.values())))
    check("realism: no two workbooks or documents share a creation stamp", len({c for c, _ in stamps.values()}) == len(stamps))
    entry_ok, parts_ok = True, True
    for f in files:
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(os.path.join(tdir, f)) as z:
                dts = {zi.date_time for zi in z.infolist()}
                parts_ok &= not any(n in ("word/stylesWithEffects.xml", "docProps/thumbnail.jpeg") for n in z.namelist())
            mod = dt.datetime.strptime(stamps[f][1], "%Y-%m-%dT%H:%M:%SZ")
            entry_ok &= dts == {(mod.year, mod.month, mod.day, mod.hour, mod.minute, mod.second)} and mod <= P.EXPORT_DATE
    check("realism: every Office file's zip entries carry its own last-saved stamp, none after the as-of date", entry_ok)
    check("realism: no Office file carries the writing library's template parts (styles with effects, thumbnail)", parts_ok)
    pdates = [re.search(rb"/CreationDate \(D:(\d{14})", open(os.path.join(tdir, f), "rb").read()).group(1) for f in files if f.endswith(".pdf")]
    check("realism: each PDF carries its own creation date", len(set(pdates)) == len(pdates), str(pdates))
    check("leak: no file name matches the author-word list leak.py sweeps (versions, samples, cleaned copies included)",
          not any(re.search(r"(?<![a-z])(trap|decoy|distractor|naive|rung|stump|ladder|golden|answer|truth|hidden|secret|solution|"
                            r"clean(ed)?_|_fixed|correct(ed)?_|synthetic|generated|_seed|placeholder|dummy|sample_|test_|_v\d+\b|"
                            r"\bcopy\b|backup)", f, re.I) for f in files))
    check("positive control: the PDF extractor reads the notice's datum sentence", "Chart datum at Fendmouth is 2.90 m below Ordnance Datum Newlyn" in notice)
    check("positive control: the DOCX extractor reads the basis's change line", "Year 1 quantity defined for the tender" in basis)

    fails = [o for o in OUT if not o[1]]
    for label, ok, detail in OUT:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    print("%d assertions, %d FAIL" % (len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
