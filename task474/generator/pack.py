"""Cut the pack: registrations, both vendors' exports, the policy, the notice, the request and the context files."""
import csv
import datetime as dt
import io
import json
import os
import re
import zipfile
from email.message import EmailMessage
from email.utils import format_datetime

import numpy as np
import openpyxl
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import world as W

FILES = {
    "brindle": "brindle_theory_results_2020-2026.csv",
    "harrowgate": "harrowgate_theory_sittings_2026-04_2026-09.json",
    "register": "heatwise_candidate_register_2026-10-12.csv",
    "ap3": "ap3_pass_marks_and_standards.pdf",
    "notice": "theory_paper_change_notice_2026.pdf",
    "request": "pass_mark_paper_request.eml",
    "providers": "approved_training_providers_2026.xlsx",
    "venues": "exam_venues_2026.csv",
    "items": "harrowgate_item_statistics_2026-09.csv",
    "feedback": "candidate_feedback_2026.xlsx",
}
DISTRACTORS = ["items", "feedback"]
UK = dt.timezone.utc

SURNAMES = ("Smith Jones Taylor Brown Williams Wilson Johnson Davies Robinson Wright Thompson Evans Walker White "
            "Roberts Green Hall Wood Jackson Clarke Patel Khan Lewis James Phillips Mason Mitchell Rose Davis "
            "Rodriguez Cox Alexander Morgan Moore Hughes Edwards Hill Harris Martin Lee Ward Turner Parker Cooper "
            "Morris Bell Watson Cook Hussain Ali Begum Kaur Singh Murphy Kelly Price Bennett Shaw Lloyd Ellis "
            "Fisher Bailey Simpson Marshall Holmes Gray Chapman Webb Barker Gibson Dixon Knight Hunt Mills Palmer "
            "Matthews Foster Atkinson Burton Pearson Dawson Harvey Gill Barnes Hudson Lawrence Fox Butler Owen "
            "Holland Stevens Pearce Saunders Grant Kennedy Stewart Murray Ross Reid Henderson Hamilton Graham "
            "Kerr Wallace Russell Fraser Sutherland Lowe Booth Riley Ford Payne Hart Spencer Sharp Andrews "
            "Nicholson Jenkins Hayes Byrne O'Brien Doyle Howard Day Kay Clayton Mann Francis Bull Ingram Nash "
            "Pope Sinclair Tucker Whitehead Wilkinson Lambert Fletcher Rowe Briggs Hartley Holt Iqbal Mahmood "
            "Okafor Adeyemi Nowak Kowalski Silva Santos Costa Rossi Brennan Quinn Lynch Walsh Boyle").split()
INITIALS = "ABCDEFGHIJKLMNOPRSTW"


def _csv(path, header, rows, delim=","):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delim, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def _xlsx(path, sheets, creator, created, modified):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for title, rows, bold in sheets:
        ws = wb.create_sheet(title)
        for r in rows:
            ws.append(list(r))
        for i in bold:
            for c in ws[i]:
                c.font = Font(bold=True)
        for col, width in zip("ABCDEFGH", (14, 40, 26, 18, 16, 16, 16, 16)):
            ws.column_dimensions[col].width = width
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = created
    wb.properties.modified = modified
    wb.properties.title = None
    buf = io.BytesIO()
    wb.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in src.infolist():
            data = src.read(info.filename)
            if info.filename == "docProps/core.xml":
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              b"\\g<1>" + modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode() + b"\\g<2>", data)
            if info.filename == "docProps/app.xml":
                data = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                        b'<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
                        b'<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity>'
                        b'<ScaleCrop>false</ScaleCrop><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                        b'<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
            zi = zipfile.ZipInfo(info.filename, date_time=modified.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.6, leading=13, alignment=TA_LEFT, spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=13, leading=17, spaceAfter=4),
            "s": ParagraphStyle("s", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#4a5560")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, leading=14, spaceBefore=6),
            "p": base,
            "cell": ParagraphStyle("c", parent=base, fontSize=8.8, leading=11, spaceAfter=0)}


def pdf(path, blocks, title, author, created, modified, footer):
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#5b6670"))
        canvas.drawString(20 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            invariant=1)
    story = []
    for kind, val in blocks:
        if kind == "table":
            width = A4[0] - 40 * mm
            n = len(val[0])
            widths = [width * 0.32] + [width * 0.68 / (n - 1)] * (n - 1) if n > 1 else [width]
            rows = [[Paragraph(str(c).replace("&", "&amp;"), st["cell"]) for c in r] for r in val]
            t = Table(rows, colWidths=widths, hAlign="LEFT")
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8a949c")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
            story += [t, Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)


# ------------------------------------------------------------------------------------------------- identities

def identities(persons):
    """board numbers, provider numbers and names for every person; a person whose sittings have a gap of a year
    re-registers before the later booking under a new board number (and new provider numbers)"""
    r = W.rng("ids")
    used_b, used_br, used_hg, used_name = set(), set(), set(), set()

    def fresh(used, fmt, lo, hi):
        while True:
            x = fmt % int(r.integers(lo, hi))
            if x not in used:
                used.add(x)
                return x
    regs = []
    for pid, p in enumerate(persons):
        while True:
            nm = (SURNAMES[int(r.integers(0, len(SURNAMES)))],
                  "".join(INITIALS[int(i)] for i in r.integers(0, len(INITIALS), size=1 + int(r.random() < 0.45))))
            if (nm, p["dob"]) not in used_name:
                used_name.add((nm, p["dob"]))
                break
        p["name"] = nm
        ss = p["sittings"]
        cut = None
        for i in range(1, len(ss)):
            if (ss[i]["date"] - ss[i - 1]["date"]).days >= 330 and r.random() < 0.7:
                cut = i
                break
        spans = [(0, len(ss))] if cut is None else [(0, cut), (cut, len(ss))]
        for k, (a, b) in enumerate(spans):
            sub = ss[a:b]
            reg = p["registered"] if k == 0 else sub[0]["date"] - dt.timedelta(days=int(r.integers(10, 60)))
            prov = p["provider"]
            if prov in W.MERGED and reg >= W.MERGED[prov][1]:
                prov = W.MERGED[prov][0]
            row = {"pid": pid, "board": fresh(used_b, "HQ%06d", 100000, 999999), "registered": reg,
                   "provider": prov, "brindle": "", "harrowgate": ""}
            if any(s["vendor"] == "old" for s in sub):
                row["brindle"] = fresh(used_br, "B%07d", 1000000, 9999999)
            if any(s["vendor"] == "new" for s in sub):
                row["harrowgate"] = fresh(used_hg, "HG%06d", 100000, 999999)
            for s in sub:
                s["board"] = row["board"]
                s["vid"] = row["brindle"] if s["vendor"] == "old" else row["harrowgate"]
            regs.append(row)
    return regs


# ------------------------------------------------------------------------------------------------- the files

def write_register(persons, regs, path):
    rows = []
    for g in sorted(regs, key=lambda g: (g["registered"], g["board"])):
        p = persons[g["pid"]]
        rows.append([g["board"], p["name"][0], p["name"][1], p["dob"].isoformat(), g["registered"].isoformat(),
                     g["provider"], g["brindle"], g["harrowgate"]])
    _csv(path, ["board_number", "surname", "initials", "date_of_birth", "registered_on", "training_provider",
                "brindle_candidate_id", "harrowgate_candidate_id"], rows)


def venues():
    sites = [("HTS-%02d" % k, nm) for k, nm in enumerate(
        ["Manchester Spinningfields", "Bristol Harbourside", "Birmingham Brindleyplace", "London Southwark",
         "Leeds Dock", "Norwich Whitefriars", "Southampton Bargate", "Newcastle Gateshead Quays", "Nottingham Trent",
         "Exeter Quay"], start=1)]
    return sites


def write_brindle(persons, path):
    r = W.rng("brindle")
    centres = W.BRINDLE_CENTRES
    rows = []
    for p in persons:
        home = centres[int(r.integers(0, len(centres)))][0]
        for s in p["sittings"]:
            if s["vendor"] != "old":
                continue
            form = "HPI3-%s" % "ABCD"[((s["date"].year - 2020) * 4 + (s["date"].month - 1) // 3) % 4]
            status = {"sat": "SAT", "absent": "ABS", "void": "VOID"}[s["status"]]
            rows.append([s["vid"], home if r.random() < 0.9 else centres[int(r.integers(0, len(centres)))][0],
                         s["date"].strftime("%d/%m/%Y"), form, status, s.get("score", "") if status == "SAT" else ""])
    rows.sort(key=lambda x: (dt.datetime.strptime(x[2], "%d/%m/%Y"), x[1], x[0]))
    _csv(path, ["candidate_id", "centre", "sitting_date", "form", "status", "scaled_score"], rows)


def uk_offset(d):
    """British Summer Time: the last Sunday of March to the last Sunday of October"""
    def last_sunday(y, m):
        x = dt.date(y, m, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return 1 if last_sunday(d.year, 3) <= d < last_sunday(d.year, 10) else 0


def write_harrowgate(persons, path):
    r = W.rng("harrowgate")
    sites = venues()
    out = []
    seq = 0
    for p in persons:
        for s in p["sittings"]:
            if s["vendor"] != "new":
                continue
            seq += 1
            remote = r.random() < 0.62
            if remote:
                # remote sittings run from 07:00 to 23:59 UK time; a share start in the late evening
                pw = np.array([.05, .07, .08, .08, .07, .07, .07, .07, .07, .07, .08, .08, .07, .05, .04, .02])
                hour = int(r.choice([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], p=pw / pw.sum()))
            else:
                hour = int(r.choice([9, 10, 11, 13, 14, 15]))
            minute = int(r.integers(0, 60))
            local = dt.datetime.combine(s["date"], dt.time(hour, minute))
            utc = local - dt.timedelta(hours=uk_offset(s["date"]))
            rec = {"sitting_ref": "HGS-%s-%05d" % (s["date"].strftime("%y%m"), seq),
                   "candidate_id": s["vid"], "mode": "remote" if remote else "test_site",
                   "site": "" if remote else sites[int(r.integers(0, len(sites)))][0],
                   "started_at": utc.strftime("%Y-%m-%dT%H:%M:00Z")}
            if s["status"] == "sat":
                u = r.random()
                if u < 0.05:
                    # held for the proctor's review: the export keeps the held record and the release beside it
                    out.append(dict(rec, raw_mark=None, review="held"))
                    rel = utc + dt.timedelta(days=int(r.integers(2, 12)), hours=int(r.integers(1, 9)))
                    rec = dict(rec)
                    rec.update({"raw_mark": s["score"], "review": "released", "released_at": rel.strftime("%Y-%m-%dT%H:%M:00Z")})
                else:
                    rec.update({"raw_mark": s["score"], "review": "cleared"})
            else:
                rec.update({"raw_mark": None, "review": "no_show" if s["status"] == "absent" else "voided"})
            out.append(rec)
    out.sort(key=lambda x: (x["started_at"], x["sitting_ref"]))
    payload = {"provider": P.NEW_VENDOR, "client": P.ORG, "assessment": P.PAPER, "items": P.NEW_ITEMS,
               "exported_at": "2026-10-12T06:30:00Z", "sittings": out}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1)
        f.write("\n")


def write_venues(path):
    rows = [[c, nm, P.OLD_VENDOR, "test centre", "31/03/2026"] for c, nm in W.BRINDLE_CENTRES]
    rows += [[c, nm, P.NEW_VENDOR, "test site", ""] for c, nm in venues()]
    _csv(path, ["venue_code", "venue", "provider", "type", "closed_on"], rows)


def write_providers(path):
    rows = [("Code", "Provider", "Region", "Approved", "Note")]
    r = W.rng("providers")
    for code, nm, region in W.PROVIDERS:
        approved = dt.date(int(r.integers(2014, 2021)), int(r.integers(1, 13)), 1).strftime("%m/%Y")
        note = ""
        if code in W.MERGED:
            note = "Merged into %s on %s; candidates registered before the merger keep %s on the register" % (
                W.MERGED[code][0], W.MERGED[code][1].strftime("%d %B %Y").lstrip("0"), code)
        if code in W.GAS_PROVIDERS:
            note = (note + "; " if note else "") + "Also runs the conversion course for qualified gas engineers"
        rows.append((code, nm, region, approved, note))
    _xlsx(path, [("Approved providers", rows, [1])], "Heatwise Qualifications", dt.datetime(2026, 2, 9, 10, 12),
          dt.datetime(2026, 9, 18, 15, 41))


def write_items(path):
    r = W.rng("items")
    topics = ["Heat loss and emitter sizing", "Refrigerant circuits", "Hydraulics and buffers", "Controls",
              "Electrical safety", "Regulations and MCS", "Commissioning", "Customer handover"]
    rows = []
    for i in range(1, P.NEW_ITEMS + 1):
        p = float(np.clip(r.normal(0.6, 0.14), 0.18, 0.95))
        pb = float(np.clip(r.normal(0.33, 0.08), 0.05, 0.55))
        rows.append(["Q%02d" % i, topics[(i - 1) % len(topics)], "%.3f" % p, "%.3f" % pb, "check key" if pb < 0.15 else ""])
    _csv(path, ["item", "topic", "facility", "point_biserial", "panel_note"], rows)


def write_feedback(path):
    r = W.rng("feedback")
    qs = ["The booking process was clear", "The paper covered the syllabus", "The time allowed was enough",
          "The remote proctoring check-in worked", "I would recommend the qualification"]
    rows = [("Question", "Provider", "Responses", "Mean rating (1 to 5)")]
    for q in qs:
        for v in (P.OLD_VENDOR, P.NEW_VENDOR):
            if "remote" in q and v == P.OLD_VENDOR:
                continue
            rows.append((q, v, int(r.integers(380, 1400)), round(float(r.uniform(3.2, 4.4)), 2)))
    _xlsx(path, [("Survey 2026", rows, [1])], "Heatwise Qualifications", dt.datetime(2026, 7, 2, 9, 5),
          dt.datetime(2026, 10, 6, 16, 22))


def write_ap3(path):
    b = [("t", "Assessment Policy AP-3: Pass marks and standards"),
         ("s", "%s. Approved by the Board on 11 March 2025. Owner: the Head of Qualifications. Applies to the "
               "theory papers of the %s." % (P.ORG, P.QUAL)),
         ("h", "1. The standard"),
         ("p", "The theory paper's standard is a scaled score of 65 on the scale %s reports, set by the Board in 2019. "
               "A candidate passes when their result is at or above the pass mark that carries that standard on the "
               "paper they sat." % P.OLD_VENDOR),
         ("h", "2. A new paper"),
         ("p", "When the paper or its provider changes, the Board sets the new paper's pass mark from the new paper's "
               "sittings. The pass mark is the lowest raw mark that no larger share of an equivalent group of "
               "candidates reaches than reaches 65 on the established scale. An equivalent group is a group whose "
               "proficiency would be the same whichever paper it sat."),
         ("p", "Results on a new paper are held until the Board sets its pass mark. The pass mark applies to the held "
               "results and to every later sitting of the paper until the paper changes again."),
         ("h", "3. Resits"),
         ("p", "A candidate who does not pass may resit. From 1 October 2025 a candidate scoring 55 to 64 may resit once "
               "free of charge, booked within six weeks of the result; a candidate scoring under 55 may resit no "
               "sooner than six months after the sitting, once the refresher module is complete."),
         ("h", "4. Records"),
         ("p", "Each provider reports results against its own candidate numbers, and the Board's candidate register "
               "ties them to board numbers. A sitting the provider voids, or one the candidate does not attend, is "
               "not a sitting of the paper.")]
    pdf(path, b, "AP-3 Pass marks and standards", P.ORG, "D:20250311142000+00'00'", "D:20250311142000+00'00'",
        "%s  |  AP-3 Pass marks and standards  |  March 2025" % P.ORG)


def write_notice(path):
    b = [("t", "The theory paper from 1 April 2026"),
         ("s", "%s, notice to approved training providers and candidates. Issued 2 February 2026." % P.ORG),
         ("p", "From 1 April 2026 %s delivers the %s in place of %s. %s's last sittings are on 31 March 2026 at its "
               "test centres." % (P.NEW_VENDOR, P.PAPER, P.OLD_VENDOR, P.OLD_VENDOR)),
         ("table", [["", "To 31 March 2026", "From 1 April 2026"],
                    ["Provider", P.OLD_VENDOR, P.NEW_VENDOR],
                    ["Paper", "Forms A to D, results on a scaled score from 0 to 100",
                     "60 questions in 90 minutes, results as a raw mark out of 60"],
                    ["Where", "Brindle test centres", "Remote with live proctoring, 07:00 to 23:59 UK time, or a "
                                                      "Harrowgate test site"],
                    ["Results", "Issued within ten working days",
                     "Held until the Board sets the pass mark at its meeting on 4 November 2026"]]),
         ("p", "Syllabus, eligibility and fees are unchanged. Candidates book through their training provider as "
               "now; a candidate who sat with %s keeps their board number." % P.OLD_VENDOR)]
    pdf(path, b, "The theory paper from 1 April 2026", P.ORG, "D:20260130113000+00'00'", "D:20260202090500+00'00'",
        "%s  |  Notice to providers and candidates  |  February 2026" % P.ORG)


def write_request(path):
    m = EmailMessage()
    m["From"] = "Laura Kay <laura.kay@heatwisequals.org.uk>"
    m["To"] = "Assessment Analysis <analysis@heatwisequals.org.uk>"
    m["Cc"] = "Alan Clayton <alan.clayton@heatwisequals.org.uk>"
    m["Subject"] = "Board paper: the theory paper pass mark"
    m["Date"] = format_datetime(dt.datetime(2026, 10, 13, 9, 14, tzinfo=dt.timezone(dt.timedelta(hours=1))))
    m["Message-ID"] = "<20261013091402.4471@heatwisequals.org.uk>"
    m.set_content(
        "Hello,\n\n"
        "The Board sets the pass mark on Harrowgate's theory paper at its meeting on 4 November, under AP-3, and the "
        "held results go out the week after. Alan and I would like the paper to the Board by 28 October.\n\n"
        "The folder has Brindle's results export, Harrowgate's sittings to 30 September, the register extract of "
        "12 October and the policy. Alan has also asked for the monthly sittings this year, the new paper's "
        "candidates by training provider and Brindle's first-time pass rates for the last five years, which the Board "
        "keeps in its standards file.\n\n"
        "Thanks,\n\n"
        "Laura Kay\nHead of Qualifications, %s\n" % P.ORG)
    with open(path, "wb") as f:
        f.write(bytes(m))


def build(target):
    os.makedirs(target, exist_ok=True)
    persons = W.build()
    regs = identities(persons)
    f = lambda k: os.path.join(target, FILES[k])
    write_register(persons, regs, f("register"))
    write_brindle(persons, f("brindle"))
    write_harrowgate(persons, f("harrowgate"))
    write_venues(f("venues"))
    write_providers(f("providers"))
    write_items(f("items"))
    write_feedback(f("feedback"))
    write_ap3(f("ap3"))
    write_notice(f("notice"))
    write_request(f("request"))
    stamp = dt.datetime(2026, 10, 12, 7, 0).timestamp()
    for k in FILES:
        os.utime(f(k), (stamp, stamp))
    return persons, regs
