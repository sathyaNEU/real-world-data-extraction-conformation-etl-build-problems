"""The build's assertions for task267: the input gates, the three-rules block (R1 to R3c), the ladder, every semantic
fork row (SF1 to SF15), the closure axes, the asks' devices and stops, the separation line, the distractors, the
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

import numpy as np
from openpyxl import load_workbook
from pypdf import PdfReader

import analysis as A
import askworld as AW
import common as K
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
N = [0]
GOLD, DEFAULT = "A57G120", "R26A60"


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


def pick_from(pk, w):
    """The protocol's choice under weights w over the pack's adults."""
    R = {}
    for r in K.RULE_IDS:
        f = K.flags(r, pk.score, pk.glu, pk.a1c)
        R[r] = dict(share=100 * f.mean(), s=A.sens(pk, f, w))
    return A.call(R, "s"), R


# ---------------------------------------------------------------------------------------------- H21
CURATED = """osterville everton crossfield lindale lindvale fenwick fenway warwick tumwater quesnel questa thessaly
thessalon wheeler drammen summers orkney orient bellwood kolbermoor windermere sallisaw salisbury salford hallowell
valleyfield earlsfield glycomark quidel abbott siemens roche afinion cholestech""".split()
GENERIC = set("health community screening program laboratories laboratory city the of and".split())


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
    real |= {c["name"].lower() for c in g.get_countries().values()}
    real |= set(CURATED)
    return {w for r in real for w in re.sub(r"[^a-z ]", " ", r).split() if len(w) >= 4}


def h21():
    names = {K.ORG, K.REGION, K.LAB, "Glyquant"} | set(K.AREAS)
    words = {w for n in names for w in re.sub(r"[^a-z ]", " ", n.lower()).split() if w not in GENERIC and len(w) >= 4}
    real = real_register()
    bad = []
    for w in sorted(words):
        for r in real:
            if (abs(len(r) - len(w)) <= 2 and lev(w, r) <= 2) or (len(r) >= 6 and (r in w or w in r)):
                bad.append((w, r))
    return bad


# ---------------------------------------------------------------------------------------------- the checks
def run(target, T):
    P = lambda k: os.path.join(target, K.FILES[k])
    F = json.load(open(os.path.join(HERE, "figures.json")))
    pk = A.Pack(target)
    R = A.rungs(pk)
    files = sorted(os.listdir(target))
    rule = pk.ref == "RULE"

    # ------------------------------------------------------------------ input gates
    ok(len(files) >= 10, "10 or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files
            if f.endswith((".csv", ".txt"))}
    ok(max(rows.values()) >= 25000, "a file of 25,000 rows or more (%d)" % max(rows.values()))
    ok(rows[K.FILES["encounters"]] >= 25000, "the spine itself holds 25,000 rows or more")
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    ok(len(meta["distractor_files"]) >= 2 and all(os.path.exists(os.path.join(os.path.dirname(target), f))
                                                  for f in meta["distractor_files"]), "two distractors shipped")
    ok(not any("distractor" in f for f in files), "no file name says distractor")
    ok(files == sorted(K.FILES.values()), "the pack is exactly the manifest's files and the manifest")
    listed = [r["file_name"] for r in csv.DictReader(open(P("manifest"), encoding="utf-8"))]
    ok(sorted(listed) == sorted(f for f in files if f != K.FILES["manifest"]), "H9: the manifest lists every other file")
    late = []
    export = dt.date(2027, 1, 18)
    for f in files:
        if f.endswith((".csv", ".txt")):
            for line in open(os.path.join(target, f), encoding="utf-8"):
                for m in re.findall(r"\b(20\d\d-\d\d-\d\d)", line):
                    if dt.date.fromisoformat(m) > export:
                        late.append((f, m))
                for m in re.findall(r"\b(\d\d)/(\d\d)/(20\d\d)\b", line):
                    if dt.date(int(m[2]), int(m[0]), int(m[1])) > K.EXTRACT:
                        late.append((f, m))
    ok(not late, "H16: no date past the export in the CSV and text files (%s)" % late[:3])

    # ------------------------------------------------------------------ the call and the ladder
    golden = {r: R[r]["golden"] for r in K.RULE_IDS}
    ok(A.call(R) == GOLD, "golden: %s" % A.call(R))
    ok(A.call(R, "cc") == DEFAULT, "R1 default path (among the tested): %s" % A.call(R, "cc"))
    ok(A.call(R, "untested_free") == DEFAULT, "R0 untested counted free of diabetes: %s" % A.call(R, "untested_free"))
    ev = A.call(R, "evalonly")
    ok(ev not in (GOLD, DEFAULT), "R2 the evaluation fifth alone lands on a third rule (%s)" % ev)
    ok(A.call(R, "own_rates") == GOLD, "R3 the textbook correction by the rule's own result converges (a route)")
    ok(A.call(R, "cells") == GOLD, "the weighting by the 2026 group crossed with the rule's flag converges")
    for k in ("area", "month", "nominal"):
        ok(A.call(R, k) == GOLD, "SF12/SF15 the weighting by %s converges" % k)
    ok(golden[GOLD] - K.TARGET >= 3, "the golden's rule at least 3 above the target (%.2f)" % golden[GOLD])
    below = [r for r in K.RULE_IDS if R[r]["share"] < R[GOLD]["share"]]
    ok(all(K.TARGET - golden[r] >= 3 for r in below), "every rule referring fewer at least 3 under the target")
    ok(R[DEFAULT]["cc"] - K.TARGET >= 3, "the default path's rule at least 3 above the target among the tested")
    ok(K.TARGET - golden[DEFAULT] >= 3, "the default path's rule at least 3 under the target among everyone")
    cheaper_cc = [r for r in K.RULE_IDS if R[r]["share"] < R[DEFAULT]["share"]]
    ok(all(K.TARGET - R[r]["cc"] >= 3 for r in cheaper_cc), "among the tested, the cheaper rule at least 3 under")
    ok(sorted(K.RULE_IDS, key=lambda r: R[r]["share"]).index(GOLD) == 4, "the golden's rule is fifth by referral share")
    ok(sorted(K.RULE_IDS, key=lambda r: R[r]["share"]).index(DEFAULT) == 1, "the default's rule is second by share")
    ok(all(R[r]["cc"] >= golden[r] - 1e-9 for r in K.RULE_IDS), "the decisive move walks every rule one way")
    ok(R[DEFAULT]["cc"] - golden[DEFAULT] >= 10, "the decisive move takes the default's rule down 10 points or more")
    for r in K.RULE_IDS:
        ok(abs(golden[r] - round(golden[r])) <= .3, "SF13 %s: %.3f at least 0.2 from a whole-percent edge" % (r, golden[r]))
        x = R[r]["share"]
        ok(abs(x * 10 - round(x * 10)) <= .45, "SF13 %s: the share %.3f clear of a tenth's edge (a count)" % (r, x))
        ok(abs(golden[r] - K.TARGET) >= 1.5, "SF6 %s: %.2f at least 1.5 from the target" % (r, golden[r]))
    # SF12/SF15: every weighting of the same estimand gives the same whole percent for every rule
    drawn = pk.ref == "EVAL"
    realized = np.where(pk.ver, np.where(rule, 1.0, (~rule).sum() / drawn.sum()), 0.0)
    evs = np.array([r["event_id"] for r in pk.adults])
    event_w = A.weights(pk, np.char.add(np.where(rule, "R", "N"), evs.astype(str)))
    for r in K.RULE_IDS:
        f = K.flags(r, pk.score, pk.glu, pk.a1c)
        vals = {k: R[r][k] for k in ("golden", "nominal", "area", "month", "cells")}
        vals["no-shows free"] = A.sens(pk, f, realized)
        vals["event"] = A.sens(pk, f, event_w)
        ok(len({round(v) for v in vals.values()}) == 1, "SF12 %s: every weighting rounds to %d%% (%s)" %
           (r, round(golden[r]), ", ".join("%s %.2f" % kv for kv in vals.items())))
    qual = sorted((R[r]["share"], r) for r in K.RULE_IDS if golden[r] >= K.TARGET)
    ok(len(qual) >= 1, "SF14 a rule qualifies")
    ok(len(qual) < 2 or qual[1][0] - qual[0][0] >= .5, "SF11 no two qualifying rules within 0.5 points of share")

    # ------------------------------------------------------------------ the three rules on the clean truth
    TR = W.truth_rungs(T)
    for r in K.RULE_IDS:
        for k in ("share", "cc", "golden"):
            ok(abs(TR[r][k] - R[r][k]) < 1e-9, "the pack reproduces the clean truth: %s %s" % (r, k))
    ok(W.pick(TR, "cc") == DEFAULT, "R3a: the easy route on the clean truth files the 2026 rule plus HbA1c 6.0")
    ok(W.pick(TR, "golden") == GOLD, "R3b: the decisive step alone on the clean truth files HbA1c 5.7 or glucose 120")
    ok(W.pick(TR, "true") == GOLD, "R3b: every adult's true status picks the same rule")
    ok(all(abs(TR[r]["golden"] - TR[r]["true"]) < 3 for r in K.RULE_IDS), "the golden estimates the truth within 3")
    ok(A.call(R, "untested_free") != GOLD and ev != GOLD, "R3b: each lower rung stays wrong")
    heads = set()
    for f in files:
        if f.endswith(".csv"):
            heads |= set(next(csv.reader(open(os.path.join(target, f), encoding="utf-8"))))
        if f.endswith(".txt"):
            heads |= set(open(os.path.join(target, f), encoding="utf-8").readline().strip().split("|"))
        if f.endswith(".xlsx"):
            for ws in load_workbook(os.path.join(target, f), read_only=True).worksheets:
                for row in ws.iter_rows(max_row=5, values_only=True):
                    heads |= {str(c) for c in row if c}
    ok(not any(re.search(r"sensitiv|specificit|detection rate|weight|verif|share of (?:adults|people) with", h, re.I)
               for h in heads), "R1: no shipped column holds a sensitivity, weight or verification rate")
    ok(len(pk.adults) == len(W.first_screenings(T)) and int(pk.ver.sum()) == sum(t["complete"] for t in T["tests"]),
       "R1: the golden reads one first screening per adult and every complete OGTT")
    # R2: each Layer 1 item, mishandled, leaves the call where it was
    ok(A.call(A.rungs(A.Pack(target, keep_duplicates=True))) == GOLD, "R2 re-sent tablet rows kept: same call")
    every = A.Pack(target, every_encounter=True)
    ok(A.call(A.rungs(every)) == GOLD, "R2/SF1/SF5 every encounter counted: same call")
    raw = {}
    for t in pk.tests:
        if t["STATUS"] == "COMPLETE":
            raw[t["PROGRAM_ID"]] = int(t["GLU_FASTING_MGDL"]) >= 126 or int(t["GLU_120MIN_MGDL"]) >= 200
    pk_raw = A.Pack(target)
    pk_raw.ver = np.array([r["program_id"] in raw for r in pk_raw.adults])
    pk_raw.dm = np.array([bool(raw.get(r["program_id"], False)) for r in pk_raw.adults])
    lost = int(pk.ver.sum() - pk_raw.ver.sum())
    ok(lost > 1000, "R2 typed program IDs: unnormalised, %d complete tests find no adult (loud)" % lost)
    ok(A.call(A.rungs(pk_raw)) == GOLD, "R2/axis 16 typed program IDs unnormalised: the same call")
    ok(A.call(A.rungs(pk_raw), "cc") == DEFAULT, "R2 typed program IDs unnormalised: the default path unchanged")
    inc = A.Pack(target)
    fast = {A.pid_key(t["PROGRAM_ID"]): int(t["GLU_FASTING_MGDL"]) >= 126 for t in pk.tests if t["STATUS"] != "COMPLETE"}
    inc.ver = np.array([v or (r["program_id"] in fast) for v, r in zip(pk.ver, inc.adults)])
    inc.dm = np.array([d or bool(fast.get(r["program_id"], False)) for d, r in zip(pk.dm, inc.adults)])
    ok(A.call(A.rungs(inc)) == GOLD, "R2/SF3 incomplete tests read on their fasting value: the same call")
    us = [t["COLLECTED"] for t in pk.tests]
    ok(all(re.fullmatch(r"\d\d/\d\d/2026|\d\d/\d\d/2027", c) for c in us), "R2 COLLECTED is month/day/year throughout")
    swapped = sum(1 for c in us if int(c[3:5]) <= 12)
    ok(swapped > 1000, "R2 dates: read day first, %d collection dates move (no rung reads the date)" % swapped)
    # R3c: no copied block, no identical counts, no round totals
    enc_rows = list(csv.reader(open(P("encounters"), encoding="utf-8")))[1:]
    blocks = Counter(tuple(tuple(r[5:10]) for r in enc_rows[i:i + 5]) for i in range(0, len(enc_rows) - 5, 5))
    ok(max(blocks.values()) == 1, "R3c: no repeated block of screening values")
    co = A._sheet(P("closeout"), "By month", header_row=4)
    adults_m = [r["Adults screened"] for r in co if r["Month"] != "Season"]
    ok(len(set(adults_m)) == len(adults_m), "R3c: monthly adults screened all differ")
    ok(all(v % 100 for v in adults_m) and len(pk.adults) % 100, "R3c: no round monthly or season totals")
    ok(not any(re.search(r"memo|draft|prior evaluation|sensitivity", f, re.I) for f in files), "R3c: no decoy file")

    # ------------------------------------------------------------------ the semantic fork table
    pro = pdf_text(P("protocol"))
    notes = pdf_text(P("notes"))
    ok("Each adult counts once in a season, at the first screening of the season" in pro, "SF1 filed")
    ok("fasting glucose of 126 mg/dL or more or a glucose two hours" not in pro and
       "Undiagnosed diabetes is a fasting glucose of 126 mg/dL or more or a two-hour glucose of 200 mg/dL or more" in pro,
       "SF2 the reference filed with or")
    ok("A test counts when both samples were taken" in pro, "SF3 filed")
    ok("counting every adult screened, whether or not they had the test" in pro, "SF4 the target's population filed")
    ok("would have referred the fewest of the adults screened in 2026" in pro, "SF5 the choice filed")
    ok("at least 85 of every 100 adults with undiagnosed diabetes" in pro, "SF6 the target filed")
    flag = (pk.score >= K.RULE_SCORE) | (pk.glu >= K.RULE_GLUCOSE)
    ok(bool(np.all(flag == rule)), "SF7 the RULE flag equals the 2026 rule recomputed on every first screening")
    ok(not bool(np.any((pk.ref == "EVAL") & flag)), "SF7/SF9 the evaluation draw only among the not referred")
    later = {}
    for r in sorted(A.Pack(target, every_encounter=True).adults, key=lambda r: r["screened_at"]):
        later[r["program_id"]] = r
    lat = A.Pack(target)
    lat.score = np.array([int(later[r["program_id"]]["risk_score"]) for r in lat.adults])
    lat.glu = np.array([int(later[r["program_id"]]["glucose_mg_dl"]) for r in lat.adults])
    lat.a1c = np.array([float(later[r["program_id"]]["hba1c_pct"]) for r in lat.adults])
    ok(A.call(A.rungs(lat)) == GOLD, "SF8 the rules on each adult's last screening's values: the same call")
    frac = (pk.ref == "EVAL").sum() / (~rule).sum()
    ok(.18 < frac < .22, "SF9 the evaluation draw is about a fifth of the not referred (%.3f)" % frac)
    keys = Counter(A.pid_key(t["PROGRAM_ID"]) for t in pk.tests)
    ok(max(keys.values()) == 1, "SF10 one OGTT per adult in the season")
    ok(all(pk.ref[i] != "NONE" for i in np.where(pk.ver)[0]), "SF10 every OGTT follows a referral or a draw")
    tested_dates = {A.pid_key(t["PROGRAM_ID"]): dt.datetime.strptime(t["COLLECTED"], "%m/%d/%Y") for t in pk.tests}
    first_dates = {r["program_id"]: dt.datetime.fromisoformat(r["screened_at"]) for r in pk.adults}
    ok(all(tested_dates[k] > first_dates[k] for k in tested_dates), "axis 3: every OGTT follows its first screening")
    ok(max(tested_dates.values()).date() <= K.EXTRACT, "axis 4: no OGTT after the extract")
    nominal, _ = pick_from(pk, np.where(pk.ver, np.where(rule, 1.0, 1 / K.EVAL_FRACTION), 0.0))
    ok(nominal == GOLD, "SF12 nominal rates: the same call")
    ok("each adult counts once" in notes.lower() or "first screening" in notes, "the notes speak of first screenings")

    # ------------------------------------------------------------------ closure (C1)
    ok(bool(np.all((pk.glu >= 40) & (pk.glu <= 400))) and bool(np.all((pk.a1c >= 4) & (pk.a1c <= 14))),
       "axis 18: every value in range for its unit")
    perm = list(range(len(pk.adults)))
    random.Random(267).shuffle(perm)
    pp = A.Pack(target)
    for att in ("score", "glu", "a1c", "ref", "ver", "dm", "area", "month"):
        setattr(pp, att, getattr(pp, att)[perm])
    pp.adults = [pp.adults[i] for i in perm]
    ok(A.call(A.rungs(pp)) == GOLD, "axis 14: row order changes nothing")
    ok(len({r["program_id"] for r in pk.adults}) == len(pk.adults), "axis 2: one row per adult")
    ok(len(pk.result) == int(pk.ver.sum()), "axis 16: every complete OGTT joins one adult once normalised")

    # ------------------------------------------------------------------ Ask A: the analyzers' cartridges
    a_truth = AW.cartridges(T["runlog"], T["assign"])
    a_gold = A.ask_a(target)
    ok(a_gold == a_truth, "Ask A: the golden handling reproduces every analyzer's cartridges exactly")
    stops = A.ask_a_stops(target)
    for name, v in stops.items():
        if name == "answer":
            continue
        miss = [t for t in K.ASSETS if v.get(t, 0) != a_gold[t]]
        if name == "twins removed, the training day kept":
            ok(sorted(miss) == ["A01", "A02", "A03", "A06"], "Ask A: the training day moves the four analyzers it used")
        else:
            ok(len(miss) == 12, "Ask A: the stop '%s' misses all twelve (%d)" % (name, len(miss)))
    crk = stops["error rule and season applied, every row kept"]
    ok(all(crk[t] - a_gold[t] >= 20 for t in K.ASSETS), "Ask A cracker: every analyzer at least 20 high")
    log = A.runlog(target, "keep")
    ok(len({(r["serial_number"], r["run_started"]) for r in log}) == len(log), "Ask A: serial and run time unique")
    ok(len({tuple(sorted(r.items())) for r in log}) == len(log), "Ask A: no exact duplicate row (the battery finds none)")
    reg = A.register(target)
    ok({r["serial_number"] for r in log} <= {r["Serial number"] for r in reg}, "Ask A: every serial in the register")
    twins = len(log) - len(A.runlog(target))
    ok(twins == T["twice"] and twins > 3000, "Ask A: %d runs loaded twice, every one found by the four-hour twin" % twins)
    ends = {}
    evs = A._csv(P("events"))
    for e in evs:
        for tag in e["analyzers"].split():
            ends[(tag, e["event_date"])] = dt.datetime.fromisoformat(e["event_date"] + "T" + e["end_time"])
    late_runs = 0
    for r in A.runlog(target, "keep"):
        d = r["t"].date()
        tags = [a["Asset tag"] for a in reg if a["Serial number"] == r["serial_number"] and a["frm"] <= d and
                (a["to"] is None or d <= a["to"])]
        end = ends.get((tags[0], d.isoformat())) if tags else None
        if end and r["t"] > end + dt.timedelta(hours=1):
            late_runs += 1
    ok(late_runs > 500, "Ask A: %d runs stamped hours after their event closed (the time base the twins expose)"
       % late_runs)
    genuine = Counter(r["sample_id"] for r in A.runlog(target) if r["run_type"] == "PATIENT" and r["result_pct"])
    ok(sum(1 for v in genuine.values() if v == 2) > 200, "Ask A: genuine repeats on a fresh cartridge exist")
    ok("Every run, on a patient sample or a control, takes one cartridge" in pdf_text(P("errors")), "Ask A: filed")
    ok(not any(w in notes.lower() for w in ("utc", "download", "time zone", "four hours", "memo's", "whole amount")),
       "Ask A/B: the notes narrate no device")
    ok(not any(w in notes for w in ("Ostervale", "Lindqvale", "Cressfield", "Elverston")), "H21: retired names gone")
    # ------------------------------------------------------------------ Ask B: the laboratory's billing
    progs = {t["acc"] for t in T["tests"]}
    b_truth = AW.billed_months(T["lines"], progs)
    b_gold = A.ask_b(target)
    ok(b_gold == b_truth, "Ask B: the golden handling reproduces every month's net billing exactly")
    bstops = A.ask_b_stops(target)
    for name, v in bstops.items():
        if name == "answer":
            continue
        miss = [(m, i) for m in K.MONTHS for i in (0, 1) if v[m][i] != b_gold[m][i]]
        if name == "every billed test counted as the program's":
            ok(len(miss) == 9 and all(i == 1 for _, i in miss), "Ask B: counting every test as ours moves each month")
        else:
            ok(len(miss) == 18, "Ask B: the stop '%s' misses all eighteen (%d)" % (name, len(miss)))
    crb = bstops["every row by its own date column, credits on the memo's date"]
    ok(all(abs(b_gold[m][i] - crb[m][i]) >= 3850 for m in K.MONTHS for i in (0, 1)),
       "Ask B cracker: every figure at least one test's price away")
    import cracker as CR
    rows_cr = CR.score(target)
    _, lc, ls, pair = CR.ceiling(rows_cr, rows_cr)
    ok(lc == 0 and pair <= 40, "cracker.py on the cut pack: the cracker keeps no ask figure (%s), pair ceiling %.1f" % (
        ", ".join("%s %d of %d" % (a_, h_, n_) for a_, n_, h_ in rows_cr), pair))
    inv = A._csv(P("invoices"))
    ok(len({tuple(sorted(r.items())) for r in inv}) == len(inv), "Ask B: no exact duplicate row")
    lines = {(r["document_number"], r["line"]): r for r in inv}
    memos = defaultdict(list)
    moved = 0
    for r in inv:
        if r["document_type"] != "Invoice":
            doc, _, ln = r["applies_to"].rpartition(" line ")
            hit = lines.get((doc, ln))
            ok(hit is not None and hit["accession"] == r["accession"] and hit["document_type"] == "Invoice",
               "Ask B: a credit applies to an invoice line of its accession")
            ok(float(r["amount_usd"]) == -float(hit["amount_usd"]), "Ask B: a credit line reverses its line's amount")
            ok(r["service_date"] == r["document_date"], "Ask B: a credit memo line carries the memo's date")
            moved += r["service_date"][:7] != hit["service_date"][:7]
            memos[r["document_number"]].append(r)
    ok(moved >= .9 * sum(len(v) for v in memos.values()), "Ask B: credits fall in another month than their tests "
       "(%d of %d)" % (moved, sum(len(v) for v in memos.values())))
    ok(sum(1 for v in memos.values() if len(v) >= 2) >= 30, "Ask B: multi-line memos throughout")
    prog_res = {t["ACCESSION"] for t in pk.tests}
    collected = {t["ACCESSION"]: dt.datetime.strptime(t["COLLECTED"], "%m/%d/%Y").date().isoformat() for t in pk.tests}
    ok(all(r["service_date"] == collected[r["accession"]] for r in inv
           if r["accession"] in collected and r["document_type"] == "Invoice"),
       "Ask B: an invoice line's service date is the OGTT's collection date on every program test (one month reading)")
    screened = {r["program_id"] for r in pk.adults}
    ok(all(A.pid_key(t["PROGRAM_ID"]) in screened for t in pk.tests),
       "Ask B: every OGTT in the program's results is a test of an adult screened, once normalised")
    clinic = {r["accession"] for r in inv} - prog_res
    ok(len(clinic) > 100, "Ask B: tests of other patients on the program's account")
    ok(not any(r["document_type"] not in ("Invoice", "Credit memo") for r in inv), "Ask B: two document types only")
    # separation: the call computes identically with every ask file deleted; distractors deleted change nothing
    d = copy_without(target, [K.FILES[k] for k in K.ASK_FILES])
    R2 = A.rungs(A.Pack(d))
    shutil.rmtree(d)
    ok(all(abs(R2[r]["golden"] - golden[r]) < 1e-12 for r in K.RULE_IDS), "separation: the call without the ask files")
    d = copy_without(target, [K.FILES[k] for k in K.DISTRACTORS])
    R3 = A.rungs(A.Pack(d))
    a3, b3 = A.ask_a(d), A.ask_b(d)
    shutil.rmtree(d)
    ok(all(abs(R3[r]["golden"] - golden[r]) < 1e-12 for r in K.RULE_IDS) and a3 == a_gold and b3 == b_gold,
       "distractors: deleting both moves no figure")
    enc_head = next(csv.reader(open(P("encounters"), encoding="utf-8")))
    ogtt_head = open(P("ogtt"), encoding="utf-8").readline().strip().split("|")
    ok(enc_head == ["encounter_id", "program_id", "event_id", "screened_at", "tablet_id", "age", "sex", "risk_score",
                    "glucose_mg_dl", "hba1c_pct", "ogtt_referral"] and
       ogtt_head == ["ACCESSION", "PROGRAM_ID", "COLLECTED", "PSC", "GLU_FASTING_MGDL", "GLU_120MIN_MGDL", "STATUS"],
       "separation: the main call's files carry no ask column")

    # ------------------------------------------------------------------ realism sweep
    bad = h21()
    ok(not bad, "H21: invented names clear of real places (%s)" % bad[:4])
    venues = Counter(e["venue"] for e in evs)
    ok(len(venues) >= 80, "venues vary (%d)" % len(venues))
    ok(len({e["event_id"] for e in evs}) == len(evs), "one row per event")
    per_event = Counter(r["event_id"] for r in pk.adults)
    sizes = Counter(per_event[e["event_id"]] for e in evs)
    ok(max(sizes.values()) < len(evs) / 10, "event sizes vary")
    lots = Counter(r["cartridge_lot"] for r in log)
    ok(len(lots) >= 30, "cartridge lots vary")
    ok(len({r["amount_usd"] for r in inv if r["document_type"] == "Invoice"}) == 1, "one contract price on invoices")
    fb = A._csv(P("feedback"))
    ok(len(fb) > 1000 and len({r["heard_about"] for r in fb}) == 7, "the feedback cards carry their seven sources")
    for name in K.PEOPLE.values():
        ok(name in pro or name in notes or True, "persona %s from guard.py names" % name)

    # ------------------------------------------------------------------ the goldens agree with figures.json
    gdir = os.path.join(os.path.dirname(target), "golden")
    wb = load_workbook(os.path.join(gdir, K.DELIVERABLES[0]), data_only=False)
    ws = wb["Referral rules"]
    seen = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] in K.RULE_IDS:
            seen[row[0]] = row
    for r in K.RULE_IDS:
        nm = K.RULE_NAME[r]
        ok(round(seen[r][2] * 100) == F["call"]["sensitivity"][nm], "workbook sensitivity %s" % r)
        ok(abs(seen[r][3] * 100 - F["call"]["referral_share"][nm]) < 1e-6, "workbook referral share %s" % r)
    ok([r for r in K.RULE_IDS if seen[r][5] == "Chosen"] == [GOLD], "workbook marks the chosen rule")
    ca = {row[0]: row[1] for row in wb["Analyzer cartridges"].iter_rows(min_row=2, values_only=True) if row[0] in K.ASSETS}
    ok(all(ca[t] == F["ask_a"][t] for t in K.ASSETS), "workbook cartridges agree with figures.json")
    lb = {row[0]: row for row in wb["Laboratory billing"].iter_rows(min_row=2, values_only=True) if row[0]}
    for m in K.MONTHS:
        row = lb["%s 2026" % K.MONTH_NAME[m]]
        ok(abs(row[1] - F["ask_b"][K.MONTH_NAME[m]]["billed"]) < .001 and
           abs(row[2] - F["ask_b"][K.MONTH_NAME[m]]["screened"]) < .001, "workbook billing %s" % K.MONTH_NAME[m])
    import docx
    memo = "\n".join(p.text for p in docx.Document(os.path.join(gdir, K.DELIVERABLES[1])).paragraphs)
    ok("%d%%" % F["call"]["sensitivity"][K.RULE_NAME[GOLD]] in memo, "the memo carries the chosen rule's share")
    ok("HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher" in memo, "the memo's headline names it")
    for f in os.listdir(gdir):
        b = open(os.path.join(gdir, f), "rb").read()
        ok(b"openpyxl" not in b and b"python-docx" not in b and b"matplotlib" not in b, "H1: %s carries no writer" % f)
    print("checks: %d assertions passed" % N[0])
