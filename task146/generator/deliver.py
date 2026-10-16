"""The goldens, computed from the shipped pack: Rothwell Bank's one-page initial claims preview (docx, with its chart of
the weekly national count from April 2026 and the call) and the preview workbook (the call, the notified layoffs by
region and period, the third quarter's change in initial claims by industry group); and generator/figures.json, every
figure the write-up states."""
from __future__ import annotations

import datetime as dt
import io
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt               # noqa: E402
from matplotlib import font_manager            # noqa: E402

import calc as C                               # noqa: E402
import common as K                             # noqa: E402
import industry as I                           # noqa: E402
import notices as N                            # noqa: E402
import postprocess as PP                       # noqa: E402

GOLD_DOC = "ic_preview_2026-10-10.docx"
GOLD_BOOK = "ic_preview_2026-10-10.xlsx"
WCI = ("Western", "Coastal", "Island")
CHART_FROM = dt.date(2026, 4, 5)              # the first claims week of April 2026 (ended 11 April)
for _f in ("Carlito-Regular.ttf", "Carlito-Bold.ttf"):
    font_manager.fontManager.addfont("/usr/share/fonts/truetype/crosextra/" + _f)
INK, INK2, GRID, PAPER = "#0b0b0b", "#52514e", "#e2e1dc", "#fcfcfb"
SERIES_C, CALL_C = "#2a78d6", "#eb6834"      # categorical slots 1 and 2, validated (light surface)


def compute(target):
    V = C.from_pack(target)
    L = C.ladder(V)
    cm = C.components(V, L)
    pr = C.precision(V, L)
    a, _ = C.ask_a(target)
    b, tot = C.ask_b(target)
    weeks = [d for d in V.weeks if d >= CHART_FROM]
    return dict(V=V, L=L, cm=cm, pr=pr, a=a, b=b, b_tot=tot, chart=[(d, V.nat[d]) for d in weeks],
                call=K.round_to(L["gold"], 1000), refile_lo=4000, refile_hi=5000, without_lo=11000, without_hi=12000,
                base=int(round(cm["base"])), pool=int(cm["pool"]),
                national=K.round_to(L["national"]["all turns"], 1000),
                groups_lower=sum(1 for k in I.G if k not in (4, 7) and b[k] < 0),
                industry_sentence=industry_sentence(b, tot),
                pool_wci_pct=K.round_dp(100.0 * cm["pool_wci_share"], 1),
                shares={r: cm["shares"][r] for r in K.REGIONS})


WORDS = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "all twelve"}


def industry_sentence(b, tot):
    """What the industry table says about the rise on a year ago, worded from the figures."""
    rise = {k: tot[2026][k] - tot[2025][k] for k in I.G}
    total = sum(rise.values())
    lower = sum(1 for k in I.G if k not in (4, 7) and b[k] < 0)
    ca = rise[4] + rise[7]
    if ca > total:
        head = "Claims from construction and accommodation rose by more than the whole rise on a year ago"
    else:
        head = "Construction and accommodation account for %s of the rise in claims on a year ago" % (
            "most" if ca > 0.5 * total else "part")
    return "%s; %s of the other twelve industry groups %s lower." % (head, WORDS[lower], "is" if lower == 1 else "are")


def n0(v):
    return "{:,}".format(int(v))


def pct1(v):
    return "%.1f" % K.round_dp(v, 1)


def figures(c):
    cm = c["cm"]
    return {
        "call": {"initial_claims_week_ended_2026-10-10": n0(c["call"]), "release": "15 October 2026"},
        "critical_components": {
            "ineligible_determinations_jul_sep_2026": n0(c["pool"]),
            "share_in_western_coastal_island_pct": "%.1f" % c["pool_wci_pct"],
            "refiled_claims_range": [n0(c["refile_lo"]), n0(c["refile_hi"])],
            "refiled_share_wci": "nine tenths",
            "week_without_refiling_range": [n0(c["without_lo"]), n0(c["without_hi"])],
            "first_week_share_words": "one in four (Western), three in ten (Coastal, Island), fewer than one in ten "
                                      "(the other five regions)",
            "pool_against_usual": "about one and a half times a usual quarter's; about a fifth in the three regions at "
                                  "a usual turn",
        },
        "steps": {
            "base_week_ended_2026-10-03_advance": n0(c["base"]),
            "turns": "50",
            "turns_from": "April 2014", "turns_to": "July 2026",
        },
        "default_path": {"national_rate": n0(c["national"]),
                         "seasonal_step": n0(K.round_to(c["L"]["rivals"][[k for k in c["L"]["rivals"] if k.startswith("R0 ")][0]], 1000))},
        "precision": {"one_standard_error_claims": "%d" % round(c["pr"]["se_call"])},
        "ask_a_workers_by_region_and_period": {
            r: {p: n0(c["a"][(r, p)]) for p, _, _ in N.PERIODS} for r in K.REGIONS},
        "ask_a_totals": {p: n0(sum(c["a"][(r, p)] for r in K.REGIONS)) for p, _, _ in N.PERIODS},
        "ask_b_change_pct_by_group": {I.G[k]: pct1(c["b"][k]) for k in I.G},
        "ask_b_claims_jul_sep": {I.G[k]: {"2025": n0(c["b_tot"][2025][k]), "2026": n0(c["b_tot"][2026][k])}
                                 for k in I.G},
        "ask_b_all_groups": {"2025": n0(sum(c["b_tot"][2025].values())), "2026": n0(sum(c["b_tot"][2026].values())),
                             "change_pct": pct1((sum(c["b_tot"][2026].values()) / sum(c["b_tot"][2025].values()) - 1)
                                                * 100.0)},
    }


# ---------------------------------------------------------------------------------------------------- chart
def chart_png(c):
    plt.rcParams.update({"font.family": "Carlito", "font.size": 9.0, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                         "xtick.color": INK2, "ytick.color": INK2})
    fig, ax = plt.subplots(figsize=(6.9, 2.75), dpi=180)
    fig.patch.set_facecolor(PAPER)
    ds = [d for d, _ in c["chart"]]
    ys = [v for _, v in c["chart"]]
    xs = list(range(len(ds)))
    ax.plot(xs, ys, color=SERIES_C, linewidth=1.7, marker="o", markersize=2.8, zorder=3, label="Initial claims")
    xc = len(ds)
    ax.plot([xs[-1], xc], [ys[-1], c["call"]], color=CALL_C, linewidth=1.3, linestyle=(0, (3, 2)), zorder=3)
    ax.scatter([xc], [c["call"]], s=34, color=PAPER, edgecolor=CALL_C, linewidth=1.6, zorder=4,
               label="Our call, week ended 10 Oct")
    ax.annotate("%s (call)" % n0(c["call"]), (xc, c["call"]), xytext=(-9, 5), textcoords="offset points",
                fontsize=8.6, color=INK, ha="right")
    ax.annotate("%s" % n0(ys[-1]), (xs[-1], ys[-1]), xytext=(-5, -12), textcoords="offset points", fontsize=8.0,
                color=INK2, ha="right")
    ticks = [k for k, d in enumerate(ds) if K.saturday(d).day <= 7]
    labs = [K.saturday(ds[k]).strftime("%-d %b") for k in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labs)
    ax.set_xlim(-0.6, xc + 0.8)
    ax.set_ylim(9000, 17000)
    ax.set_yticks(range(9000, 17001, 2000))
    ax.set_yticklabels([n0(v) for v in range(9000, 17001, 2000)])
    ax.yaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
    ax.set_xlabel("Claims week ended", fontsize=8.4)
    ax.set_ylabel("Initial claims", fontsize=8.4)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    ax.legend(frameon=False, fontsize=8.2, loc="upper left")
    ax.set_title("Claims jump in the first week of October as the third quarter's refused claimants file again",
                 fontsize=9.4, color=INK, loc="left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=PAPER, metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


# ---------------------------------------------------------------------------------------------------- the preview
def write_docx(path, c, png):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt, RGBColor

    cm = c["cm"]
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin, sec.bottom_margin = Cm(1.8), Cm(1.6)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    st.paragraph_format.space_after = Pt(6)

    def para(text="", bold=False, size=None, color=None, after=None, keep=False, align=None):
        p = doc.add_paragraph()
        if text:
            r = p.add_run(text)
            r.bold = bold
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = RGBColor.from_string(color)
        if after is not None:
            p.paragraph_format.space_after = Pt(after)
        if keep:
            p.paragraph_format.keep_with_next = True
        if align:
            p.alignment = align
        return p

    para("Rothwell Bank  |  Economics  |  Initial claims preview  |  Thursday 8 October 2026", size=8.5,
         color="5D6875", after=10)
    para("Initial claims, week ended 10 October: about %s" % n0(c["call"]), bold=True, size=15, color="1F4E79", after=8)
    para("We expect the Unemployment Insurance Board to report about %s initial claims for the claims week ended "
         "10 October 2026 when it publishes the advance count next Thursday, 15 October, up from %s in the week ended "
         "3 October." % (n0(c["call"]), n0(c["base"])), size=10.5, after=8)
    para("The week ended 10 October is the first claims week of the fourth quarter, the first in which claimants "
         "refused in July to September for want of base-period earnings can file again. How many of them do differs "
         "a lot from region to region. Over the past 50 quarter turns about one refused claimant in four has filed "
         "again in the first week in Western and about three in ten in Coastal and Island, where most of the refused "
         "are seasonal hotel and building workers whose last season now counts, against fewer than one in ten in the "
         "other five regions. This quarter's refusals sit where claimants come back: the third quarter left %s "
         "monetarily ineligible determinations, about one and a half times a normal quarter, and %s per cent of them "
         "were in Western, Coastal and Island, against about a fifth at a usual quarter turn." % (
             n0(c["pool"]), "%.1f" % c["pool_wci_pct"]))
    para("Taking each region's refused claimants at its own rate, we put the claims filed again at %s to %s, about "
         "nine tenths of them in Western, Coastal and Island, on top of %s to %s for the rest of the week. The national "
         "refusals taken at the national rate would put the week near %s, and a seasonal reading of past October first "
         "weeks lower still, because neither allows for where this quarter's refusals sit." % (
             n0(c["refile_lo"]), n0(c["refile_hi"]), n0(c["without_lo"]), n0(c["without_hi"]), n0(c["national"])),
         after=6, keep=True)
    pic = doc.add_paragraph()
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.add_run().add_picture(io.BytesIO(png), width=Cm(16.4))
    pic.paragraph_format.space_after = Pt(1)
    pic.paragraph_format.keep_with_next = True
    para("National initial claims by claims week, not seasonally adjusted; the week ended 3 October at its advance "
         "count. Initial claims are new and additional claims as the board counts them (technical notes, section 2.2). "
         "Source: Unemployment Insurance Board weekly claims and program statistics; Rothwell Bank Economics.",
         size=8, color="5D6875", after=9)
    para("Layoffs already notified to the board for the rest of the year, by region, and the third quarter's change "
         "in claims by industry are in the attached workbook. %s" % c["industry_sentence"], after=10)
    para("Stacey Baxter", bold=True, after=0)
    para("Senior Economist, Rothwell Bank", size=9, color="5D6875", after=14)
    para("This note is prepared by Rothwell Bank Economics for the bank's clients. It is not investment advice.",
         size=7.5, color="5D6875", after=0)
    doc.core_properties.title = "Initial claims preview, week ended 10 October 2026"
    doc.save(path)
    return PP.normalize_docx(path, K.PEOPLE["economist"], K.PEOPLE["economist"], "2026-10-08T01:12:00Z",
                             "2026-10-08T03:51:00Z", revision=6, total_time=118, seed="task146/preview",
                             title="Initial claims preview, week ended 10 October 2026", company=K.BANK)


def write_xlsx(path, c):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Call"
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DCE6F0")
    thin = Side(style="thin", color="A6A6A6")
    ws["A1"] = "Initial claims preview, claims week ended 10 October 2026"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Rothwell Bank Economics, 8 October 2026"
    rows = [("Initial claims, claims week ended 10 October 2026 (advance count, released 15 October 2026)", c["call"]),
            ("Initial claims, claims week ended 3 October 2026 (advance count)", c["base"])]
    for i, (k, v) in enumerate(rows, 4):
        ws.cell(row=i, column=1, value=k)
        x = ws.cell(row=i, column=2, value=v)
        x.number_format = "#,##0"
    ws["B4"].font = bold
    work = [("How the call is built", None, None),
            ("Monetarily ineligible determinations, claims weeks of July to September 2026", c["pool"], "#,##0"),
            ("  of which Western, Coastal and Island (%)", c["pool_wci_pct"], "0.0"),
            ("Claims expected to be filed again in the week, low", c["refile_lo"], "#,##0"),
            ("Claims expected to be filed again in the week, high", c["refile_hi"], "#,##0"),
            ("The rest of the week, low", c["without_lo"], "#,##0"),
            ("The rest of the week, high", c["without_hi"], "#,##0")]
    for i, (k, v, f) in enumerate(work, 7):
        x = ws.cell(row=i, column=1, value=k)
        if v is None:
            x.font = bold
            continue
        y = ws.cell(row=i, column=2, value=v)
        y.number_format = f
    ws.cell(row=15, column=1, value="Each region's July to September determinations at the share its own first claims "
                                    "weeks of a quarter have filed again since 2014; about four fifths of the claims "
                                    "filed again are in Western, Coastal and Island.")
    ws.column_dimensions["A"].width = 84
    ws.column_dimensions["B"].width = 12
    # notified layoffs
    ws = wb.create_sheet("Layoff notices")
    ws["A1"] = "Workers to be laid off under layoff notices given to the board, by region of the site and month of the " \
               "first layoff"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Notices in Employer Services' register and on the Employer Portal at 7 October 2026; amended notices " \
               "in place of the notices they replace, withdrawn notices excluded."
    hdr = ["Region", "11 to 31 Oct 2026", "Nov 2026", "Dec 2026"]
    for j, h in enumerate(hdr, 1):
        x = ws.cell(row=4, column=j, value=h)
        x.font = bold
        x.fill = head
        x.alignment = Alignment(horizontal="left" if j == 1 else "right")
    for i, r in enumerate(K.REGIONS, 5):
        ws.cell(row=i, column=1, value=r)
        for j, (p, _, _) in enumerate(N.PERIODS, 2):
            x = ws.cell(row=i, column=j, value=c["a"][(r, p)])
            x.number_format = "#,##0"
    tr = 5 + len(K.REGIONS)
    ws.cell(row=tr, column=1, value="All regions").font = bold
    for j, (p, _, _) in enumerate(N.PERIODS, 2):
        x = ws.cell(row=tr, column=j, value=sum(c["a"][(r, p)] for r in K.REGIONS))
        x.number_format = "#,##0"
        x.font = bold
        x.border = Border(top=thin)
    ws.cell(row=tr, column=1).border = Border(top=thin)
    ws.column_dimensions["A"].width = 16
    for col in "BCD":
        ws.column_dimensions[col].width = 17
    ws.freeze_panes = "B5"
    ws.print_title_rows = "4:4"
    # industry
    ws = wb.create_sheet("Claims by industry")
    ws["A1"] = "Initial claims by industry group of the last employer, claims weeks of July to September"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "New and additional claims, claims weeks by the month of their Sunday; 2025 weeks coded on SIC 2006 " \
               "and mapped to the 2023 groups; the week ended 3 October 2026 at its advance count."
    hdr = ["Industry group", "Jul to Sep 2025", "Jul to Sep 2026", "Change (%)"]
    for j, h in enumerate(hdr, 1):
        x = ws.cell(row=4, column=j, value=h)
        x.font = bold
        x.fill = head
        x.alignment = Alignment(horizontal="left" if j == 1 else "right")
    for i, k in enumerate(I.G, 5):
        ws.cell(row=i, column=1, value=I.G[k])
        for j, v in ((2, c["b_tot"][2025][k]), (3, c["b_tot"][2026][k])):
            ws.cell(row=i, column=j, value=v).number_format = "#,##0"
        x = ws.cell(row=i, column=4, value=K.round_dp(c["b"][k], 1))
        x.number_format = "0.0"
    tr = 5 + len(I.G)
    t25, t26 = sum(c["b_tot"][2025].values()), sum(c["b_tot"][2026].values())
    ws.cell(row=tr, column=1, value="All groups").font = bold
    for j, v in ((2, t25), (3, t26)):
        x = ws.cell(row=tr, column=j, value=v)
        x.number_format = "#,##0"
        x.font = bold
    x = ws.cell(row=tr, column=4, value=K.round_dp((t26 / t25 - 1) * 100, 1))
    x.number_format = "0.0"
    x.font = bold
    for j in range(1, 5):
        ws.cell(row=tr, column=j).border = Border(top=thin)
    ws.column_dimensions["A"].width = 50
    for col in "BCD":
        ws.column_dimensions[col].width = 16
    ws.freeze_panes = "B5"
    ws.print_title_rows = "4:4"
    ws = wb.create_sheet("Notes")
    notes = [("As at", "Thursday 8 October 2026, after the board's 08:30 release (claims week ended 3 October)"),
             ("Initial claims", "New and additional claims as the board counts them (technical notes, section 2.2); "
                                "transitional claims are not initial claims"),
             ("The call", "The advance count for the claims week ended 10 October 2026, released Thursday 15 October; "
                          "to the nearest thousand"),
             ("Layoff notices", "Employer Services' register to 30 June 2026 and the Employer Portal export of 7 October "
                                "2026; a notice re-keyed onto the portal counted once, an amended notice in place of the "
                                "one it replaces, notices withdrawn in the case notes left out, reduced-hours notices "
                                "left out; workers in the region of the site; periods by the date of the first layoff"),
             ("Claims by industry", "The board's open data by industry; claims weeks in the month of their Sunday; "
                                    "2025 weeks on SIC 2006 divisions mapped to the 2023 groups through the Statistics "
                                    "Office's concordance; changes in per cent to one decimal"),
             ("Prepared by", "Tia Hewitt and Stacey Baxter, Rothwell Bank Economics")]
    for i, (k, v) in enumerate(notes, 1):
        ws.cell(row=i, column=1, value=k).font = bold
        x = ws.cell(row=i, column=2, value=v)
        x.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=i, column=1).alignment = Alignment(vertical="top")
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 96
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["analyst"], K.PEOPLE["economist"], "2026-10-07T20:05:41Z", "2026-10-08T03:49:12Z",
                       excel=True, company=K.BANK)


def main(target, golden, figures_path, Wd=None):
    os.makedirs(golden, exist_ok=True)
    c = compute(target)
    png = chart_png(c)
    stats = write_docx(os.path.join(golden, GOLD_DOC), c, png)
    write_xlsx(os.path.join(golden, GOLD_BOOK), c)
    with open(figures_path, "w", encoding="utf-8") as fh:
        json.dump(figures(c), fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    c["docx_stats"] = stats
    c["png"] = png
    return c
