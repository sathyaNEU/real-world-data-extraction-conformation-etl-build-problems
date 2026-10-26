"""task308 goldens: the board paper section ebike_deployment_2027.docx (with its chart) and the workbook behind it,
ebike_deployment_2027.xlsx, written from figures.json."""
import os
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from matplotlib.ticker import FuncFormatter
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import params as P
import postprocess

XLSX = "ebike_deployment_2027.xlsx"
DOCX = "ebike_deployment_2027.docx"
NETS = ["Central", "University", "Riverside", "Old Town", "Hillcrest"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]
HEAD = PatternFill("solid", fgColor="DCE4EC")
LINE = Border(top=Side(style="thin", color="8A8A8A"))


def usd(x):
    return "USD {:,}".format(int(x))


def c(x):
    return "{:,}".format(int(x))


def _head(ws, row, cols):
    for j, h in enumerate(cols, 1):
        cell = ws.cell(row=row, column=j, value=h)
        cell.font = Font(bold=True)
        cell.fill = HEAD
        cell.alignment = Alignment(wrap_text=True, vertical="top")


def _widths(ws, w):
    for j, x in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(j)].width = x


def workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Networks"
    best = fig["recommended_network"]
    ws["A1"] = "The 300 e-bikes go to %s: %s a year in net fares at 2025 demand" % (best, usd(fig["net_revenue"][best]))
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Net fare revenue a year: what riders would pay with the e-bikes in the network, less what they paid "
                "there in 2025, at 2025 demand (board paper, item 7). Demand is the rides the stations served plus "
                "the requests they turned away while empty.")
    ws["A2"].font = Font(italic=True, size=9)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:I2")
    ws.row_dimensions[2].height = 30
    cols = ["Network", "Rides 2025 (classic)", "Requests turned away while the station was empty",
            "Demand 2025 (requests)", "Turned away, share of demand", "Classic fare a ride, USD",
            "Net fare revenue a year, USD", "Net fare revenue, nearest USD 25,000", "On the recorded rides only, USD"]
    _head(ws, 4, cols)
    ws.row_dimensions[4].height = 58
    for n in NETS:
        ws.append([n, fig["rides_2025"][n], fig["turned_away_exact"][n], fig["rides_2025"][n] + fig["turned_away_exact"][n],
                   fig["turned_away_share"][n] / 100.0, fig["fare_classic"][n], fig["net_revenue_exact"][n],
                   fig["net_revenue"][n], fig["recorded_route_exact"][n]])
    for r in range(5, 10):
        for col, f in zip("BCDEFGHI", ["#,##0", "#,##0", "#,##0", "0.0%", "0.00", "#,##0", "#,##0", "#,##0"]):
            ws["%s%d" % (col, r)].number_format = f
        if ws["A%d" % r].value == best:
            for col in "ABCDEFGHI":
                ws["%s%d" % (col, r)].font = Font(bold=True)
    ws["A11"] = ("Turned-away requests: each station's classic stock rebuilt second by second from the 03:00 audit, "
                 "every undock and dock in the trip exports and every van move in the dispatch log; requests per "
                 "stocked second in each month, weekday or weekend, and local hour, times the seconds the station "
                 "stood empty in it. False starts (under 60 seconds, back at the same station) are not requests.")
    ws["A12"] = ("With the e-bikes every request is served: %.1f per cent of rides on an e-bike at the e-bike fare, as "
                 "on the Harbour pilot stations, and %.1f per cent more requests than the comparison stations drew."
                 % (fig["pilot"]["ebike_share"], fig["pilot"]["uplift"]))
    ws["A13"] = "Source: trip exports 2025, dispatch log, 03:00 audit, station feeds, Harbour pilot note and fares."
    for a in ("A11", "A12", "A13"):
        ws[a].font = Font(size=9)
        ws[a].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A11:I11"); ws.merge_cells("A12:I12"); ws.merge_cells("A13:I13")
    ws.row_dimensions[11].height = 40; ws.row_dimensions[12].height = 28
    _widths(ws, [14, 13, 17, 14, 13, 11, 15, 16, 15])
    ws.freeze_panes = "B5"
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1

    p = wb.create_sheet("Harbour pilot")
    p["A1"] = "Harbour e-bike pilot, 2025: what a pilot station did against a comparison station"
    p["A1"].font = Font(bold=True, size=12)
    _head(p, 3, ["Measure", "Value"])
    pl = fig["pilot"]
    rows = [("Pilot stations", pl["stations_pilot"]), ("Comparison stations", pl["stations_comparison"]),
            ("Rides from pilot stations", pl["rides_pilot"]), ("of which on e-bikes", pl["ebike_rides"]),
            ("E-bike share of rides at pilot stations", pl["ebike_share"] / 100.0),
            ("Rides from comparison stations", pl["rides_comparison"]),
            ("More rides a station at pilot stations than at comparison stations", pl["uplift"] / 100.0),
            ("Average e-bike fare, USD", pl["fare_ebike"]), ("Average classic fare at pilot stations, USD", pl["fare_classic"]),
            ("E-bike fare above the classic fare, USD a ride", pl["premium"])]
    for k, v in rows:
        p.append([k, v])
    for r in range(4, 4 + len(rows)):
        v = p["B%d" % r].value
        p["B%d" % r].number_format = "0.0%" if isinstance(v, float) and v < 1 and "share" in p["A%d" % r].value.lower() or "More rides" in p["A%d" % r].value else ("0.00" if isinstance(v, float) else "#,##0")
    _widths(p, [62, 14])

    pe = wb.create_sheet("Riders")
    pe["A1"] = "People who rode with us in 2025, by where they live"
    pe["A1"].font = Font(bold=True, size=12)
    _head(pe, 3, ["Home area", "People"])
    for n in NETS:
        pe.append([n, fig["people"][n]])
        pe["B%d" % pe.max_row].number_format = "#,##0"
    pe["A10"] = ("One person per rider with at least one ride in 2025 (false starts are not rides), placed by the home "
                 "area on the account. Accounts on one payment card are one person where the later account was opened "
                 "after the earlier account's last ride; two accounts riding through the same months on one card are "
                 "two people. January to June rides carry the old trip system's account numbers.")
    pe["A10"].alignment = Alignment(wrap_text=True, vertical="top"); pe["A10"].font = Font(size=9)
    pe.merge_cells("A10:B10"); pe.row_dimensions[10].height = 75
    _widths(pe, [60, 12])

    ch = wb.create_sheet("Charging")
    ch["A1"] = "Energy the Harbour pilot's charging points delivered, 2025"
    ch["A1"].font = Font(bold=True, size=12)
    _head(ch, 3, ["Month", "kWh"])
    for m in MONTHS:
        ch.append([m, fig["energy_kwh"][m]])
        ch["B%d" % ch.max_row].number_format = "#,##0"
    ch.append(["2025", sum(fig["energy_kwh"].values())])
    ch["A16"].font = Font(bold=True); ch["B16"].font = Font(bold=True); ch["B16"].number_format = "#,##0"
    ch["A18"] = ("Each session once: a controller re-sends its buffered sessions after a restart, stamped from a clock "
                 "it saved before the restart, so a session whose point already shows the same register readings is "
                 "not counted again. Sessions count in the local month their plug-out falls.")
    ch["A18"].alignment = Alignment(wrap_text=True, vertical="top"); ch["A18"].font = Font(size=9)
    ch.merge_cells("A18:B18"); ch.row_dimensions[18].height = 62
    _widths(ch, [52, 12])

    wk = wb.create_sheet("Workshop")
    wk["A1"] = "Workshop jobs per 10,000 rides, 2025"
    wk["A1"].font = Font(bold=True, size=12)
    _head(wk, 3, ["Quarter", "E-bike jobs", "E-bike rides", "E-bike jobs per 10,000 rides", "Classic jobs",
                  "Classic rides", "Classic jobs per 10,000 rides"])
    for q in range(1, 5):
        e, k = "E-bike Q%d" % q, "Classic Q%d" % q
        wk.append(["Q%d" % q, fig["workshop_jobs"][e], fig["workshop_rides"][e], fig["workshop_per_10000"][e],
                   fig["workshop_jobs"][k], fig["workshop_rides"][k], fig["workshop_per_10000"][k]])
        r = wk.max_row
        for col, f in zip("BCDEFG", ["#,##0", "#,##0", "0.0", "#,##0", "#,##0", "0.0"]):
            wk["%s%d" % (col, r)].number_format = f
    wk["A9"] = ("A job opened on a bike with no ride since its last job closed is that repair's road test failing, "
                "not a new fault, and is not counted. Rides exclude false starts; quarters by local time.")
    wk["A9"].alignment = Alignment(wrap_text=True, vertical="top"); wk["A9"].font = Font(size=9)
    wk.merge_cells("A9:G9"); wk.row_dimensions[9].height = 30
    _widths(wk, [10, 12, 13, 16, 12, 13, 16])

    nt = wb.create_sheet("Notes")
    nt["A1"] = "Notes"
    nt["A1"].font = Font(bold=True, size=12)
    notes = [("Prepared", "%s, e-bike product lead, 20 November 2026, for board item 7 (9 December 2026)." % P.PEOPLE["lead"]),
             ("Records", "Trips: %s and %s (old trip system, to 30 June), %s and %s (new platform, from 1 July). "
                         "Dispatch log %s; 03:00 audit %s; station feeds %s and %s as at 1 November 2026; account "
                         "register %s; charging sessions %s; workshop jobs %s."
                         % (P.FILES["q1"], P.FILES["q2"], P.FILES["q3"], P.FILES["q4"], P.FILES["moves"], P.FILES["audit"],
                            P.FILES["stations"], P.FILES["regions"], P.FILES["accounts"], P.FILES["charging"], P.FILES["workshop"])),
             ("Times", "Central Time throughout. The dispatch log and the charging and workshop exports are stamped in "
                       "UTC and were converted."),
             ("False starts", "An undock of under 60 seconds that ends at the station it started from is not a ride "
                              "and is not charged (fare schedule 2025)."),
             ("Fares", "Annual pass fees are not fares and are left out (board paper, item 7, section 2)."),
             ("Rounding", "The paper rounds revenue to the nearest USD 25,000 and requests to the nearest hundred; "
                          "this workbook carries the unrounded figures beside the rounded revenue.")]
    for i, (k, v) in enumerate(notes, 3):
        nt.cell(row=i, column=1, value=k).font = Font(bold=True)
        nt.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True, vertical="top")
        nt.cell(row=i, column=1).alignment = Alignment(vertical="top")
    nt.row_dimensions[4].height = 92
    _widths(nt, [14, 96])
    wb.properties.creator = P.PEOPLE["lead"]
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2026-11-20")
    postprocess.finish_office(path, "2026-11-12T14:05:00Z", "2026-11-20T16:48:00Z", P.ORG, person=P.PEOPLE["lead"])


def chart(path, fig):
    INK, MUTED, SURF, BLUE, ORANGE = "#0b0b0b", "#52514e", "#ffffff", "#2a78d6", "#eb6834"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    f, ax = plt.subplots(figsize=(7.2, 3.6), dpi=150)
    order = sorted(NETS, key=lambda n: -fig["net_revenue_exact"][n])
    y = list(range(len(order)))[::-1]
    rec = [fig["recorded_route_exact"][n] / 1000 for n in order]
    net = [fig["net_revenue_exact"][n] / 1000 for n in order]
    ax.barh([v + 0.19 for v in y], net, 0.36, color=BLUE, label="At 2025 demand (rides plus requests turned away)", zorder=3)
    ax.barh([v - 0.19 for v in y], rec, 0.36, color=ORANGE, label="On the rides the stations served", zorder=3)
    for v, n, a in zip(y, order, net):
        ax.text(a + 1.5, v + 0.19, "%d" % (fig["net_revenue"][n] // 1000), va="center", fontsize=8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(order, color=INK)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: "%d" % v))
    ax.set_xlabel("Net fare revenue a year, USD thousand", color=MUTED)
    ax.grid(axis="x", color="#e6e6e3", linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0, colors=MUTED)
    ax.set_xlim(0, max(net) * 1.18)
    ax.legend(frameon=False, loc="lower right", fontsize=7.6)
    f.suptitle("%s adds the most at 2025 demand; on the rides served alone, %s would lead" %
               (fig["recommended_network"], fig["recorded_route_pick"]), x=0.015, ha="left", fontsize=9.5, color=INK)
    f.subplots_adjust(left=0.15, right=0.98, top=0.88, bottom=0.15)
    f.savefig(path, facecolor=SURF, metadata={"Software": None})
    plt.close(f)


def paper(path, fig):
    best = fig["recommended_network"]
    nr, ta = fig["net_revenue"], fig["turned_away"]
    pl = fig["pilot"]
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for name, size in (("Heading 1", 15), ("Heading 2", 12)):
        hs = d.styles[name]
        hs.font.name = "Calibri"
        hs.font.size = Pt(size)
        hs.font.color.rgb = RGBColor(0x1F, 0x2A, 0x36)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        fp = s.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        fr = fp.add_run("%s | Board 9 December 2026 | Item 7 | page " % P.ORG_SHORT)
        fr.font.size = Pt(8)
        fr.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        pr = fp.add_run()
        pr.font.size = Pt(8)
        pr.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        for tag, val in (("w:fldChar", "begin"), ("w:instrText", "PAGE"), ("w:fldChar", "end")):
            el = OxmlElement(tag)
            if tag == "w:fldChar":
                el.set(qn("w:fldCharType"), val)
            else:
                el.set(qn("xml:space"), "preserve")
                el.text = val
            pr._r.append(el)
    p = d.add_paragraph()
    r = p.add_run("%s | Board of Directors, 9 December 2026 | Item 7, 2027 e-bike deployment" % P.ORG)
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    d.add_heading("The 300 e-bikes should go to %s, where they add %s a year in net fares" % (best, usd(nr[best])), level=1)
    p = d.add_paragraph()
    r = p.add_run("%s, e-bike product lead, 20 November 2026. For decision." % P.PEOPLE["lead"])
    r.italic = True
    r.font.size = Pt(9.5)
    d.add_heading("Decision sought", level=2)
    d.add_paragraph("Approve %s as the network for the %d e-bikes in the 2027 capital plan, so that the order can go to "
                    "the vendor by 15 January 2027 for the season opening on 1 April." % (best, fig["constants"]["ebikes"]))
    d.add_heading("Recommendation", level=2)
    others = sorted((n for n in NETS if n != best), key=lambda n: -fig["net_revenue_exact"][n])
    d.add_paragraph(
        "Put the 2027 e-bikes on the %s network. At 2025 demand they add %s a year in net fare revenue there, against "
        "%s on %s, the next best network, and %s or less on each of the others." %
        (best, usd(nr[best]), usd(nr[others[0]]), others[0], usd(max(nr[n] for n in others[1:]))))
    d.add_paragraph(
        "The case turns on demand rather than rides. A ride only exists when a rider finds a bike, and the two "
        "residence-hall hubs at %s run dry most teaching weekdays: the morning class change empties them, the noon "
        "change finds them empty, and they stay short until the 14:00 van. Rebuilding every station's stock from the "
        "03:00 audit, the trips and the van moves, the %s stations turned away about %s requests in 2025, %.0f per "
        "cent of their demand. Those riders pay nothing today; with e-bikes at every station they ride, and that "
        "revenue is new. On %s the stations turned away about %s requests and most e-bike rides would replace a "
        "classic ride, which adds only the e-bike premium of %s a ride."
        % (best, best, c(ta[best]), fig["turned_away_share"][best], others[0], c(ta[others[0]]),
           "USD %.2f" % pl["premium"]))
    d.add_paragraph(
        "Read on the rides the stations served, %s looks best (%s against %s for %s): that view counts only the "
        "riders who found a bike and so sends the e-bikes where supply already meets demand."
        % (fig["recorded_route_pick"], usd(fig["recorded_route"][fig["recorded_route_pick"]]),
           usd(fig["recorded_route"][best]), best))
    d.add_heading("Every network", level=2)
    t = d.add_table(rows=1, cols=5)
    t.style = "Light Grid Accent 1"
    for i, h in enumerate(["Network", "Rides 2025", "Requests turned away", "Net fare revenue a year",
                           "On served rides only"]):
        t.rows[0].cells[i].text = h
    for n in sorted(NETS, key=lambda n: -fig["net_revenue_exact"][n]):
        row = t.add_row().cells
        row[0].text, row[1].text, row[2].text = n, c(fig["rides_2025"][n]), "about %s" % c(ta[n])
        rr = fig["recorded_route"][n]
        row[3].text, row[4].text = usd(nr[n]), (usd(rr) if rr else "under USD 12,500")
    p = d.add_paragraph()
    r = p.add_run("Revenue to the nearest USD 25,000; requests to the nearest hundred. Annual pass fees are not fares and "
                  "are left out (item 7, section 2). Source: ebike_deployment_2027.xlsx.")
    r.font.size = Pt(8.5)
    tmp = tempfile.mkdtemp()
    png = os.path.join(tmp, "networks.png")
    chart(png, fig)
    d.add_picture(png, width=Cm(16))
    p = d.add_paragraph()
    r = p.add_run("Net fare revenue a year by network, at 2025 demand and on the rides the stations served; bars to scale, "
                  "labels in USD thousand to the nearest 25 (the served-rides figures are in the table above).")
    r.font.size = Pt(8.5)
    d.add_heading("How the figure is built", level=2)
    d.add_paragraph(
        "With the e-bikes, every request at the network's stations is served: %.1f per cent of rides go on an e-bike, "
        "the share riders chose at the Harbour pilot stations, and the e-bikes draw %.1f per cent more requests, the "
        "pilot stations' rides against the comparison stations'. Net fare revenue is what those riders would pay at "
        "the network's classic fare and the pilot's e-bike premium, less the fares the network took in 2025."
        % (pl["ebike_share"], pl["uplift"]))
    d.add_paragraph(
        "Turned-away requests come from each station's own requests per stocked second in each month, weekday or "
        "weekend, and local hour, applied to the seconds it stood empty in that hour. The pilot ran on Harbour, "
        "where stations rarely run dry, so the pilot's rides measure its demand.")
    d.add_heading("Supporting figures", level=2)
    d.add_paragraph(
        "The workbook gives the people who rode with us in 2025 by home area (%s: %s), the energy the pilot's "
        "charging points delivered each month (%s kWh in the year) and the workshop jobs per 10,000 rides by quarter "
        "(e-bikes %s to %s, classic bikes %s to %s)."
        % (best, c(fig["people"][best]), c(sum(fig["energy_kwh"].values())),
           "%.1f" % min(v for k, v in fig["workshop_per_10000"].items() if k.startswith("E")),
           "%.1f" % max(v for k, v in fig["workshop_per_10000"].items() if k.startswith("E")),
           "%.1f" % min(v for k, v in fig["workshop_per_10000"].items() if k.startswith("C")),
           "%.1f" % max(v for k, v in fig["workshop_per_10000"].items() if k.startswith("C"))))
    d.core_properties.author = P.PEOPLE["lead"]
    d.core_properties.title = "2027 e-bike deployment"
    d.save(path)
    postprocess.scrub(path, P.ORG, "2026-11-20")
    postprocess.finish_office(path, "2026-11-13T09:40:00Z", "2026-11-20T17:02:00Z", P.ORG, person=P.PEOPLE["lead"], revision=7)
    os.remove(png)
    os.rmdir(tmp)
