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
BANDS = ["Under one year", "One to under two years", "Two to under three years", "Three years or more"]
MEMO_DATE = "16 October 2026"


WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
        10: "ten"}
ORD = {6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth"}


def n0(x):
    return "{:,}".format(int(round(x)))


def figures(C):
    g = C["call"]
    tot = g["total"]
    p = g["parts"]
    info = g["info"]
    rt = C["rates"]
    f = {"call.pods": g["pods"], "call.admissions_unrounded": round(tot, 1),
         "call.pods_ratio": round(tot / K.POD_SIZE, 2), "call.beds": g["pods"] * K.POD_BEDS, "pods_2026": K.PODS_2026,
         "pod_size": K.POD_SIZE, "pod_beds": K.POD_BEDS, "transition_terms": C["transition"],
         "parts.pending": round(p["pending"]), "parts.ordinary": round(p["ordinary"]),
         "parts.end_of_term": round(p["window"]), "parts.new_terms": round(p["new"]),
         "parts.end_of_term.no_room": round(info["none"]), "parts.end_of_term.room": round(info["room"]),
         "parts.transition": round(info["transition"]),
         "capped.transition": C["capped"]["transition"], "capped.cap": C["capped"]["cap"],
         "capped.class_max": C["capped"]["class_max"], "capped.room": C["capped"]["room"],
         "rate.at_max_pct": round(100 * rt["n"], 1), "rate.with_room_pct": round(100 * rt["e"], 1),
         "rate.pooled_pct": round(100 * rt["pool"], 1), "rate.extended_with_room_pct": round(100 * rt["x_e"], 1),
         "rate.windows": rt["n_windows"], "rate.windows_at_max": rt["n_nonext"],
         "rate.windows_with_room": rt["n_windows"] - rt["n_nonext"], "rate.petitions_at_max": rt["hits_n"],
         "rate.petitions_with_room": rt["hits_e"],
         "trailing.felony_admissions": C["trailing"], "felony_terms": len(C["R"].cases),
         "open_felony_terms": len(C["R"].active), "call.admissions_whole": int(round(tot)),
         "param.end_of_term_window_days": 120, "param.window_family_days": [90, 105, 150],
         "param.act_cap_months": 24, "param.extension_months": K.EXT_MONTHS, "pods.six_cover": 6 * K.POD_SIZE,
         "pods.seven_cover": 7 * K.POD_SIZE}
    for k, v in C["rungs"].items():
        f["rung.%s" % k] = round(v)
        f["rung.%s.pods" % k] = K.pods(v)
    for k, v in C["family"].items():
        key = k.replace(" ", "_")
        f["family.%s" % key] = round(v)
        f["family.%s.pods" % key] = K.pods(v)
    fam = list(C["family"].values()) + [tot]
    f["family.low"], f["family.high"] = round(min(fam)), round(max(fam))
    A = C["ask_a"]
    for i in range(4):
        f["ask_a.q%d.felony" % (i + 1)] = int(A[i, 0])
        f["ask_a.q%d.misdemeanor" % (i + 1)] = int(A[i, 1])
    Bt = C["ask_b"]
    for code, _, _ in K.OFFICES:
        for k in range(4):
            f["ask_b.%s.band%d" % (code, k)] = Bt[(code, k)]
    f["ask_b.total"] = sum(Bt.values())
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
    info = g["info"]
    rt = C["rates"]
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
        ("Terms supervised at the extract: petitions as the term runs out", g["parts"]["window"],
         "each term's last 120 days before its end under the Act (from 1 January 2027 for the 31 March ends)"),
        ("of which terms with no room to extend (the Act or the class maximum)", info["none"],
         "%s per cent of the record's terms reaching their last 120 days at their class maximum had a petition filed "
         "in them; the Act leaves every capped term in that position" % f["rate.at_max_pct"]),
        ("of which terms that can still be extended", info["room"],
         "%s per cent had a petition, %s per cent were extended (%d months more, or to the latest end the Act "
         "allows if sooner, then as above)"
         % (f["rate.with_room_pct"], f["rate.extended_with_room_pct"], K.EXT_MONTHS)),
        ("Terms whose supervision begins after the extract", g["parts"]["new"],
         "supervision starts at the trailing year's monthly rate, each on the supervision clock"),
    ]
    first = ws.max_row + 1
    for lab, v, how in rows:
        ws.append([lab, round(v), how])
    ws.append(["Projected admissions, 2027", round(g["total"]), None])
    _total(ws)
    ws.append([])
    ws.append(["Violator pods for 2027 (one 64-bed pod for each %d projected admissions or part of %d)" % (
        K.POD_SIZE, K.POD_SIZE), g["pods"],
               "%s admissions over %d is %.2f pods; %d beds. Six pods cover %s admissions, seven %s"
               % (n0(g["total"]), K.POD_SIZE, g["total"] / K.POD_SIZE, g["pods"] * K.POD_BEDS, n0(6 * K.POD_SIZE),
                  n0(7 * K.POD_SIZE))])
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
    _widths(ws, [52, 14, 96])

    we = wb.create_sheet("End of term")
    _title(we, "What the record's terms did as they ran out, by room to extend",
           "Felony terms in CMS 1 and 2 reaching their last 120 days before the scheduled expiration then in force, "
           "alive and on supervision, July 2016 to August 2026. Room: the term in force against the longest term the "
           "Criminal Code allows for its class (Clerk's code table).")
    he = _head(we, ["Term reaching its last 120 days", "Terms", "With a petition filed in them", "Share with a petition",
                    "Extended in them", "Share extended"])
    n_e = rt["n_windows"] - rt["n_nonext"]
    for lab, n, hp, xs in (("At its class maximum (no room)", rt["n_nonext"], rt["hits_n"], rt["x_n"]),
                           ("With room under its class maximum", n_e, rt["hits_e"], rt["x_e"]),
                           ("All terms", rt["n_windows"], rt["hits"], rt["x_pool"])):
        we.append([lab, n, hp, hp / n, int(round(xs * n)), xs])
    _total(we)
    for row in we.iter_rows(min_row=he + 1, max_row=we.max_row):
        for j in (1, 2, 4):
            row[j].number_format = "#,##0"
        for j in (3, 5):
            row[j].number_format = "0.0%"
    we.append([])
    cp = C["capped"]
    we.append(["Open felony terms at the extract by their end under SB 26-118", None, None, None, None, None])
    we.cell(we.max_row, 1).font = BOLD
    for lab, v in (("Ended by section 4 on 31 March 2027 (scheduled expiration later)", cp["transition"]),
                   ("Ended on the day 24 months after supervision began (scheduled expiration later)", cp["cap"]),
                   ("Ending on their own expiration with less than a month of room (class maximum or the Act)",
                    cp["class_max"]),
                   ("Ending on their own expiration with room to extend", cp["room"])):
        we.append([lab, v])
        we.cell(we.max_row, 2).number_format = "#,##0"
    we.append([])
    we.append(["No order on or after 1 January 2027 may set a felony term's expiration past the day sections 3 and 4 "
               "allow (section 5), so a term ending on its cap has no room, whatever its class."])
    we.cell(we.max_row, 1).font = Font(name="Calibri", italic=True, size=9, color="595959")
    we.freeze_panes = we.cell(he + 1, 1)
    _widths(we, [62, 11, 16, 14, 13, 12])

    ws2 = wb.create_sheet("Sensitivity")
    _title(ws2, "The projection under other constructions",
           "Each line changes one choice and recomputes the 2027 projection from the same records.")
    _head(ws2, ["Construction", "Admissions 2027", "Pods"])
    ws2.append(["As projected (end-of-term window 120 days)", round(g["total"]), g["pods"]])
    for k, v in C["family"].items():
        ws2.append([k[0].upper() + k[1:], round(v), K.pods(v)])
    ws2.append([])
    ws2.append(["Readings the records rule out", None, None])
    ws2.cell(ws2.max_row, 1).font = BOLD
    why = {"pooled": "Every term's end at the record's end-of-term rates, the extensions the Act forbids treated as "
                     "lapses",
           "iia": "The extensions the Act forbids shared between petitions and lapses in the record's proportion",
           "full": "Every extension the Act forbids filed as a petition",
           "two_clock_no_extension": "Every term ending once at the record's pooled end-of-term rate",
           "persistence": "The trailing year's admissions, before the Act moves any term's end",
           "rate_on_exposure": "The trailing year's admissions per month on supervision, over the months the Act "
                               "leaves in 2027",
           "one_clock": "Petitions by month on supervision and CSRS score, each term cut at its end under the Act",
           "one_clock_by_term": "Petitions by month on supervision and term length, each term cut at its end under "
                                "the Act"}
    for k in ("pooled", "iia", "full", "two_clock_no_extension", "persistence", "rate_on_exposure", "one_clock",
              "one_clock_by_term"):
        v = C["rungs"][k]
        ws2.append([why[k], round(v), K.pods(v)])
    for row in ws2.iter_rows(min_row=5, max_row=ws2.max_row):
        for c in row[1:]:
            c.number_format = "#,##0"
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    ws2.append([])
    ws2.append(["The record's own end-of-term rate was earned by terms that could mostly still be extended; the "
                "terms already at their class maximum show what a term with no room draws."])
    ws2.cell(ws2.max_row, 1).font = Font(name="Calibri", italic=True, size=9, color="595959")
    ws2.freeze_panes = "A5"
    _widths(ws2, [92, 15, 8])

    ws3 = wb.create_sheet("Bed-days 2025-26")
    _title(ws3, "Violator bed-days by quarter, October 2025 to September 2026",
           "Persons in the Detention Center at 00:00 county time serving a commitment the court has ordered on a "
           "probation revocation, main building and annex; felony when the commitment revokes a felony term (Board "
           "instructions, section 5).")
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
    ws3.append(["A commitment counts from the night after the court orders it; a person the jail already held stays "
                "booked on the hold until the order reaches the records unit. A misdemeanor commitment of a person "
                "then on felony probation is booked PV-FEL and counted here as misdemeanor."])
    ws3.cell(ws3.max_row, 1).font = Font(name="Calibri", italic=True, size=9, color="595959")
    ws3.freeze_panes = ws3.cell(h3 + 1, 1)
    _widths(ws3, [30, 12, 13, 13])

    ws4 = wb.create_sheet("Felony supervision")
    _title(ws4, "Felony probationers on supervision at 30 September 2026, by supervising office",
           "CMS 2 terms open at the end of the extract; the supervising office is the office of the officer then "
           "supervising the term (officer assignments in effect on 30 September 2026). Board instructions, section 6.")
    h4 = _head(ws4, ["Supervising office"] + BANDS + ["All"])
    Bt = C["ask_b"]
    for code, name, _ in K.OFFICES:
        vals = [Bt[(code, k)] for k in range(4)]
        ws4.append(["%s (%s)" % (name, code)] + vals + [sum(vals)])
    tots = [sum(Bt[(o[0], k)] for o in K.OFFICES) for k in range(4)]
    ws4.append(["All offices"] + tots + [sum(tots)])
    _total(ws4)
    for row in ws4.iter_rows(min_row=h4 + 1, max_row=ws4.max_row):
        for c in row[1:]:
            c.number_format = "#,##0"
    ws4.append([])
    ws4.append(["CMS 2 keeps the office that took a term in; terms move between offices with their officers, and "
                "Eastfield took over the eastern townships' terms when it opened on 2 June 2025."])
    ws4.cell(ws4.max_row, 1).font = Font(name="Calibri", italic=True, size=9, color="595959")
    ws4.freeze_panes = ws4.cell(h4 + 1, 2)
    _widths(ws4, [24, 15, 18, 18, 18, 10])

    wn = wb.create_sheet("Notes")
    notes = [
        ("Admission", "A person's commitment to the Detention Center on the revocation of a probation term the Adult "
                      "Probation Department supervises, counted once on the day the court orders it; felony when a "
                      "revoked term is a felony term (Board instructions, section 3)."),
        ("Projection basis", "SB 26-118 as enrolled: a running felony term ends on the earlier of its scheduled "
                             "expiration and 24 months after supervision began, not before 31 March 2027; a term "
                             "imposed from 1 January 2027 runs no more than 24 months from the start of supervision; "
                             "no order from 1 January 2027 extends a term past those days. The courts, the Department "
                             "and the Sheriff acting as the records to the extract show (Board instructions, section "
                             "4)."),
        ("End-of-term rates", "From every felony term in CMS 1 and 2 since July 2016, the Circuit Court's petitions "
                              "and term orders: the share of terms reaching their last 120 days with a petition filed "
                              "in them and the share extended in them, split by whether the term in force (the term "
                              "imposed and every extension ordered before the 120 days began) had reached the longest "
                              "term for its class."),
        ("Petition rates", "The hazard by month on supervision outside each term's last 120 days; revocation rates by "
                           "kind and filing-to-decision days from petitions decided by the start of the trailing "
                           "year."),
        ("Scheduled expiration", "As in force on each day, from the term orders: tolling and extensions move it, early "
                                 "termination ends the term."),
        ("Pods", "County standard on file with the State Jail Standards Board (3 March 2021): one 64-bed violator pod "
                 "for each %d felony probation revocation admissions projected for the plan year, or part of %d."
                 % (K.POD_SIZE, K.POD_SIZE)),
        ("Bed-days", "Booking times in the new jail management system (from 4 February 2025) are UTC and are read in "
                     "county time; a person under bookings split by an annex move, the system replacement or a "
                     "reclassification is counted once a night."),
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
    info = g["info"]
    p = doc.add_paragraph()
    r = p.add_run("Staff %s violator pods for 2027: the Act takes away the extensions our expiring terms rely on, "
                  "and capped terms will draw petitions instead" % WORD[g["pods"]])
    r.bold = True
    r.font.size = Pt(13)
    doc.add_paragraph(
        "The plan should staff %s violator pods (%d beds) for 2027, %s more than this year. We project %s felony "
        "probation revocation admissions, %.2f pods under our standard of one pod for each %d projected admissions "
        "or part of %d: more than the %s six pods cover and within the %s of seven. In the year to September 2026 "
        "the Detention Center admitted %s."
        % (WORD[g["pods"]], g["pods"] * K.POD_BEDS, WORD[g["pods"] - K.PODS_2026], n0(g["total"]),
           g["total"] / K.POD_SIZE, K.POD_SIZE, K.POD_SIZE, n0(6 * K.POD_SIZE), n0(7 * K.POD_SIZE),
           n0(C["trailing"])))
    doc.add_paragraph(
        "When a felony term runs out with something still open (restitution owed, treatment unfinished, a pending "
        "charge) the court extends it if the term has room under the longest term the Criminal Code allows for its "
        "class, and the officer files a violation petition to keep the court's jurisdiction if it has none. Our "
        "record shows both. Of the felony terms that reached their last 120 days at their class maximum, about two in "
        "five had a petition filed in those days (%s of %s, %s per cent); of the terms with room, %s per cent had a "
        "petition and %s per cent were extended."
        % (n0(f["rate.petitions_at_max"]), n0(f["rate.windows_at_max"]), f["rate.at_max_pct"], f["rate.with_room_pct"],
           f["rate.extended_with_room_pct"]))
    doc.add_paragraph(
        "SB 26-118 caps felony supervision at 24 months and, from 1 January 2027, bars any order setting a term's "
        "expiration past that cap (section 5). Section 4 ends %s of the felony terms open at the extract on 31 March "
        "2027, and %s more end on the day 24 months after supervision began; none of them has room left, any more "
        "than the %s ending on their own expiration at their class maximum or within a month of the Act's limit. They "
        "will end the way our terms at their class maximum end, not the way the record's terms did on average, and "
        "their end-of-term petitions bring %s admissions, most in the spring: the peak comes in %s."
        % (n0(C["capped"]["transition"]), n0(C["capped"]["cap"]), n0(C["capped"]["class_max"]), n0(info["none"]),
           f["peak_month"]))
    doc.add_paragraph("Projected felony probation revocation admissions, 2027").runs[0].bold = True
    tb = doc.add_table(rows=1, cols=2)
    tb.style = "Table Grid"
    tb.rows[0].cells[0].text = "Part"
    tb.rows[0].cells[1].text = "Admissions"
    for lab, v in (("Petitions pending at 30 September 2026", g["parts"]["pending"]),
                   ("Terms on supervision at the extract, petitions through the term", g["parts"]["ordinary"]),
                   ("Terms on supervision at the extract, petitions as the term runs out", g["parts"]["window"]),
                   ("   of which terms with no room to extend (the Act or the class maximum)", info["none"]),
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
    r = q.add_run("Source: CMS 1 and 2, the Circuit Court's term orders and violation petitions, the Clerk's code table, "
                  "extracts of 2 October 2026. Parts are rounded and add to the projection before rounding.")
    r.italic = True
    r.font.size = Pt(8.5)
    doc.add_paragraph(
        "Projecting the capped terms at the record's average end-of-term rate gives about %s admissions and %s "
        "pods: that rate was earned by terms that could mostly still be extended, which the Act forbids. Sharing the "
        "lost extensions between petitions and lapses in the record's proportion gives about %s (%s pods), and "
        "filing every one of them as a petition about %s (%s); neither matches how our terms at their maximum "
        "actually ended. Every reasonable variant of the projection (an end-of-term window from 90 to 150 days, with "
        "or without the CSRS score, one revocation rate or two) gives %s to %s admissions and %s pods; the "
        "workbook's Sensitivity sheet lists them."
        % (n0(K.round_to(C["rungs"]["pooled"], 10)), WORD[K.pods(C["rungs"]["pooled"])],
           n0(K.round_to(C["rungs"]["iia"], 10)), WORD[K.pods(C["rungs"]["iia"])],
           n0(K.round_to(C["rungs"]["full"], 10)), WORD[K.pods(C["rungs"]["full"])], n0(f["family.low"]),
           n0(f["family.high"]), WORD[g["pods"]]))
    A = C["ask_a"]
    doc.add_paragraph(
        "Violator housing is near capacity now. Felony violator bed-days ran %s, %s, %s and %s in the four quarters to "
        "September 2026 (misdemeanor %s, %s, %s and %s), an average of %s felony violators a night against the %s "
        "pods' %d beds. The %s pods should be open by February 2027, ahead of the spring."
        % (n0(A[0, 0]), n0(A[1, 0]), n0(A[2, 0]), n0(A[3, 0]), n0(A[0, 1]), n0(A[1, 1]), n0(A[2, 1]), n0(A[3, 1]),
           n0(A[:, 0].sum() / (K.EXTRACT - K.day("2025-10-01") + 1)), WORD[K.PODS_2026], K.PODS_2026 * K.POD_BEDS,
           " and ".join(ORD[k] for k in range(K.PODS_2026 + 1, g["pods"] + 1))))
    Bt = C["ask_b"]
    tots = {o[0]: sum(Bt[(o[0], k)] for k in range(4)) for o in K.OFFICES}
    doc.add_paragraph(
        "For section 6 of the plan, the Department supervised %s felony probationers at the extract: Central %s, "
        "Northgate %s, Riverside %s and Eastfield %s, counted by the office of the officer supervising each term. The "
        "workbook breaks each office down by time on supervision."
        % (n0(sum(tots.values())), n0(tots["CEN"]), n0(tots["NGT"]), n0(tots["RVS"]), n0(tots["EFD"])))
    q = doc.add_paragraph()
    r = q.add_run("Bed-days count each person in the Detention Center at 00:00 county time serving a commitment the "
                  "court has ordered, from the night after the order; a misdemeanor commitment of a felony probationer "
                  "(booked PV-FEL) counts as misdemeanor. CMS 2 keeps the office that took a term in, so supervising "
                  "offices come from the officer assignments.")
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
    ax.text(dt.date(2027, 3, 24), max(py) * 1.08, "31 March 2027: %s running\nterms end under section 4" %
            n0(C["transition"]), fontsize=8.2, color=INK, va="bottom", ha="right")
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
    ax.set_title("Felony revocation admissions climb in spring 2027 as SB 26-118 ends terms with no room to extend: "
                 "%s violator pods" % WORD[C["call"]["pods"]], loc="left", fontsize=11.2, color=INK,
                 fontweight="bold", pad=12)
    fig.text(0.01, 0.012, "Admissions: one a person and day the Circuit Court revoked a felony term. Source: Circuit "
                          "Court petitions and term orders, CMS 1 and 2, extracts of 2 October 2026. Okelan County "
                          "Sheriff's Office, jail planning.", fontsize=7.4, color=INK2)
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
