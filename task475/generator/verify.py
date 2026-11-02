"""Independent verifier: reads only the shipped bundle (target/, golden/, figures.json), on its own code path, and
recomputes every graded figure. It shares no code with the generator.

    python3 task475/generator/verify.py
"""
import base64
import csv
import datetime as dt
import json
import os
import re
import sys
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def pdf_strings(path):
    raw = open(path, "rb").read()
    chunks = re.split(rb"endstream", raw)
    text = []
    for ch in chunks[:-1]:
        k = ch.rfind(b"stream")
        if k < 0:
            continue
        hdr, body = ch[:k], ch[k + 6:].strip()
        if b"ASCII85Decode" in hdr[-300:]:
            body = base64.a85decode(body.rstrip(b"~>").strip() if body.endswith(b"~>") else body, adobe=False)
        if b"FlateDecode" in hdr[-300:]:
            body = zlib.decompress(body)
        for lit in re.findall(rb"\(((?:\\\)|\\\(|\\\\|\\[0-7]{3}|[^()\\])*)\)\s*Tj", body):
            s = re.sub(rb"\\([0-7]{3})", lambda z: bytes([int(z.group(1), 8)]), lit)
            s = s.replace(b"\\(", b"(").replace(b"\\)", b")").replace(b"\\\\", b"\\")
            text.append(s.decode("latin-1"))
    return " ".join(text)


def letters(s):
    return re.sub(r"[^A-Z]", "", (s or "").upper())


def main():
    names = sorted(os.listdir(T))
    # every format read back, each with a positive control on the same code path
    regs = pdf_strings(os.path.join(T, "cae_examination_regulations_2026.pdf"))
    mins = pdf_strings(os.path.join(T, "examinations_committee_minutes_2026-06-18.pdf"))
    paper = pdf_strings(os.path.join(T, "cae_paper2_nov2026.pdf"))
    ok("PDF regulations read back (control: regulation 14.1 and Schedule 1)",
       "each counted once" in regs and "Clerical check, per script" in regs, "%d chars" % len(regs))
    ok("PDF minutes read back (control: the moves table)", "Move (marks)" in mins, "%d chars" % len(mins))
    ok("PDF question paper read back (control: the rubric)", "Answer any FIVE questions" in paper)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(T, "cae_candidates_may2026.xlsx"), read_only=True)
    may_reg = list(wb["Candidates"].iter_rows(values_only=True))
    ok("XLSX May register read back", may_reg[0][0] == "Cand No" and len(may_reg) > 500, "%d rows" % len(may_reg))
    req = json.load(open(os.path.join(T, "portal_requests_nov2026.json")))
    ok("JSON request log read back", req["count"] == len(req["requests"]) > 50, "%d requests" % req["count"])
    exp = rows("cae_marking_export_2026.csv")
    ok("CSV export read back", len(exp) >= 25000, "%d rows" % len(exp))

    # the main call: least squares with a dummy for every candidate and every question
    last = {}
    for r in exp:
        if r["series"] != "NOV26":
            continue
        q = int(r["item"][1:3]) - 1
        key = (r["candidate_no"], q, r["item"])
        if key not in last or r["entered_at"] > last[key][0]:
            last[key] = (r["entered_at"], 0 if r["mark"] == "-" else int(r["mark"]))
    qm = {}
    for (c, q, _i), (_t, v) in last.items():
        qm[(c, q)] = qm.get((c, q), 0) + v
    cands = sorted({c for c, _q in qm}, key=int)
    idx = {c: i for i, c in enumerate(cands)}
    obs = sorted(qm.items(), key=lambda kv: (int(kv[0][0]), kv[0][1]))
    n, nq = len(cands), 8
    X = np.zeros((len(obs), n + nq - 1))
    y = np.zeros(len(obs))
    for k, ((c, q), v) in enumerate(obs):
        X[k, idx[c]] = 1.0
        if q < nq - 1:
            X[k, n + q] = 1.0
        else:
            X[k, n:] = -1.0
        y[k] = v
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    eff = np.append(beta[n:], -beta[n:].sum())
    moves_raw = -eff
    moves = [int(np.floor(v + 0.5)) for v in moves_raw]
    ok("main call: moves by least squares with candidate and question dummies", moves == [-1, 1, 0, 1, 0, 3, -1, -3],
       "%s" % np.round(moves_raw, 3).tolist())
    ok("main call: no move within 0.3 of a rounding line under this fit",
       min(0.5 - abs(v - round(v)) for v in moves_raw) >= 0.3)
    totals = {}
    for (c, q), v in qm.items():
        totals[c] = totals.get(c, 0) + min(20, max(0, v + moves[q]))
    n_pass = sum(1 for v in totals.values() if v >= 50)
    ok("main call: sitters and passes", (len(cands), n_pass) == (714, 393), "%d sat, %d pass" % (len(cands), n_pass))
    means = np.zeros(8)
    for q in range(8):
        vs = [v for (c, qq), v in qm.items() if qq == q]
        means[q] = np.mean(vs)
    fac = [int(np.floor(v + 0.5)) for v in (means.mean() - means)]
    fac_pass = sum(1 for c in cands if sum(min(20, max(0, qm[(c, q)] + fac[q])) for q in range(8) if (c, q) in qm) >= 50)
    ok("ladder: the means rung files Q6 +1, Q8 -1 and 417 passes", fac[5] == 1 and fac[7] == -1 and fac_pass == 417,
       "%s %d" % (fac, fac_pass))

    # golden CSV read back and compared row by row
    gold = list(csv.DictReader(open(os.path.join(G, "nov2026_paper2_results.csv"), encoding="utf-8")))
    good = len(gold) == len(cands)
    for r in gold:
        c = r["candidate_no"]
        t = 0
        for q in range(8):
            cell = r["Q%d" % (q + 1)]
            if (c, q) in qm:
                want = min(20, max(0, qm[(c, q)] + moves[q]))
                good &= cell != "" and int(cell) == want
                t += want
            else:
                good &= cell == ""
        good &= int(r["total"]) == t and r["result"] == ("Pass" if t >= 50 else "Fail")
    ok("golden CSV: every row's counted marks, total and result recompute", good, "%d rows" % len(gold))

    # May back-test against the minutes
    mm = re.search(r"Move \(marks\)((?:\s*[+-]?\d+){8})", mins)
    may_mv = [int(x) for x in mm.group(1).split()]
    lastm = {}
    for r in exp:
        if r["series"] != "MAY26" or r["entered_at"][:10] > "2026-06-18":
            continue
        q = int(r["item"].split("(")[0]) - 1
        key = (r["candidate_no"], r["item"])
        if key not in lastm or r["entered_at"] > lastm[key][0]:
            lastm[key] = (r["entered_at"], q, 0 if r["mark"] == "-" else int(r["mark"]))
    mq = {}
    for (c, _i), (_t, q, v) in lastm.items():
        mq[(c, q)] = mq.get((c, q), 0) + v
    mmeans = np.array([np.mean([v for (c, qq), v in mq.items() if qq == q]) for q in range(8)])
    may_fac = [int(np.floor(v + 0.5)) for v in (mmeans.mean() - mmeans)]
    mt = {}
    for (c, q), v in mq.items():
        mt[c] = mt.get(c, 0) + min(20, max(0, v + may_mv[q]))
    ok("back-test: the May means reproduce the minutes' moves and 433 passes",
       may_fac == may_mv and sum(1 for v in mt.values() if v >= 50) == 433, "%s" % may_fac)

    # ask 1: centres
    nov_sat = {c for c in cands}
    regp2 = [r for r in rows("cae_entries_nov2026.csv") if r["paper"] == "P2"]

    def syd(s):
        t = dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
        return t + dt.timedelta(hours=11 if dt.datetime(2026, 10, 3, 16) <= t < dt.datetime(2027, 4, 3, 16) else 10)
    wreq = {}
    for q in req["requests"]:
        if q["type"] == "Withdrawal" and "P2" in q["papers"]:
            wreq.setdefault(q["applicant_id"], []).append(syd(q["submitted"]))
    cen = {}
    for r in regp2:
        c = r["centre_code"]
        cen.setdefault(c, [0, 0, 0])
        early = [t for t in wreq.get(r["applicant_id"], []) if t.date() < dt.date(2026, 11, 7)]
        if r["status"] == "Withdrawn" and early:
            cen[c][0] += 1
        elif r["candidate_no"] not in nov_sat:
            cen[c][1] += 1
    may_sat_cands = {r["candidate_no"] for r in exp if r["series"] == "MAY26"}
    mem, keys = set(), set()
    for row in may_reg[1:]:
        cand, name, dob, memno, _cen, papers, _ed, _st = row
        if "2" not in str(papers) or str(cand) not in may_sat_cands:
            continue
        fam, given = name.split(",", 1)
        if memno:
            mem.add(str(memno))
        keys.add((letters(fam), letters(given.split()[0]), dt.datetime.strptime(dob, "%d/%m/%Y").date().isoformat()))
    for r in regp2:
        if r["candidate_no"] in nov_sat:
            k = (letters(r["family_name"]), letters(r["given_names"].split()[0]), r["date_of_birth"])
            if (r["member_no"] and r["member_no"] in mem) or k in keys:
                cen[r["centre_code"]][2] += 1

    # ask 2: reviews
    sched = {}
    for label, key in (("Re-mark, per question named", "remark"), ("Clerical check, per script", "clerical")):
        i = regs.index(label)
        a, b = re.findall(r"\d+\.\d\d", regs[i:i + 100])[:2]
        sched[key] = (float(a), float(b))
    disc = {r["account_code"]: float(r["exam_services_discount_pct"]) for r in rows("corporate_accounts.csv")}
    fam_of = {str(row[0]): letters(row[1].split(",")[0]) for row in may_reg[1:]}

    def may_total(c, until):
        best = {}
        for r in exp:
            if r["series"] == "MAY26" and r["candidate_no"] == c and (until is None or r["entered_at"][:10] <= until):
                if r["item"] not in best or r["entered_at"] > best[r["item"]][0]:
                    best[r["item"]] = (r["entered_at"], 0 if r["mark"] == "-" else int(r["mark"]))
        per = {}
        for item, (_t, v) in best.items():
            q = int(item.split("(")[0]) - 1
            per[q] = per.get(q, 0) + v
        return sum(min(20, max(0, v + may_mv[q])) for q, v in per.items())
    changed, refund = 0, 0.0
    for r in rows("results_review_requests_2026.csv"):
        typed = r["candidate_no"]
        opts = [typed] + ["".join(s[:k] + [s[k + 1], s[k]] + s[k + 2:]) for s in [list(typed)]
                          for k in range(len(typed) - 1)]
        c = next((o for o in opts if fam_of.get(o) == letters(r["family_name"])), typed)
        rec = dt.datetime.strptime(r["received"], "%d/%m/%Y %H:%M")
        declined = rec.date() > dt.date(2026, 7, 21)
        ch = (not declined) and may_total(c, "2026-06-30") < 50 <= may_total(c, None)
        col = 0 if rec.date() < dt.date(2026, 7, 1) else 1
        nq = len([x for x in r["questions"].split(";") if x.strip()])
        fee = sched["remark"][col] * nq if r["service"] == "Re-mark" else sched["clerical"][col]
        paid = float(r["amount_aud"]) if r["payment"] == "Card" else round(fee * (1 - disc[r["account_code"]] / 100), 2)
        changed += ch
        refund += paid if (ch or declined) else 0.0

    f = json.load(open(os.path.join(HERE, "figures.json")))
    order = [("SYD", "Sydney"), ("WSY", "Western Sydney"), ("MEL", "Melbourne"), ("BNE", "Brisbane"),
             ("PER", "Perth"), ("ADL", "Adelaide")]
    ok("ask 1: every centre's withdrawals, absentees and May sitters match figures.json",
       all(cen[c] == [f["centres"][nm]["withdrawals"], f["centres"][nm]["absentees"], f["centres"][nm]["may_sitters"]]
           for c, nm in order), json.dumps(cen))
    ok("ask 2: May results changed and refund match figures.json",
       changed == f["reviews_changed"] and int(np.floor(refund + 0.5)) == f["refund_aud"],
       "%d, %.2f" % (changed, refund))
    ok("figures.json: moves and pass count", [f["moves"]["Q%d" % (j + 1)] for j in range(8)] == moves and
       f["passed"] == n_pass and f["sat"] == len(cands))

    # golden DOCX read back
    from docx import Document
    d = Document(os.path.join(G, "paper2_results_committee_paper.docx"))
    body = "\n".join(p.text for p in d.paragraphs)
    tabs = [[[c.text for c in r.cells] for r in t.rows] for t in d.tables]
    t1 = {r[0]: r[3] for r in tabs[0][1:]}
    t2 = {r[0]: [int(x) for x in r[1:]] for r in tabs[1][1:]}
    ok("DOCX read back: Table 1 moves", [int(t1["Q%d" % (j + 1)]) for j in range(8)] == moves)
    ok("DOCX read back: the recommendation's pass count", "%d of the %d candidates who sat" % (n_pass, len(cands)) in body)
    ok("DOCX read back: Table 2 by centre", all(t2[nm] == cen[c] for c, nm in order))
    ok("DOCX read back: the reviews paragraph", ("%d May results changed on review" % changed) in body and
       ("AUD {:,}".format(int(np.floor(refund + 0.5)))) in body)
    ok("DOCX read back: the chart is embedded", len(d.inline_shapes) == 1)

    for label, good, detail in OUT:
        print("%s  %s  %s" % ("PASS" if good else "FAIL", label, ("[" + detail[:150] + "]") if detail else ""))
    bad = sum(1 for _l, g, _d in OUT if not g)
    print("%d verifications, %d failed" % (len(OUT), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
