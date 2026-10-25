"""task301 goldens: the selection workbook fenmore_site_selection_2027.xlsx and the committee paper
fenmore_build_paper_2027.docx with its chart, written from figures.json and the solve's working."""
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Cm, Pt, RGBColor
from matplotlib.ticker import FuncFormatter
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import params as P
import postprocess
import solve as SV

XLSX = "fenmore_site_selection_2027.xlsx"
DOCX = "fenmore_build_paper_2027.docx"
HEAD = PatternFill("solid", fgColor="DDE5EA")
PICK = PatternFill("solid", fgColor="E3EEF9")
LINE = Border(top=Side(style="thin", color="8A8A8A"))
ANALYST = "Rosie Taylor"
LEAD = "Valerie Freeman"


def _head(ws, row, cols, height=None):
    for j, h in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    if height:
        ws.row_dimensions[row].height = height


def _widths(ws, w):
    for j, x in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(j)].width = x


def _fmt(ws, rows, cols, f):
    for row in ws.iter_rows(min_row=rows[0], max_row=rows[1], min_col=cols[0], max_col=cols[1]):
        for c in row:
            c.number_format = f


def _date(s):
    d = dt.date.fromisoformat(s)
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def workbook(path, F, X):
    c = X["call"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Selection"
    ws["A1"] = "2027 build: Kingsley Fields, %s MWh expected in 2028" % "{:,}".format(F["call_export_mwh"])
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Export in the first full year of operation (2028), 11.0 MWp on Knowle Park's layout and bifacial "
                "410 W modules, in a year of average weather (the 2016 to 2025 record in the site weather file), on "
                "Knowle Park's measured performance. Development team, %s, November 2026." % P.ORG)
    ws["A2"].font = Font(italic=True, size=9)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 30
    cols = ["Candidate", "Energised", "Irradiation, average year (kWh/m2)", "Age at mid-2028 (years)",
            "2028 export before broiler dust (MWh)", "Broiler dust lost on the planned blocks", "Expected 2028 export (MWh)",
            "Decision"]
    _head(ws, 4, cols, 46)
    order = ["Kingsley Fields", "Larkhill Common", "Hallam Down", "Marston Vale"]
    r = 5
    for k in order:
        if k == "Hallam Down":
            row = [k, _date(F["energised"][k]), F["irradiation_kwh_m2"][k], round(SV.age_2028(k), 2),
                   F["hallam_clean_export_mwh"], F["hallam_loss_pct"] / 100.0,
                   "%s (no fit above %s)" % ("{:,}".format(F["hallam_export_mwh"]),
                                             "{:,}".format(F["hallam_export_range_mwh"][1])), ""]
        else:
            row = [k, _date(F["energised"][k]), F["irradiation_kwh_m2"][k], round(SV.age_2028(k), 2),
                   F["export_mwh"][k], None, F["export_mwh"][k], "Build" if k == F["call_site"] else ""]
        ws.append(row)
        if k == F["call_site"]:
            for x in ws[r]:
                x.fill = PICK
                x.font = Font(bold=True)
        r += 1
    _fmt(ws, (5, 8), (3, 3), "#,##0")
    _fmt(ws, (5, 8), (4, 4), "0.00")
    _fmt(ws, (5, 8), (5, 5), "#,##0")
    _fmt(ws, (5, 8), (6, 6), "0.0%")
    _fmt(ws, (5, 8), (7, 7), "#,##0")
    for row in ws.iter_rows(min_row=5, max_row=8, min_col=7, max_col=7):
        for x in row:
            x.alignment = Alignment(horizontal="right")
    r += 1
    rows = [("Site to build in 2027", F["call_site"], None),
            ("Its 2028 export (MWh, nearest 100)", F["call_export_mwh"], "#,##0"),
            ("Knowle Park's measured performance ratio, 16 January 2024 to 31 December 2025", F["knowle_ratio"], "0.000"),
            ("Fleet bifacial degradation, a year (four bifacial farms)", F["fleet_degradation_pct"] / 100.0, "0.00%"),
            ("Hallam Down's irradiation lead over Kingsley Fields", F["hallam_lead_pct"] / 100.0, "0.0%"),
            ("Hallam Down's broiler-dust loss on the best fit (never under %.1f per cent on any fit)" %
             F["hallam_loss_range_pct"][0], F["hallam_loss_pct"] / 100.0, "0.0%")]
    for a, b, f in rows:
        ws.cell(row=r, column=1, value=a).font = Font(bold=a.startswith(("Site", "Its")))
        x = ws.cell(row=r, column=5, value=b)
        x.font = Font(bold=a.startswith(("Site", "Its")))
        if f:
            x.number_format = f
        r += 1
    _widths(ws, [18, 18, 14, 11, 15, 15, 22, 10])
    ws.freeze_panes = "B5"

    # the broiler dust: Wexcombe's blocks near its sheds and Hallam Down's planned blocks
    ws = wb.create_sheet("Broiler dust")
    ws["A1"] = "Broiler dust on the blocks near a 10-shed unit: Wexcombe's measured blocks and Hallam Down's planned ones"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Wexcombe: each block's daily AC energy per MWp in the inverter SCADA against the median of its blocks "
                "more than %d m from the sheds, outage days in the O&M log left out. Each block within %d m fitted with "
                "a deposit that builds on days under %d mm of rain, is cut by %d to %d mm and nearly cleared by %d mm or "
                "more (the thresholds the blocks fit best); the daily rate falls with distance from the sheds. Hallam "
                "Down: that rate at each planned block's distance from its unit, run through Hallam Down's 2016 to 2025 "
                "rain, weighted by its irradiation."
                % (F["far_ref_m"], F["near_m"], F["wash_mm"][0], F["wash_mm"][0], F["wash_mm"][1], F["wash_mm"][1]))
    ws["A2"].font = Font(italic=True, size=9)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 64
    _head(ws, 4, ["Wexcombe block", "Distance from the sheds (m)", "Output against the far blocks",
                  "Fitted deposit a dry day"], 32)
    near = c["near"]
    per = c["rates"]
    r = 5
    for inv, x in near[near.d < F["near_m"]].sort_values("d").iterrows():
        ws.append([inv, int(round(x.d)), float(x.rel), per[inv][1] if inv in per else None])
        r += 1
    _fmt(ws, (5, r - 1), (3, 3), "0.000")
    _fmt(ws, (5, r - 1), (4, 4), "0.00%")
    r += 1
    _head(ws, r, ["Hallam Down block", "Distance from the sheds (m)", "Deposit a dry day", "Loss, average year"], 32)
    L = SV.block_distances(X["K"], "Hallam Down").sort_values("d")
    f = SV.rate_fn(per, "exp")
    h = X["K"].w[X["K"].w.site == "Hallam Down"].sort_values("date")
    poa, rain = h.poa_irradiation_kwh_m2.values, h.rainfall_mm.values
    lo, hi = F["wash_mm"]
    r0 = r + 1
    for x in L.itertuples():
        dep = SV.run_deposit(rain, f(x.d), lo, hi)
        ws.append([x.inverter, int(round(x.d)), f(x.d), float((poa * dep).sum() / poa.sum())])
    r1 = r0 + len(L) - 1
    _fmt(ws, (r0, r1), (3, 3), "0.00%")
    _fmt(ws, (r0, r1), (4, 4), "0.0%")
    ws.cell(row=r1 + 1, column=1, value="Ten planned blocks").font = Font(bold=True)
    x = ws.cell(row=r1 + 1, column=4, value=F["hallam_loss_pct"] / 100.0)
    x.number_format = "0.0%"
    x.font = Font(bold=True)
    x.border = LINE
    _widths(ws, [18, 16, 16, 16, 12, 12])

    ws = wb.create_sheet("Pyranometers 2025")
    ws["A1"] = "Plane-of-array irradiation measured on site in 2025, as a ratio to the site weather file"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Each day the station recorded: its signal over the sensitivity on the certificate in force that day for "
                "the sensor then in the mast (the sensor that came down until the register's installation date, the "
                "register's sensor from it; the station file keeps the logger's sensor setting, not changed at the "
                "swap), summed, over the weather file's irradiation on the same days.")
    ws["A2"].font = Font(italic=True, size=9)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 44
    _head(ws, 4, ["Farm", "Sensor until the swap", "Sensor from the swap", "Swapped", "Days recorded",
                  "Measured over weather file"], 32)
    for k in P.OPERATING:
        ws.append([k, F["ask_a_down"][k], F["ask_a_up"][k], _date(F["ask_a_swap"][k]), F["ask_a_days"][k],
                   F["ask_a"][k]])
    _fmt(ws, (5, 18), (6, 6), "0.000")
    _widths(ws, [17, 15, 15, 16, 10, 14])
    ws.freeze_panes = "B5"

    ws = wb.create_sheet("Alarm response 2025")
    ws["A1"] = "Hours from an inverter fault alarm to the attending technician's arrival on site, 2025"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Each fault alarm (F code) with a work order: from the SCADA's raised time to the first van tracker "
                "entry at the farm after it by the van the assigned technician had that day, the tracker's UK times "
                "taken to UTC. The CMMS attended stamp is the tablet's sync, after the visit, where the farm has no "
                "signal.")
    ws["A2"].font = Font(italic=True, size=9)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 44
    _head(ws, 4, ["Farm", "Fault alarms attended", "Average hours to arrival"], 32)
    for k in P.OPERATING:
        ws.append([k, F["ask_b_alarms"][k], F["ask_b"][k]])
    _fmt(ws, (5, 18), (3, 3), "0.0")
    _widths(ws, [17, 12, 14])
    ws.freeze_panes = "B5"

    ws = wb.create_sheet("Notes")
    notes = [
        ("Performance", "Knowle Park's export at its fiscal meter over its satellite irradiation in the site weather file "
                        "and its 12.0 MWp, from energisation to 31 December 2025, outage days kept in. Knowle Park is the "
                        "one farm on the raised frame and bifacial 410 W modules the build repeats."),
        ("Age", "Carried to each candidate's age at mid-2028 from its energisation date at the four bifacial farms' "
                "fitted degradation (annual ratios, a level for each farm)."),
        ("Average year", "The ten years 2016 to 2025 of each candidate's irradiation in the site weather file, "
                         "averaged."),
        ("Broiler dust", "The Hallam Down loss is the share of its average-year output the deposit takes, averaged over "
                         "its ten planned blocks. Across the fits the record supports (far blocks or the farm median "
                         "as the reference; partial or full washing at the thresholds that fit best; the rate falling "
                         "with distance exponentially, as a power or by straight lines) it is never under %.1f per "
                         "cent; Kingsley Fields stays first under every one." % F["hallam_loss_range_pct"][0]),
        ("Sources", "Fiscal meters and inverter SCADA 2022 to 2025; site weather file 2016 to 2025; site register; "
                    "array layout; environs listing (2 km); O&M log; met-station files, pyranometer register and "
                    "certificates; SCADA alarm log, CMMS work orders, van tracker and van list, 2025."),
    ]
    _head(ws, 1, ["Item", "Note"])
    for a, b in notes:
        ws.append([a, b])
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for x in row:
            x.alignment = Alignment(wrap_text=True, vertical="top")
    _widths(ws, [16, 110])
    wb.properties.creator = ANALYST
    wb.properties.lastModifiedBy = ANALYST
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2026-11-05")
    postprocess.finish_office(path, "2026-11-03T08:45:00Z", "2026-11-05T17:10:00Z", P.ADVISER, person=ANALYST)


def chart(F):
    BLUE, INK, MUTED, GREY, SURF, BAND = "#2a78d6", "#0b0b0b", "#52514e", "#8c8b86", "#fcfcfb", "#d9d8d3"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    fig, ax = plt.subplots(figsize=(8.6, 3.9), dpi=170)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    rows = ["Kingsley Fields", "Larkhill Common", "Hallam Down", "Marston Vale"]
    y = {k: len(rows) - 1 - i for i, k in enumerate(rows)}
    for k in rows:
        if k == "Hallam Down":
            lo, hi = F["hallam_export_range_mwh"]
            ax.plot([lo, hi], [y[k], y[k]], color=BAND, linewidth=9, solid_capstyle="round", zorder=2)
            ax.annotate("", xy=(F["hallam_export_mwh"] + 30, y[k]), xytext=(F["hallam_clean_export_mwh"] - 30, y[k]),
                        arrowprops=dict(arrowstyle="-|>", color=GREY, linewidth=1.2, shrinkA=4, shrinkB=4), zorder=3)
            ax.scatter([F["hallam_clean_export_mwh"]], [y[k]], s=70, facecolor=SURF, edgecolor=GREY, linewidth=1.6, zorder=4)
            ax.scatter([F["hallam_export_mwh"]], [y[k]], s=70, color=GREY, zorder=4)
            ax.text(F["hallam_clean_export_mwh"], y[k] + 0.30, "%s before broiler dust" %
                    "{:,}".format(F["hallam_clean_export_mwh"]), ha="center", va="bottom", fontsize=8.4, color=MUTED)
            ax.text(lo, y[k] - 0.32, "%s on the best fit, no fit above %s" % ("{:,}".format(F["hallam_export_mwh"]),
                                                                             "{:,}".format(hi)),
                    ha="left", va="top", fontsize=8.4, color=MUTED)
        else:
            v = F["export_mwh"][k]
            col = BLUE if k == F["call_site"] else GREY
            ax.scatter([v], [y[k]], s=70, color=col, zorder=4)
            ax.text(v + 28, y[k], "{:,}".format(v), ha="left", va="center", fontsize=9, color=INK,
                    fontweight="bold" if k == F["call_site"] else "normal")
    ax.set_yticks([y[k] for k in rows])
    ax.set_yticklabels(rows, color=INK)
    ax.set_ylim(-0.7, len(rows) - 0.35)
    ax.set_xlim(9000, 10300)
    ax.set_xticks(range(9000, 10201, 200))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: "{:,}".format(int(v))))
    ax.set_xlabel("Expected export in 2028, MWh", color=MUTED)
    ax.tick_params(colors=MUTED, length=0)
    ax.grid(axis="x", color="#e4e3df", linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#bdbcb6")
    fig.text(0.015, 0.95, "Kingsley Fields exports the most in 2028", ha="left", va="top", fontsize=13,
             fontweight="bold", color=INK)
    fig.text(0.015, 0.875, "Each candidate at 11.0 MWp in a year of average weather (2016 to 2025), on Knowle Park's "
                           "measured performance;\nHallam Down after the broiler dust its planned blocks would carry",
             ha="left", va="top", fontsize=8.8, color=MUTED)
    fig.text(0.015, 0.02, "Source: site weather file 2016 to 2025, fiscal meters and inverter SCADA 2022 to 2025, array "
                          "layout and environs listing. Development team, November 2026.", fontsize=7.4, color=MUTED)
    fig.subplots_adjust(left=0.17, right=0.965, top=0.74, bottom=0.2)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=SURF, metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def paper(path, F):
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for sec in d.sections:
        sec.left_margin = sec.right_margin = Cm(2.2)
    p = d.add_paragraph()
    r = p.add_run("%s: Investment Committee, December 2026" % P.ORG)
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    h = d.add_paragraph()
    r = h.add_run("2027 build: Kingsley Fields, about %s MWh in its first full year" % "{:,}".format(F["call_export_mwh"]))
    r.bold = True
    r.font.size = Pt(15)
    meta = d.add_paragraph()
    meta.add_run("From: %s, Head of Development, with %s, Performance    Date: 5 November 2026" %
                 (LEAD, ANALYST)).font.size = Pt(9)
    d.add_heading("Recommendation", level=2)
    d.add_paragraph(
        "Approve Kingsley Fields as the 2027 build. At 11.0 MWp on the Knowle Park design it will export about %s MWh "
        "in 2028, its first full year, in a year of average weather. It is the most of the four consented sites once "
        "Hallam Down is priced for the broiler dust its planned blocks would carry." % "{:,}".format(F["call_export_mwh"]))
    d.add_heading("Why not Hallam Down", level=2)
    d.add_paragraph(
        "Hallam Down has the best sun of the four, %.1f per cent more irradiation in an average year than Kingsley "
        "Fields, and on Knowle Park's performance alone it would export about %s MWh. But its ten planned blocks sit "
        "%d to %d m from a 10-shed broiler unit, and broiler litter dust settles on modules on dry days until rain "
        "washes it off. Our fiscal meters do not show this: Wexcombe, the one farm beside a unit of that size, meters "
        "%.1f per cent above its 2012 to 2014 peers, because its meter sums 58 blocks and only the few nearest the sheds "
        "are touched. Its inverter records do show it. Against Wexcombe's blocks more than %d m from the sheds, its three "
        "nearest blocks, %d to %d m away, produce %.1f to %.1f per cent less, falling through dry spells and recovering "
        "after %d mm of rain or more." % (F["hallam_lead_pct"], "{:,}".format(F["hallam_clean_export_mwh"]),
                                          F["hallam_block_range_m"][0], F["hallam_block_range_m"][1],
                                          F["wexcombe_meter_vs_peers_pct"], F["far_ref_m"], F["corner_range_m"][0],
                                          F["corner_range_m"][1], F["corner_loss_range_pct"][0],
                                          F["corner_loss_range_pct"][1], F["wash_mm"][1]))
    d.add_paragraph(
        "We fitted that deposit to each Wexcombe block within %d m, its daily rate falling with distance from the sheds, "
        "and ran it at each of Hallam Down's planned blocks through Hallam Down's own rain, about %s mm a year against "
        "Wexcombe's %s. Hallam Down would lose %.1f per cent of its output on the best fit, and no less than %.1f per "
        "cent on any fit the Wexcombe record supports: more than its lead in every case. Its 2028 export falls to about "
        "%s MWh, and to no more than %s MWh on any fit."
        % (F["near_m"], "{:,}".format(F["hallam_rain_mm"]), "{:,}".format(F["wexcombe_rain_mm"]), F["hallam_loss_pct"],
           F["hallam_loss_range_pct"][0], "{:,}".format(F["hallam_export_mwh"]),
           "{:,}".format(F["hallam_export_range_mwh"][1])))
    d.add_heading("The four candidates", level=2)
    t = d.add_table(rows=1, cols=4)
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hd in enumerate(["Site", "Energised", "Irradiation, average year (kWh/m2)", "Expected 2028 export (MWh)"]):
        t.rows[0].cells[i].text = hd
    for k in ["Kingsley Fields", "Larkhill Common", "Hallam Down", "Marston Vale"]:
        row = t.add_row().cells
        row[0].text, row[1].text = k, _date(F["energised"][k])
        row[2].text = "{:,}".format(F["irradiation_kwh_m2"][k])
        row[3].text = ("{:,}".format(F["export_mwh"][k]) if k != "Hallam Down" else
                       "%s (no fit above %s)" % ("{:,}".format(F["hallam_export_mwh"]),
                                                 "{:,}".format(F["hallam_export_range_mwh"][1])))
    src = d.add_paragraph()
    r = src.add_run("Exports at the fiscal meter. Each site is energised between July and October 2027, so 2028 is the "
                    "first full calendar year for all four. Source: site weather file 2016 to 2025; Knowle Park's meter.")
    r.font.size = Pt(8)
    d.add_picture(io.BytesIO(chart(F)), width=Cm(16.2))
    d.add_heading("Basis", level=2)
    d.add_paragraph(
        "Each candidate's irradiation is the ten-year average of the site weather file. Performance is Knowle Park's, "
        "the one farm on the raised frame and bifacial modules the build repeats: a performance ratio of %.2f from its "
        "fiscal meter, January 2024 to December 2025, outages included, carried to each site's age in 2028 at the "
        "bifacial farms' measured degradation." % F["knowle_ratio_2dp"])
    d.add_heading("Fleet measures in the workbook", level=2)
    d.add_paragraph(
        "The workbook also gives each operating farm's 2025 irradiation measured by its met-station pyranometer as a "
        "ratio to the weather file, and the average hours in 2025 from an inverter fault alarm to the attending "
        "technician's arrival on site.")
    d.add_heading("Risks", level=2)
    d.add_paragraph(
        "Kingsley Fields' figure rests on two years of Knowle Park's record; a weaker or sunnier year moves all four "
        "candidates alike and leaves the order unchanged. Should the Hallam Down unit close, the site would be worth "
        "revisiting for a later build.")
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    for sec in d.sections:
        fp = sec.footer.paragraphs[0]
        run = fp.add_run("%s, Investment Committee, December 2026    Page " % P.ORG)
        run.font.size = Pt(8)
        fld = OxmlElement("w:fldSimple")
        fld.set(qn("w:instr"), "PAGE")
        r_ = OxmlElement("w:r")
        t_ = OxmlElement("w:t")
        t_.text = "1"
        r_.append(t_)
        fld.append(r_)
        fp._p.append(fld)
    d.core_properties.author = ANALYST
    d.core_properties.title = "2027 build"
    d.save(path)
    postprocess.scrub(path, P.ORG, "2026-11-05")
    postprocess.finish_office(path, "2026-11-04T09:30:00Z", "2026-11-05T17:25:00Z", P.ADVISER, person=ANALYST,
                              revision=4)


def write(folder, F, X):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, XLSX), F, X)
    paper(os.path.join(folder, DOCX), F)
