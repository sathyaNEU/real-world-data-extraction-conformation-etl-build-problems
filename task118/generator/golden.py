"""The golden deliverables: the Treasury's paper to the Council of Ministers (docx, with the chart) and the envelope
workbook (xlsx) with the appraisal and Customs' excise on releases for the Budget's excise annex."""
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

import figs as FG
import params as P
import postprocess
import solve as SV

DOCX = "budget_2027_duty_cut_paper.docx"
XLSX = "budget_2027_duty_envelope.xlsx"
AUTHOR = P.PEOPLE["economist"]
LOWER = {"BEER": "beer", "CIDR": "cider", "WINE": "wine", "SPIR": "spirits", "FUEL": "road fuel"}


def chart_png(F):
    order = F["order"]
    vals = [F["duties"][c]["eb_k"] for c in order]
    fig, ax = plt.subplots(figsize=(6.4, 2.9), dpi=150)
    colours = ["#7A2E39" if c == order[0] else "#B9AEA6" for c in order]
    y = list(range(len(order)))[::-1]
    ax.barh(y, vals, color=colours, height=0.58)
    ax.set_yticks(y)
    ax.set_yticklabels([F["duties"][c]["name"] for c in order], fontsize=8.5)
    for yi, v in zip(y, vals):
        ax.text(v + 12, yi, "%d" % v, va="center", fontsize=8.5)
    ax.text(vals[0] / 2, y[0], "Recommended", va="center", ha="center", color="white", fontsize=8.5,
            fontweight="bold")
    fig.suptitle("The spirits cut removes more than twice what any other duty's would",
                 x=0.015, ha="left", fontsize=9.5, color="#222222")
    ax.set_xlabel("GBP thousand, 2027", fontsize=8.5)
    ax.set_xlim(0, max(vals) * 1.16)
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


def docx(path, F):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    sec = d.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.1)
    sec.top_margin = Cm(1.8)
    foot = sec.footer.paragraphs[0]
    fr = foot.add_run("%s, %s. Meeting of 2 December 2026. Budget 2027 amendment. Page " % (P.PANEL, P.ASSEMBLY))
    fr.font.size = Pt(8)
    _page_field(foot)
    w, r = F["winner"], F["runner"]
    W, R = F["duties"][w], F["duties"][r]
    h = d.add_paragraph()
    run = h.add_run("Budget 2027: the duty envelope should go to %s" % LOWER[w])
    run.bold = True
    run.font.size = Pt(14)
    p = d.add_paragraph("For decision. 26 October 2026. From %s, the panel's expert adviser, to the %s (Chair, Deputy "
                        "%s) for its meeting on 2 December 2026 and its amendment to the 2027 Budget, debated on 15 "
                        "December." % (AUTHOR, P.PANEL, P.PEOPLE["minister"]))
    p.runs[0].font.size = Pt(8.5)
    p.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    p = d.add_paragraph()
    run = p.add_run("Recommendation: the panel's amendment gives the GBP %.1f million to %s duty, cutting its 2027 "
                    "rate of GBP %.2f a litre by about a fifth from 1 January 2027. The cut removes about GBP %.1f "
                    "million of excess burden in 2027. The next best is %s duty, which would remove about GBP %.1f "
                    "million." % (F["envelope_m"], LOWER[w], W["rate27"], F["winner_m"], LOWER[r],
                                  F["runner_m"]))
    run.bold = True
    d.add_paragraph(
        "Every litre a duty cut adds to what people buy carries the whole of the duty and GST still charged on it, and "
        "that is where most of the gain is. Spirits carry the largest wedge of the alcohol duties, %d per cent of the "
        "shelf price, and their buyers respond within months. Road fuel carries a larger wedge still, but drivers "
        "change what they buy over years rather than months, so in 2027 a fuel cut would remove less than a fifth "
        "of what the spirits cut removes. Cider buyers respond most to price, but cider's wedge is small, so most of "
        "what a cider cut gives back is the duty itself." % round(100 * W["wedge_share"]))
    d.add_paragraph("The envelope given to each duty in turn:")
    t = d.add_table(rows=1, cols=4)
    t.style = "Light List Accent 1"
    hdr = t.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = ("Duty", "2027 rate (GBP a litre)", "Cut (GBP a litre)",
                                                          "Excess burden removed in 2027 (GBP thousand)")
    for c in F["order"]:
        x = F["duties"][c]
        cells = t.add_row().cells
        cells[0].text = x["name"]
        dp = "%.4f" if c == "FUEL" else "%.2f"      # road fuel's rate is set to a hundredth of a penny
        cells[1].text = dp % x["rate27"]
        cells[2].text = dp % x["cut"]
        cells[3].text = "%d" % x["eb_k"]
    for row in t.rows:
        for c in row.cells[1:]:
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    src = d.add_paragraph("Each cut is the one that gives up GBP %.1f million of duty and GST in 2027 once buyers have "
                          "responded. Sources: Eskerholm Statistics Office, duty-paid clearances and shelf prices, "
                          "2008 to 2026; Treasury duty rates." % F["envelope_m"])
    src.runs[0].font.size = Pt(8)
    src.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    d.add_picture(io.BytesIO(F["png"]), width=Cm(15.5))
    cap = d.add_paragraph("Excess burden removed in 2027 by each duty's cut; the recommended duty in red.")
    cap.runs[0].font.size = Pt(8.5)
    h2 = d.add_paragraph()
    run = h2.add_run("How it was appraised")
    run.bold = True
    d.add_paragraph(
        "As the appraisal manual sets out, the starting point is the latest four quarters of duty-paid clearances, "
        "each standing for the same quarter of 2027, at the latest shelf prices with the 2027 rates already set "
        "(%d per cent above 2026). A cut passes in full to the shelf price with GST on top." % F["uprate_pct"])
    d.add_paragraph(
        "How far buyers respond, and how fast, comes from the quarterly clearances and prices since %s. For each duty "
        "we fitted log clearances on the quarter, log shelf price and the previous quarter's log clearances, which "
        "gives the response in the first quarter and the share of the gap closed each quarter after. In 2027 the "
        "response builds through the year: by its fourth quarter spirits have made %d per cent of their long-run "
        "response and road fuel %d per cent."
        % (F["first_quarter"][0], round(100 * (1 - F["duties"]["SPIR"]["lam"] ** 4)),
           round(100 * (1 - F["duties"]["FUEL"]["lam"] ** 4))))
    d.add_paragraph(
        "Each duty's cut is set so that the duty and GST given up in 2027, after buyers respond, is GBP %.1f million. "
        "The excess burden it removes is the value of the extra litres to the people who buy them less what they cost "
        "to supply, quarter by quarter along the demand curve fitted for that duty: the duty and GST still charged on "
        "each extra litre, plus half the cut." % F["envelope_m"])
    note = d.add_paragraph("The cut is permanent and goes on removing excess burden after 2027; the manual appraises "
                           "the Budget year only (section 4). Health, road safety and environmental effects are reported "
                           "by the departments concerned (section 9).")
    note.runs[0].font.size = Pt(8)
    note.runs[0].font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    d.core_properties.author = AUTHOR
    d.core_properties.title = "Budget 2027: the duty envelope"
    d.save(path)
    postprocess.scrub(path, P.ASSEMBLY, "2026-10-26")
    postprocess.finish_office(path, "2026-10-21T08:40:00Z", "2026-10-26T16:05:00Z", P.ASSEMBLY, person=AUTHOR)


def xlsx(path, F):
    wb = Workbook()
    ws = wb.active
    ws.title = "Appraisal 2027"
    thin = Side(style="thin", color="B0B7BE")
    head = PatternFill("solid", fgColor="E7DFD8")
    ws.append(["Duty", "Clearances, latest four quarters (000 litres)", "Shelf price 2027 before the cut (GBP a litre)",
               "Producer price (GBP a litre)", "2027 rate already set (GBP a litre)",
               "Duty and GST, share of the shelf price", "Response in the first quarter", "Share of the gap closed "
               "each quarter", "Response by Q1 2027", "Response by Q2 2027", "Response by Q3 2027",
               "Response by Q4 2027", "Cut (GBP a litre)", "Rate after the cut (GBP a litre)",
               "Extra litres bought in 2027 (000)", "Excess burden removed in 2027 (GBP thousand)"])
    for c in F["order"]:
        x = F["duties"][c]
        ws.append([x["name"], x["litres_k"], x["shelf"], x["producer"], x["rate27"], x["wedge_share"], x["beta"],
                   round(1 - x["lam"], 3)] + x["eps"] + [x["cut"], x["new_rate"], x["extra_litres_k"], x["eb_k"]])
    for row in ws.iter_rows(min_row=2, max_row=6):
        row[1].number_format = "#,##0.0"
        for k in (2, 3):
            row[k].number_format = "0.00"
        row[4].number_format = "0.0000"
        for k in range(5, 12):
            row[k].number_format = "0.000"
        for k in (12, 13):
            row[k].number_format = "0.0000"
        row[14].number_format = "#,##0.0"
        row[15].number_format = "#,##0"
    ws.append([])
    ws.append(["Envelope: GBP %.1f million of duty and GST given up in 2027 after buyers respond, given to one duty."
               % F["envelope_m"]])
    ws.append(["Recommended: %s, about GBP %.1f million of excess burden removed in 2027; next best %s, about GBP "
               "%.1f million." % (F["winner_name"].lower(), F["winner_m"], F["runner_name"].lower(), F["runner_m"])])
    ws2 = wb.create_sheet("Excise on releases")
    ws2.append(["Duty"] + [FG.QUARTER_LABEL[q] for q in P.ASK_QUARTERS])
    for c, *_ in P.DUTIES:
        ws2.append([F["duties"][c]["name"]] + [F["asks_k"][c][q] for q in P.ASK_QUARTERS])
    ws2.append(["Five duties"] + [SV.thousand(sum(F["asks_exact"][c][q] for c, *_ in P.DUTIES)) for q in P.ASK_QUARTERS])
    for row in ws2.iter_rows(min_row=2, max_row=7):
        for cell in row[1:]:
            cell.number_format = "#,##0.0"
    for cell in ws2[7]:
        cell.font = Font(bold=True)
        cell.border = Border(top=thin)
    ws2.append([])
    ws2.append(["GBP thousand. Excise accounted for on releases from bonded warehouses (procedure 4071): each release "
                "once, as the last declaration correcting it, in the quarter it was first accepted (Eskerholm date), "
                "each item at the rate in force that day; less repayments (6171) in the quarter accepted; plus removals "
                "to premises no longer approved on the day (CE14, sections 2 to 4)."])
    ws3 = wb.create_sheet("Notes")
    notes = [
        ["Notes"],
        ["Records to 30 September 2026: the Statistics Office's release and back series as at 19 October 2026, Customs' "
         "declarations extract to 30 September 2026, the register as at 29 September 2026."],
        ["Clearances and shelf prices: Eskerholm Statistics Office, %s to 2026 Q3, at constant 2026 prices; 2008 to "
         "2011 from the back-series workbook." % ("%d Q%d" % tuple(F["first_quarter"]))],
        ["Demand: for each duty, log clearances on quarter dummies, log shelf price and the previous quarter's log "
         "clearances (%d quarters). The response by each quarter of 2027 builds from the first quarter's response at "
         "the fitted rate of adjustment." % (F["quarters"] - 1)],
        ["Cut: the cut in each duty that gives up GBP %.1f million of duty and GST in 2027, at the clearances buyers "
         "reach in each quarter after the cut, GST at %d per cent on the duty-inclusive price." % (F["envelope_m"],
                                                                                                F["gst_pct"])],
        ["Excess burden removed: the area between the fitted demand curve and the producer price over the extra litres "
         "bought in each quarter of 2027."],
    ]
    for n in notes:
        ws3.append(n)
    ws3["A1"].font = Font(bold=True)
    ws3.column_dimensions["A"].width = 120
    for wsx in (ws, ws2):
        for c in wsx[1]:
            c.font = Font(bold=True)
            c.fill = head
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=thin)
    ws.column_dimensions["A"].width = 12
    for k in range(2, 17):
        ws.column_dimensions[chr(64 + k)].width = 12
    ws2.column_dimensions["A"].width = 12
    for col in "BCDE":
        ws2.column_dimensions[col].width = 16
    ws.freeze_panes = "B2"
    ws2.freeze_panes = "B2"
    ws.print_title_rows = "1:1"
    ws2.print_title_rows = "1:1"
    wb.save(path)
    postprocess.scrub(path, P.ASSEMBLY, "2026-10-26")
    postprocess.finish_office(path, "2026-10-20T10:15:00Z", "2026-10-26T15:50:00Z", P.ASSEMBLY, person=AUTHOR)


def write(golden_dir, F):
    os.makedirs(golden_dir, exist_ok=True)
    F = dict(F)
    F["png"] = chart_png(F)
    docx(os.path.join(golden_dir, DOCX), F)
    xlsx(os.path.join(golden_dir, XLSX), F)
