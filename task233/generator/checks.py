"""The generator's assertions on the clean truth and the cut pack. Exit 1 on any failure.

    python3 checks.py <target_dir> <golden_dir>
"""
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict

import params as P
import analysis
from io_util import pdf_text
from world import World

RESULTS = []
CODE = {"Compliant": "C", "Corrective action": "A", "Service credit": "S"}
GOLDEN_VECTOR = "CACCSCACCACACC"      # CR01 to CR14
DEFAULT_VECTOR = "CACASASAASASAA"


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))


def vec(p, acc):
    return "".join(CODE[p.outcome(acc[r])] for r in p.regions)


def edge(v, edges):
    return min(abs(v - e) for e in edges)


def round_edge(v):
    """distance from a one-decimal value to the nearest rounding edge (0.05 means dead centre)"""
    return 0.05 - abs(v - round(v, 1))


def main(target, golden):
    w = World()
    res = analysis.run(target)
    p = res["pack"]
    R = p.regions
    edges = [p.band_compliant, p.band_credit]
    files = sorted(os.listdir(target))

    # input gates --------------------------------------------------------------------------------
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("G2 three or more formats", len(fmts) >= 3, ",".join(sorted(fmts)))
    with open(os.path.join(target, "cpi_field_quotes_2025-10_2026-09.csv")) as fh:
        nrows = sum(1 for _ in fh) - 1
    ok("G3 a file of 25,000 rows or more", nrows >= 25000, "%d rows" % nrows)
    meta = json.load(open(os.path.join(os.path.dirname(target.rstrip("/")), "metadata.json"))) if os.path.exists(
        os.path.join(os.path.dirname(target.rstrip("/")), "metadata.json")) else None
    dis = meta["distractor_files"] if meta else []
    ok("G4 two or more distractors, present in the pack", len(dis) >= 2 and all(os.path.exists(os.path.join(target, os.path.basename(d))) for d in dis), str(dis))
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|codebook|schema|guide|glossary", f, re.I)]
    ok("G5 no file describing the data", not bad, str(bad))
    bad = [f for f in files if re.search(r"test|trap|decoy|distract|answer|golden|stump", f, re.I)]
    ok("G6 no file named after the task", not bad, str(bad))

    # the three rules --------------------------------------------------------------------------------
    heads = []
    for f in files:
        if f.endswith(".csv"):
            heads += open(os.path.join(target, f)).readline().lower().split(",")
    bad = [h for h in heads if re.search(r"lag|delay|accura|frequen|chang|probab|error|days_since", h)]
    ok("R1 no shipped column holds a delay, change chance or accuracy", not bad, str(bad))
    ok("R1 the golden reads the back-checks, the visit log and the price database's monthly prices",
       len(p.counted()) > 5000 and len(p.visit_days) > 800 and len(p.quotes) > 50000,
       "%d back-checks, %d outlet-months visited, %d quote-months" % (len(p.counted()), len(p.visit_days), len(p.quotes)))
    gold = res["golden"]
    gvec = vec(p, gold)
    ok("C1 golden outcomes", gvec == GOLDEN_VECTOR, gvec)
    # R2: each Layer 1 item mishandled leaves the call where it was
    mess = mess_variants(target)
    for name, acc in mess.items():
        ok("R2 %s leaves every outcome" % name, vec(p, acc) == GOLDEN_VECTOR, vec(p, acc))
    # R3a, R3b on the clean truth (the world before any export)
    clean_def, clean_gold, clean_nofv = clean_routes(w)
    ok("R3a the easy route on the clean truth files the named wrong answer", clean_def == DEFAULT_VECTOR, clean_def)
    ok("R3b the easy route with only the decisive step files the golden", clean_gold == GOLDEN_VECTOR, clean_gold)
    ok("R3b setting fruit and vegetables aside alone stays wrong", clean_nofv != GOLDEN_VECTOR, clean_nofv)
    dup_bc = len(p.backchecks) != p.bc_raw
    ok("R3c no copied block in the back-check register", not dup_bc, "%d raw, %d distinct" % (p.bc_raw, len(p.backchecks)))
    ok("R3c re-sent upload rows differ in their load batch", resent_rows_differ(target))
    ok("R3c no memo, draft or briefing ships", not [f for f in files if re.search(r"memo|draft|brief|email|minutes", f, re.I)])

    # the call and its rungs --------------------------------------------------------------------------
    agree = p.agreement()
    dvec = vec(p, agree)
    ok("C2 default path (raw agreement) outcomes", dvec == DEFAULT_VECTOR, dvec)
    ok("C2 default path wrong on ten regions", sum(a != b for a, b in zip(dvec, gvec)) == 10)
    nofv = {}
    for r in R:
        v = [b for b in p.counted() if b["region"] == r and p.item_class[b["item"]] not in ("01.1.6", "01.1.7")]
        nofv[r] = 100.0 * sum(abs(b["rec"] - b["fqt"]) < 0.005 for b in v) / len(v)
    ok("C3 rung 1 (fruit and vegetables set aside) names a wrong set", vec(p, nofv) != gvec and vec(p, nofv) != dvec, vec(p, nofv))
    pers = p.persistence()
    ok("C4 rung 2 (price persistence read quote by quote) names a wrong set", vec(p, pers) != gvec and vec(p, pers) not in (dvec, vec(p, nofv)), vec(p, pers))
    fam = {}
    for key in ("class", "item", "stratum", "all"):
        for form in ("exp", "lin"):
            fam["%s %s" % (key, form)] = p.netted(key=key, form=form)
    fam["Q3 window"] = p.netted(months=["2026-07", "2026-08", "2026-09"])
    fam["Jan to Sep window"] = p.netted(months=[m for m in p.months if m >= "2026-01"])
    fam["index day as visit date (SF2)"] = p.netted(basis="index")
    fam["consistent working days (SF9)"] = workday_variant(p)
    fam["error-netted frequency (SF11)"] = error_netted(p)
    bad = [k for k, v in fam.items() if vec(p, v) != gvec]
    ok("C5 SF11 every member of the netting family names the golden set", not bad, str(bad))
    mind = min((edge(v[r], edges), k, r) for k, v in fam.items() for r in R)
    ok("C6 every family member at least 0.25 points from a band edge", mind[0] >= 0.25, "%.3f %s %s" % mind)
    dmin = min((edge(agree[r], edges), r) for r in R)
    ok("C7 the default path's figures at least 0.3 points from a band edge", dmin[0] >= 0.3, "%.3f %s" % dmin)
    ok("C8 no golden accuracy above 100 per cent", max(gold.values()) < 100.0, "%.2f" % max(gold.values()))
    ok("C9 golden service credit 1,775.20", abs(res["credit"] - 1775.20) < 0.005, "%.2f" % res["credit"])
    dcred = p.credit(p.outcomes(agree))
    ok("C9 default service credit 7,049.40", abs(dcred - 7049.40) < 0.005, "%.2f" % dcred)
    ok("C10 SF12 the credit sits clear of a whole-dollar rounding edge", abs(abs(res["credit"] - round(res["credit"])) - 0.5) >= 0.2)
    truth = population_truth(w)
    ok("C11 the golden matches the collectors' accuracy over every price they recorded", truth == gvec, truth)
    flips = [r for r in R if CODE[p.outcome(gold[r])] != CODE[p.outcome(agree[r])]]
    worth = min(gold[r] - agree[r] for r in flips)
    spread = max(max(v[r] for v in fam.values()) - min(v[r] for v in fam.values()) for r in R)
    ok("C12 the decisive step's worth exceeds the family's spread", worth > 1.4 and spread < 0.9 and worth > spread,
       "worth %.2f, spread %.2f" % (worth, spread))
    ok("C13 corrective and credit regions are not an interval of the raw agreement",
       not is_interval([r for r in R if gvec[R.index(r)] != "C"], agree), "")

    # separation of the asks' devices from the call's population ------------------------------------------
    bc_oids = {(b["oid"], b["y"], b["m"]) for b in w.backchecks}
    take = {o["oid"] for o in w.outlets if o["chain"] in ("Lifeline Chemists", "CareMed Pharmacy")}
    ok("S1 no back-check at a sold branch or its successor", not [k for k in bc_oids if k[0] in take])
    rep_oids = {w.quotes[q]["oid"] for (q, y, m) in w.forced}
    ok("S2 no back-check at an outlet carrying a repeated replacement", not [k for k in bc_oids if k[0] in rep_oids])
    bad = [k for k in bc_oids if len(w.vis_index[k]["days"]) != 1 or w.vis_index[k]["days"][0] not in w.vis_index[k]["win"][:4]]
    ok("S3 every back-checked outlet-month had one visit inside the window's first four days", not bad, str(bad[:3]))
    single = all(len(p.visit_days[(p.by_code[b["outlet"]]["Contractor outlet no."], b["month"])]) == 1 for b in p.counted())
    ok("S4 SF10 every back-check finds exactly one visit row in the log", single)

    # semantic forks --------------------------------------------------------------------------------
    ok("SF1 the estimate reads every back-checked price found, both outlet types and all three months",
       {b["month"] for b in p.counted()} == set(analysis.QUARTER) and {p.stratum(b["outlet"]) for b in p.counted()} == {"M", "I"})
    ok("SF2 the standard names the time the collector recorded the price", "at the time the collector recorded it" in p.pcqs_text)
    without_r = netted_without_replacements(p)
    ok("SF3 replacement prices kept or dropped name the same set", vec(p, without_r) == gvec, vec(p, without_r))
    ok("SF4 items the officer could not find are left out (3.2)", "Items the officer cannot find are left out" in p.pcqs_text)
    ok("SF5 bands compared without rounding (3.3)", "as estimated, without rounding" in p.pcqs_text)
    ok("SF6 the back-check register holds each price once", not dup_bc)
    ok("SF7 re-sent uploads kept or dropped name the same set", vec(p, mess["re-sent uploads kept"]) == gvec)
    ok("SF8 status 30 read as a same-variety price names the same set", vec(p, mess["status 30 read as same variety"]) == gvec)
    ok("SF9 calendar or working days name the same set", vec(p, fam["consistent working days (SF9)"]) == gvec)
    ok("SF13 the register's region is the back-check register's region",
       all(p.by_code[b["outlet"]]["Region"] == b["region"] for b in p.counted()))

    # asks ------------------------------------------------------------------------------------------
    tim, missed = res["timeliness"], res["missed"]
    ntim, nmiss = p.timeliness(follow_takeover=False)
    ok("A1 timeliness moves in every region when the sale is not followed", all(abs(tim[r] - ntim[r]) >= 0.1 for r in R))
    ok("A2 missed visits move in every region when the sale is not followed", all(nmiss[r] != missed[r] for r in R))
    htim, _ = p.timeliness(holidays=False)
    ok("A3 the August holiday moves timeliness in most regions", sum(abs(tim[r] - htim[r]) >= 0.1 for r in R) >= 10)
    acc, ntot = res["acceptance"], res["replacements"]
    acc_q, _ = p.acceptance(assign="all")
    ok("A4 acceptance moves in every region when decisions are read per quote", all(abs(acc[r] - acc_q[r]) >= 0.1 for r in R))
    ok("A5 timeliness shares sit clear of a rounding edge", min(round_edge(tim[r]) for r in R) >= 0.0005,
       "%.4f" % min(round_edge(tim[r]) for r in R))
    ok("A6 acceptance shares sit clear of a rounding edge", min(round_edge(acc[r]) for r in R) >= 0.0005,
       "%.4f" % min(round_edge(acc[r]) for r in R))
    ok("A7 every region carries replacements in the quarter", all(ntot.get(r, 0) >= 5 for r in R), str(ntot))
    truth_tim = truth_timeliness(w, p)
    ok("A8 timeliness and missed visits match the world's visits", truth_tim == ({r: round(tim[r], 6) for r in R}, missed))
    ok("A9 acceptance matches the world's decisions", truth_acceptance(w) == {r: round(acc[r], 6) for r in R})

    # realism sweep --------------------------------------------------------------------------------
    for f, col in (("cpi_field_quotes_2025-10_2026-09.csv", "quote_id"), ("tallis_visit_log_2026-07_2026-09.csv", "visit_ref")):
        vals = sorted({int(re.sub(r"\D", "", r[col])) for r in csv.DictReader(open(os.path.join(target, f)))})
        steps = {b - a for a, b in zip(vals, vals[1:])}
        ok("Z1 %s is not an arithmetic sequence" % col, len(steps) > 3)
    codes = sorted(int(o["Outlet code"][2:]) for o in p.outlets)
    ok("Z1 outlet codes are not an arithmetic sequence", len({b - a for a, b in zip(codes, codes[1:])}) > 3)
    names = [p.region_name[r] for r in R]
    ok("Z2 region names are not in alphabetical order by code", names != sorted(names))
    shapes = {re.sub(r"[A-Z][a-z']+", "W", o["Outlet name"]) for o in p.outlets}
    ok("Z3 outlet names take more than two shapes", len(shapes) > 2, str(len(shapes)))
    counts = [len([b for b in p.counted() if b["region"] == r]) for r in R]
    ok("Z4 back-check counts vary by region", len(set(counts)) == len(counts), str(counts))
    ok("Z5 no extract carries a date after its pull", dates_in_range(p))
    pc = pdf_text(os.path.join(target, "pcqs_price_collection_quality_standard_v3.pdf"))
    ok("Z7 PCQS read back (positive control) and its bands parsed", "collection window" in pc and p.band_compliant == 98.0 and p.band_credit == 96.0)
    ok("Z7 Schedule 4 fees read back for every region", len(p.fees) == len(R) and all(r in p.fees for r in R))
    sig = toolchain_signatures(target) + toolchain_signatures(golden)
    ok("Z8 no writing-library signature in any shipped file", not sig, str(sig))
    ok("Z10 personas from the draw", "Joanne MacDonald" in pdf_text(os.path.join(golden, "pcqs_2026q3_contractor_letter.pdf"))
       and "L. Morrison" in xlsx_text(os.path.join(target, "tallis_quarterly_return_2026q3.xlsx")))

    # distractors -------------------------------------------------------------------------------
    for d in dis:
        alt = without(target, os.path.basename(d))
        r2 = analysis.run(alt)
        same = (r2["outcomes"] == res["outcomes"] and r2["timeliness"] == tim and r2["missed"] == missed
                and r2["acceptance"] == acc and abs(r2["credit"] - res["credit"]) < 1e-9)
        shutil.rmtree(alt)
        ok("D1 deleting %s moves nothing" % os.path.basename(d), same)

    # figures.json --------------------------------------------------------------------------------
    fig = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    ok("F1 figures.json carries the call", fig["call"]["credit_dollars"] == "{:,}".format(int(round(res["credit"]))))
    ok("F1 figures.json carries every region's answers",
       all(fig["deliverables"][r]["timeliness"] == "%.1f" % tim[r] and fig["deliverables"][r]["missed_visits"] == missed[r]
           and fig["deliverables"][r]["replacement_acceptance"] == "%.1f" % acc[r] for r in R))

    fails = [r for r in RESULTS if not r[1]]
    for name, passed, detail in RESULTS:
        print("%s  %s  %s" % ("PASS" if passed else "FAIL", name, detail))
    print("%d assertions, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


# helpers ---------------------------------------------------------------------------------------
def mess_variants(target):
    """the golden method with each Layer 1 item mishandled"""
    out = {}
    p = analysis.Pack(target)
    # re-sent uploads kept: every row of the price database counts in the frequency
    rows = list(csv.DictReader(open(os.path.join(target, "cpi_field_quotes_2025-10_2026-09.csv"))))
    seq = defaultdict(list)
    for r in rows:
        seq[r["quote_id"]].append(r)
    pos = {m: i for i, m in enumerate(p.months)}
    cmp_, chg = defaultdict(int), defaultdict(int)
    for q, lst in seq.items():
        lst.sort(key=lambda r: r["ref_month"])
        for a, b in zip(lst, lst[1:]):
            if pos[b["ref_month"]] - pos[a["ref_month"]] > 1 or a["status"] not in ("P", "R", "10", "30") or b["status"] not in ("P", "10"):
                continue
            k = (p.item_class[b["item_code"]], p.stratum(b["outlet_code"]))
            cmp_[k] += 1
            chg[k] += abs(float(a["price"]) - float(b["price"])) > 0.004
    out["re-sent uploads kept"] = p.netted(f={k: chg[k] / cmp_[k] for k in cmp_})
    # status 30 read as a same-variety price
    q2 = analysis.Pack(target)
    for k, r in q2.quotes.items():
        if r["status"] == "30":
            r["status"] = "10"
    out["status 30 read as same variety"] = q2.netted()
    # visit dates taken in UTC
    q3 = analysis.Pack(target)
    q3.visit_days = defaultdict(list)
    for v in q3.visits:
        if int(v["prices_entered"]) == 0:
            continue
        t = dt.datetime.fromisoformat(v["started"])
        q3.visit_days[(v["outlet_no"], v["started"][:7])].append((t - t.utcoffset()).date())
    out["visit dates read in UTC"] = q3.netted()
    out["index day taken as the visit date"] = p.netted(basis="index")
    return out


def workday_variant(p):
    f = p.change_frequency()
    out = {}
    for r in p.regions:
        v = [b for b in p.counted() if b["region"] == r]
        a = sum(abs(b["rec"] - b["fqt"]) < 0.005 for b in v)
        out[r] = 100.0 * a / sum((1 - f[p.fkey(b, "class")]) ** (p.lag(b, workdays=True) / 21.7) for b in v)
    return out


def error_netted(p):
    f = p.change_frequency()
    e = 0.01
    for _ in range(6):
        fc = {k: max(0.0, (x - 2 * e) / (1 - 2 * e)) for k, x in f.items()}
        acc = p.netted(f=fc)
        n = sum(len([b for b in p.counted() if b["region"] == r]) for r in p.regions)
        e = 1 - sum(acc[r] * len([b for b in p.counted() if b["region"] == r]) for r in p.regions) / n / 100
    return acc


def netted_without_replacements(p):
    keep = {(m, q) for (m, q), r in p.quotes.items() if r["status"] not in ("R", "30")}
    saved = p.backchecks
    p.backchecks = [b for b in saved if (b["month"], b["quote"]) in keep]
    out = p.netted()
    p.backchecks = saved
    return out


def clean_routes(w):
    """the default, the golden step alone and the fruit-and-vegetable rung, on the world before export"""
    recs = defaultdict(dict)
    for r in w.records:
        recs[r["qid"]][(r["y"], r["m"])] = r
    cmp_, chg = defaultdict(int), defaultdict(int)
    for qid, d in recs.items():
        q = w.quotes[qid]
        for a, b in zip(P.MONTHS[:-1], P.MONTHS[1:]):
            ra, rb = d.get(a), d.get(b)
            if ra is None or rb is None or ra["price"] is None or rb["price"] is None or rb["status"] != "P":
                continue
            k = (q["group"], q["stratum"])
            cmp_[k] += 1
            chg[k] += abs(ra["price"] - rb["price"]) > 0.004
    f = {k: chg[k] / cmp_[k] for k in cmp_}

    def band(a):
        return "C" if a >= P.BAND_COMPLIANT else ("A" if a >= P.BAND_CREDIT else "S")
    d, g, n = "", "", ""
    for r in w.regions:
        v = [b for b in w.backchecks if b["region"] == r["code"] and b["fqt_price"] is not None]
        a = sum(abs(b["rec_price"] - b["fqt_price"]) < 0.005 for b in v)
        s = sum((1 - f[(w.quotes[b["qid"]]["group"], w.quotes[b["qid"]]["stratum"])]) ** ((b["fqt"] - b["vday"]).days / 30.4) for b in v)
        v2 = [b for b in v if w.quotes[b["qid"]]["group"] != "FV"]
        a2 = sum(abs(b["rec_price"] - b["fqt_price"]) < 0.005 for b in v2)
        d += band(100.0 * a / len(v))
        g += band(100.0 * a / s)
        n += band(100.0 * a2 / len(v2))
    return d, g, n


def population_truth(w):
    out = ""
    for r in w.regions:
        pop = [x for x in w.records if w.quotes[x["qid"]]["region"] == r["code"] and (x["y"], x["m"]) in P.QUARTER and x["price"] is not None]
        a = 100.0 * sum(x["err"] is None for x in pop) / len(pop)
        out += "C" if a >= P.BAND_COMPLIANT else ("A" if a >= P.BAND_CREDIT else "S")
    return out


def truth_timeliness(w, p):
    from world import window
    done, tot, miss = defaultdict(int), defaultdict(int), defaultdict(int)
    bom = by_outlet_month(w)
    for (y, m) in P.QUARTER:
        win = window(y, m)
        for o in w.base_outlets:
            v = w.vis_index[(o["oid"], y, m)]
            days = [d for d in v["days"] if any(rr["vday"] == d for rr in bom.get((o["oid"], y, m), []))]
            tot[o["region"]] += 1
            if not days:
                miss[o["region"]] += 1
            elif all(win[0] <= d <= win[-1] for d in days):
                done[o["region"]] += 1
    return ({r["code"]: round(100.0 * done[r["code"]] / tot[r["code"]], 6) for r in w.regions},
            {r["code"]: miss[r["code"]] for r in w.regions})


_BOM = {}


def by_outlet_month(w):
    if "x" not in _BOM:
        d = defaultdict(list)
        for r in w.records:
            d[(w.quotes[r["qid"]]["oid"], r["y"], r["m"])].append(r)
        _BOM["x"] = d
    return _BOM["x"]


def truth_acceptance(w):
    latest = {}
    for rv in sorted(w.reviews, key=lambda x: x["date"]):
        if rv["decision"] != "Query to contractor":
            latest[(rv["qid"], rv["y"], rv["m"])] = rv["decision"]
    tot, acc = defaultdict(int), defaultdict(int)
    for r in w.records:
        if r["status"] == "R" and (r["y"], r["m"]) in P.QUARTER:
            reg = w.quotes[r["qid"]]["region"]
            tot[reg] += 1
            acc[reg] += latest.get((r["qid"], r["y"], r["m"])) == "Comparable"
    return {reg: round(100.0 * acc[reg] / tot[reg], 6) for reg in tot}


def is_interval(members, stat):
    order = sorted(stat, key=stat.get)
    idx = sorted(order.index(m) for m in members)
    return idx == list(range(idx[0], idx[0] + len(idx)))


def resent_rows_differ(target):
    seen = {}
    for r in csv.DictReader(open(os.path.join(target, "cpi_field_quotes_2025-10_2026-09.csv"))):
        k = (r["ref_month"], r["quote_id"])
        if k in seen:
            a = seen[k]
            if a["load_batch"] == r["load_batch"] or any(a[c] != r[c] for c in ("outlet_code", "item_code", "variety", "price", "status")):
                return False
        seen[k] = r
    return True


def dates_in_range(p):
    if max(p.months) > "2026-09":
        return False
    if max(b["when"] for b in p.backchecks) > dt.date(2026, 9, 30):
        return False
    if max(v["started"][:10] for v in p.visits) > "2026-09-30":
        return False
    if max(analysis.d_parse(r["Decided on"]) for r in p.reviews) > P.EXTRACT_DATE:
        return False
    return True


def toolchain_signatures(folder):
    out = []
    for f in sorted(os.listdir(folder)):
        path = os.path.join(folder, f)
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(path) as z:
                blob = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
        elif f.endswith(".pdf"):
            blob = open(path, "rb").read()
        else:
            continue
        for s in (b"openpyxl", b"reportlab", b"ReportLab", b"matplotlib", b"Matplotlib", b"python"):
            if s in blob:
                out.append("%s:%s" % (f, s.decode()))
    return out


def xlsx_text(path):
    from openpyxl import load_workbook
    wb = load_workbook(path)
    return " ".join(str(c) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for c in row if c is not None)


def without(target, name):
    alt = tempfile.mkdtemp(prefix="t233_")
    for f in os.listdir(target):
        if f != name:
            shutil.copy(os.path.join(target, f), alt)
    return alt


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
