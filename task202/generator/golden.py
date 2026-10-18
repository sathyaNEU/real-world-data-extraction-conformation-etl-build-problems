"""The two deliverables: the schedule workbook the Office files and the board paper the trustees read."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer

import docs
import params as P
import records as RC
import writeup as WU

XLSX = "relief_referral_ceilings_2027-28.xlsx"
PDF = "referral_ceiling_board_paper.pdf"
ANNEX = "claims_annex.xlsx"
PNG = "_award_distribution.png"


def schedule_workbook(path, fig):
    wb = Workbook()
    ws = wb.active
    ws.title = "Schedule"
    bold = Font(bold=True)
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="2F4B6E")
    thin = Side(style="thin", color="9AA3AE")
    ws["A1"] = "%s: referral ceiling schedule, 2027/28" % P.SCHEME
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Clause 9 ceiling at the reference household size: PHP %s" % "{:,}".format(fig["call"])
    ws["A2"].font = Font(bold=True, size=11)
    ws["A3"] = ("Prepared by %s, %s. Basis: claim returns for April 2026 to March 2027 and the "
                "partner claim portal for the same months." % (P.PEOPLE["assurance"][0], P.OFFICE))
    ws["A4"] = "Amounts in pesos. Shares of the band's own awards in those twelve months."
    for r in (3, 4):
        ws.cell(row=r, column=1).font = Font(italic=True, size=9)
    cols = ["Band", "Household size", "Scale factor (B.2)", "Referral ceiling (PHP)",
            "Referred share of awards (%)", "Referred share of award value (%)"]
    for j, c in enumerate(cols, start=1):
        cl = ws.cell(row=6, column=j, value=c)
        cl.font = head
        cl.fill = fill
        cl.alignment = Alignment(wrap_text=True, vertical="center")
    for i, b in enumerate(P.BANDS, start=7):
        d = fig["bands"][str(b)]
        vals = [RC.legacy_band(b), P.BAND_LABEL[b], d["factor"], d["ceiling"],
                d["referred_share"], d["referred_value_share"]]
        for j, v in enumerate(vals, start=1):
            cl = ws.cell(row=i, column=j, value=v)
            cl.border = Border(bottom=thin)
            if j == 3:
                cl.number_format = "0.000"
            if j == 4:
                cl.number_format = "#,##0"
            if j in (5, 6):
                cl.number_format = "0.0"
        if b == P.REF_BAND:
            for j in range(1, 7):
                ws.cell(row=i, column=j).font = bold
    r = 7 + len(P.BANDS)
    ws.cell(row=r, column=1, value="All bands").font = bold
    ws.cell(row=r, column=4, value="").font = bold
    c = ws.cell(row=r, column=5, value=fig["referred_share"])
    c.number_format = "0.0"
    c.font = bold
    c = ws.cell(row=r, column=6, value=fig["referred_value_share"])
    c.number_format = "0.0"
    c.font = bold
    for j, w in enumerate([9, 17, 17, 18, 17, 20], start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(row=7, column=1)

    bs = wb.create_sheet("Basis")
    rows = [
        ("Clause 9 quantity", "lowest amount in Schedule E referring at or below 6.0 per cent of the "
                              "scheme's awards"),
        ("Window", "the twelve months to 31 March 2027, award counted in the month it was paid"),
        ("Awards in the window", fig["awards"]),
        ("Partner-band cells", fig["cells"]),
        ("Partners accredited in the window", fig["partners"]),
        ("Portal award rows in the window", fig["portal_window_rows"]),
        ("Award shape, coefficient of variation", fig["cv"]),
        ("Referred share at PHP %s" % "{:,}".format(fig["call"]), fig["share_pct"]),
        ("Referred share at PHP %s" % "{:,}".format(fig["call_down"]), fig["share_down_pct"]),
        ("Referred awards at the schedule", fig["referred_awards"]),
        ("Rounding", "each band ceiling rounded up to the nearest PHP 100 under B.3"),
        ("Returns superseded", "REVISED returns taken for the two reopened months, Nov-2026 and "
                               "Feb-2027"),
    ]
    bs["A1"] = "Basis of the schedule"
    bs["A1"].font = Font(bold=True, size=12)
    for i, (k, v) in enumerate(rows, start=3):
        bs.cell(row=i, column=1, value=k).font = Font(bold=True)
        cl = bs.cell(row=i, column=2, value=v)
        if isinstance(v, float):
            cl.number_format = "0.00" if abs(v) < 100 else "#,##0.0"
    bs.column_dimensions["A"].width = 38
    bs.column_dimensions["B"].width = 74
    wb.properties.creator = P.PEOPLE["assurance"][0]
    wb.properties.lastModifiedBy = P.PEOPLE["assurance"][0]
    wb.properties.title = "%s referral ceiling schedule 2027/28" % P.SCHEME_SHORT
    wb.properties.created = dt.datetime(2027, 5, 21, 16, 5)
    wb.properties.modified = dt.datetime(2027, 5, 21, 16, 5)
    wb.save(path)
    docs.finalise_xlsx(path, (2027, 5, 21, 16, 5, 0))


def annex_workbook(path, fig):
    """The closed-period annex the audit committee asked for beside the schedule."""
    a = fig["asks"]
    wb = Workbook()
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor="2F4B6E")
    bold = Font(bold=True)
    thin = Side(style="thin", color="9AA3AE")
    money = "#,##0"

    ws = wb.active
    ws.title = "Payments and holds"
    ws["A1"] = "%s: claims assurance annex, closed claim months" % P.SCHEME
    ws["A1"].font = Font(bold=True, size=13)
    tot_held = sum(a["held"][q] for q in a["quarters"])
    tot_uns = sum(a["unsettled"][q] for q in a["quarters"])
    ws["A2"] = ("The check held PHP %s back over the eighteen closed claim months, and PHP %s of "
                "what partners claimed had not been settled when the archive was cut."
                % ("{:,}".format(tot_held), "{:,}".format(tot_uns)))
    ws["A2"].font = Font(bold=True, size=10)
    ws["A3"] = ("Claim months July 2024 to December 2025, the period the pre-payment claim check "
                "covered. Scheme quarters, July to June. Amounts in pesos.")
    ws["A4"] = ("Prepared by %s, %s, for the audit committee. Claims extract of %s."
                % (P.PEOPLE["assurance"][0], P.OFFICE, P.EXTRACT_DATE.strftime("%d %B %Y")))
    for r in (3, 4):
        ws.cell(row=r, column=1).font = Font(italic=True, size=9)
    cols = ["Scheme quarter", "Claimed on returns", "Passed by the check", "Held by the check",
            "Recovered in the runs", "Not settled in the archive", "Settled by the Treasury",
            "Payment instructions"]
    for j, c in enumerate(cols, start=1):
        cl = ws.cell(row=6, column=j, value=c)
        cl.font = head
        cl.fill = fill
        cl.alignment = Alignment(wrap_text=True, vertical="center")
    tot = [0, 0, 0, 0, 0, 0, 0]
    for i, q in enumerate(a["quarters"], start=7):
        vals = [a["claimed"][q], a["passed"][q], a["held"][q], a["recovered"][q],
                a["unsettled"][q], a["transferred"][q], a["instructions"][q]]
        ws.cell(row=i, column=1, value=q).border = Border(bottom=thin)
        for j, v in enumerate(vals, start=2):
            cl = ws.cell(row=i, column=j, value=v)
            cl.number_format = money
            cl.border = Border(bottom=thin)
            tot[j - 2] += v
    r = 7 + len(a["quarters"])
    ws.cell(row=r, column=1, value="All six quarters").font = bold
    for j, v in enumerate(tot, start=2):
        cl = ws.cell(row=r, column=j, value=v)
        cl.number_format = money
        cl.font = bold
    notes = [
        "Claimed less held, recovered and not yet settled equals settled in every quarter, and "
        "claimed less held equals passed.",
        "A payment instruction settles a partner's claim month. Where the first half's release was "
        "held for a mandate re-validation the Treasury settled both halves on one instruction, and "
        "the archive is an instruction extract, so that instruction's amounts stand on each of the "
        "two run lines it covers: those lines together come to more than the partner claimed for "
        "the month, which cannot be settled, so they are one instruction and one amount.",
        "Each side is keyed to the claim month: the month a return was filed for, and for a payment "
        "run line the claim month it covers.",
        "The %d partner claim-months with no run line in the extract were released in a run dated "
        "after the archive's cut-off of 31 January 2026 and are shown as not settled; the manifest "
        "records the cut-off." % (a["check_months"] - a["run_months"]),
        "A recovery is applied against the partner's next transfer, so it falls in the quarter after "
        "the one the negative claim line sits in.",
    ]
    for i, t in enumerate(notes):
        cl = ws.cell(row=r + 2 + i, column=1, value=t)
        cl.font = Font(italic=True, size=9)
    for j, w in enumerate([18, 19, 19, 18, 19, 21, 21, 18], start=1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(row=7, column=1)
    ws.print_area = "A1:H%d" % (r + 2 + len(notes))
    ws.print_title_rows = "6:6"

    hs = wb.create_sheet("Hold reasons")
    hs["A1"] = "Partner claim-months the check held an amount back in, by reason recorded"
    hs["A1"].font = Font(bold=True, size=12)
    hs["A2"] = "Claim months July 2024 to December 2025."
    hs["A2"].font = Font(italic=True, size=9)
    for j, c in enumerate(["Reason recorded", "Partner claim-months"], start=1):
        cl = hs.cell(row=4, column=j, value=c)
        cl.font = head
        cl.fill = fill
    n = 0
    for i, k in enumerate(WU.REASONS, start=5):
        hs.cell(row=i, column=1, value=k).border = Border(bottom=thin)
        cl = hs.cell(row=i, column=2, value=a["holds_by_reason"][k])
        cl.number_format = "#,##0"
        cl.border = Border(bottom=thin)
        n += a["holds_by_reason"][k]
    hs.cell(row=5 + len(WU.REASONS), column=1, value="All reasons").font = bold
    cl = hs.cell(row=5 + len(WU.REASONS), column=2, value=n)
    cl.font = bold
    cl.number_format = "#,##0"
    hs.column_dimensions["A"].width = 32
    hs.column_dimensions["B"].width = 22

    bs = wb.create_sheet("Basis")
    rows = [
        ("As at", P.EXTRACT_DATE.isoformat()),
        ("Period", "claim months July 2024 to December 2025; the pre-payment check was withdrawn "
                   "on 1 January 2026 and returns are paid in full and reviewed after payment"),
        ("Quarters", "the scheme's own quarters, July to September and so on; the folder's export "
                     "manifest gives each return workbook's fiscal year as July to June"),
        ("Basis of each side", "the claim month the return was filed for, and for a run line the "
                               "claim month it covers"),
        ("Check register rows read", a["check_rows"]),
        ("Partner claim-months checked", a["check_months"]),
        ("Partner claim-months with run lines", a["run_months"]),
        ("Claim-months settled on one payment instruction", a["instruction_repeats"]),
        ("Holds in the period", n),
        ("Note on the register", "a partner claim-month checked twice is taken at the later check, "
                                 "and the two currency columns run on from the scheme year's July "
                                 "row, so each month's own figure is the difference inside the "
                                 "scheme year"),
        ("Note on the archive", "where one payment instruction settled both of a partner's "
                                "half-month runs, its amounts stand on both lines and the "
                                "instruction is counted once"),
        ("Note on the reasons", "the reason was free text until the April 2025 release, so the "
                                "earlier entries are folded onto the five reasons on the list, and "
                                "a hold with no reason recorded is shown as its own line"),
        ("Out of scope", "claim months from January 2026, which the check register does not cover, "
                         "and the ceiling's own window of April 2026 to March 2027"),
    ]
    bs["A1"] = "Basis of the annex"
    bs["A1"].font = Font(bold=True, size=12)
    for i, (k, v) in enumerate(rows, start=3):
        bs.cell(row=i, column=1, value=k).font = Font(bold=True)
        cl = bs.cell(row=i, column=2, value=v)
        cl.alignment = Alignment(wrap_text=True, vertical="top")
        if isinstance(v, int):
            cl.number_format = "#,##0"
    bs.column_dimensions["A"].width = 42
    bs.column_dimensions["B"].width = 86
    wb.properties.creator = P.PEOPLE["assurance"][0]
    wb.properties.lastModifiedBy = P.PEOPLE["assurance"][0]
    wb.properties.title = "%s claims assurance annex" % P.SCHEME_SHORT
    wb.properties.created = dt.datetime(2027, 5, 21, 16, 5)
    wb.properties.modified = dt.datetime(2027, 5, 21, 16, 5)
    wb.save(path)
    docs.finalise_xlsx(path, (2027, 5, 21, 16, 5, 0))


def chart(path, fig, test):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    edges, counts = test["hist_edges"], test["hist_counts"]
    f, ax = plt.subplots(1, 2, figsize=(10.4, 3.9))
    mid = 0.5 * (np.array(edges[:-1]) + np.array(edges[1:]))
    ceil4 = fig["bands"][str(P.REF_BAND)]["ceiling"]
    col = ["#c0392b" if m > ceil4 else "#2f4b6e" for m in mid]
    ax[0].bar(mid, counts, width=np.diff(edges), color=col, edgecolor="white", linewidth=0.3)
    ax[0].axvline(ceil4, color="#c0392b", lw=1.3, ls="--")
    ax[0].annotate("ceiling PHP %s\n%.1f%% of band 4 awards referred" % (
        "{:,}".format(ceil4), fig["bands"][str(P.REF_BAND)]["referred_share"]),
        xy=(ceil4, max(counts) * 0.72), xytext=(ceil4 * 1.15, max(counts) * 0.78), fontsize=8,
        color="#c0392b", arrowprops=dict(arrowstyle="-", color="#c0392b", lw=0.8))
    ax[0].set_title("Four-person household awards, twelve months to 31 March 2027", fontsize=9.5)
    ax[0].set_xlabel("Award amount (PHP)", fontsize=8.5)
    ax[0].set_ylabel("Awards", fontsize=8.5)
    top = edges[-1]
    ax[0].set_xlim(0, top)
    ax[0].set_xticks([x for x in range(0, int(top), 5000)])
    ax[0].xaxis.set_major_formatter(FuncFormatter(lambda v, p: "{:,.0f}".format(v)))
    ax[0].annotate("and above", xy=(0.5 * (edges[-2] + top), counts[-1]), xytext=(-2, 9),
                   textcoords="offset points", ha="center", fontsize=7.2, color="#c0392b")
    ax[0].yaxis.set_major_formatter(FuncFormatter(lambda v, p: "{:,.0f}".format(v)))
    bands = [int(b) for b in sorted(fig["bands"], key=int)]
    cl = [fig["bands"][str(b)]["ceiling"] for b in bands]
    sh = [fig["bands"][str(b)]["referred_share"] for b in bands]
    ax[1].step(bands + [7], cl + [cl[-1]], where="post", color="#2f4b6e", lw=1.6)
    ax[1].scatter(bands, cl, s=22, color="#2f4b6e", zorder=3)
    for b, c, s in zip(bands, cl, sh):
        ax[1].annotate("%s\n%.1f%%" % ("{:,}".format(c), s), xy=(b, c), xytext=(0, 7),
                       textcoords="offset points", ha="center", fontsize=7.4, color="#333333")
    ax[1].set_xlim(0.6, 6.9)
    ax[1].set_ylim(0, max(cl) * 1.28)
    ax[1].set_xticks(bands)
    ax[1].set_xticklabels([P.BAND_LABEL[b].replace(" or more persons", "+").replace(" persons", "")
                           .replace(" person", "") for b in bands])
    ax[1].set_title("Ceiling and referred share by household size", fontsize=9.5)
    ax[1].set_xlabel("Household size band", fontsize=8.5)
    ax[1].set_ylabel("Referral ceiling (PHP)", fontsize=8.5)
    ax[1].yaxis.set_major_formatter(FuncFormatter(lambda v, p: "{:,.0f}".format(v)))
    for a in ax:
        a.spines[["top", "right"]].set_visible(False)
        a.tick_params(labelsize=8)
        a.grid(axis="y", color="#e7e7e7", lw=0.6)
        a.set_axisbelow(True)
    f.tight_layout()
    f.savefig(path, dpi=190, metadata={"Software": "", "Creation Time": ""})
    plt.close(f)


def board_paper(path, fig, test, png):
    body, h1, h2, small, cell = docs.styles()
    s = [Paragraph(P.FOUNDATION_LEGAL, small),
         Paragraph("Referral ceiling schedule for 2027/28", h1),
         Paragraph("Board of Trustees, June 2027. Paper from the %s. Prepared by %s, %s."
                   % (P.OFFICE, P.PEOPLE["assurance"][0], P.PEOPLE["assurance"][2]), small),
         Spacer(1, 6),
         Paragraph("Recommendation", h2),
         Paragraph("<b>Set the 2027/28 referral ceiling for a four-person household at PHP %s.</b>"
                   % "{:,}".format(fig["call"]), body),
         Paragraph("The schedule below would refer %.2f per cent of the awards the scheme resolved in "
                   "the twelve months to 31 March 2027, within the %.1f per cent the Board committed "
                   "to in clause 9. PHP %s, the next amount down in Schedule E, would refer "
                   "%.2f per cent and is outside it." %
                   (fig["share_pct"], 100 * P.COMMITTED_SHARE, "{:,}".format(fig["call_down"]),
                    fig["share_down_pct"]), body),
         Paragraph("Schedule", h2)]
    rows = [["Band", "Household size", "Factor", "Ceiling (PHP)", "Awards referred (%)",
             "Award value referred (%)"]]
    for b in P.BANDS:
        d = fig["bands"][str(b)]
        rows.append([RC.legacy_band(b), P.BAND_LABEL[b], "%.3f" % d["factor"],
                     "{:,}".format(d["ceiling"]), "%.1f" % d["referred_share"],
                     "%.1f" % d["referred_value_share"]])
    rows.append(["All", "", "", "", "%.1f" % fig["referred_share"],
                 "%.1f" % fig["referred_value_share"]])
    s.append(docs.grid(rows, [38, 92, 45, 70, 85, 100], cell, align_right=(2, 3, 4, 5)))
    s.append(Spacer(1, 7))
    s.append(Image(png, width=172 * mm, height=64.5 * mm))
    s.append(Paragraph("What the figures rest on", h2))
    s.append(Paragraph(
        "The scheme resolved %s awards in the twelve months, across %d partner-band cells and %d "
        "accredited partners. The claim returns state a total and an award count for each cell, so "
        "the average award in each cell is known exactly; the spread of awards about a partner's own "
        "average is known only from the %s awards the %d portal partners recorded one at a time in "
        "the same months. The schedule is struck on the award distribution those two together imply, "
        "and the award shape has a coefficient of variation of %.2f." %
        ("{:,}".format(fig["awards"]), fig["cells"], fig["partners"],
         "{:,}".format(fig["portal_window_rows"]), fig["portal_partners"], fig["cv"]), body))
    s.append(Paragraph(
        "Struck instead on the distribution of the %d partner-band averages, which carries no spread "
        "within a partner, the ceiling would come out at PHP %s and would refer %.2f per cent of "
        "awards, more than half again the Desk's agreed capacity." %
        (fig["cells"], "{:,}".format(test["default_call"]), test["default_share_pct"]), body))
    s.append(Paragraph(
        "The two reopened claim months, Nov-2026 and Feb-2027, are taken at their revised returns. "
        "The award value referred runs near %.0f per cent in every band because the capital-item "
        "components carry far more value than count." % fig["referred_value_share"], body))
    d = docs.doc(path, "Referral ceiling schedule 2027/28", P.PEOPLE["assurance"][0],
                 "%s referral ceiling schedule for 2027/28" % P.SCHEME_SHORT)
    foot = docs.footer("%s - board paper, June 2027" % P.FOUNDATION)
    with docs.stamped(docs.epoch(2027, 5, 21, 16, 5)):
        d.build(s, onFirstPage=foot, onLaterPages=foot, canvasmaker=docs.org_canvas())
    docs.finalise_pdf(path)


def write(folder, fig, test):
    os.makedirs(folder, exist_ok=True)
    png = os.path.join(folder, PNG)
    schedule_workbook(os.path.join(folder, XLSX), fig)
    annex_workbook(os.path.join(folder, ANNEX), fig)
    chart(png, fig, test)
    board_paper(os.path.join(folder, PDF), fig, test, png)
    os.remove(png)
