"""task183 goldens: fci_referrals_jan2027.docx (the referral paper with the chart) and cash_review_2026.xlsx (the
An Post and till service months), every figure computed from target/ by calc.py, and generator/figures.json."""
from __future__ import annotations

import io
import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "task183"
matplotlib.rcParams["font.family"] = "DejaVu Sans"
import matplotlib.pyplot as plt                                   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C           # noqa: E402
import postprocess as PP   # noqa: E402

MONTH_NAME = {m: n for m, n in zip(C.MONTHS, ["October 2025", "November 2025", "December 2025", "January 2026",
                                              "February 2026", "March 2026", "April 2026", "May 2026", "June 2026",
                                              "July 2026", "August 2026", "September 2026"])}


def nearest5k(x):
    return int(5000 * round(x / 5000.0))


def others_bound(P, referred):
    """An upper bound on every non-referred customer's figure over every reading the records leave standing (the
    estimator family and the edge of the year's card trade), rounded up to the thousand."""
    import math
    vals = []
    for kw in ({}, dict(kind="wls"), dict(kind="huber"), dict(kind="days"), dict(fit_on="all"),
               dict(net_refunds=False)):
        f = C.unexplained(P, **kw)
        vals += [f[c] for c in P.cust if c not in referred]
    lods, card = P.lodgements(), P.card_by_day()
    for cid in P.cust:
        if cid in referred or cid in P.till_cids:
            continue
        pairs = [p for p in C.windows(lods.get(cid, []), card.get(cid, {})) if C.in_year(p[0])]
        _, s, _, _ = C.fit(pairs, "ols")
        vals.append(sum(L["amount"] for L, _, _ in pairs) - s * sum(
            v for d, v in card.get(cid, {}).items() if C.REVIEW_START <= d <= C.REVIEW_END))
    return int(1000 * math.ceil(max(vals) / 1000.0))


def figures(target):
    P = C.Pack(target)
    fig, referred = C.golden(P)
    apg = C.ap_figures(target, "golden")
    tg = C.till_figures_ask(P, target, "golden")
    lods, card = P.lodgements(), P.card_by_day()
    refs = []
    for cid in referred:
        s = P.cust[cid]
        pairs = [p for p in C.windows(lods[cid], card[cid]) if C.in_year(p[0])]
        a, sl, _, _ = C.fit(pairs, "ols")
        refs.append(dict(customer=cid, name=s["Trading name"], trade=s["Trade"], branch=s["Home branch"],
                         account=s["Current account"], unexplained_eur=round(fig[cid], 2),
                         referral_cash_eur=nearest5k(fig[cid]), lodgements=len(pairs),
                         fixed_per_lodgement_eur=int(round(a)), own_ratio=round(sl, 2)))
    _, _, info = C.default_path(P)
    rel = {c: info["ratio"][c] / info["peer"][P.cust[c]["Trade"]] for c in P.cust}
    heavy = [c for c, _ in sorted(rel.items(), key=lambda kv: -kv[1])[:2]]
    tills = sorted(rel[c] - 1.0 for c in P.till_cids)
    return dict(
        line_eur=40000,
        highest_other_eur=int(round(max(v for c, v in fig.items() if c not in referred))),
        not_referred=[dict(customer=c, name=P.cust[c]["Trading name"], times_trade_median=round(rel[c], 1))
                      for c in heavy],
        till_customers=dict(count=len(P.till_cids), below_trade_median_pct=round(-100 * tills[0], 0),
                            above_trade_median_pct=round(100 * tills[-1], 0)),
        referrals=refs,
        reviewed={cid: round(fig[cid], 2) for cid in sorted(fig)},
        an_post={m: dict(cash_eur=apg[m][1], fee_eur=apg[m][2]) for m in C.MONTHS},
        till={m: dict(cash_sales_eur=tg[m][1], paid_outs_eur=tg[m][2]) for m in C.MONTHS})


INK, INK2, MUTED, GRID = "#1d2126", "#52575e", "#8a9099", "#e3e5e8"
BAR, HOT, LINE = "#9fb3c8", "#123f6b", "#b23a2e"


def chart_png(f, names):
    items = sorted(f["reviewed"].items(), key=lambda kv: kv[1])
    ref = {r["customer"] for r in f["referrals"]}
    fig, ax = plt.subplots(figsize=(7.2, 7.6), dpi=150)
    fig.patch.set_facecolor("white")
    ys = range(len(items))
    ax.barh(list(ys), [v / 1000.0 for _, v in items], height=0.72,
            color=[HOT if c in ref else BAR for c, _ in items], zorder=3)
    ax.axvline(40, color=LINE, lw=1.3, zorder=4)
    ax.text(40.8, 1.0, "EUR 40,000\nreferral line", color=LINE, fontsize=7.5, va="bottom")
    for y, (c, v) in zip(ys, items):
        if c in ref:
            ax.text(v / 1000.0 + 1.2, y, "%s  (%s)" % (names[c], c), va="center", fontsize=7.5, color=INK,
                    fontweight="bold")
    ax.axvline(0, color=MUTED, lw=0.8, zorder=2)
    ax.set_yticks([])
    ax.set_xlabel("Unexplained cash, review year 2025-26 (EUR thousand)", fontsize=8.5, color=INK2)
    ax.set_xlim(-20, 145)
    ax.tick_params(axis="x", colors=MUTED, labelsize=8, length=0)
    ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.set_title("Only two customers lodged more than EUR 40,000 their own trading did not take", fontsize=9.5,
                 color=INK, loc="left", pad=10)
    ax.text(0.0, -0.075, "One bar per customer on the 2025-26 review list (%d). Referrals in dark blue." % len(items),
            transform=ax.transAxes, fontsize=7.2, color=MUTED)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_docx(path, f, png):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt, RGBColor

    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(2.0)
    h = d.add_paragraph()
    r = h.add_run("Lough Ree Bank DAC  |  Financial Crime Operations")
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x12, 0x3F, 0x6B)
    r.bold = True
    t = d.add_paragraph()
    r = t.add_run("Business cash review 2025-26: two customers referred to Financial Crime Investigations")
    r.bold = True
    r.font.size = Pt(14)
    meta = d.add_table(rows=4, cols=2)
    for i, (k, v) in enumerate([("To", "Financial Crime Risk Committee, meeting of 21 January 2027"),
                                ("From", "Malachy Crohan, Head of Financial Crime Operations"),
                                ("Date", "6 November 2026"),
                                ("Under", "BCR-3, Business Cash Review Standard, issue 3, sections 4.1 to 4.3")]):
        meta.cell(i, 0).text = k
        meta.cell(i, 1).text = v
        meta.cell(i, 0).paragraphs[0].runs[0].bold = True
        meta.cell(i, 0).width = Cm(2.4)
        meta.cell(i, 1).width = Cm(14.2)
    d.add_paragraph()
    n = len(f["reviewed"])
    refs = f["referrals"]
    d.add_paragraph(
        "We reviewed the %d customers on the cash-intensive segment's list for the year to 30 September 2026. "
        "%s customers lodged more than EUR 40,000 that their own trading did not take, and we refer them to "
        "Financial Crime Investigations. Their accounts are restricted from the committee's decision until "
        "Investigations closes each case (BCR-3 4.3). A referral is not a finding of wrongdoing (4.4)."
        % (n, "Two" if len(refs) == 2 else str(len(refs))))
    tb = d.add_table(rows=1 + len(refs), cols=5)
    tb.style = "Light Grid Accent 1"
    for j, hd in enumerate(["Customer", "Trading name", "Trade", "Home branch", "Unexplained cash"]):
        tb.cell(0, j).text = hd
    for i, rr in enumerate(refs, 1):
        vals = [rr["customer"], rr["name"].split(",")[0], rr["trade"], rr["branch"],
                "EUR %s" % format(rr["referral_cash_eur"], ",")]
        for j, v in enumerate(vals):
            tb.cell(i, j).text = v
        tb.cell(i, 4).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    src = d.add_paragraph("Source: account export and merchant services daily trade, review year 2025-26. Unexplained "
                          "cash to the nearest EUR 5,000 (BCR-3 4.1, 4.3).")
    src.runs[0].font.size = Pt(8.5)
    src.runs[0].font.color.rgb = RGBColor(0x5D, 0x65, 0x70)
    d.add_paragraph()
    d.add_paragraph("How the figures were reached", style="Heading 2")
    d.add_paragraph(
        "For each customer we set every cash lodgement in the year against the card trade its terminals took on the "
        "trading days since its previous lodgement, the days whose takings it carried. A customer's cash moves with "
        "its card trade at a ratio of its own, so we fitted that ratio, with a fixed part per lodgement, to the "
        "customer's own lodgements. The cash its trading took is that ratio times the card trade of the days its "
        "lodgements in the year carried; the rest of what it lodged is unexplained. For the customers on our till service BCR-3 4.2 applies and the "
        "till's own cash sales are the measure.")
    tc = f["till_customers"]
    d.add_paragraph(
        "The %d till customers show why the comparison has to be with each business's own trade. Their lodgements "
        "match the till's cash, net of paid-outs, over the same days to the cent, with no fixed part, yet their cash "
        "per euro of card trade runs from %d per cent below to %d per cent above their trade's median. A trade "
        "average would have mis-stated every one of them." % (tc["count"], tc["below_trade_median_pct"],
                                                              tc["above_trade_median_pct"]))
    for rr in refs:
        d.add_paragraph("%s, %s (%s)" % (rr["name"], rr["customer"], rr["account"]), style="Heading 3")
        d.add_paragraph(
            "Each of its %d lodgements in the year carried about EUR %s more than the card trade of its days "
            "explains, in busy weeks and quiet ones alike. The cash that does move with its trade runs at %s cent a "
            "euro of card trade, light for the trade. Over the year the fixed part comes to EUR %s to the nearest "
            "five thousand." % (rr["lodgements"], format(rr["fixed_per_lodgement_eur"], ","),
                               "%d" % round(100 * rr["own_ratio"]), format(rr["referral_cash_eur"], ",")))
    nr = f["not_referred"]
    d.add_paragraph("Not referred", style="Heading 2")
    d.add_paragraph(
        "%s (%s) and %s (%s) lodge the most cash per euro of card trade against their trades, %s and %s times "
        "their trade's median. Their cash rises and falls with their own card trade lodgement by lodgement, with no "
        "fixed part, so their own trading took it, and neither is referred."
        % (nr[0]["name"], nr[0]["customer"], nr[1]["name"], nr[1]["customer"], nr[0]["times_trade_median"],
           nr[1]["times_trade_median"]))
    d.add_paragraph()
    d.add_picture(io.BytesIO(png), width=Cm(15.5))
    cap = d.add_paragraph("Figure 1. Unexplained cash by customer, review year 2025-26.")
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(9)
    d.add_paragraph()
    d.add_paragraph(
        "The monthly An Post and till service figures that support this paper are in cash_review_2026.xlsx.")
    fn = d.add_paragraph(
        "Note. Post office lodgements are dated by the counter day carried in the An Post reference, not the day "
        "they were credited (BCR-3 3.2). The account export repeats April to June 2026 in full; each posting is "
        "counted once.")
    fn.runs[0].font.size = Pt(8.5)
    fn.runs[0].font.color.rgb = RGBColor(0x5D, 0x65, 0x70)
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    fp = d.sections[0].footer.paragraphs[0]
    fr = fp.add_run("Lough Ree Bank DAC  |  Financial Crime Operations  |  Restricted  |  Page ")
    fr.font.size = Pt(8)
    run = fp.add_run()
    run.font.size = Pt(8)
    for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)
    d.core_properties.author = "Malachy Crohan"
    d.save(path)


def write_xlsx(path, f):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "An Post"
    ws.append(["Business lodgements taken at post office counters for the Bank, review year 2025-26"])
    ws["A1"].font = Font(bold=True, size=11)
    ws.append(["Cash is notes and coin together. Agency fee per Schedule 2: EUR 1.15 a lodgement plus 0.065% of the "
               "cash, each lodgement's fee to the cent."])
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws.append([])
    ws.append(["Month", "Cash lodged (EUR)", "Agency fee due (EUR)"])
    for c in ws[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="123F6B")
    for m in C.MONTHS:
        ws.append([MONTH_NAME[m], f["an_post"][m]["cash_eur"], f["an_post"][m]["fee_eur"]])
    ws.append(["Year", round(sum(f["an_post"][m]["cash_eur"] for m in C.MONTHS), 2),
               round(sum(f["an_post"][m]["fee_eur"] for m in C.MONTHS), 2)])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=5, min_col=2, max_col=3):
        for c in row:
            c.number_format = "#,##0.00"
            c.alignment = Alignment(horizontal="right")
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 22
    ws.freeze_panes = "A5"
    ws2 = wb.create_sheet("Till service")
    ws2.append(["Till service: cash sales and paid-outs recorded, all till-service customers, review year 2025-26"])
    ws2["A1"].font = Font(bold=True, size=11)
    ws2.append(["Each Z-report is placed on the trading day it closed. Figures as the tills recorded them."])
    ws2["A2"].font = Font(italic=True, size=9, color="555555")
    ws2.append([])
    ws2.append(["Month", "Cash sales (EUR)", "Paid-outs (EUR)"])
    for c in ws2[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="123F6B")
    for m in C.MONTHS:
        v = f["till"][m]
        ws2.append([MONTH_NAME[m], v["cash_sales_eur"], v["paid_outs_eur"]])
    ws2.append(["Year", round(sum(f["till"][m]["cash_sales_eur"] for m in C.MONTHS), 2),
                round(sum(f["till"][m]["paid_outs_eur"] for m in C.MONTHS), 2)])
    for c in ws2[ws2.max_row]:
        c.font = Font(bold=True)
    for row in ws2.iter_rows(min_row=5, min_col=2, max_col=3):
        for c in row:
            c.number_format = "#,##0.00"
    for col, w in zip("ABC", (18, 18, 18)):
        ws2.column_dimensions[col].width = w
    ws2.freeze_panes = "A5"
    ws3 = wb.create_sheet("Notes")
    for line in [
        "Business cash review 2025-26: supporting months for the referral paper of 6 November 2026.",
        "",
        "An Post: every business lodgement a post office counter took for the Bank, in the month the counter took it "
        "(Schedule 2, 1.3).",
        "Cash is notes and coin together. Fees are Schedule 2's EUR 1.15 a lodgement and 0.065% of its cash, each "
        "lodgement's fee rounded to the cent.",
        "An Post's file for 21 January 2026 arrived twice; each lodgement is counted once.",
        "",
        "Till service: every Z-report in the service's central log, on the trading day it closed, all till-service "
        "customers.",
        "Cash sales and paid-outs as the tills recorded them.",
    ]:
        ws3.append([line or None])
    ws3.column_dimensions["A"].width = 120
    ws3["A1"].font = Font(bold=True)
    wb.save(path)


def main(target, golden, figs_path):
    os.makedirs(golden, exist_ok=True)
    f = figures(target)
    P = C.Pack(target)
    names = {cid: P.cust[cid]["Trading name"].split(",")[0] for cid in P.cust}
    png = chart_png(f, names)
    dpath = os.path.join(golden, "fci_referrals_jan2027.docx")
    write_docx(dpath, f, png)
    PP.normalize_ooxml(dpath, "Malachy Crohan", "Malachy Crohan", "2026-11-04T09:12:00Z", "2026-11-06T16:48:00Z",
                       title="Business cash review 2025-26: referrals to Financial Crime Investigations")
    xpath = os.path.join(golden, "cash_review_2026.xlsx")
    write_xlsx(xpath, f)
    PP.normalize_ooxml(xpath, "Conall Mulgrew", "Malachy Crohan", "2026-11-03T10:05:00Z", "2026-11-06T15:20:00Z",
                       excel=True)
    with open(figs_path, "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return f
