"""Writes the bundle under target/ from the world and the administrative records, each file in the form its
producing system exports it."""
import datetime as dt
import hashlib
import os
import random

import openpyxl
from openpyxl.styles import Font

import admin as AD
import docs
import io_util as IO
import params as P
import world as WD

FILES = {
    "holds": "shelfmark_holds_20250901-20261031.csv",
    "loans": "shelfmark_checkouts_20250901-20261031.csv",
    "terms": "UC-26-114_course_texts_fund_2027_terms.pdf",
    "lending": "shelfmark_lending_licence_terms_v2025.2.pdf",
    "procedures": "collections_procedures_course_texts_v3.pdf",
    "register": "erm_licence_register_20261031.xlsx",
    "status": "shelfmark_licence_status_20250901.csv",
    "lists": "leganto_reading_list_items_2025-26_2026-27.csv",
    "courses": "course_catalogue_2025-26_2026-27.xlsx",
    "catalogue": "alma_course_text_records_20261030.csv",
    "invoices": "agresso_invoice_lines_CT_20260101-20261031.csv",
    "rates": "finance_office_monthly_rates_2025-26.csv",
    "survey": "SA_textbook_access_survey_2026_results.xlsx",
    "usage": "shelfmark_title_usage_2025-26.csv",
}
KBART = {
    "Stanwell Business and Economics Core 2026": "StanwellPress_BusinessEconomicsCore_2026_kbart.txt",
    "Corran & Lyle Law Library 2026": "CorranLyle_LawLibrary_2026_kbart.txt",
    "Northfield Health Sciences Essentials 2026": "NorthfieldMedical_HealthSciencesEssentials_2026_kbart.txt",
    "Ashdown STEM Texts 2026": "AshdownScientific_STEMTexts_2026_kbart.txt",
    "Ellesmere Humanities and Social Sciences 2026": "EllesmereUP_HumanitiesSocialSciences_2026_kbart.txt",
}
DISTRACTORS = [FILES["survey"], FILES["usage"]]

PATRON_TYPE = {"UG": "Undergraduate", "PGT": "Taught postgraduate", "PGR": "Research postgraduate", "STAFF": "Staff"}
STATUS = {"fulfilled": "Fulfilled", "expired": "Offer expired", "cancelled_user": "Cancelled by borrower",
          "cancelled_system": "Cancelled - account closed", "waiting": "Waiting"}


def ts(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ") if t else ""


def hid(prefix, n, salt):
    h = hashlib.sha1(("%s-%d" % (salt, n)).encode()).hexdigest()
    return prefix + str(int(h[:10], 16) % 10 ** 9).zfill(9)


def patron_key(sid):
    return "p_" + hashlib.sha1(("ardmuir-sso-%d" % sid).encode()).hexdigest()[:12]


def assign_ids(W):
    """platform identifiers: hashed sequence numbers, re-drawn on a clash so every identifier is unique"""
    for objs, prefix, salt, attr in ((W.holds, "HLD", "hold", "hold_id"), (W.loans, "CHK", "loan", "loan_id")):
        seen = set()
        for i, o in enumerate(objs):
            k = 0
            v = hid(prefix, i, salt)
            while v in seen:
                k += 1
                v = hid(prefix, i, "%s%d" % (salt, k))
            seen.add(v)
            setattr(o, attr, v)


def write(W, A, target):
    os.makedirs(target, exist_ok=True)
    rng = random.Random(P.SEED * 13 + 5)
    tby = {t["id"]: t for t in W.titles}
    assign_ids(W)
    W._loan_by_hold = {}
    for l in W.loans:
        if l.hold is not None:
            W._loan_by_hold.setdefault(id(l.hold), []).append(l)

    # holds export
    rows = []
    for h in W.holds:
        t = tby[h.title]
        s = W.students[h.student]
        chk = ""
        if h.status == "fulfilled":
            chk = next(l.loan_id for l in W._loan_by_hold[id(h)])
        rows.append([h.hold_id, t["platform_id"], t["e_isbn"], t["title"], patron_key(h.student),
                     PATRON_TYPE[s["group"]], "ard-sch-" + s["school"].lower(), ts(h.placed), STATUS[h.status],
                     ts(h.closed) if h.status != "waiting" else "", ts(h.offered),
                     ts(h.offered + dt.timedelta(hours=P.OFFER_HOURS)) if h.offered else "", chk])
    IO.write_csv(os.path.join(target, FILES["holds"]),
                 ["hold_id", "title_id", "isbn", "title", "patron_id", "patron_type", "department_code",
                  "placed_at", "status", "status_changed_at", "offer_made_at", "offer_expires_at", "checkout_id"],
                 rows, crlf=True)

    # checkouts export
    rows = []
    for l in W.loans:
        t = tby[l.title]
        if l.returned >= P.EXTRACT:
            ended, reason = "", ""
        else:
            ended = ts(l.returned)
            reason = "Returned early" if l.returned < l.due else "Loan period ended"
        rows.append([l.loan_id, t["platform_id"], patron_key(l.student), ts(l.start), l.days, ts(l.due), ended, reason])
    IO.write_csv(os.path.join(target, FILES["loans"]),
                 ["checkout_id", "title_id", "patron_id", "checked_out_at", "loan_days", "due_at", "ended_at",
                  "end_reason"], rows, crlf=True)

    # governing documents
    docs.fund_terms(os.path.join(target, FILES["terms"]))
    docs.lending_terms(os.path.join(target, FILES["lending"]))
    docs.procedures(os.path.join(target, FILES["procedures"]))

    # licence register (ERM)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Licences"
    head = ["Licence ID", "Platform title ID", "e-ISBN", "Title", "Publisher", "Licence model", "Copies",
            "Order date", "PO line", "Order type", "Net price (line)", "Currency", "Fund code"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
    mtext = {"1U": "1 user, perpetual", "1U-M": "1 user, 40 loans", "3U": "3 users, perpetual"}
    lics = [L for L in W.licences if L.model != "PKG" and L.bought <= dt.date(2026, 10, 31)]
    lics.sort(key=lambda L: (L.bought, L.lic_id))
    for L in lics:
        t = tby[L.title]
        price = _price_in_currency(A, L)
        # the platform's automatic re-licences reach the register through the order feed, without a fund
        fund = "" if L.order_type == "Renewal" else AD.fund_code(W.school_old[L.ordered_by], L.bought)
        ws.append([L.lic_id, t["platform_id"], t["e_isbn"], t["title"], t["publisher"], mtext[L.model], L.copies,
                   L.bought, L.po_line, L.order_type, round(price, 2), L.currency, fund])
    for row in ws.iter_rows(min_row=2, min_col=8, max_col=8):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("Packages")
    ws2.append(["Package", "Publisher", "Agent", "Access from", "Access to", "PO line", "Net price", "Currency",
                "Fund code"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    for pk in A.packages:
        agent = [p[1] for p in WD.PUBLISHERS if p[0] == pk["publisher"]][0]
        ws2.append([pk["name"], pk["publisher"], agent, dt.date(2026, 1, 1), dt.date(2026, 12, 31), pk["po_line"],
                    pk["amount"], pk["currency"], "CT-CORE"])
    _save_xlsx(wb, os.path.join(target, FILES["register"]))

    # platform licence status report at 1 September 2025 (40-loan licences)
    rows = []
    for L in sorted([L for L in W.licences if L.model == "1U-M" and L.bought <= P.RECORD_START.date()],
                    key=lambda L: L.lic_id):
        t = tby[L.title]
        rows.append([L.lic_id, t["platform_id"], "1 user, 40 loans", L.remaining0[0], "2025-09-01"])
    IO.write_csv(os.path.join(target, FILES["status"]),
                 ["licence_id", "title_id", "model", "loans_remaining", "as_at"], rows)

    # reading list items
    period = {"A25": "2025-26 Semester 1", "S26": "2025-26 Semester 2", "A26": "2026-27 Semester 1"}
    ctitle = {c["code"]: c["title"] for c in A.courses}
    rows = []
    for it in A.items:
        rows.append([it["list_item"], it["course"], ctitle[it["course"]], period[it["sem"]], it["title"],
                     _ord(it["edition"]), it["isbn"], it["importance"], "Book"])
    IO.write_csv(os.path.join(target, FILES["lists"]),
                 ["list_item_id", "course_code", "course_title", "teaching_period", "item_title", "edition", "isbn",
                  "importance", "item_type"], rows)

    # course catalogue
    wb = openpyxl.Workbook()
    first = True
    for yr, sems in (("2025-26", ("A25", "S26")), ("2026-27", ("A26",))):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = yr
        ws.append(["Course code", "Course title", "School code", "School", "Semester", "Credits", "Enrolled at census"])
        for c in ws[1]:
            c.font = Font(bold=True)
        for c in sorted([c for c in A.courses if c["sem"] in sems], key=lambda c: c["code"]):
            ws.append([c["code"], c["title"], c["school"], W.school_name[c["school"]],
                       "Semester 1" if c["sem"] != "S26" else "Semester 2", 20 if c["level"] < 5 else 15, c["enrol"]])
    _save_xlsx(wb, os.path.join(target, FILES["courses"]))

    # catalogue records
    rows = []
    for r in A.catalogue:
        rows.append([r["mms"], r["title"], _ord(r["edition"]), r["year"], r["isbn"], r["rtype"], r["platform"],
                     r["linked"], r["preceded_by"], r["publisher"]])
    IO.write_csv(os.path.join(target, FILES["catalogue"]),
                 ["mms_id", "title", "edition", "publication_year", "isbn", "resource_type", "shelfmark_title_id",
                  "related_record_mms", "preceding_edition_mms", "publisher"], rows)

    # invoice lines (finance system export, UK dates)
    rows = []
    for i in A.invoices:
        rows.append([i["vendor"], i["invoice"], i["inv_date"].strftime("%d/%m/%Y"), i["po_line"], i["desc"], i["isbn"],
                     i["qty"], i["currency"], "%.2f" % i["amount"], i["fund"], i["line_type"]])
    IO.write_csv(os.path.join(target, FILES["invoices"]),
                 ["supplier", "invoice_no", "invoice_date", "po_line", "description", "isbn", "qty", "currency",
                  "net_amount", "fund_code", "line_type"], rows, crlf=True)

    # Finance Office monthly rates
    rows = [[r["month"].strftime("%Y-%m"), "%.4f" % r["eur"], "%.4f" % r["usd"]] for r in A.rates]
    IO.write_csv(os.path.join(target, FILES["rates"]), ["month", "EUR_per_GBP", "USD_per_GBP"], rows)

    # KBART title lists, one per package
    for pk in A.packages:
        rows = []
        items = [(t["title"], t["p_isbn"] if rng.random() < 0.4 else "", t["e_isbn"], t["edition"], t["year"])
                 for t in pk["titles"]]
        items += [(x["title"], "", x["e_isbn"], x["edition"], x["year"]) for x in pk["extra"]]
        rng.shuffle(items)
        for (tt, pi, oi, ed, yr) in items:
            rows.append([tt, pi, oi, "", "", "", "", "", "", "", "", "", "", "fulltext", "", pk["publisher"],
                         "monograph", "%d" % yr, "%d" % yr, "", str(ed), "", "", "", "P"])
        IO.write_csv(os.path.join(target, KBART[pk["name"]]),
                     ["publication_title", "print_identifier", "online_identifier", "date_first_issue_online",
                      "num_first_vol_online", "num_first_issue_online", "date_last_issue_online",
                      "num_last_vol_online", "num_last_issue_online", "title_url", "first_author", "title_id",
                      "embargo_info", "coverage_depth", "notes", "publisher_name", "publication_type",
                      "date_monograph_published_print", "date_monograph_published_online", "monograph_volume",
                      "monograph_edition", "first_editor", "parent_publication_title_id",
                      "preceding_publication_title_id", "access_type"], rows, delimiter="\t")

    # distractors
    survey(W, os.path.join(target, FILES["survey"]), rng)
    usage(W, os.path.join(target, FILES["usage"]), rng)

    for f in os.listdir(target):
        IO.set_mtime(os.path.join(target, f))


def _price_in_currency(A, L):
    """a register line's net price in the currency it was invoiced in"""
    gbp = L.price_gbp * L.copies
    if L.currency == "GBP":
        return round(gbp, 2)
    for r in A.rates:
        if r["month"].year == L.bought.year and r["month"].month == L.bought.month:
            return round(gbp * (r["eur"] if L.currency == "EUR" else r["usd"]), 2)
    return round(gbp * (1.1612 if L.currency == "EUR" else 1.2745), 2)


def _ord(n):
    n = int(n)
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, suf)


def _save_xlsx(wb, path):
    wb.properties.creator = "Ardmuir University Library"
    wb.properties.lastModifiedBy = "Ardmuir University Library"
    wb.properties.created = dt.datetime(2026, 10, 31, 9, 0, 0)
    wb.properties.modified = dt.datetime(2026, 10, 31, 9, 0, 0)
    wb.save(path)
    IO.fix_zip(path)


def survey(W, path, rng):
    """The Students' Association's spring survey (distractor): responses by faculty."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "By faculty"
    ws.append(["Students' Association textbook access survey, spring 2026"])
    ws.append(["Fieldwork 20 April to 8 May 2026. Weighted to the student body by faculty and level."])
    ws.append([])
    ws.append(["Faculty (2025-26)", "Responses", "Used Shelfmark Lend this semester (%)",
               "Read course texts mainly on a phone (%)", "Prefer 7-day loans (%)",
               "Satisfied with e-textbook access (%)"])
    for c in ws[4]:
        c.font = Font(bold=True)
    names = {"AH": "Arts and Humanities", "SS": "Social Sciences", "BS": "Ardmuir Business School", "LW": "Law",
             "EN": "Engineering", "PS": "Physical Sciences", "LS": "Life Sciences", "MD": "Medicine and Dentistry",
             "NH": "Nursing and Health Sciences"}
    for o in ["AH", "SS", "BS", "LW", "EN", "PS", "LS", "MD", "NH"]:
        ws.append([names[o], rng.randint(88, 410), round(rng.uniform(58, 86), 1), round(rng.uniform(21, 47), 1),
                   round(rng.uniform(52, 81), 1), round(rng.uniform(29, 58), 1)])
    _save_xlsx(wb, path)


def usage(W, path, rng):
    """Shelfmark's title usage report (distractor): checkouts and turnaways by title and month."""
    tby = {t["id"]: t for t in W.titles}
    agg = {}
    for l in W.loans:
        m = l.start.strftime("%Y-%m")
        agg.setdefault((l.title, m), [0, 0])[0] += 1
    for h in W.holds:
        m = h.placed.strftime("%Y-%m")
        agg.setdefault((h.title, m), [0, 0])[1] += 1
    rows = []
    for (tid, m), (c, tw) in sorted(agg.items(), key=lambda x: (tby[x[0][0]]["platform_id"], x[0][1])):
        t = tby[tid]
        rows.append([t["platform_id"], t["title"], t["e_isbn"], m, c, tw])
    IO.write_csv(os.path.join(path), ["title_id", "title", "isbn", "month", "checkouts", "turnaways"], rows)
