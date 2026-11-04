"""Write the golden deliverables from golden.compute: the Authority's return file, the covering note with its chart,
and the terminal's stock account; and generator/figures.json, which the write-up is drafted from."""
import csv
import io
import json
import os

import golden as G
import terminal as T
import world as W

POINTS = ["VRU-1", "BAY-4", "BAY-5"]
TANKS = list(W.TANKS)
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def r1(v):
    return float("%.1f" % v)


def figures(c):
    q = {"%s Q%d" % (p, qi): r1(c["quarters"][(p, qi)]) for p in POINTS for qi in range(1, 5)}
    year = {p: r1(sum(c["quarters"][(p, qi)] for qi in range(1, 5))) for p in POINTS}
    tanks = {tk: int(round(c["tanks"][tk])) for tk in TANKS}
    gain = {"%s Q%d" % (tk, qi): int(round(c["gain"][(tk, qi)])) for tk in TANKS for qi in range(1, 5)}
    switch_kl = sum(pl["l"]["gross"] for pl in c["per_load"] if pl["switch"]) / 1e6
    dist_kl = sum(pl["l"]["gross"] for pl in c["per_load"]) / 1e6
    rungs = {r: r1(sum(v for v in c["load"][r].values())) for r in c["load"]}
    return {
        "call": {"total_t": r1(c["total"]), "limit_t": W.LIMIT_T, "exceeded": bool(c["over"]),
                 "excess_t": r1(c["excess"])},
        "components": {"distillate_bays_t": r1(sum(c["quarters"][(p, qi)] for p in ("BAY-4", "BAY-5")
                                                   for qi in range(1, 5))),
                       "switch_ml": float("%.1f" % switch_kl), "distillate_ml": float("%.1f" % dist_kl),
                       "vru_t": year["VRU-1"]},
        "loading_quarters_t": q, "loading_year_t": year, "tanks_kg": tanks, "stock_gain_kl": gain,
        "rungs_distillate_t": rungs,
        "saturation": {"vapour_balanced": 1.0, "normal": 0.6},
    }


def write_return(path, fig):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(["licence_no", "year", "section", "point_id", "period", "substance", "quantity", "unit"])
    for p in POINTS:
        for qi in range(1, 5):
            w.writerow([W.LICENCE_NO, 2026, "LOADING", p, "Q%d" % qi, "VOC", "%.1f" % fig["loading_quarters_t"]["%s Q%d" % (p, qi)], "t"])
    for tk in TANKS:
        w.writerow([W.LICENCE_NO, 2026, "TANKS", tk, "YEAR", "VOC", fig["tanks_kg"][tk], "kg"])
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())


def chart_png(path, c, fig):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task461"})
    colours = {"BAY-4": "#2a78d6", "BAY-5": "#eb6834", "VRU-1": "#1baf7a"}
    labels = {"BAY-4": "Bay 4 (distillate)", "BAY-5": "Bay 5 (distillate)", "VRU-1": "VRU-1 stack (bays 1 to 3)"}
    order = ["BAY-4", "BAY-5", "VRU-1"]
    figp, ax = plt.subplots(figsize=(6.6, 3.15), dpi=200)
    bottom = [0.0] * 12
    for p in order:
        vals = [c["monthly"].get((p, m), 0.0) for m in range(1, 13)]
        ax.bar(range(12), vals, bottom=bottom, width=0.62, color=colours[p], edgecolor="#fcfcfb", linewidth=0.8,
               label="%s, %.1f t" % (labels[p], fig["loading_year_t"][p]))
        bottom = [b + v for b, v in zip(bottom, vals)]
    for i, b in enumerate(bottom):
        ax.text(i, b + 0.06, "%.1f" % b, ha="center", va="bottom", fontsize=7, color="#52514e")
    ax.set_xticks(range(12))
    ax.set_xticklabels(MONTHS)
    ax.set_ylabel("Tonnes of VOC released")
    ax.set_ylim(0, max(bottom) * 1.18)
    ax.grid(axis="y", color="#e4e3df", linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#9b9a96")
    ax.tick_params(colors="#52514e")
    ax.set_title("VOC from product loading by month, 2026: %.1f t for the year against the %.0f t limit"
                 % (fig["call"]["total_t"], W.LIMIT_T), fontsize=9, color="#0b0b0b", loc="left")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False, fontsize=7.5)
    figp.tight_layout()
    figp.savefig(path, metadata={"Software": None}, facecolor="#fcfcfb")
    plt.close(figp)


def write_note(path, c, fig, png):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    import docs  # noqa: F401  (registers the fonts)
    body = ParagraphStyle("b", fontName="LiberationSerif", fontSize=10.3, leading=14, spaceAfter=6)
    small = ParagraphStyle("s", fontName="LiberationSans", fontSize=8.3, leading=10.6, textColor=colors.HexColor("#52514e"))
    head = ParagraphStyle("h", fontName="LiberationSans-Bold", fontSize=12.5, leading=16, spaceAfter=2)
    cell = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.6, leading=10.8)
    cellb = ParagraphStyle("cb", parent=cell, fontName="LiberationSans-Bold")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Annual return 2026, EPL 20514: covering note",
                            author=W.PEOPLE["manager"], subject="", creator="", producer="")
    f = fig

    def footer(canvas, d):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.4)
        canvas.setFillColor(colors.HexColor("#52514e"))
        canvas.drawString(22 * mm, 10 * mm, "Brennock Fuels  |  EPL 20514 annual return 2026, covering note under "
                                            "condition R2  |  Ref WT-ENV-2027-003")
        canvas.drawRightString(A4[0] - 22 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    s = [Paragraph("Brennock Fuels Pty Ltd, Warrenby terminal, 14 Wharf Road, Port Warrenby", small),
         Spacer(1, 4),
         Paragraph("Product loading at the Warrenby terminal released %.1f t of VOC in 2026, %.1f t over the "
                   "licence limit" % (f["call"]["total_t"], f["call"]["excess_t"]), head),
         Paragraph("To: Industry Reporting, %s, Coastal Region. From: %s, %s. 8 January 2027. Covering note to the "
                   "2026 annual return under condition R2 of Environment Protection Licence 20514." %
                   (W.AUTHORITY, W.PEOPLE["manager"], W.TITLES["manager"]), small),
         Spacer(1, 8),
         Paragraph("The terminal released <b>%.1f tonnes</b> of VOC from product loading in 2026. Condition L1 limits "
                   "that release to %.0f tonnes in a calendar year, so the terminal <b>exceeded the limit by %.1f "
                   "tonnes</b>. The release at each loading point in each quarter is in the return file lodged with "
                   "this note." % (f["call"]["total_t"], W.LIMIT_T, f["call"]["excess_t"]), body),
         Paragraph("Bays 4 and 5 are not connected to VRU-1, so their release is estimated load by load: the diesel "
                   "loaded into each compartment pushes out the vapour that compartment carried back from its "
                   "previous delivery. Of the %.1f ML of diesel loaded at the two bays, %.1f ML went into "
                   "compartments whose previous delivery was petrol made through a service station's vapour "
                   "balance, and each of those loads released saturated petrol vapour (properties from Tables 1 and "
                   "2 of the return protocol, at the loading meter's temperature). The rest released diesel vapour "
                   "only. The VRU-1 figures are the stack monitor's, worked under section 3 of the protocol."
                   % (f["components"]["distillate_ml"], f["components"]["switch_ml"]), body),
         Spacer(1, 4)]
    rows = [["Loading point", "Q1", "Q2", "Q3", "Q4", "2026"]]
    for p, nm in (("VRU-1", "VRU-1 stack (bays 1 to 3)"), ("BAY-4", "Bay 4"), ("BAY-5", "Bay 5")):
        rows.append([nm] + ["%.1f" % f["loading_quarters_t"]["%s Q%d" % (p, qi)] for qi in range(1, 5)] +
                    ["%.1f" % f["loading_year_t"][p]])
    rows.append(["All loading points", "", "", "", "", "%.1f" % f["call"]["total_t"]])
    t = Table([[Paragraph(str(x), cellb if (i == 0 or j == 0) else cell) for j, x in enumerate(r)]
               for i, r in enumerate(rows)], colWidths=[52 * mm] + [20 * mm] * 5, hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#52514e")),
                           ("LINEABOVE", (0, -1), (-1, -1), 0.4, colors.HexColor("#9b9a96")),
                           ("ALIGN", (1, 0), (-1, -1), "RIGHT")]))
    s.append(Paragraph("Tonnes of VOC released, 2026", cellb))
    s.append(t)
    s.append(Paragraph("Source: return file warrenby_2026_annual_return.csv lodged with this note; VRU-1 from its "
                       "continuous emission monitor, bays 4 and 5 from the terminal management system's loads and the "
                       "dispatch system's delivery dockets.", small))
    s.append(Spacer(1, 8))
    s.append(Image(png, width=166 * mm, height=79 * mm))
    s.append(Spacer(1, 6))
    s.append(Paragraph("We will report separately on the vapour collection works at bays 4 and 5 that this result "
                       "calls for.", body))
    s.append(Paragraph("%s, %s" % (W.PEOPLE["manager"], W.TITLES["manager"]), body))
    s.append(Spacer(1, 10))
    s.append(Paragraph("Quarters and the year are calendar periods in the premises' local time (licence D1); VOC is "
                       "reported as its own mass (licence D3).", small))
    doc.build(s, onFirstPage=footer, onLaterPages=footer)


def write_stock(path, c, fig):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Stock account 2026"
    ws["A1"] = "Warrenby terminal stock account, 2026 (kilolitres at 15 C)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Stock at local midnight opening and closing each quarter, from the 06:00 AEST dips with the loads "
                "and VRU-1 returns between midnight and the dip added back. Gain positive, loss negative.")
    cols = ["Tank", "Quarter", "Opening stock", "Received from ships", "Returned by VRU-1", "Transfers in",
            "Loaded at the bays", "Transfers out", "Closing stock", "Gain or loss"]
    for j, h in enumerate(cols, start=1):
        cell = ws.cell(row=4, column=j, value=h)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="E7E6E2")
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    r = 5
    for tk in TANKS:
        for qi in range(1, 5):
            p = c["parts"][(tk, qi)]
            vals = [tk, "Q%d" % qi, p["opening"] / 1000, p["received"] / 1000, p["returned"] / 1000, p["t_in"] / 1000,
                    p["dispatched"] / 1000, p["t_out"] / 1000, p["closing"] / 1000,
                    fig["stock_gain_kl"]["%s Q%d" % (tk, qi)]]
            for j, v in enumerate(vals, start=1):
                cell = ws.cell(row=r, column=j, value=round(v, 1) if isinstance(v, float) else v)
                if j >= 3:
                    cell.number_format = "#,##0.0" if j < 10 else "#,##0;-#,##0"
            r += 1
    for qi in range(1, 5):
        tot = sum(c["gain"][(tk, qi)] for tk in TANKS)
        ws.cell(row=r, column=1, value="Terminal").font = Font(bold=True)
        ws.cell(row=r, column=2, value="Q%d" % qi).font = Font(bold=True)
        cell = ws.cell(row=r, column=10, value=int(round(tot)))
        cell.font = Font(bold=True)
        cell.number_format = "#,##0;-#,##0"
        r += 1
    for col, wdt in zip("ABCDEFGHIJ", (9, 8, 13, 13, 12, 11, 13, 11, 13, 11)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "C5"
    ws.print_title_rows = "4:4"
    nt = wb.create_sheet("Notes")
    notes = [("Prepared", "8 January 2027, %s, %s" % (W.PEOPLE["manager"], W.TITLES["manager"])),
             ("Volumes", "Kilolitres at 15 C throughout; tank stocks are the tank gauging system's net standard "
                         "volumes"),
             ("Midnight stocks", "The gauging system dips at 06:00 AEST every day (07:00 local while daylight saving "
                                 "runs); each quarter's opening and closing stock is that dip with the loads and the "
                                 "VRU-1 product returns between local midnight and the dip added back or taken off"),
             ("Received", "Ships: the surveyors' shore received figures, by discharge date. VRU-1: the absorber return "
                          "pump's deliveries to the tank the absorber was lined up to (TK-1, except %s). Transfers: the "
                          "control room's transfer meter readings" % "; ".join(
                              "%s to %s on %s" % (a.strftime("%d %B").lstrip("0"), b.strftime("%d %B").lstrip("0"), tk)
                              for a, b, tk, _ in T.ABSORBER_PLAN)),
             ("Loaded", "Terminal management system loads (legacy export to 30 June, new system from 1 July), diesel "
                        "put on TK-4 or TK-5 by the header line-up in the shift log"),
             ("Sign", "Gain positive, loss negative; whole kilolitres")]
    for i, (k, v) in enumerate(notes, start=1):
        nt.cell(row=i, column=1, value=k).font = Font(bold=True)
        nt.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 16
    nt.column_dimensions["B"].width = 96
    wb.save(path)


def main(target, gdir, fig_path):
    import postprocess as PP
    os.makedirs(gdir, exist_ok=True)
    c = G.compute(target)
    fig = figures(c)
    write_return(os.path.join(gdir, W.GOLDEN["return"]), fig)
    png = os.path.join(os.path.dirname(fig_path), ".chart_note.png")
    chart_png(png, c, fig)
    write_note(os.path.join(gdir, W.GOLDEN["note"]), c, fig, png)
    os.remove(png)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["note"]), b"D:20270108101400+11'00'", b"D:20270108101400+11'00'")
    write_stock(os.path.join(gdir, W.GOLDEN["stock"]), c, fig)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["stock"]), W.PEOPLE["manager"], W.PEOPLE["manager"],
                       "2027-01-06T21:40:00Z", "2027-01-07T23:02:00Z", excel=True, company=W.ORG)
    with open(fig_path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
    return c, fig
