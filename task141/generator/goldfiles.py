"""The golden deliverables from the cut pack: the jail planning workbook (the 2027 projection and its parts, the pods,
the projection's sensitivity, violator bed-days by quarter, the felony probationers on supervision), the plan's
violator housing section as a memo, and the chart of monthly felony revocation admissions. Every figure is computed
once in golden.py and returned for figures.json."""
from __future__ import annotations

import datetime as dt

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import common as K  # noqa: E402
import golden as G  # noqa: E402
import postprocess as PP  # noqa: E402

HIST, PROJ, INK, INK2, SURF, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#fcfcfb", "#dddcd6"
QLAB = ["October to December 2025", "January to March 2026", "April to June 2026", "July to September 2026"]
BANDS = ["Under one year", "One year to under two years", "Two years to under three years", "Three years or more"]
MEMO_DATE = "16 October 2026"


def n0(x):
    return "{:,}".format(int(round(x)))


def figures(C):
    g = C["call"]
    tot = g["total"]
    p = g["parts"]
    f = {"call.pods": g["pods"], "call.admissions": g["printed"], "call.admissions_unrounded": round(tot, 1),
         "call.pods_ratio": round(tot / K.POD_SIZE, 2), "call.beds": g["pods"] * K.POD_BEDS, "pods_2026": K.PODS_2026,
         "pod_size": K.POD_SIZE, "pod_beds": K.POD_BEDS, "transition_terms": C["transition"],
         "parts.pending": round(p["pending"]), "parts.ordinary": round(p["ordinary"]),
         "parts.end_of_term": round(p["window"]), "parts.new_terms": round(p["new"]),
         "parts.transition": round(g["est"]["trans"]["window"]),
         "end_of_term.share_pct": round(100 * C["share"]["near"], 1),
         "end_of_term.year_before_pct": round(100 * C["share"]["year_before"], 1),
         "end_of_term.terms": C["share"]["reach"], "end_of_term.with_petition": C["share"]["wpet"],
         "trailing.felony_admissions": C["trailing"], "felony_terms": len(C["R"].cases),
         "open_felony_terms": len(C["R"].active)}
    for k, v in C["rungs"].items():
        f["rung.%s" % k] = round(v)
        f["rung.%s.pods" % k] = K.pods(v)
        f["rung.%s.printed" % k] = K.round_to(v, 100)
    for k, v in C["family"].items():
        key = k.replace(" ", "_")
        f["family.%s" % key] = round(v)
        f["family.%s.pods" % key] = K.pods(v)
        f["family.%s.printed" % key] = K.round_to(v, 100)
    fam = list(C["family"].values()) + [tot]
    f["family.low"], f["family.high"] = round(min(fam)), round(max(fam))
    A = C["ask_a"]
    for i in range(4):
        f["ask_a.q%d.felony" % (i + 1)] = int(A[i, 0])
        f["ask_a.q%d.misdemeanor" % (i + 1)] = int(A[i, 1])
    offs, sups = C["ask_b"]
    n_off, n_sup = C["ask_b_n"]
    for (code, _, _), v, n in zip(K.OFFICES, offs, n_off):
        f["ask_b.office.%s" % code] = K.round1(v)
        f["ask_b.office.%s.n" % code] = n
    for i, (v, n) in enumerate(zip(sups, n_sup)):
        f["ask_b.band%d" % i] = K.round1(v)
        f["ask_b.band%d.n" % i] = n
    mon = C["monthly"]
    s = sum(mon)
    f["monthly_2027"] = [round(x * tot / s, 1) for x in mon]
    f["quarter_2027"] = [round(sum(x * tot / s for x in mon[3 * q:3 * q + 3])) for q in range(4)]
    f["peak_month"] = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                       "November", "December"][max(range(12), key=lambda i: mon[i])]
    return f


# ---------------------------------------------------------------------------------------------------- workbook
def _widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


BOLD = Font(name="Calibri", bold=True)
HEAD = PatternFill("solid", fgColor="E6ECF2")
THIN = Side(style="thin", color="7F8C99")


def _title(ws, a, b):
    ws["A1"] = a
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws["A2"] = b
    ws["A2"].font = Font(name="Calibri", italic=True, size=9.5, color="595959")
    ws.append([])


def _head(ws, cols):
    ws.append(cols)
    for c in ws[ws.max_row]:
        c.font = BOLD
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    return ws.max_row


def _total(ws):
    for c in ws[ws.max_row]:
        c.font = BOLD
        c.border = Border(top=THIN)


def workbook(path, C, f):
    g = C["call"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Projection 2027"
    _title(ws, "Felony probation revocation admissions in 2027 under SB 26-118: projection for the Jail Operations Plan",
           "Okelan County Sheriff's Office, jail planning. Records to 30 September 2026 (extracts pulled 2 October "
           "2026). Admissions as the Board's instructions define them, section 3.")
    h = _head(ws, ["Part", "Admissions 2027", "How it is built"])
    rows = [
        ("Petitions pending at 30 September 2026", g["parts"]["pending"],
         "each pending petition at the record's revocation rate for its kind and its filing-to-decision days, decided "
         "in 2027"),
        ("Terms supervised at the extract: petitions through the term", g["parts"]["ordinary"],
         "monthly petition hazard by month on supervision over each term's months to its end under the Act, the "
         "record's revocation rate and filing-to-decision days"),
        ("Terms supervised at the extract: petitions filed as the term lapses", g["parts"]["window"],
         "%s per cent of terms reaching their last 120 days on supervision carry a petition filed in them; carried "
         "to each term's end under the Act, the windows of the terms section 4 ends on 31 March 2027 opening on 1 "
         "January 2027" % f["end_of_term.share_pct"]),
        ("of which the %s terms section 4 ends on 31 March 2027" % n0(C["transition"]),
         g["est"]["trans"]["window"], "the same petitions, filed from 1 January to 30 March 2027"),
        ("Terms whose supervision begins after the extract", g["parts"]["new"],
         "supervision starts at the trailing year's monthly rate, each on the supervision clock"),
    ]
    first = ws.max_row + 1
    for lab, v, how in rows:
        ws.append([lab, round(v), how])
        if lab.startswith("of which"):
            ws.cell(ws.max_row, 1).alignment = Alignment(indent=2, wrap_text=True, vertical="top")
    ws.append(["Projected admissions, 2027", round(g["total"]), None])
    _total(ws)
    ws.append(["Plan figure (nearest 100)", g["printed"], None])
    ws.cell(ws.max_row, 1).font = BOLD
    ws.cell(ws.max_row, 2).font = BOLD
    ws.append([])
    ws.append(["Violator pods for 2027 (one 64-bed pod for each 220 projected admissions or part of 220)", g["pods"],
               "%s admissions over 220 is %.2f pods; %d beds" % (n0(g["total"]), g["total"] / K.POD_SIZE,
                                                                  g["pods"] * K.POD_BEDS)])
    ws.cell(ws.max_row, 1).font = BOLD
    ws.cell(ws.max_row, 2).font = BOLD
    ws.append(["Violator pods staffed in 2026", K.PODS_2026, "%d beds" % (K.PODS_2026 * K.POD_BEDS)])
    ws.append([])
    ws.append(["Projected admissions by quarter of 2027", None, None])
    ws.cell(ws.max_row, 1).font = BOLD
    for q, v in zip(("January to March", "April to June", "July to September", "October to December"), f["quarter_2027"]):
        ws.append([q, v, None])
    for row in ws.iter_rows(min_row=first, max_row=ws.max_row):
        row[1].number_format = "#,##0"
        row[1].alignment = Alignment(horizontal="right", vertical="top")
        ind = 2 if (isinstance(row[0].value, str) and (row[0].value.startswith("of which") or row[0].value.endswith(
            (" to March", " to June", " to September", " to December")))) else 0
        row[0].alignment = Alignment(wrap_text=True, vertical="top", indent=ind)
        row[2].alignment = Alignment(wrap_text=True, vertical="top")
    ws.append([])
    ws.append(["Quarters add to the projection before rounding; the trailing year (October 2025 to September 2026) "
               "had %s felony probation revocation admissions." % n0(C["trailing"])])
    ws.cell(ws.max_row, 1).font = Font(name="Calibri", italic=True, size=9, color="595959")
    ws.freeze_panes = ws.cell(h + 1, 1)
    _widths(ws, [58, 14, 92])

    ws2 = wb.create_sheet("Sensitivity")
    _title(ws2, "The projection under other constructions",
           "Each line changes one choice and recomputes the 2027 projection from the same records.")
    _head(ws2, ["Construction", "Admissions 2027", "Nearest 100", "Pods"])
    ws2.append(["As projected (end-of-term window 120 days)", round(g["total"]), g["printed"], g["pods"]])
    for k, v in C["family"].items():
        ws2.append([k[0].upper() + k[1:], round(v), K.round_to(v, 100), K.pods(v)])
    ws2.append([])
    ws2.append(["Readings the records rule out", None, None, None])
    ws2.cell(ws2.max_row, 1).font = BOLD
    why = {"persistence": "the trailing year's admissions, before the Act moves any term's end",
           "rate_on_exposure": "the trailing year's admissions per month on supervision, over the months the Act "
                               "leaves in 2027",
           "one_clock_by_term": "petitions by month on supervision and term length, each term cut at its end under "
                                "the Act",
           "one_clock": "petitions by month on supervision and CSRS score, each term cut at its end under the Act",
           "two_clock_no_transition": "as projected, without the petitions of the terms the Act ends on 31 March 2027"}
    for k in ("persistence", "rate_on_exposure", "one_clock_by_term", "one_clock", "two_clock_no_transition"):
        v = C["rungs"][k]
        ws2.append([why[k][0].upper() + why[k][1:], round(v), K.round_to(v, 100), K.pods(v)])
    for row in ws2.iter_rows(min_row=5, max_row=ws2.max_row):
        for c in row[1:]:
            c.number_format = "#,##0"
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    ws2.append([])
    ws2.append(["The time-on-supervision readings book the end-of-term petitions at the expirations the record's terms "
                "had; the Act removes those dates, and the petitions follow the new ones."])
    ws2.cell(ws2.max_row, 1).font = Font(name="Calibri", italic=True, size=9, color="595959")
    ws2.freeze_panes = "A5"
    _widths(ws2, [86, 15, 12, 8])

    ws3 = wb.create_sheet("Bed-days 2025-26")
    _title(ws3, "Violator bed-days by quarter, October 2025 to September 2026",
           "Persons in the Detention Center at 00:00 county time on a probation revocation commitment, main building "
           "and annex; felony when the commitment revokes a felony term (Board instructions, section 5).")
    h3 = _head(ws3, ["Quarter", "Felony", "Misdemeanor", "All violators"])
    A = C["ask_a"]
    for i, q in enumerate(QLAB):
        ws3.append([q, int(A[i, 0]), int(A[i, 1]), int(A[i, 0] + A[i, 1])])
    ws3.append(["Four quarters", int(A[:, 0].sum()), int(A[:, 1].sum()), int(A.sum())])
    _total(ws3)
    for row in ws3.iter_rows(min_row=h3 + 1, max_row=ws3.max_row):
        for c in row[1:]:
            c.number_format = "#,##0"
    ws3.append([])
    ws3.append(["A misdemeanor commitment of a person then on felony probation is booked PV-FEL and counted here as "
                "misdemeanor: the commitment revokes the misdemeanor term."])
    ws3.cell(ws3.max_row, 1).font = Font(name="Calibri", italic=True, size=9, color="595959")
    ws3.freeze_panes = ws3.cell(h3 + 1, 1)
    _widths(ws3, [30, 12, 13, 13])

    ws4 = wb.create_sheet("Felony supervision")
    _title(ws4, "Felony probationers on supervision at 30 September 2026: term imposed at sentencing",
           "CaseTrak 2 terms open at the extract; term imposed is the term length less the months the Circuit Court's "
           "orders extended it (Board instructions, section 6).")
    h4 = _head(ws4, ["Supervising office", "Probationers", "Average term imposed (months)"])
    offs, sups = C["ask_b"]
    n_off, n_sup = C["ask_b_n"]
    for (code, name, _), v, n in zip(K.OFFICES, offs, n_off):
        ws4.append(["%s (%s)" % (name, code), n, K.round1(v)])
    ws4.append([])
    _head(ws4, ["Time on supervision at the extract", "Probationers", "Average term imposed (months)"])
    for lab, v, n in zip(BANDS, sups, n_sup):
        ws4.append([lab, n, K.round1(v)])
    ws4.append(["All felony probationers", sum(n_off), K.round1(sum(v * n for v, n in zip(offs, n_off)) / sum(n_off))])
    _total(ws4)
    for row in ws4.iter_rows(min_row=h4 + 1, max_row=ws4.max_row):
        if row[1].value is not None and not isinstance(row[1].value, str):
            row[1].number_format = "#,##0"
            row[2].number_format = "0.0"
    ws4.freeze_panes = ws4.cell(h4 + 1, 1)
    _widths(ws4, [40, 14, 30])

    wn = wb.create_sheet("Notes")
    notes = [
        ("Admission", "A person's commitment to the Detention Center on the revocation of a probation term the Adult "
                      "Probation Department supervises, counted once on the day the commitment begins; felony when a "
                      "revoked term is a felony term (Board instructions, section 3)."),
        ("Projection basis", "SB 26-118 as enrolled: a running felony term ends on the earlier of its scheduled "
                             "expiration and 24 months after supervision began, not before 31 March 2027; a term "
                             "imposed from 1 January 2027 runs no more than 24 months from the start of supervision. "
                             "The courts, the Department and the Sheriff acting as the records to the extract show "
                             "(Board instructions, section 4)."),
        ("Petition rates", "From every felony term in CaseTrak 1 and 2 since July 2016 and the Circuit Court's "
                           "petitions on them: the hazard by month on supervision outside each term's last 120 days, "
                           "the share of terms reaching their last 120 days with a petition filed in them, revocation "
                           "rates by kind and filing-to-decision days from petitions decided by the start of the "
                           "trailing year."),
        ("Scheduled expiration", "As in force on each day, from the term orders: tolling and extensions move it, early "
                                 "termination ends the term."),
        ("Pods", "County standard on file with the State Jail Standards Board (3 March 2021): one 64-bed violator pod "
                 "for each 220 felony probation revocation admissions projected for the plan year, or part of 220."),
        ("Bed-days", "Booking times in the new jail management system (from 4 February 2025) are UTC and are read in "
                     "county time; a person under bookings split by an annex move or a reclassification is counted "
                     "once a night."),
        ("Not used", "The daily 06:00 headcount and the Department's fiscal 2025 annual report."),
        ("Prepared", "Gina Yoder, jail planning analyst, %s." % MEMO_DATE)]
    wn.append(["Item", "Note"])
    for c in wn[1]:
        c.font = BOLD
        c.fill = HEAD
    for k, v in notes:
        wn.append([k, v])
    for row in wn.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
    _widths(wn, [22, 112])
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- memo
def _page_field(par):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for kind, text in (("begin", None), (None, " PAGE "), ("separate", None), (None, "1"), ("end", None)):
        r = par.add_run()
        if kind:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            r._r.append(fc)
        elif text.strip() == "PAGE":
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            r._r.append(it)
        else:
            r.text = text


def memo(path, C, f):
    import docx
    from docx.shared import Pt, RGBColor
    g = C["call"]
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    fp = doc.sections[0].footer.paragraphs[0]
    fp.text = "2027 Jail Operations Plan, section 3: violator housing. Draft for the commander. Page "
    _page_field(fp)
    for r in fp.runs:
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    p = doc.add_paragraph()
    r = p.add_run("OKELAN COUNTY SHERIFF'S OFFICE, DETENTION CENTER")
    r.bold = True
    r.font.size = Pt(10)
    p = doc.add_paragraph()
    r = p.add_run("Memorandum")
    r.bold = True
    r.font.size = Pt(15)
    for a_, b_ in (("To:", "Colleen Cameron, Detention Center Commander"),
                   ("Copy:", "Larry Pugh, Chief Probation Officer; Gloria Lynch, County Budget Director"),
                   ("From:", "Gina Yoder, jail planning analyst"),
                   ("Date:", MEMO_DATE),
                   ("Re:", "2027 Jail Operations Plan, section 3: violator housing under SB 26-118")):
        q = doc.add_paragraph()
        q.paragraph_format.space_after = Pt(0)
        q.add_run(a_ + " ").bold = True
        q.add_run(b_)
    doc.add_paragraph()
    p = doc.add_paragraph()
    r = p.add_run("Staff six violator pods for 2027: the Act brings felony revocation admissions up to about %s, not "
                  "down" % n0(g["printed"]))
    r.bold = True
    r.font.size = Pt(13)
    doc.add_paragraph(
        "The plan should carry %s felony probation revocation admissions for 2027 and staff six violator pods (%d "
        "beds), one more than this year. The projection is %s admissions, %.2f pods under our standard of one pod for "
        "each 220 projected admissions or part of 220. In the year to September 2026 the Detention Center admitted "
        "%s."
        % (n0(g["printed"]), g["pods"] * K.POD_BEDS, n0(g["total"]), g["total"] / K.POD_SIZE, n0(C["trailing"])))
    doc.add_paragraph(
        "SB 26-118 caps felony supervision at 24 months from 1 January 2027 and, under section 4, ends %s of the "
        "felony terms open at the extract on 31 March 2027. That shortens supervision, but it does not cut "
        "revocations, because a large part of our violation petitions are filed against the end of a term rather than "
        "during it. Officers file on matters still open as a term runs out (restitution, unfinished treatment, a "
        "pending charge) so the court keeps jurisdiction. Of the felony terms that reached their last 120 days on "
        "supervision with nothing pending, %s per cent had a petition filed in those days (%s of %s), against %s per "
        "cent in the same days a year earlier."
        % (n0(C["transition"]), f["end_of_term.share_pct"], n0(C["share"]["wpet"]), n0(C["share"]["reach"]),
           f["end_of_term.year_before_pct"]))
    doc.add_paragraph(
        "Those petitions follow each term's scheduled expiration, so when the Act moves the expirations they move "
        "with them. For the %s terms ending on 31 March 2027 they fall in the first quarter of 2027 and the "
        "commitments in the spring: %s admissions, the peak coming in %s. Through the rest of the year every term "
        "reaching 24 months on supervision ends, and its end-of-term petitions come with it."
        % (n0(C["transition"]), n0(g["est"]["trans"]["window"]), f["peak_month"]))
    doc.add_paragraph("Projected felony probation revocation admissions, 2027").runs[0].bold = True
    tb = doc.add_table(rows=1, cols=2)
    tb.style = "Table Grid"
    tb.rows[0].cells[0].text = "Part"
    tb.rows[0].cells[1].text = "Admissions"
    for lab, v in (("Petitions pending at 30 September 2026", g["parts"]["pending"]),
                   ("Terms on supervision at the extract, petitions through the term", g["parts"]["ordinary"]),
                   ("Terms on supervision at the extract, petitions filed as the term lapses", g["parts"]["window"]),
                   ("Terms beginning supervision after the extract", g["parts"]["new"]),
                   ("Projected admissions", g["total"])):
        row = tb.add_row().cells
        row[0].text = lab
        row[1].text = n0(v)
    for rr in tb.rows:
        for cell in rr.cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(9.5)
    q = doc.add_paragraph()
    r = q.add_run("Source: CaseTrak 1 and 2, the Circuit Court's term orders and violation petitions, extracts of 2 "
                  "October 2026. Parts are rounded and add to the projection before rounding.")
    r.italic = True
    r.font.size = Pt(8.5)
    doc.add_paragraph(
        "The usual survival projection, petitions by month on supervision with the CSRS score carried to each term's "
        "new end, gives about %s (three pods): it books the end-of-term petitions at expirations the Act removes. "
        "Keeping this year's %s gives five pods and misses the 31 March ends altogether. Every reasonable variant of "
        "the projection (an end-of-term window from 90 to 150 days, with or without the CSRS score, one revocation rate "
        "for both kinds of petition) gives %s to %s admissions and six pods; the workbook's Sensitivity sheet lists "
        "them."
        % (n0(K.round_to(C["rungs"]["one_clock"], 10)), n0(C["trailing"]), n0(f["family.low"]), n0(f["family.high"])))
    A = C["ask_a"]
    doc.add_paragraph(
        "Violator housing is close to full now. Felony violator bed-days ran %s, %s, %s and %s in the four quarters to "
        "September 2026 (misdemeanor %s, %s, %s and %s), an average of %s felony violators a night against the five "
        "pods' %d beds. The sixth pod should be open by February 2027, ahead of the spring."
        % (n0(A[0, 0]), n0(A[1, 0]), n0(A[2, 0]), n0(A[3, 0]), n0(A[0, 1]), n0(A[1, 1]), n0(A[2, 1]), n0(A[3, 1]),
           n0(A[:, 0].sum() / (K.EXTRACT - K.day("2025-10-01") + 1)), K.PODS_2026 * K.POD_BEDS))
    offs, sups = C["ask_b"]
    doc.add_paragraph(
        "For section 6 of the plan, the %s felony probationers on supervision at the extract were sentenced to %s "
        "months on average (Central %s, Northgate %s, Riverside %s, Eastfield %s); by time on supervision, %s months "
        "under one year, %s from one to two years, %s from two to three years and %s at three years or more. The "
        "workbook carries the counts."
        % (n0(sum(C["ask_b_n"][0])), "%.1f" % K.round1(sum(v * n for v, n in zip(offs, C["ask_b_n"][0])) /
                                                      sum(C["ask_b_n"][0])),
           "%.1f" % K.round1(offs[0]), "%.1f" % K.round1(offs[1]), "%.1f" % K.round1(offs[2]),
           "%.1f" % K.round1(offs[3]), "%.1f" % K.round1(sups[0]), "%.1f" % K.round1(sups[1]),
           "%.1f" % K.round1(sups[2]), "%.1f" % K.round1(sups[3])))
    q = doc.add_paragraph()
    r = q.add_run("Bed-days count each person in the Detention Center at 00:00 county time on a revocation commitment; a "
                  "misdemeanor commitment of a felony probationer (booked PV-FEL) counts as misdemeanor. Terms imposed "
                  "exclude extensions ordered since sentencing.")
    r.font.size = Pt(8.5)
    doc.core_properties.author = K.PEOPLE["analyst"]
    doc.core_properties.title = "2027 Jail Operations Plan, violator housing"
    doc.save(path)
    PP.normalize_docx(path, K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2026-10-14T15:06:00Z", "2026-10-16T19:41:00Z",
                      revision=5, total_time=142, seed="task141/memo", title="2027 Jail Operations Plan, violator housing",
                      company="Okelan County Sheriff's Office")


# ---------------------------------------------------------------------------------------------------- chart
def chart(path, C, f):
    hist = C["history"]
    xs = [dt.date(y, m, 15) for (y, m), _ in hist]
    ys = [v for _, v in hist]
    px = [dt.date(2027, m, 15) for m in range(1, 13)]
    py = f["monthly_2027"]
    fig, ax = plt.subplots(figsize=(10.4, 5.4), dpi=150)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    ax.plot(xs, ys, color=HIST, lw=2.0, label="Admitted, January 2019 to September 2026")
    ax.plot(px, py, color=PROJ, lw=2.0, ls=(0, (4, 2)), marker="o", ms=4.2,
            label="Projected for 2027 under SB 26-118 (%s)" % n0(C["call"]["total"]))
    ax.axvline(dt.date(2027, 3, 31), color=INK2, lw=0.9, ls=":")
    ax.text(dt.date(2027, 4, 8), max(py) * 1.02, "31 March 2027: %s running\nterms end under section 4" %
            n0(C["transition"]), fontsize=8.2, color=INK, va="bottom")
    top = px[max(range(12), key=lambda i: py[i])]
    ax.annotate("%s in %s" % (n0(max(py)), f["peak_month"]), xy=(top, max(py)), xytext=(dt.date(2025, 9, 1), max(py) * 0.97),
                fontsize=8.2, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    ax.set_ylabel("Felony probation revocation admissions a month", fontsize=9, color=INK2)
    ax.set_ylim(0, max(max(ys), max(py)) * 1.22)
    ax.set_xlim(dt.date(2018, 12, 1), dt.date(2028, 1, 15))
    ax.grid(axis="y", color=GRID, lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.spines["left"].set_color("#a9a8a2")
    ax.spines["bottom"].set_color("#a9a8a2")
    ax.tick_params(colors=INK2, labelsize=8.5)
    ax.legend(loc="upper left", frameon=False, fontsize=8.6)
    ax.set_title("Felony revocation admissions rise in spring 2027 as SB 26-118 ends running terms: six pods for %s"
                 % n0(C["call"]["printed"]), loc="left", fontsize=11.2, color=INK, fontweight="bold", pad=12)
    fig.text(0.01, 0.012, "Admissions: one a person and day the Circuit Court revoked a felony term. Source: Circuit "
                          "Court petitions, CaseTrak 1 and 2, extracts of 2 October 2026. Okelan County Sheriff's "
                          "Office, jail planning.", fontsize=7.4, color=INK2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, facecolor=SURF, metadata={"Software": None})
    plt.close(fig)


def write(gpath, C):
    f = figures(C)
    workbook(gpath(K.GOLD_BOOK), C, f)
    PP.normalize_ooxml(gpath(K.GOLD_BOOK), K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2026-10-12T14:20:00Z",
                       "2026-10-16T18:55:00Z", title="Violator housing plan 2027", excel=True,
                       company="Okelan County Sheriff's Office")
    memo(gpath(K.GOLD_MEMO), C, f)
    chart(gpath(K.GOLD_CHART), C, f)
    return f
