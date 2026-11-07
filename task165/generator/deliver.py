"""task165 architecture 2: the goldens (the evaluation workbook and the board deck), figures.json and submission.md,
every figure carried from golden.py's reading of the shipped pack."""
import datetime as dt
import io
import json
import os
import zipfile

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.util import Emu, Inches, Pt

import golden as G
import ooxml

F_XLSX = "clay_street_storage_evaluation.xlsx"
F_PPTX = "clay_street_tank_selection_board.pptx"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
GAUGES = ["RG-1", "RG-2", "RG-3", "RG-4"]
YEARS = [2021, 2022, 2023, 2024, 2025]
COST = {"A": 78.6, "B": 96.0, "C": 128.5, "D": 158.9}
STAMP = dt.datetime(2026, 1, 22, 16, 40)
ZIP_TIME = (2026, 1, 22, 16, 40, 0)


def r1(x):
    return round(x + 1e-9, 1)


def r2(x):
    return round(x + 1e-9, 2)


def r0(x):
    return int(round(x + 1e-9))


def normalize_zip(path):
    """Rewrite an OOXML package with every member at one fixed time, so two builds are byte-identical."""
    src = zipfile.ZipFile(path)
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            zi = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    open(path, "wb").write(buf.getvalue())


def by_year(target, room=True):
    """Each alternative's events in each year of the record (the event's start year, Eastern time)."""
    o = G.read_meter(target)
    ss = G.read_plant(target)
    import numpy as np
    rm = np.repeat(G.CAP - ss, 4) if room else None
    out = {}
    for lab, v, p in G.ALTS:
        s = G.replay(o, v, p, rm)
        on = np.flatnonzero(s > 1e-9)
        starts = [on[0]] + [on[c + 1] for c in np.flatnonzero(np.diff(on) > 96)] if len(on) else []
        ys = {}
        for i in starts:
            y = (G.T0 + dt.timedelta(minutes=15 * int(i))).astimezone(G.NY).year
            ys[y] = ys.get(y, 0) + 1
        out[lab] = ys
    return out


def figures(target):
    res = G.solve(target)
    ev = res["events"]
    lad = res["ladder"]
    f = {"pick": res["pick"], "limit": 4}
    for lab, v, p in G.ALTS:
        f["events_%s" % lab] = r1(ev[lab])
        f["rated_%s" % lab] = r1(lad["r1"][lab])
        f["vol_%s" % lab] = int(v)
        f["pump_%s" % lab] = int(p)
        f["cost_%s" % lab] = COST[lab]
    f["cost_step_CD"] = round(COST["D"] - COST["C"], 1)
    f["plant_cap"] = 140
    f["record_years"] = 12
    for g in GAUGES:
        for m in range(12):
            f["rain_%s_%02d" % (g, m + 1)] = r2(res["ask1"][g][m])
    for y in YEARS:
        f["nt_%d" % y] = r0(res["ask2"][y])
    f["transducer_offset_ft"] = 0.45
    f["rg4_tip_in"] = 0.0079
    f["rg4_tip_mm"] = 0.2
    f["cfs_to_mgd"] = G.CFS
    return f, res


# ----------------------------------------------------------------------------------------------- workbook
THIN = Side(style="thin", color="999999")
HEAD = Font(bold=True, color="FFFFFF")
FILL = PatternFill("solid", fgColor="1F4E79")


def _head(ws, row, values):
    for j, v in enumerate(values, 1):
        c = ws.cell(row, j, v)
        c.font = HEAD
        c.fill = FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def write_xlsx(path, f, yearly):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Selection"
    ws["A1"] = "Outfall 014 (Clay Street) storage: alternative to carry into design"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Carry Alternative C (38 MG) into design. Untreated overflow events in an average year, 2014 to "
                "2025 metered record, Appendix C criterion no more than 4.")
    _head(ws, 4, ["Alternative", "Storage (MG)", "Dewatering firm capacity (MGD)", "Capital cost (USD M, 2025)",
                  "Events a year, dewatering held to Southside room", "Meets Appendix C",
                  "Events a year at pump rating (for reference)"])
    for k, (lab, v, p) in enumerate(G.ALTS):
        r = 5 + k
        vals = [lab, f["vol_%s" % lab], f["pump_%s" % lab], f["cost_%s" % lab], f["events_%s" % lab],
                "Yes" if f["events_%s" % lab] <= 4 else "No", f["rated_%s" % lab]]
        for j, x in enumerate(vals, 1):
            c = ws.cell(r, j, x)
            c.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
            if j in (4,):
                c.number_format = "0.0"
            if j in (5, 7):
                c.number_format = "0.0"
        if lab == f["pick"]:
            for j in range(1, 8):
                ws.cell(r, j).font = Font(bold=True)
    ws["A10"] = "Basis"
    ws["A10"].font = Font(bold=True)
    notes = ["Overflow record: OF-014 meter, FM-0142 (cfs, EST) to 9 Jun 2019 and AV-3315 (MGD, UTC) from 2 Jun 2019, "
             "all readings on UTC; overlap week dry.",
             "Each tank fills from the overflow and is pumped back once the overflow stops (TM-7 3.2).",
             "Pump-back limited each hour to the lesser of the station's firm capacity and the Southside WRP's "
             "room at SI-1: 140 MGD headworks capacity less the historian's hourly influent (local time to UTC).",
             "Events: discharges less than 24 hours apart counted once (Appendix C 2.2); average year = 2014 to 2025 "
             "events / 12.",
             "Southside holds its 140 MGD limit for one to four days after most March to June storms, so the "
             "pump stations' ratings overstate how fast a Clay Street tank empties."]
    for k, t in enumerate(notes):
        ws.cell(11 + k, 1, t)
    for col, w in zip("ABCDEFG", (14, 12, 16, 14, 22, 12, 20)):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 46

    wy = wb.create_sheet("Events by year")
    _head(wy, 1, ["Year"] + ["Alt %s (%d MG)" % (lab, int(v)) for lab, v, _ in G.ALTS])
    for k, y in enumerate(range(2014, 2026)):
        wy.cell(2 + k, 1, y)
        for j, (lab, _, _) in enumerate(G.ALTS):
            wy.cell(2 + k, 2 + j, yearly[lab].get(y, 0))
    wy.cell(14, 1, "Total")
    wy.cell(15, 1, "Per year")
    for j, (lab, _, _) in enumerate(G.ALTS):
        col = openpyxl.utils.get_column_letter(2 + j)
        wy.cell(14, 2 + j, "=SUM(%s2:%s13)" % (col, col))
        wy.cell(15, 2 + j, "=ROUND(%s14/12,1)" % col)
        wy.cell(14, 2 + j).font = Font(bold=True)
    wy.column_dimensions["A"].width = 10
    for col in "BCDE":
        wy.column_dimensions[col].width = 15

    wr = wb.create_sheet("Rainfall 2025")
    wr["A1"] = "Rainfall recorded at the Authority's rain gauges, 2025, inches (calendar months, Eastern time)"
    wr["A1"].font = Font(bold=True)
    _head(wr, 3, ["Gauge"] + MONTHS + ["Year"])
    for k, g in enumerate(GAUGES):
        wr.cell(4 + k, 1, g)
        for m in range(12):
            c = wr.cell(4 + k, 2 + m, f["rain_%s_%02d" % (g, m + 1)])
            c.number_format = "0.00"
        c = wr.cell(4 + k, 14, "=SUM(B%d:M%d)" % (4 + k, 4 + k))
        c.number_format = "0.00"
    wr["A9"] = ("Calibration pours removed (steady tip runs on cal-check visits); re-sent duplicate tips dropped; "
                "RG-3 and RG-4 TipLink loggers read as UTC from May 2024; every gauge's tips at 0.2 mm (0.0079 in) "
                "from the July 2025 contract visit that fitted its new mechanism (field log), the inventory's 0.01 in "
                "before it.")
    wr.column_dimensions["A"].width = 10

    wn = wb.create_sheet("Northside returns")
    wn["A1"] = "Northside tank: volume returned to the Northside Interceptor, million gallons"
    wn["A1"].font = Font(bold=True)
    _head(wn, 3, ["Year", "Returned (MG)"])
    for k, y in enumerate(YEARS):
        wn.cell(4 + k, 1, y)
        wn.cell(4 + k, 2, f["nt_%d" % y])
    wn["A10"] = ("Mass balance on each 15-minute interval a pump ran: fall in storage (LIT-601 through O&M Table "
                 "4-1) plus FIT-600 inflow over the interval. LIT-601 readings after the 23 Aug 2023 re-mount read "
                 "0.45 ft high (empty tank) and are corrected. FIT-600 carries SG-600's leak-by while its seals were "
                 "failing (2022 to 2025 work orders), pumped back with the stored flow. P-2 has delivered less than "
                 "its nameplate since its March 2023 rebuild, so run states times the station curve overstate.")
    wn.column_dimensions["A"].width = 10
    wn.column_dimensions["B"].width = 16
    wb.properties.creator = "QSA Engineering and Planning"
    wb.properties.lastModifiedBy = "QSA Engineering and Planning"
    wb.properties.created = STAMP
    wb.properties.modified = STAMP
    wb.save(path)
    ooxml.normalize(path, STAMP, STAMP)


# ----------------------------------------------------------------------------------------------- deck
def _text(slide, x, y, w, h, text, size=16, bold=False, color="1F1F1F"):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for k, line in enumerate(text if isinstance(text, list) else [text]):
        p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor.from_string(color)
    return tb


def write_pptx(path, f):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    s = prs.slides.add_slide(blank)
    _text(s, 0.7, 2.3, 12, 1.2, "Outfall 014 Clay Street storage: alternative for the design task order", 32, True,
          "1F4E79")
    _text(s, 0.7, 3.6, 12, 1.0, "Board of Directors, February 2026. Engineering and Planning.", 18)

    s = prs.slides.add_slide(blank)
    _text(s, 0.6, 0.4, 12.2, 0.9, "Recommendation: carry Alternative C (38 MG) into design", 28, True, "1F4E79")
    _text(s, 0.6, 1.25, 12.2, 0.8,
          "Alternative C leaves %.1f untreated overflow events in an average year against the decree's limit of 4. "
          "Alternative B (26 MG) leaves %.1f." % (f["events_C"], f["events_B"]), 16)
    cd = CategoryChartData()
    cd.categories = ["A (19 MG)", "B (26 MG)", "C (38 MG)", "D (50 MG)"]
    cd.add_series("Events a year", [f["events_%s" % lab] for lab, _, _ in G.ALTS])
    x, y, cx, cy = Inches(0.8), Inches(2.1), Inches(8.6), Inches(5.0)
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, cd).chart
    ch.has_legend = False
    ch.has_title = True
    ch.chart_title.text_frame.text = "Untreated overflow events a year at Outfall 014, 2014 to 2025 record"
    ch.chart_title.text_frame.paragraphs[0].font.size = Pt(13)
    va = ch.value_axis
    va.maximum_scale, va.minimum_scale, va.major_unit = 12.0, 0.0, 2.0
    va.has_major_gridlines = True
    va.tick_labels.font.size = Pt(11)
    ch.category_axis.tick_labels.font.size = Pt(12)
    pl = ch.plots[0]
    pl.has_data_labels = True
    pl.data_labels.number_format = "0.0"
    pl.data_labels.number_format_is_linked = False
    pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    pl.data_labels.font.size = Pt(12)
    ser = pl.series[0]
    for k, (lab, _, _) in enumerate(G.ALTS):
        pt = ser.points[k]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = RGBColor.from_string("1F4E79" if lab == f["pick"] else "9DB3C8")
    # the decree's limit, drawn across the plot at 4 events a year (the plot area estimated from the chart frame)
    top, bottom = y + Emu(int(cy * 0.16)), y + Emu(int(cy * 0.91))
    yl = bottom - Emu(int((bottom - top) * 4.0 / 12.0))
    ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x + Emu(int(cx * 0.08)), yl, x + cx - Emu(int(cx * 0.03)), yl)
    ln.line.color.rgb = RGBColor.from_string("C00000")
    ln.line.width = Pt(2)
    _text(s, 7.6, yl / 914400 - 0.42, 1.8, 0.4, "Limit: 4", 12, True, "C00000")
    _text(s, 9.7, 2.3, 3.3, 4.6,
          ["Each tank is replayed through the 2014 to 2025 Outfall 014 record.",
           "Pump-back to SI-1 is limited to the room the Southside WRP has under its 140 MGD headworks capacity, "
           "hour by hour from the plant historian.",
           "At their stations' ratings alone the tanks would leave A %.1f, B %.1f, C %.1f, D %.1f; Southside's "
           "days at capacity after spring storms keep the tanks full into the next storm." %
           (f["rated_A"], f["rated_B"], f["rated_C"], f["rated_D"])], 13)

    s = prs.slides.add_slide(blank)
    _text(s, 0.6, 0.4, 12.2, 0.9, "Cost and next steps", 28, True, "1F4E79")
    _text(s, 0.6, 1.4, 12.2, 5.0,
          ["Alternative C: USD %.1f million (TM-7, Class 4, 2025 dollars), the least-cost alternative that meets "
           "Appendix C at Outfall 014." % f["cost_C"],
           "Alternative D adds USD %.1f million for performance the decree does not require." % f["cost_step_CD"],
           "Design task order to Ostrem Calder for Alternative C by 1 March 2026; Facility Plan to EPA and the "
           "Department by 30 June 2026; in service by 31 December 2029.",
           "The pump station and force main to SI-1 are sized in design against the Southside room, not the "
           "rated capacity alone."], 17)
    cp = prs.core_properties
    cp.author = "QSA Engineering and Planning"
    cp.last_modified_by = "QSA Engineering and Planning"
    cp.title = "Outfall 014 Clay Street storage alternative"
    cp.created = STAMP
    cp.modified = STAMP
    cp.revision = 3
    prs.save(path)
    ooxml.normalize(path, STAMP, STAMP)


# ----------------------------------------------------------------------------------------------- submission
def submission(f):
    ev = lambda lab: "%.1f" % f["events_%s" % lab]  # noqa: E731
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences (hydrology, flood frequency).  ")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Carry Alternative C, the 38 MG tank, into design.**")
    L.append("It leaves Outfall 014 %s untreated overflow events in an average year against the decree's limit of 4. "
             "Not Alternative B (26 MG), which meets the limit only at its pump station's 31 MGD rating (%s) and "
             "leaves %s once its pump-back is held to the room the Southside plant has under its 140 MGD headworks "
             "capacity. Not Alternative D, which meets the limit too but costs USD %.1f million more.\n" %
             (ev("C"), "%.1f" % f["rated_B"], ev("B"), f["cost_step_CD"]))
    L.append("## 2. Critical Components\n")
    L.append("1. Alternative B, pumped back no faster than the Southside plant's room: **%s events a year**" % ev("B"))
    L.append("2. Alternative C on the same replay: **%s events a year**\n" % ev("C"))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Joined the two loggers in outfall_014_flow_monitoring_2014-2025.parquet onto UTC, FM-0142's cfs "
             "(Eastern Standard Time) times 0.646317 and AV-3315's MGD, the overlap week once.")
    L.append("2. Took the Southside WRP's hourly influent from wrp_influent_hourly_2014-2025.csv (both tag sets, local "
             "time with its repeated and missing hours, to UTC) and its room as 140 MGD less the influent.")
    L.append("3. Replayed the record through each TM-7 tank filling from the overflow and pumped back after the overflow "
             "stops (TM-7 3.2) at the lesser of the station's firm capacity and that hour's room.")
    L.append("4. Counted untreated overflow events under Appendix C 2.2 and 2.3: A %s, B %s, C %s, D %s a year; C is "
             "the least-cost alternative at or under 4 (TM-7 4)." % (ev("A"), ev("B"), ev("C"), ev("D")))
    L.append("5. Rainfall 2025: dropped repeated tips, removed each calibration pour (a steady run of tips on a "
             "cal-check visit in rain_gauge_field_service_2014-2025.xlsx), read the TipLink C200 loggers (RG-3 and RG-4 "
             "from May 2024) as UTC and the HOBO loggers as Eastern Standard Time, and counted each gauge's tips at 0.2 mm "
             "from the July 2025 visit the field log records its new mechanism on.")
    L.append("6. Northside returns: on each quarter hour a pump ran in northside_tank_scada_2020-2025.csv, the fall "
             "in storage (NT_LIT601_FT through O&M Table 4-1, readings from the 23 August 2023 re-mount less the 0.45 "
             "ft the empty tank reads) plus NT_FIT600_MGD over the quarter hour, summed by year.")
    L.append("7. Recommended Alternative C at %s events a year.\n" % ev("C"))
    L.append("## 4. Deliverable Answers\n")
    L.append("### clay_street_storage_evaluation.xlsx\n")
    L.append("1. Events a year each alternative would leave, to one decimal:")
    for lab, v, _ in G.ALTS:
        L.append("   - Alternative %s (%d MG): %s" % (lab, int(v), ev(lab)))
    L.append("2. Alternative to carry into design: Alternative C (38 MG)")
    L.append("3. Rainfall recorded in 2025, inches:")
    for g in GAUGES:
        L.append("   - %s: %s" % (g, ", ".join("%s %.2f" % (MONTHS[m], f["rain_%s_%02d" % (g, m + 1)]) for m in range(12))))
    L.append("4. Volume the Northside tank returned to the Northside interceptor, million gallons:")
    for y in YEARS:
        L.append("   - %d: %d" % (y, f["nt_%d" % y]))
    L.append("")
    L.append("### clay_street_tank_selection_board.pptx\n")
    L.append("1. Selection: Alternative C (38 MG), on slide 2")
    L.append("2. Column chart of events a year by alternative (A %s, B %s, C %s, D %s) against the limit of 4, on "
             "slide 2, Alternative C highlighted" % (ev("A"), ev("B"), ev("C"), ev("D")))
    return "\n".join(L) + "\n"


def main(target, golden_dir, fig_path, sub_path):
    f, res = figures(target)
    yearly = by_year(target)
    os.makedirs(golden_dir, exist_ok=True)
    write_xlsx(os.path.join(golden_dir, F_XLSX), f, yearly)
    write_pptx(os.path.join(golden_dir, F_PPTX), f)
    json.dump(f, open(fig_path, "w"), indent=1, sort_keys=True)
    open(sub_path, "w").write(submission(f))
    return f


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    main(os.path.join(task, "target"), os.path.join(task, "golden"), os.path.join(here, "figures.json"),
         os.path.join(task, "submission.md"))
