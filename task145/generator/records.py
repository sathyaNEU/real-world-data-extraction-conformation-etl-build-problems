"""The extracts, each in the layout its system writes: the clearance system's quarterly high-value check extracts (two
layouts), the gateway activity reports (legacy and new), the time and attendance exports (legacy and new), the HR
files, the finance cost-centre map, Brandmoor's portal export, the AP register, and the two distractors."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import field as FD

# ---------------------------------------------------------------------------------------------------- the files
F_HV = {"2024Q4": "highvalue_check_2024Q4.csv", "2025Q1": "highvalue_check_2025Q1.csv",
        "2025Q2": "highvalue_check_2025Q2.csv", "2025Q3": "highvalue_check_2025Q3.csv",
        "2025Q4": "highvalue_check_2025Q4.csv", "2026Q1": "highvalue_check_2026Q1.csv",
        "2026Q2": "highvalue_check_2026Q2.csv", "2026Q3": "highvalue_check_2026Q3.csv"}
OLD_LAYOUT = ("2024Q4", "2025Q1", "2025Q2", "2025Q3", "2025Q4")     # pulled before the release of 17 February 2026
HV_WINDOW = {"2024Q4": (dt.date(2024, 10, 1), dt.date(2024, 12, 31), dt.date(2025, 1, 7)),
             "2025Q1": (dt.date(2025, 1, 1), dt.date(2025, 3, 31), dt.date(2025, 4, 7)),
             "2025Q2": (dt.date(2025, 4, 1), dt.date(2025, 6, 30), dt.date(2025, 7, 8)),
             "2025Q3": (dt.date(2025, 7, 1), dt.date(2025, 9, 30), dt.date(2025, 10, 7)),
             "2025Q4": (dt.date(2025, 10, 1), dt.date(2025, 12, 31), dt.date(2026, 1, 6)),
             "2026Q1": (dt.date(2026, 1, 1), dt.date(2026, 3, 31), dt.date(2026, 4, 7)),
             "2026Q2": (dt.date(2026, 4, 1), dt.date(2026, 6, 30), dt.date(2026, 7, 7)),
             "2026Q3": (dt.date(2026, 7, 1), dt.date(2026, 9, 30), dt.date(2026, 10, 7))}
F_GW_LEGACY = "gateway_activity_2021-01_2024-09.xlsx"
F_GW_NEW = "gateway_activity_2024-10_2026-09.csv"
F_PLAN27 = "network_plan_2027.xlsx"
F_PLAN26 = "network_plan_2026_issued_2025-09.xlsx"
F_STD = "brk_std_03_brokerage_staffing_standard.pdf"
F_CLR = "clr_ops_11_clearance_routing.docx"
F_NOTE_CLR = "clearance_extracts_note_2026-10-07.txt"
F_TA_OLD = "ta_legacy_export_2025-04-01_2025-10-31.csv"
F_TA_NEW = "ta_export_2025-10-27_2026-09-30.csv"
F_HR_STAFF = "hr_brokerage_staff_2026-10-06.xlsx"
F_HR_CHG = "hr_assignment_changes_2025-04_2026-09.csv"
F_CC = "finance_cost_centres_2026.csv"
F_NOTE_PAY = "payroll_hr_extracts_note_2026-10-06.txt"
F_BCS_PDF = "brandmoor_statements_2025-04_2026-03.pdf"
F_BCS_PORTAL = "brandmoor_portal_detail_2025-04_2026-03.json"
F_AP = "ap_invoice_register_brandmoor_2025-04_2026-09.xlsx"
F_BCS_RATES = "brandmoor_rate_schedule_2025.pdf"
F_EXPORTS = "export_declarations_monthly_2025-04_2026-09.csv"
DISTRACTORS = [F_PLAN26, F_EXPORTS]

LEGACY_CC = {"YYZ": "4511", "YUL": "4512", "YVR": "4513", "YYC": "4514", "YWG": "4515"}
NEW_CC = {"YYZ": "610411", "YUL": "610412", "YVR": "610415", "YYC": "610418", "YWG": "610419"}

# ---------------------------------------------------------------------------------------------------- high-value check
HV_OLD = ["WAYBILL", "GTWY", "REL_DT", "REL_TM_UTC", "IMPORTER_ACCT", "HS_CODE", "ORIG_CTRY", "INV_CURR", "VFD_INV",
          "CUST_RATE", "VFD_CAD", "ROUTE", "ENTRY_NO", "OGD_PGM", "AMEND"]
HV_NEW = ["waybill", "gateway", "release_local_date", "release_utc", "importer_account", "hs_code", "origin_country",
          "invoice_currency", "value_for_duty", "customs_exchange_rate", "value_for_duty_cad", "route", "entry_number",
          "ogd_program", "amended"]


def fmt_value(cur, v):
    return "%d" % int(round(v)) if cur == "JPY" else "%.2f" % v


def fmt_rate(cur, r):
    return ("%." + str(K.RATE_DP[cur]) + "f") % r if cur != "CAD" else "1"


def hv_rows(W):
    """The eight quarterly extracts: each shipment released in its window (local release date), and the shipments
    amended since the last pull with their corrected value."""
    out = {q: [] for q in F_HV}
    by_q = {q: [] for q in F_HV}
    for s in W.prior + W.ships:
        d = s.local.date()
        for q, (a, b, _) in HV_WINDOW.items():
            if a <= d <= b:
                by_q.setdefault(q, []).append((s, s.value, ""))
    qs = list(F_HV)
    for s, nv in W.amended:
        d = s.local.date()
        for i, q in enumerate(qs):
            a, b, _ = HV_WINDOW[q]
            if a <= d <= b and i + 1 < len(qs):
                by_q[qs[i + 1]].append((s, nv, "Y"))
    for q in qs:
        rows = []
        for s, v, am in by_q[q]:
            cad = K.round_dp(v * s.rate, 2)
            if q in OLD_LAYOUT:
                rows.append({"WAYBILL": s.waybill, "GTWY": s.gw, "REL_DT": s.local.strftime("%d/%m/%Y"),
                             "REL_TM_UTC": s.utc.strftime("%H:%M"), "IMPORTER_ACCT": s.importer, "HS_CODE": s.hs,
                             "ORIG_CTRY": s.origin, "INV_CURR": s.cur, "VFD_INV": fmt_value(s.cur, v),
                             "CUST_RATE": fmt_rate(s.cur, s.rate), "VFD_CAD": "%.2f" % cad, "ROUTE": s.route,
                             "ENTRY_NO": s.entry, "OGD_PGM": s.ogd, "AMEND": am or "N"})
            else:
                rows.append({"waybill": s.waybill, "gateway": s.gw, "release_local_date": s.local.strftime("%Y-%m-%d"),
                             "release_utc": s.utc.strftime("%Y-%m-%dT%H:%M:%SZ"), "importer_account": s.importer,
                             "hs_code": s.hs, "origin_country": s.origin, "invoice_currency": s.cur,
                             "value_for_duty": fmt_value(s.cur, v), "customs_exchange_rate": fmt_rate(s.cur, s.rate),
                             "value_for_duty_cad": "%.2f" % cad, "route": s.route, "entry_number": s.entry,
                             "ogd_program": s.ogd or "NONE", "amended": am or "N"})
        # the extract sorts by release time, the amended rows after the window's own
        if q in OLD_LAYOUT:
            rows.sort(key=lambda r: (r["AMEND"], r["REL_DT"][6:] + r["REL_DT"][3:5] + r["REL_DT"][:2],
                                     r["REL_TM_UTC"], r["WAYBILL"]))
        else:
            rows.sort(key=lambda r: (r["amended"], r["release_utc"], r["waybill"]))
        out[q] = rows
    return out


# ---------------------------------------------------------------------------------------------------- gateway activity
def accounting_shift(W, g, y, m, r):
    """The legacy brokerage system counted a formal entry in the month its B3 was accounted, a few business days
    after release: the last days' releases fall in the next month."""
    return int(round(W.formal_hist[(g, y, m)] * (0.031 + 0.012 * r.random())))


def gw_legacy_rows(W):
    r = K.rng("legacy_report")
    rows = []
    carry = {g: int(round(W.formal_hist[(g, 2020 + 1, 1)] * 0.035)) for g in K.GATEWAYS}
    for (y, m) in K.HIST_MONTHS:
        if dt.date(y, m, 1) > K.LEGACY_REPORT_END:
            break
        for g in K.GATEWAYS:
            sh = accounting_shift(W, g, y, m, r)
            acc = W.formal_hist[(g, y, m)] - sh + carry[g]
            carry[g] = sh
            vol = W.volume[(g, y, m)]
            rows.append([dt.date(y, m, 1), K.DESK[g], vol, vol - W.formal_hist[(g, y, m)], acc])
    return rows


GW_NEW = ["gateway_code", "period", "inbound_international_shipments", "clvs_releases", "formal_entries_released"]


def gw_new_rows(W):
    rows = []
    for (y, m) in K.HIST_MONTHS:
        if dt.date(y, m, 1) <= K.LEGACY_REPORT_END:
            continue
        for g in K.GATEWAYS:
            vol = W.volume[(g, y, m)]
            f = W.formal_hist[(g, y, m)]
            rows.append({"gateway_code": g, "period": "%d-%02d" % (y, m), "inbound_international_shipments": vol,
                         "clvs_releases": vol - f, "formal_entries_released": f})
    return rows


# ---------------------------------------------------------------------------------------------------- time and attendance
TA_OLD = ["EMPLID", "WORK_DATE", "PAY_CODE", "HOURS", "IN_TIME", "OUT_TIME", "HOME_CC"]
TA_NEW = ["employee_number", "work_date", "earning_code", "quantity", "punch_in", "punch_out", "home_cost_center",
          "source"]
OLD_CODE = {"REG": "REG", "OT15": "OT15", "OT20": "OT20", "CB": "CALLB", "VAC": "VAC", "SCK": "SICK", "TRN": "TRAIN",
            "STAT": "STAT"}
NEW_CODE = {"REG": "REG", "OT15": "OT1.5", "OT20": "OT2.0", "CB": "CB", "VAC": "VAC", "SCK": "SCK", "TRN": "TRN",
            "STAT": "STH"}


def ta_rows(staff, lines):
    """The legacy export (1 April to 31 October 2025, pulled 31 October 2025) and the new system's export (from 27
    October 2025, pulled 6 October 2026). Each line carries the employee's home cost centre as the export found it.
    The new system was loaded with the legacy system's open timecards of 27 to 31 October (source MIGRATED, copied as
    they stood); its own lines from 1 November are punches rounded to the quarter hour."""
    by_k = {s.k: s for s in staff}
    old, new = [], []
    for ln in lines:
        s = by_k[ln.emp]
        if ln.day <= FD.TA_LEGACY_END:
            home = s.desk_on(FD.TA_LEGACY_PULL) if (s.left is None or s.left > FD.TA_LEGACY_PULL) else s.desk_on(s.left)
            old.append({"EMPLID": s.legacy_id, "WORK_DATE": ln.day.strftime("%m/%d/%Y"), "PAY_CODE": OLD_CODE[ln.code],
                        "HOURS": "%.2f" % ln.hours, "IN_TIME": ln.t_in.strftime("%H:%M") if ln.t_in else "",
                        "OUT_TIME": ln.t_out.strftime("%H:%M") if ln.t_out else "", "HOME_CC": LEGACY_CC[home]})
        if ln.day >= FD.TA_NEW_FROM:
            home = s.desk_on(FD.TA_NEW_PULL) if (s.left is None or s.left > FD.TA_NEW_PULL) else s.desk_on(s.left)
            migrated = ln.day <= FD.TA_LEGACY_END
            manual = (not migrated and ln.code == "REG" and ln.t_in is not None and
                      (s.k * 7 + ln.day.toordinal()) % 53 == 0)
            if manual:
                new.append({"employee_number": s.emp_no, "work_date": ln.day.isoformat(), "earning_code": "REG",
                            "quantity": "%.2f" % ln.hours, "punch_in": "", "punch_out": "",
                            "home_cost_center": NEW_CC[home], "source": "MANUAL"})
                continue
            new.append({"employee_number": s.emp_no, "work_date": ln.day.isoformat(),
                        "earning_code": NEW_CODE[ln.code], "quantity": "%.2f" % ln.hours,
                        "punch_in": ln.t_in.strftime("%Y-%m-%dT%H:%M") if ln.t_in else "",
                        "punch_out": ln.t_out.strftime("%Y-%m-%dT%H:%M") if ln.t_out else "",
                        "home_cost_center": NEW_CC[home], "source": "MIGRATED" if migrated else "TIMECLOCK"})
    old.sort(key=lambda r: (r["EMPLID"], r["WORK_DATE"][6:] + r["WORK_DATE"][:2] + r["WORK_DATE"][3:5], r["PAY_CODE"]))
    new.sort(key=lambda r: (r["work_date"], r["employee_number"], r["earning_code"]))
    return old, new


# ---------------------------------------------------------------------------------------------------- HR and finance
HR_CHG = ["employee_number", "effective_date", "change_type", "from_desk", "to_desk", "note"]


def hr_change_rows(staff):
    rows = []
    for s in staff:
        for i, (f, g) in enumerate(s.desks):
            if i == 0:
                if f >= dt.date(2025, 4, 1):
                    rows.append({"employee_number": s.emp_no, "effective_date": f.isoformat(), "change_type": "HIRE",
                                 "from_desk": "", "to_desk": K.DESK[g], "note": s.position})
                continue
            prev = s.desks[i - 1][1]
            rows.append({"employee_number": s.emp_no, "effective_date": f.isoformat(), "change_type": "TRANSFER",
                         "from_desk": K.DESK[prev], "to_desk": K.DESK[g], "note": "desk reassignment"})
        if s.left:
            rows.append({"employee_number": s.emp_no, "effective_date": s.left.isoformat(), "change_type": "TERMINATION",
                         "from_desk": K.DESK[s.desk_on(s.left)], "to_desk": "", "note": "resignation"})
    # promotions and licence grants on the same file
    for s in staff:
        if s.position == "Broker Trainee" and s.hired < dt.date(2025, 1, 1):
            rows.append({"employee_number": s.emp_no, "effective_date": "2026-09-08", "change_type": "LICENCE",
                         "from_desk": "", "to_desk": "", "note": "customs broker licence granted, title unchanged "
                                                                   "until the January establishment"})
    rows.sort(key=lambda r: (r["effective_date"], r["employee_number"]))
    return rows


CC_COLS = ["cost_centre", "scheme", "description", "desk", "valid_from", "valid_to"]


def cc_rows():
    rows = []
    for g in K.GATEWAYS:
        rows.append({"cost_centre": LEGACY_CC[g], "scheme": "LEGACY", "description": "Brokerage desk %s" % K.DESK[g],
                     "desk": K.DESK[g], "valid_from": "2014-04-01", "valid_to": "2025-10-31"})
    for g in K.GATEWAYS:
        rows.append({"cost_centre": NEW_CC[g], "scheme": "ERP 2025", "description": "Customs brokerage - %s desk" %
                     K.DESK[g], "desk": K.DESK[g], "valid_from": "2025-11-01", "valid_to": ""})
    extra = [("4520", "LEGACY", "Clearance operations Mississauga", "", "2014-04-01", "2025-10-31"),
             ("4521", "LEGACY", "Clearance operations Dorval", "", "2014-04-01", "2025-10-31"),
             ("620401", "ERP 2025", "Clearance operations - Mississauga", "", "2025-11-01", ""),
             ("620402", "ERP 2025", "Clearance operations - Dorval", "", "2025-11-01", ""),
             ("610400", "ERP 2025", "Customs brokerage - department", "", "2025-11-01", ""),
             ("4510", "LEGACY", "Customs brokerage department", "", "2014-04-01", "2025-10-31")]
    for c in extra:
        rows.append(dict(zip(CC_COLS, c)))
    rows.sort(key=lambda r: (r["scheme"], r["cost_centre"]))
    return rows


# ---------------------------------------------------------------------------------------------------- Brandmoor
PORTAL = ["statement_month", "statement_number", "client_code", "entry_number", "transmitted_et", "service", "rush",
          "fee", "rush_fee", "statement_minimum_adjustment"]


def statement_month_label(st):
    return "%d-%02d" % (st.issued.year, st.issued.month) if not st.reissue_of else "%d-%02d" % (
        (st.month[0] + (st.month[1] == 12)), st.month[1] % 12 + 1)


def portal_rows(stmts):
    """The client portal's detail export, filtered by statement month April 2025 to March 2026: one line per entry on
    the statement as it now stands (a re-issued statement replaces its original)."""
    rows = []
    replaced = {s.reissue_of for s in stmts if s.reissue_of}
    for st in stmts:
        if st.number in replaced:
            continue
        lab = statement_month_label(st)
        if not ("2025-04" <= lab <= "2026-03"):
            continue
        std_r, ogd_r, rush_r = st.portal_rates
        for e in st.entries:
            fee = std_r if e.service == "STD" else ogd_r
            rows.append({"statement_month": lab, "statement_number": st.number, "client_code": FD.CLIENT_CODE[st.gw],
                         "entry_number": e.entry, "transmitted_et": e.t.strftime("%Y-%m-%dT%H:%M"),
                         "service": e.service, "rush": "Y" if e.rush else "N", "fee": "%.2f" % fee,
                         "rush_fee": "%.2f" % (rush_r if e.rush else 0.0),
                         "statement_minimum_adjustment": "%.2f" % st.minimum_adj})
    rows.sort(key=lambda r: (r["statement_month"], r["statement_number"], r["transmitted_et"], r["entry_number"]))
    return rows


def write_portal(path, stmts):
    """The portal's statement-detail export as its API returns it: a header naming the client and the statement
    months asked for, then one object per entry line, each line on its own line of the file."""
    import json
    rows = portal_rows(stmts)
    head = [("export", "Statement detail"), ("client", "Larchwood Express Canada Ltd."),
            ("client_codes", [FD.CLIENT_CODE[g] for g in K.GATEWAYS]),
            ("statement_months", {"from": "2025-04", "to": "2026-03"}),
            ("exported_et", "2026-10-06T09:14:52"), ("line_count", len(rows))]
    out = ["{"]
    for k, v in head:
        out.append("  %s: %s," % (json.dumps(k), json.dumps(v, ensure_ascii=False)))
    out.append('  "lines": [')
    for i, r in enumerate(rows):
        out.append("    " + json.dumps(r, ensure_ascii=False) + ("," if i < len(rows) - 1 else ""))
    out += ["  ]", "}"]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")
    return len(rows)


def ap_rows(stmts, holidays):
    """Larchwood's AP register for Brandmoor, postings April 2025 to September 2026."""
    r = K.rng("ap")
    rows = []
    for st in stmts:
        post = st.issued + dt.timedelta(days=int(r.integers(1, 4)))
        while post.weekday() >= 5 or post in holidays:
            post += dt.timedelta(days=1)
        cc = NEW_CC[st.gw] if post >= dt.date(2025, 11, 1) else LEGACY_CC[st.gw]
        if post < dt.date(2025, 4, 1) or post > dt.date(2026, 9, 30):
            continue
        rows.append(["Brandmoor Customs Services Inc.", "Invoice", st.number, st.issued, post, cc, st.net,
                     round(sum(v for _, v in st.taxes), 2), st.total, "Statement %s" % FD.CLIENT_CODE[st.gw]])
        if st.credit_memo:
            num, d = st.credit_memo
            p2 = d + dt.timedelta(days=1)
            cc2 = NEW_CC[st.gw]
            rows.append(["Brandmoor Customs Services Inc.", "Credit memo", num, d, p2, cc2, -st.net,
                         -round(sum(v for _, v in st.taxes), 2), -st.total, "Reverses %s" % st.number])
    rows.sort(key=lambda x: (x[4], x[2]))
    return rows


# ---------------------------------------------------------------------------------------------------- distractor
EXPORTS = ["gateway_code", "period", "export_declarations_filed", "cers_exemptions", "shipments_outbound_intl"]


def export_rows(W):
    r = K.rng("exports")
    rows = []
    for (y, m) in K.months(dt.date(2025, 4, 1), dt.date(2026, 9, 30)):
        for g in K.GATEWAYS:
            out = int(W.volume[(g, y, m)] * {"YYZ": 0.46, "YUL": 0.38, "YVR": 0.29, "YYC": 0.34, "YWG": 0.27}[g]
                      * math.exp(r.normal(0, 0.03)))
            decl = int(out * (0.021 + 0.004 * r.random()))
            rows.append({"gateway_code": g, "period": "%d-%02d" % (y, m), "export_declarations_filed": decl,
                         "cers_exemptions": int(out * (0.012 + 0.003 * r.random())), "shipments_outbound_intl": out})
    return rows
