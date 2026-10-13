"""The goldens: the memo to the Fuel Price Commissioner (pass_through_inquiry_2027.docx: the call, the share of each
brand's examined stations found and, on page 2, the chart of regular litres by brand and month) and the inquiry scope
workbook (inquiry_scope_2027.xlsx: each brand's stations priced by the brand on 1 December 2026 and its regular litres
in each month of the first quarter, with notes), both written from figures.json."""
import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import survey as SV        # noqa: E402
import world as W          # noqa: E402

MEMO = "pass_through_inquiry_2027.docx"
SCOPE = "inquiry_scope_2027.xlsx"
ORDER = sorted(W.CODES, key=lambda b: W.NAME[b])
MONTHS = ["January 2026", "February 2026", "March 2026"]
MONTH_SHADES = ["#86b6ef", "#3987e5", "#184f95"]        # one blue, light to dark
INK, INK2, GRID, BAND, PAPER = "#1d2329", "#56606a", "#e1e5e9", "#f3efe6", "#ffffff"
REF = "PD-FPM-2026-41"


def figures(mc, litres, priced):
    """every figure the write-up and the goldens state"""
    sh = mc["shares"]
    ex_total = sum(n for _, n in sh.values())
    return {
        "call": W.NAME[mc["call"]] if mc["call"] else "none",
        "change_examined": W.CHANGE.isoformat(),
        "stations_examined": ex_total,
        "stations_examined_by_brand": {W.NAME[b]: sh[b][1] for b in ORDER},
        "stations_found": sum(f for f, _ in sh.values()),
        "stations_found_by_brand": {W.NAME[b]: sh[b][0] for b in ORDER},
        "share_found_nearest_ten_per_cent": {W.NAME[b]: "%d" % tens(sh[b]) for b in ORDER},
        "inquiry_bar": "one in ten",
        "false_discovery_rate": "5",
        "levy_regular_cents_2025": "%.2f" % W.LEVY["gasoline"][2025],
        "levy_regular_cents_2026": "%.2f" % W.LEVY["gasoline"][2026],
        "priced_by_brand_2026_12_01": {W.NAME[b]: priced[b] for b in ORDER},
        "regular_litres_thousands": {W.NAME[b]: {m: SV.thousands(litres[b][i]) for i, m in enumerate(MONTHS)}
                                     for b in ORDER},
        "survey_references_reissued": mc["reissued"],
        "found_towns": mc["found_towns"],
        "window_days": W.WINDOW,
        "days_with_a_price_each_window": W.MIN_DAYS,
        "standard_clauses": [num for _, items in D.STANDARD_CLAUSES for num, _ in items],
    }


def tens(fn):
    f, n = fn
    return int((f * 1000 // n + 50) // 100) * 10 if n else 0


def _fmt(x):
    return "{:,}".format(x)


# ------------------------------------------------------------------------------------------------- the chart
def chart_png(fig):
    lit = fig["regular_litres_thousands"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.6, "axes.edgecolor": INK2,
                         "axes.labelcolor": INK2, "xtick.color": INK, "ytick.color": INK2})
    f, ax = plt.subplots(figsize=(7.1, 3.7), dpi=170)
    f.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    width = 0.26
    names = [W.NAME[b] for b in ORDER]
    call = fig["call"]
    for i, nm in enumerate(names):
        if nm == call:
            ax.axvspan(i - 0.47, i + 0.47, color=BAND, zorder=0, linewidth=0)
    for j, m in enumerate(MONTHS):
        xs = [i + (j - 1) * width for i in range(len(names))]
        ys = [lit[nm][m] for nm in names]
        ax.bar(xs, ys, width=width - 0.025, color=MONTH_SHADES[j], label=m.split()[0] + " 2026", zorder=3,
               linewidth=0)
        k = names.index(call) if call in names else None
        if k is not None:
            ax.text(xs[k], ys[k] - 600, _fmt(ys[k]), ha="center", va="top", rotation=90, fontsize=7.4,
                    color="#ffffff" if j else INK, zorder=4)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels([nm.replace(" ", "\n", 1) for nm in names], fontsize=8.2)
    for lab in ax.get_xticklabels():
        if lab.get_text().replace("\n", " ") == call:
            lab.set_fontweight("bold")
    top = max(lit[nm][m] for nm in names for m in MONTHS)
    ax.set_ylim(0, top * 1.14)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: _fmt(int(v))))
    ax.set_ylabel("Thousand litres of regular")
    ax.yaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="both", length=0)
    ax.legend(ncol=3, frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0.0, 1.02))
    ax.set_title("Regular sold at the stations carrying each brand, first quarter of 2026", loc="left", fontsize=9.6,
                 fontweight="bold", color=INK, pad=12)
    f.tight_layout()
    buf = io.BytesIO()
    f.savefig(buf, format="png", facecolor=PAPER, metadata={"Software": None})
    plt.close(f)
    return buf.getvalue()


# ------------------------------------------------------------------------------------------------- the memo
def write_memo(path, fig, png):
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor

    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(27.94), Cm(21.59)
    sec.left_margin = sec.right_margin = Cm(2.3)
    sec.top_margin, sec.bottom_margin = Cm(2.0), Cm(1.9)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    st.font.size = Pt(10.5)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing = 1.1

    def para(text="", bold=False, size=None, color=None, after=None, italic=False, align=None):
        p = doc.add_paragraph()
        if text:
            r = p.add_run(text)
            r.bold, r.italic = bold, italic
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = RGBColor.from_string(color)
        if after is not None:
            p.paragraph_format.space_after = Pt(after)
        if align is not None:
            p.alignment = align
        return p

    def no_borders(tbl):
        b = OxmlElement("w:tblBorders")
        for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
            el = OxmlElement("w:%s" % e)
            el.set(qn("w:val"), "nil")
            b.append(el)
        tbl._tbl.tblPr.append(b)

    comm, comm_role = W.PEOPLE["commissioner"]
    who, role = W.PEOPLE["director"]
    para(W.BUREAU + "  |  " + W.DIVISION + "  |  Fuel Price Monitor", size=8.5, color="56606A", after=10)
    head = doc.add_table(rows=5, cols=2)
    no_borders(head)
    head.autofit = False
    head.columns[0].width, head.columns[1].width = Cm(2.5), Cm(14.4)
    for i, (k, v) in enumerate([("To", "%s, %s" % (comm, comm_role)),
                                ("From", "%s, %s" % (who, "Director, " + W.DIVISION)),
                                ("Date", "27 November 2026"), ("Reference", REF),
                                ("Subject", "The brand for the pass-through inquiry before the 1 January 2027 levy rise")]):
        head.cell(i, 0).width, head.cell(i, 1).width = Cm(2.5), Cm(14.4)
        r = head.cell(i, 0).paragraphs[0].add_run(k)
        r.bold = True
        r.font.size = Pt(9)
        r2 = head.cell(i, 1).paragraphs[0].add_run(v)
        r2.font.size = Pt(9)
        for cell in head.rows[i].cells:
            cell.paragraphs[0].paragraph_format.space_after = Pt(1)
    para("", after=2)

    call = fig["call"]
    share = fig["share_found_nearest_ten_per_cent"]
    para("Tallis Petroleum for the 2027 pass-through inquiry", bold=True, size=14, after=8)
    para("We recommend that your inquiry before the 1 January 2027 levy rise examine %s. At the 1 January 2026 rise, %s "
         "per cent of Tallis's examined stations passed on more than the rise under standard PM-04, with the false "
         "discovery rate across all %d stations examined held at 5 per cent. No station of the other six brands was "
         "found, so Tallis is the only brand at or above the one-in-ten share that clause 4.1 sets for an inquiry."
         % (call, share[call], fig["stations_examined"]))
    towns = [W.AREA_NAME[a] for a in fig["found_towns"]]
    para("The stations found are Tallis's company-run sites and commission agents in %s and %s, whose pump prices "
         "Tallis set itself at the change. From 1 January 2026 their margins over the rack price and the levy sat "
         "about 3 cents a litre above where they had been, and they have stayed there. Tallis's dealers in the same "
         "towns, and the other brands' stations around them, moved with their towns." % (", ".join(towns[:-1]),
                                                                                        towns[-1]))
    para("Harbourline's stations show the largest margin rises across the change, and a test of each station's change "
         "against its own day-to-day variation would find most of them. That test does not hold up. Margins in every "
         "town cycle over five to nine weeks, stations undercutting one another for a month or more and then restoring "
         "together, and Brackwater and Port Ostley, where most Harbourline stations trade, restored their prices around "
         "the turn of the year. Run at dates when the levy did not move, the same test finds a large part of every brand's "
         "stations, so it cannot hold the false discovery rate the standard sets. We judged each station's change "
         "against the 28-day changes its own margin made at every date in the log when the levy did not move; on "
         "that footing Harbourline's rises are ordinary for their towns.")
    hp = para("Stations found at the 1 January 2026 rise", bold=True, size=10, after=3)
    hp.paragraph_format.keep_with_next = True
    tb = doc.add_table(rows=len(ORDER) + 1, cols=3)
    tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.LEFT
    tb.autofit = False
    widths = (Cm(5.4), Cm(3.6), Cm(4.4))
    for j, h in enumerate(["Brand", "Stations examined", "Share found"]):
        c = tb.cell(0, j)
        r = c.paragraphs[0].add_run(h)
        r.bold = True
        r.font.size = Pt(9)
        if j:
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for i, b in enumerate(ORDER, 1):
        nm = W.NAME[b]
        vals = [nm, "%d" % fig["stations_examined_by_brand"][nm], "%s per cent" % share[nm]]
        for j, v in enumerate(vals):
            c = tb.cell(i, j).paragraphs[0]
            r = c.add_run(v)
            r.font.size = Pt(9)
            r.bold = nm == call
            if j:
                c.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for col, wd in zip(tb.columns, widths):
        col.width = wd
    for row in tb.rows:
        for c, wd in zip(row.cells, widths):
            c.width = wd
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
    para("Examined: carrying the brand on the register on 1 January 2026, with a daily price on at least 20 of the 28 "
         "days on each side of the change (PM-04 3.2). Share found to the nearest ten per cent, Benjamini-Hochberg at "
         "5 per cent across every station examined (PM-04 3.3).", size=8, color="56606A", after=10)
    para("The information request under clause 4.2 goes to the stations whose pump prices the brand sets: %d for "
         "Tallis on 1 December 2026, read from the November submissions, where a brand's pricing desk sends its "
         "stations' prices through its own system at the same minutes of the day for all of them. The register's site ownership "
         "column does not give this: dealer-owned commission agents are priced by the brand and company-owned "
         "dealer-run sites are not. The accompanying workbook gives every brand's count and the litres of regular its "
         "stations sold in the first quarter, which the chart overleaf shows."
         % fig["priced_by_brand_2026_12_01"][call])
    para("%s" % who, after=0)
    para("Director, %s" % W.DIVISION, size=9, color="56606A")

    brk = doc.add_paragraph()
    brk.add_run().add_break(WD_BREAK.PAGE)
    para("The litres behind each case", bold=True, size=11, after=4)
    pic = doc.add_paragraph()
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.add_run().add_picture(io.BytesIO(png), width=Cm(16.6))
    pic.paragraph_format.space_after = Pt(2)
    para("Figure 1. Thousand litres of regular sold at the stations carrying each brand in January, February and "
         "March 2026; %s's bars labelled. Monthly fuel sales survey: the latest revision of each return, counted for "
         "the month it reports, at the station carrying the brand that month. %d survey references freed when "
         "dealers closed between March and July 2026 were given to stations added to the frame from August; their "
         "January to March returns are the closed stations', found on the register by the site address each return "
         "carries."
         % (call, fig["survey_references_reissued"]), size=8, color="56606A", after=8)

    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fr = footer.add_run(REF + "   page ")
    fr.font.size = Pt(7.5)
    run = footer.add_run()
    run.font.size = Pt(7.5)
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)
    doc.core_properties.title = "Pass-through inquiry 2027"
    doc.save(path)
    PP.normalize_ooxml(path, who, who, "2026-11-26T14:12:00Z", "2026-11-27T16:48:00Z", title="Pass-through inquiry 2027")


# ------------------------------------------------------------------------------------------------- the workbook
def write_scope(path, fig):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    who = W.PEOPLE["director"][0]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inquiry scope"
    ws["A1"] = "Pass-through inquiry 2027: scope by brand"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "%s, %s, for the %s. Reference %s, 27 November 2026." % (W.BUREAU, W.DIVISION, W.COMMISSIONER, REF)
    ws["A2"].font = Font(italic=True, size=9, color="56606A")
    head = ["Brand", "Brand code", "Stations the brand prices itself, 1 December 2026",
            "Regular litres sold, January 2026 (thousands)", "Regular litres sold, February 2026 (thousands)",
            "Regular litres sold, March 2026 (thousands)"]
    fill = PatternFill("solid", fgColor="E6EAEE")
    for j, h in enumerate(head, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = Font(bold=True, size=10)
        c.fill = fill
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if j < 3 else "right")
    ws.row_dimensions[4].height = 46
    hair = Border(bottom=Side(style="hair", color="C8CDD2"))
    for i, b in enumerate(ORDER):
        nm = W.NAME[b]
        lit = fig["regular_litres_thousands"][nm]
        vals = [nm, b, fig["priced_by_brand_2026_12_01"][nm]] + [lit[m] for m in MONTHS]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=5 + i, column=j, value=v)
            c.border = hair
            if j >= 3:
                c.number_format = "#,##0"
            if nm == fig["call"]:
                c.font = Font(bold=True)
    for col, wd in zip("ABCDEF", (22, 11, 20, 19, 19, 19)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "C5"
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    ns = wb.create_sheet("Notes")
    notes = [
        "Stations the brand prices itself: stations carrying the brand and open on 1 December 2026 whose pump prices "
        "the brand sets (PM-04 4.2). Read from the platform's November 2026 submissions: a brand's pricing desk sends "
        "the prices of the stations it prices through its own system at the same minutes of the day for all of them, "
        "so the brand's push times are the minutes of the day at which three or more of its stations submitted "
        "regular prices through the API, and a station counts when most of its regular-price changes came at its "
        "brand's push times. The register's site_ownership column records who owns the site, not "
        "who sets the price: commission agents on dealer-owned sites are priced by the brand, and company-owned "
        "sites leased to dealers are priced by the dealer. Dealer groups' and software vendors' systems also submit "
        "through the API, at their own times.",
        "Regular litres: the monthly fuel sales survey, the latest revision of each return, counted for the month it "
        "reports (reference_month), not the month it was processed, at the station that filed it and under the "
        "brand that station carried that month on the register's brand history; a station that opened or closed "
        "during a month is counted in full under the brand it traded that month. Brand changes take effect on the "
        "first of a month. Rounded to the nearest thousand litres.",
        "Survey references: when a station closes, the frame frees its reference and may give it to a station added "
        "to the frame later. %d references freed when dealers closed between March and July 2026 were given to "
        "stations added to the frame from August to October 2026; the frame now shows only the new holder, while the "
        "January to March returns under those references were filed by the closed stations. Those returns are "
        "matched to the closed stations on the register by the site address each return carries." %
        fig["survey_references_reissued"],
        "Brands in alphabetical order. %s is the brand recommended for the inquiry (memo %s)." % (fig["call"], REF),
    ]
    ns["A1"] = "Notes"
    ns["A1"].font = Font(bold=True)
    for i, t in enumerate(notes, 2):
        c = ns.cell(row=i, column=1, value="%d. %s" % (i - 1, t))
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ns.row_dimensions[i].height = 118 if i == 2 else 74
    ns.column_dimensions["A"].width = 118
    ns.page_setup.orientation = "landscape"
    ns.page_setup.fitToWidth = 1
    ns.page_setup.fitToHeight = 0
    ns.sheet_properties.pageSetUpPr.fitToPage = True
    wb.active = 0
    wb.save(path)
    PP.normalize_ooxml(path, who, who, "2026-11-26T10:05:00Z", "2026-11-27T16:41:00Z", excel=True)
