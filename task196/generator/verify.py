#!/usr/bin/env python3
"""task196's independent verifier. It reads only the shipped bundle, never the generator's world.

    python3 task196/generator/verify.py

It recomputes the call, the four review-group indices, the bridge, the whole ladder, the estimator family
and all three asks from target/ alone, then checks the golden deliverables and figures.json against what
it computed. Every shipped format is read back through this file's own readers, and every absence
assertion carries a positive control on the same code path.
"""
import csv
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

MEASURED = "2026/27"
AS_OF = dt.date(2027, 3, 31)
PULL = dt.date(2027, 7, 2)
SUBJECT = "KM-104"
ROUTES = ["beneficiary recall", "repatriation", "insurer contribution"]
NAMED_WINDOWS = (0, 1, 2, 3, 5, 7, 10, 14, 21, 28, 30, 45, 60, 90, 120)

PASS, FAIL = [], []


def ok(label, cond, detail=""):
    (PASS if cond else FAIL).append(label)
    print("%-5s %-46s %s" % ("PASS" if cond else "FAIL", label, detail))


def eq(label, a, b, detail=""):
    ok(label, a == b, detail or "%s against %s" % (a, b))


# --- readers, one per shipped format -------------------------------------
def rows(name, where=TARGET):
    with open(os.path.join(where, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sheet(name, tab, where=TARGET):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(where, name), data_only=True)
    vals = list(wb[tab].values)
    head = [str(h) if h is not None else "" for h in vals[0]]
    return [dict(zip(head, r)) for r in vals[1:] if any(v is not None for v in r)]


def pdf(name, where=TARGET):
    import pdfplumber
    out = []
    with pdfplumber.open(os.path.join(where, name)) as f:
        for page in f.pages:
            out.append(page.extract_text() or "")
    return re.sub(r"\s+", " ", "\n".join(out))


def text(name, where=TARGET):
    return re.sub(r"\s+", " ", open(os.path.join(where, name), encoding="utf-8").read())


def norm_account(ref):
    a, _, b = (ref or "").partition("/")
    return re.sub(r"\D", "", a) + re.sub(r"\D", "", b).zfill(8)


def d(s):
    return dt.date.fromisoformat(s) if s else None


# --- the call, rebuilt from the bundle -----------------------------------
def index_for(code, reg, matches, requests, volumes):
    recorded = [r for r in reg if r["member_code"] == code and r["scheme_year"] == MEASURED
                and r["cover_class"] == "scam reimbursement"]
    mine = [m for m in matches if m["member_code"] == code and m["scheme_year"] == MEASURED]
    req = {}
    for r in requests:
        if r["member_code"] == code and r["case_reference"]:
            req.setdefault(r["case_reference"], []).append(r["request_sent_date"])
    def produced_by_the_member(m):
        return any(s and s <= m["registered_date"] for s in req.get(m["case_reference"], []))
    independent = [m for m in mine if not produced_by_the_member(m)]
    both = [m for m in independent if m["case_reference"]]
    est = len(recorded) * len(independent) / len(both)
    vol = volumes[code]
    return dict(recorded=len(recorded), independent=len(independent), both=len(both),
                matched=len(mine), matched_recorded=len([m for m in mine if m["case_reference"]]),
                estimate=est, rate=est / vol * 1e6, index=round(est / vol * 1e6), volume=vol)


def main():
    reg = rows("case_register_2024_27.csv")
    matches = rows("member_payment_matches.csv")
    requests = rows("fund_return_requests.csv")
    register = rows("mule_account_register.csv")
    legs = rows("case_payments.csv")
    members = rows("member_register.csv")
    qr = sheet("member_quarterly_returns.xlsx", "returns 2024-25 onward")
    std = pdf("indemnity_standard_v6.pdf")
    pack_txt = pdf("trustee_pack_2027_07.pdf")
    notes = text("register_feed_notes.txt")
    figures = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))

    print("-- every shipped format reads back, with its positive control")
    ok("csv reads back", len(reg) > 15000 and "case_reference" in reg[0], "%d register rows" % len(reg))
    ok("xlsx reads back", len(qr) > 100 and "payments_sent" in qr[0], "%d return rows" % len(qr))
    ok("pdf reads back (standard), positive control",
       "whether or not the member's own systems recorded them" in std, "%d characters" % len(std))
    ok("pdf reads back (trustee pack), positive control",
       "Membership position at 31 March 2027" in pack_txt, "%d characters" % len(pack_txt))
    ok("txt reads back, positive control",
       "Pad the account number back to eight digits" in notes, "%d characters" % len(notes))
    wbk = sheet("settlement_advices_2026_27.xlsx", "advices")
    ok("xlsx reads back (settlement advices)", len(wbk) > 100 and "advice_total_gbp" in wbk[0],
       "%d advices" % len(wbk))
    dic = rows("data_dictionary.csv")
    dic_txt = " | ".join("%s %s %s" % (r["extract"], r["column"], r["definition"]) for r in dic)
    ok("the dictionary reads back and files the conventions the call leans on, positive control",
       len(dic_txt) > 0 and len({r["extract"] for r in dic}) >= 10
       and "The cover the case falls under: scam reimbursement or unauthorised fraud." in dic_txt
       and "A case is one case however many legs it covers." in dic_txt
       and "in thousands, on the sheet covering scheme years to 2023/24" in dic_txt,
       "%d rows over %d extracts, %d characters"
       % (len(dic), len({r["extract"] for r in dic}), len(dic_txt)))
    ok("the dictionary does not name the decisive step, on the same reader",
       not leaky_dic().search(dic_txt), "clean")

    print("\n-- the call")
    volumes = {}
    for m in members:
        volumes[m["member_code"]] = sum(int(r["payments_sent"]) for r in qr
                                        if r["member_code"] == m["member_code"]
                                        and r["scheme_year"] == MEASURED and r["vintage"] == "revised")
    ix = index_for(SUBJECT, reg, matches, requests, volumes)
    eq("the recorded case count", ix["recorded"], figures["call"]["recorded_cases"])
    eq("the indexed case count", round(ix["estimate"]), figures["call"]["indexed_cases"])
    eq("the payments sent", ix["volume"], figures["call"]["payments_sent"])
    eq("the index", ix["index"], figures["call"]["index_per_million"])
    ok("the index is the unrounded rate rounded once",
       abs(ix["rate"] - figures["call"]["index_unrounded"]) < 5e-4, "%.3f" % ix["rate"])
    edge = 0.5 - abs(ix["rate"] - round(ix["rate"]))
    ok("the index sits mid-bin at the stated rounding", edge >= 0.3,
       "distance to the bin edge %.3f against the floor 0.30" % edge)
    cc = figures["critical_components"]
    eq("the cases its own record did not hold", round(ix["estimate"]) - ix["recorded"],
       cc["cases_its_record_did_not_hold"])
    eq("the independent sightings", ix["independent"], cc["independent_sightings"])
    eq("the sightings that are also its own cases", ix["both"],
       cc["independent_sightings_also_recorded"])
    eq("the matches in total", ix["matched"], cc["matches_in_total"])
    eq("the matches its own requests produced", ix["matched"] - ix["independent"],
       cc["matches_its_own_requests_produced"])
    ok("its own detection coverage",
       abs(ix["recorded"] / ix["estimate"] * 100 - cc["own_detection_coverage_per_cent"]) < 0.05,
       "%.1f per cent" % (ix["recorded"] / ix["estimate"] * 100))

    print("\n-- the review group and the deliverables")
    review = [m["member_code"] for m in members if m["triennial_review_this_cycle"] == "yes"]
    eq("four members come to review", len(review), 4, ", ".join(review))
    for code in review:
        i2 = index_for(code, reg, matches, requests, volumes)
        eq("index for %s" % code, i2["index"], figures["review_group_index"][code])
        e2 = 0.5 - abs(i2["rate"] - round(i2["rate"]))
        ok("index for %s sits mid-bin" % code, e2 >= 0.3, "%.3f, edge %.3f" % (i2["rate"], e2))
    g_csv = rows("incidence_index_2027_28.csv", GOLDEN)
    eq("the golden csv carries the review group", len(g_csv), 4)
    for r in g_csv:
        i2 = index_for(r["member_code"], reg, matches, requests, volumes)
        eq("the golden csv's index for %s" % r["member_code"],
           int(r["scam_incidence_index_per_million"]), i2["index"])
        eq("the golden csv's recorded count for %s" % r["member_code"],
           int(r["cases_recorded_2026_27"]), i2["recorded"])
    g_ix = [r for r in sheet("member_incidence_review.xlsx", "index", GOLDEN)
            if str(r.get("member_code") or "").startswith("KM-")]
    eq("the golden workbook carries the review group", len(g_ix), 4)
    for r in g_ix:
        i2 = index_for(r["member_code"], reg, matches, requests, volumes)
        eq("the golden workbook's index for %s" % r["member_code"],
           int(r["scam_incidence_index_per_million"]), i2["index"])
    g_br = sheet("member_incidence_review.xlsx", "castlegate bridge", GOLDEN)
    col = "cases_per_million_payments"
    bridge = [r for r in g_br if r.get(col) is not None]
    per_m = lambda n: round(n / ix["volume"] * 1e6)
    eq("the walk is stated in index units and walks recorded to indexed",
       [int(r[col]) for r in bridge[:3]],
       [per_m(ix["recorded"]), per_m(ix["estimate"] - ix["recorded"]), per_m(ix["estimate"])])
    ok("the walk's two lines add to the index",
       per_m(ix["recorded"]) + per_m(ix["estimate"] - ix["recorded"]) == ix["index"],
       "%d + %d = %d" % (per_m(ix["recorded"]), per_m(ix["estimate"] - ix["recorded"]), ix["index"]))

    print("\n-- the ladder, the estimator family and the window sweep")
    def naive():
        mine = [m for m in matches if m["member_code"] == SUBJECT and m["scheme_year"] == MEASURED]
        mrec = [m for m in mine if m["case_reference"]]
        est = ix["recorded"] * len(mine) / len(mrec)
        return est / ix["volume"] * 1e6
    def window(days):
        opened = {r["case_reference"]: d(r["notified_date"]) for r in reg}
        keep = []
        for m in matches:
            if m["member_code"] != SUBJECT or m["scheme_year"] != MEASURED:
                continue
            o = opened.get(m["case_reference"])
            rd = d(m["registered_date"])
            if o and o <= rd and (rd - o).days <= days:
                continue
            keep.append(m)
        kr = [m for m in keep if m["case_reference"]]
        est = ix["recorded"] * len(keep) / len(kr)
        return est / ix["volume"] * 1e6
    def post_case():
        opened = {r["case_reference"]: d(r["notified_date"]) for r in reg}
        keep = [m for m in matches if m["member_code"] == SUBJECT and m["scheme_year"] == MEASURED
                and not (opened.get(m["case_reference"]) and d(m["registered_date"])
                         > opened[m["case_reference"]])]
        kr = [m for m in keep if m["case_reference"]]
        return ix["recorded"] * len(keep) / len(kr) / ix["volume"] * 1e6
    lad = figures["ladder"]
    ok("rung 0 reproduces", abs(naive() - lad["rung0_all_matches"]) < 5e-4, "%.3f" % naive())
    ok("rung 1 reproduces", abs(window(14) - lad["rung1_fortnight_window"]) < 5e-4, "%.3f" % window(14))
    ok("rung 2 reproduces", abs(post_case() - lad["rung2_all_post_case"]) < 5e-4, "%.3f" % post_case())
    ok("the recorded register rate reproduces",
       abs(ix["recorded"] / ix["volume"] * 1e6 - lad["recorded_register_rate"]) < 5e-4,
       "%.3f" % (ix["recorded"] / ix["volume"] * 1e6))
    printed = {round(v) for v in lad.values()}
    ok("every rung prints its own figure", len(printed) == len(lad), sorted(printed))
    for k, v in lad.items():
        if k == "golden":
            continue
        ok("rung %s is at least 6 per cent from the golden" % k,
           abs(v - ix["rate"]) / ix["rate"] >= 0.06,
           "%.1f per cent" % (100 * abs(v - ix["rate"]) / ix["rate"]))
    n1, n2, m2 = ix["recorded"], ix["independent"], ix["both"]
    fam = {"petersen": n1 * n2 / m2, "chapman": (n1 + 1) * (n2 + 1) / (m2 + 1) - 1,
           "bailey": n1 * (n2 + 1) / (m2 + 1),
           "continuity corrected": (n1 + 0.5) * (n2 + 0.5) / (m2 + 0.5) - 0.5,
           "conditional maximum likelihood": float(int(n1 * n2 / m2))}
    ok("every licensed estimator form prints the golden integer",
       {round(v / ix["volume"] * 1e6) for v in fam.values()} == {ix["index"]},
       ", ".join("%s %.3f" % (k, v / ix["volume"] * 1e6) for k, v in sorted(fam.items())))
    for k, v in fam.items():
        want = figures["estimator_family"][k]
        ok("the estimator family's %s reproduces" % k, abs(v - want["cases"]) < 5e-3,
           "%.3f cases" % v)
    ok("the observed union is not the golden",
       round((n1 + n2 - m2) / ix["volume"] * 1e6) != ix["index"],
       "%d cases" % (n1 + n2 - m2))
    sweep = {w: window(w) for w in range(0, 121)}
    ok("no named date window prints the golden integer",
       all(round(sweep[w]) != ix["index"] for w in NAMED_WINDOWS),
       "named windows print %s" % sorted({round(sweep[w]) for w in NAMED_WINDOWS}))
    hitting = [w for w in sweep if round(sweep[w]) == ix["index"]]
    ok("at most one unnamed window reaches the golden integer",
       len(hitting) <= 1 and not (set(hitting) & set(NAMED_WINDOWS)), "windows %s" % (hitting or "none"))

    print("\n-- the attribution and the conventions")
    req_pairs = []
    for r in requests:
        for m in matches:
            if m["case_reference"] and m["case_reference"] == r["case_reference"]:
                req_pairs.append((r["request_sent_date"], m["registered_date"]))
    ok("no registration shares its date with the request that produced it",
       not [1 for a, b in req_pairs if a == b], "%d request and registration pairs" % len(req_pairs))
    accounts = {norm_account(r["beneficiary_account"]) for r in register}
    ok("every matched account is on the register under the filed normalisation",
       all(norm_account(m["beneficiary_account_ref"]) in accounts for m in matches),
       "%d matches" % len(matches))
    raw = {r["beneficiary_account"] for r in register}
    ok("a raw string join misses rows, which is why the note files the handling",
       sum(1 for m in matches if m["beneficiary_account_ref"] in raw) < len(matches) * 0.95,
       "%d of %d match raw" % (sum(1 for m in matches if m["beneficiary_account_ref"] in raw),
                               len(matches)))
    ok("the standard files the estimand's five parts",
       all(p in std for p in ("arising from payments its own customers sent in the scheme year ended "
                              "31 March", "whether or not the member's own systems recorded them",
                              "counted once a case however many payments it covers",
                              "per million payments sent as reported on the member's revised quarterly "
                              "returns", "being the members' case registers and the scheme's "
                              "beneficiary account register")), "clause 4.2 carries all five")
    ok("the standard files the index year and the rounding",
       "beginning on the following 1 October" in std
       and "to the nearest whole case per million payments sent" in std, "clauses 4.3 and 4.4")
    leaky = re.compile(r"independen|capture|recapture|two.source|Petersen|Chapman|Bailey|self.produced"
                       r"|cannot have|attribut|detection coverage|sighting|overlap", re.I)
    for name, body in (("standard", std), ("trustee pack", pack_txt), ("feed notes", notes)):
        hits = sorted(set(x.group(0).lower() for x in leaky.finditer(body)))
        ok("no shipped document names the decisive step (%s)" % name, not hits,
           ", ".join(hits) or "clean")

    # --- the readings a judge reaches for, each closed on the shipped bytes -----------
    print("\n-- the request gap, the standing register and the evidence date")
    mine = [m for m in matches if m["member_code"] == SUBJECT and m["scheme_year"] == MEASURED]
    req = {}
    for r in requests:
        if r["member_code"] == SUBJECT and r["case_reference"]:
            req.setdefault(r["case_reference"], []).append(r["request_sent_date"])
    def first_request(m):
        ds = [s for s in req.get(m["case_reference"], []) if s]
        return min(ds) if ds else None
    def produced(m):
        return any(s and s <= m["registered_date"] for s in req.get(m["case_reference"], []))
    def est_of(keep):
        kr = [m for m in keep if m["case_reference"]]
        return len(recorded_rows) * len(keep) / len(kr) / ix["volume"] * 1e6
    recorded_rows = [r for r in reg if r["member_code"] == SUBJECT and r["scheme_year"] == MEASURED
                     and r["cover_class"] == "scam reimbursement"]
    leads = []
    for m in mine:
        rq = first_request(m)
        if rq and m["registered_date"] < rq:
            leads.append((d(rq) - d(m["registered_date"])).days)
    ok("no independent registration sits inside the request gap", leads and min(leads) >= 22,
       "closest is %d days ahead of the request" % (min(leads) if leads else -1))
    ok("the one-to-five-day band ahead of a request is empty",
       not [x for x in leads if x <= 5], "%d in the band" % len([x for x in leads if x <= 5]))
    for lead in (1, 2, 3, 5, 7, 14, 21):
        keep = [m for m in mine if not (first_request(m) and m["registered_date"]
                                        >= (d(first_request(m)) - dt.timedelta(days=lead)).isoformat())]
        r_ = est_of(keep)
        ok("a %d-day request window is the same call" % lead, round(r_) == ix["index"],
           "%.3f prints %d" % (r_, round(r_)))
    prepay = [m for m in mine if m["registered_date"] < m["payment_date"]]
    ok("registrations that predate their payment are a real body", len(prepay) >= 60,
       "%d rows" % len(prepay))
    indep = [m for m in mine if not produced(m)]
    pre_rec = len([m for m in prepay if m["case_reference"] and not produced(m)])
    pre_un = len([m for m in prepay if not m["case_reference"] and not produced(m)])
    b_ = len([m for m in indep if m["case_reference"]])
    sh_rec, sh_un = pre_rec / b_, pre_un / (len(indep) - b_)
    ok("the pre-payment share is the same on both sides of the overlap", abs(sh_rec - sh_un) < 0.03,
       "%.3f against %.3f" % (sh_rec, sh_un))
    keep = [m for m in indep if m["registered_date"] >= m["payment_date"]]
    r_ = est_of(keep)
    ok("SF13 dropping every pre-payment registration is the same call", round(r_) == ix["index"],
       "%.3f prints %d" % (r_, round(r_)))
    keep = [m for m in indep if m["registered_date"] <= AS_OF.isoformat()]
    r_ = est_of(keep)
    ok("cutting the register at the scheme year end gives another figure", round(r_) != ix["index"],
       "%.3f prints %d" % (r_, round(r_)))
    ok("the standard dates the evidence base to the review", 
       "as it stands when the review is prepared" in std, "clause 4.2")
    ok("the pack dates the evidence base to the pull and names no feed change",
       "as pulled for this meeting on 2 July 2027" in pack_txt
       and "register feed change of February" not in pack_txt, "the pack agrees")
    ok("the feed note keeps the padding convention and carries no steer",
       "Pad the account number back to eight digits" in notes
       and "An account stays on the register" not in notes
       and "already on the register" not in notes
       and "the field is blank" not in notes, "the note reads as an operations note")
    manifest = open(os.path.join(TARGET, "export_manifest.csv"), encoding="utf-8").read()
    ok("no shipped file comments on what a source omits",
       "never recorded" not in manifest and "nobody has reported" not in manifest,
       "the manifest states coverage and not absence")
    reasons = {r["report_reason"] for r in register}
    ok("the register's report reasons vary as a real register's do", len(reasons) >= 3,
       "%d distinct reasons" % len(reasons))
    wren = [m for m in members if m["member_code"] == "KM-103"][0]
    ok("the tier a member is carried at names the review that set it",
       "held from the 2024 review" in wren["tier_basis"], wren["tier_basis"])

    print("\n-- the asks")
    det = sheet("settlement_advices_2026_27.xlsx", "advice detail")
    tier = {m["member_code"]: m["contribution_tier"] for m in members}
    a_fig = {}
    for r in det:
        if r["cover_class"] != "unauthorised fraud":
            continue
        y, mo = [int(x) for x in str(r["settlement_month"]).split("-")]
        q = (mo - 4) // 3 + 1 if mo >= 4 else (mo + 8) // 3 + 1
        q = {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[mo]
        k = "Q%d %s" % (q, tier[r["member_code"]])
        a_fig[k] = round(a_fig.get(k, 0.0) + float(r["indemnity_paid_gbp"]), 2)
    for q in (1, 2, 3, 4):
        a_fig["Q%d total" % q] = round(sum(a_fig.get("Q%d %s" % (q, t), 0.0) for t in "ABC"), 2)
    bad = [k for k, v in figures["ask_a_indemnity_unauthorised"].items()
           if abs(a_fig.get(k, 0.0) - v) > 0.011]
    ok("ask A reproduces from the advice detail", not bad,
       "%d figures, worst gap %.2f" % (len(a_fig),
                                       max(abs(a_fig.get(k, 0.0) - v) for k, v in
                                           figures["ask_a_indemnity_unauthorised"].items())))
    adv_total = {}
    for r in wbk:
        if r["cover_class"] != "unauthorised fraud":
            continue
        mo = int(str(r["settlement_month"]).split("-")[1])
        q = {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[mo]
        k = "Q%d %s" % (q, tier[r["member_code"]])
        adv_total[k] = round(adv_total.get(k, 0.0) + float(r["advice_total_gbp"]), 2)
    moved = [k for k in a_fig if k in adv_total and abs(adv_total[k] - a_fig[k]) > 0.011]
    ok("ask A's device moves the natural read outside the asking sentence's rounding",
       moved, "the advice totals differ from their own detail on %d figures, worst %.2f"
       % (len(moved), max([abs(adv_total[k] - a_fig[k]) for k in moved] or [0])))
    q1 = rows("notifications_2027_28_q1.csv")
    supp = rows("notifications_2027_28_q1_supplementary.csv")
    b_fig = {}
    for m in members:
        mine = [r for r in q1 + supp if r["member_code"] == m["member_code"]]
        b_fig["%s notified" % m["member_code"]] = len(mine)
        b_fig["%s value" % m["member_code"]] = round(sum(float(r["payment_amount_gbp"]) for r in mine))
    eq("ask B reproduces from both extracts", b_fig, figures["ask_b_q1_notifications"],
       "%d figures" % len(b_fig))
    main_only = {}
    for m in members:
        mine = [r for r in q1 if r["member_code"] == m["member_code"]]
        main_only["%s notified" % m["member_code"]] = len(mine)
        main_only["%s value" % m["member_code"]] = round(sum(float(r["payment_amount_gbp"])
                                                             for r in mine))
    short = [k for k in main_only if main_only[k] != b_fig[k]]
    ok("ask B's device moves every figure in the ask", len(short) == len(b_fig),
       "%d of %d figures understated by the main extract alone" % (len(short), len(b_fig)))
    q1_ret = sheet("member_quarterly_returns.xlsx", "return 2027-28 Q1")
    mism = [r["member_code"] for r in q1_ret
            if int(r["scam_cases_notified"]) != main_only["%s notified" % r["member_code"]]]
    ok("ask B's inconsistency is findable against the member return", len(mism) >= 8,
       "%d members' returns exceed the main extract's rows" % len(mism))
    closed_by = {}
    for r in reg:
        closed_by[r["case_reference"]] = r
    c_fig = {}
    for q in (1, 2, 3, 4):
        sel = [r for r in reg if r["cover_class"] == "scam reimbursement" and r["scheme_year"] == "2025/26"
               and r["closed_date"] and _q(d(r["closed_date"]), "2025/26") == q]
        reimb = sum(float(r["reimbursed_amount_gbp"]) for r in sel)
        refs = {r["case_reference"] for r in sel}
        for route in ROUTES:
            got = sum(float(l["credit_amount_gbp"]) for l in legs
                      if l["entry_type"] == "recovery credit" and l["recovery_route"] == route
                      and l["case_reference"] in refs)
            c_fig["Q%d %s" % (q, route)] = round(got / reimb * 100.0, 1) if reimb else 0.0
    # the route total covers the same four quarters the rows cover, which is what the ask pins
    sel = [r for r in reg if r["cover_class"] == "scam reimbursement" and r["scheme_year"] == "2025/26"
           and r["closed_date"] and _q(d(r["closed_date"]), "2025/26") is not None]
    reimb = sum(float(r["reimbursed_amount_gbp"]) for r in sel)
    refs = {r["case_reference"] for r in sel}
    for route in ROUTES:
        got = sum(float(l["credit_amount_gbp"]) for l in legs
                  if l["entry_type"] == "recovery credit" and l["recovery_route"] == route
                  and l["case_reference"] in refs)
        c_fig["year %s" % route] = round(got / reimb * 100.0, 1)
    badc = [k for k, v in figures["ask_c_recovery_share"].items() if abs(c_fig.get(k, -1) - v) > 0.051]
    ok("ask C reproduces from the case-level credits", not badc, "%d figures" % len(c_fig))
    stmt = rows("recovery_statement_2025_26.csv")
    stated = {}
    for r in stmt:
        q = int(r["quarter_closed"][1])
        stated["Q%d %s" % (q, r["recovery_route"])] = (float(r["recovered_stated_gbp"])
                                                       / float(r["reimbursed_in_quarter_gbp"]) * 100.0)
    gaps = {k: abs(stated[k] - c_fig[k]) for k in stated if "repatriation" in k}
    ok("ask C's device moves the natural read outside the stated rounding",
       all(v > 0.1 for v in gaps.values()),
       "repatriation understated by %s percentage points" % ", ".join("%.1f" % v
                                                                      for v in gaps.values()))

    # --- the two asks the judge could not reconcile ----------------------------------
    print("\n-- the asks reconcile on the basis their own sentence pins")
    # ask 6: the route total covers the same four quarters as the rows, so the quarters' own
    # numerators over the quarters' own denominators is the stated total
    num = {r: 0.0 for r in ROUTES}
    den = 0.0
    for q in (1, 2, 3, 4):
        sel = [r for r in reg if r["cover_class"] == "scam reimbursement"
               and r["scheme_year"] == "2025/26" and r["closed_date"]
               and _q(d(r["closed_date"]), "2025/26") == q]
        den += sum(float(r["reimbursed_amount_gbp"]) for r in sel)
        refs = {r["case_reference"] for r in sel}
        for route in ROUTES:
            num[route] += sum(float(l["credit_amount_gbp"]) for l in legs
                              if l["entry_type"] == "recovery credit" and l["recovery_route"] == route
                              and l["case_reference"] in refs)
    bad = [r for r in ROUTES if abs(round(num[r] / den * 100.0, 1) - c_fig["year %s" % r]) > 0.051]
    ok("ask 6's route totals reconcile with its own four quarters", not bad,
       "; ".join("%s %.1f" % (r, num[r] / den * 100.0) for r in ROUTES))
    # ask 4: the quarter total is taken from the unrounded tier amounts, which the ask pins, and on at
    # least one quarter that differs from adding the rounded tier figures, so the pin is load bearing
    diff = []
    for q in (1, 2, 3, 4):
        unrounded = round(sum(a_fig["Q%d %s" % (q, t)] for t in "ABC"))
        rounded = sum(round(a_fig["Q%d %s" % (q, t)]) for t in "ABC")
        if unrounded != rounded:
            diff.append("Q%d %d against %d" % (q, unrounded, rounded))
        ok("ask 4's Q%d total is the unrounded tier amounts rounded once" % q,
           round(a_fig["Q%d total" % q]) == unrounded,
           "%d" % unrounded)
    ok("ask 4's rounding basis changes at least one quarter total, so the ask pins it", diff,
       "; ".join(diff) or "no quarter differs")

    print("\n-- the gates")
    files = sorted(os.listdir(TARGET))
    ok("10 or more files", len(files) >= 10, "%d" % len(files))
    ok("3 or more formats", len({os.path.splitext(f)[1] for f in files}) >= 3,
       ", ".join(sorted({os.path.splitext(f)[1] for f in files})))
    big = max((sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8", errors="replace")) - 1, f)
              for f in files if f.endswith(".csv"))
    ok("a file of 25,000 rows or more", big[0] >= 25000, "%s, %d rows" % (big[1], big[0]))
    md = json.load(open(os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    ok("two or more distractors declared", len(md["distractor_files"]) >= 2,
       "%d" % len(md["distractor_files"]))
    ok("the committed answer in metadata.json matches the index",
       str(ix["index"]) in md["committed_answer"] and str(round(ix["estimate"])) in md["committed_answer"],
       md["committed_answer"][:80] + "...")

    print("\n%d checks, %d PASS, %d FAIL" % (len(PASS) + len(FAIL), len(PASS), len(FAIL)))
    return 1 if FAIL else 0


def leaky_dic():
    return re.compile(r"independen|capture|recapture|two.source|Petersen|Chapman|Bailey|self.produced"
                      r"|cannot have|attribut|detection coverage|sighting|overlap", re.I)


def _q(day, year):
    a = int(year.split("/")[0])
    for i, (lo, hi) in enumerate([(dt.date(a, 4, 1), dt.date(a, 6, 30)),
                                  (dt.date(a, 7, 1), dt.date(a, 9, 30)),
                                  (dt.date(a, 10, 1), dt.date(a, 12, 31)),
                                  (dt.date(a + 1, 1, 1), dt.date(a + 1, 3, 31))]):
        if lo <= day <= hi:
            return i + 1
    return None


if __name__ == "__main__":
    sys.exit(main())
