"""Generator checks, run on the installed pack (task475/target) and the generator's clean truth.

    python3 task475/generator/checks.py

Blocks: R (the three rules on the clean truth: R1 raw material, R2 mess neutrality per Layer 1 item, R3a the analyst
test, R3b the decisive step alone, R3c no plant), L (ladder, standing family, back-test, data-native evidence, cheap
routes), SF (every row of the semantic fork table), A (asks against the clean truth, the cracker's route, the
separation line), G (input gates), RS (realism sweep). Exit 1 on any failure."""
import copy
import csv
import datetime as dt
import glob
import json
import os
import re
import shutil
import sys
import tempfile
import warnings
import zipfile

import numpy as np

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import estimators as E  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

RESULTS = []
GOLD_MOVES = [-1, 1, 0, 1, 0, 3, -1, -3]


def flat(t):
    return re.sub(r"\s+", " ", t)


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), str(detail)))


def part_fit_moves(export_rows):
    cell = {}
    for r in export_rows:
        if r["series"] != "NOV26":
            continue
        q, k = A.question_of("NOV26", r["item"])
        cell[(r["candidate_no"], q, k)] = (0 if r["mark"] == "-" else int(r["mark"])) / float(r["max_mark"])
    cands = sorted({c for c, _q, _k in cell}, key=int)
    parts = sorted({(q, k) for _c, q, k in cell})
    ci = {c: i for i, c in enumerate(cands)}
    pi = {p: i for i, p in enumerate(parts)}
    m = np.full((len(cands), len(parts)), np.nan)
    for (c, q, k), v in cell.items():
        m[ci[c], pi[(q, k)]] = v
    a = np.nanmean(m, axis=1)
    d = np.zeros(len(parts))
    for _ in range(5000):
        dn = np.nanmean(m - a[:, None], axis=0)
        dn -= dn.mean()
        an = np.nanmean(m - dn[None, :], axis=1)
        if np.max(np.abs(dn - d)) < 1e-12:
            d, a = dn, an
            break
        d, a = dn, an
    am = a.mean()
    eq = np.array([sum(P.NOV_QUESTIONS[q][1][k] * (am + d[pi[(q, k)]]) for k in range(len(P.NOV_QUESTIONS[q][1])))
                   for q in range(8)])
    return eq.mean() - eq


def truth_asks(w):
    sitting = P.NOV_SITTING
    codes = P.CODES
    wd = {c: 0 for c in codes}
    ab = {c: 0 for c in codes}
    may = {c: 0 for c in codes}
    may_sat = {e["pid"] for e in w.may_sitters}
    for x in w.nov_entries:
        if "P2" not in x["papers"]:
            continue
        if x["withdrawn_at"] is not None and x["withdrawn_at"].date() < sitting:
            wd[x["centre"]] += 1
        elif not x["sat2"]:
            ab[x["centre"]] += 1
        if x["sat2"] and x["pid"] in may_sat:
            may[x["centre"]] += 1
    changed = sum(1 for r in w.may_reviews if r["changed"])
    refund = round(sum(r["paid"] for r in w.may_reviews if r["changed"] or r["declined"]), 2)
    return wd, ab, may, changed, refund


def text_files(target):
    out = {}
    for fn in sorted(os.listdir(target)):
        p = os.path.join(target, fn)
        if fn.endswith((".csv", ".json")):
            out[fn] = open(p, encoding="utf-8").read()
        elif fn.endswith(".pdf"):
            out[fn] = flat(A.pdf_text(p))
        elif fn.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(p, read_only=True)
            out[fn] = "\n".join("\t".join("" if v is None else str(v) for v in row)
                                for ws in wb.worksheets for row in ws.iter_rows(values_only=True))
    return out


def main():
    w = W.build()
    Pk, M, B, C, R = A.run(TARGET)
    m = M["m"]
    golden = M["golden"]
    exp = Pk.export
    nov_rows = [r for r in exp if r["series"] == "NOV26"]

    # ---------------- R1: the field's raw material ships
    per_answer = {}
    for r in nov_rows:
        q, _k = A.question_of("NOV26", r["item"])
        per_answer[(r["candidate_no"], q)] = per_answer.get((r["candidate_no"], q), 0) + 1
    check("R1a part marks per answer ship (every November answer carries 3 or 4 part rows)",
          min(per_answer.values()) >= 3 and set((~np.isnan(m)).sum(1)) <= {4, 5},
          "answers %d, parts per answer %d to %d" % (len(per_answer), min(per_answer.values()),
                                                       max(per_answer.values())))
    hdrs = []
    for fn in os.listdir(TARGET):
        if fn.endswith(".csv"):
            hdrs += next(csv.reader(open(os.path.join(TARGET, fn), encoding="utf-8")))
    reqkeys = set()
    for q in Pk.requests:
        reqkeys |= set(q)
    bad = [h for h in hdrs + sorted(reqkeys) if re.search(r"move|difficult|facility|adjust|scaled", h, re.I)]
    check("R1b no shipped column holds a question's difficulty or move", not bad, ", ".join(bad) or "none")
    check("R1c the November matrix read from the export is the clean truth's", np.array_equal(
        np.nan_to_num(m, nan=-1), np.nan_to_num(w.nov_m, nan=-1)), "%d x 8" % m.shape[0])

    # ---------------- R2: every Layer 1 item real and neutral on the call
    pm = part_fit_moves(exp)
    check("R2.1 part marks out of different maxima: a part-level fit summed to questions gives the golden moves",
          np.array_equal(np.rint(pm).astype(int), golden), np.round(pm, 2).tolist())
    qfmt = [r for r in exp if re.fullmatch(r"Q\d\d\.\d", r["item"])]
    check("R2.2 legacy item codes and component on the May rows: the November rows by item format are the rows by "
          "series", len(qfmt) == len(nov_rows) and all(r["series"] == "NOV26" for r in qfmt), "%d rows" % len(qfmt))
    k5 = (~np.isnan(m)).sum(1) == 5
    m5 = E.fe(m[k5])
    check("R2.3 candidates who answered four questions: leaving them out of the fit leaves the moves",
          np.array_equal(np.rint(m5).astype(int), golden), "%d four-answer candidates" % int((~k5).sum()))
    marks_skip = {}
    for r in nov_rows:
        if r["mark"] == "-":
            continue
        q, _k = A.question_of("NOV26", r["item"])
        marks_skip[(r["candidate_no"], q)] = marks_skip.get((r["candidate_no"], q), 0) + int(r["mark"])
    mo = A.marks_of_record(Pk, "NOV26")
    same = all(marks_skip.get((c, q), 0) == v for c, qs in mo.items() for q, v in qs.items())
    check("R2.4 no-response parts: reading '-' as nothing or dropping it gives the same question marks", same,
          "%d no-response parts" % sum(1 for r in nov_rows if r["mark"] == "-"))
    n_abs = sum(C[c]["absentees"] for c in C)
    mabs = np.vstack([m, np.full((n_abs, 8), np.nan)])
    check("R2.5 absentees in the register: adding them as candidates with no answers leaves the moves and the pass "
          "count", np.array_equal(np.rint(E.fe(mabs)).astype(int), golden) and E.passes(mabs, golden) == M["n_pass"],
          "%d absentees" % n_abs)

    class Bare:
        pass
    bare = Bare()
    bare.export = exp
    Mb = A.main_call(bare)
    check("R2.6 the register, the request log, the CRM, the ledger and the May register (centre rename, re-issued "
          "numbers, UTC stamps, legacy names) sit outside the call: it computes from the export alone",
          Mb["n_pass"] == M["n_pass"] and np.array_equal(Mb["golden"], golden), "export only")
    naive = {}
    for r in nov_rows:
        q, k = A.question_of("NOV26", r["item"])
        naive[(r["candidate_no"], q, k)] = r["mark"]
    check("R2.7 entered_at offsets (+10 in May, +11 in November): one mark per November part, so no ordering by "
          "time is needed", len(naive) == len(nov_rows), "%d parts" % len(naive))

    # ---------------- R3: the three rules on the clean truth
    fac_t = E.facility(w.nov_m)
    check("R3a analyst test: each question's mean among its answerers against the paper mean, every filed rule "
          "applied, files Q6 +1 and Q8 -1 and 417 passes on the clean truth",
          np.rint(fac_t[5]) == 1 and np.rint(fac_t[7]) == -1 and E.passes(w.nov_m, fac_t) == 417
          and E.passes(w.nov_m, fac_t) != M["n_pass"], np.round(fac_t, 2).tolist())
    fe_t = E.fe(w.nov_m)
    check("R3b decisive step alone: the same route with the fit of candidate and question in place of the means "
          "files the golden; no moves and the means each stay wrong",
          E.passes(w.nov_m, fe_t) == M["n_pass"] == 393 and E.passes(w.nov_m, np.zeros(8)) == 433,
          "%d / %d / %d" % (E.passes(w.nov_m, np.zeros(8)), E.passes(w.nov_m, fac_t), E.passes(w.nov_m, fe_t)))
    seen = set()
    dup = 0
    for r in exp:
        key = tuple(r.values())
        dup += key in seen
        seen.add(key)
    vecs = {}
    for r in nov_rows:
        vecs.setdefault(r["candidate_no"], []).append((r["item"], r["mark"]))
    vv = [tuple(sorted(v)) for v in vecs.values()]
    texts = text_files(TARGET)
    gm = " ".join("%+d" % x for x in GOLD_MOVES)
    nov_moves_shipped = any(("Q6" in t and "+3" in t and "November" in t and "move" in t.lower()) for fn, t in
                            texts.items() if fn.endswith(".pdf"))
    check("R3c no plant: no repeated export row, no copied mark block, no file stating a November move",
          dup == 0 and len(set(vv)) == len(vv) and not nov_moves_shipped, "dup rows %d" % dup)

    # ---------------- L: ladder, standing family, back-test, evidence, cheap routes
    pz = M["passes"]
    check("L1 rungs separate: unmoved 433, the means 417, the golden 393",
          (pz["R0 no moves"], pz["R1 facility"], pz["golden"]) == (433, 417, 393), str(pz))
    check("L2 golden moves Q1 -1, Q2 +1, Q3 0, Q4 +1, Q5 0, Q6 +3, Q7 -1, Q8 -3; the means differ at Q6 and Q8 only",
          golden.tolist() == GOLD_MOVES and [j for j in range(8) if M["rungs"]["R1 facility"][j] != golden[j]] == [5, 7],
          str(M["rungs"]["R1 facility"].tolist()))
    edges = {k: float(E.edge(v).min()) for k, v in M["family"].items()}
    check("L3 standing family: alternating means, least squares, one-step differences, the regression adjustment, "
          "the random intercept and the logit-scale fit each round to the golden, every value at least 0.15 from a "
          "rounding line", all(np.array_equal(np.rint(v).astype(int), golden) for v in M["family"].values())
          and min(edges.values()) >= 0.15, json.dumps({k: round(v, 3) for k, v in edges.items()}))
    check("L4 the means rung is stable (every value at least 0.1 from a rounding line)",
          E.edge(M["facility"]).min() >= 0.1, "%.3f" % E.edge(M["facility"]).min())
    check("L5 back-test: on the May marks at the committee's meeting the means and the fit both give the minutes' "
          "moves and its 433 passes of 698", np.array_equal(B["facility"], B["minutes"]) and
          np.array_equal(B["family"]["fe"], B["minutes"]) and B["pass_fac"] == B["pass_fe"] == 433 and
          B["minutes_pass"] == (433, 698), str(B["minutes"].tolist()))
    s6 = ~np.isnan(m[:, 5])
    s8 = ~np.isnan(m[:, 7])

    def oth(s, j):
        o = m[s].copy()
        o[:, j] = np.nan
        return float(np.nanmean(np.nanmean(o, axis=1)))
    g6 = oth(s6, 5) - float(np.nanmean(m[s6, 5]))
    g8 = float(np.nanmean(m[s8, 7])) - oth(s8, 7)
    check("L6 data-native evidence: Question 6's answerers score at least 3 marks less on it than on their other "
          "answers, Question 8's at least 3 more", g6 >= 3.0 and g8 >= 3.0, "%.2f / %.2f" % (g6, g8))
    pct = np.nanmean(m, axis=0) / 20.0
    cheap = {
        "unmoved": np.zeros(8),
        "means": E.facility(m),
        "means, answer-weighted average": (np.nansum(m, axis=0).sum() / (~np.isnan(m)).sum()) - np.nanmean(m, axis=0),
        "medians": np.nanmedian(np.nanmedian(m, axis=0)) - np.nanmedian(m, axis=0),
        "facility per cent": (pct.mean() - pct) * 20.0,
    }
    landing = [k for k, v in cheap.items() if E.passes(m, v) == M["n_pass"]]
    check("L7 Gate F: no cheap route that skips the comparison across the same candidates lands 393", not landing,
          json.dumps({k: E.passes(m, v) for k, v in cheap.items()}))

    # ---------------- SF: the semantic fork table
    rows = {r[0]: r for r in M["rows"]}
    ok1 = True
    for i, c in enumerate(M["cands"]):
        for q in range(8):
            if not np.isnan(m[i, q]):
                ok1 &= rows[c][1 + q] == int(min(20, max(0, m[i, q] + golden[q])))
    check("SF1 'moved': a whole-mark constant added to every answer to the question, held within 0 and 20", ok1)
    d = -E.fe(m)
    n = (~np.isnan(m)).sum(0)
    wmv = (n * d).sum() / n.sum() - d
    check("SF2 'the average of the optional questions, each counted once' against an answer-weighted average: same "
          "call", np.array_equal(np.rint(wmv).astype(int), golden) and E.passes(m, wmv) == M["n_pass"],
          np.round(wmv, 2).tolist())
    check("SF3 'the candidates who sat the paper': every candidate marked present (714), as regulation 2 defines; "
          "the golden reads all of them", M["n_sat"] == 714 and "every candidate marked present" in flat(Pk.regs_text),
          "714 sitters")
    trunc = np.trunc(M["family"]["fe"]).astype(int)
    check("SF4 'rounded to the nearest whole mark' against truncation: truncation files another call, and no "
          "standing value is within 0.15 of a rounding line", not np.array_equal(trunc, golden) and
          min(edges.values()) >= 0.15, str(trunc.tolist()))
    tot_nocap = np.nansum(np.where(np.isnan(m), np.nan, m + golden[None, :]), axis=1)
    check("SF5 the 0 to 20 limits of regulation 14.2: the pass count is 393 with or without them",
          int((tot_nocap >= 50).sum()) == M["n_pass"], "%d" % int((tot_nocap >= 50).sum()))
    tot = np.nansum(E.apply_moves(m, golden), axis=1)
    check("SF6 '50 or more': regulation 12's sentence is shipped; 'more than 50' would file another count",
          "total of 50 or more" in flat(Pk.regs_text) and int((tot > 50).sum()) != M["n_pass"], "%d" % int((tot > 50).sum()))
    keys = [(r["candidate_no"], r["item"]) for r in nov_rows]
    check("SF7 the mark of record (regulation 11.2): one November row per candidate and part", len(set(keys)) == len(keys))
    check("SF8 a no-response part counts nothing whether read as 0 or skipped (R2.4)", same)
    check("SF9 four-answer candidates are in the results and their exclusion from the fit moves nothing",
          np.array_equal(np.rint(m5).astype(int), golden) and len(M["rows"]) == M["n_sat"])
    check("SF10 the move is per question (regulation 14.1); a part-level fit summed to questions is the same call",
          np.array_equal(np.rint(pm).astype(int), golden))
    csv_ok = all(r[9] == sum(v for v in r[1:9] if v != "") and r[10] == ("Pass" if r[9] >= 50 else "Fail")
                 for r in M["rows"])
    check("SF11 the mark counted is the moved, held mark; the total and result follow from it", csv_ok)
    check("SF12 the November paper's rows are the NOV26 series (R2.2)", len(qfmt) == len(nov_rows))
    check("SF13 the total sums the counted marks over the questions answered", csv_ok)
    wr = A.withdrawal_requests(Pk)
    utc_count = sum(1 for r in Pk.nov_reg if r["paper"] == "P2" and r["status"] == "Withdrawn" and
                    any(q["applicant_id"] == r["applicant_id"] and q["type"] == "Withdrawal" and "P2" in q["papers"]
                        and q["submitted"][:10] < "2026-11-07" for q in Pk.requests))
    check("SF14 a withdrawal is dated by the request's receipt in Sydney time (regulations 17.1 and 20), not the "
          "day it was actioned or the UTC date", "has effect from the time the request is received" in flat(Pk.regs_text)
          and "Sydney time" in flat(Pk.regs_text), "UTC dating would give %d, Sydney %d" %
          (utc_count, sum(C[c]["withdrawals"] for c in C)))
    sat = A.nov_sat(Pk)
    day = [q for q in Pk.requests if q["type"] == "Withdrawal" and "P2" in q["papers"] and
           A.utc_to_sydney(q["submitted"]).date() >= A.SITTING]
    day_apps = {q["applicant_id"] for q in day}
    day_rows = [r for r in Pk.nov_reg if r["paper"] == "P2" and r["applicant_id"] in day_apps]
    check("SF15 'absent' (regulation 17.3): requests received on the day leave the entry live and its candidate "
          "absent", day_rows and all(r["candidate_no"] not in sat for r in day_rows), "%d such requests" % len(day))
    tr_ok = True
    last_to = {}
    for q in sorted(Pk.requests, key=lambda q: q["submitted"]):
        if q["type"] == "Centre transfer":
            last_to[q["applicant_id"]] = q["detail"].split(" to ")[1]
    for r in Pk.nov_reg:
        if r["applicant_id"] in last_to:
            tr_ok &= r["centre_code"] == last_to[r["applicant_id"]]
    check("SF16 a candidate is counted at the entry's centre after any transfer (regulation 18)", tr_ok,
          "%d transfers" % len(last_to))
    may_entered = A.may_people(Pk, "register")
    may_sat_p = A.may_people(Pk, "golden")
    check("SF17 'had sat Paper 2 in May' is marked present (MAY26 marks), not entered", len(may_entered) > len(may_sat_p),
          "%d entered and not withdrawn, %d sat" % (len(may_entered), len(may_sat_p)))
    mem = [x["member"] for x in may_sat_p if x["member"]]
    kk = [x["key"] for x in may_sat_p]
    check("SF18 identity across sittings is unique: no two May sitters share a member number or a name key",
          len(mem) == len(set(mem)) and len(kk) == len(set(kk)))
    check("SF19 May results as issued use the marks of record on 30 June (regulation 16), after review all marks, "
          "both with the minutes' moves (regulation 19.2)", "issued on the marks of record on that date" in flat(Pk.regs_text)
          and "does not change the moves approved" in flat(Pk.regs_text))
    alloc = A.invoice_allocation(Pk)
    ok20 = all(abs(dd["paid"] - alloc[dd["request"]]) < 0.005 for dd in R["detail"] if dd["request"] in alloc)
    check("SF20 the fee paid on an account is the agreed rate, equal to the request's share of its invoice to the "
          "cent; declined requests are those received after 21 July", ok20 and len(alloc) > 0,
          "%d account requests" % len(alloc))
    cents = R["refund"] - int(R["refund"])
    check("SF21 the refund to the nearest dollar is clear of the half dollar", abs(cents - 0.5) >= 0.1, "%.2f" % R["refund"])

    # ---------------- A: asks against the clean truth, the cracker, the separation line
    wd, ab, may, changed, refund = truth_asks(w)
    ok_a = all(C[c]["withdrawals"] == wd[c] and C[c]["absentees"] == ab[c] and C[c]["may_sitters"] == may[c]
               for c in P.CODES)
    check("A1 every centre's withdrawals, absentees and May sitters recompute the clean truth", ok_a,
          json.dumps(C))
    check("A2 the May reviews recompute the clean truth (results changed, refund)",
          R["changed"] == changed and abs(R["refund"] - refund) < 0.005, "%d, %.2f" % (R["changed"], R["refund"]))
    Cc = A.ask_centres(Pk, "cracker")
    Rc = A.ask_reviews(Pk, "cracker")
    miss = [c + " " + k for c in P.CODES for k in ("withdrawals", "absentees", "may_sitters") if Cc[c][k] == C[c][k]]
    check("A3 the careful route (register dates, register entrants, number-only joins, schedule fees) misses every "
          "ask figure", not miss and Rc["changed"] != R["changed"] and round(Rc["refund"]) != round(R["refund"]),
          ", ".join(miss) or "all 20 missed")
    lag = {c: 0 for c in P.CODES}
    for r in Pk.nov_reg:
        if r["paper"] == "P2" and r["status"] == "Withdrawn":
            t = wr.get(r["applicant_id"])
            if t is not None and t.date() < A.SITTING <= dt.date.fromisoformat(r["status_changed"]):
                lag[r["centre_code"]] += 1
    check("A4 device mass: every centre holds a withdrawal received before the sitting and actioned after it",
          all(v >= 1 for v in lag.values()), json.dumps(lag))
    dev_rows = sum(1 for r in nov_rows if r["candidate_no"] in {x["candidate_no"] for x in Pk.nov_reg
                                                                  if x["status"] == "Withdrawn" and x["paper"] == "P2"})
    check("A5 separation: no withdrawn entry carries a November mark, and the call reads no ask file (R2.6)",
          dev_rows == 0, "%d" % dev_rows)

    # ---------------- G: input gates
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    check("G2 three or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
    check("G3 a file of 25,000 or more rows", len(exp) >= 25000, "%d export rows" % len(exp))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("G4 two or more distractors named in metadata.json, none named so in target/",
          len(meta["distractor_files"]) >= 2 and not any("distract" in f.lower() for f in files),
          ", ".join(meta["distractor_files"]))
    sheets = []
    import openpyxl
    for f in files:
        if f.endswith(".xlsx"):
            sheets += openpyxl.load_workbook(os.path.join(TARGET, f), read_only=True).sheetnames
    bad = [x for x in files + sheets if re.search(r"readme|dictionar|notes|manifest|field.?guide|schema", x, re.I)]
    check("G5 no file or sheet describes the data", not bad, ", ".join(bad) or "none")
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in meta["distractor_files"]:
            shutil.copy(os.path.join(TARGET, f), tmp)
    _p2, M2, _b2, C2, R2 = A.run(tmp)
    shutil.rmtree(tmp)
    check("G6 deleting the distractors changes no golden or ask figure", M2["n_pass"] == M["n_pass"] and C2 == C and
          R2["changed"] == R["changed"] and R2["refund"] == R["refund"])

    # ---------------- RS: realism sweep
    def const_step(vals):
        v = sorted(set(vals))
        dd = {b - a for a, b in zip(v, v[1:])}
        return len(dd) == 1
    idcols = {
        "candidate numbers (November)": [int(r["candidate_no"]) for r in Pk.nov_reg if r["candidate_no"]],
        "entry refs": [int(r["entry_ref"][4:]) for r in Pk.nov_reg],
        "request ids": [int(q["request_id"][3:]) for q in Pk.requests],
        "review request numbers": [int(r["request_no"][5:]) for r in Pk.reviews],
        "invoice numbers": [int(r["invoice_no"][4:]) for r in Pk.invoices],
    }
    check("RS1 no id column is an arithmetic sequence", not any(const_step(v) for v in idcols.values()),
          ", ".join(k for k, v in idcols.items() if const_step(v)) or "none")
    names = [c[1] for c in P.CENTRES]
    check("RS2 centre codes are not in alphabetical order of their names", names != sorted(names))
    shapes = {re.sub(r"^.*?\b(Pty Ltd|Group|Services|Consultants|Certifiers|Approvals|Partners|Certification)$",
                     r"\1", a["account_name"]) for a in Pk.accounts}
    check("RS3 account names take more than two shapes", len(shapes) > 2, "%d shapes" % len(shapes))
    periodic = False
    for q in range(8):
        seq = [r["marker"] for r in nov_rows if r["item"] == "Q%02d.1" % (q + 1)]
        for per in range(2, 9):
            if all(seq[i] == seq[i % per] for i in range(len(seq))):
                periodic = True
    check("RS4 no marker is dealt round-robin", not periodic)
    stamps = []
    for f in files:
        if f.endswith(".pdf"):
            mm = re.search(rb"/CreationDate \(D:(\d{8})", open(os.path.join(TARGET, f), "rb").read())
            stamps.append(dt.datetime.strptime(mm.group(1).decode(), "%Y%m%d").date())
    late = [r for r in exp if A.entered(r).date() > P.EXPORT_DAY]
    late += [q for q in Pk.requests if q["submitted"][:10] > P.EXPORT_DAY.isoformat()]
    late += [r for r in Pk.nov_reg if r["entered_on"] > P.EXPORT_DAY.isoformat()]
    late += [r for r in Pk.invoices if r["issue_date"] > P.EXPORT_DAY.isoformat()]
    check("RS5 no document dated after the as-of day and no extract carrying a date after its pull",
          all(s <= P.ASOF for s in stamps) and not late, "pdf dates %s" % [s.isoformat() for s in stamps])
    check("RS6 no round headline figure", M["n_sat"] % 10 and M["n_pass"] % 10 and round(R["refund"]) % 10,
          "%d, %d, %d" % (M["n_sat"], M["n_pass"], round(R["refund"])))
    for k in ("withdrawals", "absentees", "may_sitters"):
        vals = [C[c][k] for c in P.CODES]
        check("RS7 %s are not identical across centres" % k, len(set(vals)) > 1, str(vals))
    cand_names = {(A.norm(r["family_name"]), A.norm(r["given_names"].split()[0])) for r in Pk.nov_reg}
    cand_names |= {(A.norm(r["Candidate Name"].split(",")[0]), A.norm(r["Candidate Name"].split(",")[1].split()[0]))
                   for r in Pk.may_reg}
    persona = {(A.norm(v.split()[1]), A.norm(v.split()[0])) for v in P.PEOPLE.values()}
    check("RS8 the personas (guard.py names) are not candidates and appear in the minutes",
          not (persona & cand_names) and all(v in flat(Pk.minutes_text) for v in P.PEOPLE.values()))
    sig = []
    for f in files:
        b = open(os.path.join(TARGET, f), "rb").read()
        blobs = [b]
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(TARGET, f)) as z:
                blobs = [z.read(n) for n in z.namelist()]
        for blob in blobs:
            for s in (b"ReportLab", b"reportlab", b"openpyxl", b"python-docx", b"matplotlib"):
                if s in blob:
                    sig.append("%s:%s" % (f, s.decode()))
    check("RS9 containers scrubbed of the writers' signatures", not sig, ", ".join(sig) or "none")
    hits14 = [fn for fn, t in texts.items() if "each counted once" in t]
    hits_close = [fn for fn, t in texts.items() if "21 July 2026" in t]
    hits_mv = [fn for fn, t in texts.items() if "Move (marks)" in t]
    check("RS10 each load-bearing fact sits in one file (regulation 14.1, the review closing date, May's moves)",
          hits14 == [P.FILES["regs"]] and hits_close == [P.FILES["minutes"]] and hits_mv == [P.FILES["minutes"]],
          "%s %s %s" % (hits14, hits_close, hits_mv))
    ctrl = {P.FILES["regs"]: "rounded to the nearest whole mark", P.FILES["paper"]: "Answer any FIVE questions",
            P.FILES["minutes"]: "subject to the borderline review"}
    check("RS11 every PDF reads back through the extractor, with a known sentence found (positive control)",
          all(len(texts[f]) > 500 and s in texts[f] for f, s in ctrl.items()), "3 PDFs")
    det = [q["detail"] for q in Pk.requests if q["detail"]]
    top = max(det.count(x) for x in set(det)) / float(len(det))
    check("RS12 no free text recurs beyond a real rate in the request log", top < 0.6, "%.2f" % top)

    width = max(len(l) for l, _o, _d in RESULTS)
    fails = 0
    for label, ok, detail in RESULTS:
        fails += not ok
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", label[:150], ("[" + detail[:160] + "]") if detail else ""))
    print("%d checks, %d failed" % (len(RESULTS), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
