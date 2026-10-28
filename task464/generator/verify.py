"""task464 architecture 8: the independent verifier.

Reads only the shipped bundle under target/ and the goldens, on its own code path: no generator module is
imported, the parsers are its own, the PDFs are read back with pypdf (checks.py uses pdftotext), and the
cutover links are rebuilt from the learners' own moves between terms rather than from the catalogue match
answers.py uses. Every graded figure is recomputed and compared with figures.json and with the goldens.
"""
import collections, csv, json, os, sys
import numpy as np
from pypdf import PdfReader
import openpyxl

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(BASE, "target")
G = os.path.join(BASE, "golden")
FAIL, N = [], [0]


def ck(name, ok, detail=""):
    N[0] += 1
    if not ok:
        FAIL.append("%s: %s" % (name, detail))


def rd(name):
    return list(csv.DictReader(open(os.path.join(T, name), encoding="utf-8")))


def pdf(name):
    return " ".join((p.extract_text() or "") for p in PdfReader(os.path.join(T, name)).pages).replace("\n", " ")


def main():
    fig = json.load(open(os.path.join(BASE, "generator", "figures.json")))
    codes = [r["reason_code"] for r in sorted(rd("reason_code_list.csv"), key=lambda r: int(r["manual_order"]))]

    # ---- every format read back -------------------------------------------------------
    a = rd("withdrawals_autumn_winter_2025.csv")
    js = json.load(open(os.path.join(T, "withdrawals_spring_summer_2026.json"), encoding="utf-8"))
    mod = rd("coding_moderation_2025_26.csv")
    tor, qa, man = (pdf("withdrawal_review_terms_of_reference.pdf"), pdf("quality_assurance_procedure.pdf"),
                    pdf("coding_manual_2025.pdf"))
    ck("pdf: the terms of reference file the estimand", "happened for that reason" in tor)
    ck("pdf: the terms of reference scope the four terms", "four terms" in tor)
    ck("pdf: the quality procedure states the draw",
       "Every withdrawal coded OT is moderated" in qa and "400 withdrawals" in qa, qa[:200])
    ck("pdf: the quality procedure carries no substitution rule", "stands as" not in qa)
    ck("pdf: the manual lists the six codes", all(c in man for c in codes))
    for x in ("learner_satisfaction_2025_26.xlsx", "retention_budget_2027_lines.xlsx"):
        wb = openpyxl.load_workbook(os.path.join(T, x))
        ck("xlsx: %s reads back" % x, len(wb.sheetnames) >= 1)

    # ---- the call ---------------------------------------------------------------------
    labels = sorted({r["term"] for r in a}, key=lambda l: min(r["withdrawal_date"] for r in a if r["term"] == l))
    tmap = dict(zip(labels, ["T1", "T2"]))
    recs = {}
    for r in a:
        recs.setdefault(r["withdrawal_ref"], (tmap[r["term"]], r["reason_code"].strip().upper()))
    for r in js["records"]:
        recs.setdefault(r["withdrawalRef"], (r["termCode"], r["exitReasonCode"].strip().upper()))
    n = len(recs)
    ck("call: every withdrawal carries one of the six codes", all(c in codes for _, c in recs.values()))
    cnt = collections.Counter(c for _, c in recs.values())
    q = np.array([cnt[c] / n for c in codes])
    strata = {c: collections.Counter(m["moderated_reason"] for m in mod if m["coded_reason"] == c) for c in codes}
    Rm = np.array([[strata[i][j] / sum(strata[i].values()) for i in codes] for j in codes])   # R[j, i]
    p = Rm @ q
    order = np.argsort(-p)
    ck("call: the withdrawal count", n == fig["withdrawals_total"], "%d" % n)
    ck("call: the reason", codes[order[0]] == fig["call"], codes[order[0]])
    ck("call: the runner-up", codes[order[1]] == fig["runner_up"], codes[order[1]])
    for k, c in enumerate(codes):
        ck("call: share %s" % c, round(100 * p[k], 1) == fig["corrected_share_pct"][c], "%.3f" % (100 * p[k]))
        ck("call: coded share %s" % c, round(100 * q[k], 1) == fig["coded_share_pct"][c])
    ck("call: the gap", round(100 * (p[order[0]] - p[order[1]]), 1) == fig["gap_points"])
    ck("call: the split behind the work hours code",
       round(100 * Rm[codes.index("CR"), codes.index("WH")], 1) == fig["wh_coded_belonging_cr_pct"])

    # ---- the rungs, each on its own arithmetic ----------------------------------------
    ck("rung 0 names work hours clash", codes[int(np.argmax(q))] == "WH")
    keep = [k for k, c in enumerate(codes) if c != "OT"]
    ck("rung 1 names work hours clash", codes[keep[int(np.argmax(q[keep]))]] == "WH")
    mc = collections.Counter(m["moderated_reason"] for m in mod)
    ck("rung 2 names other or not stated", mc.most_common(1)[0][0] == "OT")
    mref = {m["withdrawal_ref"]: m["moderated_reason"] for m in mod}
    sub = collections.Counter(mref.get(ref, c) for ref, (_, c) in recs.items())
    ck("rung 2b names work hours clash", sub.most_common(1)[0][0] == "WH")
    joint = collections.Counter((m["coded_reason"], m["moderated_reason"]) for m in mod)
    tot_true = collections.Counter(m["moderated_reason"] for m in mod)
    M = np.array([[joint[(i, j)] / tot_true[j] for j in codes] for i in codes])
    ck("rung 3 the unweighted inversion gives a negative share", (np.linalg.solve(M, q) < 0).any())

    # ---- the asks ---------------------------------------------------------------------
    sites = rd("site_directory.csv")
    sc = {s_["site_code"]: s_["site_name"] for s_ in sites}
    cat = {c["course_ref"]: c for c in rd("course_catalogue_2025_26.csv")}
    rows = [e for e in rd("enrolments_2025_26.csv") if e["site_code"] in sc]
    tc = ["T1", "T2", "T3", "T4"]
    by_l = collections.defaultdict(list)
    for e in rows:
        by_l[e["uln"]].append(e)
    # own path: a learner whose two-term course stops after its first term and who turns up in the next term
    # on a one-term course starting then, at that course's centre, has moved with the course
    moves = collections.Counter()
    for u, es in by_l.items():
        refs = {(e["course_ref"], e["term_code"]) for e in es}
        for e in es:
            c = cat[e["course_ref"]]
            if c["terms_spanned"] != "2" or e["term_code"] != c["start_term"]:
                continue
            nxt = tc[tc.index(c["start_term"]) + 1]
            if (e["course_ref"], nxt) in refs:
                continue
            for f in es:
                c2 = cat[f["course_ref"]]
                if (f["term_code"] == nxt and c2["start_term"] == nxt and c2["terms_spanned"] == "1"
                        and c2["curriculum_area"] == c["curriculum_area"]
                        and c2["planned_guided_hours"] == c["planned_guided_hours"]):
                    moves[(f["course_ref"], e["course_ref"])] += 1
    link = {}
    for (new, old), k in moves.items():
        if k > moves.get((new, link.get(new)), 0):
            link[new] = old
    ck("asks: one old reference per new one", len(set(link.values())) == len(link) == fig["cutover_links"],
       "%d links" % len(link))
    lc = collections.defaultdict(lambda: {"rows": [], "done": False})
    for e in rows:
        d = lc[(e["uln"], link.get(e["course_ref"], e["course_ref"]))]
        d["rows"].append((tc.index(e["term_code"]), e["site_code"]))
        d["done"] |= e["status"] == "completed"
    hours = collections.Counter()
    st, dn = collections.Counter(), collections.Counter()
    for (u, ref), d in lc.items():
        hours[cat[ref]["curriculum_area"]] += int(cat[ref]["planned_guided_hours"])
        first = sc[min(d["rows"])[1]]
        st[first] += 1
        dn[first] += d["done"]
    for area, v in fig["ask1_planned_hours"].items():
        ck("ask 1 hours %s" % area, hours[area] == v, "%d against %d" % (hours[area], v))
    for c, v in fig["ask2_started"].items():
        ck("ask 2 started %s" % c, st[c] == v, "%d against %d" % (st[c], v))
        ck("ask 2 completed %s" % c, round(100 * dn[c] / st[c], 1) == fig["ask2_completed_pct"][c])

    # ---- the goldens agree with the recomputation ------------------------------------
    gc = {r["reason_code"]: float(r["share_of_withdrawals_pct"])
          for r in csv.DictReader(open(os.path.join(G, "withdrawal_reason_composition_2025_26.csv"), encoding="utf-8"))}
    ck("golden csv shares", all(abs(gc[c] - round(100 * p[k], 1)) < 1e-9 for k, c in enumerate(codes)))
    wb = openpyxl.load_workbook(os.path.join(G, "retention_target_2027.xlsx"))
    vals = [[c.value for c in r] for r in wb["Provision 2025-26"].iter_rows()]
    gh = {r[0]: r[1] for r in vals if r and r[0] in hours}
    ck("golden workbook hours", all(gh[a_] == hours[a_] for a_ in hours))
    gs = {r[0]: (r[1], r[2]) for r in vals if r and r[0] in st}
    ck("golden workbook centres", all(gs[c][0] == st[c] and gs[c][1] == round(100 * dn[c] / st[c], 1) for c in st))
    ck("golden workbook names the reason", any(fig["call_label"] in str(c.value or "")
                                               for r in wb["Reason composition"].iter_rows() for c in r))
    ck("golden workbook carries the chart", len(wb["Reason composition"]._charts) == 1)

    print("verify: %d checks, %d failed" % (N[0], len(FAIL)))
    for x in FAIL:
        print("  FAIL", x)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
