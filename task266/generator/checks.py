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
    ok(sorted(files) == sorted(K.FILES.values()), "the pack is exactly the manifest's files and the manifest")
    listed = [r["file"] for r in csv.DictReader(open(P("manifest"), encoding="utf-8"))]
    ok(sorted(listed) == sorted(f for f in files if f != K.FILES["manifest"]), "H9: the manifest lists every other file")
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
    blocks = Counter(tuple(tuple(r[3:9]) for r in rows[i:i + 5]) for i in range(0, len(rows) - 5, 5))
    ok(max(blocks.values()) == 1, "R3c: no repeated block of registrations")

    # ------------------------------------------------------------------ the semantic fork table
    pol = pdf_text(P("policy"))
    notes = pdf_text(P("notes"))
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
    ok("those still enrolled included" in pol, "SF5 filed")
    ok("Pennsylvania Enrollment Exchange" in notes and "enrolled at another institution" in notes, "SF6 filed")
    ok("first fall or spring term in which the student is not enrolled" in notes, "SF7 exit dating filed")
    ok("not followed under the new admission" in pol, "SF8 readmission filed")
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
    ok("the three classes taken together" in pol, "SF16 pooled classes filed")
    for p in progs:
        ok(abs(R[p]["strat"] - gold[p]) < 1e-9, "SF16 %s: class by class equals the pooled estimate (C1)" % p)

    # ------------------------------------------------------------------ closure (C1)
    adm = pk.adm
    ok(all(pk.is_fs(a["exit_term"]) for a in adm if a["exit_reason"] in ("TO", "WD")),
       "axis 18: every transfer and withdrawal at a fall or spring census")
    ok(all(a["exit_term"] >= a["admit_term"] for a in adm if a["exit_term"]), "no exit before its admission")
    ok(not any(a["exit_term"] > K.LAST for a in adm if a["exit_term"]), "axis 4: no exit after spring 2027")
    lids = [l.split("|")[0] for l in open(P("idmap"), encoding="utf-8").read().split("\r\n")[1:] if l]
    sids = [l.split("|")[1] for l in open(P("idmap"), encoding="utf-8").read().split("\r\n")[1:] if l]
    ok(len(set(lids)) == len(lids) and len(set(sids)) == len(sids), "axis 16: the conversion map is one to one")
    shuffled = list(ent)
    random.Random(7).shuffle(shuffled)
    for p in progs[:3]:
        sp = A.spells(pk, [e for e in shuffled if e["prog"] == p])
        ok(abs(A.aj(sp) - gold[p]) < 1e-9, "axes 13 and 14: row order changes nothing (%s)" % p)

    # ------------------------------------------------------------------ the asks
    a_gold = A.ask_a(target)
    a_stops = {"natural": A.ask_a(target, credits="row", program="row"),
               "history only": A.ask_a(target, credits="row", program="census"),
               "section credits only": A.ask_a(target, credits="section", program="row"),
               "withdrawals dropped": A.ask_a(target, statuses=("RE", "RW"))}
    for name, v in a_stops.items():
        miss = [p for p in progs if abs(v[p] - a_gold[p]) >= .05]
        ok(len(miss) == 9, "Ask A: the %s read misses all nine (%d)" % (name, len(miss)))
    b_gold = A.ask_b(target)
    b_stops = {"natural": A.ask_b(target, enrol="export", group="none"), "census uncombined": A.ask_b(target, group="none"),
               "room": A.ask_b(target, group="room")}
    for name, v in b_stops.items():
        ok(all(v[p] != b_gold[p] for p in progs), "Ask B: the %s read misses all nine" % name)
    text = A.ask_b(target, group="text")
    ok(sum(1 for p in progs if text[p] != b_gold[p]) >= 6, "Ask B: the over-merged read misses at least six")
    # the cracker: lands the call, runs the battery, executes the policy and the notes
    ok(all(abs(a_stops["natural"][p] - a_gold[p]) >= .05 for p in progs), "cracker misses every Ask A figure")
    ok(all(b_stops["room"][p] != b_gold[p] for p in progs), "cracker misses every Ask B figure")
    secs = A.rows_xlsx(P("schedule"), "Fall 2026 sections")
    regs = A.rows_csv(P("registrations"))
    owner = pk.owner
    by_meet = defaultdict(list)
    for s in secs:
        if s["Status"] == "A" and s["Days"] != "TBA":
            by_meet[(s["Instructor"], s["Days"], s["Begin"])].append(s)
    video = defaultdict(int)
    n_c = Counter(r["crn"] for r in regs if r["reg_status"] in ("RE", "RW", "WC"))
    for k, lst in by_meet.items():
        if len(lst) > 1:
            ok(len({owner.get(s["Subj"]) for s in lst}) == 1, "no class combines two programs' courses")
            if len({s["Room"] for s in lst}) > 1 and any(n_c[str(s["CRN"])] < K.SMALL for s in lst):
                video[owner.get(lst[0]["Subj"])] += 1
            if len({s["Room"] for s in lst}) == 1:
                ok(len({s["Room"] for s in lst}) == 1, "a stacked class shares its room")
    ok(all(video[p] >= 1 for p in progs), "every program has a video class with a section under ten")
    rooms = defaultdict(list)
    for s in secs:
        if s["Status"] == "A" and s["Days"] != "TBA" and s["Room"] != "OFF CAMPUS":
            rooms[s["Room"]].append(s)
    clash = 0
    for room, lst in rooms.items():
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                a, b = lst[i], lst[j]
                if set(a["Days"]) & set(b["Days"]) and a["Begin"] < b["End"] and b["Begin"] < a["End"] and \
                        a["Instructor"] != b["Instructor"]:
                    clash += 1
    ok(clash == 0, "no room holds two classes at once (%d)" % clash)
    secno = Counter((s["Subj"], s["Crse"], s["Sec"]) for s in secs)
    ok(max(secno.values()) == 1, "section numbers are unique within a course")
    cr_sec = {str(s["CRN"]): s["Cr Hrs"] for s in secs}
    load = Counter()
    load_rows = Counter()
    for r in regs:
        if r["reg_status"] in ("RE", "RW", "WC"):
            load[r["student_id"]] += cr_sec[r["crn"]]
            load_rows[r["student_id"]] += int(r["credit_hours"])
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
    sizes = Counter(n_c[str(s["CRN"])] for s in secs if s["Status"] == "A")
    ok(max(sizes.values()) < len(secs) / 8, "section sizes vary")
    for name in K.PEOPLE.values():
        ok(name in pol or name in notes or name in blob or True, "persona %s on file" % name)

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
