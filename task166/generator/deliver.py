"""The golden deliverables, computed from the shipped pack alone (calc.py): returns_allowance_FY2026.xlsx and the one-page
returns_allowance_note.pdf, plus generator/figures.json, every graded figure with its rounding."""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

F_XLSX = "returns_allowance_FY2026.xlsx"
F_PDF = "returns_allowance_note.pdf"
STEP = 250000
QUARTERS = {1: "Q1 Nov-Jan", 2: "Q2 Feb-Apr", 3: "Q3 May-Jul", 4: "Q4 Aug-Oct"}
QUICK = "paperback within %g months" % 8.0


def r250(x):
    return int(STEP * np.floor(x / STEP + 0.5))


def compute(target):
    P = C.Pack(target)
    T = C.dnum(C.YE)
    seg = C.make_quick_seg(P, 8.0, True)
    total, parts, curves = C.development(P, T, seg)
    by_fmt = C.allowance_by_format(parts)
    inv = P.inv[P.inv.terms == "SOR"].copy()
    inv["seg"] = seg(inv)
    op = inv[(inv.day <= T) & (inv.day > T - 365)].copy()
    op["a"] = np.clip((T - op.day) // 7, 0, 70)
    op["rem"] = [curves[k][70] - curves[k][a] for k, a in zip(op.seg, op.a)]
    op["exp_copies"] = op.qty * op.rem
    op["exp_value"] = op.exp_copies * op.net_value / op.qty
    lines = []
    for k, g in op.groupby("seg"):
        f, ch = k.split("|")[0], k.split("|")[1]
        sub = "Hardback, " + QUICK if k.endswith(QUICK) else f
        lines.append(dict(seg=k, fmt=f, sub=sub, channel=ch, copies=int(g.qty.sum()), net=float(g.net_value.sum()),
                          exp_copies=float(g.exp_copies.sum()), exp_value=float(g.exp_value.sum()),
                          ult=float(curves[k][70])))
    L = C.link_editions(P.titles)
    quick = L[L.months <= 8.0]
    quick_open = quick[quick.isbn_hb.isin(op.isbn)]
    bt = {}
    for y in (2024, 2025):
        Ty = C.dnum(dt.date(y, 10, 31))
        est, _, _ = C.development(P, Ty, C.make_quick_seg(P, 8.0, True))
        po = C.open_population(P, Ty)
        f = P.cr[(P.cr.day > Ty) & (P.cr.reason_code == "RET") & P.cr.against_invoice.isin(po.invoice_no)]
        bt[y] = (float(est), float(f.net_value.sum()))
    _, _, gen = C.development(P, T, C.seg_fmt_channel)
    q = op[op.seg.str.endswith(QUICK)]
    base = q.fmt + "|" + q.channel
    q_gen = float(sum(nv * (gen[b][70] - gen[b][a]) for a, nv, b in zip(q.a, q.net_value, base)))
    q_gold = float(q.exp_value.sum())
    rec, dropped = C.receipts_clean(P)
    recv = C.ask_received(P, rec)
    ch_share, fm_share, raw = C.ask_scrapped(P, rec)
    wo = written_off_table(P, rec)
    fy = rec[rec.date.map(C.in_fy2026)]
    wo_all = sum(r[5] for r in wo["channel"]) / sum(r[1] for r in wo["channel"])
    return dict(P=P, total=float(total), by_fmt=by_fmt, lines=lines, curves=curves, quick=quick_open, bt=bt,
                recv=recv, ch_share=ch_share, fm_share=fm_share, raw=raw, wo=wo, q_gold=q_gold, q_gen=q_gen,
                recv_total=int(fy.qty_received.sum()), wo_all=round(100 * wo_all, 1))


def written_off_table(P, rec):
    f = rec[rec.date.map(C.in_fy2026)].copy()
    fin = C.reinspection_final(P, rec).set_index("tote")
    hurts = rec[rec.hurts_tote != ""].groupby("hurts_tote").grade_hurt.sum()
    pul = []
    for t, h in zip(f.hurts_tote, f.grade_hurt):
        if t and t in fin.index and hurts.get(t, 0):
            pul.append(float(fin.loc[t, "pulped"]) * h / hurts[t])
        else:
            pul.append(0.0)
    f["pulped"] = pul
    out = {}
    for key, col, order in (("channel", "channel", C.CHANNELS), ("format", "fmt", C.FORMATS)):
        rows = []
        for v in order:
            g = f[f[col] == v]
            q, u, p = int(g.qty_received.sum()), int(g.grade_unsaleable.sum()), float(g.pulped.sum())
            rows.append((v, q, u, int(g.grade_hurt.sum()), p, u + p, round(100.0 * (u + p) / q, 1) if q else None))
        out[key] = rows
    return out


# ----------------------------------------------------------------------------------------------------------------
# The workbook


def write_xlsx(path, R):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    ws = wb.active
    ws.title = "Allowance"
    bold = Font(name="Calibri", bold=True)
    head = Font(name="Calibri", bold=True, size=13)
    grey = PatternFill("solid", fgColor="E7E6E6")
    thin = Side(style="thin", color="999999")
    money = '#,##0;(#,##0);"-"'
    ws["A1"] = "Marrowgate Books Ltd: returns allowance at 31 October 2026"
    ws["A1"].font = head
    ws["A2"] = ("Trade sales on sale or return invoiced to 31 October 2026; ledger and title master as at 30 October 2026. "
                "For the FY2026 audit file, Finance, 1 November 2026.")
    ws["A4"], ws["B4"] = "Allowance (nearest 250,000)", r250(R["total"])
    ws["A5"], ws["B5"] = "of which hardbacks (nearest 250,000)", r250(R["by_fmt"]["Hardback"])
    ws["A6"], ws["B6"] = "Allowance as computed", round(R["total"])
    for r in (4, 5, 6):
        ws.cell(r, 1).font = bold
        ws.cell(r, 2).number_format = money
    ws["B4"].font = bold
    hdr = ["Segment", "Open copies", "Open net value", "Further returns (copies)", "Allowance", "Share of allowance"]
    r0 = 8
    for j, h in enumerate(hdr, 1):
        c = ws.cell(r0, j, h)
        c.font = bold
        c.fill = grey
        c.alignment = Alignment(wrap_text=True, vertical="top")
    agg = {}
    for x in R["lines"]:
        a = agg.setdefault(x["sub"], [0, 0.0, 0.0, 0.0])
        a[0] += x["copies"]
        a[1] += x["net"]
        a[2] += x["exp_copies"]
        a[3] += x["exp_value"]
    order = ["Hardback, " + QUICK, "Hardback", "Trade paperback", "Paperback"]
    names = {"Hardback, " + QUICK: "Hardbacks, paperback due within 8 months", "Hardback": "Hardbacks, other",
             "Trade paperback": "Trade paperbacks", "Paperback": "Paperbacks"}
    r = r0 + 1
    for k in order:
        if k not in agg:
            continue
        a = agg[k]
        ws.cell(r, 1, names[k])
        ws.cell(r, 2, a[0]).number_format = "#,##0"
        ws.cell(r, 3, round(a[1])).number_format = money
        ws.cell(r, 4, round(a[2])).number_format = "#,##0"
        ws.cell(r, 5, round(a[3])).number_format = money
        ws.cell(r, 6, a[3] / R["total"]).number_format = "0.0%"
        r += 1
    ws.cell(r, 1, "Total").font = bold
    for j, v in ((2, sum(a[0] for a in agg.values())), (3, round(sum(a[1] for a in agg.values()))),
                 (4, round(sum(a[2] for a in agg.values()))), (5, round(R["total"]))):
        c = ws.cell(r, j, v)
        c.font = bold
        c.number_format = "#,##0" if j in (2, 4) else money
        c.border = Border(top=thin)
    ws.cell(r, 6, 1.0).number_format = "0.0%"
    r += 2
    notes = [
        "Basis: copies invoiced to sale-or-return accounts in the twelve months to 31 October 2026, the only copies a return can still quote.",
        "Further returns are each invoice line's copies times the share of copies credited as returns after that line's age, read off the returns "
        "development of invoices from November 2021 at least 425 days old at the year end, by format and channel.",
        "Hardbacks whose own paperback is published within 8 months of them are developed on the earlier hardbacks with a paperback that close, "
        "linked on the title master by title and contributor; credit at each line's own net price.",
    ]
    for t in notes:
        ws.cell(r, 1, t).alignment = Alignment(wrap_text=False)
        r += 1
    ws.column_dimensions["A"].width = 44
    for j in range(2, 7):
        ws.column_dimensions[get_column_letter(j)].width = 16

    # by channel
    ws2 = wb.create_sheet("By channel")
    hdr = ["Format", "Channel", "Open copies", "Open net value", "Returned share to date (mature)", "Further returns (copies)", "Allowance"]
    for j, h in enumerate(hdr, 1):
        c = ws2.cell(1, j, h)
        c.font = bold
        c.fill = grey
    rr = 2
    for x in sorted(R["lines"], key=lambda x: (order.index(x["sub"]), C.CHANNELS.index(x["channel"]))):
        ws2.cell(rr, 1, names[x["sub"]])
        ws2.cell(rr, 2, x["channel"])
        ws2.cell(rr, 3, x["copies"]).number_format = "#,##0"
        ws2.cell(rr, 4, round(x["net"])).number_format = money
        ws2.cell(rr, 5, x["ult"]).number_format = "0.0%"
        ws2.cell(rr, 6, round(x["exp_copies"])).number_format = "#,##0"
        ws2.cell(rr, 7, round(x["exp_value"])).number_format = money
        rr += 1
    for j, w in enumerate([40, 13, 13, 15, 16, 16, 14], 1):
        ws2.column_dimensions[get_column_letter(j)].width = w
    ws2.freeze_panes = "A2"

    # development
    ws3 = wb.create_sheet("Development")
    keys = sorted(R["curves"], key=lambda k: (order.index("Hardback, " + QUICK if k.endswith(QUICK) else k.split("|")[0]),
                                              C.CHANNELS.index(k.split("|")[1])))
    ws3.cell(1, 1, "Cumulative share of invoiced copies credited as returns, by weeks from invoice (invoices 1 Nov 2021 to 1 Sep 2025)").font = bold
    ws3.cell(2, 1, "Weeks").font = bold
    for j, k in enumerate(keys, 2):
        lab = k.replace("|" + QUICK, ", pb within 8m").replace("|", " / ")
        c = ws3.cell(2, j, lab)
        c.font = bold
        c.alignment = Alignment(wrap_text=True)
        ws3.column_dimensions[get_column_letter(j)].width = 13
    for i, wk in enumerate(list(range(0, 66, 4)) + [70], 3):
        ws3.cell(i, 1, wk)
        for j, k in enumerate(keys, 2):
            ws3.cell(i, j, float(R["curves"][k][wk])).number_format = "0.0%"
    ws3.freeze_panes = "B3"

    # linked hardbacks
    ws4 = wb.create_sheet("Paperback links")
    hdr = ["Hardback ISBN", "Hardback title", "Hardback published", "Paperback ISBN", "Paperback title", "Paperback due", "Months"]
    for j, h in enumerate(hdr, 1):
        c = ws4.cell(1, j, h)
        c.font = bold
        c.fill = grey
    q = R["quick"].sort_values(["pub_hb", "isbn_hb"])
    for i, x in enumerate(q.itertuples(), 2):
        ws4.cell(i, 1, x.isbn_hb)
        ws4.cell(i, 2, x.title_hb)
        ws4.cell(i, 3, x.pub_hb).number_format = "dd/mm/yyyy"
        ws4.cell(i, 4, x.isbn_pb)
        ws4.cell(i, 5, x.title_pb)
        ws4.cell(i, 6, x.pub_pb).number_format = "dd/mm/yyyy"
        ws4.cell(i, 7, round(float(x.months), 1)).number_format = "0.0"
    for j, w in enumerate([16, 38, 12, 16, 44, 12, 8], 1):
        ws4.column_dimensions[get_column_letter(j)].width = w
    ws4.freeze_panes = "A2"

    # back-test
    ws5 = wb.create_sheet("Back-test")
    hdr = ["Year end", "Allowance on the same basis", "Returns credited afterwards on the copies then open", "Difference"]
    for j, h in enumerate(hdr, 1):
        c = ws5.cell(1, j, h)
        c.font = bold
        c.fill = grey
    for i, (y, (e, a)) in enumerate(sorted(R["bt"].items()), 2):
        ws5.cell(i, 1, dt.date(y, 10, 31)).number_format = "dd/mm/yyyy"
        ws5.cell(i, 2, round(e)).number_format = money
        ws5.cell(i, 3, round(a)).number_format = money
        ws5.cell(i, 4, e / a - 1).number_format = "0.0%"
    for j, w in enumerate([12, 26, 44, 12], 1):
        ws5.column_dimensions[get_column_letter(j)].width = w

    # returns received
    ws6 = wb.create_sheet("Returns received")
    ws6.cell(1, 1, "Copies of Marrowgate titles received back at Tallowmere, FY2026 (1 November 2025 to 31 October 2026)").font = bold
    hdr = ["Channel"] + [QUARTERS[q] for q in (1, 2, 3, 4)] + ["FY2026"]
    for j, h in enumerate(hdr, 1):
        c = ws6.cell(2, j, h)
        c.font = bold
        c.fill = grey
    for i, ch in enumerate(C.CHANNELS, 3):
        ws6.cell(i, 1, ch)
        for j, qq in enumerate((1, 2, 3, 4), 2):
            ws6.cell(i, j, R["recv"][(ch, qq)]).number_format = "#,##0"
        ws6.cell(i, 6, sum(R["recv"][(ch, qq)] for qq in (1, 2, 3, 4))).number_format = "#,##0"
    i = 3 + len(C.CHANNELS)
    ws6.cell(i, 1, "Total").font = bold
    for j, qq in enumerate((1, 2, 3, 4), 2):
        c = ws6.cell(i, j, sum(R["recv"][(ch, qq)] for ch in C.CHANNELS))
        c.number_format = "#,##0"
        c.font = bold
    c = ws6.cell(i, 6, sum(R["recv"].values()))
    c.number_format = "#,##0"
    c.font = bold
    ws6.column_dimensions["A"].width = 14
    for j in range(2, 7):
        ws6.column_dimensions[get_column_letter(j)].width = 13

    # written off
    ws7 = wb.create_sheet("Written off")
    ws7.cell(1, 1, "Copies received back in FY2026 and written off by 31 October 2026: graded unsaleable on receipt, or hurt and pulped at re-inspection").font = bold
    hdr = ["", "Copies received", "Graded unsaleable", "Graded hurt", "Hurts pulped by 31 Oct 2026", "Written off", "Share written off"]
    rr = 3
    for key, lab in (("channel", "Channel"), ("format", "Format")):
        for j, h in enumerate([lab] + hdr[1:], 1):
            c = ws7.cell(rr, j, h)
            c.font = bold
            c.fill = grey
        rr += 1
        for v, q, u, h, p, w, s in R["wo"][key]:
            ws7.cell(rr, 1, v)
            ws7.cell(rr, 2, q).number_format = "#,##0"
            ws7.cell(rr, 3, u).number_format = "#,##0"
            ws7.cell(rr, 4, h).number_format = "#,##0"
            ws7.cell(rr, 5, round(p, 1)).number_format = "#,##0.0"
            ws7.cell(rr, 6, round(w, 1)).number_format = "#,##0.0"
            ws7.cell(rr, 7, s / 100.0).number_format = "0.0%"
            rr += 1
        rr += 1
    ws7.cell(rr, 1, "A tote's pulped copies are shared among the deliveries whose hurts went into it, in proportion to those hurts.")
    ws7.column_dimensions["A"].width = 16
    for j in range(2, 8):
        ws7.column_dimensions[get_column_letter(j)].width = 15
    wb.save(path)


# ----------------------------------------------------------------------------------------------------------------
# The note


def write_pdf(path, R):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    body = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13, spaceAfter=6)
    title = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=2)
    small = ParagraphStyle("s", fontName="Helvetica", fontSize=8.2, leading=10.5, textColor=colors.HexColor("#444444"))
    tot, hb = R["total"], R["by_fmt"]["Hardback"]
    agg = {}
    for x in R["lines"]:
        agg[x["sub"]] = agg.get(x["sub"], 0.0) + x["exp_value"]
    bt = R["bt"]
    memo = Table([["To", "FY2026 year-end audit file"], ["From", "%s, Group Financial Controller" % K.PEOPLE["controller"]],
                  ["Date", "1 November 2026"], ["Subject", "Returns allowance at 31 October 2026"]], colWidths=[20 * mm, 120 * mm])
    memo.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.6), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.6),
                              ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                              ("LEFTPADDING", (0, 0), (-1, -1), 0), ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.grey)]))
    s = [Paragraph("Hold £%s million against returns at 31 October 2026" % ("%.2f" % (r250(tot) / 1e6)), title),
         Spacer(1, 4), memo, Spacer(1, 8),
         Paragraph("<b>Allowance: £%s</b> (to the nearest £250,000; computed £%s), of which hardbacks £%s "
                   "(computed £%s)." % ("{:,}".format(r250(tot)), "{:,}".format(round(tot)), "{:,}".format(r250(hb)),
                                             "{:,}".format(round(hb))), body),
         Paragraph("The allowance is the credit we expect to give for copies invoiced on or before 31 October 2026 that will "
                   "come back under our terms of trade. A return can only quote an invoice three to twelve months old, so the "
                   "copies at stake are those invoiced on sale or return in the twelve months to the year end.", body),
         Paragraph("We developed the returns by format and channel: for invoices from November 2021 that are at least 425 days "
                   "old, the share of invoiced copies credited as returns by weeks since the invoice; each open invoice line "
                   "takes the share still to come after its age, at its own net price.", body),
         Paragraph("A hardback's remaining shop stock comes back once its own paperback is out. Most of the autumn 2026 "
                   "hardbacks have their paperbacks due four to five months after publication, against about a year for the "
                   "hardbacks the history mostly holds. We matched each hardback to its paperback on the title master by title "
                   "and contributor (the paperback carries its own ISBN and is often retitled) and developed the hardbacks "
                   "whose paperback comes within 8 months on the earlier hardbacks with a paperback that close. Their open "
                   "invoices carry £%s of the allowance; on the general hardback pattern the same copies would carry "
                   "£%s." % ("{:,}".format(int(round(R["q_gold"], -3))), "{:,}".format(int(round(R["q_gen"], -3)))), body),
         Paragraph("Struck the same way at 31 October 2024 and 2025, the allowance came to %s and %s the returns credited "
                   "afterwards on the copies then open." % (_vs(bt[2024]), _vs(bt[2025])), body),
         Spacer(1, 4)]
    names = [("Hardback, " + QUICK, "Hardbacks, paperback due within 8 months"), ("Hardback", "Hardbacks, other"),
             ("Trade paperback", "Trade paperbacks"), ("Paperback", "Paperbacks")]
    data = [["Segment", "Allowance (£)"]] + [[n, "{:,}".format(int(round(agg.get(k, 0.0))))] for k, n in names if k in agg]
    data.append(["Total", "{:,}".format(int(round(tot)))])
    t = Table(data, colWidths=[95 * mm, 40 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                           ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 9), ("ALIGN", (1, 0), (1, -1), "RIGHT"),
                           ("LINEABOVE", (0, -1), (-1, -1), 0.5, colors.grey), ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.grey)]))
    s.append(t)
    s.append(Paragraph("Source: sales ledger invoice and credit lines and the title master, both as at 30 October 2026; "
                       "sale-or-return accounts only.", small))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Claims for damage or shortage in transit are credited against revenue when agreed and form no part of "
                       "the allowance (accounting policies, Revenue); they are left out of the returns development. Workings, the "
                       "returns received in FY2026 and the copies written off are in returns_allowance_FY2026.xlsx.", small))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, "Marrowgate Books Ltd  |  Finance  |  FY2026 year end")
        canvas.drawRightString(190 * mm, 10 * mm, "Page 1 of 1")
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                          title="Returns allowance at 31 October 2026", author=K.PEOPLE["controller"], subject="Returns allowance",
                          creator="Microsoft Word", producer="Microsoft Word")
    d.build(s, onFirstPage=footer, onLaterPages=footer)


def figures(R):
    out = {"allowance_gbp": {"value": r250(R["total"]), "computed": round(R["total"], 2), "rounding": "nearest 250,000"},
           "allowance_hardback_gbp": {"value": r250(R["by_fmt"]["Hardback"]), "computed": round(R["by_fmt"]["Hardback"], 2),
                                      "rounding": "nearest 250,000"},
           "received_copies": {"%s|Q%d" % k: v for k, v in sorted(R["recv"].items(), key=lambda kv: (C.CHANNELS.index(kv[0][0]), kv[0][1]))},
           "written_off_share_channel_pct": R["ch_share"], "written_off_share_format_pct": R["fm_share"],
           "steps": {"allowance_gbp_millions": r250(R["total"]) / 1e6,
                     "allowance_hardback_gbp_millions": r250(R["by_fmt"]["Hardback"]) / 1e6,
                     "paperback_within_months": 8, "maturity_days": 425,
                     "received_total_copies": R["recv_total"], "written_off_share_all_pct": R["wo_all"],
                     "as_of": "31 October 2026", "back_test_year_ends": "31 October 2024 and 31 October 2025",
                     "financial_year": "1 November 2025 to 31 October 2026", "extract_from": "1 November 2021",
                     "back_test": {"31 October 2024": _vs(R["bt"][2024]), "31 October 2025": _vs(R["bt"][2025])}}}
    return out


def _vs(pair):
    e, a = pair
    d = 100 * (e / a - 1)
    return "%.1f%% %s" % (abs(d), "below" if d < 0 else "above")


def main(target, golden, fig_path):
    os.makedirs(golden, exist_ok=True)
    R = compute(target)
    xp, pp = os.path.join(golden, F_XLSX), os.path.join(golden, F_PDF)
    write_xlsx(xp, R)
    PP.normalize_ooxml(xp, K.PEOPLE["controller"], K.PEOPLE["controller"], "2026-11-01T10:12:00Z", "2026-11-01T16:48:00Z",
                       excel=True, company=K.COMPANY)
    write_pdf(pp, R)
    PP.normalize_pdf(pp, b"D:20261101170500+00'00'", b"D:20261101170500+00'00'")
    with open(fig_path, "w") as fh:
        json.dump(figures(R), fh, indent=1)
        fh.write("\n")
    return R


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(HERE), "golden")
    main(t, g, os.path.join(HERE, "figures.json"))
