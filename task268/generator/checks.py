"""The generator's assertions on the cut pack and the clean truth: the three rules (R1 to R3c), every semantic fork
(SF1 to SF16), the passing family (FAMILY), the separation of the asks from the call (SEP), the Layer 1 neutrality,
the input gates, the realism sweep and the documents read back with positive controls."""
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402
import world as W      # noqa: E402

ROWS = []


def ok(name, cond, detail=""):
    ROWS.append((name, bool(cond), detail))


def r1(x):
    return "%.1f" % (x + 1e-12)


def pair(fr):
    o = sorted(K.REG, key=lambda r: -fr[r])
    return o[:2]


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in PdfReader(path).pages))


def truth_dev(w, how, ay, years):
    """the developments on the generator's clean truth (no file read): R3a and R3b"""
    pc = [c for c in w.all_claims if c["product"] == "PC"]
    def key(c):
        nb = {"PH": "P", "TPD": "T", "INS": "I", "SOL": "R", "CMC": "R"}[c["route"]]
        return {"pooled": 0, "head": c["head"], "notified_by": nb, "route": c["route"]}[how]
    def pos(a):
        return [c for c in pc if c["ay"] == a and c["notified"] <= dt.date(a + 1, 9, 30)]
    num, den = Counter(), Counter()
    for a in years:
        num.update(key(c) for c in pc if c["ay"] == a)
        den.update(key(c) for c in pos(a))
    f = {k: num[k] / den[k] for k in num if den[k]}
    est = Counter()
    for c in pos(ay):
        est[c["region"]] += f.get(key(c), 1.0)
    return est


def run(task):
    ROWS.clear()
    tgt = os.path.join(task, "target")
    G = A.Golden(tgt)
    R = G.run()
    F = json.load(open(os.path.join(HERE, "figures.json")))
    gold = R["freq"]["route"]
    GOLD_PAIR = ["Mersey", "Pennine"]

    # ---------------------------------------------------------------- the call
    ok("CALL pair", R["call"] == GOLD_PAIR, R["call"])
    ok("CALL third", R["third"] == "Severn", R["third"])
    ok("CALL printed", [r1(gold[r]) for r in K.REG] == ["8.9", "8.2", "7.3", "5.9", "8.0"], [r1(gold[r]) for r in K.REG])
    ok("CALL gap", r1(R["gap"]) == "0.2" and r1(gold["Pennine"] - gold["Severn"]) == "0.2", "%.3f" % R["gap"])
    edges = {r: 0.05 - abs(gold[r] - round(gold[r], 1)) for r in K.REG}
    ok("CALL mid-bin", min(edges.values()) >= 0.03, {r: round(v, 3) for r, v in edges.items()})
    ok("CALL figures.json", F["frequency"] == {r: float(r1(gold[r])) for r in K.REG} and F["call"] == GOLD_PAIR)

    # ---------------------------------------------------------------- R1: the field's raw material ships
    c = G.B.claims
    ok("R1 claim rows", len(c) > 100000 and c.claim_ref.is_unique, len(c))
    ok("R1 dates at row level", c.accident_date.str.match(r"^\d{4}-\d{2}-\d{2}$").all() and
       (c.notified_at.str.len() >= 10).all())
    header = open(os.path.join(tgt, K.FILES["claims"]), encoding="utf-8").readline().strip().split(",")
    banned_cols = [x for x in header if re.search(r"freq|factor|ultimate|ibnr|lag|route|channel|firm", x, re.I)]
    ok("R1 no deciding column", not banned_cols, banned_cols)
    ok("R1 firm type off the extract", "firm_type" not in header and set(G.B.reps.firm_type) ==
       {"Solicitor practice", "Claims management company"})

    # ---------------------------------------------------------------- R3: the analyst test on the clean truth
    w = W.World(K.SEED)
    cy = {r: R["cy"][r] for r in K.REG}
    tr = {h: {r: 100 * v / cy[r] for r, v in truth_dev(w, h, 2025, K.CLOSED).items()} for h in
          ("pooled", "head", "notified_by", "route")}
    for h in ("pooled", "head", "notified_by"):
        ok("R3a default %s on the truth" % h, pair(tr[h]) == ["Mersey", "Severn"], {r: round(v, 2) for r, v in tr[h].items()})
    ok("R3b the decisive step alone", pair(tr["route"]) == GOLD_PAIR, {r: round(v, 2) for r, v in tr["route"].items()})
    ult = Counter(c_["region"] for c_ in w.all_claims if c_["product"] == "PC" and c_["ay"] == 2025)
    ok("R3b the truth agrees", pair({r: ult[r] / cy[r] for r in K.REG}) == GOLD_PAIR)
    th = open(os.path.join(tgt, K.FILES["thread"]), encoding="utf-8").read()
    ok("R3c no plant", not re.search(r"\d+(\.\d+)? (claims )?per 100|frequenc\w* (of|at|is|was) \d", th, re.I) and
       not any(x in th for x in ("Pennine", "Severn", "Mersey", "Wessex", "Fenland")), "the thread states no frequency or region")

    # ---------------------------------------------------------------- SF rows
    ok("SF1 notified only names the default pair", pair(R["raw"]) == ["Mersey", "Severn"])
    ok("SF2 the 2.1 count leaves the call's population as it is", len(G.main_counted) == len(G.main))
    m = G.main
    nonil = {r: 0.0 for r in K.REG}
    sub = m[(m.ay == 2025) & (m.status != "Closed nil")]
    f_r = R["factors_route"]
    for reg, rt in zip(sub[sub.note <= dt.date(2026, 9, 30)].region, sub[sub.note <= dt.date(2026, 9, 30)].route):
        nonil[reg] += f_r[rt]
    ok("SF3 nil claims dropped keep the pair", pair({r: nonil[r] / cy[r] for r in K.REG}) == GOLD_PAIR)
    ok("SF4 every district on the 2025 drawing", c.region.notna().all())
    allp = c[c.ay == 2025]
    ok("SF5 vans in keep the pair", pair({r: int((allp.region == r).sum()) for r in K.REG}) == ["Mersey", "Severn"] and True)
    # SF6: the UTC calendar date of each timestamp read as the notification date
    c2 = c.copy()
    c2["note"] = [dt.date.fromisoformat(s[:10]) for s in c2.notified_at]
    moved = int((c2.note != c.note).sum())
    G2 = A.Golden.__new__(A.Golden)
    G2.B = G.B
    pc2 = c2[c2["product"] == "PC"]
    G2.main = pc2[pc2.ay.isin(list(K.CLOSED) + [K.OPEN_YEAR])].copy()
    G2.main_counted = A.count_rule(G2.main)
    G2.pc = pc2
    f6, _ = G2.frequency("route")
    ok("SF6 the UTC date gives the same figures", [r1(f6[r]) for r in K.REG] == [r1(gold[r]) for r in K.REG],
       "%d timestamps change date" % moved)
    # SF7: completion by each claim's own age in days, route by route (the accident-date grain)
    lagf = {}
    for rt in set(G.main_counted.route):
        lags = []
        for ay in K.CLOSED:
            fn = G.final(ay)
            fn = fn[fn.route == rt]
            lags += [(n - a).days for n, a in zip(fn.note, fn.acc)]
        lagf[rt] = sorted(lags)
    import bisect
    p25 = G.position(2025)
    e7 = Counter()
    for reg, rt, a in zip(p25.region, p25.route, p25.acc):
        age = (dt.date(2026, 9, 30) - a).days
        L = lagf[rt]
        e7[reg] += len(L) / max(bisect.bisect_right(L, age), 1)
    ok("SF7 completion by age in days keeps the pair", pair({r: e7[r] / cy[r] for r in K.REG}) == GOLD_PAIR,
       {r: round(100 * e7[r] / cy[r], 3) for r in K.REG})
    f8, _ = G.frequency("route", years=(2020, 2021, 2022))
    ok("SF8 closed years 2020 to 2022", [r1(f8[r]) for r in K.REG] == [r1(gold[r]) for r in K.REG])
    ok("SF9 simple-average factors", [r1(R["freq"]["route_simple"][r]) for r in K.REG] == [r1(gold[r]) for r in K.REG])
    for h in ("pooled", "head", "notified_by", "representative", "region"):
        worst = max(abs(v[2]) for v in R["bt"][h].values())
        ok("SF10 %s fails the back-test and names the default pair" % h,
           worst > 2 * K.TOLERANCE and pair(R["freq"][h]) == ["Mersey", "Severn"], "%.2f" % worst)
    ok("SF11 the family passes", set(R["passing"]) == {"route", "route_head", "cmc_rest", "route_simple"}, R["passing"])
    # SF12: a car count at 30 September 2026 for the denominator
    cars = R["ask_a"]
    ok("SF12 a car count keeps the pair", pair({r: R["est"]["route"][r] / sum(cars[(r, cv)] for cv in ("COMP", "TPFT", "TPO"))
                                               for r in K.REG}) == GOLD_PAIR)
    ok("SF13 the gap rounded either way", r1(R["gap"]) == "%.1f" % (float(r1(gold["Pennine"])) - float(r1(gold["Severn"]))))
    ok("SF14 no tie", R["gap"] >= 0.1, "%.3f" % R["gap"])
    # SF15: the in-force row carries the district and cover at the term's start
    inf, ch = G.B.inforce, G.B.changes
    dmap = dict(zip(inf.policy_ref, inf.risk_postcode_district))
    smap = dict(zip(inf.policy_ref, inf.term_start))
    adr = ch[(ch.change_type == "ADDRESS")]
    first_new = {}
    for p_, eff, nd in sorted(zip(adr.policy_ref, adr.effective_from, adr.new_postcode_district)):
        first_new.setdefault(p_, nd)
    stale = sum(1 for p_ in first_new if p_ in dmap and dmap[p_] != first_new[p_])
    ok("SF15 the in-force district is the term's start", stale == len([p for p in first_new if p in dmap]), stale)
    naive_a = G.ask_a(apply_changes=False)
    ok("SF15 every ask cell moves", all(abs(naive_a[k] - cars[k]) >= 10 for k in cars),
       {"%s %s" % k: naive_a[k] - cars[k] for k in cars})
    # SF16: the cover on the in-force row is the cover at the term's start; a later cover change sets the cover that day
    cvc = ch[(ch.change_type == "COVER")]
    cmap = dict(zip(inf.policy_ref, inf.cover))
    first_cov = {}
    for p_, eff, nc in sorted(zip(cvc.policy_ref, cvc.effective_from, cvc.new_cover)):
        first_cov.setdefault(p_, nc)
    held = [p_ for p_ in first_cov if p_ in cmap]
    ok("SF16 the in-force cover is the term's start", all(cmap[p_] != first_cov[p_] for p_ in held) and len(held) > 100, len(held))
    mir = G.ask_a(apply_changes=True, effective_only=False)
    ok("SF16 changes dated after 30 September move the ask", sum(abs(mir[k] - cars[k]) for k in cars) >= 15,
       sum(abs(mir[k] - cars[k]) for k in cars))

    # ---------------------------------------------------------------- FAMILY
    fam = [R["freq"][h] for h in ("route", "route_head", "cmc_rest", "route_simple")] + [f8]
    ok("FAMILY same printed figures", all([r1(x[r]) for r in K.REG] == [r1(gold[r]) for r in K.REG] for x in fam))
    ok("FAMILY within 1.2 per cent", all(max(abs(v[2]) for v in R["bt"][h].values()) <= 1.2
                                         for h in ("route", "route_head", "cmc_rest", "route_simple")))

    # ---------------------------------------------------------------- SEP: the asks off the call's population
    twins = c[(c.status == "Closed nil")]
    tw_main = 0
    pcm = c[(c["product"] == "PC") & (c.ay <= 2025)]
    key = ["policy_ref", "vrm", "accident_date", "head_of_claim"]
    dupe = pcm.duplicated(key, keep=False) & (pcm.claimant_no == "")
    ok("SEP no twin in the call's years", int(dupe.sum()) == 0 and tw_main == 0, int(dupe.sum()))
    ok("SEP no blank pair in the call's years", int((pcm[pcm.claimant_no == ""].duplicated(key)).sum()) == 0)
    src = open(os.path.join(HERE, "analysis.py")).read()
    call_part = src[src.index("class Golden"):src.index("# ------------------------------------------------------------------ the ask")]
    ok("SEP the call reads no policy file", "inforce" not in call_part and "changes" not in call_part)

    # ---------------------------------------------------------------- Layer 1 neutrality (R2)
    legacy = c[c.notified_at.str.len() == 10]
    ok("R2 LAYER1 migration: legacy dates before the go-live, timestamps after",
       (legacy.note < K.MIGRATION).all() and (c[c.notified_at.str.len() > 10].note >= K.MIGRATION - dt.timedelta(days=1)).all()
       and (legacy.legacy_claim_ref != "").all())
    ok("R2 LAYER1 migration neutral (the UTC date read)", True if [r1(f6[r]) for r in K.REG] == [r1(gold[r]) for r in K.REG] else False)
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(tgt, K.FILES["exposure"]), read_only=True)
    old_hdr = next(wb["2021"].iter_rows(values_only=True))
    new_hdr = next(wb["2025"].iter_rows(values_only=True))
    ok("R2 LAYER1 mart layout change, the call reads 2025 only", old_hdr[0] == "period" and new_hdr[0] == "month")
    ok("R2 LAYER1 open years present and unread", set(c.ay) == set(K.ACCIDENT_YEARS) and
       set(G.main.ay) == set(K.CLOSED) | {K.OPEN_YEAR})

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(tgt))
    exts = Counter(f.rsplit(".", 1)[1] for f in files)
    ok("GATE files", len(files) >= 10, len(files))
    ok("GATE formats", len(exts) >= 3, dict(exts))
    ok("GATE a 25,000-row file", len(c) >= 25000)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    ok("GATE distractors", len(meta["distractor_files"]) >= 2 and not any("distract" in f for f in files))
    ok("GATE no file describes the data", not any(re.search(r"readme|dictionary|manifest|notes|contents", f, re.I) for f in files))
    # each distractor deleted: the golden is the same
    tmp = tempfile.mkdtemp(dir=task)
    try:
        for f in files:
            if "target/" + f not in meta["distractor_files"]:
                shutil.copy(os.path.join(tgt, f), tmp)
        R2 = A.Golden(tmp).run()
        ok("GATE distractors deleted, the golden holds", R2["call"] == R["call"] and R2["ask_a"] == R["ask_a"] and
           all(r1(R2["freq"]["route"][r]) == r1(gold[r]) for r in K.REG))
    finally:
        shutil.rmtree(tmp)

    # ---------------------------------------------------------------- the documents, read back (positive controls first)
    terms, std = pdf_text(os.path.join(tgt, K.FILES["terms"])), pdf_text(os.path.join(tgt, K.FILES["standard"]))
    quote = pdf_text(os.path.join(tgt, K.FILES["quote"]))
    ok("DOC terms readable", "whether or not they had been notified to Corriven by the end of 30 September 2026" in terms)
    ok("DOC standard 3.3 readable", "reproduces that year's final count in every sales region to within two per cent" in std)
    ok("DOC standard 2.1 readable", "one claimant's claim under one head of claim" in std and "arising from one accident" in std)
    ok("DOC standard 3.2 readable", "apply the whole book's factors to each region's notified claims" in std)
    ok("DOC quote readable", "Q-26-1184" in quote)
    from pypdf import PdfReader
    import io
    import logging
    import subprocess
    logging.getLogger("pypdf").setLevel(logging.WARNING)
    log = io.StringIO()
    h = logging.StreamHandler(log)
    logging.getLogger("pypdf").addHandler(h)
    for k in ("terms", "standard", "quote"):
        pth = os.path.join(tgt, K.FILES[k])
        strict = re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in PdfReader(pth, strict=True).pages))
        ok("H25 %s strict reader" % k, strict == pdf_text(pth) and len(strict) > 500)
        if shutil.which("pdftotext"):
            out = subprocess.run(["pdftotext", "-layout", pth, "-"], capture_output=True, text=True)
            pt = re.sub(r"\s+", " ", out.stdout)
            key = {"terms": "whether or not they had been notified to Corriven", "standard": "to within two per cent",
                   "quote": "Q-26-1184"}[k]
            ok("H25 %s pdftotext" % k, out.returncode == 0 and not out.stderr.strip() and key in pt, out.stderr[:80])
    logging.getLogger("pypdf").removeHandler(h)
    ok("H25 no parser warnings", not log.getvalue().strip(), log.getvalue()[:120])
    thread = open(os.path.join(tgt, K.FILES["thread"]), encoding="utf-8").read()
    docs = terms + " " + std + " " + thread
    leak = [x for x in ("claims management", "claims-management", "firm type", "representative", "solicitor",
                        "notifying route", "notified late", "late notification", "Pennine", "Severn")
            if x.lower() in docs.lower()]
    ok("LEAK no document names the decisive split or a region's standing", not leak, leak)
    ok("LEAK the terms carry no pin on the grouping", "group" not in terms.lower() and "segment" not in std.lower())

    # ---------------------------------------------------------------- realism sweep
    def steps(col):
        nums = sorted(int(re.sub(r"\D", "", x)) for x in col if x)
        d = {b - a for a, b in zip(nums, nums[1:])}
        return len(d)
    ok("REAL claim refs not a constant step", steps(c.claim_ref) > 1)
    ok("REAL legacy refs not a constant step", steps(c.legacy_claim_ref) > 1)
    ok("REAL change refs not a constant step", steps(ch.change_ref) > 1)
    ok("REAL representative refs not a constant step", steps(G.B.reps.representative_ref) > 1)
    shapes = Counter(n.split()[-1] for n in G.B.reps.firm_name)
    ok("REAL firm names take several shapes", len(shapes) > 4, dict(shapes))
    ok("REAL earned car-years not round", all(abs(v - round(v, -1)) > 0.5 for v in R["cy"].values()), R["cy"])
    ok("REAL notified counts distinct", len(set(R["notified"].values())) == 5)
    ok("REAL no date after the pull", (c.note <= K.EXTRACT).all() and (c[c.closed_on != ""].closed_on <= K.EXTRACT.isoformat()).all()
       and (ch.processed_on <= K.EXTRACT.isoformat()).all())
    ok("REAL no claim before its accident", (c.note >= c.acc).all())
    ok("REAL personas drawn", all(p in thread for p in K.PEOPLE.values()))
    ok("REAL region codes not alphabetical", [r[0] for r in K.REGIONS] != sorted(r[0] for r in K.REGIONS))
    return ROWS


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    rows = run(task)
    for n, good, d in rows:
        print("%s  %-60s %s" % ("PASS" if good else "FAIL", n, str(d)[:120] if (not good or d) else ""))
    print("%d assertions, %d failed" % (len(rows), sum(1 for r in rows if not r[1])))
    sys.exit(1 if any(not r[1] for r in rows) else 0)
