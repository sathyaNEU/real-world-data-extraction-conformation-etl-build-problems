"""The two deliverables: bypass_flow_record_2026.xlsx (the daily record, with the measurement check behind it) and
minimum_flow_deviation_report_2026.docx (the licensee's report to the Commission). Every figure comes from golden.py."""
import datetime as dt

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import golden as G
import world as W


def write_record(path, d, g, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Daily record"
    ws.append(["%s, gauge BP-1: 2026 daily mean flow in the bypassed reach" % W.PROJECT])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Local calendar days (Pacific Daylight Time). Flows on Rating 7 to the 27 July storm's peak (%s PDT) and "
               "on Rating 7 with a stage shift of %s ft after it (about %s ft, the mean of the four post-storm "
               "measurements' shifts); above 4.00 ft, Rating 7's high-water segment."
               % (fig["storm_peak_local"].split(" ")[-1], fig["post_storm_shift_fitted_ft"], fig["post_storm_shift_ft"])])
    ws.append([])
    head = ["Date", "Article 403 minimum (cfs)", "Daily mean flow (cfs)", "Met minimum", "Shortfall (acre-feet)"]
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    red = PatternFill("solid", fgColor="F4D6D2")
    for k, v in g["daily"].items():
        if k.month < 7:
            continue
        mn = d["minimum"](k)
        met = v >= mn
        short = (mn - v) * G.AF_PER_CFS_DAY if not met else None
        ws.append([k, int(mn), G.r0(v), "Yes" if met else "No", round(short, 1) if short is not None else None])
        row = ws.max_row
        ws.cell(row, 1).number_format = "yyyy-mm-dd"
        ws.cell(row, 5).number_format = "0.0"
        if not met:
            for col in range(1, 6):
                ws.cell(row, col).fill = red
    last = ws.max_row
    ws.append([])
    ws.append(["Season total shortfall (acre-feet, nearest 100)", None, None, None,
               int(fig["shortfall_af"].replace(",", ""))])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    for col, wd in zip("ABCDE", (12, 14, 14, 10, 14)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = "A4:E%d" % last
    m = wb.create_sheet("Measurements")
    m.append(["2026 discharge measurements at BP-1 against Rating 7"])
    m["A1"].font = Font(bold=True)
    m.append([])
    m.append(["Date", "Mean gage height (ft)", "Measured (cfs)", "Rating 7 (cfs)", "Difference (%)", "Stage shift (ft)"])
    for c in m[3]:
        c.font = Font(bold=True)
    for v in sorted(g["shifts"], key=lambda v: v["mid"]):
        m.append([v["date"], v["gh"], v["q"], round(v["rated"], 1), round(v["pct"], 1), round(v["shift"], 4)])
        m.cell(m.max_row, 1).number_format = "yyyy-mm-dd"
        for col in (4, 5):
            m.cell(m.max_row, col).number_format = "0.0"
        m.cell(m.max_row, 6).number_format = "0.0000"
    m.append([])
    m.append(["Mean stage shift of the four measurements after the 27 July storm (ft)", None, None, None, None,
              float(fig["post_storm_shift_fitted_ft"])])
    m.cell(m.max_row, 6).number_format = "0.0000"
    for col, wd in zip("ABCDEF", (12, 12, 12, 12, 12, 12)):
        m.column_dimensions[col].width = wd
    vol = wb.create_sheet("Article 404")
    vol.append(["Month", "Bypass volume (acre-feet, nearest 100)"])
    for c in vol[1]:
        c.font = Font(bold=True)
    vol.append(["May 2026", int(fig["may_af"].replace(",", ""))])
    vol.append(["June 2026", int(fig["june_af"].replace(",", ""))])
    vol.append(["May and June", int(fig["may_june_af"].replace(",", ""))])
    vol.append([])
    vol.append(["Peak flow (cfs)", int(fig["spring_peak_cfs"].replace(",", ""))])
    vol.append(["Peak time (PDT)", fig["spring_peak_local"]])
    vol.column_dimensions["A"].width = 16
    vol.column_dimensions["B"].width = 22
    wb.save(path)


def _p(doc, text, bold=False, size=10.5, space=6):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(space)
    return p


def write_report(path, d, g, fig):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    _p(doc, W.COMPANY, bold=True, size=13, space=0)
    _p(doc, "%s" % W.PROJECT, size=10, space=12)
    _p(doc, "November 4, 2026", space=12)
    _p(doc, "To the Commission", space=0)
    _p(doc, "Re: Article 403 minimum-flow deviations in 2026, and Article 404 spring volumes", bold=True, space=12)
    per = fig["deviation_periods_text"]
    _p(doc, "The bypassed reach of Tallis Creek fell below its Article 403 minimum flow from %s 2026 and from %s 2026, "
            "%d days in all, with a total shortfall of %s acre-feet below the minimum." % (per[0], per[1],
                                                                                         fig["deviation_days"],
                                                                                         fig["shortfall_af"]))
    _p(doc, "Cause. The 27 July thunderstorm sent the reach over 6.5 feet at gauge BP-1 and shifted the gauge's "
            "stage-discharge control, the riffle below the orifice. From then on the gauge read the same stage at a lower "
            "flow, so Rating 7 overstated the flow. The plant's gate controller holds the bypass at the flow BP-1 reads on Rating 7, 54 cfs in July "
            "through September and 33 cfs in October, and it held that reading throughout. The four discharge "
            "measurements made after the storm were %s to %s per cent below Rating 7 at the gauge heights the controller "
            "held, against %s per cent below to %s per cent above before it; on the relation they establish (Rating 7 "
            "with a stage shift of %s feet, about %s foot, from the storm's peak), the reach carried about %s cfs "
            "through August and %s cfs in October."
         % (fig["post_storm_pct_range"][1].lstrip("-"), fig["post_storm_pct_range"][0].lstrip("-"),
            fig["pre_storm_pct_extremes"][0], fig["pre_storm_pct_extremes"][1], fig["post_storm_shift_fitted_ft"],
            fig["post_storm_shift_ft"], fig["held_aug_cfs"],
            fig["held_oct_cfs"]))
    _p(doc, "Corrective action. The gate controller will run on the shifted rating from November 5, and Corvid "
            "Hydrometric Services will develop Rating 8 from the 2026 measurements before the 2027 season.")
    _p(doc, "Article 404. The bypassed reach passed %s acre-feet in May and %s acre-feet in June 2026, %s acre-feet in "
            "the two months. The period's peak flow was %s cfs at %s (Pacific Daylight Time)."
         % (fig["may_af"], fig["june_af"], fig["may_june_af"], fig["spring_peak_cfs"], fig["spring_peak_local"]))
    t = doc.add_table(rows=1, cols=3)
    t.style = "Light Grid Accent 1"
    for c, txt in zip(t.rows[0].cells, ("Deviation period", "Days", "Minimum (cfs)")):
        c.text = txt
    for a, b in g["periods"]:
        days = [k for k in g["dev"] if a <= k <= b]
        mins = sorted({int(d["minimum"](k)) for k in days}, reverse=True)
        row = t.add_row().cells
        row[0].text = "%s to %s" % (a.strftime("%-d %b"), b.strftime("%-d %b"))
        row[1].text = str(len(days))
        row[2].text = " then ".join(str(m) for m in mins)
    _p(doc, "", space=6)
    _p(doc, "The daily record is in bypass_flow_record_2026.xlsx.", size=9.5)
    _p(doc, "Marissa Harmon", space=0)
    _p(doc, "Environmental Manager, %s" % W.COMPANY, space=0)
    doc.core_properties.author = W.MANAGER
    doc.core_properties.title = "2026 Article 403 deviation report"
    doc.save(path)
