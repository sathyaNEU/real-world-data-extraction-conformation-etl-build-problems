"""checks.py: the generator's assertions on the clean truth and on the cut pack (target/).

    python3 checks.py            exit 0 when every assertion passes
"""
import csv
import datetime as dt
import filecmp
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
TDIR = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import params as P          # noqa: E402
import pack                 # noqa: E402
import analysis as A        # noqa: E402
import world_ops as O       # noqa: E402
import ceiling              # noqa: E402
import docs                 # noqa: E402
from io_util import pdf_text  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def rnd(v, u):
    return int(round(v / u)) * u


def edge(v, u):
    """Distance from v to the nearest edge of its printed cell at unit u."""
    return u / 2.0 - abs(v - rnd(v, u))


def copy_without(names):
    d = tempfile.mkdtemp(prefix="t159c_")
    for f in os.listdir(TDIR):
        if f not in names:
            shutil.copy(os.path.join(TDIR, f), os.path.join(d, f))
    return d


def main():
    # ------------------------------------------------------------------ the clean truth, rebuilt
    tmp = tempfile.mkdtemp(prefix="t159t_")
    truth = pack.build(tmp)
    names = sorted(os.listdir(tmp))
    _, mism, err = filecmp.cmpfiles(tmp, TDIR, names, shallow=False)
    check("rebuild: a fresh build is byte-identical to target/", not mism and not err and names == sorted(os.listdir(TDIR)),
          (mism, err))

    files = sorted(os.listdir(TDIR))
    rows = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(TDIR, f), encoding="utf-8") as fh:
                rows[f] = sum(1 for l in fh if not l.startswith("#")) - 1
    meta = json.load(open(os.path.join(TASK, "metadata.json")))

    # ------------------------------------------------------------------ input gates
    check("gate: 10 or more files", len(files) >= 10, len(files))
    check("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, sorted({f.rsplit(".", 1)[1] for f in files}))
    check("gate: a file of 25,000 or more rows", max(rows.values()) >= 25000, max(rows.items(), key=lambda x: x[1]))
    dis = [d["file"] for d in meta["distractor_files"]]
    check("gate: two or more distractors named in metadata.json, each shipped", len(dis) >= 2 and all(d in files for d in dis), dis)
    check("gate: no file name says distractor, readme, dictionary, notes or manifest",
          not any(re.search(r"distract|readme|dictionar|notes|manifest|field_guide|schema", f, re.I) for f in files))
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            sheets += load_workbook(os.path.join(TDIR, f), read_only=True).sheetnames
    check("gate: no workbook sheet describes the data", not any(re.search(r"note|readme|dictionar|about|legend|how to", s, re.I)
                                                                 for s in sheets), sheets)

    # ------------------------------------------------------------------ the main call on the cut pack
    m = A.main_call(TDIR)
    fam = {k: m[k] for k in ("A", "B05", "B10", "B20", "C", "D")}
    p = A.paired(TDIR)
    pl = A.plan(TDIR)
    fam["D_uncentred"] = A.route_D(p, pl, centred=False)[0]
    dep = A._csv(os.path.join(TDIR, pack.F_DEPL))
    dep["ijk"] = dep["IJK"].astype(int)
    pm = p.join(dep.set_index("ijk")["MONTH"])
    for lab, sel in (("A_last12", pm["MONTH"] >= "2025-11"), ("A_last24", pm["MONTH"] >= "2024-11")):
        fam[lab] = A.route_A(pm[sel], pl)
        fam["D_" + lab[2:]] = A.route_D(pm[sel], pl)[0]
    gold = rnd(m["golden"], 10000)
    check("R1 the field's raw material ships: per-hole assays with collars, per-block estimates, the block schedule",
          rows[pack.F_LIMS] >= 25000 and m["n_pairs"] == int((truth["blocks"]["period"] == "HIST").sum()) and m["n_plan"] > 9000,
          (rows[pack.F_LIMS], m["n_pairs"], m["n_plan"]))
    hdrs = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(TDIR, f), encoding="utf-8") as fh:
                for l in fh:
                    if not l.startswith("#"):
                        hdrs += l.strip().split(",")
                        break
    check("R1 no shipped column holds a block's grade-control grade or a factor at the new cut-off",
          not any(re.search(r"GC_|_GC|F1|FACTOR|RECON", h, re.I) for h in hdrs), [h for h in hdrs if "GC" in h])
    check("main: the per-block golden prints 150,000 oz", gold == 150000, m["golden"])
    check("main: every licensed estimator prints the golden's 150,000 oz",
          all(rnd(v, 10000) == gold for v in fam.values()), {k: round(v) for k, v in fam.items()})
    check("main: every licensed estimator sits at least 1,000 oz inside the 145,000 to 155,000 cell",
          min(edge(v, 10000) for v in fam.values()) >= 1000, round(min(edge(v, 10000) for v in fam.values())))
    tfam = {"A": m["A_t"], "B05": m["B05_t"], "B10": m["B10_t"], "B20": m["B20_t"], "C": m["C_t"], "D": m["D_t"]}
    check("main: every licensed estimator's ore tonnes print 2,800,000 t", all(rnd(v, 100000) == 2800000 for v in tfam.values()),
          {k: round(v) for k, v in tfam.items()})
    check("main: the ore tonnes sit at least 15,000 t inside their cell", min(edge(v, 100000) for v in tfam.values()) >= 15000,
          round(min(edge(v, 100000) for v in tfam.values())))

    # ------------------------------------------------------------------ the three rules, executed
    rep = pdf_text(os.path.join(TDIR, pack.F_RECON))
    f1_printed = float(re.search(r"Jan 2023-Oct 2026\n(?:[\d.]+\n){11}([\d.]+)", rep).group(1))
    check("R3a analyst test: the plan's model gold times the reports' printed 0.50 g/t factor files 130,000 oz",
          rnd(m["plan_oz"] * f1_printed, 10000) == 130000, (f1_printed, round(m["plan_oz"] * f1_printed)))
    check("R3a the plan's own model gold (rung 0) files 130,000 oz", rnd(m["R0"], 10000) == 130000, round(m["R0"]))
    check("R3a the model checked right on average and kept (rung 1b) files 130,000 oz",
          rnd(m["R2"], 10000) == 130000 and abs(m["calib"] - 1) < 0.02, (round(m["R2"]), round(m["calib"], 4)))
    check("R3b the decisive step alone (the factor re-cut at 0.90 g/t on the record) files the golden",
          rnd(m["A"], 10000) == gold, round(m["A"]))
    ore_only = A.route_D(p, pl[pl["au"] >= A.NEW_CUT])[0]
    check("R3b a per-block reading over the plan's ore blocks alone (the schedule's waste left out) stays wrong",
          rnd(ore_only, 10000) != gold, round(ore_only))
    tf = p["t"][p["gc"] >= 0.5].sum() / p["t"][p["au"] >= 0.5].sum()
    check("R3b the reports' tonnage factor on the plan's tonnes stays wrong", rnd(m["plan_t"] * tf, 100000) != 2800000,
          round(m["plan_t"] * tf))
    check("R3a the correctly read past does not pin the forward factor: 0.50 and 0.90 g/t factors a sixth apart",
          m["f09"] / m["f05"] > 1.12, (round(m["f05"], 4), round(m["f09"], 4)))
    # mess neutrality, one per Layer 1 item
    for lab, kw in (("below-detection results read as zero", dict(bdl="zero")),
                    ("below-detection results read at the limit", dict(bdl="dl")),
                    ("field duplicates averaged in", dict(with_dups=True)),
                    ("over-range results capped at 10 g/t", dict(grav="cap10"))):
        q = A.paired(TDIR, **kw)
        d_oz, d_t = A.route_D(q, pl)
        check("R2 mess neutral: %s" % lab, rnd(d_oz, 10000) == gold and rnd(d_t, 100000) == 2800000,
              (round(d_oz), round(d_t)))
    lims = A._csv(os.path.join(TDIR, pack.F_LIMS))
    d_new = A.route_D(A.paired(TDIR, source="LIMS"), pl)[0]
    check("R2 mess neutral: the legacy laboratory system's rows dropped (post-migration record only)",
          rnd(d_new, 10000) == gold, round(d_new))
    g0 = A.grid(TDIR)
    x1, y1 = A.utm_to_kmg([472500.0], [5372000.0], g0)
    x2, y2 = A.utm_to_kmg([472500.0], [5372000.0], (g0[0], g0[1], g0[2], 1.0))
    hb = A.blast_holes(TDIR)
    xx, yy = A.utm_to_kmg(hb["EASTING_UTM17"].astype(float), hb["NORTHING_UTM17"].astype(float), g0)
    fx = np.minimum((xx - 10000.0) % 10.0, 10.0 - (xx - 10000.0) % 10.0)
    fy = np.minimum((yy - 20000.0) % 10.0, 10.0 - (yy - 20000.0) % 10.0)
    check("R2 mess neutral: the grid's scale factor ignored moves no collar across a block edge",
          float(np.min(np.minimum(fx, fy))) > 0.5 and abs(x1[0] - x2[0]) < 0.5, round(float(np.min(np.minimum(fx, fy))), 3))
    check("R2 the call reads no mill, dispatch, DCS, maintenance, gold room or refinery file",
          abs(A.main_call(copy_without([pack.F_MILL, pack.F_DISP, pack.F_DCS, pack.F_CMMS, pack.F_BARS, pack.F_REF,
                                        pack.F_FLEET, pack.F_INV]))["golden"] - m["golden"]) < 1e-6)
    check("R3c no plant: no row block of the laboratory export or the model repeats", _no_repeated_blocks())
    check("R3c no plant: no document argues a figure for the budget (the memo files definitions only)",
          not re.search(r"\b1[0-9]{2},[0-9]{3}\b|ounces? (?:of|for) (?:the )?budget", pdf_text(os.path.join(TDIR, pack.F_BASIS))))

    # ------------------------------------------------------------------ semantic fork table
    basis = pdf_text(os.path.join(TDIR, pack.F_BASIS))
    flat = re.sub(r"\s+", " ", basis)
    check("SF1 budget gold is contained gold, not recovered", "gold contained in the ore mined in calendar 2027" in flat)
    check("SF2 2027 is the calendar year: the schedule runs January to December 2027",
          sorted(set(pl["MONTH"])) == sorted(["Jan-27", "Feb-27", "Mar-27", "Apr-27", "May-27", "Jun-27", "Jul-27",
                                              "Aug-27", "Sep-27", "Oct-27", "Nov-27", "Dec-27"]) and "calendar 2027" in flat)
    check("SF3 ore is selected on grade control, block by block", "A block is ore when its grade-control grade is 0.90 g/t or more" in flat)
    q = A.paired(TDIR, with_dups=True)
    check("SF4 a block's grade excludes field duplicates; averaging them in prints the same call",
          "field duplicates and the laboratory's control samples are not blast-hole assays" in flat
          and rnd(A.route_D(q, pl)[0], 10000) == gold)
    check("SF5 the below-detection convention prints the same call",
          all(rnd(A.route_D(A.paired(TDIR, bdl=b), pl)[0], 10000) == gold for b in ("half", "zero", "dl")))
    check("SF6 over-range results from the gravimetric column or capped print the same call",
          rnd(A.route_D(A.paired(TDIR, grav="cap10"), pl)[0], 10000) == gold)
    check("SF7 the schedule's waste blocks are in the budget's volume (ore and waste alike), and leaving them out moves "
          "the call", "ore and waste alike" in flat and rnd(ore_only, 10000) != gold)
    mt = A.model(TDIR)
    check("SF8 the schedule's tonnes are the model's block tonnages",
          np.allclose(pl.set_index("IJK")["t"].values, mt.loc[pl["IJK"].astype(int), "t"].values))
    check("SF9 the record's window (all, last 24 or last 12 months) prints the same call",
          all(rnd(fam[k], 10000) == gold for k in ("A_last12", "A_last24", "D_last12", "D_last24")))
    check("SF10 the estimator inside the per-block family (ratios, log-normal, binned means, the re-cut factor) prints "
          "the same call", all(rnd(fam[k], 10000) == gold for k in ("A", "B05", "B10", "B20", "C", "D")))
    check("SF11 centring the ratios or not prints the same call", rnd(fam["D_uncentred"], 10000) == gold)
    check("SF12 the budget figure sits clear of its rounding line", edge(m["golden"], 10000) >= 1000, round(m["golden"]))
    check("SF13 troy ounces at 31.1034768 g", abs(A.TROY - 31.1034768) < 1e-9)
    check("SF14 the stated transformation reproduces the control monuments to a millimetre", _monuments_ok())
    check("SF15 the model carries one estimate (AU_OK)", [c for c in mt.columns if c.startswith("AU")] == ["AU_OK"])
    check("SF16 ore tonnes are tonnes of grade-control ore: every licensed route prints 2.8 Mt, the plan's model ore "
          "and the reports' tonnage factor do not", rnd(m["plan_t"], 100000) != 2800000 and rnd(m["plan_t"] * tf, 100000) != 2800000)

    # ------------------------------------------------------------------ the asks
    stock = A.stockpile(TDIR)
    loads = truth["loads"]
    st_truth = pack.stock_truth(loads, truth["lgsp_open_t"])
    check("ask stockpile: the golden equals the hauls' truth at every date",
          all(abs(a[0] - b[0]) < 1 and abs(a[1] - b[1]) < 0.5 for a, b in zip(stock.values(), st_truth)),
          [(round(a[0]), round(b[0])) for a, b in zip(stock.values(), st_truth)])
    hours = A.mill_hours(TDIR)
    stops = truth["stops"].copy()
    stops.loc[stops["unlogged"], "start"] = stops.loc[stops["unlogged"], "iso_start"]
    stops.loc[stops["unlogged"], "end"] = stops.loc[stops["unlogged"], "iso_end"]
    h_truth = [O.run_hours(stops, a, b) for a, b in O.QUARTERS]
    check("ask hours: the golden equals the recorded stops at every quarter",
          all(abs(a - b) < 1e-6 for a, b in zip(hours.values(), h_truth)), [round(a - b, 3) for a, b in zip(hours.values(), h_truth)])
    fine = A.fine_gold(TDIR)
    f_truth = O.quarter_fine(truth["bars"])
    check("ask fine gold: the golden equals the lots shared by gross weight at every quarter",
          all(abs(a - f_truth[i]) < 0.6 for i, a in enumerate(fine.values())), [round(a - f_truth[i], 2) for i, a in enumerate(fine.values())])
    edges = ([edge(v[0], 1000) for v in stock.values()] + [edge(v[1], 100) for v in stock.values()]
             + [edge(v, 1) for v in hours.values()] + [edge(v, 100) for v in fine.values()])
    check("ask figures all sit clear of their rounding lines (tonnes 80 t, gold 8 oz, hours 0.15 h, fine 10 oz)",
          min(edge(v[0], 1000) for v in stock.values()) >= 80 and min(edge(v[1], 100) for v in stock.values()) >= 8
          and min(edge(v, 1) for v in hours.values()) >= 0.15 and min(edge(v, 100) for v in fine.values()) >= 10,
          [round(e, 2) for e in edges])
    cr = ceiling.ceiling(TDIR)
    check("cracker misses every ask figure", cr["lc"] == 0, cr["lc"])
    check("mirror keeps under two fifths of the ask figures", cr["ls"] < 0.4, cr["ls"])
    check("pair ceiling at or under 60", cr["pair"] <= 60, cr["pair"])
    # each device moves its figures by several bins
    s_ph = A.stockpile(TDIR, dedup=False, asof=True)
    s_re = A.stockpile(TDIR, dedup=True, asof=False)
    check("device: the duplicate hauls move every stockpile figure by 5 cells or more",
          all(abs(a[0] - b[0]) >= 5000 and abs(a[1] - b[1]) >= 500 for a, b in zip(s_ph.values(), stock.values())))
    check("device: the reissued truck numbers move every stockpile figure by 5 cells or more",
          all(abs(a[0] - b[0]) >= 5000 and abs(a[1] - b[1]) >= 500 for a, b in zip(s_re.values(), stock.values())))
    h_dcs = A.mill_hours(TDIR, use_cmms=False)
    check("device: the shutdowns the historian missed move every quarter by 5 hours or more",
          all(a - b >= 5 for a, b in zip(h_dcs.values(), hours.values())), [round(a - b, 1) for a, b in zip(h_dcs.values(), hours.values())])
    h_old = A.mill_hours(TDIR, tags="old")
    check("device: the migrated tag moves the quarters after the DCS upgrade by 5 hours or more",
          all(abs(h_old[k] - hours[k]) >= 5 for k in ("2026 Q2", "2026 Q3")))
    f_sum = A.fine_gold(TDIR, allocate=False)
    check("device: lot fine gold on every line moves every quarter by 5 cells or more",
          all(a - b >= 500 for a, b in zip(f_sum.values(), fine.values())), [round(a - b) for a, b in zip(f_sum.values(), fine.values())])
    ref = A._csv(os.path.join(TDIR, pack.F_REF))
    nbar = ref.groupby("LOT_NO")["CLIENT_REF"].nunique()
    nlot = ref.groupby("CLIENT_REF")["LOT_NO"].nunique()
    check("device: the refinery file carries both shapes (lots of two bars and bars of two lots) in every quarter",
          (nbar > 1).sum() >= 14 and (nlot > 1).sum() >= 14, ((nbar > 1).sum(), (nlot > 1).sum()))
    check("separation: the asks' files hold no row the main call reads (the call is unchanged with them deleted)",
          abs(A.main_call(copy_without([pack.F_DISP, pack.F_DCS, pack.F_CMMS, pack.F_BARS, pack.F_REF, pack.F_FLEET,
                                        pack.F_INV]))["golden"] - m["golden"]) < 1e-6)
    for d in dis:
        r2 = A.compute(copy_without([d]))
        check("distractor deleted leaves every figure: %s" % d,
              abs(r2["main"]["golden"] - m["golden"]) < 1e-6 and r2["stockpile"] == stock and r2["hours"] == hours
              and r2["fine"] == fine)

    # ------------------------------------------------------------------ realism sweep
    disp = A._csv(os.path.join(TDIR, pack.F_DISP))
    for lab, seq in (("dispatch load ids", disp["LOAD_ID"].astype(int)),
                     ("work order numbers", A._csv(os.path.join(TDIR, pack.F_CMMS))["WONUM"].str[3:].astype(int)),
                     ("legacy sample numbers", lims.loc[lims["SOURCE_SYSTEM"] == "LEGACY-LIMS", "SAMPLE_ID"].str[2:].astype(int)),
                     ("statement numbers", pd.Series(sorted(set(ref["STATEMENT_NO"].str[3:].astype(int)))))):
        dif = np.diff(seq.values)
        check("realism: %s are not one arithmetic step" % lab, len(set(dif)) > 1, sorted(set(dif))[:6])
    mon = dep.groupby("MONTH").size()
    check("realism: blocks mined per month all differ in count (no uniform stream)", mon.nunique() > 0.8 * len(mon))
    check("realism: no headline figure is round", all(v % 100 != 0 for v in (round(m["golden"]), round(m["plan_oz"]))))
    cmms = A._csv(os.path.join(TDIR, pack.F_CMMS))
    sd = cmms[cmms["WORKTYPE"] == "SD"]
    dcs = A._csv(os.path.join(TDIR, pack.F_DCS))
    dcs_bm = dcs[dcs["TAG"].isin(["BM101.RUNNING", "GRD.BM01.RUN_STS"])]
    dloc = set(A.utc_to_local(dt.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")).strftime("%Y-%m-%d %H:%M") for t in dcs_bm["TIME_UTC"])
    same = sum(1 for a in sd["ACTSTART"] if a in dloc) + sum(1 for b in sd["ACTFINISH"] if b in dloc)
    check("realism: the maintenance system's isolation times never coincide with the DCS stop and start", same == 0, same)
    authors = set()
    for f in files:
        if f.endswith(".pdf"):
            raw = open(os.path.join(TDIR, f), "rb").read()
            authors |= set(x.decode("latin-1") for x in re.findall(rb"/Author \(([^)]*)\)", raw))
    card = json.load(open(os.path.join(REPO, ".claude", "skills", "fingerprint", "cards", "task159.json")))
    people = set(card["world"]["people"]) | {"Geotechnical engineering", "Corporate finance"}
    check("realism: every document author is a persona on the card or a department", authors <= people, authors - people)
    check("realism: the budget memo postdates the plan it cites and the reconciliation postdates October 2026",
          docs.STAMP_BASIS[2:10] >= P.PLAN_DATE.strftime("%Y%m%d") and docs.STAMP_RECON[2:10] >= "20261101")
    for d in (TDIR, os.path.join(TASK, "golden")):
        out = subprocess.run([sys.executable, os.path.join(REPO, ".claude", "skills", "reduce-house-fixes", "scripts",
                                                          "scrub_producer_metadata.py"), d, "--floor", "2023-01-01",
                              "--ceiling", "2026-11-30"], capture_output=True, text=True).stdout
        check("H1 no writer signature or out-of-band stamp in %s" % os.path.basename(d), "clean" in out, out.strip()[-120:])
    # H16: no extract carries a date after its own pull
    lim_rep = [dt.datetime.strptime(x, "%d/%m/%Y").date() if "/" in x else dt.date.fromisoformat(x)
               for x in lims["DATE_REPORTED"]]
    disp_t = pd.to_datetime(disp["TIME_UTC"].str.replace("Z", ""))
    bars_csv = A._csv(os.path.join(TDIR, pack.F_BARS))
    check("H16 no extract runs past its pull: LIMS reported by 5 Nov, dispatch by the October night shift's last haul, "
          "DCS by the end of October local, "
          "refinery statements by 6 Nov, bars, mill and maintenance by 31 Oct",
          max(lim_rep) <= P.LIMS_PULL and disp_t.max() < pd.Timestamp("2026-11-01 12:00")
          and pd.to_datetime(dcs["TIME_UTC"]).max() <= pd.Timestamp("2026-11-01 04:00")
          and max(ref["STATEMENT_DATE"]) <= pack.REFINERY_PULL.isoformat()
          and max(bars_csv["POUR_DATE"]) <= "2026-10-31" and max(cmms["ACTFINISH"]) <= "2026-10-31 23:59",
          (max(lim_rep), disp_t.max(), max(ref["STATEMENT_DATE"])))
    settled_bars = set(ref["CLIENT_REF"])
    q3 = bars_csv[bars_csv["POUR_DATE"] < "2026-10-01"]
    check("ask fine gold: every bar poured before 1 October 2026 has settled on the statements",
          all(("KL %d" % int(b.split("-")[1])) in settled_bars for b in q3["BAR_NO"]))
    import pypdf
    for f in files:
        if not f.endswith(".pdf"):
            continue
        rd = pypdf.PdfReader(os.path.join(TDIR, f), strict=True)
        strict = re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in rd.pages))
        lay = re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-layout", os.path.join(TDIR, f), "-"],
                                                 capture_output=True, text=True).stdout)
        own = re.sub(r"\s+", " ", pdf_text(os.path.join(TDIR, f)))
        first = own.split(" ")[:6]
        check("H25 %s reads under pypdf strict and pdftotext" % f, len(strict) > 200 and len(lay) > 200
              and " ".join(first[:4]) in strict and " ".join(first[:4]) in lay)
    rep_lay = subprocess.run(["pdftotext", "-layout", os.path.join(TDIR, pack.F_RECON), "-"], capture_output=True,
                             text=True).stdout
    check("H13 the reconciliation table's last column survives the page edge (every F3 value is extracted)",
          len(re.findall(r"\b\d\.\d\d\s*$", rep_lay, re.M)) >= 46)
    for f, key in ((pack.F_BASIS, "0.90 g/t or more"), (pack.F_RECON, "0.50 g/t cut-off")):
        strict = " ".join(pg.extract_text() for pg in pypdf.PdfReader(os.path.join(TDIR, f), strict=True).pages)
        lay = subprocess.run(["pdftotext", "-layout", os.path.join(TDIR, f), "-"], capture_output=True, text=True).stdout
        check("H25 %s reads under a strict parser, pdftotext and the generator's decoder" % f,
              key in re.sub(r"\s+", " ", strict) and key in re.sub(r"\s+", " ", lay) and key in re.sub(r"\s+", " ", pdf_text(os.path.join(TDIR, f))))
    for f in ("prompt.txt", "submission.md"):
        txt = open(os.path.join(TASK, f), encoding="utf-8").read()
        check("text: no em or en dash in %s" % f, "—" not in txt and "–" not in txt)
    txt_all = " ".join(pdf_text(os.path.join(TDIR, f)) for f in files if f.endswith(".pdf"))
    check("text: no em or en dash in the shipped documents", "—" not in txt_all and "–" not in txt_all)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    check("figures.json carries the call and the asks as the write-up states them",
          fig["budget_oz"] == gold and fig["ore_t_100k"] == 2800000 and len(fig["stock_rows"]) == 4
          and len(fig["hours_rows"]) == 7 and len(fig["fine_rows"]) == 7)

    shutil.rmtree(tmp, ignore_errors=True)
    fails = [r for r in RESULTS if not r[1]]
    for name, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  " + str(detail)[:300]))
    print("%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


def _no_repeated_blocks():
    for f, skip in ((pack.F_LIMS, False), (pack.F_MODEL, True)):
        with open(os.path.join(TDIR, f), encoding="utf-8") as fh:
            lines = [l.split(",", 1)[1] for l in fh if not l.startswith("#")][1:]
        seen = set()
        for i in range(0, len(lines) - 6, 3):
            k = "".join(lines[i:i + 6])
            if k in seen:
                return False
            seen.add(k)
    return True


def _monuments_ok():
    g = A.grid(TDIR)
    txt = open(os.path.join(TDIR, pack.F_GRID), encoding="utf-8").read()
    ok = True
    for m_ in re.finditer(r"KCM-\d+\s+([\d.]+)\s+([\d.]+)\s+[\d.]+\s+([\d.]+)\s+([\d.]+)", txt):
        x, y, e, n = map(float, m_.groups())
        xx, yy = A.utm_to_kmg([e], [n], g)
        ok &= abs(xx[0] - x) < 0.002 and abs(yy[0] - y) < 0.002
    return ok


if __name__ == "__main__":
    sys.exit(main())
