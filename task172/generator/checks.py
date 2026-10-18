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


def check(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def qm(rens, comp_kw=None, sim_kw=None):
    comp = K.components(rens, **(comp_kw or {}))
    w, info = K.simulate(comp, **(sim_kw or {}))
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
    gold = C.half_month(Q["months"])
    exp = C.EXPORT

    # ------------------------------------------------------------------ the golden and its edge
    check("golden quote 5.5 months", gold == 5.5, "%.3f months" % Q["months"])
    check("golden mid-bin (a quarter-bin clear of each edge)", C.edge(Q["months"], 0.5) >= 0.125,
          "edge distance %.3f" % C.edge(Q["months"], 0.5))
    fw = Wm.forward_truth(W)
    truth = float(np.quantile(fw, 0.8)) / M
    check("generator truth: the realised quarter's 80th percentile rounds to the golden", C.half_month(truth) == gold,
          "%.3f months over %d renewals" % (truth, len(fw)))
    dpost = [(c.card.valid_to - c.received).days for c in W.cases if c.received and C.IFR <= c.received <= exp and
             c.filed_by == "Counsel"]
    mq, reach_m, cut_m = Wm.model_quantile(d_samples=dpost)
    check("generator truth: the process's 80th percentile rounds to the golden", C.half_month(mq / M) == gold,
          "%.3f months" % (mq / M))

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
    w, _ = K.simulate(comp)
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
    v = float(np.quantile(K.simulate(comp11)[0], 0.8)) / M
    check("SF11 card gaps from 2026 renewals only give the same call", C.half_month(v) == gold, "%.3f" % v)
    v = float(np.quantile(w, 0.8, method="linear")) / M
    v2 = float(np.quantile(w, 0.8, method="lower")) / M
    check("SF12 percentile conventions agree", C.half_month(v) == C.half_month(v2) == gold, "%.3f %.3f" % (v, v2))
    late = [n for n in T["notices"] if K._d(n["logged_on"]) > exp]
    check("SF13 nothing in the export is logged after 4 December 2026, so a later as-of reads the same rows", not late,
          "%d" % len(late))
    v, _ = qm(renewals_with(T, cases, ref, appt="first"))
    check("SF14 the first appointment notice gives the same call", C.half_month(v) == gold, "%.3f" % v)

    # ------------------------------------------------------------------ constructions, one sigma, rivals
    var = L.variants(Q)
    worst = min(var.values(), key=lambda x: C.edge(x, 0.5))
    check("every standard construction lands the golden bin a quarter-bin clear",
          all(C.half_month(x) == gold and C.edge(x, 0.5) >= 0.125 for x in var.values()),
          "%d constructions %.3f to %.3f, tightest edge %.3f" % (len(var), min(var.values()), max(var.values()),
                                                                C.edge(worst, 0.5)))
    sig = L.one_sigma(Q)
    check("a one-sigma move in each component leaves the quote", all(C.half_month(x) == gold for x in sig.values()),
          "%.3f to %.3f" % (min(sig.values()), max(sig.values())))
    natural = [k for k in routes if not k.startswith("_") and not k.startswith("cut at the card") and
               not k.startswith("every renewal cut") and not k.startswith("renewals decided after an expedite") and
               k not in ("record plus 1.5 months", "post-rule record, 97.5th percentile")]
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
    check("the write-up's 7.0 rival holds on the whole record too", C.half_month(v) == 7.0, "%.3f" % v)
    check("the subset at the forward exposure is empty (no decided renewal met the new delay)",
          routes["_longest_decided_post_rule_lead"] < np.percentile(comp["L"], 10),
          "longest decided post-rule lead %.0f days, forward tenth percentile %.0f" % (
              routes["_longest_decided_post_rule_lead"], np.percentile(comp["L"], 10)))
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
    per = []
    for cat in C.CATS:
        sub = [r for r in rens if r["cat"] == cat]
        c2 = K.components(sub) if cat == "(c)(26)" else dict(K.components(rens), qrows=K.components(sub)["qrows"],
                                                             pA=K.components(sub)["pA"])
        per.append(float(np.quantile(K.simulate(c2)[0], 0.8)) / M)
    check("H14 the quote holds with the components by category", all(C.half_month(x) == gold for x in per),
          "(c)(9) %.3f, (c)(26) %.3f" % tuple(per))
    last12 = [r for r in rens if r["received"] >= dt.date(2025, 12, 1)]
    c3 = dict(comp, qrows=K.components(last12)["qrows"])
    v = float(np.quantile(K.simulate(c3)[0], 0.8)) / M
    check("H14 the quote holds with the review from the last 12 months of receipts", C.half_month(v) == gold, "%.3f" % v)

    # ------------------------------------------------------------------ critical components
    for a, b in ((dt.date(2026, 10, 1), dt.date(2026, 10, 31)), (dt.date(2026, 11, 1), dt.date(2026, 11, 30)),
                 (dt.date(2026, 10, 1), dt.date(2026, 11, 30)), (dt.date(2026, 9, 14), dt.date(2026, 11, 30))):
        s = [(r["appt"] - r["received"]).days for r in rens if r["route"] == "appointment" and r["appt"] and
             a <= r["received"] <= b]
        check("CC1 the appointment lead rounds to 17 weeks, receipts %s to %s" % (a, b),
              round(np.median(s) / 7) == 17 and C.edge(np.median(s) / 7, 1) >= 0.1, "%.2f weeks" % (np.median(s) / 7))
    old = [(r["appt"] - r["received"]).days for r in rens if r["route"] == "appointment" and r["appt"] and
           r["received"] < dt.date(2026, 9, 1)]
    check("CC1 the earlier lead rounds to 4 weeks", round(np.median(old) / 7) == 4, "%.2f" % (np.median(old) / 7))
    reaches = [K.simulate(K.components(rens, regime=rg))[1]["reach"] for rg in (
        K.NEW_REGIME, (dt.date(2026, 11, 1), dt.date(2026, 11, 30)), (dt.date(2026, 9, 14), dt.date(2026, 11, 30)))]
    check("CC2 more than half reach their card's expiry undecided under every lead window", min(reaches) > 0.55,
          "%.3f to %.3f" % (min(reaches), max(reaches)))
    ex = [r for r in rens if r["exp_req"] and r["decided"] and r["decided"] >= r["exp_req"]]
    e_all = np.median([(r["decided"] - r["exp_req"]).days for r in ex])
    e_acc = np.median([(r["decided"] - r["exp_req"]).days for r in ex if r["exp_out"] == "Accepted"])
    check("CC3 the expedite response is about a week, accepted or all requests", 3.5 <= e_all < 10.5 and 3.5 <= e_acc < 10.5,
          "%.1f and %.1f days" % (e_all, e_acc))
    pend = [c for c in W.cases if c.received and C.IFR <= c.received and c.filed_by == "Counsel" and
            c.w_nat > (c.card.valid_to - c.received).days and c.card.valid_to < exp and
            not (c.principal.term and c.principal.term <= c.card.valid_to)]
    check("the case log carries an expedite request for every post-rule renewal still in the team's care at expiry",
          all(c.exp_req for c in pend), "%d renewals" % len(pend))

    # ------------------------------------------------------------------ asks: truth, devices, cracker, separation line
    def active(e):
        return e.hire <= exp and (e.term is None or e.term > exp)
    ta = {(y, m, c): 0 for (y, m) in C.ASK_A_MONTHS for c in C.CATS}
    a1 = Counter()
    a5 = Counter()
    for c in W.cards:
        if c.valid_from > exp or (c.case is not None and (c.case.withdrawn or c.case.received is None)):
            continue
        if c.case is not None and c.case.decided and c.case.decided > exp:
            continue
        cur = active(c.holder) if c.htype == "Employee" else active(c.holder.principal)
        k = (c.valid_to.year, c.valid_to.month, c.cat)
        if cur and k in ta:
            ta[k] += 1
            if not c.roster:
                a1[k] += 1
            elif c.roster_cat != c.cat:
                a5[k] += 1
                a5[(k[0], k[1], c.roster_cat)] += 1
    A = K.ask_a(T, cases, ref)
    check("ask A: the pack's answer equals the clean truth, cell by cell", A == ta, str(sorted(A.items())))
    check("ask A: device A1 (cards missing from the roster) moves every cell", all(a1[k] >= 1 for k in ta),
          str(dict(a1)))
    check("ask A: device A5 (category stored before the switch) moves every cell", all(a5[k] >= 1 for k in ta),
          str(dict(a5)))
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
    v = float(np.quantile(K.simulate(Qc)[0], 0.8)) / M
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
