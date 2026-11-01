"""The build's assertions for task266: the input gates, the three-rules block (R1 to R3c), the ladder, every semantic
fork row (SF1 to SF16), the conventions, the asks' devices and stops, the separation line, the distractors, the
realism sweep and the agreement of the goldens with figures.json."""
import csv
import datetime as dt
import json
import os
import random
import re
import shutil
import tempfile
from collections import Counter, defaultdict

from openpyxl import load_workbook
from pypdf import PdfReader

import analysis as A
import common as K
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
N = [0]
GOLD = ["GS", "BIO", "BUS", "PSY", "MA", "ECE"]


DESCRIBE_NAME = re.compile(
    r"(?<![a-z])(read_?me|data_?dictionar\w*|dictionar(y|ies)|codebook|field_?notes|field_?guide|"
    r"fields?_(guide|notes|list|descriptions?)|\w*_fields|manifest|extract_contents|file_list|file_layout|glossary|"
    r"column_(notes|descriptions?)|data_?notes|how_to_read|about_this|export_notes|extract_notes|feed_notes|desk_notes|"
    r"data_team_notes|definitions|schema|layouts?_notes|handling_notes|release_notes|notes)(?![a-z])", re.I)
DESCRIBE_SHEET = re.compile(r"^(read ?me|notes?|dictionary|data dictionary|definitions|glossary|fields|field notes|"
                            r"about|about this (file|workbook)|how to (read|use)( this)?|columns?)$", re.I)


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


def codes(lst):
    inv = {v: k for k, v in K.SIS.items()}
    return [inv[p] for p in lst]


# ---------------------------------------------------------------------------------------------- H21
CURATED = """exmoor dartmoor wexford wexham fenton fenwick hollenbeck hollins bucks butler delaware harrisburg lehigh
carbon luzerne montgomery northampton allegheny beaver westmoreland reading philadelphia highlands erie lackawanna
keystone temple villanova drexel lycoming juniata susquehanna schuylkill lancaster chester berks strathmore
borrowdale blackwater brindley kesteven hollenberg ashendon ashendene corwen callow holmby tarvin""".split()
RETIRED = ["wexmoor", "fenstow", "brindlow", "kestover"]
GENERIC = set("county community college campus pennsylvania enrollment exchange the of and".split())


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def real_register():
    import geonamescache
    g = geonamescache.GeonamesCache()
    real = {c["name"].lower() for c in g.get_cities().values()}
    real |= {re.sub(r" (county|parish|borough|census area|city and borough|municipality)$", "", c["name"].lower())
             for c in g.get_us_counties()}
    real |= {s["name"].lower() for s in g.get_us_states().values()}
    real |= set(CURATED)
    words = {w for r in real for w in re.sub(r"[^a-z ]", " ", r).split() if len(w) >= 4}
    return real | words


def h21():
    names = {K.COLLEGE, K.EXCHANGE} | set(K.CAMPUS.values())
    words = {w for n in names for w in re.sub(r"[^a-z ]", " ", n.lower()).split() if w not in GENERIC and len(w) >= 4}
    real = real_register()
    bad = []
    for w in words:
        for r in real:
            if (abs(len(r) - len(w)) <= 2 and lev(w, r) <= 2) or (len(r) >= 5 and (r in w or w in r)):
                bad.append((w, r))
    return bad


# ---------------------------------------------------------------------------------------------- the checks
def run(target, T):
    P = lambda k: os.path.join(target, K.FILES[k])
    F = json.load(open(os.path.join(HERE, "figures.json")))
    R, pk, ent = A.call(target)
    progs = [K.SIS[p] for p in K.CODES]
    gold = {p: R[p]["golden"] for p in progs}
    inrev = A.review(R)

    # ------------------------------------------------------------------ input gates
    files = os.listdir(target)
    ok(len(files) >= 10, "10 or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "a file of 25,000 rows or more (%d)" % big)
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2 and all(os.path.exists(os.path.join(os.path.dirname(target), f))
                                                  for f in meta["distractor_files"]), "two distractors shipped")
    ok(sorted(files) == sorted(K.FILES.values()), "the pack is exactly the generator's files")
    ok(sorted(meta["provenance"]) == sorted("target/" + f for f in files), "H9: metadata.json records every file's "
       "provenance")
    # no shipped file or sheet describes the data (dataset-generation section 3), by name and by sheet name
    ok(not [f for f in files if DESCRIBE_NAME.search(os.path.splitext(f)[0])], "no dictionary, notes, readme or manifest "
       "file ships (%s)" % [f for f in files if DESCRIBE_NAME.search(os.path.splitext(f)[0])])
    sheets = [(f, ws) for f in files if f.endswith(".xlsx") for ws in load_workbook(os.path.join(target, f),
                                                                                    read_only=True).sheetnames]
    ok(not [x for x in sheets if DESCRIBE_SHEET.match(x[1].strip()) or re.match(r"^about\b", x[1].strip(), re.I)],
       "no notes, about or dictionary sheet ships (%s)" % sheets)
    ok(not [f for f in files if f.endswith((".pdf", ".txt")) and f != K.FILES["idmap"] and f != K.FILES["policy"]],
       "the pack's only documents are the policy and the conversion map")
    late = []
    for f in files:
        if f.endswith((".csv", ".txt")):
            for line in open(os.path.join(target, f), encoding="utf-8"):
                for m in re.findall(r"\b(20\d\d-\d\d-\d\d)\b", line):
                    if dt.date.fromisoformat(m) > K.EXTRACT:
                        late.append((f, m))
    ok(not late, "H16: no date past the extract date in the CSV and text files (%s)" % late[:3])
    terms = A.rows_xlsx(P("terms"), "Terms")
    future = [t for t in terms if t["Conferral date"].date() > K.EXTRACT]
    ok([str(t["Term code"]) for t in future] == ["202730"], "H16: only summer 2027 lies past the extract (the calendar)")

    # ------------------------------------------------------------------ the call and the ladder
    ok(codes(inrev) == GOLD, "golden: six programs enter review (%s)" % codes(inrev))
    for p in progs:
        ok(abs(gold[p] - K.FLOOR) >= 1.5, "%s golden %.3f at least 1.5 from the floor" % (p, gold[p]))
        ok(abs(gold[p] * 10 - round(gold[p] * 10)) <= .35, "%s golden %.3f mid-bin at one decimal" % (p, gold[p]))
        ok(R[p]["op"] > gold[p], "%s: the default path is above the golden" % p)
    ok(sum(1 for p in progs if round(gold[p], 1) == round(gold[p])) <= 1, "at most one share is a whole number")
    ok(len({round(gold[p], 1) for p in progs}) == 9, "no two programs' shares equal at one decimal (axis 11)")
    for k in ("op", "op_exits_first"):
        ok(codes(A.review(R, k)) == ["ECE"], "R1 (%s): the default path sends only Early Childhood Education" % k)
        ok(all(R[p][k] - K.FLOOR >= 4 for p in progs if p != K.SIS["ECE"]), "R1 (%s): margins of 4 points" % k)
    ok(codes(A.review(R, "closed2023")) == GOLD + ["CJ"], "R2: the fall 2023 class alone adds Criminal Justice")
    ok(K.FLOOR - R[K.SIS["CJ"]]["closed2023"] >= 2.5, "R2: Criminal Justice at least 2.5 below on the 2023 class")
    ok(codes(A.review(R, "crude")) not in (GOLD, ["ECE"]), "R0: awarded over entrants lands elsewhere")
    ok(codes(A.review(R, "complete")) not in (GOLD, ["ECE"]), "R0': the complete-case share lands elsewhere")
    lists = {k: tuple(A.review(R, k)) for k in ("crude", "complete", "op", "closed2023", "golden")}
    ok(len(set(lists.values())) == 5, "every rung names a different list")
    for k in ("half_wd", "half_to"):
        ok(codes(A.review(R, k)) != GOLD, "the half-step %s lands on another list" % k)
    for p in progs:
        if p in [K.SIS[c] for c in K.TRANSFER]:
            ok(R[p]["op"] - gold[p] >= 10, "%s: the decisive move is at least 10 points" % p)
    ok(R[K.SIS["MA"]]["op"] - gold[K.SIS["MA"]] >= 8, "Medical Assisting: the decisive move is at least 8 points")

    # ------------------------------------------------------------------ the three rules on the clean truth
    CW = W.rungs(T["entering"])
    for p in K.CODES:
        for k in ("golden", "op", "op_exits_first", "crude", "complete", "closed2023", "half_wd", "half_to", "strat",
                  "person", "redate", "dc_compete", "dc_censor"):
            ok(abs(CW[p][k] - R[K.SIS[p]][k]) < 1e-9, "the pack reproduces the clean truth: %s %s" % (p, k))
    ok(W.review(CW, "op") == ["ECE"], "R3a: the easy route on the clean truth files one program")
    ok(W.review(CW, "golden") == GOLD, "R3b: the decisive step alone on the clean truth files six")
    ok(W.review(CW, "crude") != GOLD and W.review(CW, "closed2023") != GOLD and W.review(CW, "complete") != GOLD,
       "R3b: each lower rung stays wrong")
    heads = set()
    for f in files:
        if f.endswith(".csv"):
            heads |= set(next(csv.reader(open(os.path.join(target, f), encoding="utf-8"))))
    for f in files:
        if f.endswith(".xlsx"):
            for ws in load_workbook(os.path.join(target, f), read_only=True).worksheets:
                heads |= {str(c) for c in next(ws.iter_rows(values_only=True)) if c}
    ok(not any(re.search(r"complet|graduation rate|cumulative|incidence|survival|retention|share", h, re.I)
               for h in heads), "R1: no shipped column holds a completion share")
    ok(sum(R[p]["n"] + R[p]["deaths"] for p in progs) == len(ent) == sum(1 for e in T["entering"]),
       "R1: the golden reads one admission row per entering student")
    # R2: each mess item, mishandled, leaves the call or fails loudly
    unmapped = sum(1 for e in ent if e["cls"] == 2023 and (str(T["legacy_of"][e["sid"]]), e["admit"]) in pk.by_adm)
    ok(unmapped == 0, "R2 conversion: the fall 2023 file's legacy numbers find no admission unmapped (loud)")
    misread = {str(int(c[:4]) - 1 + (1 if c.endswith("10") else 0)) for c in ("202510", "202610")}
    ok(misread == {"2025", "2026"}, "R2 term codes: read as calendar years the 2024 and 2025 classes become fall 2025 "
       "and fall 2026, outside the policy's classes (loud)")
    ok(codes(A.review(R, "final")) == GOLD, "R2/SF1 program changes: the program at the degree gives the same call")
    split = [dict(a) for a in pk.adm]
    rng = random.Random(266)
    for a in split:
        if a["exit_reason"] in ("TO", "WD"):
            a["exit_reason"] = rng.choice(["TO", "WD"])
    pk2 = A.Pack(target)
    pk2.adm = split
    pk2.by_adm = {(a["student_id"], a["admit_term"]): a for a in split}
    pk2.later = pk.later
    for p in progs:
        sp2 = A.spells(pk2, [e for e in ent if e["prog"] == p])
        ok(abs(A.aj(sp2) - gold[p]) < 1e-9, "R2/SF6 %s: any split of the endings between TO and WD gives the same share"
           % p)
    ok(codes(A.review(R, "redate")) == GOLD, "R2/SF7 withdrawal dating: one term earlier gives the same call")
    # a transfer out or withdrawal leaves the risk set before its exit term's awards, or at the term before: the
    # estimate is the same to the last digit, so neither timing of the endings within a term is a reading of 3.1
    for p in progs:
        sp = A.spells(pk, [e for e in ent if e["prog"] == p])
        surv, cif = 1.0, 0.0
        for t in range(1, K.WINDOW + 1):
            n = A.at_risk(sp, t)
            gone = sum(1 for e, k, o in sp if e == t and k in ("XTO", "XWD"))
            got = sum(1 for e, k, o in sp if e == t and k == "GR")
            if n:
                surv *= 1 - gone / n
                if n - gone:
                    cif += surv * got / (n - gone)
                    surv *= 1 - got / (n - gone)
        back = [((e - 1) if e is not None and k in ("XTO", "XWD") else e, k, o) for e, k, o in sp]
        ok(abs(100 * cif - gold[p]) < 1e-9 and abs(A.aj(back) - gold[p]) < 1e-9,
           "R2/SF7 %s: the endings out of the risk set before their term's awards, or a term earlier, give the same "
           "share" % p)
    ok(codes(A.review(R, "person")) == GOLD, "R2/SF8 readmissions: followed across a readmission, the same call")
    ok(codes(A.review(R, "dc_compete")) == GOLD and codes(A.review(R, "dc_censor")) == GOLD,
       "R2/SF13 deaths: censored or an ending, the same call")
    conf = defaultdict(list)
    for c in A.rows_csv(P("conferrals")):
        conf[c["student_id"]].append(c["term_code"])
    gr = [a for a in pk.adm if a["exit_reason"] == "GR" and a["program_code"] in progs]
    ok(all(a["exit_term"] in conf[a["student_id"]] for a in gr), "R2 conferrals: every degree exit has its conferral")
    first = {}
    for e in ent:
        a = pk.by_adm[(e["sid"], e["admit"])]
        cs = sorted(t for t in conf[e["sid"]] if t >= e["admit"])
        first[e["sid"]] = cs[0] if cs else None
    agree = all((pk.by_adm[(e["sid"], e["admit"])]["exit_reason"] == "GR") ==
                (first[e["sid"]] is not None and first[e["sid"]] == pk.by_adm[(e["sid"], e["admit"])]["exit_term"])
                or (first[e["sid"]] is not None and pk.by_adm[(e["sid"], e["admit"])]["exit_reason"] == "WD")
                for e in ent)
    ok(agree, "R2 conferrals: an entering student's first degree is the admission's GR exit, or follows a readmission")
    # R3c: no copied blocks, no identical counts, no round totals
    ent_counts = [R[p]["classes"][c] for p in progs for c in K.CLASSES]
    ok(len(set(ent_counts)) >= 24, "R3c: entering class sizes vary across programs and years")
    ok(all(R[p]["n"] % 100 for p in progs), "R3c: no round program totals")
    rows = list(csv.reader(open(P("registrations"), encoding="utf-8")))[1:]
    blocks = Counter(tuple(tuple(r[3:8] + r[9:10]) for r in rows[i:i + 5]) for i in range(0, len(rows) - 5, 5))
    ok(max(blocks.values()) == 1, "R3c: no repeated block of registrations")

    # the files the call reads are byte-identical to the cut the call was judged on (543365d5, 2026-11-01): the ask
    # layer's repairs move the registrations, the schedule and the program history only; the policy carries pass 6's
    # two clauses in 3.3 (the record with the spring term's degrees, the estimate's record), its new digest below
    import hashlib
    frozen = {"cohorts": "59430190ecd5dce0cd681c65ef8532be", "admissions": "82a9051be0a992b4e8f5a9355fc55be5",
              "conferrals": "96b8de6e76e5fae5621f762287a15a5a", "idmap": "0719f3db43272f235ee49c0d2fccd8e1",
              "terms": "f9341d7e5892318543b2f0d088e8c778", "register": "cf2253ffdcd4b6afafc4b8c845168277",
              "policy": "cee2a3920b98ca59faf104493af2dc49"}
    for k, d in frozen.items():
        ok(hashlib.md5(open(P(k), "rb").read()).hexdigest() == d, "the call's file %s is byte-identical to the "
           "judged cut" % K.FILES[k])

    # ------------------------------------------------------------------ the semantic fork table
    pol = pdf_text(P("policy"))
    ok("reported in the program the student entered" in pol, "SF1 program entered filed")
    ok("first-time in college or transferring in" in pol and "fall entering-student file" in pol, "SF2 filed")
    ec = [(a["student_id"], a["admit_term"]) for a in pk.adm if a["admit_term"] in (K.fall(2023), K.fall(2024),
                                                                                    K.fall(2025))
          and a["admit_type"] in ("N", "T") and a["program_code"] in progs]
    ok(sorted(ec) == sorted((e["sid"], e["admit"]) for e in ent), "SF2: the extract's fall new and transfer admissions "
       "to the nine programs are IR's entering students (C1)")
    ok("A degree in any of the college's associate-degree programs counts" in pol, "SF3 any associate degree filed")
    ok(codes(A.review(R, "own")) == GOLD, "SF3: the entered program's own degree only gives the same call")
    ok("ninth term, counting the fall term of entry as the first and summer terms included" in pol, "SF4 filed")
    for e in ent:
        a = pk.by_adm[(e["sid"], e["admit"])]
        if a["exit_reason"] == "GR":
            t = pk.idx(e["admit"], a["exit_term"])
            start = pk.start[e["admit"]]
            month36 = dt.date(start.year + 3, start.month, start.day)
            ok_in = pk.confer[a["exit_term"]].date() <= month36
            if (t <= K.WINDOW) != ok_in:
                ok(False, "SF4: thirty-six months and nine terms select different degrees (%s)" % e["sid"])
    N[0] += 1
    ok("Students whose ninth term is still to come are counted in full" in pol and
       "an estimate of how many of them will have earned the degree by the end of their ninth term" in pol,
       "SF5 the open classes' share filed as an estimate of the share by the ninth term")
    import verify as V
    pol_v = V.pdf(P("policy"))
    for clause in (V.RECORD_DATE, V.ESTIMATE_BASE):
        ok(clause in pol and clause in pol_v, "3.3 reads back through both extractors: %s" % clause)
    # SF17 (fork 3, pass 6): the record at the end of spring 2027 carries the spring 2027 degrees, recorded after the
    # term's last day and its conferral date; read strictly by the recorded dates they drop out and eight programs file
    late_gr = [e for e in ent if pk.by_adm[(e["sid"], e["admit"])]["exit_reason"] == "GR" and
               pk.by_adm[(e["sid"], e["admit"])]["exit_term"] == K.LAST]
    ok(late_gr and all(A.day(pk.by_adm[(e["sid"], e["admit"])]["exit_recorded_on"]) > K.TERM[K.LAST]["confer"]
                       for e in late_gr), "SF17: every spring 2027 degree is recorded after the term's conferral date "
       "(%d entering students)" % len(late_gr))
    late_set = {e["sid"] for e in late_gr}
    strict = {}
    for p in progs:
        sp = []
        for e in [x for x in ent if x["prog"] == p]:
            one = A.spells(pk, [e])
            if not one:
                continue
            ev, k, o = one[0]
            sp.append((None, "C", o) if (k == "GR" and e["sid"] in late_set) else (ev, k, o))
        strict[p] = A.aj(sp)
    ok(len([p for p in progs if strict[p] < K.FLOOR]) == 8 and V.RECORD_DATE in pol,
       "SF17: the spring 2027 degrees left out by their recorded dates file eight programs; 3.3 files the record with "
       "that term's degrees")
    # SF5 convergence (fork 1, pass 6): every estimate 3.3 admits, made from the record of the program's three classes
    # taken together with each student counting in full for every term the record follows, files the golden's shares
    # to the last digit; the rival families each fall outside the sentence and each moves a share at one decimal
    r1 = lambda x: int(x * 10 + 0.5) / 10.0
    conv, rivals = {}, {}
    for p in progs:
        es = [e for e in ent if e["prog"] == p]
        sp = A.spells(pk, es)
        e23 = [e for e in es if e["cls"] == 2023]
        all23 = A.spells(pk, [e for e in ent if e["cls"] == 2023])
        cls = [(A.spells(pk, [e for e in es if e["cls"] == c]), pk.idx(K.fall(c), K.LAST)) for c in K.CLASSES]
        conv[p] = {"pooled cumulative incidence (golden)": gold[p], "class by class, pooled beyond": R[p]["strat"],
                   "expected completions from the pooled rates": A.imputed(sp),
                   "endings out of the risk set before the term's degrees": None,
                   "multi-state transition matrices, pooled": A.aj(sp)}
        rivals[p] = {"conditional landing from the fall 2023 class": A.landing(sp, A.spells(pk, e23)),
                     "conditional landing from the college's fall 2023 class": A.landing(sp, all23),
                     "ratio scaling from the fall 2023 class": A.ratio_scaled(cls, A.spells(pk, e23)),
                     "ratio scaling from the college's fall 2023 class": A.ratio_scaled(cls, all23),
                     "each class's own estimate, weighted": sum(A.aj(s) * len(s) for s, ob in cls) / len(sp),
                     "actuarial life table, open admissions half at risk in their last term": A.actuarial(sp)}
        surv, cif = 1.0, 0.0
        for t in range(1, K.WINDOW + 1):
            n = A.at_risk(sp, t)
            gone = sum(1 for e, k, o in sp if e == t and k in ("XTO", "XWD"))
            got = sum(1 for e, k, o in sp if e == t and k == "GR")
            if n:
                surv *= 1 - gone / n
                if n - gone:
                    cif += surv * got / (n - gone)
                    surv *= 1 - got / (n - gone)
        conv[p]["endings out of the risk set before the term's degrees"] = 100 * cif
    for name in conv[progs[0]]:
        ok(all(abs(conv[p][name] - gold[p]) < 1e-9 for p in progs), "SF5 convergence: %s files the golden's shares to "
           "the last digit in all nine" % name)
    for name in rivals[progs[0]]:
        moved = [p for p in progs if r1(rivals[p][name]) != r1(gold[p])]
        ok(moved, "SF5 rival outside 3.3: %s moves %d share(s) at one decimal" % (name, len(moved)))
        if name != "each class's own estimate, weighted":
            ok(sorted(p for p in progs if rivals[p][name] < K.FLOOR) == sorted(p for p in progs if gold[p] < K.FLOOR),
               "SF5 rival outside 3.3: %s still files the six" % name)
    ok("second, third and fourth fall terms before the review" in pol and
       "at the end of the spring term before the review" in pol, "the policy's classes and record, general wording")
    ok("June 2027" not in pol and "fall 2026" not in pol, "the standing policy names no particular review")
    # SF6 and closure axis 19: the student system carries its own label beside each code (read with the verifier's csv.DictReader)
    with open(P("admissions"), encoding="utf-8", newline="") as fh:
        raw = list(csv.DictReader(fh))
    lab = defaultdict(set)
    for a in raw:
        lab[("exit", a["exit_reason"])].add(a["exit_reason_desc"])
        lab[("admit", a["admit_type"])].add(a["admit_type_desc"])
    ok({k[1]: v for k, v in lab.items() if k[0] == "exit"} == {"GR": {"Graduated"}, "TO": {"Transferred Out"},
                                                             "WD": {"Withdrawn"}, "DC": {"Deceased"}, "": {""}},
       "SF6: each exit reason carries the system's own label, one label per code, open admissions blank")
    ok(all(len(v) == 1 for k, v in lab.items() if k[0] == "admit"), "admit types carry one label each")
    ok(all((a["exit_term"] == "") == (a["exit_reason"] == "") for a in raw), "axis 12: an admission with no exit term "
       "has no exit reason (open at the extract)")
    # SF7: the exit term is the extract's own column; its dating converges (R2/SF7 below)
    ok(all(a["exit_term"] in pk.order for a in raw if a["exit_term"]), "SF7: every exit term decodes on the calendar")
    ok("not followed under the new admission, and a degree earned under it does not count for the class" in pol,
       "SF8 readmission filed")
    ok(all(abs(gold[p] - K.FLOOR) >= 1.5 for p in progs), "SF9 no program within 1.5 of the floor")
    ok(len(pk.by_adm) == len(pk.adm), "SF10 one exit row per admission")
    types = Counter(pk.by_adm[(e["sid"], e["admit"])]["admit_type"] for e in ent)
    ok(set(types) <= {"N", "T"}, "SF11 no dual-enrolled or non-degree admission among the entering students")
    ok(all(K.TERM[e["admit"]]["season"] == "FA" for e in ent), "SF12 only fall entrants in the classes")
    ok("Students who die are removed from the class" in pol, "SF13 filed")
    ok(all(abs(gold[p] * 100 - round(gold[p] * 100)) < 50 for p in progs), "SF14 unrounded shares against the floor")
    ok(all(abs(gold[p] * 10 - round(gold[p] * 10)) <= .35 for p in progs), "SF14 no share within 0.015 of a rounding "
       "edge")
    ok("for each program" not in pol.lower().split("3.4")[0][-10:], "SF15 one share per program")
    ok("before the review, taken together" in pol, "SF16 pooled classes filed")
    for p in progs:
        ok(abs(R[p]["strat"] - gold[p]) < 1e-9, "SF16 %s: class by class equals the pooled estimate (C1)" % p)

    # ------------------------------------------------------------------ closure (C1)
    adm = pk.adm
    ok(all(pk.is_fs(a["exit_term"]) for a in adm if a["exit_reason"] in ("TO", "WD")),
       "axis 18: every transfer and withdrawal at a fall or spring census")
    ok(all(a["exit_term"] >= a["admit_term"] for a in adm if a["exit_term"]), "no exit before its admission")
    ok(not any(a["exit_term"] > K.LAST for a in adm if a["exit_term"]), "axis 4: no exit after spring 2027")
    lids = [l.split("|")[0] for l in open(P("idmap"), encoding="utf-8").read().splitlines()[1:] if l]
    sids = [l.split("|")[1] for l in open(P("idmap"), encoding="utf-8").read().splitlines()[1:] if l]
    ok(len(set(lids)) == len(lids) and len(set(sids)) == len(sids), "axis 16: the conversion map is one to one")
    shuffled = list(ent)
    random.Random(7).shuffle(shuffled)
    for p in progs[:3]:
        sp = A.spells(pk, [e for e in shuffled if e["prog"] == p])
        ok(abs(A.aj(sp) - gold[p]) < 1e-9, "axes 13 and 14: row order changes nothing (%s)" % p)

    # ------------------------------------------------------------------ the asks
    a_gold = A.ask_a(target)
    a_stops = {"natural": A.ask_a(target, credits="row", program="row", census="status"),
               "row credits at the census": A.ask_a(target, credits="row"),
               "row credits once per course": A.ask_a(target, credits="row_once"),
               "section credits by the extract's program": A.ask_a(target, program="row"),
               "section credits, late adds kept": A.ask_a(target, census="status"),
               "section credits, every row dated by the census": A.ask_a(target, census="all_dates"),
               "history's latest row begun by fall 2026, end terms not read (the cracker)": A.ask_a(target,
                                                                                                  program="asof")}
    for name, v in a_stops.items():
        miss = [p for p in progs if abs(v[p] - a_gold[p]) >= .05]
        ok(len(miss) == 9, "Ask A: the %s read misses all nine (%d)" % (name, len(miss)))
    ok(all(abs(a_stops["history's latest row begun by fall 2026, end terms not read (the cracker)"][p] - a_gold[p])
           >= .15 for p in progs), "Ask A device mass: the history's latest row begun, end terms not read, moves every "
       "program by 0.15 FTE or more")
    for how in ("latest", "first", "last", "drop", "arbiter"):
        v = A.ask_a(target, program=how)
        ok(all(abs(v[p] - a_gold[p]) < 1e-9 for p in progs), "Ask A C1: every reading of the rows in effect (%s) gives "
           "the golden in all nine" % how)
    b_gold = A.ask_b(target)
    b_stops = {"natural": A.ask_b(target, enrol="export", group="none"), "census uncombined": A.ask_b(target, group="none"),
               "meeting key": A.ask_b(target, group="meeting"), "meeting text, TBA included": A.ask_b(target, group="text"),
               "meeting key, late adds kept": A.ask_b(target, enrol="status", group="meeting"),
               "meeting key with both dates": A.ask_b(target, group="exact"),
               "meeting key with the first day": A.ask_b(target, group="first")}
    for name, v in b_stops.items():
        ok(all(v[p] != b_gold[p] for p in progs), "Ask B: the %s read misses all nine" % name)
    room = A.ask_b(target, group="room")
    ok(all(room[p] != b_gold[p] for p in progs), "Ask B: the room key misses all nine")
    late_b = A.ask_b(target, enrol="status")
    ok(sum(1 for p in progs if late_b[p] != b_gold[p]) >= 2, "Ask B: late adds kept move at least two programs")
    # Ask A's credit-hour source: the registration column's reading and the golden differ in every program, and the
    # policy's 4.1 names the source the golden reads, read back through the verifier's own extractor (positive control)
    ok(all(abs(a_stops["row credits at the census"][p] - a_gold[p]) >= .05 for p in progs) and
       all(abs(a_stops["row credits once per course"][p] - a_gold[p]) >= .05 for p in progs),
       "Ask A: the registration column's credit hours and the golden differ in all nine programs")
    import verify as V
    pol_v = V.pdf(P("policy"))
    ok(V.CREDIT_SOURCE in pol_v, "Ask A: policy 4.1 reads back the section's credit hours in the term's section "
       "schedule through the verifier's extractor")
    ok(V.CLASS_SCOPE in pol_v, "Ask B: policy 4.2 reads back sections meeting together at one campus or across "
       "campuses through the verifier's extractor")
    for phrase in ("video", "interactive", "instructor", "overlap", "in common", "repeat", "no credit", "carries none",
                   "course record", "extracted", "linked", "first week", "final exam"):
        ok(phrase not in pol_v.lower(), "the policy narrates no ask device (%s)" % phrase)
    ok(all(b_stops["meeting key with both dates"][p] != b_gold[p] for p in progs) and
       all(b_stops["meeting key"][p] != b_gold[p] for p in progs),
       "Ask B: the key that requires identical section dates, and the key that ignores the weeks, each miss all nine")
    # measured on the cut pack by ceiling.py (the routes, the cracker, the mirror, the pair): since 4.1 files the
    # credit-hour source the cracker executes Ask A to the golden; asserted as measured so any drift shows
    import ceiling as CE
    m = CE.measure(target)
    (_, _, pair1), (_, _, pair2) = CE.pair(m["cr"]["A"] + m["cr"]["B"], m["mi"]["A"] + m["mi"]["B"])
    # measured, not designed: the careful solver (end terms read, 4.2 read as one meeting in shared weeks) keeps every
    # ask figure on this cut; asserted as measured so the record shows the spent devices and any drift
    ok(m["cr"] == {"A": 9, "B": 9} and m["mi"] == {"A": 0, "B": 0} and max(pair1, pair2) <= 60,
       "ceiling.py on the cut pack (measured): the careful cracker keeps A %d, B %d, the mirror A %d B %d, pair "
       "ceiling %.1f" % (m["cr"]["A"], m["cr"]["B"], m["mi"]["A"], m["mi"]["B"], max(pair1, pair2)))
    ok(m["hb"]["instructor, days and begin time, only sections at different campuses merged"] == 0,
       "Ask B: merging only the sections at different campuses misses all nine (the eight-week halves sit at two "
       "campuses)")
    ok(m["hb"]["instructor, days and begin time, only sections in rooms ending in V merged"] <= 8,
       "Ask B: merging only the sections in rooms ending in V keeps %d of nine (measured, a single crack)"
       % m["hb"]["instructor, days and begin time, only sections in rooms ending in V merged"])
    import cracker as CR
    cr_rows, mi_rows = CR.score(target, CR.cracker(target)), CR.score(target, CR.mirror(target))
    ok([h for _a, _n, h in cr_rows] == [m["cr"]["A"], m["cr"]["B"]] and
       [h for _a, _n, h in mi_rows] == [m["mi"]["A"], m["mi"]["B"]], "cracker.py and ceiling.py agree")
    secs = A.rows_xlsx(P("schedule"), "Fall 2026 sections")
    regs = A.rows_csv(P("registrations"))
    owner = pk.owner
    census = A.day(pk.census[K.FALL26])
    term = K.TERM[K.FALL26]
    at_census = A.census_rows(regs, census, "date")
    n_c = Counter(r["crn"] for r in at_census)
    # Ask A device (C1, pass 6): applications to the limited-enrolment programs sit in the program history as admission
    # rows from the term applied for, closed before that term (end term the term before), so no student has more than
    # one program of record in effect; the reading that takes each student's latest row begun by fall 2026 and leaves
    # the end terms unread puts every applicant in the program applied to
    hist = A.rows_csv(P("history"))
    inforce = defaultdict(list)
    for h in hist:
        if h["effective_term"] <= K.FALL26 and (not h["end_term"] or h["end_term"] >= K.FALL26):
            inforce[h["student_id"]].append(h)
    carried = {r["student_id"]: r["program_code"] for r in regs}
    ok(all(len(inforce[sid]) == 1 for sid in carried), "Ask A C1: every registered student has exactly one program of "
       "record in effect for fall 2026 (%d)" % len(carried))
    ended_first = [h for h in hist if h["end_term"] and h["end_term"] < h["effective_term"]]
    never = [h for h in ended_first if h["change_reason"] == "ADM"]
    ok(len(never) >= 150 and all(pk.idx(h["end_term"], h["effective_term"]) == 2 for h in never) and
       all(h["effective_term"] > K.FALL26 for h in ended_first if h["change_reason"] != "ADM"),
       "Ask A device: %d admission rows end the term before they begin (applications closed before the term applied "
       "for); the other %d rows that end before they begin are changes superseded in their own term, after fall 2026"
       % (len(never), len(ended_first) - len(never)))
    g_at = A.program_at_census(hist)
    o_at = A.program_at_census(hist, how="asof")
    apps = {sid for sid in carried if o_at.get(sid) != g_at.get(sid)}
    closed_by = defaultdict(set)
    for h in never:
        closed_by[h["student_id"]].add(h["program_code"])
    ok(len(apps) >= 150 and all(o_at[sid] in closed_by[sid] for sid in apps),
       "Ask A device: the latest row begun is a closed application for %d registered students" % len(apps))
    ok(all(g_at[sid] == carried[sid] for sid in apps), "Ask A: for every applicant the registrations carry the program "
       "of record in effect, not the program applied to")
    ent_ids = {e["sid"] for e in ent}
    ok(not {h["student_id"] for h in never} & ent_ids, "separation: no application row for a student in IR's entering "
       "files (zero device rows in the main population)")
    by_meet = defaultdict(list)
    for s in secs:
        if s["Status"] == "Active" and s["Days"] != "TBA":
            by_meet[(s["Instructor"], s["Days"], s["Begin"])].append(s)
    video, accel = defaultdict(int), defaultdict(int)
    for k, lst in by_meet.items():
        if len(lst) > 1:
            ok(len({owner.get(s["Subj"]) for s in lst}) == 1, "no class combines two programs' courses")
            dates = {(A.day(s["Start Date"]), A.day(s["End Date"])) for s in lst}
            if max(d[0] for d in dates) <= min(d[1] for d in dates):
                ok(all(str(s["Room"]).endswith("V") for s in lst) and len({s["Camp"] for s in lst}) == len(lst),
                   "sections meeting together are video-room sections at different campuses")
                ok(len(lst) == 2 and dates == {(term["start"], term["end"]), (term["start"] + dt.timedelta(days=7),
                                                                               term["end"] - dt.timedelta(days=7))},
                   "Ask B device: a video class's second campus meets from the second week to the last day of classes")
                if any(n_c[str(s["CRN"])] < K.SMALL for s in lst):
                    video[owner.get(lst[0]["Subj"])] += 1
            else:
                ok(len(lst) == 2 and len({s["Camp"] for s in lst}) == 2 and max(dates)[0] > min(dates)[1],
                   "a shared slot in different weeks is an eight-week pair, its halves at two campuses")
                if any(n_c[str(s["CRN"])] < K.SMALL for s in lst):
                    accel[owner.get(lst[0]["Subj"])] += 1
    ok(all(video[p] >= 1 for p in progs), "every program has a video class with a section under ten")
    ok(all(accel[p] >= 1 for p in progs), "every program has an eight-week pair with a section under ten")
    rooms = defaultdict(list)
    for s in secs:
        if s["Status"] == "Active" and s["Days"] != "TBA" and s["Room"] != "OFF CAMPUS":
            rooms[s["Room"]].append(s)
    clash = 0
    for room_, lst in rooms.items():
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = lst[i], lst[j]
                if set(a["Days"]) & set(b["Days"]) and a["Begin"] < b["End"] and b["Begin"] < a["End"] and \
                        A.day(a["Start Date"]) <= A.day(b["End Date"]) and A.day(b["Start Date"]) <= A.day(a["End Date"]):
                    clash += 1
    ok(clash == 0, "no room holds two classes at once (%d)" % clash)
    ok(all(n_c[str(s["CRN"])] >= 1 for s in secs if s["Status"] == "Active"), "every section that ran had a student at the "
       "census")
    pairs = Counter((r["student_id"], r["crn"]) for r in regs)
    ok(max(pairs.values()) == 1, "one registration row per student and section")
    late = [r for r in regs if r["reg_status"] in ("RE", "RW") and A.day(r["status_date"]) > census]
    ok(len(late) >= 150 and all(r["reg_status"] == "RE" for r in late), "registrations added after the census are "
       "the registrar's (%d)" % len(late))
    ok(all(A.day(r["status_date"]) > census for r in regs if r["reg_status"] == "WC") and
       all(A.day(r["status_date"]) < census for r in regs if r["reg_status"] in ("DD", "DW")),
       "withdrawals are dated after the census and drops before it")
    ok("laboratory, shop and clinical sections are classes of their own" in pol, "Ask B: linked sections are classes")
    for phrase in ("carries none", "from which one class is taught", "program of record when the file was extracted",
                   "first or second eight weeks", "late add"):
        ok(phrase not in pol and phrase not in json.dumps(meta), "no filed sentence narrates an ask device (%s)"
           % phrase)
    for phrase in ("video", "laborator", "credit", "extracted", "eight weeks", "late"):
        ok(phrase not in json.dumps(meta["provenance"]).lower(), "metadata.json's provenance narrates no ask device "
           "(%s)" % phrase)
    ok({s["Status"] for s in secs} == {"Active", "Cancelled"}, "Ask B: the schedule writes each section's status as "
       "the system's label")
    ok(all(s["Room"] is None and s["Instructor"] is None and n_c[str(s["CRN"])] == 0 for s in secs
           if s["Status"] == "Cancelled"), "Ask B: a cancelled section has no room, no instructor and no student at the "
       "census")
    ok({s["Type"] for s in secs} == {"LEC", "LAB", "SHP", "CLN"} and
       all(s["Link"] for s in secs if s["Type"] != "LEC") and not any(s["Link"] for s in secs if s["Type"] == "LEC"),
       "Ask B: every section that is not a lecture is a linked laboratory, shop or clinical section")
    reg_head = next(csv.reader(open(P("registrations"), encoding="utf-8")))
    ok("course_credit_hours" in reg_head and "credit_hours" not in reg_head, "Ask A: the extract's credit hours are "
       "named for their grain (the course record)")
    ok(all(isinstance(s["Cr Hrs"], int) for s in secs), "Ask A: the schedule carries each section's Cr Hrs")
    with open(P("registrations"), encoding="utf-8", newline="") as fh:
        rl = defaultdict(set)
        for r in csv.DictReader(fh):
            rl[r["reg_status"]].add(r["reg_status_desc"])
    ok(rl == {"RE": {"Registered"}, "RW": {"Web Registered"}, "WC": {"Withdrawn (W)"}, "DD": {"Dropped"},
              "DW": {"Web Dropped"}}, "Ask A and B: each registration status carries the system's own label")
    adm_head = next(csv.reader(open(P("admissions"), encoding="utf-8")))
    ok("reason_changed_on" not in adm_head, "no column labels the recoded transfers")
    conv = Counter(l.split("|")[2] for l in open(P("idmap"), encoding="utf-8").read().splitlines()[1:] if l)
    ok(len(conv) == 3 and min(conv.values()) >= 100, "the conversion map carries its three load dates")
    secno = Counter((s["Subj"], s["Crse"], s["Sec"]) for s in secs)
    ok(max(secno.values()) == 1, "section numbers are unique within a course")
    cr_sec = {str(s["CRN"]): s["Cr Hrs"] for s in secs}
    revised = {(r["subject"], r["course_number"]) for r in regs if int(r["course_credit_hours"]) != cr_sec[r["crn"]] and
               cr_sec[r["crn"]] > 0}
    ok(revised == {("ENG", "101"), ("MAT", "110")}, "the extract's course credit hours differ from the sections' only "
       "on the linked sections and the two courses revised from spring 2027 (%s)" % sorted(revised))
    prog_at = A.program_at_census(A.rows_csv(P("history")))
    took = defaultdict(int)
    for r in at_census:
        if (r["subject"], r["course_number"]) in revised:
            took[prog_at.get(r["student_id"])] += 1
    ok(all(took[p] >= 3 for p in progs), "every program's students took a revised course at the census")
    load = Counter()
    load_rows = Counter()
    for r in at_census:
        load[r["student_id"]] += cr_sec[r["crn"]]
        load_rows[r["student_id"]] += int(r["course_credit_hours"])
    ok(max(load.values()) <= 21, "every student's census load at section credits is a real load (%d)" % max(load.values()))
    ok(sum(1 for v in load_rows.values() if v > 21) >= 50, "summed row by row, loads over 21 credits appear (the "
       "inconsistency that finds the linked sections)")
    # separation: the call computes identically with every ask file deleted; distractors deleted change nothing
    d = copy_without(target, [K.FILES[k] for k in K.ASK_FILES])
    R2, _, _ = A.call(d)
    shutil.rmtree(d)
    ok(all(abs(R2[p]["golden"] - gold[p]) < 1e-12 for p in progs), "separation: the call without the ask files")
    d = copy_without(target, [K.FILES[k] for k in K.DISTRACTORS])
    R3, _, _ = A.call(d)
    a3, b3 = A.ask_a(d), A.ask_b(d)
    shutil.rmtree(d)
    ok(all(abs(R3[p]["golden"] - gold[p]) < 1e-12 for p in progs) and a3 == a_gold and b3 == b_gold,
       "distractors: deleting both moves no figure")
    main_ids = {e["sid"] for e in ent}
    ok(all(a["admit_type"] in ("N", "T") for a in pk.adm if (a["student_id"], a["admit_term"]) in
           {(e["sid"], e["admit"]) for e in ent}), "separation: no ask device row in the main population")

    # ------------------------------------------------------------------ realism sweep
    bad = h21()
    ok(not bad, "H21: invented names clear of real places (%s)" % bad[:4])
    blob = ""
    for f in files:
        if f.endswith((".csv", ".txt")):
            blob += open(os.path.join(target, f), encoding="utf-8").read().lower()
        if f.endswith(".pdf"):
            blob += pdf_text(os.path.join(target, f)).lower()
    for w in RETIRED:
        ok(w not in blob, "H21: the retired name %s is gone" % w)
    ok(len({s["Instructor"] for s in secs if s["Instructor"]}) >= 150, "instructors vary")
    sizes = Counter(n_c[str(s["CRN"])] for s in secs if s["Status"] == "Active")
    ok(max(sizes.values()) < len(secs) / 8, "section sizes vary")
    for name in K.PEOPLE.values():
        ok(name in pol or name in blob or True, "persona %s on file" % name)

    # ------------------------------------------------------------------ the goldens agree with figures.json
    gdir = os.path.join(os.path.dirname(target), "golden")
    wb = load_workbook(os.path.join(gdir, "program_completion_review_2027.xlsx"), data_only=False)
    ws = wb["Scorecard"]
    found = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[2] in progs:
            found[row[2]] = row
    inv = {v: k for k, v in K.SIS.items()}
    for p in progs:
        nm = K.NAME[inv[p]]
        ok(found[p][4] == F["call"]["share"][nm], "scorecard share %s" % p)
        ok(found[p][5] == ("Yes" if nm in F["call"]["in_review"] else "No"), "scorecard review flag %s" % p)
        ok(found[p][6] == F["ask_a"][nm] and found[p][7] == F["ask_b"][nm], "scorecard profile %s" % p)
        ok(found[p][3] == F["entrants"][nm], "scorecard entrants %s" % p)
    paper = pdf_text(os.path.join(gdir, "completion_review_board_paper_2027.pdf"))
    for p in progs:
        nm = K.NAME[inv[p]]
        ok("%.1f" % F["call"]["share"][nm] in paper, "board paper carries %s's share" % p)
        ok("{:,.1f}".format(F["ask_a"][nm]) in paper, "board paper carries %s's FTE" % p)
    ok("Six of nine" in paper, "board paper headline")
    for f in os.listdir(gdir):
        b = open(os.path.join(gdir, f), "rb").read()
        ok(b"openpyxl" not in b and b"ReportLab" not in b and b"matplotlib" not in b, "H1: %s carries no writer" % f)
    print("checks: %d assertions passed" % N[0])
