"""The golden deliverables: the trustees' paper (docx, with the chart of 2027 starts) and the clinics' confirmed cures
workbook (xlsx, the ten counts with the course list behind them)."""
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import params as P
import postprocess

DOCX = "van_2027_trustee_paper.docx"
XLSX = "clinic_cures_2024-25.xlsx"
HALF = {"H1": "October 2024 to March 2025", "H2": "April to September 2025"}


def chart_png(F):
    order = F["order"]
    vals = [F["starts10"][s] for s in order]
    fig, ax = plt.subplots(figsize=(6.4, 3.0), dpi=150)
    y = list(range(len(order)))[::-1]
    ax.barh(y, vals, color=["#1F5C8B" if s == order[0] else "#A9B6C2" for s in order], height=0.58)
    ax.set_yticks(y)
    ax.set_yticklabels([P.SHORT[s] for s in order], fontsize=8.5)
    for yi, v in zip(y, vals):
        ax.text(v + 1.0, yi, "%d" % v, va="center", fontsize=8.5)
    ax.text(vals[0] / 2, y[0], "Van, 2027", va="center", ha="center", color="white", fontsize=8.5, fontweight="bold")
    fig.suptitle("Fenwold Recovery's new entrants would see the most people start treatment",
                 x=0.015, ha="left", fontsize=9.5, color="#222222")
    ax.set_xlabel("People started on hepatitis C treatment in 2027 (nearest 10)", fontsize=8.5)
    ax.set_xlim(0, max(vals) * 1.18)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="x", labelsize=8)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _page_field(par):
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    par._p.append(fld)


def _small(d, text):
    p = d.add_paragraph(text)
    p.runs[0].font.size = Pt(8)
    p.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    return p


def docx(path, F):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.1)
    sec.top_margin = Cm(1.8)
    foot = sec.footer.paragraphs[0]
    fr = foot.add_run("Brannock Trust. Trustees' meeting, 12 November 2026. For decision. Page ")
    fr.font.size = Pt(8)
    _page_field(foot)
    s10, f10 = F["starts10"], F["found10"]
    h = d.add_paragraph()
    r = h.add_run("Find-and-treat van 2027: Fenwold Recovery's new entrants")
    r.bold = True
    r.font.size = Pt(14)
    _small(d, "For decision. From %s, Director of Services, to the trustees' meeting of 12 November 2026. This paper "
              "completes the outreach team's plan of 6 October with the figures for the four settings." % P.DIRECTOR)
    p = d.add_paragraph()
    r = p.add_run("Recommendation: the van works with Fenwold Recovery's new entrants in 2027. It would start about %d "
                  "people on hepatitis C treatment there, %d more than at the needle exchange pharmacies' new "
                  "registrants, the next best at about %d." % (s10["DS"], F["gap10"], s10["NSP"]))
    r.bold = True
    d.add_paragraph(
        "The 2026 rota found the most active infections per test at the needle exchange pharmacies and in the hostels, "
        "and a year that repeated 2026 would put the van at the pharmacies. 2027 will not repeat 2026 in either place. "
        "From 1 April 2027 the integrated care board commissions pharmacist test and treat at every needle exchange "
        "pharmacy (its 2027/28 intentions, PH-12). Three pharmacies, Gorse Street, Halden and Morrow & Pike, have done "
        "it since 2025, and there the van found %d people with an active infection in %d tests, against %s per test at "
        "the other 21. From April every pharmacy will look like those three." % (F["pilot_found"], F["pilot_tested"],
                                                                            F["F_nonpilot"]))
    d.add_paragraph(
        "The hostels' figure in 2026 came from a first round. The van tested %d of the %d people on the hostels' 30 "
        "September lists and found %d of them with an active infection, whom it does not test again, so in 2027 it "
        "would meet the other %d with a negative test behind them; the infections still to find sit with the %d "
        "residents it has not tested and the %d people who arrive in a year. Fenwold Recovery's new entrants are a "
        "steady flow of people the van has not met, so the 2026 rates hold there."
        % (F["hh_tested"], F["census"], F["hh_found"], F["hh_negative"], F["hh_untested"], F["hh_arrivals"]))
    d.add_paragraph("What the van would find and start in 2027, by setting:")
    t = d.add_table(rows=1, cols=3)
    t.style = "Light List Accent 1"
    hdr = t.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Setting", "Active infections found", "Started on treatment"
    for s in F["order"]:
        c = t.add_row().cells
        c[0].text = P.SHORT[s]
        c[1].text = "%d" % f10[s]
        c[2].text = "%d" % s10[s]
    for row in t.rows:
        for c in row.cells[1:]:
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _small(d, "People, rounded to the nearest 10. Sources: the van's tablet export and the network's treatment register "
              "for 2026; the settings' returns, the hostels' resident lists and the pharmacies' registrations for the "
              "twelve months to September 2026; Fenwold Pathology for new infections among hostel residents.")
    d.add_picture(io.BytesIO(F["png"]), width=Cm(15.5))
    cap = d.add_paragraph("People started on treatment in 2027, by setting; the van's setting in blue.")
    cap.runs[0].font.size = Pt(8.5)
    h2 = d.add_paragraph()
    r = h2.add_run("How we sized it")
    r.bold = True
    d.add_paragraph(
        "Each setting's pool follows the plan: residents on 30 September 2026 and the arrivals of the twelve months to "
        "September, month for month. Each setting keeps the van's own 2026 share of people offered who took a test and "
        "of people found who started within twelve weeks, the latter over people found by 8 July 2026, the last day "
        "with twelve weeks of follow-up. At the pharmacies, January to March 2027 is at each pharmacy's own 2026 rate "
        "and April to December at the three test-and-treat pharmacies' rate. In the hostels, untested residents and "
        "arrivals are at the 2026 rate and the %d residents who tested negative at the homeless health clinic's rate "
        "of new infection, %d in %s person-years." % (F["hh_negative"], F["inc_events"], "{:,}".format(F["inc_py"])))
    _small(d, "Clinic outcomes for October 2024 to September 2025 are in the clinic cures workbook.")
    d.core_properties.author = P.DIRECTOR
    d.core_properties.title = "Find-and-treat van 2027"
    d.save(path)
    postprocess.scrub(path, P.ORG, "2026-10-21")
    postprocess.finish_office(path, "2026-10-19T09:10:00Z", "2026-10-21T15:35:00Z", P.ORG, person=P.DIRECTOR)


def xlsx(path, F):
    wb = Workbook()
    ws = wb.active
    ws.title = "Confirmed cures"
    thin = Side(style="thin", color="B0B7BE")
    head = PatternFill("solid", fgColor="DCE6EE")
    ws.append(["Clinic", "Courses ended " + HALF["H1"], "Courses ended " + HALF["H2"]])
    for c in P.CLINICS:
        nm = P.CLINIC_NAME[c]
        ws.append([nm[0].upper() + nm[1:], F["cures"]["%s_H1" % c], F["cures"]["%s_H2" % c]])
    ws.append(["All five clinics", sum(F["cures"]["%s_H1" % c] for c in P.CLINICS),
               sum(F["cures"]["%s_H2" % c] for c in P.CLINICS)])
    for cell in ws[ws.max_row]:
        cell.font = Font(bold=True)
        cell.border = Border(top=thin)
    ws.append([])
    ws.append(["Confirmed cure: hepatitis C RNA not detected on a sample taken 84 days or more after the course's last "
               "dose (network pathway 2026, section 3). Last dose: the last 28-day pack dispensed, plus 27 days."])
    ws.append(["Records to 30 September 2026. Clinical audit, %s network." % P.NETWORK])
    ws2 = wb.create_sheet("Courses")
    ws2.append(["Course", "Clinic", "Last dose", "Half-year", "Confirming RNA sample", "Confirmed cure"])
    for c in F["course_rows"]:
        ws2.append([c["ref"], c["clinic"], c["last"], c["half"], c["confirm"], "Yes" if c["confirm"] else "No"])
        ws2.cell(ws2.max_row, 3).number_format = "dd/mm/yyyy"
        if c["confirm"]:
            ws2.cell(ws2.max_row, 5).number_format = "dd/mm/yyyy"
    for w in (ws, ws2):
        for c in w[1]:
            c.font = Font(bold=True)
            c.fill = head
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=thin)
        w.freeze_panes = "A2"
        w.print_title_rows = "1:1"
    for col, wd in zip("ABC", (44, 22, 22)):
        ws.column_dimensions[col].width = wd
    for col, wd in zip("ABCDEF", (14, 8, 12, 26, 20, 14)):
        ws2.column_dimensions[col].width = wd
    wb.save(path)
    postprocess.scrub(path, P.NETWORK, "2026-10-21")
    postprocess.finish_office(path, "2026-10-14T10:02:00Z", "2026-10-21T15:12:00Z", P.NETWORK, person=P.CLIN_LEAD)


def write(golden_dir, F):
    os.makedirs(golden_dir, exist_ok=True)
    F = dict(F, png=chart_png(F))
    docx(os.path.join(golden_dir, DOCX), F)
    xlsx(os.path.join(golden_dir, XLSX), F)
