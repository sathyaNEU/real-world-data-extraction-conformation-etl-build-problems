"""The two goldens: the appraisal workbook and the case paper, written from figures.json."""
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Cm
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import params as P
import postprocess

XLSX = "marrable_site_appraisal_2027.xlsx"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#d9d8d4", "#ffffff"
GUESTS, RESIDENTS = "#2a78d6", "#a9a8a2"
DOCX = "new_store_case_2027.docx"
HEAD = PatternFill("solid", fgColor="DCE6DF")
PICK = PatternFill("solid", fgColor="FFF2CC")


def _sheet(ws, header, rows, widths, fmts=None, title=None, note=None):
    r0 = 1
    if title:
        ws.cell(row=1, column=1, value=title).font = Font(bold=True, size=12)
        r0 = 3
    for j, h in enumerate(header, 1):
        c = ws.cell(row=r0, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(vertical="top", wrap_text=True)
    for i, row in enumerate(rows, r0 + 1):
        for j, v in enumerate(row, 1):
            ws.cell(row=i, column=j, value=v)
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    for col, f in (fmts or {}).items():
        j = header.index(col) + 1
        for i in range(r0 + 1, r0 + 1 + len(rows)):
            ws.cell(row=i, column=j).number_format = f
    ws.freeze_panes = ws.cell(row=r0 + 1, column=1)
    if note:
        ws.cell(row=r0 + len(rows) + 2, column=1, value=note).font = Font(italic=True, size=9, color="555555")
    return r0


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Appraisal"
    s = fig["sites"]
    order = sorted(s, key=lambda k: -s[k]["add_exact"])
    rows = [[k, s[k]["name"], s[k]["area"], s[k]["sales_exact"], s[k]["took"], s[k]["cost"], s[k]["add_exact"],
             s[k]["resident_add_exact"], s[k]["add"]] for k in order]
    r0 = _sheet(ws, ["Site", "Location", "Floor area (m2)", "Sales a year (GBP)", "Taken from our stores (GBP)",
                     "Running costs (GBP)", "Addition to contribution (GBP)", "Addition, residents only (GBP)",
                     "Addition (GBP m)"], rows, [7, 26, 13, 17, 19, 17, 20, 20, 13],
                {"Sales a year (GBP)": "#,##0", "Taken from our stores (GBP)": "#,##0", "Running costs (GBP)": "#,##0",
                 "Addition to contribution (GBP)": "#,##0", "Addition, residents only (GBP)": "#,##0",
                 "Addition (GBP m)": "0.0"},
                title="Open S3 Wrentoft, Mill Lane: it adds GBP %.1f million a year, ahead of S1 Bellingtoft at GBP %.1f "
                      "million" % (fig["add"], s["S1"]["add"]),
                note="Addition = %d%% of the store's sales, less %d%% of the sales it takes from our ten stores, less its "
                     "running costs (Finance's appraisal rule, spend-share model sheet). Sales include the guests of the "
                     "region's holiday parks at GBP %s a pitch a season; the residents-only column leaves them out."
                     % (fig["margin_pct"], fig["margin_pct"], "{:,}".format(fig["V"])))
    for j in range(1, 10):
        ws.cell(row=r0 + 1, column=j).fill = PICK
    ws2 = wb.create_sheet("Holiday parks")
    rows = [[p["desc"].title().replace(" And ", " and "), p["postcode"], p["pitches"]] for p in fig["parks"]]
    rows.append(["Total", "", sum(p["pitches"] for p in fig["parks"])])
    _sheet(ws2, ["Rating-list description", "Postcode", "Pitches"], rows, [36, 12, 10], {"Pitches": "#,##0"},
           title="%s pitch-measured sites on the 2026 rating list; Wrentoft Lakes is the largest" % (
               ["No", "One", "Two", "Three", "Four", "Five", "Six"][len(fig["parks"])]),
           note="Guests' in-store spend: GBP %s a pitch for a season, from the out-of-region card spend at our stores "
                "(March to October, above each store's November to February level, grossed up by its card share)."
                % "{:,}".format(fig["V"]))
    ws3 = wb.create_sheet("Guest spend by store")
    rows = [[k, v] for k, v in fig["guests_by_store"].items()]
    _sheet(ws3, ["Store", "Guests' spend FY2025/26 (GBP)"], rows, [8, 26], {"Guests' spend FY2025/26 (GBP)": "#,##0"},
           title="Guests' spend at our stores, FY2025/26", note="The smallest values are at the stores no park reaches.")
    ws4 = wb.create_sheet("DC cases")
    rows = [[k, v] for k, v in fig["ask_a"].items()]
    _sheet(ws4, ["Store", "Cases a week"], rows, [8, 14], {"Cases a week": "#,##0"},
           title="Cases a week delivered from Loderwell Gate, 6 October 2025 to 29 March 2026 (25 weeks)",
           note="A load a store turned away (the stop closed within minutes and the same cases went back the next day on "
                "a trip of their own) is counted once, on the day the store took it in.")
    ws5 = wb.create_sheet("Paid hours")
    rows = [[k, v] for k, v in fig["ask_b"].items()]
    _sheet(ws5, ["Store", "Paid hours a week"], rows, [8, 18], {"Paid hours a week": "#,##0"},
           title="Paid hours a week worked at each store, 6 October 2025 to 29 March 2026 (25 weeks)",
           note="Each shift once, at the hours it was paid (the workforce report lists a night shift against the date "
                "it starts and again against the morning it ends) and at the store whose terminal the colleague clocked "
                "in at, so relief cover, shifts at a neighbouring store and colleagues who have since moved are counted "
                "where they worked.")
    ws6 = wb.create_sheet("Buses")
    rows = [[k, fig["sites"][k]["name"], v] for k, v in fig["ask_c"].items()]
    _sheet(ws6, ["Site", "Location", "Departures"], rows, [7, 26, 12],
           title="Bus departures within %d m of each site, %s %d January 2027" % (fig["radius_m"], fig["bus_weekday"],
                                                                               fig["bus_day"]),
           note="By the clock: the day's journeys up to midnight and Thursday's late journeys after it. Each bus once, "
                "by its running board: routes 4 and 41 are in both operators' data, and Sallowmere Motor Services' "
                "Friday-late timetable repeats the evening's weekday journeys, so each of those counts once; the school-day "
                "duplicates on routes 4 and 41 are second buses and count.")
    ws7 = wb.create_sheet("Notes")
    notes = [["As at", "9 October 2026"], ["Model", "Spend-share parameters, June 2025: floor area to the power 1.0, "
              "exp(-0.22 x road km), road km 1.25 x straight line, %d%% of households' grocery spend in store" % fig["instore_pct"]],
             ["Stores in the share", "%d grocery stores of %d m2 or more on the 2026 rating list" % (fig["n_stores_share"], fig["min_area"])],
             ["Running costs", "Site schedule estimates (rent, rates, staffing, other)"],
             ["Rounding", "Additions to the nearest GBP 0.1 million; cases, paid hours and departures whole"]]
    _sheet(ws7, ["Item", "Note"], notes, [20, 100])
    wb.properties.creator = P.PEOPLE["property"]
    wb.properties.lastModifiedBy = P.PEOPLE["property"]
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2026-10-09")
    postprocess.finish_office(path, "2026-10-08T09:10:00Z", "2026-10-09T16:25:00Z", P.ORG, person=P.PEOPLE["property"])


def chart(fig):
    """each site's addition on the residents alone and with the parks' guests, PNG bytes"""
    s = fig["sites"]
    order = sorted(s, key=lambda k: -s[k]["add_exact"])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task305"})
    f, ax = plt.subplots(figsize=(6.3, 2.9), dpi=150)
    f.patch.set_facecolor(SURF)
    x = list(range(len(order)))
    w = 0.36
    res = [s[k]["resident_add_exact"] / 1e6 for k in order]
    gst = [s[k]["add_exact"] / 1e6 for k in order]
    ax.bar([i - w / 2 - 0.01 for i in x], res, w, color=RESIDENTS, label="Residents only", zorder=2)
    ax.bar([i + w / 2 + 0.01 for i in x], gst, w, color=GUESTS, label="With the holiday parks' guests", zorder=2)
    for i, k in enumerate(order):
        if k in (fig["site"], fig["resident_site"]):
            ax.text(i + w / 2 + 0.01, gst[i] + 0.015, "%.1f" % s[k]["add"], ha="center", va="bottom", color=INK, fontsize=8)
            ax.text(i - w / 2 - 0.01, res[i] + 0.015, "%.1f" % s[k]["resident_add"], ha="center", va="bottom", color=INK2,
                    fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(["%s\n%s" % (k, s[k]["name"].split(",")[0]) for k in order], color=INK)
    ax.set_ylabel("GBP million a year", color=INK2)
    ax.set_ylim(0, 1.0)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(INK2)
    ax.tick_params(axis="both", length=0, colors=INK2)
    ax.legend(frameon=False, loc="upper right", fontsize=8)
    ax.set_title("Addition to the chain's contribution by site", loc="left", fontsize=9.5, color=INK, fontweight="bold")
    f.tight_layout()
    buf = io.BytesIO()
    f.savefig(buf, format="png", facecolor=SURF, metadata={"Software": None})
    plt.close(f)
    return buf.getvalue()


def paper(path, fig):
    s = fig["sites"]
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    for sec in d.sections:
        sec.left_margin = sec.right_margin = Cm(2.2)
    p = d.add_paragraph()
    r = p.add_run("Marrable Foodstores: Executive team")
    r.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    h = d.add_paragraph()
    r = h.add_run("Open Wrentoft, Mill Lane in 2027: it adds GBP %.1f million a year" % fig["add"])
    r.bold = True
    r.font.size = Pt(15)
    meta = d.add_paragraph()
    meta.add_run("From: %s, Property and Network Planning    To: %s, chair    Date: 9 October 2026" %
                 (P.PEOPLE["property"], P.PEOPLE["chair"])).font.size = Pt(9)
    d.add_heading("Recommendation", level=2)
    d.add_paragraph(
        "Approve S3, %s, as the one new store for 2027. Once trading it adds GBP %.1f million a year to the chain's "
        "contribution, against GBP %.1f million at S1, %s, the next best site." %
        (fig["site_name"], fig["add"], s["S1"]["add"], s["S1"]["name"]))
    d.add_heading("Why Wrentoft", level=2)
    d.add_paragraph(
        "Our spend-share model shares the grocery spend that starts at each place among the stores that can win it: a "
        "household's at its output area, and anyone else's where they are staying. On the households alone Wrentoft "
        "ranks %s of six at GBP %.1f million. But Wrentoft Lakes Holiday Park, %s pitches on the rating list, is nearer "
        "this site than any other on the shortlist. What its guests spend we see only through our own stores: at "
        "Raddleford, Withybeck and Sallowmere, beside the region's other parks, cardholders from outside the LQ postcode "
        "area spend far more from March to October than in the winter. Those stores take only part of their parks' "
        "spend, though: a larger competitor stands at each park's gate, and the model gives our stores %d, %d and %d per "
        "cent of what starts at Raddleford Water, Withybeck Lakes and Sallowmere Mill. Our stores' season excess, grossed "
        "up for cash, over the pitches weighted by that share is GBP %s of in-store grocery spend a pitch for a season. "
        "Over the pitches alone it would be about GBP %s a pitch, and Wrentoft would stay behind Bellingtoft." % (
            fig["s3_resident_rank"], fig["s3_resident"], "{:,}".format(fig["wrentoft_lakes_pitches"]),
            fig["park_shares_pct"]["Raddleford Water Holiday Park"], fig["park_shares_pct"]["Withybeck Lakes Caravan Park"],
            fig["park_shares_pct"]["Sallowmere Mill Caravan Park"], "{:,}".format(fig["V"]), "{:,}".format(fig["v_direct"])))
    d.add_paragraph(
        "With every park carried as a place where spend starts, a store at Mill Lane sells GBP %.1f million a year and "
        "takes little from our own stores, because none of them is near. That is the whole difference between the "
        "sites: the other five are priced almost unchanged." % fig["s3_sales"])
    d.add_heading("The six sites", level=2)
    order = sorted(s, key=lambda k: -s[k]["add_exact"])
    t = d.add_table(rows=1, cols=4)
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hd in enumerate(["Site", "Location", "Addition (GBP m)", "Residents only (GBP m)"]):
        t.rows[0].cells[i].text = hd
    for k in order:
        row = t.add_row().cells
        row[0].text, row[1].text = k, s[k]["name"]
        row[2].text, row[3].text = "%.1f" % s[k]["add"], "%.1f" % s[k]["resident_add"]
    d.add_picture(io.BytesIO(chart(fig)), width=Cm(15.5))
    src = d.add_paragraph()
    src.add_run("Source: site schedule (October 2026), spend-share model (June 2025), card feed FY2025/26.").font.size = Pt(8)
    d.add_heading("Supporting measures", level=2)
    d.add_paragraph(
        "The appraisal workbook carries the distribution centre's cases a week and the paid hours a week at each of our "
        "stores over the 25 weeks from 6 October 2025, and the bus departures within %d m of each site on %s %d "
        "January 2027." % (fig["radius_m"], fig["bus_weekday"], fig["bus_day"]))
    d.add_heading("Risks", level=2)
    d.add_paragraph(
        "The spend per pitch rests on one year of card data at our own stores; a weaker season at Wrentoft "
        "Lakes, or a park closing, would cut the site's trade. Floor areas are the rating list's measure throughout.")
    d.core_properties.author = P.PEOPLE["property"]
    d.core_properties.title = "New store 2027"
    d.save(path)
    postprocess.scrub(path, P.ORG, "2026-10-09")
    postprocess.finish_office(path, "2026-10-07T08:40:00Z", "2026-10-09T16:30:00Z", P.ORG, person=P.PEOPLE["property"],
                              revision=6)


def write(folder, fig):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, XLSX), fig)
    paper(os.path.join(folder, DOCX), fig)
