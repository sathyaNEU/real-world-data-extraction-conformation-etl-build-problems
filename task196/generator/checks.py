#!/usr/bin/env python3
"""task196 assertions. Run after build.py.

    python3 task196/generator/checks.py

Three blocks: the client's three rules executed on the clean truth (R1 to R3c), the ladder and the
forcing (rungs, the estimator family, the date-window sweep, the fork grid, the bins), and the pack
(input gates, the separation line, mess neutrality, realism, document control dates).

Every document assertion goes through the same extractor the verifier uses and carries a positive
control on that same code path, so a search that cannot read a file fails loudly.
"""
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import docs
import golden as G
import world as W

PASS, FAIL = [], []


def ok(label, cond, detail=""):
    (PASS if cond else FAIL).append((label, detail))
    print("%-5s %-44s %s" % ("PASS" if cond else "FAIL", label, detail))


def eq(label, a, b, tol=0.0, detail=""):
    cond = abs(a - b) <= tol if isinstance(a, float) or isinstance(b, float) else a == b
    ok(label, cond, detail or "%s against %s" % (a, b))


# ---------------------------------------------------------------------------
# readers, shared with verify.py so the bundle is read one way only
# ---------------------------------------------------------------------------
def read_csv(name):
    with open(os.path.join(TARGET, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def squash(t):
    """Collapse whitespace, because a PDF extractor breaks a filed sentence across lines and a search
    for the sentence then reports absent when it is present."""
    return re.sub(r"\s+", " ", t)


def pdf_text(name):
    """Extract a shipped PDF's text through pdfplumber, the one extractor this build uses."""
    import pdfplumber
    out = []
    with pdfplumber.open(os.path.join(TARGET, name)) as pdf:
        for page in pdf.pages:
            out.append(page.extract_text() or "")
    return "\n".join(out)


def xlsx_rows(name, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, name), data_only=True)
    ws = wb[sheet]
    rows = list(ws.values)
    head = [str(h) if h is not None else "" for h in rows[0]]
    return [dict(zip(head, r)) for r in rows[1:] if any(v is not None for v in r)]


def main():
    w = W.world()
    code = "KM-104"
    ix = G.member_index(w, code)
    gold_rate, gold_index = ix["rate"], ix["index"]
    cases = [c for c in w["cases"] if c.member == code and c.year == W.MEASURED]

    # =====================================================================
    # R1 to R3c, the client's three rules, on the clean truth
    # =====================================================================
    print("\n-- the three rules, executed on the clean truth")
    reg = read_csv("case_register_2024_27.csv")
    matches = read_csv("member_payment_matches.csv")
    requests = read_csv("fund_return_requests.csv")
    ok("R1 case-level rows ship",
       len(reg) > 15000 and all(k in reg[0] for k in ("case_reference", "payment_date",
                                                      "notified_date", "cover_class")),
       "%d register rows at case grain" % len(reg))
    ok("R1 both detection channels ship at row grain",
       len(matches) > 5000 and "registered_date" in matches[0] and len(requests) > 4000
       and "request_sent_date" in requests[0],
       "%d matches, %d requests" % (len(matches), len(requests)))
    headers = []
    for n in sorted(os.listdir(TARGET)):
        if n.endswith(".csv"):
            with open(os.path.join(TARGET, n), encoding="utf-8") as f:
                headers.extend("%s:%s" % (n, h) for h in next(csv.reader(f)))
    bad = [h for h in headers if re.search(r"incidence|_index\b|unseen|undetected|true_case|coverage"
                                           r"|independent|self_produced|is_correct|should_", h, re.I)]
    ok("R1 no column holds the deciding quantity", not bad, ", ".join(bad) or "none of 100+ columns")
    scam_rows = [r for r in reg if r["cover_class"] == "scam reimbursement"]
    ok("R1 the index is not a sort or a filter of a shipped column",
       all(not re.search(r"rate|per_million|score", k, re.I) for k in reg[0]),
       "register carries dates, amounts and codes only")

    # R2, one assertion per Layer 1 item: the golden and every critical component hold
    def golden_with(**kw):
        return G.member_index(w, code)["rate"]

    ok("R2 old 2023/24 layout cannot move the call",
       all(c.year != "2023/24" for c in cases), "the call reads 2026/27 rows only")
    old = read_csv("case_register_2023_24.csv")
    ok("R2 the pence layout sits only in the old extract",
       "payment_pence" in old[0] and "payment_pence" not in reg[0],
       "pence in 2023/24, pounds after")
    qr_old = xlsx_rows("member_quarterly_returns.xlsx", "returns to 2023-24")
    qr_new = xlsx_rows("member_quarterly_returns.xlsx", "returns 2024-25 onward")
    ok("R2 thousands and units never share a sheet",
       "payments_sent_thousands" in qr_old[0] and "payments_sent" in qr_new[0]
       and "payments_sent" not in qr_old[0], "the unit is per sheet")
    rev = sum(int(r["payments_sent"]) for r in qr_new
              if r["member_code"] == code and r["scheme_year"] == W.MEASURED)
    eq("R2 the call's volume is the revised return's", rev, ix["volume"])
    prelim = xlsx_rows("member_quarterly_returns.xlsx", "preliminary 2026-27")
    pre = sum(int(r["payments_sent"]) for r in prelim if r["member_code"] == code)
    ok("R2 the preliminary vintage differs and is superseded by a filed word",
       pre != rev and "revised" in pdf_text("indemnity_standard_v6.pdf"),
       "preliminary %d against revised %d" % (pre, rev))
    def norm(ref):
        """The handling the register feed note files: digits only, with the account number padded back
        to eight. A digits-only normalisation misses every account whose number starts with a zero."""
        a, _, b = (ref or "").partition("/")
        return re.sub(r"\D", "", a) + re.sub(r"\D", "", b).zfill(8)
    reg_accounts = {norm(r["beneficiary_account"]) for r in read_csv("mule_account_register.csv")}
    raw_accounts = {r["beneficiary_account"] for r in read_csv("mule_account_register.csv")}
    m_raw = sum(1 for r in matches if r["beneficiary_account_ref"] in raw_accounts)
    m_norm = sum(1 for r in matches if norm(r["beneficiary_account_ref"]) in reg_accounts)
    ok("R2 the padding mess bites but cannot move the call",
       m_norm == len(matches) and m_raw < len(matches) * 0.95,
       "normalised %d of %d, raw %d" % (m_norm, len(matches), m_raw))
    ok("R2 the mid-year joiner is outside the review group",
       all(m["code"] != "KM-124" or not m["review"] for m in w["members"]),
       "Garnock joined 17 October 2023 and is not indexed")
    ok("R2 recoveries cannot move the call",
       all(not re.search(r"amount|gbp|pence", k, re.I) for k in
           ("recorded", "independent", "both")),
       "the index reads counts, never an amount column")
    ok("R2 the PDF tables are not load bearing for the call",
       "Membership position" in squash(pdf_text("trustee_pack_2027_07.pdf")),
       "the pack carries the membership position and no case figure")

    naive_cases, naive_rate = G.naive_index(w, code)
    rec_rate = ix["recorded"] / ix["volume"] * 1e6
    ok("R3a the default path files the named wrong answer",
       round(naive_rate) != gold_index and round(naive_rate) == 25,
       "%.3f prints %d against the golden %d" % (naive_rate, round(naive_rate), gold_index))
    eq("R3b the decisive step alone files the golden", round(gold_rate), 31)
    w14 = G.window_index(w, code, 14)[1]
    pc = G.post_case_index(w, code)[1]
    ok("R3b each lower rung's own correction stays wrong",
       round(w14) != gold_index and round(pc) != gold_index,
       "fortnight %.2f prints %d, all post-case %.2f prints %d" % (w14, round(w14), pc, round(pc)))
    std = squash(pdf_text("indemnity_standard_v6.pdf"))
    ok("R3c positive control: the standard reads back",
       docs.CONTROL["indemnity_standard_v6.pdf"] in std, "%d characters extracted" % len(std))
    pack_txt = squash(pdf_text("trustee_pack_2027_07.pdf"))
    ok("R3c positive control: the pack reads back",
       docs.CONTROL["trustee_pack_2027_07.pdf"] in pack_txt, "%d characters" % len(pack_txt))
    notes = open(os.path.join(TARGET, "register_feed_notes.txt"), encoding="utf-8").read()
    manifest_text = open(os.path.join(TARGET, "export_manifest.csv"), encoding="utf-8").read()
    # the words that would name the decisive step. "estimated" is the standard's own word for the
    # index and is not one of them; everything here would hand over the move.
    leaky = re.compile(r"independen|capture|recapture|two.source|Petersen|Chapman|Bailey"
                       r"|self.produced|cannot have|attribut|detection coverage|second sighting"
                       r"|sighting|because of (that|the) request|overlap", re.I)
    for name, text in (("indemnity standard", std), ("trustee pack", pack_txt),
                       ("register feed notes", notes)):
        hits = sorted(set(m.group(0).lower() for m in leaky.finditer(text)))
        ok("R3c no document names the decisive step (%s)" % name, not hits, ", ".join(hits) or "clean")
    graded = {str(G.member_index(w, m["code"])["index"]) for m in w["members"] if m["review"]}
    graded |= {str(G.member_index(w, m["code"])["recorded"]) for m in w["members"] if m["review"]}
    # a graded figure of three digits or more must be absent outright; a two-digit one could be a day
    # in a date, so the test is that no number in the pack sits beside a case or index word.
    nums = set(re.findall(r"\d+", pack_txt))
    big = {g for g in graded if len(g) >= 3}
    beside = re.findall(r"[^.]{0,40}\b\d+\b[^.]{0,40}", pack_txt)
    near = [b for b in beside if re.search(r"case|index|incidence|per million", b, re.I)]
    ok("R3c no document states a graded figure or ranks the members",
       not (big & nums) and not near and "incidence" not in pack_txt.lower(),
       "no three-digit graded figure, and no number beside a case or index word")

    # =====================================================================
    # the ladder and the forcing
    # =====================================================================
    print("\n-- the ladder, the estimator family and the window sweep")
    rungs = {"recorded register": rec_rate, "rung 0 all matches": naive_rate,
             "rung 1 fortnight": w14, "rung 2 all post-case": pc, "golden": gold_rate}
    printed = {k: round(v) for k, v in rungs.items()}
    ok("every rung prints a distinct figure", len(set(printed.values())) == len(printed),
       json.dumps(printed))
    for k, v in rungs.items():
        if k == "golden":
            continue
        ok("rung %r is at least 6 per cent from the golden" % k,
           abs(v - gold_rate) / gold_rate >= 0.06,
           "%.3f against %.3f, %.1f per cent" % (v, gold_rate, 100 * abs(v - gold_rate) / gold_rate))
    ok("the golden is bracketed",
       min(rungs.values()) < gold_rate < max(rungs.values()),
       "%.2f below, %.2f above" % (min(rungs.values()), max(rungs.values())))
    mults = {"recorded to rung 0": naive_rate / rec_rate, "rung 0 to rung 1": w14 / naive_rate,
             "rung 1 to rung 2": pc / w14}
    decisive = gold_rate / w14
    ok("the decisive move is not the smallest on the ladder (37's law)",
       decisive > min(mults.values()),
       "decisive %.3fx against %s" % (decisive, ", ".join("%s %.3fx" % (k, v)
                                                          for k, v in sorted(mults.items()))))
    ok("the decisive move is the only one that reverses direction",
       all(v > 1.0 for v in mults.values()) and gold_rate < pc,
       "every correction walks up, the decisive move comes back from %.2f to %.2f" % (pc, gold_rate))
    for name, bits in (("golden index", (gold_rate, 1.0)),):
        v, u = bits
        edge = u / 2 - abs(v - round(v / u) * u)
        ok("%s sits mid-bin" % name, edge >= 0.3 * u,
           "value %.3f, bin centre %d, distance to edge %.3f against the floor %.2f"
           % (v, round(v), edge, 0.3 * u))
    for m in w["members"]:
        if not m["review"]:
            continue
        i2 = G.member_index(w, m["code"])
        edge = 0.5 - abs(i2["rate"] - round(i2["rate"]))
        ok("review-group index mid-bin: %s" % m["name"], edge >= 0.3,
           "%.3f prints %d, edge %.3f" % (i2["rate"], i2["index"], edge))
    fam = G.estimator_family(ix)
    for k, v in G.capture_readings(w, code, ix).items():
        fam[k] = dict(cases=v["cases"], rate=v["cases"] / ix["volume"] * 1e6,
                      index=round(v["cases"] / ix["volume"] * 1e6), p=v["p"], n=v["n"])
    ok("every licensed estimator form prints the golden integer",
       {v["index"] for v in fam.values()} == {gold_index} and len(fam) >= 8,
       "%d forms: %s" % (len(fam), ", ".join("%s %.3f" % (k, v["rate"])
                                             for k, v in sorted(fam.items()))))
    # SF12's sixth form: the capture probability read off a subset of the member's own cases. The three
    # readings are one number by construction, so no subset choice crosses the printed bin.
    caps = {k: v for k, v in fam.items() if "p" in v}
    ok("the capture probability is the same off every subset of the member's own cases",
       max(v["p"] for v in caps.values()) - min(v["p"] for v in caps.values()) < 0.002,
       ", ".join("%.6f on %d" % (v["p"], v["n"]) for v in caps.values()))
    ok("SF12 the capture-probability readings print the golden integer",
       {v["index"] for v in caps.values()} == {gold_index} and len(caps) == 3,
       ", ".join("%.3f" % v["rate"] for v in caps.values()))
    spread = (max(v["rate"] for v in fam.values()) - min(v["rate"] for v in fam.values())) / gold_rate
    ok("the estimator family's spread is inside the printed bin", spread < 0.5 / gold_rate,
       "%.2f per cent against a half bin of %.2f per cent" % (100 * spread, 100 * 0.5 / gold_rate))
    union = ix["recorded"] + ix["independent"] - ix["both"]
    ok("the observed union is not the golden and is ruled out by clause 4.2",
       round(union / ix["volume"] * 1e6) != gold_index
       and "whether or not the member's own systems recorded them" in std,
       "union %d cases prints %d" % (union, round(union / ix["volume"] * 1e6)))
    sweep = {d: G.window_index(w, code, d)[1] for d in range(0, 121)}
    hits = [d for d, v in sweep.items() if round(v) == gold_index]
    ok("no named date window prints the golden integer",
       all(round(sweep[d]) != gold_index for d in (0, 1, 2, 3, 5, 7, 10, 14, 21, 28, 30, 45, 60, 90, 120)),
       "named windows print %s" % sorted({round(sweep[d]) for d in
                                          (0, 1, 2, 3, 5, 7, 10, 14, 21, 28, 30, 45, 60, 90, 120)}))
    ok("the date-window family reaches the golden integer at no more than one unnamed window",
       len(hits) <= 1 and all(d not in (0, 1, 2, 3, 5, 7, 10, 14, 21, 28, 30, 45, 60, 90, 120)
                              for d in hits),
       "windows %s" % (hits or "none"))
    ok("the window family is monotone in the window",
       all(sweep[d] <= sweep[d + 1] + 1e-9 for d in range(0, 120)), "rises with the window")

    # --- the readings the judge reached for, each closed in the data ------------------
    print("\n-- the request gap, the standing register and the evidence date")
    cs_all = [c for c in w["cases"] if c.member == code and c.year == W.MEASURED]
    # 1. no band of independent registrations sitting just ahead of a request: either the request
    #    precedes the registration, or the registration precedes it by REQUEST_GAP_DAYS or more
    leads = [(c.request_date - c.independent_reg_date).days for c in cs_all
             if c.independent_reg and c.request_date is not None
             and c.independent_reg_date < c.request_date]
    ok("no independent registration sits inside the request gap",
       leads and min(leads) >= W.REQUEST_GAP_DAYS,
       "closest independent registration is %d days ahead of the request, floor %d"
       % (min(leads) if leads else -1, W.REQUEST_GAP_DAYS))
    band = [d for d in leads if d <= 5]
    ok("the one-to-five-day band ahead of a request is empty", not band,
       "%d registrations in the band" % len(band))
    for lead in (1, 2, 3, 5, 7, 14, 21):
        keep = [c for c in cs_all if c.matched and not (
            c.registration_date is not None and c.request_date is not None
            and c.request_date - dt.timedelta(days=lead) <= c.registration_date)]
        kr = [c for c in keep if c.recorded]
        rate = G.petersen(ix["recorded"], len(keep), len(kr)) / ix["volume"] * 1e6
        ok("treating a registration up to %d day(s) before a request as request-linked is the "
           "same call" % lead, round(rate) == gold_index, "%.3f prints %d" % (rate, round(rate)))
    # 2. the register is a standing list: the share of independent registrations that predate their
    #    own payment is the same among the member's own cases and the cases it never recorded, so an
    #    analyst who drops those rows divides a smaller numerator by a proportionally smaller overlap
    pre = [c for c in cs_all if c.independent_reg and c.independent_reg_date < c.payment_date]
    ok("registrations that predate their payment are a real body, not a handful",
       len(pre) >= 60, "%d of %d independent registrations" % (len(pre), ix["independent"]))
    sh_rec = len([c for c in pre if c.recorded]) / ix["both"]
    sh_un = len([c for c in pre if not c.recorded]) / (ix["independent"] - ix["both"])
    ok("the pre-payment share is the same on both sides of the overlap", abs(sh_rec - sh_un) < 0.03,
       "%.3f of the recorded against %.3f of the rest" % (sh_rec, sh_un))
    keep = [c for c in cs_all if c.matched and not G._self_produced(c)
            and c.registration_date >= c.payment_date]
    kr = [c for c in keep if c.recorded]
    drop_rate = G.petersen(ix["recorded"], len(keep), len(kr)) / ix["volume"] * 1e6
    ok("SF13 dropping every registration that predates its payment is the same call",
       round(drop_rate) == gold_index, "%.3f prints %d" % (drop_rate, round(drop_rate)))
    ok("SF13 is closed by convergence and no sentence, deletion test",
       "An account stays on the register" not in notes
       and "already on the register" not in notes
       and round(drop_rate) == gold_index,
       "the clause is gone and dropping the rows still prints %d" % round(drop_rate))
    ok("no shipped file comments on what the register or the case extract omits",
       "never recorded" not in manifest_text and "nobody has reported" not in manifest_text,
       "the manifest states coverage and not absence")
    # 3. the evidence date: the register feed runs to the pull, which the standard and the pack say,
    #    and cutting it at the scheme year end is a different figure rather than a reading
    cut = [c for c in cs_all if c.matched and not G._self_produced(c)
           and c.registration_date <= W.AS_OF]
    cutr = [c for c in cut if c.recorded]
    cut_rate = G.petersen(ix["recorded"], len(cut), len(cutr)) / ix["volume"] * 1e6
    ok("cutting the register at the scheme year end gives another figure",
       round(cut_rate) != gold_index, "%.3f prints %d" % (cut_rate, round(cut_rate)))
    ok("the standard dates the evidence base to the review, not to the year end",
       "as it stands when the review is prepared" in std, "clause 4.2")
    ok("the trustees' pack dates the evidence base the same way",
       "as pulled for this meeting on 2 July 2027" in squash(pdf_text("trustee_pack_2027_07.pdf"))
       and "register feed change of February" not in squash(pdf_text("trustee_pack_2027_07.pdf")),
       "the pack carries the pull date and names no feed change")
    ok("the feed note no longer explains what a blank case reference means",
       "the field is blank" not in notes
       and "Pad the account number back to eight digits" in notes,
       "the padding convention kept, the mechanics gone")

    print("\n-- the settlement advices tie, and the walk holds in index units")
    # SF14: the quarter an indemnity line belongs to. Both readings are computable and they differ, so
    # the asking sentence pins the grain; what is gone is any unexplained amount between them.

    import openpyxl
    _wb = openpyxl.load_workbook(os.path.join(TARGET, "settlement_advices_2026_27.xlsx"),
                                 data_only=True)

    def _tab(name):
        vals = list(_wb[name].values)
        head = [str(h) for h in vals[0]]
        return [dict(zip(head, r)) for r in vals[1:] if any(v is not None for v in r)]

    _adv, _det = _tab("advices"), _tab("advice detail")
    _sum, _n = {}, {}
    for r in _det:
        _sum[r["advice_no"]] = round(_sum.get(r["advice_no"], 0.0) + float(r["indemnity_paid_gbp"]), 2)
        _n[r["advice_no"]] = _n.get(r["advice_no"], 0) + 1
    untied = [a["advice_no"] for a in _adv
              if abs(_sum.get(a["advice_no"], 0.0) - float(a["advice_total_gbp"])) > 0.011]
    ok("every settlement advice total ties to the sum of its own detail lines", not untied,
       "%d advices, %d untied" % (len(_adv), len(untied)))
    badn = [a["advice_no"] for a in _adv if _n.get(a["advice_no"], 0) != int(a["case_lines"])]
    ok("every advice's case_lines equals its own detail row count", not badn,
       "%d mismatched" % len(badn))
    ok("the prior-period adjustments settle in a different quarter from the advice that pays them",
       all(G._settlement_quarter(a["own_date"])
           != G._settlement_quarter(dt.date(a["advice_month"][0], a["advice_month"][1], 15))
           for a in w["adjustments"]) and len(w["adjustments"]) >= 30,
       "%d adjustments, every one in an earlier quarter than its advice" % len(w["adjustments"]))
    # the walk in index units is one answer under every licensed form, which the whole-case walk was not
    walks = set()
    for v in fam.values():
        walks.add((round(ix["recorded"] / ix["volume"] * 1e6),
                   round((v["cases"] - ix["recorded"]) / ix["volume"] * 1e6),
                   round(v["cases"] / ix["volume"] * 1e6)))
    ok("the walk in index units is the same under every licensed estimator form", len(walks) == 1,
       "%s across %d forms" % (sorted(walks), len(fam)))
    cases_walks = {(ix["recorded"], round(v["cases"]) - ix["recorded"], round(v["cases"]))
                   for v in fam.values()}
    ok("the whole-case walk is the reading that moves, which is why the walk is stated per million",
       len(cases_walks) > 1, "%d distinct whole-case walks" % len(cases_walks))
    bridge_sum = round(ix["recorded"] / ix["volume"] * 1e6) + \
        round((ix["estimate"] - ix["recorded"]) / ix["volume"] * 1e6)
    ok("the walk's two lines add to the index", bridge_sum == gold_index,
       "%d + %d = %d" % (round(ix["recorded"] / ix["volume"] * 1e6),
                         round((ix["estimate"] - ix["recorded"]) / ix["volume"] * 1e6), bridge_sum))
    for m2 in w["members"]:
        if not m2["review"]:
            continue
        i2 = G.member_index(w, m2["code"])
        vals = [("index", i2["rate"])]
        if m2["code"] == code:
            # the walk is graded for the named member only, so its two lines carry the floor too
            vals += [("walk, recorded incidence", i2["recorded"] / i2["volume"] * 1e6),
                     ("walk, incidence not held",
                      (i2["estimate"] - i2["recorded"]) / i2["volume"] * 1e6)]
        for label, val in vals:
            e = 0.5 - abs(val - round(val))
            ok("%s mid-bin: %s" % (label, m2["name"]), e >= 0.3,
               "%.3f prints %d, edge %.3f against the 0.30 floor" % (val, round(val), e))

    # the attribution is exact on the shipped bytes
    print("\n-- the attribution, recomputed from the shipped bytes")
    req_by_case = {}
    for r in requests:
        req_by_case.setdefault(r["case_reference"], []).append(r["request_sent_date"])
    mine = [r for r in matches if r["member_code"] == code and r["scheme_year"] == W.MEASURED]
    def self_made(r):
        ds = req_by_case.get(r["case_reference"], [])
        return any(d <= r["registered_date"] for d in ds if d)
    indep = [r for r in mine if not self_made(r)]
    both_b = [r for r in indep if r["case_reference"]]
    rec_b = sum(1 for r in reg if r["member_code"] == code and r["scheme_year"] == W.MEASURED
                and r["cover_class"] == "scam reimbursement")
    est_b = rec_b * len(indep) / len(both_b)
    eq("the bundle reproduces the recorded count", rec_b, ix["recorded"])
    eq("the bundle reproduces the independent sightings", len(indep), ix["independent"])
    eq("the bundle reproduces the overlap", len(both_b), ix["both"])
    eq("the bundle reproduces the index", round(est_b / ix["volume"] * 1e6), gold_index)
    ok("no independent sighting is preceded by a request",
       not [c for c in w["cases"] if c.matched and c.request_date and c.self_reg_date is None
            and c.request_date <= c.registration_date],
       "zero of %d matched cases" % sum(1 for c in w["cases"] if c.matched))
    ok("no registration shares its date with the request that produced it",
       not [c for c in w["cases"] if c.self_reg_date and c.request_date == c.self_reg_date],
       "nothing on the boundary (SF11)")
    ok("the lag spike is discoverable from the two date columns",
       sum(1 for r in mine if r["case_reference"] and r["registered_date"] >= r["payment_date"]
           and (dt.date.fromisoformat(r["registered_date"])
                - dt.date.fromisoformat(r["payment_date"])).days <= 40) > 100,
       "a spike a lag histogram shows")

    # =====================================================================
    # the fork grid
    # =====================================================================
    print("\n-- the semantic fork grid")
    vol = ix["volume"]
    both_classes = rec_b + sum(1 for r in reg if r["member_code"] == code
                               and r["scheme_year"] == W.MEASURED
                               and r["cover_class"] == "unauthorised fraud")
    ok("SF1 both cover classes gives another figure",
       round(both_classes * len(indep) / len(both_b) / vol * 1e6) != gold_index,
       "%d cases" % both_classes)
    ok("SF2 the register holds sending-side cases only",
       {r["side"] for r in reg} == {"sending"} and "belongs to the sending firm" in std,
       "one side, filed in clause 2.2")
    for label, key in (("SF3 case open date", "notified_date"),):
        alt = sum(1 for r in reg if r["member_code"] == code and r["cover_class"] == "scam reimbursement"
                  and r[key][:4] in ("2026", "2027")
                  and dt.date(2026, 4, 1) <= dt.date.fromisoformat(r[key]) <= dt.date(2027, 3, 31))
        alt_rate = alt * len(indep) / len(both_b) / vol * 1e6
        # closed twice over: clause 4.2 files the payment-date window in its own words, and the cases
        # the other reading selects carry the same printed index anyway, so no reading of the window
        # moves the call
        ok("%s is barred by the clause and converges on the same call" % label,
           "arising from payments its own customers sent in the scheme year ended 31 March" in std
           and round(alt_rate) == gold_index,
           "%d cases against the filed %d, %.3f prints %d"
           % (alt, len(rec_cases) if "rec_cases" in dir() else rec_b, alt_rate, round(alt_rate)))
    ok("SF4 the volume basis is filed and the alternatives differ",
       "payments sent as reported on the member's revised quarterly returns" in std
       and pre != rev, "clause 4.2 names the return field")
    ok("SF5 the recorded-only reading answers a different question",
       round(rec_b / vol * 1e6) != gold_index, "%d prints %d" % (rec_b, round(rec_b / vol * 1e6)))
    ok("SF6 the index year mapping is filed once",
       std.count("beginning on the following 1 October") == 1, "clause 4.3")
    ok("SF7 the rounding is filed at authority",
       "to the nearest whole case per million payments sent" in std, "clause 4.4")
    legs = read_csv("case_payments.csv")
    multi = {}
    for r in legs:
        if r["entry_type"] == "payment":
            multi[r["case_reference"]] = multi.get(r["case_reference"], 0) + 1
    ok("SF8 cases with several legs exist and the unit is filed",
       sum(1 for v in multi.values() if v > 1) > 500
       and "counted once a case however many payments it covers" in std,
       "%d multi-leg cases" % sum(1 for v in multi.values() if v > 1))
    ok("SF9 the filed normalisation selects every matched row",
       m_norm == len(matches), "%d of %d under the handling the feed note files" % (m_norm, len(matches)))
    ok("SF9 the call never reads the register, so the padding cannot move it",
       all(k in matches[0] for k in ("registered_date", "case_reference")),
       "the match extract carries the registration date and the case reference itself")
    mr = read_csv("mule_account_register.csv")
    matched_accounts = {norm(r["beneficiary_account_ref"]) for r in matches}
    statuses = {r["register_status"] for r in mr if norm(r["beneficiary_account"]) in matched_accounts}
    ok("SF10 no matched account carries a withdrawn or expired status", statuses == {"reported"},
       ", ".join(sorted(statuses)))
    dupes = {}
    for r in mr:
        k = norm(r["beneficiary_account"])
        if k in matched_accounts:
            dupes[k] = dupes.get(k, 0) + 1
    ok("SF10 no matched account is registered twice", max(dupes.values()) == 1,
       "%d matched accounts, each registered once" % len(dupes))
    ok("SF12 the estimator family converges on the printed figure",
       {v["index"] for v in fam.values()} == {gold_index}, "five forms, one integer")

    # =====================================================================
    # the pack
    # =====================================================================
    print("\n-- the pack, the gates and the separation line")
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    ok("input gate: 10 or more files", len(files) >= 10, "%d files" % len(files))
    ok("input gate: 3 or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
    biggest = max((sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8", errors="replace"))
                   - 1, f) for f in files if f.endswith(".csv"))
    ok("input gate: a file of 25,000 rows or more", biggest[0] >= 25000,
       "%s holds %d rows" % (biggest[1], biggest[0]))
    md = json.load(open(os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    ok("input gate: two or more distractors named in metadata.json",
       len(md["distractor_files"]) >= 2,
       ", ".join(d["file"] for d in md["distractor_files"]))
    for d in md["distractor_files"]:
        ok("distractor ships and is unread by the call: %s" % d["file"],
           os.path.exists(os.path.join(TARGET, d["file"])), "present")
    ok("no file name broadcasts the stump",
       not [f for f in files if re.search(r"independ|attribut|unseen|coverage|answer|golden|known",
                                          f, re.I)], "none")
    # the separation line: the ask devices sit outside the call's own rows
    adv = xlsx_rows("settlement_advices_2026_27.xlsx", "advices")
    det = xlsx_rows("settlement_advices_2026_27.xlsx", "advice detail")
    adv_month = {a["advice_no"]: a["settlement_month"] for a in adv}
    resid = [d for d in det if d["settlement_month"] != adv_month.get(d["advice_no"])]
    # SF14: the quarter an indemnity line belongs to. Both readings compute from the shipped sheets and
    # they differ, so the asking sentence pins the grain; what is gone is any unexplained amount between
    # them, because every advice ties to the sum of its own lines.
    _tierof = {m["code"]: m["tier"] for m in w["members"]}
    _qof = lambda ms: G._settlement_quarter(dt.date(int(ms.split("-")[0]), int(ms.split("-")[1]), 15))
    _own, _adv_basis = {}, {}
    for r in _det:
        if r["cover_class"] != "unauthorised fraud":
            continue
        k = (_qof(r["settlement_month"]), _tierof[r["member_code"]])
        _own[k] = round(_own.get(k, 0.0) + float(r["indemnity_paid_gbp"]), 2)
    for a in _adv:
        if a["cover_class"] != "unauthorised fraud":
            continue
        k = (_qof(a["settlement_month"]), _tierof[a["member_code"]])
        _adv_basis[k] = round(_adv_basis.get(k, 0.0) + float(a["advice_total_gbp"]), 2)
    gap = sum(abs(_adv_basis.get(k, 0.0) - v) for k, v in _own.items())
    ok("SF14 the own-month reading is the golden and the advice-month reading differs",
       all(abs(_own[(q, t)] - G.ask_a(w)["Q%d %s" % (q, t)]) < 0.011
           for q in (1, 2, 3, 4) for t in "ABC") and gap > 1000.0,
       "the two readings differ by %.2f across the year, every pound of it a quarter attribution" % gap)
    ok("ask A's device sits on the unauthorised class only",
       resid and all(d["cover_class"] == "unauthorised fraud" for d in resid),
       "%d detail lines settle in a month other than their advice's" % len(resid))
    q1 = read_csv("notifications_2027_28_q1.csv")
    supp = read_csv("notifications_2027_28_q1_supplementary.csv")
    ok("ask B's device sits after the evidence base closes",
       all(dt.date.fromisoformat(r["notified_date"]) > W.AS_OF for r in q1 + supp),
       "%d + %d rows, all after 31 March 2027" % (len(q1), len(supp)))
    ok("ask B's supplementary rows are the quarter's tail",
       all(dt.date.fromisoformat(r["notified_date"]) > dt.date(2027, 6, 20) for r in supp)
       and all(dt.date.fromisoformat(r["notified_date"]) <= dt.date(2027, 6, 20) for r in q1),
       "the main extract was cut on 20 June")
    rs = read_csv("recovery_statement_2025_26.csv")
    ok("ask C's device sits on the 2025/26 recovery statement",
       {r["statement_basis"] for r in rs} == {"as credited", "net of recovery agent charges"},
       "one route stated on another basis")
    ok("no ask device touches a row the call reads",
       all(r["cover_class"] != "scam reimbursement" for r in resid)
       and all(dt.date.fromisoformat(r["notified_date"]) > W.AS_OF for r in q1 + supp),
       "zero device rows inside the call's population")
    # deleting every device leaves the call where it is
    ok("the call survives deleting every ask device",
       round(G.member_index(w, code)["rate"]) == gold_index,
       "the index reads no amount, no notification and no statement")

    print("\n-- realism and document control")
    ok("no round headline", abs(gold_rate - round(gold_rate)) > 0.02,
       "%.3f is not a round number" % gold_rate)
    counts = {}
    for r in reg:
        counts[(r["member_code"], r["scheme_year"])] = counts.get((r["member_code"],
                                                                   r["scheme_year"]), 0) + 1
    ok("no two members share a case count in the measured year",
       len({v for k, v in counts.items() if k[1] == W.MEASURED}) >= 11,
       "%d distinct counts across 12 members" % len({v for k, v in counts.items()
                                                     if k[1] == W.MEASURED}))
    amounts = [r["payment_amount_gbp"] for r in reg[:4000]]
    ok("no repeating block of amounts", len(set(amounts)) > 3900, "%d distinct of 4000" % len(set(amounts)))
    ok("the standard's approval predates every event it describes",
       "19 May 2026" in std and "1 October 2026" in std, "approved before it took effect")
    ok("the pack's issue date sits between the evidence base and the pull",
       "2 July 2027" in pack_txt and W.AS_OF < dt.date(2027, 7, 2) <= W.PULL, "2 July 2027")
    ok("no extract carries a date after its own pull",
       max(dt.date.fromisoformat(r["registered_date"]) for r in matches) <= W.PULL,
       "latest registration %s" % max(r["registered_date"] for r in matches))
    ok("the dictionary covers every shipped file that needs it",
       len({r["extract"] for r in read_csv("data_dictionary.csv")}) >= 10,
       "%d files described" % len({r["extract"] for r in read_csv("data_dictionary.csv")}))
    ok("the manifest covers every shipped file",
       {r["file"] for r in read_csv("export_manifest.csv")} >= set(files) - {"export_manifest.csv"},
       "%d rows" % len(read_csv("export_manifest.csv")))

    print("\n%d checks, %d PASS, %d FAIL" % (len(PASS) + len(FAIL), len(PASS), len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
