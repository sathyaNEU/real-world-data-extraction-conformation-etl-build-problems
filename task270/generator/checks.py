"""task270's checks, run by build.py on every build: the input gates; the client's three rules executed on the
generator's clean truth (R1 the raw material ships, R2 each Layer 1 item neutral, R3a the analyst test, R3b the
decisive step alone, R3c no plant); the ladder, the licensed family and the margins on the shipped pack; the semantic
fork rows; the asks, their devices and the separation line; the cracker; the realism sweep; Gate G and the leak
greps."""
import collections
import csv
import datetime as dt
import inspect
import json
import os
import re

import numpy as np

import analysis as A
import common as K
import cracker as CR
import pack as PK
import world as W

N = {"ok": 0, "fail": 0}
FAILS = []
COMP = K.COMPONENTS
ADMS = [a["name"] for a in K.ADMIN]


def check(label, cond, detail=""):
    if cond:
        N["ok"] += 1
    else:
        N["fail"] += 1
        FAILS.append("%s %s" % (label, detail))


def _pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def truth_sample(rows):
    """The clean truth: every full candidate's scores as the vendors and boards produced them, the appointments and the
    academy criterion, before any record is written."""
    out = []
    for r in rows:
        if not r["full"]:
            continue
        s = {"written": float(r["written"]), "oral": float(r["oral"]), "pat": float(r["pat"]),
             "sjt": float(r["sjt"]), "inventory": float(r["inventory"])}
        app = r["status"] == "Appointed"
        out.append(dict(cand=r["no"], s=s, vet=r["vet"], appointed=app, y=r["acad"] if app else None,
                        pat_pass=r["pat_pass"], listed=r["rank"] is not None, final=r["final"]))
    return out


def keep(v):
    return A.call(v)["keep"]


def run(task, b, fig, exact):
    target = os.path.join(task, "target")
    w = b["w"]
    rows = b["rows"]
    golden_keep = ["written", "oral"]
    golden_order = ["written", "oral", "inventory", "sjt", "pat"]

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    check("INPUT ten or more files", len(files) >= 10, len(files))
    exts = {f.rsplit(".", 1)[-1] for f in files}
    check("INPUT three or more formats", len(exts) >= 3, exts)
    check("INPUT a file of 25,000 rows or more", max(b["counts"].values()) >= 25000, max(b["counts"].values()))
    meta = json.load(open(os.path.join(task, "metadata.json")))
    check("INPUT two or more distractors named in metadata", len(meta["distractors"]) >= 2)
    for d in meta["distractors"]:
        check("INPUT distractor shipped " + d, d in files)
        check("INPUT distractor not named for its role " + d, "distract" not in d.lower())
    check("INPUT every file has provenance", set(meta["provenance"]) >= set(files))
    contents = open(os.path.join(target, K.FILES["contents"]), encoding="utf-8").read()
    listed = {l.strip() for l in contents.splitlines() if l.strip() and not l.startswith(" ") and "." in l
              and " " not in l.strip()}
    check("INPUT the contents list names every other file (H9)", listed == set(files) - {K.FILES["contents"]},
          sorted(set(files) ^ (listed | {K.FILES["contents"]})))

    # ------------------------------------------------------------------ R3a and R3b on the clean truth
    ts = truth_sample(rows)
    rt = A.routes(ts)
    check("R3a the analyst test: the appointees' correlations on the clean truth keep the written test and the "
          "inventory", keep(rt["appointees"]) == ["written", "inventory"], keep(rt["appointees"]))
    check("R3a the field's reflex (Case II on each component) on the clean truth keeps the written test and the "
          "inventory", keep(rt["case2"]) == ["written", "inventory"], keep(rt["case2"]))
    check("R3b the decisive step alone on the clean truth files the golden", keep(rt["golden"]) == golden_keep,
          keep(rt["golden"]))
    for m in ("appointees", "case2", "mixed"):
        check("R3b a lower rung stays wrong on the clean truth: " + m, keep(rt[m]) != golden_keep, keep(rt[m]))
    check("R3 the clean truth's order equals the pack's", A.order(rt["golden"]) == golden_order, A.order(rt["golden"]))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    def hdr(k):
        return next(csv.reader(open(os.path.join(target, K.FILES[k]), encoding="utf-8")))
    check("R1 the written test results carry each candidate's scaled score", {"client_reference", "scaled_score"} <= set(hdr("written")))
    check("R1 the oral board ratings carry every rating", {"candidate_no", "rater", "dimension", "rating"} <= set(hdr("oral")))
    check("R1 the course sheets carry every run", {"candidate_no", "attempt", "course_seconds", "points"} <= set(hdr("pat")))
    check("R1 the lists carry every listed candidate's disposition", {"disposition", "employee_no", "final_score"} <= set(hdr("roster")))
    for k in ("roster", "crosswalk", "written", "oral", "pat", "inventory", "ledger", "ats_old", "ats_new", "calendar"):
        h = " ".join(hdr(k)).lower()
        for wd in ("valid", "correl", "corrected", "restrict", "predict", "criterion"):
            check("R1 no shipped column names the deciding quantity (%s, %s)" % (k, wd), wd not in h)
    smp = PK.sample(target)
    check("R1 the pool on the pack is the clean truth's pool", len(smp) == len(ts) == fig["components"]["pool"])
    check("R1 the appointees on the pack are the clean truth's",
          sum(m["appointed"] for m in smp) == sum(m["appointed"] for m in ts) == fig["components"]["appointees"])

    # ------------------------------------------------------------------ R2: each Layer 1 item is neutral
    layer1 = {"the written test's raw score for the scaled": dict(written="raw_score"),
              "the oral board's sum of ratings for the mean": dict(oral="sum"),
              "the course's first run for the faster": dict(pat="first"),
              "the course's time for its points": dict(pat="time"),
              "Pellwyn's raw score for the scaled": dict(sjt_key="Raw score"),
              "separated recruits dropped (the new layout's own column missed)": dict(separated=False)}
    for name, kw in layer1.items():
        s2 = PK.sample(target, **kw)
        r2 = A.routes(s2)
        check("R2 neutral: %s keeps the call" % name, keep(r2["golden"]) == golden_keep, keep(r2["golden"]))
        check("R2 neutral: %s keeps the first below" % name, A.call(r2["golden"])["first_below"] == "inventory")
        check("R2 neutral: %s leaves the default path wrong" % name, keep(r2["case2"]) != golden_keep)

    # ------------------------------------------------------------------ R3c: no plant
    for k in ("written", "oral", "pat", "inventory", "roster"):
        body = open(os.path.join(target, K.FILES[k]), encoding="utf-8").read().splitlines()[1:]
        tails = [",".join(l.split(",")[1:]) for l in body]
        runs = sum(1 for i in range(2, len(tails)) if tails[i] == tails[i - 1] == tails[i - 2])
        check("R3c no copied block of rows, three alike in a row (%s)" % k, runs == 0, runs)
    texts = {k: _pdf_text(os.path.join(target, K.FILES[k])) for k in ("rules", "plan", "handbook", "jobs")}
    for k, t in texts.items():
        low = t.lower()
        check("R3c no shipped document ranks the components by a figure (%s)" % k,
              not re.search(r"(rank|order)\w* (of|by) (the )?(component|validit)", low))

    # ------------------------------------------------------------------ the ladder and the licensed family
    ro = exact["routes"]
    check("LADDER R0 (appointees) keeps the inventory and the written test", keep(ro["appointees"]) == ["written", "inventory"])
    check("LADDER R1 (Case II) keeps the written test and the inventory", keep(ro["case2"]) == ["written", "inventory"])
    check("LADDER R2 (mixed) keeps the written test and the inventory", keep(ro["mixed"]) == ["written", "inventory"])
    check("LADDER R3 (golden) keeps the written test and the oral board", keep(ro["golden"]) == golden_keep)
    check("LADDER the oral board is never in the pair before R3",
          all("oral" not in keep(ro[m]) for m in ("appointees", "case2", "mixed")))
    g = ro["golden"]
    check("LADDER the golden margin at the cut is 0.10 or more", g[1] - g[4] >= 0.10, g[1] - g[4])
    for m in A.LICENSED:
        check("SF8 the licensed correction %s keeps the pair" % m, keep(ro[m]) == golden_keep, keep(ro[m]))
        check("SF8 the licensed correction %s gives the order" % m, A.order(ro[m]) == golden_order, A.order(ro[m]))
        srt = np.sort(ro[m])[::-1]
        check("SF8 adjacent validities 0.03 apart or more under %s" % m, (-np.diff(srt)).min() >= 0.03,
              (-np.diff(srt)).min())
    check("SF15 every validity positive under every route", all((v > 0).all() for v in ro.values()))
    X, vet, a, Y, fin = A.arrays(smp)
    u_fin = fin.std(ddof=1) / fin[a].std(ddof=1)
    u_w = X[:, 0].std(ddof=1) / X[a, 0].std(ddof=1)
    u_o = X[:, 1].std(ddof=1) / X[a, 1].std(ddof=1)
    check("LADDER the composite is cut harder than either ranked component (the stump's arithmetic)",
          u_fin > 1.9 and u_w < 1.4 and u_o < 1.5, (u_fin, u_w, u_o))

    # ------------------------------------------------------------------ the semantic fork rows
    plan, rules, hb = texts["plan"], texts["rules"], texts["handbook"]
    check("SF1 the pool: everyone who sat all five, appointed or not",
          "every candidate who sat all five components in the four examinations, whether or not they were appointed" in plan)
    check("SF2 the criterion and separations", "average the academy recorded at separation" in plan and
          "average at separation" in hb)
    s_grad = PK.sample(target, separated=False)
    check("SF2 graduates only keeps the call", keep(A.routes(s_grad)["golden"]) == golden_keep)
    check("SF3 the written test score is the scaled score", "written test score is the scaled score" in rules)
    check("SF4 the oral board score is the mean of the ratings given, times 20",
          "mean of the ratings given, multiplied by 20" in rules)
    check("SF5 the faster run counts and its points", "the faster time counts" in rules and "points for the faster run" in plan)
    check("SF6 Pellwyn's scaled score", "Pellwyn's scaled score" in plan)
    check("SF7 the inventory's Dependability scale", "Dependability scale" in plan)
    check("SF9 the veterans' credit stays out under ranked_only and the pair holds", keep(ro["ranked_only"]) == golden_keep)
    pp = np.array([1.0 if m["pat_pass"] else 0.0 for m in smp])
    check("SF10 the course's pass is constant among the appointees (no correction can carry it)",
          pp[a].min() == pp[a].max() == 1.0)
    cands = np.array([m["cand"][:3] for m in smp])
    zs, ws = [], []
    for code in sorted(set(cands)):
        msk = cands == code
        Zs = np.column_stack([X[msk, 0], X[msk, 1], vet[msk], X[msk, 2], X[msk, 3], X[msk, 4], Y[msk]])
        Ps = A.to_r(A.lawley(np.cov(Zs[:, :4].T), np.cov(Zs[a[msk]].T), [0, 1, 2, 3], [4, 5, 6]))
        zs.append(np.arctanh([Ps[0, 6], Ps[1, 6], Ps[3, 6], Ps[4, 6], Ps[5, 6]]))
        ws.append(msk.sum())
    zbar = np.tanh(np.average(np.array(zs), axis=0, weights=ws))
    check("SF11 each examination corrected on its own and combined keeps the pair and the order",
          keep(zbar) == golden_keep and A.order(zbar) == golden_order, A.order(zbar))
    check("SF12 the plan's validity is the correlation", "validity is the correlation between its score and the "
          "criterion across the candidate pool" in plan)
    allapp = sum(1 for r in rows if r["status"] == "Appointed")
    check("SF13 the appointees in the pool are fewer than every appointee (partial candidates are out)",
          fig["components"]["appointees"] < allapp, (fig["components"]["appointees"], allapp))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, K.FILES["academy"]), read_only=True)
    check("SF14 the new layout carries the average at separation in its own column",
          "Average at Separation" in [c.value for c in next(wb["26-1"].iter_rows(max_row=1))])

    # ------------------------------------------------------------------ asks
    ct = W.cost_truth(rows, w["L"])
    check("ASK A the golden equals the truth", all(fig["ask_a"][K.LABEL[c]] == round(ct[0][c], 2) for c in COMP))
    for c in COMP:
        v = ct[0][c] * 100
        check("ASK A %s sits a tenth of a cent or more from a rounding edge" % c, abs((v % 1) - 0.5) >= 0.1, v)
    for how in ("every_line", "accruals_out", "named_only"):
        alt = A.cost(target, how)[0]
        check("ASK A stop %s misses every figure" % how,
              all(abs(round(alt[c], 2) - fig["ask_a"][K.LABEL[c]]) >= 0.01 for c in COMP),
              {c: round(alt[c], 2) for c in COMP})
    L = w["L"]
    acc24 = [l for l in L if l["kind"] == "accrual" and l["date"].year == 2024]
    acc25 = [l for l in L if l["kind"] == "accrual" and l["date"].year == 2025]
    rev = [l for l in L if l["kind"] == "reversal"]
    check("ASK A one reversal, equal to the 2024 accruals", len(rev) == 1 and
          abs(rev[0]["amount"] + sum(l["amount"] for l in acc24)) < 0.005)
    check("ASK A the 2024 accruals cover all five components", {l["cc"] for l in acc24} == set(K.CC_OF.values()))
    check("ASK A the 2025 accruals cover all five components", {l["cc"] for l in acc25} == set(K.CC_OF.values()))
    relief = [l for l in L if l["kind"] == "relief" and l["date"].year == 2025]
    check("ASK A every 2025 accrual has its invoice's difference on the same purchase order",
          {l["po"] for l in relief} == {l["po"] for l in acc25})
    check("ASK A some 2025 differences are negative", any(l["amount"] < 0 for l in relief))
    check("ASK A no reversal of the 2025 accruals", not any("FY2025" in l["narration"] and "Reversal" in l["narration"] for l in L))
    ledger_text = open(os.path.join(target, K.FILES["ledger"]), encoding="utf-8").read().lower()
    for wd in ("relief", "relieved", "matched", "difference", "double", "net of accrual"):
        check("ASK A no ledger line narrates the device ('%s')" % wd, wd not in ledger_text)
    at = W.applicant_truth(w["by_adm"])
    code = {a["name"]: a["code"] for a in K.ADMIN}
    check("ASK B the golden equals the truth", all(fig["ask_b"]["applicants"][n] == at[code[n]] for n in ADMS),
          (fig["ask_b"]["applicants"], at))
    stops = {"name and date of birth only": ("name_dob",), "email only": ("email",),
             "name and date of birth or email": ("name_dob", "email"),
             "name and date of birth or name and phone": ("name_dob", "name_phone"),
             "email or name and phone": ("email", "name_phone"), "phone only": ("phone",), "name only": ("name",)}
    for name, keys in stops.items():
        alt = A.applicants(target, keys=keys)
        check("ASK B stop '%s' misses every examination" % name,
              all(alt[n] != fig["ask_b"]["applicants"][n] for n in ADMS), alt)
    alt = A.applicants(target, laterals="title")
    check("ASK B laterals by title misses autumn 2025", alt["Autumn 2025"] != fig["ask_b"]["applicants"]["Autumn 2025"])
    alt = A.applicants(target, window=False)
    check("ASK B no window misses autumn 2025", alt["Autumn 2025"] != fig["ask_b"]["applicants"]["Autumn 2025"])
    # the identity graph is exact: no two people share a key, every person's forms share one
    def norm(s):
        return " ".join(s.lower().split())
    for a_ in K.ADMIN:
        cd = a_["code"]
        late = set(w["by_adm"][cd]["late"])
        recs = [r for r in w["legacy"] + w["new"] if r["adm"] == cd]
        seen = {"nd": {}, "em": {}, "np": {}}
        clash = 0
        for r in recs:
            for kk, v in (("nd", (norm(r["first"]), norm(r["last"]), r["dob"])), ("em", r["email"].lower()),
                          ("np", (norm(r["first"]), norm(r["last"]), r["phone"]))):
                if kk == "em" and not v:
                    continue
                if v in seen[kk] and seen[kk][v] != r["pid"]:
                    clash += 1
                seen[kk][v] = r["pid"]
        check("ASK B no two people share a key in %s" % cd, clash == 0, clash)
        by = collections.defaultdict(list)
        for r in recs:
            if r["track"] == "entry" and r["status"] != "Incomplete" and not r.get("migrated") and r["pid"] not in late:
                by[r["pid"]].append(r)
        kinds = collections.Counter()
        for pid, rs in by.items():
            if len(rs) == 2:
                x, y = rs
                kinds[(x["dob"] == y["dob"], x["email"].lower() == y["email"].lower(), x["phone"] == y["phone"])] += 1
        check("ASK B every pair of forms shares a key in %s" % cd, kinds[(False, False, False)] == 0)
        for kind, nm in (((False, True, False), "email"), ((False, False, True), "name and phone"),
                         ((True, False, False), "name and date of birth")):
            check("ASK B three or more pairs joined only by %s in %s" % (nm, cd), kinds[kind] >= 3, kinds[kind])
    comp = A.completion(target)
    check("ASK B completion rates recompute", all(round(comp[c], 2) == fig["ask_b"]["completion"][K.LABEL[c]] for c in COMP))
    check("ASK B completion rates differ by component", len(set(fig["ask_b"]["completion"].values())) == 5)
    camp = open(os.path.join(target, K.FILES["campaign"]), "rb").read()
    check("ASK the campaign workbook ties no applicant count", all(str(v).encode() not in camp
                                                                for v in fig["ask_b"]["applicants"].values()))

    # ------------------------------------------------------------------ separation
    for fn in (PK.scores, PK.sample, PK.academy, PK.register):
        src = inspect.getsource(fn)
        for k in ("ledger", "ats_old", "ats_new", "campaign", "calendar"):
            check("SEPARATION the call's loader %s opens no ask file (%s)" % (fn.__name__, k), '"%s"' % k not in src)
    src = inspect.getsource(A.cost) + inspect.getsource(A.applicants) + inspect.getsource(A.completion)
    check("SEPARATION the asks read the score files only through the counts of who sat",
          "sample(" not in src and "routes(" not in src)

    # ------------------------------------------------------------------ cracker and pair
    cr = CR.run(target, quiet=True)
    check("CRACKER keeps none of the 14 ask figures", cr["kept"] == 0, cr["kept"])
    check("CRACKER pair ceiling 40 or under", cr["pair"] <= 40, cr["pair"])

    # ------------------------------------------------------------------ realism
    sat = fig["sat"]
    check("REALISM candidates who sat differ by component", len(set(sat.values())) == 5, sat)
    per_adm = W.sat_counts(rows)
    check("REALISM written test sitters differ by examination", len({v["written"] for v in per_adm.values()}) == 4)
    for c, v in fig["ask_a"].items():
        check("REALISM cost per candidate not round (%s)" % c, abs(v * 100 % 100) > 1e-6 and (v * 100) % 10 != 0, v)
    for n, v in fig["ask_b"]["applicants"].items():
        check("REALISM applicants not round (%s)" % n, v % 10 != 0, v)
    card = json.load(open(os.path.join(os.path.dirname(task), ".claude", "skills", "fingerprint", "cards", "task270.json")))
    allt = " ".join(texts.values())
    for p in card["world"]["people"]:
        check("REALISM persona from the card appears: " + p, p in allt)
    sep = sum(1 for r in rows if r["separated"] is not None)
    check("REALISM some recruits separated", 10 <= sep <= 120, sep)
    people = {r["pid"]: (r["first"], r["last"]) for r in rows}
    names = collections.Counter(people.values())
    check("REALISM people sharing a name are a few per cent", sum(v for v in names.values() if v > 1) < 0.04 * len(people),
          (sum(v for v in names.values() if v > 1), len(people)))
    for f in files:
        data = open(os.path.join(target, f), "rb").read()
        for wd in (b"ReportLab", b"openpyxl", b"python-docx", b"matplotlib"):
            check("REALISM no writer's name in %s (%s)" % (f, wd.decode()), wd not in data)
    latest = dt.date(2000, 1, 1)
    for f in files:
        if f.endswith(".csv"):
            for row in csv.reader(open(os.path.join(target, f), encoding="utf-8")):
                for cell in row:
                    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", cell)
                    if m:
                        latest = max(latest, dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
    check("REALISM no record after the pack's assembly (6 October 2026)", latest <= K.ASSEMBLED.date(), latest)
    for nm in ("Brightwater", "Sinclair", "Wright State", "Central State", "Northgate"):
        check("REALISM H21 no real organisation's name: " + nm, all(nm.encode() not in open(os.path.join(target, f), "rb").read()
                                                                     for f in files))
    bad = h21()
    check("H21 invented names clear of real places and organisations (none within two edits of a real one, none "
          "containing one)", not bad, bad)

    # ------------------------------------------------------------------ Gate G and the leak greps
    docs = " ".join(texts.values()).lower() + contents.lower()
    for wd in ("range restriction", "restriction of range", "restricted", "case ii", "case iii", "thorndike", "lawley",
               "pearson", "corrected", "correction", "selection effect", "incidental", "explicit selection",
               "multivariate", "selection ratio", "unrestricted", "attenuat", "covarian"):
        check("LEAK no shipped document says '%s'" % wd, wd not in docs)
    for wd in ("day first", "day-first", "swapped", "month first", "duplicate applicant", "same person"):
        check("LEAK no shipped document narrates an ask device ('%s')" % wd, wd not in docs)
    check("GATE G no shipped file ranks the components on validity", "validity" not in contents.lower())

    print("checks: %d passed, %d failed" % (N["ok"], N["fail"]))
    for f in FAILS[:60]:
        print("  FAIL", f)
    return 0 if not FAILS else 1


# real places and organisations the invented names were screened against: Ohio's cities and the Dayton region's
# towns, the region's colleges, and the public-safety testing and staffing firms the fiction sits beside
REAL = ["Akron", "Canton", "Dayton", "Kettering", "Xenia", "Fairborn", "Beavercreek", "Huber Heights", "Miamisburg",
        "Centerville", "Springfield", "Troy", "Piqua", "Sidney", "Lebanon", "Middletown", "Hamilton", "Fairfield",
        "Mason", "Kent", "Kenton", "Medina", "Mentor", "Lorain", "Elyria", "Sandusky", "Findlay", "Lima", "Marion",
        "Mansfield", "Massillon", "Zanesville", "Newark", "Lancaster", "Chillicothe", "Athens", "Marietta",
        "Portsmouth", "Steubenville", "Youngstown", "Warren", "Toledo", "Cleveland", "Columbus", "Cincinnati",
        "Dublin", "Westerville", "Delaware", "Wooster", "Ashland", "Bowling Green", "Tiffin", "Fremont", "Norwalk",
        "Defiance", "Wapakoneta", "Bellefontaine", "Urbana", "Greenville", "Eaton", "Wilmington", "Hillsboro",
        "Circleville", "Kessler", "Sinclair", "Wright State", "Central State", "Cedarville",
        "Wittenberg", "Antioch", "Stanard", "Ergometrics", "Biddle", "Morris McDaniel", "Hogan", "Pearson",
        "Prometric", "Brightwater", "Northgate", "Pelham", "Pellston", "Kelly Services",
        "Robert Half", "Adecco", "Manpower", "Express Employment"]
INVENTED = ["Kessling", "Halvorsen", "Pellwyn", "Kessling Temporary", "Kessling State", "Kessling Convention"]
GENERIC = {"college", "state", "university", "center", "centre", "temporary", "services", "partners", "systems",
           "selection", "assessment", "the", "of", "city", "division"}


def _key(name):
    return " ".join(w for w in re.sub(r"[^a-z ]", " ", name.lower()).split() if w not in GENERIC)


def _edits(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def h21():
    bad = []
    for inv in INVENTED:
        ki = _key(inv)
        for real in REAL:
            kr = _key(real)
            if not ki or not kr:
                continue
            if ki == kr or (len(kr) > 3 and kr in ki) or _edits(ki, kr) <= 2:
                bad.append((inv, real))
    return bad
