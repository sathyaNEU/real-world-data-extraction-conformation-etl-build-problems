"""task474 checks: the input gates, the three rules executed on the clean truth (R1 to R3c), the ladder and its
separating facts, the semantic fork table (SF1 to SF13), the Layer 1 items, every graded figure's distance to its bin
edge, the asks' devices, stops and hazards, the distractors, the realism sweep and the deliverables' agreement with
figures.json."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

import numpy as np

import askpaths as AP
import asks as A
import ceiling as C
import golden as GO
import methods as M
import pack as P
import sources as S
import world as W

RESULTS = []
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [%s]" % detail) if (detail != "" and not ok) else ""))
    return ok


def pdf_text(path):
    out = subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True, check=True).stdout
    return re.sub(r"\s+", " ", out)


def xlsx_text(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    return " ".join(str(v) for ws in wb for row in ws.iter_rows(values_only=True) for v in row if v is not None)


def docx_text(path):
    import docx
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts += [c.text for c in row.cells]
    return re.sub(r"\s+", " ", " ".join(parts))


def text_of(path):
    if path.endswith(".pdf"):
        return pdf_text(path)
    if path.endswith(".xlsx"):
        return xlsx_text(path)
    if path.endswith(".docx"):
        return docx_text(path)
    return re.sub(r"\s+", " ", open(path, encoding="utf-8").read())


def edge(v, unit):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def rounded(sm):
    return dict(amount={r: M.rnd(sm["amount"][r], 10000) for r in W.REGION_NAMES},
                avg={r: M.rnd(sm["avg"][r], 100) for r in W.REGION_NAMES},
                cells={(r, y): M.rnd(sm["series"][r][y], 100) for r in W.REGION_NAMES for y in W.LEGACY_YEARS})


def off(a, b):
    return sum(a["amount"][r] != b["amount"][r] for r in W.REGION_NAMES)


def run(target, golden, meta_path=None, fig_path=None):
    RESULTS.clear()
    files = sorted(os.listdir(target))
    path = lambda k: os.path.join(target, W.FILES[k])
    meta = json.load(open(meta_path)) if meta_path else {}
    F = json.load(open(fig_path, encoding="utf-8"))
    X = GO.compute(target)
    Pk = X["P"]

    # ------------------------------------------------------------------------------------------ input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    with open(path("extract"), encoding="utf-8") as fh:
        n_ext = sum(1 for _ in fh) - 1
    check("gates: %d files (10 or more), formats %s (3 or more), the extract %d rows (25,000 or more)" % (
        len(files), sorted(fmts), n_ext), len(files) >= 10 and len(fmts) >= 3 and n_ext >= 25000)
    check("gates: the pack is exactly the files world.FILES declares", set(files) == set(W.FILES.values()),
          sorted(set(files) ^ set(W.FILES.values())))
    dis = meta.get("distractor_files", [])
    check("gates: two distractors named in metadata.json, none named for its role", len(dis) >= 2 and all(
        d in files and "distract" not in d.lower() for d in dis), dis)

    # ------------------------------------------------------------------------------------------ the call
    R = {k: M.summary(v) for k, v in M.routes().items()}
    G = rounded(R["G"])
    gb = X["routes"]["golden"]
    check("call: the golden computed from the shipped files equals the generator's on all nine amounts",
          all(F["amounts"][r] == G["amount"][r] for r in W.REGION_NAMES), F["amounts"])
    check("call: and on the nine averages and the 27 region-years",
          all(F["average"][r] == G["avg"][r] for r in W.REGION_NAMES) and
          all(F["cells"][r][str(y)] == G["cells"][(r, y)] for r in W.REGION_NAMES for y in W.LEGACY_YEARS))
    check("call: the unrounded allocations sum to $12,000,000",
          abs(sum(gb["amount"].values()) - W.FUND) < 1e-6)
    check("call: the region figures for 2020-2022 sum to the former counties' totals each year (SF2)",
          all(abs(sum(gb["series"][g][y] for g in Pk.regions) - sum(Pk.sdc[(c, y)] for c in Pk.counties)) < 1e-6
              for y in W.LEGACY_YEARS))

    # ------------------------------------------------------------------------------------------ R block
    no_town_year = True
    with open(path("acs"), encoding="utf-8") as fh:
        hdr = fh.readline()
    no_town_year = "2020" not in hdr and "2021" not in hdr
    check("R1 the field's raw material ships: 118 towns' monthly SNAP recipients (Jan 2019 to Jun 2026), the survey's "
          "five-year town counts with margins, the model estimates by year; no file holds a town's residents in "
          "poverty for a single year", len(Pk.snap) == 118 * 90 and len(Pk.below) == 118 and no_town_year)
    # R2: each Layer 1 item, mishandled the natural way
    raw_key = {t.upper(): t for t in Pk.towns}
    raw_hits = 0
    with open(path("snap"), encoding="utf-8") as fh:
        names = {r["TOWN"] for r in csv.DictReader(fh, delimiter="|")}
    raw_hits = len([n for n in names if n in raw_key])
    check("R2 DSS's spellings: the codes file's names in capitals match %d of the 118 towns, so the mishandling is "
          "loud (missing towns); matched by DSS's abbreviations, 118 of 118" % raw_hits,
          raw_hits < 118 and not Pk.snap_unmatched)
    check("R2 DSS's UNKNOWN and STATE TOTAL rows join to no town, so reading them as rows changes nothing",
          "UNKNOWN" in names and "STATE TOTAL" in names and not ({"UNKNOWN", "STATE TOTAL"} & set(raw_key)))
    acs_by_name = {}
    with open(path("acs"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["summary_level"] == "060" and r["table_line"] == "B17001_002":
                acs_by_name[re.sub(r" (town|city),.*$", "", r["area_name"])] = int(r["estimate"])
    check("R2 the town GEO_IDs re-keyed under the region codes: joining by name instead gives the same 118 counts",
          acs_by_name == Pk.below)
    cells_ok = True
    with open(path("acs"), encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["summary_level"] == "060"]
    by_geo = {}
    for r in rows:
        by_geo.setdefault(r["geo_id"], {})[r["table_line"]] = int(r["estimate"])
    for g, v in by_geo.items():
        below_cells = sum(v["B17001_%03d" % i] for i in list(range(4, 17)) + list(range(18, 31)))
        cells_ok &= below_cells == v["B17001_002"] and v["B17001_003"] + v["B17001_017"] == v["B17001_002"]
    check("R2 the 26 age-sex cells: summed in place of the total they give the total in every town", cells_ok)
    texts_rule = pdf_text(path("rule"))
    fr = rounded(M.summary(M.series_first_release()))
    check("R2 first and revised estimates side by side: the golden reads each year's latest publication (2020 to 2023 "
          "revised, 2024 first), as rule 2.1 pins it; a year's first estimate in its place moves %d amounts (SF1)" %
          off(fr, G), all(Pk.sdc[(a, y)] == S.sdc_latest("county" if y <= 2022 else "region", a, y)
                         for (a, y) in Pk.sdc if y >= 2020) and "as last published" in texts_rule)
    wb_award = {}
    import openpyxl
    for row in openpyxl.load_workbook(path("closeout"), data_only=True)["FY2026 closeout"].iter_rows(min_row=5,
                                                                                                     values_only=True):
        if row[2]:
            wb_award[row[2]] = row[3]
    check("R2 awards in thousands against expenditures in dollars: read as dollars the unexpended balance turns "
          "negative for every agency (loud), and the main path never reads the closeout",
          all(wb_award[c] - A.BALANCES[c]["spent"] < 0 for c in W.COUNTY_NAMES))
    r0 = rounded(R["R0_window"])
    check("R3a the analyst test: the easy route on the clean truth (the release's town shares, every filed rule "
          "applied) files Greater Ormsby $%s and Mill River Valley $%s, %d of nine amounts off" % (
              "{:,}".format(r0["amount"]["Greater Ormsby"]), "{:,}".format(r0["amount"]["Mill River Valley"]),
              off(r0, G)), off(r0, G) >= 6 and r0["amount"]["Greater Ormsby"] != G["amount"]["Greater Ormsby"] and
          r0["amount"]["Mill River Valley"] != G["amount"]["Mill River Valley"])
    check("R3a and the same route read from the shipped files lands on the same amounts",
          all(F["rivals"]["release_shares"][r] == r0["amount"][r] for r in W.REGION_NAMES))
    check("R3b the decisive step alone: the easy route with only the town-year estimator changed (each town's "
          "recipients that year times its release over its mean recipients) files the golden",
          rounded(R["G"])["amount"] == G["amount"])
    lower = {k: off(rounded(R[k]), G) for k in ("R1_snap", "R7_midpoint", "R8_additive", "R2_hedge", "R4_carryback")}
    check("R3b each lower rung's single correction leaves a wrong allocation: %s" % lower, all(v >= 2 for v in lower.values()))
    texts = {k: text_of(path(k)) for k in W.FILES}
    controls = {"rule": "in proportion to each town's residents in poverty in that year",
                "methods": "counts the residents in poverty in that calendar year",
                "acs_notes": "January 1, 2020 to December 31, 2024",
                "rel2024": "does not produce planning region estimates for years before 2023",
                "layout": "town of residence",
                "rel2025": "Residents in poverty, 2024, first estimates, planning regions"}
    check("R3c positive controls: each document's text is read through the extractor the absence checks use",
          all(v in texts[k] for k, v in controls.items()), [k for k, v in controls.items() if v not in texts[k]])
    docs = [k for k in W.FILES if k not in ("snap", "extract", "audit", "conversion", "acs", "codes", "factors")]
    banned = re.compile(r"SNAP|Supplemental Nutrition|benchmark|indicator|Bellmont|Marlridge Commons|relocat|"
                        r"redevelop|temporal|disaggregat|take-up|participation rate", re.I)
    hits = {k: banned.findall(texts[k]) for k in docs if banned.search(texts[k])}
    check("R3c no plant: no document names SNAP, an indicator, a benchmark, a ratio method, the relocations or "
          "take-up", not hits, hits)
    check("R3c no memo, briefing, draft or stakeholder figure ships (the documents are the SDC's releases and methods "
          "note, the Bureau's notes, the OBP's rule, tables and closeout, the export layout)",
          all(not re.search(r"memo|draft|briefing", f, re.I) for f in files))

    # ------------------------------------------------------------------------------------------ the ladder
    names = {"R0_window": 6, "R1_snap": 6, "R7_midpoint": 3, "R8_additive": 2}
    got = {k: off(rounded(R[k]), G) for k in names}
    check("ladder: rung misses %s, each at or above its floor %s" % (got, names), all(got[k] >= v for k, v in names.items()),
          got)
    lands = [k for k in R if k not in M.GOLDEN_FAMILY and off(rounded(R[k]), G) == 0]
    check("ladder: no route outside the golden family lands the nine amounts", not lands, lands)
    distinct = {k: tuple(sorted(rounded(R[k])["amount"].items())) for k in ("R0_window", "R1_snap", "R7_midpoint",
                                                                          "R8_additive", "R2_hedge", "R4_carryback")}
    check("ladder: every rung names its own allocation", len(set(distinct.values())) == len(distinct))
    m = lambda n, y, mo: Pk.snap[(n, y, mo)][1]
    four = ("Fenbrook", "Tilcombe", "Carrholt", "Draywick")
    drop = m("Ormsby", 2021, 3) - m("Ormsby", 2022, 1)
    rise = sum(m(t, 2022, 1) - m(t, 2021, 3) for t in four)
    before = abs(m("Ormsby", 2021, 3) - m("Ormsby", 2020, 11))
    check("ladder: the SNAP counts date the Ormsby move (recipients down %d from March 2021 to January 2022, the four "
          "Mill River towns up %d) and show nothing like it before April 2021 (%d over the four months before)" % (
              drop, rise, before), drop > 4000 and rise > 3000 and before < 600)
    ch = {r: abs(Pk.sdc[(r, 2024)] / Pk.sdc[(r, 2023)] - 1) for r in Pk.regions}
    check("ladder: no published estimate shows the move: every region changes under 2 per cent from 2023 to 2024 "
          "(largest %.1f)" % (100 * max(ch.values())), max(ch.values()) < 0.02)
    rat = X["ratio"]
    check("ladder: the towns' release over mean recipients runs %.2f to %.2f (R1 dies to it)" % (
        min(rat.values()), max(rat.values())), max(rat.values()) / min(rat.values()) > 3)
    st = {y: sum(Pk.sdc[(g, y)] for g in Pk.regions) for y in W.NATIVE_YEARS}

    def backtest(est):
        e = []
        for y in W.NATIVE_YEARS:
            pred = {g: sum(est(t, y) for t in Pk.towns if Pk.region_of[t] == g) for g in Pk.regions}
            tt = sum(pred.values())
            e += [abs(st[y] * pred[g] / tt / Pk.sdc[(g, y)] - 1) for g in Pk.regions]
        return max(e)
    sy = lambda t, y: Pk.snap_year(t, y)
    bt_g = backtest(lambda t, y: sy(t, y) * rat[t])
    bt_0 = backtest(lambda t, y: float(Pk.below[t]))
    check("oracles: the 2023-2024 region estimates confirm no route (the golden's own town sums miss by up to %.1f per "
          "cent, the release's by %.1f)" % (100 * bt_g, 100 * bt_0), bt_g > 0.04 and bt_0 > 0.04)

    # ------------------------------------------------------------------------------------------ the fork table
    check("SF1 each year's first estimate moves %d amounts, %d averages and %d cells; closed by rule 2.1 'as last "
          "published'" % (off(fr, G), sum(fr["avg"][r] != G["avg"][r] for r in W.REGION_NAMES),
                          sum(fr["cells"][k] != G["cells"][k] for k in G["cells"])), "as last published" in texts["rule"])
    check("SF2 rule 2.2 divides each former county's estimate among its towns",
          "each former county's estimate is divided among the former county's towns" in texts["rule"])
    fam = {}
    for kind, months in (("ffy", [(-1, 10), (-1, 11), (-1, 12)] + [(0, mm) for mm in range(1, 10)]),
                         ("sfy", [(-1, mm) for mm in range(7, 13)] + [(0, mm) for mm in range(1, 7)]),
                         ("dec", [(0, 12)]), ("jul", [(0, 7)])):
        def yv(t, y, months=months):
            return np.mean([S.SNAP[(t["name"], y + dy, mm)]["recipients"] for dy, mm in months])

        def est(t, y, yv=yv):
            return yv(t, y) * S.ACS[t["name"]]["below"] / np.mean([yv(t, yy) for yy in range(2020, 2025)])
        fam[kind] = off(rounded(M.summary(M.series(est))), G)
    check("SF3 'that year' is the calendar year: a federal-fiscal, State-fiscal, December or July SNAP year moves %s "
          "amounts; closed by the methods note and the Bureau's notes" % fam,
          max(fam.values()) >= 2 and "in that calendar year" in texts["methods"]
          and "January 1, 2020 to December 31, 2024" in texts["acs_notes"])
    check("SF4 the release read as 2022 (R7) moves %d amounts; the Bureau's notes make it the 60 months' average" %
          got["R7_midpoint"], got["R7_midpoint"] >= 3 and "average characteristics of the population over the 60 "
          "months" in texts["acs_notes"])
    hh = rounded(R["G_households"])
    check("SF5 SNAP households for recipients: every graded main figure in the same bin (C1)",
          hh["amount"] == G["amount"] and hh["avg"] == G["avg"] and hh["cells"] == G["cells"])
    pc = rounded(R["G_piece"])
    spread = []
    for c in W.COUNTY_NAMES:
        for g in W.REGION_NAMES:
            rs = [rat[t["name"]] for t in W.TOWNS if t["county"] == c and t["region"] == g]
            if len(rs) > 1:
                spread.append(max(rs) / min(rs))
    check("SF6 the piece-pooled ratio moves %d amount(s) and up to %d persons in a cell; the rule divides by each "
          "town's own figure and the ratios differ inside every piece (narrowest spread %.2fx)" % (
              off(pc, G), max(abs(pc["cells"][k] - G["cells"][k]) for k in G["cells"]), min(spread)),
          "in proportion to each town's residents in poverty in that year" in texts["rule"] and min(spread) > 1.1)
    Y = (2019, 2020, 2021, 2022)
    est19 = {}
    import bundle as B
    t, yr = B.release_tables(path("rel2021"))
    for area, v in t[2].items():
        est19[area] = v
    panel = {c: [est19[c]] + [Pk.sdc[(c, y)] for y in (2020, 2021, 2022)] for c in Pk.counties}
    snapc = {c: [sum(Pk.snap_year(tw, y) for tw in Pk.towns if Pk.county_of[tw] == c) for y in Y] for c in Pk.counties}
    lr = np.array([[np.log(panel[c][i] / snapc[c][i]) for i in range(4)] for c in Pk.counties])
    df = np.array([[panel[c][i] - snapc[c][i] for i in range(4)] for c in Pk.counties])
    tw2 = lambda a: a - a.mean(1, keepdims=True) - a.mean(0, keepdims=True) + a.mean()
    rl = float(np.sqrt((tw2(lr) ** 2).mean()))
    rd = np.abs(tw2(df)) / np.array([panel[c] for c in Pk.counties])
    check("SF7 the former counties' estimates against their recipients, 2019 to 2022, move by one statewide ratio "
          "(two-way residual %.2f per cent) and not by one difference (up to %.1f per cent)" % (100 * rl, 100 * rd.max()),
          rl < 0.006 and rd.max() > 0.10 and got["R8_additive"] >= 2)
    check("SF8 rule 2.3 weighs the five years equally", "each year with equal weight" in texts["rule"])
    region_by_geo = {r["town"]: r["region_fips"] for r in Pk.codes}
    geo_ok = all(r["town_geoid_region_basis"][:5] == r["region_fips"] for r in Pk.codes)
    check("SF9 the codes file's 118 towns, each GEO_ID's region prefix the codes file's region",
          len(Pk.codes) == 118 and geo_ok and len(region_by_geo) == 118)
    ra = {r: M.rnd(R["G"]["avg"][r], 100) for r in W.REGION_NAMES}
    tot = sum(ra.values())
    moved = [r for r in W.REGION_NAMES if M.rnd(W.FUND * ra[r] / tot, 10000) != G["amount"][r]]
    check("SF10 amounts from the averages rounded to hundreds move %s; rule 2.4 computes from the unrounded "
          "averages" % (moved or "none"), "computed from the unrounded averages" in texts["rule"])
    check("SF11 the carry-in is paid in addition to the FY2027 allocation (rule 3.1)",
          "in addition to their FY2027 allocations" in texts["rule"])
    check("SF12 one council per planning region, nine (rule 1.1)",
          "nine regional councils of governments, one for each planning region" in texts["rule"])
    first22 = B.release_tables(path("rel2023"))[0][1]
    check("SF13 the 2022 figures are the transition report's revisions, which differ from December 2023's first "
          "estimates for %d of 8 counties" % sum(first22[c] != Pk.sdc[(c, 2022)] for c in Pk.counties),
          all(Pk.sdc[(c, 2022)] == S.sdc_latest("county", c, 2022) for c in Pk.counties)
          and any(first22[c] != Pk.sdc[(c, 2022)] for c in Pk.counties))

    # ------------------------------------------------------------------------------------------ bins
    gs, gh = R["G"], R["G_households"]
    ma = min(edge(gs["amount"][r], 10000) - abs(gh["amount"][r] - gs["amount"][r]) for r in W.REGION_NAMES)
    mv = min(edge(gs["avg"][r], 100) - abs(gh["avg"][r] - gs["avg"][r]) for r in W.REGION_NAMES)
    mc = min(edge(gs["series"][r][y], 100) - abs(gh["series"][r][y] - gs["series"][r][y])
             for r in W.REGION_NAMES for y in W.LEGACY_YEARS)
    ea = min(edge(gs["amount"][r], 10000) for r in W.REGION_NAMES)
    check("bins: every graded main figure clears its edge by more than the family's spread (amounts by $%.0f or more, "
          "averages %.1f, cells %.1f; the tightest amount $%.0f from its edge)" % (ma, mv, mc, ea),
          ma >= 800 and mv >= 3 and mc >= 2)
    ag = A.golden()
    eca = min(edge(ag["carry"][r], 100) for r in W.REGION_NAMES)
    ene = min(edge(ag["energy"][r], 100) for r in W.REGION_NAMES)
    check("bins: every carry-in at least $8 from its $100 edge (%.1f), every energy figure $8 (%.1f)" % (eca, ene),
          eca >= 8 and ene >= 8)

    # ------------------------------------------------------------------------------------------ asks
    ext, aud, conv, bal = Pk.asks_inputs()
    gold = C.ask_figures(ag)
    stops = {k: C.ask_figures(AP.figures(ext, aud, conv, bal, **kw)) for k, kw in AP.STOPS.items()}
    hit = lambda s, k: sum(stops[s][k + "." + r] == gold[k + "." + r] for r in W.REGION_NAMES)
    check("ask: the golden handling of the shipped rows recovers the truth exactly (27 of 27)",
          all(stops["golden"][k] == gold[k] for k in gold))
    check("ask: the careful path (the extract's town and numbers as they stand, energy summed on the rows) misses all "
          "27", all(hit("careful", k) == 0 for k in ("carry", "people", "energy")))
    want = {"history only": (7, 7, 0), "conversion only": (0, 0, 0), "one payment per household only": (0, 0, 0),
            "history and one payment per household": (7, 7, 9), "conversion and one payment per household": (0, 0, 0)}
    gotst = {s: (hit(s, "carry"), hit(s, "people"), hit(s, "energy")) for s in want}
    check("ask: the stops as tabled %s" % gotst, gotst == want, gotst)
    ck = stops["careful"]
    gap_c = min(abs(ck["carry." + r] - gold["carry." + r]) for r in W.REGION_NAMES)
    gap_p = min(abs(ck["people." + r] - gold["people." + r]) for r in W.REGION_NAMES)
    check("ask: the careful path misses every carry-in by $%d or more and every count by %d or more" % (gap_c, gap_p),
          gap_c >= 300 and gap_p >= 8)
    whole = stops["every row the extract holds"]
    check("ask hazard: the extract kept whole moves asks A and B (%d of 18 kept) and not ask C" % (
        hit("every row the extract holds", "carry") + hit("every row the extract holds", "people")),
          hit("every row the extract holds", "carry") + hit("every row the extract holds", "people") <= 2 and
          hit("every row the extract holds", "energy") == 9)
    nodup = C.ask_figures(AP.figures(ext, aud, conv, bal, dedup=False))
    check("ask hazard: the twice-received upload moves no figure", nodup == gold)
    G_ = P.grants()
    resent = [x for x in G_["rows"] if x.get("resent")]
    check("ask: Wexmoor's April 2026 upload appears twice (%d rows), every repeated row an exact copy" % len(resent),
          len(resent) > 500 and all(x["agency"] == "Wexmoor" and dt.date(2026, 4, 1) <= x["entered"] <=
                                    dt.date(2026, 4, 30) for x in resent))
    moves = A.DATA["moves"]
    cross = [h for h in moves if A.council_of(h["home"]) != A.council_of(h["move"][0])]
    town_edits = [a for a in aud if a[2] == "town"]
    check("ask device D2: %d households moved in FY2026, %d across council lines; %d town edits among %d audit rows, "
          "each with an effective date" % (len(moves), len(cross), len(town_edits), len(aud)),
          len(cross) > 1000 and all(a[5] for a in town_edits) and len(town_edits) < 0.25 * len(aud))
    old = {r[1] for r in ext if r[0] == "CCA" and r[5] < "2026-01-01"}
    mp = {a: b for a, b, _ in conv}
    check("ask device D7: every Corbin client number entered before 2026 is in the conversion, one to one",
          old <= set(mp) and len(set(mp.values())) == len(mp))
    pay_rows = [r for r in ext if r[3] == "EA"]
    pays = {(r[2], r[4], r[7]) for r in pay_rows}
    check("ask device D6: %d energy assistance rows carry %d payments" % (len(pay_rows), len(pays)),
          len(pay_rows) > 1.8 * len(pays))
    check("separation: the main path reads no Fund record (the golden's routes use the releases, the survey table, the "
          "SNAP counts and the codes file only)", set(X["routes"]) == {"golden", "release_shares", "snap_shares",
                                                                   "middle_year"})

    # ------------------------------------------------------------------------------------------ distractors
    tmp = tempfile.mkdtemp()
    try:
        same = []
        for d in dis:
            sub = os.path.join(tmp, d.rsplit(".", 1)[0])
            shutil.copytree(target, sub)
            os.remove(os.path.join(sub, d))
            try:
                Y_ = GO.compute(sub)
                Fd = GO.figures(Y_)
                same.append(Fd["amounts"] == F["amounts"] and Fd["asks"] == F["asks"])
            except Exception:
                same.append(False)
        check("distractors: each deleted, the golden and every ask figure unchanged", all(same) and len(same) >= 2)
    finally:
        shutil.rmtree(tmp)
    r3 = rounded(R["R3_pop_factors"])
    check("wrong-basis distractor: the allocation factors give a split that is neither the golden nor rung 0 (%d and %d "
          "amounts off)" % (off(r3, G), off(r3, r0)), off(r3, G) >= 6 and off(r3, r0) >= 6)

    # ------------------------------------------------------------------------------------------ realism
    dash = [k for k, v in texts.items() if "—" in v or "–" in v]
    check("realism: no en or em dash in any shipped file", not dash, dash)
    people = set(W.PEOPLE.values())
    named = set(re.findall(r"(Wendy Taylor|Martin Estrada|Paige Hodges)", " ".join(texts.values())))
    card = json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task474.json")))
    check("realism: every persona is the card's (guard.py names)", named <= set(card["world"]["people"]) and
          named == people)
    late_ext = max(r[5] for r in ext)
    late_svc = max(r[4] for r in ext)
    late_aud = max(a[6] for a in aud)
    check("realism: no extract or audit date after the September 30, 2026 cut (entered %s, served %s, audit %s)" % (
        late_ext, late_svc, late_aud), late_ext <= "2026-09-30" and late_svc <= "2026-09-30" and late_aud <= "2026-09-30")
    import build as BD
    late = {}
    for k in W.FILES:
        if k in ("snap", "extract", "audit", "conversion", "acs", "codes", "factors"):
            continue
        yrs = [int(v) for v in re.findall(r"(?<!\d)(20\d\d)(?!\d)", texts[k])]
        own = int(BD.AS_OF[k][:4])
        if yrs and max(yrs) > own + 1:
            late[k] = max(yrs)
    check("realism: DSS runs January 2019 to June 2026, and no document names a year more than one past its own date",
          max(k[1] * 100 + k[2] for k in Pk.snap) == 202606 and not late, late)
    import itertools
    series = {}
    for (tn, y, mo), (h, rc) in sorted(Pk.snap.items()):
        series.setdefault(tn, []).append(rc)
    runs = {tn: max(sum(1 for _ in g) for _, g in itertools.groupby(v)) for tn, v in series.items()}
    check("realism sweep: no two towns share a SNAP series and no town holds one count more than four months running "
          "(longest run %d)" % max(runs.values()),
          len({tuple(v) for v in series.values()}) == len(series) and max(runs.values()) <= 4)
    totals = [sum(Pk.sdc[(c, y)] for c in Pk.counties) for y in W.LEGACY_YEARS] + [st[2023], st[2024]]
    check("realism sweep: no State total, balance or award total on a round thousand",
          all(v % 1000 for v in totals) and all(A.BALANCES[c]["unspent"] % 100 for c in W.COUNTY_NAMES))
    ids = [(r[0], r[1]) for r in ext]
    agency_of = {}
    clash = 0
    for a, c_ in ids:
        if agency_of.setdefault(c_, a) != a:
            clash += 1
    check("realism: every client number belongs to one agency, and the old and new Corbin ranges do not overlap",
          clash == 0 and not (set(mp) & set(mp.values())))
    with zipfile.ZipFile(path("closeout")) as z:
        core = z.read("docProps/core.xml").decode()
    check("realism: the workbooks carry their owners' stamps, not the writing library's",
          "openpyxl" not in core and W.PEOPLE["grants"] in core)

    # ------------------------------------------------------------------------------------------ deliverables
    with open(os.path.join(golden, W.DELIVERABLES[0]), encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    csv_ok = all(int(r["residents_in_poverty_%d" % y]) == F["cells"][r["planning_region"]][str(y)]
                 for r in rows for y in W.LEGACY_YEARS) and all(
        int(r["average_2020_2024"]) == F["average"][r["planning_region"]] for r in rows)
    check("deliverables: the CSV's 27 region-years and nine averages are figures.json's", csv_ok and len(rows) == 9)
    memo = docx_text(os.path.join(golden, W.DELIVERABLES[1]))
    fm = lambda v: "{:,}".format(v)
    need = ["$" + fm(F["amounts"][g]) for g in Pk.regions] + ["$" + fm(F["asks"]["carry"][g]) for g in Pk.regions] + \
        [fm(F["asks"]["people"][g]) for g in Pk.regions] + ["$" + fm(F["asks"]["energy"][g]) for g in Pk.regions]
    miss = [n for n in need if n not in memo]
    check("deliverables: the memo states every amount and every transition figure as figures.json has it", not miss,
          miss[:5])
    with zipfile.ZipFile(os.path.join(golden, W.DELIVERABLES[1])) as z:
        has_chart = any(n.startswith("word/media/") for n in z.namelist())
    check("deliverables: the memo carries the bar chart of the nine amounts", has_chart)
    task = os.path.dirname(target)
    fc = subprocess.run(["python3", os.path.join(REPO, ".claude", "skills", "determinism-check", "figures_check.py"),
                         task, "--quiet"], capture_output=True, text=True)
    check("deliverables: figures_check.py passes on submission.md", fc.returncode == 0, fc.stdout.strip()[-200:])
    # ------------------------------------------------------------------------------------------ house fixes
    scrub = os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    audits = [subprocess.run(["python3", scrub, d], capture_output=True, text=True).stdout for d in (target, golden)]
    check("H1 no writer signature or out-of-band stamp in the pack or the goldens",
          all("clean" in a for a in audits), audits)
    sub = open(os.path.join(task, "submission.md"), encoding="utf-8").read()
    cited = set(re.findall(r"\b[\w-]+\.(?:pdf|xlsx|csv|txt|docx)\b", sub))
    shipped = set(files) | set(W.DELIVERABLES)
    headers = set()
    for k in ("snap", "acs", "codes", "extract", "audit", "conversion"):
        with open(path(k), encoding="utf-8") as fh:
            headers |= set(re.split(r"[,|]", fh.readline().strip()))
    fields = {"RECIPIENTS", "town_geoid_region_basis", "effective_date", "household_no", "service_date"}
    sections = all(("%s " % sec) in texts["rule"] for sec in F["rule_sections"].values())
    check("H8 every file, field, table and rule section the write-up cites exists (%d files)" % len(cited),
          cited <= shipped and fields <= headers and "B17001_002" in texts["acs"] and "Unexpended" in texts["closeout"]
          and sections and all("Table 2" in texts[k] for k in ("rel2022", "rel2023", "rel2024")),
          sorted(cited - shipped))
    found = []
    for root, dirs, fs in os.walk(task):
        dirs[:] = [d for d in dirs if not d.endswith(".tmp")]
        found += [os.path.relpath(os.path.join(root, f), task) for f in fs if f in ("submission.md", "prompt.txt",
                                                                                   "prompt.md")]
    check("H11 exactly one submission.md and one prompt.txt in the task tree", sorted(found) == ["prompt.txt",
                                                                                         "submission.md"], found)
    import logging
    import pypdf
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    strict_ok = []
    for k in W.FILES:
        if not W.FILES[k].endswith(".pdf"):
            continue
        rd = pypdf.PdfReader(path(k), strict=True)
        txt = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in rd.pages))
        strict_ok.append(len(txt) > 400 and (k not in controls or controls[k].split(" ")[0] in txt))
    check("H25 every PDF opens in a strict reader and its text extracts (%d PDFs)" % len(strict_ok), all(strict_ok))
    fails = [r for r in RESULTS if not r[1]]
    print("checks: %d assertions, %d failed" % (len(RESULTS), len(fails)))
    return not fails


if __name__ == "__main__":
    t = os.path.join(os.path.dirname(HERE), "target")
    run(t, os.path.join(os.path.dirname(HERE), "golden"), os.path.join(os.path.dirname(HERE), "metadata.json"),
        os.path.join(HERE, "figures.json"))
