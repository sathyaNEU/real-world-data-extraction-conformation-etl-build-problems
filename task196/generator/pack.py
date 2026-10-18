"""Writes target/: the mutual's own extracts, the scheme's register, the member returns and the
settlement, recovery and notification files the asks run on.

Layer 1 is what these systems really produce: the case register changed layout at the 2024/25 scheme
year and still holds its old amounts in pence, the member return reports payment volumes in thousands on
the old sheet and in units on the new one, account references are zero-padded in the scheme's register
and unpadded in the mutual's match extract, one member joined part way through a scheme year, and the
quarterly return exists in a preliminary and a revised vintage. None of it decides the call.
"""
import csv
import datetime as dt
import json
import os
import re

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import world as W

FIXED_ZIP_TIME = (2027, 7, 2, 9, 0, 0)


def freeze_workbook(wb, path):
    """Save a workbook so two builds give identical bytes: no author, no timestamps in the document
    properties, and every zip member written with the pack's own export time."""
    import zipfile
    wb.properties.creator = ""
    wb.properties.lastModifiedBy = ""
    wb.properties.created = dt.datetime(*FIXED_ZIP_TIME)
    wb.properties.modified = dt.datetime(*FIXED_ZIP_TIME)
    wb.properties.title = None
    wb.properties.description = None
    wb.save(path)
    stamp = b"2027-07-02T09:00:00Z"
    with zipfile.ZipFile(path) as zf:
        items = []
        for i in sorted(zf.infolist(), key=lambda x: x.filename):
            data = zf.read(i.filename)
            if i.filename == "docProps/app.xml":
                data = re.sub(rb"<Application>[^<]*</Application>",
                              b"<Application>Kelverstone Mutual secretariat</Application>", data)
            if i.filename == "docProps/core.xml":
                # openpyxl writes the save time into the document properties whatever the workbook
                # object says, so the stamp is replaced here, on the bytes that ship
                data = re.sub(rb">[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:]{8}Z<", b">" + stamp + b"<", data)
            items.append((i, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        for info, data in items:
            zi = zipfile.ZipInfo(info.filename, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zf.writestr(zi, data)

OLD_YEAR = "2023/24"


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)


def _d(d):
    return d.isoformat() if d else ""


def _uk(d):
    return d.strftime("%d/%m/%Y") if d else ""


def case_ref(c, m_code):
    r = W.rng("ref", m_code, c.year, c.idx)
    return "%s-%s-%05d" % (m_code.split("-")[1], c.year.replace("/", ""), r.randrange(10000, 99999))


def assign_refs(cases, by_code):
    for c in cases:
        if c.recorded:
            c.case_ref = case_ref(c, c.member)


# ---------------------------------------------------------------------------
# the unauthorised-fraud class: the mutual's other cover, and the home of ask A
# ---------------------------------------------------------------------------
def unauthorised_cases(members):
    """Card and remote-banking fraud cases, the cover the mutual writes beside scam reimbursement. The
    call's population is the scam class only; these rows are outside it."""
    out = []
    for m in members:
        for y in W.SCHEME_YEARS:
            lo, hi = W.year_bounds(y)
            if m["joined"] > lo:
                lo = m["joined"]
            span = max(1, (hi - lo).days)
            r = W.rng("unauth", m["code"], y)
            n = int(round(m["volume"] / 1e6 * 17.5 * {"2023/24": 0.82, "2024/25": 0.9,
                                                      "2025/26": 0.96, "2026/27": 1.0}[y]))
            refs = r.sample(range(10000, 99999), n)
            for i in range(n):
                pd = lo + dt.timedelta(days=r.randrange(span))
                amt = round(min(r.lognormvariate(6.05, 1.02), 24000.0), 2)
                open_d = pd + dt.timedelta(days=r.randint(0, 9))
                out.append(dict(member=m["code"], year=y, idx=i, payment_date=pd, open_date=open_d,
                                amount=amt, reimbursed=round(amt * (1.0 if r.random() < 0.91 else
                                                                    r.uniform(0.4, 0.95)), 2),
                                closed_date=open_d + dt.timedelta(
                                    days=r.randint(6, max(7, min(95, (W.PULL - open_d).days - 1)))),
                                sub_class=r.choices(["card not present", "lost or stolen",
                                                     "remote banking", "counterfeit"],
                                                    weights=[58, 17, 19, 6])[0],
                                ref="%s-U%s-%05d" % (m["code"].split("-")[1], y.replace("/", ""),
                                                     refs[i]),
                                recovery_route=(r.choice(W.ROUTES) if r.random() < 0.31 else None),
                                recovery_frac=r.uniform(0.1, 0.7),
                                recovery_offset=r.randint(2, 60)))
    return out


# ---------------------------------------------------------------------------
# the files
# ---------------------------------------------------------------------------
def case_registers(target, w, unauth):
    """Two extracts of the same register, cut either side of the 2024/25 layout change."""
    members = w["by_code"]
    scam = [c for c in w["cases"]]
    old_rows, new_rows = [], []
    for c in scam:
        if not c.recorded:
            continue
        m = members[c.member]
        if c.year == OLD_YEAR:
            old_rows.append([c.case_ref, c.member, "APP", _uk(c.payment_date), _uk(c.open_date),
                             int(round(c.amount * 100)), int(round(c.reimbursed * 100)),
                             _uk(c.closed_date), c.scam_type, c.channel, c.dest_firm, "Y"])
        else:
            new_rows.append([c.case_ref, c.member, m["name"], "scam reimbursement", c.year,
                             _d(c.payment_date), _d(c.open_date), "%.2f" % c.amount,
                             "%.2f" % c.reimbursed, _d(c.closed_date), c.scam_type, c.channel,
                             c.dest_firm, "sending"])
    for u in unauth:
        if u["year"] == OLD_YEAR:
            old_rows.append([u["ref"], u["member"], "UNAUTH", _uk(u["payment_date"]), _uk(u["open_date"]),
                             int(round(u["amount"] * 100)), int(round(u["reimbursed"] * 100)),
                             _uk(u["closed_date"]), u["sub_class"], "", "", "Y"])
        else:
            new_rows.append([u["ref"], u["member"], members[u["member"]]["name"], "unauthorised fraud",
                             u["year"], _d(u["payment_date"]), _d(u["open_date"]),
                             "%.2f" % u["amount"], "%.2f" % u["reimbursed"], _d(u["closed_date"]),
                             u["sub_class"], "", "", "sending"])
    old_rows.sort(key=lambda r: (r[1], r[3][6:], r[3][3:5], r[3][:2], r[0]))
    new_rows.sort(key=lambda r: (r[4], r[1], r[5], r[0]))
    _w(os.path.join(target, "case_register_2023_24.csv"),
       ["case_no", "member_code", "cover", "payment_dt", "notified_dt", "payment_pence",
        "reimbursed_pence", "closed_dt", "category", "payment_channel", "beneficiary_firm_type",
        "sending_side"], old_rows)
    _w(os.path.join(target, "case_register_2024_27.csv"),
       ["case_reference", "member_code", "member_name", "cover_class", "scheme_year", "payment_date",
        "notified_date", "payment_amount_gbp", "reimbursed_amount_gbp", "closed_date", "scam_type",
        "payment_channel", "beneficiary_firm_type", "side"], new_rows)
    return len(old_rows), len(new_rows)


def case_payments(target, w, unauth):
    """One row per money movement on a case: the payment legs the customer sent and the credits that came
    back later. Recoveries are credit rows against the original case, posted when they arrive."""
    rows = []
    for c in w["cases"]:
        if not c.recorded:
            continue
        amounts = ([c.amount] if c.legs == 1
                   else [round(c.amount * 0.6, 2), round(c.amount - round(c.amount * 0.6, 2), 2)])
        for j, a in enumerate(amounts):
            rows.append([c.case_ref, c.member, "scam reimbursement", "payment", j + 1,
                         _d(c.payment_date + dt.timedelta(days=j)), "%.2f" % a, "", ""])
        if c.recovery_route:
            rows.append([c.case_ref, c.member, "scam reimbursement", "recovery credit", 1,
                         _d(c.recovery_date), "", "%.2f" % c.recovery_amount, c.recovery_route])
    for u in unauth:
        rows.append([u["ref"], u["member"], "unauthorised fraud", "payment", 1, _d(u["payment_date"]),
                     "%.2f" % u["amount"], "", ""])
        if u["recovery_route"] and (u["closed_date"] + dt.timedelta(days=u["recovery_offset"])) <= W.PULL:
            rows.append([u["ref"], u["member"], "unauthorised fraud", "recovery credit", 1,
                         _d(u["closed_date"] + dt.timedelta(days=u["recovery_offset"])), "",
                         "%.2f" % round(u["reimbursed"] * u["recovery_frac"], 2),
                         u["recovery_route"]])
    rows.sort(key=lambda x: (x[1], x[0], x[3], x[4], x[5]))
    _w(os.path.join(target, "case_payments.csv"),
       ["case_reference", "member_code", "cover_class", "entry_type", "leg_no", "value_date",
        "paid_amount_gbp", "credit_amount_gbp", "recovery_route"], rows)
    return len(rows)


def mule_register(target, w):
    """The scheme's central register of beneficiary accounts firms have reported. Industry wide, so most
    rows have nothing to do with this mutual's members."""
    rows = []
    for c in w["cases"]:
        if c.registration_date is None:
            continue
        rows.append([_pad(c.account), _d(c.registration_date), "reported",
                     _firm_of(c), "scam proceeds"])
    # the rest of the industry's reporting over the same window
    r = W.rng("industry")
    lo = dt.date(2023, 1, 1)
    for i in range(21400):
        acc = W.account_ref(r)
        d = lo + dt.timedelta(days=r.randrange((W.AS_OF - lo).days))
        rows.append([_pad(acc), _d(d), r.choices(["reported", "closed by firm", "reported"],
                                                 weights=[72, 19, 9])[0],
                     r.choices(["clearing bank", "e-money institution", "building society",
                                "overseas correspondent"], weights=[46, 34, 12, 8])[0],
                     r.choices(["scam proceeds", "mule recruitment", "unauthorised proceeds"],
                               weights=[61, 17, 22])[0]])
    rows.sort(key=lambda x: (x[1], x[0]))
    _w(os.path.join(target, "mule_account_register.csv"),
       ["beneficiary_account", "registered_date", "register_status", "registering_firm_type",
        "report_reason"], rows)
    return len(rows)


def _pad(acc):
    """The register holds the sort code without separators and the account number zero padded to eight."""
    a, b = acc.split("/")
    return "%s/%s" % (a.replace("-", ""), b.zfill(8))


def _firm_of(c):
    return c.dest_firm


def payment_matches(target, w):
    """The mutual runs its members' outbound payments against the register each week and keeps what
    matched. The reference is unpadded here and padded in the register, so a raw join misses rows."""
    rows = []
    for c in w["cases"]:
        if c.registration_date is None:
            continue
        rows.append([c.member, _unpad(c.account), _d(c.payment_date), "%.2f" % c.amount, c.channel,
                     c.dest_firm, _d(c.registration_date), c.case_ref or "", c.year])
    rows.sort(key=lambda x: (x[0], x[2], x[1]))
    _w(os.path.join(target, "member_payment_matches.csv"),
       ["member_code", "beneficiary_account_ref", "payment_date", "payment_amount_gbp",
        "payment_channel", "beneficiary_firm_type", "registered_date", "case_reference",
        "scheme_year"], rows)
    return len(rows)


def _unpad(acc):
    """The mutual's own match extract keeps the sort code hyphenated and strips leading zeros, so a raw
    string join against the register misses every account whose number starts with a zero."""
    a, b = acc.split("/")
    return "%s/%s" % (a, b.lstrip("0") or "0")


def fund_return_requests(target, w):
    """The members' own outbound fund-return requests: what the mutual's claims team asked receiving
    firms to send back, and what came back. One row per request."""
    rows = []
    for c in w["cases"]:
        if c.request_date is None:
            continue
        r = W.rng("frr", c.member, c.year, c.idx)
        returned = ""
        if c.self_reg_date is not None and r.random() < 0.34:
            returned = "%.2f" % round(c.amount * r.uniform(0.02, 0.38), 2)
        elif r.random() < 0.12:
            returned = "%.2f" % round(c.amount * r.uniform(0.01, 0.2), 2)
        rows.append([c.member, c.case_ref, _unpad(c.account), _d(c.request_date), c.dest_firm,
                     "%.2f" % c.amount, returned,
                     "returned in part" if returned else r.choice(["no funds held", "no response",
                                                                   "declined"])])
    rows.sort(key=lambda x: (x[0], x[3], x[1]))
    _w(os.path.join(target, "fund_return_requests.csv"),
       ["member_code", "case_reference", "beneficiary_account_ref", "request_sent_date",
        "destination_firm_type", "payment_amount_gbp", "funds_returned_gbp", "request_outcome"], rows)
    return len(rows)


def member_register(target, w):
    rows = []
    for m in w["members"]:
        rows.append([m["code"], m["name"], m["tier"], W.TIER_NAMES[m["tier"]], _d(m["joined"]),
                     "yes" if m["review"] else "no",
                     int(round(w["volumes"][(m["code"], W.MEASURED)] * 1.04 / 1000.0) * 1000),
                     "scam reimbursement, unauthorised fraud"])
    _w(os.path.join(target, "member_register.csv"),
       ["member_code", "member_name", "contribution_tier", "tier_basis", "joined_date",
        "triennial_review_this_cycle", "notified_payments_next_indemnity_year",
        "covers_held"], rows)
    return len(rows)


def quarterly_returns(target, w):
    """The member return, as the mutual holds it: the pre-2024/25 sheet reports payment volumes in
    thousands and the current sheet in units, and the current year exists in a preliminary and a revised
    vintage. The revised vintage supersedes."""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    head = Font(bold=True)
    fill = PatternFill("solid", fgColor="E8E8E2")

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
        return ws

    old = []
    for m in w["members"]:
        for q in (1, 2, 3, 4):
            v = w["quarter_volumes"][(m["code"], OLD_YEAR, q)]
            n = _notified(w, m["code"], OLD_YEAR, q)
            old.append([m["code"], OLD_YEAR, "Q%d" % q, round(v / 1000.0, 1), n[0], n[1]])
    sheet("returns to 2023-24", ["member_code", "scheme_year", "quarter", "payments_sent_thousands",
                                 "scam_cases_notified", "unauthorised_cases_notified"], old,
          [14, 12, 9, 22, 18, 22])
    new = []
    for m in w["members"]:
        for y in ["2024/25", "2025/26", "2026/27"]:
            for q in (1, 2, 3, 4):
                v = w["quarter_volumes"][(m["code"], y, q)]
                n = _notified(w, m["code"], y, q)
                new.append([m["code"], m["name"], y, "Q%d" % q, v, n[0], n[1], "revised"])
    sheet("returns 2024-25 onward", ["member_code", "member_name", "scheme_year", "quarter",
                                     "payments_sent", "scam_cases_notified",
                                     "unauthorised_cases_notified", "vintage"], new,
          [14, 24, 12, 9, 14, 18, 22, 11])
    prelim = []
    for m in w["members"]:
        for q in (1, 2, 3, 4):
            v = w["quarter_volumes"][(m["code"], W.MEASURED, q)]
            n = _notified(w, m["code"], W.MEASURED, q)
            r = W.rng("prelim", m["code"], q)
            # the preliminary return always moves somewhere before it is revised: the fourth quarter
            # is still settling when the member first files, and earlier quarters move sometimes
            back = r.randrange(600, 9000) if (q == 4 or r.random() < 0.45) else 0
            prelim.append([m["code"], m["name"], W.MEASURED, "Q%d" % q, v - back,
                           n[0] - (1 if r.random() < 0.3 else 0), n[1], "preliminary"])
    sheet("preliminary 2026-27", ["member_code", "member_name", "scheme_year", "quarter",
                                  "payments_sent", "scam_cases_notified",
                                  "unauthorised_cases_notified", "vintage"], prelim,
          [14, 24, 12, 9, 14, 18, 22, 11])
    path = os.path.join(target, "member_quarterly_returns.xlsx")
    freeze_workbook(wb, path)
    return len(old) + len(new) + len(prelim)


def _notified(w, code, y, q):
    scam = sum(1 for c in w["cases"] if c.member == code and c.year == y and c.recorded
               and W.quarter_of(c.open_date, y) == q)
    un = sum(1 for u in w["unauth"] if u["member"] == code and u["year"] == y
             and W.quarter_of(u["open_date"], y) == q)
    return scam, un


def write_all(target, w):
    os.makedirs(target, exist_ok=True)
    counts = {}
    counts["case_register"] = case_registers(target, w, w["unauth"])
    counts["case_payments"] = case_payments(target, w, w["unauth"])
    counts["mule_register"] = mule_register(target, w)
    counts["matches"] = payment_matches(target, w)
    counts["requests"] = fund_return_requests(target, w)
    counts["members"] = member_register(target, w)
    counts["returns"] = quarterly_returns(target, w)
    return counts
