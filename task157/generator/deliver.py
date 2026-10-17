"""The goldens, from the shipped files only: guarantee_fund_jan2027.xlsx (the fund, the drivers expected to qualify and
how they build up, the earlier winters' returns and the back-test, the 2025 and 2026 guarantees from main run to net
cost, the onboarding table, notes), guarantee_fund_jan2027.pptx (the fund slide and the two guarantees' steps from
main run to net cost), submission.md and generator/figures.json (every figure the write-up states, as it states it)."""
from __future__ import annotations

import io
import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import calc as C
import common as K
import docs as DOC
import postprocess as PP
import records as R

XLSX = "guarantee_fund_jan2027.xlsx"
PPTX = "guarantee_fund_jan2027.pptx"
AUTHOR = K.PEOPLE["supply"]
CREATED = "2027-01-03T23:58:00Z"
MODIFIED = "2027-01-04T04:47:00Z"
BAND_LABEL = ["1 to 9", "10 to 19", "20 to 29", "30 to 39", "40 to 59", "60 or more"]


def fmt(x, dp=0):
    v = K.round_half_up(x, dp)
    return format(v, ",.%df" % dp) if dp else format(int(v), ",")


def money(x):
    return "$" + fmt(x)


def about(x, step):
    return fmt(K.round_to(x, step))


# ------------------------------------------------------------------------------------------------- the figures
class X_:
    pass


def compute(target):
    X = X_()
    D = C.load(target)
    X.D = D
    X.F = C.fund(D)
    X.L = C.ladder(D)
    X.BT = C.backtest(D)
    X.A = C.ask_a(D)
    X.B = C.ask_b(D)
    F = X.F
    # the build-up by group
    S27, back27, jan27 = C.wave(D, 2027)
    dec27 = C.roster(D, 2027)
    rates = C.band_rates(D, 2026)
    b = C.band(C.dec_trips(D, 2027))
    X.bands = []
    for k in range(len(C.BANDS)):
        n = int((dec27 & ~back27 & (b == k)).sum())
        X.bands.append((BAND_LABEL[k], n, rates[k], n * rates[k]))
    X.waves = {}
    for y in (2024, 2025, 2026):
        S, bk, jn = C.wave(D, y)
        X.waves[y] = (int(S.sum()), int(bk.sum()), int(jn.sum()))
    X.waves[2027] = (int(S27.sum()), int(back27.sum()), None)
    camp = np.array([D.acc[d]["signup_channel"] == "campaign_winter26" for d in D.ids])
    X.back_campaign = int((back27 & camp).sum())
    X.S_campaign = int((S27 & camp).sum())
    fm = D.mi[(2026, 2)], D.mi[(2026, 3)]
    X.campaign_drove = int((camp & D.A[:, fm[0]:fm[1] + 1].any(1)).sum())
    q26 = C.qualified(D, 2026)
    X.q26 = int(q26.sum())
    X.new_rate = F.new26_from_pool / F.apn26
    import datetime as dt
    end26 = dt.datetime(2026, 1, 4, 23, 59, 59)
    appr = [a for a in D.apps if a["status"] in ("approved", "approval_lapsed") and a["decision_at_utc"] and
            C.central(a["decision_at_utc"]) <= end26 and
            (dt.date(2026, 1, 4) - C.central(a["decision_at_utc"]).date()).days <= 90]
    X.apn26_nodec = len([a for a in appr if not a["first_trip_at_utc"] or
                         C.central(a["first_trip_at_utc"]) >= dt.datetime(2026, 1, 1)])
    X.first_drove_jan = X.apn26_nodec - F.apn26
    # the sigma bands
    X.sigma_drivers = F.n_back * F.g_sigma * F.qJ
    gy = np.array([F.g_by_year[y] for y in (2024, 2025, 2026)])
    X.g_sd_years = float(np.std(gy, ddof=1))
    X.drivers_round = F.drivers_rounded
    X.fund = int(F.fund)
    return X


# ------------------------------------------------------------------------------------------------- the workbook
THIN = Side(style="thin", color="A9B4AD")
HEAD = PatternFill("solid", fgColor="E1E9E3")
TOT = PatternFill("solid", fgColor="F2F5F2")
MONEY = '"$"#,##0'


def _head(ws, row, cols, widths=None, height=None):
    for c, v in enumerate(cols, 1):
        cell = ws.cell(row=row, column=c, value=v)
        cell.font = Font(bold=True)
        cell.fill = HEAD
        cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left" if c == 1 else "right")
        cell.border = Border(bottom=THIN)
    if widths:
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w
    if height:
        ws.row_dimensions[row].height = height


def _width(ws, merge_to):
    last = openpyxl_col(merge_to)
    return sum((ws.column_dimensions[get_column_letter(c)].width or 8.43) for c in range(1, last + 1))


def openpyxl_col(letter):
    from openpyxl.utils import column_index_from_string
    return column_index_from_string(letter)


def _wrapped(ws, row, text, merge_to, bold=False):
    c = ws.cell(row=row, column=1, value=text)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if bold:
        c.font = Font(bold=True)
    ws.merge_cells("A%d:%s%d" % (row, merge_to, row))
    per_line = max(20.0, _width(ws, merge_to) * 1.05)
    ws.row_dimensions[row].height = 15.0 * (1 + int(len(text) / per_line))


def _title(ws, title, lines, merge_to):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=13)
    for k, t in enumerate(lines):
        _wrapped(ws, 2 + k, t, merge_to)


def _print(ws, landscape=False):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True


def write_xlsx(path, X):
    F = X.F
    wb = Workbook()
    ws = wb.active
    ws.title = "Fund"
    for c, w in enumerate([66, 12, 15, 14], 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    _title(ws, "Fund the winter guarantee account with %s at go-live" % money(X.fund), [
        "Expected total the 2027 winter guarantee pays: $350 to every driver expected to complete 40 trips between "
        "00:00 on Monday 4 January and 23:59 on Sunday 31 January 2027, Central time, accounts approved by Sunday 3 "
        "January (the 2027 terms). Data to the warehouse extract run of Sunday 3 January 2027.",
        "Treasury funds in $50,000 steps (Kathy Sherman, 30 December 2026). Each group's 2026 share is the share of "
        "the same group a year earlier that the 2026 guarantee paid (main run and late credits, less fraud "
        "recoveries)."], "D")
    for k, (lab, v, nf) in enumerate((("Fund at go-live, to the nearest $50,000", X.fund, MONEY),
                                      ("Drivers expected to qualify, to the nearest 100", X.drivers_round, "#,##0"))):
        a = ws.cell(row=5 + k, column=1, value=lab)
        a.font = Font(bold=True)
        c = ws.cell(row=5 + k, column=4, value=v)
        c.font = Font(bold=True, size=12)
        c.number_format = nf
    _head(ws, 8, ["Group", "Drivers", "Share that qualified, 2026", "Expected to qualify"], None, 30)
    r = 9
    for lab, n, rate, exp in X.bands:
        vals = ["December 2026 roster, %s trips in December, not last winter's drivers" % lab, n, rate, exp]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.number_format = {2: "#,##0", 3: "0.0%", 4: "#,##0"}.get(c, "General")
        r += 1
    rows = [
        ("Last winter's drivers back by 3 January", F.n_back, F.qD, F.back),
        ("Last winter's drivers due back 4 to 31 January (back by 3 January x %.3f)" % F.g, F.n_rest, F.qJ, F.rest),
        ("Drivers back after other breaks (as in January 2026)", None, None, F.other),
        ("Approved by 3 January, first trip not yet taken", F.apn27, X.new_rate, F.new),
    ]
    for lab, n, rate, exp in rows:
        vals = [lab, n, rate, exp]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.number_format = {2: "#,##0", 3: "0.0%", 4: "#,##0"}.get(c, "General")
        r += 1
    for c, v in enumerate(["All drivers expected to qualify", None, None, F.drivers], 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.font = Font(bold=True)
        cell.fill = TOT
        cell.border = Border(top=THIN)
        if c == 4:
            cell.number_format = "#,##0"
    r += 1
    for c, v in enumerate(["At $350 a driver", None, None, F.total], 1):
        cell = ws.cell(row=r, column=c, value=v)
        cell.font = Font(bold=True)
        if c == 4:
            cell.number_format = MONEY
    r += 2
    for t in [
        "Last winter's drivers: a completed trip from January to March 2026 and none from May to October 2026. %s of "
        "the %s are recruits of the winter 2026 campaign, %s of the %s back by 3 January." % (
            fmt(X.S_campaign), fmt(X.waves[2027][0]), fmt(X.back_campaign), fmt(F.n_back)),
        "Due back: each of the last three winters brought back more of its drivers in January than in November and "
        "December (Earlier winters sheet); the ratio over the three, %.3f, applied to the drivers back by 3 January." % F.g,
        "Approved, first trip not yet taken: the onboarding app's approvals within their 90 days with no first trip. "
        "2026 share: %d of the %d accounts approved in the 90 days to 4 January 2026 that had taken no trip by the end "
        "of that day were paid by the 2026 guarantee (the %d that first drove on 1 to 4 January are not among them)." % (
            F.new26_from_pool, F.apn26, X.first_drove_jan),
    ]:
        _wrapped(ws, r, t, "D")
        r += 1
    ws.freeze_panes = "A9"
    _print(ws)

    # earlier winters
    w2 = wb.create_sheet("Earlier winters")
    for c, w in enumerate([18, 16, 18, 16, 20], 1):
        w2.column_dimensions[get_column_letter(c)].width = w
    _title(w2, "Every winter on record brought back more of its drivers in January than in November and December", [
        "Each winter's drivers: a completed trip from January to March and none from May to October of the year before "
        "the guarantee. Back by December: a trip in November or December; back in January: none then, a trip in January. "
        "Old-platform months through the migration crosswalk."], "E")
    _head(w2, 4, ["Guarantee year", "Last winter's drivers", "Back in November or December", "Back in January",
                  "January returns per driver back by December"], None, 45)
    r = 5
    for y in (2024, 2025, 2026):
        S, bk, jn = X.waves[y]
        for c, v in enumerate([str(y), S, bk, jn, jn / bk], 1):
            cell = w2.cell(row=r, column=c, value=v)
            cell.number_format = "0.000" if c == 5 else "#,##0"
        r += 1
    sb = sum(X.waves[y][1] for y in (2024, 2025, 2026))
    sj = sum(X.waves[y][2] for y in (2024, 2025, 2026))
    for c, v in enumerate(["2024 to 2026", sum(X.waves[y][0] for y in (2024, 2025, 2026)), sb, sj, sj / sb], 1):
        cell = w2.cell(row=r, column=c, value=v)
        cell.font = Font(bold=True)
        cell.fill = TOT
        cell.number_format = "0.000" if c == 5 else "#,##0"
    r += 1
    for c, v in enumerate(["2027", X.waves[2027][0], X.waves[2027][1], None, None], 1):
        cell = w2.cell(row=r, column=c, value=v)
        cell.number_format = "#,##0"
    w2.cell(row=r, column=4, value="due 4 to 31 January")
    r += 2
    w2.cell(row=r, column=1, value="Checked at the earlier funding dates: January returns of the winter's drivers").font = \
        Font(bold=True)
    r += 1
    _head(w2, r, ["Funding date", "Predicted: ratio of the winters before, on those back by December",
                  "Predicted: last year's January share, on those still away", "Actual January returns"], None, 75)
    r += 1
    for y, label in ((2025, "5 January 2025"), (2026, "4 January 2026")):
        bt = X.BT[y]
        for c, v in enumerate([label, bt["development"], bt["pool"], bt["actual"]], 1):
            cell = w2.cell(row=r, column=c, value=v)
            cell.number_format = "#,##0"
        r += 1
    w2.freeze_panes = "A5"
    _print(w2)

    # the two guarantees
    w3 = wb.create_sheet("Guarantees 2025 and 2026")
    for c, w in enumerate([66, 17, 17], 1):
        w3.column_dimensions[get_column_letter(c)].width = w
    _title(w3, "The 2026 guarantee cost %s net and paid %s drivers" % (money(X.A[2026]["net"]),
                                                                       fmt(X.A[2026]["drivers"])), [
        "As the payout notes book it (Payments Operations, 20 March 2026): what the runs paid, less payouts the bank "
        "returned that were never paid out again and less what was recovered, each return and recovery booked to the "
        "guarantee of the payout it reverses. Drivers paid: people who kept a payment, one each however many accounts."],
        "C")
    _head(w3, 4, ["", "2025 guarantee", "2026 guarantee"])
    lines = [("Main run", "main", MONEY), ("Later runs (late credits)", "later", MONEY),
             ("Returned by the bank, never paid out again (never reached a driver)", "never", MONEY),
             ("Recovered (fraud and second accounts)", "recovered", MONEY), ("Net cost", "net", MONEY),
             ("Drivers paid", "drivers", "#,##0")]
    for i, (lab, key, nf) in enumerate(lines):
        w3.cell(row=5 + i, column=1, value=lab)
        for j, y in enumerate((2025, 2026)):
            v = X.A[y][key]
            if key in ("never", "recovered"):
                v = -v
            c = w3.cell(row=5 + i, column=2 + j, value=v)
            c.number_format = nf if key in ("main", "later", "net", "drivers") else '"$"#,##0;-"$"#,##0'
            if key in ("net", "drivers"):
                c.font = Font(bold=True)
        if key == "net":
            for j in range(3):
                w3.cell(row=5 + i, column=1 + j).border = Border(top=THIN)
    _wrapped(w3, 12, "The 2025 main run is read from the old payout report, in cents. A payout the bank returned and "
             "that the payments system sent again after the driver updated their payout details reached the driver; "
             "the events log shows each send.", "C")
    _print(w3)

    # onboarding
    w4 = wb.create_sheet("Onboarding Jun-Oct 2026")
    for c, w in enumerate([18, 16, 14, 18], 1):
        w4.column_dimensions[get_column_letter(c)].width = w
    _title(w4, "Onboarding pipeline by month of first application, June to October 2026", [
        "People, not applications (one screening candidate each), in the month of their first submission, Central time; "
        "approved on any of their applications; a first trip by the extract run of 3 January 2027 (Driver Onboarding's "
        "counting notes, 5 August 2026)."], "D")
    _head(w4, 4, ["Month", "People who applied", "Approved", "First trip by 3 January 2027"], None, 30)
    for i, m in enumerate(range(6, 11)):
        v = X.B[m]
        w4.cell(row=5 + i, column=1, value="%s 2026" % K.MONTH_NAMES[m])
        for j, key in enumerate(("applied", "approved", "first_trip")):
            w4.cell(row=5 + i, column=2 + j, value=v[key]).number_format = "#,##0"
    _wrapped(w4, 11, "The onboarding app's submitted time is the applicant's latest submission; the first submission is "
             "the screening vendor's order, placed when an application is first submitted.", "D")
    w4.freeze_panes = "A5"
    _print(w4)

    w5 = wb.create_sheet("Notes")
    w5.column_dimensions["A"].width = 22
    w5.column_dimensions["B"].width = 108
    notes = [
        ("Estimand", "Finance's email of 30 December 2026: the expected total the guarantee will pay for 4 to 31 January, "
                     "$350 for every driver expected to complete 40 trips, drivers not driving now included, to the "
                     "nearest $50,000; returns and recoveries left out."),
        ("Trips", "Completed trips by driver and month: the old platform's export to 14 July 2024 (legacy driver "
                  "numbers through the migration crosswalk) and the warehouse's monthly activity from 15 July 2024. "
                  "January 2027 holds 1 to 3 January."),
        ("Last year's qualifiers", "Accounts paid by the 2026 main run and the March 2026 late credits, less the "
                                   "payouts recovered for trips refunded as fraudulent: %s." % fmt(X.q26)),
        ("December roster", "Accounts with a completed trip in December 2026, last winter's drivers back by then "
                            "priced apart; each band at the share of December 2025's roster in the same band, without "
                            "that winter's returning drivers, that the 2026 guarantee paid."),
        ("Last winter's drivers", "Back by 3 January: priced at the share of 2026's back-by-December drivers that "
                                  "the 2026 guarantee paid. Due back in the window: at the share of January 2026's "
                                  "returning drivers that it paid."),
        ("Other returns", "Drivers with no trip in December, not last winter's drivers, who came back and qualified "
                          "in January 2026: %d, carried as a count." % int(round(X.F.other))),
        ("New drivers", "Only accounts approved by Sunday 3 January take part (the terms)."),
        ("Rounding", "The expected total to the nearest $50,000; drivers to the nearest 100."),
    ]
    _head(w5, 1, ["Item", "Note"])
    for i, (k, v) in enumerate(notes, 2):
        w5.cell(row=i, column=1, value=k).font = Font(bold=True)
        c = w5.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        w5.cell(row=i, column=1).alignment = Alignment(vertical="top")
        w5.row_dimensions[i].height = 15 * (1 + len(v) // 104)
    _print(w5, landscape=True)
    wb.save(path)
    PP.normalize_ooxml(path, AUTHOR, AUTHOR, CREATED, MODIFIED, excel=True, company=K.OPERATOR)


# ------------------------------------------------------------------------------------------------- the chart
INK, INK2, GRID, AXIS = "#16201b", "#4f5a54", "#e3e7e3", "#c4cbc6"
UP, DOWN, TOTAL = "#2f5d3a", "#c0563c", "#7d8a83"


def chart_png(X):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in ("/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf",
              "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"):
        font_manager.fontManager.addfont(f)
    plt.rcParams["font.family"] = "Carlito"
    plt.rcParams["svg.hashsalt"] = "task157"
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 4.9), dpi=150)
    fig.subplots_adjust(left=0.075, right=0.99, top=0.87, bottom=0.14, wspace=0.16)
    steps = ["Main run", "Later runs", "Never reached\na driver", "Recovered", "Net cost"]
    lo_all = min(X.A[y]["net"] for y in (2025, 2026))
    for ax, y in zip(axes, (2025, 2026)):
        a = X.A[y]
        vals = [a["main"], a["later"], -a["never"], -a["recovered"], a["net"]]
        level = 0.0
        bottoms, heights, cols = [], [], []
        for k, v in enumerate(vals):
            if k in (0, 4):
                bottoms.append(0.0)
                heights.append(v)
                cols.append(TOTAL if k == 4 else UP)
                level = v
            else:
                bottoms.append(level + min(v, 0))
                heights.append(abs(v))
                cols.append(UP if v > 0 else DOWN)
                level += v
        xs = np.arange(len(steps))
        ax.bar(xs, heights, bottom=bottoms, color=cols, width=0.62, zorder=3)
        run = [a["main"], a["main"] + a["later"], a["main"] + a["later"] - a["never"], a["net"]]
        for k in range(4):
            ax.plot([k + 0.31, k + 0.69], [run[k], run[k]], color=AXIS, lw=0.9, zorder=2)
        for k, v in enumerate(vals):
            top = bottoms[k] + heights[k]
            lab = money(v) if k in (0, 4) else ("+" if v > 0 else "-") + money(abs(v))
            ax.text(k, top + 0.06 * (a["main"] + a["later"] - a["net"]), lab, ha="center", va="bottom",
                    fontsize=10.5, color=INK,
                    fontweight="bold" if k == 4 else "normal")
        ax.set_xticks(xs)
        ax.set_xticklabels(steps, fontsize=10, color=INK2)
        ax.set_title("%d guarantee: %s drivers paid" % (y, fmt(a["drivers"])), fontsize=12.5, color=INK, loc="left")
        span = a["main"] + a["later"] - a["net"]
        ax.set_ylim(a["net"] - 3.2 * span, a["main"] + a["later"] + 1.1 * span)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: "$" + format(int(v), ",")))
        ax.grid(axis="y", color=GRID, lw=0.7, zorder=1)
        for sp in ("top", "right", "left"):
            ax.spines[sp].set_visible(False)
        ax.spines["bottom"].set_color(AXIS)
        ax.tick_params(axis="y", labelsize=9.5, colors=INK2, length=0)
        ax.tick_params(axis="x", length=0)
    axes[0].set_ylabel("US dollars (axis starts above zero)", fontsize=10.5, color=INK2)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


# ------------------------------------------------------------------------------------------------- the deck
def write_pptx(path, X, png):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Inches, Pt

    ink = RGBColor(0x16, 0x20, 0x1B)
    grey = RGBColor(0x4F, 0x5A, 0x54)
    green = RGBColor(0x2F, 0x5D, 0x3A)
    pale = RGBColor(0xEE, 0xF2, 0xEE)
    white = RGBColor(0xFF, 0xFF, 0xFF)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    F = X.F

    def text(sl, x, y, w, h, paras, align=None):
        tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for k, (t, size, bold, col) in enumerate(paras):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = t
            p.font.size, p.font.bold = Pt(size), bold
            p.font.color.rgb = col
            p.font.name = "Calibri"
            if align is not None:
                p.alignment = align
            if k:
                p.space_before = Pt(8)
        return tb

    def footer(sl, n):
        text(sl, 0.6, 7.02, 10.0, 0.3, [("Larch Rides Driver Supply  |  Winter guarantee 2027 funding  |  "
                                         "3 January 2027", 9.5, False, grey)])
        text(sl, 11.9, 7.02, 0.8, 0.3, [(str(n), 9.5, False, grey)], align=PP_ALIGN.RIGHT)

    # slide 1: the fund
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    text(s1, 0.6, 0.4, 12.1, 1.4, [
        ("Fund the winter guarantee account with %s at go-live" % money(X.fund), 32, True, ink),
        ("%s drivers expected to complete 40 trips between 4 and 31 January 2027, at $350 each" % fmt(X.drivers_round),
         18, False, grey)])
    parts = [("December 2026 roster", F.nonwave), ("Last winter's drivers back by 3 January", F.back),
             ("Last winter's drivers due back 4 to 31 January", F.rest), ("Other returning and new drivers",
                                                                          F.other + F.new)]
    shown = [int(K.round_to(v, 10)) for _, v in parts]
    shown[0] += X.drivers_round - sum(shown)
    rows = len(parts) + 2
    shape = s1.shapes.add_table(rows, 2, Inches(0.6), Inches(2.1), Inches(5.6), Inches(0.42 * rows))
    tbl = shape.table
    tbl.columns[0].width, tbl.columns[1].width = Inches(4.2), Inches(1.4)
    cells = [("Expected to qualify", "Drivers")] + [(lab, fmt(v)) for (lab, _), v in zip(parts, shown)] + \
            [("All drivers", fmt(X.drivers_round))]
    for i, (a_, b_) in enumerate(cells):
        for j, v in enumerate((a_, b_)):
            c = tbl.cell(i, j)
            c.text = v
            c.fill.solid()
            c.fill.fore_color.rgb = green if i == 0 else (pale if i == rows - 1 else white)
            p = c.text_frame.paragraphs[0]
            p.font.size = Pt(14)
            p.font.name = "Calibri"
            p.font.bold = i in (0, rows - 1)
            p.font.color.rgb = white if i == 0 else ink
            if j == 1:
                p.alignment = PP_ALIGN.RIGHT
    paras = [
        ("Why it is above last January", 17, True, ink),
        ("Last winter's recruitment campaign put about %s new drivers on the road in February and March 2026. Most "
         "stopped driving in March or April and took no trip from May to October." % fmt(K.round_to(X.campaign_drove,
                                                                                                  100)),
         14, False, ink),
        ("They are coming back with the winter: about %s of last winter's drivers were back on the road by 3 January. "
         "In each of the last three winters January brought back about %s drivers for every one back in November and "
         "December, so about %s more are due inside the window." % (
             about(F.n_back, 100), "%.1f" % K.round_half_up(F.g, 1), about(F.n_rest, 100)), 14, False, ink),
        ("Priced at last January's shares, last winter's drivers account for about %s of the %s." % (
            about(F.back + F.rest, 100), fmt(X.drivers_round)), 14, False, ink),
    ]
    text(s1, 6.75, 2.0, 6.0, 4.4, paras)
    text(s1, 0.6, 6.45, 12.1, 0.5, [(
        "Expected total at $350 a qualifying driver, to the nearest $50,000 (finance, 30 December 2026). Returns and "
        "recoveries come back to the account and are left out. Data to the extract run of 3 January 2027. Workings: "
        "%s." % XLSX, 10.5, False, grey)])
    footer(s1, 1)

    # slide 2: the two guarantees
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    text(s2, 0.6, 0.3, 12.1, 1.2, [
        ("The 2026 guarantee cost %s after returns and recoveries" % money(X.A[2026]["net"]), 26, True, ink),
        ("Each guarantee from its main run to its net cost, as Payments Operations books it: returns never paid out "
         "again and recoveries booked to the guarantee of the payout they reverse.", 14, False, grey)])
    s2.shapes.add_picture(io.BytesIO(png), Inches(0.55), Inches(1.55), width=Inches(12.2))
    text(s2, 0.6, 6.5, 12.1, 0.45, [(
        "Main runs of 14 February 2025 and 13 February 2026, the adjustment runs to June 2026, the bank's ACH return "
        "report and the payout events log. Drivers paid: people who kept a payment.", 10.5, False, grey)])
    footer(s2, 2)
    buf = io.BytesIO()
    prs.save(buf)
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())
    PP.normalize_ooxml(path, AUTHOR, AUTHOR, CREATED, MODIFIED, title="Winter guarantee 2027 funding",
                       company=K.OPERATOR)


# ------------------------------------------------------------------------------------------------- the write-up
def submission(X):
    F, A, B = X.F, X.A, X.B
    bt = X.BT
    L = []
    a = L.append
    a("## Tags")
    a("")
    a("**Domain:** Product Analytics (retention, cohort and lifetime value modeling: a ride-hail platform's supply-side "
      "driver cohorts, last winter's recruits read as a returning cohort whose resurrection is under way at the "
      "forecast date).")
    a("**Analytical objective:** Forecasting & Predictive Modeling.")
    a("")
    a("## 1. Final Recommendation")
    a("")
    a("**Fund the winter guarantee account with %s at go-live on Monday 4 January: we expect %s drivers to complete 40 "
      "trips by Sunday 31 January.**" % (money(X.fund), fmt(X.drivers_round)))
    a("About %s of last winter's drivers, most of them recruits of the winter 2026 campaign who stopped driving in "
      "March and April, were back on the road by 3 January, and every earlier winter brought back about %s drivers in "
      "January for each one back in November and December, so about %s more are due inside the window and last "
      "winter's drivers make up about %s of the %s. Not December's roster with the drivers away priced at last "
      "January's return rate, which treats last winter's drivers as a pool whose return rate moves with who sits in it: "
      "on last winter's drivers alone that rate over-predicted January 2026's returns, because the 2025 rental "
      "programme's drivers sat in the pool and never came back. Not one ratio of "
      "January to November and December returns over every driver back after a break, which mixes in occasional "
      "drivers who keep no seasonal timing. Not the drivers already back priced by their December trips, which "
      "under-predicted last year's back-by-December drivers' qualification." % (
          about(F.n_back, 100), "%.1f" % K.round_half_up(F.g, 1), about(F.n_rest, 100), about(F.back + F.rest, 100),
          fmt(X.drivers_round)))
    a("")
    a("## 2. Critical Components")
    a("")
    a("1. About **%s** of last winter's drivers (a trip from January to March 2026, none from May to October 2026) "
      "were back on the road by 3 January 2027." % about(F.n_back, 100))
    a("2. Each of the 2024, 2025 and 2026 winters brought back about **%s** drivers in January for every one back in "
      "November and December." % ("%.1f" % K.round_half_up(F.g, 1)))
    a("3. About **%s** more of last winter's drivers are due back inside the window." % about(F.n_rest, 100))
    a("4. Last winter's drivers make up about **%s** of the %s drivers expected to qualify." % (
        about(F.back + F.rest, 100), fmt(X.drivers_round)))
    a("")
    a("## 3. Step-by-Step Solution")
    a("")
    a("1. Stacked %s (legacy driver numbers through %s) with %s into completed trips by driver and month; last year's "
      "qualifiers are the accounts paid in %s and by the late credits in %s, less the fraud recoveries." % (
          R.F_LEGACY, R.F_CROSSWALK, R.F_ACTIVITY, R.F_RUN26, R.F_ADJ))
    a("2. Took each winter's drivers as those with a trip from January to March and none from May to October: %s of "
      "last winter's had a trip in November or December 2026." % fmt(F.n_back))
    a("3. Over the 2024, 2025 and 2026 winters, January returns ran %.3f times the November and December returns; at "
      "the 2025 and 2026 funding dates this ratio put January's returns within %d per cent, where the previous "
      "January's share on the drivers still away missed by %d and %d per cent." % (
          F.g, max(int(np.ceil(abs(bt[y]["development"] / bt[y]["actual"] - 1) * 100)) for y in (2025, 2026)),
          int(K.round_half_up(abs(bt[2025]["pool"] / bt[2025]["actual"] - 1) * 100)),
          int(K.round_half_up(abs(bt[2026]["pool"] / bt[2026]["actual"] - 1) * 100))))
    a("4. Priced December 2026's roster without last winter's drivers at the share of each December-trip band of "
      "December 2025's roster that the 2026 guarantee paid (about %s drivers), last winter's drivers back by 3 January "
      "at the %d per cent of 2026's back-by-December drivers it paid, and the %s due back at the %d per cent of January "
      "2026's returners it paid." % (about(F.nonwave, 100), int(K.round_half_up(100 * F.qD)), fmt(F.n_rest),
                                     int(K.round_half_up(100 * F.qJ))))
    a("5. Added the %d drivers who came back after other breaks and qualified in January 2026, and the %d accounts "
      "approved in the 90 days to 3 January without a first trip (%s; an approval lapses after 90 days) at the %d of "
      "%d accounts approved in the 90 days to 4 January 2026 with no first trip by the end of that day that the 2026 "
      "guarantee paid (the %d that first drove on 1 to 4 January are not among them): %s drivers expected to qualify, "
      "%s at $350 each to the nearest $50,000 (%s)." % (
          int(round(F.other)), F.apn27, R.F_APPS, F.new26_from_pool, F.apn26, X.first_drove_jan, fmt(X.drivers_round),
          money(X.fund), DOC.F_EMAIL))
    a("6. For each guarantee, a returned payout that %s shows sent again and settled reached its driver; only payouts "
      "whose last event is a return never did. Recoveries go to the guarantee of the payout they reverse, the 2025 "
      "run read in cents and people through merged_into in %s (%s)." % (R.F_EVENTS, R.F_ACCOUNTS, DOC.F_PAYNOTES))
    a("7. For the pipeline, counted people by screening candidate in %s, each in the month (Central time) of their "
      "first order, which is placed at first submission while the app's submitted time is the latest resubmission "
      "(%s)." % (R.F_ORDERS, DOC.F_ONBNOTES))
    a("")
    a("## 4. Deliverable Answers")
    a("")
    a("### %s" % XLSX)
    a("")
    a("1. Fund at go-live, to the nearest $50,000: %s." % money(X.fund))
    a("2. Drivers expected to qualify, to the nearest 100: %s." % fmt(X.drivers_round))
    for i, y in enumerate((2025, 2026), 3):
        a("%d. %d guarantee: %s never reached a driver; net cost %s; %s drivers paid." % (
            i, y, money(A[y]["never"]), money(A[y]["net"]), fmt(A[y]["drivers"])))
    a("5. Onboarding pipeline by month of first application, whole people:")
    for m in range(6, 11):
        v = B[m]
        a("   - %s 2026: %s applied, %s approved, %s with a first trip by 3 January 2027" % (
            K.MONTH_NAMES[m], fmt(v["applied"]), fmt(v["approved"]), fmt(v["first_trip"])))
    a("")
    a("### %s" % PPTX)
    a("")
    a("6. Slide 1 states the fund, %s at go-live, with the %s drivers expected to qualify." % (
        money(X.fund), fmt(X.drivers_round)))
    a("7. Slide 2 charts each guarantee from main run to net cost:")
    for y in (2025, 2026):
        v = A[y]
        a("   - %d: main run %s, later runs %s, never reached a driver %s, recovered %s, net cost %s" % (
            y, money(v["main"]), money(v["later"]), money(v["never"]), money(v["recovered"]), money(v["net"])))
    return "\n".join(L) + "\n"


def figures(X):
    F, A, B, bt = X.F, X.A, X.B, X.BT
    return {
        "call": {"fund": money(X.fund), "drivers": fmt(X.drivers_round)},
        "terms": {"amount": "$350", "trips": "40", "step": "$50,000", "driver_step": "100", "go_live_day": "4",
                  "window_last_day": "31", "asof_day": "3"},
        "components": {"back_by_asof": about(F.n_back, 100), "ratio": "%.1f" % K.round_half_up(F.g, 1),
                       "due_back": about(F.n_rest, 100), "wave_qualifiers": about(F.back + F.rest, 100)},
        "steps": {
            "back_count": fmt(F.n_back), "ratio_exact": "%.3f" % F.g,
            "backtest_within_pct": str(max(int(np.ceil(abs(bt[y]["development"] / bt[y]["actual"] - 1) * 100))
                                           for y in (2025, 2026))),
            "pool_miss_2025_pct": str(int(K.round_half_up(abs(bt[2025]["pool"] / bt[2025]["actual"] - 1) * 100))),
            "pool_miss_2026_pct": str(int(K.round_half_up(abs(bt[2026]["pool"] / bt[2026]["actual"] - 1) * 100))),
            "roster_part": about(F.nonwave, 100), "qD_pct": str(int(K.round_half_up(100 * F.qD))),
            "due_back_exact": fmt(F.n_rest), "qJ_pct": str(int(K.round_half_up(100 * F.qJ))),
            "other_returns": str(int(round(F.other))), "approved_not_started": str(F.apn27),
            "new_paid_2026": str(F.new26_from_pool), "approved_not_started_2026": str(F.apn26),
            "lapse_days": "90", "first_drove_jan_1_to_4": str(X.first_drove_jan),
        },
        "answers": {
            "fund": money(X.fund), "drivers": fmt(X.drivers_round),
            "ask_a": {str(y): {"never_reached": money(A[y]["never"]), "net_cost": money(A[y]["net"]),
                               "drivers_paid": fmt(A[y]["drivers"]), "main_run": money(A[y]["main"]),
                               "later_runs": money(A[y]["later"]), "recovered": money(A[y]["recovered"])}
                      for y in (2025, 2026)},
            "ask_b": {K.MONTH_NAMES[m]: {k: fmt(B[m][k]) for k in ("applied", "approved", "first_trip")}
                      for m in range(6, 11)},
        },
    }


def main(target, golden, fig_path, sub_path):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    write_xlsx(os.path.join(golden, XLSX), X)
    png = chart_png(X)
    write_pptx(os.path.join(golden, PPTX), X, png)
    with open(sub_path, "w", encoding="utf-8") as fh:
        fh.write(submission(X))
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(figures(X), fh, indent=2)
        fh.write("\n")
    return X
