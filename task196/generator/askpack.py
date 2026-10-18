"""The files the three device asks run on, plus the mutual's reference and provenance files.

Every row these writers produce sits outside the main call's declared population: the unauthorised-fraud
cover class, the quarter after the evidence base closes, the recovery statements and the contribution
reference files. The call reads no amount column at all, so every monetary quantity here is off its path.
"""
import csv
import datetime as dt
import os

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import pack
import world as W

def _adjustments_by_advice(w):
    """The prior-period adjustments keyed by the advice that carries them (world.build_adjustments)."""
    out = {}
    for a in w["adjustments"]:
        out.setdefault((a["member"], a["advice_month"], a["cover"]), []).append(a)
    return out


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)


def _d(d):
    return d.isoformat() if d else ""


def _run_days(yy, mm):
    """The mutual's monthly settlement run and the working days after it that are still inside the
    month. The run is dated the 25th and moves back to the preceding working day when the 25th falls at
    a weekend, because the run cannot settle on a day the payment system is shut; a member whose
    reconciliation comes in late is settled a working day or two behind the run."""
    d = dt.date(yy, mm, 25)
    while d.weekday() >= 5:
        d -= dt.timedelta(days=1)
    last = (dt.date(yy, mm, 1) + dt.timedelta(days=31)).replace(day=1) - dt.timedelta(days=1)
    out = []
    while d <= last:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def _months(y):
    a = int(y.split("/")[0])
    out = []
    for i in range(12):
        mo = 4 + i
        out.append((a + (mo - 1) // 12, (mo - 1) % 12 + 1))
    return out


def settlement_advices(target, w):
    """What the mutual actually paid each member each month, by cover class, with the case detail the
    advice covers. Written as the mutual's own settlement workbook."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    head, fill = Font(bold=True), PatternFill("solid", fgColor="E6ECE6")

    def sheet(name, header, rows, widths):
        ws = wb.create_sheet(name)
        ws.append(header)
        for c in ws[1]:
            c.font = head
            c.fill = fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for r in rows:
            ws.append(r)
        for i, wd in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = wd
        ws.freeze_panes = "A2"

    detail, advice = [], []
    adj = _adjustments_by_advice(w)
    for m in w["members"]:
        for (yy, mm) in _months(W.MEASURED):
            for cover, items in (("unauthorised fraud", w["unauth"]), ("scam reimbursement", None)):
                if cover == "unauthorised fraud":
                    sel = [u for u in items if u["member"] == m["code"]
                           and u["closed_date"].year == yy and u["closed_date"].month == mm]
                    lines = [(u["ref"], u["reimbursed"]) for u in sel]
                else:
                    sel = [c for c in w["cases"] if c.member == m["code"] and c.recorded
                           and c.closed_date and c.closed_date.year == yy and c.closed_date.month == mm]
                    lines = [(c.case_ref, c.reimbursed) for c in sel]
                if not lines:
                    continue
                advice_no = "ADV-%d%02d-%s-%s" % (yy, mm, m["code"].split("-")[1],
                                                  "U" if cover == "unauthorised fraud" else "S")
                rows_out = [("%d-%02d" % (yy, mm), ref, amt) for ref, amt in lines]
                # the recoveries team's prior-period adjustment is one of the advice's own lines and
                # carries the month it settles in, which is not the month of the advice that pays it
                for a in adj.get((m["code"], (yy, mm), cover), []):
                    rows_out.append(("%d-%02d" % a["own_month"], a["ref"], a["amount"]))
                tot = round(sum(amt for _, _, amt in rows_out), 2)
                _rd = _run_days(yy, mm)
                _r = W.rng("advdate", m["code"], yy, mm, cover)
                _i = 0 if _r.random() < 0.72 else min(len(_rd) - 1, _r.randint(1, 3))
                advice.append([advice_no, m["code"], m["tier"], "%d-%02d" % (yy, mm), cover,
                               len(rows_out), "%.2f" % tot,
                               _d(_rd[_i])])
                for mth, ref, amt in rows_out:
                    detail.append([advice_no, m["code"], mth, cover, ref, "%.2f" % amt])
    advice.sort(key=lambda r: (r[3], r[1], r[4]))
    detail.sort(key=lambda r: (r[2], r[1], r[3], r[4]))
    sheet("advices", ["advice_no", "member_code", "contribution_tier", "settlement_month", "cover_class",
                      "case_lines", "advice_total_gbp", "advice_date"], advice,
          [22, 14, 11, 16, 20, 11, 17, 13])
    sheet("advice detail", ["advice_no", "member_code", "settlement_month", "cover_class",
                            "case_reference", "indemnity_paid_gbp"], detail, [22, 14, 16, 20, 18, 18])
    pack.freeze_workbook(wb, os.path.join(target, "settlement_advices_2026_27.xlsx"))
    return len(advice), len(detail)


def recovery_statements(target, w):
    """The mutual's recovery statement for the 2025/26 scheme year, by route and quarter of closure. The
    repatriation route is stated after the recovery agent's own charge, which the case-level credits are
    not, so the statement and the case ledger disagree on that route and on no other."""
    FEE = 0.145
    rows = []
    for qi in (1, 2, 3, 4):
        reimb = sum(c.reimbursed for c in w["cases"]
                    if c.year == "2025/26" and c.recorded and c.closed_date
                    and W.quarter_of(c.closed_date, "2025/26") == qi)
        for route in W.ROUTES:
            # the statement counts a recovery in the quarter the money arrived, which is not the
            # quarter the case closed in: the recoveries team reports its own cash quarter
            gross = sum(c.recovery_amount for c in w["cases"]
                        if c.year == "2025/26" and c.recorded and c.recovery_date
                        and W.quarter_of(c.recovery_date, "2025/26") == qi
                        and c.recovery_route == route)
            stated = gross * (1 - FEE) if route == "repatriation" else gross
            rows.append(["2025/26", "Q%d" % qi, route, "%.2f" % round(reimb, 2),
                         "%.2f" % round(stated, 2),
                         "net of recovery agent charges" if route == "repatriation" else "as credited"])
    _w(os.path.join(target, "recovery_statement_2025_26.csv"),
       ["scheme_year", "quarter_closed", "recovery_route", "reimbursed_in_quarter_gbp",
        "recovered_stated_gbp", "statement_basis"], rows)
    return len(rows)


def q1_notifications(target, w):
    """Scam cases notified in the quarter to 30 June 2027, from the mutual's notification feed. The main
    extract was cut on 20 June and the rest of the quarter sits in the supplementary file the feed sends
    at quarter end. Each file knows only what its own cut date knew, so a case the main extract carries
    is closed in it only where it closed on or before 20 June."""
    QSTART, CUT, QEND = dt.date(2027, 4, 1), dt.date(2027, 6, 20), dt.date(2027, 6, 30)
    main, supp = [], []
    for m in w["members"]:
        r = W.rng("q1", m["code"])
        # the calendar stream is its own, so moving a notification onto the working day the desk
        # logged it moves no amount, no lag and no reference
        rc = W.rng("q1cal", m["code"])
        used = set()
        n = max(8, int(round(m["volume"] / 1e6 * 4.4 * r.uniform(0.78, 1.26))))
        days = [r.randrange(91) for _ in range(n)]
        # every member notifies something in the last ten days of the quarter: with eight cases or
        # more over ninety days, a member with nothing in that span would be the odd one out
        if not any(x > 80 for x in days):
            days[days.index(max(days))] = 81 + r.randrange(10)
        drawn = []
        for i in range(n):
            nd = QSTART + dt.timedelta(days=days[i])
            lag = r.randint(1, 40)
            amt = round(min(r.lognormvariate(7.1, 1.2), 210000.0), 2)
            # a case notified late in the quarter can still be closed inside it: the simple purchase
            # scams close in days, the investment cases take months
            clag = r.randint(12, 60) if r.random() < 0.62 else r.randint(1, 6)
            # A reference identifies one case, so the member's own Q1 block is drawn without
            # replacement: two notifications sharing a reference would be one case carrying two
            # notified dates and two payment legs, which no notification run produces, and the count
            # of cases would then differ from the count of rows. The draw stays in the same stream
            # position, so no date, amount or count moves when a collision is walked on.
            k = r.randrange(1000, 9999)
            while k in used:
                k = k + 1 if k < 9999 else 1000
            used.add(k)
            drawn.append([nd, lag, amt, clag, k])
        # the fraud desk takes the notification on a working day
        for d in drawn:
            d[0] = W.on_a_working_day(d[0], rc, lo=QSTART, hi=QEND, keep_month=False)
        if not any(d[0] > CUT for d in drawn):
            d = max(drawn, key=lambda x: x[0])
            d[0] = W.on_a_working_day(CUT + dt.timedelta(days=5), rc,
                                      lo=CUT + dt.timedelta(days=1), hi=QEND, keep_month=False)
        for nd, lag, amt, clag, k in drawn:
            asof = CUT if nd <= CUT else QEND
            pay = nd - dt.timedelta(days=lag)
            closed = nd + dt.timedelta(days=clag)
            if closed <= asof:
                closed = W.on_a_working_day(closed, rc, lo=nd + dt.timedelta(days=1), hi=asof,
                                            keep_month=False)
            ref = "%s-Q1%s-%04d" % (m["code"].split("-")[1], "2728", k)
            row = [ref, m["code"], m["name"], _d(pay), _d(nd), "%.2f" % amt,
                   _d(closed) if closed <= asof else "",
                   "closed" if closed <= asof else "open"]
            (main if nd <= CUT else supp).append(row)
    hdr = ["case_reference", "member_code", "member_name", "payment_date", "notified_date",
           "payment_amount_gbp", "closed_date", "case_status"]
    main.sort(key=lambda r: (r[4], r[1]))
    supp.sort(key=lambda r: (r[4], r[1]))
    _w(os.path.join(target, "notifications_2027_28_q1.csv"), hdr, main)
    _w(os.path.join(target, "notifications_2027_28_q1_supplementary.csv"), hdr, supp)
    return len(main), len(supp), main, supp


def q1_return_sheet(target, w, main, supp):
    """The members' own Q1 2027/28 return, appended to the returns workbook: the stated case count covers
    the whole quarter, which the main extract alone does not."""
    path = os.path.join(target, "member_quarterly_returns.xlsx")
    wb = openpyxl.load_workbook(path)
    ws = wb.create_sheet("return 2027-28 Q1")
    ws.append(["member_code", "member_name", "scheme_year", "quarter", "payments_sent",
               "scam_cases_notified", "unauthorised_cases_notified", "vintage"])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E8E8E2")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for m in w["members"]:
        n = sum(1 for r in main + supp if r[1] == m["code"])
        r2 = W.rng("q1u", m["code"])
        ws.append([m["code"], m["name"], "2027/28", "Q1",
                   int(round(w["volumes"][(m["code"], W.MEASURED)]
                             * W.member_shape(m["code"])[0] * 1.064)),
                   n, int(round(m["volume"] / 1e6 * 4.6)), "revised"])
    for i, wd in enumerate([14, 24, 12, 9, 14, 18, 22, 11], start=1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A2"
    pack.freeze_workbook(wb, path)


def reference_files(target, w):
    """The two distractors, the dictionary, the register feed note and the export manifest."""
    r = W.rng("national")
    rows = []
    for yr in (2023, 2024, 2025, 2026):
        for q in (1, 2, 3, 4):
            rows.append([yr, "Q%d" % q, "authorised push payment",
                         "%.1f" % (r.uniform(41.0, 58.0)), "%.2f" % r.uniform(2.8, 4.1),
                         "%.1f" % r.uniform(58.0, 71.0)])
    _w(os.path.join(target, "national_scam_statistics_calendar_year.csv"),
       ["calendar_year", "calendar_quarter", "fraud_type", "reported_losses_gbp_million",
        "losses_per_gbp_million_of_payments", "reimbursed_share_per_cent"], rows)

    rows = []
    for m in w["members"]:
        for y in W.SCHEME_YEARS:
            for q in (1, 2, 3, 4):
                rr = W.rng("aml", m["code"], y, q)
                vol = w["quarter_volumes"][(m["code"], y, q)]
                rows.append([m["code"], y, "Q%d" % q, int(vol * rr.uniform(0.0008, 0.0021)),
                             int(vol * rr.uniform(0.00004, 0.00011)),
                             "%.1f" % rr.uniform(3.1, 9.4)])
    _w(os.path.join(target, "aml_alert_summary.csv"),
       ["member_code", "scheme_year", "quarter", "alerts_raised", "alerts_escalated",
        "escalation_rate_per_cent"], rows)

    dic = [
        ("case_register_2023_24.csv", "cover", "APP for a scam reimbursement case, UNAUTH for an "
         "unauthorised fraud case. The 2023/24 extract predates the 2024/25 layout change."),
        ("case_register_2023_24.csv", "payment_pence", "The amount the customer sent, in pence."),
        ("case_register_2023_24.csv", "notified_dt", "Date the member recorded the case, dd/mm/yyyy."),
        ("case_register_2024_27.csv", "cover_class", "The cover the case falls under: scam "
         "reimbursement or unauthorised fraud."),
        ("case_register_2024_27.csv", "payment_date", "Date the customer's payment left the member."),
        ("case_register_2024_27.csv", "notified_date", "Date the member recorded the case. A case "
         "appears in the register only when the member's own controls or its customer brought it to it."),
        ("case_register_2024_27.csv", "side", "sending where the member sent the payment. The register "
         "holds sending-side cases only."),
        ("case_payments.csv", "entry_type", "payment for a leg the customer sent, recovery credit for "
         "money that came back later. A case is one case however many legs it covers."),
        ("case_payments.csv", "value_date", "Date the entry was valued, so a recovery credit carries the "
         "date the money arrived rather than the date of the case."),
        ("mule_account_register.csv", "beneficiary_account", "Sort code without separators and account "
         "number zero padded to eight digits."),
        ("mule_account_register.csv", "registered_date", "Date the scheme register accepted the report "
         "from the firm that holds the account."),
        ("mule_account_register.csv", "registering_firm_type", "The kind of firm that received the "
         "money and reported the account."),
        ("member_payment_matches.csv", "beneficiary_account_ref", "As the mutual's own matching run "
         "writes it: sort code hyphenated, account number without leading zeros."),
        ("member_payment_matches.csv", "registered_date", "The register's date for the matched account."),
        ("fund_return_requests.csv", "request_sent_date", "Date the member asked the firm holding the "
         "beneficiary account to return the funds."),
        ("fund_return_requests.csv", "funds_returned_gbp", "Amount the receiving firm sent back, blank "
         "where nothing came back."),
        ("member_quarterly_returns.xlsx", "payments_sent_thousands", "Payments sent in the quarter, in "
         "thousands, on the sheet covering scheme years to 2023/24."),
        ("member_quarterly_returns.xlsx", "payments_sent", "Payments sent in the quarter, in whole "
         "payments, on the sheets covering 2024/25 onward."),
        ("member_quarterly_returns.xlsx", "vintage", "revised supersedes preliminary for the same "
         "member, scheme year and quarter."),
        ("settlement_advices_2026_27.xlsx", "advice_total_gbp", "The amount the advice settled with the "
         "member."),
        ("settlement_advices_2026_27.xlsx", "indemnity_paid_gbp", "The amount the advice settled for "
         "that case."),
        ("recovery_statement_2025_26.csv", "recovered_stated_gbp", "Recoveries on cases closed in the "
         "quarter, on the basis named in statement_basis."),
        ("notifications_2027_28_q1.csv", "notified_date", "Date the member recorded the case."),
        ("member_register.csv", "notified_payments_next_indemnity_year", "Payments the member expects to "
         "send in the indemnity year beginning 1 October 2027, as notified to the mutual."),
        ("member_register.csv", "triennial_review_this_cycle", "yes where the member's triennial "
         "experience review falls at this meeting of the trustees."),
    ]
    _w(os.path.join(target, "data_dictionary.csv"), ["extract", "column", "definition"],
       [[a, b, c] for a, b, c in dic])

    with open(os.path.join(target, "register_feed_notes.txt"), "w", encoding="utf-8") as f:
        f.write(
            "Kelverstone Mutual: scheme register feed\n"
            "Operations note, reissued %s by Lydia Page, underwriting and pricing\n\n"
            "The scheme sends the mutual the whole beneficiary account register each week, not only the\n"
            "accounts our members paid. The register is industry wide: an account appears on it because\n"
            "the firm that holds it reported it, whichever firm's customer was scammed.\n\n"
            "Account references are not written the same way on both sides. The register holds the sort\n"
            "code without separators and the account number zero padded to eight digits. Our own\n"
            "matching run writes the sort code hyphenated and drops leading zeros from the account\n"
            "number. Pad the account number back to eight digits before matching anything against the\n"
            "register, or the match loses every account whose number starts with a zero.\n\n"
            "The weekly run writes one row per member payment that matched a registered account, with\n"
            "the register's date for that account.\n"
            % W.PULL.strftime("%d %B %Y"))


def manifest(target, w, counts):
    rows = [
        ["case_register_2023_24.csv", "Claims register extract, scheme year 2023/24, pre-2024/25 layout",
         "scam reimbursement and unauthorised fraud cases recorded by members",
         "later scheme years", "claims system extract"],
        ["case_register_2024_27.csv", "Claims register extract, scheme years 2024/25 to 2026/27",
         "cases recorded by members, both covers", "", "claims system"],
        ["case_payments.csv", "Money movements on recorded cases",
         "payment legs and recovery credits", "cases with no movement posted", "claims ledger"],
        ["mule_account_register.csv", "Scheme beneficiary account register, whole industry",
         "accounts reported by the firms that hold them", "",
         "scheme weekly feed"],
        ["member_payment_matches.csv", "Weekly matching run output",
         "member payments whose beneficiary account is on the register",
         "payments to accounts nobody reported", "mutual matching run"],
        ["fund_return_requests.csv", "Outbound fund-return requests",
         "requests the claims team sent to receiving firms",
         "cases where no request was sent", "claims workflow"],
        ["member_quarterly_returns.xlsx", "Member quarterly returns",
         "payments sent and cases notified per member per quarter",
         "anything the member did not return", "member portal"],
        ["member_register.csv", "Membership register", "members, tiers, joining dates, notified volumes",
         "former members", "mutual secretariat"],
        ["settlement_advices_2026_27.xlsx", "Settlement advices and their case detail, 2026/27",
         "what the mutual settled with each member each month",
         "settlements outside 2026/27", "settlement run"],
        ["recovery_statement_2025_26.csv", "Recovery statement, scheme year 2025/26",
         "recoveries on cases closed in the year by route",
         "recoveries on cases closed in other years", "recoveries team"],
        ["notifications_2027_28_q1.csv", "Notification feed, quarter to 30 June 2027, cut 20 June 2027",
         "cases notified to 20 June 2027", "notifications after the cut", "notification feed"],
        ["notifications_2027_28_q1_supplementary.csv", "Notification feed supplement, quarter end",
         "cases notified 21 to 30 June 2027", "cases already in the main extract", "notification feed"],
        ["national_scam_statistics_calendar_year.csv", "Published national scam statistics",
         "national reported losses by calendar quarter per million pounds of payment value",
         "any member level detail; any count basis", "industry body publication"],
        ["aml_alert_summary.csv", "Member AML alert summary",
         "alerts raised and escalated per member per quarter",
         "what the alerts were about", "member returns"],
        ["data_dictionary.csv", "Field definitions", "fields across the pack", "derived quantities",
         "mutual data office"],
        ["register_feed_notes.txt", "Operations note on the register feed",
         "how the feed and the matching run are written", "anything about a member's experience",
         "mutual operations"],
        ["indemnity_standard_v6.pdf", "The mutual's indemnity standard, version 6",
         "cover, the incidence index and the evidence base", "parts 1 to 3 and the schedules",
         "mutual secretariat"],
        ["trustee_pack_2027_07.pdf", "Trustees' meeting pack, 14 July 2027",
         "agenda and membership position", "any index or recommendation", "mutual secretariat"],
    ]
    _w(os.path.join(target, "export_manifest.csv"),
       ["file", "what_it_is", "what_it_covers", "what_it_omits", "produced_by"], rows)
    return len(rows)
