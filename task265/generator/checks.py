"""The build's assertions for task265: the input gates, the three-rules block (R1 to R3c), the ladder, every semantic
fork row (SF1 to SF15), the conventions, the asks' devices and stops, the separation line, the distractors, the
realism sweep and the agreement of the goldens with figures.json."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import tempfile
from collections import Counter

from openpyxl import load_workbook
from pypdf import PdfReader

import analysis as A
import common as K
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
N = [0]


def ok(cond, label):
    N[0] += 1
    assert cond, "FAILED: " + label


def pdf_text(path):
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def copy_without(target, drop):
    d = tempfile.mkdtemp()
    for f in os.listdir(target):
        if f not in drop:
            shutil.copy(os.path.join(target, f), d)
    return d


def run(target, T):
    P = lambda k: os.path.join(target, K.FILES[k])
    F = json.load(open(os.path.join(HERE, "figures.json")))
    fig, hips = A.call(target)
    gold = {c: fig[c]["golden"] for c in K.CODES}

    # ------------------------------------------------------------------ input gates
    files = os.listdir(target)
    ok(len(files) >= 10, "10 or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "a file of 25,000 rows or more (%d)" % big)
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2 and all(os.path.exists(os.path.join(os.path.dirname(target), f))
                                                  for f in meta["distractor_files"]), "two distractors shipped")
    ok(sorted(files) == sorted(K.FILES.values()), "the pack is exactly the manifest's files and the manifest")
    listed = [r["file"] for r in csv.DictReader(open(os.path.join(target, K.FILES["manifest"]), encoding="utf-8"))]
    ok(sorted(listed) == sorted(f for f in files if f != K.FILES["manifest"]), "H9: the manifest lists every other file")
    asof = dt.date(2027, 1, 27)
    late = []
    for f in files:
        if f.endswith(".csv"):
            for line in open(os.path.join(target, f), encoding="utf-8"):
                for m in re.findall(r"\b(20\d\d-\d\d-\d\d)\b", line):
                    if dt.date.fromisoformat(m) > asof:
                        late.append((f, m))
    ok(not late, "H16: no date past the pack's export date (%s)" % late[:3])

    # ------------------------------------------------------------------ the call and the ladder
    stays = A.keeps(fig, "golden")
    ok(stays == ["MF", "VS", "MS"], "golden keeps Askvane/Quarvel, Holbrin/Pellvoro, Askvane/Pellvoro (%s)" % stays)
    for c in K.CODES:
        ok(abs(gold[c] - K.BAR) >= 0.4, "%s golden %.3f at least 0.4 from the bar" % (c, gold[c]))
        ok(abs(gold[c] * 10 - round(gold[c] * 10)) <= 0.35, "%s golden %.3f mid-bin at one decimal" % (c, gold[c]))
        ok(fig[c]["prosp_max_years"] < 10, "%s: prospective hips alone reach no ten-year estimate" % c)
        ok(fig[c]["op"] < fig[c]["reg"] < fig[c]["golden"], "%s: each correction raises the figure" % c)
    ok(A.keeps(fig, "crude") == K.CODES, "R0 crude keeps all six")
    ok(A.keeps(fig, "op") == ["TA", "TS", "MF", "VS", "MS"], "R1 (default path) keeps five, both Edvalt constructs")
    reg = A.keeps(fig, "reg")
    ok(len(reg) == 4 and "TS" in reg and "TA" not in reg, "R2 keeps four: Edvalt/Pellvoro stays, Edvalt/Kelvarne goes")
    for c in K.CODES:
        for r in ("op", "reg", "crude"):
            ok(abs(fig[c][r] - K.BAR) >= 0.3, "%s %s %.3f clear of the bar" % (c, r, fig[c][r]))
    ok(fig["TA"]["golden"] - fig["TA"]["op"] >= 2.0 and fig["TS"]["golden"] - fig["TS"]["op"] >= 2.0,
       "the decisive move carries both Edvalt constructs at least 2 points")
    sets = {r: tuple(A.keeps(fig, r)) for r in ("crude", "op", "reg", "golden")}
    ok(len(set(sets.values())) == 4, "every rung names a different set")

    # ------------------------------------------------------------------ the three rules, executed on the clean truth
    R = W.rungs(T)
    clean = lambda r: [c for c in K.CODES if R[c][r] <= K.BAR]
    ok(clean("op") == ["TA", "TS", "MF", "VS", "MS"], "R3a: the easy route on the clean truth keeps five")
    ok(clean("golden") == ["MF", "VS", "MS"], "R3b: the decisive step alone on the clean truth keeps three")
    ok(clean("reg") != clean("golden") and clean("crude") != clean("golden"), "R3b: each lower rung stays wrong")
    heads = set()
    for f in files:
        if f.endswith(".csv"):
            heads |= set(next(csv.reader(open(os.path.join(target, f), encoding="utf-8"))))
    ok(not any(re.search(r"cumulative|survival|revision_rate|at_risk|percent", h, re.I) for h in heads),
       "R1: no shipped column holds the deciding quantity")
    ok(sum(1 for h in hips.values() if h["construct"] in K.CNAME.values()) == sum(fig[c]["n"] for c in K.CODES),
       "R1: the golden reads hip-level rows of both exports")
    # R2: each mess item, mishandled, leaves the call (or fails loudly)
    for dd in (1, "last"):
        g2, _ = A.call(target, death_day=dd)
        ok(all(round(g2[c]["golden"], 1) == round(gold[c], 1) for c in K.CODES), "R2/SF11: month-only deaths on day %s" % dd)
    try:
        import pandas as pd
        pd.to_datetime(pd.read_excel(P("legacy"))["Date of operation"], dayfirst=True, format="%d/%m/%Y")
        loud = False
    except Exception:
        loud = True
    ok(loud, "R2: the legacy dates read day first fail loudly")
    xw = A.crosswalk(lambda f: os.path.join(target, f))[0]
    old = [k for k in xw if k.startswith("71-")]
    ok(len(old) > 0, "R2: Thorvik's old numbers are in the crosswalk")
    kes_legacy = sum(1 for h in hips.values() if h["legacy"] and h["construct"] in ("Askvane/Quarvel", "Askvane/Pellvoro"))
    ok(kes_legacy > 0, "R2: dropping Thorvik's old numbers removes every legacy Askvane hip (no ten-year estimate), loud")
    # bilateral patients read as one hip each patient: same call
    first = {}
    for k, h in sorted(hips.items(), key=lambda kv: (kv[1]["op"], kv[0])):
        first.setdefault(h["pat"], k)
    sub = {k: h for k, h in hips.items() if first[h["pat"]] == k}
    pl = [c for c in K.CODES if A.km(A.rows_for(sub, K.CNAME[c], "golden")) <= K.BAR]
    ok(pl == stays, "R2/SF6: one hip per patient gives the same call")
    # R3c: no repeated block, no identical counts across sites
    a, nat = A.asks(target), A.asks(target, honour_side=False, merges=False)
    for k in ("C_hosp",):
        ok(len(set(a[k].values())) == 3 and len(set(nat[k].values())) == 3, "R3c: no identical counts across hospitals")
    tots = [sum(a["A"][c][h] for c in K.CODES) for h in K.HOSP]
    ok(len(set(tots)) == 3 and all(t % 100 for t in tots), "R3c: hospital totals differ and are not round")
    rows = [r for r in csv.reader(open(P("implants"), encoding="utf-8"))][1:]
    blocks = Counter(tuple(tuple(r[5:12]) for r in rows[i:i + 6]) for i in range(0, len(rows) - 6, 6))
    ok(max(blocks.values()) == 1, "R3c: no repeated block of six implant lines")

    # ------------------------------------------------------------------ the semantic fork table
    pol = pdf_text(P("policy"))
    dic = pdf_text(P("dictionary"))
    ok("one femoral stem family used with one acetabular cup family" in pol, "SF1 construct filed")
    ok("adds, removes or replaces a component" in pol and "only the first revision" in pol, "SF2 revision filed")
    revs = [r for r in csv.DictReader(open(P("revisions"), encoding="utf-8"))]
    ok(len({r["registry_hip_id"] for r in revs if r["revision_number"] == "1"}) ==
       sum(1 for r in revs if r["revision_number"] == "1"), "SF2 one first revision per hip")
    ok("ten years after the operation" in pol, "SF3 time since the operation filed")
    ok("Deaths and loss to follow-up are censored" in pol and "Kaplan-Meier" in pol, "SF4 deaths censored, KM filed")
    g5 = dict(gold)
    for h in hips.values():
        pass
    moved_ignored = {}
    for c in K.CODES:
        rr = []
        for k, h in hips.items():
            if h["construct"] != K.CNAME[c]:
                continue
            rr.append(((h["entry"] - h["op"]).days, (h["stop"] - h["op"]).days, h["event"]))
        moved_ignored[c] = A.km(rr)
    ok([c for c in K.CODES if moved_ignored[c] <= K.BAR] == stays, "SF5 same call")
    ok("the registry loses follow-up of a hip when its patient moves out of the state" in dic,
       "SF5 the move ends follow-up, filed in the dictionary")
    ok("the unit being the hip" in pol, "SF6 the hip filed")
    ok("every primary total hip operation with the construct at a system hospital on the registry" in pol,
       "SF7 population filed")
    ok(max(h["stop"] for h in hips.values()) <= K.EXTRACT, "SF8 nothing after the extract")
    ok(all(abs(gold[c] - K.BAR) >= 0.4 for c in K.CODES), "SF9 no construct within 0.4 of the bar")
    near = [h for h in hips.values() if h["event"] and h["construct"] in K.CNAME.values()
            and 3651 <= (h["stop"] - h["op"]).days <= 3653]
    ok(not near, "SF10 no revision on day 3,651, 3,652 or 3,653")
    for hz in (3650, 3653):
        g2, _ = A.call(target, horizon=hz)
        ok(all(round(g2[c]["golden"], 1) == round(gold[c], 1) for c in K.CODES), "SF10 horizon %d" % hz)
    mo = {r["registry_patient_id"]: r["date_of_death"] for r in csv.DictReader(open(P("deaths"), encoding="utf-8"))
          if len(r["date_of_death"]) == 7}
    clash = [h for h in hips.values() if h["pat"] in mo and h["rev"] and h["rev"].strftime("%Y-%m") >= mo[h["pat"]]]
    ok(not clash, "SF11 no revision in or after the month of a month-only death")
    ok(all(h["construct"] is not None for h in hips.values()), "SF12/SF15 every registry hip maps to a construct")
    g2, _ = A.call(target, inclusive=True)
    ok(all(round(g2[c]["golden"], 1) == round(gold[c], 1) for c in K.CODES), "SF13 entry inclusive")
    ok("entered when the patient first attended a registry clinic" in dic, "SF14 legacy entry filed in the dictionary")
    ok(reg != stays, "SF14 the registry-start reading files another call (R2)")
    ok("quarterly linkage with the state's hospital discharge data" in dic and "Revisions of registry hips are recorded" in dic,
       "SF16 follow-up runs through the forms and the discharge-data linkage, not clinic attendance")

    # ------------------------------------------------------------------ the asks
    for c in K.CODES:
        for h in K.HOSP:
            ok(nat["A"][c][h] != a["A"][c][h], "Ask A %s %s: the natural read misses" % (c, h))
    m_only = A.asks(target, honour_side=False, merges=True)
    p_only = A.asks(target, honour_side=True, merges=False)
    for h in K.HOSP:
        for s in (nat, m_only, p_only):
            ok(s["C_hosp"][h] != a["C_hosp"][h], "Ask C %s: every stop misses" % h)
    for c in K.CODES:
        for s in (nat, m_only, p_only):
            ok(s["C_construct"][c] != a["C_construct"][c], "Ask C %s: every stop misses" % c)
    case_count = {c: {h: 0 for h in K.HOSP} for c in K.CODES}
    ok(sum(1 for x in T["log"] if x["case"].get("phantom") and x["side"] != x["case"]["side"]) == 4 * len(T["phantoms"]),
       "Ask A: every existing-implant record sits on the side the case did not operate on")
    ok(len(T["phantoms"]) >= 18 and {(p["construct"], p["case"]["hosp"]) for p in T["phantoms"]} ==
       {(c, h) for c in K.CODES for h in K.HOSP}, "Ask A: an existing hip in every construct and hospital cell")
    lots = [x for x in T["log"] if x["action"] == "Implanted" and not x["lot"] and not x["case"].get("phantom")]
    ok(len(lots) > 100, "Ask A: genuine implants without a lot number (the blank lot's benign twin)")
    dev = [m for m in T["merges"] if m["device"]]
    ok({c["hosp"] for c in T["merged_cases"]} == set(K.HOSP) and
       {c["hips"][0]["construct"] for c in T["merged_cases"]} == set(K.CODES), "Ask C: merges at every hospital and construct")
    ok(len(T["merges"]) > 10 * len(dev), "Ask C: device merges are a small share of the merge list")

    # ------------------------------------------------------------------ separation and distractors
    main = ["prosp", "legacy", "revisions", "deaths", "status", "crosswalk", "policy", "dictionary"]
    d = copy_without(target, [K.FILES[k] for k in K.FILES if k not in main])
    g3, _ = A.call(d)
    shutil.rmtree(d)
    ok(all(g3[c]["golden"] == gold[c] for c in K.CODES), "separation: the call computes from the main files alone")
    reg26 = {(r["hospital_mrn"], r["side"]) for r in csv.DictReader(open(P("prosp"), encoding="utf-8"))
             if r["operation_date"].startswith("2026")}
    ph_pat = [T["patients"][p["case"]["patient"]]["mrn"] for p in T["phantoms"]]
    ok(not any((m, s) in reg26 for m, s in zip(ph_pat, [p["side"][0] for p in T["phantoms"]])),
       "separation: no registry row for an existing hip")
    for k in K.DISTRACTORS:
        d = copy_without(target, [K.FILES[k]])
        g4, _ = A.call(d)
        a4 = A.asks(d)
        shutil.rmtree(d)
        ok(all(g4[c]["golden"] == gold[c] for c in K.CODES) and a4 == a, "distractor %s: deleting it changes nothing" % k)

    # ------------------------------------------------------------------ Gate G and the vocabulary sweep
    for k in ("policy", "dictionary", "schedule"):
        t = pdf_text(P(k)).lower()
        ok(not re.search(r"left truncation|delayed entry|risk set|at risk|survivor", t), "%s: no method words" % k)
        ok(not re.search(r"\d\.\d per cent revis", t), "%s: no construct's revision figure" % k)
    ok("percent" not in pdf_text(P("schedule")).lower(), "Gate G: the schedule ranks nothing on revision")

    # ------------------------------------------------------------------ the goldens agree with figures.json
    ok(F["call"]["stays"] == [K.CNAME[c] for c in stays], "figures.json call")
    for c in K.CODES:
        ok(F["call"]["cpr10"][K.CNAME[c]] == float("%.1f" % (int(gold[c] * 10 + 0.5) / 10)), "figures.json %s" % c)
    wb = load_workbook(os.path.join(os.path.dirname(target), "golden", "hip_construct_scorecard_2027.xlsx"), data_only=True)
    ws = wb["Scorecard"]
    got = {r[0]: r for r in ws.iter_rows(min_row=5, max_row=10, values_only=True)}
    for c in K.CODES:
        r = got[K.CNAME[c]]
        ok(r[1] == F["call"]["cpr10"][K.CNAME[c]] and list(r[3:6]) == [a["A"][c][h] for h in K.HOSP] and
           r[6] == sum(a["A"][c].values()) and r[7] == a["C_construct"][c], "scorecard row %s agrees" % c)
    tot = [r for r in ws.iter_rows(min_row=11, max_row=11, values_only=True)][0]
    ok(tot[0] == "All six" and tot[6] == F["ask_a_total"] and tot[7] == F["ask_c_total"], "scorecard totals agree")
    cap = {r[0]: r for r in wb["Registry capture 2026"].iter_rows(min_row=4, values_only=True)}
    ok(all(cap[K.HOSP_NAME[h]][2] == a["C_hosp"][h] for h in K.HOSP), "capture sheet agrees")

    # ------------------------------------------------------------------ H21: invented names clear of real ones
    blob = ""
    for f in files:
        fp = os.path.join(target, f)
        if f.endswith(".pdf"):
            blob += pdf_text(fp) + " "
        elif f.endswith(".csv"):
            blob += open(fp, encoding="utf-8").read(200000) + " "
        else:
            wb2 = load_workbook(fp, read_only=True)
            for ws2 in wb2.worksheets:
                for row in ws2.iter_rows(values_only=True, max_row=400):
                    blob += " ".join(str(v) for v in row if v is not None) + " "
    ok(h21(), "H21: no invented word within two edits of, or containing, a real name on the near-miss register")
    low = blob.lower()
    ok(not any(re.search(r"\b%s\b" % r, low) for r in RETIRED), "H21: no retired name survives the rename")
    for person in re.findall(r"\b(?:Melinda|Richard|Sara) [A-Z][a-z]+", blob):
        ok(person in K.PEOPLE.values(), "personas only from the card (%s)" % person)
    print("checks: %d assertions passed" % N[0])


REAL = ["warwick", "hardwick", "harwich", "warrick", "petaluma", "solvay", "solano", "arcos", "arden", "malvern",
        "tallinn", "keswick", "bracken", "breckenridge", "pelham", "morrow", "barrow", "meadow", "hollister", "hollis",
        "orange", "irvine", "orland", "camden", "hamden", "lassen", "ramsey", "reno", "menlo", "vero", "silvan",
        "sylvan", "becker", "addis", "paris", "allen", "glen", "wilson", "ferrol", "crane", "roane", "exeter", "corail",
        "pinnacle", "taperloc", "accolade", "trident", "tritanium", "summit", "duraloc", "continuum", "trilogy",
        "avenir", "polarstem", "quadra", "amistem", "synergy", "reflection", "anthology", "emperion", "regenerex",
        "ringloc", "profemur", "dynasty", "procotyl", "lineage", "insignia", "actis", "trilock", "gription",
        "securus", "mpact", "ancora", "kinectiv", "fitmore", "allofit", "durom", "metasul", "omnifit", "restoration",
        "rejuvenate", "citation", "meridian", "osteonics", "stryker", "zimmer", "biomet", "depuy", "synthes",
        "smith", "nephew", "exactech", "medacta", "corin", "enovis", "encore", "wright", "conformis", "mathys",
        "aesculap", "globus", "orthofix", "arthrex", "tornier", "optimys", "charnley", "spectron", "versys",
        "tantalum", "bicontact", "plasmacup", "genesis", "legion", "journey", "triathlon", "persona", "vanguard",
        "attune", "sigma", "nexgen", "scorpio", "verilast", "advocate", "aurora", "froedtert", "marshfield",
        "gundersen", "thedacare", "bellin", "prevea", "ascension", "aspirus", "mayo", "sanford", "essentia",
        "mercyhealth", "meriter", "baraboo", "brillion", "kenosha", "racine", "waukesha", "oshkosh", "sheboygan",
        "janesville", "appleton", "eau claire", "tomah", "tomahawk", "stoughton", "sturgeon", "superior"]
RETIRED = ["talvenn", "ardis", "merrow", "fenrow", "venro", "solvane", "brecken", "pellamy", "corvane", "ilsen",
           "orvane", "kessick", "teraluma", "hollis-ward", "tamsen", "harwick"]
GENERIC = set("""health valley joint registry medical center hospital orthopaedic orthopedics surgical medical implants
lake the of and""".split())


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def h21():
    names = {K.SYSTEM, K.REGISTRY} | {h[1] for h in K.HOSPITALS} | {h[2] for h in K.HOSPITALS} | \
        set(K.MAKERS.values()) | {f[1] for f in K.FAMILIES}
    words = {w for n in names for w in re.sub(r"[^a-z ]", " ", n.lower()).split() if w not in GENERIC and len(w) >= 4}
    for w in words:
        for r in REAL:
            if lev(w, r) <= 2 or (len(r) >= 5 and (w in r or r in w)):
                return False
    return True
