"""The golden deliverables (tier_g_2027.xlsx and tier_g_2027.docx) and figures.json, from target/ alone."""
import json
import os

import analysis as AN
import io_util as IO

BOOK = "tier_g_2027.xlsx"
PAGE = "tier_g_2027.docx"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#c9c8c3"
TIER = "#2a78d6"


def compute(target):
    M = AN.main_call(target, "duration")
    R1 = AN.main_call(target, "linemap")
    R0 = AN.main_call(target, "none")
    RA = AN.main_call(target, "allday")
    mg = AN.make_good(target)
    sc = AN.screens_on_sale(target)
    rev = AN.net_revenue(target)
    bk = AN.load_bookings(target)
    parts = AN.net_revenue_parts(target)
    rates = {}
    for s in AN.load_statements(target):
        base = sum(parts["invoiced"][r] + sum(a for d, a in parts["credits"][r] if d <= s["date"]) for r in s["refs"])
        rates[s["agency"]] = s["amount"] / base
    return {"M": M, "R1": R1, "R0": R0, "RA": RA, "make_good": mg, "screens": sc, "revenue": rev, "bookings": bk,
            "rates": rates}


def r10(x):
    return int(round(x / 10.0)) * 10


def figures(c):
    M = c["M"]
    pk = M.packages
    f = {"call": [pk[k][0] for k in M.tier], "tier_codes": M.tier,
         "regular_riders": len(M.regular),
         "reach": {pk[k][0]: int(round(M.reach[k])) for k in pk},
         "reach_exact": {pk[k][0]: round(M.reach[k], 3) for k in pk},
         "reach_linemap": {pk[k][0]: int(round(c["R1"].reach[k])) for k in pk},
         "tier_linemap": [pk[k][0] for k in c["R1"].tier],
         "reach_gates_only": {pk[k][0]: int(round(c["R0"].reach[k])) for k in pk},
         "tier_gates_only": [pk[k][0] for k in c["R0"].tier],
         "make_good_hours": {b["booking_ref"]: c["make_good"][b["booking_ref"]]["make_good"] for b in c["bookings"]},
         "screens_on_sale_2027": {pk[k][0]: c["screens"][k] for k in pk},
         "net_revenue_eur": {pk[k][0]: r10(c["revenue"][k]) for k in pk},
         "tier_line_pct": 40, "effective_frequency": 3, "headway_min": 3, "make_good_allowance_pct": 0.5,
         "agency_rates_pct": {a: round(100 * v, 1) for a, v in c["rates"].items()},
         "booking_package": {b["booking_ref"]: b["package"] for b in c["bookings"]},
         "peak_windows": "07:00 to 09:30 and 16:00 to 18:30",
         "clauses_cited": "rate card 3.1, 3.2, 3.3, 3.4, 3.5; general terms 6.1, 6.2, 6.3, 8.2, 8.3"}
    return f


def chart(c, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    M = c["M"]
    pk = M.packages
    codes = sorted(pk, key=lambda k: -M.reach[k])
    vals = [int(round(M.reach[k])) for k in codes]
    names = [pk[k][0] for k in codes]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "t255"})
    fig, ax = plt.subplots(figsize=(6.9, 3.55), dpi=200)
    cols = [TIER if k in M.tier else MUTED for k in codes]
    ax.barh(range(len(codes)), vals, color=cols, height=0.66, edgecolor="white", linewidth=1.0)
    ax.axvline(40, color=INK2, lw=1.0, ls=(0, (4, 3)))
    ax.text(40.5, -0.75, "Tier G line, 40%", color=INK2, fontsize=7.8, va="center")
    for i, v in enumerate(vals):
        ax.text(v + 0.7, i, "%d%%" % v, va="center", fontsize=8, color=INK)
    ax.set_yticks(range(len(codes)))
    ax.set_yticklabels(names, color=INK)
    ax.set_ylim(len(codes) - 0.4, -1.2)
    ax.set_xlim(0, 60)
    ax.set_xticks(range(0, 61, 10))
    ax.set_xticklabels(["%d%%" % x for x in range(0, 61, 10)], color=INK2)
    ax.set_xlabel("Regular riders passing the package's screens three times or more, 5 Oct to 1 Nov 2026",
                  color=INK2, fontsize=7.8)
    ax.tick_params(axis="both", length=0)
    ax.grid(axis="x", color="#ecebe7", lw=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#bdbcb6")
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def workbook(c, f, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    M = c["M"]
    pk = M.packages
    wb = Workbook()
    wb.remove(wb.active)
    bold, grey = Font(bold=True), Font(color="52514E", italic=True, size=9)
    head_fill = PatternFill("solid", fgColor="EDF2F8")

    def sheet(name, title, header, rows, widths, formats, notes):
        ws = wb.create_sheet(name)
        ws.append([title])
        ws["A1"].font = Font(bold=True, size=12)
        ws.append([])
        ws.append(header)
        for cell in ws[3]:
            cell.font = bold
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="bottom")
        for r in rows:
            ws.append(list(r))
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
        for row in ws.iter_rows(min_row=4, max_row=3 + len(rows)):
            for i, cell in enumerate(row):
                if formats.get(i):
                    cell.number_format = formats[i]
                    cell.alignment = Alignment(horizontal="right")
        ws.freeze_panes = "A4"
        ws.row_dimensions[3].height = 30
        r0 = 5 + len(rows)
        for k, line in enumerate(notes):
            ws.cell(row=r0 + k, column=1, value=line).font = grey
        return ws

    order = sorted(pk, key=lambda k: -M.reach[k])
    sheet("Tier G 2027", "Tier G 2027: effective reach by package, audience window 5 October to 1 November 2026",
          ["Package", "Code", "Effective reach (%)", "Tier 2027"],
          [[pk[k][0], k, int(round(M.reach[k])), "Tier G" if k in M.tier else "standard"] for k in order],
          [20, 8, 14, 12], {2: "0"},
          ["Regular riders: %s passenger cards with a metro journey in each calendar week of the window; staff and "
           "service cards left out (rate card 3.3)." % format(len(M.regular), ","),
           "Passes: the hall of check-in, the hall of check-out and the interchange passage wherever the rider "
           "changed trains (3.4); a journey without a check-out counts its check-in hall only.",
           "Changes at Centraal read from each journey's duration: on weekday peaks (07:00 to 09:30, 16:00 to 18:30) "
           "north runs through to east and west to south."])
    bk = c["bookings"]
    sheet("Make-good", "Make-good owed on the autumn 2026 bookings",
          ["Booking", "Advertiser", "Package", "Flight", "Make-good (hours)"],
          [[b["booking_ref"], b["advertiser"], b["package"], "%s to %s" % (b["start"].strftime("%d %b"),
                                                                           b["end"].strftime("%d %b")),
            c["make_good"][b["booking_ref"]]["make_good"]] for b in bk],
          [12, 26, 16, 18, 14], {4: "#,##0"},
          ["Dark hours above 0.5 per cent of booked screen-hours, in whole hours, part of an hour counted as an hour "
           "(general terms 6.3).",
           "Player log times are UTC and were read in Ravelmond time; re-cablings dated from the receiving player's "
           "display report, not the register's entry."])
    sheet("Screens 2027", "Screens on sale on 1 January 2027",
          ["Package", "Code", "Screens"],
          [[pk[k][0], k, c["screens"][k]] for k in pk], [20, 8, 10], {2: "0"},
          ["From the screen register of 12 November 2026: one screen to a position; planned hangings and take-downs "
           "dated on or before 1 January counted; screens held outside the packages left out."])
    sheet("Net revenue", "Net revenue from the autumn 2026 bookings, by package",
          ["Package", "Code", "Net revenue (EUR)"],
          [[pk[k][0], k, r10(c["revenue"][k])] for k in pk], [20, 8, 16], {2: "#,##0"},
          ["Invoiced value excluding VAT, less credit notes, less the agency commission due at each agency's contract "
           "rate (general terms 8.2, 8.3); rounded to the nearest 10 euros."])
    for ws in wb.worksheets:
        ws.sheet_view.showGridLines = False
        ws.print_title_rows = "3:3"
    wb.save(path)
    IO.repack_xlsx(path, "Floortje Brugman", "Floortje Brugman", "2026-11-13T13:40:00Z", "2026-11-13T15:55:00Z",
                   "Tier G 2027", "Spoorbeeld Media B.V.")


def page(c, f, path, png):
    """A one-page note in Word: the identifying block, the finding as its title, the chart, the reasoning."""
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt, RGBColor
    tier = sorted(f["call"], key=lambda k: -f["reach_exact"][k])
    names = "%s, %s and %s" % tuple(tier)
    reach, lm = f["reach"], f["reach_linemap"]
    below = sorted((k for k in reach if k not in tier), key=lambda k: -f["reach_exact"][k])[0]
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin, sec.bottom_margin = Cm(1.7), Cm(1.6)
    base = doc.styles["Normal"]
    base.font.name = "Arial"
    base.font.size = Pt(9.5)
    grey = RGBColor(0x52, 0x51, 0x4E)

    def para(text, size=9.5, bold=False, colour=None, after=4, italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        if colour is not None:
            r.font.color.rgb = colour
        return p
    para("Spoorbeeld Media B.V. \u00b7 Audience research \u00b7 13 November 2026", 8.5, colour=grey, after=1)
    para("To: commercial director, rate card 2027 \u00b7 From: Floortje Brugman \u00b7 Subject: Tier G 2027", 8.5,
         colour=grey, after=10)
    para("%s clear the 40 per cent Tier G line; Centraal and Binnenstad do not" % names, 13, bold=True, after=8)
    pic = doc.add_paragraph()
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.paragraph_format.space_after = Pt(2)
    pic.add_run().add_picture(png, width=Cm(16.8))
    para("Source: RVB OV-chipkaart metro journeys 1 October to 4 November 2026 (re-export of 5 November), RVB planning "
         "model 2026, rate card 2027 Annex A.", 7.5, colour=grey, after=10)
    para("Three packages qualify for Tier G in 2027: %s at %d, %d and %d per cent of the %s regular riders. %s is the "
         "nearest below the line at %d per cent." % (names, reach[tier[0]], reach[tier[1]], reach[tier[2]],
                                                     format(f["regular_riders"], ","), below, reach[below]), after=6)
    para("Centraal and Binnenstad both come to %d per cent. Put every change of trains where the line map puts it and "
         "they would reach %d and %d per cent, but the journeys' own durations show that on weekday peaks, 07:00 to "
         "09:30 and 16:00 to 18:30, trains from the north branch run on to the east branch and trains from the west run "
         "on to the south. The north-east and west-south commuters, the largest flows, stay on board through Centraal "
         "and never use the interchange passage; the north-south and west-east commuters change there instead."
         % (reach["Centraal"], lm["Centraal"], lm["Binnenstad"]), after=10)
    para("Regular riders are passenger cards with a metro journey in each calendar week from 5 October to 1 November "
         "2026; staff and service cards are left out (rate card 3.3). A journey without a check-out counts its check-in "
         "hall only (3.4). Make-good, the screens on sale on 1 January and net revenue by package are in "
         "tier_g_2027.xlsx.", 8, colour=grey, italic=True, after=0)
    doc.core_properties.title = "Tier G 2027"
    doc.save(path)
    IO.repack_xlsx(path, "Floortje Brugman", "Floortje Brugman", "2026-11-13T14:30:00Z", "2026-11-13T16:10:00Z",
                   "Tier G 2027", "Spoorbeeld Media B.V.", application="Microsoft Office Word")


def write_all(target, golden, gen):
    os.makedirs(golden, exist_ok=True)
    os.makedirs(gen, exist_ok=True)
    c = compute(target)
    f = figures(c)
    workbook(c, f, os.path.join(golden, BOOK))
    png = os.path.join(gen, "reach_chart.png")
    chart(c, png)
    page(c, f, os.path.join(golden, PAGE), png)
    json.dump(f, open(os.path.join(gen, "figures.json"), "w"), indent=1, sort_keys=True)
    return c, f
