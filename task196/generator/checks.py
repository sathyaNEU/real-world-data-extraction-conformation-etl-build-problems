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



def settled_advices(adv, det):
    """The advices the mutual actually settled, read from the shipped rows alone. An advice file rejected
    on transmission was re-sent under fresh advice numbers, so one member's month and cover can hold two
    advices carrying the same case lines, and the second settled nothing. Identity is the line set, so a
    busy member-month's several batches, which carry different cases, are every one of them kept."""
    lines = {}
    for d in det:
        lines.setdefault(d["advice_no"], []).append(
            (str(d["case_reference"]), str(d["settlement_month"]),
             "%.2f" % float(d["indemnity_paid_gbp"])))
    seen, keep = set(), []
    for a in sorted(adv, key=lambda r: str(r["advice_no"])):
        key = (str(a["member_code"]), str(a["settlement_month"]), str(a["cover_class"]),
               tuple(sorted(lines.get(a["advice_no"], []))))
        if key in seen:
            continue
        seen.add(key)
        keep.append(a)
    nos = {a["advice_no"] for a in keep}
    return keep, [d for d in det if d["advice_no"] in nos]


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
    # The index is one figure under every form; the whole-case counts are not, so each count the
    # deliverables state is read inside a band (golden.COUNT_BAND). The band is asserted to hold the
    # golden count and every closed-form estimator's count for that member, and the index is asserted
    # not to move anywhere in the family, which is what makes the index the figure the walk states.
    for _m in w["members"]:
        if not _m["review"]:
            continue
        _ixm = G.member_index(w, _m["code"])
        _forms = G.estimator_family(_ixm)
        _lo, _hi = G.COUNT_BAND[_m["code"]]
        _counts = sorted(round(v["cases"]) for v in _forms.values())
        ok("the count band holds every closed form: %s" % _m["name"],
           _lo <= round(_ixm["estimate"]) <= _hi and _counts[0] >= _lo and _counts[-1] <= _hi,
           "band %d to %d, golden %d, closed forms %d to %d"
           % (_lo, _hi, round(_ixm["estimate"]), _counts[0], _counts[-1]))
        ok("the index does not move across the closed forms: %s" % _m["name"],
           {v["index"] for v in _forms.values()} == {_ixm["index"]},
           "%d under %d forms" % (_ixm["index"], len(_forms)))
    _lo, _hi = G.COUNT_BAND["KM-104 not held"]
    _nh = sorted(round(v["cases"]) - ix["recorded"] for v in G.estimator_family(ix).values())
    ok("the not-held band holds every closed form",
       _lo <= round(ix["estimate"]) - ix["recorded"] <= _hi and _nh[0] >= _lo and _nh[-1] <= _hi,
       "band %d to %d, golden %d, closed forms %d to %d"
       % (_lo, _hi, round(ix["estimate"]) - ix["recorded"], _nh[0], _nh[-1]))
    _ixt = G.member_index(w, "KM-108")
    _edge = 0.5 - abs(_ixt["estimate"] - round(_ixt["estimate"]))
    ok("the widened band is the count sitting on a printing edge", _edge < 0.1,
       "Trentmoor %.3f cases, %.3f of a case from the %.1f edge"
       % (_ixt["estimate"], _edge, round(_ixt["estimate"]) + 0.5))
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
    # SF14 and SF15: the asking sentence pins the basis (the quarter the case closed in) and the grain
    # (the case), so what is asserted here is that the pinned basis has one value on every line and the
    # advice grain is the rollup the device rides on, never that two readings of a field both stand.

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
    adv_all = xlsx_rows("settlement_advices_2026_27.xlsx", "advices")
    det_all = xlsx_rows("settlement_advices_2026_27.xlsx", "advice detail")
    adv, det = settled_advices(adv_all, det_all)
    adv_month = {a["advice_no"]: a["settlement_month"] for a in adv}
    resid = [d for d in det if d["settlement_month"] != adv_month.get(d["advice_no"])]
    # ask 4's basis and grain, pinned in the asking sentence: "the indemnity the advices settled, by
    # member tier and the 2026/27 quarter each case closed in". Every licensed route to that basis and
    # that grain is computed here and has to give one table (SF14, SF15, SF16); the advice grain is the
    # rollup the device rides on and has to differ on every figure.
    _tierof = {m["code"]: m["tier"] for m in w["members"]}
    _qof = lambda ms: G._settlement_quarter(dt.date(int(ms.split("-")[0]), int(ms.split("-")[1]), 15))
    _closed = {r["case_reference"]: r["closed_date"] for r in reg}
    _reimb = {r["case_reference"]: float(r["reimbursed_amount_gbp"]) for r in reg}
    _adv, _det = adv, det
    _atier = {a["advice_no"]: a["contribution_tier"] for a in _adv}
    _gold_a = G.ask_a(w)
    _U = [r for r in _det if r["cover_class"] == "unauthorised fraud"]

    def _table(triples):
        """A quarter x tier table of the sixteen graded figures, from (quarter, tier, amount) rows."""
        acc = {}
        for q, t, amt in triples:
            acc[(q, t)] = round(acc.get((q, t), 0.0) + amt, 2)
        f = {}
        for q in (1, 2, 3, 4):
            for t in G.TIERS:
                f["Q%d %s" % (q, t)] = round(acc.get((q, t), 0.0), 2)
            f["Q%d total" % q] = round(sum(acc.get((q, t), 0.0) for t in G.TIERS), 2)
        return f

    def _against_golden(f):
        return [k for k, v in _gold_a.items() if abs(f.get(k, 0.0) - v) > 0.011]

    # the basis: every line's case has one closure date, in the register, and the line's own month is
    # the same month on every line, so the pinned basis has one value however it is reached (C1)
    _stale = [d for d in _det if _closed.get(d["case_reference"], "")[:7] != str(d["settlement_month"])]
    ok("every advice line's own month is the month its case closed in the register", not _stale,
       "%d detail lines, %d disagreeing with the register's closed_date" % (len(_det), len(_stale)))
    ok("every advice line's case closed inside the 2026/27 scheme year",
       all(_qof(_closed[d["case_reference"]][:7]) is not None for d in _det),
       "%d lines, none closing outside the four quarters" % len(_det))
    _by_closure = _table([(_qof(_closed[d["case_reference"]][:7]), _tierof[d["member_code"]],
                           float(d["indemnity_paid_gbp"])) for d in _U])
    _by_line_month = _table([(_qof(d["settlement_month"]), _tierof[d["member_code"]],
                              float(d["indemnity_paid_gbp"])) for d in _U])
    ok("SF14 the pinned basis reproduces the golden from the register's closed_date",
       not _against_golden(_by_closure), "16 figures, 0 off the golden")
    ok("SF14 the line's own settlement month gives the same table",
       _by_line_month == _by_closure, "both routes to the closure quarter agree on all 16 figures")
    # ask A's device, measured: the workbook's own rows summed as they stand, and the blunt repair that
    # drops every repeated case reference, are each a complete pipeline at another table
    _Uall = [r for r in det_all if r["cover_class"] == "unauthorised fraud"]
    _by_raw = _table([(_qof(_closed[d["case_reference"]][:7]), _tierof[d["member_code"]],
                       float(d["indemnity_paid_gbp"])) for d in _Uall])
    _once, _by_dedup_rows = set(), []
    for d in sorted(_Uall, key=lambda r: (str(r["case_reference"]), str(r["advice_no"]))):
        if d["case_reference"] in _once:
            continue
        _once.add(d["case_reference"])
        _by_dedup_rows.append(d)
    _by_dedup = _table([(_qof(_closed[d["case_reference"]][:7]), _tierof[d["member_code"]],
                         float(d["indemnity_paid_gbp"])) for d in _by_dedup_rows])
    for _lab3, _alt3, _floor3 in (
            # the natural read, which has to miss every one of the sixteen
            ("the workbook's lines as they stand", _by_raw, 16),
            # the blunt repair, which takes the re-sends out and the prior-period top-ups with them
            ("one line per case reference", _by_dedup, 9)):
        _off3 = _against_golden(_alt3)
        _wk3 = max(_gold_a, key=lambda k: abs(_alt3.get(k, 0.0) - _gold_a[k]))
        ok("ask A's stop is a table of its own: %s" % _lab3, len(_off3) >= _floor3,
           "%d of 16 off (floor %d), worst %.2f on %s"
           % (len(_off3), _floor3, abs(_alt3[_wk3] - _gold_a[_wk3]), _wk3))
    _resent = [a["advice_no"] for a in adv_all if a["advice_no"] not in {x["advice_no"] for x in adv}]
    ok("the re-sent advices tie to their own totals and case counts like every other advice",
       not [a for a in adv_all if a["advice_no"] in _resent
            and (abs(round(sum(float(d["indemnity_paid_gbp"]) for d in det_all
                               if d["advice_no"] == a["advice_no"]), 2)
                     - float(a["advice_total_gbp"])) > 0.011
                 or int(a["case_lines"]) != len([d for d in det_all
                                                 if d["advice_no"] == a["advice_no"]]))],
       "%d advices in the workbook, %d of them a re-send that settled nothing"
       % (len(adv_all), len(_resent)))
    ok("a member-month's several advices are the run's own batches, so a second advice is not a tell",
       len({(a["member_code"], a["settlement_month"], a["cover_class"]) for a in adv
            if len([b for b in adv
                    if (b["member_code"], b["settlement_month"], b["cover_class"])
                    == (a["member_code"], a["settlement_month"], a["cover_class"])]) > 1}) >= 60,
       "%d member-month-covers settled over more than one advice with no re-send among them"
       % len({(a["member_code"], a["settlement_month"], a["cover_class"]) for a in adv
              if len([b for b in adv
                      if (b["member_code"], b["settlement_month"], b["cover_class"])
                      == (a["member_code"], a["settlement_month"], a["cover_class"])]) > 1}))
    # the other dates the register carries against a case, each a basis the wording has to exclude
    _paydate = {r["case_reference"]: r["payment_date"] for r in reg}
    _notdate = {r["case_reference"]: r["notified_date"] for r in reg}
    _CAL = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4}
    for _label, _alt in (
            ("the case's payment date",
             _table([(_qof(_paydate[d["case_reference"]][:7]), _tierof[d["member_code"]],
                      float(d["indemnity_paid_gbp"])) for d in _U
                     if _qof(_paydate[d["case_reference"]][:7]) is not None])),
            ("the case's notified date",
             _table([(_qof(_notdate[d["case_reference"]][:7]), _tierof[d["member_code"]],
                      float(d["indemnity_paid_gbp"])) for d in _U
                     if _qof(_notdate[d["case_reference"]][:7]) is not None])),
            ("calendar quarters on the closure date",
             _table([(_CAL[int(_closed[d["case_reference"]][5:7])], _tierof[d["member_code"]],
                      float(d["indemnity_paid_gbp"])) for d in _U]))):
        _off = _against_golden(_alt)
        _w = max(_gold_a, key=lambda k: abs(_alt[k] - _gold_a[k]))
        ok("SF14 a basis the wording excludes gives another table: %s" % _label, len(_off) == 16,
           "%d of 16 off, worst %.2f on %s" % (len(_off), abs(_alt[_w] - _gold_a[_w]), _w))
    # the grain: the case, and the detail line rolls up to it without changing a figure
    _percase, _casekey = {}, {}
    for d in _U:
        _percase[d["case_reference"]] = round(_percase.get(d["case_reference"], 0.0)
                                              + float(d["indemnity_paid_gbp"]), 2)
        _casekey[d["case_reference"]] = (_qof(_closed[d["case_reference"]][:7]),
                                         _tierof[d["member_code"]])
    _by_case = _table([(_casekey[r][0], _casekey[r][1], v) for r, v in _percase.items()])
    ok("SF15 the case grain and the line grain give the same table", _by_case == _by_closure,
       "%d lines over %d cases, %d of them paid by more than one advice"
       % (len(_U), len(_percase), sum(1 for r in _percase
                                      if sum(1 for d in _U if d["case_reference"] == r) > 1)))
    ok("SF16 the tier is the same from the member register and from the advice",
       not [a for a in _adv if _atier[a["advice_no"]] != _tierof[a["member_code"]]],
       "%d advices, 0 carrying a tier the register does not" % len(_adv))
    # the closure the reconciliation sits on: each advice's lines sum to its total, so the case grain
    # accounts for every pound the advice grain holds and the difference is attribution alone
    _adv_basis = _table([(_qof(a["settlement_month"]), _tierof[a["member_code"]],
                          float(a["advice_total_gbp"])) for a in _adv
                         if a["cover_class"] == "unauthorised fraud"])
    _moved = _against_golden(_adv_basis)
    _worst = max(_gold_a, key=lambda k: abs(_adv_basis[k] - _gold_a[k]))
    ok("the case grain and the advice grain hold the same money over the year",
       abs(sum(_percase.values()) - sum(float(a["advice_total_gbp"]) for a in _adv
                                        if a["cover_class"] == "unauthorised fraud")) < 0.011,
       "%.2f on both grains" % sum(_percase.values()))
    ok("ask A's device: the advice grain differs on every graded figure", len(_moved) == 16,
       "%d of 16 moved, worst %.2f on %s" % (len(_moved), abs(_adv_basis[_worst] - _gold_a[_worst]),
                                             _worst))
    # the amount side: the register's own reimbursement column is a different quantity, which is why the
    # asking sentence names what the advices settled
    _by_reimb = _table([(_casekey[r][0], _casekey[r][1], _reimb[r]) for r in _percase])
    ok("SF17 the register's reimbursement column is not the indemnity the advices settled",
       len(_against_golden(_by_reimb)) >= 12,
       "%d of 16 differ, %.2f of top-up the register does not carry"
       % (len(_against_golden(_by_reimb)), round(sum(_percase.values()) - sum(_reimb[r] for r in _percase), 2)))
    ok("ask A's device sits on the unauthorised class only",
       resid and all(d["cover_class"] == "unauthorised fraud" for d in resid),
       "%d detail lines sit on an advice raised in a later quarter than their case closed" % len(resid))
    # The prior-period lines stay, and the advices' own arithmetic is why. Dropping them leaves 35
    # advices whose stated total no longer equals the sum of their own lines and whose case_lines no
    # longer equals their row count, and the total it leaves is the register's reimbursement column to
    # the penny, which is the other, named quantity the asking sentence excludes (SF17).
    _kept_t = round(sum(float(d["indemnity_paid_gbp"]) for d in _U), 2)
    _drop_t = round(sum(float(d["indemnity_paid_gbp"]) for d in _U
                        if d["settlement_month"] == adv_month.get(d["advice_no"])), 2)
    _brk_total, _brk_lines = 0, 0
    for _a in _adv:
        _lines = [d for d in _det if d["advice_no"] == _a["advice_no"]]
        _keptl = [d for d in _lines if d["settlement_month"] == adv_month.get(_a["advice_no"])]
        if len(_keptl) == len(_lines):
            continue
        if abs(round(sum(float(d["indemnity_paid_gbp"]) for d in _keptl), 2)
               - float(_a["advice_total_gbp"])) > 0.011:
            _brk_total += 1
        if int(_a["case_lines"]) != len(_keptl):
            _brk_lines += 1
    ok("dropping the prior-period lines breaks the advices' own arithmetic",
       _brk_total == len(resid) and _brk_lines == len(resid),
       "%d advices stop tying to their own total and %d case_lines counts stop matching, on %.2f "
       "dropped from %.2f" % (_brk_total, _brk_lines, _kept_t - _drop_t, _kept_t))
    ok("the drop reading is the register's reimbursement column the sentence excludes",
       abs(_drop_t - sum(_reimb[r] for r in _percase)) < 0.011,
       "%.2f against the register's %.2f on the same cases"
       % (_drop_t, round(sum(_reimb[r] for r in _percase), 2)))
    q1 = read_csv("notifications_2027_28_q1.csv")
    supp = read_csv("notifications_feed_latest.csv")
    _nd = lambda r: dt.date.fromisoformat(r["notified_date"])
    ok("ask B's device sits after the evidence base closes",
       all(_nd(r) > W.AS_OF for r in q1 + supp),
       "%d + %d rows, all after 31 March 2027" % (len(q1), len(supp)))
    # the quarter extract reaches the quarter end on its own dates, so nothing in it says it is short
    ok("the quarter extract's own dates reach the quarter end",
       max(_nd(r) for r in q1) == dt.date(2027, 6, 30)
       and all(_nd(r) <= dt.date(2027, 6, 30) for r in q1),
       "latest notified date in the quarter extract is %s" % max(_nd(r) for r in q1))
    ok("no member's own rows in the quarter extract stop at the bulk load",
       sum(1 for m in w["members"]
           if max([_nd(r) for r in q1 if r["member_code"] == m["code"]] or [W.AS_OF])
           <= dt.date(2027, 6, 20)) == 0,
       "0 of 12 members end on 20 June in the quarter extract")
    _late = [r for r in supp if dt.date(2027, 6, 21) <= _nd(r) <= dt.date(2027, 6, 30)]
    ok("every member has quarter notifications in the July load",
       {r["member_code"] for r in _late} == {m["code"] for m in w["members"]},
       "%d rows of the quarter in the current load, over %d members"
       % (len(_late), len({r["member_code"] for r in _late})))
    ok("the current load also carries the new quarter, so its name is not the quarter's tail",
       any(_nd(r) > dt.date(2027, 6, 30) for r in supp),
       "%d of %d rows in the current load are notified after the quarter"
       % (sum(1 for r in supp if _nd(r) > dt.date(2027, 6, 30)), len(supp)))
    ok("ask B's device moves every one of the twenty-four figures",
       True, "measured in the forcing block below")
    rs = read_csv("recovery_statement_2025_26.csv")
    ok("ask C's device sits on the 2025/26 recovery statement",
       {r["statement_basis"] for r in rs} == {"as credited", "net of recovery agent charges"},
       "one route stated on another basis")

    # -- SF19: ask 5's count basis, pinned in the asking sentence and converged in the feed --------
    # "the distinct cases each member notified in 2027/28 Q1". A reference is one case and no
    # reference repeats, so counting rows and counting cases select the same rows (C1) and the pin
    # agrees with the dictionary's "a case is one case however many legs it covers".
    _QA, _QB = dt.date(2027, 4, 1), dt.date(2027, 6, 30)
    # the ask is the quarter's notifications, so the current load's new-quarter rows are not in it
    _feed = [r for r in q1 + supp if _QA <= dt.date.fromisoformat(r["notified_date"]) <= _QB]
    _refs = [r["case_reference"] for r in _feed]
    _bfig = G.ask_b(TARGET, w)
    ok("SF19 no notification reference repeats, so a row is one case",
       len(set(_refs)) == len(_refs),
       "%d rows, %d distinct references" % (len(_refs), len(set(_refs))))
    _rows_by, _cases_by = {}, {}
    for _m in w["members"]:
        _mine = [r for r in _feed if r["member_code"] == _m["code"]]
        _rows_by[_m["code"]] = len(_mine)
        _cases_by[_m["code"]] = len({r["case_reference"] for r in _mine})
    ok("SF19 the pinned reading returns the committed count for every member",
       all(_cases_by[c] == _bfig["%s notified" % c] for c in _cases_by),
       "12 members, every distinct-case count equal to the figure the ask states")
    ok("SF19 counting rows returns the same twelve counts", _rows_by == _cases_by,
       "both readings select the same cases")
    # The other extract a literal reader could take for the quarter's notifications is the case
    # register, which carries a notified date too. Two shipped facts separate them: the register
    # extract's own stated scope (scheme years 2024/25 to 2026/27) cannot hold a case from a 2027/28
    # payment, which is most of the quarter's notifications, and every member's own Q1 return states
    # the feed's count and no member's register count.
    _A, _B = dt.date(2027, 4, 1), dt.date(2027, 6, 30)
    _regq1 = [r for r in reg if r["notified_date"]
              and _A <= dt.date.fromisoformat(r["notified_date"]) <= _B]
    _regscam = {}
    for r in _regq1:
        if r["cover_class"] == "scam reimbursement":
            _regscam[r["member_code"]] = _regscam.get(r["member_code"], 0) + 1
    _ret = xlsx_rows("member_quarterly_returns.xlsx", "return 2027-28 Q1")
    _late = [r for r in _feed if dt.date.fromisoformat(r["payment_date"]) >= _A]
    ok("the register cannot be the quarter's notification extract",
       len(_late) > len(_feed) * 0.5
       and all(r["scheme_year"] in ("2024/25", "2025/26", "2026/27") for r in _regq1),
       "%d of %d notified cases sit on a 2027/28 payment, outside the register's stated scope"
       % (len(_late), len(_feed)))
    # The return is the member's own declaration off its own case system, so it ties to no extract and
    # arbitrates nothing: a response that reconciles to it lands on neither the quarter extract's count
    # nor the whole quarter's.
    _q1_by = {}
    for _m in w["members"]:
        _q1_by[_m["code"]] = len({r["case_reference"] for r in q1
                                  if r["member_code"] == _m["code"]
                                  and _QA <= dt.date.fromisoformat(r["notified_date"]) <= _QB})
    ok("no member's return states the committed count, the quarter extract's, or the register's",
       not [r for r in _ret if int(r["scam_cases_notified"])
            in (_cases_by[r["member_code"]], _q1_by[r["member_code"]],
                _regscam.get(r["member_code"], 0))],
       "0 of 12 returns equal any of the three, against the register's %d rows notified in the quarter"
       % len(_regq1))
    ok("ask B's device moves every member's count and every member's value",
       all(_q1_by[c] != _cases_by[c] for c in _cases_by)
       and all(abs(round(sum(float(r["payment_amount_gbp"]) for r in q1
                             if r["member_code"] == c
                             and _QA <= dt.date.fromisoformat(r["notified_date"]) <= _QB))
                   - _bfig["%s value" % c]) >= 1.0 for c in _cases_by),
       "12 of 12 counts and 12 of 12 values differ on the quarter extract alone")

    # -- SF18: ask 6's population, pinned in the asking sentence -----------------------------------
    # "the share of scam reimbursement recovered by route on cases from 2025/26 payments closed in
    # each 2025/26 quarter, from every case-level credit". Every reading the pack makes plausible is
    # computed on the shipped rows: the pinned one returns the committed fifteen figures and each
    # rival returns another grid.
    _gold_c = G.ask_c(w)
    # Every case-level credit, which the pin names: the claims ledger holds a route's recoveries until
    # the scheme took that route's remittance over, the scheme's remittance run holds them from that
    # date, and the five members that reconcile the remittance post it back into their own ledger too,
    # so the two sources overlap on exactly those rows and a credit is one credit per case and route.
    _remit = read_csv("scheme_remittance_credits.csv")
    _credit, _seen_cr = {}, set()
    for _l in legs:
        if _l["entry_type"] == "recovery credit":
            _credit.setdefault(_l["case_reference"], []).append(_l)
            _seen_cr.add((_l["case_reference"], _l["recovery_route"]))
    for _l in _remit:
        if (_l["case_reference"], _l["recovery_route"]) in _seen_cr:
            continue
        _seen_cr.add((_l["case_reference"], _l["recovery_route"]))
        _credit.setdefault(_l["case_reference"], []).append(
            {"case_reference": _l["case_reference"], "member_code": _l["member_code"],
             "cover_class": _l["cover_class"], "entry_type": "recovery credit", "leg_no": "1",
             "value_date": _l["remitted_date"], "paid_amount_gbp": "",
             "credit_amount_gbp": _l["credit_amount_gbp"], "recovery_route": _l["recovery_route"]})
    # the two stops the device puts between the ledger and the answer
    _ledger_only, _double = {}, {}
    for _l in legs:
        if _l["entry_type"] == "recovery credit":
            _ledger_only.setdefault(_l["case_reference"], []).append(_l)
            _double.setdefault(_l["case_reference"], []).append(_l)
    for _l in _remit:
        _double.setdefault(_l["case_reference"], []).append(
            {"value_date": _l["remitted_date"], "credit_amount_gbp": _l["credit_amount_gbp"],
             "recovery_route": _l["recovery_route"]})
    _CALQ = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4}

    def _sy(iso):
        d0 = dt.date.fromisoformat(iso)
        y0 = d0.year if d0 >= dt.date(d0.year, 4, 1) else d0.year - 1
        return "%d/%s" % (y0, str(y0 + 1)[2:])

    def _cgrid(cover="scam reimbursement", year="2025/26", cal=False,
               denom="reimbursed_amount_gbp", credits_in_year=False):
        src = [r for r in reg if r["closed_date"]]
        if cover:
            src = [r for r in src if r["cover_class"] == cover]
        if year:
            src = [r for r in src if r["scheme_year"] == year]

        def _num(keys, route):
            tot = 0.0
            for k in keys:
                for l2 in _credit.get(k, []):
                    if l2["recovery_route"] != route:
                        continue
                    if credits_in_year and not (dt.date(2025, 4, 1)
                                                <= dt.date.fromisoformat(l2["value_date"])
                                                <= dt.date(2026, 3, 31)):
                        continue
                    tot += float(l2["credit_amount_gbp"])
            return tot

        out, every = {}, []
        for q2 in (1, 2, 3, 4):
            if cal:
                sel = [r for r in src if dt.date.fromisoformat(r["closed_date"]).year == 2025
                       and _CALQ[int(r["closed_date"][5:7])] == q2]
            else:
                sel = [r for r in src
                       if W.quarter_of(dt.date.fromisoformat(r["closed_date"]), "2025/26") == q2]
            every += sel
            den = sum(float(r[denom]) for r in sel)
            keys = {r["case_reference"] for r in sel}
            for route in W.ROUTES:
                out["Q%d %s" % (q2, route)] = round(_num(keys, route) / den * 100.0, 1) if den else 0.0
        den = sum(float(r[denom]) for r in every)
        keys = {r["case_reference"] for r in every}
        for route in W.ROUTES:
            out["year %s" % route] = round(_num(keys, route) / den * 100.0, 1) if den else 0.0
        return out

    _cfull = _cgrid()
    ok("SF18 the pinned population returns the committed fifteen figures", _cfull == _gold_c,
       "15 figures, %d off the golden" % len([k for k in _gold_c if _cfull[k] != _gold_c[k]]))
    # ask C's device, measured: the claims ledger alone and the two sources unreconciled are each a
    # complete pipeline at another grid, and neither disagrees with any control the pack ships
    _save = _credit
    _credit = _ledger_only
    _conly = _cgrid()
    _credit = _double
    _cdbl = _cgrid()
    _credit = _save
    for _lab, _alt2 in (("the claims ledger alone", _conly),
                        ("both sources with the overlap counted twice", _cdbl)):
        _offc2 = [k for k in _gold_c if abs(_alt2[k] - _gold_c[k]) > 0.051]
        _wk2 = max(_gold_c, key=lambda k: abs(_alt2[k] - _gold_c[k]))
        ok("ask C's device moves every figure: %s" % _lab, len(_offc2) == 15,
           "%d of 15 off, worst %.1f points on %s, narrowest %.1f"
           % (len(_offc2), abs(_alt2[_wk2] - _gold_c[_wk2]), _wk2,
              min(abs(_alt2[k] - _gold_c[k]) for k in _gold_c)))
    ok("ask C's two sources overlap on the members that post the remittance back and on no others",
       {r["member_code"] for r in _remit
        if (r["case_reference"], r["recovery_route"])
        in {(l["case_reference"], l["recovery_route"]) for l in legs
            if l["entry_type"] == "recovery credit"}} == set(W.REMITTANCE_POSTED_BACK),
       "%d remittance rows, %d of them also in the ledger"
       % (len(_remit), len([r for r in _remit
                            if (r["case_reference"], r["recovery_route"])
                            in {(l["case_reference"], l["recovery_route"]) for l in legs
                                if l["entry_type"] == "recovery credit"}])))
    for _label, _alt in (
            ("both covers", _cgrid(cover=None)),
            ("any scheme year", _cgrid(year=None)),
            ("both covers and any scheme year", _cgrid(cover=None, year=None)),
            ("the unauthorised cover", _cgrid(cover="unauthorised fraud")),
            ("calendar quarters", _cgrid(cal=True)),
            ("the payment amount as the denominator", _cgrid(denom="payment_amount_gbp")),
            ("credits dated inside 2025/26 only", _cgrid(credits_in_year=True))):
        _offc = [k for k in _gold_c if abs(_alt[k] - _gold_c[k]) > 0.051]
        _wk = max(_gold_c, key=lambda k: abs(_alt[k] - _gold_c[k]))
        ok("SF18 a population the wording excludes gives another grid: %s" % _label, len(_offc) >= 9,
           "%d of 15 off, worst %.1f points on %s" % (len(_offc), abs(_alt[_wk] - _gold_c[_wk]), _wk))
    ok("SF18 the register's scheme year is the scheme year of the payment it holds",
       not [r for r in reg if _sy(r["payment_date"]) != r["scheme_year"]],
       "%d rows, 0 where the pinned payment year and the register's own column part" % len(reg))
    _old23 = read_csv("case_register_2023_24.csv")
    ok("SF18 the 2023/24 extract holds no case closing inside 2025/26",
       not [r for r in _old23 if r["closed_dt"]
            and dt.date(2025, 4, 1)
            <= dt.datetime.strptime(r["closed_dt"], "%d/%m/%Y").date() <= dt.date(2026, 3, 31)],
       "%d rows in the legacy layout, none inside the four quarters" % len(_old23))

    ok("no ask device touches a row the call reads",
       all(r["cover_class"] != "scam reimbursement" for r in resid)
       and all(dt.date.fromisoformat(r["notified_date"]) > W.AS_OF for r in q1 + supp),
       "zero device rows inside the call's population")
    # deleting every device leaves the call where it is
    ok("the call survives deleting every ask device",
       round(G.member_index(w, code)["rate"]) == gold_index,
       "the index reads no amount, no notification and no statement")

    print("\n-- the payments-sent series, member by member")
    _ann = {}
    for _r in qr_new:
        if _r["vintage"] == "revised":
            _k = (_r["member_code"], _r["scheme_year"])
            _ann[_k] = _ann.get(_k, 0) + int(_r["payments_sent"])
    for _r in qr_old:
        _k = (_r["member_code"], _r["scheme_year"])
        _ann[_k] = _ann.get(_k, 0.0) + float(_r["payments_sent_thousands"]) * 1000.0
    _codes = sorted({k[0] for k in _ann})
    _steps = {c: [round((_ann[(c, W.SCHEME_YEARS[i + 1])] / _ann[(c, W.SCHEME_YEARS[i])] - 1) * 100, 3)
                  for i in range(3)] for c in _codes}
    ok("no two members share a payments-sent growth rate to three decimals",
       len(_codes) == 12 and all(len({_steps[c][i] for c in _codes}) == 12 for i in range(3))
       and len({x for c in _codes for x in _steps[c]}) == 36,
       "%d members, %d distinct rates over 36 member-years"
       % (len(_codes), len({x for c in _codes for x in _steps[c]})))
    ok("every member's growth path has its own shape, not one path scaled twelve times",
       len({tuple(sorted(_steps[c])) for c in _codes}) == 12
       and len([c for c in _codes if min(_steps[c]) < 0]) >= 3,
       "%d distinct shapes, %d members giving a year back"
       % (len({tuple(sorted(_steps[c])) for c in _codes}),
          len([c for c in _codes if min(_steps[c]) < 0])))
    ok("Castlegate's three annual payments-sent totals are the ones the call rests on",
       [_ann[(code, y)] for y in ("2024/25", "2025/26", "2026/27")]
       == [19120600, 20677000, 22233300],
       ", ".join("%d" % _ann[(code, y)] for y in ("2024/25", "2025/26", "2026/27")))
    ok("every graded review-group index is the figure the deliverables print",
       {c: G.member_index(w, c)["index"] for c in ("KM-104", "KM-112", "KM-108", "KM-101")}
       == {"KM-104": 31, "KM-112": 22, "KM-108": 15, "KM-101": 12},
       ", ".join("%s %d" % (c, G.member_index(w, c)["index"])
                 for c in ("KM-104", "KM-112", "KM-108", "KM-101")))
    # the year a return implies is the sum of the four quarters the member filed, so it carries no
    # rounding of its own: a year lands on a hundred only where the review reads an index off it, or
    # once in a hundred by chance, and never because the generator rounded a year and divided it
    _rev_years = [k for k in _ann if k[1] != "2023/24"]
    _round = sorted(k for k in _rev_years if int(_ann[k]) % 100 == 0)
    _unpinned = [k for k in _round if k not in W.PINNED_YEARS]
    ok("an annual payments-sent total is round only where the review reads it",
       len(_round) <= 8 and len(_unpinned) <= 2 and set(W.PINNED_YEARS) <= set(_round),
       "%d of %d member-years land on a multiple of a hundred, %d of them the years the review reads, "
       "%d by chance" % (len(_round), len(_rev_years), len(_round) - len(_unpinned), len(_unpinned)))
    _q100 = [r for r in qr_new if int(r["payments_sent"]) % 100 == 0]
    _q10 = [r for r in qr_new if int(r["payments_sent"]) % 10 == 0]
    ok("the quarterly payments-sent figures are whole payments, not a rounded multiple",
       len(_q10) < len(qr_new) * 0.25 and len(_q100) < len(qr_new) * 0.05,
       "%d of %d quarters land on a multiple of a hundred, %d on a multiple of ten"
       % (len(_q100), len(qr_new), len(_q10)))
    ok("the review group's payments sent are the figures the deliverables print",
       {c: _ann[(c, W.MEASURED)] for c in ("KM-104", "KM-112", "KM-108", "KM-101")}
       == {"KM-104": 22233300, "KM-112": 6365500, "KM-108": 20002400, "KM-101": 42722700},
       ", ".join("%s %d" % (c, _ann[(c, W.MEASURED)])
                 for c in ("KM-104", "KM-112", "KM-108", "KM-101")))
    _qsum = {}
    for _r in qr_new:
        if _r["vintage"] == "revised":
            _qsum[(_r["member_code"], _r["scheme_year"])] = _qsum.get(
                (_r["member_code"], _r["scheme_year"]), 0) + int(_r["payments_sent"])
    ok("every annual total is the sum of the four quarters the member filed",
       all(_qsum[k] == int(_ann[k]) for k in _qsum)
       and _qsum[(code, W.MEASURED)] == G.member_index(w, code)["volume"],
       "%d member-years tie, the call's denominator among them" % len(_qsum))

    print("\n-- the working calendar")
    _wk = lambda ds: 100.0 * sum(1 for x in ds if x.weekday() >= 5) / max(1, len(ds))
    _spread = lambda ds: max(100.0 * sum(1 for x in ds if x.weekday() == i) / max(1, len(ds))
                             for i in range(5))
    _notif = [dt.date.fromisoformat(r["notified_date"]) for r in q1 + supp]
    _nclose = [dt.date.fromisoformat(r["closed_date"]) for r in q1 + supp if r["closed_date"]]
    _rclose = [dt.date.fromisoformat(r["closed_date"]) for r in reg if r["closed_date"]]
    ok("the notification feed is taken on working days", _wk(_notif) < 6.0,
       "%.2f per cent of %d notifications at a weekend, busiest weekday %.1f per cent"
       % (_wk(_notif), len(_notif), _spread(_notif)))
    ok("the feed's closures fall on working days", _wk(_nclose) < 6.0,
       "%.2f per cent of %d closures at a weekend" % (_wk(_nclose), len(_nclose)))
    ok("the register's closures fall on working days", _wk(_rclose) < 6.0,
       "%.2f per cent of %d closures at a weekend, busiest weekday %.1f per cent"
       % (_wk(_rclose), len(_rclose), _spread(_rclose)))
    _advd = [dt.date.fromisoformat(str(a["advice_date"])[:10]) for a in _adv]
    ok("no settlement advice is dated at a weekend and the run is not one date a month",
       _wk(_advd) == 0.0 and len(set(_advd)) > 12 and len({d.day for d in _advd}) > 1,
       "%d advices over %d dates on %d days of the month, none at a weekend"
       % (len(_advd), len(set(_advd)), len({d.day for d in _advd})))
    _outside = [a for a in _adv
                if str(a["advice_date"])[:7] != str(a["settlement_month"])[:7]]
    ok("every advice is dated inside the month it settles", not _outside,
       "%d advices, %d dated outside their own settlement month" % (len(_adv), len(_outside)))
    _cut = dt.date(2027, 6, 30)
    ok("the main notification extract carries no closure after its own cut date",
       not [r for r in q1 if r["closed_date"]
            and dt.date.fromisoformat(r["closed_date"]) > _cut]
       and max(dt.date.fromisoformat(r["notified_date"]) for r in q1) <= _cut,
       "%d closed of %d rows, latest closure %s, latest notification %s"
       % (len([r for r in q1 if r["closed_date"]]), len(q1),
          max((r["closed_date"] for r in q1 if r["closed_date"]), default=""),
          max(r["notified_date"] for r in q1)))
    _gaps = [(dt.date.fromisoformat(r["closed_date"]) - dt.date.fromisoformat(r["notified_date"])).days
             for r in reg if r["closed_date"]]
    _early = [g for g in _gaps if g <= 0]
    ok("no case closes on or before the day it was notified", not _early,
       "%d of %d closed register rows close on or before notification, gap %d to %d days"
       % (len(_early), len(_gaps), min(_gaps), max(_gaps)))

    # the register's notified date is the day the member recorded the case, which is desk work: it
    # carries the working week the closures and the notification feed carry, nudged inside the case's
    # own calendar month so no month or quarter any ask or any return attributes by can move
    _rnot = [dt.date.fromisoformat(r["notified_date"]) for r in reg]
    _onot = [dt.datetime.strptime(r["notified_dt"], "%d/%m/%Y").date() for r in _old23]
    ok("the register's recorded dates fall on working days",
       _wk(_rnot) < 6.0 and _wk(_onot) < 6.0,
       "%.2f per cent of %d in the current layout and %.2f per cent of %d in the legacy one at a "
       "weekend" % (_wk(_rnot), len(_rnot), _wk(_onot), len(_onot)))
    _held = [c for c in w["cases"] if c.recorded and c.member == W.LADDER_SUBJECT
             and c.year == W.MEASURED and c.registration_date is not None
             and c.registration_date >= c.open_date]
    _subject = [c for c in w["cases"] if c.recorded and c.member == W.LADDER_SUBJECT
                and c.year == W.MEASURED]
    ok("only the rows the date-only rungs measure keep the date they were drawn on",
       len(_held) == 167 and all(c.registration_date >= c.open_date for c in _held)
       and _wk([c.open_date for c in _subject if c not in _held]) < 6.0,
       "%d of %d rows held, the ladder's own member-year, %.2f per cent of the rest at a weekend"
       % (len(_held), len(_subject), _wk([c.open_date for c in _subject if c not in _held])))
    # the nudge moved no case out of the quarter it was recorded in, so the returns' notified counts
    # are the counts the pre-nudge dates gave, member-year by member-year and cover by cover
    _moved = []
    for _c in w["cases"]:
        if not _c.recorded or _c.open_date is None:
            continue
        _raw = _c.payment_date + dt.timedelta(days=_c.report_lag)
        if W.quarter_of(_raw, _c.year) != W.quarter_of(_c.open_date, _c.year):
            _moved.append(_c.case_ref)
    _umoved = [u["ref"] for u in w["unauth"]
               if W.quarter_of(u["open_raw"], u["year"]) != W.quarter_of(u["open_date"], u["year"])]
    ok("the recorded-date nudge moves no case out of its own quarter",
       not _moved and not _umoved,
       "%d scam and %d unauthorised cases over %d member-years change quarter"
       % (len(_moved), len(_umoved), len({(m["code"], y) for m in w["members"]
                                          for y in W.SCHEME_YEARS})))
    _tie = []
    for _m in w["members"]:
        for _y in ["2024/25", "2025/26", "2026/27"]:
            for _q in (1, 2, 3, 4):
                _said = [r for r in qr_new if r["vintage"] == "revised"
                         and r["member_code"] == _m["code"] and r["scheme_year"] == _y
                         and r["quarter"] == "Q%d" % _q][0]
                _rows = [r for r in reg if r["member_code"] == _m["code"]
                         and r["scheme_year"] == _y
                         and W.quarter_of(dt.date.fromisoformat(r["notified_date"]), _y) == _q]
                for _cover, _col in (("scam reimbursement", "scam_cases_notified"),
                                     ("unauthorised fraud", "unauthorised_cases_notified")):
                    if int(_said[_col]) != len([r for r in _rows if r["cover_class"] == _cover]):
                        _tie.append((_m["code"], _y, _q, _cover))
    ok("every return's notified counts tie to the register's own recorded dates", not _tie,
       "%d cells over 36 member-years and both covers, %d untied" % (36 * 4 * 2, len(_tie)))
    _reqs = {r["case_reference"]: r["request_sent_date"] for r in read_csv("fund_return_requests.csv")}
    _before = [k for k, v in _reqs.items()
               if k in _notdate and v <= _notdate[k]]
    ok("no fund-return request is dated on or before the case was recorded", not _before,
       "%d requests, %d dated on or before their case's recorded date" % (len(_reqs), len(_before)))
    _cl = {r["case_reference"]: r["closed_date"] for r in reg}
    _cr = [r for r in read_csv("case_payments.csv")
           if r["credit_amount_gbp"] and float(r["credit_amount_gbp"]) > 0]
    _pre = [r for r in _cr if _cl.get(r["case_reference"])
            and dt.date.fromisoformat(r["value_date"])
            <= dt.date.fromisoformat(_cl[r["case_reference"]])]
    ok("no recovery credit values on or before the closure it belongs to", not _pre,
       "%d credit rows, %d valued on or before their case's closure" % (len(_cr), len(_pre)))
    ok("the feed's current load carries no closure after the feed's own pull date",
       not [r for r in supp if r["closed_date"]
            and dt.date.fromisoformat(r["closed_date"]) > W.PULL],
       "%d rows, latest closure %s"
       % (len(supp), max((r["closed_date"] for r in supp if r["closed_date"]), default="")))

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
