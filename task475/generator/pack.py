"""Write the evidence pack (target/) from the clean truth in world.py. Each file is written the way its source system
writes it (the e-marking platform's export, the legacy candidate register, the candidate portal's entries and its
request log, the enquiries CRM, the finance ledger); nothing here describes the data."""
import csv
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np

import params as P
import world as W

D = dt.date
TD = dt.timedelta
FIXED_ZIP_TIME = P.STAMP


# ---------------------------------------------------------------------------------------------------------------
# helpers
def sydney_offset(t):
    """Hours ahead of UTC in Sydney: AEST +10, AEDT +11 from the first Sunday of October to the first Sunday of
    April (changes at 2 am local)."""
    y = t.year

    def first_sunday(m):
        d = D(y, m, 1)
        while d.weekday() != 6:
            d += TD(days=1)
        return dt.datetime(d.year, d.month, d.day, 2, 0)

    return 10 if first_sunday(4) <= t < first_sunday(10) else 11


def iso_local(t):
    off = sydney_offset(t)
    return t.strftime("%Y-%m-%dT%H:%M:%S") + "+%02d:00" % off


def iso_utc(t):
    u = t - TD(hours=sydney_offset(t))
    return u.strftime("%Y-%m-%dT%H:%M:%SZ")


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)


def normalise_zip(path, when="2026-11-30T06:05:00Z", app="Microsoft Excel", stats=None):
    """Rewrite an OOXML container with fixed member times and order and fixed document dates, so two builds are
    byte-identical."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in items:
        if name == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>",
                          data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
            for k, v in (stats or {}).items():
                data = re.sub(rb"<%s>[^<]*</%s>" % (k.encode(), k.encode()),
                              b"<%s>%d</%s>" % (k.encode(), int(v), k.encode()), data)
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + when.encode() + rb"\g<2>",
                          data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + when.encode() +
                          rb"\g<2>", data)
        fixed.append((name, data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in fixed:
            zi = zipfile.ZipInfo(name, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


def xlsx_props(wb, creator, title, when):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = when
    wb.properties.modified = when
    wb.properties.title = title


def write_pdf(path, title, issuer, blocks, stamp_date):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.6)
    head = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=13.5,
                          spaceBefore=7, spaceAfter=2)
    ttl = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=13.5, leading=16.5)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    story = []
    for kind, val in blocks:
        if kind == "title":
            story += [Paragraph(val, ttl), Spacer(1, 3)]
        elif kind == "h":
            story.append(Paragraph(val, head))
        elif kind == "p":
            story += [Paragraph(val, body), Spacer(1, 2.5)]
        elif kind == "small":
            story += [Paragraph(val, small), Spacer(1, 2)]
        elif kind == "table":
            t = Table(val, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
                                   ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9a9a9a")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story += [t, Spacer(1, 5)]
        elif kind == "space":
            story.append(Spacer(1, val))

    def stamp(canvas, doc):
        canvas.setAuthor(issuer)
        canvas.setCreator(issuer)
        canvas.setProducer(issuer)
        canvas.setTitle(title)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(18 * mm, 10 * mm, "%s  |  %s  |  page %d" % (issuer, title, doc.page))

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, invariant=1, title=title, author=issuer, creator=issuer,
                            producer=issuer)
    doc.build(story, onFirstPage=stamp, onLaterPages=stamp)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)",
                b"ReportLab Generated PDF document http://www.reportlab.com"):
        data = data.replace(sig, b" " * len(sig))
    for key in (b"/CreationDate", b"/ModDate"):
        def sub(m):
            new = stamp_date.encode()
            assert len(new) == len(m.group(1)), (m.group(1), new)
            return key + b" (" + new + b")"
        data = re.sub(re.escape(key) + rb" \(([^)]*)\)", sub, data)
    assert b"ReportLab" not in data and b"reportlab" not in data
    open(path, "wb").write(data)


def abn(rng):
    w8 = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    while True:
        d = [int(x) for x in rng.integers(0, 10, 11)]
        if d[0] == 0:
            continue
        dd = d.copy()
        dd[0] -= 1
        if sum(a * b for a, b in zip(dd, w8)) % 89 == 0:
            s = "".join(map(str, d))
            return "%s %s %s %s" % (s[:2], s[2:5], s[5:8], s[8:])


# ---------------------------------------------------------------------------------------------------------------
# the e-marking platform's export of marks of record (both 2026 series)
def marking_rows(w, rng):
    rows = []
    # markers: each question has its own team in each series
    may_team = {j: ["E%03d" % (110 + 7 * j + k) for k in range(4)] for j in range(8)}
    nov_team = {j: ["MK%04d" % int(x) for x in rng.choice(np.arange(2100, 2999), size=4, replace=False)]
                for j in range(8)}
    se = ["SE%02d" % k for k in (3, 4, 7, 9, 11)]

    def may_item(j, k):
        return "%d(%s)" % (j + 1, "abcd"[k])

    def nov_item(j, k):
        return "Q%02d.%d" % (j + 1, k + 1)

    def blank_ok(v):
        return v == 0 and rng.random() < 0.55

    # May original marking, 18 May to 12 June; the delayed script on 2 and 3 July
    sitters = w.may_sitters
    noresp = {}
    for (i, j), pm in sorted(w.may_parts0.items()):
        if i == w.may_late:
            day = D(2026, 7, 2) + TD(days=int(rng.integers(0, 2)))
        else:
            day = D(2026, 5, 18) + TD(days=int(rng.integers(0, 26)))
        t = W.stamp_in(rng, day, 8.0, 21.5)
        mk = may_team[j][int(rng.integers(0, 4))]
        for k, v in enumerate(pm):
            dash = blank_ok(int(v))
            noresp[(i, j, k)] = dash
            rows.append(("MAY26", "CAE2", sitters[i]["cand"], may_item(j, k), P.MAY_QUESTIONS[j][1][k],
                         "-" if dash else str(int(v)), mk, t + TD(seconds=int(rng.integers(20, 150)) * (k + 1))))
    # borderline re-marks, whole script, 19 to 26 June
    done = set()
    for kind, i, j, day in w.may_events:
        t = W.stamp_in(rng, day, 8.5, 17.5)
        mk = se[int(rng.integers(0, 4))]
        for k, v in enumerate(w.may_parts1[(i, j)]):
            dash = noresp[(i, j, k)] and int(v) == 0
            rows.append(("MAY26", "CAE2", sitters[i]["cand"], may_item(j, k), P.MAY_QUESTIONS[j][1][k],
                         "-" if dash else str(int(v)), mk, t + TD(seconds=int(rng.integers(30, 200)) * (k + 1))))
    # reviews: the senior examiner's marks become the marks of record
    for r in w.may_reviews:
        if r["declined"]:
            continue
        i = r["i"]
        t = W.stamp_in(rng, r["completed"], 8.5, 17.5)
        mk = se[int(rng.integers(0, 5))]
        for j, ks in r["rows"]:
            for k in ks:
                v = int(w.may_parts2[(i, j)][k])
                dash = noresp[(i, j, k)] and v == 0
                rows.append(("MAY26", "CAE2", sitters[i]["cand"], may_item(j, k), P.MAY_QUESTIONS[j][1][k],
                             "-" if dash else str(v), mk, t + TD(seconds=int(rng.integers(30, 200)) * (k + 1))))
    # November original marking, 9 to 27 November
    for (i, j), pm in sorted(w.nov_parts.items()):
        day = D(2026, 11, 9) + TD(days=int(rng.integers(0, 19)))
        t = W.stamp_in(rng, day, 7.5, 22.0)
        mk = nov_team[j][int(rng.integers(0, 4))]
        for k, v in enumerate(pm):
            dash = blank_ok(int(v))
            rows.append(("NOV26", "CAE-P2", w.nov_sitters[i]["cand"], nov_item(j, k), P.NOV_QUESTIONS[j][1][k],
                         "-" if dash else str(int(v)), mk, t + TD(seconds=int(rng.integers(20, 150)) * (k + 1))))
    rows.sort(key=lambda r: (r[0] != "MAY26", int(r[2]), r[3], r[7]))
    return [(a, b, c, d, e, f, g, iso_local(t)) for a, b, c, d, e, f, g, t in rows]


def legacy_name(fam, given):
    return "%s, %s" % (fam.upper(), given)


def build_pack(w, out):
    os.makedirs(out, exist_ok=True)
    rng = np.random.default_rng(P.SEED_OPS + 7)
    fp = lambda k: os.path.join(out, P.FILES[k])
    counts = {}
    people = w.people

    # 1 marking export
    rows = marking_rows(w, rng)
    write_csv(fp("export"), ["series", "component", "candidate_no", "item", "max_mark", "mark", "marker",
                             "entered_at"], rows)
    counts["export"] = len(rows)

    # 2 legacy candidate register, May 2026 sitting
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Candidates"
    hdr = ["Cand No", "Candidate Name", "Date of Birth", "Member No", "Centre", "Papers", "Entry Date", "Status"]
    ws.append(hdr)
    for c in ws[1]:
        c.font = Font(bold=True)
    may_rows = sorted(w.may_entries, key=lambda e: int(e["cand"]))
    for e in may_rows:
        p = people[e["pid"]]
        ws.append([e["cand"], legacy_name(p["family"], p["given"]), p["dob"].strftime("%d/%m/%Y"), p["member_no"],
                   P.MAY_NAME[e["centre"]], e["papers"], e["entered"].strftime("%d/%m/%Y"),
                   "Withdrawn" if e["withdrawn"] else "Entered"])
    for col, wd in zip("ABCDEFGH", (9, 34, 13, 11, 13, 8, 12, 11)):
        ws.column_dimensions[col].width = wd
    xlsx_props(wb, "Examinations Office", "CAE May 2026 candidates", dt.datetime(2026, 8, 3, 8, 40))
    wb.save(fp("may_reg"))
    normalise_zip(fp("may_reg"), when="2026-08-02T22:40:00Z")
    counts["may_reg"] = len(may_rows)

    # 3 candidate portal entries, November 2026 sitting (one row per paper entered)
    refs = rng.choice(np.arange(100_000, 999_999), size=len(w.nov_entries) * 2, replace=False)
    ent = []
    k = 0
    for x in sorted(w.nov_entries, key=lambda x: (x["entered"], x["applicant"])):
        pp = w.nov_people[x["pid"]]
        p = people[x["pid"]]
        for paper in [q for q in ("P1", "P2") if q in x["papers"]]:
            status, changed = "Entered", ""
            if x["status_changed"] is not None:
                status, changed = "Withdrawn", x["status_changed"].isoformat()
            elif paper == "P1" and x.get("p1_closed"):
                status, changed = "Withdrawn", x["p1_closed"].isoformat()
            ent.append(["E26-%06d" % int(refs[k]), x["applicant"], x["cand"], pp["family"], pp["given"],
                        p["dob"].isoformat(), pp["member_no"], pp["email"], x["centre"], paper,
                        x["entered"].isoformat(), status, changed])
            k += 1
    write_csv(fp("nov_reg"), ["entry_ref", "applicant_id", "candidate_no", "family_name", "given_names",
                              "date_of_birth", "member_no", "email", "centre_code", "paper", "entered_on", "status",
                              "status_changed"], ent)
    counts["nov_reg"] = len(ent)

    # 4 candidate portal request log (API export)
    reqs = []
    ids = rng.choice(np.arange(10_000, 99_999), size=len(w.nov_requests), replace=False)
    for r, rid in zip(sorted(w.nov_requests, key=lambda r: (r["created"], r["x"]["applicant"])), sorted(ids)):
        reqs.append({"request_id": "RQ-%05d" % int(rid), "applicant_id": r["x"]["applicant"], "type": r["type"],
                     "papers": r["paper"], "submitted": iso_utc(r["created"]), "detail": r["detail"],
                     "status": r["state"], "actioned_on": r["closed"].isoformat()})
    with open(fp("requests"), "w", encoding="utf-8") as f:
        json.dump({"export": "candidate-requests", "generated": "2026-11-30T06:05:00Z", "count": len(reqs),
                   "requests": reqs}, f, indent=1)
        f.write("\n")
    counts["requests"] = len(reqs)

    # 5 centre directory
    cen = []
    for code, name, blk, _s, venue, state in P.CENTRES:
        if code == "WSY":
            cen.append(["PAR", "Parramatta", venue, state, blk * 1000 + 1, blk * 1000 + 999, "2014-03-01",
                        "2026-07-31"])
            cen.append([code, name, venue, state, blk * 1000 + 1, blk * 1000 + 999, "2026-08-01", ""])
        else:
            cen.append([code, name, venue, state, blk * 1000 + 1, blk * 1000 + 999, "2011-05-01", ""])
    cen.append(["HBA", "Hobart", "Level 1, 85 Macquarie Street, Hobart", "TAS", 7001, 7999, "2015-05-01",
                "2025-06-30"])
    write_csv(fp("centres"), ["centre_code", "centre_name", "venue", "state", "cand_no_from", "cand_no_to",
                              "opened", "closed"], cen)
    counts["centres"] = len(cen)

    # 6 enquiries CRM: results review requests, May 2026 sitting
    firms = {f[0]: f for f in W.FIRMS}
    inv_no = {}
    invoices = []
    seq = 260_418
    acct_reqs = {}
    for r in w.may_reviews:
        if r["account"]:
            acct_reqs.setdefault(r["account"], []).append(r)
    review_inv_total = {}
    for a in sorted(acct_reqs):
        review_inv_total[a] = round(sum(r["paid"] for r in acct_reqs[a]), 2)
    rr = []
    rno = 1180
    for r in w.may_reviews:
        rno += int(rng.integers(1, 4))
        s = w.may_sitters[r["i"]]
        p = people[s["pid"]]
        r["request_no"] = "RR26-%04d" % rno
        if r["account"]:
            amount = review_inv_total[r["account"]]
        else:
            amount = r["paid"]
        r["amount_shown"] = amount
        rr.append([r["request_no"], r["received"].strftime("%d/%m/%Y %H:%M"), r["typed"], p["family"].upper(),
                   "Re-mark" if r["service"] == "remark" else "Clerical check",
                   "; ".join(str(j + 1) for j in r["qs"]), "Account" if r["account"] else "Card", r["account"],
                   "%.2f" % amount, "", r["completed"].strftime("%d/%m/%Y")])
    # 7 finance ledger: accounts receivable invoices to corporate accounts, 2026
    led = []
    day_events = []
    for code, name, dom, disc in W.FIRMS:
        day_events.append((D(2026, 1, 20) + TD(days=int(rng.integers(0, 10))), code,
                           "Corporate membership 2026 (%d certifiers)" % int(rng.integers(3, 18)),
                           round(float(rng.integers(9, 40)) * 185.0, 2)))
        for _ in range(int(rng.integers(1, 4))):
            mth = int(rng.integers(2, 11))
            day_events.append((D(2026, mth, 5) + TD(days=int(rng.integers(0, 20))), code,
                               pick_cpd(rng), round(float(rng.integers(2, 9)) * 395.0 * (1 - disc / 100), 2)))
    # employer-paid November entries
    for x in w.nov_entries:
        p = people[x["pid"]]
        if p["firm"] and rng.random() < 0.5:
            fee = sum(P.FEES["2026-27"]["entry_%s" % q.lower()] for q in ("P1", "P2") if q in x["papers"])
            disc = firms[p["firm"]][3]
            day_events.append((x["entered"], p["firm"], "Examination entry, November 2026 sitting",
                               round(fee * (1 - disc / 100), 2)))
    # monthly roll-up of entry fees per account
    ent_month = {}
    other = []
    for ev in day_events:
        if ev[2].startswith("Examination entry"):
            key = (ev[1], ev[0].month)
            ent_month.setdefault(key, []).append(ev)
        else:
            other.append(ev)
    for (code, mth), evs in sorted(ent_month.items()):
        last = D(2026, mth + 1, 1) - TD(days=1) if mth < 12 else D(2026, 12, 31)
        other.append((last, code, "Examination entries, November 2026 sitting (%d candidate%s)" %
                      (len(evs), "" if len(evs) == 1 else "s"), round(sum(e[3] for e in evs), 2)))
    for a in sorted(acct_reqs):
        n = len(acct_reqs[a])
        other.append((D(2026, 7, 31), a, "Results review fees, May 2026 sitting (%d request%s)" %
                      (n, "" if n == 1 else "s"), review_inv_total[a]))
    other.sort(key=lambda e: (e[0], e[1], e[2]))
    for d_, code, desc, amt in other:
        seq += int(rng.integers(1, 5))
        no = "INV-%d" % seq
        if desc.startswith("Results review fees"):
            inv_no[code] = no
        paid = d_ + TD(days=int(rng.integers(9, 35)))
        led.append([no, code, firms[code][1], d_.isoformat(), desc, "%.2f" % amt, "%.2f" % round(amt / 11.0, 2),
                    "Paid" if paid <= P.EXPORT_DAY else "Open", paid.isoformat() if paid <= P.EXPORT_DAY else ""])
    for row, r in zip(rr, w.may_reviews):
        if r["account"]:
            row[9] = inv_no[r["account"]]
    write_csv(fp("reviews"), ["request_no", "received", "candidate_no", "family_name", "service", "questions",
                              "payment", "account_code", "amount_aud", "invoice_no", "completed"], rr)
    counts["reviews"] = len(rr)
    write_csv(fp("invoices"), ["invoice_no", "account_code", "account_name", "issue_date", "description",
                               "amount_aud", "gst_aud", "status", "paid_date"], led)
    counts["invoices"] = len(led)

    # 8 corporate accounts
    acc = []
    for code, name, dom, disc in W.FIRMS:
        acc.append([code, name, abn(rng), "accounts@%s" % dom, "Member firm agreement" if disc else "Standard terms",
                    ("%.1f" % disc).rstrip("0").rstrip("."), "2025-07-01", "2027-06-30"])
    write_csv(fp("accounts"), ["account_code", "account_name", "abn", "billing_email", "terms",
                               "exam_services_discount_pct", "agreement_from", "agreement_to"], acc)
    counts["accounts"] = len(acc)

    # 9-11 governing documents and the May minutes
    import docs
    docs.regulations(fp("regs"))
    docs.question_paper(fp("paper"))
    docs.minutes(fp("minutes"), w)

    # 12-13 distractors
    hist = docs.history_rows()
    write_csv(fp("history"), ["sitting", "candidates_examined", "accredited", "accreditation_rate_pct"], hist)
    counts["history"] = len(hist)
    docs.venue_holds(fp("venues"), rng)

    # every file carries the export day's clock
    stamp = dt.datetime(*P.STAMP).timestamp()
    for fn in os.listdir(out):
        os.utime(os.path.join(out, fn), (stamp, stamp))
    return counts


CPD = ["CPD workshop: NCC 2025 changes for certifiers", "CPD workshop: performance solutions in practice",
       "CPD seminar: occupation certificates and final inspections", "CPD workshop: waterproofing and AS 3740",
       "CPD seminar: building product safety and cladding", "CPD workshop: access and the Premises Standards"]


def pick_cpd(rng):
    return CPD[int(rng.integers(0, len(CPD)))] + " (group booking)"
