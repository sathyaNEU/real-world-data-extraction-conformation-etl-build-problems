"""Rows of the pack's tables, rendered from the world the way each system writes them: the claims system's extract,
the triage screen's pilot register, the nurses' case log, Kellerman Pryce's verification rows, the segment crosswalk,
the payment register and the bank's ACH returns, and the pilot's worker survey."""
from __future__ import annotations

import datetime as dt

import common as K

EXTRACT_COLS = ["claim_no", "legacy_claim_no", "office", "segment", "class_code", "injury_date", "report_date",
                "disability_began", "time_off_at_report", "claim_type", "first_indemnity_date", "status", "closed_date",
                "reopened_date"]
NURSE_COLS = ["case_no", "claim_ref", "team", "nurse", "opened", "closed", "closure", "reopen"]
CROSS_COLS = ["legacy_code", "legacy_description", "new_code", "new_description", "effective"]
PAY_COLS = ["payment_no", "line", "claim_no", "benefit", "payee", "method", "check_or_trace", "issue_date",
            "period_from", "period_to", "amount", "status", "void_date"]
ACH_COLS = ["return_date", "orig_settlement_date", "trace_number", "amount", "return_code", "return_reason",
            "individual_id", "company_name"]
SURVEY_COLS = ["case_no", "sent", "returned", "q1_contact_prompt", "q2_explained_duties", "q3_employer_involved",
               "q4_overall", "back_at_work"]

TEAMS_OF = {"HC-SS": ["ERN 1", "ERN 2"], "HC-OT": ["ERN 2"], "RW-SS": ["ERN 3"], "RW-OT": ["ERN 3"],
            "MF-SS": ["ERN 4", "ERN 6"], "MF-OT": ["ERN 4"], "CN-SS": ["ERN 5", "ERN 6"], "CN-OT": ["ERN 5"]}
NURSES = {"ERN 1": ["DMR", "KLT"], "ERN 2": ["SBH", "PJW"], "ERN 3": ["ACN", "RGF"], "ERN 4": ["LWE", "MTS"],
          "ERN 5": ["JRP", "CAK"], "ERN 6": ["EHV", "NBO"]}


def iso(d):
    return d.isoformat() if d else ""


def us(d):
    return d.strftime("%m/%d/%Y") if d else ""


def extract_rows(W):
    """The claims system's listing at 30 September 2026: every claim reported since January 2021 whose first report
    recorded time lost or that has paid or reserved indemnity. Claims reported before the 2 June 2025 upgrade were
    converted with their legacy number; the conversion filled time_off_at_report from the legacy LOST_TIME indicator,
    which the legacy system set for any claim with lost time on record."""
    rows = []
    for c in W.claims:
        if not c.intake and c.dis_began > K.PULL_DATE:
            continue                     # a later conversion whose time lost has not begun is not on file yet
        converted = (c.report < K.UPGRADE and not c.native) or c.dup_of >= 0
        if c.dup_of >= 0:
            tor = "Y"
            ctype, first, status, closed, reo = "MO", None, "CLOSED", c.closed, None
        else:
            tor = "Y" if (converted or c.intake) else "N"
            ctype = "IND" if c.ind else "MO"
            first = c.first_ind if c.ind else None
            if c.reopened is not None:
                status = "REOPENED"
            elif c.closed is not None and c.closed <= K.PULL_DATE:
                status = "CLOSED"
            else:
                status = "OPEN"
            closed = c.closed if (c.closed is not None and c.closed <= K.PULL_DATE) else None
            reo = c.reopened
        rows.append(dict(claim_no=c.claim_no, legacy_claim_no=c.legacy_no if converted else "", office=c.office,
                         segment=c.seg, class_code=c.klass, injury_date=iso(c.injury), report_date=iso(c.report),
                         disability_began=iso(c.dis_began), time_off_at_report=tor, claim_type=ctype,
                         first_indemnity_date=iso(first) if first and first <= K.PULL_DATE else "", status=status,
                         closed_date=iso(closed), reopened_date=iso(reo)))
    rows.sort(key=lambda r: r["claim_no"])
    return rows


def register_rows(W):
    """The triage screen's pilot list: one row per pilot intake, in triage order."""
    cs = sorted([W.claims[i] for i in W.pilot_ids], key=lambda c: (c.triage, c.report, c.legacy_no))
    out = []
    for k, c in enumerate(cs):
        c.pref = "EP-%05d" % (k + 1)
        out.append((c.pref, c.legacy_no, c.office, K.LEGACY_OF_NEW[c.seg], c.report, c.triage,
                    "ERN" if c.arm == "E" else "Usual handling"))
    return out


def _typed(no, rg):
    """A claim number as a nurse typed it into the case system."""
    u = rg.random()
    if u < 0.04:
        return no.lower()
    if u < 0.07:
        head, tail = no.split("-")
        return "%s-%d" % (head, int(tail))
    if u < 0.09:
        return no.replace("-", " ")
    if u < 0.10:
        return no.replace("-", "")
    return no


def nurse_rows(W):
    rg = K.rng("nurse-log")
    cs = sorted([W.claims[i] for i in W.pilot_ids if W.claims[i].arm == "E"], key=lambda c: (c.triage, c.legacy_no))
    rows, seq = [], {}
    for c in cs:
        yr = c.triage.year % 100
        seq[yr] = seq.get(yr, 0) + 1
        case = "ERN-%02d-%04d" % (yr, seq[yr])
        teams = TEAMS_OF[c.seg]
        team = teams[0] if len(teams) == 1 or rg.random() < 0.7 else teams[1]
        nurse = NURSES[team][int(rg.integers(0, 2))]
        ref = _typed(c.legacy_no, rg)
        for j, (o, cl, n) in enumerate(c.files):
            if j == 0:
                closure = "Full duty"
                if c.ind and c.days_off > 150 and n < (c.dis_began + dt.timedelta(days=c.days_off) - c.triage).days:
                    closure = "MMI"
                elif c.ind and n < (c.dis_began + dt.timedelta(days=c.days_off) - c.triage).days - 3:
                    closure = "Back to adjuster"
            else:
                closure = "Full duty"
            rows.append(dict(case_no=case, claim_ref=ref, team=team, nurse=nurse, opened=us(o), closed=us(cl),
                             closure=closure, reopen="Y" if j else ""))
    return rows


# the review's workpaper section for each segment sheet, and how often each sheet's reviewer left a remark
WORKPAPER = {s: "B%d" % (i + 1) for i, s in enumerate(K.PROG)}
NOTE_RATE = {"HC-SS": 0.21, "HC-OT": 0.16, "RW-SS": 0.24, "RW-OT": 0.13, "MF-SS": 0.18, "MF-OT": 0.22, "CN-SS": 0.15,
             "CN-OT": 0.19}


def review_sheets(W):
    """Kellerman Pryce's verified rows by segment, both groups together and blind to group, in claim-number order. The
    reference is the workpaper section and the item number the file took when the segment's pooled files were worked,
    in an order that knows nothing of group."""
    out = {}
    for seg in K.PROG:
        ids = W.review[(seg, "E")] + W.review[(seg, "U")]
        cs = sorted([W.claims[i] for i in ids], key=lambda c: c.legacy_no)
        item = K.rng("review-refs", seg).permutation(len(cs)) + 1
        rows = []
        rg = K.rng("review-notes", seg)
        for k, c in enumerate(cs):
            st = "Open" if (c.closed is None or c.closed > K.VALUATION or (c.reopened and c.reopened <= K.VALUATION)) else "Closed"
            no = "%s-%s" % (c.legacy_no, K.check_digit(c.legacy_no))
            note = _note(c, rg, NOTE_RATE[seg])
            rows.append(("%s.%d" % (WORKPAPER[seg], int(item[k])), no, st, K.cents(c.ttd), K.cents(c.tpd),
                         K.cents(c.ppd), note or None))
        out[seg] = rows
    return out


def _d(d, u):
    """A date the way a reviewer jots it, one style a remark: 04/12/2024, 4/12/24 or 4/12/2024."""
    if u < 0.45:
        return d.strftime("%m/%d/%Y")
    if u < 0.8:
        return "%d/%d/%02d" % (d.month, d.day, d.year % 100)
    return "%d/%d/%d" % (d.month, d.day, d.year)


def _note(c, rg, rate):
    """A verifier's remark where the file needed one, in the reviewers' own shorthand, with the claim's own facts."""
    if rg.random() > rate:
        return ""
    style = rg.random()
    back = c.dis_began + dt.timedelta(days=c.days_off)
    is_open = c.closed is None or c.closed > K.VALUATION or bool(c.reopened and c.reopened <= K.VALUATION)
    weeks = c.ppd / max(c.ppd_rate, 1.0)
    opts = []
    if c.ttd > 0:
        opts += [lambda: "AWW recomputed from 13-wk wage stmt, $%.2f" % c.aww,
                 lambda: "AWW $%s per employer wage statement" % format(c.aww, ",.2f"),
                 lambda: "aww %.2f agrees to wage stmt (13 wks)" % c.aww,
                 lambda: "TTD through %s confirmed to RTW slip" % _d(back, style),
                 lambda: "Rate corrected to $%.2f/wk, arrears paid" % c.ttd_rate,
                 lambda: "TTD rate $%.2f checked to MO max for DOI %s" % (c.ttd_rate, _d(c.injury, style)),
                 lambda: "Off work %d days, TTD paid to RTW" % c.days_off,
                 lambda: "TTD %s to %s per work status reports" % (_d(c.dis_began, style), _d(back, style))]
        if c.ttd_rate + 0.005 < c.aww * 2 / 3:
            opts.append(lambda: "Comp rate at MO max, $%.2f" % c.ttd_rate)
        else:
            opts.append(lambda: "Comp rate 2/3 of AWW = $%.2f" % c.ttd_rate)
        if c.tpd > 0:
            opts.append(lambda: "RTW %s at reduced hours per treating MD" % _d(back, style))
        else:
            opts.append(lambda: "RTW full duty %s per treating MD, TTD period agrees" % _d(back, style))
        if c.days_off > 14:
            opts += [lambda: "Waiting period paid after day 14 (%d days)" % c.days_off,
                     lambda: "3-day wait paid back, off %d days" % c.days_off]
    if c.ppd > 0:
        opts += [lambda: "PPD %.1f wks per stipulation" % weeks,
                 lambda: "PPD rating per treating physician, %.1f wks" % weeks,
                 lambda: "%.1f wks PPD agrees to award" % weeks,
                 lambda: "PPD %.1f wks x $%.2f" % (weeks, c.ppd_rate)]
        if c.ppd_award is not None:
            appr = c.ppd_award + dt.timedelta(days=21)
            opts += [lambda: "Settlement approved by ALJ %s" % _d(appr, style),
                     lambda: "Stip for compromise approved %s, %.1f wks" % (_d(appr, style), weeks)]
            if c.ppd_lump and c.ppd_atty:
                opts.append(lambda: "Atty fee 25%% taken from PPD lump sum, $%s" % format(round(c.ppd * 0.25, 2), ",.2f"))
            elif not c.ppd_lump:
                opts.append(lambda: "PPD paid biweekly at $%.2f/wk" % c.ppd_rate)
    if c.tpd > 0:
        opts += [lambda: "TPD %d wks at reduced hours confirmed" % c.tpd_weeks,
                 lambda: "TPD %d wks, wage loss stmts on file" % c.tpd_weeks]
    if is_open:
        if c.ppd > 0:
            opts += [lambda: "Open at valuation: PPD rating pending",
                     lambda: "Open 6/30/26, rating outstanding; projected",
                     lambda: "Projected to ult. on %.1f wks PPD expected" % weeks]
        elif back > K.VALUATION:
            opts += [lambda: "Open at valuation: TTD continuing",
                     lambda: "Still off work at 6/30/26; projected",
                     lambda: "Open 6/30, projected on %d days off" % c.days_off]
        else:
            opts += [lambda: "RTW %s, open at valuation for final bills" % _d(back, style)]
    if not opts:
        return ""
    return opts[int(rg.integers(0, len(opts)))]()


def crosswalk_rows():
    rows = [dict(legacy_code=leg, legacy_description=name, new_code=new, new_description=name, effective="2025-06-02")
            for new, leg, name, _, _ in K.ALL_SEGMENTS]
    rows.append(dict(legacy_code="G9", legacy_description="Unassigned (pending segment review)", new_code="GN-AL",
                     new_description=K.NAME["GN-AL"], effective="2025-06-02"))
    rows.sort(key=lambda r: r["legacy_code"])
    return rows


def payment_rows(W):
    """One row per week a payment covers (a settlement, one row); each row carries the payment's amount."""
    rows = []
    for p in sorted(W.payments, key=lambda p: p["pno"]):
        for j, (a, b) in enumerate(p["lines"]):
            rows.append(dict(payment_no=p["pno"], line=j + 1, claim_no=p["claim_no"], benefit=p["benefit"],
                             payee=p["payee"], method=p["method"], check_or_trace=p["ref"], issue_date=iso(p["issue"]),
                             period_from=iso(a), period_to=iso(b), amount="%.2f" % p["amount"], status=p["status"],
                             void_date=iso(p["void"])))
    return rows


def ach_rows(W):
    rows = []
    for r in sorted(W.returns, key=lambda r: (r["rdate"], r["trace"])):
        rows.append(dict(return_date=r["rdate"].strftime("%Y%m%d"), orig_settlement_date=r["settle"].strftime("%Y%m%d"),
                         trace_number=r["trace"], amount="%.2f" % r["amount"], return_code=r["code"],
                         return_reason=r["reason"], individual_id=r["name_id"], company_name="HAVERLINE CAS WC"))
    return rows


def survey_rows(W):
    rows = []
    cases = _case_numbers(W)
    for s in W.survey:
        rows.append(dict(case_no=cases[s["cid"]], sent=us(s["sent"]), returned=us(s["back"]), q1_contact_prompt=s["q1"],
                         q2_explained_duties=s["q2"], q3_employer_involved=s["q3"], q4_overall=s["q4"],
                         back_at_work=s["rtw"]))
    rows.sort(key=lambda r: (r["sent"][6:] + r["sent"][:5], r["case_no"]))
    return rows


def _case_numbers(W):
    cs = sorted([W.claims[i] for i in W.pilot_ids if W.claims[i].arm == "E"], key=lambda c: (c.triage, c.legacy_no))
    seq, out = {}, {}
    for c in cs:
        yr = c.triage.year % 100
        seq[yr] = seq.get(yr, 0) + 1
        out[c.cid] = "ERN-%02d-%04d" % (yr, seq[yr])
    return out
