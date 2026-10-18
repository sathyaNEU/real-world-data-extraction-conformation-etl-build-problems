"""task172 generator checks: the three rules executed on the clean truth (R1, R2, R3a to R3c), every semantic fork
row (SF1 to SF14), the constructions, the rivals, the one-sigma moves, the asks' truth and devices, the input gates and
the realism sweep. Exit 1 on any failure.

    python3 task172/generator/checks.py task172/target"""
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K       # noqa: E402
import common as C     # noqa: E402
import cracker as CR   # noqa: E402
import docs as D       # noqa: E402
import ladder as L     # noqa: E402
import pack as P       # noqa: E402
import world as Wm     # noqa: E402

M = C.MONTH_DAYS
ROWS = []
MIX = {}            # the quarter's category mix the golden reads, set in main


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def norm_ws(s):
    return re.sub(r"\s+", " ", s.replace("’", "'")).strip()


def pdf_reads(path):
    """the shipped PDF's text as each reader a solver would reach for extracts it, whitespace collapsed"""
    import shutil
    import subprocess
    import pdfplumber
    from pdfminer.high_level import extract_text
    from pypdf import PdfReader
    out = {"pypdf": " ".join(p.extract_text() or "" for p in PdfReader(path).pages),
           "pypdf strict": " ".join(p.extract_text() or "" for p in PdfReader(path, strict=True).pages),
           "pdfminer.six": extract_text(path)}
    with pdfplumber.open(path) as doc:
        out["pdfplumber"] = " ".join(p.extract_text() or "" for p in doc.pages)
    if shutil.which("pdftotext"):
        out["pdftotext"] = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True, check=True).stdout
    return {k: norm_ws(v) for k, v in out.items()}


def qm(rens, comp_kw=None, sim_kw=None):
    comp = K.components(rens, **(comp_kw or {}))
    w, info = K.simulate(comp, **dict(dict(mix=MIX or None), **(sim_kw or {})))
    return float(np.quantile(w, 0.8)) / M, info


def renewals_with(T, cases, ref, received="received_date", decision="notice_date", appt="latest", start_at=None):
    """counsel's renewals rebuilt with another choice of date or notice, for the R2 and SF assertions"""
    import copy
    T2 = copy.copy(T)
    rows = []
    for n in T["notices"]:
        n2 = dict(n)
        if received == "notice_date" and n["notice_type"] == "Receipt notice":
            n2["received_date"] = n["notice_date"]
        if received == "logged_on" and n["notice_type"] == "Receipt notice":
            n2["received_date"] = n["logged_on"]
        if decision == "logged_on" and n["notice_type"] in ("Approval notice", "Denial notice"):
            n2["notice_date"] = n["logged_on"]
        rows.append(n2)
    T2["notices"] = rows
    rens = K.renewals(T2, cases, ref)
    if appt == "first":
        for r in rens:
            r["appt"] = r["appt_first"]
    return rens


def main(target):
    W, R = P.records()
    Q = K.quote(target)
    T, cases, ref, rens, comp = Q["T"], Q["cases"], Q["ref"], Q["rens"], Q["comp"]
    MIX.update(Q["mix"])
    gold = C.half_month(Q["months"])
    exp = C.EXPORT

    # ------------------------------------------------------------------ the golden and its edge
    check("golden quote 5.5 months", gold == 5.5, "%.3f months" % Q["months"])
    mg = L.margin(Q)
    check("the margin rule: every construction, moved by the golden's largest one-sigma move, a quarter-bin clear of "
          "both edges", mg["ok"], "%d constructions %.3f to %.3f; with one sigma %.3f to %.3f, edges %.3f and %.3f" % (
              len(mg["var"]), min(mg["var"].values()), max(mg["var"].values()), mg["lo"], mg["hi"], mg["edge_lo"],
              mg["edge_hi"]))
    fw = Wm.forward_truth(W)
    truth = float(np.quantile(fw, 0.8)) / M
    check("generator truth: the realised quarter's 80th percentile rounds to the golden", C.half_month(truth) == gold,
          "%.3f months over %d renewals" % (truth, len(fw)))
    pq, n_fw, _ = Wm.process_q80(W)
    check("generator truth: the process 80th percentile (every renewal of the quarter re-run 200 times) rounds to the "
          "golden", C.half_month(pq / M) == gold, "%.3f months over %d renewals" % (pq / M, n_fw))
    fq = [cs for cs in W.cases if cs.received and C.Q_START <= cs.received <= C.Q_END and cs.filed_by == "Counsel"]
    share9 = sum(cs.cat == "(c)(9)" for cs in fq) / len(fq)
    check("the quarter's category mix read from the pack is the quarter's own (within three points)",
          abs(Q["mix"]["(c)(9)"] - share9) < 0.03, "pack %.3f, world %.3f" % (Q["mix"]["(c)(9)"], share9))

    # ------------------------------------------------------------------ R1: the field's raw material ships
    rec = [r for r in rens if r["received"] and r["received"] <= exp]
    check("R1 censored durations ship: receipts, appointments and decisions for every renewal, open ones included",
          len(rec) > 9000 and sum(1 for r in rec if r["decided"] is None and not r["withdrawn"]) > 500,
          "%d renewals, %d open" % (len(rec), sum(1 for r in rec if r["decided"] is None and not r["withdrawn"])))
    check("R1 the cut's raw material ships: card expiries (register) and expedite requests (case log)",
          len(comp["D"]) > 2000 and len(comp["E"]) > 50, "D %d, E %d" % (len(comp["D"]), len(comp["E"])))
    heads = []
    for f in glob.glob(os.path.join(target, "*.csv")):
        heads += [(os.path.basename(f), h) for h in open(f, encoding="utf-8").readline().strip().split(",")]
    bad = [h for f, h in heads if re.search(r"wait|quote|percentile|processing_time|lapse|capped", h, re.I)]
    check("R1 no shipped column holds the deciding quantity", not bad, ", ".join(bad) or "none")

    # ------------------------------------------------------------------ R2: every mess item neutral for the call
    def r2(label, rens2, **kw):
        v, info = qm(rens2, **kw)
        check("R2 " + label, C.half_month(v) == gold, "%.3f months" % v)
    no_legacy = dict(ref)
    for k in list(no_legacy):
        if k.startswith("RN-"):
            no_legacy.pop(k)
    r2("crosswalk ignored (RN references left unmatched)", K.renewals(T, cases, no_legacy))
    r2("first appointment notice taken, not the latest", renewals_with(T, cases, ref, appt="first"))
    r2("receipt notice's notice date taken for the receipt date", renewals_with(T, cases, ref, received="notice_date"))
    r2("logged dates taken for receipts and decisions",
       renewals_with(T, cases, ref, received="logged_on", decision="logged_on"))
    r2("withdrawn renewals kept as open", [dict(r, withdrawn=False) for r in rens])
    r2("stopped renewals left out", [r for r in rens if not r["stop"]])
    reg_dec = []
    for r in rens:
        c = cases.get(r["case"])
        d = c["decided"] if c else None
        reg_dec.append(dict(r, decided=d if d and r["decided"] else (None if not d else d)))
    r2("the register's decision dates taken (they lag counsel's)", reg_dec)
    T_nocards = dict(T)
    T_nocards["notices"] = [n for n in T["notices"] if not n["notice_type"].startswith("Card ")]
    r2("card production and mailing events removed (re-scans included)", K.renewals(T_nocards, cases, ref))
    T_norej = dict(T)
    T_norej["notices"] = [n for n in T["notices"] if n["notice_type"] != "Rejection notice"]
    r2("rejection notices removed from the export", K.renewals(T_norej, cases, ref))
    r2("legacy register sheet dropped (card expiries only from the current sheet)",
       [dict(r, card_exp=r["card_exp"] if (r["case"] or "").startswith("GM-") else None) for r in rens])

    # ------------------------------------------------------------------ R3: the analyst test, the decisive step, no plant
    routes = L.routes(Q)
    dflt = routes["default: post-rule record, appointment waits plus the new delay"]
    check("R3a analyst test: the default path, every filed rule applied, files 7.0", C.half_month(dflt) == 7.0,
          "%.3f months" % dflt)
    check("R3a the default path reweighted to the quarter's categories files 6.5 (the write-up's 6.5 to 7.0)",
          C.half_month(routes["default path reweighted to the quarter's categories"]) == 6.5,
          "%.3f" % routes["default path reweighted to the quarter's categories"])
    check("R3a the record's own waits, open cases censored, file 4.0",
          C.half_month(routes["record KM, all receipts"]) == 4.0, "%.3f" % routes["record KM, all receipts"])
    unc = routes["stage model, uncapped"]
    check("R3b the decisive step alone (the cut at each card's expiry plus the response) moves the default to the golden",
          C.half_month(unc) != gold and gold == 5.5, "uncapped %.3f, cut %.3f" % (unc, Q["months"]))
    for k in ("record KM, since 30 Oct 2025", "record since the rule plus the new delay, flat",
              "record since the rule plus the new delay times the appointment share"):
        check("R3b a lower rung's single correction stays wrong: " + k, abs(C.half_month(routes[k]) - gold) >= 0.5,
              "%.3f" % routes[k])
    thread = " ".join(D.thread_text())
    nums = [x for x in re.findall(r"\d+(?:\.\d+)?", re.sub(r"\(c\)\(\d+\)", "", thread))]
    check("R3c no plant: the thread carries no figure about the wait (only its calendar and the 18-month cards)",
          set(nums) <= {"15", "10", "1", "18", "2026"}, ",".join(nums))
    check("R3c no prior quote or stakeholder figure ships", not any(re.search(r"\bquote\b", h, re.I) for _, h in heads))

    # ------------------------------------------------------------------ the semantic fork table
    sent = {}
    for c in cases.values():
        if c["sent"]:
            sent[c["id"]] = c["sent"]
    sf1 = [dict(r, received=sent.get(r["case"], r["received"])) for r in rens]
    v, _ = qm(sf1)
    check("SF1 waits from the packet's dispatch give the same call", C.half_month(v) == gold, "%.3f" % v)
    v, _ = qm(rens, comp_kw=dict(d_from=C.IFR))
    check("SF2 the quarter by receipt (dispatch only shifts the card gaps it reads)", C.half_month(v) == gold, "%.3f" % v)
    check("SF3 four in five is the 80th percentile (prompt and standard 4.1)",
          "four in five" in open(os.path.join(os.path.dirname(target), "prompt.txt")).read())
    appr_only = []
    for r in rens:
        appr_only.append(dict(r, decided=r["decided"] if r["approved"] else None))
    v, _ = qm(appr_only)
    check("SF4 approvals only as decisions give the same call", C.half_month(v) == gold, "%.3f" % v)
    deliv = defaultdict(list)
    for n in T["notices"]:
        if n["notice_type"] == "Card delivered":
            deliv[n["receipt_no"]].append(K._d(n["notice_date"]))
    sf5 = [dict(r, decided=min(deliv[r["receipt"]]) if r["decided"] and deliv.get(r["receipt"]) else None) for r in rens]
    v, _ = qm(sf5)
    check("SF5 the wait to the card's delivery is another quantity (standard 4.2 rules it out)",
          "date of USCIS's decision notice" in " ".join(D.policy_text()) and C.half_month(v) != gold, "%.3f" % v)
    w, _ = K.simulate(comp, mix=MIX)
    v = float(np.quantile(w, 0.8)) / (365.25 / 12)
    check("SF6 a month of 365.25/12 days gives the same call", C.half_month(v) == gold, "%.3f" % v)
    check("SF7 rounding is pinned to the nearest half month (prompt, standard 4.3)",
          "nearest half month" in open(os.path.join(os.path.dirname(target), "prompt.txt")).read())
    v, _ = qm([dict(r, withdrawn=False) for r in rens])
    check("SF8 withdrawn renewals kept as open give the same call", C.half_month(v) == gold, "%.3f" % v)
    v, _ = qm([r for r in rens if not r["stop"]])
    check("SF9 renewals stopped on a departure left out give the same call", C.half_month(v) == gold, "%.3f" % v)
    check("SF10 one quote over both categories (the prompt asks one wait)",
          open(os.path.join(os.path.dirname(target), "prompt.txt")).read().count("What wait") == 1)
    opened = {c["person"] for c in cases.values() if c["type"] == "renewal" and c["opened"] and
              c["opened"] >= dt.date(2026, 11, 1)}
    comp11 = dict(comp)
    comp11["D"] = np.array([(r["card_exp"] - r["received"]).days for r in rens if r["card_exp"] and
                            r["received"] >= dt.date(2026, 1, 1)], float)
    v = float(np.quantile(K.simulate(comp11, mix=MIX)[0], 0.8)) / M
    check("SF11 card gaps from 2026 renewals only give the same call", C.half_month(v) == gold, "%.3f" % v)
    v = float(np.quantile(w, 0.8, method="linear")) / M
    v2 = float(np.quantile(w, 0.8, method="lower")) / M
    check("SF12 percentile conventions agree", C.half_month(v) == C.half_month(v2) == gold, "%.3f %.3f" % (v, v2))
    late = [n for n in T["notices"] if K._d(n["logged_on"]) > exp]
    check("SF13 nothing in the export is logged after 4 December 2026, so a later as-of reads the same rows", not late,
          "%d" % len(late))
    v, _ = qm(renewals_with(T, cases, ref, appt="first"))
    check("SF14 the first appointment notice gives the same call", C.half_month(v) == gold, "%.3f" % v)
    dn = defaultdict(set)
    for n in T["notices"]:
        if n["notice_type"] in ("Approval notice", "Denial notice"):
            dn[ref.get(n["client_ref"])].add(K._d(n["notice_date"]))
    both = [(c["decided"], dn[c["id"]]) for c in cases.values() if c["decided"] and c["id"] in dn]
    check("SF15 the register's decided_on is the decision notice's date on every case both hold", len(both) > 3000 and
          all(d in ds and len(ds) == 1 for d, ds in both), "%d cases" % len(both))
    pol = " ".join(D.policy_text())
    reads = pdf_reads(os.path.join(target, C.F_POLICY))
    paras = [norm_ws(x) for x in D.policy_text()]
    lost = {k: sum(1 for x in paras if x not in t) for k, t in reads.items()}
    check("H25 the standard opens in every reader a solver would use (pypdf lenient and strict, pdfminer.six, "
          "pdfplumber, pdftotext) with every paragraph, GM-07 1.3 and 1.4 included, and the strict text equals the "
          "lenient", len(reads) >= 4 and not any(lost.values()) and reads["pypdf strict"] == reads["pypdf"],
          "; ".join("%s %d lost" % kv for kv in lost.items()))
    v, _ = qm(rens, sim_kw=dict(mix=None))
    check("SF16 the record's own category mix in place of the quarter's gives the same call", C.half_month(v) == gold,
          "%.3f" % v)
    check("SF17 GM-07 1.4 files ask A's permit: the card approved for the person most recently, held to its last day",
          "approved for the person most recently" in pol and "until its last day" in pol)
    check("SF18 GM-07 1.4 files ask A's category: the one on the card's approval notice, not the roster's entry",
          "category on its approval notice" in pol and "not always the category entered on HR's work permit roster" in pol)
    check("SF19 GM-07 1.3 files ask A's current employees (Active on HR's program roster) and their spouses",
          "shows the employee as Active" in pol and "spouses of current employees" in pol)
    check("SF20 GM-07 2.4 files ask B's within 30 days (USCIS's receipt no later than the 30th day after the notice's "
          "date); no refiling lands on day 30 or 31, so the inclusive and exclusive readings agree (asserted below)",
          "no later than the 30th day after the date on the rejection notice" in pol)
    check("SF21 GM-07 2.3 and 2.4 file ask B's filed again as USCIS's receipt", "filed on the date USCIS receives it" in pol
          and "when USCIS receives it" in pol)
    ratio = {}
    emp_state = {e["employee_id"]: e["work_state"] for e in T["employees"]}
    for st in sorted(set(emp_state.values())):
        def lead_in(a, b):
            v = []
            for r in rens:
                c = cases.get(r["case"])
                if not (c and r["route"] == "appointment" and r["appt"] and a <= r["received"] <= b):
                    continue
                e = c["person"] if c["ptype"] == "employee" else c["sponsor"]
                if emp_state.get(e) == st:
                    v.append((r["appt"] - r["received"]).days)
            return v
        now = lead_in(dt.date(2026, 10, 1), dt.date(2026, 11, 30))
        then = lead_in(dt.date(2025, 1, 1), dt.date(2025, 12, 31))
        if len(now) >= 5 and len(then) >= 20:
            ratio[st] = float(np.median(now) / np.median(then))
    check("SF22 the appointment queue is the support centre's, not a category's: the October and November lead stands "
          "at about four times the 2025 lead in every state the receipts reached", len(ratio) >= 5 and
          max(ratio.values()) / min(ratio.values()) < 1.35, ", ".join("%s %.2f" % kv for kv in ratio.items()))
    check("SF23 GM-07 1.3 files the spouse as the one person Global Mobility took into its care with the household, "
          "however Benefits covers her (a domestic partner included), and no other dependant",
          "the one person Global Mobility took into its care with the employee's household" in pol and
          "however Benefits covers her" in pol and "no other dependant is tracked" in pol)
    # SF25: one spouse per household forces a spouse's two IDs into one person; the per-ID reading that leaves out the
    # Benefits ID no Global Mobility record carries drops the current cards those IDs alone hold
    gmh = defaultdict(set)
    for p_ in T["permits"]:
        if p_.get("household_employee_id"):
            gmh[p_["household_employee_id"]].add(p_["holder_id"])
    for c in cases.values():
        if c["ptype"] == "spouse" and c["sponsor"]:
            gmh[c["sponsor"]].add(c["person"])
    for t in T["tracker"]:
        if t["relationship"] == "Spouse":
            gmh[t["principal_employee_id"]].add(t["applicant_id"])
    enr_ = {e["benefits_enrollment_id"]: e["employee_id"] for e in T["employees"]}
    benh = defaultdict(set)
    for d in T["dependants"]:
        if d["relationship"] in ("Spouse", "Domestic partner") and d["benefits_enrollment_id"] in enr_:
            benh[enr_[d["benefits_enrollment_id"]]].add(d["dependant_id"])
    extra = {e: ids - gmh[e] for e, ids in benh.items() if e in gmh and ids - gmh[e]}
    one = all(len(ids) <= 1 for ids in gmh.values()) and all(len(ids) <= 1 for ids in benh.values()) and \
        all(len(gmh[e]) == 1 for e in extra)
    act_ = {e["employee_id"] for e in T["employees"] if e["status"] == "Active"}
    best_ = {}
    for c in K.cards_held(T, cases, ref):
        h = c["holder"]
        if h in {e["employee_id"] for e in T["employees"]}:
            cur = h in act_
        else:
            cur = any(h in ids for e, ids in gmh.items() if e in act_)
        if cur and (h not in best_ or c["vf"] > best_[h]["vf"]):
            best_[h] = c
    A_ = K.ask_a(T, cases, ref)
    by_id_gm = {k: 0 for k in A_}
    for c in best_.values():
        k = (c["vt"].year, c["vt"].month, c["cat"])
        if k in by_id_gm:
            by_id_gm[k] += 1
    moved = {k: by_id_gm[k] - A_[k] for k in A_ if by_id_gm[k] != A_[k]}
    only_b = {k: v for k, v in K.benefits_id_only(T, cases, ref).items() if v}
    never = set().union(*[ids for e, ids in benh.items() if e not in gmh])
    never_cards = [c for c in K.cards_held(T, cases, ref) if c["holder"] in never]
    check("SF25 one spouse per household: every household whose Benefits spouse ID no Global Mobility record carries "
          "has exactly one Global Mobility spouse ID, so the two are one person; leaving the Benefits ID out drops the "
          "current cards only it carries (the cards submission step 5 names), and the spouses Benefits covers in "
          "households Global Mobility never took in hold no card",
          one and len(extra) > 500 and moved == {(2027, 9, "(c)(26)"): -2} and
          only_b == {k: -v for k, v in moved.items()} and never and not never_cards,
          "%d households, persons by ID with Global Mobility's links only %s, latest card only under the Benefits ID "
          "%s; %d spouses in households never taken in, %d cards" % (len(extra), moved, only_b, len(never),
                                                                     len(never_cards)))
    gm_spouse = {p_["holder_id"] for p_ in T["permits"] if p_["holder_type"] == "Spouse"}
    gm_spouse |= {c["person"] for c in cases.values() if c["ptype"] == "spouse"}
    gm_spouse |= {t["applicant_id"] for t in T["tracker"] if t["relationship"] == "Spouse"}
    kid_clash = [d["dependant_id"] for d in T["dependants"] if d["relationship"] == "Child" and d["dependant_id"] in gm_spouse]
    check("SF24 one dependant ID, one person: no child in Benefits carries a spouse's ID from Global Mobility's records",
          not kid_clash, ", ".join(kid_clash) or "none")

    # ------------------------------------------------------------------ constructions, one sigma, rivals
    var, sig = mg["var"], mg["sig"]
    check("every construction in the family lands the golden bin", all(C.half_month(x) == gold for x in var.values()),
          "; ".join("%s %.3f" % (k[:38], v) for k, v in var.items()))
    check("a one-sigma move in each component leaves the quote", all(C.half_month(x) == gold for x in sig.values()),
          "%.3f to %.3f" % (min(sig.values()), max(sig.values())))
    mr = L.misreads(Q)
    check("misreads of a shipped record still land the bin (none is in the family)",
          all(C.half_month(x) == gold for x in mr.values()), "; ".join("%s %.3f" % (k, v) for k, v in mr.items()))
    thin = [k for k in routes if k.startswith("decided renewals with an appointment") and k.endswith("since the rule")
            and not np.isnan(routes[k]) and routes["_n_lead_%s_post" % k.split(" days")[0].split()[-1]] < 15]
    check("the long-lead analogs filed since the rule that land are thin (fewer than 15 renewals each)",
          all(routes["_n_lead_%s_post" % k.split(" days")[0].split()[-1]] < 15 for k in thin
              if C.half_month(routes[k]) == gold),
          "; ".join("%s %.3f (n %d)" % (k.replace("decided renewals with an appointment ", ""), routes[k],
                                       routes["_n_lead_%s_post" % k.split(" days")[0].split()[-1]]) for k in thin))
    coincid = ("record since the rule plus the new delay times the quarter's appointment share",
               "record, all receipts, plus the new delay times the quarter's appointment share")
    check("flagged coincidental routes: a percentile moved by the new delay times the quarter's appointment share lands "
          "(a mean added to a percentile; the record's own share gives 6.0)",
          all(C.half_month(routes[k]) == gold for k in coincid) and
          C.half_month(routes["record since the rule plus the new delay times the appointment share"]) == 6.0,
          "%.3f and %.3f at the quarter's share %.3f; %.3f at the record's" % (
              routes[coincid[0]], routes[coincid[1]], routes["_pA_quarter"],
              routes["record since the rule plus the new delay times the appointment share"]))
    natural = [k for k in routes if not k.startswith("_") and not k.startswith("cut at the card") and
               not k.startswith("every renewal cut") and not k.startswith("renewals decided after an expedite") and
               k not in ("record plus 1.5 months", "post-rule record, 97.5th percentile") and k not in thin and
               k not in coincid]
    misses = {k: routes[k] for k in natural if not np.isnan(routes[k])}
    bad = [k for k, x in misses.items() if abs(C.half_month(x) - gold) < 0.5]
    check("every natural route misses the golden by a bin or more", not bad,
          "%d routes; landing: %s" % (len(misses), ", ".join(bad) or "none"))
    check("routes that land contain the cut, or are flagged reflexes",
          all(C.half_month(routes[k]) == gold for k in ("every renewal cut: q80 of expiry plus response",
                                                       "renewals decided after an expedite request, q80")),
          "flags: record plus 1.5 months %.3f, post-rule 97.5th percentile %.3f" % (
              routes["record plus 1.5 months"], routes["post-rule record, 97.5th percentile"]))
    whole = []
    for r in rens:
        if r["withdrawn"] or not r["route"] or r["received"] > dt.date(2026, 8, 23):
            continue
        end = min(x for x in (exp, r["stop"]) if x)
        add = routes["_dL_days"] if r["route"] == "appointment" else 0.0
        if r["decided"] and r["decided"] <= end:
            whole.append(((r["decided"] - r["received"]).days + add, 1))
        else:
            whole.append(((end - r["received"]).days + add, 0))
    v = K.km_quantile(whole) / M
    check("the write-up's 6.5 to 7.0 rival holds on the whole record too", C.half_month(v) in (6.5, 7.0), "%.3f" % v)
    p10 = float(np.percentile(comp["L"], 10))
    dec_a = [r for r in rens if r["decided"] and not r["withdrawn"] and r["route"] == "appointment" and r["appt"]]
    at_post = [r for r in dec_a if r["received"] >= C.IFR and (r["appt"] - r["received"]).days >= p10]
    at_all = [r for r in dec_a if (r["appt"] - r["received"]).days >= p10]
    q_all = float(np.quantile([(r["decided"] - r["received"]).days for r in at_all], 0.8)) / M if at_all else float("nan")
    check("common-exposure screen: the decided renewals at the forward exposure filed since the rule are too few to read "
          "a percentile from, and the whole record's (filed before the rule, their cards extended) miss the golden",
          len(at_post) <= 5 and (len(at_all) < 5 or abs(C.half_month(q_all) - gold) >= 0.5),
          "%d since the rule, %d in the whole record (80th percentile %.3f), at or past %.0f days" % (
              len(at_post), len(at_all), q_all, p10))
    bt = L.backtest(Q)
    check("separation: the cut model predicts the post-rule renewals pending at expiry, the uncapped model does not",
          bt["uncapped_mae"] >= 3 * bt["capped_mae"] and bt["share_within_14"] >= 0.9,
          "n %d, observed median %.0f days, uncapped predicted median %.1f, MAE %.1f vs %.1f, within 14 days %.2f" % (
              bt["n"], bt["obs_median"], bt["uncapped_pred_median"], bt["uncapped_mae"], bt["capped_mae"],
              bt["share_within_14"]))

    check("the write-up's back-test claim: the uncapped model's typical remaining wait is more than two weeks",
          bt["uncapped_pred_median"] > 14 and bt["obs_median"] <= 7, "%.1f against %.0f days" % (
              bt["uncapped_pred_median"], bt["obs_median"]))
    # H14: the quote at the finer grain the data allows (components by category where the category has them)
    parts = []
    for k, cat in enumerate(C.CATS):
        sub = [r for r in rens if r["cat"] == cat]
        c2 = dict(comp, pA=comp["pA_cat"][cat], qrows=K.components(sub)["qrows"])
        parts.append(K.simulate(c2, seed=500 + k, n=int(K.N_SIM * Q["mix"][cat]))[0])
    v = float(np.quantile(np.concatenate(parts), 0.8)) / M
    check("H14 the quote at the finest grain the record allows (route share and review by category, mixed by the "
          "quarter's categories)", C.half_month(v) == gold, "%.3f" % v)
    last12 = [r for r in rens if r["received"] >= dt.date(2025, 12, 1)]
    c3 = dict(comp, qrows=K.components(last12)["qrows"])
    v = float(np.quantile(K.simulate(c3, mix=MIX)[0], 0.8)) / M
    check("H14 the quote holds with the review from the last 12 months of receipts", C.half_month(v) == gold, "%.3f" % v)

    # ------------------------------------------------------------------ critical components
    for a, b in ((dt.date(2026, 10, 1), dt.date(2026, 10, 31)), (dt.date(2026, 11, 1), dt.date(2026, 11, 30)),
                 (dt.date(2026, 10, 1), dt.date(2026, 11, 30)), (dt.date(2026, 9, 14), dt.date(2026, 11, 30))):
        s = [(r["appt"] - r["received"]).days for r in rens if r["route"] == "appointment" and r["appt"] and
             a <= r["received"] <= b]
        check("CC1 the appointment lead rounds to 17 weeks, receipts %s to %s" % (a, b),
              round(np.median(s) / 7) == 17 and C.edge(np.median(s) / 7, 1) >= 0.1, "%.2f weeks" % (np.median(s) / 7))
    old = [(r["appt"] - r["received"]).days for r in rens if r["route"] == "appointment" and r["appt"] and
           r["received"] < dt.date(2026, 1, 1)]
    check("CC1 the lead through 2024 and 2025 rounds to 4 weeks", round(np.median(old) / 7) == 4 and
          C.edge(np.median(old) / 7, 1) >= 0.1, "%.2f" % (np.median(old) / 7))
    reaches = []
    for rg in (K.NEW_REGIME, (dt.date(2026, 11, 1), dt.date(2026, 11, 30)), (dt.date(2026, 9, 14), dt.date(2026, 11, 30))):
        for qm_ in ("km", "decided"):
            for dfr in (C.IFR, C.RECORD_START):
                reaches.append(K.simulate(K.components(rens, regime=rg, q_mode=qm_, d_from=dfr), mix=Q["mix"])[1]["reach_appt"])
    check("CC2 about nine in ten of the quarter's appointment-route renewals reach their card's expiry undecided, under "
          "every lead window, review estimator and card-gap window", 0.85 <= min(reaches) and max(reaches) < 0.95,
          "%.3f to %.3f" % (min(reaches), max(reaches)))
    ex = [r for r in rens if r["exp_req"] and r["decided"] and r["decided"] >= r["exp_req"]]
    e_all = np.median([(r["decided"] - r["exp_req"]).days for r in ex])
    e_acc = np.median([(r["decided"] - r["exp_req"]).days for r in ex if r["exp_out"] == "Accepted"])
    check("CC3 the expedite response is about a week, accepted or all requests", 3.5 <= e_all < 10.5 and 3.5 <= e_acc < 10.5,
          "%.1f and %.1f days" % (e_all, e_acc))
    pend = [c for c in W.cases if c.received and C.IFR <= c.received and c.filed_by == "Counsel" and
            c.w_nat > (c.card.valid_to - c.received).days + 15 and c.card.valid_to + dt.timedelta(days=15) < exp and
            not (c.principal.term and c.principal.term <= c.card.valid_to + dt.timedelta(days=15))]
    check("the case log carries an expedite request for every post-rule renewal still pending in the team's care two "
          "weeks past its card's expiry", all(c.exp_req for c in pend), "%d renewals" % len(pend))
    # H2/H3: the write-up's other claims
    summer = [(r["appt"] - r["received"]).days for r in rens if r["route"] == "appointment" and r["appt"] and
              dt.date(2026, 6, 1) <= r["received"] <= dt.date(2026, 8, 23)]
    check("H3 the lead rose to about 5 weeks by the summer of 2026 (receipts June to 23 August)",
          round(np.median(summer) / 7) == 5, "%.2f weeks" % (np.median(summer) / 7))
    check("H3 about half the quarter's renewals are (c)(9); fewer than three in ten (c)(9) renewals went to an "
          "appointment against seven in ten (c)(26)", 0.45 <= Q["mix"]["(c)(9)"] < 0.55 and Q["pA_cat"]["(c)(9)"] < 0.3
          and round(Q["pA_cat"]["(c)(26)"], 1) == 0.7, "mix %.3f; %.3f and %.3f" % (
              Q["mix"]["(c)(9)"], Q["pA_cat"]["(c)(9)"], Q["pA_cat"]["(c)(26)"]))
    offs = Counter()
    for r in rens:
        if r["exp_req"] and r["received"] >= C.IFR and r["card_exp"]:
            o = (r["exp_req"] - r["card_exp"]).days
            offs["on" if 0 <= o <= 3 and r["exp_req"] == C.next_busday(r["card_exp"]) else ("before" if o < 0 else "after")] += 1
    check("H3 the team's requests come mostly on the card's expiry date (or the next business day), some days before "
          "or after it", offs["on"] > 0.5 * sum(offs.values()) and offs["before"] >= 10 and offs["after"] >= 10,
          str(dict(offs)))
    check("H3 USCIS accepted most of the requests", 0.75 <= comp["accept"] < 0.95, "%.3f" % comp["accept"])
    # option A: USCIS's response held across months of very different volume, and after the appointment queue tripled
    exr = [r for r in rens if r["exp_req"] and r["received"] >= C.IFR and r["exp_out"] == "Accepted" and r["decided"]
           and r["decided"] >= r["exp_req"]]
    per_m = Counter(r["exp_req"].strftime("%Y-%m") for r in exr)
    busy = {m for m, n in per_m.items() if n >= 2 * np.median(list(per_m.values()))}
    e_busy = [(r["decided"] - r["exp_req"]).days for r in exr if r["exp_req"].strftime("%Y-%m") in busy]
    e_rest = [(r["decided"] - r["exp_req"]).days for r in exr if r["exp_req"].strftime("%Y-%m") not in busy]
    e_late = [(r["decided"] - r["exp_req"]).days for r in exr if r["exp_req"] >= dt.date(2026, 9, 1)]
    e_early = [(r["decided"] - r["exp_req"]).days for r in exr if r["exp_req"] < dt.date(2026, 9, 1)]
    check("option A: the expedite response is the same in the busiest request months and the rest, and since the "
          "appointment queue tripled", busy and len(e_busy) >= 20 and abs(np.median(e_busy) - np.median(e_rest)) <= 2
          and len(e_late) >= 20 and abs(np.median(e_late) - np.median(e_early)) <= 2,
          "busiest months %s (%d requests, median %.1f days) against %.1f; from September 2026 %d requests, median "
          "%.1f against %.1f; requests a month %d to %d" % (",".join(sorted(busy)), len(e_busy), np.median(e_busy),
                                                             np.median(e_rest), len(e_late), np.median(e_late),
                                                             np.median(e_early), min(per_m.values()), max(per_m.values())))

    # ------------------------------------------------------------------ asks: truth, devices, cracker, separation line
    def active(e):
        return e.hire <= exp and (e.term is None or e.term > exp)
    latest, ties = {}, []
    for c in W.cards:
        if c.valid_from > exp or (c.case is not None and (c.case.withdrawn or c.case.received is None)):
            continue
        if not (active(c.holder) if c.htype == "Employee" else active(c.holder.principal)):
            continue
        h = id(c.holder)
        if h in latest and latest[h].valid_from == c.valid_from:
            ties.append((latest[h], c))
        if h not in latest or c.valid_from > latest[h].valid_from:
            latest[h] = c
    lo_w, hi_w = dt.date(2027, 6, 1), dt.date(2027, 9, 30)
    check("ask A: GM-07 1.4 names one card per person wherever it counts (no current person with two cards approved "
          "the same day holds either to a last day from June to September 2027)",
          not any(lo_w <= x.valid_to <= hi_w for pair in ties for x in pair), "%d same-day pairs, none in the window" %
          len(ties))
    enr_active = {e["benefits_enrollment_id"] for e in T["employees"] if e["status"] == "Active"}
    dep_linked = {d["dependant_id"] for d in T["dependants"] if d["relationship"] != "Child" and
                  d["benefits_enrollment_id"] in enr_active}
    ta = {(y, m, c): 0 for (y, m) in C.ASK_A_MONTHS for c in C.CATS}
    a1, a2, a5, a3 = Counter(), Counter(), Counter(), Counter()
    for c in latest.values():
        k = (c.valid_to.year, c.valid_to.month, c.cat)
        if k not in ta:
            continue
        ta[k] += 1
        if not c.roster:
            a1[k] += 1
        if c.htype == "Spouse" and c.holder.id not in dep_linked:
            a2[k] += 1
        if c.roster and c.roster_cat != c.cat:
            a5[k] += 1
        p = c.holder if c.htype == "Employee" else c.holder.principal
        if c.cat == "(c)(9)" and p.gc_approved and p.gc_approved <= exp:
            a3[k] += 1
    A = K.ask_a(T, cases, ref)
    check("ask A: the pack's literal execution of GM-07 1.3 and 1.4 equals the clean truth, cell by cell", A == ta,
          str(sorted(A.items())))
    check("ask A: silent device A1 (the person's latest card never reached HR's roster) moves every cell",
          all(a1[k] >= 1 for k in ta), str(dict(a1)))
    check("ask A: silent device A2 (a spouse Benefits does not link to a current employee) moves every cell",
          all(a2[k] >= 1 for k in ta), str(dict(a2)))
    check("ask A: seen device A5 (the roster's category is not the approval's; GM-07 1.4) and hazard A3 (permanent "
          "residents' last cards, GM-07 1.4 keeps them) are present", sum(a5.values()) >= 3 and sum(a3.values()) >= 1,
          "A5 %s; A3 %s" % (dict(a5), dict(a3)))
    # A6: a spouse who joined the plan after intake carries her MP- ID on Global Mobility's records and a dependant ID
    # in Benefits and on the portal's uploads; an employee has one spouse, so the two IDs are one person
    by_id = K.ask_a(T, cases, ref, merge=False)
    moved6 = [k for k in A if by_id[k] != A[k]]
    _, spons = K.holders_current(T, cases)
    inv = defaultdict(set)
    for sid, eid in spons.items():
        inv[eid].add(sid)
    pairs = {eid: ids for eid, ids in inv.items() if len(ids) > 1}
    world_pair = {s.principal.id: {s.id, s.dep_id} for s in W.spouses if s.late_enroll}
    held = defaultdict(set)
    for c in K.cards_held(T, cases, ref):
        held[c["holder"]].add((c["vf"], c["vt"]))
    shared = sum(1 for eid, ids in pairs.items() if len(set.intersection(*[held[i] for i in ids])) > 0)
    one_each = all(sum(1 for x in W.spouses if x.principal is e) <= 1 for e in W.emps if e.spouse is not None)
    check("ask A: silent device A6 (one spouse under two IDs) moves every (c)(26) cell and a (c)(9) one, and every "
          "household the pack shows with two spouse IDs is one spouse's two IDs (an employee has one spouse; most "
          "pairs share a card to the day)",
          all((y, m, "(c)(26)") in moved6 for (y, m) in C.ASK_A_MONTHS) and len(moved6) >= 4 and one_each and
          all(world_pair.get(eid) == ids for eid, ids in pairs.items()) and shared >= 0.5 * len(pairs),
          "%d cells moved %s; %d households with two IDs, %d sharing a card" % (
              len(moved6), {k: by_id[k] - A[k] for k in moved6}, len(pairs), shared))
    # the call through ask A's devices un-cracked: roster cards and labels only, spouses linked through Benefits only
    enroll = {e["benefits_enrollment_id"]: e["employee_id"] for e in T["employees"]}
    dlink = {d["dependant_id"]: enroll[d["benefits_enrollment_id"]] for d in T["dependants"]
             if d["relationship"] != "Child" and d["benefits_enrollment_id"] in enroll}
    act_e = {e["employee_id"] for e in T["employees"] if e["status"] == "Active"}
    emp_ids = {e["employee_id"] for e in T["employees"]}
    best = {}
    for p_ in T["permits"]:
        h, vf, vt = p_["holder_id"], K._d(p_["valid_from"]), K._d(p_["valid_to"])
        cur = (h in act_e) if h in emp_ids else (dlink.get(h) in act_e)
        if cur and vf <= exp and (h not in best or vf > best[h][0]):
            best[h] = (vf, vt, p_["category"])
    lpr = {t["applicant_id"] for t in T["tracker"] if t["i485_status"] == "Approved"}
    g50 = int(round(Q["d_median"]))
    nm = Counter()
    for h, (vf, vt, cat) in best.items():
        if not (cat == "(c)(9)" and h in lpr) and C.Q_START <= vt - dt.timedelta(days=g50) <= C.Q_END:
            nm[cat] += 1
    mix_bad = {c: nm[c] / sum(nm.values()) for c in C.CATS}
    v_bad = float(np.quantile(K.simulate(comp, mix=mix_bad)[0], 0.8)) / M
    check("separation line: the call through ask A's devices un-cracked is the same call within a day",
          C.half_month(v_bad) == gold and abs(v_bad - Q["months"]) * M <= 1.0 + 1e-9,
          "%.3f against %.3f; the quarter's (c)(9) share %.3f against %.3f" % (v_bad, Q["months"], mix_bad["(c)(9)"],
                                                                           Q["mix"]["(c)(9)"]))
    tb = {}
    appl = Counter()
    selfref = Counter()
    for lab, a, b in C.ASK_B_QUARTERS:
        nr = nf = 0
        for cs in W.cases:
            for s in cs.sends:
                if s["outcome"] != "Rejected" or not (a <= s["notice"] <= b):
                    continue
                nr += 1
                appl[lab] += s["copy"] == "Applicant"
                if cs.received and cs.received > s["notice"] and (cs.received - s["notice"]).days <= C.REFILE_DAYS:
                    nf += 1
                    selfref[lab] += cs.filed_by == "Applicant" or s["copy"] == "Applicant"
                if cs.received and (cs.received - s["notice"]).days in (30, 31):
                    check("ask B: no refiling lands on day 30 or 31 (within 30 days reads one way)", False,
                          "%s %s" % (cs.id, s["notice"]))
        tb[lab] = (nr, nf)
    B = K.ask_b(T, cases, ref)
    check("ask B: the pack's answer equals the clean truth, quarter by quarter", B == tb, str(B))
    stops = {}
    for a in T["actions"]:
        if a["action"] == "Stop work":
            stops[ref.get(a["case_id"])] = K._d(a["action_date"])
    rec_on = set()
    for n in T["notices"]:
        if n["notice_type"] == "Receipt notice":
            rec_on.add(ref.get(n["client_ref"]))
    for c in cases.values():
        if c["received"]:
            rec_on.add(c["id"])
    first_sent = {}
    for r in sorted(T["dispatch"], key=lambda r: r["sent_on"]):
        if "renewal" in r["contents"]:
            first_sent.setdefault(ref.get(r["case_id"]), K._d(r["sent_on"]))
    late_refile = [r["packet_id"] for r in T["dispatch"] if "renewal" in r["contents"] and ref.get(r["case_id"]) in stops
                   and K._d(r["sent_on"]) > stops[ref.get(r["case_id"])] and
                   K._d(r["sent_on"]) > first_sent[ref.get(r["case_id"])]]
    no_rcpt = [r["packet_id"] for r in T["dispatch"] if "renewal" in r["contents"] and r["status"] == "Receipted" and
               ref.get(r["case_id"]) not in rec_on]
    check("ask B: no renewal packet is sent again after the team stopped work on its case, and every packet the mailroom "
          "marks Receipted has USCIS's receipt on record (so the mailroom log adds no refiling)",
          not late_refile and not no_rcpt, "%d late refiles, %d receipted without a receipt" % (len(late_refile),
                                                                                           len(no_rcpt)))
    check("ask B: applicant-only rejection notices fall in every quarter", all(appl[k] >= 1 for k in tb), str(dict(appl)))
    check("ask B: every quarter's refiled count turns on a filing counsel never logged", all(selfref[k] >= 1 for k in tb),
          str(dict(selfref)))
    S = CR.sheets(target)
    check("cracker misses every ask cell", S["base"] == 0, "%d of %d" % (S["base"], CR.N_ASK))
    check("pair ceiling at or under 40 with the most obvious device cracked", S["pair"] <= 40.0, "%.1f" % S["pair"])
    check("both top responses on the call, no device cracked: at or under 45", S["both_on_call"] <= 45.0,
          "%.1f" % S["both_on_call"])
    check("mirror leakage under 35 per cent of ask weight", S["mirror_leak"] < 35.0, "%.1f" % S["mirror_leak"])
    T_cut = dict(T)
    T_cut["actions"] = [a for a in T["actions"] if a["action"] != "Notice forwarded by applicant"]
    T_cut["notices"] = [n for n in T["notices"] if n["notice_type"] != "Rejection notice"]
    Qc = K.components(K.renewals(T_cut, cases, ref))
    v = float(np.quantile(K.simulate(Qc, mix=MIX)[0], 0.8)) / M
    check("separation line: the call reads no ask device (forwarded notices, rejection notices removed)",
          abs(v - Q["months"]) < 1e-9, "%.3f" % v)

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("input gates: 10 or more files", len(files) >= 10, "%d" % len(files))
    check("input gates: 3 or more formats", len(fmts) >= 3, ",".join(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("input gates: one file of 25,000 or more rows", big >= 25000, "%d" % big)
    meta = os.path.join(os.path.dirname(target), "metadata.json")
    if os.path.exists(meta):
        md = json.load(open(meta))
        check("input gates: two or more distractors named in metadata.json", len(md.get("distractors", [])) >= 2,
              ",".join(d["file"] for d in md.get("distractors", [])))
        check("distractor names carry no hint", not any(re.search(r"distract|decoy|unused", f, re.I) for f in files))

    # H9: the manifest lists the shipped set; the dictionary covers every data file
    man = [r["file"] for r in C.read_csv(os.path.join(target, C.F_MANIFEST))]
    check("H9 the manifest names exactly the shipped files", sorted(man) == sorted(files), str(set(man) ^ set(files)))
    dfiles = {f for f, _, _ in D.DICT}
    need = {f for f in files if f.endswith((".csv", ".xlsx")) and f not in (C.F_DICT, C.F_MANIFEST)}
    check("H9 the dictionary covers every data file", need <= dfiles, str(need - dfiles))
    # H16: dates past the export only in forward-looking columns, file by file
    allow = {C.F_NOTICES: {"appointment_date", "valid_to"}, C.F_REGISTER: {"card_expires", "new_card_expires"},
             C.F_PERMITS: {"valid_to"}, C.F_TRACKER: {"ead_valid_to"}, C.F_H1B: {"H-1B valid to"},
             C.F_EMPLOYEES: set(), C.F_DEPENDANTS: set(), C.F_ACTIONS: set(), C.F_DISPATCH: set(), C.F_POSTED: set()}
    late_cols = defaultdict(set)
    for f in (C.F_NOTICES, C.F_EMPLOYEES, C.F_DEPENDANTS, C.F_ACTIONS, C.F_DISPATCH, C.F_POSTED):
        for row in C.read_csv(os.path.join(target, f)):
            for k, v in row.items():
                if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v or "") and v > exp.isoformat():
                    late_cols[f].add(k)
    for r in T["reg_old"]:
        for k, v in r.items():
            d = K._d(v) if isinstance(v, str) and re.fullmatch(r"\d\d/\d\d/\d{4}", v) else None
            if d and d > exp:
                late_cols[C.F_REGISTER].add({"Card Expires": "card_expires", "New Card Expires": "new_card_expires"}.get(k, k))
    for r in T["reg_new"]:
        for k, v in r.items():
            if isinstance(v, (dt.date, dt.datetime)) and K._d(v) > exp:
                late_cols[C.F_REGISTER].add(k)
    for p in T["permits"]:
        for k, v in p.items():
            if isinstance(v, (dt.date, dt.datetime)) and K._d(v) > exp:
                late_cols[C.F_PERMITS].add(k)
    for t in T["tracker"]:
        for k, v in t.items():
            if isinstance(v, (dt.date, dt.datetime)) and K._d(v) > exp:
                late_cols[C.F_TRACKER].add(k)
    bad16 = {f: sorted(c - allow.get(f, set())) for f, c in late_cols.items() if c - allow.get(f, set())}
    check("H16 dates past the export sit only in forward-looking columns", not bad16, str(bad16))

    # ------------------------------------------------------------------ realism sweep
    months = Counter(r["received"].strftime("%Y-%m") for r in rens if r["received"] < dt.date(2026, 12, 1))
    check("realism: monthly receipt counts are not a constant stream", len(set(months.values())) >= 0.8 * len(months),
          "%d distinct of %d" % (len(set(months.values())), len(months)))
    acts = Counter(a["action"] for a in T["actions"])
    exn = acts["Expedite request"]
    det = Counter(a["detail"] for a in T["actions"] if a["action"] == "Expedite request")
    pre = sum(1 for a in T["actions"] if a["action"] == "Expedite request" and K._d(a["action_date"]) < C.IFR)
    check("realism: the expedite organ is a minority of the case log, varied, with pre-rule requests",
          exn < 0.1 * sum(acts.values()) and len(det) >= 3 and pre >= 3,
          "%d of %d actions, %d details, %d before the rule" % (exn, sum(acts.values()), len(det), pre))
    blob = b""
    for f in files:
        blob += open(os.path.join(target, f), "rb").read() if not f.endswith(".xlsx") else b"".join(
            zipfile.ZipFile(os.path.join(target, f)).read(n) for n in zipfile.ZipFile(os.path.join(target, f)).namelist())
    tells = [t for t in (b"openpyxl", b"ReportLab", b"reportlab", b"python-docx", b"matplotlib") if t in blob]
    check("realism: containers carry no writing library", not tells, ",".join(t.decode() for t in tells))
    names = {"Melinda Yang", "Brandon Zamora", "Jasmin Sims", "Raymond Navarro"}
    card = json.load(open(os.path.join(HERE, "..", "..", ".claude", "skills", "fingerprint", "cards", "task172.json")))
    check("realism: every named person is on the card or drawn from guard.py names (seed 172)",
          set(card["world"]["people"]) <= names)
    stamps = [v[3] for v in P.STAMPS.values()]
    check("realism: no office file saved after the export", max(stamps) <= "2026-12-04T23:59:59Z", max(stamps))
    check("realism: the thread is dated before the export", "03 Dec 2026" in D.THREAD[0]["date"])
    blocks = Counter()
    rows = open(os.path.join(target, C.F_NOTICES), encoding="utf-8").read().splitlines()[1:]
    for i in range(0, len(rows) - 5, 5):
        blocks[tuple(r.split(",", 1)[1] for r in rows[i:i + 5])] += 1
    check("realism: no repeated block of notice rows", max(blocks.values()) == 1)

    # ------------------------------------------------------------------ report
    fails = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %-100s %s" % ("PASS" if ok else "FAIL", label[:100], detail[:160]))
    print("%d checks, %d failed" % (len(ROWS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
